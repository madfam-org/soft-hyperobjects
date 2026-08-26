"""
Draped turban hat — FC-400 rank #357, Lane 6 (millinery). Fashion Cabinet Cartridge.

A soft draped turban in stretch jersey: a fitted CAP that covers the head plus a long
WRAP band gathered into a knot at the centre front. The turban pulls on, so the cap is
drafted SMALLER than the head and stretches on — SIGNED negative ease. The wrap is a long
strip that crosses at the front and its ends tuck; the knot is a short gathered panel.

Pieces:
  - cap   : the fitted head cap, cut 2 mirrored (two half-domes seamed at the crown).
  - wrap  : the long drape band, cut 1 (length = head circ × wrap_turns, height = wrap_h).
  - knot  : the gathered front knot panel, cut 1.

Drafting notes:
  * The cap half is a quarter-dome profile from the nape ring up to the crown; its crown
    seam is straight and its face edge is the head ring half.
  * NEGATIVE EASE: the cap draft girth is head_girth + neg ease, floored so it stays
    wearable at maximum stretch.
  * The wrap length is DERIVED (head circ × turns) and floored; the knot width is floored.

Hardware: none — a draped turban pulls on and has no closure.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # cap|wrap|knot|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
head_height = float(PARAM(lambda: head_height, 200.0))   # nape ring to crown
knit_ease = float(PARAM(lambda: knit_ease, -40.0))       # SIGNED negative (pulls on)
wrap_turns = float(PARAM(lambda: wrap_turns, 2.2))       # how many times the wrap circles
wrap_h = float(PARAM(lambda: wrap_h, 140.0))             # wrap band height
knot_width = float(PARAM(lambda: knot_width, 160.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

head_girth = max(480.0, min(head_girth, 640.0))
head_height = max(130.0, min(head_height, 300.0))
knit_ease = max(-120.0, min(knit_ease, 20.0))
wrap_turns = max(1.0, min(wrap_turns, 4.0))
wrap_h = max(60.0, min(wrap_h, 280.0))
knot_width = max(70.0, min(knot_width, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

DRAFT_GIRTH = max(360.0, head_girth + knit_ease)
HALF_HEAD = DRAFT_GIRTH / 2.0
H = max(100.0, head_height)
WRAP_LEN = max(400.0, DRAFT_GIRTH * wrap_turns)


def _cap():
    """One cap half: a dome profile. Frame: x=0 crown seam, y=0 face (nape) ring.
    Face edge (bottom) is a quarter of the head ring; crown seam runs up the centre."""
    face_w = HALF_HEAD / 2.0                     # quarter head ring (flat)
    return fc.Piece(
        "cap",
        [
            fc.Edge("face", [fc.Line(fc.P(0.0, 0.0), fc.P(face_w, 0.0))]),   # head opening
            fc.Edge("side", [fc.curve_through(fc.P(face_w, 0.0), fc.P(face_w * 0.5, H),
                                              bulge=0.10, side=1.0)]),
            fc.Edge("crown_seam", [fc.Line(fc.P(face_w * 0.5, H), fc.P(0.0, H))]),
            fc.Edge("centre", [fc.Line(fc.P(0.0, H), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"face": seam_allowance},
        notches=[fc.Notch("face", 0.5, "side head")],
        grainline=fc.Grainline(fc.P(face_w * 0.3, 10.0), fc.P(face_w * 0.3, H - 10.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cap half",
    )


def _wrap():
    length = WRAP_LEN
    h = wrap_h
    return fc.Piece(
        "wrap",
        [
            fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
            fc.Edge("upper", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.5, "centre wrap")],
        grainline=fc.Grainline(fc.P(length * 0.5, h * 0.2), fc.P(length * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Drape wrap band",
    )


def _knot():
    w = knot_width
    h = wrap_h * 1.2
    return fc.Piece(
        "knot",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        internals=[fc.Internal("gather line", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, h)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Front knot panel",
    )


def build():
    pattern = fc.PatternSet("turban-wrap-hat")
    everything = target_piece == "set"
    cap = _cap()
    if everything or target_piece == "cap":
        pattern.add(cap)
    if everything or target_piece == "wrap":
        pattern.add(_wrap())
    if everything or target_piece == "knot":
        pattern.add(_knot())

    if "cap" in {p.name for p in pattern.pieces}:
        # the two cap halves join at the crown seam.
        pattern.declare_seam(("cap", "crown_seam"), ("cap", "crown_seam"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "viscose jersey (stretch)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 70% marker. A drapey stretch jersey is "
                 "essential — the cap is drafted under the head and stretches on."},
        {"item": "soft lining (cap, optional)", "qty": 1, "unit": "as chosen",
         "note": "a light lining stops the cap seams showing through."},
        {"item": "thread (stretch)", "qty": 1, "unit": "spool",
         "note": "overlock or narrow zigzag; the wrap and knot are gathered by hand."},
    ]
    pattern.metadata = {
        "fc400_rank": 357, "family": "millinery", "lane": 6,
        "fabric_hint": "jersey-viscose",
        "head_girth_mm": round(head_girth, 1), "draft_girth_mm": round(DRAFT_GIRTH, 1),
        "knit_ease_mm": round(knit_ease, 1),
        "wrap_len_mm": round(WRAP_LEN, 1), "wrap_turns": round(wrap_turns, 2),
        "wrap_h_mm": round(wrap_h, 1), "knot_width_mm": round(knot_width, 1),
        "solved": {
            "half_head_mm": round(HALF_HEAD, 1),
            "note": "the cap draft girth is floored for the negative-ease pull-on; the wrap "
                    "length is DERIVED (head circ × turns) and floored so it can never go "
                    "negative",
        },
        "hardware": "none — a draped turban pulls on and has no closure",
    }
    return pattern


result = build()
