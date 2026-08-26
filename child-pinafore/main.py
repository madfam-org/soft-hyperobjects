"""
Children's Pinafore Dress — Fashion Cabinet Garment Cartridge
(FC-400 #324, kids_baby, T2).

A pinafore dress for a child: a bib bodice and a gathered skirt joined at a raised
waist, with two shoulder straps that cross at the back and BUTTON to the bib
front, so the straps let out as the child grows. Drafted from CHILD measurements
(bodies/child-6y), not a shrunk adult — the waist sits high (a child has a short
torso and no defined waist), and the skirt is full for movement.

Two things are solved by measurement rather than by formula:

  1. THE SKIRT GATHER IS SOLVED AGAINST THE BODICE WAIST. The skirt is cut wider
     than the waist and GATHERED to it, so the flat skirt-top width is the bodice
     waist times a MEASURED gather ratio — and the ratio is clamped so the skirt
     is never cut narrower than the waist (which would stretch, not gather) nor so
     wide it will not gather into the seam. The finished waist seam closes at the
     bodice waist by construction.

  2. THE STRAPS ARE CUT TO A MEASURED PATH WITH BUTTON ADJUSTMENT. The strap runs
     from the back waist, over the shoulder, to the bib front where it buttons.
     That path is DERIVED from the measured back rise and bib height plus a
     shoulder arc, and a run of buttonholes gives the growth adjustment — a strap
     cut to a guessed length runs out of adjustment in a term.

The SEW-THROUGH BUTTON SOLID is Yantra4D territory (`sew-through-button`; see
notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
# bib|skirt|strap|set

chest_girth = float(PARAM(lambda: chest_girth, 600.0))     # child chest
waist_high = float(PARAM(lambda: waist_high, 580.0))       # raised waist girth
back_rise = float(PARAM(lambda: back_rise, 200.0))         # waist to back neck
bib_height = float(PARAM(lambda: bib_height, 150.0))       # waist to bib top
bib_width = float(PARAM(lambda: bib_width, 210.0))         # bib top width
skirt_length = float(PARAM(lambda: skirt_length, 300.0))
gather_ratio = float(PARAM(lambda: gather_ratio, 1.7))     # skirt : waist
strap_width = float(PARAM(lambda: strap_width, 34.0))
button_ligne = float(PARAM(lambda: button_ligne, 22.0))
wear_ease = float(PARAM(lambda: wear_ease, 80.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

chest_girth = max(500.0, min(chest_girth, 760.0))
waist_high = max(480.0, min(waist_high, 720.0))
back_rise = max(150.0, min(back_rise, 300.0))
bib_height = max(90.0, min(bib_height, 240.0))
bib_width = max(150.0, min(bib_width, 320.0))
skirt_length = max(180.0, min(skirt_length, 520.0))
gather_ratio = max(1.2, min(gather_ratio, 2.6))
strap_width = max(22.0, min(strap_width, 48.0))
button_ligne = max(16.0, min(button_ligne, 28.0))
wear_ease = max(40.0, min(wear_ease, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 16.0))
hem_allowance = max(20.0, min(hem_allowance, 60.0))

TOPSTITCH = 5.0
BUTTON_MM = button_ligne * 0.635

QUARTER_WAIST = (waist_high + wear_ease) / 4.0
# The bib clamped against the waist it sews to.
_BIB_HALF_RAW = bib_width / 2.0
BIB_HALF = max(strap_width + 10.0, min(_BIB_HALF_RAW, QUARTER_WAIST - 8.0))
# The skirt gather: the flat skirt-top half = the waist half times the ratio,
# clamped so it is never narrower than the waist.
_SKIRT_TOP_RAW = QUARTER_WAIST * gather_ratio
SKIRT_TOP_HALF = max(QUARTER_WAIST + 10.0, _SKIRT_TOP_RAW)
SKIRT_HEM_HALF = SKIRT_TOP_HALF * 1.15    # a little flare


def _button(label, x, y):
    r = BUTTON_MM / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a))) for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


def build_bib():
    """The bib bodice front, cut 1 on the CF fold. Straps button to its top."""
    h = bib_height
    edges = [
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        fc.Edge("bib_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(QUARTER_WAIST, 0.0))]),
        fc.Edge("bib_side", [fc.Line(fc.P(QUARTER_WAIST, 0.0), fc.P(BIB_HALF, h))]),
        fc.Edge("bib_top", [fc.Line(fc.P(BIB_HALF, h), fc.P(0.0, h))]),
    ]
    internals = [
        fc.Internal("bib topstitch",
                    [fc.P(0.0, h - TOPSTITCH), fc.P(BIB_HALF - TOPSTITCH, h - TOPSTITCH),
                     fc.P(QUARTER_WAIST - TOPSTITCH, TOPSTITCH)], kind="trace"),
    ]
    # The button-adjustment run at the bib top where the strap buttons on.
    for i in range(3):
        internals.append(_button(f"strap button-{i + 1}", BIB_HALF * 0.6,
                                 h - TOPSTITCH - i * BUTTON_MM * 1.6))
    return fc.Piece(
        "bib", edges,
        seam_allowance=seam_allowance,
        allowances={"bib_top": hem_allowance * 0.4, "cf_fold": 0.0},
        notches=[fc.Notch("bib_bottom", 1.0, "skirt/bib waist match"),
                 fc.Notch("bib_side", 1.0, "strap corner")],
        grainline=fc.Grainline(fc.P(BIB_HALF * 0.5, 12.0), fc.P(BIB_HALF * 0.5, h - 12.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Bib bodice (cut on fold)",
    )


def build_skirt():
    """The skirt, cut 2 (front + back) on the fold. Gathered to the bodice waist."""
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, skirt_length), fc.P(SKIRT_TOP_HALF, skirt_length))]),
        fc.Edge("side", [fc.Line(fc.P(SKIRT_TOP_HALF, skirt_length),
                                 fc.P(SKIRT_HEM_HALF, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(SKIRT_HEM_HALF, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, skirt_length))]),
    ]
    return fc.Piece(
        "skirt", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("waist", 0.0, "CF"),
                 fc.Notch("waist", 1.0, "side seam"),
                 fc.Notch("waist", 0.5, "gather quarter")],
        grainline=fc.Grainline(fc.P(SKIRT_TOP_HALF * 0.4, 20.0),
                               fc.P(SKIRT_TOP_HALF * 0.4, skirt_length - 20.0)),
        internals=[
            fc.Internal("gather line",
                        [fc.P(0.0, skirt_length - TOPSTITCH),
                         fc.P(SKIRT_TOP_HALF, skirt_length - TOPSTITCH)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cf_fold"),
        label="Skirt (cut 2, on fold)",
    )


# The strap path, MEASURED.
SHOULDER_ARC = max(90.0, chest_girth * 0.24)
STRAP_PATH = bib_height + back_rise + SHOULDER_ARC
BUTTON_ADJ = max(50.0, STRAP_PATH * 0.14)
STRAP_CUT = STRAP_PATH + BUTTON_ADJ + 2.0 * seam_allowance


def build_strap():
    """A shoulder strap, cut 2. Buttons to the bib; buttonholes give growth."""
    ln = STRAP_CUT
    w = strap_width * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("button_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("waist_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)], kind="marking"),
    ]
    for i in range(3):
        internals.append(fc.Internal(
            f"buttonhole-{i + 1}",
            [fc.P(ln - seam_allowance - i * BUTTON_ADJ / 2.0, w / 2.0 - BUTTON_MM * 0.6),
             fc.P(ln - seam_allowance - i * BUTTON_ADJ / 2.0, w / 2.0 + BUTTON_MM * 0.6)],
            kind="cut"))
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "back waist end"),
                 fc.Notch("lower", 1.0, "bib button end")],
        grainline=fc.Grainline(fc.P(ln * 0.12, w / 2.0), fc.P(ln * 0.88, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Shoulder strap (cut 2)",
    )


def build():
    pattern = fc.PatternSet("child-pinafore")
    everything = target_piece == "set"
    want = {
        "bib": everything or target_piece == "bib",
        "skirt": everything or target_piece == "skirt",
        "strap": everything or target_piece == "strap",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bib"]:
        pattern.add(build_bib())
    if want["skirt"]:
        pattern.add(build_skirt())
    if want["strap"]:
        pattern.add(build_strap())

    if want["strap"]:
        pattern.declare_seam(("strap", "lower"), ("strap", "upper"), tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton poplin, 130 gsm (childrenswear print)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a crisp poplin "
                 f"holds the gathered skirt full."},
        {"item": "sew-through button", "qty": 6, "unit": "piece",
         "note": f"Yantra4D sew-through-button (notion.hardware_ref) at "
                 f"{button_ligne:.0f} ligne ({BUTTON_MM:.1f} mm): 3 per strap "
                 f"button on the bib, giving the growth adjustment as the child "
                 f"gets taller."},
        {"item": "gather thread + needle 80/12", "qty": 1, "unit": "spool",
         "note": f"gather the skirt top to the bodice waist at a ratio of "
                 f"{gather_ratio:.1f}:1; {TOPSTITCH:.0f} mm edge topstitch."},
    ]
    pattern.metadata = {
        "fc400_rank": 324,
        "family": "kids_baby",
        "tier": 2,
        "fabric_hint": "cotton-poplin",
        "finished_mm": {
            "quarter_waist": round(QUARTER_WAIST, 1),
            "bib_height": round(bib_height, 1),
            "bib_half_width": round(BIB_HALF, 1),
            "skirt_top_half": round(SKIRT_TOP_HALF, 1),
            "skirt_length": round(skirt_length, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
        },
        "solved": {
            "gather_ratio_requested": round(gather_ratio, 2),
            "skirt_top_requested_mm": round(_SKIRT_TOP_RAW, 2),
            "skirt_top_final_mm": round(SKIRT_TOP_HALF, 2),
            "skirt_wider_than_waist": bool(SKIRT_TOP_HALF > QUARTER_WAIST),
            "strap_path_measured_mm": round(STRAP_PATH, 2),
            "button_adjustment_mm": round(BUTTON_ADJ, 2),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(BIB_HALF, 2),
            "bib_half_was_clamped": bool(abs(BIB_HALF - _BIB_HALF_RAW) > 0.01),
            "note": "the skirt is cut wider than the waist and gathered to it, at a "
                    "ratio clamped so the skirt is never narrower than the waist "
                    "(which would stretch, not gather). The straps are cut to a "
                    "MEASURED path (bib + back rise + shoulder arc) with a run of "
                    "buttonholes for growth, and the bib is clamped against the "
                    "waist it sews to (an inverted bib the kernel CCW-normalizes "
                    "into a healthy-looking piece).",
        },
        "child_proportion": {
            "source": "drafted from child measurements directly (bodies/child-6y)",
            "high_waist": "the waist sits high — a child has a short torso and no "
                          "defined waist to draft to",
            "full_skirt": "the skirt is gathered full for movement",
            "growth_buttons": "three strap buttons on the bib let the straps out as "
                              "the child gets taller",
        },
        "hardware": "sew-through buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); the solid's button_ligne is fed from this "
                    "garment's button_ligne, which also sizes the buttonholes and "
                    "the strap-adjustment run.",
    }
    return pattern


result = build()
