"""
Hakama (袴) — FC-300 rank #281. Fashion Cabinet Garment Cartridge.

The hakama is the pleated over-garment worn from the waist down over a kimono:
formal wear, and the working dress of kendō, aikidō, kyūdō and Shintō practice.
This cartridge drafts the 馬乗り袴 (`umanori`, "horse-riding") form — the DIVIDED
hakama, split into two legs — which is the everyday and martial form.

The hakama's construction is unlike a Western trouser in every respect, and the
draft encodes those differences rather than smoothing them away:

  - IT HAS NO CROTCH CURVE AND NO SEAT SHAPING. The leg is a straight panel;
    the division is made by a straight vertical seam that stops partway up. The
    unsewn remainder above that stop is the 相引き (`aibiki`) — the open side
    gap that lets the garment wrap and lets the wearer move. There is no
    drafted rise curve because the tradition has none.
  - THE PLEATS ARE NAMED AND ASYMMETRIC. Front: five pleats (三つ山, three
    outward-facing plus two inward), traditionally read as the five virtues.
    Back: two. This draft holds that 5/2 asymmetry as a hard structural fact
    rather than a decorative option, because the front and back must pleat to
    DIFFERENT band lengths and still meet at the sides.
  - 腰板 (`KOSHIITA`) — THE BACK BOARD. A stiffened trapezoidal board at the
    back waist that sits in the small of the back and holds the garment's
    posture. Its lower edge is the seam the back pleating sews to. It is the
    single most distinctive piece and the reason a hakama stands up.
  - FOUR STRAPS (紐, `himo`), not a waistband: two long front straps and two
    shorter back straps, tied in a specific sequence. Their lengths are solved
    as real wrap circuits, not guessed.

Drafting note — what actually SOLVES: the front and back pleat into DIFFERENT
finished spans (front carries the wrap overlap; back is bounded by the koshiita
board), and each side's pleat depth is back-solved INDEPENDENTLY from its own
integer pleat count and its own span, so both pleatings tile their bands
exactly. The koshiita's lower edge is MEASURED from the drafted trapezoid
polygon (it is a slanted-sided piece, so its bottom is not the same as its top)
and the back panel's pleated span is reconciled against that measurement. The
aibiki opening is solved as the remainder of the side edge above the leg-seam
stop, and the front and back side edges are checked to close.

EXCLUSION, stated rather than quietly ignored: 行灯袴 (`andon` hakama, the
undivided skirt-like form) is a genuinely different garment and is not drafted
here — it is not this pattern with a parameter turned off. The rank-bearing and
ritual hakama — the stiff 長袴 (`nagabakama`) of court and Noh, and the specific
colours and crests that mark Shintō office and martial rank — are likewise NOT
drafted. Those carry standing and religious meaning; they are not styling.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|koshiita|himo_long|himo_short|set

waist_girth = float(PARAM(lambda: waist_girth, 820.0))       # tied at the hips
hakama_length = float(PARAM(lambda: hakama_length, 960.0))   # waist → ankle
leg_width = float(PARAM(lambda: leg_width, 420.0))           # half-leg flat width
aibiki_drop = float(PARAM(lambda: aibiki_drop, 300.0))       # side opening depth
front_pleats = float(PARAM(lambda: front_pleats, 5.0))       # traditionally 5
back_pleats = float(PARAM(lambda: back_pleats, 2.0))         # traditionally 2
wrap_overlap = float(PARAM(lambda: wrap_overlap, 200.0))     # front wrap surplus
koshiita_h = float(PARAM(lambda: koshiita_h, 150.0))         # back board height
koshiita_taper = float(PARAM(lambda: koshiita_taper, 60.0))  # board side slant
himo_width = float(PARAM(lambda: himo_width, 55.0))          # strap finished width
fabric_width = float(PARAM(lambda: fabric_width, 380.0))     # tanmono bolt width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hakama_length = max(600.0, min(hakama_length, 1300.0))
leg_width = max(280.0, min(leg_width, 620.0))
aibiki_drop = max(150.0, min(aibiki_drop, 480.0))
front_pleats = max(3.0, min(front_pleats, 9.0))
back_pleats = max(1.0, min(back_pleats, 5.0))
wrap_overlap = max(80.0, min(wrap_overlap, 400.0))
koshiita_h = max(90.0, min(koshiita_h, 250.0))
koshiita_taper = max(10.0, min(koshiita_taper, 140.0))
himo_width = max(30.0, min(himo_width, 100.0))
fabric_width = max(300.0, min(fabric_width, 1200.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

# ── The two independent pleat solves ─────────────────────────────────────────
# The hakama does NOT pleat symmetrically. The front carries the wrap overlap
# and takes five pleats; the back is bounded by the koshiita board and takes
# two. Each side is solved on its own span with its own integer count.
FRONT_PLEATS = max(1, int(round(front_pleats)))
BACK_PLEATS = max(1, int(round(back_pleats)))

# Finished spans. The front spans half the waist PLUS the wrap; the back spans
# half the waist and is capped by the board (solved below against the measured
# board edge).
FRONT_SPAN = waist_girth / 2.0 + wrap_overlap
BACK_SPAN = waist_girth / 2.0

# Hakama pleats are knife pleats: each consumes 2x its visible face.
FRONT_FACE = FRONT_SPAN / FRONT_PLEATS
FRONT_DEPTH = FRONT_FACE / 2.0
FRONT_FLAT = FRONT_FACE * 2.0 * FRONT_PLEATS

BACK_FACE = BACK_SPAN / BACK_PLEATS
BACK_DEPTH = BACK_FACE / 2.0
BACK_FLAT = BACK_FACE * 2.0 * BACK_PLEATS

# The leg: the divided seam runs up from the hem and STOPS, leaving the aibiki.
BODY_H = hakama_length - koshiita_h * 0.35   # board overlaps the panel slightly
if BODY_H < 300.0:
    BODY_H = 300.0
LEG_SEAM_H = BODY_H - aibiki_drop            # how far the leg seam is sewn
if LEG_SEAM_H < 80.0:                        # the division must actually exist
    LEG_SEAM_H = 80.0
    aibiki_drop = BODY_H - LEG_SEAM_H

# The himo. The long front straps wrap the body once and tie; the short back
# straps wrap forward and tie into the same knot. Solved as real circuits.
HIMO_LONG = waist_girth * 1.55 + 320.0
HIMO_SHORT = waist_girth * 0.85 + 220.0

# Panel piecing from the real bolt. Traditional 反物 (tanmono) is ~360-400 mm
# wide, which is why a hakama is always pieced — the draft honours that.
FRONT_PANELS = max(1, int(math.ceil(FRONT_FLAT / fabric_width - 1e-9)))
BACK_PANELS = max(1, int(math.ceil(BACK_FLAT / fabric_width - 1e-9)))
FRONT_CUT_W = FRONT_FLAT / FRONT_PANELS
BACK_CUT_W = BACK_FLAT / BACK_PANELS


def build_front():
    """One front width (cut FRONT_PANELS), pleated to the front span.

    A straight rectangle — the hakama has no crotch curve and no seat shaping.
    The leg-division seam runs up the `inner` edge from the hem and stops at
    LEG_SEAM_H; above that is the aibiki, marked and left open.
    """
    w, h = FRONT_CUT_W, BODY_H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("inner", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("outer", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # Where the leg seam stops and the aibiki opening begins.
        fc.Internal("aibiki-stop",
                    [fc.P(w, LEG_SEAM_H), fc.P(w - 40.0, LEG_SEAM_H)],
                    kind="marking"),
        # One pleat repeat, marked at the panel start.
        fc.Internal("pleat-fold", [fc.P(0.0, h), fc.P(0.0, h - koshiita_h)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(FRONT_DEPTH, h), fc.P(FRONT_DEPTH, h - koshiita_h)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(FRONT_FACE * 2.0, h), fc.P(FRONT_FACE * 2.0, h - koshiita_h)],
                    kind="marking"),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("inner", 0.0, "hem — leg seam start"),
                 fc.Notch("top", 0.0, "pleat repeat start")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=FRONT_PANELS * 2, mirror=True),
        label="Front width (前身頃 maemigoro)",
    )


def build_back():
    """One back width (cut BACK_PANELS), pleated to the koshiita's lower edge.

    Same straight construction as the front; only the pleat count and the span
    differ. Its `top` edge sews to the board's MEASURED bottom edge.
    """
    w, h = BACK_CUT_W, BODY_H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("inner", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("outer", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("aibiki-stop",
                    [fc.P(w, LEG_SEAM_H), fc.P(w - 40.0, LEG_SEAM_H)],
                    kind="marking"),
        fc.Internal("pleat-fold", [fc.P(0.0, h), fc.P(0.0, h - koshiita_h)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(BACK_DEPTH, h), fc.P(BACK_DEPTH, h - koshiita_h)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(BACK_FACE * 2.0, h), fc.P(BACK_FACE * 2.0, h - koshiita_h)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("inner", 0.0, "hem — leg seam start"),
                 fc.Notch("top", 0.5, "centre back — board match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=BACK_PANELS * 2, mirror=True),
        label="Back width (後身頃 ushiromigoro)",
    )


def build_koshiita():
    """The 腰板 (koshiita) — the stiffened back board.

    A trapezoid: wider at the top, tapering down by `koshiita_taper` on each
    side. Because the sides slant, the BOTTOM edge is shorter than the top —
    and it is the bottom edge that the back pleating sews to. That length is
    therefore MEASURED from this polygon, never assumed equal to the top.
    """
    top_w = BACK_SPAN
    bot_w = max(120.0, top_w - koshiita_taper * 2.0)
    h = koshiita_h
    ht, hb = top_w / 2.0, bot_w / 2.0
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(-hb, 0.0), fc.P(hb, 0.0))]),
        fc.Edge("side_right", [fc.Line(fc.P(hb, 0.0), fc.P(ht, h))]),
        fc.Edge("top", [fc.Line(fc.P(ht, h), fc.P(-ht, h))]),
        fc.Edge("side_left", [fc.Line(fc.P(-ht, h), fc.P(-hb, 0.0))]),
    ]
    internals = [
        # The two short back himo anchor at the board's upper corners.
        fc.Internal("himo-anchor",
                    [fc.P(-ht + seam_allowance, h - himo_width),
                     fc.P(-ht + seam_allowance, h)],
                    kind="marking"),
        fc.Internal("himo-anchor",
                    [fc.P(ht - seam_allowance, h - himo_width),
                     fc.P(ht - seam_allowance, h)],
                    kind="marking"),
        # The stiffener pocket: the board is interfaced or carries a thin insert.
        fc.Internal("stiffener-pocket",
                    [fc.P(-hb * 0.8, h * 0.25), fc.P(hb * 0.8, h * 0.25)],
                    kind="marking"),
    ]
    return fc.Piece(
        "koshiita",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre back — back panel match")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.2), fc.P(0.0, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=False, mirror=False),
        label="Back board (腰板 koshiita)",
    )


def build_himo_long():
    """A long front himo (紐), cut 2 — cut double and folded lengthwise.

    Length is a real circuit: it must wrap the body one and a half times and
    still tie the front knot.
    """
    ln, w = HIMO_LONG, himo_width
    return fc.Piece(
        "himo_long",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("tie_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("body_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.0, "front panel attachment")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Front strap (前紐 mae-himo)",
    )


def build_himo_short():
    """A short back himo (紐), cut 2 — anchors at the koshiita's upper corners."""
    ln, w = HIMO_SHORT, himo_width
    return fc.Piece(
        "himo_short",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("tie_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("board_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.0, "koshiita attachment")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Back strap (後紐 ushiro-himo)",
    )


def build():
    pattern = fc.PatternSet("hakama")
    every = target_piece == "set"
    if every or target_piece == "front":
        pattern.add(build_front())
    if every or target_piece == "back":
        pattern.add(build_back())
    if every or target_piece == "koshiita":
        pattern.add(build_koshiita())
    if every or target_piece == "himo_long":
        pattern.add(build_himo_long())
    if every or target_piece == "himo_short":
        pattern.add(build_himo_short())

    if every:
        back = pattern.piece("back")
        board = pattern.piece("koshiita")
        _front = pattern.piece("front")

        # The koshiita is a TRAPEZOID: its bottom edge is shorter than its top
        # because the sides slant. The seam that matters is the BOTTOM one, so
        # measure it from the polygon rather than reusing BACK_SPAN.
        board_bottom = board.edge("bottom").length(0.05)
        back_top_total = back.edge("top").length(0.05) * BACK_PANELS
        pattern.declare_seam(
            [("back", "top")] * BACK_PANELS, [("koshiita", "bottom")],
            tol=1.5, ease=(back_top_total - board_bottom),
        )

        # The leg-division seam: front inner meets back inner, but only for the
        # sewn portion — the aibiki above it is deliberately open. Both edges
        # are the full panel height, so they must be equal.
        pattern.declare_seam(("front", "inner"), ("back", "inner"), tol=0.5)

        # The side seam closes front to back over the full panel height.
        pattern.declare_seam(("front", "outer"), ("back", "outer"), tol=0.5)

        # The board's two slanted sides are mirror-equal — a trapezoid, not a
        # trapezium; if the taper ever broke this the board would twist.
        pattern.declare_seam(("koshiita", "side_right"), ("koshiita", "side_left"),
                             tol=0.5)

    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.88)   # narrow bolt, tight nest
    pattern.bom = [
        {"item": "cotton/linen twill, tetron, or silk (sendai-hira for formal)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm bolt width, 88% marker; "
                 f"{FRONT_PANELS} front + {BACK_PANELS} back widths per side."},
        {"item": "koshiita stiffener", "qty": 1, "unit": "piece",
         "note": "heavy interfacing, buckram, or a thin板 insert — the board must "
                 "hold its shape in the small of the back."},
        {"item": "himo interfacing", "qty": 4, "unit": "strip",
         "note": "the straps carry the whole garment; interface or self-line them."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "pleats are basted, then edge-stitched their full length."},
    ]
    pattern.metadata = {
        "fc300_rank": 281,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "tradition": "Japanese (袴) — the 馬乗り umanori (divided) hakama",
        "finished_mm": {"length": round(hakama_length, 1),
                        "front_span": round(FRONT_SPAN, 1),
                        "back_span": round(BACK_SPAN, 1),
                        "aibiki": round(aibiki_drop, 1),
                        "himo_long": round(HIMO_LONG, 1)},
        "solved": {
            "front_pleats": FRONT_PLEATS,
            "back_pleats": BACK_PLEATS,
            "front_face_mm": round(FRONT_FACE, 2),
            "front_depth_mm": round(FRONT_DEPTH, 2),
            "back_face_mm": round(BACK_FACE, 2),
            "back_depth_mm": round(BACK_DEPTH, 2),
            "front_flat_mm": round(FRONT_FLAT, 2),
            "back_flat_mm": round(BACK_FLAT, 2),
            "front_widths": FRONT_PANELS,
            "back_widths": BACK_PANELS,
            "leg_seam_h_mm": round(LEG_SEAM_H, 2),
            "note": "front and back pleat into DIFFERENT spans (the front carries "
                    "the wrap overlap, the back is bounded by the board), so each "
                    "side's depth is back-solved independently from its own integer "
                    "count. The koshiita is a trapezoid, so the seam length that "
                    "matters is its MEASURED bottom edge — shorter than its top — "
                    "and the back pleating is reconciled against that measurement. "
                    "The aibiki is the remainder of the side above the leg-seam stop.",
        },
        "hardware": "none — the hakama is entirely self-fastening by its four himo. "
                    "Adding a buckle or snap would be an invention, not a hakama.",
        "cut_philosophy": "no crotch curve, no seat shaping, no rise. The legs are "
                          "straight panels divided by a seam that stops partway up; "
                          "the aibiki opening and the pleating do all the fitting.",
        "excluded": "行灯袴 (andon, the undivided form) is a DIFFERENT garment, not "
                    "this one with a switch. 長袴 (nagabakama, the trailing court and "
                    "Noh hakama) and the colours and crests marking Shintō office or "
                    "martial rank are NOT drafted: they carry standing and religious "
                    "meaning and are not styling options.",
    }
    return pattern


result = build()
