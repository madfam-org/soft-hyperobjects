"""
Soft-finger dressing mitt — Fashion Cabinet Garment Cartridge
(FC-500 rank #433, adaptive / soft-exo, Yantra4D-bridged soft-finger).

A dressing mitt for a hand with limited grip: a neoprene mitt (all four fingers in one pocket,
thumb separate) whose palmar side carries a single soft-finger actuator that curls to pinch a
zip-pull, a button hook or a sock edge against the palm. The mitt is the soft body; the
soft-finger actuator is the Yantra4D `soft-finger` solid, never modelled here.

Two real decisions:

  1. THE ACTUATOR POCKET IS SOLVED TO THE FINGER LENGTH — THE DIMENSIONAL HANDSHAKE. The palmar
     pocket runs the drafted `finger_len` from the palm base to the finger tip; that is the same
     number that drives the Yantra4D `soft-finger` `finger_len`, so the printed curling finger
     is exactly as long as the pocket that holds it. `finger_len` drives BOTH the hardware AND
     the garment's `actuator_pocket` interface.

  2. A ROUNDED MITT, NEVER A DEGENERATE POINT. The mitt top is a rounded dome whose depth is
     clamped so the top can never collapse to a point (which would degenerate the panel).

Pieces: palm (with the actuator pocket), back, thumb, cuff. Made to measure to hand length,
palm girth, finger length and wrist girth.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # palm|back|thumb|cuff|set

hand_length = float(PARAM(lambda: hand_length, 195.0))
palm_girth = float(PARAM(lambda: palm_girth, 215.0))
finger_len = float(PARAM(lambda: finger_len, 85.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 175.0))
cuff_height = float(PARAM(lambda: cuff_height, 65.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hand_length = max(140.0, min(hand_length, 240.0))
palm_girth = max(150.0, min(palm_girth, 290.0))
finger_len = max(50.0, min(finger_len, 115.0))
wrist_girth = max(130.0, min(wrist_girth, 240.0))
cuff_height = max(30.0, min(cuff_height, 130.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 12.0))
seam_allowance = max(2.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
PALM_FIN = palm_girth * NEG
WRIST_FIN = wrist_girth * NEG
finger_len = min(finger_len, hand_length - 50.0)
PALM_BODY = max(60.0, hand_length - finger_len)
HALF = PALM_FIN / 2.0
DOME = max(20.0, min(finger_len, HALF * 0.9))    # dome depth clamped so top never a point


def _mitt_shell(name, label, palmar):
    """One mitt panel (palm or back): a rounded dome top; the palmar panel carries the
    actuator pocket."""
    w = HALF
    kb = PALM_BODY
    tip = PALM_BODY + finger_len
    edges = [
        fc.Edge("wrist", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_thumb", [fc.Line(fc.P(w, 0.0), fc.P(w, tip - DOME))]),
        fc.Edge("top", [fc.Bezier(fc.P(w, tip - DOME),
                                  fc.P(w, tip), fc.P(0.0, tip),
                                  fc.P(0.0, tip - DOME))]),
        fc.Edge("side_pinky", [fc.Line(fc.P(0.0, tip - DOME), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if palmar:
        cx = w * 0.5
        internals.append(fc.Internal("actuator_pocket",
                                     [fc.P(cx, kb * 0.5), fc.P(cx, kb * 0.5 + finger_len)],
                                     kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance, allowances={"wrist": 0.0},
        notches=[fc.Notch("wrist", 0.5, "centre"), fc.Notch("side_thumb", 0.5, "thumb match")],
        grainline=fc.Grainline(fc.P(w * 0.5, kb * 0.2), fc.P(w * 0.5, kb * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_palm():
    return _mitt_shell("palm", "Palm (actuator pocket)", palmar=True)


def build_back():
    return _mitt_shell("back", "Back", palmar=False)


def build_thumb():
    """The thumb pocket (cut 2 mirrored): a small rounded stall."""
    w = max(45.0, PALM_FIN * 0.22)
    h = finger_len * 0.85
    dome = max(15.0, min(h * 0.5, w * 0.9))
    edges = [
        fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("outer", [fc.Line(fc.P(w, 0.0), fc.P(w, h - dome))]),
        fc.Edge("tip", [fc.Bezier(fc.P(w, h - dome), fc.P(w, h), fc.P(0.0, h),
                                  fc.P(0.0, h - dome))]),
        fc.Edge("inner", [fc.Line(fc.P(0.0, h - dome), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "thumb", edges, seam_allowance=seam_allowance, allowances={"base": 0.0},
        notches=[fc.Notch("base", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Thumb pocket (cut 2)")


def build_cuff():
    ln = PALM_FIN
    h = cuff_height
    return fc.Piece(
        "cuff", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1), label="Wrist cuff (cut 1)")


def build():
    pattern = fc.PatternSet("soft-finger-mitt")
    every = target_piece == "set"
    palm = build_palm()
    back = build_back()
    thumb = build_thumb()
    cuff = build_cuff()
    if not every:
        picked = {"palm": palm, "back": back, "thumb": thumb, "cuff": cuff}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (palm, back, thumb, cuff):
        pattern.add(piece)
    pattern.declare_seam(("palm", "side_thumb"), ("back", "side_thumb"), tol=1.0)
    pattern.declare_seam(("palm", "side_pinky"), ("back", "side_pinky"), tol=1.0)
    pattern.declare_seam(("palm", "top"), ("back", "top"), tol=1.5)
    pattern.declare_seam(("cuff", "attach"), [("palm", "wrist"), ("back", "wrist")], tol=1.5)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "neoprene (2 mm, four-way stretch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "palm + back + thumb + cuff at negative ease so the mitt grips."},
        {"item": "soft-finger actuator (Yantra4D soft-finger)", "qty": 1, "unit": "piece",
         "note": f"one printed curling finger, finger_len {finger_len:.0f} mm = the drafted "
                 "palmar pocket; slid in, never modelled here."},
        {"item": "silicone air tube + bulb", "qty": round(finger_len * 3.0), "unit": "mm_length",
         "note": "squeeze the bulb to curl the finger and pinch a zip-pull or sock edge."},
        {"item": "wrist elastic", "qty": round(WRIST_FIN), "unit": "mm_length",
         "note": f"gathers the cuff mouth ({PALM_FIN:.0f} mm) down to the wrist "
                 f"({WRIST_FIN:.0f} mm)."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock the mitt seams so nothing presses a hand with limited grip."},
    ]
    pattern.metadata = {
        "fc500_rank": 433, "family": "adaptive", "fabric_hint": "neopreno",
        "silhouette_note": "A soft-finger dressing mitt: a neoprene mitt carrying one curling "
            "soft-finger actuator that pinches a zip-pull, button hook or sock edge against the "
            "palm.",
        "hardware": "soft-finger actuator via Yantra4D (notion.hardware_ref -> soft-finger); "
            "finger_len IS the drafted palmar pocket, the same finger_len that drives the "
            "actuator_pocket interface — the dimensional handshake.",
        "solver": {
            "finger_len_mm": round(finger_len, 1), "dome_mm": round(DOME, 1),
            "palm_finished_mm": round(PALM_FIN, 1),
            "note": "the mitt-top dome depth is clamped between 20 mm and 90% of the half-width "
                    "so the top can never collapse to a degenerate point; finger_len clamped "
                    "under hand_length-50.",
        },
        "adaptive": {
            "assist": "one curling actuator pinches an object against the palm — a dressing aid "
                      "for a hand that cannot oppose thumb and fingers on its own.",
        },
    }
    return pattern


result = build()
