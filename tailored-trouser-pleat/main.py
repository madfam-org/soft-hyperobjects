"""
Double-Pleat Tailored Trouser — Fashion Cabinet Garment Cartridge
(FC-400 #316, tailoring, T3).

The dress trouser: two forward-facing pleats off the waist, a curtained
waistband closed by a trouser hook-and-bar (no button showing), a fly, and a
clean straight leg. The signature is the DOUBLE PLEAT reconciled with the
waistband, and the number that has to be right is how much cloth the pleats take
out of the waist so the finished band still measures the waist.

Three things are solved by measurement rather than by formula:

  1. THE TWO PLEATS ARE FOLDED OUT BEFORE THE WAIST IS MEASURED. Each pleat adds
     its own depth to the flat front waist; the waistband is cut to the FINISHED
     (folded) waist, which is the flat run less both pleat depths. A band cut to
     the flat run is loose by the sum of the two pleats on each front.

  2. THE HOOK-AND-BAR CLOSURE IS DIMENSIONALLY BRIDGED. The hook's span drives
     both the drafted overlap of the waistband ends AND the Yantra4D hook-bar's
     hook_width, so the printed hook matches the sewn overlap — the same number
     flows to the garment's edge and the hardware's sewn flange.

  3. THE TWO INSEAMS ARE BALANCED TO ZERO AND THE PLEATS CLAMPED. Front and back
     inseams must MEASURE the same or the leg twists; and each pleat depth is
     clamped so two deep pleats cannot together exceed the flat front waist and
     fold the panel through itself — geometry the kernel CCW-normalizes into a
     healthy-looking piece.

TAILORING CONVENTIONS: fine edge-stitch; a curtained waistband; hard goods via
Yantra4D. The TROUSER-HOOK-BAR SOLID is Yantra4D territory (`trouser-hook-bar`;
see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front_leg|back_leg|waistband|fly|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))
hip_girth = float(PARAM(lambda: hip_girth, 1020.0))
inside_leg = float(PARAM(lambda: inside_leg, 780.0))
front_rise = float(PARAM(lambda: front_rise, 280.0))
hem_width = float(PARAM(lambda: hem_width, 210.0))
band_depth = float(PARAM(lambda: band_depth, 38.0))
pleat1_depth = float(PARAM(lambda: pleat1_depth, 30.0))   # deep (forward) pleat
pleat2_depth = float(PARAM(lambda: pleat2_depth, 18.0))   # shallow (back) pleat
hook_span = float(PARAM(lambda: hook_span, 40.0))         # hook-bar overlap span
wear_ease = float(PARAM(lambda: wear_ease, 50.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))

waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(760.0, min(hip_girth, 1400.0))
inside_leg = max(600.0, min(inside_leg, 950.0))
front_rise = max(220.0, min(front_rise, 380.0))
hem_width = max(160.0, min(hem_width, 320.0))
band_depth = max(28.0, min(band_depth, 55.0))
pleat1_depth = max(0.0, min(pleat1_depth, 60.0))
pleat2_depth = max(0.0, min(pleat2_depth, 50.0))
hook_span = max(24.0, min(hook_span, 70.0))
wear_ease = max(0.0, min(wear_ease, 140.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(28.0, min(hem_allowance, 70.0))

TOPSTITCH = 6.0

QUARTER_HIP = (hip_girth + wear_ease) / 4.0
BACK_RISE = max(front_rise + 45.0, front_rise * 1.13)
_QUARTER_WAIST_RAW = (waist_girth + wear_ease) / 4.0
QUARTER_WAIST = max(QUARTER_HIP * 0.62, min(_QUARTER_WAIST_RAW, QUARTER_HIP - 6.0))
HALF_HEM = hem_width / 2.0
FORK_F = max(20.0, QUARTER_HIP * 0.13)
FORK_B = max(34.0, QUARTER_HIP * 0.21)
FLY_LAP = max(30.0, 50.0)

# The two pleats, each clamped so together they cannot exceed the flat front
# waist and fold the panel through itself.
_PLEAT_TOTAL_RAW = pleat1_depth + pleat2_depth
MAX_PLEAT_TOTAL = max(0.0, QUARTER_WAIST * 0.7)
if _PLEAT_TOTAL_RAW > MAX_PLEAT_TOTAL and _PLEAT_TOTAL_RAW > 0.0:
    _scale = MAX_PLEAT_TOTAL / _PLEAT_TOTAL_RAW
    PLEAT1 = pleat1_depth * _scale
    PLEAT2 = pleat2_depth * _scale
else:
    PLEAT1 = pleat1_depth
    PLEAT2 = pleat2_depth
PLEAT_TOTAL = PLEAT1 + PLEAT2
# The flat front waist edge carries the finished waist plus both pleat depths.
FLAT_FRONT_WAIST = QUARTER_WAIST + PLEAT_TOTAL


def _front_inseam(bulge):
    return fc.Edge("inseam", [fc.curve_through(
        fc.P(QUARTER_HIP + FORK_F, front_rise), fc.P(HALF_HEM, 0.0),
        bulge=bulge, side=-1.0)])


_BACK_INSEAM = fc.Edge("inseam", [fc.curve_through(
    fc.P(QUARTER_HIP + FORK_B, BACK_RISE), fc.P(HALF_HEM, 0.0), bulge=0.0, side=-1.0)])
_BACK_INSEAM_LEN = _BACK_INSEAM.length(0.05)


def _solve_front_bulge():
    lo, hi = 0.0, 0.45
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if _front_inseam(mid).length(0.05) < _BACK_INSEAM_LEN:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


BULGE = _solve_front_bulge()
_FRONT_INSEAM_LEN = _front_inseam(BULGE).length(0.05)


def build_front_leg():
    """Front leg, cut 2 mirrored. Two waist pleats folded out."""
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(FLAT_FRONT_WAIST, front_rise)
    p_fork = fc.P(QUARTER_HIP + FORK_F, front_rise)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 6.0, front_rise - front_rise * 0.44),
            fc.P(QUARTER_HIP + FORK_F * 0.35, front_rise * 0.18), p_fork)]),
        _front_inseam(BULGE),
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    px1 = FLAT_FRONT_WAIST * 0.30
    px2 = FLAT_FRONT_WAIST * 0.55
    internals = [
        fc.Internal("crease line",
                    [fc.P(HALF_HEM * 0.5, 0.0), fc.P(FLAT_FRONT_WAIST * 0.42, front_rise)],
                    kind="marking"),
        fc.Internal("pleat 1 (fold out)",
                    [fc.P(px1, front_rise), fc.P(px1, front_rise - 120.0)],
                    kind="marking"),
        fc.Internal("pleat 1 (fold to)",
                    [fc.P(px1 + PLEAT1, front_rise), fc.P(px1 + PLEAT1, front_rise - 120.0)],
                    kind="marking"),
        fc.Internal("pleat 2 (fold out)",
                    [fc.P(px2, front_rise), fc.P(px2, front_rise - 100.0)],
                    kind="marking"),
        fc.Internal("pleat 2 (fold to)",
                    [fc.P(px2 + PLEAT2, front_rise), fc.P(px2 + PLEAT2, front_rise - 100.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF / fly match"),
                 fc.Notch("inseam", 0.5, "inseam balance"),
                 fc.Notch("waist", 0.30, "pleat 1"),
                 fc.Notch("waist", 0.55, "pleat 2")],
        grainline=fc.Grainline(fc.P(FLAT_FRONT_WAIST * 0.42, inside_leg * 0.08),
                               fc.P(FLAT_FRONT_WAIST * 0.42, front_rise * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front leg (cut 2, mirrored)",
    )


def build_back_leg():
    """Back leg, cut 2 mirrored. A back dart; the rise carried at CB."""
    p_hem_side = fc.P(0.0, 0.0)
    p_waist_side = fc.P(0.0, front_rise)
    p_waist_in = fc.P(QUARTER_WAIST + 20.0, BACK_RISE)   # +dart intake
    p_fork = fc.P(QUARTER_HIP + FORK_B, BACK_RISE)
    edges = [
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        fc.Edge("waist", [fc.Line(p_waist_side, p_waist_in)]),
        fc.Edge("crotch", [fc.Bezier(
            p_waist_in, fc.P(QUARTER_HIP - 6.0, BACK_RISE - BACK_RISE * 0.44),
            fc.P(QUARTER_HIP + FORK_B * 0.35, BACK_RISE * 0.18), p_fork)]),
        _BACK_INSEAM,
        fc.Edge("hem", [fc.Line(fc.P(HALF_HEM, 0.0), p_hem_side)]),
    ]
    return fc.Piece(
        "back_leg", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CB match"),
                 fc.Notch("inseam", 0.5, "inseam balance")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.42, inside_leg * 0.08),
                               fc.P(QUARTER_HIP * 0.42, BACK_RISE * 0.9)),
        internals=[
            fc.Internal("back dart",
                        [fc.P(QUARTER_WAIST * 0.55, BACK_RISE),
                         fc.P(QUARTER_WAIST * 0.55 - 10.0, BACK_RISE - 110.0),
                         fc.P(QUARTER_WAIST * 0.55 + 10.0, BACK_RISE - 110.0),
                         fc.P(QUARTER_WAIST * 0.55, BACK_RISE)], kind="marking"),
            fc.Internal("welt pocket",
                        [fc.P(QUARTER_WAIST * 0.3, BACK_RISE - 60.0),
                         fc.P(QUARTER_WAIST * 0.3 + 130.0, BACK_RISE - 60.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back leg (cut 2, mirrored)",
    )


_FL = build_front_leg()
_BL = build_back_leg()
FLAT_FRONT_RUN = _FL.edge("waist").length(0.05)
FINISHED_FRONT_RUN = FLAT_FRONT_RUN - PLEAT_TOTAL
BACK_WAIST_RUN = _BL.edge("waist").length(0.05)
# The band is cut to the finished waist plus the hook overlap span.
BAND_LENGTH = 2.0 * FINISHED_FRONT_RUN + 2.0 * BACK_WAIST_RUN - seam_allowance + hook_span
BAND_CUT_H = band_depth * 2.0 + 2.0 * seam_allowance


def build_waistband():
    """Curtained waistband, cut 1. Closed by the hook-and-bar over the overlap."""
    ln = BAND_LENGTH
    w = BAND_CUT_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("hook_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("bar_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "waistband", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.5, "CB"),
                 fc.Notch("lower", 1.0 - hook_span / ln, "hook overlap start")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("hook placement",
                        [fc.P(ln - seam_allowance - hook_span * 0.5, w / 2.0)],
                        kind="drill"),
            fc.Internal("bar placement",
                        [fc.P(seam_allowance + hook_span * 0.5, w / 2.0)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Curtained waistband (cut 1)",
    )


def build_fly():
    lap = FLY_LAP
    depth = max(80.0, front_rise - band_depth - 20.0)
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(lap, depth))]),
        fc.Edge("curve", [fc.curve_through(
            fc.P(lap, depth), fc.P(0.0, 0.0), bulge=0.30, side=1.0)]),
    ]
    return fc.Piece(
        "fly", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("cf", 1.0, "waistband join")],
        grainline=fc.Grainline(fc.P(lap * 0.4, depth * 0.15), fc.P(lap * 0.4, depth * 0.85)),
        internals=[
            fc.Internal("fly topstitch (J-stitch)",
                        [fc.P(lap * 0.5, depth - TOPSTITCH), fc.P(lap * 0.5, depth * 0.3),
                         fc.P(lap * 0.1, depth * 0.1)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Fly (cut 2)",
    )


def build():
    pattern = fc.PatternSet("tailored-trouser-pleat")
    everything = target_piece == "set"
    want = {
        "front_leg": everything or target_piece == "front_leg",
        "back_leg": everything or target_piece == "back_leg",
        "waistband": everything or target_piece == "waistband",
        "fly": everything or target_piece == "fly",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front_leg"]:
        pattern.add(build_front_leg())
    if want["back_leg"]:
        pattern.add(build_back_leg())
    if want["waistband"]:
        pattern.add(build_waistband())
    if want["fly"]:
        pattern.add(build_fly())

    if want["front_leg"] and want["back_leg"]:
        pattern.declare_seam(("front_leg", "inseam"), ("back_leg", "inseam"), tol=0.4)
        pattern.declare_seam(("front_leg", "side"), ("back_leg", "side"), tol=1.0)
        pattern.declare_seam(("front_leg", "hem"), ("back_leg", "hem"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "wool worsted, 280 gsm (dress trouser)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker."},
        {"item": "trouser hook and bar (set)", "qty": 1, "unit": "set",
         "note": f"Yantra4D trouser-hook-bar (notion.hardware_ref); the hook_width "
                 f"is fed from this garment's hook_span ({hook_span:.0f} mm), the "
                 f"same number that drafts the waistband overlap. No button shows."},
        {"item": "fly zipper", "qty": 1, "unit": "piece",
         "note": "the fly closes on a zip under the hook-and-bar band; a companion "
                 "hard good, not the bridged one."},
        {"item": "fine edge-stitch thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"{TOPSTITCH:.0f} mm on the fly J-stitch and the crease."},
    ]
    pattern.metadata = {
        "fc400_rank": 316,
        "family": "tailoring",
        "tier": 3,
        "fabric_hint": "wool-worsted",
        "finished_mm": {
            "quarter_hip": round(QUARTER_HIP, 1),
            "quarter_waist": round(QUARTER_WAIST, 1),
            "front_rise": round(front_rise, 1),
            "back_rise": round(BACK_RISE, 1),
            "hem_width": round(hem_width, 1),
            "band_length": round(BAND_LENGTH, 1),
            "pleat1_depth": round(PLEAT1, 1),
            "pleat2_depth": round(PLEAT2, 1),
        },
        "solved": {
            "front_inseam_measured_mm": round(_FRONT_INSEAM_LEN, 2),
            "back_inseam_measured_mm": round(_BACK_INSEAM_LEN, 2),
            "inseam_delta_mm": round(abs(_FRONT_INSEAM_LEN - _BACK_INSEAM_LEN), 4),
            "flat_front_waist_run_mm": round(FLAT_FRONT_RUN, 2),
            "pleat_total_requested_mm": round(_PLEAT_TOTAL_RAW, 2),
            "pleat_total_clamped_mm": round(PLEAT_TOTAL, 2),
            "pleat_total_was_clamped": bool(abs(PLEAT_TOTAL - _PLEAT_TOTAL_RAW) > 0.01),
            "finished_front_waist_run_mm": round(FINISHED_FRONT_RUN, 2),
            "band_length_measured_mm": round(BAND_LENGTH, 2),
            "hook_span_mm": round(hook_span, 2),
            "note": "the two pleats are FOLDED OUT before the waist is measured, so "
                    "the band is cut to the finished (folded) waist plus the hook "
                    "overlap span, never the flat run — a band cut flat is loose by "
                    "both pleats on each front. The pleat depths are together "
                    "clamped so they cannot exceed the flat front waist and fold "
                    "the panel through itself. The inseams are balanced to zero.",
        },
        "hardware": "trouser hook-and-bar via Yantra4D (notion.hardware_ref -> "
                    "trouser-hook-bar); the solid's hook_width — the sewn flange "
                    "dimension — is fed from this garment's hook_span, which ALSO "
                    "drafts the waistband overlap, so the same number flows to both "
                    "the garment's edge and the hardware's sewn edge.",
    }
    return pattern


result = build()
