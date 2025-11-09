# ODS to Genericode (ods2gc) Transformation Analysis

## Executive Summary

The `ods2gc` target in the UBL build system converts OpenDocument Spreadsheet (ODS) files into OASIS Genericode 1.0 XML format. This transformation is critical for processing CCTS (Core Component Technical Specification) information used to generate UBL schemas.

## Table of Contents

1. [Overview](#overview)
2. [Build Target Details](#build-target-details)
3. [XSLT Stylesheet Architecture](#xslt-stylesheet-architecture)
4. [ODS File Structure](#ods-file-structure)
5. [Transformation Process](#transformation-process)
6. [Python Implementation Guide](#python-implementation-guide)

---

## Overview

### Purpose
The transformation converts structured metadata in ODS spreadsheets into Genericode XML format, which is then used downstream to generate XSD schemas and documentation for the UBL standard.

### Key Files
- **Build Target**: `build.xml` (line 946: target `-ods2gc`)
- **Main Stylesheet**: `utilities/Crane-ods2obdgc/Crane-ods2obdgc.xsl`
- **Support Stylesheet**: `utilities/Crane-ods2obdgc/support/gcExportSubset.xsl`
- **Common Functions**: `utilities/Crane-ods2obdgc/support/odsCommon.xsl`

---

## Build Target Details

### Ant Target: `-ods2gc`

**Location**: `build.xml:946`

**Purpose**: Rebuilds Genericode (.gc) files from ODS source files.

### Invocation Examples

The target is called multiple times in the build process:

#### 1. UBL Signature Entities (line 267)
```xml
<antcallback target="-ods2gc" return="returnGCsig">
  <param name="okay" value="gc-sig-okay"/>
  <param name="source" value="${dir}/UBL-Signature-Google.ods"/>
  <param name="target" value="${dir}/UBL-Signature-Entities-${UBLversion}.gc"/>
  <param name="identification-uri" value="${ident-uri-sig}"/>
  <param name="lengthen-model-name-uri" value="${lengthen-uri}"/>
  <param name="returnProperty" value="returnGCsig"/>
</antcallback>
```

#### 2. UBL Base Entities (line 347)
```xml
<antcallback target="-ods2gc" return="returnGC">
  <param name="okay" value="gc-okay"/>
  <param name="source" value="${dir}/UBL-Library-Google.ods,${dir}/UBL-Documents-Google.ods"/>
  <param name="target" value="${dir}/UBL-Entities-${UBLversion}.gc"/>
  <param name="identification-uri" value="${ident-uri}"/>
  <param name="lengthen-model-name-uri" value="${lengthen-uri}"/>
  <param name="returnProperty" value="returnGC"/>
</antcallback>
```

#### 3. UBL Endorsed Entities (line 373)
```xml
<antcallback target="-ods2gc" return="returnGCE">
  <param name="okay" value="gc-okay"/>
  <param name="source" value="${dir}/UBL-Library-Google.ods,${dir}/UBL-Documents-Google.ods"/>
  <param name="target" value="${dir}/UBL-Endorsed-Entities-${UBLversion}-raw.gc"/>
  <param name="identification-uri" value="${ident-uri-endorsed}"/>
  <param name="lengthen-model-name-uri" value="${lengthen-uri}"/>
  <param name="returnProperty" value="returnGCE"/>
</antcallback>
```

### Saxon Command

The target executes Saxon XSLT processor:

```xml
<java append="true" jar="utilities/saxon9he/saxon9he.jar" fork="true">
  <arg value="-xsl:${utilitydir}Crane-ods2obdgc/Crane-ods2obdgc.xsl"/>
  <arg value="-o:${target}"/>
  <arg value="-it:ods-uri"/>
  <arg value="ods-uri=${source}"/>
  <arg value="identification-uri=${identification-uri}"/>
  <arg value="included-sheet-name-regex=^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*"/>
  <arg value="lengthen-model-name-uri=${lengthen-model-name-uri}"/>
</java>
```

### Parameters Explained

| Parameter | Purpose | Example Value |
|-----------|---------|---------------|
| `ods-uri` | Comma-separated list of ODS file paths | `UBL-Library-Google.ods,UBL-Documents-Google.ods` |
| `identification-uri` | XML file with metadata for output | `ident-UBL.xml` |
| `lengthen-model-name-uri` | XML file with model name transformation rules | `massageModelName.xml` |
| `included-sheet-name-regex` | Regex to filter which sheets to process | `^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*` |

**Sheet Name Regex Explanation**:
The regex `^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*` excludes sheets starting with "Log" or "log" (case-insensitive for the first letter) but includes all other sheets.

---

## XSLT Stylesheet Architecture

### Main Stylesheet: `Crane-ods2obdgc.xsl`

**Namespace Declarations**:
```xml
xmlns:gc="http://docs.oasis-open.org/codelist/ns/genericode/1.0/"
xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"
```

### Key Functions and Templates

#### 1. ODS File Access (lines 102-106)
```xslt
<xsl:function name="c:ods-uri">
  <xsl:param name="c:ods-uri" as="xsd:string?"/>
  <xsl:variable name="c:ods-uri" select="translate($c:ods-uri,'\','/')"/>
  <xsl:sequence select="concat('jar:file:',$c:ods-uri,'!/content.xml')"/>
</xsl:function>
```
**Purpose**: Converts file path to JAR URI format to access `content.xml` inside ODS (which is a ZIP file).

#### 2. Column Metadata Extraction (lines 233-248)
```xslt
<xsl:variable name="c:columnMetadata" as="element(Column)*">
  <xsl:for-each-group group-by="normalize-space(string-join(text:p,' '))"
    select="($c:tables//table:table-row)[1]/table:table-cell[normalize-space(.)]">
    <xsl:variable name="c:longName" select="normalize-space(current-grouping-key())"/>
    <xsl:variable name="c:shortName" select="replace($c:longName,'\W+','')"/>
    <Column Id="{$c:shortName}"
            Use="{if( $c:shortName = 'DictionaryEntryName' and
                      empty( $raw-sheet-long-name ) )
                  then 'required' else 'optional'}">
      <ShortName><xsl:value-of select="$c:shortName"/></ShortName>
      <LongName><xsl:value-of select="$c:longName"/></LongName>
      <Data Type="string"/>
    </Column>
  </xsl:for-each-group>
</xsl:variable>
```

**Logic**:
- Reads first row of each table
- Groups cells by their text content
- Creates column metadata from unique column headers
- Generates `ShortName` by removing non-word characters from `LongName`
- `DictionaryEntryName` is marked as `required`, all others as `optional`

#### 3. Column Set Generation (lines 274-311)

The transformation creates three column structures:

**Standard Mode** (when `raw-sheet-long-name` is empty):
```xml
<ColumnSet>
  <Column Id="ModelName" Use="required">
    <ShortName>ModelName</ShortName>
    <LongName>Model Name</LongName>
    <Data Type="string"/>
  </Column>
  <!-- Optional row number column -->
  <Column Id="{$row-number-column-name}" Use="required">
    <Data Type="integer"/>
  </Column>
  <!-- User-defined columns from spreadsheet -->
  <Key Id="key">
    <ShortName>Key</ShortName>
    <ColumnRef Ref="DictionaryEntryName"/>
  </Key>
</ColumnSet>
```

**Raw Mode** (when `raw-sheet-long-name` has a value):
```xml
<ColumnSet>
  <Column Id="{$worksheetIdentifier}" Use="optional">
    <ShortName>{$worksheetIdentifier}</ShortName>
    <LongName>{$raw-sheet-long-name}</LongName>
    <Data Type="string"/>
  </Column>
  <!-- User-defined columns -->
</ColumnSet>
```

#### 4. Identification Metadata (lines 340-373)

```xslt
<xsl:template name="c:Identification">
  <xsl:choose>
    <xsl:when test="exists($identification-uri)">
      <xsl:copy-of select="doc($identification-uri)/Identification"/>
    </xsl:when>
    <xsl:otherwise>
      <Identification>
        <ShortName>OBDNDRSkeleton</ShortName>
        <LongName>OASIS Business Document NDR skeleton genericode file</LongName>
        <Version>1</Version>
        <CanonicalUri>urn:X-CraneSoftwrights.com</CanonicalUri>
        <CanonicalVersionUri>urn:X-CraneSoftwrights.com</CanonicalVersionUri>
      </Identification>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>
```

### Support Stylesheet: `gcExportSubset.xsl`

This included stylesheet handles row-by-row data extraction.

#### Model Name Lengthening (lines 213-235)

```xslt
<xsl:function name="c:lengthen">
  <xsl:param name="c:value" as="xsd:string?"/>
  <xsl:param name="c:pass" as="element(pass)?"/>
  <xsl:sequence select="if( $c:pass ) then c:lengthen(
        replace( $c:value, $c:pass/lengthen/@find, $c:pass/lengthen/@replace ),
                                           $c:pass/preceding-sibling::pass[1] )
                                      else $c:value"/>
</xsl:function>
```

**Purpose**: Applies regex transformations from `massageModelName.xml` to expand abbreviated sheet names.

**Example transformations** (from `massageModelName.xml`):
```xml
<pass>
  <shorten find="Catalogue" replace="Ctlg"/>
  <lengthen find="Ctlg" replace="Catalogue"/>
</pass>
<pass>
  <shorten find="Signature" replace="Sgnt"/>
  <lengthen find="Sgnt" replace="Signature"/>
</pass>
```

#### Row Data Emission (lines 134-200)

```xslt
<xsl:template name="c:emitGenericode">
  <xsl:param name="c:tables" as="element(table:table)*"/>
  <xsl:for-each select="$c:tables">
    <xsl:variable name="c:modelName" select="c:lengthen(@table:name)"/>
    <xsl:variable name="c:columnCount" select="..."/>
    <xsl:variable name="c:columnHeads" select="..."/>
    <xsl:variable name="c:lastTableRow"
                  select="( (.//table:table-row)[normalize-space(
                  string-join(table:table-cell/o:odsCell2Text(.),''))='END']/
                                    preceding::table:table-row[1],
                            (.//table:table-row)[last()] )[1]"/>
    <xsl:for-each select="(.//table:table-row)[position()>1]
                                         [ .    is    $c:lastTableRow or
                                           . &lt;&lt; $c:lastTableRow ]
                     [string-join(table:table-cell/o:odsCell2Text(.),'')!='']">
      <Row>
        <Value ColumnRef="{$worksheetIdentifier}">
          <SimpleValue><xsl:value-of select="$c:modelName"/></SimpleValue>
        </Value>
        <!-- Iterate through columns and emit values -->
      </Row>
    </xsl:for-each>
  </xsl:for-each>
</xsl:template>
```

**Key Logic**:
1. Find last data row (marked with "END" in any cell, or last row if no "END")
2. Skip first row (headers)
3. Process only non-empty rows
4. For each column, emit a `<Value>` element if the cell has content

### Common Functions: `odsCommon.xsl`

This stylesheet provides utility functions for working with ODS XML.

#### Column Number Conversion (lines 586-638)

```xslt
<xsl:function name="o:columnAlpha2Numeric">
  <xsl:param name="o:alpha" as="xsd:string"/>
  <xsl:analyze-string select="$o:alpha"
                      regex="\s*(([A-Z])?([A-Z]))?([A-Z])\s*">
    <xsl:matching-substring>
      <xsl:sequence select="o:alpha2ordinal(regex-group(2))*26*26 +
                            o:alpha2ordinal(regex-group(3))*26 +
                            o:alpha2ordinal(regex-group(4))"/>
    </xsl:matching-substring>
  </xsl:analyze-string>
</xsl:function>

<xsl:function name="o:columnNumeric2Alpha">
  <xsl:param name="o:numeric" as="xsd:integer"/>
  <xsl:variable name="o:first" select="( $o:numeric - 1 ) idiv (27*26)"/>
  <xsl:variable name="o:second"
                select="(($o:numeric - 1 + $o:first*26) mod (27*26) idiv 26)"/>
  <xsl:variable name="o:third" select="( $o:numeric - 1 ) mod 26 + 1 "/>
  <xsl:sequence
      select="concat( o:ordinal2alpha( $o:first ),
                      o:ordinal2alpha( $o:second ),
                      o:ordinal2alpha( $o:third ) )"/>
</xsl:function>
```

**Algorithm**:
- Converts between column letters (A, B, ..., Z, AA, AB, ...) and numbers (1, 2, ..., 26, 27, 28, ...)
- Based on Python algorithm provided in comments (lines 547-577)

#### Cell Position Calculation (lines 408-462)

```xslt
<xsl:function name="o:column" as="xsd:integer*">
  <xsl:param name="o:cell" as="node()"/>
  <!-- Complex logic to handle repeated columns and column spanning -->
  <xsl:variable name="o:start"
                select="count($o:prevCells) + 1
    + sum($o:prevCells/@table:number-columns-spanned)
    + sum($o:prevCells/@table:number-columns-repeated)
    + sum($o:prevRowSpans/(xsd:integer(@table:number-columns-repeated),1)[1])
    - count($o:prevCells[@table:number-columns-spanned])
    - count($o:prevCells[@table:number-columns-repeated])"/>
</xsl:function>
```

**Purpose**: Calculates actual column position accounting for:
- `table:number-columns-repeated` (when multiple columns are identical)
- `table:number-columns-spanned` (when a cell spans multiple columns)
- `table:covered-table-cell` (cells covered by spanning)

#### Cell Text Extraction (lines 170-200)

```xslt
<xsl:function name="o:odsCell2Text">
  <xsl:param name="o:cell" as="element(table:table-cell)?"/>
  <xsl:sequence select="string-join($o:cell/text:p/string(.),'&#xa;')"/>
</xsl:function>

<xsl:function name="o:odsColumn2Text">
  <xsl:param name="o:row" as="element(table:table-row)"/>
  <xsl:param name="o:column" as="xsd:decimal"/>
  <xsl:for-each select="$o:row/(table:table-cell|table:covered-table-cell)
                               [o:column(.) = $o:column]">
    <xsl:choose>
      <xsl:when test="self::table:covered-table-cell">
        <!-- Recursively get value from row above for spanned cells -->
        <xsl:sequence select="
    o:odsColumn2Text($o:row/preceding-sibling::table:table-row[1],$o:column)"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:sequence select="o:odsCell2Text(.)"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:for-each>
</xsl:function>
```

**Purpose**:
- Extract text from cells
- Handle cells that are covered by row-spanning cells above
- Join multiple `<text:p>` elements with newlines

---

## ODS File Structure

### Physical Structure

ODS files are ZIP archives containing:

```
ODS File (ZIP)
├── META-INF/
│   └── manifest.xml
├── content.xml          ← Main data (spreadsheet content)
├── meta.xml             ← Metadata
├── settings.xml         ← View settings
└── styles.xml           ← Style definitions
```

### Content.xml Structure

```xml
<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
                         xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"
                         xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
  <office:body>
    <office:spreadsheet>
      <table:table table:name="SheetName">
        <table:table-column table:style-name="..." />
        <table:table-row table:style-name="...">
          <table:table-cell office:value-type="string">
            <text:p>Cell Value</text:p>
          </table:table-cell>
        </table:table-row>
      </table:table>
    </office:spreadsheet>
  </office:body>
</office:document-content>
```

### Column Structure for UBL CCTS Model

Based on analysis of the "Empty CCTS Model.ods" file, the spreadsheet has **45 columns** (A through AS):

| # | Column Letter | Column Name | Purpose |
|---|---------------|-------------|---------|
| 1 | A | Component Name | Derived from Dictionary Entry Name |
| 2 | B | Subset MyProf 1 | Subset cardinality profile 1 |
| 3 | C | Subset MyProf 2 | Subset cardinality profile 2 |
| 4 | D | Subset Comment | Informal collaboration comments |
| 5 | E | Cardinality | Optionality and occurrence constraints |
| 6 | F | **Dictionary Entry Name** | **KEY COLUMN** - Unique identifier |
| 7 | G | Object Class Qualifier | Qualifiers for the object class |
| 8 | H | Object Class | The business object being modeled |
| 9 | I | Property Term Qualifier | Qualifiers for the property |
| 10 | J | Property Term Possessive Noun | Possessive noun part of property |
| 11 | K | Property Term Primary Noun | Primary noun of the property |
| 12 | L | Property Term | Complete property term |
| 13 | M | Representation Term | How the property is represented |
| 14 | N | Data Type Qualifier | Qualifiers for the data type |
| 15 | O | Data Type | The data type of the property |
| 16 | P | Associated Object Class Qualifier | Qualifier for associated object |
| 17 | Q | Associated Object Class | Related object class for associations |
| 18 | R | Alternative Business Terms | Synonyms or alternative names |
| 19 | S | Component Type | ABIE, BBIE, ASBIE, etc. |
| 20 | T | Definition | Formal definition |
| 21 | U | Examples | Example values |
| 22 | V | UN/TDED Code | UN Trade Data Elements Directory code |
| 23 | W | Current Version | Version information |
| 24 | X | Analyst Notes | Notes for analysts |
| 25 | Y | CCL Dictionary Entry Name | Core Component Library name |
| 26 | Z | Context: Business Process | Business process context |
| 27 | AA | Context: Region (Geopolitical) | Regional context |
| 28 | AB | Context: Official Constraints | Official constraint context |
| 29 | AC | Context: Product | Product context |
| 30 | AD | Context: Industry | Industry context |
| 31 | AE | Context: Role | Role context |
| 32 | AF | Context: Supporting Role | Supporting role context |
| 33 | AG | Context: System Constraint | System constraint context |
| 34 | AH | Editor's Notes | Editorial notes |
| 35 | AI | Changes from Previous Version | Version change notes |
| 36 | AJ | . Details | Additional details |
| 37 | AK | ABIE | Aggregate Business Information Entity marker |
| 38 | AL | ? | Unknown/unused |
| 39 | AM | . | Separator/unused |
| 40 | AN | . Type | Type information |
| 41 | AO | BBIE | Basic Business Information Entity marker |
| 42 | AP | ? | Unknown/unused |
| 43 | AQ | . | Separator/unused |
| 44 | AR | ASBIE | Association Business Information Entity marker |
| 45 | AS | END | Row termination marker |

### Important Column Notes

1. **Dictionary Entry Name** (Column F): This is the primary key column. In standard mode, this column is marked as `Use="required"` and is referenced in the `<Key>` element.

2. **Component Name** (Column A): Derived from Dictionary Entry Name and used as the human-readable name in schemas.

3. **Subset Columns** (B, C, D): Used when creating subsets/profiles of UBL. These columns may have different cardinality constraints than the base model.

4. **Context Columns** (Z-AG): Define the business context for which the component is applicable.

5. **END Marker** (Column AS): Special marker column. When the text "END" appears in any cell of a row, it signals the end of data processing for that sheet.

### Cell Value Structure

Individual cells can contain:

1. **Simple Text**:
```xml
<table:table-cell office:value-type="string">
  <text:p>Simple value</text:p>
</table:table-cell>
```

2. **Multi-line Text**:
```xml
<table:table-cell office:value-type="string">
  <text:p>First line</text:p>
  <text:p>Second line</text:p>
</table:table-cell>
```

3. **Empty Cells**:
```xml
<table:table-cell/>
```

4. **Repeated Cells**:
```xml
<table:table-cell table:number-columns-repeated="5"/>
```

5. **Spanned Cells**:
```xml
<table:table-cell table:number-columns-spanned="3">
  <text:p>Spanning value</text:p>
</table:table-cell>
<table:covered-table-cell table:number-columns-repeated="2"/>
```

6. **Cell with Annotations** (Comments):
```xml
<table:table-cell>
  <text:p>Cell value</text:p>
  <office:annotation>
    <text:p>Comment text</text:p>
  </office:annotation>
</table:table-cell>
```

---

## Transformation Process

### Step-by-Step Flow

1. **Input Processing**
   - Accept comma-separated ODS file paths via `ods-uri` parameter
   - Convert each path to JAR URI: `jar:file:/path/to/file.ods!/content.xml`
   - Load each file as an XML document

2. **Sheet Filtering**
   - Apply `included-sheet-name-regex` to filter sheets
   - Default regex excludes sheets named "Log" or "log"
   - Multiple sheets from multiple files are combined

3. **Column Discovery**
   - Read first row of each table
   - Extract text from each non-empty cell
   - Create unique column list by grouping identical headers
   - Generate `ShortName` by removing non-word characters (`\W+`)
   - Example: "Property Term Qualifier" → "PropertyTermQualifier"

4. **Column Metadata Creation**
   - Create `<Column>` elements for each discovered column
   - Mark `DictionaryEntryName` as `Use="required"` (standard mode only)
   - All other columns marked as `Use="optional"`
   - Add `ModelName` column (standard mode) or sheet name column (raw mode)
   - Optionally add row number column if `row-number-column-name` is set

5. **Identification Metadata**
   - Load metadata from `identification-uri` XML file
   - If not provided, use default placebo identification

6. **Row Processing**
   - Find last data row (row with "END" marker or last row in sheet)
   - Skip first row (headers)
   - Process only non-empty rows (rows where concatenated cell values ≠ '')
   - For each row:
     - Add `ModelName` value (expanded sheet name)
     - Add row number (if enabled)
     - Iterate through columns and emit `<Value>` for non-empty cells

7. **Model Name Expansion**
   - Apply transformations from `lengthen-model-name-uri`
   - Process in reverse document order (last pass to first)
   - Example: "Ctlg" → "Catalogue" → "UBL-Catalogue-2.5"

8. **Output Generation**
   - Create Genericode XML structure
   - Apply indentation if requested
   - Write to output file

### Example Transformation

**Input ODS Row** (Sheet: "Invoice"):
```
| DictionaryEntryName | ObjectClass | PropertyTerm | RepresentationTerm | Definition |
|---------------------|-------------|--------------|--------------------|-----------  |
| Invoice. Issue Date | Invoice     | Issue Date   | Date               | The date... |
```

**Output Genericode**:
```xml
<Row>
  <Value ColumnRef="ModelName">
    <SimpleValue>UBL-Invoice-2.5</SimpleValue>
  </Value>
  <Value ColumnRef="DictionaryEntryName">
    <SimpleValue>Invoice. Issue Date</SimpleValue>
  </Value>
  <Value ColumnRef="ObjectClass">
    <SimpleValue>Invoice</SimpleValue>
  </Value>
  <Value ColumnRef="PropertyTerm">
    <SimpleValue>Issue Date</SimpleValue>
  </Value>
  <Value ColumnRef="RepresentationTerm">
    <SimpleValue>Date</SimpleValue>
  </Value>
  <Value ColumnRef="Definition">
    <SimpleValue>The date...</SimpleValue>
  </Value>
</Row>
```

---

## Python Implementation Guide

This section provides detailed guidance for implementing the ODS to Genericode transformation in native Python.

### Required Libraries

```python
from zipfile import ZipFile
from xml.etree import ElementTree as ET
from typing import List, Dict, Optional, Tuple
import re
from pathlib import Path
```

### Core Classes

```python
class ODSReader:
    """Reads and parses ODS files"""

    ODS_NAMESPACES = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
    }

    def __init__(self, ods_path: str):
        self.ods_path = ods_path
        self.content_xml = None

    def load(self):
        """Extract content.xml from ODS ZIP file"""
        with ZipFile(self.ods_path, 'r') as zip_file:
            content_xml_bytes = zip_file.read('content.xml')
            self.content_xml = ET.fromstring(content_xml_bytes)
        return self

    def get_sheets(self, name_regex: str = None) -> List[ET.Element]:
        """Get all sheets, optionally filtered by regex"""
        xpath = './/table:table'
        tables = self.content_xml.findall(xpath, self.ODS_NAMESPACES)

        if name_regex:
            pattern = re.compile(name_regex)
            tables = [t for t in tables
                     if pattern.match(t.get(f'{{{self.ODS_NAMESPACES["table"]}}}name', ''))]

        return tables

    def get_sheet_name(self, sheet: ET.Element) -> str:
        """Extract sheet name from table element"""
        return sheet.get(f'{{{self.ODS_NAMESPACES["table"]}}}name', '')


class CellPosition:
    """Handles ODS cell position calculations"""

    @staticmethod
    def column_letter_to_number(letter: str) -> int:
        """
        Convert column letter (A, B, ..., Z, AA, AB, ...) to number (1, 2, ..., 26, 27, 28, ...)

        Algorithm based on odsCommon.xsl:586-608
        """
        letter = letter.strip().upper()
        match = re.match(r'\s*(([A-Z])?([A-Z]))?([A-Z])\s*', letter)
        if not match:
            raise ValueError(f"Invalid column letter: {letter}")

        groups = match.groups()
        first = groups[1] if groups[1] else ''
        second = groups[2] if groups[2] else ''
        third = groups[3]

        def alpha_to_ordinal(char: str) -> int:
            return 0 if not char else ord(char) - ord('A') + 1

        return (alpha_to_ordinal(first) * 26 * 26 +
                alpha_to_ordinal(second) * 26 +
                alpha_to_ordinal(third))

    @staticmethod
    def column_number_to_letter(num: int) -> str:
        """
        Convert column number to letter

        Algorithm based on odsCommon.xsl:616-638
        """
        first = (num - 1) // (27 * 26)
        second = ((num - 1 + first * 26) % (27 * 26)) // 26
        third = (num - 1) % 26 + 1

        def ordinal_to_alpha(ordinal: int) -> str:
            return '' if ordinal == 0 else chr(ordinal + ord('A') - 1)

        return ordinal_to_alpha(first) + ordinal_to_alpha(second) + ordinal_to_alpha(third)

    @staticmethod
    def calculate_column_position(cell: ET.Element, row: ET.Element,
                                   namespaces: dict) -> int:
        """
        Calculate actual column position accounting for repeated/spanned columns

        Based on odsCommon.xsl:408-462
        """
        # Get all preceding cells in the same row
        all_cells = list(row.findall('table:table-cell|table:covered-table-cell', namespaces))
        cell_index = all_cells.index(cell)
        prev_cells = all_cells[:cell_index]

        # Calculate position
        position = 1  # 1-based indexing

        for prev_cell in prev_cells:
            # Add 1 for the cell itself
            position += 1

            # Add extra for column spanning
            spanned = prev_cell.get(f'{{{namespaces["table"]}}}number-columns-spanned')
            if spanned:
                position += int(spanned) - 1

            # Add extra for column repetition
            repeated = prev_cell.get(f'{{{namespaces["table"]}}}number-columns-repeated')
            if repeated:
                position += int(repeated) - 1

        return position


class CellReader:
    """Reads cell values from ODS XML"""

    @staticmethod
    def extract_text(cell: ET.Element, namespaces: dict) -> str:
        """
        Extract text from cell, joining multiple <text:p> elements with newlines

        Based on odsCommon.xsl:170-173
        """
        text_elements = cell.findall('.//text:p', namespaces)
        texts = [elem.text or '' for elem in text_elements]
        return '\n'.join(texts)

    @staticmethod
    def get_column_text(row: ET.Element, column_num: int, namespaces: dict) -> str:
        """
        Get text from specific column, handling spanned cells

        Based on odsCommon.xsl:184-200
        """
        all_cells = list(row.findall('table:table-cell|table:covered-table-cell', namespaces))

        for cell in all_cells:
            pos = CellPosition.calculate_column_position(cell, row, namespaces)
            if pos == column_num:
                # Check if this is a covered cell (from row-spanning)
                if cell.tag == f'{{{namespaces["table"]}}}covered-table-cell':
                    # Recursively get value from previous row
                    prev_row = row.getprevious()
                    if prev_row is not None:
                        return CellReader.get_column_text(prev_row, column_num, namespaces)
                    return ''
                else:
                    return CellReader.extract_text(cell, namespaces)

        return ''


class RowProcessor:
    """Processes spreadsheet rows"""

    @staticmethod
    def is_empty_row(row: ET.Element, namespaces: dict) -> bool:
        """Check if row is empty (all cells have no text)"""
        cells = row.findall('.//table:table-cell', namespaces)
        all_text = ''.join(CellReader.extract_text(cell, namespaces) for cell in cells)
        return all_text.strip() == ''

    @staticmethod
    def has_end_marker(row: ET.Element, namespaces: dict) -> bool:
        """Check if row contains 'END' marker"""
        cells = row.findall('.//table:table-cell', namespaces)
        for cell in cells:
            text = CellReader.extract_text(cell, namespaces).strip()
            if text == 'END':
                return True
        return False

    @staticmethod
    def find_last_data_row(rows: List[ET.Element], namespaces: dict) -> Optional[ET.Element]:
        """
        Find last data row (row before 'END' marker or last row)

        Based on gcExportSubset.xsl:154-158
        """
        for i, row in enumerate(rows):
            if RowProcessor.has_end_marker(row, namespaces):
                # Return previous row if exists
                return rows[i - 1] if i > 0 else None

        # No END marker found, return last row
        return rows[-1] if rows else None


class ColumnMetadata:
    """Manages column metadata"""

    def __init__(self, long_name: str, is_key: bool = False):
        self.long_name = long_name
        # Generate short name by removing non-word characters
        self.short_name = re.sub(r'\W+', '', long_name)
        self.use = 'required' if is_key else 'optional'
        self.data_type = 'string'

    def to_xml(self) -> ET.Element:
        """Convert to Genericode Column XML element"""
        col = ET.Element('Column', Id=self.short_name, Use=self.use)

        short_name = ET.SubElement(col, 'ShortName')
        short_name.text = self.short_name

        long_name = ET.SubElement(col, 'LongName')
        long_name.text = self.long_name

        data = ET.SubElement(col, 'Data', Type=self.data_type)

        return col


class ModelNameTransformer:
    """Handles model name transformations (lengthening/shortening)"""

    def __init__(self, massage_xml_path: Optional[str] = None):
        self.passes = []
        if massage_xml_path:
            self.load_transformations(massage_xml_path)

    def load_transformations(self, xml_path: str):
        """Load transformations from massageModelName.xml"""
        tree = ET.parse(xml_path)
        root = tree.getroot()

        for pass_elem in root.findall('pass'):
            lengthen = pass_elem.find('lengthen')
            if lengthen is not None:
                self.passes.append({
                    'find': lengthen.get('find'),
                    'replace': lengthen.get('replace')
                })

    def lengthen(self, value: str) -> str:
        """
        Apply lengthening transformations in reverse document order

        Based on gcExportSubset.xsl:213-235
        """
        result = value
        # Process passes in reverse order
        for pass_data in reversed(self.passes):
            result = re.sub(pass_data['find'], pass_data['replace'], result)
        return result


class GenericodeBuilder:
    """Builds Genericode XML output"""

    GC_NAMESPACE = 'http://docs.oasis-open.org/codelist/ns/genericode/1.0/'

    def __init__(self, identification_xml_path: Optional[str] = None):
        self.identification_path = identification_xml_path
        self.columns = []
        self.rows = []

    def add_column(self, column: ColumnMetadata):
        """Add column to column set"""
        self.columns.append(column)

    def add_model_name_column(self):
        """Add the ModelName column (standard mode)"""
        col = ColumnMetadata('Model Name', is_key=False)
        col.short_name = 'ModelName'
        col.use = 'required'
        self.columns.insert(0, col)

    def add_row_number_column(self, column_name: str):
        """Add row number column"""
        col = ColumnMetadata(column_name, is_key=False)
        col.use = 'required'
        col.data_type = 'integer'
        self.columns.insert(1, col)

    def create_key_element(self, key_column_ref: str = 'DictionaryEntryName') -> ET.Element:
        """Create Key element"""
        key = ET.Element('Key', Id='key')
        short_name = ET.SubElement(key, 'ShortName')
        short_name.text = 'Key'
        col_ref = ET.SubElement(key, 'ColumnRef', Ref=key_column_ref)
        return key

    def load_identification(self) -> ET.Element:
        """
        Load Identification metadata from XML file

        Based on Crane-ods2obdgc.xsl:340-373
        """
        if self.identification_path and Path(self.identification_path).exists():
            tree = ET.parse(self.identification_path)
            return tree.getroot()
        else:
            # Return default placebo identification
            ident = ET.Element('Identification')

            short_name = ET.SubElement(ident, 'ShortName')
            short_name.text = 'OBDNDRSkeleton'

            long_name = ET.SubElement(ident, 'LongName')
            long_name.text = 'OASIS Business Document NDR skeleton genericode file'

            version = ET.SubElement(ident, 'Version')
            version.text = '1'

            canonical_uri = ET.SubElement(ident, 'CanonicalUri')
            canonical_uri.text = 'urn:X-CraneSoftwrights.com'

            canonical_version_uri = ET.SubElement(ident, 'CanonicalVersionUri')
            canonical_version_uri.text = 'urn:X-CraneSoftwrights.com'

            return ident

    def build(self, indent: bool = True) -> ET.Element:
        """Build complete Genericode XML structure"""
        # Set namespace
        ET.register_namespace('gc', self.GC_NAMESPACE)

        root = ET.Element(f'{{{self.GC_NAMESPACE}}}CodeList')

        # Add Identification
        ident = self.load_identification()
        root.append(ident)

        # Add ColumnSet
        column_set = ET.SubElement(root, 'ColumnSet')
        for col in self.columns:
            column_set.append(col.to_xml())

        # Add Key (for DictionaryEntryName)
        key = self.create_key_element()
        column_set.append(key)

        # Add SimpleCodeList
        simple_code_list = ET.SubElement(root, 'SimpleCodeList')
        for row_data in self.rows:
            simple_code_list.append(row_data)

        return root

    def add_row_data(self, row_elem: ET.Element):
        """Add a row element to the output"""
        self.rows.append(row_elem)


class ODS2GenericodeConverter:
    """Main converter class"""

    def __init__(self,
                 ods_files: List[str],
                 output_path: str,
                 identification_uri: Optional[str] = None,
                 lengthen_model_name_uri: Optional[str] = None,
                 sheet_name_regex: str = r'^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*',
                 row_number_column_name: Optional[str] = None,
                 raw_sheet_long_name: Optional[str] = None):

        self.ods_files = ods_files
        self.output_path = output_path
        self.identification_uri = identification_uri
        self.sheet_name_regex = sheet_name_regex
        self.row_number_column_name = row_number_column_name
        self.raw_sheet_long_name = raw_sheet_long_name

        # Initialize transformers
        self.name_transformer = ModelNameTransformer(lengthen_model_name_uri)
        self.gc_builder = GenericodeBuilder(identification_uri)

        # Standard mode vs raw mode
        self.is_raw_mode = raw_sheet_long_name is not None and raw_sheet_long_name != ''

    def extract_column_metadata(self, sheets: List[Tuple[ET.Element, str]]) -> List[ColumnMetadata]:
        """
        Extract column metadata from first row of sheets

        Based on Crane-ods2obdgc.xsl:233-248
        """
        namespaces = ODSReader.ODS_NAMESPACES

        # Collect all unique column headers
        column_names = {}  # Use dict to preserve order while ensuring uniqueness

        for sheet, _ in sheets:
            rows = sheet.findall('.//table:table-row', namespaces)
            if not rows:
                continue

            # First row contains headers
            header_row = rows[0]
            cells = header_row.findall('.//table:table-cell', namespaces)

            for cell in cells:
                text = CellReader.extract_text(cell, namespaces).strip()
                if text:  # Only non-empty headers
                    column_names[text] = True

        # Create column metadata
        columns = []
        for name in column_names.keys():
            # DictionaryEntryName is the key column (required) in standard mode
            is_key = (name == 'Dictionary Entry Name' and not self.is_raw_mode)
            col = ColumnMetadata(name, is_key=is_key)
            columns.append(col)

        return columns

    def process_sheet(self, sheet: ET.Element, sheet_name: str,
                     column_metadata: List[ColumnMetadata]) -> List[ET.Element]:
        """
        Process a single sheet and return row elements

        Based on gcExportSubset.xsl:134-200
        """
        namespaces = ODSReader.ODS_NAMESPACES
        rows_data = []

        # Get all rows
        all_rows = sheet.findall('.//table:table-row', namespaces)
        if not all_rows:
            return rows_data

        # Skip first row (headers)
        data_rows = all_rows[1:]

        # Find last data row
        last_row = RowProcessor.find_last_data_row(data_rows, namespaces)
        if not last_row:
            return rows_data

        last_row_index = data_rows.index(last_row)

        # Process rows up to and including last_row
        for row_num, row in enumerate(data_rows[:last_row_index + 1], start=2):
            # Skip empty rows
            if RowProcessor.is_empty_row(row, namespaces):
                continue

            # Create Row element
            row_elem = ET.Element('Row')

            # Add ModelName value (expanded sheet name)
            model_name = self.name_transformer.lengthen(sheet_name)

            if not self.is_raw_mode:
                # Standard mode: add ModelName
                value_elem = ET.SubElement(row_elem, 'Value', ColumnRef='ModelName')
                simple_value = ET.SubElement(value_elem, 'SimpleValue')
                simple_value.text = model_name
            else:
                # Raw mode: add sheet name column
                worksheet_id = re.sub(r'\W+', '', self.raw_sheet_long_name)
                value_elem = ET.SubElement(row_elem, 'Value', ColumnRef=worksheet_id)
                simple_value = ET.SubElement(value_elem, 'SimpleValue')
                simple_value.text = model_name

            # Add row number if enabled
            if self.row_number_column_name:
                col_ref = re.sub(r'\W+', '', self.row_number_column_name)
                value_elem = ET.SubElement(row_elem, 'Value', ColumnRef=col_ref)
                simple_value = ET.SubElement(value_elem, 'SimpleValue')
                simple_value.text = str(row_num)

            # Add column values
            for col_idx, col_meta in enumerate(column_metadata, start=1):
                cell_text = CellReader.get_column_text(row, col_idx, namespaces)

                # Only add Value if cell has content
                if cell_text.strip():
                    value_elem = ET.SubElement(row_elem, 'Value',
                                               ColumnRef=col_meta.short_name)
                    simple_value = ET.SubElement(value_elem, 'SimpleValue')
                    simple_value.text = cell_text

            rows_data.append(row_elem)

        return rows_data

    def convert(self):
        """Main conversion method"""
        # Load all ODS files and extract sheets
        all_sheets = []

        for ods_path in self.ods_files:
            reader = ODSReader(ods_path).load()
            sheets = reader.get_sheets(self.sheet_name_regex)

            for sheet in sheets:
                sheet_name = reader.get_sheet_name(sheet)
                all_sheets.append((sheet, sheet_name))

        if not all_sheets:
            raise ValueError("No sheets found matching the filter criteria")

        # Extract column metadata from all sheets
        column_metadata = self.extract_column_metadata(all_sheets)

        # Add special columns
        if not self.is_raw_mode:
            # Standard mode: add ModelName column
            self.gc_builder.add_model_name_column()
        else:
            # Raw mode: add sheet name column
            if self.raw_sheet_long_name:
                col = ColumnMetadata(self.raw_sheet_long_name, is_key=False)
                col.short_name = re.sub(r'\W+', '', self.raw_sheet_long_name)
                col.use = 'optional'
                self.gc_builder.add_column(col)

        # Add row number column if specified
        if self.row_number_column_name:
            self.gc_builder.add_row_number_column(self.row_number_column_name)

        # Add user-defined columns
        for col in column_metadata:
            self.gc_builder.add_column(col)

        # Process all sheets
        for sheet, sheet_name in all_sheets:
            row_elements = self.process_sheet(sheet, sheet_name, column_metadata)
            for row_elem in row_elements:
                self.gc_builder.add_row_data(row_elem)

        # Build and write output
        root = self.gc_builder.build(indent=True)
        tree = ET.ElementTree(root)

        # Write with proper indentation
        ET.indent(tree, space='  ')
        tree.write(self.output_path, encoding='utf-8', xml_declaration=True)


# Example usage
if __name__ == '__main__':
    converter = ODS2GenericodeConverter(
        ods_files=[
            'UBL-Library-Google.ods',
            'UBL-Documents-Google.ods'
        ],
        output_path='UBL-Entities-2.5.gc',
        identification_uri='ident-UBL.xml',
        lengthen_model_name_uri='massageModelName.xml',
        sheet_name_regex=r'^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*',
        row_number_column_name=None,
        raw_sheet_long_name=None
    )

    converter.convert()
```

### Implementation Notes

1. **Namespace Handling**: Python's ElementTree requires full namespace URIs in XPath expressions. Use the namespace dictionary consistently.

2. **Column Position**: The XSLT has complex logic for handling repeated and spanned columns. The Python implementation simplifies this by iterating through cells and checking attributes.

3. **Cell Text Extraction**: Multiple `<text:p>` elements in a cell should be joined with newlines (`\n`), matching the XSLT behavior.

4. **END Marker**: The transformation stops processing rows when it encounters a cell containing "END" text.

5. **Empty Row Detection**: Rows where all cells are empty (after stripping whitespace) should be skipped.

6. **Model Name Transformation**: Apply regex transformations in **reverse** document order (last pass first).

7. **Short Name Generation**: Remove all non-word characters (`\W+` regex) from long names to create short names.

8. **Key Column**: In standard mode, `DictionaryEntryName` is the required key column.

9. **Optional vs Required**: Only `DictionaryEntryName` and injected columns (ModelName, row number) are marked as `Use="required"`. All user-defined columns are `Use="optional"`.

10. **XML Indentation**: Use `ET.indent()` (Python 3.9+) or a custom indentation function for readable output.

### Testing Strategy

1. **Unit Tests**:
   - Test `column_letter_to_number()` and `column_number_to_letter()` with edge cases (A, Z, AA, AZ, ZZ, AAA)
   - Test `extract_text()` with multi-line cells
   - Test `calculate_column_position()` with repeated/spanned columns
   - Test `ModelNameTransformer` with various regex patterns

2. **Integration Tests**:
   - Compare output of Python implementation with XSLT output
   - Test with multiple ODS files
   - Test sheet filtering with various regexes
   - Test both standard and raw modes

3. **Edge Cases**:
   - Empty sheets
   - Sheets with only headers
   - Cells with annotations/comments
   - Repeated rows
   - Spanned cells (both column and row spanning)

### Performance Considerations

1. **Memory**: Loading entire ODS files into memory may be expensive for very large spreadsheets. Consider streaming approaches if needed.

2. **XML Parsing**: `xml.etree.ElementTree` is reasonably fast but not the fastest option. Consider `lxml` for better performance.

3. **Regex Compilation**: Compile frequently-used regexes once at initialization.

4. **Caching**: Cache column positions and frequently accessed elements to avoid repeated XPath queries.

### Differences from XSLT

1. **XPath**: XSLT uses sophisticated XPath 2.0 expressions. Python requires more explicit iteration.

2. **Type System**: XSLT has strong typing (xsd:string, xsd:integer). Python is dynamically typed but should validate data types.

3. **Error Handling**: XSLT terminates with `xsl:message terminate="yes"`. Python should raise appropriate exceptions.

4. **Indentation**: XSLT uses Saxon's built-in indentation. Python requires explicit indentation logic.

---

## Appendix A: Regular Expression Reference

### Sheet Name Filter

Default regex: `^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))|^[^Ll].*`

**Purpose**: Exclude sheets named "Log" or "log" (case-insensitive for first letter).

**Breakdown**:
- `^([Ll]($|[^o].*|o($|[^g].*|g($|[^s].*))))` - Starts with L or l, but not followed by "og"
- `|^[^Ll].*` - OR starts with any character except L or l

**Examples**:
- ✓ Matches: "Invoice", "Library", "Line", "Legal"
- ✗ Excludes: "Log", "log", "Logs"

---

## Appendix B: File References

### massageModelName.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
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
    <shorten find="Qualification" replace="Qlfctn"/>
    <lengthen find="Qlfctn" replace="Qualification"/>
  </pass>
  <!-- Additional passes... -->
</modelNameMassage>
```

### ident-UBL.xml

```xml
<!DOCTYPE Identification [
<!ENTITY short "CSD01">
<!ENTITY dir   "csd01">
<!ENTITY version "2.5">
]>
<Identification>
  <ShortName>UBL-&version;-&short;</ShortName>
  <LongName>UBL &version; &short; Business Entity Summary</LongName>
  <Version>&version;</Version>
  <CanonicalUri>urn:oasis:names:specification:ubl:BIE</CanonicalUri>
  <CanonicalVersionUri>urn:oasis:names:specification:ubl:BIE:&version;</CanonicalVersionUri>
  <LocationUri>http://docs.oasis-open.org/ubl/&dir;-UBL-&version;/mod/UBL-Entities-&version;.gc</LocationUri>
  <Agency>
     <LongName xml:lang="en">OASIS Universal Business Language</LongName>
     <Identifier>UBL</Identifier>
  </Agency>
</Identification>
```

---

## Appendix C: Genericode Output Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<gc:CodeList xmlns:gc="http://docs.oasis-open.org/codelist/ns/genericode/1.0/">
  <Identification>
    <ShortName>UBL-2.5-CSD01</ShortName>
    <LongName>UBL 2.5 CSD01 Business Entity Summary</LongName>
    <Version>2.5</Version>
    <CanonicalUri>urn:oasis:names:specification:ubl:BIE</CanonicalUri>
    <CanonicalVersionUri>urn:oasis:names:specification:ubl:BIE:2.5</CanonicalVersionUri>
    <LocationUri>http://docs.oasis-open.org/ubl/csd01-UBL-2.5/mod/UBL-Entities-2.5.gc</LocationUri>
    <Agency>
      <LongName xml:lang="en">OASIS Universal Business Language</LongName>
      <Identifier>UBL</Identifier>
    </Agency>
  </Identification>
  <ColumnSet>
    <Column Id="ModelName" Use="required">
      <ShortName>ModelName</ShortName>
      <LongName>Model Name</LongName>
      <Data Type="string"/>
    </Column>
    <Column Id="DictionaryEntryName" Use="required">
      <ShortName>DictionaryEntryName</ShortName>
      <LongName>Dictionary Entry Name</LongName>
      <Data Type="string"/>
    </Column>
    <Column Id="ObjectClass" Use="optional">
      <ShortName>ObjectClass</ShortName>
      <LongName>Object Class</LongName>
      <Data Type="string"/>
    </Column>
    <!-- More columns... -->
    <Key Id="key">
      <ShortName>Key</ShortName>
      <ColumnRef Ref="DictionaryEntryName"/>
    </Key>
  </ColumnSet>
  <SimpleCodeList>
    <Row>
      <Value ColumnRef="ModelName">
        <SimpleValue>UBL-Invoice-2.5</SimpleValue>
      </Value>
      <Value ColumnRef="DictionaryEntryName">
        <SimpleValue>Invoice. Issue Date</SimpleValue>
      </Value>
      <Value ColumnRef="ObjectClass">
        <SimpleValue>Invoice</SimpleValue>
      </Value>
      <!-- More values... -->
    </Row>
    <!-- More rows... -->
  </SimpleCodeList>
</gc:CodeList>
```

---

## Summary

The `ods2gc` transformation is a sophisticated process that:

1. **Extracts** structured data from ODS spreadsheet files
2. **Transforms** sheet names using configurable regex patterns
3. **Generates** Genericode XML with proper column metadata
4. **Validates** data structure (required columns, key columns)
5. **Injects** metadata from external XML files

The Python implementation should closely follow the XSLT logic while taking advantage of Python's clearer iteration and data structure capabilities. Key areas requiring careful attention are:

- Column position calculations with repeated/spanned cells
- Model name transformations in reverse order
- Proper namespace handling throughout
- Correct identification of the last data row
- Generation of short names from long names

This analysis provides everything needed to recreate the exact transformation logic in native Python code.

---

## Appendix D: Actual Spreadsheet Analysis

### Downloaded Spreadsheets

The actual source spreadsheets used in the UBL build process were downloaded and analyzed:

- **Library Spreadsheet**: `UBL-Library-Google.ods` (639 KB)
  - URL: https://docs.google.com/spreadsheets/d/18o1YqjHWUw0-s8mb3ja4i99obOUhs-4zpgso6RZrGaY
  - Sheet: `CommonLibrary`

- **Documents Spreadsheet**: `UBL-Documents-Google.ods` (912 KB)
  - URL: https://docs.google.com/spreadsheets/d/1024Th-Uj8cqliNEJc-3pDOR7DxAAW7gCG4e-pbtarsg
  - Sheets: `ApplicationResponse`, `AttachedDocument`, `AwardedNotification`, `BillOfLading`, `BusinessCard`, etc.

- **Signature Spreadsheet**: `UBL-Signature-Google.ods` (16 KB)
  - URL: https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g

### Actual Column Structure

The actual UBL spreadsheets have **26 columns** (A through Z), not 45 as shown in the empty template. The structure is identical across all document sheets and the library sheet.

| # | Letter | Column Name | Type | Notes |
|---|--------|-------------|------|-------|
| 1 | A | Component Name | **FORMULA** | Always calculated from Object Class Qualifier + Object Class |
| 2 | B | Subset Cardinality | MANUAL | Subset-specific cardinality constraints |
| 3 | C | Cardinality | MANUAL | Base model cardinality (0..1, 1, 0..n, 1..n) |
| 4 | D | Endorsed Cardinality | MANUAL | Future cardinality when breaking backwards compatibility |
| 5 | E | Endorsed Cardinality Rationale | MANUAL | Explanation for endorsed changes |
| 6 | F | Definition | MANUAL/FORMULA | Manual for BBIEs/ASBIEs, formula for ABIEs |
| 7 | G | Deprecated Definition | MANUAL | Historical definitions when changed |
| 8 | H | Alternative Business Terms | MIXED | Sometimes formula, sometimes manual |
| 9 | I | Examples | MANUAL | Sample values |
| 10 | J | **Dictionary Entry Name** | **MANUAL** | **PRIMARY KEY** - unique identifier |
| 11 | K | Object Class Qualifier | MANUAL | Qualifiers for the object class |
| 12 | L | Object Class | MANUAL | The business object being modeled |
| 13 | M | Property Term Qualifier | FORMULA/MANUAL | Derived for some component types |
| 14 | N | Property Term Possessive Noun | MIXED | Sometimes calculated |
| 15 | O | Property Term Primary Noun | MIXED | Sometimes calculated |
| 16 | P | Property Term | MIXED | Sometimes calculated from parts |
| 17 | Q | Representation Term | MANUAL | How the property is represented (Identifier, Text, Code, etc.) |
| 18 | R | Data Type Qualifier | MANUAL | Qualifiers for data type |
| 19 | S | Data Type | MANUAL | The data type (e.g., Code Type, Identifier Type) |
| 20 | T | Associated Object Class Qualifier | MANUAL | Qualifier for associated ABIE |
| 21 | U | Associated Object Class | MANUAL | Related ABIE for associations |
| 22 | V | Component Type | MANUAL | ABIE, BBIE, or ASBIE |
| 23 | W | UN/TDED Code | MANUAL | UN Trade Data Elements Directory code |
| 24 | X | Current Version | MANUAL | Version when introduced |
| 25 | Y | Last Changed | MANUAL | Version of last change |
| 26 | Z | Editor's Notes | MANUAL | Internal notes for editors |

### Formula Columns Explained

#### Column A: Component Name (ALWAYS FORMULA)

```
Formula: =SUBSTITUTE(CONCATENATE([.K];[.L]);" ";"")
Purpose: Removes spaces from Object Class Qualifier + Object Class
Example: "Activity" + "Data Line" → "ActivityDataLine"
```

This column is **never** manually entered - it's always calculated from the object class components.

#### Column F: Definition (FORMULA for ABIEs)

For Aggregate Business Information Entities (ABIEs), the definition is generated:

```
Formula: =CONCATENATE(IF([.K]="";"";CONCATENATE([.K];"_ "));[.L];". Details")
Purpose: Creates standard ABIE definition
Example: "Activity Data Line. Details" or "Acknowledged_ Receipt. Details"
```

For Basic BIEs (BBIEs) and Association BIEs (ASBIEs), this column contains manually-entered semantic definitions.

#### Column M: Property Term Qualifier (FORMULA for BBIEs)

For BBIEs, complex formulas derive the property term qualifier from representation terms:

```
Formula: =SUBSTITUTE(CONCATENATE([.M];[.N];
         IF([.O]="Identifier";"ID";
         IF(AND([.O]="Text";OR([.M]<>"";[.N]<>""));"";[.O]));
         IF(AND([.Q]<>"Text";[.O]<>[.Q];...)
         IF([.Q]="Identifier";"ID";[.Q]);""));" ";"")
         
Purpose: Derives the property term qualifier from property components
Example: "Action" + "Code" with RepresentationTerm="Code" → "ActionCode"
```

This formula handles special cases like converting "Identifier" to "ID" and removing redundant "Text" qualifiers.

#### Column J: Dictionary Entry Name (ALWAYS MANUAL - PRIMARY KEY)

This is the **most critical column** - it is:
- Always manually entered
- Never calculated by formula
- The primary key for the genericode output
- Used to uniquely identify each Business Information Entity

**Format**: Follows CCTS naming rules, e.g.:
- ABIE: `Activity Data Line`
- BBIE: `Activity Data Line. Identifier. Identifier`
- ASBIE: `Activity Data Line. Acknowledged_ Receipt`

### Formula vs Manual Input Summary

**100% Formula** (Never manual input):
- Column A: Component Name

**100% Manual** (Never formulas):
- Column C: Cardinality
- Column D: Endorsed Cardinality
- Column E: Endorsed Cardinality Rationale
- Column I: Examples
- **Column J: Dictionary Entry Name (PRIMARY KEY)**
- Column K: Object Class Qualifier
- Column L: Object Class
- Column Q: Representation Term
- Column R: Data Type Qualifier
- Column S: Data Type
- Column T: Associated Object Class Qualifier
- Column U: Associated Object Class
- Column V: Component Type
- Column W: UN/TDED Code
- Column X: Current Version
- Column Y: Last Changed
- Column Z: Editor's Notes

**Context-Dependent** (Formula or manual depending on row type):
- Column F: Definition (formula for ABIEs, manual for BBIEs/ASBIEs)
- Column H: Alternative Business Terms (mixed)
- Column M: Property Term Qualifier (formula for some BBIEs)
- Column N: Property Term Possessive Noun (formula for some rows)
- Column O: Property Term Primary Noun (formula for some rows)
- Column P: Property Term (formula for some rows)

### Component Types and Formula Usage

The spreadsheet contains three types of components, each with different formula patterns:

#### 1. ABIE (Aggregate Business Information Entity)
**Pink/red background rows**
- Column A (Component Name): Formula
- Column F (Definition): Formula (generates "ObjectClass. Details")
- Column J (Dictionary Entry Name): Manual - just the object class
- Other semantic columns: Usually empty

#### 2. BBIE (Basic Business Information Entity)
**White background rows**
- Column A (Component Name): Formula
- Column F (Definition): Manual - semantic business definition
- Column J (Dictionary Entry Name): Manual - full DEN with property and representation
- Columns M-P (Property Term parts): Often formulas that derive from components
- Columns Q-S (Data Type info): Manual

#### 3. ASBIE (Association Business Information Entity)  
**Green background rows**
- Column A (Component Name): Formula
- Column F (Definition): Manual - relationship description
- Column J (Dictionary Entry Name): Manual - full DEN with associated object class
- Columns T-U (Associated Object Class): Manual
- Representation Term column: Usually "Association"

### Verification Against Template

The empty template file (`Empty CCTS Model.ods`) that was initially analyzed had **45 columns** with additional subset-related columns and context columns. The actual production spreadsheets use a **streamlined 26-column structure** that focuses on the core CCTS metamodel elements.

**Key differences**:
1. Template has subset profile columns (Subset MyProf 1, Subset MyProf 2, Subset Comment) - production has single Subset Cardinality
2. Template has extensive Context columns (Business Process, Region, Industry, etc.) - production omits these
3. Template includes CCL Dictionary Entry Name column - production omits
4. Template has marker columns (ABIE, BBIE, ASBIE, END) - production uses Component Type column

The **core 26 columns** documented above are what's actually used in the UBL 2.5 build process.

### Python Implementation Considerations

When implementing the Python version, be aware that:

1. **Formula cells should be ignored** - only read the calculated/displayed value, not the formula itself
2. **Column A values are derived** - but the ODS file stores the calculated result, so just read it as text
3. **Column J is the key** - ensure this is always present and unique
4. **Empty cells are common** - many columns are only populated for specific component types
5. **Component Type (Column V)** determines which other columns should have data

### Row Structure Pattern

Typical row grouping in the spreadsheets:

```
Row 1: ABIE (pink) - Activity Data Line
  - Component Name: ActivityDataLine (formula)
  - Dictionary Entry Name: Activity Data Line (manual)
  - Object Class: Activity Data Line (manual)
  - Component Type: ABIE
  - Definition: Activity Data Line. Details (formula)

Row 2: BBIE (white) - Identifier property
  - Component Name: ActivityDataLineIdentifier (formula)
  - Dictionary Entry Name: Activity Data Line. Identifier. Identifier (manual)
  - Object Class: Activity Data Line (manual)
  - Property Term: Identifier (manual/formula)
  - Representation Term: Identifier (manual)
  - Component Type: BBIE
  - Definition: Identifies the Activity Data Line (manual)

Row 3: ASBIE (green) - Reference to another ABIE
  - Component Name: AcknowledgedReceipt (formula)
  - Dictionary Entry Name: Activity Data Line. Acknowledged_ Receipt (manual)
  - Object Class: Activity Data Line (manual)
  - Associated Object Class: Receipt (manual)
  - Representation Term: Association (manual)
  - Component Type: ASBIE
  - Definition: Reference to receipt acknowledgement (manual)
```

This hierarchical structure groups child elements under their parent ABIE.

---

