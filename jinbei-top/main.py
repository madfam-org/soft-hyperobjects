"""
Jinbei (top) — Fashion Cabinet Garment Cartridge (FC-200 rank #158, Japanese heritage).

The jinbei is the traditional Japanese summer set worn at home and at festivals: a light,
open, kimono-cut jacket that ties at the sides, usually paired with matching shorts. This
cartridge drafts the JACKET — a rectangular kimono-cut body (back on fold + two fronts) with
wide dropped sleeves, an overlapping front closed by inner and outer side ties, in the
straight-seam idiom of Japanese garment construction where the side and armhole seams balance
by construction. The traditional sashiko/aizome finishing is the maker's and is not
reproduced here. Offered with respect for the living tradition.

Pieces:
  - back   : back rectangle, cut on fold at CB.
  - front  : front panel, cut 2 mirror (they overlap and tie).
  - sleeve : wide dropped sleeve rectangle, cut 2 mirror.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # back|front|sleeve|set

chest_girth   = float(PARAM(lambda: chest_girth, 1060.0))  # full chest
jacket_length = float(PARAM(lambda: jacket_length, 680.0)) # nape to hem (hip length)
neck_girth    = float(PARAM(lambda: neck_girth, 420.0))    # full neck
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 260.0))  # armhole drop
sleeve_length = float(PARAM(lambda: sleeve_length, 300.0)) # shoulder to sleeve opening
ease          = float(PARAM(lambda: ease, 240.0))          # light, airy ease
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth   = max(700.0, min(chest_girth, 1700.0))
jacket_length = max(500.0, min(jacket_length, 900.0))
neck_girth    = max(300.0, min(neck_girth, 560.0))
sleeve_depth  = max(180.0, min(sleeve_depth, 400.0))
sleeve_length = max(150.0, min(sleeve_length, 480.0))
ease          = max(120.0, min(ease, 460.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = jacket_length
BODY = (chest_girth + ease) / 2.0
BW = BODY / 2.0                                # back half-width (on fold)
FW = BW                                        # front == back width (straight seams balance)
NECK_SCOOP = max(60.0, neck_girth / 5.0)
BACK_NECK_DROP = 16.0
FRONT_NECK_DROP = 30.0


def build_back():
    neck_top = fc.P(0.0, L)
    neck_out = fc.P(NECK_SCOOP, L)
    back_bulge = BACK_NECK_DROP / max(NECK_SCOOP, 1.0)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=back_bulge, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, L), fc.P(BW, L - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, L - sleeve_depth), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    cf_x = 0.0
    side_x = FW
    neck_in = fc.P(cf_x, L - FRONT_NECK_DROP)
    neck_out = fc.P(NECK_SCOOP, L)
    internals = [
        # inner and outer side ties (himo) — inner anchors the right front, outer ties left
        fc.Internal("inner-tie", [fc.P(side_x - 30.0, L - sleeve_depth - 40.0),
                                  fc.P(side_x, L - sleeve_depth - 40.0)], kind="marking"),
        fc.Internal("cf-overlap", [fc.P(cf_x, 0.0), fc.P(cf_x, L - FRONT_NECK_DROP)], kind="fold"),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            fc.Edge("neck", [fc.curve_through(neck_in, neck_out, bulge=0.10, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(side_x, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(side_x, L), fc.P(side_x, L - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(side_x, L - sleeve_depth), fc.P(side_x, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(side_x, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(side_x * 0.5, 80.0), fc.P(side_x * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (ties at side)",
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
            fc.Edge("opening", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 0.0, "underarm"), fc.Notch("sleevehead", 1.0, "shoulder")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.2), fc.P(sw * 0.5, head_h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("jinbei-top")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1120.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "light cotton / linen (sashiko-weight or gauze)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1120 mm width, 74% marker; airy, open jacket."},
        {"item": "self-fabric ties (himo)", "qty": 4, "unit": "strips",
         "note": "inner + outer side ties close the overlapping front; cut from self fabric."},
        {"item": "front/neck band", "qty": 1, "unit": "strip",
         "note": "a folded band finishes the CF and neck (okumi-style); maker's width."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "straight seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 158,
        "family": "heritage_global",
        "fabric_hint": "algodon-gauze",
        "heritage_note": "The jinbei is living Japanese summer/festival dress, traditionally a "
            "set with matching shorts. This cartridge drafts the JACKET geometry only — the "
            "sashiko stitching, aizome (indigo) dyeing, and festival motifs that carry identity "
            "are the maker's and are not reproduced here. Offered with respect.",
        "construction": "rectangular kimono cut (back on fold + two overlapping fronts + wide "
            "dropped sleeves); closes with inner and outer side ties; straight side/armhole "
            "seams balance by construction.",
        "solved": {"body_half_mm": round(BW, 1), "front_width_mm": round(FW, 1),
                   "sleeve_depth_mm": round(sleeve_depth, 1)},
        "pairs_with": "traditionally worn with matching jinbei shorts (draft separately).",
    }
    return pattern


result = build()
