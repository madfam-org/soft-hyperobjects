"""
Sweater Dress — Fashion Cabinet Garment Cartridge (FC-200 #188, dress gap).

The knit sweater dress: a long-sleeved knit column dress with a ribbed crew or funnel neck and
ribbed cuffs/hem, cut close and cosy in a sweater knit — the winter pull-on dress. Distinct from
FC-100's tank-dress (sleeveless) and the woven dresses. Front and back share the body width so the
shoulder and side seams balance by construction; a set sleeve joins at the armhole.

Pieces:
  - front / back : knit body panels to dress length (cut on fold), gentle waist shaping.
  - sleeve       : long fitted set sleeve (cut 2 mirror).
  - band         : ribbed band strip (neck/cuff/hem), cut to the measured openings.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|sleeve|band|set

chest_girth  = float(PARAM(lambda: chest_girth, 960.0))
hip_girth    = float(PARAM(lambda: hip_girth, 1000.0))
dress_length = float(PARAM(lambda: dress_length, 940.0))
neck_width   = float(PARAM(lambda: neck_width, 180.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 240.0))
wrist_girth   = float(PARAM(lambda: wrist_girth, 180.0))
band_height  = float(PARAM(lambda: band_height, 40.0))
ease         = float(PARAM(lambda: ease, 90.0))            # close, cosy knit fit
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(660.0, min(chest_girth, 1500.0))
hip_girth    = max(700.0, min(hip_girth, 1600.0))
dress_length = max(700.0, min(dress_length, 1350.0))
neck_width   = max(130.0, min(neck_width, 300.0))
sleeve_length = max(350.0, min(sleeve_length, 720.0))
sleeve_depth  = max(180.0, min(sleeve_depth, 360.0))
wrist_girth   = max(130.0, min(wrist_girth, 300.0))
band_height  = max(20.0, min(band_height, 90.0))
ease         = max(20.0, min(ease, 260.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = dress_length
CHEST_HALF = (chest_girth + ease) / 4.0
HIP_HALF   = (hip_girth + ease) / 4.0
NECK_HALF  = neck_width / 2.0
WAIST_Y = L * 0.55
WAIST_HALF = min(CHEST_HALF, HIP_HALF) - 20.0        # slight waist nip


def _panel(name, neck_dip, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    # dropped-shoulder knit armhole: a STRAIGHT vertical of height sleeve_depth so it matches
    # the straight sleevehead exactly (balances by construction).
    shoulder_end = fc.P(CHEST_HALF, top_y)
    armhole_bot = fc.P(CHEST_HALF, top_y - sleeve_depth)
    side_pts = [armhole_bot, fc.P(WAIST_HALF, WAIST_Y), fc.P(HIP_HALF, L * 0.28),
                fc.P(HIP_HALF, 0.0)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[i], side_pts[i + 1]) for i in range(3)])
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                              bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
            fc.Edge("armhole", [fc.Line(shoulder_end, armhole_bot)]),
            side_edge,
            fc.Edge("hem", [fc.Line(fc.P(HIP_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("side", 0.33, "waist")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve():
    head_h = sleeve_depth
    sw = sleeve_length
    wrist = wrist_girth / 2.0
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


def build_band():
    ln = 520.0
    h = band_height * 2.0
    return fc.Piece(
        "band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Ribbed band (neck/cuff/hem)",
    )


def build():
    pattern = fc.PatternSet("sweater-dress")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_panel("front", 60.0, "Front"))
    if everything or target_piece == "back":
        pattern.add(_panel("back", 24.0, "Back"))
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("sleeve", "sleevehead"), ("back", "armhole"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "sweater knit / double-knit / ponte",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 74% marker; a stable sweater knit with recovery."},
        {"item": "rib knit for bands", "qty": 1, "unit": "as measured",
         "note": "rib for the neck, cuffs, and hem; cut to the measured openings."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "knit seams; coverstitch the band joins."},
    ]
    pattern.metadata = {
        "fc200_rank": 188, "family": "dresses_jumpsuits", "fabric_hint": "punto-sweater",
        "silhouette_note": "A long-sleeved knit column dress with a slight waist nip, ribbed "
            "neck/cuffs/hem — the cosy winter pull-on dress. Front and back share the body width "
            "so the seams balance; a set sleeve joins at the armhole.",
        "solved": {"chest_q_mm": round(CHEST_HALF, 1), "hip_q_mm": round(HIP_HALF, 1)},
    }
    return pattern


result = build()
