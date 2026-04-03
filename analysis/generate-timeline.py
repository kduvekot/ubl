#!/usr/bin/env python3
"""
Generate chronological timeline CSV for the UBL repository.
See timeline-rules.md for the conventions used.

Uses the manually verified fork tree rather than auto-detection,
since the deep branch overlaps cause algorithmic detection to fail.
"""

import subprocess
import sys
from collections import OrderedDict, deque

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

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
    # ubl-2.5 connects through UBL-433-xsd-doc back to ubl-2.5-dev.
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

    # Assign commits to branches
    # Each branch claims its first-parent commits not yet claimed by an ancestor
    assignment = {}
    fp_sets = {name: set(chain) for name, chain in fp_chains.items()}

    for branch in process_order:
        claimed = 0
        for sha in fp_chains[branch]:
            if sha not in assignment:
                assignment[sha] = branch
                claimed += 1
        print(f"  {branch}: claimed {claimed} new commits", file=sys.stderr)

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
                fork_points[full_sha].append((parent, child))
                # Update first appearance for child
                fork_idx = sha_to_row.get(full_sha, 9999)
                if child not in first_appearance or fork_idx < first_appearance[child]:
                    first_appearance[child] = fork_idx
            else:
                print(f"  WARNING: fork sha {fork_sha_short} not found for {child}", file=sys.stderr)

    # Column order aligned with train track diagram:
    # 1. Trunk (ubl-2.5)
    # 2. Right-side merge-back branches
    # 3. Left-side dead-end branches (by fork point)
    # 4. Other branches in the broader tree
    TRAIN_TRACK_ORDER = [
        'ubl-2.5',
        # Right side (merge-back PRs)
        'ubl-2.4-csd01wd02', 'ubl-2.5-python',
        # Left side (dead-ends, by fork point)
        'ubl-2.3-csd05-copy', 'ubl-2.3-cs02', 'ubl-2.3-os', 'ubl-2.3-os-iso',
        'review', 'main', 'tsc-ubl-2.5-experimental',
        'ubl-2.4-os', 'ubl-2.4-os-iso-pub', 'retest', 'ubl-2.5-kenneth',
        'server-test', 'kentest', 'ubl-2.5-retry',
        # Other (broader tree)
        'ubl-2.5-dev', 'UBL-433-xsd-doc', 'ubl-2.5-2025-layout',
        'ubl-2.4-csd01wd01', 'ubl-2.4-csd01', 'ubl-2.4-csd02-prd01-13',
        'ubl-2.4-csd02-tsc', 'ubl-2.4-csd02', 'ubl-2.4-cs01-work', 'ubl-2.4-cs01',
    ]
    # Use train track order for known branches, append any new ones at the end
    known = set(TRAIN_TRACK_ORDER)
    sorted_branches = [b for b in TRAIN_TRACK_ORDER if b in branch_names]
    sorted_branches += sorted([b for b in branch_names if b not in known],
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
    header = ["#", "Date", "SHA", "Author", "Message", "Event"] + sorted_branches

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

        row = [str(row_num), date, short_sha, author, message, event_str] + cols
        rows.append(row)

    # Output
    print(",".join(csv_escape(h) for h in header))
    for i, row in enumerate(rows):
        print(",".join(csv_escape(v) for v in row))
        if (i + 1) % 50 == 0 and i + 1 < len(rows):
            print(",".join(csv_escape(h) for h in header))

    print(f"\nGenerated {len(rows)} data rows", file=sys.stderr)

    # Stats
    branch_counts = {}
    for sha, b in assignment.items():
        branch_counts[b] = branch_counts.get(b, 0) + 1
    print("\nCommits per branch:", file=sys.stderr)
    for b in sorted_branches:
        print(f"  {b}: {branch_counts.get(b, 0)}", file=sys.stderr)

if __name__ == "__main__":
    main()
