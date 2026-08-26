"""
Straw boater hat — FC-400 rank #354, Lane 6 (millinery). Fashion Cabinet Cartridge.

The straw boater: a stiff FLAT-TOP cylindrical crown and a stiff FLAT wide brim, the
summer-regatta hat. Drafted in three pieces — a circular flat TIP the same size as the head
ring (a true cylinder, not a dome), a straight side-crown BAND, and a flat annular BRIM.
Sizing clips into a Yantra4D hat-size-reducer (point hardware, no sewn edge).

Pieces:
  - tip   : the flat circular crown top, cut 1 (tip circ == head circ: a cylinder).
  - band  : the straight side crown, cut 1 (a rectangle: head circ × crown height).
  - brim  : the flat annular brim, cut on fold + mirrored (half-annulus).

Drafting notes:
  * Circular runs use the CORRECTED polygon radius so perimeters equal circumferences.
  * A boater crown is a true cylinder — the tip and band-top rings are BOTH the head ring,
    so the band is a plain rectangle, not a trapezoid.
  * The brim inner radius is floored below its outer so the annulus never inverts.

Hardware: Yantra4D hat-size-reducer (point/slot — no sewn edge, no dimensional handshake).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # tip|band|brim|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
ease = float(PARAM(lambda: ease, 8.0))
crown_height = float(PARAM(lambda: crown_height, 90.0))  # cylinder height (shallow)
brim_width = float(PARAM(lambda: brim_width, 70.0))      # flat brim radial width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

head_girth = max(480.0, min(head_girth, 640.0))
ease = max(0.0, min(ease, 30.0))
crown_height = max(40.0, min(crown_height, 180.0))
brim_width = max(30.0, min(brim_width, 180.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48
head_eff = head_girth + ease


def _poly_radius(c, n):
    return c / (2.0 * n * math.sin(math.pi / n))


R_HEAD = _poly_radius(head_eff, SEGS)
R_BRIM = R_HEAD + max(20.0, brim_width)
TIP_CIRC = 2.0 * SEGS * R_HEAD * math.sin(math.pi / SEGS)   # == head_eff (cylinder)


def _arc_points(r, a0, a1, n):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _build_tip():
    pts = _arc_points(R_HEAD, 0.0, 2.0 * math.pi, SEGS)
    half = SEGS // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SEGS)]),
    ]
    return fc.Piece(
        "tip", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_HEAD * 0.6), fc.P(0.0, R_HEAD * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Tip (flat crown top)",
    )


def _build_band():
    w, h = head_eff, crown_height
    return fc.Piece(
        "band",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),   # to the brim
            fc.Edge("end_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),          # to the tip
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre front"), fc.Notch("top", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Side crown band (straight)",
    )


def _build_brim():
    half = SEGS // 2
    outer = _arc_points(R_BRIM, -math.pi / 2.0, math.pi / 2.0, half)
    inner = _arc_points(R_HEAD, math.pi / 2.0, -math.pi / 2.0, half)
    edges = [
        fc.Edge("outer", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("centre_back", [fc.Line(outer[-1], inner[0])]),
        fc.Edge("inner", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("centre_front", [fc.Line(inner[-1], outer[0])]),
    ]
    return fc.Piece(
        "brim", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", 0.5, "side head")],
        grainline=fc.Grainline(fc.P(R_HEAD + brim_width * 0.4, -R_BRIM * 0.3),
                               fc.P(R_HEAD + brim_width * 0.4, R_BRIM * 0.3)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Brim (flat annulus)",
    )


def build():
    pattern = fc.PatternSet("boater-hat")
    everything = target_piece == "set"
    if everything or target_piece == "tip":
        pattern.add(_build_tip())
    if everything or target_piece == "band":
        pattern.add(_build_band())
    if everything or target_piece == "brim":
        pattern.add(_build_brim())

    names = {p.name for p in pattern.pieces}
    if {"tip", "band"} <= names:
        pattern.declare_seam([("tip", "rim_a"), ("tip", "rim_b")], ("band", "top"), tol=1.5)
    if {"band", "brim"} <= names:
        pattern.declare_seam(("band", "bottom"),
                             [("brim", "inner"), ("brim", "inner")], tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "sewn straw braid (or straw-cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker; a stiff sewn-braid straw "
                 "holds the flat boater shape."},
        {"item": "millinery wire (brim edge) + stiffener", "qty": 1, "unit": "set",
         "note": "wire and stiffen the flat brim so it stays crisp."},
        {"item": "hat size reducer strip", "qty": 1, "unit": "count",
         "note": "Yantra4D hat-size-reducer (see notion.hardware_ref) — clips inside the "
                 "crown band; not sewn into a seam."},
        {"item": "grosgrain band + ribbon", "qty": 1, "unit": "set",
         "note": "the classic boater ribbon band around the crown; grosgrain sweatband inside."},
    ]
    pattern.metadata = {
        "fc400_rank": 354, "family": "millinery", "lane": 6,
        "fabric_hint": "straw-braid",
        "head_girth_mm": round(head_girth, 1), "head_opening_mm": round(head_eff, 1),
        "crown_height_mm": round(crown_height, 1), "brim_width_mm": round(brim_width, 1),
        "solved": {
            "tip_circ_mm": round(TIP_CIRC, 2),
            "band_top_mm": round(head_eff, 2),
            "band_bottom_mm": round(head_eff, 2),
            "brim_inner_full_mm": round(head_eff, 2),
            "brim_outer_dia_mm": round(2.0 * R_BRIM, 1),
            "note": "a true cylinder — tip and band rings are both the head ring; the brim "
                    "inner radius is below the outer so the annulus never inverts",
        },
        "hardware": "sizing delegated to Yantra4D hat-size-reducer (point/slot — no sewn "
                    "edge, no dimensional handshake)",
    }
    return pattern


result = build()
