"""
Puffer Vest — FC-100 rank #64. Fashion Cabinet Garment Cartridge.

The puffer jacket with the sleeves removed: a roomy SLEEVELESS insulated zip
vest ("chaleco acolchado"). The body is the zip-hoodie / bomber-jacket block
(rank #14 / #29) halved at center front — the front is cut as TWO mirrored
halves whose center edge is the full separating-zipper seam (15 mm tape
allowance, top/bottom stop notches, 7 mm stitch line per the zipper-notion
convention). With no sleeve, each ARMHOLE is a finished/BOUND edge — a clean
armscye curve, bound with a strip or elastic, no sleeve piece (the waistcoat's
bound-armscye method). A STAND / funnel collar is solved by bisection to the
full neck opening (front×2 + back×2), so collar.neckline ↔ neckline is
delta≈0 (the hood-neck attach-to-measured-curve method).

The signature is the QUILTING: horizontal quilt CHANNELS are drawn on the shell
of the front and back as `fc.Internal(kind="trace")` lines at `channel_spacing`
(default 80 mm). The garment is the ripstop shell + a lining quilted over the
insulation (down or synthetic fill) between them — geometry is a normal roomy
vest; the quilt lines are traces and the fill/lining are BOM. The hem is a
bound / elastic-cased finished edge (BOM: elastic, exact mm). Optional zip
hand-warmer pockets are welt markings. Zipper slider/pull hardware is a
Yantra4D solid, federated through the zipper-notion cartridge.

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
# front|back|collar|set

chest_girth     = float(PARAM(lambda: chest_girth, 1060.0))
body_length     = float(PARAM(lambda: body_length, 680.0))
neck_girth      = float(PARAM(lambda: neck_girth, 400.0))
puffer_ease     = float(PARAM(lambda: puffer_ease, 240.0))   # roomy over layers
channel_spacing = float(PARAM(lambda: channel_spacing, 80.0))  # quilt channel pitch
collar_height   = float(PARAM(lambda: collar_height, 90.0))   # stand/funnel height
loft_mm         = float(PARAM(lambda: loft_mm, 25.0))         # insulation loft (fill)
hem_elastic     = float(PARAM(lambda: hem_elastic, 0.90))     # hem draw ratio (bound)
pockets         = bool(PARAM(lambda: pockets, True))          # zip hand-warmer marks
seam_allowance  = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance   = float(PARAM(lambda: hem_allowance, 22.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1900.0))
body_length = max(440.0, min(body_length, 900.0))
neck_girth = max(300.0, min(neck_girth, 540.0))
puffer_ease = max(120.0, min(puffer_ease, 480.0))
channel_spacing = max(40.0, min(channel_spacing, 160.0))
collar_height = max(40.0, min(collar_height, 140.0))
loft_mm = max(8.0, min(loft_mm, 60.0))
hem_elastic = max(0.7, min(hem_elastic, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 40.0))

# ── Vest block (roomy body, no sleeve; armhole is a bound finished edge) ──────
W = (chest_girth + puffer_ease) / 4.0            # quarter body width (with loft ease)
L = body_length                                  # datum y=0 is the hem
AH = (chest_girth + puffer_ease) / 8.0 + 100.0   # armhole depth
AH = max(190.0, min(AH, L - 90.0))
NW = max(62.0, neck_girth / 5.0 + 4.0)           # half neck width at HPS
HPS_Y = L + 20.0
SH_END = fc.P(W - 8.0, HPS_Y - 32.0)             # dropped, roomy shoulder
UNDERARM = fc.P(W, SH_END.y - AH)
FRONT_NECK_DROP = 80.0
BACK_NECK_DROP = 22.0
ARM_SCOOP = 20.0                                 # sleeveless armscye scoop
ZIP_SA = 15.0          # tape allowance on the front center edge (zipper seam)
ZIP_STITCH = 7.0       # stitch line offset from the seam line (zipper-notion)
ZIP_STOP_INSET = 10.0  # stop notches sit this far inside the seam ends
CHANNEL_MARGIN = 45.0  # keep channel traces clear of hem and shoulder


def _armhole_edge():
    """Sleeveless bound armscye: shoulder end down to the underarm (no sleeve).

    A slightly scooped clean armhole curve; it is BOUND (strip or elastic), not
    sewn to a sleeve — so it is a finished edge, never a declared seam (the
    waistcoat's bound-armscye method)."""
    fah = SH_END.y - UNDERARM.y
    return fc.Edge(
        "armhole",
        [fc.Bezier(SH_END, fc.P(W - ARM_SCOOP, SH_END.y - fah * 0.35),
                   fc.P(W - 6.0, UNDERARM.y + fah * 0.30), UNDERARM)],
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


def _quilt_channels(x_lo, x_hi, label):
    """Horizontal quilt channels across a shell panel, at `channel_spacing`.

    Traces (kind="trace") — the sew-through lines that hold the loft; they are
    markings, not seams. First channel sits one spacing above the hem; the last
    stops CHANNEL_MARGIN below the shoulder line so it clears the neck/armhole."""
    marks = []
    y = channel_spacing
    top_limit = SH_END.y - CHANNEL_MARGIN
    n = 0
    while y <= top_limit:
        n += 1
        marks.append(
            fc.Internal(f"{label} channel {n}",
                        [fc.P(x_lo, y), fc.P(x_hi, y)], kind="trace")
        )
        y += channel_spacing
    return marks


def _pocket_marks():
    """Zip hand-warmer pocket: a near-vertical 150 mm opening trace toward CF,
    plus a surround box. Markings only (welt method); the pocket zip is another
    zipper-notion reference in the BOM, not modeled here."""
    cx = min(W * 0.52, W - 95.0)
    cy = max(120.0, min(L * 0.30, UNDERARM.y - 90.0))
    along = fc.P(-0.30, 1.0)                        # opening runs up-and-inward
    along = fc.P(along.x / along.length(), along.y / along.length())
    perp = fc.P(along.y, -along.x)
    p1 = fc.P(cx - 22.0, cy - 72.0)                 # lower end (toward CF)
    p2 = fc.P(cx + 22.0, cy + 72.0)                 # upper end (toward chest)
    opening = fc.Internal("pocket zip opening", [p1, p2], kind="trace")
    e1 = p1 - along * 10.0
    e2 = p2 + along * 10.0
    corners = [e1 + perp * 18.0, e2 + perp * 18.0, e2 - perp * 18.0, e1 - perp * 18.0]
    box = fc.Internal("pocket surround", corners + corners[:1])
    return [opening, box]


def build_front():
    """Half front, cut 2 mirrored (never on fold): the center edge is the zip
    seam. Bound armscye (no sleeve). Horizontal quilt channels are traces on the
    shell; optional zip hand-warmer pocket markings."""
    zlen = HPS_Y - FRONT_NECK_DROP                 # straight zipper-seam length
    t_stop = ZIP_STOP_INSET / zlen
    internals = [
        fc.Internal(
            "zipper stitch line",
            [fc.P(ZIP_STITCH, ZIP_STOP_INSET), fc.P(ZIP_STITCH, zlen - ZIP_STOP_INSET)],
            kind="trace",
        )
    ]
    # Channels span from just off CF to just short of the side seam.
    internals += _quilt_channels(ZIP_SA + 5.0, W - 10.0, "front")
    if pockets:
        internals += _pocket_marks()
    return fc.Piece(
        "front",
        _body_edges(FRONT_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": ZIP_SA},
        notches=[
            fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "front armhole (bound)"),
            fc.Notch("center", 1.0 - t_stop, "zipper top stop"),
            fc.Notch("center", t_stop, "zipper bottom stop"),
        ],
        grainline=fc.Grainline(fc.P(W * 0.60, 70.0), fc.P(W * 0.60, L - 110.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (zip half, quilted)",
    )


def build_back():
    """Half back, cut 1 on fold at CF. Quilt channels are traces on the shell;
    bound armscye (no sleeve)."""
    internals = _quilt_channels(10.0, W - 10.0, "back")
    return fc.Piece(
        "back",
        _body_edges(BACK_NECK_DROP),
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", 0.5), fc.Notch("armhole", 0.5, "back armhole (bound)")],
        grainline=fc.Grainline(fc.P(W * 0.60, 70.0), fc.P(W * 0.60, L - 110.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back (quilted)",
    )


def _collar_neck_edge(bx):
    """Stand-collar bottom (neckline seam): a shallow curve from center back
    (x = bx) down to center front (x = 0). Its length is solved to the half neck
    opening by scaling bx (hood-neck attach-to-measured-curve method)."""
    return fc.Edge(
        "neckline",
        [fc.Bezier(fc.P(bx, 30.0), fc.P(bx * 0.58, -14.0),
                   fc.P(bx * 0.26, -14.0), fc.P(0.0, 0.0))],
    )


def build_collar(half_opening):
    """Stand / funnel collar, cut 1 on fold at center back. The neckline edge is
    SOLVED by bisection so it equals the half neck opening (one front half +
    the folded back half); the collar then rises `collar_height` to a funnel top.
    Cut on the fold at CB, the physical collar spans the full neck opening."""
    lo, hi = half_opening * 0.35, half_opening * 1.15
    for _ in range(52):
        bx = (lo + hi) / 2.0
        if _collar_neck_edge(bx).length(0.05) < half_opening:
            lo = bx
        else:
            hi = bx
    bx = (lo + hi) / 2.0
    if abs(_collar_neck_edge(bx).length(0.05) - half_opening) > 1.0:
        raise ValueError("collar neckline solver did not converge")
    ch = collar_height
    top_out = 12.0                                   # slight funnel flare at top
    neck = _collar_neck_edge(bx)
    edges = [
        neck,                                        # CB(top) → CF(bottom) neckline
        fc.Edge("front_edge", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, ch))]),  # CF (zips)
        fc.Edge(
            "top",
            [fc.curve_through(fc.P(0.0, ch), fc.P(bx + top_out, ch + 8.0),
                              bulge=0.05, side=-1.0)],
        ),
        fc.Edge("fold", [fc.Line(fc.P(bx + top_out, ch + 8.0), fc.P(bx, 30.0))]),  # CB fold
    ]
    return fc.Piece(
        "collar",
        edges,
        seam_allowance=seam_allowance,
        allowances={"front_edge": ZIP_SA, "top": seam_allowance},
        notches=[fc.Notch("neckline", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(bx * 0.5, 6.0), fc.P(bx * 0.5, ch)),
        internals=[fc.Internal("collar fold guide",
                               [fc.P(0.0, ch * 0.5), fc.P(bx, ch * 0.5)])],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="fold", mirror=True),
        label="Stand Collar (funnel)",
    )


def build():
    pattern = fc.PatternSet("puffer-vest")
    front = build_front()
    back = build_back()
    # Full neck opening: TWO front halves (cut 2) + the folded back's two halves.
    neck_opening = 2.0 * (front.edge("neck").length(0.05) + back.edge("neck").length(0.05))
    # The collar is cut 1 on fold, so ONE collar neckline covers HALF the opening.
    half_opening = neck_opening / 2.0

    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "collar":
        pattern.add(build_collar(half_opening))

    # ── Seams (all delta ≈ 0). Armhole + hem are BOUND finished edges, not seams;
    #    the CF zipper is a notion, not a fabric-to-fabric seam. ───────────────
    if (everything or target_piece == "front") and (everything or target_piece == "back") \
            and pattern.pieces and any(p.name == "back" for p in pattern.pieces):
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
    if everything:
        # Collar neckline sews to the full neckline: one folded collar (cut 1 on
        # fold) spans two front halves' necks + the folded back's two necks.
        pattern.declare_seam(
            [("collar", "neckline")],
            [("front", "neck"), ("back", "neck")],
            tol=2.0,
        )

    # ── BOM: shell + lining + fill (by area) + separating zipper + bindings ───
    fabric_width = 1450.0                            # nylon-ripstop-shell card width
    shell_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in (front, back, build_collar(half_opening))
    )
    shell_len = shell_area / (fabric_width * 0.62)   # 62% marker efficiency
    # Insulation is a garment-area component: shell body area × loft factor.
    body_area = (front.area() * 2.0 + back.area() * 2.0) / 1_000_000.0  # m²
    fill_area_m2 = round(body_area * 1.10, 2)        # +10% for channels/overlap
    # Separating zipper: CF opening = the straight center run + the hem casing.
    zip_total = front.edge("center").length() + hem_allowance
    zipper_len = int(round(zip_total / 10.0) * 10)
    # Bound armscyes: two fronts + the folded back = 4 armhole runs to bind.
    one_armhole_pair = front.edge("armhole").length() + back.edge("armhole").length()
    armscye_bind = int(round(2.0 * one_armhole_pair))  # 2 pairs = 4 armhole runs
    # Bound / elastic-cased hem: full hem circumference × draw ratio.
    hem_circ = 2.0 * (front.edge("hem").length() + back.edge("hem").length())
    hem_elastic_len = int(round(hem_circ * hem_elastic))
    pattern.bom = [
        {"item": "nylon-ripstop-shell", "qty": round(shell_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"outer shell, at {fabric_width:.0f} mm width, 62% marker "
                 f"efficiency; the loft-eased vest body + collar"},
        {"item": "lining (downproof / taffeta)", "qty": round(shell_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "inner face; shell + lining are quilted together over the fill "
                 "so the sew-through channels hold the loft"},
        {"item": "insulation fill (down or synthetic batt)", "qty": fill_area_m2,
         "unit": "m2",
         "note": f"~{loft_mm:.0f} mm loft between shell and lining across the body "
                 f"panels; quantity is body area +10% for channel overlap"},
        {"item": "separating zipper (closed-bottom molded)", "qty": zipper_len,
         "unit": "mm_length",
         "note": "full CF separating zipper; slider/pull hardware is a Yantra4D "
                 "cartridge (zipper-notion), never re-implemented here"},
        {"item": "bias binding / armhole tape", "qty": armscye_bind,
         "unit": "mm_length",
         "note": "binds the two sleeveless armscyes (no sleeve piece); a bound "
                 "or elastic-finished clean armhole edge"},
        {"item": "hem elastic + drawcord channel", "qty": hem_elastic_len,
         "unit": "mm_length",
         "note": f"elastic-cased / bound hem at {hem_elastic:.2f} draw; the hem is "
                 f"a finished edge, not a rib band"},
        {"item": "polyester thread + microtex needle 70/10", "qty": 1, "unit": "set",
         "note": "fine needle keeps holes small in the slippery ripstop; pin "
                 "inside the allowance"},
    ]
    pattern.metadata = {
        "fc100_rank": 64,
        "fabric_hint": "nylon-ripstop-shell",
        "silhouette": "roomy sleeveless insulated zip vest (puffer jacket minus "
                      "the sleeves)",
        "sleeveless": "armhole is a finished/BOUND edge — no sleeve piece "
                      "(waistcoat bound-armscye method)",
        "quilting": {
            "channel_spacing_mm": round(channel_spacing, 1),
            "loft_mm": round(loft_mm, 1),
            "note": "horizontal quilt channels are fc.Internal(kind='trace') "
                    "sew-through lines on the shell of front + back; the garment "
                    "is shell + lining quilted over the fill between them",
        },
        "collar": "stand / funnel, cut 1 on fold at CB; neckline edge solved by "
                  "bisection to the half neck opening",
        "collar_height_mm": round(collar_height, 1),
        "hem": f"bound / elastic-cased finished edge, {hem_elastic:.2f} draw "
               f"({hem_elastic_len} mm elastic)",
        "zipper_length_mm": zipper_len,
        "zipper_note": "order this separating zipper; hardware via zipper-notion "
                       "(Yantra4D)",
        "neck_opening_mm": round(neck_opening, 1),
        "armhole_front_mm": round(front.edge("armhole").length(), 1),
        "armhole_back_mm": round(back.edge("armhole").length(), 1),
        "hem_circumference_mm": round(hem_circ, 1),
        "insulation": "down or synthetic batt between shell and lining; a "
                      "purchased component (BOM), not modeled geometry",
        "pockets": "zip hand-warmer pockets are welt markings; pocket zips are "
                   "another zipper-notion reference" if pockets else "omitted",
        "drafting": "zip-hoodie / bomber-jacket body block halved at CF for the "
                    "separating zipper, sleeves removed (bound armscye), quilt "
                    "channels as traces, and a stand/funnel collar solved to the "
                    "neck opening; teaching-grade — the loft is BOM, the quilt "
                    "lines are markings, geometry stays a roomy vest",
    }
    return pattern


result = build()
