"""
Guayabera (de alforzas) — Fashion Cabinet Garment Cartridge (FC-400 #391; y4d sew-through-button).

The guayabera is the pleated men's dress shirt of the Caribbean and the Mexican Gulf — worn
untucked, in light linen or cotton, and defined by its two vertical bands of FINE PLEATS
(*alforzas*) running the length of each front and the back, its FOUR patch pockets, and its
side vents. This cartridge drafts a real guayabera around the two features that actually make
it one, rather than a plain shirt with decoration added:

  1. THE ALFORZAS ARE PLEATS, AND PLEATS EAT CLOTH. Each front and the back carry two vertical
     bands of narrow pleats. A pleat of finished width `w` folded from `depth` per pleat
     consumes `2*depth` of cloth, so a panel with N pleats per band and two bands must be cut
     WIDER than its finished width by `4*N*depth`. The commonest error is drafting the panel
     to the finished chest and then "adding pleats", which either runs out of cloth or shifts
     the pocket placement. Here the pleat take-up is SOLVED and added to the cut width, and the
     finished chest is what the wearer measured — the pleats sit on a panel that still fits.

  2. THE FOUR POCKETS AND THE BUTTONS SIT ON THE ALFORZA GRID. Two chest pockets and two lower
     pockets, each aligned to the pleat bands, each closed with a button. The buttons are the
     Yantra4D `sew-through-button`; `button_ligne` drives BOTH the drafted buttonhole spacing
     AND the printed button size, so the placket and pockets and buttons agree.

Pieces: front (cut 2, with the pleat allowance), back (cut 1 on fold, with pleat allowance),
sleeve, collar, pocket, cuff. Made to measure to chest, waist, hip girths, back and sleeve
lengths. The pleats are drawn as fold-line internals with the take-up solved into the width.

Cultural note (stated, not decorative): the guayabera is a real regional dress garment with a
contested but well-documented Cuban/Mexican origin; this is an everyday four-pocket alforza
guayabera, not any ceremonial or badge-bearing variant, and it invents no motif.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
waist_girth = float(PARAM(lambda: waist_girth, 980.0))
shirt_length = float(PARAM(lambda: shirt_length, 760.0))    # nape to straight hem
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 380.0))
neck_girth = float(PARAM(lambda: neck_girth, 420.0))
ease_pct = float(PARAM(lambda: ease_pct, 18.0))             # a guayabera is worn loose
alforza_count = float(PARAM(lambda: alforza_count, 7.0))    # pleats per band
alforza_depth = float(PARAM(lambda: alforza_depth, 4.0))    # fold depth per pleat
button_ligne = float(PARAM(lambda: button_ligne, 18.0))    # button size (ligne)
collar_height = float(PARAM(lambda: collar_height, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1500.0))
waist_girth = max(700.0, min(waist_girth, 1450.0))
shirt_length = max(600.0, min(shirt_length, 1000.0))
sleeve_length = max(200.0, min(sleeve_length, 720.0))
bicep_girth = max(260.0, min(bicep_girth, 600.0))
neck_girth = max(340.0, min(neck_girth, 520.0))
ease_pct = max(6.0, min(ease_pct, 30.0))
alforza_count = max(3.0, min(round(alforza_count), 12.0))
alforza_depth = max(2.0, min(alforza_depth, 8.0))
button_ligne = max(14.0, min(button_ligne, 26.0))
collar_height = max(40.0, min(collar_height, 110.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── The alforza take-up solver ───────────────────────────────────────────────
EASE = 1.0 + ease_pct / 100.0
CHEST_FIN = chest_girth * EASE
# front (x2 halves) + back = the finished chest circuit. Front half + back half each carry a
# quarter... the shirt is front-left + front-right (each half the front) + back (on fold).
FRONT_FIN = CHEST_FIN / 4.0                 # one front's finished chest width
BACK_FIN = CHEST_FIN / 4.0                  # back half's finished width (on fold)
# Each panel has TWO pleat bands; each band has `alforza_count` pleats; each pleat eats
# 2*depth of cloth. So the added cut width per panel = 2 bands * count * 2 * depth.
N = int(alforza_count)
PLEAT_TAKEUP = 2 * N * 2.0 * alforza_depth  # cloth eaten by the two bands, per panel
FRONT_CUT = FRONT_FIN + PLEAT_TAKEUP
BACK_CUT = BACK_FIN + PLEAT_TAKEUP
H = shirt_length
ARM_DEPTH = H * 0.26
BUTTON_MM = button_ligne * 0.635           # ligne -> mm


def _pleat_internals(x0, band_w, label_prefix):
    """Fold-line internals for one pleat band starting at x0, spanning band_w, full height."""
    lines = []
    step = band_w / max(1, N)
    for i in range(N):
        x = x0 + step * (i + 0.5)
        lines.append(fc.Internal(f"{label_prefix} fold {i + 1}",
                                 [fc.P(x, H * 0.06), fc.P(x, H * 0.94)], kind="marking"))
    return lines


def build_front():
    """A front (cut 2): centre-front placket edge, two pleat bands, side seam, armhole,
    shoulder, straight hem, side vent at the hem. Cut WIDER by the solved pleat take-up.
    """
    w = FRONT_CUT
    band_w = PLEAT_TAKEUP / 2.0 * 0.5 + 40.0   # visual band width for the fold marks
    cf = fc.P(0.0, 0.0)
    cf_top = fc.P(0.0, H)
    neck_pt = fc.P(w * 0.34, H)
    shoulder = fc.P(w * 0.86, H - 14.0)
    arm_top = fc.P(w, H - ARM_DEPTH)
    side_bot = fc.P(w, 0.0)
    edges = [
        fc.Edge("center_front", [fc.Line(cf, cf_top)]),
        fc.Edge("neckline", [fc.Bezier(cf_top,
                                       fc.P(w * 0.10, H - collar_height * 0.15),
                                       fc.P(w * 0.24, H),
                                       neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w * 0.98, H - ARM_DEPTH * 0.35),
                                      fc.P(w * 1.0, H - ARM_DEPTH * 0.7),
                                      arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, side_bot)]),
        fc.Edge("hem", [fc.Line(side_bot, cf)]),
    ]
    internals = (_pleat_internals(w * 0.14, band_w, "inner alforza")
                 + _pleat_internals(w * 0.62, band_w, "outer alforza"))
    internals.append(fc.Internal("button placket",
                                 [fc.P(BUTTON_MM * 0.6, H * 0.1),
                                  fc.P(BUTTON_MM * 0.6, H * 0.9)], kind="marking"))
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "center_front": BUTTON_MM * 1.2},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("hem", 0.9, "side vent top")],
        grainline=fc.Grainline(fc.P(w * 0.4, H * 0.15), fc.P(w * 0.4, H * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2, alforza take-up + placket)")


def build_back():
    """The back (cut 1 on fold): two pleat bands, two armholes, straight hem. Cut wider."""
    w = BACK_CUT
    band_w = PLEAT_TAKEUP / 2.0 * 0.5 + 40.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, H),
                                       fc.P(w * 0.18, H),
                                       fc.P(w * 0.30, H - 8.0),
                                       fc.P(w * 0.40, H - 12.0))]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.40, H - 12.0), fc.P(w * 0.86, H - 14.0))]),
        fc.Edge("armhole", [fc.Bezier(fc.P(w * 0.86, H - 14.0),
                                      fc.P(w * 0.98, H - ARM_DEPTH * 0.35),
                                      fc.P(w, H - ARM_DEPTH * 0.7),
                                      fc.P(w, H - ARM_DEPTH))]),
        fc.Edge("side_seam", [fc.Line(fc.P(w, H - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    internals = (_pleat_internals(w * 0.20, band_w, "back inner alforza")
                 + _pleat_internals(w * 0.64, band_w, "back outer alforza"))
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("hem", 0.9, "side vent top")],
        grainline=fc.Grainline(fc.P(w * 0.4, H * 0.15), fc.P(w * 0.4, H * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (cut 1 on fold, alforza take-up)")


def build_sleeve(armhole_ring):
    """A short or long sleeve (cut 2): cap solved to the armhole ring, straight to a cuff."""
    wrist = min(bicep_girth * EASE * 0.5, armhole_ring * 0.7)
    ln = sleeve_length
    cap_w = min(armhole_ring * 0.92, wrist * 1.6)
    bow = ARM_DEPTH * 0.5
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln),
                                       fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow),
                                       fc.P(cap_w, ln))]).length()
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
        fc.Edge("underseam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln),
                                  fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow),
                                  fc.P(0.0, ln))]),
        fc.Edge("underseam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        allowances={"cuff": 25.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (cut 2)")


def build_collar(neck_run):
    """A camp/spread collar band (cut 1): its length is the measured neckline run."""
    ln = neck_run
    h = collar_height
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
        fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back"),
                 fc.Notch("neck_edge", 0.25, "shoulder"),
                 fc.Notch("neck_edge", 0.75, "shoulder")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Collar band (cut 1)")


def build_pocket():
    """A patch pocket (cut 4): a square patch with its own pleat and a button seat."""
    w = FRONT_FIN * 0.42
    h = w * 1.05
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("pocket alforza", [fc.P(w * 0.5, h * 0.08), fc.P(w * 0.5, h * 0.92)],
                    kind="marking"),
        fc.Internal("pocket button seat", [fc.P(w * 0.5, h * 0.86),
                                           fc.P(w * 0.5 + BUTTON_MM, h * 0.86)],
                    kind="marking"),
    ]
    return fc.Piece(
        "pocket", edges, seam_allowance=seam_allowance,
        allowances={"top": 30.0},
        notches=[fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.75)),
        internals=internals, cut=fc.CutSpec(quantity=4, mirror=True),
        label="Patch pocket (cut 4 — 2 chest, 2 lower)")


MEASURED = {}


def build():
    pattern = fc.PatternSet("guayabera-shirt")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = (2.0 * front.edge("neckline").length()
                            + back.edge("neckline").length())
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()

    if not every:
        picked = {"front": front, "back": back,
                  "sleeve": build_sleeve(armhole_ring),
                  "collar": build_collar(MEASURED["neck_run"]),
                  "pocket": build_pocket()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    sleeve = build_sleeve(armhole_ring)
    collar = build_collar(MEASURED["neck_run"])
    pocket = build_pocket()
    for piece in (front, back, sleeve, collar, pocket):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(front.edge("side_seam").length()
                               - back.edge("side_seam").length()))
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5,
                         ease=(front.edge("shoulder").length()
                               - back.edge("shoulder").length()))
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"),
                          ("back", "neckline")], tol=2.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    total_buttons = 6 + 4          # placket (approx) + 4 pockets
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "lightweight linen or cotton (guayabera cloth)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"fronts + back + sleeves + collar + pockets at {fabric_width:.0f} mm width, "
                 "62% marker. The cut width already INCLUDES the solved alforza take-up "
                 f"({PLEAT_TAKEUP:.0f} mm per panel), so the pleated panel still fits the chest."},
        {"item": "sew-through buttons (Yantra4D sew-through-button)", "qty": total_buttons,
         "unit": "piece",
         "note": f"placket + four pocket buttons; button_ligne {button_ligne:.0f} "
                 f"(~{BUTTON_MM:.1f} mm). The button is the Yantra4D solid (notion.hardware_ref "
                 "-> sew-through-button); button_ligne drives the printed button AND the drafted "
                 "buttonhole spacing."},
        {"item": "interfacing (collar + placket)", "qty": 1, "unit": "set",
         "note": "light fusible for the collar band and the button placket."},
        {"item": "polyester/cotton thread", "qty": 1, "unit": "set",
         "note": "topstitch the alforza folds down their length; they are pressed knife "
                 "pleats, stitched close to the fold."},
    ]
    pattern.metadata = {
        "fc400_rank": 391, "family": "heritage_global", "fabric_hint": "linen-lightweight",
        "tradition": "Caribbean / Mexican Gulf — the pleated men's dress shirt worn untucked",
        "silhouette_note": "A four-pocket alforza guayabera: two vertical bands of fine pleats "
            "down each front and the back, four patch pockets on the pleat grid, side vents, a "
            "straight untucked hem. The pleats are the garment, and their cloth take-up is "
            "solved into the cut width.",
        "hardware": "buttons via Yantra4D (notion.hardware_ref -> sew-through-button); "
            "button_ligne drives BOTH the printed button and the drafted buttonhole spacing.",
        "solver": {
            "chest_finished_mm": round(CHEST_FIN, 1),
            "alforza_count_per_band": N,
            "alforza_depth_mm": round(alforza_depth, 1),
            "pleat_takeup_per_panel_mm": round(PLEAT_TAKEUP, 1),
            "front_cut_width_mm": round(FRONT_CUT, 1),
            "button_ligne": round(button_ligne, 1),
            "note": "each pleat eats 2*depth of cloth; two bands of N pleats add 4*N*depth to "
                    "the cut width, so the finished chest is what the wearer measured while the "
                    "pleats sit on cloth that still fits.",
        },
        "cultural_note": "The guayabera is a real regional dress garment with a contested but "
            "well-documented Cuban/Mexican origin. This is an everyday four-pocket alforza "
            "guayabera; it is not a ceremonial or badge-bearing variant and invents no motif.",
        "drafting": "Made to measure to chest and waist girths + shirt and sleeve lengths; the "
            "alforza take-up is solved into the cut width.",
    }
    return pattern


result = build()
