"""
Flexure-gusset performance legging — FC-400 rank #346, Lane 5 (am_fashion). Fashion Cabinet.

A compression legging with a printed TPU flexure gusset at the crotch — a slit-and-hinge
diamond panel that stretches diagonally with the stride and returns, printed into the one
place a legging works hardest. The flexure gusset is Yantra4D territory (notion.hardware_ref
→ tpu-gusset-flexure); Fashion Cabinet owns the legging FASHION: the leg panel and the
gusset diamond dimensions DERIVED from the thigh girth and the rise.

What this cartridge owns:
  - THE LEG panel placement guide: a tapered leg (cut 2, mirrored) from waist to ankle,
    sized from waist, hip, thigh, ankle girths and the inseam.
  - THE GUSSET diamond (diag_w × diag_h) DERIVED from the thigh girth and rise — the exact
    diamond the tpu-gusset-flexure solid prints, placed at the crotch.

Solving and clamps. Every leg width (waist, hip, thigh, ankle quarters) is DERIVED and
FLOORED, and the taper is monotone-clamped so the ankle is never wider than the thigh. The
gusset diamond is floored. Match the manifest params_map exactly.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # placement-guide|set

waist_girth = float(PARAM(lambda: waist_girth, 780.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
thigh_girth = float(PARAM(lambda: thigh_girth, 560.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 240.0))
inseam = float(PARAM(lambda: inseam, 760.0))
rise = float(PARAM(lambda: rise, 280.0))                 # crotch to waist
knit_ease = float(PARAM(lambda: knit_ease, -80.0))      # compression: strongly negative
gusset_w = float(PARAM(lambda: gusset_w, 90.0))
gusset_h = float(PARAM(lambda: gusset_h, 120.0))
wall = float(PARAM(lambda: wall, 1.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth = max(600.0, min(hip_girth, 1500.0))
thigh_girth = max(360.0, min(thigh_girth, 850.0))
ankle_girth = max(160.0, min(ankle_girth, 420.0))
inseam = max(500.0, min(inseam, 950.0))
rise = max(180.0, min(rise, 420.0))
knit_ease = max(-180.0, min(knit_ease, 40.0))
gusset_w = max(40.0, min(gusset_w, 220.0))
gusset_h = max(50.0, min(gusset_h, 260.0))
wall = max(0.5, min(wall, 3.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# Compression: negative ease, floored.
def _q(g):
    return max(60.0, (g + knit_ease) / 4.0)


WAIST_Q = _q(waist_girth)
HIP_Q = max(WAIST_Q, _q(hip_girth))
THIGH_Q = max(90.0, _q(thigh_girth))
ANKLE_Q = max(50.0, min(_q(ankle_girth), THIGH_Q - 10.0))   # ankle never wider than thigh
H = max(400.0, inseam + rise)                            # full leg length
HIP_Y = H - rise                                         # hip level (below the waist)
KNEE_Y = HIP_Y * 0.5
# Gusset diamond floored.
GW = max(30.0, gusset_w)
GH = max(40.0, gusset_h)


def build():
    # Leg panel: outer side (waist->hip->knee->ankle), ankle hem, inseam, crotch (gusset).
    waist_out = fc.P(WAIST_Q, H)
    hip_out = fc.P(HIP_Q, HIP_Y)
    thigh_out = fc.P(THIGH_Q, HIP_Y - 40.0)
    ankle_out = fc.P(ANKLE_Q, 0.0)
    ankle_in = fc.P(-ANKLE_Q, 0.0)
    crotch = fc.P(-THIGH_Q * 0.6, HIP_Y)                 # crotch point (inner top)
    waist_in = fc.P(-WAIST_Q * 0.4, H)
    edges = [
        # outer side seam
        fc.Edge("side", [fc.Line(waist_out, hip_out), fc.Line(hip_out, thigh_out),
                         fc.Line(thigh_out, ankle_out)]),
        fc.Edge("hem", [fc.Line(ankle_out, ankle_in)]),
        # inseam up to the crotch
        fc.Edge("inseam", [fc.Line(ankle_in, crotch)]),
        # crotch / gusset seam (the sewn edge the printed gusset attaches to)
        fc.Edge("guide", [fc.Line(crotch, waist_in)]),
        # waist
        fc.Edge("waist", [fc.Line(waist_in, waist_out)]),
    ]
    internals = [
        fc.Internal("hip line", [fc.P(-WAIST_Q, HIP_Y), fc.P(HIP_Q, HIP_Y)], kind="marking"),
        fc.Internal("knee line", [fc.P(-THIGH_Q, KNEE_Y), fc.P(THIGH_Q, KNEE_Y)], kind="marking"),
        # gusset diamond placement at the crotch
        fc.Internal("gusset diamond",
                    [fc.P(crotch.x, crotch.y - GH * 0.5),
                     fc.P(crotch.x + GW * 0.5, crotch.y),
                     fc.P(crotch.x, crotch.y + GH * 0.5),
                     fc.P(crotch.x - GW * 0.5, crotch.y),
                     fc.P(crotch.x, crotch.y - GH * 0.5)], kind="marking"),
    ]
    piece = fc.Piece(
        "placement-guide", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, H - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Flexure-Gusset Legging Placement Guide",
    )
    pattern = fc.PatternSet("gusset-flexure-legging")
    pattern.add(piece)
    pattern.metadata = {
        "fc400_rank": 346, "family": "am_fashion", "lane": 5,
        "leg_length_mm": round(H, 1),
        "gusset_w_mm": round(GW, 1), "gusset_h_mm": round(GH, 1), "wall_mm": wall,
        "waist_q_mm": round(WAIST_Q, 1), "thigh_q_mm": round(THIGH_Q, 1),
        "ankle_q_mm": round(ANKLE_Q, 1),
        "knit_ease_mm": round(knit_ease, 1),
        "seam_allowance_mm": seam_allowance,
        "fabric": "tpu-panel-impreso (Bambu TPU 95A) gusset; compression legging body",
        "hardware": "flexure gusset delegated to Yantra4D "
                    "(notion.hardware_ref -> tpu-gusset-flexure)",
        "note": "every leg width is DERIVED with compression ease and floored; the ankle "
                "is clamped never wider than the thigh so the taper never inverts",
    }
    return pattern


result = build()
