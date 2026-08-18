"""
Kids' T-shirt — FC-100 rank #93. Fashion Cabinet Garment Cartridge.

A children's crew tee: a scaled-down knit block (front + back cut on fold),
a set-in sleeve whose cap length is SOLVED numerically to the front + back
armholes (multi-edge seam check), and a bound rib neckline whose strip length
is derived from the measured neck opening times a rib-stretch ratio.

Child-specific feature — the classic ENVELOPE / lap-shoulder neckline. A
`neckline` switch chooses:
  - "crew": a normal bound crew neck (as a grown-up tee).
  - "envelope": the front and back shoulders each carry a lapped extension that
    overlaps at wear, so the wide neck opens over a child's head with no closure
    (or an optional shoulder snap). The overlap is marked on both pieces; the
    two shoulder edges stay equal length, so the shoulder seam still balances.

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


# ── Parameters (millimetres; girths are full-body child measurements) ────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|neckband|set
neckline     = str(PARAM(lambda: neckline, "envelope"))  # crew | envelope

chest_girth    = float(PARAM(lambda: chest_girth, 640.0))   # child chest, full-body
body_length    = float(PARAM(lambda: body_length, 380.0))   # nape to hem
neck_girth     = float(PARAM(lambda: neck_girth, 300.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 130.0))  # cap apex to hem
knit_ease      = float(PARAM(lambda: knit_ease, 80.0))       # total positive comfort ease
armhole_depth  = float(PARAM(lambda: armhole_depth, 0.0))    # 0 = auto
sleeve_opening = float(PARAM(lambda: sleeve_opening, 0.0))   # full width flat; 0 = auto
overlap        = float(PARAM(lambda: overlap, 22.0))         # envelope lap depth
neckband_ratio = float(PARAM(lambda: neckband_ratio, 0.88))  # rib length / opening
neckband_width = float(PARAM(lambda: neckband_width, 16.0))  # finished band height
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (mirror the manifest sliders exactly) ─────────────────────────────
if neckline not in ("crew", "envelope"):
    neckline = "envelope"
chest_girth = max(480.0, min(chest_girth, 820.0))
body_length = max(280.0, min(body_length, 520.0))
neck_girth = max(240.0, min(neck_girth, 380.0))
sleeve_length = max(50.0, min(sleeve_length, 300.0))
knit_ease = max(20.0, min(knit_ease, 160.0))
armhole_depth = max(0.0, min(armhole_depth, 250.0))
sleeve_opening = max(0.0, min(sleeve_opening, 320.0))
overlap = max(12.0, min(overlap, 40.0))
neckband_ratio = max(0.75, min(neckband_ratio, 1.0))
neckband_width = max(8.0, min(neckband_width, 30.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

ENVELOPE = neckline == "envelope"

W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
AH = armhole_depth if armhole_depth > 0 else (chest_girth + knit_ease) / 8.0 + 55.0
AH = max(110.0, min(AH, L - 80.0))
# Envelope necks are cut wider (they open over the head with no closure);
# crew necks are the usual snug rib opening.
NW = max(48.0, neck_girth / 5.0 + (18.0 if ENVELOPE else 0.0))
HPS_Y = L + 16.0                             # high-point shoulder above nape line
SHOULDER_DROP = 22.0                         # set-in shoulder slope (child scale)
FRONT_NECK_DROP = 58.0 if ENVELOPE else 62.0
BACK_NECK_DROP = 16.0
# Envelope shoulder extends OUTWARD past the HPS by the lap depth so the two
# shoulders overlap at wear. Both front and back carry the same extension, so
# the shoulder edges stay equal length and the seam balances.
LAP = overlap if ENVELOPE else 0.0
SH_END = fc.P(W - 4.0, HPS_Y - SHOULDER_DROP)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)


def _armhole_edge():
    """Shared front/back armhole curve (set-in cap; child-scale depth)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.34),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_piece(name, neck_edge, neck_top_y, label, shoulder_overlap):
    """One body panel: cut on fold at the center. `shoulder_overlap` extends the
    HPS end of the shoulder outward (envelope lap); the shoulder line is drawn
    from the extended neck point to SH_END so its length matches on both panels.
    A marked overlap internal shows the lap zone when envelope."""
    origin = fc.P(0.0, 0.0)
    hps = fc.P(NW, HPS_Y + shoulder_overlap)     # lap raises the neck-side point
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck_edge,
        fc.Edge("shoulder", [fc.Line(hps, SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    internals = []
    if shoulder_overlap > 0.0:
        internals.append(fc.Internal(
            "shoulder overlap",
            [fc.P(0.0, HPS_Y), fc.P(NW, HPS_Y)],
            kind="marking",
        ))
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "neck": 0.0},  # neck is bound (0 SA)
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, f"{name} armhole")],
        grainline=fc.Grainline(fc.P(W * 0.6, 40.0), fc.P(W * 0.6, max(60.0, L - 70.0))),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        internals=internals,
        label=label,
    )


def build_front():
    cf_neck_y = HPS_Y - FRONT_NECK_DROP
    hps = fc.P(NW, HPS_Y + LAP)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, cf_neck_y), fc.P(NW * 0.55, cf_neck_y),
                   fc.P(NW, cf_neck_y + FRONT_NECK_DROP * 0.45), hps)],
    )
    return _body_piece("front", neck, cf_neck_y, "Front", LAP)


def build_back():
    cb_neck_y = HPS_Y - BACK_NECK_DROP
    hps = fc.P(NW, HPS_Y + LAP)
    neck = fc.Edge(
        "neck",
        [fc.curve_through(fc.P(0.0, cb_neck_y), hps, bulge=0.12, side=-1.0)],
    )
    return _body_piece("back", neck, cb_neck_y, "Back", LAP)


def _cap_curve(hb, sl, ch):
    """Sleeve-cap edge: two mirrored beziers over the apex, authored R→L."""
    apex = fc.P(0.0, sl + ch)
    right = fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12),
                      fc.P(hb * 0.32, sl + ch), apex)
    left = fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch),
                     fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl))
    return fc.Edge("cap", [right, left])


def build_sleeve(cap_target):
    """Set-in sleeve; cap length SOLVED by bisection to the armhole sum
    (small/zero ease for knits)."""
    ch = max(35.0, AH * 0.33)                       # shallow knit cap
    sl = max(40.0, sleeve_length - ch)              # underarm-to-hem length
    lo, hi = 15.0, cap_target / 2.0 + ch + 60.0
    hb = hi
    for _ in range(52):                             # bisect: cap length grows with hb
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
    chw = (sleeve_opening / 2.0) if sleeve_opening > 0 else hb * 0.85
    chw = max(45.0, min(chw, hb))
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
        label="Sleeve",
    )


def build_neckband(neck_opening):
    """Straight rib strip, folded lengthwise when sewn. Length is the measured
    neck opening times the rib ratio, plus joins — the construction rule
    encoded, not a fixed number."""
    band_len = neck_opening * neckband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * neckband_width                   # folded lengthwise when sewn
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neckband",
        edges,
        seam_allowance=0.0,                         # band length already includes joins
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Neck Binding (rib)",
    )


def build():
    pattern = fc.PatternSet("kids-t-shirt")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # Full neckline opening measured on the fold (front-half + back-half, both
    # halves around the body) → the true opening the rib strip seats into.
    neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())

    wanted = {
        "front": target_piece in ("front", "set"),
        "back": target_piece in ("back", "set"),
        "sleeve": target_piece in ("sleeve", "set"),
        "neckband": target_piece in ("neckband", "set"),
    }
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}
    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["sleeve"]:
        pattern.add(build_sleeve(cap_target))
    if wanted["neckband"]:
        pattern.add(build_neckband(neck_opening))

    # ── Declared seams (all must balance to delta ≈ 0) ───────────────────────
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Shoulder: a plain seam (crew) or a lapped overlap (envelope). Either
        # way both shoulder edges are drawn to the same length, so the seam
        # balances; the envelope overlap is a marked construction zone.
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
    if wanted["neckband"] and wanted["front"] and wanted["back"]:
        # Bound rib neckline: a folded strip stitched around the FULL neckline
        # while stretched by the rib ratio. Both on-fold neck edges are summed
        # twice to give the true opening. The strip is relaxed-shorter than the
        # opening; that intentional negative stretch is the seam ease, leaving
        # delta ≈ 0.  len_a = opening·ratio + 2·SA ; len_b = opening.
        neck_ease = 2.0 * seam_allowance - neck_opening * (1.0 - neckband_ratio)
        pattern.declare_seam(
            ("neckband", "bottom"),
            [("front", "neck"), ("back", "neck"), ("front", "neck"), ("back", "neck")],
            tol=2.0,
            ease=neck_ease,
        )

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1600.0                       # jersey-algodon card width
    body_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces if p.name in ("front", "back", "sleeve")
    )
    marker_len = body_area / (fabric_width * 0.70) if body_area > 0 else 0.0
    band_cut_mm = round(neck_opening * neckband_ratio + 2.0 * seam_allowance)
    pattern.bom = [
        {"item": "jersey-algodon (cotton/elastane single knit)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"child body + sleeves; at {fabric_width:.0f} mm width, "
                 f"70% marker efficiency; stretch runs around the body"},
        {"item": "1x1 rib for neck binding",
         "qty": band_cut_mm, "unit": "mm_length",
         "note": f"cut {2.0 * neckband_width:.0f} mm wide × {band_cut_mm} mm long "
                 f"(neckline {round(neck_opening)} mm × {neckband_ratio:.2f} ratio + joins)"},
        {"item": "polyester thread + ballpoint/stretch needle", "qty": 1, "unit": "set",
         "note": "stretch or coverstitch on knit seams and bound neck; 75/11 ballpoint"},
    ]
    if ENVELOPE:
        pattern.bom.append(
            {"item": "shoulder snap (optional)", "qty": 2, "unit": "pcs",
             "note": "OPTIONAL — the wide envelope neck opens over the head with no "
                     "closure; a light snap per shoulder keeps the lap flat. Hardware "
                     "is a Yantra4D cartridge (notion.hardware_ref: snap-fastener), "
                     "not re-implemented here — only the overlap is marked."})

    # ── Metadata ───────────────────────────────────────────────────────────────
    pattern.metadata = {
        "fc100_rank": 93,
        "fabric_hint": "jersey-algodon",
        "neckline": neckline,
        "child_scale": True,
        "chest_girth_mm": round(chest_girth, 1),
        "body_length_mm": round(L, 1),
        "knit_ease_mm": round(knit_ease, 1),
        "neck_opening_mm": round(neck_opening, 1),
        "neckband_ratio": neckband_ratio,
        "neck_binding_cut_mm": band_cut_mm,
        "armhole_each_mm": round(cap_target / 2.0, 1),
        "shoulder_overlap_mm": (round(overlap, 1) if ENVELOPE else 0.0),
        "min_head_stretch_pct": round(
            (520.0 / max(neck_opening * neckband_ratio, 1.0) - 1.0) * 100.0, 1
        ),
        "drafting": (
            "child-scale crew tee: front/back on fold, set-in sleeve cap solved "
            "to the armhole sum, bound rib neckline (length = opening × ratio). "
            "Envelope neckline adds a marked lap-shoulder overlap so the wide "
            "neck opens over the head; crew is a plain snug rib. Teaching-grade: "
            "straight rib strip (real ribbing is cut narrower and eased); the "
            "envelope lap is drawn as equal-length shoulders with a marked "
            "overlap zone rather than a graded step, and bound edges use 0 SA."
        ),
    }
    return pattern


result = build()
