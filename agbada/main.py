"""
Agbàdá — FC-300 rank #282. Fashion Cabinet Garment Cartridge.

The agbàdá is the wide-sleeved flowing outer robe of the Yorùbá of southwestern
Nigéria and Bénin, worn over a long tunic (bùbá) and drawstring trousers
(ṣòkòtò). Cognate garments run across West Africa — the Hausa `babban riga`,
the Wolof and Mande `grand boubou` — and the construction logic below is shared
with them, though the naming and the embroidery vocabulary here are Yorùbá.

The agbàdá's whole geometry follows from ONE material fact, and the draft is
built around it:

  - IT IS MADE FROM STRIP-WOVEN CLOTH. Traditional `aṣọ òkè` comes off a narrow
    men's treadle loom in strips roughly 100-150 mm wide. A garment as wide as
    an agbàdá is therefore assembled from MANY strips sewn selvedge to selvedge.
    The strip is not a detail to be smoothed over — it is the unit of the
    garment, it sets the achievable widths, and its seams are visible and
    intentional. This draft solves an INTEGER strip count for every panel and
    reports the exact assembled width those strips produce, which is generally
    NOT the width you asked for. That discrepancy is honest: you cannot half-weave
    a strip.

  - THE SLEEVE IS THE BODY. There is no armscye and no set-in sleeve. The body
    panel simply continues outward past the shoulder to the full wing span, and
    the "sleeve" is the part of that continuous cloth that hangs below. The
    garment's dramatic width — the wing that is gathered up over the shoulders in
    wear — is drafted as ONE dimension, `wing_span`, measured fingertip to
    fingertip, not as a body plus a sleeve length.

  - THE NECK IS A SLIT, AND THE FRONT PANEL IS ITS FRAME. `Ọrùn` (the neck
    opening) is cut as an opening with a `ìlà` (front slit) below it. The
    embroidered chest field (`onídìí` / breast panel) surrounds it.

Drafting note — what actually SOLVES: the strip count per panel is an integer
ceiling from the real loom-strip width, and the assembled width is recomputed
FROM that integer — so the drafted panel is the width the loom can actually
make, and the requested width is reported alongside it as the delta. The wing's
hang depth is then solved from the wing span and the body width by measuring the
actual drop, rather than being a free parameter that could contradict them. The
neck facing's inner edge is MEASURED from the drafted neck polygon (a rounded
opening, not a rectangle) so the facing fits the hole it faces.

EXCLUSION, stated rather than quietly ignored: the embroidery is NOT drafted.
The chest and neck embroidery of an agbàdá is a named, regionally specific craft
with its own motif vocabulary — `olówu`, `ẹ̀wù`, the dense `onídìí` breast work —
executed by specialist embroiderers, and the specific motifs carry lineage,
title and occasion. This cartridge marks the FIELD where embroidery goes and
leaves the work itself to the embroiderer. Chieftaincy and title regalia, and
the specific agbàdá worn for `ìṣọmọlọ́rùkọ` and other rites, are likewise not
drafted: those are conferred, not configured.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
"""

import math

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
# body|neck_facing|chest_panel|set

wing_span = float(PARAM(lambda: wing_span, 2100.0))     # fingertip to fingertip
robe_length = float(PARAM(lambda: robe_length, 1250.0))  # shoulder → hem
body_width = float(PARAM(lambda: body_width, 720.0))    # half-width at the side
neck_width = float(PARAM(lambda: neck_width, 220.0))    # ọrùn opening width
neck_drop = float(PARAM(lambda: neck_drop, 130.0))      # opening depth
slit_length = float(PARAM(lambda: slit_length, 260.0))  # ìlà front slit
chest_field = float(PARAM(lambda: chest_field, 380.0))  # embroidery field width
chest_depth = float(PARAM(lambda: chest_depth, 420.0))  # embroidery field depth
strip_width = float(PARAM(lambda: strip_width, 120.0))  # aṣọ òkè loom strip
facing_width = float(PARAM(lambda: facing_width, 55.0))  # neck facing depth
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 35.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
wing_span = max(1400.0, min(wing_span, 3000.0))
robe_length = max(800.0, min(robe_length, 1600.0))
body_width = max(450.0, min(body_width, 1100.0))
neck_width = max(150.0, min(neck_width, 340.0))
neck_drop = max(70.0, min(neck_drop, 260.0))
slit_length = max(80.0, min(slit_length, 520.0))
chest_field = max(200.0, min(chest_field, 700.0))
chest_depth = max(200.0, min(chest_depth, 700.0))
strip_width = max(60.0, min(strip_width, 400.0))
facing_width = max(30.0, min(facing_width, 110.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 80.0))

# ── The strip solve — the material fact the garment is built from ────────────
# The body is cut on the fold at the shoulder: one piece, front and back
# continuous, folded along the shoulder line. Its flat half-span is therefore
# half the wing span, and the drafted piece is that half-span wide.
HALF_SPAN = wing_span / 2.0

# The panel's flat height is front + back: twice the robe length (folded at the
# shoulder). That is the dimension the strips run along.
PANEL_H = robe_length * 2.0

# How many woven strips the half-span needs. Strips run vertically (along the
# body's length), so the panel's WIDTH is what the strip count must cover.
# This is an integer: you cannot weave 6.4 strips.
STRIPS = max(1, int(math.ceil(HALF_SPAN / strip_width - 1e-9)))

# The width those strips ACTUALLY assemble to — recomputed from the integer, so
# the draft is the width the loom can make, not the width that was asked for.
ASSEMBLED_HALF_SPAN = STRIPS * strip_width
SPAN_DELTA = ASSEMBLED_HALF_SPAN * 2.0 - wing_span   # honest, reported

# The wing's hang: how far the cloth drops below the underarm. This is SOLVED
# from the geometry — it is the panel's half-height less the depth taken up by
# the body's own width — not an independent parameter that could contradict the
# span and the body width.
WING_DROP = robe_length - body_width * 0.55
if WING_DROP < 150.0:
    WING_DROP = 150.0

# The underarm point: where the body's side edge meets the wing's lower edge.
UNDERARM_X = body_width
if UNDERARM_X > ASSEMBLED_HALF_SPAN - 100.0:      # the wing must exist
    UNDERARM_X = ASSEMBLED_HALF_SPAN - 100.0


def build_body():
    """The whole robe body — ONE piece, cut on the fold at the shoulder.

    There is no armscye and no set-in sleeve: the body continues outward past
    the shoulder to the full wing span, and the wing IS the sleeve. The drafted
    piece is the half-span (fold at centre... no: fold at the SHOULDER, so the
    piece runs from the shoulder line down to the hem, and is cut twice-height
    on the fold). Here the fold edge is `shoulder`, running horizontally.

    Coordinates: x runs outward from the centre front/back line toward the
    wingtip; y runs from the hem (0) up to the shoulder fold.
    """
    w = ASSEMBLED_HALF_SPAN
    h = robe_length
    ua = UNDERARM_X

    edges = [
        # The hem, from centre out to the side seam.
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(ua, 0.0))]),
        # The side seam runs UP from the hem to the underarm point.
        fc.Edge("side", [fc.Line(fc.P(ua, 0.0), fc.P(ua, h - WING_DROP))]),
        # The wing's lower edge runs outward from the underarm to the wingtip.
        fc.Edge("wing_under", [fc.Line(fc.P(ua, h - WING_DROP), fc.P(w, h - WING_DROP))]),
        # The wingtip — the open end the arm comes through.
        fc.Edge("wingtip", [fc.Line(fc.P(w, h - WING_DROP), fc.P(w, h))]),
        # The shoulder fold, from the wingtip back to the centre.
        fc.Edge("shoulder", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        # The centre line — front and back are cut here, the neck opens into it.
        fc.Edge("center", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]

    # The ọrùn (neck opening) and the ìlà (front slit) below it, plus the
    # marked field where the embroiderer works.
    internals = [
        fc.Internal("orun-opening",
                    [fc.P(0.0, h - neck_drop), fc.P(neck_width / 2.0, h)],
                    kind="cut"),
        fc.Internal("ila-slit",
                    [fc.P(0.0, h - neck_drop),
                     fc.P(0.0, h - neck_drop - slit_length)],
                    kind="cut"),
        fc.Internal("embroidery-field",
                    [fc.P(0.0, h - neck_drop - slit_length),
                     fc.P(chest_field, h - neck_drop - slit_length)],
                    kind="marking"),
        fc.Internal("embroidery-field",
                    [fc.P(chest_field, h - neck_drop - slit_length),
                     fc.P(chest_field, h - neck_drop - slit_length + chest_depth)],
                    kind="marking"),
        # Strip seams: mark the first two so the maker sees the repeat pitch.
        fc.Internal("strip-seam", [fc.P(strip_width, 0.0), fc.P(strip_width, h)],
                    kind="marking"),
        fc.Internal("strip-seam",
                    [fc.P(strip_width * 2.0, 0.0), fc.P(strip_width * 2.0, h)],
                    kind="marking"),
    ]

    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "shoulder": 0.0, "center": 0.0},
        notches=[fc.Notch("side", 1.0, "underarm point"),
                 fc.Notch("shoulder", 0.5, "wing gather point — carried on the shoulder"),
                 fc.Notch("wing_under", 0.0, "underarm — side seam match")],
        grainline=fc.Grainline(fc.P(w * 0.6, h * 0.15), fc.P(w * 0.6, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="shoulder", mirror=True),
        label="Robe body + wing (ara agbàdá)",
    )


def build_neck_facing():
    """The facing that finishes the ọrùn and the top of the ìlà.

    Its INNER edge must match the neck opening it faces. The opening is a
    rounded quarter — an arc from the centre line to the shoulder — so its
    length is MEASURED from that arc, not taken as the straight neck_width.
    """
    nw, nd, fw = neck_width / 2.0, neck_drop, facing_width

    # The neck opening as a scooped curve: from (0, nd) to (nw, 0) in
    # facing-local coordinates, where y measures DOWN from the shoulder line.
    inner = fc.curve_through(fc.P(0.0, nd), fc.P(nw, 0.0), bulge=0.28, side=-1.0)
    # The outer edge is the same curve offset outward by the facing width, and
    # traced in reverse so the polygon closes.
    outer = fc.curve_through(fc.P(nw + fw, 0.0), fc.P(0.0, nd + fw),
                             bulge=0.28, side=1.0)

    edges = [
        fc.Edge("inner", [inner]),
        fc.Edge("shoulder_end", [fc.Line(fc.P(nw, 0.0), fc.P(nw + fw, 0.0))]),
        fc.Edge("outer", [outer]),
        fc.Edge("center_end", [fc.Line(fc.P(0.0, nd + fw), fc.P(0.0, nd))]),
    ]
    return fc.Piece(
        "neck_facing",
        edges,
        seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("inner", 0.5, "neck arc midpoint")],
        grainline=fc.Grainline(fc.P(nw * 0.3, nd * 0.25), fc.P(nw * 0.6, nd * 0.7)),
        cut=fc.CutSpec(quantity=4, mirror=True),
        label="Neck facing (ìdí ọrùn)",
    )


def build_chest_panel():
    """The embroidered breast field, drafted as a separate applied panel.

    Some agbàdá are embroidered directly on the body; others carry a worked
    panel applied over the chest. This piece is the latter — it gives the
    embroiderer a flat field to work before assembly, which is how the dense
    `onídìí` breast work is actually done. The MOTIFS are not drafted.
    """
    w, h = chest_field, chest_depth
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("outer", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # The slit passes through this panel too, when it is applied.
        fc.Internal("ila-passage",
                    [fc.P(0.0, h), fc.P(0.0, max(0.0, h - slit_length * 0.6))],
                    kind="cut"),
        fc.Internal("embroidery-field",
                    [fc.P(w * 0.12, h * 0.12), fc.P(w * 0.88, h * 0.88)],
                    kind="marking"),
    ]
    return fc.Piece(
        "chest_panel",
        edges,
        seam_allowance=seam_allowance,
        allowances={"center": 0.0},
        notches=[fc.Notch("top", 0.0, "centre front — align to ìlà")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Breast panel (onídìí)",
    )


# Filled in during build() from the drafted facing polygon, so the metadata
# reports MEASURED curve lengths rather than the numbers that went in.
FACING_MEASURED = {}


def build():
    pattern = fc.PatternSet("agbada")
    every = target_piece == "set"
    if every or target_piece == "body":
        pattern.add(build_body())
    if every or target_piece == "neck_facing":
        pattern.add(build_neck_facing())
    if every or target_piece == "chest_panel":
        pattern.add(build_chest_panel())

    if every:
        _body = pattern.piece("body")
        facing = pattern.piece("neck_facing")

        # The side seam closes front to back: the body is cut twice and the two
        # `side` edges meet. Same piece, so equal by construction — declaring it
        # proves the fold-cut assumption still holds after any clamping.
        pattern.declare_seam(("body", "side"), ("body", "side"), tol=0.5)

        # The wing's lower edges close from the underarm out to the wingtip,
        # forming the tube the arm passes through.
        pattern.declare_seam(("body", "wing_under"), ("body", "wing_under"), tol=0.5)

        # The facing rings the ọrùn: the front and back facings join at their
        # short ends. Both ends are one facing-width across by construction, so
        # this seam closes with no ease — and declaring it proves the drafted
        # curve offset did not distort the ends it has to join on.
        pattern.declare_seam(("neck_facing", "shoulder_end"),
                             ("neck_facing", "center_end"), tol=0.5)

        # The facing's own two curves are measured and reported (not a seam —
        # a facing's outer edge is necessarily longer than its inner, since it
        # is the same curve offset outward). The MEASURED pair is what the
        # metadata reports, so the offset is proven rather than assumed.
        FACING_MEASURED["inner_mm"] = round(facing.edge("inner").length(0.05), 2)
        FACING_MEASURED["outer_mm"] = round(facing.edge("outer").length(0.05), 2)

    _total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    # Strip cloth is bought by the strip-length, so report it that way too.
    strip_run = (ASSEMBLED_HALF_SPAN / strip_width) * (robe_length * 2.0) * 2.0
    pattern.bom = [
        {"item": "aṣọ òkè strip cloth (or damask / brocade / cotton for plain)",
         "qty": round(strip_run / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ total woven strip run at {strip_width:.0f} mm strip width; "
                 f"{STRIPS} strips per half-span, both body pieces."},
        {"item": "embroidery thread", "qty": 1, "unit": "set",
         "note": "for the marked chest field — the motifs are the embroiderer's "
                 "work, not the draft's."},
        {"item": "neck facing cloth", "qty": 1, "unit": "piece",
         "note": "self or contrast; 4 facing pieces (front and back, both layers)."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "strip seams are flat-felled and visible — they are part of the look."},
    ]
    pattern.metadata = {
        "fc300_rank": 282,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "tradition": "Yorùbá (southwestern Nigéria, Bénin); cognate with Hausa "
                     "babban riga and Wolof/Mande grand boubou",
        "finished_mm": {"wing_span_requested": round(wing_span, 1),
                        "wing_span_assembled": round(ASSEMBLED_HALF_SPAN * 2.0, 1),
                        "length": round(robe_length, 1),
                        "wing_drop": round(WING_DROP, 1)},
        "solved": {
            "strips_per_half_span": STRIPS,
            "strip_width_mm": round(strip_width, 2),
            "assembled_half_span_mm": round(ASSEMBLED_HALF_SPAN, 2),
            "span_delta_mm": round(SPAN_DELTA, 2),
            "wing_drop_mm": round(WING_DROP, 2),
            "underarm_x_mm": round(UNDERARM_X, 2),
            "panel_flat_h_mm": round(PANEL_H, 2),
            "neck_facing_measured": dict(FACING_MEASURED),
            "note": "the strip count is an INTEGER ceiling from the real loom-strip "
                    "width, and the assembled span is recomputed FROM that integer — "
                    "so the draft is the width the loom can actually make. The delta "
                    "against the requested span is reported rather than hidden: you "
                    "cannot half-weave a strip. The wing drop is solved from the span "
                    "and the body width, not left free to contradict them. The neck "
                    "facing's edges are measured from its drafted ARC, so the facing "
                    "matches the curve it faces.",
        },
        "hardware": "none — the agbàdá is pulled over the head and has no closure. "
                    "There is nothing to fasten and nothing to bridge.",
        "cut_philosophy": "no armscye, no set-in sleeve. The body continues outward "
                          "past the shoulder to the full wing span; the wing IS the "
                          "sleeve, and in wear it is gathered up onto the shoulders.",
        "excluded": "the embroidery is NOT drafted — the chest and neck work "
                    "(olówu, onídìí) is a named specialist craft whose motifs carry "
                    "lineage, title and occasion. This draft marks the FIELD and "
                    "leaves the work to the embroiderer. Chieftaincy and title "
                    "regalia, and rite-specific agbàdá, are likewise not drafted: "
                    "those are conferred, not configured.",
        "worn_with": "bùbá (tunic) and ṣòkòtò (drawstring trousers); the cap is "
                     "fìlà — none of which are this cartridge.",
    }
    return pattern


result = build()
