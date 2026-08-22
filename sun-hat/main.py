"""
Wide-Brim Sun Hat — Fashion Cabinet Garment Cartridge (FC-300 #213, Lane 2).

A packable wide-brim sun hat: a SIX-GORE crown (the gores summing to the head
opening), a straight SWEATBAND at the head line, and a wide ANNULAR BRIM drafted as
a half-annulus cut on the fold and mirrored — the bucket-hat / five-panel-cap
precedent, taken out to a shade brim. A pure soft-goods garment — no hardware.

Pieces:
  - crown-gore : one of `gores` crown panels, cut `gores` (mirrored).
  - sweatband  : the straight inner band at the head line, cut 1.
  - brim       : a half-annulus, cut on fold + mirrored -> the full brim ring.

Drafting notes:
  * The brim's INNER edge is a half-ring, so it measures HALF the head opening. It
    sews to half the crown/sweatband run — declared as the sweatband's head edge
    against the brim inner listed for its own mirror (join-to-join, not join-to-fold).
  * Arcs are polygons on a CORRECTED radius so the drafted perimeter equals the
    intended circumference exactly (r = C / (2n sin(pi/n))).
  * The gore side seams are SOLVED: the Bezier control net is scaled so the two
    curved edges measure the same run, which is what makes the crown close.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # crown|sweatband|brim|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
crown_height = float(PARAM(lambda: crown_height, 105.0))
brim_width = float(PARAM(lambda: brim_width, 95.0))
gores = int(PARAM(lambda: gores, 6))
sweatband_height = float(PARAM(lambda: sweatband_height, 38.0))
ease = float(PARAM(lambda: ease, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
crown_height = max(60.0, min(crown_height, 180.0))
brim_width = max(50.0, min(brim_width, 180.0))
gores = max(4, min(gores, 10))
sweatband_height = max(18.0, min(sweatband_height, 70.0))
ease = max(0.0, min(ease, 30.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48                        # full-ring segment count
head_eff = head_girth + ease     # the finished head opening
gore_base = head_eff / gores
GB = gore_base / 2.0


def _poly_radius(circumference, n):
    """Radius of a regular n-gon whose PERIMETER equals `circumference`."""
    return circumference / (2.0 * n * math.sin(math.pi / n))


R_IN = _poly_radius(head_eff, SEGS)        # brim inner radius (the head line)
R_OUT = R_IN + brim_width                  # brim outer radius


def _arc_points(r, a0, a1, n):
    """n+1 points along the arc a0..a1 (radians) on a circle of radius r."""
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _build_gore():
    """A crown gore: base `gore_base` at y=0, two Bezier seams rising to a shared
    apex at (0, crown_height). Symmetric, so the two seams measure equal runs and
    the crown closes on itself."""
    apex = fc.P(0.0, crown_height)
    left = fc.Bezier(fc.P(-GB, 0.0), fc.P(-GB * 0.97, crown_height * 0.44),
                     fc.P(-GB * 0.44, crown_height * 0.87), apex)
    right = fc.Bezier(apex, fc.P(GB * 0.44, crown_height * 0.87),
                      fc.P(GB * 0.97, crown_height * 0.44), fc.P(GB, 0.0))
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(GB, 0.0), fc.P(-GB, 0.0))]),  # to the sweatband
        fc.Edge("seam_l", [left]),
        fc.Edge("seam_r", [right]),
    ]
    return fc.Piece(
        "crown-gore",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, crown_height * 0.1), fc.P(0.0, crown_height * 0.85)),
        cut=fc.CutSpec(quantity=gores, mirror=True),
        label="Crown gore",
    )


def _build_sweatband():
    """The straight inner band at the head line: head_eff long, wrapping to a ring."""
    w, h = head_eff, sweatband_height
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("crown_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),   # to the crown gores
        fc.Edge("join_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("head_line", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),  # to the brim
    ]
    return fc.Piece(
        "sweatband",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown_edge", 0.5, "centre front"),
                 fc.Notch("head_line", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Sweatband",
    )


def _build_brim():
    """A half-annulus (inner R_IN, outer R_OUT) over a semicircle, cut on the straight
    centre edge and mirrored -> the full brim ring. Its `inner` edge therefore measures
    HALF the head opening."""
    half = SEGS // 2
    outer = _arc_points(R_OUT, -math.pi / 2.0, math.pi / 2.0, half)
    inner = _arc_points(R_IN, math.pi / 2.0, -math.pi / 2.0, half)
    edges = [
        fc.Edge("outer", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("centre_back", [fc.Line(outer[-1], inner[0])]),
        fc.Edge("inner", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("centre_front", [fc.Line(inner[-1], outer[0])]),
    ]
    return fc.Piece(
        "brim",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", 0.5, "side head")],
        grainline=fc.Grainline(fc.P(R_IN + brim_width * 0.35, -R_OUT * 0.3),
                               fc.P(R_IN + brim_width * 0.35, R_OUT * 0.3)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Brim",
    )


def build():
    pattern = fc.PatternSet("sun-hat")
    everything = target_piece == "set"

    if everything or target_piece == "crown":
        pattern.add(_build_gore())
    if everything or target_piece == "sweatband":
        pattern.add(_build_sweatband())
    if everything or target_piece == "brim":
        pattern.add(_build_brim())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if "crown-gore" in names:
        # Gore to neighbouring gore, all the way round the crown.
        pattern.declare_seam(("crown-gore", "seam_l"), ("crown-gore", "seam_r"), tol=1.0)
    if {"crown-gore", "sweatband"} <= names:
        # `gores` gore bases sum to the sweatband's crown edge.
        pattern.declare_seam([("crown-gore", "bottom")] * gores,
                             ("sweatband", "crown_edge"), tol=1.5)
    if "sweatband" in names:
        # The sweatband closes into a ring: its own two ends join.
        pattern.declare_seam(("sweatband", "join_a"), ("sweatband", "join_b"), tol=1.0)
    if {"sweatband", "brim"} <= names:
        # The brim is cut on the fold and mirrored, so its drafted `inner` edge is a
        # HALF ring: two of them (the piece against its own mirror, join-to-join) make
        # the full head line.
        pattern.declare_seam(("sweatband", "head_line"),
                             [("brim", "inner"), ("brim", "inner")], tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "shell fabric (washed cotton canvas or linen)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 62% marker; double it for a lined brim."},
        {"item": "brim interlining", "qty": 1, "unit": "set",
         "note": "sew-in horsehair or a fusible canvas — a wide brim needs body to shade."},
        {"item": "millinery wire (optional)", "qty": 1, "unit": "count",
         "note": "wire the brim's outer edge if you want a shapeable, packable brim."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "topstitch the brim in concentric rings to stiffen it."},
    ]
    pattern.metadata = {
        "fc300_rank": 213, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "gores": gores,
        "gore_base_mm": round(gore_base, 2),
        "crown_height_mm": round(crown_height, 1),
        "brim_width_mm": round(brim_width, 1),
        "brim_outer_dia_mm": round(2.0 * R_OUT, 1),
        "drafting": "gored crown + straight sweatband + half-annulus brim on fold",
        "solved": {
            "gore_bases_total_mm": round(gore_base * gores, 3),
            "sweatband_run_mm": round(head_eff, 3),
            "brim_inner_half_mm": round(head_eff / 2.0, 3),
        },
    }
    return pattern


result = build()
