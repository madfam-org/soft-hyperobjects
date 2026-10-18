#!/usr/bin/env python3
"""Opt cartridges in to an OPTIONAL export format — a mechanical, idempotent sweep.

A cartridge publishes an optional export format (today: `dxf-aama`, the
AAMA / ASTM D6673 pattern-interchange DXF) by listing it in its manifest's
`export_formats`. The platform holds every manifest to
`universal ⊆ export_formats ⊆ runner capability`, in the runner's canonical
order, and — for `dxf-aama` — renders every cartridge that lists it and checks
the file against the D6673 layer conventions (fashion-cabinet
`scripts/qa/verify_dxf_aama.py`). This script adds the format to every
manifest except the ones named in a skip file, i.e. the cartridges that lane
found non-conformant (each with its reason in that file).

Properties:
  * idempotent — a manifest that already lists the format is left byte-identical;
  * canonical order — the format is inserted where the keystone schema's
    `export_formats` enum puts it (the enum IS the runner's order, drift-checked
    platform-side), so the result is sorted the way the platform demands;
  * formatting-preserving — only the `export_formats` array is rewritten, in the
    file's own style (one-line or expanded, same indentation); no other byte of
    the manifest moves;
  * fail-visible — an unknown format, a manifest without the field, an entry the
    enum does not know, or a skip-file slug with no cartridge is an error.

Usage:
    python3 .github/scripts/opt_in_export_format.py dxf-aama \\
        --skip-file .github/scripts/dxf-aama-deferred.txt          # apply
    python3 .github/scripts/opt_in_export_format.py dxf-aama \\
        --skip-file .github/scripts/dxf-aama-deferred.txt --check  # exit 1 on drift
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DECLARATION = re.compile(
    r'^(?P<indent>[ \t]*)"export_formats"\s*:\s*(?P<value>\[[^\]]*\])',
    re.MULTILINE,
)


def canonical_order() -> list[str]:
    """The `export_formats` enum of the keystone's garment-manifest schema."""
    try:
        from importlib.resources import files

        schema = files("fc_spec").joinpath("schemas/garment-manifest.schema.json")
        doc = json.loads(schema.read_text(encoding="utf-8"))
    except (ModuleNotFoundError, FileNotFoundError) as exc:
        raise SystemExit(
            f"opt_in_export_format: the keystone (hyperobjects-spec, import fc_spec) "
            f"is not installed — it owns the canonical order ({exc})")
    return list(doc["properties"]["export_formats"]["items"]["enum"])


def read_skip_file(path: Path | None) -> dict[str, str]:
    """slug → reason. Lines are `slug  # reason`; blank lines and `#` lines skip."""
    if path is None:
        return {}
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        slug, _, reason = line.partition("#")
        out[slug.strip()] = reason.strip()
    return out


def opt_in(text: str, fmt: str, order: list[str]) -> str:
    """`text` with `fmt` added to its export_formats array (unchanged if present)."""
    match = DECLARATION.search(text)
    if not match:
        raise ValueError("no 'export_formats' array to extend — add one by hand")
    existing = json.loads(match.group("value"))
    unknown = [f for f in existing if f not in order]
    if unknown:
        raise ValueError(f"export_formats has entries the schema does not know: {unknown}")
    if fmt in existing:
        return text
    wanted = [f for f in order if f in set(existing) | {fmt}]
    indent = match.group("indent")
    if "\n" in match.group("value"):
        inner = ",\n".join(f'{indent}  "{f}"' for f in wanted)
        value = f"[\n{inner}\n{indent}]"
    else:
        value = "[" + ", ".join(f'"{f}"' for f in wanted) + "]"
    start, end = match.span("value")
    return text[:start] + value + text[end:]


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("format")
    ap.add_argument("--skip-file", type=Path)
    ap.add_argument("--check", action="store_true",
                    help="change nothing; exit 1 if any manifest would change")
    args = ap.parse_args(argv)

    order = canonical_order()
    if args.format not in order:
        print(f"opt_in_export_format: FAIL '{args.format}' is not in the schema enum {order}")
        return 1
    skip = read_skip_file(args.skip_file)
    manifests = sorted(root.glob("*/project.json"))
    if not manifests:
        print("opt_in_export_format: FAIL listed=0 manifests — refusing an empty read")
        return 1
    slugs = {p.parent.name for p in manifests}
    problems = [f"skip-file names '{s}', which has no cartridge" for s in skip if s not in slugs]

    changed = already = skipped = 0
    for path in manifests:
        slug = path.parent.name
        if slug in skip:
            skipped += 1
            continue
        text = path.read_text(encoding="utf-8")
        try:
            new = opt_in(text, args.format, order)
        except ValueError as exc:
            problems.append(f"{slug}: {exc}")
            continue
        if new == text:
            already += 1
            continue
        changed += 1
        if args.check:
            problems.append(f"{slug}: does not list '{args.format}'")
        else:
            path.write_text(new, encoding="utf-8")

    for problem in problems:
        print(f"  FAIL {problem}")
    verb = "would_add" if args.check else "added"
    print(f"opt_in_export_format: format={args.format} manifests={len(manifests)} "
          f"{verb}={changed} already={already} skipped={skipped} problems={len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
