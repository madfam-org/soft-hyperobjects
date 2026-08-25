"""
Baby Kimono Wrap — Fashion Cabinet Garment Cartridge (FC-300 #289, kids_baby, T1).

A newborn's first shirt: it does not go over the head at all. The back is cut in
one piece on the fold, the two fronts cross over it, and side ties hold the
crossing shut. A parent lays the baby down on the open garment and folds it
closed — no neck opening is ever pulled past the skull, no arm is ever pushed
through a tube.

This is a genuine T1 garment and is drafted as one: four straight-forward pieces,
no closures, no hardware, no shaping the maker has to trust. What it does NOT do
is guess. Two numbers are solved rather than assumed:

  1. THE WRAP OVERLAP IS SOLVED FROM THE CHEST, NOT PICKED. A wrap that gapes is
     a wrap that fails; a wrap that is too deep binds a newborn's ribs. Each
     front is drafted with a crossover extension past the centre line, and that
     extension is derived from the quarter chest and then CLAMPED so it can never
     exceed what the panel can physically carry — a percentage applied blind to a
     small size produces a front narrower than its own overlap, which is a piece
     that folds inside out.

  2. THE ARMHOLE DEPTH IS SOLVED AGAINST THE BODY LENGTH. An infant torso is
     short. An armhole scaled off the chest alone will, at the small end of the
     range, reach below the hem — so it is clamped against the measured body
     length, not just against the chest.

The neckline is a self-bound edge, not a band: on a seamless-shoulder kimono the
front edge and the back neck are ONE continuous run, so the binding is cut to
that MEASURED run rather than to a formula.

No hardware. A newborn wrap with a snap, a button or a buckle at the front is a
hard object pressed between an infant's chest and an adult's forearm for hours;
the ties sit at the side seam where nothing lies on them.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body infant measurements) ───────
target_piece = str(PARAM(lambda: target_piece, "set"))
# back|front|sleeve|tie|binding|set

chest_girth = float(PARAM(lambda: chest_girth, 480.0))    # infant chest, full body
body_length = float(PARAM(lambda: body_length, 260.0))    # nape to hem
neck_girth = float(PARAM(lambda: neck_girth, 240.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 130.0))  # shoulder line to cuff
knit_ease = float(PARAM(lambda: knit_ease, 70.0))         # total positive ease
wrap_depth = float(PARAM(lambda: wrap_depth, 0.42))       # crossover, fraction of ¼ chest
tie_length = float(PARAM(lambda: tie_length, 260.0))
binding_width = float(PARAM(lambda: binding_width, 14.0))  # finished bound edge
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
chest_girth = max(380.0, min(chest_girth, 640.0))
body_length = max(180.0, min(body_length, 380.0))
neck_girth = max(190.0, min(neck_girth, 320.0))
sleeve_length = max(60.0, min(sleeve_length, 240.0))
knit_ease = max(30.0, min(knit_ease, 150.0))
wrap_depth = max(0.20, min(wrap_depth, 0.70))
tie_length = max(150.0, min(tie_length, 420.0))
binding_width = max(8.0, min(binding_width, 24.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))
hem_allowance = max(0.0, min(hem_allowance, 30.0))

# ── Derived block dimensions ─────────────────────────────────────────────────
W = (chest_girth + knit_ease) / 4.0          # quarter body width (back is on fold)
L = body_length                              # hem at y=0, nape line at y=L

# Armhole depth: scaled off the chest, then CLAMPED against the MEASURED body
# length. An infant torso is short — at the small end of the chest range an
# unclamped armhole reaches past the hem and the side seam vanishes.
AH = (chest_girth + knit_ease) / 8.0 + 30.0
AH = max(60.0, min(AH, L - 70.0))

NW = max(38.0, neck_girth / 6.0 + 6.0)       # half back-neck width
BACK_NECK_DROP = 12.0                        # a shallow back scoop
SHOULDER_DROP = 12.0                         # infant shoulder slope (near-flat)
HPS_Y = L                                    # high-point-shoulder line

SH_END = fc.P(W - 3.0, HPS_Y - SHOULDER_DROP)      # shoulder tip, shared F/B
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)     # armhole bottom, shared F/B

# The crossover: how far each front reaches PAST the centre line. Solved from the
# quarter chest, then clamped so the extension can never approach the panel's own
# width — a front narrower than its overlap is a piece that folds inside out, and
# it passes verify() perfectly happily because area() takes an absolute value.
_WRAP_RAW = W * wrap_depth
WRAP = max(12.0, min(_WRAP_RAW, W - 45.0))   # never wider than panel minus a stand
FRONT_W = W + WRAP                           # full width of one front panel
FRONT_NECK_DROP = min(L * 0.42, AH + 34.0)   # where the front edge meets the hem run


def _armhole_edge(x_off):
    """The armhole scoop, drafted identically on back and front (x_off shifts it
    onto the front's own coordinate frame, which is offset by the wrap).

    Walked UNDERARM → shoulder tip, which is the direction the outline chain
    needs (…side seam up to the underarm, then this, then the shoulder inwards).
    """
    return fc.Edge(
        "armhole",
        [fc.Bezier(fc.P(UNDERARM.x + x_off, UNDERARM.y),
                   fc.P(W - 4.0 + x_off, UNDERARM.y + AH * 0.30),
                   fc.P(W - 9.0 + x_off, SH_END.y - AH * 0.36),
                   fc.P(SH_END.x + x_off, SH_END.y))],
    )


def build_back():
    """Kimono back, cut 1 on the fold at centre back.

    The shoulder is NOT a seam here: it is the top edge of this piece, which is
    why the sleeve is set into a straight armhole and the neck run is continuous.
    """
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(W, 0.0)
    p_neck_cb = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    p_neck_sh = fc.P(NW, HPS_Y)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, fc.P(UNDERARM.x, UNDERARM.y))]),
        _armhole_edge(0.0),
        fc.Edge("shoulder", [fc.Line(SH_END, p_neck_sh)]),
        fc.Edge("neck", [fc.Bezier(p_neck_sh,
                                   fc.P(NW * 0.55, HPS_Y - 2.0),
                                   fc.P(NW * 0.20, p_neck_cb.y),
                                   p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0, "neck": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve cap back match"),
                 fc.Notch("side", 0.5, "tie level")],
        grainline=fc.Grainline(fc.P(W * 0.55, 25.0), fc.P(W * 0.55, L - 30.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Kimono back (cut on fold)",
    )


def build_front():
    """One kimono front, cut 2 MIRRORED — left over right, or right over left.

    Drafted in its own frame: x=0 is the side seam edge's inner limit and the
    panel runs out to FRONT_W, so the crossover extension past the body's centre
    is carried in the piece itself rather than added at construction.
    """
    p_hem_in = fc.P(0.0, 0.0)                     # the wrap edge at the hem
    p_hem_side = fc.P(FRONT_W, 0.0)
    p_under = fc.P(UNDERARM.x + WRAP, UNDERARM.y)
    p_sh_end = fc.P(SH_END.x + WRAP, SH_END.y)
    p_neck_sh = fc.P(NW + WRAP, HPS_Y)
    # Where the diagonal wrap edge lands at the inner hem. Held clear of the hem
    # by a fixed run so the point never degenerates into a spike.
    p_wrap_low = fc.P(0.0, max(18.0, L - FRONT_NECK_DROP - 26.0))

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_in, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_under)]),
        _armhole_edge(WRAP),
        fc.Edge("shoulder", [fc.Line(p_sh_end, p_neck_sh)]),
        # The wrap edge: neck point → down across the chest → inner hem. This is
        # ONE edge because it is bound in one pass, and its measured length is
        # what the binding strip is cut to.
        fc.Edge("wrap_edge", [fc.Bezier(p_neck_sh,
                                        fc.P(NW + WRAP * 0.55, HPS_Y - 16.0),
                                        fc.P(WRAP * 0.35, p_wrap_low.y + 40.0),
                                        p_wrap_low)]),
        fc.Edge("front_edge", [fc.Line(p_wrap_low, p_hem_in)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "wrap_edge": 0.0},  # wrap edge is bound
        notches=[fc.Notch("armhole", 0.5, "sleeve cap front match"),
                 fc.Notch("side", 0.5, "tie level")],
        grainline=fc.Grainline(fc.P(FRONT_W * 0.62, 25.0),
                               fc.P(FRONT_W * 0.62, L - 30.0)),
        internals=[
            # The centre line of the BODY inside this panel: everything to its
            # left is crossover. Marked so the maker can see the lap without
            # measuring, and can check the two fronts lap by the same amount.
            fc.Internal("body-centre-line",
                        [fc.P(WRAP, 0.0), fc.P(WRAP, HPS_Y - 20.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Kimono front (cut 2, mirrored)",
    )


# ── Solve the sleeve cap against the MEASURED armholes ───────────────────────
_BACK = build_back()
_FRONT = build_front()
ARMHOLE_B = _BACK.edge("armhole").length(0.05)
ARMHOLE_F = _FRONT.edge("armhole").length(0.05)
CAP_TARGET = ARMHOLE_F + ARMHOLE_B          # jersey, set flat: no cap ease
BICEPS = max(120.0, CAP_TARGET * 0.72)


def _cap_curve(half_b, under_y, cap_h):
    """A symmetric two-Bézier sleeve cap of height cap_h over width 2·half_b."""
    apex = fc.P(0.0, under_y + cap_h)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(half_b, under_y),
                  fc.P(half_b * 0.66, under_y + cap_h * 0.14),
                  fc.P(half_b * 0.32, under_y + cap_h), apex),
        fc.Bezier(apex,
                  fc.P(-half_b * 0.32, under_y + cap_h),
                  fc.P(-half_b * 0.66, under_y + cap_h * 0.14),
                  fc.P(-half_b, under_y)),
    ])


def _solve_half_biceps(cap_h, under_y):
    """Bisect the half-biceps until the MEASURED cap equals CAP_TARGET.

    The cap length grows monotonically with the half-width, so a plain bisection
    converges. Solving the WIDTH (rather than the height) keeps the shallow,
    flat kimono cap a kimono cap — a deep cap on an infant sleeve binds the arm.
    """
    lo, hi = 30.0, CAP_TARGET
    half = hi
    for _ in range(60):
        half = (lo + hi) / 2.0
        if _cap_curve(half, under_y, cap_h).length(0.05) < CAP_TARGET:
            lo = half
        else:
            hi = half
    return half


CAP_H = max(20.0, AH * 0.30)                 # deliberately shallow (kimono)
HALF_BICEPS = _solve_half_biceps(CAP_H, 0.0)


def build_sleeve():
    """Sleeve, cut 2 mirrored; a shallow set-in cap and a straight taper."""
    under_y = max(45.0, sleeve_length - CAP_H)
    cuff_half = max(38.0, HALF_BICEPS * 0.78)
    edges = [
        fc.Edge("sleeve_hem", [fc.Line(fc.P(-cuff_half, 0.0), fc.P(cuff_half, 0.0))]),
        fc.Edge("under_back", [fc.Line(fc.P(cuff_half, 0.0), fc.P(HALF_BICEPS, under_y))]),
        _cap_curve(HALF_BICEPS, under_y, CAP_H),
        fc.Edge("under_front", [fc.Line(fc.P(-HALF_BICEPS, under_y),
                                        fc.P(-cuff_half, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"sleeve_hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder point match")],
        grainline=fc.Grainline(fc.P(0.0, 18.0), fc.P(0.0, under_y + CAP_H * 0.5)),
        internals=[
            # A fold-back cuff line: on a newborn sleeve the cuff is turned up
            # over the hand for the first weeks, then turned down.
            fc.Internal("mitten-cuff fold",
                        [fc.P(-cuff_half, 26.0), fc.P(cuff_half, 26.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


# ── The bound edge run, MEASURED not assumed ─────────────────────────────────
# On a seamless-shoulder kimono the front wrap edge and the back neck are one
# continuous run: binding goes on in a single pass from one hem, up the wrap
# edge, around the back neck, down the other wrap edge, to the other hem. So the
# strip is cut to that MEASURED total, not to a neck formula.
WRAP_RUN = _FRONT.edge("wrap_edge").length(0.05)
BACK_NECK_RUN = 2.0 * _BACK.edge("neck").length(0.05)   # both halves of the fold
BINDING_RUN = 2.0 * WRAP_RUN + BACK_NECK_RUN


def build_binding():
    """The self-fabric binding strip for the whole continuous bound run (cut 1)."""
    ln = BINDING_RUN + 2.0 * seam_allowance
    h = 2.0 * binding_width                    # folded lengthwise when applied
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "binding", edges,
        seam_allowance=0.0,                    # the joins are already in `ln`
        grainline=fc.Grainline(fc.P(ln * 0.15, h / 2.0), fc.P(ln * 0.85, h / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, h / 2.0), fc.P(ln, h / 2.0)],
                        kind="marking"),
            # Where the binding turns the back neck — marked so the strip is
            # positioned by its own mark rather than eased in by guesswork.
            fc.Internal("back-neck start",
                        [fc.P(seam_allowance + WRAP_RUN, 0.0),
                         fc.P(seam_allowance + WRAP_RUN, h)],
                        kind="marking"),
            fc.Internal("back-neck end",
                        [fc.P(seam_allowance + WRAP_RUN + BACK_NECK_RUN, 0.0),
                         fc.P(seam_allowance + WRAP_RUN + BACK_NECK_RUN, h)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Edge binding strip",
    )


def build_tie():
    """A side tie, cut 4: two on the inside (holding the under-front), two out."""
    w = 22.0
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(tie_length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(tie_length, 0.0), fc.P(tie_length, w))]),
        fc.Edge("upper", [fc.Line(fc.P(tie_length, w), fc.P(0.0, w))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "tie", edges,
        seam_allowance=seam_allowance,
        allowances={"end_a": 0.0},              # this end is caught in the side seam
        grainline=fc.Grainline(fc.P(tie_length * 0.15, w / 2.0),
                               fc.P(tie_length * 0.85, w / 2.0)),
        cut=fc.CutSpec(quantity=4),
        label="Side tie (cut 4)",
    )


def build():
    pattern = fc.PatternSet("baby-kimono-wrap")
    everything = target_piece == "set"
    want = {
        "back": everything or target_piece == "back",
        "front": everything or target_piece == "front",
        "sleeve": everything or target_piece == "sleeve",
        "binding": everything or target_piece == "binding",
        "tie": everything or target_piece == "tie",
    }
    if not any(want.values()):                  # an unknown target renders the set
        want = dict.fromkeys(want, True)
        everything = True
    if want["back"]:
        pattern.add(build_back())
    if want["front"]:
        pattern.add(build_front())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["binding"]:
        pattern.add(build_binding())
    if want["tie"]:
        pattern.add(build_tie())

    if want["back"] and want["front"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # The shoulder: on a kimono this is a short join outboard of the neck,
        # and both edges are drawn to the same run, so it balances exactly.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.8)
    if want["sleeve"] and want["back"] and want["front"]:
        # One sleeve cap takes one front armhole plus one back armhole. No ease:
        # a flat-set jersey kimono sleeve is sewn in flat before the side seam.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.2, ease=0.0)
        pattern.declare_seam(("sleeve", "under_front"), ("sleeve", "under_back"),
                             tol=0.8)
    if want["binding"] and want["front"] and want["back"]:
        # The binding is cut to the MEASURED continuous run (both wrap edges +
        # both halves of the back neck) plus its two joins; the joins are the
        # declared ease so the check lands at delta ≈ 0.
        pattern.declare_seam(
            ("binding", "lower"),
            [("front", "wrap_edge"), ("front", "wrap_edge"),
             ("back", "neck"), ("back", "neck")],
            tol=1.5, ease=2.0 * seam_allowance)

    fabric_width = 1600.0                       # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton jersey, 180 gsm (jersey-algodon)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a soft single "
                 f"jersey against newborn skin, washed before cutting — this "
                 f"garment is laundered daily."},
        {"item": "self-fabric binding strip",
         "qty": round(BINDING_RUN + 2.0 * seam_allowance), "unit": "mm_length",
         "note": f"cut to the MEASURED continuous bound run "
                 f"({BINDING_RUN:.0f} mm: two wrap edges + the whole back neck), "
                 f"applied in a single pass."},
        {"item": "thread (cotton or poly, fine)", "qty": 1, "unit": "spool",
         "note": "bar-tack each tie where it is caught in the side seam — that "
                 "join takes every pull the garment ever gets."},
    ]
    pattern.metadata = {
        "fc300_rank": 289,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "jersey-algodon",
        "finished_mm": {
            "body_length": round(L, 1),
            "quarter_chest": round(W, 1),
            "front_panel_width": round(FRONT_W, 1),
            "armhole_depth": round(AH, 1),
            "sleeve_length": round(sleeve_length, 1),
        },
        "solved": {
            "wrap_overlap_requested_mm": round(_WRAP_RAW, 2),
            "wrap_overlap_clamped_mm": round(WRAP, 2),
            "wrap_overlap_was_clamped": bool(abs(WRAP - _WRAP_RAW) > 0.01),
            "armhole_front_mm": round(ARMHOLE_F, 2),
            "armhole_back_mm": round(ARMHOLE_B, 2),
            "cap_target_mm": round(CAP_TARGET, 2),
            "half_biceps_solved_mm": round(HALF_BICEPS, 2),
            "wrap_edge_run_mm": round(WRAP_RUN, 2),
            "back_neck_run_mm": round(BACK_NECK_RUN, 2),
            "binding_run_total_mm": round(BINDING_RUN, 2),
            "note": "the crossover is derived from the quarter chest and then "
                    "CLAMPED to W-45 mm — a front narrower than its own overlap "
                    "folds inside out and still passes an area check, because "
                    "area() takes an absolute value. The armhole depth is likewise "
                    "clamped against the measured body length, because an infant "
                    "torso is short enough for a chest-scaled armhole to reach "
                    "past the hem. The binding is cut to the MEASURED continuous "
                    "run, not to a neck formula — on a seamless-shoulder kimono "
                    "the wrap edges and the back neck are one bound pass.",
        },
        "infant_safety": {
            "no_overhead": "nothing passes over the head; the baby is laid on the "
                           "open garment and it is folded closed",
            "no_hardware": "no snap, button or buckle anywhere — nothing hard sits "
                           "between an infant's chest and an adult's forearm",
            "ties_at_the_side": "the ties are at the side seam, off the spine and "
                                "off the front, so nothing is lain on",
            "mitten_cuff": "the cuff is marked to turn back over the hand for the "
                           "first weeks",
        },
        "drafting": "seamless-shoulder kimono: back cut 1 on fold, two mirrored "
                    "crossing fronts, shallow flat-set sleeve, one continuous "
                    "bound edge run, four side ties. No closures.",
    }
    return pattern


result = build()
