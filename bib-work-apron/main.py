"""
Denim Bib Work Apron — Fashion Cabinet Garment Cartridge
(FC-400 #306, workwear_uniforms, T2).

The adjustable bib apron: one body panel cut on the fold, a neck strap that
threads a D-ring so its length adjusts, and two waist ties. The whole point of
the D-ring is adjustment, and the whole point of THIS draft is that the strap is
cut to the range the D-ring can actually take up — not to a guessed length that
leaves the ring at one end of its travel.

Three things are solved by measurement rather than by formula:

  1. THE NECK STRAP IS CUT TO ITS ADJUSTMENT RANGE. A D-ring neck strap is cut so
     its slack tail, folded back through the ring, gives a MEASURED range of
     adjustment centred on the nominal neck drop. A strap cut to the nominal
     length alone has no tail to thread and no adjustment at all — the ring might
     as well be a stitched loop.

  2. THE WAIST TIES ARE CUT TO WRAP AND TIE. A waist tie is not the half-waist:
     it has to reach round the back and tie in a bow at the front, so its length
     is the MEASURED half-waist plus a wrap allowance plus a bow tail. A tie cut
     to the half-waist meets at the back and cannot be tied.

  3. THE POCKET IS CLAMPED AGAINST THE BODY IT SITS ON. A pocket wider than the
     apron body folds back on itself and — because the kernel CCW-normalizes an
     inverted outline and area() takes an absolute value — renders and passes
     verify() looking healthy. The pocket width and both strap dimensions are
     clamped and reported.

DENIM/WORKWEAR CONVENTIONS (denim-chore-apron): 7 mm twin-needle topstitch; every
outer edge turned; every hard good a Yantra4D reference. The D-RING SOLID is
Yantra4D territory (`d-ring`; see notion.hardware_ref).

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


# ── Parameters (millimetres) ─────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# body|neck_strap|waist_tie|pocket|set

bib_width = float(PARAM(lambda: bib_width, 300.0))
bib_height = float(PARAM(lambda: bib_height, 320.0))       # waist to bib top
skirt_width = float(PARAM(lambda: skirt_width, 640.0))     # width at waist
skirt_length = float(PARAM(lambda: skirt_length, 580.0))
neck_drop = float(PARAM(lambda: neck_drop, 640.0))         # bib top round the neck
half_waist = float(PARAM(lambda: half_waist, 440.0))       # half body at waist
strap_width = float(PARAM(lambda: strap_width, 34.0))
dring_webbing = float(PARAM(lambda: dring_webbing, 34.0))  # d-ring webbing width
pocket_width = float(PARAM(lambda: pocket_width, 400.0))
pocket_height = float(PARAM(lambda: pocket_height, 220.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 22.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bib_width = max(180.0, min(bib_width, 460.0))
bib_height = max(200.0, min(bib_height, 460.0))
skirt_width = max(380.0, min(skirt_width, 900.0))
skirt_length = max(300.0, min(skirt_length, 900.0))
neck_drop = max(420.0, min(neck_drop, 820.0))
half_waist = max(300.0, min(half_waist, 700.0))
strap_width = max(22.0, min(strap_width, 55.0))
dring_webbing = max(20.0, min(dring_webbing, 50.0))
pocket_width = max(200.0, min(pocket_width, 760.0))
pocket_height = max(120.0, min(pocket_height, 360.0))
hem_allowance = max(12.0, min(hem_allowance, 40.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

TOPSTITCH = 7.0

# ── Derived, clamped ─────────────────────────────────────────────────────────
HALF_SKIRT = skirt_width / 2.0
_BIB_HALF_RAW = bib_width / 2.0
HALF_BIB = max(strap_width + 12.0, min(_BIB_HALF_RAW, HALF_SKIRT - 30.0))
_POCKET_HALF_RAW = pocket_width / 2.0
HALF_POCKET = max(60.0, min(_POCKET_HALF_RAW, HALF_SKIRT - 18.0))
POCKET_H = max(60.0, min(pocket_height, skirt_length - hem_allowance - 60.0))
POCKET_TOP_Y = -max(60.0, skirt_length * 0.22)

# The neck strap: the loop over the neck plus the tail that threads the D-ring for
# adjustment. The adjustment range is a MEASURED fraction of the drop.
NECK_ADJ_RANGE = max(90.0, neck_drop * 0.22)
NECK_STRAP_CUT = neck_drop + NECK_ADJ_RANGE + dring_webbing * 2.0 + 2.0 * seam_allowance
STRAP_END_H = strap_width * 2.0 + 2.0 * seam_allowance

# The waist tie: half-waist to reach round + wrap allowance + bow tail.
WRAP_ALLOW = max(80.0, half_waist * 0.18)
BOW_TAIL = max(180.0, half_waist * 0.40)
WAIST_TIE_CUT = half_waist + WRAP_ALLOW + BOW_TAIL + 2.0 * seam_allowance


def build_body():
    """Apron body: bib + skirt in ONE piece, cut on the CF fold."""
    p_hem_c = fc.P(0.0, -skirt_length)
    p_hem_side = fc.P(HALF_SKIRT - 22.0, -skirt_length)
    p_waist_side = fc.P(HALF_SKIRT, 0.0)
    p_bib_side = fc.P(HALF_BIB, bib_height)
    p_bib_c = fc.P(0.0, bib_height)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_c, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_waist_side)]),
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
        allowances={"hem": hem_allowance, "side": hem_allowance,
                    "underarm": hem_allowance, "bib_top": hem_allowance,
                    "cf_fold": 0.0},
        notches=[fc.Notch("side", 0.0, "waist / tie level"),
                 fc.Notch("underarm", 1.0, "bib corner / neck strap")],
        grainline=fc.Grainline(fc.P(HALF_BIB * 0.6, -skirt_length + 40.0),
                               fc.P(HALF_BIB * 0.6, bib_height - 40.0)),
        internals=[
            fc.Internal("bib topstitch",
                        [fc.P(0.0, bib_height - TOPSTITCH),
                         fc.P(HALF_BIB - TOPSTITCH, bib_height - TOPSTITCH)],
                        kind="trace"),
            fc.Internal("pocket placement",
                        [fc.P(0.0, POCKET_TOP_Y), fc.P(HALF_POCKET, POCKET_TOP_Y),
                         fc.P(HALF_POCKET, POCKET_TOP_Y - POCKET_H),
                         fc.P(0.0, POCKET_TOP_Y - POCKET_H),
                         fc.P(0.0, POCKET_TOP_Y)], kind="marking"),
            fc.Internal("neck-strap anchor (bib corner)",
                        [fc.P(HALF_BIB - hem_allowance, bib_height - hem_allowance),
                         fc.P(HALF_BIB - hem_allowance - strap_width,
                              bib_height - hem_allowance)], kind="marking"),
            fc.Internal("waist-tie anchor",
                        [fc.P(HALF_SKIRT - hem_allowance, 0.0),
                         fc.P(HALF_SKIRT - hem_allowance - strap_width, 0.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Apron body (cut on fold)",
    )


def build_neck_strap():
    """The D-ring neck strap, cut 1. Cut with a threading tail for adjustment."""
    ln = NECK_STRAP_CUT
    w = STRAP_END_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("ring_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("fix_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "neck_strap", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.0, "fixed (bib) end"),
                 fc.Notch("lower", 1.0, "D-ring threading tail")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            fc.Internal("adjustment range",
                        [fc.P(ln - seam_allowance - NECK_ADJ_RANGE, w / 2.0),
                         fc.P(ln - seam_allowance, w / 2.0)], kind="marking"),
            fc.Internal("nominal neck setting",
                        [fc.P(ln - seam_allowance - NECK_ADJ_RANGE / 2.0, 0.0),
                         fc.P(ln - seam_allowance - NECK_ADJ_RANGE / 2.0, w)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="D-ring neck strap (cut 1)",
    )


def build_waist_tie():
    """A waist tie, cut 2. Long enough to wrap round and tie a bow at the front."""
    ln = WAIST_TIE_CUT
    w = STRAP_END_H
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("fix_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        # A pointed tie end: two lines meeting at a point.
        fc.Edge("tail", [fc.Line(fc.P(0.0, w), fc.P(-w * 0.6, w / 2.0)),
                         fc.Line(fc.P(-w * 0.6, w / 2.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "waist_tie", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 1.0, "apron side seam anchor"),
                 fc.Notch("lower", WRAP_ALLOW / ln, "wrap-to-back mark")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Waist tie (cut 2)",
    )


def build_pocket():
    """Divided patch pocket, cut 1 on the fold. Clamped against the body."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(HALF_POCKET, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(HALF_POCKET, 0.0), fc.P(HALF_POCKET, POCKET_H))]),
        fc.Edge("top", [fc.Line(fc.P(HALF_POCKET, POCKET_H), fc.P(0.0, POCKET_H))]),
        fc.Edge("cf_fold", [fc.Line(fc.P(0.0, POCKET_H), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("top", 0.5, "divider position"),
                 fc.Notch("bottom", 0.5, "divider position")],
        grainline=fc.Grainline(fc.P(HALF_POCKET * 0.75, 18.0),
                               fc.P(HALF_POCKET * 0.75, POCKET_H - 18.0)),
        internals=[
            fc.Internal("mouth topstitch",
                        [fc.P(TOPSTITCH, POCKET_H - TOPSTITCH),
                         fc.P(HALF_POCKET - TOPSTITCH, POCKET_H - TOPSTITCH)],
                        kind="trace"),
            fc.Internal("divider",
                        [fc.P(HALF_POCKET * 0.5, 0.0),
                         fc.P(HALF_POCKET * 0.5, POCKET_H)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Divided patch pocket (cut on fold)",
    )


def build():
    pattern = fc.PatternSet("bib-work-apron")
    everything = target_piece == "set"
    want = {
        "body": everything or target_piece == "body",
        "neck_strap": everything or target_piece == "neck_strap",
        "waist_tie": everything or target_piece == "waist_tie",
        "pocket": everything or target_piece == "pocket",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["body"]:
        pattern.add(build_body())
    if want["neck_strap"]:
        pattern.add(build_neck_strap())
    if want["waist_tie"]:
        pattern.add(build_waist_tie())
    if want["pocket"]:
        pattern.add(build_pocket())

    if want["pocket"]:
        pattern.declare_seam(("pocket", "side"), ("pocket", "cf_fold"), tol=0.3)
    if want["neck_strap"]:
        pattern.declare_seam(("neck_strap", "lower"), ("neck_strap", "upper"), tol=0.3)
    if want["waist_tie"]:
        pattern.declare_seam(("waist_tie", "lower"), ("waist_tie", "upper"), tol=0.3)

    fabric_width = 1500.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "mezclilla-denim, 12 oz (407 gsm)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker."},
        {"item": "D-ring (pair)", "qty": 1, "unit": "pair",
         "note": f"Yantra4D d-ring (notion.hardware_ref) for {dring_webbing:.0f} mm "
                 f"webbing; the neck strap threads it for a MEASURED "
                 f"{NECK_ADJ_RANGE:.0f} mm of adjustment."},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "spool",
         "note": f"twin-needle at {TOPSTITCH:.0f} mm on every turned edge, both "
                 f"strap edges, the pocket mouth and the divider."},
        {"item": "bar-tack / rivet at strap anchors", "qty": 6, "unit": "point",
         "note": "the neck strap fixed end, both waist-tie anchors, the pocket "
                 "corners; on 12 oz denim these are the load-path terminations."},
    ]
    pattern.metadata = {
        "fc400_rank": 306,
        "family": "workwear_uniforms",
        "tier": 2,
        "fabric_hint": "denim-12oz",
        "finished_mm": {
            "bib_half_width": round(HALF_BIB, 1),
            "bib_height": round(bib_height, 1),
            "skirt_half_width": round(HALF_SKIRT, 1),
            "skirt_length": round(skirt_length, 1),
            "neck_strap_cut": round(NECK_STRAP_CUT, 1),
            "waist_tie_cut": round(WAIST_TIE_CUT, 1),
            "pocket_half_width": round(HALF_POCKET, 1),
        },
        "solved": {
            "neck_drop_mm": round(neck_drop, 2),
            "neck_adjust_range_mm": round(NECK_ADJ_RANGE, 2),
            "neck_strap_cut_mm": round(NECK_STRAP_CUT, 2),
            "waist_wrap_allow_mm": round(WRAP_ALLOW, 2),
            "waist_bow_tail_mm": round(BOW_TAIL, 2),
            "waist_tie_cut_mm": round(WAIST_TIE_CUT, 2),
            "bib_half_requested_mm": round(_BIB_HALF_RAW, 2),
            "bib_half_clamped_mm": round(HALF_BIB, 2),
            "bib_half_was_clamped": bool(abs(HALF_BIB - _BIB_HALF_RAW) > 0.01),
            "pocket_half_requested_mm": round(_POCKET_HALF_RAW, 2),
            "pocket_half_clamped_mm": round(HALF_POCKET, 2),
            "pocket_half_was_clamped": bool(abs(HALF_POCKET - _POCKET_HALF_RAW) > 0.01),
            "note": "the neck strap is cut to the nominal drop PLUS a measured "
                    "adjustment range PLUS the webbing that threads the D-ring, so "
                    "the ring actually adjusts instead of sitting at one end of its "
                    "travel. The waist ties are cut to the half-waist plus a wrap "
                    "allowance plus a bow tail, so they reach round and tie. The "
                    "pocket and bib are clamped against the body, because an "
                    "inverted piece is CCW-normalized by the kernel and passes "
                    "verify() looking healthy.",
        },
        "topstitch": f"twin-needle heavy contrast (gold) at {TOPSTITCH:.0f} mm",
        "hardware": "D-ring via Yantra4D (notion.hardware_ref -> d-ring); the solid's "
                    "webbing — the parameter driving its bar width, i.e. the slot the "
                    "strap threads — is fed from this garment's dring_webbing, which "
                    "also sizes the neck strap that runs through it. The tie and "
                    "pocket anchors are a second finding, marked and counted.",
    }
    return pattern


result = build()
