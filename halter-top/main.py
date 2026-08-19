"""
Halter Top — Fashion Cabinet Garment Cartridge (FC-200 #162, everyday silhouette gap).

A halter top: a shaped front bodice that rises to a neck strap tied behind the neck, with an
open upper back and bare shoulders; a small back band wraps the body and closes at centre
back. The front and back share the structural underbust/side width so the side seams balance
by construction. The neck strap is a self-fabric tie (a marked, cut-separately strip in the
BOM); the front's rise to the strap is a shaped centre.

Pieces:
  - front : shaped halter front rising to a centre neck-strap point (cut on fold).
  - back  : low back band that wraps to CB (cut on fold), ties/hooks at CB.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|set

bust_girth   = float(PARAM(lambda: bust_girth, 900.0))     # full bust
underbust    = float(PARAM(lambda: underbust, 760.0))      # under-bust / body band girth
front_len    = float(PARAM(lambda: front_len, 360.0))      # underbust to neck-strap point
back_height  = float(PARAM(lambda: back_height, 180.0))    # low back band height
strap_width  = float(PARAM(lambda: strap_width, 40.0))     # neck-strap width
ease         = float(PARAM(lambda: ease, 40.0))            # close fit
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 18.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(650.0, min(bust_girth, 1400.0))
underbust    = max(560.0, min(underbust, 1200.0))
front_len    = max(240.0, min(front_len, 500.0))
back_height  = max(100.0, min(back_height, 320.0))
strap_width  = max(20.0, min(strap_width, 90.0))
ease         = max(0.0, min(ease, 160.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

# Underbust band quarter is the shared width both front & back side seams use.
BAND_HALF = (underbust + ease) / 2.0 / 2.0
BUST_HALF = (bust_girth + ease) / 2.0 / 2.0
STRAP_HALF = strap_width / 2.0


def build_front():
    # Shaped front: side seam is a straight vertical of height front_len at x=BAND_HALF so it
    # balances the back band's side. The neckline sweeps from the side up-and-in to the centre
    # neck-strap point at the top.
    top_y = front_len
    strap_pt = fc.P(STRAP_HALF, top_y)                 # where the neck strap attaches (near CF)
    side_top = fc.P(BAND_HALF, top_y - 120.0)          # armhole/side top
    internals = [fc.Internal("bust-shape",
                             [fc.P(0.0, top_y - 60.0), fc.P(BUST_HALF * 0.6, top_y - 140.0)],
                             kind="marking")]
    return fc.Piece(
        "front",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("neck", [fc.Line(fc.P(0.0, top_y), strap_pt)]),
            # armhole edge: from strap point out and down to the side top (bare shoulder)
            fc.Edge("armhole", [fc.curve_through(strap_pt, side_top, bulge=0.20, side=-1.0)]),
            fc.Edge("side", [fc.Line(side_top, fc.P(BAND_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BAND_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.0, "underarm"), fc.Notch("neck", 1.0, "strap")],
        grainline=fc.Grainline(fc.P(BAND_HALF * 0.5, 30.0), fc.P(BAND_HALF * 0.5, top_y - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Front (halter)",
    )


def build_back():
    # Low back band: side seam is a straight vertical of height... to balance the front side
    # (front side length = front_len - 120). Match that exactly.
    side_h = front_len - 120.0
    top_y = side_h
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, top_y), fc.P(BAND_HALF, top_y))]),
            fc.Edge("side", [fc.Line(fc.P(BAND_HALF, top_y), fc.P(BAND_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BAND_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.0, "underarm"), fc.Notch("center", 1.0, "CB closure")],
        grainline=fc.Grainline(fc.P(BAND_HALF * 0.5, 20.0), fc.P(BAND_HALF * 0.5, top_y - 20.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back band",
    )


def build():
    pattern = fc.PatternSet("halter-top")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "woven or firm knit (cotton / linen / sateen)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; a firm hand supports the halter front."},
        {"item": "neck strap (self fabric)", "qty": 1, "unit": "strip",
         "note": "cut a self-fabric strip to tie behind the neck; length is the maker's."},
        {"item": "back closure (ties or hook-and-bar)", "qty": 1, "unit": "set",
         "note": "the back band closes at centre back."},
        {"item": "lightweight boning (optional)", "qty": 1, "unit": "as chosen",
         "note": "optional at the front side seams for extra support."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + hems."},
    ]
    pattern.metadata = {
        "fc200_rank": 162, "family": "woven_tops", "fabric_hint": "algodon-firme",
        "silhouette_note": "A shaped halter front rises to a self-fabric neck strap tied behind "
            "the neck, with bare shoulders and an open upper back; a low back band wraps to CB. "
            "Front and back share the band-girth side seam, so the sides balance.",
        "solved": {"band_quarter_mm": round(BAND_HALF, 1), "front_len_mm": round(front_len, 1),
                   "back_height_mm": round(back_height, 1)},
    }
    return pattern


result = build()
