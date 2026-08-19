"""
Peasant Top — Fashion Cabinet Garment Cartridge (FC-200 #186, neckline gap).

The peasant (folk) top: a loose blouse gathered onto an elasticated or drawstring neckline that
can be worn on or off the shoulder, with full gathered sleeves ending in elastic or a cuff — the
European/Latin American folk-blouse line. Built as wide gathered front+back panels (their top
edges gathered to the neck casing) plus a full gathered sleeve. The volume is the gather; front
and back share the body width so the side seams balance by construction.

Pieces:
  - front / back : wide gathered body panels (cut on fold), top edge gathered to neck casing.
  - sleeve       : full gathered sleeve (cut 2 mirror), gathered at head and cuff.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|set

chest_girth  = float(PARAM(lambda: chest_girth, 960.0))
top_length   = float(PARAM(lambda: top_length, 560.0))
neck_gather  = float(PARAM(lambda: neck_gather, 1.7))      # body top width / finished neck
sleeve_len   = float(PARAM(lambda: sleeve_len, 420.0))
sleeve_gather = float(PARAM(lambda: sleeve_gather, 1.8))   # sleeve fullness
ease         = float(PARAM(lambda: ease, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(660.0, min(chest_girth, 1500.0))
top_length   = max(360.0, min(top_length, 820.0))
neck_gather  = max(1.3, min(neck_gather, 2.6))
sleeve_len   = max(120.0, min(sleeve_len, 620.0))
sleeve_gather = max(1.3, min(sleeve_gather, 2.6))
ease         = max(80.0, min(ease, 420.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
TOP_HALF = HALF * neck_gather / 1.4                   # gathered top edge is wider than body
ARMHOLE_DROP = 200.0


def _panel(name, label):
    top_y = L
    internals = [fc.Internal("neck-casing", [fc.P(0.0, top_y), fc.P(TOP_HALF, top_y)],
                             kind="marking")]
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("neck", [fc.Line(fc.P(0.0, top_y), fc.P(TOP_HALF, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(TOP_HALF, top_y), fc.P(HALF, top_y - ARMHOLE_DROP))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, top_y - ARMHOLE_DROP), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("neck", 0.5, "gather centre"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve():
    sw = sleeve_len
    head_w = ARMHOLE_DROP * sleeve_gather              # gathered sleevehead (wide)
    cuff_w = head_w * 0.7
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, head_w))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(0.0, head_w), fc.P(sw, (head_w + cuff_w) / 2.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(sw, (head_w + cuff_w) / 2.0),
                                     fc.P(sw, (head_w - cuff_w) / 2.0))]),
            fc.Edge("underarm", [fc.Line(fc.P(sw, (head_w - cuff_w) / 2.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 0.5, "shoulder gather")],
        grainline=fc.Grainline(fc.P(sw * 0.3, head_w / 2.0), fc.P(sw * 0.7, head_w / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (gathered)",
    )


def build():
    pattern = fc.PatternSet("peasant-top")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_panel("front", "Front"))
    if everything or target_piece == "back":
        pattern.add(_panel("back", "Back"))
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything:
        # the neck edges gather to a common casing; the sewn balanced seam is the side.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "light cotton, lawn, or gauze",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; a light fabric gathers softly."},
        {"item": "neck + sleeve elastic or drawstring", "qty": 1, "unit": "set",
         "note": "elastic or a drawstring at the neck (wear on/off shoulder) and at the cuffs."},
        {"item": "all-purpose + gathering thread", "qty": 1, "unit": "set",
         "note": "gather the panels and sleeves onto their casings."},
    ]
    pattern.metadata = {
        "fc200_rank": 186, "family": "woven_tops", "fabric_hint": "algodon-gasa",
        "silhouette_note": "A loose folk blouse gathered onto an elasticated/drawstring neckline "
            "(wearable on or off the shoulder) with full gathered sleeves. The gather is the "
            "volume; front and back share the body width so the side seams balance.",
        "solved": {"body_half_mm": round(HALF, 1), "top_gather_half_mm": round(TOP_HALF, 1),
                   "neck_gather": neck_gather, "sleeve_gather": sleeve_gather},
    }
    return pattern


result = build()
