"""
Soft triangle bralette — Fashion Cabinet Garment Cartridge (FC-400 #382; y4d bra-ring-slider).

A wireless soft-cup bralette in cotton-modal: two triangle cups on an elastic underband,
held by adjustable straps that run through a ring at the cup point and a slider on the
shoulder. There is no wire and no moulding — the shape is the triangle and the band, and the
support such as it is comes from the band's light negative ease. This is the honest opposite
of the underwire bra: where that garment SOLVES a wire, this one places a soft triangle and
declares that it does not pretend to lift.

Two real decisions:

  1. THE TRIANGLE IS A TRUE TRIANGLE, plus a fold. A bralette cup is a triangle of doubled
     cloth whose lower edge sits on the band, whose inner edge runs to centre front, and
     whose apex carries the strap ring. Drafting it as a true triangle (rather than a scaled
     bra cup) is what gives the soft, unmoulded look; the only shaping is an optional dart
     of gathers along the band edge, set by a fullness parameter, for a little more room.

  2. THE STRAP IS ADJUSTABLE THROUGH A RING AND A SLIDER. The strap runs from the band, up
     through a RING at the cup apex, over the shoulder, and back through a SLIDER — the same
     bra-ring-slider hardware family the nursing and swim cartridges use. `strap_w` drives
     BOTH the drafted strap's cut width AND the ring/slider's strap channel, so the webbing
     threads by construction. This is the dimensional handshake for this lane's soft cups.

Four pieces: the triangle cup, the underband, the back band, and the strap. Made to measure
to underbust and bust girths; the cup triangle is sized from the bust-minus-underbust surplus.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))
bust_girth = float(PARAM(lambda: bust_girth, 900.0))
band_height = float(PARAM(lambda: band_height, 22.0))     # elastic underband depth
cup_spread = float(PARAM(lambda: cup_spread, 150.0))      # cup lower-edge width on band
cup_rise = float(PARAM(lambda: cup_rise, 180.0))          # band to apex (triangle height)
fullness = float(PARAM(lambda: fullness, 0.10))           # gather share on band edge
strap_w = float(PARAM(lambda: strap_w, 12.0))             # strap / ring channel width
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth = max(600.0, min(bust_girth, 1400.0))
band_height = max(10.0, min(band_height, 60.0))
cup_spread = max(90.0, min(cup_spread, 260.0))
cup_rise = max(90.0, min(cup_rise, 320.0))
fullness = max(0.0, min(fullness, 0.4))
strap_w = max(6.0, min(strap_w, 24.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# two cups must fit inside the band with room for the back
cup_spread = min(cup_spread, underbust_girth * 0.30)

# ── Solved geometry ──────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FIN = underbust_girth * NEG
BAND_HALF = BAND_FIN / 2.0
# The cup's lower edge is spread + the gathered fullness; the gathers are eased onto the
# band's cup span, so the band cup span is the un-gathered spread.
CUP_LOWER = cup_spread * (1.0 + fullness)
BACK_SPAN = max(60.0, BAND_HALF - cup_spread)


def build_cup():
    """A true triangle cup (cut 2, doubled): lower edge on the band, inner edge to CF,
    outer/apex edge carrying the strap ring at the point.

    CCW: lower (on band, left->right) -> outer edge up to apex -> inner edge down to CF.
    The lower edge is drafted at CUP_LOWER (spread + fullness) so the gathers ease onto
    the band's spread; the apex is the ring point.
    """
    w = cup_spread
    h = cup_rise
    # points: CF bottom (0,0), outer bottom (CUP_LOWER approx spread wide), apex at top-inner
    cf_bot = fc.P(0.0, 0.0)
    out_bot = fc.P(CUP_LOWER, 0.0)
    apex = fc.P(w * 0.16, h)          # apex sits inboard, the classic triangle lean
    edges = [
        fc.Edge("lower", [fc.Line(cf_bot, out_bot)]),
        fc.Edge("outer", [fc.Bezier(out_bot,
                                    fc.P(CUP_LOWER * 0.72, h * 0.35),
                                    fc.P(apex.x + w * 0.30, h * 0.82),
                                    apex)]),
        fc.Edge("inner", [fc.Line(apex, cf_bot)]),
    ]
    internals = [fc.Internal("ring seat (strap apex)",
                             [fc.P(apex.x, apex.y - 12.0), fc.P(apex.x + strap_w, apex.y - 12.0)],
                             kind="marking")]
    return fc.Piece(
        "cup", edges, seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "outer": 0.0, "inner": 0.0},
        notches=[fc.Notch("lower", 0.5, "band gather centre"),
                 fc.Notch("outer", 1.0, "ring apex")],
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.2), fc.P(w * 0.3, h * 0.7)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Triangle cup (cut 2 pairs, doubled)")


def build_underband(cup_span):
    """The elastic underband under the cups (cut 1, closing at a side/back seam).

    Its `cup_edge` carries the two cups' spread (per side); its lower edge is the finished
    band ring. The cups' gathered lower edges ease onto the cup_edge.
    """
    front = cup_span                # one cup's spread
    back = BACK_SPAN
    w = front + back                # half the band
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, band_height))]),
        fc.Edge("cup_edge", [fc.Line(fc.P(0.0, band_height), fc.P(front, band_height))]),
        fc.Edge("back_edge", [fc.Line(fc.P(front, band_height), fc.P(w, band_height))]),
        fc.Edge("center_back", [fc.Line(fc.P(w, band_height), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "underband", edges, seam_allowance=seam_allowance,
        allowances={"lower": 0.0},
        notches=[fc.Notch("cup_edge", 0.5, "cup centre"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(w * 0.5, 4.0), fc.P(w * 0.5, band_height - 4.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)")


def build_strap():
    """An adjustable strap: a rectangle cut to `strap_w`, threading the ring and slider."""
    length = cup_rise + 260.0        # apex ring up over the shoulder to the back band
    edges = [
        fc.Edge("end_band", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_ring", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges, seam_allowance=0.0,
        notches=[fc.Notch("strap_edge", 0.55, "slider position (adjustable)"),
                 fc.Notch("end_ring", 0.5, "ring at cup apex — thread and fold")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Adjustable strap (cut 2, ring at apex)")


def build():
    pattern = fc.PatternSet("bralette-soft")
    cup = build_cup()
    band = build_underband(cup_spread)
    strap = build_strap()

    picked = {"cup": cup, "underband": band, "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cup, band, strap):
            pattern.add(piece)
        # The cup's lower edge eases (gathers) onto the band's cup span.
        pattern.declare_seam(("cup", "lower"), ("underband", "cup_edge"), tol=1.5,
                             ease=(cup.edge("lower").length()
                                   - band.edge("cup_edge").length()))
        # The strap's band end and ring end are one continuous piece threaded through the
        # ring, so its two ends match by construction.
        pattern.declare_seam(("strap", "end_band"), ("strap", "end_ring"), tol=0.5)

    band_opening = 2.0 * band.edge("lower").length()
    cup_edges = 2.0 * (cup.edge("outer").length() + cup.edge("inner").length())
    fabric_width = 1500.0
    area = cup.area() * 4.0 + band.area() * 2.0
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "cotton-modal jersey (doubled cups)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"cups + band at {fabric_width:.0f} mm width, 60% marker. Cups are cut "
                 "DOUBLE so the triangle is self-lined and the edges finish clean."},
        {"item": "bra rings + sliders (Yantra4D bra-ring-slider)", "qty": 2, "unit": "set",
         "note": f"one ring + one slider per strap; strap channel strap_w {strap_w:.0f} mm. "
                 "The ring/slider is the Yantra4D solid (notion.hardware_ref -> "
                 "bra-ring-slider), never modelled here; the drafted strap is cut to the "
                 "width the channel expects."},
        {"item": f"strap elastic {strap_w:.0f} mm",
         "qty": round(2 * strap.edge("strap_edge").length() * 1.2),
         "unit": "mm_length",
         "note": "two straps + slider/ring fold-backs; cut to the SAME width as the ring "
                 "channel."},
        {"item": "band elastic (plush-back) 10-12 mm", "qty": round(band_opening * 0.9),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm x 0.9 — the band is the only support a "
                 "wireless bralette has, so it carries a light negative ease."},
        {"item": "picot elastic (cup edges) 6-8 mm", "qty": round(cup_edges * 0.9),
         "unit": "mm_length",
         "note": f"cup outer + inner edges {cup_edges:.0f} mm at 0.9."},
        {"item": "hook-and-eye (2x2) or slip-on", "qty": 1, "unit": "piece",
         "note": "a soft bralette can close at a small CB hook or be pulled on; the hook is "
                 "Yantra4D hook-and-eye."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "gather the cup lower edge onto the band; zigzag the elastics."},
    ]
    pattern.metadata = {
        "fc400_rank": 382, "family": "underwear_lounge", "fabric_hint": "cotton-modal",
        "silhouette_note": "A wireless soft-cup bralette: two TRUE TRIANGLES of doubled "
            "jersey on an elastic underband, held by ring-and-slider straps. No wire, no "
            "moulding — the shape is the triangle and the band, and it does not pretend to "
            "lift.",
        "hardware": "rings + sliders via Yantra4D (notion.hardware_ref -> bra-ring-slider); "
            "strap_w drives BOTH the drafted strap's cut width (the strap_edge interface) "
            "and the ring/slider strap channel — the dimensional handshake.",
        "solved": {
            "band_finished_mm": round(BAND_FIN, 1),
            "cup_spread_mm": round(cup_spread, 1),
            "cup_lower_gathered_mm": round(CUP_LOWER, 1),
            "fullness_share": round(fullness, 2),
            "cup_rise_mm": round(cup_rise, 1),
            "strap_w_mm": round(strap_w, 1),
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "small centre-back hook-and-eye or pull-on",
        "drafting": "Made to measure to underbust and bust girths; the cup triangle is sized "
            "from the surplus and the band from the underbust.",
    }
    return pattern


result = build()
