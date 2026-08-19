"""
Balaclava — Fashion Cabinet Garment Cartridge (FC-200 #195, accessory gap).

The knit balaclava (ski mask): a close hood that covers the head and neck with a face opening,
seamed up the back and under the chin. This cartridge drafts a single hood panel (cut on fold at
CB) with a shaped face opening cut into the front edge and a neck extension, in a stretch knit
with negative ease so it hugs. Distinct from FC-100's hoodie hoods (which are open) — the
balaclava wraps the whole head with just the face exposed.

Pieces:
  - hood : the balaclava panel (cut on fold at CB), face opening + neck, back self-seam.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # hood|set

head_girth   = float(PARAM(lambda: head_girth, 580.0))
face_height  = float(PARAM(lambda: face_height, 460.0))   # crown to neck-base coverage
face_open_w  = float(PARAM(lambda: face_open_w, 130.0))   # face opening half-width
face_open_h  = float(PARAM(lambda: face_open_h, 150.0))   # face opening height
neg_ease     = float(PARAM(lambda: neg_ease, 50.0))       # negative ease (stretch)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(480.0, min(head_girth, 680.0))
face_height  = max(360.0, min(face_height, 600.0))
face_open_w  = max(80.0, min(face_open_w, 200.0))
face_open_h  = max(90.0, min(face_open_h, 230.0))
neg_ease     = max(0.0, min(neg_ease, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HALF = (head_girth - neg_ease) / 2.0
H = face_height
FACE_Y = H * 0.55                                      # centre of the face opening


def build_hood():
    # panel on the CB fold. Front edge (CF) has the face opening cut into it: the front edge
    # runs up from the neck, in around the face opening, and up to the crown.
    face_lo = FACE_Y - face_open_h / 2.0
    face_hi = FACE_Y + face_open_h / 2.0
    internals = [fc.Internal("face-opening",
                             [fc.P(0.0, face_lo), fc.P(face_open_w, face_lo),
                              fc.P(face_open_w, face_hi), fc.P(0.0, face_hi)], kind="marking")]
    return fc.Piece(
        "hood",
        [
            # CF/front edge from neck up, indenting around the face hole, to the crown
            fc.Edge("center_front",
                    [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, face_lo)),
                     fc.Line(fc.P(0.0, face_lo), fc.P(face_open_w, face_lo)),
                     fc.Line(fc.P(face_open_w, face_lo), fc.P(face_open_w, face_hi)),
                     fc.Line(fc.P(face_open_w, face_hi), fc.P(0.0, face_hi)),
                     fc.Line(fc.P(0.0, face_hi), fc.P(0.0, H))]),
            fc.Edge("crown", [fc.Line(fc.P(0.0, H), fc.P(HALF, H))]),
            fc.Edge("back", [fc.Line(fc.P(HALF, H), fc.P(HALF, 0.0))]),
            fc.Edge("neck", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("crown", 1.0, "back"), fc.Notch("neck", 1.0, "back")],
        grainline=fc.Grainline(fc.P(HALF * 0.6, 20.0), fc.P(HALF * 0.6, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_front", mirror=True),
        label="Balaclava hood",
    )


def build():
    pattern = fc.PatternSet("balaclava")
    pattern.add(build_hood())
    # cut on the CF fold; the mirrored copy's 'back' edge meets this 'back' edge at CB — a
    # balanced self-seam (back == back by construction).
    pattern.declare_seam(("hood", "back"), ("hood", "back"), tol=1.5)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "merino, fleece, or stretch technical knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 74% marker; negative ease means it MUST stretch to hug."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "one back seam; bind or coverstitch the face opening and neck edges."},
    ]
    pattern.metadata = {
        "fc200_rank": 195, "family": "accessories", "fabric_hint": "punto-merino",
        "silhouette_note": "A close knit hood covering head and neck with a shaped face opening, "
            "seamed up the back. Cut with negative ease so it hugs; the back is a balanced "
            "self-seam. The whole head is wrapped with just the face exposed.",
        "solved": {"flat_half_mm": round(HALF, 1),
                   "face_open_mm": [face_open_w * 2.0, face_open_h]},
    }
    return pattern


result = build()
