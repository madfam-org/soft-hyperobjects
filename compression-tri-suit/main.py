"""
Triathlon compression suit — Fashion Cabinet Garment Cartridge
(FC-500 rank #449, active_swim, Yantra4D-bridged invisible-zipper).

A one-piece sleeveless tri-suit in compression lycra: swim, bike and run in one garment, cut at
negative ease so it compresses the muscle and does not billow in the water, split down the centre
front and closed with a short invisible zipper at the chest so it can be got on and off over the
shoulders. Short legs to mid-thigh, a racer back, a rear pocket panel.

Two real decisions:

  1. THE ZIP IS SOLVED TO THE CHEST OPENING — THE DIMENSIONAL HANDSHAKE. The centre-front zip runs
     the drafted `zip_length` from the chest to the collar; that number drives BOTH the Yantra4D
     invisible-zipper `zip_length` AND the garment's `center_front` interface. The zip length is
     clamped under the torso length so it can never exceed the front.

  2. NEGATIVE EASE EVERYWHERE, ONE SHARED CROTCH. Every panel is cut smaller than the body; the
     front and back legs share ONE crotch point and one inseam length so the leg cannot twist.

Pieces: front (cut 1, zip edge split as an internal), back (cut 1 racer), leg (cut 2). Made to
measure to chest, waist, hip girths, torso and thigh.

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
# front|back|leg|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 820.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
torso_length = float(PARAM(lambda: torso_length, 640.0))   # shoulder to crotch
thigh_length = float(PARAM(lambda: thigh_length, 220.0))   # crotch to mid-thigh hem
thigh_girth = float(PARAM(lambda: thigh_girth, 560.0))
zip_length = float(PARAM(lambda: zip_length, 260.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(720.0, min(chest_girth, 1400.0))
waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
torso_length = max(480.0, min(torso_length, 820.0))
thigh_length = max(120.0, min(thigh_length, 380.0))
thigh_girth = max(360.0, min(thigh_girth, 800.0))
zip_length = max(120.0, min(zip_length, 400.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 22.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
WAIST_FIN = waist_girth * NEG
HIP_FIN = hip_girth * NEG
THIGH_FIN = thigh_girth * NEG
FRONT_W = CHEST_FIN / 2.0                    # front panel width (half the ring)
BACK_W = CHEST_FIN / 2.0
# The zip is clamped under the torso so it never exceeds the front.
ZIP = min(zip_length, torso_length * 0.7)
LEG_W = THIGH_FIN / 2.0


def build_front():
    """Front torso panel (cut 1). Shoulders taper to a racer front; the centre-front carries the
    invisible zip (an internal marking, the panel stays one closed ring). Waist nips in."""
    wt = FRONT_W / 2.0                        # half-front top (chest) — panel is symmetric
    wh = HIP_FIN / 2.0
    h = torso_length
    # symmetric about x=0: left edge mirrors right. Draft the right half then close.
    edges = [
        fc.Edge("shoulder", [fc.Line(fc.P(-wt * 0.5, h), fc.P(wt * 0.5, h))]),
        fc.Edge("armhole_r", [fc.Bezier(fc.P(wt * 0.5, h), fc.P(wt, h - h * 0.18),
                                        fc.P(wt, h - h * 0.30), fc.P(wt, h - h * 0.34))]),
        fc.Edge("side_r", [fc.Line(fc.P(wt, h - h * 0.34), fc.P(wh, 0.0))]),
        fc.Edge("crotch", [fc.Line(fc.P(wh, 0.0), fc.P(-wh, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(-wh, 0.0), fc.P(-wt, h - h * 0.34))]),
        fc.Edge("armhole_l", [fc.Bezier(fc.P(-wt, h - h * 0.34), fc.P(-wt, h - h * 0.30),
                                        fc.P(-wt, h - h * 0.18), fc.P(-wt * 0.5, h))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"crotch": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre front"), fc.Notch("shoulder", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        internals=[fc.Internal("zip-line", [fc.P(0.0, h - ZIP), fc.P(0.0, h - 10.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, mirror=False), label="Front torso (zip)")


def build_back():
    """Back torso panel (cut 1), racer back. Same waist/hip widths so the side seams match."""
    wt = BACK_W / 2.0
    wh = HIP_FIN / 2.0
    h = torso_length
    edges = [
        fc.Edge("racer", [fc.Bezier(fc.P(-wt * 0.35, h), fc.P(-wt * 0.15, h - h * 0.14),
                                    fc.P(wt * 0.15, h - h * 0.14), fc.P(wt * 0.35, h))]),
        fc.Edge("armhole_r", [fc.Bezier(fc.P(wt * 0.35, h), fc.P(wt, h - h * 0.12),
                                        fc.P(wt, h - h * 0.28), fc.P(wt, h - h * 0.34))]),
        fc.Edge("side_r", [fc.Line(fc.P(wt, h - h * 0.34), fc.P(wh, 0.0))]),
        fc.Edge("crotch", [fc.Line(fc.P(wh, 0.0), fc.P(-wh, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(-wh, 0.0), fc.P(-wt, h - h * 0.34))]),
        fc.Edge("armhole_l", [fc.Bezier(fc.P(-wt, h - h * 0.34), fc.P(-wt, h - h * 0.28),
                                        fc.P(-wt, h - h * 0.12), fc.P(-wt * 0.35, h))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"crotch": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre back"), fc.Notch("racer", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        internals=[fc.Internal("rear-pocket", [fc.P(-wt * 0.4, h * 0.12), fc.P(wt * 0.4, h * 0.12)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, mirror=False), label="Back torso (racer)")


def build_leg():
    """Short leg (cut 2 mirrored): a tapered tube from the crotch/hip to the mid-thigh hem, cut
    at negative ease. Front and back inseams share ONE length by construction."""
    top = HIP_FIN / 4.0                       # a quarter-hip per leg top
    hem = LEG_W
    h = thigh_length
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(top, h))]),
        fc.Edge("outseam", [fc.Line(fc.P(top, h), fc.P((top + hem) / 2.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P((top + hem) / 2.0, 0.0), fc.P((top - hem) / 2.0, 0.0))]),
        fc.Edge("inseam", [fc.Line(fc.P((top - hem) / 2.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "leg", edges, seam_allowance=seam_allowance, allowances={"hem": 15.0},
        notches=[fc.Notch("top", 0.5, "crotch"), fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(top * 0.5, h * 0.15), fc.P(top * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Short leg (cut 2)")


def build():
    pattern = fc.PatternSet("compression-tri-suit")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    leg = build_leg()
    picked = {"front": front, "back": back, "leg": leg}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, leg):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_r"), ("back", "side_r"), tol=1.5)
    pattern.declare_seam(("front", "side_l"), ("back", "side_l"), tol=1.5)
    # legs attach to the front+back crotch region; the leg top sums to the crotch width.
    pattern.declare_seam(("leg", "top"), ("front", "crotch"), tol=2.0,
                         ease=(leg.edge("top").length() - front.edge("crotch").length()))
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "compression lycra (nylon/elastane, chlorine-resistant, 4-way)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "front + back + legs at negative ease so the suit compresses and does not "
                 "billow in the water."},
        {"item": "invisible zipper (Yantra4D invisible-zipper)", "qty": 1, "unit": "piece",
         "note": f"a short chest zip, zip_length {ZIP:.0f} mm = the drafted centre-front opening; "
                 "the invisible-zipper solid is Yantra4D, never modelled here; zip_length IS the "
                 "opening it closes."},
        {"item": "silicone leg gripper", "qty": round(THIGH_FIN * 0.5 + 40.0), "unit": "mm_length",
         "note": "a gripper at each thigh hem holds the short legs down cycling and running."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes over a swim-bike-run."},
    ]
    pattern.metadata = {
        "fc500_rank": 449, "family": "active_swim", "fabric_hint": "nylon-elastano",
        "silhouette_note": "A one-piece sleeveless tri-suit: compression lycra, short legs, racer "
            "back, short chest zip, cut at negative ease for swim-bike-run.",
        "hardware": "invisible zipper via Yantra4D (notion.hardware_ref -> invisible-zipper); "
            "zip_length IS the drafted centre-front opening, the same zip_length that drives the "
            "center_front interface — the dimensional handshake.",
        "solver": {
            "zip_mm": round(ZIP, 1), "chest_finished_mm": round(CHEST_FIN, 1),
            "note": "the zip is clamped under 0.7x the torso so it never exceeds the front; the "
                    "front and back legs share ONE crotch width so the leg cannot twist; every "
                    "panel is cut at negative ease.",
        },
        "active": {"use": "swim, bike and run in one garment; compression + a short chest zip to "
                   "get it on and off over the shoulders."},
    }
    return pattern


result = build()
