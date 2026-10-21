"""Native regression; run with an FC Python environment and --runner fc_runner.py.
Missing dependencies or runner fail; no skipped render is counted as a pass.
"""

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--runner", required=True, type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "project.json").read_text())
runner = args.runner.resolve(strict=True)
count = 0


def render(folder, params, fmt="json", fails=False):
    global count
    count += 1
    target = folder / (str(count) + "." + fmt)
    run = subprocess.run(
        [
            sys.executable,
            str(runner),
            str(root / "main.py"),
            str(target),
            json.dumps(params),
            fmt,
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    if fails:
        assert run.returncode != 0 and not target.exists(), run.stdout + run.stderr
        return None
    assert run.returncode == 0 and target.stat().st_size > 0, run.stdout + run.stderr
    if fmt == "json":
        result = json.loads(target.read_text())
        assert result["pieces"] and not result["issues"]
        assert all(seam["ok"] for seam in result["seams"])
        return result
    return target


def points(svg, role):
    el = next(
        e
        for e in ET.parse(svg).getroot().iter()
        if e.tag.endswith("polygon") and e.attrib.get("class") == role
    )
    return [tuple(map(float, p.split(","))) for p in el.attrib["points"].split()]


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def simple(poly):
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        for j in range(i + 2, n):
            if i == 0 and j == n - 1:
                continue
            c, d = poly[j], poly[(j + 1) % n]
            assert not (
                cross(a, b, c) * cross(a, b, d) < -1e-8
                and cross(c, d, a) * cross(c, d, b) < -1e-8
            ), (i, j)


with tempfile.TemporaryDirectory(prefix="native-scallop-review-") as temporary:
    folder = Path(temporary)
    defaults = {p["id"]: p["default"] for p in manifest["parameters"]}
    bounds = {p["id"]: (p["min"], p["max"]) for p in manifest["parameters"]}
    cases = [defaults, defaults | manifest["presets"][0]["values"]]
    cases += [
        {"length": l, "width": w} for l in bounds["length"] for w in bounds["width"]
    ]
    for params in cases:
        result = render(folder, params)
        assert result["metadata"]["scallop_count"] == 10
        svg = render(folder, params, "svg")
        stitch = points(svg, "stitch")
        cut = points(svg, "cut")
        assert len(stitch) == 203, len(stitch)
        assert len({round(p[1], 2) for p in stitch}) >= 11, (
            "Scallops collapsed to triangular teeth"
        )
        assert len(result["pieces"][0]["edges"]) == 203
        simple(stitch)
        simple(cut)
    for fmt in ("dxf", "pdf"):
        render(folder, defaults, fmt)
print(f"native scallop check: cartridge={root.name} renders={count} failures=0")
