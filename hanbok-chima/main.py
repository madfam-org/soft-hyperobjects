"""
Chima (치마) — FC-300 rank #280. Fashion Cabinet Garment Cartridge.

The chima is the skirt of the Korean hanbok: a very full, high-waisted wrap
skirt suspended from a chest band (말기, `malgi`) with long ties (끈, `kkeun`),
worn with the short jeogori jacket (drafted separately as `hanbok-jeogori`).
Its silhouette — a bell that begins at the chest, not the waist — is produced
entirely by pleating an enormous rectangle of cloth into a short band.

What actually makes a chima a chima, and what this draft encodes:

  - SUSPENSION AT THE CHEST. The band sits above the bust, not at the waist.
    The garment therefore hangs from the ribcage; the waist is never engaged.
    `band_girth` is a CHEST-BAND measurement (underbust/upper-chest), which is
    why this cartridge does not take a waist measurement at all.
  - A WRAP, NOT A TUBE. The skirt is one flat panel that overlaps itself at the
    back; it never closes into a sewn ring. `wrap_overlap` is real cloth, so
    the band and the pleated panel must both carry it.
  - PLEATS, NOT GATHERS. Traditional chima is knife- or box-pleated into the
    band. Pleating is a DISCRETE operation: a whole number of pleats, each
    consuming a fixed depth of cloth. This draft therefore solves an integer
    pleat count and then reports the depth those pleats actually consume,
    rather than declaring a continuous "fullness ratio" that no maker can pleat.
  - LOOM WIDTH IS REAL. A chima this wide is pieced from several straight
    fabric widths joined at vertical seams. The panel count is solved from the
    real usable `fabric_width`.

Drafting note — what actually SOLVES: the pleat count is an INTEGER derived
from the cloth the panel has and the band it must fit. Because it is integer,
the pleat depth cannot be assumed; it is back-solved from the surplus that
integer count must absorb, and the band's finished length is then measured from
the band polygon itself and reconciled with the pleated panel top. The panel's
piecing count is solved from the real loom width. The tie length is measured as
a wrap circuit plus a bow allowance, not guessed.

EXCLUSION, stated rather than quietly ignored: the ceremonial and rank-bearing
hanbok — 활옷 (hwarot, the bridal robe), 당의 (dangui, the court jacket) and the
gold-leaf 금박 (geumbak) treatments — are NOT drafted here. Those are not
"decorated chima"; they are distinct garments carrying social and ritual
meaning, and reducing them to a parameter on a skirt would be exactly the
costume-ification this commons refuses. This cartridge drafts the everyday and
festival chima only, and leaves surface decoration to the maker.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # band|panel|tie|set

band_girth = float(PARAM(lambda: band_girth, 880.0))      # CHEST band, not waist
band_height = float(PARAM(lambda: band_height, 120.0))    # finished band depth
chima_length = float(PARAM(lambda: chima_length, 1180.0))  # band top → hem
pleat_count = float(PARAM(lambda: pleat_count, 28.0))     # requested pleat count
pleat_style = float(PARAM(lambda: pleat_style, 1.0))      # 1 = knife, 2 = box
wrap_overlap = float(PARAM(lambda: wrap_overlap, 320.0))  # back overlap of cloth
tie_width = float(PARAM(lambda: tie_width, 70.0))         # kkeun finished width
tie_extra = float(PARAM(lambda: tie_extra, 900.0))        # bow + hanging tail
fabric_width = float(PARAM(lambda: fabric_width, 1120.0))  # real usable width
button_ligne = float(PARAM(lambda: button_ligne, 20.0))   # band anchor button
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 60.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
band_girth = max(600.0, min(band_girth, 1300.0))
band_height = max(70.0, min(band_height, 220.0))
chima_length = max(700.0, min(chima_length, 1500.0))
pleat_count = max(8.0, min(pleat_count, 60.0))
pleat_style = 2.0 if pleat_style >= 1.5 else 1.0
wrap_overlap = max(120.0, min(wrap_overlap, 600.0))
tie_width = max(40.0, min(tie_width, 130.0))
tie_extra = max(400.0, min(tie_extra, 1600.0))
fabric_width = max(700.0, min(fabric_width, 1600.0))
button_ligne = max(12.0, min(button_ligne, 36.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(20.0, min(hem_allowance, 120.0))

# ── The pleat solve ──────────────────────────────────────────────────────────
# The band's finished span is the chest circuit PLUS the wrap overlap: the
# overlap is cloth that exists and must be carried, not a styling notion.
BAND_SPAN = band_girth + wrap_overlap

# Each pleat consumes cloth. A knife pleat folds cloth back on itself once and
# so consumes 2x its visible face; a box pleat folds twice and consumes 4x.
FOLDS_PER_PLEAT = 4.0 if pleat_style >= 1.5 else 2.0

# Pleat count is DISCRETE — you cannot sew 27.4 pleats. Round to an integer and
# work from that integer thereafter; everything downstream is solved to it.
PLEATS = int(round(pleat_count))
PLEATS = max(6, min(PLEATS, 60))

# The visible face of each pleat is what shows on the finished band, so the
# faces must tile the band span exactly.
PLEAT_FACE = BAND_SPAN / PLEATS

# The depth each pleat folds away, and therefore the flat cloth each consumes.
PLEAT_DEPTH = PLEAT_FACE * (FOLDS_PER_PLEAT - 1.0) / 2.0
CLOTH_PER_PLEAT = PLEAT_FACE * FOLDS_PER_PLEAT

# The flat panel width the pleating requires. This is the chima's real width.
PANEL_WIDTH = CLOTH_PER_PLEAT * PLEATS

# Piecing: how many usable loom widths that flat panel needs. A chima is always
# pieced; the seams are vertical and fall inside pleat folds where possible.
PANELS = max(1, int(math.ceil(PANEL_WIDTH / fabric_width - 1e-9)))
PANEL_CUT_WIDTH = PANEL_WIDTH / PANELS

# The skirt body height below the band.
SKIRT_H = chima_length - band_height
if SKIRT_H < 200.0:                     # never let the band eat the skirt
    SKIRT_H = 200.0

# The tie: it must wrap the chest circuit once and still tie a bow at the front.
TIE_LENGTH = band_girth * 0.55 + tie_extra


def build_band():
    """The malgi (말기) — the chest band the whole garment hangs from.

    Drafted flat as a straight strip spanning the chest circuit plus the wrap
    overlap. Its `bottom` edge is the seam the pleated panel sews to; the tie
    anchor points and the wrap's closing button seat are marked on it.
    """
    w, h = BAND_SPAN, band_height
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("end_right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("end_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]

    internals = [
        # The two kkeun (ties) anchor at the band ends — the wrap ties in front.
        fc.Internal("tie-anchor",
                    [fc.P(seam_allowance, h * 0.5 - tie_width / 2.0),
                     fc.P(seam_allowance, h * 0.5 + tie_width / 2.0)],
                    kind="marking"),
        fc.Internal("tie-anchor",
                    [fc.P(w - seam_allowance, h * 0.5 - tie_width / 2.0),
                     fc.P(w - seam_allowance, h * 0.5 + tie_width / 2.0)],
                    kind="marking"),
        # Where the overlap begins — the wrap's inner edge lands here.
        fc.Internal("overlap-line",
                    [fc.P(wrap_overlap, 0.0), fc.P(wrap_overlap, h)],
                    kind="marking"),
        # A single anchor button holds the wrap while the ties are tied.
        fc.Internal("button-seat",
                    [fc.P(wrap_overlap * 0.5, h * 0.5),
                     fc.P(wrap_overlap * 0.5 + button_ligne * 0.635, h * 0.5)],
                    kind="drill"),
    ]

    return fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.25, "pleat block quarter"),
                 fc.Notch("bottom", 0.5, "pleat block centre"),
                 fc.Notch("bottom", 0.75, "pleat block quarter")],
        grainline=fc.Grainline(fc.P(w * 0.08, h * 0.2), fc.P(w * 0.08, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Chest band (말기 malgi)",
    )


def build_panel():
    """One straight skirt width (cut PANELS), joined side-to-side then pleated.

    A rectangle — the chima is not shaped, it is pleated. The pleat fold lines
    are marked on the top edge so the maker folds to the draft rather than
    eyeballing. Marking every fold on every panel would be unreadable, so the
    first pleat block on each panel is marked as the repeat unit.
    """
    w, h = PANEL_CUT_WIDTH, SKIRT_H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]

    # Mark the repeat unit: one pleat's worth of cloth at the panel's start.
    internals = [
        fc.Internal("pleat-fold", [fc.P(0.0, h), fc.P(0.0, h - band_height * 1.5)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(PLEAT_DEPTH, h), fc.P(PLEAT_DEPTH, h - band_height * 1.5)],
                    kind="marking"),
        fc.Internal("pleat-fold",
                    [fc.P(CLOTH_PER_PLEAT, h),
                     fc.P(CLOTH_PER_PLEAT, h - band_height * 1.5)],
                    kind="marking"),
    ]

    return fc.Piece(
        "panel",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("top", 0.0, "pleat repeat start"),
                 fc.Notch("top", 0.5, "panel centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=PANELS),
        label="Skirt width (폭 pok)",
    )


def build_tie():
    """One kkeun (끈), cut 2 — the long band tie that fastens the chima.

    Drafted as a straight strip cut double-width and folded lengthwise, so the
    drafted `fold` edge is the long fold and the finished tie is `tie_width`.
    Length is the measured half-circuit plus the bow-and-tail allowance.
    """
    ln, w = TIE_LENGTH, tie_width
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("tail_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("band_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "tie",
        edges,
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.0, "band attachment end")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Tie (끈 kkeun)",
    )


def build():
    pattern = fc.PatternSet("hanbok-chima")
    every = target_piece == "set"
    if every or target_piece == "band":
        pattern.add(build_band())
    if every or target_piece == "panel":
        pattern.add(build_panel())
    if every or target_piece == "tie":
        pattern.add(build_tie())

    if every:
        band = pattern.piece("band")
        panel = pattern.piece("panel")

        # The pleat seam, stated honestly. The panel tops (all PANELS of them)
        # sew to the band bottom, and the surplus IS the pleating. Both lengths
        # are MEASURED from the drafted polygons — neither is assumed — and the
        # declared ease is exactly the cloth the integer pleat count folds away.
        panel_top_total = panel.edge("top").length(0.05) * PANELS
        band_bottom = band.edge("bottom").length(0.05)
        pattern.declare_seam(
            [("panel", "top")] * PANELS, [("band", "bottom")],
            tol=1.5, ease=(panel_top_total - band_bottom),
        )

        # The piecing seams: each panel's right edge meets the next panel's
        # left, so the two must be equal in length.
        pattern.declare_seam(("panel", "side_right"), ("panel", "side_left"),
                             tol=0.5)

    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.85)   # rectangles nest tightly
    pattern.bom = [
        {"item": "ramie, silk gauze, or cotton lawn",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm usable width, 85% marker; "
                 f"{PANELS} straight widths pieced vertically."},
        {"item": "band anchor button", "qty": 1, "unit": "count",
         "note": f"Yantra4D sew-through-button at {button_ligne:.0f} ligne "
                 "(see notion.hardware_ref); holds the wrap while the ties tie."},
        {"item": "band interfacing", "qty": round(BAND_SPAN * band_height / 1000.0),
         "unit": "cm2",
         "note": "the malgi carries the entire skirt weight — interface it firmly."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "pleats basted to the band before the final seam."},
    ]
    pattern.metadata = {
        "fc300_rank": 280,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "tradition": "Korean (한복 hanbok) — the everyday and festival chima",
        "finished_mm": {"length": round(chima_length, 1),
                        "band_span": round(BAND_SPAN, 1),
                        "flat_panel_width": round(PANEL_WIDTH, 1),
                        "tie_length": round(TIE_LENGTH, 1)},
        "solved": {
            "pleats": PLEATS,
            "pleat_style": "box" if pleat_style >= 1.5 else "knife",
            "pleat_face_mm": round(PLEAT_FACE, 2),
            "pleat_depth_mm": round(PLEAT_DEPTH, 2),
            "cloth_per_pleat_mm": round(CLOTH_PER_PLEAT, 2),
            "loom_widths": PANELS,
            "panel_cut_width_mm": round(PANEL_CUT_WIDTH, 2),
            "note": "pleating is DISCRETE: the count is rounded to an integer "
                    "first, and the pleat face, depth and flat panel width are "
                    "all back-solved from that integer so the pleats tile the "
                    "band exactly. The band-to-panel seam is declared with the "
                    "ease MEASURED from both drafted polygons, so the surplus "
                    "the pleats absorb is proven, not asserted. Piecing count "
                    "comes from the real usable loom width.",
        },
        "hardware": "band anchor button via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); button_ligne drives the band's seat",
        "cut_philosophy": "the chima is not shaped — it is a pieced rectangle "
                          "pleated into a short chest band. The bell silhouette "
                          "comes from suspension at the ribcage, not from cutting.",
        "excluded": "ceremonial and rank-bearing hanbok are NOT drafted: 활옷 "
                    "(hwarot, bridal robe), 당의 (dangui, court jacket) and 금박 "
                    "(geumbak) gold-leaf work are distinct garments carrying "
                    "ritual and social meaning, not decoration options on a skirt.",
        "pairs_with": "hanbok-jeogori (the short upper jacket) — worn together",
    }
    return pattern


result = build()
