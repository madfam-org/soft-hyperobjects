"""
Turtleneck Sweater — FC-100 rank #40. Fashion Cabinet Garment Cartridge.

The sweater block with a TALL FUNNEL COLLAR. Slim knit body (ease 90), a
higher neckline than the crew (front drop 55, back 15) so the funnel sits
close to the throat, long sleeve with the cap solved to the armholes, and
FOUR derived rib pieces:

  collar    length = neck opening x collar_ratio (0.75 — turtlenecks need
            strong negative ease to hug) + 2 x seam_allowance.
            Piece height = 2 x collar_height + 2 x seam_allowance: the tube
            is folded double when sewn, and the funnel is worn folded, so the
            FINISHED height = collar_height (default 110) while the PIECE is
            cut at twice that plus allowances.
  cuffs     sleeve opening x 0.72 — deeper grip (finished height 70)
  hem band  hem x 0.88 (finished height 45)

Shoulder seams carry stabilizer-tape placement traces (knits grow on the
bias of the shoulder). Cut-and-sew knitwear branch; fully-fashioned is a
future mode.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|ribs|set

chest_girth   = float(PARAM(lambda: chest_girth, 960.0))
body_length   = float(PARAM(lambda: body_length, 650.0))    # nape to hem-band seam
neck_girth    = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 610.0))  # apex to cuff seam
sweater_ease  = float(PARAM(lambda: sweater_ease, 90.0))    # slim knit total ease
collar_ratio  = float(PARAM(lambda: collar_ratio, 0.75))    # collar/neck opening
collar_height = float(PARAM(lambda: collar_height, 110.0))  # FINISHED funnel height
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.72))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.88))
cuff_height    = float(PARAM(lambda: cuff_height, 70.0))    # finished rib heights
hemband_height = float(PARAM(lambda: hemband_height, 45.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
sweater_ease = max(30.0, min(sweater_ease, 300.0))
collar_ratio = max(0.55, min(collar_ratio, 0.95))
collar_height = max(60.0, min(collar_height, 180.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
hemband_ratio = max(0.70, min(hemband_ratio, 1.0))

W = (chest_girth + sweater_ease) / 4.0
L = body_length
AH = (chest_girth + sweater_ease) / 8.0 + 95.0        # closer armscye than the crew
AH = max(180.0, min(AH, L - 100.0))
NW = max(62.0, neck_girth / 5.0 + 2.0)
HPS_Y = L + 20.0
SHOULDER_DROP = 35.0                                  # slimmer, more sloped shoulder
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
FRONT_NECK_DROP = 55.0                                # high neckline — funnel sits close
BACK_NECK_DROP = 15.0


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _shoulder_tape():
    """Stabilizer-tape placement trace 10 mm inside the shoulder seam."""
    return fc.Internal(
        "shoulder tape",
        [fc.P(NW, HPS_Y - 10.0), fc.P(W - 5.0, HPS_Y - SHOULDER_DROP - 10.0)],
        kind="trace",
    )


def _body_piece(name, neck_drop, label):
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},            # hem seams onto the rib band
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=[_shoulder_tape()],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
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
    chw = max(85.0, hb * 0.58)                         # slim taper into the deep cuff
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


def _rib(name, finished_len, piece_h, qty, label, notches=None):
    """Rib rectangle drawn at RAW size: length = finished + 2sa, height as given.

    seam_allowance is 0 because allowances are already inside the drawn size;
    the fold line marks the doubled-when-sewn midline.
    """
    length = finished_len + 2.0 * seam_allowance
    piece = fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, piece_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, piece_h), fc.P(0.0, piece_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, piece_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=list(notches or []),
        grainline=fc.Grainline(fc.P(length * 0.2, piece_h / 2.0),
                               fc.P(length * 0.8, piece_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, piece_h / 2.0),
                                             fc.P(length, piece_h / 2.0)])],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )
    return piece


def build():
    pattern = fc.PatternSet("turtleneck-sweater")
    front = _body_piece("front", FRONT_NECK_DROP, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    sleeve = build_sleeve(cap_target)
    if all_pieces or target_piece == "sleeve":
        pattern.add(sleeve)
    if all_pieces or target_piece == "ribs":
        neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
        hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
        cuff_circ = sleeve.edge("hem").length()
        # Strong negative ease gets QUARTERED onto the neckline when sewn.
        quarters = [fc.Notch("bottom", 0.25, "quarter"), fc.Notch("bottom", 0.5, "center"),
                    fc.Notch("bottom", 0.75, "quarter")]
        pattern.add(_rib("collar", neck_opening * collar_ratio,
                         2.0 * collar_height + 2.0 * seam_allowance, 1,
                         "Funnel Collar (rib)", quarters))
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, 2.0 * cuff_height, 2,
                         "Cuff (rib)"))
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, 2.0 * hemband_height, 1,
                         "Hem Band (rib)"))
    if all_pieces:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
    pattern.metadata = {
        "fc100_rank": 40,
        "fabric_hint": "felpa-algodon",
        "knit_note": "cut-and-sew branch; fully-fashioned future",
        "collar_note": "wear folded; piece height = 2x finished",
        "rib_ratios": {"collar": collar_ratio, "cuff": cuff_ratio, "hem": hemband_ratio},
        "drafting": "slim sweater block; high neckline; funnel collar folded double",
    }
    return pattern


result = build()
