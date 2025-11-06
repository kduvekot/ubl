# UBL Branch Strategy and Release Process

## Overview

The UBL repository uses a branch-based workflow to manage multiple versions, stages, and parallel development efforts. This document explains the branching strategy, naming conventions, and release progression.

## Branch Types

### 1. Release Branches
**Format:** `ubl-{version}-{stage}`

**Examples:**
- `ubl-2.5-csd01` - UBL 2.5 Committee Specification Draft 01
- `ubl-2.5-cs01` - UBL 2.5 Committee Specification 01
- `ubl-2.4-os` - UBL 2.4 OASIS Standard

**Purpose:**
- Represent official stages in OASIS TC Process
- Long-lived branches maintained throughout version lifecycle
- Each stage builds upon previous stage

**Characteristics:**
- Protected from direct pushes (use PRs)
- Contain complete, buildable code
- Tagged at publication milestones
- Archived after OASIS Standard publication

### 2. Feature Branches
**Format:** `claude/{description}-{session-id}`

**Examples:**
- `claude/fix-invoice-schema-abc123def`
- `claude/add-catalog-document-xyz789ghi`
- `claude/update-spreadsheet-urls-jkl456mno`

**Purpose:**
- Individual development work
- Pull request targets
- Short-lived (merged and deleted after PR acceptance)

**Characteristics:**
- Created from release branches
- Must start with `claude/` prefix
- Must end with session ID (for authentication)
- Merged via pull request

### 3. Main Branch
**Format:** `main` or `master`

**Purpose:**
- Default repository branch
- Contains latest approved work
- Merges from release branches at major milestones
- Snapshot for public reference

**Characteristics:**
- Protected (no direct commits)
- Updated only via PR from release branches
- Represents "current stable state"
- May not be actively developed (release branches are active)

### 4. Experimental Branches
**Format:** `{username}/{experiment}` or `{feature}-experimental`

**Examples:**
- `ubl-2.5-python` - Python build system migration
- `john/json-schema-v2` - JSON schema improvements
- `subcommittee-tsc` - Transportation Subcommittee branch

**Purpose:**
- Major refactoring or new features
- Testing alternative approaches
- Subcommittee work products

**Characteristics:**
- May diverge significantly from release branches
- Not subject to same protection rules
- Eventually merged or archived

## Stage Progression

UBL follows OASIS Technical Committee Process stages:

### Committee Specification Drafts (CSD)
**Sequence:** csd01 → csd02 → csd03 → ... → csdNN

**Purpose:** Iterative development and refinement

**Characteristics:**
- Incremental changes between drafts
- Internal TC review and approval
- Model changes allowed
- Multiple drafts typical (5-10+ common)

**Branch Progression:**
```
ubl-2.5-csd01 → ubl-2.5-csd02 → ubl-2.5-csd03 → ...
```

**Transition Criteria:**
- TC member contributions incorporated
- Build successful
- No critical issues
- TC vote to publish draft

### Committee Specification (CS)
**Sequence:** cs01 → cs02 (rarely needed)

**Purpose:** Stable specification for public review

**Characteristics:**
- Public review period (typically 30-60 days)
- Minimal changes (editorial only preferred)
- Requires formal TC approval
- Significant milestone

**Branch Progression:**
```
ubl-2.5-csd05 → ubl-2.5-cs01
```

**Transition Criteria:**
- All CSD issues resolved
- TC vote to approve CS
- Public review completed
- Feedback incorporated (if requiring cs02)

### OASIS Standard (OS)
**Format:** `os` (no number, only one per version)

**Purpose:** Final, approved standard

**Characteristics:**
- No further technical changes
- Permanent, immutable
- Officially published by OASIS
- Reference implementation

**Branch Progression:**
```
ubl-2.5-cs01 → ubl-2.5-os
```

**Transition Criteria:**
- Successful public review
- TC and Board approval
- Final editorial review
- OASIS publication requirements met

## Version Progression

### Major Versions
**Format:** X.Y (e.g., 2.4 → 2.5)

**When to Create:**
- Significant new functionality
- Model restructuring
- Potential breaking changes
- New document types

**Process:**
1. Create new branch: `git checkout -b ubl-2.5-csd01 ubl-2.4-os`
2. Update version in configuration files
3. Copy and update all version-specific files
4. Create new Google Spreadsheets
5. Progress through stage sequence

### Minor Versions
UBL does not use minor versions (e.g., 2.5.1). Instead:
- Corrections published as Errata
- Significant fixes trigger new stage (rare)

## Branching Workflows

### Creating New Stage

**Scenario:** Moving from CSD01 to CSD02

```bash
# Start from previous stage
git checkout ubl-2.5-csd01

# Create new stage branch
git checkout -b ubl-2.5-csd02

# Update configuration
# Edit build.py and build.sh
#   ubl_stage = "csd02"
#   ubl_prev_stage = "csd01"

# Update UBL.xml entities
# Edit UBL.xml internal DTD subset

# Rename genericode files
mv UBL-Entities-2.5.gc UBL-Entities-2.5-csd01.gc
mv UBL-Signature-Entities-2.5.gc UBL-Signature-Entities-2.5-csd01.gc

# Copy and rename spreadsheets in Google Sheets
# Update URLs in build.py and build.sh

# Commit
git add build.py build.sh UBL.xml
git commit -m "Initialize UBL 2.5 CSD02"

# Push
git push -u origin ubl-2.5-csd02
```

### Creating New Version

**Scenario:** Starting UBL 2.6 after 2.5 OS

```bash
# Start from previous version OASIS Standard
git checkout ubl-2.5-os

# Create new version branch
git checkout -b ubl-2.6-csd01

# Update configuration (all version references)
# Edit build.py, build.sh, config-UBL.xml, etc.

# Update XSD schema fragments (all 8 files in raw/xsd/common/)
# Update version= attributes and comments

# Update JSON schema fragments

# Create new Google Spreadsheets

# Copy previous version genericode files
cp UBL-Entities-2.5.gc UBL-Entities-2.5-os.gc
cp UBL-Signature-Entities-2.5.gc UBL-Signature-Entities-2.5-os.gc

# Update CVA and validation scripts

# Commit
git add .
git commit -m "Initialize UBL 2.6 CSD01"

# Push
git push -u origin ubl-2.6-csd01
```

### Feature Development

**Scenario:** Adding new document type

```bash
# Create feature branch from target release branch
git checkout ubl-2.5-csd02
git checkout -b claude/add-catalog-document-abc123def

# Make changes
# Edit spreadsheets
# Add samples
# Update documentation

# Test locally
python build.py target local debug

# Commit and push
git add .
git commit -m "Add Catalog document type

- Add Catalog to Documents spreadsheet
- Create sample instance
- Update schema summary documentation
- Add validation tests
"

git push -u origin claude/add-catalog-document-abc123def

# Create pull request to ubl-2.5-csd02
# After approval and merge, delete feature branch
```

### Hotfix / Correction

**Scenario:** Fixing critical error in published CS

```bash
# Branch from affected stage
git checkout ubl-2.5-cs01
git checkout -b claude/fix-invoice-date-xyz789ghi

# Make minimal fix
# Edit affected files only

# Test thoroughly
python build.py target local debug
cd raw/val && ./test.sh && ./testsamples.sh

# Commit with detailed explanation
git add .
git commit -m "Fix Invoice due date cardinality

Issue: Due date marked as required (1..1) but should be optional (0..1)
Impact: Existing invoices without due date now validate
Compatibility: Non-breaking change (relaxes constraint)

Fixes #123
"

git push -u origin claude/fix-invoice-date-xyz789ghi

# Create pull request
# Request expedited review
# After merge, may trigger cs02 publication
```

## Pull Request Workflow

### Creating Pull Request

1. **Prepare branch:**
   - Ensure all tests pass
   - Run local build successfully
   - Review changes with git diff
   - Write clear commit messages

2. **Push branch:**
   ```bash
   git push -u origin claude/{description}-{session}
   ```

3. **Open PR:**
   - Target: Appropriate release branch (e.g., ubl-2.5-csd02)
   - Title: Brief summary of changes
   - Description: Detailed explanation, rationale, testing done
   - Reviewers: Assign TC editors/maintainers

4. **PR Description Template:**
   ```markdown
   ## Summary
   [Brief description of changes]

   ## Changes Made
   - [Specific change 1]
   - [Specific change 2]

   ## Testing
   - [ ] Local build successful
   - [ ] Validation tests pass
   - [ ] Sample instances validate
   - [ ] Documentation builds correctly

   ## Impact
   [Breaking/Non-breaking, affected components]

   ## Related Issues
   Fixes #123, Relates to #456
   ```

### Reviewing Pull Request

**Reviewer Checklist:**
- [ ] Changes align with UBL design principles
- [ ] Build completes successfully
- [ ] No auto-generated files committed
- [ ] Documentation updated
- [ ] Tests added/updated for changes
- [ ] Backward compatibility considered
- [ ] Follows coding standards

**Review Process:**
1. Check out PR branch locally
2. Run build: `python build.py target local debug`
3. Review generated artifacts
4. Test specific scenarios
5. Provide feedback or approve

### Merging Pull Request

**Merge Strategy:** Squash and merge (preferred) or Merge commit

**Post-Merge:**
1. Delete feature branch
2. Verify CI passes on target branch
3. Update any tracking issues
4. Notify TC if significant change

## Maintenance Guidelines

### Active Development

**Current Stage Branches:**
- Actively developed
- Accept pull requests
- Regular builds and testing
- Frequent commits

**Example:** `ubl-2.5-csd02` (current work)

### Stable Branches

**Published CS Branches:**
- Minimal changes (critical fixes only)
- Require strong justification
- Thorough testing mandatory
- May trigger new CS revision

**Example:** `ubl-2.5-cs01` (published, in review)

### Archived Branches

**OASIS Standard Branches:**
- Read-only (effectively)
- No changes except errata
- Reference implementation
- Permanent record

**Example:** `ubl-2.4-os` (published standard)

## Subcommittee Branches

Subcommittees create customized branches for specialized work products.

**Format:** `ubl-{version}-{stage}-{subcommittee}`

**Example:** `ubl-2.5-csd01-tsc` (Transportation Subcommittee)

**Characteristics:**
- Independent configuration (build.py, spreadsheets)
- Custom package names (e.g., UBL-2.5-TSC)
- Merged into main TC branch via PR when ready
- May have different release schedule

**Setup Process:**
1. Branch from TC version
2. Update title and package in build config
3. Copy and customize spreadsheets
4. Develop subcommittee-specific content
5. Submit PR to TC for inclusion

## Best Practices

### Branching
- Always branch from appropriate release branch
- Use descriptive branch names
- Include session ID in feature branches
- Delete merged feature branches

### Committing
- Atomic commits (one logical change)
- Clear, descriptive messages
- Reference issues/PRs when applicable
- Test before committing

### Merging
- Prefer squash merge for feature branches
- Keep release branch history clean
- Ensure CI passes before merge
- Update documentation

### Communication
- Announce new stage branches on TC mailing list
- Coordinate large changes with TC
- Document rationale for significant changes
- Update CLAUDE.md when branches change

## Branch Protection

### Protected Branches
- `main`
- `master`
- `ubl-*-os` (OASIS Standard branches)

### Protection Rules
- Require pull request reviews
- Require status checks to pass
- No force pushes
- No deletions

### Override Permissions
- TC Chairs
- Designated Editors
- Repository Administrators

## Disaster Recovery

### Corrupted Branch
```bash
# Reset to known good commit
git reset --hard <commit-hash>

# Force push (with permission)
git push --force origin <branch-name>
```

### Lost Branch
```bash
# Recover from reflog
git reflog
git checkout -b recovered-branch <commit-hash>
```

### Merge Conflict Resolution
```bash
# During merge
git merge ubl-2.5-csd01
# Fix conflicts
git add resolved-files
git commit
```

## References

- OASIS TC Process: https://www.oasis-open.org/policies-guidelines/tc-process
- Git Branching Models: https://nvie.com/posts/a-successful-git-branching-model/
- UBL TC Charter: https://www.oasis-open.org/committees/ubl/charter.php
