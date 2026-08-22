"""
Cotehardie — Fashion Cabinet Costume Cartridge (FC-300 rank #270, y4d eyelet bridged).

The fitted gown of the mid-14th century, c. 1340–1400. The cotehardie is the moment
European dress stops being a draped tube and becomes TAILORED: it fits the torso closely
through shaped seams and then releases into a full skirt through inserted GORES. Getting
that transition right is the whole garment.

The documented construction this draft reproduces:

  - a four-panel body (front, back, two sides) fitted through the torso by the shape of the
    seams themselves — there is no waist seam and no dart. The cotehardie is cut in one
    length from shoulder to hem;
  - GORES inserted into the seams below the hip, which is what turns a close body into a
    full skirt without ever cutting the body apart at the waist. This is the defining
    medieval solution, and it is why the garment has no waist seam;
  - SIDE LACING through worked eyelets at one or both side seams, which is how a garment
    with no elastic and no back zip gets close enough to fit;
  - a modest boat neckline and close sleeves buttoned or laced at the forearm.

Drafting note — the seam that must SOLVE. A gore is a triangle inserted into a SLIT in a
seam. Its two long sides are sewn to the two lips of that slit, so each gore side must
equal the slit depth exactly. This draft builds the gore first, MEASURES its side off the
built polygon, and cuts the body panels' gore-slit edges to exactly that measured length —
so the gore seam balances by construction. Separately, the hem is not assumed: it is
MEASURED as the sum of the built panel hems plus the built gore bases, and reported.

Pieces:
  - front  : centre-front body panel, cut on the fold (cut 1).
  - back   : centre-back body panel, cut on the fold (cut 1).
  - side   : side body panel carrying the lacing (cut 2, mirrored).
  - gore   : skirt gore inserted into the seams below the hip (cut 4).
  - sleeve : close sleeve, buttoned/laced at the forearm (cut 2, mirrored).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|side|gore|sleeve|set

bust_girth = float(PARAM(lambda: bust_girth, 900.0))
waist_girth = float(PARAM(lambda: waist_girth, 740.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
gown_length = float(PARAM(lambda: gown_length, 1350.0))   # shoulder to hem
waist_drop = float(PARAM(lambda: waist_drop, 380.0))      # shoulder to waist
gore_rise = float(PARAM(lambda: gore_rise, 620.0))        # how far up the seam a gore reaches
gore_flare = float(PARAM(lambda: gore_flare, 260.0))      # width each gore adds at the hem
shoulder_width = float(PARAM(lambda: shoulder_width, 130.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 600.0))
eyelet_pitch = float(PARAM(lambda: eyelet_pitch, 26.0))   # side-lacing eyelet spacing
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane 14th-c gown ranges) ─────────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1300.0))
hip_girth = max(760.0, min(hip_girth, 1500.0))
gown_length = max(900.0, min(gown_length, 1750.0))
waist_drop = max(280.0, min(waist_drop, 520.0))
gore_rise = max(250.0, min(gore_rise, 1100.0))
gore_flare = max(80.0, min(gore_flare, 520.0))
shoulder_width = max(90.0, min(shoulder_width, 190.0))
sleeve_length = max(420.0, min(sleeve_length, 740.0))
eyelet_pitch = max(15.0, min(eyelet_pitch, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = gown_length
WD = waist_drop
# A gore cannot rise above the waist — the body must stay whole where it fits.
gore_rise = min(gore_rise, L - WD - 40.0)
HIP_DROP = WD + (L - WD) * 0.22          # hip line, below the waist
ARMHOLE_DEPTH = WD * 0.52

# The body is drafted in four panels around the torso. Close fit: small ease.
BUST_4 = (bust_girth + 50.0) / 4.0 / 2.0    # half-width of one panel at the bust
WAIST_4 = (waist_girth + 30.0) / 4.0 / 2.0
HIP_4 = (hip_girth + 60.0) / 4.0 / 2.0

# Vertical positions measured DOWN from the shoulder (y = L is the shoulder, y = 0 the hem).
Y_SHOULDER = L
Y_BUST = L - ARMHOLE_DEPTH
Y_WAIST = L - WD
Y_HIP = L - HIP_DROP
Y_GORE_TOP = gore_rise                       # the gore's apex, measured up from the hem


def build_gore():
    """A skirt gore: an isosceles triangle inserted into a slit in a body seam.

    `side_l` / `side_r` are the SEWN edges — they go to the two lips of the slit.
    `base` falls at the hem. Built FIRST so the body panels' slit edges can be cut to
    the gore side's MEASURED length rather than to an assumed value.
    """
    half = gore_flare / 2.0
    rise = Y_GORE_TOP
    return fc.Piece(
        "gore",
        [
            fc.Edge("base", [fc.Line(fc.P(-half, 0.0), fc.P(half, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(half, 0.0), fc.P(0.0, rise))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, rise), fc.P(-half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"base": 30.0},   # a deep hem, as period gowns carry
        notches=[fc.Notch("side_r", 1.0, "gore apex"),
                 fc.Notch("side_l", 0.0, "gore apex"),
                 fc.Notch("side_r", 0.5, "gore midpoint"),
                 fc.Notch("side_l", 0.5, "gore midpoint")],
        grainline=fc.Grainline(fc.P(0.0, rise * 0.12), fc.P(0.0, rise * 0.88)),
        cut=fc.CutSpec(quantity=4),
        label="Skirt gore (cut 4)",
    )


GORE = build_gore()
# The MEASURED sewn side of the gore — the slit in the body seam must equal THIS.
GORE_SIDE = GORE.edge("side_l").length()


def _body_side_edge(top_w, top_y):
    """The shaped side edge of a body panel, from the underarm down to the hem.

    It runs: underarm -> waist (nipped in) -> hip (out) -> then STRAIGHT down for exactly
    GORE_SIDE, which is the slit the gore is sewn into. Building the lower run as a
    measured straight segment is what makes the gore seam solve.
    """
    return [
        fc.Line(fc.P(top_w, top_y), fc.P(WAIST_4, Y_WAIST)),
        fc.Line(fc.P(WAIST_4, Y_WAIST), fc.P(HIP_4, Y_HIP)),
        # from the hip down to the gore apex — the body stays whole here
        fc.Line(fc.P(HIP_4, Y_HIP), fc.P(HIP_4, Y_GORE_TOP)),
        # the SLIT: exactly the gore's measured side length, straight down to the hem
        fc.Line(fc.P(HIP_4, Y_GORE_TOP), fc.P(HIP_4, Y_GORE_TOP - GORE_SIDE)),
    ]


HEM_Y = Y_GORE_TOP - GORE_SIDE   # where the body panel's hem actually lands


# Each panel carries a different neck width — the period cut scoops the front neck low
# and narrow, sets the back higher and wider, and the side splits the difference. Every
# panel's shoulder edge runs from its own neck point out to the common shoulder point, so
# a naive draft leaves three shoulder seams of three different lengths. They are sewn to
# each other, so that is a real defect, not a rounding artefact.
FRONT_NECK_W = shoulder_width * 0.52
BACK_NECK_W = shoulder_width * 0.56
SIDE_NECK_W = shoulder_width * 0.50
PANEL_NECK_WIDTHS = (FRONT_NECK_W, BACK_NECK_W, SIDE_NECK_W)

# The shoulder point sits a little forward of the neck point — SHOULDER_DROP is that
# nominal slope, taken on the panel with the NARROWEST neck (the longest flat run).
SHOULDER_DROP = 14.0

# The reference shoulder length is solved, not assumed. A panel's shoulder is the
# hypotenuse over horizontal run dx = shoulder_width - neck_w and vertical drop d ≥ 0,
# so the shortest length any panel can reach is its own dx (a flat shoulder, d = 0). The
# common length must therefore be at least the LARGEST dx across the panels — i.e. the
# panel with the WIDEST neck sets the floor — or that panel has no solution at all.
_WIDEST_NECK_DX = max(shoulder_width - nw for nw in PANEL_NECK_WIDTHS)
_NARROWEST_NECK_DX = min(shoulder_width - nw for nw in PANEL_NECK_WIDTHS)
SHOULDER_LEN = max(
    (_NARROWEST_NECK_DX ** 2 + SHOULDER_DROP ** 2) ** 0.5,   # nominal slope on the long run
    (_WIDEST_NECK_DX ** 2 + SHOULDER_DROP ** 2) ** 0.5,      # keeps the widest neck solvable
)
# Kept under the historical name for the metadata block; both now agree by construction.
FRONT_SHOULDER_LEN = SHOULDER_LEN


def _shoulder_drop_for(neck_w):
    """Solve the shoulder-point drop that makes THIS panel's shoulder equal SHOULDER_LEN.

    dx is the horizontal run from this panel's neck point to the common shoulder point;
    the drop is the remaining leg of the right triangle whose hypotenuse is the shared
    SHOULDER_LEN. Because SHOULDER_LEN was chosen to exceed every panel's dx, the term
    under the root is positive for all three panels — there is no degenerate branch to
    fall back to, and no tolerance to widen.
    """
    dx = shoulder_width - neck_w
    return max(0.0, SHOULDER_LEN ** 2 - dx ** 2) ** 0.5


def _body_panel(name, neck_w, neck_drop, armhole_bulge, label, qty, on_fold, extra_internals):
    """One body panel: shoulder to hem in a single length, no waist seam."""
    side_segs = _body_side_edge(BUST_4, Y_BUST)
    sh_drop = _shoulder_drop_for(neck_w)
    edges = [
        fc.Edge("cf", [fc.Line(fc.P(0.0, HEM_Y), fc.P(0.0, Y_SHOULDER - neck_drop))]),
        fc.Edge("neck", [fc.curve_through(fc.P(0.0, Y_SHOULDER - neck_drop),
                                          fc.P(neck_w, Y_SHOULDER), 0.16, -1.0)]),
        fc.Edge("shoulder", [fc.Line(fc.P(neck_w, Y_SHOULDER),
                                     fc.P(shoulder_width, Y_SHOULDER - sh_drop))]),
        fc.Edge("armhole", [fc.curve_through(fc.P(shoulder_width, Y_SHOULDER - sh_drop),
                                             fc.P(BUST_4, Y_BUST), armhole_bulge, -1.0)]),
        fc.Edge("side", side_segs),
        fc.Edge("hem", [fc.Line(fc.P(HIP_4, HEM_Y), fc.P(0.0, HEM_Y))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"cf": 0.0 if on_fold else seam_allowance, "hem": 30.0, "neck": 8.0},
        notches=[fc.Notch("side", 0.5, "waist"),
                 fc.Notch("armhole", 0.5, "armhole balance")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.45, HEM_Y + 40.0),
                               fc.P(BUST_4 * 0.45, Y_SHOULDER - 40.0)),
        internals=extra_internals,
        cut=fc.CutSpec(quantity=qty, on_fold=on_fold,
                       fold_edge="cf" if on_fold else None,
                       mirror=not on_fold),
        label=label,
    )


def build_front():
    """Centre-front panel, cut on the fold. A modest boat neck, as the period wears."""
    internals = [fc.Internal("gore-slit-mark",
                             [fc.P(HIP_4, Y_GORE_TOP), fc.P(HIP_4 - 12.0, Y_GORE_TOP)],
                             kind="drill")]
    return _body_panel("front", FRONT_NECK_W, 62.0, 0.20,
                       "Front (cut 1 on fold)", 1, True, internals)


def build_back():
    """Centre-back panel, cut on the fold. The back neck sits higher than the front."""
    internals = [fc.Internal("gore-slit-mark",
                             [fc.P(HIP_4, Y_GORE_TOP), fc.P(HIP_4 - 12.0, Y_GORE_TOP)],
                             kind="drill")]
    return _body_panel("back", BACK_NECK_W, 26.0, 0.13,
                       "Back (cut 1 on fold)", 1, True, internals)


# How many lacing eyelets fit up the side seam, at the requested pitch.
N_EYELETS = max(4, int((Y_BUST - Y_WAIST + WD * 0.5) / eyelet_pitch))
# Forearm buttons closing the sleeve from elbow to wrist.
N_FOREARM_BUTTONS = max(3, int((sleeve_length * 0.34) / max(eyelet_pitch, 1.0)))


def build_side():
    """Side panel (cut 2, mirrored) carrying the lacing eyelets at the front side seam."""
    n_eyelets = N_EYELETS
    internals = [fc.Internal("gore-slit-mark",
                             [fc.P(HIP_4, Y_GORE_TOP), fc.P(HIP_4 - 12.0, Y_GORE_TOP)],
                             kind="drill")]
    for i in range(n_eyelets):
        y = Y_WAIST - WD * 0.22 + i * eyelet_pitch
        if y < Y_BUST:
            internals.append(fc.Internal("lacing-eyelet",
                                         [fc.P(10.0, y), fc.P(10.0, y + 1.0)], kind="drill"))
    return _body_panel("side", SIDE_NECK_W, 44.0, 0.17,
                       "Side (cut 2 mirrored, side lacing)", 2, False, internals)


def _cap_length(bulge, cap_w, cap_h):
    """Measured length of the two-lobe sleeve cap at the given bulge factor."""
    a = fc.curve_through(fc.P(0.0, 0.0), fc.P(cap_w * 0.5, cap_h), bulge * 0.58, 1.0)
    b = fc.curve_through(fc.P(cap_w * 0.5, cap_h), fc.P(cap_w, 0.0), bulge, 1.0)
    return (fc.polyline_length(a.flatten(0.2))
            + fc.polyline_length(b.flatten(0.2)))


def _solve_cap_bulge(cap_w, cap_h, target):
    """Bisect the cap's bulge until the MEASURED cap length equals `target`.

    The armscye is a fixed, measured quantity; the cap is solved to match it. Doing it
    the other way round — computing both from formulas and hoping — is what leaves a
    sleeve that will not set in.
    """
    lo, hi = 0.0, 3.0
    if _cap_length(hi, cap_w, cap_h) < target:
        return hi, _cap_length(hi, cap_w, cap_h)
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if _cap_length(mid, cap_w, cap_h) < target:
            lo = mid
        else:
            hi = mid
    b = (lo + hi) / 2.0
    return b, _cap_length(b, cap_w, cap_h)


# The armscye is MEASURED off the built body panels, then the cap is solved against it.
ARMSCYE = 0.0        # filled in after the body panels are built
CAP_BULGE = 0.0
CAP_MEASURED = 0.0
SLEEVE_EASE = 18.0   # modest ease worked into a close medieval sleeve


def build_sleeve():
    """A close sleeve, buttoned or laced at the forearm — the period's fitted sleeve.

    The cap is drafted at the SOLVED bulge, so it measures the armscye plus the ease.
    """
    cap_w = ARMSCYE * 0.60
    cap_h = ARMHOLE_DEPTH * 0.70
    wrist_w = cap_w * 0.38          # genuinely close at the wrist
    inset = (cap_w - wrist_w) / 2.0
    ln = sleeve_length
    n_but = N_FOREARM_BUTTONS
    internals = []
    for i in range(n_but):
        y = -ln + 30.0 + i * eyelet_pitch
        internals.append(fc.Internal("forearm-button", [fc.P(inset + 8.0, y),
                                                        fc.P(inset + 8.0, y + 1.0)],
                                     kind="drill"))
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("under_b", [fc.Line(fc.P(cap_w, 0.0), fc.P(cap_w - inset, -ln))]),
            fc.Edge("wrist", [fc.Line(fc.P(cap_w - inset, -ln), fc.P(inset, -ln))]),
            fc.Edge("under_f", [fc.Line(fc.P(inset, -ln), fc.P(0.0, 0.0))]),
            fc.Edge("cap", [
                fc.curve_through(fc.P(0.0, 0.0), fc.P(cap_w * 0.5, cap_h),
                                 CAP_BULGE * 0.58, 1.0),
                fc.curve_through(fc.P(cap_w * 0.5, cap_h), fc.P(cap_w, 0.0),
                                 CAP_BULGE, 1.0),
            ]),
        ],
        seam_allowance=seam_allowance,
        allowances={"wrist": 8.0},
        notches=[fc.Notch("cap", 0.25, "front cap notch"),
                 fc.Notch("cap", 0.75, "back cap notch (double)")],
        grainline=fc.Grainline(fc.P(cap_w * 0.5, -24.0), fc.P(cap_w * 0.5, -ln + 24.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve (cut 2 mirrored, forearm buttons)",
    )


FRONT = build_front()
BACK = build_back()
SIDE = build_side()

# MEASURE the armscye off the built panels, then SOLVE the sleeve cap against it.
ARMSCYE = FRONT.edge("armhole").length() + BACK.edge("armhole").length()
CAP_TARGET = ARMSCYE + SLEEVE_EASE
CAP_BULGE, CAP_MEASURED = _solve_cap_bulge(ARMSCYE * 0.60,
                                           ARMHOLE_DEPTH * 0.70, CAP_TARGET)

# The hem is MEASURED, never assumed: the built panel hems plus the built gore bases.
HEM_MEASURED = (FRONT.edge("hem").length() * 2.0        # front panel is cut on the fold
                + BACK.edge("hem").length() * 2.0       # back panel likewise
                + SIDE.edge("hem").length() * 2.0       # two side panels
                + GORE.edge("base").length() * 4.0)     # four gores


def build():
    pattern = fc.PatternSet("cotehardie")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(FRONT)
    if everything or target_piece == "back":
        pattern.add(BACK)
    if everything or target_piece == "side":
        pattern.add(SIDE)
    if everything or target_piece == "gore":
        pattern.add(GORE)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())

    if everything:
        # The body seams: front to side, side to back. All panels share the same shaped
        # side-edge construction, so paired seams balance exactly.
        pattern.declare_seam(("front", "side"), ("side", "side"), tol=1.0)
        pattern.declare_seam(("side", "side"), ("back", "side"), tol=1.0)
        # The shoulder seams.
        pattern.declare_seam(("front", "shoulder"), ("side", "shoulder"), tol=1.0)
        # The set-in sleeve, eased into the front+back armscye.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.5, ease=SLEEVE_EASE)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)   # gores nest poorly; honest 62%
    n_eyelets = N_EYELETS
    pattern.bom = [
        {"item": "wool broadcloth (fulled, unlined or linen-lined)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker — gores nest poorly and that is honest, "
                 "not pessimistic. Period wool is fulled so cut edges barely fray."},
        {"item": "lacing eyelets (Yantra4D garment-eyelet)", "qty": n_eyelets * 2,
         "unit": "count",
         "note": f"{n_eyelets} per side seam at {eyelet_pitch:.0f} mm pitch. Period eyelets "
                 f"are worked with linen thread over an awl-pierced hole — the fibres are "
                 f"PUSHED aside, never cut. Set metal eyelets are the modern equivalent."},
        {"item": "lacing cord", "qty": round(WD * 4.0), "unit": "mm_length",
         "note": "spiral-laced at the side seam; this is how a garment with no elastic "
                 "and no zip gets close enough to fit."},
        {"item": "forearm buttons", "qty": N_FOREARM_BUTTONS * 2, "unit": "count",
         "note": "small buttons closing the sleeve from elbow to wrist, opposed by worked "
                 "thread loops."},
        {"item": "linen thread", "qty": 1, "unit": "spool",
         "note": "the gore seams take the skirt's whole weight — backstitch by hand or "
                 "use a short machine stitch, and finish the seam allowances."},
    ]
    pattern.metadata = {
        "fc300_rank": 270,
        "family": "costume_historical",
        "period": "c. 1340–1400 (mid-to-late 14th century)",
        "fabric_hint": "lana-melton-abrigo",
        "silhouette_note": "Close through the torso, full at the hem, with NO waist seam. "
            "The transition is made entirely by gores inserted into the seams below the hip "
            "— the defining medieval solution, and the thing a modern draft usually gets "
            "wrong by cutting a bodice and a skirt and joining them at the waist.",
        "construction_note": "Four body panels shaped by the seams themselves; no darts, no "
            "waist seam. Side lacing through worked eyelets provides the close fit.",
        "hardware": "lacing eyelets via Yantra4D (notion.hardware_ref -> garment-eyelet); "
            "the eyelet pitch drives barrel_h/inner_dia — the dimensional handshake.",
        "solved": {
            "gore_side_measured_mm": round(GORE_SIDE, 2),
            "body_slit_mm": round(GORE_SIDE, 2),
            "gore_apex_above_hem_mm": round(Y_GORE_TOP, 1),
            "hem_measured_mm": round(HEM_MEASURED, 1),
            "armscye_measured_mm": round(ARMSCYE, 2),
            "cap_measured_mm": round(CAP_MEASURED, 2),
            "cap_residual_mm": round(CAP_MEASURED - (ARMSCYE + SLEEVE_EASE), 4),
            "cap_bulge_solved": round(CAP_BULGE, 5),
            "shoulder_seam_mm": round(FRONT_SHOULDER_LEN, 2),
            "hem_sweep_note": "the hem is the SUM of the built panel hems and the built gore "
                              "bases, measured off the polygons — not gown_length times a "
                              "flare factor.",
            "note": "each body panel's seam carries a straight slit cut to the gore side's "
                    "MEASURED length, so the inserted gore balances by construction.",
        },
    }
    return pattern


result = build()
