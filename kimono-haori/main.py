"""
Haori (羽織) — women's lined — Fashion Cabinet Cartridge (FC-400 #399; heritage_global, Japanese).

The haori is the hip- or thigh-length jacket worn OPEN over a kimono, closed only by a short
braided cord (羽織紐, haori-himo) tied between two chest loops (乳, chi). The FC-300 `haori` drafts
the everyday open haori and, correctly, treats the lining as bought-by-the-bolt rather than a
drafted piece. THIS haori is the women's lined (袷, awase) haori, and it deepens the FC-300 draft
in exactly the direction it left open: it DRAFTS THE LINING as a real co-drafted piece — because
in a women's haori the lining (羽裏, hauro) is the expressive surface, and its panels must be cut
to the shell's own measured runs so the jacket hangs flat and reversible-clean.

Everything the FC-300 haori encodes still holds and is inherited:

  - THE BOLT IS THE UNIT. Kimono-family garments are cut from a 反物 (tanmono) bolt ~375 mm wide,
    and the pieces are RECTANGLES of the bolt used whole. The body is a bolt width; the okumi is a
    half. The front OVERLAP is SOLVED from the bolt width and the target chest, not cut to a girth.
  - THE 前衿 (maeeri) IS FOLDED BACK. The collar runs at DOUBLE its finished width plus
    turn-of-cloth, and its LENGTH is the measured run of both back-neck curves and both fronts.

What this women's lined haori ADDS, and why it earns its own rank:

  1. THE LINING IS DRAFTED, NOT BOUGHT-BY-THE-BOLT. The 羽裏 lining body and sleeve linings are cut
     to the shell's measured body and sleeve runs (a few mm smaller so the lining does not peek),
     so they are declared seams against the shell — the lining is a real member of the pattern.
  2. THE FRONT CORNERS ARE ROUNDED (丸, maru). The women's haori often finishes the lower front
     corner with a soft curve rather than the square men's corner; this is drawn as a solved arc
     at the front hem.

Pieces: body, okumi, sleeve, collar, chi, body_lining, sleeve_lining. Made to measure to bolt
width, chest girth, haori length, sleeve depth and reach.

Cultural note (stated): the haori is Japanese; the 紋付 (montsuki) crested formal haori is NOT
drafted (a 家紋/kamon is a family's mark, not a decoration, and this cartridge places none), and
the surface dyeing traditions (友禅 yūzen, 絞り shibori) belong to their own crafts.

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

bolt_width = float(PARAM(lambda: bolt_width, 375.0))
chest_girth = float(PARAM(lambda: chest_girth, 940.0))
haori_length = float(PARAM(lambda: haori_length, 830.0))
sleeve_depth = float(PARAM(lambda: sleeve_depth, 500.0))
sleeve_reach = float(PARAM(lambda: sleeve_reach, 340.0))
furi_open = float(PARAM(lambda: furi_open, 220.0))         # longer furi on a women's haori
collar_finished = float(PARAM(lambda: collar_finished, 55.0))
neck_drop = float(PARAM(lambda: neck_drop, 95.0))
chi_drop = float(PARAM(lambda: chi_drop, 300.0))
maru_radius = float(PARAM(lambda: maru_radius, 40.0))      # rounded front-corner radius
lining_reduction = float(PARAM(lambda: lining_reduction, 4.0))  # lining cut smaller (mm)
turn_of_cloth = float(PARAM(lambda: turn_of_cloth, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bolt_width = max(300.0, min(bolt_width, 700.0))
chest_girth = max(700.0, min(chest_girth, 1500.0))
haori_length = max(500.0, min(haori_length, 1200.0))
sleeve_depth = max(280.0, min(sleeve_depth, 800.0))
sleeve_reach = max(200.0, min(sleeve_reach, 520.0))
furi_open = max(0.0, min(furi_open, 400.0))
collar_finished = max(25.0, min(collar_finished, 110.0))
neck_drop = max(40.0, min(neck_drop, 180.0))
chi_drop = max(150.0, min(chi_drop, 520.0))
maru_radius = max(0.0, min(maru_radius, 120.0))
lining_reduction = max(0.0, min(lining_reduction, 15.0))
turn_of_cloth = max(0.0, min(turn_of_cloth, 20.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(10.0, min(hem_allowance, 80.0))

if furi_open > sleeve_depth - 120.0:
    furi_open = max(0.0, sleeve_depth - 120.0)
maru_radius = min(maru_radius, bolt_width * 0.4)

# ── The tanmono solve (inherited) ────────────────────────────────────────────
BODY_CIRCUIT = bolt_width * 2.0 + bolt_width
OVERLAP = BODY_CIRCUIT - chest_girth
BOLT_SUFFICIENT = OVERLAP > 0.0
if not BOLT_SUFFICIENT:
    OVERLAP = 0.0
OKUMI_W = bolt_width / 2.0
HALF_BODY = bolt_width / 2.0
SLEEVE_ATTACH = sleeve_depth - furi_open
COLLAR_CUT_W = collar_finished * 2.0 + turn_of_cloth

MEASURED = {}


def build_body():
    """One body half (cut 2, fold at the shoulder). The lower FRONT corner is rounded (maru)
    with a solved arc of radius `maru_radius`; the back-neck scoop is the only other curve.
    """
    w, h = HALF_BODY, haori_length
    attach = SLEEVE_ATTACH
    r = maru_radius
    # hem runs from the side (w,0) toward centre; the front corner (at x=0) is rounded up by r.
    edges = [
        fc.Edge("center_back", [fc.Line(fc.P(0.0, r), fc.P(0.0, h))]),
        fc.Edge("back_neck", [fc.curve_through(fc.P(0.0, h), fc.P(w * 0.42, h),
                                               bulge=0.20, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.42, h), fc.P(w, h))]),
        fc.Edge("armhole", [fc.Line(fc.P(w, h), fc.P(w, h - attach))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - attach), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(r, 0.0))]),
        # the rounded front corner (maru): a quarter-arc from (r,0) up to (0,r)
        fc.Edge("maru", [fc.curve_through(fc.P(r, 0.0), fc.P(0.0, r), bulge=0.28, side=1.0)]
                if r > 1.0 else [fc.Line(fc.P(r, 0.0), fc.P(0.0, r))]),
    ]
    internals = [fc.Internal("furi-reference",
                             [fc.P(w, h - attach), fc.P(w - 30.0, h - attach)], kind="marking")]
    return fc.Piece(
        "body", edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve attachment match"),
                 fc.Notch("armhole", 1.0, "furi start — do not sew below")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="shoulder", mirror=True),
        label="Body half (身頃 migoro, maru corner)")


def build_okumi():
    w, h = OKUMI_W, haori_length
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("front_edge", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("body_edge", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("chi-seat",
                             [fc.P(w - collar_finished, chi_drop),
                              fc.P(w - collar_finished + 25.0, chi_drop)], kind="marking")]
    return fc.Piece(
        "okumi", edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("front_edge", 0.5, "collar run midpoint"),
                 fc.Notch("body_edge", 0.5, "body panel match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel (衽 okumi)")


def build_sleeve():
    w, h = sleeve_reach, sleeve_depth
    attach = SLEEVE_ATTACH
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("sleeve_end", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("sleeve_hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("furi", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - attach))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, h - attach), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        allowances={"sleeve_hem": hem_allowance, "fold": 0.0, "furi": seam_allowance},
        notches=[fc.Notch("attach", 0.5, "body armhole match"),
                 fc.Notch("furi", 1.0, "furi top — attachment begins here")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve (袖 sode)")


def build_collar():
    ln = MEASURED.get("collar_run", haori_length * 2.0)
    w = COLLAR_CUT_W
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_right", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_left", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("maeeri-fold",
                    [fc.P(0.0, collar_finished + turn_of_cloth * 0.5),
                     fc.P(ln, collar_finished + turn_of_cloth * 0.5)], kind="marking"),
        fc.Internal("centre-back-neck", [fc.P(ln * 0.5, 0.0), fc.P(ln * 0.5, w * 0.4)],
                    kind="marking"),
    ]
    return fc.Piece(
        "collar", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back neck"),
                 fc.Notch("neck_edge", 0.25, "shoulder match"),
                 fc.Notch("neck_edge", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.2), fc.P(ln * 0.1, w * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Collar (衿 eri) — cut double for the maeeri fold")


def build_chi():
    ln, w = 90.0, 20.0
    return fc.Piece(
        "chi",
        [fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
         fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
         fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
         fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))])],
        seam_allowance=seam_allowance, allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.5, "loop fold point")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Cord loop (乳 chi)")


def build_body_lining():
    """The 羽裏 (hauro) body lining (cut 2, on fold): the shell body run less `lining_reduction`
    so it does not peek. Its side and armhole are declared against the shell so the lining is a
    real member of the pattern, not bolt goods.
    """
    w = HALF_BODY - lining_reduction
    h = haori_length - lining_reduction
    attach = SLEEVE_ATTACH - lining_reduction
    edges = [
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("back_neck", [fc.curve_through(fc.P(0.0, h), fc.P(w * 0.42, h),
                                               bulge=0.20, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.42, h), fc.P(w, h))]),
        fc.Edge("armhole", [fc.Line(fc.P(w, h), fc.P(w, h - attach))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - attach), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "body_lining", edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve lining match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="shoulder", mirror=True),
        label="Body lining (羽裏 hauro, cut 2)")


def build_sleeve_lining():
    """The sleeve lining (cut 2, on fold): the sleeve run less `lining_reduction`."""
    w = sleeve_reach - lining_reduction
    h = sleeve_depth - lining_reduction
    attach = SLEEVE_ATTACH - lining_reduction
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("sleeve_end", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("sleeve_hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("furi", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - attach))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, h - attach), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "sleeve_lining", edges, seam_allowance=seam_allowance,
        allowances={"sleeve_hem": hem_allowance, "fold": 0.0},
        notches=[fc.Notch("attach", 0.5, "body lining match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve lining (cut 2)")


def build():
    pattern = fc.PatternSet("kimono-haori")
    every = target_piece == "set"
    body = build_body()
    okumi = build_okumi()
    MEASURED["back_neck"] = body.edge("back_neck").length(0.05)
    MEASURED["front_edge"] = okumi.edge("front_edge").length(0.05)
    MEASURED["collar_run"] = (MEASURED["back_neck"] * 2.0 + MEASURED["front_edge"] * 2.0)
    MEASURED["armhole"] = body.edge("armhole").length(0.05)

    builders = {"body": body, "okumi": okumi, "sleeve": build_sleeve,
                "collar": build_collar, "chi": build_chi,
                "body_lining": build_body_lining, "sleeve_lining": build_sleeve_lining}

    if not every:
        if target_piece in ("body", "okumi"):
            pattern.add(builders[target_piece])
        elif target_piece in builders:
            pattern.add(builders[target_piece]())
        return _finish(pattern, body, okumi)

    sleeve = build_sleeve()
    collar = build_collar()
    chi = build_chi()
    body_lining = build_body_lining()
    sleeve_lining = build_sleeve_lining()
    for piece in (body, okumi, sleeve, collar, chi, body_lining, sleeve_lining):
        pattern.add(piece)

    MEASURED["sleeve_attach"] = sleeve.edge("attach").length(0.05)
    # The sleeve attaches along its SOLVED attachment length only (furi stays open).
    pattern.declare_seam(("sleeve", "attach"), ("body", "armhole"), tol=0.5)
    pattern.declare_seam(("okumi", "body_edge"), ("body", "side"), tol=1.5,
                         ease=(okumi.edge("body_edge").length(0.05)
                               - body.edge("side").length(0.05)))
    pattern.declare_seam(("collar", "neck_edge"),
                         [("body", "back_neck"), ("body", "back_neck"),
                          ("okumi", "front_edge"), ("okumi", "front_edge")], tol=1.5)
    # THE NEW DEPTH: the drafted lining is a real member — its armhole matches the sleeve lining,
    # and its side matches the shell side less the lining reduction.
    pattern.declare_seam(("sleeve_lining", "attach"), ("body_lining", "armhole"), tol=1.0,
                         ease=(sleeve_lining.edge("attach").length()
                               - body_lining.edge("armhole").length()))
    pattern.declare_seam(("body_lining", "side"), ("body", "side"), tol=2.0,
                         ease=(body_lining.edge("side").length()
                               - body.edge("side").length()))

    return _finish(pattern, body, okumi)


def _finish(pattern, body, okumi):
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    bolt_run = total_area / bolt_width
    pattern.bom = [
        {"item": "tanmono bolt cloth (silk or fine cotton)", "qty": round(bolt_run / 10.0) * 10,
         "unit": "mm_length",
         "note": f"shell pieces at {bolt_width:.0f} mm bolt width; every shell piece is a "
                 "rectangle of the bolt used whole — almost no waste."},
        {"item": "羽裏 (hauro) lining silk — the EXPRESSIVE surface",
         "qty": round(bolt_run * 0.9 / 10.0) * 10, "unit": "mm_length",
         "note": "the lining is DRAFTED here (body_lining + sleeve_lining), cut a few mm smaller "
                 "than the shell so it does not peek; in a women's haori the lining is the "
                 "expressive surface while the outside stays plain."},
        {"item": "haori-himo cord", "qty": 1, "unit": "count",
         "note": "a braided cord tied between the two chi loops — the garment's ONLY fastening."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "traditionally hand-sewn so it can be unpicked, washed flat and re-sewn."},
    ]
    pattern.metadata = {
        "fc400_rank": 399, "family": "heritage_global", "fabric_hint": "silk-habutai",
        "tradition": "Japanese (羽織) — the women's lined (袷 awase) jacket, worn open",
        "silhouette_note": "The open haori of the FC-300 draft, deepened to the women's lined "
            "version: the 羽裏 lining is DRAFTED as a real member cut to the shell's runs, and "
            "the lower front corner is rounded (丸 maru). Still closed only by the haori-himo "
            "cord between two chi loops.",
        "hardware": "none — closed only by a braided haori-himo cord between two cloth loops.",
        "solved": {
            "bolt_width_mm": round(bolt_width, 2),
            "body_circuit_mm": round(BODY_CIRCUIT, 2),
            "overlap_mm": round(OVERLAP, 2),
            "bolt_sufficient": BOLT_SUFFICIENT,
            "sleeve_attach_mm": round(SLEEVE_ATTACH, 2),
            "furi_open_mm": round(furi_open, 2),
            "collar_run_mm": round(MEASURED.get("collar_run", 0.0), 2),
            "collar_cut_width_mm": round(COLLAR_CUT_W, 2),
            "maru_radius_mm": round(maru_radius, 1),
            "lining_reduction_mm": round(lining_reduction, 1),
            "note": "inherits the FC-300 haori tanmono solve (bolt is the unit, overlap solved, "
                    "furi kept open, collar solved to the measured run) and ADDS a DRAFTED lining "
                    "cut to the shell's runs less a small reduction, plus the maru front corner.",
        },
        "cultural_note": "The haori is Japanese; the 紋付 (montsuki) crested formal haori is NOT "
            "drafted (a 家紋/kamon is a family's mark, not a decoration, and this cartridge places "
            "none), and the surface dyeing traditions (友禅 yūzen, 絞り shibori) belong to their "
            "own crafts.",
        "worn_over": "a kimono; the haori hangs OPEN and is never wrapped closed.",
        "drafting": "Made to measure via the bolt width and chest; the lining is drafted to the "
            "shell and the front corner is rounded.",
    }
    return pattern


result = build()
