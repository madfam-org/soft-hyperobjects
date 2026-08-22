"""
Ballet Flat Upper — Fashion Cabinet Garment Cartridge (FC-300 #234, lane 4 footwear).

The upper of a ballet flat: a one-piece `upper` wrapping the whole foot (toe to heel, both
sides) with a deep scooped topline, closed by a heel seam and finished with a `binding`
strip that folds over the topline to form an ELASTIC CASING — the drawn-in edge that makes
a ballet flat grip without any hardware at all.

The casing is the point of the draft, so it is dimensional: the binding is drafted at the
true folded width for the elastic it must carry (`elastic_w`), and the elastic is cut
SHORTER than the topline by `draw_in` — that gather is what holds the shoe on, and it is
declared as honest negative ease on the casing seam rather than pretended away.

SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json declares NO foot landmark codes, so
foot_length and foot_girth are PLAIN parameters with no `measurement` block. A ballet flat
does not reach the ankle, so no ankle code is claimed either. Nothing is invented.

Pieces:
  - upper   : the one-piece wrap (cut 1 on fold at centre front, mirrored).
  - binding : the topline casing strip (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # upper|binding|set

# Plain sized params — ISO 8559 has no foot codes.
foot_length = float(PARAM(lambda: foot_length, 250.0))
foot_girth = float(PARAM(lambda: foot_girth, 230.0))

topline_depth = float(PARAM(lambda: topline_depth, 58.0))   # how deep the scoop cuts
heel_height = float(PARAM(lambda: heel_height, 56.0))       # quarter height at the heel
elastic_w = float(PARAM(lambda: elastic_w, 6.0))            # elastic width
draw_in = float(PARAM(lambda: draw_in, 34.0))               # topline minus elastic
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
topline_depth = max(20.0, min(topline_depth, 120.0))
heel_height = max(25.0, min(heel_height, 120.0))
elastic_w = max(3.0, min(elastic_w, 20.0))
draw_in = max(0.0, min(draw_in, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
# The upper is cut on the fold at CENTRE FRONT: flat, it opens out to the whole
# wrap, toe at the fold and heel edges at the two free ends. The half-wrap run is
# the toe-to-heel path down ONE side of the foot, so a wider foot needs a longer
# run for the same length — the girth term is what makes the flat actually wrap.
LAST_HALF = foot_girth / 2.0 / 2.0 + 10.0     # half-width at the ball
HALF_WRAP = foot_length * 0.86 + LAST_HALF * 0.30

# The casing must be wide enough to pass its own elastic, plus turn-under on both
# sides. This is the binding's real folded width, not a decorative number.
CASING_W = elastic_w + 2.0 * max(2.0, seam_allowance * 0.5)


def build_upper():
    """One-piece wrap, cut on the fold at centre front. `topline` is the scooped
    edge the casing binds; `lasting` is the sole stitch-down; `heel` is the free
    end that meets its mirror at centre back."""
    ln = HALF_WRAP
    top_y = heel_height
    scoop_y = max(6.0, top_y - topline_depth * 0.5)
    internals = [
        fc.Internal("centre-front",
                    [fc.P(0.0, 0.0), fc.P(0.0, scoop_y)], kind="marking"),
        fc.Internal("elastic-casing-line",
                    [fc.P(4.0, scoop_y - CASING_W), fc.P(ln - 4.0, top_y - CASING_W)],
                    kind="marking"),
    ]
    return fc.Piece(
        "upper",
        [
            # centre_front is the fold, from the topline scoop down to the sole
            fc.Edge("centre_front", [fc.Line(fc.P(0.0, scoop_y), fc.P(0.0, 0.0))]),
            fc.Edge("lasting", [fc.curve_through(fc.P(0.0, 0.0), fc.P(ln, 0.0),
                                                 bulge=0.06, side=1.0)]),
            fc.Edge("heel", [fc.Line(fc.P(ln, 0.0), fc.P(ln, top_y))]),
            # topline scoops from the heel top down to the centre-front notch
            fc.Edge("topline", [fc.curve_through(fc.P(ln, top_y), fc.P(0.0, scoop_y),
                                                 bulge=0.16, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"lasting": 12.0},
        notches=[fc.Notch("lasting", 0.5, "side match"),
                 fc.Notch("topline", 0.5, "casing midpoint")],
        grainline=fc.Grainline(fc.P(ln * 0.30, 8.0), fc.P(ln * 0.30, top_y - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Upper (one-piece wrap)",
    )


def build_binding(topline_run):
    """The topline casing strip. Its `attach` edge equals the doubled topline (the
    upper is cut on the fold) plus its own joins; its height is twice the casing
    width so it folds over the raw topline to form the elastic tunnel."""
    band_len = topline_run + 2.0 * seam_allowance
    band_h = CASING_W * 2.0
    return fc.Piece(
        "binding",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
            fc.Edge("outer", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                    # length already carries the joins
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[
            fc.Internal("fold line",
                        [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
                        kind="marking"),
            fc.Internal("casing stitch line",
                        [fc.P(0.0, CASING_W * 0.5), fc.P(band_len, CASING_W * 0.5)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Binding (elastic casing)",
    )


def build():
    pattern = fc.PatternSet("ballet-flat-upper")
    everything = target_piece == "set"

    upper = build_upper()
    # Cut on the fold => the finished topline is twice the drafted edge.
    topline_run = 2.0 * upper.edge("topline").length(0.05)
    binding = build_binding(topline_run)
    # The elastic is cut SHORTER than the topline by draw_in — that gather is what
    # holds a ballet flat on the foot.
    elastic_len = max(60.0, topline_run - draw_in)

    if everything or target_piece == "upper":
        pattern.add(upper)
    if everything or target_piece == "binding":
        pattern.add(binding)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything or target_piece == "upper":
        # Centre back: the mirrored upper meets its own heel edge (self-seam,
        # join-to-join — the accessory self-seam rule, not join-to-fold).
        pattern.declare_seam(("upper", "heel"), ("upper", "heel"), tol=0.5)
    if everything:
        # The casing binds the doubled topline; the binding's own joins are the ease.
        casing_ease = binding.edge("attach").length(0.05) - topline_run
        pattern.declare_seam(
            [("binding", "attach")],
            [("upper", "topline"), ("upper", "topline")],
            ease=casing_ease, tol=1.0)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "garment leather, satin, or canvas (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1200 mm width, 55% marker. Per PAIR, double this."},
        {"item": "elastic", "qty": round(elastic_len), "unit": "mm_length",
         "note": f"{round(elastic_w, 1)} mm wide, cut {round(draw_in, 1)} mm SHORTER "
                 f"than the topline — the draw-in is what holds the shoe on."},
        {"item": "sole unit", "qty": 1, "unit": "pcs",
         "note": "the lasting edge stitches down to it. A hard good, out of scope."},
        {"item": "lining (optional)", "qty": 1, "unit": "as chosen",
         "note": "a lining hides the casing stitching and softens the topline."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "close the heel seam, apply the binding, stitch the casing tunnel."},
    ]
    pattern.metadata = {
        "fc300_rank": 234, "family": "footwear_soft", "fabric_hint": "piel-satin",
        "silhouette_note": "A one-piece ballet-flat upper cut on the fold at centre "
            "front, with a deep scooped topline bound by a folded strip that doubles "
            "as an elastic casing, and a single heel seam at centre back.",
        "sizing_note": "foot_length / foot_girth are PLAIN parameters — ISO 8559 as "
            "vendored declares no foot landmark codes, so none is claimed or invented. "
            "A ballet flat does not reach the ankle, so no ankle code is claimed.",
        "construction_note": "HARDWARE-FREE by design: the elastic casing IS the "
            "closure. The elastic is cut draw_in mm shorter than the topline, and the "
            "binding is drafted at the true folded width to pass its own elastic.",
        "solved": {
            "topline_run_mm": round(topline_run, 1),
            "casing_width_mm": round(CASING_W, 1),
            "elastic_len_mm": round(elastic_len, 1),
            "draw_in_mm": round(draw_in, 1),
            "half_wrap_mm": round(HALF_WRAP, 1),
            "ball_half_width_mm": round(LAST_HALF, 1),
        },
    }
    return pattern


result = build()
