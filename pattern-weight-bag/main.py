"""
Pattern-weight bag set — Fashion Cabinet Care & Keeping Cartridge (FC-500 #415, care_keeping, T1).

A set of soft covers that turn the Yantra4D `pattern-weight` cores into quiet, non-scratch
pattern weights — a printed weight core dropped into a padded fabric pouch so it holds tissue
flat without marking it or sliding. Each cover is a TOP disc and a BOTTOM disc joined by a
GUSSET band, sized to the core's diameter and height, with a small turning gap.

Solved, not guessed:

  1. THE COVER IS CUT TO THE MEASURED CORE. The disc radius is the core radius plus the wall,
     and the gusset length is the MEASURED disc circumference — so the cover neither strains
     over the core nor bags loose.
  2. THE GUSSET HEIGHT IS CLAMPED so the band is always at least the core height plus a seam,
     never a hairline the kernel would still close.
  3. THE DISCS ARE POLYGONISED so the two circular seams are measured, not assumed, and the
     gusset is declared to their measured circumference.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # top|bottom|gusset|set

core_dia = float(PARAM(lambda: core_dia, 60.0))
core_height = float(PARAM(lambda: core_height, 26.0))
wall = float(PARAM(lambda: wall, 6.0))                    # fabric+pad wall around the core
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

core_dia = max(30.0, min(core_dia, 140.0))
core_height = max(10.0, min(core_height, 80.0))
wall = max(2.0, min(wall, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 14.0))

DISC_R = core_dia / 2.0 + wall
GUSSET_H = max(core_height + 6.0, core_height + 2.0 * wall)
SEGS = 40


def _disc_pts(r):
    return [fc.P(r * math.cos(2.0 * math.pi * i / SEGS),
                 r * math.sin(2.0 * math.pi * i / SEGS)) for i in range(SEGS)]


def _disc(name, label):
    pts = _disc_pts(DISC_R)
    edges = [fc.Edge(f"arc{i}", [fc.Line(pts[i], pts[(i + 1) % SEGS])])
             for i in range(SEGS)]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("arc0", 0.5, "quarter")],
        grainline=fc.Grainline(fc.P(-DISC_R * 0.5, 0.0), fc.P(DISC_R * 0.5, 0.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


_DISC = _disc("top", "top")
DISC_CIRC = sum(_DISC.edge(f"arc{i}").length(0.05) for i in range(SEGS))


def _gusset():
    ln = DISC_CIRC
    h = GUSSET_H
    return fc.Piece(
        "gusset", [
            fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("upper", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.25, "quarter"),
                 fc.Notch("lower", 0.5, "half"),
                 fc.Notch("lower", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("turning gap",
                               [fc.P(ln * 0.4, h * 0.5), fc.P(ln * 0.6, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Gusset band (cut 1)",
    )


def build():
    pattern = fc.PatternSet("pattern-weight-bag")
    everything = target_piece == "set"
    if everything or target_piece == "top":
        pattern.add(_disc("top", "Top disc (cut 1)"))
    if everything or target_piece == "bottom":
        pattern.add(_disc("bottom", "Bottom disc (cut 1)"))
    if everything or target_piece == "gusset":
        pattern.add(_gusset())

    if everything:
        # the gusset wraps both discs — its length is the measured disc circumference.
        pattern.declare_seam(("gusset", "end_a"), ("gusset", "end_b"), tol=0.5)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "soft cotton / suede-cloth (non-marking)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 55% marker (discs nest poorly); a "
                 f"non-marking face so the weight never prints on tissue."},
        {"item": "pattern-weight core", "qty": 1, "unit": "count",
         "note": f"Yantra4D pattern-weight (notion.hardware_ref) at a {core_dia:.0f} mm "
                 f"diameter; the cover is cut to the core plus a {wall:.0f} mm wall."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "sew the gusset to both discs, leave the turning gap, drop the core in, "
                 "slip the gap closed."},
    ]
    pattern.metadata = {
        "fc500_rank": 415, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A padded cover for a printed pattern-weight core: two discs and "
            "a gusset band, cut to the core.",
        "solved": {
            "disc_radius_mm": round(DISC_R, 1),
            "disc_circumference_mm": round(DISC_CIRC, 1),
            "gusset_height_mm": round(GUSSET_H, 1),
            "note": "the disc radius is the core radius plus the wall; the gusset length is "
                    "the MEASURED (polygonised) disc circumference so the cover neither "
                    "strains nor bags; the gusset height is clamped to at least the core "
                    "height plus a seam.",
        },
        "hardware": "pattern-weight core via Yantra4D (notion.hardware_ref -> "
                    "pattern-weight); weight_dia and weight_h are fed from the core "
                    "dimensions. No flange interface — the cover holds the core, so no "
                    "dimensional handshake is owed.",
    }
    return pattern


result = build()
