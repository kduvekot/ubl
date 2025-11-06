# UBL Repository - Claude Code Configuration

## Project Overview

This is the **OASIS Universal Business Language (UBL)** standard development repository. UBL is an open library of standard electronic XML business documents for procurement and transportation.

**Key Characteristics:**
- Complex multi-stage specification development (CSD → CS → OS)
- XML Schema generation from Google Spreadsheets
- Multi-format output: XSD, JSON Schema, genericode, documentation
- DocBook-based specification documents
- Branch-based workflow for versions and stages

## Current Branch Context

- **Branch**: ubl-2.5-python
- **Version**: 2.5
- **Stage**: csd01 (Committee Specification Draft 01)
- **Previous Version**: 2.4 (OASIS Standard)
- **Build System**: Python 3.12 (migrating from shell scripts)

## Key File Locations

### Build Configuration
- `build.py` - Python build script (preferred on this branch)
- `build.sh` - Shell build script (legacy, still functional)
- `build-py.xml` - Ant build file for Python builds
- `build.xml` - Ant build file for shell builds
- `build-common.sh` - Common shell utilities

### Source Documents
- `UBL.xml` - Main hub document (specification source)
- `UBL-Party-summary-information.xml` - Party model documentation
- `UBL-Schema-summary-information.xml` - Schema documentation

### Configuration Files
- `config-UBL.xml` - Main schema generation config
- `config-UBL-Signature.xml` - Signature schema config
- `ident-UBL.xml` - Library identification for genericode conversion
- `ident-UBL-Signature.xml` - Signature identification
- `massageModelName.xml` - Google bug workaround directives
- `realta-user-parameters.xml` - Publishing service parameters

### Schema and Samples
- `raw/xsd/` - Hand-authored XML Schema fragments
- `raw/xsd/common/` - 8 UBL-*.xsd files with version hardcoded
- `raw/json-schema/` - Hand-authored JSON Schema fragments
- `raw/xml/` - Sample XML instances
- `raw/json/` - Sample JSON instances
- `raw/cl/` - Code list content and master files
- `raw/mod/` - Model documentation fragments
- `raw/val/` - Validation scripts and demonstration environment

### Reference Genericode Files
- `UBL-Entities-2.4-os.gc` - Previous version library entities
- `UBL-Signature-Entities-2.4-os.gc` - Previous version signature entities

### Previous Version Archives
- `os-UBL-2.0/` through `os-UBL-2.4/` - Code lists from released versions

### Utilities
- `utilities/ant/` - Apache Ant
- `utilities/saxon/` and `utilities/saxon9he/` - XSLT processors
- `utilities/Crane-gc2obdndr/` - Genericode to schema conversion tools

## Build Commands

### Local Development Build
```bash
# Using Python (preferred on this branch)
python build.py target local debug

# Using shell script
./build.sh target local debug
```

### Build with Réalta Publishing (requires credentials)
```bash
python build.py target local debug "username" "password"
```

### GitHub Actions
- Automatically triggers on every push
- Runs both shell and Python builds (Python only on ubl-2.5-python branch)
- Artifacts available in Actions tab for 90 days
- Downloads are doubly-zipped (outer: GitHub, inner: distribution packages)

### Understanding Build Output
After build completes, check `target/UBL-2.5-csd01-{label}/` for:

**Success Indicators:**
- `build.console.{label}.txt` - Build log exists
- `build.exitcode.{label}.txt` - Contains "0" for success
- Three .7z files created: archive, ISO, distribution

**Warning/Error Files** (should NOT exist):
- `ATTENTION-new-entities.txt` - Entity files changed, update local copies
- `HUB-SKIPPED-INCOMPLETE-ARTEFACTS.txt` - Build incomplete
- `INTEGRITY-PROBLEMS.txt` - Files referenced but missing or vice versa
- `INVALID-ASSEMBLED-HUB-XML.txt` - Hub document validation failed
- `LIST-OF-PROBLEM-CODE-LISTS.txt` - Invalid genericode files
- `MISMATCHED-TEST-SAMPLES-SH-WARNING.txt` - Sample count mismatch
- `NDR-SPELL-CHECK-WARNING.txt` - See unexpectedWords.txt for details
- `UNEXPECTED-SAMPLES-NS-PI-DETAILS.txt` - Namespace issues in samples
- `UNEXPECTED-TEST-RESULT-WARNING.txt` - Validation test failures

## Common Development Tasks

### 1. Creating a New Stage
1. Create branch: `git checkout -b ubl-{version}-{stage}`
2. Update `build.py` and `build.sh`:
   - `title`, `package`, `ubl_version`, `ubl_stage`
   - `ubl_prev_stage_version`, `ubl_prev_stage`, `ubl_prev_version`
3. Update Google spreadsheet titles (copy from previous stage)
4. Update `UBL.xml` entity declarations in internal DTD subset
5. Replace previous stage genericode files:
   - Rename `UBL-Entities-{version}.gc` → `UBL-Entities-{version}-{prevstage}.gc`
6. Update `.claude/CLAUDE.md` with new version context (this file!)

### 2. Creating a New Version
Includes all stage steps above, plus:
1. Update version in 8 XSD fragments in `raw/xsd/common/UBL-*.xsd`:
   - Comment headers (stage, date, URLs)
   - `version=` attribute in schema elements
2. Update `raw/json-schema/common/UBL-*.json` schema references
3. Update `config-UBL.xml` version comments
4. Update `massageModelName.xml` if model names changed
5. Add new CVA code list entries in `UBL-CVA-Skeleton.cva`
6. Create new CVA Schematron shell: `UBL-DefaultDTQ-{version}.sch`
7. Update 4 validation scripts in `raw/val/` (first line version refs)
8. Add previous version genericode files:
   - `UBL-Entities-{prevVersion}-os.gc`
   - `UBL-Signature-Entities-{prevVersion}-os.gc`

### 3. Updating Spreadsheets
Google Spreadsheets are the **source of truth** for the UBL model:
- **Library**: `libGoogle` URL in build config
- **Documents**: `docGoogle` URL in build config
- **Signature**: `sigGoogle` URL in build config

**Process:**
1. Copy previous stage spreadsheet in Google Sheets
2. Update title: "UBL {version} {type} Elements Spreadsheet - {STAGE} master"
3. Make model changes in spreadsheet
4. Update URL in `build.py` and `build.sh`
5. Commit empty: `git commit --allow-empty -m "Updated spreadsheet data"`
6. Push to trigger build: `git push`

### 4. Validating Build Locally
```bash
cd raw/val
./test.sh              # Run validation environment test
./testsamples.sh       # Validate all sample instances
```

### 5. Previewing Hub Document (UBL.xml)
**Windows:** Drag `UBL.xml` to Internet Explorer, refresh with Ctrl-R
**macOS:** Drag `UBL.xml` to Safari, refresh with Cmd-R
**Note:** Images appear oversized (uses PDF high-res images, not HTML low-res)

## Important Constraints and Rules

### ⛔ NEVER Do These
- **Edit `-ent.xml` files directly** - They are auto-generated from XML sources
- **Commit without build test** - Always run local build first
- **Push to main/master directly** - Use feature branches and PRs
- **Delete workflow artifacts thoughtlessly** - Check branch name first
- **Edit spreadsheets without copying** - Always work from stage-specific copies
- **Skip version updates in XSD files** - All 8 common/*.xsd must match

### ✅ ALWAYS Do These
- **Update CLAUDE.md** when changing version/stage (this file!)
- **Run local build** before pushing to GitHub
- **Check for warning .txt files** in build output
- **Quote paths with spaces** in shell commands
- **Use absolute paths** in build scripts when possible
- **Document commit reasons** clearly in commit messages
- **Delete GitHub Action workflows** after downloading artifacts (saves space)
- **Archive to Kavi** - Official publishing happens there, not GitHub

## Google Spreadsheets Integration

Build process automatically downloads from Google during GitHub Actions:
- Downloaded as ODS format
- Converted to genericode (.gc files)
- Genericode processed to generate XSD, JSON Schema, documentation

**Manual Override:**
For reproducing old builds, copy these from archive to parent directory:
- `UBL-Signature-Google.ods`
- `UBL-Library-Google.ods`
- `UBL-Documents-Google.ods`

**IMPORTANT:** Delete these files to resume online spreadsheet access!

## Coding Standards

### Python
- Follow PEP 8 style guide
- Use type hints for function parameters and returns
- Prefer dataclasses for configuration objects
- Use pathlib.Path for file operations
- Error handling: catch specific exceptions, provide helpful messages
- Command-line: use sys.argv or argparse for parameters

### XML/XSLT
- Maintain DocBook 5.0 validation
- Use entity references for repeated content
- Keep hand-authored XSD fragments minimal
- Follow OASIS naming conventions

### Shell Scripts
- Always quote paths containing spaces: `"${path}"`
- Check for required arguments at script start
- Use absolute paths for build artifacts
- Exit with meaningful codes (0 = success)

### Git Commits
- **Format**: Brief summary (50 chars), then detailed body if needed
- **Style**: Describe "why" not just "what"
- **Scope**: Atomic commits (one logical change)
- **Messages**: Use conventional commit format when applicable

## GitHub Workflow

### Branch Naming
- **Feature branches**: `claude/{description}-{session-id}`
- **Release branches**: `ubl-{version}-{stage}` (e.g., ubl-2.5-csd01)

### Push Protocol
```bash
# Always use -u flag for new branches
git push -u origin <branch-name>

# Branch must start with 'claude/' and end with session ID
# Otherwise: 403 HTTP error
```

### Retry Logic (Network Issues)
- Retry up to 4 times with exponential backoff: 2s, 4s, 8s, 16s
- Applies to: git push, git fetch, git pull

### Pull Requests
- Create PR from feature branch to release branch (e.g., ubl-2.5-csd01)
- Never PR directly to main/master
- Include summary of changes and test results
- Reference related issues if applicable

## Dependencies and Environment

### Required Software
- **Java**: JDK 1.8 (Zulu distribution recommended)
- **Python**: 3.12+
- **System packages**: aspell, libreoffice, pandoc
- **Python packages**: py7zr (for 7z archive creation)
- **Utilities**: 7z, git, bash

### XSLT Processors
- Saxon-HE 9 (utilities/saxon9he/saxon9he.jar)
- Main class: net.sf.saxon.Transform

### Java Classpath
```bash
utilities/saxon/saxon.jar:utilities/ant/lib/ant-launcher.jar:utilities/saxon9he/saxon9he.jar
```

## Réalta Publishing Service

External publishing service for OASIS and ISO layouts:
- **Input**: XML hub document via HTTP API
- **Outputs**: HTML, PDF (OASIS layout), PDF/DOCX (ISO Directives Part 2 layout)
- **Credentials**: Stored in GitHub secrets (REALTA_USERNAME, REALTA_PASSWORD)
- **Optional**: Can build without credentials (limited output)

## Troubleshooting

### Build Fails with "Transform.class not found"
```bash
jar tf utilities/saxon9he/saxon9he.jar | grep net/sf/saxon/Transform.class
```
Verify Saxon JAR integrity, re-download if needed.

### Spreadsheet Download Fails
- Check URL format (no `/edit...` at end)
- Verify spreadsheet is publicly readable
- Check GitHub Actions secrets for credentials

### Validation Failures
- Check `raw/val/test.sh` output
- Review sample files in `raw/xml/` for schema compliance
- Verify namespace declarations in samples

### Empty Console Log
Build script failed unexpectedly. Check GitHub Actions workflow log.

### Entity Files Changed
If `ATTENTION-new-entities.txt` appears:
1. Look in `archive-only/new-entities/` subdirectory
2. Copy new entity files to repository root
3. Commit updated entities

## Useful Slash Commands

This repository includes custom slash commands in `.claude/commands/`:
- `/build-local` - Build locally with validation checks
- `/create-release` - Guide for creating new version/stage
- `/validate-schemas` - Run schema validation tests
- `/analyze-spreadsheet` - Analyze spreadsheet changes
- `/compare-versions` - Compare UBL versions/stages

Type `/` in Claude Code to see all available commands.

## Additional Resources

- **OASIS TC**: https://www.oasis-open.org/committees/ubl/
- **GitHub Actions**: https://github.com/oasis-tcs/ubl/actions
- **Kavi Documents**: https://www.oasis-open.org/committees/documents.php?wg_abbrev=ubl
- **UBL Specification**: Generated during build process
- **README**: See repository README.md for comprehensive documentation

## Team Collaboration

- **Maintainers**: Request access from TC chair with GitHub username
- **Editors**: Responsible for final review and Kavi publishing
- **Subcommittees**: Create separate branches with custom configurations
- **Public feedback**: Welcomed under OASIS Feedback License

---

**Last Updated**: 2025-11-06
**Maintained by**: UBL TC Maintainers
**Version Context**: ubl-2.5-python branch, UBL 2.5 CSD01
