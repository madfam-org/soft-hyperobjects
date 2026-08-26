"""
Lattice-drape printed skirt — Fashion Cabinet Garment Cartridge (FC-500 #410, am_fashion, T4).

A made-to-measure skirt built from a printed TPU PLEAT PANEL — a printed accordion of
vertical pleats that springs the skirt into a permanent sculptural drape (the pleats are
printed IN, not pressed, so they never fall out). Fashion Cabinet owns the fashion: an
A-line skirt panel (cut on the fold, front and back) sized from the waist and hip, and the
pleat FIELD (pleat count) DERIVED from the panel width and the pleat pitch so the accordion
exactly fills the skirt. The pleat panel is Yantra4D territory (tpu-pleat-panel).

Solved, not guessed:

  1. THE PLEAT FIELD FILLS THE PANEL EXACTLY. The pleat count is derived from the panel
     width and the pleat pitch, floored at 2 so a coarse pitch against a narrow panel never
     yields fewer than two pleats (a single pleat is not an accordion).
  2. THE WAIST AND HIP HALF-WIDTHS ARE DERIVED AND FLOORED. The hip half is never below the
     waist half, and the hem half is never below the hip half, so the A-line never inverts
     into an hourglass the kernel would CCW-normalize into a healthy-looking sliver.
  3. THE PLEAT DEPTH IS CLAMPED under the pitch so the accordion folds cannot cross through
     one another.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # panel|set

waist_girth = float(PARAM(lambda: waist_girth, 780.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 560.0))
hem_flare = float(PARAM(lambda: hem_flare, 160.0))       # each side release at hem
pleat_pitch = float(PARAM(lambda: pleat_pitch, 30.0))    # centre-to-centre pleat spacing
pleat_depth = float(PARAM(lambda: pleat_depth, 18.0))    # printed pleat fold depth
wall = float(PARAM(lambda: wall, 1.4))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

waist_girth = max(560.0, min(waist_girth, 1400.0))
hip_girth = max(600.0, min(hip_girth, 1600.0))
skirt_length = max(300.0, min(skirt_length, 1100.0))
hem_flare = max(0.0, min(hem_flare, 400.0))
pleat_pitch = max(10.0, min(pleat_pitch, 80.0))
pleat_depth = max(4.0, min(pleat_depth, 60.0))
wall = max(0.6, min(wall, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

# Panel = the skirt front quarter (cut on fold, mirrored).
WAIST_HALF = max(80.0, waist_girth / 4.0)
HIP_HALF = max(WAIST_HALF, hip_girth / 4.0)              # never below the waist
HEM_HALF = HIP_HALF + hem_flare                          # never below the hip
H = max(200.0, skirt_length)
HIP_Y = H * 0.75                                         # hip level below the waist
PANEL_W = HEM_HALF                                       # the pleat field spans the hem
# The pleat depth is clamped under the pitch so the accordion folds never cross.
PLEAT_DEPTH = min(pleat_depth, pleat_pitch * 0.45)
PLEAT_COUNT = max(2, round(PANEL_W / pleat_pitch))


def build_panel():
    """The A-line skirt panel (front quarter, cut on fold, mirrored). Waist at the top,
    hem at the bottom, an A-line side release. The pleat field runs vertically."""
    p_waist_cf = fc.P(0.0, H)
    p_waist_side = fc.P(WAIST_HALF, H)
    p_hip_side = fc.P(HIP_HALF, HIP_Y)
    p_hem_side = fc.P(HEM_HALF, 0.0)
    p_hem_cf = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("cf", [fc.Line(p_hem_cf, p_waist_cf)]),        # fold line
        fc.Edge("waist", [fc.Line(p_waist_cf, p_waist_side)]),
        fc.Edge("side", [fc.curve_through(p_waist_side, p_hip_side, bulge=0.05, side=1.0),
                         fc.curve_through(p_hip_side, p_hem_side, bulge=0.06, side=1.0)]),
        fc.Edge("hem", [fc.Line(p_hem_side, p_hem_cf)]),
    ]
    internals = []
    for i in range(PLEAT_COUNT + 1):
        x = i * (PANEL_W / PLEAT_COUNT)
        # each pleat line runs from its waist x (capped at the waist half) to its hem x
        # (capped at the hem half) so no guide line runs off the panel edge.
        internals.append(fc.Internal(f"pleat {i}",
                         [fc.P(min(x, WAIST_HALF), H), fc.P(min(x, HEM_HALF), 0.0)],
                         kind="marking"))
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "waist": 12.0},
        notches=[fc.Notch("waist", 1.0, "side seam"),
                 fc.Notch("side", 0.5, "hip"),
                 fc.Notch("hem", 0.5, "CF")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.3, 20.0),
                               fc.P(WAIST_HALF * 0.3, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cf", mirror=True),
        label="Skirt panel (front + back, cut on fold, 2)",
    )


def build():
    pattern = fc.PatternSet("lattice-drape-skirt")
    pattern.add(build_panel())

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "printed TPU pleat panel yardage",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm print width, 70% marker; a {PLEAT_COUNT}-pleat "
                 f"accordion at a {pleat_pitch:.0f} mm pitch / {PLEAT_DEPTH:.0f} mm depth "
                 f"(Yantra4D tpu-pleat-panel, notion.hardware_ref), printed the full panel so "
                 f"the drape is permanent."},
        {"item": "waistband elastic or facing", "qty": round(waist_girth * 1.0),
         "unit": "mm_length", "note": "the pleated waist gathers into a facing or elastic."},
        {"item": "matching thread", "qty": 1, "unit": "spool",
         "note": "join the two panels at the side seams; the pleats spring the drape."},
    ]
    pattern.metadata = {
        "fc500_rank": 410, "family": "am_fashion", "tier": 4,
        "fabric_hint": "tpu-panel-impreso",
        "silhouette_note": "An A-line skirt of printed TPU accordion pleats — the drape is "
            "printed in, not pressed, so it never falls out.",
        "solved": {
            "waist_half_mm": round(WAIST_HALF, 1),
            "hip_half_mm": round(HIP_HALF, 1),
            "hem_half_mm": round(HEM_HALF, 1),
            "panel_width_mm": round(PANEL_W, 1),
            "pleat_count": PLEAT_COUNT,
            "pleat_depth_requested_mm": round(pleat_depth, 1),
            "pleat_depth_clamped_mm": round(PLEAT_DEPTH, 1),
            "pleat_depth_was_clamped": bool(abs(PLEAT_DEPTH - pleat_depth) > 0.01),
            "note": "the pleat count is derived from the panel width and pitch, floored at "
                    "2; the hip half is never below the waist half and the hem half never "
                    "below the hip half so the A-line never inverts; the pleat depth is "
                    "clamped under the pitch so the accordion folds never cross.",
        },
        "hardware": "printed TPU pleat panel via Yantra4D (notion.hardware_ref -> "
                    "tpu-pleat-panel); pleats/pleat_pitch/panel_width/wall are fed from the "
                    "panel and pitch. The pleat_field interface lists every driving param so "
                    "the dimensional handshake holds.",
    }
    return pattern


result = build()
