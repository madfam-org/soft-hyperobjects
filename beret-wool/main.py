"""
Wool beret — FC-400 rank #355, Lane 6 (millinery). Fashion Cabinet Cartridge.

The classic soft wool beret: a full circular TOP and an annular UNDER whose outer edge
matches the top's circumference and whose inner hole is the head opening, finished with a
narrow band. Unlike the structured beret, this is the soft blocked-wool version with no
sizing hardware — the band is knitted or bias-cut wool that hugs the head.

Pieces:
  - top   : the full circular crown, cut 1.
  - under : the annulus, cut on fold + mirrored (a half-annulus draft).
  - band  : the soft inner band that finishes the head opening, cut 1.

Drafting notes:
  * Circular runs are polygons on a CORRECTED radius (r = C / (2n sin(pi/n))) so the
    drafted perimeter equals the intended circumference exactly.
  * The under is a HALF-annulus cut on the fold, so both its outer and inner edges
    measure HALF their rings; each is declared against its mate listed twice.
  * `overhang` is the beret's signature: the top circle is bigger than the head opening,
    and that difference is what makes it flop over the band. It is FLOORED so a zero or
    negative overhang can never invert the annulus.

Hardware: none — a soft wool beret has no sizing hardware.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # top|under|band|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
overhang = float(PARAM(lambda: overhang, 70.0))      # how far the top oversails the head
band_height = float(PARAM(lambda: band_height, 28.0))
ease = float(PARAM(lambda: ease, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

head_girth = max(480.0, min(head_girth, 640.0))
overhang = max(30.0, min(overhang, 160.0))
band_height = max(12.0, min(band_height, 60.0))
ease = max(0.0, min(ease, 26.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48
TWO_PI = 2.0 * math.pi
head_eff = head_girth + ease


def _poly_radius(c, n):
    return c / (2.0 * n * math.sin(math.pi / n))


R_HEAD = _poly_radius(head_eff, SEGS)
R_TOP = R_HEAD + max(20.0, overhang)                  # floored so the annulus never inverts
TOP_CIRC = 2.0 * SEGS * R_TOP * math.sin(math.pi / SEGS)


def _arc_points(r, a0, a1, n):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _build_top():
    pts = _arc_points(R_TOP, 0.0, TWO_PI, SEGS)
    half = SEGS // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SEGS)]),
    ]
    return fc.Piece(
        "top", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_TOP * 0.6), fc.P(0.0, R_TOP * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Top (crown)",
    )


def _build_under():
    half = SEGS // 2
    outer = _arc_points(R_TOP, -math.pi / 2.0, math.pi / 2.0, half)
    inner = _arc_points(R_HEAD, math.pi / 2.0, -math.pi / 2.0, half)
    edges = [
        fc.Edge("outer", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("centre_back", [fc.Line(outer[-1], inner[0])]),
        fc.Edge("inner", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("centre_front", [fc.Line(inner[-1], outer[0])]),
    ]
    return fc.Piece(
        "under", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer", 0.5, "side head"), fc.Notch("inner", 0.5, "side head")],
        grainline=fc.Grainline(fc.P(R_HEAD + overhang * 0.4, -R_TOP * 0.3),
                               fc.P(R_HEAD + overhang * 0.4, R_TOP * 0.3)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Under (annulus)",
    )


def _build_band():
    w, h = head_eff, band_height
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("under_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("join_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("head_opening", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("under_edge", 0.5, "centre front"),
                 fc.Notch("head_opening", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Inner band",
    )


def build():
    pattern = fc.PatternSet("beret-wool")
    everything = target_piece == "set"
    if everything or target_piece == "top":
        pattern.add(_build_top())
    if everything or target_piece == "under":
        pattern.add(_build_under())
    if everything or target_piece == "band":
        pattern.add(_build_band())

    names = {p.name for p in pattern.pieces}
    if {"top", "under"} <= names:
        pattern.declare_seam([("top", "rim_a"), ("top", "rim_b")],
                             [("under", "outer"), ("under", "outer")], tol=1.5)
    if {"under", "band"} <= names:
        pattern.declare_seam([("under", "inner"), ("under", "inner")],
                             ("band", "under_edge"), tol=1.5)
    if "band" in names:
        pattern.declare_seam(("band", "join_a"), ("band", "join_b"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.58)
    pattern.bom = [
        {"item": "boiled/felted wool (melton)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 58% marker; a fulled wool blocks best."},
        {"item": "soft band (knitted or bias wool)", "qty": 1, "unit": "set",
         "note": "the soft band hugs the head; no sizing hardware."},
        {"item": "grosgrain + thread", "qty": 1, "unit": "set",
         "note": "face the band with grosgrain; press over a plate to block."},
    ]
    pattern.metadata = {
        "fc400_rank": 355, "family": "millinery", "lane": 6,
        "fabric_hint": "wool-felt",
        "head_girth_mm": round(head_girth, 1), "head_opening_mm": round(head_eff, 1),
        "overhang_mm": round(overhang, 1), "top_dia_mm": round(2.0 * R_TOP, 1),
        "band_height_mm": round(band_height, 1),
        "drafting": "circular top + half-annulus under on fold + soft band",
        "solved": {
            "top_rim_mm": round(TOP_CIRC, 3),
            "under_outer_full_mm": round(TOP_CIRC, 3),
            "under_inner_full_mm": round(head_eff, 3),
            "band_run_mm": round(head_eff, 3),
            "note": "the overhang is floored at 20 mm so the top ring is always larger "
                    "than the head ring and the annulus can never invert",
        },
        "hardware": "none — a soft wool beret has no sizing hardware",
    }
    return pattern


result = build()
