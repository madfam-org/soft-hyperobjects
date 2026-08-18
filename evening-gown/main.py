"""
Evening Gown — FC-100 rank #72 (Vestido de noche). Fashion Cabinet Cartridge.

The a-line-dress lineage taken to the floor and cut on the bias. A woven,
floor-length formal gown: front cut on fold from a scooped neck through a
fitted torso to the floor; back cut 2 with a CB seam carrying the invisible
zipper (or a side zip — see `zip_placement`), a LOW back scoop, and one
fisheye waist dart per panel. Two signatures make it a gown, not a long shift:

  1. TRUE BIAS. The grainline is drawn at an exact 45 degrees on both body
     panels (the slip-dress trick), so the fabric hangs liquid instead of
     boardy — the reason a real gown is cut on the bias in silk crepe/satin.
  2. A TRAIN. `train_length` extends the CB back hem BELOW the floor line into
     a sweep: the back hem is a curve from the side-hem point (at the floor,
     y = 0) down to the CB point at y = -train_length, while the front hem
     stays level at the floor. Hems are faced/finished, not sewn to each other,
     so the train changes only the back hem + the CB seam start point — the
     side seam is untouched and matches the front exactly.

A `silhouette` select swaps the sweep: "bias_column" skims the hip with light
flare (the classic bias column), "a_line_train" opens the hem well past the
hip for a dramatic A-line sweep. Either way the torso is fitted and the gown
is fully lined (a bias shell needs an underlining/lining to hang true) — the
lining is cut from the same body pieces, noted in the BOM, not re-drafted.

Front and back share one shoulder, armhole, and side construction, so the
declared seams match by construction; the neck and armhole facings are derived
from the measured openings. Internal darts stay internal (teaching-grade, not
rotated into the outline).

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|facings|set
silhouette = str(PARAM(lambda: silhouette, "bias_column"))     # bias_column|a_line_train
zip_placement = str(PARAM(lambda: zip_placement, "center_back"))  # center_back|side

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
dress_length = float(PARAM(lambda: dress_length, 1450.0))   # nape line to floor hem
train_length = float(PARAM(lambda: train_length, 250.0))    # extra CB sweep below floor
flare_mm = float(PARAM(lambda: flare_mm, 90.0))             # extra half-hem over the hip
strap_width = float(PARAM(lambda: strap_width, 40.0))
back_drop = float(PARAM(lambda: back_drop, 210.0))         # low back scoop below the nape
front_drop = float(PARAM(lambda: front_drop, 80.0))
zipper_length = float(PARAM(lambda: zipper_length, 520.0))
bust_dart_intake = float(PARAM(lambda: bust_dart_intake, 26.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (mirror each manifest slider's min/max) ───────────────────────────
if silhouette not in ("bias_column", "a_line_train"):
    silhouette = "bias_column"
if zip_placement not in ("center_back", "side"):
    zip_placement = "center_back"

bust_girth = max(600.0, min(bust_girth, 1700.0))
waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(600.0, min(hip_girth, 1700.0))
dress_length = max(1200.0, min(dress_length, 1700.0))
train_length = max(0.0, min(train_length, 900.0))
flare_mm = max(20.0, min(flare_mm, 400.0))
strap_width = max(20.0, min(strap_width, 90.0))
back_drop = max(60.0, min(back_drop, 380.0))
front_drop = max(50.0, min(front_drop, 200.0))
bust_dart_intake = max(0.0, min(bust_dart_intake, 50.0))
zipper_length = max(300.0, min(zipper_length, dress_length * 0.55))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Derived skeleton (y-up: floor hem at y = 0, nape near the top) ────────────
BUST_EASE = 70.0        # woven formal ease, folded into every width below
NECK_W = 60.0           # half neck width at the high point of shoulder
BUST_DROP = 60.0        # fitted vertical run below the underarm to the bust line
DART_LEN = 115.0        # side-bust dart, leg line to apex
FISHEYE_INTAKE = 14.0
FISHEYE_LEN = 260.0
FACING_DEPTH = 32.0     # finished facing depth; strips are 2x this tall
HIP_FROM_NAPE = 620.0   # nape-to-hip vertical run (locates the flare start)
FLARE_EXTRA = 130.0     # extra half-hem the A-line silhouette adds past the hip

W = (bust_girth + BUST_EASE) / 4.0                  # bust quarter
HIPW = (hip_girth + BUST_EASE) / 4.0                # hip quarter
HPS_Y = dress_length + 20.0                         # nape line above the floor
AH = (bust_girth + BUST_EASE) / 8.0 + 95.0          # armhole scoop depth
AH = max(180.0, min(AH, 300.0))
STRAP_END = fc.P(NECK_W + strap_width, HPS_Y - 12.0)
UNDERARM = fc.P(W, HPS_Y - AH)
BUST_PT = fc.P(W, UNDERARM.y - BUST_DROP)
HIP_Y = max(HPS_Y - HIP_FROM_NAPE, BUST_PT.y - 120.0)  # hip line, kept below the bust
HIP_PT = fc.P(HIPW, HIP_Y)
# Hem half-width: the column skims the hip with light flare; the A-line opens up.
HEM_HALF = HIPW + flare_mm + (FLARE_EXTRA if silhouette == "a_line_train" else 0.0)
HEM_OUT = fc.P(HEM_HALF, 0.0)                       # side hem point, at the floor
CB_HEM = fc.P(0.0, -train_length)                   # CB hem point, dropped by the train
WAIST_Y = HIP_Y + 210.0                             # waist line, locates back darts


def _neck_edge(drop):
    """Scoop from the center top to the HPS point — identical curve family."""
    top_y = HPS_Y - drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + drop * 0.40), fc.P(NECK_W, HPS_Y))],
    )


def _armhole_edge():
    """Formal scoop, identical front/back — the armhole facing depends on it."""
    return fc.Edge(
        "armhole",
        [fc.Bezier(STRAP_END, fc.P(STRAP_END.x + 6.0, STRAP_END.y - AH * 0.45),
                   fc.P(W - AH * 0.28, UNDERARM.y + 14.0), UNDERARM)],
    )


def _shoulder_edge():
    return fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), STRAP_END)])


def _side_edge():
    """One fitted-then-flared side run for BOTH panels, so front.side matches
    back.side exactly. Underarm to the bust line straight (fitted), a first
    Bezier eases the waist suppression down onto the hip, a second sweeps out
    to the floor hem. The train never touches this edge — it is shared."""
    mid_y = (BUST_PT.y + HIP_Y) / 2.0
    flare_dir = (HEM_OUT - HIP_PT).normalized()
    run = HIP_Y * 0.30
    return fc.Edge(
        "side",
        [
            fc.Line(UNDERARM, BUST_PT),
            fc.Bezier(BUST_PT, fc.P(W - 8.0, mid_y),
                      fc.P(HIPW + 4.0, HIP_Y + (BUST_PT.y - HIP_Y) * 0.22), HIP_PT),
            fc.Bezier(HIP_PT, HIP_PT + flare_dir * run, HEM_OUT - flare_dir * run, HEM_OUT),
        ],
    )


def _grainline():
    """True 45-degree bias: equal run and rise gives an exact diagonal."""
    a = fc.P(W * 0.34, HPS_Y * 0.28)
    return fc.Grainline(a, fc.P(a.x + 140.0, a.y + 140.0))


def _front_hem():
    """Front hem stays level at the floor line from the side point to CF."""
    return fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(0.0, 0.0))])


def _back_hem():
    """Back hem sweeps from the side point (floor, y = 0) down to the CB point
    at y = -train_length. With no train it degenerates to the floor line, so
    the back matches the front; with a train it curves into the sweep."""
    if train_length < 1.0:
        return fc.Edge("hem", [fc.Line(HEM_OUT, fc.P(0.0, 0.0))])
    return fc.Edge(
        "hem",
        [fc.Bezier(HEM_OUT,
                   fc.P(HEM_HALF * 0.58, -train_length * 0.12),
                   fc.P(HEM_HALF * 0.30, -train_length * 0.72),
                   CB_HEM)],
    )


def _front():
    top_y = HPS_Y - front_drop
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        _neck_edge(front_drop),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        _front_hem(),
    ]
    # Side-bust dart, internal only. Legs sit on the fitted vertical run; the
    # fold-mirror cut yields one dart per physical side.
    y_d = BUST_PT.y + BUST_DROP / 2.0
    half = bust_dart_intake / 2.0
    dart = fc.Internal(
        "side bust dart",
        [fc.P(W, y_d + half), fc.P(W - DART_LEN, y_d), fc.P(W, y_d - half)],
        kind="dart",
    )
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("side", 0.0, "hip match")],
        grainline=_grainline(),
        internals=[dart] if bust_dart_intake > 0.5 else [],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Gown Front (bias, cut on fold)",
    )


def _back():
    cb_top = HPS_Y - back_drop
    # CB seam runs from the (possibly dropped) CB hem point up to the low back.
    center = fc.Edge("center", [fc.Line(CB_HEM, fc.P(0.0, cb_top))])
    edges = [
        center,
        _neck_edge(back_drop),
        _shoulder_edge(),
        _armhole_edge(),
        _side_edge(),
        _back_hem(),
    ]
    # One fisheye (lens) waist dart per panel; the cut-2 pair gives the classic
    # two back waist darts. Widest at the waist line, kept below the bust.
    cx = max(60.0, min(waist_girth / 8.0, W - 40.0))
    top = min(WAIST_Y + FISHEYE_LEN / 2.0, BUST_PT.y - 15.0)
    bot = max(top - FISHEYE_LEN, HIP_Y + 20.0)
    mid = (top + bot) / 2.0
    half = FISHEYE_INTAKE / 2.0
    fisheye = fc.Internal(
        "back fisheye dart",
        [fc.P(cx, top), fc.P(cx - half, mid), fc.P(cx, bot),
         fc.P(cx + half, mid), fc.P(cx, top)],
        kind="dart",
    )
    # Invisible zipper spans zipper_length from the low back DOWN the CB seam.
    # `center` is authored hem -> back-neck, so the stop sits at authored
    # fraction 1 - zipper_length / |center|. A side zip moves the notch to the
    # side seam instead (noted in the BOM), leaving the CB a plain seam.
    notches = [fc.Notch("side", 0.5, "side match"), fc.Notch("side", 0.0, "hip match")]
    cb_len = center.length()
    if zip_placement == "center_back" and cb_len > 1.0:
        notches.append(fc.Notch("center", 1.0 - min(zipper_length / cb_len, 0.98), "zipper stop"))
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 20.0},  # CB seam carries the zipper
        notches=notches,
        grainline=_grainline(),
        internals=[fisheye],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Gown Back (bias, CB seam + zip)",
    )


def _facing(name, opening_len, quantity, label):
    """Straight facing strip: measured opening + 2 sa ends, 2x depth tall."""
    length = opening_len + 2.0 * seam_allowance
    h = 2.0 * FACING_DEPTH
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, h))]),
        fc.Edge("top", [fc.Line(fc.P(length, h), fc.P(0.0, h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, h / 2.0), fc.P(length * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("evening-gown")
    front = _front()
    back = _back()
    want_body = target_piece in ("front", "back", "set")
    want_face = target_piece in ("facings", "set")
    if not (want_body or want_face):
        want_body = want_face = True
    if want_body and target_piece in ("front", "set"):
        pattern.add(front)
    if want_body and target_piece in ("back", "set"):
        pattern.add(back)
    if want_face:
        # Physical neck opening: front is cut on fold (its drafted half-neck
        # sews in twice); back is cut 2 (its drafted neck also appears twice).
        neck_opening = 2.0 * (front.edge("neck").length() + back.edge("neck").length())
        # Each armhole = one front scoop + one back scoop; cut 2 (one per side).
        armhole_opening = front.edge("armhole").length() + back.edge("armhole").length()
        pattern.add(_facing("neck_facing", neck_opening, 1, "Neck Facing"))
        pattern.add(_facing("armhole_facing", armhole_opening, 2, "Armhole Facing"))
    have = {piece.name for piece in pattern.pieces}
    if {"front", "back"} <= have:
        # Shared shoulder + side geometry: identical construction both panels,
        # so the declared seams pass by construction and any drift breaks it.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)

    # ── Bill of materials ─────────────────────────────────────────────────────
    # Fabric estimate: floor length + train, cut single-layer on the bias, needs
    # a generous open width. Shell then a full lining cut from the same pieces.
    shell_len_mm = dress_length + train_length + hem_allowance + 120.0
    shell_m = round(shell_len_mm / 1000.0 * 2.2, 2)  # ~2.2 lengths for bias single-layer
    lining_m = round(shell_len_mm / 1000.0 * 2.0, 2)
    zip_where = "center back" if zip_placement == "center_back" else "left side seam"
    zip_seam = "CB seam" if zip_placement == "center_back" else "left side seam"
    pattern.bom = [
        {"item": "shell fabric (silk crepe/satin/chiffon; poplin stand-in)",
         "qty": shell_m, "unit": "m",
         "note": "~1.4 m goods; cut SINGLE LAYER on the true bias (45 deg grainline). "
                 "Generous for floor length + train; let bias-cut panels HANG 24 h "
                 "before the final hem so the grain settles."},
        {"item": "lining / underlining (silk habotai or acetate)",
         "qty": lining_m, "unit": "m",
         "note": "fully lined — a bias shell needs a lining to hang true; cut the "
                 "lining from the front + back body pieces (not re-drafted). Line to "
                 "the floor; the train may be self-faced or lined to match."},
        {"item": f"invisible zipper ({zip_where})",
         "qty": 1, "unit": "pc",
         "note": f"invisible zip ~{round(zipper_length)} mm at the {zip_seam} marked "
                 "notch; HARDWARE is a Yantra4D cartridge reference (zipper-notion / "
                 "notion.hardware_ref: yantra4d/invisible-zip) — tape geometry only "
                 "here, slider/pull not re-implemented."},
        {"item": "hook & eye (above the zipper top stop)",
         "qty": 1, "unit": "pc",
         "note": "one hook & eye closes the seam above the zipper stop; hard goods "
                 "federate to a Yantra4D notion cartridge, never re-drafted here."},
        {"item": "fusible interfacing (neck + armhole facings)",
         "qty": 0.3, "unit": "m",
         "note": "light fusible on the derived neck/armhole facing strips."},
        {"item": "matching thread", "qty": 1, "unit": "spool",
         "note": "fine thread for bias seams; staystitch curved edges before assembly."},
    ]

    pattern.metadata = {
        "fc100_rank": 72,
        "fabric_hint": "popelina-algodon",
        "silhouette": silhouette,
        "zip_placement": zip_placement,
        "bias_cut": True,
        "bias_note": "body panels cut on the TRUE bias — grainline drawn at exactly "
                     "45 deg; hang 24 h before hemming",
        "lined": True,
        "low_back": True,
        "back_drop_mm": round(back_drop, 1),
        "train_length_mm": round(train_length, 1),
        "bust_quarter_mm": round(W, 1),
        "hip_quarter_mm": round(HIPW, 1),
        "hem_half_mm": round(HEM_HALF, 1),
        "side_seam_mm": round(front.edge("side").length(), 1),
        "back_hem_mm": round(back.edge("hem").length(), 1),
        "front_hem_mm": round(front.edge("hem").length(), 1),
        "zipper_length_mm": round(zipper_length, 1),
        "drafting": "a-line-dress lineage taken to the floor and cut on the bias: "
                    "shared shoulder/side seams (delta 0 by construction), internal "
                    "side-bust + back fisheye darts, CB (or side) invisible zip, a "
                    "train that drops only the back hem, fully lined. Teaching-grade: "
                    "darts not rotated into the outline; bias behaviour drawn, not draped.",
    }
    return pattern


result = build()
