# Claude Code Configuration for UBL Repository

This directory contains Claude Code configuration, custom commands, hooks, and documentation specifically tailored for the OASIS UBL standard development repository.

## Directory Structure

```
.claude/
├── CLAUDE.md                   # Auto-loaded project context (READ THIS FIRST!)
├── settings.json               # Tool permissions and project config
├── .gitignore                  # Files to exclude from git
├── README.md                   # This file
│
├── commands/                   # Custom slash commands
│   ├── build-local.md         # Build locally with validation
│   ├── create-release.md      # Create new version/stage
│   ├── validate-schemas.md    # Run schema validation
│   ├── analyze-spreadsheet.md # Analyze Google spreadsheets
│   └── compare-versions.md    # Compare UBL versions
│
├── hooks/                      # Event hooks
│   └── pre-tool-use.sh        # Validation before tool execution
│
├── docs/                       # Reference documentation
│   ├── architecture.md        # Build system architecture
│   ├── branch-strategy.md     # Branching and release process
│   ├── common-tasks.md        # Task cookbook
│   └── troubleshooting.md     # Problem-solving guide
│
└── templates/                  # Reusable templates
    ├── new-stage-checklist.md      # New stage release checklist
    └── build-config-template.sh    # Build configuration template
```

## Quick Start

### For First-Time Users

1. **Read CLAUDE.md** - This file is automatically loaded into Claude Code context and contains essential repository information

2. **Explore Slash Commands** - Type `/` in Claude Code to see available commands:
   - `/build-local` - Build the UBL package locally
   - `/create-release` - Guide for creating new releases
   - `/validate-schemas` - Comprehensive validation
   - `/analyze-spreadsheet` - Work with Google Spreadsheets
   - `/compare-versions` - Compare UBL versions/stages

3. **Check Documentation** - Browse `docs/` directory:
   - Start with `architecture.md` to understand the build system
   - Read `common-tasks.md` for step-by-step instructions
   - Reference `troubleshooting.md` when issues arise

### For Experienced Users

- **Quick build:** `python build.py target local debug`
- **Validation:** `cd raw/val && ./test.sh && ./testsamples.sh`
- **Branch setup:** Use `/create-release` command for guided setup
- **Troubleshooting:** Check `docs/troubleshooting.md` for common issues

## Files Overview

### CLAUDE.md (Most Important!)
Auto-loaded project context containing:
- Repository overview and current branch info
- Key file locations
- Build commands and processes
- Common development tasks
- Coding standards and conventions
- Git workflow
- Troubleshooting quick reference

**This file is loaded into every Claude Code session automatically.**

### settings.json
Tool permissions and project configuration:
- Allowed tools (Read, Write, Edit, Bash, etc.)
- Git workflow settings
- Build configuration
- File patterns (auto-generated, do-not-edit)
- Documentation references

### Custom Slash Commands

#### /build-local
Comprehensive local build with:
- Configuration verification
- Build execution
- Error detection and reporting
- Validation testing
- Results analysis

#### /create-release
Step-by-step guide for creating new UBL releases:
- Determines version vs stage
- Updates all configuration files
- Manages Google Spreadsheets
- Updates documentation
- Creates commits

#### /validate-schemas
Complete validation workflow:
- Main validation tests
- Sample instance validation
- JSON validation
- Code list integrity checks
- Detailed error reporting

#### /analyze-spreadsheet
Google Spreadsheet management:
- URL verification
- Configuration analysis
- Accessibility checks
- Version comparison
- Update guidance

#### /compare-versions
Version/stage comparison:
- Locates comparison reports
- Parses HTML reports
- Analyzes entity files
- Generates summaries
- Migration guidance

### Hooks

#### pre-tool-use.sh
Validates operations before execution:
- Blocks pushes to protected branches
- Prevents editing auto-generated files
- Warns about critical file deletions
- Validates git operations
- Prevents force pushes

**Note:** Hooks are OPTIONAL. Enable with `/hooks` command in Claude Code.

### Documentation

#### architecture.md
- System overview and data flow
- Technology stack
- Build phases (acquisition → packaging)
- Configuration management
- Performance characteristics
- Extension points

#### branch-strategy.md
- Branch types and naming
- Stage progression (CSD → CS → OS)
- Version progression
- Branching workflows
- Pull request process
- Maintenance guidelines

#### common-tasks.md
Cookbook with step-by-step instructions:
- Building locally
- Adding document types
- Adding library components
- Updating code lists
- Adding samples
- Updating documentation
- And more...

#### troubleshooting.md
Problem-solving guide:
- Build failures
- Validation errors
- Spreadsheet issues
- Git problems
- Platform-specific issues
- Emergency recovery

### Templates

#### new-stage-checklist.md
Complete checklist for new stage releases:
- Branch setup
- Configuration updates
- Spreadsheet management
- Build and validation
- Commit and push
- Publication preparation
- Post-release tasks

#### build-config-template.sh
Template for build configuration:
- All configuration parameters
- Examples for different scenarios
- Subcommittee configuration
- Pre-build checklist

## Usage Tips

### Getting Help
1. Type `/` to see available slash commands
2. Read `CLAUDE.md` for quick reference
3. Check `docs/troubleshooting.md` for common issues
4. Use specific slash commands for guided workflows

### Best Practices
- Always read `CLAUDE.md` when starting work
- Use slash commands for complex workflows
- Test locally before pushing to GitHub
- Keep configuration files synchronized
- Update CLAUDE.md when making structural changes

### Customization
- Add new slash commands in `commands/`
- Extend hooks in `hooks/`
- Add documentation in `docs/`
- Create templates in `templates/`
- Update `CLAUDE.md` with new patterns

## Integration with Repository

### Version Control
- **Committed to git:** CLAUDE.md, settings.json, commands/, docs/, templates/
- **Gitignored:** CLAUDE.local.md, *.log, *.tmp
- **Shared with team:** All committed files
- **Local only:** .gitignored files

### Build Process
Claude Code configuration does not affect the build process. It enhances:
- Developer workflow efficiency
- Consistency across contributors
- Documentation accessibility
- Common task automation

### CI/CD
GitHub Actions workflows are independent of Claude Code configuration. The `.claude/` directory provides:
- Context for understanding workflows
- Documentation of build process
- Troubleshooting for CI failures

## Maintenance

### Updating Configuration

**When creating new version/stage:**
1. Update `CLAUDE.md` "Current Branch Context"
2. Update branch references in documentation
3. Run `/create-release` for guided updates

**When adding new functionality:**
1. Document in `CLAUDE.md` if widely applicable
2. Create slash command in `commands/` if repetitive
3. Add to `docs/common-tasks.md` if task-specific

**When discovering new patterns:**
1. Update relevant documentation
2. Consider creating template in `templates/`
3. Share with team via git commit

### Team Collaboration

This configuration is:
- Checked into git for team sharing
- Updated collaboratively
- Version-controlled alongside code
- Part of repository documentation

When making changes:
1. Test changes locally
2. Document rationale
3. Commit with clear message
4. Notify team if significant

## Frequently Asked Questions

**Q: Do I need Claude Code to work on UBL?**
A: No. This configuration enhances Claude Code usage but is not required for development.

**Q: Will this affect my local builds?**
A: No. The `.claude/` directory does not affect build processes.

**Q: Can I customize for my workflow?**
A: Yes! Create `CLAUDE.local.md` for personal customizations (gitignored).

**Q: How do I enable hooks?**
A: Run `/hooks` in Claude Code and select the hooks you want to enable.

**Q: What if I find an error in the documentation?**
A: Fix it and commit! This is collaborative documentation.

**Q: Can I add my own slash commands?**
A: Absolutely! Add `.md` files to `commands/` directory.

## Resources

- **Claude Code Docs:** https://docs.claude.com/en/docs/claude-code/
- **UBL TC:** https://www.oasis-open.org/committees/ubl/
- **Repository:** https://github.com/oasis-tcs/ubl
- **Main README:** ../README.md
- **Environment Setup:** ../ENVIRONMENT_SETUP.md

## Version History

- **2025-11-06:** Initial creation for ubl-2.5-python branch
  - Complete directory structure
  - 5 custom slash commands
  - Pre-tool-use hook
  - 4 documentation files
  - 2 template files

---

**Maintained by:** UBL TC Maintainers
**Questions?** Check CLAUDE.md or ask on UBL TC mailing list
