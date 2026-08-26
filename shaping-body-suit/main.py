"""
Shaping bodysuit (scoop tank) — Fashion Cabinet Garment Cartridge (FC-400 #383; y4d hook-and-eye).

A scoop-neck tank bodysuit in power-mesh: a front and a back panel that run from the
shoulders to a hook-and-eye gusset at the crotch, so the garment cannot ride up out of a
skirt or trousers. It deepens the FC-300 princess-seamed shaping bodysuit into the everyday
tank-cut version worn as a top — the one whose whole appeal is a clean smooth line under
clothes, held down by the crotch closure.

Two real decisions:

  1. THE BODYSUIT STAYS DOWN BECAUSE OF THE GUSSET, NOT THE FABRIC. The reason a bodysuit
     beats a tucked-in top is the crotch closure: it anchors the hem so the torso stays
     smooth however you move. The closure is the Yantra4D hook-and-eye — a 3-column, 2-row
     plate whose sewn footprint is driven by `columns` and `rows`. The gusset is drafted to
     seat that plate, and the crotch run is solved so the front and back crotch edges meet
     the gusset squarely.

  2. THE COMPRESSION IS LIGHT AND EVEN. This is a bodysuit worn as a top, not shapewear, so
     the negative ease is light and uniform (no zoned squeeze). The finished torso ring is
     printed so it stays a number, and the neckline and armholes are scooped and bound flat
     for a clean edge under a jacket.

Three pieces: front, back, and gusset. The straps are cut in one with the panels (a tank
strap, not a bra strap). Made to measure to bust, waist, hip girths and the shoulder-to-crotch
length; there is no inseam — the leg is an opening finished with elastic.

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

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
shoulder_to_crotch = float(PARAM(lambda: shoulder_to_crotch, 660.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 340.0))
strap_width = float(PARAM(lambda: strap_width, 40.0))
neck_scoop = float(PARAM(lambda: neck_scoop, 90.0))
arm_scoop = float(PARAM(lambda: arm_scoop, 200.0))
gusset_w = float(PARAM(lambda: gusset_w, 80.0))
compression_pct = float(PARAM(lambda: compression_pct, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(680.0, min(bust_girth, 1400.0))
waist_girth = max(520.0, min(waist_girth, 1300.0))
hip_girth = max(680.0, min(hip_girth, 1600.0))
shoulder_to_crotch = max(480.0, min(shoulder_to_crotch, 900.0))
shoulder_width = max(240.0, min(shoulder_width, 520.0))
strap_width = max(20.0, min(strap_width, 90.0))
neck_scoop = max(30.0, min(neck_scoop, 220.0))
arm_scoop = max(100.0, min(arm_scoop, 340.0))
gusset_w = max(40.0, min(gusset_w, 150.0))
compression_pct = max(0.0, min(compression_pct, 18.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# geometry floors so extremes stay watertight
TORSO_H = shoulder_to_crotch
arm_scoop = min(arm_scoop, TORSO_H * 0.5)
neck_scoop = min(neck_scoop, TORSO_H * 0.35)

# ── The even-compression solver ──────────────────────────────────────────────
NEG = 1.0 - compression_pct / 100.0
BUST_FIN = bust_girth * NEG
WAIST_FIN = waist_girth * NEG
HIP_FIN = hip_girth * NEG
# each panel (front, back) carries half the widest ring; sides are straight and congruent.
WIDEST = max(BUST_FIN, HIP_FIN)
PANEL_W = WIDEST / 2.0
# hip line and bust line heights on the panel
HIP_Y = TORSO_H * 0.30
BUST_Y = TORSO_H * 0.72


def _panel(name, neck, is_back, label):
    """Front or back panel, symmetric about centre. Shoulder straps cut in one; the crotch
    is a gusset-width flat at the bottom; the leg openings are the lower corners.

    CCW: left leg opening (up to side) -> left side seam (up) -> left armscye -> left strap
    -> neckline -> right strap -> right armscye -> right side seam (down) -> right leg
    opening (in) -> crotch flat (across).
    """
    w = PANEL_W
    cx = w / 2.0
    top = TORSO_H
    g = gusset_w / 2.0
    sh_in = min(shoulder_width / 2.0, w * 0.42)
    strap_out = sh_in
    strap_inr = max(strap_out - strap_width, w * 0.06)
    crotch_l = fc.P(cx - g, 0.0)
    crotch_r = fc.P(cx + g, 0.0)
    side_bot = fc.P(w, HIP_Y * 0.5)
    side_bot_l = fc.P(0.0, HIP_Y * 0.5)
    edges = [
        fc.Edge("leg_opening_l", [fc.Bezier(crotch_l,
                                            fc.P((cx - g) * 0.5, HIP_Y * 0.10),
                                            fc.P(0.0 + w * 0.04, HIP_Y * 0.32),
                                            side_bot_l)]),
        fc.Edge("side_seam_l", [fc.Line(side_bot_l, fc.P(0.0, top - arm_scoop))]),
        fc.Edge("armscye_l", [fc.Bezier(fc.P(0.0, top - arm_scoop),
                                        fc.P(w * 0.06, top - arm_scoop * 0.4),
                                        fc.P(strap_out * 0.6, top - 8.0),
                                        fc.P(strap_out, top))]),
        fc.Edge("strap_l", [fc.Line(fc.P(strap_out, top), fc.P(strap_inr, top))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(strap_inr, top),
                                       fc.P(cx - w * 0.06, top - neck),
                                       fc.P(cx + w * 0.06, top - neck),
                                       fc.P(w - strap_inr, top))]),
        fc.Edge("strap_r", [fc.Line(fc.P(w - strap_inr, top), fc.P(w - strap_out, top))]),
        fc.Edge("armscye_r", [fc.Bezier(fc.P(w - strap_out, top),
                                        fc.P(w - strap_out * 0.6, top - 8.0),
                                        fc.P(w - w * 0.06, top - arm_scoop * 0.4),
                                        fc.P(w, top - arm_scoop))]),
        fc.Edge("side_seam_r", [fc.Line(fc.P(w, top - arm_scoop), side_bot)]),
        fc.Edge("leg_opening_r", [fc.Bezier(side_bot,
                                            fc.P(w - w * 0.04, HIP_Y * 0.32),
                                            fc.P(cx + g + (w - cx - g) * 0.5, HIP_Y * 0.10),
                                            crotch_r)]),
        fc.Edge("crotch", [fc.Line(crotch_r, crotch_l)]),
    ]
    internals = [fc.Internal("waist line",
                             [fc.P(0.0, HIP_Y + (BUST_Y - HIP_Y) * 0.5),
                              fc.P(w, HIP_Y + (BUST_Y - HIP_Y) * 0.5)], kind="marking")]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0, "armscye_l": 0.0, "armscye_r": 0.0,
                    "leg_opening_l": 0.0, "leg_opening_r": 0.0},
        notches=[fc.Notch("crotch", 0.5, "centre crotch"),
                 fc.Notch("side_seam_r", 0.5, "waist line")],
        grainline=fc.Grainline(fc.P(cx, HIP_Y), fc.P(cx, top - 30.0)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_front():
    return _panel("front", neck_scoop, False, "Front panel (cut 1, straps cut in one)")


def build_back():
    return _panel("back", neck_scoop * 0.55, True, "Back panel (cut 1, higher neckline)")


def build_gusset():
    """The gusset seating the hook-and-eye plate: a rectangle bridging front and back crotch.

    Cut 2 (self + cotton lining). Its two short ends sew to the front and back crotch flats
    (both `gusset_w`); the hook-and-eye plate is seated on the marked footprint so the
    bodysuit opens to be stepped into and hooked shut.
    """
    w, ln = gusset_w, gusset_w * 1.6
    edges = [
        fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("back_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("side_b", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("hook-and-eye plate footprint",
                             [fc.P(w * 0.2, ln * 0.5), fc.P(w * 0.8, ln * 0.5)],
                             kind="marking")]
    return fc.Piece(
        "gusset", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("front_end", 0.5, "centre-front match"),
                 fc.Notch("back_end", 0.5, "centre-back match")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.15), fc.P(w * 0.5, ln * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Gusset (cut 2 — self + cotton lining, hook-and-eye seat)")


def build():
    pattern = fc.PatternSet("shaping-body-suit")
    every = target_piece == "set"
    front = build_front()
    back = build_back()

    if not every:
        picked = {"front": front, "back": back, "gusset": build_gusset()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    gusset = build_gusset()
    for piece in (front, back, gusset):
        pattern.add(piece)
    pattern.declare_seam(("front", "side_seam_l"), ("back", "side_seam_l"), tol=1.0)
    pattern.declare_seam(("front", "side_seam_r"), ("back", "side_seam_r"), tol=1.0)
    pattern.declare_seam(("front", "strap_l"), ("back", "strap_l"), tol=1.0)
    pattern.declare_seam(("front", "strap_r"), ("back", "strap_r"), tol=1.0)
    pattern.declare_seam(("gusset", "front_end"), ("front", "crotch"), tol=1.0)
    pattern.declare_seam(("gusset", "back_end"), ("back", "crotch"), tol=1.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    neck_opening = front.edge("neckline").length() + back.edge("neckline").length()
    arm_opening = 2.0 * (front.edge("armscye_r").length() + back.edge("armscye_r").length())
    leg_opening = 2.0 * (front.edge("leg_opening_r").length()
                         + back.edge("leg_opening_r").length())
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "power-mesh (4-way stretch)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front + back + gusset at {fabric_width:.0f} mm width, 60% marker. Light "
                 "even compression — this is a bodysuit worn as a top, not shapewear."},
        {"item": "hook-and-eye gusset plate (Yantra4D hook-and-eye, 3x2)", "qty": 1,
         "unit": "piece",
         "note": "the crotch closure — 3 columns x 2 rows — seated on the gusset's marked "
                 "footprint. The plate is the Yantra4D solid (notion.hardware_ref -> "
                 "hook-and-eye), never modelled here; the gusset is drafted to seat it. This "
                 "is what keeps the bodysuit from riding up."},
        {"item": "cotton gusset lining", "qty": 1, "unit": "piece",
         "note": "the gusset self-piece encloses a cotton lining, the hygienic standard."},
        {"item": "neckline + armscye + leg binding (flat) 8-10 mm",
         "qty": round((neck_opening + arm_opening + leg_opening) * 0.93), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} + armscyes {arm_opening:.0f} + legs "
                 f"{leg_opening:.0f} mm at 0.93; bound flat for a clean edge under clothes."},
        {"item": "polyester thread + ballpoint 70/10 + coverstitch", "qty": 1, "unit": "set",
         "note": "coverstitch the binding so seams stretch and lie flat."},
    ]
    pattern.metadata = {
        "fc400_rank": 383, "family": "underwear_lounge", "fabric_hint": "power-mesh",
        "silhouette_note": "A scoop-neck tank bodysuit: front and back panels from the "
            "shoulders to a hook-and-eye gusset at the crotch, straps cut in one, leg "
            "OPENINGS (no inseam). The crotch closure — not the fabric — is what keeps it "
            "from riding up.",
        "hardware": "hook-and-eye gusset closure via Yantra4D (notion.hardware_ref -> "
            "hook-and-eye, 3 columns x 2 rows); the gusset is drafted to seat the plate so "
            "the bodysuit opens to be stepped into and hooked shut.",
        "solved": {
            "bust_finished_mm": round(BUST_FIN, 1),
            "waist_finished_mm": round(WAIST_FIN, 1),
            "hip_finished_mm": round(HIP_FIN, 1),
            "compression_pct": round(compression_pct, 1),
            "torso_length_mm": round(TORSO_H, 1),
            "neck_opening_mm": round(neck_opening, 1),
            "leg_opening_mm": round(leg_opening, 1),
        },
        "closure": "hook-and-eye gusset (3x2)",
        "drafting": "Made to measure to bust, waist and hip girths + shoulder-to-crotch "
            "length; the compression is light and even and the finished rings are printed.",
    }
    return pattern


result = build()
