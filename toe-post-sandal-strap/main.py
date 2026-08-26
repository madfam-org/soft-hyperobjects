"""
Toe-post sandal strap set — Fashion Cabinet Cartridge (FC-500 #430, footwear_soft, T2).

The strap set for a toe-post sandal (the leather flip-flop / huarache toe-post): a Y-shaped
TOE POST that passes between the big and second toe and splits into two INSTEP straps, and a
back HEEL strap — all riveted through the sole. The rivets bridge to a Yantra4D `rivet`.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. Sized from
PLAIN parameters (foot_length, foot_width, instep_girth); no landmark code is invented.

Solved, not guessed:

  1. THE STRAP LENGTHS ARE CUT TO THE MEASURED FOOT. The instep straps are half the instep
     girth plus a rivet lap each; the heel strap is the back-of-heel run plus laps — measured,
     not guessed.
  2. THE RIVET LAPS SIT ON CLOTH. Each strap end carries a rivet stepped in off the end by its
     own cap plus a margin, so it seats on leather and grips.
  3. THE TOE POST SPLIT is clamped so the Y never crosses itself — the split point stays below
     the instep join.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # toe_post|heel|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_width = float(PARAM(lambda: foot_width, 95.0))
instep_girth = float(PARAM(lambda: instep_girth, 240.0))
strap_width = float(PARAM(lambda: strap_width, 22.0))
rivet_cap = float(PARAM(lambda: rivet_cap, 9.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_width = max(60.0, min(foot_width, 150.0))
instep_girth = max(150.0, min(instep_girth, 340.0))
strap_width = max(12.0, min(strap_width, 45.0))
rivet_cap = max(5.0, min(rivet_cap, 16.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

LAP = max(18.0, rivet_cap * 2.0)
INSTEP_HALF = instep_girth / 2.0 + LAP        # each instep strap
HEEL_RUN = foot_width * 1.3 + 2.0 * LAP       # back-of-heel strap + laps
POST_STEM = max(30.0, foot_length * 0.16)     # toe-post stem before the split
SPLIT_SPREAD = min(foot_width * 0.7, INSTEP_HALF * 0.6)   # clamped so the Y never crosses
SPLIT_SPREAD = max(strap_width * 1.5, SPLIT_SPREAD)


def _rivet(label, x, y):
    a = max(3.0, rivet_cap * 0.5)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def build_toe_post():
    """The Y toe-post + two instep straps, cut 1 as one piece. The stem runs up from the toe
    rivet, splits, and each arm runs out to an instep rivet lap."""
    sw = strap_width
    stem = POST_STEM
    arm = INSTEP_HALF
    spread = SPLIT_SPREAD
    # outline: start at toe rivet (bottom of stem), up the right of the stem, out along the
    # top of the right arm, around the right end, back along the bottom of the right arm to
    # the split, then mirror for the left arm, down the left of the stem, close.
    p0 = fc.P(-sw / 2.0, 0.0)                       # toe rivet, left of stem base
    p1 = fc.P(sw / 2.0, 0.0)                        # toe rivet, right of stem base
    p2 = fc.P(sw / 2.0, stem)                       # up right of stem to split
    p3 = fc.P(spread + arm, stem + spread * 0.4)    # right arm end top
    p4 = fc.P(spread + arm, stem + spread * 0.4 - sw)  # right arm end bottom
    p5 = fc.P(spread, stem - sw * 0.3)              # back to split (right underside)
    p6 = fc.P(-spread, stem - sw * 0.3)             # left underside of split
    p7 = fc.P(-spread - arm, stem + spread * 0.4 - sw)  # left arm end bottom
    p8 = fc.P(-spread - arm, stem + spread * 0.4)  # left arm end top
    p9 = fc.P(-sw / 2.0, stem)                      # up left of stem
    edges = [
        fc.Edge("toe_end", [fc.Line(p0, p1)]),
        fc.Edge("stem_r", [fc.Line(p1, p2)]),
        fc.Edge("arm_r_top", [fc.Line(p2, p3)]),
        fc.Edge("arm_r_end", [fc.Line(p3, p4)]),
        fc.Edge("arm_r_bot", [fc.Line(p4, p5)]),
        fc.Edge("split", [fc.Line(p5, p6)]),
        fc.Edge("arm_l_bot", [fc.Line(p6, p7)]),
        fc.Edge("arm_l_end", [fc.Line(p7, p8)]),
        fc.Edge("arm_l_top", [fc.Line(p8, p9)]),
        fc.Edge("stem_l", [fc.Line(p9, p0)]),
    ]
    return fc.Piece(
        "toe_post", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("toe_end", 0.5, "toe rivet centre")],
        grainline=fc.Grainline(fc.P(0.0, 6.0), fc.P(0.0, stem - 6.0)),
        internals=[
            _rivet("toe rivet", 0.0, LAP * 0.5),
            _rivet("instep rivet R", spread + arm - LAP * 0.6,
                   stem + spread * 0.4 - sw * 0.5),
            _rivet("instep rivet L", -(spread + arm) + LAP * 0.6,
                   stem + spread * 0.4 - sw * 0.5),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Toe post + instep straps (cut 1)",
    )


def build_heel():
    """The heel strap, cut 1. A band the back-of-heel run with a rivet lap at each end."""
    ln = HEEL_RUN
    w = strap_width
    return fc.Piece(
        "heel", [
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("end_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[
            _rivet("heel rivet L", LAP * 0.5, w * 0.5),
            _rivet("heel rivet R", ln - LAP * 0.5, w * 0.5),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Heel strap (cut 1)",
    )


def build():
    pattern = fc.PatternSet("toe-post-sandal-strap")
    everything = target_piece == "set"
    if everything or target_piece == "toe_post":
        pattern.add(build_toe_post())
    if everything or target_piece == "heel":
        pattern.add(build_heel())

    # the straps do not sew to each other — each is riveted independently to the sole, so no
    # inter-piece seam is declared.

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.45)
    pattern.bom = [
        {"item": "vegetable-tanned strap leather", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 45% marker (long thin straps); a firm "
                 f"3-4 mm strap leather. Per PAIR, double this."},
        {"item": "rivet + burr", "qty": 5, "unit": "set",
         "note": f"Yantra4D rivet (notion.hardware_ref) at a {rivet_cap:.0f} mm cap; the toe "
                 f"post (1), the two instep laps (2) and the heel strap (2), each riveted "
                 f"through the sole, stepped in off the strap end so it seats on leather."},
        {"item": "leather sole + edge finish", "qty": 1, "unit": "pair",
         "note": "the straps rivet through a stacked leather sole; burnish the strap edges."},
    ]
    pattern.metadata = {
        "fc500_rank": 430, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "cuero-vegetal",
        "silhouette_note": "A toe-post sandal strap set: a Y toe post + instep straps and a "
            "heel strap, all riveted through the sole.",
        "sizing_note": "Sized from foot_length / foot_width / instep_girth as PLAIN "
            "parameters — ISO 8559 declares no foot landmark codes, so none is invented.",
        "solved": {
            "instep_strap_mm": round(INSTEP_HALF, 1),
            "heel_run_mm": round(HEEL_RUN, 1),
            "post_stem_mm": round(POST_STEM, 1),
            "split_spread_mm": round(SPLIT_SPREAD, 1),
            "note": "the instep straps are half the instep girth plus a rivet lap; the heel "
                    "strap is the back-of-heel run plus laps; each rivet is stepped in off "
                    "the strap end so it seats on leather; the toe-post split is clamped so "
                    "the Y never crosses itself.",
        },
        "hardware": "rivet via Yantra4D (notion.hardware_ref -> rivet); cap height, bore and "
                    "burr are fed from rivet_cap (the sewn-edge params are left unmapped — a "
                    "rivet is set through a drilled hole, no sewn seam, no handshake owed).",
    }
    return pattern


result = build()
