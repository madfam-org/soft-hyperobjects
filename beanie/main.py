"""
Beanie — Fashion Cabinet Garment Cartridge (FC-200 #191, accessory gap).

The knit beanie: a stretch tube that hugs the head, seamed up the back and gathered or darted
closed at the crown, with a folded ribbed brim. Cut with negative ease so it grips. This
cartridge drafts a single panel (cut on fold) whose width is the head girth minus stretch ease
and whose top edge closes into the crown; the brim is a marked fold. Distinct from FC-100's
structured caps (bucket-hat, five-panel-cap) — the beanie is a knit stretch cap.

Pieces:
  - panel : the beanie body (cut on fold at CB), crown-closing top + folded brim marked.

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

head_girth   = float(PARAM(lambda: head_girth, 560.0))
beanie_height = float(PARAM(lambda: beanie_height, 240.0))  # brim fold to crown
brim_fold    = float(PARAM(lambda: brim_fold, 60.0))       # folded ribbed brim depth
neg_ease     = float(PARAM(lambda: neg_ease, 40.0))        # negative ease so it grips
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(440.0, min(head_girth, 660.0))
beanie_height = max(160.0, min(beanie_height, 360.0))
brim_fold    = max(0.0, min(brim_fold, 140.0))
neg_ease     = max(0.0, min(neg_ease, 100.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# panel on the CB fold: half width = (head - neg_ease)/2
HALF = (head_girth - neg_ease) / 2.0
H = beanie_height + brim_fold                          # total cut height incl. the fold-under


def build_panel():
    internals = [fc.Internal("brim-fold", [fc.P(0.0, brim_fold), fc.P(HALF, brim_fold)],
                             kind="fold"),
                 fc.Internal("crown-gather", [fc.P(0.0, H - 20.0), fc.P(HALF, H - 20.0)],
                             kind="marking")]
    return fc.Piece(
        "panel",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("crown", [fc.Line(fc.P(0.0, H), fc.P(HALF, H))]),
            fc.Edge("join", [fc.Line(fc.P(HALF, H), fc.P(HALF, 0.0))]),
            fc.Edge("brim", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown", 1.0, "join"), fc.Notch("brim", 0.0, "join")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 20.0), fc.P(HALF * 0.5, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Beanie panel",
    )


def build():
    pattern = fc.PatternSet("beanie")
    pattern.add(build_panel())
    # the panel is cut on the CB fold; its two 'join' edges meet at CF — a balanced self-seam.
    pattern.declare_seam(("panel", "join"), ("panel", "center_back"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "rib knit or stretch jersey",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 82% marker; negative ease means it MUST stretch to grip."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "one back seam; gather or dart the crown closed; fold the ribbed brim."},
    ]
    pattern.metadata = {
        "fc200_rank": 191, "family": "accessories", "fabric_hint": "punto-rib",
        "silhouette_note": "A knit stretch cap: one panel seamed up the back, gathered closed at "
            "the crown, with a folded ribbed brim. Cut with negative ease so it hugs the head; "
            "the back seam is a balanced self-seam.",
        "solved": {"flat_half_mm": round(HALF, 1), "neg_ease_mm": round(neg_ease, 1)},
    }
    return pattern


result = build()
