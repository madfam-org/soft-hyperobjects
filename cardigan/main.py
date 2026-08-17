"""
Cardigan — FC-100 rank #39. Fashion Cabinet Garment Cartridge.

Button-front CUT-AND-SEW knitwear: the crewneck sweater (rank #38) opened
down the center front. The front becomes TWO mirrored halves — never on
fold — whose straight center edge takes a folded BUTTON BAND (cut 2, one
per side): band length is the MEASURED center edge plus end allowances,
verified as a declared seam with ease. Five buttonhole crosses are marked
on the band; mark both bands, work buttonholes on one, sew buttons to the
other. The V-ish front neck (160 mm drop, gentle curve) meets the band
top. Long sleeve cap stays SOLVED by bisection against the measured
armhole pair; cuffs and split hem band derive from measured openings times
sweater-rib recovery ratios. Shoulders carry the knitwear tape marking.

Honest scope note: the FC-100 index asks knitout_or_cut_and_sew for this
slot. This cartridge is the cut-and-sew branch; the fully-fashioned
machine-knit (Knitout) version is future work. Button hardware is a
Yantra4D solid, federated through the shank-button notion cartridge.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|band|ribs|set

chest_girth   = float(PARAM(lambda: chest_girth, 1000.0))
body_length   = float(PARAM(lambda: body_length, 680.0))    # nape to hem-band seam
neck_girth    = float(PARAM(lambda: neck_girth, 390.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))  # apex to cuff seam; LONG
cardigan_ease = float(PARAM(lambda: cardigan_ease, 140.0))  # roomier than the crewneck
band_width    = float(PARAM(lambda: band_width, 28.0))      # finished button-band width
cuff_ratio    = float(PARAM(lambda: cuff_ratio, 0.72))
hemband_ratio = float(PARAM(lambda: hemband_ratio, 0.88))
cuff_height    = float(PARAM(lambda: cuff_height, 65.0))
hemband_height = float(PARAM(lambda: hemband_height, 50.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 950.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(200.0, min(sleeve_length, 760.0))
cardigan_ease = max(60.0, min(cardigan_ease, 350.0))
band_width = max(15.0, min(band_width, 45.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
hemband_ratio = max(0.70, min(hemband_ratio, 1.0))

W = (chest_girth + cardigan_ease) / 4.0
L = body_length
AH = (chest_girth + cardigan_ease) / 8.0 + 85.0       # crewneck's set-in-feel armhole
AH = max(180.0, min(AH, L - 100.0))
NW = max(62.0, neck_girth / 5.0 + 2.0)
HPS_Y = L + 20.0
SHOULDER_DROP = 30.0
SH_END = fc.P(W - 5.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)
FRONT_NECK_DROP = 160.0                               # V-ish open front neck
BACK_NECK_DROP = 20.0
TAPE_INSET = 6.0                                      # tape guide offset from stitch line
BUTTON_COUNT = 5
CROSS_ARM = 4.0                                       # buttonhole cross half-arm


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _shoulder_tape():
    """Seam-stabilization guide just inside the shoulder edge — knits grow."""
    a, b = fc.P(NW, HPS_Y), SH_END
    along = (b - a).normalized()
    inward = fc.P(along.y, -along.x)                  # shoulder runs right+down → into body
    return fc.Internal(
        "tape shoulder seam",
        [a + (along + inward) * TAPE_INSET, b + (inward - along) * TAPE_INSET],
    )


def _neck_edge(neck_drop):
    """V-ish front neck: a gentle, near-chord curve from band top to shoulder."""
    neck_top_y = HPS_Y - neck_drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y),
                   fc.P(NW * 0.25, neck_top_y + neck_drop * 0.30),
                   fc.P(NW * 0.62, HPS_Y - neck_drop * 0.32),
                   fc.P(NW, HPS_Y))],
    )


def _crew_neck_edge(neck_drop):
    """Shallow scooped back neck, unchanged from the crewneck block."""
    neck_top_y = HPS_Y - neck_drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )


def _body_edges(neck):
    origin = fc.P(0.0, 0.0)
    return [
        fc.Edge("center", [fc.Line(origin, neck.start)]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge takes the band."""
    return fc.Piece(
        "front",
        _body_edges(_neck_edge(FRONT_NECK_DROP)),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=[_shoulder_tape()],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (half)",
    )


def build_back():
    return fc.Piece(
        "back",
        _body_edges(_crew_neck_edge(BACK_NECK_DROP)),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        internals=[_shoulder_tape()],
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
    chw = max(90.0, hb * 0.62)                         # tapers into the deep cuff
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


def _buttonhole_crosses(length, band_h):
    """Five drill crosses on the finished face half of the folded band."""
    y = band_h * 0.25
    inset = seam_allowance + 40.0
    span = max(length - 2.0 * inset, 10.0)
    marks = []
    for i in range(BUTTON_COUNT):
        x = inset + span * i / (BUTTON_COUNT - 1)
        label = f"buttonhole {i + 1}"
        marks.append(fc.Internal(label, [fc.P(x - CROSS_ARM, y - CROSS_ARM),
                                         fc.P(x + CROSS_ARM, y + CROSS_ARM)], kind="drill"))
        marks.append(fc.Internal(label, [fc.P(x - CROSS_ARM, y + CROSS_ARM),
                                         fc.P(x + CROSS_ARM, y - CROSS_ARM)], kind="drill"))
    return marks


def build_band(center_len):
    """Button band, cut 2: length = measured front center edge + end allowances.

    Folded double along its long axis (width 2 × finished). Mark the five
    buttonhole crosses on BOTH bands; work buttonholes on one, sew shank
    buttons through the crosses on the other.
    """
    band_h = 2.0 * band_width
    length = center_len + 2.0 * seam_allowance
    internals = [fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                           fc.P(length, band_h / 2.0)])]
    internals.extend(_buttonhole_crosses(length, band_h))
    return fc.Piece(
        "band",
        [
            fc.Edge("long_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("fold", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Button Band",
    )


def _rib(name, finished_len, finished_height, qty, label, notches=None):
    band_h = 2.0 * finished_height                     # folded when sewn
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
    pattern = fc.PatternSet("cardigan")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    sleeve = build_sleeve(cap_target)
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "band":
        pattern.add(build_band(front.edge("center").length()))
    if everything or target_piece == "ribs":
        cuff_circ = sleeve.edge("hem").length()
        hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
        pattern.add(_rib("cuff", cuff_circ * cuff_ratio, cuff_height, 2, "Cuff (rib)"))
        # The hem band is SPLIT for the open front: cut flat, ends open at the
        # band edges; the center notch (= center back when worn) marks the fold.
        cb_notch = fc.Notch("bottom", 0.5, "center back; open ends meet the bands")
        pattern.add(_rib("hem_band", hem_circ * hemband_ratio, hemband_height, 1,
                         "Hem Band (split rib)", notches=[cb_notch]))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve still meets
        # exactly ONE front armhole + ONE back armhole — the drafted pair.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
        # One band sews to one front's center edge; the band carries the end
        # allowances (hem seam + neck turn-in), hence the declared ease.
        pattern.declare_seam([("band", "long_edge")], [("front", "center")],
                             tol=2.0, ease=2.0 * seam_allowance)
    pattern.metadata = {
        "fc100_rank": 39,
        "fabric_hint": "felpa-algodon",
        "knit_note": "cut-and-sew branch; fully-fashioned future",
        "button_count": BUTTON_COUNT,
        "button_note": "shank buttons via shank-button notion cartridge; "
                       "mark both bands, work buttonholes on one",
        "rib_ratios": {"cuff": cuff_ratio, "hem": hemband_ratio},
        "drafting": "crewneck-sweater block split at CF; measured-length button "
                    "bands; taped shoulders; ribs derived from openings",
    }
    return pattern


result = build()
