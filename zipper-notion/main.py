"""
Zipper — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

Like the shank button, the federation pattern: slider/pull SOLIDS belong to
the Yantra4D commons (manifest notion.hardware_ref, honestly unlinked until
a verified slug exists); Fashion Cabinet owns the fashion semantics — tape
geometry and installation math — and renders a printable INSTALLATION GUIDE
strip: stitch lines at the tape edges, top/bottom stop cross-marks, and
transfer notches on the seam edge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "guide"))

zipper_length = float(PARAM(lambda: zipper_length, 180.0))  # stop to stop
tape_width    = float(PARAM(lambda: tape_width, 32.0))      # full tape pair width
end_margin    = float(PARAM(lambda: end_margin, 25.0))
stitch_offset = float(PARAM(lambda: stitch_offset, 7.0))    # from center line

zipper_length = max(80.0, min(zipper_length, 900.0))
tape_width = max(20.0, min(tape_width, 60.0))
end_margin = max(10.0, min(end_margin, 60.0))
stitch_offset = max(3.0, min(stitch_offset, tape_width / 2.0 - 2.0))

L = zipper_length + 2.0 * end_margin
W = tape_width + 24.0
CX = W / 2.0
TOP_STOP_Y = L - end_margin
BOTTOM_STOP_Y = end_margin


def _cross(x, y, size=7.0):
    half = size / 2.0
    return [
        fc.Internal("stop-h", [fc.P(x - half, y), fc.P(x + half, y)], kind="drill"),
        fc.Internal("stop-v", [fc.P(x, y - half), fc.P(x, y + half)], kind="drill"),
    ]


def build():
    internals = [
        fc.Internal("center/seam line", [fc.P(CX, 0.0), fc.P(CX, L)], kind="marking"),
        fc.Internal("stitch line L",
                    [fc.P(CX - stitch_offset, BOTTOM_STOP_Y),
                     fc.P(CX - stitch_offset, TOP_STOP_Y)], kind="trace"),
        fc.Internal("stitch line R",
                    [fc.P(CX + stitch_offset, BOTTOM_STOP_Y),
                     fc.P(CX + stitch_offset, TOP_STOP_Y)], kind="trace"),
        fc.Internal("bottom bar-tack",
                    [fc.P(CX - stitch_offset, BOTTOM_STOP_Y),
                     fc.P(CX + stitch_offset, BOTTOM_STOP_Y)], kind="marking"),
    ]
    internals.extend(_cross(CX, TOP_STOP_Y))
    internals.extend(_cross(CX, BOTTOM_STOP_Y))
    piece = fc.Piece(
        "installation-guide",
        [
            fc.Edge("guide", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, L), fc.P(W, L))]),
            fc.Edge("outer", [fc.Line(fc.P(W, L), fc.P(W, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[
            fc.Notch("guide", TOP_STOP_Y / L, "top stop"),
            fc.Notch("guide", BOTTOM_STOP_Y / L, "bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.85, L * 0.15), fc.P(W * 0.85, L * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Zipper Installation Guide",
    )
    pattern = fc.PatternSet("zipper-notion")
    pattern.add(piece)
    pattern.metadata = {
        "enabler": True,
        "interface": "zipper_tape",
        "zipper_length_mm": zipper_length,
        "hardware": "slider/pull solids delegated to Yantra4D (manifest notion.hardware_ref)",
    }
    return pattern


result = build()
