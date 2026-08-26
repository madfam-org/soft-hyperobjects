"""
Cable-Conduit Harness Tee — Fashion Cabinet E-Textile Cartridge (FC-500 #472; seam-conduit-clip).

A wearable cable harness in the form of a tee: conductive/data cable bundles run ALONG the seams
(the strongest, least-flexing lines of a garment), held off the skin and away from the wash in
Yantra4D `seam-conduit-clip` bundles clipped into the seam allowances, converging at a junction
pocket. It is the garment that a wearable-electronics maker actually needs and never has: a base
tee whose seams are cable races, so an LED costume, a haptic suit, or a sensor rig routes its
wiring in the seams instead of safety-pinning it to the inside.

  **This is a garment pattern, not a wiring loom.** It routes and clips cable bundles along the
  seams. It contains no cable, connector, or circuit and makes no electrical claim.

The clip-count SOLVE. A conduit clip holds the bundle at intervals; too few and the bundle sags
off the seam, too many and the seam stiffens. The clip count on each seam is solved from the
seam's MEASURED length and the clip pitch:

    clips = round(seam_length / clip_pitch)

so a longer seam gets more clips and the spacing stays constant, whatever the body size. The clips
are placed by fraction along each seam, drafted, not guessed.

The DIMENSIONAL HANDSHAKE. `seam-conduit-clip`'s sewn `seam_tabs` flange is driven by `tab_w`. The
garment's `tab_w` drives the carrier's `tab_w` AND the drafted clip footprint AND the tee's own
`seam_conduit` interface, so the printed clip is exactly as wide as the tab it sews into.

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

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 980.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
body_length = float(PARAM(lambda: body_length, 680.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 220.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
tab_w = float(PARAM(lambda: tab_w, 16.0))                 # conduit-clip tab width
clip_pitch = float(PARAM(lambda: clip_pitch, 70.0))      # spacing of clips along a seam
bundle_dia = float(PARAM(lambda: bundle_dia, 8.0))       # cable bundle diameter
junction_pocket = float(PARAM(lambda: junction_pocket, 110.0))
ease_pct = float(PARAM(lambda: ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
waist_girth = max(560.0, min(waist_girth, 1400.0))
body_length = max(450.0, min(body_length, 900.0))
sleeve_length = max(120.0, min(sleeve_length, 500.0))
bicep_girth = max(220.0, min(bicep_girth, 550.0))
tab_w = max(8.0, min(tab_w, 34.0))
clip_pitch = max(30.0, min(clip_pitch, 140.0))
bundle_dia = max(3.0, min(bundle_dia, 24.0))
junction_pocket = max(70.0, min(junction_pocket, 180.0))
ease_pct = max(0.0, min(ease_pct, 18.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# the seam allowance must hold the clip tab plus the bundle
seam_allowance = max(seam_allowance, tab_w + bundle_dia * 0.5 + 4.0)

# ── Solved widths ────────────────────────────────────────────────────────────
E = 1.0 + ease_pct / 100.0
CHEST_HALF = (chest_bust_girth * E) / 2.0
WAIST_HALF = (waist_girth * E) / 2.0
PANEL_CHEST = CHEST_HALF / 2.0
PANEL_WAIST = WAIST_HALF / 2.0
BL = body_length
AL = sleeve_length
ARMSCYE = max(200.0, PANEL_CHEST * 1.05)
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


def _clip_marks(edge_name, seam_len):
    """Return conduit-clip drill marks by fraction along an edge, at clip_pitch spacing."""
    n = max(1, int(round(seam_len / clip_pitch)))
    return n


def _body(is_front):
    p_hem_l = fc.P(0.0, 0.0)
    p_side_hem = fc.P(PANEL_WAIST, 0.0)
    armscye_y = BL - ARMSCYE
    p_underarm = fc.P(PANEL_CHEST, armscye_y)
    p_shoulder = fc.P(NECK_W + (PANEL_CHEST - NECK_W) * 0.7, BL - 8.0)
    if is_front:
        neck_drop = NECK_W * 0.85
        p_neck_sh = fc.P(NECK_W, BL)
        p_center_top = fc.P(0.0, BL - neck_drop)
        neck_ctrl0 = fc.P(NECK_W * 0.7, BL - neck_drop * 0.35)
        neck_ctrl1 = fc.P(NECK_W * 0.3, BL - neck_drop * 0.8)
    else:
        neck_drop = NECK_W * 0.25
        p_neck_sh = fc.P(NECK_W, BL)
        p_center_top = fc.P(0.0, BL - neck_drop)
        neck_ctrl0 = fc.P(NECK_W * 0.6, BL - neck_drop * 0.5)
        neck_ctrl1 = fc.P(NECK_W * 0.25, BL - neck_drop)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_l, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem,
                                   fc.P(PANEL_WAIST + (PANEL_CHEST - PANEL_WAIST) * 0.4,
                                        armscye_y * 0.5),
                                   fc.P(PANEL_CHEST * 0.98, armscye_y * 0.85), p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(PANEL_CHEST * 0.9, armscye_y + ARMSCYE * 0.45),
                                      fc.P(p_shoulder.x + 14.0, p_shoulder.y - 30.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_sh)]),
        fc.Edge("neck", [fc.Bezier(p_neck_sh, neck_ctrl0, neck_ctrl1, p_center_top)]),
        fc.Edge("center", [fc.Line(p_center_top, p_hem_l)]),
    ]
    name = "front" if is_front else "back"
    piece = fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("armscye", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(PANEL_CHEST * 0.4, BL * 0.2),
                               fc.P(PANEL_CHEST * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=(2 if is_front else 1),
                       mirror=is_front, on_fold=(not is_front),
                       fold_edge=(None if is_front else "center")),
        label=("Front (cut 2 — cable races at the seams)" if is_front
               else "Back (cut 1 on fold — cable races at the seams)"),
    )
    # conduit-clip marks along the SIDE seam (the main cable race)
    side_len = piece.edge("side").length()
    n_clips = _clip_marks("side", side_len)
    internals = []
    for i in range(n_clips):
        t = (i + 0.5) / n_clips
        p, _ = piece.edge("side").point_at_fraction(t)
        internals.append(fc.Internal(f"side-clip-{i}", [fc.P(p.x - tab_w / 2.0, p.y),
                                                        fc.P(p.x + tab_w / 2.0, p.y)],
                                                            kind="drill"))
    internals.append(fc.Internal("side-conduit", [(piece.edge("side").point_at_fraction(0.05)[0]),
                                                  (piece.edge("side").point_at_fraction(0.95)[0])],
                                 kind="trace"))
    piece.internals = internals
    return piece


def build_sleeve(armscye_len):
    bicep_half = (bicep_girth * E) / 2.0
    chord = min(2.0 * bicep_half, armscye_len * 0.92)
    bicep_half = chord / 2.0
    cuff_half = max(70.0, bicep_half * 0.82)
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
    piece = fc.Piece(
        "sleeve",
        [fc.Edge("cap", [fc.Line(cap_pts[i], cap_pts[i + 1]) for i in range(len(cap_pts) - 1)]),
         fc.Edge("underseam_r", [fc.Line(cap_pts[-1], p_cuff_r)]),
         fc.Edge("cuff", [fc.Line(p_cuff_r, p_cuff_l)]),
         fc.Edge("underseam_l", [fc.Line(p_cuff_l, cap_pts[0])])],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(bicep_half, -AL * 0.2), fc.P(bicep_half, -AL * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2 — underseam cable race)",
    )
    # conduit-clip marks along the underseam
    us_len = piece.edge("underseam_r").length()
    n = _clip_marks("underseam_r", us_len)
    internals = []
    for i in range(n):
        t = (i + 0.5) / n
        p, _ = piece.edge("underseam_r").point_at_fraction(t)
        internals.append(fc.Internal(f"sleeve-clip-{i}", [fc.P(p.x - tab_w / 2.0, p.y),
                                                          fc.P(p.x + tab_w / 2.0, p.y)],
                                                              kind="drill"))
    piece.internals = internals
    return piece


def build_junction():
    w = junction_pocket
    d = junction_pocket * 1.1
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, d), fc.P(0.0, d)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("mouth", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("bundle-entry", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, d * 0.5)], kind="trace"),
                 fc.Internal("mouth-fold", [fc.P(0.0, d - 20.0), fc.P(w, d - 20.0)],
                     kind="marking")]
    return fc.Piece(
        "junction", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Junction pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("conduit-cable-harness-tee")
    front = _body(True)
    back = _body(False)
    armscye_len = front.edge("armscye").length() + back.edge("armscye").length()
    sleeve = build_sleeve(armscye_len)
    junction = build_junction()

    picked = {"front": front, "back": back, "sleeve": sleeve, "junction": junction}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, sleeve, junction):
            pattern.add(piece)
        # side seam: front side to back side. Back is on fold -> its side edge is one side;
        # two fronts each meet a back side.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=2.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armscye"), ("back", "armscye")], tol=2.0)

    side_clips = max(1, int(round(front.edge("side").length() / clip_pitch)))
    sleeve_clips = max(1, int(round(sleeve.edge("underseam_r").length() / clip_pitch)))
    total_clips = side_clips * 2 + sleeve_clips * 2

    fabric_width = 1650.0
    area = front.area() * 2.0 + back.area() * 2.0 + sleeve.area() * 2.0 + junction.area()
    marker_len = area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "base tee knit (cotton/poly)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front, back, sleeves and junction at {fabric_width:.0f} mm width, 80% marker."},
        {"item": "seam conduit clips (Yantra4D seam-conduit-clip)", "qty": total_clips,
         "unit": "count",
         "note": f"{total_clips} clips: {side_clips} per side seam x2 + {sleeve_clips} per "
                 f"underseam x2, at {clip_pitch:.0f} mm pitch (notion.hardware_ref -> "
                 f"seam-conduit-clip); tab_w {tab_w:.0f} mm drives the clip AND the drafted tab."},
        {"item": "cable bundle (routed in-seam)",
         "qty": round((front.edge('side').length()
                       + sleeve.edge('underseam_r').length()) * 2.0),
         "unit": "mm_length",
         "note": f"the {bundle_dia:.0f} mm bundle runs in the seam allowances, held by the clips; "
                 "sourced separately — this pattern contains no cable, connector, or circuit."},
        {"item": "coverstitch + junction closure", "qty": 1, "unit": "set",
         "note": "the bundles converge at the junction pocket at the front hem."},
    ]
    pattern.metadata = {
        "fc500_rank": 472, "family": "etextile", "fabric_hint": "jersey-conductor",
        "not_a_loom": "This routes and clips cable bundles along the seams. It contains no cable, "
                      "connector, or circuit and makes no electrical claim.",
        "silhouette_note": "A base tee whose seams are cable races: conduit clips hold cable "
            "bundles in the side and underarm seams, converging at a pocket. The garment a "
            "wearable-electronics maker needs — wiring in the seams, not safety-pinned inside.",
        "hardware": "conduit clips via Yantra4D (notion.hardware_ref -> seam-conduit-clip); tab_w "
            "drives the clip's seam_tabs flange AND the drafted clip footprint.",
        "solved": {
            "chest_half_mm": round(CHEST_HALF, 1),
            "side_seam_mm": round(front.edge("side").length(), 1),
            "side_clips": side_clips,
            "sleeve_underseam_mm": round(sleeve.edge("underseam_r").length(), 1),
            "sleeve_clips": sleeve_clips,
            "total_clips": total_clips,
            "clip_pitch_mm": round(clip_pitch, 1),
            "note": "clips = round(seam_length / clip_pitch) per seam, so spacing stays constant "
                    "whatever the body size; the seam allowance holds the tab + bundle.",
        },
        "etextile_note": "The conduit clip positions, the in-seam cable traces, and the junction "
                         "bundle-entry are MARKED. No cable, connector, or circuit is drafted.",
    }
    return pattern


result = build()
