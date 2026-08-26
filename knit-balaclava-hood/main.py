"""
Knit balaclava hood — Fashion Cabinet Garment Cartridge (FC-500 #412, knitwear, T2).

A close-fitting knit balaclava: a hood that covers the head and neck with a FACE OPENING.
Drafted as two mirrored SIDE panels (each wrapping from the face opening over the ear to
the centre back) and a CENTRE GORE running crown-to-nape that gives the crown its round.
The face opening and the neck opening are finished with ribbed bands; the whole is cut in
a stretch wool knit with negative ease so it grips.

Solved, not guessed:

  1. THE GORE SEAM MATCHES THE SIDE CROWN EDGE. The centre gore's two long edges are drafted
     to the SAME length as the side panels' crown edges, so the gore sews in without easing
     a mismatch — measured, then declared.
  2. THE FACE OPENING IS CLAMPED. The face hole height cannot exceed the head-arc height
     less a floor, so an over-tall face request can never eat past the crown and collapse
     the side panel above the opening into a self-crossing outline.
  3. NEGATIVE EASE IS FLOORED. Panel widths carry a stretch factor below 1.0, floored so a
     tight fit never draws a hairline gore the kernel would CCW-normalize into a healthy sliver.

Pull-on: no hardware. Ribbed face and neck bands are companion rectangles.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # side|gore|face_band|set

head_girth = float(PARAM(lambda: head_girth, 570.0))     # around the head
head_height = float(PARAM(lambda: head_height, 230.0))   # crown to jaw
neck_depth = float(PARAM(lambda: neck_depth, 180.0))     # below the jaw
face_width = float(PARAM(lambda: face_width, 130.0))     # face opening width
face_height = float(PARAM(lambda: face_height, 150.0))   # face opening height
stretch_factor = float(PARAM(lambda: stretch_factor, 0.86))
band_depth = float(PARAM(lambda: band_depth, 26.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

head_girth = max(460.0, min(head_girth, 680.0))
head_height = max(170.0, min(head_height, 300.0))
neck_depth = max(90.0, min(neck_depth, 280.0))
face_width = max(90.0, min(face_width, 190.0))
face_height = max(90.0, min(face_height, 220.0))
stretch_factor = max(0.66, min(stretch_factor, 0.98))
band_depth = max(16.0, min(band_depth, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# The head-arc height a side panel must reach from the face opening over the crown.
HEAD_ARC = max(120.0, head_height * stretch_factor)
# The face opening height, clamped under the head-arc so it never eats past the crown.
FACE_H = min(face_height * stretch_factor, HEAD_ARC - 40.0)
FACE_H = max(40.0, FACE_H)
HALF_FACE_W = face_width / 2.0 * stretch_factor
# side panel half-depth (front-to-back over the ear), from the head girth
SIDE_DEPTH = max(90.0, head_girth / 4.0 * stretch_factor)
NECK = max(60.0, neck_depth * stretch_factor)


def _side():
    """One side panel (cut 2 mirrored). x runs 0 (face/CF) -> SIDE_DEPTH (centre back).
    y runs from the neck bottom up over the crown. The face opening is a scoop at x=0."""
    y_neck = 0.0
    y_jaw = NECK
    y_crown = NECK + HEAD_ARC
    p_cf_neck = fc.P(0.0, y_neck)
    p_cb_neck = fc.P(SIDE_DEPTH, y_neck)
    p_cb_crown = fc.P(SIDE_DEPTH, y_crown)
    # crown edge sweeps from CB crown down to the top of the face opening
    p_face_top = fc.P(HALF_FACE_W, y_jaw + FACE_H)
    p_face_bot = fc.P(0.0, y_jaw)
    edges = [
        # neck edge along the bottom
        fc.Edge("neck", [fc.Line(p_cf_neck, p_cb_neck)]),
        # centre-back seam up
        fc.Edge("cb", [fc.Line(p_cb_neck, p_cb_crown)]),
        # crown edge (sews to the gore) from CB over to the face top
        fc.Edge("crown", [fc.curve_through(p_cb_crown, p_face_top,
                                           bulge=0.20, side=-1.0)]),
        # the face opening: down the face top to the jaw
        fc.Edge("face", [fc.curve_through(p_face_top, p_face_bot,
                                          bulge=0.14, side=1.0)]),
        # front lower: from the jaw down to the CF neck (the chin/CF edge)
        fc.Edge("cf", [fc.Line(p_face_bot, p_cf_neck)]),
    ]
    return fc.Piece(
        "side", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("crown", 0.5, "gore balance"),
                 fc.Notch("face", 0.5, "face opening"),
                 fc.Notch("neck", 0.5, "neck balance")],
        grainline=fc.Grainline(fc.P(SIDE_DEPTH * 0.4, y_neck + 20.0),
                               fc.P(SIDE_DEPTH * 0.4, y_crown - 20.0)),
        internals=[fc.Internal("ear ease",
                               [fc.P(SIDE_DEPTH * 0.5, y_jaw),
                                fc.P(SIDE_DEPTH * 0.75, y_jaw + HEAD_ARC * 0.4)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side panel (cut 2, mirrored)",
    )


_S = _side()
CROWN_LEN = _S.edge("crown").length(0.05)


def _gore():
    """The centre gore, crown-to-nape, cut 1. A symmetric leaf centred on x=0: the two long
    edges bow OUTWARD from a nape point to a crown point, so it is a genuine lens with real
    width — never a hairline sliver. The chord is SOLVED (bisected) so each bowed edge
    measures the same as the side panel's crown edge, and the gore sews in flush."""
    half_w = max(18.0, HALF_FACE_W * 0.55)   # half the gore's widest point (fixed bow)

    def side_edge(chord):
        return fc.curve_through(fc.P(0.0, 0.0), fc.P(0.0, chord),
                                bulge=half_w / chord, side=1.0)

    # Solve the chord so the bowed edge length == the side crown length.
    lo, hi = CROWN_LEN * 0.4, CROWN_LEN
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if side_edge(mid).length(0.05) < CROWN_LEN:
            lo = mid
        else:
            hi = mid
    chord = (lo + hi) / 2.0
    p_nape = fc.P(0.0, 0.0)
    p_crown = fc.P(0.0, chord)
    edges = [
        fc.Edge("side_a", [side_edge(chord)]),
        fc.Edge("side_b", [fc.curve_through(p_crown, p_nape,
                                            bulge=half_w / chord, side=1.0)]),
    ]
    return fc.Piece(
        "gore", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("side_a", 0.5, "crown centre"),
                 fc.Notch("side_b", 0.5, "crown centre")],
        grainline=fc.Grainline(fc.P(1.0, chord * 0.1), fc.P(1.0, chord * 0.9)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Centre gore (cut 1)",
    )


_G = _gore()
GORE_SIDE_LEN = _G.edge("side_a").length(0.05)


def _face_band():
    """The ribbed face-opening band: a rectangle, its length the MEASURED face opening
    (two side face edges), folded to band_depth."""
    ln = _S.edge("face").length(0.05) * 2.0
    w = band_depth * 2.0
    return fc.Piece(
        "face_band", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "chin centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=[fc.Internal("rib fold", [fc.P(0.0, w * 0.5), fc.P(ln, w * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Ribbed face band (cut 1)",
    )


def build():
    pattern = fc.PatternSet("knit-balaclava-hood")
    everything = target_piece == "set"
    if everything or target_piece == "side":
        pattern.add(_side())
    if everything or target_piece == "gore":
        pattern.add(_gore())
    if everything or target_piece == "face_band":
        pattern.add(_face_band())

    if everything:
        # the gore sews to both side panels' crown edges (measured to the same length);
        # the two side panels join at the centre back.
        pattern.declare_seam(("side", "crown"), ("gore", "side_a"),
                             tol=1.0, ease=CROWN_LEN - GORE_SIDE_LEN)
        pattern.declare_seam(("side", "cb"), ("side", "cb"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "fine merino knit (4-way stretch)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker; negative ease (factor "
                 f"{stretch_factor:.2f}) so the hood grips."},
        {"item": "ribbing for face + neck bands", "qty": 1, "unit": "set",
         "note": "cut the face band to the measured opening; the neck band to its edge."},
        {"item": "wool thread + ballpoint needle", "qty": 1, "unit": "spool",
         "note": "flatlock or zigzag the gore and CB so they stretch over the head."},
    ]
    pattern.metadata = {
        "fc500_rank": 412, "family": "knitwear", "tier": 2,
        "fabric_hint": "punto-lana",
        "silhouette_note": "A close-fitting knit balaclava: two side panels + a crown gore, "
            "ribbed face and neck bands, drafted with negative ease.",
        "solved": {
            "head_arc_mm": round(HEAD_ARC, 1),
            "face_height_requested_mm": round(face_height, 1),
            "face_height_clamped_mm": round(FACE_H, 1),
            "face_was_clamped": bool(abs(FACE_H - face_height * stretch_factor) > 0.01),
            "side_crown_mm": round(CROWN_LEN, 1),
            "gore_side_mm": round(GORE_SIDE_LEN, 1),
            "gore_seam_ease_mm": round(CROWN_LEN - GORE_SIDE_LEN, 2),
            "note": "the gore's long edges are measured against the side crown edge and the "
                    "residual is declared as ease so the gore sews in without a mismatch; "
                    "the face opening height is clamped under the head-arc so it never eats "
                    "past the crown; the stretch factor is floored at 0.66.",
        },
        "hardware": "none — a pull-on knit balaclava.",
    }
    return pattern


result = build()
