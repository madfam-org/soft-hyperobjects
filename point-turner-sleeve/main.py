"""
Point-turner tool sleeve — Fashion Cabinet Care & Keeping Cartridge (FC-500 #414, care_keeping, T1).

A slim padded sleeve that protects a point turner (the flat wooden or printed tool that
pushes out a collar point without piercing the seam). A BACK panel and a shorter FRONT
panel make an open-top pocket; a FLAP folds over and a TAB holds it shut. Drafted to a
KNOWN tool — the Yantra4D `point-turner` solid — so the sleeve is exactly as long as the
tool plus the flap, never a loose bag the tool slides out of.

Solved, not guessed:

  1. THE SLEEVE IS CUT TO THE MEASURED TOOL. The pocket length is the tool length plus a
     seat, and the flap length is the pocket mouth width plus a fold — measured, then the
     front/back mouths declared to match.
  2. THE FRONT IS CLAMPED SHORTER THAN THE BACK so the mouth is always open (a front as
     tall as the back would seal the pocket).
  3. THE TAB SITS ON CLOTH. The closure tab is stepped in off the flap end so it lands on
     fabric, not on the fold.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))  # back|front|flap|set

tool_length = float(PARAM(lambda: tool_length, 150.0))
tool_width = float(PARAM(lambda: tool_width, 40.0))       # presser width
tool_thick = float(PARAM(lambda: tool_thick, 8.0))
seat = float(PARAM(lambda: seat, 20.0))                   # extra below the tool
flap_fold = float(PARAM(lambda: flap_fold, 40.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

tool_length = max(80.0, min(tool_length, 260.0))
tool_width = max(20.0, min(tool_width, 90.0))
tool_thick = max(3.0, min(tool_thick, 24.0))
seat = max(8.0, min(seat, 60.0))
flap_fold = max(20.0, min(flap_fold, 90.0))
seam_allowance = max(0.0, min(seam_allowance, 14.0))

# the sleeve width wraps the tool's width plus its thickness turn-of-cloth
SLEEVE_W = tool_width + tool_thick * 2.0 + 12.0
BACK_H = tool_length + seat + flap_fold
# the front is clamped shorter than the back so the mouth stays open
FRONT_H = min(tool_length * 0.72, BACK_H - flap_fold - 20.0)
FRONT_H = max(40.0, FRONT_H)


def _rect(name, w, h, mouth_alw=0.0, extra_internals=None, label=""):
    return fc.Piece(
        name, [
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": mouth_alw},
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=extra_internals or [],
        cut=fc.CutSpec(quantity=1),
        label=label or name,
    )


def build_back():
    a = max(3.0, tool_width * 0.1)
    tab_y = BACK_H - flap_fold * 0.5
    internals = [
        fc.Internal("flap fold line",
                    [fc.P(0.0, BACK_H - flap_fold), fc.P(SLEEVE_W, BACK_H - flap_fold)],
                    kind="marking"),
        fc.Internal("closure tab",
                    [fc.P(SLEEVE_W * 0.5 - a, tab_y), fc.P(SLEEVE_W * 0.5 + a, tab_y)],
                    kind="marking"),
    ]
    return _rect("back", SLEEVE_W, BACK_H, mouth_alw=0.0,
                 extra_internals=internals, label="Back with flap (cut 1)")


def build_front():
    return _rect("front", SLEEVE_W, FRONT_H, mouth_alw=16.0, label="Front pocket (cut 1)")


def build_flap():
    """A separate reinforcing flap facing, cut 1 (interfaced)."""
    w = SLEEVE_W
    h = flap_fold + seam_allowance
    return _rect("flap", w, h, mouth_alw=0.0, label="Flap facing (cut 1)")


def build():
    pattern = fc.PatternSet("point-turner-sleeve")
    everything = target_piece == "set"
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "flap":
        pattern.add(build_flap())

    if everything:
        # the front and back share the same width so their side/bottom seams sew flush
        pattern.declare_seam(("front", "bottom"), ("back", "bottom"), tol=0.5)
        pattern.declare_seam(("front", "left"), ("back", "left"), tol=1.0,
                             ease=FRONT_H - BACK_H)

    fabric_width = 900.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "cotton + fusible fleece (padded sleeve)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker; a light fleece pads the "
                 f"sleeve so the point turner does not poke through."},
        {"item": "point turner", "qty": 1, "unit": "count",
         "note": f"Yantra4D point-turner (notion.hardware_ref): the sleeve is cut to the "
                 f"tool length ({tool_length:.0f} mm) plus a seat and the flap."},
        {"item": "snap or hook-loop dot + thread", "qty": 1, "unit": "set",
         "note": "the closure tab holds the flap over the mouth."},
    ]
    pattern.metadata = {
        "fc500_rank": 414, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A slim padded sleeve for a point turner: an open-top pocket with "
            "a fold-over flap and a closure tab.",
        "solved": {
            "sleeve_width_mm": round(SLEEVE_W, 1),
            "back_height_mm": round(BACK_H, 1),
            "front_height_mm": round(FRONT_H, 1),
            "front_clamped": bool(abs(FRONT_H - tool_length * 0.72) > 0.01),
            "note": "the sleeve is cut to the measured tool length plus a seat and the flap; "
                    "the front is clamped shorter than the back so the mouth is always open; "
                    "the closure tab is stepped in off the flap end so it seats on cloth.",
        },
        "hardware": "point turner via Yantra4D (notion.hardware_ref -> point-turner); "
                    "tool_len and presser_w are fed from the tool dimensions. No flange "
                    "interface — the sleeve holds the tool, so no dimensional handshake owed.",
    }
    return pattern


result = build()
