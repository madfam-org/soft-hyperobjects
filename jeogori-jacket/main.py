"""
Jeogori (저고리) maedeup — Fashion Cabinet Cartridge (FC-400 #394; y4d frog-closure co-create).

The jeogori is the short upper jacket of the Korean hanbok — cropped at the ribcage, with a
deep curved collar band (깃, `git`) faced in a removable white strip (동정, `dongjeong`) and
wide gently-curved sleeves. The FC-300 hanbok-jeogori is drafted with the traditional long
ribbon ties (고름, `goreum`). THIS jeogori is the variant fastened with knotted cloth buttons
(매듭단추, `maedeup-danchu`) — the Korean decorative-knot-and-loop closure worn on some jeogori,
magoja and durumagi — a distinct garment in the same family, and the reason this rank names the
`frog-closure` hardware as a Group-B co-creation.

What actually makes a jeogori a jeogori, and what this draft encodes:

  1. THE GIT IS A DEEP CURVED COLLAR BAND, AND ITS LENGTH IS MEASURED. The git runs down the
     right front, around the back neck, and down the left front, crossing over itself at the
     centre front (the jeogori laps right-over-left). Its length is the SOLVED run of the
     neckline it faces, not a guess, so the collar closes flat. The dongjeong is a narrow white
     strip cut to the git's visible edge.

  2. THE MAEDEUP CLOSURE IS A KNOT-AND-LOOP, NOT A BUTTON THROUGH A HOLE. A maedeup-danchu is a
     cloth knot on one lap that passes through a corded loop on the other. This cartridge draws
     the loop tab and the knot-button seat, and wires them to the `frog-closure` Yantra4D solid
     as a CO-CREATION (the FC-300 frog-closure carry-over): `span` = the closure width, `knots`
     = the knot count. The closure is decorative and structural at once, which is why the
     jeogori laps closed by it rather than tying.

Pieces: back, front (cut 2 — the lapping fronts), sleeve, git (collar band), dongjeong (white
collar strip), loop_tab (the maedeup loop). Made to measure to chest girth, jacket length,
sleeve length and neck run. The jeogori is SHORT — cropped just below the bust — by tradition.

Cultural note (stated): the jeogori is core Korean traditional dress; proportions differ by
era and gender and this is a plain everyday women's-style short jeogori. The maedeup knotwork
is a living Korean craft (매듭); this cartridge draws the closure seat and defers the knot
pattern itself to the maker, inventing none.

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

chest_girth = float(PARAM(lambda: chest_girth, 920.0))
jacket_length = float(PARAM(lambda: jacket_length, 240.0))   # nape to the short hem
sleeve_length = float(PARAM(lambda: sleeve_length, 520.0))
bicep_girth = float(PARAM(lambda: bicep_girth, 340.0))
git_width = float(PARAM(lambda: git_width, 55.0))            # collar band finished width
dongjeong_width = float(PARAM(lambda: dongjeong_width, 22.0))  # white strip width
lap_depth = float(PARAM(lambda: lap_depth, 180.0))          # how far the fronts cross
closure_span = float(PARAM(lambda: closure_span, 60.0))     # maedeup closure width
knot_count = float(PARAM(lambda: knot_count, 1.0))          # knot buttons
ease_pct = float(PARAM(lambda: ease_pct, 16.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1400.0))
jacket_length = max(160.0, min(jacket_length, 420.0))
sleeve_length = max(300.0, min(sleeve_length, 680.0))
bicep_girth = max(240.0, min(bicep_girth, 560.0))
git_width = max(30.0, min(git_width, 100.0))
dongjeong_width = max(12.0, min(dongjeong_width, 45.0))
lap_depth = max(80.0, min(lap_depth, 300.0))
closure_span = max(30.0, min(closure_span, 140.0))
knot_count = max(1.0, min(round(knot_count), 5.0))
ease_pct = max(6.0, min(ease_pct, 28.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

dongjeong_width = min(dongjeong_width, git_width - 6.0)
lap_depth = min(lap_depth, jacket_length - 40.0)

# ── Geometry ─────────────────────────────────────────────────────────────────
EASE = 1.0 + ease_pct / 100.0
CHEST_CUT = chest_girth * EASE
BODY_HALF = CHEST_CUT / 4.0
H = jacket_length
ARM_DEPTH = H * 0.72                # a short jeogori's armhole is deep relative to length
ARM_DEPTH = min(ARM_DEPTH, H - 30.0)


def build_back():
    """Back panel (cut 1 on fold): a short rectangle with a shallow back-neck scoop."""
    w = BODY_HALF
    h = H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(0.0, h),
                                       fc.P(w * 0.24, h),
                                       fc.P(w * 0.36, h - 6.0),
                                       fc.P(w * 0.46, h - 10.0))]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.46, h - 10.0), fc.P(w * 0.9, h - 14.0))]),
        fc.Edge("armhole", [fc.Bezier(fc.P(w * 0.9, h - 14.0),
                                      fc.P(w * 0.98, h - ARM_DEPTH * 0.4),
                                      fc.P(w, h - ARM_DEPTH * 0.75),
                                      fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("side", [fc.Line(fc.P(w, h - ARM_DEPTH), fc.P(w, 0.0))]),
    ]
    return fc.Piece(
        "back", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "center_back": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match")],
        grainline=fc.Grainline(fc.P(w * 0.4, h * 0.15), fc.P(w * 0.4, h * 0.8)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back (깃 body, cut 1 on fold)")


def build_front():
    """A front (cut 2): the lapping front. Its centre-front edge is a diagonal from the neck
    point down-and-in to the lap, so the two fronts cross right-over-left. Carries the collar
    edge and, on the overlap, the maedeup loop seat.
    """
    w = BODY_HALF
    h = H
    # neck point at the shoulder, collar edge diagonal down to the lap at centre
    neck_pt = fc.P(w * 0.46, h - 10.0)
    lap_bottom = fc.P(w * 0.06, h - lap_depth)      # where the lap crosses, near CF
    edges = [
        fc.Edge("collar_edge", [fc.Bezier(neck_pt,
                                          fc.P(w * 0.30, h - lap_depth * 0.35),
                                          fc.P(w * 0.14, h - lap_depth * 0.75),
                                          lap_bottom)]),
        fc.Edge("center_front", [fc.Line(lap_bottom, fc.P(0.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w, h - ARM_DEPTH))]),
        fc.Edge("armhole", [fc.Bezier(fc.P(w, h - ARM_DEPTH),
                                      fc.P(w, h - ARM_DEPTH * 0.75),
                                      fc.P(w * 0.98, h - ARM_DEPTH * 0.4),
                                      fc.P(w * 0.9, h - 14.0))]),
        fc.Edge("shoulder", [fc.Line(fc.P(w * 0.9, h - 14.0), neck_pt)]),
    ]
    internals = [fc.Internal("maedeup closure seat",
                             [fc.P(w * 0.22, h - lap_depth + closure_span * 0.5),
                              fc.P(w * 0.22 + closure_span, h - lap_depth + closure_span * 0.5)],
                             kind="marking")]
    return fc.Piece(
        "front", edges, seam_allowance=seam_allowance,
        allowances={"hem": 20.0, "collar_edge": 0.0},
        notches=[fc.Notch("armhole", 0.5, "sleeve match"),
                 fc.Notch("collar_edge", 1.0, "lap point")],
        grainline=fc.Grainline(fc.P(w * 0.55, h * 0.15), fc.P(w * 0.55, h * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (lapping right-over-left, cut 2)")


def build_sleeve(armhole_ring):
    """Wide gently-curved jeogori sleeve (cut 2): cap solved to the armhole, to a curved cuff."""
    wrist = min(bicep_girth * EASE * 0.82, armhole_ring * 0.85)
    ln = sleeve_length
    cap_w = min(armhole_ring * 0.95, wrist * 1.5)
    bow = ARM_DEPTH * 0.5
    for _ in range(40):
        test = fc.Edge("t", [fc.Bezier(fc.P(0.0, ln),
                                       fc.P(cap_w * 0.25, ln + bow),
                                       fc.P(cap_w * 0.75, ln + bow),
                                       fc.P(cap_w, ln))]).length()
        if test < 1e-6:
            break
        ratio = armhole_ring / test
        if ratio > 1.0:
            cap_w = min(cap_w * ratio, armhole_ring)
        else:
            bow = max(4.0, bow * ratio)
        cap_w = max(wrist + 10.0, cap_w)
        if abs(test - armhole_ring) < 0.4:
            break
    cuff_off = (cap_w - wrist) / 2.0
    edges = [
        fc.Edge("cuff", [fc.Bezier(fc.P(cuff_off, 0.0),
                                   fc.P(cuff_off + wrist * 0.35, -wrist * 0.06),
                                   fc.P(cuff_off + wrist * 0.65, -wrist * 0.06),
                                   fc.P(cuff_off + wrist, 0.0))]),
        fc.Edge("underseam_r", [fc.Line(fc.P(cuff_off + wrist, 0.0), fc.P(cap_w, ln))]),
        fc.Edge("cap", [fc.Bezier(fc.P(cap_w, ln),
                                  fc.P(cap_w * 0.75, ln + bow),
                                  fc.P(cap_w * 0.25, ln + bow),
                                  fc.P(0.0, ln))]),
        fc.Edge("underseam_l", [fc.Line(fc.P(0.0, ln), fc.P(cuff_off, 0.0))]),
    ]
    return fc.Piece(
        "sleeve", edges, seam_allowance=seam_allowance,
        allowances={"cuff": 20.0},
        notches=[fc.Notch("cap", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, ln * 0.15), fc.P(cap_w * 0.5, ln * 0.85)),
        cut=fc.CutSpec(quantity=2, mirror=True), label="Sleeve (소매, cut 2)")


def build_git(collar_run):
    """The git collar band (cut 1): a long strip, its length the measured collar run (both
    fronts' collar edges + the back neck), folded to its finished width.
    """
    ln = collar_run
    w = git_width * 2.0            # cut double, folds to finished width
    edges = [
        fc.Edge("neck_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("git fold", [fc.P(0.0, git_width), fc.P(ln, git_width)],
                             kind="marking")]
    return fc.Piece(
        "git", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("neck_edge", 0.5, "centre back neck")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.2), fc.P(ln * 0.1, w * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Git 깃 collar band (cut 1)")


def build_dongjeong(collar_run):
    """The dongjeong (cut 1): the removable white collar strip, along the git's visible edge."""
    ln = collar_run
    w = dongjeong_width
    edges = [
        fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("end_r", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("outer", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("end_l", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "dongjeong", edges, seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("inner", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.3), fc.P(ln * 0.1, w * 0.7)),
        cut=fc.CutSpec(quantity=1), label="Dongjeong 동정 white strip (cut 1)")


def build_loop_tab():
    """The maedeup loop tab (cut 1 per knot): a small strip forming the corded loop the knot
    button passes through. Cut width is the closure span; length allows the loop.
    """
    n = int(knot_count)
    ln = closure_span * 1.4
    w = closure_span
    edges = [
        fc.Edge("seam", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("loop_edge", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "loop_tab", edges, seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("loop_edge", 0.5, "knot passes here")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=n, mirror=False),
        label="Maedeup loop tab (cut 1 per knot)")


MEASURED = {}


def build():
    pattern = fc.PatternSet("jeogori-jacket")
    every = target_piece == "set"
    back = build_back()
    front = build_front()
    MEASURED["collar_run"] = (2.0 * front.edge("collar_edge").length()
                              + back.edge("neckline").length())
    armhole_ring = front.edge("armhole").length() + back.edge("armhole").length()

    if not every:
        picked = {"back": back, "front": front,
                  "sleeve": build_sleeve(armhole_ring),
                  "git": build_git(MEASURED["collar_run"]),
                  "dongjeong": build_dongjeong(MEASURED["collar_run"]),
                  "loop_tab": build_loop_tab()}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    sleeve = build_sleeve(armhole_ring)
    git = build_git(MEASURED["collar_run"])
    dongjeong = build_dongjeong(MEASURED["collar_run"])
    loop_tab = build_loop_tab()
    for piece in (back, front, sleeve, git, dongjeong, loop_tab):
        pattern.add(piece)
    pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5,
                         ease=(front.edge("shoulder").length()
                               - back.edge("shoulder").length()))
    pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    pattern.declare_seam(("sleeve", "cap"),
                         [("front", "armhole"), ("back", "armhole")], tol=2.5)
    # The git faces the whole collar run (both fronts' collar edges + back neck).
    pattern.declare_seam(("git", "neck_edge"),
                         [("front", "collar_edge"), ("front", "collar_edge"),
                          ("back", "neckline")], tol=2.0)
    # The dongjeong runs the same length as the git's outer visible edge.
    pattern.declare_seam(("dongjeong", "inner"), ("git", "outer"), tol=2.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    n_knots = int(knot_count)
    fabric_width = 1100.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "silk-ramie or fine cotton (jeogori cloth)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"body + sleeves + git at {fabric_width:.0f} mm width, 62% marker. Jeogori "
                 "cloth is light and often lined; the git and dongjeong are contrast pieces."},
        {"item": "white cotton for the dongjeong", "qty": 1, "unit": "piece",
         "note": "the dongjeong is REMOVABLE and washed/replaced separately — a defining detail "
                 "of hanbok upkeep."},
        {"item": "maedeup knot buttons + loops (Yantra4D frog-closure, co-create)",
         "qty": n_knots, "unit": "set",
         "note": f"{n_knots} maedeup-danchu knot-and-loop closure(s); span {closure_span:.0f} mm. "
                 "The frog-closure is a Yantra4D CO-CREATION (notion.hardware_ref, linked=false) "
                 "— the FC-300 frog-closure carry-over; span drives the closure width and knots "
                 "the count. The maedeup knotwork itself is the maker's craft, not drawn here."},
        {"item": "lining + thread", "qty": 1, "unit": "set",
         "note": "hand-finish the git and lap so the jeogori can be unpicked and washed flat."},
    ]
    pattern.metadata = {
        "fc400_rank": 394, "family": "heritage_global", "fabric_hint": "silk-ramie",
        "tradition": "Korean (저고리) — the short upper jacket of the hanbok, maedeup-fastened",
        "silhouette_note": "A SHORT jacket cropped just below the bust, lapping right-over-left, "
            "with a deep curved git collar faced in a removable white dongjeong and wide gently "
            "curved sleeves. Fastened by a knotted cloth-button (maedeup-danchu) closure rather "
            "than the goreum ties of the FC-300 hanbok-jeogori.",
        "hardware": "maedeup knot-button closure via Yantra4D frog-closure (CO-CREATION, "
            "notion.hardware_ref linked=false); span -> closure width, knots -> knot count.",
        "solved": {
            "chest_cut_mm": round(CHEST_CUT, 1),
            "jacket_length_mm": round(jacket_length, 1),
            "collar_run_mm": round(MEASURED.get("collar_run", 0.0), 1),
            "git_width_mm": round(git_width, 1),
            "closure_span_mm": round(closure_span, 1),
            "knot_count": n_knots,
            "note": "the git length is the SOLVED collar run (both fronts + back neck) so the "
                    "curved collar closes flat; the jeogori is short by tradition.",
        },
        "cultural_note": "The jeogori is core Korean traditional dress; proportions differ by "
            "era and gender, and this is a plain everyday women's-style short jeogori. The "
            "maedeup knotwork is a living Korean craft (매듭); this cartridge draws the closure "
            "seat and defers the knot pattern itself to the maker, inventing none.",
        "drafting": "Made to measure to chest girth, jacket length and sleeve length; the git is "
            "solved to the collar run and the closure is a maedeup knot-and-loop.",
    }
    return pattern


result = build()
