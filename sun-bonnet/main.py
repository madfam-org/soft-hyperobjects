"""
Sun Bonnet — Fashion Cabinet Garment Cartridge (FC-300 #217, Lane 2).

The working sun bonnet: a stiffened front BRIM, a gathered CAUL that covers the head,
a NECK CURTAIN that shades the nape and shoulders, and self-fabric TIES under the chin.
A pure soft-goods garment — no hardware.

Pieces:
  - brim         : the stiffened shading brim, cut on fold + mirrored (cut 2 + interlining).
  - caul         : the head-covering crown, gathered onto the brim, cut on fold + mirrored.
  - neck-curtain : the nape shade, gathered onto the caul's back, cut on fold + mirrored.
  - tie          : the chin tie, cut 2.

Drafting notes — both gathers are declared as REAL seams with ease equal to the
fullness removed, so the checks are substantive: the caul is cut `caul_gather` times
the brim's head run, and the curtain `curtain_gather` times the caul's back run. The
on-fold pieces are declared against their mates with the folded edge listed twice
(the piece against its own mirror, join-to-join, never join-to-fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # brim|caul|curtain|tie|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
neck_girth = float(PARAM(lambda: neck_girth, 360.0))
brim_depth = float(PARAM(lambda: brim_depth, 110.0))
caul_depth = float(PARAM(lambda: caul_depth, 190.0))
curtain_drop = float(PARAM(lambda: curtain_drop, 130.0))
caul_gather = float(PARAM(lambda: caul_gather, 1.7))
curtain_gather = float(PARAM(lambda: curtain_gather, 1.4))
tie_length = float(PARAM(lambda: tie_length, 420.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
neck_girth = max(280.0, min(neck_girth, 460.0))
brim_depth = max(50.0, min(brim_depth, 200.0))
caul_depth = max(110.0, min(caul_depth, 300.0))
curtain_drop = max(50.0, min(curtain_drop, 260.0))
caul_gather = max(1.1, min(caul_gather, 2.6))
curtain_gather = max(1.0, min(curtain_gather, 2.2))
tie_length = max(220.0, min(tie_length, 700.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The brim spans the FRONT of the head, ear to ear over the forehead: ~55% of the girth.
BRIM_RUN = head_girth * 0.55          # the brim's head edge, full run
BRIM_HALF = BRIM_RUN / 2.0            # drafted on the fold at centre front

# The caul is cut full and gathered onto that same head run.
CAUL_FLAT_HALF = (BRIM_RUN * caul_gather) / 2.0
CAUL_TAKEN = BRIM_RUN * (caul_gather - 1.0)

# The caul's back edge takes the neck curtain, gathered in turn.
CAUL_BACK = head_girth * 0.42         # the caul's nape run, full
CAUL_BACK_HALF = CAUL_BACK / 2.0
CURTAIN_FLAT_HALF = (CAUL_BACK * curtain_gather) / 2.0
CURTAIN_TAKEN = CAUL_BACK * (curtain_gather - 1.0)


def _build_brim():
    """The stiffened shading brim, drafted on the fold at centre front: a curved
    outer edge sweeping forward, a straight head edge that takes the gathered caul."""
    hw, d = BRIM_HALF, brim_depth
    edges = [
        fc.Edge("centre_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, d))]),
        fc.Edge("outer", [fc.curve_through(fc.P(0.0, d), fc.P(hw, 0.0),
                                           bulge=0.22, side=-1.0)]),
        fc.Edge("head_edge", [fc.Line(fc.P(hw, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("cording", [fc.P(0.0, d * 0.45), fc.P(hw * 0.72, d * 0.28)],
                    kind="marking"),
    ]
    return fc.Piece(
        "brim",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("head_edge", 0.5, "brim quarter")],
        grainline=fc.Grainline(fc.P(hw * 0.4, d * 0.15), fc.P(hw * 0.4, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_front", mirror=True),
        label="Brim",
    )


def _build_caul():
    """The head-covering crown, cut full and gathered onto the brim's head edge; its
    back edge in turn takes the gathered neck curtain."""
    hw, d = CAUL_FLAT_HALF, caul_depth
    back_half = CAUL_BACK_HALF
    edges = [
        fc.Edge("centre_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, d))]),
        fc.Edge("front_edge", [fc.Line(fc.P(0.0, d), fc.P(hw, d))]),   # gathers to the brim
        fc.Edge("side", [fc.curve_through(fc.P(hw, d), fc.P(back_half, 0.0),
                                          bulge=0.16, side=-1.0)]),
        fc.Edge("back_edge", [fc.Line(fc.P(back_half, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("gather_front", [fc.P(0.0, d - 10.0), fc.P(hw, d - 10.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "caul",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "gather midpoint"),
                 fc.Notch("back_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(hw * 0.4, d * 0.15), fc.P(hw * 0.4, d * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_back", mirror=True),
        label="Caul",
    )


def _build_curtain():
    """The neck curtain: cut full and gathered onto the caul's back edge, dropping to
    shade the nape and shoulders. Its hem flares past the neck girth."""
    hw, dr = CURTAIN_FLAT_HALF, curtain_drop
    hem_half = max(hw, neck_girth * 0.5) * 1.06
    edges = [
        fc.Edge("centre_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, dr))]),
        fc.Edge("heading", [fc.Line(fc.P(0.0, dr), fc.P(hw, dr))]),   # gathers to the caul
        fc.Edge("side", [fc.Line(fc.P(hw, dr), fc.P(hem_half, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hem_half, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neck-curtain",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 16.0},
        notches=[fc.Notch("heading", 0.5, "gather midpoint")],
        grainline=fc.Grainline(fc.P(hw * 0.4, dr * 0.15), fc.P(hw * 0.4, dr * 0.85)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="centre_back", mirror=True),
        label="Neck curtain",
    )


def _build_tie():
    """A self-fabric chin tie, cut 2."""
    ln, w = tie_length, 34.0
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("long_a", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("long_b", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "tie",
        edges,
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=2),
        label="Chin tie",
    )


def build():
    pattern = fc.PatternSet("sun-bonnet")
    everything = target_piece == "set"

    if everything or target_piece == "brim":
        pattern.add(_build_brim())
    if everything or target_piece == "caul":
        pattern.add(_build_caul())
    if everything or target_piece == "curtain":
        pattern.add(_build_curtain())
    if everything or target_piece == "tie":
        pattern.add(_build_tie())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if {"brim", "caul"} <= names:
        # THE FRONT GATHER. Both pieces are cut on the fold, so each drafted edge is a
        # HALF run: listed twice (each against its own mirror, join-to-join) they give
        # the full runs. The ease is the fullness the gathers remove.
        pattern.declare_seam([("caul", "front_edge"), ("caul", "front_edge")],
                             [("brim", "head_edge"), ("brim", "head_edge")],
                             tol=1.0, ease=CAUL_TAKEN)
    if {"caul", "neck-curtain"} <= names:
        # THE BACK GATHER, same construction onto the caul's nape edge.
        pattern.declare_seam([("neck-curtain", "heading"), ("neck-curtain", "heading")],
                             [("caul", "back_edge"), ("caul", "back_edge")],
                             tol=1.0, ease=CURTAIN_TAKEN)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "shell fabric (cotton lawn, chambray or calico)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 68% marker; the brim needs a second layer."},
        {"item": "brim interlining", "qty": 1, "unit": "set",
         "note": "buckram, heavy canvas, or corded channels — the brim must hold its shade."},
        {"item": "cotton cord (optional)", "qty": 1, "unit": "count",
         "note": "for a corded brim: rows of cord between the two brim layers, the "
                 "traditional way to stiffen a washable bonnet."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "two rows of gathering stitch at each gathered edge."},
    ]
    pattern.metadata = {
        "fc300_rank": 217, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "neck_girth_mm": round(neck_girth, 1),
        "brim_run_mm": round(BRIM_RUN, 2),
        "brim_depth_mm": round(brim_depth, 1),
        "caul_depth_mm": round(caul_depth, 1),
        "curtain_drop_mm": round(curtain_drop, 1),
        "caul_gather": round(caul_gather, 2),
        "curtain_gather": round(curtain_gather, 2),
        "drafting": "stiffened brim + gathered caul + gathered neck curtain + ties",
        "solved": {
            "caul_flat_run_mm": round(BRIM_RUN * caul_gather, 3),
            "caul_finished_run_mm": round(BRIM_RUN, 3),
            "caul_gather_removed_mm": round(CAUL_TAKEN, 3),
            "curtain_flat_run_mm": round(CAUL_BACK * curtain_gather, 3),
            "curtain_finished_run_mm": round(CAUL_BACK, 3),
            "curtain_gather_removed_mm": round(CURTAIN_TAKEN, 3),
        },
    }
    return pattern


result = build()
