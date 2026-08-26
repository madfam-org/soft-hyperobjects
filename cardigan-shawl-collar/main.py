"""
Shawl-collar cardigan — FC-400 rank #333, Lane 4 (knitwear). Fashion Cabinet Cartridge.

A cardigan opens down the centre front, and the shawl collar is the feature: a single
continuous collar-and-lapel that rolls from the back neck down both fronts to the hem of
the button placket, with no seam at the shoulder break. It is the knitter's soft-tailored
cardigan — a drop-shoulder body (as the Aran) with a button band up each front and a
shawl collar drafted as one long strip that is eased around the neckline.

What this cartridge owns:
  - THE FRONT (cut 2, mirrored — a cardigan is NOT cut on the fold; it opens) with a
    button-band extension, a drop-shoulder armhole, and a neckline the shawl rolls onto.
  - THE BACK (cut on fold), the drop-shoulder SLEEVE, the CUFFS and HEM rib.
  - THE SHAWL COLLAR as a long strip whose sewn edge equals the full neckline run
    (both front necklines + the back neck) so the collar seam balances by construction.
  - BUTTONHOLES marked up one front band; the buttons bridge to Yantra4D shank-button.

Solving and clamps. The shoulder run is derived (quarter width less half neck width) and
FLOORED — a wide neck on a narrow body would drive it to zero or negative and invert the
yoke after CCW normalization. The button-band width is added OUTSIDE the centre front, so
the two fronts overlap by two band widths when closed. The collar strip length is SOLVED
from the measured neckline (front necks + back neck), floored so it can never go negative.
Knit ease is signed and defaults slightly positive here (a cardigan is worn over other
layers).

Hardware: Yantra4D `shank-button-solid` (point hardware; buttonholes are marked, the
button is set through, no sewn edge — no dimensional handshake owed).

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|cuff|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
body_length = float(PARAM(lambda: body_length, 640.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
knit_ease = float(PARAM(lambda: knit_ease, 40.0))           # SIGNED; positive default (over-layer)
armhole_depth = float(PARAM(lambda: armhole_depth, 250.0))
front_neck_drop = float(PARAM(lambda: front_neck_drop, 120.0))  # cardigans open low
shoulder_slope = float(PARAM(lambda: shoulder_slope, 22.0))
band_width = float(PARAM(lambda: band_width, 32.0))         # button band width
collar_width = float(PARAM(lambda: collar_width, 90.0))     # finished shawl width at back
button_count = int(PARAM(lambda: button_count, 6))
button_dia = float(PARAM(lambda: button_dia, 18.0))     # button dia (drives buttonhole)
cuff_ratio = float(PARAM(lambda: cuff_ratio, 0.72))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.92))
rib_height = float(PARAM(lambda: rib_height, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(440.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(320.0, min(sleeve_length, 780.0))
knit_ease = max(-100.0, min(knit_ease, 220.0))
armhole_depth = max(170.0, min(armhole_depth, 380.0))
front_neck_drop = max(60.0, min(front_neck_drop, 260.0))
shoulder_slope = max(5.0, min(shoulder_slope, 55.0))
band_width = max(18.0, min(band_width, 60.0))
collar_width = max(50.0, min(collar_width, 160.0))
button_count = max(3, min(button_count, 12))
button_dia = max(9.0, min(button_dia, 40.0))
cuff_ratio = max(0.50, min(cuff_ratio, 0.95))
hemband_ratio = max(0.72, min(hemband_ratio, 1.0))
rib_height = max(30.0, min(rib_height, 120.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))

DRAFT_GIRTH = max(560.0, chest_girth + knit_ease)
W = DRAFT_GIRTH / 4.0                              # quarter body (back half-width)
L = body_length
NW = max(48.0, min(neck_girth / 5.0 + 4.0, W - 60.0))   # half neck width
BACK_NECK_DROP = 24.0
UNDERARM_Y = max(60.0, L - armhole_depth)
SLOPE = max(2.0, min(shoulder_slope, armhole_depth * 0.45))
SHOULDER_PT_Y = L - SLOPE
_shoulder_run_raw = W - NW
SHOULDER_RUN = max(45.0, _shoulder_run_raw)
SHOULDER_RUN_CLAMPED = _shoulder_run_raw < 45.0


def _rib(name, finished_len, finished_height, qty, label):
    band_h = max(20.0, 2.0 * finished_height)
    length = max(80.0, finished_len) + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build_front():
    """A cardigan front, cut 2 mirrored. Centre-front at x=0 with a button-band
    extension of band_width to the LEFT (negative x). Drop-shoulder armhole to the
    right. Buttonholes marked up the band."""
    neck_top_y = SHOULDER_PT_Y
    neck_low_y = SHOULDER_PT_Y - front_neck_drop
    neck_low_y = max(80.0, neck_low_y)                  # never below the hem region
    neck_pt = fc.P(NW, neck_top_y)
    shoulder_pt = fc.P(W, SHOULDER_PT_Y)
    x_band = -band_width                                # button band outer edge
    internals = [
        fc.Internal("centre front", [fc.P(0.0, 0.0), fc.P(0.0, neck_low_y)],
                    kind="marking"),
        fc.Internal("underarm", [fc.P(x_band, UNDERARM_Y), fc.P(W, UNDERARM_Y)],
                    kind="marking"),
    ]
    # Buttonhole ladder up the band, between the hem and the neck break.
    top_bh = min(neck_low_y - 20.0, UNDERARM_Y + 40.0)
    for i in range(button_count):
        t = (i + 0.5) / button_count
        y = 30.0 + (top_bh - 30.0) * t
        bh = button_dia / 2.0 + 2.0                     # buttonhole slit half-length
        internals.append(fc.Internal(f"buttonhole {i + 1}",
                                     [fc.P(-band_width * 0.5 - bh, y),
                                      fc.P(-band_width * 0.5 + bh, y)], kind="drill"))
    return fc.Piece(
        "front",
        [
            # hem: from band outer edge across to the side
            fc.Edge("hem", [fc.Line(fc.P(x_band, 0.0), fc.P(W, 0.0))]),
            fc.Edge("side", [fc.Line(fc.P(W, 0.0), fc.P(W, UNDERARM_Y))]),
            fc.Edge("armhole", [fc.Line(fc.P(W, UNDERARM_Y), shoulder_pt)]),
            fc.Edge("shoulder", [fc.Line(shoulder_pt, neck_pt)]),
            # neckline: from the neck point down to the centre-front break at neck_low
            fc.Edge("neck", [fc.curve_through(neck_pt, fc.P(0.0, neck_low_y),
                                              bulge=0.14, side=1.0)]),
            # front placket edge: across to the band outer edge, then down the band to
            # the hem start — the button band is added OUTSIDE the centre front.
            fc.Edge("front_edge",
                    [fc.Line(fc.P(0.0, neck_low_y), fc.P(x_band, neck_low_y)),
                     fc.Line(fc.P(x_band, neck_low_y), fc.P(x_band, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(W * 0.4, 40.0), fc.P(W * 0.4, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (with button band)",
    )


def build_back():
    neck_top_y = SHOULDER_PT_Y
    neck_low_y = SHOULDER_PT_Y - BACK_NECK_DROP
    neck_pt = fc.P(NW, neck_top_y)
    shoulder_pt = fc.P(W, SHOULDER_PT_Y)
    internals = [
        fc.Internal("underarm", [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_low_y))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, neck_low_y), neck_pt,
                                              bulge=0.12, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            fc.Edge("armhole", [fc.Line(shoulder_pt, fc.P(W, UNDERARM_Y))]),
            fc.Edge("side", [fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(W * 0.5, 40.0), fc.P(W * 0.5, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (cut on fold)",
    )


def build_sleeve(armhole_len):
    bicep_half = max(90.0, W * 0.66)
    HEAD_RISE = max(30.0, min(armhole_depth * 0.18, 90.0))
    ul = max(120.0, sleeve_length - HEAD_RISE)
    y_ua = ul
    HEAD_HALF_MIN = 30.0
    dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    if dx2 <= 1.0:
        HEAD_RISE = max(10.0, armhole_len * 0.4)
        dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    head_dx = dx2 ** 0.5
    bicep_half = max(bicep_half, head_dx + HEAD_HALF_MIN)
    cuff_half = max(50.0, min(bicep_half * cuff_ratio, bicep_half - 12.0))
    head_x = bicep_half - head_dx
    top_y = y_ua + HEAD_RISE
    front_top = fc.P(-head_x, top_y)
    back_top = fc.P(head_x, top_y)
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-cuff_half, 0.0), fc.P(cuff_half, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(cuff_half, 0.0), fc.P(bicep_half, y_ua))]),
            fc.Edge("head_back", [fc.Line(fc.P(bicep_half, y_ua), back_top)]),
            fc.Edge("crown", [fc.curve_through(back_top, front_top, bulge=0.05, side=1.0)]),
            fc.Edge("head_front", [fc.Line(front_top, fc.P(-bicep_half, y_ua))]),
            fc.Edge("underarm_front", [fc.Line(fc.P(-bicep_half, y_ua), fc.P(-cuff_half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("head_front", 0.5, "front armhole match"),
                 fc.Notch("head_back", 0.5, "back armhole match"),
                 fc.Notch("crown", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, y_ua * 0.85)),
        internals=[fc.Internal("sleeve biceps line",
                               [fc.P(-bicep_half, y_ua), fc.P(bicep_half, y_ua)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (drop-shoulder)",
    )


def build_collar(neck_run):
    """The shawl collar: one long strip, cut 2 mirrored, whose inner (sewn) edge equals
    the full neckline run so the collar seam balances. Drafted as a rectangle of length
    = neck_run and height = collar_width, rolled and eased in construction."""
    length = max(120.0, neck_run)
    h = collar_width
    return fc.Piece(
        "collar",
        [
            fc.Edge("neck_seam", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
            fc.Edge("outer", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_seam", 0.5, "centre back neck")],
        grainline=fc.Grainline(fc.P(length * 0.5, h * 0.2), fc.P(length * 0.5, h * 0.8)),
        internals=[fc.Internal("roll line",
                               [fc.P(0.0, h * 0.45), fc.P(length, h * 0.45)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shawl collar",
    )


def build():
    pattern = fc.PatternSet("cardigan-shawl-collar")
    front = build_front()
    back = build_back()
    armhole_len = front.edge("armhole").length(0.05)
    sleeve = build_sleeve(armhole_len)
    # neckline run: both front necks + the back neck (front neck counted for both fronts)
    front_neck = front.edge("neck").length(0.05)
    back_neck = back.edge("neck").length(0.05)
    # Full neckline: both fronts (2×front_neck) + full back neck (back is on fold -> 2×).
    neck_run = 2.0 * front_neck + 2.0 * back_neck
    # The shawl collar is cut in TWO mirrored halves meeting at centre back, so each
    # strip covers HALF the neckline.
    collar = build_collar(neck_run / 2.0)

    names = ("front", "back", "sleeve", "collar", "cuff", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["collar"]:
        pattern.add(collar)

    hem_circ = 2.0 * (front.edge("hem").length(0.05)) + 2.0 * back.edge("hem").length(0.05)
    cuff_circ = sleeve.edge("hem").length(0.05)
    if wanted["cuff"]:
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, rib_height, 2, "Cuff (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, rib_height, 1, "Hem Band (rib)"))

    # ── Declared seams ───────────────────────────────────────────────────────
    if wanted["front"] and wanted["sleeve"]:
        pattern.declare_seam(("front", "armhole"), ("sleeve", "head_front"), tol=1.5)
    if wanted["back"] and wanted["sleeve"]:
        pattern.declare_seam(("back", "armhole"), ("sleeve", "head_back"), tol=1.5)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if wanted["sleeve"]:
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0)
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        # collar inner seam (2 strips) == the full neckline run
        pattern.declare_seam(
            [("collar", "neck_seam"), ("collar", "neck_seam")],
            [("front", "neck"), ("front", "neck"), ("back", "neck"), ("back", "neck")],
            tol=2.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "lambswool jersey / sweater knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker. Cut-and-sew branch."},
        {"item": "rib knit (2x2)",
         "qty": round(total_area * 0.10 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length", "note": "cuffs and hem band — double height, folded"},
        {"item": "band interfacing (fronts + collar)", "qty": 1, "unit": "set",
         "note": "stabilise the button bands and the shawl roll so they hold"},
        {"item": "shank buttons", "qty": button_count, "unit": "count",
         "note": "Yantra4D shank-button-solid (see notion.hardware_ref) — set through "
                 "the marked band; buttonholes are worked on the opposite front."},
        {"item": "thread (wool or wool-nylon)", "qty": 1, "unit": "spool",
         "note": "stretch seam for the body; a firmer topstitch for the bands"},
    ]
    pattern.metadata = {
        "fc400_rank": 333, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-lambswool",
        "architecture": "drop-shoulder cardigan with a continuous shawl collar rolled "
                        "around the full neckline and a button band up each front",
        "knit_ease_mm": round(knit_ease, 1),
        "knit_ease_note": "SIGNED; positive default — a cardigan is worn over layers",
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "shoulder_run_mm": round(SHOULDER_RUN, 2),
            "shoulder_run_clamped": SHOULDER_RUN_CLAMPED,
            "armhole_mm": round(armhole_len, 2),
            "neck_run_mm": round(neck_run, 1),
            "collar_strip_mm": round(max(120.0, neck_run), 1),
            "band_width_mm": round(band_width, 1),
            "note": "the collar strip length is SOLVED from the measured neckline "
                    "(both fronts + back), floored so it can never go negative; the "
                    "shoulder run is floored so the yoke never inverts at extremes",
        },
        "buttons": button_count,
        "hardware": "Yantra4D shank-button-solid (point hardware; buttonholes marked, "
                    "no sewn edge — no dimensional handshake owed)",
    }
    return pattern


result = build()
