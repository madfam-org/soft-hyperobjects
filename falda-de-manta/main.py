"""
Falda de Manta — Fashion Cabinet Garment Cartridge (FC-200 rank #140, MX heritage).

The falda de manta is the gathered skirt of traditional Mexican dress: wide widths of
manta (plain cotton) or woven cloth gathered onto a waistband, full and swishing, often
finished with embroidered or ribbon bands at the hem. Its construction is a rectangle
gathered to a band — the fullness is the point, and the decoration (deshilado drawn-work,
embroidery, listones/ribbons) is the maker's.

This cartridge drafts the garment geometry: a skirt rectangle whose width is the waist
times a gather ratio, gathered to a fitted waistband, with a marked hem-band. Offered
with respect for the living tradition.

Pieces:
  - skirt : one wide rectangle (cut on fold at CB), gathered at the top to the band.
  - band  : the fitted waistband strip.

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # skirt|band|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))   # fitted waist
skirt_length = float(PARAM(lambda: skirt_length, 850.0))  # waist to finished hem
gather_ratio = float(PARAM(lambda: gather_ratio, 2.4))    # skirt width / waist (fullness)
band_height  = float(PARAM(lambda: band_height, 40.0))    # finished waistband height
hem_band     = float(PARAM(lambda: hem_band, 100.0))      # marked embroidered/ribbon hem band
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(500.0, min(waist_girth, 1400.0))
skirt_length = max(400.0, min(skirt_length, 1200.0))
gather_ratio = max(1.5, min(gather_ratio, 3.5))
band_height  = max(20.0, min(band_height, 90.0))
hem_band     = max(0.0, min(hem_band, 300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

SKIRT_W = waist_girth * gather_ratio          # full gathered width (flat)
HALF_W = SKIRT_W / 2.0                          # cut on fold → half-width
L = skirt_length


def build_skirt():
    """The gathered skirt rectangle, cut on fold at CB. Top edge (gathered) is the full
    half-width; sides straight; hem straight with a marked decorative band."""
    internals = []
    if hem_band > 0.0:
        internals.append(fc.Internal("hem-band",
                                     [fc.P(0.0, hem_band), fc.P(HALF_W, hem_band)], kind="marking"))
    return fc.Piece(
        "skirt",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(HALF_W, L))]),   # gathered to the band
            fc.Edge("side", [fc.Line(fc.P(HALF_W, L), fc.P(HALF_W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "quarter (gather)"),
                 fc.Notch("side", 1.0, "waist")],
        grainline=fc.Grainline(fc.P(HALF_W * 0.5, 80.0), fc.P(HALF_W * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt",
    )


def build_band():
    """The fitted waistband: a strip the finished waist long (plus overlap), cut on fold
    lengthwise so it folds to the finished band_height."""
    band_len = waist_girth + 40.0                  # + underlap for the closure
    h = band_height * 2.0                            # cut double-height, folds to band_height
    return fc.Piece(
        "band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),  # to gathered waist
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, h))]),
            fc.Edge("fold", [fc.Line(fc.P(band_len, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.25, "quarter"), fc.Notch("attach", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, h / 2.0), fc.P(band_len * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("falda-de-manta")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "skirt":
        pattern.add(build_skirt())
    if all_pieces or target_piece == "band":
        pattern.add(build_band())

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "manta (plain cotton) or woven cloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 75% marker; the fullness comes from the gather ratio, "
                 "not from shaping — straight widths gathered to the band."},
        {"item": "hem decoration (deshilado / embroidery / listones)", "qty": 1,
         "unit": "as applied", "note": "drawn-work, embroidery, and ribbon bands: the maker's."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "straight seams + gathering."},
        {"item": "waist closure (hook or tie)", "qty": 1, "unit": "set",
         "note": "a hook-and-bar or a self tie at the band — maker's choice."},
    ]
    pattern.metadata = {
        "fc200_rank": 140,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "heritage_note": "The falda de manta is part of living Mexican traditional dress. "
            "This cartridge drafts the gathered GARMENT GEOMETRY only — the deshilado "
            "(drawn-work), embroidery, and ribbon (listón) decoration that carries regional "
            "identity is the maker's to supply and is not reproduced here. Offered with respect.",
        "gathered_fullness": "A rectangle gathered_ratio times the waist, gathered onto a "
            "fitted band; the fullness and the swish are the design — no shaped seams.",
        "solved": {"skirt_full_width_mm": round(SKIRT_W, 1),
                   "gather_ratio": gather_ratio, "waist_girth_mm": round(waist_girth, 1)},
        "drafting": "one gathered skirt rectangle on fold + a fitted double-height "
            "waistband; hem band marked for the maker's decoration.",
    }
    return pattern


result = build()
