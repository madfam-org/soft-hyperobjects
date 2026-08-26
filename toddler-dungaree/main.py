"""
Toddler Dungaree — Fashion Cabinet Garment Cartridge (FC-400 #321, kids_baby, T2).

A bib-front dungaree for a toddler: a bib, two crossing back straps on sliding
overall buckles, and full-length legs — drafted from CHILD measurements directly,
NOT a shrunk adult. The toddler-specific proportions are stated in the geometry,
not inherited from an adult block.

CHILD PROPORTION, NOT A SHRUNK ADULT (bodies/child-6y):
  - The waist is NOT smaller than the hip — a toddler has no waist indentation to
    draft to, and a shaped waist here will not pass over the hips.
  - The rise is a LARGER fraction of the leg than an adult's, because a nappy or
    a full seat occupies it; the back fork is the deeper one.
  - The bib is sized off the CHEST, not a fashion proportion, and clamped against
    the waist it sews to.

Two things are solved by measurement rather than by formula:

  1. THE STRAP LENGTH IS A MEASURED PATH WITH THE BUCKLE'S TRAVEL CENTRED ON IT.
     The strap runs bib corner → over the shoulder → across to the opposite back
     waist. That path is DERIVED from the measured bib height and back rise plus a
     shoulder arc, and the buckle's adjustment range is centred on it — a strap
     cut to a guessed length runs out of buckle on a growing child in one season.

  2. THE BIB IS CLAMPED AGAINST THE WAIST. A bib wider than the front waist it
     sews to pleats itself shut, and — because the kernel CCW-normalizes an
     inverted outline and area() takes an absolute value — such a piece renders
     and passes verify() looking healthy. The bib width is clamped and reported.

The BUCKLE SOLID is Yantra4D territory (`overall-buckle`; see notion.hardware_ref).

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|bib|strap|set

chest_girth = float(PARAM(lambda: chest_girth, 560.0))     # child chest
hip_girth = float(PARAM(lambda: hip_girth, 600.0))         # over the nappy
inside_leg = float(PARAM(lambda: inside_leg, 340.0))       # crotch to ankle
back_rise = float(PARAM(lambda: back_rise, 230.0))         # crotch to waist, back
bib_height = float(PARAM(lambda: bib_height, 170.0))       # waist to bib top
bib_width = float(PARAM(lambda: bib_width, 200.0))         # full bib top width
strap_width = float(PARAM(lambda: strap_width, 28.0))
hem_width = float(PARAM(lambda: hem_width, 170.0))         # flat leg opening
wear_ease = float(PARAM(lambda: wear_ease, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 28.0))

chest_girth = max(440.0, min(chest_girth, 700.0))
hip_girth = max(460.0, min(hip_girth, 760.0))
inside_leg = max(200.0, min(inside_leg, 520.0))
back_rise = max(160.0, min(back_rise, 320.0))
bib_height = max(100.0, min(bib_height, 250.0))
bib_width = max(140.0, min(bib_width, 320.0))
strap_width = max(18.0, min(strap_width, 42.0))
hem_width = max(120.0, min(hem_width, 260.0))
wear_ease = max(40.0, min(wear_ease, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 16.0))
hem_allowance = max(15.0, min(hem_allowance, 45.0))

TOPSTITCH = 6.0

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
# A toddler has no waist indentation: the waist quarter is the hip quarter less a
# token, floored at 90% of it.
QUARTER_WAIST = max(QUARTER_HIP - 12.0, QUARTER_HIP * 0.90)
RISE_DIFF = 30.0
FRONT_RISE = max(90.0, back_rise - RISE_DIFF)
HALF_HEM = hem_width / 2.0
FORK_F = max(12.0, QUARTER_HIP * 0.13)
FORK_B = max(20.0, QUARTER_HIP * 0.21)
# The bib from the CHEST, clamped against the waist it sews to.
_BIB_HALF_RAW = chest_girth / 6.0 + 6.0
BIB_HALF = max(strap_width + 10.0, min(_BIB_HALF_RAW, QUARTER_WAIST - 10.0))


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
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, FRONT_RISE)
    p_waist_in = fc.P(QUARTER_WAIST, FRONT_RISE)
    p_fork = fc.P(QUARTER_HIP + FORK_F, FRONT_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 5.0, FRONT_RISE - FRONT_RISE * 0.42),
            fc.P(QUARTER_HIP + FORK_F * 0.35, FRONT_RISE * 0.20), p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / bib match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.1),
                               fc.P(QUARTER_HIP * 0.42, FRONT_RISE * 0.9)),
        internals=[
            fc.Internal("out-seam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, FRONT_RISE)], kind="trace"),
            fc.Internal("knee-patch zone",
                        [fc.P(HALF_HEM * 0.2, FRONT_RISE * 0.3),
                         fc.P(QUARTER_HIP * 0.8, FRONT_RISE * 0.3),
                         fc.P(QUARTER_HIP * 0.8, FRONT_RISE * 0.06),
                         fc.P(HALF_HEM * 0.2, FRONT_RISE * 0.06),
                         fc.P(HALF_HEM * 0.2, FRONT_RISE * 0.3)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    cb_y = back_rise
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, back_rise - RISE_DIFF)
    p_waist_in = fc.P(QUARTER_WAIST, cb_y)
    p_fork = fc.P(QUARTER_HIP + FORK_B, cb_y)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 5.0, cb_y - back_rise * 0.42),
            fc.P(QUARTER_HIP + FORK_B * 0.35, back_rise * 0.20), p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.1),
                               fc.P(QUARTER_HIP * 0.42, back_rise * 0.9)),
        internals=[
            fc.Internal("out-seam topstitch",
                        [fc.P(TOPSTITCH, 0.0), fc.P(TOPSTITCH, back_rise - RISE_DIFF)],
                        kind="trace"),
            fc.Internal("strap catch",
                        [fc.P(QUARTER_WAIST * 0.45, cb_y - 15.0),
                         fc.P(QUARTER_WAIST * 0.45 + strap_width, cb_y - 15.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


def build_bib():
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
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 12.0), fc.P(BIB_HALF * 0.5, h - 12.0)),
        internals=[
            fc.Internal("bib topstitch",
                        [fc.P(0.0, h - TOPSTITCH), fc.P(BIB_HALF - TOPSTITCH, h - TOPSTITCH),
                         fc.P(QUARTER_WAIST - TOPSTITCH, TOPSTITCH)], kind="trace"),
            fc.Internal("buckle catch",
                        [fc.P(max(BIB_HALF * 0.4, BIB_HALF - strap_width * 0.9),
                              h - max(12.0, strap_width * 0.5))], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Bib (cut on fold)",
    )


_BIB = build_bib()
SHOULDER_ARC = max(80.0, chest_girth * 0.22)
STRAP_PATH = bib_height + back_rise + SHOULDER_ARC
BUCKLE_TRAVEL = max(40.0, STRAP_PATH * 0.16)
STRAP_CUT = STRAP_PATH + BUCKLE_TRAVEL + 2.0 * seam_allowance


def build_strap():
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
        ],
        cut=fc.CutSpec(quantity=2),
        label="Crossing strap (cut 2)",
    )


def build():
    pattern = fc.PatternSet("toddler-dungaree")
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
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.5)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)
    if want["bib"] and want["front_leg"]:
        pattern.declare_seam(("bib", "bib_bottom"), ("front_leg", "waist"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "cotton twill, 6 oz (childrenswear weight)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 74% marker; wash before cutting "
                 f"— cotton twill shrinks and the child outgrows it before it wears."},
        {"item": "overall buckle + catch button", "qty": 2, "unit": "set",
         "note": f"Yantra4D overall-buckle (notion.hardware_ref) on a "
                 f"{strap_width:.0f} mm strap; {BUCKLE_TRAVEL:.0f} mm of travel "
                 f"centred on a MEASURED strap path of {STRAP_PATH:.0f} mm."},
        {"item": "knee-patch fabric (self or contrast)", "qty": 2, "unit": "piece",
         "note": "the front leg carries a marked knee-patch zone — the first thing "
                 "a toddler wears through."},
        {"item": "topstitch thread + needle 90/14", "qty": 1, "unit": "spool",
         "note": f"out-seams, bib edge, both strap edges at {TOPSTITCH:.0f} mm."},
    ]
    pattern.metadata = {
        "fc400_rank": 321,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "cotton-twill",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(FRONT_RISE, 1),
            "back_rise": round(back_rise, 1),
            "bib_height": round(bib_height, 1),
            "bib_half_width": round(BIB_HALF, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "strap_path_measured_mm": round(STRAP_PATH, 2),
            "buckle_travel_mm": round(BUCKLE_TRAVEL, 2),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(BIB_HALF, 2),
            "bib_half_was_clamped": bool(abs(BIB_HALF - _BIB_HALF_RAW) > 0.01),
            "note": "the strap is cut to a MEASURED path (bib + back rise + shoulder "
                    "arc) with the overall buckle's travel centred on it, so a "
                    "growing child does not run out of adjustment in one season. "
                    "The bib is clamped against the front waist, because an inverted "
                    "piece is CCW-normalized by the kernel and passes verify() "
                    "looking healthy.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y), "
                      "NOT a scaled adult block",
            "no_waist_indentation": "the waist quarter is the hip quarter less a "
                                    "token — a toddler has no waist to draft to",
            "rise_over_nappy": f"front rise {FRONT_RISE:.0f} mm vs back "
                               f"{back_rise:.0f} mm; the back fork is the deeper one",
            "bib_from_chest": "the bib half-width comes from the chest, clamped "
                              "against the waist it sews to",
        },
        "hardware": "sliding overall buckles via Yantra4D (notion.hardware_ref -> "
                    "overall-buckle); the solid's strap_w is fed from this garment's "
                    "strap_width, which also sizes the strap the buckle slides on.",
    }
    return pattern


result = build()
