"""
Children's Anorak — Fashion Cabinet Garment Cartridge
(FC-400 #329, kids_baby, T2).

A pullover anorak for a child in ripstop nylon: a half-zip front, a kangaroo
pouch pocket, an attached hood, and a drawcord hem gathered on a cord-lock. It
goes over the head (a half-zip, not a full front), which is the number that has
to be right: the neck-plus-half-zip opening must clear the child's HEAD, or the
anorak cannot be pulled on.

Two things are solved by measurement rather than by formula:

  1. THE HALF-ZIP OPENING CLEARS THE HEAD. A pullover has no full front, so the
     opening the head passes through is the neckline PLUS the length of the
     half-zip. That combined opening is drafted to at least the MEASURED head
     girth — the zip length is floored so, added to the neck, the head always
     passes. A half-zip cut to a fashion length leaves an opening too small for
     the head.

  2. THE HEM DRAWCORD IS RECONCILED WITH THE CORD-LOCK. The drawcord channel runs
     the MEASURED hem circumference; the cord is cut to that plus the tail the
     cord-lock needs to grip and the child needs to pull, so the anorak actually
     cinches. The cord-lock's cord_dia drives the channel width so the cord runs
     free.

The CORD-LOCK SOLID is Yantra4D territory (`cord-lock`; see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|hood|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 640.0))
head_girth = float(PARAM(lambda: head_girth, 500.0))
head_length = float(PARAM(lambda: head_length, 230.0))
body_length = float(PARAM(lambda: body_length, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 350.0))
neck_width = float(PARAM(lambda: neck_width, 135.0))
half_zip = float(PARAM(lambda: half_zip, 180.0))          # half-zip length
cord_dia = float(PARAM(lambda: cord_dia, 4.0))            # drawcord diameter
pocket_width = float(PARAM(lambda: pocket_width, 240.0))
wear_ease = float(PARAM(lambda: wear_ease, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 28.0))  # drawcord channel

chest_girth = max(520.0, min(chest_girth, 820.0))
head_girth = max(420.0, min(head_girth, 580.0))
head_length = max(180.0, min(head_length, 300.0))
body_length = max(300.0, min(body_length, 600.0))
sleeve_length = max(240.0, min(sleeve_length, 480.0))
neck_width = max(100.0, min(neck_width, 190.0))
half_zip = max(100.0, min(half_zip, 300.0))
cord_dia = max(3.0, min(cord_dia, 7.0))
pocket_width = max(140.0, min(pocket_width, 360.0))
wear_ease = max(80.0, min(wear_ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 45.0))

TOPSTITCH = 6.0

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
NECK_DROP_F = max(50.0, HALF_NECK * 0.9)
NECK_DROP_B = max(14.0, HALF_NECK * 0.28)

# The head-clearing opening: the neckline run plus the half-zip. Floor the zip so
# that opening is at least the head girth.
NECK_RUN_EST = neck_width * 1.5   # rough finished neckline (front + back)
_HALF_ZIP_RAW = half_zip
NEEDED_ZIP = max(0.0, head_girth * 0.5 - NECK_RUN_EST * 0.5)
HALF_ZIP = max(NEEDED_ZIP, _HALF_ZIP_RAW)
HEAD_OPENING = NECK_RUN_EST + HALF_ZIP * 2.0

# The hood from the measured head.
HOOD_HEIGHT = max(head_length * 0.9, head_girth * 0.42)
HOOD_FACE = max(head_girth * 0.55, head_length)

# The hem drawcord: hem circumference plus a cord-lock grip tail.
HEM_CIRC = QUARTER_CHEST * 4.0 * 0.94   # slightly gathered
CORD_TAIL = max(120.0, HEM_CIRC * 0.15)
CORD_CUT = HEM_CIRC + CORD_TAIL + cord_dia * 6.0
CHANNEL_W = max(cord_dia * 2.4, 12.0)

# The pocket clamped against the front.
_POCKET_W_RAW = pocket_width
POCKET_W = max(100.0, min(_POCKET_W_RAW, QUARTER_CHEST * 2.0 - 2.0 * seam_allowance))
POCKET_H = max(90.0, POCKET_W * 0.5)


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
        fc.Edge("raglan", [fc.Line(p_underarm, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": 0.0},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("cf", 1.0 - HALF_ZIP / (body_length - NECK_DROP_B - NECK_DROP_F),
                          "half-zip base"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 20.0), fc.P(hw * 0.4, body_length - 20.0)),
        internals=[
            fc.Internal("half-zip topstitch",
                        [fc.P(TOPSTITCH, body_length - NECK_DROP_B - NECK_DROP_F),
                         fc.P(TOPSTITCH, body_length - NECK_DROP_B - NECK_DROP_F - HALF_ZIP)],
                        kind="trace"),
            fc.Internal("hem drawcord channel",
                        [fc.P(0.0, CHANNEL_W), fc.P(hw, CHANNEL_W)], kind="marking"),
            fc.Internal("kangaroo pocket placement",
                        [fc.P(hw - POCKET_W / 2.0, CHANNEL_W + 20.0),
                         fc.P(hw + POCKET_W / 2.0 - POCKET_W, CHANNEL_W + 20.0 + POCKET_H)],
                        kind="marking"),
        ],
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
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("side", 0.0, "hem"),
                 fc.Notch("raglan", 0.5, "raglan mid")],
        grainline=fc.Grainline(fc.P(hw * 0.35, 20.0), fc.P(hw * 0.35, body_length - 20.0)),
        internals=[
            fc.Internal("hem drawcord channel",
                        [fc.P(0.0, CHANNEL_W), fc.P(hw, CHANNEL_W)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
FRONT_RAGLAN = _FRONT.edge("raglan").length(0.05)
BACK_RAGLAN = _BACK.edge("raglan").length(0.05)


def build_sleeve():
    import math as _m
    sw = QUARTER_CHEST * 1.02
    ln = sleeve_length
    cuff_w = sw * 0.66
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
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Raglan sleeve (cut 2, mirrored)",
    )


def build_hood():
    h = HOOD_HEIGHT
    face = HOOD_FACE
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(face * 0.6, 0.0))]),
        fc.Edge("face", [fc.Line(fc.P(face * 0.6, 0.0), fc.P(face * 0.75, face))]),
        fc.Edge("crown", [fc.curve_through(
            fc.P(face * 0.75, face), fc.P(0.0, h), bulge=0.25, side=-1.0)]),
        fc.Edge("cb", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "hood", edges,
        seam_allowance=seam_allowance,
        allowances={"face": hem_allowance * 0.5},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(face * 0.3, face * 0.2), fc.P(face * 0.3, h - 20.0)),
        internals=[
            fc.Internal("brim drawcord channel",
                        [fc.P(face * 0.6, 6.0), fc.P(face * 0.72, face - 6.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (cut 2, mirrored)",
    )


def build_pocket():
    """The kangaroo pouch, cut 1. Clamped against the front width."""
    w = POCKET_W
    h = POCKET_H
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        # Angled hand openings at the two top corners, straight sides, flat bottom.
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, h * 0.4)),
                           fc.Line(fc.P(w, h * 0.4), fc.P(w - h * 0.4, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w - h * 0.4, 0.0), fc.P(h * 0.4, 0.0))]),
        fc.Edge("side_l", [fc.Line(fc.P(h * 0.4, 0.0), fc.P(0.0, h * 0.4)),
                           fc.Line(fc.P(0.0, h * 0.4), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance * 0.5},
        notches=[fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[
            fc.Internal("hand-opening topstitch (R)",
                        [fc.P(w - TOPSTITCH, h * 0.4), fc.P(w - h * 0.4, TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Kangaroo pouch (cut 1)",
    )


def build():
    pattern = fc.PatternSet("kids-anorak")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "hood": everything or target_piece == "hood",
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
    if want["hood"]:
        pattern.add(build_hood())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "hem"), ("back", "hem"), tol=1.0)
    if want["front"] and want["sleeve"]:
        pattern.declare_seam(("front", "raglan"), ("sleeve", "raglan_l"), tol=1.5)
    if want["back"] and want["sleeve"]:
        pattern.declare_seam(("back", "raglan"), ("sleeve", "raglan_r"), tol=1.5)

    fabric_width = 1450.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "ripstop nylon, 70 gsm (windproof, packable)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a light ripstop that "
                 f"packs into its own pouch — a good travel/play anorak."},
        {"item": "cord-lock (single-hole) + drawcord", "qty": 2, "unit": "set",
         "note": f"Yantra4D cord-lock (notion.hardware_ref) for a {cord_dia:.0f} mm "
                 f"cord; the cord runs {CORD_CUT:.0f} mm round the MEASURED hem plus "
                 f"a grip tail. cord_dia drives the channel width so it runs free."},
        {"item": "half-zip + zip garage", "qty": 1, "unit": "piece",
         "note": f"a {HALF_ZIP:.0f} mm half-zip; floored so the neck-plus-zip "
                 f"opening ({HEAD_OPENING:.0f} mm) always clears the head. A garage "
                 f"at the top protects the chin."},
        {"item": "bar-tack thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": "bar-tack the pocket corners and the zip base; topstitch the "
                 "channels."},
    ]
    pattern.metadata = {
        "fc400_rank": 329,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "ripstop-nylon",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "half_zip": round(HALF_ZIP, 1),
            "head_opening": round(HEAD_OPENING, 1),
            "hood_face": round(HOOD_FACE, 1),
            "pocket_width": round(POCKET_W, 1),
        },
        "solved": {
            "half_zip_requested_mm": round(_HALF_ZIP_RAW, 2),
            "half_zip_floored_mm": round(HALF_ZIP, 2),
            "half_zip_was_floored": bool(abs(HALF_ZIP - _HALF_ZIP_RAW) > 0.01),
            "head_opening_mm": round(HEAD_OPENING, 2),
            "head_opening_clears_head": bool(HEAD_OPENING >= head_girth * 0.95),
            "hem_circ_mm": round(HEM_CIRC, 2),
            "cord_cut_mm": round(CORD_CUT, 2),
            "channel_width_mm": round(CHANNEL_W, 2),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "note": "a pullover anorak has no full front, so the head passes through "
                    "the neckline PLUS the half-zip — the zip is FLOORED so that "
                    "combined opening is at least the measured head girth, or the "
                    "anorak cannot be pulled on. The hem drawcord is cut to the "
                    "MEASURED hem plus a cord-lock grip tail, and the channel width "
                    "is driven by the cord diameter so the cord runs free. The "
                    "kangaroo pouch is clamped against the front.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y)",
            "pullover_head_clearance": "the half-zip is floored so the neck-plus-zip "
                                       "opening clears the head — a pullover's whole "
                                       "risk",
        },
        "hardware": "cord-lock via Yantra4D (notion.hardware_ref -> cord-lock); the "
                    "solid's cord_dia is fed from this garment's cord_dia, which also "
                    "sizes the drawcord channel width. The half-zip is a companion "
                    "hard good, floored for head clearance.",
    }
    return pattern


result = build()
