"""
Side-Opening Top — Fashion Cabinet Garment Cartridge (FC-200 #149, adaptive; y4d magnetic-clasp).

An adaptive pull-on-free top: a relaxed front + back where ONE side seam and the matching
sleeve underarm open fully, closed by a run of magnetic clasps, so the garment can be
dressed one-handed or seated without raising the arms over the head. The magnetic-clasp
SOLID is Yantra4D territory (`magnetic-clasp`; see the manifest's notion.hardware_ref).
Fashion Cabinet owns the garment + the clasp placement.

Adaptive design is the point: the open side + magnetic closure replaces the overhead
motion and the fine-motor fastening a conventional top demands.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 1040.0))  # full chest
top_length   = float(PARAM(lambda: top_length, 680.0))    # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 200.0))    # wide, easy neck opening
sleeve_grown = float(PARAM(lambda: sleeve_grown, 170.0))  # grown cap sleeve
ease         = float(PARAM(lambda: ease, 140.0))          # generous, easy fit
clasps       = int(  PARAM(lambda: clasps, 6))            # magnetic clasps down the open side
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(700.0, min(chest_girth, 1600.0))
top_length   = max(450.0, min(top_length, 950.0))
neck_width   = max(140.0, min(neck_width, 360.0))
sleeve_grown = max(60.0, min(sleeve_grown, 280.0))
ease         = max(60.0, min(ease, 400.0))
clasps       = max(2, min(clasps, 12))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SHOULDER_X = HALF
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 230.0


def _panel(name, neck_dip, is_open_side, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 110.0)
    body_side_top = fc.P(SHOULDER_X, top_y - SLEEVE_DROP)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
        fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
        fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
        fc.Edge("side", [fc.Line(body_side_top, fc.P(SHOULDER_X, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(SHOULDER_X, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if is_open_side:
        # Magnetic-clasp positions down the open side seam (the adaptive opening).
        for i in range(clasps):
            t = i / max(clasps - 1, 1)
            y = (top_y - SLEEVE_DROP) * (1.0 - t)
            internals.append(fc.Internal("clasp-mark",
                                         [fc.P(SHOULDER_X - 6.0, y), fc.P(SHOULDER_X, y)],
                                         kind="drill"))
        internals.append(fc.Internal("open-side-note",
                                     [fc.P(SHOULDER_X, 0.0),
                                      fc.P(SHOULDER_X, top_y - SLEEVE_DROP)], kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("side-opening-top")
    front = _panel("front", 60.0, True, "Front (open side + clasps)")
    back = _panel("back", 25.0, False, "Back")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        # NOTE: only ONE side seam is sewn; the other is the magnetic-clasp opening. The
        # panels are symmetric so the side edges balance regardless of which side opens.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "jersey or soft woven", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length", "note": "≈ at 1600 mm width, 75% marker; soft, easy-wear fabric."},
        {"item": "magnetic clasps", "qty": clasps, "unit": "sets",
         "note": "Yantra4D magnetic-clasp (see notion.hardware_ref) down the open side."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "flat, soft seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 149, "family": "knit_tops", "fabric_hint": "jersey-algodon",
        "adaptive_note": "One side seam + sleeve underarm open fully and close with magnetic "
            "clasps, so the top is dressed one-handed or seated without the overhead motion "
            "and fine-motor fastening a conventional top demands. Clasp positions are marked; "
            "the printable clasp is the Yantra4D solid.",
        "hardware": "side closure via Yantra4D (notion.hardware_ref -> magnetic-clasp)",
    }
    return pattern


result = build()
