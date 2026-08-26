"""
Packable running windbreaker — Fashion Cabinet Garment Cartridge
(FC-500 rank #455, active_swim, Yantra4D-bridged cord-lock).

A featherweight ripstop running windbreaker that packs into its own chest pocket: a full-zip
shell with a drawcord hem and hood, cut with POSITIVE ease so it layers over a running top, and
so light it stuffs into a pocket the size of a fist. The drawcords cinch on cord-locks at the hem
and hood so the wind does not get under it on a descent.

Two real decisions:

  1. THE HEM DRAWCORD CHANNEL IS SOLVED TO THE HEM. The channel runs the full hem; its cord runs
     the hem plus a cord-lock tail, and the cord-lock is the Yantra4D solid whose cord diameter is
     driven by the garment's drawcord parameter — the hem cinch interface.

  2. POSITIVE EASE, PACK POCKET CLAMPED. The shell is cut with positive ease to layer; the packable
     pocket is clamped under the front so the whole jacket can invert into it.

Pieces: front (cut 2, zip + pocket), back (cut 1), sleeve (cut 2), hood (cut 2). Made to measure
to chest, back, sleeve, neck. FC-500 lane 6 (active).

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
# front|back|sleeve|hood|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
back_length = float(PARAM(lambda: back_length, 680.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 360.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
hood_height = float(PARAM(lambda: hood_height, 320.0))
drawcord_dia = float(PARAM(lambda: drawcord_dia, 4.0))
shell_ease = float(PARAM(lambda: shell_ease, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
back_length = max(520.0, min(back_length, 860.0))
sleeve_length = max(420.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 560.0))
neck_girth = max(320.0, min(neck_girth, 560.0))
hood_height = max(220.0, min(hood_height, 440.0))
drawcord_dia = max(2.0, min(drawcord_dia, 8.0))
shell_ease = max(80.0, min(shell_ease, 320.0))
seam_allowance = max(6.0, min(seam_allowance, 14.0))

CHEST_FIN = chest_girth + shell_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 2.0
ARM_DEPTH = back_length * 0.30
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0


def build_front():
    w = FRONT_HALF
    h = back_length
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 14.0
    NECK_DROP = 10.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    edges = [
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h - NECK_DROP), fc.P(neck_x * 0.35, h - NECK_DROP),
                                       fc.P(neck_x * 0.72, h - NECK_DROP * 0.4), neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder, fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7), arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"hem": 25.0, "center_front": 25.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("center_front", 0.5, "zip")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        internals=[fc.Internal("hem-drawcord", [fc.P(0.0, 15.0), fc.P(w, 15.0)], kind="marking"),
                   fc.Internal("pack-pocket", [fc.P(w * 0.2, h * 0.45),
                                               fc.P(w * 0.2, h * 0.45 + min(160.0, h * 0.3))],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (zip + pack pocket)")


def build_back():
    w = BACK_HALF
    h = back_length
    neck_x = max(w * 0.20, w - SH_SEAM)
    SH_DROP = 14.0
    NECK_DROP = 10.0
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
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 25.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * 0.85, armhole_ring * 0.72)
    cap_w = min(armhole_ring * 0.9, wrist * 1.4)
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
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 20.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_hood():
    neck = MEASURED.get("neck_run", neck_girth) / 2.0
    h = hood_height
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(neck, 0.0))]),
        fc.Edge("back_edge", [fc.Line(fc.P(neck, 0.0), fc.P(neck * 0.85, h))]),
        fc.Edge("crown", [fc.curve_through(fc.P(neck * 0.85, h), fc.P(0.0, h * 0.72),
                                           bulge=0.26, side=1.0)]),
        fc.Edge("front_edge", [fc.Line(fc.P(0.0, h * 0.72), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "hood", edges, seam_allowance=seam_allowance, allowances={"front_edge": 20.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder")],
        grainline=fc.Grainline(fc.P(neck * 0.3, h * 0.15), fc.P(neck * 0.3, h * 0.65)),
        internals=[fc.Internal("hood-drawcord", [fc.P(0.0, h * 0.1), fc.P(0.0, h * 0.62)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Hood (cut 2, drawcord)")


def build():
    pattern = fc.PatternSet("windbreaker-packable")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = 2.0 * front.edge("neckline").length() + back.edge("neckline").length()
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    picked = {"front": front, "back": back, "sleeve": build_sleeve(armhole_ring),
              "hood": build_hood()}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    sleeve = build_sleeve(armhole_ring)
    hood = build_hood()
    for piece in (front, back, sleeve, hood):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    pattern.declare_seam([("hood", "neck_edge"), ("hood", "neck_edge")],
                         [("front", "neckline"), ("front", "neckline"), ("back", "neckline")],
                         tol=2.5)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "featherweight ripstop nylon (DWR)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a 15-denier DWR ripstop so the whole jacket packs into its own chest pocket the "
                 "size of a fist; positive ease to layer over a running top."},
        {"item": "cord-locks (Yantra4D cord-lock)", "qty": 3, "unit": "piece",
         "note": f"hem and hood cord-locks, cord {drawcord_dia:.0f} mm = the drawcord_dia that "
                 "drives the hem-cinch interface; the cord-lock solid is Yantra4D, never modelled "
                 "here."},
        {"item": "drawcord + zip", "qty": round(back_length * 2.5 + neck_girth),
                "unit": "mm_length",
         "note": "the hem and hood drawcords plus a lightweight full-length front zip."},
        {"item": "flat thread", "qty": 1, "unit": "spool",
         "note": "flat-fell or bind the seams so the shell packs small and sheds wind."},
    ]
    pattern.metadata = {
        "fc500_rank": 455, "family": "active_swim", "fabric_hint": "nylon-ripstop",
        "silhouette_note": "A featherweight full-zip running windbreaker with a drawcord hem and "
            "hood, packing into its own chest pocket.",
        "hardware": "cord-locks via Yantra4D (notion.hardware_ref -> cord-lock); cord_dia = "
            "drawcord_dia, the parameter that drives the hem-cinch interface.",
        "solver": {
            "chest_finished_mm": round(CHEST_FIN,
                    1), "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "note": "the shell is cut with positive ease to layer; the pack pocket is clamped "
                    "under the front so the whole jacket can invert into it; the hood neck is the "
                    "measured neckline run.",
        },
        "active": {"use": "trail and road running in wind and light rain; cinches at hem and hood "
                   "on a descent and packs to fist size when the sun comes out."},
    }
    return pattern


result = build()
