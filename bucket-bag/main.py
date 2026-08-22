"""
Bucket Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #208, y4d strap end tip).

A drawcord bucket: a circular BASE, a slightly flared cylindrical BODY that sews to it, a
drawcord CASING at the top, and a shoulder STRAP finished with a metal strap end tip. The
tip is a Yantra4D solid (`strap-end-tip`; see the manifest's notion.hardware_ref) whose
strap channel takes this bag's `strap_width`.

The seam that must SOLVE: the base is a 48-gon whose perimeter is under the true circle,
AND the body flares — its base edge is narrower than its top edge. Both runs are measured
off the drafted geometry: the body's base edge is derived from the measured base polygon
perimeter, and the casing is drafted to the body's measured top edge. Neither is a formula.

Pieces:
  - body   : the flared cylinder wall; wraps so `wrap_a` meets `wrap_b`.
  - base   : the circular base panel.
  - casing : the drawcord casing sewn to the body's top edge.
  - strap  : the shoulder strap, finished with the Yantra4D end tip.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|base|casing|strap|set

base_diameter = float(PARAM(lambda: base_diameter, 200.0))  # circular base diameter
bag_height = float(PARAM(lambda: bag_height, 260.0))        # wall height
top_flare = float(PARAM(lambda: top_flare, 40.0))           # extra diameter at the top
casing_depth = float(PARAM(lambda: casing_depth, 34.0))     # drawcord casing depth
strap_width = float(PARAM(lambda: strap_width, 25.0))       # shoulder strap width
strap_length = float(PARAM(lambda: strap_length, 900.0))    # shoulder strap length
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
base_diameter = max(120.0, min(base_diameter, 340.0))
bag_height = max(140.0, min(bag_height, 420.0))
top_flare = max(0.0, min(top_flare, 140.0))
casing_depth = max(18.0, min(casing_depth, 70.0))
strap_width = max(12.0, min(strap_width, 50.0))
strap_length = max(400.0, min(strap_length, 1400.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SIDES = 48
R_BASE = base_diameter / 2.0


def _arc_points(cx, cy, r, a0, a1, n):
    """n+1 points along the arc from a0 to a1 (radians) on a circle at (cx, cy)."""
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


# The measured perimeter of the 48-gon base — the body's base edge must equal THIS.
_BASE_PTS = _arc_points(0.0, 0.0, R_BASE, 0.0, 2.0 * math.pi, SIDES)
BASE_PERIMETER = sum(_BASE_PTS[i].distance(_BASE_PTS[i + 1]) for i in range(SIDES))

# The top is flared: its circumference grows by pi * top_flare, scaled by the same
# polygon-vs-circle ratio the base carries, so both ends stay consistent.
_POLY_RATIO = BASE_PERIMETER / (2.0 * math.pi * R_BASE)
TOP_PERIMETER = _POLY_RATIO * math.pi * (base_diameter + top_flare)


def build_body():
    """The flared cylinder wall: `base_edge` is the measured base perimeter, `top_edge`
    is the flared top perimeter, and the two wrap seams close the tube. The flare makes
    this a trapezoid, not a rectangle."""
    wb, wt, h = BASE_PERIMETER, TOP_PERIMETER, bag_height
    dx = (wt - wb) / 2.0        # how far each side leans out
    edges = [
        fc.Edge("wrap_a", [fc.Line(fc.P(0.0, 0.0), fc.P(-dx, h))]),
        fc.Edge("top_edge", [fc.Line(fc.P(-dx, h), fc.P(wb + dx, h))]),
        fc.Edge("wrap_b", [fc.Line(fc.P(wb + dx, h), fc.P(wb, 0.0))]),
        fc.Edge("base_edge", [fc.Line(fc.P(wb, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # Eyelet marks where the drawcord exits the casing.
        fc.Internal("cord-exit",
                    [fc.P(wb * 0.5 - 20.0, h - casing_depth * 0.5),
                     fc.P(wb * 0.5 + 20.0, h - casing_depth * 0.5)], kind="drill"),
    ]
    # Strap anchor runs on the two sides of the wrap.
    for x in (wb * 0.25, wb * 0.75):
        internals.append(fc.Internal("strap-anchor",
                                     [fc.P(x, h * 0.62), fc.P(x, h * 0.62 + strap_width)],
                                     kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base_edge", 0.5, "centre front"),
                 fc.Notch("top_edge", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(wb * 0.5, 30.0), fc.P(wb * 0.5, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (flared wall)",
    )


def build_base():
    """The circular base panel, split into two named half-perimeter edges."""
    pts = _BASE_PTS
    half = SIDES // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SIDES)]),
    ]
    return fc.Piece(
        "base",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, -R_BASE * 0.6), fc.P(0.0, R_BASE * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Base Panel",
    )


def build_casing():
    """The drawcord casing: a strip the length of the body's MEASURED top edge, folded
    double so the cord runs inside it."""
    ln = build_body().edge("top_edge").length(0.02)
    w = casing_depth
    return fc.Piece(
        "casing",
        [
            fc.Edge("join", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Drawcord Casing",
    )


def build_strap():
    """The shoulder strap; its `tip_end` is finished with the Yantra4D strap end tip, so
    it is cut at exactly the width that tip's channel expects."""
    ln, w = strap_length, strap_width
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("tip_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Shoulder Strap",
    )


def build():
    pattern = fc.PatternSet("bucket-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "base":
        pattern.add(build_base())
    if all_pieces or target_piece == "casing":
        pattern.add(build_casing())
    if all_pieces or target_piece == "strap":
        pattern.add(build_strap())

    if all_pieces:
        # The body's base edge wraps the whole base polygon perimeter.
        pattern.declare_seam(("body", "base_edge"),
                             [("base", "rim_a"), ("base", "rim_b")], tol=1.0)
        # The casing is drafted to the body's measured (flared) top edge.
        pattern.declare_seam(("casing", "join"), ("body", "top_edge"), tol=1.0)
    if all_pieces or target_piece == "body":
        # The tube's back seam: the two leaning wrap edges are equal by construction.
        pattern.declare_seam(("body", "wrap_a"), ("body", "wrap_b"), tol=0.5)
    if all_pieces or target_piece == "strap":
        # The strap's two ends are the same width — both feed the same-width hardware.
        pattern.declare_seam(("strap", "tip_end"), ("strap", "anchor_end"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "garment leather, suede or heavy canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 66% marker; the base wants a stiffener disc."},
        {"item": "drawcord", "qty": round(TOP_PERIMETER + 400.0), "unit": "mm_length",
         "note": "through the casing and out the marked eyelets."},
        {"item": "strap end tip", "qty": 1, "unit": "count",
         "note": "Yantra4D strap-end-tip (see notion.hardware_ref); its strap channel "
                 f"takes the same {strap_width:.0f} mm strap. The tip is what stops a "
                 "leather strap end from curling and fraying."},
        {"item": "base stiffener", "qty": 1, "unit": "count",
         "note": f"≈ {base_diameter:.0f} mm disc so the bucket stands up when empty."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "ease the wall to the base around the whole rim; notch at centre front."},
    ]
    pattern.metadata = {
        "fc300_rank": 208,
        "family": "bags_luggage",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"base_diameter": round(base_diameter, 1),
                        "top_diameter": round(base_diameter + top_flare, 1),
                        "height": round(bag_height, 1)},
        "solved": {
            "base_polygon_sides": SIDES,
            "base_perimeter_mm": round(BASE_PERIMETER, 2),
            "true_circle_mm": round(2.0 * math.pi * R_BASE, 2),
            "top_perimeter_mm": round(TOP_PERIMETER, 2),
            "note": "the body's base edge = the MEASURED 48-gon base perimeter, and the "
                    "casing = the body's MEASURED flared top edge. The wall is a "
                    "trapezoid because of the flare, not a rectangle.",
        },
        "hardware": "strap end tip via Yantra4D (notion.hardware_ref -> strap-end-tip); "
                    "the tip's strap channel and the strap share strap_width",
    }
    return pattern


result = build()
