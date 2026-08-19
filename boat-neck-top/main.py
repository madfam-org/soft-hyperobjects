"""
Boat-Neck Top — Fashion Cabinet Garment Cartridge (FC-200 #185, neckline gap).

The boat-neck (bateau) top: a wide, shallow neckline running straight across from shoulder
point to shoulder point, high at centre, with a slightly dropped shoulder and often a three-
quarter sleeve — the Breton/ballet line. This cartridge drafts a clean front + back with the
distinctive wide shallow bateau neck (front and back nearly identical), plus a set sleeve.
Distinct from FC-100's crew and scoop tees. Front and back share the body width so the shoulder
and side seams balance by construction.

Pieces:
  - front / back : body panels (cut on fold) with a wide shallow boat neck.
  - sleeve       : three-quarter set sleeve (cut 2 mirror).

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

chest_girth  = float(PARAM(lambda: chest_girth, 940.0))
top_length   = float(PARAM(lambda: top_length, 600.0))
boat_width   = float(PARAM(lambda: boat_width, 320.0))     # wide neck (shoulder to shoulder)
boat_dip     = float(PARAM(lambda: boat_dip, 40.0))        # shallow front dip
sleeve_len   = float(PARAM(lambda: sleeve_len, 340.0))     # three-quarter
sleeve_depth = float(PARAM(lambda: sleeve_depth, 210.0))
ease         = float(PARAM(lambda: ease, 110.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(640.0, min(chest_girth, 1500.0))
top_length   = max(400.0, min(top_length, 850.0))
boat_width   = max(220.0, min(boat_width, 460.0))
boat_dip     = max(15.0, min(boat_dip, 120.0))
sleeve_len   = max(120.0, min(sleeve_len, 620.0))
sleeve_depth = max(160.0, min(sleeve_depth, 360.0))
ease         = max(40.0, min(ease, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
BOAT_HALF = boat_width / 2.0                          # half the wide neck opening


def _panel(name, dip, label):
    top_y = L
    neck_in = fc.P(0.0, top_y - dip)
    neck_out = fc.P(BOAT_HALF, top_y)                 # wide shoulder-neck point
    shoulder_end = fc.P(HALF, top_y - 6.0)            # slightly dropped shoulder
    armhole_bot = fc.P(HALF, top_y - sleeve_depth)
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_in)]),
            fc.Edge("neck", [fc.curve_through(neck_in, neck_out,
                                              bulge=dip / max(BOAT_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_end, armhole_bot,
                                                 bulge=0.14, side=-1.0)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_len
    opening = HALF * 0.62
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - opening) / 2.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(sw, (head_h - opening) / 2.0),
                                     fc.P(sw, (head_h + opening) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + opening) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (3/4)",
    )


def build():
    pattern = fc.PatternSet("boat-neck-top")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_panel("front", boat_dip, "Front"))
    if everything or target_piece == "back":
        pattern.add(_panel("back", boat_dip * 0.6, "Back"))
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "cotton jersey or interlock (Breton stripe optional)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 75% marker; a stable knit holds the wide neck flat."},
        {"item": "neck + cuff binding", "qty": 1, "unit": "set",
         "note": "a narrow band or fold-over finishes the boat neck and cuffs."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool", "note": "knit seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 185, "family": "knit_tops", "fabric_hint": "jersey-interlock",
        "silhouette_note": "A wide, shallow bateau neckline running straight across from shoulder "
            "to shoulder (Breton/ballet line), slightly dropped shoulder, three-quarter sleeve. "
            "Front and back are near-identical; shoulder and side seams balance.",
        "solved": {"body_half_mm": round(HALF, 1), "boat_width_mm": round(boat_width, 1)},
    }
    return pattern


result = build()
