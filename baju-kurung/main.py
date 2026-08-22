"""
Baju Kurung — FC-300 rank #278. Fashion Cabinet Garment Cartridge.

The Malay baju kurung: a loose, unfitted tunic worn over a wrapped skirt (kain
sarung), the national dress of Malaysia and Brunei and widely worn across
Singapore, southern Thailand and Indonesian Riau. `Kurung` means "enclosed" —
the garment's whole logic is to skim, never to trace, the body.

This draft encodes the traditional GUSSETED cut, which is the constructional
heart of the garment and the reason it can be made without curved seams:

  - KEKEK (the underarm square): a square gusset set into the underarm between
    body and sleeve. It is what lets a straight sleeve meet a straight body and
    still lift the arm. Its side is solved so that the body's armhole opening,
    the sleeve's head and the kekek's two sides close a consistent circuit.
  - PESAK (the side gore): a triangular/trapezoidal gore inserted in each lower
    side seam, widening the hem without shaping the body panel. Its slanted edge
    is measured and the body's side edge is solved to match it exactly.
  - BELAH (the neck opening): a plain slit neckline with a small stand, closed
    by a single button at the throat — the everyday `cekak musang` alternative
    (a full stand collar) is noted in the docs but not drafted here.

The garment is CUT ON THE STRAIGHT throughout — no curved armscye, no dart, no
shaped shoulder. That is not a simplification; it is the tradition, and it is
precisely why the baju kurung is so cloth-efficient and so forgiving of body
change.

Drafting note — what actually SOLVES: the sleeve is a straight tapered tube,
so its head length is known exactly. The body's armhole opening is then set
FROM the measured sleeve head minus the two kekek sides, so the three-way
underarm junction closes rather than being three numbers that nearly agree.
The pesak's slant edge is measured and the body's lower side edge is solved to
that measured length by bisection on the body's hem width.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # body|sleeve|kekek|pesak|set

chest_girth = float(PARAM(lambda: chest_girth, 960.0))    # body chest circuit
body_ease = float(PARAM(lambda: body_ease, 220.0))        # the "kurung" looseness
top_length = float(PARAM(lambda: top_length, 780.0))      # shoulder → hem
shoulder_width = float(PARAM(lambda: shoulder_width, 400.0))  # point to point
sleeve_length = float(PARAM(lambda: sleeve_length, 540.0))    # shoulder → cuff
cuff_girth = float(PARAM(lambda: cuff_girth, 280.0))          # sleeve opening
kekek_side = float(PARAM(lambda: kekek_side, 110.0))          # underarm gusset side
pesak_flare = float(PARAM(lambda: pesak_flare, 150.0))        # gore width at hem
neck_width = float(PARAM(lambda: neck_width, 160.0))          # belah opening width
neck_drop = float(PARAM(lambda: neck_drop, 130.0))            # slit depth
button_ligne = float(PARAM(lambda: button_ligne, 18.0))       # throat button
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1400.0))
body_ease = max(120.0, min(body_ease, 400.0))
top_length = max(550.0, min(top_length, 1100.0))
shoulder_width = max(300.0, min(shoulder_width, 520.0))
sleeve_length = max(300.0, min(sleeve_length, 680.0))
cuff_girth = max(200.0, min(cuff_girth, 420.0))
kekek_side = max(70.0, min(kekek_side, 160.0))
pesak_flare = max(60.0, min(pesak_flare, 300.0))
neck_width = max(110.0, min(neck_width, 240.0))
neck_drop = max(70.0, min(neck_drop, 260.0))
button_ligne = max(12.0, min(button_ligne, 30.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# ── Derived geometry ─────────────────────────────────────────────────────────
HALF_BODY = (chest_girth + body_ease) / 4.0     # quarter circuit = half panel width
HALF_SHOULDER = shoulder_width / 2.0
# The body panel width must at least carry the shoulder.
HALF_BODY = max(HALF_BODY, HALF_SHOULDER + 20.0)

SLEEVE_HEAD = HALF_BODY - HALF_SHOULDER + kekek_side   # straight drop from shoulder end
# Armhole depth on the body: the straight vertical drop the sleeve head meets.
ARM_DEPTH = SLEEVE_HEAD
PESAK_TOP = 0.0                                  # the gore starts at a point
PESAK_H = top_length * 0.55                      # gore height up from the hem
# The pesak's slanted edge, measured from its own geometry (not assumed).
PESAK_SLANT = math.hypot(pesak_flare, PESAK_H)

# The body's armhole is a SLANT from the shoulder end down to the side seam, so
# its true length is the hypotenuse — not the vertical drop. Measure it, then
# take the sleeve head FROM that measurement less one kekek side, so the
# three-way underarm junction closes exactly.
ARMHOLE_RUN = HALF_BODY - HALF_SHOULDER
ARMHOLE_LEN = math.hypot(ARMHOLE_RUN, ARM_DEPTH)
SLEEVE_HEAD_SOLVED = ARMHOLE_LEN - kekek_side
if SLEEVE_HEAD_SOLVED < 40.0:                    # gusset must not eat the armhole
    kekek_side = max(30.0, ARMHOLE_LEN - 60.0)
    SLEEVE_HEAD_SOLVED = ARMHOLE_LEN - kekek_side


def build_body():
    """Front/back body panel (cut 2), cut on the fold at centre.

    Straight throughout: level shoulder, straight vertical armhole opening,
    straight side seam. `side_lower` is solved to the pesak's MEASURED slant so
    the gore sets in exactly; `armhole` is the vertical opening the sleeve head
    meets.
    """
    w = HALF_BODY
    h = top_length
    # The lower side edge must equal the pesak slant so the gore fits flat.
    # It runs from the armhole base down to the hem corner: solve its run.
    _side_upper_h = h - PESAK_H
    # side_lower is a straight edge of length PESAK_SLANT from (w, PESAK_H) down
    # to the hem; its horizontal run is solved from that measured length.
    run_sq = PESAK_SLANT ** 2 - PESAK_H ** 2
    run = math.sqrt(max(0.0, run_sq))            # == pesak_flare by construction
    hem_x = w - run if run < w - 40.0 else w * 0.6
    # Re-solve the true slant for the clamped hem_x so the seam is exact.
    true_run = w - hem_x
    slant_h = math.sqrt(max(1.0, PESAK_SLANT ** 2 - true_run ** 2))

    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("shoulder", [fc.Line(fc.P(0.0, h), fc.P(HALF_SHOULDER, h))]),
        fc.Edge("armhole", [fc.Line(fc.P(HALF_SHOULDER, h),
                                    fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side_upper", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, slant_h))]),
        fc.Edge("side_lower", [fc.Line(fc.P(w, slant_h), fc.P(hem_x, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hem_x, 0.0), fc.P(0.0, 0.0))]),
    ]
    # The belah: a centre-front slit, marked (the back is cut the same, slit
    # omitted on the back when cutting).
    internals = [
        fc.Internal("belah-slit", [fc.P(0.0, h - neck_drop - neck_width * 0.30),
                                   fc.P(0.0, h - neck_width * 0.30)], kind="cut"),
        fc.Internal("neck-scoop", [fc.P(0.0, h - neck_width * 0.30),
                                   fc.P(neck_width / 2.0, h)], kind="marking"),
        fc.Internal("button-seat",
                    [fc.P(0.0, h - neck_width * 0.30),
                     fc.P(button_ligne * 0.635, h - neck_width * 0.30)],
                    kind="drill"),
    ]
    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve head match"),
                 fc.Notch("side_lower", 0.0, "pesak top — gore point")],
        grainline=fc.Grainline(fc.P(w * 0.35, h * 0.15), fc.P(w * 0.35, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center", mirror=True),
        label="Body (badan)",
    )


def build_sleeve():
    """Straight tapered sleeve (cut 2), cut on the fold along its LENGTH.

    The fold runs along the top of the arm, so the drafted half-sleeve's `head`
    edge is the vertical drop at the shoulder end — this is the edge that sews
    to the body's armhole opening, and it is exactly ARM_DEPTH less the kekek
    side (the kekek takes the remainder of the circuit). `taper` runs from the
    head's base to the cuff; `underarm` is the fold.
    """
    head = SLEEVE_HEAD_SOLVED                # solved from the MEASURED armhole
    half_cuff = cuff_girth / 2.0
    ln = sleeve_length
    edges = [
        # x = along the arm (shoulder → cuff); y = fold (0) out to the underarm.
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
        notches=[fc.Notch("head", 0.5, "body armhole match")],
        grainline=fc.Grainline(fc.P(ln * 0.15, head * 0.3),
                               fc.P(ln * 0.85, half_cuff * 0.4)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve (lengan)",
    )


def build_kekek():
    """The kekek: a square underarm gusset (cut 2).

    Four equal sides — two sew to the body's armhole base, two to the sleeve's
    underarm. Squareness is the point: it is what turns two straight seams into
    a joint that lifts.
    """
    s = kekek_side
    return fc.Piece(
        "kekek",
        [
            fc.Edge("to_body_a", [fc.Line(fc.P(0.0, 0.0), fc.P(s, 0.0))]),
            fc.Edge("to_sleeve_a", [fc.Line(fc.P(s, 0.0), fc.P(s, s))]),
            fc.Edge("to_body_b", [fc.Line(fc.P(s, s), fc.P(0.0, s))]),
            fc.Edge("to_sleeve_b", [fc.Line(fc.P(0.0, s), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("to_body_a", 0.5, "underarm point")],
        grainline=fc.Grainline(fc.P(s * 0.5, s * 0.15), fc.P(s * 0.5, s * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underarm gusset (kekek)",
    )


def build_pesak():
    """The pesak: the side gore (cut 2), a triangle rising from the hem.

    Its two slanted edges are equal and each sews to one body panel's
    `side_lower`. The gore is what gives the hem its sweep without shaping the
    body panel at all.
    """
    fl, h = pesak_flare, PESAK_H
    return fc.Piece(
        "pesak",
        [
            fc.Edge("hem", [fc.Line(fc.P(-fl, 0.0), fc.P(fl, 0.0))]),
            fc.Edge("slant_back", [fc.Line(fc.P(fl, 0.0), fc.P(0.0, h))]),
            fc.Edge("slant_front", [fc.Line(fc.P(0.0, h), fc.P(-fl, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("slant_front", 1.0, "gore point — match body notch")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side gore (pesak)",
    )


def build():
    pattern = fc.PatternSet("baju-kurung")
    every = target_piece == "set"
    if every or target_piece == "body":
        pattern.add(build_body())
    if every or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if every or target_piece == "kekek":
        pattern.add(build_kekek())
    if every or target_piece == "pesak":
        pattern.add(build_pesak())

    if every:
        # The underarm circuit: the body's armhole opening is taken by the
        # sleeve head PLUS one kekek side — that is the whole point of the
        # gusset, and the check proves the three-way junction closes.
        pattern.declare_seam(("body", "armhole"),
                             [("sleeve", "head"), ("kekek", "to_body_a")], tol=1.0)
        # The gore's slant meets the body's lower side edge, exactly.
        pattern.declare_seam(("pesak", "slant_front"), ("body", "side_lower"), tol=1.0)
        pattern.declare_seam(("pesak", "slant_back"), ("body", "side_lower"), tol=1.0)
        # The kekek is square: its body sides and sleeve sides are equal.
        pattern.declare_seam(("kekek", "to_body_a"), ("kekek", "to_sleeve_a"), tol=0.5)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "cotton voile / rayon / songket-weight silk",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 80% marker; straight cut nests well."},
        {"item": "throat button", "qty": 1, "unit": "count",
         "note": f"Yantra4D sew-through-button at {button_ligne:.0f} ligne "
                 "(see notion.hardware_ref); closes the belah at the throat."},
        {"item": "neck facing", "qty": 1, "unit": "piece",
         "note": "bias or shaped facing finishing the belah slit and neck scoop."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": "flat-fell the straight seams."},
    ]
    pattern.metadata = {
        "fc300_rank": 278,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "tradition": "Malay (Malaysia, Brunei, Singapore, Riau) — the gusseted cut",
        "finished_mm": {"length": round(top_length, 1),
                        "chest": round(chest_girth + body_ease, 1),
                        "sleeve": round(sleeve_length, 1)},
        "solved": {
            "half_body_mm": round(HALF_BODY, 2),
            "armhole_len_mm": round(ARMHOLE_LEN, 2),
            "sleeve_head_mm": round(SLEEVE_HEAD_SOLVED, 2),
            "kekek_side_mm": round(kekek_side, 2),
            "pesak_slant_mm": round(PESAK_SLANT, 2),
            "note": "the body armhole is a SLANT, so its length is measured as the "
                    "hypotenuse and the sleeve head is solved FROM that measurement "
                    "less one kekek side — the three-way underarm junction closes "
                    "exactly. The body's lower side edge is solved to the pesak's "
                    "measured slant, so the gore sets in flat.",
        },
        "hardware": "throat button via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); button_ligne drives the belah's button seat",
        "cut_philosophy": "straight-cut throughout — no curved armscye, no dart, no "
                          "shaped shoulder. The kekek and pesak do the shaping work.",
    }
    return pattern


result = build()
