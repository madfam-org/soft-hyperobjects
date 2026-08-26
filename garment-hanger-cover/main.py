"""
Padded garment-hanger cover — Fashion Cabinet Cartridge (FC-500 #419, care_keeping, T1).

A quilted slip-on cover that pads a bare hanger so a knit or a silk blouse hangs without
shoulder dents. Two mirrored SHELL halves close around the shoulder and a gathered CUFF grips
the hook shaft. Drafted to a KNOWN hanger — the Yantra4D `garment-hanger` solid — so the
shell's inner arc is sized to that hanger's printed shoulder rather than to a guess.

THE SEAM THAT MUST SOLVE (the FC-400 hanger-cover scar, carried here): a hanger shoulder is
an ARC. The shell's inner edge (against the bar) and outer edge (the padded face) are two
CONCENTRIC arcs SHARING ONE CENTRE — not per-radius centres, which collapse to a zero-area
lens on a shallow drop. The outer arc is genuinely longer than the inner by an amount set by
the sweep and the pad girth; both are POLYGONISED and MEASURED and the excess is declared as
the seam ease. The sagitta relation R=(c²+s²)/2s solves the shoulder radius from span and
drop; the drop is clamped so a deep drop never folds the concentric arcs through one another.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|cuff|set

hanger_span = float(PARAM(lambda: hanger_span, 430.0))    # tip to tip
shoulder_drop = float(PARAM(lambda: shoulder_drop, 60.0))
pad_girth = float(PARAM(lambda: pad_girth, 24.0))
cuff_rise = float(PARAM(lambda: cuff_rise, 75.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

hanger_span = max(280.0, min(hanger_span, 540.0))
shoulder_drop = max(15.0, min(shoulder_drop, 120.0))
pad_girth = max(8.0, min(pad_girth, 48.0))
cuff_rise = max(30.0, min(cuff_rise, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HALF_SPAN = hanger_span / 2.0
shoulder_drop = min(shoulder_drop, HALF_SPAN * 0.85)

ARC_SEGS = 28
_C, _S = HALF_SPAN, shoulder_drop
ARC_R = (_C * _C + _S * _S) / (2.0 * _S)
ARC_HALF_ANGLE = math.asin(min(1.0, _C / ARC_R))


def _arc_pts(r, a_from, a_to, n=ARC_SEGS):
    # BOTH arcs share ONE centre at (0, -ARC_R).
    cy = -ARC_R
    return [fc.P(r * math.sin(a_from + (a_to - a_from) * i / n),
                 cy + r * math.cos(a_from + (a_to - a_from) * i / n))
            for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


_INNER = _arc_pts(ARC_R, -ARC_HALF_ANGLE, ARC_HALF_ANGLE)
_OUTER = _arc_pts(ARC_R + pad_girth, -ARC_HALF_ANGLE, ARC_HALF_ANGLE)
INNER_LEN = _poly_len(_INNER)
OUTER_LEN = _poly_len(_OUTER)
ARC_EXCESS = OUTER_LEN - INNER_LEN
DART_TAKE = min(ARC_EXCESS * 0.5, pad_girth * 0.9)


def build_shell():
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
                     fc.P(0.0, _INNER[ARC_SEGS // 2].y + pad_girth * 0.25),
                     fc.P(DART_TAKE / 2.0, _OUTER[ARC_SEGS // 2].y)],
                    kind="dart"),
        fc.Internal("hook-slot", [fc.P(-cuff_rise * 0.16, 0.0),
                                  fc.P(cuff_rise * 0.16, 0.0)], kind="marking"),
    ]
    return fc.Piece(
        "shell", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer_arc", 0.5, "crown — hook centre"),
                 fc.Notch("inner_arc", 0.5, "crown — hook centre"),
                 fc.Notch("outer_arc", 0.25, "quarter ease mark"),
                 fc.Notch("outer_arc", 0.75, "quarter ease mark")],
        grainline=fc.Grainline(fc.P(-HALF_SPAN * 0.55, -shoulder_drop * 0.4),
                               fc.P(HALF_SPAN * 0.55, -shoulder_drop * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Padded shell half (cut 2, mirrored)",
    )


CUFF_CIRC = max(40.0, pad_girth * 2.4 + 18.0)


def build_cuff():
    w, h = CUFF_CIRC, cuff_rise
    return fc.Piece(
        "cuff", [
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
        label="Hook cuff (cut 1)",
    )


def build():
    pattern = fc.PatternSet("garment-hanger-cover")
    everything = target_piece == "set"
    if everything or target_piece == "shell":
        pattern.add(build_shell())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())

    if everything or target_piece == "shell":
        pattern.declare_seam(("shell", "outer_arc"), ("shell", "outer_arc"), tol=0.5)
        pattern.declare_seam(("shell", "outer_arc"), ("shell", "inner_arc"),
                             tol=0.8, ease=ARC_EXCESS)
        pattern.declare_seam(("shell", "tip_r"), ("shell", "tip_l"), tol=0.5)
    if everything:
        pattern.declare_seam(("cuff", "seam_a"), ("cuff", "seam_b"), tol=0.5)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "quilted cotton (pre-wadded)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 66% marker; a pre-quilted face grips the "
                 f"hanger and pads the shoulder."},
        {"item": "printed hanger body", "qty": 1, "unit": "count",
         "note": f"Yantra4D garment-hanger (notion.hardware_ref): its {hanger_span:.0f} mm "
                 f"shoulder is what the shell inner arc is drafted against."},
        {"item": "narrow ribbon (gather tie)", "qty": round(CUFF_CIRC * 3.0),
         "unit": "mm_length", "note": "threads the cuff gather channel."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "hand-slip the inner arc closed after the hanger is inside."},
    ]
    pattern.metadata = {
        "fc500_rank": 419, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A quilted slip-on hanger cover: two shell halves + a gathered "
            "hook cuff, drafted to the printed hanger shoulder.",
        "solved": {
            "arc_radius_mm": round(ARC_R, 2),
            "arc_half_angle_deg": round(math.degrees(ARC_HALF_ANGLE), 2),
            "inner_arc_mm": round(INNER_LEN, 2),
            "outer_arc_mm": round(OUTER_LEN, 2),
            "concentric_excess_mm": round(ARC_EXCESS, 2),
            "crown_dart_take_mm": round(DART_TAKE, 2),
            "note": "shoulder radius solved from span and drop by R=(c²+s²)/2s; the inner "
                    "and outer arcs share ONE centre and are polygonised and measured; the "
                    "excess of outer over inner cups the cover, half taken by a crown dart; "
                    "the drop is clamped under 0.85·half-span so the arcs never invert.",
        },
        "hardware": "printed hanger body via Yantra4D (notion.hardware_ref -> "
                    "garment-hanger); shoulder_w is fed from hanger_span. No flange "
                    "interface — the cover slips over the hanger, no seam handshake owed.",
    }
    return pattern


result = build()
