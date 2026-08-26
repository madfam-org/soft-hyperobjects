"""
Bib-front formal shirt — Fashion Cabinet Garment Cartridge
(FC-500 rank #443, tailoring, T3; y4d sew-through-button).

The stiff-fronted evening dress shirt: a marcella (piqué) or pleated BIB panel across the chest,
worn under a tailcoat or dinner jacket, with studs/buttons down the bib and a wing or turndown
collar. The bib is the garment's defining feature — a separate stiffened panel applied to the
shirt front, its width and drop solved so it sits inside the jacket opening and above the
waistcoat.

Two real decisions:

  1. THE BIB IS SOLVED TO THE CHEST AND SITS INSIDE THE PLACKET. The bib width is a clamped
     fraction of the chest so it never exceeds the shirt front (which would push the bib edge
     past the side seam); its drop is clamped under the shirt length.

  2. THE STUDS ARE SOLVED TO THE BIB. The sew-through buttons/studs run the bib centre; their
     ligne is the drafted button_ligne that drives the garment's button-stand interface AND the
     Yantra4D sew-through-button sew face.

Pieces: front (with placket), bib (the stiff panel), back (cut 1 on fold), sleeve, collar.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|bib|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
back_length = float(PARAM(lambda: back_length, 780.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 360.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
bib_width = float(PARAM(lambda: bib_width, 220.0))
bib_drop = float(PARAM(lambda: bib_drop, 300.0))
button_ligne = float(PARAM(lambda: button_ligne, 18.0))
shirt_ease = float(PARAM(lambda: shirt_ease, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1500.0))
back_length = max(600.0, min(back_length, 920.0))
sleeve_length = max(520.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 520.0))
neck_girth = max(320.0, min(neck_girth, 520.0))
bib_width = max(120.0, min(bib_width, 340.0))
bib_drop = max(160.0, min(bib_drop, 460.0))
button_ligne = max(12.0, min(button_ligne, 30.0))
shirt_ease = max(80.0, min(shirt_ease, 280.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

CHEST_FIN = chest_girth + shirt_ease
FRONT_HALF = CHEST_FIN / 4.0
BACK_HALF = CHEST_FIN / 4.0
ARM_DEPTH = back_length * 0.28
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
BIB_W = min(bib_width, FRONT_HALF * 1.6)      # bib total width clamped under 2 front halves
BIB_DROP = min(bib_drop, back_length * 0.7)


def build_front():
    """Shirt front (cut 2) with a placket at the CF."""
    w = FRONT_HALF
    h = back_length
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 10.0
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)
    arm_top = fc.P(w, h - ARM_DEPTH)
    edges = [
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - NECK_DROP))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h - NECK_DROP),
                                       fc.P(neck_x * 0.35, h - NECK_DROP),
                                       fc.P(neck_x * 0.72, h - NECK_DROP * 0.4), neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7), arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 20.0,
                "center_front": 30.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("center_front", 0.5,
                "placket")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (placket)")


def build_bib():
    """The stiff bib panel (cut 1): a shield of BIB_W x BIB_DROP applied to the front, carrying
    the studs down its centre."""
    w, h = BIB_W, BIB_DROP
    edges = [
        fc.Edge("bottom", [fc.curve_through(fc.P(0.0, 0.0), fc.P(w, 0.0), bulge=0.12, side=-1.0)]),
        fc.Edge("right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "bib", edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("top", 0.5, "centre front"), fc.Notch("bottom", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[fc.Internal("stud-line", [fc.P(w * 0.5, h * 0.12), fc.P(w * 0.5, h * 0.88)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, mirror=False), label="Stiff bib panel (cut 1)")


def build_back():
    w = BACK_HALF
    h = back_length
    neck_x = max(w * 0.20, w - SH_SEAM)
    SH_DROP = 12.0
    NECK_DROP = 10.0
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h), fc.P(neck_x * 0.5, h),
                                       fc.P(neck_x * 0.8, h - NECK_DROP * 0.5),
                                       fc.P(neck_x, h - NECK_DROP))]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h - NECK_DROP), shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 20.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold)")


def build_sleeve(armhole_ring):
    ln = sleeve_length
    wrist = min(bicep_girth * 0.72, armhole_ring * 0.6)
    cap_w = min(armhole_ring * 0.9, wrist * 1.6)
    bow = ARM_DEPTH * 0.55
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln), fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow), fc.P(cap_w, ln))]).length()
        if test < 1e-6:
            break
        ratio = armhole_ring / test
        if ratio > 1.0:
            cap_w = min(cap_w * ratio, armhole_ring)
        else:
            bow = max(4.0, bow * ratio)
        cap_w = max(wrist + 10.0, cap_w)
        if abs(test - armhole_ring) < 0.4:
            break
    cuff_off = (cap_w - wrist) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Line(fc.P(cuff_off, 0.0), fc.P(cuff_off + wrist, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln), fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow), fc.P(0.0, ln))]),
        fc.Edge("seam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance, allowances={"cuff": 30.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"), fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


MEASURED = {}


def build_collar():
    ln = MEASURED.get("neck_run", neck_girth)
    h = 75.0
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Wing/turndown collar (cut 1)")


def build():
    pattern = fc.PatternSet("formal-bib-shirt")
    every = target_piece == "set"
    front = build_front()
    bib = build_bib()
    back = build_back()
    MEASURED["neck_run"] = 2.0 * front.edge("neckline").length() + back.edge("neckline").length()
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    picked = {"front": front, "bib": bib, "back": back, "sleeve": sleeve, "collar": collar}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, bib, back, sleeve, collar):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"), ("back", "neckline")],
                         tol=3.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "cotton poplin (shirt body)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "the shirt body, sleeves and collar; a fine poplin under the stiff bib."},
        {"item": "marcella / piqué (bib)", "qty": round(BIB_W * BIB_DROP / 1000.0),
         "unit": "mm_length",
         "note": "the stiffened bib panel; marcella piqué for white-tie, "
                 "pleated poplin for black-tie."},
        {"item": "shirt studs / buttons (Yantra4D sew-through-button)", "qty": 4, "unit": "piece",
         "note": f"four bib studs, ligne {button_ligne:.0f} = the button_ligne that drives the "
                 "button-stand interface AND the sew-through-button sew face; the stud solid is "
                 "Yantra4D, never modelled here."},
        {"item": "collar + bib interfacing", "qty": round(BIB_DROP + 200.0), "unit": "mm_length",
         "note": "stiffens the bib and the collar so they stand."},
    ]
    pattern.metadata = {
        "fc500_rank": 443, "family": "tailoring", "fabric_hint": "popelina-algodon",
        "silhouette_note": "A bib-front evening dress shirt: a stiff marcella or pleated bib "
            "across the chest with studs down the centre, wing or turndown collar.",
        "hardware": "shirt studs via Yantra4D (notion.hardware_ref -> sew-through-button); "
            "button_ligne drives the button-stand interface and the sew face — the handshake.",
        "solver": {
            "bib_w_mm": round(BIB_W, 1), "bib_drop_mm": round(BIB_DROP, 1),
            "note": "the bib width is clamped under 1.6x the front half so it never exceeds the "
                    "shirt front; the bib drop is clamped under 0.7x the shirt length.",
        },
        "tailoring": {"cut": "bib-front evening dress shirt, stiff applied bib, "
                "wing/turndown collar."},
    }
    return pattern


result = build()
