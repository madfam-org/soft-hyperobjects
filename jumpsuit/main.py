"""
Jumpsuit — FC-100 rank #47 (Jumpsuit (mono)). Fashion Cabinet Garment Cartridge.

The commons' first full-body garment: a sleeveless woven BODICE (a-line-dress
lineage: front on fold, back cut 2 with a CB zipper allowance and derived
neck/armhole facing strips) joins a side-seamed TROUSER (sweatpants lineage:
front inseam bowed by a solved bulge to match the deeper back fork) at THE
WAIST SEAM. Bodice hem half-widths and pant waist edges are driven by the
SAME waist formulas — (waist + ease)/4 -/+ a quarter shift — so the declared
eight-reference waist seam (each side listed once per physical cut) closes
with delta ~ 0 by construction. A waist tie strip plus a marked tie channel
finish the seam. The CB zipper is measured from the neck DOWN and continues
conceptually past the waist into the pant back CB: when zipper_length exceeds
the bodice CB, the stop notch lands on the pant back crotch edge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
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


_KNOWN = ("bodice_front", "bodice_back", "pant_front", "pant_back",
          "facings", "tie", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 760.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
bodice_length = float(PARAM(lambda: bodice_length, 420.0))  # nape to waist seam
inseam_length = float(PARAM(lambda: inseam_length, 700.0))
front_rise = float(PARAM(lambda: front_rise, 270.0))
back_rise = float(PARAM(lambda: back_rise, 300.0))
jumpsuit_ease = float(PARAM(lambda: jumpsuit_ease, 120.0))  # total woven ease
hem_width = float(PARAM(lambda: hem_width, 120.0))          # pant half-hem, flat
zipper_length = float(PARAM(lambda: zipper_length, 450.0))  # neck down along CB
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

bust_girth = max(600.0, min(bust_girth, 1700.0))
waist_girth = max(450.0, min(waist_girth, 1500.0))
hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = min(waist_girth, hip_girth)  # a fitted woven waist never exceeds hip
bodice_length = max(300.0, min(bodice_length, 600.0))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
jumpsuit_ease = max(40.0, min(jumpsuit_ease, 300.0))
hem_width = max(90.0, min(hem_width, 260.0))
zipper_length = max(250.0, min(zipper_length, 600.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

NECK_W = 62.0           # half neck width at the high point of shoulder
STRAP_W = 42.0          # shoulder strap width
FRONT_DROP = 90.0       # front neck scoop
BACK_NECK_DROP = 30.0   # shallow back scoop
QS = 10.0               # quarter shift: front quarters narrower, back wider
FACING_DEPTH = 30.0     # finished facing depth; strips are 2x this tall
TIE_LEN = 1800.0        # waist tie strip, cut net
TIE_W = 40.0
CHANNEL_UP = 25.0       # tie-channel marking above the waist stitch line
BACK_HEM_EXTRA = 12.0   # back pant hem is slightly wider, like the block

# ── Shared waist formulas — THE waist seam is driven from here, both sides ──
BUST_E = bust_girth + jumpsuit_ease
WAIST_E = waist_girth + jumpsuit_ease
HIP_E = hip_girth + jumpsuit_ease
BUST_F, BUST_B = BUST_E / 4.0 - QS, BUST_E / 4.0 + QS
WAIST_F, WAIST_B = WAIST_E / 4.0 - QS, WAIST_E / 4.0 + QS

# Bodice frame: waist seam at y = 0, nape line at y = bodice_length.
HPS_Y = bodice_length + 20.0
AH = BUST_E / 8.0 + 90.0
AH = max(150.0, min(AH, min(280.0, bodice_length - 80.0)))
STRAP_END = fc.P(NECK_W + STRAP_W, HPS_Y - 12.0)
UNDERARM_Y = HPS_Y - AH
CB_LEN = HPS_Y - BACK_NECK_DROP  # bodice CB neck point down to the waist seam

# Pant frame: hem at y = 0, front waist line at y = inseam + front_rise.
CROTCH_Y = inseam_length
P_WAIST_Y = inseam_length + front_rise
RISE_DIFF = back_rise - front_rise
PFW, PBW = HIP_E / 4.0 - QS, HIP_E / 4.0 + QS
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + BACK_HEM_EXTRA
# The back waist rises RISE_DIFF at CB; solve its inner x so the slanted edge
# length is EXACTLY the back waist quarter from the shared formulas above.
PANT_WAIST_XF = WAIST_F
PANT_WAIST_XB = math.sqrt(WAIST_B * WAIST_B - RISE_DIFF * RISE_DIFF)


# ── Bodice (a-line-dress lineage, ending at the waist seam) ─────────────────
def _neck_edge(drop):
    """Scoop from the center top to the HPS point — tank-style curve."""
    top_y = HPS_Y - drop
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, top_y), fc.P(NECK_W * 0.55, top_y),
                   fc.P(NECK_W, top_y + drop * 0.45), fc.P(NECK_W, HPS_Y))],
    )


def _shoulder_edge():
    return fc.Edge("shoulder", [fc.Line(fc.P(NECK_W, HPS_Y), STRAP_END)])


def _armhole_edge(bust_w):
    """Tank-style scoop; front/back differ only by the quarter shift."""
    underarm = fc.P(bust_w, UNDERARM_Y)
    return fc.Edge(
        "armhole",
        [fc.Bezier(STRAP_END, fc.P(STRAP_END.x + 6.0, STRAP_END.y - AH * 0.45),
                   fc.P(bust_w - AH * 0.28, UNDERARM_Y + 14.0), underarm)],
    )


def _side_edge(bust_w, waist_w):
    """Straight fitted taper underarm -> waist seam.

    Front and back share the same vertical run and the same horizontal
    intake (bust_w - waist_w == (BUST_E - WAIST_E)/4 on both), so the
    declared bodice side seam matches exactly by construction.
    """
    return fc.Edge("side", [fc.Line(fc.P(bust_w, UNDERARM_Y), fc.P(waist_w, 0.0))])


def _hem_edge(waist_w):
    return fc.Edge("hem", [fc.Line(fc.P(waist_w, 0.0), fc.P(0.0, 0.0))])


def _tie_channel(waist_w):
    """Stitching guide for the waist-tie channel just above the waist seam."""
    return fc.Internal(
        "tie channel",
        [fc.P(0.0, CHANNEL_UP), fc.P(waist_w, CHANNEL_UP)],
    )


def _bodice_grainline(bust_w):
    return fc.Grainline(fc.P(bust_w * 0.55, 60.0), fc.P(bust_w * 0.55, UNDERARM_Y - 40.0))


def _bodice_front():
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, HPS_Y - FRONT_DROP))]),
        _neck_edge(FRONT_DROP),
        _shoulder_edge(),
        _armhole_edge(BUST_F),
        _side_edge(BUST_F, WAIST_F),
        _hem_edge(WAIST_F),
    ]
    return fc.Piece(
        "bodice_front", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hem", 0.5, "waist quarter"), fc.Notch("side", 0.5, "side match")],
        grainline=_bodice_grainline(BUST_F),
        internals=[_tie_channel(WAIST_F)],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Bodice Front",
    )


def _bodice_back():
    zip_in_bodice = min(zipper_length, CB_LEN)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, CB_LEN))]),
        _neck_edge(BACK_NECK_DROP),
        _shoulder_edge(),
        _armhole_edge(BUST_B),
        _side_edge(BUST_B, WAIST_B),
        _hem_edge(WAIST_B),
    ]
    return fc.Piece(
        "bodice_back", edges,
        seam_allowance=seam_allowance,
        allowances={"center": 20.0},  # CB seam carries the zipper
        notches=[
            fc.Notch("hem", 0.5, "waist quarter"),
            fc.Notch("side", 0.5, "side match"),
            # Zipper spans zip_in_bodice from the neck DOWN; `center` is
            # authored waist->neck, so the stop sits at 1 - zip/CB_LEN. When
            # the zipper is longer than the bodice CB the stop notch moves
            # onto the pant back crotch edge (see build_pants).
            fc.Notch("center", 1.0 - zip_in_bodice / CB_LEN, "zipper stop"),
        ],
        grainline=_bodice_grainline(BUST_B),
        internals=[_tie_channel(WAIST_B)],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice Back",
    )


# ── Trouser (sweatpants lineage, woven ease, fitted waist seam) ─────────────
def _pant_edges(width, fork, hem_w, waist_x, cb_y, rise):
    tip = fc.P(width + fork, CROTCH_Y)
    waist = fc.Edge("waist", [fc.Line(fc.P(0.0, P_WAIST_Y), fc.P(waist_x, cb_y))])
    crotch = fc.Edge(
        "crotch",
        [fc.Bezier(fc.P(waist_x, cb_y), fc.P(width - 4.0, cb_y - rise * 0.45),
                   fc.P(width + (tip.x - width) * 0.35, CROTCH_Y + 55.0), tip)],
    )

    def inseam(bulge):
        return fc.Edge(
            "inseam",
            [fc.curve_through(tip, fc.P(hem_w, 0.0), bulge=bulge, side=-1.0)],
        )

    return waist, crotch, inseam


def build_pants():
    f_waist, f_crotch, f_inseam = _pant_edges(
        PFW, FORK_F, FHW, PANT_WAIST_XF, P_WAIST_Y, front_rise)
    b_waist, b_crotch, b_inseam = _pant_edges(
        PBW, FORK_B, BHW, PANT_WAIST_XB, P_WAIST_Y + RISE_DIFF, back_rise)
    # Solve the front-inseam bow so it matches the deeper back (bisection).
    back_len = b_inseam(0.0).length(0.05)
    lo, hi = 0.0, 0.35
    for _ in range(44):
        mid = (lo + hi) / 2.0
        if f_inseam(mid).length(0.05) < back_len:
            lo = mid
        else:
            hi = mid
    bulge = (lo + hi) / 2.0
    if abs(f_inseam(bulge).length(0.05) - back_len) > 1.0:
        raise ValueError("front-inseam solver did not converge")

    def make(name, waist, crotch, inseam_edge, hem_w, width, label, extra):
        edges = [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, P_WAIST_Y))]),
            waist,
            crotch,
            inseam_edge,
            fc.Edge("hem", [fc.Line(fc.P(hem_w, 0.0), fc.P(0.0, 0.0))]),
        ]
        notches = [fc.Notch("waist", 0.5, "waist quarter"), fc.Notch("side", 0.5),
                   fc.Notch("inseam", 0.5)] + extra
        return fc.Piece(
            name, edges,
            seam_allowance=seam_allowance,
            allowances={"hem": hem_allowance},  # open hem
            notches=notches,
            grainline=fc.Grainline(fc.P(width * 0.45, inseam_length * 0.12),
                                   fc.P(width * 0.45, inseam_length * 0.92)),
            cut=fc.CutSpec(quantity=2, mirror=True),
            label=label,
        )

    # Zipper overrun: the CB zipper conceptually crosses the waist seam and
    # ends on the pant back crotch (CB) edge — mark the stop there.
    back_extra = []
    overrun = zipper_length - CB_LEN
    if overrun > 1.0:
        back_extra.append(
            fc.Notch("crotch", min(overrun / b_crotch.length(), 0.35), "zipper stop"))
    front = make("pant_front", f_waist, f_crotch, f_inseam(bulge), FHW, PFW,
                 "Pant Front", [])
    back = make("pant_back", b_waist, b_crotch, b_inseam(0.0), BHW, PBW,
                "Pant Back", back_extra)
    return front, back


# ── Derived strips (facings + waist tie) ────────────────────────────────────
def _strip(name, length, height, quantity, label):
    """A straight-grain strip cut net (allowances already folded into length)."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, height))]),
        fc.Edge("top", [fc.Line(fc.P(length, height), fc.P(0.0, height))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, height), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, height / 2.0),
                               fc.P(length * 0.8, height / 2.0)),
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("jumpsuit")
    b_front = _bodice_front()
    b_back = _bodice_back()
    p_front, p_back = build_pants()
    known = target_piece in _KNOWN
    add_bf = not known or target_piece in ("bodice_front", "set")
    add_bb = not known or target_piece in ("bodice_back", "set")
    add_pf = not known or target_piece in ("pant_front", "set")
    add_pb = not known or target_piece in ("pant_back", "set")
    add_face = not known or target_piece in ("facings", "set")
    add_tie = not known or target_piece in ("tie", "set")
    if add_bf:
        pattern.add(b_front)
    if add_bb:
        pattern.add(b_back)
    if add_pf:
        pattern.add(p_front)
    if add_pb:
        pattern.add(p_back)
    if add_face:
        # Physical openings: the front is cut on fold (drafted half sews in
        # twice); the back is cut 2 (its drafted edge appears once per panel).
        # Neck facing = 2*front.neck + 2*back.neck + 2 sa, cut 1 (ends meet
        # the CB zipper). Each armhole = one front + one back scoop, cut 2.
        neck_opening = 2.0 * (b_front.edge("neck").length() + b_back.edge("neck").length())
        armhole_opening = b_front.edge("armhole").length() + b_back.edge("armhole").length()
        pattern.add(_strip("neck_facing", neck_opening + 2.0 * seam_allowance,
                           2.0 * FACING_DEPTH, 1, "Neck Facing"))
        pattern.add(_strip("armhole_facing", armhole_opening + 2.0 * seam_allowance,
                           2.0 * FACING_DEPTH, 2, "Armhole Facing"))
    if add_tie:
        pattern.add(_strip("waist_tie", TIE_LEN, TIE_W, 1, "Waist Tie"))
    if add_bf and add_bb:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.5)
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"), tol=1.5)
    if add_pf and add_pb:
        pattern.declare_seam(("pant_front", "side"), ("pant_back", "side"), tol=1.5)
        pattern.declare_seam(("pant_front", "inseam"), ("pant_back", "inseam"), tol=1.5)
    if add_bf and add_bb and add_pf and add_pb:
        # THE WAIST SEAM. Each reference appears once per physical cut: the
        # fold-cut bodice front hem sews in twice; the cut-2 bodice backs,
        # pant fronts, and pant backs each contribute one edge per panel.
        # Both sides are driven by WAIST_F/WAIST_B, so delta ~ 0.
        pattern.declare_seam(
            [("bodice_front", "hem"), ("bodice_front", "hem"),
             ("bodice_back", "hem"), ("bodice_back", "hem")],
            [("pant_front", "waist"), ("pant_front", "waist"),
             ("pant_back", "waist"), ("pant_back", "waist")],
            tol=3.0,
        )
    if add_bb:
        pattern.bom.append({
            "item": "invisible zipper (CB)",
            "qty": round(zipper_length),
            "unit": "mm",
            "note": "set from the back neck down; past the waist seam the tape "
                    "continues into the pant back CB to the marked stop notch",
        })
    pattern.metadata = {
        "fc100_rank": 47,
        "fabric_hint": "popelina-algodon",
        "waist_seam_mm": round(2.0 * (WAIST_F + WAIST_B), 1),
        "drafting": "sleeveless bodice + side-seamed trouser joined at a declared "
                    "waist seam driven by shared waist formulas; front inseam bow "
                    "solved to the deeper back; facings derived from measured "
                    "openings; CB zipper continues into the pant back CB",
    }
    return pattern


result = build()
