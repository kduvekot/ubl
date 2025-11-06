#!/bin/bash
#
# UBL Build Configuration Template
#
# This template provides the standard configuration structure for UBL builds.
# Copy and customize for new versions or stages.
#
# Usage: Edit the configuration parameters below, then use with build-common.sh
#

# Verify required arguments
if [ "$3" = "" ]; then
    echo "Missing required arguments: results-directory platform label [realta-username] [realta-password]"
    exit 1
fi

# Build environment parameters (passed from command line)
export targetdir="$1"        # Target directory for build output
export platform="$2"         # Platform: local, github, etc.
export label="$3"            # Build label (timestamp or custom)

# =============================================================================
# VERSION AND STAGE CONFIGURATION
# =============================================================================

# Current version and stage
export title="UBL X.X"              # Human-readable title
export package="UBL-X.X"            # Package name prefix
export UBLversion="X.X"             # Version number (e.g., 2.5)
export UBLstage="csdXX"             # Stage (e.g., csd01, cs01, os)

# Previous stage (for stage comparison)
export UBLprevStageVersion="X.X"    # Version of previous stage
export UBLprevStage="csdXX"         # Previous stage name

# Previous version (for version comparison)
export UBLprevVersion="X.X"         # Previous version number

# =============================================================================
# SOURCE MATERIALS
# =============================================================================

# Directory containing raw/source materials
export rawdir="raw"

# =============================================================================
# GOOGLE SPREADSHEETS (Source of Truth for Data Model)
# =============================================================================

# Library Components Spreadsheet
# Contains: Common library components (reusable elements)
# Format: https://docs.google.com/spreadsheets/d/SPREADSHEET_ID
# IMPORTANT: Do NOT include "/edit..." at the end
export libGoogle="https://docs.google.com/spreadsheets/d/LIBRARY_SPREADSHEET_ID"

# Documents Spreadsheet
# Contains: Document-level structures (Invoice, Order, etc.)
export docGoogle="https://docs.google.com/spreadsheets/d/DOCUMENTS_SPREADSHEET_ID"

# Signature Components Spreadsheet
# Contains: Digital signature components
export sigGoogle="https://docs.google.com/spreadsheets/d/SIGNATURE_SPREADSHEET_ID"

# =============================================================================
# PUBLISHING OPTIONS
# =============================================================================

# Include ISO/IEC 19845 formatted outputs
# Set to "true" for final releases, "false" for development builds
export includeISO="false"

# Draft status (used for watermarking, etc.)
export isDraft=""

# =============================================================================
# STAGE-SPECIFIC NOTES
# =============================================================================

# Committee Specification Draft (CSD)
# - Development stages
# - Incremental changes
# - Internal TC review
# Example: csd01, csd02, csd03, ...

# Committee Specification (CS)
# - Public review
# - Stable specification
# - Minimal changes
# Example: cs01, cs02 (rarely needed)

# OASIS Standard (OS)
# - Final approved standard
# - No further technical changes
# - One per version
# Example: os

# =============================================================================
# EXAMPLES
# =============================================================================

# Example 1: UBL 2.5 CSD01 (First draft of new version)
# export title="UBL 2.5"
# export package="UBL-2.5"
# export UBLversion="2.5"
# export UBLstage="csd01"
# export UBLprevStageVersion="2.4"
# export UBLprevStage="os"
# export UBLprevVersion="2.4"

# Example 2: UBL 2.5 CSD02 (Second draft, following CSD01)
# export title="UBL 2.5"
# export package="UBL-2.5"
# export UBLversion="2.5"
# export UBLstage="csd02"
# export UBLprevStageVersion="2.5"
# export UBLprevStage="csd01"
# export UBLprevVersion="2.4"

# Example 3: UBL 2.5 CS01 (Committee Specification for public review)
# export title="UBL 2.5"
# export package="UBL-2.5"
# export UBLversion="2.5"
# export UBLstage="cs01"
# export UBLprevStageVersion="2.5"
# export UBLprevStage="csd05"
# export UBLprevVersion="2.4"

# Example 4: UBL 2.5 OS (OASIS Standard - final)
# export title="UBL 2.5"
# export package="UBL-2.5"
# export UBLversion="2.5"
# export UBLstage="os"
# export UBLprevStageVersion="2.5"
# export UBLprevStage="cs01"
# export UBLprevVersion="2.4"
# export includeISO="true"

# =============================================================================
# SUBCOMMITTEE CONFIGURATION EXAMPLE
# =============================================================================

# Example: Transportation Subcommittee (TSC)
# export title="UBL 2.5 TSC"
# export package="UBL-2.5-TSC"
# export UBLversion="2.5"
# export UBLstage="csd01"
# export UBLprevStageVersion="2.5"
# export UBLprevStage="csd02"          # From main TC branch
# export UBLprevVersion="2.4"
#
# Use separate spreadsheets for subcommittee work:
# export libGoogle="https://docs.google.com/spreadsheets/d/TSC_LIBRARY_ID"
# export docGoogle="https://docs.google.com/spreadsheets/d/TSC_DOCUMENTS_ID"
# export sigGoogle="https://docs.google.com/spreadsheets/d/TSC_SIGNATURE_ID"

# =============================================================================
# CHECKLIST BEFORE BUILDING
# =============================================================================

# Before running build with this configuration:
#
# [ ] All version/stage variables are correct
# [ ] Google Spreadsheet URLs are valid (no /edit... suffix)
# [ ] Spreadsheets are publicly accessible ("Anyone with link can view")
# [ ] Previous version genericode files exist (UBL-Entities-{prevVersion}-os.gc)
# [ ] Previous stage genericode files renamed if needed
# [ ] UBL.xml entity declarations updated to match
# [ ] XSD schema files updated if new version (version= attributes)
# [ ] This file (build.sh) and build.py are synchronized
# [ ] .claude/CLAUDE.md updated with current context

# =============================================================================
# EXECUTE BUILD
# =============================================================================

# Call common build script with all parameters
bash build-common.sh "$1" "$2" "$3" "$4" "$5" "$6"

# Always exit successfully for GitHub Actions to capture artifacts
exit 0
