"""
Denim Short Overall (Shortall) — Fashion Cabinet Garment Cartridge
(FC-400 #305, denim, T2).

The adult shortall: a bib front, a back with two crossing straps that fasten with
sliding overall buckles, side-button openings at the waist, and short legs cut off
above the knee. The whole load hangs off the shoulders through the straps, so the
strap length is the number that has to be right.

Three things are solved by measurement rather than by formula:

  1. THE STRAP LENGTH IS A MEASURED PATH WITH THE BUCKLE'S TRAVEL CENTRED ON IT.
     A shortall strap runs from the bib top, over the shoulder, crossing to the
     opposite back waist. That path is DERIVED from the measured bib height, the
     measured back rise and a shoulder arc — never entered — and the overall
     buckle's adjustment range is centred on it. A strap cut to a guessed length
     runs out of buckle travel and the bib either strangles or sags.

  2. THE SIDE OPENING IS RECONCILED WITH THE WAIST GIRTH. A shortall is stepped
     into over the head, so the side seams open at the waist and button. The
     opening length is taken out of the side seam and the button run solved
     across it, so the last button lands on cloth and not on the leg hem.

  3. THE BIB IS CLAMPED AGAINST THE WAIST IT SEWS TO. A bib wider than the front
     waist it joins is a piece that pleats itself shut, and — because the kernel
     CCW-normalizes an inverted outline and area() takes an absolute value — such
     a piece renders and passes verify() looking healthy. The bib width and the
     button count are both clamped and reported.

DENIM CONVENTIONS, per the family (bib-overalls, toddler-play-dungarees): 7 mm
twin-needle topstitch; every hard good a Yantra4D reference. The OVERALL-BUCKLE
SOLID is Yantra4D territory (`overall-buckle`; see notion.hardware_ref).

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


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|bib|strap|set

hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 840.0))
short_length = float(PARAM(lambda: short_length, 330.0))    # crotch to short hem
back_rise = float(PARAM(lambda: back_rise, 320.0))
bib_height = float(PARAM(lambda: bib_height, 300.0))        # waist to bib top
bib_width = float(PARAM(lambda: bib_width, 300.0))          # full bib top width
strap_width = float(PARAM(lambda: strap_width, 38.0))
hem_width = float(PARAM(lambda: hem_width, 300.0))          # flat short hem
side_buttons = float(PARAM(lambda: side_buttons, 3.0))
button_head = float(PARAM(lambda: button_head, 17.0))       # overall-buckle catch
wear_ease = float(PARAM(lambda: wear_ease, 100.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 32.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hip_girth = max(720.0, min(hip_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1200.0))
short_length = max(180.0, min(short_length, 520.0))
back_rise = max(240.0, min(back_rise, 420.0))
bib_height = max(200.0, min(bib_height, 420.0))
bib_width = max(200.0, min(bib_width, 460.0))
strap_width = max(24.0, min(strap_width, 60.0))
hem_width = max(220.0, min(hem_width, 480.0))
side_buttons = max(1.0, min(round(side_buttons), 6.0))
button_head = max(11.0, min(button_head, 24.0))
wear_ease = max(40.0, min(wear_ease, 220.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 50.0))

TOPSTITCH = 7.0
N_SIDE_BUTTONS = int(side_buttons)

# ── Derived block dimensions, clamped ────────────────────────────────────────
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.72, min((waist_girth + wear_ease) / 4.0,
                                            QUARTER_HIP - 6.0))
FRONT_RISE = max(160.0, back_rise - 40.0)
HALF_HEM = hem_width / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.13)
FORK_B = max(34.0, QUARTER_HIP * 0.21)
# The bib clamped against the front waist it sews to.
_BIB_HALF_RAW = bib_width / 2.0
BIB_HALF = max(strap_width + 20.0, min(_BIB_HALF_RAW, QUARTER_WAIST - 12.0))

# The side opening: taken out of the top part of the side seam, buttoned.
SIDE_SEAM_LEN = FRONT_RISE + short_length
OPENING_LEN = max(80.0, min(back_rise * 0.75, SIDE_SEAM_LEN - hem_allowance - 40.0))
BUTTON_END_CLEAR = max(button_head * 1.2, 30.0)
BUTTON_RUN = max(button_head * 2.0, OPENING_LEN - 2.0 * BUTTON_END_CLEAR)
N_INTERVALS = max(1, N_SIDE_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS


def _cross(label, x, y, arm=None):
    a = arm if arm is not None else max(3.0, button_head * 0.35)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


# ── Inseams solved equal ─────────────────────────────────────────────────────
def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, FRONT_RISE), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, back_rise), fc.P(HALF_HEM, 0.0), bulge=0.0, side=-1.0)])
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
    """Front short leg, cut 2 mirrored. Its waist sews to the bib."""
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, FRONT_RISE)
    p_waist_in = fc.P(QUARTER_WAIST, FRONT_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_F, FRONT_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, FRONT_RISE - FRONT_RISE * 0.42),
            fc.P(QUARTER_HIP + FORK_F * 0.35, FRONT_RISE * 0.18),
            p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    internals = [
        fc.Internal("outseam topstitch",
                    [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, FRONT_RISE)],
                    kind="trace"),
    ]
    # The side-opening button run, solved up the side seam from the hem clearance.
    y0 = FRONT_RISE + short_length - BUTTON_END_CLEAR - (SIDE_SEAM_LEN - OPENING_LEN)
    for i in range(N_SIDE_BUTTONS):
        internals.append(_cross(f"side button-{i + 1}",
                                seam_allowance + button_head * 0.6,
                                max(hem_allowance + button_head,
                                    y0 - BUTTON_PITCH * i)))
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / bib match"),
                 fc.Notch("side", 1.0 - OPENING_LEN / SIDE_SEAM_LEN, "opening top"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, short_length * 0.2),
                               fc.P(QUARTER_HIP * 0.42, FRONT_RISE * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back short leg, cut 2 mirrored. The straps buckle at the raised CB waist."""
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, FRONT_RISE)          # side matches front height
    p_waist_in = fc.P(QUARTER_WAIST, back_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_B, back_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in,
            fc.P(QUARTER_HIP - 6.0, back_rise - back_rise * 0.42),
            fc.P(QUARTER_HIP + FORK_B * 0.35, back_rise * 0.18),
            p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("side", 1.0 - OPENING_LEN / SIDE_SEAM_LEN, "opening top"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, short_length * 0.2),
                               fc.P(QUARTER_HIP * 0.42, back_rise * 0.9)),
        internals=[
            fc.Internal("outseam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, FRONT_RISE)],
                        kind="trace"),
            _cross("strap catch", QUARTER_WAIST * 0.5, back_rise - 22.0),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


def build_bib():
    """Bib front, cut 1 on the CF fold. Its bottom sews to the front waists."""
    h = bib_height
    edges = [
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        fc.Edge("bib_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(QUARTER_WAIST, 0.0))]),
        fc.Edge("bib_side", [fc.Line(fc.P(QUARTER_WAIST, 0.0), fc.P(BIB_HALF, h))]),
        fc.Edge("bib_top", [fc.Line(fc.P(BIB_HALF, h), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "bib", edges,
        seam_allowance=seam_allowance,
        allowances={"bib_top": hem_allowance * 0.6, "cf_fold": 0.0},
        notches=[fc.Notch("bib_bottom", 1.0, "front-leg waist match"),
                 fc.Notch("bib_side", 1.0, "buckle corner")],
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 15.0), fc.P(BIB_HALF * 0.5, h - 15.0)),
        internals=[
            fc.Internal("bib topstitch",
                        [fc.P(0.0, h - TOPSTITCH),
                         fc.P(BIB_HALF - TOPSTITCH, h - TOPSTITCH),
                         fc.P(QUARTER_WAIST - TOPSTITCH, TOPSTITCH)], kind="trace"),
            _cross("buckle catch",
                   max(BIB_HALF * 0.4, BIB_HALF - strap_width * 0.9),
                   h - max(16.0, strap_width * 0.55),
                   arm=max(4.0, strap_width * 0.22)),
            fc.Internal("bib pocket placement",
                        [fc.P(0.0, h * 0.2), fc.P(BIB_HALF * 0.8, h * 0.2),
                         fc.P(BIB_HALF * 0.8, h * 0.72), fc.P(0.0, h * 0.72),
                         fc.P(0.0, h * 0.2)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Bib (cut on fold)",
    )


# ── The strap path, MEASURED, with buckle travel centred on it ───────────────
_BIB = build_bib()
SHOULDER_ARC = max(120.0, QUARTER_HIP * 0.34)
STRAP_PATH = bib_height + back_rise + SHOULDER_ARC
BUCKLE_TRAVEL = max(60.0, STRAP_PATH * 0.16)
STRAP_CUT = STRAP_PATH + BUCKLE_TRAVEL + 2.0 * seam_allowance


def build_strap():
    """A crossing back strap, cut 2. Buckles at the bib, caught at the back waist."""
    w = strap_width * 2.0 + 2.0 * seam_allowance
    ln = STRAP_CUT
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("waist_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "back waist end"),
                 fc.Notch("lower", 1.0, "buckle end")],
        grainline=fc.Grainline(fc.P(ln * 0.12, w / 2.0), fc.P(ln * 0.88, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("buckle travel",
                        [fc.P(ln - seam_allowance - BUCKLE_TRAVEL, w / 2.0),
                         fc.P(ln - seam_allowance, w / 2.0)], kind="marking"),
            fc.Internal("nominal buckle position",
                        [fc.P(ln - seam_allowance - BUCKLE_TRAVEL / 2.0, 0.0),
                         fc.P(ln - seam_allowance - BUCKLE_TRAVEL / 2.0, w)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Crossing strap (cut 2)",
    )


def build():
    pattern = fc.PatternSet("denim-overall-short")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "bib": everything or target_piece == "bib",
        "strap": everything or target_piece == "strap",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["bib"]:
        pattern.add(build_bib())
    if want["strap"]:
        pattern.add(build_strap())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["bib"] and want["front_leg"]:
        pattern.declare_seam(("bib", "bib_bottom"), ("front_leg", "waist"), tol=0.6)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "mezclilla-denim, 10 oz (339 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; 10 oz for a shortall "
                 f"— lighter than trousers, it is worn over a lot of skin."},
        {"item": "overall buckle + catch button", "qty": 2, "unit": "set",
         "note": f"Yantra4D overall-buckle (notion.hardware_ref) on a "
                 f"{strap_width:.0f} mm strap; {BUCKLE_TRAVEL:.0f} mm of travel "
                 f"centred on a MEASURED strap path of {STRAP_PATH:.0f} mm."},
        {"item": "side-opening button", "qty": N_SIDE_BUTTONS * 2, "unit": "piece",
         "note": f"{N_SIDE_BUTTONS} per side at a SOLVED pitch of "
                 f"{BUTTON_PITCH:.1f} mm across a {OPENING_LEN:.0f} mm opening."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm throughout."},
    ]
    pattern.metadata = {
        "fc400_rank": 305,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "denim-10oz",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(FRONT_RISE, 1),
            "back_rise": round(back_rise, 1),
            "bib_height": round(bib_height, 1),
            "bib_half_width": round(BIB_HALF, 1),
            "short_length": round(short_length, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "strap_path_measured_mm": round(STRAP_PATH, 2),
            "buckle_travel_mm": round(BUCKLE_TRAVEL, 2),
            "side_opening_len_mm": round(OPENING_LEN, 2),
            "side_button_count": N_SIDE_BUTTONS,
            "side_button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(BIB_HALF, 2),
            "bib_half_was_clamped": bool(abs(BIB_HALF - _BIB_HALF_RAW) > 0.01),
            "note": "the strap is cut to a MEASURED path (bib + back rise + "
                    "shoulder arc) with the overall buckle's travel centred on it, "
                    "so a wearer does not run out of adjustment. The side opening "
                    "is taken out of the side seam and its buttons solved across "
                    "the measured opening. The bib is clamped against the front "
                    "waist it sews to, because an inverted piece is CCW-normalized "
                    "by the kernel and passes verify() looking healthy.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm",
        "hardware": "sliding overall buckles via Yantra4D (notion.hardware_ref -> "
                    "overall-buckle); the solid's strap_w — the parameter driving "
                    "its strap_slot flange — is fed from this garment's strap_width, "
                    "which also sizes the strap the buckle slides on. The side "
                    "buttons are a second finding, marked and counted.",
    }
    return pattern


result = build()
