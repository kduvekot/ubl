#!/usr/bin/env python3
"""
Generate chronological timeline CSV for the UBL repository.
See timeline-rules.md for the conventions used.

Uses the manually verified fork tree rather than auto-detection,
since the deep branch overlaps cause algorithmic detection to fail.

Usage: python3 generate-timeline.py [/path/to/ubl/clone]
Output: chronological-timeline.csv in the current working directory.
"""

import subprocess
import sys
import os
from collections import OrderedDict, deque

# Use command-line arg, or default to the repo containing this script
if len(sys.argv) > 1:
    REPO = os.path.abspath(sys.argv[1])
else:
    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, cwd=REPO).strip()

def get_first_parent_chain(branch_ref):
    """Get first-parent chain as list of SHAs (oldest first)."""
    out = run(f"git rev-list --first-parent {branch_ref}")
    if not out:
        return []
    return list(reversed(out.split("\n")))

def get_commit_info(sha):
    """Get commit metadata."""
    fmt = "%H|%ae|%ai|%s"
    out = run(f'git log --format="{fmt}" -1 {sha}')
    parts = out.split("|", 3)
    return {
        "sha": parts[0],
        "author": parts[1],
        "date": parts[2],
        "message": parts[3],
    }

def short_author(email):
    """Shorten author email to a readable name."""
    mapping = {
        "gkenholman+github@gmail.com": "gkholman",
        "66590520+bdxhub@users.noreply.github.com": "bdxhub",
        "49699333+dependabot[bot]@users.noreply.github.com": "dependabot",
        "noreply@github.com": "GitHub",
        "robin.cover@oasis-open.org": "Robin Cover",
    }
    if email in mapping:
        return mapping[email]
    if "+" in email and "@users.noreply.github.com" in email:
        return email.split("+")[1].split("@")[0]
    return email.split("@")[0]

def csv_escape(val):
    """Escape a CSV field."""
    val = str(val)
    if "," in val or '"' in val or "\n" in val:
        return '"' + val.replace('"', '""') + '"'
    return val

def main():
    # ===== VERIFIED FORK TREE =====
    # Format: child -> (parent_branch, fork_sha)
    # This was manually verified by walking first-parent chains.
    #
    # TRUNK MODEL: The first-parent chain of ubl-2.5 (328 commits) is the
    # single continuous trunk.  Many branch names pointed to different
    # positions along this same chain at different times.  In the CSV,
    # ALL trunk commits appear in the "ubl-2.5" column; the "Active Branch"
    # metadata column records which name was active for each commit.
    #
    # Branches whose first-parent chains are entirely subsets of the trunk
    # (no unique commits) are "trunk aliases" — they don't get their own
    # column.  Branches with unique non-trunk commits keep a column for
    # those commits only.
    FORK_TREE = {
        "main": (None, None),
        # 2.3 branch family
        "ubl-2.3-csd05-copy": ("main", "6d153bf"),
        "ubl-2.3-cs02": ("ubl-2.3-csd05-copy", "57dda2e"),
        "ubl-2.3-os": ("ubl-2.3-cs02", "47eb1f5"),
        "ubl-2.3-os-iso": ("ubl-2.3-os", "bc99520"),
        "review": ("ubl-2.3-os", "bc99520"),
        # 2.4 branch family
        "ubl-2.4-csd01wd01": ("main", "f71d2be"),
        "ubl-2.4-csd01wd02": ("ubl-2.4-csd01wd01", "21efa9e"),
        "ubl-2.4-csd01": ("ubl-2.4-csd01wd02", "294527e"),
        "ubl-2.4-csd02-prd01-13": ("ubl-2.4-csd01", "2e3c601"),
        "ubl-2.4-csd02-tsc": ("ubl-2.4-csd02-prd01-13", "476e1ad"),
        "ubl-2.4-csd02": ("ubl-2.4-csd02-prd01-13", "476e1ad"),
        "ubl-2.4-cs01-work": ("ubl-2.4-csd02", "9b42a40"),
        "ubl-2.4-cs01": ("ubl-2.4-cs01-work", "7c01887"),
        "ubl-2.4-os": ("ubl-2.4-cs01", "6cc2cf5"),
        "ubl-2.4-os-iso-pub": ("ubl-2.4-os", "8c99636"),
        # 2.5 branch family (connected tree)
        "tsc-ubl-2.5-experimental": ("ubl-2.4-cs01", "16ca084"),
        "ubl-2.5-dev": ("ubl-2.4-cs01", "b9df309"),
        "ubl-2.5-kenneth": ("ubl-2.5-dev", "76dcc63"),
        "UBL-433-xsd-doc": ("ubl-2.5-dev", "39fae0d"),
        "retest": ("ubl-2.5-dev", "153236e"),
        # 2.5 branch family
        "ubl-2.5": ("UBL-433-xsd-doc", "4c0ffc3"),
        "ubl-2.5-python": ("ubl-2.5", "0b44c38"),
        "server-test": ("ubl-2.5", "b122814"),
        "ubl-2.5-2025-layout": ("ubl-2.5", "b122814"),
        "kentest": ("ubl-2.5-2025-layout", "5e984b8"),
        "ubl-2.5-retry": ("ubl-2.5", "ea6223d"),
    }

    # The trunk is the first-parent chain of ubl-2.5
    TRUNK_BRANCH = "ubl-2.5"
    TRUNK_COLUMN = "UBL-Trunk"  # display name for the trunk column in CSV

    branch_names = list(FORK_TREE.keys())
    print(f"Branches: {len(branch_names)}", file=sys.stderr)

    # Build first-parent chains
    fp_chains = {}
    for name in branch_names:
        fp_chains[name] = get_first_parent_chain(f"origin/{name}")
        print(f"  {name}: {len(fp_chains[name])} fp commits", file=sys.stderr)

    # Build processing order: BFS from main through fork tree
    children = {name: [] for name in branch_names}
    for child, (parent, _) in FORK_TREE.items():
        if parent:
            children[parent].append(child)

    process_order = []
    queue = deque(["main"])
    visited = set()
    while queue:
        b = queue.popleft()
        if b in visited:
            continue
        visited.add(b)
        process_order.append(b)
        for child in children[b]:
            queue.append(child)

    print(f"\nProcess order: {process_order}", file=sys.stderr)

    # Identify the trunk: the first-parent chain of TRUNK_BRANCH (oldest first)
    trunk_chain = fp_chains[TRUNK_BRANCH]
    trunk_set = set(trunk_chain)
    print(f"\nTrunk ({TRUNK_BRANCH}): {len(trunk_set)} first-parent commits", file=sys.stderr)

    # Load forensics data for trunk active branch timeline.
    # This captures information that git alone cannot provide (renames,
    # bookmarks, fast-forward merges) — derived from GitHub Activity API
    # and workflow run evidence.
    forensics_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "branch-forensics.json")
    trunk_segments = None
    if os.path.exists(forensics_path):
        import json
        with open(forensics_path) as f:
            forensics = json.load(f)
        trunk_segments = forensics.get("trunk_active_branch_timeline", {}).get("segments", [])
        print(f"Loaded {len(trunk_segments)} trunk segments from forensics", file=sys.stderr)

    # Assign "active branch name" for each trunk commit.
    active_branch = {}
    if trunk_segments:
        # Use forensics-based segments (includes renamed/deleted branches)
        for seg in trunk_segments:
            name = seg["branch"]
            start = seg["trunk_start"]
            end = seg["trunk_end"]
            for i in range(start, min(end + 1, len(trunk_chain))):
                active_branch[trunk_chain[i]] = name
        # Any trunk commits not covered by segments get TRUNK_BRANCH
        for sha in trunk_chain:
            if sha not in active_branch:
                active_branch[sha] = TRUNK_BRANCH
    else:
        # Fallback: derive from FORK_TREE by walking backward from TRUNK_BRANCH
        trunk_path = []
        cur = TRUNK_BRANCH
        while cur is not None:
            trunk_path.append(cur)
            parent, _ = FORK_TREE[cur]
            cur = parent
        trunk_path.reverse()
        print(f"Trunk path (FORK_TREE fallback): {' → '.join(trunk_path)}", file=sys.stderr)

        transition_shas = {}
        for i in range(1, len(trunk_path)):
            child = trunk_path[i]
            parent, fork_sha_short = FORK_TREE[child]
            if fork_sha_short:
                for sha in trunk_chain:
                    if sha.startswith(fork_sha_short):
                        transition_shas[sha] = child
                        break

        current_name = trunk_path[0]
        for sha in trunk_chain:
            if sha in transition_shas:
                active_branch[sha] = current_name
                current_name = transition_shas[sha]
            else:
                active_branch[sha] = current_name

    # Report transitions
    prev = None
    for i, sha in enumerate(trunk_chain):
        ab = active_branch[sha]
        if ab != prev:
            print(f"  Trunk [{i}]: {ab} (from {sha[:7]})", file=sys.stderr)
            prev = ab

    # Assign commits to branches using the trunk model:
    # 1. All trunk commits → TRUNK_COLUMN (display name)
    # 2. Non-trunk commits → deepest branch (original logic)
    assignment = {}
    for sha in trunk_set:
        assignment[sha] = TRUNK_COLUMN

    # Assign non-trunk first-parent commits
    for branch in process_order:
        claimed = 0
        for sha in fp_chains[branch]:
            if sha not in assignment:
                assignment[sha] = branch
                claimed += 1
        if claimed:
            print(f"  {branch}: claimed {claimed} non-trunk commits", file=sys.stderr)

    # Now assign "merged-in" commits: commits reachable from branches but NOT on
    # any first-parent chain. These came from PR/feature branches that were merged.
    # Assign each to the branch that contains the merge commit that brought it in.
    print("\nAssigning merged-in (non-first-parent) commits...", file=sys.stderr)

    # Get all reachable commits
    all_refs_str = " ".join(f"origin/{name}" for name in branch_names)
    all_reachable_out = run(f"git rev-list {all_refs_str}")
    all_reachable = set(all_reachable_out.split("\n"))

    non_fp = all_reachable - set(assignment.keys())
    print(f"  Non-first-parent commits to assign: {len(non_fp)}", file=sys.stderr)

    # For each merge commit, find what it brought in and assign those commits
    merge_out = run(f'git log --all --merges --format="%H %P" {all_refs_str}')
    for line in merge_out.split("\n"):
        if not line.strip():
            continue
        parts = line.split()
        merge_sha = parts[0]
        if len(parts) < 3:
            continue
        first_parent = parts[1]
        second_parent = parts[2]

        if merge_sha not in assignment:
            continue

        merge_branch = assignment[merge_sha]

        # Find commits reachable from second_parent but not from first_parent
        try:
            brought_in = run(f"git rev-list {second_parent} ^{first_parent}")
            if brought_in:
                for sha in brought_in.split("\n"):
                    sha = sha.strip()
                    if sha and sha not in assignment and sha in non_fp:
                        assignment[sha] = merge_branch
        except subprocess.CalledProcessError:
            pass

    # Check what's still unassigned
    still_unassigned = all_reachable - set(assignment.keys())
    if still_unassigned:
        print(f"  Still unassigned after merge processing: {len(still_unassigned)}", file=sys.stderr)
        # Assign remaining to the first branch that contains them
        for sha in still_unassigned:
            for name in process_order:
                try:
                    run(f"git merge-base --is-ancestor {sha} origin/{name}")
                    assignment[sha] = name
                    break
                except subprocess.CalledProcessError:
                    continue

    # Collect all assigned SHAs
    all_shas = list(assignment.keys())
    print(f"\nTotal commits: {len(all_shas)}", file=sys.stderr)

    # Get metadata (batch via git log)
    print("Fetching commit metadata...", file=sys.stderr)
    commit_info = {}
    # Use git log to batch - fetch ALL reachable commits' metadata
    all_refs = " ".join(
        f"origin/{name}" for name in branch_names
    )
    out = run(f'git log --format="%H|%ae|%ai|%s" {all_refs}')
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("|", 3)
        sha = parts[0]
        commit_info[sha] = {
            "sha": sha,
            "author": parts[1],
            "date": parts[2],
            "message": parts[3],
        }

    # Any missing? (shouldn't happen)
    for sha in all_shas:
        if sha not in commit_info:
            print(f"  WARNING: no metadata for {sha[:7]}, fetching individually", file=sys.stderr)
            commit_info[sha] = get_commit_info(sha)

    # Sort chronologically
    sorted_shas = sorted(all_shas, key=lambda s: commit_info[s]["date"])

    # Build sha -> row index
    sha_to_row = {sha: i for i, sha in enumerate(sorted_shas)}

    # Determine column order by first appearance
    first_appearance = {}
    for idx, sha in enumerate(sorted_shas):
        branch = assignment[sha]
        if branch not in first_appearance:
            first_appearance[branch] = idx

    # Determine which branches have commits assigned (vs pure trunk aliases)
    branches_with_commits = set(assignment.values())

    # Also account for fork point entries in child columns
    fork_points = {}  # sha -> [(parent_branch, child_branch), ...]
    for child, (parent, fork_sha_short) in FORK_TREE.items():
        if parent and fork_sha_short:
            # Resolve short sha to full sha
            full_sha = None
            for sha in sorted_shas:
                if sha.startswith(fork_sha_short):
                    full_sha = sha
                    break
            if full_sha:
                if full_sha not in fork_points:
                    fork_points[full_sha] = []
                # If parent is a trunk alias (no column), remap to trunk
                effective_parent = parent
                if full_sha in trunk_set and parent not in branches_with_commits:
                    effective_parent = TRUNK_COLUMN
                fork_points[full_sha].append((effective_parent, child))
                # Update first appearance for child (only if it has a column)
                if child in branches_with_commits:
                    fork_idx = sha_to_row.get(full_sha, 9999)
                    if child not in first_appearance or fork_idx < first_appearance[child]:
                        first_appearance[child] = fork_idx
            else:
                print(f"  WARNING: fork sha {fork_sha_short} not found for {child}", file=sys.stderr)
    active_branches = [TRUNK_COLUMN] + [b for b in branch_names if b in branches_with_commits]
    print(f"\nBranches with commits: {len(active_branches)} (of {len(branch_names)} total)", file=sys.stderr)
    dropped = [b for b in branch_names if b not in branches_with_commits]
    if dropped:
        print(f"Trunk aliases (no column): {dropped}", file=sys.stderr)

    # Column order aligned with train track diagram:
    # 1. Trunk (ubl-2.5)
    # 2. Right-side merge-back branches
    # 3. Left-side dead-end branches (by fork point)
    # 4. Other branches with unique commits
    TRAIN_TRACK_ORDER = [
        TRUNK_COLUMN,
        # Right side (merge-back PRs)
        'ubl-2.4-csd01wd02', 'ubl-2.5-python',
        # Left side (dead-ends, by fork point)
        'ubl-2.3-csd05-copy', 'ubl-2.3-cs02', 'ubl-2.3-os', 'ubl-2.3-os-iso',
        'review', 'main', 'tsc-ubl-2.5-experimental',
        'ubl-2.4-os', 'ubl-2.4-os-iso-pub', 'retest', 'ubl-2.5-kenneth',
        'server-test', 'kentest', 'ubl-2.5-retry',
        # Other (branches with unique non-trunk commits)
        'ubl-2.5-2025-layout',
        'ubl-2.4-csd01', 'ubl-2.4-csd02-tsc', 'ubl-2.4-cs01',
    ]
    # Use train track order for branches that have commits, append any new ones
    known = set(TRAIN_TRACK_ORDER)
    sorted_branches = [b for b in TRAIN_TRACK_ORDER if b in active_branches]
    sorted_branches += sorted([b for b in active_branches if b not in known],
                              key=lambda b: first_appearance.get(b, 9999))
    col_idx = {name: i for i, name in enumerate(sorted_branches)}
    print(f"\nColumn order: {sorted_branches}", file=sys.stderr)

    # Get merge info
    out = run(f'git log --all --merges --format="%H|%P|%s" {all_refs}')
    merges = {}
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("|", 2)
        sha = parts[0]
        parents = parts[1].split()
        merges[sha] = {"parents": parents, "message": parts[2]}

    # Find branch tips
    tips = {}
    for name in branch_names:
        if fp_chains[name]:
            tip_sha = fp_chains[name][-1]
            if tip_sha not in tips:
                tips[tip_sha] = []
            tips[tip_sha].append(name)

    # Root
    root_sha = sorted_shas[0] if sorted_shas else None

    # ===== GENERATE CSV =====
    header = ["#", "Date", "SHA", "Author", "Message", "Active Branch", "Event"] + sorted_branches

    rows = []
    for idx, sha in enumerate(sorted_shas):
        row_num = idx + 1
        info = commit_info[sha]
        branch = assignment[sha]
        short_sha = sha[:7]
        date = info["date"][:10]
        author = short_author(info["author"])
        message = info["message"].replace('"', "'")

        # Build events
        events = []
        if sha == root_sha:
            events.append("ROOT: main")

        if sha in fork_points:
            for parent_branch, child_branch in fork_points[sha]:
                events.append(f"BRANCH: {child_branch}")

        if sha in tips:
            for tip_name in tips[sha]:
                events.append(f"◆ TIP: {tip_name}")

        # Merge info
        if sha in merges:
            m = merges[sha]
            second_parent = m["parents"][1] if len(m["parents"]) > 1 else None
            if second_parent and second_parent in assignment:
                source_branch = assignment[second_parent]
                if source_branch != branch:
                    dest_col = col_idx.get(branch, 0)
                    src_col = col_idx.get(source_branch, 0)
                    if src_col > dest_col:
                        events.append(f"←merged← {source_branch}")
                    else:
                        events.append(f"→merged→ {source_branch}")

        event_str = " | ".join(events)

        # Active branch: for trunk commits, show the original branch name
        # (only when it differs from TRUNK_BRANCH)
        ab = active_branch.get(sha, "")

        # Build columns
        cols = []
        for b in sorted_branches:
            if b == branch:
                cols.append(short_sha)
            else:
                cols.append(" ")

        # Add fork markers to parent and child columns
        if sha in fork_points:
            for parent_branch, child_branch in fork_points[sha]:
                p_i = col_idx.get(parent_branch, -1)
                c_i = col_idx.get(child_branch, -1)
                marker = f"⊢→{child_branch}"

                if p_i >= 0:
                    existing = cols[p_i].strip()
                    if existing and existing != " ":
                        cols[p_i] = f"{existing} {marker}"
                    else:
                        cols[p_i] = marker

                if c_i >= 0:
                    existing = cols[c_i].strip()
                    if existing and existing != " ":
                        cols[c_i] = f"{existing} {marker}"
                    else:
                        cols[c_i] = marker

        row = [str(row_num), date, short_sha, author, message, ab, event_str] + cols
        rows.append(row)

    # Output to current working directory
    outpath = os.path.join(os.getcwd(), "chronological-timeline.csv")
    with open(outpath, "w") as f:
        f.write(",".join(csv_escape(h) for h in header) + "\n")
        for i, row in enumerate(rows):
            f.write(",".join(csv_escape(v) for v in row) + "\n")
            if (i + 1) % 50 == 0 and i + 1 < len(rows):
                f.write(",".join(csv_escape(h) for h in header) + "\n")

    print(f"\nGenerated {len(rows)} data rows → {outpath}", file=sys.stderr)

    # Stats
    branch_counts = {}
    for sha, b in assignment.items():
        branch_counts[b] = branch_counts.get(b, 0) + 1
    print("\nCommits per branch:", file=sys.stderr)
    for b in sorted_branches:
        print(f"  {b}: {branch_counts.get(b, 0)}", file=sys.stderr)

if __name__ == "__main__":
    main()
