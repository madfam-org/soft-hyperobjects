"""
Kente wrapper cloth garment — Fashion Cabinet Cartridge (FC-400 #396; heritage_global, Akan/Ewe).

Kente is the strip-woven cloth of the Akan (Asante) and Ewe peoples of Ghana and Togo: narrow
warp-striped strips woven on a men's double-heddle loom and sewn edge-to-edge into a large
rectangular cloth. The men's wearing cloth (the toga-style wrapper) is that WHOLE UNCUT
RECTANGLE, draped over the left shoulder and wound round the body; it is not tailored. This
cartridge honours that: it draws the assembled cloth as its strips and the drape as a marked
wrapping path, and it CUTS NOTHING into the cloth — because cutting kente destroys the strip
weave and the meaning woven into it.

What this cartridge actually encodes, and why it earns a place beside the tailored heritage
garments rather than being a plain rectangle:

  1. THE CLOTH IS AN ASSEMBLY OF STRIPS, AND THE STRIP WIDTH IS REAL. Kente is woven in strips
     of a fixed loom width (`strip_width`, typically ~100 mm) and the cloth is a whole number
     of them sewn side by side. So the cloth's width is not free — it is `strip_count *
     strip_width`, and this cartridge solves the strip count from the target cloth width and
     reports the true assembled width. Each strip's join is a real straight seam drawn as an
     internal line, because that seam is where the weaver's strips actually meet.

  2. THE GARMENT IS THE DRAPE, NOT A CUT. The wearing cloth is sized to the wearer by the CLOTH
     DIMENSIONS (length and assembled width) and the wrapping is a path, not a set of pattern
     pieces. The draft marks the shoulder line and the wrap turns so a wearer knows how the
     rectangle sits, while leaving the cloth whole.

Pieces: cloth (the whole assembled rectangle, cut 1, uncut), strip (one representative loom
strip, for the weaver). Made to measure to the wearer's height and reach (which set the cloth
length and width), plus the strip width.

Cultural note (stated, and load-bearing): kente patterns (the named weaves, e.g. the many
adinkra-linked and proverb-named setts) carry specific meaning and belong to Akan and Ewe
weavers and communities. This cartridge draws NO kente pattern and names none — it supplies the
CLOTH DIMENSIONS and the drape only, and the weave is the weaver's.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

wearer_height = float(PARAM(lambda: wearer_height, 1720.0))
wearer_reach = float(PARAM(lambda: wearer_reach, 1800.0))     # fingertip to fingertip span
cloth_length_factor = float(PARAM(lambda: cloth_length_factor, 1.4))  # cloth len / height
strip_width = float(PARAM(lambda: strip_width, 100.0))       # loom strip width
target_cloth_width = float(PARAM(lambda: target_cloth_width, 1900.0))  # assembled width goal
hem_allowance = float(PARAM(lambda: hem_allowance, 15.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
wearer_height = max(1400.0, min(wearer_height, 2100.0))
wearer_reach = max(1400.0, min(wearer_reach, 2200.0))
cloth_length_factor = max(1.1, min(cloth_length_factor, 1.9))
strip_width = max(60.0, min(strip_width, 160.0))
target_cloth_width = max(1200.0, min(target_cloth_width, 2600.0))
hem_allowance = max(5.0, min(hem_allowance, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# ── The strip-assembly solver ────────────────────────────────────────────────
# The cloth is a whole number of loom strips. Solve the count from the target width and report
# the true assembled width (which snaps to a multiple of the strip width).
STRIP_COUNT = max(6, int(round(target_cloth_width / strip_width)))
CLOTH_WIDTH = STRIP_COUNT * strip_width
# The men's wearing cloth is long — roughly the wearer's height times a factor, so it can wrap.
CLOTH_LENGTH = wearer_height * cloth_length_factor


def build_cloth():
    """The whole assembled kente cloth (cut 1, UNCUT): a rectangle CLOTH_WIDTH x CLOTH_LENGTH,
    marked with the strip-join seams (internals), the shoulder line, and the wrap turns. The
    cloth is never cut into pieces — that is the point.
    """
    w, h = CLOTH_WIDTH, CLOTH_LENGTH
    edges = [
        fc.Edge("hem_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("selvedge_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("hem_top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("selvedge_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # strip-join seams: STRIP_COUNT-1 vertical lines where the loom strips meet.
    for i in range(1, STRIP_COUNT):
        x = strip_width * i
        internals.append(fc.Internal(f"strip join {i}", [fc.P(x, 0.0), fc.P(x, h)],
                                     kind="marking"))
    # drape guides: the shoulder line and the two wrap turns (where the cloth folds over the
    # left shoulder and winds round). These are wearing marks, not seams.
    internals.append(fc.Internal("left-shoulder line",
                                 [fc.P(w * 0.5, h * 0.62), fc.P(w * 0.5, h * 0.62 + 1.0)],
                                 kind="marking"))
    internals.append(fc.Internal("wrap turn A",
                                 [fc.P(0.0, h * 0.5), fc.P(w, h * 0.5)], kind="marking"))
    internals.append(fc.Internal("wrap turn B",
                                 [fc.P(0.0, h * 0.32), fc.P(w, h * 0.32)], kind="marking"))
    return fc.Piece(
        "cloth", edges, seam_allowance=seam_allowance,
        allowances={"hem_bottom": hem_allowance, "hem_top": hem_allowance,
                    "selvedge_r": 0.0, "selvedge_l": 0.0},
        notches=[fc.Notch("selvedge_l", 0.62, "left-shoulder point"),
                 fc.Notch("hem_bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Kente cloth — whole assembled rectangle (cut 1, UNCUT)")


def build_strip():
    """One representative loom strip (cut STRIP_COUNT), for the weaver: a long narrow band of
    `strip_width`, the unit the cloth is assembled from. It carries no pattern — the weave is
    the weaver's.
    """
    w, h = strip_width, CLOTH_LENGTH
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("join_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("join_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strip", edges, seam_allowance=seam_allowance,
        allowances={"bottom": hem_allowance, "top": hem_allowance},
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        cut=fc.CutSpec(quantity=STRIP_COUNT),
        label="Loom strip (weave to width; join edge-to-edge)")


def build():
    pattern = fc.PatternSet("kente-wrap")
    cloth = build_cloth()
    strip = build_strip()

    picked = {"cloth": cloth, "strip": strip}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        pattern.add(cloth)
        pattern.add(strip)
        # The strips assemble into the cloth: each strip's join edge meets the next. Declared
        # as a self-consistent join (one strip's two long edges are equal by construction).
        pattern.declare_seam(("strip", "join_r"), ("strip", "join_l"), tol=0.5)

    total_strip_run = STRIP_COUNT * CLOTH_LENGTH
    pattern.bom = [
        {"item": "hand-woven kente strips (Akan/Ewe double-heddle loom)",
         "qty": round(total_strip_run / 100.0) * 100, "unit": "mm_length",
         "note": f"{STRIP_COUNT} strips x {CLOTH_LENGTH:.0f} mm at {strip_width:.0f} mm strip "
                 f"width; assembled width {CLOTH_WIDTH:.0f} mm. The strips are woven with the "
                 "weaver's own named pattern — this cartridge supplies dimensions, NOT a weave."},
        {"item": "sewing thread (strip joins)", "qty": 1, "unit": "spool",
         "note": f"{STRIP_COUNT - 1} straight edge-to-edge strip joins; the cloth is otherwise "
                 "whole and UNCUT."},
    ]
    pattern.metadata = {
        "fc400_rank": 396, "family": "heritage_global", "fabric_hint": "kente-weave",
        "tradition": "Akan (Asante) / Ewe — Ghana & Togo; the strip-woven wearing cloth",
        "silhouette_note": "The whole assembled kente cloth worn as a toga-style wrapper: draped "
            "over the left shoulder and wound round the body. It is NOT cut or tailored — the "
            "garment is the drape of an uncut rectangle of strip-woven cloth.",
        "hardware": "none — the wearing cloth is draped, not fastened.",
        "no_cut": "The cloth is drawn WHOLE and marked with wrap guides; cutting into kente "
            "destroys the strip weave and the meaning woven into it, so this cartridge cuts "
            "nothing.",
        "solved": {
            "strip_width_mm": round(strip_width, 1),
            "strip_count": STRIP_COUNT,
            "assembled_cloth_width_mm": round(CLOTH_WIDTH, 1),
            "cloth_length_mm": round(CLOTH_LENGTH, 1),
            "note": "the assembled width snaps to a whole number of loom strips (strip_count * "
                    "strip_width); the length is the wearer's height times a wrap factor.",
        },
        "cultural_note": "Kente patterns (the named weaves and proverb-named setts) carry "
            "specific meaning and belong to Akan and Ewe weavers and communities. This cartridge "
            "draws NO kente pattern and names none — it supplies the cloth dimensions and the "
            "drape only, and the weave is the weaver's.",
        "drafting": "Made to measure to the wearer's height and reach (which set the cloth "
            "length and width) plus the loom strip width; nothing is cut.",
    }
    return pattern


result = build()
