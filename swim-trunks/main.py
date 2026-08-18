"""
Swim Trunks — FC-100 rank #53. Fashion Cabinet Garment Cartridge.

Board-short-style men's swim trunks: a RELAXED outer trunk (mid-thigh, woven-
like fit even in 4-way-stretch swim tricot, so NO negative ease on the outer)
with an elastic waistband casing and an internal drawcord, worn over a MESH
BRIEF LINER. One waistband casing catches both layers; the mesh liner attaches
only at the waist and hangs free at the leg. The outer carries a curved/split
side hem (a bezier that sweeps UP at the side seam — the board-short side vent)
and a patch BACK POCKET with a drain eyelet.

Three seam-matching techniques from the commons converge here (mirroring the
running-shorts sibling, rank #52):
  • the outer BACK hem width is solved analytically so the straight outer
    inseams match exactly (rank #18 athletic-shorts idiom), and the same solve
    is applied to the mesh liner brief;
  • the mesh liner waist width is PINNED to the outer waist width so both layers
    meet the waistband at one length (waist seam delta ~ 0 by construction);
  • the liner is a BRIEF cut with mild negative ease at the hip and leg (rank
    #45 panties-bikini idiom) while its leg opening is elastic-finished with an
    exact-mm elastic cut length in the BOM. The RELAXED outer takes no negative
    ease — a swim trunk hangs like a woven short, the stretch is comfort not fit.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
# target: outer_front|outer_back|liner_front|liner_back|waistband|back_pocket|set
target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth       = float(PARAM(lambda: hip_girth, 1000.0))
outer_inseam    = float(PARAM(lambda: outer_inseam, 220.0))   # board-short inseam (mm)
liner_inseam    = float(PARAM(lambda: liner_inseam, 40.0))    # mesh brief liner (short)
front_rise      = float(PARAM(lambda: front_rise, 265.0))
back_rise       = float(PARAM(lambda: back_rise, 300.0))
sport_ease      = float(PARAM(lambda: sport_ease, 170.0))     # relaxed outer ease
outer_hem_width = float(PARAM(lambda: outer_hem_width, 285.0))  # front half-hem, flat
side_scoop      = float(PARAM(lambda: side_scoop, 45.0))      # side-hem rise (split hem)
liner_neg_ease  = float(PARAM(lambda: liner_neg_ease, 8.0))   # liner negative ease (%)
elastic_width   = float(PARAM(lambda: elastic_width, 35.0))
waist_elastic_ratio = float(PARAM(lambda: waist_elastic_ratio, 0.92))
leg_elastic_ratio   = float(PARAM(lambda: leg_elastic_ratio, 0.90))
drawcord_ratio  = float(PARAM(lambda: drawcord_ratio, 1.35))  # drawcord/waist length
pocket_width    = float(PARAM(lambda: pocket_width, 140.0))   # back patch pocket (mm)
pocket_depth    = float(PARAM(lambda: pocket_depth, 150.0))
seam_allowance  = float(PARAM(lambda: seam_allowance, 8.0))
hem_allowance   = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps (mirror the manifest slider ranges) ───────────────────────────────
hip_girth = max(650.0, min(hip_girth, 1800.0))
outer_inseam = max(120.0, min(outer_inseam, 320.0))
liner_inseam = max(20.0, min(liner_inseam, 120.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
sport_ease = max(90.0, min(sport_ease, 380.0))
outer_hem_width = max(190.0, min(outer_hem_width, 380.0))
side_scoop = max(0.0, min(side_scoop, 130.0))
liner_neg_ease = max(0.0, min(liner_neg_ease, 18.0))
elastic_width = max(20.0, min(elastic_width, 60.0))
waist_elastic_ratio = max(0.80, min(waist_elastic_ratio, 1.0))
leg_elastic_ratio = max(0.75, min(leg_elastic_ratio, 1.0))
drawcord_ratio = max(1.0, min(drawcord_ratio, 1.7))
pocket_width = max(90.0, min(pocket_width, 200.0))
pocket_depth = max(90.0, min(pocket_depth, 220.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

# ── Outer geometry (relaxed board short, NO negative ease, split side hem) ───
HIP_E = hip_girth + sport_ease
CROTCH_Y = outer_inseam
WAIST_Y = outer_inseam + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0, HIP_E / 12.0
HEM_DROP = 0.0                       # hem lowest point (at the inseam corner)
OF_WAIST_IN = FW * 0.92              # outer waist inner x (front)
OB_WAIST_IN = BW * 0.92              # outer waist inner x (back)
ELASTIC_ZONE = 8.0                   # marked elastic application width (mm)


def _outer_back_hem():
    """Solve the outer back hem half-width so the straight inseams match."""
    f_tip_x = FW + FORK_F
    b_tip_x = BW + FORK_B
    dy = CROTCH_Y - HEM_DROP
    front_len = math.hypot(f_tip_x - outer_hem_width, dy)
    run = math.sqrt(max(front_len ** 2 - dy ** 2, 25.0))
    bhw = b_tip_x - run
    if bhw < 100.0:
        raise ValueError("solved outer back hem width degenerate; widen outer_hem_width")
    return bhw


def _outer_piece(name, width, tip_x, hem_w, cb_y, waist_in, label, internals=None):
    """Relaxed outer trunk half: vertical side (scooped) + bezier curved hem."""
    edges = [
        # side/outseam: vertical, starting at the scooped hem corner (side vent)
        fc.Edge("side", [fc.Line(fc.P(0.0, side_scoop), fc.P(0.0, WAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y),
                       fc.P(width - 4.0, cb_y - front_rise * 0.45),
                       fc.P(width + (tip_x - width) * 0.35, CROTCH_Y + 40.0),
                       fc.P(tip_x, CROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_w, HEM_DROP))]),
        # curved/split hem: bezier sweeping UP from the hem corner to the side scoop
        fc.Edge(
            "hem",
            [fc.Bezier(fc.P(hem_w, HEM_DROP),
                       fc.P(hem_w * 0.55, HEM_DROP - 6.0),
                       fc.P(hem_w * 0.22, side_scoop * 0.35),
                       fc.P(0.0, side_scoop))],
        ),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(width * 0.45, WAIST_Y * 0.15),
                               fc.P(width * 0.45, WAIST_Y * 0.8)),
        internals=internals or [],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def _pocket_placement(cb_y):
    """Back-pocket placement rectangle on the outer back, below the waist."""
    top_y = cb_y - front_rise * 0.30
    cx = (FW + FORK_B) * 0.42
    half = pocket_width / 2.0
    left = max(cx - half, 20.0)
    right = cx + half
    bot_y = top_y - pocket_depth
    corners = [
        fc.P(left, top_y), fc.P(right, top_y),
        fc.P(right, bot_y), fc.P(left, bot_y),
    ]
    return fc.Internal("back pocket placement", corners + corners[:1])


def build_outer():
    bhw = _outer_back_hem()
    front = _outer_piece("outer_front", FW, FW + FORK_F, outer_hem_width, WAIST_Y,
                         OF_WAIST_IN, "Outer Front")
    back_cb_y = WAIST_Y + (back_rise - front_rise)
    back = _outer_piece("outer_back", BW, BW + FORK_B, bhw, back_cb_y,
                        OB_WAIST_IN, "Outer Back",
                        internals=[_pocket_placement(back_cb_y)])
    return front, back


# ── Mesh brief liner geometry (fitted brief, mild negative ease) ─────────────
NEG = 1.0 - liner_neg_ease / 100.0
LCROTCH_Y = liner_inseam
LWAIST_Y = liner_inseam + front_rise
LFW = (hip_girth * NEG) / 4.0 - 8.0
LBW = (hip_girth * NEG) / 4.0 + 8.0
LFORK_F, LFORK_B = (hip_girth * NEG) / 16.0, (hip_girth * NEG) / 12.0


def _liner_back_hem():
    """Solve the liner back hem half-width so the liner inseams match."""
    lf_tip_x = LFW + LFORK_F
    lb_tip_x = LBW + LFORK_B
    ldy = LCROTCH_Y
    lhem_f = LFW * 0.86
    lfront_len = math.hypot(lf_tip_x - lhem_f, ldy)
    lrun = math.sqrt(max(lfront_len ** 2 - ldy ** 2, 25.0))
    lhem_b = lb_tip_x - lrun
    if lhem_b < 55.0:
        raise ValueError("solved liner back hem width degenerate; raise liner_inseam")
    return lhem_f, lhem_b


def _elastic_zone(edge, label, t0, t1, samples=13):
    """Internal trace parallel to an elastic edge, ELASTIC_ZONE mm inside.

    Pieces here are authored CCW; the inward normal at tangent t is (-t.y, t.x).
    """
    pts = []
    for i in range(samples):
        t = t0 + (t1 - t0) * i / (samples - 1)
        p, tan = edge.point_at_fraction(t)
        pts.append(fc.P(p.x - tan.y * ELASTIC_ZONE, p.y + tan.x * ELASTIC_ZONE))
    return fc.Internal(label, pts)


def _liner_piece(name, waist_in, tip_x, hem_w, cb_y, hipw, label):
    """Mesh brief half: waist pinned to outer waist; leg opening elastic-finished."""
    hem = fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))])
    edges = [
        fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, LWAIST_Y))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, LWAIST_Y), fc.P(waist_in, cb_y))]),
        fc.Edge(
            "crotch",
            [fc.Bezier(fc.P(waist_in, cb_y),
                       fc.P(hipw - 4.0, cb_y - front_rise * 0.42),
                       fc.P(hipw + (tip_x - hipw) * 0.35, LCROTCH_Y + 30.0),
                       fc.P(tip_x, LCROTCH_Y))],
        ),
        fc.Edge("inseam", [fc.Line(fc.P(tip_x, LCROTCH_Y), fc.P(hem_w, 0.0))]),
        hem,
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0},  # leg opening is elastic-finished, not turned
        notches=[fc.Notch("side", 0.5), fc.Notch("inseam", 0.5)],
        grainline=fc.Grainline(fc.P(hipw * 0.4, LWAIST_Y * 0.2),
                               fc.P(hipw * 0.4, LWAIST_Y * 0.8)),
        internals=[_elastic_zone(hem, "leg elastic zone", 0.08, 0.92)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_liner():
    lhem_f, lhem_b = _liner_back_hem()
    front = _liner_piece("liner_front", OF_WAIST_IN, LFW + LFORK_F, lhem_f, LWAIST_Y,
                         LFW, "Mesh Liner Front (brief)")
    back = _liner_piece("liner_back", OB_WAIST_IN, LBW + LFORK_B, lhem_b,
                        LWAIST_Y + (back_rise - front_rise), LBW,
                        "Mesh Liner Back (brief)")
    return front, back


# ── Waistband (one elastic casing catching both layers + drawcord channel) ───
def build_waistband(outer_front, outer_back):
    """Fold-over casing. Bottom edge = the outer waist opening exactly, so the
    band <-> outer-waist seam balances; the elastic inside is shorter (BOM)."""
    circ = 2.0 * (outer_front.edge("waist").length() + outer_back.edge("waist").length())
    length = circ
    band_h = 2.0 * (elastic_width + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)]),
            fc.Internal("drawcord channel",
                        [fc.P(length * 0.30, band_h * 0.30), fc.P(length * 0.70, band_h * 0.30)]),
            # two center-front eyelet drill crosses where the drawcord exits
            fc.Internal("cf eyelet L-h",
                        [fc.P(length * 0.47, band_h * 0.30 - 4.0),
                         fc.P(length * 0.47, band_h * 0.30 + 4.0)], kind="drill"),
            fc.Internal("cf eyelet L-v",
                        [fc.P(length * 0.47 - 4.0, band_h * 0.30),
                         fc.P(length * 0.47 + 4.0, band_h * 0.30)], kind="drill"),
            fc.Internal("cf eyelet R-h",
                        [fc.P(length * 0.53, band_h * 0.30 - 4.0),
                         fc.P(length * 0.53, band_h * 0.30 + 4.0)], kind="drill"),
            fc.Internal("cf eyelet R-v",
                        [fc.P(length * 0.53 - 4.0, band_h * 0.30),
                         fc.P(length * 0.53 + 4.0, band_h * 0.30)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Waistband Casing",
    )


# ── Back patch pocket (with drain eyelet) ────────────────────────────────────
def build_back_pocket():
    """A patch pocket: hemmed top opening, three turned sides, a drain eyelet
    drill cross at the bottom centre. Topstitched onto the outer back at the
    marked placement (a topstitch, not a length-balanced seam — like the
    bermuda/jeans back pockets)."""
    w = pocket_width
    d = pocket_depth
    taper = w * 0.06                      # slight trapezoid taper toward the base
    return fc.Piece(
        "back_pocket",
        [
            # top opening (hemmed), left → right
            fc.Edge("opening", [fc.Line(fc.P(0.0, d), fc.P(w, d))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, d), fc.P(w - taper, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(w - taper, 0.0), fc.P(taper, 0.0))]),
            fc.Edge("side_l", [fc.Line(fc.P(taper, 0.0), fc.P(0.0, d))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"opening": hem_allowance},  # top opening is hemmed
        notches=[fc.Notch("opening", 0.5, "fold/topstitch")],
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=[
            fc.Internal("drain eyelet-h",
                        [fc.P(w * 0.5 - 5.0, d * 0.16), fc.P(w * 0.5 + 5.0, d * 0.16)],
                        kind="drill"),
            fc.Internal("drain eyelet-v",
                        [fc.P(w * 0.5, d * 0.16 - 5.0), fc.P(w * 0.5, d * 0.16 + 5.0)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Back Patch Pocket",
    )


# ── Assembly ─────────────────────────────────────────────────────────────────
def build():
    pattern = fc.PatternSet("swim-trunks")
    outer_front, outer_back = build_outer()
    liner_front, liner_back = build_liner()
    waistband = build_waistband(outer_front, outer_back)
    back_pocket = build_back_pocket()

    picked = {
        "outer_front": outer_front,
        "outer_back": outer_back,
        "liner_front": liner_front,
        "liner_back": liner_back,
        "waistband": waistband,
        "back_pocket": back_pocket,
    }
    order = (outer_front, outer_back, liner_front, liner_back, waistband, back_pocket)
    everything = target_piece == "set"
    if everything:
        for piece in order:
            pattern.add(piece)
    elif target_piece in picked:
        pattern.add(picked[target_piece])
    else:  # unknown target → build the full set
        for piece in order:
            pattern.add(piece)
        everything = True

    if everything:
        # Outer trunk seams (curved/split side + straight inseam, both matched)
        pattern.declare_seam(("outer_front", "side"), ("outer_back", "side"), tol=1.5)
        pattern.declare_seam(("outer_front", "inseam"), ("outer_back", "inseam"), tol=1.5)
        # Mesh brief liner seams
        pattern.declare_seam(("liner_front", "side"), ("liner_back", "side"), tol=1.5)
        pattern.declare_seam(("liner_front", "inseam"), ("liner_back", "inseam"), tol=1.5)
        # Liner attaches to the outer AT THE WAIST (stacked), and the waistband
        # catches that stack — both length-match the outer waist opening.
        pattern.declare_seam(
            [("liner_front", "waist"), ("liner_front", "waist"),
             ("liner_back", "waist"), ("liner_back", "waist")],
            [("outer_front", "waist"), ("outer_front", "waist"),
             ("outer_back", "waist"), ("outer_back", "waist")],
            tol=1.5,
        )
        pattern.declare_seam(
            ("waistband", "bottom"),
            [("outer_front", "waist"), ("outer_front", "waist"),
             ("outer_back", "waist"), ("outer_back", "waist")],
            tol=1.5,
        )

    # ── BOM: exact fabric + exact-mm elastics + drawcord + thread + eyelets ──
    waist_opening = 2.0 * (outer_front.edge("waist").length()
                           + outer_back.edge("waist").length())
    leg_opening = liner_front.edge("hem").length() + liner_back.edge("hem").length()
    waist_elastic = round(waist_opening * waist_elastic_ratio)
    leg_elastic = round(leg_opening * leg_elastic_ratio)          # per leg
    drawcord_len = round(waist_opening * drawcord_ratio)

    shell_width = 1500.0   # tricot-nylon-elastano card width
    liner_width = 1500.0   # mesh liner grade of the same swim tricot card
    shell_area = sum(p.area() * p.cut.quantity
                     for p in (outer_front, outer_back, back_pocket))
    liner_area = sum(p.area() * p.cut.quantity for p in (liner_front, liner_back))
    shell_marker = shell_area / (shell_width * 0.62)
    liner_marker = liner_area / (liner_width * 0.60)

    pattern.bom = [
        {"item": "tricot-nylon-elastano", "qty": round(shell_marker / 10.0) * 10,
         "unit": "mm_length",
         "note": f"outer trunk shell + back pocket at {shell_width:.0f} mm width, 62% "
                 "marker efficiency; chlorine-resistant grade, greatest stretch (weft) "
                 "horizontal around the body; RELAXED cut, no negative ease on the outer"},
        {"item": "tricot-nylon-elastano", "qty": round(liner_marker / 10.0) * 10,
         "unit": "mm_length",
         "note": f"mesh brief liner at {liner_width:.0f} mm width, 60% marker efficiency; "
                 "use the LIGHTER open-mesh grade of this swim tricot for the inner brief "
                 "(quick-drain, drafted with mild negative ease)"},
        {"item": "plush-back waist elastic 35 mm", "qty": waist_elastic,
         "unit": "mm_length",
         "note": f"exact cut: {waist_opening:.0f} mm opening x {waist_elastic_ratio:.2f}; "
                 "join in a ring, quarter-mark, enclose in the casing catching both layers"},
        {"item": "clear/knit leg elastic 6 mm", "qty": 2 * leg_elastic,
         "unit": "mm_length",
         "note": f"two mesh-liner legs x {leg_elastic} mm each ({leg_opening:.0f} mm opening "
                 f"x {leg_elastic_ratio:.2f}); coverstitch into the marked leg zone"},
        {"item": "flat drawcord 4 mm", "qty": drawcord_len,
         "unit": "mm_length",
         "note": f"internal drawcord: {waist_opening:.0f} mm opening x {drawcord_ratio:.2f}; "
                 "threaded through the casing channel, exits the two CF eyelets; cord "
                 "stops/tips are a Yantra4D notion reference, not modelled here"},
        {"item": "metal/plastic eyelet 5 mm", "qty": 3, "unit": "count",
         "note": "2 center-front drawcord eyelets in the waistband + 1 drain eyelet in the "
                 "back pocket; eyelet/grommet hardware is a Yantra4D cartridge reference "
                 "(notion.kind=eyelet, hardware_ref -> yantra4d), not re-implemented here"},
        {"item": "polyester stretch thread", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11 needle; flatlock/coverstitch or 4-thread overlock every "
                 "seam to avoid chafe; bar-tack the pocket corners. Hardware is a "
                 "Yantra4D reference only."},
    ]

    pattern.metadata = {
        "fc100_rank": 53,
        "fabric_hint": "tricot-nylon-elastano",
        "liner_fabric_hint": "tricot-nylon-elastano (lighter open-mesh grade)",
        "construction": "relaxed board-short outer trunk (no negative ease) with a "
                        "curved/split side hem over a fitted mesh brief liner; one elastic "
                        "casing with an internal drawcord catches both layers",
        "curved_hem_note": "the outer hem edge is a bezier that sweeps up "
                           f"{side_scoop:.0f} mm at the side seam (board-short side vent)",
        "mesh_liner_note": "the mesh brief liner attaches at the waist only and hangs free "
                           "at the leg; its leg opening is elastic-finished with an exact-mm "
                           "cut length; it is the lighter open-mesh grade of the swim tricot",
        "drawcord_note": f"internal flat drawcord ({drawcord_len} mm) threaded through the "
                         "waistband channel, exiting two center-front eyelets",
        "back_pocket_note": "a patch pocket with a hemmed top and a drain eyelet at the "
                            "bottom centre, topstitched onto the outer back at the marked "
                            "placement (topstitch, not a length-balanced seam)",
        "outer_no_negative_ease": "the RELAXED outer trunk is drafted at body girth + ease "
                                  "like a woven short; the stretch is comfort, not fit",
        "liner_negative_ease_pct": liner_neg_ease,
        "waist_opening_mm": round(waist_opening, 1),
        "waist_elastic_mm": waist_elastic,
        "leg_opening_each_mm": round(leg_opening, 1),
        "leg_elastic_each_mm": leg_elastic,
        "drawcord_mm": drawcord_len,
        "outer_back_hem_solved": "back hem width solved so straight outer inseams match",
        "liner_waist_pinned": "liner waist width pinned to the outer waist so the waist "
                              "seam balances (delta ~ 0)",
        "drafting": "teaching-grade: outer trunk and mesh brief liner share one waistband; "
                    "both back hems solved analytically so the straight inseams match; the "
                    "mesh liner is a brief drafted with mild negative ease while its waist "
                    "is pinned to the outer waist so all waist-stack seams balance; the "
                    "relaxed outer takes no negative ease. Eyelet hardware is a Yantra4D ref.",
    }
    return pattern


result = build()
