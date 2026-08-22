"""
Elizabethan Doublet — Fashion Cabinet Costume Cartridge (FC-300 rank #269, y4d button bridged).

A man's doublet of the later 16th century, c. 1570–1600, drafted on period tailoring logic.
The doublet is the fitted upper garment worn over the shirt: close through the body, buttoned
edge-to-edge up the centre front, with a stiffened front that in the fashionable extreme
becomes the PEASCOD — a belly padded and shaped to a point that overhangs the waist.

The documented construction this draft reproduces:

  - front and back cut close, with the shaping taken at the SIDE and back seams rather than
    by modern bust/waist darts;
  - a centre-front closure buttoned EDGE TO EDGE with many small closely-spaced buttons —
    no lapped placket, no facing extension, because the two fronts meet rather than overlap;
  - the peascod belly: the CF edge is drafted with a forward bow below the chest, and the
    interlining is padded to hold it. `peascod_bow` at zero gives the plainer earlier doublet;
  - SKIRTS (short tabs, called "bases" or skirts) set on around the waist below the seam;
  - a standing COLLAR band carrying the ruff or falling band;
  - a two-piece sleeve set into a high, small armscye with the cap eased in.

Drafting note — the seam that must SOLVE. A set-in sleeve is the honest test of a bodice
draft: the sleeve cap must equal the armscye it sews into, PLUS a declared ease that is
worked in over the cap. This cartridge does not assume a cap curve and hope. It builds the
front and back armholes, MEASURES their combined length off the built polygons, and then
solves the sleeve cap's bulge factor by bisection until the cap's measured length equals the
measured armscye plus the requested ease. The residual is reported in the metadata.

Pieces:
  - front   : doublet front (cut 2, mirrored) — CF button stand, peascod bow, armhole.
  - back    : doublet back (cut 2, mirrored) — CB seam, armhole.
  - sleeve  : one-piece sleeve with a solved cap (cut 2, mirrored).
  - skirt   : waist tab / base (cut as a run around the waist).
  - collar  : standing collar band (cut 1 on fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|skirt|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 860.0))
back_length = float(PARAM(lambda: back_length, 430.0))   # nape to waist
shoulder_width = float(PARAM(lambda: shoulder_width, 145.0))  # neck to shoulder point
sleeve_length = float(PARAM(lambda: sleeve_length, 620.0))
peascod_bow = float(PARAM(lambda: peascod_bow, 38.0))    # forward bow of the CF belly; 0 = plain
skirt_depth = float(PARAM(lambda: skirt_depth, 95.0))    # depth of the waist tabs
collar_height = float(PARAM(lambda: collar_height, 55.0))
button_pitch = float(PARAM(lambda: button_pitch, 28.0))  # CF button spacing
sleeve_ease = float(PARAM(lambda: sleeve_ease, 22.0))    # ease worked into the cap
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane doublet ranges) ─────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1400.0))
waist_girth = max(620.0, min(waist_girth, 1350.0))
back_length = max(330.0, min(back_length, 540.0))
shoulder_width = max(100.0, min(shoulder_width, 200.0))
sleeve_length = max(450.0, min(sleeve_length, 780.0))
peascod_bow = max(0.0, min(peascod_bow, 90.0))
skirt_depth = max(40.0, min(skirt_depth, 180.0))
collar_height = max(25.0, min(collar_height, 95.0))
button_pitch = max(14.0, min(button_pitch, 55.0))
sleeve_ease = max(0.0, min(sleeve_ease, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = back_length
# Quarter measures: the doublet is close-fitting, so ease is small and period-plausible.
CHEST_Q = (chest_girth + 60.0) / 4.0     # 60 mm total wearing ease over the shirt
WAIST_Q = (waist_girth + 40.0) / 4.0
ARMHOLE_DEPTH = L * 0.46                 # high, small armscye — the period cut
CURVE_N = 20                             # polyline resolution of the armhole curves


def _bez_pts(p0, p1, bulge, side, n=CURVE_N):
    """Flattened points of a `curve_through` bezier — used where a curve must be MEASURED."""
    return fc.curve_through(p0, p1, bulge, side).flatten(0.2)


def _front_armhole_segs():
    """The front armhole: shoulder point down to the underarm, hollowed forward."""
    shoulder_pt = fc.P(shoulder_width, L)
    underarm = fc.P(CHEST_Q, L - ARMHOLE_DEPTH)
    return [fc.curve_through(shoulder_pt, underarm, 0.20, -1.0)]


def _back_armhole_segs():
    """The back armhole: shallower than the front, as the shoulder blade needs room."""
    shoulder_pt = fc.P(shoulder_width, L)
    underarm = fc.P(CHEST_Q, L - ARMHOLE_DEPTH)
    return [fc.curve_through(shoulder_pt, underarm, 0.12, -1.0)]


def build_front():
    """Doublet front (cut 2, mirrored). CF is a butt edge — the fronts meet, not overlap."""
    # CF runs bottom (waist) to top (neck). The peascod bows the belly FORWARD, which in
    # this flat draft means the CF edge swings out below the chest and returns at the waist.
    chest_y = L - ARMHOLE_DEPTH
    cf_segs = [
        # waist up to the belly point, bowing forward by peascod_bow
        fc.curve_through(fc.P(0.0, 0.0), fc.P(0.0, chest_y), peascod_bow / max(chest_y, 1.0), -1.0),
        # belly point up to the neck, straight
        fc.Line(fc.P(0.0, chest_y), fc.P(0.0, L)),
    ]
    neck_w = shoulder_width * 0.40
    edges = [
        fc.Edge("cf", cf_segs),
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, L), fc.P(neck_w, L + 18.0), 0.18, -1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_w, L + 18.0), fc.P(shoulder_width, L))]),
        fc.Edge("armhole", _front_armhole_segs()),
        fc.Edge("side", [fc.Line(fc.P(CHEST_Q, L - ARMHOLE_DEPTH), fc.P(WAIST_Q, 0.0))]),
        fc.Edge("waist", [fc.Line(fc.P(WAIST_Q, 0.0), fc.P(0.0, 0.0))]),
    ]
    n_buttons = max(4, int((L - 30.0) / button_pitch))
    internals = [fc.Internal("peascod-padding",
                             [fc.P(6.0, 10.0), fc.P(CHEST_Q * 0.55, chest_y)], kind="marking")]
    for i in range(n_buttons):
        y = 15.0 + i * button_pitch
        if y < L - 10.0:
            internals.append(fc.Internal("button", [fc.P(9.0, y), fc.P(9.0, y + 1.0)],
                                         kind="drill"))
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"cf": 16.0, "neck": 8.0},
        notches=[fc.Notch("armhole", 0.5, "front armhole balance"),
                 fc.Notch("side", 0.5, "side seam balance")],
        grainline=fc.Grainline(fc.P(CHEST_Q * 0.4, 26.0), fc.P(CHEST_Q * 0.4, L - 26.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 mirrored, butt-buttoned CF)",
    )


def build_back():
    """Doublet back (cut 2, mirrored). Shaping is at the CB and side seams, not in darts.

    The back neck is drafted WIDER and shallower than the front (the period cut: the
    front neck scoops, the back sits high across the nape). That would leave the back
    shoulder shorter than the front's, so the back neck point's height is SOLVED — not
    guessed — to make the two shoulder seams equal, which is what actually gets sewn.
    """
    neck_w = shoulder_width * 0.46
    # Front shoulder runs (0.40*sw, L+18) -> (sw, L); solve the back neck point height
    # `ny` so that the back shoulder (neck_w, ny) -> (sw, L) has the SAME length.
    front_shoulder_len = FRONT_SHOULDER_LEN
    dx_back = shoulder_width - neck_w
    if front_shoulder_len > dx_back:
        ny = L + math.sqrt(front_shoulder_len ** 2 - dx_back ** 2)
    else:
        # Degenerate: the back neck is so wide there is no rise that can match the front.
        # Fall back to a flat shoulder and let the declared seam report the truth.
        ny = L
    edges = [
        fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, L), fc.P(neck_w, ny), 0.10, -1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_w, ny), fc.P(shoulder_width, L))]),
        fc.Edge("armhole", _back_armhole_segs()),
        fc.Edge("side", [fc.Line(fc.P(CHEST_Q, L - ARMHOLE_DEPTH), fc.P(WAIST_Q, 0.0))]),
        fc.Edge("waist", [fc.Line(fc.P(WAIST_Q, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"cb": 14.0, "neck": 8.0},
        notches=[fc.Notch("armhole", 0.5, "back armhole balance"),
                 fc.Notch("side", 0.5, "side seam balance")],
        grainline=fc.Grainline(fc.P(CHEST_Q * 0.4, 26.0), fc.P(CHEST_Q * 0.4, L - 26.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2 mirrored)",
    )


# Build the bodice first so the armscye can be MEASURED before the sleeve is drafted.
FRONT = build_front()
# The front shoulder is the reference the back shoulder is solved against.
FRONT_SHOULDER_LEN = FRONT.edge("shoulder").length()
BACK = build_back()
ARMSCYE = FRONT.edge("armhole").length() + BACK.edge("armhole").length()
CAP_TARGET = ARMSCYE + sleeve_ease   # what the sleeve cap must measure


def _cap_length(bulge, cap_w, cap_h):
    """Measured length of a two-lobe sleeve cap at the given bulge factor.

    The cap is the classic S: hollowed on the front half, full on the back half.
    """
    left = _bez_pts(fc.P(0.0, 0.0), fc.P(cap_w * 0.5, cap_h), bulge * 0.55, 1.0)
    right = _bez_pts(fc.P(cap_w * 0.5, cap_h), fc.P(cap_w, 0.0), bulge, 1.0)
    return fc.polyline_length(left) + fc.polyline_length(right)


def _solve_cap_bulge(cap_w, cap_h):
    """Bisect the cap's bulge factor until the MEASURED cap equals CAP_TARGET.

    This is the honest way round: the armscye is a fixed measured quantity, and the cap
    is solved to match it, rather than both being computed from a formula and hoped to agree.
    """
    lo, hi = 0.0, 3.0
    if _cap_length(hi, cap_w, cap_h) < CAP_TARGET:
        return hi, _cap_length(hi, cap_w, cap_h)
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _cap_length(mid, cap_w, cap_h) < CAP_TARGET:
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2.0
    return b, _cap_length(b, cap_w, cap_h)


# Cap geometry: width is the biceps line, height the cap rise. Both period-plausible
# for a high small armscye; the bulge is then SOLVED against the measured armscye.
CAP_W = ARMSCYE * 0.62
CAP_H = ARMHOLE_DEPTH * 0.72
CAP_BULGE, CAP_MEASURED = _solve_cap_bulge(CAP_W, CAP_H)


def build_sleeve():
    """One-piece sleeve with the SOLVED cap (cut 2, mirrored).

    The cap's two lobes are drafted at the solved bulge, so `cap` measures the armscye
    plus the declared ease. The sleeve tapers to the wrist, as the period sleeve does.
    """
    wrist_w = CAP_W * 0.52
    ln = sleeve_length
    inset = (CAP_W - wrist_w) / 2.0
    cap_segs = [
        fc.curve_through(fc.P(0.0, 0.0), fc.P(CAP_W * 0.5, CAP_H), CAP_BULGE * 0.55, 1.0),
        fc.curve_through(fc.P(CAP_W * 0.5, CAP_H), fc.P(CAP_W, 0.0), CAP_BULGE, 1.0),
    ]
    edges = [
        # underarm seam down the back side
        fc.Edge("under_b", [fc.Line(fc.P(CAP_W, 0.0), fc.P(CAP_W - inset, -ln))]),
        fc.Edge("wrist", [fc.Line(fc.P(CAP_W - inset, -ln), fc.P(inset, -ln))]),
        fc.Edge("under_f", [fc.Line(fc.P(inset, -ln), fc.P(0.0, 0.0))]),
        fc.Edge("cap", cap_segs),
    ]
    return fc.Piece(
        "sleeve",
        edges,
        seam_allowance=seam_allowance,
        allowances={"wrist": 10.0},
        notches=[fc.Notch("cap", 0.25, "front cap notch"),
                 fc.Notch("cap", 0.75, "back cap notch (double)")],
        grainline=fc.Grainline(fc.P(CAP_W * 0.5, -20.0), fc.P(CAP_W * 0.5, -ln + 20.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2 mirrored, solved cap)",
    )


def build_skirt():
    """A waist tab ("base" / skirt) set on below the waist seam, cut as a run.

    Period doublet skirts are a run of short tabs; this drafts the run as one piece
    whose top edge equals the front+back waist it is set to.
    """
    run = (FRONT.edge("waist").length() + BACK.edge("waist").length())
    d = skirt_depth
    internals = []
    # Tab divisions: the run is slashed into tabs after it is set on.
    n_tabs = max(3, int(run / 70.0))
    for i in range(1, n_tabs):
        x = run * i / n_tabs
        internals.append(fc.Internal("tab-division", [fc.P(x, 0.0), fc.P(x, d * 0.85)],
                                     kind="trace"))
    return fc.Piece(
        "skirt",
        [
            fc.Edge("waist_seam", [fc.Line(fc.P(0.0, d), fc.P(run, d))]),
            fc.Edge("end_b", [fc.Line(fc.P(run, d), fc.P(run, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(run, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("end_f", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, d))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 8.0},
        notches=[fc.Notch("waist_seam", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(run * 0.2, d * 0.5), fc.P(run * 0.8, d * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Waist skirt / base run (cut 2 mirrored)",
    )


def build_collar():
    """Standing collar band, cut on the fold at CB. Carries the ruff or falling band."""
    run = FRONT.edge("neck").length() + BACK.edge("neck").length()
    h = collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(run, h))]),
            fc.Edge("cf_end", [fc.Line(fc.P(run, h), fc.P(run, 0.0))]),
            fc.Edge("neck_seam", [fc.Line(fc.P(run, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": 0.0},
        notches=[fc.Notch("neck_seam", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(run * 0.2, h * 0.5), fc.P(run * 0.8, h * 0.5)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb"),
        label="Standing collar (cut 1 on fold)",
    )


def build():
    pattern = fc.PatternSet("elizabethan-doublet")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(FRONT)
    if everything or target_piece == "back":
        pattern.add(BACK)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "skirt":
        pattern.add(build_skirt())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The set-in sleeve: cap = front armhole + back armhole, plus the declared ease.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.5, ease=sleeve_ease)
        # Side seam and shoulder both balance by construction (shared points).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # The skirt run is set to the front+back waist.
        pattern.declare_seam(("skirt", "waist_seam"),
                             [("front", "waist"), ("back", "waist")], tol=1.5)
        # The collar band is set to the front+back neckline.
        pattern.declare_seam(("collar", "neck_seam"),
                             [("front", "neck"), ("back", "neck")], tol=1.5)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    n_buttons = max(4, int((L - 30.0) / button_pitch))
    pattern.bom = [
        {"item": "wool broadcloth or silk (+ linen interlining + lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1200 mm width, 68% marker. A period doublet is a three-layer "
                 "structure: fashion fabric, a linen interlining that carries the shape, "
                 "and a lining. The stiffness is in the interlining, not in fusible."},
        {"item": "buttons (Yantra4D sew-through-button)", "qty": n_buttons, "unit": "count",
         "note": f"{n_buttons} at {button_pitch:.0f} mm pitch up the centre front. Period "
                 f"doublets butt-button EDGE TO EDGE with many small buttons — worked "
                 f"thread loops or eyelets oppose them, not a modern buttonhole in a lap."},
        {"item": "padding / bombast for the peascod",
         "qty": 1 if peascod_bow > 0.0 else 0, "unit": "set",
         "note": "wool or cotton wadding quilted into the front interlining on the marked "
                 "line, to hold the belly. Zero at peascod_bow = 0 (the plainer doublet)."},
        {"item": "linen thread + buttonhole silk", "qty": 1, "unit": "set",
         "note": "the CF edge and every tab edge are finished by hand."},
    ]
    pattern.metadata = {
        "fc300_rank": 269,
        "family": "costume_historical",
        "period": "c. 1570–1600 (later Elizabethan)",
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "Close through the body with a high, small armscye and a stiffened "
            "front. At peascod_bow > 0 the belly bows forward to a point over the waist — the "
            "fashionable late-Tudor extreme; at 0 it is the plainer earlier doublet.",
        "construction_note": "Shaping is taken at the side and back seams, not in modern "
            "darts. The centre front BUTTS and buttons edge to edge rather than lapping.",
        "hardware": "buttons via Yantra4D (notion.hardware_ref -> sew-through-button); the "
            "CF button pitch drives hole_spacing — the dimensional handshake.",
        "solved": {
            "armscye_measured_mm": round(ARMSCYE, 2),
            "cap_target_mm": round(CAP_TARGET, 2),
            "cap_measured_mm": round(CAP_MEASURED, 2),
            "cap_residual_mm": round(CAP_MEASURED - CAP_TARGET, 4),
            "cap_bulge_solved": round(CAP_BULGE, 5),
            "sleeve_ease_mm": round(sleeve_ease, 1),
            "note": "the armscye is MEASURED off the built front and back armhole curves; "
                    "the sleeve cap's bulge is then solved by bisection until the cap's "
                    "measured length equals that armscye plus the declared ease. Neither "
                    "side is a formula hoping to agree with the other.",
        },
    }
    return pattern


result = build()
