"""
Invisible Zipper — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The zipper SOLID is Yantra4D territory (invisible-zipper; see the manifest's
notion.hardware_ref). What Fashion Cabinet owns is the installation — where the
stitch line runs relative to the coil, where the slider stops, where the crossing
seams must match — and the 2-D fabrication output: an INSTALLATION GUIDE strip
laid along the seam, carrying the stitch line, the tape width, and notches at the
top stop, any crossing seam, and the bottom stop.

An invisible zipper differs from a conventional one in exactly one way that
matters to the pattern: the coil rolls under, so the stitch line sits a coil
radius off the seam line rather than a topstitch width away from it. That offset
is what this guide encodes.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `zipper_length`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
zipper_length = float(PARAM(lambda: zipper_length, 560.0))
tape_width    = float(PARAM(lambda: tape_width, 24.0))
end_margin    = float(PARAM(lambda: end_margin, 30.0))    # guide run past each stop
coil_dia      = float(PARAM(lambda: coil_dia, 4.0))
cross_seam    = float(PARAM(lambda: cross_seam, 0.0))     # 0 = none; else mm from top

# ── Clamps ───────────────────────────────────────────────────────────────────
zipper_length = max(100.0, min(zipper_length, 900.0))
tape_width    = max(18.0, min(tape_width, 40.0))
end_margin    = max(10.0, min(end_margin, 80.0))
coil_dia      = max(3.0, min(coil_dia, 7.0))
cross_seam    = max(0.0, min(cross_seam, zipper_length))

# The invisible-zipper stitch line: half a coil off the folded seam line, so the
# coil rolls under and the stitching disappears.
stitch_offset = coil_dia / 2.0
run_length    = zipper_length + 2.0 * end_margin
# The tape lies flat inside the guide; the guide is one tape wide plus the seam
# allowance the tape is caught in.
strip_width   = tape_width + stitch_offset


def _notch_positions():
    """(fraction along the guide edge, label) for each installation landmark."""
    marks = [
        (end_margin + zipper_length, "top stop"),
        (end_margin, "bottom stop"),
    ]
    if cross_seam > 0.0:
        marks.append((end_margin + zipper_length - cross_seam, "cross seam"))
    return [(y / run_length, label) for y, label in marks]


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(strip_width, run_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge sits on the garment seam line — the fold the coil hides in.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = [
        # The stitch line: where the zipper foot rides, one coil radius in.
        fc.Internal(
            "stitch-line",
            [fc.P(stitch_offset, 0.0), fc.P(stitch_offset, run_length)],
            kind="marking",
        ),
        # The far edge of the tape — the tape must not extend past this.
        fc.Internal(
            "tape-edge",
            [fc.P(strip_width, 0.0), fc.P(strip_width, run_length)],
            kind="marking",
        ),
        # Stop bars: the slider travel limits, drawn across the tape.
        fc.Internal(
            "top-stop",
            [fc.P(0.0, end_margin + zipper_length), fc.P(strip_width, end_margin + zipper_length)],
            kind="drill",
        ),
        fc.Internal(
            "bottom-stop",
            [fc.P(0.0, end_margin), fc.P(strip_width, end_margin)],
            kind="drill",
        ),
    ]
    if cross_seam > 0.0:
        y = end_margin + zipper_length - cross_seam
        internals.append(
            fc.Internal("cross-seam", [fc.P(0.0, y), fc.P(strip_width, y)], kind="marking")
        )

    piece = fc.Piece(
        "installation-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=[fc.Notch("guide", frac, label) for frac, label in _notch_positions()],
        grainline=fc.Grainline(
            fc.P(strip_width * 0.8, run_length * 0.15),
            fc.P(strip_width * 0.8, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Invisible Zipper Installation Guide",
    )

    pattern = fc.PatternSet("invisible-zipper-notion")
    pattern.add(piece)
    pattern.metadata = {
        "zipper_length_mm": round(zipper_length, 1),
        "tape_width_mm": round(tape_width, 1),
        "stitch_offset_mm": round(stitch_offset, 2),
        "guide_run_mm": round(run_length, 1),
        "cross_seam_mm": round(cross_seam, 1) if cross_seam > 0.0 else None,
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> invisible-zipper)",
    }
    return pattern


result = build()
