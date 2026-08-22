"""
Boot Shaper Sleeve — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #258,
Yantra4D-bridged hook-and-loop tape).

The stiffened sleeve that stands inside a tall boot so the shaft does not crease and
collapse at the ankle. A leather boot left slumped for a season learns the fold; this is
the removable insert that prevents it. A tapered SLEEVE wraps into a truncated cone,
a stiffening BATTEN pocket runs its height, and a hook-and-loop TAB lets one sleeve fit
a range of calf widths.

Drafting note — the seam that must SOLVE: a boot shaft is a TRUNCATED CONE (wider at the
calf than at the ankle), and the flat pattern for a cone is an ANNULAR SECTOR — not a
trapezoid. Getting this wrong is the classic error: a trapezoid rolled up gives a cone
whose seam edges do not lie flat against each other. This cartridge solves the true cone
development — slant height from the radius difference, sector angle from the ratio — and
then POLYGONISES AND MEASURES both arcs, so the top arc really equals the calf
circumference and the bottom arc really equals the ankle circumference.

Pieces:
  - sleeve : the annular-sector cone development (cut 1).
  - batten : the stiffener pocket that runs the slant height (cut 1).
  - tab    : the hook-and-loop adjustment tab (cut 2).

Hardware: `hook-loop-tape` (Yantra4D). Its `sew_face` flange is driven by `strip_width`,
mapped from this cartridge's `tab_width` — which also drives the garment's own
`closure_tab` interface, so the handshake is dimensional.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # sleeve|batten|tab|set

shaft_height = float(PARAM(lambda: shaft_height, 330.0))   # ankle to boot top
calf_circ = float(PARAM(lambda: calf_circ, 380.0))         # circumference at the top
ankle_circ = float(PARAM(lambda: ankle_circ, 260.0))       # circumference at the base
tab_width = float(PARAM(lambda: tab_width, 25.0))          # drives the Yantra4D tape
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
shaft_height = max(150.0, min(shaft_height, 520.0))
calf_circ = max(240.0, min(calf_circ, 520.0))
ankle_circ = max(180.0, min(ankle_circ, 420.0))
tab_width = max(12.0, min(tab_width, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# A shaper only makes sense when the calf is wider than the ankle; if a caller passes
# an inverted pair, hold a minimum flare rather than draft an inside-out cone.
ankle_circ = min(ankle_circ, calf_circ - 20.0)

ARC_SEGS = 40           # per arc; both arcs are polygonised and MEASURED

# ── Solve the truncated-cone development ─────────────────────────────────────
R_TOP = calf_circ / (2.0 * math.pi)        # radius at the boot top
R_BOT = ankle_circ / (2.0 * math.pi)       # radius at the ankle
D_R = R_TOP - R_BOT                        # radial difference over the shaft

# Slant height of the frustum's wall (the pattern's radial depth).
SLANT = math.hypot(shaft_height, D_R)

# Develop: the sector's outer radius is the full cone's slant to the wide end.
# For a frustum, L_outer / L_inner = R_TOP / R_BOT, and L_outer − L_inner = SLANT.
L_OUTER = SLANT * R_TOP / D_R
L_INNER = L_OUTER - SLANT

# The sector angle that makes the outer arc equal the calf circumference.
SECTOR_ANGLE = calf_circ / L_OUTER          # radians


def _arc(r, a0, a1, n=ARC_SEGS):
    return [fc.P(r * math.cos(a0 + (a1 - a0) * i / n),
                 r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# Draft the sector symmetric about the +y axis so the piece sits upright.
_A0 = math.pi / 2.0 - SECTOR_ANGLE / 2.0
_A1 = math.pi / 2.0 + SECTOR_ANGLE / 2.0

_OUTER_ARC = _arc(L_OUTER, _A0, _A1)                    # the calf edge
_INNER_ARC = list(reversed(_arc(L_INNER, _A0, _A1)))    # the ankle edge, walked back

OUTER_ARC_LEN = _poly_len(_OUTER_ARC)
INNER_ARC_LEN = _poly_len(_INNER_ARC)


def build_sleeve():
    """The cone development: an annular sector. `arc_calf` becomes the boot top,
    `arc_ankle` the base, and `seam_a` / `seam_b` meet each other up the back."""
    edges = [
        fc.Edge("arc_calf", _lines(_OUTER_ARC)),
        fc.Edge("seam_b", [fc.Line(_OUTER_ARC[-1], _INNER_ARC[0])]),
        fc.Edge("arc_ankle", _lines(_INNER_ARC)),
        fc.Edge("seam_a", [fc.Line(_INNER_ARC[-1], _OUTER_ARC[0])]),
    ]
    # The batten channel runs radially at the sector's centre — up the boot's front.
    mid = math.pi / 2.0
    internals = [
        fc.Internal("batten-channel",
                    [fc.P(L_INNER * math.cos(mid), L_INNER * math.sin(mid)),
                     fc.P(L_OUTER * math.cos(mid), L_OUTER * math.sin(mid))],
                    kind="marking"),
    ]
    # Vent holes on the quarter radials: a sealed shaper traps damp and rots leather.
    for f in (0.25, 0.75):
        a = _A0 + SECTOR_ANGLE * f
        rm = (L_INNER + L_OUTER) * 0.5
        internals.append(fc.Internal("vent",
                                     [fc.P((rm - 14.0) * math.cos(a),
                                           (rm - 14.0) * math.sin(a)),
                                      fc.P((rm + 14.0) * math.cos(a),
                                           (rm + 14.0) * math.sin(a))],
                                     kind="drill"))
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("arc_calf", 0.5, "boot front centre"),
                 fc.Notch("arc_ankle", 0.5, "boot front centre"),
                 fc.Notch("arc_calf", 0.25, "quarter"),
                 fc.Notch("arc_calf", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(0.0, L_INNER + 10.0), fc.P(0.0, L_OUTER - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cone sleeve (annular sector)",
    )


def build_batten():
    """The stiffener pocket: runs the slant height, cut double and folded so the
    batten slides in from the top and can be pulled for washing."""
    ln, w = SLANT, max(38.0, tab_width * 1.6)
    return fc.Piece(
        "batten",
        [
            fc.Edge("attach_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ln))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, ln), fc.P(w, ln))]),
            fc.Edge("attach_r", [fc.Line(fc.P(w, ln), fc.P(w, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        notches=[fc.Notch("attach_l", 0.5, "midpoint")],
        grainline=fc.Grainline(fc.P(w * 0.5, 10.0), fc.P(w * 0.5, ln - 10.0)),
        cut=fc.CutSpec(quantity=1),
        label="Batten pocket",
    )


# The tab must span the largest adjustment the sleeve offers: from a fully closed
# cone to one opened by a quarter of the calf circumference.
TAB_LENGTH = max(70.0, calf_circ * 0.28)


def build_tab():
    """The hook-and-loop adjustment tab (cut 2 — hook side and loop side)."""
    ln, w = TAB_LENGTH, tab_width
    return fc.Piece(
        "tab",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("sewn_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.15, "tape start")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("tape-field",
                               [fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.95, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hook-and-loop tab",
    )


def build():
    pattern = fc.PatternSet("boot-shaper-sleeve")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces or target_piece == "batten":
        pattern.add(build_batten())
    if all_pieces or target_piece == "tab":
        pattern.add(build_tab())

    if all_pieces or target_piece == "sleeve":
        # THE solving seam: the sector's two radial edges meet up the boot's back.
        # Both are exactly SLANT long — that they match is the proof the development
        # is a true cone and not a trapezoid rolled into an approximation.
        pattern.declare_seam(("sleeve", "seam_a"), ("sleeve", "seam_b"), tol=0.3)
    if all_pieces:
        # The batten runs the sector's radial depth: the same SLANT.
        pattern.declare_seam(("batten", "attach_l"), ("sleeve", "seam_a"), tol=0.5)
        pattern.declare_seam(("batten", "attach_r"), ("sleeve", "seam_b"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)   # a sector nests badly; be honest
    pattern.bom = [
        {"item": "canvas or heavy twill", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker — an annular sector nests poorly; "
                 "cut two boots' worth head-to-tail to recover some of it."},
        {"item": "hook-and-loop tape", "qty": round(TAB_LENGTH * 2.0), "unit": "mm_length",
         "note": f"Yantra4D hook-loop-tape (see notion.hardware_ref), {tab_width:.0f} mm "
                 f"wide — its sew_face takes the same tab_width."},
        {"item": "batten (plastic or split cane)", "qty": round(SLANT), "unit": "mm_length",
         "note": "slides into the batten pocket; removable so the sleeve can be washed."},
        {"item": "eyelets or worked vents", "qty": 2, "unit": "count",
         "note": "at the marked vent points — a sealed shaper rots the leather it "
                 "is meant to save."},
    ]
    pattern.metadata = {
        "fc300_rank": 258,
        "family": "care_and_keeping",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"shaft_height": round(shaft_height, 1),
                        "calf_circ": round(calf_circ, 1),
                        "ankle_circ": round(ankle_circ, 1)},
        "solved": {
            "r_top_mm": round(R_TOP, 2),
            "r_bottom_mm": round(R_BOT, 2),
            "slant_height_mm": round(SLANT, 2),
            "sector_outer_radius_mm": round(L_OUTER, 2),
            "sector_inner_radius_mm": round(L_INNER, 2),
            "sector_angle_deg": round(math.degrees(SECTOR_ANGLE), 2),
            "measured_calf_arc_mm": round(OUTER_ARC_LEN, 2),
            "target_calf_circ_mm": round(calf_circ, 2),
            "measured_ankle_arc_mm": round(INNER_ARC_LEN, 2),
            "target_ankle_circ_mm": round(ankle_circ, 2),
            "segments_per_arc": ARC_SEGS,
            "note": "a truncated cone develops flat as an ANNULAR SECTOR, not a "
                    "trapezoid. Slant and sector angle are solved from the two radii, "
                    "then both arcs are polygonised and MEASURED against the target "
                    "circumferences — the chord error is reported, not hidden.",
        },
        "hardware": "adjustment tape via Yantra4D "
                    "(notion.hardware_ref -> hook-loop-tape); strip_width = tab_width",
    }
    return pattern


result = build()
