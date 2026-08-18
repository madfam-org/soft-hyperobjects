"""
Track pants — FC-100 rank #50. Fashion Cabinet Garment Cartridge.

The classic athletic track pant: the side-seamed trouser block cut RELAXED
(a straight-to-slightly-tapered leg with small POSITIVE ease — NOT compression;
the power-stretch interlock only lends comfort give), an elastic waistband
casing with an optional drawcord, and the signature contrast SIDE STRIPE(S)
running the full outseam of both legs. The ankle is either an elastic/rib cuff
(cut 2, length derived from the ankle opening) or a plain open hem.

Idioms borrowed:
  - joggers / sweatpants: separate front/back legs, the front inseam bowed by a
    SOLVED amount to match the deeper back fork, sides equal by construction,
    and rib cuff + waistband casing derived from the measured edges.
  - panties-bikini: an fc.Internal trace laid parallel to an edge (here the
    outseam, for the side stripe) and EXACT-MM notion cut lengths (waist
    elastic, drawcord, contrast tape) derived from the measured openings.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|cuff|waistband|set

hip_girth     = float(PARAM(lambda: hip_girth, 1000.0))
inseam_length = float(PARAM(lambda: inseam_length, 720.0))
front_rise    = float(PARAM(lambda: front_rise, 265.0))
back_rise     = float(PARAM(lambda: back_rise, 305.0))
relaxed_ease  = float(PARAM(lambda: relaxed_ease, 150.0))   # POSITIVE ease at the hip
hem_width     = float(PARAM(lambda: hem_width, 115.0))       # ankle half-width, flat
cuffed        = bool(PARAM(lambda: cuffed, True))
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.80))
cuff_height   = float(PARAM(lambda: cuff_height, 55.0))
elastic_width = float(PARAM(lambda: elastic_width, 40.0))
elastic_ratio = float(PARAM(lambda: elastic_ratio, 0.92))   # waist elastic / opening
drawcord      = bool(PARAM(lambda: drawcord, True))
stripe_count  = int(PARAM(lambda: stripe_count, 2))          # 1 or 2 side stripes
stripe_width  = float(PARAM(lambda: stripe_width, 18.0))     # each stripe, mm
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))   # used only when open-hemmed

# ── Clamps (mirror the manifest sliders) ─────────────────────────────────────
hip_girth = max(650.0, min(hip_girth, 1800.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
relaxed_ease = max(60.0, min(relaxed_ease, 400.0))
hem_width = max(85.0, min(hem_width, 220.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.98))
cuff_height = max(30.0, min(cuff_height, 90.0))
elastic_width = max(20.0, min(elastic_width, 70.0))
elastic_ratio = max(0.80, min(elastic_ratio, 1.0))
stripe_count = 2 if stripe_count >= 2 else 1
stripe_width = max(6.0, min(stripe_width, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Derived draft dimensions ─────────────────────────────────────────────────
HIP_E = hip_girth + relaxed_ease            # positive ease → relaxed fit
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0       # relaxed: hem stays wide (straight leg)
STRIPE_INSET = 14.0                          # first stripe centre, mm in from outseam
STRIPE_GAP = 10.0                            # gap between the two stripes, mm


def _side_stripe(side_edge):
    """Contrast side-stripe trace(s) parallel to the outseam ('side' edge).

    Pieces are authored CCW; the inward normal at a tangent (tx, ty) is
    (-ty, tx). We lay `stripe_count` traces stepping inward from the seam so
    they ride the full outseam — the visible signature of a track pant.
    """
    traces = []
    for k in range(stripe_count):
        offset = STRIPE_INSET + k * (stripe_width + STRIPE_GAP)
        pts = []
        samples = 24
        for i in range(samples):
            t = i / (samples - 1)
            p, tan = side_edge.point_at_fraction(t)
            pts.append(fc.P(p.x - tan.y * offset, p.y + tan.x * offset))
        label = "side stripe" if stripe_count == 1 else f"side stripe {k + 1}"
        traces.append(fc.Internal(label, pts, kind="trace"))
    return traces


def build_legs():
    """Front/back relaxed legs; the front inseam is bowed to the deeper back."""
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    def f_inseam(bulge):
        return fc.Edge("inseam", [fc.curve_through(f_tip, fc.P(FHW, 0.0),
                                                   bulge=bulge, side=-1.0)])

    b_inseam = fc.Edge("inseam", [fc.Line(b_tip, fc.P(BHW, 0.0))])
    back_len = b_inseam.length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):                       # bow the front inseam to match the back
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge to the back inseam length")

    # Open-hem legs turn a real hem; cuffed legs seam onto the rib/elastic cuff.
    leg_hem_allowance = seam_allowance if cuffed else hem_allowance

    def make(name, width, tip, inseam_edge, hem_w, cb_y, label):
        waist_in = width * 0.92
        side_edge = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))])
        edges = [
            side_edge,
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(waist_in, cb_y), fc.P(width - 4.0, cb_y - front_rise * 0.45),
                           fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)],
            ),
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": leg_hem_allowance},
            notches=[fc.Notch("inseam", 0.5), fc.Notch("side", 0.5)],
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            internals=_side_stripe(side_edge),
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("front", FW, f_tip, f_inseam(bulge), FHW, WAIST_Y, "Front Leg")
    back = make("back", BW, b_tip, b_inseam, BHW, WAIST_Y + (back_rise - front_rise),
                "Back Leg")
    return front, back


def _band(name, finished_len, finished_height, qty, label, eyelets=False):
    """Rectangular fold-over band (cuff or waistband casing)."""
    band_h = 2.0 * finished_height
    length = finished_len + 2.0 * seam_allowance
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)])]
    if eyelets:
        # Two drawcord eyelet marks straddling the centre-front of the casing.
        cx = length / 2.0
        ey = band_h * 0.75                    # on the outer (public) half of the fold
        for dx in (-1.0, 1.0):
            ex = cx + dx * 45.0
            internals.append(fc.Internal("drawcord eyelet",
                                         [fc.P(ex - 5.0, ey), fc.P(ex + 5.0, ey),
                                          fc.P(ex, ey - 5.0), fc.P(ex, ey + 5.0)],
                                         kind="drill"))
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("track-pants")
    front, back = build_legs()
    everything = target_piece == "set"

    ankle_circ = front.edge("hem").length() + back.edge("hem").length()   # per leg
    waist_circ = 2.0 * (front.edge("waist").length() + back.edge("waist").length())
    outseam = front.edge("side").length()   # == back.edge("side") by construction

    # Bands are built up-front so declared seams can read their exact bottom-edge
    # length; the casing/cuff carry their own join allowance (2 x seam_allowance)
    # and the cuff is deliberately drafted SMALLER than the ankle (rib recovers),
    # so both band seams balance via an exact measured `ease`, not a fudged tol.
    wb = _band("waistband", waist_circ, elastic_width + seam_allowance, 1,
               "Waistband Casing", eyelets=drawcord)
    cuff_piece = _band("cuff", ankle_circ * cuff_ratio, cuff_height, 2,
                       "Ankle Cuff (elastic/rib)") if cuffed else None

    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if cuffed and (everything or target_piece == "cuff"):
        pattern.add(cuff_piece)
    if everything or target_piece == "waistband":
        pattern.add(wb)

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        # Waistband casing (a ring) sews onto BOTH leg waists summed x2 legs.
        # ease = band bottom length over the summed opening (its join allowance).
        wb_ease = wb.edge("bottom").length() - waist_circ
        pattern.declare_seam(
            ("waistband", "bottom"),
            [("front", "waist"), ("front", "waist"),
             ("back", "waist"), ("back", "waist")],
            tol=1.5, ease=wb_ease,
        )
        if cuffed:
            # One cuff (a ring) closes one leg = front hem + back hem of that leg.
            # ease is negative: the cuff is smaller than the ankle opening.
            cuff_ease = cuff_piece.edge("bottom").length() - ankle_circ
            pattern.declare_seam(
                ("cuff", "bottom"),
                [("front", "hem"), ("back", "hem")],
                tol=1.5, ease=cuff_ease,
            )

    # ── Notion accounting (exact-mm, the factory spec numbers) ───────────────
    waist_opening = waist_circ                            # measured leg waists x2
    waist_elastic = round(waist_opening * elastic_ratio)
    stripe_tape = round(2.0 * outseam * stripe_count)     # 2 legs x outseam x count
    drawcord_len = round(waist_opening + 350.0) if drawcord else 0  # opening + tie tails

    fabric_width = 1550.0                                 # power-stretch card width
    piece_area = sum(p.area() for p in (front, back)) * 2.0     # front+back, cut 2 each
    total_area = piece_area + wb.area()
    if cuffed:
        total_area += cuff_piece.area() * 2.0                   # two ankle cuffs
    marker_len = total_area / (fabric_width * 0.62)

    bom = [
        {"item": "poliester-elastano-compresion",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"relaxed track pant at {fabric_width:.0f} mm width, ~62% marker "
                 "efficiency; greatest stretch weft (around the leg). Small POSITIVE "
                 "ease — this is a relaxed fit, not a compression cut"},
        {"item": f"waistband elastic {elastic_width:.0f} mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, feed through the casing"},
        {"item": f"contrast side-stripe tape {stripe_width:.0f} mm", "qty": stripe_tape,
         "unit": "mm_length",
         "note": f"{stripe_count} stripe(s) x 2 legs x {outseam:.0f} mm outseam; "
                 "topstitch down each outseam before closing the side seam"},
        {"item": "stretch/wooly thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11; flatlock or 3-thread overlock + coverstitch hems "
                 "to avoid chafe (per the fabric card)"},
    ]
    if cuffed:
        bom.insert(3, {"item": "ankle cuff rib/elastic", "qty": round(2.0 * cuff_height),
                       "unit": "mm_length",
                       "note": f"2 cuffs cut {round(ankle_circ * cuff_ratio)} mm each "
                               f"({ankle_circ:.0f} mm opening x {cuff_ratio:.2f}); "
                               "self-rib or 40 mm knit tube folded"})
    if drawcord:
        bom.append({"item": "drawcord", "qty": drawcord_len, "unit": "mm_length",
                    "note": f"flat or round cord: {waist_opening:.0f} mm opening + "
                            "350 mm tie tails; thread through the two casing eyelets"})
        bom.append({"item": "drawcord eyelets", "qty": 2, "unit": "pieces",
                    "note": "metal eyelet/grommet HARDWARE — Yantra4D cartridge "
                            "reference (eyelet), not drafted here; set at the two "
                            "marked centre-front drill points"})
    pattern.bom = bom

    pattern.metadata = {
        "fc100_rank": 50,
        "fabric_hint": "poliester-elastano-compresion",
        "fit_note": "RELAXED / straight-leg track pant with small positive ease "
                    "(relaxed_ease added to the hip girth) — NOT a compression cut; "
                    "the technical interlock only gives comfort stretch",
        "side_stripe": {
            "count": stripe_count,
            "each_width_mm": stripe_width,
            "outseam_mm": round(outseam, 1),
            "tape_total_mm": stripe_tape,
            "spec": "contrast tape topstitched down the outseam of both legs; "
                    "modelled as kind='trace' internals on front and back, aligned "
                    "across the side seam",
        },
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "ankle_opening_each_mm": round(ankle_circ, 1),
        "cuffed": cuffed,
        "cuff_length_each_mm": round(ankle_circ * cuff_ratio) if cuffed else None,
        "drawcord": drawcord,
        "drawcord_len_mm": drawcord_len,
        "drafting": "relaxed side-seamed leg (joggers block, straight hem); solved "
                    "front-inseam bow; derived waistband casing + optional ankle cuff; "
                    "side-stripe traces + exact-mm elastic/tape/cord accounting",
    }
    return pattern


result = build()
