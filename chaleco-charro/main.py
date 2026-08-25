"""
Chaleco Charro — Fashion Cabinet Heritage Cartridge (FC-300 #300, long-tail band).

The waistcoat of the traje de charro: the Mexican horseman's suit, and the last entry
in the FC-300 catalog. Short, close, cut in worsted wool to sit ABOVE the trouser
waistband, with peaked lapels and a hook-and-bar front that closes edge to edge without
a button stand.

It is not an English suit waistcoat with different trim, and the differences are
structural, not decorative:

  - THE LENGTH IS SET BY THE TROUSER, NOT BY THE TORSO. The charro trouser rides high
    and is held by a wide waistband; the chaleco must finish ABOVE it, because a
    waistcoat that laps over the trouser waistband breaks the long unbroken line from
    shoulder to boot that the whole suit is built around. So `waist_rise` — where the
    trouser waistband sits — is a real parameter here, and the waistcoat length is
    SOLVED from it rather than from a nape measurement.
  - THE FRONT CLOSES EDGE TO EDGE. There is no button stand and no overlap: the two
    fronts meet at centre front and are held by hook-and-bar sets sewn behind the edge
    (Yantra4D `trouser-hook-bar`). That means the front edge is drafted AT centre front,
    not a stand's width beyond it — the error that makes a copied waistcoat gape.
  - THE HEM IS STRAIGHT OR SHALLOWLY SHAPED, NOT POINTED. The English waistcoat's
    signature point at centre front belongs to that garment; it is not this one.
  - THERE IS NO CINCH BELT. The back is cut in the suiting, shaped at the centre-back
    seam, and it is part of the suit's face — not a lining-weight back hidden by a coat.

Drafting note — the seam that must SOLVE, and the number that has to be honest:

  An edge-to-edge front has no overlap to absorb error. Every millimetre of shaping is
  visible as a gap or a strain at the closure line, so the front's own vertical circuit
  must be exact. The kernel therefore drafts the front's centre edge, MEASURES it, and
  cuts the facing to that measurement — and the hooks are spaced along the MEASURED
  edge, recomputed to whole intervals so the first and last sit clear of the lapel break
  and the hem rather than drifting off the last one.

  The closure count itself is derived, not chosen: from the measured closure run and a
  comfortable pitch. A charro chaleco with hooks bunched at the hem is a chaleco that
  was drafted by dividing a guessed length.

Pieces:
  - front  : the front (cut 2 mirrored), peaked lapel, edge-to-edge closure, welts.
  - back   : the back (cut 2 mirrored), shaped centre-back seam, in the suiting.
  - facing : the front facing, cut to the MEASURED front edge run.
  - lapel  : the under-collar / lapel facing, cut to the MEASURED lapel run.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|facing|lapel|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))
waist_girth = float(PARAM(lambda: waist_girth, 880.0))
nape_to_waist = float(PARAM(lambda: nape_to_waist, 445.0))   # nape to natural waist
waist_rise = float(PARAM(lambda: waist_rise, 40.0))          # trouser band above waist
shoulder_width = float(PARAM(lambda: shoulder_width, 450.0))
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
chest_ease = float(PARAM(lambda: chest_ease, 70.0))          # close — it is tailoring
lapel_break = float(PARAM(lambda: lapel_break, 0.42))        # fraction down the front
lapel_width = float(PARAM(lambda: lapel_width, 72.0))        # at the widest point
hook_pitch = float(PARAM(lambda: hook_pitch, 78.0))          # requested hook spacing
hook_width = float(PARAM(lambda: hook_width, 16.0))          # the hook-and-bar's span
soutache_rows = int(PARAM(lambda: soutache_rows, 2))         # greca rows along the edge
soutache_inset = float(PARAM(lambda: soutache_inset, 7.0))   # first row from the edge
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(800.0, min(chest_girth, 1350.0))
waist_girth = max(650.0, min(waist_girth, 1300.0))
nape_to_waist = max(360.0, min(nape_to_waist, 540.0))
waist_rise = max(0.0, min(waist_rise, 110.0))
shoulder_width = max(360.0, min(shoulder_width, 540.0))
neck_girth = max(330.0, min(neck_girth, 500.0))
chest_ease = max(30.0, min(chest_ease, 160.0))
lapel_break = max(0.22, min(lapel_break, 0.62))
lapel_width = max(35.0, min(lapel_width, 130.0))
hook_pitch = max(45.0, min(hook_pitch, 150.0))
hook_width = max(9.0, min(hook_width, 30.0))
soutache_rows = max(0, min(soutache_rows, 4))
soutache_inset = max(3.0, min(soutache_inset, 25.0))
seam_allowance = max(8.0, min(seam_allowance, 18.0))

# A waist is not larger than a chest on a tailored waistcoat's block. Entered the other
# way round the side seam would flare outward from the armhole and the shaping would
# invert — a piece whose edges cross, which the kernel CCW-normalizes into geometry that
# verifies and cannot be made.
waist_girth = min(waist_girth, chest_girth - 20.0)

HALF_CHEST = (chest_girth + chest_ease) / 4.0
HALF_WAIST = (waist_girth + chest_ease * 0.72) / 4.0

# ── The length solve — the trouser sets it, not the torso ────────────────────
# The chaleco finishes ABOVE the trouser waistband. `waist_rise` is how far the band
# sits above the natural waist, so the waistcoat's own length is the nape-to-waist run
# LESS that rise, less a clearance so the two never meet.
CLEARANCE = 12.0
LENGTH_RAW = nape_to_waist - waist_rise - CLEARANCE
# At the extremes (a 360 mm nape-to-waist under a 110 mm rise) this goes to 238 mm and
# keeps falling; below the armhole depth there is no waistcoat left, only an armhole.
# The floor is the armhole plus a real body run, and it is reported when it fires.
ARMHOLE_DEPTH = HALF_CHEST * 0.86 + 24.0
LENGTH_FLOOR = ARMHOLE_DEPTH + 70.0
LENGTH = max(LENGTH_RAW, LENGTH_FLOOR)
LENGTH_FLOORED = LENGTH > LENGTH_RAW + 1e-9

# The neckline: a charro chaleco sits high, so the front neck drop is shallow and the
# lapel breaks well up the chest.
NECK_W = neck_girth / 6.0 + 12.0
NECK_DROP_B = 20.0
SHOULDER_SLOPE = 44.0
HALF_SHOULDER = shoulder_width / 2.0
# The shoulder must reach outward from the neck; a very wide neck on a narrow shoulder
# would invert it.
NECK_W = min(NECK_W, HALF_SHOULDER - 40.0)

# The break point: where the lapel stops rolling and the closure begins.
BREAK_Y = LENGTH * (1.0 - lapel_break)
# The closure run: from the break down to a clearance above the hem.
HEM_CLEAR = 42.0
CLOSURE_RUN = max(BREAK_Y - HEM_CLEAR, 40.0)

# ── The hook column, solved ──────────────────────────────────────────────────
# Whole intervals across the measured closure run, then the pitch RECOMPUTED so the
# column lands exactly on both clearances instead of drifting off the last hook.
#
# The rounding goes UP, not to-nearest. On a short closure run there are only two or
# three intervals, and rounding to-nearest can push the solved pitch well ABOVE the
# request (93 mm for a requested 78) — a chaleco with visibly sparse hooks. Rounding up
# tightens the pitch instead, which is the direction that keeps an edge-to-edge front
# closed.
N_INTERVALS = max(1, math.ceil(CLOSURE_RUN / hook_pitch - 1e-9))
N_HOOKS = N_INTERVALS + 1
PITCH_SOLVED = CLOSURE_RUN / N_INTERVALS

# The lapel's widest point cannot exceed the front's own half-width, or the peak runs
# off the piece it is cut from — a 130 mm lapel on an 800 mm chest does exactly that,
# and the resulting outline crosses itself into geometry that verifies and cannot be
# made. The requested value is kept so the cap can be reported rather than hidden.
LAPEL_WIDTH_REQUESTED = lapel_width
lapel_width = min(lapel_width, HALF_CHEST * 0.55)
LAPEL_WIDTH_CAPPED = lapel_width < LAPEL_WIDTH_REQUESTED - 1e-9


def _hook_ys():
    """y of every hook centre, top-down from the break."""
    return [BREAK_Y - PITCH_SOLVED * i for i in range(N_HOOKS)]


def build_front():
    """The front (cut 2 mirrored): peaked lapel, EDGE-TO-EDGE closure at centre front,
    two lower welts and a breast welt.

    x = 0 IS centre front. There is no button stand: the front edge is drafted at
    centre front, which is the whole difference between a chaleco charro that closes
    and a copied waistcoat that gapes."""
    p_hem_cf = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_WAIST, 0.0)
    p_side_top = fc.P(HALF_CHEST, LENGTH - ARMHOLE_DEPTH)
    p_shoulder_out = fc.P(HALF_SHOULDER, LENGTH - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W, LENGTH)
    # The peaked lapel: up from the break, out to the peak, back in to the neck point.
    p_break = fc.P(0.0, BREAK_Y)
    p_peak = fc.P(lapel_width, BREAK_Y + (LENGTH - BREAK_Y) * 0.72)
    p_lapel_neck = fc.P(NECK_W * 0.55, LENGTH - 6.0)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cf, p_hem_side)]),
        # The side seam carries the waist shaping: chest at the armhole, waist at hem.
        fc.Edge("side", [fc.Bezier(p_hem_side,
                                   fc.P(HALF_WAIST + (HALF_CHEST - HALF_WAIST) * 0.30,
                                        (LENGTH - ARMHOLE_DEPTH) * 0.42),
                                   fc.P(HALF_CHEST - 3.0,
                                        (LENGTH - ARMHOLE_DEPTH) * 0.80),
                                   p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 8.0,
                                           LENGTH - ARMHOLE_DEPTH * 0.44),
                                      fc.P(HALF_SHOULDER + 6.0,
                                           LENGTH - SHOULDER_SLOPE - 44.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        # The lapel run: neck point, in along the gorge, out to the peak, down to break.
        fc.Edge("lapel", [fc.Line(p_neck_shoulder, p_lapel_neck),
                          fc.Line(p_lapel_neck, p_peak),
                          fc.Bezier(p_peak,
                                    fc.P(lapel_width * 0.52,
                                         BREAK_Y + (LENGTH - BREAK_Y) * 0.34),
                                    fc.P(lapel_width * 0.16,
                                         BREAK_Y + (LENGTH - BREAK_Y) * 0.12),
                                    p_break)]),
        # THE edge: centre front, from the break to the hem. No stand.
        fc.Edge("centre_front", [fc.Line(p_break, p_hem_cf)]),
    ]

    internals = []
    # The hook-and-bar column, on the MEASURED closure run at the solved pitch.
    for i, y in enumerate(_hook_ys()):
        internals.append(fc.Internal(
            f"hook-{i + 1}",
            [fc.P(2.0, y), fc.P(2.0 + hook_width, y)], kind="drill"))
    # The greca: soutache rows following the front edge and the lapel. MARKED as
    # placement lines only — the braid pattern itself is the maker's and the region's,
    # and this cartridge does not invent one.
    for r in range(soutache_rows):
        off = soutache_inset + r * (soutache_inset * 0.85)
        internals.append(fc.Internal(
            f"greca-row-{r + 1}",
            [fc.P(off, 6.0), fc.P(off, BREAK_Y - 4.0),
             fc.P(min(lapel_width - off, HALF_CHEST * 0.5),
                  BREAK_Y + (LENGTH - BREAK_Y) * 0.62)], kind="marking"))
    # Welts: two lower, one breast. Marked, not drafted as separate pieces.
    wl_w, wl_h = min(HALF_CHEST * 0.52, 118.0), 16.0
    wl_x = max(HALF_CHEST * 0.22, lapel_width * 0.5)
    for label, wy, ww in (("welt-lower", LENGTH * 0.30, wl_w),
                          ("welt-breast", LENGTH - ARMHOLE_DEPTH * 0.30, wl_w * 0.62)):
        internals.append(fc.Internal(
            label,
            [fc.P(wl_x, wy), fc.P(wl_x + ww, wy),
             fc.P(wl_x + ww, wy + wl_h), fc.P(wl_x, wy + wl_h),
             fc.P(wl_x, wy)], kind="marking"))
    # The trouser-band clearance line: the chaleco must finish ABOVE this.
    internals.append(fc.Internal(
        "trouser-band-clearance",
        [fc.P(0.0, -CLEARANCE), fc.P(HALF_WAIST, -CLEARANCE)], kind="marking"))

    return fc.Piece(
        "front", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 18.0},
        notches=[fc.Notch("centre_front", 0.0, "lapel break"),
                 fc.Notch("armhole", 0.55, "balance mark"),
                 fc.Notch("side", 0.55, "waist level")],
        grainline=fc.Grainline(fc.P(lapel_width * 0.8, 30.0),
                               fc.P(lapel_width * 0.8, LENGTH - ARMHOLE_DEPTH - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (peaked lapel, edge-to-edge)",
    )


def build_back():
    """The back (cut 2 mirrored, joined at centre back): shaped at the CB seam, cut in
    the SUITING — it is part of the suit's face, not a lining-weight back under a coat.

    The back neck width is solved from the front's measured shoulder, so the seam
    matches by construction; and the clamp lands on the drawn rise, not on a local
    solve variable, so the piece cannot be drafted at a rise the solve never agreed to.
    """
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(HALF_WAIST, 0.0)
    p_side_top = fc.P(HALF_CHEST, LENGTH - ARMHOLE_DEPTH)
    p_shoulder_out = fc.P(HALF_SHOULDER, LENGTH - SHOULDER_SLOPE)
    p_neck_shoulder = fc.P(NECK_W_BACK, LENGTH + BACK_NECK_Y)
    p_neck_cb = fc.P(0.0, LENGTH + BACK_NECK_Y + NECK_DROP_B * 0.3)

    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Bezier(p_hem_side,
                                   fc.P(HALF_WAIST + (HALF_CHEST - HALF_WAIST) * 0.30,
                                        (LENGTH - ARMHOLE_DEPTH) * 0.42),
                                   fc.P(HALF_CHEST - 3.0,
                                        (LENGTH - ARMHOLE_DEPTH) * 0.80),
                                   p_side_top)]),
        fc.Edge("armhole", [fc.Bezier(p_side_top,
                                      fc.P(HALF_CHEST - 6.0,
                                           LENGTH - ARMHOLE_DEPTH * 0.46),
                                      fc.P(HALF_SHOULDER + 5.0,
                                           LENGTH - SHOULDER_SLOPE - 40.0),
                                      p_shoulder_out)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_out, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_W_BACK * 0.58, p_neck_shoulder.y + 2.0),
                                   fc.P(NECK_W_BACK * 0.24, p_neck_cb.y),
                                   p_neck_cb)]),
        # The centre-back seam carries the back's waist shaping.
        fc.Edge("cb", [fc.Bezier(p_neck_cb,
                                 fc.P(-3.0, LENGTH * 0.62),
                                 fc.P(-5.0, LENGTH * 0.28),
                                 p_hem_cb)]),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 18.0},
        notches=[fc.Notch("armhole", 0.55, "balance mark"),
                 fc.Notch("side", 0.55, "waist level")],
        grainline=fc.Grainline(fc.P(HALF_WAIST * 0.45, 30.0),
                               fc.P(HALF_WAIST * 0.45, LENGTH - ARMHOLE_DEPTH - 30.0)),
        internals=[fc.Internal("trouser-band-clearance",
                               [fc.P(0.0, -CLEARANCE), fc.P(HALF_WAIST, -CLEARANCE)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (shaped CB seam, in the suiting)",
    )


# ── The back neck solved from the MEASURED front shoulder ────────────────────
# The front's shoulder runs from (HALF_SHOULDER, LENGTH - SHOULDER_SLOPE) to
# (NECK_W, LENGTH). The back shares the outer point but its neck point sits higher, so
# a back neck at NECK_W would give a LONGER shoulder. Solve the back neck WIDTH from
# the front's measured shoulder instead.
#
# The rise is the vertical leg of a right triangle whose hypotenuse is that shoulder. A
# narrow shoulder with a deep neck makes the rise EXCEED the shoulder length, and there
# is no horizontal run left. Clamping only a local solve variable while drawing the
# piece at the unclamped rise gives a drafted back shoulder that measures something the
# solve never agreed to — so the clamp lands on BACK_NECK_Y itself, and every use
# (solve and draw alike) reads that one value.
_SHOULDER_LEN = math.hypot(HALF_SHOULDER - NECK_W, SHOULDER_SLOPE)
_BACK_RISE_WANTED = NECK_DROP_B * 0.9
_dy = SHOULDER_SLOPE + _BACK_RISE_WANTED
if _dy >= _SHOULDER_LEN * 0.94:
    _dy = _SHOULDER_LEN * 0.94
BACK_NECK_Y = _dy - SHOULDER_SLOPE
BACK_NECK_CLAMPED = BACK_NECK_Y < _BACK_RISE_WANTED - 1e-9
NECK_W_BACK = HALF_SHOULDER - math.sqrt(max(_SHOULDER_LEN ** 2 - _dy ** 2, 1.0))

# ── The measured front edge ──────────────────────────────────────────────────
# The facing and the lapel facing are cut to the MEASURED runs off the drawn front, not
# recomputed from the same formulas and hoped to agree. On an edge-to-edge front there
# is no overlap to absorb the difference.
_FRONT = build_front()
CF_LEN = _FRONT.edge("centre_front").length(0.2)
LAPEL_LEN = _FRONT.edge("lapel").length(0.2)
FRONT_EDGE_RUN = CF_LEN + LAPEL_LEN


def build_facing():
    """The front facing, cut to the MEASURED centre-front run.

    A charro chaleco's front edge is seen: it carries the greca and it must not ripple.
    The facing is cut to what the front edge actually measures, and declared against it."""
    w = max(lapel_width * 0.9, 48.0)
    h = CF_LEN
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    internals = [
        fc.Internal("edge-line", [fc.P(3.0, 0.0), fc.P(3.0, h)], kind="marking"),
        fc.Internal("hook-land",
                    [fc.P(2.0, 6.0), fc.P(2.0 + hook_width, 6.0),
                     fc.P(2.0 + hook_width, h - 6.0), fc.P(2.0, h - 6.0),
                     fc.P(2.0, 6.0)], kind="marking"),
    ]
    return fc.Piece(
        "facing",
        [fc.Edge("hem_end", [fc.Line(p0, p1)]),
         fc.Edge("inner", [fc.Line(p1, p2)]),
         fc.Edge("break_end", [fc.Line(p2, p3)]),
         fc.Edge("front_edge", [fc.Line(p3, p0)])],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "closure midpoint")],
        grainline=fc.Grainline(fc.P(w * 0.5, 10.0), fc.P(w * 0.5, h - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front facing (measured CF run)",
    )


def build_lapel():
    """The lapel facing, cut to the MEASURED lapel run.

    It is the piece the greca actually sits on where the lapel rolls back, so it is cut
    to the measurement rather than to the drafted formula."""
    ln = LAPEL_LEN
    w = max(lapel_width * 1.05, 42.0)
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, w)
    p3 = fc.P(0.0, w)
    internals = [
        fc.Internal("roll-line", [fc.P(0.0, w * 0.42), fc.P(ln, w * 0.42)],
                    kind="marking"),
    ]
    for r in range(soutache_rows):
        off = soutache_inset + r * (soutache_inset * 0.85)
        internals.append(fc.Internal(f"greca-row-{r + 1}",
                                     [fc.P(0.0, off), fc.P(ln, off)], kind="marking"))
    return fc.Piece(
        "lapel",
        [fc.Edge("attach", [fc.Line(p0, p1)]),
         fc.Edge("peak_end", [fc.Line(p1, p2)]),
         fc.Edge("outer", [fc.Line(p2, p3)]),
         fc.Edge("neck_end", [fc.Line(p3, p0)])],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "peak match")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w * 0.5), fc.P(ln * 0.9, w * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Lapel facing (measured lapel run)",
    )


def build():
    pattern = fc.PatternSet("chaleco-charro")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "facing":
        pattern.add(build_facing())
    if everything or target_piece == "lapel":
        pattern.add(build_lapel())

    if everything:
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        # THE seams that had to solve: an edge-to-edge front has no overlap to absorb
        # error, so both facings are cut to the MEASURED runs and declared against them.
        pattern.declare_seam(("facing", "front_edge"), ("front", "centre_front"),
                             tol=0.5)
        pattern.declare_seam(("lapel", "attach"), ("front", "lapel"), tol=0.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "worsted wool suiting", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker. The back is cut in the SUITING, not "
                 "in lining — it is part of the suit's face. Worsted takes a 160 °C "
                 "iron; the lapel roll is pressed, never creased."},
        {"item": "trouser hook and bar sets", "qty": N_HOOKS, "unit": "set",
         "note": f"Yantra4D trouser-hook-bar (notion.hardware_ref); {N_HOOKS} sets at a "
                 f"solved {PITCH_SOLVED:.1f} mm pitch over the measured "
                 f"{CLOSURE_RUN:.0f} mm closure run, sewn BEHIND the edge so nothing "
                 f"shows on an edge-to-edge front."},
        {"item": "soutache braid (greca)",
         "qty": round(soutache_rows * FRONT_EDGE_RUN * 2.2), "unit": "mm_length",
         "note": f"{soutache_rows} rows following the front edge and lapel. PLACEMENT "
                 f"is drafted; the braid pattern itself is the maker's and the "
                 f"region's, and is not invented here."},
        {"item": "canvas / haircloth front interlining", "qty": 1, "unit": "set",
         "note": "the front is canvassed: an edge-to-edge closure with no stand shows "
                 "every ripple, and fusible alone will not hold the lapel roll."},
        {"item": "lining (fronts and back)", "qty": 1, "unit": "set",
         "note": "the chaleco is fully lined; the welts are marked, and their bags are "
                 "cut from the lining."},
    ]
    pattern.metadata = {
        "fc300_rank": 300,
        "family": "heritage_global",
        "fabric_hint": "lana-peinada-traje",
        "finished_mm": {
            "chest": round(HALF_CHEST * 4.0, 1),
            "waist": round(HALF_WAIST * 4.0, 1),
            "length": round(LENGTH, 1),
            "armhole_depth": round(ARMHOLE_DEPTH, 1),
            "lapel_width": round(lapel_width, 1),
            "break_y": round(BREAK_Y, 1),
        },
        "solved": {
            "length_raw_mm": round(LENGTH_RAW, 2),
            "length_mm": round(LENGTH, 2),
            "length_floor_mm": round(LENGTH_FLOOR, 2),
            "length_floored": LENGTH_FLOORED,
            "waist_rise_mm": round(waist_rise, 2),
            "trouser_clearance_mm": round(CLEARANCE, 2),
            "closure_run_mm": round(CLOSURE_RUN, 2),
            "hooks": N_HOOKS,
            "hook_pitch_requested_mm": round(hook_pitch, 2),
            "hook_pitch_solved_mm": round(PITCH_SOLVED, 3),
            "cf_measured_mm": round(CF_LEN, 3),
            "lapel_measured_mm": round(LAPEL_LEN, 3),
            "front_edge_run_mm": round(FRONT_EDGE_RUN, 3),
            "front_shoulder_mm": round(_SHOULDER_LEN, 3),
            "back_neck_rise_mm": round(BACK_NECK_Y, 3),
            "back_neck_rise_requested_mm": round(_BACK_RISE_WANTED, 3),
            "back_neck_clamped": BACK_NECK_CLAMPED,
            "lapel_width_requested_mm": round(LAPEL_WIDTH_REQUESTED, 2),
            "lapel_width_capped": LAPEL_WIDTH_CAPPED,
            "note": "the length is set by the TROUSER, not by the torso: the charro "
                    "trouser rides high on a wide band, and the chaleco must finish "
                    "ABOVE it or it breaks the long shoulder-to-boot line the suit is "
                    "built around. So LENGTH = nape_to_waist - waist_rise - clearance, "
                    "floored at the armhole depth plus a real body run — below that "
                    "there is no waistcoat left, only an armhole, and the floor is "
                    "reported when it fires. The front closes EDGE TO EDGE at centre "
                    "front with no button stand, so there is no overlap to absorb "
                    "error: both facings are cut to the MEASURED runs off the drawn "
                    "front and declared against them, and the hooks are spaced on the "
                    "measured closure run at a pitch recomputed to whole intervals so "
                    "the column lands on both clearances instead of drifting.",
        },
        "heritage": {
            "garment": "chaleco charro — the waistcoat of the traje de charro",
            "not_an_english_waistcoat": "no button stand (edge-to-edge, hook and bar), "
                                        "no pointed CF hem, no lining-weight cinch "
                                        "back; the length is set by the trouser band",
            "greca": "soutache PLACEMENT is drafted as marked rows following the front "
                     "edge and lapel. The braid pattern itself belongs to the maker and "
                     "the region and is not invented here.",
            "excluded": "no botonadura de plata, no escudo, no association or team "
                        "insignia; the gala categories' silverwork and the competition "
                        "dress codes of the Federación Mexicana de Charrería are not "
                        "drafted by this cartridge",
        },
        "hardware": "front closure via Yantra4D (notion.hardware_ref -> "
                    "trouser-hook-bar); the hook's sewn plate is driven by this "
                    "chaleco's hook_width, and the count and pitch come from the "
                    "MEASURED closure run",
    }
    return pattern


result = build()
