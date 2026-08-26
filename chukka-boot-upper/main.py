"""
Chukka boot soft upper — Fashion Cabinet Cartridge (FC-500 #423, footwear_soft, T3).

The chukka: an ankle boot with a VAMP over the toes and instep and two QUARTERS that wrap the
ankle and carry two or three lace pairs on open-throat facings (the low, quick-lace boot). The
quarters rise higher than a shoe to cover the ankle bone; the whole lower edge (the lasting
edge) stitches down to the sole. The lace hooks bridge to a Yantra4D `lacing-hook`.

FOOT SIZING NOTE (honest, checked): ISO 8559 as vendored declares NO foot landmark codes.
This cartridge drafts from PLAIN sized parameters (foot_length, foot_girth, ankle_height),
never measurement-coded body landmarks. No landmark code is invented.

Solving and clamps (the FC-400 footwear idiom):
  - Both lasting edges are SOLVED (bisected-bulge arcs) to a PROPORTIONATE BOW over the
    piece's own chord (2 x half-width), NOT a share of the whole sole perimeter — a lasting
    arc far longer than its chord bows into a thin degenerate sliver at the extreme.
  - The quarter facing seam is drafted to the vamp throat seam length so the declared seam
    balances at delta ~ 0.
  - The ankle height (quarter rise) is clamped so it never exceeds a sane multiple of the
    quarter half-width, which would fold the topline through the lasting edge.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|quarter|set

foot_length = float(PARAM(lambda: foot_length, 260.0))
foot_girth = float(PARAM(lambda: foot_girth, 240.0))
vamp_depth = float(PARAM(lambda: vamp_depth, 120.0))
ankle_height = float(PARAM(lambda: ankle_height, 130.0))   # quarter rise over the sole
lace_pairs = int(PARAM(lambda: lace_pairs, 3))
lace_dia = float(PARAM(lambda: lace_dia, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
vamp_depth = max(70.0, min(vamp_depth, 200.0))
ankle_height = max(80.0, min(ankle_height, 220.0))
lace_pairs = max(2, min(lace_pairs, 4))
lace_dia = max(2.5, min(lace_dia, 8.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

VAMP_SHARE = max(0.30, min(vamp_depth / foot_length + 0.12, 0.60))
VAMP_HALF = max(22.0, foot_girth / 2.0 / 2.0 + 10.0)
QUARTER_HALF = max(20.0, foot_girth / 2.0 / 2.0 * 0.95)
# ankle height clamped so the topline never folds through the lasting edge
QUARTER_RISE = min(ankle_height, QUARTER_HALF * 4.0)
QUARTER_RISE = max(60.0, QUARTER_RISE)
_vamp_bow = 1.10 + 0.55 * VAMP_SHARE
_quarter_bow = 1.10 + 0.35 * (1.0 - VAMP_SHARE)
VAMP_LAST = 2.0 * VAMP_HALF * _vamp_bow
QUARTER_LAST = 2.0 * QUARTER_HALF * _quarter_bow


def _arc(name, p0, p1, target, side):
    def mk(bulge):
        return fc.Edge(name, [fc.curve_through(p0, p1, bulge=bulge, side=side)])
    chord = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
    if target <= chord:
        raise ValueError(f"{name}: target {target:.1f} < chord {chord:.1f}")
    lo, hi = 0.0, 3.0
    if mk(hi).length(0.05) < target:
        raise ValueError(f"{name}: target unreachable")
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
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=1.0)]),
            fc.Edge("throat_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"),
                 fc.Notch("throat", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_quarter(facing_len):
    """One quarter (side + back), cut 2 mirrored. Rises to the ankle; its facing seam is
    drafted to the vamp throat length so the declared seam balances; the lace hooks run up
    the facing."""
    h = QUARTER_RISE
    p_ll = fc.P(-QUARTER_HALF, 0.0)
    p_lr = fc.P(QUARTER_HALF, 0.0)
    dx = QUARTER_HALF * 0.15
    dy2 = facing_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("quarter: facing shorter than its horizontal run")
    dy = dy2 ** 0.5              # the facing top height that MEASURES facing_len exactly
    # the back rises to at least the ankle height, but never below the facing top, so the
    # topline is always a real span and the facing seam length is preserved.
    back_h = max(h, dy)
    p_tr = fc.P(QUARTER_HALF - dx, dy)
    p_tl = fc.P(-QUARTER_HALF + dx, back_h)
    internals = []
    inset = max(9.0, lace_dia * 2.4)
    for i in range(lace_pairs):
        t = (i + 0.5) / lace_pairs
        cx = (QUARTER_HALF - dx) - inset
        cy = dy - inset - (dy - inset * 2.0) * t if dy > inset * 3 else dy * (1 - t)
        r = lace_dia / 2.0
        internals.append(fc.Internal(f"lace hook {i + 1}",
                         [fc.P(cx - r, cy), fc.P(cx + r, cy)], kind="drill"))
    return fc.Piece(
        "quarter", [
            _arc("lasting", p_ll, p_lr, QUARTER_LAST, side=1.0),
            fc.Edge("facing", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.08, side=-1.0)]),
            fc.Edge("back_seam", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "side"), fc.Notch("facing", 0.5, "throat")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, min(dy, back_h) - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Quarter (ankle wrap, lace facing)",
    )


def build():
    pattern = fc.PatternSet("chukka-boot-upper")
    everything = target_piece == "set"
    vamp = build_vamp()
    facing_len = vamp.edge("throat_r").length(0.05)
    quarter = build_quarter(facing_len)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "quarter":
        pattern.add(quarter)

    if everything or target_piece == "set":
        pattern.declare_seam(("vamp", "throat_r"), ("quarter", "facing"), tol=1.0)
        pattern.declare_seam(("vamp", "throat_l"), ("quarter", "facing"), tol=1.0)
    if "quarter" in {p.name for p in pattern.pieces}:
        pattern.declare_seam(("quarter", "back_seam"), ("quarter", "back_seam"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    n_hooks = 2 * lace_pairs
    pattern.bom = [
        {"item": "waxed canvas / suede (upper)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 55% marker; a soft chukka upper over a crepe or "
                 "leather sole. Per PAIR, double this."},
        {"item": "crepe / leather sole + welt", "qty": 1, "unit": "pair",
         "note": "the lasting edge is stitched down / welted to the sole."},
        {"item": "lacing hooks", "qty": n_hooks, "unit": "count",
         "note": f"Yantra4D lacing-hook (notion.hardware_ref) — {lace_pairs} pairs up the "
                 f"open-throat facing; set through the marked drill points."},
        {"item": "laces + waxed thread", "qty": 1, "unit": "set",
         "note": "round waxed laces; waxed lasting thread and a curved needle."},
    ]
    pattern.metadata = {
        "fc500_rank": 423, "family": "footwear_soft", "tier": 3,
        "fabric_hint": "lona-encerada",
        "silhouette_note": "An ankle chukka upper: a vamp over the toes and two ankle-rise "
            "quarters carrying two or three lace pairs on open-throat facings.",
        "sizing_note": "Sized from foot_length / foot_girth / ankle_height as PLAIN "
            "parameters — ISO 8559 declares no foot landmark codes, so none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "quarter_lasting_mm": round(QUARTER_LAST, 1),
            "facing_seam_mm": round(facing_len, 1),
            "quarter_rise_requested_mm": round(ankle_height, 1),
            "quarter_rise_clamped_mm": round(QUARTER_RISE, 1),
            "rise_was_clamped": bool(abs(QUARTER_RISE - ankle_height) > 0.01),
            "lace_hooks": n_hooks,
            "note": "the lasting edges are proportionate bows over their own chords (never a "
                    "share of the whole sole perimeter, which degenerates); the quarter "
                    "facing is drafted to the vamp throat; the ankle rise is clamped under 4x "
                    "the quarter half-width so the topline never folds through the lasting edge.",
        },
        "hardware": "Yantra4D lacing-hook (notion.hardware_ref); the hook count, pitch and "
                    "cord diameter are fed from the lace pairs and lace_dia. The sew-plate "
                    "params are left unmapped — the hooks set through drilled holes, no sewn "
                    "seam, so no dimensional handshake is owed.",
    }
    return pattern


result = build()
