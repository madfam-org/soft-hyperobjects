"""
Belt Buckle — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The buckle SOLID — frame, centre bar, prong — is Yantra4D territory (belt-buckle;
see the manifest's notion.hardware_ref). What Fashion Cabinet owns is the strap:
where the strap folds back around the bar, where the prong slot is cut, how the
punch holes are pitched so the middle hole lands on the wearer's measured waist,
and where the keeper sits. The 2-D output is a STRAP TIP TEMPLATE carrying the
fold-back notch, the prong slot, the punch-hole crosses, and the keeper marks.

A centre-bar prong buckle, unlike a side-release or slide buckle, adjusts in
discrete steps — the hole pitch IS the fit resolution, so it is a parameter.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `strap_width`).
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
strap_width   = float(PARAM(lambda: strap_width, 38.0))
buckle_return = float(PARAM(lambda: buckle_return, 70.0))   # fold-back around the bar
hole_count    = int(  PARAM(lambda: hole_count, 7))
hole_pitch    = float(PARAM(lambda: hole_pitch, 25.0))
hole_dia      = float(PARAM(lambda: hole_dia, 5.0))
tip_length    = float(PARAM(lambda: tip_length, 45.0))      # taper past the last hole

# ── Clamps ───────────────────────────────────────────────────────────────────
strap_width   = max(15.0, min(strap_width, 75.0))
buckle_return = max(40.0, min(buckle_return, 120.0))
hole_count    = max(3, min(hole_count, 12))
hole_pitch    = max(15.0, min(hole_pitch, 40.0))
hole_dia      = max(3.0, min(hole_dia, 8.0))
tip_length    = max(20.0, min(tip_length, 120.0))

# The first punch hole clears the fold-back by a hole pitch, so the prong never
# fouls the folded strap.
first_hole = buckle_return + hole_pitch
run_length = first_hole + hole_pitch * (hole_count - 1) + tip_length
# The prong slot sits mid-fold, where the strap wraps the centre bar.
prong_slot_y = buckle_return / 2.0
prong_slot_len = max(hole_dia * 2.0, 12.0)


def _hole_ys():
    return [first_hole + hole_pitch * i for i in range(hole_count)]


def _cross(center, size=6.0):
    half = size / 2.0
    return [
        fc.Internal("drill-h", [fc.P(center.x - half, center.y), fc.P(center.x + half, center.y)],
                    kind="drill"),
        fc.Internal("drill-v", [fc.P(center.x, center.y - half), fc.P(center.x, center.y + half)],
                    kind="drill"),
    ]


def _circle(center, radius, name="punch-hole", sides=20):
    pts = [fc.P(center.x + radius * math.cos(2.0 * math.pi * i / sides),
                center.y + radius * math.sin(2.0 * math.pi * i / sides))
           for i in range(sides + 1)]
    return fc.Internal(name, pts, kind="marking")


def build():
    cx = strap_width / 2.0
    ys = _hole_ys()

    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(strap_width, run_length)
    bottom_right = fc.P(strap_width, 0.0)

    edges = [
        # The guide edge sits on the strap's own long edge.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = [
        # Fold line: the strap wraps the centre bar here and is stitched back.
        fc.Internal("fold-back",
                    [fc.P(0.0, buckle_return), fc.P(strap_width, buckle_return)],
                    kind="marking"),
        # The prong slot, cut on the strap centre line inside the fold.
        fc.Internal("prong-slot",
                    [fc.P(cx, prong_slot_y - prong_slot_len / 2.0),
                     fc.P(cx, prong_slot_y + prong_slot_len / 2.0)],
                    kind="drill"),
    ]
    for y in ys:
        c = fc.P(cx, y)
        internals.extend(_cross(c))
        internals.append(_circle(c, hole_dia / 2.0))

    # The middle hole is the nominal-fit hole — mark it for the wearer.
    mid = ys[hole_count // 2]

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=[
            fc.Notch("guide", buckle_return / run_length, "fold back"),
            fc.Notch("guide", mid / run_length, "nominal fit"),
        ],
        grainline=fc.Grainline(
            fc.P(strap_width * 0.85, run_length * 0.15),
            fc.P(strap_width * 0.85, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Belt Strap Tip Template",
    )

    pattern = fc.PatternSet("belt-buckle-notion")
    pattern.add(piece)
    pattern.metadata = {
        "strap_width_mm": round(strap_width, 1),
        "buckle_return_mm": round(buckle_return, 1),
        "hole_count": hole_count,
        "hole_pitch_mm": round(hole_pitch, 1),
        "adjust_range_mm": round(hole_pitch * (hole_count - 1), 1),
        "strap_cut_length_mm": round(run_length, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> belt-buckle)",
    }
    return pattern


result = build()
