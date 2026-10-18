#!/usr/bin/env python3
"""Is the `fc` kernel reachable? Say so in a way nobody can misread.

Pattern verification (render + seam parity) needs the `fc` drafting kernel,
which lives in the PRIVATE platform repository. CI reads it with the repository
secret ``FC_PLATFORM_READ_TOKEN``. While that secret is unset, nothing can be
rendered — and until 2026-10-18 the pattern jobs then concluded **success**:
the job summary said "not verified", but every check list showed a green tick
next to "Pattern verification" and "Nightly pattern sweep". A lane that did not
run and a lane that passed looked the same (geo-stab audit A2, finding D3).

This script is the single place that decides what a missing kernel means, per
lane:

  probe    The ``kernel`` job. Writes ``available=true|false`` to
           ``$GITHUB_OUTPUT`` so the ``patterns`` job can NAME ITSELF after the
           result ("Pattern verification — NOT VERIFIED (no kernel)"). Exit 0.

  pr       The ``patterns`` job on pull_request / push. A contributor cannot
           mint the token, so a PR is not failed for its absence — but the job
           emits a ``::warning::`` annotation and a "NOT VERIFIED: no kernel"
           job-summary block before it exits 0, and (through ``probe``) its
           check name says the same.

  nightly  The ``patterns-nightly`` job (schedule, or a dispatch without a
           fixture). Its whole purpose is a full render sweep, so a missing
           kernel is a FAILURE: ``::error::`` plus the summary block, exit 1.
           A green nightly therefore always means a real sweep. The tracking
           issue is left alone either way — the reporter only fires on a sweep
           that ran.

The token value is never printed; only whether it is present (a whitespace-only
value counts as absent — it cannot authenticate).

stdlib only. Tests: ``python3 -m pytest .github/scripts``.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import NamedTuple

TOKEN_ENV = "FC_PLATFORM_READ_TOKEN"
LANES = ("probe", "pr", "nightly")
OPERATOR_STEP = "GOVERNANCE.md → *Rulings this pipeline is waiting on* → item 5"


class Verdict(NamedTuple):
    available: bool
    exit_code: int
    stdout: list          # lines for the log (annotations included)
    summary: list         # lines for $GITHUB_STEP_SUMMARY (may be empty)


def decide(token, lane: str) -> Verdict:
    """Pure decision: what a present/absent token means on ``lane``."""
    if lane not in LANES:
        raise ValueError(f"unknown lane {lane!r}; expected one of {LANES}")
    available = bool(token and token.strip())

    if available:
        line = {
            "probe": "kernel: token present — pattern verification will run.",
            "pr": "patterns: kernel token present — the render lane will run.",
            "nightly": "nightly: kernel token present — the sweep will run.",
        }[lane]
        return Verdict(True, 0, [line], [])

    if lane == "probe":
        return Verdict(False, 0, [
            f"kernel: {TOKEN_ENV} is unset — pattern verification will be "
            "reported as NOT VERIFIED."], [])

    if lane == "pr":
        return Verdict(False, 0, [
            "::warning title=Pattern verification NOT VERIFIED (no kernel)::"
            f"{TOKEN_ENV} is unset, so the fc kernel could not be installed. "
            "Nothing was rendered or seam-checked on this run; only manifest "
            "conformance was. This job exits 0 so a contributor is not blocked "
            "by a secret they cannot set — it is NOT a pass.",
            "patterns: NOT VERIFIED — no kernel, nothing was rendered or seam-checked.",
        ], [
            "### NOT VERIFIED: no kernel",
            "",
            "The render + seam-parity lane did **not** run. It needs the `fc`",
            "drafting kernel from the private platform repository, and the",
            f"repository secret `{TOKEN_ENV}` is not set (fork pull requests",
            "never receive it).",
            "",
            "**This job exiting 0 does not mean the patterns are verified.** Its",
            "check is named *Pattern verification — NOT VERIFIED (no kernel)*;",
            "only *Pattern verification (render + seam parity)* is a real pass.",
            "Only manifest conformance was checked on this run.",
            "",
            f"Operator step: {OPERATOR_STEP}.",
        ])

    # nightly
    return Verdict(False, 1, [
        "::error title=Nightly pattern sweep NOT RUN (no kernel)::"
        f"{TOKEN_ENV} is unset, so the fc kernel could not be installed and "
        "no cartridge was rendered. The nightly fails on purpose: a green "
        "nightly must mean a real sweep. No tracking issue was opened or closed.",
        "nightly: NOT VERIFIED — no kernel, nothing was rendered or seam-checked.",
    ], [
        "### NOT VERIFIED: no kernel — nightly failed on purpose",
        "",
        "The sweep did **not** run: the repository secret",
        f"`{TOKEN_ENV}` is unset, so the `fc` kernel could not be installed.",
        "This run is RED by design — a nightly that cannot render must never",
        "conclude green. No tracking issue was opened OR closed: a lane that",
        "did not run must not raise or clear a render alert.",
        "",
        f"Operator step: {OPERATOR_STEP}.",
    ])


def _append(path, lines) -> None:
    if path and lines:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--lane", required=True, choices=LANES)
    args = ap.parse_args(argv)

    v = decide(os.environ.get(TOKEN_ENV), args.lane)
    _append(os.environ.get("GITHUB_OUTPUT"),
            [f"available={'true' if v.available else 'false'}"])
    _append(os.environ.get("GITHUB_STEP_SUMMARY"), v.summary)
    for line in v.stdout:
        print(line)
    return v.exit_code


if __name__ == "__main__":
    sys.exit(main())
