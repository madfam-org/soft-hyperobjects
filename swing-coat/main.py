"""
Swing Coat — Fashion Cabinet Garment Cartridge (FC-200 #189, outerwear gap).

The swing coat: a coat that flares dramatically from a fitted shoulder to a wide swinging hem
(A-line/trapeze line), with a set sleeve and often a small collar — the 1950s swing silhouette.
Distinct from FC-100's straight overcoat/trench/parka. The flare is built into the side seam
(both front and back release to the same wide hem, so the side seam balances by construction);
the front laps for a button closure.

Pieces:
  - front / back : flared body panels (front cut 2 with lap; back on fold), releasing to a wide hem.
  - sleeve       : set sleeve (cut 2 mirror).
  - collar       : a small stand-fall collar strip.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|collar|set

chest_girth  = float(PARAM(lambda: chest_girth, 1040.0))
coat_length  = float(PARAM(lambda: coat_length, 900.0))
neck_girth   = float(PARAM(lambda: neck_girth, 440.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 280.0))
swing_flare  = float(PARAM(lambda: swing_flare, 340.0))    # extra hem width per side (the swing)
ease         = float(PARAM(lambda: ease, 260.0))           # coat ease over layers
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 45.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(760.0, min(chest_girth, 1750.0))
coat_length  = max(600.0, min(coat_length, 1300.0))
neck_girth   = max(320.0, min(neck_girth, 580.0))
sleeve_length = max(400.0, min(sleeve_length, 720.0))
sleeve_depth  = max(200.0, min(sleeve_depth, 400.0))
swing_flare  = max(120.0, min(swing_flare, 560.0))
ease         = max(160.0, min(ease, 420.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

L = coat_length
CHEST_HALF = (chest_girth + ease) / 4.0
HEM_HALF = CHEST_HALF + swing_flare                  # wide swinging hem
NECK_SCOOP = max(70.0, neck_girth / 5.0)
FRONT_LAP = 55.0


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y)
    neck_out = fc.P(NECK_SCOOP, top_y)
    armhole_bot = fc.P(CHEST_HALF, top_y - sleeve_depth)
    # side seam flares straight out from the armhole to the wide hem
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=0.12, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(CHEST_HALF, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(CHEST_HALF, top_y), armhole_bot)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(HEM_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    top_y = L
    cf_x = -FRONT_LAP
    neck_in = fc.P(cf_x, top_y - 40.0)
    neck_out = fc.P(NECK_SCOOP, top_y)
    armhole_bot = fc.P(CHEST_HALF, top_y - sleeve_depth)
    internals = [fc.Internal("button-line", [fc.P(0.0, 0.0), fc.P(0.0, top_y - 40.0)],
                             kind="marking")]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            fc.Edge("neck", [fc.Line(neck_in, neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(CHEST_HALF, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(CHEST_HALF, top_y), armhole_bot)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(HEM_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (lap + buttons)",
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_length
    cuff = CHEST_HALF * 0.7
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - cuff) / 2.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(sw, (head_h - cuff) / 2.0),
                                     fc.P(sw, (head_h + cuff) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + cuff) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_collar():
    ln = neck_girth + 40.0
    h = 150.0
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("outer", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        internals=[fc.Internal("roll-line", [fc.P(0.0, h * 0.45), fc.P(ln, h * 0.45)],
                               kind="fold")],
        cut=fc.CutSpec(quantity=1),
        label="Collar",
    )


def build():
    pattern = fc.PatternSet("swing-coat")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "collar":
        pattern.add(build_collar())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "wool melton or boiled wool coating",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 68% marker; the flared hem uses a lot of cloth."},
        {"item": "coat buttons", "qty": 4, "unit": "pcs", "note": "single-breasted front lap."},
        {"item": "lining", "qty": 1, "unit": "as chosen", "note": "a full lining is recommended."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "seams + collar."},
    ]
    pattern.metadata = {
        "fc200_rank": 189, "family": "outerwear", "fabric_hint": "melton-lana",
        "silhouette_note": "A coat that flares from a fitted shoulder to a wide swinging hem "
            "(1950s A-line/trapeze). The flare is in the side seam — front and back release to "
            "the same wide hem so the side balances; the front laps for buttons.",
        "solved": {"chest_q_mm": round(CHEST_HALF, 1), "hem_half_mm": round(HEM_HALF, 1),
                   "swing_flare_mm": round(swing_flare, 1)},
    }
    return pattern


result = build()
