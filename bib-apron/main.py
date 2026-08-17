"""
Bib Apron — FC-100 rank #91. Fashion Cabinet Garment Cartridge.

The simplest complete garment in the index: one body piece cut on fold with
a curved underarm sweep, neck strap and waist ties as straight-grain strips,
and a divided patch pocket. First-project material for the commons, and the
Wave-1 candidate for the First Garment ceremony.

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

bib_width    = float(PARAM(lambda: bib_width, 280.0))     # full bib width
waist_width  = float(PARAM(lambda: waist_width, 600.0))   # full width at waist
skirt_length = float(PARAM(lambda: skirt_length, 500.0))
bib_height   = float(PARAM(lambda: bib_height, 300.0))
tie_length   = float(PARAM(lambda: tie_length, 900.0))
strap_length = float(PARAM(lambda: strap_length, 520.0))
pocket_width = float(PARAM(lambda: pocket_width, 380.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

bib_width = max(180.0, min(bib_width, 420.0))
waist_width = max(bib_width + 80.0, min(waist_width, 900.0))
skirt_length = max(250.0, min(skirt_length, 800.0))
bib_height = max(180.0, min(bib_height, 420.0))
pocket_width = max(180.0, min(pocket_width, waist_width * 0.8))

HB, HW = bib_width / 2.0, waist_width / 2.0


def build_body():
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, -skirt_length), fc.P(0.0, bib_height))]),
        fc.Edge("bib_top", [fc.Line(fc.P(0.0, bib_height), fc.P(HB, bib_height))]),
        fc.Edge(
            "underarm",
            [fc.Bezier(fc.P(HB, bib_height), fc.P(HB + (HW - HB) * 0.15, bib_height * 0.45),
                       fc.P(HB + (HW - HB) * 0.55, 30.0), fc.P(HW, 0.0))],
        ),
        fc.Edge("side", [fc.Line(fc.P(HW, 0.0), fc.P(HW - 20.0, -skirt_length))]),
        fc.Edge("hem", [fc.Line(fc.P(HW - 20.0, -skirt_length), fc.P(0.0, -skirt_length))]),
    ]
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "bib_top": hem_allowance},
        notches=[fc.Notch("side", 0.0, "waist level"), fc.Notch("underarm", 1.0, "tie point")],
        grainline=fc.Grainline(fc.P(HB * 0.8, -skirt_length * 0.8),
                               fc.P(HB * 0.8, bib_height * 0.6)),
        internals=[fc.Internal(
            "pocket placement",
            [fc.P(0.0, -140.0), fc.P(pocket_width / 2.0, -140.0),
             fc.P(pocket_width / 2.0, -140.0 - 180.0), fc.P(0.0, -320.0)],
        )],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Apron Body",
    )


def _strip(name, length, width, qty, label):
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0), fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build_pocket():
    h = 200.0
    return fc.Piece(
        "pocket",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(pocket_width / 2.0, h))]),
            fc.Edge("side", [fc.Line(fc.P(pocket_width / 2.0, h), fc.P(pocket_width / 2.0, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(pocket_width / 2.0, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": 20.0},
        internals=[fc.Internal("divider stitch", [fc.P(0.0, 0.0), fc.P(0.0, h)])],
        grainline=fc.Grainline(fc.P(pocket_width * 0.25, 30.0),
                               fc.P(pocket_width * 0.25, h - 30.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Patch Pocket",
    )


def build():
    pattern = fc.PatternSet("bib-apron")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything or target_piece == "strips":
        pattern.add(_strip("neck_strap", strap_length, 40.0, 1, "Neck Strap"))
        pattern.add(_strip("waist_tie", tie_length, 40.0, 2, "Waist Tie"))
    pattern.metadata = {
        "fc100_rank": 91,
        "fabric_hint": "manta-cruda",
        "drafting": "one-piece bib apron on fold; First Garment ceremony candidate",
    }
    return pattern


result = build()
