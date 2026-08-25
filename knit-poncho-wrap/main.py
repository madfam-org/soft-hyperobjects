"""
Knit poncho wrap — FC-300 rank #293. Fashion Cabinet Garment Cartridge.

The contemporary poncho wrap: a heavy knitted or fulled outer layer that is
neither the closed woven rectangle nor the open heritage ruana, but the third
thing the commons did not yet hold — a wrap with a REAL SHAPED NECKLINE, a
stand collar, and an ASYMMETRIC toggle closure that lets it be worn shut like a
coat or thrown open like a shawl.

What separates it from its two neighbours in the commons, in construction and
not in vocabulary:

  - `sarape-poncho` is ONE rectangle with a head slit. Nothing is shaped; you
    pull it over your head and it stays a tube.
  - `poncho-ruana` is split up the centre front and has a plain slot neck. It
    opens like a cape but the neck is a slit, not a neckline.
  - THIS one has a scooped neckline drafted from a measured neck girth, a stand
    collar solved to that neckline, and an off-centre toggle band. It is a
    garment you fasten, not a cloth you drape — which is why it is the one that
    needs hardware at all.

Three things solve, and each is protected by a floor:

  - THE NECKLINE: a real scoop, drafted per panel from the measured neck girth,
    with the front dropped below the back. Its measured length drives the
    collar, which is bisected to it rather than assumed.
  - THE SHOULDER SLOPE: the wrap is not a flat rectangle — each panel's outer
    edge falls away from the neck by `shoulder_slope`, which is what stops a
    heavy melton wrap from standing up in a hoop around the neck.
  - THE TOGGLE LADDER: the number of toggles is DERIVED from the closure run
    divided by the toggle pitch. A derived count is exactly the kind of value
    that goes to zero or negative at parameter extremes, so it is clamped, and
    the toggle band's own length is clamped with it.

Hardware: the toggles bridge to the Yantra4D `toggle` solid. `barrel_len` and
`cord_dia` drive the printed toggle, its marked seat on the band and the cord
loop opposite, so a bigger toggle cannot end up with a loop it will not pass.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
# front|back|collar|toggle_band|set

span_width = float(PARAM(lambda: span_width, 620.0))       # neck centre → outer edge
wrap_length = float(PARAM(lambda: wrap_length, 780.0))     # neck → front hem
back_drop = float(PARAM(lambda: back_drop, 120.0))         # extra length on the back
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
front_neck_drop = float(PARAM(lambda: front_neck_drop, 95.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 70.0))  # outer edge fall
collar_height = float(PARAM(lambda: collar_height, 85.0))
closure_run = float(PARAM(lambda: closure_run, 320.0))     # toggled length below the neck
toggle_pitch = float(PARAM(lambda: toggle_pitch, 110.0))   # spacing between toggles
barrel_len = float(PARAM(lambda: barrel_len, 46.0))        # toggle barrel length
cord_dia = float(PARAM(lambda: cord_dia, 6.0))             # toggle cord diameter
band_width = float(PARAM(lambda: band_width, 70.0))        # toggle band width
seam_allowance = float(PARAM(lambda: seam_allowance, 14.0))

# ── Clamps (match the manifest slider bounds exactly) ────────────────────────
span_width = max(420.0, min(span_width, 850.0))
wrap_length = max(500.0, min(wrap_length, 1150.0))
back_drop = max(0.0, min(back_drop, 300.0))
neck_girth = max(300.0, min(neck_girth, 520.0))
front_neck_drop = max(30.0, min(front_neck_drop, 200.0))
shoulder_slope = max(0.0, min(shoulder_slope, 180.0))
collar_height = max(0.0, min(collar_height, 160.0))
closure_run = max(80.0, min(closure_run, 600.0))
toggle_pitch = max(60.0, min(toggle_pitch, 260.0))
barrel_len = max(25.0, min(barrel_len, 70.0))
cord_dia = max(3.0, min(cord_dia, 9.0))
band_width = max(35.0, min(band_width, 130.0))
seam_allowance = max(10.0, min(seam_allowance, 25.0))

# ── The neckline: a real scoop, not a slit ───────────────────────────────────
# Half neck width at the shoulder line, from the measured girth with wearing
# ease for a heavy outer layer worn over other clothes.
NW = max(60.0, neck_girth / 5.0 + 22.0)
BACK_NECK_DROP = 26.0
NECK_Y = wrap_length                             # neck level = top of the front draft

# The outer edge falls away from the neck by `shoulder_slope`. That fall is what
# stops a stiff melton wrap standing in a hoop. The shoulder line's OUTER end
# must stay above the hem or the panel inverts, so the slope is capped against
# the available length before any point is built — a derived shoulder-end height
# that went negative would be CCW-normalized into a valid-LOOKING outline.
_slope_room = wrap_length - 120.0                # keep a real panel below the shoulder
SHOULDER_FALL = max(0.0, min(shoulder_slope, _slope_room))
SLOPE_CLAMPED = shoulder_slope > _slope_room

# The neck span the scoop is carved from. Derived (half span less half neck) and
# therefore floored: a very wide neck on a narrow wrap would leave nothing.
_neck_span_raw = span_width - NW
NECK_SPAN = max(80.0, _neck_span_raw)
SPAN_CLAMPED = _neck_span_raw < 80.0
PANEL_W = NW + NECK_SPAN                         # the panel's true half-span

BACK_LENGTH = wrap_length + back_drop

# ── The toggle ladder: a DERIVED count, therefore clamped ────────────────────
# The closure run cannot exceed the front's length below the neck, and the
# toggle count is that run over the pitch. Both are floored: a count of zero
# would emit a band with no toggles on it, and a negative run would put the
# marks above the neckline.
_run_room = max(60.0, wrap_length - front_neck_drop - 40.0)
CLOSURE_RUN = max(60.0, min(closure_run, _run_room))
RUN_CLAMPED = closure_run > _run_room
TOGGLE_COUNT = int(max(1.0, min(CLOSURE_RUN / toggle_pitch, 8.0)))
BAND_LENGTH = max(120.0, CLOSURE_RUN + 2.0 * seam_allowance)


def _neck_edge(name, drop, x_from, x_to, y_shoulder):
    """One panel's neckline scoop: a real curve from the centre down and out to
    the shoulder point. `drop` is how far below the shoulder line the centre of
    the scoop sits — the front is dropped, the back barely."""
    a = fc.P(x_from, y_shoulder - drop)
    b = fc.P(x_to, y_shoulder)
    return fc.Edge(name, [fc.Bezier(a, fc.P(x_from + (x_to - x_from) * 0.55,
                                            y_shoulder - drop),
                                    fc.P(x_to, y_shoulder - drop * 0.35), b)])


def build_front():
    """Front panel (cut 2, mirrored) — the wrap opens at centre front.

    Centre-front edge up to the neck scoop, scoop out to the shoulder point, the
    sloped shoulder line out to the outer edge, the outer edge down, and the hem
    back to centre. The toggle marks live on the centre-front edge.
    """
    h = wrap_length
    sh_y = h                                    # shoulder line at the top
    out_y = sh_y - SHOULDER_FALL                # the outer edge is lower
    neck_top = sh_y - front_neck_drop
    internals = [
        fc.Internal("CF line", [fc.P(0.0, 0.0), fc.P(0.0, neck_top)],
                    kind="marking"),
    ]
    # Toggle seats: the DERIVED ladder, marked down the centre-front edge.
    for i in range(TOGGLE_COUNT):
        y = neck_top - (i + 0.5) * (CLOSURE_RUN / TOGGLE_COUNT)
        internals.append(fc.Internal(f"toggle-seat-{i + 1}",
                                     [fc.P(0.0, y - barrel_len / 2.0),
                                      fc.P(0.0, y + barrel_len / 2.0)],
                                     kind="drill"))
        internals.append(fc.Internal(f"cord-loop-{i + 1}",
                                     [fc.P(0.0, y),
                                      fc.P(barrel_len * 1.3, y)],
                                     kind="marking"))
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_top))]),
            _neck_edge("neck", front_neck_drop, 0.0, NW, sh_y),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, sh_y), fc.P(PANEL_W, out_y))]),
            fc.Edge("outer", [fc.Line(fc.P(PANEL_W, out_y), fc.P(PANEL_W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(PANEL_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"center_front": 0.0, "hem": seam_allowance * 2.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder match"),
                 fc.Notch("neck", 1.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(PANEL_W * 0.5, h * 0.12),
                               fc.P(PANEL_W * 0.5, h * 0.72)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel",
    )


def build_back():
    """Back panel (cut 1 on the centre-back fold), drafted longer by `back_drop`.

    Same shoulder slope as the front so the two shoulder seams are identical
    lines and balance by construction, and a shallow back neck scoop.
    """
    h = BACK_LENGTH
    sh_y = h
    out_y = sh_y - SHOULDER_FALL
    neck_top = sh_y - BACK_NECK_DROP
    return fc.Piece(
        "back",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, neck_top))]),
            _neck_edge("neck", BACK_NECK_DROP, 0.0, NW, sh_y),
            fc.Edge("shoulder", [fc.Line(fc.P(NW, sh_y), fc.P(PANEL_W, out_y))]),
            fc.Edge("outer", [fc.Line(fc.P(PANEL_W, out_y), fc.P(PANEL_W, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(PANEL_W, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"center_back": 0.0, "hem": seam_allowance * 2.0},
        notches=[fc.Notch("shoulder", 0.5, "shoulder match"),
                 fc.Notch("neck", 1.0, "shoulder point")],
        grainline=fc.Grainline(fc.P(PANEL_W * 0.5, h * 0.12),
                               fc.P(PANEL_W * 0.5, h * 0.72)),
        internals=[fc.Internal("back drop line",
                               [fc.P(0.0, back_drop), fc.P(PANEL_W, back_drop)],
                               kind="marking")] if back_drop > 0.0 else None,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back",
                       mirror=True),
        label="Back panel (on fold)",
    )


def _collar_neck(flat, rise):
    """The collar's neck edge as a function of its flat length — the function the
    bisection solves against the measured neckline."""
    return fc.Edge("neck", [fc.curve_through(fc.P(0.0, 0.0), fc.P(flat, rise),
                                             bulge=0.06, side=-1.0)])


def build_collar(neck_target):
    """Stand collar, half on the centre-back fold.

    Its neck edge is SOLVED by bisection to the measured neckline per half
    (front scoop + back scoop), so the collar cannot be a guess that happens to
    fit. A collar shorter than its neckline puckers; one longer flutes.
    """
    rise = max(4.0, collar_height * 0.18)
    lo, hi = neck_target * 0.55, neck_target * 1.15
    for _ in range(52):
        mid = (lo + hi) / 2.0
        if _collar_neck(mid, rise).length(0.05) < neck_target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(_collar_neck(flat, rise).length(0.05) - neck_target) > 1.0:
        raise ValueError("collar neck solver did not converge")
    d = max(25.0, collar_height)                 # floored: a 0-height stand is not a piece
    return fc.Piece(
        "collar",
        [
            _collar_neck(flat, rise),
            fc.Edge("front_edge", [fc.Line(fc.P(flat, rise), fc.P(flat, rise + d))]),
            fc.Edge("top", [fc.curve_through(fc.P(flat, rise + d), fc.P(0.0, d),
                                             bulge=0.03, side=1.0)]),
            fc.Edge("cb", [fc.Line(fc.P(0.0, d), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 0.5, "shoulder seam match")],
        grainline=fc.Grainline(fc.P(flat * 0.2, d / 2.0), fc.P(flat * 0.8, d / 2.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Stand collar (half, on fold)",
    )


def build_toggle_band():
    """The toggle band (cut 2, mirrored): the reinforced strip the toggles and
    their cord loops are set into.

    Its length is the CLAMPED closure run plus end allowances, and it carries
    the same derived toggle ladder as the front's centre edge, so band and panel
    cannot disagree about where the toggles go.
    """
    ln, w = BAND_LENGTH, band_width
    internals = [fc.Internal("fold line",
                             [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                             kind="marking")]
    for i in range(TOGGLE_COUNT):
        x = seam_allowance + (i + 0.5) * (CLOSURE_RUN / TOGGLE_COUNT)
        internals.append(fc.Internal(f"toggle-{i + 1}",
                                     [fc.P(x - barrel_len / 2.0, w / 2.0),
                                      fc.P(x + barrel_len / 2.0, w / 2.0)],
                                     kind="drill"))
        internals.append(fc.Internal(f"cord-channel-{i + 1}",
                                     [fc.P(x, w / 2.0 - cord_dia),
                                      fc.P(x, w / 2.0 + cord_dia)],
                                     kind="drill"))
    return fc.Piece(
        "toggle_band",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("free", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,                      # length already carries 2×sa
        notches=[fc.Notch("attach", seam_allowance / ln, "neck end")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Toggle band",
    )


def build():
    pattern = fc.PatternSet("knit-poncho-wrap")
    front = build_front()
    back = build_back()
    neck_target = (front.edge("neck").length(0.05)
                   + back.edge("neck").length(0.05))

    names = ("front", "back", "collar", "toggle_band")
    wanted = {n: target_piece in (n, "set") for n in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    if wanted["front"]:
        pattern.add(front)
    if wanted["back"]:
        pattern.add(back)
    if wanted["collar"]:
        pattern.add(build_collar(neck_target))
    if wanted["toggle_band"]:
        pattern.add(build_toggle_band())

    # ── Declared seams ───────────────────────────────────────────────────────
    # Front and back shoulders are the SAME sloped line (same NW, same PANEL_W,
    # same SHOULDER_FALL), so this balances to delta 0.0 by construction.
    if wanted["front"] and wanted["back"]:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # The outer edges are NOT sewn — the wrap is open at the sides. The
        # back's extra length is the deliberate `back_drop`, declared as ease so
        # the run proves the drop is exactly what was asked for.
        pattern.declare_seam(("back", "outer"), ("front", "outer"),
                             tol=1.0, ease=back_drop)
    # The collar's neck edge is bisected to the measured front + back scoops.
    if wanted["collar"] and wanted["front"] and wanted["back"]:
        pattern.declare_seam([("collar", "neck")],
                             [("front", "neck"), ("back", "neck")], tol=1.5)
    # The band's attach edge sews to the front's centre-front edge over the
    # closure run. The front's CF edge is longer than the run (it continues to
    # the hem below the last toggle), so that surplus is declared as honest ease
    # rather than hidden by a loosened tolerance.
    if wanted["toggle_band"] and wanted["front"]:
        cf_len = front.edge("center_front").length(0.05)
        band_len = pattern.piece("toggle_band").edge("attach").length(0.05)
        pattern.declare_seam(("front", "center_front"),
                             ("toggle_band", "attach"),
                             tol=1.0, ease=cf_len - band_len)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1500.0                        # lana-melton-abrigo card width
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "lana-melton-abrigo", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"fulled wool coating at {fabric_width:.0f} mm width, 74% "
                 "marker. The fulled face barely frays, so the outer and hem "
                 "edges can be left raw-cut and topstitched rather than turned"},
        {"item": "toggle", "qty": TOGGLE_COUNT, "unit": "count",
         "note": f"Yantra4D toggle, {barrel_len:.0f} mm barrel for "
                 f"{cord_dia:.0f} mm cord (see notion.hardware_ref); the count "
                 "is derived from the closure run over the toggle pitch"},
        {"item": "cord", "qty": round(barrel_len * 5.0 * TOGGLE_COUNT),
         "unit": "mm_length",
         "note": f"{cord_dia:.0f} mm cord for the toggle loops and channels"},
        {"item": "interfacing (toggle band)", "qty": round(BAND_LENGTH * 2.0),
         "unit": "mm_length",
         "note": "the band takes the whole closing load in a heavy wrap; a "
                 "fusible or a strip of firm cotton keeps the toggles from "
                 "dragging the melton out of shape"},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "heavy poly or wool topstitch thread; the shoulder seam and "
                 "the band carry the weight of the whole garment"},
    ]
    pattern.metadata = {
        "fc300_rank": 293,
        "family": "knitwear",
        "fabric_hint": "lana-melton-abrigo",
        "distinction": "NOT the closed rectangle (`sarape-poncho`) and NOT the "
                       "slit-neck open heritage wrap (`poncho-ruana`): this one "
                       "has a drafted neckline, a solved stand collar and a "
                       "toggle closure — a garment you fasten, not a cloth you "
                       "drape",
        "finished_mm": {"front_length": round(wrap_length, 1),
                        "back_length": round(BACK_LENGTH, 1),
                        "span": round(PANEL_W * 2.0, 1),
                        "neck_run": round(neck_target, 1)},
        "solved": {
            "panel_half_span_mm": round(PANEL_W, 2),
            "half_neck_width_mm": round(NW, 2),
            "neck_span_mm": round(NECK_SPAN, 2),
            "shoulder_fall_mm": round(SHOULDER_FALL, 2),
            "collar_neck_target_mm": round(neck_target, 2),
            "closure_run_mm": round(CLOSURE_RUN, 2),
            "toggle_count": TOGGLE_COUNT,
            "band_length_mm": round(BAND_LENGTH, 2),
            "slope_clamped": SLOPE_CLAMPED,
            "neck_span_clamped": SPAN_CLAMPED,
            "closure_run_clamped": RUN_CLAMPED,
            "note": "the shoulder fall, the neck span, the closure run and the "
                    "toggle count are all DERIVED; each is floored before any "
                    "point is built, because a derived dimension that goes "
                    "negative inverts the piece and CCW normalization then "
                    "launders it into a valid-LOOKING outline",
        },
        "hardware": "toggles via Yantra4D (notion.hardware_ref -> toggle); "
                    "barrel_len and cord_dia drive the printed toggle, its seat "
                    "on the band and the cord loop opposite, together",
    }
    return pattern


result = build()
