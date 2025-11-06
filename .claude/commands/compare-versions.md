# Compare UBL Versions

Compare two UBL versions or stages to understand changes, additions, and deletions in the data model.

## Usage

Invoke with comparison arguments:
```
/compare-versions 2.4 vs 2.5
/compare-versions csd01 vs csd02
/compare-versions $ARGUMENTS
```

## Instructions

### Step 1: Parse Comparison Request

If arguments provided in `$ARGUMENTS`, parse them:
- Extract version/stage identifiers
- Determine if comparing versions (2.4 vs 2.5) or stages (csd01 vs csd02)
- Handle various formats: "X vs Y", "X to Y", "X and Y", "compare X Y"

If no arguments, ask the user:
```
What would you like to compare?
1. Two versions (e.g., 2.4 vs 2.5)
2. Two stages (e.g., csd01 vs csd02)
3. Current version vs previous version
4. Current stage vs previous stage
```

### Step 2: Determine Comparison Context

Read current build configuration from `build.py`:
- `ubl_version` - Current version
- `ubl_stage` - Current stage
- `ubl_prev_version` - Previous version
- `ubl_prev_stage` - Previous stage

Display context:
```
Current Configuration:
Version: {ubl_version}, Stage: {ubl_stage}
Previous Version: {ubl_prev_version}, Stage: {ubl_prev_stage}
```

### Step 3: Identify Comparison Type

Determine what's being compared:

**Type A: Version Comparison** (e.g., 2.4 vs 2.5)
- Major model changes
- New document types
- Modified component structures
- Backward compatibility issues

**Type B: Stage Comparison** (e.g., csd01 vs csd02)
- Incremental changes within same version
- Bug fixes
- Model refinements
- Editorial corrections

### Step 4: Locate Comparison Files

Build process generates comparison reports. Look for:

#### For Version Comparison:
```bash
find target -name "check-ubl-${current_version}-${current_stage}-ubl-${prev_version}.html"
```
Also check for entity files:
```bash
find . -name "old2newDoc-from-previous-version-*.xml"
```

Expected files:
- `old2newDoc-from-previous-version-documents-ent.xml`
- `old2newDoc-from-previous-version-library-ent.xml`

#### For Stage Comparison:
```bash
find target -name "check-ubl-${version}-${current_stage}-ubl-${version}-${prev_stage}.html"
```
Also check for entity files:
```bash
find . -name "old2newDoc-from-previous-stage-*.xml"
```

Expected files:
- `old2newDoc-from-previous-stage-documents-ent.xml`
- `old2newDoc-from-previous-stage-library-ent.xml`

### Step 5: Check if Files Exist

If comparison files exist:
- Read and parse HTML reports
- Extract key statistics
- Summarize changes

If files don't exist:
```
⚠ Comparison files not found.

These files are generated during the build process.

Options:
1. Run a build to generate comparison reports: /build-local
2. Check if build completed successfully
3. Verify build artifacts in target/ directory
```

Offer to run build: **"Run build now to generate comparison reports?"**

### Step 6: Parse HTML Comparison Report (if available)

If HTML report exists, extract:

**Summary Statistics:**
- Total components in old version
- Total components in new version
- Net change (added - deleted)
- Number of added components
- Number of deleted components
- Number of modified components
- Number of unchanged components

**Added Components:**
- List new document types
- List new library components
- Note any new namespaces

**Deleted Components:**
- List removed documents
- List removed components
- Note deprecation warnings

**Modified Components:**
- Components with changed cardinality
- Components with changed data types
- Components with updated definitions
- Structural changes

### Step 7: Parse Entity XML Files (if available)

Read the `old2newDoc-from-previous-*-ent.xml` files if they exist.

These are XML entity files containing structured comparison data.

Look for patterns like:
```xml
<!ENTITY component-name "
<row>
  <entry>Component</entry>
  <entry>Change type</entry>
  <entry>Description</entry>
</row>
">
```

Extract and format for user display.

### Step 8: Compare Genericode Files

If comparing versions, check genericode files:

```bash
# Current version
ls -lh UBL-Entities-${current_version}.gc 2>/dev/null

# Previous version
ls -lh UBL-Entities-${prev_version}-os.gc 2>/dev/null
```

Display file sizes and modification dates for comparison.

### Step 9: Generate Summary Report

Create comprehensive comparison report:

```
=== UBL Version Comparison Report ===

Comparing: UBL {old_version} {old_stage} → UBL {new_version} {new_stage}
Comparison Type: {Version/Stage} comparison
Generated: {date}

--- Overall Statistics ---
Previous: {N} components
Current:  {M} components
Net Change: {+/- X} components

--- Breakdown ---
Added:       {count} components
Deleted:     {count} components
Modified:    {count} components
Unchanged:   {count} components

--- Notable Changes ---
{List most significant changes}

--- New Document Types ---
{List new documents if any}

--- Deprecated Components ---
{List deprecated items if any}

--- Backward Compatibility ---
{Analysis of breaking changes}

--- Recommendation ---
{Upgrade notes or migration guidance}
```

### Step 10: Detailed Change Analysis

For each category, provide details:

#### Added Components
```
New Components in UBL {version}:
--------------------------------
1. {ComponentName}
   Type: {ABIE/BBIE/ASBIE}
   Location: {Document/Library}
   Description: {Brief description}
   Impact: {How this affects users}

2. {Next component...}
```

#### Deleted Components
```
Removed Components from UBL {version}:
--------------------------------------
1. {ComponentName}
   Reason: {Why removed}
   Migration: {Alternative component or approach}
   Impact: {Breaking change severity}
```

#### Modified Components
```
Changed Components in UBL {version}:
------------------------------------
1. {ComponentName}
   Change: {What changed}
   Before: {Old definition}
   After: {New definition}
   Impact: {Compatibility notes}
```

### Step 11: Check Schema File Differences

For technical comparison, offer to check schema differences:

```bash
# List schema files in both versions
find raw/xsd -name "*.xsd" -type f | sort

# If old version available, compare
find os-UBL-${prev_version}/xsd -name "*.xsd" 2>/dev/null
```

Offer: **"Generate detailed schema file diff?"**

If yes, use git or diff to compare schema files:
```bash
diff -u os-UBL-${prev_version}/xsd/common/UBL-CommonBasicComponents-*.xsd \
        raw/xsd/common/UBL-CommonBasicComponents-*.xsd
```

Summarize technical differences.

### Step 12: Check Documentation Changes

Compare hub documents if available:

```bash
# Current hub
ls -lh UBL.xml

# Previous version hub (if exists)
ls -lh UBL-${prev_version}.xml 2>/dev/null
```

Note changes in:
- Specification structure
- Examples and use cases
- Code lists
- Namespace declarations

### Step 13: Code List Comparison

Compare code lists between versions:

```bash
# Current code lists
find raw/cl -name "*.gc" -o -name "master-code-list*.xml"

# Previous version code lists
find os-UBL-${prev_version}/cl -name "*.gc" 2>/dev/null
```

Report:
- New code lists added
- Modified code lists
- New code values in existing lists

### Step 14: Sample Instance Changes

Check if sample instances changed:

```bash
# Count samples
find raw/xml -name "*.xml" | wc -l
find raw/json -name "*.json" | wc -l
```

Compare with previous version if available.

### Step 15: Provide Actionable Insights

Based on comparison, provide recommendations:

**For Implementers:**
```
Migration Guidance:
-------------------
- Mandatory changes: {list breaking changes}
- Optional enhancements: {list new features}
- Deprecated usage: {list items to phase out}
- Testing focus: {areas requiring thorough testing}
```

**For Standards Committee:**
```
Review Points:
--------------
- Significant structural changes: {count}
- Backward compatibility: {assessment}
- Documentation completeness: {status}
- Sample coverage: {adequacy}
```

## Comparison Scenarios

### Scenario 1: Current vs Previous Stage
```
/compare-versions current stage vs previous stage
```
Shows incremental changes during development.

### Scenario 2: Major Version Upgrade
```
/compare-versions 2.4 vs 2.5
```
Shows all changes for major release.

### Scenario 3: Multiple Stage Evolution
```
/compare-versions csd01 vs cs01
```
Shows cumulative changes across stages.

### Scenario 4: Historical Comparison
```
/compare-versions 2.2 vs 2.5
```
Shows evolution over multiple versions.

## Expected Output Formats

### Console Summary (default)
Brief text summary suitable for terminal display.

### Detailed Report (optional)
Ask: **"Generate detailed markdown report?"**

If yes, create comprehensive markdown file:
```
comparison-UBL-{old}-{new}-{timestamp}.md
```

### HTML Report (from build)
If HTML exists, offer to open:
**"Open HTML comparison report in browser? (file://...)"**

## Troubleshooting

### No comparison files available
**Solution:** Run build process to generate comparison artifacts

### Comparison looks empty
**Possible causes:**
- No changes between versions
- Comparison files corrupted
- Wrong version/stage specified

### Cannot access previous version
**Solution:** Ensure previous version genericode files exist:
- `UBL-Entities-{prev_version}-os.gc`
- `UBL-Signature-Entities-{prev_version}-os.gc`

### Comparison shows unexpected changes
**Possible causes:**
- Spreadsheet formatting issues
- Model refactoring
- Component renaming

## Advanced Options

### Generate Custom Comparison
```bash
# Using genericode files
utilities/Crane-gc2obdndr/compare-gc.xsl \
  UBL-Entities-2.4-os.gc \
  UBL-Entities-2.5.gc
```

### Export Comparison Data
Offer to export structured comparison data:
- JSON format for automated processing
- CSV for spreadsheet analysis
- XML for integration with other tools

## Notes

- Comparison files generated automatically during build
- HTML reports include detailed tables and statistics
- Entity files used in hub document generation
- Always verify comparison against actual schema files
- Consider both technical and business impact of changes
- Stage comparisons typically show fewer changes than version comparisons
