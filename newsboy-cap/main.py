"""
Eight-panel newsboy cap — FC-400 rank #356, Lane 6 (millinery). Fashion Cabinet Cartridge.

The gavroche/newsboy: a full, soft eight-panel crown gathered to a covered button at the
apex, with a short stiff peak at the front. Drafted as ONE crown panel (cut 8) — a curved
wedge from the head ring up to the apex — plus a headband and a peak. The panels are all
identical; eight of them tile the crown. The apex button bridges to a Yantra4D
sew-through-button (point hardware).

Pieces:
  - panel : the crown wedge, cut 8. Its base arc is 1/8 of the head ring; its two sides
            meet at the apex; the outer profile bulges for the newsboy fullness.
  - band  : the headband, cut 1 (head circ × band height).
  - peak  : the stiff front peak, cut 2 (mirrored, a shallow crescent).

Drafting notes:
  * The panel base arc == head_eff / 8, solved so eight bases == the head ring exactly.
  * The panel height (apex rise) is FLOORED so a huge head on a short cap can never drive
    the wedge sides to cross; the fullness bulge is clamped so the outline never
    self-intersects.

Hardware: Yantra4D sew-through-button at the apex (point hardware; sewn through the covered
button, no sewn edge — no dimensional handshake owed).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""


import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # panel|band|peak|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
ease = float(PARAM(lambda: ease, 12.0))
crown_rise = float(PARAM(lambda: crown_rise, 150.0))     # base ring to apex
fullness = float(PARAM(lambda: fullness, 30.0))          # panel outward bulge (the newsboy puff)
band_height = float(PARAM(lambda: band_height, 45.0))
peak_depth = float(PARAM(lambda: peak_depth, 60.0))      # peak stick-out
button_ligne = float(PARAM(lambda: button_ligne, 24.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

head_girth = max(480.0, min(head_girth, 640.0))
ease = max(0.0, min(ease, 40.0))
crown_rise = max(80.0, min(crown_rise, 260.0))
fullness = max(0.0, min(fullness, 90.0))
band_height = max(25.0, min(band_height, 90.0))
peak_depth = max(25.0, min(peak_depth, 110.0))
button_ligne = max(14.0, min(button_ligne, 54.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

head_eff = head_girth + ease
PANELS = 8
BASE_ARC = head_eff / PANELS                             # each panel's base width
RISE = max(80.0, crown_rise)
BULGE = min(fullness, BASE_ARC * 0.45)                   # never self-intersect


def _panel():
    """One crown wedge. Base along y=0 (width BASE_ARC + the fullness gather), straight
    sides up to a short apex flat, so the eight wedges tile the crown and the newsboy puff
    comes from the extra base width gathered into the same seam. Straight sides never
    degenerate at any rise; a tiny apex flat keeps the wedge a real quad, not a spike."""
    hw = BASE_ARC / 2.0                                    # base tiles the band exactly
    # The newsboy puff comes from a WIDE apex flat gathered to the button, plus the panel
    # bulging above the head — a wider apex flat = more fullness. Clamped below the base
    # half so the wedge stays a proper trapezoid (apex never wider than the base).
    apex_hw = max(4.0, min(hw * 0.14 + BULGE * 0.5, hw - 4.0))
    base_l = fc.P(-hw, 0.0)
    base_r = fc.P(hw, 0.0)
    apex_r = fc.P(apex_hw, RISE)
    apex_l = fc.P(-apex_hw, RISE)
    return fc.Piece(
        "panel",
        [
            fc.Edge("base", [fc.Line(base_l, base_r)]),        # to the band (gathered)
            fc.Edge("seam_r", [fc.Line(base_r, apex_r)]),
            fc.Edge("apex", [fc.Line(apex_r, apex_l)]),        # short apex flat
            fc.Edge("seam_l", [fc.Line(apex_l, base_l)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base", 0.5, "panel centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, RISE - 10.0)),
        cut=fc.CutSpec(quantity=PANELS),
        label="Crown panel (×8)",
    )


def _band():
    w, h = head_eff, band_height
    return fc.Piece(
        "band",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),     # to the panels
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Headband",
    )


def _peak():
    """A shallow crescent peak, cut 2 (self + lining). Width ~ a third of the head, depth
    = peak_depth."""
    w = head_eff * 0.34
    d = peak_depth
    return fc.Piece(
        "peak",
        [
            fc.Edge("attach", [fc.curve_through(fc.P(-w / 2.0, 0.0), fc.P(w / 2.0, 0.0),
                                                bulge=0.10, side=-1.0)]),   # to the band
            fc.Edge("side_r", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(w * 0.32, d))]),
            fc.Edge("front", [fc.curve_through(fc.P(w * 0.32, d), fc.P(-w * 0.32, d),
                                               bulge=0.16, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(-w * 0.32, d), fc.P(-w / 2.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, 5.0), fc.P(0.0, d - 5.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Peak (self + lining)",
    )


def build():
    pattern = fc.PatternSet("newsboy-cap")
    everything = target_piece == "set"
    panel = _panel()
    band = _band()
    peak = _peak()
    if everything or target_piece == "panel":
        pattern.add(panel)
    if everything or target_piece == "band":
        pattern.add(band)
    if everything or target_piece == "peak":
        pattern.add(peak)

    names = {p.name for p in pattern.pieces}
    if {"panel", "band"} <= names:
        # eight panel bases tile the band top: declare the panel base ×8 == band top.
        pattern.declare_seam([("panel", "base")] * PANELS, ("band", "top"), tol=2.0)
    if "panel" in names:
        # adjacent panels join seam_r to seam_l.
        pattern.declare_seam(("panel", "seam_r"), ("panel", "seam_l"), tol=1.0)

    bh_half = button_ligne * 0.635 / 2.0
    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "tweed / wool (crown, band, peak)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker; a soft tweed gives the "
                 "newsboy its slouch."},
        {"item": "peak stiffener", "qty": 1, "unit": "set",
         "note": "a plastic or buckram peak insert between the two peak layers."},
        {"item": "covered sew-through button (apex)", "qty": 1, "unit": "count",
         "note": "Yantra4D sew-through-button (see notion.hardware_ref) — the covered "
                 "button at the crown apex; sewn through, no sewn edge."},
        {"item": "lining + sweatband", "qty": 1, "unit": "set",
         "note": "line the crown; grosgrain sweatband inside the headband."},
    ]
    pattern.metadata = {
        "fc400_rank": 356, "family": "millinery", "lane": 6,
        "fabric_hint": "tweed-wool",
        "head_girth_mm": round(head_girth, 1), "head_opening_mm": round(head_eff, 1),
        "panels": PANELS, "base_arc_mm": round(BASE_ARC, 2), "crown_rise_mm": round(RISE, 1),
        "fullness_bulge_mm": round(BULGE, 1), "band_height_mm": round(band_height, 1),
        "peak_depth_mm": round(peak_depth, 1), "button_ligne": round(button_ligne, 1),
        "buttonhole_half_mm": round(bh_half, 2),
        "solved": {
            "eight_bases_mm": round(PANELS * BASE_ARC, 2),
            "band_top_mm": round(head_eff, 2),
            "note": "eight panel bases tile the band top exactly (8 x head/8 == head); the "
                    "panel sides are straight (never degenerate at any rise) and the apex "
                    "flat is clamped below the base half so the wedge stays a proper "
                    "trapezoid; the rise is floored",
        },
        "hardware": "Yantra4D sew-through-button at the apex (point hardware; sewn through, "
                    "no sewn edge — no dimensional handshake owed)",
    }
    return pattern


result = build()
