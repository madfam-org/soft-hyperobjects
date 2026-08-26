"""
Morning coat — Fashion Cabinet Garment Cartridge
(FC-500 rank #439, tailoring, T4, made-to-measure; y4d shank-button-solid).

Formal daywear, the descendant of the riding coat: below the single fastening button the
centre-front edge SWEEPS AWAY in a continuous cutaway curve to the side seam, and the coat
continues behind as long tails. The cutaway curve IS the garment — it changes which edges exist
and where the button sits relative to the sweep. Distinct from a tailcoat's square-cut fronts:
the morning coat's front is one continuous curve from the button break to the tail.

Three things solved by measurement, not sketched:

  1. THE CUTAWAY IS A CLAMPED SPAN. The sweep runs from the fastening point down and back to
     the side; its horizontal run and vertical drop are both FLOORED, because at parameter
     extremes the derived span goes to zero or negative and a negative span does not fail — it
     inverts the front into geometry the kernel's CCW normalization launders into a valid-looking
     outline. Both are clamped positive so the front is always a real cutaway.

  2. THE TAIL IS A SEPARATE WAIST-SEAMED SKIRT on its own grain, drafted to the measured back
     waist so the waist seam closes.

  3. THE SHANK BUTTON is Yantra4D territory (shank-button-solid; notion.hardware_ref); its disc
     diameter is the drafted button_dia that drives the garment's button-stand interface.

Pieces: front (cutaway), back, tail, sleeve (two-piece: upper + under), collar. Made to measure.

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
# front|back|tail|upper_sleeve|under_sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
back_length = float(PARAM(lambda: back_length, 440.0))     # nape to waist
tail_length = float(PARAM(lambda: tail_length, 400.0))     # waist to tail hem
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
button_rise = float(PARAM(lambda: button_rise, 40.0))      # button above the waist
cutaway_sweep = float(PARAM(lambda: cutaway_sweep, 180.0))  # horizontal run of the cutaway
button_dia = float(PARAM(lambda: button_dia, 23.0))
lapel_width = float(PARAM(lambda: lapel_width, 90.0))
coat_ease = float(PARAM(lambda: coat_ease, 100.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1400.0))
waist_girth = max(640.0, min(waist_girth, 1300.0))
back_length = max(360.0, min(back_length, 520.0))
tail_length = max(280.0, min(tail_length, 560.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 520.0))
button_rise = max(0.0, min(button_rise, 120.0))
cutaway_sweep = max(60.0, min(cutaway_sweep, 320.0))
button_dia = max(15.0, min(button_dia, 34.0))
lapel_width = max(50.0, min(lapel_width, 140.0))
coat_ease = max(40.0, min(coat_ease, 200.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

CHEST_FIN = chest_girth + coat_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
ARM_DEPTH = back_length * 0.62
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
WAIST_Y = 0.0                              # waist line at y=0 for the body block
BODY_TOP = back_length                     # nape/shoulder line
# The cutaway span: from the button break (at the CF, y = button_rise) sweeping to the side
# at the waist. Both run and the effective drop are floored positive.
SWEEP_RUN = max(40.0, min(cutaway_sweep, FRONT_HALF * 0.9))
BUTTON_Y = max(10.0, min(button_rise + 20.0, BODY_TOP * 0.5))


def build_front():
    """Cutaway front (cut 2). CF rises from the button break; below the button the edge sweeps
    away to the side at the waist. Upper front is a normal shoulder/armhole/lapel block."""
    w = FRONT_HALF
    h = BODY_TOP
    neck_x = max(w * 0.28, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 12.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    side_waist = fc.P(w, WAIST_Y)
    button_pt = fc.P(0.0, BUTTON_Y)
    # cutaway sweep: from the button point at the CF, curve back to the side waist.
    cf_top = fc.P(0.0, h - NECK_DROP - lapel_width * 0.2)   # lapel break at CF top
    edges = [
        fc.Edge("lapel_cf", [fc.Line(cf_top, button_pt)]),
        fc.Edge("cutaway", [fc.Bezier(button_pt,
                                      fc.P(SWEEP_RUN * 0.5, BUTTON_Y * 0.5),
                                      fc.P(w - SWEEP_RUN * 0.5, WAIST_Y + 8.0),
                                      side_waist)]),
        fc.Edge("side_seam", [fc.Line(side_waist, arm_top)]),
        fc.Edge("armhole", [fc.Bezier(arm_top,
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      shoulder)]),
        fc.Edge("shoulder", [fc.Line(shoulder, neck_pt)]),
        fc.Edge("lapel", [fc.Line(neck_pt, cf_top)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"cutaway": 15.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("lapel_cf", 0.5, "button")],
        grainline=fc.Grainline(fc.P(w * 0.45, h * 0.15), fc.P(w * 0.45, h * 0.8)),
        internals=[fc.Internal("button-stand",
                               [button_pt, fc.P(0.0, BUTTON_Y + button_dia)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Cutaway front")


def build_back():
    """Coat back to the waist (cut 1 on fold)."""
    w = BACK_HALF
    h = BODY_TOP
    neck_x = max(w * 0.18, w - SH_SEAM)
    SH_DROP = 16.0
    NECK_DROP = 12.0
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(w, WAIST_Y), fc.P(0.0, WAIST_Y))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h), fc.P(neck_x * 0.5, h),
                                       fc.P(neck_x * 0.8, h - NECK_DROP * 0.5),
                                       fc.P(neck_x, h - NECK_DROP))]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, WAIST_Y))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("waist", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold)")


def build_tail(back_waist_len):
    """The tail skirt (cut 1 on fold): top = the measured back waist; hangs tail_length. A
    centre-back vent splits it, drawn as a marking."""
    top = back_waist_len
    hem = top * 1.08
    h = tail_length
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, h), fc.P(top, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(top, h), fc.P(hem, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hem, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "tail", edges, seam_allowance=seam_allowance, allowances={"hem": 40.0, "center_back": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(top * 0.4, h * 0.2), fc.P(top * 0.4, h * 0.8)),
        internals=[fc.Internal("vent", [fc.P(0.0, 0.0), fc.P(0.0, h * 0.4)], kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Tail skirt (cut 1 on fold)")


def build_sleeve(armhole_ring):
    """A set-in sleeve (cut 2) whose cap is SOLVED to the armscye ring by iterating the cap
    width and bow, tapering to a tailored cuff. Drafted flat, symmetric."""
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
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_collar():
    ln = MEASURED.get("neck_run", 420.0)
    h = 80.0
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
    pattern = fc.PatternSet("morning-coat-tailcoat")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    back_waist = back.edge("waist").length()
    MEASURED["back_waist"] = back_waist
    MEASURED["neck_run"] = back.edge("neckline").length() * 2.0 + 40.0
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    tail = build_tail(back_waist)
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    picked = {"front": front, "back": back, "tail": tail, "sleeve": sleeve, "collar": collar}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, tail, sleeve, collar):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(front.edge("side_seam").length() - back.edge("side_seam").length()))
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5,
                         ease=(front.edge("shoulder").length() - back.edge("shoulder").length()))
    # tail waist to back waist.
    pattern.declare_seam(("tail", "waist"), ("back", "waist"), tol=2.0)
    # sleeve cap solved to the armscye ring (front + back armhole).
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=3.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "worsted wool coating", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "the cutaway front + back + tail + two-piece sleeves + collar; a firm worsted "
                 "holds the cutaway and the tail's hang."},
        {"item": "shank button (Yantra4D shank-button-solid)", "qty": 1, "unit": "piece",
         "note": f"the single fastening button at the waist break, disc {button_dia:.0f} mm = the "
                 "button_dia that drives the button-stand interface; the shank solid is Yantra4D, "
                 "never modelled here."},
        {"item": "canvas + lapel interfacing", "qty": round(area / 1500.0), "unit": "mm_length",
         "note": "hair canvas through the front + lapel so the cutaway rolls and holds."},
        {"item": "silk facing + lining", "qty": round(marker_len * 0.8), "unit": "mm_length",
         "note": "faced lapel and full lining; edge-stitch the cutaway and the tail."},
    ]
    pattern.metadata = {
        "fc500_rank": 439, "family": "tailoring", "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "A morning coat: below the single button the front sweeps away in a "
            "continuous cutaway to the side, and the coat continues as a long tail skirt.",
        "hardware": "shank button via Yantra4D (notion.hardware_ref -> shank-button-solid); "
            "diameter_mm = button_dia, the same parameter that drives the button_stand interface.",
        "solver": {
            "sweep_run_mm": round(SWEEP_RUN, 1), "button_y_mm": round(BUTTON_Y, 1),
            "back_waist_mm": round(MEASURED.get("back_waist", 0.0), 1),
            "note": "the cutaway run and the button height are both floored positive so a "
                    "negative span can never invert the front; the tail top is the measured "
                    "back waist so the waist seam closes.",
        },
        "tailoring": {
            "cut": "single-breasted cutaway morning coat, waist-seamed tail, two-piece sleeve, "
                   "faced peak lapel; formal daywear.",
        },
    }
    return pattern


result = build()
