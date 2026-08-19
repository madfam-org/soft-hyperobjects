"""
Sheath Dress — Fashion Cabinet Garment Cartridge (FC-200 #172, dress silhouette gap).

The fitted sheath: a close, straight dress shaped by bust and waist darts (kept as internal
markings over a COMMON fitted side seam, so the seam balances by construction), a jewel neck,
and a straight skirt to the knee with a back walking vent marked. Distinct from FC-100's loose
shift dress — the sheath is darted and body-skimming. Front and back share the structural
bust/waist/hip widths, so shoulder and side seams balance.

Pieces:
  - front / back : one-piece fitted front + back (cut on fold), bust/waist darts marked.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|set

bust_girth   = float(PARAM(lambda: bust_girth, 920.0))
waist_girth  = float(PARAM(lambda: waist_girth, 740.0))
hip_girth    = float(PARAM(lambda: hip_girth, 980.0))
dress_length = float(PARAM(lambda: dress_length, 1000.0))  # shoulder to hem (knee)
waist_pos    = float(PARAM(lambda: waist_pos, 400.0))      # shoulder to natural waist
neck_width   = float(PARAM(lambda: neck_width, 180.0))
shoulder_w   = float(PARAM(lambda: shoulder_w, 120.0))
ease         = float(PARAM(lambda: ease, 80.0))            # close, body-skimming
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(700.0, min(bust_girth, 1400.0))
waist_girth  = max(560.0, min(waist_girth, 1250.0))
hip_girth    = max(760.0, min(hip_girth, 1450.0))
dress_length = max(750.0, min(dress_length, 1350.0))
waist_pos    = max(320.0, min(waist_pos, 500.0))
neck_width   = max(130.0, min(neck_width, 300.0))
shoulder_w   = max(70.0, min(shoulder_w, 200.0))
ease         = max(20.0, min(ease, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 70.0))

L = dress_length
WAIST_Y = L - waist_pos                              # y of the natural waist (from hem up)
BUST_HALF  = (bust_girth + ease) / 4.0
WAIST_HALF = (waist_girth + ease) / 4.0
HIP_HALF   = (hip_girth + ease) / 4.0
NECK_HALF  = neck_width / 2.0
SHOULDER_X = NECK_HALF + shoulder_w
ARMSCYE_DROP = 220.0
HIP_Y = WAIST_Y - 200.0                              # hip line below waist


def _panel(name, neck_dip, is_front, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER_X, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    # side seam: bust -> waist (in) -> hip (out) -> straight to hem, as a smooth polyline
    side_pts = [armscye_bot,
                fc.P(WAIST_HALF, WAIST_Y),
                fc.P(HIP_HALF, HIP_Y),
                fc.P(HIP_HALF, 0.0)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[i], side_pts[i + 1]) for i in range(3)])
    internals = []
    # waist dart (both), bust dart (front only) — markings, do NOT open the seam
    internals.append(fc.Internal("waist-dart",
                                 [fc.P(WAIST_HALF * 0.5, WAIST_Y + 110.0),
                                  fc.P(WAIST_HALF * 0.5, WAIST_Y - 130.0)], kind="dart"))
    if is_front:
        internals.append(fc.Internal("bust-dart",
                                     [fc.P(BUST_HALF, top_y - ARMSCYE_DROP - 20.0),
                                      fc.P(WAIST_HALF * 0.55, top_y - ARMSCYE_DROP - 60.0)],
                                     kind="dart"))
    else:
        internals.append(fc.Internal("back-vent",
                                     [fc.P(0.0, 0.0), fc.P(0.0, 240.0)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                                 bulge=0.18, side=-1.0)]),
            side_edge,
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 0.33, "waist")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 80.0), fc.P(WAIST_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("sheath-dress")
    everything = target_piece == "set"
    front = _panel("front", 62.0, True, "Front (darts)")
    back = _panel("back", 24.0, False, "Back (vent)")
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "stable woven with a little stretch (suiting / ponte)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 72% marker; a stable cloth holds the fitted shape."},
        {"item": "invisible back zip", "qty": 1, "unit": "pc",
         "note": "a fitted sheath closes with a CB invisible zip; a lining is the maker's option."},
        {"item": "lightweight fusible (neck/armscye)", "qty": 1, "unit": "as needed",
         "note": "stabilises the neckline and armholes."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + darts."},
    ]
    pattern.metadata = {
        "fc200_rank": 172, "family": "dresses_jumpsuits", "fabric_hint": "ponte-suiting",
        "silhouette_note": "A close, straight, darted sheath shaped by bust and waist darts "
            "over a common fitted side seam (side balances by construction), a jewel neck, and "
            "a straight knee-length skirt with a back walking vent. Distinct from the loose shift.",
        "solved": {"bust_q_mm": round(BUST_HALF, 1), "waist_q_mm": round(WAIST_HALF, 1),
                   "hip_q_mm": round(HIP_HALF, 1)},
    }
    return pattern


result = build()
