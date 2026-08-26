"""
Aymara pollera skirt — Fashion Cabinet Heritage Cartridge (FC-500 #497, heritage_global;
Aymara, Bolivia & Peru — the cholita's pollera).

The pollera is the full, gathered skirt of the Aymara and Quechua women of the Bolivian and
Peruvian altiplano — the cholita's skirt, worn in layers over the enagua (underskirt) with the
manta shawl and the bowler hat. Its defining quality is FULLNESS: it is many loom widths of
cloth gathered or knife-pleated tightly onto a waistband, and it carries horizontal decorative
tucks (ALFORZAS) near the hem that both ornament it and let it be lengthened. It is a garment
of enormous cloth volume and precise gathering, and it is a marker of Aymara identity and
pride.

Two things the draft solves honestly:

  1. THE FULLNESS IS SOLVED, AND IT IS EXTREME. The skirt panel width is SOLVED from the waist
     times a large gather ratio (typically 3–6×), so the gathered top matches the waistband by
     construction. The pollera's volume is not decoration added on — it is the panel width, and
     the draft reports the true cloth width and the marker length the volume demands.

  2. THE ALFORZAS ARE HORIZONTAL TUCKS NEAR THE HEM, AND THEY EAT LENGTH. The decorative tucks
     each take up twice their depth in cloth, so the cut length must include the tuck take-up or
     the finished skirt is short. The draft adds the tuck take-up to the cut length and reports
     both the finished and the cut length.

Pieces:
  - skirt : the very full gathered skirt panel (one length, seamed into a tube in make-up).
  - band  : the waistband the panel gathers onto.

Hardware: none — the pollera fastens with ties or a hook at the band; drafted as a tie band.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # skirt|band|set

waist_girth = float(PARAM(lambda: waist_girth, 780.0))
finished_length = float(PARAM(lambda: finished_length, 620.0))  # waist to hem, finished
gather_ratio = float(PARAM(lambda: gather_ratio, 4.5))    # panel width / waist (extreme)
band_height = float(PARAM(lambda: band_height, 40.0))
alforza_count = int(PARAM(lambda: alforza_count, 4))      # horizontal tucks near the hem
alforza_depth = float(PARAM(lambda: alforza_depth, 18.0))  # each tuck depth
hem_band_depth = float(PARAM(lambda: hem_band_depth, 90.0))  # contrast hem band zone
tie_length = float(PARAM(lambda: tie_length, 700.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(620.0, min(waist_girth, 1150.0))
finished_length = max(480.0, min(finished_length, 900.0))
gather_ratio = max(2.5, min(gather_ratio, 6.5))
band_height = max(28.0, min(band_height, 70.0))
alforza_count = max(0, min(alforza_count, 8))
alforza_depth = max(8.0, min(alforza_depth, 35.0))
hem_band_depth = max(40.0, min(hem_band_depth, 180.0))
tie_length = max(500.0, min(tie_length, 1100.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

# ── The fullness + tuck solve ────────────────────────────────────────────────
BAND_LEN = waist_girth + 40.0             # the waistband, with a small overlap
PANEL_WIDTH = BAND_LEN * gather_ratio     # SOLVED — the extreme fullness IS the panel width
# Each alforza tuck eats twice its depth in cloth. The cut length must include the tuck take-up
# plus the hem allowance, or the finished skirt is short.
TUCK_TAKEUP = alforza_count * alforza_depth * 2.0
CUT_LENGTH = finished_length + TUCK_TAKEUP + hem_allowance


def build_skirt():
    """The very full gathered skirt panel: a rectangle PANEL_WIDTH x CUT_LENGTH, its top
    gathered onto the band, with the alforza tucks and the hem band marked."""
    w = PANEL_WIDTH
    h = CUT_LENGTH
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("hem", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),   # the two sides seam into a tube
        fc.Edge("top", [fc.Line(p2, p3)]),      # gathered onto the band
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("gather-line", [fc.P(0.0, h - 14.0), fc.P(w, h - 14.0)], kind="marking"),
        fc.Internal("hem-band", [fc.P(0.0, hem_allowance + hem_band_depth),
                                 fc.P(w, hem_allowance + hem_band_depth)], kind="marking"),
    ]
    # the alforza tucks: horizontal lines near the hem, above the hem band.
    base = hem_allowance + hem_band_depth + 40.0
    for i in range(alforza_count):
        y = base + i * (alforza_depth * 2.0 + 12.0)
        internals.append(fc.Internal(f"alforza-{i + 1}", [fc.P(0.0, y), fc.P(w, y)],
                                     kind="marking"))
    return fc.Piece(
        "skirt", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 0.0},
        notches=[fc.Notch("top", 0.25, "quarter"),
                 fc.Notch("top", 0.5, "half"),
                 fc.Notch("top", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(w * 0.5, hem_allowance + 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Full gathered skirt panel (alforzas + hem band)",
    )


def build_band():
    """The waistband the pollera panel gathers onto; ties extend from its ends."""
    ln = BAND_LEN
    h = band_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("gathered_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("gathered_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, band_height + 2.0),
                                        fc.P(ln, band_height + 2.0)], kind="marking"),
                   fc.Internal("tie-exit", [fc.P(ln, h * 0.5),
                                            fc.P(ln + tie_length * 0.15, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Waistband (ties at the ends)",
    )


def build():
    pattern = fc.PatternSet("aymara-pollera-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "skirt":
        pattern.add(build_skirt())
    if everything or target_piece == "band":
        pattern.add(build_band())
    # No equal-length seam between skirt and band: the skirt top gathers onto the band (an
    # intentionally unequal gather). The gather ratio is the design and is reported.

    pattern.bom = [
        {"item": "pollera cloth (bayeta wool, velvet, or aguayo)", "qty": round(
            PANEL_WIDTH * CUT_LENGTH / 1000.0), "unit": "cm2",
         "note": f"the panel is {PANEL_WIDTH:.0f} mm wide (a gather ratio of "
                 f"{gather_ratio:.1f}) and {CUT_LENGTH:.0f} mm long (including "
                 f"{TUCK_TAKEUP:.0f} mm of alforza tuck take-up). The fullness IS the cloth "
                 f"volume — a pollera is several metres of cloth round the waist."},
        {"item": "waistband + ties", "qty": round(BAND_LEN + tie_length * 2.0),
         "unit": "mm_length", "note": "the band with ties at both ends."},
        {"item": "hem-band / alforza contrast cloth", "qty": round(PANEL_WIDTH),
         "unit": "mm_length",
         "note": f"{alforza_count} alforza tucks and a {hem_band_depth:.0f} mm hem band; the "
                 f"tucks also let the pollera be lengthened later."},
    ]
    pattern.metadata = {
        "fc500_rank": 497,
        "family": "heritage_global",
        "fabric_hint": "lana-tejida",
        "finished_mm": {
            "waist_girth": round(waist_girth, 1),
            "finished_length": round(finished_length, 1),
            "cut_length": round(CUT_LENGTH, 1),
            "panel_width": round(PANEL_WIDTH, 1),
        },
        "solved": {
            "band_length_mm": round(BAND_LEN, 2),
            "panel_width_mm": round(PANEL_WIDTH, 2),
            "gather_ratio": round(gather_ratio, 2),
            "alforza_count": alforza_count,
            "alforza_takeup_mm": round(TUCK_TAKEUP, 2),
            "cut_length_mm": round(CUT_LENGTH, 2),
            "finished_length_mm": round(finished_length, 2),
            "note": "the pollera's FULLNESS is solved, not decorative: the panel width is the "
                    "waist times a large gather ratio (2.5–6.5×), so the gathered top matches "
                    "the band by construction and the true cloth volume is reported. The "
                    "ALFORZA tucks near the hem each eat twice their depth in cloth, so the cut "
                    "length includes alforza_takeup_mm — cut to the finished length instead and "
                    "the skirt comes up short. The tucks also let the pollera be lengthened.",
        },
        "heritage": {
            "garment": "pollera — the full gathered skirt of the Aymara and Quechua cholita",
            "worn": "in layers over the enagua underskirt, with the manta shawl and the bowler "
                    "hat; a marker of Aymara identity in Bolivia and Peru",
            "construction": "several loom widths gathered or knife-pleated onto a waistband, "
                            "with horizontal alforza tucks and a contrast hem band",
            "excluded": "no specific aguayo pattern, embroidery, or trim colourway is drawn — "
                        "those are the maker's and the region's",
        },
        "hardware": "none — the pollera fastens with ties or a hook at the band; drafted with "
                    "ties.",
    }
    return pattern


result = build()
