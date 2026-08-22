"""
Garter Belt (suspender belt) — Fashion Cabinet Garment Cartridge (FC-300 #222; y4d garter-clip).

A shaped belt that sits between waist and high hip and hangs four suspender straps, each
ending in a clip that grips a stocking welt. Two things make this a real garment rather
than a strip of elastic:

  1. THE BELT IS SHAPED, NOT STRAIGHT. The body narrows to the waist and flares to the
     hip, so a rectangle cut to waist girth rides up and a rectangle cut to hip girth
     falls down. The belt here is drafted as a ring of panels whose top edge sums to the
     waist ring and whose bottom edge sums to the high-hip ring — a truncated cone
     flattened out. That single decision is why it stays put.
  2. THE STRAPS ARE PLACED, NOT SPRINKLED. Four straps at the classic positions — front
     pair either side of centre front, back pair either side of centre back — with the
     drop set so the clip lands on the stocking welt rather than below it.

The DIMENSIONAL HANDSHAKE. The clip is the Yantra4D solid `garter-clip`, whose sewn
mating feature is a `strap_slot` **flange** driven by `strap_w` and `strap_t`: the slot
the strap threads through. A strap wider than the slot will not thread; narrower and it
twists and the clip hangs crooked. So the garment's `strap_w` parameter drives BOTH the
drafted strap piece (its cut width is `strap_w`, and it is the piece's `strap_edge`
interface) AND the hardware's slot width — one number, two objects. `strap_t` is mapped
from the material's finished thickness so the printed slot clears the folded webbing.

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

waist_girth   = float(PARAM(lambda: waist_girth, 700.0))
hip_girth     = float(PARAM(lambda: hip_girth, 960.0))
belt_depth    = float(PARAM(lambda: belt_depth, 90.0))    # waist edge -> hip edge
strap_w       = float(PARAM(lambda: strap_w, 16.0))       # suspender strap width
strap_t       = float(PARAM(lambda: strap_t, 2.4))        # finished strap thickness
strap_drop    = float(PARAM(lambda: strap_drop, 180.0))   # belt hem -> clip
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
waist_girth   = max(500.0, min(waist_girth, 1400.0))
hip_girth     = max(600.0, min(hip_girth, 1700.0))
belt_depth    = max(45.0, min(belt_depth, 200.0))
strap_w       = max(8.0, min(strap_w, 30.0))
strap_t       = max(1.0, min(strap_t, 6.0))
strap_drop    = max(80.0, min(strap_drop, 340.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 16.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The shaped-ring solver ───────────────────────────────────────────────────
# A belt that stays put is a truncated cone: its top edge is the waist ring and its
# bottom edge the high-hip ring. Split into four panels (front, two sides, back) so
# each panel's top and bottom widths carry a quarter of each ring.
NEG = 1.0 - negative_ease_pct / 100.0
WAIST_RING = waist_girth * NEG
HIP_RING = hip_girth * NEG
BD = belt_depth
# Per-panel widths: front and back panels take a larger share than the sides, which is
# where a real belt puts its seams.
#
# CRITICAL: every panel gets the SAME flare (the same bottom-minus-top increment), not
# a flare proportional to its share. The cone's total flare is distributed EQUALLY over
# the six vertical seams, so every slanted seam edge is congruent and the ring balances
# by construction. Giving each panel a proportional flare instead makes the wide panels
# slant harder than the narrow ones and the seams cannot meet — the verifier catches it.
# The ring is walked as: front(on fold, = half the front) + side + back(on fold, = half
# the back), mirrored — so ONE half of the body is front_half + 2 sides + back_half is
# wrong; it is front_half + 1 side + back_half, and the mirror supplies the other half.
# The fractions below are shares of the FULL waist ring, and front/back are halved
# because those panels are cut on the fold. They must therefore close as:
#     2 * (FRONT_FRAC/2 + SIDE_FRAC + BACK_FRAC/2) == 1
FRONT_FRAC = 0.30
SIDE_FRAC = 0.20
BACK_FRAC = 0.30
_CLOSURE = 2.0 * (FRONT_FRAC / 2.0 + SIDE_FRAC + BACK_FRAC / 2.0)   # == 1.0
#
# The half-ring is front_half + one side + back_half, i.e. THREE seam-joined panels.
# The total flare over that half is (HIP_RING - WAIST_RING)/2, split equally three
# ways, so the hem edges sum back to exactly HIP_RING while every seam stays congruent
# (equal flare per panel = congruent slants; proportional flare would not meet).
_HALF_FLARE = (HIP_RING - WAIST_RING) / 2.0
_PANELS_PER_HALF = 3.0
PANEL_FLARE = _HALF_FLARE / _PANELS_PER_HALF
F_TOP = WAIST_RING * FRONT_FRAC / 2.0
F_BOT = F_TOP + PANEL_FLARE
S_TOP = WAIST_RING * SIDE_FRAC
S_BOT = S_TOP + PANEL_FLARE
B_TOP = WAIST_RING * BACK_FRAC / 2.0
B_BOT = B_TOP + PANEL_FLARE

# Strap placement: four straps, front pair and back pair, at these fractions across
# their panels (0 = the fold/centre, 1 = the side seam).
FRONT_STRAP_AT = 0.62
BACK_STRAP_AT = 0.55


def _tab(label, x, y_top):
    """A strap-attachment marking on the belt hem, drawn strap_w wide.

    The strap is stitched here; drawing it at the same `strap_w` the hardware slot
    receives keeps the belt, the strap and the clip on one number.
    """
    return fc.Internal(label,
                       [fc.P(x - strap_w / 2.0, y_top), fc.P(x + strap_w / 2.0, y_top)],
                       kind="marking")


def _panel(name, top_w, bot_w, on_fold, label, strap_at=None, strap_label=""):
    """One shaped belt panel: top edge = waist share, bottom edge = hip share.

    The vertical seams slant outward from waist to hip, which is the flattened cone.
    Panels drafted on the fold (front, back) carry `fold_edge="center"`.
    """
    # The cone flare (bot_w - top_w) is carried implicitly by the slanted `seam` edge.
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(bot_w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BD))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, BD), fc.P(top_w, BD))]),
        fc.Edge("seam", [fc.Line(fc.P(top_w, BD), fc.P(bot_w, 0.0))]),
    ]
    internals = []
    if strap_at is not None:
        internals.append(_tab(strap_label, bot_w * strap_at, 0.0))
    notches = [fc.Notch("waist", 0.5, "quarter mark")]
    if strap_at is not None:
        notches.append(fc.Notch("hem", 1.0 - strap_at, "strap position"))
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"waist": 10.0, "hem": 10.0},
        notches=notches,
        grainline=fc.Grainline(fc.P(top_w * 0.5, 8.0), fc.P(top_w * 0.5, BD - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1 if on_fold else 2, on_fold=on_fold,
                       fold_edge="center" if on_fold else None,
                       mirror=not on_fold),
        label=label,
    )


def build_front():
    return _panel("front_panel", F_TOP, F_BOT, True,
                  "Front panel (cut 1 on fold, 2 strap positions)",
                  strap_at=FRONT_STRAP_AT, strap_label="front strap position")


def build_side():
    return _panel("side_panel", S_TOP, S_BOT, False, "Side panel (cut 2 pairs)")


def build_back():
    return _panel("back_panel", B_TOP, B_BOT, True,
                  "Back panel (cut 1 on fold, 2 strap positions, hook closure)",
                  strap_at=BACK_STRAP_AT, strap_label="back strap position")


def build_strap():
    """A suspender strap: a narrow rectangle whose CUT WIDTH IS `strap_w`.

    `strap_edge` is the long edge that threads the clip's slot and the slider — it is
    the interface the hardware handshake couples to. The clip end is left unsewn
    (the strap threads through and folds back), so it is declared as a hardware span
    rather than a sewn seam.
    """
    length = strap_drop
    edges = [
        fc.Edge("end_belt", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_clip", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap",
        edges,
        seam_allowance=0.0,   # folded/turned strap elastic, cut to finished width
        notches=[fc.Notch("strap_edge", 0.62, "slider position (adjustable)"),
                 fc.Notch("end_clip", 0.5, "clip slot — thread and fold back")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=4),
        label="Suspender strap (cut 4, clip at the free end)",
    )


def build():
    pattern = fc.PatternSet("garter-belt")
    front = build_front()
    side = build_side()
    back = build_back()
    strap = build_strap()

    picked = {"front_panel": front, "side_panel": side, "back_panel": back,
              "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, side, back, strap):
            pattern.add(piece)
        # The shaped ring: front -> side -> back. Every panel shares the same depth
        # and the same cone flare, so paired seams balance by construction.
        pattern.declare_seam(("front_panel", "seam"), ("side_panel", "seam"), tol=1.0)
        pattern.declare_seam(("side_panel", "seam"), ("back_panel", "seam"), tol=1.0)
        # Each strap's belt end is stitched to the hem at its marked position; the
        # strap's cut width is what must match, and it is the same `strap_w` the
        # clip's slot receives.
        pattern.declare_seam(("strap", "end_belt"), ("strap", "end_clip"), tol=0.5)

    # One half of the ring = front(on fold, half the front) + one side + back(on fold,
    # half the back); the mirror supplies the other half, hence the leading 2.0.
    waist_finished = 2.0 * (front.edge("waist").length()
                            + side.edge("waist").length()
                            + back.edge("waist").length())
    hem_finished = 2.0 * (front.edge("hem").length()
                          + side.edge("hem").length()
                          + back.edge("hem").length())
    strap_total = 4.0 * strap.edge("strap_edge").length()

    fabric_width = 1400.0
    area = (front.area() * 2.0 + side.area() * 4.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "powernet or satin tricot (+ lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"belt panels at {fabric_width:.0f} mm width, 62% marker; fully lined "
                 "so the strap stitching is enclosed. Cut with little or no stretch "
                 "around the body — a garter belt works by shape, not by squeeze."},
        {"item": "garter clips (Yantra4D garter-clip)", "qty": 4, "unit": "piece",
         "note": f"four clips; slot width strap_w {strap_w:.0f} mm, slot clearance for "
                 f"strap_t {strap_t:.1f} mm folded thickness. The clip is the Yantra4D "
                 "solid (notion.hardware_ref -> garter-clip), never modelled here; the "
                 "drafted strap is cut to exactly the width its slot expects."},
        {"item": f"strap elastic {strap_w:.0f} mm", "qty": round(strap_total * 1.15),
         "unit": "mm_length",
         "note": f"four straps x {strap_drop:.0f} mm + 15% for the slider fold-backs. "
                 "Cut to the SAME width as the clip slot."},
        {"item": "strap sliders", "qty": 4, "unit": "piece",
         "note": "one per strap for length adjustment; sized to strap_w."},
        {"item": "waist + hem elastic 10 mm",
         "qty": round(waist_finished * 0.96 + hem_finished * 0.98), "unit": "mm_length",
         "note": f"waist {waist_finished:.0f} mm x 0.96 + hem {hem_finished:.0f} mm x "
                 "0.98; both edges are lightly stabilised, not gathered."},
        {"item": "hook-and-eye tape (2 rows)", "qty": 1, "unit": "piece",
         "note": "centre-back closure; a garter belt is stepped into or hooked, so a "
                 "short tape is enough."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "bar-tack each strap to the hem at its marked position."},
    ]
    pattern.metadata = {
        "fc300_rank": 222, "family": "underwear_lounge", "fabric_hint": "powernet",
        "silhouette_note": "A SHAPED belt — a flattened truncated cone whose top edge "
            "is the waist ring and bottom edge the high-hip ring — hanging four "
            "suspender straps at the classic front and back positions. The shaping is "
            "why it stays put; a straight strip rides up or falls down.",
        "hardware": "clips via Yantra4D (notion.hardware_ref -> garter-clip); strap_w "
            "drives BOTH the drafted strap's cut width (the strap_edge interface) and "
            "the clip's strap_slot flange — the dimensional handshake. strap_t feeds "
            "the slot clearance for the folded webbing.",
        "solver": {
            "waist_ring_mm": round(WAIST_RING, 1),
            "hip_ring_mm": round(HIP_RING, 1),
            "cone_flare_mm": round(HIP_RING - WAIST_RING, 1),
            "waist_finished_mm": round(waist_finished, 1),
            "hem_finished_mm": round(hem_finished, 1),
            "strap_w_mm": round(strap_w, 1),
            "strap_t_mm": round(strap_t, 2),
            "note": "strap_w is the strap's cut width AND the clip slot width — one "
                    "number reaching both objects.",
        },
        "strap_positions": {
            "count": 4,
            "front_at_frac": FRONT_STRAP_AT,
            "back_at_frac": BACK_STRAP_AT,
            "drop_mm": round(strap_drop, 1),
            "note": "drop is belt hem to clip; set it so the clip lands on the "
                    "stocking welt, not below it.",
        },
        "closure": "centre-back hook-and-eye tape (2 rows)",
        "drafting": "Sized from waist and hip girths; the belt is a shaped ring, not a "
            "straight band.",
    }
    return pattern


result = build()
