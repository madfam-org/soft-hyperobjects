"""
Nursing Top — Fashion Cabinet Garment Cartridge (FC-200 rank #151, maternity/nursing).

A relaxed nursing top with a double-layer front: an outer front with a lift-access opening
and an inner modesty layer with the nursing slit, so a parent can feed discreetly without
undressing. A soft-goods garment — no hardware; the access is a sewn overlap, marked here.

Pieces:
  - front_outer : the outer front (cut on fold), with a marked lift-access line.
  - front_inner : the inner modesty layer (cut on fold), with a marked nursing slit.
  - back        : the back (cut on fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front_outer|front_inner|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 1000.0))
top_length   = float(PARAM(lambda: top_length, 660.0))
neck_width   = float(PARAM(lambda: neck_width, 190.0))
sleeve_grown = float(PARAM(lambda: sleeve_grown, 150.0))
ease         = float(PARAM(lambda: ease, 120.0))
access_drop  = float(PARAM(lambda: access_drop, 240.0))   # how far the lift access extends
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(700.0, min(chest_girth, 1500.0))
top_length   = max(450.0, min(top_length, 950.0))
neck_width   = max(140.0, min(neck_width, 340.0))
sleeve_grown = max(60.0, min(sleeve_grown, 260.0))
ease         = max(60.0, min(ease, 360.0))
access_drop  = max(120.0, min(access_drop, top_length * 0.6))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 220.0


def _panel(name, neck_dip, marks, label, on_fold=True):
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
    internals = list(marks)
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=on_fold, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("nursing-top")
    # Outer front: a lift-access line (the outer layer lifts from the hem to feed).
    outer_marks = [fc.Internal("lift-access",
                               [fc.P(0.0, L - access_drop), fc.P(HALF, L - access_drop)],
                               kind="marking")]
    # Inner front: a vertical nursing slit near CF.
    inner_marks = [fc.Internal("nursing-slit",
                              [fc.P(HALF * 0.25, L - 40.0), fc.P(HALF * 0.25, L - access_drop)],
                              kind="drill")]
    outer = _panel("front_outer", 55.0, outer_marks, "Front Outer (lift access)")
    inner = _panel("front_inner", 90.0, inner_marks, "Front Inner (nursing slit)")
    back = _panel("back", 25.0, [], "Back")

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front_outer":
        pattern.add(outer)
    if all_pieces or target_piece == "front_inner":
        pattern.add(inner)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces:
        pattern.declare_seam(("front_outer", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front_outer", "side"), ("back", "side"), tol=1.0)
    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "soft jersey (double-layer front)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1600 mm width, 72% marker; the front is two layers."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "finish the nursing slit + lift-access edges; no hardware."},
    ]
    pattern.metadata = {
        "fc200_rank": 151, "family": "knit_tops", "fabric_hint": "jersey-algodon",
        "nursing_note": "A double-layer front: the outer layer lifts from the hem (marked "
            "lift-access line) over an inner modesty layer with a nursing slit (marked), so "
            "a parent can feed discreetly without undressing. Sewn overlap access, no hardware.",
    }
    return pattern


result = build()
