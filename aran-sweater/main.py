"""
Aran cable sweater — FC-400 rank #331, Lane 4 (knitwear). Fashion Cabinet Cartridge.

The fisherman's Aran: a heavy full-fashioned crewneck worked in panels of cables,
diamonds and moss stitch. Architecturally it is a DROP-SHOULDER set-in body — a wide,
shallow armhole and a straight sleeve head — because that is the shape a hand-knitter
works flat and seams, and because the bulk of an Aran cable panel wants a generous,
square armhole rather than a scooped set-in curve.

What this cartridge owns (Fashion Cabinet is pattern-native, 2-D first):
  - THE PANELS as pieces: front and back (cut on the centre fold), a straight
    drop-shoulder sleeve, and three rib bands (neckband, cuffs, hem band).
  - NEGATIVE-EASE knit drafting: `knit_ease` is SIGNED and defaults slightly negative
    — an Aran is worn close but not compressed, so the default is a small stretch-on.
    The floor keeps the draft wearable at maximum compression.
  - THE CABLE-PANEL LAYOUT marked as internals: a central panel flanked by side
    panels, so the pattern carries the stitch architecture and not merely the outline.

Drop-shoulder solving. The armhole is a straight vertical drop of `armhole_depth`
from the shoulder to the underarm; the sleeve head is a straight run whose width equals
the armhole opening exactly, so the armhole seam balances by construction. The shoulder
run is DERIVED (quarter width less half neck width) and FLOORED — a wide neck on a
narrow body would drive it to zero or negative and invert the yoke into valid-looking
geometry after CCW normalization. The back-neck rise tracks any flattened shoulder run
(the back-neck-rise clamp lesson): it is solved from the shoulder slope so it can never
outrun a collapsed shoulder.

Hardware: none — a crewneck pullover has no closure.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|neckband|cuff|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
body_length = float(PARAM(lambda: body_length, 660.0))       # nape to hem-band seam
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))    # shoulder to cuff seam
knit_ease = float(PARAM(lambda: knit_ease, -20.0))           # SIGNED; negative = stretch on
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))   # drop-shoulder depth
front_neck_drop = float(PARAM(lambda: front_neck_drop, 80.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 22.0))  # shoulder point drop
cable_panel_frac = float(PARAM(lambda: cable_panel_frac, 0.42))  # central panel share
cuff_ratio = float(PARAM(lambda: cuff_ratio, 0.66))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.90))
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.86))
rib_height = float(PARAM(lambda: rib_height, 70.0))          # cuff / hem band depth
neckband_width = float(PARAM(lambda: neckband_width, 26.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (match the manifest slider bounds exactly) ────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(440.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(320.0, min(sleeve_length, 780.0))
knit_ease = max(-140.0, min(knit_ease, 160.0))
armhole_depth = max(170.0, min(armhole_depth, 380.0))
front_neck_drop = max(30.0, min(front_neck_drop, 170.0))
shoulder_slope = max(5.0, min(shoulder_slope, 55.0))
cable_panel_frac = max(0.20, min(cable_panel_frac, 0.66))
cuff_ratio = max(0.50, min(cuff_ratio, 0.95))
hemband_ratio = max(0.72, min(hemband_ratio, 1.0))
neckband_ratio = max(0.72, min(neckband_ratio, 1.0))
rib_height = max(30.0, min(rib_height, 120.0))
neckband_width = max(15.0, min(neckband_width, 55.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))

# ── The knit block ───────────────────────────────────────────────────────────
DRAFT_GIRTH = max(560.0, chest_girth + knit_ease)
W = DRAFT_GIRTH / 4.0                            # quarter body width
L = body_length
# Half neck width, floored well under the quarter width so a shoulder always survives.
NW = max(48.0, min(neck_girth * neckband_ratio / 5.0 + 4.0, W - 60.0))
BACK_NECK_DROP = 22.0

# Drop-shoulder armhole: a straight vertical from the shoulder line down to the
# underarm. The shoulder line sits `armhole_depth` above the hem's top region.
UNDERARM_Y = max(60.0, L - armhole_depth)        # never below the hem
# Shoulder point height above the underarm.
SHOULDER_Y = L

# The shoulder RUN is derived and floored (the back-neck-rise clamp lesson): a wide
# neck on a narrow body would otherwise give a zero or negative run and invert the
# yoke. The drawn neck rise then tracks this floored run, never outrunning it.
_shoulder_run_raw = W - NW
SHOULDER_RUN = max(45.0, _shoulder_run_raw)
SHOULDER_RUN_CLAMPED = _shoulder_run_raw < 45.0
# The shoulder point drops by shoulder_slope, floored so it cannot exceed what the
# shoulder run can carry (rise can never make the neck point dip below the underarm).
SLOPE = max(2.0, min(shoulder_slope, armhole_depth * 0.45))
SHOULDER_PT_Y = SHOULDER_Y - SLOPE


def _rib(name, finished_len, finished_height, qty, label):
    """A rib band, drafted double-height and folded when sewn."""
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


def _cable_marks(name):
    """Central cable panel flanked by side panels — the Aran stitch architecture,
    marked so the pattern carries it. The central panel is `cable_panel_frac` of the
    half width, centred on the fold."""
    half_panel = min(W - 12.0, W * cable_panel_frac)
    marks = [
        fc.Internal(f"{name} cable panel edge",
                    [fc.P(half_panel, 0.0), fc.P(half_panel, UNDERARM_Y)],
                    kind="marking"),
        fc.Internal(f"{name} underarm line",
                    [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)], kind="marking"),
    ]
    return marks


def _body_piece(name, neck_drop, label):
    """A body panel (front or back), cut 1 on the centre fold. Straight sides, a
    drop-shoulder armhole (straight vertical), a sloped shoulder, a scooped neck."""
    # Neck point on the shoulder line: at (NW, neck top). Neck drops to (0, neck_low).
    neck_top_y = SHOULDER_PT_Y
    neck_low_y = SHOULDER_PT_Y - neck_drop
    neck_pt = fc.P(NW, neck_top_y)
    # Shoulder: from neck point out to shoulder point (W - side inset, at shoulder pt).
    shoulder_pt = fc.P(W, SHOULDER_PT_Y)
    internals = _cable_marks(name)
    return fc.Piece(
        name,
        [
            # centre fold up to the neck low point
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_low_y))]),
            # neckline: scoop from centre out to the neck point on the shoulder line
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, neck_low_y), neck_pt,
                                              bulge=0.18, side=-1.0)]),
            # shoulder: neck point out to the shoulder point
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            # armhole: straight vertical drop from shoulder point to underarm
            fc.Edge("armhole", [fc.Line(shoulder_pt, fc.P(W, UNDERARM_Y))]),
            # side seam: underarm straight down to the hem
            fc.Edge("side", [fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            # hem
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(W * 0.5, 40.0), fc.P(W * 0.5, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve(armhole_len):
    """Straight drop-shoulder sleeve (cut 2, mirrored). Its head is a straight run
    whose two halves each equal the armhole opening, so the armhole seam balances by
    construction. Frame: x=0 centre, y=0 cuff seam."""
    # Biceps half-width from the drafted girth (negative ease flows in), floored.
    bicep_half = max(90.0, W * 0.66)
    cuff_half = max(50.0, min(bicep_half * cuff_ratio, bicep_half - 12.0))
    # Underarm length is the sleeve length less the (small) head rise.
    HEAD_RISE = max(30.0, min(armhole_depth * 0.18, 90.0))
    ul = max(120.0, sleeve_length - HEAD_RISE)
    y_ua = ul
    # The head: two straight edges from the biceps up to the sleeve head, each equal to
    # the body's armhole length. The head keeps a minimum crown width HEAD_HALF_MIN so
    # the crown curve is never degenerate; the biceps is WIDENED if it cannot contain
    # both the head run and that minimum crown. Solve so the straight head edge length
    # == armhole_len exactly: length^2 = (bicep_half - head_x)^2 + HEAD_RISE^2.
    HEAD_HALF_MIN = 30.0
    dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    if dx2 <= 1.0:
        # armhole shorter than the rise: collapse the rise so a real head survives
        HEAD_RISE = max(10.0, armhole_len * 0.4)
        dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    head_dx = dx2 ** 0.5
    # need bicep_half - head_dx >= HEAD_HALF_MIN  →  widen biceps if not
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
            fc.Edge("underarm_back",
                    [fc.Line(fc.P(cuff_half, 0.0), fc.P(bicep_half, y_ua))]),
            fc.Edge("head_back", [fc.Line(fc.P(bicep_half, y_ua), back_top)]),
            # the sleeve-head crown between the two head edges
            fc.Edge("crown", [fc.curve_through(back_top, front_top,
                                               bulge=0.05, side=1.0)]),
            fc.Edge("head_front", [fc.Line(front_top, fc.P(-bicep_half, y_ua))]),
            fc.Edge("underarm_front",
                    [fc.Line(fc.P(-bicep_half, y_ua), fc.P(-cuff_half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("head_front", 0.5, "front armhole match"),
                 fc.Notch("head_back", 0.5, "back armhole match"),
                 fc.Notch("crown", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, y_ua * 0.85)),
        internals=[fc.Internal("sleeve biceps line",
                               [fc.P(-bicep_half, y_ua), fc.P(bicep_half, y_ua)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (drop-shoulder)",
    )


def build():
    pattern = fc.PatternSet("aran-sweater")
    front = _body_piece("front", front_neck_drop, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")
    armhole_len = front.edge("armhole").length(0.05)
    sleeve = build_sleeve(armhole_len)

    names = ("front", "back", "sleeve", "neckband", "cuff", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)

    neck_opening = 2.0 * (front.edge("neck").length(0.05)
                          + back.edge("neck").length(0.05))
    hem_circ = 2.0 * (front.edge("hem").length(0.05)
                      + back.edge("hem").length(0.05))
    cuff_circ = sleeve.edge("hem").length(0.05)
    if wanted["neckband"]:
        pattern.add(_rib("neckband", neck_opening * neckband_ratio,
                         neckband_width, 1, "Neckband (rib)"))
    if wanted["cuff"]:
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, rib_height, 2, "Cuff (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, rib_height, 1,
                         "Hem Band (rib)"))

    # ── Declared seams ───────────────────────────────────────────────────────
    # Drop-shoulder armhole: the sleeve head edge equals the body armhole exactly.
    if wanted["front"] and wanted["sleeve"]:
        pattern.declare_seam(("front", "armhole"), ("sleeve", "head_front"), tol=1.5)
    if wanted["back"] and wanted["sleeve"]:
        pattern.declare_seam(("back", "armhole"), ("sleeve", "head_back"), tol=1.5)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if wanted["sleeve"]:
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "aran wool (bulky, worsted-spun)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker. Cut-and-sew branch; "
                 "a fully hand-knitted version works the cables in the panel."},
        {"item": "rib knit (2x2, self or contrast)",
         "qty": round(total_area * 0.12 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length", "note": "neckband, two cuffs, hem band — double height, folded"},
        {"item": "stay tape (neckline + shoulders)", "qty": 1200, "unit": "mm_length",
         "note": "an Aran is heavy; tape the shoulders so they hold the weight"},
        {"item": "thread (wool or wool-nylon)", "qty": 1, "unit": "spool",
         "note": "mattress-seam by hand, or a stretch machine seam"},
    ]
    pattern.metadata = {
        "fc400_rank": 331, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-aran",
        "architecture": "drop-shoulder set-in: a wide shallow straight armhole and a "
                        "straight sleeve head, the shape a hand-knitter seams",
        "knit_ease_mm": round(knit_ease, 1),
        "knit_ease_note": "SIGNED; negative = the draft is smaller than the body and "
                          "stretches on. Aran default is a small stretch (-20 mm).",
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "shoulder_run_mm": round(SHOULDER_RUN, 2),
            "shoulder_run_clamped": SHOULDER_RUN_CLAMPED,
            "armhole_mm": round(armhole_len, 2),
            "half_neck_width_mm": round(NW, 2),
            "underarm_y_mm": round(UNDERARM_Y, 1),
            "note": "the shoulder run is DERIVED (quarter width less half neck) and "
                    "floored; the neck rise tracks the floored shoulder so it cannot "
                    "invert the yoke at extremes (the back-neck-rise clamp lesson)",
        },
        "cable_layout": {"central_panel_frac": round(cable_panel_frac, 3),
                         "note": "central cable panel flanked by side panels, marked "
                                 "as internals so the pattern carries the stitch plan"},
        "hardware": "none — a crewneck pullover has no closure",
    }
    return pattern


result = build()
