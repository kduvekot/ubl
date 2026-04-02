# UBL Release → Commit Mapping

Maps each official OASIS UBL release to the specific commit in the `oasis-tcs/ubl` repository
that corresponds to that release.

## Methodology

1. **Release dates** extracted from the OASIS distribution packages (spec HTML `<date>` element)
2. **Version/stage** confirmed via `config-UBL.xml` (ENTITY declarations) and `UBL.xml` (DocBook source)
3. **Release commits** identified as the last commit that set the version metadata to match the release,
   cross-referenced with branch activity and workflow runs
4. **Branch tips** noted where they differ from the release commit (post-release maintenance)

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

| Release | Date | Commit | Branch | Note |
|---------|------|--------|--------|------|
| UBL 2.3 CSD05 | 12 May 2021 | `57dda2e` | `ubl-2.3-csd05-copy` | Branch tip. Copy of pre-existing CSD05 distribution. `config-UBL.xml` confirms `versionDisplay: 2.3 CSD05`. Note: "CSD05" was not published on OASIS as a formal stage — the published progression was CSPRD01→CSPRD02→CSD03→CSD04→CS01→CS02→OS. This appears to be an internal working label. |
| UBL 2.3 CS02 | 25 May 2021 | `47eb1f5` | `ubl-2.3-cs02` | Branch tip. `UBL.xml` stage=`cs02`, date=`25 May 2021`. Commit msg: "First attempt at CS02" |
| UBL 2.3 OS | 15 June 2021 | `bc99520` | `ubl-2.3-os` | Branch tip. `UBL.xml` stage=`os`, date=`15 June 2021`. Also tip of `ubl-2.3-os-iso` (identical) |

## UBL 2.4 Releases

| Release | Date | Release Commit | Branch | Branch Tip | Note |
|---------|------|---------------|--------|------------|------|
| UBL 2.4 CSD01 | 08 Feb 2023 | `2e3c601` | `ubl-2.4-csd01` | `0b0b0b3` | `2e3c601` is the last commit before the CSD02 branch forked. `config-UBL.xml` has `versionDate: 08 February 2023`, `versionDisplay: 2.4 CSD01`. Branch tip (`0b0b0b3`, Sep 2023) includes post-release DOCX merge (PR#24). |
| UBL 2.4 CSD02 | 26 Jul 2023 | `9b42a40` | `ubl-2.4-csd02` | `9b42a40` | Branch tip = release commit. `config-UBL.xml` updated to `versionDate: 26 July 2023`, `versionDisplay: 2.4 CSD02`. This commit is also the fork point for `ubl-2.4-cs01-work`. |
| UBL 2.4 CS01 | 17 Oct 2023 | `b9df309` | `ubl-2.4-cs01` | `8c4d077` | `b9df309` ("Update UBL.xml", 2023-10-24) is the last commit in the batch that set `versionDate: 17 October 2023` (preceded by `e4809af` updating config-UBL.xml and `b448cd7` updating config-UBL-Signature.xml). Initially set to "27 September 2023" at `f204999`, then corrected. Branch tip (`8c4d077`, Jun 2024) includes server testing. Fork point for `ubl-2.5-dev`. |
| UBL 2.4 OS | 20 Jun 2024 | `8c99636` | `ubl-2.4-os` | `779bf4b` | `8c99636` ("update os + date", 2024-06-23) is the last version-setting commit and the fork point for `ubl-2.4-os-iso-pub`. `config-UBL.xml` has `versionDate: 20 June 2024`, `versionDisplay: 2.4`. Branch tip (`779bf4b`, Mar 2025) includes publishing retry. |

## UBL 2.5 Releases

All UBL 2.5 releases are on the `ubl-2.5` branch (no separate branch per stage).

| Release | Date | Release Commit | Branch | Note |
|---------|------|---------------|--------|------|
| UBL 2.5 CSD01 | 20 Aug 2025 | `0b44c38` | `ubl-2.5` | "Merge pull request #28 from oasis-tcs/ubl-2.5-7zip-test". `config-UBL.xml` has `versionDate: 20 August 2025`, `versionDisplay: 2.5 CSD01`. This is also the fork point for `ubl-2.5-python`. |
| UBL 2.5 CSD02 | 03 Dec 2025 | `b122814` | `ubl-2.5` | "Updated date to today" at 13:39 CET (12:39 UTC — matching the zip timestamp `20251203-1239z`). `config-UBL.xml` has `versionDate: 03 December 2025`, `versionDisplay: 2.5 CSD02`. This is also the fork point for `server-test` and `ubl-2.5-2025-layout`. |
| UBL 2.5 CSD03 | 11 Feb 2026 | `3d81e8a` | `ubl-2.5` | Current branch tip. `config-UBL.xml` has `versionDate: 11 February 2026`, `versionDisplay: 2.5 CSD03`. Release in progress. |

## Sources

- **OASIS packages**: Downloaded from Google Drive archive containing official OASIS distribution zips
- **config-UBL.xml**: Contains `versionDate`, `versionDisplay`, `versionDirectory` ENTITY declarations
- **UBL.xml**: DocBook source with `stage`, `version`, `stagetext` ENTITY declarations
- **GitHub Activity API**: Branch creation/push events from `repos/oasis-tcs/ubl/activity`
- **GitHub Actions**: Workflow run list from `gh run list --repo oasis-tcs/ubl`
