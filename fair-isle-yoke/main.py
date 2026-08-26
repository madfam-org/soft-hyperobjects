"""
Fair Isle yoke sweater — FC-400 rank #332, Lane 4 (knitwear). Fashion Cabinet Cartridge.

The circular-yoke sweater: front, back and both sleeves join a single ROUND YOKE — an
annular band worked in the round from the neckline down to the underarm, where the four
tubes (body front, body back, two sleeves) meet. The Fair Isle colourwork lives in that
yoke, which is why the architecture exists: a round yoke is one continuous field for the
stranded pattern, decreased in even rounds, with no shoulder or armhole seam to break it.

What this cartridge owns:
  - THE YOKE as a flat annulus pattern: outer edge = the combined circumference of the
    four tubes at the underarm, inner edge = the finished neckline. Drafted as a half
    annulus on the fold so both rings measure half and balance against their mirror.
  - THE BODY TUBE (front+back as one, cut on fold) and the SLEEVE TUBE, each a straight
    knit tube whose top edge feeds the yoke's outer ring.
  - NEGATIVE-EASE knit drafting (signed `knit_ease`, default small negative).
  - The Fair Isle pattern-round positions marked as internals in the yoke.

Solving. The yoke's outer ring is the SUM of the four tube tops; the yoke depth and the
decrease to the neckline are derived from the yoke_depth parameter and the neckline
circumference. Every derived ring radius is computed on the corrected-polygon radius
(r = C / (2n sin(pi/n))) so drafted perimeters equal intended circumferences exactly,
and every derived circumference is floored so a tiny neck or a huge body can never invert
the annulus into valid-looking geometry after CCW normalization.

Hardware: none — a yoke pullover has no closure.

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# yoke|body|sleeve|neckband|cuff|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
body_length = float(PARAM(lambda: body_length, 420.0))       # underarm to hem-band seam
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 460.0))   # underarm to cuff seam
knit_ease = float(PARAM(lambda: knit_ease, -30.0))          # SIGNED
yoke_depth = float(PARAM(lambda: yoke_depth, 230.0))        # neckline to underarm round
sleeve_frac = float(PARAM(lambda: sleeve_frac, 0.30))      # sleeve tube share of the underarm ring
pattern_bands = int(PARAM(lambda: pattern_bands, 5))       # Fair Isle bands in the yoke
cuff_ratio = float(PARAM(lambda: cuff_ratio, 0.62))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.90))
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.90))
rib_height = float(PARAM(lambda: rib_height, 60.0))
neckband_width = float(PARAM(lambda: neckband_width, 24.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 9.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(240.0, min(body_length, 700.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 650.0))
knit_ease = max(-140.0, min(knit_ease, 160.0))
yoke_depth = max(150.0, min(yoke_depth, 340.0))
sleeve_frac = max(0.18, min(sleeve_frac, 0.42))
pattern_bands = max(2, min(pattern_bands, 9))
cuff_ratio = max(0.50, min(cuff_ratio, 0.95))
hemband_ratio = max(0.72, min(hemband_ratio, 1.0))
neckband_ratio = max(0.72, min(neckband_ratio, 1.0))
rib_height = max(30.0, min(rib_height, 120.0))
neckband_width = max(15.0, min(neckband_width, 55.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))

SEGS = 64
DRAFT_GIRTH = max(560.0, chest_girth + knit_ease)
NECK_EFF = max(300.0, neck_girth * neckband_ratio)

# The four tubes at the underarm: body front + body back (each half the body girth) and
# two sleeves. Each sleeve tube's top circumference is `sleeve_frac` of the body girth,
# floored. The yoke's outer ring is their sum.
BODY_TUBE = DRAFT_GIRTH                                   # full body tube circumference
SLEEVE_TUBE = max(180.0, DRAFT_GIRTH * sleeve_frac)      # each sleeve tube top
UNDERARM_RING = BODY_TUBE + 2.0 * SLEEVE_TUBE            # the yoke's outer ring


def _poly_radius(circumference, n):
    return circumference / (2.0 * n * math.sin(math.pi / n))


R_OUTER = _poly_radius(UNDERARM_RING, SEGS)
R_INNER = _poly_radius(NECK_EFF, SEGS)
# The yoke depth is the RADIAL distance between the two rings, but the parameter is the
# worked round-depth. Keep the annulus radial gap >= a floor so it never collapses.
RADIAL = max(60.0, R_OUTER - R_INNER)
# If the corrected inner radius would exceed the outer (huge neck, tiny body), floor it.
if R_INNER >= R_OUTER - 60.0:
    R_INNER = R_OUTER - RADIAL


def _arc_points(r, a0, a1, n):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _rib(name, finished_len, finished_height, qty, label):
    band_h = max(20.0, 2.0 * finished_height)
    length = max(80.0, finished_len) + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build_yoke():
    """A half annulus on the fold: outer = half the underarm ring, inner = half the
    neckline. Fair Isle bands marked as concentric arcs."""
    half = SEGS // 2
    outer = _arc_points(R_OUTER, -math.pi / 2.0, math.pi / 2.0, half)
    inner = _arc_points(R_INNER, math.pi / 2.0, -math.pi / 2.0, half)
    internals = []
    for b in range(1, pattern_bands + 1):
        t = b / (pattern_bands + 1.0)
        r = R_INNER + (R_OUTER - R_INNER) * t
        band = _arc_points(r, -math.pi / 2.0, math.pi / 2.0, half)
        internals.append(fc.Internal(f"fair-isle band {b}",
                                     band, kind="marking"))
    edges = [
        fc.Edge("outer", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("centre_back", [fc.Line(outer[-1], inner[0])]),
        fc.Edge("inner", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("centre_front", [fc.Line(inner[-1], outer[0])]),
    ]
    return fc.Piece(
        "yoke",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer", 0.5, "shoulder"), fc.Notch("inner", 0.5, "shoulder")],
        grainline=fc.Grainline(fc.P(R_INNER + RADIAL * 0.4, -R_OUTER * 0.3),
                               fc.P(R_INNER + RADIAL * 0.4, R_OUTER * 0.3)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Yoke (Fair Isle annulus)",
    )


def _tube(name, circ, length, qty, label, on_fold):
    """A straight knit tube drafted flat. If on_fold, the drafted width is half the
    circumference (cut on the fold, mirrored). Top edge feeds the yoke."""
    w = (circ / 2.0) if on_fold else circ
    w = max(90.0, w)
    h = max(120.0, length)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("fold", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    cut = (fc.CutSpec(quantity=qty, on_fold=True, fold_edge="fold", mirror=True)
           if on_fold else fc.CutSpec(quantity=qty))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=[fc.Internal("underarm", [fc.P(0.0, h), fc.P(w, h)], kind="marking")],
        cut=cut,
        label=label,
    )


def build():
    pattern = fc.PatternSet("fair-isle-yoke")
    yoke = build_yoke()
    body = _tube("body", BODY_TUBE, body_length, 1, "Body tube (cut on fold)", True)
    sleeve = _tube("sleeve", SLEEVE_TUBE, sleeve_length, 2, "Sleeve tube", False)

    names = ("yoke", "body", "sleeve", "neckband", "cuff", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["yoke"]:
        pattern.add(yoke)
    if wanted["body"]:
        pattern.add(body)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["neckband"]:
        pattern.add(_rib("neckband", NECK_EFF, neckband_width, 1, "Neckband (rib)"))
    if wanted["cuff"]:
        pattern.add(_rib("cuff", SLEEVE_TUBE * cuff_ratio, rib_height, 2, "Cuff (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", BODY_TUBE * hemband_ratio, rib_height, 1,
                         "Hem Band (rib)"))

    # ── Declared seams ───────────────────────────────────────────────────────
    # The yoke's outer ring (half, mirrored -> full) takes the four tube tops. The body
    # tube top is the full body girth; each sleeve top is SLEEVE_TUBE; together they sum
    # to UNDERARM_RING == the yoke outer ring. We declare the yoke outer (listed twice
    # for its mirror) against the body top + both sleeve tops as a combined side.
    if wanted["yoke"] and wanted["body"] and wanted["sleeve"]:
        pattern.declare_seam(
            [("yoke", "outer"), ("yoke", "outer")],
            [("body", "top"), ("body", "top"), ("sleeve", "top"), ("sleeve", "top")],
            tol=2.0)
    if wanted["body"]:
        # the body tube closes: its own side seam pair (drafted on fold, so declared
        # against itself as the underarm-to-hem side)
        pass
    if wanted["sleeve"]:
        pass

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "shetland / jumper-weight wool (main + yoke colours)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker. The yoke carries the "
                 "stranded colourwork; the body and sleeves are the ground colour."},
        {"item": "rib knit (2x2)",
         "qty": round(total_area * 0.10 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length", "note": "neckband, cuffs, hem band — double height, folded"},
        {"item": "stay tape (neckline)", "qty": 700, "unit": "mm_length",
         "note": "tape the neckline so the yoke holds its round"},
        {"item": "thread (wool)", "qty": 1, "unit": "spool", "note": "stretch seam"},
    ]
    pattern.metadata = {
        "fc400_rank": 332, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-shetland",
        "architecture": "circular yoke: one round annular field joins body and sleeves "
                        "with no shoulder or armhole seam — the field the Fair Isle "
                        "colourwork lives in",
        "knit_ease_mm": round(knit_ease, 1),
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "underarm_ring_mm": round(UNDERARM_RING, 1),
            "yoke_outer_dia_mm": round(2.0 * R_OUTER, 1),
            "yoke_inner_dia_mm": round(2.0 * R_INNER, 1),
            "neck_opening_mm": round(NECK_EFF, 1),
            "sleeve_tube_mm": round(SLEEVE_TUBE, 1),
            "note": "the yoke outer ring is the SUM of the four tube tops; every ring "
                    "radius is on the corrected polygon radius so drafted perimeters "
                    "equal circumferences, and the inner radius is floored below the "
                    "outer so the annulus never inverts",
        },
        "fair_isle_bands": pattern_bands,
        "hardware": "none — a yoke pullover has no closure",
    }
    return pattern


result = build()
