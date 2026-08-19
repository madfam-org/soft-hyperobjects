"""
Huipil — Fashion Cabinet Garment Cartridge (FC-200 rank #137, MX heritage).

The huipil is one of the oldest and most widely worn Indigenous garments of Mexico and
Central America: a rectangular tunic assembled from straight-woven webs (traditionally
woven to width on a backstrap loom), joined by straight seams, with a neck opening cut or
woven into the top. Its identity is RECTANGULAR CONSTRUCTION and the economy of the
web — the artistry lives in the woven/embroidered bands, not in shaped seams.

This cartridge drafts the *garment geometry* — two rectangular panels, a boat/keyhole
neck, straight shoulder seams, and side seams left open above the waist for the arms —
so a maker can cut and construct a huipil to measure. It carries the woven/embroidered
decoration as marked bands, not as engineered seams. Offered with respect for the
living traditions it comes from; the maker supplies the cultural design.

Pieces (all rectangles):
  - front : one panel, cut on fold at CF, with a front-neck scoop.
  - back  : one panel, cut on fold at CB, with a shallower back-neck scoop.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|set

chest_girth   = float(PARAM(lambda: chest_girth, 960.0))    # full chest girth
huipil_length = float(PARAM(lambda: huipil_length, 900.0))  # shoulder to finished hem
neck_width    = float(PARAM(lambda: neck_width, 200.0))     # boat-neck opening width
neck_drop     = float(PARAM(lambda: neck_drop, 60.0))       # front-neck scoop depth
web_ease      = float(PARAM(lambda: web_ease, 160.0))       # total width ease (loose tunic)
arm_opening   = float(PARAM(lambda: arm_opening, 240.0))    # unsewn side length for the arm
band_depth    = float(PARAM(lambda: band_depth, 120.0))     # decorative neck-band depth (marked)
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth   = max(650.0, min(chest_girth, 1500.0))
huipil_length = max(500.0, min(huipil_length, 1300.0))
neck_width    = max(120.0, min(neck_width, 360.0))
neck_drop     = max(10.0, min(neck_drop, 160.0))
web_ease      = max(80.0, min(web_ease, 400.0))
arm_opening   = max(150.0, min(arm_opening, 400.0))
band_depth    = max(0.0, min(band_depth, 250.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = huipil_length
HALF = (chest_girth + web_ease) / 2.0 / 2.0        # each panel is cut on fold: half-width
NECK_HALF = neck_width / 2.0


def _panel(name, neck_dip, label):
    """One rectangular panel cut on fold at centre. Top edge: a straight shoulder from
    the neck-opening point out to the armhole corner, then the boat-neck scoop from the
    neck point to centre. Sides straight; hem straight."""
    top_y = L
    neck_center = fc.P(0.0, top_y - neck_dip)          # CF/CB neck point (scoop lowers it)
    neck_out = fc.P(NECK_HALF, top_y)                  # shoulder-neck point
    neck = fc.Edge("neck", [fc.curve_through(neck_center, neck_out,
                                             bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)])
    internals = []
    if band_depth > 0.0:
        # A marked decorative band running across the panel below the neck (the woven /
        # embroidered field the maker fills).
        by = top_y - neck_dip - band_depth
        internals.append(fc.Internal("neck-band",
                                     [fc.P(0.0, by), fc.P(HALF, by)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_center)]),
            neck,
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(HALF, top_y))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, top_y), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", arm_opening / L, "arm opening bottom"),
                 fc.Notch("shoulder", 1.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 80.0), fc.P(HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("huipil")
    front = _panel("front", neck_drop, "Front Panel")
    back = _panel("back", neck_drop * 0.4, "Back Panel")

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)

    if all_pieces:
        # Straight shoulder seams (front shoulder ↔ back shoulder) and the side seams
        # BELOW the arm opening (front side ↔ back side) both balance by construction —
        # they are equal-length straight verticals. Declare them for the seam-parity
        # lane the way every FC garment does.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "woven web (manta or backstrap-woven cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 70% marker; traditionally woven to width on a "
                 "backstrap loom, then the panels seamed selvedge-to-selvedge."},
        {"item": "embroidery / brocade thread", "qty": 1, "unit": "as needed",
         "note": "the neck band and body field carry the maker's woven or embroidered design."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "straight seams only."},
    ]
    pattern.metadata = {
        "fc200_rank": 137,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "heritage_note": "The huipil is a living Indigenous garment of Mexico and Central "
            "America. This cartridge drafts the rectangular GARMENT GEOMETRY only — the "
            "woven and embroidered designs that give each huipil its community identity are "
            "the maker's to supply, and are not reproduced here. Offered with respect for "
            "the traditions it comes from.",
        "rectangular_economy": "Two straight-edged panels cut on fold, joined by straight "
            "shoulder and side seams, sides left open above the waist for the arms — the "
            "economy of the woven web with almost no waste.",
        "drafting": "boat/keyhole neck by a shallow scoop; straight shoulders; side seams "
            "open above the arm-opening notch; decorative neck band marked, not seamed.",
    }
    return pattern


result = build()
