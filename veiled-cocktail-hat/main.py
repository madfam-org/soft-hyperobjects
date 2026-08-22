"""
Veiled Cocktail Hat — Fashion Cabinet Garment Cartridge (FC-300 #214, Lane 2).

A small perched cocktail hat with a birdcage veil: a shallow gored CROWN on a short
SIDE BAND, and a wide VEIL panel gathered down onto a Yantra4D `veil-comb` bar.

The bridge is DIMENSIONAL through the gather. The veil is cut `gather_ratio` times
wider than the comb bar; its gathered edge therefore finishes at exactly `bar_length`,
which is the run the comb's `veil_gather_bar` flange presents. So one garment
parameter — `bar_length` — drives both the hardware's sewn edge and the garment's own
`veil_heading` interface. The `gather_line` internal marks where the fullness is
controlled down to that finished run.

Pieces:
  - crown-gore : a gore of the shallow crown, cut `gores` (mirrored).
  - side-band  : the short cylindrical wall, cut 1.
  - veil       : the birdcage veil panel, cut on fold + mirrored.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # crown|side-band|veil|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
crown_dia = float(PARAM(lambda: crown_dia, 150.0))     # the perched crown's diameter
band_height = float(PARAM(lambda: band_height, 34.0))
gores = int(PARAM(lambda: gores, 6))
bar_length = float(PARAM(lambda: bar_length, 80.0))    # the Yantra4D comb bar run
veil_drop = float(PARAM(lambda: veil_drop, 220.0))
gather_ratio = float(PARAM(lambda: gather_ratio, 2.4))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
crown_dia = max(80.0, min(crown_dia, 260.0))
band_height = max(15.0, min(band_height, 80.0))
gores = max(4, min(gores, 10))
bar_length = max(40.0, min(bar_length, 140.0))
veil_drop = max(80.0, min(veil_drop, 420.0))
gather_ratio = max(1.5, min(gather_ratio, 4.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

CROWN_CIRC = math.pi * crown_dia       # the crown/band run
gore_base = CROWN_CIRC / gores
GB = gore_base / 2.0
CROWN_RISE = crown_dia * 0.28          # a shallow perched dome

# The veil is cut full and gathered DOWN to the comb bar's run.
VEIL_FLAT_HALF = (bar_length * gather_ratio) / 2.0   # half-width, cut on fold


def _build_gore():
    """One gore of the shallow perched crown."""
    apex = fc.P(0.0, CROWN_RISE)
    left = fc.Bezier(fc.P(-GB, 0.0), fc.P(-GB * 0.95, CROWN_RISE * 0.45),
                     fc.P(-GB * 0.42, CROWN_RISE * 0.88), apex)
    right = fc.Bezier(apex, fc.P(GB * 0.42, CROWN_RISE * 0.88),
                      fc.P(GB * 0.95, CROWN_RISE * 0.45), fc.P(GB, 0.0))
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(GB, 0.0), fc.P(-GB, 0.0))]),
        fc.Edge("seam_l", [left]),
        fc.Edge("seam_r", [right]),
    ]
    return fc.Piece(
        "crown-gore",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, CROWN_RISE * 0.1), fc.P(0.0, CROWN_RISE * 0.85)),
        cut=fc.CutSpec(quantity=gores, mirror=True),
        label="Crown gore",
    )


def _build_side_band():
    """The short wall the crown sits on; it wraps into a ring."""
    w, h = CROWN_CIRC, band_height
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("crown_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("join_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("lower", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "side-band",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown_edge", 0.5, "centre front"),
                 fc.Notch("lower", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Side band",
    )


def _build_veil():
    """The birdcage veil: a wide panel cut on the fold at centre front. Its `heading`
    edge is the FLAT (ungathered) run; gathered at `gather_ratio` it finishes at half
    the comb bar, and the mirrored pair finishes at the full bar_length."""
    hw, dr = VEIL_FLAT_HALF, veil_drop
    # The lower edge sweeps out and down — a birdcage veil is wider at the hem.
    hem_out = hw * 1.18
    edges = [
        fc.Edge("centre_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, dr))]),
        fc.Edge("heading", [fc.Line(fc.P(0.0, dr), fc.P(hw, dr))]),   # gathers to the comb
        fc.Edge("side", [fc.Line(fc.P(hw, dr), fc.P(hem_out, 0.0))]),
        fc.Edge("hem", [fc.curve_through(fc.P(hem_out, 0.0), fc.P(0.0, 0.0),
                                         bulge=0.12, side=-1.0)]),
    ]
    internals = [
        fc.Internal("gather_line", [fc.P(0.0, dr - 12.0), fc.P(hw, dr - 12.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "veil",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0},          # birdcage netting is cut raw, never hemmed
        notches=[fc.Notch("heading", 0.5, "gather midpoint")],
        grainline=fc.Grainline(fc.P(hw * 0.5, dr * 0.15), fc.P(hw * 0.5, dr * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Birdcage veil",
    )


def _build_comb_casing():
    """The narrow self-fabric casing that binds the gathered veil heading onto the
    comb's bar. Its `bar` edge measures bar_length exactly — this is the garment edge
    that mates the Yantra4D comb's veil_gather_bar flange."""
    ln, w = bar_length, 26.0
    edges = [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("bar", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),   # takes the gathered veil
        fc.Edge("end_b", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("fold_back", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "comb-casing",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bar", 0.5, "comb centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Comb casing",
    )


def build():
    pattern = fc.PatternSet("veiled-cocktail-hat")
    everything = target_piece == "set"

    if everything or target_piece == "crown":
        pattern.add(_build_gore())
    if everything or target_piece == "side-band":
        pattern.add(_build_side_band())
    if everything or target_piece == "veil":
        pattern.add(_build_veil())
        pattern.add(_build_comb_casing())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if "crown-gore" in names:
        pattern.declare_seam(("crown-gore", "seam_l"), ("crown-gore", "seam_r"), tol=1.0)
    if {"crown-gore", "side-band"} <= names:
        pattern.declare_seam([("crown-gore", "bottom")] * gores,
                             ("side-band", "crown_edge"), tol=1.5)
    if "side-band" in names:
        pattern.declare_seam(("side-band", "join_a"), ("side-band", "join_b"), tol=1.0)
    if {"veil", "comb-casing"} <= names:
        # THE GATHER, declared as a real seam with ease. The veil is cut on the fold, so
        # the mirrored pair's flat heading run is 2 * VEIL_FLAT_HALF =
        # bar_length * gather_ratio. It is gathered down onto the comb casing, whose
        # `bar` edge measures bar_length — the run the comb's veil_gather_bar flange
        # presents. The ease IS the fullness removed by gathering, so the check is
        # substantive: flat_run == bar_length + removed, and it fails if gather_ratio,
        # bar_length or the casing ever drift apart.
        removed = bar_length * (gather_ratio - 1.0)
        pattern.declare_seam([("veil", "heading"), ("veil", "heading")],
                             ("comb-casing", "bar"), tol=1.0, ease=removed)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "crown fabric (silk faille, satin or velvet)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 55% marker; block-fuse the crown."},
        {"item": "birdcage veiling (Russian net, 9 mm mesh)",
         "qty": round(bar_length * gather_ratio / 10.0) * 10, "unit": "mm_length",
         "note": "cut wide and gathered down to the comb bar; the hem is left raw."},
        {"item": "veil comb", "qty": 1, "unit": "count",
         "note": "Yantra4D veil-comb (see notion.hardware_ref) — the veil's gathered "
                 "heading is bound onto its bar, sized by bar_length."},
        {"item": "millinery thread + buckram", "qty": 1, "unit": "set",
         "note": "the perched crown needs a stiffened base to hold its angle."},
    ]
    pattern.metadata = {
        "fc300_rank": 214, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "crown_dia_mm": round(crown_dia, 1),
        "crown_circumference_mm": round(CROWN_CIRC, 2),
        "gores": gores,
        "bar_length_mm": round(bar_length, 1),
        "veil_drop_mm": round(veil_drop, 1),
        "gather_ratio": round(gather_ratio, 2),
        "drafting": "shallow gored crown + short side band + gathered birdcage veil",
        "hardware": "veil mounting delegated to Yantra4D veil-comb; the veil's gathered "
                    "heading finishes at bar_length (the veil_gather_bar flange run)",
        "solved": {
            "veil_flat_run_mm": round(bar_length * gather_ratio, 3),
            "veil_finished_run_mm": round(bar_length, 3),
            "gather_removed_mm": round(bar_length * (gather_ratio - 1.0), 3),
            "gore_bases_total_mm": round(gore_base * gores, 3),
        },
    }
    return pattern


result = build()
