"""
Knit ruana poncho — FC-400 rank #336, Lane 4 (knitwear). Fashion Cabinet Cartridge.

The ruana: an open-front poncho, a rectangle of soft knit split up the centre front so it
falls as two panels off the shoulders, with a shaped neckline at the top so it sits rather
than slides. It is the simplest wrap architecture — two mirrored rectangular panels joined
at the centre back, each with a short shoulder shoulder-seam shaping and a neckline that
scoops toward the front opening.

What this cartridge owns:
  - THE PANEL (cut 2, mirrored): a rectangle `panel_width` wide and `panel_length` tall,
    with the top corner nearest the neck shaped into a shoulder run and a neckline scoop.
  - THE CENTRE-BACK SEAM joining the two panels; the FRONT stays open (an interface).
  - Optional fringe depth marked along the hem.

Solving and clamps. The neckline scoop is derived from the neck girth and clamped so the
shoulder run never goes below a floor (a huge neck on a narrow panel would otherwise
invert the top corner). The panel width is floored so the poncho always covers the
shoulder. There are no sleeves and no closure.

Hardware: none — a ruana is open and unfastened.

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

panel_width = float(PARAM(lambda: panel_width, 520.0))     # shoulder to front edge (each panel)
panel_length = float(PARAM(lambda: panel_length, 900.0))   # neck to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
neck_scoop = float(PARAM(lambda: neck_scoop, 90.0))     # neckline scoop at the front
shoulder_run = float(PARAM(lambda: shoulder_run, 140.0))   # shaped shoulder run at the top
fringe_depth = float(PARAM(lambda: fringe_depth, 60.0))    # marked fringe zone at hem
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

panel_width = max(300.0, min(panel_width, 900.0))
panel_length = max(500.0, min(panel_length, 1300.0))
neck_girth = max(300.0, min(neck_girth, 560.0))
neck_scoop = max(20.0, min(neck_scoop, 260.0))
shoulder_run = max(60.0, min(shoulder_run, 320.0))
fringe_depth = max(0.0, min(fringe_depth, 160.0))
seam_allowance = max(6.0, min(seam_allowance, 24.0))

W = panel_width
Ln = panel_length
# Half neck width at the top of the panel: the neck opening is shared between the two
# panels at the centre back. Each panel's neck edge is a quarter of the neck opening.
NECK_Q = max(40.0, min(neck_girth / 4.0, W - 60.0))
# The shoulder run is the shaped top run from the centre-back neck point out to the
# shoulder; floored so the top corner never inverts.
SRUN = max(50.0, min(shoulder_run, W - NECK_Q - 20.0))
# Neck scoop clamped so the neckline never dips past the panel.
NSCOOP = max(15.0, min(neck_scoop, Ln * 0.4))


def build_panel():
    """One ruana panel, cut 2 mirrored. Frame: x=0 centre-back seam, y=0 hem.
    Edges: centre_back (the seam), neckline (scoops toward the front), shoulder (short
    shaped run), front (the open centre-front edge, straight down), hem."""
    top = Ln
    # centre-back seam runs full height at x=0. Neck point at (0, top). Shoulder run out
    # to (SRUN, top). Then the neckline scoops down-forward to (SRUN + a bit, top-NSCOOP)
    # and continues to the front edge at x=W.
    neck_pt = fc.P(0.0, top)
    shoulder_pt = fc.P(SRUN, top)
    front_top = fc.P(W, top - NSCOOP)
    return fc.Piece(
        "panel",
        [
            # centre-back seam: hem up to the neck point
            fc.Edge("centre_back", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            # shoulder: short shaped run across the top
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            # neckline: scoops from the shoulder point down toward the front
            fc.Edge("neck", [fc.curve_through(shoulder_pt, front_top, bulge=0.12, side=1.0)]),
            # front edge: straight down the open centre front
            fc.Edge("front", [fc.Line(front_top, fc.P(W, 0.0))]),
            # hem
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": max(seam_allowance, fringe_depth), "front": seam_allowance},
        notches=[fc.Notch("centre_back", 0.5), fc.Notch("neck", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(W * 0.3, 40.0), fc.P(W * 0.3, Ln - 40.0)),
        internals=([fc.Internal("fringe zone", [fc.P(0.0, fringe_depth),
                                                fc.P(W, fringe_depth)], kind="marking")]
                   if fringe_depth > 0.0 else []),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Ruana panel",
    )


def build():
    pattern = fc.PatternSet("poncho-knit")
    panel = build_panel()
    pattern.add(panel)
    # The two panels join at the centre back; the front stays open.
    pattern.declare_seam(("panel", "centre_back"), ("panel", "centre_back"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.85)
    pattern.bom = [
        {"item": "alpaca / soft blanket knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 85% marker (large rectangular panels "
                 "nest efficiently). A soft, draping knit gives the ruana its fall."},
        {"item": "thread (wool)", "qty": 1, "unit": "spool",
         "note": "one centre-back seam; the front edge and hem are finished or fringed"},
    ]
    pattern.metadata = {
        "fc400_rank": 336, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-alpaca",
        "architecture": "open-front ruana: two mirrored rectangular panels joined at the "
                        "centre back, shaped at the neckline, open down the front",
        "solved": {
            "panel_width_mm": round(W, 1),
            "panel_length_mm": round(Ln, 1),
            "neck_quarter_mm": round(NECK_Q, 1),
            "shoulder_run_mm": round(SRUN, 1),
            "neck_scoop_mm": round(NSCOOP, 1),
            "note": "the shoulder run is floored below the panel width less the neck "
                    "quarter, and the neck scoop is clamped inside the panel, so the top "
                    "corner never inverts at extremes",
        },
        "hardware": "none — a ruana is open and unfastened",
    }
    return pattern


result = build()
