# soft-hyperobjects

**The soft half of the MADFAM commons: 516 parametric garment, block, notion and
technique cartridges, licensed CERN-OHL-W-2.0.**

Every directory at the root of this repository is one **cartridge** — a
parametric fashion hyperobject that drafts a real, sewable pattern:

```
t-shirt-crew/
  main.py            # the draft — `fc` and `math` pre-injected, assigns `result`
  project.json       # the manifest — parameters, sizes, BOM, provenance, licence
  docs/README.md     # what it is, how it is constructed, what it is for
```

There is no platform code here. Validating a cartridge takes one `pip install`
and one command — see [Verifying a cartridge](#verifying-a-cartridge).

---

## The four-repo topology

This repository is one of four, plus a keystone. The split is
[RFC 0038 §9](https://github.com/madfam-org/internal-devops/blob/main/rfcs/0038-commons-1000x2.md)
("Topology P2"), ratified by the operator on 2026-08-22.

| Repo | What lives there | Licence |
|---|---|---|
| [`fashion-cabinet`](https://github.com/madfam-org/fashion-cabinet) | The **soft platform** — studio, catalog/render API, the `fc` drafting kernel, the MTM seam | AGPL-3.0 |
| [`yantra4d`](https://github.com/madfam-org/yantra4d) | The **solid platform** — studio, API, tiers, render workers | AGPL-3.0 |
| **`soft-hyperobjects`** (here) | The **soft commons** — garments, blocks, notions, techniques | CERN-OHL-W-2.0 |
| [`solid-hyperobjects`](https://github.com/madfam-org/solid-hyperobjects) | The **solid commons** — printed and machined cartridges | CERN-OHL-W-2.0 |
| [`hyperobjects-spec`](https://github.com/madfam-org/hyperobjects-spec) | The **keystone** — schemas, `fc-spec`/`y4d-spec` validators, the commons sandbox | permissive |

**The split is by kernel, not by stiffness.** A hyperobject lives where its
*representation* lives: solid geometry (B-Rep/CSG/SDF, printed) on the solid
side; pattern geometry (2-D drafted, sewn) here. An AM-fashion piece is one
identity in two linked artifacts — its printable solid there, its pattern here,
joined by the bridge and a shared material identity.

**The keystone rule.** The verification bar ships as an installable package, so
this repository's CI never touches platform code:

```bash
pip install "hyperobjects-spec @ git+https://github.com/madfam-org/hyperobjects-spec@db65cf1e7a2732d7263efd6eb6ba533640eb536f"
fc-spec check garment-manifest */project.json
```

### How the platform consumes this repository

Fashion Cabinet mounts this repository as a **single submodule at `projects/`**,
pinned to a commit. Every platform path stays exactly as it was —
`apps/api/catalog.py` and `apps/api/dress.py` both resolve
`PROJECTS_DIR = ROOT / "projects"`, and a cartridge is still
`projects/<slug>/project.json` from inside the platform. Here, without the
platform in front of it, the same cartridge is simply `<slug>/`.

---

## Verifying a cartridge

Manifest conformance needs nothing but the keystone package:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "hyperobjects-spec @ git+https://github.com/madfam-org/hyperobjects-spec@db65cf1e7a2732d7263efd6eb6ba533640eb536f"

fc-spec check garment-manifest my-garment/project.json   # one cartridge
fc-spec check garment-manifest */project.json            # the whole commons
```

`fc-spec` is read-proof: it prints how many files it checked, and checking zero
files is a usage error, never a pass. Exit `0` means every file conformed; `1` a
conformance problem; `2` a usage or read error.

**Pattern verification — rendering the draft and checking seam parity — needs
the `fc` kernel**, which lives in the Fashion Cabinet platform repository. CI
runs it as a separate job that skips cleanly when the platform read token is
absent (see [.github/workflows/ci.yml](.github/workflows/ci.yml)). Locally, if
you have platform access:

```bash
pip install "git+https://github.com/madfam-org/fashion-cabinet@main#subdirectory=packages/kernel"
pip install "git+https://github.com/madfam-org/fashion-cabinet@main#subdirectory=packages/commons-sandbox"
```

---

## The cartridge contract

The full contract is Fashion Cabinet's
[AGENTS.md](https://github.com/madfam-org/fashion-cabinet/blob/main/AGENTS.md);
the published, versioned form is its `docs/spec/v1/`. In short:

- `fc` and `math` are **pre-injected globals** in the sandbox. Nothing else is
  importable — no repo libraries, no file or network I/O.
- Manifest parameters arrive as **bare globals**. Read them through
  `PARAM(lambda: <name>, <default>)` so the script also runs standalone. Never
  `globals()`, `eval`, or `getattr` — the sandbox blocks them.
- Multi-piece dispatch goes through a `target_piece` parameter; assign the final
  `fc.PatternSet` to a top-level **`result`**.
- **Units are millimetres.** Girths are full-body measurements. Drafting
  coordinates are y-up; exporters handle the flips.
- Verification is **fail-closed**: `PatternSet.verify()` error-level issues — an
  open outline, a degenerate piece, a seam-length mismatch, a dangling seam
  reference — abort the render. Declare every sewn relationship with
  `pattern.declare_seam(...)`; an undeclared seam is an unverified seam.
- `hyperobject` metadata is **top-level only**; the schema rejects
  `project.hyperobject`.
- `project.attribution` with `license` + `lineage[]` is **required** on every
  object — provenance from object #1.

---

## Licence

All 516 objects here are **CERN-OHL-W-2.0** — the FC1 operator ruling of
2026-08-25, applied by [ADR-011](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/rulings/fc1-commons-license.md).
The full text is in [LICENSE](./LICENSE); provenance and the carve-out registry
are in [NOTICE.md](./NOTICE.md).

Weakly reciprocal is the operative choice: **you may make and sell physical
products from these patterns with no obligation to open anything you make.** The
reciprocity attaches to the *design* — modify the pattern itself and you publish
the modified pattern under the same terms.

No object ships a per-directory `LICENSE` file. An in-repo object is covered by
the text in [LICENSE](./LICENSE) plus its own declared `commons_license`; the
declaration in the manifest is the normative statement.

Platform code is a different thing under a different licence (AGPL-3.0) and
stays in the platform repositories.

---

## Contributing

[CONTRIBUTING.md](./CONTRIBUTING.md) is the pipeline; [GOVERNANCE.md](./GOVERNANCE.md)
is who decides what, on what evidence. [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)
applies to everyone. Security reports go through [SECURITY.md](./SECURITY.md).

> **The contribution pipeline is scaffolded, not fully ruled.** The sign-off
> mechanism (CLA vs DCO) is an open **operator** ruling, and until it lands a
> third-party PR can be opened, reviewed and iterated but **cannot be merged**.
> Read [CONTRIBUTING.md § Sign-off](./CONTRIBUTING.md#sign-off) before you invest
> a weekend.

[MIGRATION.md](./MIGRATION.md) records how this repository was extracted from
the platform, with the hashes to verify it.
