"""
Tiered Dress — Fashion Cabinet Garment Cartridge (FC-200 #174, dress silhouette gap).

The gathered tiered (prairie) dress: a simple bodice seamed to a skirt of stacked rectangular
tiers, each tier wider than the one above and gathered onto it, so fullness grows toward the
hem. Distinct from FC-100's dresses (none are tiered). The bodice front/back share the waist
width so shoulder and side seams balance; each tier is a plain rectangle whose gathered top is
marked — the gather (not shaping) makes the volume.

Pieces:
  - bodice_front / bodice_back : simple bodice halves (cut on fold), waist-seamed.
  - tier1 / tier2 / tier3      : stacked gathered rectangles (cut on fold), each wider.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # bodice|tiers|set

bust_girth   = float(PARAM(lambda: bust_girth, 940.0))
waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
bodice_len   = float(PARAM(lambda: bodice_len, 380.0))     # shoulder to waist
skirt_length = float(PARAM(lambda: skirt_length, 720.0))   # waist to hem (all tiers)
neck_width   = float(PARAM(lambda: neck_width, 190.0))
tier_growth  = float(PARAM(lambda: tier_growth, 1.5))      # each tier wider than the last by x
sleeve_grown = float(PARAM(lambda: sleeve_grown, 130.0))
ease         = float(PARAM(lambda: ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(680.0, min(bust_girth, 1400.0))
waist_girth  = max(560.0, min(waist_girth, 1300.0))
bodice_len   = max(300.0, min(bodice_len, 470.0))
skirt_length = max(400.0, min(skirt_length, 1100.0))
neck_width   = max(140.0, min(neck_width, 320.0))
tier_growth  = max(1.2, min(tier_growth, 2.0))
sleeve_grown = max(0.0, min(sleeve_grown, 260.0))
ease         = max(40.0, min(ease, 360.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

BUST_HALF  = (bust_girth + ease) / 4.0
WAIST_HALF = (waist_girth + ease) / 4.0
NECK_HALF  = neck_width / 2.0
SHOULDER   = BUST_HALF + sleeve_grown
ARMSCYE_DROP = 200.0
TIER_H = skirt_length / 3.0                          # three equal-depth tiers
# tier top widths: tier1 top == bodice waist (half, on fold); grows down
T1 = WAIST_HALF
T2 = T1 * tier_growth
T3 = T2 * tier_growth


def build_bodice(name, neck_dip, label):
    top_y = bodice_len
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    waist_side = fc.P(WAIST_HALF, 0.0)
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                                 bulge=0.16, side=-1.0)]),
            fc.Edge("side", [fc.Line(armscye_bot, waist_side)]),
            fc.Edge("waist", [fc.Line(waist_side, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("waist", 1.0, "side")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 40.0), fc.P(WAIST_HALF * 0.5, top_y - 60.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_tier(name, half_w, is_hem, label):
    h = TIER_H
    internals = [fc.Internal("gather-top", [fc.P(0.0, h), fc.P(half_w, h)], kind="marking")]
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(half_w, h))]),
            fc.Edge("side", [fc.Line(fc.P(half_w, h), fc.P(half_w, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(half_w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance} if is_hem else {},
        notches=[fc.Notch("top", 0.5, "centre"), fc.Notch("side", 1.0, "top")],
        grainline=fc.Grainline(fc.P(half_w * 0.5, 20.0), fc.P(half_w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("tiered-dress")
    everything = target_piece == "set"
    if everything or target_piece == "bodice":
        pattern.add(build_bodice("bodice_front", 60.0, "Bodice Front"))
        pattern.add(build_bodice("bodice_back", 24.0, "Bodice Back"))
    if everything or target_piece == "tiers":
        pattern.add(build_tier("tier1", T1, False, "Tier 1 (waist)"))
        pattern.add(build_tier("tier2", T2, False, "Tier 2 (middle)"))
        pattern.add(build_tier("tier3", T3, True, "Tier 3 (hem)"))
    if everything:
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"), tol=1.0)
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "light cotton lawn / voile / double gauze",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 74% marker; a light fabric keeps the gathered tiers soft."},
        {"item": "back closure (buttons or zip)", "qty": 1, "unit": "set",
         "note": "the bodice opens at CB; maker's choice."},
        {"item": "all-purpose + gathering thread", "qty": 1, "unit": "set",
         "note": "gather each tier's top onto the piece above; the gather is the volume."},
    ]
    pattern.metadata = {
        "fc200_rank": 174, "family": "dresses_jumpsuits", "fabric_hint": "algodon-voile",
        "silhouette_note": "A simple bodice over three stacked rectangular tiers, each wider "
            "than the one above and gathered onto it, so fullness grows toward the hem. The "
            "gather (not shaping) makes the volume; the bodice side/shoulder seams balance.",
        "solved": {"tier_widths_half_mm": [round(T1, 1), round(T2, 1), round(T3, 1)],
                   "tier_growth": tier_growth},
    }
    return pattern


result = build()
