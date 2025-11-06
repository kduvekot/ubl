# New Stage Release Checklist

Use this checklist when creating a new UBL stage release.

## Release Information

- **Previous Stage:** _____________
- **New Stage:** _____________
- **Version:** _____________
- **Date:** _____________
- **Release Manager:** _____________

## Pre-Release Tasks

### 1. Branch Setup
- [ ] Create new branch from previous stage: `git checkout -b ubl-{version}-{stage}`
- [ ] Verify branch created successfully: `git branch --show-current`
- [ ] Push initial branch: `git push -u origin ubl-{version}-{stage}`

### 2. Configuration Updates

#### build.py
- [ ] Update `ubl_stage` = "{new_stage}"
- [ ] Update `ubl_prev_stage` = "{previous_stage}"
- [ ] Verify `ubl_version` is correct
- [ ] Verify `ubl_prev_version` is correct

#### build.sh
- [ ] Update `UBLstage` = "{new_stage}"
- [ ] Update `UBLprevStage` = "{previous_stage}"
- [ ] Verify all variables match build.py
- [ ] Verify export statements are correct

#### UBL.xml Entity Declarations
- [ ] Update `<!ENTITY stage "{new_stage}">`
- [ ] Update `<!ENTITY STAGE "{NEW_STAGE_UPPERCASE}">`
- [ ] Update `<!ENTITY pstage "{previous_stage}">`
- [ ] Update `<!ENTITY PSTAGE "{PREVIOUS_STAGE_UPPERCASE}">`
- [ ] Update `<!ENTITY standard "...">` with stage description
- [ ] Update `<!ENTITY stagetext "...">` to match standard
- [ ] Update `<!ENTITY pubdate "...">` with current date
- [ ] Update `<!ENTITY pubyear "...">` with current year

### 3. Google Spreadsheet Setup

#### Library Spreadsheet
- [ ] Open current library spreadsheet (URL from build.py)
- [ ] File → Make a copy
- [ ] Rename: "UBL {version} Library Elements Spreadsheet - {STAGE} master"
- [ ] Share → "Anyone with link can view"
- [ ] Copy URL (without `/edit...` suffix)
- [ ] Update `lib_google` in build.py
- [ ] Update `libGoogle` in build.sh

#### Documents Spreadsheet
- [ ] Open current documents spreadsheet
- [ ] File → Make a copy
- [ ] Rename: "UBL {version} Document Elements Spreadsheet - {STAGE} master"
- [ ] Share → "Anyone with link can view"
- [ ] Copy URL (without `/edit...` suffix)
- [ ] Update `doc_google` in build.py
- [ ] Update `docGoogle` in build.sh

#### Signature Spreadsheet
- [ ] Open current signature spreadsheet
- [ ] File → Make a copy
- [ ] Rename: "UBL {version} Signature Elements Spreadsheet - {STAGE} master"
- [ ] Share → "Anyone with link can view"
- [ ] Copy URL (without `/edit...` suffix)
- [ ] Update `sig_google` in build.py
- [ ] Update `sigGoogle` in build.sh

### 4. Genericode File Management
- [ ] Rename `UBL-Entities-{version}.gc` → `UBL-Entities-{version}-{prev_stage}.gc`
- [ ] Rename `UBL-Signature-Entities-{version}.gc` → `UBL-Signature-Entities-{version}-{prev_stage}.gc`
- [ ] Verify renamed files exist in repository
- [ ] Note: New .gc files will be generated during build

### 5. Documentation Updates
- [ ] Update `.claude/CLAUDE.md` "Current Branch Context" section
- [ ] Update stage information in CLAUDE.md
- [ ] Review and update any stage-specific documentation
- [ ] Check that README.md references are still accurate

## Build and Validation

### 6. Local Build Test
- [ ] Create target directory: `mkdir -p target`
- [ ] Run local build: `python build.py target local debug`
- [ ] Build completes without errors (exit code 0)
- [ ] Check for warning files in `target/UBL-{version}-{stage}-debug/`:
  - [ ] No `HUB-SKIPPED-INCOMPLETE-ARTEFACTS.txt`
  - [ ] No `INVALID-ASSEMBLED-HUB-XML.txt`
  - [ ] No `INTEGRITY-PROBLEMS.txt`
  - [ ] No `LIST-OF-PROBLEM-CODE-LISTS.txt`
  - [ ] No `UNEXPECTED-TEST-RESULT-WARNING.txt`

### 7. Artifact Verification
- [ ] Verify three .7z archives created:
  - [ ] `UBL-{version}-{stage}-debug.7z` (distribution)
  - [ ] `UBL-{version}-{stage}-debug-archive-only.7z`
  - [ ] `UBL-{version}-{stage}-debug-iso-iec-19845.7z`
- [ ] Extract and review distribution package
- [ ] Check XSD schemas generated in `xsd/` directories
- [ ] Check JSON schemas generated in `json-schema/` directories
- [ ] Review generated documentation (HTML/PDF if available)

### 8. Schema Validation
- [ ] Navigate to `raw/val/`
- [ ] Run main validation: `./test.sh`
- [ ] Run sample validation: `./testsamples.sh`
- [ ] All tests pass
- [ ] No validation errors reported
- [ ] Sample count matches test scripts

### 9. Documentation Review
- [ ] Generated HTML documentation is readable
- [ ] All images display correctly
- [ ] Code examples are properly formatted
- [ ] Version/stage information correct throughout
- [ ] Table of contents complete
- [ ] Cross-references work

### 10. Comparison Reports
- [ ] Review stage comparison report (vs previous stage)
- [ ] Verify changes documented correctly
- [ ] Check `old2newDoc-from-previous-stage-*.xml` entities
- [ ] No unexpected differences
- [ ] All intended changes present

## Commit and Push

### 11. Initial Commit
- [ ] Stage configuration changes: `git add build.py build.sh UBL.xml .claude/CLAUDE.md`
- [ ] Stage genericode renames: `git add UBL-Entities-* UBL-Signature-Entities-*`
- [ ] Create commit with message:
```
Initialize UBL {version} {stage}

- Update build configuration for {stage}
- Rename previous stage genericode files
- Update UBL.xml entity declarations
- Update Google spreadsheet references
- Update Claude Code configuration

Previous stage: {prev_stage}
```
- [ ] Commit created: `git commit`
- [ ] Push to GitHub: `git push -u origin ubl-{version}-{stage}`

### 12. Verify GitHub Actions
- [ ] Go to GitHub Actions tab
- [ ] Verify build workflow triggered
- [ ] Build completes successfully
- [ ] Artifacts available for download
- [ ] Review build logs for issues

## Content Development

### 13. Model Updates (if applicable)
- [ ] Make changes in Google Spreadsheets
- [ ] Document changes in spreadsheet comments
- [ ] Test changes with build
- [ ] Commit changes: `git commit --allow-empty -m "Updated spreadsheet data"`
- [ ] Push: `git push`

### 14. Sample Updates
- [ ] Add new sample instances if needed
- [ ] Update existing samples for changes
- [ ] Add samples to test scripts
- [ ] Validate all samples

### 15. Documentation Updates
- [ ] Update specification text in UBL.xml
- [ ] Add new diagrams/artwork if needed
- [ ] Update examples
- [ ] Review and correct spelling
- [ ] Update change summary sections

## Quality Assurance

### 16. Review Checklist
- [ ] All configuration files synchronized
- [ ] All validation tests pass
- [ ] Documentation builds correctly
- [ ] Comparison reports accurate
- [ ] No uncommitted changes
- [ ] Branch up to date with remote

### 17. Team Review
- [ ] Create pull request (if using PR workflow)
- [ ] Request review from TC editors
- [ ] Address review feedback
- [ ] Obtain approvals

## Publication Preparation

### 18. Final Build
- [ ] Run clean build: `rm -rf target && python build.py target local {stage}`
- [ ] All artifacts generated successfully
- [ ] Download artifacts
- [ ] Archive locally

### 19. Kavi Upload (TC Editors)
- [ ] Upload archive ZIP to Kavi
- [ ] Upload distribution ZIP to Kavi
- [ ] Upload ISO ZIP to Kavi (if applicable)
- [ ] Verify files accessible on Kavi
- [ ] Post announcement to TC mailing list

### 20. Cleanup
- [ ] Delete GitHub Actions workflow artifacts (after archiving to Kavi)
- [ ] Tag release in git: `git tag ubl-{version}-{stage}`
- [ ] Push tag: `git push origin ubl-{version}-{stage}`
- [ ] Update OASIS TC website if applicable

## Post-Release

### 21. Communication
- [ ] Announce to UBL TC mailing list
- [ ] Update TC work product status page
- [ ] Notify liaisons if applicable
- [ ] Post to OASIS announcements if public milestone

### 22. Archive
- [ ] Archive artifacts locally
- [ ] Document any issues encountered
- [ ] Update process documentation if needed
- [ ] Prepare notes for next stage

---

## Notes

**Stage Types:**
- **CSD (Committee Specification Draft):** Development stages, multiple iterations
- **CS (Committee Specification):** Public review, stable
- **OS (OASIS Standard):** Final, approved standard

**Frequency:**
- CSD stages: As needed, typically 3-6 months apart
- CS stages: After CSD stabilizes, ~1-2 per version
- OS stage: Once per version after TC and Board approval

**Key Contacts:**
- TC Chair: _____________
- Editors: _____________
- Release Manager: _____________

**Resources:**
- GitHub Repository: https://github.com/oasis-tcs/ubl
- Kavi Documents: https://www.oasis-open.org/committees/documents.php?wg_abbrev=ubl
- OASIS TC Page: https://www.oasis-open.org/committees/ubl/

---

**Completed by:** _____________
**Date:** _____________
**Verified by:** _____________
