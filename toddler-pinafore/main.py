"""
Toddler pinafore dress — Fashion Cabinet Garment Cartridge (FC-500 #408, kids_baby, T2).

The pinafore (pichi): a sleeveless bib BODICE over a gathered SKIRT, the shoulder STRAPS
crossing at the back and buttoning to the bodice back so the dress grows with the child (two
button rows let the straps drop as she gets taller). A bodice FRONT, a bodice BACK, two
STRAPS and a gathered SKIRT. The strap buttons bridge to the Yantra4D `sew-through-button`.

Solved, not guessed:

  1. THE SKIRT GATHERS TO THE MEASURED BODICE WAIST. The skirt is cut a gather ratio wider
     than the bodice waist edge, and that fullness is declared as the seam's ease against
     the MEASURED bodice waist — so the gather is real, not a guess.
  2. THE STRAP BUTTON ROWS SIT ON CLOTH. Two button positions are stepped in off the bodice
     back's top edge, each by its own button width plus clearance, so a growth adjustment
     never lands a button on the turned edge.
  3. EVERY DERIVED DIMENSION IS CLAMPED. The bib width is held under the chest quarter and
     the strap length floored, so a small-body request never draws a negative-width bib.

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
# bodice_front|bodice_back|strap|skirt|set

chest_girth = float(PARAM(lambda: chest_girth, 560.0))
waist_girth = float(PARAM(lambda: waist_girth, 540.0))
bib_height = float(PARAM(lambda: bib_height, 150.0))       # bodice front height
skirt_length = float(PARAM(lambda: skirt_length, 320.0))
bib_width = float(PARAM(lambda: bib_width, 170.0))         # bib top width
strap_length = float(PARAM(lambda: strap_length, 260.0))
strap_width = float(PARAM(lambda: strap_width, 34.0))
gather_ratio = float(PARAM(lambda: gather_ratio, 1.8))     # skirt fullness
button_ligne = float(PARAM(lambda: button_ligne, 24.0))    # drives sew-through-button (ligne)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

chest_girth = max(420.0, min(chest_girth, 720.0))
waist_girth = max(400.0, min(waist_girth, 700.0))
bib_height = max(90.0, min(bib_height, 240.0))
skirt_length = max(180.0, min(skirt_length, 520.0))
bib_width = max(100.0, min(bib_width, 260.0))
strap_length = max(150.0, min(strap_length, 380.0))
strap_width = max(20.0, min(strap_width, 60.0))
gather_ratio = max(1.2, min(gather_ratio, 2.6))
button_ligne = max(16.0, min(button_ligne, 34.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

Q_WAIST = max(60.0, waist_girth / 4.0)
# The bib top width is clamped under the chest quarter so it never draws wider than the
# body it covers (a bib wider than the chest gapes and flips the piece).
HALF_BIB = min(bib_width / 2.0, chest_girth / 4.0 - 6.0)
HALF_BIB = max(30.0, HALF_BIB)
BUTTON_MM = button_ligne * 0.635    # ligne -> mm


def build_bodice_front():
    """The bib front, cut 1. A trapezoid: waist wide (the bodice quarter x2), narrowing to
    the bib top, with the armhole scoops at the top corners."""
    y_waist = 0.0
    y_top = bib_height
    half_waist = Q_WAIST
    p_waist_l = fc.P(-half_waist, y_waist)
    p_waist_r = fc.P(half_waist, y_waist)
    p_top_r = fc.P(HALF_BIB, y_top)
    p_top_l = fc.P(-HALF_BIB, y_top)
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_l, p_waist_r)]),
        fc.Edge("side_r", [fc.curve_through(p_waist_r, p_top_r, bulge=0.10, side=-1.0)]),
        fc.Edge("top", [fc.Line(p_top_r, p_top_l)]),
        fc.Edge("side_l", [fc.curve_through(p_top_l, p_waist_l, bulge=0.10, side=-1.0)]),
    ]
    return fc.Piece(
        "bodice_front", edges,
        seam_allowance=seam_allowance,
        allowances={"top": 12.0},
        notches=[fc.Notch("waist", 0.5, "CF"),
                 fc.Notch("top", 0.25, "strap"),
                 fc.Notch("top", 0.75, "strap")],
        grainline=fc.Grainline(fc.P(0.0, y_waist + 10.0), fc.P(0.0, y_top - 10.0)),
        internals=[fc.Internal("bib topstitch",
                               [fc.P(-HALF_BIB + 8.0, y_top - 8.0),
                                fc.P(HALF_BIB - 8.0, y_top - 8.0)], kind="trace")],
        cut=fc.CutSpec(quantity=1),
        label="Bodice front / bib (cut 1)",
    )


def build_bodice_back():
    """The bib back, cut 1. A lower band that the straps button to, with two growth rows."""
    y_waist = 0.0
    y_top = bib_height * 0.7
    half_waist = Q_WAIST
    p_waist_l = fc.P(-half_waist, y_waist)
    p_waist_r = fc.P(half_waist, y_waist)
    p_top_r = fc.P(HALF_BIB, y_top)
    p_top_l = fc.P(-HALF_BIB, y_top)
    a = max(3.0, BUTTON_MM * 0.5)
    internals = []
    for row, ry in enumerate((y_top - BUTTON_MM - 6.0,
                              y_top - 2.0 * BUTTON_MM - 16.0)):
        ry = max(y_waist + 20.0, ry)
        for sx in (-HALF_BIB * 0.55, HALF_BIB * 0.55):
            internals.append(fc.Internal(f"button r{row}",
                             [fc.P(sx - a, ry), fc.P(sx + a, ry)], kind="drill"))
    edges = [
        fc.Edge("waist", [fc.Line(p_waist_l, p_waist_r)]),
        fc.Edge("side_r", [fc.curve_through(p_waist_r, p_top_r, bulge=0.08, side=-1.0)]),
        fc.Edge("top", [fc.Line(p_top_r, p_top_l)]),
        fc.Edge("side_l", [fc.curve_through(p_top_l, p_waist_l, bulge=0.08, side=-1.0)]),
    ]
    return fc.Piece(
        "bodice_back", edges,
        seam_allowance=seam_allowance,
        allowances={"top": 12.0},
        notches=[fc.Notch("waist", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(0.0, y_waist + 10.0), fc.P(0.0, y_top - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Bodice back (cut 1)",
    )


def build_strap():
    """A shoulder strap, cut 2. A rectangle the strap length + a buttonhole end."""
    ln = strap_length
    w = strap_width
    a = max(3.0, BUTTON_MM * 0.5)
    return fc.Piece(
        "strap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "front join")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("buttonhole",
                               [fc.P(ln - BUTTON_MM - a, w * 0.5 - a),
                                fc.P(ln - BUTTON_MM - a, w * 0.5 + a)], kind="cut")],
        cut=fc.CutSpec(quantity=2),
        label="Shoulder strap (cut 2)",
    )


_BF = build_bodice_front()
_BB = build_bodice_back()
BODICE_WAIST = _BF.edge("waist").length(0.05) + _BB.edge("waist").length(0.05)
SKIRT_TOP = BODICE_WAIST * gather_ratio


def build_skirt():
    """A gathered skirt, cut 1 (or 2 pieced). Its top edge is the bodice waist times the
    gather ratio; it gathers down to the MEASURED bodice waist."""
    ln = SKIRT_TOP
    h = skirt_length
    return fc.Piece(
        "skirt", [
            fc.Edge("waist", [fc.Line(fc.P(0.0, h), fc.P(ln, h))]),
            fc.Edge("side_r", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 34.0},
        notches=[fc.Notch("waist", 0.5, "CF gather centre"),
                 fc.Notch("waist", 0.25, "gather quarter"),
                 fc.Notch("waist", 0.75, "gather quarter")],
        grainline=fc.Grainline(fc.P(ln * 0.5, 10.0), fc.P(ln * 0.5, h - 10.0)),
        internals=[fc.Internal("gather line",
                               [fc.P(0.0, h - 8.0), fc.P(ln, h - 8.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Gathered skirt (cut 1)",
    )


def build():
    pattern = fc.PatternSet("toddler-pinafore")
    everything = target_piece == "set"
    want = {
        "bodice_front": everything or target_piece == "bodice_front",
        "bodice_back": everything or target_piece == "bodice_back",
        "strap": everything or target_piece == "strap",
        "skirt": everything or target_piece == "skirt",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bodice_front"]:
        pattern.add(build_bodice_front())
    if want["bodice_back"]:
        pattern.add(build_bodice_back())
    if want["strap"]:
        pattern.add(build_strap())
    if want["skirt"]:
        pattern.add(build_skirt())

    if want["skirt"] and want["bodice_front"] and want["bodice_back"]:
        # the skirt top gathers to the measured bodice waist; declare the fullness as ease
        # (side_a = skirt.waist, side_b = the two bodice waists).
        pattern.declare_seam(("skirt", "waist"),
                             [("bodice_front", "waist"), ("bodice_back", "waist")],
                             tol=1.0, ease=SKIRT_TOP - BODICE_WAIST)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cotton poplin / needlecord", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker; a firm cotton holds the "
                 f"gather and washes hard."},
        {"item": "sew-through buttons (strap growth rows)", "qty": 4, "unit": "count",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at {button_ligne:.0f} "
                 f"ligne; two rows so the straps drop as the child grows."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "gather the skirt to the bodice waist; the straps cross at the back and "
                 "button to the growth rows."},
    ]
    pattern.metadata = {
        "fc500_rank": 408, "family": "kids_baby", "tier": 2,
        "fabric_hint": "popelina-algodon",
        "silhouette_note": "A cross-back pinafore over a gathered skirt, the straps "
            "buttoning to two growth rows so the dress lasts a season longer.",
        "solved": {
            "bodice_waist_measured_mm": round(BODICE_WAIST, 1),
            "skirt_top_mm": round(SKIRT_TOP, 1),
            "gather_ratio": round(gather_ratio, 2),
            "half_bib_requested_mm": round(bib_width / 2.0, 1),
            "half_bib_clamped_mm": round(HALF_BIB, 1),
            "bib_was_clamped": bool(abs(HALF_BIB - bib_width / 2.0) > 0.01),
            "note": "the skirt gathers to the MEASURED bodice waist (the fullness declared "
                    "as the seam ease); the bib top is clamped under the chest quarter so a "
                    "small body never draws a bib wider than the chest; the button growth "
                    "rows are stepped in off the top edge so they seat on cloth.",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the thickness, dish and card count are fed from "
                    "button_ligne (the sew-face params are left unmapped — the button sits "
                    "on the cloth face, no seam handshake owed).",
    }
    return pattern


result = build()
