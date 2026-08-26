"""
Zip-pull-assist bootie — Fashion Cabinet Cartridge (FC-500 #428, footwear_soft, T2).

An adaptive neoprene bootie with a long side ZIP and a printed pull-assist LEVER (the
Yantra4D `zipper-pull-assist`) clipped to the zip pull — a big finger-loop lever that lets a
person with limited grip or reach close the zip one-handed. A soft neoprene VAMP + QUARTER
wrap the foot; a ZIP GUARD backs the side zip; and a LEVER TAB carries the printed assist.
Sized so the zip runs the full opening and the lever seats to the printed body.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. Sized from
PLAIN parameters (foot_length, foot_girth, ankle_height); no landmark code is invented.

Solving and clamps (the FC-400 footwear idiom):
  - The vamp lasting edge is a SOLVED bow over its own chord (proportionate, never a share of
    the whole sole perimeter, which degenerates).
  - The zip length is the MEASURED quarter side edge, so the zip runs the full opening.
  - The lever tab is cut to the printed assist body plus a clearance; the ankle rise is clamped
    so the quarter never folds through the lasting edge.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|quarter|guard|lever|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
vamp_depth = float(PARAM(lambda: vamp_depth, 110.0))
ankle_height = float(PARAM(lambda: ankle_height, 120.0))
assist_body = float(PARAM(lambda: assist_body, 40.0))     # printed pull-assist body length
lever_len = float(PARAM(lambda: lever_len, 60.0))         # finger lever length
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
vamp_depth = max(70.0, min(vamp_depth, 200.0))
ankle_height = max(70.0, min(ankle_height, 220.0))
assist_body = max(20.0, min(assist_body, 90.0))
lever_len = max(30.0, min(lever_len, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

VAMP_HALF = max(24.0, foot_girth / 2.0 / 2.0 + 12.0)
QUARTER_HALF = max(22.0, foot_girth / 2.0 / 2.0 * 0.95)
QUARTER_RISE = min(ankle_height, QUARTER_HALF * 4.0)
QUARTER_RISE = max(60.0, QUARTER_RISE)
VAMP_LAST = 2.0 * VAMP_HALF * 1.14
QUARTER_LAST = 2.0 * QUARTER_HALF * 1.12


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
            fc.Edge("throat_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.12, side=1.0)]),
            fc.Edge("throat_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 8.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_quarter(facing_len):
    h = QUARTER_RISE
    p_ll = fc.P(-QUARTER_HALF, 0.0)
    p_lr = fc.P(QUARTER_HALF, 0.0)
    dx = QUARTER_HALF * 0.15
    dy2 = facing_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("quarter: facing shorter than run")
    dy = dy2 ** 0.5
    back_h = max(h, dy)
    p_tr = fc.P(QUARTER_HALF - dx, dy)
    p_tl = fc.P(-QUARTER_HALF + dx, back_h)
    return fc.Piece(
        "quarter", [
            _arc("lasting", p_ll, p_lr, QUARTER_LAST, side=1.0),
            fc.Edge("zip_edge", [fc.Line(p_lr, p_tr)]),   # the side zip runs here
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.08, side=-1.0)]),
            fc.Edge("back_seam", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "side"),
                 fc.Notch("zip_edge", 1.0, "zip top")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, min(dy, back_h) - 8.0)),
        internals=[],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Quarter (ankle wrap, side zip)",
    )


def build_guard(zip_len):
    """The zip guard, cut 1. A strip the length of the zip that backs it against the skin."""
    ln = zip_len
    w = max(24.0, QUARTER_HALF * 0.5)
    return fc.Piece(
        "guard", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "zip centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Zip guard (cut 1)",
    )


def build_lever():
    """The lever tab, cut 1. Carries the printed pull-assist body and a finger lever."""
    w = assist_body + 16.0
    h = lever_len + assist_body + 20.0
    return fc.Piece(
        "lever", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("end", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "zip pull join")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=[
            fc.Internal("assist body seat",
                        [fc.P(w * 0.5 - assist_body / 2.0, 10.0),
                         fc.P(w * 0.5 + assist_body / 2.0, 10.0),
                         fc.P(w * 0.5 + assist_body / 2.0, 10.0 + assist_body),
                         fc.P(w * 0.5 - assist_body / 2.0, 10.0 + assist_body),
                         fc.P(w * 0.5 - assist_body / 2.0, 10.0)], kind="marking"),
            fc.Internal("finger loop",
                        [fc.P(w * 0.5, 10.0 + assist_body + 6.0), fc.P(w * 0.5, h - 6.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Pull-assist lever tab (cut 1)",
    )


def build():
    pattern = fc.PatternSet("zip-pull-assist-bootie")
    everything = target_piece == "set"
    vamp = build_vamp()
    facing_len = vamp.edge("throat_r").length(0.05)
    quarter = build_quarter(facing_len)
    zip_len = quarter.edge("zip_edge").length(0.05)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "quarter":
        pattern.add(quarter)
    if everything or target_piece == "guard":
        pattern.add(build_guard(zip_len))
    if everything or target_piece == "lever":
        pattern.add(build_lever())

    if everything or target_piece == "set":
        pattern.declare_seam(("vamp", "throat_r"), ("quarter", "zip_edge"), tol=1.5)
    if "quarter" in {p.name for p in pattern.pieces}:
        pattern.declare_seam(("quarter", "back_seam"), ("quarter", "back_seam"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "neoprene (2-3 mm) + jersey lining", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker; a soft stretch neoprene for an adaptive "
                 "bootie. Per PAIR, double this."},
        {"item": "long side zip", "qty": 1, "unit": "count",
         "note": f"a {zip_len:.0f} mm zip running the full quarter side opening."},
        {"item": "printed zipper pull-assist", "qty": 1, "unit": "count",
         "note": f"Yantra4D zipper-pull-assist (notion.hardware_ref) at a {assist_body:.0f} "
                 f"mm body; the finger lever clips to the zip pull for one-handed closing."},
        {"item": "sole + thread", "qty": 1, "unit": "pair",
         "note": "the lasting edge stitches to a flexible sole; ballpoint needle for the "
                 "neoprene."},
    ]
    pattern.metadata = {
        "fc500_rank": 428, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "neopreno",
        "silhouette_note": "An adaptive neoprene bootie with a full side zip and a printed "
            "pull-assist lever for one-handed closing.",
        "sizing_note": "Sized from foot_length / foot_girth / ankle_height as PLAIN "
            "parameters — ISO 8559 declares no foot landmark codes, so none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "quarter_lasting_mm": round(QUARTER_LAST, 1),
            "zip_length_mm": round(zip_len, 1),
            "lever_mm": [round(assist_body + 16.0, 1), round(lever_len + assist_body + 20.0, 1)],
            "quarter_rise_clamped": bool(abs(QUARTER_RISE - ankle_height) > 0.01),
            "note": "the vamp lasting edge is a proportionate bow over its own chord; the zip "
                    "runs the MEASURED quarter side; the lever tab is cut to the printed "
                    "assist body plus a clearance; the ankle rise is clamped under 4x the "
                    "quarter half-width.",
        },
        "hardware": "zipper pull-assist via Yantra4D (notion.hardware_ref -> "
                    "zipper-pull-assist); body_l and lever_len are fed from the assist body "
                    "and lever. No flange interface — the assist clips to the zip pull, no "
                    "seam handshake owed.",
    }
    return pattern


result = build()
