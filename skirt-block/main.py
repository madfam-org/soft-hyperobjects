"""
Straight Skirt Block — Fashion Cabinet Enabler Cartridge (not FC-100 counted).

The woven bottom-block primitive: front on fold, back in two panels with a
CB seam carrying a zipper notch, waist darts as internal markings, curved
side seams over the hip, equal sides by construction. Provider of the
`waistband` interface (verified against waistband-block in CI) and the
parent geometry for the FC-100 skirt family.

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


target_piece = str(PARAM(lambda: target_piece, "set"))

waist_girth  = float(PARAM(lambda: waist_girth, 700.0))
hip_girth    = float(PARAM(lambda: hip_girth, 940.0))
skirt_length = float(PARAM(lambda: skirt_length, 600.0))
hip_depth    = float(PARAM(lambda: hip_depth, 200.0))
hip_ease     = float(PARAM(lambda: hip_ease, 40.0))
waist_ease   = float(PARAM(lambda: waist_ease, 20.0))
front_dart   = float(PARAM(lambda: front_dart, 20.0))
back_dart    = float(PARAM(lambda: back_dart, 28.0))
zipper_length = float(PARAM(lambda: zipper_length, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(waist_girth, min(hip_girth, 1700.0))
skirt_length = max(300.0, min(skirt_length, 950.0))
hip_depth = max(140.0, min(hip_depth, min(260.0, skirt_length - 80.0)))
front_dart = max(0.0, min(front_dart, 45.0))
back_dart = max(0.0, min(back_dart, 50.0))
zipper_length = max(100.0, min(zipper_length, skirt_length * 0.6))

QH = (hip_girth + hip_ease) / 4.0
HIP_Y = skirt_length - hip_depth
SIDE_RISE = 12.0


def _skirt_piece(name, dart_intake, dart_len, center_fold, label):
    # Common side-waist point for BOTH pieces (average suppression) so the
    # side seams match exactly; per-piece dart intakes stay as internals.
    quarter_waist = (waist_girth + waist_ease) / 4.0
    waist_w = min(quarter_waist + (front_dart + back_dart) / 2.0, QH - 5.0)
    origin = fc.P(0.0, 0.0)
    top = fc.P(0.0, skirt_length)
    waist_out = fc.P(waist_w, skirt_length + SIDE_RISE)
    hip_pt = fc.P(QH, HIP_Y)
    edges = [
        fc.Edge("center", [fc.Line(origin, top)]),
        fc.Edge("waist", [fc.curve_through(top, waist_out, bulge=0.05, side=-1.0)]),
        fc.Edge(
            "side",
            [fc.Bezier(waist_out, fc.P(waist_w + (QH - waist_w) * 0.55, skirt_length - 40.0),
                       fc.P(QH, HIP_Y + hip_depth * 0.35), hip_pt),
             fc.Line(hip_pt, fc.P(QH, 0.0))],
        ),
        fc.Edge("hem", [fc.Line(fc.P(QH, 0.0), origin)]),
    ]
    notches = [fc.Notch("side", 0.5, "hip line")]
    allowances = {"hem": hem_allowance}
    if center_fold:
        cut = fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True)
    else:
        cut = fc.CutSpec(quantity=2, mirror=True)
        allowances["center"] = 20.0                    # CB seam with zipper
        notches.append(fc.Notch("center", 1.0 - zipper_length / skirt_length, "zipper stop"))
    dart_cx = waist_w * 0.55
    internals = []
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


def build():
    pattern = fc.PatternSet("skirt-block")
    front = _skirt_piece("front", front_dart, 90.0, True, "Skirt Front")
    back = _skirt_piece("back", back_dart, 110.0, False, "Skirt Back")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "enabler": True,
        "interface": "waistband",
        "zipper_length_mm": zipper_length,
        "drafting": "straight skirt block; darts internal; CB zipper notch",
    }
    return pattern


result = build()
