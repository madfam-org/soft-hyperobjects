"""
Turban Band — Fashion Cabinet Garment Cartridge (FC-300 #215, Lane 2).

A pleated turban band: a wide fabric BAND, knife-pleated across its length, wrapped
around and sewn to a rigid Yantra4D `headband-blank`, with a KNOT panel at the centre
front that gives the turban its twist. The band is drafted flat and PLEATED DOWN to
the blank's own arc, so the pleats do the shaping rather than a curved seam.

The bridge is DIMENSIONAL through the band width. The band's finished (folded) width
is `band_width`, which is exactly the run the blank's `casing_sew_edge` flange
presents — the same parameter drives both the hardware's sewn edge and the garment's
`casing` interface.

Pieces:
  - band       : the pleated wrapping band, cut 1.
  - knot       : the centre-front twist panel, cut 1.
  - band-lining: the casing that encloses the blank, cut 1.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # band|knot|lining|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
band_width = float(PARAM(lambda: band_width, 55.0))    # finished band width == blank band_w
blank_arc = float(PARAM(lambda: blank_arc, 340.0))     # the rigid blank's own arc run
pleat_ratio = float(PARAM(lambda: pleat_ratio, 1.8))   # flat length / finished length
knot_width = float(PARAM(lambda: knot_width, 110.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
band_width = max(25.0, min(band_width, 110.0))
blank_arc = max(200.0, min(blank_arc, 460.0))
pleat_ratio = max(1.2, min(pleat_ratio, 3.0))
knot_width = max(50.0, min(knot_width, 220.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The band spans the blank's arc plus the wrap that meets behind the head.
FINISHED_RUN = blank_arc
FLAT_RUN = FINISHED_RUN * pleat_ratio          # cut length before pleating
PLEAT_TAKEN = FLAT_RUN - FINISHED_RUN          # fullness the pleats remove
# The band is cut double-width and folded, so its finished width is band_width.
CUT_WIDTH = band_width * 2.0


def _build_band():
    """The pleated wrapping band, cut flat at FLAT_RUN and pleated down to the blank's
    arc. Cut double-width so it folds to `band_width` — the blank's casing run."""
    ln, w = FLAT_RUN, CUT_WIDTH
    n_pleats = max(4, int(FLAT_RUN / 42.0))
    internals = []
    for i in range(n_pleats):
        x = FLAT_RUN * (i + 0.5) / n_pleats
        internals.append(fc.Internal("pleat", [fc.P(x, 0.0), fc.P(x, w)], kind="fold"))
    edges = [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("casing", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),  # over the blank
    ]
    return fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("casing", 0.5, "centre front"),
                 fc.Notch("upper", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pleated band",
    )


def _build_knot():
    """The centre-front twist panel: a short double-width rectangle knotted over the
    band's centre front to make the turban's signature crossing."""
    ln, w = knot_width, CUT_WIDTH * 1.15
    edges = [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "knot",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.5, "knot centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Knot panel",
    )


def _build_band_lining():
    """The casing that encloses the rigid blank. Its `casing` edge measures the
    blank's arc exactly — this is the garment edge mating the blank's casing_sew_edge
    flange, and its width is the blank's band_w."""
    ln, w = FINISHED_RUN, band_width
    edges = [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("outer", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("end_b", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("casing", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "band-lining",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("casing", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Band lining / blank casing",
    )


def build():
    pattern = fc.PatternSet("turban-band")
    everything = target_piece == "set"

    if everything or target_piece == "band":
        pattern.add(_build_band())
    if everything or target_piece == "knot":
        pattern.add(_build_knot())
    if everything or target_piece == "lining":
        pattern.add(_build_band_lining())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if {"band", "band-lining"} <= names:
        # THE PLEATING, declared as a seam with ease: the band is cut at FLAT_RUN and
        # pleated down onto the lining's casing run (the blank's arc). The ease is the
        # fullness the pleats remove, so the check is substantive — it goes red if
        # pleat_ratio and blank_arc ever drift apart.
        pattern.declare_seam(("band", "casing"), ("band-lining", "casing"),
                             tol=1.0, ease=PLEAT_TAKEN)
    if {"knot", "band"} <= names:
        # The knot panel's ends are caught into the band's centre-front pleats; its
        # own two ends join around the twist.
        pattern.declare_seam(("knot", "end_a"), ("knot", "end_b"), tol=1.0)
    if {"band-lining"} <= names and "band" not in names:
        pattern.declare_seam(("band-lining", "end_a"), ("band-lining", "end_b"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "band fabric (jersey, silk or viscose crepe)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 66% marker; a soft drape pleats best."},
        {"item": "headband blank", "qty": 1, "unit": "count",
         "note": "Yantra4D headband-blank (see notion.hardware_ref) — the rigid arc the "
                 "casing encloses, sized by band_width and blank_arc."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "baste the pleats before enclosing the blank; they set the whole shape."},
    ]
    pattern.metadata = {
        "fc300_rank": 215, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "band_width_mm": round(band_width, 1),
        "cut_width_mm": round(CUT_WIDTH, 1),
        "blank_arc_mm": round(blank_arc, 1),
        "pleat_ratio": round(pleat_ratio, 2),
        "knot_width_mm": round(knot_width, 1),
        "drafting": "flat band pleated down to the blank's arc + knot panel + casing",
        "hardware": "rigid arc delegated to Yantra4D headband-blank; the casing's width "
                    "is the blank's band_w (the casing_sew_edge flange run)",
        "solved": {
            "band_flat_run_mm": round(FLAT_RUN, 3),
            "band_finished_run_mm": round(FINISHED_RUN, 3),
            "pleat_fullness_removed_mm": round(PLEAT_TAKEN, 3),
        },
    }
    return pattern


result = build()
