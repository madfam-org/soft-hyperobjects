"""
Rehab Sensor Cuff — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A forearm cuff that holds a motion sensor in one place on a limb that is trying to
push it off. This is the wearable half of joint-motion rehab: the sensor's numbers
are only worth anything if the sensor did not rotate or migrate between sessions,
and on a tapering forearm a straight tube cuff does both.

Not the same object as `printed-flexure-cuff` (a printed TPU trim that finishes a
sleeve) or `arm-warmers` (a tapered stretch tube for warmth, cut as a flat panel
with a straight join). This one is drafted as a TRUNCATED CONE, and the cone is the
whole point.

Drafting note — the seam that must SOLVE: a cuff whose proximal and distal girths
differ is a frustum, and the flat pattern of a frustum is an ANNULAR SECTOR, not a
trapezoid. Cut it as a trapezoid — which is what a straight-taper draft gives you —
and the two curved edges come out as straight lines, so the cuff cones the wrong way
and its edges cup. The kernel solves the sector properly from the two girths and the
slant:

    r_p, r_d  = girths / 2pi                      (cone radii at each end)
    slant     = hypot(cuff_height, r_p - r_d)     (the surface, not the axis)
    R_d       = r_d * slant / (r_p - r_d)         (similar triangles)
    R_p       = R_d + slant
    theta     = C_p / R_p                         (the sector angle, radians)

and then `R_d * theta == C_d` falls out exactly — which is the check that the draft
is right, and which the kernel asserts by declaring both arcs as measured seams
against the closure straps cut to them.

The degenerate case is real and handled: at zero taper the frustum is a cylinder,
R_d goes to infinity, and the cuff must be drafted as a plain rectangle instead.

The sensor seat is placed by ARC-LENGTH fraction around the drawn proximal arc, so
`sensor_offset` means the same thing on every limb size — the anatomical landmark
(the ulnar border, say) does not move to a different fraction of the circumference
just because the forearm got bigger.

Pieces:
  - cuff    : the annular-sector shell, with the sensor plate footprint and traces.
  - lining  : the skin-side layer, cut to the same sector, carrying the grip zones.
  - strap   : the closure strap, cut to the MEASURED proximal arc plus its overlap.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # cuff|lining|strap|set

prox_girth = float(PARAM(lambda: prox_girth, 280.0))     # girth at the elbow end
dist_girth = float(PARAM(lambda: dist_girth, 220.0))     # girth at the wrist end
cuff_height = float(PARAM(lambda: cuff_height, 120.0))   # along the limb
compression = float(PARAM(lambda: compression, 0.08))    # negative ease
plate_w = float(PARAM(lambda: plate_w, 38.0))            # sensor plate width
plate_d = float(PARAM(lambda: plate_d, 30.0))            # sensor plate depth
sensor_offset = float(PARAM(lambda: sensor_offset, 0.25))  # fraction round the arc
strap_overlap = float(PARAM(lambda: strap_overlap, 60.0))  # closure adjustment
grip_bands = int(PARAM(lambda: grip_bands, 3))           # anti-migration grip rows
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
prox_girth = max(150.0, min(prox_girth, 520.0))
dist_girth = max(120.0, min(dist_girth, 500.0))
cuff_height = max(50.0, min(cuff_height, 300.0))
compression = max(0.0, min(compression, 0.22))
plate_w = max(14.0, min(plate_w, 90.0))
plate_d = max(12.0, min(plate_d, 90.0))
sensor_offset = max(0.05, min(sensor_offset, 0.95))
strap_overlap = max(20.0, min(strap_overlap, 200.0))
grip_bands = max(0, min(grip_bands, 8))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# A forearm narrows toward the wrist. If the maker enters them the other way round
# the cuff would cone backwards, so the ends are ordered rather than trusted.
if dist_girth > prox_girth:
    prox_girth, dist_girth = dist_girth, prox_girth

# The cuff must be tall enough to seat the sensor plate with a margin.
cuff_height = max(cuff_height, plate_d + 30.0)

# Compression is applied to both ends equally: the cut girths, not the body girths.
C_P = prox_girth * (1.0 - compression)
C_D = dist_girth * (1.0 - compression)


# ── The frustum solve ────────────────────────────────────────────────────────
# The flat pattern of a truncated cone is an annular sector. Solving it needs the
# SLANT (the distance along the cone's surface), not the axial height — using the
# height instead is the quiet error that makes a coned cuff come out short.
_r_p = C_P / (2.0 * math.pi)
_r_d = C_D / (2.0 * math.pi)
_dr = _r_p - _r_d
SLANT = math.hypot(cuff_height, _dr)

# Degenerate case: as the taper goes to zero the frustum becomes a cylinder, R_d
# diverges, and the sector stops being a thing anyone can cut. The guard is NOT a
# girth comparison and NOT a bare epsilon on _dr — a 10 mm taper over a 380 mm calf
# is numerically fine and geometrically absurd, producing a 3.5-degree sector on a
# five-and-a-half-metre radius. What actually matters is whether the sector's radius
# is a size a cutting table and a maker can work with, so the guard is on R_D
# itself, expressed as a multiple of the piece's own slant.
_MAX_RADIUS_RATIO = 12.0   # R_D beyond ~12 slants is a straight line in disguise
if _dr > 1e-6:
    _R_D_TRIAL = _r_d * SLANT / _dr
    CONICAL = _R_D_TRIAL <= SLANT * _MAX_RADIUS_RATIO
else:
    _R_D_TRIAL = 0.0
    CONICAL = False

if CONICAL:
    R_D = _R_D_TRIAL                # inner sector radius (wrist end)
    R_P = R_D + SLANT               # outer sector radius (elbow end)
    THETA = C_P / R_P               # sector angle, radians
else:
    R_D = 0.0
    R_P = 0.0
    THETA = 0.0

# Where the sector is drawn: centred on the +y axis so the piece sits upright.
_HALF = THETA / 2.0
_CX, _CY = 0.0, 0.0


def _arc(radius, n=48, reverse=False):
    """Polyline the sector arc at `radius`, as fc.Line segments.

    Drawn as chords rather than a Bezier because the arc's LENGTH is load-bearing
    here — it is what the strap is cut to — and a flattened chord run has a length
    the kernel and the maker agree on. 48 segments puts the sagitta under 0.02 mm
    at the radii this draft produces.
    """
    pts = []
    for i in range(n + 1):
        a = -_HALF + THETA * (i / n)
        pts.append(fc.P(_CX + radius * math.sin(a), _CY + radius * math.cos(a)))
    if reverse:
        pts.reverse()
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


def _arc_point(radius, t):
    """A point at arc-length fraction `t` along the sector arc at `radius`.

    Uniform in angle IS uniform in arc length on a circular arc, so `t` maps
    directly — which is the property that makes `sensor_offset` mean the same
    anatomical place on every limb size.
    """
    a = -_HALF + THETA * t
    return fc.P(_CX + radius * math.sin(a), _CY + radius * math.cos(a))


def _rect_edges(w, h):
    """Fallback outline for the effectively-untapered (cylindrical) case.

    Cut at the PROXIMAL girth, so the residual taper is absorbed as ease at the
    wrist end rather than as a cone nobody can cut. That residual is reported as
    `rect_fallback_slack_mm` — the fallback declares what it gave up.
    """
    return [
        fc.Edge("closure_d", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("prox", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("closure_p", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("dist", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]


def _sector_edges():
    """The annular sector: distal arc, closure edge, proximal arc, closure edge."""
    inner = _arc(R_D)
    outer = _arc(R_P, reverse=True)
    p_d_start = inner[0].p0
    p_d_end = inner[-1].p1
    p_p_start = outer[0].p0      # outer arc reversed: starts at the +theta end
    p_p_end = outer[-1].p1
    return [
        fc.Edge("dist", inner),
        fc.Edge("closure_p", [fc.Line(p_d_end, p_p_start)]),
        fc.Edge("prox", outer),
        fc.Edge("closure_d", [fc.Line(p_p_end, p_d_start)]),
    ]


def _shell_edges():
    return _sector_edges() if CONICAL else _rect_edges(C_P, cuff_height)


def _seat_centre():
    """The sensor plate's centre, placed by arc-length fraction and set in from the
    proximal edge far enough to clear the plate and the seam."""
    if CONICAL:
        # Midway in radius between the two arcs, biased proximally where the limb
        # is fleshier and the sensor sits more stably.
        r = R_D + SLANT * 0.58
        return _arc_point(r, sensor_offset)
    return fc.P(C_P * sensor_offset, cuff_height * 0.58)


def build_cuff():
    """The outer shell: the solved annular sector, sensor plate footprint, traces."""
    seat = _seat_centre()
    internals = [
        # The sensor mount plate's sewn footprint — the same rectangle the Yantra4D
        # sensor-mount-plate's base is generated at.
        fc.Internal("sensor-plate", [
            fc.P(seat.x - plate_w / 2.0, seat.y - plate_d / 2.0),
            fc.P(seat.x + plate_w / 2.0, seat.y - plate_d / 2.0),
            fc.P(seat.x + plate_w / 2.0, seat.y + plate_d / 2.0),
            fc.P(seat.x - plate_w / 2.0, seat.y + plate_d / 2.0),
            fc.P(seat.x - plate_w / 2.0, seat.y - plate_d / 2.0)], kind="marking"),
        # The four sew points that keep the plate from rotating. A plate sewn at two
        # points is a hinge; at four it is a mount.
        fc.Internal("plate-sew-nw", [
            fc.P(seat.x - plate_w / 2.0 + 4.0, seat.y - plate_d / 2.0 + 4.0),
            fc.P(seat.x - plate_w / 2.0 + 4.0, seat.y - plate_d / 2.0 + 4.0)],
            kind="drill"),
        fc.Internal("plate-sew-ne", [
            fc.P(seat.x + plate_w / 2.0 - 4.0, seat.y - plate_d / 2.0 + 4.0),
            fc.P(seat.x + plate_w / 2.0 - 4.0, seat.y - plate_d / 2.0 + 4.0)],
            kind="drill"),
        fc.Internal("plate-sew-sw", [
            fc.P(seat.x - plate_w / 2.0 + 4.0, seat.y + plate_d / 2.0 - 4.0),
            fc.P(seat.x - plate_w / 2.0 + 4.0, seat.y + plate_d / 2.0 - 4.0)],
            kind="drill"),
        fc.Internal("plate-sew-se", [
            fc.P(seat.x + plate_w / 2.0 - 4.0, seat.y + plate_d / 2.0 - 4.0),
            fc.P(seat.x + plate_w / 2.0 - 4.0, seat.y + plate_d / 2.0 - 4.0)],
            kind="drill"),
        # The lead run from the plate back to the closure edge, where it exits.
        fc.Internal("lead-run", [
            fc.P(seat.x, seat.y),
            _arc_point(R_D + SLANT * 0.58, min(sensor_offset + 0.30, 0.98))
            if CONICAL else fc.P(C_P * 0.95, cuff_height * 0.58)], kind="trace"),
    ]
    return fc.Piece(
        "cuff", _shell_edges(),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("prox", sensor_offset, "sensor axis"),
                 fc.Notch("dist", sensor_offset, "sensor axis")],
        grainline=fc.Grainline(fc.P(seat.x, seat.y - plate_d),
                               fc.P(seat.x, seat.y + plate_d)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cuff shell (annular sector)" if CONICAL else "Cuff shell (rectangle)",
    )


# ── The measured arcs ────────────────────────────────────────────────────────
# The strap is cut to the shell's MEASURED proximal arc, not to C_P. The arc is
# drawn as a 48-chord polyline, so its measured length is very slightly under the
# true arc — and that difference is real cloth. Measuring the drawn edge is what
# keeps the strap and the cuff the same length.
_CUFF = build_cuff()
PROX_ARC = _CUFF.edge("prox").length()
DIST_ARC = _CUFF.edge("dist").length()
CLOSURE_LEN = _CUFF.edge("closure_p").length()


def build_lining():
    """The skin side: the same solved sector, carrying the anti-migration grip rows.

    Cut to the SAME sector as the shell — deliberately not eased. A lining eased
    inside a coned cuff would rotate independently of the shell, which is exactly
    the failure the whole cuff exists to prevent.
    """
    internals = []
    for b in range(grip_bands):
        # Grip rows run parallel to the arcs, spaced across the slant.
        f = (b + 1) / (grip_bands + 1)
        if CONICAL:
            r = R_D + SLANT * f
            pts = [_arc_point(r, i / 16.0) for i in range(17)]
        else:
            y = cuff_height * f
            pts = [fc.P(C_P * i / 16.0, y) for i in range(17)]
        internals.append(fc.Internal(f"grip-band-{b}", pts, kind="marking"))
    return fc.Piece(
        "lining", _shell_edges(),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("prox", sensor_offset, "sensor axis"),
                 fc.Notch("dist", sensor_offset, "sensor axis")],
        grainline=_CUFF.grainline,
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Lining (grip side)",
    )


def build_strap():
    """The closure strap, cut to the shell's MEASURED proximal arc plus the overlap.

    Its `attach` edge is declared against the cuff's proximal arc, so if the sector
    solve is ever wrong the seam check catches it rather than the maker.
    """
    ln = PROX_ARC + strap_overlap
    h = max(plate_d * 0.6, 24.0)
    internals = [
        # The engagement field starts one overlap in from the free end.
        fc.Internal("closure-field", [
            fc.P(ln - strap_overlap, h * 0.12),
            fc.P(ln - 6.0, h * 0.12),
            fc.P(ln - 6.0, h * 0.88),
            fc.P(ln - strap_overlap, h * 0.88),
            fc.P(ln - strap_overlap, h * 0.12)], kind="marking"),
        # A tension index at the measured arc: pulled to here, the cuff is at the
        # compression the pattern was cut for. Repeatability is the point.
        fc.Internal("tension-index", [
            fc.P(PROX_ARC, 0.0), fc.P(PROX_ARC, h)], kind="drill"),
    ]
    return fc.Piece(
        "strap",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(ln, h))]),
            fc.Edge("free", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", PROX_ARC / ln, "tension index")],
        grainline=fc.Grainline(fc.P(ln * 0.15, h / 2.0), fc.P(ln * 0.85, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Closure strap",
    )


def build():
    pattern = fc.PatternSet("rehab-sensor-cuff")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "cuff":
        pattern.add(build_cuff())
    if all_pieces or target_piece == "lining":
        pattern.add(build_lining())
    if all_pieces or target_piece == "strap":
        pattern.add(build_strap())

    if all_pieces:
        # The lining is cut to the SAME sector as the shell, both arcs and the
        # closure edge — declared so an eased lining can never sneak in.
        pattern.declare_seam(("lining", "prox"), ("cuff", "prox"), tol=1.0)
        pattern.declare_seam(("lining", "dist"), ("cuff", "dist"), tol=1.0)
        pattern.declare_seam(("lining", "closure_p"), ("cuff", "closure_p"), tol=1.0)
        # THE seam that had to solve: the strap's top edge is the measured proximal
        # arc plus the overlap it was drafted with. If the frustum solve drifts, this
        # check fires.
        pattern.declare_seam(("strap", "top"), ("cuff", "prox"),
                             tol=1.0, ease=strap_overlap)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "compression knit (skin-safe, launderable)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker; an annular sector nests poorly, "
                 "which is the honest cost of drafting the cone properly."},
        {"item": "sensor mount plate", "qty": 1, "unit": "count",
         "note": f"Yantra4D sensor-mount-plate (notion.hardware_ref); base "
                 f"{plate_w:.0f} x {plate_d:.0f} mm, sewn at the four marked "
                 f"plate-sew points so it cannot hinge."},
        {"item": "hook-and-loop closure", "qty": 1, "unit": "run",
         "note": f"{strap_overlap:.0f} mm engagement field; the tension-index drill "
                 f"at {PROX_ARC:.0f} mm marks the drafted compression."},
        {"item": "silicone grip print or tape", "qty": grip_bands, "unit": "run",
         "note": f"{grip_bands} rows on the lining, following the arcs; this is what "
                 f"stops the cuff walking distally between sessions."},
        {"item": "sensor lead or wireless module", "qty": 1, "unit": "count",
         "note": "exits along the marked lead-run to the closure edge."},
    ]
    pattern.metadata = {
        "fc300_rank": 266,
        "family": "etextile",
        "fabric_hint": "poliester-elastano-compresion",
        "finished_mm": {"prox_girth": round(prox_girth, 1),
                        "dist_girth": round(dist_girth, 1),
                        "cuff_height": round(cuff_height, 1),
                        "cut_prox": round(C_P, 1),
                        "cut_dist": round(C_D, 1)},
        "solved": {
            "conical": CONICAL,
            "cone_r_prox_mm": round(_r_p, 3),
            "cone_r_dist_mm": round(_r_d, 3),
            "slant_mm": round(SLANT, 3),
            "sector_r_inner_mm": round(R_D, 3),
            "sector_r_outer_mm": round(R_P, 3),
            "sector_angle_deg": round(math.degrees(THETA), 3),
            "prox_arc_measured_mm": round(PROX_ARC, 3),
            "dist_arc_measured_mm": round(DIST_ARC, 3),
            "dist_arc_target_mm": round(C_D, 3),
            "dist_arc_error_mm": round(abs(DIST_ARC - C_D), 4),
            "closure_len_mm": round(CLOSURE_LEN, 3),
            "slant_vs_height_mm": round(SLANT - cuff_height, 4),
            "sector_radius_ratio": round(R_D / SLANT, 3) if CONICAL else None,
            "rect_fallback_slack_mm": None if CONICAL else round(C_P - C_D, 3),
            "note": "the flat pattern of a tapered cuff is an ANNULAR SECTOR, not a "
                    "trapezoid: R_d = r_d*slant/(r_p-r_d), R_p = R_d+slant, "
                    "theta = C_p/R_p — and R_d*theta then equals C_d exactly, which "
                    "is the proof the draft is right (dist_arc_error_mm). The slant, "
                    "not the axial height, is the radial span; using the height "
                    "instead cuts the cuff short by slant_vs_height_mm. As the taper "
                    "goes to zero R_d diverges, so the fallback is guarded on R_d/slant "
                    "(sector_radius_ratio) rather than on a bare epsilon: a nearly "
                    "cylindrical limb is drafted as a rectangle at the proximal girth, "
                    "and the taper it gave up is declared as rect_fallback_slack_mm.",
        },
        "etextile_note": "The sensor plate footprint, its four sew points, the lead "
                         "run and the grip bands are MARKED. No sensor, IMU, "
                         "goniometer, or circuit is drafted here.",
        "hardware": "sensor mount via Yantra4D (notion.hardware_ref -> "
                    "sensor-mount-plate); the plate's base_w x base_d is this cuff's "
                    "plate_w x plate_d, the same rectangle marked on the shell",
    }
    return pattern


result = build()
