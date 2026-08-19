"""
Bolero — Fashion Cabinet Garment Cartridge (FC-200 #176, layer gap).

The cropped open bolero (shrug jacket): a very short, open-front jacket that ends above the
waist with curved fronts that meet only at the top (no closure) and set-in-look grown sleeves —
worn over a dress or top for the shoulders and arms. Distinct from FC-100's cardigan (hip-length,
button front) and the outerwear. Front and back share the body width so the shoulder and side
seams balance by construction; the open curved front is the front's inner edge.

Pieces:
  - front / back : short body panels (front cut 2, curved open edge; back on fold), grown sleeves.

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

chest_girth  = float(PARAM(lambda: chest_girth, 960.0))
bolero_length = float(PARAM(lambda: bolero_length, 340.0)) # nape to cropped hem (above waist)
neck_width   = float(PARAM(lambda: neck_width, 200.0))
sleeve_grown = float(PARAM(lambda: sleeve_grown, 260.0))   # grown sleeve length
sleeve_depth = float(PARAM(lambda: sleeve_depth, 150.0))   # grown sleeve height at cuff
front_curve  = float(PARAM(lambda: front_curve, 140.0))    # how deep the open front curves away
ease         = float(PARAM(lambda: ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(660.0, min(chest_girth, 1500.0))
bolero_length = max(220.0, min(bolero_length, 480.0))
neck_width   = max(150.0, min(neck_width, 340.0))
sleeve_grown = max(80.0, min(sleeve_grown, 420.0))
sleeve_depth = max(100.0, min(sleeve_depth, 240.0))
front_curve  = max(60.0, min(front_curve, 260.0))
ease         = max(40.0, min(ease, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

L = bolero_length
HALF = (chest_girth + ease) / 4.0
NECK_HALF = neck_width / 2.0
SLEEVE_X = HALF + sleeve_grown
SLEEVE_DROP = L - 40.0                                # grown-sleeve underarm height


def build_back():
    top_y = L
    neck_pt = fc.P(0.0, top_y - 20.0)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - sleeve_depth)
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
        grainline=fc.Grainline(fc.P(HALF * 0.5, 40.0), fc.P(HALF * 0.5, L - 60.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    # front (cut 2 mirror). Inner edge curves away from CF (the open front) from a small
    # overlap at the shoulder/neck down to the cropped hem, so the fronts meet only at the top.
    top_y = L
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - sleeve_depth)
    body_side_top = fc.P(HALF, top_y - SLEEVE_DROP)
    neck_in = fc.P(0.0, top_y - 40.0)                 # small front neck near CF at the top
    hem_in = fc.P(front_curve, 0.0)                    # hem pulled in by the open-front curve
    return fc.Piece(
        "front",
        [
            fc.Edge("front_edge", [fc.curve_through(neck_in, hem_in, bulge=0.30, side=1.0)]),
            fc.Edge("hem", [fc.Line(hem_in, fc.P(HALF, 0.0))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, 0.0), body_side_top)]),
            fc.Edge("sleeve_under", [fc.Line(body_side_top, sleeve_bot)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_bot, sleeve_top)]),
            fc.Edge("shoulder", [fc.Line(sleeve_top, neck_out)]),
            fc.Edge("neck", [fc.Line(neck_out, neck_in)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 1.0, "neck"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.6, 40.0), fc.P(HALF * 0.6, L - 60.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (open curve)",
    )


def build():
    pattern = fc.PatternSet("bolero")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "ponte, boiled wool, or soft woven",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 72% marker; a fabric with body holds the open front."},
        {"item": "bias binding for all edges", "qty": 1, "unit": "as needed",
         "note": "the open front, neck, and hem are bound as one continuous edge; no closure."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + binding."},
    ]
    pattern.metadata = {
        "fc200_rank": 176, "family": "knitwear", "fabric_hint": "ponte-lana",
        "silhouette_note": "A very short open-front bolero ending above the waist, with curved "
            "fronts that meet only at the top (no closure) and grown sleeves. The open curved "
            "front is the front's inner edge; shoulder/side/underarm seams balance.",
        "solved": {"body_q_mm": round(HALF, 1), "front_curve_mm": round(front_curve, 1)},
    }
    return pattern


result = build()
