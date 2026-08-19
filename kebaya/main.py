"""
Kebaya — Fashion Cabinet Garment Cartridge (FC-200 #199, Southeast Asian heritage).

The kebaya is the fitted, open-front blouse worn across Indonesia, Malaysia, Brunei, Singapore
and beyond — often in fine embroidered lace or voile, shaped close to the body with bust and
waist darts, an open centre-front edge (pinned or hooked, worn over a kemben or camisole), long
sleeves, and a curved front hem. This cartridge drafts the GARMENT GEOMETRY — a darted fitted
body, sleeve, curved open front — and marks (does not reproduce) the sulaman embroidery. Offered
with respect for the living traditions it belongs to.

Pieces:
  - front / back : fitted darted body (front cut 2, open CF; back on fold), curved front hem.
  - sleeve       : long fitted sleeve (cut 2 mirror).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|set

bust_girth   = float(PARAM(lambda: bust_girth, 900.0))
waist_girth  = float(PARAM(lambda: waist_girth, 720.0))
hip_girth    = float(PARAM(lambda: hip_girth, 960.0))
kebaya_length = float(PARAM(lambda: kebaya_length, 620.0))  # nape to front point
neck_width   = float(PARAM(lambda: neck_width, 170.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 580.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 230.0))
front_point  = float(PARAM(lambda: front_point, 120.0))    # how far the CF hem dips to a point
ease         = float(PARAM(lambda: ease, 70.0))            # close, fitted
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 18.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(680.0, min(bust_girth, 1400.0))
waist_girth  = max(540.0, min(waist_girth, 1250.0))
hip_girth    = max(720.0, min(hip_girth, 1450.0))
kebaya_length = max(480.0, min(kebaya_length, 850.0))
neck_width   = max(130.0, min(neck_width, 300.0))
sleeve_length = max(400.0, min(sleeve_length, 700.0))
sleeve_depth  = max(180.0, min(sleeve_depth, 360.0))
front_point  = max(0.0, min(front_point, 300.0))
ease         = max(20.0, min(ease, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

L = kebaya_length
BUST_HALF  = (bust_girth + ease) / 4.0
WAIST_HALF = (waist_girth + ease) / 4.0
HIP_HALF   = (hip_girth + ease) / 4.0
NECK_HALF  = neck_width / 2.0
SHOULDER_X = BUST_HALF
ARMSCYE_DROP = sleeve_depth
WAIST_Y = L - 300.0


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER_X, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    side_pts = [armscye_bot, fc.P(WAIST_HALF, WAIST_Y), fc.P(HIP_HALF, 0.0)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[0], side_pts[1]),
                                 fc.Line(side_pts[1], side_pts[2])])
    internals = [fc.Internal("back-dart", [fc.P(WAIST_HALF * 0.5, WAIST_Y + 90.0),
                                           fc.P(WAIST_HALF * 0.5, WAIST_Y - 110.0)], kind="dart")]
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=0.14, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                                 bulge=0.18, side=-1.0)]),
            side_edge,
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 80.0), fc.P(WAIST_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    top_y = L
    cf_x = 0.0
    neck_in = fc.P(cf_x, top_y - 40.0)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER_X, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    side_pts = [armscye_bot, fc.P(WAIST_HALF, WAIST_Y), fc.P(HIP_HALF, 0.0)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[0], side_pts[1]),
                                 fc.Line(side_pts[1], side_pts[2])])
    # open CF edge runs from the front point (dipped below hem) up to the neck
    cf_point = fc.P(cf_x, -front_point)
    internals = [
        fc.Internal("bust-dart", [fc.P(BUST_HALF, top_y - ARMSCYE_DROP - 20.0),
                                  fc.P(WAIST_HALF * 0.55, top_y - ARMSCYE_DROP - 60.0)],
                    kind="dart"),
        fc.Internal("waist-dart", [fc.P(WAIST_HALF * 0.5, WAIST_Y + 90.0),
                                   fc.P(WAIST_HALF * 0.5, WAIST_Y - 110.0)], kind="dart"),
        fc.Internal("front-lace-band", [fc.P(cf_x + 15.0, 0.0), fc.P(cf_x + 15.0, top_y - 60.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(cf_point, neck_in)]),
            fc.Edge("neck", [fc.Line(neck_in, neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                                 bulge=0.18, side=-1.0)]),
            side_edge,
            fc.Edge("hem", [fc.curve_through(fc.P(HIP_HALF, 0.0), cf_point, bulge=0.22, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 80.0), fc.P(WAIST_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (open, darted, lace band)",
    )


def build_sleeve(head_h=None):
    # sleevehead height is solved to the measured armscye edge so the seam balances.
    head_h = sleeve_depth if head_h is None else head_h
    sw = sleeve_length
    wrist = BUST_HALF * 0.5
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - wrist) / 2.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(sw, (head_h - wrist) / 2.0),
                                     fc.P(sw, (head_h + wrist) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + wrist) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("kebaya")
    everything = target_piece == "set"
    back = build_back()
    armscye_len = next(e for e in back.edges if e.name == "armscye").length()
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve(armscye_len))
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armscye"), tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "embroidered lace, voile, or fine cotton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; a fine, often sheer fabric."},
        {"item": "front fastening (kerongsang brooches or hooks)", "qty": 1, "unit": "set",
         "note": "the open front is pinned with brooches or hooked; the maker's/wearer's choice."},
        {"item": "sulaman embroidery / lace edging", "qty": 1, "unit": "as applied",
         "note": "the embroidery and lace carry the identity — the maker's."},
        {"item": "fine thread", "qty": 1, "unit": "spool",
         "note": "French or bound seams; roll the hems."},
    ]
    pattern.metadata = {
        "fc200_rank": 199, "family": "heritage_global", "fabric_hint": "encaje-voile",
        "heritage_note": "The kebaya is living dress across Indonesia, Malaysia, Brunei, Singapore "
            "and beyond, recognised by UNESCO. This cartridge drafts the GARMENT GEOMETRY only — "
            "the sulaman embroidery, the lace, and the kerongsang brooches that carry regional and "
            "personal identity are the maker's/wearer's and are not reproduced here. With respect.",
        "construction": "a close darted body (bust + waist darts over common seams) with an open "
            "curved front worn over a camisole, and fitted sleeves; side/armscye seams balance.",
        "solved": {"bust_q_mm": round(BUST_HALF, 1), "waist_q_mm": round(WAIST_HALF, 1),
                   "front_point_mm": round(front_point, 1)},
    }
    return pattern


result = build()
