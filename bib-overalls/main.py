"""
Bib overalls — FC-100 rank #49. Fashion Cabinet Garment Cartridge.

Denim dungarees on the side-seamed trouser block (chinos/jumpsuit lineage) with
NO fly: front/back legs (cut 2 each) join UP to a shaped chest BIB (cut 1 on the
CF fold) at the front waist and to a lower BACK panel (cut 1 on the CB fold) at
the back waist. Those two waist joins are THE SIGNATURE SEAMS: the leg waist
quarters and the bib/back-panel bottom half-widths are both driven from the SAME
shared waist formulas — (waist + ease)/4 -/+ a quarter shift — so each declared
seam closes with delta ~ 0 by construction (jumpsuit waist-seam method). The back
leg waist rises RISE_DIFF at CB, so its inner x is solved analytically
(sqrt(WAIST_B^2 - RISE_DIFF^2)) to keep the slanted edge exactly the back quarter.

Two adjustable STRAPS (cut 2) cross in back and buckle to the bib front; the
buckle catch on the bib and the buckle/slider ladder on each strap are drill-cross
internals. The hips open with a button placket on each side seam (marked internals
+ BOM buttons). Topstitch traces run the bib edges, out-seams, hems and pocket.
A bib patch POCKET (cut 1 on fold) finishes the chest. The front inseam is bowed
by a solved bulge to match the deeper back fork; sides are equal by construction.

All HARDWARE — overall buckles, sliders, jean tack buttons, rivets — is a Yantra4D
cartridge reference in the BOM note text, never re-implemented here (federation
contract: hard goods live in Yantra4D).

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


_KNOWN = ("front", "back", "bib", "back_panel", "strap", "bib_pocket", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

hip_girth      = float(PARAM(lambda: hip_girth, 1020.0))
waist_girth    = float(PARAM(lambda: waist_girth, 900.0))
inseam_length  = float(PARAM(lambda: inseam_length, 720.0))
front_rise     = float(PARAM(lambda: front_rise, 280.0))
back_rise      = float(PARAM(lambda: back_rise, 330.0))
denim_ease     = float(PARAM(lambda: denim_ease, 140.0))    # total hip ease, rigid denim
hem_width      = float(PARAM(lambda: hem_width, 120.0))     # front half-hem, flat
bib_width      = float(PARAM(lambda: bib_width, 260.0))     # full bib width at the top
bib_height     = float(PARAM(lambda: bib_height, 300.0))    # front waist up to bib top
back_height    = float(PARAM(lambda: back_height, 200.0))   # back waist up to back-panel top
strap_width    = float(PARAM(lambda: strap_width, 45.0))    # finished strap width
strap_length   = float(PARAM(lambda: strap_length, 700.0))  # each strap, cut net
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))  # deep denim hem, turned twice

hip_girth = max(650.0, min(hip_girth, 1800.0))
waist_girth = max(500.0, min(waist_girth, hip_girth))
inseam_length = max(300.0, min(inseam_length, 950.0))
front_rise = max(190.0, min(front_rise, 380.0))
back_rise = max(front_rise, min(back_rise, front_rise + 90.0))
denim_ease = max(60.0, min(denim_ease, 400.0))
hem_width = max(90.0, min(hem_width, 260.0))
bib_width = max(180.0, min(bib_width, 380.0))
bib_height = max(200.0, min(bib_height, 420.0))
back_height = max(120.0, min(back_height, 360.0))
strap_width = max(30.0, min(strap_width, 60.0))
strap_length = max(450.0, min(strap_length, 1000.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Shared waist formulas — BOTH signature seams are driven from here ────────
HIP_E = hip_girth + denim_ease
WAIST_E = waist_girth + denim_ease            # overalls sit loose; full ease at waist
QS = 12.0                                      # quarter shift: front narrower, back wider
WAIST_F, WAIST_B = WAIST_E / 4.0 - QS, WAIST_E / 4.0 + QS

# Pant frame: hem at y = 0, front waist line at y = inseam + front_rise.
CROTCH_Y = inseam_length
P_WAIST_Y = inseam_length + front_rise
RISE_DIFF = back_rise - front_rise
FW, BW = HIP_E / 4.0 - 10.0, HIP_E / 4.0 + 10.0
FORK_F, FORK_B = HIP_E / 16.0 + 10.0, HIP_E / 8.0 + 15.0
FHW, BHW = hem_width, hem_width + 12.0
# The back waist rises RISE_DIFF at CB; solve its inner x so the slanted waist
# edge length is EXACTLY the back waist quarter WAIST_B (jumpsuit method).
if WAIST_B <= RISE_DIFF:
    raise ValueError("back waist quarter is shorter than the rise difference; "
                     "lower back_rise or raise waist_girth")
PANT_WAIST_XB = math.sqrt(WAIST_B * WAIST_B - RISE_DIFF * RISE_DIFF)

HALF_BIB = bib_width / 2.0
PLACKET_DROP = 130.0                           # side button placket run below the waist
BTN_ARM = 4.0                                  # drill-cross half-length


# ── Internals: drill crosses, plackets, topstitch traces ────────────────────
def _cross(label, x, y, arm=BTN_ARM):
    """A small + drawn as one drill polyline at (x, y)."""
    return fc.Internal(
        label,
        [fc.P(x - arm, y), fc.P(x + arm, y), fc.P(x, y),
         fc.P(x, y - arm), fc.P(x, y + arm)],
        kind="drill",
    )


def _side_placket(label):
    """Side hip opening: a marked vertical placket down the side seam from the
    waist, with two button drill crosses (overalls open at the hips, not a fly)."""
    x = 6.0
    top = P_WAIST_Y
    marks = [fc.Internal(label, [fc.P(x, top), fc.P(x, top - PLACKET_DROP)])]
    marks.append(_cross(f"{label} button 1", x, top - 30.0))
    marks.append(_cross(f"{label} button 2", x, top - PLACKET_DROP + 30.0))
    return marks


def _out_topstitch(hem_w, label):
    """Twin-needle out-seam topstitch trace: side seam, hem line to waist."""
    x = 6.0
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, P_WAIST_Y)], kind="trace")


# ── Legs (side-seamed block, no fly) ─────────────────────────────────────────
def build_legs():
    f_tip = fc.P(FW + FORK_F, CROTCH_Y)
    b_tip = fc.P(BW + FORK_B, CROTCH_Y)

    def f_inseam(bulge):
        return fc.Edge("inseam", [fc.curve_through(f_tip, fc.P(FHW, 0.0),
                                                   bulge=bulge, side=-1.0)])

    b_inseam = fc.Edge("inseam", [fc.curve_through(b_tip, fc.P(BHW, 0.0),
                                                   bulge=0.0, side=-1.0)])
    back_len = b_inseam.length(0.05)
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

    # FRONT: flat waist from CF (x=0) out to WAIST_F — sews to the bib bottom.
    front = fc.Piece(
        "front",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, P_WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, P_WAIST_Y), fc.P(WAIST_F, P_WAIST_Y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(WAIST_F, P_WAIST_Y),
                           fc.P(FW - 4.0, P_WAIST_Y - front_rise * 0.45),
                           fc.P(FW + (f_tip.x - FW) * 0.35, CROTCH_Y + 55.0), f_tip)],
            ),
            f_inseam(bulge),
            fc.Edge("hem", [fc.Line(fc.P(FHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 1.0, "CF match"), fc.Notch("side", 0.5),
                 fc.Notch("inseam", 0.5),
                 fc.Notch("side", (P_WAIST_Y - PLACKET_DROP) / P_WAIST_Y, "placket stop")],
        grainline=fc.Grainline(fc.P(FW * 0.45, inseam_length * 0.12),
                               fc.P(FW * 0.45, inseam_length * 0.92)),
        internals=[_out_topstitch(FHW, "out-seam topstitch")] + _side_placket("front placket"),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front Leg",
    )

    # BACK: waist rises RISE_DIFF at CB; inner x solved so the slanted waist
    # edge length == WAIST_B exactly.
    cb_y = P_WAIST_Y + RISE_DIFF
    back = fc.Piece(
        "back",
        [
            fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, P_WAIST_Y))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, P_WAIST_Y), fc.P(PANT_WAIST_XB, cb_y))]),
            fc.Edge(
                "crotch",
                [fc.Bezier(fc.P(PANT_WAIST_XB, cb_y),
                           fc.P(BW - 4.0, cb_y - front_rise * 0.45),
                           fc.P(BW + (b_tip.x - BW) * 0.35, CROTCH_Y + 55.0), b_tip)],
            ),
            b_inseam,
            fc.Edge("hem", [fc.Line(fc.P(BHW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "CB match"), fc.Notch("side", 0.5),
                 fc.Notch("inseam", 0.5),
                 fc.Notch("side", (P_WAIST_Y - PLACKET_DROP) / P_WAIST_Y, "placket stop")],
        grainline=fc.Grainline(fc.P(BW * 0.45, inseam_length * 0.12),
                               fc.P(BW * 0.45, inseam_length * 0.92)),
        internals=[_out_topstitch(BHW, "out-seam topstitch")] + _side_placket("back placket"),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back Leg",
    )
    return front, back


# ── Bib (cut 1 on the CF fold; bottom == front waist quarter) ────────────────
def build_bib():
    """Shaped chest panel: bottom edge at y=0 sews to the two front-leg waists;
    a bib top narrower than the waist with a topstitched edge, a strap-buckle
    catch drill-cross near each top corner, and a chest topstitch outline."""
    hb_top = HALF_BIB
    top_y = bib_height
    # Bottom half-width equals the front waist quarter so the seam balances.
    bottom_x = WAIST_F
    # Waist->side rises straight, then curves in to the (narrower) bib top.
    side_top_y = top_y - 40.0
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        fc.Edge("bib_top", [fc.Line(fc.P(0.0, top_y), fc.P(hb_top, top_y))]),
        fc.Edge(
            "side",
            [fc.Bezier(fc.P(hb_top, top_y),
                       fc.P(hb_top + 6.0, side_top_y),
                       fc.P(bottom_x + (hb_top - bottom_x) * 0.35, top_y * 0.42),
                       fc.P(bottom_x, 0.0))],
        ),
        fc.Edge("bottom", [fc.Line(fc.P(bottom_x, 0.0), fc.P(0.0, 0.0))]),
    ]
    # Buckle catch: where the strap buttons/buckles onto the bib front, just
    # below the top corner (hardware is a Yantra4D ref — this is only the mark).
    buckle = _cross("bib buckle catch", hb_top - 22.0, top_y - 26.0)
    # Chest topstitch outline: parallel to the top and side, 8 mm in.
    ts = fc.Internal(
        "bib topstitch",
        [fc.P(0.0, top_y - 8.0), fc.P(hb_top - 8.0, top_y - 8.0),
         fc.P(bottom_x + (hb_top - bottom_x) * 0.35, top_y * 0.42),
         fc.P(bottom_x - 8.0, 12.0)],
        kind="trace",
    )
    return fc.Piece(
        "bib",
        edges,
        seam_allowance=seam_allowance,
        allowances={"bib_top": hem_allowance},   # top edge turned and topstitched
        notches=[fc.Notch("bottom", 1.0, "CF match"),
                 fc.Notch("side", 0.0, "waist match")],
        grainline=fc.Grainline(fc.P(hb_top * 0.5, top_y * 0.15),
                               fc.P(hb_top * 0.5, top_y * 0.85)),
        internals=[buckle, ts],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Bib (front)",
    )


# ── Back panel (cut 1 on the CB fold; bottom == back waist quarter) ──────────
def build_back_panel():
    """Upper back panel, lower than the bib: bottom edge sews to the two
    back-leg waists; the two strap ends attach to its top with buckle sliders
    (marked as drill crosses)."""
    top_y = back_height
    # Bottom half-width equals the back waist quarter so the seam balances.
    bottom_x = WAIST_B
    hb_top = bottom_x - 30.0                    # back panel narrows slightly to top
    side_top_y = top_y - 30.0
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        fc.Edge("back_top", [fc.Line(fc.P(0.0, top_y), fc.P(hb_top, top_y))]),
        fc.Edge(
            "side",
            [fc.Bezier(fc.P(hb_top, top_y),
                       fc.P(hb_top + 4.0, side_top_y),
                       fc.P(bottom_x - 6.0, top_y * 0.4),
                       fc.P(bottom_x, 0.0))],
        ),
        fc.Edge("bottom", [fc.Line(fc.P(bottom_x, 0.0), fc.P(0.0, 0.0))]),
    ]
    # Strap attach: where each strap is stitched onto the back panel top.
    attach = _cross("strap attach", hb_top - 26.0, top_y - 24.0)
    ts = fc.Internal(
        "back topstitch",
        [fc.P(0.0, top_y - 8.0), fc.P(hb_top - 8.0, top_y - 8.0)],
        kind="trace",
    )
    return fc.Piece(
        "back_panel",
        edges,
        seam_allowance=seam_allowance,
        allowances={"back_top": hem_allowance},
        notches=[fc.Notch("bottom", 1.0, "CB match"),
                 fc.Notch("side", 0.0, "waist match")],
        grainline=fc.Grainline(fc.P(hb_top * 0.5, top_y * 0.15),
                               fc.P(hb_top * 0.5, top_y * 0.85)),
        internals=[attach, ts],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back Panel",
    )


# ── Strap (cut 2, rectangular, adjustable) ───────────────────────────────────
def build_strap():
    """Adjustable overall strap, cut net (allowances folded into length). The
    buckle/slider ladder near the free end is a set of drill crosses; the actual
    buckle + slider are a Yantra4D hardware cartridge (see BOM)."""
    length = strap_length
    w = strap_width
    # Ladder of adjustment holes / slider positions near the buckling end.
    ladder = []
    for i in range(4):
        x = length - 60.0 - i * 45.0
        ladder.append(_cross(f"strap hole {i + 1}", x, w / 2.0, arm=3.0))
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, w))]),
            fc.Edge("top", [fc.Line(fc.P(length, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.15, w / 2.0), fc.P(length * 0.85, w / 2.0)),
        internals=[fc.Internal("edge topstitch",
                               [fc.P(0.0, 6.0), fc.P(length, 6.0)], kind="trace")] + ladder,
        cut=fc.CutSpec(quantity=2),
        label="Strap",
    )


# ── Bib patch pocket (cut 1 on fold) ─────────────────────────────────────────
def build_bib_pocket():
    """Bib patch pocket, cut 1 on the CF fold, with a divider topstitch."""
    pw = max(140.0, min(bib_width - 70.0, 260.0))
    h = 170.0
    half = pw / 2.0
    return fc.Piece(
        "bib_pocket",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(half, h))]),
            fc.Edge("side", [fc.Line(fc.P(half, h), fc.P(half, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(half, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": hem_allowance},        # pocket mouth turned + topstitched
        internals=[fc.Internal("divider topstitch", [fc.P(0.0, 0.0), fc.P(0.0, h)],
                               kind="trace")],
        grainline=fc.Grainline(fc.P(half * 0.5, 20.0), fc.P(half * 0.5, h - 20.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Bib Pocket",
    )


def build():
    pattern = fc.PatternSet("bib-overalls")
    front, back = build_legs()
    known = target_piece in _KNOWN
    everything = target_piece == "set" or not known
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "bib":
        pattern.add(build_bib())
    if everything or target_piece == "back_panel":
        pattern.add(build_back_panel())
    if everything or target_piece == "strap":
        pattern.add(build_strap())
    if everything or target_piece == "bib_pocket":
        pattern.add(build_bib_pocket())

    if everything:
        # Leg seams.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.5)
        # SIGNATURE SEAM 1 — bib bottom ↔ front-leg waists. Bib is cut on fold
        # (its half bottom sews in twice); the two front legs each contribute
        # one waist edge. Both driven by WAIST_F, so delta ~ 0.
        pattern.declare_seam(
            [("bib", "bottom"), ("bib", "bottom")],
            [("front", "waist"), ("front", "waist")],
            tol=2.0,
        )
        # SIGNATURE SEAM 2 — back-panel bottom ↔ back-leg waists. Same fold /
        # cut-2 accounting; both driven by WAIST_B, so delta ~ 0.
        pattern.declare_seam(
            [("back_panel", "bottom"), ("back_panel", "bottom")],
            [("back", "waist"), ("back", "waist")],
            tol=2.0,
        )

    # Fabric consumption on the denim card (1500 mm), plus notions. All hardware
    # is a Yantra4D cartridge reference in the note text — never re-implemented.
    fabric_width = 1500.0                          # mezclilla-denim card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.6)  # 60% marker efficiency, rigid denim
    pattern.bom = [
        {"item": "mezclilla-denim", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 60% marker efficiency"},
        {"item": "overall buckles + sliders (25 mm)", "qty": 2, "unit": "set",
         "note": "one buckle + one slider per strap; hardware is a Yantra4D "
                 "cartridge (buckle notion), never re-implemented here"},
        {"item": "jean tack buttons 17 mm", "qty": 6, "unit": "pcs",
         "note": "2 bib buckle catches + 4 side placket buttons; hardware is a "
                 "Yantra4D cartridge (shank-button guide), not re-implemented"},
        {"item": "tubular rivets 9 mm", "qty": 8, "unit": "pcs",
         "note": "reinforce placket ends, bib corners and pocket mouth; hardware "
                 "is a Yantra4D cartridge (rivet notion), not re-implemented"},
        {"item": "heavy topstitch thread (gold) + jeans needle 100/16",
         "qty": 1, "unit": "set", "note": "double-needle out-seams, bib and pocket edges"},
    ]
    pattern.metadata = {
        "fc100_rank": 49,
        "fabric_hint": "mezclilla-denim",
        "waist_front_quarter_mm": round(WAIST_F, 1),
        "waist_back_quarter_mm": round(WAIST_B, 1),
        "back_waist_inner_x_mm": round(PANT_WAIST_XB, 1),
        "rise_diff_mm": round(RISE_DIFF, 1),
        "bib_bottom_half_mm": round(WAIST_F, 1),
        "back_panel_bottom_half_mm": round(WAIST_B, 1),
        "topstitch": "double-needle heavy contrast (gold): out-seams, bib edges, "
                     "back-panel top, pocket mouth and hems",
        "hardware": "buckles + sliders + jean tack buttons + rivets are Yantra4D "
                    "cartridge references (see BOM); never drafted in the kernel",
        "drafting": "denim dungarees on the side-seamed trouser block, no fly; bib "
                    "and back panel join the legs at two declared waist seams driven "
                    "by shared waist formulas (delta ~ 0); back waist inner x solved "
                    "analytically; front inseam bow solved to the deeper back fork; "
                    "teaching-grade — straps are straight strips and the side hip "
                    "opening is marked, not a drafted placket underlay",
    }
    return pattern


result = build()
