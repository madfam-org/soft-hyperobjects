"""
Raglan baseball tee — FC-100 rank #74. Fashion Cabinet Garment Cartridge.

The commons' FIRST raglan geometry: there is no shoulder seam. Front and back
(cut on fold) carry a shortened neckline that ends at the raglan point, then a
long gentle raglan edge down to the underarm. The sleeve is drafted flat with
TWO raglan edges meeting a short neckline arc at its top — each sleeve raglan
is SOLVED numerically (bisected control-point bulge) to match the measured
body raglan on its side, front and back differing slightly because the neck
drops differ. The neckband is derived from the measured three-arc opening.
Classic baseball styling: contrast sleeves and band.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `chest_girth`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|neckband|set

chest_girth     = float(PARAM(lambda: chest_girth, 980.0))
body_length     = float(PARAM(lambda: body_length, 720.0))    # nape to hem
neck_girth      = float(PARAM(lambda: neck_girth, 390.0))
sleeve_length   = float(PARAM(lambda: sleeve_length, 480.0))  # neck edge to hem (3/4 baseball)
knit_ease       = float(PARAM(lambda: knit_ease, 70.0))       # total, can be small
raglan_neck_w   = float(PARAM(lambda: raglan_neck_w, 45.0))   # raglan point x on the neckline
sleeve_neck_len = float(PARAM(lambda: sleeve_neck_len, 70.0))  # neckline arc on the sleeve top
wrist_opening   = float(PARAM(lambda: wrist_opening, 200.0))  # full width flat at sleeve hem
neckband_ratio  = float(PARAM(lambda: neckband_ratio, 0.85))  # rib length / opening
neckband_width  = float(PARAM(lambda: neckband_width, 18.0))  # finished band height
seam_allowance  = float(PARAM(lambda: seam_allowance, 7.0))
hem_allowance   = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1800.0))
body_length = max(400.0, min(body_length, 1000.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(340.0, min(sleeve_length, 700.0))
knit_ease = max(-80.0, min(knit_ease, 300.0))
raglan_neck_w = max(25.0, min(raglan_neck_w, 70.0))
sleeve_neck_len = max(40.0, min(sleeve_neck_len, 120.0))
wrist_opening = max(140.0, min(wrist_opening, 400.0))
neckband_ratio = max(0.70, min(neckband_ratio, 1.0))
neckband_width = max(10.0, min(neckband_width, 40.0))

# ── Block constants ──────────────────────────────────────────────────────────
W = (chest_girth + knit_ease) / 4.0          # quarter body width (fold at CF/CB)
L = body_length
SL = sleeve_length
HPS_Y = L + 20.0                             # conceptual shoulder line — no seam exists there
RAG_DEPTH = (chest_girth + knit_ease) / 8.0 + 115.0   # HPS to underarm (raglans run deep)
RAG_DEPTH = max(180.0, min(RAG_DEPTH, L - 140.0))
UNDERARM = fc.P(W, HPS_Y - RAG_DEPTH)
NECK_K = neck_girth / 390.0                  # neckline depth scale
RP_FRONT = fc.P(raglan_neck_w, HPS_Y - 20.0 * NECK_K)  # raglan point on the front neckline
RP_BACK = fc.P(raglan_neck_w, HPS_Y - 14.0 * NECK_K)   # back raglan point sits higher
FRONT_NECK_RISE = 58.0 * NECK_K              # CF neck sits this far below its raglan point
BACK_NECK_RISE = 22.0 * NECK_K


def _neck_edge(cf_y, rp):
    """CF/CB neckline run: horizontal at the fold, rising to the raglan point."""
    c0 = fc.P(rp.x * 0.50, cf_y)
    c1 = fc.P(rp.x * 0.85, cf_y + (rp.y - cf_y) * 0.55)
    return fc.Edge("neck", [fc.Bezier(fc.P(0.0, cf_y), c0, c1, rp)])


def _body_raglan(rp):
    """Body raglan: near-straight with a gentle hollow toward the armpit."""
    return fc.Edge("raglan", [fc.curve_through(rp, UNDERARM, bulge=0.025, side=-1.0)])


def _body_piece(name, rp, neck_rise, raglan_notches, label):
    cf_y = rp.y - neck_rise
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, cf_y))]),
        _neck_edge(cf_y, rp),
        _body_raglan(rp),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5)] + raglan_notches,
        grainline=fc.Grainline(fc.P(W * 0.62, 80.0), fc.P(W * 0.62, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    # Single notch on the front raglan — never confusable with the back's pair.
    notches = [fc.Notch("raglan", 0.5, "front raglan")]
    return _body_piece("front", RP_FRONT, FRONT_NECK_RISE, notches, "Front")


def build_back():
    # Double notch on the back raglan (garment convention for back seams).
    notches = [fc.Notch("raglan", 0.45, "back raglan"), fc.Notch("raglan", 0.55, "back raglan")]
    return _body_piece("back", RP_BACK, BACK_NECK_RISE, notches, "Back")


def _sleeve_neck_curve(half_w):
    """Sleeve-top neckline arc: a gentle dome bridging the two raglan points."""
    return fc.curve_through(fc.P(half_w, SL), fc.P(-half_w, SL), bulge=0.10, side=-1.0)


def _solve_neck_half_width():
    """Bisect the arc's half-chord until its length equals sleeve_neck_len."""
    lo, hi = 8.0, 60.0
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _sleeve_neck_curve(mid).length(0.05) < sleeve_neck_len:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _sleeve_raglan_curve(bulge, nhw, ua):
    """Raglan template on the +x half: neck-arc end to underarm, bowing outward."""
    return fc.curve_through(fc.P(nhw, SL), ua, bulge=bulge, side=1.0)


def _solve_raglan_bulge(target, nhw, ua, tag):
    """Bisect the control-point bulge until the curve length matches the body raglan."""
    lo, hi = 0.0, 0.45
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if _sleeve_raglan_curve(mid, nhw, ua).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    solved = _sleeve_raglan_curve(bulge, nhw, ua).length(0.05)
    if abs(solved - target) > 1.5:
        raise ValueError(
            f"{tag} raglan solver did not converge: {solved:.1f} vs target {target:.1f}"
        )
    return bulge, solved


def build_sleeve(targ_front, targ_back):
    """Flat raglan sleeve; each raglan edge solved to its measured body raglan."""
    nhw = _solve_neck_half_width()
    hb = max(nhw + 25.0, (chest_girth + knit_ease) * 0.125)   # half biceps, flat
    dx = hb - nhw
    # Underarm drop: place the corners so the straight chord sits ~1.5% short of
    # the shorter (front) target; the solved bulges supply the remainder.
    chord = 0.985 * min(targ_front, targ_back)
    drop = math.sqrt(max(chord * chord - dx * dx, 120.0 * 120.0))
    if drop > SL - 60.0:
        raise ValueError(
            f"sleeve_length {SL:.0f} mm too short for raglan drop {drop:.0f} mm — lengthen it"
        )
    ua_y = SL - drop
    ua = fc.P(hb, ua_y)
    bulge_f, len_f = _solve_raglan_bulge(targ_front, nhw, ua, "front")
    bulge_b, len_b = _solve_raglan_bulge(targ_back, nhw, ua, "back")
    wr2 = min(wrist_opening / 2.0, hb)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-wr2, 0.0), fc.P(wr2, 0.0))]),
        fc.Edge("underarm_back", [fc.Line(fc.P(wr2, 0.0), ua)]),
        fc.Edge("back_raglan", [_sleeve_raglan_curve(bulge_b, nhw, ua).reversed()]),
        fc.Edge("sleeve_neck", [_sleeve_neck_curve(nhw)]),
        fc.Edge("front_raglan", [_sleeve_raglan_curve(bulge_f, nhw, ua).mirrored_x(0.0)]),
        fc.Edge("underarm_front", [fc.Line(fc.P(-hb, ua_y), fc.P(-wr2, 0.0))]),
    ]
    piece = fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[
            fc.Notch("front_raglan", 0.5, "front raglan"),
            fc.Notch("back_raglan", 0.45, "back raglan"),
            fc.Notch("back_raglan", 0.55, "back raglan"),
        ],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, SL - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (raglan, contrast)",
    )
    info = {
        "front_bulge": bulge_f, "front_len": len_f,
        "back_bulge": bulge_b, "back_len": len_b,
    }
    return piece, info


def build_neckband(front, back, sleeve):
    # Neckline accounting — the opening is THREE arcs per half-garment:
    #   half = front.neck (CF → front raglan point, on fold)
    #        + back.neck  (CB → back raglan point, on fold)
    #        + sleeve_neck (ONE sleeve's arc bridging the two raglan points)
    # Two mirrored halves and two sleeves make the full opening:
    #   total = 2*(front.neck + back.neck) + 2*sleeve_neck = 2*half
    # Band length = total * neckband_ratio (rib stretch) + 2*seam_allowance
    # for the single closing join; the band height is doubled to fold.
    half = (front.edge("neck").length() + back.edge("neck").length()
            + sleeve.edge("sleeve_neck").length())
    band_len = 2.0 * half * neckband_ratio + 2.0 * seam_allowance
    band_h = 2.0 * neckband_width
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(band_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(band_len, 0.0), fc.P(band_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(band_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neckband",
        edges,
        seam_allowance=0.0,                  # band length already includes joins
        grainline=fc.Grainline(fc.P(band_len * 0.2, band_h / 2.0),
                               fc.P(band_len * 0.8, band_h / 2.0)),
        internals=[fc.Internal(
            "fold line",
            [fc.P(0.0, band_h / 2.0), fc.P(band_len, band_h / 2.0)],
        )],
        cut=fc.CutSpec(quantity=1),
        label="Neckband (contrast rib)",
    )


def build():
    pattern = fc.PatternSet("raglan-baseball-tee")
    front = build_front()
    back = build_back()
    targ_front = front.edge("raglan").length(0.05)
    targ_back = back.edge("raglan").length(0.05)
    sleeve, solve = build_sleeve(targ_front, targ_back)
    neckband = build_neckband(front, back, sleeve)
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
        pattern.add(sleeve)
    if wanted["neckband"]:
        pattern.add(neckband)
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    if wanted["sleeve"] and wanted["front"]:
        pattern.declare_seam([("sleeve", "front_raglan")], [("front", "raglan")], tol=2.0)
    if wanted["sleeve"] and wanted["back"]:
        pattern.declare_seam([("sleeve", "back_raglan")], [("back", "raglan")], tol=2.0)
    if wanted["sleeve"]:
        pattern.declare_seam(
            ("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0
        )
    total_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length()
                           + sleeve.edge("sleeve_neck").length())
    band_len = total_opening * neckband_ratio + 2.0 * seam_allowance
    fabric_width = 1600.0                    # jersey-algodon card width
    body_area = 2.0 * (front.area() + back.area())            # both cut on fold
    contrast_area = 2.0 * sleeve.area() + neckband.area()     # sleeves + band
    body_marker = body_area / (fabric_width * 0.70)           # knits nest tightly
    contrast_marker = contrast_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "jersey-algodon (body colour)", "qty": round(body_marker / 10.0) * 10,
         "unit": "mm_length", "note": f"at {fabric_width:.0f} mm width, 70% marker efficiency"},
        {"item": "jersey-algodon (contrast colour)", "qty": round(contrast_marker / 10.0) * 10,
         "unit": "mm_length", "note": "sleeves + neckband — classic baseball contrast"},
        {"item": "polyester thread + stretch needle", "qty": 1, "unit": "set",
         "note": "ballpoint 75/11"},
    ]
    pattern.metadata = {
        "fc100_rank": 74,
        "fabric_hint": "jersey-algodon",
        "styling": "contrast sleeves classic",
        "neck_opening_mm": round(total_opening, 1),
        "neckband_len_mm": round(band_len, 1),
        "raglan_front_body_mm": round(targ_front, 1),
        "raglan_front_sleeve_mm": round(solve["front_len"], 1),
        "raglan_front_bulge": round(solve["front_bulge"], 4),
        "raglan_back_body_mm": round(targ_back, 1),
        "raglan_back_sleeve_mm": round(solve["back_len"], 1),
        "raglan_back_bulge": round(solve["back_bulge"], 4),
        "min_head_stretch_pct": round(
            (560.0 / max(total_opening * neckband_ratio, 1.0) - 1.0) * 100.0, 1
        ),
        "drafting": "first raglan block: no shoulder seam; sleeve raglans solved to body",
    }
    return pattern


result = build()
