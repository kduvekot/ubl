# Enabling Secure UBL Builds in Restricted Environments

**Date:** 2025-10-24
**Context:** Analysis of build requirements vs security restrictions
**Current Issue:** Build fails due to network restrictions and missing dependencies

---

## Current Problems Identified

### Issue 1: Network Access Restrictions

```
❌ apt-get: 403 Forbidden
   URL: ppa.launchpadcontent.net
   Reason: Package repository access blocked

❌ wget: 403 Forbidden
   URL: docs.google.com/spreadsheets/.../export?format=ods
   Reason: Google Drive/Sheets access blocked
```

**Impact:**
- Cannot install required system packages (7z, libreoffice, pandoc)
- Cannot download build inputs (Google Sheets with UBL data model)

### Issue 2: Missing Dependencies

**Required but not available:**
- `p7zip-full` (7z command) - for creating compressed archives
- `libreoffice` (soffice) - for ODS→XLS conversion
- `aspell` - for spell checking
- `pandoc` - for document format conversion

**Available:**
- Java (v21, though build expects v8)
- Python 3.11
- wget binary (blocked by network)
- bash, basic Unix tools

---

## Security Considerations

### Why These Restrictions Exist

1. **Prevent Arbitrary Code Execution**
   - Package installation can introduce backdoors
   - Unverified packages could be malicious

2. **Prevent Data Exfiltration**
   - Unrestricted internet access enables data theft
   - Build processes could send data externally

3. **Resource Protection**
   - Limit network bandwidth usage
   - Prevent abuse of external services

4. **Reproducibility**
   - Controlled environment ensures consistent builds
   - No unknown external dependencies

### Legitimate Build Requirements

The UBL build **legitimately needs:**

1. **External data inputs** (Google Sheets with UBL specification)
2. **Compression tools** (7z for creating distribution archives)
3. **Document processors** (LibreOffice for ODS/XLS conversion)
4. **Format converters** (pandoc for documentation)

---

## Solution Options (Ranked by Security)

### Option 1: Pre-Built Container Image ⭐ MOST SECURE

**Approach:** Include all dependencies in base container image

**Implementation:**
```dockerfile
FROM ubuntu:22.04

# Install all required dependencies at image build time
RUN apt-get update && apt-get install -y \
    openjdk-8-jdk \
    python3 \
    p7zip-full \
    libreoffice \
    aspell \
    pandoc \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Pre-install Python packages
RUN pip3 install py7zr

# Optionally: pre-download Google Sheets as base data
COPY UBL-Library-Google.ods /opt/ubl-data/
COPY UBL-Documents-Google.ods /opt/ubl-data/
COPY UBL-Signature-Google.ods /opt/ubl-data/
```

**Advantages:**
- ✅ No runtime package installation needed
- ✅ No runtime network access needed
- ✅ Fully reproducible builds
- ✅ Fastest build times (dependencies cached)
- ✅ Most secure (all dependencies verified at image creation)

**Disadvantages:**
- ⚠️ Larger base image (~2-3 GB with LibreOffice)
- ⚠️ Requires updating image when dependencies change
- ⚠️ Google Sheets data becomes stale (needs periodic updates)

**Security Level:** ⭐⭐⭐⭐⭐ (Highest)

---

### Option 2: Whitelisted Network Access ⭐⭐⭐⭐ BALANCED

**Approach:** Allow specific URLs through network filter

**Implementation:**
```yaml
# Network whitelist configuration
allowed_hosts:
  # Package repositories
  - archive.ubuntu.com
  - security.ubuntu.com

  # Google Sheets (read-only)
  - docs.google.com
  - docs.googleusercontent.com

  # Optional: Realta API (for documentation)
  - www.realtaonline.com

allowed_operations:
  - GET  # Read-only
  # POST blocked (prevents data upload)
```

**Package Installation:**
```bash
# Allow apt-get from official Ubuntu repos only
apt-get update
apt-get install -y p7zip-full libreoffice pandoc aspell
```

**Google Sheets Download:**
```bash
# Allow wget from whitelisted domains
wget --no-check-certificate \
     https://docs.google.com/spreadsheets/d/.../export?format=ods
```

**Advantages:**
- ✅ Fresh data from Google Sheets
- ✅ Standard Ubuntu packages (verified)
- ✅ Build uses latest UBL specifications
- ✅ Moderate image size

**Disadvantages:**
- ⚠️ Network dependency (build fails if Google is down)
- ⚠️ Potential for data exfiltration if whitelist is too broad
- ⚠️ Requires network filtering infrastructure

**Security Level:** ⭐⭐⭐⭐ (High - with proper whitelist)

---

### Option 3: Cached External Resources ⭐⭐⭐⭐⭐ RECOMMENDED

**Approach:** Pre-download and cache all external resources

**Implementation:**

1. **Cache Google Sheets in Repository:**
   ```bash
   # Add to repository (updated periodically)
   ubl/
   ├── cached-data/
   │   ├── UBL-Library-Google.ods
   │   ├── UBL-Documents-Google.ods
   │   └── UBL-Signature-Google.ods
   ```

2. **Modify build scripts to use cached data:**
   ```bash
   # build.sh modification
   if [ -f "cached-data/UBL-Library-Google.ods" ]; then
       cp cached-data/UBL-Library-Google.ods ../
       export USE_CACHED_DATA=true
   fi
   ```

3. **Pre-install dependencies in container:**
   ```dockerfile
   RUN apt-get update && apt-get install -y \
       p7zip-full libreoffice pandoc aspell
   ```

**Advantages:**
- ✅ No runtime network access needed
- ✅ Fully reproducible builds (same inputs every time)
- ✅ Fast builds (no download time)
- ✅ Works offline
- ✅ Git tracks when data changes

**Disadvantages:**
- ⚠️ Repository size increases (~10-20 MB for ODS files)
- ⚠️ Manual process to update cached data
- ⚠️ Data can become stale

**Security Level:** ⭐⭐⭐⭐⭐ (Highest - no network needed)

**Maintenance:**
```bash
# Update cached data (manual process, monthly?)
cd cached-data/
wget -O UBL-Library-Google.ods "https://docs.google.com/.../export?format=ods"
git add *.ods
git commit -m "Update cached Google Sheets data"
```

---

### Option 4: Build Stages with Network Isolation ⭐⭐⭐ COMPLEX

**Approach:** Separate download phase from build phase

**Implementation:**

**Stage 1: Download (with network):**
```yaml
download-stage:
  network: enabled
  allowed_hosts: [docs.google.com]
  steps:
    - wget UBL-Library-Google.ods
    - wget UBL-Documents-Google.ods
    - wget UBL-Signature-Google.ods
    - save to artifact storage
```

**Stage 2: Build (isolated):**
```yaml
build-stage:
  network: disabled  # Completely isolated
  dependencies: [7z, libreoffice, pandoc]
  inputs:
    - artifacts from download-stage
  steps:
    - run build.sh with cached data
```

**Advantages:**
- ✅ Fresh data when needed
- ✅ Build phase is network-isolated (secure)
- ✅ Clear separation of concerns

**Disadvantages:**
- ⚠️ Complex infrastructure (two-stage pipeline)
- ⚠️ Download stage still needs network access
- ⚠️ More moving parts = more failure points

**Security Level:** ⭐⭐⭐ (Good - if download stage is properly isolated)

---

### Option 5: Mount External Volumes ⭐⭐ REQUIRES INFRASTRUCTURE

**Approach:** Mount pre-prepared volumes with dependencies and data

**Implementation:**
```yaml
volumes:
  - /opt/ubl-dependencies/  # 7z, libreoffice, etc.
  - /opt/ubl-data/          # Google Sheets ODS files
  - /opt/java8/             # Specific Java version

container:
  mounts:
    - /opt/ubl-dependencies:/usr/local/bin
    - /opt/ubl-data:/workspace/data
```

**Advantages:**
- ✅ No network needed
- ✅ Dependencies managed externally
- ✅ Can update dependencies without rebuilding container

**Disadvantages:**
- ⚠️ Requires volume management infrastructure
- ⚠️ Complexity in maintaining mounted volumes
- ⚠️ Potential security issues with shared volumes

**Security Level:** ⭐⭐ (Depends on volume security)

---

## Recommended Solution: Option 3 (Cached Resources)

### Why This Is Best

1. **Security:** No network access needed at all ⭐⭐⭐⭐⭐
2. **Reproducibility:** Same inputs = same outputs always
3. **Performance:** No download time, fastest builds
4. **Simplicity:** Just add files to repository
5. **Transparency:** Git tracks all data changes

### Implementation Plan

#### Step 1: Create Cached Data Directory

```bash
mkdir -p ubl/cached-data/
```

#### Step 2: Download Google Sheets (one-time, or monthly update)

```bash
cd cached-data/

# Download current UBL 2.5 specifications
wget -O UBL-Library-Google.ods \
  "https://docs.google.com/spreadsheets/d/18o1YqjHWUw0-s8mb3ja4i99obOUhs-4zpgso6RZrGaY/export?format=ods"

wget -O UBL-Documents-Google.ods \
  "https://docs.google.com/spreadsheets/d/1024Th-Uj8cqliNEJc-3pDOR7DxAAW7gCG4e-pbtarsg/export?format=ods"

wget -O UBL-Signature-Google.ods \
  "https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g/export?format=ods"

# Add to repository
git add *.ods
git commit -m "Add cached Google Sheets for offline builds"
```

#### Step 3: Modify build.xml to Use Cached Data

```xml
<!-- In build.xml, add check for cached data -->
<available property="google-sig-file-exists-cached"
           file="cached-data/UBL-Signature-Google.ods"/>

<sequential if:set="google-sig-file-exists-cached">
  <echo message="Using cached signature Google spreadsheet"/>
  <copy file="cached-data/UBL-Signature-Google.ods"
        tofile="${dir}/UBL-Signature-Google.ods"/>
</sequential>

<!-- Similar for Library and Documents -->
```

#### Step 4: Update Container Image with Dependencies

```dockerfile
FROM ubuntu:22.04

# Install all required dependencies
RUN apt-get update && \
    apt-get install -y \
        openjdk-8-jdk \
        python3 \
        python3-pip \
        p7zip-full \
        libreoffice-calc \
        aspell \
        pandoc \
        wget \
        git \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install py7zr

# Set Java 8 as default
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
```

#### Step 5: Build Process (No Network Needed)

```bash
# Clone repository (includes cached-data/)
git clone https://github.com/kduvekot/ubl.git
cd ubl

# Run build (uses cached data automatically)
bash build.sh target local test-build

# Success! No network access needed.
```

---

## Alternative: Quick Win with skip-gc.txt

**For immediate testing without code changes:**

```bash
# Use existing .gc files from repo (v2.4)
touch skip-gc.txt

# Build will skip Google Sheets download
bash build.sh target local test-build

# This works NOW but uses old data (UBL 2.4 instead of 2.5)
```

**When to use:**
- Quick testing of build process
- Validating build scripts work
- Testing changes that don't affect data model

**Limitations:**
- Uses UBL 2.4 data (not 2.5)
- Not suitable for production builds

---

## Comparison Matrix

| Solution | Security | Performance | Maintenance | Network Needed | Recommended |
|----------|----------|-------------|-------------|----------------|-------------|
| **Pre-built image** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | No | ✅ Good |
| **Whitelisted network** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Yes | ⚠️ Moderate |
| **Cached resources** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | No | ⭐ **BEST** |
| **Build stages** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Yes (stage 1) | ⚠️ Complex |
| **Volume mounts** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | No | ❌ Complex |
| **skip-gc.txt** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | No | ⚠️ Old data |

---

## Implementation Priorities

### Immediate (Can Do Now)

1. **Use skip-gc.txt** for testing
   - Zero code changes
   - Works with existing .gc files
   - Validates build infrastructure

### Short Term (Days)

1. **Add cached-data/ directory** to repository
2. **Download current Google Sheets** to cached-data/
3. **Modify build.xml** to check for cached data first
4. **Update documentation** with offline build instructions

### Medium Term (Weeks)

1. **Create optimized container image** with all dependencies
2. **Test reproducible builds** with cached data
3. **Set up monthly process** to update cached Google Sheets
4. **Add validation** to ensure cached data is current

### Long Term (Months)

1. **Implement network whitelist** (if needed for fresh data)
2. **Add CI/CD checks** for cached data freshness
3. **Automate cache updates** with scheduled jobs
4. **Document security model** for auditing

---

## Security Audit Checklist

Before enabling builds in restricted environment:

- [ ] All dependencies from trusted sources (Ubuntu official repos)
- [ ] Cached data verified with checksums
- [ ] Network access minimal or zero
- [ ] No arbitrary code execution paths
- [ ] Build process fully reproducible
- [ ] Output artifacts verifiable
- [ ] No data exfiltration paths
- [ ] Container image regularly updated (security patches)
- [ ] Logs captured and auditable
- [ ] Resource limits enforced (CPU, memory, disk)

---

## Conclusion

**Recommended Approach:** Option 3 (Cached Resources)

**Implementation:**
1. Add `cached-data/` directory with Google Sheets
2. Modify `build.xml` to use cached data
3. Update container image with dependencies
4. No network access needed during build

**Benefits:**
- ⭐ Highest security (no network)
- ⭐ Best performance (no downloads)
- ⭐ Fully reproducible
- ⭐ Simple to implement
- ⭐ Works offline

**Trade-off:**
- Manual process to update cached data (monthly/quarterly)
- Repository size increases by ~10-20 MB

**This enables secure builds in Claude Code or any restricted environment!**

---

**Last Updated:** 2025-10-24
**Status:** Analysis complete, ready for implementation
**Next Steps:** Add cached-data/ directory and modify build.xml
