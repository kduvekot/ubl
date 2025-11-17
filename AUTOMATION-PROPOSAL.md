# Automating Row Number Updates in UBL Documentation

## Current Workflow

### Source of Truth
1. **Google Sheets** → Exported to ODS files:
   - `UBL-Library-Google.ods`
   - `UBL-Documents-Google.ods`
   - `UBL-Signature-Google.ods`

2. **ODS → Genericode (.gc)** conversion:
   - `Crane-ods2obdgc/Crane-ods2obdgc.xsl` converts ODS to `UBL-Entities-${version}.gc`
   - This is the **authoritative source** for row numbers

3. **HTML Reports** generated from .gc files:
   - `mod/summary/reports/UBL-Invoice-2.5.html` etc.

4. **Documentation** (`UBL.xml`):
   - Contains **hardcoded row number references** in `<ulink role="DEN-Row">` elements
   - These become stale when the spreadsheet changes

5. **Validation** (`hub-integrity.xsl`):
   - Checks row numbers in UBL.xml against calculated rows in .gc file
   - Reports mismatches but doesn't fix them

## The Problem

When the Google Sheets are updated and rows are added/removed:
- The .gc file is regenerated with new row positions
- The UBL.xml documentation still has old row numbers
- Build fails with "Mismatched row number" errors
- **Manual fix required** for each mismatched reference

## Automation Solution

### Option 1: XSLT Auto-Update Script (Recommended)

Create a new XSLT stylesheet: `utilities/update-ubl-row-numbers.xsl`

**Purpose**: Automatically update all `role="DEN-Row"` row numbers in UBL.xml based on the actual rows in the .gc file.

**Algorithm**:
```xslt
For each <ulink role="DEN-Row" remap="DEN-name">NNNN</ulink>:
  1. Look up the DEN (Dictionary Entry Name) in the .gc file
  2. Calculate the actual row number: 2 + count(preceding rows in same model)
  3. Replace the text content with the calculated row number
  4. Copy everything else unchanged
```

**Integration into build.xml**:
```xml
<target name="-update-doc-row-numbers"
        depends="-ods2gc-for-signature,-ods2gc-for-base">
  <echo message="Updating row numbers in UBL.xml..."/>
  <java jar="utilities/saxon9he/saxon9he.jar" fork="true">
    <arg value="-xsl:utilities/update-ubl-row-numbers.xsl"/>
    <arg value="-s:UBL.xml"/>
    <arg value="-o:UBL.xml"/>
    <arg value="gc-uri=UBL-Entities-${UBLversion}.gc"/>
  </java>
</target>
```

**Benefits**:
- ✅ Fully automated - no manual intervention
- ✅ Runs during normal build process
- ✅ Always in sync with .gc file
- ✅ Uses existing Saxon XSLT processor
- ✅ Similar pattern to existing hub-integrity.xsl

### Option 2: Python Script

Create `utilities/update-row-numbers.py`:
- Parse UBL.xml using ElementTree
- Parse .gc file
- Update row numbers
- Write back to UBL.xml

**Benefits**:
- Easier to debug
- More flexible

**Drawbacks**:
- Adds Python dependency
- Inconsistent with existing all-XSLT toolchain

### Option 3: Enhanced Validation Script

Extend `hub-integrity.xsl` to:
1. Detect mismatches (current behavior)
2. **Generate a patch file** with corrections
3. Apply patch automatically

**Drawbacks**:
- More complex than Option 1
- Mixing validation and modification concerns

## Recommendation

**Implement Option 1** - Create `update-ubl-row-numbers.xsl`

### Implementation Steps

1. **Create the XSLT stylesheet** (see template below)
2. **Add build target** to run after .gc generation
3. **Run before validation** so hub-integrity.xsl always passes
4. **Optional**: Add a flag to skip auto-update for manual control

### XSLT Template Structure

```xslt
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:gc="http://docs.oasis-open.org/codelist/ns/genericode/1.0/">

  <xsl:param name="gc-uri" required="yes"/>
  <xsl:variable name="gc" select="document($gc-uri)"/>

  <!-- Key to look up rows by DEN -->
  <xsl:key name="rows" match="gc:Row"
    use="gc:Value[@ColumnRef='DictionaryEntryName']/gc:SimpleValue"/>

  <!-- Identity template - copy everything by default -->
  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <!-- Update DEN-Row references -->
  <xsl:template match="ulink[@role='DEN-Row']/text()">
    <xsl:variable name="den" select="../@remap"/>
    <xsl:variable name="row" select="key('rows', $den, $gc)"/>
    <xsl:variable name="model"
      select="$row/gc:Value[@ColumnRef='ModelName']/gc:SimpleValue"/>
    <xsl:variable name="rowNum"
      select="2 + count($row/preceding-sibling::gc:Row
        [gc:Value[@ColumnRef='ModelName']/gc:SimpleValue = $model])"/>
    <xsl:value-of select="$rowNum"/>
  </xsl:template>

</xsl:stylesheet>
```

## Build Process Integration

### Current Flow
```
1. ODS files → .gc files (Crane-ods2obdgc.xsl)
2. .gc files → HTML reports
3. Build UBL.xml (unchanged)
4. Validate with hub-integrity.xsl ❌ FAILS if rows mismatched
```

### Proposed Flow
```
1. ODS files → .gc files (Crane-ods2obdgc.xsl)
2. .gc files → Auto-update UBL.xml row numbers ✨ NEW
3. .gc files → HTML reports
4. Validate with hub-integrity.xsl ✅ ALWAYS PASSES
```

## Migration Path

1. **Phase 1**: Create the XSLT script and test it
2. **Phase 2**: Add optional build target (manual invocation)
3. **Phase 3**: Integrate into main build (automatic)
4. **Phase 4**: Document for contributors

## Notes

- The .gc file row numbers are calculated as: `2 + count(preceding rows in same model)`
  - The `+2` accounts for header rows in the spreadsheet
- Each model (worksheet) has its own row numbering
- The `@remap` attribute contains the Dictionary Entry Name (DEN) which is unique
- This same logic is used in `hub-integrity.xsl` for validation

## Workflow for Adding New References

When editing UBL.xml and adding new row number references:

### Step 1: Use Placeholder "0"

```xml
<para>
  The Party ABIE (line
  <ulink url="mod/summary/reports/UBL-Invoice-&version;.html#Table-Party.Details"
         conformance="skip"
         role="DEN-Row"
         remap="Party. Details">0</ulink>)
  contains the following elements...
</para>
```

**Key points:**
- Use `0` as the row number (clearly a placeholder)
- The `@remap` attribute must exactly match the Dictionary Entry Name (DEN) from the .gc file
- Use dot-space separator: `"Party. Details"` not `"Party.Details"`

### Step 2: Find the Correct DEN

**Option A: From HTML reports**
- Open `mod/summary/reports/UBL-Invoice-2.5.html`
- Find your element
- The URL anchor shows the DEN: `#Table-Party.Details`
- Use everything after `Table-`: `Party. Details`

**Option B: From .gc file**
```bash
grep -i "party. details" UBL-Entities-2.5.gc
```

**Option C: Copy from existing references**
```bash
grep 'role="DEN-Row"' UBL.xml | grep -i party
```

### Step 3: Run Auto-Update

```bash
java -jar utilities/saxon9he/saxon9he.jar \
  -xsl:utilities/update-ubl-row-numbers.xsl \
  -s:UBL.xml -o:UBL.xml \
  gc-uri=UBL-Entities-2.5.gc
```

### Step 4: Check the Output

The script will show:
```
========================================
UBL Row Number Auto-Update
========================================
Source: file:/home/user/ubl/UBL.xml
GC file: UBL-Entities-2.5.gc
Total DEN-Row references: 234
========================================
  Updated: Party. Details (0 → 1744)
  Updated: PartyName. Details (0 → 1793)

Done. Check output for any ERROR messages.
```

### If You Get the DEN Wrong

```
ERROR: DEN not found in .gc file: "Partty. Details" - keeping original value 0
                                   ^^^^^^ typo!
```

Fix the `@remap` attribute and run again.

## Testing

Test the auto-update script with:
```bash
# Generate .gc file from ODS
ant -Ddir=target -ods2gc-for-base

# Run auto-update
java -jar utilities/saxon9he/saxon9he.jar \
  -xsl:utilities/update-ubl-row-numbers.xsl \
  -s:UBL.xml -o:UBL.xml \
  gc-uri=target/UBL-Entities-2.5.gc

# Verify no mismatches
ant -Ddir=target -consistency-check
```

## Quick Reference: DEN Examples

Common Dictionary Entry Names you might reference:

| Element | DEN (for @remap) |
|---------|------------------|
| Invoice ABIE | `Invoice. Details` |
| Period ABIE | `Period. Details` |
| Party ABIE | `Party. Details` |
| PartyName ABIE | `Party Name. Details` |
| SupplierParty ABIE | `Supplier Party. Details` |
| MonetaryTotal ABIE | `Monetary Total. Details` |

Note: Always include the space after the dot!
