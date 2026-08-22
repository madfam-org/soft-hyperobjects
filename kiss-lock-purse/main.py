"""
Kiss-Lock Purse — Fashion Cabinet Bag Cartridge (FC-300 rank #202, y4d kiss-lock frame).

A curved-top clutch whose MOUTH IS SEWN INTO the kiss-lock frame's channel. The frame is
edge-mated hardware — not a point fastener — so this cartridge's whole job is to hand the
frame a mouth run of exactly the right length. The frame solid is Yantra4D territory
(`kiss-lock-frame`; see the manifest's notion.hardware_ref); Fashion Cabinet owns the
purse bag, its arch, and the gusset.

The seam that must SOLVE. The frame is an arch of half-width `frame_width/2` rising
`frame_arch` — the run a purse mouth must follow to seat in the channel is that arch's
ARC LENGTH, not the frame's chord width. The purse's `mouth` edge is drafted as a Bezier
whose bulge is bisected until its measured length equals the measured frame arc within
0.05 mm, so the mouth cannot be eased or stretched into the channel: it fits.

Pieces:
  - front  : purse panel (cut 2 — front and back), mouth curve solved to the frame arc.
  - gusset : the side/base gusset strip that gives the clutch its depth.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|gusset|set

frame_width = float(PARAM(lambda: frame_width, 200.0))   # frame opening width (chord)
frame_arch = float(PARAM(lambda: frame_arch, 34.0))      # frame arch rise above the hinges
purse_depth = float(PARAM(lambda: purse_depth, 150.0))   # body depth below the hinges
gusset_width = float(PARAM(lambda: gusset_width, 46.0))  # side/base gusset width
channel_width = float(PARAM(lambda: channel_width, 6.0))  # frame sew-channel width
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
frame_width = max(90.0, min(frame_width, 320.0))
frame_arch = max(10.0, min(frame_arch, 80.0))
purse_depth = max(70.0, min(purse_depth, 260.0))
gusset_width = max(0.0, min(gusset_width, 120.0))
channel_width = max(3.0, min(channel_width, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

HALF = frame_width / 2.0
SEGS = 48


def _frame_arc_edge():
    """The frame's own arch, sampled as a polyline: a circular arc through the two hinge
    points (+/- HALF, 0) and the crown (0, frame_arch). This is the HARDWARE's run — the
    length the purse mouth must match to seat in the channel."""
    # Circle through (-HALF,0),(HALF,0),(0,arch): centre on the y axis at cy.
    cy = (frame_arch * frame_arch - HALF * HALF) / (2.0 * frame_arch)
    r = frame_arch - cy
    a_end = math.atan2(0.0 - cy, HALF)          # right hinge
    a_start = math.atan2(0.0 - cy, -HALF)       # left hinge
    pts = [fc.P(r * math.cos(a_start + (a_end - a_start) * i / SEGS),
                cy + r * math.sin(a_start + (a_end - a_start) * i / SEGS))
           for i in range(SEGS + 1)]
    return sum(pts[i].distance(pts[i + 1]) for i in range(SEGS))


FRAME_ARC = _frame_arc_edge()          # the measured channel run, one side of the frame


def _mouth(bulge):
    """The purse's mouth edge as a Bezier from the right hinge to the left hinge,
    bulging up by `bulge`. Length grows monotonically with bulge."""
    right = fc.P(HALF, purse_depth)
    left = fc.P(-HALF, purse_depth)
    return fc.Edge("mouth", [fc.curve_through(right, left, bulge=bulge, side=1.0)])


def _solve_mouth():
    """Bisect the mouth bulge until the mouth run equals the measured frame arc."""
    lo, hi = 0.0, 1.5
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if _mouth(mid).length(0.02) < FRAME_ARC:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    got = _mouth(bulge).length(0.02)
    if abs(got - FRAME_ARC) > 0.05:
        raise ValueError(
            f"kiss-lock mouth solver did not converge: {got:.3f} vs frame arc "
            f"{FRAME_ARC:.3f} mm"
        )
    return bulge


MOUTH_BULGE = _solve_mouth()
MOUTH_LEN = _mouth(MOUTH_BULGE).length(0.02)


def build_front():
    """One purse panel (cut 2). The mouth (top) is the solved curve that seats in the
    frame channel; the sides and base drop to a softly rounded bottom that takes the
    gusset. Drafted with x from -HALF..HALF, y from 0 (base) to purse_depth (hinges)."""
    right_hinge = fc.P(HALF, purse_depth)
    left_hinge = fc.P(-HALF, purse_depth)
    base_r = fc.P(HALF * 0.86, 0.0)
    base_l = fc.P(-HALF * 0.86, 0.0)
    edges = [
        # Right side: hinge down to the base corner, bowing slightly outward.
        fc.Edge("side_r", [fc.curve_through(right_hinge, base_r, bulge=0.08, side=1.0)]),
        # Base: the run the gusset's long edge sews to (with side_l it is the full seam).
        fc.Edge("base", [fc.curve_through(base_r, base_l, bulge=0.10, side=1.0)]),
        fc.Edge("side_l", [fc.curve_through(base_l, left_hinge, bulge=0.08, side=1.0)]),
        fc.Edge("mouth", [fc.curve_through(left_hinge, right_hinge,
                                           bulge=MOUTH_BULGE, side=-1.0)]),
    ]
    internals = [
        # The channel seat: how deep the mouth edge rides inside the frame channel.
        fc.Internal("frame-channel-seat",
                    [fc.P(-HALF * 0.7, purse_depth - channel_width),
                     fc.P(HALF * 0.7, purse_depth - channel_width)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"mouth": channel_width},
        notches=[fc.Notch("mouth", 0.5, "frame crown centre"),
                 fc.Notch("base", 0.5, "gusset centre")],
        grainline=fc.Grainline(fc.P(0.0, purse_depth * 0.2),
                               fc.P(0.0, purse_depth * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Purse Panel",
    )


def _panel_wrap_length():
    """The measured run of one panel's side + base + side — what the gusset must span."""
    piece = build_front()
    return sum(piece.edge(name).length(0.02) for name in ("side_r", "base", "side_l"))


def build_gusset():
    """The gusset strip: gusset_width wide, long enough to span one panel's
    side+base+side run. Its two long edges each sew to one panel."""
    ln = _panel_wrap_length()
    w = max(gusset_width, 1.0)
    return fc.Piece(
        "gusset",
        [
            fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("join_b", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join_a", 0.5, "base centre"),
                 fc.Notch("join_b", 0.5, "base centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Side/Base Gusset",
    )


def build():
    pattern = fc.PatternSet("kiss-lock-purse")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())

    if all_pieces:
        # Each gusset long edge takes one panel's side+base+side run.
        pattern.declare_seam(("gusset", "join_a"),
                             [("front", "side_r"), ("front", "base"), ("front", "side_l")],
                             tol=1.0)
        pattern.declare_seam(("gusset", "join_b"),
                             [("front", "side_r"), ("front", "base"), ("front", "side_l")],
                             tol=1.0)
    if all_pieces or target_piece == "front":
        # The mouth sews to its own mirror across the frame: front and back panels take
        # the two channel sides of the same frame, so the two mouth runs must be equal.
        pattern.declare_seam(("front", "mouth"), ("front", "mouth"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "silk dupioni, brocade or garment leather",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker; interline for the frame to hold its arch."},
        {"item": "kiss-lock frame", "qty": 1, "unit": "count",
         "note": f"Yantra4D kiss-lock-frame (see notion.hardware_ref): {frame_width:.0f} mm "
                 f"opening, {frame_arch:.0f} mm arch, {channel_width:.1f} mm channel. The "
                 f"mouth run is solved to {MOUTH_LEN:.2f} mm = the frame's own arc."},
        {"item": "fusible interlining", "qty": round(marker_len / 20.0) * 10,
         "unit": "mm_length", "note": "body the panels so the mouth holds the channel line."},
        {"item": "frame cord + fine thread", "qty": 1, "unit": "set",
         "note": "glue-and-cord the mouth into the channel, then whip-stitch through the "
                 "frame's stitch holes."},
    ]
    pattern.metadata = {
        "fc300_rank": 202,
        "family": "bags_luggage",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {"frame_width": round(frame_width, 1),
                        "frame_arch": round(frame_arch, 1),
                        "depth": round(purse_depth, 1),
                        "gusset": round(gusset_width, 1)},
        "solved": {
            "frame_arc_mm": round(FRAME_ARC, 3),
            "mouth_run_mm": round(MOUTH_LEN, 3),
            "mouth_bulge": round(MOUTH_BULGE, 5),
            "delta_mm": round(MOUTH_LEN - FRAME_ARC, 4),
            "note": "the mouth Bezier bulge is bisected until the mouth run equals the "
                    "frame's measured arc — the purse mouth SEATS in the channel rather "
                    "than being eased into it.",
        },
        "hardware": "kiss-lock frame via Yantra4D (notion.hardware_ref -> kiss-lock-frame); "
                    "EDGE-MATED: the purse mouth is sewn into the frame's sew_channel flange",
    }
    return pattern


result = build()
