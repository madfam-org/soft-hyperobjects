"""
Palazzo pants — FC-100 rank #79. Fashion Cabinet Garment Cartridge.

A dramatically wide-leg pull-on trouser on the sweatpants side-seamed woven
block: separate front and back legs (cut 2 each) that flare from the hip to a
very wide hem, the front inseam bowed by a solved amount to match the deeper
back fork, equal side seams by construction (both outseams share one flared
curve, so the leg widens on BOTH edges toward the hem), a straight open hem,
and an elastic waistband CASING (a folded strip carrying the elastic through a
channel). Waist finish is a select: `elastic` (default, no opening) or
`side_zip`, which adds a left-side zip-stop notch and a zipper BOM line.

Hardware (the zipper) is a Yantra4D cartridge referenced in the BOM note, never
re-implemented here (federation contract). The waistband elastic is a soft
notion cut-to-waist, not hardware.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
closure = str(PARAM(lambda: closure, "elastic"))  # elastic | side_zip

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
inseam_length = float(PARAM(lambda: inseam_length, 760.0))
front_rise    = float(PARAM(lambda: front_rise, 260.0))
back_rise     = float(PARAM(lambda: back_rise, 310.0))
woven_ease    = float(PARAM(lambda: woven_ease, 120.0))
hem_width     = float(PARAM(lambda: hem_width, 380.0))     # front half-hem, flat
side_flare    = float(PARAM(lambda: side_flare, 90.0))     # outseam kick at hem
elastic_width = float(PARAM(lambda: elastic_width, 40.0))
zip_length    = float(PARAM(lambda: zip_length, 180.0))    # side-zip stop-to-stop
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

if closure not in ("elastic", "side_zip"):
    closure = "elastic"
hip_girth = max(650.0, min(hip_girth, 1800.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
woven_ease = max(60.0, min(woven_ease, 400.0))
hem_width = max(220.0, min(hem_width, 520.0))              # dramatic wide range
side_flare = max(0.0, min(side_flare, 200.0))
elastic_width = max(20.0, min(elastic_width, 70.0))
zip_length = max(120.0, min(zip_length, 300.0))

HIP_E = hip_girth + woven_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0
RISE_DELTA = back_rise - front_rise

OVERLAP = 30.0                                  # casing join/overlap allowance
BAND_H = 2.0 * (elastic_width + seam_allowance)  # flat casing height (folds to channel)


def _outseam():
    """Shared flared side seam: kicks out to x = -side_flare at the hem, up to
    (0, WAIST_Y) at the waist. Front and back share this exact curve, so the
    two outseams match by construction and the leg widens on the side too."""
    return fc.Edge(
        "side",
        [fc.curve_through(fc.P(-side_flare, 0.0), fc.P(0.0, WAIST_Y), bulge=0.0, side=-1.0)],
    )


def _front_inseam(bulge):
    return fc.Edge(
        "inseam",
        [fc.curve_through(fc.P(FW + FORK_F, CROTCH_Y), fc.P(FHW, 0.0), bulge=bulge, side=-1.0)],
    )


def _back_inseam():
    return fc.Edge(
        "inseam",
        [fc.curve_through(fc.P(BW + FORK_B, CROTCH_Y), fc.P(BHW, 0.0), bulge=0.0, side=-1.0)],
    )


def _solve_front_bulge():
    """Bow the front inseam outward until it matches the deeper back inseam."""
    back_len = _back_inseam().length(0.05)
    lo, hi = 0.0, 0.5
    for _ in range(50):
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(_front_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")
    return bulge


def _leg(name, width, fork, hem_w, cb_y, inseam_edge, label):
    fork_tip = fc.P(width + fork, CROTCH_Y)
    waist_in = width * 0.92
    side = _outseam()
    edges = [
        side,
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.45),
                       fc.P(width + (fork_tip.x - width) * 0.35, CROTCH_Y + 55.0), fork_tip)],
        ),
        inseam_edge,
        fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(-side_flare, 0.0))]),
    ]
    notches = [fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)]
    if closure == "side_zip" and name == "front":
        # Left-side zip: stop-notch measured down from the waist on the outseam.
        notches.append(fc.Notch("side", 1.0 - zip_length / side.length(0.05), "zip stop"))
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=notches,
        grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                               fc.P(width * 0.45, inseam_length * 0.92)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_legs():
    bulge = _solve_front_bulge()
    front = _leg("front", FW, FORK_F, FHW, WAIST_Y, _front_inseam(bulge), "Front Leg")
    back = _leg("back", BW, FORK_B, BHW, WAIST_Y + RISE_DELTA, _back_inseam(), "Back Leg")
    return front, back


def build_casing(front, back):
    """Elastic waistband casing, drafted as two mirror halves joined at the
    sides: each half's bottom = front waist + back waist, plus the join/overlap
    allowance carried as declared seam ease. The strip folds on its centre line
    to a channel; the elastic threads through and is cut shorter than the body."""
    waists = front.edge("waist").length() + back.edge("waist").length()
    length = waists + OVERLAP + 2.0 * seam_allowance
    cy = BAND_H / 2.0
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, BAND_H))]),
            fc.Edge("top", [fc.Line(fc.P(length, BAND_H), fc.P(0.0, BAND_H))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, BAND_H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, cy), fc.P(length * 0.8, cy)),
        internals=[fc.Internal("fold line", [fc.P(0.0, cy), fc.P(length, cy)])],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Waistband Casing (half)",
    )


def _fabric_bom(front, back, casing):
    """Rough single-layer woven yardage: two legs side by side + the casing.
    Fabric width assumed ~1500 mm; qty reported in metres of length used."""
    lo_f, hi_f = front.bbox()
    lo_b, hi_b = back.bbox()
    leg_h = max(hi_f.y - lo_f.y, hi_b.y - lo_b.y)
    length_mm = 2.0 * leg_h + (2.0 * (casing.edge("end_a").length()) + 40.0)
    return round(length_mm / 1000.0, 2)


def _elastic_len():
    """Waist elastic cut length: ~0.9 of the waist girth so it gathers the
    fuller pull-on waist to the body. Approximated from hip since palazzos are
    drafted to hip; honest teaching value, tune to the wearer."""
    return round(hip_girth * 0.9, 0)


def build():
    pattern = fc.PatternSet("palazzo-pants")
    front, back = build_legs()
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    casing = build_casing(front, back)
    if everything or target_piece == "waistband":
        pattern.add(casing)
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        pattern.declare_seam(
            [("waistband", "bottom")],
            [("front", "waist"), ("back", "waist")],
            tol=2.5,
            ease=OVERLAP + 2.0 * seam_allowance,
        )

    yardage = _fabric_bom(front, back, casing)
    elastic_len = _elastic_len()
    pattern.bom = [
        {"item": "Woven fabric (popelina/manta)", "qty": yardage, "unit": "m",
         "note": "single-layer estimate at ~1500 mm width; "
                 "drape-friendly plain weave for the wide leg"},
        {"item": "Waistband elastic", "qty": elastic_len, "unit": "mm",
         "note": f"soft notion, cut to ~0.9x waist ({elastic_width:.0f} mm wide); "
                 "threaded through the folded casing channel, not hardware"},
        {"item": "All-purpose thread", "qty": 1, "unit": "spool",
         "note": "construction + hems"},
    ]
    if closure == "side_zip":
        pattern.bom.append(
            {"item": "Invisible zipper", "qty": 1, "unit": "pc",
             "note": f"{zip_length:.0f} mm, LEFT side seam; hard good — see Yantra4D "
                     "zipper cartridge (notion.hardware_ref), not modelled here"}
        )

    pattern.metadata = {
        "fc100_rank": 79,
        "fabric_hint": "popelina-algodon",
        "closure": closure,
        "hem_half_width_front_mm": round(front.edge("hem").length(0.05), 1),
        "hem_half_width_back_mm": round(back.edge("hem").length(0.05), 1),
        "hem_circumference_mm": round(2.0 * (front.edge("hem").length(0.05)
                                             + back.edge("hem").length(0.05)), 1),
        "side_seam_mm": round(front.edge("side").length(0.05), 1),
        "front_inseam_bulge": round(_solve_front_bulge(), 4),
        "waist_elastic_cut_mm": elastic_len,
        "drafting": "wide-leg pull-on trouser on the sweatpants side-seamed block; "
                    "leg flares on both outseam and inseam to the hem; front inseam bow "
                    "solved to the deeper back; teaching-grade (no shaped waistband, "
                    "no pockets, elastic cut length approximated from hip)",
    }
    return pattern


result = build()
