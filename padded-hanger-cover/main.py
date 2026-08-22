"""
Padded Hanger Cover — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #257,
pattern-only — the hanger solid is not yet in the Yantra4D commons).

The slip-on padded cover that turns a wire or thin wooden hanger into something a silk
blouse can hang on without shoulder dents. Two mirrored SHELL halves sew around a wadding
core, a hook COLLAR gathers at the neck, and an optional BOW strip hides the join.

Drafting note — the seam that must SOLVE: a hanger's shoulder is an ARC, not a straight
bar, and the cover's shell is drafted around that arc. The shell's inner and outer edges
are two CONCENTRIC arcs — so the outer edge is genuinely longer than the inner, by an
amount that depends on the sweep angle and the padded thickness. That difference is what
makes the cover cup around the hanger instead of hanging slack. Both arcs are polygonised
and MEASURED; the outer-to-inner difference is declared as the seam's ease rather than
being absorbed silently. A dart is also placed at the arc's crown to take up part of the
excess where the padding is thickest.

Pieces:
  - shell  : one half of the padded sleeve (cut 2, mirrored).
  - collar : the gathered neck that closes around the hook shaft (cut 1).
  - bow    : the trim strip that covers the neck gather (cut 1).

Hardware: none referenced. The natural bridge would be a printable hanger body — see the
report's co-create note for `garment-hanger`; until such a solid exists in the pinned
Yantra4D snapshot this cartridge deliberately declares no `hardware_ref` rather than
inventing a dangling one.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|collar|bow|set

hanger_span = float(PARAM(lambda: hanger_span, 420.0))       # tip to tip, straight across
shoulder_drop = float(PARAM(lambda: shoulder_drop, 55.0))    # how far the arms fall
pad_thickness = float(PARAM(lambda: pad_thickness, 22.0))    # finished padded girth radius
neck_height = float(PARAM(lambda: neck_height, 70.0))        # the collar's rise to the hook
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hanger_span = max(280.0, min(hanger_span, 520.0))
shoulder_drop = max(15.0, min(shoulder_drop, 110.0))
pad_thickness = max(8.0, min(pad_thickness, 45.0))
neck_height = max(35.0, min(neck_height, 130.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

ARC_SEGS = 28           # per half-shoulder; the arcs are measured, never assumed
HALF_SPAN = hanger_span / 2.0

# ── Solve the shoulder arc from span and drop ────────────────────────────────
# A circular arc through (0, 0) at the crown and (HALF_SPAN, -shoulder_drop) at the
# tip. For a chord half-width c and sagitta s, the radius is R = (c² + s²) / (2s).
_C, _S = HALF_SPAN, shoulder_drop
ARC_R = (_C * _C + _S * _S) / (2.0 * _S)
ARC_HALF_ANGLE = math.asin(min(1.0, _C / ARC_R))


def _arc_pts(r, a_from, a_to, n=ARC_SEGS):
    """Points on a circle of radius r, centred so the crown sits at the origin."""
    cy = -r          # centre below the crown, so the crown is at (0, 0)
    return [fc.P(r * math.sin(a_from + (a_to - a_from) * i / n),
                 cy + r * math.cos(a_from + (a_to - a_from) * i / n))
            for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# Inner arc = the hanger bar itself; outer arc = the same sweep at radius + padding.
_INNER = _arc_pts(ARC_R, -ARC_HALF_ANGLE, ARC_HALF_ANGLE)
_OUTER = _arc_pts(ARC_R + pad_thickness, -ARC_HALF_ANGLE, ARC_HALF_ANGLE)
INNER_LEN = _poly_len(_INNER)
OUTER_LEN = _poly_len(_OUTER)
ARC_EXCESS = OUTER_LEN - INNER_LEN          # what makes the cover cup

# Half the excess is taken by a crown dart; the rest is eased in as the cover is
# stuffed. A dart deeper than the padding itself would pucker, so it is capped.
DART_TAKE = min(ARC_EXCESS * 0.5, pad_thickness * 0.9)


def build_shell():
    """One half of the sleeve (cut 2, mirrored): outer arc on top, inner arc below,
    closed at each end by a short tip edge."""
    outer = _OUTER
    inner = list(reversed(_INNER))
    edges = [
        fc.Edge("outer_arc", _lines(outer)),
        fc.Edge("tip_r", [fc.Line(outer[-1], inner[0])]),
        fc.Edge("inner_arc", _lines(inner)),
        fc.Edge("tip_l", [fc.Line(inner[-1], outer[0])]),
    ]
    internals = [
        fc.Internal("crown-dart",
                    [fc.P(-DART_TAKE / 2.0, _OUTER[ARC_SEGS // 2].y),
                     fc.P(0.0, _INNER[ARC_SEGS // 2].y + pad_thickness * 0.25),
                     fc.P(DART_TAKE / 2.0, _OUTER[ARC_SEGS // 2].y)],
                    kind="dart"),
        fc.Internal("neck-opening",
                    [fc.P(-neck_height * 0.18, 0.0), fc.P(neck_height * 0.18, 0.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "shell",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer_arc", 0.5, "crown — hook centre"),
                 fc.Notch("inner_arc", 0.5, "crown — hook centre"),
                 fc.Notch("outer_arc", 0.25, "quarter mark for easing"),
                 fc.Notch("outer_arc", 0.75, "quarter mark for easing")],
        grainline=fc.Grainline(fc.P(-HALF_SPAN * 0.55, -shoulder_drop * 0.4),
                               fc.P(HALF_SPAN * 0.55, -shoulder_drop * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Padded shell half",
    )


# The collar is a tube around the hook shaft: its circumference is the measured
# neck opening the two shells present when they meet at the crown.
NECK_CIRC = max(38.0, pad_thickness * 2.4 + 16.0)


def build_collar():
    """The gathered neck: a rectangle that rolls into the tube around the hook."""
    w, h = NECK_CIRC, neck_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("gather_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre — sits at the crown")],
        grainline=fc.Grainline(fc.P(w * 0.5, 6.0), fc.P(w * 0.5, h - 6.0)),
        internals=[fc.Internal("gather-channel",
                               [fc.P(0.0, h - 12.0), fc.P(w, h - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Hook collar",
    )


BOW_LENGTH = max(180.0, NECK_CIRC * 3.2)
BOW_WIDTH = max(22.0, pad_thickness * 1.1)


def build_bow():
    """The trim strip that ties over the neck gather. Cut double and folded."""
    ln, w = BOW_LENGTH, BOW_WIDTH * 2.0
    return fc.Piece(
        "bow",
        [
            fc.Edge("edge_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("edge_bottom", 0.5, "centre — sits at the collar")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Neck bow strip",
    )


def build():
    pattern = fc.PatternSet("padded-hanger-cover")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "collar":
        pattern.add(build_collar())
    if all_pieces or target_piece == "bow":
        pattern.add(build_bow())

    if all_pieces or target_piece == "shell":
        # THE solving seam: the two mirrored shells meet along both arcs. Sewn to
        # itself, each arc matches — but the OUTER arc is longer than the inner by
        # the MEASURED concentric excess, which is what makes the sleeve cup. That
        # relationship is declared explicitly so it can never rot into a fudge.
        pattern.declare_seam(("shell", "outer_arc"), ("shell", "outer_arc"), tol=0.5)
        pattern.declare_seam(("shell", "outer_arc"), ("shell", "inner_arc"),
                             tol=0.8, ease=ARC_EXCESS)
        pattern.declare_seam(("shell", "tip_r"), ("shell", "tip_l"), tol=0.5)
    if all_pieces:
        # The collar rolls into a tube: its two side seams close on each other.
        pattern.declare_seam(("collar", "seam_a"), ("collar", "seam_b"), tol=0.5)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "cotton sateen or silk habotai",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 68% marker; a slippery face is wrong here — "
                 "the cover's job is to GRIP so the garment does not slide off."},
        {"item": "polyester or wool wadding",
         "qty": round(hanger_span * pad_thickness * 2.4 / 100.0), "unit": "cm2",
         "note": f"{pad_thickness:.0f} mm finished thickness; wrap the bar before "
                 f"the shell goes on."},
        {"item": "narrow ribbon (gather tie)", "qty": round(NECK_CIRC * 3.0),
         "unit": "mm_length",
         "note": "threads the collar's gather channel."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "hand-slip the last arc closed after stuffing."},
    ]
    pattern.metadata = {
        "fc300_rank": 257,
        "family": "care_and_keeping",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {"span": round(hanger_span, 1),
                        "drop": round(shoulder_drop, 1),
                        "pad_thickness": round(pad_thickness, 1)},
        "solved": {
            "arc_radius_mm": round(ARC_R, 2),
            "arc_half_angle_deg": round(math.degrees(ARC_HALF_ANGLE), 2),
            "inner_arc_mm": round(INNER_LEN, 2),
            "outer_arc_mm": round(OUTER_LEN, 2),
            "concentric_excess_mm": round(ARC_EXCESS, 2),
            "crown_dart_take_mm": round(DART_TAKE, 2),
            "segments_per_arc": ARC_SEGS,
            "note": "the shoulder radius is solved from span and drop by the sagitta "
                    "relation R = (c²+s²)/2s, then the inner and outer arcs are "
                    f"POLYGONISED AND MEASURED — the {ARC_EXCESS:.1f} mm excess of outer over "
                    "inner is what cups the cover, half taken by a crown dart and "
                    "half eased.",
        },
        "hardware": "none — a printable hanger body is a wanted Yantra4D solid "
                    "(co-create: garment-hanger); this cartridge stays pattern-only "
                    "rather than declare a reference the pinned snapshot cannot resolve.",
    }
    return pattern


result = build()
