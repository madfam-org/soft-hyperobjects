"""
Cocktail dress — FC-100 rank #71 (Vestido de coctel).

The family's first WAIST-SEAMED occasion dress: a fitted knee-length sheath cut
in two horizontal stories — a princess-seamed bodice over a lightly flared
skirt, joined at a true waist seam. The bust is shaped the tailored way, by an
ARMHOLE PRINCESS SEAM that splits the front into a center-front panel (cut on
fold) and a side-front panel; the princess edge is authored ONCE and shared by
both panels (one reversed), so the seam matches to well under tol by
construction. The back is cut 2 with a CB seam carrying an INVISIBLE ZIPPER
notch and one fisheye waist dart per panel. The skirt front is cut on fold, the
skirt back cut 2 with its own CB seam continuing the zipper line; both stories
share the same waist quarter width, so the bodice waist (cf + side-front, or
the back panel) sews to the skirt waist at zero delta.

Two occasion options: a `neckline` select (strapless | straps) and a `boned`
checkbox. Strapless drafts the top edges straight and REQUIRES boning; a
strapped version adds shoulder straps and may skip it. When boned, spiral-steel
BONING CHANNELS are marked (kind="trace") down the princess and side seams of
the bodice. Fully lined (bodice + skirt): the lining mirrors the shell outlines
and is noted in the BOM (a lining note + BOM is the v0 finish — see
docs/README.md). Hardware (the invisible zip, the spiral-steel boning) is a
Yantra4D cartridge reference in the BOM, never re-implemented here.

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
# bodice_cf|bodice_sf|bodice_back|skirt_front|skirt_back|set

bust_girth     = float(PARAM(lambda: bust_girth, 900.0))
waist_girth    = float(PARAM(lambda: waist_girth, 720.0))
hip_girth      = float(PARAM(lambda: hip_girth, 980.0))
bodice_length  = float(PARAM(lambda: bodice_length, 400.0))   # nape/top edge to waist
skirt_length   = float(PARAM(lambda: skirt_length, 560.0))    # waist to knee hem
neckline       = str(PARAM(lambda: neckline, "strapless"))    # strapless | straps
boned          = bool(PARAM(lambda: boned, True))             # boning channels + steel
front_drop     = float(PARAM(lambda: front_drop, 70.0))       # CF top edge below bust line
skirt_flare    = float(PARAM(lambda: skirt_flare, 55.0))      # extra half-hem over hip qtr
zipper_length  = float(PARAM(lambda: zipper_length, 550.0))   # CB invisible zip, waist up + down
strap_width    = float(PARAM(lambda: strap_width, 40.0))      # strapped version only
waist_dart_intake = float(PARAM(lambda: waist_dart_intake, 22.0))  # back fisheye
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 40.0))

# ── Clamps (match manifest slider bounds) ────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1500.0))
waist_girth = max(550.0, min(waist_girth, 1300.0))
hip_girth = max(750.0, min(hip_girth, 1600.0))
bodice_length = max(300.0, min(bodice_length, 520.0))
skirt_length = max(400.0, min(skirt_length, 800.0))
front_drop = max(30.0, min(front_drop, 160.0))
skirt_flare = max(0.0, min(skirt_flare, 250.0))
strap_width = max(24.0, min(strap_width, 70.0))
waist_dart_intake = max(0.0, min(waist_dart_intake, 45.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))
if neckline not in ("strapless", "straps"):
    neckline = "strapless"
STRAPPED = neckline == "straps"
# A strapless bodice must be boned to stay up; force it on regardless of the box.
if not STRAPPED:
    boned = True

# ── Occasion-dress block: fitted sheath, princess front, waist seam ──────────
BODICE_EASE = 40.0      # close occasion-dress ease over the bust
WAIST_EASE = 20.0       # snug at the waist seam
HIP_EASE = 60.0         # skims the hip
BUST_Q = (bust_girth + BODICE_EASE) / 4.0      # bust quarter (bodice top width)
WAIST_Q = (waist_girth + WAIST_EASE) / 4.0     # waist quarter — SHARED bodice/skirt
HIP_Q = (hip_girth + HIP_EASE) / 4.0           # hip quarter (skirt widest)

# Bodice frame: waist line at y = 0, top (bust) line at y = bodice_length.
BODICE_TOP_Y = bodice_length
# Armhole princess line: the front split. Center-front panel spans [0, PR_X] at
# the waist; the side-front panel spans [PR_X, BUST_Q] up top. The princess x is
# a share of the bust quarter (classic ~1/2 of the front for an armhole
# princess).
PR_X = max(70.0, min(BUST_Q * 0.5, WAIST_Q - 40.0))   # princess x at both lines
# Underarm / side point at the bust line; the side seam runs down and IN to the
# waist side point at the (smaller) waist quarter — this bust-to-waist
# suppression is what makes the bodice waist edge equal the skirt waist quarter.
UNDERARM_X = BUST_Q
WAIST_SIDE_X = WAIST_Q
# Armhole scoop depth for the side-front panel top.
ARM_DEPTH = max(90.0, min((bust_girth + BODICE_EASE) / 12.0 + 55.0, 190.0))
CB_SA = 20.0            # CB seam allowance carries the invisible zipper
BONE_INSET = 3.0        # boning channel width marker half-offset from the seam

# Skirt frame: waist line at y = skirt_length, hem at y = 0 (drops DOWN).
SKIRT_WAIST_Y = skirt_length
HIP_DROP = max(150.0, min(200.0, skirt_length * 0.35))   # hip line below waist
SKIRT_HEM_Q = HIP_Q + skirt_flare                        # hem quarter half-width


# ── Boning-channel trace helper ──────────────────────────────────────────────
def _bone_channel(label, p_lo, p_hi):
    """A boning channel drawn as a narrow trace rectangle straddling a seam
    line from p_lo to p_hi. kind='trace' — a sewing guide, not a cut line."""
    axis = (p_hi - p_lo)
    if axis.length() < 1e-4:
        return None
    n = fc.Vec2(-axis.y, axis.x).normalized() * BONE_INSET
    return fc.Internal(
        label,
        [p_lo + n, p_hi + n, p_hi - n, p_lo - n, p_lo + n],
        kind="trace",
    )


# ── Front princess seam (authored ONCE, shared by both front panels) ─────────
def _princess_seam():
    """The armhole princess seam, waist -> bust line. A gentle bow gives the
    bust its 3D shape: bowed outward (toward the side) between waist and bust.
    Authored bottom->top; the center-front panel uses it reversed so its ring
    stays CCW, the side-front panel uses it as drawn. Same segment both sides =>
    the declared seam matches by construction."""
    bot = fc.P(PR_X, 0.0)
    top = fc.P(PR_X, BODICE_TOP_Y)
    return fc.Edge("princess", [fc.curve_through(bot, top, bulge=0.05, side=1.0)])


def _princess_len():
    return _princess_seam().length(0.05)


# ── Bodice center-front panel (cut on fold at CF) ────────────────────────────
def build_bodice_cf():
    """Center-front bodice panel, cut on fold at CF. Edges (CCW): cf fold up,
    neck across the top to the princess top, princess down to the waist, waist
    back to CF. Strapless => straight top at front_drop; strapped keeps the same
    top (straps land on the side-front panel shoulder)."""
    top_y = BODICE_TOP_Y - front_drop
    pr_top = fc.P(PR_X, BODICE_TOP_Y)
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
        # Sweetheart-ish top: a gentle rise from CF up to the princess top.
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, top_y), pr_top,
                                          bulge=0.08, side=1.0)]),
        _princess_seam().reversed(),                 # top -> waist (CCW continues)
        fc.Edge("waist", [fc.Line(fc.P(PR_X, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if boned:
        ch = _bone_channel("boning channel CF princess",
                           fc.P(PR_X, 8.0), fc.P(PR_X, BODICE_TOP_Y - 8.0))
        if ch is not None:
            internals.append(ch)
    return fc.Piece(
        "bodice_cf", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 1.0, "CF waist match")],
        grainline=fc.Grainline(fc.P(PR_X * 0.4, 40.0),
                               fc.P(PR_X * 0.4, BODICE_TOP_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Bodice Center Front",
    )


# ── Bodice side-front panel (cut 2 mirror) ───────────────────────────────────
def build_bodice_sf():
    """Side-front bodice panel, cut 2 mirror. Edges (CCW): princess up from the
    waist (matches CF princess), armhole scoop across the top to the underarm,
    side seam down to the waist, waist back to the princess. A shoulder strap
    stub is added on top for the strapped neckline."""
    pr_bot = fc.P(PR_X, 0.0)
    pr_top = fc.P(PR_X, BODICE_TOP_Y)
    underarm = fc.P(UNDERARM_X, BODICE_TOP_Y - 8.0)
    if STRAPPED:
        # Strap lands at the top of the armhole; the armhole scoops from the
        # strap end down to the underarm. Top edge = princess top -> strap end.
        strap_end = fc.P(PR_X + strap_width, BODICE_TOP_Y)
        top_edges = [
            fc.Edge("neck", [fc.Line(pr_top, strap_end)]),
            fc.Edge("armhole",
                    [fc.curve_through(strap_end, underarm, bulge=0.14, side=-1.0)]),
        ]
    else:
        # Strapless: a straight-ish top from princess top out to the underarm.
        top_edges = [
            fc.Edge("armhole",
                    [fc.curve_through(pr_top, underarm, bulge=0.06, side=-1.0)]),
        ]
    waist_side = fc.P(WAIST_SIDE_X, 0.0)
    edges = [_princess_seam()] + top_edges + [
        # side seam: underarm (bust width) down and IN to the waist side point
        fc.Edge("side", [fc.curve_through(underarm, waist_side,
                                          bulge=0.03, side=1.0)]),
        fc.Edge("waist", [fc.Line(waist_side, pr_bot)]),
    ]
    internals = []
    if boned:
        c1 = _bone_channel("boning channel SF princess",
                           fc.P(PR_X, 8.0), fc.P(PR_X, BODICE_TOP_Y - 8.0))
        # channel just inboard of the shaped side seam
        c2 = _bone_channel("boning channel side seam",
                           fc.P(WAIST_SIDE_X - BONE_INSET, 8.0),
                           fc.P(UNDERARM_X - BONE_INSET, BODICE_TOP_Y - 14.0))
        internals += [c for c in (c1, c2) if c is not None]
    return fc.Piece(
        "bodice_sf", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.0, "SF waist match"),
                 fc.Notch("princess", 0.5, "bust match")],
        grainline=fc.Grainline(fc.P((PR_X + UNDERARM_X) * 0.5, 40.0),
                               fc.P((PR_X + UNDERARM_X) * 0.5, BODICE_TOP_Y - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice Side Front",
    )


# ── Bodice back panel (cut 2, CB seam carries the zipper) ────────────────────
def build_bodice_back():
    """Back bodice panel, cut 2 with a CB seam (allowance 20) carrying the
    invisible zipper. Edges (CCW): center (CB) up, back neck across to the
    shoulder/underarm, side seam down to the waist, waist back to CB. One
    fisheye waist dart per panel shapes the back; the mirrored cut-2 gives the
    classic pair. The back spans [0, WAIST_Q] at the waist — the whole back
    quarter is one panel."""
    top_y = BODICE_TOP_Y - (front_drop * 0.35)   # back sits a touch higher than front
    underarm = fc.P(UNDERARM_X, BODICE_TOP_Y - 8.0)
    if STRAPPED:
        strap_in = fc.P(WAIST_Q * 0.45, BODICE_TOP_Y)
        strap_end = fc.P(WAIST_Q * 0.45 + strap_width, BODICE_TOP_Y)
        top_edges = [
            fc.Edge("neck", [fc.Line(fc.P(0.0, top_y), strap_in)]),
            fc.Edge("strap_top", [fc.Line(strap_in, strap_end)]),
            fc.Edge("armhole",
                    [fc.curve_through(strap_end, underarm, bulge=0.12, side=-1.0)]),
        ]
    else:
        top_edges = [
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, top_y),
                                              fc.P(WAIST_Q * 0.6, BODICE_TOP_Y),
                                              bulge=0.04, side=1.0)]),
            fc.Edge("armhole",
                    [fc.curve_through(fc.P(WAIST_Q * 0.6, BODICE_TOP_Y), underarm,
                                      bulge=0.10, side=-1.0)]),
        ]
    waist_side = fc.P(WAIST_SIDE_X, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, top_y))]),
    ] + top_edges + [
        # side seam: same endpoints + bulge magnitude as the side-front side
        # seam, so the bodice side seam matches by construction (side sign only
        # flips the bow direction, not the length).
        fc.Edge("side", [fc.curve_through(underarm, waist_side,
                                          bulge=0.03, side=-1.0)]),
        fc.Edge("waist", [fc.Line(waist_side, fc.P(0.0, 0.0))]),
    ]
    internals = []
    # Fisheye waist dart per panel: a closed lens, widest near the waist,
    # tapering up toward the shoulder-blade level. Kept inside the panel width.
    if waist_dart_intake > 0.5:
        cx = max(60.0, min(WAIST_Q * 0.5, UNDERARM_X - 40.0))
        y_bot = 20.0
        y_top = min(BODICE_TOP_Y - 30.0, y_bot + BODICE_TOP_Y * 0.72)
        mid = (y_bot + y_top) / 2.0
        half = waist_dart_intake / 2.0
        internals.append(fc.Internal(
            "back fisheye dart",
            [fc.P(cx, y_bot), fc.P(cx - half, mid), fc.P(cx, y_top),
             fc.P(cx + half, mid), fc.P(cx, y_bot)],
            kind="dart",
        ))
    if boned:
        c1 = _bone_channel("boning channel back CB",
                           fc.P(6.0, 8.0), fc.P(6.0, top_y - 8.0))
        c2 = _bone_channel("boning channel back side",
                           fc.P(WAIST_SIDE_X - BONE_INSET, 8.0),
                           fc.P(UNDERARM_X - BONE_INSET, BODICE_TOP_Y - 14.0))
        internals += [c for c in (c1, c2) if c is not None]
    cb_len = top_y
    return fc.Piece(
        "bodice_back", edges,
        seam_allowance=seam_allowance,
        allowances={"center": CB_SA},               # CB carries the invisible zip
        notches=[
            fc.Notch("waist", 0.0, "back waist match"),
            # Invisible zip runs from the top edge DOWN across the waist seam.
            # `center` is authored waist->top, so the bodice portion of the zip
            # spans the whole CB here; the stop notch is placed on the SKIRT CB.
            fc.Notch("center", 1.0, "zipper top"),
        ],
        grainline=fc.Grainline(fc.P(UNDERARM_X * 0.5, 40.0),
                               fc.P(UNDERARM_X * 0.5, cb_len - 40.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice Back",
    )


# ── Skirt front (cut on fold at CF) ──────────────────────────────────────────
def build_skirt_front():
    """Skirt front, cut on fold at CF. Edges (CCW): cf fold down from waist to
    hem, hem across to the side hem, side seam up from the hem through the hip
    to the waist, waist back to CF. The waist spans [0, WAIST_Q] — SAME quarter
    as the bodice front, so the waist seam matches at zero delta. The side seam
    eases waist -> hip -> flared hem."""
    waist_pt = fc.P(WAIST_Q, SKIRT_WAIST_Y)
    hip_pt = fc.P(HIP_Q, SKIRT_WAIST_Y - HIP_DROP)
    hem_pt = fc.P(SKIRT_HEM_Q, 0.0)
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, SKIRT_WAIST_Y), fc.P(0.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), hem_pt)]),
        # side seam: hem -> hip -> waist (bows through the hip, straight to hem)
        fc.Edge("side", [
            fc.Bezier(hem_pt, fc.P(SKIRT_HEM_Q, HIP_DROP * 0.6),
                      fc.P(HIP_Q, hip_pt.y - HIP_DROP * 0.15), hip_pt),
            fc.Bezier(hip_pt, fc.P(HIP_Q, hip_pt.y + HIP_DROP * 0.5),
                      fc.P(WAIST_Q, SKIRT_WAIST_Y - HIP_DROP * 0.45), waist_pt),
        ]),
        fc.Edge("waist", [fc.Line(waist_pt, fc.P(0.0, SKIRT_WAIST_Y))]),
    ]
    return fc.Piece(
        "skirt_front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "CF waist match"),
                 fc.Notch("side", 0.5, "hip match")],
        grainline=fc.Grainline(fc.P(WAIST_Q * 0.4, 60.0),
                               fc.P(WAIST_Q * 0.4, SKIRT_WAIST_Y - 60.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf", mirror=True),
        label="Skirt Front",
    )


# ── Skirt back (cut 2, CB seam continues the zipper) ─────────────────────────
def build_skirt_back():
    """Skirt back, cut 2 with a CB seam (allowance 20) continuing the invisible
    zipper down from the bodice. Edges (CCW): center (CB) down from waist to
    hem, hem across to the side hem, side seam up through the hip to the waist,
    waist back to CB. Waist spans [0, WAIST_Q] = the bodice-back waist quarter,
    so the waist seam matches at zero delta. Same side-seam construction as the
    front, so the skirt side seams match."""
    waist_pt = fc.P(WAIST_Q, SKIRT_WAIST_Y)
    hip_pt = fc.P(HIP_Q, SKIRT_WAIST_Y - HIP_DROP)
    hem_pt = fc.P(SKIRT_HEM_Q, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, SKIRT_WAIST_Y), fc.P(0.0, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), hem_pt)]),
        fc.Edge("side", [
            fc.Bezier(hem_pt, fc.P(SKIRT_HEM_Q, HIP_DROP * 0.6),
                      fc.P(HIP_Q, hip_pt.y - HIP_DROP * 0.15), hip_pt),
            fc.Bezier(hip_pt, fc.P(HIP_Q, hip_pt.y + HIP_DROP * 0.5),
                      fc.P(WAIST_Q, SKIRT_WAIST_Y - HIP_DROP * 0.45), waist_pt),
        ]),
        fc.Edge("waist", [fc.Line(waist_pt, fc.P(0.0, SKIRT_WAIST_Y))]),
    ]
    # Zipper stop: the invisible zip runs from the bodice top down the CB and
    # ends `zipper_length` below the bodice top. bodice_length above the skirt
    # waist is already zipped; the remaining run into the skirt is
    # zipper_length - bodice_length, measured from the skirt waist DOWN. `center`
    # is authored waist->hem, so the stop sits at authored fraction
    # (zip into skirt) / skirt_length.
    zip_into_skirt = max(0.0, min(zipper_length - bodice_length, skirt_length - 20.0))
    stop_t = zip_into_skirt / SKIRT_WAIST_Y
    return fc.Piece(
        "skirt_back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": CB_SA},
        notches=[fc.Notch("waist", 1.0, "back waist match"),
                 fc.Notch("side", 0.5, "hip match"),
                 fc.Notch("center", stop_t, "zipper stop")],
        grainline=fc.Grainline(fc.P(WAIST_Q * 0.4, 60.0),
                               fc.P(WAIST_Q * 0.4, SKIRT_WAIST_Y - 60.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Skirt Back",
    )


def build():
    pattern = fc.PatternSet("cocktail-dress")
    names = ("bodice_cf", "bodice_sf", "bodice_back", "skirt_front", "skirt_back")
    wanted = {name: target_piece in (name, "set") for name in names}
    if not any(wanted.values()):
        wanted = {k: True for k in wanted}

    pieces = {}
    if wanted["bodice_cf"]:
        pieces["bodice_cf"] = pattern.add(build_bodice_cf())
    if wanted["bodice_sf"]:
        pieces["bodice_sf"] = pattern.add(build_bodice_sf())
    if wanted["bodice_back"]:
        pieces["bodice_back"] = pattern.add(build_bodice_back())
    if wanted["skirt_front"]:
        pieces["skirt_front"] = pattern.add(build_skirt_front())
    if wanted["skirt_back"]:
        pieces["skirt_back"] = pattern.add(build_skirt_back())

    # ── Declared seams (every sewn relationship) ─────────────────────────────
    # 1. Front princess: CF panel princess ↔ side-front panel princess.
    if wanted["bodice_cf"] and wanted["bodice_sf"]:
        pattern.declare_seam(("bodice_cf", "princess"),
                             ("bodice_sf", "princess"), tol=1.5)
    # 2. Bodice side seam: side-front ↔ back.
    if wanted["bodice_sf"] and wanted["bodice_back"]:
        pattern.declare_seam(("bodice_sf", "side"),
                             ("bodice_back", "side"), tol=1.5)
    # 3. Strapped: shoulder strap on side-front meets the back strap. The strap
    #    is the side-front "neck" edge (princess top -> strap end); it sews to
    #    the back "strap_top". Both are strap_width straight lines => equal.
    if STRAPPED and wanted["bodice_sf"] and wanted["bodice_back"]:
        pattern.declare_seam(("bodice_sf", "neck"),
                             ("bodice_back", "strap_top"), tol=1.0)
    # 4. Waist seam FRONT: (bodice_cf.waist + bodice_sf.waist) ↔ skirt_front.waist.
    #    Both partitions of [0, WAIST_Q] at the same princess x => delta ≈ 0.
    if wanted["bodice_cf"] and wanted["bodice_sf"] and wanted["skirt_front"]:
        pattern.declare_seam([("bodice_cf", "waist"), ("bodice_sf", "waist")],
                             [("skirt_front", "waist")], tol=1.5)
    # 5. Waist seam BACK: bodice_back.waist ↔ skirt_back.waist. Both [0, WAIST_Q].
    if wanted["bodice_back"] and wanted["skirt_back"]:
        pattern.declare_seam(("bodice_back", "waist"),
                             ("skirt_back", "waist"), tol=1.5)
    # 6. Skirt side seam: front ↔ back (shared construction => equal).
    if wanted["skirt_front"] and wanted["skirt_back"]:
        pattern.declare_seam(("skirt_front", "side"),
                             ("skirt_back", "side"), tol=1.5)

    # ── BOM ──────────────────────────────────────────────────────────────────
    fabric_width = 1450.0                            # popelina-algodon card width
    shell_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces
    )
    shell_marker = shell_area / (fabric_width * 0.62)
    bom = [
        {"item": "popelina-algodon (shell)",
         "qty": round(shell_marker / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker efficiency; a real "
                 f"cocktail dress is often crepe/satin/taffeta — poplin is the "
                 f"teaching-grade stand-in"},
        {"item": "lining (bodice + skirt, full)",
         "qty": round(shell_marker / 10.0) * 10, "unit": "mm_length",
         "note": "acetate/bemberg; lining mirrors every shell outline "
                 "(cut from the same pieces) — noted, not drafted as separate "
                 "geometry in v0 (see docs/README.md)"},
        {"item": "invisible zipper 55 cm",
         "qty": 1, "unit": "pcs",
         "note": "center-back invisible zip, bodice top down through the skirt CB; "
                 "hardware is a Yantra4D cartridge (zipper-notion, invisible "
                 "subtype), never re-implemented here"},
        {"item": "fusible interfacing (bodice top edge + zip tape)",
         "qty": 1, "unit": "set",
         "note": "stay the strapless top edge and the CB zip line"},
        {"item": "polyester thread + microtex needle 70/10",
         "qty": 1, "unit": "set",
         "note": "microtex for clean seams on fine occasion fabric"},
    ]
    if boned:
        bom.append(
            {"item": "spiral-steel boning 7 mm + channel tape",
             "qty": 6, "unit": "pcs",
             "note": "spiral steel in channels down the CF princess, both SF "
                     "princess/side, and both back CB/side seams; hardware is a "
                     "Yantra4D cartridge (boning-notion, spiral-steel subtype), "
                     "never re-implemented here"})
    pattern.bom = bom

    # ── Metadata (every solved dimension + honest teaching-grade note) ───────
    princess_len = _princess_len()
    bodice_front_waist = (WAIST_Q if not wanted["bodice_cf"] else
                          pieces["bodice_cf"].edge("waist").length()
                          + pieces["bodice_sf"].edge("waist").length()) \
        if wanted["bodice_cf"] and wanted["bodice_sf"] else round(WAIST_Q, 1)
    zip_into_skirt = max(0.0, min(zipper_length - bodice_length, skirt_length - 20.0))
    pattern.metadata = {
        "fc100_rank": 71,
        "fabric_hint": "popelina-algodon",
        "neckline": neckline,
        "boned": boned,
        "lined": True,
        "bust_quarter_mm": round(BUST_Q, 1),
        "waist_quarter_mm": round(WAIST_Q, 1),
        "hip_quarter_mm": round(HIP_Q, 1),
        "princess_x_mm": round(PR_X, 1),
        "princess_seam_len_mm": round(princess_len, 1),
        "bodice_front_waist_mm": round(bodice_front_waist, 1)
        if isinstance(bodice_front_waist, float) else bodice_front_waist,
        "skirt_hem_quarter_mm": round(SKIRT_HEM_Q, 1),
        "zipper_into_skirt_mm": round(zip_into_skirt, 1),
        "waist_join": "bodice waist (cf+side-front, and back) and skirt waist share "
                      "the same waist quarter; both edges are straight horizontals of "
                      "equal length, so the waist seam solves at delta ~ 0 by "
                      "construction",
        "drafting": "fitted knee-length sheath in two stories: an armhole-princess "
                    "bodice (center-front on fold + side-front panels, princess "
                    "authored once and shared) over a hip-shaped lightly flared "
                    "skirt, joined at a true waist seam; CB invisible zipper across "
                    "both stories; back fisheye waist darts; strapless is boned; "
                    "fully lined (noted in BOM, not drafted as separate geometry)",
    }
    return pattern


result = build()
