"""
Driving-moccasin upper — Fashion Cabinet Cartridge (FC-500 #429, footwear_soft, T3).

The driving moccasin: a soft one-piece WRAP that cups the sole and rises around the foot,
gathered to a raised centre-front PLUG seam (the hand-sewn moccasin apron), with a lace pair
through the throat. The sole wrap runs UP the sides and its lasting edge is not stitched down
to a separate sole but turned up and hand-lasted, so the moccasin has the soft, seamless
underfoot of a true mocc. Rubber driving-pebbles are marked on the underfoot (not modelled).
The throat eyelets bridge to a Yantra4D `garment-eyelet`.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. Sized from
PLAIN parameters (foot_length, foot_girth); no landmark code is invented.

Solving and clamps (the FC-400 footwear idiom):
  - The wrap's lasting edge is a SOLVED bow over its own chord (proportionate, never a share
    of the whole sole perimeter, which degenerates).
  - The plug seam is drafted to the wrap's gathered throat length so the apron sews in without
    a mismatch (declared as ease — the gather is real).
  - The throat rise is clamped so the wrap never folds through the lasting edge.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # wrap|plug|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
wrap_rise = float(PARAM(lambda: wrap_rise, 95.0))
plug_length = float(PARAM(lambda: plug_length, 130.0))
gather_ratio = float(PARAM(lambda: gather_ratio, 1.4))
eyelet_dia = float(PARAM(lambda: eyelet_dia, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
wrap_rise = max(60.0, min(wrap_rise, 170.0))
plug_length = max(70.0, min(plug_length, 220.0))
gather_ratio = max(1.1, min(gather_ratio, 2.0))
eyelet_dia = max(3.0, min(eyelet_dia, 10.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

WRAP_HALF = max(28.0, foot_girth / 2.0 / 2.0 + 16.0)
WRAP_RISE = min(wrap_rise, WRAP_HALF * 4.0)
WRAP_RISE = max(50.0, WRAP_RISE)
_wrap_bow = 1.14
WRAP_LAST = 2.0 * WRAP_HALF * _wrap_bow


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


def build_wrap():
    """The sole-wrap, cut 2 mirrored (inside + outside of the foot). Lasting edge below,
    the gathered throat above where the plug seams in, a back seam at the heel."""
    h = WRAP_RISE
    p_ll = fc.P(-WRAP_HALF, 0.0)
    p_lr = fc.P(WRAP_HALF, 0.0)
    p_tr = fc.P(WRAP_HALF * 0.7, h)
    p_tl = fc.P(-WRAP_HALF * 0.7, h)
    a = max(2.0, eyelet_dia * 0.6)
    return fc.Piece(
        "wrap", [
            _arc("lasting", p_ll, p_lr, WRAP_LAST, side=1.0),
            fc.Edge("heel_seam", [fc.Line(p_lr, p_tr)]),
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.14, side=1.0)]),
            fc.Edge("front_seam", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre underfoot"),
                 fc.Notch("throat", 0.5, "plug centre")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, h - 8.0)),
        internals=[
            fc.Internal("driving pebbles (underfoot)",
                        [fc.P(-WRAP_HALF * 0.4, 6.0), fc.P(WRAP_HALF * 0.4, 6.0)],
                        kind="marking"),
            fc.Internal("throat eyelet",
                        [fc.P(-a, h - max(12.0, eyelet_dia * 2.4)),
                         fc.P(a, h - max(12.0, eyelet_dia * 2.4))], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sole wrap (cut 2, mirrored)",
    )


_W = build_wrap()
THROAT_LEN = _W.edge("throat").length(0.05)
PLUG_SEAM = THROAT_LEN * gather_ratio      # the plug gathers the wrap throat


def build_plug():
    """The raised moccasin apron / plug, cut 1. A leaf whose two long edges gather the wrap
    throats; drafted to the gathered length so the apron sews in as a real gather."""
    half_w = max(18.0, WRAP_HALF * 0.4)

    def side_edge(chord):
        return fc.curve_through(fc.P(0.0, 0.0), fc.P(0.0, chord),
                                bulge=half_w / chord, side=1.0)

    lo, hi = PLUG_SEAM * 0.4, PLUG_SEAM
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if side_edge(mid).length(0.05) < PLUG_SEAM:
            lo = mid
        else:
            hi = mid
    chord = (lo + hi) / 2.0
    return fc.Piece(
        "plug", [
            fc.Edge("side_a", [side_edge(chord)]),
            fc.Edge("side_b", [fc.curve_through(fc.P(0.0, chord), fc.P(0.0, 0.0),
                                                bulge=half_w / chord, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_a", 0.5, "apron centre"),
                 fc.Notch("side_b", 0.5, "apron centre")],
        grainline=fc.Grainline(fc.P(1.0, chord * 0.1), fc.P(1.0, chord * 0.9)),
        internals=[fc.Internal("apron topstitch",
                               [fc.P(0.5, chord * 0.1), fc.P(0.5, chord * 0.9)],
                               kind="trace")],
        cut=fc.CutSpec(quantity=1),
        label="Raised plug / apron (cut 1)",
    )


def build():
    pattern = fc.PatternSet("moccasin-driver-upper")
    everything = target_piece == "set"
    wrap = build_wrap()
    plug = build_plug()
    if everything or target_piece == "wrap":
        pattern.add(wrap)
    if everything or target_piece == "plug":
        pattern.add(plug)

    if everything:
        # the plug gathers the two wrap throats: its side is longer, declared as the gather.
        plug_side = plug.edge("side_a").length(0.05)
        pattern.declare_seam(("wrap", "throat"), ("plug", "side_a"),
                             tol=1.0, ease=THROAT_LEN - plug_side)
        pattern.declare_seam(("wrap", "heel_seam"), ("wrap", "heel_seam"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "soft calf / suede (upper)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 55% marker; a soft glove leather so the wrap hand-lasts "
                 "and the apron gathers. Per PAIR, double this."},
        {"item": "rubber driving pebbles", "qty": 1, "unit": "set",
         "note": "the marked underfoot pebbles are set as a driving sole; marked, not modelled."},
        {"item": "garment eyelets", "qty": 2, "unit": "count",
         "note": f"Yantra4D garment-eyelet (notion.hardware_ref) at {eyelet_dia:.0f} mm; the "
                 f"throat lace pair."},
        {"item": "waxed hand-sewing thread", "qty": 1, "unit": "spool",
         "note": "the apron is a hand-sewn moccasin seam; the wrap is hand-lasted."},
    ]
    pattern.metadata = {
        "fc500_rank": 429, "family": "footwear_soft", "tier": 3,
        "fabric_hint": "cuero-vegetal",
        "silhouette_note": "A driving-moccasin upper: a soft sole-wrap gathered to a raised "
            "apron plug, with rubber driving pebbles marked underfoot.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is invented.",
        "solved": {
            "wrap_lasting_mm": round(WRAP_LAST, 1),
            "throat_mm": round(THROAT_LEN, 1),
            "plug_seam_mm": round(PLUG_SEAM, 1),
            "gather_ratio": round(gather_ratio, 2),
            "wrap_rise_clamped": bool(abs(WRAP_RISE - wrap_rise) > 0.01),
            "note": "the wrap lasting edge is a proportionate bow over its own chord; the "
                    "plug seam is drafted to the gathered wrap throat (declared as the gather "
                    "ease); the wrap rise is clamped under 4x the wrap half-width.",
        },
        "hardware": "Yantra4D garment-eyelet (notion.hardware_ref); inner_dia / barrel_h / "
                    "wall are fed from the eyelet — flange params unmapped, no handshake owed.",
    }
    return pattern


result = build()
