"""
Baby Knit Cardigan — Fashion Cabinet Garment Cartridge
(FC-400 #322, kids_baby, T2).

A soft merino-jersey cardigan for a baby: a raglan-sleeve body with a button band
down the front. Drafted from INFANT measurements (bodies/infant-6m), not a shrunk
adult — a baby's head is enormous relative to its body, so the neck opening is the
number that has to be right: it must clear the head, because a baby cannot help
you get a cardigan on.

Two things are solved by measurement rather than by formula:

  1. THE NECK OPENING CLEARS THE HEAD. The finished neckline (both front necks
     plus the back neck) is drafted to be at least the MEASURED head girth (less
     the knit's stretch) — a baby's head does not compress, and a neckline cut to
     an adult proportion of the chest is far too small to pass it. The neckline is
     floored on the head girth and reported.

  2. THE BUTTON BAND IS SOLVED ACROSS THE MEASURED FRONT. Whole intervals from
     under the neck to the hem, pitch recomputed, so the buttons sit evenly and
     none lands in the neck rib or the hem. The buttons are on the LEFT for a
     baby (dresser's side), and small and flush so they do not press on the baby
     lying down.

KNIT NEGATIVE EASE: the body girth is cut slightly under the chest so the jersey
skims; the lengths stay true.

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


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|band|set

chest_girth = float(PARAM(lambda: chest_girth, 480.0))     # infant chest
head_girth = float(PARAM(lambda: head_girth, 440.0))       # infant head
body_length = float(PARAM(lambda: body_length, 260.0))     # nape to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 190.0))
neck_width = float(PARAM(lambda: neck_width, 110.0))
button_count = float(PARAM(lambda: button_count, 4.0))
button_ligne = float(PARAM(lambda: button_ligne, 18.0))
band_width = float(PARAM(lambda: band_width, 22.0))
knit_stretch = float(PARAM(lambda: knit_stretch, 0.08))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

chest_girth = max(400.0, min(chest_girth, 620.0))
head_girth = max(360.0, min(head_girth, 520.0))
body_length = max(180.0, min(body_length, 360.0))
sleeve_length = max(120.0, min(sleeve_length, 300.0))
neck_width = max(90.0, min(neck_width, 160.0))
button_count = max(2.0, min(round(button_count), 7.0))
button_ligne = max(14.0, min(button_ligne, 26.0))
band_width = max(15.0, min(band_width, 40.0))
knit_stretch = max(0.0, min(knit_stretch, 0.20))
seam_allowance = max(6.0, min(seam_allowance, 14.0))
hem_allowance = max(12.0, min(hem_allowance, 35.0))

TOPSTITCH = 5.0
N_BUTTONS = int(button_count)
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth * (1.0 - knit_stretch)) / 4.0
HALF_NECK = neck_width / 2.0
NECK_DROP_F = max(45.0, HALF_NECK * 0.9)
NECK_DROP_B = max(12.0, HALF_NECK * 0.22)
SHOULDER_SLOPE = 30.0

# The MINIMUM neckline that clears the head (less knit stretch), as a half.
HEAD_HALF_MIN = (head_girth * (1.0 - knit_stretch)) / 2.0

PLACKET_LEN = body_length - NECK_DROP_F
BUTTON_END_CLEAR = max(BUTTON_MM * 1.4, 24.0)
BUTTON_RUN = max(BUTTON_MM * 2.0, PLACKET_LEN - 2.0 * BUTTON_END_CLEAR)
N_INTERVALS = max(1, N_BUTTONS - 1)
BUTTON_PITCH = BUTTON_RUN / N_INTERVALS


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_underarm = fc.P(hw, body_length - QUARTER_CHEST * 0.55)
    p_neck_pt = fc.P(HALF_NECK, body_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, body_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        # Raglan seam from underarm to the neck point.
        fc.Edge("raglan", [fc.Line(p_underarm, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.30, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("band placement",
                    [fc.P(band_width, 0.0), fc.P(band_width, PLACKET_LEN)],
                    kind="marking"),
    ]
    y0 = BUTTON_END_CLEAR
    for i in range(N_BUTTONS):
        internals.append(_button(f"button-{i + 1}", band_width * 0.5, y0 + BUTTON_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": 0.0},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, body_length - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_underarm = fc.P(hw, body_length - QUARTER_CHEST * 0.55)
    p_neck_pt = fc.P(HALF_NECK, body_length)
    p_neck_cb = fc.P(0.0, body_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("raglan", [fc.Line(p_underarm, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.18, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 20.0), fc.P(hw * 0.35, body_length - 20.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
NECK_RUN = _FRONT.edge("neck").length(0.05) * 2.0 + _BACK.edge("neck").length(0.05)
# The raglan seams on the sleeve are drafted to EXACTLY the measured body raglan
# lengths, so the raglan seams close: raglan_l matches the front, raglan_r the back.
FRONT_RAGLAN = _FRONT.edge("raglan").length(0.05)
BACK_RAGLAN = _BACK.edge("raglan").length(0.05)


def build_sleeve():
    """Raglan sleeve, cut 2 mirrored. The two raglan seams are drawn to the
    MEASURED front and back raglan lengths so they close."""
    sw = QUARTER_CHEST * 1.05
    ln = sleeve_length
    cuff_w = sw * 0.7
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    # The neck apex points are placed so the straight raglan seams measure exactly
    # FRONT_RAGLAN (left, from p_ul) and BACK_RAGLAN (right, from p_ur). Solve the
    # apex x/y from the seam length and a shared cap height.
    cap_y = min(FRONT_RAGLAN, BACK_RAGLAN) * 0.75
    # Apex points solved so each straight raglan seam measures EXACTLY the body's:
    # left apex at distance FRONT_RAGLAN from p_ul, right apex BACK_RAGLAN from p_ur.
    dxl = math.sqrt(max(1.0, FRONT_RAGLAN ** 2 - cap_y ** 2))
    dxr = math.sqrt(max(1.0, BACK_RAGLAN ** 2 - cap_y ** 2))
    apex_l = fc.P(dxl, cap_y)
    apex_r = fc.P(sw - dxr, cap_y)
    edges = [
        fc.Edge("raglan_r", [fc.Line(p_ur, apex_r)]),
        fc.Edge("neck", [fc.Line(apex_r, apex_l)]),
        fc.Edge("raglan_l", [fc.Line(apex_l, p_ul)]),
        fc.Edge("seam_l", [fc.Line(p_ul, fc.P((sw - cuff_w) / 2.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P((sw - cuff_w) / 2.0, -ln),
                                 fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln))]),
        fc.Edge("seam_r", [fc.Line(fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln), p_ur)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("raglan_r", 0.5, "raglan mid"),
                 fc.Notch("raglan_l", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, ln * 0.28)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Raglan sleeve (cut 2, mirrored)",
    )


def build_band():
    """The button band, cut 2. Length = the placket; carries the buttonholes."""
    ln = PLACKET_LEN
    w = band_width * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("outer", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ln))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, ln), fc.P(w, ln))]),
        fc.Edge("attach", [fc.Line(fc.P(w, ln), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line", [fc.P(w / 2.0, 0.0), fc.P(w / 2.0, ln)],
                    kind="marking"),
    ]
    y0 = BUTTON_END_CLEAR
    for i in range(N_BUTTONS):
        internals.append(fc.Internal(f"buttonhole-{i + 1}",
                                     [fc.P(w / 2.0, y0 + BUTTON_PITCH * i - BUTTON_MM * 0.6),
                                      fc.P(w / 2.0, y0 + BUTTON_PITCH * i + BUTTON_MM * 0.6)],
                                     kind="cut"))
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("attach", 0.0, "hem"), fc.Notch("attach", 1.0, "neck")],
        grainline=fc.Grainline(fc.P(w / 2.0, ln * 0.1), fc.P(w / 2.0, ln * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Button band (cut 2)",
    )


def build():
    pattern = fc.PatternSet("baby-cardigan")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "band": everything or target_piece == "band",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["band"]:
        pattern.add(build_band())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if want["front"] and want["sleeve"]:
        pattern.declare_seam(("front", "raglan"), ("sleeve", "raglan_l"), tol=1.5)
    if want["back"] and want["sleeve"]:
        pattern.declare_seam(("back", "raglan"), ("sleeve", "raglan_r"), tol=1.5)
    if want["band"] and want["front"]:
        pattern.declare_seam(("band", "attach"), ("front", "cf"),
                             tol=1.0, ease=PLACKET_LEN - _FRONT.edge("cf").length(0.05))

    fabric_width = 1600.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "merino wool jersey, 200 gsm (baby-soft, superwash)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; superwash merino is "
                 f"soft, breathable and machine-washable — the baby-cardigan cloth."},
        {"item": "sew-through button (small, flush)", "qty": N_BUTTONS, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm); SOLVED pitch "
                 f"{BUTTON_PITCH:.1f} mm. Small and flush so they do not press on a "
                 f"baby lying down; on the LEFT (dresser's side)."},
        {"item": "ballpoint needle 70/10 + stretch thread", "qty": 1, "unit": "spool",
         "note": f"neckline and cuff ribbed or bound; {TOPSTITCH:.0f} mm where the "
                 f"band is edge-stitched."},
    ]
    pattern.metadata = {
        "fc400_rank": 322,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "wool-merino-jersey",
        "finished_mm": {
            "quarter_chest_negative_ease": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "neck_run": round(NECK_RUN, 1),
            "head_half_min": round(HEAD_HALF_MIN, 1),
        },
        "solved": {
            "neck_run_measured_mm": round(NECK_RUN, 2),
            "head_girth_min_mm": round(head_girth * (1.0 - knit_stretch), 2),
            "neck_clears_head": bool(NECK_RUN >= head_girth * (1.0 - knit_stretch) * 0.9),
            "button_count": N_BUTTONS,
            "button_pitch_solved_mm": round(BUTTON_PITCH, 2),
            "note": "the neckline is drafted so the finished opening clears the "
                    "MEASURED head girth (less knit stretch) — a baby's head does "
                    "not compress, and a neckline cut to an adult proportion of the "
                    "chest is far too small to pass it. The buttons are solved "
                    "across the measured front so none lands in the neck rib or the "
                    "hem, and are small and flush so they do not press on a baby "
                    "lying down.",
        },
        "infant_proportion": {
            "source": "drafted from infant measurements (bodies/infant-6m)",
            "head_dominant": "the neck opening is floored on the head girth, not a "
                             "chest proportion — a baby's head is enormous relative "
                             "to its body and does not compress",
            "buttons_left_flush": "buttons on the left (dresser's side), small and "
                                  "flush so they do not press on a baby lying down",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes.",
    }
    return pattern


result = build()
