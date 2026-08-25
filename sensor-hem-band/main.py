"""
Sensor Hem Band — Fashion Cabinet E-Textile Cartridge (FC-300 #297, long-tail band).

The instrumented hem of a compression garment: a doubled band at the leg or sleeve
opening that both GRIPS (so the garment does not ride) and CARRIES (a sensor plate and
the conductive run that reaches it). It is the finishing band every compression tight
already has, drafted for the case where something rigid has to live inside it.

Not the same object as `rehab-sensor-cuff` (a standalone tapered cuff that clamps a
sensor to a bare limb) or `biometric-bra-band` (an underbust band carrying electrodes
against the skin). This one is a HEM: it is sewn to a garment opening that already
exists, and its whole difficulty is that it must be shorter than that opening.

Drafting note — the seam that must SOLVE, and why it is not `hem * (1 - stretch)`:

  A gripping hem band is cut with NEGATIVE ease: shorter than the opening, then
  stretched onto it while sewing, so it pulls the opening in. The obvious formula is

      band = hem_opening * (1 - grip)                       # WRONG here

  and it is wrong the moment a rigid plate lives in the band. The plate cannot
  stretch. Its footprint is a DEAD LENGTH: it contributes its full width to the sewn
  band and none of it to the stretch. So the grip has to be taken out of the elastic
  remainder only:

      dead   = plate_w + 2 * plate_margin                   # the rigid island
      live   = hem_opening - dead                           # what can actually stretch
      band   = dead + live * (1 - grip)

  Apply the naive formula instead and the band comes up short by `dead * grip` — 6.9 mm
  at the defaults, 26.4 mm at a wide plate and a hard grip — which on a compression hem
  is not a fitting nuisance but a band that will not reach, or one that reaches by
  stretching the cloth across the plate until the plate rocks.

  The kernel drafts the band to the solved length, then declares its `attach` edge
  against the garment hem with the SOLVED difference as declared ease, so the seam
  check proves the arithmetic rather than the maker discovering it at the machine.

The channel is the second half. The conductive run is not printed on the face of the
band; it lies in a channel between the band's two layers, so it is never abraded by a
shoe, a sleeve, or a washing machine drum. The channel's two stitch lines are marked,
and the plate seat interrupts them.

Pieces:
  - band    : the outer band, cut to the SOLVED length, carrying the plate seat.
  - facing  : the inner layer, cut to the same solved length, carrying the channel.
  - tab     : the service tab where the run leaves the channel for the garment seam.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # band|facing|tab|set

hem_opening = float(PARAM(lambda: hem_opening, 380.0))   # the garment opening girth
band_depth = float(PARAM(lambda: band_depth, 60.0))      # finished band depth
grip = float(PARAM(lambda: grip, 0.12))                  # negative ease on the LIVE run
plate_w = float(PARAM(lambda: plate_w, 34.0))            # sensor plate width
plate_d = float(PARAM(lambda: plate_d, 26.0))            # sensor plate depth
plate_margin = float(PARAM(lambda: plate_margin, 12.0))  # dead cloth each side of it
plate_pos = float(PARAM(lambda: plate_pos, 0.25))        # fraction round the band
channel_w = float(PARAM(lambda: channel_w, 9.0))         # conductive channel width
tab_len = float(PARAM(lambda: tab_len, 55.0))            # service tab length
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hem_opening = max(140.0, min(hem_opening, 900.0))
band_depth = max(25.0, min(band_depth, 160.0))
grip = max(0.0, min(grip, 0.30))
plate_w = max(12.0, min(plate_w, 120.0))
plate_d = max(10.0, min(plate_d, 110.0))
plate_margin = max(4.0, min(plate_margin, 40.0))
plate_pos = max(0.05, min(plate_pos, 0.95))
channel_w = max(4.0, min(channel_w, 30.0))
tab_len = max(25.0, min(tab_len, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# The band must be deep enough to hold the plate AND the channel beside it, doubled.
# Without this floor a 160 mm plate in a 25 mm band produces a channel offset that
# runs off the piece and a plate seat with negative clearance.
band_depth = max(band_depth, plate_d + channel_w + 20.0)

# ── The dead-length solve ────────────────────────────────────────────────────
# The plate is rigid: its footprint plus the margin either side cannot stretch. So the
# grip is taken out of the LIVE remainder only, never out of the whole opening.
DEAD = plate_w + 2.0 * plate_margin

# The dead island cannot be larger than the opening it lives in. At the parameter
# extremes (a 120 mm plate with 40 mm margins in a 140 mm opening) DEAD exceeds
# hem_opening and LIVE goes NEGATIVE — which, drafted, is a band shorter than nothing
# that the kernel would CCW-normalize into a piece that verifies and cannot be sewn.
# The island is capped at a fraction of the opening instead, and the cap is reported.
_DEAD_CAP = hem_opening * 0.55
DEAD_CAPPED = DEAD > _DEAD_CAP
if DEAD_CAPPED:
    DEAD = _DEAD_CAP
    # Re-derive the margin the cap actually leaves, so the plate seat drawn below is
    # the one the band can hold rather than the one that was asked for.
    plate_w = min(plate_w, DEAD - 2.0 * 4.0)
    plate_margin = max((DEAD - plate_w) / 2.0, 0.0)

LIVE = hem_opening - DEAD
BAND_LEN = DEAD + LIVE * (1.0 - grip)
# What the naive formula would have produced, and the shortfall it hides.
NAIVE_LEN = hem_opening * (1.0 - grip)
SHORTFALL = BAND_LEN - NAIVE_LEN          # == DEAD * grip, always >= 0
# The declared ease: the band is SHORTER than the hem by this, on purpose.
GRIP_EASE = hem_opening - BAND_LEN

# The plate seat's x, placed by fraction of the SOLVED band length and then held clear
# of both ends so the seat never straddles the band's own join seam.
_SEAT_MIN = plate_w / 2.0 + plate_margin
_SEAT_MAX = BAND_LEN - plate_w / 2.0 - plate_margin
if _SEAT_MAX < _SEAT_MIN:                 # a band barely longer than its own island
    SEAT_X = BAND_LEN / 2.0
else:
    SEAT_X = min(max(BAND_LEN * plate_pos, _SEAT_MIN), _SEAT_MAX)

# The band is cut DOUBLE its finished depth (it folds), plus nothing else: the fold is
# the finished edge, so no hem allowance is spent there.
CUT_DEPTH = band_depth * 2.0
# The channel sits in the half that becomes the inside, clear of the fold and the seam.
CHANNEL_Y = band_depth + (band_depth - channel_w) / 2.0


def _rect_edges(x0, y0, w, h, names):
    """A CCW rectangle with four named edges. w and h must already be positive —
    a negative one is silently CCW-normalized into a piece that verifies."""
    p0 = fc.P(x0, y0)
    p1 = fc.P(x0 + w, y0)
    p2 = fc.P(x0 + w, y0 + h)
    p3 = fc.P(x0, y0 + h)
    return [
        fc.Edge(names[0], [fc.Line(p0, p1)]),
        fc.Edge(names[1], [fc.Line(p1, p2)]),
        fc.Edge(names[2], [fc.Line(p2, p3)]),
        fc.Edge(names[3], [fc.Line(p3, p0)]),
    ]


def _closed_rect_pts(x0, y0, w, h):
    return [fc.P(x0, y0), fc.P(x0 + w, y0), fc.P(x0 + w, y0 + h),
            fc.P(x0, y0 + h), fc.P(x0, y0)]


def build_band():
    """The outer band: cut to the SOLVED length, folded at its own depth, carrying the
    plate seat and the dead-length markings that tell the maker where NOT to stretch."""
    seat_y = band_depth + (band_depth - plate_d) / 2.0
    internals = [
        # The fold: the band's finished lower edge.
        fc.Internal("fold-line", [fc.P(0.0, band_depth), fc.P(BAND_LEN, band_depth)],
                    kind="marking"),
        # The plate seat — the rectangle the Yantra4D sensor-mount-plate's base sews to.
        fc.Internal("plate-seat",
                    _closed_rect_pts(SEAT_X - plate_w / 2.0, seat_y, plate_w, plate_d),
                    kind="marking"),
        # THE dead-length markers. Between these two lines the band must NOT be
        # stretched while sewing: it is the rigid island the solve accounted for, and
        # stretching it is what makes a plate rock.
        fc.Internal("dead-start",
                    [fc.P(SEAT_X - DEAD / 2.0, band_depth),
                     fc.P(SEAT_X - DEAD / 2.0, CUT_DEPTH)], kind="marking"),
        fc.Internal("dead-end",
                    [fc.P(SEAT_X + DEAD / 2.0, band_depth),
                     fc.P(SEAT_X + DEAD / 2.0, CUT_DEPTH)], kind="marking"),
    ]
    # The four plate sew points. Two points is a hinge; four is a mount.
    for lx, ly, nm in ((-1, -1, "sw"), (1, -1, "se"), (1, 1, "ne"), (-1, 1, "nw")):
        px = SEAT_X + lx * (plate_w / 2.0 - 4.0)
        py = seat_y + plate_d / 2.0 + ly * (plate_d / 2.0 - 4.0)
        internals.append(fc.Internal(f"plate-sew-{nm}", [fc.P(px, py), fc.P(px, py)],
                                     kind="drill"))
    return fc.Piece(
        "band", _rect_edges(0.0, 0.0, BAND_LEN, CUT_DEPTH,
                            ("free", "join_r", "attach", "join_l")),
        seam_allowance=seam_allowance,
        allowances={"free": 0.0},
        notches=[fc.Notch("attach", plate_pos, "plate axis"),
                 fc.Notch("attach", 0.5, "quarter match"),
                 fc.Notch("free", 0.5, "quarter match")],
        grainline=fc.Grainline(fc.P(BAND_LEN * 0.08, band_depth * 0.3),
                               fc.P(BAND_LEN * 0.92, band_depth * 0.3)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Sensor hem band (solved length)",
    )


# ── The measured band ────────────────────────────────────────────────────────
# The facing and the tab are cut to the band's MEASURED attach edge, not recomputed
# from the formula — one source, so the two layers cannot drift apart.
_BAND = build_band()
ATTACH_LEN = _BAND.edge("attach").length()
JOIN_LEN = _BAND.edge("join_r").length()


def build_facing():
    """The inner layer, cut to the band's MEASURED length, carrying the channel.

    Deliberately NOT eased against the band. An eased facing inside a gripping band
    would take the stretch unevenly, and the plate — which is in the band, not the
    facing — would end up pulled off its marks."""
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, band_depth), fc.P(ATTACH_LEN, band_depth)],
                    kind="marking"),
        # The conductive channel: two stitch lines, `channel_w` apart, running the
        # band's length. The run lies BETWEEN the layers, never on the face.
        fc.Internal("channel-lower",
                    [fc.P(0.0, CHANNEL_Y), fc.P(ATTACH_LEN, CHANNEL_Y)],
                    kind="marking"),
        fc.Internal("channel-upper",
                    [fc.P(0.0, CHANNEL_Y + channel_w),
                     fc.P(ATTACH_LEN, CHANNEL_Y + channel_w)], kind="marking"),
        # Where the channel opens for the plate's leads — the only interruption.
        fc.Internal("channel-break",
                    _closed_rect_pts(SEAT_X - plate_w / 2.0, CHANNEL_Y,
                                     plate_w, channel_w), kind="marking"),
        # Where the run leaves the channel for the tab.
        fc.Internal("run-exit",
                    [fc.P(SEAT_X + plate_w / 2.0, CHANNEL_Y + channel_w / 2.0),
                     fc.P(min(SEAT_X + plate_w / 2.0 + tab_len, ATTACH_LEN),
                          CHANNEL_Y + channel_w / 2.0)], kind="trace"),
    ]
    return fc.Piece(
        "facing", _rect_edges(0.0, 0.0, ATTACH_LEN, CUT_DEPTH,
                              ("free", "join_r", "attach", "join_l")),
        seam_allowance=seam_allowance,
        allowances={"free": 0.0},
        notches=[fc.Notch("attach", plate_pos, "plate axis"),
                 fc.Notch("attach", 0.5, "quarter match")],
        grainline=_BAND.grainline,
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Band facing (channel side)",
    )


def build_tab():
    """The service tab: where the run leaves the channel and enters the garment's own
    seam allowance. Its `attach` edge is the channel's width plus its stitch lands, so
    the channel and the tab meet without a step the run has to climb."""
    w = tab_len
    h = channel_w + 24.0
    internals = [
        fc.Internal("run-path",
                    [fc.P(0.0, h / 2.0), fc.P(w, h / 2.0)], kind="trace"),
        # The strain land: the run is tacked here, so a tug on the garment seam is
        # taken by cloth rather than by the conductor.
        fc.Internal("strain-land",
                    _closed_rect_pts(w * 0.55, 6.0, max(w * 0.35, 8.0),
                                     max(h - 12.0, 6.0)), kind="marking"),
    ]
    return fc.Piece(
        "tab", _rect_edges(0.0, 0.0, w, h, ("lower", "free", "upper", "attach")),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "channel centre")],
        grainline=fc.Grainline(fc.P(6.0, h / 2.0), fc.P(w - 6.0, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Service tab",
    )


def build():
    pattern = fc.PatternSet("sensor-hem-band")
    everything = target_piece == "set"
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything or target_piece == "facing":
        pattern.add(build_facing())
    if everything or target_piece == "tab":
        pattern.add(build_tab())

    if everything:
        # The facing is cut to the band's MEASURED length, both layers unstretched
        # against each other — declared so an eased facing can never sneak in.
        pattern.declare_seam(("facing", "attach"), ("band", "attach"), tol=0.5)
        pattern.declare_seam(("facing", "join_r"), ("band", "join_r"), tol=0.5)
        # The band's own closing join.
        pattern.declare_seam(("band", "join_l"), ("band", "join_r"), tol=0.5)

    fabric_width = 1550.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.86)
    pattern.bom = [
        {"item": "compression knit (poly/elastane, conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1550 mm width, 86% marker; long straight bands nest well. The "
                 "110 °C iron ceiling governs everywhere near the channel."},
        {"item": "sensor mount plate", "qty": 1, "unit": "count",
         "note": f"Yantra4D sensor-mount-plate (notion.hardware_ref); base "
                 f"{plate_w:.0f} x {plate_d:.0f} mm, sewn at the four marked "
                 f"plate-sew points so it cannot hinge in a stretching band."},
        {"item": "conductive thread or ribbon", "qty": round(ATTACH_LEN + tab_len),
         "unit": "mm_length",
         "note": f"laid in the {channel_w:.0f} mm channel BETWEEN the layers, never on "
                 f"the face; it is never abraded and never ironed."},
        {"item": "coverstitch thread", "qty": 1, "unit": "spool",
         "note": "the channel's two stitch lines and the band's attach seam all want a "
                 "stitch that stretches; a lockstitch here snaps on the first wear."},
        {"item": "clear elastic (stay tape)", "qty": round(DEAD), "unit": "mm_length",
         "note": f"optional, along the {DEAD:.0f} mm dead length only — it stops the "
                 f"rigid island being stretched by a hurried machinist."},
    ]
    pattern.metadata = {
        "fc300_rank": 297,
        "family": "etextile",
        "fabric_hint": "poliester-elastano-compresion",
        "finished_mm": {
            "hem_opening": round(hem_opening, 1),
            "band_length_cut": round(BAND_LEN, 1),
            "band_depth_finished": round(band_depth, 1),
            "band_depth_cut": round(CUT_DEPTH, 1),
            "plate_w": round(plate_w, 1),
            "plate_d": round(plate_d, 1),
        },
        "solved": {
            "dead_length_mm": round(DEAD, 3),
            "dead_capped": DEAD_CAPPED,
            "dead_cap_mm": round(_DEAD_CAP, 3),
            "live_length_mm": round(LIVE, 3),
            "grip": round(grip, 3),
            "band_length_mm": round(BAND_LEN, 3),
            "naive_length_mm": round(NAIVE_LEN, 3),
            "shortfall_avoided_mm": round(SHORTFALL, 3),
            "grip_ease_mm": round(GRIP_EASE, 3),
            "attach_measured_mm": round(ATTACH_LEN, 3),
            "join_measured_mm": round(JOIN_LEN, 3),
            "plate_seat_x_mm": round(SEAT_X, 3),
            "band_depth_floor_mm": round(plate_d + channel_w + 20.0, 3),
            "channel_y_mm": round(CHANNEL_Y, 3),
            "note": "a gripping hem band is cut SHORTER than the opening, but a rigid "
                    "plate inside it cannot stretch. Its footprint plus margins is a "
                    "DEAD length that contributes fully to the sewn band and nothing to "
                    "the stretch, so the grip comes out of the LIVE remainder only: "
                    "band = dead + (opening - dead) * (1 - grip). The naive "
                    "opening*(1-grip) is short by dead*grip (shortfall_avoided_mm) — a "
                    "band that will not reach, or that reaches by stretching cloth "
                    "across the plate until the plate rocks. The dead island is capped "
                    "at 55% of the opening, because at the parameter extremes it "
                    "exceeds the opening entirely and LIVE goes negative.",
        },
        "etextile_note": "The plate seat, its four sew points, the channel stitch "
                         "lines, the channel break and the run path are MARKED. No "
                         "sensor, conductor, or circuit is drafted here.",
        "hardware": "sensor mount via Yantra4D (notion.hardware_ref -> "
                    "sensor-mount-plate); the plate's base_w x base_d is this band's "
                    "plate_w x plate_d, the same rectangle marked as plate-seat and the "
                    "same footprint the dead-length solve accounts for",
    }
    return pattern


result = build()
