"""
Mesh Delicates Wash Bag — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #368, Yantra4D-bridged zipper).

The zip-top mesh bag that keeps a bra's hooks off a sweater and a sock out of the machine's
gasket: two mesh PANELS box-stitched on three sides, the fourth closed by a zipper whose
pull tucks under a small FLAP so it cannot snag or scratch the drum. The zipper is the
Yantra4D `zipper` solid (notion.hardware_ref); its tape edge is driven by the same
bag_width that drives the garment's own zip interface — the dimensional handshake the
hardware lane enforces.

Drafting note — the seam that must SOLVE: a mesh bag is dimensionally simple, but the zip
tape must run the FULL measured mouth or the corners gape and small items escape. The panel
mouth edge and the zip length are the same bag_width, and the tuck flap is sized to cover
the pull's parked position (a fixed fraction of the mouth), so the flap can never be cut too
short to hide the pull.

Pieces:
  - panel : one mesh face (cut 2); the mouth edge takes the zip.
  - flap  : the pull-tuck cover at one end of the zip (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # panel|flap|set

bag_width = float(PARAM(lambda: bag_width, 300.0))       # mouth width = zip length
bag_height = float(PARAM(lambda: bag_height, 340.0))     # mouth to base
tape_width = float(PARAM(lambda: tape_width, 30.0))      # zipper tape width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bag_width = max(150.0, min(bag_width, 500.0))
bag_height = max(150.0, min(bag_height, 560.0))
tape_width = max(18.0, min(tape_width, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The pull-tuck flap covers the parked pull: a fixed fraction of the mouth, floored
# so it is never too short to hide the pull.
FLAP_LEN = max(45.0, bag_width * 0.16)
FLAP_HEIGHT = max(30.0, tape_width * 1.6)


def build_panel():
    """One mesh face (cut 2). `mouth` takes the zip; the other three edges box-stitch."""
    w, h = bag_width, bag_height
    edges = [
        fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("mouth", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("mouth", 0.5, "zip midpoint"),
                 fc.Notch("side_r", 0.5, "seam match"),
                 fc.Notch("side_l", 0.5, "seam match")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=[fc.Internal("zip-tape-line",
                               [fc.P(0.0, h - tape_width * 0.5),
                                fc.P(w, h - tape_width * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Mesh panel",
    )


def build_flap():
    """The pull-tuck cover: a small rectangle folded over the zip's parked pull."""
    ln, w = FLAP_LEN, FLAP_HEIGHT * 2.0
    return fc.Piece(
        "flap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "over the parked pull")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Pull-tuck flap",
    )


def build():
    pattern = fc.PatternSet("delicates-wash-bag")
    everything = target_piece == "set"
    if everything or target_piece == "panel":
        pattern.add(build_panel())
    if everything or target_piece == "flap":
        pattern.add(build_flap())

    if everything:
        # The two mesh panels box-stitch on base and both sides.
        pattern.declare_seam(("panel", "base"), ("panel", "base"), tol=0.5)
        pattern.declare_seam(("panel", "side_r"), ("panel", "side_r"), tol=0.5)
        pattern.declare_seam(("panel", "side_l"), ("panel", "side_l"), tol=0.5)
        # THE zip seam: the zipper runs the full MEASURED mouth of both panels.
        pattern.declare_seam(("panel", "mouth"), ("panel", "mouth"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "polyester wash mesh", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 82% marker; a fine mesh keeps a hook in and lets "
                 "water through — a bag with too coarse a mesh lets small hooks out."},
        {"item": "closed-end zipper", "qty": 1, "unit": "count",
         "note": f"≈ {bag_width:.0f} mm; Yantra4D zipper (notion.hardware_ref) — its "
                 f"zip_length is driven by the same bag_width."},
        {"item": "solid binding for the mouth", "qty": round(bag_width * 2.2 + 60.0),
         "unit": "mm_length",
         "note": "the zip sews to a solid binding, not raw mesh, or the teeth tear out."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "zig-zag every mesh seam so it flexes wet without splitting."},
    ]
    pattern.metadata = {
        "fc400_rank": 368,
        "family": "care_and_keeping",
        "fabric_hint": "tricot-nylon-elastano",
        "finished_mm": {"width": round(bag_width, 1),
                        "height": round(bag_height, 1)},
        "solved": {
            "flap_length_mm": round(FLAP_LEN, 2),
            "flap_height_mm": round(FLAP_HEIGHT, 2),
            "note": "the zip runs the FULL measured mouth (= bag_width) so the corners "
                    "cannot gape; the pull-tuck flap is floored at 45 mm so it always "
                    "covers the parked pull that would otherwise scratch the drum.",
        },
        "hardware": "zip-top closure via Yantra4D (notion.hardware_ref -> zipper); "
                    "zip_length = bag_width, the same parameter that drives this bag's "
                    "own zip interface (the dimensional handshake).",
    }
    return pattern


result = build()
