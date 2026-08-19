"""
Tabard — Fashion Cabinet Garment Cartridge (FC-200 #171, workwear/over-garment gap).

The tabard: a simple over-garment of a front and a back panel joined at the shoulders, open
down both sides and belted or side-tied — the medieval and modern workwear/heraldic over-layer,
and the shape of a market/warehouse over-apron. Distinct from FC-100's hi-vis vest (bias-bound
minimal safety tabard) and bib-apron: the tabard covers front AND back, joins only at the
shoulders, and ties at the sides. Only the shoulder seam is sewn, so it balances by construction;
the open sides are marked with side-tie positions.

Pieces:
  - front / back : rectangular panels with a neck scoop, joined at the shoulder, open sides.

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

panel_width  = float(PARAM(lambda: panel_width, 460.0))    # panel width (flat, on fold → half)
tabard_length = float(PARAM(lambda: tabard_length, 900.0)) # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 240.0))     # pull-over neck width
shoulder_w   = float(PARAM(lambda: shoulder_w, 110.0))     # shoulder seam width
front_neck_dip = float(PARAM(lambda: front_neck_dip, 90.0))
back_neck_dip  = float(PARAM(lambda: back_neck_dip, 30.0))
side_ties    = int(  PARAM(lambda: side_ties, 2))          # tie pairs down each open side
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
panel_width  = max(300.0, min(panel_width, 700.0))
tabard_length = max(500.0, min(tabard_length, 1300.0))
neck_width   = max(180.0, min(neck_width, 380.0))
shoulder_w   = max(60.0, min(shoulder_w, 200.0))
front_neck_dip = max(40.0, min(front_neck_dip, 200.0))
back_neck_dip  = max(10.0, min(back_neck_dip, 120.0))
side_ties    = max(1, min(side_ties, 5))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

HALF = panel_width / 2.0
NECK_HALF = neck_width / 2.0
SHOULDER_X = NECK_HALF + shoulder_w
L = tabard_length


def _panel(name, neck_dip, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    shoulder_in = fc.P(NECK_HALF, top_y)
    shoulder_out = fc.P(SHOULDER_X, top_y)
    internals = []
    # side-tie positions down the open side (both sides mirrored on fold)
    for i in range(side_ties):
        t = (i + 1) / (side_ties + 1)
        y = L * (0.30 + 0.5 * t)
        internals.append(fc.Internal(f"side-tie-{i}",
                                     [fc.P(HALF, y), fc.P(HALF - 40.0, y)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, shoulder_in,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_out)]),
            fc.Edge("armhole_edge", [fc.Line(shoulder_out, fc.P(HALF, top_y - 40.0))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, top_y - 40.0), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "side": hem_allowance, "armhole_edge": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("shoulder", 1.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 80.0), fc.P(HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("tabard")
    everything = target_piece == "set"
    front = _panel("front", front_neck_dip, "Front panel")
    back = _panel("back", back_neck_dip, "Back panel")
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        # only the shoulders are sewn; the sides are open and tied
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "canvas, felt, or heavy cotton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 78% marker; two simple panels, open sides."},
        {"item": "side ties or a belt", "qty": side_ties * 2, "unit": "ties",
         "note": "self-fabric ties join the open sides; a belt is an alternative."},
        {"item": "neck + edge binding", "qty": 1, "unit": "as needed",
         "note": "all raw edges are bound or hemmed; the shoulders are the only seam."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "shoulder seam + binding."},
    ]
    pattern.metadata = {
        "fc200_rank": 171, "family": "workwear_uniforms", "fabric_hint": "lona-fieltro",
        "silhouette_note": "A front and a back panel joined only at the shoulders, open down "
            "both sides and side-tied or belted — the workwear/heraldic over-layer and market "
            "over-apron shape. Only the shoulder seam is sewn, so it balances by construction.",
        "solved": {"panel_half_mm": round(HALF, 1), "side_tie_pairs": side_ties,
                   "length_mm": round(L, 1)},
    }
    return pattern


result = build()
