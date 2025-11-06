# Common UBL Development Tasks

This document provides step-by-step instructions for frequent tasks in UBL development.

## Table of Contents

1. [Building Locally](#building-locally)
2. [Adding a New Document Type](#adding-a-new-document-type)
3. [Adding Library Components](#adding-library-components)
4. [Updating Code Lists](#updating-code-lists)
5. [Adding Sample Instances](#adding-sample-instances)
6. [Updating Documentation](#updating-documentation)
7. [Fixing Validation Errors](#fixing-validation-errors)
8. [Adding Artwork/Diagrams](#adding-artworkdiagrams)
9. [Running Spell Check](#running-spell-check)
10. [Comparing Versions](#comparing-versions)

---

## Building Locally

### Prerequisites
- Java JDK 1.8
- Python 3.12+
- System packages: aspell, libreoffice, pandoc

### Quick Build
```bash
# Using Python (preferred on ubl-2.5-python branch)
python build.py target local debug

# Using shell script
./build.sh target local debug
```

### Check Results
```bash
# Look for error files
ls target/UBL-2.5-csd01-debug/*WARNING*.txt 2>/dev/null
ls target/UBL-2.5-csd01-debug/*PROBLEMS*.txt 2>/dev/null

# Check exit code
cat target/UBL-2.5-csd01-debug-archive-only/build.exitcode.debug.txt

# Review console log
less target/UBL-2.5-csd01-debug-archive-only/build.console.debug.txt
```

### Slash Command
For guided build process: `/build-local`

---

## Adding a New Document Type

### Step 1: Update Documents Spreadsheet

1. Open Documents spreadsheet (URL in `build.py` as `docGoogle`)
2. Add new rows for your document:
   - Document name (e.g., "Catalogue")
   - Component definitions
   - Cardinality
   - Data types
   - Definitions

3. Follow existing document patterns for structure

### Step 2: Create Sample Instance

Create XML sample in `raw/xml/`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Catalogue xmlns="urn:oasis:names:specification:ubl:schema:xsd:Catalogue-2"
           xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
           xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
  <cbc:UBLVersionID>2.5</cbc:UBLVersionID>
  <cbc:ID>CAT-001</cbc:ID>
  <!-- Add required elements -->
</Catalogue>
```

### Step 3: Create JSON Sample

Create JSON sample in `raw/json/`:

```json
{
  "$schema": "../json-schema/maindoc/UBL-Catalogue-2.5.json",
  "Catalogue": {
    "UBLVersionID": "2.5",
    "ID": "CAT-001"
  }
}
```

### Step 4: Update Schema Summary

Edit `UBL-Schema-summary-information.xml`:

```xml
<row>
  <entry><filename>UBL-Catalogue-2.5.xsd</filename></entry>
  <entry>Catalogue</entry>
  <entry>A document describing items for sale or lease</entry>
</row>
```

### Step 5: Add Validation Test

Edit `raw/val/testsamples.sh`:

```bash
# Add line for your document
$validate xml/UBL-Catalogue-2.5-Example.xml maindoc/UBL-Catalogue-2.5.xsd
```

Also update `raw/val/testsamples.bat` for Windows.

### Step 6: Build and Test

```bash
python build.py target local debug

# Verify schema generated
ls target/UBL-2.5-csd01-debug/xsd/maindoc/UBL-Catalogue-2.5.xsd

# Run validation
cd raw/val
./testsamples.sh
```

### Step 7: Update Documentation

Add document description to `UBL.xml`:

- Add to document inventory section
- Include use cases
- Add examples and diagrams as needed

---

## Adding Library Components

### Step 1: Update Library Spreadsheet

1. Open Library spreadsheet (URL in `build.py` as `libGoogle`)
2. Locate appropriate section:
   - ABIEs (Aggregate Business Information Entities)
   - ASBIEs (Association Business Information Entities)
   - BBIEs (Basic Business Information Entities)

3. Add component definition:
   - Component name
   - Property term
   - Cardinality
   - Object class
   - Data type
   - Definition
   - Examples

### Step 2: Check Naming Conventions

Ensure component follows UBL naming rules:
- Object Class + Property Term + Type
- Example: `Party.Telecommunication.Telecommunication`

### Step 3: Build to Generate Schema

```bash
python build.py target local debug
```

Schema will be generated in:
- `target/.../xsd/common/UBL-CommonAggregateComponents-2.5.xsd`
- `target/.../xsd/common/UBL-CommonBasicComponents-2.5.xsd`

### Step 4: Update Samples

Add new component to existing sample instances where applicable.

### Step 5: Document Component

If significant component, add documentation to `raw/mod/summary/`:

Create `{ComponentName}.xml` with detailed description, examples, and usage guidance.

---

## Updating Code Lists

### Step 1: Identify Code List

Code lists are in `raw/cl/master-code-list-UBL-*.xml`:
- Currency codes
- Country codes
- Unit codes
- Document types
- Status codes

### Step 2: Edit Master Code List File

```xml
<CodeListDocument>
  <Identification>
    <ShortName>UBL_CurrencyCode</ShortName>
    <Version>2.5</Version>
    <CanonicalUri>urn:oasis:names:tc:ubl:codelist:CurrencyCode-2.5</CanonicalUri>
    <CanonicalVersionUri>urn:oasis:names:tc:ubl:codelist:CurrencyCode-2.5:2.5</CanonicalVersionUri>
  </Identification>
  <ColumnSet>
    <Column Id="code" Use="required">
      <ShortName>Code</ShortName>
      <Data Type="string"/>
    </Column>
    <Column Id="name" Use="optional">
      <ShortName>Name</ShortName>
      <Data Type="string"/>
    </Column>
  </ColumnSet>
  <SimpleCodeList>
    <Row>
      <Value ColumnRef="code"><SimpleValue>USD</SimpleValue></Value>
      <Value ColumnRef="name"><SimpleValue>US Dollar</SimpleValue></Value>
    </Row>
    <!-- Add/modify rows -->
  </SimpleCodeList>
</CodeListDocument>
```

### Step 3: Run Code List Tooling

If using external code list tools:
```bash
# See: https://www.oasis-open.org/committees/document.php?document_id=67039
# Process with tools and copy results to raw/cl/gc/
```

### Step 4: Update CVA Skeleton

Edit `UBL-CVA-Skeleton.cva` to add validation rules for new code list:

```xml
<ValueList uri="urn:oasis:names:tc:ubl:codelist:CurrencyCode-2.5">
  <Annotation>
    <Description>Currency codes</Description>
  </Annotation>
</ValueList>
```

### Step 5: Build and Validate

```bash
python build.py target local debug

# Check for code list warnings
ls target/*/LIST-OF-PROBLEM-CODE-LISTS.txt 2>/dev/null
```

---

## Adding Sample Instances

### XML Samples

Create in `raw/xml/` following pattern `UBL-{DocumentType}-2.5-Example.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
  <cbc:UBLVersionID>2.5</cbc:UBLVersionID>
  <cbc:CustomizationID>urn:oasis:names:specification:ubl:xpath:Invoice-2.5</cbc:CustomizationID>
  <cbc:ProfileID>urn:oasis:names:specification:ubl:profile:invoice</cbc:ProfileID>
  <cbc:ID>INV-0001</cbc:ID>
  <cbc:IssueDate>2025-11-06</cbc:IssueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <!-- More elements -->
</Invoice>
```

### JSON Samples

Create in `raw/json/` following pattern `UBL-{DocumentType}-2.5-Example.json`:

```json
{
  "$schema": "../json-schema/maindoc/UBL-Invoice-2.5.json",
  "Invoice": {
    "UBLVersionID": "2.5",
    "CustomizationID": "urn:oasis:names:specification:ubl:xpath:Invoice-2.5",
    "ProfileID": "urn:oasis:names:specification:ubl:profile:invoice",
    "ID": "INV-0001",
    "IssueDate": "2025-11-06",
    "InvoiceTypeCode": "380"
  }
}
```

### Update Test Scripts

Add to `raw/val/testsamples.sh`:
```bash
$validate xml/UBL-Invoice-2.5-Example.xml maindoc/UBL-Invoice-2.5.xsd
```

And `raw/val/testsamples.bat`:
```batch
call %validate% xml\UBL-Invoice-2.5-Example.xml maindoc\UBL-Invoice-2.5.xsd
```

### Validate

```bash
cd raw/val
./testsamples.sh

# Or validate single file
xmllint --noout --schema ../../target/.../xsd/maindoc/UBL-Invoice-2.5.xsd ../xml/UBL-Invoice-2.5-Example.xml
```

---

## Updating Documentation

### Hub Document (UBL.xml)

Main specification document in DocBook format:

```xml
<section>
  <title>New Feature</title>
  <para>Description of new feature...</para>
  <programlisting language="xml"><![CDATA[
    <Example>XML here</Example>
  ]]></programlisting>
</section>
```

### Preview Locally

**macOS:**
```bash
# Drag UBL.xml to Safari
# Refresh with Cmd-R after edits
```

**Windows:**
```bash
# Drag UBL.xml to Internet Explorer
# Refresh with Ctrl-R after edits
```

### Add Artwork

1. Create in `images/` using draw.io or SVG editor
2. Export high-res PNG (600 DPI, max 3425px width) to `art/`
3. Create low-res version (96 DPI, max 750px width) in `htmlart/`
4. Reference in UBL.xml:
```xml
<mediaobject>
  <imageobject>
    <imagedata fileref="art/my-diagram.png" width="100%"/>
  </imageobject>
</mediaobject>
```

### Model Documentation Fragments

Create in `raw/mod/summary/`:

```xml
<section>
  <title>Component Name</title>
  <para>Detailed description...</para>
  <itemizedlist>
    <listitem><para>Usage scenario 1</para></listitem>
    <listitem><para>Usage scenario 2</para></listitem>
  </itemizedlist>
</section>
```

---

## Fixing Validation Errors

### Schema Validation Errors

**Error:** "Element not allowed"
```bash
# Check schema definition
grep -A 10 "ElementName" target/.../xsd/maindoc/*.xsd

# Check spreadsheet for typos
# Rebuild after fixing spreadsheet
```

**Error:** "Invalid namespace"
```bash
# Verify namespace URIs in sample match schema
# UBL 2.5 uses: urn:oasis:names:specification:ubl:schema:xsd:{Type}-2
```

### Genericode Errors

Check `LIST-OF-PROBLEM-CODE-LISTS.txt`:

```bash
cat target/*/LIST-OF-PROBLEM-CODE-LISTS.txt

# Usually indicates:
# - Missing column definitions
# - Invalid XML in code list
# - Duplicate code values
```

### Hub Document Validation

If `INVALID-ASSEMBLED-HUB-XML.txt` exists:

```bash
cat target/*/INVALID-ASSEMBLED-HUB-XML.txt

# Check DocBook validity
xmllint --noout --schema db/spec-0.8/docbook/docbook.xsd UBL.xml

# Common issues:
# - Unclosed tags
# - Invalid DocBook elements
# - Entity reference errors
```

---

## Adding Artwork/Diagrams

### Using draw.io

1. Open https://draw.io
2. Create diagram (use UBL-2.3-Pre-awardProcess.drawio as template)
3. Save as `.drawio` in `images/` directory

### Export High-Resolution

1. File → Export as → Advanced...
2. Format: PNG
3. DPI: 600
4. Width: 3425 pixels max (for full width) or proportionally less
5. Zoom: ≤ 100%
6. Transparent background: OFF
7. Border width: 0
8. Save to `art/` directory

### Create Low-Resolution Web Version

1. Copy PNG from `art/` to `htmlart/`
2. Using GIMP or ImageMagick:

```bash
# ImageMagick
convert art/my-diagram.png -resize 750x -density 96 htmlart/my-diagram.png

# GIMP: Image → Scale Image → Width: 750px, Resolution: 96 DPI
```

### Add to Documentation

```xml
<figure>
  <title>Diagram Title</title>
  <mediaobject>
    <imageobject>
      <imagedata fileref="art/my-diagram.png" width="100%"/>
    </imageobject>
  </mediaobject>
</figure>
```

---

## Running Spell Check

### Automatic During Build

Spell check runs automatically and creates `NDR-SPELL-CHECK-WARNING.txt` if issues found.

### View Unexpected Words

```bash
cat unexpectedWords.txt
```

### Add Words to Dictionary

Edit `spellcheck-UBL.txt`:

```text
# One word per line
# Include proper names, acronyms, technical terms
BusinessDocument
Cardholder
Despatch
Geocode
```

### Run Spell Check Manually

```bash
# Using aspell
aspell list < UBL.xml | sort -u > unexpectedWords.txt

# Check against custom dictionary
aspell --personal=./spellcheck-UBL.txt list < UBL.xml
```

---

## Comparing Versions

### Using Build Artifacts

Build process generates comparison reports:

```bash
# Version comparison
open target/.../check-ubl-2.5-csd01-ubl-2.4.html

# Stage comparison
open target/.../check-ubl-2.5-csd02-ubl-2.5-csd01.html
```

### Using Slash Command

```
/compare-versions 2.4 vs 2.5
/compare-versions csd01 vs csd02
```

### Manual Comparison

```bash
# Compare genericode files
diff -u UBL-Entities-2.4-os.gc UBL-Entities-2.5.gc > version-diff.txt

# Compare schemas
diff -r os-UBL-2.4/xsd/ target/.../xsd/ > schema-diff.txt
```

### Entity File Comparison

Check auto-generated comparison entities:

```bash
cat old2newDoc-from-previous-version-library-ent.xml
cat old2newDoc-from-previous-version-documents-ent.xml
cat old2newDoc-from-previous-stage-library-ent.xml
cat old2newDoc-from-previous-stage-documents-ent.xml
```

---

## Tips and Tricks

### Faster Builds
- Cache spreadsheet ODS files locally (place in parent directory)
- Skip Réalta publishing for intermediate builds
- Use incremental validation

### Debugging XSLT
```bash
# Run XSLT manually with Saxon
java -cp utilities/saxon9he/saxon9he.jar \
  net.sf.saxon.Transform \
  -xsl:stylesheet.xsl \
  -s:input.xml \
  -o:output.xml
```

### Finding Components
```bash
# Search genericode
grep "ComponentName" UBL-Entities-2.5.gc

# Search schemas
grep -r "ComponentName" target/.../xsd/
```

### Batch Operations
```bash
# Validate all XML samples
for f in raw/xml/*.xml; do
  xmllint --noout --schema target/.../xsd/maindoc/*.xsd "$f"
done

# Convert all XML samples to JSON (if converter available)
for f in raw/xml/*.xml; do
  xml2json "$f" > "raw/json/$(basename $f .xml).json"
done
```

---

## Getting Help

- **Slash commands:** Type `/` for guided workflows
- **CLAUDE.md:** Reference for configuration and conventions
- **Architecture docs:** `.claude/docs/architecture.md`
- **README.md:** Comprehensive repository documentation
- **UBL TC mailing list:** Ask questions to committee
