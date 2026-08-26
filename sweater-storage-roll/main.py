"""
Roll-up Sweater Storage Sleeve — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #366, pattern-only).

A soft muslin sleeve a folded sweater rolls up inside: lay the sweater on the open MAT,
fold the two side FLAPS in, roll from the head end, and cinch the roll with a pair of TIE
straps. Breathable and unstructured, so a stored knit gets air and no crease line — the
opposite of a vacuum bag, which compresses a sweater into permanent folds.

Drafting note — the seam that must SOLVE: the flaps fold onto a plane thickened by the
rolled sweater, so a flap cut to the mat half-width would come up short. Each flap's width
is the mat half-width MINUS a centre gap (so the two flaps do not overlap and bulk up the
roll), and every flap is cut to the MEASURED mat edge it hinges on. The tie length is
derived from the finished roll circumference (mat width wrapped at the roll diameter), not
guessed.

Pieces:
  - mat  : the base the sweater lies on (cut 1).
  - flap : one side flap folded in before rolling (cut 2, mirrored).
  - tie  : one cinch strap (cut 2).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # mat|flap|tie|set

mat_width = float(PARAM(lambda: mat_width, 440.0))       # across the folded sweater
mat_length = float(PARAM(lambda: mat_length, 560.0))     # head-to-hem before rolling
roll_diameter = float(PARAM(lambda: roll_diameter, 130.0))  # finished roll thickness
tie_width = float(PARAM(lambda: tie_width, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
mat_width = max(300.0, min(mat_width, 620.0))
mat_length = max(360.0, min(mat_length, 760.0))
roll_diameter = max(70.0, min(roll_diameter, 240.0))
tie_width = max(16.0, min(tie_width, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HALF_W = mat_width / 2.0
# A centre gap keeps the two folded flaps from overlapping (which would double the
# fabric down the roll's spine). The flap reaches to just short of centre.
CENTRE_GAP = min(40.0, mat_width * 0.12)
FLAP_REACH = HALF_W - CENTRE_GAP / 2.0


def build_mat():
    """The base panel. Its two side edges hinge the flaps; the head edge takes the
    ties; the hem edge is where the roll starts."""
    w, h = mat_width, mat_length
    edges = [
        fc.Edge("hem_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("hinge_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("head_edge", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("hinge_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold-line-r", [fc.P(w - 3.0, 0.0), fc.P(w - 3.0, h)],
                    kind="marking"),
        fc.Internal("fold-line-l", [fc.P(3.0, 0.0), fc.P(3.0, h)], kind="marking"),
        fc.Internal("roll-start", [fc.P(0.0, roll_diameter * 0.5),
                                   fc.P(w, roll_diameter * 0.5)], kind="marking"),
    ]
    return fc.Piece(
        "mat", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hinge_r", 0.5, "flap centre"),
                 fc.Notch("hinge_l", 0.5, "flap centre"),
                 fc.Notch("head_edge", 0.33, "tie anchor"),
                 fc.Notch("head_edge", 0.67, "tie anchor")],
        grainline=fc.Grainline(fc.P(HALF_W, 30.0), fc.P(HALF_W, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Roll mat",
    )


def build_flap():
    """One side flap (cut 2 mirrored). Its `hinge` edge sews to a mat side (length =
    mat_length, MEASURED) and it reaches FLAP_REACH toward centre."""
    ln, reach = mat_length, FLAP_REACH
    edges = [
        fc.Edge("hinge", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ln))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, ln), fc.P(reach, ln))]),
        fc.Edge("free", [fc.Line(fc.P(reach, ln), fc.P(reach, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(reach, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "flap", edges,
        seam_allowance=seam_allowance,
        allowances={"free": 14.0},
        notches=[fc.Notch("hinge", 0.5, "match mat flap centre")],
        grainline=fc.Grainline(fc.P(reach * 0.5, 30.0), fc.P(reach * 0.5, ln - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side flap",
    )


# The tie wraps the finished roll once plus a bow: roll circumference + a fixed tail.
ROLL_CIRC = math.pi * roll_diameter
TIE_LENGTH = ROLL_CIRC + 300.0


def build_tie():
    """One cinch strap, cut double and folded lengthwise."""
    ln, w = TIE_LENGTH, tie_width * 2.0
    return fc.Piece(
        "tie", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.08, "anchor to head edge")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Cinch tie",
    )


def build():
    pattern = fc.PatternSet("sweater-storage-roll")
    everything = target_piece == "set"
    if everything or target_piece == "mat":
        pattern.add(build_mat())
    if everything or target_piece == "flap":
        pattern.add(build_flap())
    if everything or target_piece == "tie":
        pattern.add(build_tie())

    if everything:
        # THE solving seams: each flap hinges to a mat side, cut to the MEASURED
        # mat length so the fold seam matches by construction.
        pattern.declare_seam(("flap", "hinge"), ("mat", "hinge_r"), tol=1.0)
        pattern.declare_seam(("flap", "hinge"), ("mat", "hinge_l"), tol=1.0)
        # The ties are tacked to the head edge as short straps (not a full-width
        # seam), so they are attached in construction, not declared here.

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "cotton muslin", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 80% marker; unbleached muslin breathes, which is "
                 "the whole point over a vacuum bag."},
        {"item": "cedar sachet (optional)", "qty": 1, "unit": "count",
         "note": "tuck into the roll to deter moths without touching the knit."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "narrow-hem every free edge; the mat is unlined so it stays soft."},
    ]
    pattern.metadata = {
        "fc400_rank": 366,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"mat_width": round(mat_width, 1),
                        "mat_length": round(mat_length, 1),
                        "roll_diameter": round(roll_diameter, 1)},
        "solved": {
            "flap_reach_mm": round(FLAP_REACH, 2),
            "centre_gap_mm": round(CENTRE_GAP, 2),
            "roll_circumference_mm": round(ROLL_CIRC, 2),
            "tie_length_mm": round(TIE_LENGTH, 2),
            "note": "each flap reaches the mat half-width minus half a centre gap, so "
                    "the two folded flaps meet without overlapping down the roll's "
                    "spine; the tie length is the roll circumference plus a bow tail.",
        },
        "hardware": "none — a roll-up soft sleeve needs no hardware; pattern-only by "
                    "design, deepening the thin care_keeping family.",
    }
    return pattern


result = build()
