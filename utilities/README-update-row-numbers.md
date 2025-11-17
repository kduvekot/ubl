# Auto-Update Row Numbers in UBL.xml

Quick guide for maintaining row number references in UBL documentation.

## When to Use

Any time you edit `UBL.xml` and need to reference elements from the model spreadsheets.

## Quick Start

### Adding a New Reference

1. **Use `0` as placeholder:**
   ```xml
   <ulink role="DEN-Row" remap="Party. Details">0</ulink>
   ```

2. **Get the DEN** (Dictionary Entry Name):
   - Open `mod/summary/reports/UBL-Invoice-2.5.html`
   - Find your element
   - URL anchor shows: `#Table-Party.Details`
   - Use: `Party. Details` (with space!)

3. **Run auto-update:**
   ```bash
   java -jar utilities/saxon9he/saxon9he.jar \
     -xsl:utilities/update-ubl-row-numbers.xsl \
     -s:UBL.xml -o:UBL.xml \
     gc-uri=UBL-Entities-2.5.gc
   ```

4. **Verify** - you'll see:
   ```
   Updated: Party. Details (0 → 1744)
   ```

## Common DENs

| Element | Use in @remap |
|---------|---------------|
| Invoice | `Invoice. Details` |
| Period | `Period. Details` |
| Party | `Party. Details` |
| Party Name | `Party Name. Details` |
| Supplier Party | `Supplier Party. Details` |
| Customer Party | `Customer Party. Details` |
| Monetary Total | `Monetary Total. Details` |
| Payable Amount | `Monetary Total. Payable_ Amount. Amount` |

**Important:** Always include the space after the dot!

## Error: DEN Not Found

```
ERROR: DEN not found in .gc file: "Partty. Details"
```

**Fix:**
1. Check spelling in `@remap` attribute
2. Verify the DEN exists in the .gc file:
   ```bash
   grep -i "party" UBL-Entities-2.5.gc | grep DictionaryEntryName
   ```
3. Make sure you have space after dot: `"Party. Details"` not `"Party.Details"`

## Full Documentation

See `../AUTOMATION-PROPOSAL.md` for complete details on the automation solution.
