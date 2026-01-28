#!/bin/bash
# Auto-detect and sync fork with upstream
# Usage: ./sync-fork-auto.sh [--dry-run] [--force]

FORK="kduvekot/ubl"
UPSTREAM="oasis-tcs/ubl"
DRY_RUN=false
FORCE=false

# Parse args
for arg in "$@"; do
  case $arg in
    --dry-run) DRY_RUN=true ;;
    --force) FORCE=true ;;
  esac
done

echo "=== Fork Sync Tool ==="
echo "Fork:     $FORK"
echo "Upstream: $UPSTREAM"
echo "Dry run:  $DRY_RUN"
echo ""

# Get all branches from both repos
echo "Fetching branch lists..."
upstream_branches=$(gh api "repos/$UPSTREAM/branches" --paginate --jq '.[].name' | sort)
fork_branches=$(gh api "repos/$FORK/branches" --paginate --jq '.[].name' | sort)

# Arrays for categorization
declare -a needs_sync=()
declare -a needs_create=()
declare -a in_sync=()
declare -a fork_ahead=()
declare -a diverged=()

echo "Comparing branches..."
echo ""

# Check each upstream branch
for branch in $upstream_branches; do
  # Skip claude/* branches (fork-specific)
  [[ "$branch" == claude/* ]] && continue

  upstream_sha=$(gh api "repos/$UPSTREAM/branches/$branch" --jq '.commit.sha' 2>/dev/null)
  fork_sha=$(gh api "repos/$FORK/branches/$branch" --jq '.commit.sha' 2>/dev/null || echo "NOT_FOUND")

  if [[ "$fork_sha" == "NOT_FOUND" ]]; then
    needs_create+=("$branch:$upstream_sha")
    echo "  [CREATE] $branch"
  elif [[ "$upstream_sha" == "$fork_sha" ]]; then
    in_sync+=("$branch")
  else
    # Check if fork is ahead, behind, or diverged
    compare=$(gh api "repos/$FORK/compare/$UPSTREAM:${branch}...$FORK:${branch}" --jq '{ahead: .ahead_by, behind: .behind_by}' 2>/dev/null)
    ahead=$(echo "$compare" | jq -r '.ahead')
    behind=$(echo "$compare" | jq -r '.behind')

    if [[ "$ahead" == "0" && "$behind" != "0" ]]; then
      needs_sync+=("$branch")
      echo "  [SYNC]   $branch (behind by $behind)"
    elif [[ "$ahead" != "0" && "$behind" == "0" ]]; then
      fork_ahead+=("$branch")
      echo "  [SKIP]   $branch (fork ahead by $ahead)"
    else
      diverged+=("$branch:$ahead:$behind")
      echo "  [DIVERGED] $branch (ahead: $ahead, behind: $behind)"
    fi
  fi
done

echo ""
echo "=== Summary ==="
echo "In sync:      ${#in_sync[@]} branches"
echo "Need sync:    ${#needs_sync[@]} branches"
echo "Need create:  ${#needs_create[@]} branches"
echo "Fork ahead:   ${#fork_ahead[@]} branches (skipped)"
echo "Diverged:     ${#diverged[@]} branches (manual review needed)"
echo ""

if $DRY_RUN; then
  echo "[DRY RUN] No changes made."
  exit 0
fi

# Perform sync operations
if [[ ${#needs_sync[@]} -gt 0 ]]; then
  echo "=== Syncing branches ==="
  for branch in "${needs_sync[@]}"; do
    echo "  Syncing $branch..."
    if $FORCE; then
      gh repo sync "$FORK" --branch "$branch" --force
    else
      gh repo sync "$FORK" --branch "$branch"
    fi
  done
fi

if [[ ${#needs_create[@]} -gt 0 ]]; then
  echo "=== Creating missing branches ==="
  for item in "${needs_create[@]}"; do
    branch="${item%%:*}"
    sha="${item##*:}"
    echo "  Creating $branch..."
    gh api "repos/$FORK/git/refs" -X POST \
      -f ref="refs/heads/$branch" \
      -f sha="$sha" \
      --silent || echo "    Failed (may already exist)"
  done
fi

echo ""
echo "=== Done ==="
