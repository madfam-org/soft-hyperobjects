"""
Grip-pad palm mitt — Fashion Cabinet Garment Cartridge
(FC-500 rank #434, adaptive / soft-exo, Yantra4D-bridged soft-gripper-pad).

A fingerless palm mitt for a weak or painful grip: a neoprene palm band that leaves the fingers
free but backs the palm with a compliant ribbed gripper pad, so a rail, a walker handle or a
cup pressed into the palm does not slip. The mitt is the soft body; the ribbed pad is the
Yantra4D `soft-gripper-pad` solid, held in a palmar pocket, never modelled here.

Two real decisions:

  1. THE PAD POCKET IS SOLVED TO THE PAD FOOTPRINT — THE DIMENSIONAL HANDSHAKE. The palmar
     pocket is drafted `pad_length` x `pad_width`; those are the same numbers that drive the
     Yantra4D `soft-gripper-pad` `pad_len` / `pad_w`, so the printed pad drops into the pocket
     exactly. `pad_length` drives BOTH the hardware AND the garment's `pad_pocket` interface.

  2. A BAND, NOT A GLOVE — THE THUMB SLOT IS CLAMPED. The mitt is an open palm band with a thumb
     slot; the slot depth is clamped under the band height so it can never split the band.

Pieces: band (the palm wrap with the pad pocket + thumb slot) + closure-tab (the wrist overlap).
Made to measure to palm girth, palm width and hand breadth.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # band|tab|set

palm_girth = float(PARAM(lambda: palm_girth, 215.0))       # around the palm
band_height = float(PARAM(lambda: band_height, 95.0))      # up the palm (wrist to knuckles)
pad_length = float(PARAM(lambda: pad_length, 70.0))        # pad footprint length
pad_width = float(PARAM(lambda: pad_width, 45.0))          # pad footprint width
thumb_slot = float(PARAM(lambda: thumb_slot, 40.0))        # thumb slot depth
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
palm_girth = max(150.0, min(palm_girth, 290.0))
band_height = max(60.0, min(band_height, 150.0))
pad_length = max(40.0, min(pad_length, 110.0))
pad_width = max(25.0, min(pad_width, 90.0))
thumb_slot = max(20.0, min(thumb_slot, 70.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 12.0))
seam_allowance = max(2.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
BAND_LEN = palm_girth * NEG                 # the band wraps the palm ring
# The pad must fit inside the band: clamp its footprint under the band's usable interior.
pad_length = min(pad_length, band_height - 15.0)
pad_width = min(pad_width, BAND_LEN * 0.35)
# The thumb slot can never reach the full band height, or it splits the band.
thumb_slot = min(thumb_slot, band_height * 0.5)


def build_band():
    """The palm band (cut 1): a rectangle BAND_LEN x band_height with a thumb slot notched
    from the top edge near one end, and the pad pocket marked centrally."""
    ln, h = BAND_LEN, band_height
    # A closed band outline; the thumb slot is drawn as an internal marking (a cut line the
    # maker snips), not a hole in the outline, so the panel stays one closed ring.
    edges = [
        fc.Edge("wrist", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("knuckle", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    cx = ln * 0.5
    internals = [
        fc.Internal("pad_pocket",
                    [fc.P(cx - pad_width / 2.0, (h - pad_length) / 2.0),
                     fc.P(cx + pad_width / 2.0, (h - pad_length) / 2.0),
                     fc.P(cx + pad_width / 2.0, (h + pad_length) / 2.0),
                     fc.P(cx - pad_width / 2.0, (h + pad_length) / 2.0),
                     fc.P(cx - pad_width / 2.0, (h - pad_length) / 2.0)], kind="marking"),
        fc.Internal("thumb_slot",
                    [fc.P(ln * 0.86, h), fc.P(ln * 0.86, h - thumb_slot)], kind="marking"),
    ]
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("wrist", 0.5, "palm centre"), fc.Notch("knuckle", 0.5, "palm centre")],
        grainline=fc.Grainline(fc.P(cx, h * 0.15), fc.P(cx, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False),
        label="Palm band (pad pocket + thumb slot)")


def build_tab():
    """The closure tab (cut 1): the wrist overlap that closes the band with hook-and-loop."""
    ln = max(40.0, BAND_LEN * 0.22)
    h = band_height
    return fc.Piece(
        "tab", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(ln, h))]),
            fc.Edge("free", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "band end")],
        grainline=fc.Grainline(fc.P(ln * 0.5, h * 0.15), fc.P(ln * 0.5, h * 0.85)),
        internals=[fc.Internal("hook-loop", [fc.P(ln * 0.5, h * 0.2), fc.P(ln * 0.5, h * 0.8)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1), label="Closure tab (cut 1)")


def build():
    pattern = fc.PatternSet("grip-pad-palm-mitt")
    every = target_piece == "set"
    band = build_band()
    tab = build_tab()
    if not every:
        picked = {"band": band, "tab": tab}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (band, tab):
        pattern.add(piece)
    # The tab attaches to the band's end.
    pattern.declare_seam(("tab", "attach"), ("band", "end_a"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "neoprene (3 mm, four-way stretch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "the palm band + closure tab at negative ease so the band grips the palm."},
        {"item": "ribbed gripper pad (Yantra4D soft-gripper-pad)", "qty": 1, "unit": "piece",
         "note": f"one compliant ribbed pad, pad_len {pad_length:.0f} x pad_w {pad_width:.0f} "
                 "mm = the drafted pocket footprint; dropped in, never modelled here."},
        {"item": "hook-and-loop tape", "qty": round(band_height + 40.0), "unit": "mm_length",
         "note": "closes the band one-handed on the closure tab, no buckle to fumble."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock the pocket edges so the pad seats flat against the palm."},
    ]
    pattern.metadata = {
        "fc500_rank": 434, "family": "adaptive", "fabric_hint": "neopreno",
        "silhouette_note": "A fingerless palm mitt: a neoprene band that leaves the fingers free "
            "but backs the palm with a compliant ribbed gripper pad so a rail or cup does not "
            "slip.",
        "hardware": "ribbed gripper pad via Yantra4D (notion.hardware_ref -> soft-gripper-pad); "
            "pad_len/pad_w ARE the drafted pocket footprint, the same pad_length that drives the "
            "pad_pocket interface — the dimensional handshake.",
        "solver": {
            "band_len_mm": round(BAND_LEN, 1), "pad_len_mm": round(pad_length, 1),
            "pad_w_mm": round(pad_width, 1), "thumb_slot_mm": round(thumb_slot, 1),
            "note": "the pad footprint is clamped inside the band interior; the thumb slot depth "
                    "is clamped under half the band height so it can never split the band.",
        },
        "adaptive": {
            "assist": "a compliant gripper pad on the palm keeps a rail, walker handle or cup "
                      "from slipping for a weak or painful grip; fingers stay free.",
        },
    }
    return pattern


result = build()
