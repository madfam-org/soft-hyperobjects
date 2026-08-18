"""
Kurta — FC-100 rank #97. Fashion Cabinet Garment Cartridge.

A long, straight, loose tunic of the heritage-global family — the traditional
South Asian kurta, worn by men and women across South Asia (India, Pakistan,
Bangladesh, Nepal, Sri Lanka) and the wider diaspora. This draft encodes its
three signatures respectfully:

  - BAND COLLAR (the signature): a MANDARIN / band collar — a standing collar
    band with no fall — solved by bisection to the measured neckline
    (collar-band method): its neck edge is drafted flat, then its length is
    bisected to (front.neck + back.neck) per garment half plus the small CF
    closure overlap, so the neck seam matches to floating-point precision
    (delta ≈ 0). The classic kurta neckline.
  - PLACKET (the signature): a short CENTRE-FRONT neck placket — a partial
    front opening from the neckline down the chest, closed by buttons or ties.
    On the fold-cut front it is marked as a slit box (the two placket edges and
    a bottom bar) with buttonhole crosses; a separate PLACKET FACING strip
    backs and finishes the slash. Buttons/ties are a Yantra4D hardware ref.
  - SIDE SLITS (chaak, the signature): the lower side seams are OPEN from the
    slit top down to the hem, essential for movement. The side seam is sewn
    only from the underarm down to a notched slit top; below the notch the
    seam opens as the chaak. Both side edges are marked with the slit-top notch.

Long straight sleeves by default (a `sleeve` select offers a short sleeve),
a straight relaxed body, a straight hem, and an optional chest patch pocket
(traced) — all typical of the kurta. Real kurtas span cotton poplin → fine
silk; this draft uses a light cotton (popelina-algodon / manta-cruda).

Honest simplifications (teaching-grade — see docs/README.md):
  - The neckline where the band attaches is a plain round neckline; the placket
    is a partial CF slash finished by the facing strip. The slash itself is an
    internal marking on the fold-cut front (its two cut edges are a construction
    detail, like the henley/polo placket), not separate outline geometry.
  - A simple set-in sleeve is drafted (cap solved to the armholes at ease 0).
    The traditional grown-on / gusseted cut is noted as the alternative.
  - Straight hem and straight side (a gentle A-line flare is offered); the
    chaak side slit is a notch + construction note, not a split panel edge.

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
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|sleeve|collar|placket|pocket|set

sleeve_style = str(PARAM(lambda: sleeve_style, "long"))  # long | short

chest_girth    = float(PARAM(lambda: chest_girth, 1040.0))
kurta_length   = float(PARAM(lambda: kurta_length, 1020.0))  # nape to finished hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 600.0))  # cap apex to opening
woven_ease     = float(PARAM(lambda: woven_ease, 180.0))     # total relaxed ease
placket_length = float(PARAM(lambda: placket_length, 240.0))  # CF neck point down
placket_width  = float(PARAM(lambda: placket_width, 32.0))   # finished placket width
collar_height  = float(PARAM(lambda: collar_height, 40.0))   # mandarin band height
collar_overlap = float(PARAM(lambda: collar_overlap, 15.0))  # CF closure extension
side_flare     = float(PARAM(lambda: side_flare, 40.0))      # hem beyond chest line
slit_height    = float(PARAM(lambda: slit_height, 300.0))    # chaak top above hem
wrist_opening  = float(PARAM(lambda: wrist_opening, 260.0))  # sleeve opening (flat×2)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1800.0))
kurta_length = max(760.0, min(kurta_length, 1300.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
sleeve_length = max(180.0, min(sleeve_length, 720.0))
woven_ease = max(100.0, min(woven_ease, 420.0))
placket_length = max(120.0, min(placket_length, 380.0))
placket_width = max(20.0, min(placket_width, 50.0))
collar_height = max(25.0, min(collar_height, 60.0))
collar_overlap = max(0.0, min(collar_overlap, 40.0))
side_flare = max(0.0, min(side_flare, 200.0))
slit_height = max(0.0, min(slit_height, 500.0))
wrist_opening = max(160.0, min(wrist_opening, 380.0))

# ── Straight kurta block (woven, fold at CF/CB, relaxed drop shoulder) ────────
W = (chest_girth + woven_ease) / 4.0          # quarter body width (fold at CF/CB)
L = kurta_length                              # hem at y=0, nape line at y=L
AH = (chest_girth + woven_ease) / 8.0 + 100.0  # relaxed armhole depth
AH = max(180.0, min(AH, L - 140.0))
NW = max(62.0, neck_girth / 5.0 + 2.0)        # half neck width on the fold
HPS_Y = L + 20.0                              # high point shoulder above nape line
SHOULDER_DROP = 30.0                          # relaxed dropped shoulder
BACK_NECK_DROP = 22.0                         # HPS to CB nape
FRONT_NECK_DROP = max(70.0, neck_girth / 5.0 + 18.0)  # round band-collar front scoop
CF_NECK_Y = HPS_Y - FRONT_NECK_DROP           # CF neck point (placket top)
CB_NECK_Y = HPS_Y - BACK_NECK_DROP
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)  # shoulder tip (armhole top)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)  # underarm point at the side
HEM_SIDE = fc.P(W + side_flare, 0.0)          # side/hem corner (gentle A-line)

# Placket must sit below the neckline; keep its bottom clear of the hem region.
placket_length = min(placket_length, CF_NECK_Y - 120.0)
placket_length = max(placket_length, 100.0)

# Side slit (chaak): the side seam is sewn only underarm → slit top.
slit_height = min(slit_height, UNDERARM.y - 80.0)
slit_height = max(slit_height, 0.0)

# Sleeve style select changes the default reach only when the user left it long.
COLLAR_NECK_RISE = 14.0                        # band collar neck-edge curl
POCKET_W, POCKET_H = 120.0, 130.0
FABRIC_WIDTH = 1450.0                          # popelina-algodon card width (mm)


# ── Shared edges ─────────────────────────────────────────────────────────────
def _armhole_edge():
    """Shared front/back armhole (relaxed drop-shoulder wovens keep them equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _side_notches():
    """The chaak slit-top notch on the side edge (arc fraction from UNDERARM)."""
    if slit_height <= 0.0:
        return []
    side_len = UNDERARM.distance(HEM_SIDE)
    # side edge runs UNDERARM (t=0) → HEM_SIDE (t=1); slit top is slit_height up.
    t_slit = 1.0 - slit_height / side_len
    t_slit = max(0.0, min(1.0, t_slit))
    return [fc.Notch("side", t_slit, "chaak slit top")]


def _buttonhole_cross(cx, cy, i, half=5.0):
    """A '+' drill mark drawn as one polyline (return strokes retrace the bars)."""
    pts = [fc.P(cx - half, cy), fc.P(cx + half, cy), fc.P(cx, cy),
           fc.P(cx, cy + half), fc.P(cx, cy - half)]
    return fc.Internal(f"placket buttonhole {i}", pts, kind="drill")


def _placket_internals():
    """CF placket slash box on the fold-cut front.

    The CF-side line rides the fold (x=0, the slash opens on centre); the second
    line sits placket_width away; a bottom bar closes the box. Buttonhole crosses
    space evenly down the box centreline. The kurta placket typically carries a
    handful of small buttons or a neck tie.
    """
    y_top, y_bot = CF_NECK_Y, CF_NECK_Y - placket_length
    n_buttons = max(3, min(6, int(placket_length / 60.0) + 1))
    marks = [
        fc.Internal("placket edge (CF fold)", [fc.P(0.0, y_top), fc.P(0.0, y_bot)]),
        fc.Internal("placket edge", [fc.P(placket_width, y_top),
                                     fc.P(placket_width, y_bot)]),
        fc.Internal("placket bottom", [fc.P(0.0, y_bot),
                                       fc.P(placket_width, y_bot)]),
    ]
    for i in range(1, n_buttons + 1):
        cy = y_top - placket_length * i / (n_buttons + 1.0)
        marks.append(_buttonhole_cross(placket_width / 2.0, cy, i))
    return marks


def _pocket_trace():
    """Optional chest patch-pocket placement (wearer's left once mirrored)."""
    top = max(200.0, min(UNDERARM.y + 40.0, CF_NECK_Y - placket_length - 30.0))
    top = max(top, 220.0)
    bottom = max(top - POCKET_H, 60.0)
    left = max(placket_width + 40.0, W * 0.34)
    right = min(left + POCKET_W, W * 0.94)
    return fc.Internal(
        "chest pocket placement",
        [fc.P(left, top), fc.P(right, top), fc.P(right, bottom),
         fc.P(left, bottom), fc.P(left, top)],
        kind="trace",
    )


def build_front():
    """Front cut 1 on fold at CF: round band-collar neckline, CF placket slash."""
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CF_NECK_Y), fc.P(NW * 0.55, CF_NECK_Y),
                   fc.P(NW, CF_NECK_Y + FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, CF_NECK_Y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, HEM_SIDE)]),
        fc.Edge("hem", [fc.Line(HEM_SIDE, origin)]),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},
        notches=_side_notches() + [fc.Notch("armhole", 0.5, "front armhole")],
        grainline=fc.Grainline(fc.P(W * 0.55, 90.0), fc.P(W * 0.55, L - 140.0)),
        internals=_placket_internals() + [_pocket_trace()],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (placket)",
    )


def build_back():
    """Back cut 1 on fold at CB: shallow round neckline, otherwise the front's twin."""
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, CB_NECK_Y), fc.P(NW * 0.55, CB_NECK_Y),
                   fc.P(NW, CB_NECK_Y + BACK_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, CB_NECK_Y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, HEM_SIDE)]),
        fc.Edge("hem", [fc.Line(HEM_SIDE, origin)]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},
        notches=_side_notches() + [fc.Notch("armhole", 0.5, "back armhole")],
        grainline=fc.Grainline(fc.P(W * 0.55, 90.0), fc.P(W * 0.55, L - 140.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L.

    Cap length grows monotonically with the half-base `hb` — bisect on it.
    """
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Straight set-in sleeve; cap solved by bisection to the armhole sum (ease 0)."""
    reach = sleeve_length
    if sleeve_style == "short":
        reach = min(reach, 250.0)
    ch = max(60.0, AH * 0.32)                        # cap height
    sl = max(120.0, reach - ch)                      # underarm-to-opening length
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
    chw = max(80.0, min(wrist_opening / 2.0, hb - 8.0))  # half opening (slight taper)
    label = "Sleeve (short)" if sleeve_style == "short" else "Sleeve (long)"
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
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.55)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def _collar_neck_edge(flat):
    """Mandarin band collar neck edge: shallow curve solved to the half neckline."""
    return fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, COLLAR_NECK_RISE),
                          bulge=0.05, side=-1.0)],
    )


def build_collar(half_target):
    """Mandarin / band collar, half on fold at CB — the collar-band method.

    Neck edge bisected to half_target = front.neck + back.neck (per garment
    half) + the CF closure overlap. A standing band with no fall: the front
    edge rises straight, the top runs level back to the CB fold. The band
    closes at CF where the placket opens (button or hook), ease = overlap.
    """
    lo, hi = half_target * 0.7, half_target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _collar_neck_edge(mid).length(0.05) < half_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck_edge(flat).length(0.05) - half_target) > 1.0:
        raise ValueError("band collar neck-edge solver did not converge")
    neck = _collar_neck_edge(flat)
    top_start = fc.P(0.0, collar_height)
    top_end = fc.P(flat, COLLAR_NECK_RISE + collar_height)
    t_cf = half_target - collar_overlap
    t_cf = max(0.02, min(0.98, t_cf / half_target))  # CF closure line along the neck
    piece = fc.Piece(
        "collar",
        [
            neck,
            fc.Edge("front_edge", [fc.Line(fc.P(flat, COLLAR_NECK_RISE), top_end)]),
            fc.Edge("top",
                    [fc.curve_through(top_end, top_start, bulge=0.04, side=1.0)]),
            fc.Edge("cb", [fc.Line(top_start, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder match"),
                 fc.Notch("neck", t_cf, "CF / closure line")],
        grainline=fc.Grainline(fc.P(flat * 0.2, collar_height * 0.5),
                               fc.P(flat * 0.75, collar_height * 0.5
                                    + COLLAR_NECK_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cb", mirror=True),
        label="Band Collar (mandarin, half on fold)",
    )
    return piece, flat


def build_placket():
    """Placket facing strip that backs and finishes the CF slash.

    Cut doubled (upper + under placket in construction). The strip is
    (placket_length + turn) tall and (2 × placket_width) wide, carrying the CF
    slash line as an internal so it registers to the front's marked box. Its
    dimensions are derived from the placket parameters, not seam-declared
    against the front slash (the slash is an internal on the fold-cut front,
    like the henley/polo placket).
    """
    w = 2.0 * placket_width
    h = placket_length + 40.0
    return fc.Piece(
        "placket",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("side_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},          # neck edge joins the collar seam
        grainline=fc.Grainline(fc.P(w * 0.3, h * 0.12), fc.P(w * 0.3, h * 0.88)),
        internals=[fc.Internal(
            "CF slash line",
            [fc.P(w / 2.0, h), fc.P(w / 2.0, h - placket_length)],
        )],
        cut=fc.CutSpec(quantity=2),
        label="Placket facing (cut 2)",
    )


def build():
    pattern = fc.PatternSet("kurta")
    front = build_front()
    back = build_back()
    cap_target = (front.edge("armhole").length(0.05)
                  + back.edge("armhole").length(0.05))
    half_neck = front.edge("neck").length(0.05) + back.edge("neck").length(0.05)
    half_target = half_neck + collar_overlap

    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "collar": target_piece in ("collar", "set"),
        "placket": target_piece in ("placket", "set"),
        "pocket": target_piece in ("pocket", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    collar_flat = None
    if wanted["collar"]:
        collar, collar_flat = build_collar(half_target)
        pattern.add(collar)
    if wanted["placket"]:
        pattern.add(build_placket())
    if wanted["pocket"]:
        # A standalone chest patch pocket piece (the front carries its trace).
        pattern.add(build_pocket())

    # ── Declared seams (fail-closed; each must balance within tol) ────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Side seam: sewn underarm → chaak slit top (notched); balances full length.
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
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        # Band collar neck edge ↔ half neckline (front.neck + back.neck), the
        # CF closure overlap is the intentional extra length (ease) on the band.
        pattern.declare_seam(
            [("collar", "neck")],
            [("front", "neck"), ("back", "neck")],
            tol=2.0,
            ease=collar_overlap,
        )

    # ── Bill of materials ─────────────────────────────────────────────────────
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (FABRIC_WIDTH * 0.62)   # long straight panels nest loose
    n_buttons = max(3, min(6, int(placket_length / 60.0) + 1))
    pattern.bom = [
        {"item": "popelina-algodon", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": (f"light cotton at {FABRIC_WIDTH:.0f} mm width, 62% marker "
                  "efficiency; production kurtas span cotton poplin → fine silk, "
                  "manta-cruda is the muslin/khadi-look alternative")},
        {"item": "fusible interfacing (collar band + placket)", "qty": 1,
         "unit": "set",
         "note": "band cut doubled on fold (upper + under); placket strip fused "
                 "so the mandarin collar and slash stay crisp"},
        {"item": "kurta buttons or neck tie", "qty": n_buttons, "unit": "pieces",
         "note": (f"{n_buttons} small placket buttons (or a self/contrast neck "
                  "tie); hard goods federate to the Yantra4D button family "
                  "(notion.hardware_ref), never re-implemented in the kernel")},
        {"item": "polyester or cotton thread + universal 80/12 needle", "qty": 1,
         "unit": "set", "note": "sharp needle for poplin; finer for silk variants"},
    ]

    pattern.metadata = {
        "fc100_rank": 97,
        "fabric_hint": "popelina-algodon",
        "heritage_note": (
            "The kurta is a traditional South Asian tunic worn by men and women "
            "across India, Pakistan, Bangladesh, Nepal, Sri Lanka and the wider "
            "diaspora; drafted here respectfully as a teaching-grade block."
        ),
        "quarter_width_mm": round(W, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "neck_opening_full_mm": round(2.0 * half_neck, 1),
        "collar_style": "mandarin / band (standing band, no fall)",
        "collar_half_target_mm": round(half_target, 1),
        "collar_flat_mm": None if collar_flat is None else round(collar_flat, 1),
        "collar_height_mm": round(collar_height, 1),
        "collar_overlap_mm": round(collar_overlap, 1),
        "placket_box_mm": [round(placket_length, 1), round(placket_width, 1)],
        "placket_buttons": n_buttons,
        "slit_height_mm": round(slit_height, 1),
        "side_flare_mm": round(side_flare, 1),
        "sleeve_style": sleeve_style,
        "sleeve_cap_solved_mm": None,  # filled below if the sleeve was built
        "drafting": (
            "straight fold-cut kurta block; round band-collar neckline with the "
            "mandarin band solved by bisection to the measured neckline "
            "(collar-band method, ease = closure overlap); partial CF placket as "
            "a marked slash + separate facing strip; side seam sewn underarm to "
            "the chaak slit top, open below; set-in sleeve cap solved by bisection"
        ),
        "teaching_grade": (
            "a respectful, buildable draft of a heritage garment; the band collar, "
            "placket slash finish, and chaak side slit are construction detail "
            "layered on a simple straight tunic block, not couture geometry"
        ),
    }
    # Record the solved sleeve cap length when the sleeve is present.
    for p in pattern.pieces:
        if p.name == "sleeve":
            pattern.metadata["sleeve_cap_solved_mm"] = round(
                p.edge("cap").length(0.05), 1
            )
    return pattern


def build_pocket():
    """Chest patch pocket as a real cut piece (kurta patch pocket)."""
    flap = 20.0                                    # angled bottom point drop
    return fc.Piece(
        "pocket",
        [
            fc.Edge("top", [fc.Line(fc.P(0.0, POCKET_H), fc.P(POCKET_W, POCKET_H))]),
            fc.Edge("side_r", [fc.Line(fc.P(POCKET_W, POCKET_H),
                                       fc.P(POCKET_W, flap))]),
            fc.Edge("point_r", [fc.Line(fc.P(POCKET_W, flap),
                                        fc.P(POCKET_W / 2.0, 0.0))]),
            fc.Edge("point_l", [fc.Line(fc.P(POCKET_W / 2.0, 0.0),
                                        fc.P(0.0, flap))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, flap), fc.P(0.0, POCKET_H))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},         # top hem folds to the inside
        grainline=fc.Grainline(fc.P(POCKET_W * 0.5, 25.0),
                               fc.P(POCKET_W * 0.5, POCKET_H - 20.0)),
        internals=[fc.Internal("fold line (top facing)",
                               [fc.P(0.0, POCKET_H - hem_allowance - 12.0),
                                fc.P(POCKET_W, POCKET_H - hem_allowance - 12.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Chest Pocket",
    )


result = build()
