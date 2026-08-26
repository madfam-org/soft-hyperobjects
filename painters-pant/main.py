"""
Painter's Utility Pant — Fashion Cabinet Garment Cartridge
(FC-400 #308, workwear_uniforms, T2).

The painter's pant: a straight loose leg in cotton duck, a hammer loop down one
side, a stack of narrow brush/pencil pockets on the thigh, and a deep double-knee
zone. The defining feature is the HAMMER LOOP, and it is a CO-CREATED hard good:
the loop's stiffening insert is a new Yantra4D solid this garment pulls onto the
shelf (`hammer-loop`, co-create) rather than an existing part.

Three things are solved by measurement rather than by formula:

  1. THE HAMMER LOOP IS CUT TO A MEASURED SWING. The loop must clear a hammer head
     with room for the handle to drop through, so its cut length is twice the
     MEASURED clearance plus the strap run round the bar-tack — a MEASURED swing,
     never a fixed strip. The co-created hardware_ref's span maps to that
     clearance so the printed insert matches the sewn loop.

  2. THE BRUSH-POCKET PITCH IS SOLVED ACROSS THE MEASURED PANEL. The narrow
     pockets sit on a panel of MEASURED width; whole gaps are fitted at (or under)
     the requested pitch and the gap RECOMPUTED, so the last pocket lands on the
     panel and not off its edge.

  3. THE INSEAMS ARE BALANCED TO ZERO AND THE DOUBLE-KNEE CLAMPED. Front and back
     inseams must MEASURE the same or the loose leg twists; and the double-knee
     reinforcement zone is clamped within the leg it lies on, because a knee patch
     wider than the leg is CCW-normalized by the kernel into a healthy-looking
     inverted piece.

WORKWEAR CONVENTIONS: 7 mm topstitch; felled seams; hard goods via Yantra4D. The
HAMMER-LOOP SOLID is a Group-B CO-CREATION (`hammer-loop (co-create)`; the demand-
pull ruling): named in the notion, params mapped, linked=false because it is not
yet in FC's pinned hardware snapshot.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres) ─────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|waistband|hammer_loop|brush_panel|set

waist_girth = float(PARAM(lambda: waist_girth, 860.0))
hip_girth = float(PARAM(lambda: hip_girth, 1040.0))
inside_leg = float(PARAM(lambda: inside_leg, 800.0))
front_rise = float(PARAM(lambda: front_rise, 280.0))
hem_width = float(PARAM(lambda: hem_width, 240.0))
band_depth = float(PARAM(lambda: band_depth, 42.0))
tool_clearance = float(PARAM(lambda: tool_clearance, 42.0))   # hammer-loop swing
brush_count = float(PARAM(lambda: brush_count, 4.0))
brush_width = float(PARAM(lambda: brush_width, 32.0))
knee_drop = float(PARAM(lambda: knee_drop, 200.0))            # double-knee zone height
wear_ease = float(PARAM(lambda: wear_ease, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1400.0))
inside_leg = max(560.0, min(inside_leg, 950.0))
front_rise = max(200.0, min(front_rise, 360.0))
hem_width = max(180.0, min(hem_width, 360.0))
band_depth = max(28.0, min(band_depth, 64.0))
tool_clearance = max(24.0, min(tool_clearance, 70.0))
brush_count = max(2.0, min(round(brush_count), 8.0))
brush_width = max(18.0, min(brush_width, 55.0))
knee_drop = max(120.0, min(knee_drop, 320.0))
wear_ease = max(0.0, min(wear_ease, 180.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(22.0, min(hem_allowance, 60.0))

TOPSTITCH = 7.0
N_BRUSH = int(brush_count)

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
HALF_HEM = hem_width / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)

# The brush panel: clamped against the leg, pockets solved across it.
_BRUSH_PANEL_RAW = N_BRUSH * brush_width + (N_BRUSH + 1) * (brush_width * 0.4)
BRUSH_PANEL_W = max(3.0 * brush_width,
                    min(_BRUSH_PANEL_RAW, QUARTER_HIP - 2.0 * seam_allowance))
BRUSH_PANEL_H = max(120.0, brush_width * 4.5)
_USABLE = BRUSH_PANEL_W - 2.0 * seam_allowance - brush_width
N_GAPS = max(1, N_BRUSH - 1)
BRUSH_PITCH = _USABLE / N_GAPS if N_GAPS else 0.0

# The double-knee reinforcement, clamped within the leg.
_KNEE_W_RAW = HALF_HEM * 2.0
KNEE_W = max(80.0, min(_KNEE_W_RAW, QUARTER_HIP + FORK_F - 2.0 * seam_allowance))
KNEE_Y = inside_leg * 0.46

# The hammer loop cut to a MEASURED swing.
LOOP_STRAP_W = max(28.0, tool_clearance * 0.8)
HAMMER_LOOP_RUN = 2.0 * tool_clearance + LOOP_STRAP_W + 2.0 * seam_allowance
HAMMER_LOOP_CUT = HAMMER_LOOP_RUN + 2.0 * seam_allowance


# ── Inseams solved equal ─────────────────────────────────────────────────────
def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0), bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
    lo, hi = 0.0, 0.45
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < _BACK_INSEAM_LEN:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


BULGE = _solve_front_bulge()
_FRONT_INSEAM_LEN = _front_inseam(BULGE).length(0.05)


def build_front_leg():
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.44),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF match"),
                 fc.Notch("side", 0.46, "double-knee top"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, front_rise * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            fc.Internal("hammer-loop anchor",
                        [fc.P(seam_allowance, front_rise * 0.55),
                         fc.P(seam_allowance + LOOP_STRAP_W, front_rise * 0.55)],
                        kind="marking"),
            fc.Internal("double-knee reinforcement zone",
                        [fc.P((QUARTER_HIP + FORK_F - KNEE_W) * 0.5 + 0.0, KNEE_Y),
                         fc.P((QUARTER_HIP + FORK_F - KNEE_W) * 0.5 + KNEE_W, KNEE_Y),
                         fc.P((QUARTER_HIP + FORK_F - KNEE_W) * 0.5 + KNEE_W,
                              KNEE_Y - knee_drop),
                         fc.P((QUARTER_HIP + FORK_F - KNEE_W) * 0.5, KNEE_Y - knee_drop),
                         fc.P((QUARTER_HIP + FORK_F - KNEE_W) * 0.5, KNEE_Y)],
                        kind="marking"),
            fc.Internal("brush panel placement",
                        [fc.P(QUARTER_HIP * 0.18, front_rise * 0.30),
                         fc.P(QUARTER_HIP * 0.18 + BRUSH_PANEL_W, front_rise * 0.30),
                         fc.P(QUARTER_HIP * 0.18 + BRUSH_PANEL_W,
                              front_rise * 0.30 - BRUSH_PANEL_H),
                         fc.P(QUARTER_HIP * 0.18, front_rise * 0.30 - BRUSH_PANEL_H),
                         fc.P(QUARTER_HIP * 0.18, front_rise * 0.30)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.44),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("side", 0.46, "knee"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            fc.Internal("patch pocket placement",
                        [fc.P(QUARTER_WAIST * 0.2, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.84, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.84,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.6),
                         fc.P(QUARTER_WAIST * 0.2,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.6),
                         fc.P(QUARTER_WAIST * 0.2, BACK_RISE - band_depth - 30.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


_FL = build_front_leg()
_BL = build_back_leg()
FRONT_WAIST_RUN = _FL.edge("waist").length(0.05)
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
BAND_LENGTH = 2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN + 60.0
BAND_CUT_H = band_depth * 2.0 + 2.0 * seam_allowance


def build_waistband():
    ln = BAND_LENGTH
    w = BAND_CUT_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("ext_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("cf_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "waistband", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("band topstitch",
                        [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (cut 1)",
    )


def build_hammer_loop():
    """The hammer loop, cut 1. The stiffening insert is the co-created solid."""
    ln = HAMMER_LOOP_CUT
    w = LOOP_STRAP_W
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "hammer_loop", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "bar-tack A"),
                 fc.Notch("lower", 1.0, "bar-tack B")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("stiffening insert slot (co-created solid)",
                        [fc.P(seam_allowance * 2.0, w * 0.5),
                         fc.P(ln - seam_allowance * 2.0, w * 0.5)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Hammer loop (cut 1)",
    )


def build_brush_panel():
    """The brush/pencil pocket panel, cut 1. Pockets solved across it."""
    w = BRUSH_PANEL_W
    h = BRUSH_PANEL_H
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    internals = [
        fc.Internal("mouth topstitch",
                    [fc.P(TOPSTITCH, h - TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                    kind="trace"),
    ]
    x0 = seam_allowance + brush_width / 2.0
    for i in range(N_BRUSH):
        x = x0 + BRUSH_PITCH * i
        internals.append(fc.Internal(
            f"brush divider-{i + 1}",
            [fc.P(x + brush_width / 2.0, 0.0), fc.P(x + brush_width / 2.0, h)],
            kind="trace"))
    return fc.Piece(
        "brush_panel", edges,
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance * 0.5},
        notches=[fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Brush/pencil pocket panel (cut 1)",
    )


def build():
    pattern = fc.PatternSet("painters-pant")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "hammer_loop": everything or target_piece == "hammer_loop",
        "brush_panel": everything or target_piece == "brush_panel",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["waistband"]:
        pattern.add(build_waistband())
    if want["hammer_loop"]:
        pattern.add(build_hammer_loop())
    if want["brush_panel"]:
        pattern.add(build_brush_panel())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["hammer_loop"]:
        pattern.declare_seam(("hammer_loop", "lower"), ("hammer_loop", "upper"),
                             tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton duck canvas, 10 oz (classic painter's white)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; painter's white "
                 f"duck — the paint that lands on it is the badge, not the flaw."},
        {"item": "hammer-loop stiffening insert (co-created solid)", "qty": 1,
         "unit": "piece",
         "note": f"Yantra4D hammer-loop (notion.hardware_ref, CO-CREATE): a printed "
                 f"insert that keeps the loop open at a {tool_clearance:.0f} mm "
                 f"clearance so a hammer drops in one-handed. A Group-B co-creation."},
        {"item": "heavy topstitch thread + jeans needle 100/16", "qty": 1,
         "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; felled seams; double-knee "
                 f"reinforcement stitched in the marked zone."},
    ]
    pattern.metadata = {
        "fc400_rank": 308,
        "family": "workwear_uniforms",
        "tier": 2,
        "fabric_hint": "duck-canvas",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "hem_width": round(hem_width, 1),
            "hammer_loop_cut": round(HAMMER_LOOP_CUT, 1),
            "brush_panel_width": round(BRUSH_PANEL_W, 1),
            "double_knee_width": round(KNEE_W, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "hammer_loop_run_mm": round(HAMMER_LOOP_RUN, 2),
            "tool_clearance_mm": round(tool_clearance, 2),
            "brush_count": N_BRUSH,
            "brush_pitch_solved_mm": round(BRUSH_PITCH, 2),
            "brush_panel_requested_mm": round(_BRUSH_PANEL_RAW, 2),
            "brush_panel_clamped_mm": round(BRUSH_PANEL_W, 2),
            "brush_panel_was_clamped": bool(
                abs(BRUSH_PANEL_W - _BRUSH_PANEL_RAW) > 0.01),
            "double_knee_requested_mm": round(_KNEE_W_RAW, 2),
            "double_knee_clamped_mm": round(KNEE_W, 2),
            "double_knee_was_clamped": bool(abs(KNEE_W - _KNEE_W_RAW) > 0.01),
            "note": "the hammer loop is cut to a MEASURED swing (twice the tool "
                    "clearance plus the strap run), and its co-created stiffening "
                    "insert's span maps to that same clearance so the printed part "
                    "matches the sewn loop. The brush pockets are pitched across "
                    "the MEASURED panel with whole gaps recomputed. The inseams "
                    "are balanced to zero and the double-knee zone clamped within "
                    "the leg, because an inverted piece is CCW-normalized by the "
                    "kernel and passes verify() looking healthy.",
        },
        "co_creation": "hammer-loop is a Group-B CO-CREATION under the FC-200 "
                       "demand-pull ruling: the painter's pant needs a loop-"
                       "stiffening insert the pinned Yantra4D snapshot does not yet "
                       "carry, so the notion names it with linked=false and maps its "
                       "params, logging the pull onto the wearables shelf.",
        "topstitch": f"twin-needle heavy contrast at {TOPSTITCH:.0f} mm",
        "hardware": "hammer-loop stiffening insert via Yantra4D "
                    "(notion.hardware_ref -> hammer-loop, CO-CREATE); the solid's "
                    "span is fed from this garment's tool_clearance, so the printed "
                    "insert holds the sewn loop open at exactly the hammer clearance.",
    }
    return pattern


result = build()
