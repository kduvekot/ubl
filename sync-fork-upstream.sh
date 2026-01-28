#!/bin/bash
# Sync fork kduvekot/ubl with upstream oasis-tcs/ubl
# Generated: 2026-01-28

set -e

FORK="kduvekot/ubl"
UPSTREAM="oasis-tcs/ubl"

echo "=== Syncing fork $FORK with upstream $UPSTREAM ==="
echo ""

# Phase 1: Fast-forward sync for ubl-2.5 (fork is 2 commits behind)
echo "Phase 1: Syncing ubl-2.5 branch..."
gh repo sync "$FORK" --branch ubl-2.5 && echo "  ✓ ubl-2.5 synced" || echo "  ✗ ubl-2.5 failed"

echo ""

# Phase 2: Create missing branches from upstream
echo "Phase 2: Creating missing branches from upstream..."

# server-test
echo "  Creating server-test..."
gh api "repos/$FORK/git/refs" -X POST \
  -f ref="refs/heads/server-test" \
  -f sha="68aabb910b3a2e5fb59afa4d8911d709b4bf8027" \
  --silent && echo "  ✓ server-test created" || echo "  ✗ server-test failed (may already exist)"

# ubl-2.5-2025-layout
echo "  Creating ubl-2.5-2025-layout..."
gh api "repos/$FORK/git/refs" -X POST \
  -f ref="refs/heads/ubl-2.5-2025-layout" \
  -f sha="5e984b8c5e716ae96fc879eb886a36dd2592a5a3" \
  --silent && echo "  ✓ ubl-2.5-2025-layout created" || echo "  ✗ ubl-2.5-2025-layout failed (may already exist)"

# ubl-2.5-retry
echo "  Creating ubl-2.5-retry..."
gh api "repos/$FORK/git/refs" -X POST \
  -f ref="refs/heads/ubl-2.5-retry" \
  -f sha="f738ca337ff2a1cff48afbd9bca0007bb430038d" \
  --silent && echo "  ✓ ubl-2.5-retry created" || echo "  ✗ ubl-2.5-retry failed (may already exist)"

echo ""
echo "=== Sync complete ==="
echo ""
echo "Skipped (per plan):"
echo "  - kentest (diverged - needs manual decision)"
echo "  - ubl-2.5-python (fork is ahead with your work)"
echo "  - 21 branches already in sync"
