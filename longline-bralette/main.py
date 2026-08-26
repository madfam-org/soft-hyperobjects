"""
Longline Soft Bralette — Fashion Cabinet Garment Cartridge (FC-500 #459; y4d bra-ring-slider).

A wire-free bralette with a LONGLINE band: instead of the thin underband of a wired bra, the
support comes from a deep front frame that reaches from the wire line down to (or past) the
underbust, gripping a whole zone of ribcage at negative ease. No underwire — the shape is held by
a stretch-lace cup gathered onto a stable frame, and the load is spread over the longline band
rather than concentrated on a wire. Adjustable straps run through a Yantra4D `bra-ring-slider` at
the back wing.

What makes it a bralette and not a bra: the cup is a single soft piece (a folded, gathered lace
triangle), NOT a moulded/wired three-piece cup. Its lower edge is EASED onto the frame's top edge
— the gather is the shaping. So the frame's top edge is drafted SHORTER than the cup mouth by a
declared `cup_gather` ease, and the seam check proves the gather arithmetic:

    cup_mouth  =  frame_top * (1 + cup_gather)      # cup is longer; it gathers in

The DIMENSIONAL HANDSHAKE (the lane's discipline). The strap hardware is the Yantra4D `bra-ring-
slider`, parameterised by `strap_w` (the strap width the slider must pass). The garment's
`strap_width` drives BOTH the drafted strap tab on cup and wing AND the hardware's `strap_face`
flange — so the slider the wearer threads is exactly as wide as the tab it sits on. `strap_width`
also drives the garment's own `straps` interface, making the handshake a coupled dimension, not a
name that resolves.

Made to measure to underbust and bust girths. FC-500 lane 7 (intimates & loungewear III).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected; manifest
params arrive as BARE globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))  # cup|frame|band|back|set

underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))
bust_girth      = float(PARAM(lambda: bust_girth, 940.0))
longline_depth  = float(PARAM(lambda: longline_depth, 90.0))   # frame depth below wire line
band_height     = float(PARAM(lambda: band_height, 26.0))      # elastic underband depth
cup_gather      = float(PARAM(lambda: cup_gather, 0.18))       # cup mouth surplus over frame
strap_width     = float(PARAM(lambda: strap_width, 14.0))
negative_ease_pct = float(PARAM(lambda: negative_ease_pct, 14.0))
cup_span_frac   = float(PARAM(lambda: cup_span_frac, 0.30))    # cup plan width / half band
seam_allowance  = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1200.0))
bust_girth      = max(640.0, min(bust_girth, 1500.0))
longline_depth  = max(50.0, min(longline_depth, 180.0))
band_height     = max(16.0, min(band_height, 60.0))
cup_gather      = max(0.06, min(cup_gather, 0.34))
strap_width     = max(8.0, min(strap_width, 28.0))
negative_ease_pct = max(6.0, min(negative_ease_pct, 22.0))
cup_span_frac   = max(0.22, min(cup_span_frac, 0.40))
seam_allowance  = max(0.0, min(seam_allowance, 12.0))

# ── Support geometry (all clamped explicitly) ────────────────────────────────
NEG = 1.0 - negative_ease_pct / 100.0
BAND_FINISHED = underbust_girth * NEG
BAND_HALF = BAND_FINISHED / 2.0
# Bust surplus over the ribcage, per side — the volume the soft cup contains.
SURPLUS = max(20.0, (bust_girth - underbust_girth) / 2.0)
# Cup plan width as a fraction of the half band, floored so the frame top never vanishes.
CUP_W = max(80.0, min(cup_span_frac * BAND_HALF, BAND_HALF - 40.0))
# Cup rise: how tall the soft triangle stands, driven by the surplus.
CUP_RISE = max(60.0, SURPLUS * 0.9 + 40.0)
LD = longline_depth
BH = band_height


def _rect(x0, y0, w, h, names):
    """A CCW rectangle with four named edges; w,h must already be > 0."""
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1 = fc.P(x0, y0), fc.P(x0 + w, y0)
    p2, p3 = fc.P(x0 + w, y0 + h), fc.P(x0, y0 + h)
    return [
        fc.Edge(names[0], [fc.Line(p0, p1)]),
        fc.Edge(names[1], [fc.Line(p1, p2)]),
        fc.Edge(names[2], [fc.Line(p2, p3)]),
        fc.Edge(names[3], [fc.Line(p3, p0)]),
    ]


def build_cup():
    """The soft cup: a gathered lace triangle. Its `mouth` (lower edge) is drafted as a
    shallow arc LONGER than the frame top by `cup_gather`, so the gather is the shaping.

    The mouth run is CUP_W * (1 + cup_gather): the frame top is CUP_W, and the cup gathers
    onto it. Built as a circular arc of that run so the drafted mouth length is exact.
    """
    mouth_run = CUP_W * (1.0 + cup_gather)
    # Solve a shallow circular arc of length mouth_run and a chosen bow (sagitta/run).
    bow = 0.12
    phi = 1.0
    for _ in range(48):
        s_over_run = (1.0 - math.cos(phi / 2.0)) / phi
        phi *= (bow / s_over_run) ** 0.5 if s_over_run > 1e-9 else 1.0
        phi = max(0.05, min(phi, math.pi))
    r = mouth_run / phi
    n = 33
    pts = []
    for i in range(n):
        a = -math.pi / 2.0 - phi / 2.0 + phi * i / (n - 1)
        pts.append(fc.P(r * math.cos(a), r * math.sin(a) + r))
    dx, dy = pts[0].x, pts[0].y
    pts = [fc.P(p.x - dx, p.y - dy) for p in pts]  # left tip at origin
    left, right = pts[0], pts[-1]
    apex = fc.P((left.x + right.x) / 2.0, left.y + CUP_RISE)
    # tabs: the outer top corner carries the strap tab
    strap_top = fc.P(right.x, apex.y - CUP_RISE * 0.10)
    edges = [
        fc.Edge("mouth", [fc.Line(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]),
        fc.Edge("side", [fc.Line(right, strap_top)]),
        fc.Edge("strap_tab", [fc.Line(strap_top, fc.P(strap_top.x - strap_width, strap_top.y))]),
        fc.Edge("neckline", [fc.Bezier(fc.P(strap_top.x - strap_width, strap_top.y),
                                       fc.P(apex.x + CUP_W * 0.10, apex.y),
                                       fc.P(left.x + CUP_W * 0.14, left.y + CUP_RISE * 0.52),
                                       fc.P(left.x, left.y + CUP_RISE * 0.20))]),
        fc.Edge("center_front", [fc.Line(fc.P(left.x, left.y + CUP_RISE * 0.20), left)]),
    ]
    piece = fc.Piece(
        "cup", edges,
        seam_allowance=seam_allowance,
        allowances={"neckline": 0.0},  # elastic-finished
        notches=[fc.Notch("mouth", 0.5, "gather centre"),
                 fc.Notch("mouth", 0.25, "gather"),
                 fc.Notch("mouth", 0.75, "gather")],
        grainline=fc.Grainline(fc.P(apex.x, CUP_RISE * 0.20), fc.P(apex.x, CUP_RISE * 0.70)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Soft lace cup (cut 2 pairs, gathered)",
    )
    return piece


def build_frame():
    """The longline front frame: a deep stable panel from the wire line down to the
    underbust. Its `cup_seat` top edge is drafted to CUP_W — SHORTER than the cup mouth by
    the gather — so the cup gathers onto it. Its lower edge sits on the elastic band.
    """
    # top edge is CUP_W wide; the frame spans the whole front (two cup seats + centre gore).
    front_half = max(CUP_W + 30.0, BAND_HALF * 0.55)
    # CCW rectangle-ish frame: bottom (band seam), CF side up, top run, side down.
    p_bl = fc.P(0.0, 0.0)
    p_br = fc.P(front_half, 0.0)
    p_tr = fc.P(front_half, LD)
    # cup seat is the CUP_W run at the top, from CF inward
    p_seat_l = fc.P(0.0, LD)
    p_seat_r = fc.P(CUP_W, LD)
    edges = [
        fc.Edge("band_seam", [fc.Line(p_br, p_bl)]),        # bottom (to band top)
        fc.Edge("center_front", [fc.Line(p_bl, p_seat_l)]),  # CF up
        fc.Edge("cup_seat", [fc.Line(p_seat_l, p_seat_r)]),  # the gather seat (== CUP_W)
        fc.Edge("upper_edge", [fc.Bezier(p_seat_r,
                                         fc.P(CUP_W + (front_half - CUP_W) * 0.4, LD - 6.0),
                                         fc.P(CUP_W + (front_half - CUP_W) * 0.8, LD * 0.72),
                                         p_tr)]),             # up-and-out to side
        fc.Edge("side", [fc.Line(p_tr, p_br)]),              # side down
    ]
    piece = fc.Piece(
        "frame", edges,
        seam_allowance=seam_allowance,
        allowances={"upper_edge": 0.0},  # elastic-finished neckline continuation
        notches=[fc.Notch("cup_seat", 0.5, "cup centre"),
                 fc.Notch("band_seam", 0.5, "band match")],
        grainline=fc.Grainline(fc.P(front_half * 0.5, LD * 0.2), fc.P(front_half * 0.5, LD * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Longline front frame (cut 2 pairs)",
    )
    return piece


def build_band(frame_bottom_len):
    """Elastic underband under the longline frame — the negative-ease grip that seats
    the whole assembly. `top_front` is built to the measured frame bottom."""
    front = frame_bottom_len
    back = max(40.0, BAND_HALF - front)
    total = front + back
    edges = _rect(0.0, 0.0, total, BH, ("lower", "center_back", "top", "center_front"))
    # split top into front/back conceptually via a notch; keep single edge for the seam
    piece = fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0},  # elastic-finished
        notches=[fc.Notch("top", front / total, "frame edge"),
                 fc.Notch("center_back", 0.5, "back match")],
        grainline=fc.Grainline(fc.P(total * 0.5, BH * 0.25), fc.P(total * 0.5, BH * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Underband (cut 2 pairs)",
    )
    return piece


def build_back(side_len, back_span):
    """Back wing: strap tab (carries the ring-slider), side seam to the frame, CB, band."""
    wing_h = max(side_len, LD * 0.5)
    x_end = max(back_span, 60.0)
    side = fc.Edge("side", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, wing_h))])
    strap_tab = fc.Edge("strap_tab", [fc.Line(fc.P(0.0, wing_h), fc.P(strap_width, wing_h))])
    top = fc.Edge("top", [fc.Bezier(fc.P(strap_width, wing_h),
                                    fc.P(x_end * 0.42, wing_h * 0.66),
                                    fc.P(x_end * 0.84, BH + 8.0),
                                    fc.P(x_end, BH))])
    cb = fc.Edge("center_back", [fc.Line(fc.P(x_end, BH), fc.P(x_end, 0.0))])
    bottom = fc.Edge("band_seam", [fc.Line(fc.P(x_end, 0.0), fc.P(0.0, 0.0))])
    piece = fc.Piece(
        "back", [side, strap_tab, top, cb, bottom],
        seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("band_seam", 0.5, "band match"),
                 fc.Notch("center_back", 0.5, "hook position")],
        grainline=fc.Grainline(fc.P(x_end * 0.5, BH * 0.4), fc.P(x_end * 0.5, wing_h * 0.7)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back wing (cut 2 pairs, ring-slider strap)",
    )
    return piece


def build():
    pattern = fc.PatternSet("longline-bralette")
    cup = build_cup()
    frame = build_frame()
    band = build_band(frame.edge("band_seam").length())
    back_span = max(40.0, BAND_HALF - frame.edge("band_seam").length())
    back = build_back(frame.edge("side").length() + cup.edge("side").length(), back_span)

    picked = {"cup": cup, "frame": frame, "band": band, "back": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cup, frame, band, back):
            pattern.add(piece)
        # THE GATHER SEAM: the cup mouth is LONGER than the frame seat by cup_gather —
        # the cup gathers onto the frame. Declared with the gather as ease so the seam
        # check proves the gather arithmetic (mouth = seat + ease).
        gather_ease = frame.edge("cup_seat").length() * cup_gather
        pattern.declare_seam(("cup", "mouth"), ("frame", "cup_seat"),
                             tol=1.0, ease=gather_ease)
        # Frame front + back wing together seat on the band's whole top edge.
        pattern.declare_seam([("frame", "band_seam"), ("back", "band_seam")],
                             ("band", "top"), tol=1.5)
        # Side seam: cup outer rise + frame side joins the wing side.
        pattern.declare_seam([("cup", "side"), ("frame", "side")], ("back", "side"), tol=1.5)

    # ── Elastic + hardware accounting ────────────────────────────────────────
    band_opening = 2.0 * band.edge("lower").length()
    neck_opening = 2.0 * (cup.edge("neckline").length() + frame.edge("upper_edge").length())
    wing_opening = 2.0 * back.edge("top").length()

    fabric_width = 1400.0
    area = (cup.area() * 4.0 + frame.area() * 4.0 + band.area() * 2.0 + back.area() * 2.0)
    marker_len = area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "stretch lace (cup) + power mesh (frame/band)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"cups in stretch lace (the gather lives in the stretch); frame and band "
                 f"in stable power mesh at {fabric_width:.0f} mm width, 55% marker."},
        {"item": "strap elastic 12 mm + ring-slider set (Yantra4D bra-ring-slider)",
         "qty": 2, "unit": "set",
         "note": f"adjustable straps threaded through the printable ring-slider "
                 f"(notion.hardware_ref -> bra-ring-slider); strap_w {strap_width:.0f} mm "
                 "drives the slider AND the drafted strap tab."},
        {"item": "band elastic (plush-back) 12 mm", "qty": round(band_opening * 0.90),
         "unit": "mm_length",
         "note": f"exact cut: {band_opening:.0f} mm opening x 0.90 — the longline band "
                 "carries the load, cut short and stretched on."},
        {"item": "neckline elastic (picot) 8 mm", "qty": round(neck_opening * 0.85),
         "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm at 0.85 into the marked zones."},
        {"item": "wing/armhole elastic (picot) 8 mm", "qty": round(wing_opening * 0.85),
         "unit": "mm_length", "note": f"wing top {wing_opening:.0f} mm at 0.85."},
        {"item": "polyester thread + ballpoint 70/10", "qty": 1, "unit": "set",
         "note": "fine needle; the cup mouth is gathered onto the frame seat, not sewn flat."},
    ]
    pattern.metadata = {
        "fc500_rank": 459, "family": "underwear_lounge", "fabric_hint": "encaje-elastico",
        "silhouette_note": "Wire-free longline bralette: a soft gathered lace cup on a deep "
            "stable front frame over a negative-ease band. The support is spread over the "
            "longline zone, not concentrated on a wire.",
        "hardware": "adjustable straps via Yantra4D (notion.hardware_ref -> bra-ring-slider); "
            "strap_width drives BOTH the slider's strap_face flange and the drafted strap "
            "tab — the dimensional handshake.",
        "gather": {
            "cup_gather": round(cup_gather, 3),
            "frame_seat_mm": round(frame.edge("cup_seat").length(), 2),
            "cup_mouth_mm": round(cup.edge("mouth").length(), 2),
            "note": "cup_mouth = frame_seat * (1 + cup_gather): the cup is drafted longer "
                    "and gathers onto the frame — the gather is the cup's shaping.",
        },
        "solved": {
            "band_finished_mm": round(BAND_FINISHED, 1),
            "bust_surplus_mm": round(SURPLUS, 1),
            "cup_plan_width_mm": round(CUP_W, 1),
            "cup_rise_mm": round(CUP_RISE, 1),
            "band_opening_mm": round(band_opening, 1),
        },
        "closure": "pull-on (no back closure); adjustable ring-slider straps",
        "drafting": "Made to measure to underbust and bust girths; wire-free.",
    }
    return pattern


result = build()
