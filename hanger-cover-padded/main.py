"""
Padded Hanger Cover — Fashion Cabinet Care & Keeping Cartridge (FC-400 rank #364,
Yantra4D-bridged garment-hanger).

A quilted slip-on cover that pads a bare hanger so a knit or a silk blouse hangs without
shoulder dents. Two mirrored SHELL halves close around the shoulder, and a gathered CUFF
tube grips the hook shaft. Unlike the pattern-only FC-300 cover, this one is drafted to a
KNOWN hanger body — the Yantra4D `garment-hanger` solid (notion.hardware_ref) — so the
shell's inner arc is sized to that hanger's printed shoulder rather than to a guess.

Drafting note — the seam that must SOLVE: a hanger shoulder is an ARC. The shell's inner
edge (against the hanger bar) and outer edge (the padded face) are two CONCENTRIC arcs, so
the outer is genuinely longer than the inner by an amount set by the sweep and the pad
girth. Both arcs are POLYGONISED and MEASURED, and the excess is declared as the seam's
ease — half taken by a crown dart, half eased as the cover is stuffed. The sagitta relation
R = (c²+s²)/2s solves the shoulder radius from the span and drop; the drop is clamped so a
deep drop can never fold the concentric arcs through one another.

Pieces:
  - shell : one padded half (cut 2, mirrored).
  - cuff  : the gathered hook-shaft tube (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|cuff|set

hanger_span = float(PARAM(lambda: hanger_span, 430.0))    # tip to tip, straight across
shoulder_drop = float(PARAM(lambda: shoulder_drop, 60.0))  # arms' fall from the crown
pad_girth = float(PARAM(lambda: pad_girth, 24.0))         # finished padded radius
cuff_rise = float(PARAM(lambda: cuff_rise, 75.0))         # how far the cuff climbs the hook
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hanger_span = max(280.0, min(hanger_span, 540.0))
shoulder_drop = max(15.0, min(shoulder_drop, 120.0))
pad_girth = max(8.0, min(pad_girth, 48.0))
cuff_rise = max(30.0, min(cuff_rise, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HALF_SPAN = hanger_span / 2.0
# The drop cannot exceed the half-span or the sagitta arc inverts; hold it under so
# a real hanger arc always remains (a chord's sagitta must be < the chord half-width
# for a shallow shoulder arc).
shoulder_drop = min(shoulder_drop, HALF_SPAN * 0.85)

ARC_SEGS = 28

# ── Solve the shoulder arc from span and drop (sagitta relation) ─────────────
_C, _S = HALF_SPAN, shoulder_drop
ARC_R = (_C * _C + _S * _S) / (2.0 * _S)
ARC_HALF_ANGLE = math.asin(min(1.0, _C / ARC_R))


def _arc_pts(r, a_from, a_to, n=ARC_SEGS):
    # BOTH arcs share ONE centre at (0, -ARC_R): the inner arc rides radius ARC_R
    # and the outer rides ARC_R + pad_girth, so the two are a TRUE concentric offset
    # (a uniform pad_girth apart everywhere) rather than two arcs pinched together
    # at a shared crown — the latter collapses to a zero-area lens on a shallow drop.
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
    """One padded half (cut 2, mirrored): outer arc on top, inner arc below, a short
    tip edge at each end."""
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
        label="Padded shell half",
    )


# The cuff tube's circumference clears the hook shaft plus the pad turn-of-cloth.
CUFF_CIRC = max(40.0, pad_girth * 2.4 + 18.0)


def build_cuff():
    """The gathered hook-shaft tube: a rectangle rolled into a tube, its side seams
    closing on each other."""
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
        label="Hook cuff",
    )


def build():
    pattern = fc.PatternSet("hanger-cover-padded")
    everything = target_piece == "set"
    if everything or target_piece == "shell":
        pattern.add(build_shell())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())

    if everything or target_piece == "shell":
        # THE solving seam: the two mirrored shells meet along both arcs; the outer
        # arc is longer than the inner by the MEASURED concentric excess, declared
        # as ease so the sleeve cups the hanger instead of hanging slack.
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
         "note": "≈ at 1150 mm width, 66% marker; a pre-quilted face saves the "
                 "separate wadding step and grips better than a slick lining."},
        {"item": "printed hanger body", "qty": 1, "unit": "count",
         "note": f"Yantra4D garment-hanger (notion.hardware_ref): its {hanger_span:.0f} mm "
                 f"shoulder is what the shell's inner arc is drafted against."},
        {"item": "narrow ribbon (gather tie)", "qty": round(CUFF_CIRC * 3.0),
         "unit": "mm_length", "note": "threads the cuff's gather channel."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "hand-slip the inner arc closed after the hanger is inside."},
    ]
    pattern.metadata = {
        "fc400_rank": 364,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"span": round(hanger_span, 1),
                        "drop": round(shoulder_drop, 1),
                        "pad_girth": round(pad_girth, 1)},
        "solved": {
            "arc_radius_mm": round(ARC_R, 2),
            "arc_half_angle_deg": round(math.degrees(ARC_HALF_ANGLE), 2),
            "inner_arc_mm": round(INNER_LEN, 2),
            "outer_arc_mm": round(OUTER_LEN, 2),
            "concentric_excess_mm": round(ARC_EXCESS, 2),
            "crown_dart_take_mm": round(DART_TAKE, 2),
            "note": "shoulder radius solved from span and drop by R=(c²+s²)/2s, then "
                    "the inner and outer arcs POLYGONISED AND MEASURED; the excess of "
                    "outer over inner cups the cover, half taken by a crown dart. The "
                    "drop is clamped under 0.85·half-span so the arcs never invert.",
        },
        "hardware": "printed hanger body via Yantra4D (notion.hardware_ref -> "
                    "garment-hanger); shoulder_w = hanger_span. Logged co-create in the "
                    "FC-400 index; linked live here.",
    }
    return pattern


result = build()
