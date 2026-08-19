"""
Scrub Cap — Fashion Cabinet Garment Cartridge (FC-200 #193, accessory gap).

The surgical scrub cap (tie-back): a domed cap that covers the hair, gathered at the back over a
band and tied, worn in operating rooms and kitchens. This cartridge drafts the classic tie-back
scrub cap as a single domed panel (cut on fold) whose front band edge sits at the brow and whose
back is gathered to a bound edge with ties. Distinct from FC-100's structured caps and the knit
beanie — the scrub cap is a woven, gathered, tie-back cap.

Pieces:
  - cap  : the domed cap panel (cut on fold at CB), front brow band + gathered tie-back.
  - tie  : a self-fabric tie strip (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # cap|tie|set

head_girth   = float(PARAM(lambda: head_girth, 580.0))
cap_depth    = float(PARAM(lambda: cap_depth, 240.0))     # brow to crown depth
brow_band    = float(PARAM(lambda: brow_band, 40.0))      # front brow band height
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(480.0, min(head_girth, 680.0))
cap_depth    = max(180.0, min(cap_depth, 340.0))
brow_band    = max(20.0, min(brow_band, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 40.0))

# the cap front spans about 60% of the head girth (brow to ear to ear over the top on fold)
FRONT_HALF = head_girth * 0.30
BACK_HALF = head_girth * 0.42                          # back is wider, gathered to a bound edge
H = cap_depth


def build_cap():
    # domed panel: straight brow (front), curved crown up and over, gathered back edge.
    internals = [fc.Internal("brow-band",
                             [fc.P(0.0, H - brow_band), fc.P(FRONT_HALF, H - brow_band)],
                             kind="marking"),
                 fc.Internal("back-gather", [fc.P(0.0, 0.0), fc.P(BACK_HALF, 0.0)], kind="marking")]
    return fc.Piece(
        "cap",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("brow", [fc.Line(fc.P(0.0, H), fc.P(FRONT_HALF, H))]),
            # side/crown curves from the brow corner down and out to the wider back corner
            fc.Edge("side", [fc.curve_through(fc.P(FRONT_HALF, H), fc.P(BACK_HALF, 0.0),
                                              bulge=0.25, side=-1.0)]),
            fc.Edge("back", [fc.Line(fc.P(BACK_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"brow": hem_allowance, "back": hem_allowance},
        notches=[fc.Notch("brow", 0.5, "centre front"), fc.Notch("back", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(FRONT_HALF * 0.5, 20.0), fc.P(FRONT_HALF * 0.5, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Cap dome",
    )


def build_tie():
    ln = 420.0
    w = 30.0
    return fc.Piece(
        "tie",
        [
            fc.Edge("long_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("long_b", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Tie",
    )


def build():
    pattern = fc.PatternSet("scrub-cap")
    everything = target_piece == "set"
    if everything or target_piece == "cap":
        pattern.add(build_cap())
    if everything or target_piece == "tie":
        pattern.add(build_tie())

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "quilting cotton or poly-cotton",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 72% marker; washable, breathable cap fabric."},
        {"item": "self-fabric ties", "qty": 2, "unit": "strips",
         "note": "the back gathers to a bound edge; the ties knot at the nape."},
        {"item": "bias binding + all-purpose thread", "qty": 1, "unit": "set",
         "note": "bind the gathered back edge; a sweatband at the brow is optional."},
    ]
    pattern.metadata = {
        "fc200_rank": 193, "family": "accessories", "fabric_hint": "algodon-quilting",
        "silhouette_note": "A classic tie-back surgical/kitchen cap: a domed panel with a brow "
            "band at the front and a gathered, bound, tie-back at the nape. Woven and gathered, "
            "distinct from the knit beanie.",
        "solved": {"front_half_mm": round(FRONT_HALF, 1), "back_half_mm": round(BACK_HALF, 1)},
    }
    return pattern


result = build()
