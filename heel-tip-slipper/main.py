"""
Heel-tip-blank slipper — Fashion Cabinet Cartridge (FC-500 #426, footwear_soft, T2).

A felted-wool house slipper with a hard-wearing HEEL: a soft VAMP over the toes and instep, a
felt SOLE, and a HEEL COUNTER that seats a printed heel-tip blank (the Yantra4D
`heel-tip-blank`) so the one part of a slipper that wears through — the heel — is a
replaceable hard tip rather than felt worn to the floor. The counter is sized to the tip
blank so it drops in and pins.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. Sized from
PLAIN parameters (foot_length, foot_girth); no landmark code is invented.

Solving and clamps (the FC-400 footwear idiom):
  - The vamp lasting edge is a SOLVED bow over its own chord (proportionate, never a share of
    the whole sole perimeter, which degenerates).
  - The heel counter's tip pocket is cut to the MEASURED tip blank plus a clearance, and its
    depth is clamped under the counter height so the pocket never runs through the topline.
  - The sole is drafted to the foot length and its heel end matches the counter width.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|sole|counter|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
vamp_depth = float(PARAM(lambda: vamp_depth, 105.0))
counter_height = float(PARAM(lambda: counter_height, 70.0))
tip_width = float(PARAM(lambda: tip_width, 55.0))
tip_length = float(PARAM(lambda: tip_length, 60.0))
tip_clear = float(PARAM(lambda: tip_clear, 3.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
vamp_depth = max(60.0, min(vamp_depth, 180.0))
counter_height = max(45.0, min(counter_height, 150.0))
tip_width = max(30.0, min(tip_width, 90.0))
tip_length = max(30.0, min(tip_length, 100.0))
tip_clear = max(1.0, min(tip_clear, 10.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

VAMP_HALF = max(24.0, foot_girth / 2.0 / 2.0 + 12.0)
VAMP_LAST = 2.0 * VAMP_HALF * 1.14
SOLE_HALF = max(30.0, foot_girth * 0.16)
TIP_POCKET_W = tip_width + tip_clear * 2.0
TIP_POCKET_L = tip_length + tip_clear * 2.0
# the tip pocket depth clamped under the counter height
POCKET_DEPTH = min(TIP_POCKET_L, counter_height - 15.0)
POCKET_DEPTH = max(20.0, POCKET_DEPTH)
SEGS = 34


def _arc(name, p0, p1, target, side):
    def mk(bulge):
        return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])
    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} < chord {chord:.1f}")
    lo, hi = 0.0, 3.0
    if mk(hi).length(0.05) < target:
        raise ValueError(f"{name}: unreachable")
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if mk(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    return mk((lo + hi) / 2.0)


def build_vamp():
    h = vamp_depth
    p_ll = fc.P(-VAMP_HALF, 0.0)
    p_lr = fc.P(VAMP_HALF, 0.0)
    p_tr = fc.P(VAMP_HALF * 0.78, h)
    p_tl = fc.P(-VAMP_HALF * 0.78, h)
    return fc.Piece(
        "vamp", [
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("collar", [fc.curve_through(p_tr, p_tl, bulge=0.14, side=1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"collar": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"),
                 fc.Notch("collar", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_sole():
    """A foot-shaped sole outline, cut 2 (upper + under). Simple rounded oblong."""
    L = foot_length
    pts = []
    for i in range(SEGS):
        a = 2.0 * math.pi * i / SEGS
        x = SOLE_HALF * math.cos(a)
        y = L / 2.0 * math.sin(a)
        # widen the toe end slightly
        if math.sin(a) > 0:
            x *= 1.06
        pts.append(fc.P(x, y + L / 2.0))
    edges = [fc.Edge(f"seg{i}", [fc.Line(pts[i], pts[(i + 1) % SEGS])])
             for i in range(SEGS)]
    return fc.Piece(
        "sole", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("seg0", 0.5, "heel centre")],
        grainline=fc.Grainline(fc.P(0.0, L * 0.1), fc.P(0.0, L * 0.9)),
        internals=[fc.Internal("heel-tip seat",
                               [fc.P(-TIP_POCKET_W / 2.0, tip_clear),
                                fc.P(TIP_POCKET_W / 2.0, tip_clear),
                                fc.P(TIP_POCKET_W / 2.0, tip_clear + POCKET_DEPTH),
                                fc.P(-TIP_POCKET_W / 2.0, tip_clear + POCKET_DEPTH),
                                fc.P(-TIP_POCKET_W / 2.0, tip_clear)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Sole (cut 2)",
    )


def build_counter():
    """The heel counter, cut 1. Wraps the heel; a pocket for the printed tip blank."""
    w = max(TIP_POCKET_W + 24.0, SOLE_HALF * 2.0)
    h = counter_height
    return fc.Piece(
        "counter", [
            fc.Edge("lasting", [fc.Line(fc.P(-w / 2.0, 0.0), fc.P(w / 2.0, 0.0))]),
            fc.Edge("right", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(w / 2.0 - w * 0.1, h))]),
            fc.Edge("topline", [fc.curve_through(fc.P(w / 2.0 - w * 0.1, h),
                                                 fc.P(-w / 2.0 + w * 0.1, h),
                                                 bulge=0.10, side=-1.0)]),
            fc.Edge("left", [fc.Line(fc.P(-w / 2.0 + w * 0.1, h), fc.P(-w / 2.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, h - 8.0)),
        internals=[fc.Internal("tip blank pocket",
                               [fc.P(-TIP_POCKET_W / 2.0, 4.0),
                                fc.P(TIP_POCKET_W / 2.0, 4.0),
                                fc.P(TIP_POCKET_W / 2.0, 4.0 + POCKET_DEPTH),
                                fc.P(-TIP_POCKET_W / 2.0, 4.0 + POCKET_DEPTH),
                                fc.P(-TIP_POCKET_W / 2.0, 4.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Heel counter (cut 1)",
    )


def build():
    pattern = fc.PatternSet("heel-tip-slipper")
    everything = target_piece == "set"
    if everything or target_piece == "vamp":
        pattern.add(build_vamp())
    if everything or target_piece == "sole":
        pattern.add(build_sole())
    if everything or target_piece == "counter":
        pattern.add(build_counter())

    # The vamp and the heel counter are BOTH lasted independently to the sole — they do not
    # sew to each other (a house slipper has an open collar between vamp and counter), so no
    # inter-piece seam is declared; each lasting edge stitches to the sole edge.

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "boiled wool felt (upper + sole)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 60% marker; a dense boiled-wool felt for a warm, quiet "
                 "slipper. Per PAIR, double this."},
        {"item": "heel-tip blank", "qty": 1, "unit": "count",
         "note": f"Yantra4D heel-tip-blank (notion.hardware_ref) at {tip_width:.0f} x "
                 f"{tip_length:.0f} mm; seats in the heel counter pocket and pins to the sole "
                 f"as a replaceable hard heel."},
        {"item": "thread + heel pins", "qty": 1, "unit": "set",
         "note": "the tip blank pins through the marked seat; the felt heel wears against the "
                 "blank, not the floor."},
    ]
    pattern.metadata = {
        "fc500_rank": 426, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "fieltro-lana",
        "silhouette_note": "A felted-wool slipper with a replaceable printed heel-tip blank "
            "seated in the heel counter.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "tip_pocket_mm": [round(TIP_POCKET_W, 1), round(TIP_POCKET_L, 1)],
            "pocket_depth_mm": round(POCKET_DEPTH, 1),
            "note": "the vamp lasting edge is a proportionate bow over its own chord; the "
                    "tip pocket is cut to the MEASURED tip blank plus a clearance; the pocket "
                    "depth is clamped under the counter height so it never runs through the "
                    "topline.",
        },
        "hardware": "heel-tip blank via Yantra4D (notion.hardware_ref -> heel-tip-blank); "
                    "tip_w and tip_l are fed from the tip dimensions. No flange interface — "
                    "the blank seats in the counter pocket, no seam handshake owed.",
    }
    return pattern


result = build()
