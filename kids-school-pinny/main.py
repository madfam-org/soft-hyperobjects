"""
School Smock (Pinny) — Fashion Cabinet Garment Cartridge
(FC-400 #326, kids_baby, T1).

A pull-on school art smock for a child: a loose overhead tabard with elbow-length
raglan sleeves, a back-neck button opening (so it clears the head), and a big
front pocket for pencils and paint rags. It goes ON over the head and OFF over
the head, so — like every child's pullover — the number that has to be right is
the neck opening plus its back-button slit clearing the HEAD.

Two things are solved by measurement rather than by formula:

  1. THE BACK BUTTON SLIT IS FLOORED SO THE HEAD PASSES. A closed neckline sized
     for the neck will not pass a child's large head, so the back opening runs a
     MEASURED slit below the neckline, floored so the neckline plus the slit
     together clear the head girth — the button then closes the slit for wear.

  2. THE FRONT POCKET IS CLAMPED AGAINST THE BODY. A big smock pocket wider than
     the smock front folds it over, and — because the kernel CCW-normalizes an
     inverted outline and area() takes an absolute value — such a pocket renders
     and passes verify() looking healthy. The pocket width is clamped and reported.

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
# front|back|sleeve|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 640.0))
head_girth = float(PARAM(lambda: head_girth, 510.0))
body_length = float(PARAM(lambda: body_length, 460.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 250.0))   # elbow-length
neck_width = float(PARAM(lambda: neck_width, 140.0))
button_ligne = float(PARAM(lambda: button_ligne, 20.0))
pocket_width = float(PARAM(lambda: pocket_width, 300.0))
wear_ease = float(PARAM(lambda: wear_ease, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

chest_girth = max(520.0, min(chest_girth, 820.0))
head_girth = max(420.0, min(head_girth, 580.0))
body_length = max(320.0, min(body_length, 640.0))
sleeve_length = max(150.0, min(sleeve_length, 400.0))
neck_width = max(110.0, min(neck_width, 200.0))
button_ligne = max(14.0, min(button_ligne, 28.0))
pocket_width = max(160.0, min(pocket_width, 480.0))
wear_ease = max(120.0, min(wear_ease, 360.0))
seam_allowance = max(8.0, min(seam_allowance, 16.0))
hem_allowance = max(15.0, min(hem_allowance, 40.0))

TOPSTITCH = 5.0
BUTTON_MM = button_ligne * 0.635

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
NECK_DROP_F = max(45.0, HALF_NECK * 0.85)
NECK_DROP_B = max(14.0, HALF_NECK * 0.28)

# The head-clearing back slit: the neckline run plus the slit must clear the head.
NECK_RUN_EST = neck_width * 1.5
_SLIT_RAW = 60.0
NEEDED_SLIT = max(0.0, head_girth * 0.5 - NECK_RUN_EST * 0.5)
BACK_SLIT = max(NEEDED_SLIT, _SLIT_RAW)
HEAD_OPENING = NECK_RUN_EST + BACK_SLIT * 2.0

# The front pocket clamped against the body.
_POCKET_W_RAW = pocket_width
POCKET_W = max(120.0, min(_POCKET_W_RAW, QUARTER_CHEST * 2.0 - 2.0 * seam_allowance))
POCKET_H = max(90.0, POCKET_W * 0.42)


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_underarm = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_neck_pt = fc.P(HALF_NECK, body_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, body_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("raglan", [fc.Line(p_underarm, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.30, side=1.0)]),
        fc.Edge("cf_fold", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, body_length - 20.0)),
        internals=[
            fc.Internal("pocket placement",
                        [fc.P(-POCKET_W / 2.0 + hw * 0.0, POCKET_H + hem_allowance + 20.0),
                         fc.P(POCKET_W / 2.0, POCKET_H + hem_allowance + 20.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Front (cut on fold)",
    )


def build_back():
    """Back, cut 2 mirrored, with the CB button slit for head clearance."""
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_underarm = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_neck_pt = fc.P(HALF_NECK, body_length)
    # The CB edge runs up to the slit base, then the neckline; the slit is the top
    # part of the CB that buttons closed.
    p_slit_base = fc.P(0.0, body_length - NECK_DROP_B - BACK_SLIT)
    p_neck_cb = fc.P(0.0, body_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("raglan", [fc.Line(p_underarm, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        # The slit edge (buttons here), then the closed CB below.
        fc.Edge("slit", [fc.Line(p_neck_cb, p_slit_base)]),
        fc.Edge("cb", [fc.Line(p_slit_base, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("slit", 1.0, "slit base / bar-tack"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 20.0), fc.P(hw * 0.35, body_length - 20.0)),
        internals=[
            _button("neck button", BUTTON_MM * 1.2, body_length - NECK_DROP_B - 8.0),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2, mirrored) with CB button slit",
    )


_FRONT = build_front()
_BACK = build_back()
FRONT_RAGLAN = _FRONT.edge("raglan").length(0.05)
BACK_RAGLAN = _BACK.edge("raglan").length(0.05)


def build_sleeve():
    import math as _m
    sw = QUARTER_CHEST * 1.0
    ln = sleeve_length
    cuff_w = sw * 0.82
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    cap_y = min(FRONT_RAGLAN, BACK_RAGLAN) * 0.75
    dxl = _m.sqrt(max(1.0, FRONT_RAGLAN ** 2 - cap_y ** 2))
    dxr = _m.sqrt(max(1.0, BACK_RAGLAN ** 2 - cap_y ** 2))
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
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_y * 0.9)),
        internals=[
            fc.Internal("cuff elastic casing",
                        [fc.P((sw - cuff_w) / 2.0 + 6.0, -ln + hem_allowance * 0.5),
                         fc.P((sw - cuff_w) / 2.0 + cuff_w - 6.0,
                              -ln + hem_allowance * 0.5)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Raglan sleeve (cut 2, mirrored)",
    )


def build_pocket():
    """The big front pocket, cut 1. Clamped against the smock front."""
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
        notches=[fc.Notch("mouth", 0.33, "divider 1"),
                 fc.Notch("mouth", 0.66, "divider 2")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=[
            fc.Internal("divider 1", [fc.P(w / 3.0, 0.0), fc.P(w / 3.0, h)], kind="trace"),
            fc.Internal("divider 2", [fc.P(2.0 * w / 3.0, 0.0), fc.P(2.0 * w / 3.0, h)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Divided front pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("kids-school-pinny")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
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
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if want["front"] and want["sleeve"]:
        pattern.declare_seam(("front", "raglan"), ("sleeve", "raglan_l"), tol=1.5)
    if want["back"] and want["sleeve"]:
        pattern.declare_seam(("back", "raglan"), ("sleeve", "raglan_r"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "poly-cotton drill, 180 gsm (hard-wearing, washable)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; poly-cotton takes a "
                 f"hot wash and dries fast — the school-smock cloth (paint comes out)."},
        {"item": "sew-through button", "qty": 1, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm); closes the back "
                 f"neck slit that lets the head pass."},
        {"item": "soft cuff elastic", "qty": 2, "unit": "length",
         "note": "elbow-length sleeves gathered on a soft elastic to keep them out "
                 "of the paint."},
        {"item": "topstitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{TOPSTITCH:.0f} mm on the pocket dividers and the neck bind."},
    ]
    pattern.metadata = {
        "fc400_rank": 326,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "poly-cotton",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "back_slit": round(BACK_SLIT, 1),
            "head_opening": round(HEAD_OPENING, 1),
            "pocket_width": round(POCKET_W, 1),
        },
        "solved": {
            "back_slit_requested_mm": round(_SLIT_RAW, 2),
            "back_slit_floored_mm": round(BACK_SLIT, 2),
            "back_slit_was_floored": bool(abs(BACK_SLIT - _SLIT_RAW) > 0.01),
            "head_opening_mm": round(HEAD_OPENING, 2),
            "head_opening_clears_head": bool(HEAD_OPENING >= head_girth * 0.95),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "note": "the smock goes on over the head, so the neckline PLUS the back "
                    "button slit must clear the head — the slit is FLOORED so the "
                    "combined opening is at least the measured head girth. The big "
                    "divided front pocket is clamped against the smock front, "
                    "because an inverted pocket is CCW-normalized by the kernel and "
                    "passes verify() looking healthy.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y)",
            "head_clearing_slit": "the back button slit is floored so the neckline "
                                  "plus the slit clears the head — a pullover smock's "
                                  "whole risk",
            "elbow_sleeves": "elbow-length elasticated sleeves keep the cuffs out of "
                             "the paint",
        },
        "hardware": "sew-through button via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonhole that "
                    "closes the head-clearing slit.",
    }
    return pattern


result = build()
