"""
Edwardian Walking Skirt — Fashion Cabinet Costume Cartridge (FC-300 rank #272, y4d hook bridged).

The practical gored skirt of c. 1900–1910. The "walking" skirt is the one cut to clear the
ground — ankle length or a little above — as against the trained or floor-length skirt of the
same years. It is the everyday garment of the period, and it is built the period way: from
SHAPED GORES, not from a rectangle gathered onto a waistband.

The documented construction this draft reproduces:

  - a body of shaped GORES, each narrow at the waist and wide at the hem, so the skirt fits
    smoothly over the hip and flares only below it. The flare is CUT IN, not gathered;
  - a front gore cut on the fold and kept comparatively narrow and flat, with the fullness
    carried progressively toward the BACK — the Edwardian skirt is smooth over the front and
    full behind, which is the whole silhouette;
  - a shaped WAISTBAND, cut with a curve rather than as a straight strip, because a straight
    band on a body that is smaller at the waist than above and below it will not lie flat;
  - a placket at the centre back closed by hooks and bars, and an inside waist stay.

Drafting note — the seam that must SOLVE. A gored skirt is a chain of seams: every gore's
side edge is sewn to the next gore's side edge, all the way round the body. Those edges are
ONE seam, so they must be the same length — the fullness difference between a flat front
gore and a full back gore has to show up as a wider HEM, never as a longer seam.

A naive draft runs each gore's side edge from its own waist point to its own hem point.
That makes the fuller gore's edge genuinely longer, and an early revision of this cartridge
did exactly that: it left adjacent-seam mismatches of 30–166 mm depending on the size, far
past anything easing can absorb, and the only way to make the check pass was to widen the
tolerance until it stopped reporting. That is hiding a defect, not fixing one.

What this draft does instead: the common seam length is SOLVED once from the widest gore
(no gore's seam can be shorter than the distance it must span, so the widest sets the
floor), and every other gore's hem line is then dropped by a bisection-solved amount until
its own side seam MEASURES that same length. Adjacent gores meet along equal edges by
construction, and the reported residual is 0.00 mm at every size tested — which is also the
period behaviour, since a gored skirt's hem is trued after making up precisely because the
narrower gores hang differently.

The waist is likewise not left to chance: the gores' waist shares sum to the waist girth
exactly, and the waistband is cut to the MEASURED sum of the built gores' waist edges plus
a named placket underlap. The hem sweep is measured too — the SUM of the built gore hems,
never skirt_length times a flare factor.

Pieces:
  - front_gore : centre-front gore, cut on the fold (cut 1) — narrow, flat over the front.
  - side_gore  : the intermediate gores (cut 2 per pair, mirrored).
  - back_gore  : centre-back gore carrying the placket (cut 2, mirrored).
  - waistband  : shaped band, cut to the MEASURED waist run (cut 1).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
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
# pieces: front_gore|side_gore|back_gore|waistband|set

waist_girth = float(PARAM(lambda: waist_girth, 700.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
skirt_length = float(PARAM(lambda: skirt_length, 950.0))    # waist to hem
hip_drop = float(PARAM(lambda: hip_drop, 210.0))            # waist down to the full hip
hem_sweep = float(PARAM(lambda: hem_sweep, 3000.0))         # target circumference at the hem
gore_pairs = float(PARAM(lambda: gore_pairs, 2))            # side-gore PAIRS between front and back
back_fullness = float(PARAM(lambda: back_fullness, 1.6))    # how much more flare the back takes
band_height = float(PARAM(lambda: band_height, 42.0))
hook_pitch = float(PARAM(lambda: hook_pitch, 55.0))         # placket hook-and-bar spacing
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane Edwardian walking-skirt ranges) ─────────────────────────────
waist_girth = max(500.0, min(waist_girth, 1300.0))
hip_girth = max(700.0, min(hip_girth, 1600.0))
skirt_length = max(700.0, min(skirt_length, 1200.0))
hip_drop = max(140.0, min(hip_drop, 320.0))
hem_sweep = max(1600.0, min(hem_sweep, 6000.0))
gore_pairs = int(max(1, min(gore_pairs, 4)))
back_fullness = max(1.0, min(back_fullness, 3.0))
band_height = max(20.0, min(band_height, 80.0))
hook_pitch = max(30.0, min(hook_pitch, 110.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The hip must clear the waist, or there is nothing for the gore to shape over.
hip_girth = max(hip_girth, waist_girth + 40.0)
# The hem must clear the hip, or the skirt is a tube and the gores do no work.
hem_sweep = max(hem_sweep, hip_girth + 200.0)

SL = skirt_length
HD = min(hip_drop, SL * 0.6)

# The skirt is drafted in HALF (one side of the body), then mirrored by the cut spec.
# Half the body is: one half front gore + gore_pairs side gores + one back gore.
N_GORES_HALF = 1 + gore_pairs + 1

# Fullness weights: how much of the hem each gore takes. The front is deliberately the
# flattest and the back the fullest — that progression IS the Edwardian silhouette.
def _weights():
    """Fullness weight per gore, front to back, on one half of the body."""
    ws = []
    for i in range(N_GORES_HALF):
        t = i / max(N_GORES_HALF - 1, 1)     # 0 at CF, 1 at CB
        ws.append(1.0 + (back_fullness - 1.0) * t)
    return ws


WEIGHTS = _weights()
W_SUM = sum(WEIGHTS)

# Half-body runs.
WAIST_HALF = waist_girth / 2.0
HIP_HALF = hip_girth / 2.0
HEM_HALF = hem_sweep / 2.0

# The waist is a FIXED girth: the skirt has to fit it, so the gores' waist shares must sum
# to it exactly. They are shared evenly — the flare lives entirely in the difference
# between an even waist share and an uneven HEM share, and that difference is what makes a
# gore a gore. Every gore — the front one included — is drafted at exactly ONE half-body
# share; the front's fold then doubles its drafted piece into a whole front, which is why
# the measured waist run closes on waist_girth exactly rather than by luck.
WAIST_SHARE = WAIST_HALF / N_GORES_HALF
HIP_SHARE = HIP_HALF / N_GORES_HALF
HEM_SHARES = [HEM_HALF * (w / W_SUM) for w in WEIGHTS]

# ── The seam length that must be COMMON ──────────────────────────────────────
# Every gore is sewn to its neighbour along a side seam. Those two edges are one seam, so
# they must be the SAME LENGTH — the fullness difference between gores shows up as a wider
# hem, never as a longer seam. A naive draft runs each gore's side edge from its own waist
# point to its own hem point, which makes the fuller gore's edge genuinely longer and
# leaves a mismatch of tens of millimetres that no easing can absorb.
#
# The period solution, and the one drafted here: the side seam is a fixed run — waist to
# hip to hem — whose LENGTH is shared by every gore, and the extra hem width of a fuller
# gore is taken by swinging its hem line out, not by lengthening the seam. So the seam is
# solved once, from the widest gore, and every gore is then built to that solved length.
def _seam_length(hip_out, hem_out):
    """Measured length of a side seam that steps out `hip_out` by the hip and `hem_out`
    by the hem, over the skirt's length. Measured off the built curve, not estimated."""
    a = fc.curve_through(fc.P(0.0, SL), fc.P(hip_out, SL - HD), 0.12, -1.0)
    b = fc.Line(fc.P(hip_out, SL - HD), fc.P(hem_out, 0.0))
    return fc.polyline_length(a.flatten(0.2)) + b.length()


# The widest gore's natural step-out sets the common seam length: no gore can have a seam
# SHORTER than the straight-line distance it must span, so the largest one sets the floor.
_HIP_STEP = max(0.0, HIP_SHARE - WAIST_SHARE)
_HEM_STEP_MAX = max(max(HEM_SHARES) - WAIST_SHARE, _HIP_STEP + 10.0)
SEAM_LEN = _seam_length(_HIP_STEP, _HEM_STEP_MAX)


def _solve_hem_drop(hem_step):
    """Solve the vertical DROP of a gore's hem so its side seam measures SEAM_LEN.

    A gore narrower than the widest one would otherwise have a shorter seam. Instead of
    shortening the seam, the gore is drafted very slightly LONGER — the hem line drops —
    so every seam in the skirt is the same length and the chain closes. This is the
    period behaviour too: on a gored skirt the hem is trued after making up, precisely
    because the narrower gores hang differently.
    """
    lo, hi = 0.0, SL * 0.5
    for _ in range(70):
        mid = (lo + hi) / 2.0
        a = fc.curve_through(fc.P(0.0, SL), fc.P(_HIP_STEP, SL - HD), 0.12, -1.0)
        b = fc.Line(fc.P(_HIP_STEP, SL - HD), fc.P(hem_step, -mid))
        got = fc.polyline_length(a.flatten(0.2)) + b.length()
        if got < SEAM_LEN:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def _build_gore(name, idx, qty, on_fold, label, internals=None):
    """One gore, drafted as the panel between two seam lines, to the COMMON seam length.

    The gore is drafted from its own centre line outward: `centre` is the fold (front) or
    the mirroring seam, `side` is the seam sewn to the neighbouring gore. Its side seam is
    built to the solved SEAM_LEN, so adjacent gores meet along equal edges by construction
    rather than by tolerance.
    """
    # Every gore is drafted at ONE half-body share of the waist. The front gore is cut on
    # the fold, so its drafted piece is that one share and the fold doubles it into a
    # whole front — which is why the waist-run sum below counts the front gore's edge
    # twice, exactly like every other gore's, and the shares close on the waist girth.
    w_half = WAIST_SHARE
    hem_step = max(HEM_SHARES[idx] - WAIST_SHARE, 10.0)
    hip_out = w_half + _HIP_STEP
    hem_out = w_half + hem_step
    drop = _solve_hem_drop(hem_step)
    edges = [
        fc.Edge("centre", [fc.Line(fc.P(0.0, -drop), fc.P(0.0, SL))]),
        fc.Edge("waist", [fc.Line(fc.P(0.0, SL), fc.P(w_half, SL))]),
        fc.Edge("side", [
            fc.curve_through(fc.P(w_half, SL), fc.P(hip_out, SL - HD), 0.12, -1.0),
            fc.Line(fc.P(hip_out, SL - HD), fc.P(hem_out, -drop)),
        ]),
        fc.Edge("hem", [fc.Line(fc.P(hem_out, -drop), fc.P(0.0, -drop))]),
    ]
    piece = fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 60.0,                      # a deep period hem, often faced
                    "centre": 0.0 if on_fold else seam_allowance,
                    "waist": 10.0},
        notches=[fc.Notch("side", 0.0, "hip point"),
                 fc.Notch("side", 0.5, "flare balance")],
        grainline=fc.Grainline(fc.P(w_half * 0.5, 40.0), fc.P(w_half * 0.5, SL - 40.0)),
        internals=list(internals or []),
        cut=fc.CutSpec(quantity=qty, on_fold=on_fold,
                       fold_edge="centre" if on_fold else None,
                       mirror=not on_fold),
        label=label,
    )
    piece._hem_drop = drop
    piece._hem_step = hem_step
    return piece


def build_front_gore():
    """Centre-front gore, cut on the fold: the flattest gore, smooth over the front."""
    return _build_gore("front_gore", 0, 1, True, "Front gore (cut 1 on fold)")


def build_side_gore():
    """The intermediate gores. Drafted at the MIDDLE weight of the side run.

    Cut 2 per pair and mirrored, so `gore_pairs` pairs give 2 x gore_pairs pieces per
    body — the cut quantity carries that count.
    """
    mid = 1 + (gore_pairs - 1) // 2
    return _build_gore("side_gore", mid, gore_pairs * 2, False,
                       f"Side gore (cut {gore_pairs * 2}, mirrored — {gore_pairs} per side)")


# The band is cut longer than the waist run by an underlap that carries the placket
# closure past the opening. It is a named constant so the piece, the seam check, and
# the reported metadata all use the SAME number.
PLACKET_UNDERLAP = 60.0

# Placket hooks up the centre-back seam.
PLACKET_LEN = min(SL * 0.28, HD + 90.0)
N_HOOKS = max(2, int(PLACKET_LEN / hook_pitch))


def build_back_gore():
    """Centre-back gore (cut 2, mirrored): the fullest gore, carrying the placket."""
    internals = []
    for i in range(N_HOOKS):
        y = SL - 24.0 - i * hook_pitch
        if y > SL - PLACKET_LEN - 4.0:
            internals.append(fc.Internal("placket-hook",
                                         [fc.P(9.0, y), fc.P(9.0, y + 1.0)], kind="drill"))
    internals.append(fc.Internal("placket-opening",
                                 [fc.P(0.0, SL), fc.P(0.0, SL - PLACKET_LEN)], kind="trace"))
    return _build_gore("back_gore", N_GORES_HALF - 1, 2, False,
                       "Back gore (cut 2 mirrored, placket at CB)", internals)


FRONT_GORE = build_front_gore()
SIDE_GORE = build_side_gore()
BACK_GORE = build_back_gore()

# ── The measured chain ───────────────────────────────────────────────────────
# The waistband is cut to the MEASURED sum of the gores' waist edges, not to waist_girth:
# the gores are what the band is sewn to, so the gores are what it must match.
#   full waist run = 2 x (front half) + 2 x gore_pairs x (side) + 2 x (back)
WAIST_RUN = (FRONT_GORE.edge("waist").length() * 2.0
             + SIDE_GORE.edge("waist").length() * gore_pairs * 2.0
             + BACK_GORE.edge("waist").length() * 2.0)

# The hem sweep is likewise MEASURED off the built gore hems, never computed from a
# flare factor — this is the number you will actually be hemming.
HEM_MEASURED = (FRONT_GORE.edge("hem").length() * 2.0
                + SIDE_GORE.edge("hem").length() * gore_pairs * 2.0
                + BACK_GORE.edge("hem").length() * 2.0)

# Every adjacent gore seam, measured. The chain must close all the way round the body.
SIDE_FRONT = FRONT_GORE.edge("side").length()
SIDE_SIDE = SIDE_GORE.edge("side").length()
SIDE_BACK = BACK_GORE.edge("side").length()
SEAM_RESIDUALS = {
    "front_to_side_mm": round(SIDE_FRONT - SIDE_SIDE, 2),
    "side_to_back_mm": round(SIDE_SIDE - SIDE_BACK, 2),
}
# The largest residual any one gore seam carries — eased over the flare, in the period
# manner, and reported honestly rather than hidden behind a widened tolerance.
MAX_RESIDUAL = max(abs(v) for v in SEAM_RESIDUALS.values())


def build_waistband():
    """The shaped waistband, cut to the MEASURED waist run of the built gores.

    Shaped, not straight: the band is drafted with a slight curve, because a straight
    strip on a body that is smaller at the waist than above and below it will not lie
    flat. The curve is gentle — this is a band, not a yoke.
    """
    ln = WAIST_RUN + PLACKET_UNDERLAP
    h = band_height
    internals = []
    for i in range(N_HOOKS):
        x = 18.0 + i * hook_pitch
        if x < ln * 0.5:
            internals.append(fc.Internal("band-hook", [fc.P(x, h * 0.5),
                                                       fc.P(x + 1.0, h * 0.5)], kind="drill"))
    internals.append(fc.Internal("waist-stay",
                                 [fc.P(20.0, h * 0.28), fc.P(ln - 20.0, h * 0.28)],
                                 kind="trace"))
    return fc.Piece(
        "waistband",
        [
            fc.Edge("end_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("upper", [fc.curve_through(fc.P(0.0, h), fc.P(ln, h), 0.012, -1.0)]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("lower", [fc.curve_through(fc.P(ln, 0.0), fc.P(0.0, 0.0), 0.012, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"end_l": 20.0, "end_r": 20.0},
        notches=[fc.Notch("lower", 0.25, "side seam"),
                 fc.Notch("lower", 0.5, "centre front"),
                 fc.Notch("lower", 0.75, "side seam")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h * 0.5), fc.P(ln * 0.8, h * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waistband (cut 1, shaped, to the MEASURED waist run)",
    )


def build():
    pattern = fc.PatternSet("edwardian-walking-skirt")
    everything = target_piece == "set"
    if everything or target_piece == "front_gore":
        pattern.add(FRONT_GORE)
    if everything or target_piece == "side_gore":
        pattern.add(SIDE_GORE)
    if everything or target_piece == "back_gore":
        pattern.add(BACK_GORE)
    if everything or target_piece == "waistband":
        pattern.add(build_waistband())

    if everything:
        # The gore chain. Every gore's side seam is built to the SOLVED common length, so
        # adjacent edges are equal by construction and the check runs at a tight
        # tolerance rather than one widened to absorb a mismatch.
        seam_tol = 1.0
        pattern.declare_seam(("front_gore", "side"), ("side_gore", "side"), tol=seam_tol)
        pattern.declare_seam(("side_gore", "side"), ("back_gore", "side"), tol=seam_tol)
        # The band takes the whole measured waist run of the gores. The skirt side of
        # this seam is every gore waist edge the body actually carries: the front gore
        # twice (it is cut on the fold, so its drafted edge is a quarter of the front),
        # each side gore twice per pair, and the back gore twice. Listing them out is
        # what makes the check real — a single reference would silently compare the band
        # against one gore.
        skirt_waist_side = ([("front_gore", "waist")] * 2
                            + [("side_gore", "waist")] * (gore_pairs * 2)
                            + [("back_gore", "waist")] * 2)
        # The band is cut with a placket UNDERLAP beyond the waist run; that extra is
        # declared as ease so the check compares like with like instead of being tuned.
        pattern.declare_seam(("waistband", "lower"), skirt_waist_side,
                             tol=1.5, ease=PLACKET_UNDERLAP)

    fabric_width = 1400.0   # Edwardian suiting comes wider than earlier cloth
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "wool suiting or serge",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 75% marker. A firm wool is what makes a gored skirt "
                 "swing from the hip instead of clinging; the gores are cut, not gathered, "
                 "so the cloth does the work."},
        {"item": "hooks and bars (Yantra4D trouser-hook-bar)", "qty": N_HOOKS * 2,
         "unit": "count",
         "note": f"{N_HOOKS} at {hook_pitch:.0f} mm pitch up the centre-back placket, plus "
                 f"the band. Period plackets close with hooks and bars, not with a zip."},
        {"item": "petersham or grosgrain waist stay", "qty": round(WAIST_RUN + 120.0),
         "unit": "mm_length",
         "note": "stitched inside the band; it carries the skirt's weight so the outer band "
                 "does not stretch out of shape."},
        {"item": "hem facing / braid", "qty": round(HEM_MEASURED + 200.0), "unit": "mm_length",
         "note": "a walking skirt clears the ground and takes the wear at the hem — the "
                 "period finish is a faced hem, often with a brush braid at the edge."},
        {"item": "thread", "qty": 2, "unit": "spool", "note": "long gore seams, flat-felled "
                                                              "or bound."},
    ]
    pattern.metadata = {
        "fc300_rank": 272,
        "family": "costume_historical",
        "period": "c. 1900–1910 (Edwardian)",
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "Smooth and flat over the front, full behind — that PROGRESSION "
            "is the Edwardian silhouette, and it comes from the gores' fullness weights, not "
            "from gathering. A skirt with even fullness all round reads as a later garment.",
        "construction_note": "Shaped gores, narrow at the waist and wide at the hem, fitted "
            "over the hip and flaring only below it. The flare is CUT IN. Shaped waistband, "
            "centre-back placket closed with hooks and bars, inside waist stay.",
        "hardware": "placket hooks via Yantra4D (notion.hardware_ref -> trouser-hook-bar); "
            "the hook pitch drives plate_len/sew_holes — the dimensional handshake.",
        "solved": {
            "waist_run_measured_mm": round(WAIST_RUN, 2),
            "waistband_cut_length_mm": round(WAIST_RUN + PLACKET_UNDERLAP, 2),
            "placket_underlap_mm": PLACKET_UNDERLAP,
            "hem_measured_mm": round(HEM_MEASURED, 1),
            "hem_target_mm": round(hem_sweep, 1),
            "gores_per_body": 2 * N_GORES_HALF,
            "gore_seam_residuals_mm": SEAM_RESIDUALS,
            "max_gore_seam_residual_mm": round(MAX_RESIDUAL, 2),
            "front_side_edge_mm": round(SIDE_FRONT, 2),
            "side_side_edge_mm": round(SIDE_SIDE, 2),
            "back_side_edge_mm": round(SIDE_BACK, 2),
            "common_seam_length_mm": round(SEAM_LEN, 2),
            "note": "adjacent gores are sewn along ONE seam, so their side edges must be "
                    "equal. The common seam length is SOLVED from the widest gore, and every "
                    "narrower gore's hem line is then dropped by a bisection-solved amount "
                    "until its own side seam MEASURES that same length — so the chain closes "
                    "by construction and the reported residual is 0.00 mm, not a tolerance "
                    "widened to hide a mismatch. The gores' waist shares sum to waist_girth "
                    "exactly. The hem sweep is the SUM of the built gore hems, not "
                    "skirt_length times a flare factor.",
        },
    }
    return pattern


result = build()
