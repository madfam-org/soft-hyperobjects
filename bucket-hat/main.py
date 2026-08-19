"""
Bucket Hat — Fashion Cabinet Accessory Cartridge.

A made-to-measure bucket hat from the head girth: a circular CROWN, a rectangular SIDE
BAND (head circumference x crown depth), and a down-sloping BRIM drafted as a
half-annulus cut on the fold (fold + mirror = the full ring). A pure soft-goods
garment — no hardware.

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
head_girth = float(PARAM(lambda: head_girth, 570.0))
crown_depth = float(PARAM(lambda: crown_depth, 90.0))
brim_width = float(PARAM(lambda: brim_width, 60.0))
ease = float(PARAM(lambda: ease, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
crown_depth = max(50.0, min(crown_depth, 140.0))
brim_width = max(30.0, min(brim_width, 100.0))
ease = max(0.0, min(ease, 30.0))

TWO_PI = 2.0 * math.pi
head_eff = head_girth + ease
r_head = head_eff / TWO_PI           # crown / head-opening radius
SIDES = 48                            # polygon approximation of circular edges


def _arc_points(cx, cy, r, a0, a1, n):
    """n+1 points along the arc from a0 to a1 (radians) on a circle at (cx, cy)."""
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def build_crown():
    """A full circular crown, radius r_head + a small seam-join allowance built into
    the side seam. Approximated as a closed polygon (one edge, many segments)."""
    pts = _arc_points(0.0, 0.0, r_head, 0.0, TWO_PI, SIDES)
    # A single closed edge (last point == first); split into two named edges so the
    # piece has a sensible seam reference.
    half = SIDES // 2
    seg_a = [fc.Line(pts[i], pts[i + 1]) for i in range(half)]
    seg_b = [fc.Line(pts[i], pts[i + 1]) for i in range(half, SIDES)]
    edges = [fc.Edge("crown_seam_a", seg_a), fc.Edge("crown_seam_b", seg_b)]
    return fc.Piece(
        "crown",
        edges,
        seam_allowance=10.0,
        grainline=fc.Grainline(fc.P(0.0, -r_head * 0.6), fc.P(0.0, r_head * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Crown",
    )


def build_side_band():
    """The side wall: a rectangle head_eff wide (it wraps to a tube) x crown_depth."""
    w, h = head_eff, crown_depth
    edges = [
        fc.Edge("seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top",    [fc.Line(fc.P(0.0, h), fc.P(w, h))]),   # joins the crown
        fc.Edge("seam_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),  # joins the brim
    ]
    return fc.Piece(
        "side-band",
        edges,
        seam_allowance=10.0,
        notches=[fc.Notch("top", 0.5, "center back"), fc.Notch("bottom", 0.5, "center back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1),
        label="Side Band",
    )


def build_brim():
    """A half-annulus (inner r_head, outer r_head+brim_width) spanning a semicircle,
    cut on the straight center edge (fold) and mirrored → the full brim ring."""
    r_in, r_out = r_head, r_head + brim_width
    # Semicircle from -90° to +90° (right half), joined by two straight radial edges.
    outer = _arc_points(0.0, 0.0, r_out, -math.pi / 2.0, math.pi / 2.0, SIDES // 2)
    inner = _arc_points(0.0, 0.0, r_in, math.pi / 2.0, -math.pi / 2.0, SIDES // 2)
    edges = [
        fc.Edge("outer", [fc.Line(outer[i], outer[i + 1]) for i in range(len(outer) - 1)]),
        fc.Edge("center_top", [fc.Line(outer[-1], inner[0])]),   # top radial (fold side seam)
        fc.Edge("inner", [fc.Line(inner[i], inner[i + 1]) for i in range(len(inner) - 1)]),
        fc.Edge("center", [fc.Line(inner[-1], outer[0])]),        # the fold edge
    ]
    return fc.Piece(
        "brim",
        edges,
        seam_allowance=10.0,
        grainline=fc.Grainline(fc.P(r_in + brim_width * 0.3, -r_out * 0.3),
                               fc.P(r_in + brim_width * 0.3, r_out * 0.3)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Brim",
    )


def build():
    pattern = fc.PatternSet("bucket-hat")
    pattern.add(build_crown())
    pattern.add(build_side_band())
    pattern.add(build_brim())
    fabric_width = 1400.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0) for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "shell fabric", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm, 60% marker; double for a reversible/lined hat"},
        {"item": "sewing thread", "qty": 1, "unit": "spool", "note": "topstitch the brim"},
    ]
    pattern.metadata = {
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "crown_radius_mm": round(r_head, 1),
        "brim_width_mm": round(brim_width, 1),
        "drafting": "circular crown + rectangular side band + half-annulus brim on fold",
    }
    return pattern


result = build()
