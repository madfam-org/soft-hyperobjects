"""
Lingerie Travel Pouch — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #259,
Yantra4D-bridged zipper).

The two-compartment travel pouch that keeps clean underthings away from worn ones —
the single most useful and least glamorous object in a suitcase. A shaped SHELL front
and back, a boxed BASE, a mesh DIVIDER that splits the interior, and a zip that runs
three sides so the pouch opens flat rather than gaping through a slot.

Drafting note — the seam that must SOLVE: the zip runs a U — down one side, across the
top, and down the other — around a shell whose top corners are ROUNDED. The zip length is
therefore not `2·height + width`; it is the MEASURED length of that rounded three-sided
path. This cartridge polygonises the corner arcs, measures the U, and both sizes the
zipper from that measurement and declares the seam against it. The boxed base corners are
solved the same way: a boxed corner removes a square of side `depth/2` from each bottom
corner, which SHORTENS the side and bottom edges by a measured amount.

Pieces:
  - shell    : front/back panel with rounded top corners and boxed base (cut 2).
  - base     : the flat bottom the boxed corners close onto (cut 1).
  - divider  : the mesh partition (cut 1).
  - pull_tab : the zip pull tab (cut 2).

Hardware: `zipper` (Yantra4D). Its `tape_edge` flange is driven by `zip_length`, mapped
from this cartridge's measured U-path — expressed through `pouch_width` and
`pouch_height`, both of which drive the garment's own `zip_tape` interface.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|base|divider|pull_tab|set

pouch_width = float(PARAM(lambda: pouch_width, 300.0))
pouch_height = float(PARAM(lambda: pouch_height, 210.0))
pouch_depth = float(PARAM(lambda: pouch_depth, 90.0))
corner_radius = float(PARAM(lambda: corner_radius, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
pouch_width = max(180.0, min(pouch_width, 460.0))
pouch_height = max(120.0, min(pouch_height, 340.0))
pouch_depth = max(30.0, min(pouch_depth, 180.0))
corner_radius = max(6.0, min(corner_radius, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The rounded corners cannot eat more than the panel allows, and the boxed corner
# cannot eat more than half the panel's height.
corner_radius = min(corner_radius, pouch_width * 0.35, pouch_height * 0.35)
pouch_depth = min(pouch_depth, pouch_height * 0.9, pouch_width * 0.6)

ARC_SEGS = 18                        # per rounded corner; measured, never assumed
BOX = pouch_depth / 2.0              # the square removed at each bottom corner

W, H, R = pouch_width, pouch_height, corner_radius


def _arc(cx, cy, r, a0, a1, n=ARC_SEGS):
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# ── The shell outline, walked CCW from the bottom-left boxed notch ───────────
# Origin at the panel's bottom-left. Boxed corners are notched out; top corners
# are rounded by R.
_TOP_R_ARC = _arc(W - R, H - R, R, 0.0, math.pi / 2.0)          # right → crown
_TOP_L_ARC = _arc(R, H - R, R, math.pi / 2.0, math.pi)          # crown → left

# The zip's U-path: up the right side, round the right corner, across the top,
# round the left corner, down the left side.
_ZIP_RIGHT = [fc.P(W, BOX), fc.P(W, H - R)]
_ZIP_TOP = [fc.P(W - R, H), fc.P(R, H)]
_ZIP_LEFT = [fc.P(0.0, H - R), fc.P(0.0, BOX)]

ZIP_U_LENGTH = (_poly_len(_ZIP_RIGHT) + _poly_len(_TOP_R_ARC)
                + _poly_len(_ZIP_TOP) + _poly_len(_TOP_L_ARC)
                + _poly_len(_ZIP_LEFT))
# The naive answer a formula would have given, for the record:
ZIP_NAIVE = 2.0 * (H - BOX) + W

# The base edge each shell presents, once the two boxed corners are notched out.
BASE_RUN = W - 2.0 * BOX


def build_shell():
    """Front/back panel (cut 2). Rounded top corners, boxed bottom corners."""
    pts_start = fc.P(BOX, 0.0)
    edges = [
        # bottom run between the two boxed notches
        fc.Edge("base_seam", [fc.Line(pts_start, fc.P(W - BOX, 0.0))]),
        # the right boxed notch: out, then up
        fc.Edge("box_r", _lines([fc.P(W - BOX, 0.0), fc.P(W - BOX, BOX),
                                 fc.P(W, BOX)])),
        fc.Edge("zip_r", _lines(_ZIP_RIGHT)),
        fc.Edge("zip_corner_r", _lines(_TOP_R_ARC)),
        fc.Edge("zip_top", _lines(_ZIP_TOP)),
        fc.Edge("zip_corner_l", _lines(_TOP_L_ARC)),
        fc.Edge("zip_l", _lines(_ZIP_LEFT)),
        # the left boxed notch: in, then down to the start
        fc.Edge("box_l", _lines([fc.P(0.0, BOX), fc.P(BOX, BOX),
                                 fc.P(BOX, 0.0)])),
    ]
    internals = [
        fc.Internal("divider-attach",
                    [fc.P(BOX, H * 0.5), fc.P(W - BOX, H * 0.5)],
                    kind="marking"),
        fc.Internal("box-fold-r",
                    [fc.P(W - BOX, 0.0), fc.P(W, BOX)], kind="marking"),
        fc.Internal("box-fold-l",
                    [fc.P(BOX, 0.0), fc.P(0.0, BOX)], kind="marking"),
    ]
    return fc.Piece(
        "shell",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("zip_top", 0.5, "zip centre top"),
                 fc.Notch("base_seam", 0.5, "centre base"),
                 fc.Notch("zip_r", 0.0, "zip stop"),
                 fc.Notch("zip_l", 1.0, "zip stop")],
        grainline=fc.Grainline(fc.P(W * 0.5, 20.0), fc.P(W * 0.5, H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shell panel (front/back)",
    )


def build_base():
    """The flat bottom: BASE_RUN long by pouch_depth wide, sewn to both shells'
    `base_seam` edges and closed at each end by the boxed corners."""
    ln, w = BASE_RUN, pouch_depth
    return fc.Piece(
        "base",
        [
            fc.Edge("to_front", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("to_back", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_l", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("to_front", 0.5, "centre base"),
                 fc.Notch("to_back", 0.5, "centre base")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Boxed base",
    )


def build_divider():
    """The mesh partition: spans the base run and rises to just under the zip, so
    it never fouls the slider."""
    ln = BASE_RUN
    h = H - BOX - 25.0
    return fc.Piece(
        "divider",
        [
            fc.Edge("base_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("free_top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base_edge", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.5, 10.0), fc.P(ln * 0.5, h - 10.0)),
        internals=[fc.Internal("bound-edge",
                               [fc.P(0.0, h - 8.0), fc.P(ln, h - 8.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Mesh divider",
    )


def build_pull_tab():
    """The zip pull tab (cut 2 — one per zip end), folded over the tape."""
    ln, w = 70.0, 26.0
    return fc.Piece(
        "pull_tab",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("bottom", 0.5, "fold line")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Zip pull tab",
    )


def build():
    pattern = fc.PatternSet("lingerie-travel-pouch")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "base":
        pattern.add(build_base())
    if all_pieces or target_piece == "divider":
        pattern.add(build_divider())
    if all_pieces or target_piece == "pull_tab":
        pattern.add(build_pull_tab())

    if all_pieces or target_piece == "shell":
        # THE solving seam: the two shells' zip U-paths meet each other through the
        # zipper tape. Both are the same MEASURED rounded path, not 2·h + w.
        pattern.declare_seam(
            [("shell", "zip_r"), ("shell", "zip_corner_r"), ("shell", "zip_top"),
             ("shell", "zip_corner_l"), ("shell", "zip_l")],
            [("shell", "zip_r"), ("shell", "zip_corner_r"), ("shell", "zip_top"),
             ("shell", "zip_corner_l"), ("shell", "zip_l")],
            tol=0.5)
    if all_pieces:
        # The base's two long edges each take one shell's base seam.
        pattern.declare_seam(("base", "to_front"), ("shell", "base_seam"), tol=0.5)
        pattern.declare_seam(("base", "to_back"), ("shell", "base_seam"), tol=0.5)
        # The divider stands on the base run: same length.
        pattern.declare_seam(("divider", "base_edge"), ("shell", "base_seam"), tol=0.5)
        # Each boxed corner closes on itself: the notch's two arms are equal.
        pattern.declare_seam(("shell", "box_r"), ("shell", "box_l"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "ripstop or cotton lawn shell", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 78% marker."},
        {"item": "zipper", "qty": 1, "unit": "count",
         "note": f"≈ {ZIP_U_LENGTH:.0f} mm — the MEASURED rounded U-path, not the "
                 f"{ZIP_NAIVE:.0f} mm a square-corner formula would have ordered. "
                 f"Yantra4D `zipper` (notion.hardware_ref) is driven off the same "
                 f"pouch_width and pouch_height."},
        {"item": "nylon mesh (divider)", "qty": 1, "unit": "count",
         "note": "mesh, not solid — you have to be able to see which side is which."},
        {"item": "bias binding", "qty": round(BASE_RUN + 100.0), "unit": "mm_length",
         "note": "binds the divider's free top edge."},
    ]
    pattern.metadata = {
        "fc300_rank": 259,
        "family": "care_and_keeping",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(W, 1), "height": round(H, 1),
                        "depth": round(pouch_depth, 1)},
        "solved": {
            "zip_u_measured_mm": round(ZIP_U_LENGTH, 2),
            "zip_naive_formula_mm": round(ZIP_NAIVE, 2),
            "zip_saving_mm": round(ZIP_NAIVE - ZIP_U_LENGTH, 2),
            "corner_radius_mm": round(R, 2),
            "boxed_corner_mm": round(BOX, 2),
            "base_run_mm": round(BASE_RUN, 2),
            "segments_per_corner": ARC_SEGS,
            "note": "the zip runs a rounded U, so its length is the MEASURED path — "
                    "%.1f mm shorter than the 2·h + w a square-corner formula gives. "
                    "Ordering the formula length would leave the slider hanging past "
                    "the stop." % (ZIP_NAIVE - ZIP_U_LENGTH),
        },
        "hardware": "three-sided zip via Yantra4D (notion.hardware_ref -> zipper); "
                    "zip_length driven by pouch_width + pouch_height",
    }
    return pattern


result = build()
