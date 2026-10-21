"""Native regression; run with an FC Python environment and --runner fc_runner.py.
Missing dependencies or runner fail; no skipped render is counted as a pass.
"""

import argparse
import json
import subprocess
import sys
import tempfile
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


EXPECTED_SEAMS = 3
with tempfile.TemporaryDirectory(prefix="native-piece-review-") as temporary:
    folder = Path(temporary)
    defaults = {p["id"]: p["default"] for p in manifest["parameters"]}
    changed = defaults | manifest["presets"][0]["values"]
    for params in (defaults, changed):
        full = render(folder, params)
        explicit = render(folder, params | {"target_piece": "pattern"})
        assert full == explicit
        assert len(full["seams"]) == EXPECTED_SEAMS
        assert {p["name"] for p in full["pieces"]} == {
            p["id"] for p in manifest["pieces"]
        }
        for piece in full["pieces"]:
            name = piece["name"]
            subset = render(folder, params | {"target_piece": name})
            assert subset["pieces"] == [piece], (name, subset["pieces"])
            retained = [
                s
                for s in full["seams"]
                if all(
                    ref.split(".")[0] == name
                    for side in (s["a"], s["b"])
                    for ref in side.split("+")
                )
            ]
            assert subset["seams"] == retained
            scope = subset["metadata"]["dispatch"]
            assert scope["full_set_seams_verified"] == EXPECTED_SEAMS
            assert scope["cross_piece_seams_excluded"] == EXPECTED_SEAMS - len(retained)
            if scope["bom_scope"] == "selected-pieces":
                assert subset["bom"] == [b for b in full["bom"] if b["item"] == name]
            else:
                assert (
                    scope["bom_scope"] == "full-assembly"
                    and subset["bom"] == full["bom"]
                )
        for fmt in ("svg", "dxf", "pdf"):
            render(folder, params, fmt)
    render(folder, defaults | {"target_piece": "not-a-piece"}, fails=True)
print(f"native piece-dispatch check: cartridge={root.name} renders={count} failures=0")
