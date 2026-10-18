# Soft Hyperobjects Agent Operating Guide

> Last Updated: 2026-10-18

Read [README.md](./README.md), [CONTRIBUTING.md](./CONTRIBUTING.md), and
[GOVERNANCE.md](./GOVERNANCE.md) before changing cartridges or verification rules.
Preserve unrelated work. Keep verification fail-closed; missing kernel access is
an explicit unverified result, never successful geometry evidence.

Pattern verification (render + seam parity) runs only when the repository
secret `FC_PLATFORM_READ_TOKEN` can install the private `fc` kernel. Read the
check name: *Pattern verification (render + seam parity)* is a real pass;
*Pattern verification — NOT VERIFIED (no kernel)* rendered nothing (warning +
job-summary block, exit 0), and a nightly without the kernel fails on purpose.
Never cite either of the latter as geometry evidence. The rules live in
`.github/scripts/kernel_gate.py`; run `python3 -m pytest .github/scripts` after
changing CI scripts. See README.md, "How CI verifies a change".

## Repository boundary

Read [the public repository boundary](./docs/PUBLIC_REPO_BOUNDARY.md).
Owns parametric garment, block, notion and technique cartridges. Fashion Cabinet owns the fc drafting kernel and platform; hyperobjects-spec owns shared schemas and validators. Printable solid counterparts belong to solid-hyperobjects.

Do not change licensing, ranked bands, topology or platform access without the
operator ruling required by GOVERNANCE.md. Routine production operations use
Enclii web, API or CLI; secrets enter through Enclii secret intake. This commons
contains neither deployment credentials nor platform application code.
