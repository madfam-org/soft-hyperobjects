"""
Bomber Jacket — FC-100 rank #29. Fashion Cabinet Garment Cartridge.

The zip-hoodie architecture (rank #14) with the hood swapped for a RIBBED
STAND COLLAR. The front is cut as TWO mirrored halves — never on fold — whose
center edge is the zipper seam: 15 mm tape allowance, top/bottom stop notches,
and a 7 mm stitch line per the zipper-notion installation convention. Each
front carries a diagonal 150 mm WELT POCKET marking (opening trace + surround
box). The long sleeve cap stays SOLVED by bisection against the measured
armhole pair. All three ribs are DERIVED, no solver: the collar rib is the
full neck opening x collar_ratio + 2 sa (folded, 2 x collar_height tall),
cuffs are the sleeve opening x cuff_ratio, and the hem rib — cut SPLIT for
the zipper with a center-back notch — is the hem circumference x hem_ratio
+ 2 sa. Metadata derives the closed-end zipper length to order; slider/pull
hardware is a Yantra4D solid, federated through the zipper-notion cartridge.

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

chest_girth   = float(PARAM(lambda: chest_girth, 1040.0))
body_length   = float(PARAM(lambda: body_length, 600.0))
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
bomber_ease   = float(PARAM(lambda: bomber_ease, 200.0))
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.75))
hem_ratio     = float(PARAM(lambda: hem_ratio, 0.82))
collar_ratio  = float(PARAM(lambda: collar_ratio, 0.80))
collar_height = float(PARAM(lambda: collar_height, 40.0))
cuff_height    = float(PARAM(lambda: cuff_height, 55.0))
hem_height     = float(PARAM(lambda: hem_height, 55.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 9.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
bomber_ease = max(80.0, min(bomber_ease, 420.0))
collar_ratio = max(0.60, min(collar_ratio, 1.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
hem_ratio = max(0.70, min(hem_ratio, 1.0))
collar_height = max(20.0, min(collar_height, 80.0))
cuff_height = max(30.0, min(cuff_height, 100.0))
hem_height = max(30.0, min(hem_height, 100.0))

W = (chest_girth + bomber_ease) / 4.0
L = body_length
AH = (chest_girth + bomber_ease) / 8.0 + 105.0
AH = max(180.0, min(AH, L - 100.0))
NW = max(60.0, neck_girth / 5.0 + 2.0)         # no hood: near-standard neck
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 30.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 75.0
BACK_NECK_DROP = 20.0
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 10.0  # stop notches sit this far inside the seam ends


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_edges(neck_drop):
    """Half-body outline shared by front and back; center edge at x = 0."""
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]


def _welt_marks():
    """Diagonal welt-pocket marking: 150 mm opening trace + surround box.

    The opening is an exact 3-4-5 diagonal (120 across, 90 down = 150 mm),
    upper end toward the side seam, lower end toward center front — the hand
    enters downward and inward. The box is the welt construction surround:
    20 mm each side of the opening, ends extended 10 mm along it.
    """
    cx = min(W * 0.55, W - 90.0)
    cy = max(115.0, min(L * 0.33, UNDERARM.y - 70.0))
    along = fc.P(-0.8, -0.6)                       # unit slope, toward CF/down
    perp = fc.P(0.6, -0.8)
    p1 = fc.P(cx + 60.0, cy + 45.0)                # upper end (side-seam side)
    p2 = fc.P(cx - 60.0, cy - 45.0)                # lower end (center-front side)
    opening = fc.Internal("welt pocket opening", [p1, p2], kind="trace")
    e1 = p1 - along * 10.0
    e2 = p2 + along * 10.0
    corners = [e1 + perp * 20.0, e2 + perp * 20.0, e2 - perp * 20.0, e1 - perp * 20.0]
    box = fc.Internal("welt pocket box", corners + corners[:1])
    return [opening, box]


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge is the zip seam."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length
    t_stop = ZIP_STOP_INSET / zlen
    stitch = fc.Internal(
        "zipper stitch line",
        [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
        kind="trace",
    )
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance, "center": ZIP_SA},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("center", 1.0 - t_stop, "zipper top stop"),
            fc.Notch("center", t_stop, "zipper bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=[stitch] + _welt_marks(),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip half)",
    )


def build_back():
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
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
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Long bomber sleeve; the cap is solved by bisection to the armhole pair."""
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
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
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
    pattern = fc.PatternSet("bomber-jacket")
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
        sleeve = build_sleeve(cap_target)      # ribs need the measured opening
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "ribs":
        # DERIVED ribs — no solver: lengths are measured openings x ratios.
        cb = fc.Notch("bottom", 0.5, "center back")
        pattern.add(_rib("collar_rib", neck_opening * collar_ratio, collar_height, 1,
                         "Collar (stand rib)", notches=[cb]))
        pattern.add(_rib("cuff_rib", sleeve.edge("hem").length() * cuff_ratio,
                         cuff_height, 2, "Cuff (rib)"))
        hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
        # The hem rib is SPLIT for the zipper: cut flat, ends open at center
        # front; the center notch (= center back when worn) marks the gap.
        cbz = fc.Notch("bottom", 0.5, "center back; zipper gap at the ends")
        pattern.add(_rib("hem_rib", hem_circ * hem_ratio, hem_height, 1,
                         "Hem Rib (split)", notches=[cbz]))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve still meets
        # exactly ONE front armhole + ONE back armhole — the drafted pair.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
    # Closed-end zipper to order: the full front opening runs the center edge
    # plus the split hem rib's height; stops sit at the rib bottom and collar.
    zip_total = front.edge("center").length() + hem_height
    pattern.metadata = {
        "fc100_rank": 29,
        "fabric_hint": "felpa-algodon",
        "shell_note": "nylon-shell fabric card pending; felpa as stand-in",
        "zipper_length_mm": int(round(zip_total / 10.0) * 10),
        "zipper_note": "order this closed-end zipper; hardware via zipper-notion cartridge",
        "sleeve_zipper_garage": ("optional MA-1 sleeve utility zip: reuse the welt box on "
                                 "the left sleeve with a garage tab covering the slider at "
                                 "the top stop; hardware via zipper-notion"),
        "collar_formula": ("collar_rib = neck opening x collar_ratio + 2 x seam_allowance, "
                           "folded to 2 x collar_height; derived, no solve check"),
        "rib_ratios": {"collar": collar_ratio, "cuff": cuff_ratio, "hem": hem_ratio},
        "drafting": "zip-hoodie block, hood swapped for a derived rib stand collar",
    }
    return pattern


result = build()
