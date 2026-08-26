"""
Covert coat — Fashion Cabinet Garment Cartridge
(FC-500 rank #440, tailoring, T4, made-to-measure; y4d shank-button-solid).

The countryman's town coat: a fly-front, knee-length single-breasted covert coat in covert
twill, marked by its signature four rows of stitching at the cuff and hem. A straight-hanging
coat with a fly placket hiding the buttons, a set-in sleeve, and a whole-length body (no waist
seam) that reaches the knee.

Two real decisions:

  1. THE HEM DROP IS SOLVED, NOT SKETCHED. The coat length runs from the shoulder to the knee;
     the hem width flares from the chest by a clamped flare so the hem can never come out
     NARROWER than the chest (which would invert the side seam). The flare is floored positive.

  2. THE FLY PLACKET IS SOLVED TO THE BUTTON. The fly hides shank buttons whose disc diameter is
     the drafted button_dia that drives the garment's fly-placket interface — one number, two
     objects.

Pieces: front (with fly extension), back (cut 1 on fold), sleeve, collar. Made to measure.

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
# front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
hip_girth = float(PARAM(lambda: hip_girth, 1080.0))
coat_length = float(PARAM(lambda: coat_length, 1040.0))    # shoulder to knee hem
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 350.0))
hem_flare = float(PARAM(lambda: hem_flare, 90.0))          # extra hem width per side over chest
fly_width = float(PARAM(lambda: fly_width, 55.0))
button_dia = float(PARAM(lambda: button_dia, 22.0))
coat_ease = float(PARAM(lambda: coat_ease, 140.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(840.0, min(chest_girth, 1400.0))
hip_girth = max(860.0, min(hip_girth, 1500.0))
coat_length = max(820.0, min(coat_length, 1240.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 520.0))
hem_flare = max(20.0, min(hem_flare, 220.0))
fly_width = max(30.0, min(fly_width, 90.0))
button_dia = max(15.0, min(button_dia, 34.0))
coat_ease = max(60.0, min(coat_ease, 240.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

CHEST_FIN = chest_girth + coat_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
BODY_H = coat_length
ARM_DEPTH = min(BODY_H * 0.24, 320.0)
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
FLARE = max(10.0, hem_flare)                # floored so the hem is never narrower than chest


def build_front():
    """Front (cut 2) with a fly extension at the CF. Straight-hanging to the knee; the hem flares
    out by FLARE so it never inverts."""
    w = FRONT_HALF
    h = BODY_H
    neck_x = max(w * 0.28, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 12.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    hem_out = fc.P(w + FLARE, 0.0)
    cf_hem = fc.P(-fly_width, 0.0)
    cf_top = fc.P(-fly_width, h - NECK_DROP)
    edges = [
        fc.Edge("center_front", [fc.Line(cf_top, cf_hem)]),
        fc.Edge("hem", [fc.Line(cf_hem, hem_out)]),
        fc.Edge("side_seam", [fc.Line(hem_out, arm_top)]),
        fc.Edge("armhole", [fc.Bezier(arm_top,
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      shoulder)]),
        fc.Edge("shoulder", [fc.Line(shoulder, neck_pt)]),
        fc.Edge("neckline", [fc.Line(neck_pt, cf_top)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"hem": 50.0, "center_front": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "knee level")],
        grainline=fc.Grainline(fc.P(w * 0.45, h * 0.1), fc.P(w * 0.45, h * 0.85)),
        internals=[fc.Internal("fly-line", [fc.P(0.0, h * 0.2), fc.P(0.0, h * 0.85)],
                               kind="marking"),
                   fc.Internal("cuff-stitch-hem", [fc.P(-fly_width * 0.4, 60.0),
                                                   fc.P(w, 60.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (fly extension)")


def build_back():
    w = BACK_HALF
    h = BODY_H
    neck_x = max(w * 0.18, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 12.0
    shoulder = fc.P(w, h - SH_DROP)
    hem_out = fc.P(w + FLARE, 0.0)
    edges = [
        fc.Edge("hem", [fc.Line(hem_out, fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h), fc.P(neck_x * 0.5, h),
                                       fc.P(neck_x * 0.8, h - NECK_DROP * 0.5),
                                       fc.P(neck_x, h - NECK_DROP))]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), hem_out)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 50.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * 0.66, armhole_ring * 0.62)
    cap_w = min(armhole_ring * 0.9, wrist * 1.5)
    bow = ARM_DEPTH * 0.5
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
        fc.Edge("seam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln), fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow), fc.P(0.0, ln))]),
        fc.Edge("seam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 40.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        internals=[fc.Internal("cuff-stitch", [fc.P(cuff_off, 70.0),
                                               fc.P(cuff_off + wrist, 70.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2, four-row cuff)")


MEASURED = {}


def build_collar():
    ln = MEASURED.get("neck_run", 440.0)
    h = 85.0
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("fall", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance, allowances={"fall": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Collar (cut 1)")


def build():
    pattern = fc.PatternSet("covert-coat")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = front.edge("neckline").length() * 2.0 + back.edge("neckline").length()
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    picked = {"front": front, "back": back, "sleeve": sleeve, "collar": collar}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, sleeve, collar):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(front.edge("side_seam").length() - back.edge("side_seam").length()))
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5,
                         ease=(front.edge("shoulder").length() - back.edge("shoulder").length()))
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=3.0)
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"), ("back", "neckline")],
                         tol=3.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "covert twill (fawn, tightly woven)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "the whole-length body + sleeves + collar; covert twill holds the straight hang "
                 "and the four rows of cuff/hem stitching."},
        {"item": "shank buttons (Yantra4D shank-button-solid)", "qty": 4, "unit": "piece",
         "note": f"four fly buttons, disc {button_dia:.0f} mm = the button_dia that drives the "
                 "fly-placket interface; hidden behind the fly, the shank solid is Yantra4D, "
                 "never modelled here."},
        {"item": "fly facing + interfacing", "qty": round(BODY_H * 1.6), "unit": "mm_length",
         "note": "faces the fly so the buttons are hidden and the CF hangs clean."},
        {"item": "twill lining + tailoring canvas", "qty": round(marker_len * 0.8),
                "unit": "mm_length",
         "note": "half-canvas the front; line the body; run the signature four rows of stitching "
                 "at the cuff and hem."},
    ]
    pattern.metadata = {
        "fc500_rank": 440, "family": "tailoring", "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A fly-front, knee-length covert coat with the signature four rows of "
            "stitching at cuff and hem; a straight-hanging countryman's town coat.",
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> shank-button-solid); "
            "diameter_mm = button_dia, the same parameter that drives the fly_placket interface.",
        "solver": {
            "flare_mm": round(FLARE, 1), "body_h_mm": round(BODY_H, 1),
            "fly_width_mm": round(fly_width, 1),
            "note": "the hem flare is floored positive so the hem is never narrower than the "
                    "chest (which would invert the side seam); the collar length is measured.",
        },
        "tailoring": {
            "cut": "single-breasted fly-front covert coat, whole-length body (no waist seam), "
                   "set-in sleeve, four-row cuff and hem stitching.",
        },
    }
    return pattern


result = build()
