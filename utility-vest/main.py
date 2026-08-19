"""
Utility Vest — Fashion Cabinet Garment Cartridge (FC-200 #170, workwear gap).

The multi-pocket work/field vest: a sleeveless zip-front vest covered in tool and cargo
pockets — chest pockets, big lower bellows pockets, and a pen/tool row — for trades, field
work, photography, and fishing. Distinct from FC-100's puffer-vest (insulated, sleeveless
puffer), hi-vis vest (bias-bound tabard), and waistcoat (tailored, cinch-back): the utility
vest is a working carrier of pockets. Front + back share the body width so the shoulder and
side seams balance by construction.

Pieces:
  - front / back : vest body panels (front cut 2 for the zip; back on fold), pockets marked.
  - pocket       : one lower bellows cargo pocket (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|pocket|set

chest_girth  = float(PARAM(lambda: chest_girth, 1060.0))   # full chest
vest_length  = float(PARAM(lambda: vest_length, 640.0))    # nape to hem
neck_width   = float(PARAM(lambda: neck_width, 200.0))     # collar-stand neck
shoulder_w   = float(PARAM(lambda: shoulder_w, 120.0))     # shoulder strap width
armhole_drop = float(PARAM(lambda: armhole_drop, 300.0))   # deep vest armhole
ease         = float(PARAM(lambda: ease, 220.0))           # layering ease
pocket_w     = float(PARAM(lambda: pocket_w, 180.0))       # lower cargo pocket width
pocket_h     = float(PARAM(lambda: pocket_h, 200.0))       # lower cargo pocket height
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(720.0, min(chest_girth, 1700.0))
vest_length  = max(480.0, min(vest_length, 860.0))
neck_width   = max(160.0, min(neck_width, 360.0))
shoulder_w   = max(70.0, min(shoulder_w, 200.0))
armhole_drop = max(220.0, min(armhole_drop, 420.0))
ease         = max(120.0, min(ease, 380.0))
pocket_w     = max(120.0, min(pocket_w, 260.0))
pocket_h     = max(130.0, min(pocket_h, 300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = vest_length
BODY = chest_girth + ease
BW = BODY / 4.0
NECK_HALF = neck_width / 2.0
SHOULDER_X = NECK_HALF + shoulder_w
FRONT_EXT = 30.0


def build_front():
    top_y = L
    cf_x = -FRONT_EXT
    neck_in = fc.P(cf_x, top_y - 40.0)
    shoulder_in = fc.P(NECK_HALF, top_y)
    shoulder_out = fc.P(SHOULDER_X, top_y)
    armhole_bot = fc.P(BW, top_y - armhole_drop)
    internals = [
        fc.Internal("cf-zip", [fc.P(0.0, 0.0), fc.P(0.0, top_y - 40.0)], kind="fold"),
        # chest pocket + pen row marked on the front
        fc.Internal("chest-pocket",
                    [fc.P(BW * 0.28, top_y - 150.0), fc.P(BW * 0.78, top_y - 150.0),
                     fc.P(BW * 0.78, top_y - 300.0), fc.P(BW * 0.28, top_y - 300.0),
                     fc.P(BW * 0.28, top_y - 150.0)], kind="marking"),
        fc.Internal("lower-pocket-place",
                    [fc.P(cf_x + 25.0, 40.0), fc.P(cf_x + 25.0 + pocket_w, 40.0)], kind="marking"),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            fc.Edge("neck", [fc.curve_through(neck_in, shoulder_in, bulge=0.14, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_out)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_out, armhole_bot,
                                                 bulge=0.22, side=-1.0)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 1.0, "shoulder point"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 60.0), fc.P(BW * 0.5, L - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip + pockets)",
    )


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y - 20.0)
    shoulder_in = fc.P(NECK_HALF, top_y)
    shoulder_out = fc.P(SHOULDER_X, top_y)
    armhole_bot = fc.P(BW, top_y - armhole_drop)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, shoulder_in, bulge=0.16, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_out)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_out, armhole_bot,
                                                 bulge=0.22, side=-1.0)]),
            fc.Edge("side", [fc.Line(armhole_bot, fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 1.0, "shoulder point"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 60.0), fc.P(BW * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_pocket():
    w, h, flap = pocket_w, pocket_h, 55.0
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
        cut=fc.CutSpec(quantity=2),
        label="Cargo pocket",
    )


def build():
    pattern = fc.PatternSet("utility-vest")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton canvas / ripstop",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; body + 2 cargo pockets; more pockets marked."},
        {"item": "front zipper", "qty": 1, "unit": "pc",
         "note": "full-length CF zip; a snap storm flap is the maker's option."},
        {"item": "pocket hardware (snaps / hook-loop)", "qty": 1, "unit": "set",
         "note": "close the bellows and chest pockets; maker's choice."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "topstitch every pocket and the zip facing."},
    ]
    pattern.metadata = {
        "fc200_rank": 170, "family": "workwear_uniforms", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A sleeveless zip-front utility vest built as a carrier of pockets — "
            "chest pockets, a pen row, and big lower bellows cargo pockets — with a deep armhole "
            "to layer over. Front and back share the body width, so the seams balance.",
        "solved": {"body_quarter_mm": round(BW, 1), "armhole_drop_mm": round(armhole_drop, 1)},
    }
    return pattern


result = build()
