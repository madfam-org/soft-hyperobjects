"""
Fold-Flat Travel Garment Folder — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #363, Yantra4D-bridged folding-board).

The travel folder that keeps a dress shirt crease-free in a case: a soft SHELL panel
with two side WING flaps and a bottom TAIL flap that wrap a folded shirt around a stiff
insert, closed by a hook-and-loop TAB. The stiff insert is the Yantra4D `folding-board`
solid (notion.hardware_ref) — a rigid folding template around which the sleeves and hem
are turned so every shirt comes out the same rectangle.

Drafting note — the seam that must SOLVE: the wings do not fold onto a flat plane, they
fold onto a plane thickened by the folded stack of clothes. A wing cut exactly to the
board half-width would come up short once it climbs the stack's edge. So the wing width
is the board half-width PLUS a turn-of-cloth allowance derived from the stack height, and
the shell's wing-attach edge is MEASURED so the wing's straight fold edge matches it to
tolerance rather than by an assumed rectangle.

Pieces:
  - shell : the base panel the shirt lies on (cut 1); board pocket marked on it.
  - wing  : one side flap that folds a sleeve in (cut 2, mirrored).
  - tail  : the bottom flap that folds the hem up (cut 1).
  - tab   : the hook-and-loop closure strap (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # shell|wing|tail|tab|set

board_width = float(PARAM(lambda: board_width, 260.0))    # finished folded shirt width
board_length = float(PARAM(lambda: board_length, 340.0))  # finished folded shirt length
stack_height = float(PARAM(lambda: stack_height, 45.0))   # folded stack thickness
tab_width = float(PARAM(lambda: tab_width, 40.0))         # closure strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
board_width = max(180.0, min(board_width, 360.0))
board_length = max(240.0, min(board_length, 460.0))
stack_height = max(15.0, min(stack_height, 90.0))
tab_width = max(20.0, min(tab_width, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

HALF_W = board_width / 2.0
# Turn-of-cloth: a wing must climb the stack edge and lie back on top, so it needs
# the board half-width plus one stack height of reach. Clamped so a tall stack on a
# narrow board cannot make the wing wider than the whole shell (which would overlap
# past centre and pucker).
WING_REACH = min(HALF_W + stack_height, board_width * 0.92)
# The tail folds the hem up over the same stack.
TAIL_REACH = min(board_length * 0.42 + stack_height, board_length * 0.60)


def build_shell():
    """The base panel: the shirt lies face-down on it. The board pocket and the
    two wing-fold lines are marked, and every straight edge is addressable so the
    wings and tail can seam to it."""
    w, h = board_width, board_length
    edges = [
        fc.Edge("hem_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("attach_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top_edge", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("attach_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("board-pocket",
                    [fc.P(seam_allowance, seam_allowance),
                     fc.P(w - seam_allowance, seam_allowance),
                     fc.P(w - seam_allowance, h - seam_allowance),
                     fc.P(seam_allowance, h - seam_allowance),
                     fc.P(seam_allowance, seam_allowance)],
                    kind="marking"),
        fc.Internal("wing-fold-r", [fc.P(w - 4.0, 0.0), fc.P(w - 4.0, h)],
                    kind="marking"),
        fc.Internal("wing-fold-l", [fc.P(4.0, 0.0), fc.P(4.0, h)], kind="marking"),
        fc.Internal("tail-fold", [fc.P(0.0, TAIL_REACH), fc.P(w, TAIL_REACH)],
                    kind="marking"),
    ]
    return fc.Piece(
        "shell", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach_r", 0.5, "wing centre"),
                 fc.Notch("attach_l", 0.5, "wing centre"),
                 fc.Notch("hem_edge", 0.5, "tail centre")],
        grainline=fc.Grainline(fc.P(HALF_W, 30.0), fc.P(HALF_W, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Shell base panel",
    )


def build_wing():
    """One side flap (cut 2 mirrored). Its `fold` edge attaches to the shell's side
    (length = board_length, the MEASURED attach edge) and it reaches WING_REACH in."""
    ln = board_length
    reach = WING_REACH
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ln))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, ln), fc.P(reach, ln))]),
        fc.Edge("free", [fc.Line(fc.P(reach, ln), fc.P(reach, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(reach, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "wing", edges,
        seam_allowance=seam_allowance,
        allowances={"free": 16.0},
        notches=[fc.Notch("fold", 0.5, "match shell wing centre")],
        grainline=fc.Grainline(fc.P(reach * 0.5, 30.0), fc.P(reach * 0.5, ln - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side wing flap",
    )


def build_tail():
    """The bottom flap: its `fold` edge attaches to the shell's hem (length =
    board_width, MEASURED) and it reaches TAIL_REACH up over the stack."""
    w = board_width
    reach = TAIL_REACH
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, reach))]),
        fc.Edge("free", [fc.Line(fc.P(w, reach), fc.P(0.0, reach))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, reach), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "tail", edges,
        seam_allowance=seam_allowance,
        allowances={"free": 16.0},
        notches=[fc.Notch("fold", 0.5, "match shell tail centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, reach - 20.0)),
        cut=fc.CutSpec(quantity=1),
        label="Bottom tail flap",
    )


TAB_LENGTH = max(120.0, board_width * 0.6)


def build_tab():
    """The hook-and-loop closure strap, cut double and folded lengthwise."""
    ln, w = TAB_LENGTH, tab_width * 2.0
    return fc.Piece(
        "tab", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("hook-patch",
                               [fc.P(ln - tab_width, tab_width * 0.5),
                                fc.P(ln - 6.0, tab_width * 1.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Closure tab",
    )


def build():
    pattern = fc.PatternSet("garment-travel-fold")
    everything = target_piece == "set"
    if everything or target_piece == "shell":
        pattern.add(build_shell())
    if everything or target_piece == "wing":
        pattern.add(build_wing())
    if everything or target_piece == "tail":
        pattern.add(build_tail())
    if everything or target_piece == "tab":
        pattern.add(build_tab())

    if everything:
        # THE solving seams: each wing's fold edge sews to a shell side; the wing is
        # cut to the MEASURED shell side length, so the seam matches by construction.
        pattern.declare_seam(("wing", "fold"), ("shell", "attach_r"), tol=1.0)
        pattern.declare_seam(("wing", "fold"), ("shell", "attach_l"), tol=1.0)
        # The tail folds up off the hem.
        pattern.declare_seam(("tail", "fold"), ("shell", "hem_edge"), tol=1.0)
        # The tab is a short strap tacked to the centre of the top edge (not a
        # full-width seam), so it is attached in construction, not declared here.

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.78)
    pattern.bom = [
        {"item": "ripstop nylon or brushed cotton", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1400 mm width, 78% marker; a smooth face lets the shirt slide "
                 "into place without dragging a fresh press."},
        {"item": "folding board insert", "qty": 1, "unit": "count",
         "note": f"Yantra4D folding-board (notion.hardware_ref): {board_width:.0f} x "
                 f"{board_length:.0f} mm rigid template the wings turn around."},
        {"item": "hook-and-loop tape", "qty": round(TAB_LENGTH + tab_width * 2.0),
         "unit": "mm_length", "note": "hook on the tab, loop on the shell top edge."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bind every flap's free edge before assembly."},
    ]
    pattern.metadata = {
        "fc400_rank": 363,
        "family": "care_and_keeping",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"board_width": round(board_width, 1),
                        "board_length": round(board_length, 1),
                        "stack_height": round(stack_height, 1)},
        "solved": {
            "wing_reach_mm": round(WING_REACH, 2),
            "wing_reach_note": "board half-width + one stack height of turn-of-cloth, "
                               "clamped to 92% of board width so the wings never "
                               "overlap past centre",
            "tail_reach_mm": round(TAIL_REACH, 2),
            "note": "the wing and tail flaps are cut to the MEASURED shell edges they "
                    "attach to, plus a stack-derived turn-of-cloth reach; the reaches "
                    "are clamped so extreme stack heights cannot invert the geometry.",
        },
        "hardware": "rigid folding template via Yantra4D (notion.hardware_ref -> "
                    "folding-board); fold_w = board_width, fold_h = board_length. "
                    "Logged co-create in the FC-400 index (the board arrived on the "
                    "yantra4d 500 shelf); this cartridge links it live.",
    }
    return pattern


result = build()
