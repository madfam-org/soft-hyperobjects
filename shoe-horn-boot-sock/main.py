"""
Shoe-horn boot sock — Fashion Cabinet Cartridge (FC-500 #427, footwear_soft, T2).

A tall knit boot sock with an integrated HEEL HORN: a stiffened fabric channel at the back
heel that holds a slim printed shoe-horn (the Yantra4D `shoe-horn`) so the heel slides into a
tight boot without crushing the sock's back or bruising the achilles. The sock is a two-panel
stretch tube (a LEG panel and a FOOT panel) with the horn CHANNEL sewn up the back heel.

Solved, not guessed:

  1. THE HORN CHANNEL IS CUT TO THE MEASURED SHOE-HORN. The channel length is the horn length
     plus a seat, and its width is the horn scoop width plus a clearance — so the horn slides
     in and stays put.
  2. NEGATIVE EASE IS FLOORED. The tube panel widths carry a stretch factor below 1.0, floored
     so a tight sock never draws a hairline panel.
  3. THE FOOT AND LEG PANELS JOIN AT A MEASURED ANKLE SEAM — the foot panel's ankle edge is
     drafted to the leg panel's lower edge so the tube is continuous.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # leg|foot|channel|set

calf_girth = float(PARAM(lambda: calf_girth, 360.0))
ankle_girth = float(PARAM(lambda: ankle_girth, 240.0))
foot_length = float(PARAM(lambda: foot_length, 260.0))
leg_height = float(PARAM(lambda: leg_height, 300.0))
horn_length = float(PARAM(lambda: horn_length, 140.0))
horn_scoop = float(PARAM(lambda: horn_scoop, 45.0))
stretch_factor = float(PARAM(lambda: stretch_factor, 0.85))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

calf_girth = max(240.0, min(calf_girth, 520.0))
ankle_girth = max(160.0, min(ankle_girth, 340.0))
foot_length = max(180.0, min(foot_length, 340.0))
leg_height = max(180.0, min(leg_height, 480.0))
horn_length = max(80.0, min(horn_length, 220.0))
horn_scoop = max(25.0, min(horn_scoop, 80.0))
stretch_factor = max(0.66, min(stretch_factor, 0.98))
seam_allowance = max(0.0, min(seam_allowance, 14.0))

HALF_CALF = max(60.0, calf_girth / 2.0 * stretch_factor)
HALF_ANKLE = max(40.0, ankle_girth / 2.0 * stretch_factor)
CHANNEL_L = horn_length + 20.0
CHANNEL_W = horn_scoop + 12.0


def build_leg():
    """The leg tube panel (cut 2 mirrored, or 1 folded). A tapered panel: calf at top, ankle
    at the bottom."""
    h = leg_height
    p_bl = fc.P(-HALF_ANKLE, 0.0)
    p_br = fc.P(HALF_ANKLE, 0.0)
    p_tr = fc.P(HALF_CALF, h)
    p_tl = fc.P(-HALF_CALF, h)
    return fc.Piece(
        "leg", [
            fc.Edge("ankle", [fc.Line(p_bl, p_br)]),
            fc.Edge("seam_r", [fc.curve_through(p_br, p_tr, bulge=0.04, side=1.0)]),
            fc.Edge("cuff", [fc.Line(p_tr, p_tl)]),
            fc.Edge("seam_l", [fc.curve_through(p_tl, p_bl, bulge=0.04, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cuff": 30.0},
        notches=[fc.Notch("ankle", 0.5, "CB"), fc.Notch("cuff", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(0.0, 15.0), fc.P(0.0, h - 15.0)),
        internals=[fc.Internal("horn channel top",
                               [fc.P(-CHANNEL_W / 2.0, 10.0),
                                fc.P(CHANNEL_W / 2.0, 10.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Leg panel (cut 2, mirrored)",
    )


def build_foot():
    """The foot panel (cut 2 mirrored). Ankle edge at top (matching the leg ankle), a toe at
    the far end and a sole/instep curve."""
    Lf = foot_length
    p_ankle_l = fc.P(-HALF_ANKLE, Lf)
    p_ankle_r = fc.P(HALF_ANKLE, Lf)
    p_toe_r = fc.P(HALF_ANKLE * 0.5, 0.0)
    p_toe_l = fc.P(-HALF_ANKLE * 0.5, 0.0)
    return fc.Piece(
        "foot", [
            fc.Edge("ankle", [fc.Line(p_ankle_l, p_ankle_r)]),
            fc.Edge("instep", [fc.curve_through(p_ankle_r, p_toe_r, bulge=0.10, side=1.0)]),
            fc.Edge("toe", [fc.curve_through(p_toe_r, p_toe_l, bulge=0.30, side=1.0)]),
            fc.Edge("sole", [fc.curve_through(p_toe_l, p_ankle_l, bulge=0.10, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("ankle", 0.5, "CB"), fc.Notch("toe", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 15.0), fc.P(0.0, Lf - 15.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Foot panel (cut 2, mirrored)",
    )


def build_channel():
    """The horn channel, cut 1. A stiffened strip sewn up the back heel that holds the
    printed shoe-horn."""
    w, h = CHANNEL_W, CHANNEL_L
    return fc.Piece(
        "channel", [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": 12.0},
        notches=[fc.Notch("bottom", 0.5, "heel base")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=[fc.Internal("horn slot",
                               [fc.P(w * 0.5, h - 6.0), fc.P(w * 0.5, 6.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Heel horn channel (cut 1)",
    )


def build():
    pattern = fc.PatternSet("shoe-horn-boot-sock")
    everything = target_piece == "set"
    leg = build_leg()
    foot = build_foot()
    if everything or target_piece == "leg":
        pattern.add(leg)
    if everything or target_piece == "foot":
        pattern.add(foot)
    if everything or target_piece == "channel":
        pattern.add(build_channel())

    if everything:
        # the foot ankle edge sews to the leg ankle edge (both = ankle girth panel width)
        pattern.declare_seam(("foot", "ankle"), ("leg", "ankle"), tol=0.8)
        pattern.declare_seam(("leg", "seam_r"), ("leg", "seam_l"), tol=1.5)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "wool/nylon rib knit (sock)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a stretch rib with NEGATIVE "
                 f"ease (factor {stretch_factor:.2f}) so the sock grips the calf."},
        {"item": "printed shoe-horn", "qty": 1, "unit": "count",
         "note": f"Yantra4D shoe-horn (notion.hardware_ref) at {horn_length:.0f} mm; slides "
                 f"into the heel channel to guide the heel into a tight boot."},
        {"item": "channel stiffener + thread", "qty": 1, "unit": "set",
         "note": "a light stiffener holds the channel open; ballpoint needle for the knit."},
    ]
    pattern.metadata = {
        "fc500_rank": 427, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "punto-lana",
        "silhouette_note": "A tall knit boot sock with a heel channel holding a printed "
            "shoe-horn to guide the heel into a tight boot.",
        "solved": {
            "half_calf_mm": round(HALF_CALF, 1),
            "half_ankle_mm": round(HALF_ANKLE, 1),
            "channel_mm": [round(CHANNEL_W, 1), round(CHANNEL_L, 1)],
            "note": "the horn channel is cut to the MEASURED shoe-horn length + seat and "
                    "scoop + clearance; the tube panel widths carry a stretch factor floored "
                    "at 0.66 so a tight sock never draws a hairline; the foot ankle is drafted "
                    "to the leg ankle so the tube is continuous.",
        },
        "hardware": "shoe-horn via Yantra4D (notion.hardware_ref -> shoe-horn); horn_len and "
                    "scoop_w are fed from the horn. No flange interface — the horn slides into "
                    "the sock channel, no seam handshake owed.",
    }
    return pattern


result = build()
