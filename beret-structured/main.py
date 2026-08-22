"""
Structured Beret — Fashion Cabinet Garment Cartridge (FC-300 #216, Lane 2).

The classic two-piece beret: a full circular TOP and an ANNULAR UNDER whose outer
edge matches the top's circumference and whose inner hole is the head opening — plus
a structured BAND that finishes that hole and gives the beret its blocked edge.
Sizing is delegated to a Yantra4D `hat-size-reducer` clipped inside the band
(point/slot hardware — it sits in the band, it is not sewn to a garment edge).

Pieces:
  - top   : the full circular crown, cut 1.
  - under : the annulus, cut on fold + mirrored (a half-annulus draft).
  - band  : the structured inner band that finishes the head opening, cut 1.

Drafting notes:
  * Circular runs are polygons on a CORRECTED radius (r = C / (2n sin(pi/n))) so the
    drafted perimeter equals the intended circumference exactly.
  * The under is a HALF-annulus cut on the fold, so both its `outer` and `inner` edges
    measure HALF their rings. Each is declared against its mate listed twice — the
    piece against its own mirror, join-to-join, never join-to-fold.
  * `overhang` is the beret's signature: the top circle is bigger than the head
    opening, and that difference is what makes it flop over the band.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # top|under|band|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
overhang = float(PARAM(lambda: overhang, 55.0))     # how far the top oversails the head
band_height = float(PARAM(lambda: band_height, 32.0))
ease = float(PARAM(lambda: ease, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
overhang = max(20.0, min(overhang, 130.0))
band_height = max(15.0, min(band_height, 70.0))
ease = max(0.0, min(ease, 26.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48
TWO_PI = 2.0 * math.pi
head_eff = head_girth + ease          # the finished head opening


def _poly_radius(circumference, n):
    """Radius of a regular n-gon whose PERIMETER equals `circumference`."""
    return circumference / (2.0 * n * math.sin(math.pi / n))


R_HEAD = _poly_radius(head_eff, SEGS)       # the head-opening ring
R_TOP = R_HEAD + overhang                   # the beret's outer ring
TOP_CIRC = 2.0 * SEGS * R_TOP * math.sin(math.pi / SEGS)   # the drafted outer run


def _arc_points(r, a0, a1, n):
    """n+1 points along the arc a0..a1 (radians) on a circle of radius r."""
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _build_top():
    """The full circular crown. Two half-ring edges give named seam references."""
    pts = _arc_points(R_TOP, 0.0, TWO_PI, SEGS)
    half = SEGS // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SEGS)]),
    ]
    return fc.Piece(
        "top",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_TOP * 0.6), fc.P(0.0, R_TOP * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Top (crown)",
    )


def _build_under():
    """A half-annulus (inner R_HEAD, outer R_TOP) over a semicircle, cut on the
    straight centre edge and mirrored -> the full under ring. Both curved edges
    therefore measure HALF their rings."""
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
        "under",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer", 0.5, "side head"), fc.Notch("inner", 0.5, "side head")],
        grainline=fc.Grainline(fc.P(R_HEAD + overhang * 0.4, -R_TOP * 0.3),
                               fc.P(R_HEAD + overhang * 0.4, R_TOP * 0.3)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Under (annulus)",
    )


def _build_band():
    """The structured inner band finishing the head opening; it wraps to a ring."""
    w, h = head_eff, band_height
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("under_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),   # to the under's hole
        fc.Edge("join_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("head_opening", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("under_edge", 0.5, "centre front"),
                 fc.Notch("head_opening", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Structured band",
    )


def build():
    pattern = fc.PatternSet("beret-structured")
    everything = target_piece == "set"

    if everything or target_piece == "top":
        pattern.add(_build_top())
    if everything or target_piece == "under":
        pattern.add(_build_under())
    if everything or target_piece == "band":
        pattern.add(_build_band())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if {"top", "under"} <= names:
        # The top's full rim takes the under's outer ring. The under is cut on the fold
        # and mirrored, so its drafted `outer` is a HALF ring: listed twice (the piece
        # against its own mirror, join-to-join) it makes the full run.
        pattern.declare_seam([("top", "rim_a"), ("top", "rim_b")],
                             [("under", "outer"), ("under", "outer")], tol=1.5)
    if {"under", "band"} <= names:
        # Likewise the under's inner hole — a half ring, listed twice — takes the
        # band's upper edge.
        pattern.declare_seam([("under", "inner"), ("under", "inner")],
                             ("band", "under_edge"), tol=1.5)
    if "band" in names:
        # The band closes into a ring: its own two ends join.
        pattern.declare_seam(("band", "join_a"), ("band", "join_b"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.58)
    pattern.bom = [
        {"item": "shell fabric (boiled wool, melton or felt)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 58% marker; a fulled wool blocks best."},
        {"item": "band interfacing", "qty": 1, "unit": "set",
         "note": "the structured band is what stops the head opening stretching out."},
        {"item": "hat size reducer strip", "qty": 1, "unit": "count",
         "note": "Yantra4D hat-size-reducer (see notion.hardware_ref) — clips inside the "
                 "band to take the beret down a size; not sewn into a seam."},
        {"item": "grosgrain ribbon + thread", "qty": 1, "unit": "set",
         "note": "face the band with grosgrain; press the beret over a plate to block it."},
    ]
    pattern.metadata = {
        "fc300_rank": 216, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "overhang_mm": round(overhang, 1),
        "top_dia_mm": round(2.0 * R_TOP, 1),
        "band_height_mm": round(band_height, 1),
        "drafting": "circular top + half-annulus under on fold + structured band",
        "hardware": "sizing delegated to Yantra4D hat-size-reducer (point/slot — no sewn edge)",
        "solved": {
            "top_rim_mm": round(TOP_CIRC, 3),
            "under_outer_full_mm": round(TOP_CIRC, 3),
            "under_inner_full_mm": round(head_eff, 3),
            "band_run_mm": round(head_eff, 3),
        },
    }
    return pattern


result = build()
