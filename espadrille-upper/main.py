"""
Espadrille Upper — Fashion Cabinet Garment Cartridge (FC-300 #227, lane 4 footwear).

The canvas upper of an espadrille, drafted as the traditional two-piece cut: a `vamp`
covering the toes and instep, and a `heel_counter` wrapping the back of the foot. The two
meet at a pair of side seams; the whole lower edge (the lasting edge) is what the maker
stitches down to a jute-braid sole. Optional lace eyelets are marked up the heel counter's
top edge for the ankle-tie espadrille (the alpargata with cintas).

FOOT SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json has NO foot landmark codes (no foot_length,
no foot girth). This cartridge therefore drafts from plain SIZED parameters — foot_length
and foot_girth are ordinary millimetre inputs, NOT measurement-coded body landmarks. No
landmark code is invented. `ankle_girth` IS canonical but the espadrille upper does not
reach the ankle, so it is not used here.

Pieces:
  - vamp          : toe + instep cover (cut 1). Lasting edge below, topline above.
  - heel_counter  : back-of-foot wrap (cut 1). Lasting edge below, topline above,
                    eyelet placements marked when `eyelets` is on.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # vamp|heel_counter|set

# Sized params (NOT ISO-8559 landmarks — the schema has no foot codes).
foot_length = float(PARAM(lambda: foot_length, 255.0))    # heel to longest toe
foot_girth = float(PARAM(lambda: foot_girth, 235.0))      # around the ball of the foot
vamp_depth = float(PARAM(lambda: vamp_depth, 95.0))       # how far back the vamp reaches
counter_height = float(PARAM(lambda: counter_height, 62.0))   # heel wrap height
eyelets = bool(PARAM(lambda: eyelets, True))              # lace eyelets on the counter
eyelet_pairs = int(PARAM(lambda: eyelet_pairs, 3))        # per side of the counter
eyelet_dia = float(PARAM(lambda: eyelet_dia, 5.0))        # finished lace hole diameter
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
vamp_depth = max(50.0, min(vamp_depth, 170.0))
counter_height = max(35.0, min(counter_height, 130.0))
eyelet_pairs = max(1, min(eyelet_pairs, 6))
eyelet_dia = max(3.0, min(eyelet_dia, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
# The sole outline is a closed loop of length ~ 2*foot_length*SOLE_K (a foot-shaped
# lens is longer than twice its straight length). The upper is split between the two
# pieces along that perimeter: the vamp takes the front share, the counter the back.
SOLE_K = 1.08
SOLE_PERIM = 2.0 * foot_length * SOLE_K
VAMP_SHARE = max(0.28, min(vamp_depth / foot_length + 0.10, 0.62))
# Lasting run each piece stitches to the sole (its share of the perimeter).
VAMP_LAST = SOLE_PERIM * VAMP_SHARE
COUNTER_LAST = SOLE_PERIM * (1.0 - VAMP_SHARE)
# The vamp wraps the ball of the foot: half-girth is its flat half-width.
VAMP_HALF = foot_girth / 2.0 / 2.0 + 6.0
COUNTER_HALF = foot_girth / 2.0 / 2.0 * 0.86


def _arc(name, p0, p1, target, side):
    """An edge that is a single solved arc from p0 to p1 whose length == target.

    Bisects `bulge` (edge length grows monotonically with bulge over this range),
    the baby-sleeper sole-solver precedent. Raises rather than silently drafting a
    mismatched seam — verification is fail-closed.
    """
    def mk(bulge):
        return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])

    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} mm is shorter than the "
                         f"chord {chord:.1f} mm — geometry cannot close")
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
    """Toe + instep cover. Two straight side seams; a solved lasting arc below and a
    solved topline arc above so the sewn runs are exact, not eyeballed."""
    h = vamp_depth
    # Side seams run up from the lasting edge to the topline; their length is the
    # seam the counter must match exactly (shared coordinate => shared length).
    p_ll = fc.P(-VAMP_HALF, 0.0)
    p_lr = fc.P(VAMP_HALF, 0.0)
    p_tr = fc.P(VAMP_HALF * 0.80, h)
    p_tl = fc.P(-VAMP_HALF * 0.80, h)
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)], kind="marking"),
    ]
    return fc.Piece(
        "vamp",
        [
            # lasting edge: bows DOWN (away from the piece) to make the toe curve
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 12.0},          # topline is turned and stitched
        notches=[fc.Notch("lasting", 0.5, "centre toe"),
                 fc.Notch("topline", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_heel_counter(side_seam_len):
    """Back-of-foot wrap. Its two side seams are drafted to EXACTLY the vamp's side
    seam length, so both declared side seams verify at delta ~ 0."""
    h = counter_height
    p_ll = fc.P(-COUNTER_HALF, 0.0)
    p_lr = fc.P(COUNTER_HALF, 0.0)
    # Top corners placed so each straight side seam == side_seam_len exactly.
    dx = COUNTER_HALF * 0.12
    dy2 = side_seam_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("heel counter: side seam shorter than its horizontal run")
    dy = dy2 ** 0.5
    p_tr = fc.P(COUNTER_HALF - dx, dy)
    p_tl = fc.P(-COUNTER_HALF + dx, dy)

    internals = [
        fc.Internal("centre-back", [fc.P(0.0, 0.0), fc.P(0.0, dy)], kind="marking"),
    ]
    if eyelets:
        # Eyelet ladder: `eyelet_pairs` per side, set in from the side seam and down
        # from the topline, marked as drill points (the eyelet is Yantra4D hardware).
        inset = max(10.0, eyelet_dia * 2.2)
        for i in range(eyelet_pairs):
            t = (i + 0.5) / eyelet_pairs
            for sgn in (-1.0, 1.0):
                cx = sgn * (COUNTER_HALF - dx) * (0.42 + 0.52 * t)
                cy = dy - inset - (h * 0.16) * t
                r = eyelet_dia / 2.0
                side_tag = "l" if sgn < 0 else "r"
                internals.append(fc.Internal(
                    f"eyelet-{side_tag}{i + 1}",
                    [fc.P(cx - r, cy), fc.P(cx + r, cy)], kind="drill"))
    return fc.Piece(
        "heel_counter",
        [
            _arc("lasting", p_ll, p_lr, COUNTER_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.06, side=-1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 12.0},
        notches=[fc.Notch("lasting", 0.5, "centre back"),
                 fc.Notch("topline", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, dy - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Heel counter",
    )


def build():
    pattern = fc.PatternSet("espadrille-upper")
    everything = target_piece == "set"
    vamp = build_vamp()
    side_len = vamp.edge("side_r").length(0.05)
    counter = build_heel_counter(side_len)

    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "heel_counter":
        pattern.add(counter)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything or target_piece == "set":
        pattern.declare_seam(("vamp", "side_r"), ("heel_counter", "side_l"), tol=1.0)
        pattern.declare_seam(("vamp", "side_l"), ("heel_counter", "side_r"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    n_eyelets = (2 * eyelet_pairs) if eyelets else 0
    pattern.bom = [
        {"item": "cotton canvas / duck (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 55% marker; small awkward pieces waste more. "
                 "Per PAIR, double this."},
        {"item": "jute braid espadrille sole", "qty": 2, "unit": "pcs",
         "note": "the vulcanised or stitched jute sole the lasting edge sews down to."},
        {"item": "cotton drill lining (optional)", "qty": 1, "unit": "as chosen",
         "note": "a lining softens the topline and hides the lasting stitches."},
        {"item": "garment eyelets + washers", "qty": n_eyelets, "unit": "pairs",
         "note": "Yantra4D `garment-eyelet` — printed or metal; set through the "
                 "counter's marked drill points. Zero when eyelets are off."},
        {"item": "waxed lasting thread", "qty": 1, "unit": "spool",
         "note": "heavy thread for the sole stitch-down; a curved needle helps."},
    ]
    pattern.metadata = {
        "fc300_rank": 227, "family": "footwear_soft", "fabric_hint": "lona-algodon",
        "silhouette_note": "A two-piece canvas espadrille upper: a vamp over the toes "
            "and instep, a heel counter round the back, joined at two side seams and "
            "stitched down to a jute sole along the lasting edge. Optional eyelet "
            "ladder for ankle ties.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — "
            "ISO 8559 (as vendored) declares no foot landmark codes, so none is "
            "claimed and none is invented.",
        "solved": {
            "sole_perimeter_mm": round(SOLE_PERIM, 1),
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "counter_lasting_mm": round(COUNTER_LAST, 1),
            "side_seam_mm": round(side_len, 1),
            "eyelets": n_eyelets,
        },
    }
    return pattern


result = build()
