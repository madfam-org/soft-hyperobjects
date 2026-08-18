"""
Varsity Jacket — FC-100 rank #66. Fashion Cabinet Garment Cartridge.

The classic baseball/letterman jacket: the bomber-jacket architecture (rank #29)
with the front zipper swapped for a SNAP-BUTTON PLACKET and the sleeves cut in a
CONTRAST fabric (the two-tone letterman look). The front is cut as TWO mirrored
halves — never on fold — whose center edge is the snap placket: the wearer's right
front laps the left by a `placket_ext` stand, and five snap fasteners run the
center-front line as drill cross-marks (opening pair + surround). Each front also
carries a hand WELT-POCKET marking and a chenille chest-patch placement marking.
The long set-in sleeve cap is SOLVED by bisection against the measured armhole
pair; the sleeves are drafted in the contrast card so the BOM orders body and
sleeve yardage separately. All three ribs are DERIVED, no solver: the collar rib
is the full neck opening x collar_ratio + 2 sa (folded, 2 x collar_height tall),
the cuffs are the sleeve opening x cuff_ratio, and the hem/waist rib — cut SPLIT
for the placket opening, with a center-back notch — is the hem circumference x
hem_ratio + 2 sa. Snap hardware is a Yantra4D solid, federated through the
shank-button notion cartridge; the ribs are the negative-eased knit trim that
gives the letterman its silhouette.

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth   = float(PARAM(lambda: chest_girth, 1060.0))
body_length   = float(PARAM(lambda: body_length, 610.0))
neck_girth    = float(PARAM(lambda: neck_girth, 410.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 610.0))
varsity_ease  = float(PARAM(lambda: varsity_ease, 220.0))
placket_ext   = float(PARAM(lambda: placket_ext, 35.0))
snap_count    = int(float(PARAM(lambda: snap_count, 5)))
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.75))
hem_ratio     = float(PARAM(lambda: hem_ratio, 0.82))
collar_ratio  = float(PARAM(lambda: collar_ratio, 0.80))
collar_height = float(PARAM(lambda: collar_height, 45.0))
cuff_height    = float(PARAM(lambda: cuff_height, 60.0))
hem_height     = float(PARAM(lambda: hem_height, 60.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
varsity_ease = max(80.0, min(varsity_ease, 420.0))
placket_ext = max(20.0, min(placket_ext, 55.0))
snap_count = max(3, min(snap_count, 8))
collar_ratio = max(0.60, min(collar_ratio, 1.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
hem_ratio = max(0.70, min(hem_ratio, 1.0))
collar_height = max(20.0, min(collar_height, 80.0))
cuff_height = max(30.0, min(cuff_height, 100.0))
hem_height = max(30.0, min(hem_height, 100.0))

W = (chest_girth + varsity_ease) / 4.0
L = body_length
AH = (chest_girth + varsity_ease) / 8.0 + 105.0
AH = max(180.0, min(AH, L - 100.0))
NW = max(60.0, neck_girth / 5.0 + 2.0)         # rib band collar: near-standard neck
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 30.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 80.0
BACK_NECK_DROP = 20.0


def _cross(label, x, y, half=4.0):
    """Drill cross-mark as two internals (notion-placement convention)."""
    return [
        fc.Internal(f"{label}-h", [fc.P(x - half, y), fc.P(x + half, y)],
                    kind="drill"),
        fc.Internal(f"{label}-v", [fc.P(x, y - half), fc.P(x, y + half)],
                    kind="drill"),
    ]


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_edges(neck_drop, center_x):
    """Half-body outline shared by front and back.

    `center_x` places the center edge: 0 for the back fold, -placket_ext for a
    front so the snap stand laps past center front. The hem and neck run out to
    the same center_x so the outline stays closed.
    """
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(center_x, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Line(fc.P(center_x, neck_top_y), fc.P(0.0, neck_top_y)),
         fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45),
                   fc.P(NW, HPS_Y))],
    )
    return [
        fc.Edge("center", [fc.Line(origin, fc.P(center_x, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]


def _welt_marks():
    """Horizontal hand welt-pocket marking: 150 mm opening trace + surround box.

    A letterman's slash hand pockets sit level near the hem — modeled as a
    straight 150 mm opening (kept clear of the snap stand) inside its welt
    construction surround box (18 mm above/below, ends extended 10 mm).
    """
    cx = min(W * 0.55, W - 90.0)
    cy = max(95.0, min(L * 0.30, UNDERARM.y - 70.0))
    p1 = fc.P(cx - 75.0, cy)                        # inner end (toward CF)
    p2 = fc.P(cx + 75.0, cy)                        # outer end (toward side seam)
    opening = fc.Internal("welt pocket opening", [p1, p2], kind="trace")
    e1 = fc.P(p1.x - 10.0, cy)
    e2 = fc.P(p2.x + 10.0, cy)
    corners = [fc.P(e1.x, cy + 18.0), fc.P(e2.x, cy + 18.0),
               fc.P(e2.x, cy - 18.0), fc.P(e1.x, cy - 18.0)]
    box = fc.Internal("welt pocket box", corners + corners[:1])
    return [opening, box]


def _chest_patch_mark():
    """Chenille chest-patch placement box (left front): the letterman patch
    zone. Marking only — the patch is an applied trim, not a pattern piece."""
    px = W * 0.42
    py = L * 0.62
    hw, hh = 55.0, 65.0
    corners = [fc.P(px - hw, py + hh), fc.P(px + hw, py + hh),
               fc.P(px + hw, py - hh), fc.P(px - hw, py - hh)]
    return [fc.Internal("chenille patch zone", corners + corners[:1],
                        kind="marking")]


def _snap_marks():
    """Snap-fastener placement along center front (x = 0): `snap_count` drill
    crosses evenly spaced between the collar seam and the hem-rib seam. Snaps
    are Yantra4D hardware (shank-button notion), never modeled here."""
    top = HPS_Y - FRONT_NECK_DROP - 30.0
    bottom = 45.0
    marks = []
    if snap_count == 1:
        ys = [(top + bottom) / 2.0]
    else:
        step = (top - bottom) / (snap_count - 1)
        ys = [bottom + i * step for i in range(snap_count)]
    for i, y in enumerate(ys):
        marks += _cross(f"snap-{i + 1}", 0.0, y)
    return marks


def build_front():
    """Half front, cut 2 mirrored (never on fold): center edge is the snap
    stand (laps past CF by placket_ext), carrying the snap line + pockets."""
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP, -placket_ext),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("center", 0.5, "snap placket / CF fold"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=_snap_marks() + _welt_marks() + _chest_patch_mark(),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (snap-placket half)",
    )


def build_back():
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP, 0.0),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                  fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                  fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Long CONTRAST sleeve; the set-in cap is solved by bisection to the
    armhole pair (ease 0). Cut in the contrast card (the two-tone look)."""
    ch = max(50.0, AH * 0.30)
    sl = max(100.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(90.0, hb * 0.62)
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},        # wrist finished with a rib cuff
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (contrast)",
    )


def _rib(name, finished_len, finished_height, qty, label, notches=None):
    band_h = 2.0 * finished_height
    length = finished_len + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=list(notches or []),
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("varsity-jacket")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # Full neck opening: TWO front halves (cut 2) + the folded back's two halves.
    neck_opening = 2.0 * (front.edge("neck").length(0.05) + back.edge("neck").length(0.05))
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    sleeve = None
    if everything or target_piece in ("sleeve", "ribs"):
        sleeve = build_sleeve(cap_target)          # ribs need the measured opening
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "ribs":
        # DERIVED ribs — no solver: lengths are measured openings x ratios.
        cb = fc.Notch("bottom", 0.5, "center back")
        pattern.add(_rib("collar_rib", neck_opening * collar_ratio, collar_height, 1,
                         "Collar (band rib)", notches=[cb]))
        pattern.add(_rib("cuff_rib", sleeve.edge("hem").length() * cuff_ratio,
                         cuff_height, 2, "Cuff (rib)"))
        hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
        # The hem/waist rib is SPLIT for the snap placket: cut flat, ends open at
        # center front; the center notch (= center back when worn) marks the gap.
        cbz = fc.Notch("bottom", 0.5, "center back; placket gap at the ends")
        pattern.add(_rib("hem_rib", hem_circ * hem_ratio, hem_height, 1,
                         "Waist Rib (split)", notches=[cbz]))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve still meets
        # exactly ONE front armhole + ONE back armhole — the drafted pair.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)

    # ── BOM: two-tone body + contrast sleeves + rib trim + snap hardware ──────
    body_pieces = [p for p in pattern.pieces if p.name in ("front", "back")]
    rib_pieces = [p for p in pattern.pieces
                  if p.name in ("collar_rib", "cuff_rib", "hem_rib")]
    sleeve_pieces = [p for p in pattern.pieces if p.name == "sleeve"]

    def _yardage(pieces, width):
        area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                   for p in pieces)
        return round((area / (width * 0.60)) / 10.0) * 10 if area else 0

    body_width = 1700.0                            # felpa-algodon card width
    sleeve_width = 1500.0                          # mezclilla-denim card width
    rib_len = sum(p.edge("bottom").length() * p.cut.quantity for p in rib_pieces)
    if everything:
        pattern.bom = [
            {"item": "felpa-algodon", "qty": _yardage(body_pieces, body_width),
             "unit": "mm_length",
             "note": f"body (front x2 + back) at {body_width:.0f} mm width, "
                     "60% marker efficiency"},
            {"item": "mezclilla-denim", "qty": _yardage(sleeve_pieces, sleeve_width),
             "unit": "mm_length",
             "note": f"CONTRAST sleeves (x2) at {sleeve_width:.0f} mm width, "
                     "60% marker efficiency; two-tone letterman look — classic is "
                     "a wool-melton body with leather sleeves"},
            {"item": "1x1 rib knit trim (collar + cuffs + waist)",
             "qty": round(rib_len / 10.0) * 10, "unit": "mm_length",
             "note": "negative-eased knit; total finished band length, cut to "
                     "2 x height and folded; sold by the metre or as pre-knit "
                     "collar/cuff/waistband sets in team colors"},
            {"item": "ring-snap fasteners 15 mm", "qty": snap_count, "unit": "sets",
             "note": f"{snap_count} snap sets on the center-front placket; each "
                     "set = cap+socket+stud+post; hardware is a Yantra4D cartridge "
                     "(shank-button notion guide), never re-implemented here"},
            {"item": "all-purpose thread + ballpoint/jersey needle 80/12",
             "qty": 1, "unit": "set",
             "note": "ballpoint for the rib knit; topstitch the placket and welts"},
        ]

    pattern.metadata = {
        "fc100_rank": 66,
        "fabric_hint": "felpa-algodon",
        "body_fabric": "felpa-algodon",
        "sleeve_fabric": "mezclilla-denim",
        "two_tone_note": ("body and sleeves are cut in different cards — the "
                          "letterman two-tone; the classic is a wool-melton body "
                          "with leather sleeves"),
        "sleeve_attachment": ("set-in cap solved to the armhole pair (bomber "
                              "method); the authentic letterman uses RAGLAN "
                              "sleeves — set-in is the declared simplification "
                              "here for a robust solved cap"),
        "snap_count": snap_count,
        "snap_note": ("center-front SNAP placket (not a zipper); snap hardware "
                      "via the shank-button notion cartridge (Yantra4D)"),
        "placket_extension_mm": placket_ext,
        "collar_formula": ("collar_rib = neck opening x collar_ratio + 2 x "
                           "seam_allowance, folded to 2 x collar_height; derived, "
                           "no solve check"),
        "rib_ratios": {"collar": collar_ratio, "cuff": cuff_ratio, "hem": hem_ratio},
        "rib_note": ("collar / cuffs / waist are rib bands whose length = opening "
                     "x ratio (negative-eased, delta 0 by construction — they "
                     "stretch to fit the larger opening)"),
        "drafting": ("bomber-jacket block: zipper swapped for a snap placket "
                     "(stand extension + snap drill marks) and sleeves cut in the "
                     "contrast card; teaching-grade — welt pockets and chenille "
                     "patch are markings, snaps and set-in-vs-raglan are noted"),
    }
    return pattern


result = build()
