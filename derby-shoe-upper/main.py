"""
Derby shoe upper — FC-400 rank #359, Lane 6 (footwear). Fashion Cabinet Cartridge.

The Derby (open-lacing) shoe upper: a VAMP over the toes and instep, and two QUARTERS
(the sides and back) whose facings sit OVER the vamp and carry the lace eyelets — the open
throat that distinguishes a Derby from an Oxford. The two quarters meet at a centre-back
seam; the whole lower edge (the lasting edge) is stitched down to the sole. The eyelets
bridge to a Yantra4D garment-eyelet.

FOOT SIZING NOTE (honest, checked): ISO 8559 as vendored declares NO foot landmark codes.
This cartridge drafts from PLAIN sized parameters (foot_length, foot_girth), never
measurement-coded body landmarks. No landmark code is invented.

Pieces:
  - vamp     : toe + instep cover (cut 1). Lasting edge below, throat above.
  - quarter  : the side-and-back wrap with the eyelet facing (cut 2, mirrored). Lasting
               edge below, top line above, eyelet ladder up the facing.

Solving and clamps. Both lasting edges are SOLVED (bisected-bulge arcs) to a length that
is a PROPORTIONATE BOW over the piece's own chord (2 x half-width), not a share of the
whole sole perimeter — a lasting arc far longer than its chord would bow into a thin
degenerate sliver at the short-foot / wide-foot extreme. The quarter's facing seam is
drafted to the vamp's throat seam length so the declared seam balances. The eyelet count
is clamped.

Hardware: Yantra4D garment-eyelet (point hardware; set through drilled holes, no sewn edge
— no dimensional handshake owed).

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
vamp_depth = float(PARAM(lambda: vamp_depth, 110.0))
quarter_height = float(PARAM(lambda: quarter_height, 70.0))
eyelet_pairs = int(PARAM(lambda: eyelet_pairs, 5))
eyelet_dia = float(PARAM(lambda: eyelet_dia, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

foot_length = max(150.0, min(foot_length, 340.0))
foot_girth = max(150.0, min(foot_girth, 330.0))
vamp_depth = max(60.0, min(vamp_depth, 190.0))
quarter_height = max(40.0, min(quarter_height, 150.0))
eyelet_pairs = max(2, min(eyelet_pairs, 8))
eyelet_dia = max(2.5, min(eyelet_dia, 10.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

SOLE_K = 1.08
VAMP_SHARE = max(0.30, min(vamp_depth / foot_length + 0.12, 0.60))
# The piece half-widths come from the foot girth.
VAMP_HALF = max(20.0, foot_girth / 2.0 / 2.0 + 8.0)
QUARTER_HALF = max(18.0, foot_girth / 2.0 / 2.0 * 0.92)
# The lasting edge is a solved ARC that bows down (the toe/side curve). Its length is a
# proportionate BOW over its own chord (2 x half), NOT a share of the whole sole perimeter
# — a lasting arc far longer than its chord bows into a thin degenerate sliver. The bow
# factor grows with the piece's share of the foot length so a deeper vamp bows more, but
# it is clamped so the arc is always a sane curve over its chord.
_vamp_bow = 1.10 + 0.55 * VAMP_SHARE
_quarter_bow = 1.10 + 0.35 * (1.0 - VAMP_SHARE)
VAMP_LAST = 2.0 * VAMP_HALF * _vamp_bow
QUARTER_LAST = 2.0 * QUARTER_HALF * _quarter_bow


def _arc(name, p0, p1, target, side):
    """An edge that is a single solved arc from p0 to p1 whose length == target."""
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
        "vamp",
        [
            _arc("lasting", p_ll, p_lr, VAMP_LAST, side=1.0),
            fc.Edge("throat_r", [fc.Line(p_lr, p_tr)]),        # to the quarter facing
            fc.Edge("throat", [fc.curve_through(p_tr, p_tl, bulge=0.10, side=1.0)]),
            fc.Edge("throat_l", [fc.Line(p_tl, p_ll)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"throat": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"), fc.Notch("throat", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=[fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, h)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Vamp (toe + instep)",
    )


def build_quarter(facing_len):
    """One quarter (side + back), cut 2 mirrored. Its facing seam is drafted to the vamp's
    throat_r length so the declared seam balances; the eyelet ladder runs up the facing."""
    h = quarter_height
    p_ll = fc.P(-QUARTER_HALF, 0.0)          # centre-back-ish lower
    p_lr = fc.P(QUARTER_HALF, 0.0)           # throat-side lower
    # Facing edge: from the throat-side lower up, its straight length == facing_len.
    dx = QUARTER_HALF * 0.15
    dy2 = facing_len ** 2 - dx ** 2
    if dy2 <= 1.0:
        raise ValueError("quarter: facing shorter than its horizontal run")
    dy = dy2 ** 0.5
    p_tr = fc.P(QUARTER_HALF - dx, dy)       # throat-side top (facing top)
    p_tl = fc.P(-QUARTER_HALF + dx, dy * 0.7)  # back-side top
    internals = []
    inset = max(9.0, eyelet_dia * 2.4)
    for i in range(eyelet_pairs):
        t = (i + 0.5) / eyelet_pairs
        cx = (QUARTER_HALF - dx) - inset
        cy = dy - inset - (h * 0.5) * t
        r = eyelet_dia / 2.0
        internals.append(fc.Internal(f"eyelet-{i + 1}",
                                     [fc.P(cx - r, cy), fc.P(cx + r, cy)], kind="drill"))
    return fc.Piece(
        "quarter",
        [
            _arc("lasting", p_ll, p_lr, QUARTER_LAST, side=1.0),
            fc.Edge("facing", [fc.Line(p_lr, p_tr)]),          # to the vamp throat
            fc.Edge("topline", [fc.curve_through(p_tr, p_tl, bulge=0.08, side=-1.0)]),
            fc.Edge("back_seam", [fc.Line(p_tl, p_ll)]),       # centre-back join
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "side"), fc.Notch("facing", 0.5, "throat")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, dy - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Quarter (side + back, eyelet facing)",
    )


def build():
    pattern = fc.PatternSet("derby-shoe-upper")
    everything = target_piece == "set"
    vamp = build_vamp()
    facing_len = vamp.edge("throat_r").length(0.05)
    quarter = build_quarter(facing_len)
    if everything or target_piece == "vamp":
        pattern.add(vamp)
    if everything or target_piece == "quarter":
        pattern.add(quarter)

    if everything or target_piece == "set":
        # the vamp throat sides sew under the two quarter facings
        pattern.declare_seam(("vamp", "throat_r"), ("quarter", "facing"), tol=1.0)
        pattern.declare_seam(("vamp", "throat_l"), ("quarter", "facing"), tol=1.0)
    if "quarter" in {p.name for p in pattern.pieces}:
        # the two quarters join at the centre back
        pattern.declare_seam(("quarter", "back_seam"), ("quarter", "back_seam"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    n_eyelets = 2 * eyelet_pairs
    pattern.bom = [
        {"item": "calf leather (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 55% marker (leather is cut in hides, not width; this "
                 "is an area proxy). Per PAIR, double this."},
        {"item": "leather sole + welt", "qty": 1, "unit": "pair",
         "note": "the lasting edge is stitched down / welted to the sole."},
        {"item": "garment eyelets", "qty": n_eyelets, "unit": "count",
         "note": "Yantra4D garment-eyelet (see notion.hardware_ref) — set through the "
                 "quarter's marked drill points; open-lacing Derby facing."},
        {"item": "laces + waxed thread", "qty": 1, "unit": "set",
         "note": "flat or round laces; waxed lasting thread and a curved needle."},
    ]
    pattern.metadata = {
        "fc400_rank": 359, "family": "footwear_soft", "lane": 6,
        "fabric_hint": "leather-calf",
        "silhouette_note": "An open-lacing Derby upper: a vamp over the toes and instep, "
            "and two quarters whose eyelet facings sit OVER the vamp — the open throat that "
            "makes it a Derby, not an Oxford.",
        "sizing_note": "Sized from foot_length / foot_girth as PLAIN parameters — ISO 8559 "
            "declares no foot landmark codes, so none is claimed and none is invented.",
        "solved": {
            "sole_perimeter_est_mm": round(2.0 * foot_length * SOLE_K, 1),
            "vamp_lasting_mm": round(VAMP_LAST, 1),
            "quarter_lasting_mm": round(QUARTER_LAST, 1),
            "facing_seam_mm": round(facing_len, 1),
            "eyelets": n_eyelets,
        },
        "hardware": "Yantra4D garment-eyelet (point hardware; drilled, no sewn edge — no "
                    "dimensional handshake owed)",
    }
    return pattern


result = build()
