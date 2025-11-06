# Analyze Google Spreadsheet Configuration

Analyze and manage Google Spreadsheet references for UBL data model definitions.

## Overview

UBL data models are defined in three Google Spreadsheets:
- **Library Spreadsheet**: Common library components (reusable elements)
- **Documents Spreadsheet**: Document-level structures (invoices, orders, etc.)
- **Signature Spreadsheet**: Digital signature components

This command helps you work with these spreadsheets and their configuration.

## Instructions

### Step 1: Identify Spreadsheet Type

Ask the user which spreadsheet they want to analyze:
1. Library (common components)
2. Documents (document types)
3. Signature (digital signatures)
4. All spreadsheets

Or accept spreadsheet URL directly if provided as argument: `$ARGUMENTS`

### Step 2: Read Current Configuration

Read the current spreadsheet URLs from `build.py`:

```python
lib_google = "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"
doc_google = "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"
sig_google = "https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"
```

Display current configuration:
```
Current Spreadsheet Configuration:
-----------------------------------
Library:   {lib_google}
Documents: {doc_google}
Signature: {sig_google}

Version: {ubl_version}
Stage:   {ubl_stage}
```

### Step 3: Extract Spreadsheet IDs

From each URL, extract the spreadsheet ID (the part between `/d/` and the next `/`).

Display:
```
Spreadsheet IDs:
Library:   {lib_id}
Documents: {doc_id}
Signature: {sig_id}
```

### Step 4: Verify URL Format

Check that URLs are properly formatted:

**✓ Correct format:**
```
https://docs.google.com/spreadsheets/d/1bWAhvsb8iCMLhgUrHFzY
```

**✗ Incorrect format (has /edit):**
```
https://docs.google.com/spreadsheets/d/1bWAhvsb8iCMLhgUrHFzY/edit#gid=0
```

If URLs contain `/edit...`, warn the user and offer to fix them:
- Remove everything after the spreadsheet ID
- Update build.py and build.sh with corrected URLs

### Step 5: Check Spreadsheet Naming Convention

Expected spreadsheet titles should follow this pattern:
- "UBL {version} Library Elements Spreadsheet - {STAGE} master"
- "UBL {version} Document Elements Spreadsheet - {STAGE} master"
- "UBL {version} Signature Elements Spreadsheet - {STAGE} master"

Examples:
- "UBL 2.5 Library Elements Spreadsheet - CSD01 master"
- "UBL 2.5 Document Elements Spreadsheet - CS01 master"

**Note:** Cannot verify title without accessing spreadsheet, but can provide expected format.

### Step 6: Compare with Previous Configuration

If there's a parent branch (e.g., comparing to previous stage), offer to check differences:

```bash
# Get previous branch name
git branch -r | grep "ubl-{version}"
```

If previous branch exists, read its build.py and compare spreadsheet URLs.

Report if URLs have changed:
```
Spreadsheet URL Changes:
------------------------
Library:   CHANGED ✓ (new spreadsheet for this stage)
Documents: UNCHANGED (reusing previous spreadsheet)
Signature: UNCHANGED (reusing previous spreadsheet)
```

### Step 7: Verify Spreadsheet Accessibility

Inform the user about accessibility requirements:

**Requirements for build process:**
- Spreadsheet must be **"Anyone with link can view"**
- Or build process must have read credentials (REALTA_USERNAME/PASSWORD)
- URLs must not have access restrictions

**Cannot directly test accessibility**, but provide checklist:
```
Spreadsheet Access Checklist:
☐ Spreadsheet shared as "Anyone with link can view"
☐ No sign-in required to access
☐ URL copied without /edit... suffix
☐ Spreadsheet contains UBL data (not empty)
```

### Step 8: Explain Spreadsheet Download Process

Explain how spreadsheets are used:

```
How Spreadsheets are Processed:
--------------------------------
1. Build process downloads ODS format from Google
2. ODS converted to genericode (.gc files)
3. Genericode processed to generate:
   - XSD schemas (raw/xsd/)
   - JSON schemas (raw/json-schema/)
   - Documentation (embedded in UBL.xml)
4. Validation performed on generated schemas
5. Distribution packages created

Files Generated:
- UBL-Entities-{version}.gc (from Library)
- UBL-Signature-Entities-{version}.gc (from Signature)
- Multiple .xsd files
- Multiple .json files
```

### Step 9: Check for Offline Spreadsheet Overrides

Check if offline ODS files exist in parent directory:

```bash
ls ../*-Google.ods 2>/dev/null
```

If found:
```
⚠ WARNING: Offline Spreadsheet Overrides Detected
--------------------------------------------------
Found: {list of .ods files}

These offline files will be used INSTEAD of downloading from Google.
This is typically used to reproduce old builds.

To resume online access, delete these files:
rm ../*-Google.ods
```

### Step 10: Offer Actions

Based on the analysis, offer these actions:

**If URL format is wrong:**
```
Action: Fix URL format in build.py and build.sh?
```

**If changing spreadsheet URLs:**
```
You are changing spreadsheet references. This suggests:
a) Creating a new stage (copied spreadsheets)
b) Fixing incorrect URLs
c) Testing with different data

Which scenario applies?
```

**If starting new work:**
```
To create new stage spreadsheets:
1. Go to current spreadsheet URL
2. File → Make a copy
3. Rename with new stage: "UBL {version} {Type} - {NEW_STAGE} master"
4. Share → "Anyone with link can view"
5. Copy new URL (without /edit...)
6. Update build.py and build.sh
7. Commit changes

Would you like help updating the configuration?
```

### Step 11: Update Configuration (if requested)

If user provides new spreadsheet URLs:

1. Validate URL format
2. Extract spreadsheet IDs
3. Update build.py:
   ```python
   lib_google = "new_url"
   doc_google = "new_url"
   sig_google = "new_url"
   ```
4. Update build.sh with same URLs
5. Show diff of changes
6. Offer to commit:
   ```bash
   git add build.py build.sh
   git commit -m "Update spreadsheet URLs for {stage}"
   ```

### Step 12: Trigger Build with New Spreadsheets

After updating URLs, explain next steps:

```
Next Steps:
-----------
1. Commit spreadsheet URL changes
2. Push to GitHub to trigger build:
   git commit --allow-empty -m "Updated spreadsheet data"
   git push

   OR run local build:
   python build.py target local debug

3. Build process will download latest spreadsheet data
4. Review generated schemas and documentation
5. Check for validation errors
6. Compare with previous stage using generated reports
```

Offer to run local build: **"Run `/build-local` now?"**

## Spreadsheet Structure Reference

For user reference, typical spreadsheet columns include:

**Library/Document Spreadsheets:**
- Component name
- Property term
- Cardinality
- Object class
- Data type
- Definition
- Business terms
- Examples

**Common Issues:**
- Typos in component names
- Incorrect cardinality
- Missing definitions
- Invalid data type references
- Circular dependencies

## Troubleshooting

### Error: Cannot download spreadsheet
**Causes:**
- Spreadsheet not publicly accessible
- Invalid spreadsheet ID
- Network issues
- Google API rate limiting

**Solutions:**
- Verify sharing settings
- Check URL format
- Try manual download and place ODS in parent directory
- Wait and retry

### Error: Invalid spreadsheet format
**Causes:**
- Wrong spreadsheet structure
- Missing required columns
- Corrupted data

**Solutions:**
- Compare with previous version spreadsheet
- Verify column headers
- Check for special characters or formatting issues

### Warning: Spreadsheet appears empty
**Cause:** Wrong sheet selected or spreadsheet truly empty

**Solution:** Verify correct sheet/tab is being processed

## Advanced: Manual Spreadsheet Processing

For debugging, can manually process spreadsheets:

```bash
# If you have ODS file
cp {spreadsheet}.ods ../UBL-Library-Google.ods

# Run build - it will use local file
python build.py target local debug

# Check generated genericode
ls -lh target/*/UBL-Entities-*.gc

# Restore online access
rm ../*-Google.ods
```

## Summary Report

Provide final summary:
```
=== Spreadsheet Configuration Analysis ===

Current Configuration: UBL {version} {stage}
Library:   {URL} [{ID}]
Documents: {URL} [{ID}]
Signature: {URL} [{ID}]

URL Format: ✓ Valid / ✗ Invalid
Offline Overrides: None / {count} files found
Configuration Status: Up to date / Needs update

Recommendations:
- {specific recommendation if any}

Ready for build: YES/NO
```

## Notes

- Spreadsheets are **source of truth** for UBL data model
- URLs must not include `/edit...` suffix
- Build process downloads automatically from Google
- Offline ODS files override online access
- Always test build after changing spreadsheet URLs
- Spreadsheet title should reflect version and stage
