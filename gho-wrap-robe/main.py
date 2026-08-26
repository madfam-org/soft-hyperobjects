"""
Gho wrap robe (བགོ་) — Fashion Cabinet Heritage Cartridge (FC-500 #500, heritage_global;
Bhutan).

The gho is the national dress of Bhutanese men: a knee-length wrapped robe, put on long,
crossed right-over-left across the body, and then HITCHED UP and belted at the waist with the
woven kera belt so the hem sits at the knee and the excess blouses over the belt to form the
gho's characteristic front pouch (the traditional "pocket"). It has wide sleeves with white
folded-back cuffs (the liṅgto), a low round-and-crossed neckline, and it is worn over a
turned-cuff undershirt with knee socks, and with the ceremonial kabney scarf on formal
occasions. It is woven in checked or striped Bhutanese cloth (the finest a kushuthara or
mathra).

The gho is the 500th ratified garment of the Fashion Cabinet — the last of the first half of
one thousand — and it is drafted here in the same plain, honest way as the first: a real
pattern for a real garment, with the weaving left to the weaver.

Two facts govern the draft, and both come from HOW THE GHO IS WORN:

  1. IT IS CUT LONG AND WORN HITCHED. The robe is drafted to the FULL length (ankle), because
     it is worn pulled up to the knee and belted — the difference between the cut length and the
     worn length is the blouse that forms the pouch. So the draft takes the wearer's height for
     the cut length and the knee height for the worn length, and reports the pouch blouse that
     results. Draft it to the worn length and there is no pouch, which is the whole silhouette.

  2. THE FRONT CROSSES, AND THE OVERLAP IS REAL. The right front crosses well past centre front
     (a deep wrap, held by the belt), so each front is drafted with a real overlap, and the two
     fronts always meet with a genuine cross rather than gaping.

Pieces:
  - front  : one front (cut 2), with the deep centre-front overlap.
  - back   : the back (cut on fold), one-piece wide sleeve.
  - sleeve : the wide sleeve extension with the folded-back cuff (liṅgto), cut 2.
  - collar : the low neckband, cut to the MEASURED neckline.

Hardware: none — the gho is closed entirely by the kera belt; there is no button or hook.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1020.0))
wearer_height = float(PARAM(lambda: wearer_height, 1720.0))
knee_height = float(PARAM(lambda: knee_height, 500.0))    # floor to knee (sets the worn hem)
cut_length = float(PARAM(lambda: cut_length, 1180.0))     # nape to cut hem (worn hitched)
neck_girth = float(PARAM(lambda: neck_girth, 410.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 470.0))
sleeve_reach = float(PARAM(lambda: sleeve_reach, 300.0))  # wide sleeve past the body
sleeve_depth = float(PARAM(lambda: sleeve_depth, 300.0))
cuff_fold = float(PARAM(lambda: cuff_fold, 120.0))        # the folded-back white cuff depth
front_overlap = float(PARAM(lambda: front_overlap, 260.0))  # deep wrap
collar_height = float(PARAM(lambda: collar_height, 28.0))
ease = float(PARAM(lambda: ease, 180.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(840.0, min(chest_girth, 1300.0))
wearer_height = max(1500.0, min(wearer_height, 1950.0))
knee_height = max(420.0, min(knee_height, 600.0))
cut_length = max(1000.0, min(cut_length, 1400.0))
neck_girth = max(360.0, min(neck_girth, 480.0))
shoulder_width = max(400.0, min(shoulder_width, 540.0))
sleeve_reach = max(180.0, min(sleeve_reach, 460.0))
sleeve_depth = max(240.0, min(sleeve_depth, 380.0))
cuff_fold = max(60.0, min(cuff_fold, 200.0))
front_overlap = max(140.0, min(front_overlap, 400.0))
collar_height = max(18.0, min(collar_height, 45.0))
ease = max(120.0, min(ease, 320.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))
hem_allowance = max(15.0, min(hem_allowance, 60.0))

# ── The hitch solve — cut long, worn to the knee ─────────────────────────────
# The gho is worn pulled up so the hem sits at the knee. The worn length (nape to knee) is the
# wearer's height minus the head/neck and minus the floor-to-knee. The pouch blouse is the cut
# length minus the worn length — that excess is what forms the front pocket over the belt.
NAPE_HEIGHT = wearer_height - 260.0              # roughly nape height above the floor
WORN_LENGTH = max(NAPE_HEIGHT - knee_height, 300.0)  # nape to knee, the hem as worn
POUCH_BLOUSE = max(cut_length - WORN_LENGTH, 0.0)  # the excess that forms the pouch
CHEST_Q = (chest_girth + ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_HALF = min((neck_girth + 26.0) / 4.0, HALF_SHOULDER - 30.0)
FRONT_NECK_DROP = NECK_HALF * 0.9 + 16.0
BACK_NECK_DROP = 24.0
SHOULDER_Y = cut_length
UNDERARM_Y = cut_length - sleeve_depth


def build_front():
    """One front (cut 2): the body quarter plus the deep centre-front overlap; one-piece wide
    sleeve run out at the shoulder. x = 0 is the crossing edge; x = CHEST_Q + overlap is the
    side."""
    overlap = front_overlap
    x_side = CHEST_Q + overlap
    x_neck = overlap + NECK_HALF
    p_hem_cross = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, UNDERARM_Y)
    p_sleeve_end = fc.P(x_side + sleeve_reach, UNDERARM_Y + sleeve_depth * 0.35)
    p_sleeve_top = fc.P(x_side + sleeve_reach, SHOULDER_Y)
    p_neck_shoulder = fc.P(x_neck, SHOULDER_Y)
    p_neck_cross = fc.P(0.0, SHOULDER_Y - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cross, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end, p_sleeve_top)]),
        fc.Edge("shoulder", [fc.Line(p_sleeve_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(x_neck * 0.65, SHOULDER_Y - 6.0),
                                   fc.P((x_neck) * 0.3, p_neck_cross.y + 10.0),
                                   p_neck_cross)]),
        fc.Edge("cross_edge", [fc.Line(p_neck_cross, p_hem_cross)]),
    ]
    internals = [
        fc.Internal("centre-front", [fc.P(overlap, SHOULDER_Y - FRONT_NECK_DROP),
                                     fc.P(overlap, 30.0)], kind="marking"),
        # the belt line and the hem-as-worn (at the knee), so the maker can see the pouch.
        fc.Internal("belt-line", [fc.P(0.0, POUCH_BLOUSE), fc.P(x_side, POUCH_BLOUSE)],
                    kind="marking"),
        fc.Internal("worn-hem", [fc.P(0.0, 30.0), fc.P(x_side, 30.0)], kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", POUCH_BLOUSE / max(UNDERARM_Y, 1.0), "belt line")],
        grainline=fc.Grainline(fc.P(x_side * 0.5, hem_allowance + 30.0),
                               fc.P(x_side * 0.5, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (deep centre-front overlap, one-piece sleeve)",
    )


def build_back():
    top = SHOULDER_Y
    x_side = CHEST_Q
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(x_side, 0.0)
    p_underarm = fc.P(x_side, UNDERARM_Y)
    p_sleeve_end = fc.P(x_side + sleeve_reach, UNDERARM_Y + sleeve_depth * 0.35)
    p_sleeve_top = fc.P(x_side + sleeve_reach, top)
    p_neck_shoulder = fc.P(NECK_HALF, top)
    p_neck_cb = fc.P(0.0, top - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end, p_sleeve_top)]),
        fc.Edge("shoulder", [fc.Line(p_sleeve_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, top - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("belt-line", [fc.P(0.0, POUCH_BLOUSE), fc.P(x_side, POUCH_BLOUSE)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", POUCH_BLOUSE / max(UNDERARM_Y, 1.0), "belt line")],
        grainline=fc.Grainline(fc.P(x_side * 0.3, hem_allowance + 30.0),
                               fc.P(x_side * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back (one-piece sleeve), cut on fold",
    )


def build_sleeve():
    """The wide sleeve cuff extension with the folded-back white cuff (liṅgto): a rectangle the
    sleeve mouth wide, cut_fold deep for the turn-back, cut 2."""
    w = sleeve_depth + sleeve_reach * 0.4        # the sleeve mouth width (wide)
    h = cuff_fold * 2.0 + 20.0                   # doubled for the fold-back
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("wrist", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("sleeve_join", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"wrist": 0.0},
        notches=[fc.Notch("wrist", 0.5, "cuff centre")],
        grainline=fc.Grainline(fc.P(w * 0.1, h * 0.5), fc.P(w * 0.9, h * 0.5)),
        internals=[fc.Internal("fold-back", [fc.P(0.0, cuff_fold + 10.0),
                                             fc.P(w, cuff_fold + 10.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Folded-back white cuff (liṅgto)",
    )


# ── The neckband, cut to the MEASURED neckline ───────────────────────────────
_FRONT = build_front()
_BACK = build_back()
FRONT_NECK = _FRONT.edge("neck").length(0.2)
BACK_NECK = _BACK.edge("neck").length(0.2)
NECK_RUN = 2.0 * FRONT_NECK + 2.0 * BACK_NECK
NECK_NAIVE = neck_girth + 26.0


def build_collar():
    ln = NECK_RUN
    h = collar_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", FRONT_NECK / ln, "left shoulder"),
                 fc.Notch("neck_edge", (FRONT_NECK + BACK_NECK) / ln, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Low neckband (cut to the measured neckline)",
    )


def build():
    pattern = fc.PatternSet("gho-wrap-robe")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(_FRONT)
    if everything or target_piece == "back":
        pattern.add(_BACK)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The side seam and one-piece sleeve underseam match front to back (both a body quarter
        # + the same sleeve reach — the front's extra overlap is at centre front, not the side).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "cuff"), ("back", "cuff"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # THE neckband against the MEASURED neckline (both fronts with overlaps + both backs).
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "Bhutanese checked or striped cloth (mathra / kushuthara)", "qty": round(
            (cut_length + hem_allowance) * 2.6 / 10.0) * 10, "unit": "mm_length",
         "note": "the gho is cut LONG (to the ankle) and worn hitched to the knee; the finest "
                 "are hand-woven kushuthara. The weave is the weaver's; none is drafted."},
        {"item": "white cuff cloth (liṅgto)", "qty": round((sleeve_depth + sleeve_reach) * 2),
         "unit": "mm_length", "note": "the folded-back white cuffs at the wrists."},
        {"item": "kera belt", "qty": 1, "unit": "length",
         "note": "the woven belt is the ONLY closure — the gho has no button or hook; the belt "
                 "hitches the robe to the knee and holds the pouch."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 500,
        "family": "heritage_global",
        "fabric_hint": "algodon-tejido",
        "finished_mm": {
            "chest_girth": round(chest_girth, 1),
            "cut_length": round(cut_length, 1),
            "worn_length": round(WORN_LENGTH, 1),
            "front_overlap": round(front_overlap, 1),
        },
        "solved": {
            "chest_quarter_mm": round(CHEST_Q, 2),
            "nape_height_mm": round(NAPE_HEIGHT, 2),
            "worn_length_mm": round(WORN_LENGTH, 2),
            "pouch_blouse_mm": round(POUCH_BLOUSE, 2),
            "front_overlap_mm": round(front_overlap, 2),
            "front_neck_quarter_mm": round(FRONT_NECK, 3),
            "back_neck_quarter_mm": round(BACK_NECK, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "collar_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "note": "the gho is cut LONG and worn HITCHED to the knee, belted with the kera: "
                    "the pouch_blouse (cut length minus worn length) is the excess that blouses "
                    "over the belt to form the gho's front pocket — draft it to the worn length "
                    "and there is no pouch, which is the whole silhouette. The front CROSSES "
                    "deep (a real overlap), held by the belt. The low neckband is cut to the "
                    "MEASURED neckline. There is no button or hook — the belt is the closure.",
        },
        "heritage": {
            "garment": "གོ་ gho — the national dress of Bhutanese men",
            "worn": "put on long, crossed right-over-left, hitched up and belted at the waist "
                    "with the kera so the hem sits at the knee and the excess forms the front "
                    "pouch; with white folded-back cuffs (liṅgto), knee socks, and the kabney "
                    "scarf on formal occasions",
            "construction": "a wrapped robe cut to the ankle and worn to the knee, deep "
                            "centre-front cross, one-piece wide sleeves with folded-back cuffs, "
                            "a low neckband; closed only by the belt",
            "excluded": "no specific kushuthara or mathra weave, and no dzong or dratshang "
                        "dress code, is drawn — the cloth is the weaver's and the wearing is "
                        "the wearer's",
        },
        "hardware": "none — the gho is closed entirely by the kera belt.",
        "milestone": "the 500th ratified garment of the Fashion Cabinet — the last of the "
                     "first half of one thousand, drafted 2026-08-26.",
    }
    return pattern


result = build()
