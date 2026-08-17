"""
Pencil Skirt — FC-100 rank #32. Fashion Cabinet Garment Cartridge.

The mini-skirt straight block carried to knee length with a stronger pencil
taper: the hem half-width pulls in `taper_mm` from the hip half-width, and
the walking ease the taper removes comes back as a CB back vent — two
parallel marked lines rising `vent_height` from the hem, 40 mm apart, beside
the CB seam. Front on fold with one waist dart per half; back in two panels
with a CB zipper notch, a hook & eye drill cross above the zipper top stop,
a vent-top notch, one long dart per panel and the vent internals. A
`waistband_style` select swaps the waist finish: "band" emits the straight
cut-1 overlap waistband verified with an eased multi-edge check; "facing"
emits a clean single-layer waist facing strip with its own exact-ease check.
Front and back share one side-waist construction so the side seams match.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|waistband|facing|set
waistband_style = str(PARAM(lambda: waistband_style, "band"))  # band|facing

waist_girth  = float(PARAM(lambda: waist_girth, 700.0))
hip_girth    = float(PARAM(lambda: hip_girth, 940.0))
skirt_length = float(PARAM(lambda: skirt_length, 580.0))
hip_depth    = float(PARAM(lambda: hip_depth, 200.0))
taper_mm     = float(PARAM(lambda: taper_mm, 25.0))
hip_ease     = float(PARAM(lambda: hip_ease, 30.0))
waist_ease   = float(PARAM(lambda: waist_ease, 15.0))
front_dart   = float(PARAM(lambda: front_dart, 20.0))
back_dart    = float(PARAM(lambda: back_dart, 25.0))
vent_height  = float(PARAM(lambda: vent_height, 160.0))
zipper_length = float(PARAM(lambda: zipper_length, 200.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

if waistband_style not in ("band", "facing"):
    waistband_style = "band"

waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(waist_girth, min(hip_girth, 1700.0))
skirt_length = max(420.0, min(skirt_length, 760.0))
hip_depth = max(150.0, min(hip_depth, min(280.0, skirt_length - 120.0)))
taper_mm = max(0.0, min(taper_mm, 50.0))
front_dart = max(0.0, min(front_dart, 45.0))
back_dart = max(0.0, min(back_dart, 50.0))
vent_height = max(80.0, min(vent_height, skirt_length * 0.45))
zipper_length = max(120.0, min(zipper_length, skirt_length * 0.5))

QH = (hip_girth + hip_ease) / 4.0
HIP_Y = skirt_length - hip_depth
SIDE_RISE = 12.0
OVERLAP = 30.0     # waistband hook/button overlap ("band" style only)
BAND_H = 38.0      # finished waistband height (folds double)
FACING_H = 55.0    # waist facing strip width ("facing" style)
VENT_W = 40.0      # vent underlap width beside the CB
DART_LEN = 130.0   # pencil darts run long toward the hip


def _skirt_piece(name, dart_intake, center_fold, label):
    # Common side-waist point for BOTH pieces (average suppression) so the
    # side seams match exactly; per-piece dart intakes stay as internals.
    quarter_waist = (waist_girth + waist_ease) / 4.0
    waist_w = min(quarter_waist + (front_dart + back_dart) / 2.0, QH - 5.0)
    origin = fc.P(0.0, 0.0)
    top = fc.P(0.0, skirt_length)
    waist_out = fc.P(waist_w, skirt_length + SIDE_RISE)
    hip_pt = fc.P(QH, HIP_Y)
    hem_out = fc.P(QH - taper_mm, 0.0)                 # pencil-tapered hem half-width
    side = fc.Edge(
        "side",
        [fc.Bezier(waist_out, fc.P(waist_w + (QH - waist_w) * 0.55, skirt_length - 40.0),
                   fc.P(QH, HIP_Y + hip_depth * 0.35), hip_pt),
         fc.Line(hip_pt, hem_out)],
    )
    hip_t = 1.0 - fc.polyline_length([hip_pt, hem_out]) / side.length()
    edges = [
        fc.Edge("center", [fc.Line(origin, top)]),
        fc.Edge("waist", [fc.curve_through(top, waist_out, bulge=0.05, side=-1.0)]),
        side,
        fc.Edge("hem", [fc.Line(hem_out, origin)]),
    ]
    notches = [fc.Notch("side", hip_t, "hip line")]
    allowances = {"hem": hem_allowance}
    internals = []
    if center_fold:
        cut = fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True)
    else:
        cut = fc.CutSpec(quantity=2, mirror=True)
        allowances["center"] = 20.0                    # CB seam with zipper
        notches.append(fc.Notch("center", 1.0 - zipper_length / skirt_length, "zipper stop"))
        notches.append(fc.Notch("center", vent_height / skirt_length, "vent top"))
        # Hook & eye drill cross at the CB waist, above the zipper top stop.
        hx, hy = 10.0, skirt_length - 12.0
        internals.append(fc.Internal(
            "hook & eye (h)", [fc.P(hx - 4.0, hy), fc.P(hx + 4.0, hy)], kind="drill"))
        internals.append(fc.Internal(
            "hook & eye (v)", [fc.P(hx, hy - 4.0), fc.P(hx, hy + 4.0)], kind="drill"))
        # CB vent: fold line on the CB seam, underlap edge VENT_W inside —
        # the walking ease the pencil taper removes comes back here.
        internals.append(fc.Internal(
            "back vent fold", [fc.P(0.0, 0.0), fc.P(0.0, vent_height)]))
        internals.append(fc.Internal(
            "back vent edge", [fc.P(VENT_W, 0.0), fc.P(VENT_W, vent_height)]))
    dart_cx = waist_w * 0.55
    if dart_intake > 0.5:
        internals.append(fc.Internal(
            f"{name} waist dart",
            [fc.P(dart_cx - dart_intake / 2.0, skirt_length + SIDE_RISE * 0.5),
             fc.P(dart_cx, skirt_length - DART_LEN),
             fc.P(dart_cx + dart_intake / 2.0, skirt_length + SIDE_RISE * 0.5)],
            kind="dart",
        ))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=notches,
        grainline=fc.Grainline(fc.P(QH * 0.55, 60.0), fc.P(QH * 0.55, skirt_length - 90.0)),
        internals=internals,
        cut=cut,
        label=label,
    )


def _waistband(front, back):
    """Straight cut-1 band sized off the measured waist seam + overlap."""
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ + OVERLAP + 2.0 * seam_allowance
    band_h = 2.0 * (BAND_H + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,  # drafted cut-ready; allowances live in the rectangle
        notches=[fc.Notch("bottom", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def _facing(front, back):
    """Clean-finish waist facing strip sized off the measured waist seam."""
    circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    length = circ + 2.0 * seam_allowance
    return fc.Piece(
        "facing",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, FACING_H))]),
            fc.Edge("top", [fc.Line(fc.P(length, FACING_H), fc.P(0.0, FACING_H))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, FACING_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,  # drafted cut-ready; end allowances live in the strip
        notches=[fc.Notch("bottom", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(length * 0.2, FACING_H / 2.0),
                               fc.P(length * 0.8, FACING_H / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waist Facing",
    )


def build():
    pattern = fc.PatternSet("pencil-skirt")
    front = _skirt_piece("front", front_dart, True, "Pencil Skirt Front")
    back = _skirt_piece("back", back_dart, False, "Pencil Skirt Back")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if target_piece == "waistband" or (everything and waistband_style == "band"):
        pattern.add(_waistband(front, back))
    if target_piece == "facing" or (everything and waistband_style == "facing"):
        pattern.add(_facing(front, back))
    # Seam declarations guarded by which pieces actually exist in the set.
    have = {piece.name for piece in pattern.pieces}
    if {"front", "back"} <= have:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        waist_edges = [("front", "waist"), ("front", "waist"),
                       ("back", "waist"), ("back", "waist")]
        if "waistband" in have:
            pattern.declare_seam([("waistband", "bottom")], waist_edges,
                                 tol=2.5, ease=OVERLAP + 2.0 * seam_allowance)
        if "facing" in have:
            pattern.declare_seam([("facing", "bottom")], waist_edges,
                                 tol=2.5, ease=2.0 * seam_allowance)
    pattern.metadata = {
        "fc100_rank": 32,
        "fabric_hint": "popelina-algodon",
        "waistband_style": waistband_style,
        "vent": {"height_mm": vent_height, "underlap_mm": VENT_W},
        "drafting": "mini-skirt block carried to knee length with a stronger pencil taper; "
                    "CB vent keeps the tapered hem walkable; waistband_style selects band "
                    "vs clean waist facing, each verified against the full waist seam",
    }
    return pattern


result = build()
