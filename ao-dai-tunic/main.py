"""
Áo Dài (tunic) — Fashion Cabinet Garment Cartridge (FC-200 #200, Vietnamese heritage).

The áo dài is the Vietnamese national dress: a long, close-fitting tunic split high at both sides
into front and back panels (flaps) that fall to the ankle, worn over wide trousers, with a
mandarin (stand) collar and raglan or set sleeves. This cartridge drafts the TUNIC — a fitted
darted body with a mandarin collar and long side-split panels — offered with respect for the
living tradition. The trousers are drafted separately; the woven/embroidered motifs that carry
regional and personal identity are the maker's and are not reproduced here.

This is the 200th Fashion Cabinet hyperobject.

Pieces:
  - front / back : fitted darted body splitting into long ankle panels (front cut 2, open CF
                   placket; back on fold), high side slits.
  - sleeve       : long fitted sleeve (cut 2 mirror).
  - collar       : mandarin stand collar.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|collar|set

bust_girth   = float(PARAM(lambda: bust_girth, 880.0))
waist_girth  = float(PARAM(lambda: waist_girth, 700.0))
hip_girth    = float(PARAM(lambda: hip_girth, 930.0))
tunic_length = float(PARAM(lambda: tunic_length, 1250.0))  # nape to ankle panel hem
neck_girth   = float(PARAM(lambda: neck_girth, 380.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 220.0))
slit_height  = float(PARAM(lambda: slit_height, 640.0))    # high side slit (from hem up)
collar_height = float(PARAM(lambda: collar_height, 45.0))
ease         = float(PARAM(lambda: ease, 60.0))            # very close fit
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(680.0, min(bust_girth, 1400.0))
waist_girth  = max(540.0, min(waist_girth, 1250.0))
hip_girth    = max(720.0, min(hip_girth, 1450.0))
tunic_length = max(900.0, min(tunic_length, 1500.0))
neck_girth   = max(300.0, min(neck_girth, 520.0))
sleeve_length = max(400.0, min(sleeve_length, 700.0))
sleeve_depth  = max(180.0, min(sleeve_depth, 340.0))
slit_height  = max(400.0, min(slit_height, 900.0))
collar_height = max(20.0, min(collar_height, 90.0))
ease         = max(20.0, min(ease, 180.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

L = tunic_length
BUST_HALF  = (bust_girth + ease) / 4.0
WAIST_HALF = (waist_girth + ease) / 4.0
HIP_HALF   = (hip_girth + ease) / 4.0
NECK_HALF  = neck_girth / 5.0
SHOULDER_X = BUST_HALF
ARMSCYE_DROP = sleeve_depth
WAIST_Y = L - 380.0
HIP_Y = WAIST_Y - 200.0


def _body(name, is_front, label):
    top_y = L
    cf_x = 0.0
    neck_top = fc.P(0.0, top_y) if not is_front else fc.P(cf_x, top_y - 30.0)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER_X, top_y - 30.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    # side: bust -> waist (nip) -> hip -> straight down to the slit top; below that the panel
    # is the ankle flap (down to hem). The slit means the side seam ends at slit_height.
    side_pts = [armscye_bot, fc.P(WAIST_HALF, WAIST_Y), fc.P(HIP_HALF, HIP_Y),
                fc.P(HIP_HALF, slit_height)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[i], side_pts[i + 1]) for i in range(3)])
    internals = [fc.Internal("waist-dart", [fc.P(WAIST_HALF * 0.5, WAIST_Y + 100.0),
                                            fc.P(WAIST_HALF * 0.5, WAIST_Y - 120.0)], kind="dart")]
    if is_front:
        internals.append(fc.Internal("bust-dart",
                                     [fc.P(BUST_HALF, top_y - ARMSCYE_DROP - 20.0),
                                      fc.P(WAIST_HALF * 0.55, top_y - ARMSCYE_DROP - 60.0)],
                                     kind="dart"))
        internals.append(fc.Internal("cf-placket", [fc.P(0.0, top_y - 30.0),
                                                    fc.P(NECK_HALF, top_y - 30.0)], kind="marking"))
    # edges: CF/center (down to hem), neck, shoulder, armscye, side (to slit), slit, panel-hem
    cf_edge = (fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_top)]) if is_front
               else fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]))
    neck_edge = (fc.Edge("neck", [fc.Line(neck_top, neck_out)]) if is_front
                 else fc.Edge("neck", [fc.curve_through(neck_top, neck_out,
                                                        bulge=0.12, side=-1.0)]))
    return fc.Piece(
        name,
        [
            cf_edge,
            neck_edge,
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                                 bulge=0.18, side=-1.0)]),
            side_edge,
            fc.Edge("slit", [fc.Line(fc.P(HIP_HALF, slit_height), fc.P(HIP_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("slit", 1.0, "slit top")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 100.0), fc.P(WAIST_HALF * 0.5, L - 140.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True) if is_front
        else fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve(head_h=None):
    # sleevehead height is solved to the measured armscye edge so the seam balances.
    head_h = sleeve_depth if head_h is None else head_h
    sw = sleeve_length
    wrist = BUST_HALF * 0.45
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, (head_h - wrist) / 2.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(sw, (head_h - wrist) / 2.0),
                                     fc.P(sw, (head_h + wrist) / 2.0))]),
            fc.Edge("sleeve_top", [fc.Line(fc.P(sw, (head_h + wrist) / 2.0), fc.P(0.0, head_h))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sleevehead", 1.0, "shoulder"), fc.Notch("sleevehead", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.3), fc.P(sw * 0.5, head_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build_collar():
    ln = neck_girth + 20.0
    h = collar_height * 2.0
    return fc.Piece(
        "collar",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Mandarin collar",
    )


def build():
    pattern = fc.PatternSet("ao-dai-tunic")
    everything = target_piece == "set"
    back_body = _body("back", False, "Back (ankle panels)")
    armscye_len = next(e for e in back_body.edges if e.name == "armscye").length()
    if everything or target_piece == "front":
        pattern.add(_body("front", True, "Front (open placket, ankle panels)"))
    if everything or target_piece == "back":
        pattern.add(back_body)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve(armscye_len))
    if everything or target_piece == "collar":
        pattern.add(build_collar())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armscye"), tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "silk, brocade, or fine synthetic (fluid, holds a line)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; a fluid fabric that skims and flows."},
        {"item": "side + placket closure (snaps or hooks)", "qty": 1, "unit": "set",
         "note": "the áo dài closes along the shoulder/side with snaps under the placket."},
        {"item": "mandarin collar interfacing", "qty": 1, "unit": "as needed",
         "note": "the stand collar is interfaced to hold its shape."},
        {"item": "fine thread", "qty": 1, "unit": "spool",
         "note": "narrow rolled or bound edges on the split panels; fully faced front."},
    ]
    pattern.metadata = {
        "fc200_rank": 200, "family": "heritage_global", "fabric_hint": "seda-brocado",
        "milestone": "The 200th Fashion Cabinet hyperobject.",
        "heritage_note": "The áo dài is the national dress of Vietnam. This cartridge drafts the "
            "TUNIC GEOMETRY only — the trousers are drafted separately, and the woven, painted, "
            "and embroidered motifs that carry regional and personal identity are the maker's and "
            "are not reproduced here. Offered with respect for the living tradition.",
        "construction": "a very close darted body (bust + waist darts over common seams) with a "
            "mandarin collar, splitting high at both sides into long front and back ankle panels "
            "worn over trousers; side/armscye seams balance by construction.",
        "solved": {"bust_q_mm": round(BUST_HALF, 1), "waist_q_mm": round(WAIST_HALF, 1),
                   "slit_height_mm": round(slit_height, 1), "tunic_length_mm": round(L, 1)},
    }
    return pattern


result = build()
