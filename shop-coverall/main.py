"""
Mechanic's Shop Coverall — Fashion Cabinet Garment Cartridge
(FC-400 #309, workwear_uniforms, T3).

The one-piece shop coverall: a bodice joined to a trouser at the waist, a full
centre-front two-way zipper from throat to crotch, set-in sleeves, and a stack of
chest and thigh pockets. A coverall is stepped into and zipped, so the ZIPPER
LENGTH is the number the whole garment turns on — a zip cut short of the crotch
cannot be stepped into, and a zip run long is a zip that pools at the throat.

Three things are solved by measurement rather than by formula:

  1. THE ZIPPER LENGTH IS THE MEASURED CF RUN, TO A STANDARD TAPE LENGTH. The
     centre-front seam is MEASURED from the collar break down over the bust and
     the belly to the crotch, and the zipper is specified to the nearest standard
     tape length AT OR ABOVE that run (never below — a short zip strands the
     wearer half in). The chosen length and the shortfall/overage are reported.

  2. THE BODICE AND TROUSER WAISTS ARE RECONCILED. The bodice bottom and the
     trouser top join at the waist; both are drafted to the same MEASURED waist
     quarter so the seam closes at delta zero, and the declared seam catches any
     future redraft that breaks it.

  3. THE SLEEVE CAP EASE IS TAKEN OFF THE MEASURED ARMSCYE, and the chest pocket
     is clamped against the bodice it sits on — an inverted pocket is CCW-
     normalized by the kernel into a healthy-looking piece.

WORKWEAR CONVENTIONS: 7 mm topstitch; felled seams; hard goods via Yantra4D. The
ZIPPER SOLID is Yantra4D territory (`zipper`; see notion.hardware_ref).

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
# bodice_front|bodice_back|leg_front|leg_back|sleeve|collar|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1060.0))
waist_girth = float(PARAM(lambda: waist_girth, 940.0))
hip_girth = float(PARAM(lambda: hip_girth, 1080.0))
back_width = float(PARAM(lambda: back_width, 470.0))
back_length = float(PARAM(lambda: back_length, 440.0))     # nape to waist
inside_leg = float(PARAM(lambda: inside_leg, 780.0))
front_rise = float(PARAM(lambda: front_rise, 300.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
hem_width = float(PARAM(lambda: hem_width, 250.0))
zip_chain = float(PARAM(lambda: zip_chain, 8.0))           # zipper chain size (#)
wear_ease = float(PARAM(lambda: wear_ease, 240.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 32.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(860.0, min(chest_girth, 1500.0))
waist_girth = max(700.0, min(waist_girth, 1400.0))
hip_girth = max(760.0, min(hip_girth, 1440.0))
back_width = max(380.0, min(back_width, 560.0))
back_length = max(360.0, min(back_length, 540.0))
inside_leg = max(560.0, min(inside_leg, 950.0))
front_rise = max(220.0, min(front_rise, 380.0))
sleeve_length = max(520.0, min(sleeve_length, 780.0))
hem_width = max(180.0, min(hem_width, 360.0))
zip_chain = max(5.0, min(zip_chain, 10.0))
wear_ease = max(140.0, min(wear_ease, 360.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 45.0))

TOPSTITCH = 7.0

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_CHEST * 0.72,
                    min((waist_girth + wear_ease) / 4.0, QUARTER_CHEST - 6.0))
QUARTER_HIP = (hip_girth + wear_ease) / 4.0
HALF_BACK = back_width / 2.0
HALF_NECK = max(70.0, HALF_BACK * 0.38)
NECK_DROP_F = max(70.0, HALF_NECK * 1.0)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)
SHOULDER_SLOPE = 45.0
BACK_RISE = max(front_rise + 40.0, front_rise * 1.12)
HALF_HEM = hem_width / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.14)
FORK_B = max(34.0, QUARTER_HIP * 0.22)

# Standard zipper tape lengths (mm).
STD_ZIP = [400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]


def build_bodice_front():
    hw = QUARTER_CHEST
    p_waist_cf = fc.P(0.0, 0.0)
    # The bodice narrows to the waist quarter (where it joins the trouser) and
    # sweeps out to the chest quarter at the armhole — so the waist edge MEASURES
    # QUARTER_WAIST, matching the trouser it seams to.
    p_waist_side = fc.P(QUARTER_WAIST, 0.0)
    p_armhole = fc.P(hw, back_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, back_length - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, back_length)
    p_neck_cf = fc.P(0.0, back_length - NECK_DROP_F)
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_cf, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, back_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, back_length - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.30, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_waist_cf)]),
    ]
    return fc.Piece(
        "bodice_front", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("waist", 1.0, "side seam"),
                 fc.Notch("cf", 0.0, "zip base / waist"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, back_length - 20.0)),
        internals=[
            fc.Internal("CF zip topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, back_length - NECK_DROP_F)],
                        kind="trace"),
            fc.Internal("chest pocket placement",
                        [fc.P(hw * 0.36, back_length - QUARTER_CHEST * 0.35),
                         fc.P(hw * 0.36 + QUARTER_CHEST * 0.42,
                              back_length - QUARTER_CHEST * 0.35),
                         fc.P(hw * 0.36 + QUARTER_CHEST * 0.42,
                              back_length - QUARTER_CHEST * 0.75),
                         fc.P(hw * 0.36, back_length - QUARTER_CHEST * 0.75),
                         fc.P(hw * 0.36, back_length - QUARTER_CHEST * 0.35)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice front (cut 2, mirrored)",
    )


def build_bodice_back():
    hw = QUARTER_CHEST
    p_waist_cb = fc.P(0.0, 0.0)
    p_waist_side = fc.P(QUARTER_WAIST, 0.0)   # matches the trouser back waist
    p_armhole = fc.P(hw, back_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, back_length - SHOULDER_SLOPE)
    p_neck_pt = fc.P(HALF_NECK, back_length)
    p_neck_cb = fc.P(0.0, back_length - NECK_DROP_B)
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_cb, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, back_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, back_length - SHOULDER_SLOPE + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_waist_cb)]),
    ]
    return fc.Piece(
        "bodice_back", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("waist", 1.0, "side seam"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, back_length - 20.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Bodice back (cut on fold)",
    )


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


def build_leg_front():
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.44),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18), p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "leg_front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / bodice match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, front_rise * 0.9)),
        internals=[
            fc.Internal("thigh pocket placement",
                        [fc.P(HALF_HEM * 0.2, front_rise * 0.3),
                         fc.P(HALF_HEM * 0.2 + QUARTER_HIP * 0.4, front_rise * 0.3),
                         fc.P(HALF_HEM * 0.2 + QUARTER_HIP * 0.4, front_rise * 0.05),
                         fc.P(HALF_HEM * 0.2, front_rise * 0.05),
                         fc.P(HALF_HEM * 0.2, front_rise * 0.3)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser front (cut 2, mirrored)",
    )


def build_leg_back():
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST, BACK_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.44),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18), p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "leg_back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB / bodice match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trouser back (cut 2, mirrored)",
    )


_BF = build_bodice_front()
_LF = build_leg_front()
_LB = build_leg_back()
ARMSCYE_RUN = (_BF.edge("armscye").length(0.05)
               + build_bodice_back().edge("armscye").length(0.05))
# The CF zip run: bodice CF plus the front rise (throat over belly to crotch).
CF_BODICE_RUN = _BF.edge("cf").length(0.05)
ZIP_RUN = CF_BODICE_RUN + front_rise
# Choose the standard tape length at or above the measured run.
ZIP_LENGTH = next((z for z in STD_ZIP if z >= ZIP_RUN), STD_ZIP[-1])
ZIP_OVERAGE = ZIP_LENGTH - ZIP_RUN


def build_sleeve():
    sw = QUARTER_CHEST * 0.92
    cap_h = QUARTER_CHEST * 0.30
    ln = sleeve_length
    cuff_w = sw * 0.66
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    edges = [
        fc.Edge("cap_r", [fc.Bezier(
            p_ur, fc.P(sw * 0.86, cap_h * 0.75),
            fc.P(sw * 0.60, cap_h), fc.P(sw / 2.0, cap_h))]),
        fc.Edge("cap_l", [fc.Bezier(
            fc.P(sw / 2.0, cap_h), fc.P(sw * 0.40, cap_h),
            fc.P(sw * 0.14, cap_h * 0.75), p_ul)]),
        fc.Edge("seam_l", [fc.Line(p_ul, fc.P((sw - cuff_w) / 2.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P((sw - cuff_w) / 2.0, -ln),
                                 fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln))]),
        fc.Edge("seam_r", [fc.Line(fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln), p_ur)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap_r", 1.0, "shoulder point"),
                 fc.Notch("cap_l", 0.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff topstitch",
                        [fc.P((sw - cuff_w) / 2.0 + TOPSTITCH, -ln + TOPSTITCH),
                         fc.P((sw - cuff_w) / 2.0 + cuff_w - TOPSTITCH, -ln + TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


def build_collar():
    neck_run = (_BF.edge("neck").length(0.05) * 2.0
                + build_bodice_back().edge("neck").length(0.05))
    ln = neck_run / 2.0
    depth = max(45.0, HALF_NECK * 0.55)
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("collar topstitch",
                        [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Collar (cut 2, on fold)",
    )


# Chest pocket clamped against the bodice.
_POCKET_W_RAW = QUARTER_CHEST * 0.42
POCKET_W = max(90.0, min(_POCKET_W_RAW, QUARTER_CHEST - 2.0 * seam_allowance))
POCKET_H = max(120.0, POCKET_W * 1.1)


def build_pocket():
    w = POCKET_W
    h = POCKET_H
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance * 0.6},
        notches=[fc.Notch("mouth", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, h - TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=3),
        label="Patch pocket (cut 3)",
    )


def build():
    pattern = fc.PatternSet("shop-coverall")
    everything = target_piece == "set"
    want = {
        "bodice_front": everything or target_piece == "bodice_front",
        "bodice_back": everything or target_piece == "bodice_back",
        "leg_front": everything or target_piece == "leg_front",
        "leg_back": everything or target_piece == "leg_back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bodice_front"]:
        pattern.add(build_bodice_front())
    if want["bodice_back"]:
        pattern.add(build_bodice_back())
    if want["leg_front"]:
        pattern.add(build_leg_front())
    if want["leg_back"]:
        pattern.add(build_leg_back())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["collar"]:
        pattern.add(build_collar())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.0)
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"),
                             tol=1.0)
    if want["leg_front"] and want["leg_back"]:
        pattern.declare_seam(("leg_front", "inseam"), ("leg_back", "inseam"), tol=0.4)
        pattern.declare_seam(("leg_front", "side"), ("leg_back", "side"), tol=1.0)
        pattern.declare_seam(("leg_front", "hem"), ("leg_back", "hem"), tol=1.0)
    if want["bodice_front"] and want["leg_front"]:
        # The bodice waist joins the trouser waist — both to QUARTER_WAIST.
        pattern.declare_seam(("bodice_front", "waist"), ("leg_front", "waist"), tol=0.6)
    if want["sleeve"] and want["bodice_front"] and want["bodice_back"]:
        cap = (build_sleeve().edge("cap_r").length(0.05)
               + build_sleeve().edge("cap_l").length(0.05))
        pattern.declare_seam([("sleeve", "cap_r"), ("sleeve", "cap_l")],
                             [("bodice_front", "armscye"), ("bodice_back", "armscye")],
                             tol=2.5, ease=cap - ARMSCYE_RUN)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton twill, 8 oz (workwear weight)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a coverall is the "
                 f"most cloth-hungry garment in the family."},
        {"item": "two-way separating zipper", "qty": 1, "unit": "piece",
         "note": f"Yantra4D zipper (notion.hardware_ref), #{zip_chain:.0f} chain, "
                 f"{ZIP_LENGTH:.0f} mm tape — chosen at or above the MEASURED CF "
                 f"run of {ZIP_RUN:.0f} mm (overage {ZIP_OVERAGE:.0f} mm). Two-way "
                 f"so the wearer can vent the crotch when kneeling."},
        {"item": "heavy topstitch thread + jeans needle 100/16", "qty": 1,
         "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; felled seams throughout."},
    ]
    pattern.metadata = {
        "fc400_rank": 309,
        "family": "workwear_uniforms",
        "tier": 3,
        "fabric_hint": "twill-cotton",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "quarter_hip": round(QUARTER_HIP, 1),
            "back_length": round(back_length, 1),
            "inside_leg": round(inside_leg, 1),
            "zip_length": round(ZIP_LENGTH, 1),
        },
        "solved": {
            "cf_bodice_run_mm": round(CF_BODICE_RUN, 2),
            "zip_run_measured_mm": round(ZIP_RUN, 2),
            "zip_length_chosen_mm": round(ZIP_LENGTH, 2),
            "zip_overage_mm": round(ZIP_OVERAGE, 2),
            "zip_at_or_above_run": bool(ZIP_LENGTH >= ZIP_RUN),
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "note": "the CF zip is specified to the nearest STANDARD tape length AT "
                    "OR ABOVE the measured throat-to-crotch run — never below, "
                    "because a short zip strands the wearer half in. The bodice and "
                    "trouser waists are both drafted to the same measured quarter "
                    "so the join closes at delta zero, the inseams are balanced to "
                    "zero, and the chest pocket is clamped against the bodice.",
        },
        "topstitch": f"twin-needle heavy contrast at {TOPSTITCH:.0f} mm; felled seams",
        "hardware": "two-way separating zipper via Yantra4D (notion.hardware_ref -> "
                    "zipper); the solid's zip_length is fed from this garment's "
                    "chosen standard length (solved from the measured CF run) and "
                    "its chain_size from zip_chain. One number sizes the teeth, "
                    "another the run.",
    }
    return pattern


result = build()
