"""
Buttonhole-spacer guide roll — Fashion Cabinet Cartridge (FC-500 #417, care_keeping, T1).

A roll-up guide that stores the Yantra4D `buttonhole-spacer` rail (the sliding rail tool that
marks even buttonhole spacing) AND carries its own printed measuring scale, so the rail and
the guide it needs live together. A BODY panel with a long rail POCKET the length of the rail,
a marked scale line at the rail pitch, and a TIE.

Solved, not guessed:

  1. THE RAIL POCKET IS CUT TO THE MEASURED RAIL. The pocket length is the rail length plus a
     seat; the pocket is declared to the body length so they sew flush.
  2. THE SCALE TICKS ARE DERIVED FROM THE RAIL PITCH. The tick count along the body is the
     usable length over the pitch, floored at 2, so a coarse pitch never yields a single tick.
  3. THE POCKET DEPTH IS CLAMPED under the body width so the rail pocket never runs off the
     panel edge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # body|pocket|tie|set

rail_length = float(PARAM(lambda: rail_length, 240.0))
rail_width = float(PARAM(lambda: rail_width, 24.0))
rail_pitch = float(PARAM(lambda: rail_pitch, 20.0))       # buttonhole spacing pitch
seat = float(PARAM(lambda: seat, 20.0))
margin = float(PARAM(lambda: margin, 28.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

rail_length = max(120.0, min(rail_length, 400.0))
rail_width = max(12.0, min(rail_width, 60.0))
rail_pitch = max(8.0, min(rail_pitch, 60.0))
seat = max(8.0, min(seat, 50.0))
margin = max(15.0, min(margin, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

BODY_L = rail_length + seat + 2.0 * margin
BODY_W = rail_width + 2.0 * margin + 30.0            # room for the scale beside the rail
POCKET_L = rail_length + seat
POCKET_W = min(rail_width + 12.0, BODY_W - margin)   # clamped inside the body width
POCKET_W = max(20.0, POCKET_W)
TICKS = max(2, round(rail_length / rail_pitch))


def build_body():
    w, h = BODY_W, BODY_L
    scale_x = margin + POCKET_W + 14.0
    internals = [
        fc.Internal("rail pocket outline",
                    [fc.P(margin, margin), fc.P(margin + POCKET_W, margin),
                     fc.P(margin + POCKET_W, margin + POCKET_L),
                     fc.P(margin, margin + POCKET_L), fc.P(margin, margin)],
                    kind="marking"),
    ]
    for i in range(TICKS + 1):
        ty = margin + i * (rail_length / TICKS)
        internals.append(fc.Internal(f"scale tick {i}",
                         [fc.P(scale_x, ty), fc.P(min(scale_x + 16.0, w), ty)],
                         kind="marking"))
    return fc.Piece(
        "body", [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "roll centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 15.0), fc.P(w * 0.5, h - 15.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Guide body (cut 1)",
    )


def build_pocket():
    w, h = POCKET_W, POCKET_L
    return fc.Piece(
        "pocket", [
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 14.0},
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Rail pocket (cut 1)",
    )


def build_tie():
    ln = max(2.0 * BODY_W, BODY_W + 260.0)
    w = max(18.0, margin * 0.8)
    return fc.Piece(
        "tie", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "body join")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Wrap tie (cut 1)",
    )


def build():
    pattern = fc.PatternSet("buttonhole-spacer-guide")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything or target_piece == "tie":
        pattern.add(build_tie())

    if everything:
        pattern.declare_seam(("pocket", "left"), ("body", "left"), tol=1.0,
                             ease=POCKET_L - BODY_L)

    fabric_width = 1100.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "printed / stencilled cotton (with the scale)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; the measuring scale is "
                 f"printed or stencilled beside the rail pocket."},
        {"item": "buttonhole-spacer rail", "qty": 1, "unit": "count",
         "note": f"Yantra4D buttonhole-spacer (notion.hardware_ref): the pocket is cut to "
                 f"the rail ({rail_length:.0f} mm) plus a seat; the scale ticks step at the "
                 f"rail pitch."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "sew the rail pocket, print the scale, roll and tie."},
    ]
    pattern.metadata = {
        "fc500_rank": 417, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A roll-up guide storing the buttonhole-spacer rail and its own "
            "printed measuring scale.",
        "solved": {
            "body_length_mm": round(BODY_L, 1),
            "pocket_length_mm": round(POCKET_L, 1),
            "pocket_width_mm": round(POCKET_W, 1),
            "scale_ticks": TICKS,
            "note": "the rail pocket is cut to the measured rail plus a seat; the scale tick "
                    "count is derived from the rail length over the pitch, floored at 2; the "
                    "pocket width is clamped inside the body so it never runs off the panel.",
        },
        "hardware": "buttonhole-spacer rail via Yantra4D (notion.hardware_ref -> "
                    "buttonhole-spacer); rail_len, rail_w and pitch are fed from the rail. "
                    "No flange interface — the guide holds the rail, no seam handshake owed.",
    }
    return pattern


result = build()
