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

### PRD3R1, CS and OS, October – December 2006

No package of these three stages is in the archive; they exist only as
published at `https://docs.oasis-open.org/ubl/`. Their schemas say they were
generated on Tue Oct 03 2006, the same as the schemas of the 2.0 Update
(below). See "Published packages compared" for how the three relate.

### UBL 2.0 Update, 2007 – 2008

| Uploaded | By | File | Built | Types | Notes |
|---|---|---|---|---|---|
| 2007-04-16 | Ken Holman | `ubl/submission956/2007-04-16_UBL-2.0-20070415-clsupport.zip` | | | Code list support package |
| 2008-03-14 – 04-11 | Jon Bosak | `ubl/standards/…prd-UBL-2.0-update-delta.zip` (4 uploads) | Tue Oct 03 2006 | 16 | Public review draft of the Update; only the changed schemas, "Manual changes for Update Package by J. Bosak Jan/Feb 2008" |
| 2008-05-10, 05-17 | Jon Bosak | `ubl/standards/…os-UBL-2.0-update-delta.zip` (2 uploads) | Tue Oct 03 2006 | 16 | Update as approved |
| 2009-07-06 | Ken Holman | `ubl/discussion979/2009-07-06_UBL-2.0-Entities-gc-20090706-2240z.zip` | | | All 2.0 entities as one genericode file: the start of the genericode-based build used from 2.1 on |

### How UBL 2.0 grew, August 2005 – December 2006

The archive holds 23 dated uploads with the UBL 2.0 model spreadsheets and 18
with schemas generated from them, between the first phase 1 spreadsheets of
August 2005 and the OASIS Standard of December 2006. Taken in order, they show
how the 2.0 library came about, far more finely than the five published
stages.

How this was measured: every model spreadsheet (`UBL-*.xls`, the source the
schemas were generated from) was read row by row, and each snapshot compared
with the one before it, matching components on their Dictionary Entry Name. A
component that only changed its notation (a qualifier written `Inhouse_ Mail`
instead of `Inhouse Mail`, or an association named with or without its target
class) counts as notation, not as a change. The published packages carry the
same spreadsheets under `mod/`, so the published stages are in the same series.
Dates are the upload date, with the newest file date inside the upload where
the two differ; that shows when the content was last edited.

#### The document types

| First seen | Document types | Notes |
|---|---|---|
| 12 Aug 2005 | Credit Note, Debit Note, Despatch Advice, Invoice, Order, Receipt Advice, Request For Quotation, Self Billed Invoice, Statement; also Account Response, Quote, Remittance, Self Billing Credit Note | Phase 0/1, the procurement documents of UBL 1.0 and their first additions |
| 15 Aug 2005 | Order Cancellation, Order Change, Order Response, Order Response Simple | Phase 1 draft 2. These four were already modelled in Tim McGrath's spreadsheets of 3–4 August 2005, which are only on the mailing list (see below) |
| Nov – Dec 2005 | Bill Of Lading, Certificate Of Origin, Forwarding Instruction, Freight Invoice, Packing List, Waybill | Modelled by the Transportation SC (Tim McGrath, Chi-Yuen Ng, Jern-Kuan Leong) in Enterprise Architect and spreadsheets |
| 19 Jan 2006 (PRD1) | Application Response, Attached Document, Catalogue, Catalogue Deletion, Catalogue Item Specification Update, Catalogue Pricing Update, Catalogue Request, Quotation, Remittance Advice, Self Billed Credit Note, and the six transport documents | 29 document types. Quote becomes Quotation, Remittance becomes Remittance Advice, Self Billing Credit Note becomes Self Billed Credit Note; Account Response is gone |
| 9 Jun 2006 (WD3) | Reminder, Transportation Status | 31 document types, the final number. Forwarding Instruction becomes Forwarding Instructions |

There are no model snapshots from September 2005 to January 2006 on the main
line (only the transport models), nor from February to early June 2006: the
working drafts WD1 and WD2 are not in the archive.

#### The library

Until February 2006 the reusable components were kept in three libraries:
Common, Procurement and, from November 2005, Transportation. From WD3 (June
2006) there is one Common Library. The counts below take the libraries
together.

| Snapshot | Date (newest file) | ABIE | BBIE | ASBIE | What changed |
|---|---|---|---|---|---|
| Phase 0/1 "rough diamond" (Stephen Green) | 12 Aug 2005 | 69 | 319 | 136 | Starting point: Common and Procurement libraries |
| Phase 1 draft 2 (Stephen Green) | 15 Aug 2005 (14 Aug) | 68 | 316 | 138 | `Rounding` removed; `Despatch Line. Back Order Allowed` removed; `Payment. Paid Date Time` added |
| Phase 1 draft 3 (Stephen Green) | 23 Aug 2005 (21 Aug) | 70 | 317 | 153 | `Related Document` and `Response` added; credit and debit note lines get a `Discrepancy Response` instead of reason code and note |
| Phase 1 draft 4 (Sylvia Webb) | 31 Aug 2005 (30 Aug) | 70 | 317 | 155 | `Item Instance` moves from `Item` to the despatch and invoice lines |
| Transportation library (TSC) | 21 Nov and 9 Dec 2005 | 99 | 522 | 262 | Third library, with the transport components |
| **PRD1** (published) | 19 Jan 2006 | 104 | 541 | 278 | 166 components removed and 547 added against draft 4: the catalogue, transport and response components; many definitions rewritten (342) |
| Library with CC IDs (Tim McGrath) | 1 Feb 2006 (31 Jan) | 105 | 545 | 279 | PRD1 library with candidate Core Component identifiers, for the submission to UN/CEFACT |
| WD3 (Sven Rasmussen) | 9 Jun 2006 (8 Jun) | 113 | 612 | 314 | The three libraries merged into one. Added: `Billing Reference` and its line, `Price`, `Pricing Reference`, `Location`, `Line Reference`, `Line Response`, `Reminder Line`, the catalogue request and update lines; removed: `Accounting Document Reference` and its line, `Base Price`, `Port`. 84 components renamed, 218 added, 97 removed, 19 cardinalities changed. `Consignment` is now `Transport Handling Unit` in the UBL names |
| WD3 with QDT | 13 Jun 2006 | 113 | 612 | 314 | Same library; a spreadsheet of qualified data types added |
| WD4 | 16 Jun 2006 | 113 | 614 | 314 | `Attention Of`/`Care Of` become `Mark Attention`/`Mark Care`; `To Be Paid Amount` becomes `Payable Amount`; `Party. Website Identifier` becomes `Website_ Uniform Ressource Identifier` (UBL name `WebSiteURI`); `Transport Contract` moves from `Shipment` to `Consignment` |
| WD5 | 19 Jun 2006 | 113 | 614 | 320 | Catalogue lines get contractor and seller parties; `Copy Indicator` optional |
| WD7 | 30 Jun 2006 | 113 | 614 | 320 | Three definitions |
| WD8 (Tim McGrath) | 10 Jul 2006 | 113 | 613 | 320 | Property terms made explicit in 112 entries (`Allowance Charge. Reason. Code` becomes `Allowance Charge. Allowance Charge Reason Code. Code`); `Reason` becomes `AllowanceChargeReason`; `Classification Scheme. Status` removed |
| WD9 (Jon Bosak) | 16 Jul 2006 (14 Jul) | 113 | 613 | 320 | `Universally Unique Identifier` becomes `UUID` |
| **PRD2** (published) | 28 Jul 2006 (27 Jul) | 113 | 613 | 320 | Same as WD9 |
| PRD3 spreadsheets (Alan Lemming) | 30 Aug 2006 | 113 | 618 | 322 | `Legal Total` becomes `Monetary Total`, `Tax Sub Total` becomes `Tax Subtotal`; codes made specific (`Address. Code` → `Address Type Code`, `Chip` → `Card Chip Code`, …); `EndPointID` → `EndpointID`; 887 definitions rewritten |
| PRD3 schema test 2 and 3 | 6 and 7 Sep 2006 | 113 | 618 | 322 | Representation terms corrected (`Goods Item. Quantity` was `Numeric`, now `Quantity`; `Status. Percent` now `Percent`) |
| PRD3_7 (Sylvia Webb) | 9 Sep 2006 (8 Sep) | 113 | 620 | 332 | Credit and debit note lines get credited/debited quantity, delivery, item and price; credit and debit notes get despatch and receipt line references |
| PRD3_8 | 11 Sep 2006 (10 Sep) | 113 | 620 | 332 | Credit and debit note line `Item` and `Line Extension Amount` made optional |
| PRD3_9, PRD3_10 | 12 Sep 2006 | 113 | 620 | 332 | No change in the library |
| **PRD3** (published) | 21 Sep 2006 | 113 | 620 | 332 | Same as PRD3_10 |
| **PRD3R1** (published) | 5 Oct 2006 | 113 | 620 | 332 | 106 definitions in the library and 214 in the documents rewritten; `ServiceCode` becomes `TransportServiceCode` |
| **CS**, **OS** (published) | 12 Oct, 12 Dec 2006 | 113 | 620 | 332 | No change |

Three periods stand out. In August 2005 the library was small and stable while
the documents were being worked out. Between September 2005 and June 2006,
mostly outside the archive, it grew from 70 to 113 aggregates as the
catalogue, transport and response documents were added. From June to
September 2006 the aggregates stayed at 113 while their members were renamed,
moved and completed; after PRD3 only definitions changed.

#### The schemas generated from the models

The schemas follow the models a few days later. Comparing each schema round
with the one before it, on the common aggregate components
(`UBL-CommonAggregateComponents-2.0.xsd`), gives the same story, with one
episode that is in the schemas only: from WD4 to WD6 the schema generation
added the representation term to almost every element name (`CityName`
became `CityNameName`, `Line` became `LineText`, `AccountID` became
`AccountIDID`). The spreadsheets of those weeks still say `CityName`, so this
was a setting of the generation, not a modelling decision; it was dropped
again in the WD7 schemas of 3 July 2006 and is in no published package.

| Round | ABIEs | What changed |
|---|---|---|
| PRD1, 19 Jan 2006 | 107 | Starting point |
| WD4 schemas, 18 Jun | 113 | The aggregates added and removed in WD3 (above); the doubled element names (219 names gone, 263 new); `ActualDeliveryDateTime` split into date and time |
| WD5, 20 Jun | 113 | `DocumentReference/CopyIndicator` becomes optional |
| WD6, 28 Jun | 113 | No change in the aggregates |
| WD7 schemas, 3 Jul | 113 | Element names back to the model names (`CityName`, `Line`, `AccountID`), keeping the split of date-time into date and time |
| PRD2 candidates, 4 and 6 Jul | 113 | The document schemas are added: 30, then 31 |
| PRD2 GEFEG build, 13 Jul | 113 | The WD8 renames (`AllowanceChargeReason`, `StatusReason`, …); `UniversallyUniqueID` becomes `UUIDID`; `URI` becomes `URIID` |
| wd9spec, 14 Jul | 113 | Final namespaces |
| PRD2 sanity check, 17 Jul | 113 | `UUIDID` becomes `UUID`; 16 aggregates with new definitions |
| PRD2, 28 Jul | 113 | As the sanity check |
| PRD3 schema test 2, 6 Sep | 113 | The PRD3 spreadsheet changes (`MonetaryTotal`, `TaxSubtotal`, specific code names); 95 aggregates with new definitions |
| PRD3 schema test 3, 7 Sep | 113 | `GoodsItem/Quantity`, `Status/Percent`; leftover doubled names (`TimingComplaintCodeCode`) fixed |
| PRD3_7, 9 Sep | 113 | `CreditedQuantity`, `DebitedQuantity` |
| PRD3_8, 10 Sep | 113 | `CreditNoteLine/LineExtensionAmount` optional |
| PRD3_10, 12 Sep | 113 | The PRD3 schemas as published |
| PRD3R1, 5 Oct | 113 | 53 aggregates with new definitions |
| CS, OS | 113 | No change |

The schema counts (107 at PRD1) and the model counts (104) differ because
the schemas also declare some aggregates that the models keep in the document
spreadsheets.

### How the specification text grew, 2004 – 2008

The models and schemas are only part of UBL 2.0. The specification document
itself (introduction, context of use, the business processes, release notes,
the appendices on code lists, design rules and upgrading from 1.0) was
written alongside them. The archive holds six unpublished drafts of that text around the
public review drafts, and its sources from 2005.

**It was not DocBook from the start.** Up to and including PRD3 the
specification was a hand-written XHTML file (`index.html`, from 19 July 2006
`UBL-index-2.0.html`) with the internal stylesheet and `W3C-REC.css`
reference of the UBL 1.0 specification of 2004. DocBook XML 4.4 arrived with
PRD3R1 on 5 October 2006: `UBL-2.0.xml` is from then on "the 'original' of
this specification", the HTML is generated with the DocBook XSL stylesheets
1.69.1 and the OASIS specification stylesheets, and the package carries them
in `db/` and `css/`. Every PDF, from PRD1 to OS, was printed from the HTML
with OpenOffice.org 2.0; PRD1 says the PDF "has no practical purpose and
should be ignored", and the OS PDF was made on 18 December 2006, six days
after the standard's date. The 2.0 Update of 2008 is a separate OpenOffice
Writer document.

How this was measured: the text of each version was taken from its HTML, the
section numbers removed (they shift as sections move), and each version
compared word by word with the one before. "Words" is the size of that text.

| Version | File date | By | Format | Words | Change from the previous version |
|---|---|---|---|---|---|
| UBL 1.0 CD (`cd-UBL-1.0`) | 15 Sep 2004 | Jon Bosak | XHTML | about 9,600 | Starting point: about a quarter of the first 2.0 draft is text of the 1.0 specification |
| `wd-UBL-2.0` "Candidate UBL 2.0 CD 1 for initial public review" | 8 Jan 2006 | Jon Bosak | XHTML, PDF | 11,415 | First 2.0 text in the archive |
| **PRD1** (published) | 19 Jan 2006 | Jon Bosak, Tim McGrath (editors) | XHTML, PDF | 11,488 | +105 −31: stage and locations; the note on the PDF; copyright 2006 |
| `2-test01` "Just a mechanical test -- incomplete" | 9 Jul 2006 | Jon Bosak | XHTML | 14,234 | +4,900 −2,198: the UBL 1.0 material in the introduction moves to a new appendix "Upgrading from UBL 1.0 to UBL 2.0"; the transport documents get full descriptions and the document type table almost doubles; the code list appendix is rewritten for two-phase validation (`cl/gc/default`, `cl/gc/cefact`, `cl/gc/special-purpose`); the methodology and model appendices are rewritten |
| `2-prd2-sanity1` | 17 Jul 2006 | Jon Bosak | XHTML | 14,856 | +886 −286: the extension element `UBLExtensions` and the extension schemas; `cl/xsdcl`; the ASN.1 appendix; "Collaboration" dropped from the process headings; Forwarding Instruction becomes Forwarding Instructions |
| `2-prd2-sanity3` | 19 Jul 2006 | Tim McGrath | XHTML | 14,943 | +112 −29: the file is renamed `UBL-index-2.0.html`; imported code list schemas; "Customization and Profiling" becomes "Customization" |
| `2-prd2-cd` | 20 Jul 2006 | Tim McGrath | XHTML | 14,984 | +61 −20: code list schemas, acknowledgements |
| `prd2-UBL-2.0-test` | 24 Jul 2006 | Jon Bosak | XHTML, PDF | 14,972 | +4 −16; its PDF is the published one (same SHA-256) |
| **PRD2** (published) | 27 Jul 2006 | Jon Bosak, Ken Holman, Tim McGrath | XHTML, PDF | 14,948 | +3 −27 |
| **PRD3** (published) | 21 Sep 2006 | same | XHTML, PDF | 19,784 | +7,107 −2,313: the new OASIS title page (artifact type and identifier, chairs) with the notices in front; a new section 7, "Additional Document Constraints" (validation, character encoding, empty elements); a table of about 4,500 words of changes to the basic information entities since UBL 1.0; "Report Status of Goods"; "Business Rules" becomes "Business Rules Assumed"; "Supporting Materials" becomes the "Support Package" |
| **PRD3R1** (published) | 5 Oct 2006 | same | **DocBook XML**, HTML, PDF | 20,134 | +602 −332: converted to DocBook with little change to the text; the normative references move to the end, so the sections renumber (Context of Use becomes section 4); the ASN.1 modules are added |
| **CS** (published) | 12 Oct 2006 | same | DocBook XML, HTML, PDF | 20,134 | +25 −24: stage and date |
| **OS** (published) | 12 Dec 2006 | same | DocBook XML, HTML, PDF | 20,339 | +453 −248: the notices of the new OASIS IPR Policy; a link to the errata page |

No drafts of the text are in the archive between January and July 2006, nor
between PRD2 and PRD3, nor for the conversion to DocBook. The two change logs
of 2006 (PRD1 to PRD2, PRD2 to PRD3) cover the models only, not the text.

**Where the first text came from.** Much of the Context of Use in the January
2006 draft was taken from the process proposals of the subcommittees. Counting
runs of eight words that appear in both, 37% of section 5 is found in three
documents from the archive:

| Source in the archive | By | Date | Sections of the January 2006 draft taken from it |
|---|---|---|---|
| "Proposal for UBL 2.0 process", version 10 (`ubl-psc/business1404`) | Sylvia Webb (Procurement SC) | 30 Aug 2005 | Punchout (72%), Fulfilment (80%), Billing (70%), Traditional Billing (66%), Self Billing (46%) |
| "Proposal for UBL 2.0 Catalogue process", 6 Nov 2005 (in `catalogue20051107.zip`) | Tim McGrath for the catalogue working group | 9 Nov 2005 | Items (62%), Catalogue Provision (42%) |
| "Proposal for UBL 2.0 transport process", five versions 4–22 Dec 2005 | Jern-Kuan Leong, Chi-Yuen Ng (Transportation SC) | 21 Dec 2005 | Initiate Transport Services (71%), Forwarding Instruction (75%), Bill of Lading (89%), Waybill (67%), Certification of Origin (63%), Freight Billing (44%) |

About 43% of the transport proposal is in the specification word for word,
and between a quarter and a third of it is still there in the OS.

**The 2.0 Update, 2008.** "UBL 2.0 Errata 01" is a separate document of about
6,500 words, edited by Jon Bosak, Ken Holman and Tim McGrath in OpenOffice
Writer with the OASIS template. Its drafts are in the update packages:
14 March 2008 (6,298 words), 18 March (+367 −194), 26 March (+428 −397),
11 April (+52 −51; published as `prd-UBL-2.0-update.pdf`), 10 May (+108 −81;
the approved `os-UBL-2.0-update.pdf`), and 17 May (the same text, re-uploaded).
Ken Holman's "UBL Methodology for Code List and Value Validation" (version
0.8, drafts D2 to D6, January – June 2007) is in DocBook with the OASIS
template, but shares only about 4% of its text with the Update.

### What the mailing lists add, 2005 – 2006

Not everything was uploaded to Kavi: much was sent to the TC mailing lists as
attachments. The live list archive at `lists.oasis-open.org` is behind a
browser check, but the Internet Archive (Wayback Machine) holds copies. For
2005 – 2008 it has every monthly index of `ubl`, `ubl-psc`, `ubl-tsc`,
`ubl-dev` and `ubl-comment`, and a part of the messages:

| List | Messages 2005 – 2008 | Captured | Notes |
|---|---|---|---|
| `ubl` | 3,382 | 2,421 (72%) | Complete for most months; almost nothing for May, June and August 2006 |
| `ubl-psc` (Procurement SC) | 570 | 263 (46%) | |
| `ubl-tsc` (Transportation SC) | 395 | 321 (81%) | |
| `ubl-dev` | 1,752 | 407 (23%) | |
| `ubl-comment` | 1,861 | 313 (17%) | |

51 attachments from June 2005 to April 2006 were captured. Only two of
them are in Kavi as they are. The ones that matter for the 2.0 chain:

| Sent | By | Message | Attachment | What it is |
|---|---|---|---|---|
| 5 Jul 2005 | Tim McGrath | `ubl` 200507/msg00005 "Proposal for UBL 2.0 Extended Procurement Process Model" | `Proposal for UBL 2.0 process_09.pdf` | Version 9 of the procurement process proposal, the source of much of the Context of Use; version 10 followed on 12 July (msg00033) and is the file later uploaded to Kavi |
| 15 Jul 2005 | David Kruppke (GEFEG) | `ubl` 200507/msg00074 "UBL 2.0 schemas" | `xsd.zz`, `xsdrt.zz` | The earliest UBL 2.0 schemas found: generated on 14 July 2005, draft namespaces, 8 document types (the UBL 1.0 set), 60 aggregates, 234 basic components, with code list schemas |
| 19 Jul 2005 | Tim McGrath | `ubl` 200507/msg00097 "Draft of Templates for UBL 2.0 spreadsheets" | `UBL-2.0-templates.zzz` | The 2.0 spreadsheet templates: Invoice, Common and Procurement libraries (59 ABIEs, 257 BBIEs, 104 ASBIEs) |
| 4 Aug 2005 | Tim McGrath | `ubl` 200508, zip00000 | 10 spreadsheets `…-20050803-tm.xls` | Model snapshot: the Order documents, including Order Change, Order Response, Order Response Simple and Order Cancellation; library 62/278/105 |
| 9 Aug 2005 | (Ottawa face-to-face) | `ubl` 200508, zip00003 and zip00005 | `ModelSpreadsheets-20050809-f2f`, Additions list of 8 Aug | Model snapshot during the meeting; library 62/281/105 |
| 10 Aug 2005 | (Ottawa face-to-face) | `ubl` 200508, bin00004 | `Model-Fulfilment-20050810-tl` | Despatch Advice and Receipt Advice models, with the EA model and slides |
| April 2006 | Procurement SC | `ubl-psc` 200604 | five spreadsheets | Comments on PRD1 from the public review (issues ISS-4 to ISS-171, and a sheet of general comments that starts with the layout of `index.pdf`) |

The issues list of 2.0 was also kept on the list: Stephen Green and Tim
McGrath sent `UBL-2-0-Additions_v0507xx` versions on 6, 11, 17, 18, 19 and
24 July 2005, before the first Kavi upload of 12 August. Of these, only the
names are known so far where the Wayback Machine did not keep the file.

So the series of model snapshots now starts on 19 July 2005, three weeks
before the first Kavi upload, and the first generated 2.0 schemas are from
14 July 2005. The download of the remaining captured messages was cut short
when the Wayback Machine stopped answering; 149 of about 2,700 have been read.

### Published packages compared

The UBL 2.0 packages published at `https://docs.oasis-open.org/ubl/`,
downloaded on 9 October 2026, compared file by file with each other and with
the Kavi uploads. Working backwards from the OASIS Standard:

| Published package | Bytes | SHA-256 (first 16) | Files | Stage on the title page | In Kavi? |
|---|---|---|---|---|---|
| `os-UBL-2.0.zip` | 32,192,754 | `d3eb3356d425bcf1` | 752 | OASIS Standard, 12 December 2006 | No |
| `cs-UBL-2.0.zip` | 32,188,680 | `820791475696948b` | 752 | Committee Specification, 12 October 2006 | No |
| `prd3r1-UBL-2.0.zip` | 32,190,155 | `626dc7a9fa82cecf` | 752 | Committee Specification, 5 October 2006 | No |
| `prd3-UBL-2.0.zip` | 31,576,116 | `cf5595a2103b258a` | 633 | (no specification document; files dated 21 September 2006) | Schemas only |
| `prd2-UBL-2.0.zip` | 30,471,968 | `4dbbc56364a41f21` | 623 | Public Review Draft 2 | **Yes, the same zip** |
| `prd-UBL-2.0.zip` | 12,443,604 | `b37bd8a7e990c00b` | 198 | Public Review Draft | **Yes, the same zip** |
| `os-UBL-2.0-update-delta.zip` | 8,703,923 | `8e2b160b97281236` | 289 | UBL 2.0 Update | **Yes, the same zip** |

**OS = CS apart from the stage identification.** 747 of the 752 files are
identical, including every schema, code list, model and example. The
differences are the specification document (`UBL-2.0.xml`, `.html`, `.pdf`:
"Committee Specification" becomes "Standard", the date becomes 12 December
2006, the location points to `os-UBL-2.0`, the OASIS notices are replaced by
the newer copyright and IPR text, and a pointer to the errata page is added),
the stylesheet (`css/spec.css` becomes `css/oasis-standard.css`), and one model
spreadsheet (`mod/maindoc/UBL-CatalogueDeletion-2.0.xls`) whose bytes differ.

**CS = PRD3R1 apart from the date and editorial touches.** 746 of 752 files
are identical, again including all schemas. The package published as `prd3r1`
already calls itself "Committee Specification, 5 October 2006" and names
`cs-UBL-2.0` as its current version: it is the CS candidate. The CS of 12
October changes the date, a few headings and words ("implementors" becomes
"implementers"), one DocBook stylesheet (`db/UBL-2.0-html.xsl`) and the ASN.1
files (the order of two elements in Receipt Advice).

**PRD3R1 differs from PRD3 in content.** The schemas were regenerated on
3 October 2006: the document and common schemas carry revised definitions (for
example "A computer-generated universally unique identifier (UUID) for the
Invoice instance" becomes "A universally unique identifier for an instance of
this ABIE"), and the code-list schemas point to the genericode files by their
full name (`…/AccountTypeCode-2.0` becomes `…/AccountTypeCode-2.0.gc`). Both
already point to `os-ubl-2.0` locations. PRD3R1 also adds the ASN.1 modules,
the stylesheets for each stage, and the specification document in place of
the PRD3 index.

**PRD3 = the last Kavi schema round, plus one later file.** Of the 43
document and common schemas in the published PRD3, 42 are byte-identical to
`2006-09-12_UBL_2.0_PRD3_10.zip`. The one other, `UBL-QualifiedDatatypes-2.0.xsd`,
was generated again on Tue Sep 19 2006 and derives the code types from
`udt:CodeType` where the Kavi upload has `xsd:normalizedString`. The 90 code-list
schemas and the rest of the PRD3 package are not in Kavi.

**PRD2 is in Kavi, with its candidates.** `2006-07-28_prd2-UBL-2.0.zip` is the
published zip. The candidate of 21 July (`2-prd2-cd`) differs from it in four
files: the index page was titled "Second Public Review Draft Candidate" where
the published one says "Second Public Review Draft", two schemas included
`UBL-ExtensionContentDataType-2.0.xsd` while the file is named
`UBL-ExtensionContentDatatype-2.0.xsd` (fixed in the published package), and
a test script; it also had
an ASN.1 readme instead of the ASN.1 package and no PDF index. The check build
of 25 July differs in one file, a paragraph of the release notes.

**PRD1 is in Kavi, with its working draft.** `2006-01-19_prd-UBL-2.0.zip` is the
published zip. The working draft of 8 January (`wd-UBL-2.0`) has the same 198
files; the 74 that differ differ only in their header comments: the copyright
year 2005 becomes 2006, and "Copyright updated: Thu Jan 19 2006" and
"Annotations stripped: Thu Jan 19 2006" replace "Stripped: Sun Jan 1 2006".

**The 2.0 Update is in Kavi.** `2008-05-17_os-UBL-2.0-update-delta.zip` is the
published zip. The earlier uploads of March to May 2008 are its review
drafts.

So for UBL 2.0 the chain is complete for the schemas from PRD1 to PRD3. The
step from PRD3 to the final schemas (the regeneration of 3 October 2006)
happened outside Kavi; after it, CS and OS only changed the identification of
the stage in the specification document.
