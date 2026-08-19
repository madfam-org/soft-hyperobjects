"""
Sweater Vest — Fashion Cabinet Garment Cartridge (FC-200 #175, knitwear gap).

The knit pullover V-neck vest: a sleeveless knit layer with a deep V neck, ribbed neck/armhole/
hem bands, worn over a shirt. Distinct from FC-100's woven vests (waistcoat, puffer-vest,
hi-vis, and the new utility-vest) — this is a cut-and-sew knit pullover. Front and back share
the body width so the shoulder and side seams balance by construction; the ribbed bands are
strips solved to the measured openings.

Pieces:
  - front / back : knit body panels (cut on fold), front with a V neck.
  - band         : one ribbed band strip pattern (neck/armhole/hem cut to measured length).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|band|set

chest_girth  = float(PARAM(lambda: chest_girth, 980.0))
vest_length  = float(PARAM(lambda: vest_length, 620.0))    # nape to hem
v_depth      = float(PARAM(lambda: v_depth, 220.0))        # depth of the front V
neck_width   = float(PARAM(lambda: neck_width, 180.0))     # shoulder neck width
shoulder_w   = float(PARAM(lambda: shoulder_w, 110.0))
armhole_drop = float(PARAM(lambda: armhole_drop, 250.0))
band_height  = float(PARAM(lambda: band_height, 35.0))     # ribbed band finished height
ease         = float(PARAM(lambda: ease, 100.0))           # close knit fit
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(680.0, min(chest_girth, 1500.0))
vest_length  = max(460.0, min(vest_length, 820.0))
v_depth      = max(120.0, min(v_depth, 360.0))
neck_width   = max(130.0, min(neck_width, 300.0))
shoulder_w   = max(70.0, min(shoulder_w, 190.0))
armhole_drop = max(180.0, min(armhole_drop, 380.0))
band_height  = max(20.0, min(band_height, 70.0))
ease         = max(20.0, min(ease, 260.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = vest_length
BODY_HALF = (chest_girth + ease) / 4.0
NECK_HALF = neck_width / 2.0
SHOULDER_X = NECK_HALF + shoulder_w


def build_front():
    top_y = L
    v_point = fc.P(0.0, top_y - v_depth)
    shoulder_in = fc.P(NECK_HALF, top_y)
    shoulder_out = fc.P(SHOULDER_X, top_y)
    armhole_bot = fc.P(BODY_HALF, top_y - armhole_drop)
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), v_point)]),
            fc.Edge("neck", [fc.Line(v_point, shoulder_in)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_out)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_out, armhole_bot,
                                                 bulge=0.24, side=-1.0)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(BODY_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BODY_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 1.0, "shoulder point"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(BODY_HALF * 0.5, 60.0), fc.P(BODY_HALF * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (V-neck)",
    )


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y - 20.0)
    shoulder_in = fc.P(NECK_HALF, top_y)
    shoulder_out = fc.P(SHOULDER_X, top_y)
    armhole_bot = fc.P(BODY_HALF, top_y - armhole_drop)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, shoulder_in, bulge=0.16, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_out)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_out, armhole_bot,
                                                 bulge=0.24, side=-1.0)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(BODY_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BODY_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 1.0, "shoulder point"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(BODY_HALF * 0.5, 60.0), fc.P(BODY_HALF * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_band():
    # a representative ribbed band strip: cut to the measured opening at 0.9x (rib stretches).
    ln = 600.0                                        # reference length; maker cuts to opening
    h = band_height * 2.0
    return fc.Piece(
        "band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Ribbed band (neck/armhole/hem)",
    )


def build():
    pattern = fc.PatternSet("sweater-vest")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "sweater knit / ponte / double-knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 74% marker; a stable sweater knit for a cut-and-sew vest."},
        {"item": "rib knit for bands", "qty": 1, "unit": "as measured",
         "note": "2x1 or 1x1 rib for the V-neck, armhole, and hem bands; cut to the openings."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "knit seams; a mock-mitred point finishes the V."},
    ]
    pattern.metadata = {
        "fc200_rank": 175, "family": "knitwear", "fabric_hint": "punto-sweater",
        "silhouette_note": "A sleeveless cut-and-sew knit pullover with a deep V neck and ribbed "
            "neck/armhole/hem bands. Front and back share the body width so the seams balance; "
            "the bands are cut to the measured openings.",
        "solved": {"body_q_mm": round(BODY_HALF, 1), "v_depth_mm": round(v_depth, 1)},
    }
    return pattern


result = build()
