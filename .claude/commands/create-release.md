# Create New UBL Release

Guide the user through creating a new UBL version or stage release with all necessary configuration updates.

## Instructions

### Step 1: Determine Release Type

Ask the user:
- **"Are you creating a new VERSION (e.g., 2.5 → 2.6) or a new STAGE (e.g., csd01 → csd02)?"**

**Stage progression:** csd01 → csd02 → ... → cs01 → os
**Version progression:** 2.x → 2.(x+1)

### Step 2: Gather Information

Based on release type, collect:

**For New Stage:**
- Current version (e.g., 2.5)
- New stage name (e.g., csd02)
- Previous stage name (e.g., csd01)

**For New Version:**
- New version number (e.g., 2.6)
- New stage (typically starts at csd01)
- Previous version (e.g., 2.5)
- Previous stage of previous version (typically "os")

### Step 3: Read Current Configuration

Read `build.py` and display current values:
```python
title = "UBL X.X"
package = "UBL-X.X"
ubl_version = "X.X"
ubl_stage = "csdXX"
ubl_prev_stage_version = "X.X"
ubl_prev_stage = "csdXX"
ubl_prev_version = "X.X"
```

Show these to the user and confirm the new values.

### Step 4: Create New Branch

```bash
# For new stage
git checkout -b ubl-{version}-{stage}

# For new version
git checkout -b ubl-{version}-{stage}
```

Example: `git checkout -b ubl-2.5-csd02`

Confirm branch creation: `git branch --show-current`

### Step 5: Update Build Configuration Files

#### 5a. Update build.py

Edit the following variables in `/home/user/ubl/build.py`:
- `title` → "UBL {version}"
- `package` → "UBL-{version}"
- `ubl_version` → "{version}"
- `ubl_stage` → "{stage}"
- `ubl_prev_stage_version` → "{previous stage version}"
- `ubl_prev_stage` → "{previous stage}"
- `ubl_prev_version` → "{previous version}"

**Important:** Keep Google spreadsheet URLs unchanged for now (will update separately).

#### 5b. Update build.sh

Edit the same variables in `/home/user/ubl/build.sh` to match build.py.

Confirm both files are synchronized.

### Step 6: Update Google Spreadsheets

Instruct the user:

**"You need to copy the Google Spreadsheets for the new stage:"**

1. **Library Spreadsheet:**
   - Go to current libGoogle URL (from build config)
   - File → Make a copy
   - Rename: "UBL {version} Library Elements Spreadsheet - {STAGE} master"
   - Share as "Anyone with link can view"
   - Copy new URL (without `/edit...` suffix)

2. **Documents Spreadsheet:**
   - Same process for docGoogle URL
   - Rename: "UBL {version} Document Elements Spreadsheet - {STAGE} master"

3. **Signature Spreadsheet:**
   - Same process for sigGoogle URL
   - Rename: "UBL {version} Signature Elements Spreadsheet - {STAGE} master"

**Ask user to provide the three new URLs**, then update build.py and build.sh:
```python
lib_google = "https://docs.google.com/spreadsheets/d/NEW_ID"
doc_google = "https://docs.google.com/spreadsheets/d/NEW_ID"
sig_google = "https://docs.google.com/spreadsheets/d/NEW_ID"
```

### Step 7: Update UBL.xml Entity Declarations

Edit `/home/user/ubl/UBL.xml` internal DTD subset.

Find the entity declarations (near top of file) and update:
```xml
<!ENTITY version  "{version}">
<!ENTITY pversion "{prev_version}">
<!ENTITY stage    "{stage}">
<!ENTITY STAGE    "{STAGE_UPPERCASE}">
<!ENTITY pstage   "{prev_stage}">
<!ENTITY PSTAGE   "{PREV_STAGE_UPPERCASE}">
<!ENTITY standard "{Standard name - e.g., Committee Specification Draft 01}">
<!ENTITY stagetext "{Same as standard}">
<!ENTITY pubdate  "{Month Day, Year}">
<!ENTITY pubyear  "{Year}">
```

### Step 8: Update Genericode Files (Stage Changes Only)

For stage changes, rename previous stage genericode files:

```bash
# If previous stage was csd01 and new is csd02, rename:
mv UBL-Entities-{version}.gc UBL-Entities-{version}-csd01.gc
mv UBL-Signature-Entities-{version}.gc UBL-Signature-Entities-{version}-csd01.gc
```

**Note:** These files will be regenerated during build with current stage name.

### Step 9: Additional Steps for NEW VERSION

If this is a new version (not just stage), perform these additional updates:

#### 9a. Update XSD Schema Fragments

Edit ALL 8 files in `raw/xsd/common/UBL-*.xsd`:
- UBL-CommonAggregateComponents-2.x.xsd
- UBL-CommonBasicComponents-2.x.xsd
- UBL-CommonExtensionComponents-2.x.xsd
- UBL-CommonSignatureComponents-2.x.xsd
- UBL-ExtensionContentDataType-2.x.xsd
- UBL-QualifiedDataTypes-2.x.xsd
- UBL-SignatureAggregateComponents-2.x.xsd
- UBL-SignatureBasicComponents-2.x.xsd
- UBL-UnqualifiedDataTypes-2.x.xsd

**In each file:**
1. Update comment header:
   - Library version and stage
   - Release date
   - URLs to docs.oasis-open.org

2. Update `version=` attribute in `<xsd:schema>` element:
   ```xml
   <xsd:schema version="{version}">
   ```

3. Update schemaLocation attributes referencing other UBL schemas

#### 9b. Update JSON Schema Fragments

Edit `raw/json-schema/common/UBL-*.json` files to update version references.

#### 9c. Update config-UBL.xml

Update version and stage comments at the top of `config-UBL.xml` and `config-UBL-Signature.xml`.

#### 9d. Update CVA Files

- Add entries to `UBL-CVA-Skeleton.cva` for new code lists if applicable
- Create `UBL-DefaultDTQ-{version}.sch` (copy from previous version)

#### 9e. Update Validation Scripts

Edit first line of 4 scripts in `raw/val/` to reference new version:
- `validate-UBL-{version}.sh`
- `validate-UBL-{version}.bat`
- (and two others if present)

#### 9f. Add Previous Version Genericode Files

Ensure these files exist in repository root:
```
UBL-Entities-{prev_version}-os.gc
UBL-Signature-Entities-{prev_version}-os.gc
```

Copy from `os-UBL-{prev_version}/` directory if needed.

### Step 10: Update .claude/CLAUDE.md

Edit `.claude/CLAUDE.md` to update the "Current Branch Context" section:
```markdown
## Current Branch Context

- **Branch**: ubl-{version}-{stage}
- **Version**: {version}
- **Stage**: {stage}
- **Previous Version**: {prev_version}
- **Build System**: Python 3.12
```

### Step 11: Commit Changes

Create a comprehensive commit with all changes:

```bash
git add build.py build.sh UBL.xml .claude/CLAUDE.md
# Add other modified files based on version vs stage
git commit -m "Initialize UBL {version} {stage} release

- Update build configuration for version {version}, stage {stage}
- Update UBL.xml entity declarations
- Update Google spreadsheet references
[Add more details based on what was changed]
"
```

### Step 12: Display Completion Checklist

Show the user this checklist of remaining manual tasks:

**✓ Completed by this process:**
- [x] Created new branch
- [x] Updated build.py and build.sh
- [x] Updated UBL.xml entities
- [x] Updated CLAUDE.md context
- [x] Committed initial configuration

**⚠ Manual tasks required:**
- [ ] Copy and rename Google Spreadsheets
- [ ] Update spreadsheet URLs in build configs
- [ ] Make model changes in spreadsheets (if applicable)
- [ ] Run local build to test: `python build.py target local debug`
- [ ] Verify build completes without errors
- [ ] Review generated documentation
- [ ] Push branch: `git push -u origin ubl-{version}-{stage}`
- [ ] Create pull request when ready

**📋 For new versions only:**
- [ ] Update all 8 XSD files in raw/xsd/common/
- [ ] Update JSON schema files
- [ ] Update validation scripts
- [ ] Copy previous version genericode files
- [ ] Update CVA skeleton and Schematron

### Step 13: Offer to Run Build Test

Ask user: **"Would you like me to run a local build test to verify the configuration?"**

If yes, execute: `/build-local`

## Expected Outcome

After completing these steps:
1. New branch created and checked out
2. All configuration files updated
3. Initial commit made
4. User has clear checklist of remaining tasks
5. Ready for local build testing

## Notes

- **Stage changes** are simpler (fewer files to update)
- **Version changes** require extensive file updates
- Always test build locally before pushing
- Spreadsheet copying must be done manually in Google Sheets
- Genericode files are auto-generated during build
