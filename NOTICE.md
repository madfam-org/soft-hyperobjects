# Notice — licence, provenance, and carve-outs

This file states what the commons is licensed under, what its provenance
actually is, and where an exception would be recorded if one were ever ruled.
It reports rulings made elsewhere; it does not make any.

## Licence

Every object in this repository is **CERN-OHL-W-2.0**. That is the **FC1
ruling**, made by the operator on 2026-08-25 and recorded at
[`docs/rulings/fc1-commons-license.md`](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/rulings/fc1-commons-license.md)
in the Fashion Cabinet platform repository. The full licence text is in
[LICENSE](./LICENSE).

**No agent, and no maintainer, chooses a licence.** Licences are operator
rulings ([GOVERNANCE.md](./GOVERNANCE.md)), and this repository applies the one
already made rather than issuing a new one.

### How an object declares it

Every manifest carries the SPDX identifier in **two** machine-read fields, which
must both be present and must agree:

```json
{
  "project":     { "attribution": { "license": "CERN-OHL-W-2.0", "lineage": [ ... ] } },
  "hyperobject": { "commons_license": "CERN-OHL-W-2.0" }
}
```

`hyperobject.commons_license` is `required` in the schema, so a third party
validating with `fc-spec` alone is told about the licence field by the contract
rather than discovering it from a CI lane they cannot run.

Objects do **not** ship a per-directory `LICENSE` file. An in-repo object is
covered by the text in [LICENSE](./LICENSE) plus its declared
`commons_license` — the same convention `solid-hyperobjects` uses, where only a
cartridge published as its own standalone repo carries its own copy. The
declaration is the normative statement; `LICENSE` is the text it points at.

## Provenance

The provenance audit performed at the FC1 ruling found the commons **uniformly
MADFAM-authored, with zero third-party lineage sources and zero external `url`
fields**. Every one of the 516 objects is original work drafted against the
kernel, not a port or a re-license of someone else's pattern.

The platform regenerates a dated attestation of that fact from the manifests
themselves (`scripts/qa/provenance_attestation.py --check`) rather than letting
anyone hand-type it. That lane also enforces the corollary this repository
inherits: **no stray `LICENSE` or `COPYING` file at any depth inside a
cartridge.**

## Carve-outs

**There are none, and an empty registry is the correct state.**

The FC1 ruling is uniform by design, and it says what its single exception looks
like: *"a genuinely third-party-licensed object would need an explicit
documented carve-out, never a lone differing manifest."* That registry is
[`docs/licenses/CARVE-OUTS.md`](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/licenses/CARVE-OUTS.md)
in the platform repository, machine-read by `scripts/qa/verify_compliance.py` on
every CI run. A manifest whose licence differs and whose slug is not registered
there is a hard error — not a warning, not a review note.

A carve-out is for an object **genuinely** derived from a third-party source
whose licence the derivative must carry and which CERN-OHL-W-2.0 cannot satisfy.
That is a narrow set. It is **not** for an object whose provenance is merely
unclear (that is a provenance dispute, or a reason not to land the object), and
it is **not** for a contributor's preference for a different licence on their
own original work — the commons is uniformly licensed.

Only the **operator** may rule a carve-out. The registry row and the object land
in the same pull request: a row whose slug has no cartridge, and a cartridge
whose licence differs with no row, are both CI failures.

> **Registry location during the transition.** The registry and its enforcement
> lane still live in the platform repository, which is where they run today
> against the pinned commons. Moving them here is part of the follow-on tranche
> recorded in [MIGRATION.md](./MIGRATION.md).

## Provenance disputes and takedowns

A wrong or missing attribution, an unlicensed source, a cultural-provenance
concern, or a takedown request is **not** a security report and **not** an
ordinary bug. It follows the intake, evidence standard, interim-unlisting,
resolution and appeal process in
[`docs/policies/provenance-disputes.md`](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/policies/provenance-disputes.md).

Interim measures unlist an object from the indexes and catalogue **without
deleting history**.

## Irrevocability

**A published licence grant cannot be withdrawn.** CERN-OHL-W-2.0, once
published for a version, is irrevocable for that version. Removing an object
from this repository removes it from *distribution here*; it does not and cannot
un-license copies already made.

The lanes enforce the corollary: no object may return to the retired
`LicenseRef-FC1-pending` sentinel. That sentinel is a hard error under any
circumstances and is never carve-out-able.

## Cross-commons

CERN-OHL-W-2.0 matches what `solid-hyperobjects` uses. That is deliberate: an
object can cross between the two commons — a garment referencing a solid notion
through `notion.hardware_ref` — without a licence boundary in the middle.
