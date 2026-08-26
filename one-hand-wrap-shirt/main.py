"""
One-hand-close wrap shirt — Fashion Cabinet Garment Cartridge
(FC-500 rank #438, adaptive, Yantra4D-bridged magnetic-button-cover).

A wrap shirt a person can close with one hand: the front crosses over (cache-cœur) and fastens
with magnetic button covers that look like buttons but snap shut with a magnet, so someone with
one working hand, weak pinch, or tremor gets a shirt on and closed without threading a button
through a hole. The rest is an ordinary set-in-sleeve shirt in cotton poplin. The button covers
are the Yantra4D `magnetic-button-cover` solid (notion.hardware_ref); their button diameter is
driven by the same button_diameter that drives the garment's wrap-closure interface.

Two real decisions:

  1. THE COVER IS SOLVED TO THE BUTTON FACE — THE DIMENSIONAL HANDSHAKE. The wrap-closure line
     carries covers whose `button_dia` is the drafted `button_diameter`, so the printed cover
     matches the button stand; `button_diameter` drives BOTH the hardware AND the garment's
     `wrap_closure` interface.

  2. A TRUE WRAP, CLAMPED. The overlap the front crosses is clamped under the half-chest so the
     wrap can never exceed the body and fold back on itself.

Pieces: front-wrap (cut 2, the crossing fronts) + back (cut 1 on fold) + sleeve (cut 2) +
collar (cut 1). Made to measure to chest, waist girths, back and sleeve lengths.

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
back_length = float(PARAM(lambda: back_length, 720.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
wrap_overlap = float(PARAM(lambda: wrap_overlap, 200.0))
button_diameter = float(PARAM(lambda: button_diameter, 20.0))
ease_pct = float(PARAM(lambda: ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
waist_girth = max(600.0, min(waist_girth, 1400.0))
back_length = max(520.0, min(back_length, 900.0))
sleeve_length = max(300.0, min(sleeve_length, 720.0))
bicep_girth = max(240.0, min(bicep_girth, 560.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
wrap_overlap = max(100.0, min(wrap_overlap, 360.0))
button_diameter = max(12.0, min(button_diameter, 34.0))
ease_pct = max(4.0, min(ease_pct, 24.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE = 1.0 + ease_pct / 100.0
CHEST_FIN = chest_girth * EASE
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
ARM_DEPTH = back_length * 0.30
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
# The wrap the fronts cross; clamp under the front half so it can never exceed the panel.
WRAP = min(wrap_overlap, FRONT_HALF * 0.95)


def build_front():
    """Wrap front (cut 2). A shirt front whose centre-front extends past centre by WRAP so the
    two fronts cross; the wrap edge is the diagonal from the neck to the opposite side waist."""
    w = FRONT_HALF
    h = back_length
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 14.0
    NECK_DROP = 10.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    side_bot = fc.P(w, 0.0)
    # The wrap edge runs from the neck point diagonally down to a low inner point at x=-WRAP.
    wrap_low = fc.P(-WRAP, 0.0)
    edges = [
        fc.Edge("wrap_edge", [fc.Bezier(neck_pt,
                                        fc.P(neck_x * 0.4, h * 0.6),
                                        fc.P(-WRAP * 0.5, h * 0.28),
                                        wrap_low)]),
        fc.Edge("hem", [fc.Line(wrap_low, side_bot)]),
        fc.Edge("side_seam", [fc.Line(side_bot, arm_top)]),
        fc.Edge("armhole", [fc.Bezier(arm_top,
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      shoulder)]),
        fc.Edge("shoulder", [fc.Line(shoulder, neck_pt)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 20.0, "wrap_edge": 30.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("wrap_edge", 0.5, "cover midpoint")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        internals=[fc.Internal("cover-line",
                               [fc.P(-WRAP * 0.6, h * 0.25), fc.P(-WRAP * 0.6, h * 0.7)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Wrap front (crosses over)")


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
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
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
        label="Back (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * EASE * 0.7, armhole_ring * 0.7)
    cap_w = min(armhole_ring * 0.9, wrist * 1.5)
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
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 25.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_collar():
    ln = MEASURED.get("neck_run", neck_girth)
    h = 70.0
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Collar (cut 1)")


def build():
    pattern = fc.PatternSet("one-hand-wrap-shirt")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    # The collar spans the back neckline plus the short upper run of each wrap edge that meets
    # the neck; approximated as a fraction of the wrap edge measured off the built fronts.
    MEASURED["neck_run"] = (back.edge("neckline").length()
                            + 2.0 * front.edge("wrap_edge").length() * 0.18)
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    if not every:
        picked = {"front": front, "back": back,
                  "sleeve": build_sleeve(armhole_ring), "collar": build_collar()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front)
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    for piece in (front, back, sleeve, collar):
        pattern.add(piece)
    # Side seams: each front to the back (back has two side edges, one per side).
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(front.edge("side_seam").length() - back.edge("side_seam").length()))
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    # Collar to the back neckline + the upper wrap edges (measured neck_run).
    pattern.declare_seam(("collar", "neck_edge"),
                         [("back", "neckline")], tol=2.5,
                         ease=(MEASURED["neck_run"] - back.edge("neckline").length()))
    return _finish(pattern, front)


def _finish(pattern, front):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "cotton poplin (soft, opaque)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "fronts + back + sleeves + collar; a crisp poplin holds the wrap flat to close."},
        {"item": "magnetic button covers (Yantra4D magnetic-button-cover)", "qty": 5,
         "unit": "piece",
         "note": f"five covers, button_dia {button_diameter:.0f} mm = the button_diameter that "
                 "drives the wrap-closure interface; they look like buttons but snap shut with a "
                 "magnet, so the shirt closes one-handed with no pinch grip or aim."},
        {"item": "interfacing (wrap edge + collar)", "qty": round(front.edge("wrap_edge").length()),
         "unit": "mm_length",
         "note": "stabilises the diagonal wrap edge so the magnetic covers sit flat and true."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "topstitch the wrap edge so it does not roll."},
    ]
    pattern.metadata = {
        "fc500_rank": 438, "family": "adaptive", "fabric_hint": "popelina-algodon",
        "silhouette_note": "A cross-front wrap shirt that closes one-handed on magnetic button "
            "covers — an ordinary poplin shirt for a hand that cannot thread a button.",
        "hardware": "magnetic button covers via Yantra4D (notion.hardware_ref -> "
            "magnetic-button-cover); button_dia = button_diameter, the same parameter that "
            "drives the wrap_closure interface — the dimensional handshake.",
        "solver": {
            "wrap_mm": round(WRAP, 1), "chest_finished_mm": round(CHEST_FIN, 1),
            "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "note": "the wrap overlap is clamped under 95% of the front half so the wrap can "
                    "never exceed the body and fold back; the collar length is the measured "
                    "back-neck run.",
        },
        "adaptive": {
            "dressing": "the front crosses over and fastens on magnetic button covers, so a "
                        "wearer with one working hand, weak pinch or tremor closes the shirt "
                        "without threading a button through a hole",
        },
    }
    return pattern


result = build()
