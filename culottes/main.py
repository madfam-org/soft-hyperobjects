"""
Culottes — FC-100 rank #80. Fashion Cabinet Garment Cartridge.

Culottes read as a DIVIDED SKIRT: the tailored trouser block (front/back legs,
cut 2 mirror each, joined at inseam + outseam) drawn wide and cropped so the
legs drape like a skirt. The legs share ONE outer construction — the same
side-waist point, the same over-hip curve, the same wide hem-outer — so the
outseam matches by construction; the front inseam is bowed by a solved amount
to match the deeper back fork. The front waist carries two knife pleats folding
toward centre front (each hiding 2× its depth); that pleat intake is drafted
into the front waist edge and declared back to the band as seam EASE, so the
straight cut-1 waistband — sized to the finished pleated-down waist + a
hook-and-bar overlap — still balances to delta 0 against the four unpleated
waist edges. The back opens at CENTRE BACK with an invisible zipper set into
the straight CB-rise seam (a zipper-stop notch on the back crotch edge), and a
hook-and-bar drill cross sits above it at the CB waist.

Honest teaching-grade simplifications: the crotch fork is a plain bezier (no
separate gusset); the back has no waist darts (a wide culotte's seat drape is
carried by the fork + side curve, not suppression), so the only waist ease is
the front pleat intake; the hem is a straight blind-hem allowance.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|waistband|set

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
waist_girth   = float(PARAM(lambda: waist_girth, 780.0))
inseam_length = float(PARAM(lambda: inseam_length, 380.0))   # cropped: knee→midcalf
front_rise    = float(PARAM(lambda: front_rise, 280.0))
back_rise     = float(PARAM(lambda: back_rise, 310.0))
woven_ease    = float(PARAM(lambda: woven_ease, 120.0))
hem_width     = float(PARAM(lambda: hem_width, 300.0))       # front half-hem, flat
pleat_depth   = float(PARAM(lambda: pleat_depth, 30.0))      # each knife pleat's fold depth
zipper_length = float(PARAM(lambda: zipper_length, 200.0))
overlap       = float(PARAM(lambda: overlap, 30.0))          # waistband hook-and-bar overlap
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))   # blind-hem depth

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 450.0))
front_rise = max(200.0, min(front_rise, 360.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
woven_ease = max(60.0, min(woven_ease, 400.0))
hem_width = max(250.0, min(hem_width, 350.0))
pleat_depth = max(10.0, min(pleat_depth, 45.0))
zipper_length = max(120.0, min(zipper_length, front_rise + inseam_length * 0.3))
overlap = max(0.0, min(overlap, 60.0))

HIP_E = hip_girth + woven_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length                     # crotch line height above hem
WAIST_Y = inseam_length + front_rise         # front waist height
HIP_LINE_Y = CROTCH_Y + front_rise * 0.35    # hip balance line
QH = HIP_E / 4.0                             # hip quarter (shared side reference)
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0  # fork extensions past hip
FHW, BHW = hem_width, hem_width + 12.0       # wide flat half-hems

PLEAT_COUNT = 2                              # knife pleats per front half
PLEAT_INTAKE = PLEAT_COUNT * 2.0 * pleat_depth   # fabric hidden across the front waist
BAND_H = 40.0                               # finished waistband height (folds double)
SIDE_RISE = 8.0                             # side seam rises slightly above the waist line


def _pleat(fold_x, depth, label):
    """Knife-pleat marking: fold line + placement line + waist fold arrow.

    The pleat spans [fold_x, fold_x + 2*depth] at the waist; folding on the
    fold line lays 2*depth of fabric under the placement line (toward CF),
    pressing the panel down to its finished waist. Arrow shows fold direction.
    """
    intake = 2.0 * depth
    x_fold = fold_x
    x_place = fold_x + intake
    return fc.Internal(
        label,
        [fc.P(x_fold, WAIST_Y), fc.P(x_fold, HIP_LINE_Y),
         fc.P(x_place, HIP_LINE_Y), fc.P(x_place, WAIST_Y),
         fc.P(x_fold + depth, WAIST_Y - 14.0), fc.P(x_place, WAIST_Y)],
        kind="marking",
    )


def build_legs():
    rise_delta = back_rise - front_rise
    # Shared outer construction: a straight outseam at x = 0 running hem → waist,
    # IDENTICAL for front and back, so the outseam matches by construction. Both
    # side seams reach the same height (WAIST_Y + SIDE_RISE); the deeper back
    # rise is taken up at the centre-back, never at the side (trouser/skirt
    # convention). Wide culottes need no hip bulge on the outseam — the fullness
    # lives in the wide hem and the inner (crotch) extension; the hip-line notch
    # still marks the balance point.
    waist_out = fc.P(0.0, WAIST_Y + SIDE_RISE)
    hem_out = fc.P(0.0, 0.0)

    def shared_side():
        return [fc.Line(hem_out, waist_out)]

    # ── inner widths (waist / crotch tip / hem-inner) ────────────────────────
    front_waist_w = WAIST_E / 4.0 + PLEAT_INTAKE     # drafted wide; pleats fold intake out
    back_waist_w = WAIST_E / 4.0                      # no back suppression
    f_tip = fc.P(QH - 6.0 + FORK_F, CROTCH_Y)
    b_tip = fc.P(QH + 6.0 + FORK_B, CROTCH_Y)
    f_hem_inner = fc.P(FHW, 0.0)
    b_hem_inner = fc.P(BHW, 0.0)

    # ── FRONT leg ────────────────────────────────────────────────────────────
    # Front crotch: CF waist point down a smooth fork to the front tip.
    f_cf = fc.P(front_waist_w, WAIST_Y)
    front_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(f_cf,
                   fc.P(front_waist_w, WAIST_Y - front_rise * 0.55),
                   fc.P(f_tip.x - (f_tip.x - front_waist_w) * 0.35, CROTCH_Y + front_rise * 0.30),
                   f_tip)],
    )

    def f_inseam(bulge):
        return fc.Edge("inseam",
                       [fc.curve_through(f_tip, f_hem_inner, bulge=bulge, side=-1.0)])

    # ── BACK leg ─────────────────────────────────────────────────────────────
    # Back crotch = straight CB rise (hosts the invisible zipper) + fork bezier.
    cb_y = WAIST_Y + rise_delta
    b_cb = fc.P(back_waist_w, cb_y)
    seat = fc.P(back_waist_w, HIP_LINE_Y + rise_delta * 0.6)   # CB rise ends at the seat
    back_crotch = fc.Edge(
        "crotch",
        [fc.Line(b_cb, seat),
         fc.Bezier(seat,
                   fc.P(back_waist_w - 6.0, HIP_LINE_Y - 10.0),
                   fc.P(b_tip.x - (b_tip.x - back_waist_w) * 0.30, CROTCH_Y + 55.0),
                   b_tip)],
    )
    b_inseam = fc.Edge("inseam",
                       [fc.curve_through(b_tip, b_hem_inner, bulge=0.0, side=-1.0)])

    # Solve the front inseam bulge so front inseam == back inseam length.
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.45
    if f_inseam(hi).length(0.05) < back_len:
        raise ValueError("front-inseam solver: back fork too long to match at max bulge")
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    # zipper-stop fraction measured DOWN the CB from the waist end of `crotch`.
    zip_frac = zipper_length / back_crotch.length(0.05)

    # Pleat fold positions: two pleats between CF and the crease, folding to CF.
    crease_x = front_waist_w * 0.5
    p1_x = max(6.0, crease_x - 2.0 * pleat_depth - 6.0)
    p2_x = crease_x + 8.0

    front = fc.Piece(
        "front",
        [
            fc.Edge("side", shared_side()),
            fc.Edge("waist", [fc.Line(waist_out, f_cf)]),
            front_crotch,
            f_inseam(bulge),
            fc.Edge("hem", [fc.Line(f_hem_inner, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[
            fc.Notch("side", 0.5, "hip line"),
            fc.Notch("inseam", 0.5),
        ],
        grainline=fc.Grainline(fc.P(FHW * 0.5, inseam_length * 0.15),
                               fc.P(FHW * 0.5, WAIST_Y - 40.0)),
        internals=[
            _pleat(p1_x, pleat_depth, "front pleat 1"),
            _pleat(p2_x, pleat_depth, "front pleat 2"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back = fc.Piece(
        "back",
        [
            fc.Edge("side", shared_side()),
            fc.Edge("waist", [fc.Line(waist_out, b_cb)]),
            back_crotch,
            b_inseam,
            fc.Edge("hem", [fc.Line(b_hem_inner, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "crotch": 15.0},   # CB seam hosts the zipper
        notches=[
            fc.Notch("side", 0.5, "hip line"),
            fc.Notch("inseam", 0.5),
            fc.Notch("crotch", zip_frac, "zipper stop"),
        ],
        grainline=fc.Grainline(fc.P(BHW * 0.5, inseam_length * 0.15),
                               fc.P(BHW * 0.5, WAIST_Y - 40.0)),
        internals=[
            # hook-and-bar drill cross at the CB waist, above the zipper top stop.
            fc.Internal("hook & bar (h)",
                        [fc.P(back_waist_w - 14.0, cb_y - 12.0),
                         fc.P(back_waist_w - 6.0, cb_y - 12.0)], kind="drill"),
            fc.Internal("hook & bar (v)",
                        [fc.P(back_waist_w - 10.0, cb_y - 16.0),
                         fc.P(back_waist_w - 10.0, cb_y - 8.0)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back, bulge


def build_waistband(front, back):
    """Straight cut-1 band = finished (pleated-down) waist + overlap + 2sa.

    The waist edges measured off the drafted legs are UNPLEATED (they include
    the front pleat intake). The finished waist the band presses onto is that
    circumference minus the two fronts' pleat intake; the difference returns as
    the declared seam ease, so the accounting closes to delta 0.
    """
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    finished = circ - 2.0 * PLEAT_INTAKE
    length = finished + overlap + 2.0 * seam_allowance
    band_h = 2.0 * (BAND_H + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,  # drafted cut-ready; end allowances live in the rectangle
        notches=[
            fc.Notch("bottom", (seam_allowance + finished * 0.25) / length, "side seam"),
            fc.Notch("bottom", (seam_allowance + finished * 0.50) / length, "CF match"),
            fc.Notch("bottom", (seam_allowance + finished * 0.75) / length, "side seam"),
        ],
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("culottes")
    front, back, bulge = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband(front, back))

    have = {piece.name for piece in pattern.pieces}
    if {"front", "back"} <= have:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
    if {"front", "back", "waistband"} <= have:
        # Four unpleated waist edges (2 fronts + 2 backs) close onto the finished
        # band bottom. Ease = the two fronts' pleat intake − the band's overlap
        # and 2sa extras, from the same formulas that drafted the geometry → delta 0.
        pattern.declare_seam(
            [("front", "waist"), ("front", "waist"), ("back", "waist"), ("back", "waist")],
            [("waistband", "bottom")],
            tol=2.5,
            ease=2.0 * PLEAT_INTAKE - (overlap + 2.0 * seam_allowance),
        )

    # ── Bill of materials ────────────────────────────────────────────────────
    fabric_width = 1450.0                        # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker efficiency"},
        {"item": "invisible zipper (CB)", "qty": round(zipper_length), "unit": "mm",
         "note": "set into the centre-back rise seam, closing at the zipper-stop "
                 "notch; hardware is a Yantra4D cartridge (zipper family), never "
                 "re-implemented here"},
        {"item": "hook-and-bar (trouser)", "qty": 1, "unit": "pcs",
         "note": "on the waistband overlap above the zipper; hardware is a "
                 "Yantra4D cartridge (hook family), never re-implemented here"},
        {"item": "fusible waistband interfacing", "qty": 1, "unit": "strip",
         "note": "stabilises the straight cut-1 band"},
        {"item": "polyester thread + universal needle 80/12", "qty": 1, "unit": "set",
         "note": "press each pleat before setting the waistband"},
    ]

    pattern.metadata = {
        "fc100_rank": 80,
        "fabric_hint": "popelina-algodon",
        "inseam_length_mm": round(inseam_length, 1),
        "front_rise_mm": round(front_rise, 1),
        "back_rise_mm": round(back_rise, 1),
        "hem_half_front_mm": round(FHW, 1),
        "hem_half_back_mm": round(BHW, 1),
        "pleat": {
            "count_per_front": PLEAT_COUNT,
            "depth_mm": round(pleat_depth, 1),
            "intake_per_front_mm": round(PLEAT_INTAKE, 1),
        },
        "inseam_bulge_solved": round(bulge, 4),
        "zipper_length_mm": round(zipper_length, 1),
        "drafting": "wide cropped divided-skirt culotte from the trouser block; "
                    "shared outer construction makes the outseam match, front "
                    "inseam bowed by a solved bulge to the deeper back fork; two "
                    "front knife pleats declared to the band as seam ease; CB "
                    "invisible-zip seam with a zipper-stop notch; teaching-grade "
                    "(plain fork, no back darts, straight blind hem)",
    }
    return pattern


result = build()
