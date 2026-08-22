"""
Illuminated Cycling Gilet — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A close-fitting sleeveless windshell for the drops: short in front, long and curved
at the back, with an LED harness routed along a real seam instead of cable-tied to
whatever the rider has on. This is NOT a hi-vis over-vest (see `hi-vis-vest`, cut
boxy over street clothes) and NOT the raglan `led-trim-jacket` (which carries a
printed LED channel along its raglan curve). This one is drafted for the CYCLING
POSTURE, and the posture is the whole pattern problem.

Drafting note — the seam that must SOLVE: on a bike the spine lengthens and the
front shortens. So the back is drafted `tail_drop` longer than the front, and its
hem is a CURVE (the drop tail) rather than a straight line. But front and back still
have to sew together down the side, and the side seam length is not a free number —
it is whatever the curved back hem left behind after the armhole and the drop.

The kernel therefore drafts the BACK first, measures its drawn `side` edge, and
cuts the front's side edge to that MEASURED length by solving the front hem's
height from it:

    FRONT_SIDE_Y = BACK_SIDE_LEN measured off the drawn back, then the front's hem
    line is placed so front.side.length() == back.side.length().

Assume the closed form (front_length = back_length - tail_drop) and you are wrong by
the sag of the curve, which grows with `tail_drop` — exactly the parameter a rider
turns up. So it is measured.

The LED harness runs the side seam, and every `clip_pitch` millimetres along that
MEASURED run a Yantra4D `seam-conduit-clip` footprint is marked. Clip count is
therefore also solved from the drawn seam, not guessed.

Pieces:
  - front   : gilet front, cut 2 mirrored (centre-front zip), LED spur marked.
  - back    : gilet back on the fold, drop tail, harness run and clip footprints.
  - placket : centre-front zip facing, cut to the measured front CF edge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|placket|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))      # full chest
front_length = float(PARAM(lambda: front_length, 520.0))    # shoulder to front hem
tail_drop = float(PARAM(lambda: tail_drop, 130.0))          # extra length at centre back
tail_curve = float(PARAM(lambda: tail_curve, 0.30))         # how much the tail hem bows
neck_width = float(PARAM(lambda: neck_width, 170.0))        # neck opening width
shoulder_w = float(PARAM(lambda: shoulder_w, 110.0))        # neck point to shoulder tip
armhole_drop = float(PARAM(lambda: armhole_drop, 250.0))    # shoulder down to underarm
gilet_ease = float(PARAM(lambda: gilet_ease, 60.0))         # aero fit: little ease
waist_suppress = float(PARAM(lambda: waist_suppress, 22.0))  # side-seam waist shaping
strip_w = float(PARAM(lambda: strip_w, 10.0))               # LED strip / harness width
clip_pitch = float(PARAM(lambda: clip_pitch, 90.0))         # conduit clip spacing
clip_tab = float(PARAM(lambda: clip_tab, 16.0))             # clip sewn tab width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(720.0, min(chest_girth, 1400.0))
front_length = max(380.0, min(front_length, 720.0))
tail_drop = max(40.0, min(tail_drop, 260.0))
tail_curve = max(0.05, min(tail_curve, 0.60))
neck_width = max(120.0, min(neck_width, 240.0))
shoulder_w = max(70.0, min(shoulder_w, 180.0))
armhole_drop = max(150.0, min(armhole_drop, 360.0))
gilet_ease = max(0.0, min(gilet_ease, 200.0))
waist_suppress = max(0.0, min(waist_suppress, 70.0))
strip_w = max(5.0, min(strip_w, 30.0))
clip_pitch = max(40.0, min(clip_pitch, 240.0))
clip_tab = max(8.0, min(clip_tab, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 18.0))
hem_allowance = max(8.0, min(hem_allowance, 50.0))

# The armhole cannot swallow the whole front — leave a body below it.
armhole_drop = min(armhole_drop, front_length - 90.0)
# The clip tab must fit inside the seam allowance it is caught in.
clip_tab = min(clip_tab, max(seam_allowance, 6.0) * 2.4)

QUARTER = (chest_girth + gilet_ease) / 4.0   # half-front / half-back width
BACK_LEN = front_length + tail_drop          # centre-back length
# The waist can never be suppressed past the point where the side seam would cross
# the centre line — cap it well short of that.
waist_suppress = min(waist_suppress, QUARTER * 0.30)


def build_back():
    """Back on the fold: full-length centre back, curved drop tail, harness run.

    x = 0 is centre back (the fold); x = QUARTER is the side seam. y grows downward
    from the shoulder line, so the hem is at large y.

    The side seam is SHAPED, not straight: an aero gilet is suppressed at the waist
    and lets out again over the hip, because in the drops the hip is the widest thing
    the garment passes. That shaping is what makes the side seam's LENGTH stop being
    `y_side_hem - y_underarm` — a bowed edge is longer than the drop it spans, by an
    amount that scales with `waist_suppress`. The drop tail is likewise a curve.
    """
    w = QUARTER
    y_shoulder = 0.0
    y_underarm = armhole_drop
    y_side_hem = front_length          # the side of the back stops at the front's line
    y_cb_hem = BACK_LEN                # centre back drops the full tail

    neck_half = neck_width / 2.0
    shoulder_tip = fc.P(neck_half + shoulder_w, y_shoulder + 26.0)  # shoulder slope

    # The side seam bows INWARD at the waist. `waist_suppress` is the millimetres
    # taken out at the narrowest point; `curve_through`'s bulge is a fraction of the
    # chord, so it is converted against the actual drop the seam spans.
    side_drop = y_side_hem - y_underarm
    side_bulge = waist_suppress / max(side_drop, 1.0)

    edges = [
        # Centre back fold, nape down to the tail point.
        fc.Edge("cb", [fc.Line(fc.P(0.0, y_cb_hem), fc.P(0.0, y_shoulder + 12.0))]),
        # Back neckline: shallow scoop.
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, y_shoulder + 12.0),
                                          fc.P(neck_half, y_shoulder),
                                          bulge=0.18, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_half, y_shoulder), shoulder_tip)]),
        # Armhole: shoulder tip curving in to the underarm at the side seam.
        fc.Edge("armhole", [fc.curve_through(shoulder_tip, fc.P(w, y_underarm),
                                             bulge=0.22, side=1.0)]),
        # Side seam: SHAPED, bowing in at the waist. Its length is therefore longer
        # than `side_drop`, and by how much is not a closed form you want to trust.
        fc.Edge("side", [fc.curve_through(fc.P(w, y_underarm), fc.P(w, y_side_hem),
                                          bulge=side_bulge, side=1.0)]),
        # THE DROP TAIL: side hem curving down and in to the centre-back point.
        fc.Edge("hem", [fc.curve_through(fc.P(w, y_side_hem), fc.P(0.0, y_cb_hem),
                                         bulge=tail_curve, side=1.0)]),
    ]

    internals = []
    # The harness run follows the SHAPED side seam (sampled off the drawn curve, so
    # it stays inside the allowance where the seam bows in), then breaks away across
    # to centre back at the tail where the battery sits — low, out of the wind, and
    # off the shoulder blades.
    _side = next(e for e in edges if e.name == "side")
    run = []
    for k in range(6):
        pt, _tan = _side.point_at_fraction(0.08 + 0.84 * k / 5.0)
        run.append(fc.P(pt.x - seam_allowance * 0.5, pt.y))
    run.append(fc.P(w * 0.35, y_cb_hem - 40.0))
    internals.append(fc.Internal("harness-run", run, kind="trace"))
    # Battery pocket at the tail, on the fold side.
    internals.append(fc.Internal("battery-pocket", [
        fc.P(w * 0.06, y_cb_hem - 34.0 - strip_w * 5.0),
        fc.P(w * 0.06 + strip_w * 7.0, y_cb_hem - 34.0 - strip_w * 5.0),
        fc.P(w * 0.06 + strip_w * 7.0, y_cb_hem - 34.0),
        fc.P(w * 0.06, y_cb_hem - 34.0),
        fc.P(w * 0.06, y_cb_hem - 34.0 - strip_w * 5.0)], kind="marking"))
    # Rear light seat, centred on the tail where a following driver sees it.
    internals.append(fc.Internal("rear-light-seat", [
        fc.P(w * 0.30, y_cb_hem - 96.0), fc.P(w * 0.30 + strip_w * 4.0, y_cb_hem - 96.0),
        fc.P(w * 0.30 + strip_w * 4.0, y_cb_hem - 96.0 + strip_w * 2.4),
        fc.P(w * 0.30, y_cb_hem - 96.0 + strip_w * 2.4),
        fc.P(w * 0.30, y_cb_hem - 96.0)], kind="marking"))

    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side balance"),
                 fc.Notch("armhole", 0.5, "back armhole balance")],
        grainline=fc.Grainline(fc.P(w * 0.5, y_underarm * 0.6),
                               fc.P(w * 0.5, y_side_hem - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb"),
        label="Back (drop tail, on fold)",
    )


# ── The measured side seam ───────────────────────────────────────────────────
# The back is drafted first so its `side` edge can be MEASURED. The front's side
# edge is then cut to that same measured length rather than to an assumed
# front_length - armhole_drop, because the drop tail's curve is what actually set
# where the back's side hem landed.
_BACK = build_back()
BACK_SIDE_LEN = _BACK.edge("side").length()
BACK_HEM_LEN = _BACK.edge("hem").length()
BACK_ARMHOLE_LEN = _BACK.edge("armhole").length()
# Conduit clips march the MEASURED side run, not a nominal one.
CLIP_COUNT = max(2, int(BACK_SIDE_LEN // clip_pitch))
CLIP_SPACING = BACK_SIDE_LEN / (CLIP_COUNT + 1)


def _front_side_edge(y_hem):
    """The front's side seam as drawn for a candidate hem height.

    It mirrors the back's shaping: same `waist_suppress` taken out at the waist, so
    the two seams have the same silhouette. Its LENGTH is a function of `y_hem`
    that has no useful inverse — hence the solve below.
    """
    drop = y_hem - armhole_drop
    bulge = waist_suppress / max(drop, 1.0)
    return fc.Edge("side", [fc.curve_through(fc.P(QUARTER, armhole_drop),
                                             fc.P(QUARTER, y_hem),
                                             bulge=bulge, side=1.0)])


def _solve_front_hem(target_len, tol=0.02, iters=60):
    """Bisect the front's hem height until its SHAPED side edge measures the back's.

    This is the seam that had to solve. The back's side seam is bowed by
    `waist_suppress`, so its length exceeds the vertical drop it spans; the front's
    is bowed by the same amount but over a different (unknown) drop. Setting the
    front hem to `armhole_drop + target_len` — the closed form you would reach for —
    over-shoots, because it treats the arc length as if it were the drop. The error
    grows with `waist_suppress`, which is exactly the fit parameter a rider changes.

    Length is monotonic in the hem height here (a longer drop with a fixed absolute
    suppression is a strictly longer arc), so a bisection converges cleanly.
    """
    lo = armhole_drop + 1.0
    hi = armhole_drop + target_len + max(waist_suppress, 1.0) * 4.0
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if _front_side_edge(mid).length() < target_len:
            lo = mid
        else:
            hi = mid
        if hi - lo < tol:
            break
    return (lo + hi) / 2.0


FRONT_SIDE_HEM_Y = _solve_front_hem(BACK_SIDE_LEN)
# What the naive closed form would have produced, kept so the metadata can report
# the error the solve actually removed.
FRONT_SIDE_HEM_NAIVE = armhole_drop + BACK_SIDE_LEN


def build_front():
    """Front half, cut 2 mirrored. x = 0 is centre front (the zip), x = QUARTER the
    side seam. The side edge is SOLVED to the back's MEASURED side length."""
    w = QUARTER
    y_shoulder = 0.0
    y_underarm = armhole_drop
    # Solved, not assumed — see `_solve_front_hem`.
    y_side_hem = FRONT_SIDE_HEM_Y
    # Centre front sits a touch higher than the side — a gilet front does not hang
    # square; the zip must not dig in while the rider is folded over the bars.
    y_cf_hem = y_side_hem - tail_drop * 0.18

    neck_half = neck_width / 2.0
    shoulder_tip = fc.P(neck_half + shoulder_w, y_shoulder + 26.0)

    edges = [
        # Centre front (zip edge), hem up to the neck.
        fc.Edge("cf", [fc.Line(fc.P(0.0, y_cf_hem), fc.P(0.0, y_shoulder + 42.0))]),
        # Front neckline, deeper than the back.
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, y_shoulder + 42.0),
                                          fc.P(neck_half, y_shoulder),
                                          bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_half, y_shoulder), shoulder_tip)]),
        fc.Edge("armhole", [fc.curve_through(shoulder_tip, fc.P(w, y_underarm),
                                             bulge=0.30, side=1.0)]),
        # Shaped to mirror the back's side seam, and SOLVED to its measured length.
        _front_side_edge(y_side_hem),
        fc.Edge("hem", [fc.Line(fc.P(w, y_side_hem), fc.P(0.0, y_cf_hem))]),
    ]

    internals = []
    # LED spur from the side-seam harness across the chest to the front strip.
    internals.append(fc.Internal("chest-strip", [
        fc.P(w * 0.18, y_underarm + 40.0), fc.P(w * 0.82, y_underarm + 40.0)],
        kind="trace"))
    internals.append(fc.Internal("led-spur", [
        fc.P(w - seam_allowance * 0.5, y_underarm + 40.0),
        fc.P(w * 0.82, y_underarm + 40.0)], kind="trace"))
    # Conduit-clip footprints spaced along the MEASURED side seam by ARC LENGTH, and
    # seated on the drawn curve rather than on a nominal straight x = w — the seam
    # bows inward at the waist, so a clip placed at x = w would sit off the seam it
    # is meant to be caught in.
    side_edge = _front_side_edge(y_side_hem)
    harness_pts = []
    for i in range(CLIP_COUNT):
        t = CLIP_SPACING * (i + 1) / BACK_SIDE_LEN
        seat, _tangent = side_edge.point_at_fraction(min(max(t, 0.0), 1.0))
        harness_pts.append(fc.P(seat.x - seam_allowance * 0.5, seat.y))
        internals.append(fc.Internal(f"conduit-clip-{i}", [
            fc.P(seat.x - clip_tab, seat.y - clip_tab / 2.0),
            fc.P(seat.x, seat.y - clip_tab / 2.0),
            fc.P(seat.x, seat.y + clip_tab / 2.0),
            fc.P(seat.x - clip_tab, seat.y + clip_tab / 2.0),
            fc.P(seat.x - clip_tab, seat.y - clip_tab / 2.0)], kind="marking"))
    # The harness itself follows the same shaped path, threading the clips.
    if harness_pts:
        internals.append(fc.Internal("side-harness-run", harness_pts, kind="trace"))

    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side balance"),
                 fc.Notch("armhole", 0.5, "front armhole balance")],
        grainline=fc.Grainline(fc.P(w * 0.5, y_underarm * 0.6),
                               fc.P(w * 0.5, y_side_hem - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


_FRONT = build_front()
FRONT_CF_LEN = _FRONT.edge("cf").length()
FRONT_ARMHOLE_LEN = _FRONT.edge("armhole").length()
_FRONT_SIDE_LEN = _FRONT.edge("side").length()


def build_placket():
    """The centre-front zip facing, cut to the front's MEASURED cf edge so the zip
    tape and the facing finish together instead of one running past the other."""
    ln = FRONT_CF_LEN
    w = max(strip_w * 2.6, 26.0)
    internals = [
        # The zip tape line, held one seam allowance in from the raw edge.
        fc.Internal("zip-line", [fc.P(seam_allowance, w * 0.5),
                                 fc.P(ln - seam_allowance, w * 0.5)], kind="trace"),
    ]
    return fc.Piece(
        "placket",
        [
            fc.Edge("hem_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("outer", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("neck_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("attach", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "zip midpoint")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w / 2.0), fc.P(ln * 0.85, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Zip placket facing (cut 2)",
    )


def build():
    pattern = fc.PatternSet("illuminated-gilet")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "placket":
        pattern.add(build_placket())

    if all_pieces:
        # THE seam that had to solve: the front's side edge was cut to the back's
        # MEASURED side length — after the drop tail's curve decided where the
        # back's side hem landed. Declared so the solve is machine-checked.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # The placket is cut to the front's measured centre-front edge.
        pattern.declare_seam(("placket", "attach"), ("front", "cf"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "windproof ripstop shell", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; the drop tail nests badly, "
                 "so the allowance is deliberately loose."},
        {"item": "seam conduit clip", "qty": CLIP_COUNT * 2, "unit": "count",
         "note": f"Yantra4D seam-conduit-clip (notion.hardware_ref); "
                 f"{clip_tab:.0f} mm sewn tab, {CLIP_COUNT} per side seam at "
                 f"{CLIP_SPACING:.0f} mm along the MEASURED {BACK_SIDE_LEN:.0f} mm run."},
        {"item": "LED strip or reflective harness", "qty": 1, "unit": "run",
         "note": f"{strip_w:.0f} mm wide; side-seam run plus the chest spur "
                 f"and the rear-light seat."},
        {"item": "separating zip", "qty": 1, "unit": "count",
         "note": f"{FRONT_CF_LEN:.0f} mm — the front's MEASURED centre-front edge, "
                 f"which is what the placket was cut to."},
        {"item": "battery + driver", "qty": 1, "unit": "set",
         "note": "in the back's marked battery-pocket at the tail, low and out of "
                 "the wind."},
        {"item": "hem elastic or silicone gripper", "qty": 1, "unit": "run",
         "note": f"≈ {BACK_HEM_LEN:.0f} mm back hem; a drop tail without a gripper "
                 f"flaps at speed."},
    ]
    pattern.metadata = {
        "fc300_rank": 265,
        "family": "etextile",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"chest": round(chest_girth + gilet_ease, 1),
                        "front_length": round(front_length, 1),
                        "back_length": round(BACK_LEN, 1),
                        "tail_drop": round(tail_drop, 1)},
        "solved": {
            "quarter_mm": round(QUARTER, 2),
            "back_side_len_mm": round(BACK_SIDE_LEN, 2),
            "front_armhole_mm": round(FRONT_ARMHOLE_LEN, 2),
            "back_armhole_mm": round(BACK_ARMHOLE_LEN, 2),
            "back_hem_len_mm": round(BACK_HEM_LEN, 2),
            "front_cf_len_mm": round(FRONT_CF_LEN, 2),
            "front_side_hem_y_mm": round(FRONT_SIDE_HEM_Y, 2),
            "front_side_hem_y_naive_mm": round(FRONT_SIDE_HEM_NAIVE, 2),
            "closed_form_error_mm": round(FRONT_SIDE_HEM_NAIVE - FRONT_SIDE_HEM_Y, 2),
            "front_side_len_mm": round(_FRONT_SIDE_LEN, 2),
            "side_seam_mismatch_mm": round(abs(_FRONT_SIDE_LEN - BACK_SIDE_LEN), 3),
            "waist_suppress_mm": round(waist_suppress, 2),
            "clip_count_per_seam": CLIP_COUNT,
            "clip_spacing_mm": round(CLIP_SPACING, 2),
            "note": "both side seams are SHAPED by waist_suppress, so a bowed edge is "
                    "longer than the vertical drop it spans. The front's hem height is "
                    "therefore bisected until its drawn side edge MEASURES the back's "
                    "measured side edge; the closed form (armhole_drop + back_side_len) "
                    "treats the arc length as if it were the drop and overshoots by "
                    "closed_form_error_mm, an error that grows with waist_suppress. "
                    "Conduit clips are then spaced by ARC LENGTH along that same "
                    "measured run and seated on the drawn curve.",
        },
        "etextile_note": "Harness runs, the chest strip, the LED spur, the clip "
                         "footprints, the battery pocket and the rear-light seat are "
                         "MARKED. No LED, driver, battery or circuit is drafted here.",
        "hardware": "conduit clips via Yantra4D (notion.hardware_ref -> "
                    "seam-conduit-clip); the clip's sewn tab width is this gilet's "
                    "clip_tab and its run pitch is the solved clip_spacing along the "
                    "measured side seam",
    }
    return pattern


result = build()
