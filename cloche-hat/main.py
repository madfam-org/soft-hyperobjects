"""
Cloche hat — FC-400 rank #353, Lane 6 (millinery). Fashion Cabinet Cartridge.

The 1920s cloche: a deep bell crown that hugs the head down to the brow, with a small
downturned brim. Drafted in three pieces — a circular TIP (the top of the bell), a
side-crown BAND that wraps the head and gives the bell its depth, and an annular BRIM that
turns down. Sizing is delegated to a Yantra4D hat-size-reducer clipped inside the crown
band (point hardware — it sits in the band, not sewn to a garment edge).

Pieces:
  - tip   : the circular crown top, cut 1.
  - band  : the side crown, cut 1, wrapped into the bell (drafted flat: head circ × depth).
  - brim  : the annular downturned brim, cut on fold + mirrored (half-annulus draft).

Drafting notes:
  * Circular runs use the CORRECTED polygon radius so perimeters equal circumferences.
  * The tip circumference == the band's top edge; the band's bottom edge == the head
    opening == the brim's inner ring. Each ring is solved, not eyeballed.
  * The brim inner radius is floored below its outer radius so the annulus never inverts.

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
crown_depth = float(PARAM(lambda: crown_depth, 150.0))   # side-crown height (the bell)
tip_dome = float(PARAM(lambda: tip_dome, 30.0))          # how much the tip is smaller than head
brim_width = float(PARAM(lambda: brim_width, 55.0))      # radial brim width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

head_girth = max(480.0, min(head_girth, 640.0))
ease = max(0.0, min(ease, 30.0))
crown_depth = max(60.0, min(crown_depth, 260.0))
tip_dome = max(0.0, min(tip_dome, 120.0))
brim_width = max(15.0, min(brim_width, 160.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48
head_eff = head_girth + ease


def _poly_radius(c, n):
    return c / (2.0 * n * math.sin(math.pi / n))


R_HEAD = _poly_radius(head_eff, SEGS)
# The tip is domed: slightly smaller than the head ring. Floored above zero.
TIP_CIRC = max(140.0, head_eff - 2.0 * math.pi * min(tip_dome, R_HEAD * 0.6))
R_TIP = _poly_radius(TIP_CIRC, SEGS)
R_BRIM = R_HEAD + max(10.0, brim_width)                  # brim outer, floored


def _arc_points(r, a0, a1, n):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _build_tip():
    pts = _arc_points(R_TIP, 0.0, 2.0 * math.pi, SEGS)
    half = SEGS // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SEGS)]),
    ]
    return fc.Piece(
        "tip", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_TIP * 0.6), fc.P(0.0, R_TIP * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Tip (crown top)",
    )


def _build_band():
    # Flat side crown: length = the head circ, height = crown_depth. Top edge sews to the
    # tip (so its length is the TIP circ), bottom edge to the brim (head circ). The band
    # is thus a trapezoid: top = TIP_CIRC, bottom = head_eff, height = crown_depth.
    top_len = TIP_CIRC
    bot_len = head_eff
    h = crown_depth
    dx = (bot_len - top_len) / 2.0
    return fc.Piece(
        "band",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(bot_len, 0.0))]),  # head opening
            fc.Edge("end_b", [fc.Line(fc.P(bot_len, 0.0), fc.P(bot_len - dx, h))]),
            fc.Edge("top", [fc.Line(fc.P(bot_len - dx, h), fc.P(dx, h))]),      # to the tip
            fc.Edge("end_a", [fc.Line(fc.P(dx, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre front"), fc.Notch("top", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(bot_len * 0.5, h * 0.2), fc.P(bot_len * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Side crown band",
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
        label="Brim (annulus)",
    )


def build():
    pattern = fc.PatternSet("cloche-hat")
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
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "wool felt (blocked)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker; a fur or wool felt blocks "
                 "into the bell."},
        {"item": "millinery wire (brim edge)", "qty": 1, "unit": "set",
         "note": "wire the brim edge so the downturn holds."},
        {"item": "hat size reducer strip", "qty": 1, "unit": "count",
         "note": "Yantra4D hat-size-reducer (see notion.hardware_ref) — clips inside the "
                 "crown band to take the hat down a size; not sewn into a seam."},
        {"item": "grosgrain sweatband + thread", "qty": 1, "unit": "set",
         "note": "grosgrain sweatband inside the crown band; press over a block."},
    ]
    pattern.metadata = {
        "fc400_rank": 353, "family": "millinery", "lane": 6,
        "fabric_hint": "wool-felt",
        "head_girth_mm": round(head_girth, 1), "head_opening_mm": round(head_eff, 1),
        "crown_depth_mm": round(crown_depth, 1), "brim_width_mm": round(brim_width, 1),
        "solved": {
            "tip_circ_mm": round(TIP_CIRC, 2),
            "band_top_mm": round(TIP_CIRC, 2),
            "band_bottom_mm": round(head_eff, 2),
            "brim_inner_full_mm": round(head_eff, 2),
            "brim_outer_dia_mm": round(2.0 * R_BRIM, 1),
            "note": "the tip circ is floored above zero and the brim inner radius is below "
                    "the outer so no ring inverts; every ring is on the corrected radius",
        },
        "hardware": "sizing delegated to Yantra4D hat-size-reducer (point/slot — no sewn "
                    "edge, no dimensional handshake)",
    }
    return pattern


result = build()
