"""
LED Safety Sash — Fashion Cabinet E-Textile Cartridge (FC-500 #470; y4d led-channel).

A high-visibility sash worn diagonally across the torso, carrying a lit LED strip along its whole
length in a Yantra4D `led-channel` extrusion so the strip is protected and diffused rather than
loose, with a small battery pocket at the lower end and a side-release fastening loop so it goes
on over any jacket. It is the simplest possible instrumented garment — one long strip — and its
whole craft is that the channel is exactly as long as the sash, and the sash is cut to a REAL
diagonal torso span rather than a one-size loop.

  **This is a garment pattern, not a light.** It houses and routes an LED strip in a channel. It
  contains no LED, battery, or circuit and makes no lighting or safety-certification claim.

The span SOLVE. A diagonal shoulder-to-hip sash is longer than a horizontal band: it runs from the
shoulder, across the chest, to the opposite hip, so its length is the hypotenuse of the chest rise
and the cross-body reach, times a wrap-and-overlap factor. Cut to a horizontal girth it comes up
short and rides up over the shoulder. The cartridge solves the diagonal from `torso_height` and
`chest_bust_girth`, so the sash actually reaches, and the LED channel is cut to that measured run.

The DIMENSIONAL HANDSHAKE. `led-channel` is parameterised by `strip_width`. `strip_w` drives the
carrier's `strip_width` AND the drafted channel width AND the sash's own `led_channel` interface,
so the printed channel is exactly as wide as the strip it diffuses.

Made to measure to chest/bust girth and torso height. FC-500 lane 8 (e-textile & smart garments
III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 960.0))
torso_height = float(PARAM(lambda: torso_height, 500.0))    # shoulder to hip drop
sash_width  = float(PARAM(lambda: sash_width, 90.0))        # finished sash width
strip_w     = float(PARAM(lambda: strip_w, 12.0))           # LED strip width
overlap     = float(PARAM(lambda: overlap, 1.15))           # wrap-and-overlap factor
battery_pocket = float(PARAM(lambda: battery_pocket, 80.0))
loop_width  = float(PARAM(lambda: loop_width, 40.0))        # side-release loop width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
torso_height = max(300.0, min(torso_height, 750.0))
sash_width  = max(50.0, min(sash_width, 160.0))
strip_w     = max(6.0, min(strip_w, 30.0))
overlap     = max(1.0, min(overlap, 1.4))
battery_pocket = max(50.0, min(battery_pocket, 140.0))
loop_width  = max(25.0, min(loop_width, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 18.0))

# channel must fit inside the sash width with a wall each side
strip_w = min(strip_w, sash_width - 24.0)

# ── The diagonal-span solve ──────────────────────────────────────────────────
# The sash runs from a shoulder, diagonally across the chest, to the opposite hip. Its span is
# the hypotenuse of the vertical torso drop and the cross-body horizontal reach (half the chest
# girth, since it crosses one side of the body), times a wrap-and-overlap factor for the join.
CROSS_REACH = chest_bust_girth * 0.5
DIAGONAL = math.hypot(torso_height, CROSS_REACH)
SASH_LEN = DIAGONAL * overlap
SW = sash_width


def build_sash():
    """The sash body: a long strip carrying the LED channel down its centre, plus the loop tab
    at the top and the battery pocket seat marked at the bottom."""
    p0, p1 = fc.P(0.0, 0.0), fc.P(SASH_LEN, 0.0)
    p2, p3 = fc.P(SASH_LEN, SW), fc.P(0.0, SW)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end_bottom", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("end_top", [fc.Line(p3, p0)]),
    ]
    cy = SW / 2.0
    internals = [
        fc.Internal("led-channel-centre", [fc.P(12.0, cy), fc.P(SASH_LEN - 12.0, cy)],
            kind="trace"),
        fc.Internal("channel-lower", [fc.P(12.0, cy - strip_w / 2.0),
                                      fc.P(SASH_LEN - 12.0, cy - strip_w / 2.0)], kind="marking"),
        fc.Internal("channel-upper", [fc.P(12.0, cy + strip_w / 2.0),
                                      fc.P(SASH_LEN - 12.0, cy + strip_w / 2.0)], kind="marking"),
        fc.Internal("battery-lead", [fc.P(SASH_LEN - 12.0, cy), fc.P(SASH_LEN - 40.0, cy)],
                    kind="trace"),
    ]
    return fc.Piece(
        "sash", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("end_top", 0.5, "loop position"),
                 fc.Notch("end_bottom", 0.5, "pocket/buckle position")],
        grainline=fc.Grainline(fc.P(SASH_LEN * 0.08, cy), fc.P(SASH_LEN * 0.92, cy)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Safety sash (LED channel down the centre)",
    )


def build_loop():
    """The shoulder loop tab: a small strip that folds around the side-release buckle at the top."""
    w = loop_width
    d = SW * 0.9
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, d), fc.P(0.0, d)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("fold", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "loop", edges, seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        cut=fc.CutSpec(quantity=2),
        label="Shoulder loop tab (cut 2)",
    )


def build_pocket():
    w = battery_pocket
    d = battery_pocket * 1.2
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
                 fc.Internal("mouth-fold", [fc.P(0.0, d - 18.0), fc.P(w, d - 18.0)],
                     kind="marking")]
    return fc.Piece(
        "battery_pocket", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Battery pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("led-safety-sash")
    sash = build_sash()
    loop = build_loop()
    pocket = build_pocket()

    picked = {"sash": sash, "loop": loop, "battery_pocket": pocket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (sash, loop, pocket):
            pattern.add(piece)
        # The two loop tabs each fold in half and are BAR-TACKED to the sash ends around the
        # buckle webbing (a construction tack, not a balanced edge-to-edge seam), so the loop
        # is marked, not declared. The sash is a single continuous piece with no join seam to
        # verify; its LED channel run is carried in metadata and the BOM.
        _ = (loop, pocket)  # both are separate finished pieces attached by topstitch/tack

    channel_run = SASH_LEN - 24.0

    fabric_width = 1500.0
    area = sash.area() + loop.area() * 2.0 + pocket.area()
    marker_len = area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "hi-vis fabric (fluoro + reflective tape)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"sash, loop and pocket at {fabric_width:.0f} mm width, 82% marker; add "
                 "retroreflective tape either side of the LED channel."},
        {"item": "LED channel carrier (Yantra4D led-channel)", "qty": round(channel_run),
         "unit": "mm_length",
         "note": f"the diffusing channel down the sash centre, {SASH_LEN - 24.0:.0f} mm "
                 f"(notion.hardware_ref -> led-channel); strip_w {strip_w:.0f} mm drives the "
                 "channel AND the carrier."},
        {"item": "LED strip + battery + controller", "qty": 1, "unit": "set",
         "note": "housed IN the channel and the pocket; sourced separately — this pattern "
                 "contains no LED, battery, or controller."},
        {"item": "side-release buckle + webbing", "qty": 1, "unit": "set",
         "note": "the shoulder/hip fastening so the sash goes on over a jacket."},
    ]
    pattern.metadata = {
        "fc500_rank": 470, "family": "etextile", "fabric_hint": "nylon-satinado",
        "not_a_light": "This houses and routes an LED strip in a channel. It contains no LED, "
                       "battery, or circuit and makes no lighting or certification claim.",
        "silhouette_note": "A diagonal high-vis sash with an LED channel down its whole length, a "
            "battery pocket at the lower end, and a side-release loop. Cut to a real diagonal "
            "torso span, not a one-size loop.",
        "hardware": "channel carrier via Yantra4D (notion.hardware_ref -> led-channel); strip_w "
            "drives the carrier's strip_width AND the drafted channel width.",
        "solved": {
            "cross_reach_mm": round(CROSS_REACH, 1),
            "diagonal_mm": round(DIAGONAL, 1),
            "sash_length_mm": round(SASH_LEN, 1),
            "channel_run_mm": round(SASH_LEN - 24.0, 1),
            "note": "SASH_LEN = hypot(torso_height, chest/2) * overlap: a diagonal sash is the "
                    "hypotenuse of the torso drop and the cross-body reach, not a horizontal "
                    "girth — cut to a girth it rides up over the shoulder.",
        },
        "etextile_note": "The LED channel centre-line, its two stitch lines, the battery lead "
                         "and the pocket lead-entry are MARKED. No LED, conductor, battery, or "
                         "circuit is drafted here.",
    }
    return pattern


result = build()
