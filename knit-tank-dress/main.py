"""
Knit tank dress — FC-400 rank #335, Lane 4 (knitwear). Fashion Cabinet Cartridge.

A pull-on sleeveless jersey dress: a scoop-neck tank body run down to dress length, with
a gentle A-line release from the waist to the hem. It is the plainest knit architecture in
the commons — a front and a back on the fold, a straight shoulder strap, a scooped
neckline and a scooped armhole, both finished with a binding, and a hem that flares.

What this cartridge owns:
  - THE FRONT (deep scoop) and BACK (shallow scoop), both cut on the fold, drafted from
    the chest and hip girths with SIGNED negative knit ease.
  - THE A-LINE RELEASE: the side seam runs straight from the underarm to the waist, then
    releases outward to the hem by `hem_flare`.
  - RIB or self-binding at the neck and armholes (declared as interfaces).

Solving and clamps. The shoulder strap width is derived (quarter chest less the scoop
half-width) and FLOORED so a very wide scoop can never eat the whole shoulder and invert
it. The neck and armhole scoop depths are clamped above the underarm. The hip half-width
is the larger of the hip-derived width and the chest width, so the dress never narrows
below the body at the hem. Every derived width is floored before any point is built.

Hardware: none — a pull-on tank dress has no closure.

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
# front|back|neck_band|armhole_band|set

chest_girth = float(PARAM(lambda: chest_girth, 920.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
dress_length = float(PARAM(lambda: dress_length, 950.0))    # shoulder to hem
waist_drop = float(PARAM(lambda: waist_drop, 400.0))        # shoulder to waist (release point)
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
knit_ease = float(PARAM(lambda: knit_ease, -40.0))
armhole_depth = float(PARAM(lambda: armhole_depth, 230.0))  # shoulder to underarm
front_scoop = float(PARAM(lambda: front_scoop, 130.0))      # front neck scoop depth
back_scoop = float(PARAM(lambda: back_scoop, 60.0))
scoop_half = float(PARAM(lambda: scoop_half, 110.0))        # neck scoop half-width
armhole_scoop = float(PARAM(lambda: armhole_scoop, 40.0))
hem_flare = float(PARAM(lambda: hem_flare, 90.0))           # each side release at hem
band_width = float(PARAM(lambda: band_width, 22.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 9.0))

chest_girth = max(680.0, min(chest_girth, 1700.0))
hip_girth = max(680.0, min(hip_girth, 1800.0))
dress_length = max(700.0, min(dress_length, 1400.0))
waist_drop = max(300.0, min(waist_drop, 620.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
knit_ease = max(-160.0, min(knit_ease, 100.0))
armhole_depth = max(150.0, min(armhole_depth, 320.0))
front_scoop = max(50.0, min(front_scoop, 280.0))
back_scoop = max(20.0, min(back_scoop, 200.0))
scoop_half = max(50.0, min(scoop_half, 200.0))
armhole_scoop = max(15.0, min(armhole_scoop, 100.0))
hem_flare = max(0.0, min(hem_flare, 260.0))
band_width = max(12.0, min(band_width, 45.0))
seam_allowance = max(6.0, min(seam_allowance, 18.0))

DRAFT_CHEST = max(560.0, chest_girth + knit_ease)
DRAFT_HIP = max(560.0, hip_girth + knit_ease)
WC = DRAFT_CHEST / 4.0                              # quarter chest
WH = max(WC, DRAFT_HIP / 4.0)                       # quarter hip, never below chest
L = dress_length
SHOULDER_Y = L
UNDERARM_Y = max(L * 0.4, L - armhole_depth)        # underarm below the shoulder
WAIST_Y = max(UNDERARM_Y - 120.0, L - waist_drop)   # release point, below the underarm
WAIST_Y = min(WAIST_Y, UNDERARM_Y - 20.0)           # ensure below the underarm
WAIST_Y = max(60.0, WAIST_Y)
# Neck scoop half-width, floored below the chest quarter so a strap survives.
SCOOP_HALF = max(40.0, min(scoop_half, WC - 40.0))
# Shoulder strap: from the scoop edge to the armhole edge on the shoulder line.
STRAP_IN = SCOOP_HALF                               # inner edge of the strap (neck side)
STRAP_OUT = max(STRAP_IN + 25.0, WC - armhole_scoop)  # outer edge (armhole side)
# Scoop depths clamped above the underarm.
FRONT_SCOOP_Y = max(UNDERARM_Y + 15.0, SHOULDER_Y - front_scoop)
BACK_SCOOP_Y = max(UNDERARM_Y + 15.0, SHOULDER_Y - back_scoop)
# Hem half-width releases from the waist.
HEM_HALF = WH + hem_flare


def _rib(name, finished_len, finished_height, qty, label):
    band_h = max(18.0, 2.0 * finished_height)
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


def _panel(name, scoop_y, label):
    """A tank-dress panel, cut on the fold. Edges: centre fold, neckline scoop, shoulder
    strap, armhole scoop, side seam (underarm -> waist -> flared hem), hem."""
    return fc.Piece(
        name,
        [
            # centre fold up to the scoop bottom
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, scoop_y))]),
            # neckline scoop out to the strap inner point at the shoulder line
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, scoop_y),
                                              fc.P(STRAP_IN, SHOULDER_Y),
                                              bulge=0.20, side=-1.0)]),
            # shoulder strap: straight across the shoulder line
            fc.Edge("shoulder", [fc.Line(fc.P(STRAP_IN, SHOULDER_Y),
                                         fc.P(STRAP_OUT, SHOULDER_Y))]),
            # armhole scoop: from the strap outer down to the underarm point
            fc.Edge("armhole", [fc.curve_through(fc.P(STRAP_OUT, SHOULDER_Y),
                                                 fc.P(WC, UNDERARM_Y),
                                                 bulge=0.16, side=1.0)]),
            # side seam: underarm -> waist -> flared hem corner
            fc.Edge("side", [fc.Line(fc.P(WC, UNDERARM_Y), fc.P(WC, WAIST_Y)),
                             fc.Line(fc.P(WC, WAIST_Y), fc.P(HEM_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5, "waist"), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(WC * 0.5, 40.0), fc.P(WC * 0.5, UNDERARM_Y - 30.0)),
        internals=[fc.Internal("waist line", [fc.P(0.0, WAIST_Y), fc.P(WC, WAIST_Y)],
                               kind="marking"),
                   fc.Internal("underarm", [fc.P(0.0, UNDERARM_Y), fc.P(WC, UNDERARM_Y)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("knit-tank-dress")
    front = _panel("front", FRONT_SCOOP_Y, "Front (deep scoop)")
    back = _panel("back", BACK_SCOOP_Y, "Back (shallow scoop)")

    names = ("front", "back", "neck_band", "armhole_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)

    neck_run = 2.0 * (front.edge("neck").length(0.05) + back.edge("neck").length(0.05))
    armhole_run = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    if wanted["neck_band"]:
        pattern.add(_rib("neck_band", neck_run, band_width, 1, "Neck binding (rib)"))
    if wanted["armhole_band"]:
        pattern.add(_rib("armhole_band", 2.0 * armhole_run, band_width, 2, "Armhole binding (rib)"))

    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton jersey (medium weight)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker. A stable jersey holds the "
                 "A-line without clinging."},
        {"item": "rib or self-fabric binding",
         "qty": round(total_area * 0.08 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length", "note": "neck and two armhole bindings"},
        {"item": "thread (poly-cotton, stretch)", "qty": 1, "unit": "spool",
         "note": "overlock body seams; a twin needle or coverstitch for the hem"},
    ]
    pattern.metadata = {
        "fc400_rank": 335, "family": "knitwear", "lane": 4,
        "fabric_hint": "cotton-knit",
        "architecture": "pull-on sleeveless jersey dress; scoop tank body with an A-line "
                        "release from the waist to a flared hem",
        "knit_ease_mm": round(knit_ease, 1),
        "solved": {
            "draft_chest_mm": round(DRAFT_CHEST, 1),
            "draft_hip_mm": round(DRAFT_HIP, 1),
            "scoop_half_mm": round(SCOOP_HALF, 1),
            "strap_out_mm": round(STRAP_OUT, 1),
            "front_scoop_y_mm": round(FRONT_SCOOP_Y, 1),
            "hem_half_mm": round(HEM_HALF, 1),
            "note": "the strap width is derived and floored so a wide scoop cannot eat "
                    "the shoulder; scoops are clamped above the underarm; the hem half is "
                    "the larger of hip and chest so the dress never narrows below the body",
        },
        "hardware": "none — a pull-on tank dress has no closure",
    }
    return pattern


result = build()
