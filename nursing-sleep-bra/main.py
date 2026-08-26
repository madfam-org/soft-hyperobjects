"""
Nursing Sleep Bra — Fashion Cabinet Garment Cartridge (FC-500 #464; y4d bra-ring-slider).

A wire-free nursing bra cut for SLEEP: an ultra-soft pull-aside/drop cup on a wide comfort band,
no underwire, no hooks digging into a side-lying ribcage. The nursing function is a drop cup — the
cup detaches from the strap at a Yantra4D `bra-ring-slider` so one side can be dropped for feeding
one-handed in the dark — but unlike a day nursing bra it prioritises softness: a wide, low-
compression band, a folded cup edge, and a crossover front that needs no back closure.

Distinct from the commons' `nursing-bra` (a structured day bra with a drop-cup hinge on a firmer
band). This one is a sleep garment: `band_ease` is POSITIVE (a sleep bra does not compress), the
cup is a soft single piece gathered onto the band, and there is no hook — it pulls on over the
head.

The DIMENSIONAL HANDSHAKE. The drop mechanism is the Yantra4D `bra-ring-slider`, parameterised by
`strap_w`. The garment's `strap_width` drives BOTH the drafted strap/clip tab AND the hardware's
`strap_face` flange, so the printed slider is exactly as wide as the tab it clips to.
`strap_width` also drives the garment's own `drop_clip` interface — a coupled dimension, not a
name that resolves.

Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

underbust_girth = float(PARAM(lambda: underbust_girth, 800.0))
bust_girth      = float(PARAM(lambda: bust_girth, 1000.0))   # nursing bust runs fuller
band_height     = float(PARAM(lambda: band_height, 70.0))    # wide comfort band
cup_gather      = float(PARAM(lambda: cup_gather, 0.20))
crossover_frac  = float(PARAM(lambda: crossover_frac, 0.30)) # front crossover overlap
strap_width     = float(PARAM(lambda: strap_width, 18.0))    # wide soft strap
band_ease_pct   = float(PARAM(lambda: band_ease_pct, 4.0))   # POSITIVE ease (sleep = no squeeze)
cup_span_frac   = float(PARAM(lambda: cup_span_frac, 0.34))
seam_allowance  = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(700.0, min(bust_girth, 1600.0))
band_height     = max(40.0, min(band_height, 130.0))
cup_gather      = max(0.06, min(cup_gather, 0.36))
crossover_frac  = max(0.15, min(crossover_frac, 0.45))
strap_width     = max(10.0, min(strap_width, 32.0))
band_ease_pct   = max(0.0, min(band_ease_pct, 12.0))
cup_span_frac   = max(0.26, min(cup_span_frac, 0.44))
seam_allowance  = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry ─────────────────────────────────────────────────────────
POS = 1.0 + band_ease_pct / 100.0        # POSITIVE ease: sleep bra does not compress
BAND_FINISHED = underbust_girth * POS
BAND_HALF = BAND_FINISHED / 2.0
SURPLUS = max(28.0, (bust_girth - underbust_girth) / 2.0)
CUP_W = max(90.0, min(cup_span_frac * BAND_HALF, BAND_HALF - 40.0))
CUP_RISE = max(70.0, SURPLUS * 0.95 + 44.0)
BH = band_height


def _rect(x0, y0, w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(x0, y0), fc.P(x0 + w, y0), fc.P(x0 + w, y0 + h), fc.P(x0, y0 + h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def build_cup():
    """Soft drop cup: gathered onto the band, folded soft neckline, a clip tab at the top
    outer corner where the strap detaches at the ring-slider for the drop function."""
    mouth_run = CUP_W * (1.0 + cup_gather)
    bow = 0.12
    phi = 1.0
    for _ in range(48):
        s_over_run = (1.0 - math.cos(phi / 2.0)) / phi
        phi *= (bow / s_over_run) ** 0.5 if s_over_run > 1e-9 else 1.0
        phi = max(0.05, min(phi, math.pi))
    r = mouth_run / phi
    n = 33
    pts = [fc.P(r * math.cos(-math.pi / 2.0 - phi / 2.0 + phi * i / (n - 1)),
                r * math.sin(-math.pi / 2.0 - phi / 2.0 + phi * i / (n - 1)) + r)
           for i in range(n)]
    dx, dy = pts[0].x, pts[0].y
    pts = [fc.P(p.x - dx, p.y - dy) for p in pts]
    left, right = pts[0], pts[-1]
    apex_y = left.y + CUP_RISE
    clip_top = fc.P(right.x, apex_y - CUP_RISE * 0.06)
    edges = [
        fc.Edge("mouth", [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]),
        fc.Edge("clip_tab", [fc.Line(right, clip_top)]),
        fc.Edge("drop_edge", [fc.Line(clip_top, fc.P(clip_top.x - strap_width, clip_top.y))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(clip_top.x - strap_width, clip_top.y),
                                       fc.P((left.x + right.x) / 2.0, apex_y),
                                       fc.P(left.x + CUP_W * 0.16, left.y + CUP_RISE * 0.5),
                                       fc.P(left.x, left.y + CUP_RISE * 0.18))]),
        fc.Edge("center_front", [fc.Line(fc.P(left.x, left.y + CUP_RISE * 0.18), left)]),
    ]
    return fc.Piece(
        "cup", edges, seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},
        notches=[fc.Notch("mouth", 0.5, "gather centre")],
        grainline=fc.Grainline(fc.P((left.x + right.x) / 2.0, CUP_RISE * 0.2),
                               fc.P((left.x + right.x) / 2.0, CUP_RISE * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Soft drop cup (cut 2 pairs, gathered)",
    )


def build_band(cup_seat_len):
    """Wide comfort band, cut 2 mirror (CF crossover to CB). The top edge is split into a
    `cup_seat` run (exactly the flat length one cup gathers onto) and a `crossover_top` run
    (the extension that overlaps at the front so the bra pulls on with no back closure)."""
    seat = cup_seat_len
    cross = max(30.0, BAND_HALF * crossover_frac)
    total = BAND_HALF + cross
    # CCW rectangle, but the TOP edge is two segments: seat (front) then crossover.
    p_bl = fc.P(0.0, 0.0)                 # front-lower
    p_br = fc.P(total, 0.0)               # back-lower
    p_tr = fc.P(total, BH)               # back-top (CB)
    p_seat_end = fc.P(seat, BH)          # end of the cup seat along the top
    p_tl = fc.P(0.0, BH)                 # front-top
    edges = [
        fc.Edge("lower", [fc.Line(p_br, p_bl)]),
        fc.Edge("front_edge", [fc.Line(p_bl, p_tl)]),
        fc.Edge("cup_seat", [fc.Line(p_tl, p_seat_end)]),
        fc.Edge("crossover_top", [fc.Line(p_seat_end, p_tr)]),
        fc.Edge("center_back", [fc.Line(p_tr, p_br)]),
    ]
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "cup_seat": 0.0, "crossover_top": 0.0},  # elastic-finished
        notches=[fc.Notch("cup_seat", 0.5, "cup centre"),
                 fc.Notch("center_back", 0.5, "CB match")],
        grainline=fc.Grainline(fc.P(total * 0.5, BH * 0.25), fc.P(total * 0.5, BH * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wide comfort band with crossover (cut 2 pairs)",
    )


def build():
    pattern = fc.PatternSet("nursing-sleep-bra")
    cup = build_cup()
    # The flat seat one cup gathers onto = mouth / (1 + gather).
    seat_len = cup.edge("mouth").length() / (1.0 + cup_gather)
    band = build_band(seat_len)

    picked = {"cup": cup, "band": band}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cup, band):
            pattern.add(piece)
        # THE GATHER SEAM: the cup mouth is longer than the band's cup_seat by cup_gather —
        # the cup gathers onto the band. Declared with the gather as ease so the arithmetic
        # is proven (mouth = seat + ease), at every extreme.
        gather_ease = band.edge("cup_seat").length() * cup_gather
        pattern.declare_seam(("cup", "mouth"), ("band", "cup_seat"),
                             tol=1.0, ease=gather_ease)

    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * cup.edge("neckline").length()

    fabric_width = 1500.0
    area = cup.area() * 4.0 + band.area() * 2.0
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "cotton/modal soft jersey", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"a sleep bra wants the softest hand; at {fabric_width:.0f} mm width, 60% "
                 "marker. No underwire, no moulding — the cup is soft and gathered."},
        {"item": "drop-cup ring-slider set (Yantra4D bra-ring-slider)", "qty": 2, "unit": "set",
         "note": f"one per side; strap detaches at the slider for one-handed drop feeding "
                 f"(notion.hardware_ref -> bra-ring-slider); strap_w {strap_width:.0f} mm drives "
                 "the slider AND the drafted clip tab."},
        {"item": "soft band elastic (brushed, 25 mm)", "qty": round(band_opening * 0.98),
         "unit": "mm_length",
         "note": f"{band_opening:.0f} mm ring x 0.98 — barely eased; a sleep band must not "
                 "compress a side-lying ribcage."},
        {"item": "neckline elastic (soft picot, 8 mm)", "qty": round(neck_opening * 0.88),
         "unit": "mm_length", "note": f"neckline {neck_opening:.0f} mm at 0.88."},
        {"item": "coverstitch + wooly nylon", "qty": 1, "unit": "set",
         "note": "flatlock everything; a sleep bra has no seam that may press on the skin."},
    ]
    pattern.metadata = {
        "fc500_rank": 464, "family": "underwear_lounge", "fabric_hint": "jersey-algodon",
        "silhouette_note": "Wire-free nursing SLEEP bra: a soft gathered drop cup on a wide "
            "low-ease comfort band with a front crossover (no back closure), the cup detaching "
            "at a ring-slider for one-handed feeding. Prioritises softness over structure.",
        "hardware": "drop clip via Yantra4D (notion.hardware_ref -> bra-ring-slider); "
            "strap_width drives the slider's strap_face flange AND the drafted clip tab.",
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "band_ease_pct": round(band_ease_pct, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
            "cup_plan_width_mm": round(CUP_W, 1),
            "cup_gather": round(cup_gather, 3),
            "crossover_frac": round(crossover_frac, 3),
            "note": "band ease is POSITIVE — a sleep bra does not compress; the cup mouth "
                    "gathers onto the band top by cup_gather.",
        },
        "closure": "pull-on front crossover (no hook); drop cup at ring-slider",
        "drafting": "Made to measure to underbust and bust girths; wire-free, soft.",
    }
    return pattern


result = build()
