"""
Sensory-Friendly Tee — Fashion Cabinet Garment Cartridge (FC-200 rank #153, adaptive/sensory).

A sensory-friendly tee for wearers sensitive to touch: a relaxed boxy front + back with a
tagless printed-label zone, seams marked for flat-fell / covered construction (no raised
inside seam allowances), and a soft wide neck with no binding scratch. A soft-goods
garment — no hardware. Everything that irritates on a conventional tee (tags, ridged
seams, tight neck) is designed out and marked for the maker.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 980.0))
tee_length   = float(PARAM(lambda: tee_length, 640.0))
neck_width   = float(PARAM(lambda: neck_width, 220.0))    # wide, no-scratch neck
sleeve_grown = float(PARAM(lambda: sleeve_grown, 160.0))
ease         = float(PARAM(lambda: ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(600.0, min(chest_girth, 1500.0))
tee_length   = max(400.0, min(tee_length, 900.0))
neck_width   = max(150.0, min(neck_width, 380.0))
sleeve_grown = max(60.0, min(sleeve_grown, 260.0))
ease         = max(40.0, min(ease, 360.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

L = tee_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 220.0


def _panel(name, neck_dip, with_label, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 110.0)
    body_side_top = fc.P(HALF, top_y - SLEEVE_DROP)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
        fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
        fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
        fc.Edge("side", [fc.Line(body_side_top, fc.P(HALF, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if with_label:
        # A printed-label zone at the back neck (tagless — printed, not sewn tag).
        internals.append(fc.Internal("printed-label-zone",
                                     [fc.P(0.0, top_y - neck_dip - 40.0),
                                      fc.P(NECK_HALF * 0.9, top_y - neck_dip - 40.0)],
                                     kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("sensory-tee")
    front = _panel("front", 55.0, False, "Front")
    back = _panel("back", 22.0, True, "Back (tagless label zone)")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "soft combed jersey (low-abrasion)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1600 mm width, 75% marker; softest hand available."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "flat-fell or coverstitch every seam (no raised inside allowance); no tags."},
    ]
    pattern.metadata = {
        "fc200_rank": 153, "family": "knit_tops", "fabric_hint": "jersey-algodon",
        "sensory_note": "Designed for touch-sensitivity: a wide no-scratch neck, a printed "
            "tagless label zone (no sewn tag), and every seam marked for flat-fell / covered "
            "construction so there is no raised inside seam allowance. No hardware. The "
            "irritants of a conventional tee are designed out.",
    }
    return pattern


result = build()
