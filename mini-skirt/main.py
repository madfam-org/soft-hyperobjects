"""
Mini Skirt — FC-100 rank #35. Fashion Cabinet Garment Cartridge.

The straight skirt block shortened above the knee and slightly tapered: the
hem half-width pulls in `taper_mm` from the hip half-width, and the walking
ease the taper removes comes back as a CB back vent — two parallel marked
lines rising `vent_height` from the hem, 40 mm apart, beside the CB seam on
the back piece. Front on fold with one waist dart per half; back in two
panels with a CB zipper notch, one dart per panel and the vent internals; a
straight cut-1 waistband with a 30 mm overlap is sized off the measured
waist seam and verified with an eased multi-edge check. Front and back share
one side-waist construction so the declared side seams match exactly.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|waistband|set

waist_girth  = float(PARAM(lambda: waist_girth, 700.0))
hip_girth    = float(PARAM(lambda: hip_girth, 940.0))
skirt_length = float(PARAM(lambda: skirt_length, 420.0))
hip_depth    = float(PARAM(lambda: hip_depth, 190.0))
taper_mm     = float(PARAM(lambda: taper_mm, 12.0))
hip_ease     = float(PARAM(lambda: hip_ease, 30.0))
waist_ease   = float(PARAM(lambda: waist_ease, 15.0))
front_dart   = float(PARAM(lambda: front_dart, 18.0))
back_dart    = float(PARAM(lambda: back_dart, 22.0))
vent_height  = float(PARAM(lambda: vent_height, 120.0))
zipper_length = float(PARAM(lambda: zipper_length, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(waist_girth, min(hip_girth, 1700.0))
skirt_length = max(260.0, min(skirt_length, 520.0))
hip_depth = max(140.0, min(hip_depth, min(260.0, skirt_length - 80.0)))
taper_mm = max(0.0, min(taper_mm, 40.0))
front_dart = max(0.0, min(front_dart, 45.0))
back_dart = max(0.0, min(back_dart, 50.0))
vent_height = max(60.0, min(vent_height, skirt_length * 0.45))
zipper_length = max(100.0, min(zipper_length, skirt_length * 0.6))

QH = (hip_girth + hip_ease) / 4.0
HIP_Y = skirt_length - hip_depth
SIDE_RISE = 12.0
OVERLAP = 30.0     # waistband hook/button overlap
BAND_H = 38.0      # finished waistband height (folds double)
VENT_W = 40.0      # vent underlap width beside the CB


def _skirt_piece(name, dart_intake, dart_len, center_fold, label):
    # Common side-waist point for BOTH pieces (average suppression) so the
    # side seams match exactly; per-piece dart intakes stay as internals.
    quarter_waist = (waist_girth + waist_ease) / 4.0
    waist_w = min(quarter_waist + (front_dart + back_dart) / 2.0, QH - 5.0)
    origin = fc.P(0.0, 0.0)
    top = fc.P(0.0, skirt_length)
    waist_out = fc.P(waist_w, skirt_length + SIDE_RISE)
    hip_pt = fc.P(QH, HIP_Y)
    hem_out = fc.P(QH - taper_mm, 0.0)                 # tapered hem half-width
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
        # CB vent: fold line on the CB seam, underlap edge VENT_W inside —
        # the walking ease the tapered hem removes comes back here.
        internals.append(fc.Internal(
            "back vent fold", [fc.P(0.0, 0.0), fc.P(0.0, vent_height)]))
        internals.append(fc.Internal(
            "back vent edge", [fc.P(VENT_W, 0.0), fc.P(VENT_W, vent_height)]))
    dart_cx = waist_w * 0.55
    if dart_intake > 0.5:
        internals.append(fc.Internal(
            f"{name} waist dart",
            [fc.P(dart_cx - dart_intake / 2.0, skirt_length + SIDE_RISE * 0.5),
             fc.P(dart_cx, skirt_length - dart_len),
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


def build():
    pattern = fc.PatternSet("mini-skirt")
    front = _skirt_piece("front", front_dart, 85.0, True, "Mini Skirt Front")
    back = _skirt_piece("back", back_dart, 105.0, False, "Mini Skirt Back")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(_waistband(front, back))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("front", "waist"), ("back", "waist"), ("back", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )
    pattern.metadata = {
        "fc100_rank": 35,
        "fabric_hint": "mezclilla-denim",
        "vent": {"height_mm": vent_height, "underlap_mm": VENT_W},
        "drafting": "skirt block shortened and tapered taper_mm at the hem; CB vent restores "
                    "walking ease; cut-1 waistband eased over the full waist seam",
    }
    return pattern


result = build()
