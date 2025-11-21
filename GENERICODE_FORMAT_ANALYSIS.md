# GeneriCode (GC) Format Analysis

**Status**: Complete
**Date**: 2025-11-21
**Priority**: High (needed for export functionality)

## Executive Summary

This document provides a comprehensive analysis of the GeneriCode (GC) XML format used in the UBL publishing pipeline. It answers all key questions about the format structure, transformation process, and feasibility of direct generation.

## Table of Contents

1. [What is GeneriCode?](#what-is-genericode)
2. [GC XML Structure](#gc-xml-structure)
3. [The Three Sheets](#the-three-sheets)
4. [ODS to GC Transformation](#ods-to-gc-transformation)
5. [Role of ident-UBL.xml](#role-of-ident-ublxml)
6. [Direct GC Generation Feasibility](#direct-gc-generation-feasibility)
7. [Implementation Recommendations](#implementation-recommendations)

---

## What is GeneriCode?

GeneriCode is an OASIS standard XML format for representing code lists and structured business entity vocabularies. In the UBL context, it serves as:

- **Vocabulary Storage Format**: The canonical representation of all UBL business entities (ABIEs, BBIEs, ASBIEs)
- **Schema Generation Input**: The source data for generating XSD, JSON schemas, and documentation
- **Version Control**: Snapshot format for tracking vocabulary changes between releases

**Specification**: http://docs.oasis-open.org/codelist/genericode

**Example Files**:
- `UBL-Entities-2.5-csd01.gc` (main entities)
- `UBL-Signature-Entities-2.5-csd01.gc` (signature entities)

---

## GC XML Structure

### Root Element and Namespace

```xml
<gc:CodeList xmlns:gc="http://docs.oasis-open.org/codelist/ns/genericode/1.0/">
```

### Complete Structure Hierarchy

```
gc:CodeList
├── Identification           # Metadata about the code list
│   ├── ShortName           # e.g., "UBL-2.5-CSD01"
│   ├── LongName            # e.g., "UBL 2.5 CSD01 Business Entity Summary"
│   ├── Version             # e.g., "2.5"
│   ├── CanonicalUri        # URN identifier
│   ├── CanonicalVersionUri # Version-specific URN
│   ├── LocationUri         # Official file location
│   └── Agency              # OASIS UBL details
│       ├── LongName        # "OASIS Universal Business Language"
│       └── Identifier      # "UBL"
│
├── ColumnSet                # Column definitions (metadata schema)
│   └── Column (×26)        # One for each data field
│       ├── Id              # Column identifier
│       ├── ShortName       # Short display name
│       ├── LongName        # Full display name
│       ├── Data[@Type]     # Data type (string)
│       └── @Use            # "required" or "optional"
│
├── SimpleCodeList           # The actual data rows
│   └── Row (×1000s)        # One per entity/property
│       └── Value[@ColumnRef] (×26) # One per column
│           └── SimpleValue # The actual data value
│
└── Key                      # Uniqueness constraint
    ├── @Id="key"
    └── ColumnRef[@Ref="DictionaryEntryName"]
```

### Column Definitions (26 Columns)

All columns have `Data Type="string"`. Here are the complete column definitions:

| # | Id | ShortName | LongName | Use |
|---|---|---|---|---|
| 1 | ModelName | ModelName | Model Name | required |
| 2 | ComponentName | ComponentName | Component Name | optional |
| 3 | Subset | Subset | Subset | optional |
| 4 | Cardinality | Cardinality | Cardinality | optional |
| 5 | EndorsedCardinality | EndorsedCardinality | Endorsed Cardinality | optional |
| 6 | EndorsedCardinalityRationale | EndorsedCardinalityRationale | Endorsed Cardinality Rationale | optional |
| 7 | Definition | Definition | Definition | optional |
| 8 | DeprecatedDefinition | DeprecatedDefinition | Deprecated Definition | optional |
| 9 | AlternativeBusinessTerms | AlternativeBusinessTerms | Alternative Business Terms | optional |
| 10 | Examples | Examples | Examples | optional |
| 11 | DictionaryEntryName | DictionaryEntryName | Dictionary Entry Name | required |
| 12 | ObjectClassQualifier | ObjectClassQualifier | Object Class Qualifier | optional |
| 13 | ObjectClass | ObjectClass | Object Class | optional |
| 14 | PropertyTermQualifier | PropertyTermQualifier | Property Term Qualifier | optional |
| 15 | PropertyTermPossessiveNoun | PropertyTermPossessiveNoun | Property Term Possessive Noun | optional |
| 16 | PropertyTermPrimaryNoun | PropertyTermPrimaryNoun | Property Term Primary Noun | optional |
| 17 | PropertyTerm | PropertyTerm | Property Term | optional |
| 18 | RepresentationTerm | RepresentationTerm | Representation Term | optional |
| 19 | DataTypeQualifier | DataTypeQualifier | Data Type Qualifier | optional |
| 20 | DataType | DataType | Data Type | optional |
| 21 | AssociatedObjectClassQualifier | AssociatedObjectClassQualifier | Associated Object Class Qualifier | optional |
| 22 | AssociatedObjectClass | AssociatedObjectClass | Associated Object Class | optional |
| 23 | ComponentType | ComponentType | Component Type | optional |
| 24 | UNTDEDCode | UNTDEDCode | UN/TDED Code | optional |
| 25 | CurrentVersion | CurrentVersion | Current Version | optional |
| 26 | LastChanged | LastChanged | Last Changed | optional |

### Component Types

The `ComponentType` column identifies the type of entity:

- **ABIE**: Aggregate Business Information Entity (e.g., "Address", "Party")
- **BBIE**: Basic Business Information Entity (e.g., "Identifier", "Amount")
- **ASBIE**: Association Business Information Entity (links to other ABIEs)

### Sample Row Structure

**Example 1 - ABIE (Aggregate Entity)**:
```xml
<Row>
  <Value ColumnRef="ModelName"><SimpleValue>UBL-CommonLibrary-2.5</SimpleValue></Value>
  <Value ColumnRef="ComponentName"><SimpleValue>ActivityDataLine</SimpleValue></Value>
  <Value ColumnRef="Definition"><SimpleValue>A class to associate a time period and locations...</SimpleValue></Value>
  <Value ColumnRef="DictionaryEntryName"><SimpleValue>Activity Data Line. Details</SimpleValue></Value>
  <Value ColumnRef="ObjectClass"><SimpleValue>Activity Data Line</SimpleValue></Value>
  <Value ColumnRef="ComponentType"><SimpleValue>ABIE</SimpleValue></Value>
  <Value ColumnRef="CurrentVersion"><SimpleValue>2.1</SimpleValue></Value>
</Row>
```

**Example 2 - BBIE (Basic Property)**:
```xml
<Row>
  <Value ColumnRef="ModelName"><SimpleValue>UBL-CommonLibrary-2.5</SimpleValue></Value>
  <Value ColumnRef="ComponentName"><SimpleValue>ID</SimpleValue></Value>
  <Value ColumnRef="Cardinality"><SimpleValue>1</SimpleValue></Value>
  <Value ColumnRef="Definition"><SimpleValue>An identifier for this activity data line.</SimpleValue></Value>
  <Value ColumnRef="DictionaryEntryName"><SimpleValue>Activity Data Line. Identifier</SimpleValue></Value>
  <Value ColumnRef="ObjectClass"><SimpleValue>Activity Data Line</SimpleValue></Value>
  <Value ColumnRef="PropertyTerm"><SimpleValue>Identifier</SimpleValue></Value>
  <Value ColumnRef="RepresentationTerm"><SimpleValue>Identifier</SimpleValue></Value>
  <Value ColumnRef="DataType"><SimpleValue>Identifier. Type</SimpleValue></Value>
  <Value ColumnRef="ComponentType"><SimpleValue>BBIE</SimpleValue></Value>
  <Value ColumnRef="CurrentVersion"><SimpleValue>2.1</SimpleValue></Value>
</Row>
```

---

## The Three Sheets

The UBL publishing pipeline uses **three separate Google Sheets** (not three tabs in one sheet):

### 1. Library Spreadsheet
- **URL Parameter**: `libraryGoogle`
- **Current URL**: `https://docs.google.com/spreadsheets/d/18o1YqjHWUw0-s8mb3ja4i99obOUhs-4zpgso6RZrGaY`
- **Downloaded as**: `UBL-Library-Google.ods`
- **Contains**: Common library entities (reusable components like Address, Party, etc.)
- **Example Worksheet Names**: `UBL-CommonLibrary-2.5`, etc.

### 2. Documents Spreadsheet
- **URL Parameter**: `documentsGoogle`
- **Current URL**: `https://docs.google.com/spreadsheets/d/1024Th-Uj8cqliNEJc-3pDOR7DxAAW7gCG4e-pbtarsg`
- **Downloaded as**: `UBL-Documents-Google.ods`
- **Contains**: Document-specific entities (Invoice, Order, etc.)
- **Example Worksheet Names**: `UBL-Invoice-2.5`, `UBL-Order-2.5`, etc.

### 3. Signature Spreadsheet
- **URL Parameter**: `signatureGoogle`
- **Current URL**: `https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g`
- **Downloaded as**: `UBL-Signature-Google.ods`
- **Contains**: Digital signature entities
- **Example Worksheet Names**: Signature-related components

### Mapping to GeneriCode Files

**Transformation 1**: Library + Documents → Main Entities
```
UBL-Library-Google.ods + UBL-Documents-Google.ods
  → [XSLT Transformation]
  → UBL-Entities-2.5.gc
```

**Transformation 2**: Signature → Signature Entities
```
UBL-Signature-Google.ods
  → [XSLT Transformation]
  → UBL-Signature-Entities-2.5.gc
```

### ODS Spreadsheet Structure

Each ODS file contains multiple worksheets (tabs). Each worksheet represents a **model** and has:

**Row 1**: Column headers (must match the 26 GC columns exactly)
- ModelName, ComponentName, Subset, Cardinality, etc.

**Rows 2+**: Data rows (one per entity/property)
- Empty rows are ignored
- Rows are processed until either:
  - End of sheet
  - A row whose concatenated content equals "END"

**Worksheet Naming**:
- Worksheet tab name becomes the default `ModelName` value for rows in that sheet
- Google Docs has a 31-character limit for worksheet names (workaround via `massageModelName.xml`)

---

## ODS to GC Transformation

### Transformation Tool

**XSLT Stylesheet**: `utilities/Crane-ods2obdgc/Crane-ods2obdgc.xsl`

This is a Crane Softwrights utility that converts ODS (OpenDocument Spreadsheet) format to GeneriCode format following OASIS Business Document Naming and Design Rules (OBD NDR).

### Build Process (from build.xml)

#### Step 1: Download ODS Files from Google Sheets

```xml
<!-- Download Library spreadsheet -->
<exec executable="wget">
  <arg value="--no-check-certificate"/>
  <arg value="-O"/><arg value="${dir}/UBL-Library-Google.ods"/>
  <arg value="${libraryGoogle}/export?format=ods"/>
</exec>

<!-- Download Documents spreadsheet -->
<exec executable="wget">
  <arg value="--no-check-certificate"/>
  <arg value="-O"/><arg value="${dir}/UBL-Documents-Google.ods"/>
  <arg value="${documentsGoogle}/export?format=ods"/>
</exec>

<!-- Download Signature spreadsheet -->
<exec executable="wget">
  <arg value="--no-check-certificate"/>
  <arg value="-O"/><arg value="${dir}/UBL-Signature-Google.ods"/>
  <arg value="${signatureGoogle}/export?format=ods"/>
</exec>
```

#### Step 2: Transform ODS to GeneriCode

**For Main Entities** (combines Library + Documents):
```xml
<antcallback target="-ods2gc" return="returnGC">
  <param name="source"
    value="${dir}/UBL-Library-Google.ods,${dir}/UBL-Documents-Google.ods"/>
  <param name="target"
    value="${dir}/UBL-Entities-${UBLversion}.gc"/>
  <param name="identification-uri"
    value="${ident-uri}"/>
  <param name="lengthen-model-name-uri"
    value="${lengthen-uri}"/>
</antcallback>
```

**For Signature Entities**:
```xml
<antcallback target="-ods2gc" return="returnGCsig">
  <param name="source"
    value="${dir}/UBL-Signature-Google.ods"/>
  <param name="target"
    value="${dir}/UBL-Signature-Entities-${UBLversion}.gc"/>
  <param name="identification-uri"
    value="${ident-uri-sig}"/>
  <param name="lengthen-model-name-uri"
    value="${lengthen-uri}"/>
</antcallback>
```

### Transformation Parameters

#### Required Parameters

1. **`source`**: Comma-separated list of ODS file paths
   - Can be ODS binary files or ODS XML content files
   - Multiple files are amalgamated into a single output

2. **`target`**: Output GeneriCode file path
   - Result is a well-formed GC XML file

3. **`identification-uri`**: Path to identification metadata XML file
   - Points to `ident-UBL.xml` or `ident-UBL-Signature.xml`
   - Provides the `<Identification>` metadata for the GC file

#### Optional Parameters

4. **`lengthen-model-name-uri`**: Path to model name massage rules
   - Points to `massageModelName.xml`
   - Reverses worksheet name shortening (Google Docs 31-char limit workaround)
   - Contains regex find/replace rules

5. **`row-number-column-name`**: Add row numbers as a column
   - If specified, adds row number to each GC row

6. **`indent`**: Control output formatting (default: "yes")

7. **`raw-sheet-long-name`**: Raw output mode
   - All columns become optional
   - No key fields
   - Sheet name stored in specified column

8. **`included-sheet-name-regex`**: Filter worksheets
   - Only worksheets matching regex are processed
   - Default: all worksheets

### Transformation Logic

The XSLT transformation:

1. **Reads ODS Structure**:
   - Parses ODF 1.1 XML (table:table, table:table-row, table:table-cell)
   - Extracts worksheet names
   - Reads cell values

2. **Applies Name Massaging**:
   - Uses regex rules from `massageModelName.xml`
   - Expands truncated worksheet names back to full model names

3. **Generates Column Definitions**:
   - Creates `<ColumnSet>` with column definitions
   - Determines required vs. optional based on data presence
   - Sets data types (all strings for UBL)

4. **Generates Rows**:
   - Creates `<Row>` elements for each spreadsheet row
   - Maps spreadsheet columns to GC `<Value>` elements
   - Stops at empty rows or "END" marker

5. **Adds Identification**:
   - Inserts `<Identification>` metadata from `identification-uri`
   - If not provided, uses default metadata

6. **Adds Key Constraint**:
   - Creates unique key on `DictionaryEntryName` column

### Example massageModelName.xml

This file works around the Google Docs worksheet name truncation bug:

```xml
<modelNameMassage>
  <pass>
    <shorten find="UBL-(.+)-2.5" replace="$1"/>
    <lengthen find="(.+)" replace="UBL-$1-2.5"/>
  </pass>
  <pass>
    <shorten find="Catalogue" replace="Ctlg"/>
    <lengthen find="Ctlg" replace="Catalogue"/>
  </pass>
  <pass>
    <shorten find="Transport([^a])" replace="Txp$1"/>
    <lengthen find="Txp" replace="Transport"/>
  </pass>
</modelNameMassage>
```

Rules are applied in document order for shortening, reverse order for lengthening.

---

## Role of ident-UBL.xml

### Purpose

`ident-UBL.xml` provides the **Identification metadata** that appears in the GC file's `<Identification>` element. It does NOT control the ODS-to-GC conversion logic.

### File Location and Variants

- **Main entities**: `ident-UBL.xml`
- **Signature entities**: `ident-UBL-Signature.xml`
- **Endorsed entities**: `ident-UBL-Endorsed.xml`

### Structure

```xml
<Identification>
  <ShortName>UBL-2.5-CSD02</ShortName>
  <LongName>UBL 2.5 CSD02 Business Entity Summary</LongName>
  <Version>2.5</Version>
  <CanonicalUri>urn:oasis:names:specification:ubl:BIE</CanonicalUri>
  <CanonicalVersionUri>urn:oasis:names:specification:ubl:BIE:2.5</CanonicalVersionUri>
  <LocationUri>http://docs.oasis-open.org/ubl/csd02-UBL-2.5/gc/UBL-Entities-2.5.gc</LocationUri>
  <Agency>
    <LongName>OASIS Universal Business Language</LongName>
    <Identifier>UBL</Identifier>
  </Agency>
</Identification>
```

### Configuration Requirements

When creating a new UBL version or stage, you must update:

1. **`ident-UBL.xml`**: Update ShortName, LongName, Version, URIs
2. **`ident-UBL-Signature.xml`**: Same updates for signature entities
3. **`ident-UBL-Endorsed.xml`**: Same updates for endorsed entities

### Relationship to config-UBL.xml

`config-UBL.xml` is **different** from `ident-UBL.xml`:

- **`ident-UBL.xml`**: Metadata for the GeneriCode file itself
- **`config-UBL.xml`**: Configuration for XSD/JSON schema generation from the GC file

---

## Direct GC Generation Feasibility

### Question: Can we generate GC directly, bypassing ODS?

**Answer: YES, it is completely feasible.**

### Why Direct Generation is Possible

1. **Simple XML Structure**:
   - GeneriCode has a straightforward, well-documented schema
   - Only 26 columns, all string-typed
   - Flat row structure (no complex nesting)

2. **No ODS-Specific Processing**:
   - The XSLT transformation is primarily a format conversion
   - No complex business logic or calculations
   - Main work is: read cells → write GC rows

3. **Standard Libraries Available**:
   - Python: `lxml` for XML generation
   - Any language with XML support can generate GC

4. **Existing Schema**:
   - GeneriCode XSD available: `utilities/genericode/xsd/genericode.xsd`
   - Can validate generated output

### Advantages of Direct Generation

✅ **Eliminates ODS Dependency**:
- No need for Google Sheets export
- No ODS parsing complexity
- No Google Docs worksheet name length limits

✅ **Better Version Control**:
- Direct generation from database/internal format
- Cleaner diffs in git
- No binary ODS files

✅ **Programmatic Control**:
- Validate data before generation
- Apply business rules consistently
- Generate multiple GC files from same source

✅ **Integration with Website**:
- Export directly from web app database
- No intermediate spreadsheet step
- Consistent with UBL publishing pipeline

### Implementation Considerations

#### 1. Data Source
You need access to the structured data containing:
- All 26 column values for each entity
- Hierarchical relationships (ABIE → BBIE/ASBIE)
- Model names (worksheet equivalents)

#### 2. Column Mapping
Must maintain exact column definitions:
- All 26 columns with correct IDs
- Correct Use (required vs. optional)
- Consistent data types

#### 3. Key Constraint
`DictionaryEntryName` must be unique across all rows.

#### 4. Identification Metadata
Must provide or generate the `<Identification>` section.

### Recommended Approach

**For UBL Website Export**:

1. **Store Data Internally**:
   - Keep entity data in your web application's database
   - Structure it to match the 26 GC columns

2. **Generate GC on Export**:
   ```python
   def export_to_genericode(entities, identification_metadata):
       gc = create_gc_root()
       add_identification(gc, identification_metadata)
       add_column_set(gc, COLUMN_DEFINITIONS)
       add_simple_code_list(gc, entities)
       add_key_constraint(gc)
       return serialize_xml(gc)
   ```

3. **Validate Output**:
   - Validate against GeneriCode XSD
   - Check key uniqueness
   - Verify required columns populated

4. **Integration Testing**:
   - Pass generated GC through `Crane-gc2obdndr.xsl`
   - Verify XSD schema generation works
   - Compare with reference GC files

---

## Implementation Recommendations

### For Website GC Export Feature

#### Phase 1: Research and Analysis ✅ (Complete)
- [x] Understand GC format structure
- [x] Analyze ODS to GC transformation
- [x] Identify the three sheets and their mapping
- [x] Document ident-UBL.xml role

#### Phase 2: Design Export Architecture
- [ ] Define internal data model mapping to 26 GC columns
- [ ] Design identification metadata configuration
- [ ] Plan validation strategy
- [ ] Choose XML generation library (recommendation: `lxml` for Python)

#### Phase 3: Implement GC Generator
- [ ] Create GeneriCode XML generator module
- [ ] Implement column definitions
- [ ] Implement row generation from internal data
- [ ] Add identification metadata support
- [ ] Add key constraint generation

#### Phase 4: Validation and Testing
- [ ] Validate against GeneriCode XSD schema
- [ ] Test with Crane GC-to-XSD tools
- [ ] Compare output with reference GC files
- [ ] Test with various entity configurations

#### Phase 5: Integration
- [ ] Add export endpoint to web application
- [ ] Implement download functionality
- [ ] Add user documentation
- [ ] Test with real UBL data

### Python Implementation Skeleton

```python
from lxml import etree

GC_NS = "http://docs.oasis-open.org/codelist/ns/genericode/1.0/"
GC = "{%s}" % GC_NS

COLUMN_DEFINITIONS = [
    ("ModelName", "Model Name", "required"),
    ("ComponentName", "Component Name", "optional"),
    ("Subset", "Subset", "optional"),
    # ... all 26 columns
]

def generate_genericode(entities, identification):
    """Generate GeneriCode XML from entity data."""

    nsmap = {'gc': GC_NS}
    root = etree.Element(GC + "CodeList", nsmap=nsmap)

    # Add Identification
    ident_elem = etree.SubElement(root, GC + "Identification")
    add_identification_elements(ident_elem, identification)

    # Add ColumnSet
    colset = etree.SubElement(root, GC + "ColumnSet")
    for col_id, long_name, use in COLUMN_DEFINITIONS:
        add_column_definition(colset, col_id, long_name, use)

    # Add SimpleCodeList
    codelist = etree.SubElement(root, GC + "SimpleCodeList")
    for entity in entities:
        add_row(codelist, entity)

    # Add Key
    key = etree.SubElement(root, GC + "Key", Id="key")
    etree.SubElement(key, GC + "ColumnRef", Ref="DictionaryEntryName")

    return etree.tostring(root, pretty_print=True,
                         xml_declaration=True, encoding='UTF-8')

def add_column_definition(parent, col_id, long_name, use):
    """Add a column definition."""
    col = etree.SubElement(parent, GC + "Column", Id=col_id, Use=use)
    sn = etree.SubElement(col, GC + "ShortName")
    sn.text = col_id
    ln = etree.SubElement(col, GC + "LongName")
    ln.text = long_name
    dt = etree.SubElement(col, GC + "Data", Type="string")

def add_row(parent, entity):
    """Add a data row."""
    row = etree.SubElement(parent, GC + "Row")
    for col_id, long_name, _ in COLUMN_DEFINITIONS:
        value_elem = etree.SubElement(row, GC + "Value",
                                     ColumnRef=col_id)
        simple = etree.SubElement(value_elem, GC + "SimpleValue")
        simple.text = entity.get(col_id, "")
    return row
```

### Testing Strategy

1. **Unit Tests**:
   - Test column definition generation
   - Test row generation
   - Test identification metadata
   - Test key constraint

2. **Integration Tests**:
   - Generate sample GC file
   - Validate against GeneriCode XSD
   - Pass through Crane tooling
   - Compare with reference files

3. **Validation Tools**:
   - Use `xmllint` with GeneriCode XSD
   - Use `Crane-gc2obdndr.xsl` to generate XSD
   - Use `Crane-checkgc4obdndr.xsl` to validate GC

### Reference Files for Testing

Use these as reference/test fixtures:
- `/home/user/ubl/UBL-Entities-2.5-csd01.gc`
- `/home/user/ubl/UBL-Signature-Entities-2.5-csd01.gc`
- `/home/user/ubl/UBL-Entities-2.4-os.gc`

### Validation Command Examples

```bash
# Validate GeneriCode XML structure
xmllint --noout --schema utilities/genericode/xsd/genericode.xsd output.gc

# Test GC to XSD transformation
java -jar utilities/saxon9he/saxon9he.jar \
  -s:output.gc \
  -xsl:utilities/Crane-gc2obdndr/Crane-gc2obdndr.xsl \
  -o:test-output/ \
  config-uri=config-UBL.xml

# Check GC compliance with OBD NDR
java -jar utilities/saxon9he/saxon9he.jar \
  -s:output.gc \
  -xsl:utilities/Crane-gc2obdndr/Crane-checkgc4obdndr.xsl \
  -o:check-report.html
```

---

## Additional Resources

### Key Files in Repository

- **XSLT Tools**:
  - `utilities/Crane-ods2obdgc/Crane-ods2obdgc.xsl` - ODS to GC transformation
  - `utilities/Crane-gc2odsxml/Crane-gc2odsxml.xsl` - GC to ODS XML (reverse)
  - `utilities/Crane-gc2obdndr/Crane-gc2obdndr.xsl` - GC to XSD/JSON schemas

- **Configuration**:
  - `ident-UBL.xml` - Main entities identification
  - `ident-UBL-Signature.xml` - Signature entities identification
  - `config-UBL.xml` - Schema generation configuration
  - `massageModelName.xml` - Worksheet name massage rules

- **Build Process**:
  - `build.xml` - Ant build file
  - `build.py` - Python build script
  - `build.sh` - Shell script wrapper

- **Examples**:
  - `UBL-Entities-2.5-csd01.gc` - Example main entities
  - `UBL-Signature-Entities-2.5-csd01.gc` - Example signature entities
  - `raw/cl/gc/default/*.gc` - Code list examples

### External Documentation

- GeneriCode Specification: http://docs.oasis-open.org/codelist/genericode
- Crane Softwrights GC Toolkit: http://www.CraneSoftwrights.com/links/training-gctk.htm
- UBL TC Repository: https://github.com/oasis-tcs/ubl

### CCTS Terminology

- **CCTS**: Core Component Technical Specification (UN/CEFACT standard)
- **ABIE**: Aggregate Business Information Entity (complex types)
- **BBIE**: Basic Business Information Entity (simple types)
- **ASBIE**: Association Business Information Entity (references)
- **DEN**: Dictionary Entry Name (unique identifier)

---

## Conclusion

### Key Findings

1. ✅ **GC XML Structure is Well-Defined**:
   - Standard OASIS format with clear schema
   - Simple tabular structure (26 columns × N rows)
   - Well-documented with available XSD

2. ✅ **Three Sheets Identified**:
   - Library spreadsheet (common entities)
   - Documents spreadsheet (document-specific entities)
   - Signature spreadsheet (signature entities)
   - Combined via XSLT into two GC files

3. ✅ **Transformation Process Understood**:
   - Download Google Sheets as ODS
   - Apply XSLT transformation (`Crane-ods2obdgc.xsl`)
   - Insert identification metadata from `ident-UBL.xml`
   - Apply name massaging rules
   - Generate GC XML output

4. ✅ **ident-UBL.xml Role Clarified**:
   - Provides `<Identification>` metadata only
   - Does not control conversion logic
   - Must be updated for each version/stage

5. ✅ **Direct GC Generation is Feasible**:
   - No dependency on ODS format required
   - Can generate directly from any structured data source
   - Simpler and more maintainable than ODS roundtrip
   - Recommended approach for website export

### Next Steps

1. **Design Export Data Model**:
   - Map website's internal data to 26 GC columns
   - Define how to handle model names (worksheets)

2. **Implement GC Generator**:
   - Use Python with `lxml` or similar
   - Follow structure documented in this analysis

3. **Validate Output**:
   - Test against GeneriCode XSD
   - Verify with Crane tooling
   - Compare with reference files

4. **Integrate with Website**:
   - Add export endpoint
   - Provide download functionality
   - Document for users

---

**Document Version**: 1.0
**Last Updated**: 2025-11-21
**Author**: Analysis based on UBL repository research
**Status**: Complete and Ready for Implementation
