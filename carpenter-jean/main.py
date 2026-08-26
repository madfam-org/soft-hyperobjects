"""
Carpenter Jean with Tool Loops — Fashion Cabinet Garment Cartridge
(FC-400 #302, denim, T2).

The utility jean: a straight leg carrying a hammer loop down one side, a rule
(ruler) pocket on the thigh, and a stack of narrow tool loops. The whole garment
is a set of load paths, and every one of them terminates at a RIVET rather than a
bar-tack — on 12 oz denim a bar-tack abrades before the cloth does, and a hammer
swinging in a loop is exactly the cyclic load that finds a bar-tack first.

Three things are solved by measurement rather than by formula:

  1. THE HAMMER LOOP IS CUT TO A MEASURED SWING, NOT A GUESS. A hammer loop is
     not a strip of a fixed length: it has to clear the hammer's head with room
     to drop the handle through, so its cut length is the loop's inner
     circumference (twice the clearance plus the strap width run round the bar
     tack) — derived from a MEASURED tool clearance, then the rivet that holds
     its top is stepped in so it lands on the leg panel and not on the loop's own
     turn.

  2. THE TOOL-LOOP PITCH IS SOLVED ACROSS THE MEASURED PANEL. The loops sit on a
     backing panel of a MEASURED width; the requested loop count and loop width
     are fitted to whole gaps across that width, and the gap RECOMPUTED, so the
     last loop lands on the panel and not off its edge. A pitch applied blind
     runs the final loop past the seam allowance.

  3. THE RULE POCKET IS CLAMPED AGAINST THE LEG IT SITS ON. A thigh pocket wider
     than the leg panel is a piece that folds back on itself and — because the
     kernel CCW-normalizes an inverted outline and area() takes an absolute
     value — renders and passes verify() looking healthy. Its width and the loop
     panel width are both clamped and reported.

DENIM CONVENTIONS, per the family (jeans-5-pocket, selvedge-jean): a 7 mm
twin-needle topstitch gauge; every outer edge felled or turned; every hard good a
Yantra4D reference. The RIVET SOLID is Yantra4D territory (`rivet`; see
notion.hardware_ref).

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
# front_leg|back_leg|waistband|hammer_loop|loop_panel|rule_pocket|set

waist_girth = float(PARAM(lambda: waist_girth, 860.0))
hip_girth = float(PARAM(lambda: hip_girth, 1040.0))
inside_leg = float(PARAM(lambda: inside_leg, 800.0))
front_rise = float(PARAM(lambda: front_rise, 270.0))
hem_width = float(PARAM(lambda: hem_width, 220.0))
band_depth = float(PARAM(lambda: band_depth, 42.0))
tool_clearance = float(PARAM(lambda: tool_clearance, 40.0))   # hammer head clearance
loop_count = float(PARAM(lambda: loop_count, 5.0))            # tool loops on the panel
loop_width = float(PARAM(lambda: loop_width, 26.0))          # each loop's finished width
rivet_cap = float(PARAM(lambda: rivet_cap, 11.0))           # rivet cap dia
wear_ease = float(PARAM(lambda: wear_ease, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 32.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1400.0))
inside_leg = max(560.0, min(inside_leg, 950.0))
front_rise = max(200.0, min(front_rise, 360.0))
hem_width = max(160.0, min(hem_width, 340.0))
band_depth = max(28.0, min(band_depth, 64.0))
tool_clearance = max(20.0, min(tool_clearance, 70.0))
loop_count = max(2.0, min(round(loop_count), 9.0))
loop_width = max(16.0, min(loop_width, 48.0))
rivet_cap = max(7.0, min(rivet_cap, 18.0))
wear_ease = max(0.0, min(wear_ease, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 55.0))

TOPSTITCH = 7.0
N_LOOPS = int(loop_count)

# ── Derived block dimensions, clamped ────────────────────────────────────────
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
HALF_HEM = hem_width / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)

# The loop backing panel width: clamped against the leg panel it is applied to,
# so a panel wider than the thigh can never fold back on itself.
_LOOP_PANEL_RAW = N_LOOPS * loop_width + (N_LOOPS + 1) * (loop_width * 0.5)
LOOP_PANEL_W = max(3.0 * loop_width,
                   min(_LOOP_PANEL_RAW, QUARTER_HIP - 2.0 * seam_allowance))
LOOP_PANEL_H = max(50.0, loop_width * 2.2)

# The tool-loop pitch SOLVED across the measured panel: whole gaps at (or under)
# the requested spacing, then recomputed so the last loop lands on the panel.
_USABLE = LOOP_PANEL_W - 2.0 * seam_allowance - loop_width
N_GAPS = max(1, N_LOOPS - 1)
LOOP_PITCH = _USABLE / N_GAPS if N_GAPS else 0.0

# The rule (thigh) pocket, clamped against the leg it sits on.
_RULE_W_RAW = max(70.0, QUARTER_WAIST * 0.42)
RULE_W = max(50.0, min(_RULE_W_RAW, QUARTER_HIP - 2.0 * seam_allowance))
RULE_H = max(160.0, inside_leg * 0.30)


def _rivet(label, x, y):
    a = max(3.0, rivet_cap * 0.32)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


# ── Inseams solved to equal length ───────────────────────────────────────────
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
    """Front leg, cut 2 mirrored. One leg carries the hammer loop and rule pocket
    (marked), the other the tool-loop panel — the classic asymmetric carpenter."""
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
                 fc.Notch("side", 0.5, "hammer-loop top / knee"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, front_rise * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            # The hammer loop's own anchor at the outseam, high on the thigh.
            _rivet("hammer-loop rivet",
                   max(rivet_cap, seam_allowance + rivet_cap),
                   front_rise * 0.60),
            fc.Internal("rule pocket placement",
                        [fc.P(QUARTER_HIP * 0.30, front_rise * 0.55),
                         fc.P(QUARTER_HIP * 0.30 + RULE_W, front_rise * 0.55),
                         fc.P(QUARTER_HIP * 0.30 + RULE_W, front_rise * 0.55 - RULE_H),
                         fc.P(QUARTER_HIP * 0.30, front_rise * 0.55 - RULE_H),
                         fc.P(QUARTER_HIP * 0.30, front_rise * 0.55)],
                        kind="marking"),
            fc.Internal("loop panel placement",
                        [fc.P(QUARTER_HIP * 0.20, front_rise * 0.30),
                         fc.P(QUARTER_HIP * 0.20 + LOOP_PANEL_W, front_rise * 0.30),
                         fc.P(QUARTER_HIP * 0.20 + LOOP_PANEL_W,
                              front_rise * 0.30 - LOOP_PANEL_H),
                         fc.P(QUARTER_HIP * 0.20, front_rise * 0.30 - LOOP_PANEL_H),
                         fc.P(QUARTER_HIP * 0.20, front_rise * 0.30)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back leg, cut 2 mirrored. Rise carried at CB; both side seams equal."""
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
                 fc.Notch("side", 0.5, "knee"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, front_rise)],
                        kind="trace"),
            fc.Internal("patch pocket placement",
                        [fc.P(QUARTER_WAIST * 0.18, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86, BACK_RISE - band_depth - 30.0),
                         fc.P(QUARTER_WAIST * 0.86,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.6),
                         fc.P(QUARTER_WAIST * 0.18,
                              BACK_RISE - band_depth - 30.0 - QUARTER_WAIST * 0.6),
                         fc.P(QUARTER_WAIST * 0.18, BACK_RISE - band_depth - 30.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


_FL = build_front_leg()
_BL = build_back_leg()
FRONT_WAIST_RUN = _FL.edge("waist").length(0.05)
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
BAND_LENGTH = 2.0 * FRONT_WAIST_RUN + 2.0 * BACK_WAIST_RUN + rivet_cap * 3.0
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


# ── The hammer loop, cut to a MEASURED swing ─────────────────────────────────
# A hammer loop is a strip whose finished inner loop must clear the hammer's
# head — so its cut length is the loop's inner run (twice the clearance for the
# up-and-down of the strap, plus the width of the leg it wraps to the bar-tack),
# plus turnings. Not a fixed strip.
LOOP_STRAP_W = max(28.0, tool_clearance * 0.8)
HAMMER_LOOP_RUN = 2.0 * tool_clearance + LOOP_STRAP_W + 2.0 * seam_allowance
HAMMER_LOOP_CUT = HAMMER_LOOP_RUN + 2.0 * seam_allowance


def build_hammer_loop():
    """The hammer loop, cut 1. A strip folded and riveted flat at both ends to
    the outseam, standing off the leg by the tool clearance."""
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
        notches=[fc.Notch("lower", 0.0, "rivet end A"),
                 fc.Notch("lower", 1.0, "rivet end B")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            _rivet("loop rivet A", seam_allowance + rivet_cap, w / 2.0),
            _rivet("loop rivet B", ln - seam_allowance - rivet_cap, w / 2.0),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Hammer loop (cut 1)",
    )


def build_loop_panel():
    """The tool-loop backing panel, cut 1. The loops are stitched across it at a
    SOLVED pitch so the last loop lands on the panel, not off its edge."""
    w = LOOP_PANEL_W
    h = LOOP_PANEL_H
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    internals = [
        fc.Internal("panel topstitch",
                    [fc.P(TOPSTITCH, TOPSTITCH), fc.P(w - TOPSTITCH, TOPSTITCH),
                     fc.P(w - TOPSTITCH, h - TOPSTITCH), fc.P(TOPSTITCH, h - TOPSTITCH),
                     fc.P(TOPSTITCH, TOPSTITCH)],
                    kind="trace"),
    ]
    x0 = seam_allowance + loop_width / 2.0
    for i in range(N_LOOPS):
        x = x0 + LOOP_PITCH * i
        internals.append(fc.Internal(
            f"loop-{i + 1} bar-tack",
            [fc.P(x - loop_width / 2.0, h * 0.5), fc.P(x + loop_width / 2.0, h * 0.5)],
            kind="marking"))
    return fc.Piece(
        "loop_panel", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Tool-loop panel (cut 1)",
    )


def build_rule_pocket():
    """The rule (ruler) pocket, cut 1. A long narrow thigh pocket, clamped
    against the leg it sits on."""
    w = RULE_W
    h = RULE_H
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "rule_pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance * 0.5},
        notches=[fc.Notch("mouth", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, h - TOPSTITCH),
                         fc.P(w - TOPSTITCH, h - TOPSTITCH)], kind="trace"),
            _rivet("rule pocket rivet",
                   max(rivet_cap, w - seam_allowance - rivet_cap),
                   h - hem_allowance - rivet_cap),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Rule pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("carpenter-jean")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "hammer_loop": everything or target_piece == "hammer_loop",
        "loop_panel": everything or target_piece == "loop_panel",
        "rule_pocket": everything or target_piece == "rule_pocket",
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
    if want["loop_panel"]:
        pattern.add(build_loop_panel())
    if want["rule_pocket"]:
        pattern.add(build_rule_pocket())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["hammer_loop"]:
        # Both ends of the loop are riveted flat, so the two long edges (folded to
        # the same centre) must measure identically.
        pattern.declare_seam(("hammer_loop", "lower"), ("hammer_loop", "upper"),
                             tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker."},
        {"item": "rivet + burr", "qty": 6, "unit": "set",
         "note": f"Yantra4D rivet (notion.hardware_ref) at {rivet_cap:.0f} mm: "
                 f"2 on the hammer loop, 1 on the rule pocket, and pocket corners; "
                 f"each at a load-path termination, stepped in off both edges."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm throughout."},
        {"item": "tool loop webbing / self strips", "qty": N_LOOPS, "unit": "loop",
         "note": f"{N_LOOPS} loops at a SOLVED pitch of {LOOP_PITCH:.1f} mm across "
                 f"a MEASURED {LOOP_PANEL_W:.0f} mm panel."},
    ]
    pattern.metadata = {
        "fc400_rank": 302,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "denim-14oz",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "hem_width": round(hem_width, 1),
            "band_length": round(BAND_LENGTH, 1),
            "hammer_loop_cut": round(HAMMER_LOOP_CUT, 1),
            "loop_panel_width": round(LOOP_PANEL_W, 1),
            "rule_pocket_width": round(RULE_W, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "hammer_loop_run_mm": round(HAMMER_LOOP_RUN, 2),
            "tool_clearance_mm": round(tool_clearance, 2),
            "loop_count": N_LOOPS,
            "loop_pitch_solved_mm": round(LOOP_PITCH, 2),
            "loop_panel_requested_mm": round(_LOOP_PANEL_RAW, 2),
            "loop_panel_clamped_mm": round(LOOP_PANEL_W, 2),
            "loop_panel_was_clamped": bool(abs(LOOP_PANEL_W - _LOOP_PANEL_RAW) > 0.01),
            "rule_width_requested_mm": round(_RULE_W_RAW, 2),
            "rule_width_clamped_mm": round(RULE_W, 2),
            "rule_width_was_clamped": bool(abs(RULE_W - _RULE_W_RAW) > 0.01),
            "rivet_cap_mm": round(rivet_cap, 2),
            "note": "the hammer loop is cut to a MEASURED swing (twice the tool "
                    "clearance plus the strap run), not a fixed strip; the tool "
                    "loops are pitched across the MEASURED panel with whole gaps "
                    "recomputed so the last loop lands on the panel; and the rule "
                    "pocket and loop panel are both clamped against the leg they "
                    "sit on, because an inverted piece is CCW-normalized by the "
                    "kernel and passes verify() looking healthy.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm",
        "hardware": "rivets via Yantra4D (notion.hardware_ref -> rivet); the solid's "
                    "cap_dia — the flange that bears on the cloth — is fed from this "
                    "garment's rivet_cap, which also sets every rivet's step-in from "
                    "the edges it lands between. The tool loops and pocket rivets are "
                    "marked; one bridged solid per notion.",
    }
    return pattern


result = build()
