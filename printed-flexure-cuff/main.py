"""
Printed Flexure Cuff — Fashion Cabinet Notion Cartridge (Yantra4D-bridged printed trim).

The flexure band itself is Yantra4D territory (CadQuery; see the manifest's
notion.hardware_ref → tpu-flexure-cuff). What Fashion Cabinet owns is the fashion — the
cuff circumference to the sleeve opening, the height, and the 2-D placement guide for the
sewn edge where the printed cuff joins the sleeve.

One material identity — Bambu TPU 95A (`tpu-panel-impreso` class) — spans this notion and
that solid, so the same cuff is a Fashion Cabinet trim and a Yantra4D object at once.

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


# ── Parameters ───────────────────────────────────────────────────────────────
wrist_girth    = float(PARAM(lambda: wrist_girth, 170.0))    # finished sleeve opening
cuff_height    = float(PARAM(lambda: cuff_height, 60.0))     # cuff band height
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))  # tape-bound sew edge
wall           = float(PARAM(lambda: wall, 2.0))             # printed wall (to the solid)

# ── Clamps (mirror the manifest ranges) ──────────────────────────────────────
wrist_girth    = max(120.0, min(wrist_girth, 320.0))
cuff_height    = max(15.0, min(cuff_height, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))
wall           = max(1.0, min(wall, 6.0))

# The cuff unrolled: a band `wrist_girth` around (the sew edge length) x `cuff_height`.
W = wrist_girth
H = cuff_height


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, H)
    top_right    = fc.P(W, H)
    bottom_right = fc.P(W, 0.0)

    edges = [
        # The guide edge is the sewn cuff edge (where the printed band meets the sleeve).
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("join",   [fc.Line(top_right, bottom_right)]),  # the band's own seam
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    # A few marking lines showing where the flexure slot rows land (orientation only).
    internals = []
    for frac in (0.33, 0.66):
        y = H * frac
        internals.append(fc.Internal(
            f"flex-row-{int(frac * 100)}", [fc.P(0.0, y), fc.P(W, y)], kind="marking"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("guide", 0.5, "cuff center"),
                 fc.Notch("bottom", 0.5, "cuff center")],
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.15), fc.P(W * 0.5, H * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Flexure Cuff Placement Guide",
    )

    pattern = fc.PatternSet("printed-flexure-cuff")
    pattern.add(piece)
    pattern.metadata = {
        "wrist_girth_mm": round(W, 1),
        "cuff_height_mm": round(H, 1),
        "wall_mm": wall,
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A)",
        "hardware": "flexure band delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-flexure-cuff)",
    }
    return pattern


result = build()
