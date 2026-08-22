"""
Tool Roll — Fashion Cabinet Accessory Cartridge (FC-300 #239, technical & outdoor).

The pocket-row tool roll: a flat rectangle of tough cloth with a row of divided pockets
sewn across it, rolled up around its own contents and tied shut with a cord whose ends
are finished with pressed-on strap-end tips so they never fray and always thread. The
pocket row is one continuous strip stitched down at each divider, so every pocket takes
the exact width of the tool it carries and the divider spacing IS the tool list.

The strap-end tip solid is Yantra4D territory (`cord-end`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the roll — the body, the flap that covers
the tool tips, the pocket strip, the divider pitch, the tie run.

The bridge is dimensional: `tie_cord_dia` drives the cord-end's sewn mouth flange AND
this garment's `tie_closure` interface, so the tip really is sized to the cord that
passes through the roll's own tie channel.

Pieces:
  - body    : the roll back panel with the flap, divider and roll lines marked.
  - pockets : the continuous pocket strip that becomes the divided row.
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
target_piece = str(PARAM(lambda: target_piece, "set"))       # body|pockets|tie|set

pockets       = int(PARAM(lambda: pockets, 8))               # tools in the row
pocket_width  = float(PARAM(lambda: pocket_width, 46.0))     # finished width per pocket
pocket_height = float(PARAM(lambda: pocket_height, 175.0))   # pocket depth up the body
tool_length   = float(PARAM(lambda: tool_length, 250.0))     # longest tool, tip to tail
flap_depth    = float(PARAM(lambda: flap_depth, 90.0))       # flap over the tool tips
bellows       = float(PARAM(lambda: bellows, 6.0))           # ease per pocket for tool girth
tie_cord_dia  = float(PARAM(lambda: tie_cord_dia, 5.0))      # tie cord diameter
tie_width     = float(PARAM(lambda: tie_width, 26.0))        # tie tab width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
pockets       = max(2, min(pockets, 24))
pocket_width  = max(18.0, min(pocket_width, 130.0))
pocket_height = max(60.0, min(pocket_height, 340.0))
tool_length   = max(90.0, min(tool_length, 520.0))
flap_depth    = max(0.0, min(flap_depth, 180.0))
bellows       = max(0.0, min(bellows, 30.0))
tie_cord_dia  = max(2.0, min(tie_cord_dia, 10.0))
tie_width     = max(14.0, min(tie_width, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

PITCH = pocket_width + bellows                # divider pitch across the row
ROW_RUN = PITCH * pockets                     # the pocket row's finished run
BODY_W = ROW_RUN + 2.0 * 20.0                 # body width = row plus side margins
BODY_H = tool_length + flap_depth + 30.0      # body height = tool + flap + base turn
# The pocket strip is longer than the row by the bellows the dividers take up.
STRIP_RUN = ROW_RUN + bellows * pockets


def build_body():
    """The roll's back panel: the pocket row sits low, the flap folds down over the tips."""
    internals = [
        fc.Internal("flap-fold",
                    [fc.P(0.0, BODY_H - flap_depth), fc.P(BODY_W, BODY_H - flap_depth)],
                    kind="fold"),
        fc.Internal("pocket-top",
                    [fc.P(20.0, pocket_height + 20.0), fc.P(BODY_W - 20.0, pocket_height + 20.0)],
                    kind="marking"),
    ]
    # One divider stitch line per pocket boundary — the divider pitch IS the tool list.
    for i in range(1, pockets):
        x = 20.0 + PITCH * i
        internals.append(fc.Internal(
            "divider", [fc.P(x, 20.0), fc.P(x, pocket_height + 20.0)], kind="marking"))
    # The roll lines: where the roll folds as it winds up around the tools.
    for i in (1, 2, 3):
        x = BODY_W * i / 4.0
        internals.append(fc.Internal(
            "roll-line", [fc.P(x, 0.0), fc.P(x, BODY_H)], kind="marking"))
    return fc.Piece(
        "body",
        [
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BODY_H))]),
            fc.Edge("flap_edge", [fc.Line(fc.P(0.0, BODY_H), fc.P(BODY_W, BODY_H))]),
            fc.Edge("right", [fc.Line(fc.P(BODY_W, BODY_H), fc.P(BODY_W, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(BODY_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", (pocket_height + 20.0) / BODY_H, "pocket top"),
                 fc.Notch("left", (BODY_H - flap_depth) / BODY_H, "flap fold"),
                 fc.Notch("right", 0.5, "tie tab")],
        grainline=fc.Grainline(fc.P(BODY_W * 0.5, 20.0), fc.P(BODY_W * 0.5, BODY_H - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Roll body + flap",
    )


def build_pockets():
    """The continuous pocket strip: longer than the row by the bellows each divider eats."""
    internals = []
    for i in range(1, pockets):
        x = PITCH * i + bellows * (i - 0.5)
        internals.append(fc.Internal(
            "divider-match", [fc.P(x, 0.0), fc.P(x, pocket_height)], kind="marking"))
    return fc.Piece(
        "pockets",
        [
            fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, pocket_height))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, pocket_height), fc.P(STRIP_RUN, pocket_height))]),
            fc.Edge("end_b", [fc.Line(fc.P(STRIP_RUN, pocket_height), fc.P(STRIP_RUN, 0.0))]),
            fc.Edge("attach", [fc.Line(fc.P(STRIP_RUN, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 18.0},
        notches=[fc.Notch("attach", 0.0, "row start"), fc.Notch("attach", 1.0, "row end")],
        grainline=fc.Grainline(fc.P(STRIP_RUN * 0.5, 10.0),
                               fc.P(STRIP_RUN * 0.5, pocket_height - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pocket strip",
    )


def build_tie():
    """The tie tab: a folded tab that carries the cord whose ends take the strap-end tips."""
    length = BODY_H * 0.55
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
                               [fc.P(tie_width / 2.0 - tie_cord_dia, 8.0),
                                fc.P(tie_width / 2.0 - tie_cord_dia, length - 8.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Tie tab",
    )


def build():
    pattern = fc.PatternSet("tool-roll")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "pockets":
        pattern.add(build_pockets())
    if everything or target_piece == "tie":
        pattern.add(build_tie())
    if everything:
        # The pocket strip's side ends are caught in the body's side seams.
        pattern.declare_seam(("pockets", "end_a"), ("pockets", "end_b"), tol=1.0)
        # The tie tabs are caught in the body's right-hand seam.
        pattern.declare_seam(("tie", "attach"), ("tie", "cord_end"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "waxed canvas / heavy duck",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 75% marker; the pocket strip wants the same cloth."},
        {"item": "tie cord", "qty": round(BODY_H * 1.6), "unit": "mm_length",
         "note": f"{tie_cord_dia:.1f} mm cord through both tie tabs."},
        {"item": "strap-end tips", "qty": 2, "unit": "count",
         "note": "Yantra4D cord-end (see notion.hardware_ref) finishes both cord ends."},
        {"item": "heavy-duty thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "bar-tack the top of every divider — that is where a tool roll fails."},
    ]
    pattern.metadata = {
        "fc300_rank": 239, "family": "technical_outdoor", "fabric_hint": "manta-cruda",
        "silhouette_note": "A flat panel with one continuous pocket strip stitched down at every "
            "divider, a flap over the tool tips, and a cord tie: the divider pitch is the tool "
            "list, and the roll winds around its own contents.",
        "solved": {"divider_pitch_mm": round(PITCH, 1), "row_run_mm": round(ROW_RUN, 1),
                   "strip_run_mm": round(STRIP_RUN, 1), "body_mm": [round(BODY_W, 1),
                                                                    round(BODY_H, 1)],
                   "pockets": pockets},
        "hardware": "strap-end tips via Yantra4D (notion.hardware_ref -> cord-end)",
    }
    return pattern


result = build()
