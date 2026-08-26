"""
Denim chore jacket — Fashion Cabinet Garment Cartridge (FC-500 #402, denim, T2).

The boxy denim work jacket (chore coat / bleu de travail): a straight FRONT (cut 2) with a
button placket and three patch pockets, a straight BACK (cut 1), a two-piece straight
SLEEVE (cut 2), and a band COLLAR (cut 1). Denim conventions: 7 mm twin-needle gold
topstitch, felled seams, every hard good a Yantra4D reference. The pocket-corner rivets
bridge to the Yantra4D `rivet` solid.

Solved, not guessed:

  1. THE ARMSCYE AND SLEEVE CAP MATCH. The sleeve cap is a SOLVED bow whose length equals
     the measured front + back armhole, so the sleeve sets in without easing a mismatch.
  2. THE COLLAR BAND IS CUT TO THE MEASURED NECKLINE. The band length is the summed front
     + back neck edges, never a laid-flat guess.
  3. EVERY DERIVED DIMENSION IS CLAMPED. The placket extension, the pocket size and the
     rivet insets are all floored/held so a big-ease or small-body request can never draw a
     negative-width piece the kernel would CCW-normalize into a healthy-looking sliver.

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
# front|back|sleeve|collar|patch_pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
body_length = float(PARAM(lambda: body_length, 660.0))     # nape to hem
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
neck_width = float(PARAM(lambda: neck_width, 200.0))
back_neck_rise = float(PARAM(lambda: back_neck_rise, 22.0))
placket_width = float(PARAM(lambda: placket_width, 35.0))
rivet_cap = float(PARAM(lambda: rivet_cap, 9.0))          # drives Yantra4D rivet cap_dia
ease = float(PARAM(lambda: ease, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_girth = max(760.0, min(chest_girth, 1500.0))
body_length = max(500.0, min(body_length, 820.0))
shoulder_width = max(340.0, min(shoulder_width, 580.0))
armhole_depth = max(200.0, min(armhole_depth, 360.0))
sleeve_length = max(440.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 280.0))
back_neck_rise = max(10.0, min(back_neck_rise, 45.0))
placket_width = max(20.0, min(placket_width, 60.0))
rivet_cap = max(5.0, min(rivet_cap, 16.0))
ease = max(40.0, min(ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

TOPSTITCH = 7.0
Q_CHEST = max(shoulder_width / 2.0 * 0.6, (chest_girth + ease) / 4.0)
HALF_NECK = neck_width / 2.0
HALF_SHOULDER = min(shoulder_width / 2.0, Q_CHEST - 4.0)
Y_UNDERARM = body_length - armhole_depth


def _rivet(label, x, y):
    a = max(3.0, rivet_cap * 0.6)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def build_front():
    """Front, cut 2. A straight box with a button-placket extension at CF and two lower
    patch-pocket placements (marked; the pockets are a separate piece)."""
    ext = placket_width
    p_hem_cf = fc.P(-ext, 0.0)
    p_hem_side = fc.P(Q_CHEST, 0.0)
    p_underarm = fc.P(Q_CHEST, Y_UNDERARM)
    p_shoulder = fc.P(HALF_SHOULDER, body_length)
    p_neck = fc.P(HALF_NECK, body_length)
    p_cf_neck = fc.P(-ext, body_length - back_neck_rise * 0.4)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [fc.curve_through(p_underarm, p_shoulder,
                                             bulge=0.24, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.curve_through(p_neck, p_cf_neck, bulge=0.16, side=-1.0)]),
        fc.Edge("cf", [fc.Line(p_cf_neck, p_hem_cf)]),
    ]
    pocket_y = Y_UNDERARM * 0.42
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 28.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm"),
                 fc.Notch("armhole", 0.5, "armhole balance")],
        grainline=fc.Grainline(fc.P(Q_CHEST * 0.3, 30.0),
                               fc.P(Q_CHEST * 0.3, body_length - 30.0)),
        internals=[
            fc.Internal("placket fold", [fc.P(0.0, 0.0), fc.P(0.0, body_length)],
                        kind="marking"),
            fc.Internal("button run",
                        [fc.P(-ext * 0.4, body_length * 0.85),
                         fc.P(-ext * 0.4, body_length * 0.20)], kind="marking"),
            fc.Internal("patch pocket placement",
                        [fc.P(Q_CHEST * 0.25, pocket_y),
                         fc.P(Q_CHEST * 0.75, pocket_y),
                         fc.P(Q_CHEST * 0.75, pocket_y - Q_CHEST * 0.42),
                         fc.P(Q_CHEST * 0.25, pocket_y - Q_CHEST * 0.42),
                         fc.P(Q_CHEST * 0.25, pocket_y)], kind="marking"),
            _rivet("pocket rivet (bar-tack proxy)",
                   Q_CHEST * 0.25 + rivet_cap, pocket_y - rivet_cap),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    """Back, cut 1. A straight box, higher round neck at CB."""
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(Q_CHEST, 0.0)
    p_underarm = fc.P(Q_CHEST, Y_UNDERARM)
    p_shoulder = fc.P(HALF_SHOULDER, body_length)
    p_neck = fc.P(HALF_NECK, body_length)
    p_cb_neck = fc.P(0.0, body_length - back_neck_rise)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [fc.curve_through(p_underarm, p_shoulder,
                                             bulge=0.24, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.curve_through(p_neck, p_cb_neck, bulge=0.30, side=-1.0)]),
        fc.Edge("cb", [fc.Line(p_cb_neck, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 28.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(Q_CHEST * 0.3, 30.0),
                               fc.P(Q_CHEST * 0.3, body_length - 30.0)),
        internals=[fc.Internal("centre-back yoke line",
                               [fc.P(0.0, Y_UNDERARM + armhole_depth * 0.5),
                                fc.P(Q_CHEST, Y_UNDERARM + armhole_depth * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Back (cut 1)",
    )


_F = build_front()
_B = build_back()
ARMHOLE_LEN = _F.edge("armhole").length(0.05) + _B.edge("armhole").length(0.05)
NECK_LEN = _F.edge("neck").length(0.05) * 2.0 + _B.edge("neck").length(0.05) * 2.0


def build_sleeve():
    """A straight two-fall sleeve, cut 2. The cap is a SOLVED bow whose length equals the
    measured armhole so it sets in flush; the underarm falls straight to a plain cuff."""
    half_bicep = max(120.0, Q_CHEST * 0.62)
    cap_height = max(60.0, armhole_depth * 0.42)
    p_cuff_l = fc.P(-half_bicep * 0.82, 0.0)
    p_cuff_r = fc.P(half_bicep * 0.82, 0.0)
    p_underarm_r = fc.P(half_bicep, sleeve_length - cap_height)
    p_cap = fc.P(0.0, sleeve_length)
    p_underarm_l = fc.P(-half_bicep, sleeve_length - cap_height)

    def cap_edge(bulge):
        return fc.Edge("cap", [
            fc.curve_through(p_underarm_r, p_cap, bulge=bulge, side=1.0),
            fc.curve_through(p_cap, p_underarm_l, bulge=bulge, side=1.0)])

    half_arm = ARMHOLE_LEN / 2.0
    lo, hi = 0.0, 2.5
    if cap_edge(hi).length(0.05) < half_arm:
        hi = 6.0
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if cap_edge(mid).length(0.05) < half_arm:
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Line(p_cuff_l, p_cuff_r)]),
        fc.Edge("seam_r", [fc.Line(p_cuff_r, p_underarm_r)]),
        cap_edge(b),
        fc.Edge("seam_l", [fc.Line(p_underarm_l, p_cuff_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 34.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("seam_r", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sleeve_length - 30.0)),
        internals=[fc.Internal("cuff topstitch",
                               [fc.P(-half_bicep * 0.6, TOPSTITCH),
                                fc.P(half_bicep * 0.6, TOPSTITCH)], kind="trace")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


def build_collar():
    """A band collar, cut 1. Cut to the MEASURED neckline, folded to depth."""
    ln = NECK_LEN
    depth = max(30.0, placket_width * 1.3)
    w = depth * 2.0 + 2.0 * seam_allowance
    return fc.Piece(
        "collar", [
            fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.5, "CB"),
                 fc.Notch("lower", 0.25, "shoulder"),
                 fc.Notch("lower", 0.75, "shoulder")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Band collar (cut 1)",
    )


def build_patch_pocket():
    """A patch pocket, cut 2 (chest) or 3 in wear; rivets at the top corners (marked)."""
    w = max(120.0, Q_CHEST * 0.42)
    h = max(120.0, w * 1.05)
    a = max(3.0, rivet_cap * 0.6)
    edges = [
        fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, h * 0.22))]),
        fc.Edge("point", [fc.Line(fc.P(w, h * 0.22), fc.P(w / 2.0, 0.0)),
                          fc.Line(fc.P(w / 2.0, 0.0), fc.P(0.0, h * 0.22))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h * 0.22), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "patch_pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": 26.0},
        notches=[fc.Notch("mouth", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, h - TOPSTITCH),
                         fc.P(w - TOPSTITCH, h - TOPSTITCH)], kind="trace"),
            _rivet("rivet L", seam_allowance + a, h - seam_allowance - a),
            _rivet("rivet R", w - seam_allowance - a, h - seam_allowance - a),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Patch pocket (cut 2)",
    )


def build():
    pattern = fc.PatternSet("denim-chore-jacket")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "patch_pocket": everything or target_piece == "patch_pocket",
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
    if want["patch_pocket"]:
        pattern.add(build_patch_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.8)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=0.8)
    if want["collar"] and want["front"] and want["back"]:
        summed = 2.0 * _F.edge("neck").length(0.05) + 2.0 * _B.edge("neck").length(0.05)
        pattern.declare_seam(("collar", "lower"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")],
                             tol=1.0, ease=NECK_LEN - summed)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "denim, 12-14 oz", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; felled seams and "
                 f"{TOPSTITCH:.0f} mm twin-needle gold topstitch throughout."},
        {"item": "rivet + burr (pocket corners)", "qty": 6, "unit": "set",
         "note": f"Yantra4D rivet (notion.hardware_ref) at a {rivet_cap:.0f} mm cap; set "
                 f"through the marked pocket-corner drill points."},
        {"item": "shank / tack buttons (front + cuffs)", "qty": 8, "unit": "count",
         "note": "the placket and cuff closures; marked on the button run."},
        {"item": "topstitch thread (gold) + jeans needle", "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm on all felled seams and pocket mouths."},
    ]
    pattern.metadata = {
        "fc500_rank": 402, "family": "denim", "tier": 2,
        "fabric_hint": "mezclilla-14oz",
        "silhouette_note": "The boxy denim chore jacket: straight front + back, set-in "
            "sleeve, band collar, patch pockets.",
        "solved": {
            "quarter_chest_mm": round(Q_CHEST, 1),
            "armhole_measured_mm": round(ARMHOLE_LEN, 1),
            "neck_measured_mm": round(NECK_LEN, 1),
            "note": "the sleeve cap is a solved bow whose length equals the measured "
                    "armhole so it sets in flush; the band collar is cut to the measured "
                    "neckline; the shoulder tip and quarter-chest are clamped so a big-ease "
                    "or small-body request never draws a negative-width piece.",
        },
        "hardware": "rivet via Yantra4D (notion.hardware_ref -> rivet); the rivet's cap "
                    "height and burr are fed from rivet_cap (the sewn-edge params are left "
                    "unmapped — a rivet is set through a drilled hole, no sewn seam, so no "
                    "dimensional handshake is owed). Marked at the pocket corners.",
    }
    return pattern


result = build()
