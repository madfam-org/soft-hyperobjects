"""
Zip-Pull Aid Vest — Fashion Cabinet Garment Cartridge (FC-300 #252, adaptive II).

An insulated vest built around the part of a zip that actually defeats people:
not the pulling, the STARTING. Engaging a separating zip means holding the box
and the pin in register with two hands, at the hem, below the field of view,
against the weight of the garment. Tremor, one working hand, low vision, arthritic
pinch grip, cold fingers — any of them and the pin misses the box, repeatedly,
and the garment gets abandoned.

Three things are drafted in to fix that, and none of them is a bigger zip:

  1. A RIGID STARTING BOX. The bottom 90 mm of both fronts is interfaced stiff and
     bagged into a starting block, so the box side does not fold, curl or wander
     while the pin is offered up. Most «easy zip» garments soften the hem; this
     one deliberately hardens it, because a floppy box is the actual failure.
  2. A FUNNEL. The pin side is cut with a marked funnel that guides the pin down
     onto the box, so the hand can be wrong by several millimetres and still
     engage.
  3. A FINGER-RING PULL. The slider carries a printed ring aid (Yantra4D
     `zipper-loop-aid`; see notion.hardware_ref) that a whole finger or a hook
     goes through — no pinch grip required anywhere in the operation.

A vest, not a jacket, on purpose: no sleeves means no second arm to thread, which
is the other half of why outerwear gets abandoned. It goes on like a waistcoat
and closes on one line.

The drafting problems that had to be solved, not assumed:

  1. THE ZIP MUST FIT THE OPENING. A separating zip is bought or printed at a
     LENGTH. So the front opening edge is MEASURED off the built piece and the
     zip length is taken from that measurement (rounded to a stocked 10 mm step),
     rather than the opening being assumed to equal the vest length — it does
     not, because the neckline curves and the hem is squared off the CF.

  2. SHOULDER SEAM EQUALITY. The back neck sits higher than the front neck, so
     the back neck WIDTH is solved by Pythagoras from the front's MEASURED
     shoulder length. Here the consequence is specific: an unequal shoulder tips
     the whole front panel, and a tipped front panel puts the box out of plumb
     with the pin — the one thing this garment exists to keep in register.

  3. THE ARMHOLE BINDING. Cut to the MEASURED armhole, not to a girth formula,
     and shortened by a stretch factor so it holds the armhole flat against the
     body instead of letting the vest swing while the zip is being started.

Pieces:
  - front  : vest front (cut 2 mirrored), zip stand, rigid starting block.
  - back   : vest back (cut 1 on fold at CB).
  - facing : the front facing (cut 2 mirrored), carrying the interfaced block.
  - binding: the armhole/neck binding strip (cut 1), at the MEASURED length.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
# front|back|facing|binding|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
vest_length = float(PARAM(lambda: vest_length, 640.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 430.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
zip_chain = float(PARAM(lambda: zip_chain, 8.0))
ring_inner = float(PARAM(lambda: ring_inner, 26.0))
block_height = float(PARAM(lambda: block_height, 90.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
chest_girth = max(740.0, min(chest_girth, 1520.0))
vest_length = max(480.0, min(vest_length, 820.0))
shoulder_width = max(320.0, min(shoulder_width, 560.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
zip_chain = max(5.0, min(zip_chain, 12.0))       # #5 to #10 chain
ring_inner = max(16.0, min(ring_inner, 42.0))    # a finger, or a dressing hook
block_height = max(50.0, min(block_height, 150.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE_CHEST = 170.0            # over a jumper, and roomy enough to swing on
QUARTER_CHEST = (chest_girth + EASE_CHEST) / 4.0
HALF_SHOULDER = shoulder_width / 2.0

NECK_W = neck_girth / 6.0 + 11.0
NECK_DROP_F = neck_girth / 6.0 + 20.0
NECK_DROP_B = 22.0
SHOULDER_SLOPE = 40.0
ARMHOLE_DROP = 265.0          # deep: a whole jumpered arm passes without help
TOP_Y = vest_length - NECK_DROP_F

# The zip stand: the tape plus a margin, mirrored either side of centre front.
# Equal stands are what put the two chain halves in the same plane — a stand that
# differs left to right presents the pin at an angle to the box.
TAPE_W = zip_chain * 3.6 + 6.0
STAND = TAPE_W + 8.0

# The starting block: the bottom band of both fronts, interfaced rigid.
BLOCK_H = min(block_height, vest_length * 0.28)


def _armhole(p_side_top, p_shoulder_out, bias):
    return fc.Bezier(
        p_side_top,
        fc.P(p_side_top.x - 5.0, p_side_top.y + ARMHOLE_DROP * bias),
        fc.P(p_shoulder_out.x + 14.0, p_shoulder_out.y - 44.0),
        p_shoulder_out)


def build_front():
    """Vest front (cut 2 mirrored) with the zip stand cut on.

    x runs from the stand's outer fold (x = -STAND) out to the side seam; centre
    front is x = 0, so the stand is symmetric about it by construction and the
    mirrored pair puts the two chain halves in one plane.
    """
    _h = vest_length
    x_out = -STAND
    p_hem_out = fc.P(x_out, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_side_top = fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, TOP_Y)
    p_neck_cf = fc.P(x_out, TOP_Y + 6.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_out, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out, 0.43)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.52, TOP_Y - 9.0),
                                   fc.P(x_out + STAND * 0.45, TOP_Y + 2.0),
                                   p_neck_cf)]),
        # The zip opening edge, hem to neck. Its MEASURED length is what the zip
        # is bought at — see ZIP_LEN below.
        fc.Edge("zip_edge", [fc.Line(p_neck_cf, p_hem_out)]),
    ]

    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, TOP_Y)],
                    kind="marking"),
        # The chain line: where the teeth actually sit, one tape-width in.
        fc.Internal("chain-line",
                    [fc.P(-STAND + TAPE_W / 2.0, 0.0),
                     fc.P(-STAND + TAPE_W / 2.0, TOP_Y)],
                    kind="marking"),
        # THE STARTING BLOCK: the bottom band, interfaced rigid so the box side
        # cannot fold, curl or wander while the pin is offered up.
        fc.Internal("starting-block",
                    [fc.P(x_out, 0.0), fc.P(STAND + 46.0, 0.0),
                     fc.P(STAND + 46.0, BLOCK_H), fc.P(x_out, BLOCK_H),
                     fc.P(x_out, 0.0)],
                    kind="marking"),
        # THE FUNNEL: a V above the block on the PIN side, marked as a topstitch
        # guide. It flares from the chain line out to twice the stand, so a hand
        # that is several millimetres wrong still lands the pin on the chain.
        fc.Internal("pin-funnel",
                    [fc.P(-STAND + TAPE_W / 2.0, BLOCK_H * 0.30),
                     fc.P(STAND * 1.6, BLOCK_H * 1.05),
                     fc.P(STAND * 1.6, BLOCK_H * 1.35)],
                    kind="marking"),
        # A hand-warmer pocket, placed clear of the block so it never softens it.
        fc.Internal("pocket-mouth",
                    [fc.P(STAND + 70.0, BLOCK_H + 130.0),
                     fc.P(STAND + 70.0 + 160.0, BLOCK_H + 105.0)],
                    kind="marking"),
    ]

    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        # The zip edge takes NO allowance: the stand IS the allowance, folded
        # back onto the tape. Adding one here doubles the stand and throws the
        # two chain halves out of plane.
        allowances={"hem": 26.0, "zip_edge": 0.0},
        notches=[fc.Notch("armhole", 0.55, "binding match"),
                 fc.Notch("side", 0.58, "waist level"),
                 fc.Notch("zip_edge", 0.0, "top stop"),
                 fc.Notch("zip_edge", 1.0, "box / bottom stop")],
        grainline=fc.Grainline(fc.P(STAND + 40.0, 50.0),
                               fc.P(STAND + 40.0, TOP_Y - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Vest front (zip stand + starting block)",
    )


_F = build_front()

# ── The zip length, taken from the MEASURED opening ──────────────────────────
# A separating zip is bought (or printed) at a length. The opening is NOT the
# vest length: the neckline curves up past the CF point and the hem is squared
# off the stand, so measure the edge that the zip actually has to run along, then
# round DOWN to a stocked 10 mm step — a zip longer than its opening cannot be
# fitted at all, whereas a slightly short one just finishes below the neck seam.
OPENING_RUN = _F.edge("zip_edge").length(0.2)
ZIP_LEN = math.floor((OPENING_RUN - 12.0) / 10.0) * 10.0
ZIP_LEN = max(200.0, ZIP_LEN)


# ── Solve the back neck width so the shoulder seams MATCH ────────────────────
# An unequal shoulder tips the whole front panel, and a tipped front panel puts
# the box out of plumb with the pin — which is the one thing this garment exists
# to keep in register. So the back neck WIDTH is solved from the front's MEASURED
# shoulder length rather than drafted at the same neck width and hoped for.
_SHOULDER_LEN = _F.edge("shoulder").length(0.2)
_BACK_NECK_Y_OFF = NECK_DROP_F - NECK_DROP_B - SHOULDER_SLOPE * 0.10
_dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = TOP_Y + _BACK_NECK_Y_OFF


def build_back():
    """Vest back, cut 1 on fold at centre back."""
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(QUARTER_CHEST, 0.0)
    p_side_top = fc.P(QUARTER_CHEST, TOP_Y - ARMHOLE_DROP)
    p_shoulder_out = fc.P(HALF_SHOULDER, TOP_Y - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, BACK_NECK_Y + 8.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [_armhole(p_side_top, p_shoulder_out, 0.45)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.56, p_neck_shoulder.y + 3.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y),
                                   p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 26.0, "cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "binding match"),
                 fc.Notch("side", 0.58, "waist level")],
        grainline=fc.Grainline(fc.P(QUARTER_CHEST * 0.45, 50.0),
                               fc.P(QUARTER_CHEST * 0.45, BACK_NECK_Y - 60.0)),
        internals=[
            fc.Internal("quilt-line",
                        [fc.P(0.0, TOP_Y - 200.0),
                         fc.P(QUARTER_CHEST - 15.0, TOP_Y - 200.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Vest back (cut on fold)",
    )


_B = build_back()


def build_facing():
    """The front facing (cut 2 mirrored), carrying the interfaced starting block.

    Cut to the MEASURED opening run so the facing and the zip edge finish level;
    a facing cut to the vest length would run past the neck seam and have to be
    trimmed, which is exactly where the interfacing would then be trimmed away.
    """
    w = STAND + 52.0
    ln = OPENING_RUN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, ln)
    p3 = fc.P(0.0, ln)
    edges = [
        fc.Edge("zip_side", [fc.Line(p0, p3).reversed()]),
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("inner", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
    ]
    return fc.Piece(
        "facing", edges,
        seam_allowance=seam_allowance,
        allowances={"zip_side": 0.0},
        notches=[fc.Notch("zip_side", 0.0, "box / bottom stop"),
                 fc.Notch("zip_side", min(0.99, BLOCK_H / ln), "top of starting block")],
        grainline=fc.Grainline(fc.P(w / 2.0, 30.0), fc.P(w / 2.0, ln - 30.0)),
        internals=[
            # The rigid block: the ONLY part of this garment that must not be
            # soft. Fuse a firm woven interfacing here, not a knit one.
            fc.Internal("rigid-block",
                        [fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, BLOCK_H),
                         fc.P(0.0, BLOCK_H), fc.P(0.0, 0.0)],
                        kind="marking"),
            fc.Internal("block-topstitch",
                        [fc.P(6.0, BLOCK_H), fc.P(w - 6.0, BLOCK_H)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front facing (rigid starting block)",
    )


# ── The binding, cut to the MEASURED armholes and neckline ───────────────────
# Two armholes (one front + one back each) plus the neckline. Cut to what the
# pieces actually present, then shortened by a stretch factor so the binding
# holds the armhole flat against the body — a vest that swings while the zip is
# being started is a vest whose box will not stay under the pin.
ARMHOLE_RUN = 2.0 * (_F.edge("armhole").length(0.2) + _B.edge("armhole").length(0.2))
NECK_RUN = 2.0 * _F.edge("neck").length(0.2) + 2.0 * _B.edge("neck").length(0.2)
BIND_STRETCH = 0.92
BIND_LEN = (ARMHOLE_RUN + NECK_RUN) * BIND_STRETCH
BIND_H = 46.0                 # folded to a 12 mm finished binding


def build_binding():
    """The binding strip (cut 1) for both armholes and the neckline."""
    ln = BIND_LEN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, BIND_H)
    p3 = fc.P(0.0, BIND_H)
    edges = [
        fc.Edge("attach", [fc.Line(p0, p1)]),
        fc.Edge("end_b", [fc.Line(p1, p2)]),
        fc.Edge("fold", [fc.Line(p2, p3)]),
        fc.Edge("end_a", [fc.Line(p3, p0)]),
    ]
    a_share = ARMHOLE_RUN * BIND_STRETCH / ln
    return fc.Piece(
        "binding", edges,
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("attach", 0.0, "armhole 1 start"),
                 fc.Notch("attach", min(0.98, a_share / 2.0), "armhole 1 / 2 split"),
                 fc.Notch("attach", min(0.99, a_share), "armholes end / neckline start")],
        grainline=fc.Grainline(fc.P(25.0, BIND_H / 2.0), fc.P(ln - 25.0, BIND_H / 2.0)),
        internals=[
            fc.Internal("lengthwise-fold",
                        [fc.P(0.0, BIND_H / 2.0), fc.P(ln, BIND_H / 2.0)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Binding strip (armholes + neckline, measured)",
    )


def build():
    pattern = fc.PatternSet("zip-pull-aid-vest")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "facing":
        pattern.add(build_facing())
    if everything or target_piece == "binding":
        pattern.add(build_binding())

    if everything:
        # Shoulder equality: the solve that keeps the box plumb under the pin.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=0.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # The facing runs the full measured opening — this is what guarantees the
        # interfaced block is not trimmed away at assembly.
        pattern.declare_seam(("facing", "zip_side"), ("front", "zip_edge"), tol=0.5)
        # The binding takes both armholes and the neckline, deliberately SHORT.
        pattern.declare_seam(
            ("binding", "attach"),
            [("front", "armhole"), ("front", "armhole"),
             ("back", "armhole"), ("back", "armhole"),
             ("front", "neck"), ("front", "neck"),
             ("back", "neck"), ("back", "neck")],
            tol=1.0, ease=BIND_LEN - (ARMHOLE_RUN + NECK_RUN))

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "windproof shell + 100 gsm wadding", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 76% marker, shell and lining cut alike; quilt "
                 "the back before assembly."},
        {"item": "separating zip", "qty": 1, "unit": "count",
         "note": f"#{zip_chain:.0f} chain, {ZIP_LEN:.0f} mm — taken from the MEASURED "
                 f"opening of {OPENING_RUN:.0f} mm and rounded down to a stocked step. "
                 f"A zip longer than its opening cannot be fitted at all."},
        {"item": "zipper loop aid", "qty": 1, "unit": "count",
         "note": f"Yantra4D zipper-loop-aid (notion.hardware_ref) with a "
                 f"{ring_inner:.0f} mm inner ring — a whole finger or a dressing hook "
                 f"goes through it, so no pinch grip is needed anywhere."},
        {"item": "firm woven interfacing", "qty": round(BLOCK_H * 2.4), "unit": "mm_length",
         "note": "the starting block ONLY. Firm woven, not knit: a floppy box is the "
                 "actual reason separating zips get abandoned."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "topstitch the block's upper edge — that line is what stops the "
                 "rigid section flexing at its boundary."},
    ]
    pattern.metadata = {
        "fc300_rank": 252,
        "family": "adaptive",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {
            "vest_length": round(vest_length, 1),
            "quarter_chest": round(QUARTER_CHEST, 1),
            "stand_width": round(STAND, 1),
            "tape_width": round(TAPE_W, 1),
            "block_height": round(BLOCK_H, 1),
        },
        "solved": {
            "opening_run_measured_mm": round(OPENING_RUN, 2),
            "zip_length_specified_mm": round(ZIP_LEN, 1),
            "zip_shortfall_mm": round(OPENING_RUN - ZIP_LEN, 2),
            "back_neck_half_width_mm": round(NECK_W_BACK, 2),
            "front_shoulder_measured_mm": round(_SHOULDER_LEN, 2),
            "armhole_run_measured_mm": round(ARMHOLE_RUN, 2),
            "neckline_measured_mm": round(NECK_RUN, 2),
            "binding_length_mm": round(BIND_LEN, 2),
            "note": "the zip length is taken from the MEASURED opening edge and rounded "
                    "DOWN to a stocked 10 mm step, because the opening is NOT the vest "
                    "length (the neckline curves past the CF point and the hem is squared "
                    "off the stand) and a zip longer than its opening cannot be fitted at "
                    "all. The back neck width is solved by Pythagoras from the front's "
                    "MEASURED shoulder, because an unequal shoulder tips the front panel "
                    "and puts the box out of plumb with the pin.",
        },
        "adaptive": {
            "the_real_problem": "starting a separating zip, not pulling it: engaging box "
                                "and pin needs two hands, at the hem, below the field of "
                                "view, against the weight of the garment",
            "rigid_starting_block": f"the bottom {BLOCK_H:.0f} mm of both fronts is "
                                    f"interfaced FIRM so the box cannot fold, curl or "
                                    f"wander while the pin is offered up — most 'easy zip' "
                                    f"garments soften the hem; this one hardens it",
            "pin_funnel": "a marked V above the block guides the pin down onto the chain, "
                          "so the hand can be several millimetres wrong and still engage",
            "finger_ring_pull": f"a printed ring aid with a {ring_inner:.0f} mm inner "
                                f"diameter takes a whole finger or a dressing hook — no "
                                f"pinch grip anywhere in the operation",
            "no_sleeves": "a vest on purpose: no second arm to thread, which is the other "
                          "half of why outerwear gets abandoned",
        },
        "hardware": "zip pull aid via Yantra4D (notion.hardware_ref -> zipper-loop-aid); "
                    "the aid's finger ring is driven by this vest's ring_inner and its "
                    "clip by the zip_chain the pattern's stand is sized for",
    }
    return pattern


result = build()
