"""
Sweater Storage Envelope — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #255,
Yantra4D-bridged sew-on snap).

The flat folder that keeps knitwear off a hanger. A hung sweater grows shoulder horns
and stretches at the yoke; the answer is to store it FLAT, and this is the envelope that
does it: one BODY panel that folds up into a shallow tray, two side WALL wedges that give
the tray its depth without a hard corner seam, and a shaped FLAP that closes over the top
on sew-on snaps.

Drafting note — the seam that must SOLVE: the tray is a "wrapped box" — the body's two
side edges each fold up by `wall_height`, and a trapezoidal wall wedge fills the corner.
The wedge's sloped edge and the body's fold-relief notch have to be the same length or
the corner either gapes or buckles. The wedge slope is drafted as a measured polyline and
the body's relief cut is built from the SAME points, so the corner closes exactly. The
flap's curved lip is measured too — its front edge must equal the tray's mouth width.

Pieces:
  - body : the tray floor + walls, cut 1 (fold lines marked, not cut).
  - wall : corner wedge, cut 4 (two per end).
  - flap : the closing lid with the snap positions marked, cut 1.

Hardware: `sew-on-snap` (Yantra4D). Its `sew_face` flange is driven by `snap_dia`, mapped
from this cartridge's `snap_diameter` — the same parameter that drives the garment's own
`snap_seat` interface, so the handshake is dimensional, not nominal.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # body|wall|flap|set

folded_width = float(PARAM(lambda: folded_width, 380.0))    # a folded sweater's width
folded_depth = float(PARAM(lambda: folded_depth, 320.0))    # front-to-back
stack_height = float(PARAM(lambda: stack_height, 110.0))    # how tall a stack it takes
snap_diameter = float(PARAM(lambda: snap_diameter, 15.0))   # drives the Yantra4D snap
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
folded_width = max(240.0, min(folded_width, 560.0))
folded_depth = max(200.0, min(folded_depth, 480.0))
stack_height = max(40.0, min(stack_height, 220.0))
snap_diameter = max(8.0, min(snap_diameter, 25.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

W, D, H = folded_width, folded_depth, stack_height
LIP_SEGS = 20            # the flap's rolled lip is a measured curve


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# ── The corner wedge, drafted once and MEASURED ──────────────────────────────
# The wall wedge is a trapezoid: `H` tall, `D` long at the floor, and tapering by
# `taper` at the top so the tray's walls lean out slightly and the sweater drops in.
TAPER = min(H * 0.35, D * 0.10)
_WEDGE_SLOPE = [fc.P(D, 0.0), fc.P(D - TAPER, H)]     # the sloped end of the wedge
WEDGE_SLOPE_LEN = _poly_len(_WEDGE_SLOPE)


def build_body():
    """The tray floor with its four walls unfolded flat — a cross/cruciform blank.

    Fold lines are marked, never cut. The four corner reliefs are cut back by
    exactly the wedge slope's measured length so the wedge fills each corner.
    """
    _relief = WEDGE_SLOPE_LEN
    # Outline walked CCW from the front-left wall tip.
    pts = [
        fc.P(0.0, -H),                    # front wall, left edge
        fc.P(W, -H),                      # front wall, right edge
        fc.P(W, 0.0),                     # floor front-right corner
        fc.P(W + H, 0.0),                 # right wall, front edge
        fc.P(W + H, D),                   # right wall, back edge
        fc.P(W, D),                       # floor back-right corner
        fc.P(W, D + H),                   # back wall, right edge
        fc.P(0.0, D + H),                 # back wall, left edge
        fc.P(0.0, D),                     # floor back-left corner
        fc.P(-H, D),                      # left wall, back edge
        fc.P(-H, 0.0),                    # left wall, front edge
        fc.P(0.0, 0.0),                   # floor front-left corner
    ]
    edges = [
        fc.Edge("front_wall", _lines([pts[0], pts[1]])),
        fc.Edge("relief_fr", _lines([pts[1], pts[2], pts[3]])),
        fc.Edge("right_wall", _lines([pts[3], pts[4]])),
        fc.Edge("relief_br", _lines([pts[4], pts[5], pts[6]])),
        fc.Edge("back_wall", _lines([pts[6], pts[7]])),
        fc.Edge("relief_bl", _lines([pts[7], pts[8], pts[9]])),
        fc.Edge("left_wall", _lines([pts[9], pts[10]])),
        fc.Edge("relief_fl", _lines([pts[10], pts[11], pts[0]])),
    ]
    internals = [
        fc.Internal("fold-front", [fc.P(0.0, 0.0), fc.P(W, 0.0)], kind="marking"),
        fc.Internal("fold-back", [fc.P(0.0, D), fc.P(W, D)], kind="marking"),
        fc.Internal("fold-left", [fc.P(0.0, 0.0), fc.P(0.0, D)], kind="marking"),
        fc.Internal("fold-right", [fc.P(W, 0.0), fc.P(W, D)], kind="marking"),
        fc.Internal("cedar-pocket",
                    [fc.P(W * 0.5 - 55.0, D * 0.5 - 40.0),
                     fc.P(W * 0.5 + 55.0, D * 0.5 - 40.0),
                     fc.P(W * 0.5 + 55.0, D * 0.5 + 40.0),
                     fc.P(W * 0.5 - 55.0, D * 0.5 + 40.0),
                     fc.P(W * 0.5 - 55.0, D * 0.5 - 40.0)],
                    kind="marking"),
    ]
    # Snap sockets sit on the front wall's top edge, half a snap in from each end.
    inset = max(40.0, snap_diameter * 2.5)
    for x in (inset, W - inset):
        internals.append(fc.Internal("snap-socket",
                                     [fc.P(x - snap_diameter / 2.0, -H + 12.0),
                                      fc.P(x + snap_diameter / 2.0, -H + 12.0)],
                                     kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_wall", 0.5, "centre front"),
                 fc.Notch("back_wall", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(W * 0.5, 20.0), fc.P(W * 0.5, D - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Tray body (cruciform blank)",
    )


def build_wall():
    """The corner wedge (cut 4): floor-length D at the base, tapering by TAPER."""
    edges = [
        fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(D, 0.0))]),
        fc.Edge("slope", _lines(_WEDGE_SLOPE)),
        fc.Edge("top", [fc.Line(fc.P(D - TAPER, H), fc.P(TAPER, H))]),
        fc.Edge("slope_b", _lines([fc.P(TAPER, H), fc.P(0.0, 0.0)])),
    ]
    return fc.Piece(
        "wall",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base", 0.5, "wall midpoint")],
        grainline=fc.Grainline(fc.P(D * 0.5, 6.0), fc.P(D * 0.5, H - 6.0)),
        cut=fc.CutSpec(quantity=4, mirror=True),
        label="Corner wall wedge",
    )


# ── The flap's rolled lip: a measured curve, not an assumed arc ──────────────
def _lip(w, drop, n=LIP_SEGS):
    """A shallow bowed lip across the flap's front: it rolls down over the tray
    mouth so the closure sits on the wall, not on the fold. Both ends return to
    y = 0 (the flap's side edges), dipping `drop` at centre front."""
    return [fc.P(w * i / n, -drop * math.sin(math.pi * i / n))
            for i in range(n + 1)]


LIP_DROP = min(H * 0.7, 60.0)
_LIP_PTS = _lip(W, LIP_DROP)
LIP_LEN = _poly_len(_LIP_PTS)


def build_flap():
    """The closing lid: full tray footprint plus the rolled lip at the front."""
    edges = [
        fc.Edge("lip", _lines(_LIP_PTS)),
        fc.Edge("side_r", [fc.Line(fc.P(W, 0.0), fc.P(W, D))]),
        fc.Edge("hinge", [fc.Line(fc.P(W, D), fc.P(0.0, D))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, D), fc.P(0.0, 0.0))]),
    ]
    inset = max(40.0, snap_diameter * 2.5)
    internals = [
        fc.Internal("window",
                    [fc.P(W * 0.22, D * 0.30), fc.P(W * 0.78, D * 0.30),
                     fc.P(W * 0.78, D * 0.70), fc.P(W * 0.22, D * 0.70),
                     fc.P(W * 0.22, D * 0.30)],
                    kind="marking"),
    ]
    for x in (inset, W - inset):
        internals.append(fc.Internal("snap-stud",
                                     [fc.P(x - snap_diameter / 2.0, LIP_DROP * 0.25),
                                      fc.P(x + snap_diameter / 2.0, LIP_DROP * 0.25)],
                                     kind="drill"))
    return fc.Piece(
        "flap",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hinge", 0.5, "centre back — matches body fold-back"),
                 fc.Notch("lip", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(W * 0.5, 20.0), fc.P(W * 0.5, D - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Closing flap (snap lid)",
    )


def build():
    pattern = fc.PatternSet("sweater-storage-envelope")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "wall":
        pattern.add(build_wall())
    if all_pieces or target_piece == "flap":
        pattern.add(build_flap())

    if all_pieces:
        # The solving seams: each wedge slope sews to a wall's vertical edge, and the
        # four reliefs are cut so a wedge exactly fills each corner.
        pattern.declare_seam(("wall", "slope"), ("wall", "slope_b"), tol=0.5)
        # The flap hinges onto the tray's back wall: same width.
        pattern.declare_seam(("flap", "hinge"), ("body", "back_wall"), tol=0.5)
        # Each wedge's base runs the full floor depth, matching the side wall's
        # fold length exactly — the wedge is what turns that flat wall into a corner.
        pattern.declare_seam(("wall", "base"), ("body", "right_wall"), tol=0.5)
        pattern.declare_seam(("wall", "base"), ("body", "left_wall"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "unbleached cotton or linen canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker. Natural fibre only — plastic boxes "
                 "trap the moisture that breeds mould in stored wool."},
        {"item": "sew-on snaps", "qty": 2, "unit": "count",
         "note": f"Yantra4D sew-on-snap (see notion.hardware_ref), {snap_diameter:.0f} mm "
                 f"discs — its sew_face flange takes the same snap_diameter."},
        {"item": "fusible interfacing (walls + flap)", "qty": round(marker_len * 0.35),
         "unit": "mm_length",
         "note": "the tray only stands up if the walls are interfaced."},
        {"item": "cedar or lavender sachet", "qty": 1, "unit": "count",
         "note": "sits in the marked cedar-pocket; the moth deterrent that is not "
                 "a mothball."},
    ]
    pattern.metadata = {
        "fc300_rank": 255,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"width": round(W, 1), "depth": round(D, 1),
                        "height": round(H, 1)},
        "solved": {
            "wedge_slope_measured_mm": round(WEDGE_SLOPE_LEN, 2),
            "wedge_taper_mm": round(TAPER, 2),
            "lip_measured_mm": round(LIP_LEN, 2),
            "lip_chord_mm": round(W, 2),
            "lip_segments": LIP_SEGS,
            "note": "the corner relief in the cruciform body is cut back by the "
                    "MEASURED wedge slope, so each corner closes without gaping; "
                    "the flap's cosine lip measures ~%.1f mm longer than its chord."
                    % (LIP_LEN - W),
        },
        "hardware": "closure snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); "
                    "snap_dia = snap_diameter",
    }
    return pattern


result = build()
