"""
Bodice Block (Sloper) — Fashion Cabinet Garment Cartridge (2D pattern).

A simplified metric flat block: front and back bodice slopers drafted from
body measurements, with waist darts as internal markings, matched side and
shoulder seams, fold-cut center lines, notches, and grainlines. This is a
teaching-grade block (waist kept straight, darts not rotated into the
outline) — the point is the contract: measurements in, verified pieces out.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals (e.g. `bust_girth`).
  - Access them via PARAM(lambda: <name>, <default>) so the script also runs
    standalone / with any subset of params. Do NOT use globals()/eval/getattr —
    they are not in the sandbox's allowed builtins.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import math

import fc


# ── Sandbox-safe parameter access ────────────────────────────────────────────
def PARAM(getter, default):
    """Return an injected global if present, else the default.
    `except Exception` catches the NameError raised for an unbound param name
    (the sandbox does not expose globals())."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # "front" | "back" | "set"

bust_girth        = float(PARAM(lambda: bust_girth, 880.0))
waist_girth       = float(PARAM(lambda: waist_girth, 700.0))
back_waist_length = float(PARAM(lambda: back_waist_length, 400.0))
neck_girth        = float(PARAM(lambda: neck_girth, 370.0))
shoulder_length   = float(PARAM(lambda: shoulder_length, 125.0))
armscye_depth     = float(PARAM(lambda: armscye_depth, 0.0))  # 0 = auto from bust
bust_ease         = float(PARAM(lambda: bust_ease, 80.0))
waist_ease        = float(PARAM(lambda: waist_ease, 60.0))
back_dart_intake  = float(PARAM(lambda: back_dart_intake, 25.0))
front_dart_intake = float(PARAM(lambda: front_dart_intake, 30.0))
seam_allowance    = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance     = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps (keep the draft solvable) ─────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1600.0))
waist_girth = max(450.0, min(waist_girth, bust_girth + 100.0))
back_waist_length = max(280.0, min(back_waist_length, 560.0))
neck_girth = max(280.0, min(neck_girth, 520.0))
shoulder_length = max(90.0, min(shoulder_length, 200.0))
bust_ease = max(0.0, bust_ease)
waist_ease = max(0.0, waist_ease)
back_dart_intake = max(0.0, min(back_dart_intake, 60.0))
front_dart_intake = max(0.0, min(front_dart_intake, 60.0))

H = back_waist_length                       # waist sits at y = 0, nape at y = H
AD = armscye_depth if armscye_depth > 0 else bust_girth / 8.0 + 105.0
AD = max(140.0, min(AD, H - 80.0))          # underarm stays well above the waist
NECK_RISE = 20.0                            # side-neck point above the nape line
BACK_DROP, FRONT_DROP = 40.0, 50.0          # shoulder slope drops

quarter_bust = (bust_girth + bust_ease) / 4.0
quarter_waist = (waist_girth + waist_ease) / 4.0
back_w = quarter_bust - 5.0                 # back/front balance: −5 / +5
front_w = quarter_bust + 5.0
back_neck_w = max(45.0, neck_girth / 5.0 - 2.0)
front_neck_w = max(42.0, neck_girth / 5.0 - 7.0)
front_neck_depth = neck_girth / 5.0 + 15.0


def _shoulder_tip(neck_x, neck_y, drop):
    run = math.sqrt(max(shoulder_length**2 - drop**2, 1.0))
    return fc.P(neck_x + run, neck_y - drop)


def _dart(center_x, intake, apex_h, label):
    half = intake / 2.0
    return fc.Internal(
        label,
        [fc.P(center_x - half, 0.0), fc.P(center_x, apex_h), fc.P(center_x + half, 0.0)],
        kind="dart",
    )


def build_back():
    nape = fc.P(0.0, H)
    neck_pt = fc.P(back_neck_w, H + NECK_RISE)
    tip = _shoulder_tip(neck_pt.x, neck_pt.y, BACK_DROP)
    underarm = fc.P(back_w, H - AD)
    side_waist_x = quarter_waist - 5.0 + back_dart_intake
    side_waist = fc.P(min(side_waist_x, back_w - 5.0), 0.0)
    origin = fc.P(0.0, 0.0)

    edges = [
        fc.Edge("cb", [fc.Line(origin, nape)]),
        fc.Edge("neck", [fc.curve_through(nape, neck_pt, bulge=0.12, side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_pt, tip)]),
        fc.Edge(
            "armscye",
            [fc.Bezier(tip, fc.P(tip.x + 8.0, tip.y - 90.0),
                       fc.P(underarm.x - 5.0, underarm.y + 70.0), underarm)],
        ),
        fc.Edge("side", [fc.Line(underarm, side_waist)]),
        fc.Edge("waist", [fc.Line(side_waist, origin)]),
    ]
    piece = fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"waist": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armscye", 0.45, "back single")],
        grainline=fc.Grainline(fc.P(back_w * 0.68, 60.0), fc.P(back_w * 0.68, H - 80.0)),
        internals=[_dart(side_waist.x * 0.5, back_dart_intake, 140.0, "back waist dart")]
        if back_dart_intake > 0.5 else [],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back Bodice",
    )
    return piece


def build_front():
    cf_neck = fc.P(0.0, H + NECK_RISE - front_neck_depth)
    neck_pt = fc.P(front_neck_w, H + NECK_RISE)
    tip = _shoulder_tip(neck_pt.x, neck_pt.y, FRONT_DROP)
    side_waist_x = quarter_waist + 5.0 + front_dart_intake
    side_waist = fc.P(min(side_waist_x, front_w - 5.0), 0.0)
    origin = fc.P(0.0, 0.0)

    # Place the front underarm so the front side seam equals the back's
    # analytically — the seam check then passes by construction.
    back_side_len = fc.P(back_w, H - AD).distance(
        fc.P(min(quarter_waist - 5.0 + back_dart_intake, back_w - 5.0), 0.0)
    )
    dx = front_w - side_waist.x
    underarm_y = math.sqrt(max(back_side_len**2 - dx**2, 100.0))
    underarm = fc.P(front_w, underarm_y)

    edges = [
        fc.Edge("cf", [fc.Line(origin, cf_neck)]),
        fc.Edge(
            "neck",
            [fc.Bezier(cf_neck, fc.P(front_neck_w * 0.55, cf_neck.y),
                       fc.P(neck_pt.x, cf_neck.y + (neck_pt.y - cf_neck.y) * 0.45), neck_pt)],
        ),
        fc.Edge("shoulder", [fc.Line(neck_pt, tip)]),
        fc.Edge(
            "armscye",
            [fc.Bezier(tip, fc.P(tip.x + 10.0, tip.y - 95.0),
                       fc.P(underarm.x - 10.0, underarm.y + 65.0), underarm)],
        ),
        fc.Edge("side", [fc.Line(underarm, side_waist)]),
        fc.Edge("waist", [fc.Line(side_waist, origin)]),
    ]
    piece = fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"waist": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armscye", 0.45, "front double")],
        grainline=fc.Grainline(fc.P(front_w * 0.68, 60.0), fc.P(front_w * 0.68, H - 80.0)),
        internals=[_dart(side_waist.x * 0.5, front_dart_intake, 120.0, "front waist dart")]
        if front_dart_intake > 0.5 else [],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Front Bodice",
    )
    return piece


def build():
    pattern = fc.PatternSet("bodice-block")
    pattern.metadata = {
        "bust_girth": bust_girth,
        "waist_girth": waist_girth,
        "armscye_depth": AD,
        "drafting": "simplified metric flat block (teaching-grade)",
    }
    want_front = target_piece in ("front", "set")
    want_back = target_piece in ("back", "set")
    if not (want_front or want_back):
        want_front = want_back = True
    if want_back:
        pattern.add(build_back())
    if want_front:
        pattern.add(build_front())
    if want_front and want_back:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    return pattern


result = build()
