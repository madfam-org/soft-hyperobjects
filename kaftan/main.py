"""
Kaftan — FC-100 rank #99. Fashion Cabinet Garment Cartridge.

Loose, wide, T-shaped tunic-robe of the heritage-global family. Pulled overhead
(no closures): a narrow deep KEYHOLE neckline at centre front, finished by a
shaped NECK FACING ring. Back and front panels are cut on fold at the centre
line in the flat, rectangular economy of the traditional cut; wide dropped
set-in sleeves are solved to the front + back armholes (zero cap ease — a
dropped, near-horizontal shoulder sews flat). Side seams are sewn from the
underarm down to a notched slit top; below the notch the seam opens as a side
slit. A self tie belt is offered as an optional sash.

Honest simplifications (teaching-grade — see docs/README.md):
  - The keyhole is drafted as a narrow, deep centre-front neck opening (the
    front neck curve hugs CF, then flares to the HPS). The rounded throat and
    any hand-worked slit finish are a machine detail, not separate geometry.
  - A simple dropped SET-IN sleeve is drafted (cap solved to the armholes). The
    classic grown-on/T-cut is noted as the alternative in the README.
  - The neck facing is a flat shaped ring; its inner edge reuses the exact
    neckline curves (front + back, mirrored to the full opening), so it matches
    the neckline to floating-point precision.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `chest_girth`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|facing|belt|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))
kaftan_length  = float(PARAM(lambda: kaftan_length, 1200.0))  # nape to finished hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
keyhole_drop   = float(PARAM(lambda: keyhole_drop, 220.0))    # CF neck opening depth
sleeve_length  = float(PARAM(lambda: sleeve_length, 420.0))   # cap apex to hemmed opening
kaftan_ease    = float(PARAM(lambda: kaftan_ease, 300.0))     # generous total wearing ease
slit_height    = float(PARAM(lambda: slit_height, 320.0))     # side slit top above hem
facing_width   = float(PARAM(lambda: facing_width, 55.0))     # finished facing depth
belt_width     = float(PARAM(lambda: belt_width, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
kaftan_length = max(900.0, min(kaftan_length, 1400.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
keyhole_drop = max(90.0, min(keyhole_drop, 380.0))
sleeve_length = max(200.0, min(sleeve_length, 700.0))
kaftan_ease = max(180.0, min(kaftan_ease, 600.0))
slit_height = max(0.0, min(slit_height, 600.0))
facing_width = max(35.0, min(facing_width, 90.0))
belt_width = max(40.0, min(belt_width, 110.0))

# ── Wide dropped-shoulder T-block (traditional flat, rectangular economy) ────
W = (chest_girth + kaftan_ease) / 4.0            # quarter body width (fold at CF/CB)
L = kaftan_length                                # hem at y=0, nape line at y=L
AH = (chest_girth + kaftan_ease) / 8.0 + 110.0   # generous dropped armhole depth
AH = max(190.0, min(AH, L - 140.0))
NW = max(64.0, neck_girth / 5.0 + 4.0)           # half neck width on the fold
HPS_Y = L + 20.0                                 # high point shoulder above nape line
SHOULDER_DROP = 25.0                             # near-horizontal dropped shoulder
BACK_NECK_DROP = 22.0                            # HPS to CB nape
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)    # shoulder tip (armhole top)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)   # underarm point at the side

# Keyhole throat: the front neck curve hugs CF near the bottom, flares to HPS.
keyhole_drop = min(keyhole_drop, HPS_Y - UNDERARM.y - 60.0)  # keep above the bust line
CF_NECK_Y = HPS_Y - keyhole_drop                 # slit bottom on the fold (x = 0)
THROAT_X = min(20.0, NW * 0.28)                  # how narrow the keyhole throat sits

# Side slit: seam is sewn only from the underarm down to the slit top.
slit_height = max(0.0, min(slit_height, UNDERARM.y - 80.0))
T_SLIT = 1.0 - slit_height / UNDERARM.y          # arc fraction of the slit top on `side`

BELT_LEN_RATIO = 2.6                             # sash length as a multiple of chest girth
FABRIC_WIDTH = 1450.0                            # popelina-algodon card width (mm)


# ── Shared edges ─────────────────────────────────────────────────────────────
def _armhole_edge():
    """Front/back armhole curve (dropped-shoulder wovens keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _front_neck_edge():
    """Keyhole neckline: from CF slit-bottom, hug CF, then flare out to the HPS.

    Authored slit-bottom → HPS. Control points keep the curve close to the
    centre for the lower third (the narrow keyhole throat) before opening to
    the shoulder-neck point.
    """
    cf = fc.P(0.0, CF_NECK_Y)
    hps = fc.P(NW, HPS_Y)
    return fc.Edge(
        "neck",
        [fc.Bezier(cf,
                   fc.P(THROAT_X, CF_NECK_Y + keyhole_drop * 0.42),
                   fc.P(NW * 0.42, HPS_Y - keyhole_drop * 0.06),
                   hps)],
    )


def _back_neck_edge():
    """Shallow back neck curve from CB nape to the HPS."""
    cb = fc.P(0.0, HPS_Y - BACK_NECK_DROP)
    hps = fc.P(NW, HPS_Y)
    return fc.Edge(
        "neck",
        [fc.Bezier(cb, fc.P(NW * 0.55, HPS_Y - BACK_NECK_DROP),
                   fc.P(NW, HPS_Y - BACK_NECK_DROP * 0.45), hps)],
    )


def _side_notches():
    return [fc.Notch("side", T_SLIT, "side slit top")] if slit_height > 0.0 else []


def build_front():
    """Front on fold at CF: keyhole neckline finished by the facing."""
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, CF_NECK_Y))]),
        _front_neck_edge(),
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},
        notches=_side_notches() + [fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.5, 90.0), fc.P(W * 0.5, L - 140.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front",
    )


def build_back():
    """Back on fold at CB: shallow neck, otherwise the front's twin."""
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, HPS_Y - BACK_NECK_DROP))]),
        _back_neck_edge(),
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},
        notches=_side_notches() + [fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.5, 90.0), fc.P(W * 0.5, L - 140.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L.

    Cap length grows monotonically with the half-base `hb` — bisect on it.
    """
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.62, sl + ch * 0.10),
                      fc.P(hb * 0.30, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.30, sl + ch),
                     fc.P(-hb * 0.62, sl + ch * 0.10), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Wide dropped set-in sleeve; cap length solved to the armhole sum."""
    ch = max(45.0, AH * 0.28)                        # shallow cap (dropped shoulder)
    sl = max(140.0, sleeve_length - ch)              # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    hb = hi
    for _ in range(56):                              # bisection on the cap half-base
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    solved = _cap_curve(hb, sl, ch).length(0.05)
    if abs(solved - cap_target) > 1.0:
        raise ValueError(
            f"sleeve cap solver did not converge: {solved:.1f} vs target {cap_target:.1f}"
        )
    chw = max(150.0, hb * 0.92)                      # wide open wrist, no cuff
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
        _cap_curve(hb, sl, ch),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_facing(neck_opening):
    """Neck facing: the shaped facing ring drafted as an opened-flat band.

    A facing for a closed neckline is topologically a ring; a single closed
    pattern piece can't carry a hole, so the commons convention is to cut the
    facing open (broken/seamed at CB) and lay it flat as a band. Its `inner`
    edge is the edge that sews to the neckline opening; the seam declaration
    balances it against the full opening (front neck ×2 + back neck ×2). The
    two `end` edges are the CB break, so the strip runs `neck_opening` plus one
    seam allowance at each end (declared as seam ease).

    The band is drawn with a gentle curve so the piece reads as a shaped facing
    rather than a rectangle, while `inner` stays exactly `neck_opening` long.
    """
    length = neck_opening + 2.0 * seam_allowance     # inner edge, incl. CB-break SAs
    h = 2.0 * facing_width                            # cut doubled about the fold line
    inner = fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))])
    outer = fc.Edge(
        "outer",
        [fc.curve_through(fc.P(length, h), fc.P(0.0, h), bulge=0.03, side=1.0)],
    )
    edges = [
        inner,
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
        outer,
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "facing",
        edges,
        seam_allowance=seam_allowance,
        allowances={"inner": 0.0},                   # length already carries the join SAs
        internals=[fc.Internal(
            "CB fold / break",
            [fc.P(length / 2.0, 0.0), fc.P(length / 2.0, h)],
            kind="trace",
        )],
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0),
                               fc.P(length * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Neck facing",
    )


def _strip(name, length, width, qty, label, notches=None):
    """Simple rectangular strip (tie belt / sash), grain along its length."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
        fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        notches=notches or [],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0),
                               fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("kaftan")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)

    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "facing": target_piece in ("facing", "set"),
        "belt": target_piece in ("belt", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    if wanted["facing"]:
        pattern.add(build_facing(neck_opening))
    if wanted["belt"]:
        belt_len = chest_girth * BELT_LEN_RATIO
        pattern.add(_strip("belt", belt_len, belt_width, 1, "Tie belt (sash)",
                           notches=[fc.Notch("top", 0.5, "centre back")]))

    # ── Declared seams (fail-closed; each must balance within tol) ────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        # Set-in cap sews into front + back armholes (summed side b), zero ease.
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    if wanted["facing"] and wanted["front"] and wanted["back"]:
        # Facing inner edge ↔ the full neckline opening = front neck (×2, both
        # sides of the fold) + back neck (×2). The facing runs one seam
        # allowance past the opening at each CB-break end, so that 2×SA is the
        # declared ease (intentional extra length on the facing side).
        pattern.declare_seam(
            [("facing", "inner")],
            [("front", "neck"), ("front", "neck"),
             ("back", "neck"), ("back", "neck")],
            tol=0.5,
            ease=2.0 * seam_allowance,
        )

    # ── Bill of materials ─────────────────────────────────────────────────────
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (FABRIC_WIDTH * 0.62)      # wide flowing panels nest loose
    full_neck = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": (f"light drapey woven at {FABRIC_WIDTH:.0f} mm width, 62% marker "
                  "efficiency; production kaftans span cotton → silk")},
        {"item": "self or contrast facing fabric", "qty": 1, "unit": "piece",
         "note": "neck facing ring; light fusible interfacing keeps the keyhole crisp"},
        {"item": "optional tassel / tie for the keyhole throat", "qty": 1, "unit": "unit",
         "note": ("decorative hardware is a Yantra4D cartridge reference "
                  "(notion.hardware_ref), never re-implemented in the kernel")},
        {"item": "polyester or cotton thread + universal 80/12 needle", "qty": 1,
         "unit": "set", "note": "sharp needle for poplin; finer for silk variants"},
    ]

    pattern.metadata = {
        "fc100_rank": 99,
        "fabric_hint": "popelina-algodon",
        "quarter_width_mm": round(W, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "keyhole_drop_mm": round(keyhole_drop, 1),
        "neck_opening_mm": round(full_neck, 1),
        "facing_width_mm": round(facing_width, 1),
        "slit_height_mm": round(slit_height, 1),
        "sleeve_construction": "dropped set-in; cap solved to armholes (ease 0)",
        "drafting": ("wide T-shaped fold-cut panels; keyhole neck as a narrow deep "
                     "CF opening finished by a shaped facing ring; side sewn underarm "
                     "to slit top; grown-on/T-cut noted as the traditional alternative"),
        "teaching_grade": ("a respectful, buildable draft of a heritage garment; the "
                           "keyhole throat finish and hand details are construction "
                           "choices, not separate pattern geometry"),
    }
    return pattern


result = build()
