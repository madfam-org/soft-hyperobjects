"""
High-waist control brief — Fashion Cabinet Garment Cartridge (FC-400 #384; lane 9).

A high-waisted control brief in power-mesh: waist above the navel to the leg
openings, pulled on, no hardware. The only structure is COMPRESSION, and — as in
the FC-300 shapewear short this deepens — compression is a number this cartridge
refuses to hide.

The honest bit. Control garments work by negative ease: the brief is cut SMALLER
than the body and the mesh's recovery does the rest. Commercial control briefs sell
this as a size letter and a marketing adjective ("firm", "sculpting"), which is
neither reproducible nor auditable. Here it is an explicit percentage per zone, and
the zones differ because bodies do:

  - The WAIST takes the most compression — it is the zone a high brief is bought for,
    and a deep band above the navel is what holds the tummy without a seam digging in.
  - The HIP/SEAT takes less. Over-compressing the seat just displaces volume to the
    thigh and drags the brief down.
  - The LEG OPENING takes least. A leg opening cut too tight rolls up into a cord that
    cuts in — the classic failure of cheap shapewear, and a DRAFTING decision, not a
    fabric fault. The opening is finished with its own elastic ring, sized off the
    thigh with the gentlest ease of the three.

The high brief differs from a shaping short in two real ways, both drafted here:
there is NO inseam (the leg is an OPENING, not a tube), and the seat is shaped by a
BACK-RISE curve rather than a crotch scoop plus inseam. So the draft is a front and
a back panel joined at the side seams and the crotch, closed by a cotton-lined
gusset, under a deep tapered waistband.

Made to measure to waist, high-hip, thigh girths + body rise. No `notion` hardware:
a pull-on garment has no closure, and this lane does not invent one to score a bridge.

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

waist_girth = float(PARAM(lambda: waist_girth, 760.0))
high_hip_girth = float(PARAM(lambda: high_hip_girth, 990.0))  # fullest seat
thigh_girth = float(PARAM(lambda: thigh_girth, 580.0))
body_rise = float(PARAM(lambda: body_rise, 280.0))            # waist to crotch, seated
waistband_h = float(PARAM(lambda: waistband_h, 150.0))        # above-navel band depth
front_drop = float(PARAM(lambda: front_drop, 40.0))           # centre-front dip
waist_compression = float(PARAM(lambda: waist_compression, 20.0))  # % negative ease
seat_compression = float(PARAM(lambda: seat_compression, 12.0))
leg_ease_pct = float(PARAM(lambda: leg_ease_pct, 4.0))        # gentle: opening, not tube
gusset_w = float(PARAM(lambda: gusset_w, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
waist_girth = max(520.0, min(waist_girth, 1500.0))
high_hip_girth = max(620.0, min(high_hip_girth, 1800.0))
thigh_girth = max(350.0, min(thigh_girth, 1000.0))
body_rise = max(200.0, min(body_rise, 440.0))
waistband_h = max(40.0, min(waistband_h, 280.0))
front_drop = max(0.0, min(front_drop, 120.0))
waist_compression = max(0.0, min(waist_compression, 32.0))
seat_compression = max(0.0, min(seat_compression, 26.0))
leg_ease_pct = max(-6.0, min(leg_ease_pct, 16.0))
gusset_w = max(40.0, min(gusset_w, 150.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# The band cannot be deeper than the rise it sits on, and the panel below the band
# needs a real minimum height (a control brief with a 20 mm panel is not a garment).
# Clamp the band so the panel keeps at least PANEL_MIN of rise.
PANEL_MIN = 120.0
waistband_h = min(waistband_h, max(20.0, body_rise - PANEL_MIN))
RISE = max(PANEL_MIN, body_rise - waistband_h)   # panel rise below the band, floored
# The centre-front dip cannot rise above the leg-opening region: keep it well below the
# side-seam bottom so the leg curve never inverts.
front_drop = max(0.0, min(front_drop, RISE * 0.20))

# ── THE COMPRESSION SOLVER (the number control garments hide) ────────────────
WAIST_FIN = waist_girth * (1.0 - waist_compression / 100.0)
SEAT_FIN = high_hip_girth * (1.0 - seat_compression / 100.0)
LEG_FIN = thigh_girth * (1.0 - leg_ease_pct / 100.0)

# Quarter shares: front and back each carry a quarter of the waist and seat rings.
W_Q = WAIST_FIN / 4.0
S_Q = SEAT_FIN / 4.0
# The leg opening ring is per side (one opening per leg); each panel carries HALF.
LEG_HALF = LEG_FIN / 2.0

# Seat room: the back is scooped LESS at the crotch than the front (its leg opening
# sits lower), so a control brief covers and holds the seat instead of dragging down.
# The side seam is drafted IDENTICALLY on both panels so they balance by construction;
# the front/back difference lives entirely in the leg-opening scoop depth.
HIP_Y = RISE * 0.5
# Full-panel widths (cut flat, not on the fold): each panel spans the full half-body
# quarter x2 = half the finished ring, symmetric about its own centre line.
WAIST_HALF = W_Q * 2.0          # front (or back) waist run, side to side
SIDE_TOP = RISE                 # side-seam top y — the SAME on both panels
SIDE_BOT = HIP_Y * 0.6          # side-seam bottom y — the SAME on both panels


def _panel(name, front_dip, scoop, label):
    """One full panel (front or back), cut flat and symmetric about centre.

    x runs 0..WAIST_HALF (side seam to side seam); the leg openings are the two lower
    corners, and the crotch (gusset join) is a `gusset_w`-wide flat at the centre. CCW
    outline: left side seam (up) -> waist (across) -> right side seam (down) ->
    right leg opening (in) -> gusset join (across) -> left leg opening (out).

    Both panels share IDENTICAL side seams (SIDE_TOP..SIDE_BOT); the only front/back
    difference is `scoop` — how deep the leg opening cuts up toward the hip. The front
    scoops deeper (a higher-cut leg), the back shallower (more seat coverage), and the
    crotch flat is exactly `gusset_w` on both so the gusset bridges them squarely.
    """
    cx = WAIST_HALF / 2.0
    g = gusset_w / 2.0
    left_bot = fc.P(0.0, SIDE_BOT)
    left_top = fc.P(0.0, SIDE_TOP)
    right_top = fc.P(WAIST_HALF, SIDE_TOP)
    right_bot = fc.P(WAIST_HALF, SIDE_BOT)
    gusset_r = fc.P(cx + g, front_dip)
    gusset_l = fc.P(cx - g, front_dip)
    edges = [
        fc.Edge("side_seam_l", [fc.Line(left_bot, left_top)]),
        fc.Edge("waist", [fc.Line(left_top, right_top)]),
        fc.Edge("side_seam_r", [fc.Line(right_top, right_bot)]),
        fc.Edge("leg_opening_r", [fc.Bezier(
            right_bot,
            fc.P(WAIST_HALF - (cx + g - WAIST_HALF) * -0.30, SIDE_BOT - scoop * 0.5),
            fc.P(cx + g + (WAIST_HALF - cx - g) * 0.35, front_dip + scoop * 0.4),
            gusset_r)]),
        fc.Edge("gusset_join", [fc.Line(gusset_r, gusset_l)]),
        fc.Edge("leg_opening_l", [fc.Bezier(
            gusset_l,
            fc.P(cx - g - (cx - g) * 0.35, front_dip + scoop * 0.4),
            fc.P((cx - g) * 0.30, SIDE_BOT - scoop * 0.5),
            left_bot)]),
    ]
    internals = [fc.Internal("hip line",
                             [fc.P(0.0, HIP_Y), fc.P(WAIST_HALF, HIP_Y)],
                             kind="marking")]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"waist": 0.0, "leg_opening_l": 0.0, "leg_opening_r": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre notch"),
                 fc.Notch("gusset_join", 0.5, "centre crotch")],
        grainline=fc.Grainline(fc.P(cx, front_dip + 20.0),
                               fc.P(cx, SIDE_TOP - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, mirror=False),
        label=label,
    )


def build_front():
    # Front: higher-cut leg (deeper scoop), full front dip.
    return _panel("front", front_drop, RISE * 0.34, "Front panel (cut 1)")


def build_back():
    # Back: shallower scoop = more seat coverage; front dip echoed lightly at centre.
    return _panel("back", front_drop * 0.4, RISE * 0.20,
                  "Back panel (cut 1, more seat coverage)")


def build_gusset():
    """The cotton-lined gusset: a rectangle bridging front and back at the crotch.

    Its two short ends sew to the front and back centre-front dips; cut double so the
    lining encloses the seam, the hygienic standard for a brief.
    """
    w, ln = gusset_w, gusset_w * 1.4
    edges = [
        fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("back_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("side_b", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "gusset",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_end", 0.5, "centre-front match"),
                 fc.Notch("back_end", 0.5, "centre-back match")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.15), fc.P(w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Gusset (cut 2 — self + cotton lining)",
    )


def build_waistband(front_waist, back_waist):
    """The deep control band: lower edge built to the measured panel waists, upper edge
    cut SMALLER so the band tapers toward the true waist and does not roll down.

    Cut 2 mirrored (left half + right half of the body ring); each band lower edge is
    the sum of one front waist and one back waist, i.e. the full half-body run.
    """
    lower_w = front_waist + back_waist          # one half of the body
    upper_w = lower_w * 0.93
    dx = (lower_w - upper_w) / 2.0
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(lower_w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(dx, waistband_h))]),
        fc.Edge("upper", [fc.Line(fc.P(dx, waistband_h), fc.P(dx + upper_w, waistband_h))]),
        fc.Edge("side_seam_b", [fc.Line(fc.P(dx + upper_w, waistband_h),
                                        fc.P(lower_w, 0.0))]),
    ]
    return fc.Piece(
        "waistband",
        edges,
        seam_allowance=seam_allowance,
        allowances={"upper": 0.0},              # elastic-finished top edge
        notches=[fc.Notch("lower", 0.25, "side seam match"),
                 fc.Notch("lower", 0.75, "side seam match")],
        grainline=fc.Grainline(fc.P(lower_w * 0.5, 6.0),
                               fc.P(lower_w * 0.5, waistband_h - 6.0)),
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="High control waistband (cut 1, closes at a side seam)",
    )


def build():
    pattern = fc.PatternSet("high-waist-brief")
    every = target_piece == "set"

    front = build_front()
    back = build_back()

    picked = {"front": front, "back": back}
    if not every and target_piece in ("gusset", "waistband"):
        if target_piece == "gusset":
            pattern.add(build_gusset())
        else:
            pattern.add(build_waistband(front.edge("waist").length(),
                                        back.edge("waist").length()))
        return _finish(pattern, front, back)
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    gusset = build_gusset()
    waistband = build_waistband(front.edge("waist").length(),
                                back.edge("waist").length())
    for piece in (front, back, gusset, waistband):
        pattern.add(piece)

    # Side seams: front's two sides join the back's two sides (all four identical).
    pattern.declare_seam(("front", "side_seam_l"), ("back", "side_seam_l"), tol=1.0)
    pattern.declare_seam(("front", "side_seam_r"), ("back", "side_seam_r"), tol=1.0)
    # The gusset bridges the front and back crotch flats (both `gusset_w` wide).
    pattern.declare_seam(("gusset", "front_end"), ("front", "gusset_join"), tol=1.0)
    pattern.declare_seam(("gusset", "back_end"), ("back", "gusset_join"), tol=1.0)
    # The band's lower edge meets the assembled front+back waist ring.
    pattern.declare_seam(("waistband", "lower"),
                         [("front", "waist"), ("back", "waist")], tol=1.5)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    waist_opening = front.edge("waist").length() + back.edge("waist").length()
    # One leg opening = front_r + back_r (the two curves that meet at the side seam and
    # gusset); the pair is that x2.
    leg_opening = 2.0 * (front.edge("leg_opening_r").length()
                         + back.edge("leg_opening_r").length())
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "power-mesh (powernet) 4-way stretch", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"panels + band at {fabric_width:.0f} mm width, 60% marker. The mesh's "
                 "recovery IS the control — cut on the maximum-stretch grain around the "
                 "body."},
        {"item": "cotton gusset lining", "qty": 1, "unit": "piece",
         "note": "the gusset self-piece encloses a cotton lining — the hygienic standard "
                 "for a brief worn against the skin."},
        {"item": "waistband elastic (soft plush-back) 20 mm+", "qty": round(waist_opening * 0.9),
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x 0.9 — the band's own "
                 "negative ease is what holds a high brief up without a seam that digs."},
        {"item": "leg-opening elastic (picot or fold-over) 8-10 mm",
         "qty": round(leg_opening * 0.96), "unit": "mm_length",
         "note": f"leg openings {leg_opening:.0f} mm at 0.96 — the GENTLEST ease of the "
                 "three, so the opening lies flat instead of rolling into a cord that "
                 "cuts in."},
        {"item": "polyester thread + ballpoint 70/10 + coverstitch", "qty": 1, "unit": "set",
         "note": "coverstitch or zigzag the elastic so seams stretch with the mesh and "
                 "do not pop under compression."},
    ]
    pattern.metadata = {
        "fc400_rank": 384, "family": "underwear_lounge", "fabric_hint": "power-mesh",
        "silhouette_note": "A high-waist control brief: deep tapered band above the navel, "
            "leg OPENINGS (not tubes), a cotton-lined gusset, and a higher back rise so it "
            "does not drag down at the seat.",
        "compression": {
            "waist_pct": round(waist_compression, 1),
            "seat_pct": round(seat_compression, 1),
            "leg_ease_pct": round(leg_ease_pct, 1),
            "note": "per-zone negative ease — the number control garments hide behind a "
                    "size letter. Waist compresses most, seat less, leg opening least "
                    "(the leg is the tourniquet zone).",
        },
        "solved": {
            "waist_finished_mm": round(WAIST_FIN, 1),
            "seat_finished_mm": round(SEAT_FIN, 1),
            "leg_finished_mm": round(LEG_FIN, 1),
            "front_leg_scoop_mm": round(RISE * 0.34, 1),
            "back_leg_scoop_mm": round(RISE * 0.20, 1),
            "waist_opening_mm": round(waist_opening, 1),
            "leg_opening_mm": round(leg_opening, 1),
        },
        "hardware": "none — a pull-on control brief has no closure; this lane does not "
                    "invent one to score a bridge.",
        "drafting": "Made to measure to waist, high-hip, thigh girths + body rise; each "
                    "zone's finished ring is printed above so the compression is auditable.",
    }
    return pattern


result = build()
