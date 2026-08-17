"""
Romper — FC-100 rank #48 (Mono corto). Fashion Cabinet Garment Cartridge.

Relaxed pull-on summer romper: a sleeveless blouson BODICE (front and back
both cut on fold — no zipper; the back closes with a U-shaped CB neck
KEYHOLE marked internal plus a button cross) meets a SHORTS block
(athletic-shorts lineage: the back hem width is solved analytically so the
straight inseams match exactly) at an ELASTICIZED WAIST SEAM. The bodice
hems are cut wider than the shorts waists on purpose: the blouson surplus
is computed from the same width formulas and declared as ease on the joined
waist seam, so delta is 0 by construction. An elastic channel is marked
internal at the bodice hem and the waist elastic is a BOM line.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
_KNOWN = ("bodice_front", "bodice_back", "short_front", "short_back",
          "facings", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))    # sizes the waist elastic
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
bodice_length = float(PARAM(lambda: bodice_length, 400.0))  # HPS to waist seam
inseam_length = float(PARAM(lambda: inseam_length, 90.0))
front_rise = float(PARAM(lambda: front_rise, 260.0))
back_rise = float(PARAM(lambda: back_rise, 290.0))
blouson_ease = float(PARAM(lambda: blouson_ease, 200.0))  # roomy pull-on bodice
short_ease = float(PARAM(lambda: short_ease, 120.0))
hem_width = float(PARAM(lambda: hem_width, 240.0))        # front half-hem, flat
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1700.0))
waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(650.0, min(hip_girth, 1800.0))
bodice_length = max(320.0, min(bodice_length, 600.0))
inseam_length = max(70.0, min(inseam_length, 350.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 80.0))
blouson_ease = max(80.0, min(blouson_ease, 400.0))
short_ease = max(60.0, min(short_ease, 350.0))
hem_width = max(160.0, min(hem_width, 340.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Constants ────────────────────────────────────────────────────────────────
FRONT_DROP = 95.0    # front scoop below the HPS line
BACK_DROP = 40.0     # shallow back scoop
NECK_W = 62.0        # half neck width at the high point of shoulder
STRAP_W = 42.0       # shoulder strap width
FACING_DEPTH = 30.0  # finished facing depth; strips are 2x this tall
KEY_LEN = 80.0       # CB keyhole slit length below the neckline
KEY_HALF = 9.0       # keyhole half-width at the fold
CHANNEL_RISE = 12.0  # elastic-channel stitching above the waist stitch line

# ── Shorts block (athletic-shorts lineage) ───────────────────────────────────
HIP_E = hip_girth + short_ease
CROTCH_Y = inseam_length
WAIST_Y = inseam_length + front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0, HIP_E / 12.0
BACK_TILT = back_rise - front_rise

# Waist-seam accounting, from the SAME formulas the pieces are drafted with.
# Each shorts waist edge is a straight line: front runs level for 0.92*width,
# back runs the same but tilted up BACK_TILT at the CB. Both legs cut 2.
SF_WAIST = 0.92 * FW
SB_WAIST = math.hypot(0.92 * BW, BACK_TILT)
SHORT_WAIST_TOTAL = 2.0 * (SF_WAIST + SB_WAIST)

# Bodice half-width: roomy blouson quarter, never narrower than the shorts
# waist quarter (the blouson gathers INTO the shorts, never the reverse).
BOD_W = max((bust_girth + blouson_ease) / 4.0, SHORT_WAIST_TOTAL / 4.0)
# Both bodice halves are fold-cut, so each drafted hem sews in twice:
SURPLUS = 4.0 * BOD_W - SHORT_WAIST_TOTAL  # blouson surplus, >= 0 by the max()

HPS_Y = bodice_length                      # waist seam sits at bodice y = 0
AH = (bust_girth + blouson_ease) / 8.0 + 90.0
AH = max(170.0, min(AH, 280.0, bodice_length - 120.0))
STRAP_END = fc.P(NECK_W + STRAP_W, HPS_Y - 12.0)
UNDERARM = fc.P(BOD_W, HPS_Y - AH)


def _neck_edge(drop):
    """Scoop from the center top to the HPS point — tank-style curve."""
    top_y = HPS_Y - drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + drop * 0.45), fc.P(NECK_W, HPS_Y))],
    )


def _bodice(name, center_name, drop, extras, label):
    """Blouson bodice half: fold-cut, scooped neck, straight side, waist hem."""
    top_y = HPS_Y - drop
    edges = [
        fc.Edge(center_name, [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        _neck_edge(drop),
        fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), STRAP_END)]),
        fc.Edge(
            "armhole",
            [fc.Bezier(STRAP_END,
                       fc.P(STRAP_END.x + 6.0, STRAP_END.y - AH * 0.45),
                       fc.P(BOD_W - AH * 0.28, UNDERARM.y + 14.0), UNDERARM)],
        ),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(BOD_W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(BOD_W, 0.0), fc.P(0.0, 0.0))]),
    ]
    channel = fc.Internal(
        "elastic channel",
        [fc.P(0.0, CHANNEL_RISE), fc.P(BOD_W, CHANNEL_RISE)],
    )
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("hem", 0.5, "waist quarter")],
        grainline=fc.Grainline(fc.P(BOD_W * 0.55, 40.0),
                               fc.P(BOD_W * 0.55, UNDERARM.y - 30.0)),
        internals=[channel] + extras,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge=center_name, mirror=True),
        label=label,
    )


def _keyhole_internals():
    """U-shaped CB neck keyhole (half, on the fold) + a button cross beside it."""
    cb_top = HPS_Y - BACK_DROP
    kb = cb_top - KEY_LEN
    keyhole = fc.Internal(
        "keyhole opening (cut open)",
        [fc.P(KEY_HALF, cb_top), fc.P(KEY_HALF, kb + KEY_HALF),
         fc.P(KEY_HALF * 0.55, kb + KEY_HALF * 0.3), fc.P(0.0, kb)],
        kind="trace",
    )
    bx, by = KEY_HALF + 7.0, cb_top - 8.0
    button = fc.Internal(
        "button + loop (CB keyhole)",
        [fc.P(bx - 4.0, by), fc.P(bx + 4.0, by), fc.P(bx, by),
         fc.P(bx, by + 4.0), fc.P(bx, by - 4.0)],
        kind="drill",
    )
    return [keyhole, button]


def _shorts():
    """Short-leg block; back hem width solved so straight inseams match."""
    f_tip_x = FW + FORK_F
    b_tip_x = BW + FORK_B
    front_len = math.hypot(f_tip_x - hem_width, CROTCH_Y)
    run = math.sqrt(max(front_len**2 - CROTCH_Y**2, 25.0))
    bhw = b_tip_x - run                       # back hem solved analytically
    if bhw < 100.0:
        raise ValueError("solved back hem width degenerate; widen hem_width")

    def make(name, width, tip_x, hem_w, cb_y, label):
        waist_in = width * 0.92
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, WAIST_Y), fc.P(waist_in, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(waist_in, cb_y),
                           fc.P(width - 4.0, cb_y - front_rise * 0.45),
                           fc.P(width + (tip_x - width) * 0.35, CROTCH_Y + 40.0),
                           fc.P(tip_x, CROTCH_Y))],
            ),
            fc.Edge("inseam", [fc.Line(fc.P(tip_x, CROTCH_Y), fc.P(hem_w, 0.0))]),
            fc.Edge("hem", [fc.curve_through(fc.P(hem_w, 0.0), fc.P(0.0, 0.0),
                                             bulge=0.04, side=-1.0)]),
        ]
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},
            notches=[fc.Notch("side", 0.5, "side match"),
                     fc.Notch("waist", 0.5, "waist quarter")],
            grainline=fc.Grainline(fc.P(width * 0.45, WAIST_Y * 0.15),
                                   fc.P(width * 0.45, WAIST_Y * 0.8)),
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    front = make("short_front", FW, f_tip_x, hem_width, WAIST_Y, "Short Front")
    back = make("short_back", BW, b_tip_x, bhw, WAIST_Y + BACK_TILT, "Short Back")
    return front, back


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
    pattern = fc.PatternSet("romper")
    b_front = _bodice("bodice_front", "cf", FRONT_DROP, [], "Bodice Front")
    b_back = _bodice("bodice_back", "cb", BACK_DROP, _keyhole_internals(), "Bodice Back")
    s_front, s_back = _shorts()
    known = target_piece in _KNOWN
    add_bf = not known or target_piece in ("bodice_front", "set")
    add_bb = not known or target_piece in ("bodice_back", "set")
    add_sf = not known or target_piece in ("short_front", "set")
    add_sb = not known or target_piece in ("short_back", "set")
    add_face = not known or target_piece in ("facings", "set")
    if add_bf:
        pattern.add(b_front)
    if add_bb:
        pattern.add(b_back)
    if add_sf:
        pattern.add(s_front)
    if add_sb:
        pattern.add(s_back)
    if add_face:
        # Fold-cut halves → each garment opening is twice the drafted edge.
        # The neck facing runs the full opening (keyhole is cut after); each
        # armhole facing is one front scoop + one back scoop, cut 2.
        neck_opening = 2.0 * (b_front.edge("neck").length() + b_back.edge("neck").length())
        armhole_opening = b_front.edge("armhole").length() + b_back.edge("armhole").length()
        pattern.add(_facing("neck_facing", neck_opening, 1, "Neck Facing"))
        pattern.add(_facing("armhole_facing", armhole_opening, 2, "Armhole Facing"))
    if add_bf and add_bb:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.5)
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"), tol=1.5)
    if add_sf and add_sb:
        pattern.declare_seam(("short_front", "side"), ("short_back", "side"), tol=1.5)
        pattern.declare_seam(("short_front", "inseam"), ("short_back", "inseam"), tol=1.5)
    if add_bf and add_bb and add_sf and add_sb:
        # Elasticized waist seam: every fold-cut bodice hem sews in twice,
        # every cut-2 shorts waist sews in twice. The blouson surplus is the
        # declared ease, computed from the same width formulas as the pieces,
        # so delta is 0 by construction and drift in either block breaks it.
        pattern.declare_seam(
            [("bodice_front", "hem"), ("bodice_front", "hem"),
             ("bodice_back", "hem"), ("bodice_back", "hem")],
            [("short_front", "waist"), ("short_front", "waist"),
             ("short_back", "waist"), ("short_back", "waist")],
            ease=SURPLUS, tol=3.0,
        )
        pattern.bom.append({
            "item": "soft elastic (waist channel)",
            "qty": round(waist_girth * 0.95),
            "unit": "mm",
            "note": "waist_girth x 0.95; threaded through the channel marked "
                    "inside the bodice hem after the waist seam is joined",
        })
    if add_bb:
        pattern.bom.append({
            "item": "button, 12 mm (CB keyhole)",
            "qty": 1,
            "unit": "pc",
            "note": "hardware via Yantra4D shank-button; a thread loop crosses "
                    "the keyhole at the marked drill point",
        })
    pattern.metadata = {
        "fc100_rank": 48,
        "fabric_hint": "popelina-algodon",
        "waist_surplus_mm": round(SURPLUS, 1),
        "drafting": "pull-on blouson bodice (fold-cut, CB neck keyhole) over an "
                    "athletic-shorts block with the back hem solved analytically; "
                    "the elasticized waist seam declares the computed surplus as ease",
    }
    return pattern


result = build()
