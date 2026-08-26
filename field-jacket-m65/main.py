"""
Field Jacket (M-65 pattern) — Fashion Cabinet Garment Cartridge
(FC-400 #310, workwear_uniforms, T3).

The M-65 field jacket: a snap-over-zip front, four bellows cargo pockets with
snap-down flaps, epaulettes, a stand collar with a concealed hood, and a
drawcord waist. The garment's signature is the row of snaps down the storm flap
and the snaps on the pocket flaps, and the number that has to be right is the
snap PITCH — a drifted snap column leaves the last snap in the hem or off the
flap edge.

Three things are solved by measurement rather than by formula:

  1. THE FRONT SNAP RUN IS SOLVED ACROSS THE MEASURED STORM FLAP. The storm flap
     covers the zip; its snaps are fitted to whole intervals across the MEASURED
     flap length between two end clearances and the pitch RECOMPUTED, so the top
     snap sits under the collar and the bottom clears the hem drawcord channel.

  2. THE POCKET FLAP SNAPS ARE CENTRED ON THE MEASURED FLAP. Each cargo pocket's
     flap carries two snaps, placed by MEASURING the flap width and stepping in
     from each end — never at a fixed offset that walks off a narrow flap or
     bunches on a wide one.

  3. THE BELLOWS POCKET IS CLAMPED AGAINST THE FRONT IT SITS ON. A cargo pocket
     wider than the front panel folds over the placket, and — because the kernel
     CCW-normalizes an inverted outline and area() takes an absolute value — such
     a piece renders and passes verify() looking healthy. The pocket width and
     the snap count are clamped and reported.

MILITARY/WORKWEAR CONVENTIONS: 6 mm topstitch (denser than denim); felled seams;
hard goods via Yantra4D. The SNAP-FIT SOLID is Yantra4D territory (`snap-fit`;
see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|storm_flap|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1080.0))
back_width = float(PARAM(lambda: back_width, 470.0))
body_length = float(PARAM(lambda: body_length, 720.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 660.0))
neck_width = float(PARAM(lambda: neck_width, 180.0))
collar_stand = float(PARAM(lambda: collar_stand, 65.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 45.0))
front_snaps = float(PARAM(lambda: front_snaps, 6.0))
snap_dia = float(PARAM(lambda: snap_dia, 15.0))            # snap-fit outer diameter
pocket_width = float(PARAM(lambda: pocket_width, 200.0))
pocket_bellows = float(PARAM(lambda: pocket_bellows, 25.0))  # bellows depth
wear_ease = float(PARAM(lambda: wear_ease, 220.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(880.0, min(chest_girth, 1500.0))
back_width = max(380.0, min(back_width, 560.0))
body_length = max(560.0, min(body_length, 860.0))
sleeve_length = max(520.0, min(sleeve_length, 780.0))
neck_width = max(150.0, min(neck_width, 240.0))
collar_stand = max(45.0, min(collar_stand, 95.0))
shoulder_slope = max(25.0, min(shoulder_slope, 70.0))
front_snaps = max(4.0, min(round(front_snaps), 9.0))
snap_dia = max(11.0, min(snap_dia, 22.0))
pocket_width = max(130.0, min(pocket_width, 320.0))
pocket_bellows = max(10.0, min(pocket_bellows, 45.0))
wear_ease = max(120.0, min(wear_ease, 340.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(18.0, min(hem_allowance, 45.0))

TOPSTITCH = 6.0
N_FRONT_SNAPS = int(front_snaps)

QUARTER_CHEST = (chest_girth + wear_ease) / 4.0
HALF_NECK = neck_width / 2.0
HALF_BACK = back_width / 2.0
NECK_DROP_F = max(60.0, HALF_NECK * 0.9)
NECK_DROP_B = max(20.0, HALF_NECK * 0.28)

# The storm flap runs the placket length; its snaps are solved across it.
FLAP_LEN = body_length - NECK_DROP_B
SNAP_END_CLEAR = max(snap_dia * 1.6, 50.0)
SNAP_RUN = max(snap_dia * 2.0, FLAP_LEN - 2.0 * SNAP_END_CLEAR)
N_INTERVALS = max(1, N_FRONT_SNAPS - 1)
SNAP_PITCH = SNAP_RUN / N_INTERVALS
STORM_FLAP_W = max(snap_dia * 2.4, 45.0)

# The cargo pocket clamped against the front.
_POCKET_W_RAW = pocket_width
POCKET_W = max(100.0, min(_POCKET_W_RAW, QUARTER_CHEST - 2.0 * seam_allowance))
POCKET_H = max(140.0, POCKET_W * 1.15)
FLAP_H = max(50.0, POCKET_W * 0.30)


def _snap(label, x, y):
    a = max(3.0, snap_dia * 0.30)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def build_front():
    hw = QUARTER_CHEST
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - NECK_DROP_B - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length - NECK_DROP_B)
    p_neck_cf = fc.P(0.0, body_length - NECK_DROP_B - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - NECK_DROP_B - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cf, bulge=0.28, side=1.0)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [
        fc.Internal("drawcord waist channel",
                    [fc.P(TOPSTITCH, body_length * 0.42),
                     fc.P(hw - TOPSTITCH, body_length * 0.42)], kind="marking"),
        fc.Internal("epaulette placement",
                    [fc.P(HALF_BACK - 60.0, body_length - NECK_DROP_B - shoulder_slope),
                     fc.P(HALF_NECK + 12.0, body_length - NECK_DROP_B)],
                    kind="marking"),
    ]
    # Two cargo pockets per front (chest + hip), clamped.
    for py, tag in ((body_length - QUARTER_CHEST * 0.9, "chest"),
                    (POCKET_H + hem_allowance + 30.0, "hip")):
        px = hw * 0.34
        internals.append(fc.Internal(
            f"{tag} cargo pocket placement",
            [fc.P(px, py), fc.P(px + POCKET_W, py),
             fc.P(px + POCKET_W, py - POCKET_H), fc.P(px, py - POCKET_H),
             fc.P(px, py)], kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf": hem_allowance},
        notches=[fc.Notch("armscye", 0.0, "underarm"),
                 fc.Notch("shoulder", 0.5, "shoulder mid"),
                 fc.Notch("side", 0.42, "drawcord waist")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, mirrored)",
    )


def build_back():
    hw = QUARTER_CHEST
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hw, 0.0)
    p_armhole = fc.P(hw, body_length - QUARTER_CHEST * 0.5)
    p_shoulder_pt = fc.P(HALF_BACK, body_length - shoulder_slope)
    p_neck_pt = fc.P(HALF_NECK, body_length)
    p_neck_cb = fc.P(0.0, body_length - NECK_DROP_B)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_armhole)]),
        fc.Edge("armscye", [fc.Bezier(
            p_armhole, fc.P(hw - 10.0, body_length - QUARTER_CHEST * 0.24),
            fc.P(HALF_BACK + 12.0, body_length - shoulder_slope + 20.0),
            p_shoulder_pt)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_pt, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_cb, bulge=0.16, side=1.0)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cb_fold": 0.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder mid"),
                 fc.Notch("armscye", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(hw * 0.4, 30.0), fc.P(hw * 0.4, body_length - 30.0)),
        internals=[
            fc.Internal("drawcord waist channel",
                        [fc.P(0.0, body_length * 0.42), fc.P(hw, body_length * 0.42)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Back (cut on fold)",
    )


_FRONT = build_front()
_BACK = build_back()
ARMSCYE_RUN = _FRONT.edge("armscye").length(0.05) + _BACK.edge("armscye").length(0.05)


def build_sleeve():
    sw = QUARTER_CHEST * 0.94
    cap_h = QUARTER_CHEST * 0.30
    ln = sleeve_length
    cuff_w = sw * 0.62
    p_ul = fc.P(0.0, 0.0)
    p_ur = fc.P(sw, 0.0)
    edges = [
        fc.Edge("cap_r", [fc.Bezier(
            p_ur, fc.P(sw * 0.86, cap_h * 0.75),
            fc.P(sw * 0.60, cap_h), fc.P(sw / 2.0, cap_h))]),
        fc.Edge("cap_l", [fc.Bezier(
            fc.P(sw / 2.0, cap_h), fc.P(sw * 0.40, cap_h),
            fc.P(sw * 0.14, cap_h * 0.75), p_ul)]),
        fc.Edge("seam_l", [fc.Line(p_ul, fc.P((sw - cuff_w) / 2.0, -ln))]),
        fc.Edge("cuff", [fc.Line(fc.P((sw - cuff_w) / 2.0, -ln),
                                 fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln))]),
        fc.Edge("seam_r", [fc.Line(fc.P((sw - cuff_w) / 2.0 + cuff_w, -ln), p_ur)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance},
        notches=[fc.Notch("cap_r", 1.0, "shoulder point"),
                 fc.Notch("cap_l", 0.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(sw / 2.0, -ln * 0.1), fc.P(sw / 2.0, cap_h * 0.9)),
        internals=[
            fc.Internal("adjust-tab snap",
                        [fc.P((sw - cuff_w) / 2.0 + 20.0, -ln + FLAP_H * 0.5)],
                        kind="drill"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2, mirrored)",
    )


_SLEEVE = build_sleeve()
CAP_RUN = _SLEEVE.edge("cap_r").length(0.05) + _SLEEVE.edge("cap_l").length(0.05)
CAP_EASE = CAP_RUN - ARMSCYE_RUN


def build_collar():
    neck_run = (_FRONT.edge("neck").length(0.05) * 2.0
                + _BACK.edge("neck").length(0.05))
    ln = neck_run / 2.0
    depth = collar_stand
    edges = [
        fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, depth))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, depth), fc.P(ln, depth))]),
        fc.Edge("cf_end", [fc.Line(fc.P(ln, depth), fc.P(ln, 0.0))]),
        fc.Edge("neck_edge", [fc.curve_through(
            fc.P(ln, 0.0), fc.P(0.0, 0.0), bulge=0.10, side=1.0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, depth * 0.5), fc.P(ln * 0.9, depth * 0.5)),
        internals=[
            fc.Internal("hood zip channel",
                        [fc.P(TOPSTITCH, depth - TOPSTITCH),
                         fc.P(ln - TOPSTITCH, depth - TOPSTITCH)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb_fold"),
        label="Stand collar with hood zip (cut 2, on fold)",
    )


def build_storm_flap():
    """The snap storm flap over the zip, cut 1. Snaps solved along it."""
    w = STORM_FLAP_W
    h = FLAP_LEN
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("outer", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    internals = [
        fc.Internal("flap topstitch",
                    [fc.P(w - TOPSTITCH, TOPSTITCH), fc.P(w - TOPSTITCH, h - TOPSTITCH)],
                    kind="trace"),
    ]
    y0 = SNAP_END_CLEAR
    for i in range(N_FRONT_SNAPS):
        internals.append(_snap(f"front snap-{i + 1}", w * 0.5, y0 + SNAP_PITCH * i))
    return fc.Piece(
        "storm_flap", edges,
        seam_allowance=seam_allowance,
        allowances={"outer": hem_allowance * 0.5},
        notches=[fc.Notch("attach", 0.5, "CF attach")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Snap storm flap (cut 1)",
    )


def build_pocket():
    """Bellows cargo pocket with snap flap, cut 4. Clamped against the front."""
    w = POCKET_W
    h = POCKET_H
    fh = FLAP_H
    edges = [
        # The flap sits above the pocket; the whole cut piece is pocket + flap.
        fc.Edge("flap_top", [fc.Line(fc.P(0.0, h + fh), fc.P(w, h + fh))]),
        fc.Edge("right", [fc.Line(fc.P(w, h + fh), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h + fh))]),
    ]
    internals = [
        fc.Internal("flap fold line", [fc.P(0.0, h), fc.P(w, h)], kind="marking"),
        fc.Internal("bellows fold L", [fc.P(pocket_bellows, 0.0),
                                       fc.P(pocket_bellows, h)], kind="marking"),
        fc.Internal("bellows fold R", [fc.P(w - pocket_bellows, 0.0),
                                       fc.P(w - pocket_bellows, h)], kind="marking"),
        # The two flap snaps, placed by MEASURING the flap width and stepping in.
        _snap("flap snap L", max(snap_dia, w * 0.28), h + fh * 0.45),
        _snap("flap snap R", min(w - snap_dia, w * 0.72), h + fh * 0.45),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"flap_top": hem_allowance * 0.4},
        notches=[fc.Notch("bottom", 0.5, "centre"),
                 fc.Notch("left", h / (h + fh), "flap fold")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=4),
        label="Bellows cargo pocket + flap (cut 4)",
    )


def build():
    pattern = fc.PatternSet("field-jacket-m65")
    everything = target_piece == "set"
    want = {
        "front": everything or target_piece == "front",
        "back": everything or target_piece == "back",
        "sleeve": everything or target_piece == "sleeve",
        "collar": everything or target_piece == "collar",
        "storm_flap": everything or target_piece == "storm_flap",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["front"]:
        pattern.add(build_front())
    if want["back"]:
        pattern.add(build_back())
    if want["sleeve"]:
        pattern.add(build_sleeve())
    if want["collar"]:
        pattern.add(build_collar())
    if want["storm_flap"]:
        pattern.add(build_storm_flap())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["front"] and want["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    if want["sleeve"] and want["front"] and want["back"]:
        pattern.declare_seam([("sleeve", "cap_r"), ("sleeve", "cap_l")],
                             [("front", "armscye"), ("back", "armscye")],
                             tol=2.5, ease=CAP_EASE)
    if want["storm_flap"] and want["front"]:
        pattern.declare_seam(("storm_flap", "attach"), ("front", "cf"),
                             tol=1.5, ease=FLAP_LEN - _FRONT.edge("cf").length(0.05))

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton sateen, 9 oz (NyCo-style, wind-resistant)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a tight sateen "
                 f"weave for wind resistance — the M-65's shell character."},
        {"item": "snap-fit fastener", "qty": N_FRONT_SNAPS + 8, "unit": "set",
         "note": f"Yantra4D snap-fit (notion.hardware_ref) at {snap_dia:.0f} mm: "
                 f"{N_FRONT_SNAPS} on the storm flap at a SOLVED pitch of "
                 f"{SNAP_PITCH:.1f} mm, plus 2 on each of four pocket flaps."},
        {"item": "front zipper (under the storm flap)", "qty": 1, "unit": "piece",
         "note": "the primary closure is a zip; the snap storm flap covers it. "
                 "The zip is a companion hard good, not the bridged one (one solid "
                 "per notion — the snaps are the finding here)."},
        {"item": "heavy topstitch thread + needle 90/14", "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm; felled seams; drawcord "
                 f"channels at the waist and hem."},
    ]
    pattern.metadata = {
        "fc400_rank": 310,
        "family": "workwear_uniforms",
        "tier": 3,
        "fabric_hint": "sateen-cotton",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "body_length": round(body_length, 1),
            "collar_stand": round(collar_stand, 1),
            "storm_flap_length": round(FLAP_LEN, 1),
            "pocket_width": round(POCKET_W, 1),
        },
        "solved": {
            "front_snap_count": N_FRONT_SNAPS,
            "front_snap_pitch_solved_mm": round(SNAP_PITCH, 2),
            "front_snap_run_mm": round(SNAP_RUN, 2),
            "snap_end_clear_mm": round(SNAP_END_CLEAR, 2),
            "armscye_run_measured_mm": round(ARMSCYE_RUN, 2),
            "cap_ease_mm": round(CAP_EASE, 2),
            "pocket_width_requested_mm": round(_POCKET_W_RAW, 2),
            "pocket_width_clamped_mm": round(POCKET_W, 2),
            "pocket_width_was_clamped": bool(abs(POCKET_W - _POCKET_W_RAW) > 0.01),
            "note": "the storm-flap snaps are fitted to whole intervals across the "
                    "MEASURED flap between two end clearances and the pitch "
                    "recomputed, so the top snap sits under the collar and the "
                    "bottom clears the hem drawcord. The pocket flap snaps are "
                    "placed by measuring each flap and stepping in. The bellows "
                    "cargo pockets are clamped against the front, because an "
                    "inverted piece is CCW-normalized by the kernel and passes "
                    "verify() looking healthy.",
        },
        "topstitch": f"twin-needle at {TOPSTITCH:.0f} mm (denser than denim); felled "
                     f"seams",
        "hardware": "snap-fit fasteners via Yantra4D (notion.hardware_ref -> "
                    "snap-fit); the solid's bore_dia — the parameter driving the "
                    "socket the stud seats into — is fed from this garment's "
                    "snap_dia, which also sizes and spaces the whole snap column. "
                    "The front zip is a companion hard good, marked and counted.",
    }
    return pattern


result = build()
