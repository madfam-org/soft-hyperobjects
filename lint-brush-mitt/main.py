"""
Fabric Lint-brush Mitt — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #369, pattern-only).

A washable mitt of napped velour that wipes lint, pet hair, and dust off a coat with a
stroke — the reusable answer to the sticky-tape roller. Two mirrored SHELL halves (napped
face out) close around the hand, a CUFF band finishes the wrist, and a hanging TAB lets it
dry between uses.

Drafting note — the seam that must SOLVE: the mitt outline is a rounded capsule — a straight
palm run capped by a semicircle at the fingertips — so its perimeter has no clean closed
form once polygonised. The two shells are the SAME outline mirrored, so their seam matches by
construction, and the cuff band's length is the MEASURED wrist opening the two shells present
when they meet, not a girth formula. The thumb is a marked gusset slit, not a separate piece,
so a beginner can make it flat.

Pieces:
  - shell : one mitt face (cut 2, mirrored); napped side out.
  - cuff  : the wrist band (cut 1).
  - tab   : the hanging loop (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|cuff|tab|set

hand_width = float(PARAM(lambda: hand_width, 110.0))     # across the knuckles
mitt_length = float(PARAM(lambda: mitt_length, 220.0))   # wrist to fingertip
cuff_depth = float(PARAM(lambda: cuff_depth, 55.0))      # wrist band depth
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
hand_width = max(80.0, min(hand_width, 160.0))
mitt_length = max(160.0, min(mitt_length, 300.0))
cuff_depth = max(30.0, min(cuff_depth, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

TIP_R = hand_width / 2.0
# The straight palm run below the fingertip cap; floored so a short mitt on a wide
# hand still has a real straight section (never a negative run folded into a lens).
PALM_RUN = max(30.0, mitt_length - TIP_R)
ARC_SEGS = 18


def _arc(cx, cy, r, a0, a1, n=ARC_SEGS):
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# The capsule outline in local coords: wrist at y=0, palm rises to y=PALM_RUN, then a
# semicircle cap of radius TIP_R centred at (0, PALM_RUN).
_CAP = _arc(0.0, PALM_RUN, TIP_R, 0.0, math.pi)         # right (0) round to left (pi)
CAP_LEN = _poly_len(_CAP)
WRIST_OPENING = hand_width                               # the straight wrist edge


def build_shell():
    """One mitt face (cut 2, mirrored). Edges: wrist (straight), side_l up, the tip
    cap (semicircle), side_r down."""
    edges = [
        fc.Edge("wrist", [fc.Line(fc.P(-TIP_R, 0.0), fc.P(TIP_R, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(TIP_R, 0.0), fc.P(TIP_R, PALM_RUN))]),
        fc.Edge("tip", _lines(_CAP)),
        fc.Edge("side_l", [fc.Line(fc.P(-TIP_R, PALM_RUN), fc.P(-TIP_R, 0.0))]),
    ]
    internals = [
        fc.Internal("thumb-slit",
                    [fc.P(-TIP_R + 6.0, PALM_RUN * 0.30),
                     fc.P(-TIP_R + hand_width * 0.28, PALM_RUN * 0.42)],
                    kind="marking"),
        fc.Internal("nap-direction",
                    [fc.P(0.0, PALM_RUN * 0.4), fc.P(0.0, PALM_RUN * 0.75)],
                    kind="marking"),
    ]
    return fc.Piece(
        "shell", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("wrist", 0.5, "hand centre"),
                 fc.Notch("tip", 0.5, "fingertip centre")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, PALM_RUN + TIP_R - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Mitt shell",
    )


def build_cuff():
    """The wrist band: a rectangle the MEASURED wrist opening wide (x2 for the two
    shells' wrist edges) folded to cuff_depth, its side seams closing on each other."""
    w, h = WRIST_OPENING * 2.0, cuff_depth * 2.0
    return fc.Piece(
        "cuff", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("fold_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.25, "one shell wrist centre"),
                 fc.Notch("attach", 0.75, "other shell wrist centre")],
        grainline=fc.Grainline(fc.P(w * 0.2, h / 2.0), fc.P(w * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Wrist cuff",
    )


TAB_LEN = max(60.0, cuff_depth * 1.6)


def build_tab():
    """The hanging loop, a short strip folded double."""
    ln, w = TAB_LEN, 24.0
    return fc.Piece(
        "tab", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "into the cuff seam")],
        grainline=fc.Grainline(fc.P(12.0, w * 0.5), fc.P(ln - 12.0, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Hanging tab",
    )


def build():
    pattern = fc.PatternSet("lint-brush-mitt")
    everything = target_piece == "set"
    if everything or target_piece == "shell":
        pattern.add(build_shell())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything or target_piece == "tab":
        pattern.add(build_tab())

    if everything:
        # THE solving seams: the two mirrored shells meet along both sides and the tip.
        pattern.declare_seam(("shell", "side_r"), ("shell", "side_l"), tol=0.5)
        pattern.declare_seam(("shell", "tip"), ("shell", "tip"), tol=0.6)
        # The cuff rolls into a tube: its side seams close.
        pattern.declare_seam(("cuff", "seam_a"), ("cuff", "seam_b"), tol=0.5)
        # The cuff attaches to both shells' wrist edges (its attach = 2x wrist).
        pattern.declare_seam(("cuff", "attach"),
                             [("shell", "wrist"), ("shell", "wrist")], tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton velour (napped)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; cut with the NAP running toward the "
                 "fingertips so the stroke lifts lint, not smears it."},
        {"item": "elastic (cuff)", "qty": round(WRIST_OPENING * 1.4), "unit": "mm_length",
         "note": "threads the cuff so the mitt grips the wrist and does not slip."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "turn the mitt so all seams are inside; the napped face works outside."},
    ]
    pattern.metadata = {
        "fc400_rank": 369,
        "family": "care_and_keeping",
        "fabric_hint": "felpa-algodon",
        "finished_mm": {"hand_width": round(hand_width, 1),
                        "mitt_length": round(mitt_length, 1),
                        "cuff_depth": round(cuff_depth, 1)},
        "solved": {
            "tip_cap_radius_mm": round(TIP_R, 2),
            "palm_run_mm": round(PALM_RUN, 2),
            "tip_cap_length_mm": round(CAP_LEN, 2),
            "wrist_opening_mm": round(WRIST_OPENING, 2),
            "note": "the mitt is a capsule — a straight palm run capped by a measured "
                    "semicircle; the palm run is floored at 30 mm so a short mitt on a "
                    "wide hand keeps a real straight section instead of folding to a lens.",
        },
        "hardware": "none — a napped mitt needs no hardware; pattern-only by design, "
                    "deepening the thin care_keeping family.",
    }
    return pattern


result = build()
