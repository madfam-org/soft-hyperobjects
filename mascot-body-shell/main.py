"""
Mascot Body-Shell Suit — Fashion Cabinet Costume Cartridge (FC-500 #478; y4d zipper).

The body shell of a mascot costume: the oversized foam-lined torso the performer climbs into, cut
enormous to clear a foam under-structure and give the exaggerated barrel shape a mascot needs,
with a full-length centre-back Yantra4D `zipper` so it opens right down for getting in and out and
for the ventilation a performer sweating inside a foam suit depends on. It is drafted as a wide
front, a wide back split for the zip, and shoulder/side seams, all cut at a large positive
`foam_ease` over the body plus the foam thickness.

The foam SOLVE. A mascot shell is not cut to the body — it is cut to the BODY PLUS THE FOAM, twice
(the foam wraps the whole circumference), plus a movement ease. Cut to the body it will not close
over the foam; cut to a guessed size it distorts. The circumference is solved:

    shell_circ = (body_girth + 2*pi*foam_thickness) + movement_ease

so the shell clears a foam layer of the stated thickness all the way round, with room to move.

The DIMENSIONAL HANDSHAKE. The centre back opens on a `zipper`; `zip_length` drives the zipper
tape AND the drafted CB opening AND the shell's own `cb_zip` interface, so the tape is exactly as
long as the opening it closes.

Made to measure to chest and length (plus the foam). FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 1000.0))
shell_length = float(PARAM(lambda: shell_length, 720.0))
foam_thickness = float(PARAM(lambda: foam_thickness, 40.0))
movement_ease = float(PARAM(lambda: movement_ease, 200.0))
barrel = float(PARAM(lambda: barrel, 1.3))            # how much the belly bulges vs chest
neck_opening = float(PARAM(lambda: neck_opening, 420.0))
zip_length = float(PARAM(lambda: zip_length, 600.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

chest_bust_girth = max(800.0, min(chest_bust_girth, 1500.0))
shell_length = max(450.0, min(shell_length, 1000.0))
foam_thickness = max(10.0, min(foam_thickness, 120.0))
movement_ease = max(80.0, min(movement_ease, 500.0))
barrel = max(1.0, min(barrel, 1.8))
neck_opening = max(300.0, min(neck_opening, 650.0))
zip_length = max(300.0, min(zip_length, 900.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# zip cannot be longer than the shell
zip_length = min(zip_length, shell_length - 40.0)

# ── The foam solve ───────────────────────────────────────────────────────────
SHELL_CIRC = chest_bust_girth + 2.0 * math.pi * foam_thickness + movement_ease
BELLY_CIRC = SHELL_CIRC * barrel
SHELL_HALF = SHELL_CIRC / 2.0
BELLY_HALF = BELLY_CIRC / 2.0
SL = shell_length
NECK_HALF = neck_opening / 2.0


def _shell_panel(name, is_back):
    """A shell panel: neck (top, NECK_HALF) to belly (mid, bulged) to hem (bottom). Barrel shape.
    The back is split at the CB for the zipper (drawn as an opening notch)."""
    top = NECK_HALF
    mid = BELLY_HALF / 2.0     # per-panel quarter at the belly
    hem = (SHELL_HALF / 2.0)   # per-panel quarter at the hem
    p_cf_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(hem, 0.0)
    p_side_belly = fc.P(mid, SL * 0.45)
    p_underarm = fc.P(SHELL_HALF / 2.0 * 0.9, SL * 0.8)
    p_shoulder = fc.P(top + (SHELL_HALF / 2.0 - top) * 0.4, SL)
    p_neck = fc.P(top, SL)
    p_cf_neck = fc.P(0.0, SL)
    edges = [
        fc.Edge("hem", [fc.Line(p_cf_hem, p_side_hem)]),
        fc.Edge("side", [fc.Bezier(p_side_hem, fc.P(mid + 10.0, SL * 0.25),
                                   fc.P(mid, SL * 0.35), p_side_belly)]),
        fc.Edge("side_upper", [fc.Bezier(p_side_belly, fc.P(mid, SL * 0.6),
                                         fc.P(p_underarm.x + 10.0, SL * 0.72), p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm, fc.P(SHELL_HALF / 2.0 * 0.85, SL * 0.92),
                                      fc.P(p_shoulder.x + 10.0, SL - 10.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(top * 0.5, SL - 4.0),
                                   fc.P(top * 0.2, SL - 2.0), p_cf_neck)]),
        fc.Edge("center", [fc.Line(p_cf_neck, p_cf_hem)]),
    ]
    internals = []
    if is_back:
        internals.append(fc.Internal("cb-zip",
            [fc.P(0.0, SL - 10.0), fc.P(0.0, SL - 10.0 - zip_length)],
                                     kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"armscye": 0.0, "neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("side_upper", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(mid * 0.4, SL * 0.2), fc.P(mid * 0.4, SL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=(1 if not is_back else 2), mirror=is_back,
                       on_fold=(not is_back), fold_edge=("center" if not is_back else None)),
        label=("Shell front (cut 1 on fold)" if not is_back else "Shell back (cut 2, CB zip)"),
    )


def build():
    pattern = fc.PatternSet("mascot-body-shell")
    front = _shell_panel("shell_front", False)
    back = _shell_panel("shell_back", True)

    picked = {"shell_front": front, "shell_back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back):
            pattern.add(piece)
        # Side seams (lower + upper) and shoulder join front to back.
        pattern.declare_seam([("shell_front", "side"), ("shell_front", "side_upper")],
                             [("shell_back", "side"), ("shell_back", "side_upper")], tol=2.5)
        pattern.declare_seam(("shell_front", "shoulder"), ("shell_back", "shoulder"), tol=2.0)

    fabric_width = 1550.0
    area = front.area() * 2.0 + back.area() * 2.0
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "mascot plush / fur fabric", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"the outer shell at {fabric_width:.0f} mm width; pile runs down."},
        {"item": "upholstery foam sheet", "qty": round(SHELL_CIRC * SL / 1000.0), "unit": "cm2",
         "note": f"a {foam_thickness:.0f} mm foam under-structure gives the barrel; the shell "
                 "is cut to clear it all the way round."},
        {"item": "separating zipper (Yantra4D zipper)", "qty": 1, "unit": "piece",
         "note": f"full-length CB separating zip, {zip_length:.0f} mm (hardware_ref -> zipper) — "
                 "opens right down for entry and ventilation."},
        {"item": "cooling vest + mesh vents", "qty": 1, "unit": "set",
         "note": "a mascot performer overheats fast; add underarm mesh vents + cooling vest."},
    ]
    pattern.metadata = {
        "fc500_rank": 478, "family": "costume_historical", "fabric_hint": "foam-forrado",
        "provenance": "The mascot body shell is the descendant of carnival and pageant giants and "
            "the modern sports/brand mascot: an oversized foam-and-plush torso the performer wears "
            "over their own body. Its defining problem is the foam clearance and the ventilation — "
            "both engineered here.",
        "silhouette_note": "An oversized barrel-shaped foam-lined torso shell with a full-length "
            "centre-back separating zip, cut to clear a foam under-structure all the way round.",
        "hardware": "CB zip via Yantra4D (hardware_ref -> zipper); zip_length drives the tape AND "
            "the drafted CB opening.",
        "solved": {
            "shell_circ_mm": round(SHELL_CIRC, 1),
            "belly_circ_mm": round(BELLY_CIRC, 1),
            "foam_thickness_mm": round(foam_thickness, 1),
            "barrel": round(barrel, 2),
            "zip_length_mm": round(zip_length, 1),
            "note": "shell_circ = body + 2*pi*foam_thickness + movement_ease, so the shell clears "
                    "a foam layer of the stated thickness all the way round with room to move.",
        },
        "closure": "full-length centre-back separating zipper",
        "drafting": "Made to measure to chest and length PLUS the foam thickness.",
    }
    return pattern


result = build()
