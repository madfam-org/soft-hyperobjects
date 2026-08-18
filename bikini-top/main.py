"""
Bikini Top — FC-100 rank #55. Fashion Cabinet Garment Cartridge.

The commons' swim-top draft: the classic string / sliding-triangle bikini.
Each cup is a single TRIANGLE cut four times (2 self + 2 lining) at swimwear
negative ease so the tricot tensions over the bust. Self and lining are sewn
along the outer and top edges (delta 0 BY CONSTRUCTION — they are the same
cut), turned, and the lower/underbust edge is left open and finished with clear
elastic. The top edge is a marked CASING zone: the halter NECK tie threads
through the channel it forms; a BAND tie threads the two lower edges and ties at
the back. No hardware — it ties. Optional slider/ring rests as a Yantra4D
reference in the BOM. All finished edges emit exact-mm swim-elastic and tie cut
lengths derived from the measured cup edges — the numbers factories keep on
private spec sheets.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # cup|neck_tie|band_tie|set

bust_girth        = float(PARAM(lambda: bust_girth, 900.0))     # full bust circumference
underbust_girth   = float(PARAM(lambda: underbust_girth, 760.0))  # ribcage under the bust
cup_height        = float(PARAM(lambda: cup_height, 210.0))     # underbust base -> apex
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 12.0))
apex_offset       = float(PARAM(lambda: apex_offset, 18.0))     # apex shift toward centre
tie_tail          = float(PARAM(lambda: tie_tail, 380.0))       # free tie length each end
tie_width         = float(PARAM(lambda: tie_width, 16.0))       # finished tie width
edge_elastic_ratio = float(PARAM(lambda: edge_elastic_ratio, 0.88))  # edge elastic/opening
seam_allowance    = float(PARAM(lambda: seam_allowance, 6.0))
casing_allowance  = float(PARAM(lambda: casing_allowance, 18.0))  # top-edge fold -> channel

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(650.0, min(bust_girth, 1300.0))
underbust_girth = max(550.0, min(underbust_girth, 1150.0))
cup_height = max(140.0, min(cup_height, 320.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 20.0))
apex_offset = max(0.0, min(apex_offset, 60.0))
tie_tail = max(150.0, min(tie_tail, 600.0))
tie_width = max(8.0, min(tie_width, 30.0))
edge_elastic_ratio = max(0.75, min(edge_elastic_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))
casing_allowance = max(10.0, min(casing_allowance, 40.0))

# underbust must never exceed bust (rib is smaller than the bust line)
underbust_girth = min(underbust_girth, bust_girth - 20.0)

NEG = 1.0 - negative_ease_pct / 100.0
# One cup covers roughly a quarter of the body at the bust. The underbust base
# of the triangle is derived from the ribcage quarter; the extra girth from the
# bust drives how much the apex rises/projects. Both are reduced by NEG so the
# tricot is drafted UNDER the body and tensions to fit.
BASE = underbust_girth * NEG / 4.0       # underbust base half-cup width
BUST_Q = bust_girth * NEG / 4.0          # bust quarter (for the projection allowance)
HEIGHT = cup_height * NEG                 # apex height (also reduced — vertical stretch)
APEX_X = max(0.0, min(BASE - 8.0, apex_offset))  # apex x, kept inside the base
ELASTIC_ZONE = 6.0                        # marked clear-elastic application width (mm)


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Edges here are authored CCW, so the inward normal at tangent t is
    (-t.y, t.x). The fraction window [t0, t1] keeps the trace off corners.
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _casing_zone(edge, label, samples=13):
    """Internal trace parallel to the casing (top) edge, casing_allowance mm
    inside — the fold line for the channel the halter tie runs through."""
    pts = []
    for i in range(samples):
        t = i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * casing_allowance, p.y + tan.x * casing_allowance))
    return fc.Internal(label, pts, kind="trace")


def build_cup():
    """Single sliding-triangle cup, cut 4 (2 self + 2 lining).

    Corners (y-up): A = inner-lower at centre front (0,0); B = outer-lower at
    the side (BASE, 0); C = apex where the cup rises over the bust and the
    halter tie exits the casing (APEX_X, HEIGHT). The lower edge (A->B) is the
    underbust base finished with clear elastic and threaded by the band tie; the
    side edge (B->C) is bust-shaped, bowed slightly OUTSIDE the chord for cup
    volume, and swim-elastic finished; the casing edge (C->A) folds to the
    channel the neck (halter) tie runs through.
    """
    lower = fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(BASE, 0.0))])
    # Outer/side edge bows out (side=+1 → left of B→C, i.e. away from centre) to
    # give the flat triangle some cup projection.
    side = fc.Edge(
        "side",
        [fc.curve_through(fc.P(BASE, 0.0), fc.P(APEX_X, HEIGHT),
                          bulge=0.10, side=1.0)],
    )
    # Casing (top) edge back down to centre front; a soft hollow toward the body.
    casing = fc.Edge(
        "casing",
        [fc.curve_through(fc.P(APEX_X, HEIGHT), fc.P(0.0, 0.0),
                          bulge=0.06, side=1.0)],
    )
    return fc.Piece(
        "cup",
        [lower, side, casing],
        seam_allowance=seam_allowance,
        # lower is elastic-bound (both layers caught, not turned); casing is a
        # folded channel, not a plain seam-turn.
        allowances={"lower": 0.0, "casing": casing_allowance},
        notches=[fc.Notch("lower", 0.5, "centre / band match"),
                 fc.Notch("side", 0.5, "apex-side match")],
        grainline=fc.Grainline(fc.P(BASE * 0.42, HEIGHT * 0.12),
                               fc.P(BASE * 0.42, HEIGHT * 0.72)),
        internals=[
            _elastic_zone(fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(BASE, 0.0))]),
                          "lower elastic zone", 0.06, 0.94),
            _elastic_zone(side, "side elastic zone", 0.06, 0.94),
            _casing_zone(casing, "halter casing fold"),
        ],
        cut=fc.CutSpec(quantity=4, mirror=True),  # 2 self + 2 lining
        label="Cup (2 self + 2 lining)",
    )


def _tie(name, span, label, color_len_note):
    """A long narrow tie strip: a threaded/anchored span plus two free tails.

    Length = the measured span it covers + 2 tails (the bow ends). Cut 1 as a
    doubled-and-turned tube or a folded-and-topstitched strip. Not sewn into a
    seam — it slides through the casing / anchors the lower edge — so it carries
    no declared seam, only a BOM cut length.
    """
    length = span + 2.0 * tie_tail
    band_h = 2.0 * tie_width  # cut width folds in half to the finished tie width
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build():
    pattern = fc.PatternSet("bikini-top")
    cup = build_cup()

    # measured cup edges drive every derived length below
    lower_len = cup.edge("lower").length()
    side_len = cup.edge("side").length()
    casing_len = cup.edge("casing").length()

    # The neck (halter) tie runs up through one cup casing, behind the neck, and
    # down the other — span ≈ both casings plus a nape allowance. The band tie
    # threads both lower edges and ties at the back — span ≈ both lower edges
    # plus the back gap (approximated as one more underbust base per side).
    nape_gap = BASE * 1.2
    neck_span = 2.0 * casing_len + nape_gap
    back_gap = 2.0 * BASE
    band_span = 2.0 * lower_len + back_gap

    neck_tie = _tie("neck_tie", neck_span, "Neck / halter tie", "casings")
    band_tie = _tie("band_tie", band_span, "Underbust band tie", "lower edges")

    picked = {"cup": cup, "neck_tie": neck_tie, "band_tie": band_tie}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # "set"
        for piece in (cup, neck_tie, band_tie):
            pattern.add(piece)
        # Self and lining are the SAME cup cut: they sew right-sides-together
        # along the outer (side) and top (casing) edges, then turn. Identical
        # refs → delta 0 by construction (self edge == lining edge). These are
        # the two real sewn seams of the top; the lower edge is left open for
        # the clear-elastic binding and the ties are threaded, not sewn.
        pattern.declare_seam(("cup", "side"), ("cup", "side"), tol=1.0)
        pattern.declare_seam(("cup", "casing"), ("cup", "casing"), tol=1.0)

    # ── Elastic + tie accounting (the point of this cartridge) ───────────────
    # Clear swim elastic finishes the lower (underbust) and side (outer) edges
    # of BOTH cups. Exact cut = measured opening x ratio, rounded.
    lower_opening = 2.0 * lower_len   # two cups
    side_opening = 2.0 * side_len     # two cups
    lower_elastic = round(lower_opening * edge_elastic_ratio)
    side_elastic = round(side_opening * edge_elastic_ratio)
    neck_tie_len = round(neck_span + 2.0 * tie_tail)
    band_tie_len = round(band_span + 2.0 * tie_tail)

    fabric_width = 1500.0  # tricot-nylon-elastano card width
    # Marker length must be PHYSICALLY buildable: the long tie strips are cut
    # along the roll, so the marker is at least as long as the longest tie
    # (the two ties nest side-by-side across the 1500 mm width, well within it).
    # The compact cup pieces (cut 4) nest across the width and add their
    # area-derived length on top of the tie band.
    cup_area = cup.area() * cup.cut.quantity
    cup_marker = cup_area / (fabric_width * 0.55)  # tight nesting of small parts
    tie_marker = max(neck_tie_len, band_tie_len)   # longest strip, laid on grain
    marker_len = cup_marker + tie_marker
    pattern.bom = [
        {"item": "tricot-nylon-elastano", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width: a ~{round(tie_marker / 10.0) * 10:.0f} mm "
                 "tie band (both ties on grain, nested across the width) + "
                 f"~{round(cup_marker / 10.0) * 10:.0f} mm of cups (2 self + 2 lining, "
                 "55% marker efficiency); greatest stretch (weft) runs across the cup"},
        {"item": "clear swim elastic 6 mm (lower/underbust)", "qty": lower_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {lower_opening:.0f} mm opening x {edge_elastic_ratio:.2f} "
                 "(both cups); zigzag into the marked lower zone, catch both layers"},
        {"item": "clear swim elastic 6 mm (side/outer)", "qty": side_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {side_opening:.0f} mm opening x {edge_elastic_ratio:.2f} "
                 "(both cups); zigzag into the marked side zone before turning"},
        {"item": "neck / halter tie strip", "qty": neck_tie_len,
         "unit": "mm_length",
         "note": f"one strip, finished width {tie_width:.0f} mm; span {neck_span:.0f} mm "
                 f"through both casings + 2 x {tie_tail:.0f} mm tails to knot at the nape"},
        {"item": "underbust band tie strip", "qty": band_tie_len,
         "unit": "mm_length",
         "note": f"one strip, finished width {tie_width:.0f} mm; span {band_span:.0f} mm "
                 f"across both lower edges + 2 x {tie_tail:.0f} mm tails to knot at the back"},
        {"item": "optional slider/ring pair (adjustable halter)", "qty": 2, "unit": "pcs",
         "note": "OPTIONAL — omit for a pure string tie. If adjustable: reference "
                 "a Yantra4D slider/ring cartridge (notion.hardware_ref), not "
                 "re-modelled here per the federation contract"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; 4-thread overlock the cup self/lining "
                 "seams, zigzag or coverstitch the clear elastic, edgestitch the ties"},
    ]
    pattern.metadata = {
        "fc100_rank": 55,
        "fabric_hint": "tricot-nylon-elastano",
        "style": "classic triangle / sliding-triangle string bikini top; ties, no hardware",
        "coverage": "triangle cups, halter-tied at the neck and banded/tied under the bust; "
                    "adjustable via the sliding casing (and optional sliders)",
        "fit_note": "close, tensioned swim fit — negative ease holds the cup to the body "
                    "when wet. Teaching-grade: a single bust + underbust pair drives the "
                    "cup (no separate cup-size bands yet), the triangle is unpadded/unwired, "
                    "and coverage is minimal by design — this is a string-triangle, not a "
                    "supportive bra",
        "stretch_note": "cut with greatest stretch (weft) horizontal, around the cup; "
                        "chlorine-resistant swim tricot with a knit lining",
        "negative_ease_pct": negative_ease_pct,
        "cup_base_mm": round(BASE, 1),
        "cup_height_mm": round(HEIGHT, 1),
        "cup_lower_edge_mm": round(lower_len, 1),
        "cup_side_edge_mm": round(side_len, 1),
        "cup_casing_edge_mm": round(casing_len, 1),
        "lower_opening_mm": round(lower_opening, 1),
        "lower_elastic_mm": lower_elastic,
        "side_opening_mm": round(side_opening, 1),
        "side_elastic_mm": side_elastic,
        "neck_tie_mm": neck_tie_len,
        "band_tie_mm": band_tie_len,
        "drafting": "single-triangle cup cut 4 (2 self + 2 lining) at swim negative ease; "
                    "self/lining sewn along side + casing (delta 0 by construction), lower "
                    "edge clear-elastic bound, top edge a folded halter casing; neck + band "
                    "ties are free threaded strips sized from the measured cup edges; swim "
                    "elastic and tie cut lengths derived exactly from the measured openings",
    }
    return pattern


result = build()
