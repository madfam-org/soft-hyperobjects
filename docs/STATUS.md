# soft-hyperobjects: status as of 2026-10-05

A dated snapshot for someone resuming from a fresh clone. **The
[open-PR list](https://github.com/madfam-org/soft-hyperobjects/pulls) is
authoritative**; when this file and GitHub disagree, GitHub wins. Operator
runbooks are kept privately. This repository deploys nothing itself: Fashion
Cabinet mounts it as its `projects/` submodule.

## Where it stands

- `main` is `c7edcd93`; `SPEC_PIN` is the keystone at `142db18`, the same SHA as
  the solid commons. The soft pin always equals solid's `SPEC_PIN`.
- 516 garment, block, notion and technique cartridges; CI checks every manifest
  with `fc-spec` at that pin.
- The digital twins work (assemblies, kinematics, graph twins) lives in the
  solid commons; nothing in it needs a soft-commons change. Garments reach the
  twin store through Fashion Cabinet's type-shell publisher, which is queued.

## Landed recently

| PR | What it did |
|---|---|
| [#18](https://github.com/madfam-org/soft-hyperobjects/pull/18)–[#20](https://github.com/madfam-org/soft-hyperobjects/pull/20) | `head_girth` source defaults aligned with their manifests (570) |
| [#21](https://github.com/madfam-org/soft-hyperobjects/pull/21)–[#29](https://github.com/madfam-org/soft-hyperobjects/pull/29) | `SPEC_PIN` bumps that follow the solid commons, ending at `142db18` (keystone 0.9.0; `fc_spec` unchanged) |

## Open PRs, in merge order

None of them deploys.

| PR | Purpose | Precondition |
|---|---|---|
| [#30](https://github.com/madfam-org/soft-hyperobjects/pull/30) | Docs: install commands at `SPEC_PIN`, related contracts, and this status file | CI green; any order |
| [#7](https://github.com/madfam-org/soft-hyperobjects/pull/7) | Brazilian-Portuguese backfill for all manifests | Predates this programme; not part of this queue |

## Next steps

1. **`SPEC_PIN` bump** after hyperobjects-spec#57 and #58 land, to the same SHA
   as solid-hyperobjects. Check every manifest with `fc-spec` at the new SHA first.
2. Nothing else in this repository is queued by the programme.

## Cross-repo contracts

See the README's [Related repositories and contracts](../README.md#related-repositories-and-contracts):
`fc-spec`, `ho-bridge` and the identity key in hyperobjects-spec, the solid
commons and its assemblies, and yantra4d's Fashion Cabinet consumers.
