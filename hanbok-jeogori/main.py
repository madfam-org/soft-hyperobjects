"""
Hanbok Jeogori — Fashion Cabinet Garment Cartridge (FC-200 rank #143, Korean heritage).

The jeogori is the short upper jacket of the hanbok, worn by all genders: a high-waisted,
boxy top with wide straight-cut sleeves, a wrapped front closed by the goreum (a long
ribbon tie), and the git — a folded band edging the collar and front — traditionally
tipped with the white dongjeong. Its lines are gentle: mostly straight panels with a
softly curved sleeve underarm and hem.

This cartridge drafts the garment geometry: a back panel, two wrapped front panels, wide
rectangular sleeves on a straight dropped armhole, the git band solved to the collar run,
and the goreum ties. Offered with respect for the living tradition; the maker supplies the
silk, the colour pairings (saekdong is a notable variant), and the dongjeong tipping.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|git|goreum|set

chest_girth   = float(PARAM(lambda: chest_girth, 960.0))    # full chest
jeogori_length = float(PARAM(lambda: jeogori_length, 380.0))  # nape to the short hem (high-waisted)
back_neck     = float(PARAM(lambda: back_neck, 180.0))      # back-neck width
sleeve_length = float(PARAM(lambda: sleeve_length, 480.0))  # shoulder to sleeve opening
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 260.0))   # armhole drop (straight sleevehead)
wrap_ease     = float(PARAM(lambda: wrap_ease, 180.0))      # total wrap/fit ease
git_width     = float(PARAM(lambda: git_width, 55.0))       # finished collar-band width
goreum_length = float(PARAM(lambda: goreum_length, 900.0))  # long ribbon tie length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth    = max(650.0, min(chest_girth, 1500.0))
jeogori_length = max(250.0, min(jeogori_length, 600.0))
back_neck      = max(120.0, min(back_neck, 300.0))
sleeve_length  = max(250.0, min(sleeve_length, 700.0))
sleeve_depth   = max(180.0, min(sleeve_depth, 420.0))
wrap_ease      = max(100.0, min(wrap_ease, 420.0))
git_width      = max(35.0, min(git_width, 90.0))
goreum_length  = max(500.0, min(goreum_length, 1300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

L = jeogori_length
BODY = (chest_girth + wrap_ease) / 2.0             # half-girth incl ease = back + one front
BW = BODY / 2.0                                     # back-on-fold half-width
# The front panel matches the back's structural width (BW) so the shoulder, armhole, and
# side seams balance by construction. The jeogori's wrap overlap is achieved by the two
# fronts crossing over each other at the CF (covered by the git band), NOT by a wider
# front panel — widening the shoulder would unbalance the shoulder seam.
FW = BW
NECK_HALF = back_neck / 2.0


def build_back():
    """Back rectangle, cut on fold at CB, with a shallow back-neck scoop and a straight
    dropped-shoulder armhole."""
    top_y = L
    neck_out = fc.P(NECK_HALF, top_y)
    neck = fc.Edge("neck", [fc.curve_through(fc.P(0.0, top_y), neck_out, bulge=0.12, side=-1.0)])
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, top_y), fc.P(BW, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, top_y - sleeve_depth), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 60.0), fc.P(BW * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    """Front panel (cut 2 mirror). The inner (CF) edge is straight full-length — the git
    band covers it and it wraps across the body. Straight shoulder + straight armhole.
    The hem rises gently toward CF (the jeogori's soft front line)."""
    top_y = L
    side_x = FW
    neck_out = fc.P(NECK_HALF, top_y)
    # Hem curves up from the side hem to a slightly higher CF hem point.
    cf_hem = fc.P(0.0, 30.0)
    hem = fc.Edge("hem", [fc.curve_through(fc.P(side_x, 0.0), cf_hem, bulge=0.10, side=1.0)])
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(cf_hem, fc.P(0.0, top_y))]),
            fc.Edge("neck", [fc.Line(fc.P(0.0, top_y), neck_out)]),
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(side_x, top_y))]),
            fc.Edge("armhole", [fc.Line(fc.P(side_x, top_y), fc.P(side_x, top_y - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(side_x, top_y - sleeve_depth), fc.P(side_x, 0.0))]),
            hem,
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(side_x * 0.5, 60.0), fc.P(side_x * 0.5, L - 80.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_sleeve():
    """Wide straight sleeve (cut 2 mirror). Straight sleevehead of height sleeve_depth
    (dropped shoulder) matching the straight armholes; the opposite edge is the opening."""
    head_h = sleeve_depth
    sw = sleeve_length
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, 0.0))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(sw, 0.0), fc.P(sw, head_h))]),
            fc.Edge("shoulder_fold", [fc.Line(fc.P(sw, head_h), fc.P(0.0, head_h))]),
            fc.Edge("opening", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"opening": hem_allowance},
        notches=[fc.Notch("sleevehead", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.25), fc.P(sw * 0.5, head_h * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
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


def build_git(collar_run):
    """The git: a folded collar band running down the right front, around the back neck,
    and down the left front — solved to the measured collar run."""
    flat = _solve_flat(_band_inner_edge, collar_run, "git inner-edge")
    inner = _band_inner_edge(flat)
    return fc.Piece(
        "git",
        [
            inner,
            fc.Edge("end_b", [fc.Line(fc.P(flat, 0.0), fc.P(flat, git_width))]),
            fc.Edge("outer", [fc.Line(fc.P(flat, git_width), fc.P(0.0, git_width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, git_width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", 0.5, "centre back neck")],
        grainline=fc.Grainline(fc.P(flat * 0.5, git_width * 0.5),
                               fc.P(flat * 0.5 + 100.0, git_width * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Git (collar band)",
    )


def _strip(name, length, width, qty, label):
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0), fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("hanbok-jeogori")
    front = build_front()
    back = build_back()
    # Collar run = both fronts' CF edges + the back neck.
    collar_run = 2.0 * front.edge("center_front").length(0.05) + back.edge("neck").length(0.05)

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces or target_piece == "git":
        pattern.add(build_git(collar_run))
    if all_pieces or target_piece == "goreum":
        # Two ties: one wide/long outer goreum + one shorter inner tie.
        pattern.add(_strip("goreum", goreum_length, 90.0, 1, "Goreum (outer tie)"))
        pattern.add(_strip("goreum_inner", goreum_length * 0.7, 60.0, 1, "Inner Tie"))

    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam([("sleeve", "sleevehead"), ("sleeve", "sleevehead")],
                             [("front", "armhole"), ("back", "armhole")], tol=1.5)
        pattern.declare_seam(
            [("git", "inner")],
            [("front", "center_front"), ("front", "center_front"), ("back", "neck")],
            tol=1.5)

    fabric_width = 1100.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "silk or ramie (hanbok cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1100 mm width, 68% marker; colour pairings (e.g. saekdong stripes) "
                 "and the white dongjeong collar tip are the maker's."},
        {"item": "dongjeong (white collar tip)", "qty": 1, "unit": "strip",
         "note": "the detachable white band tipping the git — traditional, the maker's."},
        {"item": "all-purpose + silk thread", "qty": 1, "unit": "set", "note": "straight seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 143,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "heritage_note": "The jeogori is the upper jacket of the Korean hanbok, a living "
            "garment. This cartridge drafts the GARMENT GEOMETRY only — the silk, the "
            "colour pairings (saekdong), and the white dongjeong collar tip that carry its "
            "identity are the maker's to supply. Offered with respect.",
        "solved": {"git_inner_edge_mm": round(_band_inner_edge(
            _solve_flat(_band_inner_edge, collar_run, "git")).length(0.05), 1),
            "collar_run_target_mm": round(collar_run, 1)},
        "drafting": "back on fold + two wrapped fronts (curved soft hem) + wide straight "
            "sleeves on a straight dropped armhole + the git collar band solved to the "
            "collar run + goreum ties. Gentle curves at the back neck and front hem.",
    }
    return pattern


result = build()
