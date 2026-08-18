"""
Hi-Vis Safety Vest — FC-100 rank #89. Fashion Cabinet Garment Cartridge.

The classic economy high-visibility safety vest ("chaleco de alta visibilidad"),
honestly simplified — the EASIEST workwear garment in the commons. A very simple,
boxy, SLEEVELESS over-vest worn over street clothes: a straight FRONT cut as two
mirrored halves that close at the center front with HOOK-AND-LOOP (Velcro), and a
BACK cut on fold. It is loose (positive ease over layers), squared off, and every
canonical edge — neck, armholes, hem, front — is a BOUND finished edge (bias
binding), not a hem or a sleeve. Real hi-vis is a fluorescent polyester knit/mesh
per EN ISO 20471; the ripstop-shell card is the closest technical base here and
its breathability note is carried in the BOM (mesh is a fabric swap).

The SIGNATURE is the RETROREFLECTIVE TAPE in the EN ISO 20471 configuration:
horizontal band(s) that encircle the torso plus vertical "braces" over the
shoulders. Tape is modelled as `fc.Internal(kind="trace")` placement lines on the
FRONT and BACK, laid so the horizontal bands meet at the side seams (same band
heights front and back) and the vertical braces run shoulder-to-hem in line
front and back. The tape run (exact mm) is summed off the trace geometry into the
BOM — this is the defining feature, so the layout is derived, not guessed.

The front closes with hook-and-loop: a HOOK strip on one CF edge, a LOOP strip on
the other (marked as traces on the CF; the pair is cut 2 mirror so one carries
each). It is a deliberate breakaway / tear-away safety closure — it must release
under load rather than trap the wearer. Optional ID/badge pocket + phone pocket
are markings. Hook-and-loop tape is a purchased notion (Yantra4D hook-notion ref
in the BOM), never re-implemented here.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters (millimetres; girths are full-body) ───────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))
# front|back|bindings|set

chest_girth    = float(PARAM(lambda: chest_girth, 1060.0))   # over street clothes
body_length    = float(PARAM(lambda: body_length, 620.0))    # nape line to hem
neck_girth     = float(PARAM(lambda: neck_girth, 420.0))
vest_ease      = float(PARAM(lambda: vest_ease, 220.0))       # roomy over layers
overlap        = float(PARAM(lambda: overlap, 60.0))          # CF hook-loop overlap
tape_width     = float(PARAM(lambda: tape_width, 50.0))       # reflective tape band
band_count     = float(PARAM(lambda: band_count, 2.0))        # horizontal tape bands
binding_ratio  = float(PARAM(lambda: binding_ratio, 0.97))    # bind/opening ratio
binding_width  = float(PARAM(lambda: binding_width, 14.0))    # finished binding height
pockets        = bool(PARAM(lambda: pockets, True))           # ID + phone pocket marks
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 0.0))     # hem is bound, not folded

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 820.0))
neck_girth = max(300.0, min(neck_girth, 560.0))
vest_ease = max(100.0, min(vest_ease, 460.0))
overlap = max(30.0, min(overlap, 110.0))
tape_width = max(25.0, min(tape_width, 70.0))
band_count = float(int(max(1.0, min(band_count, 3.0))))
binding_ratio = max(0.85, min(binding_ratio, 1.0))
binding_width = max(8.0, min(binding_width, 25.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

# ── Vest block (roomy boxy body, no sleeve; all canonical edges bound) ────────
W = (chest_girth + vest_ease) / 4.0              # quarter body width (with layer ease)
L = body_length                                  # datum y=0 is the hem
AH = (chest_girth + vest_ease) / 8.0 + 80.0      # armhole depth (auto)
AH = max(200.0, min(AH, L - 90.0))
NW = max(66.0, neck_girth / 5.0 + 8.0)           # half neck width at HPS (roomy neck)
HPS_Y = L + 20.0                                 # high-point-of-shoulder line
SH_END = fc.P(W - 10.0, HPS_Y - 26.0)            # squared, slightly dropped shoulder
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 92.0                           # scoop for an over-vest neck
BACK_NECK_DROP = 24.0
ARM_SCOOP = 24.0                                 # sleeveless armscye scoop
HL = overlap                                     # hook-loop overlap extension past CF
# Reflective-tape band placement: bands centred on evenly spaced levels between a
# lower margin (above the hem) and an upper margin (below the underarm). The SAME
# band-centre y-values are used on the front and the back, so at every side seam a
# front band meets its back band exactly (the encircling EN ISO 20471 band).
BAND_LO = tape_width * 0.5 + 45.0                # lowest band centre, clear of hem
BAND_HI = UNDERARM.y - tape_width * 0.5 - 25.0   # highest band centre, below chest


def _band_levels():
    """Centre y of each horizontal reflective band (shared front↔back)."""
    n = int(band_count)
    if BAND_HI <= BAND_LO or n <= 1:
        return [min(BAND_LO, max(BAND_HI, (BAND_LO + BAND_HI) / 2.0))] if n >= 1 else []
    step = (BAND_HI - BAND_LO) / (n - 1)
    return [BAND_LO + i * step for i in range(n)]


def _armhole_edge():
    """Sleeveless bound armscye: shoulder end down to the underarm (no sleeve).

    A slightly scooped clean armhole curve; it is BOUND (bias strip), not sewn to
    a sleeve — so it is a finished edge, never a declared seam (the waistcoat /
    puffer-vest bound-armscye method)."""
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - ARM_SCOOP, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
    )


def _neck_edge(neck_drop, cf_x):
    """Scooped neckline from the center-front/back edge (x = cf_x) out to the neck
    point, which is a fixed BODY landmark at true x = NW regardless of any CF
    overlap — so the shoulder line beyond it is identical front to back."""
    neck_top_y = HPS_Y - neck_drop
    span = NW - cf_x
    return fc.Edge(
        "neck",
        [fc.Bezier(fc.P(cf_x, neck_top_y), fc.P(cf_x + span * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45),
                   fc.P(NW, HPS_Y))],
    )


def _horizontal_bands(x_lo, x_hi, label):
    """Horizontal reflective-tape placement traces across a panel.

    Each band is drawn as its CENTRE line (a trace) spanning x_lo→x_hi at the
    shared band levels; the physical tape is `tape_width` wide, centred on it.
    Traces, not seams — the tape is topstitched on. Because front and back share
    `_band_levels()`, the bands meet at the side seam to encircle the torso."""
    marks = []
    for i, y in enumerate(_band_levels(), start=1):
        marks.append(
            fc.Internal(f"{label} reflective band {i}",
                        [fc.P(x_lo, y), fc.P(x_hi, y)], kind="trace")
        )
    return marks


def _vertical_brace(x, y_top, label):
    """A vertical 'brace' reflective trace from the shoulder line down to the hem
    at column x. Front braces and back braces sit at the same x so they read as
    one continuous shoulder-to-hem stripe over the shoulder seam."""
    return fc.Internal(label, [fc.P(x, 0.0), fc.P(x, y_top)], kind="trace")


def _tape_run_front(x_lo, x_hi, brace_x, brace_top):
    """Total reflective-tape run on ONE front half (sum of trace lengths)."""
    run = len(_band_levels()) * abs(x_hi - x_lo)
    run += abs(brace_top)  # one vertical brace, hem (y=0) up to brace_top
    return run


def _tape_run_back(x_lo, x_hi, brace_x, brace_top):
    """Total reflective-tape run on the back (cut on fold → doubles).

    Two horizontal band halves (one on the folded half → ×2) plus one brace on
    the half (→ ×2 mirrored)."""
    per_half = len(_band_levels()) * abs(x_hi - x_lo) + abs(brace_top)
    return 2.0 * per_half


def _pocket_marks():
    """ID/badge pocket (upper chest) + phone pocket (lower), as marking boxes.
    Markings only; bag pieces are future work — noted in the BOM."""
    marks = []
    # ID / badge pocket high on the chest, toward the armhole side.
    idw, idh = 95.0, 120.0
    icx = min(W * 0.60, W - idw / 2.0 - 20.0)
    icy = min(UNDERARM.y - 40.0, L * 0.62)
    id_box = [fc.P(icx - idw / 2.0, icy + idh / 2.0), fc.P(icx + idw / 2.0, icy + idh / 2.0),
              fc.P(icx + idw / 2.0, icy - idh / 2.0), fc.P(icx - idw / 2.0, icy - idh / 2.0),
              fc.P(icx - idw / 2.0, icy + idh / 2.0)]
    marks.append(fc.Internal("id badge pocket", id_box, kind="marking"))
    # Phone pocket lower, nearer center front.
    pw, ph = 90.0, 150.0
    pcx = min(W * 0.42, W - pw / 2.0 - 15.0)
    pcy = max(ph / 2.0 + 30.0, L * 0.30)
    ph_box = [fc.P(pcx - pw / 2.0, pcy + ph / 2.0), fc.P(pcx + pw / 2.0, pcy + ph / 2.0),
              fc.P(pcx + pw / 2.0, pcy - ph / 2.0), fc.P(pcx - pw / 2.0, pcy - ph / 2.0),
              fc.P(pcx - pw / 2.0, pcy + ph / 2.0)]
    marks.append(fc.Internal("phone pocket", ph_box, kind="marking"))
    return marks


def build_front():
    """Half front, cut 2 mirror (never on fold): the center edge is the closing
    edge, extended by the hook-loop overlap. Bound neck / armhole / hem / front.
    Reflective bands (front halves) + one vertical brace + hook and loop strips."""
    # CCW chain, center-front edge at x = -HL (the overlap extension past CF x=0).
    cf_x = -HL
    origin = fc.P(cf_x, 0.0)                          # hem end at CF (with overlap)
    neck_top_y = HPS_Y - FRONT_NECK_DROP
    # The overlap extends only the CF closing edge and the hem; the neck point and
    # everything beyond it (shoulder, armhole, side) stay at true body landmarks,
    # so the front shoulder equals the back shoulder (seam delta ≈ 0).
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(cf_x, neck_top_y))]),  # CF (hook-loop)
        _neck_edge(FRONT_NECK_DROP, cf_x),
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    # Reflective tape: horizontal bands span from near the CF closing edge to the
    # side seam; one vertical brace over the shoulder line, in line with the back.
    brace_x = min(cf_x + NW + 30.0, W * 0.5)
    brace_top = SH_END.y - 12.0
    internals = _horizontal_bands(cf_x + 15.0, W - 8.0, "front")
    internals.append(_vertical_brace(brace_x, brace_top, "front reflective brace"))
    # Hook-and-loop strip runs the full CF closing edge (one of hook/loop per side;
    # cut 2 mirror carries both). A trace down x = cf_x + overlap/... kept on CF.
    internals.append(
        fc.Internal("hook/loop closure strip",
                    [fc.P(cf_x + HL * 0.5, 10.0), fc.P(cf_x + HL * 0.5, neck_top_y - 10.0)],
                    kind="trace")
    )
    if pockets:
        internals += _pocket_marks()
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        # neck / armhole / hem / front(center) are BOUND finished edges (allowance 0)
        allowances={"neck": 0.0, "armhole": 0.0, "hem": hem_allowance, "center": 0.0},
        notches=[
            fc.Notch("side", 0.5),
            fc.Notch("armhole", 0.5, "front armhole (bound)"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.55, 60.0), fc.P(W * 0.55, L - 90.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (hook-loop, taped)",
    )


def build_back():
    """Half back, cut 1 on fold at CB. Bound neck / armhole / hem. Reflective
    bands (full width across the fold) + one vertical brace on the half (mirrored
    to two braces), aligned to the front braces at the shoulder seam."""
    origin = fc.P(0.0, 0.0)
    neck_top_y = HPS_Y - BACK_NECK_DROP
    edges = [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),  # CB fold
        _neck_edge(BACK_NECK_DROP, 0.0),
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]
    brace_x = min(NW + 30.0, W * 0.5)                 # matches the front brace column
    brace_top = SH_END.y - 12.0
    internals = _horizontal_bands(8.0, W - 8.0, "back")
    internals.append(_vertical_brace(brace_x, brace_top, "back reflective brace"))
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"neck": 0.0, "armhole": 0.0, "hem": hem_allowance},
        notches=[
            fc.Notch("side", 0.5),
            fc.Notch("armhole", 0.5, "back armhole (bound)"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.55, 60.0), fc.P(W * 0.55, L - 90.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (taped)",
    )


def _binding(name, finished_len, label, qty=1):
    """A straight bias-binding strip, drafted cut-ready. Its long dimension is the
    measured opening × the binding ratio, plus 2× seam allowance for the ends;
    the strip is folded to `binding_width` finished, so its cut height is 4× that.
    Bindings finish the neck / armholes / hem / front — the tank-top binding
    method (finishing strips computed from measured curves, not guessed)."""
    length = finished_len + 2.0 * seam_allowance
    band_h = 4.0 * binding_width                       # double-fold binding cut height
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
        fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,                            # strip is drafted cut-ready
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("hi-vis-vest")
    front = build_front()
    back = build_back()

    want_body = target_piece in ("front", "back", "set")
    want_bind = target_piece in ("bindings", "set")
    if not (want_body or want_bind):
        want_body = want_bind = True
    if target_piece in ("front", "set"):
        pattern.add(front)
    if target_piece in ("back", "set"):
        pattern.add(back)

    # ── Bindings: lengths derived from the measured openings × the ratio. ──────
    # Neck: two front necks (cut 2) + the folded back's two neck halves.
    neck_opening = 2.0 * front.edge("neck").length(0.05) + 2.0 * back.edge("neck").length(0.05)
    # Armhole: front + back armhole = one side's pair; ×2 for both armscyes.
    armhole_pair = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    armhole_opening = 2.0 * armhole_pair
    # Hem: two front hems (cut 2) + the folded back's two hem halves.
    hem_opening = 2.0 * front.edge("hem").length(0.05) + 2.0 * back.edge("hem").length(0.05)
    # Front closing edges: two fronts' center edges (each bound down the CF).
    front_edge_opening = 2.0 * front.edge("center").length(0.05)
    if want_bind:
        pattern.add(_binding("neck_binding", neck_opening * binding_ratio,
                             "Neck Binding (bias)"))
        pattern.add(_binding("armhole_binding", armhole_opening * binding_ratio,
                             "Armhole Binding (bias)", qty=1))
        pattern.add(_binding("hem_binding", hem_opening * binding_ratio,
                             "Hem Binding (bias)"))
        pattern.add(_binding("front_binding", front_edge_opening * binding_ratio,
                             "Front Edge Binding (bias)"))

    # ── Seams (all delta ≈ 0). Neck / armhole / hem / front are BOUND finished
    #    edges, not seams; the CF hook-loop is a notion, not a fabric seam. ─────
    if target_piece == "set":
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)

    # ── Reflective-tape run: summed off the trace geometry (the signature). ────
    cf_x = -HL
    f_brace_x = min(cf_x + NW + 30.0, W * 0.5)
    b_brace_x = min(NW + 30.0, W * 0.5)
    brace_top = SH_END.y - 12.0
    tape_front = 2.0 * _tape_run_front(cf_x + 15.0, W - 8.0, f_brace_x, brace_top)  # cut 2
    tape_back = _tape_run_back(8.0, W - 8.0, b_brace_x, brace_top)                  # cut on fold
    tape_total = int(round((tape_front + tape_back) / 10.0) * 10)
    band_levels = _band_levels()

    # ── Binding total run (all bound edges, cut-ready lengths). ───────────────
    binding_total = int(round(
        (neck_opening + armhole_opening + hem_opening + front_edge_opening) * binding_ratio
        / 10.0) * 10)

    # ── BOM: hi-vis fabric + reflective tape + hook-and-loop + binding + thread.
    fabric_width = 1450.0                              # nylon-ripstop-shell card width
    body_area = front.area() * 2.0 + back.area() * 2.0  # 2 fronts + folded back
    marker_len = body_area / (fabric_width * 0.62)     # 62% marker efficiency
    pattern.bom = [
        {"item": "hi-vis fabric (fluorescent, nylon-ripstop-shell base)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"fluorescent-yellow/orange background material at {fabric_width:.0f} mm "
                 f"width, 62% marker efficiency; EN ISO 20471 requires a certified "
                 f"fluorescent background — swap the ripstop base for a fluorescent "
                 f"polyester KNIT/MESH for breathability on a worn vest"},
        {"item": "retroreflective tape (50 mm class 2)", "qty": tape_total,
         "unit": "mm_length",
         "note": f"total tape run across front (×2) + back: {int(band_count)} horizontal "
                 f"band(s) encircling the torso + vertical shoulder braces, "
                 f"{tape_width:.0f} mm wide; bands meet at the side seams. EN ISO 20471 "
                 f"minimum band width is 50 mm — keep tape_width >= 50 for compliance"},
        {"item": "hook-and-loop tape (sew-on, hook + loop pair)", "qty": 2,
         "unit": "set",
         "note": f"center-front closure: a hook strip on one front, a loop strip on the "
                 f"other, ~{overlap:.0f} mm overlap; a BREAKAWAY / tear-away safety "
                 f"closure that releases under load. The tape is a purchased notion — "
                 f"hardware/geometry is a Yantra4D cartridge (hook-notion), not "
                 f"re-implemented here"},
        {"item": "bias binding tape", "qty": binding_total, "unit": "mm_length",
         "note": "binds the neck, both armscyes, the hem and the two front closing "
                 "edges (no sleeve, no folded hem); lengths = measured openings × "
                 f"{binding_ratio:.2f} ratio"},
        {"item": "polyester thread + microtex needle 70/10", "qty": 1, "unit": "set",
         "note": "fine needle keeps holes small in the slippery ripstop base; pin "
                 "inside the allowance and topstitch the reflective tape down"},
    ]
    pattern.metadata = {
        "fc100_rank": 89,
        "fabric_hint": "nylon-ripstop-shell",
        "silhouette": "very simple boxy sleeveless open-front over-vest worn over "
                      "clothes; roomy positive ease over layers",
        "sleeveless": "armhole is a finished/BOUND edge — no sleeve piece "
                      "(waistcoat / puffer-vest bound-armscye method)",
        "bound_edges": "neck, both armscyes, hem and the two front closing edges "
                       "are bias-bound finished edges (tank-top binding method); "
                       "no folded hem",
        "reflective_tape_layout": {
            "standard": "EN ISO 20471",
            "config": "horizontal encircling band(s) + vertical shoulder braces",
            "horizontal_bands": int(band_count),
            "band_centre_levels_mm": [round(y, 1) for y in band_levels],
            "band_width_mm": round(tape_width, 1),
            "vertical_braces": "one brace per front half (×2) + one per back half "
                               "(×2 mirrored) = 4 shoulder-to-hem braces",
            "meet_at_side_seam": "front and back share the band-centre levels, so "
                                 "each horizontal band is continuous around the torso",
            "total_tape_run_mm": tape_total,
            "note": "tape is fc.Internal(kind='trace') placement lines (band centres "
                    "+ brace columns) topstitched on; the run is summed off the trace "
                    "geometry, not guessed. EN ISO 20471 min band width is 50 mm",
        },
        "hook_loop_closure": {
            "type": "hook-and-loop (Velcro), breakaway / tear-away safety closure",
            "overlap_mm": round(overlap, 1),
            "strips": "hook on one front, loop on the other (cut 2 mirror carries "
                      "both); marked as CF traces",
            "hardware": "purchased notion; Yantra4D hook-notion reference (BOM), "
                        "never re-implemented here",
            "safety_note": "must release under load rather than trap the wearer near "
                            "machinery or traffic",
        },
        "en_iso_20471": "high-visibility class depends on certified fluorescent "
                        "background area + retroreflective band area + band placement; "
                        "this cartridge draws the placement and computes the tape run, "
                        "but certification/area minimums are a compliance step, not "
                        "geometry — keep tape_width >= 50 mm and use a certified "
                        "fluorescent background",
        "pockets": "ID/badge pocket + phone pocket are markings; bag pieces are "
                   "future work" if pockets else "omitted",
        "quarter_width_mm": round(W, 1),
        "armhole_depth_mm": round(AH, 1),
        "neck_opening_mm": round(neck_opening, 1),
        "armhole_front_mm": round(front.edge("armhole").length(), 1),
        "armhole_back_mm": round(back.edge("armhole").length(), 1),
        "hem_circumference_mm": round(hem_opening, 1),
        "front_edge_run_mm": round(front.edge("center").length(), 1),
        "binding_total_run_mm": binding_total,
        "drafting": "teaching-grade economy hi-vis safety vest: a boxy sleeveless "
                    "over-vest (quarter-width block, roomy layer ease), front cut 2 "
                    "mirror closing at CF with hook-and-loop, back cut 1 on fold, "
                    "bound armscyes (no sleeve) and bound neck/hem/front edges, with "
                    "EN ISO 20471 retroreflective tape drawn as placement traces "
                    "(horizontal encircling bands + vertical shoulder braces) whose "
                    "total run is summed off the geometry; the fluorescent background, "
                    "reflective tape and hook-and-loop are BOM/notions",
    }
    return pattern


result = build()
