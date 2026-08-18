"""
Crop top — FC-100 rank #75. Fashion Cabinet Garment Cartridge.

A cropped knit top: a tank or short tee whose hem sits at or above the waist.
Front and back cut on fold with light knit ease; the signature is BOUND edges —
neck and armhole (or sleeve-hem) binding strips whose lengths are derived from
the measured openings times a rib-stretch ratio, the construction rule encoded
rather than a fixed number. A `style` switch chooses a sleeveless tank crop
(bound armholes) or a short-sleeve crop (a set-in sleeve whose cap length is
solved numerically to the armhole).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|bindings|sleeve|set
style        = str(PARAM(lambda: style, "sleeveless"))   # sleeveless | short_sleeve

chest_girth    = float(PARAM(lambda: chest_girth, 940.0))
body_length    = float(PARAM(lambda: body_length, 380.0))   # nape line to CROPPED hem
neck_girth     = float(PARAM(lambda: neck_girth, 380.0))
knit_ease      = float(PARAM(lambda: knit_ease, 40.0))      # total; may go slightly negative
sleeve_length  = float(PARAM(lambda: sleeve_length, 110.0)) # cap apex to hem (sleeved style)
strap_width    = float(PARAM(lambda: strap_width, 40.0))    # shoulder width (sleeveless)
binding_ratio  = float(PARAM(lambda: binding_ratio, 0.90))  # rib length / opening
binding_width  = float(PARAM(lambda: binding_width, 12.0))  # finished binding height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps (mirror the manifest sliders exactly) ─────────────────────────────
if style not in ("sleeveless", "short_sleeve"):
    style = "sleeveless"
chest_girth = max(600.0, min(chest_girth, 1700.0))
body_length = max(300.0, min(body_length, 480.0))   # cropped: waist or above
neck_girth = max(300.0, min(neck_girth, 520.0))
knit_ease = max(-80.0, min(knit_ease, 200.0))
sleeve_length = max(60.0, min(sleeve_length, 260.0))
strap_width = max(24.0, min(strap_width, 90.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))
binding_width = max(8.0, min(binding_width, 25.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

SLEEVED = style == "short_sleeve"

W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
# Sleeveless crop scoops deeper (tank); a short-sleeve crop needs a shallower
# armhole to seat a set-in sleeve. Both scale with the graded chest.
AH = (chest_girth + knit_ease) / 8.0 + (105.0 if not SLEEVED else 85.0)
AH = max(150.0, min(AH, L - 60.0))
NW = max(55.0, neck_girth / 5.0 - (8.0 if not SLEEVED else 0.0))
HPS_Y = L + 20.0                             # high-point-shoulder line above nape
SHOULDER_DROP = 30.0
# Sleeveless straps end narrow near CF/CB; a sleeved crop keeps a full shoulder.
SH_X = (NW + strap_width) if not SLEEVED else (W - 5.0)
SH_END = fc.P(SH_X, HPS_Y - (12.0 if not SLEEVED else SHOULDER_DROP))
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 95.0
BACK_NECK_DROP = 28.0


def _armhole_edge():
    """Armhole curve, identical front/back (a scoop for tanks, a seated
    armscye for the short-sleeve style)."""
    if not SLEEVED:
        return fc.Edge(
            "armhole",
            [fc.Bezier(SH_END, fc.P(SH_END.x + 6.0, SH_END.y - AH * 0.45),
                       fc.P(W - AH * 0.28, UNDERARM.y + 14.0), UNDERARM)],
        )
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 14.0, SH_END.y - AH * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_piece(name, neck_drop, label):
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + neck_drop * 0.45), fc.P(NW, HPS_Y))],
    )
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    # Neck is always bound (allowance 0). Armhole is bound when sleeveless,
    # seamed to a sleeve when short-sleeve.
    allowances = {"hem": hem_allowance, "neck": 0.0}
    if not SLEEVED:
        allowances["armhole"] = 0.0
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances=allowances,
        notches=[fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.6, 40.0), fc.P(W * 0.6, max(60.0, L - 60.0))),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _binding(name, finished_len, label, quantity=1):
    """A straight rib strip, folded lengthwise when sewn. Its length is the
    measured opening times the rib ratio, plus joins — the encoded rule."""
    band_h = 2.0 * binding_width
    length = finished_len + 2.0 * seam_allowance
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,                          # length already includes joins
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def _build_sleeve(cap_target):
    """Short set-in sleeve; cap length solved by bisection to the armhole sum."""
    ch = max(40.0, AH * 0.32)                        # shallow knit cap
    sl = max(45.0, sleeve_length - ch)               # underarm-to-hem length
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(52):                              # cap length grows with hb
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
    chw = max(60.0, hb * 0.85)
    chw = min(chw, hb)
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
        allowances={"hem": 0.0},                     # sleeve hem is bound too
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Short Sleeve",
    )


def build():
    pattern = fc.PatternSet("crop-top")
    front = _body_piece("front", FRONT_NECK_DROP, "Front")
    back = _body_piece("back", BACK_NECK_DROP, "Back")

    want_front = target_piece in ("front", "set")
    want_back = target_piece in ("back", "set")
    want_neck = target_piece in ("neck_binding", "bindings", "set")
    want_arm = (not SLEEVED) and target_piece in ("armhole_binding", "bindings", "set")
    want_sleeve = SLEEVED and target_piece in ("sleeve", "set")
    if not (want_front or want_back or want_neck or want_arm or want_sleeve):
        # Unknown target: build everything appropriate to the style.
        want_front = want_back = want_neck = True
        want_arm = not SLEEVED
        want_sleeve = SLEEVED

    # Openings measured on the fold → full openings (front + back, both halves).
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()
    cap_target = armhole_opening  # sleeve cap sews into front + back armholes

    if want_front:
        pattern.add(front)
    if want_back:
        pattern.add(back)
    if want_neck:
        pattern.add(_binding("neck_binding", neck_opening * binding_ratio,
                             "Neck Binding (rib)"))
    if want_arm:
        # One cut-2 strip; each armhole opening (front+back curve of one side)
        # is bound by one strip, so length = single-armhole opening × ratio.
        pattern.add(_binding("armhole_binding", armhole_opening * binding_ratio,
                             "Armhole Binding (rib)", quantity=2))
    if want_sleeve:
        pattern.add(_build_sleeve(cap_target))

    # ── Declared seams (all must balance to delta ≈ 0) ───────────────────────
    if want_front and want_back:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if want_neck and want_front and want_back:
        # Neck binding (a folded rib strip) is stitched around the FULL
        # neckline while stretched by the rib ratio. The full neckline traverses
        # front-half + back-half twice around the body, so both on-fold neck
        # edges are referenced twice (edge lengths are summed) to give the true
        # opening. The strip is relaxed-shorter than the opening it seats into;
        # that intentional negative stretch is the seam's `ease`, leaving
        # delta ≈ 0.  len_a = opening·ratio + 2·SA ; len_b = opening.
        neck_ease = 2.0 * seam_allowance - neck_opening * (1.0 - binding_ratio)
        pattern.declare_seam(
            ("neck_binding", "bottom"),
            [("front", "neck"), ("back", "neck"), ("front", "neck"), ("back", "neck")],
            tol=2.0,
            ease=neck_ease,
        )
    if want_arm and want_front and want_back:
        # One armhole strip seats into one full armhole (its front curve + back
        # curve). Same stretched-binding rule as the neck.
        arm_ease = 2.0 * seam_allowance - armhole_opening * (1.0 - binding_ratio)
        pattern.declare_seam(
            ("armhole_binding", "bottom"),
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
            ease=arm_ease,
        )
    if want_sleeve and want_front and want_back:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                            # jersey-algodon card width
    body_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name in ("front", "back", "sleeve")
    )
    marker_len = body_area / (fabric_width * 0.70) if body_area > 0 else 0.0
    neck_strip_mm = round(neck_opening * binding_ratio + 2.0 * seam_allowance)
    arm_strip_mm = round(armhole_opening * binding_ratio + 2.0 * seam_allowance)
    pattern.bom = [
        {"item": "jersey-algodon (cotton/elastane single knit)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cropped body{' + short sleeves' if SLEEVED else ''}; "
                 f"at {fabric_width:.0f} mm width, 70% marker efficiency"},
        {"item": "self-fabric binding, neck",
         "qty": neck_strip_mm, "unit": "mm_length",
         "note": f"cut {2.0 * binding_width:.0f} mm wide × {neck_strip_mm} mm long "
                 f"(neckline {round(neck_opening)} mm × {binding_ratio:.2f} ratio + joins)"},
    ]
    if SLEEVED:
        sleeve_hem_mm = 0
        for p in pattern.pieces:
            if p.name == "sleeve":
                sleeve_hem_mm = round(p.edge("hem").length())
        pattern.bom.append(
            {"item": "self-fabric binding, sleeve hems",
             "qty": round(2.0 * sleeve_hem_mm * binding_ratio + 4.0 * seam_allowance),
             "unit": "mm_length",
             "note": f"2 sleeve hems, each {sleeve_hem_mm} mm × {binding_ratio:.2f} ratio; "
                     f"optional — sleeve hems may be turned instead"})
    else:
        pattern.bom.append(
            {"item": "self-fabric binding, armholes",
             "qty": round(2.0 * arm_strip_mm), "unit": "mm_length",
             "note": f"2 armhole strips, each {2.0 * binding_width:.0f} mm wide × "
                     f"{arm_strip_mm} mm long (armhole {round(armhole_opening)} mm × "
                     f"{binding_ratio:.2f} ratio + joins)"})
    pattern.bom.append(
        {"item": "polyester thread + ballpoint/stretch needle", "qty": 1, "unit": "set",
         "note": "stretch or coverstitch on bound edges; 75/11 ballpoint. "
                 "No hardware — this is an all-knit, notion-free garment."})

    # ── Metadata ───────────────────────────────────────────────────────────────
    pattern.metadata = {
        "fc100_rank": 75,
        "fabric_hint": "jersey-algodon",
        "style": style,
        "cropped_length_mm": round(L, 1),
        "knit_ease_mm": round(knit_ease, 1),
        "binding_ratio": binding_ratio,
        "neck_opening_mm": round(neck_opening, 1),
        "armhole_opening_mm": round(armhole_opening, 1),
        "neck_binding_cut_mm": neck_strip_mm,
        "armhole_binding_cut_mm": (None if SLEEVED else arm_strip_mm),
        "drafting": (
            "cropped knit top; hem at/above waist, light knit ease. Neck bound; "
            "armholes bound (sleeveless) or set into a solved short sleeve. "
            "Teaching-grade: straight rib strips (real ribbing is cut narrower and "
            "eased by the ratio); bound edges use 0 seam allowance."
        ),
    }
    return pattern


result = build()
