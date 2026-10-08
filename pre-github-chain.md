# UBL before GitHub: the build chain from 2.0 to 2.3

DRAFT. Section UBL 2.0 only; 2.1, 2.2 and 2.3 follow.

The OASIS UBL TC kept its work in the Kavi document repository of OASIS until
the GitHub repository `oasis-tcs/ubl` took over (first 2.3 content: 15 May
2021, see `release-commit-mapping.md`). There were no commits before that: UBL
never used the OASIS Subversion server. What remains are the files the TC
uploaded, one file per upload, with the date and the uploader.

This document lists those uploads that belong to the UBL 2.x build line, from
the start of 2.0 to the start of GitHub: the models the schemas were made from
(the inputs), the schemas and packages that came out (the outputs), and the
build tooling. It leaves out the localisations, the NDR, the IDD and the other
separate specifications, and the meeting and discussion papers.

## Source

`UBL-TC-Kavi-document-history-2026-10-08.zip`, prepared by OASIS for the UBL
TC on 8 October 2026 from its copy of the Kavi file store: 1,442 files, 8.99 GB
(8,988,353,483 bytes; SHA-256
`877475dc3a66341283df28886914e002458e2b686e3fbbdf59c6edccb62c9047`; S3 ETag
`78da4f78a3195df757d4d7388a8bf7ca-1072`). Every file was checked against the
SHA-256 in the archive's `INDEX.csv`.

Paths below are relative to `files/` in that archive. "Uploaded" is the Kavi
upload date; "Built" is the "Generated on" (or "Generated On") line in the
schemas of the package, as written by the tool that made them. "Types" is the
number of document types: distinct `maindoc` schemas (most packages hold each
one twice, in `xsd` and `xsdrt`).

## UBL 2.0

The UBL 2.0 models and schemas were made with GEFEG.FX: the working drafts
come with "spreadsheets and GEFEG model", one PRD3 upload was zipped straight
from `Documents and Settings/Sylvia/My Documents/Gefeg/ubl/UBL 2.0 PRD3/…`,
and the schema headers carry a "Generated On" line in one fixed format. Jon
Bosak put the review packages together.

### Models, August 2005 – February 2006

The first 2.0 models were spreadsheets per document, kept by the
subcommittees.

| Uploaded | By | File | What |
|---|---|---|---|
| 2005-08-12 | Stephen Green | `ubl/discussion979/2005-08-12_ModelSpreadsheets-20050811-sdg.zip` | "'rough diamond' set of model UBL 2.0 phase 0 and phase 1 spreadsheets" |
| 2005-08-15 | Stephen Green | `ubl/discussion979/2005-08-15_ModelSpreadsheets-UBL-2-0-phase-1-draft-2-20050814.zip` | Phase 1 draft 2 |
| 2005-08-23 | Stephen Green | `ubl/discussion979/2005-08-23_ModelSpreadsheets-UBL-2-0-phase-1-draft-3-20050818.zip` | Phase 1 draft 3 |
| 2005-08-31 | Sylvia Webb | `ubl-psc/technical1405/2005-08-31_ModelSpreadsheets-UBL-2-0-phase-1-draft-4-20050829.zip` | Phase 1 draft 4 |
| 2005-11-14 – 2005-12-21 | Tim McGrath, Chi-Yuen Ng, Jern-Kuan Leong | `ubl-tsc/calendar/…UBL-TransportationLibrary-2.0-*` (17 uploads) | Transport documents and library, as Enterprise Architect models and spreadsheets |
| 2005-12-09 | Chi-Yuen Ng | `ubl-tsc/calendar/2005-12-09_UBL-LibrarySpreadsheets-2.0-20051208.zip` | Library spreadsheets |
| 2006-02-01 | Tim McGrath | `ubl/submission956/2006-02-01_UBL-ModelLibrary-2-withCCID.zip` | "Library Spreadsheets with Core Components" |

### PRD1, January 2006

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2006-01-08 | Jon Bosak | `ubl/standards/2006-01-08_wd-UBL-2.0.zip` | Sat Dec 31 10:07:46 2005 | 29 | Working draft package, 198 files |
| 2006-01-19 | Jon Bosak | `ubl/standards/2006-01-19_prd-UBL-2.0.zip` | Sat Dec 31 10:07:46 2005 | 29 | First public review draft; schemas still in the `urn:oasis:names:draft:ubl` namespaces; "Copyright updated: Thu Jan 19 2006" |

### From PRD1 to PRD2, March – July 2006

The models moved from per-document spreadsheets to one set of working drafts
(WD3 to WD9), made with GEFEG and published as spreadsheets in Excel and
OpenDocument form. Ken Holman's first modelling tools appear alongside.

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2006-03-09 | Ken Holman | `ubl/temporary919/2006-03-09_wd-UBL-2-20060101-*.zip` (7 files) | | | XPath listings per document of the 2006-01-01 draft |
| 2006-06-09 | Sven Rasmussen | `ubl/standards/2006-06-09_UBL 2.0 WD3.zip` | | | WD3 spreadsheets |
| 2006-06-10 – 06-20 | Ken Holman | `ubl/discussion979/…gkholman-ubl-modeling-0.1` to `0.4` | | | Modelling tools (see Tooling) |
| 2006-06-13 | Sven Rasmussen | `ubl/standards/2006-06-13_UBL 2.0 WD3_With_QDT.zip` | | | WD3 with qualified data types |
| 2006-06-16 | Sven Rasmussen | `ubl/standards/2006-06-16_UBL 2.0 WD4.zip` | | | WD4 spreadsheets and GEFEG model |
| 2006-06-18 | Sylvia Webb | `ubl/standards/2006-06-18_UBL 2.0_WD4_draft1.zip` | | | WD4 schemas |
| 2006-06-19 | Sven Rasmussen | `ubl/standards/2006-06-19_UBL 2.0 WD5.zip` | | | WD5 spreadsheets and GEFEG model |
| 2006-06-21 | Ken Holman | `ubl/temporary919/2006-06-21_wd-UBL-20060101-codelists-20060621-1820z.zip` | | | Code lists, genericode |
| 2006-06-30 | Sven Rasmussen | `ubl-psc/technical1405/2006-06-30_UBL 2.0 WD7.zip` | | | WD7 spreadsheets, with change log |
| 2006-07-04 | Sylvia Webb | `ubl/standards/2006-07-04_UBL2.0_PRD2.zip` | Tue Jul 04 2006 | 30 | First PRD2 schemas, still "draft" namespaces |
| 2006-07-06 | Sylvia Webb | `ubl/standards/2006-07-06_UBL2.0PRD2a.zip` | Thu Jul 06 2006 | 31 | |
| 2006-07-10 | Tim McGrath | `ubl/standards/2006-07-10_UBL 2.0 WD8.zip` | | | WD8 |
| 2006-07-16 | Jon Bosak | `ubl/temporary919/2006-07-16_UBL 2.0 WD9.zip` | | | "PRD2 WD9 Spreadsheets" |

### PRD2, July 2006

On 14 July 2006 the schemas move to the final `urn:oasis:names:specification:ubl`
namespaces; all PRD2 packages carry schemas generated that day.

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2006-07-17 | Jon Bosak | `ubl/temporary919/2006-07-17_2-prd2-sanity1.zip` | Fri Jul 14 2006 | 31 | "UBL 2.0 PRD2 sanity check", 626 files |
| 2006-07-19 | Ken Holman | `ubl/standards/2006-07-19_wd9ext-20060719-0240z.zip` | Fri Jul 14 2006 | 31 | Revised schemas after the Pacific meeting of 17 July |
| 2006-07-21 | Tim McGrath | `ubl/standards/2006-07-21_2-prd2-cd.zip` | Fri Jul 14 2006 | 31 | "Committee Draft for second public review" |
| 2006-07-25 | Jon Bosak | `ubl/temporary919/2006-07-25_prd2-UBL-2.0-test.zip` | Fri Jul 14 2006 | 31 | Check build before submission |
| 2006-07-26 | Jon Bosak | `ubl/comment1140/2006-07-26_ChangeLogPRD1-to-PRD2.zip` | | | Change log PRD1 → PRD2 |
| 2006-07-28 | Jon Bosak | `ubl/standards/2006-07-28_prd2-UBL-2.0.zip` | Fri Jul 14 2006 | 31 | PRD2 as submitted, 623 files; schemas "Modified 2006-07-19 … to include references to extension constructs" |

### PRD3, September 2006

PRD3 was a schema-only round: spreadsheets, then a series of schema generation
tests until a "final".

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2006-08-30 | Alan Lemming | `ubl/temporary919/2006-08-30_UBL 2.0 PRD3.zip` | | | PRD3 spreadsheets |
| 2006-09-06 | Alan Lemming | `ubl/temporary919/2006-09-06_PRD3 schema test 2.zip` | Wed Sep 06 2006 | 31 | |
| 2006-09-07 | Alan Lemming | `ubl/temporary919/2006-09-07_PRD3 Schema test 3.zip` | Thu Sep 07 2006 | 31 | |
| 2006-09-09 | Sylvia Webb | `ubl/temporary919/2006-09-09_UBL 2.0_PRD3_7.zip` | Sat Sep 09 2006 | 31 | "PRD3 Schema generation Final" |
| 2006-09-09 | Sylvia Webb | `ubl/temporary919/2006-09-09_UBL 2.0_PRD4.zip` | | | GEFEG model file only |
| 2006-09-11 | Sylvia Webb | `ubl/temporary919/2006-09-11_UBL 2.0_PRD3_8.zip` | Sun Sep 10 2006 | 31 | Zipped from the GEFEG working folder |
| 2006-09-12 | Sylvia Webb | `ubl/temporary919/2006-09-12_UBL 2.0_PRD3_9.zip` | Tue Sep 12 2006 | 31 | |
| 2006-09-12 | Sylvia Webb | `ubl/temporary919/2006-09-12_UBL_2.0_PRD3_10.zip` | Tue Sep 12 2006 | 31 | Last PRD3 schema set |
| 2006-09-20 | Jon Bosak | `ubl/comment1140/2006-09-20_ChangeLogPRD2-to-PRD3.zip` | | | Change log PRD2 → PRD3 |

### CS and OS, October – December 2006

No CS or OS package of UBL 2.0 is in the archive. The schemas of the 2.0
Update (below) say they were generated on Tue Oct 03 2006, which dates the
final 2.0 schemas.

### UBL 2.0 Update, 2007 – 2008

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2007-04-16 | Ken Holman | `ubl/submission956/2007-04-16_UBL-2.0-20070415-clsupport.zip` | | | Code list support package |
| 2008-03-14 – 04-11 | Jon Bosak | `ubl/standards/…prd-UBL-2.0-update-delta.zip` (4 uploads) | Tue Oct 03 2006 | 16 | Public review draft of the Update; only the changed schemas, "Manual changes for Update Package by J. Bosak Jan/Feb 2008" |
| 2008-05-10, 05-17 | Jon Bosak | `ubl/standards/…os-UBL-2.0-update-delta.zip` (2 uploads) | Tue Oct 03 2006 | 16 | Update as approved |
| 2009-07-06 | Ken Holman | `ubl/discussion979/2009-07-06_UBL-2.0-Entities-gc-20090706-2240z.zip` | | | All 2.0 entities as one genericode file: the start of the genericode-based build used from 2.1 on |

### To check in a later step

- Which of these packages are byte-identical to the published PRD1, PRD2, PRD3,
  CS, OS and Update packages at `https://docs.oasis-open.org/ubl/`.
