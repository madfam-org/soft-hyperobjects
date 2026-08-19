"""
Qipao / Cheongsam — Fashion Cabinet Garment Cartridge (FC-200 rank #142, Chinese heritage).

The qipao (Cantonese: cheongsam) is the fitted Chinese dress with its unmistakable
signatures: a mandarin (stand) collar, an asymmetric front opening curving from the
centre-neck to the right underarm, hand-knotted frog (pankou) fastenings, bust and waist
shaping, and side slits for movement. This cartridge drafts the garment geometry — a
fitted front and back with waist darts, a mandarin collar band solved to the neckline,
and marked frog + slit positions. Offered with respect for the living tradition; the
maker supplies the silk brocade, the piping, and the frog knots.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|collar|set

bust_girth   = float(PARAM(lambda: bust_girth, 900.0))     # full bust
waist_girth  = float(PARAM(lambda: waist_girth, 720.0))    # full waist
hip_girth    = float(PARAM(lambda: hip_girth, 960.0))      # full hip
qipao_length = float(PARAM(lambda: qipao_length, 1150.0))  # shoulder to hem
neck_girth   = float(PARAM(lambda: neck_girth, 380.0))     # neck girth (collar run)
collar_h     = float(PARAM(lambda: collar_h, 45.0))        # mandarin collar height
slit_height  = float(PARAM(lambda: slit_height, 350.0))    # side-slit height from hem
bust_ease    = float(PARAM(lambda: bust_ease, 60.0))       # fitted ease
waist_dart   = float(PARAM(lambda: waist_dart, 30.0))      # waist-dart intake
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(650.0, min(bust_girth, 1400.0))
waist_girth  = max(500.0, min(waist_girth, bust_girth))
hip_girth    = max(650.0, min(hip_girth, 1500.0))
qipao_length = max(800.0, min(qipao_length, 1600.0))
neck_girth   = max(300.0, min(neck_girth, 500.0))
collar_h     = max(25.0, min(collar_h, 80.0))
slit_height  = max(150.0, min(slit_height, qipao_length * 0.5))
bust_ease    = max(20.0, min(bust_ease, 160.0))
waist_dart   = max(0.0, min(waist_dart, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = qipao_length
# Quarter widths (each panel is a quarter of the body, cut as front OR back half-panels
# to the side seam). Front and back use the SAME side profile so the side seam balances.
BUST_Q = (bust_girth + bust_ease) / 4.0
WAIST_Q = (waist_girth + bust_ease) / 4.0
HIP_Q = (hip_girth + bust_ease) / 4.0
WAIST_Y = L * 0.60                                  # waist level up from the hem
NECK_HALF = 70.0                                    # neck opening half-width at the shoulder
SHOULDER_Y = L
DART_Y0 = WAIST_Y - 120.0
DART_Y1 = WAIST_Y + 120.0


def _side_edge():
    """The shared side-seam profile (a smooth curve bust→waist→hip→hem), as a list of
    edges from the underarm (top) down to the hem. Identical on front and back so the
    side seam always balances."""
    p_bust = fc.P(BUST_Q, SHOULDER_Y - 200.0)          # underarm
    p_waist = fc.P(WAIST_Q, WAIST_Y)
    p_hip = fc.P(HIP_Q, WAIST_Y - 260.0)
    p_hem = fc.P(HIP_Q, 0.0)
    return [
        fc.Edge("side_upper", [fc.curve_through(p_bust, p_waist, bulge=0.12, side=1.0)]),
        fc.Edge("side_lower", [fc.curve_through(p_waist, p_hip, bulge=0.10, side=-1.0)]),
        fc.Edge("side_hem", [fc.Line(p_hip, p_hem)]),
    ]


def _panel(name, neck_dip, label):
    """A fitted half-panel (cut on fold at centre): shoulder + straight armhole down to
    the underarm, the shared side profile, hem, centre, and neck scoop. A waist dart is
    marked internally (teaching-grade — kept as a marking, not rotated)."""
    neck_pt = fc.P(0.0, SHOULDER_Y - neck_dip)
    neck_out = fc.P(NECK_HALF, SHOULDER_Y)
    p_bust = fc.P(BUST_Q, SHOULDER_Y - 200.0)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BUST_Q, SHOULDER_Y))]),
        fc.Edge("armhole", [fc.Line(fc.P(BUST_Q, SHOULDER_Y), p_bust)]),
        *_side_edge(),
        fc.Edge("hem", [fc.Line(fc.P(HIP_Q, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if waist_dart > 0.0:
        dart_x = WAIST_Q * 0.5
        internals.append(fc.Internal("waist-dart", [
            fc.P(dart_x - waist_dart / 2.0, DART_Y0), fc.P(dart_x, WAIST_Y),
            fc.P(dart_x + waist_dart / 2.0, DART_Y0)], kind="dart"))
        internals.append(fc.Internal("waist-dart-lo", [
            fc.P(dart_x - waist_dart / 2.0, DART_Y1), fc.P(dart_x, WAIST_Y),
            fc.P(dart_x + waist_dart / 2.0, DART_Y1)], kind="dart"))
    # Mark the side slit on the hem side (from hem up to slit_height).
    internals.append(fc.Internal("side-slit",
                                 [fc.P(HIP_Q, 0.0), fc.P(HIP_Q, slit_height)], kind="marking"))
    if name == "front":
        # Mark the asymmetric front opening curve (centre-neck to right underarm) + frogs.
        internals.append(fc.Internal("front-opening", [
            fc.P(0.0, SHOULDER_Y - neck_dip), fc.P(BUST_Q * 0.5, SHOULDER_Y - 90.0),
            fc.P(BUST_Q, SHOULDER_Y - 200.0)], kind="marking"))
        for i, fy in enumerate((SHOULDER_Y - neck_dip - 10.0, SHOULDER_Y - 120.0,
                                SHOULDER_Y - 200.0)):
            fx = BUST_Q * (i / 2.0)
            internals.append(fc.Internal(f"frog-{i}",
                                         [fc.P(fx - 6.0, fy), fc.P(fx + 6.0, fy)], kind="drill"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"),
                 fc.Notch("side_upper", 1.0, "waist")],
        grainline=fc.Grainline(fc.P(WAIST_Q * 0.5, 80.0), fc.P(WAIST_Q * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _band_inner_edge(flat_len):
    return fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(flat_len, 0.0))])


def _solve_flat(edge_fn, target, what):
    lo, hi = target * 0.7, target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def build_collar():
    """The mandarin (stand) collar: a band solved to the neckline run (neck_girth),
    collar_h tall, standing at the neck."""
    flat = _solve_flat(_band_inner_edge, neck_girth, "collar inner-edge")
    inner = _band_inner_edge(flat)
    return fc.Piece(
        "collar",
        [
            inner,
            fc.Edge("end_b", [fc.Line(fc.P(flat, 0.0), fc.P(flat, collar_h))]),
            fc.Edge("outer", [fc.Line(fc.P(flat, collar_h), fc.P(0.0, collar_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, collar_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", 0.5, "centre back neck")],
        grainline=fc.Grainline(fc.P(flat * 0.5, collar_h * 0.5),
                               fc.P(flat * 0.5 + 80.0, collar_h * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Mandarin Collar",
    )


def build():
    pattern = fc.PatternSet("qipao")
    front = _panel("front", 90.0, "Front")
    back = _panel("back", 30.0, "Back")

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "collar":
        pattern.add(build_collar())

    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # The side seam is the shared 3-edge profile; declare each matching segment.
        pattern.declare_seam(("front", "side_upper"), ("back", "side_upper"), tol=1.5)
        pattern.declare_seam(("front", "side_lower"), ("back", "side_lower"), tol=1.5)
        pattern.declare_seam(("front", "side_hem"), ("back", "side_hem"), tol=1.5)

    fabric_width = 1100.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "silk brocade or jacquard",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1100 mm width, 70% marker; the brocade motif and colour are the maker's."},
        {"item": "frog (pankou) fastenings", "qty": 4, "unit": "sets",
         "note": "hand-knotted frog closures along the asymmetric front — the maker's craft."},
        {"item": "bias piping", "qty": 1, "unit": "as applied",
         "note": "the contrast piping edging the collar, opening, and slits."},
        {"item": "hidden zipper (modern) or snaps", "qty": 1, "unit": "set",
         "note": "the practical closure under the frogs; maker's choice."},
    ]
    pattern.metadata = {
        "fc200_rank": 142,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "heritage_note": "The qipao (cheongsam) is a living Chinese garment. This cartridge "
            "drafts the fitted GARMENT GEOMETRY only — the silk brocade, the frog (pankou) "
            "knots, and the piped edges that carry its identity are the maker's to supply. "
            "The asymmetric front opening, frogs, and slits are marked, not engineered. "
            "Offered with respect.",
        "solved": {"collar_inner_edge_mm": round(_band_inner_edge(
            _solve_flat(_band_inner_edge, neck_girth, "collar")).length(0.05), 1),
            "neck_run_target_mm": round(neck_girth, 1)},
        "fit_note": "Bust/waist/hip quarter-widths shape a smooth side seam; the waist dart "
            "is marked (teaching-grade, kept as a marking rather than rotated). A fitted, "
            "honest draft — the signature opening and frogs are the maker's placement.",
        "drafting": "fitted front + back on fold with a shaped side seam and marked waist "
            "darts; mandarin collar band solved to the neck run; asymmetric opening, frog "
            "positions, and side slits marked.",
    }
    return pattern


result = build()
