"""
Cavalier Cloak — Fashion Cabinet Costume Cartridge (FC-300 rank #275, y4d clasp bridged).

The short circular cloak of the 17th century, c. 1620–1660 — the half-cloak worn slung from
one shoulder that gives the "cavalier" its outline. It is a garment of pure GEOMETRY: a
sector of an annulus, cut so the inner arc fits the neck and the outer arc is whatever that
sector's radius makes it. Nothing about it is eased, gathered, or fitted; if the arithmetic
is right the cloak hangs correctly, and if it is wrong nothing downstream can save it.

The documented construction this draft reproduces:

  - a CIRCULAR cut — a sector of an annulus, not a rectangle gathered at the neck. The
    difference is visible immediately in wear: a circular cloak falls in soft rolling folds
    of its own weight, a gathered rectangle stands away in stiff pleats at the neck;
  - a sweep of less than a full circle, so the cloak is a HALF-cloak that hangs open at the
    front and can be thrown back over one shoulder, which is the whole cavalier look;
  - a shaped standing COLLAR set to the neck arc;
  - a single clasp at the throat, which is the only fastening — the cloak is not buttoned.

Drafting note — the seam that must SOLVE, and it is arithmetic rather than easing. The
cloak is a sector of an annulus with inner radius r, outer radius R, and sweep angle θ. The
inner arc has to equal the wearer's neck run:

    inner arc  =  r × θ            so    r  =  neck_run / θ

and NOT a radius picked to look right. This cartridge computes r from the MEASURED neck
run and the requested sweep, builds the inner arc as a real polyline at that radius, then
MEASURES it back off the built curve and reports the residual against the neck run — so the
arithmetic is proved rather than trusted. The collar is likewise cut to the MEASURED inner
arc, not to the nominal neck girth.

Because the sweep is a parameter, the same cartridge covers a modest 3/4-circle cloak and a
dramatic near-full-circle one, and the maker can see exactly what the sweep costs in cloth:
the hem run is reported, and it grows with θ while the neck radius SHRINKS with θ. That
inverse relationship is the thing people get wrong by eye.

Pieces:
  - cloak   : the annular sector, cut 1 (or 2 and seamed at the centre back on narrow cloth).
  - collar  : standing collar, cut to the MEASURED inner arc (cut 1 on fold).
  - facing  : front edge facing, the period finish for a cloak worn thrown back (cut 2).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # cloak|collar|facing|set

neck_girth = float(PARAM(lambda: neck_girth, 420.0))     # over the doublet collar, not bare
cloak_length = float(PARAM(lambda: cloak_length, 760.0))  # neck to hem, along the radius
sweep_deg = float(PARAM(lambda: sweep_deg, 300.0))       # how much of a circle the cloak is
collar_height = float(PARAM(lambda: collar_height, 78.0))
facing_width = float(PARAM(lambda: facing_width, 90.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 14.0))

# ── Clamps (sane 17th-c half-cloak ranges) ───────────────────────────────────
neck_girth = max(300.0, min(neck_girth, 620.0))
cloak_length = max(380.0, min(cloak_length, 1250.0))
sweep_deg = max(140.0, min(sweep_deg, 350.0))
collar_height = max(30.0, min(collar_height, 140.0))
facing_width = max(40.0, min(facing_width, 180.0))
seam_allowance = max(0.0, min(seam_allowance, 25.0))

# ── The geometry ─────────────────────────────────────────────────────────────
# The neck run the cloak is drafted to. The cloak goes over a doublet collar, so a little
# clearance is added — a cloak cut to the bare neck strangles the wearer.
NECK_RUN = neck_girth + 26.0

THETA = math.radians(sweep_deg)          # the sector's sweep, in radians

# THE equation. The inner arc must equal the neck run, so the inner radius is DERIVED from
# it and from the sweep — never picked to look right on the page.
#     inner arc = r * theta   =>   r = neck_run / theta
R_INNER = NECK_RUN / THETA
R_OUTER = R_INNER + cloak_length

ARC_STEPS = 64   # polyline resolution of both arcs


def _arc_points(radius, steps=ARC_STEPS, reverse=False):
    """Points along an arc of the given radius, swept through THETA about the origin.

    The sector is drawn symmetric about the +y axis so the cloak's centre back sits at the
    top of the piece and the two front edges fall either side — the way it is worn.
    """
    a0 = math.pi / 2.0 - THETA / 2.0
    pts = []
    for i in range(steps + 1):
        t = i / steps
        a = a0 + THETA * (1.0 - t if reverse else t)
        pts.append(fc.P(radius * math.cos(a), radius * math.sin(a)))
    return pts


INNER_PTS = _arc_points(R_INNER)
OUTER_PTS = _arc_points(R_OUTER, reverse=True)


def build_cloak():
    """The annular sector: the cloak itself.

    `neck` is the inner arc (takes the collar), `hem` is the outer arc, and the two
    straight radial edges are the front opening edges, which take the facings.
    """
    inner_segs = [fc.Line(INNER_PTS[i], INNER_PTS[i + 1]) for i in range(len(INNER_PTS) - 1)]
    outer_segs = [fc.Line(OUTER_PTS[i], OUTER_PTS[i + 1]) for i in range(len(OUTER_PTS) - 1)]
    internals = [
        # The centre-back line — the balance point of the whole garment, and the seam line
        # if the cloak has to be cut in two halves on narrow cloth.
        fc.Internal("centre-back",
                    [fc.P(0.0, R_INNER), fc.P(0.0, R_OUTER)], kind="marking"),
        # Where the clasp sits at the throat.
        fc.Internal("clasp-position",
                    [INNER_PTS[2], INNER_PTS[len(INNER_PTS) - 3]], kind="trace"),
    ]
    return fc.Piece(
        "cloak",
        [
            fc.Edge("neck", inner_segs),
            fc.Edge("front_r", [fc.Line(INNER_PTS[-1], OUTER_PTS[0])]),
            fc.Edge("hem", outer_segs),
            fc.Edge("front_l", [fc.Line(OUTER_PTS[-1], INNER_PTS[0])]),
        ],
        seam_allowance=seam_allowance,
        # A circular hem is cut on every grain at once, so it is turned narrowly or faced;
        # a deep turned hem on a curve will never lie flat.
        allowances={"hem": 12.0, "neck": 10.0},
        notches=[fc.Notch("neck", 0.5, "centre back"),
                 fc.Notch("neck", 0.25, "collar quarter"),
                 fc.Notch("neck", 0.75, "collar quarter"),
                 fc.Notch("hem", 0.5, "centre back")],
        # The grain runs down the centre back: the balance line of a circular cloak.
        grainline=fc.Grainline(fc.P(0.0, R_INNER + 40.0), fc.P(0.0, R_OUTER - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cloak (cut 1; or 2 and seam at CB on narrow cloth)",
    )


CLOAK = build_cloak()

# ── The proof ────────────────────────────────────────────────────────────────
# The inner arc was CONSTRUCTED at the derived radius. Measure it back off the built
# polyline and compare it with the neck run it is supposed to equal. This is the whole
# verification of the geometry: if the arithmetic were wrong, this residual would show it.
NECK_ARC_MEASURED = CLOAK.edge("neck").length()
NECK_RESIDUAL = NECK_ARC_MEASURED - NECK_RUN
HEM_ARC_MEASURED = CLOAK.edge("hem").length()


# The collar's neck edge is drafted as a shallow CURVE, not a straight line — it is set to
# a curved neck edge, and a straight band on a curve either ripples at the top or strangles
# at the bottom. But a curve is LONGER than the chord it spans, so setting the collar's
# half-width to half the neck arc makes the collar's edge overshoot: an earlier revision did
# exactly that and left a 1.6 mm surplus the verifier caught. The half-width is therefore
# SOLVED so the built curve MEASURES half the neck arc.
COLLAR_BULGE = 0.05


def _collar_edge_length(half_w):
    """MEASURED length of the collar's curved neck edge at a given half-width."""
    c = fc.curve_through(fc.P(half_w, 0.0), fc.P(0.0, 0.0), COLLAR_BULGE, -1.0)
    return fc.polyline_length(c.flatten(0.2))


def _solve_collar_half(target):
    """Bisect the collar's half-width until its curved neck edge measures `target`."""
    lo, hi = 1.0, target * 1.5
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _collar_edge_length(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


COLLAR_HALF = _solve_collar_half(NECK_ARC_MEASURED / 2.0)


def build_collar():
    """Standing collar, cut to the MEASURED inner arc (cut 1 on fold).

    Drafted as a shallow annular strip rather than a straight band. Its half-width is
    SOLVED so the built curved neck edge measures exactly half the cloak's neck arc.
    """
    half = COLLAR_HALF
    h = collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("upper", [fc.curve_through(fc.P(0.0, h), fc.P(half, h),
                                               COLLAR_BULGE, -1.0)]),
            fc.Edge("front_end", [fc.Line(fc.P(half, h), fc.P(half, 0.0))]),
            fc.Edge("neck_seam", [fc.curve_through(fc.P(half, 0.0), fc.P(0.0, 0.0),
                                                   COLLAR_BULGE, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_seam", 0.5, "collar quarter")],
        grainline=fc.Grainline(fc.P(half * 0.2, h * 0.5), fc.P(half * 0.8, h * 0.5)),
        internals=[fc.Internal("clasp-anchor", [fc.P(half - 14.0, h * 0.4),
                                                fc.P(half - 14.0, h * 0.4 + 1.0)],
                               kind="drill")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Standing collar (cut 1 on fold, to the MEASURED neck arc)",
    )


# The front edge run: the straight radial edge, which is exactly cloak_length.
FRONT_EDGE = CLOAK.edge("front_r").length()


def build_facing():
    """Front edge facing (cut 2, mirrored) — the period finish for a cloak worn thrown back.

    Cut to the MEASURED front edge, because the whole point of a facing is that it matches
    the edge it faces. A cloak is worn open and thrown over one shoulder, so the underside
    of the front edge is on show and is faced rather than merely turned.
    """
    ln, w = FRONT_EDGE, facing_width
    return fc.Piece(
        "facing",
        [
            fc.Edge("neck_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("inner", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
            fc.Edge("hem_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
            fc.Edge("front_edge", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "front balance")],
        grainline=fc.Grainline(fc.P(w * 0.5, 30.0), fc.P(w * 0.5, ln - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front facing (cut 2 mirrored, to the MEASURED front edge)",
    )


def build():
    pattern = fc.PatternSet("cavalier-cloak")
    everything = target_piece == "set"
    if everything or target_piece == "cloak":
        pattern.add(CLOAK)
    if everything or target_piece == "collar":
        pattern.add(build_collar())
    if everything or target_piece == "facing":
        pattern.add(build_facing())

    if everything:
        # The collar takes the whole measured neck arc. It is cut on the fold, so its
        # drafted neck edge is HALF the run and the check counts it twice.
        pattern.declare_seam(("cloak", "neck"),
                             [("collar", "neck_seam"), ("collar", "neck_seam")],
                             tol=1.0)
        # Each facing takes one front edge.
        pattern.declare_seam(("facing", "front_edge"), ("cloak", "front_r"), tol=1.0)
        pattern.declare_seam(("facing", "front_edge"), ("cloak", "front_l"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    # A circular sector nests terribly — this is the honest cost of the cut, and it is the
    # reason period cloaks on narrow cloth are seamed at the centre back.
    marker_len = total_area / (fabric_width * 0.55)
    needs_cb_seam = (R_OUTER * 2.0) > fabric_width
    _cb_note = ("MUST be cut in two halves and seamed at the centre back"
                if needs_cb_seam else "fits in one piece")
    pattern.bom = [
        {"item": "wool broadcloth or melton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at 1400 mm width, 55% marker — a circular sector nests badly and that "
                 f"low yield is the real cost of the cut. The piece spans "
                 f"{round(R_OUTER * 2.0)} mm at its widest, so on this width it "
                 f"{_cb_note}. "
                 f"A fulled wool is what makes the folds roll; a thin cloth flutters."},
        {"item": "cloak clasp (Yantra4D magnetic-clasp)", "qty": 1, "unit": "count",
         "note": "ONE clasp at the throat is the entire fastening — a cavalier cloak is not "
                 "buttoned. The period original is a hook-and-chain or a pair of cords."},
        {"item": "collar interfacing", "qty": round(NECK_ARC_MEASURED + 60.0),
         "unit": "mm_length",
         "note": "the standing collar must hold up on its own."},
        {"item": "lining (optional, period-plausible)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a contrast lining shows whenever the cloak is thrown back over the "
                 "shoulder, which is most of the time it is worn — it is a visible surface, "
                 "not a hidden one."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "the hem is a curve cut on every grain at once: turn it narrowly or face "
                 "it, because a deep turned hem on a circular edge will never lie flat."},
    ]
    pattern.metadata = {
        "fc300_rank": 275,
        "family": "costume_historical",
        "period": "c. 1620–1660 (17th century)",
        "fabric_hint": "lana-melton-abrigo",
        "silhouette_note": "A CIRCULAR cut, not a gathered rectangle. A circular cloak falls "
            "in soft rolling folds of its own weight; a rectangle gathered at the neck stands "
            "away in stiff pleats. The difference is obvious the moment it is worn, and it is "
            "the single thing that separates a cavalier cloak from a costume-shop cape.",
        "construction_note": "A sector of an annulus whose inner radius is DERIVED from the "
            "neck run and the sweep angle. Standing collar set to the measured neck arc, "
            "faced front edges, and a single clasp at the throat.",
        "hardware": "throat clasp via Yantra4D (notion.hardware_ref -> magnetic-clasp); the "
            "collar height drives disc_dia — the dimensional handshake.",
        "solved": {
            "sweep_deg": round(sweep_deg, 2),
            "neck_run_target_mm": round(NECK_RUN, 2),
            "inner_radius_derived_mm": round(R_INNER, 2),
            "outer_radius_mm": round(R_OUTER, 2),
            "neck_arc_measured_mm": round(NECK_ARC_MEASURED, 2),
            "neck_arc_residual_mm": round(NECK_RESIDUAL, 3),
            "hem_arc_measured_mm": round(HEM_ARC_MEASURED, 1),
            "front_edge_mm": round(FRONT_EDGE, 2),
            "collar_half_width_solved_mm": round(COLLAR_HALF, 2),
            "collar_edge_residual_mm": round(
                _collar_edge_length(COLLAR_HALF) * 2.0 - NECK_ARC_MEASURED, 4),
            "piece_span_mm": round(R_OUTER * 2.0, 1),
            "needs_cb_seam_at_1400mm": needs_cb_seam,
            "note": "the inner radius is DERIVED from r = neck_run / theta, never picked to "
                    "look right. The inner arc is then built as a real polyline at that "
                    "radius and MEASURED back, and the residual against the neck run is "
                    "reported — so the arithmetic is proved rather than trusted. Note the "
                    "inverse relationship people get wrong by eye: a WIDER sweep gives a "
                    "SMALLER neck radius and a longer hem, because the same neck run is "
                    "spread over more angle.",
        },
    }
    return pattern


result = build()
