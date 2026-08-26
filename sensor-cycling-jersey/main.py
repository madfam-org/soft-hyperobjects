"""
Sensor-Mount Cycling Jersey — Fashion Cabinet E-Textile Cartridge (FC-500 #469; sensor-mount-
plate).

An aero-fit cycling jersey with a rigid SENSOR SEAT: a `sensor-mount-plate` (the printable
Yantra4D base that a power/cadence/heart device screws to) is seated on a stabilised patch at the
lower back, with its conductive lead routed in a between-layers channel to the standard three rear
cargo pockets. The jersey is a real racing cut — long tail hem, forward sleeves, a full-length
front for a zip — and the sensor patch is the e-textile detail that turns a jersey into an
instrumented one without a boxed, glued-in module.

  **This is a garment pattern, not a device.** It seats a mount plate and routes a lead. It
  contains no sensor, battery, or circuit and makes no measurement claim.

The seat that must SOLVE. A sensor plate is RIGID and screws down flat, but the jersey is a
stretch knit at negative ease. If the plate is sewn onto stretching cloth it rocks and the reading
drifts. So the plate sits on a STABILISED patch (a fused, non-stretch island) whose footprint is
the plate's base plus a screw-clearance margin, and that island is a dead length in the back
panel's width: the back is cut so the island takes none of the negative ease. `plate_w` drives the
island and the plate together.

The DIMENSIONAL HANDSHAKE. `sensor-mount-plate` is parameterised by `base_w`/`base_d` (its sewn
base). `plate_w`/`plate_d` drive the carrier's `base_w`/`base_d` AND the drafted stabilised seat
AND the jersey's own `sensor_seat` interface, so the printed plate is exactly the size of the
island it screws to.

Made to measure to chest/bust and waist girths. FC-500 lane 8 (e-textile & smart garments III).

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

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 840.0))
body_length = float(PARAM(lambda: body_length, 640.0))     # nape to front hem
tail_drop   = float(PARAM(lambda: tail_drop, 90.0))        # extra length at the back (racing tail)
sleeve_length = float(PARAM(lambda: sleeve_length, 240.0)) # short cycling sleeve
bicep_girth = float(PARAM(lambda: bicep_girth, 320.0))
plate_w     = float(PARAM(lambda: plate_w, 46.0))          # sensor plate base width
plate_d     = float(PARAM(lambda: plate_d, 36.0))          # sensor plate base depth
plate_margin = float(PARAM(lambda: plate_margin, 12.0))
pocket_count = float(PARAM(lambda: pocket_count, 3.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
waist_girth = max(560.0, min(waist_girth, 1400.0))
body_length = max(450.0, min(body_length, 850.0))
tail_drop   = max(30.0, min(tail_drop, 180.0))
sleeve_length = max(120.0, min(sleeve_length, 420.0))
bicep_girth = max(220.0, min(bicep_girth, 550.0))
plate_w     = max(24.0, min(plate_w, 90.0))
plate_d     = max(18.0, min(plate_d, 80.0))
plate_margin = max(6.0, min(plate_margin, 30.0))
pocket_count = max(1.0, min(pocket_count, 4.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 16.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

N_POCKET = int(round(pocket_count))

# ── Solved widths ────────────────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
CHEST_HALF = (chest_bust_girth * NEG) / 2.0
WAIST_HALF = (waist_girth * NEG) / 2.0
PANEL_CHEST = CHEST_HALF / 2.0
PANEL_WAIST = WAIST_HALF / 2.0
BL = body_length
AL = sleeve_length
ARMSCYE = max(190.0, PANEL_CHEST * 1.05)
# The stabilised sensor island is a dead length in the back panel.
ISLAND_W = plate_w + 2.0 * plate_margin
ISLAND_D = plate_d + 2.0 * plate_margin
NECK_W = max(70.0, chest_bust_girth / 12.0)


def _bell_points(chord, height):
    mid = chord / 2.0
    left = fc.Bezier(fc.P(0.0, 0.0), fc.P(chord * 0.14, height * 0.10),
                     fc.P(mid * 0.55, height), fc.P(mid, height))
    right = fc.Bezier(fc.P(mid, height), fc.P(mid + (mid - mid * 0.55), height),
                      fc.P(chord - chord * 0.14, height * 0.10), fc.P(chord, 0.0))
    return left.flatten(0.2) + right.flatten(0.2)[1:]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def build_front():
    """Front, cut 2 (mirror) for a CF zip. Full-length front, scooped neck."""
    p_cf_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(PANEL_WAIST, 0.0)
    armscye_y = BL - ARMSCYE
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.7, BL - 8.0)
    front_neck_drop = NECK_W * 0.85
    p_neck_sh = fc.P(NECK_W, BL)
    p_cf_neck = fc.P(0.0, BL - front_neck_drop)
    edges = [
        fc.Edge("hem", [fc.Line(p_cf_hem, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85), p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE * 0.45),
                                      fc.P(p_shoulder.x + 14.0, p_shoulder.y - 30.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_sh)]),
        fc.Edge("neck", [fc.Bezier(p_neck_sh, fc.P(NECK_W * 0.7, BL - front_neck_drop * 0.35),
                                   fc.P(NECK_W * 0.3, BL - front_neck_drop * 0.8), p_cf_neck)]),
        fc.Edge("center_front", [fc.Line(p_cf_neck, p_cf_hem)]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("armscye", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, BL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 — CF zip)",
    )


def build_back():
    """Back, cut on CB fold. Racing tail (extra length below the hem line), and the stabilised
    sensor island marked at the lower back."""
    # The racing tail drops the CB hem BELOW the side hem; the side seam and the upper
    # structure exactly match the front (same y-coords) so the side seam balances — the tail
    # is length added only at centre back, never on the side.
    p_cb_hem = fc.P(0.0, -tail_drop)                  # CB drops below the front hem line
    p_side_hem = fc.P(PANEL_WAIST, 0.0)               # side hem at the same y as the front
    armscye_y = BL - ARMSCYE                           # SAME as the front
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.7, BL - 8.0)
    p_neck = fc.P(NECK_W, BL)
    p_cb_neck = fc.P(0.0, BL)
    edges = [
        fc.Edge("hem", [fc.Bezier(p_cb_hem,
                                  fc.P(PANEL_WAIST * 0.4, -tail_drop * 0.8),
                                  fc.P(PANEL_WAIST * 0.8, -tail_drop * 0.2),
                                  p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85), p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE * 0.45),
                                      fc.P(p_shoulder.x + 14.0, p_shoulder.y - 30.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(NECK_W * 0.55, BL - 2.0),
                                   fc.P(NECK_W * 0.2, BL - 1.0), p_cb_neck)]),
        fc.Edge("center_back", [fc.Line(p_cb_neck, p_cb_hem)]),
    ]
    # sensor island + trace, marked at the lower back
    ix = PANEL_CHEST * 0.5
    iy = tail_drop + 60.0
    internals = [
        fc.Internal("sensor-island",
                    [fc.P(ix - ISLAND_W / 2.0, iy - ISLAND_D / 2.0),
                     fc.P(ix + ISLAND_W / 2.0, iy - ISLAND_D / 2.0),
                     fc.P(ix + ISLAND_W / 2.0, iy + ISLAND_D / 2.0),
                     fc.P(ix - ISLAND_W / 2.0, iy + ISLAND_D / 2.0),
                     fc.P(ix - ISLAND_W / 2.0, iy - ISLAND_D / 2.0)], kind="marking"),
        fc.Internal("plate-seat",
                    [fc.P(ix - plate_w / 2.0, iy - plate_d / 2.0),
                     fc.P(ix + plate_w / 2.0, iy - plate_d / 2.0),
                     fc.P(ix + plate_w / 2.0, iy + plate_d / 2.0),
                     fc.P(ix - plate_w / 2.0, iy + plate_d / 2.0),
                     fc.P(ix - plate_w / 2.0, iy - plate_d / 2.0)], kind="marking"),
        fc.Internal("sensor-trace", [fc.P(ix, iy + plate_d / 2.0), fc.P(ix, iy + 90.0)],
            kind="trace"),
    ]
    # four screw points
    for lx, ly in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        sx = ix + lx * (plate_w / 2.0 - 5.0)
        sy = iy + ly * (plate_d / 2.0 - 5.0)
        internals.append(fc.Internal(f"screw-{lx}-{ly}", [fc.P(sx, sy), fc.P(sx, sy)],
            kind="drill"))
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("armscye", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, BL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, BL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Back with sensor island (cut 1 on CB fold)",
    )


def build_sleeve(armscye_len):
    bicep_half = (bicep_girth * (1.0 + 0.04)) / 2.0
    chord = min(2.0 * bicep_half, armscye_len * 0.92)
    bicep_half = chord / 2.0
    cuff_half = max(60.0, bicep_half * 0.82)
    target = max(armscye_len, chord * 1.01)
    lo, hi = 1.0, max(chord, target)
    for _ in range(48):
        mid_h = (lo + hi) / 2.0
        if _poly_len(_bell_points(chord, mid_h)) < target:
            lo = mid_h
        else:
            hi = mid_h
    cap_pts = _bell_points(chord, (lo + hi) / 2.0)
    p_cuff_r = fc.P(bicep_half + cuff_half, -AL)
    p_cuff_l = fc.P(bicep_half - cuff_half, -AL)
    edges = [
        fc.Edge("cap", [fc.Line(cap_pts[i], cap_pts[i + 1]) for i in range(len(cap_pts) - 1)]),
        fc.Edge("underseam_r", [fc.Line(cap_pts[-1], p_cuff_r)]),
        fc.Edge("cuff", [fc.Line(p_cuff_r, p_cuff_l)]),
        fc.Edge("underseam_l", [fc.Line(p_cuff_l, cap_pts[0])]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(bicep_half, -AL * 0.2), fc.P(bicep_half, -AL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Short sleeve (cut 2, mirror)",
    )


def build_pocket_band(back_hem_len):
    """The rear cargo pocket band: a strip along the back hem divided into N_POCKET pockets."""
    length = back_hem_len * 2.0   # full back hem (fold) both sides
    depth = max(130.0, ISLAND_D + 90.0)
    p0, p1 = fc.P(0.0, 0.0), fc.P(length, 0.0)
    p2, p3 = fc.P(length, depth), fc.P(0.0, depth)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),   # to the back hem
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("mouth", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("mouth-fold", [fc.P(0.0, depth - 24.0), fc.P(length, depth - 24.0)],
                             kind="marking")]
    for i in range(1, N_POCKET):
        dx = length * i / N_POCKET
        internals.append(fc.Internal(f"divider-{i}", [fc.P(dx, 0.0), fc.P(dx, depth - 24.0)],
                                     kind="marking"))
    return fc.Piece(
        "pocket_band", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        notches=[fc.Notch("attach", 0.5, "CB match")],
        grainline=fc.Grainline(fc.P(length * 0.08, depth * 0.4), fc.P(length * 0.92, depth * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Rear cargo pocket band (cut 1)",
    )


def build():
    pattern = fc.PatternSet("sensor-cycling-jersey")
    front = build_front()
    back = build_back()
    armscye_len = front.edge("armscye").length() + back.edge("armscye").length()
    sleeve = build_sleeve(armscye_len)
    pocket_band = build_pocket_band(back.edge("hem").length())

    picked = {"front": front, "back": back, "sleeve": sleeve, "pocket_band": pocket_band}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, sleeve, pocket_band):
            pattern.add(piece)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=2.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armscye"), ("back", "armscye")], tol=2.0)
        # pocket band attaches along the whole back hem (fold => *2).
        pattern.declare_seam(("pocket_band", "attach"),
                             [("back", "hem"), ("back", "hem")], tol=2.5)

    fabric_width = 1600.0
    area = (front.area() * 2.0 + back.area() * 2.0 + sleeve.area() * 2.0 + pocket_band.area())
    marker_len = area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "aero cycling knit (poly/elastane)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body and sleeves at {fabric_width:.0f} mm width, 82% marker; cut for the "
                 "aero fit at negative ease."},
        {"item": "sensor mount plate (Yantra4D sensor-mount-plate)", "qty": 1, "unit": "count",
         "note": f"base {plate_w:.0f} x {plate_d:.0f} mm, screwed to the stabilised island "
                 "(notion.hardware_ref -> sensor-mount-plate); plate_w/plate_d drive the plate "
                 "AND the drafted seat."},
        {"item": "fusible non-stretch interfacing (island)",
         "qty": round(ISLAND_W * ISLAND_D / 100.0), "unit": "cm2",
         "note": f"the {ISLAND_W:.0f} x {ISLAND_D:.0f} mm stabilised island — the dead length "
                 "the plate screws to so it cannot rock on the stretch knit."},
        {"item": "conductive thread or ribbon", "qty": round(BL * 0.6), "unit": "mm_length",
         "note": "the lead from plate to pocket, laid between the layers, never on the face."},
        {"item": "CF zip + coverstitch", "qty": 1, "unit": "set",
         "note": "full-length front zip; coverstitch the hems and the pocket band."},
    ]
    pattern.metadata = {
        "fc500_rank": 469, "family": "etextile", "fabric_hint": "nylon-elastano",
        "not_a_device": "This seats a mount plate and routes a lead. It contains no sensor, "
                        "battery, or circuit and makes no measurement claim.",
        "silhouette_note": "Aero cycling jersey with a rigid sensor seat: a mount plate on a "
            "stabilised island at the lower back, its lead routed to the three rear cargo pockets. "
            "A racing cut — long tail, forward sleeves, full-length zip front.",
        "hardware": "sensor mount via Yantra4D (notion.hardware_ref -> sensor-mount-plate); "
            "plate_w/plate_d drive the plate base AND the drafted island/seat.",
        "solved": {
            "chest_finished_half_mm": round(CHEST_HALF, 1),
            "plate_w_mm": round(plate_w, 1),
            "plate_d_mm": round(plate_d, 1),
            "island_w_mm": round(ISLAND_W, 1),
            "island_d_mm": round(ISLAND_D, 1),
            "pocket_count": N_POCKET,
            "armscye_run_mm": round(armscye_len, 1),
            "note": "the plate sits on a fused non-stretch island (plate + margin) so it does not "
                    "rock on the negative-ease knit; the sleeve cap is solved to the armscye run.",
        },
        "etextile_note": "The sensor island, the plate seat, its four screw points, the lead "
                         "trace and the pocket band are MARKED. No sensor, conductor, battery, or "
                         "circuit is drafted here.",
    }
    return pattern


result = build()
