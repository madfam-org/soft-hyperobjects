"""
Eyelet Grommet — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The fastener SOLID is Yantra4D territory (desk-grommet; see the manifest's
notion.hardware_ref). What Fashion Cabinet owns is the fashion — spacing and
placement — and the 2-D fabrication output: a PLACEMENT GUIDE strip that pins to a
garment placement line and transfers every fastener position as a drill-cross plus an
outline, with alignment notches on the guide edge.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `count`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
count       = int(  PARAM(lambda: count,       5))
run_length  = float(PARAM(lambda: run_length,  300.0))
end_offset  = float(PARAM(lambda: end_offset,  15.0))
strip_width = float(PARAM(lambda: strip_width, 40.0))
hole_dia    = float(PARAM(lambda: hole_dia, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
count       = max(1, min(count, 24))
run_length  = max(40.0, min(run_length, 1200.0))
end_offset  = max(5.0, min(end_offset, run_length / 2.0 - 2.0))
strip_width = max(20.0, min(strip_width, 120.0))
hole_dia    = max(4.0, min(hole_dia, 40.0))

MARK_DIA = hole_dia  # the guide-mark circle diameter (mm)


def _positions():
    if count == 1:
        return [run_length / 2.0]
    usable = run_length - 2.0 * end_offset
    spacing = usable / (count - 1)
    return [run_length - end_offset - i * spacing for i in range(count)]


def _cross(center, size=8.0):
    half = size / 2.0
    return [
        fc.Internal("drill-h", [fc.P(center.x - half, center.y), fc.P(center.x + half, center.y)],
                    kind="drill"),
        fc.Internal("drill-v", [fc.P(center.x, center.y - half), fc.P(center.x, center.y + half)],
                    kind="drill"),
    ]


def _circle(center, radius, sides=24):
    pts = [fc.P(center.x + radius * math.cos(2.0 * math.pi * i / sides),
                center.y + radius * math.sin(2.0 * math.pi * i / sides))
           for i in range(sides + 1)]
    return fc.Internal("mark-outline", pts, kind="marking")


def build():
    ys = _positions()
    cx = strip_width / 2.0

    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(strip_width, run_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge sits on the garment placement line; notches transfer marks.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = []
    for y in ys:
        c = fc.P(cx, y)
        internals.extend(_cross(c))
        internals.append(_circle(c, MARK_DIA / 2.0))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=[fc.Notch("guide", y / run_length, str(i + 1))
                 for i, y in enumerate(ys)],
        grainline=fc.Grainline(
            fc.P(strip_width * 0.8, run_length * 0.15),
            fc.P(strip_width * 0.8, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Eyelet Grommet Placement Guide",
    )

    pattern = fc.PatternSet("eyelet-grommet")
    pattern.add(piece)
    pattern.metadata = {
        "fastener_count": count,
        "spacing_mm": round((run_length - 2 * end_offset) / max(count - 1, 1), 2),
        "run_length_mm": round(run_length, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> desk-grommet)",
    }
    return pattern


result = build()
