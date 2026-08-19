"""
Cocoon Coat — Fashion Cabinet Garment Cartridge (FC-200 #190, outerwear gap).

The cocoon coat: a coat with a rounded, curved silhouette — wide and softly bowed through the
body, narrowing to a hem that pulls IN below the hip, wrapping the body like a cocoon, usually
with grown or dropped sleeves and a minimal collar. Distinct from FC-100's straight overcoat and
the swing coat (which flares OUT). The curved side seam bows out at the hip and back in at the hem;
front and back share the identical curved side so it balances by construction.

Pieces:
  - front / back : cocoon body panels (front cut 2 with lap; back on fold), curved side seam.
  - sleeve       : dropped/grown sleeve rectangle (cut 2 mirror).

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

chest_girth  = float(PARAM(lambda: chest_girth, 1040.0))
coat_length  = float(PARAM(lambda: coat_length, 950.0))
neck_girth   = float(PARAM(lambda: neck_girth, 440.0))
sleeve_grown = float(PARAM(lambda: sleeve_grown, 300.0))   # grown/dropped sleeve length
sleeve_depth = float(PARAM(lambda: sleeve_depth, 300.0))
cocoon_bow   = float(PARAM(lambda: cocoon_bow, 180.0))     # how far the side bows OUT at the hip
hem_pull     = float(PARAM(lambda: hem_pull, 120.0))       # how far the hem pulls IN below hip
ease         = float(PARAM(lambda: ease, 320.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(760.0, min(chest_girth, 1750.0))
coat_length  = max(600.0, min(coat_length, 1300.0))
neck_girth   = max(320.0, min(neck_girth, 580.0))
sleeve_grown = max(120.0, min(sleeve_grown, 460.0))
sleeve_depth = max(220.0, min(sleeve_depth, 420.0))
cocoon_bow   = max(60.0, min(cocoon_bow, 320.0))
hem_pull     = max(0.0, min(hem_pull, 260.0))
ease         = max(200.0, min(ease, 480.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

L = coat_length
CHEST_HALF = (chest_girth + ease) / 4.0
HIP_HALF = CHEST_HALF + cocoon_bow                   # bows out at the hip
HEM_HALF = HIP_HALF - hem_pull                        # pulls back in at the hem
NECK_SCOOP = max(70.0, neck_girth / 5.0)
SLEEVE_X_BACK = CHEST_HALF + sleeve_grown
SLEEVE_DROP = 300.0
HIP_Y = L - 480.0
FRONT_LAP = 60.0


def _curved_side(top_pt):
    # side seam: from underarm/top down to the bowed hip then in to the pulled hem.
    return [fc.Line(top_pt, fc.P(HIP_HALF, HIP_Y)),
            fc.Line(fc.P(HIP_HALF, HIP_Y), fc.P(HEM_HALF, 0.0))]


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y)
    neck_out = fc.P(NECK_SCOOP, top_y)
    sleeve_top = fc.P(SLEEVE_X_BACK, top_y)
    sleeve_bot = fc.P(SLEEVE_X_BACK, top_y - 110.0)
    body_side_top = fc.P(CHEST_HALF, top_y - SLEEVE_DROP)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=0.12, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
            fc.Edge("side", _curved_side(body_side_top)),
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("sleeve_under", 1.0, "underarm"), fc.Notch("side", 0.5, "hip")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    top_y = L
    cf_x = -FRONT_LAP
    neck_in = fc.P(cf_x, top_y - 40.0)
    neck_out = fc.P(NECK_SCOOP, top_y)
    sleeve_top = fc.P(SLEEVE_X_BACK, top_y)
    sleeve_bot = fc.P(SLEEVE_X_BACK, top_y - 110.0)
    body_side_top = fc.P(CHEST_HALF, top_y - SLEEVE_DROP)
    internals = [fc.Internal("button-line", [fc.P(0.0, 0.0), fc.P(0.0, top_y - 40.0)],
                             kind="marking")]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            fc.Edge("neck", [fc.Line(neck_in, neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
            fc.Edge("side", _curved_side(body_side_top)),
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("sleeve_under", 1.0, "underarm"), fc.Notch("side", 0.5, "hip")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (lap + buttons)",
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_grown
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, 0.0))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(sw, 0.0), fc.P(sw, head_h))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, head_h), fc.P(0.0, head_h))]),
            fc.Edge("cuff", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 0.0, "underarm"), fc.Notch("sleevehead", 1.0, "shoulder")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.2), fc.P(sw * 0.5, head_h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("cocoon-coat")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "soft wool coating or boucle",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 70% marker; a soft cloth drapes the cocoon curve."},
        {"item": "coat buttons or a single wrap tie", "qty": 3, "unit": "pcs",
         "note": "a minimal front closure keeps the cocoon line clean."},
        {"item": "lining", "qty": 1, "unit": "as chosen",
         "note": "a lining helps the curved hem hang; the maker's choice."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set", "note": "seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 190, "family": "outerwear", "fabric_hint": "lana-boucle",
        "silhouette_note": "A rounded coat that bows OUT at the hip and pulls IN at the hem, "
            "wrapping the body like a cocoon, with grown dropped sleeves. Front and back share "
            "the identical curved side seam so it balances by construction.",
        "solved": {"chest_q_mm": round(CHEST_HALF, 1), "hip_half_mm": round(HIP_HALF, 1),
                   "hem_half_mm": round(HEM_HALF, 1)},
    }
    return pattern


result = build()
