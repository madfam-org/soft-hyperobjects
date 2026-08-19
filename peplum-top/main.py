"""
Peplum Top — Fashion Cabinet Garment Cartridge (FC-200 #160, everyday silhouette gap).

A fitted darted bodice seamed at the natural waist to a flared PEPLUM — a short circular
flounce that stands away from the body over the hip. The peplum is drafted as a partial
annulus (a ring segment) whose inner arc equals the bodice waist so the waist seam balances,
and whose outer arc gives the flare. Front and back bodice share the structural waist width,
so the shoulder and side seams balance by construction; bust/back shaping is kept as internal
dart markings over the common seam (the blouse's shared-side-point idiom).

Pieces:
  - front / back : fitted bodice halves (cut on fold), dart-marked, waist-seamed.
  - peplum       : flared ring-segment flounce (cut on fold), inner arc == bodice waist.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|peplum|set

bust_girth   = float(PARAM(lambda: bust_girth, 920.0))     # full bust
waist_girth  = float(PARAM(lambda: waist_girth, 740.0))    # fitted waist
bodice_len   = float(PARAM(lambda: bodice_len, 360.0))     # shoulder to waist seam
peplum_len   = float(PARAM(lambda: peplum_len, 220.0))     # waist seam to peplum hem
peplum_flare = float(PARAM(lambda: peplum_flare, 1.7))     # outer arc / inner arc
neck_width   = float(PARAM(lambda: neck_width, 180.0))     # neckline width
sleeve_cap   = float(PARAM(lambda: sleeve_cap, 60.0))      # small grown cap
bust_dart    = float(PARAM(lambda: bust_dart, 22.0))       # marked bust dart intake
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(680.0, min(bust_girth, 1500.0))
waist_girth  = max(540.0, min(waist_girth, 1300.0))
bodice_len   = max(300.0, min(bodice_len, 460.0))
peplum_len   = max(120.0, min(peplum_len, 400.0))
peplum_flare = max(1.2, min(peplum_flare, 2.6))
neck_width   = max(130.0, min(neck_width, 300.0))
sleeve_cap   = max(0.0, min(sleeve_cap, 180.0))
bust_dart    = max(0.0, min(bust_dart, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

BUST_HALF  = (bust_girth / 2.0) / 2.0     # quarter (on-fold half-panel)
WAIST_HALF = (waist_girth / 2.0) / 2.0
NECK_HALF  = neck_width / 2.0
SHOULDER   = BUST_HALF + sleeve_cap
ARMSCYE_DROP = 200.0


def build_bodice(name, neck_dip, dart_label, label):
    top_y = bodice_len
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    waist_side = fc.P(WAIST_HALF, 0.0)
    internals = []
    if bust_dart > 0.0 and name == "front":
        # bust dart marked from the side toward the apex (does not open the seam)
        apex = fc.P(WAIST_HALF * 0.55, top_y - ARMSCYE_DROP - 30.0)
        internals.append(fc.Internal("bust-dart",
                                     [fc.P(BUST_HALF, top_y - ARMSCYE_DROP - 10.0), apex],
                                     kind="dart"))
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
        fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot, bulge=0.16, side=-1.0)]),
        fc.Edge("side", [fc.Line(armscye_bot, waist_side)]),
        fc.Edge("waist", [fc.Line(waist_side, fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("waist", 1.0, "side")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 40.0), fc.P(WAIST_HALF * 0.5, top_y - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_peplum():
    """A quarter-annulus flounce (cut on fold at CF). Inner arc length == bodice waist
    quarter (WAIST_HALF) so the waist seam balances; outer arc = inner * flare. Modelled
    as a ring segment sampled into a smooth polyline so the seam checker measures true
    arc lengths."""
    inner_arc = WAIST_HALF
    # choose an inner radius so the segment subtends a sensible angle; angle = arc/r.
    r_in = max(inner_arc / math.radians(90.0), 60.0)   # ~quarter-circle sweep
    theta = inner_arc / r_in                            # radians actually subtended
    r_out = r_in + peplum_len
    # scale the outer radius so outer_arc == inner_arc * flare over the SAME theta
    r_out = (inner_arc * peplum_flare) / theta
    r_out = max(r_out, r_in + peplum_len * 0.5)          # ensure real depth
    n = 24
    inner_pts = [fc.P(r_in * math.cos(theta * i / n), r_in * math.sin(theta * i / n))
                 for i in range(n + 1)]
    outer_pts = [fc.P(r_out * math.cos(theta * i / n), r_out * math.sin(theta * i / n))
                 for i in range(n + 1)]
    # edges: inner arc (waist), side_b (radial), outer arc (hem), side_a (radial, at fold)
    inner_edge = fc.Edge("waist", [fc.Line(inner_pts[i], inner_pts[i + 1]) for i in range(n)])
    side_b = fc.Edge("side", [fc.Line(inner_pts[n], outer_pts[n])])
    outer_edge = fc.Edge("hem", [fc.Line(outer_pts[n - i], outer_pts[n - i - 1]) for i in range(n)])
    side_a = fc.Edge("center", [fc.Line(outer_pts[0], inner_pts[0])])
    return fc.Piece(
        "peplum",
        [inner_edge, side_b, outer_edge, side_a],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "centre front")],
        grainline=fc.Grainline(fc.P(r_in + 20.0, 10.0), fc.P(r_out - 20.0, 10.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Peplum flounce",
    )


def build():
    pattern = fc.PatternSet("peplum-top")
    all_pieces = target_piece == "set"
    front = build_bodice("front", 66.0, "bust", "Bodice Front")
    back = build_bodice("back", 24.0, "back", "Bodice Back")
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "peplum":
        pattern.add(build_peplum())
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "crisp woven (poplin / cotton-sateen)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; a crisp hand holds the peplum's stand."},
        {"item": "lightweight interfacing (neck/waist)", "qty": 1, "unit": "as needed",
         "note": "stabilises the neckline and the waist seam the peplum hangs from."},
        {"item": "invisible zip or back keyhole + button", "qty": 1, "unit": "set",
         "note": "a fitted bodice needs an opening; maker's choice."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + dart."},
    ]
    pattern.metadata = {
        "fc200_rank": 160, "family": "woven_tops", "fabric_hint": "popelina",
        "silhouette_note": "A fitted darted bodice seamed at the natural waist to a flared "
            "circular peplum. The peplum is a ring segment whose inner arc equals the bodice "
            "waist (balanced seam) and whose outer arc gives the stand-away flare.",
        "solved": {"waist_quarter_mm": round(WAIST_HALF, 1), "peplum_flare": peplum_flare,
                   "peplum_len_mm": round(peplum_len, 1)},
    }
    return pattern


result = build()
