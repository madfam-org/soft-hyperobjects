"""
Raglan knit pullover — FC-300 rank #292. Fashion Cabinet Garment Cartridge.

The raglan sweater: no shoulder seam and no armhole. Instead ONE diagonal seam
runs on each side from the underarm straight up to the neckline, and the sleeve
carries the shoulder itself. That is the whole architecture, and it is why the
raglan is the knitter's shape — a diagonal is a straight decrease line, so it
can be worked as full-fashioned shaping on the machine or the needles rather
than cut through a curve.

The commons already holds the set-in cut-and-sew knits (`crewneck-sweater`,
`turtleneck-sweater`, `cardigan`). This cartridge draws the OTHER knit body
architecture, and it makes the full-fashioned logic explicit:

  - THE RAGLAN LINE (the definition): a straight diagonal from the underarm
    point to the neckline. Its rise and its run are both solved from measured
    quantities, never assumed, and the sleeve's two raglan edges are drafted
    from the SAME solved rise so the four raglan seams balance by construction
    rather than by luck.
  - FULL-FASHIONED SHAPING: the diagonal is marked with the decrease ladder a
    knitter actually works — `fashion_step` stitches in from the edge, one
    paired decrease every `fashion_rows` rows. The internal markings are the
    ladder, so the pattern carries the shaping instruction and not merely the
    finished silhouette.
  - NEGATIVE EASE: sweater knit is drafted SMALLER than the body and stretches
    onto it. `knit_ease` is therefore signed and defaults NEGATIVE (-60 mm), the
    opposite sign convention from every woven block in the commons. The clamp
    floor stops the body ever shrinking past a wearable minimum.

Drafting note — what actually SOLVES. The body's raglan and the sleeve's raglan
are drafted as CONGRUENT right triangles: same rise, same run. The rise comes
from the raglan depth less that panel's neck drop; the run is the neck span
(quarter width less half neck width) less the share `neck_share` gives the
sleeve heads. The sleeve is then drafted FROM those two numbers rather than
guessed at, so all four raglan seams balance to delta 0.0 with zero declared
ease at every parameter combination — nothing is absorbed by tolerance. The
body's neckline ends exactly on the raglan's neck point, because on a raglan
the neckline IS the raglan's upper terminus.

The clamps that protect it, and why they are not decoration: every one of those
quantities is DERIVED, and a derived dimension that goes negative does not
fail — it inverts the piece, and the kernel's CCW normalization then hands
`verify()` a valid-LOOKING outline. So the rise is floored at 90 mm, the neck
span at 50 mm, the run at 35 mm, the sleeve head at 22 mm, and the biceps is
solved as run + head so it can never be too narrow to contain its own raglan.
The decrease-ladder tick count is clamped the same way. Every floor is applied
BEFORE any point is built, and the metadata reports which ones bit.

Hardware: none. A pullover raglan has no closure at all — that is the point of
the shape — so this cartridge declares no `hardware_ref`.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|neckband|cuff|hem_band|set

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
body_length = float(PARAM(lambda: body_length, 640.0))     # nape to hem-band seam
neck_girth = float(PARAM(lambda: neck_girth, 390.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))  # neck end to cuff seam
knit_ease = float(PARAM(lambda: knit_ease, -60.0))         # SIGNED; negative = stretch on
raglan_depth = float(PARAM(lambda: raglan_depth, 250.0))   # underarm below the neckline
front_neck_drop = float(PARAM(lambda: front_neck_drop, 70.0))
neck_share = float(PARAM(lambda: neck_share, 0.30))    # sleeve heads' share of the neckline
fashion_step = float(PARAM(lambda: fashion_step, 9.0))     # decrease inset from the edge
fashion_rows = float(PARAM(lambda: fashion_rows, 24.0))    # rows between paired decreases
cuff_ratio = float(PARAM(lambda: cuff_ratio, 0.70))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.86))
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.82))
rib_height = float(PARAM(lambda: rib_height, 60.0))        # cuff / hem band depth
neckband_width = float(PARAM(lambda: neckband_width, 28.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (match the manifest slider bounds exactly) ────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(300.0, min(sleeve_length, 800.0))
knit_ease = max(-160.0, min(knit_ease, 120.0))
raglan_depth = max(150.0, min(raglan_depth, 400.0))
front_neck_drop = max(20.0, min(front_neck_drop, 160.0))
neck_share = max(0.10, min(neck_share, 0.55))
fashion_step = max(4.0, min(fashion_step, 20.0))
fashion_rows = max(8.0, min(fashion_rows, 60.0))
cuff_ratio = max(0.55, min(cuff_ratio, 0.95))
hemband_ratio = max(0.70, min(hemband_ratio, 1.0))
neckband_ratio = max(0.70, min(neckband_ratio, 1.0))
rib_height = max(25.0, min(rib_height, 110.0))
neckband_width = max(15.0, min(neckband_width, 55.0))
seam_allowance = max(6.0, min(seam_allowance, 18.0))

# ── The knit block: negative ease is the whole point ─────────────────────────
# `knit_ease` is SIGNED and normally negative — a sweater knit is drafted
# smaller than the measured body and stretches on. The floor keeps a draft that
# is still wearable even when the wearer asks for maximum compression.
DRAFT_GIRTH = max(520.0, chest_girth + knit_ease)
W = DRAFT_GIRTH / 4.0                          # quarter body width
L = body_length
NW = max(52.0, neck_girth * neckband_ratio / 5.0 + 6.0)   # half neck width
BACK_NECK_DROP = 18.0
NECK_Y = L + 20.0                              # back-neck level = top of the draft

# ── The raglan line: rise and run, both solved and both CLAMPED ──────────────
# The raglan rise is the vertical distance the diagonal climbs, from the
# underarm point to the neckline end of the seam. It is derived — the requested
# raglan depth less however far the neckline has already dropped on that piece.
# At extremes (short body, very deep front neck) the derivation can reach zero
# or go NEGATIVE, which would invert the piece into valid-looking-but-wrong
# geometry after CCW normalization. So both rises are floored here, before any
# point is built, and the sleeve is drafted from these same clamped values.
RAGLAN_RISE_MIN = 90.0                         # a raglan seam shorter than this is not one
UNDERARM_Y = max(60.0, NECK_Y - raglan_depth)  # never below the hem
_back_rise_raw = (NECK_Y - BACK_NECK_DROP) - UNDERARM_Y
_front_rise_raw = (NECK_Y - front_neck_drop) - UNDERARM_Y
BACK_RISE = max(RAGLAN_RISE_MIN, _back_rise_raw)
FRONT_RISE = max(RAGLAN_RISE_MIN, _front_rise_raw)
RISE_CLAMPED = (_back_rise_raw < RAGLAN_RISE_MIN) or (_front_rise_raw < RAGLAN_RISE_MIN)

# The raglan RUN: how far in from the underarm the seam travels to reach its
# neck end. The available span is the quarter width less the half neck width —
# but the raglan does NOT consume all of it, because the sleeve's own head takes
# a share of the neckline. `neck_share` is that split: the fraction of the neck
# opening the two sleeve heads own, which is what a raglan actually looks like
# (a real sleeve head is a band across the neckline, not a point).
#
# Both the span and the run are derived, so both are floored: a very wide neck
# on a narrow body would otherwise give a run of zero (a vertical "raglan" and
# an unsewable neckline) or negative (inverted geometry that CCW normalization
# would launder into a valid-LOOKING outline).
_span_raw = W - NW
RAGLAN_SPAN = max(50.0, _span_raw)
RAGLAN_RUN = max(35.0, RAGLAN_SPAN * (1.0 - neck_share))
RUN_CLAMPED = (_span_raw < 50.0) or (RAGLAN_SPAN * (1.0 - neck_share) < 35.0)

# Where the body's raglan meets the neckline. The body's neck edge MUST end
# exactly here — the neckline is the raglan's neck end, not an independently
# chosen half-neck-width — or the outline does not close.
BODY_NECK_X = W - RAGLAN_RUN

# The sleeve is drafted from the SAME run and the SAME rises (see build_sleeve),
# so both raglan diagonals are congruent and the four raglan seams balance by
# construction. That congruence constrains the sleeve rather than the reverse:
# the biceps half-width must be wide enough to CONTAIN the run and still leave a
# real sleeve head, so it is solved as the larger of the anatomical biceps
# estimate and (run + head floor). A raglan sleeve is genuinely wider at the
# biceps than a set-in one for exactly this reason — the sleeve has swallowed
# the shoulder.
# The sleeve head is the OTHER side of the same split: the share of the neck
# span the body's raglan did not take. Floored for the same reason.
SLEEVE_HEAD_MIN = 22.0                         # a head narrower than this is a point
SLEEVE_HEAD_HALF = max(SLEEVE_HEAD_MIN, RAGLAN_SPAN * neck_share)
HEAD_CLAMPED = (RAGLAN_SPAN * neck_share) < SLEEVE_HEAD_MIN
# The biceps must CONTAIN the run and still leave that head, so it is solved as
# run + head — and a raglan sleeve is genuinely wider at the biceps than a
# set-in one for exactly this reason: the sleeve has swallowed the shoulder.
_bicep_anatomical = max(70.0, W * 0.62)
SLEEVE_BICEP_HALF = max(_bicep_anatomical, RAGLAN_RUN + SLEEVE_HEAD_HALF)
SLEEVE_RUN_SOLVED = RAGLAN_RUN                      # congruent with the body's
BICEP_WIDENED = SLEEVE_BICEP_HALF > _bicep_anatomical


def _raglan_edge(name, rise, run, x_out, y_bot, to_neck=True):
    """One raglan seam edge: the straight diagonal that defines the garment.

    Drawn from the underarm point (x_out, y_bot) up and in to the neck point
    (x_out - run, y_bot + rise) when `to_neck`, or the reverse. Straight, not
    curved: a straight line is what a paired full-fashioned decrease produces,
    and matching straight lines on body and sleeve balance exactly.
    """
    a = fc.P(x_out, y_bot)
    b = fc.P(x_out - run, y_bot + rise)
    return fc.Edge(name, [fc.Line(a, b)] if to_neck else [fc.Line(b, a)])


def _fashion_ladder(label, x_out, y_bot, rise, run, inward):
    """The full-fashioned decrease ladder along a raglan line.

    Marks one paired-decrease tick every `fashion_rows` of rise, set
    `fashion_step` in from the seam line — the shaping a knitter works, drawn
    on the pattern rather than merely implied by the diagonal. `inward` is +1
    when the body interior lies to the +x side of the seam, -1 otherwise.

    The tick count is derived and therefore clamped: a tall rise with a tiny
    row gauge could otherwise ask for thousands of marks.
    """
    ticks = int(max(1.0, min(rise / max(1.0, fashion_rows), 40.0)))
    pts = []
    for i in range(ticks + 1):
        t = i / float(ticks)
        x = x_out - run * t
        y = y_bot + rise * t
        pts.append(fc.P(x + inward * fashion_step, y))
    return fc.Internal(f"{label} full-fashioned decrease ladder", pts,
                       kind="marking")


def _body_piece(name, rise, neck_drop, label):
    """A body panel (front or back), cut 1 on the centre fold.

    Four real edges and no armhole at all: centre fold, neckline, the raglan
    diagonal, the side seam, the hem. The raglan edge REPLACES both the
    shoulder and the armhole — that substitution is the garment.
    """
    neck_top_y = NECK_Y - neck_drop
    # The neck edge lands exactly on the raglan's neck end — the neckline IS the
    # raglan's upper terminus, so the two are one solved point, not two guesses.
    neck_pt = fc.P(BODY_NECK_X, UNDERARM_Y + rise)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(BODY_NECK_X * 0.55, neck_top_y),
                   fc.P(BODY_NECK_X, neck_pt.y - max(neck_drop, 18.0) * 0.35),
                   neck_pt)],
    )
    internals = [
        _fashion_ladder(name, W, UNDERARM_Y, rise, RAGLAN_RUN, -1.0),
        fc.Internal(f"{name} chest line",
                    [fc.P(0.0, UNDERARM_Y), fc.P(W, UNDERARM_Y)], kind="marking"),
    ]
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_top_y))]),
            neck,
            # raglan: neck point back down and out to the underarm
            _raglan_edge("raglan", rise, RAGLAN_RUN, W, UNDERARM_Y, to_neck=False),
            fc.Edge("side", [fc.Line(fc.P(W, UNDERARM_Y), fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},        # hem seams onto the rib band
        notches=[fc.Notch("raglan", 0.5, "raglan match"),
                 fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.55, 60.0),
                               fc.P(W * 0.55, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve():
    """The raglan sleeve (cut 2, mirrored) — it carries the shoulder.

    Its top is not a cap: it is TWO straight raglan edges meeting at the sleeve
    head, plus a short neck edge between them that becomes part of the
    neckline. The front raglan edge is drafted from FRONT_RISE and the back one
    from BACK_RISE — the SAME clamped rises the body panels used — so all four
    raglan seams balance by construction.

    Frame: x = 0 at the sleeve centre, y = 0 at the cuff seam.
    """
    ul = max(120.0, sleeve_length - max(BACK_RISE, FRONT_RISE))  # underarm length
    # Sleeve half-widths at the underarm: the biceps. Solved from the drafted
    # girth (so negative ease flows into the sleeve too) and floored.
    bicep_half = SLEEVE_BICEP_HALF
    cuff_half = max(45.0, min(bicep_half * cuff_ratio, bicep_half - 10.0))
    # Head half-width: the sleeve's raglan run is SOLVED, not chosen. The body's
    # raglan is the hypotenuse of (RAGLAN_RUN, rise); the sleeve's must be the
    # same length over the same rise, so its run is exactly RAGLAN_RUN too — the
    # two diagonals are congruent and the seam balances by construction rather
    # than by tolerance. head_half is what remains of the biceps after that run,
    # and it is DERIVED, so it is clamped: a long run on a narrow sleeve would
    # otherwise drive it to zero or negative and invert the sleeve head into
    # valid-looking-but-wrong geometry after CCW normalization.
    head_half = SLEEVE_BICEP_HALF - RAGLAN_RUN   # == SLEEVE_HEAD_HALF or wider
    sleeve_run = SLEEVE_RUN_SOLVED                # == RAGLAN_RUN unless clamped
    y_ua = ul                                     # underarm level
    front_top = fc.P(-head_half, y_ua + FRONT_RISE)
    back_top = fc.P(head_half, y_ua + BACK_RISE)
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-cuff_half, 0.0), fc.P(cuff_half, 0.0))]),
            fc.Edge("underarm_back",
                    [fc.Line(fc.P(cuff_half, 0.0), fc.P(bicep_half, y_ua))]),
            fc.Edge("raglan_back",
                    [fc.Line(fc.P(bicep_half, y_ua), back_top)]),
            # the sleeve's share of the neckline, across the sleeve head
            fc.Edge("neck", [fc.curve_through(back_top, front_top,
                                              bulge=0.06, side=1.0)]),
            fc.Edge("raglan_front",
                    [fc.Line(front_top, fc.P(-bicep_half, y_ua))]),
            fc.Edge("underarm_front",
                    [fc.Line(fc.P(-bicep_half, y_ua), fc.P(-cuff_half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},        # hem seams onto the cuff rib
        notches=[fc.Notch("raglan_front", 0.5, "front raglan match"),
                 fc.Notch("raglan_back", 0.5, "back raglan match"),
                 fc.Notch("neck", 0.5, "sleeve head")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, y_ua * 0.85)),
        internals=[
            _fashion_ladder("sleeve front", -bicep_half, y_ua, FRONT_RISE,
                            -sleeve_run, 1.0),
            _fashion_ladder("sleeve back", bicep_half, y_ua, BACK_RISE,
                            sleeve_run, -1.0),
            fc.Internal("sleeve biceps line",
                        [fc.P(-bicep_half, y_ua), fc.P(bicep_half, y_ua)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (raglan)",
    )


def _rib(name, finished_len, finished_height, qty, label):
    """A rib band, drafted double-height and folded when sewn.

    Its length is the measured opening times a recovery ratio — sweater rib
    pulls in harder than jersey, so the ratios bite.
    """
    band_h = max(20.0, 2.0 * finished_height)
    length = max(60.0, finished_len) + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                        # length already carries 2×sa
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("raglan-knit-pullover")
    front = _body_piece("front", FRONT_RISE, front_neck_drop, "Front")
    back = _body_piece("back", BACK_RISE, BACK_NECK_DROP, "Back")
    sleeve = build_sleeve()

    names = ("front", "back", "sleeve", "neckband", "cuff", "hem_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(sleeve)

    # Measured openings drive the three ribs.
    neck_opening = (2.0 * (front.edge("neck").length(0.05)
                           + back.edge("neck").length(0.05))
                    + 2.0 * sleeve.edge("neck").length(0.05))
    hem_circ = 2.0 * (front.edge("hem").length(0.05)
                      + back.edge("hem").length(0.05))
    cuff_circ = sleeve.edge("hem").length(0.05)
    if wanted["neckband"]:
        pattern.add(_rib("neckband", neck_opening * neckband_ratio,
                         neckband_width, 1, "Neckband (rib)"))
    if wanted["cuff"]:
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, rib_height, 2,
                         "Cuff (rib)"))
    if wanted["hem_band"]:
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, rib_height, 1,
                         "Hem Band (rib)"))

    # ── Declared seams — the four raglans are the garment ────────────────────
    # Body and sleeve raglans are CONGRUENT right triangles — same rise, same
    # run — so these balance to delta ~ 0 with zero declared ease at every
    # parameter combination, including the clamped ones. No tolerance is
    # loosened to absorb a mismatch.
    if wanted["front"] and wanted["sleeve"]:
        pattern.declare_seam(("front", "raglan"), ("sleeve", "raglan_front"),
                             tol=1.0)
    if wanted["back"] and wanted["sleeve"]:
        pattern.declare_seam(("back", "raglan"), ("sleeve", "raglan_back"),
                             tol=1.0)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    if wanted["sleeve"]:
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                          # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "jersey-algodon (sweater knit)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker. Cut with the "
                 "stretch running AROUND the body — the draft is "
                 f"{abs(knit_ease):.0f} mm "
                 f"{'under' if knit_ease < 0 else 'over'} the measured chest and "
                 "relies on that recovery"},
        {"item": "rib knit (2x2, self or contrast)",
         "qty": round(total_area * 0.10 / (fabric_width * 0.80) / 10.0) * 10,
         "unit": "mm_length",
         "note": "neckband, two cuffs and hem band; ribs are drafted double "
                 "height and folded"},
        {"item": "stay tape (neckline + raglan tops)", "qty": 1200,
         "unit": "mm_length",
         "note": "knits grow; taping the neckline and the top 80 mm of each "
                 "raglan keeps the shoulder from dropping in wear"},
        {"item": "thread (woolly nylon in the looper)", "qty": 1, "unit": "spool",
         "note": "overlock or a narrow zigzag — the seams must stretch with the "
                 "cloth or they snap"},
    ]
    pattern.metadata = {
        "fc300_rank": 292,
        "family": "knitwear",
        "fabric_hint": "jersey-algodon",
        "architecture": "raglan: one diagonal seam per side replaces both the "
                        "shoulder seam and the armhole; the sleeve carries the "
                        "shoulder",
        "knit_ease_mm": round(knit_ease, 1),
        "knit_ease_note": "SIGNED and normally NEGATIVE — the draft is smaller "
                          "than the body and stretches on. Opposite sign "
                          "convention from every woven block in the commons.",
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "raglan_rise_front_mm": round(FRONT_RISE, 2),
            "raglan_rise_back_mm": round(BACK_RISE, 2),
            "raglan_run_mm": round(RAGLAN_RUN, 2),
            "sleeve_raglan_run_mm": round(SLEEVE_RUN_SOLVED, 2),
            "sleeve_bicep_half_mm": round(SLEEVE_BICEP_HALF, 2),
            "sleeve_head_half_mm": round(SLEEVE_HEAD_HALF, 2),
            "rise_floor_mm": RAGLAN_RISE_MIN,
            "rise_clamped": RISE_CLAMPED,
            "run_clamped": RUN_CLAMPED,
            "bicep_widened_for_run": BICEP_WIDENED,
            "sleeve_head_clamped": HEAD_CLAMPED,
            "neck_share": round(neck_share, 3),
            "note": "the raglan rise is DERIVED (raglan depth less the neck "
                    "drop) and can reach zero or go negative at parameter "
                    "extremes; it is floored before any geometry is built, and "
                    "the sleeve is drafted from the same clamped rises so the "
                    "four raglan seams balance by construction",
        },
        "full_fashioned": {
            "step_mm": round(fashion_step, 1),
            "rows_mm": round(fashion_rows, 1),
            "note": "the decrease ladder is marked on both the body and the "
                    "sleeve raglan lines — a straight diagonal is what paired "
                    "fashioning produces, which is why the raglan is the "
                    "knitter's architecture",
        },
        "rib_ratios": {"neck": neckband_ratio, "cuff": cuff_ratio,
                       "hem": hemband_ratio},
        "hardware": "none — a pullover raglan has no closure; that is the shape",
        "scope": "cut-and-sew branch, with the full-fashioned ladder marked; a "
                 "fully machine-knitted (Knitout) version is future work",
    }
    return pattern


result = build()
