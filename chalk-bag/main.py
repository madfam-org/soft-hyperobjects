"""
Chalk Bag — Fashion Cabinet Accessory Cartridge (FC-300 #236, technical & outdoor).

The climber's chalk bag: a stiff cylinder worn at the small of the back, lined with
fleece so chalk clings and releases, with a rolled fleece cuff at the mouth that keeps
the dust in and a drawcord through a top casing that a cord-lock pinches shut between
climbs. A brush loop and a belt loop finish it.

The cord-lock solid is Yantra4D territory (`cord-lock`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the bag — the cylinder that unrolls from
the mouth diameter, the base disc, the fleece cuff depth, the casing.

The base is a true circle drafted as a 48-segment polygon (the house rule for circular
pieces), and its circumference is the SOLVED mating run of the body's base edge — the
seam is declared and verifies, so the disc really does sew into the tube.

Pieces:
  - body  : the cylinder wall, unrolled (one rectangle; the join is a self-seam).
  - base  : the circular bottom disc (48-segment polygon).
  - cuff  : the fleece mouth cuff, unrolled.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # body|base|cuff|set

mouth_dia    = float(PARAM(lambda: mouth_dia, 130.0))     # inside diameter at the mouth
bag_depth    = float(PARAM(lambda: bag_depth, 175.0))     # mouth to base
cuff_depth   = float(PARAM(lambda: cuff_depth, 55.0))     # rolled fleece cuff
casing_depth = float(PARAM(lambda: casing_depth, 22.0))   # drawcord casing at the mouth
cord_dia     = float(PARAM(lambda: cord_dia, 4.0))        # drawcord diameter
belt_loop_w  = float(PARAM(lambda: belt_loop_w, 45.0))    # belt loop width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
mouth_dia    = max(90.0, min(mouth_dia, 190.0))
bag_depth    = max(110.0, min(bag_depth, 260.0))
cuff_depth   = max(25.0, min(cuff_depth, 90.0))
casing_depth = max(12.0, min(casing_depth, 40.0))
cord_dia     = max(2.0, min(cord_dia, 8.0))
belt_loop_w  = max(25.0, min(belt_loop_w, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGMENTS = 48                     # the house polygon resolution for circular pieces
R = mouth_dia / 2.0               # base/mouth radius (a straight cylinder)


def _circle_points(radius, segments=SEGMENTS):
    """A closed circle as a `segments`-gon, centred on the origin (house rule)."""
    return [fc.P(radius * math.cos(2.0 * math.pi * i / segments),
                 radius * math.sin(2.0 * math.pi * i / segments))
            for i in range(segments)]


def _polygon_perimeter(radius, segments=SEGMENTS):
    """The measured run of the `segments`-gon — the value the wall must be SOLVED to,
    not the ideal circle 2πr (which the polygon under-runs by ~0.14%)."""
    return 2.0 * segments * radius * math.sin(math.pi / segments)


# The wall length is solved to the polygon base's true perimeter, so the declared
# base seam verifies instead of drifting by the polygon deficit.
WALL_RUN = _polygon_perimeter(R)
WALL_H = bag_depth


def build_body():
    """The cylinder wall, unrolled flat. `base_edge` is the run that sews to the disc."""
    internals = [
        fc.Internal("casing-line",
                    [fc.P(0.0, WALL_H - casing_depth), fc.P(WALL_RUN, WALL_H - casing_depth)],
                    kind="marking"),
        fc.Internal("belt-loop-place",
                    [fc.P(WALL_RUN * 0.5 - belt_loop_w / 2.0, WALL_H * 0.62),
                     fc.P(WALL_RUN * 0.5 + belt_loop_w / 2.0, WALL_H * 0.62)],
                    kind="marking"),
        fc.Internal("brush-loop-place",
                    [fc.P(WALL_RUN * 0.5 - 15.0, WALL_H * 0.30),
                     fc.P(WALL_RUN * 0.5 + 15.0, WALL_H * 0.30)],
                    kind="marking"),
    ]
    return fc.Piece(
        "body",
        [
            fc.Edge("join", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WALL_H))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, WALL_H), fc.P(WALL_RUN, WALL_H))]),
            fc.Edge("join_b", [fc.Line(fc.P(WALL_RUN, WALL_H), fc.P(WALL_RUN, 0.0))]),
            fc.Edge("base_edge", [fc.Line(fc.P(WALL_RUN, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": casing_depth},
        notches=[fc.Notch("base_edge", 0.25, "base quarter"),
                 fc.Notch("base_edge", 0.5, "base half"),
                 fc.Notch("base_edge", 0.75, "base three-quarter")],
        grainline=fc.Grainline(fc.P(WALL_RUN * 0.5, 20.0), fc.P(WALL_RUN * 0.5, WALL_H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cylinder wall",
    )


def build_base():
    """The circular bottom disc: a 48-segment polygon whose perimeter is the wall run."""
    pts = _circle_points(R)
    segs = [fc.Line(pts[i], pts[(i + 1) % SEGMENTS]) for i in range(SEGMENTS)]
    return fc.Piece(
        "base",
        [fc.Edge("rim", segs)],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim", 0.25, "quarter"), fc.Notch("rim", 0.5, "half"),
                 fc.Notch("rim", 0.75, "three-quarter")],
        grainline=fc.Grainline(fc.P(-R * 0.6, 0.0), fc.P(R * 0.6, 0.0)),
        cut=fc.CutSpec(quantity=1),
        label="Base disc",
    )


def build_cuff():
    """The fleece mouth cuff, unrolled — the same run as the wall's mouth."""
    return fc.Piece(
        "cuff",
        [
            fc.Edge("join", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, cuff_depth))]),
            fc.Edge("free", [fc.Line(fc.P(0.0, cuff_depth), fc.P(WALL_RUN, cuff_depth))]),
            fc.Edge("join_b", [fc.Line(fc.P(WALL_RUN, cuff_depth), fc.P(WALL_RUN, 0.0))]),
            fc.Edge("attach", [fc.Line(fc.P(WALL_RUN, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "cuff half")],
        grainline=fc.Grainline(fc.P(WALL_RUN * 0.5, 6.0), fc.P(WALL_RUN * 0.5, cuff_depth - 6.0)),
        cut=fc.CutSpec(quantity=1),
        label="Fleece mouth cuff",
    )


def build():
    pattern = fc.PatternSet("chalk-bag")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "base":
        pattern.add(build_base())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything:
        # The wall's base run sews to the disc rim — SOLVED to the polygon perimeter,
        # so the check is a real dimensional proof, not a tolerance.
        pattern.declare_seam(("body", "base_edge"), ("base", "rim"), tol=1.0)
        # The fleece cuff sews into the mouth on the same run.
        pattern.declare_seam(("cuff", "attach"), ("body", "mouth"), tol=1.0)
        # The wall closes on itself: join to its own opposite join (never to a fold).
        pattern.declare_seam(("body", "join"), ("body", "join_b"), tol=1.0)
        pattern.declare_seam(("cuff", "join"), ("cuff", "join_b"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "packcloth / cordura shell",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; stiffen the wall with foam or a rolled rim."},
        {"item": "pile fleece lining + cuff", "qty": 1, "unit": "set",
         "note": "the pile holds and releases chalk; the rolled cuff keeps the dust in."},
        {"item": "drawcord + cord-lock", "qty": 1, "unit": "set",
         "note": "Yantra4D cord-lock (see notion.hardware_ref) pinches the mouth shut."},
        {"item": "webbing belt loop + brush loop", "qty": 1, "unit": "set",
         "note": "belt loop at the back, brush loop below it."},
    ]
    pattern.metadata = {
        "fc300_rank": 236, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A stiff fleece-lined cylinder worn at the small of the back: the "
            "wall unrolls from the mouth diameter, the base is a true 48-gon disc solved to the "
            "wall run, and a drawcord through the mouth casing is pinched by a cord-lock.",
        "solved": {"wall_run_mm": round(WALL_RUN, 2), "base_radius_mm": round(R, 2),
                   "polygon_segments": SEGMENTS, "wall_height_mm": round(WALL_H, 1)},
        "hardware": "drawcord stopper via Yantra4D (notion.hardware_ref -> cord-lock)",
    }
    return pattern


result = build()
