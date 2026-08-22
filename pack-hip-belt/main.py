"""
Pack Hip Belt — Fashion Cabinet Garment Cartridge (FC-300 #238, technical & outdoor).

The load-bearing hip belt of a backpack: two padded wings that wrap the iliac crest and
transfer the pack's weight off the shoulders onto the pelvis, joined at the centre front
by a side-release buckle and pulled tight by webbing tails running through ladder-lock
adjusters. The wing is the whole engineering problem — it must be widest over the crest,
taper to the buckle so it does not fold at the belly, and curve on its upper edge to
follow the waist-to-hip rise.

The buckle and ladder-lock solids are Yantra4D territory (`strap-buckle`; see the
manifest's notion.hardware_ref). Fashion Cabinet owns the belt — the wing solved to
ISO 8559 waist and hip girths, the pad zones, the webbing channels.

Pieces:
  - wing     : the padded hip wing (cut 2, mirrored), pad and channel zones marked.
  - pad      : the foam/spacer-mesh pad insert for one wing (cut 2).
  - webbing  : the adjuster tail that runs through the ladder-lock (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))      # wing|pad|webbing|set

waist_girth  = float(PARAM(lambda: waist_girth, 820.0))     # ISO 8559 waist girth
hip_girth    = float(PARAM(lambda: hip_girth, 1000.0))      # ISO 8559 hip girth
wing_height  = float(PARAM(lambda: wing_height, 150.0))     # tallest point over the crest
buckle_gap   = float(PARAM(lambda: buckle_gap, 140.0))      # centre-front gap the buckle spans
tip_height   = float(PARAM(lambda: tip_height, 55.0))       # wing height at the buckle tip
pad_inset    = float(PARAM(lambda: pad_inset, 18.0))        # pad inset from the wing edge
webbing      = float(PARAM(lambda: webbing, 38.0))          # adjuster webbing width
tail_length  = float(PARAM(lambda: tail_length, 260.0))     # adjuster tail run
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(560.0, min(waist_girth, 1500.0))
hip_girth    = max(700.0, min(hip_girth, 1700.0))
wing_height  = max(90.0, min(wing_height, 240.0))
buckle_gap   = max(70.0, min(buckle_gap, 260.0))
tip_height   = max(35.0, min(tip_height, 120.0))
pad_inset    = max(8.0, min(pad_inset, 40.0))
webbing      = max(20.0, min(webbing, 60.0))
tail_length  = max(120.0, min(tail_length, 500.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The belt wraps between the waist and the hip — the load path sits on the crest, so
# the wing run is the mean of the two girths, less the centre-front buckle gap, halved
# for one wing.
BELT_RUN = (waist_girth + hip_girth) / 2.0
WING_RUN = max(120.0, (BELT_RUN - buckle_gap) / 2.0)
tip_height = min(tip_height, wing_height - 15.0)


def build_wing():
    """One padded hip wing.

    x = 0 is the pack-side (back) end where the wing joins the pack frame; x = WING_RUN
    is the buckle tip at the centre front. The upper edge curves down toward the tip to
    follow the waist-to-hip rise; the lower edge stays flat on the crest.
    """
    back_top  = fc.P(0.0, wing_height)
    tip_top   = fc.P(WING_RUN, tip_height)
    tip_bot   = fc.P(WING_RUN, 0.0)
    origin    = fc.P(0.0, 0.0)
    internals = [
        # The pad zone, inset all round so the seam never crushes the foam.
        fc.Internal("pad-zone",
                    [fc.P(pad_inset, pad_inset),
                     fc.P(WING_RUN - pad_inset, pad_inset),
                     fc.P(WING_RUN - pad_inset, tip_height - pad_inset),
                     fc.P(pad_inset, wing_height - pad_inset),
                     fc.P(pad_inset, pad_inset)], kind="marking"),
        # The webbing channel the adjuster tail runs in, centred on the load line.
        fc.Internal("webbing-channel",
                    [fc.P(WING_RUN * 0.15, tip_height * 0.5),
                     fc.P(WING_RUN, tip_height * 0.5)], kind="marking"),
        # Where the ladder-lock adjuster is bar-tacked to the wing.
        fc.Internal("ladder-lock-seat",
                    [fc.P(WING_RUN - webbing * 1.4, tip_height * 0.5 - webbing / 2.0),
                     fc.P(WING_RUN - webbing * 1.4, tip_height * 0.5 + webbing / 2.0)],
                    kind="drill"),
    ]
    return fc.Piece(
        "wing",
        [
            fc.Edge("pack_edge", [fc.Line(origin, back_top)]),
            fc.Edge("upper", [fc.curve_through(back_top, tip_top, bulge=0.10, side=1.0)]),
            fc.Edge("buckle_tip", [fc.Line(tip_top, tip_bot)]),
            fc.Edge("lower", [fc.Line(tip_bot, origin)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.0, "buckle tip"),
                 fc.Notch("lower", 1.0, "pack joint"),
                 fc.Notch("upper", 0.5, "crest apex")],
        grainline=fc.Grainline(fc.P(WING_RUN * 0.2, tip_height * 0.4),
                               fc.P(WING_RUN * 0.8, tip_height * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Padded hip wing",
    )


def build_pad():
    """The foam / spacer-mesh insert — the wing's pad zone, cut as its own piece."""
    w = WING_RUN - 2.0 * pad_inset
    h_back = wing_height - 2.0 * pad_inset
    h_tip = max(12.0, tip_height - 2.0 * pad_inset)
    return fc.Piece(
        "pad",
        [
            fc.Edge("back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h_back))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, h_back), fc.P(w, h_tip))]),
            fc.Edge("tip", [fc.Line(fc.P(w, h_tip), fc.P(w, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("lower", 0.5, "pad centre")],
        grainline=fc.Grainline(fc.P(w * 0.2, h_tip * 0.4), fc.P(w * 0.8, h_tip * 0.4)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wing pad insert",
    )


def build_webbing():
    """The adjuster tail: webbing that runs from the buckle through the ladder-lock."""
    return fc.Piece(
        "webbing",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(tail_length, 0.0))]),
            fc.Edge("buckle_end", [fc.Line(fc.P(tail_length, 0.0), fc.P(tail_length, webbing))]),
            fc.Edge("top", [fc.Line(fc.P(tail_length, webbing), fc.P(0.0, webbing))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, webbing), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", 0.5, "ladder-lock travel")],
        grainline=fc.Grainline(fc.P(tail_length * 0.15, webbing / 2.0),
                               fc.P(tail_length * 0.85, webbing / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Adjuster webbing tail",
    )


def build():
    pattern = fc.PatternSet("pack-hip-belt")
    everything = target_piece == "set"
    if everything or target_piece == "wing":
        pattern.add(build_wing())
    if everything or target_piece == "pad":
        pattern.add(build_pad())
    if everything or target_piece == "webbing":
        pattern.add(build_webbing())
    if everything:
        # The left wing meets the right wing at the buckle: tip to its own mirror.
        pattern.declare_seam(("wing", "buckle_tip"), ("wing", "buckle_tip"), tol=1.0)
        # The webbing tail's anchor end is caught in the wing's buckle tip seam.
        pattern.declare_seam(("webbing", "anchor_end"), ("webbing", "buckle_end"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "cordura face + spacer mesh backing",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 68% marker; mesh against the body, cordura outboard."},
        {"item": "closed-cell foam, 6–10 mm", "qty": 2, "unit": "pc",
         "note": "one pad per wing; density carries the load, thickness only cushions."},
        {"item": "side-release buckle (centre front)", "qty": 1, "unit": "set",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) sized to the webbing."},
        {"item": "ladder-lock adjusters", "qty": 2, "unit": "count",
         "note": "one per wing; the same Yantra4D webbing width drives both."},
        {"item": "bonded nylon thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "bar-tack every webbing anchor — this is the load path."},
    ]
    pattern.metadata = {
        "fc300_rank": 238, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "Two padded wings that wrap the iliac crest to transfer pack weight "
            "onto the pelvis: widest over the crest, tapering to a side-release buckle at the "
            "centre front, pulled tight by webbing tails through ladder-lock adjusters.",
        "solved": {"belt_run_mm": round(BELT_RUN, 1), "wing_run_mm": round(WING_RUN, 1),
                   "wing_height_mm": round(wing_height, 1), "tip_height_mm": round(tip_height, 1)},
        "hardware": "buckle + ladder-locks via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()
