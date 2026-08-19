"""
Thobe / Thawb — Fashion Cabinet Garment Cartridge (FC-200 rank #159, Arabian Peninsula
and wider heritage).

The thobe (thawb, dishdasha, kandura) is the ankle-length tunic-robe worn across the Arabian
Peninsula and much of the Arab world: a long, modest T-cut body with long sleeves, a stand or
placket neck, and side gores (godets) that widen the hem for an unbroken, flowing line. This
cartridge drafts the GARMENT GEOMETRY — a rectangular T-body (back on fold + front on fold),
long straight sleeves, and triangular side gores — in the straight-seam idiom where the body
side seam and gore edges balance by construction. The regional neck/cuff treatments (the Gulf
tarboosh tassel, embroidered plackets) are the maker's and are not reproduced here. Offered
with respect for the living tradition.

Pieces:
  - back   : back body, cut on fold at CB.
  - front  : front body, cut on fold at CF (with a marked neck placket).
  - sleeve : long straight sleeve, cut 2 mirror.
  - gore   : triangular side gore, cut 2 mirror (one per side seam).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # back|front|sleeve|gore|set

chest_girth   = float(PARAM(lambda: chest_girth, 1100.0))  # full chest
robe_length   = float(PARAM(lambda: robe_length, 1400.0))  # nape to ankle
neck_girth    = float(PARAM(lambda: neck_girth, 420.0))    # full neck
sleeve_length = float(PARAM(lambda: sleeve_length, 580.0)) # shoulder to wrist
sleeve_width  = float(PARAM(lambda: sleeve_width, 200.0))  # sleeve opening (half, flat)
gore_flare    = float(PARAM(lambda: gore_flare, 220.0))    # extra hem width added by each gore
gore_rise     = float(PARAM(lambda: gore_rise, 700.0))     # how high up the side the gore starts
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth   = max(750.0, min(chest_girth, 1700.0))
robe_length   = max(1000.0, min(robe_length, 1650.0))
neck_girth    = max(300.0, min(neck_girth, 560.0))
sleeve_length = max(350.0, min(sleeve_length, 700.0))
sleeve_width  = max(140.0, min(sleeve_width, 300.0))
gore_flare    = max(80.0, min(gore_flare, 400.0))
gore_rise     = max(400.0, min(gore_rise, 1000.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = robe_length
BODY = chest_girth + 200.0                     # modest, roomy ease built in
BW = (BODY / 2.0) / 2.0                          # quarter → each on-fold half-panel width
NECK_SCOOP = max(70.0, neck_girth / 5.0)
BACK_NECK_DROP = 20.0
FRONT_NECK_DROP = 70.0
SLEEVE_DEPTH = 260.0                              # dropped-shoulder armhole height
GORE_H = gore_rise                                # gore edge length up the side (below armhole)


def build_back():
    neck_top = fc.P(0.0, L)
    neck_out = fc.P(NECK_SCOOP, L)
    back_bulge = BACK_NECK_DROP / max(NECK_SCOOP, 1.0)
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            fc.Edge("neck", [fc.curve_through(neck_top, neck_out, bulge=back_bulge, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, L), fc.P(BW, L - SLEEVE_DEPTH))]),
            fc.Edge("side_upper", [fc.Line(fc.P(BW, L - SLEEVE_DEPTH), fc.P(BW, GORE_H))]),
            fc.Edge("side_gore", [fc.Line(fc.P(BW, GORE_H), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"),
                 fc.Notch("side_gore", 1.0, "gore top")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    neck_out = fc.P(NECK_SCOOP, L)
    cf_neck = fc.P(0.0, L - FRONT_NECK_DROP)
    # marked neck placket down the CF
    internals = [fc.Internal("neck-placket",
                             [cf_neck, fc.P(0.0, L - FRONT_NECK_DROP - 180.0)], kind="marking")]
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), cf_neck)]),
            fc.Edge("neck", [fc.curve_through(cf_neck, neck_out, bulge=0.12, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, L), fc.P(BW, L - SLEEVE_DEPTH))]),
            fc.Edge("side_upper", [fc.Line(fc.P(BW, L - SLEEVE_DEPTH), fc.P(BW, GORE_H))]),
            fc.Edge("side_gore", [fc.Line(fc.P(BW, GORE_H), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"),
                 fc.Notch("side_gore", 1.0, "gore top")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (neck placket)",
    )


def build_sleeve():
    sw = sleeve_length
    head_h = SLEEVE_DEPTH
    opening = sleeve_width
    # tapered sleeve: sleevehead (armhole side) height = SLEEVE_DEPTH, wrist = opening
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - opening) / 2.0))]),
            fc.Edge("wrist", [fc.Line(fc.P(sw, (head_h - opening) / 2.0),
                                      fc.P(sw, (head_h + opening) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + opening) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_gore():
    # Triangular side gore: apex at the gore top, base = gore_flare at the hem. The two
    # long seam edges each have length GORE_H (== the body's side_gore edge) so the seam
    # balances; the apex height falls out of that constraint (isosceles triangle with
    # equal sides GORE_H and base gore_flare). The flare is the base width.
    half_base = gore_flare / 2.0
    apex_h = math.sqrt(max(GORE_H * GORE_H - half_base * half_base, 1.0))
    return fc.Piece(
        "gore",
        [
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, apex_h), fc.P(-half_base, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(-half_base, 0.0), fc.P(half_base, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(half_base, 0.0), fc.P(0.0, apex_h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("seam_a", 0.0, "gore top")],
        grainline=fc.Grainline(fc.P(0.0, apex_h * 0.2), fc.P(0.0, apex_h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side gore",
    )


def build():
    pattern = fc.PatternSet("thobe")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces or target_piece == "gore":
        pattern.add(build_gore())
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side_upper"), ("back", "side_upper"), tol=1.0)
        # the gore sews between front & back side_gore edges (both == GORE_H)
        pattern.declare_seam(("gore", "seam_a"), ("back", "side_gore"), tol=1.0)
        pattern.declare_seam(("gore", "seam_b"), ("front", "side_gore"), tol=1.0)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "fine cotton / poly-cotton (thobe cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 74% marker; long T-body + gores + sleeves."},
        {"item": "neck placket interfacing", "qty": 1, "unit": "as needed",
         "note": "the front placket / stand is interfaced; treatment is the maker's."},
        {"item": "placket closure (buttons or concealed)", "qty": 1, "unit": "set",
         "note": "the neck placket closes with small buttons or a concealed strip."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "straight seams + gores."},
    ]
    pattern.metadata = {
        "fc200_rank": 159,
        "family": "heritage_global",
        "fabric_hint": "algodon-fino",
        "heritage_note": "The thobe (thawb, dishdasha, kandura) is living dress across the "
            "Arabian Peninsula and the wider Arab world. This cartridge drafts the GARMENT "
            "GEOMETRY only — the regional neck/cuff treatments, plackets, and tassel details "
            "that carry identity are the maker's and are not reproduced here. With respect.",
        "construction": "rectangular T-body (front + back on fold) with long tapered sleeves "
            "and triangular side gores for hem flare; straight side/gore seams balance by "
            "construction.",
        "solved": {"body_half_mm": round(BW, 1), "gore_rise_mm": round(GORE_H, 1),
                   "gore_flare_mm": round(gore_flare, 1), "robe_length_mm": round(L, 1)},
    }
    return pattern


result = build()
