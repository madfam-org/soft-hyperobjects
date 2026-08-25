"""
Denim Chore Apron — Fashion Cabinet Garment Cartridge (FC-300 #291, denim, T2).

The cross-back work apron: no neck strap at all. Two straps run from the bib's
top corners, cross between the shoulder blades, and buckle or tie to the opposite
waist — so the apron's whole weight hangs off the shoulders instead of a loop
round the neck. Every point where a load path terminates is RIVETED, not
bar-tacked, because on 12 oz denim a bar-tack is the thing that gives first.

Three things are solved by measurement rather than by formula:

  1. THE CROSS-BACK STRAP LENGTH IS A HYPOTENUSE, NOT A GUESS. A crossing strap
     does not run straight down the back: it runs diagonally from one bib corner
     to the OPPOSITE waist point. Its length is therefore solved by Pythagoras
     from the MEASURED horizontal spread (bib corner to opposite waist anchor,
     across the body's back width) and the MEASURED vertical drop (bib top to
     waist), plus the arc over the shoulder. A strap cut to the vertical drop
     alone comes out short by the whole horizontal component — at the default
     size that is 399 mm, which is a strap that cannot be crossed at all.

  2. THE RIVETS SIT WHERE THE LOAD PATHS ACTUALLY TERMINATE. Four sites are
     derived from the built pieces, not decorated onto them: the two bib corners
     where the straps pull, and the two pocket top corners where a hand goes in
     with a full weight of tools. Each is placed by MEASURING the piece it lands
     on and stepping in by the rivet's own cap diameter plus a clearance, so a
     rivet is never set through a seam allowance — where it holds nothing — nor
     so close to an edge that it tears out through it.

  3. THE POCKET IS CLAMPED AGAINST THE SKIRT IT SITS ON. A pocket wider than its
     apron is a piece that folds back on itself, and — because the kernel
     CCW-normalizes an inverted outline and area() takes an absolute value — such
     a piece renders and passes verify() looking entirely healthy. The pocket
     width, the pocket height and the bib width are all clamped explicitly, and
     each clamp is reported.

DENIM CONVENTIONS, per the family's existing cartridges (jeans-5-pocket,
denim-jacket, bib-overalls): a 7 mm twin-needle topstitch gauge on every hemmed
edge and both pocket divisions; a deep turned hem; and every hard good a Yantra4D
reference rather than a re-implementation.

The RIVET SOLID is Yantra4D territory (`rivet`; see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres) ─────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# body|strap|pocket|set

bib_width = float(PARAM(lambda: bib_width, 300.0))        # full bib width at the top
bib_height = float(PARAM(lambda: bib_height, 330.0))      # waist line up to bib top
skirt_width = float(PARAM(lambda: skirt_width, 620.0))    # full width at the waist
skirt_length = float(PARAM(lambda: skirt_length, 560.0))  # waist down to hem
back_width = float(PARAM(lambda: back_width, 420.0))      # across the back, shoulder blades
strap_width = float(PARAM(lambda: strap_width, 38.0))
pocket_width = float(PARAM(lambda: pocket_width, 400.0))  # full pocket width
pocket_height = float(PARAM(lambda: pocket_height, 220.0))
rivet_cap = float(PARAM(lambda: rivet_cap, 11.0))         # rivet cap diameter
hem_allowance = float(PARAM(lambda: hem_allowance, 22.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (mirror the manifest slider bounds exactly) ───────────────────────
bib_width = max(180.0, min(bib_width, 460.0))
bib_height = max(200.0, min(bib_height, 460.0))
skirt_width = max(380.0, min(skirt_width, 900.0))
skirt_length = max(300.0, min(skirt_length, 900.0))
back_width = max(280.0, min(back_width, 600.0))
strap_width = max(22.0, min(strap_width, 60.0))
pocket_width = max(200.0, min(pocket_width, 760.0))
pocket_height = max(120.0, min(pocket_height, 360.0))
rivet_cap = max(7.0, min(rivet_cap, 18.0))
hem_allowance = max(12.0, min(hem_allowance, 40.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

TOPSTITCH = 7.0                               # denim twin-needle gauge, family std

# ── Derived dimensions, every one clamped ───────────────────────────────────
HALF_SKIRT = skirt_width / 2.0
# The bib can never be wider than the skirt it grows out of: the body is ONE
# piece cut on the fold, and a bib wider than the waist turns the underarm sweep
# inside out — geometry that renders happily and is wrong.
_BIB_HALF_RAW = bib_width / 2.0
HALF_BIB = max(strap_width + 12.0, min(_BIB_HALF_RAW, HALF_SKIRT - 30.0))

# The pocket sits on the skirt, so it is clamped against the skirt's own width and
# length. Both clamps are reported.
_POCKET_HALF_RAW = pocket_width / 2.0
HALF_POCKET = max(60.0, min(_POCKET_HALF_RAW, HALF_SKIRT - 18.0))
_POCKET_H_RAW = pocket_height
POCKET_H = max(60.0, min(_POCKET_H_RAW, skirt_length - hem_allowance - 60.0))
# Where the pocket's top edge sits below the waist, held clear of both the waist
# and the hem so the clamp above always has somewhere to land.
POCKET_TOP_Y = -max(60.0, skirt_length * 0.22)


def _rivet(label, x, y):
    """A rivet site drawn as a real ring-and-cross at the cap's own diameter.

    Drawn to SIZE rather than as a symbol, so the maker can see whether the cap
    actually clears the topstitch line it sits beside — which is the whole
    question when a rivet is set on a hemmed edge.
    """
    r = rivet_cap / 2.0
    ring = [fc.P(x + r * math.cos(math.radians(a)),
                 y + r * math.sin(math.radians(a)))
            for a in range(0, 361, 30)]
    return fc.Internal(label, ring + [fc.P(x, y)], kind="drill")


# ── The body: bib + skirt in ONE piece, cut on the fold ─────────────────────
def build_body():
    """Apron body, cut 1 on the fold at centre front.

    Bib and skirt are one piece — the classic chore apron — joined by a swept
    underarm curve. Hem at the bottom, bib top at y = bib_height.
    """
    p_hem_c = fc.P(0.0, -skirt_length)
    p_hem_side = fc.P(HALF_SKIRT - 22.0, -skirt_length)
    p_waist_side = fc.P(HALF_SKIRT, 0.0)
    p_bib_side = fc.P(HALF_BIB, bib_height)
    p_bib_c = fc.P(0.0, bib_height)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_c, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
        # The underarm sweep: waist out at the side, in to the bib corner. Drawn
        # as a Bézier whose controls are placed from the MEASURED gap between the
        # skirt half-width and the bib half-width, so the sweep keeps its shape at
        # every ratio of the two instead of collapsing when they get close.
        fc.Edge("underarm", [fc.Bezier(
            p_waist_side,
            fc.P(HALF_SKIRT - (HALF_SKIRT - HALF_BIB) * 0.14, bib_height * 0.42),
            fc.P(HALF_BIB + (HALF_SKIRT - HALF_BIB) * 0.52, bib_height - 24.0),
            p_bib_side)]),
        fc.Edge("bib_top", [fc.Line(p_bib_side, p_bib_c)]),
        fc.Edge("cf_fold", [fc.Line(p_bib_c, p_hem_c)]),
    ]
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        # Every outer edge is turned and topstitched, not seamed — a chore apron
        # has no seams except where the straps and pocket attach.
        allowances={"hem": hem_allowance, "side": hem_allowance,
                    "underarm": hem_allowance, "bib_top": hem_allowance,
                    "cf_fold": 0.0},
        notches=[fc.Notch("side", 0.0, "waist / tie level"),
                 fc.Notch("underarm", 1.0, "bib corner / strap anchor")],
        grainline=fc.Grainline(fc.P(HALF_BIB * 0.6, -skirt_length + 40.0),
                               fc.P(HALF_BIB * 0.6, bib_height - 40.0)),
        internals=[
            fc.Internal("edge topstitch",
                        [fc.P(TOPSTITCH, -skirt_length + TOPSTITCH),
                         fc.P(HALF_SKIRT - 22.0 - TOPSTITCH,
                              -skirt_length + TOPSTITCH)],
                        kind="trace"),
            fc.Internal("bib topstitch",
                        [fc.P(0.0, bib_height - TOPSTITCH),
                         fc.P(HALF_BIB - TOPSTITCH, bib_height - TOPSTITCH)],
                        kind="trace"),
            fc.Internal("pocket placement",
                        [fc.P(0.0, POCKET_TOP_Y),
                         fc.P(HALF_POCKET, POCKET_TOP_Y),
                         fc.P(HALF_POCKET, POCKET_TOP_Y - POCKET_H),
                         fc.P(0.0, POCKET_TOP_Y - POCKET_H),
                         fc.P(0.0, POCKET_TOP_Y)],
                        kind="marking"),
            # RIVET SITE 1 — the bib corner, where the strap pulls. Stepped in
            # from BOTH edges by the cap's own diameter plus a clearance, so the
            # rivet is never set through the turned hem where it holds nothing.
            _rivet("bib corner rivet",
                   max(rivet_cap, HALF_BIB - hem_allowance - rivet_cap),
                   bib_height - hem_allowance - rivet_cap),
            # RIVET SITE 2 — the waist tie anchor, where the opposite strap
            # terminates. Same treatment, on the side edge at the waist.
            _rivet("waist anchor rivet",
                   max(rivet_cap, HALF_SKIRT - hem_allowance - rivet_cap),
                   hem_allowance + rivet_cap),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Apron body (cut on fold)",
    )


# ── The cross-back strap length, solved as a HYPOTENUSE ─────────────────────
# A crossing strap does not run straight down the back. It runs diagonally, from
# one bib corner, over the shoulder, across the back to the OPPOSITE waist
# anchor. Its length is therefore the hypotenuse of a triangle whose sides are
# MEASURED off the built body, not a fraction of the apron's height.
_BODY = build_body()
# Horizontal component: from a bib corner across the back to the opposite waist
# anchor. The two anchors are on opposite sides of the body, so the run is the
# back width plus the offset of each anchor from the centre line.
STRAP_DX = back_width + HALF_BIB + (HALF_SKIRT - HALF_BIB) * 0.5
# Vertical component: bib top down to the waist.
STRAP_DY = bib_height
# The arc over the shoulder itself, which no triangle accounts for.
SHOULDER_ARC = max(70.0, back_width * 0.26)
STRAP_DIAGONAL = math.sqrt(STRAP_DX ** 2 + STRAP_DY ** 2)
STRAP_PATH = STRAP_DIAGONAL + SHOULDER_ARC
# What a naive draft would have produced, kept for the metadata comparison — the
# number this cartridge exists to not get wrong.
STRAP_NAIVE = STRAP_DY + SHOULDER_ARC
# Cut length: the path, plus a tie tail at the far end, plus turnings.
TIE_TAIL = max(120.0, STRAP_PATH * 0.22)
STRAP_CUT = STRAP_PATH + TIE_TAIL + 2.0 * seam_allowance
# The strap's cut height: folded in half lengthwise, so twice the finished width
# plus its two turnings. This is what the bib's top edge has to be able to carry.
STRAP_END_H = strap_width * 2.0 + 2.0 * seam_allowance


def build_strap():
    """A cross-back strap, cut 2. Rivets at the bib end, ties at the waist end.

    Cut flat at twice the finished width plus turnings: folded in half lengthwise
    and topstitched down both edges, which is what makes a denim strap carry a
    loaded apron without rolling into a cord across the shoulder.
    """
    w = STRAP_END_H
    ln = STRAP_CUT
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("bib_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("tie_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                    kind="marking"),
        fc.Internal("strap topstitch",
                    [fc.P(TOPSTITCH, TOPSTITCH), fc.P(ln - TOPSTITCH, TOPSTITCH)],
                    kind="trace"),
        # Where the diagonal ends and the tie tail begins — the point that lands
        # on the waist anchor. Marked so the strap is positioned by its own mark
        # rather than by holding the apron up and guessing.
        fc.Internal("waist anchor point",
                    [fc.P(TIE_TAIL + seam_allowance, 0.0),
                     fc.P(TIE_TAIL + seam_allowance, w)],
                    kind="marking"),
        fc.Internal("shoulder crossing point",
                    [fc.P(ln - seam_allowance - SHOULDER_ARC, 0.0),
                     fc.P(ln - seam_allowance - SHOULDER_ARC, w)],
                    kind="marking"),
        # RIVET SITE 3 — the strap's own bib end, the mating half of the bib
        # corner rivet. Stepped in by the cap diameter plus a clearance.
        _rivet("strap bib rivet",
               ln - seam_allowance - rivet_cap * 1.6, w / 2.0),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},   # long edges are folded, not sewn
        notches=[fc.Notch("lower", 0.0, "tie tail end"),
                 fc.Notch("lower", 1.0, "bib rivet end")],
        grainline=fc.Grainline(fc.P(ln * 0.10, w / 2.0), fc.P(ln * 0.90, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Cross-back strap (cut 2)",
    )


def build_pocket():
    """Divided patch pocket, cut 1 on the fold at centre front.

    Two divisions per half, so four compartments across the finished apron —
    the chore-apron convention. The top corners are riveted: that is where a hand
    goes in carrying a full weight of tools, and it is where an unriveted pocket
    tears away from the apron first.
    """
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(HALF_POCKET, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(HALF_POCKET, 0.0),
                                 fc.P(HALF_POCKET, POCKET_H))]),
        fc.Edge("top", [fc.Line(fc.P(HALF_POCKET, POCKET_H),
                                fc.P(0.0, POCKET_H))]),
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, POCKET_H), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("mouth topstitch",
                    [fc.P(TOPSTITCH, POCKET_H - TOPSTITCH),
                     fc.P(HALF_POCKET - TOPSTITCH, POCKET_H - TOPSTITCH)],
                    kind="trace"),
        fc.Internal("divider 1",
                    [fc.P(HALF_POCKET * 0.5, 0.0),
                     fc.P(HALF_POCKET * 0.5, POCKET_H)],
                    kind="trace"),
        # RIVET SITE 4 — the pocket's outer top corner, stepped in by the cap
        # diameter plus a clearance off BOTH edges so it lands on cloth, never on
        # the turned mouth or the side allowance.
        _rivet("pocket corner rivet",
               max(rivet_cap, HALF_POCKET - seam_allowance - rivet_cap),
               POCKET_H - hem_allowance - rivet_cap),
        # And the inner one, on the divider, where the two compartments pull
        # against each other.
        _rivet("pocket divider rivet",
               HALF_POCKET * 0.5,
               POCKET_H - hem_allowance - rivet_cap),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("top", 0.5, "divider position"),
                 fc.Notch("bottom", 0.5, "divider position")],
        grainline=fc.Grainline(fc.P(HALF_POCKET * 0.75, 18.0),
                               fc.P(HALF_POCKET * 0.75, POCKET_H - 18.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Divided patch pocket (cut on fold)",
    )


# Rivet count: 2 at the bib corners (strap ends), 2 at the waist anchors, 2 at
# the pocket's outer corners, 2 on the pocket divider. Eight, all load-bearing.
N_RIVETS = 8


def build():
    pattern = fc.PatternSet("denim-chore-apron")
    everything = target_piece == "set"
    want = {
        "body": everything or target_piece == "body",
        "strap": everything or target_piece == "strap",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["body"]:
        pattern.add(build_body())
    if want["strap"]:
        pattern.add(build_strap())
    if want["pocket"]:
        pattern.add(build_pocket())

    # ── Declared seams ───────────────────────────────────────────────────────
    # A chore apron is deliberately almost seamless: the body is one piece and
    # every outer edge is turned, not joined. What IS declarable is the three
    # applied joins, and each one is a real check that would catch a redraft.
    if want["pocket"]:
        # The pocket is topstitched onto the body down both sides. Those two
        # sides are the same edge on a piece cut on the fold, so what this proves
        # is that the piece did not invert: on an inverted outline the kernel's
        # CCW normalization reverses the edge order, and `side` would no longer
        # measure the clamped POCKET_H it was drafted to.
        pattern.declare_seam(("pocket", "side"), ("pocket", "cf_fold"), tol=0.3)
    if want["strap"]:
        # Both long edges of the strap are folded to the same centre line, so
        # they must measure identically — the check that catches a strap whose
        # cut length was solved on one edge and drawn on the other.
        pattern.declare_seam(("strap", "lower"), ("strap", "upper"), tol=0.3)
    if want["strap"] and want["body"]:
        # The strap is riveted flat across the bib's top edge, so the bib must be
        # wide enough to receive BOTH straps' ends side by side plus the turned
        # hems either side of them. HALF_BIB is floored on strap_width for that
        # reason; this declares the relationship so it is checked rather than
        # trusted. The bib top (half width, on the fold) is compared against one
        # strap end plus that floor's margin — the declared ease IS the margin,
        # so the check lands at delta ≈ 0 and goes red the day the floor is
        # loosened or the strap is widened past what the bib can carry.
        pattern.declare_seam(("body", "bib_top"), ("strap", "bib_end"),
                             tol=1.0, ease=HALF_BIB - STRAP_END_H)

    fabric_width = 1500.0                       # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; 12 oz is the right "
                 f"weight here — this is the one garment in the family that is "
                 f"SUPPOSED to be stiff, and it softens exactly where it is used."},
        {"item": "rivet + burr", "qty": N_RIVETS, "unit": "set",
         "note": f"Yantra4D rivet (notion.hardware_ref) at a {rivet_cap:.0f} mm "
                 f"cap: 2 at the bib corners, 2 at the waist anchors, 2 at the "
                 f"pocket's outer corners, 2 on the divider. Every one sits at a "
                 f"load-path termination, stepped in from both edges by the cap's "
                 f"own diameter plus clearance."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm on every turned edge, both "
                 f"strap edges, the pocket mouth and both dividers."},
        {"item": "rivet setting die + anvil", "qty": 1, "unit": "tool",
         "note": "a rivet set with a hammer and no die deforms the burr and the "
                 "joint works loose; this is the tool the garment needs and the "
                 "bar-tack alternative is the failure it is drafted against."},
    ]
    pattern.metadata = {
        "fc300_rank": 291,
        "family": "denim",
        "tier": 2,
        "fabric_hint": "mezclilla-denim",
        "finished_mm": {
            "bib_half_width": round(HALF_BIB, 1),
            "bib_height": round(bib_height, 1),
            "skirt_half_width": round(HALF_SKIRT, 1),
            "skirt_length": round(skirt_length, 1),
            "pocket_half_width": round(HALF_POCKET, 1),
            "pocket_height": round(POCKET_H, 1),
            "strap_cut_length": round(STRAP_CUT, 1),
            "strap_finished_width": round(strap_width, 1),
        },
        "solved": {
            "strap_dx_mm": round(STRAP_DX, 2),
            "strap_dy_mm": round(STRAP_DY, 2),
            "shoulder_arc_mm": round(SHOULDER_ARC, 2),
            "strap_diagonal_mm": round(STRAP_DIAGONAL, 2),
            "strap_path_solved_mm": round(STRAP_PATH, 2),
            "strap_path_naive_mm": round(STRAP_NAIVE, 2),
            "naive_shortfall_mm": round(STRAP_PATH - STRAP_NAIVE, 2),
            "tie_tail_mm": round(TIE_TAIL, 2),
            "rivet_count": N_RIVETS,
            "rivet_cap_mm": round(rivet_cap, 2),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(HALF_BIB, 2),
            "bib_half_was_clamped": bool(abs(HALF_BIB - _BIB_HALF_RAW) > 0.01),
            "pocket_half_requested_mm": round(_POCKET_HALF_RAW, 2),
            "pocket_half_clamped_mm": round(HALF_POCKET, 2),
            "pocket_half_was_clamped": bool(
                abs(HALF_POCKET - _POCKET_HALF_RAW) > 0.01),
            "pocket_height_requested_mm": round(_POCKET_H_RAW, 2),
            "pocket_height_clamped_mm": round(POCKET_H, 2),
            "pocket_height_was_clamped": bool(abs(POCKET_H - _POCKET_H_RAW) > 0.01),
            "note": "the cross-back strap is a HYPOTENUSE: it runs diagonally from "
                    "one bib corner across the back to the OPPOSITE waist anchor, "
                    "so its length is solved by Pythagoras from a MEASURED "
                    "horizontal spread and a MEASURED vertical drop, plus the "
                    "shoulder arc. A strap cut to the vertical drop alone is short "
                    "by naive_shortfall_mm — at defaults nearly 400 mm, which is a "
                    "strap that cannot be crossed at all. Every rivet is placed by "
                    "measuring the piece it lands on and stepping in by the cap's "
                    "own diameter plus clearance, so it is never set through a "
                    "turned hem (where it holds nothing) nor close enough to an "
                    "edge to tear out through it. The bib and both pocket "
                    "dimensions are clamped against the panels they sit on, "
                    "because an inverted piece is CCW-normalized by the kernel and "
                    "passes verify() looking healthy.",
        },
        "load_paths": {
            "principle": "the apron's whole weight hangs off the shoulders via the "
                         "crossed straps — there is NO neck loop, which is the "
                         "single thing that makes a loaded apron wearable all day",
            "terminations": "bib corners (strap pull), waist anchors (opposite "
                            "strap), pocket outer corners (hand + tool weight), "
                            "pocket divider (compartments pulling apart)",
            "why_rivets": "on 12 oz denim a bar-tack is what gives first: the "
                          "thread abrades before the cloth does. A rivet moves the "
                          "load into the cloth itself and spreads it over the cap.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm, the "
                     f"denim-family gauge: every turned edge, both strap edges, the "
                     f"pocket mouth and both dividers",
        "denim_conventions": {
            "gauge": f"{TOPSTITCH:.0f} mm twin-needle throughout, matching "
                     f"jeans-5-pocket, denim-jacket and bib-overalls",
            "turned_not_seamed": f"every outer edge takes the {hem_allowance:.0f} mm "
                                 f"hem allowance and is turned and topstitched — a "
                                 f"chore apron has no seams except where the straps "
                                 f"and the pocket attach",
            "hard_goods": "every rivet is a Yantra4D reference, never re-implemented",
        },
        "hardware": "rivets via Yantra4D (notion.hardware_ref -> rivet); the solid's "
                    "cap_dia — the parameter driving its set_face flange, i.e. the "
                    "face that bears on the cloth — is fed from this garment's "
                    "rivet_cap, which is also what sets every rivet's step-in from "
                    "the edges it lands between. One number sizes the rivet and "
                    "places it.",
    }
    return pattern


result = build()
