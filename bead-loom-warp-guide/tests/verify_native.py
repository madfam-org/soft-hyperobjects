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


with tempfile.TemporaryDirectory(prefix="native-guide-review-") as temporary:
    folder = Path(temporary)
    defaults = {p["id"]: p["default"] for p in manifest["parameters"]}
    for params in (defaults, defaults | manifest["presets"][0]["values"]):
        guide = render(folder, params)
        assert len(guide["pieces"]) == 1 and not guide["seams"]
        meta = guide["metadata"]
        assert meta["output_role"] == "reference-guide"
        assert meta["material_cutting_required"] is False
        assert meta["warp_threads"] == 8 and meta["warp_cut_length_mm"] is None
        assert abs(meta["working_length_mm"] - params["length"] * 0.8) < 1e-9
        assert len(guide["pieces"][0]["internals"]) == 10
        assert guide["bom"][0]["unit"] == "reference-guide"
        assert "do not cut textile" in guide["bom"][0]["note"]
        for fmt in ("svg", "dxf", "pdf"):
            render(folder, params, fmt)
print(f"native reference-guide check: cartridge={root.name} renders={count} failures=0")
