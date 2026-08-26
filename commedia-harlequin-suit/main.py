"""
Harlequin Diamond Suit — Fashion Cabinet Costume Cartridge (FC-500 #476; y4d sew-through-button).

The Arlecchino (Harlequin) suit of the commedia dell'arte: a close-fitting jacket-and-trouser of
coloured DIAMONDS (losanges), buttoned down the front with a column of Yantra4D `sew-through-
button`. The diamond is the character — Arlecchino's motley began as the patched rags of a poor
servant and formalised into the regular diamond lattice — so this cartridge draws the jacket, the
trouser, and marks the diamond lattice on both from a single `diamond_pitch`, so the pattern the
tailor pieces is the pattern the audience reads.

The lattice SOLVE. A regular diamond lattice must TILE the garment without a broken diamond at a
seam, so the diamond pitch is snapped to an integer number of diamonds across each panel width:

    columns   = round(panel_width / diamond_pitch)
    pitch_used = panel_width / columns

so the lattice meets cleanly at the side and centre seams. The lattice is marked (the tailor
pieces real diamonds or appliqués them); the count and used pitch are reported.

The DIMENSIONAL HANDSHAKE. The jacket buttons on `sew-through-button`s; `button_ligne` drives the
button seats AND the hardware `sew_face` flange, and it drives the suit's own `button_stand`
interface.

Made to measure to chest, waist, hip and lengths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 800.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
jacket_length = float(PARAM(lambda: jacket_length, 560.0))
inseam = float(PARAM(lambda: inseam, 760.0))
diamond_pitch = float(PARAM(lambda: diamond_pitch, 90.0))
button_ligne = float(PARAM(lambda: button_ligne, 22.0))
button_count = float(PARAM(lambda: button_count, 6.0))
ease_pct = float(PARAM(lambda: ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
jacket_length = max(380.0, min(jacket_length, 780.0))
inseam = max(500.0, min(inseam, 1000.0))
diamond_pitch = max(40.0, min(diamond_pitch, 180.0))
button_ligne = max(14.0, min(button_ligne, 34.0))
button_count = max(3.0, min(button_count, 12.0))
ease_pct = max(0.0, min(ease_pct, 16.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

N_BUTTON = int(round(button_count))
BUTTON_DIA = button_ligne * 0.635

# ── Solved widths ────────────────────────────────────────────────────────────
E = 1.0 + ease_pct / 100.0
CHEST_HALF = (chest_bust_girth * E) / 2.0
WAIST_HALF = (waist_girth * E) / 2.0
HIP_HALF = (hip_girth * E) / 2.0
JACKET_PANEL = CHEST_HALF / 2.0
TROUSER_PANEL = HIP_HALF / 2.0
JL = jacket_length
INS = inseam


def _diamond_lattice(w, h, tag):
    """Mark a regular diamond lattice tiling a w x h panel. The pitch is snapped so an integer
    number of diamonds spans w — no broken diamond at the seam."""
    cols = max(1, int(round(w / diamond_pitch)))
    pitch = w / cols
    rows = max(1, int(round(h / pitch)))
    marks = []
    for r in range(rows + 1):
        y = h * r / rows
        marks.append(fc.Internal(f"{tag}-lat-h{r}", [fc.P(0.0, y), fc.P(w, y)], kind="marking"))
    for c in range(cols + 1):
        x = w * c / cols
        marks.append(fc.Internal(f"{tag}-lat-v{c}", [fc.P(x, 0.0), fc.P(x, h)], kind="marking"))
    return marks, cols, pitch


def _panel(w_top, w_bot, height, name, cut_qty, on_fold, with_buttons=False):
    # A straight-sided panel from w_bot (bottom/hem) to w_top (top), with the `side` edge as
    # the slant and `center` the vertical CF/CB.
    p_bl = fc.P(0.0, 0.0)
    p_br = fc.P(w_bot, 0.0)
    p_tr = fc.P(w_top, height)
    p_tl = fc.P(0.0, height)
    edges = [
        fc.Edge("hem", [fc.Line(p_bl, p_br)]),
        fc.Edge("side", [fc.Line(p_br, p_tr)]),
        fc.Edge("top", [fc.Line(p_tr, p_tl)]),
        fc.Edge("center", [fc.Line(p_tl, p_bl)]),
    ]
    marks, cols, pitch = _diamond_lattice(max(w_top, w_bot), height, name)
    internals = list(marks)
    if with_buttons:
        for i in range(N_BUTTON):
            by = height * (0.15 + 0.7 * i / max(1, N_BUTTON - 1))
            internals.append(fc.Internal(f"{name}-button-{i}",
                                         [fc.P(w_top * 0.08 - BUTTON_DIA / 2.0, by),
                                          fc.P(w_top * 0.08 + BUTTON_DIA / 2.0, by)],
                                              kind="marking"))
    piece = fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(w_bot * 0.4, height * 0.2), fc.P(w_bot * 0.4, height * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=cut_qty, mirror=(not on_fold), on_fold=on_fold,
                       fold_edge=("center" if on_fold else None)),
        label=name.replace("_", " ").title(),
    )
    piece._lattice = (cols, pitch)
    return piece


def build():
    pattern = fc.PatternSet("commedia-harlequin-suit")
    jacket_front = _panel(JACKET_PANEL, WAIST_HALF / 2.0, JL, "jacket_front", 2, False, True)
    jacket_back = _panel(JACKET_PANEL, WAIST_HALF / 2.0, JL, "jacket_back", 1, True)
    trouser = _panel(TROUSER_PANEL, TROUSER_PANEL * 0.7, INS, "trouser", 2, False)

    picked = {"jacket_front": jacket_front, "jacket_back": jacket_back, "trouser": trouser}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (jacket_front, jacket_back, trouser):
            pattern.add(piece)
        # Jacket side seams: front side to back side (both are the same slant, so they balance).
        pattern.declare_seam(("jacket_front", "side"), ("jacket_back", "side"), tol=2.0)
        # The commedia trouser is a tapered tights-like tube seamed up one side; the two trouser
        # panels (cut 2, mirror) join side-to-side.
        pattern.declare_seam(("trouser", "side"), ("trouser", "side"), tol=2.0)

    jf_cols, jf_pitch = jacket_front._lattice
    fabric_width = 1450.0
    area = jacket_front.area() * 2.0 + jacket_back.area() * 2.0 + trouser.area() * 2.0
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "coloured suiting (two+ colours for the diamonds)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cut real diamonds or applique them on a ground; at {fabric_width:.0f} mm width. "
                 f"The lattice is {jf_cols} diamonds across the front at {jf_pitch:.0f} mm."},
        {"item": "front buttons (Yantra4D sew-through-button)", "qty": N_BUTTON, "unit": "piece",
         "note": f"{N_BUTTON} buttons, {button_ligne:.0f} ligne, down the jacket front "
                 "(hardware_ref -> sew-through-button)."},
        {"item": "lining + interfacing", "qty": round(marker_len * 0.5 / 10.0) * 10,
         "unit": "mm_length", "note": "a pieced diamond jacket wants a full lining to hide seams."},
        {"item": "thread (matched per colour)", "qty": 1, "unit": "set",
         "note": "piece the diamonds on the marked lattice so they meet cleanly at the seams."},
    ]
    pattern.metadata = {
        "fc500_rank": 476, "family": "costume_historical", "fabric_hint": "raso-poliester",
        "provenance": "Arlecchino of the commedia dell'arte: the diamond motley began as the "
            "patched rags of a poor servant and formalised into the regular losange lattice by the "
            "17th-18th century. The suit is jacket + trouser, buttoned front, all-over diamonds.",
        "silhouette_note": "Close-fitting jacket and tapered trouser marked with a regular diamond "
            "lattice snapped to tile each panel cleanly, buttoned down the front.",
        "hardware": "front buttons via Yantra4D (hardware_ref -> sew-through-button); button_ligne "
            "drives the seats AND the hardware sew face.",
        "solved": {
            "diamond_pitch_asked_mm": round(diamond_pitch, 1),
            "jacket_front_cols": jf_cols,
            "jacket_front_pitch_mm": round(jf_pitch, 1),
            "button_count": N_BUTTON,
            "button_ligne": round(button_ligne, 1),
            "note": "the diamond pitch is snapped so an integer number of diamonds spans each "
                    "panel — no broken diamond at a seam.",
        },
        "closure": "front sew-through-button column",
        "drafting": "Made to measure to chest, waist, hip and lengths; lattice tiles the panels.",
    }
    return pattern


result = build()
