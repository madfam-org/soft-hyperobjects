"""
Racerback sports bra — Fashion Cabinet Garment Cartridge (FC-400 #388; lane 9, active_swim).

A pull-on compression sports bra in power-mesh: a front panel, a racerback back panel,
and a firm support band, held up by the band's negative ease rather than by a wire. A
sports bra is a COMPRESSION garment (it limits motion by holding the chest close) rather
than an encapsulation garment (which cups each breast separately), and this cartridge
drafts the compression kind honestly:

  1. THE SUPPORT IS THE BAND, NOT THE STRAPS. A sports bra's load is carried by a wide
     firm underband gripped at negative ease against the ribcage — the same principle as
     the underwire-bra's underband, but here it is the WHOLE support, because there is no
     wire. The band's finished ring is solved from the underbust girth and an explicit
     grip percentage, and it is printed, so "high support" is a number rather than an
     adjective.

  2. THE RACERBACK IS WHAT KEEPS THE STRAPS ON. The back panel narrows to a racer: the
     two straps converge to a single yoke between the shoulder blades. This is not
     styling — a racer geometry stops the straps sliding off the shoulders during motion,
     which is the failure mode a straight-strap bra has in sport. The convergence point
     is SOLVED from the shoulder width so the straps sit inboard of the shoulder points.

  3. THE FRONT COMPRESSES EVENLY. The front is a single panel (no cups) with a scooped
     neckline; the compression is distributed across it and reported as a finished
     chest ring, so it is not a concentrated squeeze.

Three pieces: front, racerback back, and the support band (cut as a doubled ring). No
hardware — it is pulled on over the head, and the straps are cut in one with the panels.
Made to measure to chest and underbust girths, plus the strap and band geometry.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth = float(PARAM(lambda: chest_girth, 940.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 380.0))
front_length = float(PARAM(lambda: front_length, 260.0))     # band top to neckline base
band_height = float(PARAM(lambda: band_height, 60.0))        # firm support band depth
strap_width = float(PARAM(lambda: strap_width, 45.0))        # wide compression strap
neck_scoop = float(PARAM(lambda: neck_scoop, 90.0))          # front neckline drop
racer_drop = float(PARAM(lambda: racer_drop, 120.0))         # yoke below the neck line
band_grip_pct = float(PARAM(lambda: band_grip_pct, 14.0))    # band negative ease
front_grip_pct = float(PARAM(lambda: front_grip_pct, 8.0))   # front compression
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(680.0, min(chest_girth, 1400.0))
underbust_girth = max(580.0, min(underbust_girth, 1250.0))
shoulder_width = max(280.0, min(shoulder_width, 540.0))
front_length = max(150.0, min(front_length, 420.0))
band_height = max(30.0, min(band_height, 120.0))
strap_width = max(20.0, min(strap_width, 80.0))
neck_scoop = max(30.0, min(neck_scoop, 200.0))
racer_drop = max(50.0, min(racer_drop, 260.0))
band_grip_pct = max(4.0, min(band_grip_pct, 24.0))
front_grip_pct = max(0.0, min(front_grip_pct, 18.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# neck scoop cannot cross the front panel
neck_scoop = min(neck_scoop, front_length - 40.0)

# ── THE BAND SOLVER (the support, expressed as a number) ─────────────────────
BAND_FIN = underbust_girth * (1.0 - band_grip_pct / 100.0)   # finished band ring
BAND_HALF = BAND_FIN / 2.0
CHEST_FIN = chest_girth * (1.0 - front_grip_pct / 100.0)     # finished chest ring
FRONT_HALF = CHEST_FIN / 2.0
BACK_HALF = CHEST_FIN / 2.0

# The racer convergence sits INBOARD of the shoulder points so the straps do not slide off.
# Solve the yoke half-width from the shoulder: the straps converge to a yoke a quarter of
# the shoulder width wide, centred.
YOKE_HALF = max(strap_width * 0.6, shoulder_width * 0.12)
# Strap inner edges start at the neckline; the shoulder seam sits at ~ a third of the panel.
SH_IN = min(shoulder_width / 2.0, FRONT_HALF * 0.85)


def build_front():
    """Front panel (cut 1), symmetric about centre. Band bottom to two shoulder straps.

    CCW: left side (up) -> left strap (up to shoulder) -> neckline scoop -> right strap
    -> right side (down) -> band bottom (across). The straps are cut in one with the panel.
    """
    w = FRONT_HALF
    cx = w / 2.0
    top = front_length
    strap_top = top + racer_drop * 0.3      # straps rise a little above the neck base
    sh_in = min(SH_IN, w * 0.9)
    strap_out = sh_in
    strap_inr = sh_in - strap_width
    edges = [
        fc.Edge("side_seam_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top - neck_scoop * 0.3))]),
        # left armscye scoop up to the left strap outer
        fc.Edge("armscye_l", [fc.Bezier(
            fc.P(0.0, top - neck_scoop * 0.3),
            fc.P(w * 0.08, top - neck_scoop * 0.1),
            fc.P(strap_out * 0.6, top - 6.0),
            fc.P(strap_out, top))]),
        fc.Edge("strap_l", [fc.Line(fc.P(strap_out, top), fc.P(strap_inr, strap_top))]),
        # neckline scoop between the two strap inners
        fc.Edge("neckline", [fc.Bezier(
            fc.P(strap_inr, strap_top),
            fc.P(cx - w * 0.06, top - neck_scoop),
            fc.P(cx + w * 0.06, top - neck_scoop),
            fc.P(w - strap_inr, strap_top))]),
        fc.Edge("strap_r", [fc.Line(fc.P(w - strap_inr, strap_top), fc.P(w - strap_out, top))]),
        fc.Edge("armscye_r", [fc.Bezier(
            fc.P(w - strap_out, top),
            fc.P(w - strap_out * 0.6, top - 6.0),
            fc.P(w - w * 0.08, top - neck_scoop * 0.1),
            fc.P(w, top - neck_scoop * 0.3))]),
        fc.Edge("side_seam_r", [fc.Line(fc.P(w, top - neck_scoop * 0.3), fc.P(w, 0.0))]),
        fc.Edge("band_join", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("apex line",
                             [fc.P(0.0, top * 0.55), fc.P(w, top * 0.55)], kind="marking")]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0, "armscye_l": 0.0, "armscye_r": 0.0,
                    "strap_l": 0.0, "strap_r": 0.0, "band_join": 0.0},
        notches=[fc.Notch("band_join", 0.5, "centre-front"),
                 fc.Notch("side_seam_r", 0.5, "apex line")],
        grainline=fc.Grainline(fc.P(cx, top * 0.15), fc.P(cx, top * 0.80)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="Front panel (cut 1, straps cut in one)",
    )


def build_back():
    """Racerback panel (cut 1), symmetric about centre. Band bottom to a converged yoke.

    CCW: left side (up) -> left armscye scoop toward centre -> up the left racer edge to
    the yoke -> across the yoke top -> down the right racer edge -> right armscye ->
    right side (down) -> band bottom (across). The two straps CONVERGE to a narrow yoke,
    which is what keeps them on the shoulders in motion.
    """
    w = BACK_HALF
    cx = w / 2.0
    top = front_length
    yoke_top = top + racer_drop
    edges = [
        fc.Edge("side_seam_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top - racer_drop * 0.3))]),
        # left armscye scoops UP and IN toward the racer
        fc.Edge("armscye_l", [fc.Bezier(
            fc.P(0.0, top - racer_drop * 0.3),
            fc.P(w * 0.12, top - racer_drop * 0.05),
            fc.P(cx - YOKE_HALF * 1.6, top - racer_drop * 0.35),
            fc.P(cx - YOKE_HALF, top))]),
        # left racer edge rises to the yoke
        fc.Edge("racer_l", [fc.Bezier(
            fc.P(cx - YOKE_HALF, top),
            fc.P(cx - YOKE_HALF * 0.9, top + racer_drop * 0.5),
            fc.P(cx - YOKE_HALF * 0.9, yoke_top - 6.0),
            fc.P(cx - YOKE_HALF, yoke_top))]),
        fc.Edge("yoke", [fc.Line(fc.P(cx - YOKE_HALF, yoke_top), fc.P(cx + YOKE_HALF, yoke_top))]),
        fc.Edge("racer_r", [fc.Bezier(
            fc.P(cx + YOKE_HALF, yoke_top),
            fc.P(cx + YOKE_HALF * 0.9, yoke_top - 6.0),
            fc.P(cx + YOKE_HALF * 0.9, top + racer_drop * 0.5),
            fc.P(cx + YOKE_HALF, top))]),
        fc.Edge("armscye_r", [fc.Bezier(
            fc.P(cx + YOKE_HALF, top),
            fc.P(cx + YOKE_HALF * 1.6, top - racer_drop * 0.35),
            fc.P(w - w * 0.12, top - racer_drop * 0.05),
            fc.P(w, top - racer_drop * 0.3))]),
        fc.Edge("side_seam_r", [fc.Line(fc.P(w, top - racer_drop * 0.3), fc.P(w, 0.0))]),
        fc.Edge("band_join", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"armscye_l": 0.0, "armscye_r": 0.0, "racer_l": 0.0, "racer_r": 0.0,
                    "yoke": 0.0, "band_join": 0.0},
        notches=[fc.Notch("band_join", 0.5, "centre-back"),
                 fc.Notch("yoke", 0.5, "racer centre")],
        grainline=fc.Grainline(fc.P(cx, top * 0.15), fc.P(cx, top * 0.75)),
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="Racerback panel (cut 1, straps converge to a yoke)",
    )


def build_band(front_join, back_join):
    """The firm support band: a wide ring cut at negative ease. Its top edge is built to
    the measured front+back band joins so the panels sit on the band with a balanced seam.

    Cut 1 long (front + back), closing at a side seam, doubled for firmness.
    """
    top_w = front_join + back_join            # one full ring's top edge
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(top_w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, band_height))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, band_height), fc.P(top_w, band_height))]),
        fc.Edge("side_b", [fc.Line(fc.P(top_w, band_height), fc.P(top_w, 0.0))]),
    ]
    return fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},            # elastic-finished lower edge
        notches=[fc.Notch("top", 0.25, "side seam match"),
                 fc.Notch("top", 0.75, "side seam match")],
        grainline=fc.Grainline(fc.P(top_w * 0.5, 6.0), fc.P(top_w * 0.5, band_height - 6.0)),
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="Support band (cut 1, doubled for firmness)",
    )


def build():
    pattern = fc.PatternSet("racerback-sports-bra")
    every = target_piece == "set"

    front = build_front()
    back = build_back()

    if not every:
        if target_piece == "band":
            pattern.add(build_band(front.edge("band_join").length(),
                                   back.edge("band_join").length()))
            return _finish(pattern, front, back)
        picked = {"front": front, "back": back}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    band = build_band(front.edge("band_join").length(), back.edge("band_join").length())
    for piece in (front, back, band):
        pattern.add(piece)
    # Side seams: front to back, both sides.
    pattern.declare_seam(("front", "side_seam_l"), ("back", "side_seam_l"), tol=1.5,
                         ease=(front.edge("side_seam_l").length()
                               - back.edge("side_seam_l").length()))
    pattern.declare_seam(("front", "side_seam_r"), ("back", "side_seam_r"), tol=1.5,
                         ease=(front.edge("side_seam_r").length()
                               - back.edge("side_seam_r").length()))
    # The straps: front strap tops attach to the racerback yoke region (topstitched flat
    # over the shoulder). Declared as the band-to-panels seam below; the strap-to-yoke
    # join is finished by topstitch, not a balanced seam, so it is not declared.
    # The band's top edge meets the assembled front+back band joins.
    pattern.declare_seam(("band", "top"),
                         [("front", "band_join"), ("back", "band_join")], tol=1.5)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    neck_opening = front.edge("neckline").length()
    arm_opening = 2.0 * (front.edge("armscye_r").length()
                         + back.edge("armscye_r").length())
    band_opening = 2.0 * BAND_HALF
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "power-mesh + supplex (compression, 4-way)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front + racerback + band at {fabric_width:.0f} mm width, 60% marker. The "
                 "band is the support — cut it on the firm recovery grain."},
        {"item": "band elastic (firm plush-back) 25-40 mm", "qty": round(band_opening * 0.86),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm ring x 0.86 — the band carries the load, "
                 "so it is cut short and stretched on. This is the support, not the straps."},
        {"item": "neckline + armscye binding (flat) 10-12 mm",
         "qty": round((neck_opening + arm_opening) * 0.9), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm + armscyes {arm_opening:.0f} mm at 0.9."},
        {"item": "polyester thread + ballpoint 70/10 + coverstitch", "qty": 1, "unit": "set",
         "note": "coverstitch the band and binding so seams stretch and lie flat in motion."},
    ]
    pattern.metadata = {
        "fc400_rank": 388, "family": "active_swim", "fabric_hint": "power-mesh",
        "silhouette_note": "A compression (not encapsulation) sports bra: single front "
            "panel, a converged racerback that keeps the straps on in motion, on a firm "
            "wide support band. No cups, no wire — the band's negative ease is the support.",
        "support_type": "compression",
        "solved": {
            "band_finished_mm": round(BAND_FIN, 1),
            "band_grip_pct": round(band_grip_pct, 1),
            "chest_finished_mm": round(CHEST_FIN, 1),
            "front_grip_pct": round(front_grip_pct, 1),
            "yoke_half_width_mm": round(YOKE_HALF, 1),
            "band_opening_mm": round(band_opening, 1),
            "note": "The band's finished ring is solved from the underbust and an explicit "
                    "grip percentage, so 'high support' is a number, not an adjective. The "
                    "racer yoke half-width is solved from the shoulder so the straps sit "
                    "inboard of the shoulder points and do not slide off.",
        },
        "hardware": "none — pulled on over the head; the straps are cut in one with the "
                    "panels and there is no adjuster or wire to bridge.",
        "drafting": "Made to measure to chest and underbust girths; the band and chest "
                    "finished rings are printed so the compression is auditable.",
    }
    return pattern


result = build()
