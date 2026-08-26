"""
Roll-up Belt Keeper — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #370, Yantra4D-bridged belt-hanger).

The travelling belt organiser: a split-leather PANEL with a row of buckle SLOTS that belts
thread through, rolled from the tail end and closed by a stud STRAP, then hung from the
printed `belt-hanger` rack by a reinforced HANG tab. The rack is the Yantra4D belt-hanger
solid (notion.hardware_ref) — its hook count is driven by the same slot count this keeper
carries, so rack and roll always agree on how many belts.

Drafting note — the seam that must SOLVE: the slots must divide the panel into EQUAL
intervals with the first and last slot clear of the roll's ends, or a belt at the edge
falls out when the roll is stood on end. The slot pitch is SOLVED from the measured panel
run and the requested count (recomputed so the row lands exactly on both clearances), not
accumulated — the same land-exactly discipline the magnetic placket uses for its magnet
column.

Pieces:
  - panel : the belt roll body (cut 1); slots and roll lines marked.
  - strap : the stud closure strap (cut 1).
  - hang  : the reinforced tab that engages the belt-hanger hook (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # panel|strap|hang|set

panel_width = float(PARAM(lambda: panel_width, 380.0))    # across the belts' width
panel_length = float(PARAM(lambda: panel_length, 260.0))  # head (hang) to tail (roll)
belt_count = float(PARAM(lambda: belt_count, 5.0))        # number of buckle slots
slot_width = float(PARAM(lambda: slot_width, 42.0))       # a buckle's width through the slot
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
panel_width = max(200.0, min(panel_width, 520.0))
panel_length = max(160.0, min(panel_length, 400.0))
belt_count = max(2.0, min(round(belt_count), 9))
slot_width = max(24.0, min(slot_width, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

N_SLOTS = int(belt_count)
# The slot row runs across the panel width, clear of both side edges.
SIDE_CLEAR = max(30.0, panel_width * 0.08)
SLOT_RUN = panel_width - 2.0 * SIDE_CLEAR
# Whole intervals, then the pitch RECOMPUTED so the row lands exactly on both
# clearances instead of drifting.
N_INTERVALS = max(1, N_SLOTS - 1)
SLOT_PITCH = SLOT_RUN / N_INTERVALS if N_SLOTS > 1 else 0.0
SLOT_X0 = SIDE_CLEAR
# The slot must be at least the buckle width; if the pitch is tighter than the slot
# width the slots would overlap, so the slot length is clamped under the pitch.
SLOT_LEN = min(slot_width, max(20.0, SLOT_PITCH * 0.8)) if N_SLOTS > 1 else slot_width


def _slot_xs():
    return [SLOT_X0 + SLOT_PITCH * i for i in range(N_SLOTS)]


def build_panel():
    """The belt roll body. `hang_edge` (head) takes the hang tabs; `tail_edge` is
    where the roll starts; the slot row is marked across."""
    w, h = panel_width, panel_length
    edges = [
        fc.Edge("tail_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("hang_edge", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    slot_y = h * 0.5
    internals = [fc.Internal("roll-line", [fc.P(0.0, h * 0.22), fc.P(w, h * 0.22)],
                             kind="marking")]
    for i, x in enumerate(_slot_xs()):
        internals.append(fc.Internal(
            f"belt-slot-{i + 1}",
            [fc.P(x - SLOT_LEN / 2.0, slot_y), fc.P(x + SLOT_LEN / 2.0, slot_y)],
            kind="drill"))
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hang_edge", 0.33, "hang tab"),
                 fc.Notch("hang_edge", 0.67, "hang tab"),
                 fc.Notch("tail_edge", 0.5, "roll start")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Belt roll panel",
    )


STRAP_LEN = max(160.0, panel_length * 0.9)
STRAP_W = 36.0


def build_strap():
    """The stud closure strap: `attach` sews to the panel tail edge centre (a short
    strap, tacked, so it is cut narrow, not to the full width)."""
    ln, w = STRAP_LEN, STRAP_W
    return fc.Piece(
        "strap", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "tail centre")],
        grainline=fc.Grainline(fc.P(16.0, w * 0.5), fc.P(ln - 16.0, w * 0.5)),
        internals=[fc.Internal("stud-hole", [fc.P(ln - 28.0, w * 0.5),
                                             fc.P(ln - 12.0, w * 0.5)], kind="drill")],
        cut=fc.CutSpec(quantity=1),
        label="Stud closure strap",
    )


HANG_W = max(44.0, slot_width * 1.1)
HANG_H = max(60.0, panel_length * 0.24)


def build_hang():
    """The reinforced hang tab that engages a belt-hanger hook (cut 2, doubled)."""
    w, h = HANG_W, HANG_H
    return fc.Piece(
        "hang", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "match panel hang notch")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=[fc.Internal("hook-hole", [fc.P(w * 0.5 - 8.0, h * 0.6),
                                             fc.P(w * 0.5 + 8.0, h * 0.6)], kind="drill")],
        cut=fc.CutSpec(quantity=2),
        label="Hang tab",
    )


def build():
    pattern = fc.PatternSet("belt-roll-keeper")
    everything = target_piece == "set"
    if everything or target_piece == "panel":
        pattern.add(build_panel())
    if everything or target_piece == "strap":
        pattern.add(build_strap())
    if everything or target_piece == "hang":
        pattern.add(build_hang())

    if everything:
        # The two hang tabs are doubled face-to-face: their side and top edges match.
        pattern.declare_seam(("hang", "side_r"), ("hang", "side_r"), tol=0.5)
        pattern.declare_seam(("hang", "side_l"), ("hang", "side_l"), tol=0.5)
        pattern.declare_seam(("hang", "top"), ("hang", "top"), tol=0.5)
        # The strap and hang tabs are tacked to the panel edges in construction (short
        # attachments, not full-width seams), so they are not declared here.

    fabric_width = 900.0   # split leather is sold by hide, but the marker note holds
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "split leather or waxed canvas", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 900 mm width, 60% marker (leather nests loosely); a firm hand "
                 "holds the slot shape so a threaded buckle does not sag it out."},
        {"item": "belt hanger rack", "qty": 1, "unit": "count",
         "note": f"Yantra4D belt-hanger (notion.hardware_ref): {N_SLOTS} hooks, one per "
                 f"belt slot — the rack's hook_count is driven by this belt_count."},
        {"item": "line-24 snap or stud", "qty": 1, "unit": "count",
         "note": "closes the stud strap once the roll is made."},
        {"item": "waxed thread", "qty": 1, "unit": "spool",
         "note": "saddle-stitch the hang tabs; they carry the whole loaded roll."},
    ]
    pattern.metadata = {
        "fc400_rank": 370,
        "family": "care_and_keeping",
        "fabric_hint": "mezclilla-denim",
        "finished_mm": {"panel_width": round(panel_width, 1),
                        "panel_length": round(panel_length, 1),
                        "belt_count": N_SLOTS},
        "solved": {
            "slot_run_mm": round(SLOT_RUN, 2),
            "slot_pitch_mm": round(SLOT_PITCH, 2),
            "slot_length_mm": round(SLOT_LEN, 2),
            "side_clear_mm": round(SIDE_CLEAR, 2),
            "note": "the slot pitch is RECOMPUTED from whole intervals across the "
                    "measured slot run so the row lands exactly on both side "
                    "clearances instead of drifting; the slot length is clamped under "
                    "the pitch so slots never overlap at a high belt count.",
        },
        "hardware": "printed belt rack via Yantra4D (notion.hardware_ref -> "
                    "belt-hanger); hook_count = belt_count. Logged co-create in the "
                    "FC-400 index; linked live here.",
    }
    return pattern


result = build()
