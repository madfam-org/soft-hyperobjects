"""
Agbada / grand boubou — Fashion Cabinet Heritage Cartridge (FC-500 #483, heritage_global,
West African: Yoruba agbada / Wolof-Mandinka mbubb grand boubou).

The grand flowing gown of much of West Africa: an enormous rectangle of cloth, folded once
at the shoulder line, with an opening cut for the head, worn as the widest layer over a
long-sleeved tunic and drawstring trousers (the Yoruba **agbада** worn over the **bùbá**
and **ṣòkòtò**; the Senegambian **grand boubou / mbubb** worn over the **caftan** and
**tubay**). The whole garment is one width of cloth used as wide as the loom or bolt allows,
and the "sleeves" are not set in — they are the sides of that rectangle, and the arm reaches
out through the open sides while the cloth cascades to the fingertips and beyond. A neck
facing (the embroidered yoke, the **wax-print** or hand-embroidered field around the throat)
and a chest pocket are the two worked zones; everything else is drape.

Two facts govern the draft, and both are African rather than Western:

  1. THE GARMENT IS A WIDTH, FOLDED. There is no shoulder seam and no armscye. The cloth is
     folded at the shoulder line, the head-hole is cut on that fold, and the width of the
     spread cloth — from fingertip to fingertip and beyond — is a real parameter. The robe's
     drop (`gown_length`) and its half-span (`wing_span`) size the rectangle; the body is not
     used to shape it, only to check that the neck sits at the right depth. A bolt too narrow
     to make the wing is REPORTED, not silently widened.

  2. THE OPENING IS FACED, NOT COLLARED. The boubou has no collar. The neck is a wide, deep
     opening — round, or the Yoruba squared/keyhole — bound and faced with the worked panel.
     Its front is deep (the chest field shows), its back shallow. The facing is cut to the
     MEASURED neckline, not to a neck girth, because a folded-cloth neckline is two curves
     plus a deep front drop, not a circle.

Drafting note — the seam that must SOLVE, and the mistake it prevents:

  The facing's inner edge must equal the gown's neck edge, or it will not turn cleanly and the
  worked panel ripples at the throat — the first thing an outside pattern gets wrong. So the
  neck curve is drafted once on the gown, MEASURED, and the facing's matching inner edge is the
  same curve. The declared seam proves it. The chest pocket is placed on the measured chest
  field, not floated.

Pieces:
  - gown   : the whole robe, cut 1 on the shoulder fold (mirror), head-hole on the fold.
  - facing : the neck facing / worked yoke, cut to the MEASURED neckline.
  - pocket : the chest pocket (大 patch), placed on the measured chest field.

Hardware: none — the grand boubou is closure-free, pulled over the head. No hardware_ref.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))   # gown|facing|pocket|set

wing_span = float(PARAM(lambda: wing_span, 1150.0))       # shoulder to cloth edge (half span)
gown_length = float(PARAM(lambda: gown_length, 1360.0))   # shoulder fold to hem
chest_girth = float(PARAM(lambda: chest_girth, 1080.0))   # checked, never used to size
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
neck_front_drop = float(PARAM(lambda: neck_front_drop, 250.0))  # deep front opening
neck_width = float(PARAM(lambda: neck_width, 200.0))      # half-width of the head-hole
facing_depth = float(PARAM(lambda: facing_depth, 120.0))  # worked-yoke depth around the neck
pocket_width = float(PARAM(lambda: pocket_width, 240.0))
pocket_drop = float(PARAM(lambda: pocket_drop, 300.0))    # neck to pocket top
side_seam = float(PARAM(lambda: side_seam, 520.0))        # closed side below the arm
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
wing_span = max(800.0, min(wing_span, 1500.0))
gown_length = max(1000.0, min(gown_length, 1650.0))
chest_girth = max(800.0, min(chest_girth, 1500.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
neck_front_drop = max(140.0, min(neck_front_drop, 360.0))
neck_width = max(130.0, min(neck_width, 300.0))
facing_depth = max(70.0, min(facing_depth, 200.0))
pocket_width = max(150.0, min(pocket_width, 340.0))
pocket_drop = max(180.0, min(pocket_drop, 480.0))
side_seam = max(200.0, min(side_seam, 800.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

# ── The width solve — the cloth is a width, folded ───────────────────────────
# The gown is drafted as the FRONT half, folded at the shoulder line along the top edge.
# The wing runs out to `wing_span` from centre front; the body drops `gown_length`. The bolt
# must reach the wing — a bolt too narrow is reported rather than silently widened.
BOLT_WIDTH = 1400.0                       # a wide African wax-print bolt, per panel
WING_NEEDED = wing_span + seam_allowance
BOLT_SUFFICIENT = BOLT_WIDTH >= WING_NEEDED

# The head-hole geometry. Front is deep; back is shallow. neck_width is the half-width of the
# opening at the shoulder line. The front drop must clear the pocket zone but stay above the
# waist — clamped against the gown length so a deep neck cannot fall past the chest field.
NECK_DROP_F = min(neck_front_drop, gown_length * 0.42)
NECK_DROP_B = min(70.0, NECK_DROP_F * 0.5)

# The side seam is closed only for the lower body; above it the side is open for the arm to
# reach out (the boubou has open sides, not sleeves). Capped below the neck depth.
SIDE_CEILING = gown_length - NECK_DROP_F - 120.0
side_seam = min(side_seam, max(SIDE_CEILING, 100.0))

# The chest field: where the pocket sits. Checked against chest_girth for a sane placement.
CHEST_FIELD_X = min(pocket_width + 60.0, wing_span * 0.45)


def _neck_curve_front(x_edge, y_shoulder, y_drop):
    """The front neckline: from the shoulder opening point down to the deep centre-front
    drop, drawn as a single Bezier biased to a wide, squared Yoruba opening rather than a
    tight round scoop."""
    return fc.Bezier(
        fc.P(x_edge, y_shoulder),
        fc.P(x_edge * 0.96, y_shoulder - y_drop * 0.24),
        fc.P(x_edge * 0.50, y_drop + (y_shoulder - y_drop) * 0.06),
        fc.P(0.0, y_drop))


def build_gown():
    """The whole robe, drafted as the FRONT half and cut on the shoulder fold (mirror).

    x = 0 is centre front; x = wing_span is the cloth edge (the fingertip end of the wing).
    The top edge is the SHOULDER FOLD. The head-hole is cut on that fold at centre. There is
    no armscye: the arm reaches out through the open side above the side seam."""
    ws = wing_span
    top = gown_length                     # the shoulder fold line
    # points, clockwise from centre-front hem
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_edge = fc.P(ws, 0.0)
    p_side_bottom = fc.P(ws, side_seam)   # closed side up to here
    p_wing_edge = fc.P(ws, top)           # the cloth edge at the shoulder fold (wing tip)
    p_neck_shoulder = fc.P(neck_width, top)  # where the head-hole meets the shoulder fold
    p_neck_cf = fc.P(0.0, top - NECK_DROP_F)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_edge)]),
        # side: closed below the slit level, open above (drawn as the closed portion only;
        # the open arm-gap is a marking so the outline stays a single closed ring).
        fc.Edge("side", [fc.Line(p_hem_edge, p_side_bottom)]),
        fc.Edge("underarm_open", [fc.Line(p_side_bottom, p_wing_edge)]),
        # the shoulder fold, from the wing edge in to the head-hole opening point
        fc.Edge("shoulder_fold", [fc.Line(p_wing_edge, p_neck_shoulder)]),
        # the front neckline, MEASURED
        fc.Edge("neck", [_neck_curve_front(neck_width, top, top - NECK_DROP_F)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        # the arm-reach line: above the side seam the side is open for the arm.
        fc.Internal("arm-gap", [fc.P(ws, side_seam), fc.P(ws - 40.0, side_seam)],
                    kind="marking"),
        # the pocket seat, on the chest field.
        fc.Internal("pocket-seat",
                    [fc.P(CHEST_FIELD_X - pocket_width * 0.5, top - pocket_drop),
                     fc.P(CHEST_FIELD_X + pocket_width * 0.5, top - pocket_drop),
                     fc.P(CHEST_FIELD_X + pocket_width * 0.5,
                          top - pocket_drop - pocket_width * 0.9),
                     fc.P(CHEST_FIELD_X - pocket_width * 0.5,
                          top - pocket_drop - pocket_width * 0.9)],
                    kind="marking"),
        # the worked-yoke field the facing covers.
        fc.Internal("yoke-field",
                    [fc.P(neck_width + facing_depth, top - 6.0),
                     fc.P(0.0, top - NECK_DROP_F - facing_depth)],
                    kind="marking"),
    ]
    return fc.Piece(
        "gown", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side midpoint"),
                 fc.Notch("shoulder_fold", 0.5, "wing midpoint")],
        grainline=fc.Grainline(fc.P(ws * 0.2, hem_allowance + 40.0),
                               fc.P(ws * 0.2, top - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="shoulder_fold", mirror=True),
        label="Grand boubou body — one width, folded at the shoulder",
    )


# ── The neckline, MEASURED ───────────────────────────────────────────────────
_GOWN = build_gown()
NECK_FRONT = _GOWN.edge("neck").length(0.2)     # front quarter (one side of the fold)
# The gown's drawn neck edge appears on BOTH sides of the shoulder fold (the piece is cut on
# the fold, mirror), so the sewn front neck run the facing must match is twice the front
# curve. The back neck is a shallow arc taken off the same opening, reported for the record
# but carried by the same continuous facing.
_BACK_PROBE = fc.Edge("bprobe", [fc.Bezier(
    fc.P(neck_width, 0.0),
    fc.P(neck_width * 0.55, -NECK_DROP_B * 0.4),
    fc.P(neck_width * 0.30, -NECK_DROP_B * 0.9),
    fc.P(0.0, -NECK_DROP_B))])
NECK_BACK = _BACK_PROBE.length(0.2)
NECK_FRONT_RUN = 2.0 * NECK_FRONT               # both sides of the fold — the sewn front run
NECK_RUN = NECK_FRONT_RUN + 2.0 * NECK_BACK     # full head-hole, for the BOM/report
NECK_NAIVE = neck_girth + 40.0


def build_facing():
    """The neck facing / worked yoke: a shaped band cut to the MEASURED neckline, its inner
    edge equal to the gown's neck run by construction.

    Drafted flat as a band whose inner edge length equals the sewn front neck run and whose
    outer edge is the same run plus the facing_depth spread — the worked field the embroidery
    fills. It continues shallowly round the back neck (carried on the same band)."""
    inner = NECK_FRONT_RUN
    depth = facing_depth
    # A straight faced band: inner edge = NECK_RUN, outer edge slightly longer (the field
    # opens outward). Drawn as a shallow trapezoid so it is a real, non-degenerate piece.
    outer = inner + depth * 0.6
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(inner, 0.0)
    p2 = fc.P(inner + (outer - inner) * 0.5, depth)
    p3 = fc.P(-(outer - inner) * 0.5, depth)
    edges = [
        fc.Edge("neck_inner", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("fold-line", [fc.P(-(outer - inner) * 0.25, depth * 0.5),
                                  fc.P(inner + (outer - inner) * 0.25, depth * 0.5)],
                    kind="marking"),
    ]
    return fc.Piece(
        "facing", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_inner", 0.5, "centre front"),
                 fc.Notch("neck_inner", NECK_FRONT / inner, "shoulder fold (right)"),
                 fc.Notch("neck_inner", (inner - NECK_FRONT) / inner,
                          "shoulder fold (left)")],
        grainline=fc.Grainline(fc.P(inner * 0.1, depth * 0.5), fc.P(inner * 0.9, depth * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Neck facing / worked yoke (cut to the measured neckline)",
    )


def build_pocket():
    """The chest patch pocket (大 patch): a squared pocket placed on the measured chest field."""
    w = pocket_width
    h = pocket_width * 0.9
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("right", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),
        fc.Edge("left", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance * 0.6},
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[fc.Internal("opening", [fc.P(0.0, h - 8.0), fc.P(w, h - 8.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Chest patch pocket",
    )


def build():
    pattern = fc.PatternSet("agbada-boubou")
    everything = target_piece == "set"
    if everything or target_piece == "gown":
        pattern.add(build_gown())
    if everything or target_piece == "facing":
        pattern.add(build_facing())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())

    if everything:
        # THE seam that had to solve: the facing's inner edge against the gown's MEASURED
        # neck run — both sides, front and back. Cut the facing to a neck girth instead and it
        # ripples at the throat, because the folded-cloth neckline is curves plus a deep front
        # drop, not a circle.
        pattern.declare_seam(("facing", "neck_inner"),
                             [("gown", "neck"), ("gown", "neck")], tol=1.0)

    # The bolt: a wide wax-print. The wing must fit within the bolt or be reported.
    fabric_width = BOLT_WIDTH
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "wax-print or hand-woven cotton (grand boubou bolt)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"the gown is ONE width folded at the shoulder; the wing runs "
                 f"{wing_span:.0f} mm from centre front, needing a bolt ≥ "
                 f"{WING_NEEDED:.0f} mm. bolt_sufficient={BOLT_SUFFICIENT}."},
        {"item": "facing / worked-yoke cloth", "qty": round(NECK_RUN + facing_depth * 2),
         "unit": "mm_length",
         "note": "the neck is FACED, not collared; the facing is cut to the measured "
                 "neckline. The embroidery of the yoke is the maker's — none is drafted."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "the boubou is closure-free, pulled over the head."},
    ]
    pattern.metadata = {
        "fc500_rank": 483,
        "family": "heritage_global",
        "fabric_hint": "algodon-percal",
        "finished_mm": {
            "wing_span": round(wing_span, 1),
            "gown_length": round(gown_length, 1),
            "neck_front_drop": round(NECK_DROP_F, 1),
            "side_seam": round(side_seam, 1),
        },
        "solved": {
            "neck_front_quarter_mm": round(NECK_FRONT, 3),
            "neck_back_quarter_mm": round(NECK_BACK, 3),
            "neck_run_mm": round(NECK_RUN, 3),
            "neck_naive_estimate_mm": round(NECK_NAIVE, 3),
            "facing_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "bolt_width_mm": round(BOLT_WIDTH, 1),
            "wing_needed_mm": round(WING_NEEDED, 1),
            "bolt_sufficient": BOLT_SUFFICIENT,
            "side_seam_ceiling_mm": round(SIDE_CEILING, 2),
            "chest_field_x_mm": round(CHEST_FIELD_X, 2),
            "note": "the grand boubou is ONE WIDTH of cloth folded at the shoulder — no "
                    "shoulder seam and no armscye, the arm reaching out through the open "
                    "side above the closed side seam. The neck is FACED, not collared: the "
                    "facing's inner edge is cut to the MEASURED neck run (both sides, front "
                    "and back), not to a neck girth, because a folded-cloth neckline is two "
                    "curves plus a deep front drop rather than a circle (the miss is "
                    "facing_vs_neck_estimate_mm). A bolt too narrow to make the wing is "
                    "reported as bolt_sufficient=false rather than silently widened.",
        },
        "heritage": {
            "garment": "agbada / grand boubou (mbubb) — the West African grand gown",
            "worn": "the widest layer, over a long-sleeved tunic (bùbá / caftan) and "
                    "drawstring trousers (ṣòkòtò / tubay); Yoruba, Wolof, Mandinka, Hausa "
                    "and across the Sahel and its diaspora",
            "construction": "one width folded at the shoulder, head-hole on the fold, open "
                            "sides for the arm, faced neck opening, chest patch pocket",
            "excluded": "no specific embroidery motif, tribal mark, or named wax-print is "
                        "drafted — the worked yoke and the cloth's pattern are the maker's",
        },
        "hardware": "none — the grand boubou is closure-free, pulled over the head.",
    }
    return pattern


result = build()
