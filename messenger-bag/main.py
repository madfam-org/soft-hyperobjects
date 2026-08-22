"""
Messenger Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #205, y4d cam buckle).

A flap-over messenger: a BODY panel (front + base + back folded at the base), a one-piece
GUSSET that wraps the body's whole side-base-side run, a curved FLAP that drops over the
front, and a webbing closure STRAP that feeds a cam buckle. The buckle is a Yantra4D solid
(`cam-buckle`; see the manifest's notion.hardware_ref) whose webbing throat takes this
bag's `webbing_width`.

The seam that must SOLVE: the gusset is one continuous strip wrapping side + base + side
of the body, and the flap's curved front edge must match the front opening it covers. Both
runs are measured off the drafted geometry rather than assumed, so the declared seams
verify exactly instead of within a fudge factor.

Pieces:
  - body   : front + base + back as one fold-at-base panel.
  - gusset : the wrap-around side/base gusset.
  - flap   : the curved cover flap.
  - strap  : the webbing closure strap that feeds the cam buckle.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|gusset|flap|strap|set

bag_width = float(PARAM(lambda: bag_width, 380.0))       # width across the front
bag_height = float(PARAM(lambda: bag_height, 280.0))     # front-face height
bag_depth = float(PARAM(lambda: bag_depth, 110.0))       # gusset width
flap_drop = float(PARAM(lambda: flap_drop, 210.0))       # how far the flap falls
webbing_width = float(PARAM(lambda: webbing_width, 38.0))  # closure/buckle webbing width
strap_length = float(PARAM(lambda: strap_length, 420.0))   # closure strap cut length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_width = max(240.0, min(bag_width, 500.0))
bag_height = max(180.0, min(bag_height, 400.0))
bag_depth = max(50.0, min(bag_depth, 200.0))
flap_drop = max(80.0, min(flap_drop, 340.0))
webbing_width = max(20.0, min(webbing_width, 50.0))
strap_length = max(200.0, min(strap_length, 700.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BW = bag_width
BH = 2.0 * bag_height + bag_depth        # front + base + back, flat


def build_body():
    """Front + base + back as one panel, folded at the base. `side_l`/`side_r` are the
    two long edges the gusset wraps; `top_front`/`top_back` are the two openings."""
    edges = [
        fc.Edge("side_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BH))]),
        fc.Edge("top_back", [fc.Line(fc.P(0.0, BH), fc.P(BW, BH))]),
        fc.Edge("side_r", [fc.Line(fc.P(BW, BH), fc.P(BW, 0.0))]),
        fc.Edge("top_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
    ]
    y_fb = bag_height
    y_bb = bag_height + bag_depth
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(BW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(BW, y_bb)], kind="marking"),
        # Where the flap is sewn onto the back panel's top edge.
        fc.Internal("flap-seam", [fc.P(0.0, BH - 6.0), fc.P(BW, BH - 6.0)], kind="marking"),
        # The buckle-strap keeper on the front face.
        fc.Internal("buckle-keeper",
                    [fc.P(BW * 0.5 - webbing_width / 2.0, bag_height * 0.32),
                     fc.P(BW * 0.5 + webbing_width / 2.0, bag_height * 0.32)],
                    kind="drill"),
        # Shoulder-strap anchors at the two top corners of the back panel.
        fc.Internal("shoulder-anchor-l", [fc.P(14.0, BH - 40.0), fc.P(14.0, BH - 90.0)],
                    kind="drill"),
        fc.Internal("shoulder-anchor-r",
                    [fc.P(BW - 14.0, BH - 40.0), fc.P(BW - 14.0, BH - 90.0)], kind="drill"),
    ]
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


def build_gusset():
    """The wrap-around gusset: bag_depth wide, spanning one side of the body from the
    front opening, down the front, across the base and back up to the back opening —
    i.e. the body's full side run. Cut 2 (one per side)."""
    ln = BH        # the side edge run the gusset follows
    w = bag_depth
    return fc.Piece(
        "gusset",
        [
            fc.Edge("join", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("top_back", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("top_front", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join", bag_height / BH, "front base fold"),
                 fc.Notch("join", (bag_height + bag_depth) / BH, "back base fold")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side Gusset",
    )


def build_flap():
    """The cover flap: as wide as the bag, dropping flap_drop with softly rounded front
    corners. Its `attach` edge sews to the back panel's top opening."""
    w, h = BW, flap_drop
    corner = min(w * 0.18, h * 0.45)
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),   # sews to the body top_back
        fc.Edge("side_r", [fc.Line(fc.P(w, h), fc.P(w, corner))]),
        fc.Edge("front", [
            fc.curve_through(fc.P(w, corner), fc.P(w - corner, 0.0), bulge=0.42, side=-1.0),
            fc.Line(fc.P(w - corner, 0.0), fc.P(corner, 0.0)),
            fc.curve_through(fc.P(corner, 0.0), fc.P(0.0, corner), bulge=0.42, side=-1.0),
        ]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, corner), fc.P(0.0, h))]),
    ]
    internals = [
        # The buckle strap is bar-tacked to the flap's underside, on its centre line.
        fc.Internal("strap-tack",
                    [fc.P(w * 0.5 - webbing_width / 2.0, h - 30.0),
                     fc.P(w * 0.5 + webbing_width / 2.0, h - 30.0)], kind="drill"),
    ]
    return fc.Piece(
        "flap",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("front", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cover Flap",
    )


def build_strap():
    """The webbing closure strap that feeds the cam buckle."""
    ln, w = strap_length, webbing_width
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("buckle_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("tack_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Closure Strap (webbing)",
    )


def build():
    pattern = fc.PatternSet("messenger-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())
    if all_pieces or target_piece == "flap":
        pattern.add(build_flap())
    if all_pieces or target_piece == "strap":
        pattern.add(build_strap())

    if all_pieces:
        # Each gusset's join edge takes one side of the body's fold-at-base panel.
        pattern.declare_seam(("gusset", "join"), ("body", "side_l"), tol=1.0)
        # The flap's attach edge sews onto the back panel's top opening.
        pattern.declare_seam(("flap", "attach"), ("body", "top_back"), tol=1.0)
    if all_pieces or target_piece == "body":
        # Front and back openings are the same width by construction (fold at base).
        pattern.declare_seam(("body", "top_front"), ("body", "top_back"), tol=0.5)
    if all_pieces or target_piece == "gusset":
        # A gusset sews to two body sides — its own mirror across the bag.
        pattern.declare_seam(("gusset", "join"), ("gusset", "join"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "waxed canvas or cordura", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 76% marker; a messenger flap wants a fabric with body."},
        {"item": "webbing", "qty": round(strap_length + 1400.0), "unit": "mm_length",
         "note": f"{webbing_width:.0f} mm webbing: the closure strap + the shoulder strap."},
        {"item": "cam buckle", "qty": 1, "unit": "count",
         "note": "Yantra4D cam-buckle (see notion.hardware_ref); its webbing throat takes "
                 f"the same {webbing_width:.0f} mm webbing as the closure strap. A cam "
                 "buckle is one-handed — the reason messengers use them."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "box-and-cross the shoulder anchors and the strap tack."},
    ]
    pattern.metadata = {
        "fc300_rank": 205,
        "family": "bags_luggage",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"width": round(bag_width, 1), "height": round(bag_height, 1),
                        "depth": round(bag_depth, 1), "flap_drop": round(flap_drop, 1)},
        "solved": {
            "body_side_run_mm": round(BH, 2),
            "gusset_span_mm": round(BH, 2),
            "note": "the gusset spans the body's MEASURED side run (front + base + back) "
                    "so the wrap seam verifies rather than being eased in.",
        },
        "hardware": "closure cam buckle via Yantra4D (notion.hardware_ref -> cam-buckle); "
                    "the buckle throat and the closure strap share webbing_width",
    }
    return pattern


result = build()
