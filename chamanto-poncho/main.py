"""
Chamanto poncho — Fashion Cabinet Heritage Cartridge (FC-500 #496, heritage_global; Chile).

The chamanto is the fine dress poncho of the Chilean huaso — the elegant counterpart to the
everyday manta. It is woven in fine wool and silk, and its defining features are that it is
REVERSIBLE (a light "day" face and a dark "night" face, so it is woven double and finished so
both sides show), it is banded with the LISTADO — the field of fine coloured stripes — and it
is edged with the woven TRENCILLA border. Traditionally it is woven whole on the loom with the
neck slit left in the weaving; this cartridge drafts it as its assembled form so a maker
working from cut cloth can build one, while marking the listado and trencilla zones the weaver
fills.

Two things the draft solves honestly:

  1. THE NECK SLIT IS CENTRED AND SIZED FROM THE HEAD, ON THE WHOLE CLOTH. The chamanto is one
     rectangle (or two loom widths seamed at the shoulder line) with a central slit for the
     head. The slit length is solved from the head girth so it clears the head but no more, and
     it is centred on the cloth — an off-centre or oversized slit is the first thing a poncho
     draft gets wrong.

  2. IT IS REVERSIBLE, SO THE BORDER IS SYMMETRIC. Because both faces show, the trencilla
     border and the listado are drawn symmetric front-to-back and the cloth is finished on both
     faces (a marked instruction, since the kernel drafts the flat form).

Pieces:
  - cloth  : the whole chamanto rectangle (two loom halves seamed at the shoulder), neck slit.
  - border : one representative trencilla border strip (for the weaver), cut to the perimeter.

Hardware: none — a poncho has no closure.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))   # cloth|border|set

cloth_width = float(PARAM(lambda: cloth_width, 1500.0))   # across the shoulders, tip to tip
cloth_length = float(PARAM(lambda: cloth_length, 1150.0))  # front/back drop (per face)
head_girth = float(PARAM(lambda: head_girth, 580.0))
neck_slit_ease = float(PARAM(lambda: neck_slit_ease, 60.0))
trencilla_width = float(PARAM(lambda: trencilla_width, 80.0))  # woven border width
listado_count = int(PARAM(lambda: listado_count, 7))       # stripe bands in the listado
fringe_depth = float(PARAM(lambda: fringe_depth, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
cloth_width = max(1100.0, min(cloth_width, 1900.0))
cloth_length = max(850.0, min(cloth_length, 1450.0))
head_girth = max(500.0, min(head_girth, 660.0))
neck_slit_ease = max(20.0, min(neck_slit_ease, 140.0))
trencilla_width = max(40.0, min(trencilla_width, 140.0))
listado_count = max(3, min(listado_count, 14))
fringe_depth = max(0.0, min(fringe_depth, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The neck slit solve — centred, sized from the head ───────────────────────
# The slit must clear the head girth: a slit of length L opens to roughly 2L of perimeter when
# spread, so L is about half the head girth plus ease, centred on the cloth.
NECK_SLIT = head_girth / 2.0 + neck_slit_ease
NECK_SLIT = min(NECK_SLIT, cloth_length * 0.5)   # never longer than half the drop
CENTRE_X = cloth_width / 2.0
CENTRE_Y = cloth_length                          # the shoulder line is the top edge (fold/seam)


def build_cloth():
    """The whole chamanto rectangle: cloth_width x cloth_length, with a centred neck slit and
    marked listado + trencilla zones. Drawn as the flat draped cloth (the shoulder line is the
    top edge; the poncho hangs front and back from it)."""
    w = cloth_width
    h = cloth_length
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("hem_front", [fc.Line(p0, p1)]),
        fc.Edge("selvedge_r", [fc.Line(p1, p2)]),
        fc.Edge("shoulder_line", [fc.Line(p2, p3)]),   # the top: where it folds/seams over
        fc.Edge("selvedge_l", [fc.Line(p3, p0)]),
    ]
    cx = CENTRE_X
    internals = [
        # the centred neck slit, along the shoulder line.
        fc.Internal("neck-slit", [fc.P(cx - NECK_SLIT / 2.0, h),
                                  fc.P(cx + NECK_SLIT / 2.0, h)], kind="marking"),
        # the trencilla border, inset from all four edges (symmetric, since reversible).
        fc.Internal("trencilla-border",
                    [fc.P(trencilla_width, trencilla_width),
                     fc.P(w - trencilla_width, trencilla_width),
                     fc.P(w - trencilla_width, h - trencilla_width),
                     fc.P(trencilla_width, h - trencilla_width)], kind="marking"),
        # the reversibility instruction line (day face / night face).
        fc.Internal("reversible-face", [fc.P(cx, trencilla_width + 20.0),
                                        fc.P(cx, h - trencilla_width - 20.0)], kind="marking"),
    ]
    # the listado: fine coloured stripe bands running down the cloth.
    field_top = trencilla_width + 40.0
    field_bot = h - trencilla_width - 40.0
    for i in range(1, listado_count + 1):
        x = trencilla_width + (w - 2.0 * trencilla_width) * i / (listado_count + 1)
        internals.append(fc.Internal(f"listado-{i}", [fc.P(x, field_top), fc.P(x, field_bot)],
                                     kind="marking"))
    return fc.Piece(
        "cloth", edges,
        seam_allowance=seam_allowance,
        allowances={"hem_front": 0.0, "shoulder_line": 0.0,
                    "selvedge_r": 0.0, "selvedge_l": 0.0},
        notches=[fc.Notch("shoulder_line", 0.5, "neck centre"),
                 fc.Notch("hem_front", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Chamanto cloth (reversible, listado + trencilla marked)",
    )


def build_border():
    """One representative trencilla border strip, for the weaver: a long band the width of the
    woven border, its length the cloth perimeter."""
    perim = 2.0 * (cloth_width + cloth_length)
    w = trencilla_width
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(perim, 0.0)
    p2 = fc.P(perim, w)
    p3 = fc.P(0.0, w)
    edges = [
        fc.Edge("inner", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "border", edges,
        seam_allowance=seam_allowance,
        allowances={"inner": 0.0, "outer": 0.0},
        notches=[fc.Notch("inner", 0.25, "corner"),
                 fc.Notch("inner", 0.5, "corner"),
                 fc.Notch("inner", 0.75, "corner")],
        grainline=fc.Grainline(fc.P(perim * 0.1, w * 0.5), fc.P(perim * 0.9, w * 0.5)),
        internals=[fc.Internal("weave-guide", [fc.P(0.0, w * 0.5), fc.P(perim, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Trencilla border strip (the weaver's unit)",
    )


def build():
    pattern = fc.PatternSet("chamanto-poncho")
    everything = target_piece == "set"
    if everything or target_piece == "cloth":
        pattern.add(build_cloth())
    if everything or target_piece == "border":
        pattern.add(build_border())
    # No sewn piece-to-piece seam: the chamanto is (traditionally) woven whole with the slit in
    # the weaving, and the border is applied. The only seam a cut-cloth maker uses is the loom
    # centre seam, which is marked, not a pattern-piece seam.

    pattern.bom = [
        {"item": "fine wool & silk (reversible weave)", "qty": round(
            cloth_width * cloth_length / 1000.0), "unit": "cm2_face",
         "note": f"woven DOUBLE and reversible — a light day face and a dark night face — so "
                 f"both sides show. Two loom halves ~{cloth_width / 2.0:.0f} mm wide are "
                 f"seamed at the shoulder line."},
        {"item": "trencilla border", "qty": round(2.0 * (cloth_width + cloth_length)),
         "unit": "mm_length",
         "note": f"the woven border round the whole perimeter, {trencilla_width:.0f} mm wide."},
        {"item": "fringe (optional)", "qty": round(2.0 * cloth_width), "unit": "mm_length",
         "note": f"{fringe_depth:.0f} mm at the front and back hems, if used."},
    ]
    pattern.metadata = {
        "fc500_rank": 496,
        "family": "heritage_global",
        "fabric_hint": "lana-tejida",
        "finished_mm": {
            "cloth_width": round(cloth_width, 1),
            "cloth_length": round(cloth_length, 1),
            "neck_slit": round(NECK_SLIT, 1),
            "trencilla_width": round(trencilla_width, 1),
        },
        "solved": {
            "neck_slit_mm": round(NECK_SLIT, 2),
            "head_girth_mm": round(head_girth, 1),
            "centre_x_mm": round(CENTRE_X, 2),
            "listado_count": listado_count,
            "trencilla_width_mm": round(trencilla_width, 2),
            "note": "the neck slit is CENTRED on the cloth and sized from the head girth (half "
                    "the head girth plus ease, capped at half the drop) so it clears the head "
                    "but no more — an off-centre or oversized slit is the first thing a poncho "
                    "draft gets wrong. Because the chamanto is REVERSIBLE, the trencilla border "
                    "and the listado are drawn symmetric front-to-back, and both faces are "
                    "finished (a marked instruction, as the kernel drafts the flat form).",
        },
        "heritage": {
            "garment": "chamanto — the fine reversible dress poncho of the Chilean huaso",
            "construction": "one reversible cloth (two loom halves seamed at the shoulder), a "
                            "centred neck slit, the listado striped field, and the woven "
                            "trencilla border round the perimeter",
            "reversible": "a light day face and a dark night face, woven double so both show",
            "excluded": "no specific listado colourway or trencilla motif is drawn — those are "
                        "the weaver's, and the finest chamantos are the work of named weavers "
                        "of Doñihue",
        },
        "hardware": "none — a poncho has no closure.",
    }
    return pattern


result = build()
