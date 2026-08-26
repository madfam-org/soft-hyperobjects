"""
Climbing harness short — Fashion Cabinet Garment Cartridge
(FC-500 rank #452, active_swim, Yantra4D-bridged ladder-lock).

A stretch climbing short with an INTEGRATED soft harness: a durable Cordura short whose waist
belt and leg loops are structural webbing channels, adjusted on ladder-lock buckles, so the short
IS the harness for bouldering, via ferrata and gym use. (Not a certified fall-arrest harness — a
soft support short; the load webbing is the drafted structure, the short is its carrier.)

Two real decisions:

  1. THE BELT WEBBING IS SOLVED TO THE WAIST — THE DIMENSIONAL HANDSHAKE. The waist belt is a
     webbing channel closed on a ladder-lock; the webbing width is the drafted webbing_w that
     drives BOTH the Yantra4D ladder-lock webbing slots AND the garment's harness-belt interface.

  2. NEGATIVE EASE + ONE SHARED CROTCH + CLAMPED LEG LOOP. The short is cut at negative ease so it
     climbs with the body; front and back share ONE crotch so the leg cannot twist; the leg-loop
     webbing rise is clamped under the inseam so the loop never runs past the leg hem.

Pieces: front (cut 2), back (cut 2), belt (cut 1 webbing carrier). Made to measure to waist, hip,
thigh, inseam. FC-500 lane 6 (active).

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
# front|back|belt|set

waist_girth = float(PARAM(lambda: waist_girth, 840.0))
hip_girth = float(PARAM(lambda: hip_girth, 1000.0))
thigh_girth = float(PARAM(lambda: thigh_girth, 580.0))
inseam = float(PARAM(lambda: inseam, 200.0))
loop_rise = float(PARAM(lambda: loop_rise, 90.0))
webbing_w = float(PARAM(lambda: webbing_w, 40.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(600.0, min(waist_girth, 1300.0))
hip_girth = max(760.0, min(hip_girth, 1500.0))
thigh_girth = max(400.0, min(thigh_girth, 820.0))
inseam = max(120.0, min(inseam, 340.0))
loop_rise = max(40.0, min(loop_rise, 180.0))
webbing_w = max(25.0, min(webbing_w, 60.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 18.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))

NEG = 1.0 - negative_ease_pct / 100.0
HIP_FIN = hip_girth * NEG
WAIST_FIN = waist_girth * NEG
THIGH_FIN = thigh_girth * NEG
QUARTER_HIP = HIP_FIN / 4.0
THIGH_HALF = THIGH_FIN / 2.0
RISE = inseam + 120.0                          # short body rise above the crotch
CROTCH_X = -QUARTER_HIP * 0.14
LOOP = min(loop_rise, inseam * 0.7)            # leg-loop webbing rise clamped under the inseam


def _short(name, label, back):
    top = WAIST_FIN / 4.0
    hemw = THIGH_HALF
    rise = RISE + (30.0 if back else 0.0)
    cf = "centre_back" if back else "centre_front"
    edges = [
        fc.Edge("waist", [fc.Line(fc.P(0.0, rise), fc.P(top, rise))]),
        fc.Edge("side", [fc.Line(fc.P(top, rise), fc.P(hemw, inseam))]),
        fc.Edge("hem", [fc.Line(fc.P(hemw, inseam), fc.P(CROTCH_X, inseam))]),
        fc.Edge("inseam", [fc.Line(fc.P(CROTCH_X, inseam), fc.P(CROTCH_X, 0.0))]),
        fc.Edge(cf, [fc.Bezier(fc.P(CROTCH_X, 0.0), fc.P(top * 0.24, rise * 0.3),
                               fc.P(0.0, rise * 0.7), fc.P(0.0, rise))]),
    ]
    internals = [fc.Internal("leg-loop-web", [fc.P(CROTCH_X + 10.0, inseam - LOOP),
                                              fc.P(hemw - 20.0, inseam - LOOP)], kind="marking")]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance, allowances={"hem": 20.0},
        notches=[fc.Notch("side", 0.5, "hip"), fc.Notch("inseam", 0.5, "crotch")],
        grainline=fc.Grainline(fc.P(top * 0.5, rise * 0.3), fc.P(top * 0.5, rise * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True), label=label)


def build_front():
    return _short("front", "Short front (leg-loop webbing)", back=False)


def build_back():
    return _short("back", "Short back (raised, leg-loop webbing)", back=True)


def build_belt():
    """The harness belt (cut 1): a wide webbing-carrier band round the waist, closed on the
    ladder-lock. Length is the waist ring plus a long adjustment tail."""
    ln = WAIST_FIN + webbing_w * 4.0
    w = webbing_w * 1.6
    return fc.Piece(
        "belt", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "centre back"), fc.Notch("attach", 0.25, "left side"),
                 fc.Notch("attach", 0.75, "right side")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=[fc.Internal("ladder-lock", [fc.P(ln - webbing_w * 2.0, w * 0.5),
                                               fc.P(ln, w * 0.5)], kind="marking"),
                   fc.Internal("belay-loop", [fc.P(ln * 0.5, 0.0), fc.P(ln * 0.5, w)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1), label="Harness belt (webbing, ladder-lock)")


def build():
    pattern = fc.PatternSet("climbing-harness-short")
    every = target_piece == "set"
    front = build_front()
    back = build_back()
    belt = build_belt()
    picked = {"front": front, "back": back, "belt": belt}
    if not every:
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (front, back, belt):
        pattern.add(piece)
    pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5,
                         ease=(front.edge("side").length() - back.edge("side").length()))
    pattern.declare_seam(("front", "inseam"), ("back", "inseam"), tol=1.0)
    pattern.declare_seam(("belt", "attach"),
                         [("front", "waist"), ("front", "waist"),
                          ("back", "waist"), ("back", "waist")], tol=2.5,
                         ease=(belt.edge("attach").length()
                               - 2.0 * (front.edge("waist").length()
                                        + back.edge("waist").length())))
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "stretch Cordura short cloth + structural webbing",
                "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "an abrasion-resistant stretch short at negative ease with load-bearing webbing "
                 "sewn through the belt and leg loops."},
        {"item": "ladder-lock buckles (Yantra4D ladder-lock)", "qty": 2, "unit": "piece",
         "note": f"the waist and leg adjusters, webbing {webbing_w:.0f} mm = the webbing_w that "
                 "drives the harness-belt interface AND the ladder-lock slots; the buckle solid "
                 "is Yantra4D, never modelled here."},
        {"item": "harness webbing + belay loop", "qty": round(WAIST_FIN * 1.5 + LOOP * 4.0),
         "unit": "mm_length",
         "note": "the structural belt and leg-loop webbing plus a stitched belay loop."},
        {"item": "bar-tack thread", "qty": 1, "unit": "spool",
         "note": "bar-tack every load junction; the webbing carries the load, the cloth carries "
                 "the webbing."},
    ]
    pattern.metadata = {
        "fc500_rank": 452, "family": "active_swim", "fabric_hint": "nylon-cordura",
        "silhouette_note": "A stretch climbing short with an integrated soft harness: structural "
            "waist-belt and leg-loop webbing on ladder-lock buckles.",
        "hardware": "ladder-lock adjusters via Yantra4D (notion.hardware_ref -> ladder-lock); "
            "webbing_w drives the harness-belt interface AND the ladder-lock slots.",
        "solver": {
            "loop_mm": round(LOOP, 1), "rise_mm": round(RISE, 1),
            "note": "the leg-loop webbing rise is clamped under 0.7x the inseam so the loop never "
                    "runs past the leg hem; the front and back share ONE crotch so the leg cannot "
                    "twist; negative ease so the short climbs with the body.",
        },
        "active": {"use": "bouldering, via ferrata and gym; the short IS the soft support harness "
                   "(not a certified fall-arrest harness).",
                   "safety": "soft support only — not a certified EN 12277 fall-arrest harness."},
    }
    return pattern


result = build()
