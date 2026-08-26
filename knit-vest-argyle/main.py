"""
Argyle knit vest — FC-400 rank #338, Lane 4 (knitwear). Fashion Cabinet Cartridge.

A sleeveless V-neck pullover vest in the classic argyle intarsia — the diamond lattice
that is the vest's signature, marked on the front so the pattern carries the colourwork.
Architecturally a shaped-armhole vest: front and back on the fold, a curved (set-in-style)
armhole finished with a binding rather than a sleeve, ribbed V-neck, ribbed armholes and
hem. Negative-ease knit drafting.

What this cartridge owns:
  - THE FRONT (V-neck) and BACK (crew back neck), both cut on the fold.
  - THE ARMHOLE as a shaped curve, finished with a binding (no sleeve) — declared as an
    interface, not a declare_seam.
  - THE RIB bands: V-neck band, two armhole bands, hem band.
  - THE ARGYLE DIAMOND LATTICE marked on the front as internals.

Solving and clamps. The shoulder run is derived (quarter width less half neck) and
FLOORED; the V-neck depth is clamped so the point never drops below the underarm. The
armhole scoop depth is clamped against the armhole so the curve is always real. The rib
band lengths are solved from the measured openings, floored so they can never go negative.

Hardware: none — a pullover vest has no closure.

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
# front|back|vneck_band|armhole_band|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
body_length = float(PARAM(lambda: body_length, 600.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 420.0))   # across the back shoulders
knit_ease = float(PARAM(lambda: knit_ease, -30.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 230.0))
armhole_scoop = float(PARAM(lambda: armhole_scoop, 55.0))     # how far the armhole cuts in
vneck_depth = float(PARAM(lambda: vneck_depth, 200.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 20.0))
diamond_rows = int(PARAM(lambda: diamond_rows, 4))
diamond_cols = int(PARAM(lambda: diamond_cols, 3))
band_width = float(PARAM(lambda: band_width, 26.0))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.90))
rib_height = float(PARAM(lambda: rib_height, 55.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 9.0))

chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 840.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
shoulder_width = max(300.0, min(shoulder_width, 620.0))
knit_ease = max(-140.0, min(knit_ease, 120.0))
armhole_depth = max(160.0, min(armhole_depth, 340.0))
armhole_scoop = max(20.0, min(armhole_scoop, 110.0))
vneck_depth = max(80.0, min(vneck_depth, 320.0))
shoulder_slope = max(5.0, min(shoulder_slope, 50.0))
diamond_rows = max(2, min(diamond_rows, 8))
diamond_cols = max(2, min(diamond_cols, 6))
band_width = max(15.0, min(band_width, 50.0))
hemband_ratio = max(0.72, min(hemband_ratio, 1.0))
rib_height = max(25.0, min(rib_height, 110.0))
seam_allowance = max(6.0, min(seam_allowance, 18.0))

DRAFT_GIRTH = max(560.0, chest_girth + knit_ease)
W = DRAFT_GIRTH / 4.0
L = body_length
NW = max(46.0, min(neck_girth / 5.0 + 4.0, W - 55.0))
# Shoulder point x: half the shoulder width, but never wider than the body quarter.
SHOULDER_X = max(NW + 30.0, min(shoulder_width / 2.0, W))
BACK_NECK_DROP = 22.0
UNDERARM_Y = max(60.0, L - armhole_depth)
SLOPE = max(2.0, min(shoulder_slope, armhole_depth * 0.4))
SHOULDER_PT_Y = L - SLOPE
_shoulder_run_raw = SHOULDER_X - NW
SHOULDER_RUN = max(40.0, _shoulder_run_raw)
SHOULDER_RUN_CLAMPED = _shoulder_run_raw < 40.0
# V-neck point never below the underarm.
VNECK_Y = max(UNDERARM_Y + 20.0, SHOULDER_PT_Y - vneck_depth)
VNECK_CLAMPED = (SHOULDER_PT_Y - vneck_depth) < (UNDERARM_Y + 20.0)
# Armhole cuts in from the shoulder point to (SHOULDER_X - scoop) at the underarm.
ARM_IN_X = max(NW + 20.0, SHOULDER_X - armhole_scoop)


def _rib(name, finished_len, finished_height, qty, label):
    band_h = max(20.0, 2.0 * finished_height)
    length = max(70.0, finished_len) + 2.0 * seam_allowance
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


def _diamond_marks():
    """The argyle lattice, marked as diamonds on the front below the V and above the
    underarm."""
    marks = []
    x0, x1 = 0.0, W * 0.94
    y0, y1 = UNDERARM_Y * 0.35, VNECK_Y - 20.0
    if y1 <= y0 + 20.0:
        y1 = y0 + 20.0
    cw = (x1 - x0) / diamond_cols
    ch = (y1 - y0) / diamond_rows
    for r in range(diamond_rows):
        for c in range(diamond_cols):
            cx = x0 + (c + 0.5) * cw
            cy = y0 + (r + 0.5) * ch
            marks.append(fc.Internal(
                f"argyle-{r}-{c}",
                [fc.P(cx, cy - ch * 0.4), fc.P(cx + cw * 0.4, cy),
                 fc.P(cx, cy + ch * 0.4), fc.P(cx - cw * 0.4, cy),
                 fc.P(cx, cy - ch * 0.4)], kind="marking"))
    return marks


def build_front():
    neck_pt = fc.P(NW, SHOULDER_PT_Y)
    shoulder_pt = fc.P(SHOULDER_X, SHOULDER_PT_Y)
    internals = [fc.Internal("underarm", [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)],
                             kind="marking")]
    internals += _diamond_marks()
    return fc.Piece(
        "front",
        [
            # centre fold up to the V point
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, VNECK_Y))]),
            # V-neck: straight line from the V point up to the neck point
            fc.Edge("neck", [fc.Line(fc.P(0.0, VNECK_Y), neck_pt)]),
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            # armhole: curve from shoulder point in to the underarm point
            fc.Edge("armhole", [fc.curve_through(shoulder_pt, fc.P(ARM_IN_X, UNDERARM_Y),
                                                 bulge=0.18, side=1.0)]),
            # underarm-to-side then down (a small horizontal run to the side seam)
            fc.Edge("side", [fc.Line(fc.P(ARM_IN_X, UNDERARM_Y), fc.P(W, UNDERARM_Y)),
                             fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("armhole", 0.5, "armhole notch")],
        grainline=fc.Grainline(fc.P(W * 0.5, 40.0), fc.P(W * 0.5, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (V-neck argyle)",
    )


def build_back():
    neck_low_y = SHOULDER_PT_Y - BACK_NECK_DROP
    neck_pt = fc.P(NW, SHOULDER_PT_Y)
    shoulder_pt = fc.P(SHOULDER_X, SHOULDER_PT_Y)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_low_y))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, neck_low_y), neck_pt,
                                              bulge=0.14, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_pt, shoulder_pt)]),
            fc.Edge("armhole", [fc.curve_through(shoulder_pt, fc.P(ARM_IN_X, UNDERARM_Y),
                                                 bulge=0.18, side=1.0)]),
            fc.Edge("side", [fc.Line(fc.P(ARM_IN_X, UNDERARM_Y), fc.P(W, UNDERARM_Y)),
                             fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("armhole", 0.5, "armhole notch")],
        grainline=fc.Grainline(fc.P(W * 0.5, 40.0), fc.P(W * 0.5, UNDERARM_Y - 30.0)),
        internals=[fc.Internal("underarm", [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (crew back)",
    )


def build():
    pattern = fc.PatternSet("knit-vest-argyle")
    front = build_front()
    back = build_back()

    names = ("front", "back", "vneck_band", "armhole_band", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)

    # Measured openings drive the ribs.
    vneck_run = 2.0 * front.edge("neck").length(0.05) + 2.0 * back.edge("neck").length(0.05)
    armhole_run = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    hem_circ = 2.0 * (front.edge("hem").length(0.05) + back.edge("hem").length(0.05))
    if wanted["vneck_band"]:
        pattern.add(_rib("vneck_band", vneck_run, band_width, 1, "V-neck band (rib)"))
    if wanted["armhole_band"]:
        pattern.add(_rib("armhole_band", 2.0 * armhole_run, band_width, 2, "Armhole band (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, rib_height, 1, "Hem Band (rib)"))

    # ── Declared seams ───────────────────────────────────────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "lambswool jersey (intarsia argyle front)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker. The front carries the "
                 "argyle intarsia; the back is plain."},
        {"item": "rib knit (2x2)",
         "qty": round(total_area * 0.12 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length", "note": "V-neck band, two armhole bands, hem band"},
        {"item": "thread (wool)", "qty": 1, "unit": "spool", "note": "stretch seam"},
    ]
    pattern.metadata = {
        "fc400_rank": 338, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-lambswool",
        "architecture": "sleeveless V-neck vest with a shaped armhole finished by a "
                        "binding; argyle diamond lattice marked on the front",
        "knit_ease_mm": round(knit_ease, 1),
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "shoulder_run_mm": round(SHOULDER_RUN, 2),
            "shoulder_run_clamped": SHOULDER_RUN_CLAMPED,
            "vneck_y_mm": round(VNECK_Y, 1),
            "vneck_clamped": VNECK_CLAMPED,
            "armhole_run_mm": round(armhole_run, 1),
            "note": "the shoulder run is floored; the V point is clamped above the "
                    "underarm so the neck never inverts the front at extremes",
        },
        "argyle": {"rows": diamond_rows, "cols": diamond_cols},
        "hardware": "none — a pullover vest has no closure",
    }
    return pattern


result = build()
