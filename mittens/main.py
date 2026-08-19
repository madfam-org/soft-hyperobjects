"""
Mittens — Fashion Cabinet Garment Cartridge (FC-200 #134, accessory gap).

Warm mittens: a rounded hand pouch (all four fingers together) with a separate thumb and a
ribbed or folded cuff. Simpler and warmer than a five-finger glove — the fingers share one
chamber. This cartridge drafts a folded hand pouch (palm + back one piece, folded at the
rounded fingertip) with a set-in thumb and a cuff. Distinct from FC-100 (no gloves) and from the
work-glove (five fingers) — the mitten pools the fingers for warmth.

Pieces:
  - hand : folded rounded hand pouch (cut on fold at the fingertip), thumb hole marked.
  - thumb : the thumb piece (cut 2), set into the thumb hole.
  - cuff : ribbed/folded wrist cuff (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # hand|thumb|cuff|set

hand_length  = float(PARAM(lambda: hand_length, 180.0))    # wrist to fingertip
hand_span    = float(PARAM(lambda: hand_span, 210.0))
thumb_len    = float(PARAM(lambda: thumb_len, 60.0))
cuff_height  = float(PARAM(lambda: cuff_height, 70.0))
ease         = float(PARAM(lambda: ease, 30.0))            # a little room for warmth
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hand_length  = max(130.0, min(hand_length, 230.0))
hand_span    = max(160.0, min(hand_span, 280.0))
thumb_len    = max(40.0, min(thumb_len, 100.0))
cuff_height  = max(20.0, min(cuff_height, 160.0))
ease         = max(0.0, min(ease, 100.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

HALF = (hand_span + ease) / 2.0 / 2.0                  # quarter span = half flat pouch width
H = hand_length - cuff_height * 0.3                    # pouch height above the wrist


def build_hand():
    # rounded top (fingertip), straight sides, thumb hole marked on the lower side.
    internals = [
        fc.Internal("thumb-hole", [fc.P(HALF, cuff_height * 0.4),
                                   fc.P(HALF, cuff_height * 0.4 + thumb_len)], kind="marking"),
        fc.Internal("fold-tip", [fc.P(-HALF, H), fc.P(HALF, H)], kind="fold"),
    ]
    return fc.Piece(
        "hand",
        [
            fc.Edge("side_l", [fc.Line(fc.P(-HALF, 0.0), fc.P(-HALF, H - 40.0))]),
            # rounded top: curve from the left side up over the tip to the right side
            fc.Edge("tip", [fc.curve_through(fc.P(-HALF, H - 40.0), fc.P(HALF, H - 40.0),
                                             bulge=0.35, side=1.0)]),
            fc.Edge("side_r", [fc.Line(fc.P(HALF, H - 40.0), fc.P(HALF, 0.0))]),
            fc.Edge("wrist", [fc.Line(fc.P(HALF, 0.0), fc.P(-HALF, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_r", 0.1, "thumb"), fc.Notch("wrist", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, H - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="tip", mirror=True),
        label="Hand pouch",
    )


def build_thumb():
    base = 60.0
    tl = thumb_len + 20.0
    return fc.Piece(
        "thumb",
        [
            fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(base, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(base, 0.0), fc.P(base * 0.55, tl))]),
            fc.Edge("tip", [fc.curve_through(fc.P(base * 0.55, tl), fc.P(base * 0.45, tl),
                                             bulge=0.5, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(base * 0.45, tl), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(base * 0.5, 8.0), fc.P(base * 0.5, tl - 8.0)),
        cut=fc.CutSpec(quantity=2),
        label="Thumb",
    )


def build_cuff():
    ln = hand_span * 0.9
    h = cuff_height * 2.0
    return fc.Piece(
        "cuff",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Cuff",
    )


def build():
    pattern = fc.PatternSet("mittens")
    everything = target_piece == "set"
    if everything or target_piece == "hand":
        pattern.add(build_hand())
    if everything or target_piece == "thumb":
        pattern.add(build_thumb())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())

    fabric_width = 1000.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.64)
    pattern.bom = [
        {"item": "fleece, boiled wool, or quilted fabric",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1000 mm width, 64% marker; a warm, wind-resistant hand fabric."},
        {"item": "lining (optional)", "qty": 1, "unit": "as chosen",
         "note": "a soft lining adds warmth; the maker's option."},
        {"item": "rib for the cuff (optional)", "qty": 1, "unit": "as chosen",
         "note": "a rib or folded cuff keeps the wind out at the wrist."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "seam the pouch, set the thumb, attach the cuff."},
    ]
    pattern.metadata = {
        "fc200_rank": 134, "family": "accessories", "fabric_hint": "polar-lana",
        "silhouette_note": "A rounded hand pouch pooling all four fingers in one warm chamber, "
            "with a set-in thumb and a cuff. Folded at the rounded fingertip; simpler and warmer "
            "than a five-finger glove.",
        "solved": {"pouch_half_mm": round(HALF, 1), "pouch_height_mm": round(H, 1)},
    }
    return pattern


result = build()
