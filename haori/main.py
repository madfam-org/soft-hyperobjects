"""
Haori (羽織) — FC-300 rank #286. Fashion Cabinet Garment Cartridge.

The haori is the hip- or thigh-length jacket worn OPEN over a kimono, closed
only by a short braided cord (羽織紐, `haori-himo`) tied between two small loops
at the chest. It is not a coat and not a short kimono: it is a distinct garment
with its own proportions, its own collar treatment, and its own way of hanging.

Every dimension of a haori descends from ONE fact, and this draft is organised
around it:

  - IT IS DRAFTED IN 反物 (`TANMONO`) UNITS, NOT IN BODY MEASUREMENTS. Kimono-
    family garments are cut from a bolt roughly 360-400 mm wide, and the pieces
    are RECTANGLES of that bolt width used whole — the body panel is one bolt
    width, the sleeve is one bolt width, the okumi (front panel) is a half. The
    fit does not come from cutting to a body; it comes from choosing where the
    straight seams fall. This draft therefore takes `bolt_width` as a real
    parameter and solves the body's overlap FROM it, rather than cutting shaped
    panels to a chest girth. That is why a haori fits a range of bodies.

  - THE 前衿 (`MAEERI`) IS FOLDED BACK, AND THAT IS WHAT MAKES IT A HAORI. The
    collar band runs down the front and is folded outward along its length to
    form a shallow lapel. So the collar strip must be drafted at DOUBLE the
    finished width plus turn-of-cloth — and the length it needs is the MEASURED
    run of the neck and both front edges, not a neck circuit.

  - THE SLEEVE HANGS FREE BELOW THE ARM. The sleeve is attached only along its
    upper portion (`振り`, the `furi` opening is left unsewn below), so the
    attachment length is SHORTER than the sleeve's full depth. Drafting them as
    equal is the commonest error and it closes an opening that is supposed to
    be there.

  - 乳 (`CHI`): the two small loops the cord ties between. Their placement is
    solved from the collar's measured run, so they sit at the same height on
    both fronts.

Drafting note — what actually SOLVES: the body's front overlap is solved FROM
the bolt width and the target chest circuit, so the draft reports how much
overlap the real bolt actually yields (and warns, via metadata, when the bolt is
too narrow to close). The collar strip's length is the MEASURED sum of the back
neck curve and both front edge runs. The sleeve's ATTACHED length is solved as
the sleeve depth less the furi opening, and the armhole is drafted to that
solved length — so the furi stays open. The chi loops are placed from the
measured collar run.

EXCLUSION, stated rather than quietly ignored: the 紋付 (`montsuki`) crested
formal haori is NOT drafted. Its formality is set by the NUMBER and PLACEMENT of
家紋 (kamon, family crests) — one, three or five — and a kamon is a family's
mark, not a decoration. This cartridge will not place crests. The 十徳 (jittoku)
and the haori of specific professional and religious orders are likewise out of
scope. Surface dyeing traditions (yūzen, shibori) belong to their own crafts.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
# body|okumi|sleeve|collar|chi|set

bolt_width = float(PARAM(lambda: bolt_width, 375.0))       # 反物 tanmono width
chest_girth = float(PARAM(lambda: chest_girth, 980.0))     # target circuit
haori_length = float(PARAM(lambda: haori_length, 850.0))   # shoulder → hem
sleeve_depth = float(PARAM(lambda: sleeve_depth, 490.0))   # shoulder → sleeve hem
sleeve_reach = float(PARAM(lambda: sleeve_reach, 340.0))   # shoulder → sleeve end
furi_open = float(PARAM(lambda: furi_open, 170.0))         # unsewn opening below arm
collar_finished = float(PARAM(lambda: collar_finished, 55.0))  # maeeri visible width
neck_drop = float(PARAM(lambda: neck_drop, 95.0))          # back neck scoop
chi_drop = float(PARAM(lambda: chi_drop, 300.0))           # cord loop height
turn_of_cloth = float(PARAM(lambda: turn_of_cloth, 6.0))   # fold-back allowance
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
turn_of_cloth = max(0.0, min(turn_of_cloth, 20.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(10.0, min(hem_allowance, 80.0))

# The furi opening cannot swallow the whole sleeve depth — something must attach.
if furi_open > sleeve_depth - 120.0:
    furi_open = max(0.0, sleeve_depth - 120.0)

# ── The tanmono solve — the bolt is the unit, not the body ───────────────────
# The body is TWO bolt widths (left and right halves, each folded at the
# shoulder). The okumi (front panel) is a half bolt each side. So the total
# cloth going round the body is:
BODY_CIRCUIT = bolt_width * 2.0 + bolt_width          # 2 body halves + 2 okumi
# The OVERLAP is what is left after the circuit wraps the chest. This is the
# number that matters: a haori hangs open, but the fronts must still be able to
# meet when the cord is tied.
OVERLAP = BODY_CIRCUIT - chest_girth
BOLT_SUFFICIENT = OVERLAP > 0.0
if not BOLT_SUFFICIENT:
    OVERLAP = 0.0                                     # reported honestly below

OKUMI_W = bolt_width / 2.0
HALF_BODY = bolt_width / 2.0                          # drafted half of one panel

# The SLEEVE ATTACHMENT is the sleeve depth LESS the furi opening. The armhole
# is drafted to this solved length so the furi stays open — attaching the whole
# depth would sew the opening shut.
SLEEVE_ATTACH = sleeve_depth - furi_open

# The collar strip is drafted at DOUBLE its finished width plus turn-of-cloth,
# because it folds back on itself to form the maeeri lapel.
COLLAR_CUT_W = collar_finished * 2.0 + turn_of_cloth

MEASURED = {}


def build_body():
    """One body half (cut 2), a bolt-width RECTANGLE folded at the shoulder.

    No shaping: this is a straight panel of the bolt used whole. The armhole is
    not a scooped curve but a straight opening of the SOLVED attachment length,
    which is what leaves the furi free below it.

    x runs from centre back outward; y from hem (0) up to the shoulder fold.
    """
    w, h = HALF_BODY, haori_length
    attach = SLEEVE_ATTACH

    edges = [
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        # The back neck scoop — the only curve on the piece.
        fc.Edge("back_neck", [fc.curve_through(fc.P(0.0, h), fc.P(w * 0.42, h),
                                               bulge=0.20, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.42, h), fc.P(w, h))]),
        # The armhole: a straight opening of the SOLVED attachment length.
        fc.Edge("armhole", [fc.Line(fc.P(w, h), fc.P(w, h - attach))]),
        # Below the armhole the side seam closes; the furi is the gap above it
        # on the SLEEVE side, marked here for reference.
        fc.Edge("side", [fc.Line(fc.P(w, h - attach), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]

    internals = [
        fc.Internal("furi-reference",
                    [fc.P(w, h - attach), fc.P(w - 30.0, h - attach)],
                    kind="marking"),
    ]

    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve attachment match"),
                 fc.Notch("armhole", 1.0, "furi start — do not sew below")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="shoulder", mirror=True),
        label="Body half (身頃 migoro)",
    )


def build_okumi():
    """The 衽 (okumi) — the front overlap panel, a HALF bolt width (cut 2).

    A straight rectangle. It is what turns the body panels into fronts that can
    meet, and its width is a half bolt by tradition — not a number chosen to
    reach a chest measurement.
    """
    w, h = OKUMI_W, haori_length
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("front_edge", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("body_edge", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # The 乳 (chi) loop seat — solved height, same on both fronts.
        fc.Internal("chi-seat",
                    [fc.P(w - collar_finished, chi_drop),
                     fc.P(w - collar_finished + 25.0, chi_drop)],
                    kind="marking"),
    ]
    return fc.Piece(
        "okumi",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("front_edge", 0.5, "collar run midpoint"),
                 fc.Notch("body_edge", 0.5, "body panel match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel (衽 okumi)",
    )


def build_sleeve():
    """The 袖 (sode) — a bolt-width rectangle folded at the shoulder (cut 2).

    Its `attach` edge is the SOLVED attachment length; the remainder of its
    depth hangs free as the 振り (furi). Drafting the attachment equal to the
    full depth would sew the furi shut, which is the commonest haori error.
    """
    w, h = sleeve_reach, sleeve_depth
    attach = SLEEVE_ATTACH

    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("sleeve_end", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("sleeve_hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        # The furi: the free opening BELOW the attachment. Left unsewn.
        fc.Edge("furi", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h - attach))]),
        # The attachment: what actually sews to the body's armhole.
        fc.Edge("attach", [fc.Line(fc.P(0.0, h - attach), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"sleeve_hem": hem_allowance, "fold": 0.0, "furi": seam_allowance},
        notches=[fc.Notch("attach", 0.5, "body armhole match"),
                 fc.Notch("furi", 1.0, "furi top — attachment begins here")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve (袖 sode)",
    )


def build_collar():
    """The 衿 (eri) — the collar strip, cut at DOUBLE finished width.

    It folds back along its length to form the 前衿 (maeeri) lapel, which is
    what makes the garment read as a haori rather than a short kimono. Its
    LENGTH is the measured run of the back neck plus both front edges.
    """
    ln = MEASURED.get("collar_run", haori_length * 2.0)
    w = COLLAR_CUT_W
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_right", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_left", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # The fold line the maeeri turns back along — at the finished width
        # plus half the turn-of-cloth, so the fold sits where it should once
        # the cloth's own thickness is taken up.
        fc.Internal("maeeri-fold",
                    [fc.P(0.0, collar_finished + turn_of_cloth * 0.5),
                     fc.P(ln, collar_finished + turn_of_cloth * 0.5)],
                    kind="marking"),
        fc.Internal("centre-back-neck",
                    [fc.P(ln * 0.5, 0.0), fc.P(ln * 0.5, w * 0.4)],
                    kind="marking"),
    ]
    return fc.Piece(
        "collar",
        edges,
        seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back neck"),
                 fc.Notch("neck_edge", 0.25, "shoulder match"),
                 fc.Notch("neck_edge", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.2), fc.P(ln * 0.1, w * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Collar (衿 eri) — cut double for the maeeri fold",
    )


def build_chi():
    """The 乳 (chi) — the two small loops the haori-himo cord ties between.

    A short folded strip. Two are made; they are the garment's only fastening
    point, and the cord itself is a separate purchased or braided item.
    """
    ln, w = 90.0, 20.0
    return fc.Piece(
        "chi",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.5, "loop fold point")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Cord loop (乳 chi)",
    )


def build():
    pattern = fc.PatternSet("haori")
    every = target_piece == "set"

    # The body and okumi must be drafted before the collar, whose LENGTH is the
    # measured run of the back neck plus both front edges.
    body = build_body()
    okumi = build_okumi()
    MEASURED["back_neck"] = body.edge("back_neck").length(0.05)
    MEASURED["front_edge"] = okumi.edge("front_edge").length(0.05)
    # Back neck is cut twice (two body halves); both fronts run the full length.
    MEASURED["collar_run"] = (MEASURED["back_neck"] * 2.0
                              + MEASURED["front_edge"] * 2.0)
    MEASURED["armhole"] = body.edge("armhole").length(0.05)

    if every or target_piece == "body":
        pattern.add(body)
    if every or target_piece == "okumi":
        pattern.add(okumi)
    if every or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if every or target_piece == "collar":
        pattern.add(build_collar())
    if every or target_piece == "chi":
        pattern.add(build_chi())

    if every:
        sleeve = pattern.piece("sleeve")
        MEASURED["sleeve_attach"] = sleeve.edge("attach").length(0.05)

        # The sleeve attaches along its SOLVED attachment length only. The furi
        # below it is deliberately unsewn — this check proves the armhole was
        # drafted to the attachment, not to the full sleeve depth.
        pattern.declare_seam(("sleeve", "attach"), ("body", "armhole"), tol=0.5)

        # The okumi's body edge meets the body panel's side edge above the hem.
        pattern.declare_seam(("okumi", "body_edge"), ("body", "side"), tol=1.5,
                             ease=(okumi.edge("body_edge").length(0.05)
                                   - body.edge("side").length(0.05)))

        # The collar's neck edge meets the assembled neckline: two back-neck
        # curves plus both front edges. Its length was SOLVED from those
        # measurements, so this closes by construction.
        pattern.declare_seam(
            ("collar", "neck_edge"),
            [("body", "back_neck"), ("body", "back_neck"),
             ("okumi", "front_edge"), ("okumi", "front_edge")],
            tol=1.5)

    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    # Kimono-family cloth is bought by bolt length, so report it that way.
    bolt_run = total_area / bolt_width
    pattern.bom = [
        {"item": "tanmono bolt cloth (silk, wool, or cotton)",
         "qty": round(bolt_run / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ bolt run at {bolt_width:.0f} mm width; every piece is a "
                 "rectangle of the bolt used whole — there is almost no waste."},
        {"item": "haori-himo cord", "qty": 1, "unit": "count",
         "note": "a braided cord, purchased or made; it ties between the two chi "
                 "loops and is the garment's ONLY fastening."},
        {"item": "lining (胴裏 dōura)", "qty": round(bolt_run / 10.0) * 10,
         "unit": "mm_length",
         "note": "a haori is normally fully lined; the lining is often the "
                 "expressive surface, since the outside stays plain."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "traditionally hand-sewn so the garment can be unpicked, washed "
                 "flat as bolt lengths, and re-sewn."},
    ]
    pattern.metadata = {
        "fc300_rank": 286,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "tradition": "Japanese (羽織) — the jacket worn open over a kimono",
        "finished_mm": {"length": round(haori_length, 1),
                        "body_circuit": round(BODY_CIRCUIT, 1),
                        "sleeve_depth": round(sleeve_depth, 1),
                        "collar_finished": round(collar_finished, 1)},
        "solved": {
            "bolt_width_mm": round(bolt_width, 2),
            "body_circuit_mm": round(BODY_CIRCUIT, 2),
            "overlap_mm": round(OVERLAP, 2),
            "bolt_sufficient": BOLT_SUFFICIENT,
            "okumi_width_mm": round(OKUMI_W, 2),
            "sleeve_attach_mm": round(SLEEVE_ATTACH, 2),
            "furi_open_mm": round(furi_open, 2),
            "armhole_mm": round(MEASURED.get("armhole", 0.0), 2),
            "collar_run_mm": round(MEASURED.get("collar_run", 0.0), 2),
            "collar_cut_width_mm": round(COLLAR_CUT_W, 2),
            "back_neck_mm": round(MEASURED.get("back_neck", 0.0), 2),
            "front_edge_mm": round(MEASURED.get("front_edge", 0.0), 2),
            "note": "the BOLT is the unit, not the body: every piece is a rectangle "
                    "of tanmono used whole, and the front OVERLAP is solved FROM the "
                    "bolt width and the target chest rather than the panels being cut "
                    "to a girth. `bolt_sufficient` reports honestly whether the real "
                    "bolt closes the chest at all. The sleeve's ATTACHED length is "
                    "solved as depth less the furi opening and the armhole drafted to "
                    "that solved length — attaching the full depth would sew the furi "
                    "shut, which is the commonest haori error. The collar is cut at "
                    "DOUBLE its finished width plus turn-of-cloth because it folds "
                    "back to form the maeeri, and its LENGTH is the measured run of "
                    "both back-neck curves plus both front edges.",
        },
        "hardware": "none — the haori is closed only by a braided haori-himo cord "
                    "tied between two cloth loops. There is no fastener to bridge.",
        "cut_philosophy": "straight rectangles of the bolt, used whole. Fit comes "
                          "from where the straight seams fall, not from shaping to a "
                          "body — which is why one haori fits a range of wearers and "
                          "why it can be unpicked, washed flat, and re-sewn.",
        "excluded": "the 紋付 (montsuki) crested formal haori is NOT drafted: its "
                    "formality is set by the number and placement of 家紋 (kamon, "
                    "family crests) — one, three or five — and a kamon is a family's "
                    "mark, not a decoration. This cartridge will not place crests. "
                    "The 十徳 (jittoku) and the haori of specific professional and "
                    "religious orders are out of scope, as are the surface dyeing "
                    "traditions (yūzen, shibori), which belong to their own crafts.",
        "worn_over": "a kimono; the haori hangs OPEN and is never wrapped closed.",
    }
    return pattern


result = build()
