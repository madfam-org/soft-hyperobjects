"""
Kimono-wrap baby bodysuit — Fashion Cabinet Garment Cartridge (FC-500 #407, kids_baby, T1).

The newborn bodysuit that wraps like a kimono — left front crosses over right and fastens
with sew-on snaps down the side, so it goes on WITHOUT pulling anything over a newborn's
head (the reason side-snap kimono bodies exist). A right FRONT and an overlapping left
FRONT, a BACK, short kimono SLEEVES cut in one with the body, and a snap crotch gusset.

Solved, not guessed:

  1. THE WRAP OVERLAP IS A REAL, CLAMPED EXTENSION. The left front carries an overlap panel
     added to its width; the overlap is clamped so it can neither vanish (nothing to snap)
     nor exceed the body half-width (the wrap would pass centre and gape). Added cloth, not
     stolen.
  2. THE SHOULDER AND SIDE SEAMS MATCH. Front and back share one shoulder slope so the
     kimono shoulder sews flush; the side/underarm runs are drafted equal.
  3. THE SNAP RUN SITS ON CLOTH. Each snap is stepped in off the finished wrap edge by its
     own disc plus clearance, so it seats on fabric, not on the turned edge.

The snaps bridge to the Yantra4D `sew-on-snap` solid.

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
# front_right|front_left|back|sleeve|gusset|set

chest_girth = float(PARAM(lambda: chest_girth, 480.0))     # baby chest
body_length = float(PARAM(lambda: body_length, 340.0))     # shoulder to crotch
shoulder_width = float(PARAM(lambda: shoulder_width, 200.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 120.0))
neck_width = float(PARAM(lambda: neck_width, 110.0))
overlap = float(PARAM(lambda: overlap, 70.0))              # kimono wrap overlap
snap_disc = float(PARAM(lambda: snap_disc, 10.0))          # drives sew-on-snap disc
ease = float(PARAM(lambda: ease, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

chest_girth = max(360.0, min(chest_girth, 620.0))
body_length = max(240.0, min(body_length, 460.0))
shoulder_width = max(140.0, min(shoulder_width, 280.0))
sleeve_length = max(60.0, min(sleeve_length, 220.0))
neck_width = max(80.0, min(neck_width, 160.0))
overlap = max(30.0, min(overlap, 140.0))
snap_disc = max(6.0, min(snap_disc, 16.0))
ease = max(20.0, min(ease, 160.0))
seam_allowance = max(0.0, min(seam_allowance, 14.0))

Q_CHEST = max(shoulder_width / 2.0 * 0.7, (chest_girth + ease) / 4.0)
HALF_NECK = neck_width / 2.0
HALF_SHOULDER = min(shoulder_width / 2.0, Q_CHEST + 20.0)
# The wrap overlap is clamped so it never vanishes nor passes the centre.
OVERLAP = max(snap_disc * 2.0 + 8.0, min(overlap, Q_CHEST * 0.75))
ARM = max(40.0, sleeve_length)


def _kimono_body(name, is_left, is_back):
    """One body panel with the sleeve cut in one. x=0 at CF (or CB), +x to the side/sleeve.
    y=0 at the crotch, +y up to the shoulder. The kimono sleeve extends out at the shoulder.
    The left front adds an overlap panel past CF."""
    ext = OVERLAP if is_left else 0.0
    y_crotch = 0.0
    y_underarm = body_length * 0.52
    y_shoulder = body_length
    x_cf = -ext
    p_crotch_cf = fc.P(x_cf, y_crotch)
    p_crotch_side = fc.P(Q_CHEST, y_crotch)
    p_underarm = fc.P(Q_CHEST, y_underarm)
    p_sleeve_end_low = fc.P(Q_CHEST + ARM, y_underarm + 6.0)
    p_sleeve_end_high = fc.P(Q_CHEST + ARM, y_shoulder - 6.0)
    p_shoulder = fc.P(HALF_SHOULDER, y_shoulder)
    p_neck = fc.P(HALF_NECK, y_shoulder)
    if is_back:
        p_neck_cf = fc.P(x_cf, y_shoulder - 14.0)
    else:
        # front neck dips lower and, for the left, the wrap runs down to the crotch overlap
        p_neck_cf = fc.P(x_cf, y_shoulder - (40.0 if not is_left else 20.0))
    edges = [
        fc.Edge("crotch", [fc.Line(p_crotch_cf, p_crotch_side)]),
        fc.Edge("side", [fc.Line(p_crotch_side, p_underarm)]),
        fc.Edge("sleeve_seam", [fc.Line(p_underarm, p_sleeve_end_low)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end_low, p_sleeve_end_high)]),
        fc.Edge("sleeve_top", [fc.Line(p_sleeve_end_high, p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.curve_through(p_neck, p_neck_cf, bulge=0.20, side=-1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_crotch_cf)]),
    ]
    internals = []
    if is_left:
        a = max(3.0, snap_disc * 0.6)
        for i in range(3):
            sy = y_underarm - 10.0 - i * ((y_underarm - 30.0) / 3.0)
            sx = -ext + snap_disc + 6.0     # stepped in off the wrap edge
            internals.append(fc.Internal(f"snap-{i + 1}",
                             [fc.P(sx - a, sy), fc.P(sx + a, sy), fc.P(sx, sy),
                              fc.P(sx, sy - a), fc.P(sx, sy + a)], kind="drill"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"crotch": 0.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(Q_CHEST * 0.35, 20.0),
                               fc.P(Q_CHEST * 0.35, y_shoulder - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label=name.replace("_", " ").title(),
    )


def build_front_right():
    return _kimono_body("front_right", is_left=False, is_back=False)


def build_front_left():
    return _kimono_body("front_left", is_left=True, is_back=False)


def build_back():
    return _kimono_body("back", is_left=False, is_back=True)


def build_gusset():
    """The snap crotch gusset, cut 1. A short bridge between the front and back crotch
    edges, snapped so a diaper can be changed without undressing."""
    w = max(70.0, Q_CHEST * 0.8)
    h = max(60.0, body_length * 0.22)
    a = max(3.0, snap_disc * 0.6)
    edges = [
        fc.Edge("front_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w * 0.85, h))]),
        fc.Edge("back_edge", [fc.Line(fc.P(w * 0.85, h), fc.P(w * 0.15, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(w * 0.15, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "gusset", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "CF")],
        grainline=fc.Grainline(fc.P(w * 0.5, 6.0), fc.P(w * 0.5, h - 6.0)),
        internals=[
            fc.Internal("snap L", [fc.P(w * 0.2 - a, h * 0.5), fc.P(w * 0.2 + a, h * 0.5),
                                   fc.P(w * 0.2, h * 0.5),
                                   fc.P(w * 0.2, h * 0.5 - a),
                                   fc.P(w * 0.2, h * 0.5 + a)], kind="drill"),
            fc.Internal("snap R", [fc.P(w * 0.8 - a, h * 0.5), fc.P(w * 0.8 + a, h * 0.5),
                                   fc.P(w * 0.8, h * 0.5),
                                   fc.P(w * 0.8, h * 0.5 - a),
                                   fc.P(w * 0.8, h * 0.5 + a)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Snap crotch gusset (cut 1)",
    )


def build():
    pattern = fc.PatternSet("baby-kimono-bodysuit")
    everything = target_piece == "set"
    want = {
        "front_right": everything or target_piece == "front_right",
        "front_left": everything or target_piece == "front_left",
        "back": everything or target_piece == "back",
        "gusset": everything or target_piece == "gusset",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_right"]:
        pattern.add(build_front_right())
    if want["front_left"]:
        pattern.add(build_front_left())
    if want["back"]:
        pattern.add(build_back())
    if want["gusset"]:
        pattern.add(build_gusset())

    if want["front_right"] and want["back"]:
        pattern.declare_seam(("front_right", "shoulder"), ("back", "shoulder"), tol=0.6)
        pattern.declare_seam(("front_right", "side"), ("back", "side"), tol=0.6)
        pattern.declare_seam(("front_right", "sleeve_seam"),
                             ("back", "sleeve_seam"), tol=0.6)
    if want["front_left"] and want["back"]:
        # the left front's shoulder and side seams match the back's (the overlap only adds
        # cloth at CF, not at the shoulder or side).
        pattern.declare_seam(("front_left", "shoulder"), ("back", "shoulder"), tol=0.6)
        pattern.declare_seam(("front_left", "side"), ("back", "side"), tol=0.6)
        pattern.declare_seam(("front_left", "sleeve_seam"),
                             ("back", "sleeve_seam"), tol=0.6)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton interlock / jersey (baby-safe)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a soft interlock with a "
                 f"flat neck binding and no scratchy seams."},
        {"item": "sew-on snaps", "qty": 5, "unit": "count",
         "note": f"Yantra4D sew-on-snap (notion.hardware_ref) at a {snap_disc:.0f} mm disc; "
                 f"the side wrap run (3) + the crotch gusset (2), each stepped in off the "
                 f"finished edge so it seats on cloth."},
        {"item": "soft thread + ballpoint needle", "qty": 1, "unit": "spool",
         "note": "flatlock the wrap edges so nothing rubs a newborn's skin."},
    ]
    pattern.metadata = {
        "fc500_rank": 407, "family": "kids_baby", "tier": 1,
        "fabric_hint": "jersey-algodon",
        "silhouette_note": "A side-snap kimono-wrap newborn bodysuit — goes on without "
            "pulling anything over the head; kimono sleeves cut in one, snap crotch gusset.",
        "solved": {
            "quarter_chest_mm": round(Q_CHEST, 1),
            "overlap_requested_mm": round(overlap, 1),
            "overlap_clamped_mm": round(OVERLAP, 1),
            "overlap_was_clamped": bool(abs(OVERLAP - overlap) > 0.01),
            "note": "the wrap overlap is a real added extension, clamped so it neither "
                    "vanishes (nothing to snap) nor passes the centre (a gaping wrap); the "
                    "shoulder and side seams are drafted equal; and each snap is stepped in "
                    "off the finished wrap edge so it seats on cloth.",
        },
        "hardware": "sew-on snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); the "
                    "disc thickness, stud and engagement clearance are fed from snap_disc "
                    "(the sew-face params are left unmapped — the snap seats through the "
                    "cloth face, no seam handshake owed).",
    }
    return pattern


result = build()
