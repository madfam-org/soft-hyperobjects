# Security Policy

This repository holds **commons objects** — parametric fabrication data, not
software. That changes what a security report means here, so please read § 1
before reporting: it decides whether your report belongs here or in the platform
repository.

## 1. Scope

| Where | What it is | Licence | In scope for a security report *here*? |
|---|---|---|---|
| `<slug>/project.json`, `<slug>/docs/` | Cartridge manifests and documentation — parameters, sizes, BOMs, provenance | CERN-OHL-W-2.0 | **Usually no** — see § 2 |
| `<slug>/main.py` | Cartridge draft scripts — **executed**, in a restricted sandbox | CERN-OHL-W-2.0 | **Only for a sandbox escape** — see § 1.1 |
| The `fc` kernel, the sandbox core, the API, the studio, the CI lanes | Platform software | AGPL-3.0 | **No — report to the [platform repository](https://github.com/madfam-org/fashion-cabinet/security)** |
| `fc-spec`, the schemas, the validators | The keystone toolchain | permissive | **No — report to [`hyperobjects-spec`](https://github.com/madfam-org/hyperobjects-spec/security)** |

The licence split is not cosmetic. Platform code is software under AGPL-3.0.
Commons objects are *fabrication data* — pattern pieces, BOMs, construction
operations — under CERN-OHL-W-2.0. A finding in a cartridge is nearly always a
**correctness** or **provenance** matter rather than a security one.

### 1.1 The one part of the commons that is security-critical

Cartridge scripts (`<slug>/main.py`) are **executed**, in a restricted sandbox
(`packages/commons-sandbox` in the platform — restricted builtins, blocked
modules, killable subprocess). Therefore:

- **A sandbox escape is a security vulnerability.** If you can make a cartridge
  script read a file, open a socket, import a blocked module, reach the host
  environment, or survive its kill, report it privately under § 3.
- A cartridge that merely produces wrong geometry is a bug — § 2.
- A cartridge with a false `attribution`/`lineage`, or a licence problem, is a
  **provenance dispute** — see
  [the process](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/policies/provenance-disputes.md).

**Where to send a sandbox escape.** The escape is a defect in the *sandbox*, which
is platform code — so the fix lands there. If your demonstration is a cartridge
script, report it privately through the platform repository's private
vulnerability reporting and say that the proof-of-concept is a commons cartridge.
Reporting it here privately is also fine; a maintainer will route it.

Denial of service through an expensive-but-legitimate render is a **bug report**
with a note, not a vulnerability report, unless it escapes the runner's limits.

## 2. What is *not* a vulnerability here

- A pattern that drafts incorrectly, a seam that does not match, a wrong
  measurement, a bad grade rule → an ordinary issue on this repository.
- A wrong or missing attribution, an unlicensed source, a cultural-provenance
  concern, a takedown request →
  [provenance dispute](https://github.com/madfam-org/fashion-cabinet/blob/main/docs/policies/provenance-disputes.md).
- A scanner's generic advisory with no demonstrated impact. Please include the
  impact.

## 3. Reporting a vulnerability

**Do not open a public issue for a security report.**

> **Preferred:** GitHub **private vulnerability reporting** on this repository —
> the *Security* tab → *Report a vulnerability*. It is private to the
> maintainers, it threads, and it needs no address to be published first.
>
> **Alternative:** **`[PLACEHOLDER — role address pending]`**
>
> A monitored **role address** (of the form `security@<a MADFAM domain>`) is set
> here by the operator before this document is advertised publicly. It is a role
> address on purpose: reports reach a function, never a named individual.

If both channels are unavailable to you, open a public issue that says only
*"I have a security report and need a private channel"* — with **no details** —
and a maintainer will open one.

### What to include

1. The affected surface (cartridge slug, or the platform package if you know it)
   and the commit you tested.
2. What an attacker gains — the impact, stated plainly.
3. A minimal reproduction. For a sandbox escape, the smallest cartridge script
   that demonstrates it.
4. Whether it is already public anywhere.

### What to expect

This commons is maintained by a very small team, and this policy will not
promise a response time it cannot keep:

- **Acknowledgement:** we aim for a few working days.
- **Assessment and a plan:** as soon as the report is understood; you will be
  told what we think it is and what we intend to do.
- **Fix and disclosure:** coordinated with you. We will tell you when a fix
  ships and, unless you ask otherwise, credit you by the name or handle you
  choose.
- **If we disagree** that a report is a vulnerability, you will get the
  reasoning, not silence.

Please give us a reasonable window to fix an issue before disclosing it
publicly. We will not take legal action against good-faith research that stays
within this scope, avoids privacy violations and service degradation, and does
not access, modify, or exfiltrate data that is not yours.

## 4. Supported versions

This commons ships from `main`, and the platform consumes it at a pinned commit.
There are no maintained release branches. Fixes land on `main` and the pin is
advanced. Report against `main` unless you are specifically demonstrating a
regression.
