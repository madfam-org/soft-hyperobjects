"""
House Slipper — Fashion Cabinet Garment Cartridge (FC-300 #228, lane 4 footwear).

A soft indoor slipper in the classic three-part cut: a `vamp` over the toes, a
`sole_upper` (the sole-line upper — the quarters that run round the foot from one side of
the vamp, past the heel, to the other), and a `collar` band that binds the foot opening.
Sized S–XL from a discrete size step, not from a body scan.

SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json declares NO foot landmark codes. This
cartridge is therefore SIZED (S/M/L/XL → a foot length in mm), with no `measurement`
block on any parameter. No landmark code is invented.

Pieces:
  - vamp       : toe cover (cut 1). Its curved `join` edge sews to the sole_upper.
  - sole_upper : the quarters, one piece cut on the fold at centre back (cut 1 on fold).
  - collar     : the binding band round the foot opening (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # vamp|sole_upper|collar|set

size = str(PARAM(lambda: size, "m"))                      # s|m|l|xl
vamp_length = float(PARAM(lambda: vamp_length, 105.0))    # toe cover, front-to-back
collar_width = float(PARAM(lambda: collar_width, 34.0))   # finished band width
foot_ease = float(PARAM(lambda: foot_ease, 22.0))         # slouch room round the foot
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Sizing table (S–XL → foot length / ball girth in mm) ─────────────────────
_SIZES = {
    "s": (235.0, 215.0),
    "m": (255.0, 235.0),
    "l": (275.0, 252.0),
    "xl": (295.0, 268.0),
}
if size not in _SIZES:
    size = "m"
FOOT_LEN, BALL_GIRTH = _SIZES[size]

# ── Clamps ───────────────────────────────────────────────────────────────────
vamp_length = max(60.0, min(vamp_length, 170.0))
collar_width = max(15.0, min(collar_width, 70.0))
foot_ease = max(0.0, min(foot_ease, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
VAMP_HALF = (BALL_GIRTH + foot_ease) / 2.0 / 2.0          # flat half-width at the ball
# The sole_upper is drafted flat and folded at centre back; its half-length runs from
# the vamp join, past the heel, to the fold.
QUARTER_RUN = FOOT_LEN - vamp_length * 0.55 + foot_ease * 0.25
QUARTER_H = collar_width * 1.5 + 28.0                     # height of the quarters


def _arc(name, p0, p1, target, side):
    """A single solved arc edge from p0 to p1 whose length == target (bisected bulge)."""
    def mk(bulge):
        return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])

    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} mm shorter than chord {chord:.1f} mm")
    lo, hi = 0.0, 3.0
    if mk(hi).length(0.05) < target:
        raise ValueError(f"{name}: target {target:.1f} mm unreachable at max bulge")
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if mk(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    edge = mk((lo + hi) / 2.0)
    got = edge.length(0.05)
    if abs(got - target) > 0.5:
        raise ValueError(f"{name}: solver did not converge ({got:.1f} vs {target:.1f})")
    return edge


def build_vamp():
    """Toe cover: a straight front edge at the toe, two short sides, and a curved
    `join` edge across the back that the sole_upper's front edges sew to."""
    w = VAMP_HALF
    ln = vamp_length
    return fc.Piece(
        "vamp",
        [
            fc.Edge("toe", [fc.curve_through(fc.P(-w * 0.55, 0.0), fc.P(w * 0.55, 0.0),
                                             bulge=0.22, side=-1.0)]),
            fc.Edge("side_r", [fc.Line(fc.P(w * 0.55, 0.0), fc.P(w, ln))]),
            # join: bows back into the piece so the quarters meet it smoothly
            fc.Edge("join", [fc.curve_through(fc.P(w, ln), fc.P(-w, ln),
                                              bulge=0.14, side=-1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(-w, ln), fc.P(-w * 0.55, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join", 0.5, "centre front"),
                 fc.Notch("toe", 0.5, "centre toe")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, ln - 8.0)),
        internals=[fc.Internal("centre-front",
                               [fc.P(0.0, 0.0), fc.P(0.0, ln)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe cover)",
    )


def build_sole_upper(join_target):
    """The quarters: cut 1 on the fold at centre back. Its `join` edge is solved to
    exactly HALF the vamp's join length (the piece is cut on the fold, so its two
    mirrored join edges together sew to the vamp's single join) — the declared seam
    then verifies at delta ~ 0.

    Drafted as a rectangle-ish panel whose front edge is the solved join arc, back
    edge is the centre-back fold, bottom is the sole line, top is the collar line.
    The panel height is taken from the join budget (a solved arc must be LONGER than
    its chord), never set independently — otherwise the chord outruns the target and
    the seam cannot close.
    """
    ln = QUARTER_RUN
    half_join = join_target / 2.0
    # The join arc must exceed its own chord, so the panel height is capped by the
    # join budget. Every slider combination stays draftable: a short vamp simply
    # yields shallower quarters rather than an unbuildable piece.
    h = max(18.0, min(QUARTER_H, half_join * 0.86))
    p_bf = fc.P(0.0, 0.0)           # bottom front (sole line, at the vamp)
    p_bb = fc.P(ln, 0.0)            # bottom back (sole line, at the fold)
    p_tb = fc.P(ln, h)              # top back (collar line, at the fold)
    p_tf = fc.P(0.0, h)             # top front (collar line, at the vamp)
    return fc.Piece(
        "sole_upper",
        [
            fc.Edge("sole_line", [fc.curve_through(p_bf, p_bb, bulge=0.05, side=1.0)]),
            fc.Edge("centre_back", [fc.Line(p_bb, p_tb)]),
            fc.Edge("collar_line", [fc.curve_through(p_tb, p_tf, bulge=0.05, side=1.0)]),
            _arc("join", p_tf, p_bf, half_join, side=1.0),
        ],
        seam_allowance=seam_allowance,
        allowances={"sole_line": 12.0},
        notches=[fc.Notch("sole_line", 0.5, "side"),
                 fc.Notch("collar_line", 0.5, "side")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="centre_back", mirror=True),
        label="Sole-line upper (quarters)",
    )


def build_collar(opening):
    """Binding band round the foot opening. Cut as a flat strip twice the finished
    width (folded lengthwise when sewn); its `attach` edge equals the opening."""
    band_len = opening + 2.0 * seam_allowance
    band_h = collar_width * 2.0
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
            fc.Edge("outer", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                    # length already carries the joins
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Collar band",
    )


def build():
    pattern = fc.PatternSet("house-slipper")
    everything = target_piece == "set"

    vamp = build_vamp()
    join_target = vamp.edge("join").length(0.05)
    quarters = build_sole_upper(join_target)
    # Foot opening: the quarters' collar line (doubled — cut on fold) + the vamp's
    # join is enclosed, so the opening the collar binds is the collar_line run.
    opening = 2.0 * quarters.edge("collar_line").length(0.05)
    collar = build_collar(opening)

    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "sole_upper":
        pattern.add(quarters)
    if everything or target_piece == "collar":
        pattern.add(collar)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything:
        # The quarters are cut on the fold: TWO join edges sew to the vamp's one join.
        pattern.declare_seam(
            [("vamp", "join")],
            [("sole_upper", "join"), ("sole_upper", "join")],
            tol=1.5)
        # Collar attach binds the doubled collar line, plus its own two joins.
        pattern.declare_seam(
            [("collar", "attach")],
            [("sole_upper", "collar_line"), ("sole_upper", "collar_line")],
            ease=2.0 * seam_allowance, tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.58)
    pattern.bom = [
        {"item": "boiled wool, fleece, or quilted cotton (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 58% marker. Per PAIR, double this."},
        {"item": "non-slip sole fabric or suede", "qty": 2, "unit": "pcs",
         "note": "cut from the sole line; a grippy underside for hard floors."},
        {"item": "wadding / batting (optional)", "qty": 1, "unit": "as chosen",
         "note": "quilt between upper and lining for a warmer, softer slipper."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "set the vamp, close the centre back, bind the collar."},
    ]
    pattern.metadata = {
        "fc300_rank": 228, "family": "footwear_soft", "fabric_hint": "polar-lana",
        "silhouette_note": "A soft three-part indoor slipper: a toe vamp, quarters cut "
            "on the fold at centre back running round to the heel, and a folded collar "
            "band binding the foot opening.",
        "sizing_note": "SIZED S-XL (no body scan): ISO 8559 as vendored declares no "
            "foot landmark codes, so no measurement code is claimed or invented.",
        "solved": {
            "size": size,
            "foot_length_mm": FOOT_LEN,
            "vamp_half_mm": round(VAMP_HALF, 1),
            "quarter_run_mm": round(QUARTER_RUN, 1),
            "quarter_height_mm": round(quarters.edge("centre_back").length(0.05), 1),
            "opening_mm": round(opening, 1),
        },
    }
    return pattern


result = build()
