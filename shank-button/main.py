"""
Shank Button — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The solid button itself is Yantra4D territory (CadQuery; see the manifest's
`notion.hardware_ref`). What Fashion Cabinet owns is the fashion semantics —
ligne sizing, placement math — and the 2D fabrication output: a button
PLACEMENT GUIDE strip that pins to a placket center line and transfers every
button position as a drill-cross (and alignment notches on the guide edge).

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `button_count`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
button_ligne   = float(PARAM(lambda: button_ligne, 24.0))   # 1 ligne = 0.635 mm
button_count   = int(PARAM(lambda: button_count, 6))
placket_length = float(PARAM(lambda: placket_length, 300.0))
end_offset     = float(PARAM(lambda: end_offset, 15.0))     # first/last button inset
strip_width    = float(PARAM(lambda: strip_width, 40.0))
show_outline   = bool(PARAM(lambda: show_outline, True))    # draw button circles

# ── Clamps ───────────────────────────────────────────────────────────────────
button_ligne = max(10.0, min(button_ligne, 80.0))
button_count = max(1, min(button_count, 24))
placket_length = max(60.0, min(placket_length, 1200.0))
end_offset = max(5.0, min(end_offset, placket_length / 2.0 - 5.0))
strip_width = max(24.0, min(strip_width, 120.0))

LIGNE_MM = 0.635
diameter = button_ligne * LIGNE_MM


def _button_ys():
    if button_count == 1:
        return [placket_length / 2.0]
    usable = placket_length - 2.0 * end_offset
    spacing = usable / (button_count - 1)
    return [placket_length - end_offset - i * spacing for i in range(button_count)]


def _cross(center, size=8.0):
    half = size / 2.0
    return [
        fc.Internal(
            "drill-h", [fc.P(center.x - half, center.y), fc.P(center.x + half, center.y)],
            kind="drill",
        ),
        fc.Internal(
            "drill-v", [fc.P(center.x, center.y - half), fc.P(center.x, center.y + half)],
            kind="drill",
        ),
    ]


def _circle(center, radius, sides=24):
    pts = [
        fc.P(center.x + radius * math.cos(2.0 * math.pi * i / sides),
             center.y + radius * math.sin(2.0 * math.pi * i / sides))
        for i in range(sides + 1)
    ]
    return fc.Internal("button-outline", pts, kind="marking")


def build():
    ys = _button_ys()
    center_x = strip_width / 2.0

    origin = fc.P(0.0, 0.0)
    top_left = fc.P(0.0, placket_length)
    top_right = fc.P(strip_width, placket_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge sits on the placket center line; notches transfer marks.
        fc.Edge("guide", [fc.Line(origin, top_left)]),
        fc.Edge("top", [fc.Line(top_left, top_right)]),
        fc.Edge("outer", [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = []
    for y in ys:
        center = fc.P(center_x, y)
        internals.extend(_cross(center))
        if show_outline:
            internals.append(_circle(center, diameter / 2.0))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=[fc.Notch("guide", y / placket_length, f"button {i + 1}")
                 for i, y in enumerate(ys)],
        grainline=fc.Grainline(
            fc.P(strip_width * 0.8, placket_length * 0.15),
            fc.P(strip_width * 0.8, placket_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Button Placement Guide",
    )

    pattern = fc.PatternSet("shank-button")
    pattern.add(piece)
    pattern.metadata = {
        "button_diameter_mm": round(diameter, 2),
        "button_ligne": button_ligne,
        "button_count": button_count,
        "spacing_mm": round((placket_length - 2 * end_offset) / max(button_count - 1, 1), 2),
        "hardware": "solid geometry delegated to Yantra4D (see manifest notion.hardware_ref)",
    }
    return pattern


result = build()
