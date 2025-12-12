#!/bin/bash
#
# build-diagnostic.sh - Diagnostic build script for investigating parallel build issues
#
# This script is used by the parallel-build-test workflow to run the build
# with configurable CPU count and JVM memory settings while collecting diagnostics.
#
# Environment variables used:
#   BUILD_CPU_COUNT     - Number of parallel workers (default: from build.xml logic)
#   BUILD_JVM_HEAP_MAX  - Maximum JVM heap size (default: 1g)
#   DIAGNOSTIC_MODE     - Enable extra diagnostic logging (default: false)
#

if [ "$3" = "" ]; then echo Missing results directory, platform, label \(, realta-username, realta-password arguments \) ; exit 1 ; fi

export targetdir="$1"
export platform=$2
export label=$3

# Configuration parameters (same as build.sh)
export title="UBL 2.5"
export package=UBL-2.5
export UBLversion=2.5
export UBLstage=csd02
export UBLprevStageVersion=2.5
export UBLprevStage=csd01
export UBLprevVersion=2.4
export rawdir=raw
export includeISO=false

export libGoogle=https://docs.google.com/spreadsheets/d/18o1YqjHWUw0-s8mb3ja4i99obOUhs-4zpgso6RZrGaY
export docGoogle=https://docs.google.com/spreadsheets/d/1024Th-Uj8cqliNEJc-3pDOR7DxAAW7gCG4e-pbtarsg
export sigGoogle=https://docs.google.com/spreadsheets/d/1T6z2NZ4mc69YllZOXE5TnT5Ey-FlVtaXN1oQ4AIMp7g

# Diagnostic settings with defaults
export BUILD_CPU_COUNT="${BUILD_CPU_COUNT:-1}"
export BUILD_JVM_HEAP_MAX="${BUILD_JVM_HEAP_MAX:-1g}"
export DIAGNOSTIC_MODE="${DIAGNOSTIC_MODE:-false}"

echo "=============================================="
echo "DIAGNOSTIC BUILD CONFIGURATION"
echo "=============================================="
echo "CPU Count: ${BUILD_CPU_COUNT}"
echo "JVM Max Heap: ${BUILD_JVM_HEAP_MAX}"
echo "Diagnostic Mode: ${DIAGNOSTIC_MODE}"
echo "Platform: ${platform}"
echo "Label: ${label}"
echo "=============================================="

# Call the diagnostic version of build-common
bash build-common-diagnostic.sh "$1" "$2" "$3" "$4" "$5" "$6"

exit 0 # always be successful so that github returns ZIP of results
