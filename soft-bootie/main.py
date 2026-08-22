"""
Soft Bootie — Fashion Cabinet Garment Cartridge (FC-300 #232, lane 4 footwear).

An indoor bootie — a slipper that comes up over the ankle. Three pieces plus a padded
collar: a `sole` (the flat underfoot lens), a `side` panel that wraps the whole foot from
one side of the toe, round the heel, to the other (cut 1, mirrored), and a `vamp` closing
over the toes, finished with a `collar` band quilted round the ankle opening.

The sole is drafted as a lens of two solved arcs, each equal to the side panel's lower
edge — the baby-sleeper sole-solver precedent, which is the right construction for any
soft-sole footwear.

SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json declares NO foot landmark codes, so
foot_length is a PLAIN parameter with no `measurement` block. `ankle_girth` IS canonical
and IS claimed — a bootie comes up over the ankle, so that ring is genuinely measured.

Pieces:
  - sole   : underfoot lens (cut 2, mirrored) — two solved arcs to a heel/toe chord.
  - side   : the wrap panel (cut 2, mirrored).
  - vamp   : toe closure (cut 1).
  - collar : padded ankle band (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # sole|side|vamp|collar|set

# Plain sized param — ISO 8559 has no foot codes.
foot_length = float(PARAM(lambda: foot_length, 255.0))
# ankle_girth IS a canonical ISO-8559 landmark — the bootie clears the ankle.
ankle_girth = float(PARAM(lambda: ankle_girth, 245.0))

shaft_height = float(PARAM(lambda: shaft_height, 105.0))   # sole to collar seam
vamp_length = float(PARAM(lambda: vamp_length, 92.0))      # toe closure length
collar_pad = float(PARAM(lambda: collar_pad, 30.0))        # finished padded band width
foot_ease = float(PARAM(lambda: foot_ease, 24.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 330.0))
ankle_girth = max(160.0, min(ankle_girth, 340.0))
shaft_height = max(50.0, min(shaft_height, 240.0))
vamp_length = max(45.0, min(vamp_length, 170.0))
collar_pad = max(12.0, min(collar_pad, 80.0))
foot_ease = max(0.0, min(foot_ease, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
SOLE_LEN = foot_length + 10.0
# The side panel's lower edge runs the sole's half-perimeter (toe to heel down one
# side); the sole's two arcs are each solved to exactly that run.
SIDE_RUN = SOLE_LEN * 1.06


def _arc_edge(name, p0, p1, bulge, side):
    return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])


def _solve_arc(name, p0, p1, target, side):
    """Solved arc edge from p0 to p1 whose length == target (bisected bulge)."""
    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} mm shorter than chord {chord:.1f} mm")
    lo, hi = 0.0, 3.0
    if _arc_edge(name, p0, p1, hi, side).length(0.05) < target:
        raise ValueError(f"{name}: target {target:.1f} mm unreachable at max bulge")
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if _arc_edge(name, p0, p1, mid, side).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    edge = _arc_edge(name, p0, p1, (lo + hi) / 2.0, side)
    got = edge.length(0.05)
    if abs(got - target) > 0.5:
        raise ValueError(f"{name}: solver did not converge ({got:.1f} vs {target:.1f})")
    return edge


def build_sole():
    """The underfoot lens: a heel-to-toe chord with two mirrored solved arcs, each
    equal to the side panel's lower edge so both attach seams verify at delta ~ 0."""
    # Chord scales with the run so the solved bulge stays well-behaved across sizes.
    chord = max(SOLE_LEN * 0.72, ankle_girth / 2.0 + 20.0)
    heel = fc.P(0.0, 0.0)
    toe = fc.P(chord, 0.0)
    return fc.Piece(
        "sole",
        [
            _solve_arc("attach_out", heel, toe, SIDE_RUN, side=1.0),
            _solve_arc("attach_in", toe, heel, SIDE_RUN, side=1.0),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach_out", 0.5, "side match"),
                 fc.Notch("attach_in", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(chord * 0.5, -8.0), fc.P(chord * 0.5, 8.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sole (underfoot)",
    )


def build_side():
    """The wrap panel: lower edge sews to one sole arc, upper edge to the collar,
    front edge to the vamp, back edge to its mirror at centre back."""
    h = shaft_height
    ln = SIDE_RUN
    p_bf = fc.P(0.0, 0.0)          # bottom front (toe end of the sole seam)
    p_bb = fc.P(ln, 0.0)           # bottom back (heel end)
    p_tb = fc.P(ln * 0.92, h)      # top back (centre back, collar line)
    p_tf = fc.P(vamp_length * 0.5, h)   # top front (vamp join, collar line)
    return fc.Piece(
        "side",
        [
            fc.Edge("sole_seam", [fc.Line(p_bf, p_bb)]),
            fc.Edge("centre_back", [fc.Line(p_bb, p_tb)]),
            fc.Edge("collar_line", [fc.Line(p_tb, p_tf)]),
            fc.Edge("vamp_seam", [fc.Line(p_tf, p_bf)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sole_seam", 0.5, "sole match"),
                 fc.Notch("collar_line", 0.5, "collar match")],
        grainline=fc.Grainline(fc.P(ln * 0.25, 10.0), fc.P(ln * 0.25, h - 10.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side (wrap panel)",
    )


def build_vamp(vamp_seam_len):
    """Toe closure. Its two side edges are drafted to exactly the side panel's
    vamp_seam length, so both declared seams verify at delta ~ 0."""
    hw = (foot_length * 0.30 + foot_ease * 0.5) / 2.0
    # Place the top corners so each straight side edge == vamp_seam_len.
    dx = hw * 0.30
    dy2 = vamp_seam_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("vamp: side seam shorter than its horizontal run")
    dy = dy2 ** 0.5
    return fc.Piece(
        "vamp",
        [
            fc.Edge("toe", [fc.curve_through(fc.P(-hw + dx, 0.0), fc.P(hw - dx, 0.0),
                                             bulge=0.26, side=-1.0)]),
            fc.Edge("side_r", [fc.Line(fc.P(hw - dx, 0.0), fc.P(hw, dy))]),
            fc.Edge("throat", [fc.curve_through(fc.P(hw, dy), fc.P(-hw, dy),
                                                bulge=0.10, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(-hw, dy), fc.P(-hw + dx, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("toe", 0.5, "centre toe"),
                 fc.Notch("throat", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, dy - 8.0)),
        internals=[fc.Internal("centre-front",
                               [fc.P(0.0, 0.0), fc.P(0.0, dy)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe closure)",
    )


def build_collar(opening):
    """Padded ankle band: cut flat at twice the finished width, quilted with wadding
    and folded lengthwise when sewn."""
    band_len = opening + 2.0 * seam_allowance
    band_h = collar_pad * 2.0
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                    # length already carries the joins
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[
            fc.Internal("fold line",
                        [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
                        kind="marking"),
            fc.Internal("quilt line",
                        [fc.P(0.0, band_h * 0.25), fc.P(band_len, band_h * 0.25)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Collar (padded ankle band)",
    )


def build():
    pattern = fc.PatternSet("soft-bootie")
    everything = target_piece == "set"

    sole = build_sole()
    side = build_side()
    vamp = build_vamp(side.edge("vamp_seam").length(0.05))
    # Opening the collar binds: both side panels' collar lines + the vamp's throat.
    opening = max(2.0 * side.edge("collar_line").length(0.05)
                  + vamp.edge("throat").length(0.05),
                  ankle_girth + foot_ease)
    collar = build_collar(opening)

    if everything or target_piece == "sole":
        pattern.add(sole)
    if everything or target_piece == "side":
        pattern.add(side)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "collar":
        pattern.add(collar)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything:
        # Each side panel's lower edge sews to one sole arc.
        pattern.declare_seam(("side", "sole_seam"), ("sole", "attach_out"), tol=1.5)
        pattern.declare_seam(("side", "sole_seam"), ("sole", "attach_in"), tol=1.5)
        # The vamp closes over the toes between the two side panels.
        pattern.declare_seam(("vamp", "side_r"), ("side", "vamp_seam"), tol=1.0)
        pattern.declare_seam(("vamp", "side_l"), ("side", "vamp_seam"), tol=1.0)
        # Centre back: the mirrored side panel sews to itself.
        pattern.declare_seam(("side", "centre_back"), ("side", "centre_back"), tol=0.5)
        # Collar binds both collar lines plus the vamp throat; its own joins and any
        # ankle clearance are carried as declared ease.
        collar_ease = (collar.edge("attach").length(0.05)
                       - 2.0 * side.edge("collar_line").length(0.05)
                       - vamp.edge("throat").length(0.05))
        pattern.declare_seam(
            [("collar", "attach")],
            [("side", "collar_line"), ("side", "collar_line"), ("vamp", "throat")],
            ease=collar_ease, tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.58)
    pattern.bom = [
        {"item": "fleece, boiled wool, or quilted cotton (shell)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 58% marker. Per PAIR, double this."},
        {"item": "non-slip sole fabric or suede", "qty": 2, "unit": "pcs",
         "note": "cut from the sole piece; a grippy underside for hard floors."},
        {"item": "wadding / batting (collar + optional lining)", "qty": 1, "unit": "as chosen",
         "note": "the collar is quilted between its fold and its quilt line."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "set the soles, close the centre back, bind the padded collar."},
    ]
    pattern.metadata = {
        "fc300_rank": 232, "family": "footwear_soft", "fabric_hint": "polar-lana",
        "silhouette_note": "An indoor bootie coming up over the ankle: a solved-lens "
            "sole, a side panel wrapping toe-to-heel-to-toe, a vamp closing the toes, "
            "and a padded quilted collar round the ankle opening.",
        "sizing_note": "ankle_girth IS a canonical ISO-8559 landmark and is claimed. "
            "foot_length is a PLAIN parameter — ISO 8559 as vendored declares no foot "
            "landmark codes, so none is invented.",
        "solved": {
            "sole_len_mm": round(SOLE_LEN, 1),
            "side_run_mm": round(SIDE_RUN, 1),
            "vamp_seam_mm": round(side.edge("vamp_seam").length(0.05), 1),
            "collar_opening_mm": round(opening, 1),
        },
    }
    return pattern


result = build()
