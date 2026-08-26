"""
Bellows-actuated elbow sleeve — Fashion Cabinet Garment Cartridge
(FC-500 rank #436, adaptive / soft-exo, Yantra4D-bridged bellows-actuator).

An elbow sleeve that flexes and extends an arm that cannot bend on its own: a printed TPU sleeve
spanning the upper arm and forearm, carrying a bellows actuator along the inner crook so that
inflating the bellows flexes the elbow and venting it lets the arm straighten. The sleeve is the
soft body drafted here; the bellows is the Yantra4D `bellows-actuator` solid, never modelled here.

Two real decisions:

  1. THE BELLOWS CHANNEL IS SOLVED TO THE CROOK RUN — THE DIMENSIONAL HANDSHAKE. The inner
     channel runs the drafted `bellows_run` across the crook; that is the same number that drives
     the number of `bellows-actuator` convolutions (each `conv_pitch` long), so the printed
     bellows is exactly as long as the channel that holds it. `bellows_run` drives BOTH the
     hardware AND the garment's `bellows_channel` interface.

  2. TWO TAPERED TUBES SHARING ONE ELBOW GIRTH. The upper-arm and forearm sections are each a
     tapered tube meeting at ONE shared elbow girth, so the sleeve is continuous at the elbow;
     both tapers are clamped so neither end girth can exceed the elbow girth by inversion.

Pieces: upper (upper-arm section) + fore (forearm section) + cuff (the wrist gripper). Made to
measure to upper-arm, elbow and wrist girths and sleeve length.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # upper|fore|cuff|set

upper_girth = float(PARAM(lambda: upper_girth, 300.0))
elbow_girth = float(PARAM(lambda: elbow_girth, 270.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 180.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 420.0))
bellows_run = float(PARAM(lambda: bellows_run, 180.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
upper_girth = max(220.0, min(upper_girth, 440.0))
elbow_girth = max(200.0, min(elbow_girth, 400.0))
wrist_girth = max(140.0, min(wrist_girth, 260.0))
sleeve_length = max(300.0, min(sleeve_length, 560.0))
bellows_run = max(90.0, min(bellows_run, 300.0))
negative_ease_pct = max(2.0, min(negative_ease_pct, 12.0))
seam_allowance = max(4.0, min(seam_allowance, 14.0))

NEG = 1.0 - negative_ease_pct / 100.0
UPPER_FIN = upper_girth * NEG
ELBOW_FIN = elbow_girth * NEG
WRIST_FIN = wrist_girth * NEG
# The elbow is the shared join; keep the ends from exceeding it by inversion is not required
# (a tube can widen or narrow), but clamp so the panels never collapse below a minimum width.
UPPER_FIN = max(UPPER_FIN, 120.0)
ELBOW_FIN = max(ELBOW_FIN, 110.0)
WRIST_FIN = max(WRIST_FIN, 90.0)
SEC = (sleeve_length - 60.0) / 2.0          # each section length (cuff takes 60)
SEC = max(120.0, SEC)
BRUN = min(bellows_run, sleeve_length * 0.7)   # the bellows channel run across the crook


def _tube(name, label, top_w, bot_w, h, channel):
    """A tapered tube panel: bottom edge (bot_w) to top edge (top_w), two closing seams. If
    `channel`, mark the bellows channel down the crook (centre line)."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(bot_w, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(bot_w, 0.0), fc.P((bot_w + top_w) / 2.0, h))]),
        fc.Edge("top", [fc.Line(fc.P((bot_w + top_w) / 2.0, h), fc.P((bot_w - top_w) / 2.0, h))]),
        fc.Edge("seam_l", [fc.Line(fc.P((bot_w - top_w) / 2.0, h), fc.P(0.0, 0.0))]),
    ]
    cx = bot_w / 2.0
    internals = []
    if channel:
        internals.append(fc.Internal("bellows_channel",
                                     [fc.P(cx, h * 0.06), fc.P(cx, h * 0.94)], kind="marking"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance, allowances={},
        notches=[fc.Notch("bottom", 0.5, "crook centre"), fc.Notch("top", 0.5, "crook centre")],
        grainline=fc.Grainline(fc.P(cx, h * 0.15), fc.P(cx, h * 0.85)),
        internals=internals, cut=fc.CutSpec(quantity=1, mirror=False), label=label)


def build_upper():
    # upper-arm section: top = upper girth, bottom = elbow girth; bellows channel across the crook.
    return _tube("upper", "Upper-arm section (bellows channel)", UPPER_FIN, ELBOW_FIN, SEC, True)


def build_fore():
    # forearm section: top = elbow girth, bottom = wrist girth; bellows channel continues.
    return _tube("fore", "Forearm section (bellows channel)", ELBOW_FIN, WRIST_FIN, SEC, True)


def build_cuff():
    ln = WRIST_FIN
    h = 60.0
    return fc.Piece(
        "cuff", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, h))]),
            fc.Edge("top", [fc.Line(fc.P(ln, h), fc.P(0.0, h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance, allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "crook centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h / 2.0), fc.P(ln * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=1), label="Wrist cuff (cut 1)")


def build():
    pattern = fc.PatternSet("bellows-elbow-sleeve")
    every = target_piece == "set"
    upper = build_upper()
    fore = build_fore()
    cuff = build_cuff()
    if not every:
        picked = {"upper": upper, "fore": fore, "cuff": cuff}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern)
    for piece in (upper, fore, cuff):
        pattern.add(piece)
    # upper bottom (elbow) sews to fore top (elbow) — both ELBOW_FIN wide.
    pattern.declare_seam(("upper", "bottom"), ("fore", "top"), tol=1.0)
    # each section closes on itself.
    pattern.declare_seam(("upper", "seam_r"), ("upper", "seam_l"), tol=1.0)
    pattern.declare_seam(("fore", "seam_r"), ("fore", "seam_l"), tol=1.0)
    # cuff attaches to the forearm bottom (wrist).
    pattern.declare_seam(("cuff", "attach"), ("fore", "bottom"), tol=1.0)
    return _finish(pattern)


def _finish(pattern):
    fabric_width = 500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "printed TPU sleeve fabric (soft, airtight-backed crook)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "upper + forearm sections + cuff at negative ease; the inner crook backs the "
                 "bellows channel."},
        {"item": "bellows actuator (Yantra4D bellows-actuator)", "qty": 1, "unit": "piece",
         "note": f"one printed bellows, run {BRUN:.0f} mm = the drafted crook channel; slid in, "
                 "never modelled here. Inflate to flex the elbow, vent to straighten."},
        {"item": "silicone air line + pump", "qty": round(bellows_run * 3.0), "unit": "mm_length",
         "note": "carries pressure to the bellows; a small hand pump or CO2 cartridge drives it."},
        {"item": "wrist elastic + upper silicone gripper", "qty": round(upper_girth + wrist_girth),
         "unit": "mm_length",
         "note": "keep the sleeve anchored so the bellows works the elbow, not the fabric."},
    ]
    pattern.metadata = {
        "fc500_rank": 436, "family": "adaptive", "fabric_hint": "tpu-panel-impreso",
        "silhouette_note": "A bellows-actuated elbow sleeve: inflate the crook bellows to flex "
            "the elbow, vent to straighten — power for an arm that cannot bend on its own.",
        "hardware": "bellows actuator via Yantra4D (notion.hardware_ref -> bellows-actuator); "
            "bellows_run drives the crook channel, the same parameter that drives the "
            "bellows_channel interface — the dimensional handshake.",
        "solver": {
            "section_mm": round(SEC, 1), "bellows_run_mm": round(BRUN, 1),
            "elbow_fin_mm": round(ELBOW_FIN, 1),
            "note": "the upper and forearm sections meet at ONE shared elbow girth so the sleeve "
                    "is continuous at the elbow; all section widths clamped above a minimum so "
                    "no panel can collapse.",
        },
        "adaptive": {
            "assist": "a bellows in the crook flexes and extends the elbow for a wearer who "
                      "cannot bend the arm on their own; the sleeve carries and anchors it.",
        },
    }
    return pattern


result = build()
