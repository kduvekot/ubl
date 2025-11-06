# Build UBL Package Locally

Build the UBL package in your local environment with comprehensive validation and error checking.

## Instructions

Follow these steps to build and validate the UBL package:

### 1. Verify Current State
- Check which branch you're on: `git branch --show-current`
- Confirm you're on the intended development branch (e.g., ubl-2.5-python)
- Review build configuration in `build.py` for version/stage settings

### 2. Check Build Configuration
Read the following configuration values from `build.py`:
- `title` (e.g., "UBL 2.5")
- `package` (e.g., "UBL-2.5")
- `ubl_version` (e.g., "2.5")
- `ubl_stage` (e.g., "csd01")
- Google spreadsheet URLs (libGoogle, docGoogle, sigGoogle)

Display these values to the user for confirmation.

### 3. Prepare Build Environment
- Create target directory if it doesn't exist: `mkdir -p target`
- Check for leftover build artifacts: `ls target/`
- If old artifacts exist, ask user if they should be cleaned up

### 4. Run the Build
Execute the Python build script:
```bash
python build.py target local debug
```

Monitor the build process and display progress indicators.

### 5. Check Build Results
Once build completes, examine the target directory structure.

Look for the build output directory: `target/UBL-{version}-{stage}-debug/`

#### Check for Error Files
The following files indicate problems (they should NOT exist):

- **ATTENTION-new-entities.txt**: Entity files have changed
  - Action: Copy new entities from `archive-only/new-entities/` to repository root

- **HUB-SKIPPED-INCOMPLETE-ARTEFACTS.txt**: Build incomplete
  - Action: Review build console log for errors

- **INTEGRITY-PROBLEMS.txt**: File reference mismatches
  - Action: Read file to see which files are missing or unreferenced

- **INVALID-ASSEMBLED-HUB-XML.txt**: Hub document validation failed
  - Action: Read file for validation errors in UBL.xml

- **LIST-OF-PROBLEM-CODE-LISTS.txt**: Invalid genericode files
  - Action: Check code list files in raw/cl/ directory

- **MISMATCHED-TEST-SAMPLES-SH-WARNING.txt**: Sample count mismatch
  - Action: Review raw/val/testsamples.sh script

- **MISMATCHED-TEST-SAMPLES-BAT-WARNING.txt**: Sample count mismatch (Windows)
  - Action: Review raw/val/testsamples.bat script

- **NDR-SPELL-CHECK-WARNING.txt**: Spelling issues found
  - Action: Check unexpectedWords.txt for details

- **UNEXPECTED-SAMPLES-NS-PI-DETAILS.txt**: Namespace issues in samples
  - Action: Read file for affected sample files

- **UNEXPECTED-TEST-RESULT-WARNING.txt**: Validation test failed
  - Action: Review raw/val/test.sh output

#### Check Build Exit Code
Read `target/UBL-{version}-{stage}-debug-archive-only/build.exitcode.debug.txt`
- Exit code 0 = success
- Non-zero = build failed

#### Check Console Log
Display relevant sections from `build.console.debug.txt` if errors occurred.

### 6. Verify Archives Created
Check for the three .7z archive files in target directory:
- `UBL-{version}-{stage}-debug.7z` (main distribution)
- `UBL-{version}-{stage}-debug-archive-only.7z` (archive files)
- `UBL-{version}-{stage}-debug-iso-iec-19845.7z` (ISO outputs)

### 7. Report Results
Provide a summary to the user:

**If successful:**
✓ Build completed successfully
✓ Exit code: 0
✓ All three archives created
✓ No warning files detected
✓ Ready to commit and push

**If errors found:**
✗ Build had issues (exit code: X)
✗ Warning files found: [list them]
✗ Errors detected: [summarize from console log]
✗ Action required: [specific steps to fix]

### 8. Optional: Run Validation Tests
Ask user if they want to run additional validation:
```bash
cd raw/val
./test.sh
./testsamples.sh
```

Report validation results.

## Expected Output
- Build takes approximately 10-30 minutes depending on system
- Console output shows XSLT transformations, file generation, validation
- Final output: ~550MB of artifacts compressed to ~160MB in .7z files

## Troubleshooting
If build fails:
1. Check Java version: `java -version` (should be 1.8)
2. Check Python version: `python --version` (should be 3.12+)
3. Verify Saxon JAR: `jar tf utilities/saxon9he/saxon9he.jar | grep Transform.class`
4. Check dependencies: aspell, libreoffice, pandoc installed
5. Review build.console.debug.txt for detailed error messages

## Notes
- This builds locally without Réalta publishing service (limited output)
- To include Réalta publishing, provide credentials as additional arguments
- Archives are suitable for local testing, not official publication
- Official builds should be done via GitHub Actions
