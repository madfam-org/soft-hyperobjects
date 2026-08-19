"""
Pinafore Dress — Fashion Cabinet Garment Cartridge (FC-200 #163, everyday silhouette gap).

A pinafore (jumper) dress: a bib front + low back bodice held by over-shoulder straps that
cross at the back and button, seamed at the waist to a gathered or A-line skirt. Worn over a
top or blouse. The bodice is simple and open at the sides (the straps and the waist seam hold
it), so there is no fitted side seam to balance; the skirt is a gathered rectangle whose waist
equals the body waist. Straps are self-fabric strips (BOM).

Pieces:
  - bib    : the front bib bodice panel (cut on fold).
  - back   : the low back bodice panel (cut on fold).
  - skirt  : gathered skirt rectangle (cut on fold), gathered to the waist.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # bib|back|skirt|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))    # body waist (skirt attaches here)
bib_width    = float(PARAM(lambda: bib_width, 260.0))      # bib width across the chest
bib_height   = float(PARAM(lambda: bib_height, 240.0))     # waist to top of the bib
back_height  = float(PARAM(lambda: back_height, 170.0))    # waist to top of the low back
skirt_length = float(PARAM(lambda: skirt_length, 640.0))   # waist to hem
gather_ratio = float(PARAM(lambda: gather_ratio, 1.9))     # skirt fullness
strap_width  = float(PARAM(lambda: strap_width, 45.0))     # over-shoulder strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(500.0, min(waist_girth, 1300.0))
bib_width    = max(160.0, min(bib_width, 420.0))
bib_height   = max(140.0, min(bib_height, 380.0))
back_height  = max(100.0, min(back_height, 320.0))
skirt_length = max(300.0, min(skirt_length, 1000.0))
gather_ratio = max(1.3, min(gather_ratio, 3.0))
strap_width  = max(25.0, min(strap_width, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

BIB_HALF = bib_width / 2.0
SKIRT_W = waist_girth * gather_ratio
SKIRT_HALF = SKIRT_W / 2.0


def build_bib():
    top_y = bib_height
    internals = [fc.Internal("strap-attach",
                             [fc.P(BIB_HALF - strap_width, top_y), fc.P(BIB_HALF, top_y)],
                             kind="marking")]
    return fc.Piece(
        "bib",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, top_y), fc.P(BIB_HALF, top_y))]),
            fc.Edge("side", [fc.Line(fc.P(BIB_HALF, top_y), fc.P(BIB_HALF, 0.0))]),
            fc.Edge("waist", [fc.Line(fc.P(BIB_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 1.0, "side"), fc.Notch("top", 1.0, "strap")],
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 20.0), fc.P(BIB_HALF * 0.5, top_y - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Bib front",
    )


def build_back():
    top_y = back_height
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, top_y), fc.P(BIB_HALF, top_y))]),
            fc.Edge("side", [fc.Line(fc.P(BIB_HALF, top_y), fc.P(BIB_HALF, 0.0))]),
            fc.Edge("waist", [fc.Line(fc.P(BIB_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 1.0, "side"), fc.Notch("top", 1.0, "strap button")],
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 20.0), fc.P(BIB_HALF * 0.5, top_y - 20.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back bodice",
    )


def build_skirt():
    L = skirt_length
    internals = [fc.Internal("waist-gather", [fc.P(0.0, L), fc.P(SKIRT_HALF, L)], kind="marking")]
    return fc.Piece(
        "skirt",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(SKIRT_HALF, L))]),
            fc.Edge("side", [fc.Line(fc.P(SKIRT_HALF, L), fc.P(SKIRT_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(SKIRT_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "quarter"), fc.Notch("side", 1.0, "waist")],
        grainline=fc.Grainline(fc.P(SKIRT_HALF * 0.5, 80.0), fc.P(SKIRT_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt",
    )


def build():
    pattern = fc.PatternSet("pinafore-dress")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "bib":
        pattern.add(build_bib())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "skirt":
        pattern.add(build_skirt())
    # bib & back are open at the sides (held by straps + waist seam) — no fitted side seam.

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "corduroy, denim, or firm cotton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; a sturdy pinafore fabric."},
        {"item": "over-shoulder straps (self fabric)", "qty": 2, "unit": "strips",
         "note": "cross at the back and button to the back bodice; length is the maker's."},
        {"item": "strap buttons", "qty": 2, "unit": "pcs",
         "note": "the crossed straps button to the low back."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + gathering."},
    ]
    pattern.metadata = {
        "fc200_rank": 163, "family": "dresses_jumpsuits", "fabric_hint": "pana-mezclilla",
        "silhouette_note": "A bib front + low back bodice on over-shoulder straps that cross at "
            "the back and button, seamed at the waist to a gathered skirt. Open at the sides "
            "(straps + waist seam hold it), worn over a top; skirt waist == body waist.",
        "solved": {"skirt_full_width_mm": round(SKIRT_W, 1),
                   "waist_girth_mm": round(waist_girth, 1),
                   "gather_ratio": gather_ratio},
    }
    return pattern


result = build()
