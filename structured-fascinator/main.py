"""
Structured Fascinator — Fashion Cabinet Garment Cartridge (FC-300 #212, Lane 2).

A cocktail fascinator built on a rigid Yantra4D `fascinator-base`: the base disc is
COVERED with a fabric disc (top + under, the under-cover finished by the trim ring),
and a shallow DOME cover is drafted as a gored cap that sits proud of the disc. A
bias TRIM RING binds the outer edge — and it is the trim ring that makes the bridge
DIMENSIONAL: the ring's inner run is the base circumference, so the garment's own
`sew_ring` interface and the base's `trim_sew_ring` flange share `base_dia`.

Pieces:
  - cover-top   : the fabric disc covering the base's upper face, cut 1.
  - cover-under : the same disc for the underside, cut 1.
  - dome-gore   : a gore of the shallow dome cap, cut `dome_gores` (mirrored).
  - trim-ring   : the bias strip that binds the base edge, cut 1.

Drafting note — circular pieces are 48-gon polygons on a CORRECTED radius so the
polygon perimeter equals the intended circumference exactly
(r = C / (2n sin(pi/n))); the naive C/2pi radius under-runs it and pollutes the
seam checks.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # cover|dome|trim|set

base_dia = float(PARAM(lambda: base_dia, 140.0))     # the Yantra4D base disc diameter
dome_height = float(PARAM(lambda: dome_height, 45.0))
dome_gores = int(PARAM(lambda: dome_gores, 6))
trim_width = float(PARAM(lambda: trim_width, 32.0))
cover_margin = float(PARAM(lambda: cover_margin, 12.0))  # cover wraps past the rim
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
base_dia = max(70.0, min(base_dia, 300.0))
dome_height = max(12.0, min(dome_height, 110.0))
dome_gores = max(4, min(dome_gores, 10))
trim_width = max(14.0, min(trim_width, 60.0))
cover_margin = max(4.0, min(cover_margin, 30.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

SIDES = 48
TWO_PI = 2.0 * math.pi

BASE_CIRC = math.pi * base_dia          # the run the trim ring binds
COVER_DIA = base_dia + 2.0 * cover_margin
COVER_CIRC = math.pi * COVER_DIA


def _poly_radius(circumference, n):
    """Radius of a regular n-gon whose PERIMETER equals `circumference`."""
    return circumference / (2.0 * n * math.sin(math.pi / n))


R_COVER = _poly_radius(COVER_CIRC, SIDES)


def _ring_points(r, n):
    """n+1 points closing a regular n-gon of radius r (last point == first)."""
    return [fc.P(r * math.cos(TWO_PI * i / n), r * math.sin(TWO_PI * i / n))
            for i in range(n + 1)]


def _build_cover(name, label):
    """A fabric disc covering one face of the rigid base, with `cover_margin` of
    wrap past the rim. Two half-ring edges give the piece named seam references."""
    pts = _ring_points(R_COVER, SIDES)
    half = SIDES // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SIDES)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, -R_COVER * 0.6), fc.P(0.0, R_COVER * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def _build_dome_gore():
    """One gore of the shallow dome cap: base width = dome base circumference /
    gores at y=0, curving on two Beziers to a shared apex at (0, dome_height)."""
    dome_base_circ = BASE_CIRC * 0.72       # the dome sits inboard of the rim
    gore_base = dome_base_circ / dome_gores
    gb = gore_base / 2.0
    apex = fc.P(0.0, dome_height)
    left = fc.Bezier(fc.P(-gb, 0.0), fc.P(-gb * 0.96, dome_height * 0.42),
                     fc.P(-gb * 0.42, dome_height * 0.86), apex)
    right = fc.Bezier(apex, fc.P(gb * 0.42, dome_height * 0.86),
                      fc.P(gb * 0.96, dome_height * 0.42), fc.P(gb, 0.0))
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(gb, 0.0), fc.P(-gb, 0.0))]),
        fc.Edge("seam_l", [left]),
        fc.Edge("seam_r", [right]),
    ]
    return fc.Piece(
        "dome-gore",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(0.0, dome_height * 0.1), fc.P(0.0, dome_height * 0.85)),
        cut=fc.CutSpec(quantity=dome_gores, mirror=True),
        label="Dome gore",
    )


def _build_trim_ring():
    """The bias strip binding the base's outer edge. Its INNER long edge measures the
    base circumference — this is the run that mates the Yantra4D base's trim_sew_ring
    flange, so `base_dia` drives both the hardware edge and this garment edge."""
    ln, w = BASE_CIRC, trim_width
    edges = [
        fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("outer", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("join_b", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("sew_ring", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "trim-ring",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("sew_ring", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Trim ring (bias)",
    )


def build():
    pattern = fc.PatternSet("structured-fascinator")
    everything = target_piece == "set"

    if everything or target_piece == "cover":
        pattern.add(_build_cover("cover-top", "Cover — top face"))
        pattern.add(_build_cover("cover-under", "Cover — underside"))
    if everything or target_piece == "dome":
        pattern.add(_build_dome_gore())
    if everything or target_piece == "trim":
        pattern.add(_build_trim_ring())

    # ── Seams ────────────────────────────────────────────────────────────────
    names = {p.name for p in pattern.pieces}
    if {"cover-top", "cover-under"} <= names:
        # The two covers are sewn rim to rim around the rigid base.
        pattern.declare_seam([("cover-top", "rim_a"), ("cover-top", "rim_b")],
                             [("cover-under", "rim_a"), ("cover-under", "rim_b")],
                             tol=1.5)
    if "dome-gore" in names:
        # Gore to gore: each gore's left seam takes its neighbour's right seam.
        pattern.declare_seam(("dome-gore", "seam_l"), ("dome-gore", "seam_r"), tol=1.0)
    if "trim-ring" in names:
        # The bias strip closes into a ring: its own two ends join.
        pattern.declare_seam(("trim-ring", "join_a"), ("trim-ring", "join_b"), tol=1.0)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "cover fabric (sinamay, silk dupion or velvet)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 55% marker; cut the trim ring on the bias."},
        {"item": "fascinator base", "qty": 1, "unit": "count",
         "note": "Yantra4D fascinator-base (see notion.hardware_ref) — the rigid disc/dome "
                 "the covers are sewn over, sized by base_dia."},
        {"item": "millinery wire + thread", "qty": 1, "unit": "set",
         "note": "wire the covered rim before binding it with the trim ring."},
        {"item": "comb or elastic", "qty": 1, "unit": "count",
         "note": "the base's comb_slot takes a comb; the slot is Yantra4D's, not the pattern's."},
    ]
    pattern.metadata = {
        "fc300_rank": 212, "family": "millinery", "lane": 2,
        "base_dia_mm": round(base_dia, 1),
        "base_circumference_mm": round(BASE_CIRC, 2),
        "cover_dia_mm": round(COVER_DIA, 1),
        "dome_height_mm": round(dome_height, 1),
        "dome_gores": dome_gores,
        "trim_width_mm": round(trim_width, 1),
        "drafting": "covered-base discs + gored shallow dome + bias trim ring",
        "hardware": "rigid base delegated to Yantra4D fascinator-base; the trim ring's "
                    "sew_ring edge mates its trim_sew_ring flange (base_dia shared)",
        "solved": {
            "trim_inner_run_mm": round(BASE_CIRC, 3),
            "cover_rim_run_mm": round(COVER_CIRC, 3),
        },
    }
    return pattern


result = build()
