"""
Chunky roll-neck sweater — FC-400 rank #340, Lane 4 (knitwear). Fashion Cabinet Cartridge.

A heavy drop-shoulder pullover finished with a tall roll-neck (turtleneck) collar: a rib
tube drafted at twice the finished height and folded over, whose lower edge equals the
neckline run. The chunky gauge is the point — a big soft yarn worked at a wide armhole
with a generous, high collar.

What this cartridge owns:
  - THE DROP-SHOULDER BODY (front + back on the fold), the straight SLEEVE, and the
    CUFF, HEM and ROLL-NECK rib bands, drafted with SIGNED negative knit ease.
  - THE ROLL NECK as a tall rib tube: length = neckline run × the neck pull-in ratio,
    height = `collar_height` doubled and folded.

Solving and clamps. The shoulder run is derived (quarter width less half neck) and
FLOORED; the shoulder slope is capped against the armhole depth so the neck point never
dips below the underarm. The sleeve head is solved to the armhole exactly, biceps widened
when needed so the crown is never degenerate. The neckline run drives the roll-neck
length, floored so it can never go negative.

Hardware: none — a roll-neck pullover has no closure.

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
# front|back|sleeve|roll_neck|cuff|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
body_length = float(PARAM(lambda: body_length, 660.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 610.0))
knit_ease = float(PARAM(lambda: knit_ease, 0.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 270.0))
front_neck_drop = float(PARAM(lambda: front_neck_drop, 55.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 24.0))
collar_height = float(PARAM(lambda: collar_height, 150.0))    # finished roll-neck height
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.92))
cuff_ratio = float(PARAM(lambda: cuff_ratio, 0.62))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.88))
rib_height = float(PARAM(lambda: rib_height, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(440.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(320.0, min(sleeve_length, 780.0))
knit_ease = max(-100.0, min(knit_ease, 200.0))
armhole_depth = max(170.0, min(armhole_depth, 400.0))
front_neck_drop = max(30.0, min(front_neck_drop, 160.0))
shoulder_slope = max(5.0, min(shoulder_slope, 55.0))
collar_height = max(60.0, min(collar_height, 280.0))
neckband_ratio = max(0.72, min(neckband_ratio, 1.0))
cuff_ratio = max(0.50, min(cuff_ratio, 0.95))
hemband_ratio = max(0.72, min(hemband_ratio, 1.0))
rib_height = max(30.0, min(rib_height, 140.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))

DRAFT_GIRTH = max(560.0, chest_girth + knit_ease)
W = DRAFT_GIRTH / 4.0
L = body_length
NW = max(48.0, min(neck_girth / 5.0 + 4.0, W - 60.0))
BACK_NECK_DROP = 22.0
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


def _body(name, neck_drop, label):
    neck_low_y = max(80.0, SHOULDER_PT_Y - neck_drop)
    neck_pt = fc.P(NW, SHOULDER_PT_Y)
    shoulder_pt = fc.P(W, SHOULDER_PT_Y)
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_low_y))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, neck_low_y), neck_pt,
                                              bulge=0.14, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            fc.Edge("armhole", [fc.Line(shoulder_pt, fc.P(W, UNDERARM_Y))]),
            fc.Edge("side", [fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(W * 0.5, 40.0), fc.P(W * 0.5, UNDERARM_Y - 30.0)),
        internals=[fc.Internal("underarm", [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _sleeve(armhole_len):
    bicep_half = max(90.0, W * 0.68)
    HEAD_RISE = max(30.0, min(armhole_depth * 0.18, 90.0))
    ul = max(120.0, sleeve_length - HEAD_RISE)
    y_ua = ul
    dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    if dx2 <= 1.0:
        HEAD_RISE = max(10.0, armhole_len * 0.4)
        dx2 = armhole_len ** 2 - HEAD_RISE ** 2
    head_dx = dx2 ** 0.5
    bicep_half = max(bicep_half, head_dx + 30.0)
    cuff_half = max(50.0, min(bicep_half * cuff_ratio, bicep_half - 12.0))
    head_x = bicep_half - head_dx
    top_y = y_ua + HEAD_RISE
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-cuff_half, 0.0), fc.P(cuff_half, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(cuff_half, 0.0), fc.P(bicep_half, y_ua))]),
            fc.Edge("head_back", [fc.Line(fc.P(bicep_half, y_ua), fc.P(head_x, top_y))]),
            fc.Edge("crown", [fc.curve_through(fc.P(head_x, top_y), fc.P(-head_x, top_y),
                                               bulge=0.05, side=1.0)]),
            fc.Edge("head_front", [fc.Line(fc.P(-head_x, top_y), fc.P(-bicep_half, y_ua))]),
            fc.Edge("underarm_front", [fc.Line(fc.P(-bicep_half, y_ua), fc.P(-cuff_half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("head_front", 0.5), fc.Notch("head_back", 0.5),
                 fc.Notch("crown", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, y_ua * 0.85)),
        internals=[fc.Internal("sleeve biceps line",
                               [fc.P(-bicep_half, y_ua), fc.P(bicep_half, y_ua)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (drop-shoulder)",
    )


def build():
    pattern = fc.PatternSet("chunky-turtleneck")
    front = _body("front", front_neck_drop, "Front")
    back = _body("back", BACK_NECK_DROP, "Back")
    armhole_len = front.edge("armhole").length(0.05)
    sleeve = _sleeve(armhole_len)
    neck_run = 2.0 * (front.edge("neck").length(0.05) + back.edge("neck").length(0.05))

    names = ("front", "back", "sleeve", "roll_neck", "cuff", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)
    if wanted["roll_neck"]:
        pattern.add(_rib("roll_neck", neck_run * neckband_ratio, collar_height, 1,
                         "Roll-neck collar (rib)"))
    hem_circ = 2.0 * (front.edge("hem").length(0.05) + back.edge("hem").length(0.05))
    cuff_circ = sleeve.edge("hem").length(0.05)
    if wanted["cuff"]:
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, rib_height, 2, "Cuff (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, rib_height, 1, "Hem Band (rib)"))

    if wanted["front"] and wanted["sleeve"]:
        pattern.declare_seam(("front", "armhole"), ("sleeve", "head_front"), tol=1.5)
    if wanted["back"] and wanted["sleeve"]:
        pattern.declare_seam(("back", "armhole"), ("sleeve", "head_back"), tol=1.5)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if wanted["sleeve"]:
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "chunky wool (bulky gauge)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker. A heavy gauge is the point."},
        {"item": "chunky rib (2x2 or 4x2)",
         "qty": round(total_area * 0.14 / (fabric_width * 0.78) / 10.0) * 10,
         "unit": "mm_length", "note": "roll-neck, cuffs, hem — double height, folded"},
        {"item": "stay tape (shoulders + neckline)", "qty": 900, "unit": "mm_length",
         "note": "a chunky knit is heavy; tape holds the shoulder line"},
        {"item": "thread (wool)", "qty": 1, "unit": "spool", "note": "stretch seam"},
    ]
    pattern.metadata = {
        "fc400_rank": 340, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-chunky",
        "architecture": "drop-shoulder pullover with a tall folded roll-neck collar",
        "knit_ease_mm": round(knit_ease, 1),
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "shoulder_run_mm": round(SHOULDER_RUN, 2),
            "shoulder_run_clamped": SHOULDER_RUN_CLAMPED,
            "armhole_mm": round(armhole_len, 2),
            "neck_run_mm": round(neck_run, 1),
            "roll_neck_len_mm": round(neck_run * neckband_ratio, 1),
            "collar_height_mm": round(collar_height, 1),
            "note": "the roll-neck length is solved from the measured neckline, floored; "
                    "shoulder run and slope floored so the yoke never inverts at extremes",
        },
        "hardware": "none — a roll-neck pullover has no closure",
    }
    return pattern


result = build()
