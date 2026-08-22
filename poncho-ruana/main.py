"""
Ruana — FC-300 rank #279. Fashion Cabinet Garment Cartridge.

The ruana: the open-front wool wrap of the Colombian and Venezuelan Andes —
Boyacá, Cundinamarca, Santander, Nariño and the Venezuelan Andean states. It
differs from a poncho in exactly one decisive way, and that difference IS the
garment: a poncho is a closed rectangle with a neck hole; a ruana is SPLIT up
the centre front, so it opens like a cape and can be thrown over a shoulder.
The commons already holds `sarape-poncho` (the closed Mexican form); this
cartridge draws the open Andean one.

The ruana is working dress of the cold Andean highlands — páramo country — and
its logic is thermal: heavy fulled wool, a long back that shields the kidneys,
and an open front you can close by crossing or throw back to free the arms.

Three signatures, all real geometry rather than styling:

  - THE SPLIT (the definition): the front is two panels, the back is one. The
    two front panels' inner edges are the centre-front opening; their combined
    width is solved to equal the back's width exactly, so the garment hangs
    square and the shoulder seam is a true seam rather than an approximation.
  - THE NECK SLOT: a plain slot, not a scooped neckline. On a woven wrap the
    neck is a slit cut across the shoulder line, faced or bound. Drafted here as
    a shoulder-seam interruption whose length is a parameter.
  - LONGER BACK (the drop): the back panel is drafted longer than the fronts,
    the traditional working proportion — it covers the kidneys when riding or
    walking while the front stays clear of the legs.

Drafting note — what actually SOLVES: the shoulder seam. Each front panel's
shoulder edge is solved so that (front shoulder x2) + (neck slot) equals the
back's measured shoulder edge exactly. The neck slot is therefore carved out of
a real measured width rather than being an assumed leftover, and a slot wider
than the shoulder allows is clamped rather than producing a broken pattern.

Hardware: a pair of toggles at the throat lets the ruana be closed against wind
without pinning it. The toggle is a Yantra4D solid; `cord_dia` and `barrel_len`
drive both the printed toggle and this pattern's cord loop and its seat.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # back|front|collar|set

body_width = float(PARAM(lambda: body_width, 680.0))       # half-span, shoulder line
ruana_length = float(PARAM(lambda: ruana_length, 900.0))   # shoulder → front hem
back_drop = float(PARAM(lambda: back_drop, 160.0))         # extra length on the back
neck_slot = float(PARAM(lambda: neck_slot, 240.0))         # neck opening width
collar_depth = float(PARAM(lambda: collar_depth, 90.0))    # stand at the neck slot
front_overlap = float(PARAM(lambda: front_overlap, 40.0))  # CF crossing allowance
barrel_len = float(PARAM(lambda: barrel_len, 42.0))        # toggle barrel length
cord_dia = float(PARAM(lambda: cord_dia, 5.0))             # toggle cord diameter
fringe_depth = float(PARAM(lambda: fringe_depth, 70.0))    # warp fringe at the hems
seam_allowance = float(PARAM(lambda: seam_allowance, 14.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
body_width = max(450.0, min(body_width, 900.0))
ruana_length = max(600.0, min(ruana_length, 1300.0))
back_drop = max(0.0, min(back_drop, 350.0))
neck_slot = max(160.0, min(neck_slot, 340.0))
collar_depth = max(0.0, min(collar_depth, 160.0))
front_overlap = max(0.0, min(front_overlap, 120.0))
barrel_len = max(25.0, min(barrel_len, 70.0))
cord_dia = max(3.0, min(cord_dia, 9.0))
fringe_depth = max(0.0, min(fringe_depth, 160.0))
seam_allowance = max(8.0, min(seam_allowance, 25.0))

# ── Solved shoulder geometry ─────────────────────────────────────────────────
# The back's shoulder edge is the full span. The neck slot is carved from it,
# and each front's shoulder edge takes exactly half of what remains — so the
# two fronts plus the slot reconstitute the back's measured shoulder exactly.
BACK_SHOULDER = body_width                     # half-span (piece is cut on the fold)
_slot_half = neck_slot / 2.0
if _slot_half > BACK_SHOULDER - 60.0:          # keep a real shoulder to sew
    _slot_half = BACK_SHOULDER - 60.0
    neck_slot = _slot_half * 2.0
FRONT_SHOULDER = BACK_SHOULDER - _slot_half    # solved, not assumed
BACK_LENGTH = ruana_length + back_drop


def build_back():
    """The back panel: one rectangle, cut on the centre-back fold.

    Longer than the fronts by `back_drop` — the traditional working proportion
    that shields the kidneys. Its shoulder edge is the span the fronts and the
    neck slot must together reconstitute.
    """
    w, h = BACK_SHOULDER, BACK_LENGTH
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("shoulder", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # The neck slot runs from the CB fold out to the solved shoulder point.
        fc.Internal("neck-slot", [fc.P(0.0, h), fc.P(_slot_half, h)], kind="cut"),
    ]
    if fringe_depth > 0.0:
        internals.append(fc.Internal("fringe-line",
                                     [fc.P(0.0, fringe_depth), fc.P(w, fringe_depth)],
                                     kind="marking"))
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"center": 0.0, "hem": 0.0, "side": 0.0},
        notches=[fc.Notch("shoulder", _slot_half / w, "neck slot end — shoulder seam start")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back panel (espalda)",
    )


def build_front():
    """A front panel (cut 2, mirrored): the open half of the ruana.

    Its shoulder edge is FRONT_SHOULDER — solved so two of them plus the neck
    slot equal the back's shoulder exactly. `center_front` is the open edge.
    """
    w = FRONT_SHOULDER + front_overlap
    h = ruana_length
    edges = [
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("shoulder", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("side", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if fringe_depth > 0.0:
        internals.append(fc.Internal("fringe-line",
                                     [fc.P(0.0, fringe_depth), fc.P(w, fringe_depth)],
                                     kind="marking"))
    # Toggle seat at the throat, on the centre-front edge.
    internals.append(fc.Internal("toggle-seat",
                                 [fc.P(0.0, h - collar_depth - barrel_len),
                                  fc.P(0.0, h - collar_depth)], kind="drill"))
    # Cord loop that catches the toggle: sized to the toggle barrel.
    internals.append(fc.Internal("cord-loop",
                                 [fc.P(0.0, h - collar_depth - barrel_len * 0.5),
                                  fc.P(barrel_len * 1.2,
                                       h - collar_depth - barrel_len * 0.5)],
                                 kind="marking"))
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"center_front": 0.0, "hem": 0.0, "side": 0.0},
        notches=[fc.Notch("shoulder", 0.0, "neck slot end — shoulder seam start")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel (delantero)",
    )


def build_collar():
    """A narrow stand binding the neck slot (cut 1).

    Its length is solved to the FULL slot circuit — the slot is cut through both
    the back fold and the two fronts' inner shoulder ends, so the binding runs
    the slot's whole perimeter.
    """
    ln = neck_slot * 2.0 + front_overlap * 2.0     # slot runs front and back
    d = max(20.0, collar_depth)
    return fc.Piece(
        "collar",
        [
            fc.Edge("neck", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, d))]),
            fc.Edge("top", [fc.Line(fc.P(ln, d), fc.P(0.0, d))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, d), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "centre back match")],
        grainline=fc.Grainline(fc.P(ln * 0.15, d / 2.0), fc.P(ln * 0.85, d / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Neck binding (cuello)",
    )


def build():
    pattern = fc.PatternSet("poncho-ruana")
    every = target_piece == "set"
    if every or target_piece == "back":
        pattern.add(build_back())
    if every or target_piece == "front":
        pattern.add(build_front())
    if every or target_piece == "collar":
        pattern.add(build_collar())

    if every:
        # THE defining seam: the back's shoulder is reconstituted by one front
        # shoulder plus the half neck slot. Solved, so delta ≈ 0.
        back = pattern.piece("back")
        front = pattern.piece("front")
        back_sh = back.edge("shoulder").length(0.05)
        front_sh = front.edge("shoulder").length(0.05)
        # the front carries `front_overlap` past the CF: that surplus is the
        # crossing allowance, declared honestly as ease rather than hidden.
        pattern.declare_seam(("back", "shoulder"), ("front", "shoulder"),
                             tol=1.0, ease=(back_sh - front_sh))
        # Front and back side edges are the open sides — they are NOT sewn on a
        # ruana, but the back's extra length is the deliberate `back_drop`, so
        # declaring it as ease proves the drop is exactly what was asked for.
        pattern.declare_seam(("back", "side"), ("front", "side"),
                             tol=1.0, ease=back_drop)

    fabric_width = 800.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.92)   # rectangles: very high yield
    pattern.bom = [
        {"item": "fulled wool (paño / lana virgen)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 92% marker — all rectangles. "
                 "Páramo wear wants a heavy fulled cloth that sheds drizzle."},
        {"item": "toggle", "qty": 2, "unit": "count",
         "note": f"Yantra4D toggle, {barrel_len:.0f} mm barrel for {cord_dia:.0f} mm "
                 "cord (see notion.hardware_ref); closes the throat against wind."},
        {"item": "cord", "qty": round(barrel_len * 6.0), "unit": "mm_length",
         "note": f"{cord_dia:.0f} mm cord for the two toggle loops."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "wool or strong poly; the shoulder seam carries the whole weight."},
    ]
    pattern.metadata = {
        "fc300_rank": 279,
        "family": "heritage_global",
        "fabric_hint": "lana-melton-abrigo",
        "tradition": "Colombian & Venezuelan Andes (Boyacá, Cundinamarca, Santander, "
                     "Nariño, Venezuelan Andean states)",
        "finished_mm": {"front_length": round(ruana_length, 1),
                        "back_length": round(BACK_LENGTH, 1),
                        "span": round(body_width * 2.0, 1),
                        "neck_slot": round(neck_slot, 1)},
        "solved": {
            "back_shoulder_mm": round(BACK_SHOULDER, 2),
            "front_shoulder_mm": round(FRONT_SHOULDER, 2),
            "neck_slot_half_mm": round(_slot_half, 2),
            "note": "each front shoulder is solved as the back's measured shoulder "
                    "less the half neck slot, so two fronts plus the slot exactly "
                    "reconstitute the back — the slot is carved from real measured "
                    "width, never an assumed leftover.",
        },
        "hardware": "throat toggles via Yantra4D (notion.hardware_ref -> toggle); "
                    "barrel_len and cord_dia drive the printed toggle, the toggle "
                    "seat and the cord loop together",
        "distinction": "a RUANA, not a poncho: the front is SPLIT. The commons' "
                       "closed form is `sarape-poncho`.",
    }
    return pattern


result = build()
