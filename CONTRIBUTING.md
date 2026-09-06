# Contributing to soft-hyperobjects

This repository is a **commons**: a ranked, verified library of parametric
fashion hyperobjects. This document is how an object gets into it.

The commons licence was ruled on 2026-08-25 — **CERN-OHL-W-2.0** (the FC1
ruling, applied here per [NOTICE.md](./NOTICE.md)) — and that ruling exists
precisely so this door can open. Platform code lives in the
[Fashion Cabinet](https://github.com/madfam-org/fashion-cabinet) repository under
**AGPL-3.0**; the two are different things and this document keeps them apart.

> **This pipeline is scaffolded, not fully ruled.** One decision is still the
> operator's and is marked in place below: **[RULING PENDING: CLA vs DCO]**
> (§ 8 Sign-off). Until it is made, a PR can be opened, reviewed, and iterated,
> but **cannot be merged**. Read § 8 before you invest a weekend.

By participating you agree to the [Code of Conduct](./CODE_OF_CONDUCT.md). Who
decides what, and on what evidence, is [GOVERNANCE.md](./GOVERNANCE.md).

---

## 0. What a contribution is

| Contribution | Where it lands | Ranked? |
|---|---|---|
| A **garment** cartridge | `<slug>/` at the repo root | Yes — into a ratified band slot (§ 5.2 — none is open today) |
| An **enabler** (block, notion, technique) | `<slug>/` at the repo root | No — unranked, with a stated reason |
| A **translation / provenance fix** to an existing object | that object's files | n/a |
| A **fabric card** | `materials/<slug>/` **in the platform repo** — see § 0.1 | No — an enabler |
| Platform code, lanes, studio, API | the platform repo (AGPL-3.0) | n/a |

A commons object is a **cartridge**: `<slug>/` = `main.py` + `project.json` +
`docs/README.md`. The full contract is Fashion Cabinet's
[AGENTS.md](https://github.com/madfam-org/fashion-cabinet/blob/main/AGENTS.md);
the published, versioned form is its `docs/spec/v1/`. **Read both before writing
geometry** — this document covers the pipeline, not the kernel.

Hard goods (buttons, zippers, buckles, boning, rivets) are **not** soft
hyperobjects. They are solid ones: they live in
[`solid-hyperobjects`](https://github.com/madfam-org/solid-hyperobjects) and a
garment consumes one through `notion.hardware_ref` — never by re-implementing it.

### 0.1 What is here and what is still in the platform

This repository currently holds **the cartridges only**. The band indexes
(`docs/fc100` … `docs/fc500`), the fabric cards (`materials/`), the body
measurement sets (`bodies/`), the interface snapshots (`docs/interfaces/`) and
the generated commons catalogue are still in the Fashion Cabinet platform
repository, where the status lanes validate them against this repository at a
pin. [MIGRATION.md](./MIGRATION.md) records that split and what moves next.

Practically: a **cartridge** PR is opened here; a PR that touches a band index,
a fabric card, or a body is opened against the platform repo. If your change
needs both, say so in the issue and a maintainer will sequence the two PRs.

---

## 1. Census before every slug

**Never name a slug before you have looked for it.** Duplicate objects are the
failure mode that kills a ranked commons, and the census is cheap.

```bash
# 1. Every cartridge that exists right now (516 at the time of writing).
ls -d */ | sed 's#/$##' | sort

# 2. Near-misses by name, in four languages (a manifest carries en/es/fr/pt).
grep -ril "<the-thing-you-want-to-build>" */project.json
```

The remaining two places to look are still in the platform repo — every ranked
slot across all five bands (`docs/fc100/index.json` … `docs/fc500/index.json`)
and the fabric cards (`materials/`). Check them there.

Then state the result in your proposal issue: *"census run against the commons
(N cartridges) and all five band indexes; nearest existing objects are X and Y;
this differs because …"*. A PR whose census section is empty is sent back
without further review.

**Where the commons actually stands today (2026-09).** All **500** ranked slots
across FC-100 … FC-500 are claimed *and built*, plus **16** unranked enablers —
516 cartridges. There is at this moment **no unclaimed ranked slot to fill**, and
the next band (ranks 501–600) is not ratified yet. Read § 5.2 before you plan a
garment: it changes what your landing route can be.

**An "unclaimed" ranked entry, when one exists, is a name — not a reservation.**
`"project": null` means the slot is ratified and unbuilt. Say in your issue which
slot you intend to fill; a maintainer confirms nobody else is mid-flight on it.

---

## 2. Propose first, build second

Open a **proposal issue** before you write geometry. It costs you ten minutes
and can save you a weekend on an object we cannot land.

The proposal captures: the slug, the family, the band slot (or "unranked
enabler" plus a reason), demand rationale, the standards/drafting sources you
will work from, the hardware your object consumes, a licence attestation, and —
for anything with cultural provenance — an attribution section (§ 4.5).

Maintainers respond with one of: **go** (with the slot confirmed), **go as an
unranked enabler**, **not yet** (with why), or **already exists** (with the
slug).

---

## 3. The manifest contract

Everything in this section is machine-checked. Nothing here is a matter of taste.
Run `fc-spec check garment-manifest <slug>/project.json` and it will tell you.

### 3.1 `project.attribution` — provenance from object #1

`project.attribution` with `license` + `lineage[]` is **required** on every
object. Provenance is not a nice-to-have added later; it is a schema requirement
from the first object, and it exists so the commons never accumulates a
relabeling debt it cannot pay.

`lineage[]` names what you actually drafted from — a standard, a textbook, a
published block, a measured garment. If you drafted it yourself from first
principles, say that.

### 3.2 `hyperobject.commons_license` — required, and it must agree

Both licence fields must be present, must agree with each other, and must be
`CERN-OHL-W-2.0`:

```json
{
  "project":     { "attribution": { "license": "CERN-OHL-W-2.0", "lineage": [ ... ] } },
  "hyperobject": { "commons_license": "CERN-OHL-W-2.0" }
}
```

`hyperobject` metadata is **top-level only** — the schema rejects
`project.hyperobject`. Do not add a `LICENSE` file inside your cartridge; the
compliance lane treats a stray `LICENSE` or `COPYING` at any depth as an error.

### 3.3 Born quadrilingual — en / es / fr / pt

Objects carry their user-facing strings in four languages. `en` and `es` are
first-class and reviewed; `fr` and `pt` must be **reviewed by a human**, not
generated and pasted. Attest in your PR which of the four you can vouch for and
which you cannot — an honest "I do not speak Portuguese, these need review" is
useful; a silent machine translation is not.

### 3.4 `hardware_ref` — never re-implement a hard good

A button, a zipper, a buckle, a rivet, a piece of boning is a **solid**
hyperobject. Your garment references it through `notion.hardware_ref` and drives
its parameters through `params_map`. You never model it in pattern geometry.

Validate the link:

```bash
fc-spec check hardware-ref <slug>/project.json --resolve solid-commons-catalog.json
```

Without `--resolve`, a linked reference is reported as unresolvable — that is a
missing check, not a pass.

### 3.5 Things that are never in an object

No file or network I/O. No repo-library imports — only `import fc` and stdlib
`math`, both pre-injected. No `globals()`, `eval`, or `getattr` — the sandbox
blocks them and the manifest parameters arrive as bare globals for exactly this
reason. No vendored tree, no shipped licence file, no prices, no hard goods
modelled as pattern pieces.

---

## 4. Verify locally — the same code CI runs

### 4.1 Manifest conformance — no platform checkout needed

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install "hyperobjects-spec @ git+https://github.com/madfam-org/hyperobjects-spec@db65cf1e7a2732d7263efd6eb6ba533640eb536f"

fc-spec check garment-manifest <slug>/project.json
```

`fc-spec` is read-proof: it prints how many files it checked, and checking zero
files is a usage error, never a pass. This is the same runner CI invokes — see
[.github/workflows/ci.yml](./.github/workflows/ci.yml).

Other contracts your object may touch:

```bash
fc-spec list                                          # what is checkable
fc-spec check fabric-card <material>/material.json
fc-spec check body-measurements <body>.json
fc-spec check explode-json <explode>.json
```

### 4.2 Render your cartridge — needs the kernel

Pattern verification (render + seam parity) needs the `fc` drafting kernel and
the sandbox, which live in the **platform** repository. If you have access:

```bash
pip install "git+https://github.com/madfam-org/fashion-cabinet@main#subdirectory=packages/kernel"
pip install "git+https://github.com/madfam-org/fashion-cabinet@main#subdirectory=packages/commons-sandbox"
```

Verification is **fail-closed**: `PatternSet.verify()` error-level issues — an
open outline, a degenerate piece, a seam-length mismatch, a dangling seam
reference — abort the render. Declare every sewn relationship with
`pattern.declare_seam(...)`; an undeclared seam is an unverified seam.

> **Operator item, recorded honestly.** The kernel is not public today, so the
> render job in this repository's CI **skips with a visible notice** when the
> platform read token is absent. A contributor without platform access can get
> manifest conformance green here and cannot self-serve the render lane. See
> [.github/workflows/ci.yml](./.github/workflows/ci.yml) and
> [MIGRATION.md](./MIGRATION.md).

### 4.3 Do not touch these in a contribution PR

The band indexes, the pinned solid-commons snapshot, the generated catalogue and
bridge index, and any generated file marked as such. A maintainer regenerates or
claims those; a contributor who edits them makes the PR unmergeable.

### 4.4 If your object is genuinely not CERN-OHL-W-2.0

Stop and read [NOTICE.md § Carve-outs](./NOTICE.md#carve-outs). A differing
licence needs an **operator-ruled, documented carve-out registered before the
object is built**, and the registry row and the object land in the same PR. A
lone differing manifest is a hard CI failure. No maintainer, contributor, or
agent may issue a carve-out.

### 4.5 Heritage and cultural provenance

An object drawn from a living cultural tradition carries a documentation
obligation the geometry does not discharge. Name the tradition and the community
precisely, cite sources for every cultural claim, and write documentation that
**attributes rather than appropriates**. A reviewer checks this by reading your
sources, not by trusting the section exists.

---

## 5. The pull request

### 5.1 One object per PR

One cartridge per pull request. A wave of six garments is six PRs. This is not
bureaucracy: it is what lets an object be reverted, disputed, or relicensed on
its own, and it is how the ranked index stays auditable.

### 5.2 The ranked-index rule

**An object lands in exactly one of two ways.**

1. **Into a ratified band slot.** Your object fills a band entry whose
   `"project"` is `null`, and the entry's `id`, `family`, and `tier` are what you
   build to.
2. **As an unranked enabler, with a stated reason.** Blocks, notions, techniques
   and fabric cards are the dependency graph *underneath* the ranked objects and
   are deliberately not counted in the bands. Your PR must state which ranked
   object(s) the enabler unblocks, or what capability gap it closes.

There is no third way. "It's a nice garment" is not a landing route — an
unranked garment that fills no slot is count-chasing, and dilution is the
specific failure this rule exists to prevent.

**What that means for you, today.** Every slot in FC-100 … FC-500 is claimed and
built, so route 1 is currently closed:

- **An unranked enabler** (route 2) is landable right now, on a stated reason.
- **An improvement to an existing object** — a better draft, a fixed grade rule,
  missing `fr`/`pt` strings, a corrected or enriched `lineage[]` — is landable
  right now, and is genuinely wanted.
- **A new ranked garment** needs a **slot to exist first**. Nominate it in a
  proposal issue anyway: a future band entry is ratified through the evidence
  pass in [GOVERNANCE.md](./GOVERNANCE.md#ranking-the-evidence-pass), and a
  well-argued nomination with demand evidence is exactly the input that pass
  needs. What you must not do is build the garment first and ask for a slot
  afterwards — the answer will be no however good the geometry is.

**You never edit the band indexes.** A maintainer claims the slot — in the
platform repo, § 0.1 — *after* your cartridge passes the lanes. A slot marked
claimed before the object is verified is a false statement about the commons.

### 5.3 Open it

Fork, branch, commit, and open the PR against `main`. Include in the PR body:
the census result, your local lane output (paste the read-proof summary lines),
your i18n attestation (§ 3.3), and your landing route (§ 5.2).

---

## 6. What reviewers check

The split is deliberate and the halves are not interchangeable.

**The lanes verify the object** — schema conformance, geometry, seam parity,
interface composability, the hardware bridge, the licence and provenance fields.
All blocking, all fail-closed, all read-proof. A reviewer may not wave a red lane
through; there is no "advisory but red" state in this commons.

**The reviewer verifies everything a machine cannot** — whether the lineage is
*true*, whether a cited source says what the PR claims it says, whether the
census was really run, whether a heritage garment's documentation attributes
rather than appropriates, whether the `es` register is right and the `fr`/`pt`
strings were reviewed by a human rather than generated, and whether the geometry
is a garment someone could actually sew.

---

## 7. Turnaround, honestly

This commons is maintained by a very small team. Expect days rather than hours
for a first response, and expect a proposal issue to be answered faster than a
large PR. If we disagree with a submission you will get the reasoning, not
silence.

---

## 8. Sign-off

### **[RULING PENDING: CLA vs DCO]**

**How a contributor signs work into the commons has not been ruled.** This is an
operator decision, not a maintainer one and not an agent one. Until it is made:

- Proposals, PRs, review, and iteration are all **open**.
- **No third-party contribution can be merged.** This is deliberate. Merging
  outside work before the sign-off mechanism exists would put an object into a
  CERN-OHL-W-2.0 commons with no record of the right to place it there — the
  exact defect the FC1 ruling and the day-one `attribution` requirement exist to
  prevent.

Both paths are scaffolded and either can be switched on the day the ruling
lands. The switch is a repository variable, `FC_CONTRIBUTION_SIGNOFF`:

| `FC_CONTRIBUTION_SIGNOFF` | Effect |
|---|---|
| *unset* (today) | No sign-off lane runs. Merging outside work is blocked by policy, not by CI. |
| `dco` | The DCO lane in [`.github/workflows/contribution-signoff.yml`](./.github/workflows/contribution-signoff.yml) runs and blocks on any commit missing a valid `Signed-off-by`. |
| `cla` | The CLA path (below) — requires the operator to publish a CLA text and a signature record first. |

#### Variant A — DCO (Developer Certificate of Origin 1.1)

*Lightweight; no rights assignment; the contributor certifies they have the
right to submit. This is the path the workflow already implements.*

Every commit carries a real-name sign-off trailer:

```
Signed-off-by: Jane Q. Contributor <jane@example.org>
```

which `git commit -s` adds for you. It certifies
[DCO 1.1](https://developercertificate.org/) — the text ships at
[`docs/policies/DCO.txt`](./docs/policies/DCO.txt) — that you wrote the
contribution or have the right to submit it under the commons licence, and that
you understand it is public and recorded.

**To enable:** set the repository variable `FC_CONTRIBUTION_SIGNOFF` to `dco` and
add the `Contribution sign-off / DCO` check to `main`'s required checks. The
workflow and the DCO text already ship; nothing else changes.

#### Variant B — CLA (Contributor License Agreement)

*Heavier; an explicit agreement between contributor and MADFAM, signed once and
recorded, checked per PR.*

Choosing this path requires the operator to settle, in this order:

1. **Which CLA text**, and whether it takes a copyright **licence** or a
   copyright **assignment** — for an open-hardware commons these are very
   different bargains.
2. **Where signatures live** (a signatures file in-repo, or an external service).
3. **How the check runs** — a job in the same workflow, gated on
   `FC_CONTRIBUTION_SIGNOFF == 'cla'`, resolving the PR author against the
   signature record and failing with a link to sign.
4. **What happens to contributions made before the CLA existed.**

A commented, ready-to-fill job stanza sits in
[`.github/workflows/contribution-signoff.yml`](./.github/workflows/contribution-signoff.yml)
next to the DCO job. It is commented out rather than shipped disabled because,
unlike the DCO lane, it cannot be correct until decisions 1–3 are made.

The full set of open rulings is in
[GOVERNANCE.md § Rulings this pipeline is waiting on](./GOVERNANCE.md#rulings-this-pipeline-is-waiting-on).

---

## 9. Reporting things

| What | Where |
|---|---|
| A wrong draft, a bad grade rule, a broken seam in an object | An issue on this repository |
| A bug in the kernel, a lane, the API, or the studio | An issue on the [platform repository](https://github.com/madfam-org/fashion-cabinet) |
| A new object you want to build | A proposal issue here (§ 2) |
| Wrong attribution, a licence problem, a cultural-provenance concern, a takedown request | [The provenance-dispute process](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/policies/provenance-disputes.md) |
| A security vulnerability | **Not a public issue** — see [SECURITY.md](./SECURITY.md) |
| Conduct | [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) |

---

## 10. Commit and PR hygiene

- **Conventional commits**: `feat(<slug>):`, `fix(<slug>):`, `docs(<slug>):`,
  `feat(commons):`, `ci(...)`, `chore(...)`.
- Keep the diff to your object. A drive-by reformat of an unrelated file makes a
  PR unreviewable and will be asked for separately.
- Rebase rather than merge `main` into your branch; keep the history readable.
- If the ruling lands on DCO, every commit needs `-s`. Committing with `-s` now
  costs nothing and saves a rewrite later.

---

## 11. Licence of your contribution

Objects you contribute here are licensed **CERN-OHL-W-2.0** (or a registered
carve-out per § 4.4). Platform code you contribute to the platform repository is
licensed **AGPL-3.0**. The boundary and the ruling behind it are in
[NOTICE.md](./NOTICE.md).

Weak reciprocity is the operative choice: anyone may make and sell physical
garments from these patterns with no obligation to open anything they make.
Reciprocity attaches to the *design* — modify a pattern and you publish the
modified pattern under the same terms. That is the bargain you are joining.
