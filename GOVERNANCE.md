# Governance

How the soft commons decides what enters it, who checks it, and who lands it.
This document describes the process; [CONTRIBUTING.md](./CONTRIBUTING.md)
describes how to work inside it.

`soft-hyperobjects` is a MADFAM project. It is not a foundation, it does not
have a board, and this document does not pretend otherwise. What it does have is
a small number of roles with clearly separated powers, and a rule that no role
may substitute assertion for evidence.

The same governance covers the [Fashion Cabinet](https://github.com/madfam-org/fashion-cabinet)
platform repository and its sibling commons
[`solid-hyperobjects`](https://github.com/madfam-org/solid-hyperobjects); the
four-repo split ([RFC 0038 §9](https://github.com/madfam-org/internal-devops/blob/main/rfcs/0038-commons-1000x2.md))
separated the code from the objects, not the community from itself.

---

## The roles

| Role | Held by | Decides |
|---|---|---|
| **Operator / maintainer of record** | Innovaciones MADFAM (the founder, in person) | Licences, rulings, band ratification, governance itself, and anything not delegated below. |
| **Coordinator** | A maintainer, per wave or cohort | Slot claims, wave integration, merges, snapshot refreshes, the platform's pin to this repository. |
| **Reviewer** | A maintainer, or a delegated contributor | Whether a specific PR meets the bar. Cannot merge their own work. |
| **Lanes (CI)** | [`.github/workflows/ci.yml`](./.github/workflows/ci.yml) here, plus the platform's lanes against the pin | Whether an object is *verified*. Not advisory, not overridable. |
| **Contributor** | Anyone | What to propose, and what to build once a route is agreed. |

### Operator — maintainer of record

The operator is the **maintainer of record** and holds every decision that is
not explicitly delegated. In particular, and without exception:

- **No agent, and no maintainer, chooses a licence.** The commons licence was
  ruled by the operator on 2026-08-25 — CERN-OHL-W-2.0 (the FC1 ruling; see
  [NOTICE.md](./NOTICE.md)) — and any deviation requires an operator ruling
  recorded as a **carve-out**.
- **Band ratification** — declaring that ranks *N…M* exist, with those names, in
  that order — is an operator act, on the evidence pass below.
- **The sign-off mechanism** for third-party contributions (CLA vs DCO) is an
  operator ruling. It is open; see the checklist at the end of this document.
- **The four-repo topology itself** is an operator ruling (RFC 0038 §9, ratified
  2026-08-22). What lives here versus in the platform is not a maintainer's call.
- **Process rulings are recorded, dated documents.** A decision that lives only
  in someone's memory of a conversation has not been made. The FC1 ruling is the
  template: a public in-repo record, a dated decision document, and an
  enforcement lane that makes the ruling machine-checkable.

### Coordinator — who lands things

The coordinator is the only role that writes to the ranked indexes and to `main`.

- **The coordinator claims slots**, by setting a band entry's `project` field —
  and **only after** the cartridge has passed the lanes. This is the single most
  load-bearing sequencing rule in the commons: a slot marked claimed before its
  object is verified is a false public statement. Contributors never edit the
  band indexes.
- The coordinator refreshes the pinned solid-commons hardware snapshot,
  integrates a wave or cohort, and merges.
- **The coordinator advances the platform's pin to this repository.** The
  platform mounts this repo as a submodule at `projects/`; moving that pin is a
  coordinator act, taken after this repository's lanes are green, and it is what
  makes a landed object visible in the platform. A pin advanced past a red lane
  is the same false statement as an unearned slot claim.
- The coordinator does not review their own object into the commons.

### Reviewer — who verifies

Verification is deliberately split in two, and the halves are not
interchangeable.

- **The lanes verify the object.** Schema conformance, geometry, seam parity,
  interface composability, the hardware bridge, dressed-form placement, the
  doctrine gates, the licence and provenance fields. All blocking, all
  fail-closed, all read-proof — every lane prints how many items it scanned and
  fails on a zero read, because *"found nothing wrong"* and *"read nothing"* must
  never look the same.
- **The reviewer verifies everything a machine cannot**: whether the lineage is
  *true*, whether a cited source says what the PR claims it says, whether the
  census was really run, whether a heritage garment's documentation attributes
  rather than appropriates, whether the `es` register is right and the `fr`/`pt`
  strings were reviewed by a human rather than generated, and whether the
  geometry is a garment someone could actually sew.

A reviewer may not wave a red lane through. There is no "advisory but red" state
in this commons — that pattern is a known failure mode here and is not adopted.

---

## Ranking: the evidence pass

The band indexes (FC-100 … FC-500) are the demand-ranked backlog, and rank is a
claim about the world. They currently live in the platform repository (see
[MIGRATION.md](./MIGRATION.md)); the rule is the same wherever they sit:

> **A band entry may be named provisionally. It may be *ratified* only on an
> evidence pass, and it may be marked *built* only by a coordinator after the
> object passes the lanes.**

Three states, never collapsed:

| State | Meaning | Who sets it |
|---|---|---|
| **provisional** | Named from general industry knowledge, banded rather than falsely precise. An honest placeholder ranking. | Whoever drafts the band |
| **ratified** | The band has been through a demand-evidence pass: each entry is named, gap-justified against the existing catalogue, and defensible in its band. | Operator |
| **built** | A cartridge exists, passed every lane, and the coordinator has claimed the slot (`project` set). | Coordinator |

FC-100 is still marked `provisional` — truthfully, because its seed ranking has
not had a formal evidence pass even though all 100 are built. **The commons would
rather carry an honest `provisional` label than a flattering unearned `ratified`
one.** That preference is the evidence-pass rule in one sentence.

What an evidence pass consists of, minimally: real demand signals (industry size,
search/marketplace evidence, curriculum presence, or a named practitioner's
need); a census against every existing cartridge and every other band, so an
entry is not a duplicate under a new name; a family/tier gap justification —
*why this band, why this rank neighbourhood*; and, for heritage entries, sources
for every cultural claim. A rank without evidence is a guess wearing a number.

**Contributors take part in the ranking by proposing with evidence**, not by
editing the index. A proposal issue carrying real demand evidence is exactly the
input a future band's evidence pass consumes.

---

## Landing: the path an object walks

```
proposal issue  →  route agreed (ranked slot | unranked enabler)
      →  contributor builds, verifies locally with fc-spec
      →  PR (one object)  →  CI: every blocking lane
      →  reviewer: lineage, census, sources, language, heritage, geometry
      →  sign-off  [RULING PENDING: CLA vs DCO]
      →  coordinator: merge, advance the platform pin, then claim the slot
```

Sequencing that is not negotiable:

1. **Census before slug.** Always.
2. **Licence before object.** A non-CERN-OHL-W-2.0 object needs its carve-out
   *ruled and registered first*; the registry entry and the object land together.
   A licence problem discovered during review is a stop, not a negotiation.
3. **Lanes before claim.** The slot is claimed, and the pin advanced, after the
   object is verified — never before.
4. **One object per PR**, so it can be reverted, disputed, or relicensed alone.

---

## Removing or changing an object

The commons is append-mostly, but not immutable.

- **Corrections** (geometry, translation, attribution, docs) are ordinary PRs.
- **Provenance disputes, takedown requests, and cultural-attribution concerns**
  follow [the provenance-dispute process](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/policies/provenance-disputes.md),
  which defines intake, evidence standard, interim unlisting, resolution, and
  appeal. Interim measures unlist an object from the indexes and catalogue
  **without deleting history**.
- **A published licence grant cannot be withdrawn.** CERN-OHL-W-2.0, once
  published for a version, is irrevocable for that version. Removing an object
  from this repository removes it from *distribution here*; it does not and
  cannot un-license copies already made. The lanes enforce the corollary: no
  object may return to the retired `LicenseRef-FC1-pending` sentinel.

---

## Changing this document

Governance changes are operator rulings. Propose them as an issue or a PR; they
are ratified by the operator and dated in the record. This file describes the
process actually in force — if practice and this document ever disagree, that is
a defect in one of them, and the fix is to reconcile them explicitly rather than
to let the gap stand.

---

## Rulings this pipeline is waiting on

The contribution pipeline is **scaffolded, not fully ruled**. Each item below is
an operator decision. Nothing here may be decided by a maintainer, a contributor,
or an agent, and each is marked in place in the files it affects.

- [ ] **1. Sign-off: CLA or DCO.** *(blocks all third-party merges)*
      The two variants are written up in
      [CONTRIBUTING.md § 8](./CONTRIBUTING.md#8-sign-off). The DCO lane is
      implemented and shipped **disabled** in
      [`.github/workflows/contribution-signoff.yml`](./.github/workflows/contribution-signoff.yml);
      the CLA job sits beside it, commented, because it cannot be correct until
      the CLA text and signature record exist.
      **To rule DCO:** set repository variable `FC_CONTRIBUTION_SIGNOFF=dco`
      (the DCO text already ships at
      [`docs/policies/DCO.txt`](./docs/policies/DCO.txt)), and add
      `Contribution sign-off / DCO` to `main`'s required checks.
      **To rule CLA:** settle the CLA text (licence or assignment?), the
      individual/corporate split, where signatures are recorded, then enable the
      job and set `FC_CONTRIBUTION_SIGNOFF=cla`.
- [ ] **2. Review protocol.** Who may review; whether a non-MADFAM contributor
      can hold reviewer rights; how many approvals a commons object needs (one?
      two for heritage?); and whether the coordinator role can be delegated
      outside MADFAM. The roles table above records today's practice; it does
      not presume the answer.
- [ ] **3. Role addresses.** A monitored `conduct@` and a monitored `security@`
      on a MADFAM domain, replacing the two `[PLACEHOLDER — role address
      pending]` markers in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) and
      [SECURITY.md](./SECURITY.md). Role addresses only — no personal identity
      goes in a public contact field. Enable GitHub private vulnerability
      reporting on this repository at the same time.
- [ ] **4. The next band.** All 500 ranked slots are claimed and built, so there
      is no ranked route for an outside garment today. Ratifying FC-600 (ranks
      501–600) on an evidence pass is what reopens route 1 in
      [CONTRIBUTING.md § 5.2](./CONTRIBUTING.md#52-the-ranked-index-rule).
- [ ] **5. The platform read token for the render lane.** Pattern verification
      needs the `fc` kernel, which is in the private platform repository. The CI
      job that installs it is written and **skips with a visible notice** while
      `FC_PLATFORM_READ_TOKEN` is unset, so this repository's CI is honest about
      what it did not check rather than green on a lane that never ran. Minting
      that token — or making the kernel installable publicly, which would remove
      the need for it — is an operator step. See
      [MIGRATION.md](./MIGRATION.md).
- [ ] **6. The follow-on tranche.** Which of the band indexes, fabric cards,
      bodies and interface snapshots move here, and when. Recorded with
      per-item consequences in [MIGRATION.md](./MIGRATION.md); the split as it
      stands today is deliberate and staged, not an oversight.
