"""
Cord End — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The aglet or bell tip SOLID is Yantra4D territory (cord-end; see the manifest's
notion.hardware_ref). What Fashion Cabinet owns is the cord: how long it is cut
for a given channel run and the tie-off both ends need, where the tip is crimped
so the finished length is right, and how far the cord must be pulled through
before the tip goes on. The 2-D output is a CORD CUTTING GUIDE: a full-length
strip with the crimp zone marked at each tipped end, notches at the cut length
and at each crimp line, and the channel entry/exit marked.

Distinct from the cord LOCK (the spring stopper, already bridged by
`cord-stopper` and `drawcord-anchor`) — this is the tip that stops the cord
fraying and lets it be threaded at all.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `cord_dia`).
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
cord_dia    = float(PARAM(lambda: cord_dia, 5.0))
cord_length = float(PARAM(lambda: cord_length, 900.0))   # finished, tip to tip
tip_length  = float(PARAM(lambda: tip_length, 20.0))
ends        = int(  PARAM(lambda: ends, 2))              # 1 or 2 tipped ends
channel_run = float(PARAM(lambda: channel_run, 700.0))   # the casing the cord lives in

# ── Clamps ───────────────────────────────────────────────────────────────────
cord_dia    = max(2.0, min(cord_dia, 10.0))
cord_length = max(200.0, min(cord_length, 2000.0))
tip_length  = max(10.0, min(tip_length, 40.0))
ends        = 1 if ends < 2 else 2
channel_run = max(0.0, min(channel_run, cord_length))

# The cord must be cut longer than its finished length: each tip swallows its own
# length of cord in the crimp.
cut_length = cord_length + tip_length * ends
# The guide strip is a few cord diameters wide so the cord can be laid on it.
strip_width = max(12.0, cord_dia * 3.0)


def _crimp_spans():
    """(y_low, y_high) of each crimp zone along the cut length."""
    spans = [(0.0, tip_length)]
    if ends == 2:
        spans.append((cut_length - tip_length, cut_length))
    return spans


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, cut_length)
    top_right    = fc.P(strip_width, cut_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge is the cord's own lay line — measure the cord against it.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    cx = strip_width / 2.0
    internals = [
        # The cord itself, laid down the centre at its true diameter.
        fc.Internal("cord-left",
                    [fc.P(cx - cord_dia / 2.0, 0.0), fc.P(cx - cord_dia / 2.0, cut_length)],
                    kind="marking"),
        fc.Internal("cord-right",
                    [fc.P(cx + cord_dia / 2.0, 0.0), fc.P(cx + cord_dia / 2.0, cut_length)],
                    kind="marking"),
    ]

    notches = []
    for i, (y_lo, y_hi) in enumerate(_crimp_spans()):
        # The crimp zone: the length of cord the tip swallows.
        internals.append(fc.Internal(
            f"crimp-{i + 1}",
            [fc.P(cx - cord_dia, y_lo), fc.P(cx + cord_dia, y_lo),
             fc.P(cx + cord_dia, y_hi), fc.P(cx - cord_dia, y_hi),
             fc.P(cx - cord_dia, y_lo)],
            kind="marking"))
        crimp_line = y_hi if i == 0 else y_lo
        internals.append(fc.Internal(
            f"crimp-line-{i + 1}",
            [fc.P(0.0, crimp_line), fc.P(strip_width, crimp_line)], kind="drill"))
        notches.append(fc.Notch("guide", crimp_line / cut_length, f"tip {i + 1}"))

    # Where the cord enters and leaves the casing — what is left is the pull tail.
    if channel_run > 0.0:
        entry = (cut_length - channel_run) / 2.0
        for y, label in ((entry, "channel in"), (entry + channel_run, "channel out")):
            internals.append(fc.Internal(
                "channel-mark", [fc.P(0.0, y), fc.P(strip_width, y)], kind="marking"))
            notches.append(fc.Notch("guide", y / cut_length, label))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=notches,
        grainline=fc.Grainline(
            fc.P(strip_width * 0.85, cut_length * 0.15),
            fc.P(strip_width * 0.85, cut_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cord Cutting and Tip Guide",
    )

    pattern = fc.PatternSet("cord-end-notion")
    pattern.add(piece)
    pattern.metadata = {
        "cord_dia_mm": round(cord_dia, 1),
        "finished_length_mm": round(cord_length, 1),
        "cut_length_mm": round(cut_length, 1),
        "tip_length_mm": round(tip_length, 1),
        "tipped_ends": ends,
        "pull_tail_mm": round((cut_length - channel_run) / 2.0, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> cord-end)",
    }
    return pattern


result = build()
