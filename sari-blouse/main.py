"""
Sari Blouse (Choli) — Fashion Cabinet Garment Cartridge (FC-200 rank #144, South Asian heritage).

The choli is the fitted, cropped blouse worn with the sari and lehenga across South Asia:
close-fitting to the bust with a short hem above the midriff, short set-in sleeves, a
front or back opening, and — the signature — bust darts (and often a princess or waist
dart) that give it its fit. This cartridge drafts the garment geometry: a fitted front
with a bust dart and a back with a shaping dart, short sleeves, and a marked back opening.
Offered with respect for the living tradition; the maker supplies the silk, the mirror
(shisha) work, the borders, and the embroidery.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|set

bust_girth   = float(PARAM(lambda: bust_girth, 880.0))     # full bust
under_bust   = float(PARAM(lambda: under_bust, 760.0))     # underbust (the choli hem sits here)
blouse_length = float(PARAM(lambda: blouse_length, 360.0))  # shoulder to short hem
shoulder_w   = float(PARAM(lambda: shoulder_w, 110.0))     # shoulder width (half)
sleeve_length = float(PARAM(lambda: sleeve_length, 150.0))  # short sleeve
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 130.0))  # armhole depth
bust_dart     = float(PARAM(lambda: bust_dart, 45.0))      # bust-dart intake
bust_ease     = float(PARAM(lambda: bust_ease, 40.0))      # close fit ease
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth    = max(650.0, min(bust_girth, 1300.0))
under_bust    = max(550.0, min(under_bust, bust_girth))
blouse_length = max(220.0, min(blouse_length, 500.0))
shoulder_w    = max(70.0, min(shoulder_w, 180.0))
sleeve_length = max(60.0, min(sleeve_length, 320.0))
sleeve_depth  = max(90.0, min(sleeve_depth, 220.0))
bust_dart     = max(0.0, min(bust_dart, 90.0))
bust_ease     = max(10.0, min(bust_ease, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

L = blouse_length
FRONT_Q = (bust_girth + bust_ease) / 4.0            # front quarter at bust
BACK_Q = (under_bust + bust_ease) / 4.0             # back quarter (narrower, snug)
NECK_HALF = 60.0
SHOULDER_Y = L
UNDERARM_Y = L - sleeve_depth


def _bodice(name, quarter, neck_dip, dart, label):
    """A fitted half-bodice cut on fold at centre: shoulder, straight-ish armhole to the
    underarm, straight side to the short hem, hem, centre, neck scoop. A bust/shaping dart
    is marked from the side toward the apex (teaching-grade — kept as a marking)."""
    neck_pt = fc.P(0.0, SHOULDER_Y - neck_dip)
    neck_out = fc.P(NECK_HALF, SHOULDER_Y)
    shoulder_pt = fc.P(shoulder_w, SHOULDER_Y - 10.0)
    underarm = fc.P(quarter, UNDERARM_Y)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, shoulder_pt)]),
        fc.Edge("armhole", [fc.curve_through(shoulder_pt, underarm, bulge=0.16, side=1.0)]),
        fc.Edge("side", [fc.Line(underarm, fc.P(quarter, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(quarter, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if dart > 0.0:
        apex = fc.P(quarter * 0.45, UNDERARM_Y - 40.0)
        internals.append(fc.Internal("bust-dart", [
            fc.P(quarter, UNDERARM_Y - 30.0 - dart / 2.0), apex,
            fc.P(quarter, UNDERARM_Y - 30.0 + dart / 2.0)], kind="dart"))
    if name == "back":
        internals.append(fc.Internal("back-opening",
                                     [fc.P(0.0, 0.0), fc.P(0.0, SHOULDER_Y - neck_dip)],
                                     kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 0.0, "shoulder"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(quarter * 0.5, 40.0), fc.P(quarter * 0.5, L - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_sleeve():
    """A short set-in sleeve: a shallow cap (curved sleevehead) and a straight short body
    to the opening."""
    sw = FRONT_Q * 0.9                                  # sleeve width at the bicep
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, sleeve_length))]),
            fc.Edge("cap", [fc.curve_through(fc.P(0.0, sleeve_length), fc.P(sw, sleeve_length),
                                             bulge=0.18, side=1.0)]),
            fc.Edge("underarm_r", [fc.Line(fc.P(sw, sleeve_length), fc.P(sw, 0.0))]),
            fc.Edge("opening", [fc.Line(fc.P(sw, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"opening": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(sw * 0.5, sleeve_length * 0.2),
                               fc.P(sw * 0.5, sleeve_length * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def build():
    pattern = fc.PatternSet("sari-blouse")
    front = _bodice("front", FRONT_Q, 80.0, bust_dart, "Front")
    back = _bodice("back", BACK_Q, 25.0, bust_dart * 0.5, "Back")

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())

    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=2.0)
        # Front and back side seams: front quarter (bust) vs back quarter (underbust) differ,
        # so the side is a genuine ease seam — declare with the small ease the fit intends.
        fside = front.edge("side").length(0.05)
        bside = back.edge("side").length(0.05)
        pattern.declare_seam(("front", "side"), ("back", "side"),
                             ease=round(fside - bside, 1), tol=2.0)

    fabric_width = 1100.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.65)
    pattern.bom = [
        {"item": "silk or cotton blouse fabric",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1100 mm width, 65% marker; often cut from the sari's pallu or a "
                 "contrast piece — the border and mirror (shisha) work are the maker's."},
        {"item": "hook-and-eye or dori (tie) back closure", "qty": 1, "unit": "set",
         "note": "the back opening closes with hooks or a tie — maker's choice."},
        {"item": "lining / interfacing", "qty": 1, "unit": "as needed",
         "note": "a fitted choli is usually lined; cups optional."},
    ]
    pattern.metadata = {
        "fc200_rank": 144,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "heritage_note": "The choli (sari blouse) is a living South Asian garment. This "
            "cartridge drafts the fitted GARMENT GEOMETRY only — the silk, the border, the "
            "mirror (shisha) work, and the embroidery that carry its identity are the "
            "maker's to supply. The bust dart is marked (teaching-grade). Offered with respect.",
        "fit_note": "Front quarter shaped to the bust, back quarter to the underbust for a "
            "snug fit; the bust dart is marked from the side toward the apex (kept as a "
            "marking rather than rotated). The side seam carries a small intended ease.",
        "drafting": "fitted front + back on fold with marked bust/shaping darts + a short "
            "set-in sleeve; short hem above the midriff; back opening marked.",
    }
    return pattern


result = build()
