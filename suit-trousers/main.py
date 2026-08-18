"""
Suit trousers — FC-100 rank #68. Fashion Cabinet Garment Cartridge.

The dress-trousers block finished as the trouser half of a suit: front/back
legs (cut 2 each) with the front inseam bowed by a solved amount to match the
deeper back fork, a grown-on fly extension with a fly J-topstitch guide and a
fly-stop notch, and — the suit-trouser signature — one or two FORWARD pleats
whose intake is CUT INTO the front waist edge (the leg is drafted wider at the
waist, the pleats fold that surplus away), so the waist band still finishes to
the measured waist: the pleat intake is declared as waistband seam ease. A
proper two-half waistband (one half extended into a crossover tab with a
hook-and-bar cross-mark) is verified against the pleated front + darted back
waists. Full-length pressed CREASES carry the grainline down the centre of the
front AND back legs. Back waist darts, a single-welt back pocket marking, and
slant side-pocket marks complete the tailoring. The hem is cuffed OR plain
(a cuff_depth param drives a turn-up marking + the extra hem allowance a cuff
needs), and a `lined` checkbox notes a knee-length front lining in the BOM.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
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


target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth     = float(PARAM(lambda: hip_girth, 1020.0))
waist_girth   = float(PARAM(lambda: waist_girth, 880.0))
inseam_length = float(PARAM(lambda: inseam_length, 800.0))
front_rise    = float(PARAM(lambda: front_rise, 285.0))
back_rise     = float(PARAM(lambda: back_rise, 330.0))
woven_ease    = float(PARAM(lambda: woven_ease, 85.0))
hem_width     = float(PARAM(lambda: hem_width, 100.0))     # front half-hem, flat
pleat_count   = int(PARAM(lambda: pleat_count, 2))         # 1 or 2 forward pleats
pleat_depth   = float(PARAM(lambda: pleat_depth, 30.0))    # intake per pleat
fly_width     = float(PARAM(lambda: fly_width, 38.0))
fly_depth     = float(PARAM(lambda: fly_depth, 205.0))
cuff_depth    = float(PARAM(lambda: cuff_depth, 40.0))     # 0 = plain hem
lined         = bool(PARAM(lambda: lined, True))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 45.0))  # blind-hem depth

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(40.0, min(woven_ease, 400.0))
hem_width = max(80.0, min(hem_width, 260.0))
pleat_count = max(1, min(pleat_count, 2))
pleat_depth = max(15.0, min(pleat_depth, 45.0))
fly_width = max(20.0, min(fly_width, 60.0))
fly_depth = max(80.0, min(fly_depth, front_rise - 30.0))
cuff_depth = max(0.0, min(cuff_depth, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

HIP_E = hip_girth + woven_ease
WAIST_E = waist_girth + 40.0                 # waist wearing ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
HIP_LINE_Y = CROTCH_Y + front_rise * 0.4
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0       # crisp suit taper via default 100

DART_INTAKE, DART_LEN = 12.0, 95.0
TAB = 60.0                                   # waistband crossover-tab extension
BAND_H = 40.0                                # finished waistband height (folded)
SEC_PLEAT_OFF = 46.0                         # secondary pleat: offset toward side
POCKET_DROP, POCKET_OPEN = 40.0, 155.0       # slant side pocket: below waist, span
WELT_W, WELT_H = 130.0, 14.0                 # single back welt: length, welt height
# Total pleat intake folded away at the front waist (cut into the waist edge and
# declared as waistband ease). One pleat = main only; two = main + secondary.
PLEAT_INTAKE = pleat_depth * float(pleat_count)
# A cuff is a turn-up: the leg is cut 2x the cuff depth longer and the surplus
# folds back on itself, so the hem allowance must clear a full turn-up.
HEM_ALLOW = max(hem_allowance, 2.0 * cuff_depth + 10.0) if cuff_depth > 0.0 else hem_allowance


def _fly_j(fw_in):
    """Fly J-topstitch guide: vertical run inside CF hooking toward the fly stop."""
    jx = fw_in - fly_width
    cy = WAIST_Y - fly_depth + fly_width + 10.0
    pts = [fc.P(jx, WAIST_Y), fc.P(jx, cy)]
    for step in range(1, 7):
        a = math.radians(180.0 + 15.0 * step)
        pts.append(fc.P(fw_in + fly_width * math.cos(a), cy + fly_width * math.sin(a)))
    return fc.Internal("fly J topstitch", pts, kind="trace")


def _slant_pocket():
    """Slant side-entry pocket mark: opening from the waist down toward the side."""
    top = WAIST_Y - POCKET_DROP
    return fc.Internal(
        "slant pocket opening",
        [fc.P(0.0, top), fc.P(0.0, top - POCKET_OPEN)],
    )


def _pleat(fold_x, width, label):
    """Forward pleat marking: two fold lines meeting the waist, bridged at hip line.

    The fold lines are `width` apart (the intake), close down to the hip line
    and are bridged by a depth rung — the intake surplus that folds toward the
    centre front so the front waist reads to the measured waist once pleated.
    """
    return fc.Internal(
        label,
        [fc.P(fold_x, WAIST_Y), fc.P(fold_x, HIP_LINE_Y),
         fc.P(fold_x + width, HIP_LINE_Y), fc.P(fold_x + width, WAIST_Y)],
    )


def _crease(hem_half, top_y, label):
    """Pressed crease: vertical at the leg centre, hem to the top (full length)."""
    x = hem_half / 2.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, top_y)])


def _cuff_line(hem_half, label):
    """Cuff turn-up line: horizontal at cuff_depth above the hem, full width."""
    return fc.Internal(label, [fc.P(0.0, cuff_depth), fc.P(hem_half, cuff_depth)])


def _back_dart(bw_run, rise_delta, frac, label):
    """Back waist dart as an internal: legs on the waist line, apex below."""
    slope = rise_delta / bw_run
    cx = bw_run * frac
    half = DART_INTAKE / 2.0
    return fc.Internal(
        label,
        [fc.P(cx - half, WAIST_Y + (cx - half) * slope),
         fc.P(cx, WAIST_Y + cx * slope - DART_LEN),
         fc.P(cx + half, WAIST_Y + (cx + half) * slope)],
        kind="dart",
    )


def _welt_pocket():
    """Single-welt back-pocket marking: one closed welt rectangle below the darts."""
    cx = BW * 0.5
    top = WAIST_Y - 95.0
    corners = [
        fc.P(cx - WELT_W / 2.0, top),
        fc.P(cx + WELT_W / 2.0, top),
        fc.P(cx + WELT_W / 2.0, top - WELT_H),
        fc.P(cx - WELT_W / 2.0, top - WELT_H),
    ]
    return fc.Internal("back welt pocket", corners + corners[:1])


def build_legs():
    # Base (finished) quarter-waists the waistband is drafted to.
    fw_base = max(FW * 0.55, min(WAIST_E / 4.0, FW * 0.95))
    bw_run = max(BW * 0.55, min(WAIST_E / 4.0 + 2.0 * DART_INTAKE, BW * 0.95))
    # The front waist is cut wider by the pleat intake; the pleats fold it back
    # to fw_base. fw_in is the drafted (pleated-out) front waist run to the fly.
    fw_in = fw_base + PLEAT_INTAKE
    rise_delta = back_rise - front_rise
    cb_y = WAIST_Y + rise_delta
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    def f_inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(f_tip, fc.P(FHW, 0.0), bulge=bulge, side=-1.0)],
        )

    b_inseam = fc.Edge(
        "inseam",
        [fc.curve_through(b_tip, fc.P(BHW, 0.0), bulge=0.0, side=-1.0)],
    )
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    # Front crotch: line down the grown-on fly extension, then a bezier that
    # rejoins the fork curve smoothly (tangent-continuous at the fly stop).
    fx = fw_in + fly_width
    fly_knee = fc.P(fx, WAIST_Y - fly_depth)
    fork_drop = (WAIST_Y - fly_depth) - CROTCH_Y
    front_crotch = fc.Edge(
        "crotch",
        [
            fc.Line(fc.P(fx, WAIST_Y), fly_knee),
            fc.Bezier(
                fly_knee,
                fc.P(fx, fly_knee.y - fork_drop * 0.5),
                fc.P(fx + (f_tip.x - fx) * 0.4, CROTCH_Y + fork_drop * 0.38),
                f_tip,
            ),
        ],
    )
    fly_frac = fly_depth / front_crotch.length(0.05)

    crease_x = FHW / 2.0
    # Pleats sit between the crease and the fly; main pleat on the crease line,
    # secondary toward the centre (only drawn when two pleats are requested).
    sec_x = max(6.0, crease_x + SEC_PLEAT_OFF)
    pocket_top_t = (WAIST_Y - POCKET_DROP) / WAIST_Y
    pocket_bot_t = (WAIST_Y - POCKET_DROP - POCKET_OPEN) / WAIST_Y

    front_internals = [
        _fly_j(fw_base),
        _slant_pocket(),
        _pleat(crease_x, pleat_depth, "main pleat"),
    ]
    if pleat_count >= 2:
        front_internals.append(_pleat(sec_x, pleat_depth, "secondary pleat"))
    front_internals.append(_crease(FHW, WAIST_Y, "front crease"))
    front_notches = [
        fc.Notch("crotch", fly_frac, "fly stop"),
        fc.Notch("side", 0.5),
        fc.Notch("inseam", 0.5),
        fc.Notch("side", pocket_top_t, "pocket"),
        fc.Notch("side", pocket_bot_t, "pocket"),
    ]
    if cuff_depth > 0.0:
        front_internals.append(_cuff_line(FHW, "front cuff line"))
        front_notches.append(fc.Notch("hem", 0.5, "cuff"))

    front = fc.Piece(
        "front",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(fx, WAIST_Y))]),
            front_crotch,
            f_inseam(bulge),
            fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": HEM_ALLOW},
        notches=front_notches,
        grainline=fc.Grainline(fc.P(crease_x, inseam_length * 0.12),
                               fc.P(crease_x, inseam_length * 0.92)),
        internals=front_internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    back_crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(bw_run, cb_y), fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                   fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
    )
    b_slope = rise_delta / bw_run
    b_crease_x = BHW / 2.0
    back_internals = [
        _back_dart(bw_run, rise_delta, 0.35, "back dart 1"),
        _back_dart(bw_run, rise_delta, 0.62, "back dart 2"),
        _welt_pocket(),
        _crease(BHW, WAIST_Y + b_crease_x * b_slope, "back crease"),
    ]
    back_notches = [fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)]
    if cuff_depth > 0.0:
        back_internals.append(_cuff_line(BHW, "back cuff line"))
        back_notches.append(fc.Notch("hem", 0.5, "cuff"))

    back = fc.Piece(
        "back",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(bw_run, cb_y))]),
            back_crotch,
            b_inseam,
            fc.Edge("hem", [fc.Line(fc.P(BHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": HEM_ALLOW},
        notches=back_notches,
        grainline=fc.Grainline(fc.P(b_crease_x, inseam_length * 0.12),
                               fc.P(b_crease_x, inseam_length * 0.92)),
        internals=back_internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back, fw_base, bw_run


def _button_cross(x, y, arm=4.0):
    """Hook-and-bar cross-mark: one drill polyline drawing a small + at (x, y)."""
    return fc.Internal(
        "waist hook mark",
        [fc.P(x - arm, y), fc.P(x + arm, y), fc.P(x, y),
         fc.P(x, y - arm), fc.P(x, y + arm)],
        kind="drill",
    )


def _band_half(name, length, label, extras):
    """One folded waistband half: a rectangle with a centre fold line."""
    band_h = 2.0 * (BAND_H + seam_allowance)
    cy = band_h / 2.0
    fold = fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fold] + extras,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build_waistbands(leg_waists):
    """Two waistband halves drafted to the PLEATED-FLAT waist.

    `leg_waists` is the measured front.waist + back.waist run (which is longer
    than the finished waist by the pleat intake — the front leg is cut wide and
    the pleats fold that surplus away). The band is cut to leg_waists minus the
    pleat intake, so the intake plus the tab or the closure allowances become
    the declared seam ease against the (longer) leg waists.
    """
    finished = leg_waists - PLEAT_INTAKE
    band_h = 2.0 * (BAND_H + seam_allowance)
    tab_len = finished + TAB + 2.0 * seam_allowance
    plain_len = finished + 2.0 * seam_allowance
    tab_line = fc.Internal(
        "tab line",
        [fc.P(tab_len - TAB, 0.0), fc.P(tab_len - TAB, band_h)],
    )
    tab_half = _band_half(
        "waistband_tab", tab_len, "Waistband Half (tab)",
        [tab_line, _button_cross(tab_len - TAB / 2.0, band_h * 0.25)],
    )
    plain_half = _band_half("waistband_plain", plain_len, "Waistband Half (plain)", [])
    return tab_half, plain_half


def build():
    pattern = fc.PatternSet("suit-trousers")
    front, back, fw_base, bw_run = build_legs()
    leg_waists = front.edge("waist").length() + back.edge("waist").length()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece in ("waistband_tab", "waistband_plain"):
        tab_half, plain_half = build_waistbands(leg_waists)
        if everything or target_piece == "waistband_tab":
            pattern.add(tab_half)
        if everything or target_piece == "waistband_plain":
            pattern.add(plain_half)

    # The front waist edge is cut wider than the pleated-flat waist by the pleat
    # intake; the band halves are drafted to (leg_waists − PLEAT_INTAKE). So on
    # each band seam the intake folds away and only the tab / closure allowances
    # remain as positive length, giving the declared ease below (delta ≈ 0).
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        pattern.declare_seam(
            [("waistband_tab", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=TAB + 2.0 * seam_allowance - PLEAT_INTAKE,
        )
        pattern.declare_seam(
            [("waistband_plain", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=2.0 * seam_allowance - PLEAT_INTAKE,
        )

    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    fabric_width = 1500.0                     # lana-peinada-traje card width
    marker_len = total_area / (fabric_width * 0.62)
    bom = [
        {"item": "lana-peinada-traje", "qty": round(marker_len / 10.0) * 10.0,
         "unit": "mm_length",
         "note": "worsted wool suiting at 1500 mm width, ~62% marker; "
                 "pre-shrink (steam/London-shrink) before cutting"},
        {"item": "waistband + fly interfacing", "qty": 1, "unit": "set",
         "note": "fusible waistband stay + fly-shield interfacing (curtain "
                 "waistband is future work)"},
    ]
    if lined:
        bom.append(
            {"item": "lining (knee-length front)", "qty": 1, "unit": "set",
             "note": "silesia/bemberg fronts lined to the knee to stop the "
                     "wool bagging; lining not drafted as geometry in v0"})
    bom += [
        {"item": "trouser hook-and-bar", "qty": 1, "unit": "set",
         "note": "waistband closure at the tab; hardware is a Yantra4D "
                 "cartridge (hook-and-bar guide), never re-implemented here"},
        {"item": "fly zipper (metal, trouser-weight)", "qty": 1, "unit": "pcs",
         "note": f"~{fly_depth:.0f} mm; hardware is a Yantra4D cartridge "
                 "(zipper-tape guide), never re-implemented here"},
        {"item": "waistband button 17 mm", "qty": 1, "unit": "pcs",
         "note": "extension-tab button under the hook-and-bar; hardware is a "
                 "Yantra4D cartridge (shank-button guide)"},
        {"item": "polyester/silk thread + universal needle 80/12", "qty": 1,
         "unit": "set", "note": "press the creases hard — set front and back "
                                "creases with steam; a sharp crease is the suit "
                                "trouser"},
    ]
    pattern.bom = bom

    pattern.metadata = {
        "fc100_rank": 68,
        "fabric_hint": "lana-peinada-traje",
        "tailoring_note": "teaching-grade: pleat intake cut into the front "
                          "waist and declared as waistband ease; single-welt "
                          "back pocket and pleats are markings (jetting/welting "
                          "is construction, not drafted); curtain waistband and "
                          "lining noted-not-drafted",
        "pleats": {"count": pleat_count, "intake_each_mm": pleat_depth,
                   "total_intake_mm": round(PLEAT_INTAKE, 1),
                   "style": "forward pleats folded toward centre front",
                   "declared_as": "waistband seam ease"},
        "crease": {"front": "leg centre, full length (carries grainline)",
                   "back": "leg centre, full length"},
        "fly": {"depth_mm": round(fly_depth, 1), "width_mm": round(fly_width, 1),
                "type": "grown-on extension, J-topstitch + fly-stop notch"},
        "hem": {"style": "cuffed" if cuff_depth > 0.0 else "plain",
                "cuff_depth_mm": round(cuff_depth, 1),
                "hem_allowance_mm": round(HEM_ALLOW, 1)},
        "lining": ("knee-length front lining in BOM (not drafted in v0)"
                   if lined else "unlined"),
        "finished_front_quarter_waist_mm": round(fw_base, 1),
        "finished_back_quarter_waist_mm": round(bw_run, 1),
        "finished_waist_half_mm": round(fw_base + bw_run, 1),
        "front_waist_edge_mm": round(front.edge("waist").length(), 1),
        "back_waist_edge_mm": round(back.edge("waist").length(), 1),
        "crotch_y_mm": round(CROTCH_Y, 1),
        "waist_y_mm": round(WAIST_Y, 1),
        "drafting": "dress-trousers block finished as suit trousers: forward "
                    "pleats cut into the front waist (intake declared as "
                    "waistband ease), solved front-inseam bow to the back fork, "
                    "grown-on fly with J-topstitch, full-length front + back "
                    "creases, back darts + single welt, cuffed-or-plain hem, "
                    "optional knee-length front lining",
    }
    return pattern


result = build()
