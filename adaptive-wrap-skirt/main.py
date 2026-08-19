"""
Adaptive Wrap Skirt — Fashion Cabinet Garment Cartridge (FC-200 #150, adaptive; magnetic-clasp).

A wrap skirt that closes with magnetic clasps instead of ties or a fiddly button — a
wide-wrap A-line panel whose overlap and waistband snap shut, so it can be fastened
one-handed, seated, or with limited fine-motor control. The magnetic-clasp SOLID is
Yantra4D territory (`magnetic-clasp`; see the manifest's notion.hardware_ref). Fashion
Cabinet owns the skirt + the clasp placement.

Pieces:
  - panel : the wrap skirt panel (front wrap + back, cut as one wide panel on fold at CB).
  - band  : the waistband, with marked clasp positions at the overlap.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # panel|band|set

waist_girth  = float(PARAM(lambda: waist_girth, 780.0))
hip_girth    = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 620.0))
wrap_overlap = float(PARAM(lambda: wrap_overlap, 280.0))  # how far the wrap crosses over
band_height  = float(PARAM(lambda: band_height, 45.0))
clasps       = int(  PARAM(lambda: clasps, 3))            # magnetic clasps at the overlap
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(550.0, min(waist_girth, 1400.0))
hip_girth    = max(650.0, min(hip_girth, 1500.0))
skirt_length = max(300.0, min(skirt_length, 1100.0))
wrap_overlap = max(150.0, min(wrap_overlap, 450.0))
band_height  = max(25.0, min(band_height, 90.0))
clasps       = max(2, min(clasps, 8))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

# The wrap panel spans the full hip + the overlap (it wraps past CF).
PANEL_W = hip_girth + wrap_overlap
L = skirt_length


def build_panel():
    """A wide wrap panel: waist at the top (PANEL_W flat, eased to the waistband), flaring
    slightly to the hem. Straight-drafted (the flare is the hem being wider)."""
    hem_w = PANEL_W + 120.0
    edges = [
        fc.Edge("start", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),       # wrap under-edge
        fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(PANEL_W, L))]),     # to the waistband
        fc.Edge("end", [fc.Line(fc.P(PANEL_W, L), fc.P(hem_w, 0.0))]),   # wrap over-edge
        fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", hip_girth / PANEL_W, "wrap point")],
        grainline=fc.Grainline(fc.P(PANEL_W * 0.3, 80.0), fc.P(PANEL_W * 0.3, L - 80.0)),
        cut=fc.CutSpec(quantity=1),
        label="Wrap Panel",
    )


def build_band():
    """The waistband, with magnetic-clasp positions marked at the overlap end (where the
    wrap closes) so it snaps shut instead of tying."""
    band_len = waist_girth + wrap_overlap + 40.0
    h = band_height * 2.0
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, h))]),
        fc.Edge("fold", [fc.Line(fc.P(band_len, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # Clasp positions along the overlap zone (last `wrap_overlap` of the band).
    for i in range(clasps):
        t = i / max(clasps - 1, 1)
        x = (waist_girth) + wrap_overlap * t
        internals.append(fc.Internal("clasp-mark",
                                     [fc.P(x - 5.0, band_height), fc.P(x + 5.0, band_height)],
                                     kind="drill"))
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", waist_girth / band_len, "wrap point")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, h / 2.0), fc.P(band_len * 0.8, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waistband (magnetic clasps)",
    )


def build():
    pattern = fc.PatternSet("adaptive-wrap-skirt")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "panel":
        pattern.add(build_panel())
    if all_pieces or target_piece == "band":
        pattern.add(build_band())
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "medium woven (skirt-weight)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1500 mm width, 70% marker."},
        {"item": "magnetic clasps", "qty": clasps, "unit": "sets",
         "note": "Yantra4D magnetic-clasp (see notion.hardware_ref) at the wrap overlap."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "no ties, no buttons."},
    ]
    pattern.metadata = {
        "fc200_rank": 150, "family": "skirts", "fabric_hint": "popelina-algodon",
        "adaptive_note": "A wrap skirt that closes with magnetic clasps instead of ties or "
            "buttons, so it fastens one-handed, seated, or with limited fine-motor control. "
            "Clasp positions are marked at the wrap overlap; the printable clasp is the "
            "Yantra4D solid.",
        "hardware": "wrap closure via Yantra4D (notion.hardware_ref -> magnetic-clasp)",
    }
    return pattern


result = build()
