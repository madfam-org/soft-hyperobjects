"""
Cowl-Neck Top — Fashion Cabinet Garment Cartridge (FC-200 #161, everyday silhouette gap).

A relaxed knit/soft-woven top whose front neckline extends UP into a self-draping cowl: the
front panel's top edge is widened and raised past the shoulder line so that, folded back on
itself, it falls into soft folds at the neck. Back + front share the structural body width so
the shoulder and side seams balance by construction; the cowl is the front's extended, folded
self-facing (a marked fold line), needing no separate collar.

Pieces:
  - front : body panel with the raised, widened cowl extension + fold line (cut on fold).
  - back  : plain body panel with a shallow neck (cut on fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 980.0))    # full chest
top_length   = float(PARAM(lambda: top_length, 620.0))     # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 220.0))     # base neck opening
cowl_drop    = float(PARAM(lambda: cowl_drop, 150.0))      # how deep the cowl folds
cowl_rise    = float(PARAM(lambda: cowl_rise, 90.0))       # extra height above the shoulder
sleeve_grown = float(PARAM(lambda: sleeve_grown, 150.0))   # grown cap sleeve
ease         = float(PARAM(lambda: ease, 120.0))           # soft ease
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(650.0, min(chest_girth, 1500.0))
top_length   = max(420.0, min(top_length, 900.0))
neck_width   = max(160.0, min(neck_width, 380.0))
cowl_drop    = max(60.0, min(cowl_drop, 300.0))
cowl_rise    = max(30.0, min(cowl_rise, 200.0))
sleeve_grown = max(60.0, min(sleeve_grown, 260.0))
ease         = max(40.0, min(ease, 360.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 220.0


def build_back():
    top_y = L
    neck_pt = fc.P(0.0, top_y - 22.0)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 100.0)
    body_side_top = fc.P(HALF, top_y - SLEEVE_DROP)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out, bulge=0.18, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
            fc.Edge("side", [fc.Line(body_side_top, fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    # The front shoulder matches the back shoulder EXACTLY (same neck_out -> sleeve_top),
    # so the shoulder seam balances. The cowl is an extra self-facing ABOVE the shoulder line
    # that folds down — modelled as a raised centre with a fold line, not a change to the
    # shoulder seam. The neckline between CF and the shoulder point rises to cowl_rise.
    top_y = L
    cowl_top = fc.P(0.0, top_y + cowl_rise)             # raised CF for the cowl facing
    neck_out = fc.P(NECK_HALF, top_y)                    # shoulder-neck point (matches back)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 100.0)
    body_side_top = fc.P(HALF, top_y - SLEEVE_DROP)
    internals = [
        fc.Internal("cowl-fold", [fc.P(0.0, top_y), fc.P(NECK_HALF, top_y)], kind="fold"),
        fc.Internal("cowl-depth", [fc.P(0.0, top_y - cowl_drop),
                                   fc.P(NECK_HALF * 0.7, top_y - cowl_drop)], kind="marking"),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), cowl_top)]),
            # cowl neckline sweeps from the raised CF down to the shoulder-neck point
            fc.Edge("neck", [fc.curve_through(cowl_top, neck_out, bulge=0.22, side=1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
            fc.Edge("side", [fc.Line(body_side_top, fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (cowl)",
    )


def build():
    pattern = fc.PatternSet("cowl-neck-top")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "drapey knit or soft rayon woven",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 75% marker; a fluid hand makes the cowl fold softly."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "the cowl is the front's folded self-facing — no separate collar."},
    ]
    pattern.metadata = {
        "fc200_rank": 161, "family": "knit_tops", "fabric_hint": "punto-rayon",
        "silhouette_note": "The front neckline rises above the shoulder into a self-facing "
            "that folds back into a soft cowl; the shoulder seam still matches the back exactly, "
            "so it balances by construction. Cut in a fluid fabric for the drape.",
        "solved": {"cowl_rise_mm": round(cowl_rise, 1), "cowl_drop_mm": round(cowl_drop, 1),
                   "neck_width_mm": round(neck_width, 1)},
    }
    return pattern


result = build()
