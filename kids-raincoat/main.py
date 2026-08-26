"""
Children's Hooded Raincoat — Fashion Cabinet Garment Cartridge
(FC-400 #323, kids_baby, T2).

A hooded raincoat for a child in PU-coated nylon: a full body with a snap-fastened
storm-flap front, an attached hood, raglan sleeves, and every seam sealed. Drafted
from CHILD measurements (bodies/child-6y). Two things matter for a rain garment: a
hood that actually fits the head (a raincoat hood that will not go over the head,
or slides down over the eyes, is useless in rain), and a storm flap that covers
the snaps so water does not track down the closure.

Two things are solved by measurement rather than by formula:

  1. THE HOOD IS DRAFTED TO THE MEASURED HEAD, NOT SCALED FROM THE NECK. The hood
     height and width are derived from the MEASURED head girth and head length, so
     it clears the head and the face opening sits at the brow — a hood scaled from
     the neckline (the common shortcut) is far too small for a child's large head.
     The hood face opening is floored on the head girth.

  2. THE STORM FLAP IS WIDER THAN THE SNAP GAP IT COVERS. The flap covers the snap
     placket plus an overlap on each side, clamped so it can never come out
     narrower than the gap — a flap narrower than what it covers lets water track
     down the snaps, and a naive draft tying flap width to a fraction of the chest
     produces exactly that at a small size.

The SNAP-FIT SOLID is Yantra4D territory (`snap-fit`; see notion.hardware_ref).

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
# front|back|sleeve|hood|storm_flap|set

chest_girth = float(PARAM(lambda: chest_girth, 640.0))
head_girth = float(PARAM(lambda: head_girth, 500.0))
head_length = float(PARAM(lambda: head_length, 230.0))     # crown to nape over the top
body_length = float(PARAM(lambda: body_length, 420.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 340.0))
neck_width = float(PARAM(lambda: neck_width, 130.0))
front_snaps = float(PARAM(lambda: front_snaps, 5.0))
snap_dia = float(PARAM(lambda: snap_dia, 13.0))
flap_overlap = float(PARAM(lambda: flap_overlap, 28.0))
wear_ease = float(PARAM(lambda: wear_ease, 160.0))         # over rain clothes
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

chest_girth = max(520.0, min(chest_girth, 820.0))
head_girth = max(420.0, min(head_girth, 580.0))
head_length = max(180.0, min(head_length, 300.0))
body_length = max(300.0, min(body_length, 620.0))
sleeve_length = max(240.0, min(sleeve_length, 480.0))
neck_width = max(100.0, min(neck_width, 190.0))
front_snaps = max(3.0, min(round(front_snaps), 8.0))
snap_dia = max(10.0, min(snap_dia, 20.0))
flap_overlap = max(16.0, min(flap_overlap, 50.0))
wear_ease = max(80.0, min(wear_ease, 300.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(15.0, min(hem_allowance, 40.0))

TOPSTITCH = 6.0
N_SNAPS = int(front_snaps)

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
NECK_DROP_F = max(50.0, HALF_NECK * 0.95)
NECK_DROP_B = max(14.0, HALF_NECK * 0.28)

PLACKET_LEN = body_length - NECK_DROP_F
SNAP_END_CLEAR = max(snap_dia * 1.5, 30.0)
SNAP_RUN = max(snap_dia * 2.0, PLACKET_LEN - 2.0 * SNAP_END_CLEAR)
N_INTERVALS = max(1, N_SNAPS - 1)
SNAP_PITCH = SNAP_RUN / N_INTERVALS

# The hood from the MEASURED head, floored on the head girth.
HOOD_HEIGHT = max(head_length * 0.9, head_girth * 0.42)
_HOOD_FACE_RAW = head_length * 1.0
HOOD_FACE = max(head_girth * 0.55, _HOOD_FACE_RAW)

# The storm flap wider than the snap gap.
SNAP_STAND = max(snap_dia * 0.9, 18.0)
_FLAP_W_RAW = 2.0 * (SNAP_STAND + flap_overlap)
FLAP_W = max(2.0 * SNAP_STAND + 2.0 * seam_allowance, _FLAP_W_RAW)


def _snap(label, x, y):
    a = max(3.0, snap_dia * 0.3)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


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
    internals = []
    y0 = SNAP_END_CLEAR
    for i in range(N_SNAPS):
        internals.append(_snap(f"front snap-{i + 1}", SNAP_STAND, y0 + SNAP_PITCH * i))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
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
        internals=[],
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
    cuff_w = sw * 0.72
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
            fc.Internal("cuff snap tab", [fc.P((sw - cuff_w) / 2.0 + 20.0, -ln + 20.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Raglan sleeve (cut 2, mirrored)",
    )


def build_hood():
    """The hood, cut 2 mirrored. Drafted to the MEASURED head."""
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
        allowances={"face": hem_allowance * 0.6},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match"),
                 fc.Notch("face", 0.0, "brow point")],
        grainline=fc.Grainline(fc.P(face * 0.3, face * 0.2), fc.P(face * 0.3, h - 20.0)),
        internals=[
            fc.Internal("brim drawcord channel",
                        [fc.P(face * 0.6, 6.0), fc.P(face * 0.72, face - 6.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood (cut 2, mirrored)",
    )


def build_storm_flap():
    w = FLAP_W
    h = PLACKET_LEN
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("outer", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "storm_flap", edges,
        seam_allowance=seam_allowance,
        allowances={"outer": hem_allowance * 0.5},
        notches=[fc.Notch("attach", 0.5, "CF attach")],
        grainline=fc.Grainline(fc.P(w * 0.5, 15.0), fc.P(w * 0.5, h - 15.0)),
        internals=[
            fc.Internal("overlap edge topstitch",
                        [fc.P(w - TOPSTITCH, TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                        kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Snap storm flap (cut 1)",
    )


def build():
    pattern = fc.PatternSet("kids-raincoat")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "hood": everything or target_piece == "hood",
        "storm_flap": everything or target_piece == "storm_flap",
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
    if want["storm_flap"]:
        pattern.add(build_storm_flap())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if want["front"] and want["sleeve"]:
        pattern.declare_seam(("front", "raglan"), ("sleeve", "raglan_l"), tol=1.5)
    if want["back"] and want["sleeve"]:
        pattern.declare_seam(("back", "raglan"), ("sleeve", "raglan_r"), tol=1.5)
    if want["storm_flap"] and want["front"]:
        pattern.declare_seam(("storm_flap", "attach"), ("front", "cf"),
                             tol=1.5, ease=PLACKET_LEN - _FRONT.edge("cf").length(0.05))

    fabric_width = 1450.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "PU-coated nylon, 120 gsm (waterproof, taped seams)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; tape every seam — a "
                 f"sewn seam in a raincoat leaks at the needle holes."},
        {"item": "snap-fit fastener", "qty": N_SNAPS + 2, "unit": "set",
         "note": f"Yantra4D snap-fit (notion.hardware_ref) at {snap_dia:.0f} mm: "
                 f"{N_SNAPS} on the front at a SOLVED pitch of {SNAP_PITCH:.1f} mm, "
                 f"covered by the storm flap, plus 2 cuff-tab snaps."},
        {"item": "reflective piping + hood drawcord", "qty": 1, "unit": "set",
         "note": "reflective trim for visibility in rain/dusk; a soft drawcord in "
                 "the hood brim (no cord-lock on a young child's neck — a safety "
                 "choice)."},
        {"item": "waterproof seam tape + PTFE needle", "qty": 1, "unit": "roll",
         "note": "iron-on seam tape over every stitched seam."},
    ]
    pattern.metadata = {
        "fc400_rank": 323,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "pu-coated-nylon",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "hood_height": round(HOOD_HEIGHT, 1),
            "hood_face": round(HOOD_FACE, 1),
            "storm_flap_width": round(FLAP_W, 1),
        },
        "solved": {
            "front_snap_count": N_SNAPS,
            "front_snap_pitch_solved_mm": round(SNAP_PITCH, 2),
            "hood_face_requested_mm": round(_HOOD_FACE_RAW, 2),
            "hood_face_final_mm": round(HOOD_FACE, 2),
            "hood_clears_head": bool(HOOD_FACE >= head_girth * 0.5),
            "flap_width_requested_mm": round(_FLAP_W_RAW, 2),
            "flap_width_final_mm": round(FLAP_W, 2),
            "flap_covers_gap": bool(FLAP_W >= 2.0 * SNAP_STAND),
            "note": "the hood is drafted to the MEASURED head girth and length, not "
                    "scaled from the neckline — a hood scaled from the neck is far "
                    "too small for a child's large head. The storm flap width is "
                    "the snap stand plus a spark-of-water overlap on EACH side, "
                    "clamped so it can never come out narrower than the gap it "
                    "covers, or water tracks down the snaps. The snaps are solved "
                    "across the measured placket.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y)",
            "head_dominant_hood": "the hood is floored on the head girth, not a neck "
                                  "proportion — a child's head is large relative to "
                                  "the body",
            "no_neck_cordlock": "a soft drawcord in the hood brim, NOT a cord-lock at "
                                "the neck — a deliberate safety choice for a young "
                                "child",
        },
        "hardware": "snap-fit fasteners via Yantra4D (notion.hardware_ref -> "
                    "snap-fit); the solid's bore_dia — the socket the stud seats "
                    "into — is fed from this garment's snap_dia, which also sizes "
                    "and spaces the whole front snap column. Covered by the storm "
                    "flap so water does not track the closure.",
    }
    return pattern


result = build()
