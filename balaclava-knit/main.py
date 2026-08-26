"""
Knit balaclava hood — FC-400 rank #337, Lane 4 (knitwear). Fashion Cabinet Cartridge.

A close-fitting knit hood that covers the head and neck with an opening for the face. It
is drafted as TWO mirrored side halves joined by a crown-and-back seam, plus a face-opening
edge (ribbed) and a neck-tube extension that tucks under the collar. The whole thing is
worked in a stretchy rib or fine jersey and pulls onto the head, so the draft is SMALLER
than the head and stretches on — SIGNED negative knit ease, floored.

What this cartridge owns:
  - THE HOOD HALF (cut 2, mirrored): a profile from the forehead over the crown to the
    nape, down the neck tube, with a face-opening curve at the front.
  - THE FACE-OPENING band (ribbed) and the neck-tube hem, declared as interfaces.

Solving and clamps. The head profile is drafted from the head girth and the face-opening
height, both floored: a tiny head or a huge face opening would otherwise drive the crown
run or the chin run negative and invert the profile after CCW normalization. The neck-tube
width is the larger of the neck girth quarter and a floor, so it always fits over the neck.

Hardware: none — a balaclava pulls on and has no closure.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # hood|face_band|set

head_girth = float(PARAM(lambda: head_girth, 570.0))
head_height = float(PARAM(lambda: head_height, 250.0))    # chin to crown
neck_girth = float(PARAM(lambda: neck_girth, 380.0))
neck_tube = float(PARAM(lambda: neck_tube, 150.0))        # how far the neck tube extends
face_width = float(PARAM(lambda: face_width, 130.0))      # face-opening half-width
face_height = float(PARAM(lambda: face_height, 170.0))    # face-opening height
knit_ease = float(PARAM(lambda: knit_ease, -50.0))       # SIGNED negative (pulls on)
band_width = float(PARAM(lambda: band_width, 26.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

head_girth = max(460.0, min(head_girth, 680.0))
head_height = max(180.0, min(head_height, 340.0))
neck_girth = max(280.0, min(neck_girth, 520.0))
neck_tube = max(60.0, min(neck_tube, 300.0))
face_width = max(70.0, min(face_width, 200.0))
face_height = max(90.0, min(face_height, 260.0))
knit_ease = max(-140.0, min(knit_ease, 40.0))
band_width = max(15.0, min(band_width, 50.0))
seam_allowance = max(5.0, min(seam_allowance, 16.0))

DRAFT_GIRTH = max(360.0, head_girth + knit_ease)
# Half the head girth is the crown-to-nape run for one side half.
HALF_HEAD = DRAFT_GIRTH / 2.0
H = head_height
# Face opening clamped inside the head profile.
FW = max(50.0, min(face_width, HALF_HEAD - 40.0))
FH = max(60.0, min(face_height, H - 40.0))
FACE_CLAMPED = (face_width > HALF_HEAD - 40.0) or (face_height > H - 40.0)
# Neck tube half-width: the larger of the neck half (from the eased neck girth) and a
# floor, but never wider than the head half.
DRAFT_NECK = max(280.0, neck_girth + knit_ease)
NECK_W = max(70.0, min(DRAFT_NECK / 2.0, HALF_HEAD))


def build_hood():
    """One hood half, cut 2 mirrored. Frame: x=0 centre (crown/back seam), y=0 neck-tube
    hem. Profile: up the back seam over the crown, down the forehead to the face opening,
    around the face opening, and down to the neck tube."""
    # Back/crown seam runs up the centre from the neck-tube hem to the crown top.
    crown_top = fc.P(0.0, H + neck_tube)
    hem_back = fc.P(0.0, 0.0)
    # Forehead point: out from the crown toward the face.
    forehead = fc.P(HALF_HEAD, H + neck_tube - FH * 0.4)
    # Face opening lower point (chin side).
    face_low = fc.P(HALF_HEAD - FW * 0.3, neck_tube)
    # Neck-tube front bottom.
    hem_front = fc.P(NECK_W, 0.0)
    return fc.Piece(
        "hood",
        [
            # centre-back/crown seam: hem up to the crown
            fc.Edge("crown_seam", [fc.Line(hem_back, crown_top)]),
            # crown to forehead over the top of the head
            fc.Edge("crown", [fc.curve_through(crown_top, forehead, bulge=0.14, side=1.0)]),
            # face opening: forehead down to the chin-side face-low point
            fc.Edge("face", [fc.curve_through(forehead, face_low, bulge=0.18, side=-1.0)]),
            # chin / neck-tube front: face-low down to the front hem
            fc.Edge("chin", [fc.Line(face_low, hem_front)]),
            # neck-tube hem
            fc.Edge("hem", [fc.Line(hem_front, hem_back)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("crown_seam", 0.6, "crown point"),
                 fc.Notch("face", 0.5, "cheek")],
        grainline=fc.Grainline(fc.P(HALF_HEAD * 0.4, neck_tube * 0.5),
                               fc.P(HALF_HEAD * 0.4, H + neck_tube - 30.0)),
        internals=[fc.Internal("head line", [fc.P(0.0, neck_tube), fc.P(HALF_HEAD, neck_tube)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood half",
    )


def _rib(name, finished_len, finished_height, qty, label):
    band_h = max(18.0, 2.0 * finished_height)
    length = max(60.0, finished_len) + 2.0 * seam_allowance
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line",
                               [fc.P(0.0, band_h / 2.0), fc.P(length, band_h / 2.0)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("balaclava-knit")
    hood = build_hood()

    names = ("hood", "face_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["hood"]:
        pattern.add(hood)
    face_run = 2.0 * hood.edge("face").length(0.05)
    if wanted["face_band"]:
        pattern.add(_rib("face_band", face_run, band_width, 1, "Face-opening band (rib)"))

    # The two hood halves join along the crown/back seam.
    pattern.declare_seam(("hood", "crown_seam"), ("hood", "crown_seam"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.60)
    pattern.bom = [
        {"item": "fine merino rib / stretch jersey",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker. A stretchy knit is "
                 "essential — the balaclava is drafted under the head and stretches on."},
        {"item": "rib for the face band", "qty": 1, "unit": "set",
         "note": "the face-opening band holds the opening and finishes the edge"},
        {"item": "thread (woolly nylon)", "qty": 1, "unit": "spool",
         "note": "overlock or narrow zigzag — the seams must stretch"},
    ]
    pattern.metadata = {
        "fc400_rank": 337, "family": "knitwear", "lane": 4,
        "fabric_hint": "wool-merino",
        "architecture": "two mirrored hood halves joined at a crown-and-back seam, with a "
                        "ribbed face opening and a neck tube",
        "knit_ease_mm": round(knit_ease, 1),
        "solved": {
            "draft_girth_mm": round(DRAFT_GIRTH, 1),
            "half_head_mm": round(HALF_HEAD, 1),
            "face_half_width_mm": round(FW, 1),
            "face_height_mm": round(FH, 1),
            "face_clamped": FACE_CLAMPED,
            "neck_tube_half_mm": round(NECK_W, 1),
            "note": "the face opening is clamped inside the head profile so the crown and "
                    "chin runs never go negative and invert the hood; the draft girth is "
                    "floored for the negative-ease pull-on",
        },
        "hardware": "none — a balaclava pulls on and has no closure",
    }
    return pattern


result = build()
