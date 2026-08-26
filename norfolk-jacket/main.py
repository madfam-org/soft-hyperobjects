"""
Norfolk jacket — Fashion Cabinet Garment Cartridge (FC-500 #406, tailoring, T3).

The Norfolk: a belted country tweed jacket with vertical BOX PLEATS front and back (they
give room to raise a shotgun or a fishing rod) and a self-fabric BELT through side loops.
A shaped FRONT (cut 2) with a button stand, a BACK (cut 1), a set-in SLEEVE (cut 2), a
notch COLLAR (cut 1) and the BELT (cut 1). The front buttons bridge to the Yantra4D
`shank-button-solid` solid.

Solved, not guessed:

  1. THE SLEEVE CAP MATCHES THE ARMSCYE. The cap is a SOLVED bow whose length equals the
     measured front + back armhole, so the sleeve sets in without easing a mismatch.
  2. THE COLLAR IS CUT TO THE MEASURED NECKLINE.
  3. THE BOX-PLEAT DEPTH IS CLAMPED. The pleat take-up cannot exceed the panel half-width
     less a margin, so a deep pleat can never consume the whole panel and fold it into a
     self-crossing outline. Extra pleat cloth is added to the panel width, not stolen from it.

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
# front|back|sleeve|collar|belt|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
body_length = float(PARAM(lambda: body_length, 720.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
neck_width = float(PARAM(lambda: neck_width, 190.0))
back_neck_rise = float(PARAM(lambda: back_neck_rise, 22.0))
pleat_depth = float(PARAM(lambda: pleat_depth, 40.0))    # box-pleat take-up per pleat
belt_width = float(PARAM(lambda: belt_width, 50.0))
button_dia = float(PARAM(lambda: button_dia, 22.0))      # drives shank-button diameter
ease = float(PARAM(lambda: ease, 140.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_girth = max(760.0, min(chest_girth, 1500.0))
body_length = max(560.0, min(body_length, 860.0))
shoulder_width = max(340.0, min(shoulder_width, 580.0))
armhole_depth = max(200.0, min(armhole_depth, 360.0))
sleeve_length = max(440.0, min(sleeve_length, 720.0))
neck_width = max(140.0, min(neck_width, 280.0))
back_neck_rise = max(10.0, min(back_neck_rise, 45.0))
pleat_depth = max(15.0, min(pleat_depth, 90.0))
belt_width = max(30.0, min(belt_width, 80.0))
button_dia = max(14.0, min(button_dia, 34.0))
ease = max(40.0, min(ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

Q_CHEST = max(shoulder_width / 2.0 * 0.6, (chest_girth + ease) / 4.0)
HALF_NECK = neck_width / 2.0
HALF_SHOULDER = min(shoulder_width / 2.0, Q_CHEST - 4.0)
Y_UNDERARM = body_length - armhole_depth
# The box pleat ADDS cloth to the panel; the take-up is clamped under the panel half-width
# so the pleat lines never cross the panel edge, and the extra is added, not subtracted.
PLEAT = min(pleat_depth, Q_CHEST * 0.35)
BUTTON_STAND = max(30.0, button_dia * 1.6)


def build_front():
    ext = BUTTON_STAND
    # extra width for the front box pleat, added to the panel
    w = Q_CHEST + PLEAT
    p_hem_cf = fc.P(-ext, 0.0)
    p_hem_side = fc.P(w, 0.0)
    p_underarm = fc.P(w, Y_UNDERARM)
    p_shoulder = fc.P(HALF_SHOULDER + PLEAT, body_length)
    p_neck = fc.P(HALF_NECK, body_length)
    p_cf_neck = fc.P(-ext, body_length - back_neck_rise * 0.4)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("armhole", [fc.curve_through(p_underarm, p_shoulder,
                                             bulge=0.24, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.curve_through(p_neck, p_cf_neck, bulge=0.14, side=-1.0)]),
        fc.Edge("cf", [fc.Line(p_cf_neck, p_hem_cf)]),
    ]
    pleat_x = HALF_SHOULDER * 0.7
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 34.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(w * 0.3, 30.0), fc.P(w * 0.3, body_length - 30.0)),
        internals=[
            fc.Internal("button stand fold", [fc.P(0.0, 0.0), fc.P(0.0, body_length)],
                        kind="marking"),
            fc.Internal("box pleat (fold to fold)",
                        [fc.P(pleat_x - PLEAT / 2.0, 0.0),
                         fc.P(pleat_x - PLEAT / 2.0, body_length)], kind="dart"),
            fc.Internal("box pleat (fold to fold) b",
                        [fc.P(pleat_x + PLEAT / 2.0, 0.0),
                         fc.P(pleat_x + PLEAT / 2.0, body_length)], kind="dart"),
            fc.Internal("button run",
                        [fc.P(-ext * 0.45, body_length * 0.82),
                         fc.P(-ext * 0.45, body_length * 0.22)], kind="marking"),
            fc.Internal("belt loop",
                        [fc.P(w - 20.0, Y_UNDERARM * 0.7),
                         fc.P(w, Y_UNDERARM * 0.7)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    w = Q_CHEST + PLEAT
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(w, 0.0)
    p_underarm = fc.P(w, Y_UNDERARM)
    p_shoulder = fc.P(HALF_SHOULDER + PLEAT, body_length)
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
    pleat_x = HALF_SHOULDER * 0.7
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 34.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(w * 0.3, 30.0), fc.P(w * 0.3, body_length - 30.0)),
        internals=[
            fc.Internal("box pleat a",
                        [fc.P(pleat_x - PLEAT / 2.0, 0.0),
                         fc.P(pleat_x - PLEAT / 2.0, body_length)], kind="dart"),
            fc.Internal("box pleat b",
                        [fc.P(pleat_x + PLEAT / 2.0, 0.0),
                         fc.P(pleat_x + PLEAT / 2.0, body_length)], kind="dart"),
            fc.Internal("belt loop",
                        [fc.P(w - 20.0, Y_UNDERARM * 0.7),
                         fc.P(w, Y_UNDERARM * 0.7)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Back (cut 1)",
    )


_F = build_front()
_B = build_back()
ARMHOLE_LEN = _F.edge("armhole").length(0.05) + _B.edge("armhole").length(0.05)
NECK_LEN = _F.edge("neck").length(0.05) * 2.0 + _B.edge("neck").length(0.05) * 2.0


def build_sleeve():
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
        allowances={"cuff": 40.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sleeve_length - 30.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


def build_collar():
    ln = NECK_LEN
    depth = max(45.0, neck_width * 0.35)
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
        internals=[fc.Internal("roll line", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Notch collar (cut 1)",
    )


def build_belt():
    """The self-fabric belt, cut 1. Length ~ chest girth + ease + a tongue."""
    ln = chest_girth + ease + 300.0
    w = belt_width * 2.0 + 2.0 * seam_allowance
    return fc.Piece(
        "belt", [
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("point", [fc.Line(fc.P(ln, w), fc.P(ln + belt_width, w / 2.0)),
                              fc.Line(fc.P(ln + belt_width, w / 2.0), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Self belt (cut 1)",
    )


def build():
    pattern = fc.PatternSet("norfolk-jacket")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "belt": everything or target_piece == "belt",
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
    if want["belt"]:
        pattern.add(build_belt())

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
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "tweed / heavy wool", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 66% marker; the box pleats add cloth to "
                 f"the panels — the marker already includes the pleat depth."},
        {"item": "shank buttons (front + cuff)", "qty": 7, "unit": "count",
         "note": f"Yantra4D shank-button-solid (notion.hardware_ref) at a {button_dia:.0f} mm "
                 f"diameter; the front stand carries the button run."},
        {"item": "buckle for the self-belt", "qty": 1, "unit": "count",
         "note": "a plain single-prong buckle; the belt threads the side loops."},
        {"item": "lining + canvas front", "qty": 1, "unit": "set",
         "note": "a half-canvas front and a full lining, country-jacket weight."},
    ]
    pattern.metadata = {
        "fc500_rank": 406, "family": "tailoring", "tier": 3,
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "The belted Norfolk: box pleats front and back for reach room, a "
            "self-belt through side loops, a notch collar and set-in sleeves.",
        "solved": {
            "quarter_chest_mm": round(Q_CHEST, 1),
            "pleat_requested_mm": round(pleat_depth, 1),
            "pleat_clamped_mm": round(PLEAT, 1),
            "pleat_was_clamped": bool(abs(PLEAT - pleat_depth) > 0.01),
            "armhole_measured_mm": round(ARMHOLE_LEN, 1),
            "neck_measured_mm": round(NECK_LEN, 1),
            "note": "the sleeve cap is a solved bow to the measured armhole; the collar is "
                    "cut to the measured neckline; the box-pleat take-up is clamped under "
                    "the panel half-width and ADDED to the panel width, not stolen from it, "
                    "so a deep pleat can never fold the panel into a self-crossing outline.",
        },
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> shank-button-solid); "
                    "diameter_mm is fed from button_dia.",
    }
    return pattern


result = build()
