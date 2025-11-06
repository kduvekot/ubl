# UBL Build Troubleshooting Guide

Common issues and their solutions when working with the UBL repository.

## Build Failures

### Build Exits Without Creating Console Log

**Symptoms:**
- No `build.console.*.txt` file in archive directory
- Build appears to hang or terminate unexpectedly

**Causes:**
- Ant startup failure
- Java classpath issues
- Missing dependencies

**Solutions:**

1. **Check Java Version:**
```bash
java -version
# Should be 1.8.x
```

2. **Verify Java Installation:**
```bash
which java
echo $JAVA_HOME
```

3. **Check Ant Files:**
```bash
ls -lh utilities/ant/lib/ant-launcher.jar
```

4. **Run Ant Directly:**
```bash
java -Dant.home=utilities/ant \
  -classpath utilities/saxon/saxon.jar:utilities/ant/lib/ant-launcher.jar:utilities/saxon9he/saxon9he.jar \
  org.apache.tools.ant.launch.Launcher \
  -buildfile build-py.xml
```

5. **Check System Dependencies:**
```bash
# Ubuntu/Debian
sudo apt install -y openjdk-8-jdk aspell libreoffice pandoc

# macOS
brew install openjdk@8 aspell libreoffice pandoc
```

### Saxon Transform.class Not Found

**Symptoms:**
```
Exception in thread "main" java.lang.NoClassDefFoundError: net/sf/saxon/Transform
```

**Causes:**
- Corrupted Saxon JAR
- Wrong Saxon version
- Classpath misconfiguration

**Solutions:**

1. **Verify Saxon JAR Contents:**
```bash
jar tf utilities/saxon9he/saxon9he.jar | grep net/sf/saxon/Transform.class
```

2. **Check File Size:**
```bash
ls -lh utilities/saxon9he/saxon9he.jar
# Should be several MB (not 0 bytes)
```

3. **Re-download Saxon:**
```bash
# Backup old version
mv utilities/saxon9he/saxon9he.jar utilities/saxon9he/saxon9he.jar.bak

# Download fresh copy (from official source or repository maintainer)
# Then verify integrity
```

4. **Test Saxon Directly:**
```bash
java -cp utilities/saxon9he/saxon9he.jar net.sf.saxon.Transform -?
# Should display help text
```

### LibreOffice Conversion Fails

**Symptoms:**
- Build hangs at ODS conversion step
- Error: "LibreOffice not found"
- ODS files not processing

**Causes:**
- LibreOffice not installed
- Headless mode not available
- Permission issues

**Solutions:**

1. **Install LibreOffice:**
```bash
# Ubuntu/Debian
sudo apt install -y libreoffice

# macOS
brew install --cask libreoffice
```

2. **Test Headless Mode:**
```bash
libreoffice --headless --convert-to pdf test.odt
```

3. **Check Display Variable (Linux):**
```bash
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### Out of Memory Errors

**Symptoms:**
```
java.lang.OutOfMemoryError: Java heap space
```

**Causes:**
- Large XSLT transformations
- Insufficient Java memory allocation

**Solutions:**

1. **Increase Java Heap:**
Edit `build.py` or `build-py.xml` to add JVM args:
```python
# In build.py, add to java command
"-Xmx2048m",  # 2GB heap
"-Xms512m",   # 512MB initial
```

2. **Monitor Memory Usage:**
```bash
# During build
top -p $(pgrep -f 'java.*ant')
```

3. **Close Other Applications:**
Free up system memory before building.

## Validation Failures

### Schema Validation Errors

**Symptoms:**
```
Element 'ElementName' is not allowed
```

**Debugging Steps:**

1. **Check Spreadsheet:**
- Verify component definition exists
- Check cardinality is correct
- Verify data type is valid

2. **Check Generated Schema:**
```bash
grep "ElementName" target/.../xsd/**/*.xsd
```

3. **Compare with Previous Version:**
```bash
diff UBL-Entities-2.4-os.gc UBL-Entities-2.5.gc | grep ElementName
```

4. **Validate Sample Manually:**
```bash
xmllint --noout --schema target/.../xsd/maindoc/UBL-*.xsd raw/xml/sample.xml
```

### Sample Instance Invalid

**Symptoms:**
- `UNEXPECTED-TEST-RESULT-WARNING.txt` appears
- Sample validation fails

**Common Issues:**

1. **Namespace Mismatch:**
```xml
<!-- Wrong: -->
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2.4">

<!-- Correct for UBL 2.5: -->
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
```

2. **Missing Required Elements:**
Check schema for minOccurs="1" elements and ensure all are present in sample.

3. **Invalid Date/Time Formats:**
```xml
<!-- Wrong: -->
<IssueDate>11/06/2025</IssueDate>

<!-- Correct (ISO 8601): -->
<IssueDate>2025-11-06</IssueDate>
```

4. **Invalid Code Values:**
Check code lists in `raw/cl/gc/` for valid values.

### Genericode Validation Errors

**Symptoms:**
- `LIST-OF-PROBLEM-CODE-LISTS.txt` appears

**Solutions:**

1. **Check File Contents:**
```bash
cat target/*/LIST-OF-PROBLEM-CODE-LISTS.txt
```

2. **Validate Genericode File:**
```bash
xmllint --noout --schema utilities/Crane-gc2obdndr/genericode-*.xsd raw/cl/gc/problem-file.gc
```

3. **Common Genericode Issues:**
- Missing `<Identification>` section
- Invalid column references
- Duplicate code values
- Malformed XML

4. **Regenerate from Master:**
```bash
# Run code list tooling from master-code-list-UBL-*.xml
```

## Spreadsheet Issues

### Cannot Download Spreadsheet

**Symptoms:**
- Build fails with HTTP 403 or 404
- "Cannot access Google Spreadsheet"

**Causes:**
- Spreadsheet not publicly accessible
- Invalid URL
- Network issues

**Solutions:**

1. **Check Spreadsheet Sharing:**
- Open URL in browser
- Verify "Anyone with link can view"
- Check URL doesn't require sign-in

2. **Verify URL Format:**
```python
# Correct:
"https://docs.google.com/spreadsheets/d/SPREADSHEET_ID"

# Wrong (has /edit):
"https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit#gid=0"
```

3. **Manual Download Workaround:**
```bash
# Download ODS manually from Google Sheets
# Place in parent directory:
cp ~/Downloads/UBL-Library-Google.ods ../
cp ~/Downloads/UBL-Documents-Google.ods ../
cp ~/Downloads/UBL-Signature-Google.ods ../

# Build will use local files instead
python build.py target local debug

# Remember to delete after:
rm ../*-Google.ods
```

4. **Use Cached Version:**
Extract ODS files from previous build's archive-only package.

### Spreadsheet Data Errors

**Symptoms:**
- Strange component names
- Missing definitions
- Incorrect cardinality

**Solutions:**

1. **Check for Special Characters:**
- Remove non-ASCII characters
- Check for hidden formatting
- Verify cell contents match expectations

2. **Verify Column Headers:**
Ensure spreadsheet has expected columns in correct order.

3. **Check for Merged Cells:**
Unmerge any merged cells - they confuse the converter.

4. **Compare with Previous Version:**
Open both current and previous spreadsheet side-by-side.

## Documentation Issues

### Hub Document Validation Fails

**Symptoms:**
- `INVALID-ASSEMBLED-HUB-XML.txt` appears

**Debugging:**

1. **Read Error File:**
```bash
cat target/*/INVALID-ASSEMBLED-HUB-XML.txt
```

2. **Validate Hub Directly:**
```bash
xmllint --noout --schema db/spec-0.8/docbook/docbook.xsd UBL.xml
```

3. **Common DocBook Errors:**
- Unclosed tags: `<para>text` (missing `</para>`)
- Invalid elements: `<invalid>` not in DocBook schema
- Entity reference errors: `&missing-entity;`
- Nested structure violations

4. **Check Entity Files:**
```bash
# Verify entity files exist and are valid XML
xmllint --noout summary-*-ent.xml
```

5. **Preview in Browser:**
Use browser preview to identify rendering issues (see CLAUDE.md for instructions).

### Missing Entity Files

**Symptoms:**
- Build warning about missing entities
- `ATTENTION-new-entities.txt` appears

**Solution:**

```bash
# Check for new entities
ls target/*/archive-only/new-entities/

# Copy to repository root
cp target/*/archive-only/new-entities/*.xml .

# Commit the updated entities
git add *-ent.xml
git commit -m "Update auto-generated entity files"
```

### Spell Check Warnings

**Symptoms:**
- `NDR-SPELL-CHECK-WARNING.txt` appears

**Solutions:**

1. **Review Unexpected Words:**
```bash
cat unexpectedWords.txt
```

2. **Add Valid Words to Dictionary:**
```bash
echo "NewValidWord" >> spellcheck-UBL.txt
sort -u spellcheck-UBL.txt -o spellcheck-UBL.txt
```

3. **Fix Actual Misspellings:**
Edit UBL.xml to correct typos.

4. **Ignore Technical Terms:**
Add to `spellcheck-UBL.txt` if legitimate technical terminology.

## Git Issues

### Cannot Push to GitHub

**Symptoms:**
```
error: failed to push some refs
HTTP 403 Forbidden
```

**Causes:**
- Branch name doesn't match required pattern
- Missing session ID in branch name
- Pushing to protected branch

**Solutions:**

1. **Check Branch Name:**
```bash
git branch --show-current
# Should be: claude/{description}-{session-id}
```

2. **Create Proper Feature Branch:**
```bash
git checkout -b claude/my-feature-$(date +%s)
git push -u origin claude/my-feature-$(date +%s)
```

3. **Don't Push to main/master:**
```bash
# Use pull requests instead
git checkout -b feature-branch
# Make changes
git push -u origin feature-branch
# Create PR on GitHub
```

### Merge Conflicts

**Symptoms:**
```
CONFLICT (content): Merge conflict in file.xml
```

**Resolution:**

1. **Identify Conflicts:**
```bash
git status
# Lists files with conflicts
```

2. **Edit Files:**
```xml
<<<<<<< HEAD
Current version
=======
Incoming version
>>>>>>> branch-name
```

Choose correct version or merge both.

3. **Mark Resolved:**
```bash
git add resolved-file.xml
git commit
```

4. **For Binary Files:**
```bash
# Choose one version
git checkout --ours binary-file.gc   # Keep local
# or
git checkout --theirs binary-file.gc # Use incoming
git add binary-file.gc
```

### Accidentally Committed Auto-Generated Files

**Symptoms:**
- `*-ent.xml` files in commit
- Genericode files committed when they shouldn't be

**Solution:**

```bash
# Remove from staging
git reset HEAD *-ent.xml

# If already committed
git reset --soft HEAD~1
git reset HEAD *-ent.xml
git commit -m "Your original commit message (minus auto-generated files)"
```

## Performance Issues

### Build Takes Very Long

**Normal:** 10-30 minutes local, 25-35 minutes GitHub Actions

**If Much Slower:**

1. **Check Network:**
- Slow spreadsheet download
- Réalta API timeouts

2. **System Resources:**
```bash
# Check CPU usage
top

# Check disk I/O
iostat

# Check memory
free -h
```

3. **Optimize:**
- Close other applications
- Use local ODS files (cache)
- Skip Réalta publishing for intermediate builds
- Build on SSD, not network drive

### GitHub Actions Timeout

**Symptoms:**
- Workflow cancelled after 6 hours (GitHub limit)
- Build doesn't complete

**Solutions:**

1. **Check Workflow Status:**
- Look for hanging steps
- Check if Réalta is responding

2. **Simplify Build:**
- Reduce concurrent operations
- Split into multiple jobs if possible

3. **Retry:**
Sometimes network issues - re-run workflow.

## Platform-Specific Issues

### Windows: Line Endings

**Symptoms:**
- Scripts don't run
- `^M` characters appear

**Solution:**

```bash
# Configure git
git config core.autocrlf true

# Convert file
dos2unix script.sh
# or
sed -i 's/\r$//' script.sh
```

### macOS: Java Issues

**Symptoms:**
- Java not found
- Wrong Java version

**Solution:**

```bash
# Install Java 8
brew install openjdk@8

# Set JAVA_HOME
export JAVA_HOME=/Library/Java/JavaVirtualMachines/openjdk-8.jdk/Contents/Home

# Add to .zshrc or .bash_profile
echo 'export JAVA_HOME=/Library/Java/JavaVirtualMachines/openjdk-8.jdk/Contents/Home' >> ~/.zshrc
```

### Linux: Missing Libraries

**Symptoms:**
- `libreoffice: error while loading shared libraries`

**Solution:**

```bash
# Install missing dependencies
sudo apt install -y libreoffice-core libreoffice-writer libreoffice-calc

# Or full suite
sudo apt install -y libreoffice
```

## Getting Help

### Before Asking

1. **Check console log:**
```bash
cat target/*/archive-only/build.console.*.txt | less
```

2. **Check error files:**
```bash
ls target/**/*WARNING*.txt target/**/*PROBLEMS*.txt
```

3. **Review this guide:** Most issues covered here

4. **Search commit history:**
```bash
git log --grep="keyword"
```

### Where to Ask

1. **CLAUDE.md**: Check repository configuration
2. **README.md**: Comprehensive documentation
3. **UBL TC Mailing List**: Committee members
4. **GitHub Issues**: Report bugs
5. **OASIS Support**: Infrastructure issues

### Information to Provide

When reporting issues:

```
1. Operating System:
2. Java version: java -version
3. Python version: python --version
4. Branch: git branch --show-current
5. Build command used:
6. Error message (full):
7. Console log (relevant excerpt):
8. Steps to reproduce:
9. Expected vs actual behavior:
```

### Emergency Recovery

**Repository corrupted:**
```bash
# Clone fresh
git clone https://github.com/oasis-tcs/ubl.git ubl-fresh
cd ubl-fresh
git checkout your-branch
```

**Lost uncommitted work:**
```bash
# Check reflog
git reflog

# Recover
git checkout commit-hash
git checkout -b recovery-branch
```

**Build artifacts corrupted:**
```bash
# Clean everything
rm -rf target/
git clean -fdx  # WARNING: Deletes all untracked files!

# Rebuild
python build.py target local debug
```

## Prevention

### Best Practices

1. **Always test locally before pushing**
2. **Commit frequently, small chunks**
3. **Keep build configuration synced (build.py + build.sh)**
4. **Don't edit auto-generated files**
5. **Back up work before major changes**
6. **Use feature branches**
7. **Read error messages carefully**
8. **Keep dependencies updated**

### Pre-Flight Checklist

Before committing/pushing:

- [ ] Local build successful
- [ ] No error .txt files in output
- [ ] Validation tests pass
- [ ] No auto-generated files staged
- [ ] Commit message clear and descriptive
- [ ] Changes tested thoroughly
- [ ] Documentation updated if needed

---

**Still stuck?** Use `/build-local`, `/validate-schemas`, or other slash commands for guided troubleshooting.
