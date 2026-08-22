"""
Roll-Top Backpack — Fashion Cabinet Bag Cartridge (FC-300 rank #203, y4d side-release).

A roll-top rucksack: a BODY panel (front + back cut as one, folded at the base) with a
roll extension above the load line, a BASE panel that boxes the bottom, two curved
SHOULDER straps, and a webbing closure strap that buckles across the rolled top. The
buckle is a Yantra4D solid (`side-release-buckle`; see the manifest's notion.hardware_ref)
whose webbing channel takes this pack's `webbing_width`.

The seam that must SOLVE: the base panel is an oval (a 48-segment rounded rectangle), and
the body's base edge has to wrap that oval's whole perimeter. Rather than assume the two
match, the body's wrap width is derived FROM the measured base perimeter, so the
body-to-base seam verifies exactly.

Pieces:
  - body     : front + back as one fold-at-top-of-roll panel; the base edge takes the base.
  - base     : the oval base panel that boxes the bottom.
  - shoulder : a curved shoulder strap (cut 2).
  - closure  : the webbing closure strap that runs to the buckle.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|base|shoulder|closure|set

pack_width = float(PARAM(lambda: pack_width, 300.0))     # base width (across the back)
pack_depth = float(PARAM(lambda: pack_depth, 150.0))     # base depth (front to back)
pack_height = float(PARAM(lambda: pack_height, 440.0))   # height to the load line
roll_height = float(PARAM(lambda: roll_height, 200.0))   # extension above the load line
webbing_width = float(PARAM(lambda: webbing_width, 25.0))  # closure/buckle webbing width
strap_length = float(PARAM(lambda: strap_length, 700.0))   # shoulder strap length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
pack_width = max(200.0, min(pack_width, 420.0))
pack_depth = max(90.0, min(pack_depth, 260.0))
pack_height = max(280.0, min(pack_height, 620.0))
roll_height = max(80.0, min(roll_height, 340.0))
webbing_width = max(15.0, min(webbing_width, 50.0))
strap_length = max(400.0, min(strap_length, 950.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

SEGS = 48                      # polygon approximation of the rounded base
CORNER = min(pack_depth, pack_width) * 0.5   # base corner radius (a full stadium oval)


def _base_points():
    """A stadium / rounded-rectangle base: two straight runs joined by two semicircles,
    sampled as a closed 48-point polygon. Returns the point ring (open, CCW)."""
    r = CORNER
    straight = max(pack_width - 2.0 * r, 0.0)
    hs = straight / 2.0
    quarter = SEGS // 4
    pts = []
    # Right cap: -90 deg to +90 deg about (+hs, 0).
    for i in range(2 * quarter):
        a = -math.pi / 2.0 + math.pi * i / (2 * quarter)
        pts.append(fc.P(hs + r * math.cos(a), r * math.sin(a)))
    # Left cap: +90 deg to +270 deg about (-hs, 0).
    for i in range(2 * quarter):
        a = math.pi / 2.0 + math.pi * i / (2 * quarter)
        pts.append(fc.P(-hs + r * math.cos(a), r * math.sin(a)))
    return pts


_BASE_PTS = _base_points()
BASE_PERIMETER = sum(_BASE_PTS[i].distance(_BASE_PTS[(i + 1) % len(_BASE_PTS)])
                     for i in range(len(_BASE_PTS)))
# The body wraps the base: its base edge must equal the measured base perimeter.
WRAP = BASE_PERIMETER
BODY_H = pack_height + roll_height


def build_body():
    """The pack wall: WRAP wide (it rolls into the tube) x (height + roll) tall.

    `base_edge` takes the base panel; `wrap_a`/`wrap_b` meet at the back seam. The load
    line and the roll folds are internal markings.
    """
    w, h = WRAP, BODY_H
    edges = [
        fc.Edge("wrap_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("roll_top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("wrap_b", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("base_edge", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("load-line", [fc.P(0.0, pack_height), fc.P(w, pack_height)],
                    kind="marking"),
    ]
    # Roll folds every webbing-ish bite up the extension (three rolls is the norm).
    for k in (1, 2, 3):
        y = pack_height + roll_height * k / 4.0
        internals.append(fc.Internal("roll-fold", [fc.P(0.0, y), fc.P(w, y)],
                                     kind="marking"))
    # Shoulder-strap anchor runs on what becomes the back panel (centred on the wrap).
    for x in (w * 0.5 - pack_width * 0.28, w * 0.5 + pack_width * 0.28):
        internals.append(fc.Internal("strap-anchor",
                                     [fc.P(x, h - 30.0), fc.P(x, h - 30.0 - webbing_width)],
                                     kind="drill"))
    # Closure-strap anchor: where the buckle webbing is bar-tacked at the load line.
    internals.append(fc.Internal("closure-anchor",
                                 [fc.P(w * 0.5 - webbing_width / 2.0, pack_height),
                                  fc.P(w * 0.5 + webbing_width / 2.0, pack_height)],
                                 kind="drill"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base_edge", 0.5, "centre front"),
                 fc.Notch("roll_top", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, 40.0), fc.P(w * 0.5, h - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (wall + roll extension)",
    )


def build_base():
    """The oval base panel, split into two named half-perimeter edges so the body's base
    edge has a seam reference."""
    pts = _BASE_PTS + [_BASE_PTS[0]]
    n = len(_BASE_PTS)
    half = n // 2
    edges = [
        fc.Edge("rim_a", [fc.Line(pts[i], pts[i + 1]) for i in range(half)]),
        fc.Edge("rim_b", [fc.Line(pts[i], pts[i + 1]) for i in range(half, n)]),
    ]
    return fc.Piece(
        "base",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("rim_a", 0.0, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, -CORNER * 0.6), fc.P(0.0, CORNER * 0.6)),
        cut=fc.CutSpec(quantity=1),
        label="Base Panel",
    )


def build_shoulder():
    """A curved shoulder strap (cut 2): wide at the shoulder, tapering to the webbing
    width at the buckle end so it can feed the adjuster."""
    ln = strap_length
    wide = max(webbing_width * 2.4, 55.0)
    narrow = webbing_width
    top_l = fc.P(0.0, wide)
    top_r = fc.P(ln, narrow)
    return fc.Piece(
        "shoulder",
        [
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, 0.0), top_l)]),
            fc.Edge("outer", [fc.curve_through(top_l, top_r, bulge=0.06, side=1.0)]),
            fc.Edge("buckle_end", [fc.Line(top_r, fc.P(ln, 0.0))]),
            fc.Edge("inner", [fc.curve_through(fc.P(ln, 0.0), fc.P(0.0, 0.0),
                                               bulge=0.04, side=1.0)]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("outer", 0.5, "shoulder crest")],
        grainline=fc.Grainline(fc.P(ln * 0.2, narrow * 0.5), fc.P(ln * 0.8, narrow * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shoulder Strap",
    )


def build_closure():
    """The webbing closure strap that runs from the load-line anchor, over the rolled
    top, to the side-release buckle. Cut at the webbing width the buckle expects."""
    ln = pack_depth + roll_height + 180.0
    w = webbing_width
    return fc.Piece(
        "closure",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Closure Strap (webbing)",
    )


def build():
    pattern = fc.PatternSet("roll-top-backpack")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "base":
        pattern.add(build_base())
    if all_pieces or target_piece == "shoulder":
        pattern.add(build_shoulder())
    if all_pieces or target_piece == "closure":
        pattern.add(build_closure())

    if all_pieces or target_piece == "body":
        # The back seam of the tube: wrap_a meets wrap_b.
        pattern.declare_seam(("body", "wrap_a"), ("body", "wrap_b"), tol=1.0)
    if all_pieces:
        # The body's base edge wraps the whole oval base perimeter.
        pattern.declare_seam(("body", "base_edge"),
                             [("base", "rim_a"), ("base", "rim_b")], tol=1.0)
    if all_pieces or target_piece == "closure":
        # The closure webbing's two long edges are the same run (a folded/edge-bound tape).
        pattern.declare_seam(("closure", "bottom"), ("closure", "top"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "X-Pac, cordura or waxed canvas", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 78% marker; a roll-top wants a fabric that creases."},
        {"item": "webbing", "qty": round(2.0 * (pack_depth + roll_height + 180.0) + 400.0),
         "unit": "mm_length",
         "note": f"{webbing_width:.0f} mm webbing: the closure straps + strap anchors."},
        {"item": "side-release buckle", "qty": 2, "unit": "count",
         "note": "Yantra4D side-release-buckle (see notion.hardware_ref); its webbing "
                 f"channel takes the same {webbing_width:.0f} mm webbing as the closure."},
        {"item": "closed-cell foam", "qty": 2, "unit": "count",
         "note": "pad the shoulder straps; they carry the whole load."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "box-and-cross the strap anchors; a roll-top fails at its anchors first."},
    ]
    pattern.metadata = {
        "fc300_rank": 203,
        "family": "bags_luggage",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(pack_width, 1), "depth": round(pack_depth, 1),
                        "height": round(pack_height, 1), "roll": round(roll_height, 1)},
        "solved": {
            "base_polygon_points": len(_BASE_PTS),
            "base_perimeter_mm": round(BASE_PERIMETER, 2),
            "body_wrap_mm": round(WRAP, 2),
            "note": "body wrap = the MEASURED oval base perimeter, so the body-to-base "
                    "seam matches exactly instead of carrying the chord error.",
        },
        "closure": f"roll {roll_height:.0f} mm down in three folds, then buckle across.",
        "hardware": "closure buckles via Yantra4D (notion.hardware_ref -> "
                    "side-release-buckle); the buckle channel and the closure strap share "
                    "webbing_width",
    }
    return pattern


result = build()
