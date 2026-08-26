"""
Kente wrapper cloth (women's two-piece) — Fashion Cabinet Heritage Cartridge
(FC-500 #484, heritage_global; Akan/Ewe, Ghana & Togo).

Kente is the strip-woven cloth of the Akan (Asante) and Ewe peoples: narrow warp-striped
strips woven on the men's double-heddle loom and sewn edge-to-edge into a large cloth. The
women's formal ensemble is TWO wrappers plus (often) a matching blouse or cover-cloth: a
large lower wrapper (**ntoma**) wound round from the waist, and a smaller upper wrapper
worn over it or as a cover across the shoulder. This cartridge drafts THAT women's set — a
different garment from the men's single toga-style wearing cloth — and it CUTS NOTHING into
the woven field, because cutting kente destroys the strip weave and the meaning woven into
it.

What the cartridge encodes, and why it is a garment and not a plain rectangle:

  1. THE CLOTH IS AN ASSEMBLY OF STRIPS, AND THE STRIP WIDTH IS REAL. Kente is woven in
     strips of a fixed loom width (`strip_width`, ~90-110 mm) and each wrapper is a whole
     number of strips sewn side by side. The wrapper's width is therefore NOT free — it is
     `strip_count * strip_width`. The draft solves the strip count from the target width
     and reports the TRUE assembled width, snapped to a multiple of the strip.

  2. THE TWO WRAPPERS ARE SIZED FROM THE BODY, BUT USED WHOLE. The lower wrapper wraps the
     hip girth with a real overlap (so it stays closed when tucked); the upper wrapper is a
     fraction of it. Both are whole cloths, hemmed at top and bottom, selvedge at the sides.
     The wrap turns are marked so a wearer knows how each cloth sits, while the cloth stays
     uncut.

Pieces:
  - lower  : the large lower wrapper (ntoma), whole cloth, cut 1, uncut.
  - upper  : the smaller upper wrapper / cover-cloth, whole cloth, cut 1, uncut.
  - strip  : one representative loom strip, for the weaver (cut = the two wrappers' strips).

Cultural note (stated, and load-bearing): kente's named weaves (the proverb-named setts)
carry specific meaning and belong to Akan and Ewe weavers and communities. This cartridge
draws NO kente pattern and names none — it supplies the CLOTH DIMENSIONS and the drape
only; the weave is the weaver's.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # lower|upper|strip|set

hip_girth = float(PARAM(lambda: hip_girth, 1020.0))       # full hip, sets the wrap
lower_length = float(PARAM(lambda: lower_length, 1150.0))  # waist to ankle drop
upper_fraction = float(PARAM(lambda: upper_fraction, 0.62))  # upper cloth vs lower
wrap_overlap = float(PARAM(lambda: wrap_overlap, 380.0))  # tuck-in past the hip
strip_width = float(PARAM(lambda: strip_width, 100.0))    # loom strip width
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
hip_girth = max(760.0, min(hip_girth, 1500.0))
lower_length = max(850.0, min(lower_length, 1450.0))
upper_fraction = max(0.45, min(upper_fraction, 0.85))
wrap_overlap = max(200.0, min(wrap_overlap, 700.0))
strip_width = max(70.0, min(strip_width, 140.0))
hem_allowance = max(8.0, min(hem_allowance, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The strip-assembly solver ────────────────────────────────────────────────
# The lower wrapper must wrap the hip once round plus a real overlap to tuck. Its target
# width is that circuit; the strip count is solved from it and the true width snaps to a
# whole number of strips.
LOWER_TARGET = hip_girth + wrap_overlap
LOWER_STRIPS = max(6, int(round(LOWER_TARGET / strip_width)))
LOWER_WIDTH = LOWER_STRIPS * strip_width
LOWER_EASE = LOWER_WIDTH - hip_girth        # the real tuck-in the woven width gives

# The upper wrapper is a fraction of the lower's width (a smaller cover), also a whole
# number of strips.
UPPER_TARGET = LOWER_WIDTH * upper_fraction
UPPER_STRIPS = max(4, int(round(UPPER_TARGET / strip_width)))
UPPER_WIDTH = UPPER_STRIPS * strip_width
UPPER_LENGTH = lower_length * 0.78          # the upper cloth is shorter


def _wrapper(name, width, length, label):
    """A whole assembled kente wrapper: rectangle width x length, marked with the strip-join
    seams and the wrap turns. Never cut into pieces — that is the point."""
    w, h = width, length
    edges = [
        fc.Edge("hem_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("selvedge_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("hem_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("selvedge_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = []
    strips = int(round(w / strip_width))
    for i in range(1, strips):
        x = strip_width * i
        internals.append(fc.Internal(f"strip join {i}", [fc.P(x, 0.0), fc.P(x, h)],
                                     kind="marking"))
    # wrap guides: the tuck line and the top wound turn.
    internals.append(fc.Internal("waist-tuck line",
                                 [fc.P(0.0, h * 0.92), fc.P(w, h * 0.92)], kind="marking"))
    internals.append(fc.Internal("wrap turn",
                                 [fc.P(0.0, h * 0.5), fc.P(w, h * 0.5)], kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"hem_bottom": hem_allowance, "hem_top": hem_allowance,
                    "selvedge_r": 0.0, "selvedge_l": 0.0},
        notches=[fc.Notch("hem_bottom", 0.5, "centre"),
                 fc.Notch("selvedge_l", 0.92, "waist-tuck point")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1), label=label)


def build_lower():
    return _wrapper("lower", LOWER_WIDTH, lower_length,
                    "Lower wrapper (ntoma) — whole assembled cloth (cut 1, UNCUT)")


def build_upper():
    return _wrapper("upper", UPPER_WIDTH, UPPER_LENGTH,
                    "Upper wrapper / cover-cloth — whole assembled cloth (cut 1, UNCUT)")


def build_strip():
    """One representative loom strip (cut = total strips), for the weaver: a long narrow band
    the width of the loom, marked with a warp-stripe guide."""
    w = strip_width
    h = lower_length
    edges = [
        fc.Edge("start", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("selvedge_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("end", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("selvedge_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("warp-stripe guide", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, h)],
                    kind="marking"),
    ]
    return fc.Piece(
        "strip", edges, seam_allowance=seam_allowance,
        allowances={"start": 0.0, "end": 0.0, "selvedge_r": 0.0, "selvedge_l": 0.0},
        notches=[fc.Notch("start", 0.5, "strip centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=internals, cut=fc.CutSpec(quantity=LOWER_STRIPS + UPPER_STRIPS),
        label="One loom strip (warp-striped) — the weaver's unit")


def build():
    pattern = fc.PatternSet("kente-wrap-cloth")
    everything = target_piece == "set"
    if everything or target_piece == "lower":
        pattern.add(build_lower())
    if everything or target_piece == "upper":
        pattern.add(build_upper())
    if everything or target_piece == "strip":
        pattern.add(build_strip())
    # No sewn seams between the wrappers — they are separate whole cloths. The only seams are
    # the strip joins WITHIN each cloth, which are the weaver's edge-to-edge joins, marked as
    # internals rather than declared piece seams (the cloth is never cut, so there is no
    # pattern-piece seam to verify).

    pattern.bom = [
        {"item": "hand-woven kente strip cloth (Akan/Ewe)",
         "qty": round((LOWER_STRIPS + UPPER_STRIPS) * lower_length / 10.0) * 10,
         "unit": "mm_length",
         "note": f"woven in {strip_width:.0f} mm strips; the lower wrapper is "
                 f"{LOWER_STRIPS} strips ({LOWER_WIDTH:.0f} mm), the upper "
                 f"{UPPER_STRIPS} strips ({UPPER_WIDTH:.0f} mm). Strips are sewn "
                 f"edge-to-edge; the cloth is NEVER cut into pattern pieces."},
        {"item": "hemming thread", "qty": 1, "unit": "spool",
         "note": "top and bottom hems only; the sides are the woven selvedge."},
    ]
    pattern.metadata = {
        "fc500_rank": 484,
        "family": "heritage_global",
        "fabric_hint": "algodon-tejido",
        "finished_mm": {
            "lower_width": round(LOWER_WIDTH, 1),
            "lower_length": round(lower_length, 1),
            "upper_width": round(UPPER_WIDTH, 1),
            "upper_length": round(UPPER_LENGTH, 1),
            "strip_width": round(strip_width, 1),
        },
        "solved": {
            "lower_target_width_mm": round(LOWER_TARGET, 1),
            "lower_strip_count": LOWER_STRIPS,
            "lower_assembled_width_mm": round(LOWER_WIDTH, 1),
            "lower_wrap_ease_mm": round(LOWER_EASE, 1),
            "upper_strip_count": UPPER_STRIPS,
            "upper_assembled_width_mm": round(UPPER_WIDTH, 1),
            "total_strips": LOWER_STRIPS + UPPER_STRIPS,
            "note": "the women's ensemble is TWO whole wrappers, each a whole number of "
                    "loom strips sewn edge-to-edge. The wrapper width is NOT free: it is "
                    "strip_count * strip_width, solved from the target (hip + overlap) and "
                    "snapped to the strip. The cloth is never cut into pattern pieces — "
                    "cutting kente destroys the strip weave, so the wrap is a marked path, "
                    "not a set of pieces.",
        },
        "heritage": {
            "garment": "kente women's two-piece wrapper set (ntoma) — Akan (Asante) & Ewe",
            "construction": "strips woven on the men's double-heddle loom, sewn edge-to-edge "
                            "into whole wrappers; lower wrapper wound from the waist, upper "
                            "wrapper worn over or as a cover-cloth; hemmed top and bottom, "
                            "selvedge at the sides",
            "excluded": "no named kente sett or proverb-weave is drawn or named — those "
                        "carry specific meaning and belong to Akan and Ewe weavers and "
                        "communities; the weave is the weaver's",
        },
        "hardware": "none — the wrappers are wound and tucked, no closure.",
    }
    return pattern


result = build()
