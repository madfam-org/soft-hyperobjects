"""
Changpao (長袍) — Fashion Cabinet Heritage Cartridge (FC-300 #299, long-tail band).

The Chinese men's long robe: a straight, ankle-length gown with a stand collar, closed
along a curved diagonal from the throat across the chest to the right underarm and then
down the right side, fastened with knotted cloth frogs (盤扣 pánkòu). Worn as ordinary
dress across late-Qing and Republican China, and still worn — with the 馬褂 (mǎguà)
riding jacket over it as the 長袍馬褂 formal pairing, and as the ancestor of the
Cantonese 長衫 (chèuhngsāam) and of the modern 唐裝.

The construction logic this cartridge exists to encode is NOT the Western one. Two
facts govern the whole draft:

  1. THE CLOTH IS NARROW AND THE PANEL IS WHOLE. Handloom silk and cotton ran roughly
     the width of a seated weaver's reach. The robe is therefore built from panels of
     that width used whole, with a centre-back seam, and the fit comes from where the
     straight seams fall — not from shaping cut into the panel. `panel_width` is a real
     parameter here, and the body circuit is COMPUTED from it. If the cloth cannot
     reach round the wearer, the draft says so rather than quietly inventing a wider
     bolt.

  2. THE SLEEVE IS CUT IN ONE WITH THE BODY (連袖). There is no armscye. The shoulder
     line runs straight out from the neck to the wrist, and the underarm is a corner,
     not a curve. Drafting a set-in sleeve here would be a different garment wearing
     this one's name.

Drafting note — the seam that must SOLVE, and the mistake it prevents:

  The 大襟 (dàjīn) — the curved overlap that carries the closure — is the garment. Its
  edge runs from the neck, out and down across the chest, to the right underarm. The
  body panel underneath must be cut with an edge of EXACTLY that length, or the overlap
  will not lie flat and the whole front twists on the body.

  So the dajin's curve is drafted first, its length is MEASURED from the drawn edge,
  and the body's matching edge is then solved to that measurement rather than
  recomputed from the same formula and hoped to agree. The seam check proves it.

  The frogs are then spaced along the MEASURED curve, not along a straight line. A
  pánkòu spaced by chord rather than by arc bunches at the shoulder and gaps at the
  underarm — the visible signature of a robe drafted flat.

Pieces:
  - body    : one body half (cut 2), panel width used whole, sleeve cut in one.
  - dajin   : the curved overlap panel (cut 2 — face and facing).
  - collar  : the stand collar (立領), cut to the MEASURED neckline.
  - underarm: the 插角 gusset that lets the arm come down in a one-piece sleeve.

Hardware: the closures are 盤扣 knotted cloth frogs. The Yantra4D solid for a frog
closure does not yet exist on the shelf, so this cartridge declares an UNLINKED
hardware_ref naming the slug to be co-created — the same honest form FC-200's
co-create garments use. The frogs remain hand-knotted cloth, which is what they are.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # body|dajin|collar|underarm|set

panel_width = float(PARAM(lambda: panel_width, 480.0))    # loom-width panel, used whole
chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
robe_length = float(PARAM(lambda: robe_length, 1320.0))   # nape to ankle
sleeve_length = float(PARAM(lambda: sleeve_length, 540.0))  # neck point to wrist
sleeve_opening = float(PARAM(lambda: sleeve_opening, 300.0))  # 袖口 cuff opening
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
collar_height = float(PARAM(lambda: collar_height, 42.0))   # 立領 stand height
dajin_drop = float(PARAM(lambda: dajin_drop, 300.0))      # neck to underarm, vertical
dajin_reach = float(PARAM(lambda: dajin_reach, 0.62))     # across the half-panel
side_slit = float(PARAM(lambda: side_slit, 380.0))        # 開衩 slit height from hem
frog_count = int(PARAM(lambda: frog_count, 5))            # 盤扣 along the dajin curve
frog_width = float(PARAM(lambda: frog_width, 56.0))       # knot-to-loop span
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
panel_width = max(320.0, min(panel_width, 760.0))
chest_girth = max(760.0, min(chest_girth, 1400.0))
robe_length = max(900.0, min(robe_length, 1600.0))
sleeve_length = max(300.0, min(sleeve_length, 760.0))
sleeve_opening = max(180.0, min(sleeve_opening, 460.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
collar_height = max(25.0, min(collar_height, 75.0))
dajin_drop = max(180.0, min(dajin_drop, 480.0))
dajin_reach = max(0.35, min(dajin_reach, 0.90))
side_slit = max(0.0, min(side_slit, 700.0))
frog_count = max(3, min(frog_count, 9))
frog_width = max(30.0, min(frog_width, 110.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

# ── The panel solve — the cloth is the unit, not the body ────────────────────
# The robe is two body panels (left and right, joined at centre back) plus the dajin
# overlap. The body circuit is what those panels give; the ease is what is left after
# the chest is wrapped, and it can be NEGATIVE, in which case the cloth is too narrow
# and the draft must say so instead of inventing a wider loom.
#
# The robe wraps as TWO panels plus the dajin's overlap: each panel is one loom width,
# folded at the shoulder so it covers a back quarter and a front quarter, and the dajin
# carries the right front PAST centre front to the wearer's right side. So the circuit
# is what the two panels give, and the dajin's reach is the wrap-past on top of it.
HALF_PANEL = panel_width / 2.0
# The neck opening. A 立領 stands ON the base of the neck, so the opening is the neck
# girth plus a modest wearing ease, and the drafted half-width follows from that rather
# than from a Western neckline formula (girth/6, which is drafted for a turndown collar
# sitting well below the neck base and would give a 307 mm opening for a 400 mm neck).
NECK_EASE = 26.0
NECK_HALF = (neck_girth + NECK_EASE) / 4.0

# The dajin's horizontal reach across the half panel. It must clear the neck opening on
# one side and stop short of the side seam on the other, or the overlap has no panel to
# lie on. Both bounds are real at the parameter extremes.
_REACH_MIN = NECK_HALF + 40.0
_REACH_MAX = HALF_PANEL - 25.0
_reach_raw = HALF_PANEL * dajin_reach
if _REACH_MAX <= _REACH_MIN:
    # A very narrow panel with a very wide neck: there is no legal band. Split the
    # difference rather than drawing an edge that crosses the neckline.
    DAJIN_X = (HALF_PANEL + NECK_HALF) / 2.0
    REACH_CLAMPED = True
else:
    DAJIN_X = min(max(_reach_raw, _REACH_MIN), _REACH_MAX)
    REACH_CLAMPED = abs(DAJIN_X - _reach_raw) > 1e-9

BODY_CIRCUIT = panel_width * 2.0 + DAJIN_X
CHEST_EASE = BODY_CIRCUIT - chest_girth
PANEL_SUFFICIENT = CHEST_EASE >= 60.0        # a robe wants real ease, not a skim

# The side slit cannot reach the underarm — it is a walking slit, not an open side.
SLIT_CEILING = (robe_length - dajin_drop) * 0.62
side_slit = min(side_slit, SLIT_CEILING)

# The vertical: the robe's shoulder line is at the top, the underarm dajin_drop below.
SHOULDER_Y = robe_length
UNDERARM_Y = robe_length - dajin_drop
# The neck drop at centre front — shallow, because a stand collar sits on the throat.
NECK_DROP_F = min(NECK_HALF * 0.55, dajin_drop * 0.35)
NECK_DROP_B = 18.0


def _dajin_curve(x_neck, y_neck, x_arm, y_arm):
    """The 大襟 curve: out from the neck, then down to the underarm.

    Drawn as a single Bezier whose control points bias the curve OUTWARD near the neck
    and DOWNWARD near the underarm — which is the shape of a real dajin, not a
    quarter-circle. Its length is measured, never assumed."""
    return fc.Bezier(
        fc.P(x_neck, y_neck),
        fc.P(x_neck + (x_arm - x_neck) * 0.62, y_neck - (y_neck - y_arm) * 0.10),
        fc.P(x_arm, y_arm + (y_neck - y_arm) * 0.42),
        fc.P(x_arm, y_arm))


def build_body():
    """One BACK half (cut 2, joined at centre back): the panel used whole, with the
    sleeve cut in one at the shoulder line.

    x = 0 is centre back; x = HALF_PANEL is the side. The sleeve runs out beyond the
    panel from the shoulder line. There is no armscye anywhere on this piece: the
    shoulder runs straight from the neck to the wrist and the underarm is a corner."""
    hp = HALF_PANEL
    sl_open_half = sleeve_opening / 2.0
    # The sleeve extends horizontally from the shoulder; its depth at the body is the
    # dajin drop (the underarm level), tapering to the cuff opening.
    sleeve_reach = sleeve_length
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hp, 0.0)
    p_underarm = fc.P(hp, UNDERARM_Y)
    p_sl_under = fc.P(hp + sleeve_reach, UNDERARM_Y + (dajin_drop - sl_open_half * 2.0)
                      * 0.55)
    p_sl_top = fc.P(hp + sleeve_reach, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - NECK_DROP_B)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        # The side seam: below the slit it is sewn, above it is open (the 開衩).
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        # The underarm corner and the sleeve's lower edge — no armscye anywhere.
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sl_under)]),
        fc.Edge("cuff", [fc.Line(p_sl_under, p_sl_top)]),
        # The shoulder line runs straight from the cuff to the neck: one continuous
        # fold in the woven robe, drafted here as an edge so it can be measured.
        fc.Edge("shoulder", [fc.Line(p_sl_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.62, SHOULDER_Y - 3.0),
                                   fc.P(NECK_HALF * 0.30, p_neck_cb.y + 2.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        # Where the dajin's edge falls on the panel beneath it — the line the overlap
        # is stitched to, and the reason the two lengths must agree.
        fc.Internal("dajin-seat",
                    [fc.P(NECK_HALF, SHOULDER_Y - NECK_DROP_F),
                     fc.P(DAJIN_X * 0.72, SHOULDER_Y - NECK_DROP_F - dajin_drop * 0.18),
                     fc.P(DAJIN_X, UNDERARM_Y + dajin_drop * 0.30),
                     fc.P(DAJIN_X, UNDERARM_Y)], kind="marking"),
        # The 開衩 side slit: open above this point.
        fc.Internal("slit-head", [fc.P(hp, side_slit), fc.P(hp - 30.0, side_slit)],
                    kind="marking"),
        # The underarm gusset's seat, at the corner where the one-piece sleeve turns.
        fc.Internal("gusset-seat",
                    [fc.P(hp, UNDERARM_Y),
                     fc.P(hp + dajin_drop * 0.22, UNDERARM_Y),
                     fc.P(hp, UNDERARM_Y - dajin_drop * 0.22)], kind="marking"),
    ]
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cuff": hem_allowance * 0.6},
        notches=[fc.Notch("side", side_slit / max(UNDERARM_Y, 1.0), "slit head"),
                 fc.Notch("shoulder", 0.5, "sleeve midpoint")],
        grainline=fc.Grainline(fc.P(hp * 0.25, hem_allowance + 40.0),
                               fc.P(hp * 0.25, UNDERARM_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Body half (panel used whole, sleeve cut in one)",
    )


def build_front():
    """The LEFT front panel (cut 1): the under-layer the dajin closes over.

    Its neck edge is the front quarter neckline, deeper than the back's — which is why
    the collar cannot be cut to a neck girth. It runs to centre front and stops; the
    dajin then crosses it right over left and is fastened down the wearer's right."""
    hp = HALF_PANEL
    sleeve_reach = sleeve_length
    sl_open_half = sleeve_opening / 2.0
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hp, 0.0)
    p_underarm = fc.P(hp, UNDERARM_Y)
    p_sl_under = fc.P(hp + sleeve_reach,
                      UNDERARM_Y + (dajin_drop - sl_open_half * 2.0) * 0.55)
    p_sl_top = fc.P(hp + sleeve_reach, SHOULDER_Y)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y)
    p_neck_cf = fc.P(0.0, SHOULDER_Y - NECK_DROP_F)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sl_under)]),
        fc.Edge("cuff", [fc.Line(p_sl_under, p_sl_top)]),
        fc.Edge("shoulder", [fc.Line(p_sl_top, p_neck_shoulder)]),
        # The FRONT quarter neckline — deeper than the back's by construction.
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.66, SHOULDER_Y - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 8.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("slit-head", [fc.P(hp, side_slit), fc.P(hp - 30.0, side_slit)],
                    kind="marking"),
        fc.Internal("gusset-seat",
                    [fc.P(hp, UNDERARM_Y),
                     fc.P(hp + dajin_drop * 0.22, UNDERARM_Y),
                     fc.P(hp, UNDERARM_Y - dajin_drop * 0.22)], kind="marking"),
        # Where the dajin's edge lands once the robe is crossed — the fastening line.
        fc.Internal("dajin-landing",
                    [fc.P(NECK_HALF, SHOULDER_Y - NECK_DROP_F),
                     fc.P(NECK_HALF * 0.5, UNDERARM_Y + dajin_drop * 0.4)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cuff": hem_allowance * 0.6},
        notches=[fc.Notch("side", side_slit / max(UNDERARM_Y, 1.0), "slit head"),
                 fc.Notch("shoulder", 0.5, "sleeve midpoint")],
        grainline=fc.Grainline(fc.P(hp * 0.25, hem_allowance + 40.0),
                               fc.P(hp * 0.25, UNDERARM_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Left front panel (under-layer)",
    )


# ── The dajin curve, MEASURED ────────────────────────────────────────────────
# Drafted once, measured once, and every dependent length reads the measurement.
_NECK_PT = (NECK_HALF, SHOULDER_Y - NECK_DROP_F)
_ARM_PT = (DAJIN_X, UNDERARM_Y)
_CURVE = _dajin_curve(_NECK_PT[0], _NECK_PT[1], _ARM_PT[0], _ARM_PT[1])
DAJIN_LEN = _CURVE.length(0.2)
# The straight-line chord the naive draft would have used, and how much it loses.
DAJIN_CHORD = math.hypot(_ARM_PT[0] - _NECK_PT[0], _NECK_PT[1] - _ARM_PT[1])
CHORD_SHORTFALL = DAJIN_LEN - DAJIN_CHORD


def build_dajin():
    """The 大襟 overlap panel (cut 2 — face and facing).

    Its curved edge IS the drafted curve; the body's `dajin-seat` marking is the same
    curve, so the two are equal by construction and the declared seam proves it."""
    # The panel spans from the centre-front line out to the dajin's reach, and from the
    # underarm up to the shoulder.
    x0 = 0.0
    top = SHOULDER_Y
    p_bl = fc.P(x0, UNDERARM_Y)
    p_br = fc.P(DAJIN_X, UNDERARM_Y)
    p_neck = fc.P(NECK_HALF, top - NECK_DROP_F)
    p_shoulder = fc.P(NECK_HALF, top)
    p_tl = fc.P(x0, top)

    edges = [
        fc.Edge("under_edge", [fc.Line(p_bl, p_br)]),
        # THE edge: the same Bezier the body marks, run upward.
        fc.Edge("dajin", [_dajin_curve(DAJIN_X, UNDERARM_Y,
                                       NECK_HALF, top - NECK_DROP_F)]),
        fc.Edge("neck", [fc.Line(p_neck, p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_tl)]),
        fc.Edge("cf", [fc.Line(p_tl, p_bl)]),
    ]
    internals = []
    # The 盤扣 frogs, spaced by ARC LENGTH along the measured curve — not by chord.
    # Spacing by chord bunches them at the shoulder and gaps them at the underarm,
    # which is the visible signature of a robe drafted flat.
    dajin_edge = fc.Edge("probe", [_dajin_curve(DAJIN_X, UNDERARM_Y,
                                                NECK_HALF, top - NECK_DROP_F)])
    for i in range(frog_count):
        t = (i + 0.5) / frog_count
        pt, tangent = dajin_edge.point_at_fraction(t, 0.2)
        # The frog lies across the edge: the knot inboard, the loop outboard.
        nx, ny = -tangent.y, tangent.x
        internals.append(fc.Internal(
            f"frog-{i + 1}",
            [fc.P(pt.x - nx * frog_width * 0.5, pt.y - ny * frog_width * 0.5),
             fc.P(pt.x + nx * frog_width * 0.5, pt.y + ny * frog_width * 0.5)],
            kind="marking"))
    internals.append(fc.Internal(
        "facing-line",
        [fc.P(x0, UNDERARM_Y + 55.0), fc.P(DAJIN_X * 0.8, UNDERARM_Y + 55.0)],
        kind="marking"))
    return fc.Piece(
        "dajin", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("dajin", 0.5, "dajin midpoint"),
                 fc.Notch("under_edge", 0.5, "underarm match")],
        grainline=fc.Grainline(fc.P(DAJIN_X * 0.35, UNDERARM_Y + 40.0),
                               fc.P(DAJIN_X * 0.35, top - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Dajin overlap panel (大襟)",
    )


# ── The collar, cut to the MEASURED neckline ─────────────────────────────────
_BODY = build_body()
_FRONT = build_front()
_DAJIN = build_dajin()
BODY_NECK = _BODY.edge("neck").length(0.2)          # one BACK quarter
FRONT_NECK = _FRONT.edge("neck").length(0.2)        # the LEFT front quarter
DAJIN_MEASURED = _DAJIN.edge("dajin").length(0.2)
DAJIN_NECK = _DAJIN.edge("neck").length(0.2)        # the right front, on the overlap
# The stand collar runs the whole neckline: BOTH back quarters (the two body halves
# joined at centre back), the left front quarter, and the dajin's own neck edge on the
# right. All four MEASURED off the drawn pieces.
#
# A stand collar cut to `neck_girth + ease` is wrong, because the drafted neckline is
# not that circle: the four quarters are curves, the front drops, and the dajin adds a
# right-front run the circle never contained. The residual against the naive estimate
# is reported as collar_vs_neck_estimate_mm.
COLLAR_RUN = 2.0 * BODY_NECK + FRONT_NECK + DAJIN_NECK
COLLAR_NAIVE = neck_girth + NECK_EASE


def build_collar():
    """The 立領 stand collar: a straight band at DOUBLE the stand height plus
    turn-of-cloth, cut to the MEASURED neckline run."""
    ln = COLLAR_RUN
    turn = 4.0
    h = collar_height * 2.0 + turn
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        # The right end is the one that rises at the throat and takes the top frog.
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, collar_height + turn / 2.0),
                                  fc.P(ln, collar_height + turn / 2.0)],
                    kind="marking"),
        # The collar's own top frog, at the throat.
        fc.Internal("collar-frog",
                    [fc.P(ln - frog_width * 0.6, collar_height * 0.5),
                     fc.P(ln - 6.0, collar_height * 0.5)], kind="marking"),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", BODY_NECK / ln, "centre back"),
                 fc.Notch("neck_edge", (2.0 * BODY_NECK) / ln, "left shoulder"),
                 fc.Notch("neck_edge", (2.0 * BODY_NECK + FRONT_NECK) / ln,
                          "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Stand collar (立領)",
    )


def build_underarm():
    """The 插角 underarm gusset: a diamond set into the corner where the one-piece
    sleeve turns down into the side seam.

    A robe with no armscye has a right angle under the arm, and a right angle tears.
    The gusset is what lets the arm come down without the corner taking the strain —
    the same problem, and the same answer, as a smock or a kimono's 身八つ口."""
    g = max(dajin_drop * 0.30, 70.0)
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(g, 0.0)
    p2 = fc.P(g, g)
    p3 = fc.P(0.0, g)
    edges = [
        fc.Edge("body_lower", [fc.Line(p0, p1)]),
        fc.Edge("sleeve_lower", [fc.Line(p1, p2)]),
        fc.Edge("sleeve_upper", [fc.Line(p2, p3)]),
        fc.Edge("body_upper", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "underarm", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("body_lower", 0.5, "corner match")],
        grainline=fc.Grainline(fc.P(g * 0.2, g * 0.2), fc.P(g * 0.8, g * 0.8)),
        internals=[fc.Internal("bias-line", [fc.P(0.0, g), fc.P(g, 0.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Underarm gusset (插角)",
    )


def build():
    pattern = fc.PatternSet("changpao")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "dajin":
        pattern.add(build_dajin())
    if everything or target_piece == "collar":
        pattern.add(build_collar())
    if everything or target_piece == "underarm":
        pattern.add(build_underarm())

    if everything:
        # THE seam that had to solve: the collar against the MEASURED neckline — both
        # back quarters, the left front, and the dajin's own neck edge. Cut to a neck
        # girth instead and the 立領 comes up short at the throat, every time.
        pattern.declare_seam(("collar", "neck_edge"),
                             [("body", "neck"), ("body", "neck"),
                              ("front", "neck"), ("dajin", "neck")], tol=1.0)
        # The side seams: back half to front half, below the slit and up to the
        # underarm corner. Both panels are one loom width, so these are equal by
        # construction — declared so a shaped panel can never sneak into a robe whose
        # whole logic is the unshaped panel.
        pattern.declare_seam(("body", "side"), ("front", "side"), tol=0.5)
        pattern.declare_seam(("body", "sleeve_under"), ("front", "sleeve_under"),
                             tol=0.5)
        pattern.declare_seam(("body", "shoulder"), ("front", "shoulder"), tol=0.5)
        pattern.declare_seam(("body", "cuff"), ("front", "cuff"), tol=0.5)
        # The gusset's two body edges against its two sleeve edges — a square gusset,
        # declared so a rhombus cannot sneak in.
        pattern.declare_seam(("underarm", "body_lower"),
                             ("underarm", "sleeve_lower"), tol=0.5)
        pattern.declare_seam(("underarm", "body_upper"),
                             ("underarm", "sleeve_upper"), tol=0.5)

    # The bolt: a narrow loom cloth. manta-cruda is 900 mm, so a 480 mm panel takes
    # rather less than half the modern width — which is exactly the point being made.
    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "unbleached cotton (manta cruda) or plain silk",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at 900 mm width, 80% marker. The draft's own panel is "
                 f"{panel_width:.0f} mm — a handloom width — and the robe is built from "
                 f"panels used whole. Manta shrinks 5% in the warp: wash before cutting "
                 f"or the finished robe is 66 mm shorter than drafted."},
        {"item": "self-fabric bias strip (for 盤扣)",
         "qty": round((frog_count + 1) * frog_width * 6.0), "unit": "mm_length",
         "note": f"{frog_count + 1} frogs including the collar's; each knotted pánkòu "
                 f"eats roughly six times its finished span in bias strip."},
        {"item": "collar interlining", "qty": round(COLLAR_RUN), "unit": "mm_length",
         "note": f"{collar_height:.0f} mm stand; the 立領 must stand by itself, and an "
                 f"unstiffened stand collapses at the throat."},
        {"item": "facing cloth (dajin)", "qty": 1, "unit": "panel",
         "note": "the dajin is cut twice — face and facing — because its curved edge is "
                 "seen from both sides when the robe is open."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "traditionally hand-sewn, so the robe can be unpicked, washed as flat "
                 "panels, and re-sewn."},
    ]
    pattern.metadata = {
        "fc300_rank": 299,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "finished_mm": {
            "panel_width": round(panel_width, 1),
            "body_circuit": round(BODY_CIRCUIT, 1),
            "robe_length": round(robe_length, 1),
            "sleeve_length": round(sleeve_length, 1),
            "collar_height": round(collar_height, 1),
            "side_slit": round(side_slit, 1),
        },
        "solved": {
            "body_circuit_mm": round(BODY_CIRCUIT, 2),
            "chest_ease_mm": round(CHEST_EASE, 2),
            "panel_sufficient": PANEL_SUFFICIENT,
            "dajin_length_measured_mm": round(DAJIN_MEASURED, 3),
            "dajin_length_drafted_mm": round(DAJIN_LEN, 3),
            "dajin_chord_mm": round(DAJIN_CHORD, 3),
            "chord_shortfall_mm": round(CHORD_SHORTFALL, 3),
            "dajin_reach_x_mm": round(DAJIN_X, 2),
            "dajin_reach_clamped": REACH_CLAMPED,
            "back_neck_quarter_mm": round(BODY_NECK, 3),
            "front_neck_quarter_mm": round(FRONT_NECK, 3),
            "dajin_neck_measured_mm": round(DAJIN_NECK, 3),
            "collar_run_mm": round(COLLAR_RUN, 3),
            "collar_naive_estimate_mm": round(COLLAR_NAIVE, 3),
            "collar_vs_neck_estimate_mm": round(COLLAR_RUN - COLLAR_NAIVE, 3),
            "neck_opening_mm": round(NECK_HALF * 4.0, 3),
            "frog_spacing_arc_mm": round(DAJIN_MEASURED / frog_count, 3),
            "frog_spacing_chord_mm": round(DAJIN_CHORD / frog_count, 3),
            "side_slit_ceiling_mm": round(SLIT_CEILING, 2),
            "note": "the 大襟 (dàjīn) curve is drafted once and MEASURED, and the body "
                    "panel's matching seat is the same curve — equal by construction "
                    "rather than by two formulas hoping to agree. The frogs are spaced "
                    "by ARC LENGTH along that measured curve; spacing by chord "
                    "(frog_spacing_chord_mm) bunches them at the shoulder and gaps them "
                    "at the underarm, the visible signature of a robe drafted flat. The "
                    "立領 stand collar is cut to the MEASURED neckline — both back "
                    "quarters, the left front, and the dajin's own neck edge — not to "
                    "neck_girth + ease, which misses by collar_vs_neck_estimate_mm "
                    "because the drafted neckline is four curves plus a front drop plus "
                    "a right-front run, not a circle. The body circuit is computed FROM "
                    "the panel width plus the dajin's wrap-past, so a cloth too narrow "
                    "to wrap the wearer is reported as panel_sufficient=false rather "
                    "than silently widened.",
        },
        "heritage": {
            "garment": "長袍 chángpáo — the Chinese men's long robe",
            "construction": "連袖 one-piece sleeve (no armscye), 插角 underarm gusset, "
                            "立領 stand collar, 大襟 curved right-over-left overlap, "
                            "開衩 side slits, panels of loom width used whole",
            "closure": "盤扣 pánkòu — knotted cloth frogs, spaced along the dajin curve",
            "excluded": "no 補子 rank badge, no dragon roundel, no embroidery, no "
                        "clan or rank insignia is drafted here",
        },
        "hardware": "the closures are 盤扣 knotted cloth frogs. The Yantra4D frog-closure "
                    "solid does not yet exist on the shelf: the manifest declares an "
                    "UNLINKED hardware_ref naming yantra4d/frog-closure for co-creation, "
                    "in the form FC-200's co-create garments established. The frogs "
                    "remain hand-knotted cloth, which is what they are",
    }
    return pattern


result = build()
