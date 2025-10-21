# Repository Reorganization Proposal

This document presents a proposal for reorganizing the repository to improve clarity and maintainability.

## File Analysis and Classification

The following table classifies each file in the repository based on its role in the build process.

| File Path | Classification | Used By |
|---|---|---|

| `build.sh` | Build Logic | User, GitHub Actions |
| `build-common.sh` | Build Logic | `build.sh` |
| `build.xml` | Build Logic | `build-common.sh` |
| `UBL.xml` | Primary Input | `build.xml` |
| `RealtaServerAnt.xml` | Build Logic | `build.xml` |
| `UBL-Party-summary-information.xml` | Primary Input | `build.xml` |
| `UBL-Schema-summary-information.xml` | Primary Input | `build.xml` |
| `config-UBL.xml` | Primary Input | `build.xml` |
| `config-UBL-Signature.xml` | Primary Input | `build.xml` |
| `ident-UBL.xml` | Primary Input | `build.xml` |
| `ident-UBL-Signature.xml` | Primary Input | `build.xml` |
| `ident-UBL-Endorsed.xml` | Primary Input | `build.xml` |
| `massageModelName.xml` | Primary Input | `build.xml` |
| `realta-user-parameters.xml` | Primary Input | `build.xml` |
| `assembleEntities.xsl` | Build Logic | `build.xml` |
| `gc2endorsed.xsl` | Build Logic | `build.xml` |
| `gc2sch.xsl` | Build Logic | `build.xml` |
| `hub-integrity.xsl` | Build Logic | `build.xml` |
| `hub2processSummary.xsl` | Build Logic | `build.xml` |
| `namespaceCheck.xsl` | Build Logic | `build.xml` |
| `partydoc2db.xsl` | Build Logic | `build.xml` |
| `schemadoc2db.xsl` | Build Logic | `build.xml` |
| `UBL-CVA-Skeleton.cva` | Primary Input | `build.xml` |
| `UBL-DefaultDTQ-2.5.sch` | Primary Input | `build.xml` |
| `UBL-Entities-2.4-os.gc` | Versioned Data | `build.xml` |
| `UBL-Signature-Entities-2.4-os.gc` | Versioned Data | `build.xml` |
| `skeletonDisplayEditSubset.ods` | Primary Input | `build.xml` |
| `spellcheck-UBL.txt` | Primary Input | `build.xml` |
| `art/` | Static Asset | `build.xml` |
| `htmlart/` | Static Asset | `build.xml` |
| `images/` | Static Asset | `art/`, `htmlart/` |
| `db/` | Tooling | `build.xml` |
| `os-UBL-*/` | Versioned Data | `build.xml` |
| `raw/` | Primary Input | `build.xml` |
| `utilities/` | Tooling | `build-common.sh`, `build.xml` |

## Proposed Directory Structure

Based on the file classifications, I propose the following directory structure:

```
/
|-- build/
|   |-- build.sh
|   |-- build-common.sh
|   |-- build.xml
|   |-- RealtaServerAnt.xml
|   |-- assembleEntities.xsl
|   |-- gc2endorsed.xsl
|   |-- gc2sch.xsl
|   |-- hub-integrity.xsl
|   |-- hub2processSummary.xsl
|   |-- namespaceCheck.xsl
|   |-- partydoc2db.xsl
|   |-- schemadoc2db.xsl
|
|-- data/
|   |-- UBL-CVA-Skeleton.cva
|   |-- UBL-DefaultDTQ-2.5.sch
|   |-- UBL-Entities-2.4-os.gc
|   |-- UBL-Signature-Entities-2.4-os.gc
|   |-- skeletonDisplayEditSubset.ods
|   |-- spellcheck-UBL.txt
|
|-- docs/
|   |-- UBL.xml
|   |-- UBL-Party-summary-information.xml
|   |-- UBL-Schema-summary-information.xml
|
|-- config/
|   |-- config-UBL.xml
|   |-- config-UBL-Signature.xml
|   |-- ident-UBL.xml
|   |-- ident-UBL-Signature.xml
|   |-- ident-UBL-Endorsed.xml
|   |-- massageModelName.xml
|   |-- realta-user-parameters.xml
|
|-- assets/
|   |-- art/
|   |-- htmlart/
|   |-- images/
|
|-- tooling/
|   |-- db/
|   |-- utilities/
|
|-- releases/
|   |-- os-UBL-2.0/
|   |-- os-UBL-2.1/
|   |-- os-UBL-2.2/
|   |-- os-UBL-2.3/
|   |-- os-UBL-2.4/
|
|-- src/
|   |-- raw/
|
|-- jules/
|   |-- thoughts/
|   |   |-- jules-thoughts.md
|   |   |-- git-history-summary.txt
|   |-- reorganization-proposal.md
```

### Rationale

This new structure provides the following benefits:

*   **Separation of Concerns:** It clearly separates the build logic, data, documentation, configuration, and tooling into their own distinct directories.
*   **Improved Clarity:** The new structure is more intuitive and easier to understand for new developers.
*   **Enhanced Maintainability:** By grouping related files together, it will be easier to maintain and update the repository in the future.
*   **Reduced Root Directory Clutter:** The root directory is significantly cleaner, making it easier to find important files.
