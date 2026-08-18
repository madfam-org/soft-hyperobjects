"""
Puffer Jacket — FC-100 rank #31. Fashion Cabinet Garment Cartridge.

A roomy insulated zip jacket on the bomber-jacket architecture (rank #29): the
front is cut as TWO mirrored halves — never on fold — whose center edge is the
separating zipper seam (15 mm tape allowance, top/bottom stop notches, 7 mm
stitch line per the zipper-notion installation convention). The signature is
the QUILT: horizontal quilt CHANNELS drawn as `fc.Internal(kind="trace")`
lines across the front, back and sleeve at a `channel_spacing` param (default
80 mm) — the shell and lining are quilted to each other over the fill, channel
by channel. The collar is a self-fabric FUNNEL (stand) collar, cut on fold at
center back, derived to the full neck opening. The long sleeve cap stays SOLVED
by bisection against the measured armhole pair; the elastic cuffs are a derived
band (sleeve opening x cuff_ratio); the hem is an elastic-cased finish (no
separate piece). Metadata derives the closed-end separating zipper length to
order; the BOM lists shell + lining + insulating fill (by area) + zipper +
cuff/hem elastic (exact mm) + thread. Slider/pull hardware is a Yantra4D solid,
federated through the zipper-notion cartridge.

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


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth     = float(PARAM(lambda: chest_girth, 1080.0))
body_length     = float(PARAM(lambda: body_length, 680.0))
neck_girth      = float(PARAM(lambda: neck_girth, 400.0))
sleeve_length   = float(PARAM(lambda: sleeve_length, 620.0))
puffer_ease     = float(PARAM(lambda: puffer_ease, 300.0))
channel_spacing = float(PARAM(lambda: channel_spacing, 80.0))
collar_height   = float(PARAM(lambda: collar_height, 95.0))
cuff_ratio      = float(PARAM(lambda: cuff_ratio, 0.80))
cuff_height     = float(PARAM(lambda: cuff_height, 60.0))
hem_elastic_ratio = float(PARAM(lambda: hem_elastic_ratio, 0.85))
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider min/max) ──────────────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
body_length = max(420.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
puffer_ease = max(150.0, min(puffer_ease, 520.0))
channel_spacing = max(40.0, min(channel_spacing, 160.0))
collar_height = max(40.0, min(collar_height, 160.0))
cuff_ratio = max(0.60, min(cuff_ratio, 0.95))
cuff_height = max(30.0, min(cuff_height, 100.0))
hem_elastic_ratio = max(0.70, min(hem_elastic_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

W = (chest_girth + puffer_ease) / 4.0
L = body_length
AH = (chest_girth + puffer_ease) / 8.0 + 110.0        # roomy armhole for loft
AH = max(190.0, min(AH, L - 100.0))
NW = max(62.0, neck_girth / 5.0 + 6.0)                # funnel collar wants room
HPS_Y = L + 20.0
SH_END = fc.P(W - 5.0, HPS_Y - 30.0)
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 70.0
BACK_NECK_DROP = 20.0
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 10.0  # stop notches sit this far inside the seam ends


def _armhole_edge():
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - 12.0, SH_END.y - AH * 0.35),
                   fc.P(W - 5.0, UNDERARM.y + AH * 0.30), UNDERARM)],
    )


def _body_edges(neck_drop):
    """Half-body outline shared by front and back; center edge at x = 0."""
    neck_top_y = HPS_Y - neck_drop
    origin = fc.P(0.0, 0.0)
    neck = fc.Edge(
        "neck",
        [fc.Bezier(fc.P(0.0, neck_top_y), fc.P(NW * 0.55, neck_top_y),
                   fc.P(NW, neck_top_y + max(neck_drop, 24.0) * 0.45), fc.P(NW, HPS_Y))],
    )
    return [
        fc.Edge("center", [fc.Line(origin, fc.P(0.0, neck_top_y))]),
        neck,
        fc.Edge("shoulder", [fc.Line(fc.P(NW, HPS_Y), SH_END)]),
        _armhole_edge(),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(W, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(W, 0.0), origin)]),
    ]


def _x_span_at(ring, y):
    """Min/max x where the closed stitch ring crosses the horizontal line y.

    Scans every ring segment for a crossing of the scanline; returns
    (x_min, x_max) or None when the line misses the piece. Used to clip each
    quilt channel to the piece silhouette so the trace stays inside the outline.
    """
    xs = []
    n = len(ring)
    for i in range(n):
        a = ring[i]
        b = ring[(i + 1) % n]
        if (a.y <= y <= b.y) or (b.y <= y <= a.y):
            if abs(b.y - a.y) < 1e-9:
                xs.append(a.x)
                xs.append(b.x)
            else:
                t = (y - a.y) / (b.y - a.y)
                xs.append(a.x + (b.x - a.x) * t)
    if len(xs) < 2:
        return None
    return min(xs), max(xs)


def _quilt_channels(piece, inset=14.0):
    """Horizontal quilt-channel traces across a shell piece at channel_spacing.

    Lines are placed every `channel_spacing` up the piece's vertical span and
    each is clipped to the silhouette (minus a small inset so the stitch does
    not run off the cut edge). The quilt is what holds the fill; each channel
    is one shell↔lining quilting pass.
    """
    ring = piece.stitch_outline()
    ys = [p.y for p in ring]
    y_lo, y_hi = min(ys) + channel_spacing * 0.6, max(ys) - channel_spacing * 0.6
    internals = []
    y = y_lo
    idx = 1
    while y <= y_hi + 1e-6:
        span = _x_span_at(ring, y)
        if span is not None and (span[1] - span[0]) > 3.0 * inset:
            x0, x1 = span[0] + inset, span[1] - inset
            internals.append(
                fc.Internal(f"quilt channel {idx}",
                            [fc.P(x0, y), fc.P(x1, y)], kind="trace")
            )
            idx += 1
        y += channel_spacing
    return internals


def build_front():
    """Half front, cut 2 mirrored (never on fold): center edge is the zip seam."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length
    t_stop = ZIP_STOP_INSET / zlen
    stitch = fc.Internal(
        "zipper stitch line",
        [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
        kind="trace",
    )
    piece = fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance + 24.0, "center": ZIP_SA},  # hem casing
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5),
            fc.Notch("center", 1.0 - t_stop, "zipper top stop"),
            fc.Notch("center", t_stop, "zipper bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (quilted zip half)",
    )
    piece.internals = [stitch] + _quilt_channels(piece)
    return piece


def build_back():
    piece = fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance + 24.0},    # hem casing
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5)],
        grainline=fc.Grainline(fc.P(W * 0.62, 70.0), fc.P(W * 0.62, L - 110.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (quilted)",
    )
    piece.internals = _quilt_channels(piece)
    return piece


def _cap_curve(hb, sl, ch):
    apex = fc.P(0.0, sl + ch)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.65, sl + ch * 0.12), fc.P(hb * 0.32, sl + ch), apex),
        fc.Bezier(apex, fc.P(-hb * 0.32, sl + ch), fc.P(-hb * 0.65, sl + ch * 0.12), fc.P(-hb, sl)),
    ])


def build_sleeve(cap_target):
    """Long roomy sleeve; the cap is solved by bisection to the armhole pair."""
    ch = max(50.0, AH * 0.30)
    sl = max(100.0, sleeve_length - ch)
    lo, hi = 20.0, cap_target / 2.0 + ch + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl, ch).length(0.05) < cap_target:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl, ch).length(0.05) - cap_target) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(95.0, hb * 0.66)
    piece = fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl, ch),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": seam_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 30.0), fc.P(0.0, sl + ch * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (quilted)",
    )
    piece.internals = _quilt_channels(piece)
    return piece


def build_collar(neck_opening):
    """Self-fabric funnel (stand) collar, cut 1 on fold at center back.

    Derived — no solver. Cut on fold at CB, so the drafted "neck" edge is HALF
    the neckline: neck_opening/2 + seam_allowance, sewing to one front half +
    one back half with the 1 sa as the declared ease (delta ~ 0). Height =
    collar_height; the fold at the top makes it a double-layer funnel that
    stands, quilted like the body over a light fill.
    """
    half = neck_opening / 2.0 + seam_allowance      # cut on fold at CB
    band_h = 2.0 * collar_height                     # folded double funnel
    piece = fc.Piece(
        "collar",
        [
            fc.Edge("neck", [fc.Line(fc.P(0.0, 0.0), fc.P(half, 0.0))]),
            fc.Edge("cf_end", [fc.Line(fc.P(half, 0.0), fc.P(half, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(half, band_h), fc.P(0.0, band_h))]),
            fc.Edge("cb_fold", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck", 1.0, "center back on fold")],
        grainline=fc.Grainline(fc.P(half * 0.2, band_h / 2.0),
                               fc.P(half * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line (funnel top)",
                               [fc.P(0.0, band_h / 2.0), fc.P(half, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold", mirror=True),
        label="Funnel Collar (stand)",
    )
    return piece


def build_cuff(cuff_opening):
    """Elastic cuff band, cut 2: derived length = sleeve opening x cuff_ratio.

    Cut flat and joined into a ring; folded to 2 x cuff_height with elastic
    threaded through, so the roomy sleeve gathers to a snug wrist.
    """
    band_h = 2.0 * cuff_height
    length = cuff_opening * cuff_ratio + 2.0 * seam_allowance
    return fc.Piece(
        "cuff",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, band_h))]),
            fc.Edge("top", [fc.Line(fc.P(length, band_h), fc.P(0.0, band_h))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(length * 0.2, band_h / 2.0),
                               fc.P(length * 0.8, band_h / 2.0)),
        internals=[fc.Internal("fold line", [fc.P(0.0, band_h / 2.0),
                                             fc.P(length, band_h / 2.0)])],
        cut=fc.CutSpec(quantity=2),
        label="Cuff (elastic band)",
    )


def build():
    pattern = fc.PatternSet("puffer-jacket")
    front = build_front()
    back = build_back()
    cap_target = front.edge("armhole").length(0.05) + back.edge("armhole").length(0.05)
    # Full neck opening: TWO front halves (cut 2) + the folded back's two halves.
    neck_opening = 2.0 * (front.edge("neck").length(0.05) + back.edge("neck").length(0.05))
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    sleeve = None
    if everything or target_piece in ("sleeve", "cuff"):
        sleeve = build_sleeve(cap_target)          # cuff needs the measured opening
    if everything or target_piece == "sleeve":
        pattern.add(sleeve)
    if everything or target_piece == "collar":
        pattern.add(build_collar(neck_opening))
    if everything or target_piece == "cuff":
        pattern.add(build_cuff(sleeve.edge("hem").length()))
    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Front is cut 2 (not on fold), so each PHYSICAL sleeve still meets
        # exactly ONE front armhole + ONE back armhole — the drafted pair.
        pattern.declare_seam([("sleeve", "cap")],
                             [("front", "armhole"), ("back", "armhole")], tol=2.0)
        pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"),
                             tol=1.0)
        # Collar is cut ON FOLD, so its drafted "neck" edge is HALF the neckline
        # and sews to one front half + one back half (= front.neck + back.neck).
        # The derived half is neck_opening/2 + seam_allowance, so the 1 sa is the
        # declared ease and delta ~ 0.
        pattern.declare_seam([("collar", "neck")],
                             [("front", "neck"), ("back", "neck")],
                             tol=2.0, ease=seam_allowance)

    # ── Metadata: solved dims + honest teaching-grade note ───────────────────
    zip_total = front.edge("center").length()      # CF opening, hem to top stop
    channels_front = len([i for i in front.internals if i.label.startswith("quilt")])
    channels_back = len([i for i in back.internals if i.label.startswith("quilt")])
    channels_sleeve = (len([i for i in sleeve.internals if i.label.startswith("quilt")])
                       if sleeve is not None else 0)
    pattern.metadata = {
        "fc100_rank": 31,
        "fabric_hint": "nylon-ripstop-shell",
        "zipper_length_mm": int(round(zip_total / 10.0) * 10),
        "zipper_note": ("order this closed-end SEPARATING zipper; slider/pull "
                        "hardware via the zipper-notion Yantra4D cartridge"),
        "channel_spacing_mm": round(channel_spacing, 1),
        "quilt_channels": {"front": channels_front, "back": channels_back,
                           "sleeve": channels_sleeve},
        "neck_opening_mm": round(neck_opening, 1),
        "collar_half_neck_mm": round(neck_opening / 2.0 + seam_allowance, 1),
        "cap_target_mm": round(cap_target, 1),
        "cuff_opening_mm": round(sleeve.edge("hem").length(), 1) if sleeve else None,
        "quilting": ("shell (nylon-ripstop-shell) and lining are quilted to each "
                     "other over the fill along the horizontal channels; the "
                     "channels are traces, geometry stays a roomy jacket"),
        "drafting": ("bomber-jacket block widened for loft + layering; hood/rib "
                     "collar swapped for a derived self-fabric funnel collar; "
                     "elastic-cased hem (no separate piece); quilt channels are "
                     "fc.Internal traces at channel_spacing, clipped to each "
                     "shell silhouette; teaching-grade — a production puffer "
                     "adds baffle geometry (box-wall or sewn-through) and a "
                     "wind-flap behind the zip"),
    }

    # ── BOM: shell + lining + fill (by area) + zipper + elastic + thread ─────
    shell_width = 1450.0                            # nylon-ripstop-shell card
    lining_width = 1450.0
    shell_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    marker_len = shell_area / (shell_width * 0.62)   # slippery ripstop marks ~62%
    lining_len = marker_len * 0.92                   # lining ~ shell less collars
    # Insulated body area (front + back + sleeve) drives the fill weight; a
    # mid-loft synthetic runs ~120 gsm across the quilted panels.
    fill_area_m2 = 0.0
    for name in ("front", "back", "sleeve"):
        try:
            p = pattern.piece(name)
            fill_area_m2 += p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        except KeyError:
            pass
    fill_area_m2 = fill_area_m2 / 1.0e6              # mm² → m²
    fill_grams = int(round(fill_area_m2 * 120.0))    # ~120 gsm synthetic loft
    # Elastic: cuffs (2 x cuff opening x ratio) + hem casing (hem circ x ratio).
    cuff_elastic = 0.0
    if sleeve is not None:
        cuff_elastic = 2.0 * sleeve.edge("hem").length() * cuff_ratio
    hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
    hem_elastic = hem_circ * hem_elastic_ratio
    pattern.bom = [
        {"item": "nylon-ripstop-shell", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"outer shell at {shell_width:.0f} mm width, ~62% marker "
                 "efficiency (slippery ripstop marks low); pin inside the "
                 "allowance, fine microtex needle so needle holes stay small"},
        {"item": "downproof lining (nylon taffeta / ripstop)",
         "qty": round(lining_len / 10.0) * 10, "unit": "mm_length",
         "note": f"inner quilt face at {lining_width:.0f} mm width; shell + "
                 "lining are quilted to each other over the fill along the "
                 "channels; lining pieces derived from the shell, not "
                 "separately drafted in v0"},
        {"item": "insulating fill (synthetic loft or down, ~120 gsm)",
         "qty": fill_grams, "unit": "g",
         "note": f"~{fill_area_m2:.2f} m² of quilted panels (front + back + "
                 "sleeves) at ~120 gsm mid-loft; down is a warmer swap at "
                 "lower gsm; the channel_spacing sets the baffle pitch"},
        {"item": "closed-end separating zipper", "qty": 1, "unit": "pcs",
         "note": f"~{int(round(zip_total / 10.0) * 10)} mm; a SEPARATING zip "
                 "for a jacket front; slider/pull hardware is a Yantra4D "
                 "cartridge (zipper-notion), never re-implemented here"},
        {"item": "cuff + hem elastic (8-10 mm knit)",
         "qty": round((cuff_elastic + hem_elastic) / 10.0) * 10, "unit": "mm_length",
         "note": f"cuffs ~{round(cuff_elastic)} mm (2 x sleeve opening x "
                 f"{cuff_ratio:.2f}) threaded through the folded band + hem "
                 f"casing ~{round(hem_elastic)} mm (hem circ x "
                 f"{hem_elastic_ratio:.2f}) through the 24 mm hem allowance"},
        {"item": "all-purpose polyester thread + microtex needle 70/10",
         "qty": 1, "unit": "set",
         "note": "topstitch the quilt channels through shell + fill + lining; "
                 "a walking foot keeps the slippery layers from shifting"},
    ]
    return pattern


result = build()
