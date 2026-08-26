"""
Espadrille upper — FC-400 rank #361, Lane 6 (footwear). Fashion Cabinet Cartridge.

The closed espadrille (the classic flat slip-on): a single VAMP over the toes and instep
and a HEEL COUNTER round the back, joined at two side seams and stitched down to a jute
sole along the lasting edge. Unlike the FC-300 lace-eyelet espadrille, this is the plain
closed slip-on — no eyelets, no hardware — the everyday alpargata.

FOOT SIZING NOTE (honest, checked): ISO 8559 declares NO foot landmark codes. This
cartridge drafts from PLAIN sized parameters (foot_length, foot_girth). No landmark code is
invented.

Pieces:
  - vamp          : toe + instep cover (cut 1).
  - heel_counter  : back-of-foot wrap (cut 1).

Solving and clamps. Both lasting edges are SOLVED arcs whose length is a PROPORTIONATE BOW
over each piece's chord (never a share of the whole sole, which slivers at extremes). The
counter's side seams are drafted to the vamp's side seam length so both declared seams
balance at delta ~ 0.

Hardware: none — a closed slip-on espadrille has no hardware.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # vamp|heel_counter|set

foot_length = float(PARAM(lambda: foot_length, 255.0))
foot_girth = float(PARAM(lambda: foot_girth, 235.0))
vamp_depth = float(PARAM(lambda: vamp_depth, 100.0))
counter_height = float(PARAM(lambda: counter_height, 68.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
vamp_depth = max(50.0, min(vamp_depth, 170.0))
counter_height = max(35.0, min(counter_height, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

VAMP_SHARE = max(0.30, min(vamp_depth / foot_length + 0.12, 0.60))
VAMP_HALF = max(20.0, foot_girth / 2.0 / 2.0 + 6.0)
COUNTER_HALF = max(18.0, foot_girth / 2.0 / 2.0 * 0.86)
_vamp_bow = 1.10 + 0.55 * VAMP_SHARE
_counter_bow = 1.10 + 0.35 * (1.0 - VAMP_SHARE)
VAMP_LAST = 2.0 * VAMP_HALF * _vamp_bow
COUNTER_LAST = 2.0 * COUNTER_HALF * _counter_bow


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
    p_tr = fc.P(VAMP_HALF * 0.82, h)
    p_tl = fc.P(-VAMP_HALF * 0.82, h)
    return fc.Piece(
        "vamp",
        [
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 12.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"), fc.Notch("topline", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_counter(side_seam_len):
    p_ll = fc.P(-COUNTER_HALF, 0.0)
    p_lr = fc.P(COUNTER_HALF, 0.0)
    dx = COUNTER_HALF * 0.12
    dy2 = side_seam_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("counter: side seam shorter than its run")
    dy = dy2 ** 0.5
    p_tr = fc.P(COUNTER_HALF - dx, dy)
    p_tl = fc.P(-COUNTER_HALF + dx, dy)
    # The topline curves up to a centre-back rise set by counter_height relative to the
    # side height (dy): a taller counter_height lifts the back collar, a shorter one dips
    # it. The bulge is clamped to a fraction of the span so the topline never self-crosses.
    _rise = (counter_height - dy) / max(1.0, 2.0 * (COUNTER_HALF - dx))
    topline_bulge = max(-0.35, min(_rise, 0.45))
    return fc.Piece(
        "heel_counter",
        [
            _arc("lasting", p_ll, p_lr, COUNTER_LAST, side=1.0),
            fc.Edge("side_r", [fc.Line(p_lr, p_tr)]),
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=topline_bulge, side=-1.0)]),
            fc.Edge("side_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 12.0},
        notches=[fc.Notch("lasting", 0.5, "centre back"), fc.Notch("topline", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, dy - 8.0)),
        internals=[fc.Internal("centre-back", [fc.P(0.0, 0.0), fc.P(0.0, dy)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Heel counter",
    )


def build():
    pattern = fc.PatternSet("espadrille-shoe-upper")
    everything = target_piece == "set"
    vamp = build_vamp()
    side_len = vamp.edge("side_r").length(0.05)
    counter = build_counter(side_len)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "heel_counter":
        pattern.add(counter)

    if everything or target_piece == "set":
        pattern.declare_seam(("vamp", "side_r"), ("heel_counter", "side_l"), tol=1.0)
        pattern.declare_seam(("vamp", "side_l"), ("heel_counter", "side_r"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "cotton canvas / duck (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm, 55% marker. Per PAIR, double this."},
        {"item": "jute braid espadrille sole", "qty": 2, "unit": "pcs",
         "note": "the vulcanised or stitched jute sole the lasting edge sews down to."},
        {"item": "cotton drill lining (optional)", "qty": 1, "unit": "as chosen",
         "note": "softens the topline and hides the lasting stitches."},
        {"item": "waxed lasting thread", "qty": 1, "unit": "spool",
         "note": "heavy thread for the sole stitch-down; a curved needle helps."},
    ]
    pattern.metadata = {
        "fc400_rank": 361, "family": "footwear_soft", "lane": 6,
        "fabric_hint": "lona-algodon",
        "silhouette_note": "A closed canvas slip-on espadrille: a vamp over the toes and "
            "instep, a heel counter round the back, joined at two side seams and stitched "
            "to a jute sole. No eyelets, no hardware — the plain alpargata.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is claimed and none is invented.",
        "solved": {
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "counter_lasting_mm": round(COUNTER_LAST, 1),
            "side_seam_mm": round(side_len, 1),
            "note": "lasting arcs are proportionate bows over each chord so neither piece "
                    "slivers at the short-foot / wide-foot extreme",
        },
        "hardware": "none — a closed slip-on espadrille has no hardware",
    }
    return pattern


result = build()
