"""
Wrap Skirt — FC-100 rank #81. Fashion Cabinet Garment Cartridge.

A-line wrap skirt with no zipper: the back cuts on fold like the skirt-block
front; ONE front piece cuts twice mirrored, its center edge extended past CF
by `wrap_extension`, so the pair becomes the overlap and underlap panels; two
straight-grain waist ties close the wrap. Flare replaces the darts. A notch
on the front waist marks the CF wrap line; front and back share identical
side-seam geometry, declared and verified as a seam.

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

waist_girth    = float(PARAM(lambda: waist_girth, 700.0))
hip_girth      = float(PARAM(lambda: hip_girth, 940.0))
skirt_length   = float(PARAM(lambda: skirt_length, 600.0))
wrap_extension = float(PARAM(lambda: wrap_extension, 180.0))   # past CF
flare_mm       = float(PARAM(lambda: flare_mm, 70.0))          # A-line hem flare per side
waist_ease     = float(PARAM(lambda: waist_ease, 20.0))
hip_ease       = float(PARAM(lambda: hip_ease, 40.0))
tie_length     = float(PARAM(lambda: tie_length, 800.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(waist_girth, min(hip_girth, 1700.0))
skirt_length = max(350.0, min(skirt_length, 950.0))
wrap_extension = max(60.0, min(wrap_extension, waist_girth / 3.0))
flare_mm = max(0.0, min(flare_mm, 200.0))
tie_length = max(400.0, min(tie_length, 1400.0))

QH = (hip_girth + hip_ease) / 4.0
WAIST_W = min((waist_girth + waist_ease) / 4.0, QH - 5.0)
HIP_DEPTH = min(200.0, skirt_length - 150.0)
HIP_Y = skirt_length - HIP_DEPTH
SIDE_RISE = 12.0
HEM_X = QH + flare_mm
TIE_WIDTH = 40.0


def _side_edge():
    # ONE construction used verbatim by front and back so the declared side
    # seam matches by construction: skirt-block's hip curve, then the A-line
    # flare line from hip to hem instead of the straight drop.
    return fc.Edge(
        "side",
        [fc.Bezier(fc.P(WAIST_W, skirt_length + SIDE_RISE),
                   fc.P(WAIST_W + (QH - WAIST_W) * 0.55, skirt_length - 40.0),
                   fc.P(QH, HIP_Y + HIP_DEPTH * 0.35), fc.P(QH, HIP_Y)),
         fc.Line(fc.P(QH, HIP_Y), fc.P(HEM_X, 0.0))],
    )


def _waist_curve():
    return fc.curve_through(fc.P(0.0, skirt_length),
                            fc.P(WAIST_W, skirt_length + SIDE_RISE), bulge=0.05, side=-1.0)


def build_front():
    # Center edge sits wrap_extension past CF (x = 0); the waist runs level
    # across the extension, then curves up to the side like the back waist.
    waist_segs = [
        fc.Line(fc.P(-wrap_extension, skirt_length), fc.P(0.0, skirt_length)),
        _waist_curve(),
    ]
    waist = fc.Edge("waist", waist_segs)
    # CF notch: physical point wrap_extension in from the center edge, as an
    # arc-length fraction of the measured waist edge length.
    t_cf = waist_segs[0].length() / waist.length()
    edges = [
        fc.Edge("center", [fc.Line(fc.P(-wrap_extension, 0.0),
                                   fc.P(-wrap_extension, skirt_length))]),
        waist,
        _side_edge(),
        fc.Edge("hem", [fc.Line(fc.P(HEM_X, 0.0), fc.P(-wrap_extension, 0.0))]),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", t_cf, "CF wrap line"),
                 fc.Notch("side", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(QH * 0.55, 60.0), fc.P(QH * 0.55, skirt_length - 90.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),   # the pair = overlap + underlap
        label="Wrap Front",
    )


def build_back():
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, skirt_length))]),
        fc.Edge("waist", [_waist_curve()]),
        _side_edge(),
        fc.Edge("hem", [fc.Line(fc.P(HEM_X, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(QH * 0.55, 60.0), fc.P(QH * 0.55, skirt_length - 90.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt Back",
    )


def build_tie():
    w = TIE_WIDTH
    return fc.Piece(
        "tie",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(tie_length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(tie_length, 0.0), fc.P(tie_length, w))]),
            fc.Edge("top", [fc.Line(fc.P(tie_length, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(tie_length * 0.2, w / 2.0),
                               fc.P(tie_length * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Waist Tie",
    )


def build():
    pattern = fc.PatternSet("wrap-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "ties":
        pattern.add(build_tie())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    fabric_width = 1450.0                       # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0) for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.65)   # 65% marker efficiency
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 65% marker efficiency"},
        {"item": "sewing thread (poly)", "qty": 1, "unit": "spool",
         "note": "topstitch the wrap edge"},
    ]
    pattern.metadata = {
        "fc100_rank": 81,
        "fabric_hint": "popelina-algodon",
        "drafting": "A-line wrap: back on fold; one front cut 2 mirror, center edge "
                    "wrap_extension past CF; flare replaces darts; tie closure, no zipper",
    }
    return pattern


result = build()
