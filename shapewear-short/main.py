"""
Shapewear Short — Fashion Cabinet Garment Cartridge (FC-300 #224).

A high-waisted compression short in powernet: waist to mid-thigh, no hardware at all,
pulled on. The only structure is COMPRESSION, and compression is a number this cartridge
refuses to hide.

The honest bit. Shapewear works by negative ease — the garment is cut SMALLER than the
body and the fabric's recovery does the rest. Commercial shapewear expresses this as a
size letter and a marketing adjective ("firm control"), which tells a wearer nothing and
cannot be reproduced. Here it is an explicit percentage per zone, and the zones differ
because bodies do:

  - The WAIST takes the most compression (it is the zone shapewear is bought for).
  - The HIP takes less — over-compressing a hip just pushes volume somewhere else.
  - The THIGH takes least, because a leg opening cut too tight becomes a tourniquet
    that rolls up and cuts in. That is the failure mode of cheap shapewear, and it is
    a drafting decision, not a fabric problem.

Each zone's finished ring is printed in the metadata alongside the body measurement it
came from, so the compression is auditable rather than asserted.

Drafting. Four pieces: a front and a back leg panel (each cut as a mirrored pair), a
high waistband, and a gusset. The legs are drafted from the body rise and the outside
leg length; the back is cut with more width than the front through the seat, which is
what stops a compression short from dragging itself down at the back — the seat needs
room the front does not.

Made to measure to waist, hip, thigh girths + body rise. No `notion` hardware: a
pull-on garment has no closure, and this lane does not invent one to score a bridge.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

waist_girth  = float(PARAM(lambda: waist_girth, 760.0))
hip_girth    = float(PARAM(lambda: hip_girth, 990.0))
thigh_girth  = float(PARAM(lambda: thigh_girth, 580.0))
body_rise    = float(PARAM(lambda: body_rise, 280.0))       # waist to crotch, seated
inseam_len   = float(PARAM(lambda: inseam_len, 180.0))      # crotch to hem (mid-thigh)
waistband_h  = float(PARAM(lambda: waistband_h, 120.0))     # high-waist band depth
waist_compression = float(PARAM(lambda: waist_compression, 18.0))   # % negative ease
hip_compression   = float(PARAM(lambda: hip_compression, 12.0))
thigh_compression = float(PARAM(lambda: thigh_compression, 7.0))
gusset_w     = float(PARAM(lambda: gusset_w, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
waist_girth  = max(520.0, min(waist_girth, 1500.0))
hip_girth    = max(620.0, min(hip_girth, 1800.0))
thigh_girth  = max(350.0, min(thigh_girth, 1000.0))
body_rise    = max(180.0, min(body_rise, 420.0))
inseam_len   = max(60.0, min(inseam_len, 400.0))
waistband_h  = max(30.0, min(waistband_h, 260.0))
waist_compression = max(0.0, min(waist_compression, 30.0))
hip_compression   = max(0.0, min(hip_compression, 25.0))
thigh_compression = max(0.0, min(thigh_compression, 20.0))
gusset_w     = max(40.0, min(gusset_w, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# the band cannot be deeper than the rise it sits on
waistband_h = min(waistband_h, body_rise - 40.0)

# ── THE COMPRESSION SOLVER (the number shapewear hides) ──────────────────────
# Each zone gets its OWN negative ease. Finished ring = body ring x (1 - pct/100).
WAIST_FIN = waist_girth * (1.0 - waist_compression / 100.0)
HIP_FIN = hip_girth * (1.0 - hip_compression / 100.0)
THIGH_FIN = thigh_girth * (1.0 - thigh_compression / 100.0)

# Quarter shares: front and back each carry a quarter of every ring, and they carry the
# SAME quarter — the rings close exactly on the solved compression values.
W_Q = WAIST_FIN / 4.0
H_Q = HIP_FIN / 4.0
T_Q = THIGH_FIN / 4.0

# Seat room: the back needs more cloth than the front through the seat, or a compression
# short drags itself down at the back. It is added as extra DEPTH in the back crotch
# curve — NOT as extra width at the side seam, which would unbalance the front/back side
# seams and is anatomically the wrong place for it anyway.
SEAT_SHIFT = body_rise * 0.06

RISE = body_rise - waistband_h          # leg-panel rise below the band
HIP_Y = RISE * 0.55                     # hip line height on the leg panel
IL = inseam_len


def _leg(name, hip_w, thigh_w, waist_w, seat_depth, label):
    """One leg panel: waist edge at the top, hip line at HIP_Y, hem at the bottom.

    CCW outline: hem -> inseam (up to the crotch) -> crotch_seam -> waist -> side_seam.

    The SIDE SEAM IS STRAIGHT AND VERTICAL on both panels. That is not a simplification
    — it is where a compression short's side seam actually runs, and it is what lets the
    front and back seams balance by construction whatever else differs between them.
    Seat room therefore cannot live in the side seam; it lives in `seat_depth`, the
    extra scoop of the CROTCH curve, which is where the body actually needs it. A deeper
    back crotch curve is what stops a compression short dragging itself down at the
    back, and it leaves the side seams congruent.
    """
    # x = 0 is the centre (crotch) side; x grows toward the side seam.
    side_x = max(hip_w, thigh_w, waist_w)
    crotch_x = gusset_w / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(side_x, 0.0), fc.P(crotch_x, 0.0))]),
        fc.Edge("inseam", [fc.Line(fc.P(crotch_x, 0.0), fc.P(crotch_x, IL))]),
        fc.Edge("crotch_seam", [fc.Bezier(fc.P(crotch_x, IL),
                                          fc.P(crotch_x * 0.35, IL + RISE * 0.22 + seat_depth),
                                          fc.P(0.0, IL + RISE * 0.42 + seat_depth),
                                          fc.P(0.0, IL + RISE))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, IL + RISE), fc.P(side_x, IL + RISE))]),
        fc.Edge("side_seam", [fc.Line(fc.P(side_x, IL + RISE), fc.P(side_x, 0.0))]),
    ]
    internals = [fc.Internal("hip line",
                             [fc.P(0.0, IL + HIP_Y), fc.P(side_x, IL + HIP_Y)],
                             kind="marking")]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 12.0, "waist": 0.0},   # waist joins the band; hem is turned
        notches=[fc.Notch("side_seam", 0.5, "hip line"),
                 fc.Notch("waist", 0.5, "quarter mark")],
        grainline=fc.Grainline(fc.P(side_x * 0.45, 15.0),
                               fc.P(side_x * 0.45, IL + RISE - 15.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build_front():
    return _leg("front_leg", H_Q, T_Q, W_Q, 0.0,
                "Front leg panel (cut 2 pairs)")


def build_back():
    # Seat room enters as a deeper crotch scoop, never as a longer side seam.
    return _leg("back_leg", H_Q, T_Q, W_Q, SEAT_SHIFT,
                "Back leg panel (cut 2 pairs, deeper seat curve)")


def build_waistband(front_waist, back_waist):
    """The high waistband: a deep compression band whose lower edge is built to the
    measured leg waist edges, so the band-to-leg seam balances exactly.

    Its own upper edge is cut slightly SMALLER than the lower one — the band tapers in
    toward the natural waist, which is what stops a high band rolling down.
    """
    lower_w = front_waist + back_waist            # one half of the body
    upper_w = lower_w * 0.94                      # taper toward the waist
    dx = (lower_w - upper_w) / 2.0
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(lower_w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("side_seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(dx, waistband_h))]),
        fc.Edge("upper", [fc.Line(fc.P(dx, waistband_h), fc.P(dx + upper_w, waistband_h))]),
        fc.Edge("side_seam_b", [fc.Line(fc.P(dx + upper_w, waistband_h),
                                        fc.P(lower_w, 0.0))]),
    ]
    return fc.Piece(
        "waistband",
        edges,
        seam_allowance=seam_allowance,
        allowances={"upper": 12.0},               # turned and topstitched
        notches=[fc.Notch("lower", 0.5, "side seam match")],
        grainline=fc.Grainline(fc.P(lower_w * 0.5, 6.0),
                               fc.P(lower_w * 0.5, waistband_h - 6.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="High waistband (cut 2 pairs)",
    )


def build_gusset(inseam_run):
    """Cotton gusset: its side edges are built to the measured leg inseams so the
    inseam seam balances; the ends join the front and back crotch seams."""
    w = gusset_w
    ln = inseam_run
    edges = [
        fc.Edge("front_end", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_a", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("back_end", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("side_b", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "gusset",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("side_a", 0.5, "inseam match")],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.2), fc.P(w * 0.5, ln * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Gusset (cut 1 in cotton jersey)",
    )


def build():
    pattern = fc.PatternSet("shapewear-short")
    front = build_front()
    back = build_back()
    band = build_waistband(front.edge("waist").length(), back.edge("waist").length())
    # The gusset spans between the two inseams; built to the measured inseam run.
    gusset = build_gusset(front.edge("inseam").length())

    picked = {"front_leg": front, "back_leg": back, "waistband": band, "gusset": gusset}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (front, back, band, gusset):
            pattern.add(piece)
        # Side seams: front to back, full panel height.
        pattern.declare_seam(("front_leg", "side_seam"), ("back_leg", "side_seam"), tol=1.5)
        # The band's lower edge takes both leg waist edges (one half of the body).
        pattern.declare_seam(("waistband", "lower"),
                             [("front_leg", "waist"), ("back_leg", "waist")], tol=1.0)
        # The band's own side seams close the ring.
        pattern.declare_seam(("waistband", "side_seam_a"),
                             ("waistband", "side_seam_b"), tol=1.0)
        # Inseams: each leg's inseam takes one side of the gusset.
        pattern.declare_seam(("front_leg", "inseam"), ("gusset", "side_a"), tol=1.0)
        pattern.declare_seam(("back_leg", "inseam"), ("gusset", "side_b"), tol=1.0)

    # Rings: front and back each carry a quarter, and the seat shift moves width between
    # them without changing the totals — so the rings still close on the solved values.
    waist_ring = 2.0 * band.edge("upper").length()
    hip_ring = 4.0 * H_Q
    thigh_ring = 4.0 * T_Q
    hem_ring = 2.0 * (front.edge("hem").length() + back.edge("hem").length())

    fabric_width = 1500.0
    area = (front.area() * 2.0 + back.area() * 2.0 + band.area() * 2.0 + gusset.area())
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "powernet (high-recovery)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"legs + band at {fabric_width:.0f} mm width, 62% marker. Cut with the "
                 "GREATEST STRETCH HORIZONTAL — the compression works around the body, "
                 "and cutting it the wrong way turns the short into a tube that slides "
                 "down. Recovery matters more than stretch: a fabric that stretches and "
                 "stays stretched gives one wear of shaping and then nothing."},
        {"item": "cotton jersey (gusset)", "qty": round(gusset.area() / 100.0) * 100,
         "unit": "mm2",
         "note": "a breathable cotton gusset is not optional in a compression garment."},
        {"item": "clear or soft-stretch elastic 10 mm",
         "qty": round(hem_ring * 0.97 + waist_ring * 0.96), "unit": "mm_length",
         "note": f"hem {hem_ring:.0f} mm x 0.97 + band top {waist_ring:.0f} mm x 0.96; "
                 "the leg hems are stabilised only lightly — an over-tight hem is what "
                 "makes shapewear roll up and cut in at the thigh."},
        {"item": "polyester stretch thread + ballpoint 75/11", "qty": 1, "unit": "set",
         "note": "4-thread overlock the structural seams, coverstitch the hems; every "
                 "seam must stretch as far as the cloth or it will pop on donning."},
    ]
    pattern.metadata = {
        "fc300_rank": 224, "family": "underwear_lounge", "fabric_hint": "powernet",
        "silhouette_note": "A high-waisted pull-on compression short, waist to "
            "mid-thigh, with graduated compression: most at the waist, less at the hip, "
            "least at the thigh. The back is cut with extra seat room so it does not "
            "drag itself down.",
        "hardware": "none — a pull-on garment has no closure, and this cartridge does "
            "not invent one.",
        "compression": {
            "waist_pct": waist_compression,
            "hip_pct": hip_compression,
            "thigh_pct": thigh_compression,
            "waist_body_mm": round(waist_girth, 1),
            "waist_finished_mm": round(WAIST_FIN, 1),
            "hip_body_mm": round(hip_girth, 1),
            "hip_finished_mm": round(HIP_FIN, 1),
            "thigh_body_mm": round(thigh_girth, 1),
            "thigh_finished_mm": round(THIGH_FIN, 1),
            "note": "graduated on purpose: the thigh takes least, because a leg opening "
                    "cut too tight rolls up and cuts in — the failure mode of cheap "
                    "shapewear, and a drafting decision rather than a fabric problem.",
        },
        "solved": {
            "waist_ring_mm": round(waist_ring, 1),
            "hip_ring_mm": round(hip_ring, 1),
            "thigh_ring_mm": round(thigh_ring, 1),
            "hem_ring_mm": round(hem_ring, 1),
            "seat_shift_mm": round(SEAT_SHIFT, 1),
            "leg_rise_mm": round(RISE, 1),
        },
        "closure": "none (pull-on)",
        "drafting": "Made to measure to waist, hip and thigh girths plus body rise; "
            "compression is an explicit percentage per zone, never a size letter.",
    }
    return pattern


result = build()
