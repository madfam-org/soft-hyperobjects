"""
Camera Strap — Fashion Cabinet Bag Cartridge (FC-300 rank #206, y4d tri-glide slider).

An adjustable webbing camera strap: two webbing TAILS that thread the camera lugs, a
length-adjusting tri-glide slider, and a shaped shoulder PAD with a padded core and a
webbing channel through it. The slider is a Yantra4D solid (`tri-glide-slider`; see the
manifest's notion.hardware_ref) whose webbing openings take this strap's `webbing_width`.

The seam that must SOLVE: the pad is a shaped lozenge — wide and gently curved at the
shoulder, tapering to the webbing width at each end — and the pad's channel-facing edges
are Beziers whose length has no closed form. The channel piece's length is therefore taken
FROM the measured pad edge, so the channel-to-pad seam verifies exactly.

Pieces:
  - tail    : the webbing tail that threads a camera lug and the slider (cut 2).
  - pad     : the shaped shoulder pad shell (cut 2 — face and lining).
  - channel : the webbing channel sewn along the pad's underside.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # tail|pad|channel|set

strap_length = float(PARAM(lambda: strap_length, 1250.0))  # full strap span, lug to lug
webbing_width = float(PARAM(lambda: webbing_width, 25.0))  # webbing / slider width
pad_length = float(PARAM(lambda: pad_length, 340.0))       # shoulder-pad length
pad_width = float(PARAM(lambda: pad_width, 62.0))          # pad width at the shoulder
lug_taper = float(PARAM(lambda: lug_taper, 12.0))          # narrowed width at the camera lug
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
strap_length = max(700.0, min(strap_length, 1700.0))
webbing_width = max(10.0, min(webbing_width, 40.0))
pad_length = max(160.0, min(pad_length, 520.0))
pad_width = max(30.0, min(pad_width, 110.0))
lug_taper = max(8.0, min(lug_taper, 25.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# The lug end can never be wider than the webbing it narrows into.
lug_taper = min(lug_taper, webbing_width)

# The two tails split the span not taken by the pad, plus the slider's doubling-back tail.
TAIL_LEN = max((strap_length - pad_length) / 2.0 + webbing_width * 6.0, webbing_width * 8.0)


def build_tail():
    """One webbing tail (cut 2): threads the camera lug at one end and the tri-glide
    slider at the other. Narrowed at the lug end so it passes a small camera lug."""
    ln, w = TAIL_LEN, webbing_width
    taper = lug_taper
    y0 = (w - taper) / 2.0
    return fc.Piece(
        "tail",
        [
            # Lug end (narrowed), then flaring out to the full webbing width.
            fc.Edge("lug_end", [fc.Line(fc.P(0.0, y0), fc.P(0.0, y0 + taper))]),
            fc.Edge("top", [
                fc.Line(fc.P(0.0, y0 + taper), fc.P(w * 2.0, w)),
                fc.Line(fc.P(w * 2.0, w), fc.P(ln, w)),
            ]),
            fc.Edge("slider_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [
                fc.Line(fc.P(ln, 0.0), fc.P(w * 2.0, 0.0)),
                fc.Line(fc.P(w * 2.0, 0.0), fc.P(0.0, y0)),
            ]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("top", 1.0, "slider end")],
        grainline=fc.Grainline(fc.P(ln * 0.3, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Webbing Tail",
    )


def _pad_edges():
    """The shoulder pad's lozenge outline: gently bowed long edges from a webbing-width
    end, out to pad_width at the middle, back to a webbing-width end."""
    ln, w = pad_length, pad_width
    e = webbing_width          # the pad ends at the webbing width
    y_lo = (w - e) / 2.0
    y_hi = y_lo + e
    return [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, y_lo), fc.P(0.0, y_hi))]),
        # The outer (shoulder-side) long edge, bowing out to the full pad width.
        fc.Edge("outer", [fc.curve_through(fc.P(0.0, y_hi), fc.P(ln, y_hi),
                                           bulge=0.13, side=1.0)]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, y_hi), fc.P(ln, y_lo))]),
        # The inner (body-side) long edge — the run the webbing channel follows.
        fc.Edge("inner", [fc.curve_through(fc.P(ln, y_lo), fc.P(0.0, y_lo),
                                           bulge=0.13, side=1.0)]),
    ]


def build_pad():
    """The shaped shoulder pad shell (cut 2 — face and lining, sewn face to face)."""
    ln, w = pad_length, pad_width
    internals = [
        # The padded core's outline, inset from the seam line.
        fc.Internal("core-line",
                    [fc.P(ln * 0.08, w * 0.5), fc.P(ln * 0.92, w * 0.5)], kind="marking"),
    ]
    return fc.Piece(
        "pad",
        _pad_edges(),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer", 0.5, "shoulder centre"),
                 fc.Notch("inner", 0.5, "shoulder centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shoulder Pad",
    )


def _pad_inner_run():
    """The measured run of the pad's inner edge — what the webbing channel must span."""
    return build_pad().edge("inner").length(0.02)


def build_channel():
    """The webbing channel sewn along the pad's inner edge: the webbing runs through it,
    so the pad slides to where the shoulder wants it. Its `join` edge is drafted to the
    MEASURED pad inner run."""
    ln = _pad_inner_run()
    w = webbing_width + 8.0        # clearance so the webbing slides, not binds
    return fc.Piece(
        "channel",
        [
            fc.Edge("join", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join", 0.5, "shoulder centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Webbing Channel",
    )


def build():
    pattern = fc.PatternSet("camera-strap")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "tail":
        pattern.add(build_tail())
    if all_pieces or target_piece == "pad":
        pattern.add(build_pad())
    if all_pieces or target_piece == "channel":
        pattern.add(build_channel())

    if all_pieces:
        # The channel is sewn along the pad's measured inner run.
        pattern.declare_seam(("channel", "join"), ("pad", "inner"), tol=1.0)
        # Both tails feed the same slider, so their slider ends match the webbing width.
        pattern.declare_seam(("tail", "slider_end"), ("pad", "end_a"), tol=0.5)
    if all_pieces or target_piece == "pad":
        # Face and lining are the same piece sewn face to face: outer meets outer.
        pattern.declare_seam(("pad", "outer"), ("pad", "outer"), tol=0.5)
    if all_pieces or target_piece == "tail":
        # The two tails are cut identically — the slider sees the same width from both.
        pattern.declare_seam(("tail", "slider_end"), ("tail", "slider_end"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "shell fabric (canvas, leather or ripstop)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 55% marker; small pieces, so scraps do."},
        {"item": "webbing", "qty": round(2.0 * TAIL_LEN + pad_length + 200.0),
         "unit": "mm_length",
         "note": f"{webbing_width:.0f} mm webbing: both tails, through the pad channel."},
        {"item": "tri-glide slider", "qty": 1, "unit": "count",
         "note": "Yantra4D tri-glide-slider (see notion.hardware_ref); its webbing "
                 f"openings take the same {webbing_width:.0f} mm webbing as the tails. "
                 "One slider is the whole adjustment mechanism."},
        {"item": "closed-cell foam or neoprene", "qty": 1, "unit": "count",
         "note": f"≈ {pad_length:.0f} x {pad_width:.0f} mm core for the shoulder pad."},
        {"item": "bonded nylon thread", "qty": 1, "unit": "spool",
         "note": "box-and-cross the lug ends; the whole camera hangs on those stitches."},
    ]
    pattern.metadata = {
        "fc300_rank": 206,
        "family": "bags_luggage",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"strap_length": round(strap_length, 1),
                        "webbing_width": round(webbing_width, 1),
                        "pad_length": round(pad_length, 1),
                        "pad_width": round(pad_width, 1)},
        "solved": {
            "pad_inner_run_mm": round(_pad_inner_run(), 2),
            "channel_span_mm": round(_pad_inner_run(), 2),
            "tail_length_mm": round(TAIL_LEN, 1),
            "note": "the channel length is taken from the MEASURED Bezier run of the "
                    "pad's inner edge, which has no closed form.",
        },
        "adjustment": "one tri-glide slider; the tails double back through it to shorten.",
        "hardware": "length adjustment via Yantra4D (notion.hardware_ref -> "
                    "tri-glide-slider); the slider openings and the tails share webbing_width",
    }
    return pattern


result = build()
