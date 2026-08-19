"""
Dhoti — Fashion Cabinet Garment Cartridge (FC-200 rank #156, South Asian heritage).

The dhoti is the unstitched draped lower garment of South Asia: a single long rectangular
length of cloth wrapped around the waist and legs and knotted, worn across many regions
under many names (dhoti, veshti, mundu, panche). It is traditionally UNSTITCHED — the
garment is the drape, not a sewn seam. This cartridge therefore drafts the CLOTH itself: a
single rectangle at the customary proportions, with the border bands and the fold/knot
reference lines marked so a maker can cut and finish a length to size. The regional drape
styles and border meaning are the wearer's and are not reproduced here. Offered with respect.

Pieces:
  - length : one rectangular length of cloth (finished, hemmed), borders + drape marks.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # length|set

cloth_length = float(PARAM(lambda: cloth_length, 4500.0))  # full drape length (customary ~4.5 m)
cloth_width  = float(PARAM(lambda: cloth_width, 1180.0))   # loom width (waist to ankle in drape)
border_band  = float(PARAM(lambda: border_band, 60.0))     # marked woven border along the length
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
cloth_length = max(3000.0, min(cloth_length, 5500.0))
cloth_width  = max(1000.0, min(cloth_width, 1300.0))
border_band  = max(0.0, min(border_band, 200.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

Lx = cloth_length
Wy = cloth_width


def build_length():
    internals = []
    if border_band > 0.0:
        # woven borders run along both long edges (the selvedge decoration)
        internals.append(fc.Internal("border-lower", [fc.P(0.0, border_band),
                                                       fc.P(Lx, border_band)], kind="marking"))
        internals.append(fc.Internal("border-upper", [fc.P(0.0, Wy - border_band),
                                                       fc.P(Lx, Wy - border_band)], kind="marking"))
    # drape reference: centre (first waist wrap) and the pleat-fan origin
    internals.append(fc.Internal("centre-wrap", [fc.P(Lx / 2.0, 0.0), fc.P(Lx / 2.0, Wy)],
                                 kind="marking"))
    internals.append(fc.Internal("knot-ref", [fc.P(Lx * 0.5 - 120.0, Wy * 0.5),
                                              fc.P(Lx * 0.5 + 120.0, Wy * 0.5)], kind="marking"))
    return fc.Piece(
        "length",
        [
            fc.Edge("start", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, Wy))]),
            fc.Edge("selvedge_top", [fc.Line(fc.P(0.0, Wy), fc.P(Lx, Wy))]),
            fc.Edge("end", [fc.Line(fc.P(Lx, Wy), fc.P(Lx, 0.0))]),
            fc.Edge("selvedge_bottom", [fc.Line(fc.P(Lx, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        allowances={"start": hem_allowance, "end": hem_allowance},
        notches=[fc.Notch("selvedge_bottom", 0.5, "centre wrap")],
        grainline=fc.Grainline(fc.P(120.0, Wy / 2.0), fc.P(Lx - 120.0, Wy / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Dhoti length",
    )


def build():
    pattern = fc.PatternSet("dhoti")
    pattern.add(build_length())
    pattern.bom = [
        {"item": "fine cotton or silk length (unstitched cloth)",
         "qty": round(Lx / 10.0) * 10, "unit": "mm_length",
         "note": "a single length at loom width; the dhoti is DRAPED, not sewn — only the "
                 "two cut ends are hemmed."},
        {"item": "woven border (selvedge)", "qty": 1, "unit": "as woven",
         "note": "borders are woven into the cloth; marked here, supplied by the weaver/maker."},
        {"item": "matching thread", "qty": 1, "unit": "spool", "note": "narrow end hems only."},
    ]
    pattern.metadata = {
        "fc200_rank": 156,
        "family": "heritage_global",
        "fabric_hint": "algodon-fino",
        "heritage_note": "The dhoti (also veshti, mundu, panche across regions) is a living, "
            "traditionally UNSTITCHED draped garment of South Asia. This cartridge drafts the "
            "CLOTH itself — a length at customary proportions with borders and a wrap reference "
            "marked — not a sewn garment; the regional drape styles and border meaning are the "
            "wearer's and are not reproduced here. Offered with respect.",
        "construction": "no seams: a single hemmed rectangular length, draped and knotted at "
            "the waist. The 'pattern' is the cloth's finished size and its reference marks.",
        "solved": {"cloth_length_mm": round(Lx, 1), "cloth_width_mm": round(Wy, 1),
                   "unstitched": True},
    }
    return pattern


result = build()
