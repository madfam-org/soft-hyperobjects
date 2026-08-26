"""
Dirndl apron overlay (Dirndlschürze) — Fashion Cabinet Heritage Cartridge
(FC-500 #499, heritage_global; Alpine — Bavaria, Austria, Tyrol).

The dirndl apron (Schürze) is the front overlay worn over the dirndl dress across the Alpine
regions of Bavaria, Austria, South Tyrol and beyond: a rectangular panel of cloth, gathered
onto a waistband, tied at the waist with long ties whose BOW carries a social message (worn on
the left = single/available, right = taken/married, centre-front = a child or a waitress, back
= a widow). This cartridge drafts the apron only — the overlay, its waistband and its ties —
not the dirndl dress beneath it (that is drafted separately in the commons).

Two things the draft solves honestly:

  1. THE APRON IS GATHERED, AND THE GATHER IS SOLVED. The apron panel is wider than the
     waistband, and it is gathered onto it; the panel width is SOLVED from the waistband length
     times the gather ratio, so the gathered edge and the waistband match by construction rather
     than by drafting the panel to a free width and hoping.

  2. THE BOW SIDE IS A CHOICE, AND IT IS MARKED. The apron carries the tie exit and a marked
     bow-position guide (left / right / centre / back) so the maker and wearer know the socially
     meaningful placement — recorded as information, drawn as a marking, never imposed.

Pieces:
  - apron : the gathered apron panel.
  - band  : the waistband the panel gathers onto.
  - tie   : one waist tie (cut 2).

Hardware: none — the apron ties; there is no hardware closure.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # apron|band|tie|set

waist_girth = float(PARAM(lambda: waist_girth, 720.0))
apron_span = float(PARAM(lambda: apron_span, 0.72))       # apron band / waist (front coverage)
apron_length = float(PARAM(lambda: apron_length, 560.0))  # waist to hem
gather_ratio = float(PARAM(lambda: gather_ratio, 1.8))    # panel width / band
band_height = float(PARAM(lambda: band_height, 30.0))
tie_length = float(PARAM(lambda: tie_length, 900.0))      # one tie
tie_width = float(PARAM(lambda: tie_width, 70.0))
bow_side = float(PARAM(lambda: bow_side, 0.0))            # -1 left, 0 centre-ish, +1 right (marker)
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1080.0))
apron_span = max(0.5, min(apron_span, 0.95))
apron_length = max(380.0, min(apron_length, 780.0))
gather_ratio = max(1.3, min(gather_ratio, 2.8))
band_height = max(20.0, min(band_height, 55.0))
tie_length = max(600.0, min(tie_length, 1400.0))
tie_width = max(40.0, min(tie_width, 110.0))
bow_side = max(-1.0, min(bow_side, 1.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# ── The gather solve — the panel from the band ───────────────────────────────
BAND_LEN = waist_girth * apron_span         # the apron waistband covers the front
PANEL_WIDTH = BAND_LEN * gather_ratio       # SOLVED so the gathered edge matches the band
BOW_LABEL = ("left (single)" if bow_side < -0.34 else
             "right (taken)" if bow_side > 0.34 else "centre (child/server)")


def build_apron():
    """The gathered apron panel: a rectangle PANEL_WIDTH x apron_length, its top gathered onto
    the band (the gather is a marking; the top edge length is the full panel width)."""
    w = PANEL_WIDTH
    h = apron_length
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("hem", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),          # gathered onto the band
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    # the bow-position marker: where the tie/bow sits along the top.
    bow_x = w * (0.5 + bow_side * 0.32)
    internals = [
        fc.Internal("gather-line", [fc.P(0.0, h - 12.0), fc.P(w, h - 12.0)], kind="marking"),
        fc.Internal("bow-position", [fc.P(bow_x, h), fc.P(bow_x, h - 40.0)], kind="marking"),
        fc.Internal("hem-band", [fc.P(0.0, hem_allowance + 20.0),
                                 fc.P(w, hem_allowance + 20.0)], kind="marking"),
    ]
    return fc.Piece(
        "apron", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 0.0},
        notches=[fc.Notch("top", 0.5, "centre front"),
                 fc.Notch("top", 0.25, "quarter"),
                 fc.Notch("top", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(w * 0.5, hem_allowance + 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Gathered apron panel",
    )


def build_band():
    """The waistband the apron panel gathers onto; the ties extend from its ends."""
    ln = BAND_LEN
    h = band_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("gathered_edge", [fc.Line(p0, p1)]),   # the apron top gathers to this
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("gathered_edge", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, band_height + 2.0),
                                        fc.P(ln, band_height + 2.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Apron waistband",
    )


def build_tie():
    """One waist tie (cut 2): a long strip that ties into the socially meaningful bow."""
    ln = tie_length
    w = tie_width
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, w)
    p3 = fc.P(0.0, w)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("end", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("attach", [fc.Line(p3, p0)]),     # sewn to the band end (short edge)
    ]
    return fc.Piece(
        "tie", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "band join")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Waist tie (into the bow)",
    )


def build():
    pattern = fc.PatternSet("folk-dirndl-apron")
    everything = target_piece == "set"
    if everything or target_piece == "apron":
        pattern.add(build_apron())
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything or target_piece == "tie":
        pattern.add(build_tie())
    # The apron top gathers onto the band: the top edge is PANEL_WIDTH and the band is BAND_LEN,
    # and the gather ratio between them is the design. There is no equal-length seam to declare
    # (a gather is intentionally unequal); the gather ratio is reported instead.

    pattern.bom = [
        {"item": "apron cloth (cotton, silk, or printed dirndl fabric)", "qty": round(
            (apron_length + hem_allowance) * 1.2 / 10.0) * 10, "unit": "mm_length",
         "note": f"the panel is {PANEL_WIDTH:.0f} mm wide, gathered onto a {BAND_LEN:.0f} mm "
                 f"band — a gather ratio of {gather_ratio:.2f}."},
        {"item": "waist ties", "qty": 2, "unit": "count",
         "note": f"{tie_length:.0f} mm each; the bow is worn {BOW_LABEL} — a socially "
                 f"meaningful placement, marked, never imposed."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 499,
        "family": "heritage_global",
        "fabric_hint": "algodon-percal",
        "finished_mm": {
            "band_length": round(BAND_LEN, 1),
            "panel_width": round(PANEL_WIDTH, 1),
            "apron_length": round(apron_length, 1),
            "tie_length": round(tie_length, 1),
        },
        "solved": {
            "band_length_mm": round(BAND_LEN, 2),
            "panel_width_mm": round(PANEL_WIDTH, 2),
            "gather_ratio": round(gather_ratio, 3),
            "bow_side": round(bow_side, 2),
            "bow_placement": BOW_LABEL,
            "note": "the apron panel width is SOLVED from the band length times the gather "
                    "ratio, so the gathered top matches the band by construction rather than "
                    "by drafting the panel to a free width. The bow side is recorded and "
                    "MARKED (left = single, right = taken, centre = child/server), never "
                    "imposed — the meaning is the wearer's to signal.",
        },
        "heritage": {
            "garment": "Dirndlschürze — the Alpine dirndl apron overlay",
            "worn": "over the dirndl dress across Bavaria, Austria, South Tyrol and beyond; "
                    "the apron only — the dirndl dress is drafted separately",
            "bow_meaning": "left = single/available, right = taken/married, centre-front = a "
                           "child or a server, back = a widow (a living convention, marked "
                           "here as information)",
            "excluded": "no specific printed dirndl fabric or regional trim is drawn — the "
                        "cloth is the maker's",
        },
        "hardware": "none — the apron ties; there is no hardware closure.",
    }
    return pattern


result = build()
