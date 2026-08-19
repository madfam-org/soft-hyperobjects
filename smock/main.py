"""
Smock — Fashion Cabinet Garment Cartridge (FC-200 #168, workwear gap).

The pull-over craft/artist smock: a loose protective over-garment with a shoulder yoke, a
gathered body hanging from the yoke for room to move, a wide neck to pull over the head, grown
dropped sleeves, and a big divided front kangaroo pocket for tools and brushes. Distinct from
FC-100's buttoned coats (chore/lab/chef): the smock pulls over, is gathered, and closes with
nothing (or a short back neck tie). A body panel gathered to a yoke — the gather is the ease.

Pieces:
  - yoke  : shoulder yoke (front+back cut on fold), the body gathers to its lower edge.
  - body  : gathered lower body (front+back on fold), grown sleeves, big front pocket marked.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # yoke|body|set

chest_girth  = float(PARAM(lambda: chest_girth, 1080.0))   # full chest
smock_length = float(PARAM(lambda: smock_length, 760.0))   # nape to hem
yoke_depth   = float(PARAM(lambda: yoke_depth, 150.0))     # yoke height at CB
neck_width   = float(PARAM(lambda: neck_width, 240.0))     # wide pull-over neck
sleeve_grown = float(PARAM(lambda: sleeve_grown, 220.0))   # grown dropped sleeve
body_gather  = float(PARAM(lambda: body_gather, 1.6))      # body width / yoke width
ease         = float(PARAM(lambda: ease, 200.0))           # roomy ease
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(720.0, min(chest_girth, 1700.0))
smock_length = max(500.0, min(smock_length, 1000.0))
yoke_depth   = max(90.0, min(yoke_depth, 260.0))
neck_width   = max(180.0, min(neck_width, 380.0))
sleeve_grown = max(80.0, min(sleeve_grown, 340.0))
body_gather  = max(1.2, min(body_gather, 2.4))
ease         = max(100.0, min(ease, 400.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

YOKE_HALF = (chest_girth + ease) / 2.0 / 2.0        # yoke half-width (fold at CB)
BODY_HALF = YOKE_HALF * body_gather                  # gathered body half-width
NECK_HALF = neck_width / 2.0
SLEEVE_X = YOKE_HALF + sleeve_grown
BODY_L = smock_length - yoke_depth                   # body hangs below the yoke


def build_yoke(name, neck_dip, label):
    top_y = yoke_depth
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 80.0)
    yoke_side = fc.P(YOKE_HALF, 0.0)
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, yoke_side)]),
            fc.Edge("yoke_seam", [fc.Line(yoke_side, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("yoke_seam", 0.0, "side")],
        grainline=fc.Grainline(fc.P(YOKE_HALF * 0.5, 15.0), fc.P(YOKE_HALF * 0.5, top_y - 15.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_body(name, is_front, label):
    L = BODY_L
    internals = [fc.Internal("yoke-gather", [fc.P(0.0, L), fc.P(BODY_HALF, L)], kind="marking")]
    if is_front:
        # big divided kangaroo pocket across the lower front
        py = L * 0.34
        internals.append(fc.Internal("front-pocket",
                                     [fc.P(20.0, py), fc.P(BODY_HALF * 0.82, py),
                                      fc.P(BODY_HALF * 0.82, py + 230.0), fc.P(20.0, py + 230.0),
                                      fc.P(20.0, py)], kind="marking"))
        dx = BODY_HALF * 0.42
        internals.append(fc.Internal("pocket-divide",
                                     [fc.P(dx, py), fc.P(dx, py + 230.0)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("yoke_seam", [fc.Line(fc.P(0.0, L), fc.P(BODY_HALF, L))]),
            fc.Edge("side", [fc.Line(fc.P(BODY_HALF, L), fc.P(BODY_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BODY_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("yoke_seam", 0.5, "gather"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(BODY_HALF * 0.5, 80.0), fc.P(BODY_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("smock")
    everything = target_piece == "set"
    yoke_f = build_yoke("yoke_front", 55.0, "Yoke Front")
    yoke_b = build_yoke("yoke_back", 22.0, "Yoke Back")
    body_f = build_body("body_front", True, "Body Front (pocket)")
    body_b = build_body("body_back", False, "Body Back")
    if everything or target_piece == "yoke":
        pattern.add(yoke_f)
        pattern.add(yoke_b)
    if everything or target_piece == "body":
        pattern.add(body_f)
        pattern.add(body_b)
    if everything:
        pattern.declare_seam(("yoke_front", "shoulder"), ("yoke_back", "shoulder"), tol=1.0)
        pattern.declare_seam(("yoke_front", "sleeve_under"), ("yoke_back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("body_front", "side"), ("body_back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "cotton drill / canvas / oilcloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; a protective, wipeable smock cloth."},
        {"item": "neck binding + short back tie", "qty": 1, "unit": "set",
         "note": "the wide neck is bound; an optional short CB tie snugs it."},
        {"item": "all-purpose + topstitch thread", "qty": 1, "unit": "set",
         "note": "gather the body to the yoke; topstitch the big front pocket."},
    ]
    pattern.metadata = {
        "fc200_rank": 168, "family": "workwear_uniforms", "fabric_hint": "lona-algodon",
        "silhouette_note": "A pull-over craft smock: a shoulder yoke with a gathered body "
            "hanging from it for room, a wide pull-over neck, grown dropped sleeves, and a big "
            "divided front kangaroo pocket. The gather is the ease; nothing to button.",
        "solved": {"yoke_half_mm": round(YOKE_HALF, 1), "body_half_mm": round(BODY_HALF, 1),
                   "body_gather": body_gather},
    }
    return pattern


result = build()
