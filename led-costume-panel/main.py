"""
LED Costume Panel — Fashion Cabinet Accessory Cartridge (FC-200 rank #148, y4d led-channel).

A flat costume/cosplay panel prepared for LED strips: a rectangular (or shaped) panel
overlaid with LED-CHANNEL ROUTES (marked lanes an LED strip and its Yantra4D `led-channel`
diffuser follow) and a driver pocket. Sew it onto a garment or wear it as a standalone
panel. Fashion Cabinet owns the panel + the channel layout; Yantra4D owns the printable
channel.

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
panel_w    = float(PARAM(lambda: panel_w, 300.0))     # panel width
panel_h    = float(PARAM(lambda: panel_h, 400.0))     # panel height
strip_w    = float(PARAM(lambda: strip_w, 12.0))      # LED-strip width (sets the channel)
channels   = int(  PARAM(lambda: channels, 4))        # LED channel lanes
corner_r   = float(PARAM(lambda: corner_r, 30.0))     # marked rounded-corner radius
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
panel_w  = max(80.0, min(panel_w, 700.0))
panel_h  = max(80.0, min(panel_h, 900.0))
strip_w  = max(5.0, min(strip_w, 30.0))
channels = max(1, min(channels, 12))
corner_r = max(0.0, min(corner_r, min(panel_w, panel_h) * 0.3))


def build_panel():
    W, H = panel_w, panel_h
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, H), fc.P(W, H))]),
        fc.Edge("right", [fc.Line(fc.P(W, H), fc.P(W, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # Vertical LED channel lanes.
    for i in range(channels):
        x = W * (i + 0.5) / channels
        internals.append(fc.Internal(f"led-channel-{i}",
                                     [fc.P(x, H * 0.08), fc.P(x, H * 0.92)], kind="trace"))
    # A hem bus linking the channels at the bottom + a driver pocket.
    internals.append(fc.Internal("led-bus",
                                 [fc.P(W * 0.1, H * 0.08), fc.P(W * 0.9, H * 0.08)], kind="trace"))
    dx, dh = W * 0.5, 40.0
    internals.append(fc.Internal("driver-pocket", [
        fc.P(dx - dh, H * 0.03 - dh * 0.4), fc.P(dx + dh, H * 0.03 - dh * 0.4),
        fc.P(dx + dh, H * 0.03 + dh * 0.4), fc.P(dx - dh, H * 0.03 + dh * 0.4),
        fc.P(dx - dh, H * 0.03 - dh * 0.4)], kind="marking"))
    if corner_r > 0.0:
        # Marked rounded-corner trim lines (a finishing option).
        for (cx, cy, sx, sy) in [(0, 0, 1, 1), (W, 0, -1, 1), (0, H, 1, -1), (W, H, -1, -1)]:
            internals.append(fc.Internal("corner-trim", [
                fc.P(cx + sx * corner_r, cy), fc.P(cx, cy + sy * corner_r)], kind="marking"))
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(W * 0.5, H * 0.12), fc.P(W * 0.5, H * 0.88)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="LED Costume Panel",
    )


def build():
    pattern = fc.PatternSet("led-costume-panel")
    pattern.add(build_panel())
    fabric_width = 1400.0
    total_area = build_panel().area()
    marker_len = total_area / (fabric_width * 0.85)
    pattern.bom = [
        {"item": "coated / blackout costume fabric",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 85% marker; a diffusing overlay optional."},
        {"item": "LED strip + Yantra4D led-channel", "qty": channels, "unit": "lanes",
         "note": "the printable channel (see notion.hardware_ref) holds + diffuses each strip."},
        {"item": "driver + battery", "qty": 1, "unit": "set", "note": "fits the driver pocket."},
    ]
    pattern.metadata = {
        "fc200_rank": 148, "family": "etextile", "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(panel_w, 1), "height": round(panel_h, 1)},
        "channels": channels,
        "etextile_note": "A flat panel with marked LED-CHANNEL lanes (for the Yantra4D "
            "led-channel diffuser + strips), a hem bus, and a driver pocket. Channels/pocket "
            "MARKED for the maker; no electronics are drafted here.",
        "hardware": "LED channel via Yantra4D (notion.hardware_ref -> led-channel)",
    }
    return pattern


result = build()
