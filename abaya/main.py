"""
Abaya — FC-100 rank #98. Fashion Cabinet Garment Cartridge.

A long, loose, floor-length overgarment, offered as a teaching-grade
parametric draft, respectfully — the wearer chooses fabric and any
embellishment. This is the classic FRONT-OPEN ("open abaya") style, the most
common made-to-measure cut: a back panel cut 1 on the fold at centre back, two
mirrored front panels that meet (open) at centre front, long straight wide
sleeves, and a straight NECK/FRONT BINDING strip that finishes the neckline
plus both centre-front opening edges in one continuous run.

The shoulder is dropped (a low, wide shoulder), so the armhole is a short,
shallow curve and the sleeve cap is drafted flat to it (cap ease 0) with the
same numeric bisection the robe uses. The drape is the point: very generous
ease, minimal body shaping, wide sleeves. The closed overhead style is a
different draft — this cartridge models the front-open cut and says so.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|binding|set

chest_girth    = float(PARAM(lambda: chest_girth, 1000.0))
abaya_length   = float(PARAM(lambda: abaya_length, 1400.0))   # nape to floor hem
neck_girth     = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length  = float(PARAM(lambda: sleeve_length, 620.0))   # dropped shoulder to wrist
drape_ease     = float(PARAM(lambda: drape_ease, 360.0))      # very generous total ease
hem_flare      = float(PARAM(lambda: hem_flare, 140.0))       # each side widens toward hem
sleeve_width   = float(PARAM(lambda: sleeve_width, 200.0))    # half wrist opening (wide)
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (mirror the manifest slider min/max exactly) ──────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
abaya_length = max(1100.0, min(abaya_length, 1600.0))
neck_girth = max(320.0, min(neck_girth, 540.0))
sleeve_length = max(400.0, min(sleeve_length, 800.0))
drape_ease = max(200.0, min(drape_ease, 600.0))
hem_flare = max(0.0, min(hem_flare, 350.0))
sleeve_width = max(120.0, min(sleeve_width, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 80.0))

# ── Dropped-shoulder floor-length block ──────────────────────────────────────
W = (chest_girth + drape_ease) / 4.0                 # quarter body width
L = abaya_length                                     # hem at y=0, HPS line at y=L
AH = (chest_girth + drape_ease) / 8.0 + 60.0         # shallow (dropped) armhole depth
AH = max(150.0, min(AH, L - 200.0))
NW = max(66.0, neck_girth / 5.0 + 6.0)               # half neck width
HPS_Y = L + 20.0                                     # high point of shoulder line
SHOULDER_DROP = 45.0                                 # low, wide shoulder
SH_END = fc.P(W - 6.0, HPS_Y - SHOULDER_DROP)        # shoulder-point (armhole top)
UNDERARM = fc.P(W, HPS_Y - SHOULDER_DROP - AH)       # armhole bottom / side top
BACK_NECK_DROP = 22.0
FRONT_NECK_DROP = 105.0                              # deeper front scoop
HEM_SIDE = fc.P(W + hem_flare, 0.0)                  # flared hem corner


def _armhole_edge():
    """Short shallow armhole for the dropped shoulder (top → underarm)."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 10.0, SH_END.y - AH * 0.40),
                   fc.P(W - 4.0, UNDERARM.y + AH * 0.28), UNDERARM)],
    )


def build_back():
    """Back panel: cut 1 on fold at centre back; full floor length."""
    neck_top_y = HPS_Y - BACK_NECK_DROP
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(BACK_NECK_DROP, 24.0) * 0.45),
                   fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, HEM_SIDE)]),
            fc.Edge("hem", [fc.Line(HEM_SIDE, origin)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0, "neck": 0.0},
        notches=[fc.Notch("armhole", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(W * 0.5, 90.0), fc.P(W * 0.5, L - 140.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    """Front panel, cut 2 mirrored: straight open centre-front edge.

    The CF edge is a plain vertical line from the hem up to the front-neck
    point (open abaya — the two fronts meet but are not joined). The front
    neck then scoops up to the shoulder-neck point (NW, HPS_Y).
    """
    neck_top_y = HPS_Y - FRONT_NECK_DROP
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.42, neck_top_y),
                   fc.P(NW, neck_top_y + FRONT_NECK_DROP * 0.42), fc.P(NW, HPS_Y))],
    )
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_top_y))]),
            neck,
            fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
            _armhole_edge(),
            fc.Edge("side", [fc.Line(UNDERARM, HEM_SIDE)]),
            fc.Edge("hem", [fc.Line(HEM_SIDE, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center_front": 0.0, "neck": 0.0},
        notches=[fc.Notch("armhole", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(W * 0.6, 90.0), fc.P(W * 0.6, L - 140.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def _cap_curve(hb, sl, ch):
    """Sleeve-cap curve of half-base `hb`, straight length `sl`, crown `ch`."""
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.62, sl + ch * 0.14),
                  fc.P(hb * 0.30, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.30, sl + ch),
                  fc.P(-hb * 0.62, sl + ch * 0.14), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Long wide straight sleeve; cap solved flat to the armholes (ease 0)."""
    ch = max(40.0, AH * 0.26)                         # shallow crown (dropped shoulder)
    sl = max(120.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 80.0
    for _ in range(60):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(sleeve_width, hb * 0.85)                # wide open wrist, no cuff
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _binding(finished_len, band_h):
    """Straight binding strip; `bottom` edge length = finished_len exactly."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(finished_len, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(finished_len, 0.0), fc.P(finished_len, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(finished_len, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "binding",
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(finished_len * 0.2, band_h / 2.0),
                               fc.P(finished_len * 0.8, band_h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Neck & Front Binding",
    )


BIND_W = 18.0  # finished binding width; strip is cut doubled (band_h = 2 x)


def build():
    pattern = fc.PatternSet("abaya")
    front = build_front()
    back = build_back()
    # Cap target = both armholes summed (front sews cut-2, but each sleeve cap
    # matches one front armhole + one back armhole around a single armscye).
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)

    # Binding finishes the whole opening in one run: back neck + BOTH front
    # necks + BOTH centre-front edges. Length taken from the measured edges so
    # the seam delta is 0 by construction.
    neck_run = (
        back.edge("neck").length()
        + 2.0 * front.edge("neck").length()
        + 2.0 * front.edge("center_front").length()
    )

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve(cap_target))
    if all_pieces or target_piece == "binding":
        pattern.add(_binding(neck_run, 2.0 * BIND_W))

    if all_pieces:
        # Shoulder: front ↔ back (identical geometry → delta 0).
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Side: front ↔ back (identical geometry → delta 0).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Armscye: one sleeve cap ↔ (front armhole + back armhole), cap ease 0.
        pattern.declare_seam(
            [("sleeve", "cap")],
            [("front", "armhole"), ("back", "armhole")],
            tol=2.0,
        )
        # Sleeve underarm seam closes on itself.
        pattern.declare_seam(("sleeve", "underarm_front"),
                             ("sleeve", "underarm_back"), tol=1.0)
        # Binding ↔ the summed neckline + both CF edges (delta 0 by derivation).
        pattern.declare_seam(
            [("binding", "bottom")],
            [("back", "neck"),
             ("front", "neck"), ("front", "neck"),
             ("front", "center_front"), ("front", "center_front")],
            tol=1.5,
        )

    pattern.bom = [
        # Floor-length garment: two body-length spans (front pair + back) plus the
        # sleeve pair. Rough yardage at the poplin bolt width, marker efficiency ~62%.
        {"item": "popelina-algodon (drapey woven)", "qty": round((L + 250.0) * 2.6 / 10.0) * 10,
         "unit": "cm", "note": "≈2.6 body-length spans at 1450 mm width, 62% marker; "
                               "buy the length, not the width — production abaya is often "
                               "crepe/nidha, this poplin is the teaching stand-in"},
        {"item": "binding fabric (self or contrast, cut on grain or bias)",
         "qty": round(neck_run) + 40, "unit": "mm",
         "note": f"neck + both CF edges = {round(neck_run)} mm; strip cut "
                 f"{round(2.0 * BIND_W)} mm wide (doubled to {round(BIND_W)} mm finished)"},
        {"item": "closure — hidden snap set or self tie (optional)", "qty": 1, "unit": "set",
         "note": "the front-open abaya is usually worn open or with one discreet neck "
                 "closure; snap/hook hard goods federate to Yantra4D (snap-fastener "
                 "family), never modelled here — or substitute a fabric self-tie"},
        {"item": "polyester or cotton thread + universal 80/12 needle", "qty": 1, "unit": "set",
         "note": "narrow-hem the CF opening and floor hem; french-seam or overlock the "
                 "long side and sleeve seams for a clean drapey inside"},
    ]

    pattern.metadata = {
        "fc100_rank": 98,
        "fabric_hint": "popelina-algodon",
        "style": "front-open (open abaya)",
        "quarter_width_mm": round(W, 1),
        "armhole_depth_mm": round(AH, 1),
        "half_neck_width_mm": round(NW, 1),
        "hem_half_width_mm": round(HEM_SIDE.x, 1),
        "neck_binding_run_mm": round(neck_run, 1),
        "cap_target_mm": round(cap_target, 1),
        "drafting": "dropped-shoulder floor-length overgarment; back on fold, two open "
                    "CF fronts, wide straight sleeves with the cap solved flat to the "
                    "armholes (ease 0); one binding finishes neck + both CF edges. "
                    "Teaching-grade parametric draft offered respectfully — the wearer "
                    "chooses fabric and embellishment; production abaya is commonly "
                    "crepe/nidha and the closed overhead style is a separate draft",
    }
    return pattern


result = build()
