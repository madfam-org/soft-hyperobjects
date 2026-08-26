"""
Merino ski base-layer set — Fashion Cabinet Garment Cartridge
(FC-500 rank #456, active_swim, no hardware — pure pattern).

A two-piece merino base-layer set for skiing: a long-sleeve crew top and full-length leggings in
fine merino jersey, cut at slight negative ease so they sit as a warm second skin under a shell,
with flatlock seams so nothing chafes under load all day. One cartridge, two garments — a `top`
mode and a `bottom` mode selected by the `garment` parameter.

Two real decisions:

  1. TWO GARMENTS, ONE SOLVER. The `garment` parameter switches the assembled pieces between the
     crew top (front, back, sleeve) and the leggings (leg front, leg back); the measurements and
     the negative-ease solver are shared, so a set drafted together fits together.

  2. NEGATIVE EASE + SHARED SEAMS. The top's shoulders are congruent front-to-back; the leggings'
     front and back share ONE crotch so the leg cannot twist. Nothing is clamped negative.

Pieces (top): top_front, top_back, top_sleeve. Pieces (bottom): leg_front, leg_back.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "top"))     # top|bottom (the mode selector)
garment = str(PARAM(lambda: garment, target_piece if target_piece in ("top", "bottom") else "top"))

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
back_length = float(PARAM(lambda: back_length, 660.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 330.0))
outseam = float(PARAM(lambda: outseam, 1000.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 260.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1400.0))
waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
back_length = max(480.0, min(back_length, 860.0))
sleeve_length = max(400.0, min(sleeve_length, 720.0))
bicep_girth = max(240.0, min(bicep_girth, 560.0))
outseam = max(760.0, min(outseam, 1200.0))
ankle_girth = max(180.0, min(ankle_girth, 400.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 14.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
HIP_FIN = hip_girth * NEG
WAIST_FIN = waist_girth * NEG
ANKLE_FIN = ankle_girth * NEG
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 2.0
ARM_DEPTH = back_length * 0.28
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0


def build_top_front():
    w = FRONT_HALF
    h = back_length
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 20.0            # neck-POINT drop, congruent with the back so shoulders match
    CF_DROP = 40.0             # the crew neckline dips lower at the centre front only
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - CF_DROP))]),
        fc.Edge("neckline", [fc.curve_through(fc.P(0.0, h - CF_DROP), neck_pt, bulge=0.3,
                side=1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder, fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7), arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "top_front", edges, seam_allowance=seam_allowance, allowances={"hem": 25.0,
                "center_front": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_front", mirror=True),
        label="Top front (crew, cut 1 on fold)")


def build_top_back():
    w = BACK_HALF
    h = back_length
    neck_x = max(w * 0.20, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 20.0
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.curve_through(fc.P(0.0, h), fc.P(neck_x, h - NECK_DROP),
                                              bulge=0.16, side=1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder, fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "top_back", edges, seam_allowance=seam_allowance, allowances={"hem": 25.0,
                "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Top back (cut 1 on fold)")


def build_top_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * NEG * 0.66, armhole_ring * 0.62)
    cap_w = min(armhole_ring * 0.9, wrist * 1.4)
    bow = ARM_DEPTH * 0.55
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln), fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow), fc.P(cap_w, ln))]).length()
        if test < 1e-6:
            break
        ratio = armhole_ring / test
        if ratio > 1.0:
            cap_w = min(cap_w * ratio, armhole_ring)
        else:
            bow = max(4.0, bow * ratio)
        cap_w = max(wrist + 10.0, cap_w)
        if abs(test - armhole_ring) < 0.4:
            break
    cuff_off = (cap_w - wrist) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Line(fc.P(cuff_off, 0.0), fc.P(cuff_off + wrist, 0.0))]),
        fc.Edge("underseam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln), fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow), fc.P(0.0, ln))]),
        fc.Edge("underseam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "top_sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 20.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Top sleeve (cut 2)")


WB = 40.0
SIDE_LEN = outseam - WB
QUARTER_HIP = HIP_FIN / 4.0
CROTCH_Y = SIDE_LEN - (outseam * 0.28) - 50.0
CROTCH_X = -QUARTER_HIP * 0.13
ANK_HALF = ANKLE_FIN / 2.0


def _leg(name, label, back):
    top = WAIST_FIN / 4.0
    ankw = ANK_HALF
    cf = "centre_back" if back else "centre_front"
    rise = SIDE_LEN + (30.0 if back else 0.0)
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(top, SIDE_LEN), fc.P(0.0, rise))]),
        fc.Edge(cf, [fc.Bezier(fc.P(0.0, rise), fc.P(QUARTER_HIP * (0.24 if back else 0.14),
                SIDE_LEN - 30.0),
                               fc.P(QUARTER_HIP * 0.08, CROTCH_Y + 30.0), fc.P(CROTCH_X,
                                       CROTCH_Y))]),
        fc.Edge("inseam", [fc.Line(fc.P(CROTCH_X, CROTCH_Y), fc.P(0.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(ankw, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(ankw, 0.0), fc.P(top, SIDE_LEN))]),
    ]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance, allowances={"hem": 30.0},
        notches=[fc.Notch("side", 0.5, "knee"), fc.Notch("inseam", 0.5, "knee")],
        grainline=fc.Grainline(fc.P(ankw * 0.5 + 20.0, 40.0), fc.P(top * 0.5, SIDE_LEN - 40.0)),
        cut=fc.CutSpec(quantity=2, mirror=True), label=label)


def build():
    pattern = fc.PatternSet("ski-base-layer-set")
    if garment == "bottom":
        lf = _leg("leg_front", "Legging front", back=False)
        lb = _leg("leg_back", "Legging back", back=True)
        for piece in (lf, lb):
            pattern.add(piece)
        pattern.declare_seam(("leg_front", "side"), ("leg_back", "side"), tol=1.5,
                             ease=(lf.edge("side").length() - lb.edge("side").length()))
        pattern.declare_seam(("leg_front", "inseam"), ("leg_back", "inseam"), tol=1.0)
        return _finish(pattern, "bottom")
    # top
    tf = build_top_front()
    tb = build_top_back()
    armhole_ring = tf.edge("armhole").length() + tb.edge("armhole").length()
    sleeve = build_top_sleeve(armhole_ring)
    for piece in (tf, tb, sleeve):
        pattern.add(piece)
    pattern.declare_seam(("top_front", "side_seam"), ("top_back", "side_seam"), tol=1.5)
    pattern.declare_seam(("top_front", "shoulder"), ("top_back", "shoulder"), tol=1.0)
    pattern.declare_seam(("top_sleeve", "cap"),
                         [("top_front", "armhole"), ("top_back", "armhole")], tol=2.5)
    return _finish(pattern, "top")


def _finish(pattern, which):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "fine merino jersey (170-200 gsm)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a fine merino at slight negative ease so it wicks and warms as a second skin "
                 "under a ski shell."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes under a pack and boots all day."},
        {"item": "soft waistband elastic" if which == "bottom" else "neck-binding rib",
         "qty": round((WAIST_FIN if which == "bottom" else CHEST_FIN * 0.3) + 60.0),
         "unit": "mm_length",
         "note": "a soft covered elastic waistband (bottom) or a flat rib neckline (top)."},
    ]
    pattern.metadata = {
        "fc500_rank": 456, "family": "active_swim", "fabric_hint": "punto-merino",
        "silhouette_note": "A merino ski base-layer set: a long-sleeve crew top and full-length "
            "leggings at slight negative ease, flatlock-seamed, worn as a warm second skin.",
        "hardware": "none — pull-on merino base layers with no closures or hardware.",
        "solver": {
            "garment": which, "chest_finished_mm": round(CHEST_FIN, 1),
            "note": "one solver drives both garments; the top shoulders are congruent front-to-"
                    "back and the leggings' front and back share ONE crotch so the leg cannot "
                    "twist; slight negative ease, nothing clamped negative.",
        },
        "active": {"use": "skiing and cold-weather endurance; a wicking, warming merino base layer "
                   "under a shell, top and leggings drafted as a matched set."},
    }
    return pattern


result = build()
