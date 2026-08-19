"""
Godet Skirt — Fashion Cabinet Garment Cartridge (FC-200 #179, skirt gap).

The godet skirt: a slim skirt with triangular godets (flared inserts) set into seams or slashes
so the hem flares dramatically while the hip stays close — a mermaid/trumpet line. This cartridge
drafts a slim front+back panel (shared straight side seam, balances by construction) and a
triangular godet whose two seam edges are equal (isosceles, so each godet seam balances), set to
start partway up the skirt. Distinct from FC-100's straight and gathered skirts — the flare comes
from inserted wedges, not gathering or a circle.

Pieces:
  - front / back : slim skirt panels (cut on fold), slash lines marked for the godets.
  - godet        : triangular flared insert (cut several), isosceles seam edges.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|godet|set

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
hip_girth    = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 720.0))
godet_rise   = float(PARAM(lambda: godet_rise, 380.0))     # how far up the godet reaches
godet_flare  = float(PARAM(lambda: godet_flare, 260.0))    # hem width each godet adds
godets       = int(  PARAM(lambda: godets, 6))             # number of godets (sets the count)
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(520.0, min(waist_girth, 1300.0))
hip_girth    = max(700.0, min(hip_girth, 1500.0))
skirt_length = max(450.0, min(skirt_length, 1200.0))
godet_rise   = max(200.0, min(godet_rise, 700.0))
godet_flare  = max(100.0, min(godet_flare, 450.0))
godets       = max(2, min(godets, 12))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

WAIST_HALF = waist_girth / 4.0
HIP_HALF   = hip_girth / 4.0
L = skirt_length
HIP_Y = L - 200.0                                    # hip line


def _panel(name, godet_count_here, label):
    # slim panel: waist -> hip out -> straight down; side is a straight vertical (balances)
    side_pts = [fc.P(WAIST_HALF, L), fc.P(HIP_HALF, HIP_Y), fc.P(HIP_HALF, 0.0)]
    internals = []
    # slash lines where godets go (marked; the godet is a separate inserted piece)
    for i in range(godet_count_here):
        x = HIP_HALF * (i + 1) / (godet_count_here + 1)
        internals.append(fc.Internal(f"godet-slash-{i}",
                                     [fc.P(x, 0.0), fc.P(x, godet_rise)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(WAIST_HALF, L))]),
            fc.Edge("side", [fc.Line(side_pts[0], side_pts[1]), fc.Line(side_pts[1], side_pts[2])]),
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "side"), fc.Notch("side", 0.5, "hip")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 60.0), fc.P(WAIST_HALF * 0.5, L - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_godet():
    # isosceles triangle: apex at the top of the slash (godet_rise up), base = godet_flare at hem.
    # equal seam edges = godet_rise so each sews to a godet_rise-long slash side (balanced).
    half_base = godet_flare / 2.0
    apex_h = math.sqrt(max(godet_rise * godet_rise - half_base * half_base, 1.0))
    return fc.Piece(
        "godet",
        [
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, apex_h), fc.P(-half_base, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(-half_base, 0.0), fc.P(half_base, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(half_base, 0.0), fc.P(0.0, apex_h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("seam_a", 0.0, "apex")],
        grainline=fc.Grainline(fc.P(0.0, apex_h * 0.2), fc.P(0.0, apex_h * 0.8)),
        cut=fc.CutSpec(quantity=godets, mirror=False),
        label="Godet insert",
    )


def build():
    pattern = fc.PatternSet("godet-skirt")
    everything = target_piece == "set"
    # split godet slashes between front (half) and back (half)
    gf = godets // 2
    gb = godets - gf
    if everything or target_piece == "front":
        pattern.add(_panel("front", max(gf - 1, 1), "Front (slashes)"))
    if everything or target_piece == "back":
        pattern.add(_panel("back", max(gb - 1, 1), "Back (slashes)"))
    if everything or target_piece == "godet":
        pattern.add(build_godet())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "fluid woven with drape (crepe, satin-back)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 70% marker; slim panels + " + str(godets) + " godets."},
        {"item": "invisible side zip", "qty": 1, "unit": "pc",
         "note": "the slim skirt closes at a side seam."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "set each godet into its slash to a stay-stitched point; press toward the panel."},
    ]
    pattern.metadata = {
        "fc200_rank": 179, "family": "skirts", "fabric_hint": "crepe-satin",
        "silhouette_note": "A slim skirt with triangular godets set into slashes: the hip stays "
            "close and the hem flares (mermaid/trumpet line). Each godet is isosceles with equal "
            "seam edges (== the slash length) so its seams balance; flare is inserted, not "
            "gathered.",
        "solved": {"waist_q_mm": round(WAIST_HALF, 1), "godets": godets,
                   "godet_flare_mm": round(godet_flare, 1), "godet_rise_mm": round(godet_rise, 1)},
    }
    return pattern


result = build()
