"""
Headwrap — Fashion Cabinet Garment Cartridge (FC-200 #194, accessory gap; global heritage).

The pre-tied headwrap (turban-style): a fitted cap back gathered to a wide band that ties or
knots at the front — the style worn across the African diaspora, and in many cultures for
protection and expression. This cartridge drafts a gathered back cap panel + a long wide front
band, offered with respect for the living traditions it belongs to. The tie styles and the
meanings they carry are the wearer's and are not prescribed here.

Pieces:
  - cap  : gathered back cap panel (cut on fold), gathered to the band.
  - band : a long wide band that wraps the head and ties/knots at the front.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # cap|band|set

head_girth   = float(PARAM(lambda: head_girth, 570.0))
cap_depth    = float(PARAM(lambda: cap_depth, 220.0))
band_width   = float(PARAM(lambda: band_width, 180.0))    # wide wrap band (finished, folds)
band_length  = float(PARAM(lambda: band_length, 1400.0))  # long enough to wrap and tie
cap_gather   = float(PARAM(lambda: cap_gather, 1.5))      # cap width / band attach length
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 15.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(480.0, min(head_girth, 680.0))
cap_depth    = max(160.0, min(cap_depth, 320.0))
band_width   = max(100.0, min(band_width, 320.0))
band_length  = max(900.0, min(band_length, 2200.0))
cap_gather   = max(1.2, min(cap_gather, 2.2))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

CAP_HALF = head_girth * 0.30 * cap_gather              # gathered cap half-width
H = cap_depth


def build_cap():
    internals = [fc.Internal("attach-gather", [fc.P(0.0, H), fc.P(CAP_HALF, H)], kind="marking")]
    return fc.Piece(
        "cap",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("attach", [fc.Line(fc.P(0.0, H), fc.P(CAP_HALF, H))]),
            fc.Edge("side", [fc.curve_through(fc.P(CAP_HALF, H), fc.P(CAP_HALF * 0.8, 0.0),
                                              bulge=0.18, side=-1.0)]),
            fc.Edge("nape", [fc.Line(fc.P(CAP_HALF * 0.8, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"nape": hem_allowance},
        notches=[fc.Notch("attach", 0.5, "centre"), fc.Notch("nape", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(CAP_HALF * 0.4, 20.0), fc.P(CAP_HALF * 0.4, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back cap (gathered)",
    )


def build_band():
    ln = band_length
    h = band_width * 2.0                               # cut double, folds to band_width
    return fc.Piece(
        "band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Wrap band",
    )


def build():
    pattern = fc.PatternSet("headwrap")
    everything = target_piece == "set"
    if everything or target_piece == "cap":
        pattern.add(build_cap())
    if everything or target_piece == "band":
        pattern.add(build_band())

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "cotton, ankara/wax print, or satin-backed knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 76% marker; the print and cloth are the wearer's choice."},
        {"item": "matching thread", "qty": 1, "unit": "spool",
         "note": "gather the cap to the band; the long band ties/knots at the front."},
    ]
    pattern.metadata = {
        "fc200_rank": 194, "family": "accessories", "fabric_hint": "algodon-ankara",
        "heritage_note": "The headwrap is worn across the African diaspora and in many cultures "
            "for protection, faith, and expression. This cartridge drafts a pre-tied cap + band "
            "GEOMETRY only; the tie styles and the meanings they carry are the wearer's and are "
            "not prescribed here. Offered with respect.",
        "silhouette_note": "A gathered back cap seamed to a long wide band that wraps and ties at "
            "the front, so the wrap holds its shape without re-tying each time.",
        "solved": {"cap_half_mm": round(CAP_HALF, 1), "band_length_mm": round(band_length, 1)},
    }
    return pattern


result = build()
