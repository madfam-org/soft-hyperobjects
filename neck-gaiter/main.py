"""
Neck Gaiter — Fashion Cabinet Garment Cartridge (FC-200 #192, accessory gap).

The neck gaiter (buff/tube scarf): a simple stretch tube worn around the neck and pulled up
over the face, seamed into a loop. This cartridge drafts a single rectangular panel (cut on
fold) whose circumference is the head/neck girth (so it pulls over the head) and whose height is
the coverage; the one seam joins it into a tube. Distinct from FC-100 (no scarves) — the simplest
worn tube. Front and back are the same panel with one balanced join seam.

Pieces:
  - panel : the gaiter tube (cut on fold), one join seam into a loop.

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

head_girth   = float(PARAM(lambda: head_girth, 580.0))    # must pull over the head
gaiter_height = float(PARAM(lambda: gaiter_height, 380.0)) # neck-to-nose coverage
neg_ease     = float(PARAM(lambda: neg_ease, 40.0))       # slight negative ease (stretch)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(480.0, min(head_girth, 700.0))
gaiter_height = max(200.0, min(gaiter_height, 560.0))
neg_ease     = max(0.0, min(neg_ease, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

HALF = (head_girth - neg_ease) / 2.0
H = gaiter_height


def build_panel():
    return fc.Piece(
        "panel",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, H), fc.P(HALF, H))]),
            fc.Edge("join", [fc.Line(fc.P(HALF, H), fc.P(HALF, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance, "bottom": hem_allowance},
        notches=[fc.Notch("top", 1.0, "join"), fc.Notch("bottom", 0.0, "join")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 20.0), fc.P(HALF * 0.5, H - 20.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Gaiter tube",
    )


def build():
    pattern = fc.PatternSet("neck-gaiter")
    pattern.add(build_panel())
    pattern.declare_seam(("panel", "join"), ("panel", "center_back"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.84)
    pattern.bom = [
        {"item": "stretch jersey, fleece, or merino knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 84% marker; must stretch to pull over the head."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "one join seam; narrow hem or raw-edge the top and bottom (knit)."},
    ]
    pattern.metadata = {
        "fc200_rank": 192, "family": "accessories", "fabric_hint": "punto-merino",
        "silhouette_note": "The simplest worn tube: a stretch loop that covers the neck and pulls "
            "up over the face. Circumference == head girth so it pulls over; one balanced join "
            "seam; front and back are the same panel.",
        "solved": {"flat_half_mm": round(HALF, 1), "coverage_mm": round(H, 1)},
    }
    return pattern


result = build()
