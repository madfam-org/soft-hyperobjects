"""
Sarape / Poncho — Fashion Cabinet Garment Cartridge (FC-200 rank #138, MX heritage).

The sarape (and the poncho it is kin to) is a single rectangular woven blanket-garment
worn over the head through a central neck slit — one of the most recognizable garments of
Mexico. Its construction is the simplest possible: ONE rectangle, a slit for the head,
finished edges (often fringed). The artistry is entirely in the weave — the bands, the
diamond (ojo), the colour gradients — which the maker supplies.

This cartridge drafts the garment geometry: one rectangle sized to the wearer's span and
length, with a centred neck slit (and an optional short perpendicular cut for the head),
plus a marked fringe allowance at the ends. Offered with respect for the living tradition.

Pieces:
  - body : one rectangle (worn folded over the shoulders), cut on the fold at the
           shoulder line, with the neck slit on the fold.

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
span_width   = float(PARAM(lambda: span_width, 1200.0))   # width across the body (span + drape)
drop_length  = float(PARAM(lambda: drop_length, 700.0))   # drop from the shoulder fold
neck_slit    = float(PARAM(lambda: neck_slit, 300.0))     # head-slit length along the fold
head_cut     = float(PARAM(lambda: head_cut, 0.0))        # optional perpendicular head cut (mm)
fringe       = float(PARAM(lambda: fringe, 60.0))         # marked fringe allowance at the ends
band_count   = int(  PARAM(lambda: band_count, 5))        # marked weave bands (decorative)

# ── Clamps ───────────────────────────────────────────────────────────────────
span_width  = max(700.0, min(span_width, 1800.0))
drop_length = max(350.0, min(drop_length, 1000.0))
neck_slit   = max(200.0, min(neck_slit, min(span_width * 0.6, 500.0)))
head_cut    = max(0.0, min(head_cut, 200.0))
fringe      = max(0.0, min(fringe, 150.0))
band_count  = max(0, min(band_count, 20))

# The garment is worn folded at the shoulder line: total flat length = 2 * drop.
# We draft the FLAT rectangle (cut on the shoulder fold), so the piece is span_width
# wide and drop_length tall, cut on fold + mirror to make the full 2*drop length.
W = span_width
Hd = drop_length
SLIT_HALF = neck_slit / 2.0


def build_body():
    # The shoulder fold is the TOP edge (y = Hd). The neck slit sits centred on that
    # fold. We represent the slit as an internal marking on the fold plus (optionally) a
    # short perpendicular head cut marked down from the fold centre.
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, Hd))]),
        fc.Edge("fold", [fc.Line(fc.P(0.0, Hd), fc.P(W, Hd))]),     # shoulder fold (cut on fold)
        fc.Edge("right", [fc.Line(fc.P(W, Hd), fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),    # fringed end
    ]
    internals = [
        # The head slit, centred on the shoulder fold.
        fc.Internal("neck-slit",
                    [fc.P(W / 2.0 - SLIT_HALF, Hd), fc.P(W / 2.0 + SLIT_HALF, Hd)], kind="drill"),
    ]
    if head_cut > 0.0:
        internals.append(fc.Internal(
            "head-cut", [fc.P(W / 2.0, Hd), fc.P(W / 2.0, Hd - head_cut)], kind="drill"))
    if fringe > 0.0:
        internals.append(fc.Internal("fringe-line",
                                     [fc.P(0.0, fringe), fc.P(W, fringe)], kind="marking"))
    for i in range(1, band_count + 1):
        y = Hd * i / (band_count + 1)
        internals.append(fc.Internal(f"weave-band-{i}",
                                     [fc.P(0.0, y), fc.P(W, y)], kind="marking"))

    return fc.Piece(
        "body",
        edges,
        seam_allowance=0.0,   # edge-finished / fringed all round — no sewn seam
        notches=[fc.Notch("fold", 0.5, "centre neck")],
        grainline=fc.Grainline(fc.P(W * 0.5, Hd * 0.15), fc.P(W * 0.5, Hd * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fold", mirror=True),
        label="Sarape Body",
    )


def build():
    pattern = fc.PatternSet("sarape-poncho")
    pattern.add(build_body())
    fabric_width = 1400.0
    total_area = build_body().area() * 2.0             # cut on fold → 2× the drafted half
    marker_len = total_area / (fabric_width * 0.85)
    pattern.bom = [
        {"item": "woven blanket cloth (wool or cotton)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width; traditionally woven as one web on a treadle or "
                 "backstrap loom, fringed at the ends — no cutting into panels."},
        {"item": "weave design", "qty": 1, "unit": "as woven",
         "note": "the bands, ojo (diamond), and colour work are the weaver's; marked here only."},
    ]
    pattern.metadata = {
        "fc200_rank": 138,
        "family": "heritage_global",
        "fabric_hint": "lana-melton-abrigo",
        "heritage_note": "The sarape is a living Mexican woven garment. This cartridge "
            "drafts the one-rectangle GARMENT GEOMETRY and the head slit only — the weave "
            "(bands, diamond/ojo, colour gradients) that carries the sarape's identity is "
            "the weaver's to supply and is not reproduced here. Offered with respect.",
        "single_rectangle": "The whole garment is one rectangle worn folded at the "
            "shoulders through a central neck slit; finished (often fringed) all round, "
            "with no sewn seam — the simplest and most economical of garments.",
        "drafting": "one span_width x drop_length rectangle cut on the shoulder fold; "
            "centred neck slit on the fold; optional short head cut; fringe + weave bands "
            "marked for the maker.",
    }
    return pattern


result = build()
