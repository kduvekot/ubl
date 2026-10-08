# UBL repository history

This branch holds an analysis of the history of the official UBL repository,
[oasis-tcs/ubl](https://github.com/oasis-tcs/ubl): which commit each published
UBL release was built from, how the branches relate to each other, and facts
about branches that GitHub recorded but git does not keep.

It is not part of UBL. It is an orphan branch: it shares no history with the
UBL branches and must never be merged into them. It has no build workflow, so
pushing to it starts no build.

## What is here

| File | What it is | How it is made |
|---|---|---|
| `release-commit-mapping.md` | Each published UBL release from 2.3 CSD05 to 2.5 CSD03, with the commit it was built from and the evidence for it | By hand (method described in the file) |
| `branch-forensics.json` | Branch renames, deleted branches, bookmark branches and which branch name was in use when, from the GitHub Activity API and the workflow runs | By hand, from the GitHub API |
| `chronological-timeline.csv` | Every commit of every branch, one row each, in date order, with the branch it belongs to | `generate-timeline.py` |
| `timeline-rules.md` | The rules the timeline follows | By hand |
| `trunk-train.svg` | A "train track" diagram: the main line of commits, the branches that left and rejoined it, and the releases | `gen_train4.py` |
| `trunk-train.png` | The same diagram as a picture | Rendered from the SVG; no script |
| `generate-timeline.py`, `gen_train4.py` | The two scripts | |

Every commit hash in these files is a commit in oasis-tcs/ubl. To look one up,
open `https://github.com/oasis-tcs/ubl/commit/<hash>` or use any clone of that
repository. The hashes stay valid as long as the history of oasis-tcs/ubl is
not rewritten; merging, opening pull requests and deleting merged branches
never do that.

## What it covers

The analysis was made between 31 March and 3 April 2026 and covers the history
up to commit `3d81e8a` (9 February 2026), from which UBL 2.5 CSD03 was built.

Not yet covered:

- UBL 2.5 CS01 (15 April 2026) and UBL 2.5 OS (12 August 2026), with the
  branches `ubl-2.5-cs01`, `ubl-2.5-os` and `ubl-2.5-iso`;
- UBL 2.6 (branch `ubl-2.6`);
- branches deleted since: `ubl-2.5-python` was deleted on 8 October 2026; its
  last commit was `6c4d314`, which is also in `ubl-2.5` and `ubl-2.6`.

`CLAUDE.md` lists what an update involves.

## Making the timeline and the diagram again

The scripts need Python 3 and git, nothing else, and no network access. They
read the history from a clone of oasis-tcs/ubl, where they expect every branch
as `origin/<branch>`, as a normal clone has them.

1. Make a full clone (not a shallow one):

   ```sh
   git clone https://github.com/oasis-tcs/ubl.git ubl-official
   ```

2. In the folder where the results should go (for example a checkout of this
   branch), run:

   ```sh
   python3 generate-timeline.py /path/to/ubl-official
   python3 gen_train4.py /path/to/ubl-official
   ```

   They write `chronological-timeline.csv` and `trunk-train.svg` to the current
   folder, and read `branch-forensics.json` from the folder the scripts are in.

A branch that has been deleted from the official repository since the
analysis is taken from `branch-forensics.json`, where its last commit is
recorded (under `deleted_branches`, `deleted_after_analysis`); so far that is
`ubl-2.5-python`. If a branch is missing and not recorded there, the timeline
script stops and names it.

On 8 October 2026 this reproduced, from a plain clone, the committed
`chronological-timeline.csv` byte for byte, and `trunk-train.svg` apart from
its "Generated" date.

The scripts have the branch tree and the releases written into them, so they
make the same picture of the same period until they are updated; see
`CLAUDE.md`.
