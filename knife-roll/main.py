"""
Knife Roll — Fashion Cabinet Accessory Cartridge (FC-300 #240, technical & outdoor).

The chef's / bushcraft knife roll: the tool roll's harder sibling. Where a tool roll
divides one strip into pockets, a knife roll builds PADDED SLOTS — each blade rides in
its own batting-quilted channel so edges never touch each other or the cloth — under a
long tip flap that folds down past every point, and the whole thing rolls and ties on a
cord whose ends carry pressed-on tips.

The cord-end solid is Yantra4D territory (`cord-end`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the roll — the slot pitch solved to the blade
list, the padded panel, the flap drop, the tie run. The bridge is dimensional:
`cord_dia` drives the cord-end's sewn mouth flange AND this garment's `tie_closure`
interface, so the tip is sized to the cord the roll actually ties with.

Pieces:
  - body    : the padded back panel with the tip flap; quilt and slot lines marked.
  - slots   : the slot strip that forms the padded blade channels.
  - batting : the batting layer quilted between body and slots.
  - tie     : the tie tab that carries the cord (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))      # body|slots|batting|tie|set

slots        = int(PARAM(lambda: slots, 6))                 # blades carried
slot_width   = float(PARAM(lambda: slot_width, 62.0))       # widest blade at the heel
slot_height  = float(PARAM(lambda: slot_height, 230.0))     # slot depth up the panel
blade_length = float(PARAM(lambda: blade_length, 330.0))    # longest blade, tip to butt
flap_drop    = float(PARAM(lambda: flap_drop, 120.0))       # tip flap past the points
pad_ease     = float(PARAM(lambda: pad_ease, 10.0))         # ease per slot for the batting
cord_dia     = float(PARAM(lambda: cord_dia, 6.0))          # tie cord diameter
tie_width    = float(PARAM(lambda: tie_width, 30.0))        # tie tab width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
slots        = max(2, min(slots, 16))
slot_width   = max(25.0, min(slot_width, 140.0))
slot_height  = max(90.0, min(slot_height, 400.0))
blade_length = max(140.0, min(blade_length, 600.0))
flap_drop    = max(40.0, min(flap_drop, 260.0))
pad_ease     = max(4.0, min(pad_ease, 40.0))
cord_dia     = max(3.0, min(cord_dia, 12.0))
tie_width    = max(16.0, min(tie_width, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 24.0))

PITCH = slot_width + pad_ease               # slot pitch across the roll
ROW_RUN = PITCH * slots
MARGIN = 25.0
BODY_W = ROW_RUN + 2.0 * MARGIN
BODY_H = blade_length + flap_drop + 40.0
# The slot strip carries the padding wrap, so it runs longer than the row.
STRIP_RUN = ROW_RUN + pad_ease * slots


def build_body():
    """The padded back panel with the tip flap folding down past every point."""
    internals = [
        fc.Internal("flap-fold",
                    [fc.P(0.0, BODY_H - flap_drop), fc.P(BODY_W, BODY_H - flap_drop)],
                    kind="fold"),
        fc.Internal("slot-top",
                    [fc.P(MARGIN, slot_height + MARGIN),
                     fc.P(BODY_W - MARGIN, slot_height + MARGIN)], kind="marking"),
    ]
    for i in range(1, slots):
        x = MARGIN + PITCH * i
        internals.append(fc.Internal(
            "slot-line", [fc.P(x, MARGIN), fc.P(x, slot_height + MARGIN)], kind="marking"))
    # Quilt lines across the padded field — they hold the batting off the edges.
    for i in (1, 2, 3):
        y = MARGIN + slot_height * i / 4.0
        internals.append(fc.Internal(
            "quilt-line", [fc.P(MARGIN, y), fc.P(BODY_W - MARGIN, y)], kind="marking"))
    return fc.Piece(
        "body",
        [
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BODY_H))]),
            fc.Edge("flap_edge", [fc.Line(fc.P(0.0, BODY_H), fc.P(BODY_W, BODY_H))]),
            fc.Edge("right", [fc.Line(fc.P(BODY_W, BODY_H), fc.P(BODY_W, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(BODY_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", (slot_height + MARGIN) / BODY_H, "slot top"),
                 fc.Notch("left", (BODY_H - flap_drop) / BODY_H, "flap fold"),
                 fc.Notch("right", 0.5, "tie tab")],
        grainline=fc.Grainline(fc.P(BODY_W * 0.5, MARGIN), fc.P(BODY_W * 0.5, BODY_H - MARGIN)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Padded body + tip flap",
    )


def build_slots():
    """The slot strip: stitched down at each slot line to form padded blade channels."""
    internals = []
    for i in range(1, slots):
        x = PITCH * i + pad_ease * (i - 0.5)
        internals.append(fc.Internal(
            "slot-match", [fc.P(x, 0.0), fc.P(x, slot_height)], kind="marking"))
    return fc.Piece(
        "slots",
        [
            fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, slot_height))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, slot_height), fc.P(STRIP_RUN, slot_height))]),
            fc.Edge("end_b", [fc.Line(fc.P(STRIP_RUN, slot_height), fc.P(STRIP_RUN, 0.0))]),
            fc.Edge("attach", [fc.Line(fc.P(STRIP_RUN, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 20.0},
        notches=[fc.Notch("attach", 0.0, "row start"), fc.Notch("attach", 1.0, "row end")],
        grainline=fc.Grainline(fc.P(STRIP_RUN * 0.5, 10.0),
                               fc.P(STRIP_RUN * 0.5, slot_height - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Padded slot strip",
    )


def build_batting():
    """The batting layer quilted between the body and the slot strip."""
    w = ROW_RUN
    h = slot_height
    return fc.Piece(
        "batting",
        [
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", 0.5, "batting centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        cut=fc.CutSpec(quantity=1),
        label="Batting layer",
    )


def build_tie():
    """The tie tab carrying the cord whose ends take the Yantra4D cord-end tips."""
    length = BODY_H * 0.5
    return fc.Piece(
        "tie",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(tie_width, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(tie_width, 0.0), fc.P(tie_width, length))]),
            fc.Edge("cord_end", [fc.Line(fc.P(tie_width, length), fc.P(0.0, length))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, length), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_r", 0.5, "cord channel")],
        grainline=fc.Grainline(fc.P(tie_width / 2.0, length * 0.15),
                               fc.P(tie_width / 2.0, length * 0.85)),
        internals=[fc.Internal("cord-channel",
                               [fc.P(tie_width / 2.0 - cord_dia, 8.0),
                                fc.P(tie_width / 2.0 - cord_dia, length - 8.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Tie tab",
    )


def build():
    pattern = fc.PatternSet("knife-roll")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "slots":
        pattern.add(build_slots())
    if everything or target_piece == "batting":
        pattern.add(build_batting())
    if everything or target_piece == "tie":
        pattern.add(build_tie())
    if everything:
        # The slot strip's ends are caught in the body's side seams (balanced pair).
        pattern.declare_seam(("slots", "end_a"), ("slots", "end_b"), tol=1.0)
        # The batting sits exactly across the slot row, its top matching its bottom.
        pattern.declare_seam(("batting", "top"), ("batting", "bottom"), tol=1.0)
        # The tie tabs are caught in the body's right-hand seam.
        pattern.declare_seam(("tie", "attach"), ("tie", "cord_end"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "waxed canvas / heavy duck (outer) + cotton twill (slots)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; natural fibres so blades do not sweat."},
        {"item": "cotton or wool batting, 6–8 mm", "qty": 1, "unit": "pc",
         "note": "quilted between body and slots; keeps edges off each other."},
        {"item": "tie cord", "qty": round(BODY_H * 1.8), "unit": "mm_length",
         "note": f"{cord_dia:.1f} mm cord through both tie tabs."},
        {"item": "cord-end tips", "qty": 2, "unit": "count",
         "note": "Yantra4D cord-end (see notion.hardware_ref) finishes both cord ends."},
        {"item": "heavy-duty thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "bar-tack every slot mouth; the mouth is where a blade cuts out."},
    ]
    pattern.metadata = {
        "fc300_rank": 240, "family": "technical_outdoor", "fabric_hint": "manta-cruda",
        "silhouette_note": "Padded blade channels quilted over batting, each blade in its own "
            "slot so edges never touch, under a long tip flap that folds past every point; the "
            "whole roll winds up and ties on a tipped cord.",
        "solved": {"slot_pitch_mm": round(PITCH, 1), "row_run_mm": round(ROW_RUN, 1),
                   "strip_run_mm": round(STRIP_RUN, 1),
                   "body_mm": [round(BODY_W, 1), round(BODY_H, 1)], "slots": slots},
        "hardware": "cord-end tie tips via Yantra4D (notion.hardware_ref -> cord-end)",
    }
    return pattern


result = build()
