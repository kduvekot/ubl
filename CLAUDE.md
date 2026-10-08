# Background for agents working on this branch

Read `README.md` first: it says what each file is and how the timeline and the
diagram are made. This file adds the background, the rules, and what an update
involves.

## What this is

- The subject is the official UBL repository, `oasis-tcs/ubl` (OASIS UBL
  Technical Committee). Every commit hash here refers to a commit there.
- This branch lives in Kees Duvekot's fork, `kduvekot/ubl`. Kees is
  co-maintainer of `oasis-tcs/ubl`. It is an orphan branch with only the
  analysis: never merge it into a UBL branch, never base a UBL branch on it,
  and never push it to `oasis-tcs/ubl`.
- The analysis was made between 31 March and 3 April 2026 and covers the
  history up to `3d81e8a` (UBL 2.5 CSD03, 9 February 2026).
- Its most valuable parts are the two that exist nowhere else: the release
  mapping (the official repository has no release tags apart from two old
  ones) and the GitHub API facts in `branch-forensics.json`.

## Rules

- **Work from a full clone of `oasis-tcs/ubl`**, never a shallow clone and
  never a fork. A shallow clone made part of the history look disconnected
  once: a branch `recovered/ubl-2.5-lost-history` was made for "lost"
  commits that turned out to have been on the main line all along. The fork
  has its own branches and lacks some official ones.
- **Never remove anything from `branch-forensics.json`.** The GitHub Activity
  API only keeps events for a limited time, so what is recorded there may no
  longer be obtainable. Add new facts with their source and the date they
  were gathered; correct mistakes by saying what was wrong.
- **Release mapping: mark a release ★ VERIFIED only with evidence**, as the
  file describes: hash every file of the published release zip with
  `git hash-object` and compare with `git ls-tree -r <commit>`, then find
  what tells the candidate commit apart from its neighbours (publication
  date, stage, editor, the "Release Date" and "Generated on" lines in the
  XSD files, text in the published `UBL-2.x.xml`). The two
  `UBL-CommonSignatureComponents-2.x.xsd` files always differ; that is
  expected. A release that cannot be checked against a published zip is
  listed without the ★.
- **The timeline follows `timeline-rules.md`.** Change the rules there first
  when the model changes, then the script.
- **Check the scripts reproduce the committed files before changing them**
  (see `README.md`), so that any difference afterwards comes from the change.
- Commit hashes in the files are 7 characters; give longer ones where a
  short one is ambiguous in the official repository.

## Keeping it up to date

What an update to the present involves:

1. **Branches deleted from the official repository.** The scripts need every
   branch in their branch tree. Record a deleted branch's last commit in
   `branch-forensics.json` and recreate its ref in the clone before running
   the scripts (see `README.md`). Deleted so far since the analysis:
   `ubl-2.5-python` (8 October 2026, last commit `6c4d314`).
2. **The main line ("trunk").** The scripts take the trunk as the
   first-parent chain of `ubl-2.5`, which stops at `3d81e8a`. That chain
   continues unchanged in `ubl-2.6`: its first-parent chain contains all 328
   trunk commits and goes on from there (372 commits on 8 October 2026). So
   the trunk can become the first-parent chain of `ubl-2.6`. The release
   branches `ubl-2.5-cs01`, `ubl-2.5-os` and `ubl-2.5-iso` then need a place in
   the branch tree.
3. **The data written into the scripts**: `FORK_TREE` and `TRUNK_BRANCH` in
   `generate-timeline.py`; the trunk branch, `dead_branches` and `releases`
   in `gen_train4.py`. Moving this data into one data file that both scripts
   read would make later updates a matter of editing data.
4. **New releases** in `release-commit-mapping.md`: UBL 2.5 CS01 (published
   15 April 2026), UBL 2.5 OS (12 August 2026), the ISO/IEC version of 2.5,
   and the UBL 2.6 stages as they are published. Published packages are at
   `https://docs.oasis-open.org/ubl/` (for example `cs01-UBL-2.5/`).
5. **`branch-forensics.json`**: new branches, renames and deletions since
   April 2026, and the active branch names along the trunk after position
   327. The file has two known slips to correct: the rename note says
   "Three contributors" but names four, and the deletion time of
   `ubl-2.4-csd01-docx` is before its creation (the file already says so).
6. **`trunk-train.png`** has no script: render it again from the SVG.

After an update, change "What it covers" in `README.md` and the dates in
this file.
