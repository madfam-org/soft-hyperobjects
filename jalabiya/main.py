"""
Jalabiya / Gulf thobe — Fashion Cabinet Garment Cartridge (FC-400 #392; y4d sew-through-button).

The thobe (thawb) of the Arabian Gulf — a long, ankle-length robe of white cotton poplin,
straight and flowing, with long set-in sleeves, a short front placket closed by small buttons,
and a slim stand collar. It is cut for grace and coolness, not for fit, and this cartridge
drafts it around the two facts that make a thobe hang the way it should:

  1. THE FLARE IS GODETS AT THE SIDE, NOT A SHAPED SIDE SEAM. A thobe reads as a straight column
     at the shoulder that flares to a wide sweep at the hem. That flare is not cut as a curved
     side seam (which would drag the grain and pull the drape sideways); it is added as
     triangular SIDE GORES (godets) inserted from the underarm to the hem, so the body panels
     stay on grain and hang plumb while the hem still sweeps wide. This cartridge cuts the body
     as straight panels and a separate godet, and solves the godet's flare from the target hem
     sweep.

  2. THE PLACKET IS SHORT AND THE COLLAR IS SLIM. The thobe opens only at a short neck placket
     (it is pulled over the head), closed by a few small buttons, under a slim stand collar. The
     buttons are the Yantra4D `sew-through-button`; `button_ligne` drives BOTH the printed button
     and the drafted placket button spacing.

Pieces: front (cut 1 on fold), back (cut 1 on fold), side godet, sleeve, collar, placket. Made to
measure to chest girth, robe length, sleeve length, hem sweep and neck girth.

Cultural note (stated): the Gulf thobe is everyday and formal men's dress across the Arabian
Peninsula, with regional collar and cuff variations. This is a plain everyday thobe; it carries
no regional insignia and invents no ornament.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import math

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
robe_length = float(PARAM(lambda: robe_length, 1400.0))     # nape to ankle
sleeve_length = float(PARAM(lambda: sleeve_length, 640.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 380.0))
neck_girth = float(PARAM(lambda: neck_girth, 420.0))
hem_sweep = float(PARAM(lambda: hem_sweep, 1900.0))         # full hem circumference
placket_length = float(PARAM(lambda: placket_length, 260.0))
collar_height = float(PARAM(lambda: collar_height, 45.0))
button_ligne = float(PARAM(lambda: button_ligne, 15.0))
ease_pct = float(PARAM(lambda: ease_pct, 22.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1500.0))
robe_length = max(1000.0, min(robe_length, 1800.0))
sleeve_length = max(400.0, min(sleeve_length, 760.0))
bicep_girth = max(260.0, min(bicep_girth, 600.0))
neck_girth = max(340.0, min(neck_girth, 520.0))
hem_sweep = max(1200.0, min(hem_sweep, 3000.0))
placket_length = max(120.0, min(placket_length, 420.0))
collar_height = max(25.0, min(collar_height, 90.0))
button_ligne = max(12.0, min(button_ligne, 22.0))
ease_pct = max(10.0, min(ease_pct, 35.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

placket_length = min(placket_length, robe_length - 200.0)

# ── The flare solver: body straight, godets carry the sweep ──────────────────
EASE = 1.0 + ease_pct / 100.0
CHEST_CUT = chest_girth * EASE
BODY_HALF = CHEST_CUT / 4.0            # half of one straight panel (on fold)
H = robe_length
ARM_DEPTH = H * 0.16
BUTTON_MM = button_ligne * 0.635
# The straight body gives a hem of CHEST_CUT (columnar). The extra sweep is carried by the
# side godets: total added sweep = hem_sweep - CHEST_CUT, split over TWO godets (one per side).
ADDED_SWEEP = max(0.0, hem_sweep - CHEST_CUT)
# Floor each godet to a real minimum so a narrow-sweep thobe still has a valid gore (a thobe
# always has at least a small side gore for the walking split); a zero-width triangle is not
# a piece.
GODET_HEM = max(60.0, ADDED_SWEEP / 2.0)   # each godet's hem width
# The godet is a triangle from the underarm point (0 width) to GODET_HEM at the hem, over the
# height from the underarm to the hem.
GODET_H = H - ARM_DEPTH


def _body(name, is_front, label):
    """A straight body panel (cut 1 on fold): columnar, no side flare. The side seam is
    vertical; the godet is inserted into it separately. CCW: center (fold, up) -> neckline
    -> shoulder -> armhole -> side_seam (down) -> hem (in).
    """
    w = BODY_HALF
    h = H
    if is_front:
        neck_bottom = fc.P(0.0, h - collar_height * 0.4)
    else:
        neck_bottom = fc.P(0.0, h - collar_height * 0.2)
    neck_pt = fc.P(w * 0.34, h)
    shoulder = fc.P(w * 0.86, h - 14.0)
    arm_top = fc.P(w, h - ARM_DEPTH)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_bottom)]),
        fc.Edge("neckline", [fc.Bezier(neck_bottom,
                                       fc.P(w * 0.10, h - collar_height * 0.15),
                                       fc.P(w * 0.24, h),
                                       neck_pt)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, shoulder)]),
        fc.Edge("armhole", [fc.Bezier(shoulder,
                                      fc.P(w * 0.98, h - ARM_DEPTH * 0.35),
                                      fc.P(w * 1.0, h - ARM_DEPTH * 0.7),
                                      arm_top)]),
        fc.Edge("side_seam", [fc.Line(arm_top, fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if is_front:
        internals.append(fc.Internal("front placket",
                                     [fc.P(BUTTON_MM * 0.6, h - placket_length),
                                      fc.P(BUTTON_MM * 0.6, h - 6.0)], kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"hem": 30.0, "center": 0.0, "neckline": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("side_seam", 1.0, "godet top (underarm)")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.1), fc.P(w * 0.4, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label)


def build_front():
    return _body("front", True, "Front (cut 1 on fold, short placket)")


def build_back():
    return _body("back", False, "Back (cut 1 on fold)")


def build_godet():
    """A side godet (cut 2): an isosceles triangle whose two SLANTED edges each equal the
    body side-seam length (GODET_H), splayed apart so the hem opens to GODET_HEM. Because the
    slant edges equal the side seam, the godet sets into the slit side seam WITHOUT easing —
    the hem width comes from the splay, not from stretching a longer edge onto a shorter one.

    slant = GODET_H (matches the side seam); half-hem hw = GODET_HEM/2, clamped so the
    triangle is valid (hw < slant); the apex height is sqrt(slant^2 - hw^2).
    """
    slant = GODET_H
    hw = min(GODET_HEM / 2.0, slant * 0.98)      # keep the triangle valid at wide sweeps
    apex_h = math.sqrt(max(1.0, slant * slant - hw * hw))
    apex = fc.P(0.0, apex_h)                      # underarm point (zero width)
    edges = [
        fc.Edge("seam_front", [fc.Line(apex, fc.P(-hw, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(-hw, 0.0), fc.P(hw, 0.0))]),
        fc.Edge("seam_back", [fc.Line(fc.P(hw, 0.0), apex)]),
    ]
    h = apex_h
    return fc.Piece(
        "godet", edges, seam_allowance=seam_allowance,
        allowances={"hem": 30.0},
        notches=[fc.Notch("hem", 0.5, "centre"),
                 fc.Notch("seam_front", 0.0, "underarm apex")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.2), fc.P(0.0, h * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side godet (cut 2, carries the hem sweep)")


def build_sleeve(armhole_ring):
    """A long straight sleeve (cut 2): cap solved to the armhole, tapering to a cuff."""
    wrist = min(bicep_girth * EASE * 0.62, armhole_ring * 0.7)
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
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Slim stand collar (cut 1)")


def build_placket():
    """The short front placket band (cut 2), carrying the buttonholes/buttons."""
    w = BUTTON_MM * 1.6
    h = placket_length
    edges = [
        fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("outer", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    n_buttons = max(2, int(h / (BUTTON_MM * 3.5)))
    internals = []
    for i in range(n_buttons):
        y = h * (i + 0.5) / n_buttons
        internals.append(fc.Internal(f"button {i + 1}",
                                     [fc.P(w * 0.5, y), fc.P(w * 0.5 + BUTTON_MM * 0.4, y)],
                                     kind="marking"))
    return fc.Piece(
        "placket", edges, seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("inner", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front placket (cut 2, buttons)")


MEASURED = {}


def build():
    pattern = fc.PatternSet("jalabiya")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = (2.0 * front.edge("neckline").length()
                            + back.edge("neckline").length())
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()

    if not every:
        picked = {"front": front, "back": back, "godet": build_godet(),
                  "sleeve": build_sleeve(armhole_ring),
                  "collar": build_collar(MEASURED["neck_run"]),
                  "placket": build_placket()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    godet = build_godet()
    sleeve = build_sleeve(armhole_ring)
    collar = build_collar(MEASURED["neck_run"])
    placket = build_placket()
    for piece in (front, back, godet, sleeve, collar, placket):
        pattern.add(piece)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5,
                         ease=(front.edge("shoulder").length()
                               - back.edge("shoulder").length()))
    # The godet's two slant seams equal the body side seams by construction, so they set
    # into the slit side seams without easing.
    pattern.declare_seam(("godet", "seam_front"), ("front", "side_seam"), tol=1.5)
    pattern.declare_seam(("godet", "seam_back"), ("back", "side_seam"), tol=1.5)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    pattern.declare_seam(("collar", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"),
                          ("back", "neckline")], tol=2.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "white cotton poplin (thobe cloth)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body + godets + sleeves + collar + placket at {fabric_width:.0f} mm width, "
                 "60% marker. The body is cut straight and on grain; the sweep is in the "
                 f"godets ({GODET_HEM:.0f} mm hem each), so the robe hangs plumb."},
        {"item": "sew-through buttons (Yantra4D sew-through-button)",
         "qty": max(3, int(placket_length / (BUTTON_MM * 3.5))), "unit": "piece",
         "note": f"placket buttons; button_ligne {button_ligne:.0f} (~{BUTTON_MM:.1f} mm). The "
                 "button is the Yantra4D solid (notion.hardware_ref -> sew-through-button); "
                 "button_ligne drives the printed button AND the placket spacing."},
        {"item": "interfacing (collar + placket)", "qty": 1, "unit": "set",
         "note": "light fusible for the slim stand collar and the short placket."},
        {"item": "cotton thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the straight seams; the godets are set from the underarm apex to "
                 "the hem."},
    ]
    pattern.metadata = {
        "fc400_rank": 392, "family": "heritage_global", "fabric_hint": "cotton-poplin",
        "tradition": "Arabian Gulf — the ankle-length men's robe (thobe / thawb)",
        "silhouette_note": "A straight columnar robe that flares to a wide sweep through SIDE "
            "GODETS (not a shaped side seam), with long set-in sleeves, a short front placket "
            "and a slim stand collar. The godets keep the body on grain so the robe hangs plumb.",
        "hardware": "buttons via Yantra4D (notion.hardware_ref -> sew-through-button); "
            "button_ligne drives BOTH the printed button and the drafted placket spacing.",
        "solver": {
            "chest_cut_mm": round(CHEST_CUT, 1),
            "hem_sweep_mm": round(hem_sweep, 1),
            "added_sweep_mm": round(ADDED_SWEEP, 1),
            "godet_hem_each_mm": round(GODET_HEM, 1),
            "button_ligne": round(button_ligne, 1),
            "note": "the straight body gives a columnar hem; the extra sweep (hem_sweep minus "
                    "the columnar hem) is split over two side godets, so the body stays on "
                    "grain and hangs plumb while the hem still sweeps wide.",
        },
        "cultural_note": "The Gulf thobe is everyday and formal men's dress across the Arabian "
            "Peninsula, with regional collar and cuff variations. This is a plain everyday "
            "thobe; it carries no regional insignia and invents no ornament.",
        "drafting": "Made to measure to chest girth, robe length, sleeve length and hem sweep; "
            "the flare is godets, not a shaped side seam.",
    }
    return pattern


result = build()
