"""
Barong (Tagalog) — Fashion Cabinet Garment Cartridge (FC-200 #198, Filipino heritage).

The barong tagalog is the formal embroidered shirt of the Philippines: a lightweight, sheer,
untucked shirt worn over an undershirt, with a band collar, a front placket, long sleeves with
cuffs, and side slits at the hem — traditionally in piña (pineapple fibre) or jusi, with the
chest embroidery (calado/sabog) that carries its formality. This cartridge drafts the GARMENT
GEOMETRY — a straight-cut body, band collar, sleeve, cuff — and marks (does not reproduce) the
embroidery panel. Offered with respect for the living tradition.

Pieces:
  - front / back : straight sheer body (front cut 2 with placket; back on fold), side slits.
  - sleeve / cuff / collar : long sleeve, cuff band, band collar.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|cuff|collar|set

chest_girth  = float(PARAM(lambda: chest_girth, 1060.0))
shirt_length = float(PARAM(lambda: shirt_length, 760.0))
neck_girth   = float(PARAM(lambda: neck_girth, 420.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 250.0))
side_slit    = float(PARAM(lambda: side_slit, 130.0))
ease         = float(PARAM(lambda: ease, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(760.0, min(chest_girth, 1600.0))
shirt_length = max(600.0, min(shirt_length, 950.0))
neck_girth   = max(320.0, min(neck_girth, 560.0))
sleeve_length = max(400.0, min(sleeve_length, 720.0))
sleeve_depth  = max(190.0, min(sleeve_depth, 380.0))
side_slit    = max(0.0, min(side_slit, 260.0))
ease         = max(120.0, min(ease, 380.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = shirt_length
BW = (chest_girth + ease) / 4.0
NECK_SCOOP = max(70.0, neck_girth / 5.0)
FRONT_EXT = 30.0


def build_back():
    top_y = L
    neck_top = fc.P(0.0, top_y)
    neck_out = fc.P(NECK_SCOOP, top_y)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=0.14, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, top_y), fc.P(BW, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, top_y - sleeve_depth), fc.P(BW, side_slit))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, side_slit), fc.P(BW, 0.0)),
                            fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "slit top")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    top_y = L
    cf_x = -FRONT_EXT
    neck_in = fc.P(cf_x, top_y)
    neck_out = fc.P(NECK_SCOOP, top_y)
    internals = [
        fc.Internal("placket", [fc.P(0.0, top_y - 40.0), fc.P(0.0, top_y - 300.0)], kind="marking"),
        fc.Internal("embroidery-panel",
                    [fc.P(cf_x + 20.0, top_y - 120.0), fc.P(BW * 0.75, top_y - 120.0),
                     fc.P(BW * 0.75, top_y - 420.0), fc.P(cf_x + 20.0, top_y - 420.0),
                     fc.P(cf_x + 20.0, top_y - 120.0)], kind="marking"),
    ]
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            fc.Edge("neck", [fc.Line(neck_in, neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, top_y), fc.P(BW, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, top_y - sleeve_depth), fc.P(BW, side_slit))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, side_slit), fc.P(BW, 0.0)),
                            fc.Line(fc.P(BW, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "slit top")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (placket + embroidery)",
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_length
    cuff_w = BW * 0.55
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - cuff_w) / 2.0))]),
            fc.Edge("cuff_edge", [fc.Line(fc.P(sw, (head_h - cuff_w) / 2.0),
                                          fc.P(sw, (head_h + cuff_w) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + cuff_w) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_cuff():
    ln = BW * 0.55 + 40.0
    h = 120.0
    return fc.Piece(
        "cuff",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Cuff",
    )


def build_collar():
    ln = neck_girth + 30.0
    h = 80.0
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Band collar",
    )


def build():
    pattern = fc.PatternSet("barong")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything or target_piece == "collar":
        pattern.add(build_collar())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "piña, jusi, or fine organza (sheer)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; a sheer, crisp fibre worn over an undershirt."},
        {"item": "chest embroidery (calado / sabog)", "qty": 1, "unit": "as applied",
         "note": "the calado drawn-thread and sabog embroidery carry the formality — the maker's."},
        {"item": "small buttons", "qty": 5, "unit": "pcs", "note": "the front placket + cuffs."},
        {"item": "fine thread", "qty": 1, "unit": "spool",
         "note": "French seams suit the sheer cloth; roll the side-slit and hem edges."},
    ]
    pattern.metadata = {
        "fc200_rank": 198, "family": "heritage_global", "fabric_hint": "pina-jusi",
        "heritage_note": "The barong tagalog is the formal dress shirt of the Philippines. This "
            "cartridge drafts the GARMENT GEOMETRY only — the calado and sabog embroidery, and "
            "the piña/jusi weaving that carry its formality and identity, are the maker's and are "
            "not reproduced here. Offered with respect.",
        "construction": "a straight-cut sheer body worn untucked with side slits, band collar, "
            "placket front, and cuffed sleeves; straight side/armhole seams balance.",
        "solved": {"body_quarter_mm": round(BW, 1), "side_slit_mm": round(side_slit, 1)},
    }
    return pattern


result = build()
