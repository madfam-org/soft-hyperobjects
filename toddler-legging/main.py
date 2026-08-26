"""
Toddler Footed Legging — Fashion Cabinet Garment Cartridge
(FC-400 #327, kids_baby, T1, PATTERN-ONLY).

A footed stretch legging for a toddler: a single wrap-around leg piece per side
with an attached foot, drafted for a stretch knit with NEGATIVE ease so it grips
without a waistband beyond a soft elastic casing. No hard goods — this is a
pattern-only garment (needs: pattern).

CHILD PROPORTION, NOT A SHRUNK ADULT (bodies/child-6y):
  - The rise is a large fraction of the leg (a nappy or full seat occupies it),
    and the waist is not smaller than the hip.
  - The foot is drafted to the child's OWN foot length, not scaled from the leg.

Two things are solved by measurement rather than by formula:

  1. THE KNIT NEGATIVE EASE IS APPLIED TO GIRTHS, NOT TO LENGTHS. A stretch legging
     is cut SMALLER than the body around (so it grips) but TRUE to length (so it is
     not short). The negative ease is subtracted from the hip and ankle girths
     only; the rise and inside leg keep their measured length. A legging cut
     smaller in every direction is short in the body and pulls the foot off.

  2. THE FOOT IS RECONCILED WITH THE ANKLE. The foot's opening (where it joins the
     leg) is drafted to the MEASURED ankle girth (less its own negative ease), so
     the foot seam closes — a foot drawn to a guessed opening either gaps at the
     ankle or gathers.

PATTERN-ONLY: no notion, no hardware_ref. The only closure is a soft elastic in a
turned waist casing, which is a technique, not a hard good.

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
# leg|foot|set

hip_girth = float(PARAM(lambda: hip_girth, 580.0))
inside_leg = float(PARAM(lambda: inside_leg, 330.0))
back_rise = float(PARAM(lambda: back_rise, 220.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 160.0))
foot_length = float(PARAM(lambda: foot_length, 130.0))
knit_stretch = float(PARAM(lambda: knit_stretch, 0.14))    # negative ease fraction
waist_casing = float(PARAM(lambda: waist_casing, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

hip_girth = max(440.0, min(hip_girth, 760.0))
inside_leg = max(180.0, min(inside_leg, 520.0))
back_rise = max(150.0, min(back_rise, 320.0))
ankle_girth = max(110.0, min(ankle_girth, 240.0))
foot_length = max(90.0, min(foot_length, 200.0))
knit_stretch = max(0.05, min(knit_stretch, 0.30))
waist_casing = max(18.0, min(waist_casing, 50.0))
seam_allowance = max(6.0, min(seam_allowance, 14.0))

# NEGATIVE EASE applied to GIRTHS only, never to lengths.
QUARTER_HIP = (hip_girth * (1.0 - knit_stretch)) / 4.0
FRONT_RISE = max(80.0, back_rise - 24.0)
HALF_ANKLE = (ankle_girth * (1.0 - knit_stretch)) / 2.0
FORK = max(12.0, QUARTER_HIP * 0.18)


def build_leg():
    """One wrap-around leg per side, cut 2 mirrored. Foot joins at the ankle."""
    p_ankle_in = fc.P(0.0, 0.0)
    p_ankle_out = fc.P(HALF_ANKLE, 0.0)
    p_waist_out = fc.P(QUARTER_HIP, back_rise + inside_leg)
    p_waist_in = fc.P(-FORK, back_rise + inside_leg)
    edges = [
        fc.Edge("ankle", [fc.Line(p_ankle_in, p_ankle_out)]),
        fc.Edge("outseam", [fc.Line(p_ankle_out, p_waist_out)]),
        fc.Edge("waist", [fc.Line(p_waist_out, p_waist_in)]),
        # The inseam+crotch: from the waist inner down to the ankle inner, curving
        # through the fork.
        fc.Edge("inseam", [fc.Bezier(
            p_waist_in, fc.P(-FORK * 0.4, back_rise * 0.8),
            fc.P(FORK * 0.3, inside_leg * 0.4), p_ankle_in)]),
    ]
    return fc.Piece(
        "leg", edges,
        seam_allowance=seam_allowance,
        allowances={"waist": waist_casing},
        notches=[fc.Notch("waist", 1.0, "CB"),
                 fc.Notch("ankle", 0.5, "foot join centre")],
        grainline=fc.Grainline(fc.P(HALF_ANKLE * 0.5, 20.0),
                               fc.P(QUARTER_HIP * 0.5, back_rise + inside_leg - 20.0)),
        internals=[
            fc.Internal("waist elastic casing",
                        [fc.P(-FORK + 5.0, back_rise + inside_leg - waist_casing),
                         fc.P(QUARTER_HIP - 5.0, back_rise + inside_leg - waist_casing)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Leg (cut 2, mirrored)",
    )


def build_foot():
    """The footed sole+upper, cut 2 mirrored. Opening = the MEASURED ankle."""
    ln = foot_length
    # The foot's flat opening matches the leg's flat ankle edge (HALF_ANKLE); both
    # pieces are cut 2 and folded, so the sewn ankle circumference reconciles. Drawn
    # as a clean four-sided sole+upper so it cannot degenerate at the extremes.
    open_w = HALF_ANKLE
    sole_w = max(open_w * 1.1, 40.0)
    edges = [
        fc.Edge("opening", [fc.Line(fc.P(0.0, 0.0), fc.P(open_w, 0.0))]),
        fc.Edge("heel", [fc.Line(fc.P(open_w, 0.0), fc.P(sole_w, -ln))]),
        fc.Edge("toe", [fc.curve_through(
            fc.P(sole_w, -ln), fc.P(0.0, -ln), bulge=0.20, side=-1.0)]),
        fc.Edge("instep", [fc.Line(fc.P(0.0, -ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "foot", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("opening", 0.5, "ankle join centre")],
        grainline=fc.Grainline(fc.P(open_w * 0.5, -ln * 0.1), fc.P(open_w * 0.5, -ln * 0.85)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Foot (cut 2, mirrored)",
    )


def build():
    pattern = fc.PatternSet("toddler-legging")
    everything = target_piece == "set"
    want = {
        "leg": everything or target_piece == "leg",
        "foot": everything or target_piece == "foot",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["leg"]:
        pattern.add(build_leg())
    if want["foot"]:
        pattern.add(build_foot())

    if want["leg"] and want["foot"]:
        # The foot opening is drafted to the MEASURED ankle so the join closes.
        pattern.declare_seam(("leg", "ankle"), ("foot", "opening"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "cotton-lycra jersey (stretch)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 78% marker; a 4-way stretch "
                 f"cotton-lycra gives grip without a hard waistband."},
        {"item": "soft knit elastic (waist casing)", "qty": 1, "unit": "length",
         "note": f"{waist_casing:.0f} mm turned casing at the waist — the only "
                 f"closure; no hard goods (pattern-only garment)."},
        {"item": "ballpoint needle 75/11 + stretch/overlock thread", "qty": 1,
         "unit": "spool", "note": "sew on a stretch stitch or overlock — a straight "
                 "stitch pops when the legging stretches on."},
    ]
    pattern.metadata = {
        "fc400_rank": 327,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "cotton-lycra",
        "pattern_only": True,
        "finished_mm": {
            "quarter_hip_negative_ease": round(QUARTER_HIP, 1),
            "front_rise": round(FRONT_RISE, 1),
            "back_rise": round(back_rise, 1),
            "inside_leg": round(inside_leg, 1),
            "half_ankle_negative_ease": round(HALF_ANKLE, 1),
            "foot_length": round(foot_length, 1),
        },
        "solved": {
            "knit_stretch_fraction": round(knit_stretch, 3),
            "hip_girth_measured_mm": round(hip_girth, 1),
            "hip_girth_cut_mm": round(hip_girth * (1.0 - knit_stretch), 1),
            "ankle_girth_measured_mm": round(ankle_girth, 1),
            "ankle_girth_cut_mm": round(ankle_girth * (1.0 - knit_stretch), 1),
            "lengths_kept_true": True,
            "note": "the knit negative ease is applied to GIRTHS only (hip, ankle) — "
                    "the legging is cut smaller around so it grips, but TRUE to "
                    "length (rise, inside leg) so it is not short and does not pull "
                    "the foot off. The foot opening is drafted to the measured "
                    "ankle (less its own negative ease) so the foot seam closes.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y)",
            "rise_over_nappy": f"front rise {FRONT_RISE:.0f} mm vs back "
                               f"{back_rise:.0f} mm",
            "foot_from_measure": "the foot is drafted to the child's own foot "
                                 "length, not scaled from the leg",
        },
        "hardware": "none — pattern-only garment; the only closure is a soft "
                    "elastic in a turned waist casing (a technique, not a hard good).",
    }
    return pattern


result = build()
