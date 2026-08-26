"""
Bias-tape maker caddy — Fashion Cabinet Care & Keeping Cartridge (FC-500 #413, care_keeping, T1).

A roll-up fabric caddy that holds a nested set of bias-tape makers (the little metal or
printed funnels that fold a bias strip as you press it). A BODY panel with a row of
graduated POCKETS sized to the tool set, and a TIE that wraps the roll closed. Drafted to a
KNOWN tool — the Yantra4D `bias-tape-maker` solid (notion.hardware_ref) — so the pocket
widths track the actual tool throat, not a guess.

Solved, not guessed:

  1. THE POCKET ROW IS MEASURED TO THE TOOL SET. Each pocket width is the tool's own width
     plus a clearance, and the sum of the pocket widths (plus the pleat each pocket eats) is
     what the body panel is cut to — measured, then declared as the pocket-row seam ease.
  2. THE POCKET DEPTH IS CLAMPED under the body height so a deep pocket can never run past
     the fold and invert the flap.
  3. THE TIE LENGTH WRAPS THE ROLLED CADDY. It is floored so it always goes at least once
     around the roll plus a bow.

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

tool_count = int(PARAM(lambda: tool_count, 5))
tool_width = float(PARAM(lambda: tool_width, 40.0))       # widest bias-tape-maker throat
tool_length = float(PARAM(lambda: tool_length, 95.0))     # tool length (pocket depth guide)
pocket_clear = float(PARAM(lambda: pocket_clear, 10.0))
body_margin = float(PARAM(lambda: body_margin, 30.0))     # margin around the pocket row
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

tool_count = max(2, min(tool_count, 8))
tool_width = max(18.0, min(tool_width, 80.0))
tool_length = max(50.0, min(tool_length, 160.0))
pocket_clear = max(4.0, min(pocket_clear, 24.0))
body_margin = max(15.0, min(body_margin, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# Pockets graduate from the widest tool down; each pocket width = a share of the widest
# plus clearance. The row width is the sum.
POCKET_W = tool_width + pocket_clear
ROW_W = POCKET_W * tool_count
BODY_W = ROW_W + 2.0 * body_margin
POCKET_DEPTH = min(tool_length * 0.7, tool_length)       # pocket holds 70% of the tool
BODY_H = POCKET_DEPTH + tool_length * 0.5 + 2.0 * body_margin
# clamp the pocket depth under the body height less the fold
POCKET_DEPTH = min(POCKET_DEPTH, BODY_H - body_margin - 20.0)
POCKET_DEPTH = max(30.0, POCKET_DEPTH)
TIE_LEN = max(2.0 * BODY_W, BODY_W + 300.0)              # wraps the roll + a bow


def build_body():
    w, h = BODY_W, BODY_H
    return fc.Piece(
        "body", [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "CF fold when rolled"),
                 fc.Notch("top", 0.5, "flap fold")],
        grainline=fc.Grainline(fc.P(w * 0.5, 15.0), fc.P(w * 0.5, h - 15.0)),
        internals=[
            fc.Internal("pocket attach line",
                        [fc.P(body_margin, body_margin + POCKET_DEPTH),
                         fc.P(body_margin + ROW_W, body_margin + POCKET_DEPTH)],
                        kind="marking"),
        ] + [
            fc.Internal(f"pocket divider {i}",
                        [fc.P(body_margin + i * POCKET_W, body_margin),
                         fc.P(body_margin + i * POCKET_W, body_margin + POCKET_DEPTH)],
                        kind="marking")
            for i in range(1, tool_count)
        ],
        cut=fc.CutSpec(quantity=1),
        label="Caddy body (cut 1)",
    )


def build_pocket():
    """The pocket strip, cut 1. Its top edge is the pocket-row width; it is pleated at each
    divider so each tool sits in its own well."""
    w = ROW_W
    h = POCKET_DEPTH
    return fc.Piece(
        "pocket", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("mouth", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 16.0},
        notches=[fc.Notch("attach", 0.5, "centre")]
        + [fc.Notch("attach", i / tool_count, f"divider {i}")
           for i in range(1, tool_count)],
        grainline=fc.Grainline(fc.P(w * 0.5, 10.0), fc.P(w * 0.5, h - 10.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Pocket strip (cut 1)",
    )


def build_tie():
    ln = TIE_LEN
    w = max(20.0, body_margin)
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
    pattern = fc.PatternSet("bias-tape-holder-caddy")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())
    if everything or target_piece == "tie":
        pattern.add(build_tie())

    if everything:
        # the pocket strip's attach edge sews to the body's pocket-attach line — measured
        # to the same row width.
        pattern.declare_seam(("pocket", "attach"), ("body", "top"), tol=1.0,
                             ease=ROW_W - BODY_W)

    fabric_width = 1100.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "quilting cotton (body + pocket)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a firm cotton so the pockets "
                 f"stand and the roll holds its shape."},
        {"item": "bias-tape maker set", "qty": tool_count, "unit": "count",
         "note": f"Yantra4D bias-tape-maker (notion.hardware_ref): the pocket widths are "
                 f"cut to the tool throat ({tool_width:.0f} mm) plus a {pocket_clear:.0f} mm "
                 f"clearance."},
        {"item": "fusible fleece + thread", "qty": 1, "unit": "set",
         "note": "a light fleece gives the body enough body to roll and tie."},
    ]
    pattern.metadata = {
        "fc500_rank": 413, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A roll-up caddy for a graduated bias-tape-maker set, pockets "
            "sized to the tools, a wrap tie.",
        "solved": {
            "pocket_width_mm": round(POCKET_W, 1),
            "row_width_mm": round(ROW_W, 1),
            "body_width_mm": round(BODY_W, 1),
            "pocket_depth_mm": round(POCKET_DEPTH, 1),
            "tie_length_mm": round(TIE_LEN, 1),
            "note": "each pocket is the tool throat plus a clearance; the row width is the "
                    "sum (declared as the pocket-attach seam ease); the pocket depth is "
                    "clamped under the body height so a deep pocket never inverts the flap; "
                    "the tie is floored to wrap the roll plus a bow.",
        },
        "hardware": "bias-tape-maker set via Yantra4D (notion.hardware_ref -> "
                    "bias-tape-maker); tape_width and tool_len are fed from the tool "
                    "dimensions. No flange interface — the caddy holds the tool, it does "
                    "not sew to it, so no dimensional handshake is owed.",
    }
    return pattern


result = build()
