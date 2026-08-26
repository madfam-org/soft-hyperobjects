"""
Pullover Anorak Smock — Fashion Cabinet Garment Cartridge
(FC-400 rank #379, outerwear, Yantra4D-bridged cord-lock).

A ventile-cotton pullover anorak: no full-length zip, just a short neck placket you pull over
the head, a big kangaroo POCKET across the front, a two-panel HOOD, and a drawcord hem cinched
on a cord-lock. Cut generous as a smock over a jumper, in the tight-woven cotton that beads
rain without a coating. The cord-lock is the Yantra4D `cord-lock` solid (notion.hardware_ref);
its channel is bored for the same cord_dia the hem casing carries.

Drafting note — the seam that must SOLVE: a pullover front is cut on the fold, so its neck
placket is a SLIT, not a seam — the slit length is a fixed fraction of the neck depth, clamped
so it never runs past the chest. The kangaroo pocket's mouth angle must land on the front
symmetrically about centre front; its opening is derived from the front width so a wide body
gets a proportionate pocket, not a fixed one that looks lost. The hood is cut to the measured
neckline and the sleeve cap bisected against the measured armholes.

Pieces:
  - front  : anorak front (cut 1 on fold); neck-placket slit, pocket line marked.
  - back   : anorak back (cut 1 on fold).
  - sleeve : one-piece sleeve (cut 2 mirrored).
  - hood   : hood half (cut 2 mirrored).
  - pocket : kangaroo pocket (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|hood|pocket|set

chest_girth = float(PARAM(lambda: chest_girth, 1080.0))
smock_length = float(PARAM(lambda: smock_length, 720.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 470.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 630.0))
neck_girth = float(PARAM(lambda: neck_girth, 430.0))
cord_dia = float(PARAM(lambda: cord_dia, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(840.0, min(chest_girth, 1540.0))
smock_length = max(580.0, min(smock_length, 900.0))
shoulder_width = max(380.0, min(shoulder_width, 620.0))
sleeve_length = max(320.0, min(sleeve_length, 720.0))
neck_girth = max(340.0, min(neck_girth, 560.0))
cord_dia = max(3.0, min(cord_dia, 8.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

EASE = 260.0                                 # a smock over a jumper
HALF_CHEST = (chest_girth + EASE) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 12.0
NECK_DROP_F = neck_girth / 6.0 + 20.0
NECK_DROP_B = 26.0
ARMHOLE_DROP = 300.0
SHOULDER_SLOPE = 42.0
CASING_H = max(20.0, cord_dia * 4.0 + 12.0)
# Neck-placket slit: a fraction of the neck drop, clamped inside the chest.
PLACKET_SLIT = min(NECK_DROP_F * 1.6, smock_length * 0.28)


def build_front():
    """Anorak front (cut 1 on fold at CF). The neck-placket is a marked SLIT, not a
    seam. The kangaroo pocket mouth is marked, sized from the front width."""
    h = smock_length
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, h - NECK_DROP_F - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, h - NECK_DROP_F - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, h - NECK_DROP_F)
    p_neck_cf = fc.P(0.0, h - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 8.0,
                                           h - NECK_DROP_F - ARMHOLE_DROP * 0.4),
                                      fc.P(HALF_SHOULDER + 16.0,
                                           h - NECK_DROP_F - SHOULDER_SLOPE - 50.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.5, h - NECK_DROP_F - 8.0),
                                   fc.P(14.0, h - NECK_DROP_F), p_neck_cf)]),
        fc.Edge("cf_fold", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    pk_top = HALF_CHEST * 0.72
    pk_y = h - NECK_DROP_F - ARMHOLE_DROP - 40.0
    pk_y = max(pk_y, CASING_H + 120.0)
    internals = [
        fc.Internal("placket-slit",
                    [fc.P(0.0, h - NECK_DROP_F), fc.P(0.0, h - NECK_DROP_F - PLACKET_SLIT)],
                    kind="marking"),
        fc.Internal("hem-casing", [fc.P(0.0, CASING_H), fc.P(HALF_CHEST, CASING_H)],
                    kind="marking"),
        fc.Internal("pocket-mouth",
                    [fc.P(pk_top, pk_y + 60.0), fc.P(pk_top * 0.4, pk_y)], kind="marking"),
    ]
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"cf_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap front match")],
        grainline=fc.Grainline(fc.P(HALF_CHEST * 0.5, 60.0),
                               fc.P(HALF_CHEST * 0.5, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf_fold"),
        label="Anorak Front (pullover)",
    )


# ── Back neck width solved from front's measured shoulder ────────────────────
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_dy = SHOULDER_SLOPE + (NECK_DROP_F - NECK_DROP_B) - SHOULDER_SLOPE * 0.10
if _SHOULDER_LEN <= abs(_dy):
    _dy = _SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))
BACK_NECK_Y = _dy - SHOULDER_SLOPE


def build_back():
    h = smock_length
    top = h - NECK_DROP_F
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST, 0.0)
    p_side_top = fc.P(HALF_CHEST, top - ARMHOLE_DROP)
    p_shoulder = fc.P(HALF_SHOULDER, top - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, top + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, top + BACK_NECK_Y + 6.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0, top - ARMHOLE_DROP * 0.42),
                                      fc.P(HALF_SHOULDER + 14.0,
                                           top - SHOULDER_SLOPE - 44.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("armhole", 0.55, "sleeve cap back match")],
        grainline=None,
        internals=[fc.Internal("hem-casing", [fc.P(0.0, CASING_H), fc.P(HALF_CHEST, CASING_H)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Anorak Back",
    )


# ── Sleeve cap solved against MEASURED armholes ──────────────────────────────
_F = build_front()
_B = build_back()
ARMHOLE_F = _F.edge("armhole").length(0.2)
ARMHOLE_B = _B.edge("armhole").length(0.2)
CAP_EASE = 16.0
CAP_TARGET = ARMHOLE_F + ARMHOLE_B + CAP_EASE
BICEPS = max(400.0, (ARMHOLE_F + ARMHOLE_B) * 0.80)


def _cap_segments(cap_h, top_y):
    half = BICEPS / 2.0
    p_l = fc.P(-half, top_y - cap_h)
    p_top = fc.P(0.0, top_y)
    p_r = fc.P(half, top_y - cap_h)
    return [
        fc.Bezier(p_l, fc.P(-half * 0.72, top_y - cap_h * 0.94),
                  fc.P(-half * 0.34, top_y - cap_h * 0.06), p_top),
        fc.Bezier(p_top, fc.P(half * 0.34, top_y - cap_h * 0.06),
                  fc.P(half * 0.72, top_y - cap_h * 0.94), p_r),
    ]


def _solve_cap():
    lo, hi = 20.0, BICEPS * 0.95
    def f(ch):
        return sum(s.length(0.2) for s in _cap_segments(ch, 0.0)) - CAP_TARGET
    f_lo, f_hi = f(lo), f(hi)
    if f_lo * f_hi > 0.0:
        return lo if abs(f_lo) < abs(f_hi) else hi
    for _ in range(80):
        mid = (lo + hi) / 2.0
        f_mid = f(mid)
        if abs(f_mid) < 0.02:
            return mid
        if f_lo * f_mid <= 0.0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


CAP_H = _solve_cap()


def build_sleeve():
    half = BICEPS / 2.0
    cuff_half = max(100.0, half * 0.6)
    top_y = max(sleeve_length, CAP_H + 60.0)
    cap = _cap_segments(CAP_H, top_y)
    p_l = fc.P(-half, top_y - CAP_H)
    p_r = fc.P(half, top_y - CAP_H)
    edges = [
        fc.Edge("cap", cap),
        fc.Edge("under_r", [fc.Line(p_r, fc.P(cuff_half, 0.0))]),
        fc.Edge("cuff", [fc.Line(fc.P(cuff_half, 0.0), fc.P(-cuff_half, 0.0))]),
        fc.Edge("under_l", [fc.Line(fc.P(-cuff_half, 0.0), p_l)]),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 28.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.25, "front cap match"),
                 fc.Notch("cap", 0.75, "back cap match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, top_y - 30.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


# ── Hood, neck edge = MEASURED half neckline ─────────────────────────────────
_NECK_HALF_RUN = _F.edge("neck").length(0.2) + _B.edge("neck").length(0.2)


def build_hood():
    neck_run = _NECK_HALF_RUN
    hood_h = max(300.0, neck_run * 1.4)
    hood_w = max(240.0, neck_run * 1.05)
    p_neck_front = fc.P(0.0, 0.0)
    p_neck_back = fc.P(neck_run, 0.0)
    p_crown = fc.P(neck_run + 20.0, hood_h)
    p_face_top = fc.P(-hood_w * 0.15, hood_h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p_neck_front, p_neck_back)]),
        fc.Edge("centre_back", [fc.Bezier(p_neck_back,
                                          fc.P(neck_run + hood_w * 0.3, hood_h * 0.5),
                                          fc.P(neck_run + hood_w * 0.1, hood_h * 0.9),
                                          p_crown)]),
        fc.Edge("crown", [fc.Line(p_crown, p_face_top)]),
        fc.Edge("face", [fc.Bezier(p_face_top,
                                   fc.P(-hood_w * 0.2, hood_h * 0.55),
                                   fc.P(-hood_w * 0.05, hood_h * 0.2), p_neck_front)]),
    ]
    return fc.Piece(
        "hood", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(neck_run * 0.5, 20.0), fc.P(neck_run * 0.5, hood_h - 20.0)),
        internals=[fc.Internal("face-casing",
                               [fc.P(-hood_w * 0.1, hood_h - CASING_H), fc.P(0.0, CASING_H)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Hood half",
    )


POCKET_W = max(200.0, HALF_CHEST * 1.3)
POCKET_H = max(160.0, smock_length * 0.26)


def build_pocket():
    """The kangaroo pocket: a wide panel with two slanted hand openings, sized from
    the front width so a wide body gets a proportionate pocket."""
    w, h = POCKET_W, POCKET_H
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("hand-slit-r",
                    [fc.P(w * 0.72, h), fc.P(w * 0.88, h * 0.4)], kind="marking"),
        fc.Internal("hand-slit-l",
                    [fc.P(w * 0.28, h), fc.P(w * 0.12, h * 0.4)], kind="marking"),
    ]
    return fc.Piece(
        "pocket", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(w * 0.5, 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Kangaroo pocket",
    )


def build():
    pattern = fc.PatternSet("anorak-smock")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "hood":
        pattern.add(build_hood())
    if everything or target_piece == "pocket":
        pattern.add(build_pocket())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=CAP_EASE)
        pattern.declare_seam(("hood", "centre_back"), ("hood", "centre_back"), tol=1.0)
        pattern.declare_seam([("hood", "neck_edge"), ("hood", "neck_edge")],
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "ventile cotton (tight-woven)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; ventile beads rain by swelling its own "
                 "fibres — no coating to crack, so the anorak breathes."},
        {"item": "cord lock", "qty": 1, "unit": "count",
         "note": f"Yantra4D cord-lock (notion.hardware_ref): at the hem; the channel is "
                 f"bored for {cord_dia:.1f} mm cord."},
        {"item": "drawcord", "qty": round(HALF_CHEST * 4.0 + 400.0), "unit": "mm_length",
         "note": f"{cord_dia:.1f} mm; threads the hem casing."},
        {"item": "short neck zip or buttons", "qty": 1, "unit": "count",
         "note": f"closes the {PLACKET_SLIT:.0f} mm neck placket you pull over the head."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "flat-fell the side seams for a weatherproof pullover."},
    ]
    pattern.metadata = {
        "fc400_rank": 379,
        "family": "outerwear",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(smock_length, 1),
                        "placket_slit": round(PLACKET_SLIT, 1)},
        "solved": {
            "placket_slit_mm": round(PLACKET_SLIT, 2),
            "pocket_width_mm": round(POCKET_W, 2),
            "cap_height_mm": round(CAP_H, 2),
            "neck_half_run_mm": round(_NECK_HALF_RUN, 2),
            "note": "the pullover front is cut on the fold, so its neck placket is a SLIT "
                    "(clamped under 28% of the length so it never runs past the chest); the "
                    "kangaroo pocket width is derived from the front width so a wide body "
                    "gets a proportionate pocket; the hood is cut to the measured neckline "
                    "and the sleeve cap bisected against the measured armholes.",
        },
        "hardware": "drawcord cord-lock via Yantra4D (notion.hardware_ref -> cord-lock); "
                    "cord_dia = cord_dia.",
    }
    return pattern


result = build()
