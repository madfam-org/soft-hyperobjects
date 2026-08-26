"""
Clip-down nursing bra — Fashion Cabinet Garment Cartridge (FC-400 #386; y4d bra-ring-slider).

A wireless clip-down nursing bra in cotton-jersey: a soft-cup bra whose cup drops for feeding
by unclipping the strap at a RING on the cup, so the cup falls away and re-clips one-handed.
It deepens the FC-300 nursing bra (a drop-cup on a wired cradle) into the softer, wire-free
everyday version — the one worn around the clock in the early months — where the whole point
is a one-handed clip and a cup that supports without a wire pressing on milk ducts.

Three real decisions, all specific to nursing:

  1. THE DROP IS A ONE-HANDED CLIP, NOT A ZIP OR A PANEL. The strap detaches at a RING sewn to
     the top of the cup: unclip, the cup drops on its lower hinge, feed, re-clip. `strap_w`
     drives BOTH the drafted strap's cut width AND the ring/slider channel, so the clip
     threads by construction — the dimensional handshake for this lane's soft cups. The
     clip must be operable with the other arm holding a baby, which is why it is a ring-slider
     and not a hook a wearer needs two hands and sight to fasten.

  2. NO WIRE ON THE MILK DUCTS. A nursing bra is worn constantly and a wire pressing the
     underbust can block a duct and cause mastitis — a real medical risk, not a comfort
     preference. So this cup is soft, supported by a wide band and a stable sling under the
     cup, never a wire. The draft states this rather than leaving it implicit.

  3. THE CUP DROPS ON A HINGE, NOT A HOLE. The cup's lower edge stays attached to the cradle/
     band as a hinge; only the top unclips. That keeps the dropped cup out of the way and
     lets it swing back and re-seat, instead of a hole the breast is pushed through.

Pieces: cup, sling (the stable inner support under the cup), band, back, strap. Made to
measure to underbust and bust girths.

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

underbust_girth = float(PARAM(lambda: underbust_girth, 800.0))
bust_girth = float(PARAM(lambda: bust_girth, 1000.0))
band_height = float(PARAM(lambda: band_height, 40.0))
cup_spread = float(PARAM(lambda: cup_spread, 170.0))
cup_rise = float(PARAM(lambda: cup_rise, 200.0))
sling_frac = float(PARAM(lambda: sling_frac, 0.55))       # sling coverage of the cup
strap_w = float(PARAM(lambda: strap_w, 20.0))             # nursing straps are wide
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(600.0, min(underbust_girth, 1250.0))
bust_girth = max(700.0, min(bust_girth, 1500.0))
band_height = max(20.0, min(band_height, 90.0))
cup_spread = max(110.0, min(cup_spread, 280.0))
cup_rise = max(110.0, min(cup_rise, 340.0))
sling_frac = max(0.3, min(sling_frac, 0.8))
strap_w = max(12.0, min(strap_w, 40.0))
negative_ease_pct = max(6.0, min(negative_ease_pct, 22.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

cup_spread = min(cup_spread, underbust_girth * 0.30)

# ── Solved geometry ──────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FIN = underbust_girth * NEG
BAND_HALF = BAND_FIN / 2.0
BACK_SPAN = max(60.0, BAND_HALF - cup_spread)
SLING_H = cup_rise * sling_frac


def build_cup():
    """The drop cup (cut 2, doubled): lower edge on the band (the hinge), inner edge to CF,
    apex carrying the strap RING. The lower edge is the hinge that keeps the dropped cup
    seated; only the ring at the top unclips.
    """
    w = cup_spread
    h = cup_rise
    cf_bot = fc.P(0.0, 0.0)
    out_bot = fc.P(w, 0.0)
    apex = fc.P(w * 0.20, h)
    edges = [
        fc.Edge("hinge", [fc.Line(cf_bot, out_bot)]),         # stays attached to the band
        fc.Edge("outer", [fc.Bezier(out_bot,
                                    fc.P(w * 0.74, h * 0.34),
                                    fc.P(apex.x + w * 0.32, h * 0.82),
                                    apex)]),
        fc.Edge("inner", [fc.Line(apex, cf_bot)]),
    ]
    internals = [fc.Internal("clip ring seat (apex)",
                             [fc.P(apex.x, apex.y - 12.0),
                              fc.P(apex.x + strap_w, apex.y - 12.0)], kind="marking")]
    return fc.Piece(
        "cup", edges, seam_allowance=seam_allowance,
        allowances={"hinge": 0.0, "outer": 0.0, "inner": 0.0},
        notches=[fc.Notch("hinge", 0.5, "band hinge centre"),
                 fc.Notch("outer", 1.0, "clip ring apex")],
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.2), fc.P(w * 0.3, h * 0.7)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Drop cup (cut 2 pairs, doubled, hinge at the band)")


def build_sling():
    """The stable inner sling (cut 2): a lower support that stays PUT when the cup drops, so
    the breast is supported through the feed. It sits under the cup, its top edge a partial
    coverage of the cup rise (`sling_frac`).
    """
    w = cup_spread
    h = SLING_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w * 0.82, h))]),
        fc.Edge("top", [fc.Bezier(fc.P(w * 0.82, h),
                                  fc.P(w * 0.5, h * 0.92),
                                  fc.P(w * 0.2, h * 0.72),
                                  fc.P(0.0, h * 0.4))]),
        fc.Edge("center_front", [fc.Line(fc.P(0.0, h * 0.4), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "sling", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("lower", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Support sling (cut 2 pairs, stays put when cup drops)")


def build_band(cup_span):
    front = cup_span
    back = BACK_SPAN
    w = front + back
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, band_height))]),
        fc.Edge("cup_edge", [fc.Line(fc.P(0.0, band_height), fc.P(front, band_height))]),
        fc.Edge("back_edge", [fc.Line(fc.P(front, band_height), fc.P(w, band_height))]),
        fc.Edge("center_back", [fc.Line(fc.P(w, band_height), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        allowances={"lower": 0.0},
        notches=[fc.Notch("cup_edge", 0.5, "cup hinge centre"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(w * 0.5, 4.0), fc.P(w * 0.5, band_height - 4.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs, CB hook)")


def build_back(back_span):
    x = back_span
    h = band_height + 30.0
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("strap_tab", [fc.Line(fc.P(0.0, h), fc.P(strap_w, h))]),
        fc.Edge("top", [fc.Bezier(fc.P(strap_w, h),
                                  fc.P(x * 0.45, h * 0.72),
                                  fc.P(x * 0.85, band_height + 6.0),
                                  fc.P(x, band_height))]),
        fc.Edge("center_back", [fc.Line(fc.P(x, band_height), fc.P(x, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(x, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("bottom", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(x * 0.5, band_height * 0.4), fc.P(x * 0.5, h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, CB hook)")


def build_strap():
    length = cup_rise + 280.0
    edges = [
        fc.Edge("end_wing", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_clip", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges, seam_allowance=0.0,
        notches=[fc.Notch("strap_edge", 0.5, "slider position (adjustable)"),
                 fc.Notch("end_clip", 0.5, "nursing clip — one-handed drop")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Nursing strap (cut 2, clips at the cup ring)")


def build():
    pattern = fc.PatternSet("nursing-clip-bra")
    cup = build_cup()
    sling = build_sling()
    band = build_band(cup_spread)
    back = build_back(BACK_SPAN)
    strap = build_strap()

    picked = {"cup": cup, "sling": sling, "band": band, "back": back, "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cup, sling, band, back, strap):
            pattern.add(piece)
        # The cup's HINGE and the sling's lower edge both seat on the band's cup span; the
        # cup hinge stays attached (it is the drop hinge), the sling under it.
        pattern.declare_seam([("cup", "hinge"), ("sling", "lower")],
                             ("band", "cup_edge"), tol=1.5,
                             ease=(cup.edge("hinge").length() + sling.edge("lower").length()
                                   - band.edge("cup_edge").length()))
        # Back wing onto the band's back span.
        pattern.declare_seam(("back", "bottom"), ("band", "back_edge"), tol=1.0)
        # The strap's ends match (one continuous strap threaded through the clip).
        pattern.declare_seam(("strap", "end_wing"), ("strap", "end_clip"), tol=0.5)

    band_opening = 2.0 * band.edge("lower").length()
    cup_edges = 2.0 * (cup.edge("outer").length() + cup.edge("inner").length())
    fabric_width = 1500.0
    area = cup.area() * 4.0 + sling.area() * 4.0 + band.area() * 2.0 + back.area() * 2.0
    marker_len = area / (fabric_width * 0.58)
    pattern.bom = [
        {"item": "cotton jersey (soft, breathable) + sling tricot",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cups + slings + band + wings at {fabric_width:.0f} mm width, 58% marker. "
                 "Soft cotton against the skin — a nursing bra is worn constantly."},
        {"item": "nursing clips / rings + sliders (Yantra4D bra-ring-slider)", "qty": 2,
         "unit": "set",
         "note": f"one clip-ring + slider per strap; strap channel strap_w {strap_w:.0f} mm. "
                 "The ring/slider is the Yantra4D solid (notion.hardware_ref -> "
                 "bra-ring-slider), never modelled here. It must open ONE-HANDED — that is "
                 "the whole point of a nursing clip."},
        {"item": f"strap elastic {strap_w:.0f} mm (wide, soft)",
         "qty": round(2 * strap.edge("strap_edge").length() * 1.2), "unit": "mm_length",
         "note": "wide soft straps spread the load; cut to the clip channel width."},
        {"item": "band elastic (plush-back, soft) 12 mm", "qty": round(band_opening * 0.9),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm x 0.9 — the band and the sling are the "
                 "support, NOT a wire (a wire on the milk ducts risks blocked ducts)."},
        {"item": "picot elastic (cup edges) 8 mm", "qty": round(cup_edges * 0.9),
         "unit": "mm_length", "note": f"cup edges {cup_edges:.0f} mm at 0.9."},
        {"item": "hook-and-eye bra back (3x3+)", "qty": 1, "unit": "piece",
         "note": "a longer hook column allows band adjustment as the ribcage changes — "
                 "Yantra4D hook-and-eye."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "topstitch the hinge flat so the cup drops and re-seats cleanly."},
    ]
    pattern.metadata = {
        "fc400_rank": 386, "family": "underwear_lounge", "fabric_hint": "cotton-jersey",
        "silhouette_note": "A WIRELESS clip-down nursing bra: a soft cup that drops for "
            "feeding by unclipping a ring at the top, hinged at the band so it re-seats, over "
            "a stable sling and a wide soft band. No wire on the milk ducts; a one-handed clip.",
        "hardware": "clip rings + sliders via Yantra4D (notion.hardware_ref -> "
            "bra-ring-slider); strap_w drives BOTH the drafted strap's cut width (the "
            "strap_edge interface) and the ring/slider channel — the dimensional handshake.",
        "nursing_safety": {
            "wireless": True,
            "one_handed_clip": True,
            "note": "No wire, deliberately: a wire pressing the underbust while nursing "
                    "constantly can block a milk duct and cause mastitis — a medical risk, not "
                    "a comfort preference. The clip must open with the other arm holding a "
                    "baby, which is why it is a ring-slider, not a two-hand hook.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FIN, 1),
            "cup_spread_mm": round(cup_spread, 1),
            "cup_rise_mm": round(cup_rise, 1),
            "sling_height_mm": round(SLING_H, 1),
            "strap_w_mm": round(strap_w, 1),
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "clip-down cup ring + centre-back hook column",
        "drafting": "Made to measure to underbust and bust girths; wireless, soft-cup, with "
            "a support sling that stays put when the cup drops.",
    }
    return pattern


result = build()
