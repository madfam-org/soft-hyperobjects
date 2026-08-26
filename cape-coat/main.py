"""
A-line Cape Coat — Fashion Cabinet Garment Cartridge
(FC-400 rank #378, outerwear, Yantra4D-bridged toggle).

A wool-melton cape coat with no set sleeves: the body flares from the shoulder to a wide
A-line sweep that drapes over the arms, with vertical arm slits so the hands come through, a
stand collar, and a row of toggle-and-loop closures down the front. The toggle is the Yantra4D
`toggle` solid (notion.hardware_ref); its barrel length is driven by the same toggle_len the
cape's frog loops are cut for.

Drafting note — the seam that must SOLVE: an A-line flare means the hem is much wider than the
shoulder, and the side seam is NOT vertical — it slants out. The front and back side seams must
still be EQUAL length despite the slant, so the flare is applied symmetrically and the side seam
is drafted from the shoulder point to a hem point offset by a MEASURED flare amount; both panels
use the same flare so the seam matches. The arm-slit position is clamped inside the side seam so
a wide flare cannot push the slit off the panel. The collar is cut to the measured neckline.

Pieces:
  - front  : cape front (cut 2 mirrored); A-line flare, arm slit, toggle placket.
  - back   : cape back (cut 1 on fold); A-line flare.
  - collar : stand collar (cut 2 on fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|collar|set

chest_girth = float(PARAM(lambda: chest_girth, 1040.0))
cape_length = float(PARAM(lambda: cape_length, 900.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 460.0))
hem_flare = float(PARAM(lambda: hem_flare, 260.0))        # extra hem width per side
neck_girth = float(PARAM(lambda: neck_girth, 420.0))
toggle_len = float(PARAM(lambda: toggle_len, 60.0))       # toggle barrel length
toggle_count = float(PARAM(lambda: toggle_count, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(820.0, min(chest_girth, 1520.0))
cape_length = max(640.0, min(cape_length, 1200.0))
shoulder_width = max(360.0, min(shoulder_width, 600.0))
hem_flare = max(80.0, min(hem_flare, 420.0))
neck_girth = max(320.0, min(neck_girth, 540.0))
toggle_len = max(35.0, min(toggle_len, 95.0))
toggle_count = max(2.0, min(round(toggle_count), 7))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

EASE = 200.0
HALF_CHEST = (chest_girth + EASE) / 4.0
HALF_SHOULDER = shoulder_width / 2.0
NECK_W = neck_girth / 6.0 + 12.0
NECK_DROP_F = neck_girth / 6.0 + 22.0
NECK_DROP_B = 26.0
SHOULDER_SLOPE = 46.0
# Arm slit sits partway down the side seam, clamped inside the panel.
ARM_SLIT_TOP = cape_length * 0.62
ARM_SLIT_LEN = min(220.0, cape_length * 0.22)

# ── Solve the toggle column ──────────────────────────────────────────────────
N_TOG = int(toggle_count)
TOP_CLEAR = 70.0
HEM_CLEAR = 120.0
TOG_RUN = cape_length - NECK_DROP_F - TOP_CLEAR - HEM_CLEAR
N_TOG_INT = max(1, N_TOG - 1)
TOG_PITCH = TOG_RUN / N_TOG_INT
TOG_TOP_Y = cape_length - NECK_DROP_F - TOP_CLEAR


def _toggle_ys():
    return [TOG_TOP_Y - TOG_PITCH * i for i in range(N_TOG)]


def build_front():
    """Cape front (cut 2 mirrored). Shoulder at top; the side seam slants out to a hem
    offset by hem_flare (the A-line). Arm slit marked on the side seam."""
    h = cape_length
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST + hem_flare, 0.0)         # flared hem
    p_shoulder = fc.P(HALF_SHOULDER, h - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, h - NECK_DROP_F + SHOULDER_SLOPE)
    p_neck_cf = fc.P(0.0, h - NECK_DROP_F)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_shoulder)]),   # slanted A-line side seam
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W * 0.5, h - NECK_DROP_F + 6.0),
                                   fc.P(14.0, h - NECK_DROP_F + 2.0), p_neck_cf)]),
        fc.Edge("centre_front", [fc.Line(p_neck_cf, p_hem_cf)]),
    ]
    internals = [fc.Internal("arm-slit",
                             [fc.P(HALF_CHEST * 0.5, ARM_SLIT_TOP),
                              fc.P(HALF_CHEST * 0.5, ARM_SLIT_TOP - ARM_SLIT_LEN)],
                             kind="marking")]
    for i, y in enumerate(_toggle_ys()):
        internals.append(fc.Internal(f"toggle-{i + 1}",
                                     [fc.P(0.0, y), fc.P(toggle_len, y)], kind="marking"))
    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "centre_front": 0.0},
        notches=[fc.Notch("side", 0.5, "arm-slit level"),
                 fc.Notch("neck", 0.5, "collar match")],
        grainline=fc.Grainline(fc.P(HALF_CHEST * 0.4, 60.0),
                               fc.P(HALF_CHEST * 0.4, h - NECK_DROP_F - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Cape Front (A-line)",
    )


# Back neck width is solved AFTER the front is built, from its measured shoulder
# (see below); build_back references the resulting NECK_W_BACK global.


def build_back():
    h = cape_length
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_CHEST + hem_flare, 0.0)
    p_shoulder = fc.P(HALF_SHOULDER, h - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, h - NECK_DROP_B)
    p_neck_cb = fc.P(0.0, h - NECK_DROP_B + 4.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.55, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.22, p_neck_cb.y), p_neck_cb)]),
        fc.Edge("cb_fold", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 40.0, "cb_fold": 0.0},
        notches=[fc.Notch("side", 0.5, "arm-slit level"),
                 fc.Notch("neck", 0.5, "collar match")],
        grainline=None,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Cape Back (A-line)",
    )


# Solve back neck width so the back shoulder equals the front's MEASURED shoulder.
_FRONT = build_front()
_FRONT_SHOULDER_LEN = _FRONT.edge("shoulder").length(0.2)
# Back shoulder runs (HALF_SHOULDER, h-SLOPE) -> (NECK_W_BACK, h-NECK_DROP_B).
_dy_back = SHOULDER_SLOPE - NECK_DROP_B
if _FRONT_SHOULDER_LEN <= abs(_dy_back):
    _dy_back = _FRONT_SHOULDER_LEN * 0.85
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_FRONT_SHOULDER_LEN ** 2 - _dy_back ** 2, 1.0))


# ── Collar cut to the MEASURED neckline ──────────────────────────────────────
_BACK = build_back()
_NECK_RUN = 2.0 * _FRONT.edge("neck").length(0.2) + 2.0 * _BACK.edge("neck").length(0.2)


def build_collar():
    """Stand collar (cut 2 on fold), its neck edge = the measured neckline."""
    half = _NECK_RUN / 2.0
    stand_h = 60.0
    p_l_neck = fc.P(-half, 0.0)
    p_r_neck = fc.P(half, 0.0)
    p_r_top = fc.P(half - 6.0, stand_h)
    p_l_top = fc.P(-half + 6.0, stand_h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p_l_neck, p_r_neck)]),
        fc.Edge("end_r", [fc.Line(p_r_neck, p_r_top)]),
        fc.Edge("top", [fc.Line(p_r_top, p_l_top)]),
        fc.Edge("end_l", [fc.Line(p_l_top, p_l_neck)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "centre back"),
                 fc.Notch("neck_edge", 0.25, "shoulder match"),
                 fc.Notch("neck_edge", 0.75, "shoulder match")],
        grainline=fc.Grainline(fc.P(-half * 0.5, 6.0), fc.P(half * 0.5, 6.0)),
        internals=[fc.Internal("roll-line",
                               [fc.P(-half, stand_h * 0.5), fc.P(half, stand_h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Stand collar",
    )


def build():
    pattern = fc.PatternSet("cape-coat")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The A-line side seams: front to back, equal by the shared flare.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # The collar to the measured neckline (front x2, back x2 = on fold).
        pattern.declare_seam(("collar", "neck_edge"),
                             [("front", "neck"), ("front", "neck"),
                              ("back", "neck"), ("back", "neck")], tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "wool melton", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 70% marker (the A-line nests loosely); melton needs "
                 "no hem finish — it does not fray, so the sweep can be cut raw."},
        {"item": "toggle", "qty": N_TOG, "unit": "count",
         "note": f"Yantra4D toggle (notion.hardware_ref): {N_TOG} at a {TOG_PITCH:.1f} mm "
                 f"solved pitch; barrel_len = toggle_len ({toggle_len:.0f} mm)."},
        {"item": "leather or cord frog loops", "qty": N_TOG, "unit": "count",
         "note": "the loop the toggle passes through; cut to the same toggle_len."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "bind the arm-slit edges; they take the strain of the hands coming through."},
    ]
    pattern.metadata = {
        "fc400_rank": 378,
        "family": "outerwear",
        "fabric_hint": "lana-melton-abrigo",
        "finished_mm": {"chest": round(HALF_CHEST * 4.0, 1),
                        "length": round(cape_length, 1),
                        "hem_flare": round(hem_flare, 1)},
        "solved": {
            "toggles": N_TOG,
            "toggle_pitch_mm": round(TOG_PITCH, 2),
            "neck_run_mm": round(_NECK_RUN, 2),
            "front_shoulder_mm": round(_FRONT_SHOULDER_LEN, 2),
            "back_neck_width_mm": round(NECK_W_BACK, 2),
            "arm_slit_top_mm": round(ARM_SLIT_TOP, 2),
            "note": "the A-line side seam slants out to a hem offset by hem_flare; front "
                    "and back share the flare so the slanted side seams stay EQUAL. The "
                    "back neck width is solved from the front's MEASURED shoulder (with "
                    "the flatten clamp); the collar is cut to the measured neckline; the "
                    "toggle pitch is solved so the row lands exactly.",
        },
        "hardware": "toggle-and-loop closure via Yantra4D (notion.hardware_ref -> toggle); "
                    "barrel_len = toggle_len, the same parameter that drives this cape's "
                    "toggle-placket interface (the dimensional handshake).",
    }
    return pattern


result = build()
