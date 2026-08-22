"""
Hook-and-Loop Closure — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The tape SOLID — the hook field, the loop field, the base — is Yantra4D territory
(hook-loop-tape; see the manifest's notion.hardware_ref). What Fashion Cabinet owns
is the closure: how long the strip runs, how wide it is, how far in from its edge
the sewing line sits so the stitching never rides the hooks, and how a long run is
broken into segments so the closure peels progressively instead of all at once. The
2-D output is a TAPE PLACEMENT TEMPLATE: the strip footprint, a perimeter topstitch
line inset by the sew margin, per-segment gaps, and notches at each segment end.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `strip_length`).
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
strip_length = float(PARAM(lambda: strip_length, 200.0))
strip_width  = float(PARAM(lambda: strip_width, 25.0))
sew_margin   = float(PARAM(lambda: sew_margin, 3.0))
segments     = int(  PARAM(lambda: segments, 1))
segment_gap  = float(PARAM(lambda: segment_gap, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
strip_length = max(40.0, min(strip_length, 900.0))
strip_width  = max(12.0, min(strip_width, 60.0))
sew_margin   = max(2.0, min(sew_margin, 8.0))
segments     = max(1, min(segments, 12))
segment_gap  = max(0.0, min(segment_gap, 40.0))
# The margin can never eat the strip.
sew_margin   = min(sew_margin, strip_width / 2.0 - 1.0)

# Total run = the segments plus the gaps between them.
run_length = strip_length * segments + segment_gap * (segments - 1)


def _segment_spans():
    """(y_low, y_high) for each tape segment along the run."""
    spans = []
    y = 0.0
    for _ in range(segments):
        spans.append((y, y + strip_length))
        y += strip_length + segment_gap
    return spans


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(strip_width, run_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge sits on the garment placement line the tape aligns to.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    internals = []
    notches = []
    for i, (y_lo, y_hi) in enumerate(_segment_spans()):
        # Segment footprint: the tape outline itself.
        internals.append(fc.Internal(
            "tape-footprint",
            [fc.P(0.0, y_lo), fc.P(strip_width, y_lo),
             fc.P(strip_width, y_hi), fc.P(0.0, y_hi), fc.P(0.0, y_lo)],
            kind="marking"))
        # The sewing line, inset by the margin on all four sides — stitching here
        # never rides the hook field.
        m = sew_margin
        internals.append(fc.Internal(
            "sew-line",
            [fc.P(m, y_lo + m), fc.P(strip_width - m, y_lo + m),
             fc.P(strip_width - m, y_hi - m), fc.P(m, y_hi - m), fc.P(m, y_lo + m)],
            kind="marking"))
        notches.append(fc.Notch("guide", y_lo / run_length, f"seg {i + 1} start"))
        notches.append(fc.Notch("guide", y_hi / run_length, f"seg {i + 1} end"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=notches,
        grainline=fc.Grainline(
            fc.P(strip_width * 0.5, run_length * 0.15),
            fc.P(strip_width * 0.5, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Hook-and-Loop Tape Placement Template",
    )

    pattern = fc.PatternSet("hook-loop-closure")
    pattern.add(piece)
    pattern.metadata = {
        "strip_length_mm": round(strip_length, 1),
        "strip_width_mm": round(strip_width, 1),
        "sew_margin_mm": round(sew_margin, 2),
        "segments": segments,
        "total_tape_mm": round(strip_length * segments, 1),
        "run_length_mm": round(run_length, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> hook-loop-tape)",
    }
    return pattern


result = build()
