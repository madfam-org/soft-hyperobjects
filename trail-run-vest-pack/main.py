"""
Trail-running vest pack — Fashion Cabinet Garment Cartridge
(FC-500 rank #451, active_swim, Yantra4D-bridged side-release-buckle).

The trail runner's hydration vest: a light stretch-mesh vest that hugs the torso like a second
skin and carries soft flasks and food in front pockets, closing across the sternum on
side-release buckles on adjustable webbing so it holds no matter how the ribcage moves running.
Not a garment for warmth — a load-carrying vest cut at negative ease so the load does not bounce.

Two real decisions:

  1. THE STERNUM STRAP IS SOLVED TO THE CHEST — THE DIMENSIONAL HANDSHAKE. The front panels close
     on webbing across the sternum; the webbing width is the drafted webbing_w that drives BOTH
     the Yantra4D side-release-buckle webbing channel AND the garment's sternum-strap interface.

  2. NEGATIVE EASE, CLAMPED POCKET. The vest is cut smaller than the chest so the load rides
     close; the front pocket depth is clamped under the front length so the pocket can never run
     past the hem.

Pieces: front (cut 2, pockets), back (cut 1, mesh), strap (cut 2, sternum webbing). Made to
measure to chest, torso length. FC-500 lane 6 (active).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|strap|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))
torso_length = float(PARAM(lambda: torso_length, 420.0))    # shoulder to vest hem
pocket_depth = float(PARAM(lambda: pocket_depth, 180.0))
strap_count = float(PARAM(lambda: strap_count, 2.0))
webbing_w = float(PARAM(lambda: webbing_w, 25.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(720.0, min(chest_girth, 1400.0))
torso_length = max(300.0, min(torso_length, 560.0))
pocket_depth = max(80.0, min(pocket_depth, 300.0))
strap_count = max(1.0, min(round(strap_count), 4.0))
webbing_w = max(15.0, min(webbing_w, 40.0))
negative_ease_pct = max(4.0, min(negative_ease_pct, 20.0))
seam_allowance = max(4.0, min(seam_allowance, 12.0))

NEG = 1.0 - negative_ease_pct / 100.0
CHEST_FIN = chest_girth * NEG
FRONT_W = CHEST_FIN / 4.0                     # each front panel
BACK_W = CHEST_FIN / 2.0
POCKET = min(pocket_depth, torso_length * 0.75)


def build_front():
    """Front panel (cut 2): shoulder at top, armhole, side, hem; a pocket window; the CF edge
    carries the sternum straps."""
    w = FRONT_W
    h = torso_length
    edges = [
        fc.Edge("shoulder", [fc.Line(fc.P(0.0, h), fc.P(w * 0.5, h))]),
        fc.Edge("armhole", [fc.Bezier(fc.P(w * 0.5, h), fc.P(w, h - h * 0.25),
                                      fc.P(w, h - h * 0.40), fc.P(w, h - h * 0.5))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - h * 0.5), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance, allowances={"hem": 12.0},
        notches=[fc.Notch("armhole", 0.5, "shoulder"), fc.Notch("center_front", 0.5, "strap")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[fc.Internal("flask-pocket", [fc.P(w * 0.15, h * 0.2),
                                                fc.P(w * 0.15, h * 0.2 + POCKET)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label="Front (flask pockets)")


def build_back():
    """Back mesh panel (cut 1 on fold). Two armholes, one neckline notch."""
    w = BACK_W
    h = torso_length
    # The neckline spans the centre-back to the neck point; the shoulder runs from the neck point
    # to the shoulder point and matches ONE front shoulder (each front = a quarter of the ring).
    neck_x = FRONT_W * 0.5                        # == one front's shoulder run start
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Line(fc.P(0.0, h), fc.P(neck_x, h))]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_x, h), fc.P(neck_x + FRONT_W * 0.5, h))]),
        fc.Edge("armhole", [fc.Bezier(fc.P(neck_x + FRONT_W * 0.5, h), fc.P(w, h - h * 0.25),
                                      fc.P(w, h - h * 0.40), fc.P(w, h - h * 0.5))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - h * 0.5), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance, allowances={"hem": 12.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "shoulder"), fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[fc.Internal("bladder-pocket", [fc.P(w * 0.3, h * 0.25), fc.P(w * 0.7, h * 0.25)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (mesh, bladder pocket)")


def build_strap():
    """A sternum strap (cut 2 per side): webbing carrying the side-release buckle."""
    ln = max(80.0, FRONT_W * 0.7)
    w = webbing_w
    return fc.Piece(
        "strap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("attach", 0.5, "front edge")],
        grainline=fc.Grainline(fc.P(ln * 0.5, w * 0.3), fc.P(ln * 0.5, w * 0.7)),
        internals=[fc.Internal("buckle-slot", [fc.P(ln * 0.85, w * 0.3), fc.P(ln * 0.85, w * 0.7)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=int(strap_count) * 2, mirror=True), label="Sternum strap (webbing)")


def build():
    pattern = fc.PatternSet("trail-run-vest-pack")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    strap = build_strap()
    picked = {"front": front, "back": back, "strap": strap}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, strap):
        pattern.add(piece)
    pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "stretch power mesh + ripstop pocket cloth", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a breathable stretch-mesh body at negative ease with ripstop-faced front "
                 "pockets for soft flasks."},
        {"item": "side-release buckles (Yantra4D side-release-buckle)", "qty": int(strap_count) * 2,
         "unit": "piece",
         "note": f"{int(strap_count)} sternum closures, webbing {webbing_w:.0f} mm = the "
                 "webbing_w that drives the sternum-strap interface AND the buckle's webbing "
                 "channel; the buckle solid is Yantra4D, never modelled here."},
        {"item": "elastic webbing", "qty": round(FRONT_W * strap_count * 2.0 + 100.0),
         "unit": "mm_length",
         "note": "the adjustable sternum webbing that carries the buckles across the chest."},
        {"item": "flatlock thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "flatlock every seam so a loaded vest never chafes over hours on the trail."},
    ]
    pattern.metadata = {
        "fc500_rank": 451, "family": "active_swim", "fabric_hint": "nylon-ripstop",
        "silhouette_note": "A trail-running hydration vest: stretch-mesh body at negative ease, "
            "front flask pockets, sternum side-release buckles on adjustable webbing.",
        "hardware": "sternum side-release buckles via Yantra4D (notion.hardware_ref -> "
            "side-release-buckle); webbing_w drives the sternum-strap interface AND the webbing "
            "channel — the dimensional handshake.",
        "solver": {
            "pocket_mm": round(POCKET, 1), "chest_finished_mm": round(CHEST_FIN, 1),
            "note": "the front pocket depth is clamped under 0.75x the front length so it never "
                    "runs past the hem; the vest is cut at negative ease so the load rides close.",
        },
        "active": {"use": "trail and ultra running; carries soft flasks and food front and centre, "
                   "held tight to the ribs by the sternum buckles so nothing bounces."},
    }
    return pattern


result = build()
