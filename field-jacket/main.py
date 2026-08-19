"""
Field Jacket — Fashion Cabinet Garment Cartridge (FC-200 #169, workwear gap).

The M-65-style utility field jacket: a boxy, hip-length jacket with a set-in collar stand, a
zip-and-snap centre-front placket, and FOUR bellows patch pockets (two chest, two lower). Cut
straight and roomy to layer over. Distinct from FC-100's bomber (ribbed hem/cuff, no pockets),
chore coat (single button stand, no bellows), and denim jacket. The four bellows pockets and
the drawcord waist are the field jacket's signature, marked for the maker.

Pieces:
  - front / back : boxy body panels (front cut 2 for the placket; back on fold), pockets marked.
  - sleeve       : straight two-panel-look sleeve as one rectangle (cut 2 mirror).
  - pocket       : one bellows patch pocket (cut 4).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|pocket|set

chest_girth  = float(PARAM(lambda: chest_girth, 1100.0))   # full chest
jacket_length = float(PARAM(lambda: jacket_length, 720.0)) # nape to hem
neck_girth   = float(PARAM(lambda: neck_girth, 440.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 280.0))  # armhole drop
ease         = float(PARAM(lambda: ease, 300.0))           # roomy layering ease
pocket_w     = float(PARAM(lambda: pocket_w, 190.0))       # bellows pocket width
pocket_h     = float(PARAM(lambda: pocket_h, 210.0))       # bellows pocket height
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 28.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(760.0, min(chest_girth, 1750.0))
jacket_length = max(560.0, min(jacket_length, 950.0))
neck_girth   = max(320.0, min(neck_girth, 580.0))
sleeve_length = max(400.0, min(sleeve_length, 720.0))
sleeve_depth  = max(200.0, min(sleeve_depth, 400.0))
ease         = max(160.0, min(ease, 460.0))
pocket_w     = max(130.0, min(pocket_w, 260.0))
pocket_h     = max(140.0, min(pocket_h, 300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = jacket_length
BODY = chest_girth + ease
BW = BODY / 4.0                                  # quarter (back on fold half, front half)
NECK_SCOOP = max(70.0, neck_girth / 5.0)
FRONT_EXT = 35.0                                 # placket extension past CF


def _pockets(is_front, half_w):
    if not is_front:
        return []
    out = []
    cx = half_w * 0.5
    # chest pocket (upper) + lower pocket, both marked as bellows patch outlines
    for cy, tag in ((L - 260.0, "chest"), (L - 540.0, "lower")):
        out.append(fc.Internal(f"{tag}-pocket",
                               [fc.P(cx - pocket_w / 2.0, cy), fc.P(cx + pocket_w / 2.0, cy),
                                fc.P(cx + pocket_w / 2.0, cy - pocket_h),
                                fc.P(cx - pocket_w / 2.0, cy - pocket_h),
                                fc.P(cx - pocket_w / 2.0, cy)], kind="marking"))
    return out


def build_front():
    top_y = L
    cf_x = -FRONT_EXT
    neck_out = fc.P(NECK_SCOOP, top_y)
    internals = [fc.Internal("cf-placket", [fc.P(0.0, 0.0), fc.P(0.0, top_y)], kind="fold")]
    internals += _pockets(True, BW)
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), fc.P(cf_x, top_y))]),
            fc.Edge("neck", [fc.Line(fc.P(cf_x, top_y), neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, top_y), fc.P(BW, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, top_y - sleeve_depth), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (placket + pockets)",
    )


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y)
    neck_out = fc.P(NECK_SCOOP, top_y)
    internals = [fc.Internal("waist-drawcord", [fc.P(0.0, L * 0.5), fc.P(BW, L * 0.5)],
                             kind="marking")]
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=0.12, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, top_y), fc.P(BW, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, top_y - sleeve_depth), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_length
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


def build_pocket():
    w, h = pocket_w, pocket_h
    flap = 55.0
    return fc.Piece(
        "pocket",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(w, h + flap)),
                            fc.Line(fc.P(w, h + flap), fc.P(0.0, h + flap))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, h + flap), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"bottom": 8.0},
        notches=[fc.Notch("side_r", 0.0, "bellows fold")],
        grainline=fc.Grainline(fc.P(w * 0.5, 15.0), fc.P(w * 0.5, h - 15.0)),
        internals=[fc.Internal("flap-fold", [fc.P(0.0, h), fc.P(w, h)], kind="fold")],
        cut=fc.CutSpec(quantity=4),
        label="Bellows pocket",
    )


def build():
    pattern = fc.PatternSet("field-jacket")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton sateen / NyCo ripstop",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; body + 2 sleeves + 4 bellows pockets."},
        {"item": "front zipper + snaps", "qty": 1, "unit": "set",
         "note": "zip under a snap storm flap at CF; hardware is the maker's choice."},
        {"item": "waist + hem drawcord", "qty": 1, "unit": "set",
         "note": "internal drawcords at the waist and hem cinch the boxy body."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "topstitch the bellows pockets and placket."},
    ]
    pattern.metadata = {
        "fc200_rank": 169, "family": "workwear_uniforms", "fabric_hint": "sateen-algodon",
        "silhouette_note": "A boxy, hip-length M-65-style field jacket: zip-and-snap CF placket, "
            "four bellows patch pockets (two chest, two lower), grown-roomy fit, and waist/hem "
            "drawcords. Straight side/armhole seams balance by construction.",
        "solved": {"body_quarter_mm": round(BW, 1), "pocket_mm": [pocket_w, pocket_h]},
    }
    return pattern


result = build()
