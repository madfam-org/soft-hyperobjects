"""
Pillbox Hat — Fashion Cabinet Garment Cartridge (FC-300 #211, Lane 2 millinery).

The classic pillbox: a flat circular TIP sitting on a straight cylindrical SIDE BAND,
with no brim. Fully lined — the lining repeats the tip and band, so the hat is clean
inside and the head opening is a finished, bagged-out edge. Sizing is delegated to a
Yantra4D `hat-size-reducer` strip clipped inside the band (point/slot hardware — it
sits in the band, it is not sewn to a garment edge).

Pieces:
  - tip       : the flat circular crown (shell), cut 1.
  - side-band : the cylindrical wall, head circumference x band height, cut 1.
  - tip-lining/band-lining : the lining repeats, cut 1 each.

Drafting note — the circular pieces are 48-gon polygons whose radius is CORRECTED so
the polygon perimeter equals the target circumference exactly (r = C / (2n sin(pi/n))).
A naive C/2pi radius under-runs the circumference by ~0.4 mm at head size, which is
seam-check noise; the correction makes the tip/band seam exact.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # tip|side-band|lining|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
band_height = float(PARAM(lambda: band_height, 70.0))
ease = float(PARAM(lambda: ease, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
lined = bool(PARAM(lambda: lined, True))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth = max(480.0, min(head_girth, 640.0))
band_height = max(35.0, min(band_height, 130.0))
ease = max(0.0, min(ease, 24.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SIDES = 48
head_eff = head_girth + ease          # the finished head opening the band wraps


def _poly_radius(circumference, n):
    """Radius of a regular n-gon whose PERIMETER equals `circumference` — so the
    drafted polygon edge measures the real circumference, not the inscribed chord
    sum of a C/2pi circle."""
    return circumference / (2.0 * n * math.sin(math.pi / n))


R_TIP = _poly_radius(head_eff, SIDES)


def _ring_points(r, n):
    """n+1 points closing a regular n-gon of radius r (last point == first)."""
    return [fc.P(r * math.cos(2.0 * math.pi * i / n),
                 r * math.sin(2.0 * math.pi * i / n)) for i in range(n + 1)]


def _build_tip(name, label):
    """The flat circular crown. Split into two half-ring edges so the piece carries
    named seam references (the whole ring sews to the band top)."""
    pts = _ring_points(R_TIP, SIDES)
    half = SIDES // 2
    edges = [
        fc.Edge("tip_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("tip_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SIDES)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("tip_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_TIP * 0.6), fc.P(0.0, R_TIP * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def _build_band(name, label):
    """The cylindrical wall: a rectangle head_eff wide (it wraps into a tube, its two
    end seams joining) by band_height tall."""
    w, h = head_eff, band_height
    edges = [
        fc.Edge("seam_cb_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),        # sews to the tip
        fc.Edge("seam_cb_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("head_opening", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "centre front"),
                 fc.Notch("head_opening", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build():
    pattern = fc.PatternSet("pillbox-hat")
    everything = target_piece == "set"
    want_lining = lined and (everything or target_piece == "lining")

    if everything or target_piece == "tip":
        pattern.add(_build_tip("tip", "Tip (crown)"))
    if everything or target_piece == "side-band":
        pattern.add(_build_band("side-band", "Side band"))
    if want_lining:
        pattern.add(_build_tip("tip-lining", "Tip lining"))
        pattern.add(_build_band("band-lining", "Band lining"))

    # ── Seams ────────────────────────────────────────────────────────────────
    # The full tip ring (both half-edges) sews to the band's top edge.
    names = {p.name for p in pattern.pieces}
    if {"tip", "side-band"} <= names:
        pattern.declare_seam([("tip", "tip_a"), ("tip", "tip_b")],
                             ("side-band", "top"), tol=1.5)
        # The band wraps to a tube: its own two end seams join each other.
        pattern.declare_seam(("side-band", "seam_cb_a"),
                             ("side-band", "seam_cb_b"), tol=1.0)
    if {"tip-lining", "band-lining"} <= names:
        pattern.declare_seam([("tip-lining", "tip_a"), ("tip-lining", "tip_b")],
                             ("band-lining", "top"), tol=1.5)
        pattern.declare_seam(("band-lining", "seam_cb_a"),
                             ("band-lining", "seam_cb_b"), tol=1.0)
    # Shell and lining are bagged out together at the head opening.
    if {"side-band", "band-lining"} <= names:
        pattern.declare_seam(("side-band", "head_opening"),
                             ("band-lining", "head_opening"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "shell fabric (wool felt, faille or velvet)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 62% marker; a firm hand holds the cylinder."},
        {"item": "fusible interfacing / buckram",
         "qty": 1, "unit": "set",
         "note": "block-fuse the tip and band before cutting — the pillbox is a stiffened shell."},
        {"item": "hat size reducer strip", "qty": 1, "unit": "count",
         "note": "Yantra4D hat-size-reducer (see notion.hardware_ref) — clips inside the "
                 "band to take the hat down a size; not sewn into a seam."},
        {"item": "millinery thread + hat elastic", "qty": 1, "unit": "set",
         "note": "elastic or a comb anchors the pillbox; the reducer tunes the fit."},
    ]
    pattern.metadata = {
        "fc300_rank": 211, "family": "millinery", "lane": 2,
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "tip_radius_mm": round(R_TIP, 2),
        "band_height_mm": round(band_height, 1),
        "lined": lined,
        "drafting": "corrected-radius 48-gon tip + rectangular side band; fully lined",
        "hardware": "sizing delegated to Yantra4D hat-size-reducer (point/slot — no sewn edge)",
        "solved": {
            "tip_perimeter_mm": round(head_eff, 3),
            "band_top_mm": round(head_eff, 3),
        },
    }
    return pattern


result = build()
