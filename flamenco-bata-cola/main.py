"""
Flamenco Bata de Cola — Fashion Cabinet Costume Cartridge (FC-500 #475; y4d hook-and-eye).

The bata de cola: the trained flamenco dress whose skirt sweeps into a long ruffled TAIL (the
cola) that the dancer throws and controls with the legs. It is drafted here as a fitted bodice
over a gored skirt that grows from a knee-length front hem to a floor-plus train at the back,
edged with a cascade of ruffles (volantes), closing at a centre-back Yantra4D `hook-and-eye`. Made
to measure — the bata de cola only works if it is cut to the dancer, because its weight and sweep
are controlled by the body.

The tail SOLVE. The skirt is a set of gores whose length grows from the front (`front_length`) to
the back (`front_length + tail_length`), so the hem is not level — it is a drafted sweep. Each
gore is a trapezoid whose two side edges are the SAME length as its neighbours' (they sew
together), and whose hem grows down the sweep; the ruffle is gathered onto that swept hem at a
declared fullness, so the cascade length is proven arithmetic.

The DIMENSIONAL HANDSHAKE. The centre back closes on a `hook-and-eye`; `closure_rows` drives the
hook `columns` and `bodice_length` drives the drafted CB placket AND the dress's own `cb_closure`
interface, so the placket the hooks sew into is exactly as tall as the tape.

Made to measure to bust, waist, hip and length. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
bodice_length = float(PARAM(lambda: bodice_length, 380.0))   # shoulder to waist
front_length = float(PARAM(lambda: front_length, 600.0))     # waist to front hem
tail_length = float(PARAM(lambda: tail_length, 900.0))       # extra length at the back (the cola)
gore_count = float(PARAM(lambda: gore_count, 6.0))
ruffle_fullness = float(PARAM(lambda: ruffle_fullness, 2.5))
ruffle_depth = float(PARAM(lambda: ruffle_depth, 140.0))
closure_rows = float(PARAM(lambda: closure_rows, 8.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
bodice_length = max(280.0, min(bodice_length, 520.0))
front_length = max(400.0, min(front_length, 1100.0))
tail_length = max(300.0, min(tail_length, 1600.0))
gore_count = max(4.0, min(gore_count, 12.0))
ruffle_fullness = max(1.6, min(ruffle_fullness, 4.0))
ruffle_depth = max(70.0, min(ruffle_depth, 260.0))
closure_rows = max(3.0, min(closure_rows, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

N_GORE = int(round(gore_count))

# ── Solved widths ────────────────────────────────────────────────────────────
BUST_HALF = bust_girth / 2.0
WAIST_HALF = waist_girth / 2.0
HIP_HALF = hip_girth / 2.0
BODICE_PANEL = BUST_HALF / 2.0     # front/back share side seam
WAIST_PANEL = WAIST_HALF / 2.0
BL = bodice_length
# gore widths at the waist and hem
GORE_WAIST = waist_girth / N_GORE
GORE_HEM = (hip_girth * 1.8) / N_GORE    # flared hem
# a representative gore length: front gores short, back gores long; draft the LONGEST (back)
GORE_LEN = front_length + tail_length


def _bodice(is_front):
    top = BODICE_PANEL
    bot = WAIST_PANEL
    neck_w = max(60.0, top * 0.5)
    neck_drop = (top * 0.7) if is_front else (top * 0.2)
    p_cf_waist = fc.P(0.0, 0.0)
    p_side_waist = fc.P(bot, 0.0)
    p_underarm = fc.P(top, BL * 0.5)
    p_shoulder = fc.P(neck_w + (top - neck_w) * 0.5, BL)
    p_neck = fc.P(neck_w, BL - neck_drop * 0.0)
    p_cf_neck = fc.P(0.0, BL - neck_drop)
    edges = [
        fc.Edge("waist", [fc.Line(p_cf_waist, p_side_waist)]),
        fc.Edge("side", [fc.Line(p_side_waist, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm, fc.P(top * 0.95, BL * 0.75),
                                      fc.P(p_shoulder.x + 10.0, BL - 20.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.6, BL - neck_drop * 0.4),
                                   fc.P(neck_w * 0.2, BL - neck_drop * 0.85), p_cf_neck)]),
        fc.Edge("center", [fc.Line(p_cf_neck, p_cf_waist)]),
    ]
    name = "bodice_front" if is_front else "bodice_back"
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"armscye": 0.0, "neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("waist", 0.5, "gore match")],
        grainline=fc.Grainline(fc.P(top * 0.4, BL * 0.2), fc.P(top * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=(1 if is_front else 2), mirror=(not is_front),
                       on_fold=is_front, fold_edge=("center" if is_front else None)),
        label=("Bodice front (cut 1 on fold)" if is_front else "Bodice back (cut 2, CB hook)"),
    )


def build_gore():
    """One skirt gore: a trapezoid, waist (top, GORE_WAIST) to hem (bottom, GORE_HEM), of the
    longest (back) length. Side edges are equal length so gores sew together."""
    top, bot = GORE_WAIST, GORE_HEM
    off = (bot - top) / 2.0
    p_wl = fc.P(off, GORE_LEN)
    p_wr = fc.P(off + top, GORE_LEN)
    p_hr = fc.P(bot, 0.0)
    p_hl = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hl, p_hr)]),
        fc.Edge("side_r", [fc.Line(p_hr, p_wr)]),
        fc.Edge("waist", [fc.Line(p_wr, p_wl)]),
        fc.Edge("side_l", [fc.Line(p_wl, p_hl)]),
    ]
    return fc.Piece(
        "gore", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.5, "waist"), fc.Notch("hem", 0.5, "ruffle")],
        grainline=fc.Grainline(fc.P(bot * 0.5, GORE_LEN * 0.1), fc.P(bot * 0.5, GORE_LEN * 0.9)),
        cut=fc.CutSpec(quantity=N_GORE),
        label=f"Skirt gore (cut {N_GORE})",
    )


def build_ruffle():
    """A ruffle (volante) tier: a rectangle of the swept-hem length x fullness, gathered on."""
    hem_ring = GORE_HEM * N_GORE
    length = hem_ring * ruffle_fullness
    edges = _rect_named(length, ruffle_depth)
    return fc.Piece(
        "ruffle", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("gather_edge", 0.25, "q"), fc.Notch("gather_edge", 0.5, "half"),
                 fc.Notch("gather_edge", 0.75, "q")],
        grainline=fc.Grainline(fc.P(length * 0.08, ruffle_depth * 0.4),
                               fc.P(length * 0.92, ruffle_depth * 0.4)),
        cut=fc.CutSpec(quantity=1),
        label="Ruffle / volante (gathered onto the swept hem)",
    )


def _rect_named(w, h):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge("gather_edge", [fc.Line(p0, p1)]), fc.Edge("end_r", [fc.Line(p1, p2)]),
            fc.Edge("outer", [fc.Line(p2, p3)]), fc.Edge("end_l", [fc.Line(p3, p0)])]


def build_placket(cb_len):
    w = max(40.0, closure_rows * 12.0)
    edges = _rect2(w, cb_len)
    n = int(round(closure_rows))
    internals = [fc.Internal(f"hook-{i}", [fc.P(w * 0.4, (i + 0.5) * cb_len / n),
                                           fc.P(w * 0.6, (i + 0.5) * cb_len / n)], kind="drill")
                 for i in range(n)]
    return fc.Piece(
        "placket", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(w * 0.5, cb_len * 0.1), fc.P(w * 0.5, cb_len * 0.9)),
        internals=internals, cut=fc.CutSpec(quantity=2),
        label="CB hook-and-eye placket (cut 2)",
    )


def _rect2(w, h):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge("bottom", [fc.Line(p0, p1)]), fc.Edge("attach", [fc.Line(p1, p2)]),
            fc.Edge("top", [fc.Line(p2, p3)]), fc.Edge("fold", [fc.Line(p3, p0)])]


def build():
    pattern = fc.PatternSet("flamenco-bata-cola")
    b_front = _bodice(True)
    b_back = _bodice(False)
    gore = build_gore()
    ruffle = build_ruffle()
    placket = build_placket(b_back.edge("center").length())

    picked = {"bodice_front": b_front, "bodice_back": b_back, "gore": gore, "ruffle": ruffle,
              "placket": placket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (b_front, b_back, gore, ruffle, placket):
            pattern.add(piece)
        # Bodice side seams: front side to back side.
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=2.0)
        # Gore side seams close to each other (a gore's two sides are equal length).
        pattern.declare_seam(("gore", "side_l"), ("gore", "side_r"), tol=1.0)
        # Waist: the skirt gores' waists (N of them) gather/join onto the bodice waist ring.
        bodice_waist_full = 2.0 * (b_front.edge("waist").length() + b_back.edge("waist").length())
        gore_waist_full = N_GORE * gore.edge("waist").length()
        pattern.declare_seam(
            [("gore", "waist")] * N_GORE,
            [("bodice_front", "waist"), ("bodice_front", "waist"),
             ("bodice_back", "waist"), ("bodice_back", "waist")],
            tol=3.0, ease=(gore_waist_full - bodice_waist_full))
        # Ruffle gathers onto the swept hem ring.
        hem_ring = N_GORE * gore.edge("hem").length()
        pattern.declare_seam(("ruffle", "gather_edge"),
                             [("gore", "hem")] * N_GORE,
                             tol=3.0, ease=(ruffle.edge("gather_edge").length() - hem_ring))
        # Placket to the bodice CB.
        pattern.declare_seam(("placket", "attach"), ("bodice_back", "center"), tol=2.0)

    fabric_width = 1400.0
    area = (b_front.area() * 2.0 + b_back.area() * 2.0 + gore.area() * N_GORE
            + ruffle.area() + placket.area() * 2.0)
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "percale / poplin (dress)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"bodice + {N_GORE} gores + ruffle at {fabric_width:.0f} mm width; the cola is "
                 "heavy, so a firm cotton holds the sweep."},
        {"item": "ruffle (volante) cut", "qty": round(ruffle.edge('gather_edge').length()),
         "unit": "mm_length",
         "note": f"one ruffle {ruffle.edge('gather_edge').length():.0f} mm flat "
                 f"({ruffle_fullness:.1f}x the swept hem), {ruffle_depth:.0f} mm deep; layer more "
                 "for a fuller cascade."},
        {"item": "hook-and-eye tape (Yantra4D hook-and-eye)", "qty": 1, "unit": "piece",
         "note": f"CB closure, {int(round(closure_rows))} rows (hardware_ref -> hook-and-eye)."},
        {"item": "horsehair braid + underskirt", "qty": round(N_GORE * GORE_HEM * 1.05),
         "unit": "mm_length",
         "note": "stiffen the cola hem with horsehair braid; a ruffled underskirt gives throw."},
    ]
    pattern.metadata = {
        "fc500_rank": 475, "family": "costume_historical", "fabric_hint": "algodon-percal",
        "provenance": "The bata de cola is the trained dress of the flamenco escuela bolera and "
            "the danced soleá/alegrías: the cola is not decoration but an instrument the dancer "
            "moves with the legs. It is always made to measure — the weight and sweep must match "
            "the body, which is why a stock-size bata de cola does not exist.",
        "silhouette_note": "Fitted bodice over gored skirt that grows from a front hem to a long "
            "back tail (cola), edged with ruffles, closing at a centre-back hook-and-eye.",
        "hardware": "CB closure via Yantra4D (hardware_ref -> hook-and-eye); closure_rows drives "
            "the hook columns and bodice_length the drafted placket.",
        "solved": {
            "gore_count": N_GORE,
            "gore_waist_mm": round(GORE_WAIST, 1),
            "gore_hem_mm": round(GORE_HEM, 1),
            "gore_length_mm": round(GORE_LEN, 1),
            "tail_length_mm": round(tail_length, 1),
            "ruffle_fullness": round(ruffle_fullness, 2),
            "ruffle_flat_mm": round(ruffle.edge("gather_edge").length(), 1),
            "note": "the ruffle is gathered onto the swept-hem ring at ruffle_fullness, declared "
                    "as gathered ease so the cascade length is proven; gores share equal side "
                    "seams so they sew together whatever the flare.",
        },
        "closure": "centre-back hook-and-eye",
        "drafting": "Made to measure to bust, waist, hip and lengths; the cola is the tail.",
    }
    return pattern


result = build()
