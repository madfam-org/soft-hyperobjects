"""
Saddle Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #209, y4d twist-lock closure).

The saddle silhouette: a BODY panel whose base is a deep arc (the "saddle" curve), a
one-piece GUSSET wrapping that whole curved run, and a curved FLAP that continues the
body's arc down over the front, caught by a twist-lock. The lock is a Yantra4D solid
(`twist-lock-closure`; see the manifest's notion.hardware_ref) and is POINT-PLACED
hardware: it has a keeper slot and a rivet pattern but no sewn flange, so it takes drilled
plate and turn positions rather than an edge coupling.

The seam that must SOLVE: the body's saddle arc and the flap's front arc are both Beziers
with no closed-form length, and the gusset has to wrap the body's whole side-base-side run.
Every one of those runs is MEASURED off the drafted geometry, so the declared seams verify
exactly. The flap arc is additionally SOLVED by bisection so its front edge matches the
body's saddle arc — the flap and the bag bottom read as one continuous curve.

Pieces:
  - body   : the saddle panel (cut 2 — front and back).
  - gusset : the wrap-around gusset following the body's curved run.
  - flap   : the curved cover flap, its arc solved to the body's saddle arc.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|gusset|flap|set

bag_width = float(PARAM(lambda: bag_width, 300.0))       # width across the front
bag_height = float(PARAM(lambda: bag_height, 230.0))     # height at the side seams
saddle_curve = float(PARAM(lambda: saddle_curve, 0.26))  # how deeply the base arcs
bag_depth = float(PARAM(lambda: bag_depth, 90.0))        # gusset width
flap_drop = float(PARAM(lambda: flap_drop, 160.0))       # how far the flap falls
lock_plate = float(PARAM(lambda: lock_plate, 42.0))      # twist-lock plate length
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_width = max(180.0, min(bag_width, 440.0))
bag_height = max(120.0, min(bag_height, 340.0))
saddle_curve = max(0.05, min(saddle_curve, 0.55))
bag_depth = max(30.0, min(bag_depth, 180.0))
flap_drop = max(60.0, min(flap_drop, 280.0))
lock_plate = max(20.0, min(lock_plate, 80.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HW = bag_width / 2.0


def _saddle_edge(bulge):
    """The body's base arc — the saddle curve, from the right side seam to the left."""
    return fc.Edge("saddle",
                   [fc.curve_through(fc.P(HW, 0.0), fc.P(-HW, 0.0), bulge=bulge, side=1.0)])


SADDLE_LEN = _saddle_edge(saddle_curve).length(0.02)


def _flap_front(bulge):
    """The flap's front arc, spanning the same chord as the saddle so that when the flap
    falls the two curves read as one. Length grows monotonically with bulge."""
    return fc.Edge("front",
                   [fc.curve_through(fc.P(-HW, 0.0), fc.P(HW, 0.0), bulge=bulge, side=-1.0)])


def _solve_flap_arc():
    """Bisect the flap's front bulge until its run equals the body's measured saddle arc."""
    lo, hi = 0.0, 1.6
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if _flap_front(mid).length(0.02) < SADDLE_LEN:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    got = _flap_front(bulge).length(0.02)
    if abs(got - SADDLE_LEN) > 0.05:
        raise ValueError(
            f"saddle flap-arc solver did not converge: {got:.3f} vs saddle "
            f"{SADDLE_LEN:.3f} mm"
        )
    return bulge


FLAP_BULGE = _solve_flap_arc()


def build_body():
    """The saddle panel (cut 2). Its base arcs deeply; the two side seams are straight;
    the top is the bag's opening."""
    edges = [
        fc.Edge("side_r", [fc.Line(fc.P(HW, bag_height), fc.P(HW, 0.0))]),
        _saddle_edge(saddle_curve),
        fc.Edge("side_l", [fc.Line(fc.P(-HW, 0.0), fc.P(-HW, bag_height))]),
        fc.Edge("opening", [fc.Line(fc.P(-HW, bag_height), fc.P(HW, bag_height))]),
    ]
    internals = [
        # The twist-lock's KEEPER plate is riveted to the front body panel — point-placed
        # hardware, so this is a drilled position, not a sewn edge.
        fc.Internal("lock-keeper-h",
                    [fc.P(-lock_plate / 2.0, bag_height * 0.42),
                     fc.P(lock_plate / 2.0, bag_height * 0.42)], kind="drill"),
        fc.Internal("lock-keeper-v",
                    [fc.P(0.0, bag_height * 0.42 - lock_plate / 4.0),
                     fc.P(0.0, bag_height * 0.42 + lock_plate / 4.0)], kind="drill"),
    ]
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("saddle", 0.5, "base centre"),
                 fc.Notch("opening", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, bag_height * 0.25),
                               fc.P(0.0, bag_height * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Saddle Panel",
    )


def _body_wrap_run():
    """The measured run of one body's side_r + saddle + side_l — the gusset's span."""
    piece = build_body()
    return sum(piece.edge(name).length(0.02) for name in ("side_r", "saddle", "side_l"))


def build_gusset():
    """The wrap-around gusset following the body's whole curved run."""
    ln = _body_wrap_run()
    w = bag_depth
    return fc.Piece(
        "gusset",
        [
            fc.Edge("join_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("join_b", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("join_a", 0.5, "base centre"),
                 fc.Notch("join_b", 0.5, "base centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Wrap Gusset",
    )


def build_flap():
    """The cover flap: attaches to the back panel's opening, falls flap_drop, and closes
    with the SOLVED front arc that echoes the body's saddle curve."""
    h = flap_drop
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(HW, h), fc.P(-HW, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(-HW, h), fc.P(-HW, 0.0))]),
        _flap_front(FLAP_BULGE),
        fc.Edge("side_r", [fc.Line(fc.P(HW, 0.0), fc.P(HW, h))]),
    ]
    internals = [
        # The twist-lock's TURN piece rivets through the flap's underside.
        fc.Internal("lock-turn-h",
                    [fc.P(-lock_plate / 2.0, h * 0.28), fc.P(lock_plate / 2.0, h * 0.28)],
                    kind="drill"),
        fc.Internal("lock-turn-v",
                    [fc.P(0.0, h * 0.28 - lock_plate / 4.0),
                     fc.P(0.0, h * 0.28 + lock_plate / 4.0)], kind="drill"),
    ]
    return fc.Piece(
        "flap",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("front", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.2), fc.P(0.0, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Cover Flap",
    )


def build():
    pattern = fc.PatternSet("saddle-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "body":
        pattern.add(build_body())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())
    if all_pieces or target_piece == "flap":
        pattern.add(build_flap())

    if all_pieces:
        # Each gusset long edge takes one body panel's curved outer run.
        pattern.declare_seam(("gusset", "join_a"),
                             [("body", "side_r"), ("body", "saddle"), ("body", "side_l")],
                             tol=1.0)
        pattern.declare_seam(("gusset", "join_b"),
                             [("body", "side_r"), ("body", "saddle"), ("body", "side_l")],
                             tol=1.0)
        # The flap sews onto the back panel's opening.
        pattern.declare_seam(("flap", "attach"), ("body", "opening"), tol=1.0)
        # The SOLVED flap arc matches the body's saddle arc — one continuous curve.
        pattern.declare_seam(("flap", "front"), ("body", "saddle"), tol=0.5)
    if all_pieces or target_piece == "body":
        # Front and back panels meet at the opening.
        pattern.declare_seam(("body", "opening"), ("body", "opening"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.64)
    pattern.bom = [
        {"item": "bridle leather or heavy waxed canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 64% marker; the saddle curve wants a firm hand."},
        {"item": "twist-lock closure", "qty": 1, "unit": "count",
         "note": "Yantra4D twist-lock-closure (see notion.hardware_ref); POINT-PLACED — "
                 f"the {lock_plate:.0f} mm keeper rivets to the front panel and the turn "
                 "to the flap, at the marked drill positions."},
        {"item": "edge paint or binding", "qty": round(SADDLE_LEN * 2.0 + 400.0),
         "unit": "mm_length", "note": "finish the saddle arc and the flap arc to match."},
        {"item": "saddler's thread", "qty": 1, "unit": "spool",
         "note": "saddle-stitch the gusset around the curve; ease at the base notch."},
    ]
    pattern.metadata = {
        "fc300_rank": 209,
        "family": "bags_luggage",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"width": round(bag_width, 1), "height": round(bag_height, 1),
                        "depth": round(bag_depth, 1), "flap_drop": round(flap_drop, 1)},
        "solved": {
            "saddle_arc_mm": round(SADDLE_LEN, 3),
            "flap_arc_mm": round(_flap_front(FLAP_BULGE).length(0.02), 3),
            "flap_bulge": round(FLAP_BULGE, 5),
            "delta_mm": round(_flap_front(FLAP_BULGE).length(0.02) - SADDLE_LEN, 4),
            "body_wrap_run_mm": round(_body_wrap_run(), 2),
            "note": "the flap's front bulge is bisected until its arc equals the body's "
                    "MEASURED saddle arc, so flap and bag bottom read as one curve; the "
                    "gusset spans the body's measured side+saddle+side run.",
        },
        "hardware": "twist-lock via Yantra4D (notion.hardware_ref -> twist-lock-closure); "
                    "POINT/SLOT placement — the lock has a keeper slot and rivet pattern "
                    "but no sewn flange, so it takes drilled positions, not an edge",
    }
    return pattern


result = build()
