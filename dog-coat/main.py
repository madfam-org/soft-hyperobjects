"""
Dog Coat — Fashion Cabinet Garment Cartridge (FC-300 #242, technical & outdoor).

A working dog's coat: a shaped back panel that covers spine to flank, a belly strap that
passes under the ribs, and a chest strap that closes ahead of the shoulder — both strapped
with hook-and-loop tape so the coat goes on and off over a harness with cold hands and no
buckles to freeze. The panel is cut on the spine fold with a neck scoop and a tail taper,
so it lies flat over a moving back instead of bunching at the shoulder.

The hook-and-loop tape solid is Yantra4D territory (`hook-loop-tape`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the coat — the panel solved to the dog's back
length, chest girth, and neck girth, the strap runs, the tape placement.

The bridge is dimensional and enforced: `tape_width` and `tape_run` drive the tape's sewn
`sew_face` flange AND this garment's `tape_run` interface, so the tape's sewn edge and the
strap's sewn edge share one dimension.

Pieces:
  - panel : the shaped back panel (cut 1 on the spine fold), tape zones marked.
  - belly : the belly strap that passes under the ribs (cut 2).
  - chest : the chest strap that closes ahead of the shoulder (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))       # panel|belly|chest|set

back_length  = float(PARAM(lambda: back_length, 550.0))      # withers to tail base
chest_girth  = float(PARAM(lambda: chest_girth, 720.0))      # deepest girth behind the legs
neck_girth   = float(PARAM(lambda: neck_girth, 460.0))       # base-of-neck girth
flank_drop   = float(PARAM(lambda: flank_drop, 210.0))       # how far down the flank it covers
coat_ease    = float(PARAM(lambda: coat_ease, 90.0))         # ease over the coat/harness
tape_width   = float(PARAM(lambda: tape_width, 38.0))        # hook-loop tape width
tape_run     = float(PARAM(lambda: tape_run, 110.0))         # tape run per closure
strap_width  = float(PARAM(lambda: strap_width, 55.0))       # belly/chest strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
back_length  = max(200.0, min(back_length, 900.0))
chest_girth  = max(300.0, min(chest_girth, 1200.0))
neck_girth   = max(200.0, min(neck_girth, 800.0))
flank_drop   = max(80.0, min(flank_drop, 400.0))
coat_ease    = max(20.0, min(coat_ease, 220.0))
tape_width   = max(16.0, min(tape_width, 70.0))
tape_run     = max(40.0, min(tape_run, 260.0))
strap_width  = max(25.0, min(strap_width, 110.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The panel is cut on the spine fold, so the drafted width is a HALF drop.
HALF_DROP  = flank_drop
NECK_HALF  = (neck_girth + coat_ease) / 4.0     # quarter neck at the panel's front edge
L = back_length
# Strap runs: half the chest girth plus ease and the tape overlap, per strap half.
BELLY_RUN = (chest_girth + coat_ease) / 2.0 - HALF_DROP + tape_run
CHEST_RUN = (neck_girth + coat_ease) / 2.0 - NECK_HALF + tape_run


def build_panel():
    """The shaped back panel, cut on the spine fold.

    y = 0 is the tail end, y = L the withers/neck end. x = 0 is the spine (the fold);
    x grows down the flank.
    """
    tail_pt   = fc.P(HALF_DROP * 0.55, 0.0)
    flank_pt  = fc.P(HALF_DROP, L * 0.55)
    neck_pt   = fc.P(NECK_HALF, L)
    internals = [
        fc.Internal("belly-strap-place",
                    [fc.P(HALF_DROP * 0.7, L * 0.36 - strap_width / 2.0),
                     fc.P(HALF_DROP, L * 0.36 - strap_width / 2.0)], kind="marking"),
        fc.Internal("chest-strap-place",
                    [fc.P(NECK_HALF * 0.9, L - strap_width),
                     fc.P(HALF_DROP * 0.8, L - strap_width)], kind="marking"),
        # The tape zones on the panel side of each closure.
        fc.Internal("tape-zone-belly",
                    [fc.P(HALF_DROP - tape_run, L * 0.36 - tape_width / 2.0),
                     fc.P(HALF_DROP, L * 0.36 - tape_width / 2.0),
                     fc.P(HALF_DROP, L * 0.36 + tape_width / 2.0),
                     fc.P(HALF_DROP - tape_run, L * 0.36 + tape_width / 2.0),
                     fc.P(HALF_DROP - tape_run, L * 0.36 - tape_width / 2.0)], kind="marking"),
    ]
    return fc.Piece(
        "panel",
        [
            fc.Edge("spine", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, L), neck_pt, bulge=0.16, side=-1.0)]),
            fc.Edge("flank", [fc.curve_through(neck_pt, flank_pt, bulge=0.12, side=1.0),
                              fc.curve_through(flank_pt, tail_pt, bulge=0.10, side=1.0)]),
            fc.Edge("tail", [fc.Line(tail_pt, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"flank": 16.0, "tail": 16.0},
        notches=[fc.Notch("spine", 0.36, "belly strap"),
                 fc.Notch("spine", 0.92, "chest strap"),
                 fc.Notch("flank", 0.5, "flank apex")],
        grainline=fc.Grainline(fc.P(HALF_DROP * 0.35, 20.0), fc.P(HALF_DROP * 0.35, L - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="spine", mirror=True),
        label="Back panel",
    )


def _strap(name, run, label):
    """A strap with a hook-loop tape zone at its free end."""
    internals = [
        fc.Internal("tape-zone",
                    [fc.P(run - tape_run, strap_width / 2.0 - tape_width / 2.0),
                     fc.P(run, strap_width / 2.0 - tape_width / 2.0),
                     fc.P(run, strap_width / 2.0 + tape_width / 2.0),
                     fc.P(run - tape_run, strap_width / 2.0 + tape_width / 2.0),
                     fc.P(run - tape_run, strap_width / 2.0 - tape_width / 2.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        name,
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_width))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, strap_width), fc.P(run, strap_width))]),
            fc.Edge("free_end", [fc.Line(fc.P(run, strap_width), fc.P(run, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(run, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", (run - tape_run) / run, "tape start")],
        grainline=fc.Grainline(fc.P(run * 0.15, strap_width / 2.0),
                               fc.P(run * 0.85, strap_width / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("dog-coat")
    everything = target_piece == "set"
    if everything or target_piece == "panel":
        pattern.add(build_panel())
    if everything or target_piece == "belly":
        pattern.add(_strap("belly", BELLY_RUN, "Belly strap"))
    if everything or target_piece == "chest":
        pattern.add(_strap("chest", CHEST_RUN, "Chest strap"))
    if everything:
        # Each strap's attach end is caught in the panel's flank seam; the pair of
        # mirrored straps meets free end to free end on the tape.
        pattern.declare_seam(("belly", "attach"), ("belly", "free_end"), tol=1.0)
        pattern.declare_seam(("chest", "attach"), ("chest", "free_end"), tol=1.0)
        # Both straps are the same width where they land on the panel.
        pattern.declare_seam(("belly", "attach"), ("chest", "attach"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "waterproof shell + fleece lining",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 70% marker; shell out, fleece against the coat."},
        {"item": "hook-and-loop tape", "qty": round(tape_run * 4.0), "unit": "mm_length",
         "note": "Yantra4D hook-loop-tape (see notion.hardware_ref); hook on the strap, "
                 "loop on the panel so the hooks never face the dog."},
        {"item": "reflective binding", "qty": round(L * 2.0 + flank_drop * 2.0),
         "unit": "mm_length", "note": "bind the flank and tail edges; a working dog is seen."},
        {"item": "polyester thread", "qty": 1, "unit": "spool",
         "note": "bar-tack the strap roots — they take the whole pull."},
    ]
    pattern.metadata = {
        "fc300_rank": 242, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A shaped back panel cut on the spine fold with a neck scoop and tail "
            "taper so it lies flat over a moving back, closed by belly and chest straps on "
            "hook-and-loop tape that a cold hand can work over an existing harness.",
        "solved": {"half_drop_mm": round(HALF_DROP, 1), "neck_quarter_mm": round(NECK_HALF, 1),
                   "belly_run_mm": round(BELLY_RUN, 1), "chest_run_mm": round(CHEST_RUN, 1)},
        "hardware": "hook-and-loop closures via Yantra4D "
                    "(notion.hardware_ref -> hook-loop-tape)",
    }
    return pattern


result = build()
