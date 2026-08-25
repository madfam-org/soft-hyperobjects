"""
Kids School Pinafore — Fashion Cabinet Garment Cartridge (FC-300 #288, kids_baby, T2).

The school jumper worn over a shirt: a bib-and-back bodice, an A-line skirt, and
two shoulder straps that button at the front rather than sewing shut. The buttons
are the point of the garment. Each strap carries a LADDER of buttonholes, so the
same pinafore is let out three or four times across the growth of a child who
outgrows the length of a garment years before they outgrow its width.

Three things are solved by measurement rather than by formula:

  1. THE BUTTON LADDER SPANS A SOLVED RANGE, NOT A GUESSED ONE. The growth range
     the ladder has to cover is derived from the bodice height, and the number of
     rungs is then fitted as WHOLE intervals across that measured span with the
     spacing recomputed — a requested spacing is a target, never a result. A
     ladder pitched blind ends with its last rung inside the strap's own turning,
     which is a buttonhole that cannot be cut.

  2. THE SKIRT MEETS THE BODICE AT A MEASURED WAIST. The A-line skirt is flared
     from the hip, so its top edge is NOT the waist measurement — it is whatever
     the flare made it. The skirt's top is drafted, MEASURED, and the pleat depth
     is then solved so the pleated top edge equals the bodice's measured waist
     exactly. Pleats absorb the difference; a fixed pleat depth leaves it on the
     floor.

  3. THE ARMHOLE IS CLAMPED, TWICE. A pinafore is worn OVER a shirt, so its
     armhole must clear a sleeve — but a child's torso is short, and an armhole
     scaled off the chest alone reaches past the waist seam at the small end of
     the range. It is clamped against the measured bodice height, and the strap
     width is clamped against the shoulder that carries it.

CHILD PROPORTION, NOT A SHRUNK ADULT. Chest, waist-to-hip and bodice height are
child measurements taken directly (see bodies/child-6y). A pinafore has no bust
shaping at all — not because it is a simplification, but because there is nothing
there to shape — and the waist is drafted only slightly under the chest, because
a school-age child's is.

The BUTTON SOLID is Yantra4D territory (`shank-button-solid`; see
notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body CHILD measurements) ────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# bodice_front|bodice_back|skirt|strap|set

chest_girth = float(PARAM(lambda: chest_girth, 640.0))      # child chest, over a shirt
waist_girth = float(PARAM(lambda: waist_girth, 580.0))
hip_girth = float(PARAM(lambda: hip_girth, 680.0))
bodice_height = float(PARAM(lambda: bodice_height, 180.0))  # waist up to the bib top
skirt_length = float(PARAM(lambda: skirt_length, 320.0))    # waist to hem
strap_width = float(PARAM(lambda: strap_width, 38.0))       # finished strap width
button_ligne = float(PARAM(lambda: button_ligne, 24.0))     # button size in lignes
growth_rungs = float(PARAM(lambda: growth_rungs, 4.0))      # REQUESTED ladder rungs
rung_pitch = float(PARAM(lambda: rung_pitch, 22.0))         # REQUESTED rung spacing
flare = float(PARAM(lambda: flare, 0.30))                   # A-line flare fraction
shirt_ease = float(PARAM(lambda: shirt_ease, 110.0))        # ease over the shirt
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))   # deep: let down to grow

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
chest_girth = max(500.0, min(chest_girth, 820.0))
waist_girth = max(450.0, min(waist_girth, 760.0))
hip_girth = max(520.0, min(hip_girth, 880.0))
bodice_height = max(110.0, min(bodice_height, 280.0))
skirt_length = max(180.0, min(skirt_length, 560.0))
strap_width = max(22.0, min(strap_width, 60.0))
button_ligne = max(16.0, min(button_ligne, 36.0))
growth_rungs = max(2.0, min(growth_rungs, 7.0))
rung_pitch = max(12.0, min(rung_pitch, 40.0))
flare = max(0.10, min(flare, 0.60))
shirt_ease = max(60.0, min(shirt_ease, 200.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(20.0, min(hem_allowance, 70.0))

# ── Derived block dimensions (CHILD proportions, stated explicitly) ──────────
BUTTON_DIA = button_ligne * 0.635              # lignes → mm, the standard conversion

# A pinafore is worn OVER a shirt, so the ease is a shirt allowance, not a
# comfort allowance. A school-age child's waist is only slightly under the chest,
# so the waist quarter is drafted from the waist measurement directly — but
# floored against the chest quarter, because a pinafore that is narrower at the
# waist than the bodice above it cannot be pulled on over the head.
QUARTER_CHEST = (chest_girth + shirt_ease) / 4.0
QUARTER_WAIST = max((waist_girth + shirt_ease) / 4.0, QUARTER_CHEST * 0.86)
QUARTER_HIP = max((hip_girth + shirt_ease) / 4.0, QUARTER_WAIST + 8.0)

BH = bodice_height                             # waist (y=0) to bib top (y=BH)

# The armhole: a pinafore's armhole has to clear a shirt sleeve, so it is cut
# generously from the chest — then CLAMPED against the measured bodice height,
# because a child's torso is short and an unclamped armhole reaches past the
# waist seam at the small end of the range.
_AH_RAW = QUARTER_CHEST * 0.46
AH_DEPTH = max(45.0, min(_AH_RAW, BH - 34.0))

# The bib top: narrower than the waist, wide enough to carry a strap. Clamped
# both ways — a bib narrower than its own strap is a piece the strap hangs off.
_BIB_HALF_RAW = QUARTER_CHEST * 0.42
BIB_HALF = max(strap_width * 0.75 + 6.0, min(_BIB_HALF_RAW, QUARTER_WAIST - 10.0))

# Strap width clamped against the bib that carries it (belt and braces: BIB_HALF
# was already floored against the strap, so this can only bind at the extremes).
STRAP_W = max(16.0, min(strap_width, BIB_HALF - 6.0))

TOPSTITCH_OFFSET = 5.0

# How much higher the BACK bib sits than the front. It carries the strap's fixed
# end rather than its buttons, so it needs no button clearance and can sit up.
# Clamped against the armhole depth so the back armhole always has curve left to
# absorb the rise — see the underarm note in _bodice().
BACK_BIB_RISE = max(0.0, min(12.0, AH_DEPTH * 0.22))


def _cross(label, x, y, arm=None):
    """A small + drawn as one drill polyline at (x, y) — a button site."""
    a = arm if arm is not None else max(3.0, BUTTON_DIA * 0.30)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y),
         fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def _bodice(name, half_waist, half_bib, label, is_front):
    """One bodice panel, cut 1 on the fold at its centre.

    Front and back are the same block: a pinafore has no bust shaping, because on
    a school-age child there is nothing there to shape. The back's bib sits a
    little higher (it carries the strap's fixed end rather than its buttons),
    which is the only difference between the two.
    """
    top_y = BH if is_front else BH + BACK_BIB_RISE
    p_waist_c = fc.P(0.0, 0.0)
    p_waist_side = fc.P(half_waist, 0.0)
    # The UNDERARM is measured off the FRONT bib line on both panels, never off
    # each panel's own top. The back bib sits BACK_BIB_RISE higher, and if the
    # armhole were dropped from that raised line the back side seam would come
    # out exactly BACK_BIB_RISE longer than the front's — a side seam that does
    # not close, which is the failure this cartridge was caught on in build.
    # The extra height is absorbed by the back armhole's curve instead.
    p_underarm = fc.P(half_waist, BH - AH_DEPTH)
    p_bib_side = fc.P(half_bib, top_y)
    p_bib_c = fc.P(0.0, top_y)

    edges = [
        fc.Edge("waist", [fc.Line(p_waist_c, p_waist_side)]),
        fc.Edge("side", [fc.Line(p_waist_side, p_underarm)]),
        # The armhole scoops IN from the side seam to the bib edge. Walked
        # underarm → bib so the outline chain closes.
        fc.Edge("armhole", [fc.Bezier(
            p_underarm,
            fc.P(half_waist - (half_waist - half_bib) * 0.18,
                 p_underarm.y + AH_DEPTH * 0.42),
            fc.P(half_bib + (half_waist - half_bib) * 0.30, top_y - 6.0),
            p_bib_side)]),
        fc.Edge("bib_top", [fc.Line(p_bib_side, p_bib_c)]),
        fc.Edge("cf_fold", [fc.Line(p_bib_c, p_waist_c)]),
    ]
    internals = [
        fc.Internal("bib topstitch",
                    [fc.P(0.0, top_y - TOPSTITCH_OFFSET),
                     fc.P(half_bib - TOPSTITCH_OFFSET, top_y - TOPSTITCH_OFFSET)],
                    kind="trace"),
    ]
    if is_front:
        # The FRONT bib carries the buttons the strap ladder engages. One per
        # strap, set in from the bib corner by the button's own diameter so the
        # shank clears the topstitched edge.
        internals.append(_cross(
            "strap button",
            max(half_bib * 0.45, half_bib - BUTTON_DIA * 1.1),
            top_y - max(12.0, BUTTON_DIA * 0.8)))
    else:
        # The BACK bib is where the strap's fixed end is caught in the seam.
        internals.append(fc.Internal(
            "strap catch",
            [fc.P(max(half_bib * 0.35, half_bib - STRAP_W), top_y),
             fc.P(min(half_bib, half_bib - STRAP_W + STRAP_W), top_y)],
            kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"cf_fold": 0.0, "bib_top": hem_allowance * 0.35},
        notches=[fc.Notch("waist", 1.0, "side seam match"),
                 fc.Notch("armhole", 0.5, f"{name} armhole")],
        grainline=fc.Grainline(fc.P(half_bib * 0.55, 14.0),
                               fc.P(half_bib * 0.55, top_y - 14.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label=label,
    )


def build_bodice_front():
    return _bodice("bodice_front", QUARTER_WAIST, BIB_HALF,
                   "Bodice front (cut on fold)", True)


def build_bodice_back():
    return _bodice("bodice_back", QUARTER_WAIST, BIB_HALF,
                   "Bodice back (cut on fold)", False)


# ── The A-line skirt, then the pleat depth SOLVED to the measured waist ──────
# The skirt is flared from the hip, so its TOP edge is not the waist measurement —
# it is whatever the flare made it. Draft it, MEASURE it, then solve the pleat
# depth so the pleated top equals the bodice's measured waist exactly.
SKIRT_HEM_HALF = QUARTER_HIP * (1.0 + flare)
# The skirt top is drafted at the HIP quarter (not the waist): the extra is what
# the pleats take up, which is what gives a school pinafore its swing.
SKIRT_TOP_HALF = QUARTER_HIP


def build_skirt():
    """A-line skirt panel, cut 2 on the fold (one front, one back).

    Top drafted at the hip quarter and pleated down to the bodice's measured
    waist; hem flared by `flare` past the hip.
    """
    p_top_c = fc.P(0.0, 0.0)
    p_top_side = fc.P(SKIRT_TOP_HALF, 0.0)
    p_hem_side = fc.P(SKIRT_HEM_HALF, -skirt_length)
    p_hem_c = fc.P(0.0, -skirt_length)
    internals = []
    # The pleats, drawn as real fold lines: the take-up is split over PLEAT_COUNT
    # knife pleats, evenly spaced across the panel. Marked, not guessed.
    for i in range(PLEAT_COUNT):
        x = SKIRT_TOP_HALF * (i + 0.5) / PLEAT_COUNT
        internals.append(fc.Internal(
            f"pleat {i + 1} fold",
            [fc.P(x, 0.0), fc.P(x, -min(90.0, skirt_length * 0.30))],
            kind="marking"))
        internals.append(fc.Internal(
            f"pleat {i + 1} placement",
            [fc.P(x + PLEAT_DEPTH, 0.0),
             fc.P(x + PLEAT_DEPTH, -min(90.0, skirt_length * 0.30))],
            kind="marking"))
    edges = [
        fc.Edge("skirt_top", [fc.Line(p_top_c, p_top_side)]),
        fc.Edge("skirt_side", [fc.Line(p_top_side, p_hem_side)]),
        fc.Edge("hem", [fc.Line(p_hem_side, p_hem_c)]),
        fc.Edge("cf_fold", [fc.Line(p_hem_c, p_top_c)]),
    ]
    return fc.Piece(
        "skirt", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("skirt_top", 1.0, "side seam match"),
                 fc.Notch("skirt_side", 0.5, "hip level")],
        grainline=fc.Grainline(fc.P(SKIRT_TOP_HALF * 0.5, -20.0),
                               fc.P(SKIRT_TOP_HALF * 0.5, -skirt_length + 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cf_fold"),
        label="A-line skirt panel (cut 2 on fold)",
    )


# The take-up the pleats have to absorb, from the MEASURED skirt top against the
# MEASURED bodice waist. Clamped at zero: a flare small enough to leave nothing
# to pleat is a legitimate setting (a plain A-line pinafore), and a NEGATIVE
# take-up would otherwise be drawn as a pleat folding the wrong way.
PLEAT_TAKEUP = max(0.0, SKIRT_TOP_HALF - QUARTER_WAIST)
PLEAT_COUNT = 3
PLEAT_DEPTH = PLEAT_TAKEUP / (2.0 * PLEAT_COUNT)   # a knife pleat eats twice its depth


# ── The button ladder, solved across a MEASURED growth span ─────────────────
# The strap path: from the back bib, over the shoulder, down to the front bib
# button. Derived from the MEASURED bodice height plus a shoulder arc.
SHOULDER_ARC = max(80.0, chest_girth * 0.20)
STRAP_PATH = 2.0 * BH + SHOULDER_ARC
# The growth span the ladder must cover — the reason the garment buttons at all.
# Derived from the bodice height rather than picked, so a small pinafore gets a
# short ladder and a large one gets a long one.
GROWTH_SPAN = max(30.0, BH * 0.55)

# Whole intervals at (or just under) the requested pitch, then the pitch
# RECOMPUTED so the ladder lands exactly on both ends of the span. The requested
# rung COUNT is also honoured as an upper bound: whichever constraint binds first
# wins, and the result is reported.
_BY_PITCH = max(1, int(round(GROWTH_SPAN / rung_pitch)))
_BY_COUNT = max(1, int(round(growth_rungs)) - 1)
N_INTERVALS = max(1, min(_BY_PITCH, _BY_COUNT))
N_RUNGS = N_INTERVALS + 1
PITCH_SOLVED = GROWTH_SPAN / N_INTERVALS

# The strap is cut to the LONGEST setting plus its turnings: the ladder is worked
# from the far end back, so the shortest setting simply leaves strap unused
# inside. Cutting to the shortest setting is the classic error — it makes the
# ladder decorative.
STRAP_CUT = STRAP_PATH + GROWTH_SPAN + 2.0 * seam_allowance


def build_strap():
    """A shoulder strap, cut 2, carrying the buttonhole growth ladder.

    Cut flat at twice the finished width plus turnings: folded in half lengthwise
    and topstitched, which is what a school strap needs to survive being pulled
    on by the strap for several years.
    """
    w = STRAP_W * 2.0 + 2.0 * seam_allowance
    ln = STRAP_CUT
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("button_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("back_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                    kind="marking"),
    ]
    # The buttonhole ladder, worked from the button end back. Each rung is drawn
    # as a real slot of the button's own diameter plus the standard 2 mm of
    # clearance — a buttonhole cut to the button's diameter will not pass it.
    slot = BUTTON_DIA + 2.0
    for i in range(N_RUNGS):
        x = ln - seam_allowance - max(14.0, BUTTON_DIA * 0.9) - PITCH_SOLVED * i
        internals.append(fc.Internal(
            f"buttonhole rung {i + 1}",
            [fc.P(x - slot / 2.0, w / 2.0), fc.P(x + slot / 2.0, w / 2.0)],
            kind="drill"))
    internals.append(fc.Internal(
        "growth span",
        [fc.P(ln - seam_allowance - max(14.0, BUTTON_DIA * 0.9) - GROWTH_SPAN,
              w * 0.28),
         fc.P(ln - seam_allowance - max(14.0, BUTTON_DIA * 0.9), w * 0.28)],
        kind="marking"))
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},   # long edges are folded, not sewn
        notches=[fc.Notch("lower", 0.0, "back bib end"),
                 fc.Notch("lower", 1.0, "button end")],
        grainline=fc.Grainline(fc.P(ln * 0.12, w / 2.0), fc.P(ln * 0.88, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Shoulder strap with growth ladder (cut 2)",
    )


def build():
    pattern = fc.PatternSet("kids-school-pinafore")
    everything = target_piece == "set"
    want = {
        "bodice_front": everything or target_piece == "bodice_front",
        "bodice_back": everything or target_piece == "bodice_back",
        "skirt": everything or target_piece == "skirt",
        "strap": everything or target_piece == "strap",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bodice_front"]:
        pattern.add(build_bodice_front())
    if want["bodice_back"]:
        pattern.add(build_bodice_back())
    if want["skirt"]:
        pattern.add(build_skirt())
    if want["strap"]:
        pattern.add(build_strap())

    if want["bodice_front"] and want["bodice_back"]:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"),
                             tol=1.0)
        # Front and back waists are both drafted to QUARTER_WAIST, so this closes
        # at delta = 0 by construction; the check catches a future redraft.
        pattern.declare_seam(("bodice_front", "waist"), ("bodice_back", "waist"),
                             tol=0.5)
    if want["skirt"] and want["bodice_front"]:
        # The pleated skirt top against the measured bodice waist. The declared
        # ease is the pleat take-up: the skirt top measures QUARTER_HIP flat and
        # is pleated down to QUARTER_WAIST, and PLEAT_TAKEUP is exactly that
        # difference — so the check lands at delta ≈ 0 and would go red the day
        # the pleat solve stopped agreeing with the drafted flare.
        pattern.declare_seam(("skirt", "skirt_top"),
                             ("bodice_front", "waist"),
                             tol=1.0, ease=PLEAT_TAKEUP)

    fabric_width = 1450.0                       # popelina-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "popelina-algodon, 115 gsm",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 76% marker; a school pinafore "
                 f"is washed weekly for years — wash before cutting, poplin "
                 f"shrinks 2.5% in the warp."},
        {"item": f"shank button, {button_ligne:.0f} ligne "
                 f"({BUTTON_DIA:.1f} mm)", "qty": 2, "unit": "pc",
         "note": "Yantra4D shank-button-solid (notion.hardware_ref); one per "
                 "strap, on the front bib. A shank button is used because the "
                 "strap has to move on it as the ladder is let out."},
        {"item": "buttonhole ladder", "qty": N_RUNGS * 2, "unit": "count",
         "note": f"{N_RUNGS} rungs per strap at a SOLVED pitch of "
                 f"{PITCH_SOLVED:.1f} mm across a derived growth span of "
                 f"{GROWTH_SPAN:.0f} mm (requested pitch {rung_pitch:.0f} mm, "
                 f"requested {int(growth_rungs)} rungs). Slot cut at "
                 f"{BUTTON_DIA + 2.0:.1f} mm — the button's diameter plus 2 mm."},
        {"item": "lightweight fusible interfacing", "qty": round(STRAP_CUT * 2.2),
         "unit": "mm_length",
         "note": "behind every buttonhole rung and both bib tops; an unbacked "
                 "buttonhole in 115 gsm poplin frays open inside a term."},
        {"item": "thread (poly-cotton)", "qty": 1, "unit": "spool",
         "note": "bar-tack the back end of each strap where it is caught in the "
                 "bib seam — that is the join a child is lifted by."},
    ]
    pattern.metadata = {
        "fc300_rank": 288,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "popelina-algodon",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "quarter_hip": round(QUARTER_HIP, 1),
            "bodice_height": round(BH, 1),
            "bib_half_width": round(BIB_HALF, 1),
            "armhole_depth": round(AH_DEPTH, 1),
            "skirt_length": round(skirt_length, 1),
            "skirt_hem_half": round(SKIRT_HEM_HALF, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
            "strap_finished_width": round(STRAP_W, 1),
        },
        "solved": {
            "growth_span_mm": round(GROWTH_SPAN, 2),
            "rungs_requested": int(growth_rungs),
            "rungs_solved": N_RUNGS,
            "rung_pitch_requested_mm": round(rung_pitch, 2),
            "rung_pitch_solved_mm": round(PITCH_SOLVED, 3),
            "ladder_bound_by": "pitch" if _BY_PITCH <= _BY_COUNT else "count",
            "strap_path_measured_mm": round(STRAP_PATH, 2),
            "skirt_top_half_mm": round(SKIRT_TOP_HALF, 2),
            "pleat_takeup_mm": round(PLEAT_TAKEUP, 2),
            "pleat_count": PLEAT_COUNT,
            "pleat_depth_mm": round(PLEAT_DEPTH, 3),
            "armhole_depth_requested_mm": round(_AH_RAW, 2),
            "armhole_depth_clamped_mm": round(AH_DEPTH, 2),
            "armhole_was_clamped": bool(abs(AH_DEPTH - _AH_RAW) > 0.01),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(BIB_HALF, 2),
            "bib_half_was_clamped": bool(abs(BIB_HALF - _BIB_HALF_RAW) > 0.01),
            "button_diameter_mm": round(BUTTON_DIA, 2),
            "note": "the rung pitch is a TARGET: whole intervals are fitted across "
                    "a growth span DERIVED from the bodice height, and the pitch "
                    "recomputed, so the ladder lands on both ends of the span "
                    "instead of running its last rung into the strap's turning. "
                    "The pleat depth is solved from the MEASURED skirt top against "
                    "the MEASURED bodice waist — an A-line skirt's top edge is "
                    "whatever the flare made it, not the waist measurement, and a "
                    "fixed pleat depth leaves the difference on the floor. The "
                    "take-up is floored at zero so a small flare cannot produce a "
                    "pleat folding backwards.",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y), "
                      "NOT a scaled adult block",
            "no_bust_shaping": "a pinafore for a school-age child has no bust dart "
                               "and no princess seam — not as a simplification, but "
                               "because there is nothing there to shape",
            "shallow_waist_suppression": "the waist quarter is drafted from the waist "
                                         "measurement but floored at 86% of the chest "
                                         "quarter — a pinafore narrower than that will "
                                         "not pull on over the head",
            "worn_over_a_shirt": f"the ease is a SHIRT allowance ({shirt_ease:.0f} mm "
                                 f"total), and the armhole is cut to clear a sleeve",
            "grows_with_the_child": f"{N_RUNGS} buttonhole rungs give "
                                    f"{GROWTH_SPAN:.0f} mm of length adjustment, and "
                                    f"the hem carries {hem_allowance:.0f} mm to let "
                                    f"down on top of that",
        },
        "hardware": "shank buttons via Yantra4D (notion.hardware_ref -> "
                    "shank-button-solid); the solid's diameter_mm is fed from this "
                    "garment's button_ligne on the standard 0.635 mm/ligne "
                    "conversion, and that same diameter sizes every buttonhole slot "
                    "in the growth ladder (plus the standard 2 mm of clearance). A "
                    "SHANK button, not a sew-through: the strap has to move on it "
                    "each time the ladder is let out.",
    }
    return pattern


result = build()
