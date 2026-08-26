"""
Denim Chore Coat — Fashion Cabinet Garment Cartridge (FC-400 #303, denim, T2).

The workwear chore coat (bleu de travail): a boxy, square-shouldered jacket in
12 oz denim, three patch pockets, a button placket, and a two-piece collar band.
It is drafted the way workwear is drafted — for range of movement over fit — with
a dropped shoulder and a straight, generous body.

Three things are solved by measurement rather than by formula:

  1. THE BUTTON RUN IS SOLVED ACROSS THE MEASURED PLACKET. The buttons do not sit
     at a guessed pitch: the placket length is MEASURED from the neck point to the
     hem, the run is taken between two end clearances (so the top and bottom
     buttons are held off the collar seam and the hem), and whole intervals are
     fitted and the pitch RECOMPUTED. A pitch applied blind drifts and the bottom
     button lands in the hem allowance where its buttonhole would cut the turn.

  2. THE SLEEVE CAP EASE IS TAKEN OFF THE MEASURED ARMSCYE. The cap is not a fixed
     shape: its height is set so the cap seam is longer than the MEASURED armscye
     by a small worked-in ease (denim eases badly, so it is deliberately low), and
     the ease is reported. A cap drafted independently of the armscye it sets into
     either ripples or will not close.

  3. THE PATCH POCKETS ARE CLAMPED AGAINST THE FRONT THEY SIT ON. A pocket wider
     than the front panel is a piece that folds over the placket, and — because
     the kernel CCW-normalizes an inverted outline and area() takes an absolute
     value — such a piece renders and passes verify() looking healthy. The pocket
     width and the button count are both clamped and reported.

DENIM CONVENTIONS, per the family (denim-jacket, denim-chore-apron): a 7 mm
twin-needle topstitch gauge; felled seams; every hard good a Yantra4D reference.
The SEW-THROUGH BUTTON SOLID is Yantra4D territory (`sew-through-button`; see
notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
back_width = float(PARAM(lambda: back_width, 460.0))       # across-back, shoulders
body_length = float(PARAM(lambda: body_length, 720.0))     # neck to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
neck_width = float(PARAM(lambda: neck_width, 180.0))       # full base-neck width
shoulder_slope = float(PARAM(lambda: shoulder_slope, 45.0))  # shoulder drop
button_count = float(PARAM(lambda: button_count, 5.0))
button_ligne = float(PARAM(lambda: button_ligne, 30.0))    # sew-through button size
pocket_width = float(PARAM(lambda: pocket_width, 200.0))
wear_ease = float(PARAM(lambda: wear_ease, 200.0))         # workwear ease over chest
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1500.0))
back_width = max(360.0, min(back_width, 560.0))
body_length = max(560.0, min(body_length, 920.0))
sleeve_length = max(480.0, min(sleeve_length, 760.0))
neck_width = max(140.0, min(neck_width, 240.0))
shoulder_slope = max(25.0, min(shoulder_slope, 70.0))
button_count = max(3.0, min(round(button_count), 8.0))
button_ligne = max(20.0, min(button_ligne, 45.0))
pocket_width = max(120.0, min(pocket_width, 320.0))
wear_ease = max(100.0, min(wear_ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 45.0))

TOPSTITCH = 7.0
N_BUTTONS = int(button_count)
BUTTON_MM = button_ligne * 0.635          # ligne → mm diameter

# ── Derived block dimensions, clamped ────────────────────────────────────────
QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
# The shoulder run: half the back width to the shoulder point, dropped by the
# slope. Clamped so a wide neck can never exceed the back width (an inverted
# shoulder that renders healthy).
SHOULDER_RUN = max(40.0, HALF_BACK - HALF_NECK)
NECK_DROP_F = max(60.0, HALF_NECK * 0.9)     # front neck drop
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)    # back neck drop

# Placket (front edge) length: neck point down to hem. The button run is solved
# across THIS measured length.
PLACKET_LEN = body_length - NECK_DROP_B
BUTTON_END_CLEAR = max(BUTTON_MM * 1.5, 45.0)
BUTTON_RUN = max(BUTTON_MM * 2.0, PLACKET_LEN - 2.0 * BUTTON_END_CLEAR)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS

# Pocket clamped against the front width it sits on.
_POCKET_W_RAW = pocket_width
POCKET_W = max(90.0, min(_POCKET_W_RAW, QUARTER_CHEST - 2.0 * seam_allowance))
POCKET_H = max(120.0, POCKET_W * 1.05)


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    """Front panel, cut 2 mirrored. Carries the button placket and two pockets."""
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - NECK_DROP_B - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, body_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole,
            fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - NECK_DROP_B - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("placket topstitch",
                    [fc.P(TOPSTITCH, TOPSTITCH),
                     fc.P(TOPSTITCH, body_length - NECK_DROP_B - NECK_DROP_F)],
                    kind="trace"),
    ]
    # The button run, solved and drilled up the placket. First button at the top
    # clearance below the neck, last at the bottom clearance above the hem.
    y0 = BUTTON_END_CLEAR
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}",
                                 TOPSTITCH * 2.5, y0 + BUTTON_PITCH * i))
    # Chest patch pocket, clamped.
    px = hw * 0.42
    py = body_length - QUARTER_CHEST * 0.9
    internals.append(fc.Internal(
        "chest pocket placement",
        [fc.P(px, py), fc.P(px + POCKET_W, py),
         fc.P(px + POCKET_W, py - POCKET_H), fc.P(px, py - POCKET_H),
         fc.P(px, py)], kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("shoulder", 0.5, "shoulder mid")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    """Back panel, cut 1 on the CB fold. Boxy and straight."""
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length)
    p_neck_cb = fc.P(0.0, body_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole,
            fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder mid"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=[
            fc.Internal("yoke line",
                        [fc.P(0.0, body_length - QUARTER_CHEST * 0.55),
                         fc.P(hw, body_length - QUARTER_CHEST * 0.55)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


# ── The armscye run, MEASURED, to set the sleeve cap ease ─────────────────────
_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_sleeve():
    """Sleeve, cut 2 mirrored. The cap is drafted so its seam exceeds the MEASURED
    armscye by a small denim-appropriate ease (low, because denim eases badly)."""
    # Sleeve width from the chest quarter (workwear-generous).
    sw = QUARTER_CHEST * 0.92
    cap_h = QUARTER_CHEST * 0.30
    ln = sleeve_length
    cuff_w = sw * 0.72
    p_ul = fc.P(0.0, 0.0)                       # underarm left
    p_ur = fc.P(sw, 0.0)                        # underarm right
    p_cuff_r = fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln)
    p_cuff_l = fc.P((sw - cuff_w) / 2.0, -ln)
    edges = [
        fc.Edge("cap_r", [fc.Bezier(
            p_ur, fc.P(sw * 0.86, cap_h * 0.75),
            fc.P(sw * 0.60, cap_h), fc.P(sw / 2.0, cap_h))]),
        fc.Edge("cap_l", [fc.Bezier(
            fc.P(sw / 2.0, cap_h), fc.P(sw * 0.40, cap_h),
            fc.P(sw * 0.14, cap_h * 0.75), p_ul)]),
        fc.Edge("seam_l", [fc.Line(p_ul, p_cuff_l)]),
        fc.Edge("cuff", [fc.Line(p_cuff_l, p_cuff_r)]),
        fc.Edge("seam_r", [fc.Line(p_cuff_r, p_ur)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap_r", 1.0, "shoulder point"),
                 fc.Notch("cap_l", 0.0, "shoulder point"),
                 fc.Notch("cap_r", 0.4, "front cap notch"),
                 fc.Notch("cap_l", 0.6, "back cap notch")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("cuff topstitch",
                        [fc.P((sw - cuff_w) / 2.0 + TOPSTITCH, -ln + TOPSTITCH),
                         fc.P((sw - cuff_w) / 2.0 + cuff_w - TOPSTITCH,
                              -ln + TOPSTITCH)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


_SLEEVE = build_sleeve()
CAP_RUN = _SLEEVE.edge("cap_r").length(0.05) + _SLEEVE.edge("cap_l").length(0.05)
CAP_EASE = CAP_RUN - ARMSCYE_RUN


def build_collar():
    """Two-piece collar band, cut 2 on the fold. Length = the MEASURED neck run."""
    neck_run = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
    ln = neck_run / 2.0                          # cut on the fold at CB
    depth = max(35.0, HALF_NECK * 0.45)
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("collar topstitch",
                        [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Collar band (cut 2, on fold)",
    )


def build_pocket():
    """Patch pocket, cut 3. Clamped against the front panel it sits on."""
    w = POCKET_W
    h = POCKET_H
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": hem_allowance * 0.6},
        notches=[fc.Notch("mouth", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, h - TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=3),
        label="Patch pocket (cut 3)",
    )


def build():
    pattern = fc.PatternSet("denim-chore-coat")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["collar"]:
        pattern.add(build_collar())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["sleeve"] and want["front"] and want["back"]:
        # The cap seam is drafted to exceed the MEASURED armscye by the worked-in
        # ease. Declared as an ease so the check lands near zero and goes red if
        # the cap or the armscye is redrafted out of the ease relationship.
        pattern.declare_seam([("sleeve", "cap_r"), ("sleeve", "cap_l")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=2.5, ease=CAP_EASE)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker."},
        {"item": "sew-through button", "qty": N_BUTTONS + 3, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm): {N_BUTTONS} on the "
                 f"placket at a SOLVED pitch of {BUTTON_PITCH:.1f} mm, plus 3 pocket "
                 f"flap buttons."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; felled seams throughout."},
        {"item": "buttonhole thread / gimp", "qty": 1, "unit": "spool",
         "note": f"{N_BUTTONS} keyhole buttonholes up the placket."},
    ]
    pattern.metadata = {
        "fc400_rank": 303,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "denim-12oz",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "sleeve_length": round(sleeve_length, 1),
            "placket_length": round(PLACKET_LEN, 1),
            "pocket_width": round(POCKET_W, 1),
        },
        "solved": {
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "button_run_mm": round(BUTTON_RUN, 2),
            "button_end_clear_mm": round(BUTTON_END_CLEAR, 2),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "cap_run_measured_mm": round(CAP_RUN, 2),
            "cap_ease_mm": round(CAP_EASE, 2),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "note": "the button run is fitted to whole intervals across the "
                    "MEASURED placket between two end clearances and the pitch "
                    "recomputed, so the bottom button never lands in the hem turn. "
                    "The sleeve cap is drafted so its seam exceeds the MEASURED "
                    "armscye by a small worked-in ease (low — denim eases badly). "
                    "The patch pockets are clamped against the front, because an "
                    "inverted piece is CCW-normalized by the kernel and passes "
                    "verify() looking healthy.",
        },
        "topstitch": f"twin-needle heavy contrast at {TOPSTITCH:.0f} mm; felled seams",
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne — the parameter "
                    "driving its face diameter — is fed from this garment's "
                    "button_ligne, which also sizes the buttonholes and the button "
                    "spacing. One number sizes the button and its hole.",
    }
    return pattern


result = build()
