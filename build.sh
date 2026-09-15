#!/bin/bash

if [ "$3" = "" ]; then echo Missing results directory, platform, label \(, realta-username, realta-password arguments \) ; exit 1 ; fi

export targetdir="$1"
export platform=$2
export label=$3

# Configuration parameters

export title="UBL 2.6"
export package=UBL-2.6
export UBLversion=2.6
export UBLstage=pre-csd01
# Stage text as it appears on the specification cover page.
export UBLstageText="Pre-CSD01 interim build"
# Release date. While drafting leave this empty and the build stamps the
# build time, so interim builds can be told apart. For a real publication
# set the date the TC approved, e.g. "19 November 2026".
export UBLreleaseDate=""

# --- derived, do not edit ---------------------------------------------------
# Upper-case form of the stage, used on the cover page and in schema headers.
export UBLstageUC=$(printf '%s' "$UBLstage" | tr '[:lower:]' '[:upper:]')
# If no release date was set, stamp this build so interim builds are
# distinguishable. Prefer the run label (YYYYMMDD-HHMMz) so the document and
# the package name agree; fall back to the current UTC time.
if [ -z "$UBLreleaseDate" ]; then
  if printf '%s' "$label" | grep -qE '^[0-9]{8}-[0-9]{4}z$'; then
    UBLreleaseDate=$(printf '%s' "$label" | sed -E 's/^(....)(..)(..)-(..)(..)z$/\1-\2-\3 \4:\5z/')
  else
    UBLreleaseDate=$(date -u +'%Y-%m-%d %H:%Mz')
  fi
  export UBLreleaseDate
fi
# ---------------------------------------------------------------------------
export UBLprevStageVersion=2.5
export UBLprevStage=os
export UBLprevVersion=2.5
export rawdir=raw
export includeISO=false

# The library and documents spreadsheets are new documents for UBL 2.6, copied from
# the UBL 2.5 OS masters. The signature spreadsheet is shared across UBL 2 versions
# and is deliberately unchanged.
export libGoogle=https://docs.google.com/spreadsheets/d/1kTDHeGm73EyAAa5b1WoZ-9J44qNwD_8JuCZpSzzkUrw
export docGoogle=https://docs.google.com/spreadsheets/d/1Z3zXR7TtcnlgEXtx4Sr4CwnvAhwg3ebX_cyyqjN124k
export sigGoogle=https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g

# Ken's test spreadsheets
# export libGoogle=https://docs.google.com/spreadsheets/d/1UoLO8ZQ4rxnp5Pjd9iwaqCNBkvrJA5VaixtlTMNvWsk
# export docGoogle=https://docs.google.com/spreadsheets/d/1rlKMh-WatADJjf-ZY1-ytSq284thzpvXriWIbfDUJEI



bash build-common.sh "$1" "$2" "$3" "$4" "$5" "$6"

exit 0 # always be successful so that github returns ZIP of results
