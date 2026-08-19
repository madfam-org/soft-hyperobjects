"""
Maternity Dress — Fashion Cabinet Garment Cartridge (FC-200 rank #152, maternity).

An empire-waist maternity dress: a fitted bodice to just under the bust, seamed to a
gently gathered A-line skirt that falls over and grows with the bump. The high empire seam
+ the skirt's flare give room without a tent shape. A soft-goods garment — no hardware.

Pieces:
  - bodice : front + back to the empire line (cut on fold), short grown sleeves.
  - skirt  : a gathered A-line skirt panel (cut on fold), empire to hem.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # bodice_front|bodice_back|skirt|set

bust_girth   = float(PARAM(lambda: bust_girth, 960.0))
under_bust   = float(PARAM(lambda: under_bust, 800.0))    # empire seam sits here
dress_length = float(PARAM(lambda: dress_length, 1000.0))
empire_rise  = float(PARAM(lambda: empire_rise, 340.0))   # shoulder to empire seam
neck_width   = float(PARAM(lambda: neck_width, 180.0))
sleeve_grown = float(PARAM(lambda: sleeve_grown, 130.0))
skirt_flare  = float(PARAM(lambda: skirt_flare, 1.9))     # skirt width / empire (fullness)
bust_ease    = float(PARAM(lambda: bust_ease, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(700.0, min(bust_girth, 1400.0))
under_bust   = max(600.0, min(under_bust, bust_girth))
dress_length = max(700.0, min(dress_length, 1500.0))
empire_rise  = max(250.0, min(empire_rise, 450.0))
neck_width   = max(120.0, min(neck_width, 320.0))
sleeve_grown = max(40.0, min(sleeve_grown, 220.0))
skirt_flare  = max(1.4, min(skirt_flare, 3.0))
bust_ease    = max(20.0, min(bust_ease, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

BODICE_HALF = (bust_girth + bust_ease) / 2.0 / 2.0
EMPIRE_HALF = (under_bust + bust_ease) / 2.0 / 2.0
SKIRT_HALF = EMPIRE_HALF * skirt_flare
NECK_HALF = neck_width / 2.0
SLEEVE_X = BODICE_HALF + sleeve_grown
SKIRT_L = dress_length - empire_rise


def _bodice(name, neck_dip, label):
    top_y = empire_rise
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 90.0)
    underarm = fc.P(BODICE_HALF, top_y - 160.0)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),  # 0 = empire seam
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
        fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
        fc.Edge("sleeve_under", [fc.Line(sleeve_bot, underarm)]),
        fc.Edge("side", [fc.Line(underarm, fc.P(EMPIRE_HALF, 0.0))]),
        fc.Edge("empire", [fc.Line(fc.P(EMPIRE_HALF, 0.0), fc.P(0.0, 0.0))]),  # seams to skirt
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"), fc.Notch("empire", 0.5, "CF/CB")],
        grainline=fc.Grainline(fc.P(BODICE_HALF * 0.5, 30.0),
                               fc.P(BODICE_HALF * 0.5, empire_rise - 40.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_skirt():
    """A gathered A-line skirt: gathered at the empire seam (SKIRT_HALF wide) flaring to
    the hem, cut on fold at CF/CB."""
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, SKIRT_L))]),
        fc.Edge("empire", [fc.Line(fc.P(0.0, SKIRT_L), fc.P(SKIRT_HALF, SKIRT_L))]),  # gathered
        fc.Edge("side", [fc.Line(fc.P(SKIRT_HALF, SKIRT_L), fc.P(SKIRT_HALF + 60.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(SKIRT_HALF + 60.0, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "skirt", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("empire", 0.5, "quarter (gather)")],
        grainline=fc.Grainline(fc.P(SKIRT_HALF * 0.4, 80.0),
                               fc.P(SKIRT_HALF * 0.4, SKIRT_L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt (empire → hem)",
    )


def build():
    pattern = fc.PatternSet("maternity-dress")
    bf = _bodice("bodice_front", 80.0, "Bodice Front")
    bb = _bodice("bodice_back", 25.0, "Bodice Back")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "bodice_front":
        pattern.add(bf)
    if all_pieces or target_piece == "bodice_back":
        pattern.add(bb)
    if all_pieces or target_piece == "skirt":
        pattern.add(build_skirt())
    if all_pieces:
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"), tol=1.5)
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.5)
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "soft drapey knit or woven", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1500 mm width, 68% marker; drapey for the bump."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "gather the skirt to the empire seam; no hardware."},
    ]
    pattern.metadata = {
        "fc200_rank": 152, "family": "dresses_jumpsuits", "fabric_hint": "tricot-nylon-elastano",
        "maternity_note": "Empire-waist: a fitted bodice to just under the bust seamed to a "
            "gathered A-line skirt (flare " + str(round(skirt_flare, 1)) + "x) that falls over "
            "and grows with the bump. High empire seam + skirt flare give room without a tent "
            "shape. No hardware.",
        "solved": {"skirt_full_half_mm": round(SKIRT_HALF, 1),
                   "empire_half_mm": round(EMPIRE_HALF, 1)},
    }
    return pattern


result = build()
