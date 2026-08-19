"""
Tube Top — Fashion Cabinet Garment Cartridge (FC-200 #187, neckline gap).

The tube (bandeau) top: a simple strapless band of stretch fabric around the bust, held by an
elasticated top and bottom edge — the simplest possible top. Drafted as a single wrapped panel
(front + back are one continuous tube on the stretch) whose flat width is the bust minus negative
ease (so it grips), with elastic casings top and bottom. Distinct from FC-100's camisole/crop-top
(which have straps). Front and back are the same panel; the one join seam is a real balanced seam.

Pieces:
  - band : the tube panel (cut on fold at CB; the two ends join at CF or a side).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # band|set

bust_girth   = float(PARAM(lambda: bust_girth, 900.0))
band_length  = float(PARAM(lambda: band_length, 260.0))    # top edge to bottom edge
neg_ease     = float(PARAM(lambda: neg_ease, 80.0))        # negative ease so it grips (stretch)
casing       = float(PARAM(lambda: casing, 18.0))          # elastic casing depth top+bottom
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(640.0, min(bust_girth, 1400.0))
band_length  = max(140.0, min(band_length, 520.0))
neg_ease     = max(0.0, min(neg_ease, 180.0))
casing       = max(0.0, min(casing, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# tube flat width on fold = (bust - neg_ease) / 2 (the CB fold halves the full circumference)
HALF = (bust_girth - neg_ease) / 2.0
L = band_length


def build_band():
    internals = []
    if casing > 0.0:
        internals.append(fc.Internal("top-casing", [fc.P(0.0, L - casing), fc.P(HALF, L - casing)],
                                     kind="marking"))
        internals.append(fc.Internal("bottom-casing", [fc.P(0.0, casing), fc.P(HALF, casing)],
                                     kind="marking"))
    return fc.Piece(
        "band",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, L), fc.P(HALF, L))]),
            fc.Edge("join", [fc.Line(fc.P(HALF, L), fc.P(HALF, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 1.0, "join"), fc.Notch("bottom", 0.0, "join")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 20.0), fc.P(HALF * 0.5, L - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Tube band",
    )


def build():
    pattern = fc.PatternSet("tube-top")
    pattern.add(build_band())
    # the band is cut on the CB fold and its two 'join' ends meet at CF: a real balanced seam
    # (the join edge sews to its mirror). Model it as a self-seam for the checker.
    pattern.declare_seam(("band", "join"), ("band", "center_back"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "stretch knit (ITY, rib, or swim tricot)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 82% marker; negative ease means it MUST stretch to grip."},
        {"item": "top + bottom elastic", "qty": 1, "unit": "set",
         "note": "elastic in both casings holds the tube up; length is the maker's to fit."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "one join seam; coverstitch or zigzag the casings."},
    ]
    pattern.metadata = {
        "fc200_rank": 187, "family": "knit_tops", "fabric_hint": "punto-ity",
        "silhouette_note": "A strapless stretch band around the bust, elasticated top and bottom "
            "— the simplest possible top. Cut with negative ease so it grips; front and back are "
            "the same panel with one balanced join seam.",
        "solved": {"flat_half_mm": round(HALF, 1), "neg_ease_mm": round(neg_ease, 1)},
    }
    return pattern


result = build()
