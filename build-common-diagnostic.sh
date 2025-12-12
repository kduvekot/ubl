#!/bin/bash
#
# build-common-diagnostic.sh - Diagnostic version of build-common.sh
#
# This script adds memory monitoring and configurable JVM/CPU settings
# for investigating parallel build memory issues on GitHub Actions.
#

# Create directories
if [ ! -d "$targetdir" ]; then mkdir "$targetdir" ; fi
if [ ! -d "$targetdir"/"$package"-"$UBLstage"-"$label" ]; then
mkdir     "$targetdir"/"$package"-"$UBLstage"-"$label"
fi
if [ ! -d "$targetdir"/"$package"-"$UBLstage"-"$label"/intermediate-support-files/ ]; then
mkdir     "$targetdir"/"$package"-"$UBLstage"-"$label"/intermediate-support-files/
fi

# Create diagnostics directory
DIAG_DIR="$targetdir/diagnostics"
if [ ! -d "$DIAG_DIR" ]; then mkdir -p "$DIAG_DIR" ; fi

targetdirabs=$(cd "$targetdir" && pwd)

# Function to log memory stats
log_memory() {
    local label="$1"
    local logfile="$DIAG_DIR/build-memory-checkpoints.log"

    echo "" >> "$logfile"
    echo "=== Memory Checkpoint: $label ===" >> "$logfile"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" >> "$logfile"

    # System memory
    echo "--- System Memory ---" >> "$logfile"
    free -m >> "$logfile"

    # Java processes
    echo "--- Java Processes ---" >> "$logfile"
    ps aux | grep '[j]ava' | awk '{printf "PID: %s, RSS: %.0f MB, VSZ: %.0f MB, CPU: %s%%\n", $2, $6/1024, $5/1024, $3}' >> "$logfile"

    # Process count
    JAVA_COUNT=$(ps aux | grep '[j]ava' | wc -l)
    echo "Total Java processes: $JAVA_COUNT" >> "$logfile"

    # Load average
    echo "Load average: $(cat /proc/loadavg)" >> "$logfile"
}

# Function to log system info
log_system_info() {
    local logfile="$DIAG_DIR/system-info.log"

    echo "=== System Information ===" > "$logfile"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" >> "$logfile"
    echo "" >> "$logfile"

    echo "--- CPU Info ---" >> "$logfile"
    nproc >> "$logfile"
    lscpu | grep -E 'Model name|Socket|Core|Thread|CPU\(s\)' >> "$logfile"
    echo "" >> "$logfile"

    echo "--- Memory Info ---" >> "$logfile"
    free -h >> "$logfile"
    cat /proc/meminfo | head -10 >> "$logfile"
    echo "" >> "$logfile"

    echo "--- Java Version ---" >> "$logfile"
    java -version 2>&1 >> "$logfile"
    echo "" >> "$logfile"

    echo "--- Build Configuration ---" >> "$logfile"
    echo "BUILD_CPU_COUNT: ${BUILD_CPU_COUNT}" >> "$logfile"
    echo "BUILD_JVM_HEAP_MAX: ${BUILD_JVM_HEAP_MAX}" >> "$logfile"
    echo "platform: ${platform}" >> "$logfile"
}

# Log initial system info
log_system_info

# Log memory before build
log_memory "PRE-BUILD"

echo "=============================================="
echo "Building package with diagnostic settings..."
echo "=============================================="
echo "CPU Count: ${BUILD_CPU_COUNT}"
echo "JVM Max Heap: ${BUILD_JVM_HEAP_MAX}"
echo ""

# Construct JVM memory options
JVM_OPTS="-Xmx${BUILD_JVM_HEAP_MAX}"

# Add GC logging for Java 8
JVM_OPTS="$JVM_OPTS -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:$DIAG_DIR/gc.log"

# Add heap dump on OOM
JVM_OPTS="$JVM_OPTS -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=$DIAG_DIR/"

# Print JVM settings
echo "JVM Options: $JVM_OPTS"
echo ""

# Start a background process to log memory periodically during the Ant build
(
    while true; do
        log_memory "DURING-BUILD-$(date +%H%M%S)"
        sleep 30
    done
) &
MEMORY_LOGGER_PID=$!
echo "Started background memory logger with PID: $MEMORY_LOGGER_PID"

# Run the Ant build with diagnostic options
# Pass cpuCount as an override parameter (-DcpuCountOverride)
java $JVM_OPTS \
    -Dant.home=utilities/ant \
    -classpath "utilities/saxon/saxon.jar:utilities/ant/lib/ant-launcher.jar:utilities/saxon9he/saxon9he.jar" \
    org.apache.tools.ant.launch.Launcher \
    -buildfile build.xml \
    "-Dtitle=$title" \
    "-Dpackage=$package" \
    "-DUBLversion=$UBLversion" \
    "-DUBLprevStageVersion=$UBLprevStageVersion" \
    "-DUBLprevStage=$UBLprevStage" \
    "-DUBLprevVersion=$UBLprevVersion" \
    "-Drawdir=$rawdir" \
    "-DlibraryGoogle=$libGoogle" \
    "-DdocumentsGoogle=$docGoogle" \
    "-DsignatureGoogle=$sigGoogle" \
    "-Ddir=$targetdirabs" \
    "-DUBLstage=$UBLstage" \
    "-Dlabel=$label" \
    "-DisDraft=$isDraft" \
    "-Drealtauser=$4" \
    "-Drealtapass=$5" \
    "-Dplatform=$platform" \
    "-DcpuCountOverride=${BUILD_CPU_COUNT}" \
    -v 2>&1 | tee "$DIAG_DIR/ant-verbose.log"

serverReturn=${PIPESTATUS[0]}

# Stop the background memory logger
kill $MEMORY_LOGGER_PID 2>/dev/null
echo "Stopped background memory logger"

# Log memory after build
log_memory "POST-BUILD"

sleep 2

# Save build results
echo "Build exit code: $serverReturn" > "$DIAG_DIR/build-exit-code.txt"

if [ ! -d "$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only/ ]; then mkdir "$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only/ ; fi
mv build.console."$label".txt "$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only/
if compgen -G "saxon*.log" > /dev/null; then
  mv saxon*.log "$targetdir/$package-$UBLstage-$label-archive-only/"
fi
echo $serverReturn         >"$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only/build.exitcode."$label".txt
touch                       "$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only/build.console."$label".txt

# Analyze memory log for peak usage
echo "=============================================="
echo "MEMORY ANALYSIS"
echo "=============================================="
if [ -f "$DIAG_DIR/build-memory-checkpoints.log" ]; then
    echo "Memory checkpoint log created"
    echo "Peak memory observations:"
    grep "Total Java processes" "$DIAG_DIR/build-memory-checkpoints.log" | sort -t: -k2 -rn | head -5
fi

if [ -f "$DIAG_DIR/gc.log" ]; then
    echo ""
    echo "GC Log Summary:"
    echo "GC events: $(grep -c 'GC' "$DIAG_DIR/gc.log" 2>/dev/null || echo 0)"
    echo "Full GC events: $(grep -c 'Full GC' "$DIAG_DIR/gc.log" 2>/dev/null || echo 0)"

    # Check for OOM in GC log
    if grep -q "OutOfMemoryError" "$DIAG_DIR/gc.log" 2>/dev/null; then
        echo "WARNING: OutOfMemoryError detected in GC log!"
    fi
fi

# reduce GitHub storage costs by zipping results and deleting intermediate files
pushd "$targetdir" || return
if [ -f "$package"-"$UBLstage"-"$label"-archive-only.7z ]; then rm "$package"-"$UBLstage"-"$label"-archive-only.7z ; fi
7z a -t7z -mx=9 -mfb=128 -md=64m -mqs=on -aoa "$package"-"$UBLstage"-"$label"-archive-only.7z "$package"-"$UBLstage"-"$label"-archive-only
if [ -f "$package"-"$UBLstage"-"$label"-iso-iec-19845.7z ]; then rm "$package"-"$UBLstage"-"$label"-iso-iec-19845.7z ; fi
7z a -t7z -mx=9 -mfb=128 -md=64m -mqs=on -aoa "$package"-"$UBLstage"-"$label"-iso-iec-19845.7z "$package"-"$UBLstage"-"$label"-iso-iec-19845 2>/dev/null || echo "ISO package not found (may not be generated yet)"
if [ -f "$package"-"$UBLstage"-"$label".7z ]; then rm "$package"-"$UBLstage"-"$label".7z ; fi
7z a -t7z -mx=9 -mfb=128 -md=64m -mqs=on -aoa "$package"-"$UBLstage"-"$label".7z "$package"-"$UBLstage"-"$label" 2>/dev/null || echo "Main package not found (may not be generated yet)"

# Also compress diagnostics
if [ -d diagnostics ]; then
    7z a -t7z -mx=5 diagnostics.7z diagnostics/
fi
popd || return

if [ "$targetdir" = "target" ]
then
if [ "$platform" = "github" ]
then
if [ "$6" = "DELETE-REPOSITORY-FILES-AS-WELL" ] #secret undocumented failsafe
then
# further reduce GitHub storage costs by deleting repository files

find . -not -name target -not -name .github -maxdepth 1 -exec rm -r -f {} \;

mv "$targetdir"/"$package"-"$UBLstage"-"$label"-archive-only.7z . 2>/dev/null || true
mv "$targetdir"/"$package"-"$UBLstage"-"$label"-iso-iec-19845.7z . 2>/dev/null || true
mv "$targetdir"/"$package"-"$UBLstage"-"$label".7z . 2>/dev/null || true
mv "$targetdir"/diagnostics.7z . 2>/dev/null || true

# Keep diagnostics directory for artifact upload
mv "$targetdir"/diagnostics . 2>/dev/null || true

rm -r -f "$targetdir"

fi
fi
fi

echo "=============================================="
echo "DIAGNOSTIC BUILD COMPLETED"
echo "Exit code: $serverReturn"
echo "=============================================="

exit 0 # always be successful so that github returns ZIP of results
