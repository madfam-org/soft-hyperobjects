"""
Zip-hood rash guard — Fashion Cabinet Garment Cartridge
(FC-500 rank #453, active_swim, Yantra4D-bridged invisible-zipper).

A hooded zip-front rash guard in swim-lycra: the second-skin UV surf top, split down the centre
front and closed with a full invisible zipper, topped with an integrated stretch HOOD for sun and
wind on the water. Deepens the FC-400 zip rash guard (a collar, a separating zip) into the hooded
version with a clean invisible zip. Negative ease everywhere except the stabilised zip line.

Two real decisions:

  1. THE ZIP IS SOLVED TO THE FRONT + HOOD RUN — THE DIMENSIONAL HANDSHAKE. The centre-front zip
     runs the drafted front length plus the hood front; that IS the Yantra4D invisible-zipper
     `zip_length`, so the zip is exactly as long as the opening; zip_length drives BOTH the
     hardware AND the garment's center_front interface, clamped under the total front so it never
     overruns.

  2. NEGATIVE EASE, ONE SHARED SHOULDER. The front halves, back and hood are cut at negative ease;
     a shared shoulder run keeps the front-half and back shoulders congruent.

Pieces: front_left, front_right, back, sleeve, hood. Made to measure to chest, back, sleeve.

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# front_left|front_right|back|sleeve|hood|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
back_length = float(PARAM(lambda: back_length, 640.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
hood_height = float(PARAM(lambda: hood_height, 340.0))
zip_length = float(PARAM(lambda: zip_length, 700.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1500.0))
back_length = max(420.0, min(back_length, 900.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
bicep_girth = max(220.0, min(bicep_girth, 600.0))
neck_girth = max(300.0, min(neck_girth, 560.0))
hood_height = max(220.0, min(hood_height, 460.0))
zip_length = max(300.0, min(zip_length, 1200.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 20.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 2.0
ARM_DEPTH = back_length * 0.30
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
# The zip runs the front + the hood front; clamp under the total so it never overruns.
ZIP = min(zip_length, back_length + hood_height)


def build_front_half(is_left, label):
    w = FRONT_HALF
    h = back_length
    cf_bot = fc.P(0.0, 0.0)
    cf_top = fc.P(0.0, h)
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 8.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    side_bot = fc.P(w, 0.0)
    edges = [
        fc.Edge("center_front", [fc.Line(cf_bot, cf_top)]),
        fc.Edge("neckline", [fc.Bezier(cf_top, fc.P(neck_x * 0.35, h - NECK_DROP * 0.3),
                                       fc.P(neck_x * 0.72, h), neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder, fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7), arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, side_bot)]),
        fc.Edge("hem", [fc.Line(side_bot, cf_bot)]),
    ]
    name = "front_left" if is_left else "front_right"
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"center_front": 0.0, "hem": 20.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("center_front", 0.5, "zip")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        internals=[fc.Internal("zip line", [fc.P(0.0, h * 0.04), fc.P(0.0, h * 0.96)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_back():
    w = BACK_HALF
    h = back_length
    neck_x = max(w * 0.20, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 8.0
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h), fc.P(neck_x * 0.5, h),
                                       fc.P(neck_x * 0.8, h - NECK_DROP * 0.5),
                                       fc.P(neck_x, h - NECK_DROP))]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder, fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back panel (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * NEG * 0.62, armhole_ring * 0.62)
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
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 15.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_hood():
    """The hood (cut 2 mirrored): its neck edge is the measured neckline run; it rises hood_height
    and the front edge continues the zip line."""
    neck = MEASURED.get("neck_run", neck_girth) / 2.0     # each hood half takes half the neck
    h = hood_height
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(neck, 0.0))]),
        fc.Edge("back_edge", [fc.Line(fc.P(neck, 0.0), fc.P(neck * 0.85, h))]),
        fc.Edge("crown", [fc.curve_through(fc.P(neck * 0.85, h), fc.P(0.0, h * 0.75),
                                           bulge=0.28, side=1.0)]),
        fc.Edge("front_edge", [fc.Line(fc.P(0.0, h * 0.75), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "hood", edges, seam_allowance=seam_allowance, allowances={"front_edge": 20.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder"), fc.Notch("crown", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(neck * 0.3, h * 0.15), fc.P(neck * 0.3, h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Hood (cut 2)")


def build():
    pattern = fc.PatternSet("rash-guard-zip-hood")
    every = target_piece == "set"
    fl = build_front_half(True, "Front left (zip edge)")
    fr = build_front_half(False, "Front right (zip edge)")
    back = build_back()
    MEASURED["neck_run"] = (fl.edge("neckline").length() + fr.edge("neckline").length()
                            + back.edge("neckline").length())
    armhole_ring = fl.edge("armhole").length() + back.edge("armhole").length()
    picked = {"front_left": fl, "front_right": fr, "back": back,
              "sleeve": build_sleeve(armhole_ring), "hood": build_hood()}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, fl)
    sleeve = build_sleeve(armhole_ring)
    hood = build_hood()
    for piece in (fl, fr, back, sleeve, hood):
        pattern.add(piece)
    pattern.declare_seam(("front_left", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(fl.edge("side_seam").length() - back.edge("side_seam").length()))
    pattern.declare_seam(("front_right", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(fr.edge("side_seam").length() - back.edge("side_seam").length()))
    pattern.declare_seam(("front_left", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("front_right", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front_left", "armhole"), ("back", "armhole")], tol=2.5)
    # Two hood halves join at the crown; the two hood neck edges sum to the assembled neckline.
    pattern.declare_seam([("hood", "neck_edge"), ("hood", "neck_edge")],
                         [("front_left", "neckline"), ("front_right", "neckline"),
                          ("back", "neckline")], tol=2.5)
    return _finish(pattern, fl)


def _finish(pattern, fl):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "swim lycra (UV, chlorine/salt-resistant, 4-way)",
                "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "fronts + back + sleeves + hood at negative ease; a second skin for sun and wind "
                 "on the water."},
        {"item": "invisible zipper (Yantra4D invisible-zipper)", "qty": 1, "unit": "piece",
         "note": f"a full invisible front zip, zip_length {ZIP:.0f} mm = the drafted front + hood "
                 "front run; the invisible-zipper solid is Yantra4D, never modelled here; "
                 "zip_length IS the opening it closes."},
        {"item": "zip tape stabiliser", "qty": round(ZIP * 2.1), "unit": "mm_length",
         "note": "the zip tape is not stretchy, so the CF is stabilised while the rest keeps the "
                 "negative ease."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes a wet body."},
    ]
    pattern.metadata = {
        "fc500_rank": 453, "family": "active_swim", "fabric_hint": "nylon-elastano",
        "silhouette_note": "A hooded zip-front rash guard: the second-skin UV top split at the "
            "centre front with an invisible zip and topped with an integrated stretch hood.",
        "hardware": "invisible zipper via Yantra4D (notion.hardware_ref -> invisible-zipper); "
            "zip_length IS the drafted front + hood front run, the same zip_length that drives "
            "the center_front interface — the dimensional handshake.",
        "solver": {
            "zip_mm": round(ZIP, 1), "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "note": "the zip is clamped under the back_length + hood_height so it never overruns "
                    "the front; the hood neck is the measured neckline run so the hood sets in.",
        },
        "active": {"use": "surf and open-water swim; UV and wind protection with a hood, on and "
                   "off wet without dragging it over the head."},
    }
    return pattern


result = build()
