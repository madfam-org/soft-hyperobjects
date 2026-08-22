"""
Jewelry Roll — Fashion Cabinet Care & Keeping Cartridge (FC-300 rank #256,
Yantra4D-bridged D-ring).

The travelling jewelry roll: a padded rectangle that lays flat, takes a row of zip and
slip pockets and a ring bar, then rolls up on itself and cinches with a webbing tie
through a D-ring. Chains do not tangle because each one gets its own compartment and the
roll's curl keeps them under tension.

Drafting note — the seam that must SOLVE: a roll is a SPIRAL, not a cylinder — each wrap
sits one fabric-thickness further out than the last. The outer shell must therefore be
LONGER than the lining by the spiral's accumulated circumference difference, or the
finished roll cups and the edges will not align. This cartridge computes that difference
by walking an Archimedean spiral numerically and MEASURING it, then cuts `shell` that
much longer than `lining` and declares the seam with that difference as its `ease`.

Pieces:
  - shell   : the outer face (cut 1) — longer, by the measured spiral allowance.
  - lining  : the inner face carrying the pockets (cut 1).
  - pocket  : the pocket band that runs across the lining (cut 1).
  - tie     : the webbing cinch strap that passes the D-ring (cut 1).

Hardware: `d-ring` (Yantra4D). Its `bar_edge` flange is driven by `webbing`, mapped from
this cartridge's `tie_width` — which also drives the garment's own `tie_anchor` interface.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|lining|pocket|tie|set

roll_width = float(PARAM(lambda: roll_width, 300.0))       # the roll's axis length
roll_length = float(PARAM(lambda: roll_length, 240.0))     # unrolled, the rolling direction
pocket_depth = float(PARAM(lambda: pocket_depth, 85.0))    # finished pocket height
tie_width = float(PARAM(lambda: tie_width, 20.0))          # drives the Yantra4D D-ring
batting_thickness = float(PARAM(lambda: batting_thickness, 5.0))  # padded loft
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
roll_width = max(180.0, min(roll_width, 460.0))
roll_length = max(150.0, min(roll_length, 400.0))
pocket_depth = max(40.0, min(pocket_depth, 140.0))
tie_width = max(10.0, min(tie_width, 40.0))
batting_thickness = max(1.0, min(batting_thickness, 15.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# A pocket band cannot be taller than the roll it sits on.
pocket_depth = min(pocket_depth, roll_length * 0.45)

CORNER_SEGS = 12        # the roll's rounded ends are a measured arc
CORNER_R = min(24.0, roll_length * 0.12, roll_width * 0.12)


def _arc(cx, cy, r, a0, a1, n=CORNER_SEGS):
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def _poly_len(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


def _lines(pts):
    return [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]


# ── The spiral allowance: MEASURED, not assumed ──────────────────────────────
def _spiral_allowance(inner_len, thickness):
    """How much longer the OUTER face of a roll must be than the inner face.

    Walk an Archimedean spiral r(θ) = r0 + (t/2π)·θ — one fabric thickness gained
    per turn — accumulating arc length until the INNER radius' path has covered
    `inner_len`. The outer path, offset by `thickness`, is walked over the same
    θ range. The difference is the allowance. There is a closed form for a pure
    spiral, but the roll's core radius and its partial final turn make the honest
    answer a numeric walk.
    """
    r0 = max(thickness * 2.0, 6.0)          # the roll's core radius when cinched
    a = thickness / (2.0 * math.pi)         # radial gain per radian
    steps = 4000
    dtheta = 0.004
    inner = outer = 0.0
    theta = 0.0
    for _ in range(steps):
        r_in = r0 + a * theta
        r_out = r_in + thickness
        # ds = sqrt(r² + (dr/dθ)²) dθ for a polar curve
        inner += math.sqrt(r_in * r_in + a * a) * dtheta
        outer += math.sqrt(r_out * r_out + a * a) * dtheta
        theta += dtheta
        if inner >= inner_len:
            break
    return outer - inner, theta


SPIRAL_EASE, SPIRAL_THETA = _spiral_allowance(roll_length, batting_thickness)
SHELL_LENGTH = roll_length + SPIRAL_EASE


def _rounded_rect(w, h, r, tag_left, tag_right):
    """A rounded rectangle as four named edges: bottom, `tag_right`, top, `tag_left`.

    Corners are measured arcs, so the two long edges are genuinely shorter than `w`
    and the two short edges shorter than `h` — the seam check sees the truth.
    """
    br = _arc(w - r, r, r, -math.pi / 2.0, 0.0)
    tr = _arc(w - r, h - r, r, 0.0, math.pi / 2.0)
    tl = _arc(r, h - r, r, math.pi / 2.0, math.pi)
    bl = _arc(r, r, r, math.pi, 3.0 * math.pi / 2.0)
    bottom = [fc.P(r, 0.0), fc.P(w - r, 0.0)] + br[1:]
    right = [br[-1]] + [fc.P(w, h - r)] + tr[1:]
    top = [tr[-1], fc.P(r, h)] + tl[1:]
    left = [tl[-1], fc.P(0.0, r)] + bl[1:]
    return [
        fc.Edge("bottom", _lines(bottom)),
        fc.Edge(tag_right, _lines(right)),
        fc.Edge("top", _lines(top)),
        fc.Edge(tag_left, _lines(left)),
    ]


def build_shell():
    """The outer face — SHELL_LENGTH tall, the measured spiral allowance longer
    than the lining, so the finished roll lies flat instead of cupping."""
    edges = _rounded_rect(roll_width, SHELL_LENGTH, CORNER_R, "edge_l", "edge_r")
    return fc.Piece(
        "shell",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "roll start — matches lining"),
                 fc.Notch("top", 0.5, "roll finish")],
        grainline=fc.Grainline(fc.P(roll_width * 0.5, 20.0),
                               fc.P(roll_width * 0.5, SHELL_LENGTH - 20.0)),
        internals=[fc.Internal("d-ring-tab",
                               [fc.P(roll_width * 0.5 - tie_width / 2.0, 10.0),
                                fc.P(roll_width * 0.5 + tie_width / 2.0, 10.0)],
                               kind="drill"),
                   fc.Internal("quilt-lines",
                               [fc.P(0.0, SHELL_LENGTH * 0.5),
                                fc.P(roll_width, SHELL_LENGTH * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Outer shell (spiral-eased)",
    )


def build_lining():
    """The inner face: the pockets and the ring bar live here."""
    edges = _rounded_rect(roll_width, roll_length, CORNER_R, "edge_l", "edge_r")
    internals = [
        fc.Internal("ring-bar",
                    [fc.P(20.0, roll_length - pocket_depth - 30.0),
                     fc.P(roll_width - 20.0, roll_length - pocket_depth - 30.0)],
                    kind="marking"),
        fc.Internal("pocket-attach",
                    [fc.P(0.0, pocket_depth), fc.P(roll_width, pocket_depth)],
                    kind="marking"),
    ]
    # Pocket dividers: one per 70 mm of width, so bracelets do not share a slot.
    slots = max(2, int(roll_width // 70.0))
    for i in range(1, slots):
        x = roll_width * i / slots
        internals.append(fc.Internal("pocket-divider",
                                     [fc.P(x, 0.0), fc.P(x, pocket_depth)],
                                     kind="marking"))
    return fc.Piece(
        "lining",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "roll start — matches shell"),
                 fc.Notch("top", 0.5, "roll finish")],
        grainline=fc.Grainline(fc.P(roll_width * 0.5, 20.0),
                               fc.P(roll_width * 0.5, roll_length - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Lining (pockets + ring bar)",
    )


def build_pocket():
    """The pocket band: cut to twice the finished depth and folded, so its top edge
    is a clean fold rather than a bulky turned hem against the jewelry."""
    w, h = roll_width, pocket_depth * 2.0
    return fc.Piece(
        "pocket",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("fold_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        cut=fc.CutSpec(quantity=1),
        label="Pocket band (cut double, folded)",
    )


# The tie must wrap the finished roll's girth once and leave a tail to thread back.
ROLL_GIRTH = 2.0 * math.pi * (batting_thickness * 2.0 + 6.0 + SPIRAL_THETA
                              * batting_thickness / (2.0 * math.pi))
TIE_LENGTH = max(260.0, ROLL_GIRTH * 1.15 + 180.0)


def build_tie():
    """The webbing cinch: passes the D-ring and folds back on itself."""
    ln, w = TIE_LENGTH, tie_width
    return fc.Piece(
        "tie",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("ring_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", 0.12, "fold back through the D-ring")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Cinch tie (D-ring)",
    )


def build():
    pattern = fc.PatternSet("jewelry-roll")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "lining":
        pattern.add(build_lining())
    if all_pieces or target_piece == "pocket":
        pattern.add(build_pocket())
    if all_pieces or target_piece == "tie":
        pattern.add(build_tie())

    if all_pieces:
        # THE solving seam: shell and lining sew edge to edge down both sides, but
        # the shell is longer by the MEASURED spiral allowance — declared as ease,
        # not hidden in a fudge factor.
        pattern.declare_seam(("shell", "edge_r"), ("lining", "edge_r"),
                             tol=0.6, ease=SPIRAL_EASE)
        pattern.declare_seam(("shell", "edge_l"), ("lining", "edge_l"),
                             tol=0.6, ease=SPIRAL_EASE)
        # The roll's two ends match exactly — the ease is all in the rolling direction.
        pattern.declare_seam(("shell", "bottom"), ("lining", "bottom"), tol=0.5)
        pattern.declare_seam(("shell", "top"), ("lining", "top"), tol=0.5)
        # The pocket band is cut to the flat roll width, while the lining's bottom
        # edge runs through two measured corner arcs and is therefore SHORTER. The
        # difference is the band's overhang into the side seams — declared as ease
        # from the measured edge, never assumed.
        lining_bottom = pattern.piece("lining").edge("bottom").length()
        pattern.declare_seam(("pocket", "attach"), ("lining", "bottom"),
                             tol=0.6, ease=roll_width - lining_bottom)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "silk dupioni or cotton sateen (shell + lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 70% marker; a smooth lining is what stops "
                 "chains catching."},
        {"item": "cotton batting", "qty": round(roll_width * roll_length / 1000.0),
         "unit": "cm2",
         "note": f"{batting_thickness:.1f} mm loft — the padding that also sets the "
                 f"spiral allowance."},
        {"item": "D-ring", "qty": 1, "unit": "count",
         "note": "Yantra4D d-ring (see notion.hardware_ref); its bar_edge takes the "
                 f"same {tie_width:.0f} mm tie webbing."},
        {"item": "webbing or grosgrain tie", "qty": round(TIE_LENGTH), "unit": "mm_length",
         "note": f"{tie_width:.0f} mm wide."},
    ]
    pattern.metadata = {
        "fc300_rank": 256,
        "family": "care_and_keeping",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {"width": round(roll_width, 1),
                        "length": round(roll_length, 1),
                        "pocket_depth": round(pocket_depth, 1)},
        "solved": {
            "spiral_ease_mm": round(SPIRAL_EASE, 2),
            "spiral_theta_rad": round(SPIRAL_THETA, 3),
            "spiral_turns": round(SPIRAL_THETA / (2.0 * math.pi), 2),
            "shell_length_mm": round(SHELL_LENGTH, 2),
            "lining_length_mm": round(roll_length, 2),
            "corner_radius_mm": round(CORNER_R, 2),
            "note": "the outer shell is cut longer than the lining by the MEASURED "
                    f"Archimedean-spiral allowance for {SPIRAL_THETA / (2.0 * math.pi):.2f} "
                    f"turns at {batting_thickness:.1f} mm loft — "
                    "walked numerically, then declared as the seam's ease.",
        },
        "hardware": "cinch D-ring via Yantra4D (notion.hardware_ref -> d-ring); "
                    "webbing = tie_width",
    }
    return pattern


result = build()
