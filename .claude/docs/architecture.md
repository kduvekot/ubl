# UBL Build System Architecture

## Overview

The UBL build system transforms Google Spreadsheet data models into distributable XML schemas, JSON schemas, and comprehensive documentation. This document explains the architecture, data flow, and key components.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                  Google Spreadsheets (Source of Truth)       │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐     │
│  │   Library    │  │   Documents   │  │  Signatures  │     │
│  │  Components  │  │    Models     │  │   Models     │     │
│  └──────────────┘  └───────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│               Build Process (Ant + Python + XSLT)            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 1. Download ODS from Google                          │   │
│  │ 2. Convert ODS → Genericode (.gc)                    │   │
│  │ 3. Transform Genericode → XSD/JSON Schema            │   │
│  │ 4. Generate Documentation (DocBook → HTML/PDF)       │   │
│  │ 5. Validate Schemas and Samples                      │   │
│  │ 6. Package Distribution Archives                     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Distribution Packages                     │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐     │
│  │     XSD      │  │  JSON Schema  │  │     HTML     │     │
│  │   Schemas    │  │   Definitions │  │  + PDF Docs  │     │
│  └──────────────┘  └───────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐     │
│  │   Samples    │  │  Code Lists   │  │  Validation  │     │
│  │   (XML/JSON) │  │  (Genericode) │  │   Artifacts  │     │
│  └──────────────┘  └───────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### Phase 1: Model Acquisition
**Input:** Google Spreadsheet URLs
**Process:**
1. GitHub Actions or local build invokes build script
2. Downloads three spreadsheets as ODS format
3. Stores temporarily or uses cached versions

**Key Files:**
- `build.py` / `build.sh` - Contains spreadsheet URLs
- `libGoogle`, `docGoogle`, `sigGoogle` - URL parameters

**Output:** ODS files (temporary)

### Phase 2: Genericode Generation
**Input:** ODS spreadsheet files
**Process:**
1. Crane ods2obdgc utility processes ODS
2. Extracts component definitions, cardinality, types
3. Generates genericode XML format (OASIS standard)
4. Applies model name massaging (Google bug workarounds)

**Key Files:**
- `utilities/Crane-ods2obdgc/` - Conversion utilities
- `ident-UBL.xml` - Identification for library genericode
- `ident-UBL-Signature.xml` - Identification for signature genericode
- `massageModelName.xml` - Name correction rules

**Output:**
- `UBL-Entities-{version}.gc` - Library components genericode
- `UBL-Signature-Entities-{version}.gc` - Signature components genericode

### Phase 3: Schema Generation
**Input:** Genericode files
**Process:**
1. Crane gc2obdndr utility transforms genericode to schemas
2. Applies hand-authored schema fragments from `raw/xsd/`
3. Generates XSD schemas following UBL naming and design rules
4. Creates JSON schemas with similar structure

**Key Files:**
- `utilities/Crane-gc2obdndr/` - Schema generation utilities
- `config-UBL.xml` - Main schema generation configuration
- `config-UBL-Signature.xml` - Signature schema configuration
- `raw/xsd/common/*.xsd` - Hand-authored schema fragments
- `raw/json-schema/common/*.json` - JSON schema fragments

**Output:**
- `xsd/common/*.xsd` - Common component schemas
- `xsd/maindoc/*.xsd` - Document schemas (Invoice, Order, etc.)
- `json-schema/` - JSON schema definitions

### Phase 4: Documentation Generation
**Input:**
- `UBL.xml` (DocBook hub document)
- Genericode files
- Schema summary information
- Entity files

**Process:**
1. XSLT transformations generate entity files from sources
2. Saxon processes DocBook with entities
3. Réalta publishing service (optional) generates formatted output
4. Creates HTML (web) and PDF (print) versions
5. Generates ISO Directives Part 2 format (for ISO publication)

**Key Files:**
- `UBL.xml` - Main specification hub document
- `UBL-Party-summary-information.xml` - Party model documentation
- `UBL-Schema-summary-information.xml` - Schema documentation
- `db/spec-0.8/` - DocBook stylesheets
- `partydoc2db.xsl`, `schemadoc2db.xsl` - Documentation transformations
- `hub2processSummary.xsl` - Process summary generation

**Output:**
- `UBL-{version}.html` - OASIS HTML specification
- `UBL-{version}.pdf` - OASIS PDF specification
- `UBL-{version}-ISO.pdf` - ISO formatted PDF
- `UBL-{version}-ISO.docx` - ISO formatted Word document

### Phase 5: Validation
**Input:** Generated schemas and sample instances
**Process:**
1. Validates XSD schemas for well-formedness
2. Validates XML samples against schemas
3. Validates JSON samples against JSON schemas
4. Runs genericode integrity checks
5. Spell-checks documentation
6. Verifies namespace declarations

**Key Files:**
- `raw/val/test.sh` - Main validation script
- `raw/val/testsamples.sh` - Sample validation script
- `raw/xml/*.xml` - Sample XML instances
- `raw/json/*.json` - Sample JSON instances
- `spellcheck-UBL.txt` - Custom dictionary

**Output:**
- Validation reports
- Warning files (if issues detected)
- Pass/fail status

### Phase 6: Packaging
**Input:** All generated artifacts
**Process:**
1. Organizes files into distribution structure
2. Creates archive package (inputs + intermediates)
3. Creates ISO package (ISO-formatted outputs)
4. Creates distribution package (final deliverables)
5. Compresses with 7z (maximum compression)

**Output:**
- `UBL-{version}-{stage}-{label}.7z` - Distribution package
- `UBL-{version}-{stage}-{label}-archive-only.7z` - Archive package
- `UBL-{version}-{stage}-{label}-iso-iec-19845.7z` - ISO package

## Technology Stack

### Core Technologies
- **Apache Ant** - Build orchestration
- **Python 3.12** - Build script implementation (new)
- **Bash** - Build script implementation (legacy)
- **XSLT 2.0** - Transformations (Saxon)
- **DocBook 5.0** - Documentation format

### Processors
- **Saxon-HE 9** - XSLT and XQuery processor
- **Java 8** - Runtime for Saxon and Ant
- **LibreOffice** - ODS processing (headless)

### Utilities
- **Crane gc2obdndr** - Genericode to schema converter
- **Crane ods2obdgc** - Spreadsheet to genericode converter
- **Crane cva2sch** - Code value validation
- **Aspell** - Spell checking
- **Pandoc** - Document format conversion (auxiliary)
- **7z** - Archive compression

### External Services
- **Réalta Publishing** - Professional document formatting
- **Google Sheets** - Collaborative model editing

## Build Targets

### Local Development
```bash
python build.py target local debug
```
- Fast build for testing
- Skips Réalta publishing
- Uses "debug" label
- Output in `target/` directory

### GitHub Actions
```bash
python build.py target github {timestamp}z
```
- Full build with all outputs
- Includes Réalta publishing (if credentials available)
- Timestamped label
- Automatic artifact upload

### Production Release
```bash
python build.py target release {version}-{stage}
```
- Official OASIS release build
- Full validation and integrity checks
- Suitable for publication to Kavi and OASIS Docs

## Configuration Management

### Version Configuration
Defined in `build.py` and `build.sh`:
```python
ubl_version = "2.5"           # Current version
ubl_stage = "csd01"           # Current stage
ubl_prev_version = "2.4"      # Previous version for comparison
ubl_prev_stage = "os"         # Previous stage
ubl_prev_stage_version = "2.4" # Version of previous stage
```

### Build Parameters
- `title` - Human-readable title
- `package` - Package name prefix
- `rawdir` - Source materials directory
- `includeISO` - Generate ISO outputs (true/false)
- Spreadsheet URLs (libGoogle, docGoogle, sigGoogle)

### Entity Management
Auto-generated entity files:
- `summary-parties-ent.xml` - Party summaries
- `summary-schemas-ent.xml` - Schema summaries
- `summary-namespaces-ent.xml` - Namespace declarations
- `summary-examples-ent.xml` - Example references
- `summary-processes-ent.xml` - Process summaries
- `old2newDoc-from-previous-version-*.xml` - Version comparison
- `old2newDoc-from-previous-stage-*.xml` - Stage comparison

## Error Handling

### Build Failure Indicators
Warning files created in output directory when issues detected:

| File | Meaning | Action |
|------|---------|--------|
| `ATTENTION-new-entities.txt` | Entities changed | Copy new entities to repo |
| `HUB-SKIPPED-INCOMPLETE-ARTEFACTS.txt` | Build incomplete | Check console log |
| `INTEGRITY-PROBLEMS.txt` | File mismatches | Fix file references |
| `INVALID-ASSEMBLED-HUB-XML.txt` | Hub validation failed | Fix UBL.xml |
| `LIST-OF-PROBLEM-CODE-LISTS.txt` | Code list issues | Check genericode files |
| `MISMATCHED-TEST-SAMPLES-*.txt` | Sample count wrong | Update test scripts |
| `NDR-SPELL-CHECK-WARNING.txt` | Spelling errors | Review unexpectedWords.txt |
| `UNEXPECTED-SAMPLES-NS-PI-DETAILS.txt` | Namespace problems | Fix sample files |
| `UNEXPECTED-TEST-RESULT-WARNING.txt` | Validation failed | Review test output |

### Exit Codes
- `0` - Success (always returned by wrapper scripts)
- Non-zero in `build.exitcode.*.txt` - Build failed

## Performance Characteristics

### Build Times
- **Local build**: 10-30 minutes (without Réalta)
- **GitHub Actions**: 25-35 minutes (with Réalta)
- **Bottlenecks**:
  - XSLT transformations (CPU intensive)
  - Réalta API (network latency)
  - LibreOffice ODS conversion (I/O intensive)

### Resource Usage
- **Disk space**: ~1 GB build artifacts
- **Memory**: ~2 GB peak (Saxon transformations)
- **Network**: ~50 MB download (spreadsheets + dependencies)

### Optimization Strategies
- Cache spreadsheet ODS files between builds
- Parallel XSLT processing where possible
- Incremental validation (skip unchanged files)
- Local caching of Crane utilities

## Migration: Shell to Python

### Current State (ubl-2.5-python branch)
- Python implementation: `build.py`
- Maintains parity with `build.sh`
- Uses subprocess for Ant invocation
- Better error handling and logging
- Type-safe configuration (dataclasses)

### Benefits of Python Implementation
1. Cross-platform compatibility (Windows native)
2. Better error messages and debugging
3. Type safety and IDE support
4. Easier maintenance and extension
5. Consistent behavior across environments

### Compatibility
- Both implementations produce identical output
- Configuration synchronized between build.py and build.sh
- GitHub Actions tests both implementations
- Migration path: verify Python output matches shell output

## Extension Points

### Adding New Document Types
1. Update Documents spreadsheet
2. Add sample instances to `raw/xml/`
3. Update `UBL-Schema-summary-information.xml`
4. Add validation tests to `raw/val/testsamples.sh`

### Adding New Components
1. Update Library or Documents spreadsheet
2. Update `massageModelName.xml` if needed
3. Update code lists in `raw/cl/` if new value lists
4. Update spell-check dictionary if new terms

### Adding New Code Lists
1. Edit `raw/cl/master-code-list-UBL-*.xml`
2. Run code list tooling (see README)
3. Generate genericode files
4. Update `UBL-CVA-Skeleton.cva` for validation

### Customizing Output
1. Modify XSLT in `utilities/Crane-gc2obdndr/`
2. Update configuration in `config-UBL.xml`
3. Adjust DocBook stylesheets in `db/spec-0.8/`
4. Configure Réalta parameters in `realta-user-parameters.xml`

## Debugging

### Enable Verbose Logging
```bash
# In build.py, run Ant with verbose flag
ant -v ...
```

### Check Intermediate Files
```bash
# Examine intermediate-support-files/ directory
ls target/UBL-2.5-csd01-debug/intermediate-support-files/
```

### Validate Configuration
```bash
# Check XML configuration validity
xmllint --noout config-UBL.xml
xmllint --noout UBL.xml
```

### Test Individual Components
```bash
# Test genericode conversion
java -jar utilities/saxon9he/saxon9he.jar \
  -xsl:utilities/Crane-gc2obdndr/gc2obdndr.xsl \
  -s:UBL-Entities-2.5.gc
```

## References

- **OASIS UBL TC**: https://www.oasis-open.org/committees/ubl/
- **Crane Softwrights**: https://github.com/CraneSoftwrights/
- **DocBook**: https://docbook.org/
- **Saxon XSLT**: http://www.saxonica.com/
- **Genericode**: OASIS Code List Representation (Genericode) Version 1.0
