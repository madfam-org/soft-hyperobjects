"""
Salwar kameez set — Fashion Cabinet Heritage Cartridge (FC-500 #491, heritage_global;
South Asia — Punjab and across the subcontinent).

The salwar kameez is the two-piece everyday and formal dress of Punjab and much of South Asia:
the KAMEEZ (a long straight tunic with side slits, worn by women and men) over the SALWAR (a
loose, pleated trouser drawn in at the waist and gathered narrow at the ankle). It is worn with
a dupatta (a long scarf, a separate garment, not drafted here). This cartridge drafts the
kameez and the salwar together as a set.

Two facts govern the salwar draft, and both are the reason a South-Asian trouser is not a
Western one:

  1. THE SALWAR IS PANELS AND A GUSSET, GATHERED AT BOTH ENDS. The leg is a wide rectangle
     drawn in at the waist by a drawstring and at the ankle by a narrow cuff. It is not cut to
     the body's crotch curve; the width is gathered away. The generous crotch is made by a
     DIAMOND GUSSET (the miyani / nala) set between the two legs, and that gusset is what lets
     the loose trouser move — its square-diamond geometry is drafted and declared.

  2. THE WAIST AND ANKLE ARE SOLVED FROM THE LEG WIDTH. The waist drawstring channel and the
     ankle cuff are each a fraction of the flat leg width, gathered in — the fullness is real
     and reported, not guessed.

Pieces:
  - kameez_f : the kameez front (cut on fold), straight, side slits, faced neck.
  - kameez_b : the kameez back (cut on fold), straight, side slits.
  - salwar   : one salwar leg (cut 2), wide rectangle tapered to the ankle cuff.
  - gusset   : the diamond crotch gusset (miyani), cut 1 (or 2 mirrored halves).

Hardware: none — the salwar draws with a cord (naala); the kameez pulls over the head.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # kameez_f|kameez_b|salwar|gusset|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
kameez_length = float(PARAM(lambda: kameez_length, 980.0))  # shoulder to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
neck_v_depth = float(PARAM(lambda: neck_v_depth, 180.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 400.0))  # tip to tip
side_slit = float(PARAM(lambda: side_slit, 300.0))
body_ease = float(PARAM(lambda: body_ease, 140.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))       # sets the salwar leg width
salwar_length = float(PARAM(lambda: salwar_length, 980.0))  # waist to ankle
ankle_girth = float(PARAM(lambda: ankle_girth, 260.0))
gusset_size = float(PARAM(lambda: gusset_size, 260.0))    # crotch gusset diagonal
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1300.0))
kameez_length = max(800.0, min(kameez_length, 1250.0))
neck_girth = max(320.0, min(neck_girth, 480.0))
neck_v_depth = max(80.0, min(neck_v_depth, 300.0))
shoulder_width = max(340.0, min(shoulder_width, 480.0))
side_slit = max(120.0, min(side_slit, 500.0))
body_ease = max(80.0, min(body_ease, 260.0))
hip_girth = max(820.0, min(hip_girth, 1400.0))
salwar_length = max(820.0, min(salwar_length, 1150.0))
ankle_girth = max(200.0, min(ankle_girth, 400.0))
gusset_size = max(160.0, min(gusset_size, 380.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# ── Kameez geometry ──────────────────────────────────────────────────────────
KAMEEZ_Q = (chest_girth + body_ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = min((neck_girth + 24.0) / 4.0, HALF_SHOULDER - 30.0)
FRONT_V = min(neck_v_depth, kameez_length * 0.35)
side_slit = min(side_slit, kameez_length * 0.5)
ARMHOLE_DEPTH = min(KAMEEZ_Q * 0.9, kameez_length * 0.28)

# ── Salwar geometry — panels + gusset, gathered ──────────────────────────────
# The flat leg width is generous (hip-derived), gathered at both ends. The waist fullness and
# ankle fullness are reported.
LEG_WIDTH = hip_girth * 0.62              # one leg's flat width (very full)
WAIST_PER_LEG = hip_girth / 2.0 + 60.0    # the drawstring gathers the leg to about this
WAIST_GATHER = (LEG_WIDTH * 2.0) / WAIST_PER_LEG  # top gathered onto the waist channel
ANKLE_CUFF = ankle_girth
ANKLE_GATHER = LEG_WIDTH / ANKLE_CUFF     # the leg gathered into the ankle cuff


def _kameez_half(neck_drop, front):
    """A kameez half (front or back) cut on the fold: straight body, grown-on short sleeve,
    faced neck, side slit."""
    q = KAMEEZ_Q
    top = kameez_length
    y_underarm = top - ARMHOLE_DEPTH
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(q, 0.0)
    p_underarm = fc.P(q, y_underarm)
    # grown-on short sleeve: the shoulder runs out past the body to a short sleeve end.
    sleeve_reach = min(q * 0.5, 180.0)
    p_sleeve_end = fc.P(q + sleeve_reach, y_underarm + ARMHOLE_DEPTH * 0.25)
    p_sleeve_top = fc.P(q + sleeve_reach, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cf = fc.P(0.0, top - neck_drop)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end, p_sleeve_top)]),
        fc.Edge("shoulder", [fc.Line(p_sleeve_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, top - 6.0),
                                   fc.P(NECK_HALF * 0.28, p_neck_cf.y + 10.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("slit-head", [fc.P(q, side_slit), fc.P(q - 24.0, side_slit)],
                    kind="marking"),
    ]
    if front:
        internals.append(fc.Internal("neck-facing",
                                     [fc.P(0.0, top - neck_drop - 30.0),
                                      fc.P(NECK_HALF + 20.0, top - 8.0)], kind="marking"))
    return edges, internals


def build_kameez_front():
    edges, internals = _kameez_half(FRONT_V, True)
    return fc.Piece(
        "kameez_f", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(kameez_length - ARMHOLE_DEPTH, 1.0), "slit")],
        grainline=fc.Grainline(fc.P(KAMEEZ_Q * 0.3, hem_allowance + 30.0),
                               fc.P(KAMEEZ_Q * 0.3, kameez_length - ARMHOLE_DEPTH - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Kameez front (side slit, faced V-neck), cut on fold",
    )


def build_kameez_back():
    edges, internals = _kameez_half(28.0, False)
    return fc.Piece(
        "kameez_b", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", side_slit / max(kameez_length - ARMHOLE_DEPTH, 1.0), "slit")],
        grainline=fc.Grainline(fc.P(KAMEEZ_Q * 0.3, hem_allowance + 30.0),
                               fc.P(KAMEEZ_Q * 0.3, kameez_length - ARMHOLE_DEPTH - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Kameez back (side slit), cut on fold",
    )


def build_salwar():
    """One salwar leg (cut 2): a wide rectangle, the waist edge full (gathered onto the
    drawstring channel), tapering to the narrow ankle cuff."""
    w_top = LEG_WIDTH
    ankle = ANKLE_CUFF
    h = salwar_length
    # the leg tapers from the full top to the narrow ankle; the inner (crotch) edge is straight
    # and the gusset is set between the two legs.
    p_ankle_l = fc.P((w_top - ankle) / 2.0, 0.0)
    p_ankle_r = fc.P((w_top + ankle) / 2.0, 0.0)
    p_top_r = fc.P(w_top, h)
    p_top_l = fc.P(0.0, h)
    edges = [
        fc.Edge("ankle", [fc.Line(p_ankle_l, p_ankle_r)]),
        fc.Edge("outseam", [fc.Line(p_ankle_r, p_top_r)]),
        fc.Edge("waist", [fc.Line(p_top_r, p_top_l)]),   # gathered onto the drawstring channel
        fc.Edge("inseam", [fc.Line(p_top_l, p_ankle_l)]),
    ]
    internals = [
        fc.Internal("waist-channel", [fc.P(0.0, h - 40.0), fc.P(w_top, h - 40.0)],
                    kind="marking"),
        fc.Internal("gusset-seat", [fc.P(0.0, h - gusset_size), fc.P(gusset_size * 0.3, h)],
                    kind="marking"),
    ]
    return fc.Piece(
        "salwar", edges,
        seam_allowance=seam_allowance,
        allowances={"ankle": hem_allowance * 0.6, "waist": 0.0},
        notches=[fc.Notch("waist", 0.5, "leg centre"),
                 fc.Notch("inseam", 0.5, "inseam mid")],
        grainline=fc.Grainline(fc.P(w_top * 0.5, hem_allowance + 20.0),
                               fc.P(w_top * 0.5, h - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Salwar leg (full waist, narrow ankle)",
    )


def build_gusset():
    """The diamond crotch gusset (miyani / nala): a square set on point between the two legs,
    what lets the loose trouser move. Declared square so it stays a diamond, not a wedge."""
    g = gusset_size
    # a square drawn on point (a diamond): the four corners.
    p_bottom = fc.P(g * 0.5, 0.0)
    p_right = fc.P(g, g * 0.5)
    p_top = fc.P(g * 0.5, g)
    p_left = fc.P(0.0, g * 0.5)
    edges = [
        fc.Edge("leg_r_lower", [fc.Line(p_bottom, p_right)]),
        fc.Edge("leg_r_upper", [fc.Line(p_right, p_top)]),
        fc.Edge("leg_l_upper", [fc.Line(p_top, p_left)]),
        fc.Edge("leg_l_lower", [fc.Line(p_left, p_bottom)]),
    ]
    return fc.Piece(
        "gusset", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("leg_r_lower", 0.5, "crotch point")],
        grainline=fc.Grainline(fc.P(g * 0.5, g * 0.2), fc.P(g * 0.5, g * 0.8)),
        internals=[fc.Internal("bias", [fc.P(0.0, g * 0.5), fc.P(g, g * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Crotch gusset (miyani / nala)",
    )


def build():
    pattern = fc.PatternSet("salwar-kameez-set")
    everything = target_piece == "set"
    if everything or target_piece == "kameez_f":
        pattern.add(build_kameez_front())
    if everything or target_piece == "kameez_b":
        pattern.add(build_kameez_back())
    if everything or target_piece == "salwar":
        pattern.add(build_salwar())
    if everything or target_piece == "gusset":
        pattern.add(build_gusset())

    if everything:
        # The kameez side seams and shoulders match front to back.
        pattern.declare_seam(("kameez_f", "side"), ("kameez_b", "side"), tol=1.0)
        pattern.declare_seam(("kameez_f", "shoulder"), ("kameez_b", "shoulder"), tol=1.0)
        pattern.declare_seam(("kameez_f", "sleeve_under"), ("kameez_b", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("kameez_f", "cuff"), ("kameez_b", "cuff"), tol=1.0)
        # The gusset: its two right-leg edges against its two left-leg edges — declared so the
        # diamond stays a square-on-point (a symmetric crotch), not a lopsided wedge.
        pattern.declare_seam(("gusset", "leg_r_lower"), ("gusset", "leg_l_lower"), tol=0.5)
        pattern.declare_seam(("gusset", "leg_r_upper"), ("gusset", "leg_l_upper"), tol=0.5)

    pattern.bom = [
        {"item": "cotton voile / lawn (kameez + salwar)", "qty": round(
            (kameez_length + salwar_length + hem_allowance) * 2.6 / 10.0) * 10,
         "unit": "mm_length",
         "note": "the salwar is very full — the leg width is generous and gathered at both "
                 "ends, so the cloth quantity is high."},
        {"item": "waist drawstring (naala)", "qty": round(WAIST_PER_LEG * 2.0 + 400.0),
         "unit": "mm_length", "note": "the cord that draws the salwar waist in."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 491,
        "family": "heritage_global",
        "fabric_hint": "algodon-voile",
        "finished_mm": {
            "kameez_length": round(kameez_length, 1),
            "salwar_length": round(salwar_length, 1),
            "leg_width": round(LEG_WIDTH, 1),
            "ankle_girth": round(ANKLE_CUFF, 1),
        },
        "solved": {
            "kameez_quarter_mm": round(KAMEEZ_Q, 2),
            "leg_width_mm": round(LEG_WIDTH, 2),
            "waist_per_leg_mm": round(WAIST_PER_LEG, 2),
            "waist_gather_ratio": round(WAIST_GATHER, 2),
            "ankle_cuff_mm": round(ANKLE_CUFF, 2),
            "ankle_gather_ratio": round(ANKLE_GATHER, 2),
            "gusset_size_mm": round(gusset_size, 2),
            "side_slit_mm": round(side_slit, 2),
            "note": "the salwar is PANELS AND A GUSSET, gathered at both ends: the wide leg is "
                    "drawn in at the waist by a drawstring (waist_gather_ratio) and at the "
                    "ankle by a narrow cuff (ankle_gather_ratio), not cut to the body's crotch "
                    "curve. The generous crotch is the DIAMOND gusset (miyani/nala), declared "
                    "square-on-point so it stays a symmetric diamond rather than a lopsided "
                    "wedge. The kameez is a straight tunic with side slits and a faced neck.",
        },
        "heritage": {
            "garment": "salwar kameez — the two-piece dress of Punjab and South Asia",
            "worn": "the kameez tunic over the salwar trouser, with a dupatta scarf (a "
                    "separate garment, not drafted here); by women and men across the "
                    "subcontinent",
            "construction": "straight kameez with side slits; loose salwar gathered at the "
                            "waist drawstring and ankle cuff, with a diamond crotch gusset",
            "excluded": "no embroidery, phulkari, or print motif is drawn — the cloth and its "
                        "ornament are the maker's",
        },
        "hardware": "none — the salwar draws with a cord (naala); the kameez pulls over the "
                    "head.",
    }
    return pattern


result = build()
