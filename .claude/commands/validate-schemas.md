# Validate UBL Schemas and Samples

Run comprehensive validation of UBL schemas, sample instances, and code lists.

## Instructions

### Step 1: Navigate to Validation Directory

Change to the validation directory:
```bash
cd raw/val
```

### Step 2: Check for Required Files

Verify these key validation files exist:
- `test.sh` - Main validation test script
- `testsamples.sh` - Sample instance validation script
- `test.bat` - Windows version (optional)
- `testsamples.bat` - Windows samples script (optional)

List the directory contents to show the user what's available.

### Step 3: Run Main Validation Test

Execute the main validation script:
```bash
./test.sh
```

**Expected behavior:**
- Tests the validation environment setup
- Validates schema structure
- Runs integrity checks
- Reports pass/fail for each test

**Monitor output for:**
- ✓ Successful validations
- ✗ Failed validations
- Warnings or errors
- File paths of problem files

Display a summary of results to the user.

### Step 4: Run Sample Instance Validation

Execute the sample validation script:
```bash
./testsamples.sh
```

**Expected behavior:**
- Validates all XML sample instances in `raw/xml/`
- Checks against UBL XSD schemas
- Verifies namespace declarations
- Reports validation status for each sample

**Look for:**
- Total number of samples tested
- Number of successful validations
- Any validation errors with file names and line numbers
- Schema location issues
- Namespace problems

### Step 5: Check JSON Sample Validation

If JSON validation is available, run:
```bash
python jsonvalidate.py
```

**Expected behavior:**
- Validates JSON samples in `raw/json/`
- Checks against JSON Schema definitions
- Reports validation status

### Step 6: Verify Code List Integrity

Code lists are validated during the main build process. Check if build has been run recently.

Look for genericode files in `raw/cl/gc/`:
```bash
ls -lh ../cl/gc/*.gc
```

If build hasn't been run, suggest running `/build-local` first to generate and validate code lists.

### Step 7: Check for Known Issues

Look for validation warning files in the build output (if available):

```bash
cd ../..
find target -name "*WARNING*.txt" -o -name "*PROBLEMS*.txt" 2>/dev/null
```

If files are found, read and report their contents:
- `LIST-OF-PROBLEM-CODE-LISTS.txt` - Invalid genericode files
- `UNEXPECTED-SAMPLES-NS-PI-DETAILS.txt` - Namespace issues
- `UNEXPECTED-TEST-RESULT-WARNING.txt` - Test failures
- `MISMATCHED-TEST-SAMPLES-*-WARNING.txt` - Sample count mismatches

### Step 8: Analyze Results

Provide a comprehensive report:

#### ✅ If All Tests Pass:
```
Validation Results: SUCCESS ✓

✓ Main validation tests passed
✓ All sample instances valid ({N} samples tested)
✓ JSON samples valid (if applicable)
✓ No warning files detected

Your schemas and samples are valid and ready for use.
```

#### ⚠️ If Issues Found:
```
Validation Results: ISSUES DETECTED ⚠

Issues found:
1. [Specific error description]
   File: [path]
   Line: [number]
   Problem: [details]

2. [Next error...]

Recommended actions:
- [Specific fix for issue 1]
- [Specific fix for issue 2]
```

### Step 9: Check Sample Count Consistency

Verify the number of sample files matches the test script expectations:

```bash
# Count XML samples
find ../xml -name "*.xml" -type f | wc -l

# Count test invocations in testsamples.sh
grep -c "validate" testsamples.sh
```

Report any mismatches to the user.

### Step 10: Validate Namespace Declarations

Check that all sample files use correct namespace declarations:

```bash
# Look for namespace processing instructions
grep -r "xml-stylesheet" ../xml/ || echo "No stylesheet PIs found"
```

Report unexpected namespace declarations or processing instructions.

## Common Validation Errors

### Error: "Cannot find schema"
**Cause:** Schema files not generated or in wrong location
**Fix:** Run build process first to generate schemas

### Error: "Invalid namespace"
**Cause:** Sample uses wrong or outdated namespace URI
**Fix:** Update namespace in sample file to match current UBL version

### Error: "Element not allowed"
**Cause:** Sample structure doesn't match schema definition
**Fix:** Review schema and correct sample structure

### Error: "Missing required element"
**Cause:** Sample is incomplete
**Fix:** Add required elements per schema definition

### Error: "Type mismatch"
**Cause:** Value doesn't match expected type (e.g., date format, number)
**Fix:** Correct value format in sample

## Validation Environment Requirements

### Required Software:
- **XMLStarlet** or **xmllint** - XML validation
- **Java** - For JAXP validation
- **Saxon** - For XSLT-based validation
- **Python 3** - For JSON schema validation

### Check Installation:
```bash
# Check for XML validators
which xmllint && xmllint --version
which xmlstarlet && xmlstarlet --version

# Check Java
java -version

# Check Python
python --version
```

If tools are missing, notify the user which validators are unavailable.

## Advanced Validation Options

### Validate Specific Sample:
```bash
# Navigate to validation directory
cd raw/val

# Validate single file
xmllint --noout --schema path/to/schema.xsd path/to/sample.xml
```

### Validate with Saxon:
```bash
java -cp ../../utilities/saxon9he/saxon9he.jar \
  net.sf.saxon.Transform \
  -xsl:validation.xsl \
  -s:sample.xml
```

### Generate Validation Report:
```bash
./test.sh > validation-report.txt 2>&1
./testsamples.sh >> validation-report.txt 2>&1
```

Offer to create a report file if user requests it.

## Post-Validation Actions

After validation completes:

1. **If successful:**
   - Confirm schemas are ready for distribution
   - Suggest running full build: `/build-local`
   - Safe to commit changes

2. **If issues found:**
   - Ask if user wants help fixing specific errors
   - Offer to analyze error patterns
   - Suggest reviewing CLAUDE.md for troubleshooting guidance

3. **Performance notes:**
   - Report validation time
   - Note any slow-validating samples
   - Suggest optimizations if needed

## Return to Repository Root

Always return to repository root after validation:
```bash
cd ../..
pwd  # Should show /home/user/ubl
```

## Summary Report Format

Provide final summary:
```
=== UBL Schema Validation Summary ===

Test Environment: OK
Main Validation: PASSED
Sample Validation: PASSED (N/N samples)
JSON Validation: PASSED (N/N samples)
Code Lists: OK (validated during build)
Namespace Checks: OK

Total Issues: 0
Build Ready: YES ✓

Validation completed in X seconds.
```

## Notes

- Validation scripts are maintained by UBL editors
- Test expectations may change between versions
- Some warnings are informational, not errors
- Full validation requires completed build artifacts
- Always validate before committing schema changes
