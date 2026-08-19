"""
Off-Shoulder Top — Fashion Cabinet Garment Cartridge (FC-200 #184, neckline gap).

The off-shoulder (bardot) top: a wide horizontal neckline that sits below the shoulders on the
upper arm, held up by an elasticated top edge (often with a short flounce), so the shoulders are
bare. Front and back are the same wide panel (the neckline is a straight elasticated top edge
across both), so the shoulder "seam" is really the continuous top casing and the side seams
balance by construction. A soft-goods garment — no hardware.

Pieces:
  - front / back : wide body panels (cut on fold) with an elasticated straight top edge.

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

chest_girth  = float(PARAM(lambda: chest_girth, 960.0))
top_length   = float(PARAM(lambda: top_length, 520.0))     # top edge to hem
sleeve_grown = float(PARAM(lambda: sleeve_grown, 180.0))   # short grown sleeve off the shoulder
flounce      = float(PARAM(lambda: flounce, 90.0))         # depth of the top flounce/ruffle
ease         = float(PARAM(lambda: ease, 160.0))           # blousy ease (elastic gathers it)
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(660.0, min(chest_girth, 1500.0))
top_length   = max(320.0, min(top_length, 800.0))
sleeve_grown = max(60.0, min(sleeve_grown, 320.0))
flounce      = max(0.0, min(flounce, 220.0))
ease         = max(80.0, min(ease, 420.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = top_length
HALF = (chest_girth + ease) / 2.0 / 2.0
SLEEVE_X = HALF + sleeve_grown


def _panel(name, label):
    top_y = L + flounce                              # flounce sits above the body top line
    body_top = L
    internals = [fc.Internal("elastic-casing", [fc.P(0.0, body_top), fc.P(SLEEVE_X, body_top)],
                             kind="marking")]
    if flounce > 0.0:
        internals.append(fc.Internal("flounce-fold", [fc.P(0.0, top_y), fc.P(SLEEVE_X, top_y)],
                                     kind="fold"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, top_y), fc.P(SLEEVE_X, top_y))]),
            fc.Edge("sleeve_end", [fc.Line(fc.P(SLEEVE_X, top_y),
                                           fc.P(SLEEVE_X, body_top - 60.0))]),
            fc.Edge("sleeve_under", [fc.Line(fc.P(SLEEVE_X, body_top - 60.0),
                                             fc.P(HALF, body_top - 190.0))]),
            fc.Edge("side", [fc.Line(fc.P(HALF, body_top - 190.0), fc.P(HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("top", 0.5, "centre"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("off-shoulder-top")
    everything = target_piece == "set"
    front = _panel("front", "Front")
    back = _panel("back", "Back")
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        # the top edge is a continuous elasticated casing across both panels (joined at the
        # sleeve ends); the sewn seams are the underarm and the side.
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "soft drapey woven or knit (rayon, jersey)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; a fluid fabric blouses over the elastic."},
        {"item": "top-edge elastic", "qty": 1, "unit": "as measured",
         "note": "elastic in the top casing holds the neckline on the upper arm."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "casing the top edge + optional flounce."},
    ]
    pattern.metadata = {
        "fc200_rank": 184, "family": "knit_tops", "fabric_hint": "rayon-jersey",
        "silhouette_note": "A wide, straight, elasticated top edge that sits below the shoulders "
            "(bardot line) with an optional flounce, held on the upper arm by the casing elastic. "
            "Front and back are the same wide panel; underarm and side seams balance.",
        "solved": {"body_half_mm": round(HALF, 1), "flounce_mm": round(flounce, 1)},
    }
    return pattern


result = build()
