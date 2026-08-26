"""
Sensory-friendly Seamless Tee — Fashion Cabinet Garment Cartridge
(FC-400 rank #374, adaptive, pattern-only).

A tee drafted to touch the skin as little as possible: the body is cut as ONE tube with the
side seams on the fold, so there is no side seam to rub; the neck is finished with a soft
folded band rather than a bound-and-topstitched edge; and there is no back label — the size
is printed on the inside hem in the marked ink box. For a wearer with sensory processing
differences, a seam or a tag against the skin is not a nuisance but a whole-day distraction;
removing them is the design.

Drafting note — the seam that must SOLVE: cutting the body as a single tube means the front
and back necklines are two scoops out of ONE panel, and they must both land at the right
depth with the shoulder line between them the correct width. The neckband length is the
MEASURED sum of the front and back neck scoops, so the band lands flat and does not ripple —
a rippled neckband is exactly the kind of edge a sensory-friendly tee cannot have. The
shoulder-line width is derived from the shoulder measurement, and the scoops are clamped so a
deep front scoop can never cross the shoulder line.

Pieces:
  - body    : the tube (cut 1 on fold at each side), front and back scoops.
  - sleeve  : soft-set sleeve (cut 2 mirrored), flat-seam cap.
  - band    : the folded neckband (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|sleeve|band|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
tee_length = float(PARAM(lambda: tee_length, 660.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 420.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 220.0))
neck_scoop = float(PARAM(lambda: neck_scoop, 70.0))       # front neck depth
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(600.0, min(chest_girth, 1400.0))
tee_length = max(440.0, min(tee_length, 840.0))
shoulder_width = max(300.0, min(shoulder_width, 560.0))
sleeve_length = max(100.0, min(sleeve_length, 400.0))
neck_scoop = max(30.0, min(neck_scoop, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

EASE = 60.0                                   # a soft, non-clinging tee
HALF_BODY = (chest_girth + EASE) / 4.0        # one quarter, cut on fold at the side
HALF_SHOULDER = shoulder_width / 2.0
# The neck opening half-width at the shoulder line.
NECK_HALF = min(HALF_SHOULDER * 0.42, HALF_BODY * 0.7)
NECK_DROP_B = 20.0                            # shallow back scoop
ARMHOLE_DROP = min(230.0, tee_length * 0.42)
# The front scoop must stay above the armhole base so it never crosses it.
neck_scoop = min(neck_scoop, ARMHOLE_DROP - 40.0)
SEG = 16


def _scoop(x_out, y_top, depth, n=SEG):
    """A half neck scoop from the shoulder point (x_out, y_top) down to centre
    (0, y_top - depth), as a smooth quarter-cosine."""
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x_out * (1.0 - t)
        y = y_top - depth * (1.0 - math.cos(t * math.pi / 2.0))
        pts.append(fc.P(x, y))
    return pts


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# Build the two scoops once and MEASURE them for the neckband.
_TOP = tee_length
_FRONT_SCOOP = _scoop(NECK_HALF, _TOP, neck_scoop)
_BACK_SCOOP = _scoop(NECK_HALF, _TOP, NECK_DROP_B)
NECK_RUN = 2.0 * _poly_len(_FRONT_SCOOP) + 2.0 * _poly_len(_BACK_SCOOP)


def build_body():
    """The tube (cut 1 on fold at each side). Right half drawn; the left is the fold.
    Front and back are the same panel joined at the shoulders; the scoops are cut from
    the top. Modelled here as the front half with the front scoop; the back scoop is a
    marked line since the tube is symmetric front-to-back below the shoulder."""
    hb = HALF_BODY
    top = tee_length
    p_hem_fold = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hb, 0.0)
    p_arm_base = fc.P(hb, top - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, top - 6.0)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    scoop = _FRONT_SCOOP
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_fold, p_hem_side)]),
        fc.Edge("side_fold_r", [fc.Line(p_hem_side, p_arm_base)]),
        fc.Edge("armhole", [fc.Bezier(p_arm_base,
                                      fc.P(hb - 6.0, top - ARMHOLE_DROP * 0.44),
                                      fc.P(HALF_SHOULDER + 8.0, top - 30.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", _lines(scoop)),
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, top - neck_scoop), p_hem_fold)]),
    ]
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 24.0, "cf_fold": 0.0, "side_fold_r": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("neck", 0.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(hb * 0.5, 30.0), fc.P(hb * 0.5, top - 30.0)),
        internals=[fc.Internal("flatlock-note",
                               [fc.P(hb * 0.3, top * 0.3), fc.P(hb * 0.6, top * 0.3)],
                               kind="marking"),
                   fc.Internal("size-ink-box",
                               [fc.P(hb * 0.2, 20.0), fc.P(hb * 0.5, 20.0),
                                fc.P(hb * 0.5, 40.0), fc.P(hb * 0.2, 40.0),
                                fc.P(hb * 0.2, 20.0)], kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Seamless tube body",
    )


def build_sleeve():
    """Soft-set sleeve (cut 2 mirrored), flat-seam cap. Cap length is a modest fraction
    of the armhole so it sets with a flatlock and no puckered seam against the arm."""
    body = build_body()
    armhole = body.edge("armhole").length(0.2)
    biceps = max(280.0, armhole * 1.5)
    half = biceps / 2.0
    cuff_half = max(80.0, half * 0.72)
    top_y = sleeve_length
    cap_h = min(sleeve_length * 0.6, biceps * 0.28)
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    cap = [
        fc.Bezier(p_l, fc.P(-half * 0.7, top_y - cap_h * 0.9),
                  fc.P(-half * 0.3, top_y - cap_h * 0.08), p_top),
        fc.Bezier(p_top, fc.P(half * 0.3, top_y - cap_h * 0.08),
                  fc.P(half * 0.7, top_y - cap_h * 0.9), p_r),
    ]
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r, fc.P(cuff_half, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(cuff_half, 0.0), fc.P(-cuff_half, 0.0))]),
        fc.Edge("under_l", [fc.Line(fc.P(-cuff_half, 0.0), p_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 26.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, top_y - 20.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Soft-set sleeve",
    )


def build_band():
    """The folded neckband: the MEASURED neck run minus a stretch factor so it lies flat
    against the skin, folded to a soft double thickness."""
    stretch = 0.90                                # jersey band drafted 10% short to hug
    ln, w = NECK_RUN * stretch, 46.0
    return fc.Piece(
        "band", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.25, "shoulder match"),
                 fc.Notch("attach", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Soft neckband",
    )


def build():
    pattern = fc.PatternSet("sensory-friendly-tee")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "band":
        pattern.add(build_band())

    if everything:
        # The band rolls into a ring: its side seams close (the ONE seam allowed near
        # the neck, set at centre back away from the throat).
        pattern.declare_seam(("band", "seam_a"), ("band", "seam_b"), tol=0.5)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "modal jersey (OEKO-TEX)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1600 mm width, 78% marker; modal is chosen for a cool, smooth "
                 "hand — a scratchy fibre defeats the whole purpose."},
        {"item": "woolly nylon (flatlock)", "qty": 1, "unit": "cone",
         "note": "flatlock/coverstitch every seam so it lies flat against the skin, no "
                 "raised overlock ridge."},
        {"item": "printable size ink", "qty": 1, "unit": "set",
         "note": "the size prints in the marked inside-hem box — no woven label to itch."},
    ]
    pattern.metadata = {
        "fc400_rank": 374,
        "family": "adaptive",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {"chest": round(HALF_BODY * 4.0, 1),
                        "length": round(tee_length, 1),
                        "neck_scoop": round(neck_scoop, 1)},
        "solved": {
            "neck_run_mm": round(NECK_RUN, 2),
            "band_length_mm": round(NECK_RUN * 0.90, 2),
            "neck_half_mm": round(NECK_HALF, 2),
            "note": "the body is cut as ONE tube (side seams on the fold) so no seam "
                    "rubs; the neckband length is the MEASURED sum of the front and "
                    "back scoops, drafted 10% short to hug flat — a rippled band is "
                    "exactly the edge a sensory-friendly tee cannot have. The front "
                    "scoop is clamped above the armhole base so it never crosses it.",
        },
        "adaptive": {
            "sensory": "no side seams (body is a tube), flatlock everywhere, no back "
                       "label (size printed inside the hem), soft folded neckband set at "
                       "centre back — the whole draft removes skin-contact irritants",
        },
        "hardware": "none — a sensory-friendly tee deliberately carries no hardware "
                    "(no snaps, no zips, nothing hard against the skin); pattern-only.",
    }
    return pattern


result = build()
