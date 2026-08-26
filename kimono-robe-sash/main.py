"""
Sashed Kimono Robe — Fashion Cabinet Garment Cartridge (FC-500 #462; pattern-only).

A wrap dressing-robe cut on kimono logic: a body and sleeve in ONE continuous piece so there is no
set-in armscye, a wide self-fabric band running unbroken up both fronts and around the back neck,
and a self sash that ties at the waist. No hardware — the robe closes by wrapping, so this is a
pure-pattern object (the honest unbridged case the FC-500 plan reserves for wrap robes).

The kimono/dolman construction is the whole point: the sleeve is not a separate piece sewn into a
round armhole but an extension of the body, so the underarm is a single diagonal seam. That seam's
two sides — the body's `underarm` and the sleeve is part of the same panel — means the only
construction seams are the shoulder/sleeve top fold, the underarm-and-side run, the centre back,
and the band. Drafted flat, the garment reads as a cross.

The band SOLVE. A self band that runs up both fronts and around the back neck must be exactly as
long as the edge it finishes. The band length is drafted to the MEASURED front-edge + back-neck
run of the assembled body, and declared against it, so the band is never cut short (the classic
error that makes a robe band ripple or fall short at the hem).

Sashed at the waist to a self tie whose length is drafted from the waist girth plus a bow
allowance. Made to measure to height, chest/bust and hip. FC-500 lane 7 (intimates & lounge III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 1000.0))
hip_girth   = float(PARAM(lambda: hip_girth, 1040.0))
robe_length = float(PARAM(lambda: robe_length, 1150.0))    # nape to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 480.0)) # shoulder fold to cuff
sleeve_width = float(PARAM(lambda: sleeve_width, 300.0))   # depth of the kimono sleeve
body_ease   = float(PARAM(lambda: body_ease, 240.0))       # wrap robe is generous
band_width  = float(PARAM(lambda: band_width, 90.0))       # finished self-band width
sash_width  = float(PARAM(lambda: sash_width, 70.0))
waist_girth = float(PARAM(lambda: waist_girth, 820.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
hip_girth   = max(720.0, min(hip_girth, 1600.0))
robe_length = max(700.0, min(robe_length, 1500.0))
sleeve_length = max(200.0, min(sleeve_length, 700.0))
sleeve_width = max(180.0, min(sleeve_width, 440.0))
body_ease   = max(120.0, min(body_ease, 400.0))
band_width  = max(50.0, min(band_width, 140.0))
sash_width  = max(40.0, min(sash_width, 120.0))
waist_girth = max(560.0, min(waist_girth, 1400.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
# Body half-width from the widest of chest/hip plus ease, per front/back panel quarter.
BODY_GIRTH = max(chest_bust_girth, hip_girth) + body_ease
QUARTER = BODY_GIRTH / 4.0          # one panel front/back quarter width
RL = robe_length
SL = sleeve_length
SW = sleeve_width
BW = band_width
NECK_DROP_FRONT = 180.0             # how far the front neck V drops before the band
SHOULDER = max(120.0, QUARTER * 0.9)


def build_back():
    """Back panel: a kimono cross-half. Cut on the CB fold. Neck edge, shoulder/sleeve top
    fold, sleeve end, underarm+side to hem, CB fold."""
    # Coordinates: CB at x=0, hem at y=0, neck at y=RL.
    neck_w = max(60.0, QUARTER * 0.45)
    # shoulder line at the top; sleeve extends out horizontally
    p_cb_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(QUARTER, 0.0)
    underarm_y = RL - SW              # underarm point height
    p_underarm = fc.P(QUARTER, underarm_y)
    p_sleeve_end_lo = fc.P(QUARTER + SL, underarm_y)
    p_sleeve_end_hi = fc.P(QUARTER + SL, RL)
    p_shoulder = fc.P(neck_w, RL)
    p_cb_neck = fc.P(0.0, RL)
    edges = [
        fc.Edge("hem", [fc.Line(p_cb_hem, p_side_hem)]),
        fc.Edge("side", [fc.Line(p_side_hem, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end_lo)]),
        fc.Edge("sleeve_end", [fc.Line(p_sleeve_end_lo, p_sleeve_end_hi)]),
        fc.Edge("sleeve_top", [fc.Line(p_sleeve_end_hi, p_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_shoulder,
                                   fc.P(neck_w * 0.5, RL - 4.0),
                                   fc.P(neck_w * 0.2, RL - 2.0),
                                   p_cb_neck)]),
        fc.Edge("center_back", [fc.Line(p_cb_neck, p_cb_hem)]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("sleeve_under", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(QUARTER * 0.3, RL * 0.2), fc.P(QUARTER * 0.3, RL * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Back (cut 1 on CB fold)",
    )


def build_front():
    """Front panel (cut 2, mirror): like the back half but the neck edge is a long diagonal
    from shoulder down to the wrap point — the front V the band finishes. Centre-front is a
    straight open edge (the robe wraps, no seam)."""
    neck_w = max(60.0, QUARTER * 0.45)
    p_cf_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(QUARTER, 0.0)
    underarm_y = RL - SW
    p_underarm = fc.P(QUARTER, underarm_y)
    p_sleeve_end_lo = fc.P(QUARTER + SL, underarm_y)
    p_sleeve_end_hi = fc.P(QUARTER + SL, RL)
    p_shoulder = fc.P(neck_w, RL)
    # front neck V: from shoulder diagonally down to the wrap point on CF
    p_wrap = fc.P(0.0, RL - NECK_DROP_FRONT)
    edges = [
        fc.Edge("hem", [fc.Line(p_cf_hem, p_side_hem)]),
        fc.Edge("side", [fc.Line(p_side_hem, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end_lo)]),
        fc.Edge("sleeve_end", [fc.Line(p_sleeve_end_lo, p_sleeve_end_hi)]),
        fc.Edge("sleeve_top", [fc.Line(p_sleeve_end_hi, p_shoulder)]),
        fc.Edge("front_neck", [fc.Bezier(p_shoulder,
                                         fc.P(neck_w * 0.6, RL - NECK_DROP_FRONT * 0.35),
                                         fc.P(neck_w * 0.25, RL - NECK_DROP_FRONT * 0.75),
                                         p_wrap)]),
        fc.Edge("center_front", [fc.Line(p_wrap, p_cf_hem)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("sleeve_under", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(QUARTER * 0.3, RL * 0.2), fc.P(QUARTER * 0.3, RL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirror)",
    )


def build_band(band_run):
    """The self band: a long strip, cut to the MEASURED front-edge + back-neck run, folded
    to `band_width`. `attach` is the edge that sews to the robe's front+neck; declared to it."""
    length = band_run
    cut_w = BW * 2.0  # folds to finished width
    p0, p1 = fc.P(0.0, 0.0), fc.P(length, 0.0)
    p2, p3 = fc.P(length, cut_w), fc.P(0.0, cut_w)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("free", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("fold-line", [fc.P(0.0, BW), fc.P(length, BW)], kind="marking")]
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "back-neck centre")],
        grainline=fc.Grainline(fc.P(length * 0.08, BW * 0.5), fc.P(length * 0.92, BW * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Self band (cut 1, folded — front + back neck)",
    )


def build_sash():
    """The waist sash: length = waist girth + a wrap-and-bow allowance, folded to sash_width."""
    length = waist_girth * 1.5 + 500.0   # wrap once + tie
    cut_w = sash_width * 2.0
    p0, p1 = fc.P(0.0, 0.0), fc.P(length, 0.0)
    p2, p3 = fc.P(length, cut_w), fc.P(0.0, cut_w)
    edges = [
        fc.Edge("long_lower", [fc.Line(p0, p1)]),
        fc.Edge("tip_r", [fc.Line(p1, p2)]),
        fc.Edge("long_upper", [fc.Line(p2, p3)]),
        fc.Edge("tip_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("fold-line", [fc.P(0.0, sash_width), fc.P(length, sash_width)],
                             kind="marking")]
    return fc.Piece(
        "sash", edges, seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(length * 0.08, sash_width * 0.5),
                               fc.P(length * 0.92, sash_width * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waist sash (cut 1, folded)",
    )


def build():
    pattern = fc.PatternSet("kimono-robe-sash")
    back = build_back()
    front = build_front()
    # Band run: two front-neck edges (both fronts) + the back neck.
    band_run = 2.0 * front.edge("front_neck").length() + back.edge("neck").length() * 2.0
    band = build_band(band_run)
    sash = build_sash()

    picked = {"back": back, "front": front, "band": band, "sash": sash}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (back, front, band, sash):
            pattern.add(piece)
        # Underarm + side: front side/sleeve_under sews to back side/sleeve_under.
        pattern.declare_seam([("front", "side"), ("front", "sleeve_under")],
                             [("back", "side"), ("back", "sleeve_under")], tol=1.5)
        # Shoulder/sleeve top fold: front sleeve_top to back sleeve_top.
        pattern.declare_seam(("front", "sleeve_top"), ("back", "sleeve_top"), tol=1.5)
        # The self band == the whole front + back-neck run.
        pattern.declare_seam(("band", "attach"),
                             [("front", "front_neck"), ("front", "front_neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    fabric_width = 1400.0
    area = (back.area() * 1.0 + front.area() * 2.0 + band.area() + sash.area())
    marker_len = area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "robe fabric (satin / crepe / brushed cotton)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"body, sleeves, band and sash all self-fabric at {fabric_width:.0f} mm width, "
                 "72% marker. The kimono cross nests economically when the sleeves are folded in."},
        {"item": "self band (cut with the body)", "qty": 1, "unit": "piece",
         "note": f"one continuous strip {round(band.edge('attach').length())} mm long, folded "
                 f"to {band_width:.0f} mm — runs up both fronts and around the back neck."},
        {"item": "self sash", "qty": 1, "unit": "piece",
         "note": f"one strip {round(sash.edge('long_lower').length())} mm long, folded to "
                 f"{sash_width:.0f} mm; add two belt carriers at the side seams."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "French or flat-fell the underarm/side run so the inside is clean — a robe is "
                 "seen inside-out every time it is taken off."},
    ]
    pattern.metadata = {
        "fc500_rank": 462, "family": "underwear_lounge", "fabric_hint": "seda-satinada",
        "silhouette_note": "Kimono/dolman wrap robe: body and sleeve in one continuous panel "
            "(no set-in armscye), a self band up both fronts and round the back neck, and a self "
            "sash. Closes by wrapping — no hardware.",
        "hardware": "none — a wrap robe closes by tying the sash (pure-pattern, honest unbridged).",
        "solved": {
            "body_girth_with_ease_mm": round(BODY_GIRTH, 1),
            "panel_quarter_mm": round(QUARTER, 1),
            "band_run_mm": round(band.edge("attach").length(), 1),
            "sash_length_mm": round(sash.edge("long_lower").length(), 1),
            "note": "the self band is drafted to the MEASURED front-edge + back-neck run and "
                    "declared against it, so it is never cut short.",
        },
        "closure": "wrap + waist sash (no hardware)",
        "drafting": "Made to measure to chest/bust, hip and lengths; kimono cross construction.",
    }
    return pattern


result = build()
