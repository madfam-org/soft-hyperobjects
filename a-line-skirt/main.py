"""
A-Line Skirt — FC-100 rank #33 (Falda línea A).

First flare of the skirt family, same construction as the straight skirt
block — front on fold, back in two panels with a CB seam carrying a zipper
notch — but dartless: the waist suppression the block pins into darts is
swung into the side seam, which curves out over the hip and flares from the
hip point to a hem wider than the hip. Front and back share one side-seam
construction, so the declared side seam matches exactly.

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
flare_mm     = float(PARAM(lambda: flare_mm, 80.0))
waist_ease   = float(PARAM(lambda: waist_ease, 20.0))
hip_ease     = float(PARAM(lambda: hip_ease, 40.0))
zipper_length = float(PARAM(lambda: zipper_length, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(waist_girth, min(hip_girth, 1700.0))
skirt_length = max(300.0, min(skirt_length, 950.0))
flare_mm = max(30.0, min(flare_mm, 300.0))
zipper_length = max(100.0, min(zipper_length, skirt_length * 0.6))

QH = (hip_girth + hip_ease) / 4.0
HIP_DEPTH = 200.0                # body waist-to-hip; ≤ skirt_length − 80 for all clamped lengths
HIP_Y = skirt_length - HIP_DEPTH
SIDE_RISE = 12.0


def _skirt_piece(name, center_fold, label):
    # Dartless by design: the full quarter suppression (QH − quarter waist)
    # is absorbed by the side seam — curved over the hip, then flared as a
    # straight run from the hip point to a hem flare_mm wider than QH. The
    # Bezier's arrival tangent is aligned with the flare direction so the
    # seam blends through the hip. One construction for BOTH pieces, so the
    # side seams match exactly.
    quarter_waist = (waist_girth + waist_ease) / 4.0
    waist_w = min(quarter_waist, QH - 5.0)
    origin = fc.P(0.0, 0.0)
    top = fc.P(0.0, skirt_length)
    waist_out = fc.P(waist_w, skirt_length + SIDE_RISE)
    hip_pt = fc.P(QH, HIP_Y)
    hem_out = fc.P(QH + flare_mm, 0.0)
    flare_in = hip_pt - (hem_out - hip_pt).normalized() * (HIP_DEPTH * 0.35)
    edges = [
        fc.Edge("center", [fc.Line(origin, top)]),
        fc.Edge("waist", [fc.curve_through(top, waist_out, bulge=0.05, side=-1.0)]),
        fc.Edge(
            "side",
            [fc.Bezier(waist_out, fc.P(waist_w + (QH - waist_w) * 0.55, skirt_length - 40.0),
                       flare_in, hip_pt),
             fc.Line(hip_pt, hem_out)],
        ),
        fc.Edge("hem", [fc.Line(hem_out, origin)]),
    ]
    notches = [fc.Notch("side", 0.5, "side match")]
    allowances = {"hem": hem_allowance}
    if center_fold:
        cut = fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True)
    else:
        cut = fc.CutSpec(quantity=2, mirror=True)
        allowances["center"] = 20.0                    # CB seam with zipper
        notches.append(fc.Notch("center", 1.0 - zipper_length / skirt_length, "zipper stop"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=notches,
        grainline=fc.Grainline(fc.P(QH * 0.55, 60.0), fc.P(QH * 0.55, skirt_length - 90.0)),
        cut=cut,
        label=label,
    )


def build():
    pattern = fc.PatternSet("a-line-skirt")
    front = _skirt_piece("front", True, "A-Line Front")
    back = _skirt_piece("back", False, "A-Line Back")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 33,
        "fabric_hint": "popelina-algodon",
        "drafting": "dartless A-line from the skirt block; suppression swung into the side "
                    "curve; hip-pivot flare; straight hem (sweep truing deferred)",
    }
    return pattern


result = build()
