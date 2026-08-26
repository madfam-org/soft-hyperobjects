"""
Dashiki — Fashion Cabinet Garment Cartridge (FC-400 #393; heritage_global, West African).

The dashiki is the loose pull-over tunic of West Africa — a wide, straight, unfitted garment
worn over the head, cut from a small number of RECTANGULAR panels and defined by the embroidered
placket panel around its V-neck and by its short kimono-style sleeves cut in one with the body.
This cartridge drafts the everyday dashiki around the two facts that make it one, and it draws
the embroidery ground as a real facing rather than inventing a motif:

  1. THE BODY IS RECTANGULAR AND THE SLEEVES ARE CUT IN ONE. A dashiki is not a fitted shirt; it
     is a wide panel folded at the shoulder with the sleeve continued out from the body as one
     piece (a T-shape), the way many wrapper-cloth-economy garments are cut. There is no set-in
     sleeve and no side shaping — the fit is the WIDTH, chosen from a loose ease over the chest,
     and the drop of the T is the sleeve. Drafting it as a fitted tee is the error this cartridge
     avoids; the panel is a true rectangle and the neckline is cut into it.

  2. THE PLACKET PANEL IS THE EMBROIDERY GROUND — DRAWN, NOT INVENTED. The dashiki's defining
     surface is the embroidered panel around the V-neck (and often the cuffs and hem). This
     cartridge draws that panel as a FACING piece — the ground the embroidery sits on — sized to
     the neckline, and it deliberately places NO motif: the embroidery is the maker's or the
     region's, and a commons cartridge supplies the ground, not the design.

Pieces: body (front, cut 1 on fold, with the T-sleeves in one), back (cut 1 on fold), neck
facing (the embroidery ground), pocket (the single kangaroo/breast pocket, optional). Made to
measure to chest girth, body length, sleeve reach, and the neck opening.

Cultural note (stated): the dashiki is a widely worn West African and diaspora garment; this is
an everyday V-neck dashiki, it carries no specific regional or ceremonial embroidery, and the
embroidery ground is left blank for the wearer's own or a regional design.

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
body_length = float(PARAM(lambda: body_length, 800.0))     # shoulder to hem
sleeve_reach = float(PARAM(lambda: sleeve_reach, 300.0))   # shoulder point to sleeve hem
sleeve_depth = float(PARAM(lambda: sleeve_depth, 260.0))   # depth of the T drop
neck_width = float(PARAM(lambda: neck_width, 180.0))       # shoulder-to-shoulder neck span
v_drop = float(PARAM(lambda: v_drop, 200.0))               # depth of the front V
facing_width = float(PARAM(lambda: facing_width, 70.0))    # embroidery ground width
ease_pct = float(PARAM(lambda: ease_pct, 30.0))            # a dashiki is very loose
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1500.0))
body_length = max(500.0, min(body_length, 1300.0))
sleeve_reach = max(120.0, min(sleeve_reach, 520.0))
sleeve_depth = max(150.0, min(sleeve_depth, 420.0))
neck_width = max(120.0, min(neck_width, 280.0))
v_drop = max(80.0, min(v_drop, 340.0))
facing_width = max(30.0, min(facing_width, 140.0))
ease_pct = max(15.0, min(ease_pct, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# the V cannot exceed the body length
v_drop = min(v_drop, body_length - 100.0)
# the neck half-width cannot exceed the body half at the shoulder
EASE = 1.0 + ease_pct / 100.0
CHEST_CUT = chest_girth * EASE
HALF_BODY = CHEST_CUT / 4.0            # half of one panel (front on fold = half body)
neck_half = min(neck_width / 2.0, HALF_BODY * 0.7)


def _tee(name, is_front, label):
    """A T-shaped panel (cut 1 on fold at centre): the body rectangle with the sleeve
    continued out in one. Authored as a half (fold at x=0). CCW from the fold-hem corner:
    center (up the fold) -> neckline -> shoulder/sleeve-top -> sleeve-end -> sleeve-underarm
    -> side seam (down) -> hem (in to the fold).
    """
    bw = HALF_BODY                          # body half width
    h = body_length
    sw = bw + sleeve_reach                  # to the sleeve hem
    sd = sleeve_depth                       # sleeve depth (drop of the T)
    # neck: front has a V; back has a shallow scoop
    if is_front:
        neck_bottom = fc.P(0.0, h - v_drop)
    else:
        neck_bottom = fc.P(0.0, h - v_drop * 0.18)
    neck_shoulder = fc.P(neck_half, h)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_bottom)]),
        fc.Edge("neckline", [fc.Bezier(neck_bottom,
                                       fc.P(neck_half * 0.35, h - v_drop * 0.35),
                                       fc.P(neck_half * 0.75, h - 6.0),
                                       neck_shoulder)]),
        fc.Edge("shoulder_top", [fc.Line(neck_shoulder, fc.P(sw, h))]),
        fc.Edge("sleeve_end", [fc.Line(fc.P(sw, h), fc.P(sw, h - sd))]),
        fc.Edge("underarm", [fc.Line(fc.P(sw, h - sd), fc.P(bw, h - sd))]),
        fc.Edge("side_seam", [fc.Line(fc.P(bw, h - sd), fc.P(bw, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(bw, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "sleeve_end": hem_allowance,
                    "center": 0.0, "neckline": 0.0},
        notches=[fc.Notch("side_seam", 1.0, "underarm point"),
                 fc.Notch("neckline", 0.5, "facing match")],
        grainline=fc.Grainline(fc.P(bw * 0.4, h * 0.15), fc.P(bw * 0.4, h * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label)


def build_front():
    return _tee("front", True, "Front body + sleeves (cut 1 on fold, V-neck)")


def build_back():
    return _tee("back", False, "Back body + sleeves (cut 1 on fold, scoop neck)")


def build_facing(neck_run):
    """The embroidery-ground facing (cut 1): a band following the neckline, `facing_width`
    deep, its LENGTH the measured front+back neckline run. NO motif is placed — this is the
    ground the wearer's or the region's embroidery sits on.
    """
    ln = neck_run
    w = facing_width
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("embroidery ground (no motif — wearer's own)",
                             [fc.P(ln * 0.5, w * 0.5), fc.P(ln * 0.5 + 1.0, w * 0.5)],
                             kind="marking")]
    return fc.Piece(
        "facing", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre front V")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.2), fc.P(ln * 0.1, w * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Neck facing — embroidery ground (cut 1, no motif)")


def build_pocket():
    """The single breast/kangaroo pocket (cut 1): a simple patch, optional."""
    w = HALF_BODY * 0.5
    h = w * 0.9
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "pocket", edges, seam_allowance=seam_allowance,
        allowances={"top": 25.0},
        notches=[fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Breast pocket (cut 1, optional)")


MEASURED = {}


def build():
    pattern = fc.PatternSet("dashiki-tunic")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    MEASURED["neck_run"] = (front.edge("neckline").length() * 2.0
                            + back.edge("neckline").length() * 2.0)

    if not every:
        picked = {"front": front, "back": back,
                  "facing": build_facing(MEASURED["neck_run"]),
                  "pocket": build_pocket()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    facing = build_facing(MEASURED["neck_run"])
    pocket = build_pocket()
    for piece in (front, back, facing, pocket):
        pattern.add(piece)
    # Shoulder/sleeve-top: front to back (each is the same T-top run).
    pattern.declare_seam(("front", "shoulder_top"), ("back", "shoulder_top"), tol=1.5)
    # Underarm + side seam: front to back.
    pattern.declare_seam(("front", "side_seam"), ("back", "side_seam"), tol=1.0)
    pattern.declare_seam(("front", "underarm"), ("back", "underarm"), tol=1.0)
    # The facing follows the whole neckline (both fronts + both backs, mirrored).
    pattern.declare_seam(("facing", "neck_edge"),
                         [("front", "neckline"), ("front", "neckline"),
                          ("back", "neckline"), ("back", "neckline")], tol=2.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    fabric_width = 1150.0            # African wax/print cloth is often ~115 cm
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "African wax print or plain cotton", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body + facing + pocket at {fabric_width:.0f} mm width (print cloth is "
                 "often ~115 cm), 70% marker. The T-cut panels are rectangles used whole — "
                 "very little waste, in the wrapper-cloth economy tradition."},
        {"item": "embroidery thread / trim (wearer's or region's design)", "qty": 1,
         "unit": "set",
         "note": "the neck facing is the embroidery GROUND; this cartridge places NO motif. "
                 "The embroidery is the maker's or the region's own design."},
        {"item": "cotton thread", "qty": 1, "unit": "spool",
         "note": "flat-fell or overlock the few straight seams; the garment is otherwise "
                 "rectangles."},
    ]
    pattern.metadata = {
        "fc400_rank": 393, "family": "heritage_global", "fabric_hint": "cotton-print",
        "tradition": "West African — the loose pull-over tunic worn over the head",
        "silhouette_note": "A wide, straight, unfitted pull-over tunic: rectangular body panels "
            "folded at the shoulder with the short sleeves cut in one (a T-shape), a V-neck "
            "faced with an embroidery-ground panel. The fit is the width, not shaping.",
        "hardware": "none — the dashiki is a pull-over with no fastening.",
        "embroidery": "The neck facing is the embroidery ground. This cartridge deliberately "
            "places NO motif — the embroidery is the wearer's or the region's own, and a "
            "commons cartridge supplies the ground, not the design.",
        "solved": {
            "chest_cut_mm": round(CHEST_CUT, 1),
            "body_half_mm": round(HALF_BODY, 1),
            "neck_run_mm": round(MEASURED.get("neck_run", 0.0), 1),
            "v_drop_mm": round(v_drop, 1),
            "note": "the panel is a true rectangle; the fit is the loose width, and the "
                    "sleeves are continued from the body in one (a T), not set in.",
        },
        "cultural_note": "The dashiki is a widely worn West African and diaspora garment. This "
            "is an everyday V-neck dashiki; it carries no specific regional or ceremonial "
            "embroidery, and the ground is left blank for the wearer's own or a regional design.",
        "drafting": "Made to measure to chest girth, body length and sleeve reach; the body "
            "is a rectangle and the sleeves are cut in one.",
    }
    return pattern


result = build()
