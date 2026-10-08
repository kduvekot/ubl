# oasis-tcs/ubl — GitHub API snapshot, 2026-10-08

## How and when this data was gathered

- **When:** 2026-10-08, from about 12:23 to 12:35 UTC. The access check ran at 12:22:59 UTC.
- **How:** only read-only GET requests to the GitHub REST API, made with `gh api` against `repos/oasis-tcs/ubl/...`. The other reads were run logs (`gh run view --log`), two run artifacts (`gh run download`), and the two published packages from docs.oasis-open.org. Nothing was written to oasis-tcs/ubl.
- **Pagination:** `gh api --paginate` could not be used. GitHub's `Link: rel="next"` headers point to `https://api.github.com/repositories/<id>/...`, and the session's network proxy refuses numeric-ID repository paths with HTTP 403. Each page was therefore fetched with `gh api -i`. The next link was rewritten from `repositories/<id>/` to `repos/oasis-tcs/ubl/`, and the pages were joined with `jq`.
  - Activity API: 5 pages, 439 events, all event IDs unique.
  - Workflow runs: 2 pages, 138 runs (the API reports `total_count` 138).
  - Artifacts: 1 page, 13 artifacts (the API reports `total_count` 13).
- **Blob hashes:** the hash lists come from `git hash-object` on every file in each extracted package. Paths are relative to the package's top folder.

## Files

| File | Bytes | Contents |
|---|---:|---|
| `activity.json` | 610676 | `GET repos/oasis-tcs/ubl/activity?per_page=100`, all pages joined into one array (439 events, 2023-04-21T14:31:12Z to 2026-10-08T12:10:46Z) |
| `runs.json` | 1881913 | `GET repos/oasis-tcs/ubl/actions/runs?per_page=100`, all `workflow_runs` joined into one array (138 runs) |
| `artifacts.json` | 10577 | `GET repos/oasis-tcs/ubl/actions/artifacts?per_page=100`, the `artifacts` array (13 artifacts) |
| `branches.json` | 7439 | `GET repos/oasis-tcs/ubl/branches`, all branches (30) with their head commits |
| `repo.json` | 100 | `{default_branch, created_at, pushed_at}` from `GET repos/oasis-tcs/ubl` |
| `jobs-24357437746.json` | 2564 | Jobs of run 24357437746 (2026-04-13, push, ubl-2.5-cs01) |
| `jobs-24360121095.json` | 2564 | Jobs of run 24360121095 (2026-04-13, workflow_dispatch, ubl-2.5-cs01) |
| `jobs-31891163801.json` | 4963 | Jobs and steps of run 31891163801 (2026-08-15, workflow_dispatch, ubl-2.5-os) |
| `jobs-31892096050.json` | 4963 | Jobs and steps of run 31892096050 (2026-08-15, push, ubl-2.5-os) |
| `runart-24357437746.json` | 32 | Artifacts of run 24357437746 (none) |
| `runart-24360121095.json` | 32 | Artifacts of run 24360121095 (none) |
| `runart-31891163801.json` | 718 | Artifacts of run 31891163801 (1) |
| `runart-31892096050.json` | 719 | Artifacts of run 31892096050 (1) |
| `log-31891163801.txt` | 280294 | Full log of run 31891163801 (`gh run view --log`) |
| `log-31892096050.txt` | 406011 | Full log of run 31892096050 (`gh run view --log`) |
| `h-1453.tsv` | 52119 | `<blob hash>\t<path>` for `UBL-2.5-os-20260815-1453z.7z` from artifact 9248641763 (599 files) |
| `h-1513.tsv` | 113966 | `<blob hash>\t<path>` for `UBL-2.5-os-20260815-1513z.7z` from artifact 9249368308 (1304 files) |
| `h-cs01.tsv` | 113966 | `<blob hash>\t<path>` for https://docs.oasis-open.org/ubl/cs01-UBL-2.5/UBL-2.5.zip (1304 files) |
| `h-os.tsv` | 113966 | `<blob hash>\t<path>` for https://docs.oasis-open.org/ubl/os-UBL-2.5/UBL-2.5.zip (1304 files) |

No file is larger than 10 MB, so none was left out. The run artifacts, the published zips and the extracted trees are not included.

The run logs for 24357437746 and 24360121095 could not be retrieved. Both the run-log and the job-log endpoints returned `HTTP 410: Server Error`. The two GitHub Actions logs above contain only masked secrets (`***`).

---

## 5. Context

```
{"created_at":"2018-04-11T20:56:17Z","default_branch":"ubl-2.6","pushed_at":"2026-10-08T12:10:46Z"}
```

Branches (30):

```
UBL-433-xsd-doc 4c0ffc314368f519529cf253a5bd662ecf2da7d0
kentest 7f8f0465682cde4dbbd2bc645cefa8e6df9d47cf
main c12b81a5d412fdb56a11d7e638be61b08c60c3ab
retest 15c714c5caafa34b4b25fcdaf3c340fbd862ef0b
review 876778c2b322f23bc4a8841573424e252303cd56
server-test 68aabb910b3a2e5fb59afa4d8911d709b4bf8027
tsc-ubl-2.5-experimental 0b381cc002a893903eb62bb27150ef08192051ac
ubl-2.3-cs02 47eb1f5627116f966b215c09fa9109d134cd9311
ubl-2.3-csd05-copy 57dda2e5c24ea9693ed5a2365dce350e422f9d35
ubl-2.3-os bc995206894f069cebc7272ed9a2de1d2b0ab91c
ubl-2.3-os-iso bc995206894f069cebc7272ed9a2de1d2b0ab91c
ubl-2.4-cs01-work 7c0188743662b51d34186ab806b68ba4a901961a
ubl-2.4-cs01 8c4d077183bb199891fc01a48c5ea6384037a543
ubl-2.4-csd01wd01 21efa9ebf3286ee715682c9fedc4d771daef5a92
ubl-2.4-csd01wd02 33d45279a29822868347e1c0397e5c0da97753b1
ubl-2.4-csd01 0b0b0b336372c5477e022fd665f2aec641e5a0bc
ubl-2.4-csd02-prd01-13 476e1addf09f308b761dd6371e4609f36e228a3e
ubl-2.4-csd02-tsc 476e1addf09f308b761dd6371e4609f36e228a3e
ubl-2.4-csd02 9b42a40a11815a471ba5ce18913f6855c576810a
ubl-2.4-os 779bf4b42548123781b10b284a3ee662866038b4
ubl-2.4-os-iso-pub c55958d4b0e04d5ca42911f0eb789601f1b7dc23
ubl-2.5-2025-layout 5e984b8c5e716ae96fc879eb886a36dd2592a5a3
ubl-2.5-cs01 ca125dfd71f6484cd8ec7d3c91bc0d9092310c49
ubl-2.5-dev 39fae0da26cc068040dadaee406d18e582252b36
ubl-2.5-iso 8630a5f96c82453ee56865fe7ae814df63a45b2e
ubl-2.5-kenneth 154a8bcdffe5990b28edbae919f5a30426936ea4
ubl-2.5-os 345386aa0504488aebdbec1c7d629ce9b7d08826
ubl-2.5-retry f738ca337ff2a1cff48afbd9bca0007bb430038d
ubl-2.5 3d81e8acf790522057776b7d8503084d7b2bca3a
ubl-2.6 29ae6b44af4d62e4d9d0ef26541c47d6c45df6cb
```

## 1. Activity API

The file holds 439 events: 367 push, 36 branch_creation, 16 branch_deletion and 20 pr_merge. The oldest is 2023-04-21T14:31:12Z and the newest 2026-10-08T12:10:46Z.

Every event with timestamp ≥ 2026-03-31 (timestamp | activity_type | ref | before | after | actor):

```
2026-04-13T16:59:57Z | branch_creation | refs/heads/ubl-2.5-cs01 | 0000000 | 3d81e8a | bdxhub
2026-04-13T17:03:21Z | push | refs/heads/ubl-2.5-cs01 | 3d81e8a | 9992180 | bdxhub
2026-04-13T17:03:45Z | push | refs/heads/ubl-2.5-cs01 | 9992180 | 79997e6 | bdxhub
2026-04-13T17:13:57Z | push | refs/heads/ubl-2.5-cs01 | 79997e6 | 63fa602 | bdxhub
2026-04-13T17:14:19Z | push | refs/heads/ubl-2.5-cs01 | 63fa602 | b926367 | bdxhub
2026-04-13T17:14:42Z | push | refs/heads/ubl-2.5-cs01 | b926367 | 4aece0b | bdxhub
2026-04-13T17:14:58Z | push | refs/heads/ubl-2.5-cs01 | 4aece0b | 3aba646 | bdxhub
2026-04-13T17:15:15Z | push | refs/heads/ubl-2.5-cs01 | 3aba646 | 36bf605 | bdxhub
2026-04-13T17:19:38Z | push | refs/heads/ubl-2.5-cs01 | 36bf605 | 5738516 | bdxhub
2026-04-13T17:21:52Z | push | refs/heads/ubl-2.5-cs01 | 5738516 | 198b65a | bdxhub
2026-04-13T17:22:30Z | push | refs/heads/ubl-2.5-cs01 | 198b65a | 6c7fc34 | bdxhub
2026-04-13T17:22:57Z | push | refs/heads/ubl-2.5-cs01 | 6c7fc34 | 7c77dc5 | bdxhub
2026-04-13T17:23:25Z | push | refs/heads/ubl-2.5-cs01 | 7c77dc5 | 434a2f5 | bdxhub
2026-04-13T17:23:50Z | push | refs/heads/ubl-2.5-cs01 | 434a2f5 | b6fcdf0 | bdxhub
2026-04-13T17:24:27Z | push | refs/heads/ubl-2.5-cs01 | b6fcdf0 | c8137ae | bdxhub
2026-04-13T17:24:56Z | push | refs/heads/ubl-2.5-cs01 | c8137ae | 2097d08 | bdxhub
2026-04-13T17:25:28Z | push | refs/heads/ubl-2.5-cs01 | 2097d08 | 9ade5df | bdxhub
2026-04-13T17:26:07Z | push | refs/heads/ubl-2.5-cs01 | 9ade5df | 8f108d8 | bdxhub
2026-04-13T17:31:45Z | push | refs/heads/ubl-2.5-cs01 | 8f108d8 | ca125df | bdxhub
2026-08-15T14:31:38Z | branch_creation | refs/heads/ubl-2.5-os | 0000000 | ca125df | bdxhub
2026-08-15T14:36:05Z | push | refs/heads/ubl-2.5-os | ca125df | d0d1d91 | bdxhub
2026-08-15T14:38:19Z | push | refs/heads/ubl-2.5-os | d0d1d91 | 7959d83 | bdxhub
2026-08-15T14:38:34Z | push | refs/heads/ubl-2.5-os | 7959d83 | 720c712 | bdxhub
2026-08-15T14:38:48Z | push | refs/heads/ubl-2.5-os | 720c712 | ffbee98 | bdxhub
2026-08-15T14:40:57Z | push | refs/heads/ubl-2.5-os | ffbee98 | c4077e6 | bdxhub
2026-08-15T14:41:22Z | push | refs/heads/ubl-2.5-os | c4077e6 | 4d87c39 | bdxhub
2026-08-15T14:42:07Z | push | refs/heads/ubl-2.5-os | 4d87c39 | 23380c3 | bdxhub
2026-08-15T14:42:46Z | push | refs/heads/ubl-2.5-os | 23380c3 | 8983f1f | bdxhub
2026-08-15T14:45:38Z | push | refs/heads/ubl-2.5-os | 8983f1f | aa012d2 | bdxhub
2026-08-15T14:48:17Z | push | refs/heads/ubl-2.5-os | aa012d2 | 8902b7d | bdxhub
2026-08-15T14:48:24Z | push | refs/heads/ubl-2.5-os | 8902b7d | 84f3c40 | bdxhub
2026-08-15T14:48:56Z | push | refs/heads/ubl-2.5-os | 84f3c40 | 1d96071 | bdxhub
2026-08-15T14:49:04Z | push | refs/heads/ubl-2.5-os | 1d96071 | 40c6c73 | bdxhub
2026-08-15T14:49:11Z | push | refs/heads/ubl-2.5-os | 40c6c73 | 30ece8c | bdxhub
2026-08-15T14:49:18Z | push | refs/heads/ubl-2.5-os | 30ece8c | 7b1cb89 | bdxhub
2026-08-15T14:49:25Z | push | refs/heads/ubl-2.5-os | 7b1cb89 | 569684e | bdxhub
2026-08-15T14:49:33Z | push | refs/heads/ubl-2.5-os | 569684e | d2a042f | bdxhub
2026-08-15T15:13:07Z | push | refs/heads/ubl-2.5-os | d2a042f | 345386a | bdxhub
2026-09-02T08:55:37Z | branch_creation | refs/heads/ubl-2.5-iso | 0000000 | 345386a | bdxhub
2026-09-03T14:32:53Z | push | refs/heads/ubl-2.5-iso | 345386a | 8630a5f | bdxhub
2026-09-14T13:07:58Z | branch_creation | refs/heads/ubl-2.6 | 0000000 | 345386a | kduvekot
2026-09-14T22:19:24Z | pr_merge | refs/heads/ubl-2.6 | 345386a | 4a7fa8b | kduvekot
2026-09-15T15:57:26Z | pr_merge | refs/heads/ubl-2.6 | 4a7fa8b | d3e98ac | kduvekot
2026-10-07T14:07:47Z | pr_merge | refs/heads/ubl-2.6 | d3e98ac | 07fa265 | kduvekot
2026-10-08T08:04:03Z | pr_merge | refs/heads/ubl-2.6 | 07fa265 | 9b908b8 | kduvekot
2026-10-08T08:07:33Z | pr_merge | refs/heads/ubl-2.6 | 9b908b8 | f8e5a96 | kduvekot
2026-10-08T09:13:10Z | pr_merge | refs/heads/ubl-2.6 | f8e5a96 | eabb7ce | kduvekot
2026-10-08T10:36:00Z | pr_merge | refs/heads/ubl-2.6 | eabb7ce | 69c4e22 | kduvekot
2026-10-08T10:39:06Z | branch_deletion | refs/heads/ubl-2.5-python | 6c4d314 | 0000000 | kduvekot
2026-10-08T11:35:45Z | pr_merge | refs/heads/ubl-2.6 | 69c4e22 | bb79377 | kduvekot
2026-10-08T12:10:46Z | pr_merge | refs/heads/ubl-2.6 | bb79377 | 29ae6b4 | kduvekot
```

branch_creation and branch_deletion events in the whole file for branches that no longer exist:

```
2023-09-26T08:47:58Z | branch_deletion | refs/heads/ubl-2.4-csd01-docx | kduvekot
2023-09-26T08:50:42Z | branch_creation | refs/heads/ubl-2.4-csd01-docx | kduvekot
2023-09-26T08:50:46Z | branch_creation | refs/heads/revert-24-ubl-2.4-csd01-docx | kduvekot
2023-09-26T08:53:09Z | branch_creation | refs/heads/csd01-temp | kduvekot
2023-09-26T09:03:57Z | branch_creation | refs/heads/test-2.4cs01 | kduvekot
2023-09-26T10:41:36Z | branch_deletion | refs/heads/test-2.4cs01 | kduvekot
2024-03-06T14:43:26Z | branch_creation | refs/heads/ubl-2.5-csd01 | klakegg
2024-04-10T18:57:34Z | branch_deletion | refs/heads/revert-24-ubl-2.4-csd01-docx | kduvekot
2024-04-10T19:00:02Z | branch_deletion | refs/heads/ubl-2.4-csd01-docx | kduvekot
2024-04-10T19:03:35Z | branch_deletion | refs/heads/csd01-temp | kduvekot
2024-05-30T11:39:34Z | branch_creation | refs/heads/kendebug | gkholman
2024-05-30T12:46:02Z | branch_creation | refs/heads/kendebug2 | gkholman
2024-05-30T14:44:11Z | branch_deletion | refs/heads/kendebug2 | gkholman
2024-05-30T14:44:44Z | branch_deletion | refs/heads/kendebug | gkholman
2024-06-19T12:35:53Z | branch_creation | refs/heads/kd-realta-24 | kduvekot
2024-06-19T12:38:50Z | branch_deletion | refs/heads/kd-realta-24 | kduvekot
2025-03-23T20:07:13Z | branch_creation | refs/heads/ken-test | gkholman
2025-04-07T09:22:53Z | branch_deletion | refs/heads/ken-test | gkholman
2025-04-09T07:40:56Z | branch_deletion | refs/heads/ubl-2.5-csd01 | gkholman
2025-08-16T18:38:31Z | branch_creation | refs/heads/ubl-2.5-7zip-test | gkholman
2025-08-21T00:23:45Z | branch_deletion | refs/heads/ubl-2.5-7zip-test | gkholman
2025-10-07T09:37:49Z | branch_creation | refs/heads/ubl-2.5-python | kduvekot
2026-01-15T18:50:09Z | branch_creation | refs/heads/temp-test | gkholman
2026-01-15T20:07:18Z | branch_deletion | refs/heads/temp-test | gkholman
2026-10-08T10:39:06Z | branch_deletion | refs/heads/ubl-2.5-python | kduvekot
```

## 2. Workflow runs

There are 138 runs, the oldest created 2025-08-21T12:22:22Z and the newest 2026-10-08T12:10:48Z. Every run is the workflow "Build" (`.github/workflows/build.yml`).

105 runs were created before 2026-02-01, between 2025-08-21T12:22:22Z and 2026-01-28T16:25:49Z. Per head_branch:

| head_branch | runs |
|---|---:|
| ubl-2.5 | 63 |
| ubl-2.5-python | 26 |
| ubl-2.5-2025-layout | 7 |
| kentest | 5 |
| UBL-2.4-ISO | 1 |
| main | 1 |
| server-test | 1 |
| ubl-2.5-retry | 1 |

Runs created ≥ 2026-02-01 (id | created_at | run_started_at | updated_at | event | head_branch | head_sha | name | status | conclusion | actor | triggering_actor):

```
21829212212 | 2026-02-09T14:34:23Z | 2026-02-09T14:34:23Z | 2026-02-09T15:09:33Z | push | ubl-2.5 | ec5591c | Build | completed | cancelled | bdxhub | bdxhub
21829231799 | 2026-02-09T14:34:57Z | 2026-02-09T14:34:57Z | 2026-02-09T15:09:41Z | push | ubl-2.5 | 17945be | Build | completed | cancelled | bdxhub | bdxhub
21829256706 | 2026-02-09T14:35:41Z | 2026-02-09T14:35:41Z | 2026-02-09T15:13:45Z | push | ubl-2.5 | d7a6368 | Build | completed | cancelled | bdxhub | bdxhub
21829271807 | 2026-02-09T14:36:08Z | 2026-02-09T14:36:08Z | 2026-02-09T15:13:51Z | push | ubl-2.5 | 221d115 | Build | completed | cancelled | bdxhub | bdxhub
21829283788 | 2026-02-09T14:36:30Z | 2026-02-09T14:36:30Z | 2026-02-09T15:13:59Z | push | ubl-2.5 | 64216b2 | Build | completed | cancelled | bdxhub | bdxhub
21829293705 | 2026-02-09T14:36:47Z | 2026-02-09T14:36:47Z | 2026-02-09T15:14:09Z | push | ubl-2.5 | 757fb6d | Build | completed | cancelled | bdxhub | bdxhub
21829308137 | 2026-02-09T14:37:13Z | 2026-02-09T14:37:13Z | 2026-02-09T15:14:16Z | push | ubl-2.5 | a397e38 | Build | completed | cancelled | bdxhub | bdxhub
21829331279 | 2026-02-09T14:37:54Z | 2026-02-09T14:37:54Z | 2026-02-09T15:14:23Z | push | ubl-2.5 | ba7d5d7 | Build | completed | cancelled | bdxhub | bdxhub
21829458554 | 2026-02-09T14:41:28Z | 2026-02-09T14:41:28Z | 2026-02-09T15:14:27Z | push | ubl-2.5 | 8927dd6 | Build | completed | cancelled | bdxhub | bdxhub
21829483093 | 2026-02-09T14:42:10Z | 2026-02-09T14:42:10Z | 2026-02-09T14:47:03Z | push | ubl-2.5 | 7f2b4ea | Build | completed | success | bdxhub | bdxhub
21829547692 | 2026-02-09T14:43:57Z | 2026-02-09T14:43:57Z | 2026-02-09T14:48:45Z | push | ubl-2.5 | 22f30d9 | Build | completed | success | bdxhub | bdxhub
21829586800 | 2026-02-09T14:45:03Z | 2026-02-09T14:45:03Z | 2026-02-09T14:50:08Z | push | ubl-2.5 | 28960f7 | Build | completed | success | bdxhub | bdxhub
21829607494 | 2026-02-09T14:45:36Z | 2026-02-09T14:45:36Z | 2026-02-09T14:50:35Z | push | ubl-2.5 | 9a4ee63 | Build | completed | success | bdxhub | bdxhub
21829622091 | 2026-02-09T14:46:00Z | 2026-02-09T14:46:00Z | 2026-02-09T14:50:50Z | push | ubl-2.5 | 18d4448 | Build | completed | success | bdxhub | bdxhub
21829639791 | 2026-02-09T14:46:30Z | 2026-02-09T14:46:30Z | 2026-02-09T14:51:59Z | push | ubl-2.5 | 6fbccae | Build | completed | success | bdxhub | bdxhub
21830451028 | 2026-02-09T15:08:48Z | 2026-02-09T15:08:48Z | 2026-02-09T15:14:35Z | push | ubl-2.5 | a66c455 | Build | completed | cancelled | bdxhub | bdxhub
21830603834 | 2026-02-09T15:13:06Z | 2026-02-09T15:13:06Z | 2026-02-09T15:58:00Z | push | ubl-2.5 | 3d81e8a | Build | completed | success | bdxhub | bdxhub
24357437746 | 2026-04-13T17:31:51Z | 2026-04-13T17:31:51Z | 2026-04-13T19:03:21Z | push | ubl-2.5-cs01 | ca125df | Build | completed | success | bdxhub | bdxhub
24360121095 | 2026-04-13T18:31:54Z | 2026-04-13T18:31:54Z | 2026-04-13T19:17:02Z | workflow_dispatch | ubl-2.5-cs01 | ca125df | Build | completed | success | bdxhub | bdxhub
31891163801 | 2026-08-15T14:53:23Z | 2026-08-15T14:53:23Z | 2026-08-15T14:59:28Z | workflow_dispatch | ubl-2.5-os | d2a042f | Build | completed | success | bdxhub | bdxhub
31892096050 | 2026-08-15T15:13:09Z | 2026-08-15T15:13:09Z | 2026-08-15T16:00:50Z | push | ubl-2.5-os | 345386a | Build | completed | success | bdxhub | bdxhub
33611333059 | 2026-09-02T08:55:40Z | 2026-09-02T08:55:40Z | 2026-09-02T09:42:25Z | push | ubl-2.5-iso | 345386a | Build | completed | success | bdxhub | bdxhub
33767494654 | 2026-09-03T14:32:56Z | 2026-09-03T14:32:56Z | 2026-09-03T15:21:20Z | push | ubl-2.5-iso | 8630a5f | Build | completed | success | bdxhub | bdxhub
34847338944 | 2026-09-14T13:08:01Z | 2026-09-14T13:08:01Z | 2026-09-14T13:56:24Z | push | ubl-2.6 | 345386a | Build | completed | success | kduvekot | kduvekot
34903525387 | 2026-09-14T22:19:28Z | 2026-09-14T22:19:28Z | 2026-09-14T23:07:39Z | push | ubl-2.6 | 4a7fa8b | Build | completed | success | kduvekot | kduvekot
34991886882 | 2026-09-15T15:57:29Z | 2026-09-15T15:57:29Z | 2026-09-15T16:42:43Z | push | ubl-2.6 | d3e98ac | Build | completed | success | kduvekot | kduvekot
37634127894 | 2026-10-07T14:07:50Z | 2026-10-07T14:07:50Z | 2026-10-07T15:00:33Z | push | ubl-2.6 | 07fa265 | Build | completed | success | kduvekot | kduvekot
37747392902 | 2026-10-08T08:04:06Z | 2026-10-08T08:04:06Z | 2026-10-08T08:30:35Z | push | ubl-2.6 | 9b908b8 | Build | completed | success | kduvekot | kduvekot
37747777281 | 2026-10-08T08:07:36Z | 2026-10-08T08:07:36Z | 2026-10-08T08:32:35Z | push | ubl-2.6 | f8e5a96 | Build | completed | success | kduvekot | kduvekot
37755127297 | 2026-10-08T09:13:13Z | 2026-10-08T09:13:13Z | 2026-10-08T09:36:13Z | push | ubl-2.6 | eabb7ce | Build | completed | success | kduvekot | kduvekot
37764536717 | 2026-10-08T10:36:03Z | 2026-10-08T10:36:03Z | 2026-10-08T11:02:47Z | push | ubl-2.6 | 69c4e22 | Build | completed | success | kduvekot | kduvekot
37771098174 | 2026-10-08T11:35:48Z | 2026-10-08T11:35:48Z | 2026-10-08T11:51:01Z | push | ubl-2.6 | bb79377 | Build | completed | success | kduvekot | kduvekot
37775050430 | 2026-10-08T12:10:48Z | 2026-10-08T12:10:48Z | 2026-10-08T12:10:57Z | push | ubl-2.6 | 29ae6b4 | Build | in_progress | null | kduvekot | kduvekot
```

Run display titles: 24357437746 = "CSD03 entities", 24360121095 = "Build", 31891163801 = "Build", 31892096050 = "CS01 endorsed entities".

## 3. Artifacts

The API lists 13 artifacts in total. All were created on or after 2026-02-01 and none has expired. No artifacts remain for runs before 2026-08-15.

```
9248641763 | UBL-package-github-20260815-1453z | 47281259 | 2026-08-15T14:59:25Z | 2026-11-13T14:53:24Z | false | 31891163801 | ubl-2.5-os | d2a042f
9249368308 | UBL-package-github-20260815-1513z | 157611862 | 2026-08-15T16:00:46Z | 2026-11-13T15:13:09Z | false | 31892096050 | ubl-2.5-os | 345386a
9840757959 | UBL-package-github-20260902-0855z | 157617947 | 2026-09-02T09:42:22Z | 2026-12-01T08:55:41Z | false | 33611333059 | ubl-2.5-iso | 345386a
9900047567 | UBL-package-github-20260903-1433z | 157619758 | 2026-09-03T15:21:15Z | 2026-12-02T14:32:56Z | false | 33767494654 | ubl-2.5-iso | 8630a5f
10350829170 | UBL-package-github-20260914-1308z | 157609441 | 2026-09-14T13:56:18Z | 2026-12-13T13:08:01Z | false | 34847338944 | ubl-2.6 | 345386a
10372214644 | UBL-package-github-20260914-2219z | 156903166 | 2026-09-14T23:07:37Z | 2026-12-13T22:19:28Z | false | 34903525387 | ubl-2.6 | 4a7fa8b
10408002101 | UBL-package-github-20260915-1557z | 156948845 | 2026-09-15T16:42:39Z | 2026-12-14T15:57:29Z | false | 34991886882 | ubl-2.6 | d3e98ac
11492761466 | UBL-package-github-20261007-1407z | 67479626 | 2026-10-07T15:00:28Z | 2027-01-05T14:07:50Z | false | 37634127894 | ubl-2.6 | 07fa265
11537084838 | UBL-package-github-20261008-0804z | 68594794 | 2026-10-08T08:30:31Z | 2027-01-06T08:04:06Z | false | 37747392902 | ubl-2.6 | 9b908b8
11537801221 | UBL-package-github-20261008-0807z | 61604320 | 2026-10-08T08:32:32Z | 2027-01-06T08:07:36Z | false | 37747777281 | ubl-2.6 | f8e5a96
11540941900 | UBL-package-github-20261008-0913z | 61600863 | 2026-10-08T09:36:08Z | 2027-01-06T09:13:13Z | false | 37755127297 | ubl-2.6 | eabb7ce
11545691282 | UBL-package-github-20261008-1036z | 61601248 | 2026-10-08T11:02:42Z | 2027-01-06T10:36:04Z | false | 37764536717 | ubl-2.6 | 69c4e22
11547414135 | UBL-package-github-20261008-1135z | 61609352 | 2026-10-08T11:50:57Z | 2027-01-06T11:35:49Z | false | 37771098174 | ubl-2.6 | bb79377
```

(columns: id | name | size_in_bytes | created_at | expires_at | expired | workflow_run.id | workflow_run.head_branch | workflow_run.head_sha)

## 4. Release-build evidence

### 4a. Jobs

2026-04-13. In both runs the jobs have 0 recorded steps, and the run's artifact list is empty (`total_count=0`).

```
24357437746  staging  71128000424 17:31:55Z→17:31:58Z success
             build    71128022800 17:32:02Z→19:03:20Z success
             build-py 71128023140 skipped
24360121095  staging  71137302191 18:32:00Z→18:32:11Z success
             build    71137342785 18:32:15Z→19:17:01Z success
             build-py 71137343013 skipped
```

2026-08-15:

```
31891163801  staging  95027527105 14:53:26Z→14:53:28Z success
             build    95027535488 14:53:32Z→14:59:27Z success   (Build step 14:54:42→14:59:22)
             build-py skipped
31892096050  staging  95029783296 15:13:11Z→15:13:15Z success
             build    95029794712 15:13:17Z→16:00:48Z success   (Build step 15:14:01→16:00:41)
             build-py skipped
```

### 4b. Logs

The logs for the two 2026-04-13 runs are gone: both the run-log and the job-log endpoints return `HTTP 410: Server Error`.

31891163801: the log exists (2376 lines). Below is every line matching the requested terms, leaving out routine "Parse succeeded" and empty "Error check:" lines.

```
14:54:42 [echo] UBLstage=os
14:54:42 [echo] UBLprevStageVersion=2.5
14:54:42 [echo] UBLprevStage=cs01
14:56:14 [echo] Checking ".../UBL-Entities-2.5.gc" GC file against NDR and old ".../UBL-Entities-2.5-cs01.gc" ...
14:56:33 [echo] Checking ".../UBL-Endorsed-Entities-2.5.gc" GC file against NDR and old ".../UBL-Endorsed-Entities-2.5-cs01.gc" ...
14:56:37 [java] Error at char 208 in xsl:param/@select on line 48 column 23 of Crane-checkgc4obdndr.xsl:
14:56:37 [java]   file:/home/runner/work/ubl/ubl/target/UBL-Endorsed-Entities-2.5-cs01.gc
14:56:37 [java] Unable to open resolved old uri: file:/home/runner/work/ubl/ubl/target/UBL-Endorsed-Entities-2.5-cs01.gc
14:56:37 [echo] Error check: Error at char 208 in xsl:param/@select on line 48 column 23 of Crane-checkgc4obdndr.xsl:
14:56:37 [echo]   file:/home/runner/work/ubl/ubl/target/UBL-Endorsed-Entities-2.5-cs01.gc
14:56:37 [echo] Unable to open resolved old uri: file:/home/runner/work/ubl/ubl/target/UBL-Endorsed-Entities-2.5-cs01.gc
14:58:01 [echo] UBLstage=os
14:58:02 BUILD SUCCESSFUL
14:59:25 Artifact UBL-package-github-20260815-1453z.zip successfully finalized. Artifact ID 9248641763
```

31892096050: the log exists (3570 lines). The filter is the same, and it also leaves out the "No schema/value validation errors" lines and the errors that the deliberately bad test files are expected to produce.

```
15:13:12 (staging) Generated timestamp: 20260815-1513
15:14:01 bash build.sh target github 20260815-1513z "${REALTA_USERNAME:-}" "${REALTA_PASSWORD:-}" DELETE-REPOSITORY-FILES-AS-WELL
15:14:01 [echo] build.xml - UBL-2.5 os 20260815-1513z (github - 2026-08-15 15:14:01)
15:14:01 [echo] UBLstage=os
15:14:01 [echo] UBLprevStageVersion=2.5
15:14:01 [echo] UBLprevStage=cs01
15:14:01 [echo] label=20260815-1513z
15:15:14 [echo] Checking ".../UBL-Entities-2.5.gc" ... against NDR and old ".../UBL-Entities-2.5-cs01.gc"
15:15:31 [echo] Checking ".../UBL-Endorsed-Entities-2.5.gc" ... against NDR and old ".../UBL-Endorsed-Entities-2.5-cs01.gc"   (no error this time)
15:17:04 [exec] The following error report is simply the exit mechanism and can be ignored:
15:50:55 [copy] Copying 775 files to .../target/artefacts-UBL-2.5-os-20260815-1513z
15:50:57 [echo] UBLstage=os
15:50:57 [echo] UBLprevStage=cs01
15:51:04 [echo] No DTD validation errors. / No writing rule validation errors.
15:51:04 [zip] Building zip: /home/runner/work/ubl/ubl/target/UBL-2.5-pub.zip
15:51:05 [echo] Submitting "UBL-2.5-pub.zip" with "UBL 2.5 2026-08-15 15:51:05+0000" to "OASIS-2025-specnote2pdfhtml-ISO-pdfdocx" ...
15:55:12 [echo] Fetching log UBL-2.5-pub.zip.realta.txt
15:55:12 [echo] Fetching file UBL-2.5-pub.zip.realta.zip
15:55:21 [echo] Unzipping UBL-2.5-pub.zip.realta.zip PDF/HTML results...
15:55:23 [echo] Realta server access ended without error
15:55:30 BUILD SUCCESSFUL
16:00:46 Artifact UBL-package-github-20260815-1513z.zip successfully finalized. Artifact ID 9249368308
```

No line in either log contains "Generated on", "releaseDate", "csd03" or "BUILD FAILED".

### 4c. Artifacts compared with the published packages

The artifacts contain `.7z` files, not zips. The main package `UBL-2.5-os-<label>.7z` was compared in each case.

Contents of the two artifacts:

- 31891163801:
  - `UBL-2.5-os-20260815-1453z.7z`: 599 files
  - `…-archive-only.7z`: 6227 files
  - `…-iso-iec-19845.7z`: empty
- 31892096050:
  - `UBL-2.5-os-20260815-1513z.7z`: 1304 files
  - `…-archive-only.7z`: 6553 files
  - `…-iso-iec-19845.7z`: `iso-iec-19845-draft.niso.zip`, `.docx` and `.pdf`

The comparisons use git blob hashes, matched by path relative to the package's top folder:

| | Artifact 31892096050 (1513z) vs published OS | Artifact 31891163801 (1453z) vs published OS | Artifact 31892096050 (1513z) vs published CS01 (context) |
|---|---:|---:|---:|
| Files compared | 1304 | 597 | 1304 |
| Identical | 1302 | 178 | 650 |
| Differing | 2 | 419 | 654 |
| Only in artifact | 0 | 2 | 0 |
| Only in published | 0 | 707 | 0 |

1513z vs OS, the two differing files:

- `endorsed/xsdrt/common/BDNDR-CCTS_CCT_SchemaModule-1.1.xsd`: 45268 bytes in the artifact, 7124 bytes published
- `endorsed/xsdrt/common/BDNDR-UnqualifiedDataTypes-1.1.xsd`: 75029 bytes in the artifact, 7673 bytes published

The artifact contains the full versions; the second one has the header "manually-edited copy … UBL-383". The published OS package has short versions with a generated header: "UBL 2.5 OS / Release Date: 12 August 2026 / Generated on: 2026-08-15 15:16z". The published CS01 package has the same full versions as the artifact (45268 and 75029 bytes, with no "Generated on" line).

Count of "Generated on" lines: the published OS package has 208 × 15:15z and 204 × 15:16z, the artifact 208 × 15:15z and 202 × 15:16z. The difference of 2 is exactly these two files.

1453z vs OS: this is an incomplete build.

- Only in the artifact: `MISSING-COMPARISON-GC-FILE.txt` (66 bytes, naming `target/UBL-Endorsed-Entities-2.5-cs01.gc`) and an empty `HUB-SKIPPED-INCOMPLETE-ARTEFACTS.txt`.
- Only in the published package (first entries): `UBL-2.5.html`, `UBL-2.5.pdf`, `UBL-2.5.xml`, `art/*.png`, …
- Differing (first entries): `endorsed/mod/UBL-Endorsed-Entities-2.5.ods` and `.xls`, `endorsed/xsd/common/*.xsd`, `endorsed/xsd/maindoc/*.xsd`, …

The "Generated on" line of `xsd/maindoc/UBL-Invoice-2.5.xsd`:

| Package | Generated on |
|---|---|
| Artifact 1453z | 2026-08-15 14:56z |
| Artifact 1513z | 2026-08-15 15:15z |
| Published OS | 2026-08-15 15:15z |
| Published CS01 | 2026-04-13 18:35z (all 410 "Generated on" lines in the package) |

The CS01 build of 2026-04-13 cannot be checked any more, because neither of that day's runs has logs or artifacts left. By timing alone, run 24360121095 matches the 18:35z stamp: its build job started at 18:32:15Z, and in run 31892096050 the XSDs were generated about two minutes after the build started. Run 24357437746's build job started at 17:32Z, so it would have stamped about 17:35z. This is an inference and has not been verified.
