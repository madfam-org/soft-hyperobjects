"""
Deel (дээл) — FC-300 rank #285. Fashion Cabinet Garment Cartridge.

The deel is the wrap coat of Mongolia and Inner Mongolia — also worn, in
related forms, by Buryat, Kalmyk and Tuvan communities. It is a full-length
robe crossed right over left and fastened along a diagonal, worn with a long
sash (бүс, `büs`) wound at the waist. It is the everyday garment of the steppe
and remains ordinary working dress, not a costume.

The deel's construction answers a specific set of problems — riding, cold, and
long distances from a tailor — and the draft encodes those answers:

  - THE ENGER (энгэр): THE DIAGONAL CHEST FLAP. The closure is not a straight
    centre front. The right front carries a stepped, angled flap running from
    the neck across the chest to the right underarm, and the fastenings sit
    along it. This is the deel's defining line. The flap is a real polygon whose
    diagonal run is MEASURED, and the under-panel is solved against it.
  - THE STAND COLLAR IS SET TO A MEASURED NECKLINE. The collar band's length is
    solved from the drafted neck curves — front plus back — not from a neck
    girth estimate, because the enger's angled neck edge is longer than the
    neck circuit it sits on.
  - IT IS CUT LONG AND WORN BLOUSED. The sash is wound at the waist and the body
    is pulled up over it, forming a pouch that carries things. So the drafted
    length includes a `blouse_allowance` — real cloth that the sash takes up —
    and the draft reports the worn length separately from the cut length. A
    draft that ignored this would produce a deel that is correct on the table
    and short on the body.
  - THE SLEEVE RUNS LONG. Traditionally past the fingertips, turned back as a
    cuff (нударга, `nudarga`) or left down against cold.

Drafting note — what actually SOLVES: the enger's diagonal edge is measured
from its drafted polygon and the body panel's own diagonal is solved to that
measurement, so the flap lies flat across the chest. The collar band's length is
solved from the SUM of the measured front-neck and back-neck curves rather than
from a girth parameter. The armscye is measured as a curve and the sleeve head
solved from it. The cut length is solved from the worn length plus the blouse
allowance, so the number the wearer gave is the number they get.

EXCLUSION, stated rather than quietly ignored: this cartridge drafts the
everyday deel. It does NOT draft the ceremonial and rank-marking forms — the
`khantaaz` and `khurim` festival deels, the specific colour, trim and knot
conventions that mark marital status, ethnic group (Khalkha, Buryat, Kazakh,
Torguud and others each have distinct cuts and edgings), or monastic dress.
Those distinctions are how people read one another, and flattening them into a
trim slider would be exactly the costume-ification this commons refuses. The
regional cut differences are real enough that a Buryat deel is not this pattern
with different braid — it is a different draft.

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
# body|enger|sleeve|collar|sash|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
chest_ease = float(PARAM(lambda: chest_ease, 200.0))       # room for layers
worn_length = float(PARAM(lambda: worn_length, 1180.0))    # FINISHED, on the body
blouse_allowance = float(PARAM(lambda: blouse_allowance, 150.0))  # taken by the sash
shoulder_width = float(PARAM(lambda: shoulder_width, 450.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 680.0))  # long, past the hand
cuff_girth = float(PARAM(lambda: cuff_girth, 260.0))
enger_drop = float(PARAM(lambda: enger_drop, 260.0))        # flap depth at neck
enger_run = float(PARAM(lambda: enger_run, 340.0))          # flap reach to underarm
collar_height = float(PARAM(lambda: collar_height, 55.0))   # stand collar
neck_width = float(PARAM(lambda: neck_width, 180.0))
sash_width = float(PARAM(lambda: sash_width, 300.0))        # büs, folded in wear
sash_wraps = float(PARAM(lambda: sash_wraps, 3.0))          # times round the waist
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
button_ligne = float(PARAM(lambda: button_ligne, 24.0))     # enger fastenings
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(750.0, min(chest_girth, 1500.0))
chest_ease = max(100.0, min(chest_ease, 420.0))
worn_length = max(700.0, min(worn_length, 1600.0))
blouse_allowance = max(0.0, min(blouse_allowance, 350.0))
shoulder_width = max(330.0, min(shoulder_width, 580.0))
sleeve_length = max(400.0, min(sleeve_length, 850.0))
cuff_girth = max(180.0, min(cuff_girth, 420.0))
enger_drop = max(120.0, min(enger_drop, 460.0))
enger_run = max(150.0, min(enger_run, 520.0))
collar_height = max(25.0, min(collar_height, 110.0))
neck_width = max(130.0, min(neck_width, 280.0))
sash_width = max(150.0, min(sash_width, 500.0))
sash_wraps = max(1.0, min(sash_wraps, 6.0))
waist_girth = max(600.0, min(waist_girth, 1500.0))
button_ligne = max(14.0, min(button_ligne, 40.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 90.0))

HALF_CHEST = (chest_girth + chest_ease) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
ARM_DEPTH = HALF_CHEST * 0.66

# THE CUT LENGTH is solved from the WORN length plus what the sash blouses up.
# This is the number the cutter needs; worn_length is the number the wearer gave.
CUT_LENGTH = worn_length + blouse_allowance

# The enger's diagonal: measured from its own geometry, not assumed.
ENGER_DIAG = math.hypot(enger_run, enger_drop)

# The sash: a real circuit, wound `sash_wraps` times plus a tying tail.
SASH_LENGTH = waist_girth * sash_wraps + 400.0

# Measured values filled during build().
MEASURED = {}


def _armscye(x0, y0, x1, y1):
    return fc.curve_through(fc.P(x0, y0), fc.P(x1, y1), bulge=0.30, side=-1.0)


def build_body():
    """The body panel — front and back, cut 2, straight-sided steppe cut.

    The deel is cut generously and squarely; the shaping is done by the sash,
    not by the seam. The `enger_diag` edge is the diagonal the chest flap lies
    against, solved to the flap's MEASURED diagonal so the flap sits flat.
    """
    w, h = HALF_CHEST, CUT_LENGTH
    sh_y = h
    ua_y = h - ARM_DEPTH

    # The diagonal the enger crosses: from the neck edge down and out toward
    # the underarm. Its run is solved so its LENGTH equals the flap's measured
    # diagonal — the flap and the body edge it lies on must agree.
    diag_run = math.sqrt(max(0.0, ENGER_DIAG ** 2 - enger_drop ** 2))
    diag_x = min(w - 20.0, neck_width / 2.0 + diag_run)
    # Re-solve the drop for the clamped run so the edge is exactly ENGER_DIAG.
    true_run = diag_x - neck_width / 2.0
    diag_drop = math.sqrt(max(1.0, ENGER_DIAG ** 2 - true_run ** 2))

    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, sh_y - enger_drop))]),
        # The diagonal the enger lies along.
        fc.Edge("enger_diag", [fc.Line(fc.P(0.0, sh_y - enger_drop),
                                       fc.P(true_run, sh_y - enger_drop + diag_drop))]),
        fc.Edge("neck", [fc.curve_through(
            fc.P(true_run, sh_y - enger_drop + diag_drop),
            fc.P(neck_width / 2.0, sh_y), bulge=0.18, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_width / 2.0, sh_y),
                                     fc.P(HALF_SHOULDER, sh_y))]),
        fc.Edge("armscye", [_armscye(HALF_SHOULDER, sh_y, w, ua_y)]),
        fc.Edge("side", [fc.Line(fc.P(w, ua_y), fc.P(w, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]

    internals = [
        # The sash line: where the büs is wound and the body blouses over it.
        fc.Internal("sash-line",
                    [fc.P(0.0, blouse_allowance + sash_width * 0.5),
                     fc.P(w, blouse_allowance + sash_width * 0.5)],
                    kind="marking"),
        # The riding vent at the side hem, on the everyday deel.
        fc.Internal("side-vent", [fc.P(w, 0.0), fc.P(w, h * 0.18)], kind="marking"),
    ]

    return fc.Piece(
        "body",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0},
        notches=[fc.Notch("armscye", 0.5, "sleeve head match"),
                 fc.Notch("enger_diag", 0.5, "enger flap match"),
                 fc.Notch("side", 0.5, "sash line")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Body (бие) — front and back",
    )


def build_enger():
    """The энгэр (enger) — the diagonal chest flap that IS the deel's closure.

    A stepped polygon: it rises to the collar at the neck, runs across the
    chest, and steps down to the right underarm where the fastenings end. Its
    `diagonal` edge is the one the body panel was solved to.
    """
    run, drop = enger_run, enger_drop
    step = drop * 0.32                     # the characteristic shoulder step

    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, drop), fc.P(neck_width / 2.0, drop))]),
        fc.Edge("step", [fc.Line(fc.P(neck_width / 2.0, drop),
                                 fc.P(neck_width / 2.0, drop - step))]),
        fc.Edge("shoulder_run", [fc.Line(fc.P(neck_width / 2.0, drop - step),
                                         fc.P(run, drop - step))]),
        fc.Edge("underarm_end", [fc.Line(fc.P(run, drop - step), fc.P(run, 0.0))]),
        # The diagonal: the long edge that crosses the chest. Its LENGTH is
        # ENGER_DIAG by construction — the body's edge was solved to it.
        fc.Edge("diagonal", [fc.Line(fc.P(run, 0.0), fc.P(0.0, drop))]),
    ]

    # The fastenings run along the diagonal. Their count is derived from the
    # measured diagonal and a comfortable spacing — an integer, since you
    # cannot sew two-thirds of a button.
    spacing = max(60.0, button_ligne * 3.2)
    n_fast = max(2, int(ENGER_DIAG / spacing))
    internals = []
    for i in range(n_fast):
        t = (i + 0.5) / float(n_fast)
        px = run * (1.0 - t)
        py = drop * t
        internals.append(
            fc.Internal("fastening-seat",
                        [fc.P(px, py), fc.P(px + button_ligne * 0.635, py)],
                        kind="drill"))

    return fc.Piece(
        "enger",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("diagonal", 0.5, "body diagonal match"),
                 fc.Notch("neck_edge", 1.0, "collar match")],
        grainline=fc.Grainline(fc.P(run * 0.3, drop * 0.25),
                               fc.P(run * 0.3, drop * 0.75)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=False),
        label="Chest flap (энгэр enger)",
    )


def build_sleeve():
    """A long straight tapered sleeve, head SOLVED from the measured armscye."""
    head = MEASURED.get("sleeve_head", ARM_DEPTH)
    half_cuff = cuff_girth / 2.0
    ln = sleeve_length
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("cuff", [fc.Line(fc.P(ln, 0.0), fc.P(ln, half_cuff))]),
            fc.Edge("taper", [fc.Line(fc.P(ln, half_cuff), fc.P(0.0, head))]),
            fc.Edge("head", [fc.Line(fc.P(0.0, head), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cuff": hem_allowance, "fold": 0.0},
        notches=[fc.Notch("head", 0.5, "armscye match"),
                 fc.Notch("fold", 0.82, "nudarga turn-back line")],
        grainline=fc.Grainline(fc.P(ln * 0.15, head * 0.3),
                               fc.P(ln * 0.85, half_cuff * 0.4)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="fold", mirror=True),
        label="Sleeve (ханцуй khantsui)",
    )


def build_collar():
    """The stand collar, length SOLVED from the MEASURED necklines.

    Not from a neck-girth parameter: the enger's angled neck edge plus the
    body's neck curves is longer than a neck circuit, and the collar must fit
    what is actually there.
    """
    ln = MEASURED.get("collar_length", neck_width * 2.6)
    h = collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_right", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "centre back"),
                 fc.Notch("neck_edge", 0.25, "shoulder match"),
                 fc.Notch("neck_edge", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.2), fc.P(ln * 0.1, h * 0.8)),
        cut=fc.CutSpec(quantity=2),
        label="Stand collar (зах zakh)",
    )


def build_sash():
    """The büs (бүс) — the long sash wound at the waist.

    Length is a real circuit: waist times the wrap count, plus a tying tail.
    """
    ln, w = SASH_LENGTH, sash_width
    return fc.Piece(
        "sash",
        [
            fc.Edge("fold", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_right", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("open", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_left", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"fold": 0.0},
        notches=[fc.Notch("fold", 0.5, "centre — first wrap")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w * 0.5), fc.P(ln * 0.85, w * 0.5)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fold", mirror=True),
        label="Sash (бүс büs)",
    )


def build():
    pattern = fc.PatternSet("deel")
    every = target_piece == "set"

    # The body must be drafted before the sleeve and collar, which are SOLVED
    # from its measured curves.
    body = build_body()
    MEASURED["armscye"] = body.edge("armscye").length(0.05)
    MEASURED["sleeve_head"] = max(60.0, MEASURED["armscye"] - seam_allowance)
    MEASURED["body_neck"] = body.edge("neck").length(0.05)
    MEASURED["body_diag"] = body.edge("enger_diag").length(0.05)

    enger = build_enger()
    MEASURED["enger_diag"] = enger.edge("diagonal").length(0.05)
    MEASURED["enger_neck"] = enger.edge("neck_edge").length(0.05)

    # The collar spans BOTH body neck curves (front and back) plus the enger's
    # own neck edge — measured, not estimated from a neck girth.
    MEASURED["collar_length"] = (MEASURED["body_neck"] * 2.0
                                 + MEASURED["enger_neck"])

    if every or target_piece == "body":
        pattern.add(body)
    if every or target_piece == "enger":
        pattern.add(enger)
    if every or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if every or target_piece == "collar":
        pattern.add(build_collar())
    if every or target_piece == "sash":
        pattern.add(build_sash())

    if every:
        # The armscye is a measured CURVE and the sleeve head was solved from it.
        pattern.declare_seam(("body", "armscye"), ("sleeve", "head"), tol=1.5,
                             ease=(MEASURED["armscye"] - MEASURED["sleeve_head"]))

        # The enger's diagonal lies on the body's diagonal edge. The body's edge
        # was SOLVED to the flap's measured diagonal, so these must be equal —
        # this check is what proves the flap lies flat across the chest.
        pattern.declare_seam(("enger", "diagonal"), ("body", "enger_diag"), tol=1.0)

        # The collar meets the assembled neckline: two body necks plus the
        # enger's neck edge. Its length was solved from those MEASUREMENTS, so
        # the seam closes by construction rather than by a girth guess.
        pattern.declare_seam(
            ("collar", "neck_edge"),
            [("body", "neck"), ("body", "neck"), ("enger", "neck_edge")],
            tol=1.5)

        # The side seams close front to back.
        pattern.declare_seam(("body", "side"), ("body", "side"), tol=0.5)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "wool, cotton drill, or silk brocade (lined for winter)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm usable width, 80% marker; the "
                 "straight steppe cut nests well."},
        {"item": "enger fastenings", "qty": max(2, int(ENGER_DIAG / max(60.0, button_ligne * 3.2))),
         "unit": "count",
         "note": f"Yantra4D sew-through-button at {button_ligne:.0f} ligne "
                 "(see notion.hardware_ref); count derived from the MEASURED "
                 "diagonal, not chosen — they must space evenly along it."},
        {"item": "lining / wadding", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a winter deel is lined and often wadded; a summer one is not."},
        {"item": "sash cloth", "qty": round(SASH_LENGTH / 10.0) * 10,
         "unit": "mm_length",
         "note": f"the büs is wound {sash_wraps:.0f}x — it is structural, not a belt."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "the enger's edges are topstitched and often braid-bound."},
    ]
    pattern.metadata = {
        "fc300_rank": 285,
        "family": "heritage_global",
        "fabric_hint": "lana-melton-abrigo",
        "tradition": "Mongolian (дээл); related forms among Buryat, Kalmyk and "
                     "Tuvan communities — each with its own distinct cut",
        "finished_mm": {"worn_length": round(worn_length, 1),
                        "cut_length": round(CUT_LENGTH, 1),
                        "chest": round(chest_girth + chest_ease, 1),
                        "sash_length": round(SASH_LENGTH, 1)},
        "solved": {
            "cut_length_mm": round(CUT_LENGTH, 2),
            "blouse_allowance_mm": round(blouse_allowance, 2),
            "enger_diagonal_mm": round(MEASURED.get("enger_diag", 0.0), 2),
            "body_diagonal_mm": round(MEASURED.get("body_diag", 0.0), 2),
            "armscye_curve_mm": round(MEASURED.get("armscye", 0.0), 2),
            "sleeve_head_mm": round(MEASURED.get("sleeve_head", 0.0), 2),
            "collar_length_mm": round(MEASURED.get("collar_length", 0.0), 2),
            "body_neck_mm": round(MEASURED.get("body_neck", 0.0), 2),
            "enger_neck_mm": round(MEASURED.get("enger_neck", 0.0), 2),
            "note": "the CUT length is solved from the WORN length plus the blouse "
                    "allowance the sash takes up — so the number the wearer gave is "
                    "the number they get on the body, not on the table. The enger's "
                    "diagonal is measured from its own polygon and the body's "
                    "diagonal edge solved to that measurement, so the flap lies flat. "
                    "The collar is solved from the SUM of the measured neck curves "
                    "(two body necks plus the enger's neck edge) rather than from a "
                    "neck girth — the angled enger neckline is longer than a neck "
                    "circuit. The armscye is a measured curve and the sleeve head "
                    "solved from it. The fastening count is an integer derived from "
                    "the measured diagonal.",
        },
        "hardware": "enger fastenings via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); button_ligne drives both the flap's "
                    "fastening seats and the printed sew_face flange",
        "cut_philosophy": "cut long and worn bloused over the sash. The shaping is "
                          "done by the büs, not by the seam — which is why the body "
                          "is straight-sided and generous, and why the sash is a "
                          "drafted piece rather than an accessory.",
        "excluded": "this is the EVERYDAY deel. The ceremonial and rank-marking "
                    "forms are NOT drafted: khantaaz and khurim festival deels, and "
                    "the colour, trim and knot conventions marking marital status and "
                    "ethnic group. Khalkha, Buryat, Kazakh and Torguud deels differ "
                    "in CUT, not merely in braid — a Buryat deel is a different draft, "
                    "not this one with different edging. Monastic dress is likewise "
                    "out of scope.",
    }
    return pattern


result = build()
