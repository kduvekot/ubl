#!/bin/bash
#
# Pre-Tool-Use Hook for UBL Repository
#
# This hook runs before Claude executes any tool.
# It can examine the tool call and approve, modify, or block it.
#
# Arguments:
#   $1 - TOOL_NAME (e.g., "Bash", "Write", "Edit")
#   $2 - TOOL_ARGS (JSON string with tool parameters)
#
# Exit codes:
#   0 - Allow the operation
#   1 - Block the operation (with feedback message)
#
# Usage:
#   - Place in .claude/hooks/pre-tool-use.sh
#   - Make executable: chmod +x .claude/hooks/pre-tool-use.sh
#   - Enable in Claude Code with: /hooks
#
# Note: This hook is OPTIONAL. Remove or disable if not desired.

TOOL_NAME="$1"
TOOL_ARGS="$2"

# Get current git branch
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)

#
# RULE 1: Block direct pushes to protected branches
#
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$TOOL_ARGS" =~ git[[:space:]]+push ]]; then
    if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
        echo "❌ BLOCKED: Direct push to '$CURRENT_BRANCH' branch is not allowed."
        echo "Please create a feature branch and use pull requests."
        echo ""
        echo "To create a feature branch:"
        echo "  git checkout -b claude/my-feature-$(date +%s)"
        exit 1
    fi
fi

#
# RULE 2: Block editing auto-generated entity files
#
if [[ "$TOOL_NAME" == "Edit" ]] || [[ "$TOOL_NAME" == "Write" ]]; then
    if [[ "$TOOL_ARGS" =~ -ent\.xml ]]; then
        echo "❌ BLOCKED: Cannot edit auto-generated entity files (*-ent.xml)."
        echo "These files are generated during the build process."
        echo ""
        echo "Entity files are created from:"
        echo "  - UBL-Party-summary-information.xml"
        echo "  - UBL-Schema-summary-information.xml"
        echo "  - Build process outputs"
        echo ""
        echo "Edit the source XML files instead, then run the build."
        exit 1
    fi
fi

#
# RULE 3: Block deletion of critical build files
#
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$TOOL_ARGS" =~ rm.*-rf ]]; then
    # Check if trying to delete critical directories
    if [[ "$TOOL_ARGS" =~ (utilities|raw|db) ]]; then
        echo "⚠️  WARNING: About to delete critical build directories."
        echo "This will break the build process."
        echo ""
        echo "Directories protected:"
        echo "  - utilities/ (build tools)"
        echo "  - raw/ (source schemas and samples)"
        echo "  - db/ (DocBook stylesheets)"
        echo ""
        echo "If you're sure, you can override this hook temporarily."
        # Allow but warn (exit 0), or block (exit 1)
        exit 0
    fi

    # Warn about deleting target directory
    if [[ "$TOOL_ARGS" =~ target ]]; then
        echo "ℹ️  INFO: Deleting target/ directory (build artifacts)."
        echo "This is safe - artifacts will be regenerated on next build."
    fi
fi

#
# RULE 4: Block deletion of genericode reference files
#
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$TOOL_ARGS" =~ rm.*UBL-Entities-.*-os\.gc ]]; then
    echo "❌ BLOCKED: Cannot delete previous version genericode files."
    echo "These files are required for version comparison."
    echo ""
    echo "Files: UBL-Entities-*-os.gc, UBL-Signature-Entities-*-os.gc"
    echo ""
    echo "These represent the previous OASIS Standard version and must be"
    echo "preserved in the repository for generating comparison reports."
    exit 1
fi

#
# RULE 5: Warn when modifying build configuration
#
if [[ "$TOOL_NAME" == "Edit" ]] || [[ "$TOOL_NAME" == "Write" ]]; then
    if [[ "$TOOL_ARGS" =~ (build\.py|build\.sh|config-UBL\.xml) ]]; then
        echo "ℹ️  INFO: Modifying build configuration."
        echo ""
        echo "Remember to also update:"
        echo "  - .claude/CLAUDE.md (version/stage context)"
        echo "  - UBL.xml entity declarations (if version/stage changed)"
        echo "  - XSD schema files in raw/xsd/common/ (for new versions)"
        echo ""
        echo "After changes, run: /build-local to test"
        # Allow operation
    fi
fi

#
# RULE 6: Check for suspicious file operations
#
if [[ "$TOOL_NAME" == "Write" ]]; then
    # Warn if writing outside expected directories
    if [[ "$TOOL_ARGS" =~ /tmp/ ]] || [[ "$TOOL_ARGS" =~ /etc/ ]] || [[ "$TOOL_ARGS" =~ /var/ ]]; then
        echo "⚠️  WARNING: Writing to system directory: $TOOL_ARGS"
        echo "This seems unusual for UBL development."
        echo ""
        echo "Expected directories: raw/, .claude/, root files"
        # Allow but warn
    fi
fi

#
# RULE 7: Validate git operations
#
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$TOOL_ARGS" =~ git.*commit ]]; then
    # Check if there are entity files staged
    if git diff --cached --name-only 2>/dev/null | grep -q -- '-ent\.xml$'; then
        echo "⚠️  WARNING: Auto-generated entity files are staged for commit."
        echo ""
        echo "Files matching *-ent.xml should not be committed."
        echo "These are generated during build."
        echo ""
        echo "To unstage:"
        echo "  git reset HEAD *-ent.xml"
        # Warn but allow (editor might have updated them intentionally)
    fi
fi

#
# RULE 8: Prevent force push
#
if [[ "$TOOL_NAME" == "Bash" ]] && [[ "$TOOL_ARGS" =~ git.*push.*(-f|--force) ]]; then
    if [[ "$CURRENT_BRANCH" =~ ^(main|master|ubl-.*) ]]; then
        echo "❌ BLOCKED: Force push to '$CURRENT_BRANCH' is not allowed."
        echo ""
        echo "Force pushing can destroy commit history."
        echo "If you absolutely must force push, do it manually."
        exit 1
    fi
fi

# If we get here, allow the operation
exit 0
