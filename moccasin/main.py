"""
Moccasin — Fashion Cabinet Garment Cartridge (FC-300 #229, lane 4 footwear).

The classic plug-vamp moccasin: a single `vamp` wrapped UP from under the foot (the true
moccasin construction — one piece of leather that is the sole and the sides at once), a
`plug` (the apron / "tongue" panel) set into the vamp's gathered throat, and a `collar`
band round the ankle opening.

The moccasin's signature is its seam: the plug is joined to the vamp with a WHIPSTITCH
(an over-the-edge stitch through both edges, not a turned seam), which gathers the vamp's
longer throat edge onto the plug's shorter one. That gather is declared honestly as seam
`ease` — the vamp throat is INTENTIONALLY longer than the plug it sews to, and the
declared seam records exactly how much.

SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json declares NO foot landmark codes. This
cartridge drafts from PLAIN sized parameters (foot_length, foot_girth carry no
`measurement` block). No landmark code is invented. `ankle_girth` IS canonical and IS
used — the collar genuinely reaches the ankle.

Pieces:
  - vamp   : the wrap-up sole+sides (cut 1 on fold at centre line, mirrored).
  - plug   : the apron panel (cut 1), whipstitched into the vamp throat.
  - collar : the ankle band (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # vamp|plug|collar|set

# Sized params (NOT ISO-8559 landmarks — the schema has no foot codes).
foot_length = float(PARAM(lambda: foot_length, 255.0))
foot_girth = float(PARAM(lambda: foot_girth, 235.0))
# ankle_girth IS a canonical ISO-8559 landmark code and the collar does reach it.
ankle_girth = float(PARAM(lambda: ankle_girth, 245.0))

plug_width = float(PARAM(lambda: plug_width, 62.0))       # apron panel width
plug_length = float(PARAM(lambda: plug_length, 130.0))    # apron panel length
gather_ratio = float(PARAM(lambda: gather_ratio, 1.22))   # vamp throat / plug edge
collar_height = float(PARAM(lambda: collar_height, 52.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
ankle_girth = max(160.0, min(ankle_girth, 340.0))
plug_width = max(35.0, min(plug_width, 110.0))
plug_length = max(70.0, min(plug_length, 210.0))
gather_ratio = max(1.0, min(gather_ratio, 1.6))
collar_height = max(25.0, min(collar_height, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
# The vamp is cut on the fold along the foot's centre line: flat, it is the sole plus
# both sides opened out. Its half-width is half the ball girth plus the wrap-up.
VAMP_HALF = foot_girth / 2.0 / 2.0 + 14.0
VAMP_LEN = foot_length + 18.0


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


def build_plug():
    """The apron panel. Its two long sides are whipstitched into the vamp throat;
    its front is the toe end, its back the throat mouth at the collar."""
    hw = plug_width / 2.0
    ln = plug_length
    return fc.Piece(
        "plug",
        [
            # front (toe end): a small round
            fc.Edge("front", [fc.curve_through(fc.P(-hw * 0.6, 0.0), fc.P(hw * 0.6, 0.0),
                                               bulge=0.30, side=-1.0)]),
            fc.Edge("side_r", [fc.curve_through(fc.P(hw * 0.6, 0.0), fc.P(hw, ln),
                                                bulge=0.06, side=-1.0)]),
            fc.Edge("throat", [fc.Line(fc.P(hw, ln), fc.P(-hw, ln))]),
            fc.Edge("side_l", [fc.curve_through(fc.P(-hw, ln), fc.P(-hw * 0.6, 0.0),
                                                bulge=0.06, side=-1.0)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front", 0.5, "centre toe"),
                 fc.Notch("side_r", 0.5, "gather midpoint"),
                 fc.Notch("side_l", 0.5, "gather midpoint")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, ln - 8.0)),
        internals=[fc.Internal("centre-line",
                               [fc.P(0.0, 0.0), fc.P(0.0, ln)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Plug (apron panel)",
    )


def build_vamp(plug_side_len):
    """The wrap-up sole+sides, cut on the fold at the foot's centre line.

    Flat, it runs from the toe (bottom) to the heel (top). Its `throat` edge is
    SOLVED to gather_ratio x the plug's side edge: the whipstitch gathers that extra
    length onto the plug, and the declared seam carries it as honest `ease`.
    """
    w = VAMP_HALF
    ln = VAMP_LEN
    throat_target = plug_side_len * gather_ratio
    p_toe = fc.P(0.0, 0.0)                      # centre toe (on the fold line)
    # The throat runs up the outer side from the toe to where the plug ends. Its
    # chord must stay SHORTER than the solved target (an arc is always longer than
    # its chord), so the end point is placed on the throat budget rather than on
    # plug_length alone — a short plug with no gather would otherwise demand a
    # straight-line throat longer than the seam it sews to.
    end_x, end_y = w * 0.92, plug_length * 0.98
    chord = (end_x ** 2 + end_y ** 2) ** 0.5
    budget = throat_target * 0.90          # leave the arc room to bow out
    if chord > budget:                     # scale the whole vector back along its line
        end_x, end_y = end_x * budget / chord, end_y * budget / chord
    p_throat_end = fc.P(end_x, end_y)
    p_heel_top = fc.P(w * 0.62, ln)
    return fc.Piece(
        "vamp",
        [
            # centre_line is the fold: from the heel top back down to the toe
            fc.Edge("centre_line", [fc.Line(fc.P(0.0, ln), p_toe)]),
            _arc("throat", p_toe, p_throat_end, throat_target, side=-1.0),
            fc.Edge("back_side", [fc.Line(p_throat_end, p_heel_top)]),
            fc.Edge("collar_line", [fc.Line(p_heel_top, fc.P(0.0, ln))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"collar_line": 10.0},
        notches=[fc.Notch("throat", 0.5, "gather midpoint"),
                 fc.Notch("collar_line", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.35, 12.0), fc.P(w * 0.35, ln - 12.0)),
        internals=[fc.Internal("sole-line",
                               [fc.P(w * 0.30, 6.0), fc.P(w * 0.30, ln - 6.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="centre_line", mirror=True),
        label="Vamp (wrap-up sole + sides)",
    )


def build_collar(opening):
    """The ankle band. Length is the measured collar opening plus its own joins."""
    band_len = opening + 2.0 * seam_allowance
    band_h = collar_height
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
        cut=fc.CutSpec(quantity=1),
        label="Collar (ankle band)",
    )


def build():
    pattern = fc.PatternSet("moccasin")
    everything = target_piece == "set"

    plug = build_plug()
    plug_side = plug.edge("side_r").length(0.05)
    vamp = build_vamp(plug_side)
    # The collar binds the vamp's collar line (doubled — cut on fold), eased to the
    # ankle where the two disagree.
    opening = max(2.0 * vamp.edge("collar_line").length(0.05), ankle_girth * 0.55)
    collar = build_collar(opening)

    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "plug":
        pattern.add(plug)
    if everything or target_piece == "collar":
        pattern.add(collar)

    # ── Declared seams (the whipstitch pair + the collar attach) ────────────
    if everything:
        # WHIPSTITCH, right side: the vamp throat is gathered onto the plug's side.
        # The extra length is declared as ease, not hidden — that gather IS the
        # moccasin's construction, and verification records its exact amount.
        gather_r = vamp.edge("throat").length(0.05) - plug.edge("side_r").length(0.05)
        pattern.declare_seam([("vamp", "throat")], [("plug", "side_r")],
                             ease=gather_r, tol=1.0)
        # WHIPSTITCH, left side: the vamp is cut on the fold, so its single throat
        # edge is mirrored — the same run gathers onto the plug's other side.
        gather_l = vamp.edge("throat").length(0.05) - plug.edge("side_l").length(0.05)
        pattern.declare_seam([("vamp", "throat")], [("plug", "side_l")],
                             ease=gather_l, tol=1.0)
        # Collar attach: binds the doubled collar line, plus the plug's throat mouth.
        collar_ease = (collar.edge("attach").length(0.05)
                       - 2.0 * vamp.edge("collar_line").length(0.05))
        pattern.declare_seam(
            [("collar", "attach")],
            [("vamp", "collar_line"), ("vamp", "collar_line")],
            ease=collar_ease, tol=1.5)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.50)
    pattern.bom = [
        {"item": "soft garment leather, elk, or moose hide (2-3 oz)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1200 mm width, 50% marker — hide is irregular, cut generously. "
                 "Per PAIR, double this."},
        {"item": "waxed sinew or heavy linen thread", "qty": 1, "unit": "spool",
         "note": "the whipstitch that gathers the vamp throat onto the plug."},
        {"item": "glover's / harness needles", "qty": 2, "unit": "pcs",
         "note": "a three-sided glover's point pierces hide without tearing it."},
        {"item": "sole leather or crepe (optional)", "qty": 2, "unit": "pcs",
         "note": "a stitched-on outsole if the moccasin is worn outdoors."},
    ]
    pattern.metadata = {
        "fc300_rank": 229, "family": "footwear_soft", "fabric_hint": "piel-suave",
        "silhouette_note": "The classic plug-vamp moccasin: one piece of hide wrapped "
            "up from under the foot to be sole and sides at once, an apron plug set "
            "into the gathered throat with a whipstitch, and an ankle collar band.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO "
            "8559 (as vendored) declares no foot landmark codes, so none is claimed or "
            "invented. ankle_girth IS canonical and is used for the collar.",
        "construction_note": "The vamp throat is drafted LONGER than the plug side by "
            "gather_ratio; the whipstitch takes up that difference. Both throat seams "
            "declare it as explicit ease rather than pretending the edges match.",
        "solved": {
            "vamp_half_mm": round(VAMP_HALF, 1),
            "plug_side_mm": round(plug_side, 1),
            "vamp_throat_mm": round(vamp.edge("throat").length(0.05), 1),
            "gather_ratio": round(gather_ratio, 3),
            "collar_opening_mm": round(opening, 1),
        },
    }
    return pattern


result = build()
