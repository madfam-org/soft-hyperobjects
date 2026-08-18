"""
Baby bodysuit (onesie) — FC-100 rank #92. Fashion Cabinet Garment Cartridge.

The classic infant bodysuit: a soft cotton-jersey tee bodice whose front and
back BOTH extend below the waist into a rounded CROTCH FLAP. The two flaps
overlap and close with SNAP FASTENERS (no sewn crotch seam), and the shoulders
are a LAP-SHOULDER / ENVELOPE neckline so the neck stretches wide to pull over
a baby's head. Two signatures make this garment infant-specific:

  * ENVELOPE NECK — the front and back neck are cut wide and the shoulders lap
    (front shoulder crosses over the back at a marked overlap), so the opening
    can stretch far past the head girth. The neckline is finished with a bound
    knit binding derived from the measured opening times a stretch ratio.
  * SNAP CROTCH — the front and back crotch flaps are drafted to the SAME
    rounded tip so their leg openings and crotch edges match by construction;
    they overlap by a marked lap depth and close with ~3 snaps. Snap positions
    are marked internal (drill crosses); the snap hardware is a Yantra4D notion
    reference, never re-implemented here.

The sleeve cap length is SOLVED numerically to match the front + back armholes
(the t-shirt-crew idiom), the neck and leg bindings are derived bands, and all
sewn seams balance to delta ~ 0. `sleeve_style` picks short | long | sleeveless.

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
_KNOWN = ("front", "back", "sleeve", "neck_binding", "leg_binding", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

# Infant proportions default to roughly a 6–12 month size.
chest_girth   = float(PARAM(lambda: chest_girth, 500.0))    # full chest girth
back_length   = float(PARAM(lambda: back_length, 260.0))    # nape to waist line
neck_girth    = float(PARAM(lambda: neck_girth, 260.0))     # head must pass this
head_girth    = float(PARAM(lambda: head_girth, 460.0))     # the pull-over check
crotch_ext    = float(PARAM(lambda: crotch_ext, 150.0))     # waist down to crotch tip
sleeve_length = float(PARAM(lambda: sleeve_length, 90.0))   # cap apex to hem
sleeve_style  = str(PARAM(lambda: sleeve_style, "short"))   # short|long|sleeveless
knit_ease     = float(PARAM(lambda: knit_ease, 50.0))       # total, comfy for babies
crotch_width  = float(PARAM(lambda: crotch_width, 110.0))   # flat width at snap line
lap_depth     = float(PARAM(lambda: lap_depth, 30.0))       # snap overlap of the flaps
binding_ratio = float(PARAM(lambda: binding_ratio, 0.82))   # binding length / opening
binding_width = float(PARAM(lambda: binding_width, 12.0))   # finished binding height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(380.0, min(chest_girth, 720.0))
back_length = max(180.0, min(back_length, 380.0))
neck_girth = max(200.0, min(neck_girth, 340.0))
head_girth = max(360.0, min(head_girth, 560.0))
crotch_ext = max(90.0, min(crotch_ext, 240.0))
sleeve_length = max(40.0, min(sleeve_length, 260.0))
if sleeve_style not in ("short", "long", "sleeveless"):
    sleeve_style = "short"
knit_ease = max(20.0, min(knit_ease, 160.0))
crotch_width = max(70.0, min(crotch_width, 160.0))
lap_depth = max(15.0, min(lap_depth, 55.0))
binding_ratio = max(0.70, min(binding_ratio, 1.0))
binding_width = max(8.0, min(binding_width, 24.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))
hem_allowance = max(0.0, min(hem_allowance, 30.0))

# ── Derived block dimensions ─────────────────────────────────────────────────
W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
CH = W                                        # crotch half-width at the snap line
CHW = crotch_width / 2.0                      # half the flat crotch width at the tip
WAIST_Y = crotch_ext                          # waist line sits above the crotch tip
L = WAIST_Y + back_length                     # crotch tip (y=0) to nape line
AH = (chest_girth + knit_ease) / 8.0 + 55.0   # armhole depth (infant-scaled)
AH = max(90.0, min(AH, back_length - 40.0))
# Envelope neck: wider half-neck than an adult tee so it stretches over the head.
NW = max(55.0, neck_girth / 4.2)              # half neck width on the fold
HPS_Y = L + 12.0                              # high point shoulder above the nape
SHOULDER_DROP = 16.0                          # infant shoulder slope
FRONT_NECK_DROP = 55.0                        # deep front scoop (envelope)
BACK_NECK_DROP = 18.0                         # shallow back scoop
SH_END = fc.P(W - 4.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Shared front/back armhole curve (drop-shoulder infant tee → equal)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 10.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _leg_edge(waist_x):
    """Curved leg opening: from the side/underarm line down and in to the
    rounded crotch tip. Authored top→bottom (side down to the crotch tip).
    Both front and back use the SAME curve so the leg bindings match and the
    flaps stack for the snaps."""
    top = fc.P(waist_x, WAIST_Y)                     # where the side meets the leg
    tip = fc.P(CHW, 0.0)                             # crotch tip (bottom)
    return fc.Edge(
        "leg",
        [fc.Bezier(top, fc.P(waist_x - 6.0, WAIST_Y - crotch_ext * 0.45),
                   fc.P(CH * 0.80, crotch_ext * 0.28), tip)],
    )


def _body_piece(name, neck_edge, neck_top_y, snap_internals, label):
    """A tee bodice (cut on fold) that runs past the waist into a rounded
    crotch flap. Outline from the fold, CCW after normalization:
      center(fold) → neck → shoulder → armhole → side → leg → crotch(tip)."""
    origin = fc.P(0.0, 0.0)                           # crotch tip on the fold
    # The side runs straight from the underarm down to the waist line, where the
    # curved leg opening takes over.
    waist_x = W
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(waist_x, WAIST_Y))]),
        _leg_edge(waist_x),
        fc.Edge("crotch", [fc.Line(fc.P(CHW, 0.0), origin)]),
    ]
    # Elastic/binding notch on the leg + the lap line marked internal.
    lap_line = fc.Internal(
        "snap lap line",
        [fc.P(0.0, lap_depth), fc.P(CHW, lap_depth)],
        kind="trace",
    )
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"crotch": hem_allowance},
        notches=[fc.Notch("side", 0.5, f"{name} side match"),
                 fc.Notch("armhole", 0.5, f"{name} armhole"),
                 fc.Notch("leg", 0.5, f"{name} leg quarter")],
        grainline=fc.Grainline(fc.P(W * 0.5, 25.0), fc.P(W * 0.5, L - 60.0)),
        internals=[lap_line] + snap_internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    cf_neck_y = HPS_Y - FRONT_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cf_neck_y), fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + FRONT_NECK_DROP * 0.45), fc.P(NW, HPS_Y))],
    )
    return _body_piece("front", neck, cf_neck_y, _snap_internals(), "Front (to crotch flap)")


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), fc.P(NW, HPS_Y), bulge=0.12, side=-1.0)],
    )
    return _body_piece("back", neck, cb_neck_y, _snap_internals(), "Back (to crotch flap)")


def _snap_internals():
    """~3 crotch snaps marked as drill crosses along the snap (lap) line.
    Snap hardware is a Yantra4D notion reference, not drafted here."""
    marks = []
    n = 3
    y = lap_depth * 0.5                               # snaps sit on the lap band
    for i in range(n):
        # Spread the snaps across the flat crotch width (mirrored on the fold).
        x = CHW * (i + 0.5) / n
        marks.append(fc.Internal(f"snap-{i + 1}",
                     [fc.P(x, y - 4.0), fc.P(x, y + 4.0)], kind="drill"))
        marks.append(fc.Internal(f"snap-{i + 1}-x",
                     [fc.P(x - 4.0, y), fc.P(x + 4.0, y)], kind="drill"))
    return marks


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    ch = max(28.0, AH * 0.32)                         # shallow knit cap
    sl = max(30.0, sleeve_length - ch)                # underarm-to-hem length
    lo, hi = 12.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(52):                               # bisect: cap length grows with hb
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
    chw = hb * 0.86                                   # cuff half-width
    chw = max(40.0, min(chw, hb))
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
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, sl + ch * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (short)",
    )


def _binding(name, opening_len, quantity, label):
    """Derived knit binding strip: (opening x stretch ratio) + 2 sa ends, cut
    at 2x the finished width so it folds around the raw edge. The strip length
    already includes the joins, so seam_allowance=0 on the piece."""
    band_len = opening_len * binding_ratio + 2.0 * seam_allowance
    band_h = 2.0 * binding_width
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("baby-bodysuit")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)

    known = target_piece in _KNOWN
    want_sleeve = sleeve_style != "sleeveless"
    wanted = {
        "front": not known or target_piece in ("front", "set"),
        "back": not known or target_piece in ("back", "set"),
        "sleeve": (not known or target_piece in ("sleeve", "set")) and want_sleeve,
        "neck_binding": not known or target_piece in ("neck_binding", "set"),
        "leg_binding": not known or target_piece in ("leg_binding", "set"),
    }

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))

    # Envelope-neck opening: fold-cut halves → the garment opening is twice the
    # drafted front + back neck edges. The leg opening (one leg) is one front
    # leg + one back leg; there are two legs, but each leg is bound with its
    # own strip cut 2.
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
    leg_opening = front.edge("leg").length() + back.edge("leg").length()
    if wanted["neck_binding"]:
        pattern.add(_binding("neck_binding", neck_opening, 1, "Neck Binding (envelope)"))
    if wanted["leg_binding"]:
        pattern.add(_binding("leg_binding", leg_opening, 2, "Leg Binding"))

    # ── Sewn seams (every one balances to delta ~ 0) ─────────────────────────
    if wanted["front"] and wanted["back"]:
        # Side seam: straight, equal by construction.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # LAP-SHOULDER / envelope: front and back shoulders are the same length;
        # they overlap (lap) rather than butt, but the sewn length is equal.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if wanted["sleeve"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    # NOTE: the crotch is NOT a sewn seam — the front and back crotch flaps
    # OVERLAP and close with snaps. Both flaps are drafted to the same rounded
    # tip (identical `leg` and `crotch` edges), so the leg bindings match and
    # the flaps stack; no crotch seam is declared.

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                             # jersey-algodon card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name not in ("neck_binding", "leg_binding")
    )
    marker_len = total_area / (fabric_width * 0.70)   # knits nest tightly
    pattern.bom = [
        {"item": "jersey-algodon", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker efficiency (soft cotton "
                 "jersey, stretch running around the body)"},
        {"item": "jersey binding strip (neck + legs)", "qty": 1, "unit": "set",
         "note": "self-fabric or 1x1 rib; see neck_binding and leg_binding piece "
                 "dimensions (cut at 2x finished width, folded over the raw edge)"},
        {"item": "crotch snap fasteners", "qty": 3, "unit": "pieces",
         "note": "~3 snaps across the overlapping crotch flaps at the marked drill "
                 "crosses; snap hardware federates to Yantra4D (snap family), not "
                 "drafted here"},
        {"item": "polyester thread + ballpoint needle", "qty": 1, "unit": "set",
         "note": "stretch/ballpoint 70/10 for jersey; a coverstitch or zigzag "
                 "finishes the bound edges"},
    ]

    # ── Metadata ───────────────────────────────────────────────────────────────
    head_pass_stretch = round(
        (head_girth / max(neck_opening * binding_ratio, 1.0) - 1.0) * 100.0, 1
    )
    pattern.metadata = {
        "fc100_rank": 92,
        "fabric_hint": "jersey-algodon",
        "sleeve_style": sleeve_style,
        "neck_opening_mm": round(neck_opening, 1),
        "leg_opening_each_mm": round(leg_opening, 1),
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "crotch_flat_width_mm": round(crotch_width, 1),
        "snap_lap_depth_mm": round(lap_depth, 1),
        "crotch_snaps": 3,
        "binding_ratio": binding_ratio,
        "head_girth_mm": round(head_girth, 1),
        "head_pass_stretch_pct": head_pass_stretch,
        "envelope_neck": (
            "front and back shoulders lap (marked overlap) and the neck is cut "
            "wide so the bound opening stretches over the head; the strip is "
            f"cut at ratio {binding_ratio} of the {round(neck_opening)} mm opening, "
            f"needing about {head_pass_stretch:.0f}% stretch to pass the head girth"
        ),
        "drafting": (
            "teaching-grade infant knit block: a drop-shoulder tee (cap solved to "
            "the armhole) extended past the waist into a rounded snap-crotch flap; "
            "front and back share the leg/crotch curve so the flaps overlap and "
            "snap, and the leg bindings match; the crotch is an overlap, not a "
            "sewn seam"
        ),
    }
    return pattern


result = build()
