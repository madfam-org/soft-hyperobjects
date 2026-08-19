"""
Wrap Top — Fashion Cabinet Garment Cartridge (FC-200 #165, everyday silhouette gap).

A surplice wrap top: two front panels cross over each other in a deep V and tie at the side
seam (one tie through an inseam opening, one outside), over a plain back. This is the top-length
counterpart to the wrap-dress. Each front panel is wide enough to cross past centre front; the
back and front share the structural side width so the shoulder and side seams balance by
construction. The crossover and the deep-V neckline are the shaping; ties are self-fabric strips.

Pieces:
  - front  : one wrap front panel, cut 2 mirror (they cross at CF).
  - back   : plain back panel (cut on fold).
  - sleeve : short grown/set sleeve rectangle, cut 2 mirror.

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

bust_girth   = float(PARAM(lambda: bust_girth, 940.0))     # full bust
top_length   = float(PARAM(lambda: top_length, 600.0))     # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 170.0))     # base neck width (shoulder)
wrap_deep    = float(PARAM(lambda: wrap_deep, 300.0))      # depth of the V (from shoulder down)
sleeve_len   = float(PARAM(lambda: sleeve_len, 220.0))     # sleeve length
sleeve_depth = float(PARAM(lambda: sleeve_depth, 200.0))   # armhole drop
ease         = float(PARAM(lambda: ease, 110.0))           # semi-fitted ease
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(650.0, min(bust_girth, 1500.0))
top_length   = max(400.0, min(top_length, 880.0))
neck_width   = max(130.0, min(neck_width, 300.0))
wrap_deep    = max(160.0, min(wrap_deep, 460.0))
sleeve_len   = max(80.0, min(sleeve_len, 420.0))
sleeve_depth = max(150.0, min(sleeve_depth, 360.0))
ease         = max(40.0, min(ease, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (bust_girth + ease) / 2.0 / 2.0     # quarter body width (side seam at x=HALF)
NECK_HALF = neck_width / 2.0
# Each front panel extends PAST centre front by a crossover so the two fronts overlap.
CROSSOVER = HALF * 0.65


def build_back():
    top_y = L
    neck_pt = fc.P(0.0, top_y - 22.0)
    neck_out = fc.P(NECK_HALF, top_y)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out, bulge=0.16, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(HALF, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(HALF, top_y), fc.P(HALF, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, top_y - sleeve_depth), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 0.0, "underarm"), fc.Notch("shoulder", 0.0, "neck")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    # A wrap front (cut 2 mirror). The inner edge runs from the hem up in a deep diagonal V
    # to the shoulder-neck point; the panel extends to x = CROSSOVER past CF at the hem so the
    # two fronts overlap. The shoulder + side edges match the back so both seams balance.
    top_y = L
    neck_out = fc.P(NECK_HALF, top_y)
    hem_inner = fc.P(-CROSSOVER, 0.0)                 # crosses past CF at the hem
    wrap_v_top = fc.P(NECK_HALF, top_y - 8.0)         # V begins just below the shoulder-neck
    internals = [fc.Internal("wrap-cross", [fc.P(0.0, 0.0), fc.P(0.0, top_y - wrap_deep)],
                             kind="marking")]
    return fc.Piece(
        "front",
        [
            # inner wrap edge: hem_inner -> up the deep V -> shoulder-neck point
            fc.Edge("wrap_edge", [fc.Line(hem_inner, fc.P(0.0, top_y - wrap_deep)),
                                  fc.Line(fc.P(0.0, top_y - wrap_deep), wrap_v_top)]),
            fc.Edge("neck", [fc.Line(wrap_v_top, neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(HALF, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(HALF, top_y), fc.P(HALF, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, top_y - sleeve_depth), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), hem_inner)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 0.0, "underarm"), fc.Notch("side", 1.0, "tie")],
        grainline=fc.Grainline(fc.P(HALF * 0.4, 60.0), fc.P(HALF * 0.4, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wrap front",
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_len
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, 0.0))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(sw, 0.0), fc.P(sw, head_h))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, head_h), fc.P(0.0, head_h))]),
            fc.Edge("opening", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 0.0, "underarm"), fc.Notch("sleevehead", 1.0, "shoulder")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.2), fc.P(sw * 0.5, head_h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("wrap-top")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "soft drapey woven or knit (jersey / crepe)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 72% marker; drape helps the wrap sit flat."},
        {"item": "self-fabric ties", "qty": 2, "unit": "strips",
         "note": "one inseam tie through the side seam, one outside; length is the maker's."},
        {"item": "neckband / binding", "qty": 1, "unit": "strip",
         "note": "binds the wrap and neck edges into a clean finish."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + binding."},
    ]
    pattern.metadata = {
        "fc200_rank": 165, "family": "woven_tops", "fabric_hint": "crepe-jersey",
        "silhouette_note": "Two front panels cross in a deep V and tie at the side (the "
            "top-length wrap-dress counterpart). Each front extends past CF by a crossover so "
            "they overlap; shoulder + side edges match the back, so both seams balance.",
        "solved": {"body_quarter_mm": round(HALF, 1), "crossover_mm": round(CROSSOVER, 1),
                   "wrap_depth_mm": round(wrap_deep, 1)},
    }
    return pattern


result = build()
