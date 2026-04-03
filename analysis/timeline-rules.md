# Chronological Timeline CSV — Rules & Conventions

## Purpose
A single CSV file showing all commits across all branches in chronological order,
with each commit placed in exactly one branch column to show which branch "owns" it.

## Trunk Model

The first-parent chain of `ubl-2.5` (328 commits) forms a single continuous
**trunk**. Many branch names pointed to different positions along this same
chain at different times (main, ubl-2.4-csd01wd01, ubl-2.5-csd01, ubl-2.5,
etc.), but in the CSV they all appear in one column: **UBL-Trunk**.

The **Active Branch** column records which git branch name was active at each
trunk commit, based on forensic evidence from the GitHub Activity API.

### Trunk Aliases
Branches whose first-parent chains are entirely subsets of the trunk have no
unique commits — they are "trunk aliases" and don't get their own column.
Examples: ubl-2.4-csd01wd01, ubl-2.4-csd02, ubl-2.5-dev.

### Non-Trunk Branches
Branches with unique commits that are not on the trunk's first-parent chain
get their own column for those commits only. Examples: ubl-2.5-python,
ubl-2.4-csd01wd02, tsc-ubl-2.5-experimental.

## Branch Assignment Rules

### First-Parent Chain
Each branch's "native" commits are determined by walking the **first-parent chain**
from the branch tip back to the root. Only commits on this first-parent path are
candidates for assignment to that branch.

### Trunk First
All 328 trunk commits are assigned to the UBL-Trunk column before any other
branch assignment happens.

### Deepest Branch Wins
For non-trunk commits that appear on multiple branches' first-parent chains,
the commit is assigned to the **deepest branch** — the one created first,
from which the others forked.

### Fork Tree
The fork tree (hardcoded in `generate-timeline.py`) defines which branch forked
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
- **Fork tree**: Manually verified parent-child relationships with fork-point SHAs
- **`branch-forensics.json`**: Curated metadata preserving information that git
  alone cannot provide:
  - **Branch renames**: e.g., ubl-2.5-csd01 → ubl-2.5 (April 2025)
  - **Bookmark branches**: Retroactively created branches with 0 pushes
  - **Deleted branches**: PR branches, ephemeral test branches
  - **Trunk active branch timeline**: Which branch name was active at each
    trunk position, derived from GitHub Activity API events
- **GitHub Activity API**: `repos/oasis-tcs/ubl/activity` — branch creation/deletion
  timestamps, push history, and actor information used to build the forensics file
