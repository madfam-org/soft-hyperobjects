"""
Bustle Pad — Fashion Cabinet Costume Cartridge (FC-300 rank #274, y4d hook bridged).

The small stuffed bustle of the later 19th century — the soft pad, as against the caged
or wired bustle of the same decades. Tied at the waist under the skirt, it holds the
fullness out at the back and nowhere else. The soft pad is the version most people
actually wore and the version most useful today: it is quiet, it packs flat, it does not
collapse when you sit on it, and it is the right understructure for the smaller bustle
silhouettes of c. 1870–1875 and again c. 1883–1889 at the modest end.

The documented construction this draft reproduces:

  - a CRESCENT pad — wider and deeper at the centre back, tapering to nothing at the
    sides, so the fullness is held out behind and the hips stay flat. A pad of even depth
    all round is a cushion, not a bustle;
  - two crescent faces joined by a DEPTH GUSSET around the curved outer edge, which is
    what turns two flat crescents into a bag with volume;
  - horizontal stitched CHANNELS dividing the bag into compartments, so the stuffing
    cannot migrate to the bottom and leave the top empty — this is the difference between
    a bustle that keeps its shape and a sagging bag of wool;
  - a waist TAPE with a hook closure, long enough to tie or hook at the front.

Drafting note — the seam that must SOLVE. The gusset is what gives the pad its depth, so
its length must equal the crescent's curved OUTER edge exactly, or the bag will not close.
That run is not a formula: the crescent's outer edge is drafted as a polyline through the
curve, its length is MEASURED off the built piece, and the gusset is then cut to precisely
that measured length.

A second measured quantity matters just as much and is usually skipped: the crescent's
INNER edge (against the body) is SHORTER than its outer edge, because a crescent's two
curves have different radii. That difference is the pad's whole shape, and both runs are
measured and reported so the maker knows what they are easing.

Pieces:
  - crescent  : one face of the pad (cut 2 — front and back face).
  - gusset    : the depth strip around the curved outer edge (cut 1).
  - waist_tape: the tape that carries the pad and hooks at the front (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # crescent|gusset|waist_tape|set

waist_girth = float(PARAM(lambda: waist_girth, 700.0))
pad_span = float(PARAM(lambda: pad_span, 420.0))       # side to side across the back
pad_drop = float(PARAM(lambda: pad_drop, 260.0))       # waist down to the pad's lowest point
pad_depth = float(PARAM(lambda: pad_depth, 110.0))     # how far it stands out at CB
channel_count = float(PARAM(lambda: channel_count, 3))  # stuffing compartments
hook_pitch = float(PARAM(lambda: hook_pitch, 45.0))    # waist-tape hook spacing
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (sane soft-bustle ranges) ─────────────────────────────────────────
waist_girth = max(500.0, min(waist_girth, 1300.0))
pad_span = max(220.0, min(pad_span, 620.0))
pad_drop = max(120.0, min(pad_drop, 420.0))
pad_depth = max(40.0, min(pad_depth, 220.0))
channel_count = int(max(1, min(channel_count, 6)))
hook_pitch = max(25.0, min(hook_pitch, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# A pad that stands out further than it is deep top-to-bottom is a shelf, not a bustle.
pad_depth = min(pad_depth, pad_drop * 0.85)

HALF = pad_span / 2.0
CURVE_STEPS = 32   # polyline resolution of both crescent curves


def _inner_points():
    """The crescent's INNER edge — the one that lies against the body at the waist.

    A shallow arc: the waist is a curve, not a straight line, and a pad cut with a
    straight top edge stands away from the body at the sides.
    """
    pts = []
    sag = pad_drop * 0.10   # how much the waist edge dips at the centre back
    for i in range(CURVE_STEPS + 1):
        t = i / CURVE_STEPS
        x = -HALF + pad_span * t
        # a gentle arc, deepest at the centre
        y = pad_drop - sag * (1.0 - ((x / HALF) ** 2 if HALF > 0 else 0.0))
        pts.append(fc.P(x, y))
    return pts


def _outer_points():
    """The crescent's OUTER edge — the curved lower edge that takes the gusset.

    Deepest at the centre back and tapering to meet the inner edge at each side, which is
    what makes the shape a crescent rather than a cushion. The taper is what keeps the
    hips flat.
    """
    pts = []
    for i in range(CURVE_STEPS + 1):
        t = i / CURVE_STEPS
        x = HALF - pad_span * t
        # Cosine taper: `frac` is 1 at the centre back (x = 0) and 0 at each tip
        # (x = ±HALF), which is exactly the crescent profile — deepest behind, vanishing
        # at the sides so the hips stay flat.
        frac = 0.5 * (1.0 + math.cos(math.pi * (x / HALF))) if HALF > 0 else 0.0
        y = pad_drop - (pad_drop * 0.10) - pad_drop * 0.90 * frac
        pts.append(fc.P(x, y))
    return pts


INNER_PTS = _inner_points()
OUTER_PTS = _outer_points()


def build_crescent():
    """One face of the pad (cut 2: the body side and the outer side).

    `inner` lies against the body and takes the waist tape; `outer` is the curved edge
    that takes the depth gusset. The stuffing channels are marked across the face.
    """
    inner_segs = [fc.Line(INNER_PTS[i], INNER_PTS[i + 1]) for i in range(len(INNER_PTS) - 1)]
    outer_segs = [fc.Line(OUTER_PTS[i], OUTER_PTS[i + 1]) for i in range(len(OUTER_PTS) - 1)]
    internals = []
    # Horizontal stuffing channels. Each is a different length as the crescent tapers —
    # the compartments near the bottom are much shorter than those near the waist, and
    # reporting that is more useful than pretending they are the same.
    channel_lengths = []
    for i in range(channel_count):
        t = (i + 1) / (channel_count + 1)
        # the y of this channel, between the inner and outer edges at the centre
        y_in = INNER_PTS[len(INNER_PTS) // 2].y
        y_out = OUTER_PTS[len(OUTER_PTS) // 2].y
        y = y_in - (y_in - y_out) * t
        # how far the crescent still reaches sideways at this height
        span_here = HALF * (1.0 - t) ** 0.45
        channel_lengths.append(span_here * 2.0)
        internals.append(fc.Internal("stuffing-channel",
                                     [fc.P(-span_here, y), fc.P(span_here, y)],
                                     kind="marking"))
    piece = fc.Piece(
        "crescent",
        [
            fc.Edge("inner", inner_segs),
            fc.Edge("tip_r", [fc.Line(INNER_PTS[-1], OUTER_PTS[0])]),
            fc.Edge("outer", outer_segs),
            fc.Edge("tip_l", [fc.Line(OUTER_PTS[-1], INNER_PTS[0])]),
        ],
        seam_allowance=seam_allowance,
        allowances={"inner": 16.0},   # the body edge takes extra: it turns onto the tape
        notches=[fc.Notch("outer", 0.5, "centre back"),
                 fc.Notch("outer", 0.25, "gusset quarter"),
                 fc.Notch("outer", 0.75, "gusset quarter"),
                 fc.Notch("inner", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, pad_drop * 0.15), fc.P(0.0, pad_drop * 0.80)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Crescent face (cut 2)",
    )
    piece._channel_lengths = channel_lengths
    return piece


CRESCENT = build_crescent()
# The MEASURED runs. The gusset is cut to the outer one; the difference between the two
# is the crescent's shape, and it is what the maker eases at the tips.
OUTER_RUN = CRESCENT.edge("outer").length()
INNER_RUN = CRESCENT.edge("inner").length()
CRESCENT_DIFFERENCE = OUTER_RUN - INNER_RUN


def build_gusset():
    """The depth strip sewn around the curved outer edge, giving the pad its volume.

    Cut to exactly the MEASURED outer run of the crescent, `pad_depth` wide. One strip
    joins both crescent faces into a bag.
    """
    ln, d = OUTER_RUN, pad_depth
    internals = []
    # Where each stuffing channel crosses the gusset, so the compartments are continuous
    # right round the bag rather than stopping at the seam.
    for i in range(channel_count):
        t = (i + 1) / (channel_count + 1)
        x = ln * t
        internals.append(fc.Internal("channel-crossing", [fc.P(x, 0.0), fc.P(x, d)],
                                     kind="marking"))
    internals.append(fc.Internal("stuffing-opening",
                                 [fc.P(ln * 0.5 - 45.0, d * 0.5),
                                  fc.P(ln * 0.5 + 45.0, d * 0.5)], kind="trace"))
    return fc.Piece(
        "gusset",
        [
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, d))]),
            fc.Edge("seam_b", [fc.Line(fc.P(ln, d), fc.P(0.0, d))]),
            fc.Edge("end_l", [fc.Line(fc.P(0.0, d), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("seam_a", 0.5, "centre back"),
                 fc.Notch("seam_a", 0.25, "gusset quarter"),
                 fc.Notch("seam_a", 0.75, "gusset quarter"),
                 fc.Notch("seam_b", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.15, d * 0.5), fc.P(ln * 0.85, d * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Depth gusset (cut 1, to the MEASURED outer run)",
    )


# Hooks along the waist tape.
N_HOOKS = max(2, int((waist_girth * 0.22) / hook_pitch))


def build_waist_tape():
    """The tape that carries the pad and hooks at the front."""
    ln = waist_girth + 220.0    # enough to hook at the front with adjustment
    w = 30.0
    internals = [fc.Internal("pad-attachment",
                             [fc.P(ln * 0.5 - INNER_RUN * 0.5, w * 0.5),
                              fc.P(ln * 0.5 + INNER_RUN * 0.5, w * 0.5)], kind="marking")]
    for i in range(N_HOOKS):
        x = 20.0 + i * hook_pitch
        internals.append(fc.Internal("tape-hook", [fc.P(x, w * 0.5), fc.P(x + 1.0, w * 0.5)],
                                     kind="drill"))
    return fc.Piece(
        "waist_tape",
        [
            fc.Edge("end_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=8.0,
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waist tape (cut 1, hooks at the front)",
    )


def build():
    pattern = fc.PatternSet("bustle-pad")
    everything = target_piece == "set"
    if everything or target_piece == "crescent":
        pattern.add(CRESCENT)
    if everything or target_piece == "gusset":
        pattern.add(build_gusset())
    if everything or target_piece == "waist_tape":
        pattern.add(build_waist_tape())

    if everything:
        # The bag seam: the gusset's two long edges each take one crescent's outer edge.
        # The gusset was cut to the MEASURED run, so both balance exactly.
        pattern.declare_seam(("gusset", "seam_a"), ("crescent", "outer"), tol=1.0)
        pattern.declare_seam(("gusset", "seam_b"), ("crescent", "outer"), tol=1.0)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton twill or ticking",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 70% marker. A firm, closely woven cloth — a loose weave "
                 "lets the stuffing beard through and the pad sheds inside the skirt."},
        {"item": "stuffing (wool, horsehair, or cotton wadding)",
         "qty": round(OUTER_RUN * pad_depth * 0.55 / 1000.0), "unit": "count",
         "note": "≈ in units of 1000 mm² of loft. Stuff each compartment SEPARATELY and "
                 "firmly; a soft pad flattens under the skirt's weight within an hour."},
        {"item": "waist-tape hooks (Yantra4D trouser-hook-bar)", "qty": N_HOOKS, "unit": "count",
         "note": f"{N_HOOKS} at {hook_pitch:.0f} mm pitch, giving the tape real adjustment — "
                 f"the pad is worn over stays, so the waist it fastens at varies."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "the channel stitching is structural, not decorative: it is what stops the "
                 "stuffing migrating to the bottom of the bag."},
    ]
    pattern.metadata = {
        "fc300_rank": 274,
        "family": "costume_historical",
        "period": "c. 1870–1875 and c. 1883–1889 (soft bustle)",
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A CRESCENT, not a cushion. The pad is deepest at the centre back "
            "and tapers to nothing at the sides, so the fullness is held out behind and the "
            "hips stay flat. Even depth all round gives a lumpy, hip-widening shape that no "
            "skirt above it can correct.",
        "construction_note": "Two crescent faces joined by a depth gusset around the curved "
            "outer edge; horizontal stitched channels divide the bag into compartments so the "
            "stuffing cannot migrate; a waist tape with hooks carries it.",
        "hardware": "waist-tape hooks via Yantra4D (notion.hardware_ref -> trouser-hook-bar); "
            "the hook pitch drives plate_len — the dimensional handshake.",
        "solved": {
            "outer_run_measured_mm": round(OUTER_RUN, 2),
            "inner_run_measured_mm": round(INNER_RUN, 2),
            "gusset_cut_length_mm": round(OUTER_RUN, 2),
            "crescent_difference_mm": round(CRESCENT_DIFFERENCE, 2),
            "channel_lengths_mm": [round(c, 1) for c in CRESCENT._channel_lengths],
            "pad_depth_mm": round(pad_depth, 1),
            "note": "the gusset is cut to the MEASURED length of the crescent's curved outer "
                    "polyline, so the bag closes exactly. The inner edge is deliberately "
                    "SHORTER than the outer — that difference is the crescent's whole shape — "
                    "and both runs are measured and reported so the maker knows what they are "
                    "easing at the tips. Channel lengths are reported individually because "
                    "every compartment in a crescent is a different length.",
        },
    }
    return pattern


result = build()
