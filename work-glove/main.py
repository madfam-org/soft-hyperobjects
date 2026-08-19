"""
Work Glove — Fashion Cabinet Garment Cartridge (FC-200 #197, accessory gap).

A protective work glove drafted in the traditional trank style: a single hand-shaped "trank"
folded at the fingertips so palm and back are one piece, with four fingers marked as slits, plus
a separate thumb piece set into a thumb hole. This is a simplified, honest teaching draft of a
real glove — the fingers are marked for the maker to cut and the fourchettes (side-of-finger
gussets) are left as an advanced option noted in the README. Sized from hand length and span.

Pieces:
  - trank : the folded hand piece (cut 1, folds at the fingertips); finger slits + thumb marked.
  - thumb : the thumb piece (cut 1), set into the thumb hole.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # trank|thumb|set

hand_length  = float(PARAM(lambda: hand_length, 190.0))    # wrist crease to middle fingertip
hand_span    = float(PARAM(lambda: hand_span, 210.0))      # around the palm (girth)
finger_len   = float(PARAM(lambda: finger_len, 80.0))      # middle finger length
cuff_len     = float(PARAM(lambda: cuff_len, 70.0))        # gauntlet cuff beyond the wrist
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hand_length  = max(140.0, min(hand_length, 240.0))
hand_span    = max(160.0, min(hand_span, 280.0))
finger_len   = max(55.0, min(finger_len, 110.0))
cuff_len     = max(0.0, min(cuff_len, 200.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

PALM_HALF = hand_span / 2.0 / 2.0                      # quarter span = half the flat trank width
PALM_LEN = hand_length - finger_len                    # wrist to finger base
FULL_H = PALM_LEN + finger_len                         # to the fingertip (fold line)


def build_trank():
    # The trank is symmetric about the fold at the fingertips (top). We draft the flat piece from
    # the cuff bottom up to the fingertip fold; folded, palm and back mirror. Four finger slits
    # are marked from the finger base to near the tip; a thumb hole is marked at the lower side.
    W = PALM_HALF * 2.0
    internals = []
    base_y = PALM_LEN
    # 3 internal finger slits dividing the top into 4 fingers
    for i in range(1, 4):
        x = -PALM_HALF + W * i / 4.0
        internals.append(fc.Internal(f"finger-slit-{i}",
                                     [fc.P(x, base_y), fc.P(x, FULL_H - 12.0)], kind="marking"))
    # thumb hole marked on the lower-right side
    th_y = cuff_len + 30.0
    internals.append(fc.Internal("thumb-hole",
                                 [fc.P(PALM_HALF, th_y), fc.P(PALM_HALF, th_y + 70.0)],
                                 kind="marking"))
    internals.append(fc.Internal("fingertip-fold",
                                 [fc.P(-PALM_HALF, FULL_H), fc.P(PALM_HALF, FULL_H)],
                                 kind="fold"))
    return fc.Piece(
        "trank",
        [
            fc.Edge("side_l", [fc.Line(fc.P(-PALM_HALF, 0.0), fc.P(-PALM_HALF, FULL_H))]),
            fc.Edge("fingertip", [fc.Line(fc.P(-PALM_HALF, FULL_H), fc.P(PALM_HALF, FULL_H))]),
            fc.Edge("side_r", [fc.Line(fc.P(PALM_HALF, FULL_H), fc.P(PALM_HALF, 0.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(PALM_HALF, 0.0), fc.P(-PALM_HALF, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cuff": 12.0},
        notches=[fc.Notch("side_r", 0.2, "thumb"), fc.Notch("fingertip", 0.5, "fold centre")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, FULL_H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fingertip", mirror=True),
        label="Trank (folded hand)",
    )


def build_thumb():
    # a simple tapered thumb piece: base sews into the thumb hole, folds to a tip.
    base = 70.0
    tlen = finger_len + 20.0
    return fc.Piece(
        "thumb",
        [
            fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(base, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(base, 0.0), fc.P(base * 0.6, tlen))]),
            fc.Edge("tip", [fc.Line(fc.P(base * 0.6, tlen), fc.P(base * 0.4, tlen))]),
            fc.Edge("side_l", [fc.Line(fc.P(base * 0.4, tlen), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(base * 0.5, 10.0), fc.P(base * 0.5, tlen - 10.0)),
        cut=fc.CutSpec(quantity=1),
        label="Thumb",
    )


def build():
    pattern = fc.PatternSet("work-glove")
    everything = target_piece == "set"
    if everything or target_piece == "trank":
        pattern.add(build_trank())
    if everything or target_piece == "thumb":
        pattern.add(build_thumb())

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)        # small pieces, lots of waste
    pattern.bom = [
        {"item": "split leather, suede, or heavy canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 60% marker; a tough, abrasion-resistant hand material."},
        {"item": "reinforcement patch (palm)", "qty": 1, "unit": "as marked",
         "note": "an extra palm layer for wear; the maker's option."},
        {"item": "gauntlet cuff + closure", "qty": 1, "unit": "set",
         "note": "the cuff extends over the wrist; a strap or elastic is optional."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "topstitch the fingers and set the thumb; a glover's needle helps with leather."},
    ]
    pattern.metadata = {
        "fc200_rank": 197, "family": "accessories", "fabric_hint": "piel-lona",
        "silhouette_note": "A trank-style work glove: a folded hand piece (palm+back one piece) "
            "with four fingers marked as slits and a set-in thumb, plus a gauntlet cuff. A "
            "simplified teaching draft; fourchette gussets are an advanced option (see README).",
        "solved": {"palm_half_mm": round(PALM_HALF, 1), "full_height_mm": round(FULL_H, 1),
                   "finger_len_mm": round(finger_len, 1)},
    }
    return pattern


result = build()
