"""
Capelet — Fashion Cabinet Garment Cartridge (FC-200 #177, layer gap).

The short shoulder cape: a circular (partial-annulus) cape that covers the shoulders and upper
arms, opening at the centre front, with a small stand or tie at the neck. Drafted as a ring
segment whose inner arc equals the neck opening (solved) and whose outer arc gives the cape's
sweep, with a centre-front opening. Distinct from FC-100's ponchos (sarape-poncho) and outerwear
— the capelet is a short, neat shoulder layer. No side seams: the cape is one swept piece.

Pieces:
  - cape  : partial-annulus cape (cut on fold at CB), inner arc == neck, CF open.
  - collar: a small stand collar strip solved to the neck opening.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))    # cape|collar|set

neck_girth   = float(PARAM(lambda: neck_girth, 420.0))     # base of the neck (cape inner arc)
cape_length  = float(PARAM(lambda: cape_length, 320.0))    # neck to cape hem (covers shoulders)
sweep        = float(PARAM(lambda: sweep, 2.1))            # outer arc / inner arc (fullness)
collar_height = float(PARAM(lambda: collar_height, 55.0))  # stand collar height
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
neck_girth   = max(300.0, min(neck_girth, 620.0))
cape_length  = max(180.0, min(cape_length, 560.0))
sweep        = max(1.4, min(sweep, 3.0))
collar_height = max(0.0, min(collar_height, 110.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 50.0))

# Full-circle cape opened at CF: the inner arc == neck_girth. On fold at CB, we draft HALF.
INNER_ARC_HALF = neck_girth / 2.0
# choose an inner radius so the half sweep subtends a workable angle
r_in = max(INNER_ARC_HALF / math.radians(150.0), 40.0)
theta = INNER_ARC_HALF / r_in                        # radians of the half-cape
r_out = (INNER_ARC_HALF * sweep) / theta             # so outer arc == inner * sweep over theta
r_out = max(r_out, r_in + cape_length)


def build_cape():
    n = 28
    inner = [fc.P(r_in * math.cos(theta * i / n), r_in * math.sin(theta * i / n))
             for i in range(n + 1)]
    outer = [fc.P(r_out * math.cos(theta * i / n), r_out * math.sin(theta * i / n))
             for i in range(n + 1)]
    neck_edge = fc.Edge("neck", [fc.Line(inner[i], inner[i + 1]) for i in range(n)])
    cf_edge = fc.Edge("center_front", [fc.Line(inner[n], outer[n])])   # CF opening (radial)
    hem_edge = fc.Edge("hem", [fc.Line(outer[n - i], outer[n - i - 1]) for i in range(n)])
    cb_fold = fc.Edge("center_back", [fc.Line(outer[0], inner[0])])    # CB (on fold)
    return fc.Piece(
        "cape",
        [neck_edge, cf_edge, hem_edge, cb_fold],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("neck", 0.0, "centre back"), fc.Notch("neck", 1.0, "centre front")],
        grainline=fc.Grainline(fc.P(r_in + 20.0, 8.0), fc.P(r_out - 20.0, 8.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Cape",
    )


def build_collar():
    ln = neck_girth + 20.0
    h = collar_height * 2.0
    return fc.Piece(
        "collar",
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
        label="Stand collar",
    )


def build():
    pattern = fc.PatternSet("capelet")
    everything = target_piece == "set"
    if everything or target_piece == "cape":
        pattern.add(build_cape())
    if everything or (target_piece == "collar" and collar_height > 0.0):
        if collar_height > 0.0:
            pattern.add(build_collar())

    fabric_width = 1450.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "wool melton, felt, or a drapey coating",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1450 mm width, 70% marker; a fabric that holds a clean circular sweep."},
        {"item": "neck closure (tie, hook, or button)", "qty": 1, "unit": "set",
         "note": "the CF opening closes at the neck; the body hangs open."},
        {"item": "lining (optional)", "qty": 1, "unit": "as chosen",
         "note": "a full lining gives a clean finish; the maker's choice."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "collar + edges."},
    ]
    pattern.metadata = {
        "fc200_rank": 177, "family": "knitwear", "fabric_hint": "melton-lana",
        "silhouette_note": "A short circular shoulder cape (partial annulus) opening at CF, with "
            "a small stand collar. The inner arc is solved to equal the neck opening and the "
            "outer arc gives the sweep; no side seams — the cape is one swept piece.",
        "solved": {"neck_arc_half_mm": round(INNER_ARC_HALF, 1), "r_in_mm": round(r_in, 1),
                   "r_out_mm": round(r_out, 1), "sweep": sweep},
    }
    return pattern


result = build()
