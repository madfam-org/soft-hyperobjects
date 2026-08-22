"""
Sling Bag — Fashion Cabinet Bag Cartridge (FC-300 rank #204, y4d snap-hook swivel).

A single-strap cross-body sling: a TEARDROP front/back panel (wide at the shoulder end,
tapering to a rounded point at the hip end), a GUSSET strip that gives it depth, a webbing
STRAP that crosses the chest, and two anchor TABS at the panel's two ends. The strap clips
to the tabs through a swivelling snap hook — a Yantra4D solid (`snap-hook-swivel`; see the
manifest's notion.hardware_ref) whose webbing eye takes this bag's `webbing_width`.

The seam that must SOLVE: the gusset wraps the panel's whole outer run (upper + point +
lower), so its length is derived FROM the measured panel run rather than assumed — the
panel's edges are Beziers, and their combined arc length is not a formula.

Pieces:
  - panel  : the teardrop front/back panel (cut 2).
  - gusset : the depth strip; its two long edges each sew to one panel.
  - strap  : the webbing cross-body strap.
  - tab    : the anchor tab the snap hook clips into (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # panel|gusset|strap|tab|set

bag_length = float(PARAM(lambda: bag_length, 360.0))     # shoulder end to hip point
bag_width = float(PARAM(lambda: bag_width, 200.0))       # widest point (shoulder end)
point_width = float(PARAM(lambda: point_width, 90.0))    # width at the tapered hip end
bag_depth = float(PARAM(lambda: bag_depth, 70.0))        # gusset width
webbing_width = float(PARAM(lambda: webbing_width, 25.0))  # strap/hook webbing width
strap_length = float(PARAM(lambda: strap_length, 1150.0))  # cross-body strap length
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_length = max(200.0, min(bag_length, 520.0))
bag_width = max(120.0, min(bag_width, 320.0))
point_width = max(40.0, min(point_width, 200.0))
bag_depth = max(30.0, min(bag_depth, 160.0))
webbing_width = max(15.0, min(webbing_width, 50.0))
strap_length = max(700.0, min(strap_length, 1500.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The point end can never be wider than the shoulder end — that is not a teardrop.
point_width = min(point_width, bag_width * 0.9)

HW = bag_width / 2.0
HP = point_width / 2.0


def _panel_edges():
    """The teardrop outline, drafted with the wide (shoulder) end at y = bag_length and
    the tapered (hip) end at y = 0. Returns the four named edges."""
    top_r = fc.P(HW, bag_length)
    top_l = fc.P(-HW, bag_length)
    pt_r = fc.P(HP, 0.0)
    pt_l = fc.P(-HP, 0.0)
    return [
        # Right side: the long belly curve from the shoulder down to the point.
        fc.Edge("side_r", [fc.curve_through(top_r, pt_r, bulge=0.13, side=1.0)]),
        # The rounded hip point.
        fc.Edge("point", [fc.curve_through(pt_r, pt_l, bulge=0.34, side=1.0)]),
        fc.Edge("side_l", [fc.curve_through(pt_l, top_l, bulge=0.13, side=1.0)]),
        # The shoulder end: the bag's opening, which takes the zip.
        fc.Edge("opening", [fc.curve_through(top_l, top_r, bulge=0.07, side=-1.0)]),
    ]


def build_panel():
    """One teardrop panel (cut 2 — front and back)."""
    internals = [
        # Anchor-tab placements: one at each end of the panel's long axis.
        fc.Internal("tab-shoulder",
                    [fc.P(-webbing_width / 2.0, bag_length - 18.0),
                     fc.P(webbing_width / 2.0, bag_length - 18.0)], kind="drill"),
        fc.Internal("tab-hip",
                    [fc.P(-webbing_width / 2.0, 18.0),
                     fc.P(webbing_width / 2.0, 18.0)], kind="drill"),
    ]
    return fc.Piece(
        "panel",
        _panel_edges(),
        seam_allowance=seam_allowance,
        notches=[fc.Notch("point", 0.5, "hip point centre"),
                 fc.Notch("opening", 0.5, "shoulder centre")],
        grainline=fc.Grainline(fc.P(0.0, bag_length * 0.2),
                               fc.P(0.0, bag_length * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Teardrop Panel",
    )


def _panel_wrap_length():
    """The measured run of one panel's side_r + point + side_l — the gusset's span."""
    piece = build_panel()
    return sum(piece.edge(name).length(0.02) for name in ("side_r", "point", "side_l"))


def build_gusset():
    """The depth strip; bag_depth wide, spanning the panel's outer run."""
    ln = _panel_wrap_length()
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
        notches=[fc.Notch("join_a", 0.5, "hip point centre"),
                 fc.Notch("join_b", 0.5, "hip point centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Side Gusset",
    )


def build_strap():
    """The webbing cross-body strap, cut at the width the snap hook's eye expects."""
    ln, w = strap_length, webbing_width
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("hook_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("tail_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Cross-body Strap (webbing)",
    )


def build_tab():
    """The anchor tab the snap hook clips into (cut 2). Folds double around the hook's
    eye, so it is cut twice the webbing width plus the fold-over."""
    w = webbing_width
    ln = w * 3.2
    return fc.Piece(
        "tab",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("hook_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("body_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Hook Anchor Tab",
    )


def build():
    pattern = fc.PatternSet("sling-bag")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "panel":
        pattern.add(build_panel())
    if all_pieces or target_piece == "gusset":
        pattern.add(build_gusset())
    if all_pieces or target_piece == "strap":
        pattern.add(build_strap())
    if all_pieces or target_piece == "tab":
        pattern.add(build_tab())

    if all_pieces:
        # Each gusset long edge takes one panel's outer run.
        pattern.declare_seam(("gusset", "join_a"),
                             [("panel", "side_r"), ("panel", "point"), ("panel", "side_l")],
                             tol=1.0)
        pattern.declare_seam(("gusset", "join_b"),
                             [("panel", "side_r"), ("panel", "point"), ("panel", "side_l")],
                             tol=1.0)
        # The tab's hook end and the strap's hook end both take the same hook eye,
        # so they are cut to the same webbing width.
        pattern.declare_seam(("tab", "hook_end"), ("strap", "hook_end"), tol=0.5)
    if all_pieces or target_piece == "panel":
        # Front and back panels are the same piece: their openings meet at the zip.
        pattern.declare_seam(("panel", "opening"), ("panel", "opening"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "ripstop nylon or waxed canvas", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; the teardrop nests well on the marker."},
        {"item": "webbing", "qty": round(strap_length + 4.0 * webbing_width * 3.2),
         "unit": "mm_length",
         "note": f"{webbing_width:.0f} mm webbing: the cross-body strap + both anchor tabs."},
        {"item": "snap hook with swivel", "qty": 2, "unit": "count",
         "note": "Yantra4D snap-hook-swivel (see notion.hardware_ref); its webbing eye "
                 f"takes the same {webbing_width:.0f} mm webbing as the strap and tabs. "
                 "The swivel is what stops a one-strap bag from twisting on the body."},
        {"item": "curved zip", "qty": 1, "unit": "count",
         "note": "along the shoulder-end opening; a curved opening wants a coil zip."},
        {"item": "heavy-duty thread", "qty": 1, "unit": "spool",
         "note": "bar-tack both tabs; a single-strap bag hangs entirely off two points."},
    ]
    pattern.metadata = {
        "fc300_rank": 204,
        "family": "bags_luggage",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"length": round(bag_length, 1), "width": round(bag_width, 1),
                        "point_width": round(point_width, 1), "depth": round(bag_depth, 1)},
        "solved": {
            "panel_outer_run_mm": round(_panel_wrap_length(), 2),
            "note": "the gusset length is taken from the MEASURED Bezier run of the "
                    "panel's side+point+side, not from a formula — the teardrop's arc "
                    "length has no closed form.",
        },
        "hardware": "swivelling snap hooks via Yantra4D (notion.hardware_ref -> "
                    "snap-hook-swivel); the hook eye and the strap/tabs share webbing_width",
    }
    return pattern


result = build()
