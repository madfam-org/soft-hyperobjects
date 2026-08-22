"""
Camera Holster — Fashion Cabinet Accessory Cartridge (FC-300 #243, technical & outdoor).

The top-loading camera holster: a padded wedge-shaped pouch that hangs at the hip or off a
pack strap, deep enough for a body with a lens mounted, tapered at the base to the lens
barrel so nothing rattles. A padded wrap body (front + base + back cut as one, folded at
the base) boxes at the lower corners; a shaped lid closes over the top; and a swivelling
snap hook anchors the holster to a belt loop or a pack's daisy chain so it can be moved
between carries without unthreading anything.

The snap-hook-swivel solid is Yantra4D territory (`carabiner`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the holster — the pouch dimensions, the padded
wrap, the lid, the anchor tab.

The boxed wrap follows the house precedent (projects/dopp-kit, projects/belt-bag): one
panel = front + base + back with the base fold marked, corners boxed at the base.

Pieces:
  - body   : front + base + back cut as one, folded at the base, corners boxed.
  - side   : the two side gussets that give the holster its wedge.
  - lid    : the shaped top lid.
  - anchor : the webbing tab that carries the snap hook.

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
target_piece = str(PARAM(lambda: target_piece, "set"))      # body|side|lid|anchor|set

body_width   = float(PARAM(lambda: body_width, 150.0))      # camera body width
body_depth   = float(PARAM(lambda: body_depth, 120.0))      # front-to-back with lens
holster_height = float(PARAM(lambda: holster_height, 215.0))  # base to the lid seam
base_taper   = float(PARAM(lambda: base_taper, 30.0))       # narrowing to the lens barrel
pad_thickness = float(PARAM(lambda: pad_thickness, 10.0))   # foam wall
lid_drop     = float(PARAM(lambda: lid_drop, 70.0))         # lid overhang down the front
anchor_width = float(PARAM(lambda: anchor_width, 25.0))     # snap-hook tab webbing width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
body_width   = max(80.0, min(body_width, 260.0))
body_depth   = max(60.0, min(body_depth, 240.0))
holster_height = max(110.0, min(holster_height, 400.0))
base_taper   = max(0.0, min(base_taper, 90.0))
pad_thickness = max(3.0, min(pad_thickness, 25.0))
lid_drop     = max(25.0, min(lid_drop, 160.0))
anchor_width = max(15.0, min(anchor_width, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# Padding pushes the shell out on every wall.
BW = body_width + 2.0 * pad_thickness
BD = body_depth + 2.0 * pad_thickness
H = holster_height
base_taper = min(base_taper, BW / 2.0 - 20.0)
BASE_W = BW - base_taper                    # narrowed base, matching the lens barrel
# The wrap: front + base + back stacked into one flat panel.
PANEL_H = 2.0 * H + BD


def build_body():
    """Front + base + back as one fold-at-base panel; corners boxed for a flat bottom."""
    y_front_base = H
    y_base_back = H + BD
    box = BD / 2.0
    internals = [
        fc.Internal("fold-front-base",
                    [fc.P(0.0, y_front_base), fc.P(BW, y_front_base)], kind="marking"),
        fc.Internal("fold-base-back",
                    [fc.P(0.0, y_base_back), fc.P(BW, y_base_back)], kind="marking"),
        fc.Internal("pad-zone",
                    [fc.P(pad_thickness, pad_thickness),
                     fc.P(BW - pad_thickness, pad_thickness),
                     fc.P(BW - pad_thickness, PANEL_H - pad_thickness),
                     fc.P(pad_thickness, PANEL_H - pad_thickness),
                     fc.P(pad_thickness, pad_thickness)], kind="marking"),
    ]
    # The four boxed-corner stitch lines at the base folds.
    for (cx, cy, sy) in [(0.0, y_front_base, -1.0), (BW, y_front_base, -1.0),
                         (0.0, y_base_back, 1.0), (BW, y_base_back, 1.0)]:
        sx = box if cx == 0.0 else -box
        internals.append(fc.Internal(
            "box-corner", [fc.P(cx, cy + sy * box), fc.P(cx + sx, cy)], kind="marking"))
    # The anchor tab lands high on the back face.
    internals.append(fc.Internal(
        "anchor-place",
        [fc.P(BW * 0.5 - anchor_width / 2.0, PANEL_H - 30.0),
         fc.P(BW * 0.5 + anchor_width / 2.0, PANEL_H - 30.0)], kind="drill"))
    return fc.Piece(
        "body",
        [
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, PANEL_H))]),
            fc.Edge("top_back", [fc.Line(fc.P(0.0, PANEL_H), fc.P(BW, PANEL_H))]),
            fc.Edge("right", [fc.Line(fc.P(BW, PANEL_H), fc.P(BW, 0.0))]),
            fc.Edge("top_front", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", H / PANEL_H, "front base fold"),
                 fc.Notch("left", (H + BD) / PANEL_H, "back base fold")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 25.0), fc.P(BW * 0.5, PANEL_H - 25.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Body (front + base + back)",
    )


def build_side():
    """One side gusset — the piece that turns the flat wrap into a box.

    Its sewn run is SOLVED to the body's side: front_edge (H) + base (BD) + back_edge (H)
    is exactly the body's `left`/`right` edge (2H + BD), so the declared gusset seam is a
    dimensional proof rather than a tolerance. The wedge lives in the TOP edge, which
    slants back by the lid drop so the mouth opens toward the photographer.
    """
    wedge = min(lid_drop * 0.35, H * 0.25)
    return fc.Piece(
        "side",
        [
            fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(BD, 0.0))]),
            fc.Edge("back_edge", [fc.Line(fc.P(BD, 0.0), fc.P(BD, H))]),
            fc.Edge("top", [fc.Line(fc.P(BD, H), fc.P(0.0, H))]),
            fc.Edge("front_edge", [fc.Line(fc.P(0.0, H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "front face mid"),
                 fc.Notch("back_edge", 0.5, "back face mid"),
                 fc.Notch("top", wedge / BD, "lid wedge")],
        grainline=fc.Grainline(fc.P(BD * 0.5, 15.0), fc.P(BD * 0.5, H - 15.0)),
        internals=[
            # The mouth wedge: the lid seam slants back by this much so the holster
            # opens toward the photographer. Marked, not cut — the sewn run stays
            # front_edge + base + back_edge = the body's side exactly.
            fc.Internal("mouth-wedge", [fc.P(0.0, H), fc.P(BD, H - wedge)], kind="marking"),
            fc.Internal("base-taper",
                        [fc.P(0.0, base_taper * 0.5), fc.P(BD, base_taper * 0.5)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side gusset",
    )


def build_lid():
    """The shaped lid: covers the mouth and drops over the front face."""
    depth = BD + lid_drop
    return fc.Piece(
        "lid",
        [
            fc.Edge("hinge", [fc.Line(fc.P(0.0, 0.0), fc.P(BW, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(BW, 0.0), fc.P(BW, depth))]),
            fc.Edge("front_edge",
                    [fc.curve_through(fc.P(BW, depth), fc.P(0.0, depth), bulge=0.08, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, depth), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hinge", 0.5, "lid centre")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 12.0), fc.P(BW * 0.5, depth - 12.0)),
        internals=[fc.Internal("lid-fold", [fc.P(0.0, BD), fc.P(BW, BD)], kind="fold")],
        cut=fc.CutSpec(quantity=1),
        label="Top lid",
    )


def build_anchor():
    """The webbing tab that carries the swivelling snap hook."""
    length = 110.0
    return fc.Piece(
        "anchor",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(anchor_width, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(anchor_width, 0.0), fc.P(anchor_width, length))]),
            fc.Edge("hook_end", [fc.Line(fc.P(anchor_width, length), fc.P(0.0, length))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, length), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("side_r", 0.5, "hook fold")],
        grainline=fc.Grainline(fc.P(anchor_width / 2.0, length * 0.15),
                               fc.P(anchor_width / 2.0, length * 0.85)),
        cut=fc.CutSpec(quantity=1),
        label="Snap-hook anchor tab",
    )


def build():
    pattern = fc.PatternSet("camera-holster")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "side":
        pattern.add(build_side())
    if everything or target_piece == "lid":
        pattern.add(build_lid())
    if everything or target_piece == "anchor":
        pattern.add(build_anchor())
    if everything:
        # The lid's hinge sews to the body's back mouth — both are the shell width.
        pattern.declare_seam(("lid", "hinge"), ("body", "top_back"), tol=1.0)
        # The gusset wraps the body's whole side: front face + base + back face is
        # SOLVED to the body's left edge (2H + BD) — a dimensional proof, and the
        # mirrored gusset does the same on the right.
        pattern.declare_seam(
            [("side", "front_edge"), ("side", "base"), ("side", "back_edge")],
            [("body", "left")], tol=1.0)
        pattern.declare_seam(
            [("side", "front_edge"), ("side", "base"), ("side", "back_edge")],
            [("body", "right")], tol=1.0)
        # The mouth the lid closes over: the gusset top and the body's front mouth.
        pattern.declare_seam(("body", "top_front"), ("body", "top_back"), tol=1.0)
        # The anchor tab folds on itself around the hook.
        pattern.declare_seam(("anchor", "attach"), ("anchor", "hook_end"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cordura shell + brushed tricot lining",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; tricot so a lens barrel never scuffs."},
        {"item": f"closed-cell foam, {pad_thickness:.0f} mm", "qty": 1, "unit": "pc",
         "note": "padding on every wall; the base takes the drop."},
        {"item": "swivelling snap hook", "qty": 1, "unit": "count",
         "note": "Yantra4D carabiner (see notion.hardware_ref) anchors to a belt loop "
                 "or a daisy chain and swivels so the holster never twists."},
        {"item": "bonded nylon thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the anchor tab — it carries the whole holster."},
    ]
    pattern.metadata = {
        "fc300_rank": 243, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A padded top-loading wedge deep enough for a camera body with a lens "
            "mounted and tapered at the base to the barrel, boxed at the base corners on the "
            "house wrap construction, closed by a shaped lid and hung on a swivelling snap hook.",
        "solved": {"shell_width_mm": round(BW, 1), "shell_depth_mm": round(BD, 1),
                   "base_width_mm": round(BASE_W, 1), "panel_height_mm": round(PANEL_H, 1)},
        "hardware": "swivel snap hook via Yantra4D (notion.hardware_ref -> carabiner)",
    }
    return pattern


result = build()
