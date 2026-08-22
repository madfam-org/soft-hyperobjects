"""
Weekender Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #207, y4d bag feet).

A boxed weekender on the dopp-kit precedent, scaled to overnight luggage: a wrap BODY
(front + base + back folded at the base), two END gussets that give it its rigid box
shape, a top zip, and two carry HANDLES. Bag feet are riveted through the base panel so a
loaded bag never sits its fabric on the floor — the foot is a Yantra4D solid (`bag-feet`;
see the manifest's notion.hardware_ref). The foot is POINT-PLACED hardware: it has no
sewn flange, so it needs a drilled bore position, not an edge coupling.

The seam that must SOLVE: the end gussets are drafted with a softly curved top edge (the
box's rounded corner at the zip), so their attach run is a Bezier, not the flat height.
The body's side edges must match that measured run — so the body's flat panel height is
derived FROM the measured gusset run rather than from `2*height + depth`.

Pieces:
  - body   : front + base + back as one fold-at-base panel; the top edges take the zip.
  - end    : the end gusset (cut 2) that boxes the bag.
  - handle : the carry handle (cut 2).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

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

bag_length = float(PARAM(lambda: bag_length, 520.0))     # length (the zip runs along this)
bag_height = float(PARAM(lambda: bag_height, 300.0))     # front-face height
bag_depth = float(PARAM(lambda: bag_depth, 260.0))       # box depth (end-gusset width)
handle_length = float(PARAM(lambda: handle_length, 620.0))  # carry-handle cut length
handle_width = float(PARAM(lambda: handle_width, 38.0))     # carry-handle width
foot_diameter = float(PARAM(lambda: foot_diameter, 18.0))   # bag-foot flange diameter
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_length = max(320.0, min(bag_length, 750.0))
bag_height = max(180.0, min(bag_height, 460.0))
bag_depth = max(120.0, min(bag_depth, 400.0))
handle_length = max(300.0, min(handle_length, 900.0))
handle_width = max(20.0, min(handle_width, 60.0))
foot_diameter = max(10.0, min(foot_diameter, 34.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BW = bag_length
CORNER_BULGE = 0.10      # how softly the end gusset crowns toward the zip


def _end_attach_edge(bulge):
    """One end gusset's attach run: up one side, over the softly crowned top, down the
    other — i.e. attach_l + top + attach_r. This is the run the body's SIDE edge must
    match, because the gusset's fourth edge (`bottom`) lies along the base fold and is
    not sewn to the body's side at all.
    """
    w, h = bag_depth, bag_height
    return fc.Edge("attach", [
        fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h)),
        fc.curve_through(fc.P(0.0, h), fc.P(w, h), bulge=bulge, side=1.0),
        fc.Line(fc.P(w, h), fc.P(w, 0.0)),
    ])


# The crowned top means the gusset's top run is LONGER than bag_depth, so the body
# panel height is NOT 2*height + depth. Measure the gusset run and use it directly.
END_ATTACH = _end_attach_edge(CORNER_BULGE).length(0.02)
BH = END_ATTACH                      # body side edge == one gusset's attach run
BASE_RUN = END_ATTACH - 2.0 * bag_height    # the crowned top's measured run


def build_body():
    """Front + base + back as one fold-at-base panel. `side_l`/`side_r` take the end
    gussets; `zip_front`/`zip_back` are the two zip-tape edges."""
    edges = [
        fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("zip_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),
        fc.Edge("side_r", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("zip_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
    ]
    y_fb = bag_height                          # front panel ends, base begins
    y_bb = bag_height + BASE_RUN               # base ends, back panel begins
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(BW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(BW, y_bb)], kind="marking"),
    ]
    # Bag-foot bores: four, inset from the base panel's corners. Point-placed hardware —
    # a drilled position, not a sewn edge.
    inset = max(foot_diameter * 1.6, 26.0)
    for x in (inset, BW - inset):
        for y in (y_fb + inset, y_bb - inset):
            internals.append(fc.Internal("foot-bore",
                                         [fc.P(x - foot_diameter / 2.0, y),
                                          fc.P(x + foot_diameter / 2.0, y)], kind="drill"))
            internals.append(fc.Internal("foot-bore",
                                         [fc.P(x, y - foot_diameter / 2.0),
                                          fc.P(x, y + foot_diameter / 2.0)], kind="drill"))
    # Handle runs on the front and back faces.
    for x in (BW * 0.5 - bag_length * 0.16, BW * 0.5 + bag_length * 0.16):
        internals.append(fc.Internal("handle-run",
                                     [fc.P(x, 20.0), fc.P(x, y_fb - 20.0)], kind="marking"))
        internals.append(fc.Internal("handle-run",
                                     [fc.P(x, y_bb + 20.0), fc.P(x, BH - 20.0)],
                                     kind="marking"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_l", y_fb / BH, "front base fold"),
                 fc.Notch("side_l", y_bb / BH, "back base fold")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 40.0), fc.P(BW * 0.5, BH - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (front + base + back)",
    )


def build_end():
    """One end gusset (cut 2): bag_depth wide, bag_height tall, softly crowned toward the
    zip. Its `attach` run is what the body's side edges must match."""
    w, h = bag_depth, bag_height
    edges = [
        fc.Edge("attach_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.curve_through(fc.P(0.0, h), fc.P(w, h),
                                         bulge=CORNER_BULGE, side=1.0)]),
        fc.Edge("attach_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "end",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "base centre"),
                 fc.Notch("top", 0.5, "zip centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="End Gusset",
    )


def build_handle():
    """A carry handle (cut 2)."""
    ln, w = handle_length, handle_width
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
    pattern = fc.PatternSet("weekender-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "end":
        pattern.add(build_end())
    if all_pieces or target_piece == "handle":
        pattern.add(build_handle())

    if all_pieces:
        # Each body side takes one end gusset's attach run: side + crowned top + side.
        # The gusset's `bottom` lies along the base fold and is NOT part of this seam.
        pattern.declare_seam(("body", "side_l"),
                             [("end", "attach_l"), ("end", "top"), ("end", "attach_r")],
                             tol=1.0)
        pattern.declare_seam(("body", "side_r"),
                             [("end", "attach_l"), ("end", "top"), ("end", "attach_r")],
                             tol=1.0)
    if all_pieces or target_piece == "body":
        # Front and back zip tapes are the same run by construction.
        pattern.declare_seam(("body", "zip_front"), ("body", "zip_back"), tol=0.5)
    if all_pieces or target_piece == "end":
        # The two end gussets are identical — the box is symmetric.
        pattern.declare_seam(("end", "attach_l"), ("end", "attach_r"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "waxed canvas or heavy twill", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 78% marker; interline the base so the feet sit flat."},
        {"item": "bag feet", "qty": 4, "unit": "count",
         "note": "Yantra4D bag-feet (see notion.hardware_ref); POINT-PLACED through the "
                 f"marked base bores, {foot_diameter:.0f} mm flange. Feet are what keep a "
                 "loaded weekender's fabric off wet floors."},
        {"item": "top zip", "qty": 1, "unit": "count",
         "note": f"≈ {bag_length:.0f} mm along the two zip-tape edges."},
        {"item": "webbing or leather for handles", "qty": round(2.0 * handle_length),
         "unit": "mm_length", "note": f"{handle_width:.0f} mm wide, two handles."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "box the ends to the body and box-and-cross the handle runs."},
    ]
    pattern.metadata = {
        "fc300_rank": 207,
        "family": "bags_luggage",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"length": round(bag_length, 1), "height": round(bag_height, 1),
                        "depth": round(bag_depth, 1)},
        "solved": {
            "end_attach_run_mm": round(END_ATTACH, 2),
            "body_panel_height_mm": round(BH, 2),
            "corner_bulge": CORNER_BULGE,
            "note": "the end gusset is crowned toward the zip, so its attach run is a "
                    "Bezier and NOT 2*height+depth. The body panel height is derived from "
                    "the MEASURED gusset run, so the box seams verify.",
        },
        "hardware": "base feet via Yantra4D (notion.hardware_ref -> bag-feet); POINT/SLOT "
                    "placement — the foot has no sewn flange, so it takes a drilled bore "
                    "position, not an edge coupling",
    }
    return pattern


result = build()
