"""
Heated Vest Panel — Fashion Cabinet E-Textile Cartridge (FC-500 #468; y4d led-channel).

A vest whose front and back carry HEATING PANELS: serpentine channels that route a flexible
heating element (or a lit trim) across the kidneys and the chest, carried in a Yantra4D `led-
channel` extrusion so the element sits in a protective channel rather than loose against the body.
A battery/controller pocket at the front hem feeds the panels. The channel carrier is the same
`led-channel` solid the commons already uses for lit trim; here it houses a heating strip, and the
cartridge draws the routing.

  **This is a garment pattern, not an appliance.** It routes and houses a heating element in a
  channel. It contains no heater, battery, or controller, and makes no safety or thermal claim.

The routing SOLVE. A heating panel covers an AREA, but a strip element has a LENGTH, so the
panel's serpentine run must be long enough to cover the panel at the strip's own pitch:

    passes   = floor(panel_height / strip_pitch)
    run      = passes * panel_width + (passes) * strip_pitch     (the serpentine turns)

The run is drafted as a serpentine of `passes` horizontal legs joined by turns, MARKED as the
channel centre-line, so the `led-channel` carrier is cut to exactly that run. Under-route and cold
stripes appear between passes; over-route and the element bunches at the turns — both are avoided
by solving the pass count from the panel height and the strip pitch rather than eyeballing it.

The DIMENSIONAL HANDSHAKE. `led-channel` is parameterised by `strip_width` (the element it
houses). `strip_w` drives the carrier's `strip_width` AND the drafted channel width AND the vest's
own `heat_channel` interface, so the printed channel is exactly as wide as the element it carries.

Made to measure to chest/bust girth. FC-500 lane 8 (e-textile & smart garments III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 980.0))
vest_length = float(PARAM(lambda: vest_length, 560.0))       # shoulder to hem
body_ease   = float(PARAM(lambda: body_ease, 80.0))
strip_w     = float(PARAM(lambda: strip_w, 12.0))            # heating element width
panel_w     = float(PARAM(lambda: panel_w, 200.0))           # heat panel width
panel_h     = float(PARAM(lambda: panel_h, 240.0))           # heat panel height
strip_pitch = float(PARAM(lambda: strip_pitch, 40.0))        # spacing between serpentine passes
battery_pocket = float(PARAM(lambda: battery_pocket, 100.0)) # battery pocket size
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
vest_length = max(360.0, min(vest_length, 800.0))
body_ease   = max(20.0, min(body_ease, 260.0))
strip_w     = max(6.0, min(strip_w, 30.0))
panel_w     = max(90.0, min(panel_w, 340.0))
panel_h     = max(90.0, min(panel_h, 380.0))
strip_pitch = max(18.0, min(strip_pitch, 90.0))
battery_pocket = max(60.0, min(battery_pocket, 160.0))
seam_allowance = max(0.0, min(seam_allowance, 18.0))

# strip pitch must clear the strip width plus a channel wall each side
strip_pitch = max(strip_pitch, strip_w + 12.0)

# ── Solved widths ────────────────────────────────────────────────────────────
BODY = chest_bust_girth + body_ease
PANEL_QUARTER = BODY / 4.0                    # front/back share the side seam
VL = vest_length
ARMSCYE = max(200.0, VL * 0.42)
# panel dims must fit inside the body panel
PANEL_W = min(panel_w, PANEL_QUARTER * 1.6)
PANEL_H = min(panel_h, VL - ARMSCYE - 40.0)
PANEL_H = max(PANEL_H, strip_pitch)           # at least one pass
# ── The serpentine routing solve ─────────────────────────────────────────────
PASSES = max(1, int(PANEL_H // strip_pitch))
# run = horizontal legs + the vertical turns between them
SERPENTINE_RUN = PASSES * PANEL_W + (PASSES - 1) * strip_pitch


def _serpentine(x0, y0, w, passes, pitch):
    """A serpentine centre-line polyline: `passes` horizontal legs, alternating direction,
    joined by vertical turns of `pitch`."""
    pts = []
    y = y0
    for i in range(passes):
        if i % 2 == 0:
            pts.append(fc.P(x0, y))
            pts.append(fc.P(x0 + w, y))
        else:
            pts.append(fc.P(x0 + w, y))
            pts.append(fc.P(x0, y))
        y += pitch
    return pts


def _panel_edges(quarter, on_fold):
    p_hem_l = fc.P(0.0, 0.0)
    p_side_hem = fc.P(quarter, 0.0)
    underarm_y = VL - ARMSCYE
    p_underarm = fc.P(quarter, underarm_y)
    neck_w = max(70.0, quarter / 3.0)
    p_shoulder = fc.P(neck_w + (quarter - neck_w) * 0.5, VL - 10.0)
    p_neck = fc.P(neck_w, VL)
    p_cf = fc.P(0.0, VL)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_l, p_side_hem)]),
        fc.Edge("side", [fc.Line(p_side_hem, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(quarter * 0.92, underarm_y + ARMSCYE * 0.5),
                                      fc.P(p_shoulder.x + 12.0, p_shoulder.y - 30.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.5, VL - 2.0),
                                   fc.P(neck_w * 0.2, VL - 1.0), p_cf)]),
        fc.Edge("center", [fc.Line(p_cf, p_hem_l)]),
    ]
    return edges, underarm_y


def build_front():
    edges, underarm_y = _panel_edges(PANEL_QUARTER, True)
    # heat panel + serpentine routing, marked on the chest
    px = max(10.0, (PANEL_QUARTER - PANEL_W) * 0.4)
    py = VL * 0.30
    internals = [
        fc.Internal("heat-panel", [fc.P(px, py), fc.P(px + PANEL_W, py),
                                   fc.P(px + PANEL_W, py + PANEL_H), fc.P(px, py + PANEL_H),
                                   fc.P(px, py)], kind="marking"),
        fc.Internal("heat-channel-centre",
                    _serpentine(px + 6.0, py + strip_pitch / 2.0, PANEL_W - 12.0,
                                PASSES, strip_pitch),
                    kind="trace"),
        fc.Internal("lead-exit", [fc.P(px, py), fc.P(0.0, VL * 0.18)], kind="trace"),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(PANEL_QUARTER * 0.4, VL * 0.2),
                               fc.P(PANEL_QUARTER * 0.4, VL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel with heat channel (cut 2, mirror)",
    )


def build_back():
    edges, underarm_y = _panel_edges(PANEL_QUARTER, True)
    px = max(10.0, (PANEL_QUARTER - PANEL_W) * 0.4)
    py = VL * 0.24
    internals = [
        fc.Internal("heat-panel", [fc.P(px, py), fc.P(px + PANEL_W, py),
                                   fc.P(px + PANEL_W, py + PANEL_H), fc.P(px, py + PANEL_H),
                                   fc.P(px, py)], kind="marking"),
        fc.Internal("heat-channel-centre",
                    _serpentine(px + 6.0, py + strip_pitch / 2.0, PANEL_W - 12.0,
                                PASSES, strip_pitch),
                    kind="trace"),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(PANEL_QUARTER * 0.4, VL * 0.2),
                               fc.P(PANEL_QUARTER * 0.4, VL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back panel with heat channel (cut 2, mirror)",
    )


def build_battery_pocket():
    w = battery_pocket
    d = battery_pocket * 1.15
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, d), fc.P(0.0, d)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("mouth", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("lead-entry", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, d * 0.4)], kind="trace"),
                 fc.Internal("mouth-fold", [fc.P(0.0, d - 20.0), fc.P(w, d - 20.0)],
                     kind="marking")]
    return fc.Piece(
        "battery_pocket", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Battery/controller pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("heated-vest-panel")
    front = build_front()
    back = build_back()
    pocket = build_battery_pocket()

    picked = {"front": front, "back": back, "battery_pocket": pocket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, pocket):
            pattern.add(piece)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)

    fabric_width = 1550.0
    area = front.area() * 2.0 + back.area() * 2.0 + pocket.area()
    marker_len = area / (fabric_width * 0.78)
    channel_total = 2.0 * SERPENTINE_RUN * 2.0   # front + back, both sides
    pattern.bom = [
        {"item": "softshell / fleece-backed vest fabric", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front, back and pocket at {fabric_width:.0f} mm width, 78% marker."},
        {"item": "LED/heat channel carrier (Yantra4D led-channel)",
         "qty": round(channel_total), "unit": "mm_length",
         "note": f"the serpentine routing carrier, {SERPENTINE_RUN:.0f} mm per panel "
                 f"({PASSES} passes) x 4 panels (notion.hardware_ref -> led-channel); "
                 f"strip_w {strip_w:.0f} mm drives the channel AND the carrier."},
        {"item": "flexible heating element or lit trim", "qty": round(channel_total),
         "unit": "mm_length",
         "note": "housed IN the channel, never loose against the body; sourced separately — "
                 "this pattern contains no heater, battery, or controller."},
        {"item": "coverstitch + hook-loop closure", "qty": 1, "unit": "set",
         "note": "the vest closes at CF; the pocket lead-entry aligns to the panel lead-exit."},
    ]
    pattern.metadata = {
        "fc500_rank": 468, "family": "etextile", "fabric_hint": "jersey-conductor",
        "not_an_appliance": "This routes and houses a heating element in a channel. It contains "
                            "no heater, battery, or controller and makes no thermal claim.",
        "silhouette_note": "A vest whose front and back carry serpentine heat-channel panels over "
            "the chest and kidneys, fed from a battery pocket at the hem. The routing is solved "
            "so the element covers the panel at its own pitch — no cold stripes, no bunching.",
        "hardware": "channel carrier via Yantra4D (notion.hardware_ref -> led-channel); strip_w "
            "drives the carrier's strip_width AND the drafted channel width.",
        "solved": {
            "panel_w_mm": round(PANEL_W, 1),
            "panel_h_mm": round(PANEL_H, 1),
            "strip_pitch_mm": round(strip_pitch, 1),
            "passes": PASSES,
            "serpentine_run_mm": round(SERPENTINE_RUN, 1),
            "note": "passes = panel_h // strip_pitch; run = passes*panel_w + (passes-1)*pitch. "
                    "strip_pitch is floored at strip_w + 12 so passes never overlap the element.",
        },
        "etextile_note": "The heat panel, the serpentine channel centre-line, the lead exit and "
                         "the pocket lead-entry are MARKED. No heater, conductor, battery, or "
                         "circuit is drafted here.",
    }
    return pattern


result = build()
