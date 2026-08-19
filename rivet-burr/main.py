"""
Rivet + Burr — Fashion Cabinet Notion Cartridge (Yantra4D-bridged, Group-B co-creation).

The finding SOLID is Yantra4D territory (rivet; see the manifest's notion.hardware_ref) —
a fastener Fashion Cabinet needed that was co-created as a Yantra4D cartridge. What Fashion
Cabinet owns is the fashion — spacing and placement — and the 2-D PLACEMENT GUIDE strip
that transfers every position to the garment as a drill-cross, with alignment notches.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


cap_dia = float(PARAM(lambda: cap_dia, 9.0))
count = int(PARAM(lambda: count, 6))
run_length = float(PARAM(lambda: run_length, 240.0))
end_offset = float(PARAM(lambda: end_offset, 12.0))

cap_dia = max(5.0, min(cap_dia, 20.0))
count = max(1.0, min(count, 24.0))
run_length = max(40.0, min(run_length, 1200.0))
end_offset = max(5.0, min(end_offset, 100.0))

STRIP_W = 44.0


def _positions():
    if count == 1:
        return [run_length / 2.0]
    usable = run_length - 2.0 * end_offset
    spacing = usable / (count - 1)
    return [run_length - end_offset - i * spacing for i in range(count)]


def build():
    ys = _positions()
    cx = STRIP_W / 2.0
    origin, tl = fc.P(0.0, 0.0), fc.P(0.0, run_length)
    tr, br = fc.P(STRIP_W, run_length), fc.P(STRIP_W, 0.0)
    edges = [
        fc.Edge("guide", [fc.Line(origin, tl)]),
        fc.Edge("top", [fc.Line(tl, tr)]),
        fc.Edge("outer", [fc.Line(tr, br)]),
        fc.Edge("bottom", [fc.Line(br, origin)]),
    ]
    internals = []
    for y in ys:
        internals.append(fc.Internal(
            "drill-h", [fc.P(cx - 4.0, y), fc.P(cx + 4.0, y)], kind="drill"))
        internals.append(fc.Internal(
            "drill-v", [fc.P(cx, y - 4.0), fc.P(cx, y + 4.0)], kind="drill"))
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=0.0,
        notches=[fc.Notch("guide", y / run_length, str(i + 1)) for i, y in enumerate(ys)],
        grainline=fc.Grainline(fc.P(STRIP_W * 0.8, run_length * 0.15),
                               fc.P(STRIP_W * 0.8, run_length * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Rivet + Burr Placement Guide",
    )
    pattern = fc.PatternSet("rivet-burr")
    pattern.add(piece)
    pattern.metadata = {
        "count": count, "run_length_mm": round(run_length, 1),
        "hardware": "finding solid delegated to Yantra4D (notion.hardware_ref -> rivet)",
    }
    return pattern


result = build()
