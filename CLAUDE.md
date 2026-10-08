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
- The analysis was made between 31 March and 3 April 2026 and brought up to
  date on 8 October 2026. It covers the history up to `29ae6b4` on `ubl-2.6`
  (8 October 2026), including UBL 2.5 CS01 and OS.
- Its most valuable parts are the two that exist nowhere else: the release
  mapping (the official repository has no release tags apart from two old
  ones) and the GitHub API facts in `branch-forensics.json`, with the raw
  API data behind the latest of them in `api-data/`.

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
  listed without the ★. Since 2026 the workflow runs say which commit each
  build ran on, and a build artifact can be compared with the published zip
  file by file; artifacts and logs expire after about 90 days, so save their
  evidence soon after a release.
- **The timeline follows `timeline-rules.md`.** Change the rules there first
  when the model changes, then the scripts or `branch-tree.json`.
- **`api-data/<date>/` is raw evidence**: never edit it. A new snapshot goes in
  a folder of its own, with a `REPORT.md` and `SHA256SUMS.txt`.
- **Check the scripts reproduce the committed files before changing them**
  (see `README.md`), so that any difference afterwards comes from the change.
- Commit hashes in the files are 7 characters; give longer ones where a
  short one is ambiguous in the official repository.

## Keeping it up to date

What an update to the present involves (as done on 8 October 2026):

1. **A full clone of `oasis-tcs/ubl`**, and a check that the scripts still
   reproduce the committed `chronological-timeline.csv` and `trunk-train.svg`.
2. **The GitHub API data.** It is not reachable from every environment:
   the Activity API, the workflow runs (`actions/runs`), the artifacts
   (`actions/artifacts`) and the logs of release builds. Kees can fetch it
   with `gh` (`gh api repos/oasis-tcs/ubl/activity --paginate`, and the same
   for `actions/runs` and `actions/artifacts`; `gh run view <id> --log` and
   `gh run download <id>` for a release build). Keep it in
   `api-data/<date>/` with a `REPORT.md` and `SHA256SUMS.txt`.
3. **`branch-tree.json`**: add new branches with parent, fork point and full
   head; update the recorded heads of branches that moved, including the
   trunk branch; add releases and side branches for the diagram; set
   `as_of`. Today the trunk is the first-parent chain of `ubl-2.6`.
4. **`branch-forensics.json`**: new branches, renames and deletions, and the
   active branch names along the trunk after position 372, all with source
   and date, and additions only.
5. **New releases** in `release-commit-mapping.md`: the UBL 2.6 stages as
   they are published, at `https://docs.oasis-open.org/ubl/`.
6. **Run the scripts and render `trunk-train.png`** (see `README.md`), and
   check that the earlier rows of the timeline did not change.

After an update, change "What it covers" in `README.md` and the dates in
this file.

Open since 8 October 2026: why the single-file web-editor pushes of
13 April and 15 August 2026 have no workflow runs (`branch-forensics.json`,
`open_questions_2026_10_08`), and where the two replaced BDNDR files in the
published UBL 2.5 OS package come from (`release-commit-mapping.md`).
