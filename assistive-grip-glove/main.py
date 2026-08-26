"""
Assistive grip glove — Fashion Cabinet Garment Cartridge
(FC-500 rank #431, adaptive / soft-exo, Yantra4D-bridged finray-gripper).

A soft-exoskeleton grip glove for a hand that cannot close on its own: a neoprene glove shell
whose palmar side carries Fin-Ray finger ribs that flex the wearer's fingers around an object
when the tendon line is pulled, and open them when it is released. The glove is the soft body;
the Fin-Ray finger is the Yantra4D `finray-gripper` solid, printed and slid into a palmar
channel, never modelled here.

Two real decisions:

  1. THE FINGER CHANNEL IS SOLVED TO THE FINGER LENGTH — THE DIMENSIONAL HANDSHAKE. Each of the
     four finger channels on the palmar shell runs the drafted finger length from the knuckle
     line to the fingertip; that `finger_len` is the same number that drives the Yantra4D
     `finray-gripper` fin length, so the printed rib is exactly as long as the channel that
     holds it. `finger_len` drives BOTH the hardware AND the garment's `finger_channel`
     interface — one number, two objects.

  2. NEGATIVE EASE ON THE SHELL, STRAIGHT STABLE CHANNELS. The neoprene shell is cut at a small
     negative ease so it grips the hand and does not slide when the ribs work; but the channel
     seams that carry the rigid ribs are drafted straight and stable so the rib does not buckle.

Pieces: palm (with the four finger channels + thumb channel), back-of-hand, cuff. Made to
measure to hand length, palm girth, finger length and wrist girth.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # palm|back|cuff|set

hand_length = float(PARAM(lambda: hand_length, 190.0))     # wrist crease to fingertip
palm_girth = float(PARAM(lambda: palm_girth, 210.0))       # around the palm at the knuckles
finger_len = float(PARAM(lambda: finger_len, 80.0))        # knuckle line to fingertip
wrist_girth = float(PARAM(lambda: wrist_girth, 170.0))
cuff_height = float(PARAM(lambda: cuff_height, 70.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
hand_length = max(140.0, min(hand_length, 240.0))
palm_girth = max(150.0, min(palm_girth, 280.0))
finger_len = max(50.0, min(finger_len, 110.0))
wrist_girth = max(130.0, min(wrist_girth, 240.0))
cuff_height = max(30.0, min(cuff_height, 130.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 12.0))
seam_allowance = max(2.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
PALM_FIN = palm_girth * NEG
WRIST_FIN = wrist_girth * NEG
# The shell is palm + back; each is half the palm ring. Clamp the finger length so it can
# never exceed the hand length minus the palm body (which would invert the fingertip above
# the knuckle line).
PALM_BODY = max(60.0, hand_length - finger_len)            # wrist crease to knuckle line
finger_len = min(finger_len, hand_length - 50.0)           # keep a real palm body
HALF = PALM_FIN / 2.0                                       # palm/back panel width


def _hand_shell(name, label, palmar):
    """One hand shell panel (palm or back). Width HALF; body PALM_BODY up to the knuckle
    line, then the fingers splay to `finger_len`. The palmar panel carries the rib channels
    as internal markings; the back panel is plain."""
    w = HALF
    kb = PALM_BODY                       # knuckle-line y
    tip = PALM_BODY + finger_len         # fingertip y
    edges = [
        fc.Edge("wrist", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_thumb", [fc.Line(fc.P(w, 0.0), fc.P(w, kb))]),
        # finger splay: a gentle dome from the little-finger side over to the index side.
        fc.Edge("fingertips", [fc.Bezier(fc.P(w, kb),
                                         fc.P(w * 0.92, tip),
                                         fc.P(w * 0.08, tip),
                                         fc.P(0.0, kb))]),
        fc.Edge("side_pinky", [fc.Line(fc.P(0.0, kb), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if palmar:
        # Four finger channels running the knuckle line to the fingertip (finger_len), plus a
        # thumb channel angled off the thumb side.
        for i in range(4):
            x = w * (0.16 + 0.68 * i / 3.0)
            internals.append(fc.Internal(f"finger_channel_{i}",
                                         [fc.P(x, kb), fc.P(x, kb + finger_len * 0.96)],
                                         kind="marking"))
        internals.append(fc.Internal("thumb_channel",
                                     [fc.P(w * 0.86, kb * 0.30),
                                      fc.P(w * 0.98, kb * 0.30 + finger_len * 0.7)],
                                     kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"wrist": 0.0},
        notches=[fc.Notch("wrist", 0.5, "centre"),
                 fc.Notch("side_thumb", 0.5, "thumb match")],
        grainline=fc.Grainline(fc.P(w * 0.5, kb * 0.15), fc.P(w * 0.5, kb * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_palm():
    return _hand_shell("palm", "Palm shell (rib channels)", palmar=True)


def build_back():
    return _hand_shell("back", "Back-of-hand shell", palmar=False)


def build_cuff():
    """The wrist cuff (cut 1, folded): its attach length matches the palm+back wrist edges
    (the glove mouth = the palm ring); a wrist elastic gathers it down to WRIST_FIN. Height
    cuff_height."""
    ln = PALM_FIN                    # == palm.wrist + back.wrist, so it sews flat
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
    pattern = fc.PatternSet("assistive-grip-glove")
    every = target_piece == "set"
    palm = build_palm()
    back = build_back()
    cuff = build_cuff()
    if not every:
        picked = {"palm": palm, "back": back, "cuff": cuff}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, palm, cuff)
    for piece in (palm, back, cuff):
        pattern.add(piece)
    # Palm sews to back at both sides + across the fingertips (mirror halves).
    pattern.declare_seam(("palm", "side_thumb"), ("back", "side_thumb"), tol=1.0)
    pattern.declare_seam(("palm", "side_pinky"), ("back", "side_pinky"), tol=1.0)
    pattern.declare_seam(("palm", "fingertips"), ("back", "fingertips"), tol=1.5)
    # Cuff attaches to the two wrist edges (palm + back).
    pattern.declare_seam(("cuff", "attach"),
                         [("palm", "wrist"), ("back", "wrist")], tol=1.5)
    return _finish(pattern, palm, cuff)


def _finish(pattern, palm, cuff):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "neoprene (2 mm, four-way stretch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "palm + back + cuff at negative ease; the shell grips so the ribs do not "
                 "slide when they work."},
        {"item": "Fin-Ray finger ribs (Yantra4D finray-gripper)", "qty": 4, "unit": "piece",
         "note": f"four printed Fin-Ray fingers, fin_len {finger_len:.0f} mm = the drafted "
                 "finger channel; slid into the palmar channels, never modelled here."},
        {"item": "tendon cord + channel sleeving", "qty": round(finger_len * 5.0),
         "unit": "mm_length",
         "note": "the pull cord that flexes the fingers around an object and releases them."},
        {"item": "wrist elastic", "qty": round(WRIST_FIN), "unit": "mm_length",
         "note": f"gathers the cuff mouth ({PALM_FIN:.0f} mm) down to the wrist "
                 f"({WRIST_FIN:.0f} mm) so the glove stays on."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock the shell seams so nothing presses a hand that cannot re-grip."},
    ]
    pattern.metadata = {
        "fc500_rank": 431, "family": "adaptive", "fabric_hint": "neopreno",
        "silhouette_note": "A soft-exo grip glove: a neoprene shell with palmar Fin-Ray "
            "finger channels that close the hand around an object and open on release.",
        "hardware": "Fin-Ray fingers via Yantra4D (notion.hardware_ref -> finray-gripper); "
            "fin_len IS the drafted finger channel, the same finger_len that drives the "
            "finger_channel interface — the dimensional handshake.",
        "solver": {
            "finger_len_mm": round(finger_len, 1),
            "palm_body_mm": round(PALM_BODY, 1),
            "palm_finished_mm": round(PALM_FIN, 1),
            "note": "finger_len is clamped under hand_length-50 so the fingertip can never "
                    "invert above the knuckle line; the rib channels are straight so the "
                    "rigid rib does not buckle.",
        },
        "adaptive": {
            "assist": "Fin-Ray fingers flex the wearer's fingers around an object when the "
                      "tendon line is pulled and open on release — grip for a hand that "
                      "cannot close on its own.",
        },
    }
    return pattern


result = build()
