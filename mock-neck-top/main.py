"""
Mock-Neck Top — Fashion Cabinet Garment Cartridge (FC-200 #164, everyday silhouette gap).

A fitted knit top with a MOCK neck: a short stand collar (a single band, ~50-70 mm) that
stands at the neck without folding over — unlike a turtleneck, which is tall and folds. The
body is a clean front + back with a set neckline; the mock-neck band is a separate strip whose
length equals the measured neckline so it eases on without gaps. Front and back share the body
width so the shoulder and side seams balance by construction.

Pieces:
  - front / back : fitted body panels with a jewel neckline (cut on fold).
  - band         : the short mock-neck stand strip, length == neckline.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|band|set

chest_girth  = float(PARAM(lambda: chest_girth, 940.0))    # full chest
top_length   = float(PARAM(lambda: top_length, 620.0))     # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 170.0))     # jewel neck width
mock_height  = float(PARAM(lambda: mock_height, 60.0))     # stand height (short — not a turtleneck)
sleeve_grown = float(PARAM(lambda: sleeve_grown, 150.0))   # grown cap sleeve
ease         = float(PARAM(lambda: ease, 70.0))            # close knit fit
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(640.0, min(chest_girth, 1500.0))
top_length   = max(420.0, min(top_length, 880.0))
neck_width   = max(130.0, min(neck_width, 300.0))
mock_height  = max(35.0, min(mock_height, 110.0))
sleeve_grown = max(60.0, min(sleeve_grown, 260.0))
ease         = max(0.0, min(ease, 260.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 210.0
FRONT_NECK_DIP = 60.0
BACK_NECK_DIP = 24.0


def _body(name, neck_dip, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 100.0)
    body_side_top = fc.P(HALF, top_y - SLEEVE_DROP)
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
            fc.Edge("side", [fc.Line(body_side_top, fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _neckline_len(front, back):
    """Measured neckline (full): both front and back neck edges, times 2 for the mirrored
    halves. The band length matches this so it eases on cleanly."""
    fn = next(e for e in front.edges if e.name == "neck").length()
    bn = next(e for e in back.edges if e.name == "neck").length()
    return (fn + bn) * 2.0


def build_band(neck_len):
    h = mock_height * 2.0                            # cut double-height, folds to mock_height
    ln = neck_len                                     # stand length == neckline
    return fc.Piece(
        "band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back"), fc.Notch("attach", 0.25, "shoulder")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Mock-neck band",
    )


def build():
    pattern = fc.PatternSet("mock-neck-top")
    all_pieces = target_piece == "set"
    front = _body("front", FRONT_NECK_DIP, "Front")
    back = _body("back", BACK_NECK_DIP, "Back")
    neck_len = _neckline_len(front, back)
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "band":
        pattern.add(build_band(neck_len))
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "stretch knit (interlock / ponte / rib)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 76% marker; a stable knit with recovery at the neck."},
        {"item": "rib for the mock band (optional)", "qty": 1, "unit": "as chosen",
         "note": "a rib band gives the mock neck its snug stand and recovery."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "knit seams; a coverstitch or twin needle finishes hems."},
    ]
    pattern.metadata = {
        "fc200_rank": 164, "family": "knit_tops", "fabric_hint": "punto-ponte",
        "silhouette_note": "A short stand collar (~50-70 mm) that stands at the neck without "
            "folding — the mock neck, distinct from a tall folding turtleneck. The band length "
            "is solved to the measured neckline so it eases on without gaps.",
        "solved": {"neckline_len_mm": round(neck_len, 1), "mock_height_mm": round(mock_height, 1)},
    }
    return pattern


result = build()
