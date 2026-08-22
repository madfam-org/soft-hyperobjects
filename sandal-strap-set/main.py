"""
Sandal Strap Set — Fashion Cabinet Garment Cartridge (FC-300 #230, lane 4 footwear).

The strap set of a flat sandal, drafted as three straps that mount to a footbed: an
`ankle_strap` that buckles round the ankle, a `toe_strap` that crosses the forefoot, and
a `heel_strap` that links them behind the heel. Every strap is one width — `strap_w` —
because a sandal that mixes strap widths cannot share hardware; that single width is the
handshake with the Yantra4D `belt-buckle`.

Pieces:
  - ankle_strap : buckling strap round the ankle (cut 1). Buckle end + tongue holes.
  - toe_strap   : forefoot cross strap (cut 1).
  - heel_strap  : heel link between ankle and footbed (cut 1).

SIZING NOTE (honest, checked): ISO 8559 as vendored in
packages/schemas/body-measurements.schema.json declares NO foot landmark codes, so
foot_length is a PLAIN parameter with no `measurement` block. `ankle_girth` IS canonical
and IS claimed — the ankle strap genuinely wraps that landmark.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # ankle_strap|toe_strap|heel_strap|set

# ankle_girth IS a canonical ISO-8559 landmark — the ankle strap wraps it.
ankle_girth = float(PARAM(lambda: ankle_girth, 245.0))
# Plain sized param — ISO 8559 has no foot codes.
foot_length = float(PARAM(lambda: foot_length, 255.0))

strap_w = float(PARAM(lambda: strap_w, 20.0))            # ONE width for every strap
overlap = float(PARAM(lambda: overlap, 85.0))            # tongue beyond the buckle
hole_count = int(PARAM(lambda: hole_count, 5))           # adjustment holes
hole_pitch = float(PARAM(lambda: hole_pitch, 15.0))
heel_rise = float(PARAM(lambda: heel_rise, 68.0))        # footbed to ankle strap
seam_allowance = float(PARAM(lambda: seam_allowance, 5.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
ankle_girth = max(160.0, min(ankle_girth, 340.0))
foot_length = max(150.0, min(foot_length, 330.0))
strap_w = max(8.0, min(strap_w, 50.0))
overlap = max(30.0, min(overlap, 180.0))
hole_count = max(2, min(hole_count, 9))
hole_pitch = max(8.0, min(hole_pitch, 30.0))
heel_rise = max(30.0, min(heel_rise, 150.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved lengths ───────────────────────────────────────────────────────────
# Ankle strap: the girth it wraps, plus the tongue that runs past the buckle.
ANKLE_RUN = ankle_girth + overlap
# Toe strap: across the forefoot, mount tab to mount tab.
TOE_RUN = foot_length * 0.62
# Heel strap: up the back of the heel from footbed to ankle strap, both mounts.
HEEL_RUN = heel_rise + 2.0 * strap_w


def _strap(name, length, width, label, holes=0, buckle=False):
    """A straight strap: `attach_a` and `attach_b` are the mount ends, `edge_top` and
    `edge_bottom` the long sides. Both long sides are exactly `width` apart, so every
    strap in the set shares one width — the belt-buckle handshake dimension."""
    internals = []
    notches = [fc.Notch("attach_a", 0.5, "mount centre"),
               fc.Notch("attach_b", 0.5, "mount centre")]
    if buckle:
        # Buckle sits at the far end; the bar seat is where the strap folds back.
        seat = length - overlap
        internals.append(fc.Internal("buckle-fold",
                                     [fc.P(seat, 0.0), fc.P(seat, width)], kind="fold"))
        notches.append(fc.Notch("edge_bottom", max(0.02, min(seat / length, 0.98)),
                                "buckle bar"))
    if holes:
        # Adjustment holes down the tongue, centred on the strap's own width.
        span = (holes - 1) * hole_pitch
        first = length - 12.0 - span
        for i in range(holes):
            cx = first + i * hole_pitch
            cy = width / 2.0
            r = min(3.0, width * 0.16)
            internals.append(fc.Internal(f"hole-{i + 1}",
                                         [fc.P(cx - r, cy), fc.P(cx + r, cy)],
                                         kind="drill"))
    return fc.Piece(
        name,
        [
            fc.Edge("edge_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("attach_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("edge_top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("attach_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=notches,
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0),
                               fc.P(length * 0.8, width / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build():
    pattern = fc.PatternSet("sandal-strap-set")
    everything = target_piece == "set"

    ankle = _strap("ankle_strap", ANKLE_RUN, strap_w, "Ankle strap (buckling)",
                   holes=hole_count, buckle=True)
    toe = _strap("toe_strap", TOE_RUN, strap_w, "Toe strap (forefoot cross)")
    heel = _strap("heel_strap", HEEL_RUN, strap_w, "Heel strap (link)")

    if everything or target_piece == "ankle_strap":
        pattern.add(ankle)
    if everything or target_piece == "toe_strap":
        pattern.add(toe)
    if everything or target_piece == "heel_strap":
        pattern.add(heel)

    # ── Declared seams ──────────────────────────────────────────────────────
    # The heel strap links the ankle strap to the footbed: its top mount end is sewn
    # to the ankle strap's rear mount end. Both are `strap_w` wide, so the seam
    # verifies at delta 0 by construction — the shared width IS the joint.
    if everything:
        pattern.declare_seam(("heel_strap", "attach_b"), ("ankle_strap", "attach_a"),
                             tol=0.5)
        # The toe strap's two mount ends sew to the heel strap's footbed end and to
        # the footbed itself; the declared pair is the strap-to-strap one.
        pattern.declare_seam(("toe_strap", "attach_a"), ("heel_strap", "attach_a"),
                             tol=0.5)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)      # straps nest well
    pattern.bom = [
        {"item": "veg-tan leather or webbing (straps)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 72% marker — straight straps nest tightly. "
                 "Per PAIR, double this."},
        {"item": "belt buckle", "qty": 1, "unit": "pcs",
         "note": "Yantra4D `belt-buckle` — printed or metal, sized to strap_w. One "
                 "per sandal."},
        {"item": "footbed / sole unit", "qty": 1, "unit": "pcs",
         "note": "the straps mount to it; cork, leather, or EVA. Out of this "
                 "cartridge's scope (a hard good, not a soft good)."},
        {"item": "rivets or box stitching", "qty": 6, "unit": "pcs",
         "note": "secure each strap mount end; rivets for leather, bar tacks for webbing."},
        {"item": "waxed thread", "qty": 1, "unit": "spool",
         "note": "saddle-stitch the buckle fold and the strap joins."},
    ]
    pattern.metadata = {
        "fc300_rank": 230, "family": "footwear_soft", "fabric_hint": "piel-vegetal",
        "silhouette_note": "Three straps to a footbed: a buckling ankle strap, a "
            "forefoot toe strap, and a heel link. Every strap shares ONE width so one "
            "buckle size serves the whole sandal.",
        "sizing_note": "ankle_girth IS a canonical ISO-8559 landmark and is claimed. "
            "foot_length is a PLAIN parameter — ISO 8559 as vendored declares no foot "
            "landmark codes, so none is invented.",
        "solved": {
            "strap_w_mm": round(strap_w, 1),
            "ankle_run_mm": round(ANKLE_RUN, 1),
            "toe_run_mm": round(TOE_RUN, 1),
            "heel_run_mm": round(HEEL_RUN, 1),
            "holes": hole_count,
        },
    }
    return pattern


result = build()
