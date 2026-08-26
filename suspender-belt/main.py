"""
Suspender belt (six-strap) — Fashion Cabinet Garment Cartridge (FC-400 #385; y4d garter-clip).

The classic waist-sitting suspender belt (liguero) in satin tricot: a shaped belt that sits
at the natural waist and hangs SIX suspender straps — a front pair, a side pair, and a back
pair — each ending in a clip that grips a stocking welt. It deepens the FC-300 garter-belt
(four straps, sitting lower on the high hip) into the higher, six-strap version that holds a
fully-fashioned stocking dead straight, and it keeps the same dimensional handshake with the
printed `garter-clip`.

Two things make this a real garment rather than a strip of elastic, and both carry over from
the FC-300 draft:

  1. THE BELT IS SHAPED, NOT STRAIGHT. The body narrows to the waist and flares to the hip,
     so a rectangle rides up or falls down. The belt is a flattened truncated cone: its top
     edge sums to the waist ring, its bottom edge to the high-hip ring, and the flare is
     split EQUALLY over the vertical seams so every slanted seam is congruent and the ring
     closes by construction. Sitting at the WAIST (not the high hip) is what lets a six-strap
     belt keep the stocking seam straight down the back of the leg.

  2. SIX STRAPS ARE PLACED, NOT SPRINKLED. A front pair either side of centre front, a side
     pair over each hip, and a back pair either side of centre back. Six points is what holds
     a fully-fashioned stocking without the welt sagging between suspenders, and the drop is
     set so each clip lands on the welt.

THE DIMENSIONAL HANDSHAKE (inherited from #222). The clip is the Yantra4D solid `garter-clip`,
whose sewn mating feature is a `strap_slot` flange driven by `strap_w` and `strap_t`. A strap
wider than the slot will not thread; narrower and it twists. So the garment's `strap_w` drives
BOTH the drafted strap's cut width (its `strap_edge` interface) AND the hardware's slot width
— one number, two objects — and `strap_t` feeds the slot clearance for the folded webbing.

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

waist_girth = float(PARAM(lambda: waist_girth, 700.0))
high_hip_girth = float(PARAM(lambda: high_hip_girth, 900.0))
belt_depth = float(PARAM(lambda: belt_depth, 110.0))     # waist edge -> lower edge
strap_w = float(PARAM(lambda: strap_w, 16.0))            # suspender strap width
strap_t = float(PARAM(lambda: strap_t, 2.4))             # finished strap thickness
strap_drop = float(PARAM(lambda: strap_drop, 200.0))     # belt hem -> clip
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
waist_girth = max(500.0, min(waist_girth, 1400.0))
high_hip_girth = max(600.0, min(high_hip_girth, 1700.0))
belt_depth = max(60.0, min(belt_depth, 220.0))
strap_w = max(8.0, min(strap_w, 30.0))
strap_t = max(1.0, min(strap_t, 6.0))
strap_drop = max(80.0, min(strap_drop, 360.0))
negative_ease_pct = max(0.0, min(negative_ease_pct, 16.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The shaped-ring solver ───────────────────────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
WAIST_RING = waist_girth * NEG
HIP_RING = high_hip_girth * NEG
BD = belt_depth

# Half the ring = front(on fold, half front) + one side + back(on fold, half back), and
# the mirror supplies the other half. Fractions are shares of the FULL waist ring:
#     2 * (FRONT_FRAC/2 + SIDE_FRAC + BACK_FRAC/2) == 1
FRONT_FRAC = 0.30
SIDE_FRAC = 0.20
BACK_FRAC = 0.30
# Equal flare per panel => congruent slants => the ring closes. Three panels per half.
PANEL_FLARE = ((HIP_RING - WAIST_RING) / 2.0) / 3.0
F_TOP = WAIST_RING * FRONT_FRAC / 2.0
F_BOT = F_TOP + PANEL_FLARE
S_TOP = WAIST_RING * SIDE_FRAC
S_BOT = S_TOP + PANEL_FLARE
B_TOP = WAIST_RING * BACK_FRAC / 2.0
B_BOT = B_TOP + PANEL_FLARE

# Six straps: front pair near centre front, side pair over the hips, back pair near CB.
FRONT_STRAP_AT = 0.60
SIDE_STRAP_AT = 0.50
BACK_STRAP_AT = 0.55


def _tab(label, x):
    return fc.Internal(label,
                       [fc.P(x - strap_w / 2.0, 0.0), fc.P(x + strap_w / 2.0, 0.0)],
                       kind="marking")


def _panel(name, top_w, bot_w, on_fold, label, strap_at=None, strap_label=""):
    """One shaped belt panel: top edge = waist share, bottom edge = high-hip share.

    The vertical `seam` edge slants outward from waist to hip — the flattened cone. Panels
    drafted on the fold (front, back) carry `fold_edge="center"`.
    """
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(bot_w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BD))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, BD), fc.P(top_w, BD))]),
        fc.Edge("seam", [fc.Line(fc.P(top_w, BD), fc.P(bot_w, 0.0))]),
    ]
    internals = []
    notches = [fc.Notch("waist", 0.5, "quarter mark")]
    if strap_at is not None:
        internals.append(_tab(strap_label, bot_w * strap_at))
        notches.append(fc.Notch("hem", 1.0 - strap_at, "strap position"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"waist": 10.0, "hem": 10.0},
        notches=notches,
        grainline=fc.Grainline(fc.P(top_w * 0.5, 8.0), fc.P(top_w * 0.5, BD - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1 if on_fold else 2, on_fold=on_fold,
                       fold_edge="center" if on_fold else None, mirror=not on_fold),
        label=label)


def build_front():
    return _panel("front_panel", F_TOP, F_BOT, True,
                  "Front panel (cut 1 on fold, front strap pair)",
                  strap_at=FRONT_STRAP_AT, strap_label="front strap position")


def build_side():
    return _panel("side_panel", S_TOP, S_BOT, False,
                  "Side panel (cut 2 pairs, side strap pair)",
                  strap_at=SIDE_STRAP_AT, strap_label="side strap position")


def build_back():
    return _panel("back_panel", B_TOP, B_BOT, True,
                  "Back panel (cut 1 on fold, back strap pair, hook closure)",
                  strap_at=BACK_STRAP_AT, strap_label="back strap position")


def build_strap():
    """A suspender strap: a narrow rectangle whose CUT WIDTH IS `strap_w`.

    `strap_edge` is the long edge that threads the clip's slot and the slider — the
    interface the hardware handshake couples to. The clip end threads through and folds
    back, so it is a hardware span rather than a sewn seam.
    """
    length = strap_drop
    edges = [
        fc.Edge("end_belt", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(length, strap_w))]),
        fc.Edge("end_clip", [fc.Line(fc.P(length, strap_w), fc.P(length, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(length, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges, seam_allowance=0.0,
        notches=[fc.Notch("strap_edge", 0.62, "slider position (adjustable)"),
                 fc.Notch("end_clip", 0.5, "clip slot — thread and fold back")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_w / 2.0),
                               fc.P(length * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=6),
        label="Suspender strap (cut 6, clip at the free end)")


def build():
    pattern = fc.PatternSet("suspender-belt")
    front = build_front()
    side = build_side()
    back = build_back()
    strap = build_strap()

    picked = {"front_panel": front, "side_panel": side, "back_panel": back, "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, side, back, strap):
            pattern.add(piece)
        pattern.declare_seam(("front_panel", "seam"), ("side_panel", "seam"), tol=1.0)
        pattern.declare_seam(("side_panel", "seam"), ("back_panel", "seam"), tol=1.0)
        pattern.declare_seam(("strap", "end_belt"), ("strap", "end_clip"), tol=0.5)

    waist_finished = 2.0 * (front.edge("waist").length()
                            + side.edge("waist").length()
                            + back.edge("waist").length())
    hem_finished = 2.0 * (front.edge("hem").length()
                          + side.edge("hem").length()
                          + back.edge("hem").length())
    strap_total = 6.0 * strap.edge("strap_edge").length()

    fabric_width = 1400.0
    area = (front.area() * 2.0 + side.area() * 4.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "satin tricot (+ lining)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"belt panels at {fabric_width:.0f} mm width, 62% marker; fully lined so "
                 "the strap stitching is enclosed. Cut with little stretch around the body — "
                 "a suspender belt works by shape, not by squeeze."},
        {"item": "garter clips (Yantra4D garter-clip)", "qty": 6, "unit": "piece",
         "note": f"six clips; slot width strap_w {strap_w:.0f} mm, slot clearance for "
                 f"strap_t {strap_t:.1f} mm folded thickness. The clip is the Yantra4D solid "
                 "(notion.hardware_ref -> garter-clip), never modelled here; the drafted "
                 "strap is cut to exactly the width its slot expects."},
        {"item": f"strap elastic {strap_w:.0f} mm", "qty": round(strap_total * 1.15),
         "unit": "mm_length",
         "note": f"six straps x {strap_drop:.0f} mm + 15% for the slider fold-backs. Cut to "
                 "the SAME width as the clip slot."},
        {"item": "strap sliders", "qty": 6, "unit": "piece",
         "note": "one per strap for length adjustment; sized to strap_w."},
        {"item": "waist + hem elastic 10 mm",
         "qty": round(waist_finished * 0.96 + hem_finished * 0.98), "unit": "mm_length",
         "note": f"waist {waist_finished:.0f} mm x 0.96 + hem {hem_finished:.0f} mm x 0.98; "
                 "both edges are lightly stabilised, not gathered."},
        {"item": "hook-and-bar tape (2-3 rows)", "qty": 1, "unit": "piece",
         "note": "centre-back closure; a waist-level suspender belt is hooked at the back."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "bar-tack each strap to the hem at its marked position."},
    ]
    pattern.metadata = {
        "fc400_rank": 385, "family": "underwear_lounge", "fabric_hint": "satin-tricot",
        "silhouette_note": "A SHAPED belt sitting at the WAIST — a flattened truncated cone, "
            "waist ring at the top and high-hip ring at the bottom — hanging SIX suspender "
            "straps (front, side and back pairs). Six points and a waist seat keep a "
            "fully-fashioned stocking straight, which four lower straps cannot.",
        "hardware": "clips via Yantra4D (notion.hardware_ref -> garter-clip); strap_w drives "
            "BOTH the drafted strap's cut width (the strap_edge interface) and the clip's "
            "strap_slot flange — the dimensional handshake, inherited from #222. strap_t "
            "feeds the slot clearance for the folded webbing.",
        "solver": {
            "waist_ring_mm": round(WAIST_RING, 1),
            "hip_ring_mm": round(HIP_RING, 1),
            "cone_flare_mm": round(HIP_RING - WAIST_RING, 1),
            "waist_finished_mm": round(waist_finished, 1),
            "hem_finished_mm": round(hem_finished, 1),
            "strap_w_mm": round(strap_w, 1),
            "strap_t_mm": round(strap_t, 2),
            "note": "strap_w is the strap's cut width AND the clip slot width — one number "
                    "reaching both objects.",
        },
        "strap_positions": {
            "count": 6,
            "front_at_frac": FRONT_STRAP_AT,
            "side_at_frac": SIDE_STRAP_AT,
            "back_at_frac": BACK_STRAP_AT,
            "drop_mm": round(strap_drop, 1),
            "note": "drop is belt hem to clip; set it so each clip lands on the stocking welt.",
        },
        "closure": "centre-back hook-and-bar tape",
        "drafting": "Sized from waist and high-hip girths; the belt is a shaped ring sitting "
            "at the waist, not a straight band on the hip.",
    }
    return pattern


result = build()
