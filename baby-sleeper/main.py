"""
Baby sleeper (footed pajama) — FC-100 rank #94 (Mameluco con pies (pijama)).
Fashion Cabinet Garment Cartridge.

The classic zip-up footed baby pajama, as a parametric knit ONE-PIECE. Each
body half (a FRONT cut 2 for the front zip, a BACK cut 1 on fold at CB) runs
continuously from the neck, over the shoulder and armhole, down the side, down
the leg outseam, AROUND AN ENCLOSED FOOT, and back up the inseam to the crotch
— bodice + long leg + foot in a single closed outline. FRONT and BACK share
identical shoulder / armhole / side / outseam / inseam / foot geometry, so
every one of those declared seams closes with delta ~ 0 BY CONSTRUCTION; the
only front/back difference is the neck scoop and the centre edge (a straight CF
ZIP edge vs a CB fold).

The two signatures:
  * FOOTIES — the leg does not hem: it rounds into a toe box (the `foot` edge),
    and a separate flat SOLE (cut 2) is seamed underneath. The sole is a lens of
    two curves each SOLVED by bisection to equal the body `foot` edge, so the
    foot-attach seam (`sole.attach_out + sole.attach_in` == `front.foot +
    back.foot`) balances exactly.
  * ZIPPER — a full-length front separating zipper runs the CF from the neck to
    the crotch (a production 2-way sleeper diverts the tail down one inner leg
    to the ankle; noted honestly). Marked as an internal CF trace + stop notch;
    the hardware itself is a Yantra4D cartridge reference in the BOM.

Long sleeves cut 2, knit cap SOLVED to the front + back armholes, with an
optional fold-over mitten cuff (a newborn hand cover) marked as a fold line.
Soft cotton-jersey knit ease; a bound neck (strip derived from the measured
opening, not length-checked — a bound edge, like the tee's neckband).

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body, infant proportion) ────────
_KNOWN = ("front", "back", "sleeve", "sole", "neck_binding", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth = float(PARAM(lambda: chest_girth, 520.0))
hip_girth = float(PARAM(lambda: hip_girth, 540.0))
neck_girth = float(PARAM(lambda: neck_girth, 260.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 130.0))
body_length = float(PARAM(lambda: body_length, 300.0))    # crotch line to HPS
inseam_length = float(PARAM(lambda: inseam_length, 240.0))  # ankle line to crotch
sleeve_length = float(PARAM(lambda: sleeve_length, 200.0))  # cap apex to cuff
foot_length = float(PARAM(lambda: foot_length, 100.0))     # ankle line to toe tip
knit_ease = float(PARAM(lambda: knit_ease, 80.0))          # roomy pull-on infant ease
binding_ratio = float(PARAM(lambda: binding_ratio, 0.90))  # neck rib length / opening
binding_width = float(PARAM(lambda: binding_width, 18.0))  # finished neck-band height
footed = bool(PARAM(lambda: footed, True))                 # footed | cuffed-open legs
cuff_style = str(PARAM(lambda: cuff_style, "mitten"))      # mitten | plain sleeve cuff
zip_guard = bool(PARAM(lambda: zip_guard, True))           # chin flap at the neck
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match the manifest sliders) ──────────────────────────────────────
chest_girth = max(380.0, min(chest_girth, 760.0))
hip_girth = max(380.0, min(hip_girth, 800.0))
neck_girth = max(200.0, min(neck_girth, 420.0))
ankle_girth = max(90.0, min(ankle_girth, 260.0))
body_length = max(220.0, min(body_length, 520.0))
inseam_length = max(140.0, min(inseam_length, 520.0))
sleeve_length = max(110.0, min(sleeve_length, 420.0))
foot_length = max(70.0, min(foot_length, 190.0))
knit_ease = max(0.0, min(knit_ease, 260.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))
binding_width = max(10.0, min(binding_width, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 50.0))

# ── Frame (y-up; toe at y=0, ankle above it, crotch, underarm, HPS on top) ───
SHOULDER_DROP = 28.0      # relaxed infant drop shoulder
FRONT_NECK_DROP = 62.0    # CF neck scoop below the HPS line
BACK_NECK_DROP = 18.0     # shallow CB scoop
NW = max(40.0, neck_girth / 5.0)                 # half neck width at the HPS

W = (chest_girth + knit_ease) / 4.0              # quarter body width (fold at CF/CB)
AH = (chest_girth + knit_ease) / 8.0 + 55.0      # armhole depth (infant)

FOOT_H = foot_length
ANKLE_Y = FOOT_H
CROTCH_Y = FOOT_H + inseam_length
HPS_Y = CROTCH_Y + body_length
# Keep the torso above the crotch: cap AH so the underarm sits clear of the leg.
AH = max(70.0, min(AH, HPS_Y - SHOULDER_DROP - CROTCH_Y - 40.0))
UNDERARM_Y = HPS_Y - SHOULDER_DROP - AH

# Leg + foot geometry. The front-half leg spans inner (inseam) to outer
# (outseam); the full ankle circumference is 2x the half-leg ankle width.
ANKLE_INNER_X = 8.0
ANKLE_OUTER_X = ANKLE_INNER_X + ankle_girth / 2.0
TOE_X = (ANKLE_INNER_X + ANKLE_OUTER_X) / 2.0    # toe tip centred under the leg

HPS = fc.P(NW, HPS_Y)
SH_END = fc.P(W - 6.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, UNDERARM_Y)
HIP = fc.P(W, CROTCH_Y)
CROTCH = fc.P(0.0, CROTCH_Y)
ANKLE_OUT = fc.P(ANKLE_OUTER_X, ANKLE_Y)
ANKLE_IN = fc.P(ANKLE_INNER_X, ANKLE_Y)


# ── Shared body edges (front & back are identical except neck + centre) ──────
def _armhole_edge():
    """Drop-shoulder armhole; front and back share it (cap solves to 2x)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM_Y + AH * 0.30), UNDERARM)],
    )


def _side_edge():
    return fc.Edge("side", [fc.Line(UNDERARM, HIP)])


def _outseam_edge():
    """Torso side flows straight into the leg outside, hip down to ankle."""
    return fc.Edge(
        "outseam",
        [fc.curve_through(HIP, ANKLE_OUT, bulge=0.05, side=1.0)],
    )


def _inseam_edge():
    """Inner leg: ankle-inner up to the crotch point on the centre line."""
    return fc.Edge("inseam", [fc.Line(ANKLE_IN, CROTCH)])


def _foot_edge():
    """Enclosed foot: a rounded toe box from ankle-outer to ankle-inner.

    Two beziers over the toe tip at y=0; this is the sole-attach edge. Its
    length FOOT_LEN drives the solved sole so the foot-attach seam is exact.
    """
    toe = fc.P(TOE_X, 0.0)
    out_to_toe = fc.Bezier(
        ANKLE_OUT,
        fc.P(ANKLE_OUTER_X, ANKLE_Y * 0.35),
        fc.P(TOE_X + (ANKLE_OUTER_X - TOE_X) * 0.45, 0.0),
        toe,
    )
    toe_to_in = fc.Bezier(
        toe,
        fc.P(TOE_X - (TOE_X - ANKLE_INNER_X) * 0.45, 0.0),
        fc.P(ANKLE_INNER_X, ANKLE_Y * 0.35),
        ANKLE_IN,
    )
    return fc.Edge("foot", [out_to_toe, toe_to_in])


def _cuff_edge():
    """Open leg cuff (cuffed-open variant): a straight ankle line, no foot."""
    return fc.Edge("cuff", [fc.Line(ANKLE_OUT, ANKLE_IN)])


def FOOT_LEN():
    return _foot_edge().length(0.05)


def _leg_close():
    """Return the leg-bottom edges between outseam-end and inseam-start.

    Footed: the enclosed foot. Cuffed-open: a straight hemmed ankle. Either
    way the two endpoints are ANKLE_OUT and ANKLE_IN, so the outline closes.
    """
    return [_foot_edge()] if footed else [_cuff_edge()]


def _body_piece(name, center_name, neck_edge, cut, allow, extra_internals, label):
    edges = [
        fc.Edge(center_name, [fc.Line(CROTCH, fc.P(0.0, neck_edge.start.y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(HPS, SH_END)]),
        _armhole_edge(),
        _side_edge(),
        _outseam_edge(),
        *_leg_close(),
        _inseam_edge(),
    ]
    notches = [
        fc.Notch("side", 0.5, "underarm-hip match"),
        fc.Notch("outseam", 0.5, "leg match"),
        fc.Notch("inseam", 0.5, "leg match"),
        fc.Notch("armhole", 0.5, f"{name} armhole"),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances=allow,
        notches=notches,
        grainline=fc.Grainline(fc.P(W * 0.5, CROTCH_Y + 30.0),
                               fc.P(W * 0.5, HPS_Y - SHOULDER_DROP - 30.0)),
        internals=extra_internals,
        cut=cut,
        label=label,
    )


def build_front():
    cf_neck_y = HPS_Y - FRONT_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cf_neck_y), fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + FRONT_NECK_DROP * 0.45), HPS)],
    )
    # CF zip trace from the neck down to the crotch (the full front opening),
    # plus a stop notch where the torso zip ends at the crotch.
    internals = [fc.Internal(
        "front zip (CF, cut open between the two fronts)",
        [fc.P(0.0, cf_neck_y), CROTCH], kind="trace")]
    if zip_guard:
        internals.append(fc.Internal(
            "zip guard / chin flap (fold behind the top of the zip)",
            [fc.P(0.0, cf_neck_y), fc.P(14.0, cf_neck_y),
             fc.P(14.0, cf_neck_y - 40.0), fc.P(0.0, cf_neck_y - 40.0)],
            kind="marking"))
    piece = _body_piece(
        "front", "cf", neck,
        fc.CutSpec(quantity=2, mirror=True),
        {"cf": max(seam_allowance, 12.0)},   # CF carries the zipper tape
        internals, "Front (zip half)")
    piece.notches.append(fc.Notch("cf", 0.0, "zip stop at crotch"))
    return piece


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), HPS, bulge=0.12, side=-1.0)],
    )
    return _body_piece(
        "back", "cb", neck,
        fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        {}, [], "Back (on fold)")


# ── Long sleeve (knit cap solved to the armholes) ────────────────────────────
def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R->L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    ch = max(38.0, AH * 0.32)                       # shallow knit cap height
    sl = max(55.0, sleeve_length - ch)              # underarm-to-cuff run
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(48):                             # bisect: cap grows with hb
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs {cap_target:.1f}")
    # Snug infant wrist: cuff width is a fraction of the underarm width.
    cw = max(45.0, hb * 0.72)
    internals = []
    cuff_allow = hem_allowance
    if cuff_style == "mitten":
        # Fold-over hand cover: extra length below the wrist, folded back.
        cuff_allow = hem_allowance + 55.0
        internals.append(fc.Internal(
            "mitten cuff fold line (fold back over the hand)",
            [fc.P(-cw, 0.0), fc.P(cw, 0.0)], kind="marking"))
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-cw, 0.0), fc.P(cw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(cw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-cw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": cuff_allow},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 25.0), fc.P(0.0, sl + ch * 0.6)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (long)",
    )


# ── Foot sole (a lens of two curves each solved to the foot edge) ────────────
def _sole_edge(name, p0, p1, bulge, side):
    return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])


def build_sole(foot_len):
    """Flat sole: heel-to-toe chord, two mirrored curves each == foot_len.

    Each foot half (front.foot, back.foot) sews to one sole edge; the two sole
    edges summed == the two body foot edges summed, delta ~ 0 by the solve.
    """
    # Chord scales with the foot edge so the solved bulge stays well-behaved
    # (~0.8) across the whole size range; never narrower than the ankle.
    length = max(foot_len * 0.6, ankle_girth / 2.0 + 20.0)
    heel = fc.P(0.0, 0.0)
    toe = fc.P(length, 0.0)
    lo, hi = 0.05, 1.8
    bulge = hi
    for _ in range(56):                             # bisect: edge grows with bulge
        bulge = (lo + hi) / 2.0
        if _sole_edge("t", heel, toe, bulge, 1.0).segments[0].length(0.05) < foot_len:
            lo = bulge
        else:
            hi = bulge
    got = _sole_edge("t", heel, toe, bulge, 1.0).segments[0].length(0.05)
    if abs(got - foot_len) > 0.6:
        raise ValueError(
            f"sole solver did not converge: {got:.1f} vs foot {foot_len:.1f}")
    edges = [
        _sole_edge("attach_out", heel, toe, bulge, 1.0),
        _sole_edge("attach_in", toe, heel, bulge, 1.0),
    ]
    return fc.Piece(
        "sole", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach_out", 0.5, "toe/heel match")],
        grainline=fc.Grainline(fc.P(length * 0.5, -6.0), fc.P(length * 0.5, 6.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Foot Sole",
    )


# ── Bound neck (a strip from the measured opening; not length-checked) ───────
def build_neck_binding(front_piece, back_piece):
    # Front cut 2 -> two front neck edges; back on fold -> two back neck edges.
    opening = 2.0 * front_piece.edge("neck").length() + \
        2.0 * back_piece.edge("neck").length()
    band_len = opening * binding_ratio + 2.0 * seam_allowance
    band_h = 2.0 * binding_width                    # folded lengthwise when sewn
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neck_binding", edges,
        seam_allowance=0.0,                         # length already includes joins
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Neck Binding (rib)",
    )


def build():
    pattern = fc.PatternSet("baby-sleeper")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    foot_len = FOOT_LEN()

    known = target_piece in _KNOWN
    wanted = {
        "front": not known or target_piece in ("front", "set"),
        "back": not known or target_piece in ("back", "set"),
        "sleeve": not known or target_piece in ("sleeve", "set"),
        "sole": (not known or target_piece in ("sole", "set")) and footed,
        "neck_binding": not known or target_piece in ("neck_binding", "set"),
    }

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["sole"]:
        pattern.add(build_sole(foot_len))
    if wanted["neck_binding"]:
        pattern.add(build_neck_binding(front, back))

    # ── Declared seams (all delta ~ 0 by shared geometry / solves) ──────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "outseam"), ("back", "outseam"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        # Cap eases slightly into the combined armhole (knit, small ease).
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            ease=0.0, tol=2.0)
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0)
    if wanted["sole"] and wanted["front"] and wanted["back"]:
        # FOOT ATTACH: one sole per foot wraps front.foot + back.foot. Both
        # sides sum to 2x the foot edge, so delta ~ 0 by the sole solve.
        pattern.declare_seam(
            [("sole", "attach_out"), ("sole", "attach_in")],
            [("front", "foot"), ("back", "foot")],
            tol=1.5)

    # ── BOM ─────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                           # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name != "neck_binding")
    marker_len = total_area / (fabric_width * 0.72)  # knits nest tightly
    pattern.bom.append({
        "item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10,
        "unit": "mm_length",
        "note": f"at {fabric_width:.0f} mm width, ~72% marker efficiency (knit)",
    })
    if wanted["front"]:
        cf_len = front.edge("cf").length()
        pattern.bom.append({
            "item": "separating zipper, 2-way (front)",
            "qty": round(cf_len), "unit": "mm",
            "note": "hardware via Yantra4D zipper cartridge (not modelled here); "
                    "runs the CF neck-to-crotch; a production sleeper uses a "
                    "2-way tail that diverts down one inner leg to the ankle",
        })
    if wanted["neck_binding"]:
        opening = 2.0 * front.edge("neck").length() + 2.0 * back.edge("neck").length()
        pattern.bom.append({
            "item": "1x1 rib for neck binding",
            "qty": round(opening * binding_ratio + 2.0 * seam_allowance),
            "unit": "mm",
            "note": f"neck opening {round(opening)} mm x {binding_ratio:.2f} ratio "
                    "+ seam allowance; cut on the greatest-stretch grain",
        })
    if wanted["sole"]:
        pattern.bom.append({
            "item": "foot / ankle binding (optional)",
            "qty": round(2.0 * foot_len), "unit": "mm",
            "note": "both foot openings; only if the sole is bound rather than "
                    "turned — otherwise omit",
        })
    pattern.bom.append({
        "item": "polyester stretch thread + ballpoint needle",
        "qty": 1, "unit": "set", "note": "75/11 ballpoint for single jersey",
    })
    pattern.bom.append({
        "item": "sleepwear compliance note",
        "qty": 1, "unit": "note",
        "note": "infant sleepwear is regulated: cut SNUG-FITTING (this knit "
                "block, low ease) OR use inherently flame-resistant fabric; "
                "loose cotton sleepwear is non-compliant in many markets",
    })

    pattern.metadata = {
        "fc100_rank": 94,
        "fabric_hint": "jersey-algodon",
        "footed": footed,
        "cuff_style": cuff_style,
        "foot_edge_mm": round(foot_len, 1),
        "sole_perimeter_mm": round(2.0 * foot_len, 1),
        "front_zip_mm": round(front.edge("cf").length(), 1),
        "sleeve_cap_mm": round(cap_target, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "neck_opening_mm": round(
            2.0 * front.edge("neck").length() + 2.0 * back.edge("neck").length(), 1),
        "half_body_width_mm": round(W, 1),
        "drafting": "one-piece infant knit sleeper: bodice + long leg + enclosed "
                    "foot in a single outline; front cut 2 for the CF zip, back "
                    "cut 1 on fold; front/back share leg+foot geometry so those "
                    "seams close by construction; sleeve cap and foot sole solved "
                    "by bisection to their mating edges",
        "teaching_grade": "the foot is drafted as a flat toe box with a seamed "
                          "sole (a real footed-pajama construction); a couture "
                          "sleeper may shape a 3D last-fitted foot. The 2-way "
                          "ankle-diverting zip is represented as a CF neck-to-"
                          "crotch zip plus a construction note.",
    }
    return pattern


result = build()
