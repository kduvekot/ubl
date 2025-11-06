# UBL Build Test Results - Restricted Environment

**Test Date:** 2025-11-06
**Environment:** Claude Code Restricted Container
**Test Command:** `bash build.sh target local test-build "" ""`

---

## Executive Summary

❌ **BUILD FAILED** - The build cannot complete due to blocked external access to critical domains.

**Primary Failure:** Google Sheets download blocked by proxy
**Secondary Failure:** Missing system packages (7z, aspell, pandoc)

---

## Test Results Details

### ✅ What Worked

1. **Java Build System**
   - Java 21 detected and functional
   - Apache Ant 1.9.7 executed successfully
   - Saxon XSLT processor operational
   - All bundled JAR dependencies loaded correctly

2. **Partial File Operations**
   - Successfully copied 2,124 files from `raw/` directory to target
   - Created complete directory structure (18 directories)
   - Copied 236 artifact files including:
     - 10 common XSD schema fragments
     - Validation libraries
     - JSON schema templates
     - Sample XML files

3. **Build Script Execution**
   - build.sh and build-common.sh executed without syntax errors
   - Build logging working (created build.console.test-build.txt)
   - Exit code tracking functional

---

### ❌ Critical Failures

#### 1. Google Sheets Download - BLOCKED

**Error Location:** build.xml line 34-42

```
[exec] --2025-11-06 11:02:13--  https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g/export?format=ods
[exec] Connecting to 21.0.0.139:15004... connected.
[exec] Proxy request sent, awaiting response... 307 Temporary Redirect
[exec] Location: https://doc-0g-40-sheets.googleusercontent.com/export/...
[exec] Proxy tunneling failed: ForbiddenUnable to establish SSL connection.
[exec] Result: 4
```

**Root Cause:**
- Initial request to `docs.google.com` succeeds (domain whitelisted)
- Google redirects (HTTP 307) to `doc-0g-40-sheets.googleusercontent.com`
- Proxy blocks the redirect domain with "403 Forbidden"
- Result: Empty 0-byte ODS file created

**Impact:**
- Cannot generate UBL-Signature-Entities-2.5.gc (genericode file)
- Cannot generate UBL-Library-Entities-2.5.gc
- Cannot generate UBL-Documents-Entities-2.5.gc
- BUILD FAILS at XSD schema generation step

**Required Fix:** Add `*.googleusercontent.com` to proxy whitelist

---

#### 2. Package Manager Access - BLOCKED

**Error:**
```
Err:1 http://archive.ubuntu.com/ubuntu noble/main amd64 libtext-iconv-perl amd64 1.7-8build3
  403  Forbidden [IP: 21.0.0.139 15004]
```

**Missing Packages:**
- `p7zip-full` - Required for creating 7z archives (line 29-33 in build-common.sh)
- `aspell` - Required for spell checking documentation
- `pandoc` - Required for document format conversion

**Impact:**
- 7z archiving fails with "command not found"
- Cannot create final distribution archives
- Documentation generation would fail (if it got that far)

**Required Fix:** Add Ubuntu repository domains to proxy whitelist OR pre-install packages in Docker image

---

#### 3. Documentation Publishing - SKIPPED

**Status:** Not tested (skipped due to empty credentials)

```
[echo] !!!!!!!!!!!!!! Incomplete execution requested: documentation not being
       generated in the absence of secret values!!!!!!!!!!!!!!!!
```

**Impact:** Would fail if tested due to blocked `api.realtaonline.com` access

---

## Detailed Network Access Analysis

### Observed Network Requests

1. **docs.google.com** - ✅ ALLOWED
   - Initial connection succeeds
   - HTTP request accepted by proxy

2. **doc-0g-40-sheets.googleusercontent.com** - ❌ BLOCKED
   - Google's CDN for spreadsheet exports
   - Proxy returns "403 Forbidden"
   - SSL tunnel establishment fails

3. **archive.ubuntu.com** - ❌ BLOCKED
   - Ubuntu package repository
   - HTTP requests return "403 Forbidden"

4. **security.ubuntu.com** - ❌ BLOCKED (from earlier test)
   - Ubuntu security updates
   - HTTP requests return "403 Forbidden"

---

## Required Domain Whitelist

### CRITICAL (Build Cannot Proceed Without These)

```
✅ docs.google.com                         [ALREADY ALLOWED]
❌ *.googleusercontent.com                 [NEEDS WHITELIST] ⚠️ CRITICAL
   └─ Specifically: doc-*-sheets.googleusercontent.com
❌ archive.ubuntu.com                      [NEEDS WHITELIST]
❌ security.ubuntu.com                     [NEEDS WHITELIST]
```

### IMPORTANT (For Full Build with Documentation)

```
❌ api.realtaonline.com/v2                 [NEEDS WHITELIST]
❌ qatest-api.realtaonline.com/v2          [NEEDS WHITELIST]
❌ dev-api.realtaonline.com/v2             [NEEDS WHITELIST]
```

---

## Alternative Solutions (If Whitelisting Not Possible)

### Option 1: Pre-install System Packages in Docker Image

Modify the Docker image to include:
```dockerfile
RUN apt update && apt install -y \
    p7zip-full \
    aspell \
    aspell-en \
    pandoc \
    libreoffice
```

**Pros:** Eliminates need for Ubuntu repository access
**Cons:** Increases image size by ~210MB

---

### Option 2: Use Cached Google Sheets (Manual Download)

As documented in ENVIRONMENT_SETUP.md:84-89, place pre-downloaded ODS files in parent directory:

```bash
# Place these files in /home/user/ubl/
UBL-Signature-Google.ods
UBL-Library-Google.ods
UBL-Documents-Google.ods
```

**Pros:** No network access needed for build
**Cons:**
- Manual download required before each build
- Files become stale unless regularly updated
- Requires download outside restricted environment

---

### Option 3: Skip Documentation Generation

Run build without Réalta credentials:
```bash
bash build.sh target local test-build "" ""
```

**Pros:** Reduces external dependencies
**Cons:**
- No HTML/PDF documentation generated
- Still requires Google Sheets access
- Still requires 7z for archiving

---

## Build Artifacts Created (Partial)

Despite failure, the build created:

```
target/
├── csd01-2.5/                    # Partial artifact directory
│   ├── cl/                       # Code lists (empty)
│   ├── json/                     # Sample JSON (copied from raw)
│   ├── json-schema/              # JSON schema fragments
│   ├── mod/                      # Model documentation fragments
│   ├── val/                      # Validation tools
│   ├── xml/                      # Sample XML files
│   ├── xsd/common/               # 10 common XSD files
│   └── xsdrt/common/             # 10 runtime XSD files
├── Endorsed-csd01-2.5/           # Endorsed subset (partial)
├── UBL-2.5-csd01-test-build-archive-only/
│   ├── build.console.test-build.txt    # Build log
│   └── build.exitcode.test-build.txt   # Exit code: 1
└── Various metadata and support files

Total: 236 files copied, 18 directories created
```

---

## What's Missing from Build Output

Due to blocked Google Sheets access, these were NOT generated:

1. **Genericode Files:**
   - UBL-Signature-Entities-2.5.gc
   - UBL-Entities-2.5.gc (library + documents combined)

2. **Generated XSD Schemas:**
   - All document schemas (Invoice, Order, etc.)
   - All library component schemas
   - Common aggregate/basic components

3. **Code Lists:**
   - No code list files generated

4. **Validation Artefacts:**
   - Schematron validation files
   - CVA validation files

5. **Documentation:**
   - HTML documentation
   - PDF documentation
   - ODS spreadsheet reports

---

## Recommendations

### Immediate Action (Priority 1)

1. **Add `*.googleusercontent.com` to proxy whitelist**
   - This is the CRITICAL blocker
   - Without this, build cannot proceed past initialization
   - Google Sheets exports redirect to this domain

2. **Add Ubuntu repository domains to proxy whitelist OR pre-install packages**
   - `archive.ubuntu.com`
   - `security.ubuntu.com`
   - Alternative: Modify Docker image to pre-install p7zip-full, aspell, pandoc

### Future Enhancements (Priority 2)

3. **Add Réalta API domains** (if full documentation needed)
   - `api.realtaonline.com`
   - `qatest-api.realtaonline.com`
   - `dev-api.realtaonline.com`

### Testing Plan

After whitelisting changes:
1. Re-run build test with same command
2. Verify Google Sheets download succeeds
3. Verify genericode files are generated
4. Verify XSD schemas are created
5. Verify 7z archives are created
6. Test with Réalta credentials (optional)

---

## Technical Details

### Environment Information

- **Container:** Claude Code Remote Cloud Default
- **OS:** Linux 4.4.0 / Ubuntu 24.04 Noble
- **Java:** OpenJDK 21.0.8
- **Ant:** Apache Ant 1.9.7
- **User:** root (uid=0, gid=0)
- **Working Directory:** /home/user/ubl
- **Proxy:** 21.0.0.139:15004 (JWT authenticated)

### Build Configuration Used

```bash
export title="UBL 2.5"
export package=UBL-2.5
export UBLversion=2.5
export UBLstage=csd01
export UBLprevStageVersion=2.4
export UBLprevStage=os
export UBLprevVersion=2.4
export rawdir=raw
export includeISO=false

export libGoogle=https://docs.google.com/spreadsheets/d/18o1YqjHWUw0-s8mb3ja4i99obOUhs-4zpgso6RZrGaY
export docGoogle=https://docs.google.com/spreadsheets/d/1024Th-Uj8cqliNEJc-3pDOR7DxAAW7gCG4e-pbtarsg
export sigGoogle=https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g
```

---

## Conclusion

The UBL build process **CANNOT COMPLETE** in the current restricted environment due to:

1. **Critical:** Google Sheets download redirect blocked (googleusercontent.com)
2. **Critical:** Missing system packages (7z, aspell, pandoc)
3. **Important:** Documentation API blocked (realtaonline.com)

**Minimum required changes:**
- Whitelist `*.googleusercontent.com`
- Whitelist `archive.ubuntu.com` and `security.ubuntu.com` OR pre-install packages

With these changes, the build should succeed through artifact generation. Full documentation would require additional Réalta API access.
