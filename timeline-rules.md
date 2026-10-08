# Chronological Timeline CSV — Rules & Conventions

## Purpose
A single CSV file showing all commits across all branches in chronological order,
with each commit placed in exactly one branch column to show which branch "owns" it.

## Trunk Model

The first-parent chain of `ubl-2.6` (373 commits, up to `29ae6b4` of
8 October 2026) forms a single continuous **trunk**. Many branch names
pointed to different positions along this same chain at different times
(main, ubl-2.4-csd01wd01, ubl-2.5-csd01, ubl-2.5, ubl-2.5-cs01, ubl-2.5-os,
ubl-2.6, etc.), but in the CSV they all appear in one column: **UBL-Trunk**.

Up to the analysis of April 2026 the trunk was the first-parent chain of
`ubl-2.5` (328 commits, ending at `3d81e8a`). That chain is the first 328
commits of the `ubl-2.6` chain, unchanged: `ubl-2.5` itself never moved
after `3d81e8a`, and the work continued on `ubl-2.5-cs01`, then
`ubl-2.5-os`, then `ubl-2.6`, each started from the tip of the one before.

### Branch Heads Are Fixed
The data file `branch-tree.json` records the head commit of every branch
as it was when the analysis was last brought up to date. The scripts use
those commits, not the current `origin/<branch>` refs, so that they keep
producing the same timeline after branches move on or are deleted. A
branch that has moved is reported on stderr; bringing it into the timeline
means updating its recorded head.

The **Active Branch** column records which git branch name was active at each
trunk commit, based on forensic evidence from the GitHub Activity API.

### Trunk Aliases
Branches whose first-parent chains are entirely subsets of the trunk have no
unique commits — they are "trunk aliases" and don't get their own column.
Examples: ubl-2.4-csd01wd01, ubl-2.4-csd02, ubl-2.5-dev, ubl-2.5,
ubl-2.5-cs01, ubl-2.5-os.

### Non-Trunk Branches
Branches with unique commits that are not on the trunk's first-parent chain
get their own column for those commits only. Examples: ubl-2.5-python,
ubl-2.4-csd01wd02, tsc-ubl-2.5-experimental, ubl-2.5-iso (one commit,
`8630a5f`, merged into ubl-2.6 by PR #46).

## Branch Assignment Rules

### First-Parent Chain
Each branch's "native" commits are determined by walking the **first-parent chain**
from the branch tip back to the root. Only commits on this first-parent path are
candidates for assignment to that branch.

### Trunk First
All 373 trunk commits are assigned to the UBL-Trunk column before any other
branch assignment happens.

### Deepest Branch Wins
For non-trunk commits that appear on multiple branches' first-parent chains,
the commit is assigned to the **deepest branch** — the one created first,
from which the others forked.

### Fork Tree
The fork tree (in `branch-tree.json`) defines which branch forked
from which, and at what commit SHA. This was manually verified by walking
first-parent chains. It determines processing order: parent branches are
processed before children, so parent branches claim shared commits first.

## Column Layout

### Column Order
Columns are ordered to match the train track diagram:
1. **UBL-Trunk** (first)
2. Right-side merge-back branches (PR branches merged back to trunk)
3. Left-side dead-end branches (by fork point)
4. Other branches with unique non-trunk commits

### Branch Columns
- Each branch with unique commits gets one column
- A commit's SHA appears in exactly one branch column
- All other cells for that row are empty (filled with a single space for rendering)

### Active Branch Column
Between "Message" and "Event", this column shows which git branch name was
active on the trunk at each first-parent commit. This captures information
that git alone cannot provide — branch renames, deleted branches, and the
progression of names over the project's lifetime.

## Markers & Events

### Fork Points (⊢→)
When branch B forks from branch A at commit X:
- The fork-point commit X shows `⊢→B` in branch A's column
- The fork-point commit X also shows `⊢→B` in branch B's column

### BRANCH Events
The `Event` column shows `BRANCH: child-branch` on the **fork-point row**
(not the first-unique-commit row). This marks where the child diverged.

### TIP Markers (◆)
The tip (latest) commit of each branch is marked with `◆ TIP: branch` in the
Event column.

### ROOT Marker
The very first commit (root of the tree) shows `ROOT: main` in the Event column.

### Merge Markers
Merge commits show directional arrows indicating the flow:
- `←merged←` means content was merged FROM a branch to the RIGHT
- `→merged→` means content was merged FROM a branch to the LEFT

The arrow points in the direction of the source branch relative to the
destination branch's column position. The merge commit itself appears in the
**destination branch's column**.

## Rendering

### Empty Cells
All empty cells contain a single space character (` `) rather than being truly
empty. This prevents GitHub's CSV viewer from collapsing columns.

### Intermediate Headers
A header row is repeated every 50 data rows for navigation in GitHub's CSV viewer.

## Data Sources

- **Git first-parent chains**: `git rev-list --first-parent <branch>`
- **Fork tree** (`branch-tree.json`): Manually verified parent-child
  relationships with fork-point SHAs, the recorded head of every branch, the
  column order, and the releases and side branches of the diagram
- **`branch-forensics.json`**: Curated metadata preserving information that git
  alone cannot provide:
  - **Branch renames**: e.g., ubl-2.5-csd01 → ubl-2.5 (April 2025)
  - **Bookmark branches**: Retroactively created branches with 0 pushes
  - **Deleted branches**: PR branches, ephemeral test branches
  - **Trunk active branch timeline**: Which branch name was active at each
    trunk position, derived from GitHub Activity API events
- **GitHub Activity API**: `repos/oasis-tcs/ubl/activity` — branch creation/deletion
  timestamps, push history, and actor information used to build the forensics file
