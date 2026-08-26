"""
Cable-knit vest — Fashion Cabinet Garment Cartridge (FC-500 #404, knitwear, T2).

A sleeveless pullover vest in a cabled wool knit: a FRONT with a V-neck, a BACK with a
higher round neck, joined at the shoulders and sides. The armholes are cut deep and
finished with a ribbed band; the neck and hems take ribbed bands too. Because a cable
knit pulls IN across its width (the cables draw the fabric), the body width carries a
modest positive ease that is CLAMPED so it never collapses below the chest quarter.

Solved, not guessed:

  1. THE SHOULDER SEAMS MATCH. Front and back shoulders are drafted to the SAME slope and
     length so they sew without a step; the front is drawn from the same shoulder point as
     the back and only the neckline differs (V front, round back).
  2. THE V-NECK DEPTH IS CLAMPED. The V cannot be drawn deeper than the armhole depth less
     a floor, so a deep-V request can never cross the front below the armhole into a
     self-intersecting neckline that the kernel would still close and pass.
  3. THE ARMHOLE BANDS ARE MEASURED. The front and back armhole edges are measured and
     summed so the ribbed armhole band is cut to the real opening, not a guess.

Pull-on: no hardware. Ribbed bands are companion rectangles.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|armhole_band|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
body_length = float(PARAM(lambda: body_length, 620.0))    # nape to hem
shoulder_width = float(PARAM(lambda: shoulder_width, 420.0))  # across the back
armhole_depth = float(PARAM(lambda: armhole_depth, 250.0))    # from shoulder to underarm
neck_width = float(PARAM(lambda: neck_width, 180.0))
v_depth = float(PARAM(lambda: v_depth, 190.0))            # front V from neck line
back_neck_rise = float(PARAM(lambda: back_neck_rise, 24.0))
ease = float(PARAM(lambda: ease, 80.0))                   # positive wearing ease
band_depth = float(PARAM(lambda: band_depth, 30.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

chest_girth = max(700.0, min(chest_girth, 1500.0))
body_length = max(440.0, min(body_length, 800.0))
shoulder_width = max(300.0, min(shoulder_width, 560.0))
armhole_depth = max(180.0, min(armhole_depth, 340.0))
neck_width = max(120.0, min(neck_width, 280.0))
v_depth = max(40.0, min(v_depth, 300.0))
back_neck_rise = max(10.0, min(back_neck_rise, 45.0))
ease = max(0.0, min(ease, 220.0))
band_depth = max(18.0, min(band_depth, 55.0))
seam_allowance = max(0.0, min(seam_allowance, 18.0))

# Body quarter width, with ease, floored so a cabled draw-in never collapses the panel.
Q_CHEST = max(shoulder_width / 2.0 * 0.55, (chest_girth + ease) / 4.0)
HALF_NECK = neck_width / 2.0
HALF_SHOULDER = shoulder_width / 2.0
# The shoulder tip sits at HALF_SHOULDER; clamp it inside the body quarter so the shoulder
# never sticks out past the side (which would fold the armhole).
HALF_SHOULDER = min(HALF_SHOULDER, Q_CHEST - 4.0)
# The V cannot dip below the underarm; clamp it above the armhole depth by a floor so the
# neckline never crosses the front outline into a self-intersection.
V_DEPTH = min(v_depth, armhole_depth - 30.0)
V_DEPTH = max(20.0, V_DEPTH)


def _front():
    """Front panel, cut 1 on the fold at CF? No — cut 1 flat (V-neck across CF). Drawn as
    a full front: hem at y=0, shoulder at y=body_length, V-neck at CF."""
    y_hem = 0.0
    y_underarm = body_length - armhole_depth
    y_shoulder = body_length
    p_hem_r = fc.P(Q_CHEST, y_hem)
    p_underarm_r = fc.P(Q_CHEST, y_underarm)
    p_shoulder_r = fc.P(HALF_SHOULDER, y_shoulder)
    p_neck_r = fc.P(HALF_NECK, y_shoulder)
    p_v = fc.P(0.0, y_shoulder - V_DEPTH)     # V point at CF
    p_hem_cf = fc.P(0.0, y_hem)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_r)]),
        fc.Edge("side", [fc.Line(p_hem_r, p_underarm_r)]),
        fc.Edge("armhole", [fc.curve_through(p_underarm_r, p_shoulder_r,
                                             bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_r, p_neck_r)]),
        fc.Edge("neck", [fc.Line(p_neck_r, p_v)]),   # half the V
        fc.Edge("cf", [fc.Line(p_v, p_hem_cf)]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": band_depth},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm"),
                 fc.Notch("armhole", 0.5, "armhole notch")],
        grainline=fc.Grainline(fc.P(Q_CHEST * 0.3, y_hem + 30.0),
                               fc.P(Q_CHEST * 0.3, y_shoulder - 30.0)),
        internals=[fc.Internal("cable panel centre",
                               [fc.P(Q_CHEST * 0.5, y_hem + band_depth),
                                fc.P(Q_CHEST * 0.5, y_underarm)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Front panel (cut 1)",
    )


def _back():
    """Back panel, cut 1. Same block, a higher round neck instead of the V."""
    y_hem = 0.0
    y_underarm = body_length - armhole_depth
    y_shoulder = body_length
    p_hem_r = fc.P(Q_CHEST, y_hem)
    p_underarm_r = fc.P(Q_CHEST, y_underarm)
    p_shoulder_r = fc.P(HALF_SHOULDER, y_shoulder)
    p_neck_r = fc.P(HALF_NECK, y_shoulder)
    # round back neck: a shallow scoop dipping back_neck_rise below the shoulder line at CB
    p_neck_cb = fc.P(0.0, y_shoulder - back_neck_rise)
    p_hem_cb = fc.P(0.0, y_hem)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_r)]),
        fc.Edge("side", [fc.Line(p_hem_r, p_underarm_r)]),
        fc.Edge("armhole", [fc.curve_through(p_underarm_r, p_shoulder_r,
                                             bulge=0.22, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_r, p_neck_r)]),
        fc.Edge("neck", [fc.curve_through(p_neck_r, p_neck_cb, bulge=0.30, side=-1.0)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": band_depth},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm"),
                 fc.Notch("armhole", 0.5, "armhole notch")],
        grainline=fc.Grainline(fc.P(Q_CHEST * 0.3, y_hem + 30.0),
                               fc.P(Q_CHEST * 0.3, y_shoulder - 30.0)),
        internals=[fc.Internal("cable panel centre",
                               [fc.P(Q_CHEST * 0.5, y_hem + band_depth),
                                fc.P(Q_CHEST * 0.5, y_underarm)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Back panel (cut 1)",
    )


_F = _front()
_B = _back()
ARMHOLE_LEN = _F.edge("armhole").length(0.05) + _B.edge("armhole").length(0.05)


def _armhole_band():
    """The ribbed armhole band: a rectangle, its length the MEASURED armhole opening, its
    width twice the band depth (folded)."""
    ln = ARMHOLE_LEN
    w = band_depth * 2.0
    return fc.Piece(
        "armhole_band", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "shoulder / underarm balance")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("rib fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Ribbed armhole band (cut 2)",
    )


def build():
    pattern = fc.PatternSet("cable-knit-vest")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_front())
    if everything or target_piece == "back":
        pattern.add(_back())
    if everything or target_piece == "armhole_band":
        pattern.add(_armhole_band())

    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.6)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=0.6)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "cabled wool knit yardage (or hand-knit to shape)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker; a cabled knit draws IN "
                 f"across its width, so the body carries a clamped positive ease."},
        {"item": "ribbing (2x2) for neck / armhole / hem bands", "qty": 1, "unit": "set",
         "note": "cut the armhole band to the measured opening; neck and hem bands to "
                 "their own edges."},
        {"item": "wool thread + ballpoint needle", "qty": 1, "unit": "spool",
         "note": "seam the shoulders and sides; set the ribbed bands with a slight "
                 "stretch so they hug."},
    ]
    pattern.metadata = {
        "fc500_rank": 404, "family": "knitwear", "tier": 2,
        "fabric_hint": "punto-lana",
        "silhouette_note": "A sleeveless cabled vest: V-neck front, round-neck back, ribbed "
            "neck / armhole / hem bands.",
        "solved": {
            "quarter_chest_mm": round(Q_CHEST, 1),
            "half_shoulder_clamped_mm": round(HALF_SHOULDER, 1),
            "v_depth_requested_mm": round(v_depth, 1),
            "v_depth_clamped_mm": round(V_DEPTH, 1),
            "v_was_clamped": bool(abs(V_DEPTH - v_depth) > 0.01),
            "armhole_band_measured_mm": round(ARMHOLE_LEN, 1),
            "note": "the front and back share one shoulder point and slope so the shoulder "
                    "seams sew flush; the V depth is clamped above the armhole depth so a "
                    "deep-V request never self-intersects the front; the shoulder tip is "
                    "clamped inside the body quarter; and the ribbed armhole band is cut to "
                    "the MEASURED front + back armhole opening.",
        },
        "hardware": "none — a pull-on cabled vest.",
    }
    return pattern


result = build()
