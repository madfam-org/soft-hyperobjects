"""
Espadrille upper wrap — Fashion Cabinet Cartridge (FC-500 #424, footwear_soft, T2).

The espadrille: a soft canvas slip-on whose VAMP covers the toes and instep and whose HEEL
sling wraps the back of the foot, both stitched down to a jute sole. This version adds the
optional ANKLE-WRAP tie — a lace threaded through a pair of eyelets at the vamp throat that
crosses the instep and ties at the ankle. The eyelets bridge to a Yantra4D `garment-eyelet`.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. Sized from
PLAIN parameters (foot_length, foot_girth); no landmark code is invented.

Solving and clamps (the FC-400 footwear idiom):
  - Both lasting edges are SOLVED (bisected-bulge arcs) to a PROPORTIONATE BOW over the
    piece's own chord, NOT a share of the whole sole perimeter (which degenerates to a sliver).
  - The heel sling's top edge is drafted to the vamp throat so the two pieces meet flush at
    the side seams.
  - The eyelet pair is stepped in off the throat edge by its own diameter plus a margin so it
    never tears out the finished edge.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|heel|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
vamp_depth = float(PARAM(lambda: vamp_depth, 110.0))
heel_height = float(PARAM(lambda: heel_height, 70.0))
eyelet_dia = float(PARAM(lambda: eyelet_dia, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
vamp_depth = max(60.0, min(vamp_depth, 180.0))
heel_height = max(40.0, min(heel_height, 140.0))
eyelet_dia = max(3.0, min(eyelet_dia, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

VAMP_SHARE = max(0.34, min(vamp_depth / foot_length + 0.12, 0.60))
VAMP_HALF = max(24.0, foot_girth / 2.0 / 2.0 + 12.0)
HEEL_HALF = max(20.0, foot_girth / 2.0 / 2.0 * 0.9)
_vamp_bow = 1.10 + 0.55 * VAMP_SHARE
_heel_bow = 1.10 + 0.30 * (1.0 - VAMP_SHARE)
VAMP_LAST = 2.0 * VAMP_HALF * _vamp_bow
HEEL_LAST = 2.0 * HEEL_HALF * _heel_bow


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
    p_tr = fc.P(VAMP_HALF * 0.80, h)
    p_tl = fc.P(-VAMP_HALF * 0.80, h)
    a = max(2.0, eyelet_dia * 0.6)
    inset = max(10.0, eyelet_dia * 2.4)
    return fc.Piece(
        "vamp", [
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.12, side=1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"),
                 fc.Notch("throat", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[
            fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)], kind="marking"),
            fc.Internal("eyelet L",
                        [fc.P(-VAMP_HALF * 0.80 + inset - a, h - inset),
                         fc.P(-VAMP_HALF * 0.80 + inset + a, h - inset)], kind="drill"),
            fc.Internal("eyelet R",
                        [fc.P(VAMP_HALF * 0.80 - inset - a, h - inset),
                         fc.P(VAMP_HALF * 0.80 - inset + a, h - inset)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep, eyelet tie)",
    )


def build_heel(side_len):
    """The heel sling, cut 1. Wraps the back of the foot; its two top corners meet the vamp
    side edges (drafted to the vamp side length so the side seams sew flush)."""
    h = heel_height
    p_ll = fc.P(-HEEL_HALF, 0.0)
    p_lr = fc.P(HEEL_HALF, 0.0)
    dx = HEEL_HALF * 0.12
    dy2 = side_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("heel: side shorter than its run")
    dy = dy2 ** 0.5
    back_h = max(h, dy)
    p_tr = fc.P(HEEL_HALF - dx, dy)
    p_tl = fc.P(-HEEL_HALF + dx, dy)
    return fc.Piece(
        "heel", [
            _arc("lasting", p_ll, p_lr, HEEL_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=-1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre heel"),
                 fc.Notch("topline", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, min(dy, back_h) - 8.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Heel sling (cut 1)",
    )


def build():
    pattern = fc.PatternSet("espadrille-upper-wrap")
    everything = target_piece == "set"
    vamp = build_vamp()
    side_len = vamp.edge("side_r").length(0.05)
    heel = build_heel(side_len)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "heel":
        pattern.add(heel)

    if everything or target_piece == "set":
        pattern.declare_seam(("vamp", "side_r"), ("heel", "side_r"), tol=1.0)
        pattern.declare_seam(("vamp", "side_l"), ("heel", "side_l"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "cotton canvas (upper)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 60% marker; a soft canvas over a jute espadrille sole. "
                 "Per PAIR, double this."},
        {"item": "jute / rope sole", "qty": 1, "unit": "pair",
         "note": "the lasting edge is stitched down to the jute sole edge."},
        {"item": "garment eyelets", "qty": 2, "unit": "count",
         "note": f"Yantra4D garment-eyelet (notion.hardware_ref) at {eyelet_dia:.0f} mm; the "
                 f"ankle-wrap lace threads through the vamp-throat pair."},
        {"item": "cotton lace + waxed thread", "qty": 1, "unit": "set",
         "note": "a soft ankle-tie lace; the sole is stitched with waxed thread."},
    ]
    pattern.metadata = {
        "fc500_rank": 424, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "lona-algodon",
        "silhouette_note": "A canvas espadrille upper: a vamp with an ankle-wrap eyelet tie "
            "and a heel sling, stitched to a jute sole.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "heel_lasting_mm": round(HEEL_LAST, 1),
            "vamp_side_mm": round(side_len, 1),
            "note": "the lasting edges are proportionate bows over their own chords; the heel "
                    "sling's side is drafted to the vamp side so the side seams sew flush; "
                    "the eyelet pair is stepped in off the throat edge so it never tears out.",
        },
        "hardware": "Yantra4D garment-eyelet (notion.hardware_ref); inner_dia, barrel_h and "
                    "wall are fed from the eyelet — the flange params are left unmapped (the "
                    "eyelet sets through a drilled hole, no sewn edge, no handshake owed).",
    }
    return pattern


result = build()
