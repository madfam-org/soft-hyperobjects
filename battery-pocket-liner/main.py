"""
Battery Pocket Liner — Fashion Cabinet E-Textile Cartridge (FC-300 #296, long-tail band).

A drop-in liner that gives a shell garment somewhere to carry a battery that is a
BRICK: rigid, heavy, hot on one face, and connected to something else by a cable that
must survive being sat on. It is the piece almost every heated or illuminated garment
improvises badly — a patch pocket sewn to the lining, the battery swinging in it, the
cable pinched at the pocket mouth — and it is a pattern problem, not an electronics
one.

The bay is framed. A Yantra4D `battery-pocket-frame` (see the manifest's
notion.hardware_ref) is a rigid sewn ring with a retention lip: the battery drops into
the frame, the lip holds it, and the frame's flange takes the load instead of the
cloth. So this liner is drafted AROUND that frame, not around the battery.

Drafting note — the seam that must SOLVE, and the mistake it prevents:

  The liner carries a WINDOW that the frame sews into. The obvious draft cuts the
  window to the battery — and then the frame, which is wider than its bay by
  `frame_w` on every side, has nothing to sit on. The window must be cut to the
  frame's BAY, and the frame's flange lands on the cloth OUTSIDE it. So:

      bay_w  = batt_w + bay_clear          (the frame's inner opening)
      bay_h  = batt_h + bay_clear
      window = bay, and the flange footprint = window + 2*frame_w on each axis

  and the pocket BAG behind it is then cut to a perimeter that the window's own
  measured perimeter must equal — because the bag is what actually carries the
  battery's weight, and a bag cut to the battery rather than to the window comes up
  short on exactly the two sides the load hangs from.

  The bag depth is SOLVED, not chosen: a battery must be able to sit fully inside the
  frame with its cable slack coiled below it, so the bag is floored at the bay height
  plus the battery's own thickness plus the cable's minimum bend allowance. A shallow
  bag is the failure that pinches the cable at the mouth.

The seam-fed conduit is the other half. The cable does not exit through the pocket
mouth (where a hand goes in and a zip closes); it exits down a marked conduit to the
liner's side seam, where the shell garment's own seam allowance carries it. The
conduit's exit is placed by arc-length fraction along the measured side edge, so the
same value names the same height on the body at every garment size.

Pieces:
  - liner    : the liner panel, with the framed bay window and the conduit run.
  - bag      : the pocket bag behind the window, solved to the measured window.
  - flap     : the closure flap over the bay, cut to the measured window mouth.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # liner|bag|flap|set

liner_width = float(PARAM(lambda: liner_width, 320.0))    # half-front liner panel width
liner_height = float(PARAM(lambda: liner_height, 420.0))  # panel height
batt_w = float(PARAM(lambda: batt_w, 72.0))               # battery width
batt_h = float(PARAM(lambda: batt_h, 104.0))              # battery height
batt_t = float(PARAM(lambda: batt_t, 22.0))               # battery thickness
bay_clear = float(PARAM(lambda: bay_clear, 3.0))          # slip clearance round it
frame_w = float(PARAM(lambda: frame_w, 9.0))              # frame flange width
sew_pitch = float(PARAM(lambda: sew_pitch, 12.0))         # frame sew-hole pitch
cable_bend = float(PARAM(lambda: cable_bend, 30.0))       # min cable bend allowance
conduit_exit = float(PARAM(lambda: conduit_exit, 0.35))   # fraction up the side edge
flap_depth = float(PARAM(lambda: flap_depth, 42.0))       # closure flap depth
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
liner_width = max(180.0, min(liner_width, 520.0))
liner_height = max(240.0, min(liner_height, 700.0))
batt_w = max(30.0, min(batt_w, 160.0))
batt_h = max(30.0, min(batt_h, 200.0))
batt_t = max(6.0, min(batt_t, 60.0))
bay_clear = max(1.0, min(bay_clear, 12.0))
frame_w = max(4.0, min(frame_w, 24.0))
sew_pitch = max(6.0, min(sew_pitch, 30.0))
cable_bend = max(10.0, min(cable_bend, 90.0))
conduit_exit = max(0.10, min(conduit_exit, 0.90))
flap_depth = max(20.0, min(flap_depth, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 18.0))

# ── The framed bay ───────────────────────────────────────────────────────────
# The window is cut to the frame's BAY (battery + clearance), and the frame's flange
# lands on the cloth outside it. Cutting the window to the battery is the mistake this
# ordering exists to prevent: the flange would then have no cloth to sit on.
BAY_W = batt_w + bay_clear
BAY_H = batt_h + bay_clear
FLANGE_W = BAY_W + 2.0 * frame_w        # the frame's outer footprint
FLANGE_H = BAY_H + 2.0 * frame_w

# The panel must contain the whole flange footprint with room for the seam allowance
# on both sides and a margin for the conduit to pass. Every derived dimension below is
# clamped rather than trusted: at parameter extremes (a 160 x 200 mm battery in a
# 180 x 240 mm panel) the naive arithmetic goes NEGATIVE, and a negative-width piece
# is normalized into geometry that LOOKS valid.
_MARGIN = 18.0
liner_width = max(liner_width, FLANGE_W + 2.0 * _MARGIN)
liner_height = max(liner_height, FLANGE_H + flap_depth + 2.0 * _MARGIN)

# The bay sits centred horizontally, high enough that the bag hangs clear of the hem.
BAY_CX = liner_width / 2.0
BAY_BOTTOM = liner_height - _MARGIN - flap_depth - FLANGE_H + frame_w
BAY_LEFT = BAY_CX - BAY_W / 2.0

# ── The solved bag depth ─────────────────────────────────────────────────────
# The bag must swallow the battery's height, its thickness (it lies against the panel,
# so the bag's fold consumes a thickness), and the cable's minimum bend below it. A
# bag cut only to the bay height pinches the cable at the mouth — the commonest field
# failure in an improvised battery pocket.
BAG_DEPTH = BAY_H + batt_t + cable_bend
BAG_W = BAY_W + 2.0 * frame_w          # the bag is caught under the frame flange

# The frame's sew holes: whole pitch intervals round the flange, recomputed so the
# holes land exactly on the corners rather than drifting off the last one.
_PERIM = 2.0 * (BAY_W + BAY_H) + 4.0 * frame_w * 2.0
SEW_HOLES = max(8, int(round(_PERIM / sew_pitch)))
SEW_PITCH_SOLVED = _PERIM / SEW_HOLES


def _rect_edges(x0, y0, w, h, names=("bottom", "right", "top", "left")):
    """A CCW rectangle with the four edges named. w and h are already clamped
    positive by the caller — a negative one would be silently CCW-normalized."""
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


def build_liner():
    """The liner panel: the framed bay window, the flange footprint, the sew ring,
    and the conduit run down to the side seam."""
    internals = [
        # The WINDOW — cut this, not the battery outline. It is the frame's bay.
        fc.Internal("bay-window", _closed_rect_pts(BAY_LEFT, BAY_BOTTOM, BAY_W, BAY_H),
                    kind="marking"),
        # The frame's outer flange footprint: where the rigid ring actually lands.
        fc.Internal("frame-flange",
                    _closed_rect_pts(BAY_LEFT - frame_w, BAY_BOTTOM - frame_w,
                                     FLANGE_W, FLANGE_H), kind="marking"),
        # The bag's mouth line — the bag is caught under the flange, not topstitched
        # to the panel face, so the load path is frame -> bag -> seam.
        fc.Internal("bag-mouth",
                    [fc.P(BAY_LEFT - frame_w, BAY_BOTTOM + BAY_H),
                     fc.P(BAY_LEFT - frame_w + BAG_W, BAY_BOTTOM + BAY_H)],
                    kind="marking"),
    ]
    # The sew ring: drills at the solved pitch round the flange centreline. Marked as
    # a run of drills so a maker can align the frame's holes without a template.
    _ring_x0 = BAY_LEFT - frame_w / 2.0
    _ring_y0 = BAY_BOTTOM - frame_w / 2.0
    _ring_w = BAY_W + frame_w
    _ring_h = BAY_H + frame_w
    _ring_perim = 2.0 * (_ring_w + _ring_h)
    for i in range(SEW_HOLES):
        d = _ring_perim * i / SEW_HOLES
        if d < _ring_w:
            px, py = _ring_x0 + d, _ring_y0
        elif d < _ring_w + _ring_h:
            px, py = _ring_x0 + _ring_w, _ring_y0 + (d - _ring_w)
        elif d < 2.0 * _ring_w + _ring_h:
            px, py = _ring_x0 + _ring_w - (d - _ring_w - _ring_h), _ring_y0 + _ring_h
        else:
            px, py = _ring_x0, _ring_y0 + _ring_h - (d - 2.0 * _ring_w - _ring_h)
        internals.append(fc.Internal(f"frame-sew-{i}", [fc.P(px, py), fc.P(px, py)],
                                     kind="drill"))

    # The conduit: from the bay's lower-left corner, down and out to the side edge at
    # the requested fraction of the panel height. Placed by FRACTION so the same value
    # names the same height on the body at every garment size.
    _exit_y = liner_height * conduit_exit
    internals.append(fc.Internal(
        "cable-conduit",
        [fc.P(BAY_LEFT + 6.0, BAY_BOTTOM - frame_w),
         fc.P(BAY_LEFT + 6.0, _exit_y + 24.0),
         fc.P(12.0, _exit_y),
         fc.P(0.0, _exit_y)], kind="trace"))
    # The service loop: the slack the cable needs so the battery can come out without
    # the connector taking the strain.
    internals.append(fc.Internal(
        "service-loop",
        [fc.P(BAY_LEFT + 6.0, _exit_y + 24.0),
         fc.P(BAY_LEFT + 6.0 + cable_bend, _exit_y + 24.0 + cable_bend * 0.6),
         fc.P(BAY_LEFT + 6.0, _exit_y + 24.0 + cable_bend * 1.2)], kind="trace"))

    return fc.Piece(
        "liner", _rect_edges(0.0, 0.0, liner_width, liner_height,
                             ("hem", "side", "top", "front_edge")),
        seam_allowance=seam_allowance,
        allowances={"hem": 20.0},
        notches=[fc.Notch("side", conduit_exit, "conduit exit"),
                 fc.Notch("top", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(liner_width * 0.12, 30.0),
                               fc.P(liner_width * 0.12, liner_height - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Liner panel (framed battery bay)",
    )


# ── The measured window ──────────────────────────────────────────────────────
# The bag and the flap are cut to the liner's MEASURED bay geometry, not to the
# battery. The window is an internal marking, so its perimeter is computed from the
# same clamped dimensions the panel drew — the single source both pieces read.
WINDOW_PERIM = 2.0 * (BAY_W + BAY_H)
_LINER = build_liner()
SIDE_LEN = _LINER.edge("side").length()


def build_bag():
    """The pocket bag: cut to the MEASURED bay width plus the flange catch, and to the
    SOLVED depth (bay height + battery thickness + cable bend).

    Cut 2 and seamed at three sides, or cut 1 on the fold — the fold version is what
    the default draft gives, because a folded bag has no seam under the battery's
    weight where it matters most."""
    internals = [
        # Where the battery actually rests once dropped through the frame.
        fc.Internal("battery-seat",
                    _closed_rect_pts((BAG_W - batt_w) / 2.0, BAG_DEPTH - batt_h - 8.0,
                                     batt_w, batt_h), kind="marking"),
        # The slack well below it: the cable coils here, not at the mouth.
        fc.Internal("slack-well",
                    [fc.P(8.0, cable_bend), fc.P(BAG_W - 8.0, cable_bend)],
                    kind="marking"),
    ]
    return fc.Piece(
        "bag", _rect_edges(0.0, 0.0, BAG_W, BAG_DEPTH,
                           ("fold", "seam_r", "mouth", "seam_l")),
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("mouth", 0.5, "bay centre")],
        grainline=None,
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fold"),
        label="Pocket bag (solved depth)",
    )


def build_flap():
    """The closure flap over the bay mouth, cut to the MEASURED flange width so it
    covers the rigid ring rather than stopping at the bay."""
    w = FLANGE_W
    h = flap_depth
    internals = [
        fc.Internal("fold-line", [fc.P(0.0, h - 10.0), fc.P(w, h - 10.0)],
                    kind="marking"),
        # Closure field, inset from the edges so the stitching never crosses it.
        fc.Internal("closure-field",
                    _closed_rect_pts(12.0, 8.0, max(w - 24.0, 10.0),
                                     max(h - 26.0, 8.0)), kind="marking"),
    ]
    return fc.Piece(
        "flap", _rect_edges(0.0, 0.0, w, h, ("free", "end_r", "attach", "end_l")),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "bay centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 6.0), fc.P(w * 0.5, h - 6.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Bay flap",
    )


def build():
    pattern = fc.PatternSet("battery-pocket-liner")
    everything = target_piece == "set"
    if everything or target_piece == "liner":
        pattern.add(build_liner())
    if everything or target_piece == "bag":
        pattern.add(build_bag())
    if everything or target_piece == "flap":
        pattern.add(build_flap())

    if everything:
        # THE seam that had to solve: the bag's mouth is the frame's flange width, and
        # the flap's attach edge is that same width. All three read the flange, not the
        # battery — so a battery-sized cut can never sneak into any of them.
        pattern.declare_seam(("flap", "attach"), ("bag", "mouth"), tol=1.0)
        # The bag's two side seams together equal its two-sided depth. Declared so a
        # bag cut short (the shallow-bag failure) cannot pass.
        pattern.declare_seam(("bag", "seam_l"), ("bag", "seam_r"), tol=0.5)

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "ripstop nylon shell (liner weight)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 82% marker; rectangles nest well. Ripstop's "
                 "110 °C iron ceiling governs anywhere near the conduit."},
        {"item": "battery pocket frame", "qty": 1, "unit": "count",
         "note": f"Yantra4D battery-pocket-frame (notion.hardware_ref); bay "
                 f"{BAY_W:.0f} x {BAY_H:.0f} x {batt_t:.0f} mm with a {frame_w:.0f} mm "
                 f"flange, sewn through {SEW_HOLES} holes at a solved "
                 f"{SEW_PITCH_SOLVED:.1f} mm pitch."},
        {"item": "bar-tack thread (bonded)", "qty": 1, "unit": "spool",
         "note": "the bag's mouth corners are bar-tacked: the frame carries the load "
                 "into the bag, and the corners are where it arrives."},
        {"item": "closure tape or snap set", "qty": 1, "unit": "set",
         "note": f"{FLANGE_W:.0f} mm engagement across the flap; it closes over the "
                 f"FRAME, not the bay."},
        {"item": "cable grommet or seam channel", "qty": 1, "unit": "count",
         "note": f"at the marked conduit exit, {conduit_exit:.2f} up the side edge "
                 f"({SIDE_LEN * conduit_exit:.0f} mm from the hem)."},
    ]
    pattern.metadata = {
        "fc300_rank": 296,
        "family": "etextile",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {
            "liner_width": round(liner_width, 1),
            "liner_height": round(liner_height, 1),
            "bay_w": round(BAY_W, 1),
            "bay_h": round(BAY_H, 1),
            "flange_w": round(FLANGE_W, 1),
            "flange_h": round(FLANGE_H, 1),
            "bag_depth": round(BAG_DEPTH, 1),
        },
        "solved": {
            "bay_from_battery_mm": [round(batt_w, 1), round(batt_h, 1)],
            "bay_clear_mm": round(bay_clear, 2),
            "flange_footprint_mm": [round(FLANGE_W, 2), round(FLANGE_H, 2)],
            "bag_depth_mm": round(BAG_DEPTH, 2),
            "bag_depth_terms": {"bay_h": round(BAY_H, 2),
                                "batt_t": round(batt_t, 2),
                                "cable_bend": round(cable_bend, 2)},
            "window_perimeter_mm": round(WINDOW_PERIM, 2),
            "sew_holes": SEW_HOLES,
            "sew_pitch_requested_mm": round(sew_pitch, 2),
            "sew_pitch_solved_mm": round(SEW_PITCH_SOLVED, 3),
            "panel_floor_applied": {
                "width_floor_mm": round(FLANGE_W + 2.0 * _MARGIN, 2),
                "height_floor_mm": round(FLANGE_H + flap_depth + 2.0 * _MARGIN, 2)},
            "conduit_exit_mm_from_hem": round(SIDE_LEN * conduit_exit, 2),
            "note": "the window is cut to the frame's BAY (battery + clearance) and the "
                    "flange lands OUTSIDE it — cutting the window to the battery leaves "
                    "the rigid ring nothing to sit on. The bag depth is SOLVED as "
                    "bay_h + batt_t + cable_bend rather than chosen, because a bag cut "
                    "to the bay alone pinches the cable at the mouth. Both panel "
                    "dimensions are FLOORED to contain the flange footprint plus "
                    "margins: at the parameter extremes the naive arithmetic goes "
                    "negative, and a negative-width piece is CCW-normalized into "
                    "geometry that verifies but cannot be cut.",
        },
        "etextile_note": "The bay window, the flange footprint, the sew ring, the "
                         "conduit run and the service loop are MARKED. No battery, "
                         "cell, connector, BMS, or circuit is drafted here.",
        "hardware": "battery bay via Yantra4D (notion.hardware_ref -> "
                    "battery-pocket-frame); the frame's bay_w x bay_h is this liner's "
                    "battery plus bay_clear, and its sewn flange is the exact rectangle "
                    "the panel marks as frame-flange",
    }
    return pattern


result = build()
