"""
Duffel Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #201, Yantra4D-bridged strap ring).

The classic cylinder duffel: a rectangular BODY that wraps into a tube, two circular
END panels that close the cylinder, a top ZIP opening cut into the body, and two webbing
HANDLES. Strap rings anchor the removable shoulder strap at the two ends — the ring is a
Yantra4D solid (`strap-ring`; see the manifest's notion.hardware_ref) whose webbing
channel shares this bag's `webbing_width`. Fashion Cabinet owns the bag; Yantra4D owns
the ring.

Drafting note — the seam that must SOLVE: an end panel is drafted as a 48-segment
polygon, whose perimeter is slightly under the true circle 2*pi*r. The body's wrap
length is therefore taken FROM the measured polygon perimeter, not from 2*pi*r, so the
body-to-end seam matches exactly rather than within a chord-error fudge.

Pieces:
  - body   : the cylinder wall; wraps so `wrap_a` meets `wrap_b` at the base seam.
  - end    : circular end panel (cut 2) sewn to the body's two circumference edges.
  - handle : webbing carry handle (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|end|handle|set

bag_length = float(PARAM(lambda: bag_length, 550.0))     # cylinder length (end to end)
bag_diameter = float(PARAM(lambda: bag_diameter, 280.0))  # cylinder diameter
webbing_width = float(PARAM(lambda: webbing_width, 38.0))  # handle/strap webbing width
handle_length = float(PARAM(lambda: handle_length, 620.0))  # carry-handle cut length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_length = max(300.0, min(bag_length, 900.0))
bag_diameter = max(180.0, min(bag_diameter, 420.0))
webbing_width = max(20.0, min(webbing_width, 50.0))
handle_length = max(300.0, min(handle_length, 900.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SIDES = 48                       # polygon approximation of the circular end panels
R_END = bag_diameter / 2.0


def _arc_points(cx, cy, r, a0, a1, n):
    """n+1 points along the arc from a0 to a1 (radians) on a circle at (cx, cy)."""
    return [fc.P(cx + r * math.cos(a0 + (a1 - a0) * i / n),
                 cy + r * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


# The measured perimeter of the 48-gon end — the body wrap must equal THIS, not 2*pi*r.
_END_PTS = _arc_points(0.0, 0.0, R_END, 0.0, 2.0 * math.pi, SIDES)
END_PERIMETER = sum(_END_PTS[i].distance(_END_PTS[i + 1]) for i in range(SIDES))
WRAP = END_PERIMETER              # body width = the exact circumference it sews to


def build_body():
    """The cylinder wall: WRAP wide (it rolls into the tube) x bag_length tall.

    `circ_bottom` / `circ_top` are the two circumference edges that take the end
    panels; `wrap_a` / `wrap_b` meet each other at the base seam of the tube.
    The top zip opening is marked as an internal placement line running the
    length of the body, offset to what becomes the top of the cylinder.
    """
    w, h = WRAP, bag_length
    edges = [
        fc.Edge("wrap_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("circ_top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("wrap_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("circ_bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    zip_inset = 60.0
    internals = [
        fc.Internal("zip-opening",
                    [fc.P(w * 0.5, zip_inset), fc.P(w * 0.5, h - zip_inset)],
                    kind="marking"),
    ]
    # Handle attachment runs: two per face, straddling the zip line.
    for x in (w * 0.5 - bag_diameter * 0.35, w * 0.5 + bag_diameter * 0.35):
        internals.append(fc.Internal("handle-run",
                                     [fc.P(x, h * 0.22), fc.P(x, h * 0.78)],
                                     kind="marking"))
    # Strap-ring anchor tabs sit at the two ends of the base seam.
    for y in (webbing_width, h - webbing_width):
        internals.append(fc.Internal("ring-anchor",
                                     [fc.P(6.0, y), fc.P(6.0 + webbing_width, y)],
                                     kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("circ_bottom", 0.5, "cylinder top centre"),
                 fc.Notch("circ_top", 0.5, "cylinder top centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 40.0), fc.P(w * 0.5, h - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (cylinder wall)",
    )


def build_end():
    """A circular end panel (cut 2), split into two named half-circumference edges so
    the body's two circumference edges each have a seam reference."""
    pts = _END_PTS
    half = SIDES // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, SIDES)]),
    ]
    return fc.Piece(
        "end",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "cylinder top centre")],
        grainline=fc.Grainline(fc.P(0.0, -R_END * 0.6), fc.P(0.0, R_END * 0.6)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="End Panel",
    )


def build_handle():
    """A webbing carry handle (cut 2), webbing_width wide."""
    ln, w = handle_length, webbing_width
    return fc.Piece(
        "handle",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Carry Handle",
    )


def build():
    pattern = fc.PatternSet("duffel-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "end":
        pattern.add(build_end())
    if all_pieces or target_piece == "handle":
        pattern.add(build_handle())

    if all_pieces or (target_piece == "body"):
        # The tube's base seam: wrap_a meets wrap_b (own mirror of the same panel).
        pattern.declare_seam(("body", "wrap_a"), ("body", "wrap_b"), tol=1.0)
    if all_pieces:
        # Each circumference edge takes one end panel: the full 48-gon rim.
        pattern.declare_seam(("body", "circ_bottom"),
                             [("end", "rim_a"), ("end", "rim_b")], tol=1.0)
        pattern.declare_seam(("body", "circ_top"),
                             [("end", "rim_a"), ("end", "rim_b")], tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "cordura or waxed canvas", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 78% marker; a coated lining keeps the cylinder crisp."},
        {"item": "webbing", "qty": round(2.0 * handle_length + 400.0), "unit": "mm_length",
         "note": f"{webbing_width:.0f} mm webbing: two handles + the ring anchor tabs."},
        {"item": "strap ring", "qty": 2, "unit": "count",
         "note": "Yantra4D strap-ring (see notion.hardware_ref); its webbing channel takes "
                 f"the same {webbing_width:.0f} mm webbing as the anchor tabs."},
        {"item": "top zip", "qty": 1, "unit": "count",
         "note": f"≈ {bag_length - 120.0:.0f} mm along the marked zip opening."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the handle runs and the ring anchors; they carry the load."},
    ]
    pattern.metadata = {
        "fc300_rank": 201,
        "family": "bags_luggage",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"length": round(bag_length, 1),
                        "diameter": round(bag_diameter, 1)},
        "solved": {
            "end_polygon_sides": SIDES,
            "end_perimeter_mm": round(END_PERIMETER, 2),
            "true_circle_mm": round(2.0 * math.pi * R_END, 2),
            "body_wrap_mm": round(WRAP, 2),
            "note": "body wrap = the MEASURED 48-gon end perimeter, so the body-to-end "
                    "seam matches exactly instead of carrying the chord error.",
        },
        "hardware": "strap rings via Yantra4D (notion.hardware_ref -> strap-ring); the ring's "
                    "webbing channel and the bag's anchor tabs share webbing_width",
    }
    return pattern


result = build()
