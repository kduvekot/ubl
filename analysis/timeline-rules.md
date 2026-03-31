# Chronological Timeline CSV — Rules & Conventions

## Purpose
A single CSV file showing all commits across all branches in chronological order,
with each commit placed in exactly one branch column to show which branch "owns" it.

## Branch Assignment Rules

### First-Parent Chain
Each branch's "native" commits are determined by walking the **first-parent chain**
from the branch tip back to the root. Only commits on this first-parent path are
assigned to that branch.

### Deepest Branch Wins
When a commit appears on multiple branches' first-parent chains (because branches
share a common history prefix), the commit is assigned to the **deepest/earliest
branch** — i.e., the branch that was created first and from which the others forked.

### Fork Tree
The fork tree defines which branch forked from which, and at what commit SHA.
The fork point is where the child branch's first unique commit's parent sits
on the parent branch's first-parent chain.

## Column Layout

### Column Order
Branches are sorted by **first appearance** — i.e., the row number of the first
non-empty cell in that branch's column. This naturally groups related branches
together and follows the chronological creation order.

### Branch Columns
- Each branch gets one column
- A commit's SHA appears in exactly one branch column
- All other cells for that row are empty (filled with a single space for rendering)

## Markers & Events

### Fork Points (⊢→)
When branch B forks from branch A at commit X:
- The fork-point commit X shows `⊢→B` in branch A's column
- The fork-point commit X also shows `⊢→B` in branch B's column
- If multiple branches fork at the same commit, markers are comma-separated

### BRANCH Events
The `Event` column shows `BRANCH: child-branch` on the **fork-point row**
(not the first-unique-commit row). This marks where the child diverged.

### TIP Markers (◆)
The tip (latest) commit of each branch is marked with `◆` in the Event column.

### ROOT Marker
The very first commit (root of the tree) shows `ROOT: main` in the Event column.

### Merge Markers
Merge commits show directional arrows indicating the flow:
- `←merged←` means content was merged FROM a branch to the RIGHT
- `→merged→` means content was merged FROM a branch to the LEFT
The arrow points in the direction of the source branch relative to the
destination branch's column position.

The merge commit itself appears in the **destination branch's column**
(the branch whose first-parent chain contains the merge commit).

## Rendering

### Empty Cells
All empty cells contain a single space character (` `) rather than being truly
empty. This prevents GitHub's CSV viewer from collapsing columns.

### Intermediate Headers
A header row is repeated every 50 data rows for navigation in GitHub's CSV viewer.
These rows use the same format as the main header row.

## Recovered History

The repository contains 40 commits that were previously unreachable (not on any
branch ref) but were recovered from GitHub's object store. These sit between
`4c0ffc3` (UBL-433-xsd-doc tip) and `48ad2d8` (parent of `dc1249d`). They are
preserved on the `recovered/ubl-2.5-lost-history` branch and are assigned to
`ubl-2.5` in the timeline since that is the branch they were originally pushed to.

With these recovered commits, the entire repository is **one connected tree**
rooted at `71129c9` (2018-04-11). There is no disconnected/orphan tree.

## Data Sources

- **Git first-parent chains**: `git rev-list --first-parent <branch>`
- **Activity API**: `repos/oasis-tcs/ubl/activity` — provided branch creation
  dates, push history, and actor information
- **Workflow runs**: `gh run list --repo oasis-tcs/ubl` — provided headSha
  values that identified lost commits
