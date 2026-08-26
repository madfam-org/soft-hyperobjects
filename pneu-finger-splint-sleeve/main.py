"""
Pneumatic finger-splint sleeve — Fashion Cabinet Garment Cartridge
(FC-500 rank #432, adaptive / soft-exo, Yantra4D-bridged pneu-net-finger).

A splint sleeve for a single finger that cannot extend or flex on its own: a printed TPU tube
that wraps the finger and holds a PneuNet bending actuator along its dorsal (or palmar) length.
Inflate the actuator and the finger extends; vent it and the finger flexes. The sleeve is the
soft body drafted here; the PneuNet finger is the Yantra4D `pneu-net-finger` solid, never
modelled here — the sleeve only carries it.

Two real decisions:

  1. THE ACTUATOR CHANNEL IS SOLVED TO THE FINGER LENGTH — THE DIMENSIONAL HANDSHAKE. The
     dorsal channel runs the drafted `finger_len` from the base knuckle to the tip; that is the
     same number that drives the Yantra4D `pneu-net-finger` `finger_len`, so the printed
     actuator is exactly as long as the channel that holds it. `finger_len` drives BOTH the
     hardware AND the garment's `actuator_channel` interface.

  2. A TAPERED WRAP, NOT A CLOSED TUBE. The finger tapers base to tip, so the sleeve is a flat
     tapered wrap (base girth to tip girth) that closes along one seam; the taper is clamped so
     the tip girth can never exceed the base girth (which would invert the wrap).

Pieces: sleeve (the tapered finger wrap with the actuator channel) + anchor-strap (the strap
that ties the sleeve to the back of the hand so the base does not slide).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # sleeve|anchor|set

finger_len = float(PARAM(lambda: finger_len, 90.0))        # base knuckle to tip
base_girth = float(PARAM(lambda: base_girth, 70.0))        # around the finger at the base
tip_girth = float(PARAM(lambda: tip_girth, 52.0))          # around the finger at the tip
anchor_width = float(PARAM(lambda: anchor_width, 180.0))   # strap wrapping the back of hand
channel_offset = float(PARAM(lambda: channel_offset, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 5.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
finger_len = max(50.0, min(finger_len, 130.0))
base_girth = max(45.0, min(base_girth, 100.0))
tip_girth = max(30.0, min(tip_girth, 90.0))
anchor_width = max(120.0, min(anchor_width, 280.0))
channel_offset = max(2.0, min(channel_offset, 15.0))
seam_allowance = max(2.0, min(seam_allowance, 10.0))

# The tip must be no wider than the base, or the tapered wrap inverts. Clamp it.
tip_girth = min(tip_girth, base_girth - 4.0)
BASE_W = base_girth                        # flat wrap width at the base (full girth wrap)
TIP_W = tip_girth                          # flat wrap width at the tip
CHAN_LEN = finger_len * 0.96               # the actuator channel length (a hair under the tube)


def build_sleeve():
    """The tapered finger wrap (cut 1): base edge (base girth) to tip edge (tip girth), two
    closing seams, dorsal actuator channel down the centre."""
    h = finger_len
    edges = [
        fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(BASE_W, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(BASE_W, 0.0), fc.P((BASE_W + TIP_W) / 2.0, h))]),
        fc.Edge("tip", [fc.Line(fc.P((BASE_W + TIP_W) / 2.0, h),
                                fc.P((BASE_W - TIP_W) / 2.0, h))]),
        fc.Edge("seam_l", [fc.Line(fc.P((BASE_W - TIP_W) / 2.0, h), fc.P(0.0, 0.0))]),
    ]
    cx = BASE_W / 2.0
    internals = [
        fc.Internal("actuator_channel",
                    [fc.P(cx, h * 0.02), fc.P(cx, h * 0.02 + CHAN_LEN)], kind="marking"),
        fc.Internal("channel_rail_l",
                    [fc.P(cx - channel_offset, h * 0.02),
                     fc.P(cx - channel_offset, h * 0.02 + CHAN_LEN)], kind="marking"),
        fc.Internal("channel_rail_r",
                    [fc.P(cx + channel_offset, h * 0.02),
                     fc.P(cx + channel_offset, h * 0.02 + CHAN_LEN)], kind="marking"),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        allowances={"tip": 0.0, "base": 0.0},
        notches=[fc.Notch("base", 0.5, "dorsal centre"),
                 fc.Notch("tip", 0.5, "dorsal centre")],
        grainline=fc.Grainline(fc.P(cx, h * 0.15), fc.P(cx, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Tapered finger wrap (actuator channel)")


def build_anchor():
    """The hand-anchor strap (cut 1, folded): wraps the back of the hand so the sleeve base
    does not slide off. `attach` sews to the sleeve base region; the free end closes on itself."""
    ln = anchor_width
    w = 40.0
    return fc.Piece(
        "anchor", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "sleeve base")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1), label="Hand-anchor strap (cut 1)")


def build():
    pattern = fc.PatternSet("pneu-finger-splint-sleeve")
    every = target_piece == "set"
    sleeve = build_sleeve()
    anchor = build_anchor()
    if not every:
        picked = {"sleeve": sleeve, "anchor": anchor}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (sleeve, anchor):
        pattern.add(piece)
    # The wrap closes on itself: seam_r sews to seam_l (both run base to tip, equal by taper).
    pattern.declare_seam(("sleeve", "seam_r"), ("sleeve", "seam_l"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 300.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.5)
    pattern.bom = [
        {"item": "printed TPU sleeve fabric (soft, airtight-backed)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "the tapered finger wrap + anchor strap; the dorsal side backs the actuator "
                 "channel."},
        {"item": "PneuNet bending actuator (Yantra4D pneu-net-finger)", "qty": 1, "unit": "piece",
         "note": f"one printed PneuNet finger, finger_len {finger_len:.0f} mm = the drafted "
                 "actuator channel; slid into the dorsal channel, never modelled here."},
        {"item": "silicone air tube + luer fitting", "qty": round(finger_len * 3.0),
         "unit": "mm_length",
         "note": "carries the pump line to the actuator; inflate to extend, vent to flex."},
        {"item": "hook-and-loop dots", "qty": 2, "unit": "piece",
         "note": "close the anchor strap and the wrap without a seam a swollen finger can't pass."},
    ]
    pattern.metadata = {
        "fc500_rank": 432, "family": "adaptive", "fabric_hint": "tpu-panel-impreso",
        "silhouette_note": "A single-finger pneumatic splint sleeve: a tapered TPU wrap holding "
            "a PneuNet bending actuator; inflate to extend the finger, vent to flex it.",
        "hardware": "PneuNet actuator via Yantra4D (notion.hardware_ref -> pneu-net-finger); "
            "finger_len IS the drafted actuator channel, the same finger_len that drives the "
            "actuator_channel interface — the dimensional handshake.",
        "solver": {
            "finger_len_mm": round(finger_len, 1),
            "channel_len_mm": round(CHAN_LEN, 1),
            "base_w_mm": round(BASE_W, 1), "tip_w_mm": round(TIP_W, 1),
            "note": "tip_girth clamped under base_girth-4 so the tapered wrap can never invert; "
                    "both closing seams run base to tip so they match by construction.",
        },
        "adaptive": {
            "assist": "a PneuNet actuator extends or flexes a single finger that cannot move "
                      "on its own; the sleeve carries the actuator and anchors to the hand.",
        },
    }
    return pattern


result = build()
