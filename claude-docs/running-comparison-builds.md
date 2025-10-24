# Running Shell and Python Builds for Comparison

**Date:** 2025-10-24
**Purpose:** Execute both build.sh and build.py sequentially with matching timestamps for output comparison

---

## Why This Failed in Claude Code Environment

The UBL build cannot run in this restricted environment due to:

### ❌ Missing Network Access
- **Google Sheets Download:** Build tries to download 3 ODS files from Google
  ```
  wget: 403 Forbidden
  https://docs.google.com/spreadsheets/d/.../export?format=ods
  ```
- **Package Installation:** Cannot install required `p7zip-full` package
  ```
  apt-get: 403 Forbidden (ppa.launchpadcontent.net)
  ```

### ❌ Missing Dependencies
- **7z:** Required for creating compressed archives (not installed)
- **LibreOffice:** Required for ODS→XLS conversion (may not be installed)
- **aspell:** Required for spell checking (may not be installed)

### ✅ What IS Available
- Java 21.0.8 (build requires Java 8, but may work)
- Python 3.11.14
- wget (but blocked by network restrictions)
- All repository files and build scripts

---

## How to Run Both Builds Properly (Your Environment)

### Step 1: Generate Shared Timestamp

**CRITICAL:** Use the SAME timestamp for both builds so output filenames match!

```bash
# Generate timestamp once
export BUILD_TIMESTAMP=$(date -u +%Y%m%d-%H%M)
echo "Using timestamp: ${BUILD_TIMESTAMP}"

# This will be used for both builds
```

### Step 2: Create Separate Target Directories

```bash
# Create directories that won't trigger cleanup
mkdir -p target-shell target-python

# Verify
ls -ld target-*
```

### Step 3: Run Shell Build

```bash
echo "=== Starting Shell Build ==="
echo "Timestamp: ${BUILD_TIMESTAMP}"
echo "Start time: $(date)"

# Run shell build
bash build.sh target-shell local "${BUILD_TIMESTAMP}"

echo "Shell build completed at: $(date)"
echo ""
```

**Expected Duration:** 20-30 minutes

**Output Location:** `target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}/`

### Step 4: Run Python Build (Same Timestamp!)

```bash
echo "=== Starting Python Build ==="
echo "Timestamp: ${BUILD_TIMESTAMP}"  # Same timestamp!
echo "Start time: $(date)"

# Run Python build with SAME timestamp
python3 build.py target-python local "${BUILD_TIMESTAMP}"

echo "Python build completed at: $(date)"
echo ""
```

**Expected Duration:** 20-30 minutes

**Output Location:** `target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}/`

---

## Complete Script (Copy-Paste Ready)

```bash
#!/bin/bash
# Run both builds with matching timestamps for comparison

set -e  # Exit on error

# Step 1: Generate shared timestamp
export BUILD_TIMESTAMP=$(date -u +%Y%m%d-%H%M)
echo "=========================================="
echo "UBL Build Comparison Test"
echo "Timestamp: ${BUILD_TIMESTAMP}"
echo "Start time: $(date)"
echo "=========================================="
echo ""

# Step 2: Create target directories
mkdir -p target-shell target-python

# Step 3: Run shell build
echo "=== SHELL BUILD ==="
echo "Command: bash build.sh target-shell local ${BUILD_TIMESTAMP}"
echo "Output: target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}/"
echo ""
time bash build.sh target-shell local "${BUILD_TIMESTAMP}"
SHELL_EXIT=$?
echo ""
echo "Shell build exit code: ${SHELL_EXIT}"
echo "Shell build completed at: $(date)"
echo ""

# Step 4: Run Python build
echo "=== PYTHON BUILD ==="
echo "Command: python3 build.py target-python local ${BUILD_TIMESTAMP}"
echo "Output: target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}/"
echo ""
time python3 build.py target-python local "${BUILD_TIMESTAMP}"
PYTHON_EXIT=$?
echo ""
echo "Python build exit code: ${PYTHON_EXIT}"
echo "Python build completed at: $(date)"
echo ""

# Step 5: Summary
echo "=========================================="
echo "BUILD SUMMARY"
echo "=========================================="
echo "Timestamp used: ${BUILD_TIMESTAMP}"
echo "Shell build: Exit code ${SHELL_EXIT}"
echo "Python build: Exit code ${PYTHON_EXIT}"
echo ""
echo "Output directories:"
ls -lh target-shell/ target-python/
echo ""
echo "Archive files created:"
echo "Shell:"
ls -lh target-shell/*.7z 2>/dev/null || echo "  No archives (check for errors)"
echo "Python:"
ls -lh target-python/*.7z 2>/dev/null || echo "  No archives (check for errors)"
echo ""
echo "Comparison ready!"
```

---

## Verifying Outputs Match

### Step 1: Check Directory Structure

```bash
echo "=== Directory Structure Comparison ==="
echo ""
echo "Shell build structure:"
find target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP} -type d | sort | head -20
echo ""
echo "Python build structure:"
find target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP} -type d | sort | head -20
```

### Step 2: Check File Counts

```bash
echo "=== File Count Comparison ==="
echo ""
echo "Shell build files:"
find target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP} -type f | wc -l
echo ""
echo "Python build files:"
find target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP} -type f | wc -l
```

### Step 3: Check Archive Sizes

```bash
echo "=== Archive Size Comparison ==="
echo ""
echo "Shell archives:"
ls -lh target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}*.7z
echo ""
echo "Python archives:"
ls -lh target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}*.7z
```

### Step 4: Check for Error Files

```bash
echo "=== Error/Warning File Check ==="
echo ""
echo "Shell build warnings:"
find target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only -name "*.txt" -o -name "*.html" | grep -v "build.console\|build.exitcode"
echo ""
echo "Python build warnings:"
find target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only -name "*.txt" -o -name "*.html" | grep -v "build.console\|build.exitcode"
```

### Step 5: Compare Exit Codes

```bash
echo "=== Exit Code Comparison ==="
echo ""
echo "Shell build exit code:"
cat target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only/build.exitcode.${BUILD_TIMESTAMP}.txt
echo ""
echo "Python build exit code:"
cat target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only/build.exitcode.${BUILD_TIMESTAMP}.txt
```

---

## Expected Results

### If Builds Are Equivalent

**File counts should match:**
```
Shell:  ~1200-1500 files
Python: ~1200-1500 files
```

**Archive sizes should be similar (within 1%):**
```
Main package:     ~150-200 MB
Archive-only:     ~10-20 MB
ISO:              ~5-10 MB
```

**Exit codes should both be 0:**
```
Shell:  0
Python: 0
```

**No error/warning files in archive-only (except console/exitcode)**

### If There Are Differences

Check build logs for differences:
```bash
# Compare console logs
diff target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only/build.console.*.txt \
     target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}-archive-only/build.console.*.txt
```

---

## What the Same Timestamp Ensures

Using the **same timestamp** for both builds ensures:

1. **Matching output directory names:**
   - Shell: `target-shell/UBL-2.5-csd01-20251024-1512/`
   - Python: `target-python/UBL-2.5-csd01-20251024-1512/`

2. **Matching archive names:**
   - Shell: `UBL-2.5-csd01-20251024-1512.7z`
   - Python: `UBL-2.5-csd01-20251024-1512.7z`

3. **Matching log file names:**
   - Shell: `build.console.20251024-1512.txt`
   - Python: `build.console.20251024-1512.txt`

4. **Easy comparison:**
   - Can compare directories side-by-side
   - Can diff files directly by name
   - Can verify archive contents match

---

## Troubleshooting

### Different File Counts

**Possible causes:**
- Build errors in one but not the other
- Generated files have different timestamps embedded
- One build skipped optional steps

**Solution:** Check build logs and compare specific directories

### Different Archive Sizes

**Possible causes:**
- Timestamps embedded in files (different compression)
- Different file modification times
- Actual content differences

**Solution:** Extract and compare file contents, not just sizes

### One Build Fails

**Common issues:**
- Missing dependencies (check error messages)
- Insufficient memory (increase Java heap with -Xmx)
- Google Sheets download failure (use local copies)

---

## Prerequisites Checklist

Before running comparison:

- [ ] Java 8+ installed (`java -version`)
- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] 7z installed (`7z` or `sudo apt install p7zip-full`)
- [ ] wget installed (`wget --version`)
- [ ] LibreOffice installed (optional, for ODS→XLS conversion)
- [ ] aspell installed (optional, for spell checking)
- [ ] ~500MB free disk space per build
- [ ] Internet access (for Google Sheets download)
- [ ] 40-60 minutes total time available

---

## Quick Reference

**Generate timestamp:**
```bash
export BUILD_TIMESTAMP=$(date -u +%Y%m%d-%H%M)
```

**Shell build:**
```bash
bash build.sh target-shell local "${BUILD_TIMESTAMP}"
```

**Python build:**
```bash
python3 build.py target-python local "${BUILD_TIMESTAMP}"
```

**Compare outputs:**
```bash
diff -r target-shell/UBL-2.5-csd01-${BUILD_TIMESTAMP} \
        target-python/UBL-2.5-csd01-${BUILD_TIMESTAMP}
```

---

## Why This Matters

Using the **same timestamp** ensures:
- ✅ Fair comparison (same inputs, same time reference)
- ✅ Matching file names for easy comparison
- ✅ Reproducible results
- ✅ Clear identification of any differences

Without the same timestamp, you'd have:
- ❌ Different directory names making comparison harder
- ❌ Different archive names
- ❌ Potential timestamp differences in generated files
- ❌ Confusing results

---

**Last Updated:** 2025-10-24
**Status:** Cannot run in Claude Code environment (network restrictions)
**Recommended:** Run in your local development environment with network access
