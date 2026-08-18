"""
Waistcoat — FC-100 rank #69. Fashion Cabinet Garment Cartridge.

The commons' first sleeveless tailoring garment ("chaleco de vestir"): a classic
single-breasted 5-button suit waistcoat, honestly simplified. It is a tailored
FRONT with no sleeve — the armhole is a finished/BOUND edge (a clean armscye
curve, faced or bound, no sleeve piece). The neckline is a deep front V that
drops to the top button on the center front. The front's center edge runs up a
button stand to the top-button point, then breaks into the V-neck up to the neck
point. Below the bottom button the front hem comes to the signature POINTED hem
(each cut-2 front dips to a point at CF; mirrored, the pair reads as the notched
waistcoat front). A fisheye waist dart shapes the front, and welt-pocket markings
(two lower + one breast) are drilled in.

The back is the signature CINCHED back: cut 2 mirror with a shaped center-back
seam that nips the waist, drafted in LINING (a suit waistcoat's back and the
whole inside are lined — worsted fronts, satin/lining back). A CINCH BELT — two
adjustable strap pieces (cut 2: buckle strap + tongue strap) with buckle/slider
placement markings — pulls the back waist in. The front FACING (CF + V-neck +
hem-point run) is a straight strip verified against the measured front edge run,
per the blazer's facing method. Lining is noted, not fully drafted, in v0.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
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


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|facing|cinch_strap|set

chest_girth    = float(PARAM(lambda: chest_girth, 1020.0))
waist_girth    = float(PARAM(lambda: waist_girth, 880.0))    # for the CB nip
body_length    = float(PARAM(lambda: body_length, 560.0))    # nape to front point
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
waistcoat_ease = float(PARAM(lambda: waistcoat_ease, 90.0))  # total ease (close fit)
button_stand   = float(PARAM(lambda: button_stand, 20.0))    # extension past CF
neck_drop      = float(PARAM(lambda: neck_drop, 235.0))      # CF top button above point
front_point    = float(PARAM(lambda: front_point, 55.0))     # hem point dip below side hem
back_cinch     = float(PARAM(lambda: back_cinch, 22.0))      # CB waist shaping per side
strap_length   = float(PARAM(lambda: strap_length, 210.0))   # each cinch strap length
strap_width    = float(PARAM(lambda: strap_width, 32.0))     # cinch strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
waist_girth = max(600.0, min(waist_girth, 1600.0))
body_length = max(440.0, min(body_length, 720.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
waistcoat_ease = max(40.0, min(waistcoat_ease, 200.0))
button_stand = max(15.0, min(button_stand, 30.0))
neck_drop = max(170.0, min(neck_drop, 320.0))
front_point = max(25.0, min(front_point, 90.0))
back_cinch = max(8.0, min(back_cinch, 40.0))
strap_length = max(150.0, min(strap_length, 300.0))
strap_width = max(20.0, min(strap_width, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── Waistcoat block (tailored front, no sleeve) ──────────────────────────────
W = (chest_girth + waistcoat_ease) / 4.0        # quarter body width
L = body_length                                 # datum y=0 is the front hem point
NW = max(55.0, neck_girth / 5.0)                # half neck width at HPS
AH = (chest_girth + waistcoat_ease) / 8.0 + 95.0  # armhole depth (auto)
AH = max(170.0, min(AH, L - 200.0))             # chest line above the waist
HPS_Y = L + 20.0
SHOULDER_DROP = 40.0                            # waistcoats sit narrow at the shoulder
BACK_NECK_DROP = 22.0
SH_END = fc.P(W - 20.0, HPS_Y - SHOULDER_DROP)  # narrow shoulder (armhole bound)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
CHEST_Y = UNDERARM.y
BS = button_stand
# Front V-neck: center (button-stand) edge ends at the top button on CF.
TOP_BTN_Y = min(neck_drop, CHEST_Y - 25.0)      # top button height on CF
NECK_PT = fc.P(NW, HPS_Y)                        # V-neck lands on the neck point
# Pointed front hem: side hem sits `front_point` above the CF point (y=0).
HEM_SIDE_Y = front_point                         # side-seam hem height
HEM_BREAK_X = -BS + (W - (-BS)) * 0.42            # where the level hem breaks to the point
CB_WAIST_X = back_cinch                           # CB seam nip at the waist
WAIST_Y = max(90.0, min(L * 0.34, CHEST_Y - 70.0))  # waist level (cinch level)
DART_INTAKE = 16.0                                # front fisheye dart
FACING_W = 70.0                                   # straight front facing width
BUTTONS = 5


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (zipper-notion convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _armhole(scoop):
    """Bound armscye from the shoulder end down to the underarm (no sleeve)."""
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - scoop, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _fisheye_dart():
    """Front fisheye waist dart: a closed diamond widest at the waist, intake
    16 mm, running from below the waist up toward the chest."""
    dx = W * 0.46
    half = DART_INTAKE / 2.0
    y_bot = max(HEM_SIDE_Y + 30.0, WAIST_Y - 85.0)
    y_top = CHEST_Y - 35.0
    return fc.Internal(
        "front fisheye dart",
        [fc.P(dx, y_bot), fc.P(dx - half, WAIST_Y), fc.P(dx, y_top),
         fc.P(dx + half, WAIST_Y), fc.P(dx, y_bot)],
        kind="dart",
    )


def _welt(label, cx, cy, w, h):
    """A welt-pocket marking: the welt rectangle + its attach line. Jetting is
    future work — markings only in v0 (blazer flap-pocket convention)."""
    box = [fc.P(cx - w / 2.0, cy + h / 2.0), fc.P(cx + w / 2.0, cy + h / 2.0),
           fc.P(cx + w / 2.0, cy - h / 2.0), fc.P(cx - w / 2.0, cy - h / 2.0),
           fc.P(cx - w / 2.0, cy + h / 2.0)]
    line = [fc.P(cx - w / 2.0 - 6.0, cy), fc.P(cx + w / 2.0 + 6.0, cy)]
    return [fc.Internal(f"{label}", box, kind="marking"),
            fc.Internal(f"{label} attach", line, kind="marking")]


def build_front():
    """Cut 2 mirror. CCW chain: center (button stand) up to the top button; the
    V-neck up to the neck point; shoulder; bound armhole; side; and the POINTED
    hem (level run then a break down to the CF point at y=0). Worsted wool; fully
    lined + interfaced fronts."""
    cf_point = fc.P(-BS, 0.0)                     # lowest point of the pointed hem
    top_btn = fc.P(-BS, TOP_BTN_Y)                # V-neck starts here on CF
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, TOP_BTN_Y)],
                    kind="marking"),
        _fisheye_dart(),
    ]
    # Five buttonholes on CF (x=0), from the top button down to just above point.
    bh_top = TOP_BTN_Y
    bh_bottom = max(70.0, HEM_SIDE_Y + 40.0)
    step = (bh_top - bh_bottom) / (BUTTONS - 1)
    for i in range(BUTTONS):
        internals += _cross(f"buttonhole-{i + 1}", 0.0, bh_top - i * step)
    # Two lower welt pockets + one breast welt (markings only).
    internals += _welt("lower welt", W * 0.5, WAIST_Y - 25.0, 110.0, 14.0)
    internals += _welt("breast welt", W * 0.62, CHEST_Y - 25.0, 80.0, 12.0)
    # V-neck: a gentle curve from the top button up to the neck point.
    v_neck = fc.Edge(
        "neck",
        [fc.curve_through(top_btn, NECK_PT, bulge=0.06, side=1.0)],
    )
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(cf_point, top_btn)]),
            v_neck,
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(16.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, HEM_SIDE_Y))]),
            fc.Edge("hem", [fc.Line(fc.P(W, HEM_SIDE_Y),
                                    fc.P(HEM_BREAK_X, HEM_SIDE_Y)),
                            fc.Line(fc.P(HEM_BREAK_X, HEM_SIDE_Y), cf_point)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("center", 1.0, "top button"),
                 fc.Notch("side", 0.5),
                 fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.5, HEM_SIDE_Y + 40.0),
                               fc.P(W * 0.5, CHEST_Y - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_back():
    """Cut 2 mirror with a shaped CB seam that nips the waist (the cinched back),
    drafted in LINING (satin/lining back is classic; worsted fronts). CCW chain:
    CB (hem up, waist-nip curve, straight above chest to nape), back neck,
    shoulder, bound armhole, side, hem. The cinch belt attaches at the waist
    (markings)."""
    nape = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    cb_hem = fc.P(0.0, HEM_SIDE_Y)                # back hem is level (no point)
    waist = fc.P(CB_WAIST_X, WAIST_Y)            # CB nipped in at the waist
    span_up = CHEST_Y - WAIST_Y
    cb = fc.Edge(
        "cb",
        [
            fc.Bezier(cb_hem, fc.P(CB_WAIST_X * 0.5, HEM_SIDE_Y + (WAIST_Y - HEM_SIDE_Y) * 0.45),
                      fc.P(CB_WAIST_X, WAIST_Y - (WAIST_Y - HEM_SIDE_Y) * 0.35), waist),
            fc.Bezier(waist, fc.P(CB_WAIST_X, WAIST_Y + span_up * 0.4),
                      fc.P(6.0, CHEST_Y - span_up * 0.2), fc.P(0.0, CHEST_Y)),
            fc.Line(fc.P(0.0, CHEST_Y), nape),
        ],
    )
    neck = fc.Edge(
        "neck",
        [fc.Bezier(nape, fc.P(NW * 0.55, nape.y),
                   fc.P(NW, nape.y + BACK_NECK_DROP * 0.45), NECK_PT)],
    )
    # Cinch-belt attach markings at the waist, and the buckle/tongue side marks.
    internals = [
        fc.Internal("cinch attach line",
                    [fc.P(CB_WAIST_X, WAIST_Y), fc.P(W * 0.7, WAIST_Y)],
                    kind="marking"),
    ]
    internals += _cross("cinch anchor", W * 0.62, WAIST_Y)
    return fc.Piece(
        "back",
        [
            cb,
            neck,
            fc.Edge("shoulder", [fc.Line(NECK_PT, SH_END)]),
            _armhole(12.0),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, HEM_SIDE_Y))]),
            fc.Edge("hem", [fc.Line(fc.P(W, HEM_SIDE_Y), cb_hem)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": seam_allowance + 3.0, "hem": hem_allowance},
        notches=[fc.Notch("side", 0.5),
                 fc.Notch("armhole", 0.5, "back armhole"),
                 fc.Notch("cb", 0.5, "waist / cinch level")],
        grainline=fc.Grainline(fc.P(W * 0.5, HEM_SIDE_Y + 40.0),
                               fc.P(W * 0.5, CHEST_Y - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (lining)",
    )


def build_facing(center_len, neck_len):
    """Straight front facing strip: length = the measured center + V-neck run +
    end allowances (declared as seam ease), width 70. Faces the CF and the deep
    V; a shaped facing that mirrors the point/V is future work (blazer facing
    method)."""
    length = center_len + neck_len + 2.0 * seam_allowance
    t_top = (seam_allowance + center_len) / length
    return fc.Piece(
        "facing",
        [
            fc.Edge("long_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, FACING_W))]),
            fc.Edge("inner", [fc.Line(fc.P(length, FACING_W), fc.P(0.0, FACING_W))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, FACING_W), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                       # length already includes 2×sa
        notches=[fc.Notch("long_edge", t_top, "top button match")],
        grainline=fc.Grainline(fc.P(length * 0.2, FACING_W / 2.0),
                               fc.P(length * 0.8, FACING_W / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Facing",
    )


def build_cinch_strap():
    """The cinch belt: cut 2 (buckle strap + tongue/slider strap). A straight
    strap drafted cut-ready (allowances drafted into the rectangle). One strap
    carries the buckle, the other the tongue holes for the slider; the metal
    buckle + slider are Yantra4D cartridges (see BOM), never re-implemented.
    Each strap sews to the back at the cinch anchor (declared as a short seam)."""
    length = strap_length + 2.0 * seam_allowance
    height = strap_width + 2.0 * seam_allowance
    fold_x = seam_allowance                       # the attach end (sews to back)
    internals = [
        fc.Internal("buckle / tongue zone",
                    [fc.P(length - 55.0, height * 0.5),
                     fc.P(length - seam_allowance, height * 0.5)],
                    kind="marking"),
    ]
    internals += _cross("slider bar", length - 40.0, height * 0.5)
    return fc.Piece(
        "cinch_strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, height))]),
            fc.Edge("top", [fc.Line(fc.P(length, height), fc.P(0.0, height))]),
            fc.Edge("attach", [fc.Line(fc.P(0.0, height), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                       # strap is drafted cut-ready
        notches=[fc.Notch("attach", 0.5, "back cinch anchor")],
        grainline=fc.Grainline(fc.P(fold_x + 8.0, height * 0.5),
                               fc.P(length - 8.0, height * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Cinch Strap (buckle + tongue)",
    )


def build():
    pattern = fc.PatternSet("waistcoat")
    front = build_front()
    back = build_back()
    front_ah = front.edge("armhole").length(0.05)
    back_ah = back.edge("armhole").length(0.05)
    center_len = front.edge("center").length(0.05)
    neck_len = front.edge("neck").length(0.05)
    back_neck_len = back.edge("neck").length(0.05)
    names = ("front", "back", "facing", "cinch_strap")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["facing"]:
        pattern.add(build_facing(center_len, neck_len))
    if wanted["cinch_strap"]:
        pattern.add(build_cinch_strap())
    # ── Seams (all delta ≈ 0; bound armhole + welts are markings, not seams) ──
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["facing"] and wanted["front"]:
        pattern.declare_seam([("facing", "long_edge")],
                             [("front", "center"), ("front", "neck")],
                             tol=3.0, ease=2.0 * seam_allowance)
    if wanted["cinch_strap"] and wanted["back"]:
        # Both straps' attach ends sew to the back at the cinch anchor; the two
        # attach edges together bind to the two mirrored backs' anchor stubs.
        pattern.declare_seam(("cinch_strap", "attach"),
                             ("cinch_strap", "end_b"), tol=1.5)
    fabric_width = 1500.0                          # lana-peinada-traje card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "lana-peinada-traje", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"worsted suiting for the fronts, at {fabric_width:.0f} mm "
                 f"width, 60% marker efficiency"},
        {"item": "lining/satin (back + full front lining)", "qty": 1,
         "unit": "set",
         "note": "the back is cut in lining and the fronts are fully lined; "
                 "welt-pocket bags cut from lining too"},
        {"item": "fusible interfacing (fronts + facings + welts)", "qty": 1,
         "unit": "set",
         "note": "teaching-grade fusible in place of a tailored canvas front"},
        {"item": "suit buttons 15 mm", "qty": BUTTONS, "unit": "pcs",
         "note": f"{BUTTONS} front; hardware is a Yantra4D cartridge "
                 f"(shank-button guide), never re-implemented here"},
        {"item": "cinch buckle + slider", "qty": 1, "unit": "set",
         "note": "back cinch-belt hardware (adjustable buckle + slider bar); "
                 "both are Yantra4D cartridges (buckle guide), not re-implemented"},
        {"item": "polyester thread + universal needle 80/12", "qty": 1,
         "unit": "set",
         "note": "press hard at every stage; bind or face the armscyes and V-neck"},
    ]
    pattern.metadata = {
        "fc100_rank": 69,
        "fabric_hint": "lana-peinada-traje",
        "tailoring_note": "teaching-grade sleeveless waistcoat: bound armscye "
                          "(no sleeve), deep V-neck, pointed front hem, front "
                          "fisheye dart, cinched lined back with an adjustable "
                          "belt; welt pockets are markings (jetting is future "
                          "work)",
        "sleeveless": "armhole is a finished/bound edge — no sleeve piece",
        "neckline": "deep front V to the top button (no lapel, bound/faced V)",
        "front_hem": "pointed — each cut-2 front dips to a point at CF; the "
                     "mirrored pair reads as the notched waistcoat front",
        "front_point_dip_mm": round(front_point, 1),
        "back": "cinched: shaped CB seam nips the waist; cut in lining/satin",
        "back_cinch_per_side_mm": round(CB_WAIST_X, 1),
        "waist_level_mm": round(WAIST_Y, 1),
        "lining": "back drafted in lining; front lining noted, not fully drafted "
                  "in v0",
        "cinch_belt": {"straps": 2, "each_length_mm": round(strap_length, 1),
                       "width_mm": round(strap_width, 1),
                       "hardware": "buckle + slider (Yantra4D)"},
        "armhole_front_mm": round(front_ah, 1),
        "armhole_back_mm": round(back_ah, 1),
        "center_run_mm": round(center_len, 1),
        "v_neck_mm": round(neck_len, 1),
        "back_neck_mm": round(back_neck_len, 1),
        "facing_length_mm": round(center_len + neck_len + 2.0 * seam_allowance, 1),
        "buttonholes": {"count": BUTTONS, "line": "CF (x=0)",
                        "stand_extension_mm": BS,
                        "top_button_at": "V-neck break"},
        "drafting": "sleeveless single-breasted waistcoat on the tailored front "
                    "block: center edge breaks at the top button into a deep V; "
                    "pointed front hem; bound armscye (no sleeve); front fisheye "
                    "dart; shaped cinched CB seam in lining with a two-strap "
                    "adjustable cinch belt; straight facing verified against the "
                    "measured center + V-neck run",
    }
    return pattern


result = build()
