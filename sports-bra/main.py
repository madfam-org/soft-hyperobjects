"""
Sports Bra (compression) — FC-100 rank #12. Fashion Cabinet Garment Cartridge.

The commons' compression-style athletic bra: a no-hardware pullover that
supports by tensioning power-stretch against the body, NOT by encapsulating
each breast in a wired cup. Three shell pieces — a scoop FRONT and a RACERBACK
back (both cut on fold) plus a wide UNDERBAND — with an optional inner FRONT
LINING for a double layer of support.

The technique this cartridge teaches is negative ease with matched elastic
accounting (mirrors panties-bikini) laid over bound-edge tank construction
(mirrors tank-top):

  * Every girth-derived width is multiplied by NEG = 1 - negative_ease_pct/100,
    so the flat pattern is drafted SMALLER than the body and the fabric
    tensions to fit. Compression bras run a higher negative ease (~15-25%) than
    a soft bra because the power-stretch interlock recovers hard.
  * The shell tapers from the bust half-width down to the underbust half-width;
    the UNDERBAND top edge equals the summed shell lower edges BY CONSTRUCTION
    (both fold-cut halves), proven by a declared seam.
  * Shoulder and side seams balance by construction (equal-length edges).
  * Neckline, armholes and the underband hem are elastic/bound-finished
    (allowance 0, marked elastic zones); the BOM emits EXACT-MM elastic cut
    lengths derived from the measured openings — the numbers factories keep on
    private spec sheets. NO hardware: no wire, no hooks, no rings, no sliders —
    the pull-on is the whole point.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|underband|front_lining|set

chest_girth       = float(PARAM(lambda: chest_girth, 900.0))     # bust girth
underbust_girth   = float(PARAM(lambda: underbust_girth, 760.0))  # ribcage under bust
body_length       = float(PARAM(lambda: body_length, 260.0))     # underband hem to shoulder
band_height       = float(PARAM(lambda: band_height, 60.0))      # wide compression band
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 18.0))
neck_drop_front   = float(PARAM(lambda: neck_drop_front, 95.0))  # scoop depth, front
neck_drop_back    = float(PARAM(lambda: neck_drop_back, 40.0))   # racer sits high, back
strap_width       = float(PARAM(lambda: strap_width, 42.0))      # grown-on strap / shoulder
racer_pull_in     = float(PARAM(lambda: racer_pull_in, 55.0))    # how far the racer converges
neck_elastic_ratio = float(PARAM(lambda: neck_elastic_ratio, 0.88))
arm_elastic_ratio  = float(PARAM(lambda: arm_elastic_ratio, 0.85))
band_elastic_ratio = float(PARAM(lambda: band_elastic_ratio, 0.92))
seam_allowance    = float(PARAM(lambda: seam_allowance, 7.0))

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1500.0))
underbust_girth = max(550.0, min(underbust_girth, 1350.0))
body_length = max(180.0, min(body_length, 380.0))
band_height = max(35.0, min(band_height, 110.0))
negative_ease_pct = max(8.0, min(negative_ease_pct, 28.0))
neck_drop_front = max(40.0, min(neck_drop_front, 160.0))
neck_drop_back = max(10.0, min(neck_drop_back, 120.0))
strap_width = max(25.0, min(strap_width, 80.0))
racer_pull_in = max(10.0, min(racer_pull_in, 120.0))
neck_elastic_ratio = max(0.78, min(neck_elastic_ratio, 1.0))
arm_elastic_ratio = max(0.78, min(arm_elastic_ratio, 1.0))
band_elastic_ratio = max(0.82, min(band_elastic_ratio, 1.0))

# ── Derived geometry ─────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BUST_HALF = chest_girth * NEG / 4.0        # shell half-width at the bust (underarm line)
UB_HALF = underbust_girth * NEG / 4.0      # shell half-width at the underband seam
HPS_Y = body_length                        # shoulder / strap-top line
UNDERARM_Y = body_length - max(70.0, body_length * 0.42)  # bust/underarm line
BAND_HALF = underbust_girth * NEG / 2.0    # underband top length (fold-cut half)
ELASTIC_ZONE = 8.0                         # marked elastic application width (mm)

# Neck inner half-width: the front carries the strap at the shoulder; the racer
# back pulls the strap toward the spine by racer_pull_in but never past center.
NW_FRONT = max(45.0, BUST_HALF * 0.42)
NW_BACK = max(18.0, NW_FRONT - racer_pull_in)


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic-finished edge, ELASTIC_ZONE mm in.

    Edges are normalized CCW by the Piece constructor, so the inward normal at
    tangent t is (-t.y, t.x). The [t0, t1] window keeps the trace off corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts, kind="trace")


def _shell(name, neck_drop, nw, arm_bulge, label):
    """One fold-cut shell half: fold at CF/CB (x=0), tapering bust→underbust.

    The `side` and `band_join` edges are identical on front and back (same
    BUST_HALF / UB_HALF / heights), so the side and underband seams balance by
    construction; only the neck depth, strap inset (nw) and armhole scoop vary.
    """
    neck_top_y = HPS_Y - neck_drop
    strap_outer_x = nw + strap_width
    fold_bottom = fc.P(0.0, 0.0)
    underarm = fc.P(BUST_HALF, UNDERARM_Y)
    lower_outer = fc.P(UB_HALF, 0.0)

    center = fc.Edge("center", [fc.Line(fold_bottom, fc.P(0.0, neck_top_y))])
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(nw * 0.55, neck_top_y),
                   fc.P(nw, neck_top_y + neck_drop * 0.40), fc.P(nw, HPS_Y))],
    )
    # Grown-on strap top edge = the shoulder seam. Same length (strap_width)
    # front and back, so the shoulder seam balances by construction.
    shoulder = fc.Edge("shoulder",
                       [fc.Line(fc.P(nw, HPS_Y), fc.P(strap_outer_x, HPS_Y))])
    armhole = fc.Edge(
        "armhole",
        [fc.Bezier(fc.P(strap_outer_x, HPS_Y),
                   fc.P(strap_outer_x + arm_bulge, HPS_Y - (HPS_Y - UNDERARM_Y) * 0.5),
                   fc.P(BUST_HALF - 6.0, UNDERARM_Y + (HPS_Y - UNDERARM_Y) * 0.30),
                   underarm)],
    )
    side = fc.Edge("side", [fc.Line(underarm, lower_outer)])
    band_join = fc.Edge("band_join", [fc.Line(lower_outer, fold_bottom)])
    return fc.Piece(
        name,
        [center, neck, shoulder, armhole, side, band_join],
        seam_allowance=seam_allowance,
        allowances={"neck": 0.0, "armhole": 0.0},  # bound / elastic-finished
        notches=[fc.Notch("band_join", 0.5, "underband match")],
        grainline=fc.Grainline(fc.P(UB_HALF * 0.5, 20.0),
                               fc.P(UB_HALF * 0.5, HPS_Y - 30.0)),
        internals=[
            _elastic_zone(neck, "neck elastic zone", 0.06, 0.94),
            _elastic_zone(armhole, "armhole elastic zone", 0.06, 0.94),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    """Scoop-neck front: deeper neckline, straps at the shoulder point."""
    return _shell("front", neck_drop_front, NW_FRONT, 4.0, "Front (scoop)")


def build_back():
    """Racerback: sits high at center, straps converge toward the spine."""
    return _shell("back", neck_drop_back, NW_BACK, -10.0, "Back (racer)")


def build_front_lining():
    """Inner support layer: the front outline, cut on fold, understitched to
    the shell. A double front layer is the compression bra's support without
    wire; it is caught in the same side/underband seams (not separately sewn)."""
    lining = build_front()
    lining.name = "front_lining"
    lining.label = "Front Lining (inner support)"
    # Liner edges are all caught under the shell's finishes, never turned alone.
    lining.allowances = {"neck": 0.0, "armhole": 0.0, "side": 0.0, "band_join": 0.0}
    lining.internals = []
    lining.notches = []
    lining.cut = fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True)
    return lining


def build_underband(front, back):
    """Wide compression band, cut on fold. Top edge sews to the summed shell
    lower edges (front.band_join + back.band_join); bottom edge is the underband
    elastic hem. Drafted as a half so its top length matches the fold-cut
    halves by construction."""
    top_y = band_height
    bottom = fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(BAND_HALF, 0.0))])
    end_outer = fc.Edge("end_outer", [fc.Line(fc.P(BAND_HALF, 0.0), fc.P(BAND_HALF, top_y))])
    top = fc.Edge("top", [fc.Line(fc.P(BAND_HALF, top_y), fc.P(0.0, top_y))])
    center = fc.Edge("center", [fc.Line(fc.P(0.0, top_y), fc.P(0.0, 0.0))])
    return fc.Piece(
        "underband",
        [bottom, end_outer, top, center],
        seam_allowance=seam_allowance,
        allowances={"bottom": 0.0},  # elastic-finished hem
        notches=[fc.Notch("top", 0.5, "shell match")],
        grainline=fc.Grainline(fc.P(BAND_HALF * 0.5, top_y * 0.25),
                               fc.P(BAND_HALF * 0.5, top_y * 0.75)),
        internals=[_elastic_zone(bottom, "underband elastic zone", 0.06, 0.94)],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Underband (compression)",
    )


def build():
    pattern = fc.PatternSet("sports-bra")
    front = build_front()
    back = build_back()
    underband = build_underband(front, back)
    lining = build_front_lining()
    picked = {
        "front": front,
        "back": back,
        "underband": underband,
        "front_lining": lining,
    }
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (front, back, underband, lining):
            pattern.add(piece)
        # Grown-on straps meet at the shoulder; equal-length top edges.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # Side seams; identical shell side edges front/back.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # Underband top sews to the summed shell lower edges (both fold halves).
        pattern.declare_seam(
            ("underband", "top"),
            [("front", "band_join"), ("back", "band_join")],
            tol=1.0,
        )

    # ── Elastic accounting (the honest, factory-grade detail) ────────────────
    # Openings are the full-body finished openings: each fold-cut edge is a half,
    # front + back together make half the body, so double for the full ring.
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    band_opening = 2.0 * (front.edge("band_join").length()
                          + back.edge("band_join").length())
    armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()  # per arm
    neck_elastic = round(neck_opening * neck_elastic_ratio)
    band_elastic = round(band_opening * band_elastic_ratio)
    arm_elastic = round(armhole_opening * arm_elastic_ratio)                          # per arm

    fabric_width = 1550.0  # poliester-elastano-compresion card width
    area = sum(p.area() * p.cut.quantity * 2.0 for p in (front, back, underband, lining))
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "poliester-elastano-compresion", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"shell (front+back) + underband + front lining at {fabric_width:.0f} mm "
                 "width, 62% marker efficiency; greatest stretch weft (around the body)"},
        {"item": "underband elastic (wide, plush-back)", "qty": band_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm underband opening x {band_elastic_ratio:.2f}; "
                 f"cut {band_height:.0f} mm wide, join in a ring, quarter-mark, coverstitch"},
        {"item": "neckline elastic/binding", "qty": neck_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {neck_opening:.0f} mm neckline opening x {neck_elastic_ratio:.2f}; "
                 "zigzag or coverstitch into the marked neck zone"},
        {"item": "armhole elastic/binding", "qty": 2 * arm_elastic,
         "unit": "mm_length",
         "note": f"two armholes x {arm_elastic} mm each ({armhole_opening:.0f} mm opening x "
                 f"{arm_elastic_ratio:.2f}); the grown-on straps are self-fabric, no sliders"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; flatlock/coverstitch every seam to avoid chafe"},
        {"item": "hardware", "qty": 0, "unit": "none",
         "note": "NONE by design — no wire, hooks, rings or sliders. A compression "
                 "pull-on; any optional bra hardware would be a Yantra4D notion "
                 "cartridge referenced via notion.hardware_ref, never drafted here"},
    ]
    pattern.metadata = {
        "fc100_rank": 12,
        "fabric_hint": "poliester-elastano-compresion",
        "support_style": "compression (pull-on) — NOT encapsulation; no cups, no wire, "
                         "no hooks. This is the honest compression teaching draft; a "
                         "wired/molded-cup encapsulation bra is a separate future cartridge.",
        "stretch_note": "cut with greatest stretch weft (around the body); high-recovery "
                        "power-stretch interlock",
        "negative_ease_pct": negative_ease_pct,
        "bust_half_mm": round(BUST_HALF, 1),
        "underbust_half_mm": round(UB_HALF, 1),
        "underband_half_mm": round(BAND_HALF, 1),
        "neck_opening_mm": round(neck_opening, 1),
        "neck_elastic_mm": neck_elastic,
        "armhole_opening_each_mm": round(armhole_opening, 1),
        "armhole_elastic_each_mm": arm_elastic,
        "underband_opening_mm": round(band_opening, 1),
        "underband_elastic_mm": band_elastic,
        "drafting": "compression sports bra: fold-cut scoop front + racerback back "
                    "tapering bust->underbust, wide underband matching the shell lower "
                    "edges by construction; neck/armhole/underband elastic cut lengths "
                    "derived exactly from the measured openings; optional front lining "
                    "understitched for a double support layer; no hardware.",
    }
    return pattern


result = build()
