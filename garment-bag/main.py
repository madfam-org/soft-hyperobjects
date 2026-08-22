"""
Garment Bag — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #253, Yantra4D-bridged zipper).

The hanging garment bag: a suit or dress travels on its own hanger inside a shaped
sleeve that zips down the centre front. FRONT is cut in two mirrored halves so the
zipper runs between them; BACK is one whole panel; a shaped SHOULDER yoke caps the top
and carries the hanger-hook slot; a GUSSET strip walks the whole side-and-bottom
perimeter to give the bag depth for a jacket's shoulders.

Drafting note — the seam that must SOLVE: the shoulder yoke's two sloped edges are
NOT straight lines; they are the same sloped-shoulder polyline the front and back panels
carry at their tops. Rather than assume `hypot(dx, dy)`, the yoke edge is built from the
SAME point list as the panel edge and both are MEASURED, so `yoke.slope_l ↔ front.top`
matches to the tolerance the runner enforces. The gusset's length is likewise the summed
MEASURED perimeter of the back panel's side+hem edges, doubled for the two sides.

Pieces:
  - front    : half front (cut 2, mirrored) — the zip edge is `centre_front`.
  - back     : whole back panel (cut 1).
  - yoke     : shoulder cap carrying the hanger-hook slot (cut 2 — one each face).
  - gusset   : depth strip walking the side/hem perimeter (cut 2, one per side).

Hardware: the centre-front zipper bridges to Yantra4D `zipper` (notion.hardware_ref);
the zipper's `zip_length` flange dimension is driven by this bag's `bag_length`, the
same parameter that drives the garment's own `zip_tape` interface.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|yoke|gusset|set

bag_length = float(PARAM(lambda: bag_length, 1400.0))     # hook slot to hem
bag_width = float(PARAM(lambda: bag_width, 600.0))        # widest point across
shoulder_width = float(PARAM(lambda: shoulder_width, 190.0))  # flat top of the yoke
bag_depth = float(PARAM(lambda: bag_depth, 100.0))        # gusset width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_length = max(600.0, min(bag_length, 1900.0))
bag_width = max(400.0, min(bag_width, 800.0))
shoulder_width = max(100.0, min(shoulder_width, 300.0))
bag_depth = max(40.0, min(bag_depth, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The yoke must be narrower than the body, or there is no shoulder slope to draft.
shoulder_width = min(shoulder_width, bag_width - 80.0)

HALF_W = bag_width / 2.0
HALF_SH = shoulder_width / 2.0
SLOPE_SEGS = 16          # the sloped shoulder is a measured polyline, not a formula
SLOPE_DROP = min(220.0, bag_length * 0.16)   # vertical fall of the shoulder slope


def _shoulder_slope(x0, y0, x1, y1, n=SLOPE_SEGS):
    """The shoulder slope as a gently domed polyline from (x0,y0) to (x1,y1).

    A garment bag's shoulder is not a straight bevel — it bows out over the hanger
    ends. The bow is a half-sine bulge normal to the chord; both the panel and the
    yoke are built from THIS list, so their measured lengths agree exactly.
    """
    dx, dy = x1 - x0, y1 - y0
    chord = math.hypot(dx, dy)
    # unit normal to the chord
    nx, ny = (-dy / chord, dx / chord) if chord > 1e-9 else (0.0, 1.0)
    bulge = chord * 0.10
    pts = []
    for i in range(n + 1):
        t = i / n
        bow = bulge * math.sin(math.pi * t)
        pts.append(fc.P(x0 + dx * t + nx * bow, y0 + dy * t + ny * bow))
    return pts


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# Right-hand shoulder slope, drafted once in body coordinates and reused everywhere.
# Origin at hem centre; +y up. Shoulder top at y = bag_length.
_SLOPE_R = _shoulder_slope(HALF_SH, bag_length, HALF_W, bag_length - SLOPE_DROP)
SLOPE_LEN = _poly_len(_SLOPE_R)


def _mirror_x(pts):
    return [fc.P(-p.x, p.y) for p in pts]


def build_front():
    """Half front (cut 2 mirrored). `centre_front` is the zip edge; `top` is the
    shoulder slope shared with the yoke; `side` and `hem` take the gusset."""
    top = bag_length
    slope = _SLOPE_R                      # from (HALF_SH, top) out to (HALF_W, top-drop)
    pts_side = [fc.P(HALF_W, top - SLOPE_DROP), fc.P(HALF_W, 0.0)]
    edges = [
        # centre front runs bottom-to-top at x = 0: the zipper lives here.
        fc.Edge("centre_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top))]),
        # flat shoulder ledge from CF out to the yoke corner
        fc.Edge("shoulder_flat", [fc.Line(fc.P(0.0, top), fc.P(HALF_SH, top))]),
        fc.Edge("top", _lines(slope)),
        fc.Edge("side", _lines(pts_side)),
        fc.Edge("hem", [fc.Line(fc.P(HALF_W, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("hanger-hook-slot",
                    [fc.P(0.0, top - 26.0), fc.P(0.0, top - 6.0)],
                    kind="marking"),
        fc.Internal("id-window",
                    [fc.P(HALF_W * 0.30, top * 0.72), fc.P(HALF_W * 0.85, top * 0.72),
                     fc.P(HALF_W * 0.85, top * 0.62), fc.P(HALF_W * 0.30, top * 0.62),
                     fc.P(HALF_W * 0.30, top * 0.72)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("centre_front", 0.5, "zip midpoint"),
                 fc.Notch("side", 0.5, "gusset midpoint"),
                 fc.Notch("top", 0.0, "yoke corner")],
        grainline=fc.Grainline(fc.P(HALF_W * 0.5, 60.0), fc.P(HALF_W * 0.5, top - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front half (zip edge)",
    )


def build_back():
    """Whole back panel: two mirrored half-fronts joined at CF, no zip."""
    top = bag_length
    # _SLOPE_R runs (HALF_SH, top) → (HALF_W, top-drop). Walking the back CCW from
    # the hem we need it reversed on the right, and the plain mirror on the left.
    slope_r_up = list(reversed(_SLOPE_R))              # (HALF_W, top-drop) → (HALF_SH, top)
    slope_l_down = _mirror_x(_SLOPE_R)                 # (-HALF_SH, top) → (-HALF_W, top-drop)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-HALF_W, 0.0), fc.P(HALF_W, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(HALF_W, 0.0), fc.P(HALF_W, top - SLOPE_DROP))]),
        fc.Edge("top_r", _lines(slope_r_up)),
        fc.Edge("shoulder_flat", [fc.Line(fc.P(HALF_SH, top), fc.P(-HALF_SH, top))]),
        fc.Edge("top_l", _lines(slope_l_down)),
        fc.Edge("side_l", [fc.Line(fc.P(-HALF_W, top - SLOPE_DROP), fc.P(-HALF_W, 0.0))]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hem", 0.5, "centre back"),
                 fc.Notch("side_r", 0.5, "gusset midpoint"),
                 fc.Notch("side_l", 0.5, "gusset midpoint")],
        grainline=fc.Grainline(fc.P(0.0, 60.0), fc.P(0.0, top - 60.0)),
        internals=[fc.Internal("hanger-hook-slot",
                               [fc.P(-12.0, top - 16.0), fc.P(12.0, top - 16.0)],
                               kind="drill")],
        cut=fc.CutSpec(quantity=1),
        label="Back panel (whole)",
    )


def build_yoke():
    """Shoulder cap (cut 2): its two sloped edges are the SAME polyline the panels
    carry, so the seams solve by measurement rather than by trigonometric guess."""
    top = bag_length
    base_y = top - SLOPE_DROP - 40.0          # yoke drops 40 mm past the slope end
    slope_r = _SLOPE_R                                  # (HALF_SH, top) → (HALF_W, top-drop)
    slope_l = list(reversed(_mirror_x(_SLOPE_R)))        # (-HALF_W, top-drop) → (-HALF_SH, top)
    edges = [
        fc.Edge("crown", [fc.Line(fc.P(-HALF_SH, top), fc.P(HALF_SH, top))]),
        fc.Edge("slope_r", _lines(slope_r)),
        fc.Edge("drop_r", [fc.Line(fc.P(HALF_W, top - SLOPE_DROP), fc.P(HALF_W, base_y))]),
        fc.Edge("base", [fc.Line(fc.P(HALF_W, base_y), fc.P(-HALF_W, base_y))]),
        fc.Edge("drop_l", [fc.Line(fc.P(-HALF_W, base_y), fc.P(-HALF_W, top - SLOPE_DROP))]),
        fc.Edge("slope_l", _lines(slope_l)),
    ]
    return fc.Piece(
        "yoke",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown", 0.5, "hook slot centre"),
                 fc.Notch("base", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, base_y + 20.0), fc.P(0.0, top - 10.0)),
        internals=[fc.Internal("hook-slot",
                               [fc.P(-14.0, top - 18.0), fc.P(14.0, top - 18.0)],
                               kind="drill")],
        cut=fc.CutSpec(quantity=2),
        label="Shoulder yoke (hook slot)",
    )


# Gusset length = the MEASURED perimeter the back's side+hem edges present, per side.
_BACK_SIDE = bag_length - SLOPE_DROP
_HALF_HEM = HALF_W
GUSSET_RUN = _BACK_SIDE + _HALF_HEM          # one side down and half the hem across


def build_gusset():
    """Depth strip (cut 2): each runs one side seam and half the hem."""
    ln, w = GUSSET_RUN, bag_depth
    return fc.Piece(
        "gusset",
        [
            fc.Edge("seam_back", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_hem", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("seam_front", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_top", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("seam_back", _BACK_SIDE / ln, "hem corner"),
                 fc.Notch("seam_front", 1.0 - _BACK_SIDE / ln, "hem corner")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Side/hem gusset",
    )


def build():
    pattern = fc.PatternSet("garment-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "yoke":
        pattern.add(build_yoke())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())

    if all_pieces:
        # The solving seams: the yoke's slopes sew to the panels' slopes.
        pattern.declare_seam(("yoke", "slope_r"), ("front", "top"), tol=1.0)
        pattern.declare_seam(("yoke", "slope_l"), ("back", "top_l"), tol=1.0)
        # The yoke crown matches the front pair's flat shoulders and the back's flat.
        pattern.declare_seam(("yoke", "crown"),
                             [("front", "shoulder_flat"), ("front", "shoulder_flat")],
                             tol=1.0)
        pattern.declare_seam(("yoke", "crown"), ("back", "shoulder_flat"), tol=1.0)
        # The two gussets together walk both back sides plus the whole back hem —
        # the summed-sides form of the check, so no fudge factor is needed.
        pattern.declare_seam([("gusset", "seam_back"), ("gusset", "seam_back")],
                             [("back", "side_r"), ("back", "side_l"), ("back", "hem")],
                             tol=1.0)
        # And the same pair walks the two front halves' sides plus their two hems.
        pattern.declare_seam([("gusset", "seam_front"), ("gusset", "seam_front")],
                             [("front", "side"), ("front", "side"),
                              ("front", "hem"), ("front", "hem")],
                             tol=1.0)
        # Both front halves' centre-front edges are the zip: they mirror each other.
        pattern.declare_seam(("front", "centre_front"), ("front", "centre_front"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "breathable shell (nylon ripstop or cotton canvas)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker. Do NOT use unvented PVC — "
                 "wool needs to breathe or it moulds in storage."},
        {"item": "separating zipper", "qty": 1, "unit": "count",
         "note": f"≈ {bag_length:.0f} mm; Yantra4D `zipper` (notion.hardware_ref) "
                 f"is driven by the same bag_length."},
        {"item": "clear vinyl or mesh window", "qty": 1, "unit": "count",
         "note": "for the marked id-window; mesh keeps the bag breathable."},
        {"item": "polyester thread", "qty": 1, "unit": "spool",
         "note": "bind the hook slot; it carries the whole loaded bag."},
    ]
    pattern.metadata = {
        "fc300_rank": 253,
        "family": "care_and_keeping",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"length": round(bag_length, 1),
                        "width": round(bag_width, 1),
                        "depth": round(bag_depth, 1)},
        "solved": {
            "shoulder_slope_segments": SLOPE_SEGS,
            "slope_measured_mm": round(SLOPE_LEN, 2),
            "slope_chord_mm": round(math.hypot(HALF_W - HALF_SH, SLOPE_DROP), 2),
            "gusset_run_mm": round(GUSSET_RUN, 2),
            "note": "the yoke's sloped edges are built from the SAME bowed polyline "
                    "as the panels' tops, so the seam matches by measurement — the "
                    "bowed slope is ~%.1f mm longer than its chord."
                    % (SLOPE_LEN - math.hypot(HALF_W - HALF_SH, SLOPE_DROP)),
        },
        "hardware": "centre-front separating zip via Yantra4D "
                    "(notion.hardware_ref -> zipper); zip_length = bag_length",
    }
    return pattern


result = build()
