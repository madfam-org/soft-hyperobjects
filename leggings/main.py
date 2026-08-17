"""
Leggings — FC-100 rank #7. Fashion Cabinet Garment Cartridge.

Side-seamless knit leggings: ONE piece per leg (side line on the fold of the
draft, front half right, back half left), cut with NEGATIVE ease, plus a
diamond gusset and an elastic waistband casing derived from the measured
waist edge. The back fork is deeper than the front, so the front inseam is
bowed outward by a solved amount until both inseams match exactly — the
cartridge's second numeric solve after rank #1's sleeve cap.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # leg|gusset|waistband|set

waist_girth   = float(PARAM(lambda: waist_girth, 700.0))
hip_girth     = float(PARAM(lambda: hip_girth, 940.0))
inseam_length = float(PARAM(lambda: inseam_length, 700.0))
side_rise     = float(PARAM(lambda: side_rise, 250.0))     # crotch line to waist at side
ankle_girth   = float(PARAM(lambda: ankle_girth, 220.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 8.0))  # body-hugging stretch
back_rise_extra   = float(PARAM(lambda: back_rise_extra, 40.0))   # raised CB
waistband_height  = float(PARAM(lambda: waistband_height, 35.0))
waistband_ratio   = float(PARAM(lambda: waistband_ratio, 0.95))
include_gusset    = bool(PARAM(lambda: include_gusset, True))
seam_allowance    = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance     = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(600.0, min(hip_girth, 1700.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
side_rise = max(160.0, min(side_rise, 380.0))
ankle_girth = max(140.0, min(ankle_girth, 420.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 15.0))
back_rise_extra = max(0.0, min(back_rise_extra, 80.0))

SCALE = 1.0 - negative_ease_pct / 100.0
hip_e = hip_girth * SCALE
waist_e = waist_girth * SCALE
ankle_e = ankle_girth * SCALE

CROTCH_Y = inseam_length
WAIST_Y = inseam_length + side_rise
FW = hip_e / 4.0 - 5.0            # front half-width at hip (piece x > 0)
BW = hip_e / 4.0 + 5.0            # back half-width (piece x < 0)
FWW = waist_e / 4.0 - 5.0
BWW = waist_e / 4.0 + 5.0
FORK_F = hip_e / 20.0             # front fork extension
FORK_B = hip_e / 10.0             # back fork extension (deeper)
AW = ankle_e / 4.0                # ankle half-width per side of the fold
FRONT_FORK_TIP = fc.P(FW + FORK_F, CROTCH_Y)
BACK_FORK_TIP = fc.P(-(BW + FORK_B), CROTCH_Y)


def _front_inseam(bulge):
    """Front inseam bowed outward by `bulge` (fraction of chord) to gain length."""
    return fc.Edge(
        "front_inseam",
        [fc.curve_through(fc.P(AW, 0.0), FRONT_FORK_TIP, bulge=bulge, side=-1.0)],
    )


def build_leg():
    back_len = fc.P(-AW, 0.0).distance(BACK_FORK_TIP)
    lo, hi = 0.0, 0.30
    for _ in range(44):                       # bow the front inseam to match the back
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(_front_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge to the back inseam length")
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-AW, 0.0), fc.P(AW, 0.0))]),
        _front_inseam(bulge),
        fc.Edge(
            "front_crotch",
            [fc.Bezier(FRONT_FORK_TIP, fc.P(FW + FORK_F * 0.25, CROTCH_Y + 45.0),
                       fc.P(FWW, WAIST_Y - side_rise * 0.55), fc.P(FWW, WAIST_Y))],
        ),
        fc.Edge("waist", [fc.Line(fc.P(FWW, WAIST_Y),
                                  fc.P(-BWW, WAIST_Y + back_rise_extra))]),
        fc.Edge(
            "back_crotch",
            [fc.Bezier(fc.P(-BWW, WAIST_Y + back_rise_extra),
                       fc.P(-BWW - 4.0, WAIST_Y - side_rise * 0.55),
                       fc.P(-(BW + FORK_B * 0.35), CROTCH_Y + 50.0), BACK_FORK_TIP)],
        ),
        fc.Edge("back_inseam", [fc.Line(BACK_FORK_TIP, fc.P(-AW, 0.0))]),
    ]
    return fc.Piece(
        "leg",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("front_inseam", 0.5), fc.Notch("back_inseam", 0.5)],
        grainline=fc.Grainline(fc.P(0.0, inseam_length * 0.15),
                               fc.P(0.0, inseam_length * 0.9)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Leg (side-seamless)",
    )


def build_gusset():
    w, h = 60.0, 150.0
    return fc.Piece(
        "gusset",
        [
            fc.Edge("front_a", [fc.Line(fc.P(0.0, -h / 2.0), fc.P(w / 2.0, 0.0))]),
            fc.Edge("front_b", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(0.0, h / 2.0))]),
            fc.Edge("back_a", [fc.Line(fc.P(0.0, h / 2.0), fc.P(-w / 2.0, 0.0))]),
            fc.Edge("back_b", [fc.Line(fc.P(-w / 2.0, 0.0), fc.P(0.0, -h / 2.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(0.0, -h * 0.3), fc.P(0.0, h * 0.3)),
        cut=fc.CutSpec(quantity=1),
        label="Gusset (diamond)",
    )


def build_waistband(leg):
    circ = 2.0 * leg.edge("waist").length()          # both legs make the full waist
    length = circ * waistband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * waistband_height
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (fold-over)",
    )


def build():
    pattern = fc.PatternSet("leggings")
    leg = build_leg()
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "leg":
        pattern.add(leg)
    if include_gusset and (all_pieces or target_piece == "gusset"):
        pattern.add(build_gusset())
    if all_pieces or target_piece == "waistband":
        pattern.add(build_waistband(leg))
    if all_pieces or target_piece == "leg":
        pattern.declare_seam(("leg", "front_inseam"), ("leg", "back_inseam"), tol=1.5)
    pattern.metadata = {
        "fc100_rank": 7,
        "fabric_hint": "jersey-algodon",
        "negative_ease_pct": negative_ease_pct,
        "drafting": "side-seamless leg; front inseam bow solved to the back inseam",
        "gusset_note": "diamond gusset seams into the fork junction; curve-fit to the "
                       "fork openings is a later refinement",
    }
    return pattern


result = build()
