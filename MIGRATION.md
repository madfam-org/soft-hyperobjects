# Migration record — extraction from the platform

This repository was extracted from the Fashion Cabinet platform repository with
full history on **2026-09-04**, executing **P2** of
[RFC 0038 §9 "Topology P2"](https://github.com/madfam-org/internal-devops/blob/main/rfcs/0038-commons-1000x2.md#9-topology-where-the-two-thousand-live-operator-proposal-2026-08-22)
(operator-ratified 2026-08-22). It is a record, not a plan: everything below is
verifiable from the hashes.

## Source

| | |
|---|---|
| Source repository | `madfam-org/fashion-cabinet` (private) |
| Source branch | `main` |
| Source commit | `e56247bee457b2e3adbb9dc5a4f88b33b21676f2` (2026-09-03 00:43:56 +0000) |
| Extracted subtree | `projects/` |
| Tool | `git-filter-repo` |

## The extraction

```bash
git clone --no-hardlinks <fashion-cabinet> src-fc
cp -R src-fc soft-hyperobjects
cd soft-hyperobjects && git remote remove origin
git-filter-repo --force --subdirectory-filter projects
```

`--subdirectory-filter projects` rewrites history so each cartridge that was at
`projects/<slug>/` is now at `<slug>/`, and drops every commit that touched
nothing under `projects/`.

## Verification

### Content is byte-identical

The decisive check. The commons root tree, **before any skeleton file was
added**, equals the platform's `projects/` tree exactly:

| | Tree hash |
|---|---|
| `git rev-parse HEAD^{tree}` (this repo, extraction commit `e2e4cb0`) | `8e53962a8353683c4f0397ec335ba5b61f607125` |
| `git rev-parse HEAD:projects` (fashion-cabinet @ `e56247b`) | `8e53962a8353683c4f0397ec335ba5b61f607125` |

Identical tree hashes mean identical content, identical filenames, identical
modes, all the way down. Nothing was transformed, normalised, or lost.

The skeleton files (this file, `README.md`, `LICENSE`, `NOTICE.md`,
`CONTRIBUTING.md`, `GOVERNANCE.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
`.github/`, `docs/policies/DCO.txt`) were added in a **separate commit on top**,
precisely so the equality above stays checkable forever.

### Counts

| | |
|---|---|
| Cartridge directories | **516** — slug set identical to the platform's `projects/` |
| Complete triples (`main.py` + `project.json` + `docs/README.md`) | 516 / 516 |
| Commits (extraction commit and its ancestry) | **66**, from `f2d6abe` (2026-08-17) to `e2e4cb0` (2026-09-02) |
| Source commits before filtering | 207 — the 141 that touched no cartridge were dropped |
| `.git` size after repack | 6.5 MB (platform `.git`: 19 MB) |

### History was uniform

Every path that ever existed under `projects/`, across all 207 source commits,
was a cartridge file. Audited with
`git log --all --name-only -- projects`:

- **1548 distinct paths** ever added = 516 × exactly 3 (`project.json`,
  `main.py`, `docs/README.md`).
- **Zero** files ever lived directly under `projects/` (no index, no README, no
  `.gitkeep`).
- **Zero** deletions and **zero** renames under `projects/` in the entire
  history — no cartridge was ever removed or re-slugged.

So the subdirectory filter had no ambiguous case to resolve.

### Lanes run

| Check | Command | Result |
|---|---|---|
| Manifest conformance | `fc-spec check garment-manifest */project.json` (hyperobjects-spec @ `cb19e51`) | `files=516 failures=0`, exit 0 |
| Object integrity | `git fsck --no-dangling` | exit 0, no output |
| Platform manifest lane | `scripts/qa/validate_manifests.py`, run against this tree through a throwaway platform clone | see § *Running the platform's lanes* |
| Platform pattern lane | `scripts/qa/verify_patterns.py`, same rig | see § *Running the platform's lanes* |

### Running the platform's lanes against this tree

Every platform validator resolves its input **repo-relative** —
`PROJECTS = ROOT / "projects"` — with no environment-variable override. There is
therefore no way to point one at an external directory. To run them against this
repository without modifying the platform checkout, a throwaway
`git clone --no-hardlinks` of the platform was made and its `projects/`
directory replaced with a symlink to this repository's root. That rig is what
produced the results above; the platform working tree at
`/Users/aldoruizluna/labspace/fashion-cabinet` was never written to.

**This is also the shape of the real fix.** Once the platform mounts this
repository as a submodule at `projects/`, those same repo-relative paths resolve
through the submodule and every lane works unchanged — which is exactly why the
cartridges were placed at the root here rather than under a `projects/` prefix.

### Known artifact of the filter

54 commit messages in the retained history reference commit hashes that no longer
exist, because the commits they name touched only platform files and were
dropped. `git-filter-repo` reported them (`.git/filter-repo/suboptimal-issues`)
and left the text as written rather than rewriting other people's prose. This is
inherent to any subdirectory filter and is not corrected: the platform history
still resolves every one of those hashes.

## What did NOT move, and what moving it would require

This tranche moved **the cartridges only**. Everything below stays in the
platform for now — deliberately, because the platform's status lanes validate it
against this repository at a pin, and moving a validated artifact away from its
validator is the way to get a silently-unverified commons.

| Still in the platform | What it is | What would have to move with it |
|---|---|---|
| `docs/fc100` … `docs/fc500` (5 band indexes) | The demand-ranked backlog; each entry's `project` field is the slot claim | The five `scripts/qa/fc*00_status.py` lanes and their shared `_band_status.py`, which cross-check every claimed slot against a cartridge that must exist — they would need to read cartridges from here, and the coordinator's slot-claim act (GOVERNANCE.md) would move with them. |
| `materials/` (11 fabric cards) | Fabric cards — an enabler class, referenced by garment BOMs | `validate_manifests.py`'s fabric-card half and the `fc-spec check fabric-card` invocation; garment manifests reference cards by slug, so the two must be pinned together or a BOM can dangle. |
| `bodies/` (4 measurement sets) | Body / size measurement sets driving the dressed-form lane | `validate_dressing.py` and `packages/kernel/src/fc/dressing.py`'s expectations; dressing is a *kernel* capability, so a body here would be validated by code that is not here. |
| `docs/interfaces/*` | The pinned solid-commons hardware snapshot, bridge index, consumers back-edge, compat map | `verify_hardware_links.py`, `generate_bridge_index.py --check` and the weekly `snapshot-drift.yml` watcher. RFC 0038 §9 wants this to become a pure commons↔commons contract pinning `solid-hyperobjects` directly, so it should move **to** here — but only once the solid side is extracted and can be pinned. |
| `docs/commons-catalog.json` (~900 KB, generated) | The published catalogue the API serves | `generate_commons_catalog.py --check`. It is *generated from* the cartridges, so it should be produced here and consumed by the platform, not stored here as a checked-in artifact validated elsewhere. Ordering matters: move the generator, not the file. |
| `docs/licenses/CARVE-OUTS.md` + `verify_compliance.py` | The operator-ruled licence exception registry and its enforcement | The registry must sit beside the objects it governs — a row whose slug has no cartridge is a CI failure, and that check currently spans two repos. Empty today, so nothing is at risk yet. |
| `docs/rulings/fc1-commons-license.md`, `docs/policies/provenance-disputes.md` | The FC1 ruling record and the dispute process | Both are referenced from [NOTICE.md](./NOTICE.md) by URL today. They are records rather than lanes, so they can move at any time; the cost of moving them is only fixing inbound links. |

## Platform files that read `projects/`

For the platform-side lane (L4), these are the files that resolve a path under
`projects/` and therefore define the blast radius of the submodule mount. None
was changed by this extraction.

**Resolution seams (the two that matter for the mount):**
`apps/api/catalog.py` (`PROJECTS_DIR = ROOT / "projects"`) and `apps/api/dress.py`
(`PROJECTS_DIR = REPO / "projects"`). If the submodule lands at `projects/`, both
resolve unchanged.

**QA lanes (18):** `scripts/qa/validate_manifests.py`, `verify_patterns.py`,
`verify_interfaces.py`, `verify_compliance.py`, `verify_hardware_links.py`,
`verify_export_formats.py`, `generate_bridge_index.py`,
`generate_commons_catalog.py`, `provenance_attestation.py`, `validate_dressing.py`,
`ceq_coverage.py`, `check_snapshot_drift.py`, `dogfood_fc_spec.py`,
`_band_status.py`, `fc100_status.py`, `fc200_status.py`, `fc300_status.py`,
`fc400_status.py`, `fc500_status.py`.

**Dev scripts (3):** `scripts/dev/render_flats.py`, `scripts/dev/ceq_backfill.py`,
`scripts/dev/fc600_gaps.py`.

**Kernel and spec (4):** `packages/kernel/src/fc/dressing.py`,
`packages/kernel/tests/test_flats.py`, `packages/kernel/tests/test_trims.py`,
`packages/spec/tests/test_conformance.py`.

**API tests (7):** `apps/api/tests/` — `test_api.py`, `test_ceq_backfill.py`,
`test_commons_catalog.py`, `test_compliance.py`, `test_dxf_aama_e2e.py`,
`test_export_formats.py`, `test_flats_gallery.py`.

**Non-Python references:** `apps/api/Dockerfile`, `.github/workflows/deploy.yml`
(the deploy path filter, cross-checked by `verify_deploy_paths.py`), and the three
`.github/ISSUE_TEMPLATE/*.yml` templates that name `projects/<slug>/` in prose.

Every one of these is repo-relative, so a submodule mounted at `projects/`
satisfies all of them without a path change. The two things a submodule *does*
change and that L4 must handle: `actions/checkout` needs `submodules: true` (or
`recursive`) in every workflow that runs a lane, and the API's Docker build
context must include the submodule's contents.

## Operator items created by this extraction

1. **`FC_PLATFORM_READ_TOKEN`** — the render + seam-parity lane in
   [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) needs the `fc` kernel
   from the private platform repo. The job is written and skips with a visible
   job-summary notice while the secret is unset, so a green run never implies the
   patterns were verified. Mint a read-only token, or publish the kernel.
2. **Repository visibility.** RFC 0038 §9 recommends the commons goes fully
   public. This extraction does not presume it.
3. **`FC_CONTRIBUTION_SIGNOFF`** — the DCO lane ships inert, exactly as in the
   platform, pending the CLA-vs-DCO ruling (ADR-012 / GOVERNANCE.md item 1).
4. **Role addresses** — the `conduct@` and `security@` placeholders came across
   unresolved, as they are in the platform.

## What this extraction did not do

No push, no remote, no repository creation, no archive, no pull request. The
`origin` remote was removed before filtering. The platform repository was read
and cloned from, never written to.
