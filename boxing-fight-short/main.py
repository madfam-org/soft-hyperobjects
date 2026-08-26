"""
Boxing fight short — Fashion Cabinet Garment Cartridge
(FC-500 rank #457, active_swim, Yantra4D-bridged hook-loop-tape).

The wide, high-waisted boxing short of the ring: a loose, long-legged short in satin or lightweight
nylon with a broad elastic waistband, deep side vents for the guard and the kick of the leg, and a
hook-and-loop waistband tab so it cinches over the wraps and does not drop between rounds. Cut with
generous POSITIVE ease so it flares and moves; the waistband is the only fitted part.

Two real decisions:

  1. THE HOOK-LOOP TAB IS SOLVED TO THE WAISTBAND — THE DIMENSIONAL HANDSHAKE. The waistband tab
     closes on hook-and-loop; the tape strip length is the drafted waist_adjust that drives BOTH
     the Yantra4D hook-loop-tape strip AND the garment's waistband-adjust interface.

  2. POSITIVE EASE + ONE SHARED CROTCH + CLAMPED VENT. The short shares ONE crotch front-to-back so
     the leg cannot twist; the side vent rise is clamped under the leg length so the vent never
     runs past the waist.

Pieces: front (cut 2), back (cut 2), waistband (cut 1). Made to measure to waist, hip, leg length.
FC-500 lane 6 (active).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|waistband|set

waist_girth = float(PARAM(lambda: waist_girth, 880.0))
hip_girth = float(PARAM(lambda: hip_girth, 1040.0))
leg_length = float(PARAM(lambda: leg_length, 420.0))       # waistband to leg hem
vent_rise = float(PARAM(lambda: vent_rise, 160.0))
wb_depth = float(PARAM(lambda: wb_depth, 90.0))
waist_adjust = float(PARAM(lambda: waist_adjust, 120.0))
positive_ease_pct = float(PARAM(lambda: positive_ease_pct, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1400.0))
hip_girth = max(760.0, min(hip_girth, 1600.0))
leg_length = max(240.0, min(leg_length, 620.0))
vent_rise = max(40.0, min(vent_rise, 320.0))
wb_depth = max(50.0, min(wb_depth, 180.0))
waist_adjust = max(60.0, min(waist_adjust, 240.0))
positive_ease_pct = max(15.0, min(positive_ease_pct, 90.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

POS = 1.0 + positive_ease_pct / 100.0
HIP_FIN = hip_girth * POS
QUARTER_HIP = HIP_FIN / 4.0
HEM_HALF = QUARTER_HIP * 1.08                  # the leg flares below the hip
CROTCH_X = -QUARTER_HIP * 0.16
VENT = min(vent_rise, leg_length * 0.75)       # side vent rise clamped under the leg


def _short(name, label, back):
    top = QUARTER_HIP
    hemw = HEM_HALF
    cf = "centre_back" if back else "centre_front"
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, leg_length), fc.P(top, leg_length))]),
        fc.Edge("side", [fc.Line(fc.P(top, leg_length), fc.P(hemw, VENT)),
                         fc.Line(fc.P(hemw, VENT), fc.P(hemw, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(hemw, 0.0), fc.P(CROTCH_X, 0.0))]),
        fc.Edge("inseam", [fc.Line(fc.P(CROTCH_X, 0.0), fc.P(CROTCH_X, leg_length * 0.42))]),
        fc.Edge(cf, [fc.Bezier(fc.P(CROTCH_X, leg_length * 0.42),
                               fc.P(top * (0.28 if back else 0.16), leg_length * 0.7),
                               fc.P(0.0, leg_length * 0.9), fc.P(0.0, leg_length))]),
    ]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance, allowances={"hem": 25.0},
        notches=[fc.Notch("side", 0.5, "vent top"), fc.Notch("inseam", 0.5, "crotch")],
        grainline=fc.Grainline(fc.P(top * 0.5, leg_length * 0.3), fc.P(top * 0.5,
                leg_length * 0.85)),
        internals=[fc.Internal("side-vent", [fc.P(hemw, 0.0), fc.P(hemw, VENT)], kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True), label=label)


def build_front():
    return _short("front", "Fight short front (vent)", back=False)


def build_back():
    return _short("back", "Fight short back (vent)", back=True)


# The waistband length is the measured waist edges plus the hook-loop adjust overlap.
_FW = build_front().edge("waist").length(0.2)
_BW = build_back().edge("waist").length(0.2)
WB_LENGTH = 2.0 * _FW + 2.0 * _BW + waist_adjust


def build_waistband():
    ln, w = WB_LENGTH, wb_depth * 2.0
    return fc.Piece(
        "waistband", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"fold_top": 0.0},
        notches=[fc.Notch("attach", 0.25, "left side"), fc.Notch("attach", 0.5, "centre back"),
                 fc.Notch("attach", 0.75, "right side")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("hook-loop-tab", [fc.P(ln - waist_adjust, w * 0.5),
                                                 fc.P(ln, w * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=1), label="Broad waistband (hook-loop tab)")


def build():
    pattern = fc.PatternSet("boxing-fight-short")
    every = target_piece == "set"
    if every or target_piece == "front":
        pattern.add(build_front())
    if every or target_piece == "back":
        pattern.add(build_back())
    if every or target_piece == "waistband":
        pattern.add(build_waistband())
    if every:
        f = pattern.piece("front")
        b = pattern.piece("back")
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5,
                             ease=(f.edge("side").length() - b.edge("side").length()))
        pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.0)
        pattern.declare_seam(("waistband", "attach"),
                             [("front", "waist"), ("front", "waist"),
                              ("back", "waist"), ("back", "waist")], tol=2.0, ease=waist_adjust)
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "boxing satin (or lightweight nylon)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "a shiny satin with generous positive ease so the short flares and moves with the "
                 "guard and the kick."},
        {"item": "hook-and-loop tape (Yantra4D hook-loop-tape)", "qty": 1, "unit": "piece",
         "note": f"the waistband adjust tab, strip {waist_adjust:.0f} mm = the waist_adjust that "
                 "drives the waistband-adjust interface AND the hook-loop-tape strip; the tape "
                 "solid is Yantra4D, never modelled here."},
        {"item": "broad waistband elastic", "qty": round(waist_girth + waist_adjust),
                "unit": "mm_length",
         "note": "a wide elastic waistband that cinches over the hand wraps between rounds."},
        {"item": "satin binding + thread", "qty": round(VENT * 4.0 + 100.0), "unit": "mm_length",
         "note": "bind the deep side vents and the leg hems."},
    ]
    pattern.metadata = {
        "fc500_rank": 457, "family": "active_swim", "fabric_hint": "nylon-satinado",
        "silhouette_note": "A wide, high-waisted boxing fight short: loose satin legs with deep "
            "side vents, a broad elastic waistband adjusted on a hook-and-loop tab.",
        "hardware": "hook-and-loop waistband tab via Yantra4D (notion.hardware_ref -> "
            "hook-loop-tape); waist_adjust drives the waistband-adjust interface AND the tape "
            "strip — the dimensional handshake.",
        "solved": {
            "vent_mm": round(VENT, 1), "hip_finished_mm": round(HIP_FIN, 1),
            "wb_length_mm": round(WB_LENGTH, 1),
            "note": "the short shares ONE crotch front-to-back so the leg cannot twist; the side "
                    "vent rise is clamped under 0.75x the leg so it never runs past the waist; "
                    "generous positive ease so the short flares.",
        },
        "active": {"use": "boxing and Muay Thai; a wide short that flares over the guard and kick, "
                   "waist cinched over the wraps on hook-and-loop."},
    }
    return pattern


result = build()
