"""
Trouser Hook and Bar — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The hook and bar plates are Yantra4D territory (trouser-hook-bar; see the
manifest's notion.hardware_ref). What Fashion Cabinet owns is the waistband
closure: where the hook plate sits on the underlap and the bar plate on the
overlap so the two meet with the fly centred, how far each is inset from the
waistband end, and where the sew holes land relative to the waistband seams. The
2-D output is a WAISTBAND CLOSURE TEMPLATE: two plate footprints offset by the
underlap, their sew-hole crosses, and notches on the guide edge at the waistband
seam and at each plate.

A hook and bar is the flat closure trousers use because a button would print
through under a jacket — so the whole point is that it sits inside the waistband
sandwich, which is what the inset parameters control.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `hook_width`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
hook_width       = float(PARAM(lambda: hook_width, 18.0))
waistband_height = float(PARAM(lambda: waistband_height, 40.0))
end_offset       = float(PARAM(lambda: end_offset, 15.0))   # plate inset from the end
underlap         = float(PARAM(lambda: underlap, 40.0))     # hook-to-bar offset
sew_holes        = int(  PARAM(lambda: sew_holes, 4))

# ── Clamps ───────────────────────────────────────────────────────────────────
hook_width       = max(10.0, min(hook_width, 30.0))
waistband_height = max(25.0, min(waistband_height, 70.0))
end_offset       = max(5.0, min(end_offset, 40.0))
underlap         = max(15.0, min(underlap, 120.0))
sew_holes        = max(2, min(sew_holes, 6))

# The template spans the underlap plus a plate and its inset at each end.
run_length = underlap + 2.0 * (end_offset + hook_width)
# The plate sits centred on the waistband height.
plate_cy = waistband_height / 2.0
plate_len = hook_width * 1.6  # the plate is longer than it is wide


def _plate_centres():
    """(y, name) of the hook plate (underlap side) and bar plate (overlap side)."""
    hook_y = end_offset + hook_width / 2.0
    bar_y = run_length - end_offset - hook_width / 2.0
    return [(hook_y, "hook"), (bar_y, "bar")]


def _cross(center, size=5.0):
    half = size / 2.0
    return [
        fc.Internal("drill-h", [fc.P(center.x - half, center.y), fc.P(center.x + half, center.y)],
                    kind="drill"),
        fc.Internal("drill-v", [fc.P(center.x, center.y - half), fc.P(center.x, center.y + half)],
                    kind="drill"),
    ]


def _hole_offsets():
    """Sew-hole positions along the plate, relative to the plate centre."""
    if sew_holes == 2:
        return [-plate_len / 4.0, plate_len / 4.0]
    span = plate_len * 0.7
    step = span / (sew_holes - 1)
    return [-span / 2.0 + step * i for i in range(sew_holes)]


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(waistband_height, run_length)
    bottom_right = fc.P(waistband_height, 0.0)

    edges = [
        # The guide edge sits on the waistband's top seam line.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = []
    notches = []
    half_w = hook_width / 2.0
    half_l = plate_len / 2.0
    for y, name in _plate_centres():
        # The plate footprint, centred on the waistband height.
        internals.append(fc.Internal(
            f"{name}-plate",
            [fc.P(plate_cy - half_w, y - half_l), fc.P(plate_cy + half_w, y - half_l),
             fc.P(plate_cy + half_w, y + half_l), fc.P(plate_cy - half_w, y + half_l),
             fc.P(plate_cy - half_w, y - half_l)],
            kind="marking"))
        for d in _hole_offsets():
            internals.extend(_cross(fc.P(plate_cy, y + d)))
        notches.append(fc.Notch("guide", y / run_length, f"{name} plate"))

    # The closure centre: where the two plates meet when the waistband is done up.
    internals.append(fc.Internal(
        "closure-centre",
        [fc.P(0.0, run_length / 2.0), fc.P(waistband_height, run_length / 2.0)],
        kind="marking"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=notches,
        grainline=fc.Grainline(
            fc.P(waistband_height * 0.85, run_length * 0.15),
            fc.P(waistband_height * 0.85, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waistband Hook-and-Bar Template",
    )

    pattern = fc.PatternSet("trouser-hook-notion")
    pattern.add(piece)
    pattern.metadata = {
        "hook_width_mm": round(hook_width, 1),
        "waistband_height_mm": round(waistband_height, 1),
        "underlap_mm": round(underlap, 1),
        "sew_holes_per_plate": sew_holes,
        "template_run_mm": round(run_length, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> trouser-hook-bar)",
    }
    return pattern


result = build()
