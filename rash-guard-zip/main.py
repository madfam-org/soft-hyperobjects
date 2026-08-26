"""
Zip-front rash guard — Fashion Cabinet Garment Cartridge (FC-400 #390; y4d zipper).

A zip-front long-sleeve rash guard in swim-lycra: the second-skin UV surf top, but split down
the centre front and closed with a full separating zipper, so it can be got on and off wet
without dragging it over the head. It deepens the FC-100 pull-on rash guard (#57, no hardware)
into the zip version — the one surfers and swimmers actually reach for, because a wet pull-on
rash guard is a fight and a zip one is not.

Two real decisions:

  1. THE ZIP IS SOLVED TO THE FRONT LENGTH — THE DIMENSIONAL HANDSHAKE. The front is split
     into a left and a right half, and the centre-front edges carry the separating zipper. The
     Yantra4D `zipper` solid is parameterised by `zip_length`; here `zip_length` IS the drafted
     centre-front run from hem to collar, so the printed/specified zipper is exactly as long as
     the opening it closes. `zip_length` drives BOTH the hardware AND the garment's own
     `center_front` interface — one number, two objects. A zipper too short leaves a gap at the
     collar; too long buckles the hem. Solving it removes the guess.

  2. NEGATIVE EASE STILL RULES, BUT THE ZIP TAPE IS STABLE. A rash guard is a second skin, cut
     at negative ease so the lycra grips and does not billow in the water. But the zipper tape
     is NOT stretchy, so the centre-front seam is stabilised and the negative ease is taken up
     everywhere EXCEPT the zip line — the front halves are cut to close flat at the tape while
     the side and back keep the grip.

Pieces: front-left, front-right, back, sleeve, collar. Made to measure to chest, waist, hip
girths, back length and sleeve length. Flatlock seams throughout for chafe-free wear.

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

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
waist_girth = float(PARAM(lambda: waist_girth, 840.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
back_length = float(PARAM(lambda: back_length, 620.0))     # nape to hem
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))  # shoulder to wrist
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
collar_height = float(PARAM(lambda: collar_height, 60.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1500.0))
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(700.0, min(hip_girth, 1600.0))
back_length = max(420.0, min(back_length, 900.0))
sleeve_length = max(300.0, min(sleeve_length, 780.0))
bicep_girth = max(220.0, min(bicep_girth, 600.0))
neck_girth = max(300.0, min(neck_girth, 560.0))
collar_height = max(20.0, min(collar_height, 120.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The negative-ease solver ─────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
WAIST_FIN = waist_girth * NEG
HIP_FIN = hip_girth * NEG
NECK_FIN = neck_girth                       # collar opening not compressed (breathing)
# The body is front-left + front-right + back. Front total = half the body, split in two;
# back = half the body. So each front half = a quarter of the body ring.
FRONT_HALF = CHEST_FIN / 4.0                # one front half's chest width
BACK_HALF = CHEST_FIN / 2.0
ARM_DEPTH = back_length * 0.30              # armhole depth
# A shared shoulder-seam length so front-half and back shoulders are congruent (both sit
# from the neck point out to the shoulder point, and that run is the same on both).
SH_SEAM = min(FRONT_HALF, BACK_HALF) * 0.30 + 40.0
# THE ZIP HANDSHAKE: the zip length is the centre-front run from hem to collar top.
ZIP_LENGTH = back_length + collar_height


def build_front_half(is_left, label):
    """A front half (left or right): centre-front edge (carries the zip), side seam, armhole,
    shoulder, hem. The CF edge is drafted straight and stable for the zipper tape; the ease is
    taken up on the side seam. `sign` flips the geometry for left vs right.
    """
    w = FRONT_HALF
    h = back_length
    # Author both halves in a local frame with CF at x=0 rising to x=w at the side.
    # The neck point sits at x = w - SH_SEAM_X so the shoulder seam runs SH_SEAM to the
    # shoulder point at the side; that makes the front-half shoulder congruent with the back.
    cf_bot = fc.P(0.0, 0.0)
    cf_top = fc.P(0.0, h)                     # centre-front to the neck point
    neck_x = max(w * 0.30, w - SH_SEAM)
    SH_DROP = 12.0                            # fixed shoulder-point drop (front == back)
    NECK_DROP = 8.0                           # neck-point drop (front == back), so the
    # shoulder seam runs neck(neck_x, h-NECK_DROP) -> shoulder(w, h-SH_DROP) identically.
    neck_pt = fc.P(neck_x, h - NECK_DROP)
    shoulder = fc.P(w, h - SH_DROP)          # shoulder point at the side top
    arm_top = fc.P(w, h - ARM_DEPTH)
    side_bot = fc.P(w, 0.0)
    edges = [
        fc.Edge("center_front", [fc.Line(cf_bot, cf_top)]),
        fc.Edge("neckline", [fc.Bezier(cf_top,
                                       fc.P(neck_x * 0.35, h - collar_height * 0.15),
                                       fc.P(neck_x * 0.72, h),
                                       neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w + SH_SEAM * 0.10, h - ARM_DEPTH * 0.35),
                                      fc.P(w + SH_SEAM * 0.06, h - ARM_DEPTH * 0.7),
                                      arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, side_bot)]),
        fc.Edge("hem", [fc.Line(side_bot, cf_bot)]),
    ]
    internals = [fc.Internal("zip line",
                             [fc.P(0.0, h * 0.04), fc.P(0.0, h * 0.96)], kind="marking")]
    name = "front_left" if is_left else "front_right"
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"center_front": 0.0, "hem": 20.0, "neckline": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("center_front", 0.5, "zip midpoint")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_back():
    """The back panel (cut 1 on fold at centre back), symmetric. Two armholes, one neckline."""
    w = BACK_HALF
    h = back_length
    # Neck point sits SH_SEAM inboard of the shoulder point (at the side), so the back
    # shoulder run == SH_SEAM == each front-half shoulder run.
    neck_x = max(w * 0.20, w - SH_SEAM)
    SH_DROP = 12.0                            # same fixed drop as the front half
    NECK_DROP = 8.0                           # back neck point drop (shallow, fixed)
    shoulder = fc.P(w, h - SH_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h),
                                       fc.P(neck_x * 0.5, h),
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
        "back", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "neckline": 0.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back panel (cut 1 on fold)")


def build_sleeve(armhole_ring):
    """A fitted set-in sleeve (cut 2): sleeve cap SOLVED to the armhole ring, tapering to the
    wrist at negative ease. Drafted flat, symmetric about its centre.

    The cap is a shallow arc whose true run equals `armhole_ring` (one front-half armhole +
    the back armhole), so the sleeve sets in without easing a mismatch.
    """
    ln = sleeve_length
    # The cuff (wrist) is capped so it never exceeds the cap width the armhole allows — a
    # sleeve head is always wider than the wrist, and clamping the wrist keeps the geometry
    # valid at the bicep extreme.
    wrist = min(bicep_girth * NEG * 0.62, armhole_ring * 0.62)   # tapered wrist (cuff width)
    # The cap spans the FULL sleeve-head width at the top (y=ln); the cuff is the narrow
    # wrist at the bottom (y=0), centred. Solve cap_w so the cap arc's run ~ armhole_ring by
    # iterating BOTH the width and the bow so a small ring gets a flatter, narrower cap.
    cap_w = min(armhole_ring * 0.9, wrist * 1.4)   # first guess (chord < arc run)
    bow = ARM_DEPTH * 0.55
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln),
                                       fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow),
                                       fc.P(cap_w, ln))]).length()
        if test < 1e-6:
            break
        ratio = armhole_ring / test
        if ratio > 1.0:
            cap_w = min(cap_w * ratio, armhole_ring)     # widen toward the target
        else:
            bow *= ratio                                 # too long: flatten the bow
            bow = max(4.0, bow)
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
        allowances={"cuff": 15.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cuff", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2)")


def build_collar():
    """The stand collar (cut 1) topped by the zip. Its length is the measured neckline run;
    its height is `collar_height`. The zip continues up the centre-front to the collar top.
    """
    ln = MEASURED.get("neck_run", NECK_FIN)
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
        cut=fc.CutSpec(quantity=1),
        label="Stand collar (cut 1, zip continues to its top)")


MEASURED = {}


def build():
    pattern = fc.PatternSet("rash-guard-zip")
    every = target_piece == "set"
    fl = build_front_half(True, "Front left (zip edge)")
    fr = build_front_half(False, "Front right (zip edge)")
    back = build_back()
    # Collar run = both front necklines + back neckline (measured).
    MEASURED["neck_run"] = (fl.edge("neckline").length() + fr.edge("neckline").length()
                            + back.edge("neckline").length())

    armhole_ring = fl.edge("armhole").length() + back.edge("armhole").length()

    if not every:
        picked = {"front_left": fl, "front_right": fr, "back": back,
                  "sleeve": build_sleeve(armhole_ring), "collar": build_collar()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, fl, fr, back)

    sleeve = build_sleeve(armhole_ring)
    collar = build_collar()
    for piece in (fl, fr, back, sleeve, collar):
        pattern.add(piece)
    # Side seams: each front half to the back (the back has one side edge per side).
    pattern.declare_seam(("front_left", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(fl.edge("side_seam").length()
                               - back.edge("side_seam").length()))
    pattern.declare_seam(("front_right", "side_seam"), ("back", "side_seam"), tol=1.5,
                         ease=(fr.edge("side_seam").length()
                               - back.edge("side_seam").length()))
    # Shoulders.
    pattern.declare_seam(("front_left", "shoulder"), ("back", "shoulder"), tol=1.0)
    pattern.declare_seam(("front_right", "shoulder"), ("back", "shoulder"), tol=1.0)
    # Sleeve cap SOLVED to ONE front-half armhole + the back armhole (one arm's ring).
    pattern.declare_seam(("sleeve", "cap"),
                         [("front_left", "armhole"), ("back", "armhole")], tol=2.5)
    # Collar to the assembled neckline.
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front_left", "neckline"), ("front_right", "neckline"),
                          ("back", "neckline")], tol=1.5)

    return _finish(pattern, fl, fr, back)


def _finish(pattern, fl, fr, back):
    cf_run = fl.edge("center_front").length()
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "swim lycra (UV, chlorine/salt-resistant, 4-way)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"fronts + back + sleeves + collar at {fabric_width:.0f} mm width, 60% "
                 "marker. Negative-ease throughout so the rash guard is a second skin."},
        {"item": "separating zipper (Yantra4D zipper)", "qty": 1, "unit": "piece",
         "note": f"a full separating front zipper; zip_length {ZIP_LENGTH:.0f} mm = the "
                 "drafted centre-front run + collar. The zipper is the Yantra4D solid "
                 "(notion.hardware_ref -> zipper), never modelled here; zip_length IS the "
                 "opening it closes, so it fits by construction."},
        {"item": "zip tape stabiliser tape", "qty": round(ZIP_LENGTH * 2.1), "unit": "mm_length",
         "note": f"two centre-front edges x {ZIP_LENGTH:.0f} mm — the zip tape is not "
                 "stretchy, so the CF is stabilised while the side/back keep the negative "
                 "ease."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so nothing chafes a wet body; a rash guard's whole "
                 "purpose is chafe-free wear."},
    ]
    pattern.metadata = {
        "fc400_rank": 390, "family": "active_swim", "fabric_hint": "swim-lycra",
        "silhouette_note": "A zip-front long-sleeve rash guard: the second-skin UV top split "
            "down the centre front and closed with a full separating zipper, so it comes on "
            "and off wet without a fight. Negative-ease everywhere except the stabilised zip "
            "line.",
        "hardware": "separating zipper via Yantra4D (notion.hardware_ref -> zipper); "
            "zip_length IS the drafted centre-front run + collar, so the printed zipper is "
            "exactly as long as the opening — the dimensional handshake.",
        "solver": {
            "zip_length_mm": round(ZIP_LENGTH, 1),
            "cf_run_mm": round(cf_run, 1),
            "collar_height_mm": round(collar_height, 1),
            "chest_finished_mm": round(CHEST_FIN, 1),
            "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "note": "zip_length == cf_run + collar_height: the zipper and the opening are one "
                    "solved dimension.",
        },
        "drafting": "Made to measure to chest, waist, hip girths + back and sleeve lengths; "
            "negative-ease second skin with a solved separating front zip.",
    }
    return pattern


result = build()
