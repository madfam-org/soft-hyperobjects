"""
Baby Scratch Mittens — Fashion Cabinet Garment Cartridge
(FC-400 #330, kids_baby, T1, PATTERN-ONLY).

Thumbless scratch mittens for a newborn: a rounded mitten in soft cotton
interlock with an elastic cuff, worn to stop a baby scratching its own face. No
hard goods — this is a pattern-only garment (needs: pattern). It is the smallest
garment in the whole catalog, and at that size the thing that goes wrong is the
cuff: too tight and it marks the wrist, too loose and the mitten falls off.

Two things are solved by measurement rather than by formula:

  1. THE CUFF IS RECONCILED WITH THE HAND. The mitten's widest point (the palm)
     must be wide enough for the hand to pass through the cuff, so the cuff
     opening is drafted to the MEASURED palm width plus ease — a cuff drafted to
     the wrist alone will not pass the hand, and the mitten cannot be put on.

  2. THE MITTEN IS ONE CLOSED CURVE WITH A FLOORED TIP. The mitten body is a
     rounded outline whose tip radius is floored, because at the smallest sizes a
     tip radius larger than the mitten width inverts the curve — geometry the
     kernel CCW-normalizes into a valid-looking piece. The tip is floored against
     the width and reported.

PATTERN-ONLY: no notion, no hardware_ref. The only closure is a soft elastic in a
turned cuff, which is a technique, not a hard good.

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
# mitten|cuff|set

palm_width = float(PARAM(lambda: palm_width, 55.0))       # across the palm, flat
hand_length = float(PARAM(lambda: hand_length, 70.0))     # wrist to fingertip
wrist_girth = float(PARAM(lambda: wrist_girth, 90.0))
cuff_depth = float(PARAM(lambda: cuff_depth, 28.0))
tip_radius = float(PARAM(lambda: tip_radius, 26.0))
cuff_ease = float(PARAM(lambda: cuff_ease, 14.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

palm_width = max(38.0, min(palm_width, 90.0))
hand_length = max(45.0, min(hand_length, 120.0))
wrist_girth = max(60.0, min(wrist_girth, 140.0))
cuff_depth = max(15.0, min(cuff_depth, 45.0))
tip_radius = max(10.0, min(tip_radius, 50.0))
cuff_ease = max(4.0, min(cuff_ease, 30.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

HALF_PALM = palm_width / 2.0
# The tip radius floored against the mitten width so it cannot invert the curve.
_TIP_RAW = tip_radius
TIP_R = max(6.0, min(_TIP_RAW, HALF_PALM - 4.0))
# The cuff opening must pass the HAND (palm), not just the wrist.
_CUFF_OPEN_RAW = wrist_girth / 2.0
CUFF_OPEN_HALF = max(HALF_PALM + cuff_ease / 2.0, _CUFF_OPEN_RAW)


def build_mitten():
    """The mitten body, cut 2 (one per hand's front+back on the fold, or 4 flat).

    A rounded outline: straight cuff edge at the wrist, straight sides up the palm,
    a floored round tip."""
    w = HALF_PALM
    h = hand_length
    edges = [
        fc.Edge("cuff_edge", [fc.Line(fc.P(-w, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h - TIP_R))]),
        # The rounded tip: right side up to the crown, across, down the left.
        fc.Edge("tip", [fc.curve_through(
            fc.P(w, h - TIP_R), fc.P(-w, h - TIP_R), bulge=0.55, side=-1.0)]),
        fc.Edge("side_l", [fc.Line(fc.P(-w, h - TIP_R), fc.P(-w, 0.0))]),
    ]
    return fc.Piece(
        "mitten", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("cuff_edge", 0.5, "centre / cuff join"),
                 fc.Notch("tip", 0.5, "crown")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, h - 8.0)),
        internals=[],
        cut=fc.CutSpec(quantity=4),
        label="Mitten (cut 4)",
    )


def build_cuff():
    """The elastic cuff band, cut 2. Opening drafted to pass the HAND."""
    ln = CUFF_OPEN_HALF * 2.0
    w = cuff_depth * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "cuff", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("lower", 0.5, "centre"),
                 fc.Notch("lower", 1.0, "cuff seam")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("elastic channel fold", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Elastic cuff (cut 2)",
    )


def build():
    pattern = fc.PatternSet("baby-mittens")
    everything = target_piece == "set"
    want = {
        "mitten": everything or target_piece == "mitten",
        "cuff": everything or target_piece == "cuff",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["mitten"]:
        pattern.add(build_mitten())
    if want["cuff"]:
        pattern.add(build_cuff())

    if want["mitten"] and want["cuff"]:
        # The cuff opening (its lower edge) must be wide enough for the mitten's
        # cuff edge; declared so a cuff redrafted to the wrist alone (too small to
        # pass the hand) goes red. The declared ease IS the pass-the-hand margin.
        pattern.declare_seam(("cuff", "lower"), ("mitten", "cuff_edge"),
                             tol=1.0, ease=CUFF_OPEN_HALF * 2.0 - palm_width)

    fabric_width = 1600.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "cotton interlock (soft, non-pilling)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker; interlock has no "
                 f"loose fibres a baby could pull off — safe against the face."},
        {"item": "soft knit elastic (cuff)", "qty": 1, "unit": "length",
         "note": "a gentle elastic in the turned cuff — the only closure; no hard "
                 "goods (pattern-only garment). Not so tight it marks the wrist."},
        {"item": "ballpoint needle 70/10 + stretch thread", "qty": 1, "unit": "spool",
         "note": "sew on a narrow zigzag or overlock; turn all seams inward so no "
                 "seam allowance touches the baby's skin."},
    ]
    pattern.metadata = {
        "fc400_rank": 330,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "cotton-interlock",
        "pattern_only": True,
        "finished_mm": {
            "palm_width": round(palm_width, 1),
            "hand_length": round(hand_length, 1),
            "tip_radius": round(TIP_R, 1),
            "cuff_open_width": round(CUFF_OPEN_HALF * 2.0, 1),
            "cuff_depth": round(cuff_depth, 1),
        },
        "solved": {
            "cuff_open_requested_mm": round(_CUFF_OPEN_RAW * 2.0, 2),
            "cuff_open_final_mm": round(CUFF_OPEN_HALF * 2.0, 2),
            "cuff_passes_hand": bool(CUFF_OPEN_HALF * 2.0 >= palm_width),
            "tip_radius_requested_mm": round(_TIP_RAW, 2),
            "tip_radius_floored_mm": round(TIP_R, 2),
            "tip_radius_was_clamped": bool(abs(TIP_R - _TIP_RAW) > 0.01),
            "note": "the cuff opening is drafted to pass the HAND (palm width plus "
                    "ease), not just the wrist — a cuff to the wrist alone cannot be "
                    "put on over the hand. The mitten tip radius is floored against "
                    "the mitten width so it cannot invert the curve at the smallest "
                    "sizes (an inverted tip the kernel CCW-normalizes into a "
                    "valid-looking piece).",
        },
        "safety": "turn every seam inward, no seam allowance against the skin; "
                  "interlock is chosen because it sheds no loose fibre a baby could "
                  "pull into its mouth; the cuff elastic is soft so it does not mark.",
        "hardware": "none — pattern-only garment; the only closure is a soft "
                    "elastic in a turned cuff (a technique, not a hard good).",
    }
    return pattern


result = build()
