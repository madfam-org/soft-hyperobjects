"""
Deerstalker Cap — Fashion Cabinet Garment Cartridge (FC-300 #218, Lane 2).

The deerstalker: a FOUR-GORE crown, TWO PEAKS (front and rear, the cap's defining
feature), and EAR FLAPS that either cover the ears or fold up and tie across the
crown. A pure soft-goods garment — no hardware; the flaps tie with self-fabric tapes.

Pieces:
  - crown-gore : one of `gores` crown panels, cut `gores` (mirrored).
  - headband   : the inner band at the head line, cut 1.
  - peak       : the front/rear peak, cut on fold + mirrored, cut for both ends.
  - ear-flap   : the ear flap, cut 2 mirrored.
  - flap-tie   : the tape that ties the flaps over the crown, cut 2.

Drafting notes:
  * The gore bases sum to the head opening, so `gores` bases sewn together measure the
    headband exactly.
  * The two peaks together consume the front and rear thirds of the head line; the
    ear flaps take the two side spans. Those four runs are declared against the
    headband's head edge so the flaps and peaks provably tile the head line.
  * Peaks are cut on the fold, so a peak's drafted back edge is HALF its span and is
    listed twice (the piece against its own mirror, join-to-join).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # crown|headband|peak|flap|tie|set

head_girth = float(PARAM(lambda: head_girth, 580.0))
crown_height = float(PARAM(lambda: crown_height, 120.0))
peak_length = float(PARAM(lambda: peak_length, 68.0))
flap_drop = float(PARAM(lambda: flap_drop, 95.0))
gores = int(PARAM(lambda: gores, 4))
headband_height = float(PARAM(lambda: headband_height, 34.0))
ease = float(PARAM(lambda: ease, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
crown_height = max(80.0, min(crown_height, 180.0))
peak_length = max(35.0, min(peak_length, 110.0))
flap_drop = max(50.0, min(flap_drop, 170.0))
gores = max(4, min(gores, 8))
headband_height = max(18.0, min(headband_height, 60.0))
ease = max(0.0, min(ease, 30.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

head_eff = head_girth + ease          # the finished head opening
gore_base = head_eff / gores
GB = gore_base / 2.0

# The head line is tiled by two peaks (front + rear) and two ear flaps (the sides).
PEAK_SPAN = head_eff * 0.28           # each peak's share of the head line
PEAK_HALF = PEAK_SPAN / 2.0           # drafted on the fold
FLAP_SPAN = (head_eff - 2.0 * PEAK_SPAN) / 2.0   # each side span the flaps cover


def _build_gore():
    """A crown gore: base `gore_base` at y=0, two Bezier seams to a shared apex."""
    apex = fc.P(0.0, crown_height)
    left = fc.Bezier(fc.P(-GB, 0.0), fc.P(-GB * 0.96, crown_height * 0.44),
                     fc.P(-GB * 0.43, crown_height * 0.87), apex)
    right = fc.Bezier(apex, fc.P(GB * 0.43, crown_height * 0.87),
                      fc.P(GB * 0.96, crown_height * 0.44), fc.P(GB, 0.0))
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
        grainline=fc.Grainline(fc.P(0.0, crown_height * 0.1), fc.P(0.0, crown_height * 0.85)),
        cut=fc.CutSpec(quantity=gores, mirror=True),
        label="Crown gore",
    )


def _build_headband():
    """The inner band at the head line; it wraps to a ring and carries the peaks and
    flaps around its lower edge."""
    w, h = head_eff, headband_height
    internals = [
        fc.Internal("peak_front", [fc.P(w * 0.5 - PEAK_HALF, 0.0),
                                   fc.P(w * 0.5 + PEAK_HALF, 0.0)], kind="marking"),
        fc.Internal("peak_rear", [fc.P(0.0, 0.0), fc.P(PEAK_HALF, 0.0)], kind="marking"),
    ]
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("crown_edge", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),   # to the gores
        fc.Edge("join_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("head_line", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),  # peaks + flaps
    ]
    return fc.Piece(
        "headband",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown_edge", 0.5, "centre front"),
                 fc.Notch("head_line", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Headband",
    )


def _build_peak():
    """A peak (front and rear are the same piece, cut twice over): a half-ellipse cut
    on the straight back edge and mirrored. Its drafted `back` edge is HALF the peak
    span."""
    hw, pl = PEAK_HALF, peak_length
    front = fc.Bezier(fc.P(0.0, pl), fc.P(hw * 0.55, pl * 0.96),
                      fc.P(hw * 0.92, pl * 0.55), fc.P(hw, 0.0))
    edges = [
        fc.Edge("centre", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, pl))]),
        fc.Edge("front", [front]),
        fc.Edge("back", [fc.Line(fc.P(hw, 0.0), fc.P(0.0, 0.0))]),   # to the head line
    ]
    return fc.Piece(
        "peak",
        edges,
        seam_allowance=seam_allowance,
        allowances={"front": 6.0},
        notches=[fc.Notch("back", 0.5, "peak quarter")],
        grainline=fc.Grainline(fc.P(hw * 0.35, pl * 0.15), fc.P(hw * 0.35, pl * 0.75)),
        cut=fc.CutSpec(quantity=4, on_fold=True, fold_edge="centre", mirror=True),
        label="Peak (front & rear)",
    )


def _build_ear_flap():
    """An ear flap: its `head_edge` takes one side span of the head line, and it drops
    `flap_drop` to a rounded lower edge."""
    w, d = FLAP_SPAN, flap_drop
    edges = [
        fc.Edge("head_edge", [fc.Line(fc.P(0.0, d), fc.P(w, d))]),
        fc.Edge("back", [fc.Line(fc.P(w, d), fc.P(w * 0.86, 0.0))]),
        fc.Edge("lower", [fc.curve_through(fc.P(w * 0.86, 0.0), fc.P(w * 0.14, 0.0),
                                           bulge=0.18, side=1.0)]),
        fc.Edge("front", [fc.Line(fc.P(w * 0.14, 0.0), fc.P(0.0, d))]),
    ]
    return fc.Piece(
        "ear-flap",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("head_edge", 0.5, "ear point")],
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.15), fc.P(w * 0.5, d * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Ear flap",
    )


def _build_flap_tie():
    """The self-fabric tape that ties the folded-up flaps across the crown."""
    ln, w = head_eff * 0.42, 24.0
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("long_a", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("long_b", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "flap-tie",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=2),
        label="Flap tie",
    )


def build():
    pattern = fc.PatternSet("deerstalker-cap")
    everything = target_piece == "set"

    if everything or target_piece == "crown":
        pattern.add(_build_gore())
    if everything or target_piece == "headband":
        pattern.add(_build_headband())
    if everything or target_piece == "peak":
        pattern.add(_build_peak())
    if everything or target_piece == "flap":
        pattern.add(_build_ear_flap())
    if everything or target_piece == "tie":
        pattern.add(_build_flap_tie())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if "crown-gore" in names:
        pattern.declare_seam(("crown-gore", "seam_l"), ("crown-gore", "seam_r"), tol=1.0)
    if {"crown-gore", "headband"} <= names:
        pattern.declare_seam([("crown-gore", "bottom")] * gores,
                             ("headband", "crown_edge"), tol=1.5)
    if "headband" in names:
        pattern.declare_seam(("headband", "join_a"), ("headband", "join_b"), tol=1.0)
    if {"headband", "peak", "ear-flap"} <= names:
        # The head line is TILED by the two peaks and the two ear flaps. Each peak is
        # cut on the fold, so its drafted `back` is a half span: two listings per peak,
        # four in all for the front and rear peaks, plus one head edge per flap.
        pattern.declare_seam(
            ("headband", "head_line"),
            [("peak", "back")] * 4 + [("ear-flap", "head_edge")] * 2,
            tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "shell fabric (wool tweed or herringbone)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 60% marker; a fulled tweed is traditional."},
        {"item": "lining fabric", "qty": 1, "unit": "set",
         "note": "quilted or plain — the flaps and peaks are all self-lined."},
        {"item": "peak stiffener", "qty": 2, "unit": "count",
         "note": "buckram or a PE insert per peak; the deerstalker has two."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "the flaps tie over the crown with the self-fabric tapes; no hardware."},
    ]
    pattern.metadata = {
        "fc300_rank": 218, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "gores": gores,
        "gore_base_mm": round(gore_base, 2),
        "crown_height_mm": round(crown_height, 1),
        "peak_length_mm": round(peak_length, 1),
        "peak_span_mm": round(PEAK_SPAN, 2),
        "flap_span_mm": round(FLAP_SPAN, 2),
        "flap_drop_mm": round(flap_drop, 1),
        "drafting": "four-gore crown + twin peaks on fold + ear flaps + ties",
        "solved": {
            "gore_bases_total_mm": round(gore_base * gores, 3),
            "headband_run_mm": round(head_eff, 3),
            "head_line_tiling_mm": round(2.0 * PEAK_SPAN + 2.0 * FLAP_SPAN, 3),
        },
    }
    return pattern


result = build()
