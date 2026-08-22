"""
Boning Channel — Fashion Cabinet Notion Cartridge (Yantra4D-bridged hard good).

The stay itself — the spiral or flat bone, and its channel profile — is Yantra4D
territory (boning-stay; see the manifest's notion.hardware_ref). What Fashion
Cabinet owns is the channel: how wide the twin stitch lines must be for a given
stay, how long the channel runs, and where the stay's ends stop short of the seam
so the bone never rides into a seam allowance. The 2-D output is a CHANNEL
STITCHING TEMPLATE — twin parallel stitch lines at the channel width, squared off
at the stay length, repeated across the number of channels, with notches marking
each stay end on the guide edge.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `stay_length`).
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
stay_length   = float(PARAM(lambda: stay_length, 300.0))
stay_width    = float(PARAM(lambda: stay_width, 7.0))
channel_clear = float(PARAM(lambda: channel_clear, 0.5))   # ease inside the channel
stay_count    = int(  PARAM(lambda: stay_count, 8))
channel_pitch = float(PARAM(lambda: channel_pitch, 60.0))  # centre-to-centre
end_clear     = float(PARAM(lambda: end_clear, 6.0))       # stay end short of seam

# ── Clamps ───────────────────────────────────────────────────────────────────
stay_length   = max(80.0, min(stay_length, 500.0))
stay_width    = max(4.0, min(stay_width, 14.0))
channel_clear = max(0.2, min(channel_clear, 1.5))
stay_count    = max(1, min(stay_count, 24))
channel_pitch = max(20.0, min(channel_pitch, 200.0))
end_clear     = max(2.0, min(end_clear, 20.0))

# The finished channel is the stay plus its running clearance.
channel_width = stay_width + 2.0 * channel_clear
# The template runs the stay length plus the dead space at each end.
run_length    = stay_length + 2.0 * end_clear
strip_width   = channel_pitch * stay_count


def _channel_centres():
    return [channel_pitch * (i + 0.5) for i in range(stay_count)]


def build():
    origin       = fc.P(0.0, 0.0)
    top_left     = fc.P(0.0, run_length)
    top_right    = fc.P(strip_width, run_length)
    bottom_right = fc.P(strip_width, 0.0)

    edges = [
        # The guide edge sits on the garment's boned-panel seam line.
        fc.Edge("guide",  [fc.Line(origin, top_left)]),
        fc.Edge("top",    [fc.Line(top_left, top_right)]),
        fc.Edge("outer",  [fc.Line(top_right, bottom_right)]),
        fc.Edge("bottom", [fc.Line(bottom_right, origin)]),
    ]

    y_lo = end_clear
    y_hi = end_clear + stay_length
    half = channel_width / 2.0

    internals = []
    for cx in _channel_centres():
        # Twin stitch lines — the channel walls the stay slides between.
        internals.append(fc.Internal(
            "channel-stitch-left",
            [fc.P(cx - half, y_lo), fc.P(cx - half, y_hi)], kind="marking"))
        internals.append(fc.Internal(
            "channel-stitch-right",
            [fc.P(cx + half, y_lo), fc.P(cx + half, y_hi)], kind="marking"))
        # Bar tacks square the channel off at each stay end.
        internals.append(fc.Internal(
            "stay-end-low",
            [fc.P(cx - half, y_lo), fc.P(cx + half, y_lo)], kind="drill"))
        internals.append(fc.Internal(
            "stay-end-high",
            [fc.P(cx - half, y_hi), fc.P(cx + half, y_hi)], kind="drill"))

    piece = fc.Piece(
        "placement-guide",
        edges,
        seam_allowance=0.0,  # a template, not a sewn piece — cut line == outline
        notches=[
            fc.Notch("guide", y_lo / run_length, "stay end"),
            fc.Notch("guide", y_hi / run_length, "stay end"),
        ],
        grainline=fc.Grainline(
            fc.P(strip_width * 0.5, run_length * 0.15),
            fc.P(strip_width * 0.5, run_length * 0.85),
        ),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Boning Channel Stitching Template",
    )

    pattern = fc.PatternSet("boning-channel")
    pattern.add(piece)
    pattern.metadata = {
        "stay_length_mm": round(stay_length, 1),
        "stay_width_mm": round(stay_width, 2),
        "channel_width_mm": round(channel_width, 2),
        "stay_count": stay_count,
        "total_boning_mm": round(stay_length * stay_count, 1),
        "hardware": "solid geometry delegated to Yantra4D "
                    "(see manifest notion.hardware_ref -> boning-stay)",
    }
    return pattern


result = build()
