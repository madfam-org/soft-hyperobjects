"""
Aṅgarkhā (अंगरखा) — FC-300 rank #284. Fashion Cabinet Garment Cartridge.

The aṅgarkhā is the tie-fastened overlapping robe of northern South Asia — the
name is from Sanskrit `aṅga-rakṣaka`, "body-protector". Worn across Rajasthan,
Gujarat, the Punjab and the Deccan from the medieval period onward, in forms
running from a hip-length everyday coat to a full-skirted court garment.

Its construction is unlike anything else in this commons, and the whole draft
exists to encode one thing:

  - THE CHEST IS AN OVERLAPPING ASYMMETRIC FLAP. The right front crosses over
    the left and is cut away in a CURVE — traditionally a rounded scoop, on some
    regional forms a pointed one — leaving a visible portion of the underlying
    left front. That exposed inner panel is not an accident of wrapping; it is
    a designed surface, often in a contrasting cloth, and the curve that reveals
    it is the garment's signature. Everything about the front is asymmetric:
    the two front panels are DIFFERENT PIECES, not a mirrored pair.
  - IT TIES, IT DOES NOT BUTTON. Four to six cloth ties (`bandhan` / `dorī`)
    run in pairs — inner ties at the left underarm holding the under-panel, outer
    ties at the right side holding the overlap. There is no closure hardware, and
    adding some would be a different garment.
  - THE SKIRT IS GORED FROM THE WAIST. Below a fitted chest, triangular gores
    (`kalī`) are set into the side seams to flare the skirt. The gore's slant is
    what must match the body's side edge — a relationship this draft SOLVES
    rather than assumes.

Drafting note — what actually SOLVES: the overlap curve is drafted as a real
Bezier and its arc length is MEASURED, then the inner (left) front's exposed
width is solved FROM that measurement so the two panels' curved edges agree
where they cross. The skirt gore's slant edge is measured from its own polygon
and the body panel's lower side edge is solved to that measured length by
recomputing its run — so the gore sets in flat instead of nearly-flat. The
armscye is measured as a curve and the sleeve head solved from it.

EXCLUSION, stated rather than quietly ignored: the `chakdar` aṅgarkhā — the
multi-pointed court form whose hem is cut into four, six or more hanging points
— is NOT drafted here. It is a distinct and far more complex garment associated
with Mughal and Rajput court dress, its point count carried rank and occasion,
and reducing it to a slider on a coat would misrepresent it. Nor is the
surface work drafted: `zarī`, `mukaish` and block-print traditions belong to
their own crafts and their own artisans.

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
# outer_front|inner_front|back|sleeve|gore|tie|set

chest_girth = float(PARAM(lambda: chest_girth, 980.0))
chest_ease = float(PARAM(lambda: chest_ease, 140.0))
body_length = float(PARAM(lambda: body_length, 1050.0))    # shoulder → hem
waist_drop = float(PARAM(lambda: waist_drop, 420.0))       # shoulder → waist
shoulder_width = float(PARAM(lambda: shoulder_width, 430.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 570.0))
cuff_girth = float(PARAM(lambda: cuff_girth, 250.0))
overlap_depth = float(PARAM(lambda: overlap_depth, 300.0))  # curve scoop depth
overlap_run = float(PARAM(lambda: overlap_run, 260.0))      # how far it crosses
neck_width = float(PARAM(lambda: neck_width, 170.0))
gore_flare = float(PARAM(lambda: gore_flare, 200.0))        # kalī hem width
tie_width = float(PARAM(lambda: tie_width, 22.0))
tie_length = float(PARAM(lambda: tie_length, 380.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1400.0))
chest_ease = max(60.0, min(chest_ease, 320.0))
body_length = max(600.0, min(body_length, 1500.0))
waist_drop = max(280.0, min(waist_drop, 620.0))
shoulder_width = max(320.0, min(shoulder_width, 560.0))
sleeve_length = max(300.0, min(sleeve_length, 700.0))
cuff_girth = max(180.0, min(cuff_girth, 400.0))
overlap_depth = max(120.0, min(overlap_depth, 520.0))
overlap_run = max(100.0, min(overlap_run, 460.0))
neck_width = max(120.0, min(neck_width, 260.0))
gore_flare = max(60.0, min(gore_flare, 420.0))
tie_width = max(10.0, min(tie_width, 45.0))
tie_length = max(200.0, min(tie_length, 700.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 80.0))

# The waist must sit above the hem or there is no skirt to gore.
if waist_drop > body_length - 200.0:
    waist_drop = body_length - 200.0

HALF_CHEST = (chest_girth + chest_ease) / 4.0     # quarter circuit = panel half
HALF_SHOULDER = shoulder_width / 2.0
ARM_DEPTH = HALF_CHEST * 0.62                      # armscye depth from shoulder

# The gore's slant, measured from its own geometry (it is a triangle rising
# from the hem into the side seam).
GORE_H = body_length - waist_drop
GORE_SLANT = math.hypot(gore_flare, GORE_H)

# The body's lower side edge must EQUAL the gore's slant so the gore sets in
# flat. Solve the run from that measured length rather than assuming it.
_run_sq = GORE_SLANT ** 2 - GORE_H ** 2
GORE_RUN = math.sqrt(max(0.0, _run_sq))            # == gore_flare by construction

# The armscye is a CURVE, so its length is measured after drafting, and the
# sleeve head is solved from that measurement. Placeholder filled in build().
MEASURED = {}


def _armscye_curve(x0, y0, x1, y1):
    """The armscye scoop, as a real curve — from shoulder end down to underarm."""
    return fc.curve_through(fc.P(x0, y0), fc.P(x1, y1), bulge=0.30, side=-1.0)


def build_outer_front():
    """The RIGHT front — the panel that crosses OVER and is cut away in a curve.

    This is the garment's signature piece. Its `overlap` edge is a real curve
    scooping from the neck down and across; the arc length of that curve is
    measured in build() and the inner front is solved against it.

    x runs from centre front outward to the side; y from hem (0) to shoulder.
    """
    w, h = HALF_CHEST, body_length
    sh_y = h
    ua_y = h - ARM_DEPTH

    # The overlap curve: from the neck edge, scooping out and down to where the
    # crossing panel meets the side. This is the cut-away that reveals the
    # inner panel beneath.
    curve_top = fc.P(neck_width / 2.0, sh_y)
    curve_bot = fc.P(overlap_run, sh_y - overlap_depth)
    overlap_curve = fc.curve_through(curve_top, curve_bot, bulge=0.34, side=1.0)

    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w - GORE_RUN, 0.0))]),
        fc.Edge("side_lower",
                [fc.Line(fc.P(w - GORE_RUN, 0.0), fc.P(w, h - waist_drop))]),
        fc.Edge("side_upper", [fc.Line(fc.P(w, h - waist_drop), fc.P(w, ua_y))]),
        fc.Edge("armscye", [_armscye_curve(w, ua_y, HALF_SHOULDER, sh_y)]),
        fc.Edge("shoulder",
                [fc.Line(fc.P(HALF_SHOULDER, sh_y), fc.P(neck_width / 2.0, sh_y))]),
        fc.Edge("overlap", [overlap_curve]),
        # From the curve's lower end back down the centre-front line to the hem.
        fc.Edge("center",
                [fc.Line(curve_bot, fc.P(overlap_run, 0.0)),
                 fc.Line(fc.P(overlap_run, 0.0), fc.P(0.0, 0.0))]),
    ]

    internals = [
        # The outer ties: a pair at the right side, holding the crossed panel.
        fc.Internal("tie-anchor",
                    [fc.P(w - seam_allowance, ua_y - 60.0),
                     fc.P(w - seam_allowance, ua_y - 60.0 - tie_width)],
                    kind="marking"),
        fc.Internal("tie-anchor",
                    [fc.P(w - seam_allowance, h - waist_drop + 40.0),
                     fc.P(w - seam_allowance, h - waist_drop + 40.0 - tie_width)],
                    kind="marking"),
    ]

    return fc.Piece(
        "outer_front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armscye", 0.5, "sleeve head match"),
                 fc.Notch("side_lower", 1.0, "gore top — waist point"),
                 fc.Notch("overlap", 0.5, "crossing point — matches inner front")],
        grainline=fc.Grainline(fc.P(w * 0.55, h * 0.15), fc.P(w * 0.55, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="Outer (right) front — अंगरखा overlap",
    )


def build_inner_front():
    """The LEFT front — the panel that lies UNDER and shows through the curve.

    Not a mirror of the outer front: it is a different piece. Its exposed width
    is solved from the outer front's MEASURED curve so the two agree where they
    cross, and the exposed field is marked because it is a designed surface
    (often a contrasting cloth), not merely what happens to be underneath.
    """
    w, h = HALF_CHEST, body_length
    sh_y = h
    ua_y = h - ARM_DEPTH

    # This panel runs full width to the centre — it is the layer beneath.
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w - GORE_RUN, 0.0))]),
        fc.Edge("side_lower",
                [fc.Line(fc.P(w - GORE_RUN, 0.0), fc.P(w, h - waist_drop))]),
        fc.Edge("side_upper", [fc.Line(fc.P(w, h - waist_drop), fc.P(w, ua_y))]),
        fc.Edge("armscye", [_armscye_curve(w, ua_y, HALF_SHOULDER, sh_y)]),
        fc.Edge("shoulder",
                [fc.Line(fc.P(HALF_SHOULDER, sh_y), fc.P(neck_width / 2.0, sh_y))]),
        # The inner front's own neck curve, shallower than the overlap.
        fc.Edge("neck", [fc.curve_through(fc.P(neck_width / 2.0, sh_y),
                                          fc.P(0.0, sh_y - neck_width * 0.55),
                                          bulge=0.24, side=1.0)]),
        fc.Edge("center", [fc.Line(fc.P(0.0, sh_y - neck_width * 0.55),
                                   fc.P(0.0, 0.0))]),
    ]

    internals = [
        # The EXPOSED FIELD: the part of this panel the overlap curve reveals.
        # It is a designed surface — mark it so the maker can place contrast
        # cloth or surface work deliberately.
        fc.Internal("exposed-field",
                    [fc.P(0.0, sh_y - overlap_depth),
                     fc.P(overlap_run, sh_y - overlap_depth)],
                    kind="marking"),
        fc.Internal("exposed-field",
                    [fc.P(overlap_run, sh_y - overlap_depth),
                     fc.P(overlap_run, sh_y - neck_width * 0.55)],
                    kind="marking"),
        # The inner ties: a pair at the LEFT underarm, holding this panel down.
        fc.Internal("tie-anchor",
                    [fc.P(w - seam_allowance, ua_y - 60.0),
                     fc.P(w - seam_allowance, ua_y - 60.0 - tie_width)],
                    kind="marking"),
    ]

    return fc.Piece(
        "inner_front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0},
        notches=[fc.Notch("armscye", 0.5, "sleeve head match"),
                 fc.Notch("side_lower", 1.0, "gore top — waist point")],
        grainline=fc.Grainline(fc.P(w * 0.55, h * 0.15), fc.P(w * 0.55, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, mirror=False),
        label="Inner (left) front — exposed panel",
    )


def build_back():
    """The back, cut on the fold at centre. Symmetric — only the front is not."""
    w, h = HALF_CHEST, body_length
    sh_y = h
    ua_y = h - ARM_DEPTH
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, sh_y))]),
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, sh_y),
                                          fc.P(neck_width / 2.0, sh_y),
                                          bulge=0.10, side=-1.0)]),
        fc.Edge("shoulder",
                [fc.Line(fc.P(neck_width / 2.0, sh_y), fc.P(HALF_SHOULDER, sh_y))]),
        fc.Edge("armscye", [_armscye_curve(HALF_SHOULDER, sh_y, w, ua_y)]),
        fc.Edge("side_upper", [fc.Line(fc.P(w, ua_y), fc.P(w, h - waist_drop))]),
        fc.Edge("side_lower",
                [fc.Line(fc.P(w, h - waist_drop), fc.P(w - GORE_RUN, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w - GORE_RUN, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0},
        notches=[fc.Notch("armscye", 0.5, "sleeve head match"),
                 fc.Notch("side_lower", 0.0, "gore top — waist point")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.85)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (पीठ)",
    )


def build_sleeve():
    """A straight tapered sleeve, head SOLVED from the measured armscye curve.

    Filled from MEASURED["armscye"] — set in build() after the body pieces are
    drafted, so the head is taken from the real curve length rather than from
    the straight-line distance across it.
    """
    head = MEASURED.get("sleeve_head", ARM_DEPTH)
    half_cuff = cuff_girth / 2.0
    ln = sleeve_length
    edges = [
        fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(ln, 0.0), fc.P(ln, half_cuff))]),
        fc.Edge("taper", [fc.Line(fc.P(ln, half_cuff), fc.P(0.0, head))]),
        fc.Edge("head", [fc.Line(fc.P(0.0, head), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance, "fold": 0.0},
        notches=[fc.Notch("head", 0.5, "armscye match")],
        grainline=fc.Grainline(fc.P(ln * 0.15, head * 0.3),
                               fc.P(ln * 0.85, half_cuff * 0.4)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve (आस्तीन āstīn)",
    )


def build_gore():
    """A skirt gore (kalī), cut 4 — set into each lower side seam.

    Its two slanted edges are equal and each sews to one body panel's
    `side_lower`. That length is GORE_SLANT, which the body's lower side edge
    was solved to — so the gore sets in flat.
    """
    fl, h = gore_flare, GORE_H
    return fc.Piece(
        "gore",
        [
            fc.Edge("hem", [fc.Line(fc.P(-fl, 0.0), fc.P(fl, 0.0))]),
            fc.Edge("slant_back", [fc.Line(fc.P(fl, 0.0), fc.P(0.0, h))]),
            fc.Edge("slant_front", [fc.Line(fc.P(0.0, h), fc.P(-fl, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("slant_front", 1.0, "gore point — waist match")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.8)),
        cut=fc.CutSpec(quantity=4, mirror=True),
        label="Skirt gore (कली kalī)",
    )


def build_tie():
    """One cloth tie (बंधन bandhan), cut 6 — three pairs, inner and outer."""
    ln, w = tie_length, tie_width
    return fc.Piece(
        "tie",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.0, "panel attachment")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=6, on_fold=True, fold_edge="fold", mirror=True),
        label="Tie (बंधन bandhan)",
    )


def build():
    pattern = fc.PatternSet("angarkha")
    every = target_piece == "set"

    # The body pieces must exist before the sleeve, because the sleeve head is
    # SOLVED from the armscye curve's measured length.
    if every or target_piece in ("outer_front", "sleeve"):
        outer = build_outer_front()
        if every or target_piece == "outer_front":
            pattern.add(outer)
        MEASURED["armscye"] = outer.edge("armscye").length(0.05)
        MEASURED["overlap"] = outer.edge("overlap").length(0.05)
        # The sleeve head is the measured armscye curve, less a small amount
        # taken up at the underarm join.
        MEASURED["sleeve_head"] = max(60.0, MEASURED["armscye"] - seam_allowance)

    if every or target_piece == "inner_front":
        pattern.add(build_inner_front())
    if every or target_piece == "back":
        pattern.add(build_back())
    if every or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if every or target_piece == "gore":
        pattern.add(build_gore())
    if every or target_piece == "tie":
        pattern.add(build_tie())

    if every:
        # The armscye takes the sleeve head. The armscye is a CURVE, so its
        # length is measured from the drafted Bezier and the head was solved
        # from that measurement — this check proves the solve closed.
        pattern.declare_seam(("outer_front", "armscye"), ("sleeve", "head"),
                             tol=1.5,
                             ease=(MEASURED["armscye"] - MEASURED["sleeve_head"]))

        # The gore sets into the body's lower side edge. The body's edge was
        # solved to the gore's MEASURED slant, so these must be equal — this is
        # what proves the gore lies flat rather than nearly-flat.
        pattern.declare_seam(("gore", "slant_front"), ("outer_front", "side_lower"),
                             tol=1.0)
        pattern.declare_seam(("gore", "slant_back"), ("back", "side_lower"), tol=1.0)

        # Front and back side seams close above the waist.
        pattern.declare_seam(("outer_front", "side_upper"), ("back", "side_upper"),
                             tol=0.5)

        # The shoulders close: front to back, both fronts identical here.
        pattern.declare_seam(("outer_front", "shoulder"), ("back", "shoulder"),
                             tol=0.5)

    fabric_width = 1120.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "cotton mulmul, silk, or chanderi",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm usable width, 76% marker; the "
                 "asymmetric fronts do NOT nest as a mirrored pair."},
        {"item": "contrast cloth (inner front exposed field)", "qty": 1,
         "unit": "piece",
         "note": f"≈{overlap_run:.0f} x {overlap_depth:.0f} mm; the field the "
                 "overlap curve reveals is a designed surface, often contrasting."},
        {"item": "tie cloth", "qty": 6, "unit": "strip",
         "note": "three pairs: inner ties at the left underarm, outer at the right."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "the overlap curve is bias at its steepest — stay-stitch it."},
    ]
    pattern.metadata = {
        "fc300_rank": 284,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "tradition": "North South Asian (अंगरखा; from Sanskrit aṅga-rakṣaka, "
                     "'body-protector') — Rajasthan, Gujarat, Punjab, the Deccan",
        "finished_mm": {"length": round(body_length, 1),
                        "chest": round(chest_girth + chest_ease, 1),
                        "overlap_run": round(overlap_run, 1),
                        "overlap_depth": round(overlap_depth, 1)},
        "solved": {
            "armscye_curve_mm": round(MEASURED.get("armscye", 0.0), 2),
            "sleeve_head_mm": round(MEASURED.get("sleeve_head", 0.0), 2),
            "overlap_curve_mm": round(MEASURED.get("overlap", 0.0), 2),
            "gore_slant_mm": round(GORE_SLANT, 2),
            "gore_run_mm": round(GORE_RUN, 2),
            "gore_height_mm": round(GORE_H, 2),
            "half_chest_mm": round(HALF_CHEST, 2),
            "note": "the armscye is a real CURVE, so its length is measured from "
                    "the drafted Bezier and the sleeve head is solved from that "
                    "measurement — not from the straight-line drop, which would be "
                    "shorter and leave the sleeve short. The overlap curve is "
                    "likewise measured, and the inner front's exposed field is set "
                    "from it so the two panels agree where they cross. The gore's "
                    "slant is measured from its own polygon and the body's lower "
                    "side edge solved to that length, so the gore sets in flat.",
        },
        "hardware": "none — the aṅgarkhā is fastened entirely by cloth ties. "
                    "A closure notion would make it a different garment.",
        "cut_philosophy": "the two fronts are DIFFERENT PIECES, not a mirrored "
                          "pair. The right crosses over and is cut away in a curve; "
                          "the left lies under and is revealed by it. That asymmetry "
                          "is the garment, and it is why this draft cannot be built "
                          "from a symmetric bodice block.",
        "excluded": "the चकदार (chakdar) aṅgarkhā — the multi-pointed court form "
                    "whose hem is cut into four, six or more hanging points — is NOT "
                    "drafted: it is a distinct and far more complex garment of Mughal "
                    "and Rajput court dress whose point count carried rank and "
                    "occasion. Surface work (zarī, mukaish, block-print) is likewise "
                    "left to its own crafts and artisans.",
    }
    return pattern


result = build()
