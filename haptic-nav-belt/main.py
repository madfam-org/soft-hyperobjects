"""
Haptic Navigation Belt — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A waist belt that gives direction by vibration: N tactor motors spaced evenly around
the waist, so "north" or "turn left" is a buzz at a place on your body rather than a
sound or a screen. Drafted as a soft belt — an outer SHELL, an inner TACTOR LAYER with
the motor pockets, and a TAIL that carries the buckle — not as webbing with things
glued to it.

The cable run between tactors is the pattern's real problem. Every motor is a place a
wire terminates, and a terminated wire at a flexing waist is where the belt fails. So
each tactor pocket is paired with a Yantra4D `seam-strain-relief` plate sewn into the
seam beside it; the plate's sewn footprint is `relief_len` x `relief_width`, the same
rectangle the tactor layer's marked plate footprints are drawn to.

Drafting note — the seam that must SOLVE: the tactor spacing is not `belt_len / n`.
The tactors must be evenly spaced around the WEARER, which means around the shell's
measured inner run — excluding the overlap the buckle tail consumes. The kernel drafts
the shell, measures its `body_run` edge, divides THAT, and then cuts the tactor layer
to the same measured run so the two layers' pockets and seams register.

Pieces:
  - shell   : the outer belt, waist run plus the buckle overlap.
  - tactor  : the inner layer carrying the motor pockets and strain-relief footprints.
  - tail    : the buckle tail with its adjustment ladder.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # shell|tactor|tail|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))     # waist circumference
belt_width = float(PARAM(lambda: belt_width, 70.0))        # belt height
tactor_count = int(PARAM(lambda: tactor_count, 8))         # vibration motors round the waist
tactor_dia = float(PARAM(lambda: tactor_dia, 12.0))        # motor body diameter
relief_len = float(PARAM(lambda: relief_len, 26.0))        # strain-relief plate length
relief_width = float(PARAM(lambda: relief_width, 14.0))    # strain-relief plate width
overlap = float(PARAM(lambda: overlap, 180.0))             # buckle overlap / adjustment
tail_rows = int(PARAM(lambda: tail_rows, 5))               # adjustment ladder rows
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(560.0, min(waist_girth, 1500.0))
belt_width = max(35.0, min(belt_width, 140.0))
tactor_count = max(4, min(tactor_count, 16))
tactor_dia = max(6.0, min(tactor_dia, 30.0))
relief_len = max(12.0, min(relief_len, 60.0))
relief_width = max(6.0, min(relief_width, 40.0))
overlap = max(80.0, min(overlap, 400.0))
tail_rows = max(2, min(tail_rows, 10))
seam_allowance = max(0.0, min(seam_allowance, 18.0))

# The belt must be tall enough to seat a tactor pocket AND the relief plate beside it.
belt_width = max(belt_width, tactor_dia + relief_width + 22.0)
# The plate cannot be longer than the gap between two tactors would allow.
relief_len = min(relief_len, waist_girth / tactor_count * 0.5)

W = belt_width
BODY_RUN = waist_girth          # the run that actually goes round the wearer
SHELL_LEN = BODY_RUN + overlap  # plus what the buckle tail overlaps


def build_shell():
    """The outer belt: the body run plus the buckle overlap.

    `body_run` is a NAMED edge covering only the part that goes round the wearer —
    it is the edge the tactor spacing is measured from, and the edge the tactor layer
    sews to. `overlap_run` is the extra the tail rides over.
    """
    edges = [
        fc.Edge("cf_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, W))]),
        # top edge split so the body portion is separately measurable
        fc.Edge("body_top", [fc.Line(fc.P(0.0, W), fc.P(BODY_RUN, W))]),
        fc.Edge("overlap_top", [fc.Line(fc.P(BODY_RUN, W), fc.P(SHELL_LEN, W))]),
        fc.Edge("tail_end", [fc.Line(fc.P(SHELL_LEN, W), fc.P(SHELL_LEN, 0.0))]),
        fc.Edge("overlap_run", [fc.Line(fc.P(SHELL_LEN, 0.0), fc.P(BODY_RUN, 0.0))]),
        fc.Edge("body_run", [fc.Line(fc.P(BODY_RUN, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # Where the tail's buckle is bar-tacked on.
        fc.Internal("buckle-tack", [
            fc.P(SHELL_LEN - overlap * 0.15, W * 0.2),
            fc.P(SHELL_LEN - overlap * 0.15, W * 0.8)], kind="drill"),
        # The main harness run, kept along the upper third away from the fold line.
        fc.Internal("harness-run", [
            fc.P(W * 0.3, W * 0.72), fc.P(BODY_RUN - W * 0.3, W * 0.72)],
            kind="trace"),
    ]
    return fc.Piece(
        "shell", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("body_run", 0.5, "centre back"),
                 fc.Notch("body_top", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(SHELL_LEN * 0.15, W / 2.0),
                               fc.P(SHELL_LEN * 0.85, W / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Shell (outer belt)",
    )


# ── The measured body run ────────────────────────────────────────────────────
# Tactor spacing is NOT belt_len / n: the motors must be evenly spaced around the
# WEARER, so the divisor is the shell's measured body_run edge — the part that
# actually goes round — with the buckle overlap excluded.
_SHELL = build_shell()
MEASURED_BODY_RUN = _SHELL.edge("body_run").length()
TACTOR_PITCH = MEASURED_BODY_RUN / tactor_count


def build_tactor():
    """The inner layer: one motor pocket per tactor, evenly spaced around the MEASURED
    body run, each paired with a strain-relief plate footprint in the seam beside it."""
    ln = MEASURED_BODY_RUN
    internals = []
    r = tactor_dia / 2.0
    # Pocket centre line sits low; the relief plates sit above it in the top seam.
    pocket_y = W * 0.38
    plate_y = W - relief_width / 2.0 - seam_allowance
    for i in range(tactor_count):
        # Half-pitch offset so tactor 0 lands at centre back, not on the CF seam.
        cx = TACTOR_PITCH * (i + 0.5)
        internals.append(fc.Internal(f"tactor-pocket-{i}", [
            fc.P(cx - r - 4.0, pocket_y - r - 4.0), fc.P(cx + r + 4.0, pocket_y - r - 4.0),
            fc.P(cx + r + 4.0, pocket_y + r + 4.0), fc.P(cx - r - 4.0, pocket_y + r + 4.0),
            fc.P(cx - r - 4.0, pocket_y - r - 4.0)], kind="marking"))
        # The strain-relief plate: sewn into the top seam beside its tactor, so the
        # wire terminating at that motor is clamped before it reaches the flex zone.
        internals.append(fc.Internal(f"relief-plate-{i}", [
            fc.P(cx - relief_len / 2.0, plate_y - relief_width / 2.0),
            fc.P(cx + relief_len / 2.0, plate_y - relief_width / 2.0),
            fc.P(cx + relief_len / 2.0, plate_y + relief_width / 2.0),
            fc.P(cx - relief_len / 2.0, plate_y + relief_width / 2.0),
            fc.P(cx - relief_len / 2.0, plate_y - relief_width / 2.0)], kind="marking"))
        # The spur from the harness run down to this motor.
        internals.append(fc.Internal(f"tactor-spur-{i}", [
            fc.P(cx, plate_y), fc.P(cx, pocket_y)], kind="trace"))

    return fc.Piece(
        "tactor",
        [
            fc.Edge("cf_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, W))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, W), fc.P(ln, W))]),
            fc.Edge("cb_end", [fc.Line(fc.P(ln, W), fc.P(ln, 0.0))]),
            fc.Edge("body_run", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("body_run", 0.5, "centre back"),
                 fc.Notch("top", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.15, W / 2.0), fc.P(ln * 0.85, W / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Tactor layer (motor pockets)",
    )


def build_tail():
    """The buckle tail with its adjustment ladder. Cut to the overlap length so the
    belt's adjustment range is exactly the overlap it was drafted for."""
    ln = overlap
    h = W
    internals = []
    for r in range(tail_rows):
        x = ln * (0.18 + 0.66 * r / max(tail_rows - 1, 1))
        internals.append(fc.Internal(f"ladder-{r}",
                                     [fc.P(x, h * 0.28), fc.P(x, h * 0.72)],
                                     kind="drill"))
    # The controller pocket lives on the tail, at the front where you can reach it.
    internals.append(fc.Internal("controller-pocket", [
        fc.P(ln * 0.06, h * 0.16), fc.P(ln * 0.06 + relief_len * 2.2, h * 0.16),
        fc.P(ln * 0.06 + relief_len * 2.2, h * 0.84), fc.P(ln * 0.06, h * 0.84),
        fc.P(ln * 0.06, h * 0.16)], kind="marking"))
    return fc.Piece(
        "tail",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(ln, h))]),
            fc.Edge("free", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "buckle centre")],
        grainline=fc.Grainline(fc.P(ln * 0.15, h / 2.0), fc.P(ln * 0.85, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Buckle tail",
    )


def build():
    pattern = fc.PatternSet("haptic-nav-belt")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "tactor":
        pattern.add(build_tactor())
    if all_pieces or target_piece == "tail":
        pattern.add(build_tail())

    if all_pieces:
        # THE seam that had to solve: the tactor layer is cut to the shell's MEASURED
        # body run — the part that goes round the wearer, buckle overlap excluded —
        # so the motor pockets register against the shell instead of drifting.
        pattern.declare_seam(("tactor", "body_run"), ("shell", "body_run"), tol=1.0)
        pattern.declare_seam(("tactor", "top"), ("shell", "body_top"), tol=1.0)
        # The tail's attach edge sews to the shell's tail end.
        pattern.declare_seam(("tail", "attach"), ("shell", "tail_end"), tol=1.0)
        # The tail's own length is the belt's adjustment range: it must equal the
        # overlap the shell was drafted with.
        pattern.declare_seam(("tail", "bottom"), ("shell", "overlap_run"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "webbing-weight cloth (conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 80% marker; long straight pieces nest well."},
        {"item": "seam strain relief", "qty": tactor_count, "unit": "count",
         "note": f"Yantra4D seam-strain-relief (notion.hardware_ref); "
                 f"{relief_len:.0f} x {relief_width:.0f} mm sewn plate, one per tactor, "
                 f"sewn into the top seam at the marked relief-plate footprint."},
        {"item": "vibration tactor motor", "qty": tactor_count, "unit": "count",
         "note": f"{tactor_dia:.0f} mm body; drops into the marked pocket, "
                 f"spaced {TACTOR_PITCH:.0f} mm apart around the measured body run."},
        {"item": "conductive thread or ribbon cable", "qty": 1, "unit": "harness",
         "note": "harness-run along the shell, spurs down to each tactor."},
        {"item": "controller + battery", "qty": 1, "unit": "set",
         "note": "in the tail's marked controller-pocket, reachable at the front."},
        {"item": "belt buckle", "qty": 1, "unit": "count",
         "note": "bar-tacked at the marked buckle-tack; maker's choice of hardware."},
    ]
    pattern.metadata = {
        "fc300_rank": 264,
        "family": "etextile",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"waist": round(waist_girth, 1),
                        "belt_width": round(belt_width, 1),
                        "adjustment_range": round(overlap, 1)},
        "solved": {
            "shell_len_mm": round(SHELL_LEN, 2),
            "measured_body_run_mm": round(MEASURED_BODY_RUN, 2),
            "tactor_count": tactor_count,
            "tactor_pitch_mm": round(TACTOR_PITCH, 2),
            "note": "tactor pitch is the MEASURED body_run edge divided by the count, "
                    "NOT the whole belt length divided — the buckle overlap does not go "
                    "round the wearer, so including it would skew every motor's angle.",
        },
        "etextile_note": "Motor pockets, relief-plate footprints, harness run and spurs "
                         "are MARKED for the maker. No motor, driver, or circuit is "
                         "drafted here.",
        "hardware": "strain reliefs via Yantra4D (notion.hardware_ref -> "
                    "seam-strain-relief); the plate's sewn footprint is this belt's "
                    "relief_len x relief_width, the same rectangle marked on the "
                    "tactor layer",
    }
    return pattern


result = build()
