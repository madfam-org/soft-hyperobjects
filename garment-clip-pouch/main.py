"""
Garment-clip travel pouch — Fashion Cabinet Cartridge (FC-500 #420, care_keeping, T1).

A slim flat pouch that carries a handful of printed garment clips (the Yantra4D `garment-clip`
solids — the sprung fabric clips that hold a hem or a stack while sewing) so they travel to a
class or a fitting without scattering. A FRONT and a BACK panel make the pouch, a top FLAP
folds over, and a divided inner keeps the clips from tangling. Sized so the clips lie flat in
a single layer.

Solved, not guessed:

  1. THE POUCH IS CUT TO THE CLIP FOOTPRINT. The pouch width holds a row of clips laid on
     their side (clip length x count), plus a margin; the height holds one clip depth plus the
     flap. Measured from the clip, floored so it always holds at least a couple.
  2. THE FLAP IS CLAMPED shorter than the pouch height so the mouth is never sealed shut.
  3. THE DIVIDER COUNT is derived from the clip count, floored at 1.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|set

clip_count = int(PARAM(lambda: clip_count, 8))
clip_length = float(PARAM(lambda: clip_length, 45.0))
clip_width = float(PARAM(lambda: clip_width, 12.0))
rows = int(PARAM(lambda: rows, 2))
flap = float(PARAM(lambda: flap, 45.0))
margin = float(PARAM(lambda: margin, 20.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

clip_count = max(2, min(clip_count, 24))
clip_length = max(20.0, min(clip_length, 90.0))
clip_width = max(6.0, min(clip_width, 30.0))
rows = max(1, min(rows, 4))
flap = max(20.0, min(flap, 90.0))
margin = max(12.0, min(margin, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 14.0))

per_row = max(1, -(-clip_count // rows))                  # ceil div
POUCH_W = per_row * (clip_width + 4.0) + 2.0 * margin
POUCH_H = rows * (clip_length + 6.0) + 2.0 * margin
# flap clamped shorter than the pouch height so the mouth never seals
FLAP = min(flap, POUCH_H * 0.4)
FLAP = max(15.0, FLAP)
DIVIDERS = max(1, per_row - 1)


def build_front():
    w, h = POUCH_W, POUCH_H
    internals = [
        fc.Internal(f"clip divider {i}",
                    [fc.P(margin + i * (clip_width + 4.0), margin),
                     fc.P(margin + i * (clip_width + 4.0), h - margin)], kind="marking")
        for i in range(1, per_row)
    ]
    for r in range(1, rows):
        ry = margin + r * (clip_length + 6.0)
        internals.append(fc.Internal(f"row line {r}",
                         [fc.P(margin, ry), fc.P(w - margin, ry)], kind="marking"))
    return fc.Piece(
        "front", [
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 14.0},
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 10.0), fc.P(w * 0.5, h - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Front (cut 1)",
    )


def build_back():
    w = POUCH_W
    h = POUCH_H + FLAP
    return fc.Piece(
        "back", [
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 10.0), fc.P(w * 0.5, h - 10.0)),
        internals=[fc.Internal("flap fold",
                               [fc.P(0.0, POUCH_H), fc.P(w, POUCH_H)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Back with flap (cut 1)",
    )


def build():
    pattern = fc.PatternSet("garment-clip-pouch")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())

    if everything:
        pattern.declare_seam(("front", "bottom"), ("back", "bottom"), tol=0.5)
        pattern.declare_seam(("front", "left"), ("back", "left"), tol=1.0,
                             ease=POUCH_H - (POUCH_H + FLAP))

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton canvas (pouch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a firm canvas so the clips "
                 f"do not poke through."},
        {"item": "garment clips", "qty": clip_count, "unit": "count",
         "note": f"Yantra4D garment-clip (notion.hardware_ref): the pouch is cut to a "
                 f"{per_row}-across x {rows}-row footprint of {clip_length:.0f} x "
                 f"{clip_width:.0f} mm clips."},
        {"item": "closure snap + thread", "qty": 1, "unit": "set",
         "note": "the flap closes with a snap or a hook-loop dot."},
    ]
    pattern.metadata = {
        "fc500_rank": 420, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A slim divided pouch for a set of garment clips, sized to the "
            "clip footprint with a fold-over flap.",
        "solved": {
            "per_row": per_row, "rows": rows,
            "pouch_mm": [round(POUCH_W, 1), round(POUCH_H, 1)],
            "flap_mm": round(FLAP, 1),
            "dividers": DIVIDERS,
            "note": "the pouch is cut to the clip footprint (clip size x count) plus a "
                    "margin, floored to hold at least a couple; the flap is clamped shorter "
                    "than the pouch height so the mouth never seals; the divider count is "
                    "derived from the per-row clip count.",
        },
        "hardware": "garment clips via Yantra4D (notion.hardware_ref -> garment-clip); "
                    "jaw_len and jaw_w are fed from the clip footprint. No flange interface "
                    "— the pouch holds the clips, no seam handshake owed.",
    }
    return pattern


result = build()
