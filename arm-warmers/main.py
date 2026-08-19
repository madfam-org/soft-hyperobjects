"""
Arm Warmers — Fashion Cabinet Garment Cartridge (FC-200 #135, accessory gap).

Knit arm warmers: tapered stretch tubes worn on the forearms from wrist to above the elbow,
often with a thumbhole, for warmth without a full sleeve. This cartridge drafts a single tapered
panel (cut on fold) whose ends match the wrist and upper-arm girths minus stretch ease, seamed
into a tube, with a thumbhole marked at the wrist. Distinct from FC-100 (no arm warmers). Front
and back are the same panel with one balanced join seam.

Pieces:
  - panel : the tapered arm-warmer tube (cut on fold), thumbhole marked, one join seam.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # panel|set

wrist_girth  = float(PARAM(lambda: wrist_girth, 170.0))
upper_girth  = float(PARAM(lambda: upper_girth, 300.0))    # above the elbow
warmer_length = float(PARAM(lambda: warmer_length, 420.0)) # wrist to above elbow
neg_ease     = float(PARAM(lambda: neg_ease, 30.0))        # negative ease so it stays up
thumbhole    = int(  PARAM(lambda: thumbhole, 1))          # 1 = mark a thumbhole
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
wrist_girth  = max(120.0, min(wrist_girth, 240.0))
upper_girth  = max(200.0, min(upper_girth, 460.0))
warmer_length = max(250.0, min(warmer_length, 620.0))
neg_ease     = max(0.0, min(neg_ease, 80.0))
thumbhole    = 1 if thumbhole else 0
seam_allowance = max(0.0, min(seam_allowance, 16.0))

WRIST_HALF = (wrist_girth - neg_ease) / 2.0
UPPER_HALF = (upper_girth - neg_ease) / 2.0
H = warmer_length


def build_panel():
    internals = []
    if thumbhole:
        internals.append(fc.Internal("thumbhole", [fc.P(WRIST_HALF, 30.0), fc.P(WRIST_HALF, 80.0)],
                                     kind="marking"))
    return fc.Piece(
        "panel",
        [
            # tapered: wrist edge (narrow) at bottom, upper edge (wide) at top; the join edge is
            # the slanted side, and the fold is the other side.
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, H), fc.P(UPPER_HALF, H))]),
            fc.Edge("join", [fc.Line(fc.P(UPPER_HALF, H), fc.P(WRIST_HALF, 0.0))]),
            fc.Edge("wrist", [fc.Line(fc.P(WRIST_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("wrist", 1.0, "join"), fc.Notch("upper", 1.0, "join")],
        grainline=fc.Grainline(fc.P(WRIST_HALF * 0.4, 20.0), fc.P(UPPER_HALF * 0.4, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Arm-warmer tube",
    )


def build():
    pattern = fc.PatternSet("arm-warmers")
    pattern.add(build_panel())
    # cut on the fold; the 'join' edge sews to its own mirror at the inner arm — a balanced
    # self-seam (join == join by construction).
    pattern.declare_seam(("panel", "join"), ("panel", "join"), tol=2.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "rib knit or stretch jersey",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 70% marker; a pair (cut 2); negative ease keeps them up."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "one join seam each; coverstitch or fold the wrist and upper edges."},
    ]
    pattern.metadata = {
        "fc200_rank": 135, "family": "accessories", "fabric_hint": "punto-rib",
        "silhouette_note": "Tapered stretch tubes from wrist to above the elbow with an optional "
            "thumbhole, for warmth without a full sleeve. Front and back are the same tapered "
            "panel with one balanced join seam.",
        "solved": {"wrist_half_mm": round(WRIST_HALF, 1), "upper_half_mm": round(UPPER_HALF, 1),
                   "thumbhole": bool(thumbhole)},
    }
    return pattern


result = build()
