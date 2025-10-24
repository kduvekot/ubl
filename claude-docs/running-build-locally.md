# Running UBL Build Locally (GitHub Actions Equivalent)

**Date:** 2025-10-24
**Workflow File:** `.github/workflows/build.yml`

This guide explains how to run the same build process that GitHub Actions executes, but on your local machine.

---

## Overview

The GitHub Actions workflow has two build jobs:
1. **`build`** - Shell script-based build (runs on all branches)
2. **`build-py`** - Python-based build (only runs on `ubl-2.5-python` branch)

Both produce identical outputs but use different entry points.

---

## Prerequisites

### Required Software

1. **Java JDK 8** (Zulu or OpenJDK)
   ```bash
   # Check if installed
   java -version

   # Should show version 1.8.x
   ```

2. **System Dependencies**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install -y aspell libreoffice pandoc p7zip-full

   # macOS (with Homebrew)
   brew install aspell libreoffice pandoc p7zip
   ```

3. **For Python build only:**
   ```bash
   # Python 3.12+ (or 3.8+)
   python3 --version

   # Install py7zr (only for Python build)
   pip install py7zr
   ```

### Optional (for full documentation)

- **Realta API credentials** (stored in GitHub Secrets)
  - Username: `REALTA_USERNAME`
  - Password: `REALTA_PASSWORD`
  - Without these, documentation generation will be skipped (which is fine for testing)

---

## Option 1: Manual Local Build (Recommended for Testing)

This mimics what GitHub Actions does but without the cleanup that deletes repository files.

### Shell Script Build

```bash
# 1. Ensure you're in the repository root
cd /path/to/ubl

# 2. Create target directory
mkdir -p target

# 3. Generate timestamp (like GitHub Actions)
TIMESTAMP=$(date -u +%Y%m%d-%H%M)z

# 4. Run the build (WITHOUT cleanup)
bash build.sh target local "${TIMESTAMP}"

# Optional: with Realta credentials for full docs
# bash build.sh target local "${TIMESTAMP}" "YOUR_USERNAME" "YOUR_PASSWORD"
```

**Expected outputs in `target/`:**
```
target/
├── UBL-2.5-csd01-{timestamp}/              # Main package
├── UBL-2.5-csd01-{timestamp}-archive-only/ # Build logs
├── UBL-2.5-csd01-{timestamp}-iso-iec-19845/ # ISO format
├── UBL-2.5-csd01-{timestamp}.7z             # Compressed main
├── UBL-2.5-csd01-{timestamp}-archive-only.7z
└── UBL-2.5-csd01-{timestamp}-iso-iec-19845.7z
```

### Python Build

```bash
# 1. Ensure you're in the repository root
cd /path/to/ubl

# 2. Create target directory
mkdir -p target

# 3. Generate timestamp
TIMESTAMP=$(date -u +%Y%m%d-%H%M)z

# 4. Run Python build (WITHOUT cleanup)
python3 build.py target local "${TIMESTAMP}"

# Optional: with Realta credentials
# python3 build.py target local "${TIMESTAMP}" "YOUR_USERNAME" "YOUR_PASSWORD"
```

---

## Option 2: Exact GitHub Actions Simulation

This runs the **exact same command** as GitHub Actions, including the aggressive cleanup.

⚠️ **WARNING:** This will delete almost all repository files except `target/` and `.github/`!

```bash
# 1. Clone a fresh copy (DO NOT run in your main repository!)
git clone https://github.com/kduvekot/ubl.git ubl-test
cd ubl-test
git checkout ubl-2.5-python

# 2. Generate timestamp
TIMESTAMP=$(date -u +%Y%m%d-%H%M)z

# 3. Create target directory
mkdir target

# 4. Run EXACT GitHub Actions command
bash build.sh target github "${TIMESTAMP}z" "" "" DELETE-REPOSITORY-FILES-AS-WELL

# Or Python version:
# python3 build.py target github "${TIMESTAMP}z" "" "" DELETE-REPOSITORY-FILES-AS-WELL
```

**What happens:**
1. Build runs normally
2. Creates 3x .7z archives in `target/`
3. **DELETES ALL REPOSITORY FILES** except `target/` and `.github/`
4. Moves .7z files to root
5. Deletes `target/` directory

**After completion, only these files remain:**
```
.github/         # GitHub Actions configuration (preserved)
*.7z            # Three compressed archives (moved to root)
```

---

## Option 3: Using `act` (GitHub Actions Locally)

[`act`](https://github.com/nektos/act) runs GitHub Actions workflows locally in Docker.

### Install act

```bash
# macOS
brew install act

# Linux (via binary)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Windows
choco install act-cli
```

### Run the workflow

```bash
# Run the shell build job
act -j build

# Run the Python build job (on ubl-2.5-python branch)
act -j build-py

# Run with secrets (for Realta API)
act -j build --secret REALTA_USERNAME=your_username --secret REALTA_PASSWORD=your_password
```

**Note:** `act` runs in Docker, so outputs will be inside the container. You'll need to configure artifact mounting.

---

## Understanding Build Parameters

The build scripts accept these parameters:

```bash
# Shell version
bash build.sh <target_dir> <platform> <label> [realta_user] [realta_pass] [delete_option]

# Python version
python3 build.py <target_dir> <platform> <label> [realta_user] [realta_pass] [delete_option]
```

### Parameters Explained

| Parameter | GitHub Actions Value | Local Recommended | Description |
|-----------|---------------------|-------------------|-------------|
| `target_dir` | `target` | `target` | Output directory |
| `platform` | `github` | `local` | Platform identifier (affects CPU usage) |
| `label` | `{timestamp}z` | Any string | Build label/version |
| `realta_user` | `$REALTA_USERNAME` | `""` (empty) | Realta API username (optional) |
| `realta_pass` | `$REALTA_PASSWORD` | `""` (empty) | Realta API password (optional) |
| `delete_option` | `DELETE-REPOSITORY-FILES-AS-WELL` | (omit) | Triggers cleanup |

### Platform Differences

- **`platform=github`**: Uses 1 CPU core (GitHub Actions default)
- **`platform=local`**: Uses 16 CPU cores (faster on local machines)

This affects ANT's `cpuCount` property in build.xml (line 47).

---

## Verifying Build Success

### Check for Error Files

After build completes, check the archive-only directory for error indicators:

```bash
# Find the archive-only directory
cd target/UBL-2.5-csd01-*-archive-only/

# Check for error/warning files
ls -la *.txt *.html 2>/dev/null

# Should only see:
# - build.console.{label}.txt  (build log - always present)
# - build.exitcode.{label}.txt (exit code - should be 0)

# Any OTHER .txt or .html files indicate warnings/errors!
```

### Common Warning Files

If these appear, there were issues:
- `NDR-CHECK-WARNING.txt` - NDR compliance issues
- `INVALID-*.txt` - Invalid generated files
- `INTEGRITY-PROBLEMS.txt` - Missing/extra files
- `UNEXPECTED-*.txt` - Unexpected validation results

### Check Exit Code

```bash
cat target/UBL-2.5-csd01-*-archive-only/build.exitcode.*.txt
# Should show: 0
```

### Inspect Build Log

```bash
# View last 50 lines of build log
tail -50 target/UBL-2.5-csd01-*-archive-only/build.console.*.txt

# Search for errors
grep -i error target/UBL-2.5-csd01-*-archive-only/build.console.*.txt
```

---

## Quick Build Testing (Minimal)

For testing changes without full build:

```bash
# Create skip files to bypass slow operations
touch skip-gc.txt          # Skip genericode generation (use existing)
touch skip-ss.txt          # Skip spreadsheet generation
touch skip-html.txt        # Skip detailed HTML reports
touch skip-samples.txt     # Skip sample validation

# Run fast build
TIMESTAMP=$(date -u +%Y%m%d-%H%M)z
bash build.sh target local "${TIMESTAMP}"

# Clean up skip files when done
rm skip-*.txt
```

---

## Extracting Outputs

### View Archive Contents (without extracting)

```bash
# List contents of main package
7z l target/UBL-2.5-csd01-*.7z | less

# List ISO package
7z l target/UBL-2.5-csd01-*-iso-iec-19845.7z | less

# List archive-only package
7z l target/UBL-2.5-csd01-*-archive-only.7z | less
```

### Extract Archives

```bash
cd target

# Extract main package
7z x UBL-2.5-csd01-*.7z

# Now you can browse:
ls -la UBL-2.5-csd01-*/
```

---

## Troubleshooting

### Java Version Issues

**Error:** `Unsupported class file major version`
**Solution:** Ensure Java 8 is being used

```bash
# Check Java version
java -version

# If multiple Java versions installed, set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

### Missing Dependencies

**Error:** `wget: command not found` or `7z: command not found`
**Solution:** Install missing tools

```bash
# Ubuntu/Debian
sudo apt install -y wget p7zip-full

# macOS
brew install wget p7zip
```

### LibreOffice Issues

**Error:** `soffice: command not found`
**Solution:** Install LibreOffice or skip spreadsheet generation

```bash
# Install LibreOffice
sudo apt install -y libreoffice

# OR skip with flag
touch skip-ss.txt
```

### Memory Issues

**Error:** `java.lang.OutOfMemoryError`
**Solution:** Increase Java heap size

Edit `build-common.sh` or `build.py` to add Java memory flags:
```bash
# In build-common.sh line 14, add -Xmx4g
java -Xmx4g -Dant.home=utilities/ant ...
```

### Google Sheets Download Fails

**Error:** `wget` fails to download spreadsheets
**Solution:** Use cached versions

1. Download the archive-only package from a previous build
2. Extract the .ods files: `UBL-*-Google.ods`
3. Place them in parent directory: `../UBL-*-Google.ods`
4. Build script will detect and use them

---

## Comparing with GitHub Actions Output

To verify your local build matches GitHub Actions:

```bash
# 1. Download artifacts from GitHub Actions
#    Go to: https://github.com/kduvekot/ubl/actions
#    Download the artifact ZIP

# 2. Extract GitHub Actions output
unzip UBL-package-github-*.zip -d github-build/

# 3. Run local build
TIMESTAMP=$(date -u +%Y%m%d-%H%M)z
bash build.sh target local "${TIMESTAMP}"

# 4. Compare checksums
cd target
sha256sum *.7z > ../local-checksums.txt
cd ../github-build
sha256sum *.7z > ../github-checksums.txt

# Note: Checksums will differ due to timestamps and paths in archives
# But file sizes should be very similar
```

---

## GitHub Actions Workflow Details

### What GitHub Actions Does

**Job: `build` (Shell Script)**
1. Checkout repository
2. Install Java 8 (Zulu distribution)
3. Install dependencies: `aspell`, `libreoffice`, `pandoc`
4. Run: `bash build.sh target github {timestamp}z {secrets} DELETE-REPOSITORY-FILES-AS-WELL`
5. Upload artifacts (the 3x .7z files)

**Job: `build-py` (Python Script - only on ubl-2.5-python branch)**
1. Checkout repository
2. Install Java 8 (Zulu distribution)
3. Install Python 3.12
4. Install dependencies: `aspell`, `libreoffice`, `pandoc`, `py7zr`
5. Run: `python build.py target github {timestamp}z {secrets} DELETE-REPOSITORY-FILES-AS-WELL`
6. Upload artifacts (the 3x .7z files)

### Timing

GitHub Actions build takes approximately **25-30 minutes** with these phases:
- Setup (Java, dependencies): ~2 minutes
- ANT build process: ~20 minutes
- Archive creation (7z): ~3-5 minutes
- Upload artifacts: ~2 minutes

Local builds may be faster with `platform=local` (uses 16 CPU cores vs 1).

---

## Best Practices

### For Development/Testing

```bash
# Use local platform for speed
bash build.sh target local test-build-001

# Keep repository files intact (no DELETE option)
# Output goes to target/ directory
```

### For Release Candidates

```bash
# Use github platform for consistency
bash build.sh target github rc-$(date +%Y%m%d)

# Review outputs thoroughly before publishing
```

### For CI/CD Validation

```bash
# Use act to run exact workflow
act -j build

# Or clone fresh repo and test with cleanup
git clone ... temp-ubl-test
cd temp-ubl-test
bash build.sh target github test "" "" DELETE-REPOSITORY-FILES-AS-WELL
```

---

## Summary

**Quickest Way to Test Locally:**
```bash
mkdir target
bash build.sh target local $(date -u +%Y%m%d-%H%M)z
```

**Most Accurate (matches GitHub Actions):**
```bash
act -j build
```

**Safest (no repository deletion):**
```bash
mkdir target
bash build.sh target local my-test-build
# Outputs to target/, repository intact
```

---

**Last Updated:** 2025-10-24
**Workflow File:** `.github/workflows/build.yml`
**Related Docs:**
- `build-analysis.md` - Complete build system analysis
- `build-py-vs-shell-comparison.md` - Python vs Shell equivalence validation
