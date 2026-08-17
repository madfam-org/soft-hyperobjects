"""
Pleated Skirt — FC-100 rank #34. Fashion Cabinet Garment Cartridge.

The commons' first PLEAT-SPREADING draft: a knife-pleated skirt built from
rectangular panels whose flat width is the finished waist SPREAD by a pleat
multiplier — half-panel width = (waist_girth + waist_ease) / 4 ×
pleat_multiplier, so at the default multiplier 3.0 every pleat hides 2× its
visible face (fully pleated) and the panel presses back down to the finished
waist. Pleat markings are generated per pleat in a loop: a solid fold line,
a dashed-role placement line, and a 3-point arrow at the waist showing the
fold direction (toward the center fold). Front and back are identical panels
cut 1 on fold; the zipper opens the FRONT side seam (the fold edges leave no
CF/CB seam to host it) with a zipper-stop notch on both side edges. The
straight cut-1 waistband equals the FINISHED pleated-down waist + overlap +
2 seam allowances — never the panel widths — and is verified against the
four unpleated waist edges with an eased multi-edge check whose ease is the
computed total pleat intake minus the band's overlap-and-allowance extras,
so the accounting closes to delta 0 by construction.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|waistband|set

waist_girth      = float(PARAM(lambda: waist_girth, 700.0))
skirt_length     = float(PARAM(lambda: skirt_length, 560.0))
waist_ease       = float(PARAM(lambda: waist_ease, 15.0))
pleat_multiplier = float(PARAM(lambda: pleat_multiplier, 3.0))
pleat_face       = float(PARAM(lambda: pleat_face, 30.0))
zipper_length    = float(PARAM(lambda: zipper_length, 180.0))
overlap          = float(PARAM(lambda: overlap, 30.0))
seam_allowance   = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance    = float(PARAM(lambda: hem_allowance, 30.0))

waist_girth = max(450.0, min(waist_girth, 1500.0))
skirt_length = max(350.0, min(skirt_length, 900.0))
waist_ease = max(0.0, min(waist_ease, 80.0))
pleat_multiplier = max(2.0, min(pleat_multiplier, 3.5))
pleat_face = max(15.0, min(pleat_face, 60.0))
zipper_length = max(120.0, min(zipper_length, skirt_length * 0.45))
overlap = max(0.0, min(overlap, 60.0))

# ── Pleat spreading (the star) ──────────────────────────────────────────────
FINISHED_QUARTER = (waist_girth + waist_ease) / 4.0  # what a half-panel presses down to
HALF_W = FINISHED_QUARTER * pleat_multiplier         # unpleated half-panel width
PLEAT_COUNT = max(1, int(HALF_W // (pleat_face * 3.0)))   # knife pleats per half-panel
REPEAT = HALF_W / PLEAT_COUNT                        # flat width of one pleat unit
INTAKE = (HALF_W - FINISHED_QUARTER) / PLEAT_COUNT   # fabric hidden per pleat (2× fold depth)
FACE = REPEAT - INTAKE                               # visible face at the waist
BAND_H = 38.0        # finished waistband height (folds double)
ARROW_DROP = 10.0    # fold arrow sits this far below the waist stitch line


def _pleat_internals():
    """Fold line + placement line + fold-direction arrow for each knife pleat.

    Repeat k spans [k·REPEAT, (k+1)·REPEAT]: the visible FACE leads (so the
    center fold starts flat), the INTAKE strip trails, and the fold line
    bisects the intake — folding there lays the crease exactly on the
    placement line and hides INTAKE mm. All pleats press toward the center
    fold; the mirrored halves are symmetric about CF/CB.
    """
    marks = []
    for k in range(PLEAT_COUNT):
        x_place = k * REPEAT + FACE          # where the fold edge must land
        x_fold = x_place + INTAKE / 2.0      # crease line, bisects the intake
        marks.append(fc.Internal(
            f"pleat {k + 1} fold line",
            [fc.P(x_fold, 0.0), fc.P(x_fold, skirt_length)],
            kind="marking",
        ))
        marks.append(fc.Internal(
            f"pleat {k + 1} placement line (dashed)",
            [fc.P(x_place, 0.0), fc.P(x_place, skirt_length)],
            kind="marking",
        ))
        marks.append(fc.Internal(
            f"pleat {k + 1} fold arrow",
            [fc.P(x_fold, skirt_length - ARROW_DROP),
             fc.P(x_place, skirt_length - ARROW_DROP - 12.0),
             fc.P(x_fold, skirt_length - ARROW_DROP - 24.0)],
            kind="marking",
        ))
    return marks


def _panel(name, label):
    """One rectangular pleated panel, center line on the fold."""
    w, ln = HALF_W, skirt_length
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("waist", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "side": 15.0},  # side seam hosts the zipper
        notches=[fc.Notch("side", 1.0 - zipper_length / ln, "zipper stop")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.1), fc.P(w * 0.5, ln * 0.9)),
        internals=_pleat_internals(),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _waistband():
    """Straight cut-1 band = FINISHED (pleated-down) waist + overlap + 2sa.

    Sized off the finished waist, NOT the spread panel widths — the pleat
    intake is what separates the two, and the declared seam check proves it.
    """
    finished_waist = waist_girth + waist_ease
    length = finished_waist + overlap + 2.0 * seam_allowance
    band_h = 2.0 * (BAND_H + seam_allowance)
    return fc.Piece(
        "waistband",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,  # drafted cut-ready; allowances live in the rectangle
        notches=[
            fc.Notch("bottom", (seam_allowance + finished_waist * 0.25) / length, "CF match"),
            fc.Notch("bottom", (seam_allowance + finished_waist * 0.50) / length,
                     "right side seam"),
            fc.Notch("bottom", (seam_allowance + finished_waist * 0.75) / length, "CB match"),
        ],
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1),
        label="Waistband",
    )


def build():
    pattern = fc.PatternSet("pleated-skirt")
    front = _panel("front", "Pleated Skirt Front")
    back = _panel("back", "Pleated Skirt Back")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
        pattern.bom.append({
            "item": "side zipper",
            "qty": round(zipper_length),
            "unit": "mm",
            "note": "set into the front-left side seam, closing at the zipper-stop notch",
        })
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "waistband":
        pattern.add(_waistband())
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Pleat accounting: four unpleated waist edges (each panel is cut on
        # fold, so its waist edge sews in twice) close onto the finished band
        # bottom. Ease = total pleat intake − the band's overlap + 2sa extras,
        # computed from the same formulas that drafted the geometry → delta 0.
        intake_total = 4.0 * (HALF_W - FINISHED_QUARTER)
        pattern.declare_seam(
            [("front", "waist"), ("front", "waist"), ("back", "waist"), ("back", "waist")],
            [("waistband", "bottom")],
            tol=2.5,
            ease=intake_total - (overlap + 2.0 * seam_allowance),
        )
    pattern.metadata = {
        "fc100_rank": 34,
        "fabric_hint": "popelina-algodon",
        "pleat_count": PLEAT_COUNT,
        "pleats_total": 4 * PLEAT_COUNT,
        "pleat": {
            "face_mm": round(FACE, 2),
            "intake_mm": round(INTAKE, 2),
            "repeat_mm": round(REPEAT, 2),
            "multiplier": pleat_multiplier,
        },
        "drafting": "half-panels spread to (waist + ease)/4 × pleat_multiplier; knife-pleat "
                    "fold/placement/arrow markings generated per pleat; band = finished waist "
                    "+ overlap + 2sa, eased against the unpleated waists by the pleat intake",
    }
    return pattern


result = build()
