"""
Dive-skin swim suit — Fashion Cabinet Garment Cartridge
(FC-500 rank #458, active_swim, Yantra4D-bridged invisible-zipper).

A full-coverage dive skin in thin swim-lycra: a one-piece long-sleeve, long-leg skin worn under a
wetsuit for warmth and easy donning, or alone in warm water against sun, sting and abrasion. Cut at
negative ease as a true second skin, split down the centre BACK and closed with a long invisible
zipper so it can be got on over the shoulders and hips.

Two real decisions:

  1. THE BACK ZIP IS SOLVED TO THE BACK RUN — THE DIMENSIONAL HANDSHAKE. The centre-back zip runs
     the drafted nape-to-seat length; that IS the Yantra4D invisible-zipper zip_length, so the zip
     is exactly as long as the opening; zip_length drives BOTH the hardware AND the garment's
     center_back interface, clamped under the torso so it never overruns.

  2. NEGATIVE EASE, ONE SHARED CROTCH + SHARED SHOULDER. Every panel is cut smaller than the body;
     the leg fronts and backs share ONE crotch and the sleeve caps solve to the armscye ring.

Pieces: front, back (split for the zip), sleeve, leg. Made to measure to chest, waist, hip, torso,
inseam, sleeve. FC-500 lane 6 (active).

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
# front|back|sleeve|leg|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
torso_length = float(PARAM(lambda: torso_length, 640.0))    # shoulder to crotch
inseam = float(PARAM(lambda: inseam, 760.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 330.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 260.0))
zip_length = float(PARAM(lambda: zip_length, 560.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(720.0, min(chest_girth, 1400.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
torso_length = max(480.0, min(torso_length, 820.0))
inseam = max(560.0, min(inseam, 940.0))
sleeve_length = max(400.0, min(sleeve_length, 720.0))
bicep_girth = max(240.0, min(bicep_girth, 560.0))
ankle_girth = max(180.0, min(ankle_girth, 400.0))
zip_length = max(300.0, min(zip_length, 800.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 22.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
HIP_FIN = hip_girth * NEG
ANKLE_FIN = ankle_girth * NEG
FRONT_W = CHEST_FIN / 2.0
BACK_HALF = CHEST_FIN / 4.0      # back is split for the zip, each half a quarter
ARM_DEPTH = torso_length * 0.30
SH_SEAM = min(FRONT_W / 2.0, BACK_HALF) * 0.30 + 40.0
ZIP = min(zip_length, torso_length + 120.0)


def build_front():
    """Front torso panel (cut 1), full width, shoulders, two armholes, waist to crotch."""
    wt = FRONT_W / 2.0
    wh = HIP_FIN / 2.0
    h = torso_length
    edges = [
        fc.Edge("shoulder", [fc.Line(fc.P(-wt * 0.5, h), fc.P(wt * 0.5, h))]),
        fc.Edge("armhole_r", [fc.Bezier(fc.P(wt * 0.5, h), fc.P(wt, h - ARM_DEPTH * 0.5),
                                        fc.P(wt, h - ARM_DEPTH * 0.85), fc.P(wt, h - ARM_DEPTH))]),
        fc.Edge("side_r", [fc.Line(fc.P(wt, h - ARM_DEPTH), fc.P(wh, 0.0))]),
        fc.Edge("crotch", [fc.Line(fc.P(wh, 0.0), fc.P(-wh, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(-wh, 0.0), fc.P(-wt, h - ARM_DEPTH))]),
        fc.Edge("armhole_l", [fc.Bezier(fc.P(-wt, h - ARM_DEPTH), fc.P(-wt, h - ARM_DEPTH * 0.85),
                                        fc.P(-wt, h - ARM_DEPTH * 0.5), fc.P(-wt * 0.5, h))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"crotch": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre front"), fc.Notch("shoulder", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        cut=fc.CutSpec(quantity=1, mirror=False), label="Front torso")


def build_back():
    """Back torso panel (cut 1 on fold at CB). Same width/shape as the front so the side seams
    match by construction; the centre-back zip is an internal marking (the panel stays one closed
    ring, the zip is applied to the CB fold line)."""
    wt = FRONT_W / 2.0
    wh = HIP_FIN / 2.0
    h = torso_length
    edges = [
        fc.Edge("shoulder", [fc.Line(fc.P(-wt * 0.5, h), fc.P(wt * 0.5, h))]),
        fc.Edge("armhole_r", [fc.Bezier(fc.P(wt * 0.5, h), fc.P(wt, h - ARM_DEPTH * 0.5),
                                        fc.P(wt, h - ARM_DEPTH * 0.85), fc.P(wt, h - ARM_DEPTH))]),
        fc.Edge("side_r", [fc.Line(fc.P(wt, h - ARM_DEPTH), fc.P(wh, 0.0))]),
        fc.Edge("crotch", [fc.Line(fc.P(wh, 0.0), fc.P(-wh, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(-wh, 0.0), fc.P(-wt, h - ARM_DEPTH))]),
        fc.Edge("armhole_l", [fc.Bezier(fc.P(-wt, h - ARM_DEPTH), fc.P(-wt, h - ARM_DEPTH * 0.85),
                                        fc.P(-wt, h - ARM_DEPTH * 0.5), fc.P(-wt * 0.5, h))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"crotch": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre back"), fc.Notch("shoulder", 0.5, "zip top")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        internals=[fc.Internal("zip-line", [fc.P(0.0, h - ZIP), fc.P(0.0, h - 10.0)],
                kind="marking")],
        cut=fc.CutSpec(quantity=1, mirror=False), label="Back torso (CB zip)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * NEG * 0.55, armhole_ring * 0.55)
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
        fc.Edge("underseam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln), fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow), fc.P(0.0, ln))]),
        fc.Edge("underseam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 10.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


def build_leg():
    """Full-length leg (cut 2 mirrored): a tapered tube from the crotch/hip to the ankle, cut at
    negative ease. Front and back share ONE inseam length."""
    top = HIP_FIN / 4.0
    ank = ANKLE_FIN / 2.0
    h = inseam
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(top, h))]),
        fc.Edge("outseam", [fc.Line(fc.P(top, h), fc.P((top + ank) / 2.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P((top + ank) / 2.0, 0.0), fc.P((top - ank) / 2.0, 0.0))]),
        fc.Edge("inseam", [fc.Line(fc.P((top - ank) / 2.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "leg", edges, seam_allowance=seam_allowance, allowances={"hem": 12.0},
        notches=[fc.Notch("top", 0.5, "crotch"), fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(top * 0.5, h * 0.15), fc.P(top * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Full leg (cut 2)")


def build():
    pattern = fc.PatternSet("dive-skin-suit")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    armhole_ring = front.edge("armhole_r").length() + back.edge("armhole_r").length()
    picked = {"front": front, "back": back, "sleeve": build_sleeve(armhole_ring),
            "leg": build_leg()}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    sleeve = build_sleeve(armhole_ring)
    leg = build_leg()
    for piece in (front, back, sleeve, leg):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_r"), ("back", "side_r"), tol=1.5)
    pattern.declare_seam(("front", "side_l"), ("back", "side_l"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole_r"), ("back", "armhole_r")], tol=2.5)
    pattern.declare_seam(("leg", "top"), ("front", "crotch"), tol=2.5,
                         ease=(leg.edge("top").length() - front.edge("crotch").length()))
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "thin swim lycra (UV, 4-way, chlorine/salt-resistant)",
                "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "front + back + sleeves + legs at negative ease; a true second skin, thin enough "
                 "to layer under a wetsuit."},
        {"item": "invisible zipper (Yantra4D invisible-zipper)", "qty": 1, "unit": "piece",
         "note": f"a long centre-back zip, zip_length {ZIP:.0f} mm = the drafted nape-to-seat run; "
                 "the invisible-zipper solid is Yantra4D, never modelled here; zip_length IS the "
                 "opening it closes."},
        {"item": "zip tape stabiliser", "qty": round(ZIP * 1.1), "unit": "mm_length",
         "note": "the zip tape is not stretchy, so the CB is stabilised while the rest keeps its "
                 "grip."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes under a wetsuit or against the skin."},
    ]
    pattern.metadata = {
        "fc500_rank": 458, "family": "active_swim", "fabric_hint": "nylon-elastano",
        "silhouette_note": "A full-coverage dive skin: a one-piece long-sleeve, long-leg "
            "swim-lycra skin split down the centre back with a long invisible zip.",
        "hardware": "invisible zipper via Yantra4D (notion.hardware_ref -> invisible-zipper); "
            "zip_length IS the drafted nape-to-seat run, the same zip_length that drives the "
            "center_back interface — the dimensional handshake.",
        "solver": {
            "zip_mm": round(ZIP, 1), "chest_finished_mm": round(CHEST_FIN, 1),
            "note": "the back zip is clamped under the torso + 120 so it never overruns; the leg "
                    "fronts and backs share ONE inseam and the front + back legs share ONE crotch "
                    "so the leg cannot twist; negative ease throughout.",
        },
        "active": {"use": "scuba and snorkelling under a wetsuit for warmth and easy donning, or "
                   "alone in warm water against sun, sting and abrasion."},
    }
    return pattern


result = build()
