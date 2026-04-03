# UBL Release → Commit Mapping

Maps each official OASIS UBL release to the specific commit in the `oasis-tcs/ubl` repository
that corresponds to that release, with forensic evidence from blob matching against the
official distribution zips.

## Methodology

1. **Blob fingerprinting**: Each file in the release zip is hashed using `git hash-object` and
   compared against the full tree at the candidate commit. Byte-identical files confirm the
   source tree; files with differing content are investigated individually.
2. **Entity-resolved content**: The distributed `UBL-2.X.xml` (DocBook spec) has all `<!ENTITY>`
   references resolved inline. Changes to `UBL.xml` source (pubdate, stage, text) produce
   unique resolved output that pinpoints the exact source commit.
3. **Generated file metadata**: XSD schemas embed `Release Date:` and `Generated on:` timestamps
   from the build, traced to `config-UBL.xml` entity values and CI run times.
4. **Timestamp correlation**: Zip filenames, internal timestamps, and commit times are cross-referenced.

### Recurring pattern

- **`UBL-CommonSignatureComponents-2.X.xsd`** (both `xsd/` and `xsdrt/` variants) always differs
  between the zip and the repo. This is the only recurring content mismatch across all releases.
- **Static content** (DocBook toolchain `db/spec-0.8/`, artwork PNGs, old example XMLs) accounts
  for ~400-500 of the blob matches and is identical across many commits/releases.

## Pre-Repository Releases

These UBL versions were released **before** the GitHub repository was created (2018-04-11).
They are not tracked in the repo:

| Release | Date | Note |
|---------|------|------|
| UBL 2.0 | 12 December 2006 | OASIS Standard |
| UBL 2.1 | 04 November 2013 | OASIS Standard |
| UBL 2.2 | 09 July 2018 | OASIS Standard |

## UBL 2.3 Releases

The 2.3 source was loaded into the repo on 2021-05-15. Earlier 2.3 stages predate the repo or were loaded
as a bulk copy. The official OASIS-published progression was: CSPRD01 (07 Aug 2019) → CSPRD02 (29 Jan 2020)
→ CSD03 (29 Jul 2020) → CSD04 (25 Nov 2020) → CS01 (19 Jan 2021) → CS02 (25 May 2021) → OS (15 Jun 2021).

### UBL 2.3 CSD05 — `57dda2e`

- **No zip available** for validation (CSD05 was not published on OASIS as a formal stage —
  appears to be an internal working label)
- Branch tip of `ubl-2.3-csd05-copy`
- `config-UBL.xml` confirms `versionDisplay: 2.3 CSD05`, `versionDate: 12 May 2021`

### UBL 2.3 CS02 — `47eb1f5` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **590 / 891** (66%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.3.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 25 May 2021` — **differs from parent** `57dda2e` (12 May 2021) |
| UBL.xml pubdate | `25 May 2021` — **differs from parent** (12 May 2021) |
| Zip spec pubdate | `25 May 2021` ✓ |
| XSD Release Date | `25 May 2021` ✓ |
| XSD Generated on | `2021-05-24 00:10z` (CI run ~5h after commit at 19:22 EDT) |
| Branch tip | Yes — last commit on `ubl-2.3-cs02` |
| Uniqueness | **config-UBL.xml versionDate differs from parent → uniquely this commit** |

### UBL 2.3 OS — `bc99520` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **590 / 890** (66%) identical to commit tree |
| Content differs | 3 files: `UBL-CommonSignatureComponents-2.3.xsd` (×2) + `UBL-Entities-2.3.gc` |
| config-UBL.xml | `versionDate: 15 June 2021` (same as parent `89d22de`) |
| UBL.xml pubdate | `15 June 2021` (same as parent) |
| Zip spec pubdate | `15 June 2021` ✓ |
| XSD Release Date | `15 June 2021` ✓ |
| XSD Generated on | `2021-06-18 19:57z` (3 min after commit at 15:54 EDT = 19:54z) |
| Entity-resolved | Zip `UBL-2.3.xml` contains `membership of OASIS` — **matches bc99520 only**, parent has `OASIS Universal Business Language TC` |
| Branch tip | Yes — last commit on `ubl-2.3-os` (also tip of `ubl-2.3-os-iso`) |
| Uniqueness | **Entity-resolved text in UBL-2.3.xml uniquely identifies this commit** |

## UBL 2.4 Releases

### UBL 2.4 CSD01 — `2e3c601` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **597 / 910** (65%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.4.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 08 February 2023` (same as parent `8482207`) |
| UBL.xml pubdate | `08 February 2023` — **differs from parent** `8482207` (07 February 2023) |
| Zip spec pubdate | `08 February 2023` ✓ |
| XSD Release Date | `08 February 2023` ✓ |
| XSD Generated on | `2023-02-28 16:59z` (1 min after commit at 17:56 CET = 16:56z) |
| Branch | `ubl-2.4-csd01` — not tip (tip is `0b0b0b3`, post-release DOCX merge PR#24) |
| Uniqueness | **UBL.xml pubdate differs from parent → uniquely this commit** |

### UBL 2.4 CSD02 — `9b42a40` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **597 / 910** (65%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.4.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 26 July 2023` — **differs from parent** `d88d78c` (25 July 2023) |
| UBL.xml pubdate | `26 July 2023` ✓ |
| Zip spec pubdate | `26 July 2023` ✓ |
| XSD Release Date | `26 July 2023` ✓ |
| XSD Generated on | `2023-07-25 10:32z` (5 min after commit at 12:27 CEST = 10:27z) |
| Branch tip | Yes — last commit on `ubl-2.4-csd02` |
| Uniqueness | **config-UBL.xml versionDate differs from parent → uniquely this commit** |

### UBL 2.4 CS01 — `b9df309` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **597 / 910** (65%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.4.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 17 October 2023` (same as parent `e4809af`) |
| UBL.xml pubdate | `17 October 2023` (same as parent) |
| Zip spec pubdate | `17 October 2023` ✓ |
| XSD Release Date | `17 October 2023` ✓ |
| XSD Generated on | `2023-10-24 19:56z` (27 min before commit at 21:23 CEST = 19:23z — build precedes commit) |
| Entity-resolved | Zip `UBL-2.4.xml` contains `cranesoftwrights.github.io` URL — **matches b9df309 only**, parent has old `CraneSoftwrights.com` URL |
| Branch | `ubl-2.4-cs01` — not tip (tip is `8c4d077`, server testing Jun 2024) |
| Uniqueness | **Entity-resolved URL in UBL-2.4.xml uniquely identifies this commit** |

Note: Initially version date was set to "27 September 2023" at `f204999`, then corrected
to "17 October 2023" at `e4809af`/`b448cd7`.

### UBL 2.4 OS — `8c99636` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **597 / 910** (65%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.4.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 20 June 2024`, `versionDisplay: 2.4` (same as parent `a2f1431`) |
| UBL.xml pubdate | `20 June 2024` (same as parent) |
| Zip spec pubdate | `20 June 2024` ✓ |
| XSD Release Date | `20 June 2024` ✓ |
| XSD Generated on | `2024-06-25 15:49z` (2 days after commit — manual rebuild) |
| Signature XSD | Embeds `Library: OASIS Universal Business Language (UBL) 2.4` with `os-UBL-2.4` — **matches 8c99636 only**, parent `a2f1431` still had `CS01` in `config-UBL-Signature.xml` |
| Branch | `ubl-2.4-os` — not tip (tip is `779bf4b`, publishing retry Mar 2025) |
| Uniqueness | **Signature XSD metadata uniquely identifies this commit** (commit changed `config-UBL-Signature.xml` from CS01→OS) |

## UBL 2.5 Releases

All UBL 2.5 releases are on the `ubl-2.5` branch (no separate branch per stage).

### UBL 2.5 CSD01 — `0b44c38` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **620 / 2539** (24%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.5.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 20 August 2025`, `versionDisplay: 2.5 CSD01` |
| XSD Release Date | `20 August 2025` ✓ |
| XSD Generated on | `2025-08-13 23:06z` |
| Commit type | Merge of PR#28 (`ubl-2.5-7zip-test`); first parent is `09e538e` |
| Build source | XSDs generated 4 min after `09e538e` (23:02z); `0b44c38` only adds `build-common.sh` (7z flags — not in output). Both commits produce identical 620 blob matches. |
| Zip packaging | Internal timestamps show `2025-08-27` (manual Mac packaging, contains `__MACOSX/.DS_Store`). Content generated from `09e538e` tree. |
| Uniqueness | `0b44c38` is the merge commit marking the official CSD01 release point. The tree content is identical to `09e538e` for all distributed files. Fork point for `ubl-2.5-python`. |

### UBL 2.5 CSD02 — `b122814` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **624 / 1256** (49%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.5.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 03 December 2025` (same as parent `1ae74f8`) |
| UBL.xml pubdate | `03 December 2025` — **differs from parent** `1ae74f8` (26 November 2025) |
| Zip spec pubdate | `03 December 2025` ✓ |
| XSD Release Date | `03 December 2025` ✓ |
| XSD Generated on | `2025-12-03 12:42z` (3 min after commit at 13:39 CET = 12:39z) |
| Zip filename | `UBL-2.5-csd02-20251203-1239z.zip` — **timestamp matches commit to the minute** (12:39z) |
| Entity-resolved | Zip `UBL-2.5.xml` has unfixed `&version;` bug in 2.3/2.4 sections ("UBL 2.5 is technically a minor release") — **matches b122814 only**; next commit `ea6223d` fixed this to "UBL 2.3"/"UBL 2.4" |
| Uniqueness | **Three independent discriminators**: pubdate, entity-resolved text bug, zip filename timestamp |

### UBL 2.5 CSD03 — `3d81e8a` ★ VERIFIED

| Evidence | Detail |
|----------|--------|
| Blob matches | **672 / 1304** (51%) identical to commit tree |
| Content differs | 2 files: `UBL-CommonSignatureComponents-2.5.xsd` (xsd + xsdrt) |
| config-UBL.xml | `versionDate: 11 February 2026`, `versionDisplay: 2.5 CSD03` (same as parent `a66c455`) |
| UBL.xml pubdate | `11 February 2026` — **differs from parent** `a66c455` (03 December 2025) |
| UBL.xml stage | `csd03` — **differs from parent** (csd02) |
| UBL.xml editor | `Kenneth Bengtsson` — **differs from parent** (TBD) |
| Zip spec pubdate | `11 February 2026` ✓ |
| XSD Release Date | `11 February 2026` ✓ |
| XSD Generated on | `2026-02-09 15:16z` (commit at 19:13 +0400 = 15:13z — 3 min before build) |
| Entity-resolved | Zip `UBL-2.5.xml` contains `Committee Specification Draft 03` and editor `Kenneth Bengtsson` — **matches 3d81e8a only** |
| Branch tip | Yes — current tip of `ubl-2.5` |
| Uniqueness | **Multiple discriminators**: pubdate, stage, editor name all changed from parent |

## Summary

| Release | Date | Commit | Verification | Discriminating Evidence |
|---------|------|--------|-------------|------------------------|
| UBL 2.3 CSD05 | 12 May 2021 | `57dda2e` | No zip | Internal label only |
| UBL 2.3 CS02 | 25 May 2021 | `47eb1f5` | ★ 590/891 blobs | config versionDate differs from parent |
| UBL 2.3 OS | 15 June 2021 | `bc99520` | ★ 590/890 blobs | Entity-resolved text ("membership of OASIS") |
| UBL 2.4 CSD01 | 08 Feb 2023 | `2e3c601` | ★ 597/910 blobs | UBL.xml pubdate differs from parent |
| UBL 2.4 CSD02 | 26 Jul 2023 | `9b42a40` | ★ 597/910 blobs | config versionDate differs from parent |
| UBL 2.4 CS01 | 17 Oct 2023 | `b9df309` | ★ 597/910 blobs | Entity-resolved URL (cranesoftwrights.github.io) |
| UBL 2.4 OS | 20 Jun 2024 | `8c99636` | ★ 597/910 blobs | Signature XSD stage (CS01→OS) |
| UBL 2.5 CSD01 | 20 Aug 2025 | `0b44c38` | ★ 620/2539 blobs | Merge commit; build from first-parent 09e538e |
| UBL 2.5 CSD02 | 03 Dec 2025 | `b122814` | ★ 624/1256 blobs | Pubdate + entity text bug + zip timestamp |
| UBL 2.5 CSD03 | 11 Feb 2026 | `3d81e8a` | ★ 672/1304 blobs | Pubdate + stage + editor all changed from parent |

## Sources

- **OASIS release zips**: Downloaded from Google Drive archive and OASIS docs server
- **Blob fingerprinting**: `git hash-object` comparison of zip files against `git ls-tree -r <commit>`
- **config-UBL.xml**: Contains `versionDate`, `versionDisplay`, `versionDirectory` ENTITY declarations
- **UBL.xml**: DocBook source with `stage`, `version`, `stagetext`, `pubdate` ENTITY declarations
- **Generated XSDs**: Embed `Release Date:` and `Generated on:` in XML comments from build
- **GitHub Activity API**: Branch creation/push events from `repos/oasis-tcs/ubl/activity`
