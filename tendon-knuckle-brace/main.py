"""
Tendon-knuckle wrist brace — Fashion Cabinet Garment Cartridge
(FC-500 rank #435, adaptive / soft-exo, Yantra4D-bridged tendon-knuckle).

A wrist-and-knuckle brace that lends a tendon back to a hand that has lost extension: a printed
TPU wrap spanning the forearm, wrist and back of the hand, carrying an articulated tendon-knuckle
linkage along its dorsal line so a pull at the forearm extends the knuckles. The brace is the
soft body drafted here; the articulated knuckle is the Yantra4D `tendon-knuckle` solid, never
modelled here.

Two real decisions:

  1. THE LINKAGE CHANNEL IS SOLVED TO THE SPAN — THE DIMENSIONAL HANDSHAKE. The dorsal channel
     runs the drafted `linkage_span` from the forearm anchor to the knuckle line; that is the
     same number that drives the count of `tendon-knuckle` segments (each `seg_len` long), so the
     printed linkage is exactly as long as the channel that holds it. `linkage_span` drives BOTH
     the hardware AND the garment's `linkage_channel` interface.

  2. A TWO-GIRTH TAPERED WRAP, CLAMPED. The forearm girth exceeds the wrist girth exceeds nothing;
     the wrist girth is clamped under the forearm girth so the tapered forearm-to-wrist wrap can
     never invert.

Pieces: forearm-wrap (tapered, tendon channel) + hand-wrap (the back-of-hand knuckle band) +
strap (the closure). Made to measure to forearm girth, wrist girth and brace length.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # forearm|hand|strap|set

forearm_girth = float(PARAM(lambda: forearm_girth, 260.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 175.0))
brace_length = float(PARAM(lambda: brace_length, 220.0))    # forearm anchor to knuckle line
hand_span = float(PARAM(lambda: hand_span, 95.0))           # wrist to knuckle line
linkage_span = float(PARAM(lambda: linkage_span, 150.0))    # dorsal linkage run
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
forearm_girth = max(180.0, min(forearm_girth, 380.0))
wrist_girth = max(130.0, min(wrist_girth, 240.0))
brace_length = max(140.0, min(brace_length, 320.0))
hand_span = max(60.0, min(hand_span, 150.0))
linkage_span = max(80.0, min(linkage_span, 280.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 10.0))
seam_allowance = max(2.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
FORE_FIN = forearm_girth * NEG
WRIST_FIN = wrist_girth * NEG
# wrist must be smaller than forearm, or the tapered wrap inverts.
WRIST_FIN = min(WRIST_FIN, FORE_FIN - 10.0)
FORE_LEN = brace_length - hand_span        # forearm-to-wrist section length
FORE_LEN = max(60.0, FORE_LEN)
# the linkage channel can never exceed the dorsal run (forearm section + hand section).
CHAN = min(linkage_span, (FORE_LEN + hand_span) * 0.96)


def build_forearm():
    """Tapered forearm-to-wrist wrap (cut 1): forearm edge (FORE_FIN) to wrist edge (WRIST_FIN),
    two closing seams, dorsal tendon channel."""
    h = FORE_LEN
    bw, tw = FORE_FIN, WRIST_FIN
    edges = [
        fc.Edge("forearm", [fc.Line(fc.P(0.0, 0.0), fc.P(bw, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(bw, 0.0), fc.P((bw + tw) / 2.0, h))]),
        fc.Edge("wrist", [fc.Line(fc.P((bw + tw) / 2.0, h), fc.P((bw - tw) / 2.0, h))]),
        fc.Edge("seam_l", [fc.Line(fc.P((bw - tw) / 2.0, h), fc.P(0.0, 0.0))]),
    ]
    cx = bw / 2.0
    internals = [fc.Internal("tendon_channel",
                             [fc.P(cx, h * 0.05), fc.P(cx, h * 0.95)], kind="marking")]
    return fc.Piece(
        "forearm", edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("forearm", 0.5, "dorsal centre"), fc.Notch("wrist", 0.5,
                "dorsal centre")],
        grainline=fc.Grainline(fc.P(cx, h * 0.15), fc.P(cx, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Forearm wrap (tendon channel)")


def build_hand():
    """Back-of-hand knuckle band (cut 1): wrist edge (WRIST_FIN) to knuckle edge, carries the
    dorsal channel continuing to the knuckle line."""
    h = hand_span
    ww = WRIST_FIN
    kw = WRIST_FIN * 1.06                    # knuckles a touch wider than the wrist
    edges = [
        fc.Edge("wrist", [fc.Line(fc.P((kw - ww) / 2.0, 0.0), fc.P((kw + ww) / 2.0, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P((kw + ww) / 2.0, 0.0), fc.P(kw, h))]),
        fc.Edge("knuckle", [fc.Line(fc.P(kw, h), fc.P(0.0, h))]),
        fc.Edge("seam_l", [fc.Line(fc.P(0.0, h), fc.P((kw - ww) / 2.0, 0.0))]),
    ]
    cx = kw / 2.0
    internals = [fc.Internal("tendon_channel",
                             [fc.P(cx, h * 0.05), fc.P(cx, h * 0.95)], kind="marking")]
    return fc.Piece(
        "hand", edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("wrist", 0.5, "dorsal centre"), fc.Notch("knuckle", 0.5,
                "dorsal centre")],
        grainline=fc.Grainline(fc.P(cx, h * 0.15), fc.P(cx, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Back-of-hand knuckle band")


def build_strap():
    """The closure strap (cut 2 mirrored) that cinches the wraps on hook-and-loop."""
    ln = max(60.0, FORE_FIN * 0.35)
    w = 35.0
    return fc.Piece(
        "strap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "wrap edge")],
        grainline=fc.Grainline(fc.P(ln * 0.5, w * 0.2), fc.P(ln * 0.5, w * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Closure strap (cut 2)")


def build():
    pattern = fc.PatternSet("tendon-knuckle-brace")
    every = target_piece == "set"
    fore = build_forearm()
    hand = build_hand()
    strap = build_strap()
    if not every:
        picked = {"forearm": fore, "hand": hand, "strap": strap}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (fore, hand, strap):
        pattern.add(piece)
    # forearm wrist edge sews to hand wrist edge (both == WRIST_FIN).
    pattern.declare_seam(("forearm", "wrist"), ("hand", "wrist"), tol=1.0)
    # each wrap closes on itself.
    pattern.declare_seam(("forearm", "seam_r"), ("forearm", "seam_l"), tol=1.0)
    pattern.declare_seam(("hand", "seam_r"), ("hand", "seam_l"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "printed TPU brace fabric (semi-rigid dorsal, soft palmar)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "forearm wrap + hand band + straps; the dorsal side backs the linkage channel."},
        {"item": "articulated tendon-knuckle linkage (Yantra4D tendon-knuckle)", "qty": 1,
         "unit": "piece",
         "note": f"the printed segmented knuckle linkage spanning {CHAN:.0f} mm of the drafted "
                 "dorsal channel; slid in, never modelled here."},
        {"item": "tendon cord + return spring", "qty": round(linkage_span * 3.0),
         "unit": "mm_length",
         "note": "a pull at the forearm extends the knuckles; the spring returns them."},
        {"item": "hook-and-loop tape", "qty": round(forearm_girth + wrist_girth),
         "unit": "mm_length",
         "note": "the straps cinch the wraps one-handed, no buckle to fumble."},
    ]
    pattern.metadata = {
        "fc500_rank": 435, "family": "adaptive", "fabric_hint": "tpu-panel-impreso",
        "silhouette_note": "A wrist-and-knuckle brace with a dorsal tendon-knuckle linkage: a "
            "pull at the forearm extends the knuckles for a hand that has lost extension.",
        "hardware": "articulated knuckle linkage via Yantra4D (notion.hardware_ref -> "
            "tendon-knuckle); linkage_span drives the linkage channel, the same parameter that "
            "drives the linkage_channel interface — the dimensional handshake.",
        "solver": {
            "fore_len_mm": round(FORE_LEN, 1), "channel_mm": round(CHAN, 1),
            "fore_fin_mm": round(FORE_FIN, 1), "wrist_fin_mm": round(WRIST_FIN, 1),
            "note": "wrist girth clamped under forearm girth so the tapered wrap can never "
                    "invert; the linkage channel clamped under the dorsal run.",
        },
        "adaptive": {
            "assist": "an articulated tendon linkage lends knuckle extension back to a hand that "
                      "has lost it — a wrist-drop or radial-nerve brace with real motion.",
        },
    }
    return pattern


result = build()
