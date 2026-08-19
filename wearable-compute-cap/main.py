"""
Wearable-Compute Cap — Fashion Cabinet Accessory Cartridge (FC-200 rank #147, y4d pi-hat-case).

A cap prepared to carry a single-board computer: a crown band + a peak, overlaid with an
ELECTRONICS POCKET whose opening is sized to the Yantra4D `pi-hat-case` enclosure, plus
marked cable routes to a rear battery loop. Fashion Cabinet owns the cap + the pocket
plan; Yantra4D owns the printable case.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # crown|peak|set

head_girth  = float(PARAM(lambda: head_girth, 580.0))     # head circumference
crown_depth = float(PARAM(lambda: crown_depth, 130.0))    # crown band height
peak_length = float(PARAM(lambda: peak_length, 70.0))     # peak projection
case_size   = float(PARAM(lambda: case_size, 70.0))       # electronics-pocket opening
ease        = float(PARAM(lambda: ease, 10.0))            # fit ease
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth  = max(500.0, min(head_girth, 640.0))
crown_depth = max(90.0, min(crown_depth, 180.0))
peak_length = max(40.0, min(peak_length, 100.0))
case_size   = max(40.0, min(case_size, 120.0))
ease        = max(0.0, min(ease, 30.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

head_eff = head_girth + ease


def build_crown():
    """The crown band: a rectangle head_eff wide x crown_depth, with a marked electronics
    pocket and cable routes on the (rear) inside face."""
    w, h = head_eff, crown_depth
    edges = [
        fc.Edge("seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),        # joins a crown top/closure
        fc.Edge("seam_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),  # headband edge
    ]
    # Electronics pocket at the back-centre (x = w/2).
    cx, cy = w / 2.0, h * 0.55
    hs = case_size / 2.0
    internals = [
        fc.Internal("electronics-pocket", [
            fc.P(cx - hs, cy - hs), fc.P(cx + hs, cy - hs),
            fc.P(cx + hs, cy + hs), fc.P(cx - hs, cy + hs), fc.P(cx - hs, cy - hs)],
            kind="marking"),
        # Cable route to a battery loop lower on the band.
        fc.Internal("cable-route", [fc.P(cx, cy - hs), fc.P(cx + 40.0, h * 0.2)], kind="trace"),
    ]
    return fc.Piece(
        "crown", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "centre back"), fc.Notch("bottom", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Crown Band (with electronics pocket)",
    )


def build_peak():
    """The peak: a half-ellipse cut on the back edge (fold) and mirrored."""
    half_w = head_eff * 0.22
    front = fc.Bezier(fc.P(-half_w, 0.0), fc.P(-half_w * 0.6, peak_length),
                      fc.P(half_w * 0.6, peak_length), fc.P(half_w, 0.0))
    edges = [
        fc.Edge("back", [fc.Line(fc.P(half_w, 0.0), fc.P(-half_w, 0.0))]),
        fc.Edge("front", [front]),
    ]
    return fc.Piece(
        "peak", edges,
        seam_allowance=8.0, allowances={"front": 6.0},
        grainline=fc.Grainline(fc.P(0.0, peak_length * 0.1), fc.P(0.0, peak_length * 0.8)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="back", mirror=True),
        label="Peak",
    )


def build():
    pattern = fc.PatternSet("wearable-compute-cap")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "crown":
        pattern.add(build_crown())
    if all_pieces or target_piece == "peak":
        pattern.add(build_peak())
    pattern.bom = [
        {"item": "twill (conductive-thread compatible)", "qty": 300, "unit": "mm_length",
         "note": "≈ at 1400 mm width for the crown + peak; see the fabric card's e_textile block."},
        {"item": "SBC enclosure", "qty": 1, "unit": "count",
         "note": "Yantra4D pi-hat-case (see notion.hardware_ref) slips into the pocket."},
        {"item": "cabling + battery loop", "qty": 1, "unit": "set", "note": "route per the marks."},
    ]
    pattern.metadata = {
        "fc200_rank": 147, "family": "etextile", "fabric_hint": "popelina-algodon",
        "head_opening_mm": round(head_eff, 1),
        "etextile_note": "A cap crown + peak with a marked ELECTRONICS POCKET sized to the "
            "Yantra4D pi-hat-case and a cable route to a battery loop. Pocket and route are "
            "MARKED for the maker; no electronics are drafted here.",
        "hardware": "SBC enclosure via Yantra4D (notion.hardware_ref -> pi-hat-case)",
        "geometry_note": f"crown radius ≈ {head_eff / (2.0 * math.pi):.1f} mm",
    }
    return pattern


result = build()
