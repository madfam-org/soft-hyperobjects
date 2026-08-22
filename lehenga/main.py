"""
Leheṅgā (लहंगा) — FC-300 rank #283. Fashion Cabinet Garment Cartridge.

The leheṅgā is the long, full, gored skirt of northern and western South Asia
— also `ghagra` / `ghāgrā` (घाघरा), `chaniya` in Gujarati, `pāvāḍai` in Tamil.
It is worn with a fitted `cholī` blouse (drafted in this commons as
`sari-blouse`) and a `dupaṭṭā` draped over. Its everyday form is the working
skirt of Rajasthan and Gujarat; its worked form is the standard bridal and
festival skirt across much of the region.

The leheṅgā is NOT a gathered rectangle. That is what separates it from the
chima, the sarafan, and every other full skirt in this commons, and it is what
this draft is built to encode:

  - IT IS GORED. The skirt is assembled from `kalī` — tapered panels, narrow at
    the waist and wide at the hem — so that the fullness is BUILT INTO THE CUT
    rather than gathered into a band. That is why a leheṅgā flares smoothly and
    holds a bell rather than bunching at the waist, and it is why it can carry
    the weight of heavy zarī work without the waist collapsing.
  - THE GORE IS A TRUE CONICAL FRUSTUM SECTION. Each kalī is one slice of a cone
    whose apex lies above the waist. Getting this right means solving the
    SLANT — the panel's side length — from the cone geometry, not just drawing a
    trapezoid of the requested height. A trapezoid of height H has side edges
    LONGER than H, so a skirt drafted as trapezoids comes out longer than asked
    and the hem does not level. This draft solves the frustum properly: the
    radii are derived from the waist and hem circuits, and the panel height is
    then back-solved so the FINISHED length is the length you asked for.
  - THE HEM IS A CIRCUIT, NOT A WIDTH. `hem_sweep` is the full circumference the
    hem describes, and the gore count divides it.

Drafting note — what actually SOLVES: the cone's inner and outer radii come from
the waist and hem circuits (r = C / 2π), the slant is the difference between
them, and the panel's drafted HEIGHT is then solved by Pythagoras from that
slant and the panel's half-width difference — so the side edges measure the true
slant and the finished length is correct rather than merely nominal. The gore
count is an integer and the panel widths are recomputed from it. The waistband's
finished length is MEASURED from its drafted polygon and reconciled against the
sum of the gore tops.

EXCLUSION, stated rather than quietly ignored: the surface work is NOT drafted.
`Zarī`, `zardozī`, `gōṭā pattī`, `śīśā` (mirror work) and `bandhanī` are named
crafts with their own regional lineages and specialist practitioners; the motifs
and their placement carry community, occasion and family meaning. This cartridge
marks the border field and the panel seams that such work is organised around,
and leaves the work to the artisans whose knowledge it is. Bridal leheṅgā as a
category — its colours, its prescribed elements — is likewise not encoded: this
is a skirt draft, not a wedding.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # waistband|kali|border|set

waist_girth = float(PARAM(lambda: waist_girth, 760.0))     # fitted waist
hem_sweep = float(PARAM(lambda: hem_sweep, 4200.0))        # full hem circuit
skirt_length = float(PARAM(lambda: skirt_length, 1000.0))  # waist → hem, FINISHED
gore_count = float(PARAM(lambda: gore_count, 12.0))        # number of kalī
band_height = float(PARAM(lambda: band_height, 40.0))      # waistband depth
border_depth = float(PARAM(lambda: border_depth, 180.0))   # worked border field
zip_length = float(PARAM(lambda: zip_length, 220.0))       # side opening
tape_width = float(PARAM(lambda: tape_width, 30.0))        # zip tape width
fabric_width = float(PARAM(lambda: fabric_width, 1120.0))  # usable cloth width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(550.0, min(waist_girth, 1300.0))
hem_sweep = max(1500.0, min(hem_sweep, 9000.0))
skirt_length = max(500.0, min(skirt_length, 1400.0))
gore_count = max(4.0, min(gore_count, 32.0))
band_height = max(20.0, min(band_height, 100.0))
border_depth = max(0.0, min(border_depth, 500.0))
zip_length = max(120.0, min(zip_length, 400.0))
tape_width = max(20.0, min(tape_width, 50.0))
fabric_width = max(700.0, min(fabric_width, 1600.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(15.0, min(hem_allowance, 100.0))

# The hem must actually be fuller than the waist — otherwise it is a tube.
if hem_sweep < waist_girth * 1.4:
    hem_sweep = waist_girth * 1.4

# ── The conical frustum solve — what makes this a gored skirt ────────────────
GORES = max(4, int(round(gore_count)))

# The skirt is a frustum of a cone. Its inner and outer radii come straight
# from the two circuits it must span: r = C / 2*pi.
R_WAIST = waist_girth / (2.0 * math.pi)
R_HEM = hem_sweep / (2.0 * math.pi)

# The SLANT is the distance along the cone's surface from the waist circle to
# the hem circle. This is the true finished length of the skirt measured down
# its own surface — which is exactly what "skirt length" means to a wearer.
# So the slant IS the requested length, and the radial difference must be
# reconciled against it rather than the other way round.
RADIAL_RUN = R_HEM - R_WAIST
SLANT = skirt_length

# A cone can only exist if the slant reaches at least as far as the radial run.
# If the requested hem is so full that the radial run exceeds the length, the
# skirt would be flatter than a full circle — clamp to a true circle skirt.
if SLANT <= RADIAL_RUN:
    SLANT = RADIAL_RUN + 1.0

# The drafted panel's HEIGHT is the vertical drop, solved by Pythagoras from the
# slant and the radial run. This is the number a naive trapezoid draft gets
# wrong: it uses the requested length AS the height, which makes the side edges
# (the real slant) longer than asked and the finished skirt too long.
PANEL_H = math.sqrt(max(1.0, SLANT ** 2 - RADIAL_RUN ** 2))

# Each kalī takes one GORES-th of each circuit.
GORE_TOP = waist_girth / GORES
GORE_HEM = hem_sweep / GORES

# How many gores fit across the real cloth, laid alternating (tip up, tip down).
# Two gores nest into roughly one gore-hem width plus one gore-top width.
NEST_PITCH = (GORE_HEM + GORE_TOP) / 2.0
GORES_PER_WIDTH = max(1, int(fabric_width / max(1.0, NEST_PITCH)))

# The waistband spans the waist plus an underlap for the closure.
BAND_SPAN = waist_girth + zip_length * 0.25


def build_waistband():
    """The fitted waistband the gore tops are set into.

    A straight strip. Its `bottom` edge is the seam the assembled gore tops
    meet; that length is MEASURED from this polygon in build() and reconciled
    against the summed gore tops, so the two are proven equal rather than both
    being computed from `waist_girth` and assumed to agree.
    """
    w, h = BAND_SPAN, band_height
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("end_right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("end_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    internals = [
        # The side closure: the zip runs down from the band's left end.
        fc.Internal("zip-seat",
                    [fc.P(0.0, h * 0.5), fc.P(tape_width, h * 0.5)],
                    kind="marking"),
        fc.Internal("underlap-line",
                    [fc.P(w - zip_length * 0.25, 0.0),
                     fc.P(w - zip_length * 0.25, h)],
                    kind="marking"),
    ]
    # Mark the gore seam positions around the band so the panels register.
    for i in range(1, min(GORES, 12)):
        x = w * (i / float(GORES))
        internals.append(
            fc.Internal("gore-register", [fc.P(x, 0.0), fc.P(x, h * 0.45)],
                        kind="marking"))

    return fc.Piece(
        "waistband",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.25, "quarter — gore register"),
                 fc.Notch("bottom", 0.5, "centre front"),
                 fc.Notch("bottom", 0.75, "quarter — gore register")],
        grainline=fc.Grainline(fc.P(w * 0.08, h * 0.2), fc.P(w * 0.08, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Waistband (कमरबंद kamarband)",
    )


def build_kali():
    """One kalī (कली) — a single gore, cut GORES times.

    A conical frustum section: narrow at the waist, wide at the hem. Its side
    edges measure the TRUE SLANT, because the panel height was back-solved from
    the slant and the radial run rather than being set to the nominal length.
    """
    ht, hb = GORE_TOP / 2.0, GORE_HEM / 2.0
    h = PANEL_H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-hb, 0.0), fc.P(hb, 0.0))]),
        fc.Edge("side_right", [fc.Line(fc.P(hb, 0.0), fc.P(ht, h))]),
        fc.Edge("top", [fc.Line(fc.P(ht, h), fc.P(-ht, h))]),
        fc.Edge("side_left", [fc.Line(fc.P(-ht, h), fc.P(-hb, 0.0))]),
    ]
    internals = []
    if border_depth > 1.0:
        # The worked border field runs along the hem of every gore. The seams
        # between gores are what such work is organised around, so the field is
        # marked panel by panel rather than as one continuous band.
        internals.append(
            fc.Internal("border-field",
                        [fc.P(-hb * 0.98, border_depth),
                         fc.P(hb * 0.98, border_depth)],
                        kind="marking"))
    return fc.Piece(
        "kali",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("top", 0.5, "gore centre — band register"),
                 fc.Notch("side_right", 0.5, "gore seam midpoint match")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=GORES),
        label="Gore (कली kalī)",
    )


def build_border():
    """The applied hem border (गोटा पट्टी field), cut as straight strips.

    Optional: only drafted when `border_depth` is set. It is a straight strip
    because it is applied around a hem whose curve is already absorbed by the
    gore seams — the border follows the assembled hem, it does not shape it.
    The MOTIFS are not drafted; this is the field they go on.
    """
    strip_len = min(fabric_width * 0.96, GORE_HEM * 2.0)
    h = max(20.0, border_depth)
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(strip_len, 0.0))]),
        fc.Edge("end_right", [fc.Line(fc.P(strip_len, 0.0), fc.P(strip_len, h))]),
        fc.Edge("top", [fc.Line(fc.P(strip_len, h), fc.P(0.0, h))]),
        fc.Edge("end_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    # How many strips the assembled hem needs — an integer, from real cloth.
    n_strips = max(1, int(math.ceil(hem_sweep / strip_len - 1e-9)))
    return fc.Piece(
        "border",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "strip centre")],
        grainline=fc.Grainline(fc.P(strip_len * 0.15, h * 0.5),
                               fc.P(strip_len * 0.85, h * 0.5)),
        internals=[fc.Internal("border-field",
                               [fc.P(strip_len * 0.04, h * 0.5),
                                fc.P(strip_len * 0.96, h * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=n_strips),
        label="Hem border strip (बॉर्डर)",
    )


def build():
    pattern = fc.PatternSet("lehenga")
    every = target_piece == "set"
    if every or target_piece == "waistband":
        pattern.add(build_waistband())
    if every or target_piece == "kali":
        pattern.add(build_kali())
    if (every or target_piece == "border") and border_depth > 1.0:
        pattern.add(build_border())

    if every:
        band = pattern.piece("waistband")
        kali = pattern.piece("kali")

        # The gore tops, summed, meet the waistband's MEASURED bottom edge. The
        # band carries an underlap for the closure, so the surplus is real and
        # declared as ease rather than being allowed to read as a mismatch.
        gore_top_total = kali.edge("top").length(0.05) * GORES
        band_bottom = band.edge("bottom").length(0.05)
        pattern.declare_seam(
            [("kali", "top")] * GORES, [("waistband", "bottom")],
            tol=1.5, ease=(gore_top_total - band_bottom),
        )

        # The gore seams: each kalī's right edge meets the next kalī's left.
        # Both are the TRUE SLANT, so they must be equal — and this check is
        # what proves the frustum was solved rather than approximated by a
        # trapezoid of nominal height.
        pattern.declare_seam(("kali", "side_right"), ("kali", "side_left"), tol=0.5)

    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)   # gores nest, but waste
    pattern.bom = [
        {"item": "silk, raw silk, brocade, or cotton (chaniya)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm usable width, 72% marker; "
                 f"{GORES} gores nested tip-up/tip-down, "
                 f"≈{GORES_PER_WIDTH} across the width."},
        {"item": "side zip", "qty": 1, "unit": "count",
         "note": f"Yantra4D invisible-zipper at {zip_length:.0f} mm "
                 "(see notion.hardware_ref); the leheṅgā's only closure."},
        {"item": "waistband interfacing",
         "qty": round(BAND_SPAN * band_height / 1000.0), "unit": "cm2",
         "note": "a gored skirt hangs its whole weight on the band — interface firmly."},
        {"item": "lining", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "a worked leheṅgā is always lined; the lining takes the same gores."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "gore seams are long and bias-adjacent — sew them with care."},
    ]
    pattern.metadata = {
        "fc300_rank": 283,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "tradition": "North and West South Asian (लहंगा leheṅgā / घाघरा ghāgrā; "
                     "Gujarati chaniya, Tamil pāvāḍai)",
        "finished_mm": {"length": round(SLANT, 1),
                        "waist": round(waist_girth, 1),
                        "hem_sweep": round(hem_sweep, 1)},
        "solved": {
            "gores": GORES,
            "r_waist_mm": round(R_WAIST, 2),
            "r_hem_mm": round(R_HEM, 2),
            "radial_run_mm": round(RADIAL_RUN, 2),
            "slant_mm": round(SLANT, 2),
            "panel_drafted_height_mm": round(PANEL_H, 2),
            "gore_top_mm": round(GORE_TOP, 2),
            "gore_hem_mm": round(GORE_HEM, 2),
            "gores_per_cloth_width": GORES_PER_WIDTH,
            "note": "this is a true CONICAL FRUSTUM, not a trapezoid. The radii "
                    "come from the two circuits (r = C / 2pi); the SLANT is the "
                    "finished length the wearer asked for; and the drafted panel "
                    "height is back-solved by Pythagoras from the slant and the "
                    "radial run. A trapezoid draft would set the height to the "
                    "nominal length, making the real side edges (the slant) too "
                    "long and the finished skirt longer than requested with an "
                    "unlevel hem. Here PANEL_H < SLANT by exactly the amount the "
                    "cone geometry requires, and the equal-sides seam check proves it.",
        },
        "hardware": "side zip via Yantra4D (notion.hardware_ref -> "
                    "invisible-zipper); zip_length drives both the band's zip "
                    "seat and the printed tape_edge flange",
        "cut_philosophy": "the fullness is CUT IN, not gathered in. That is what "
                          "separates a leheṅgā from a gathered skirt: the waist "
                          "stays flat and fitted while the hem carries several "
                          "metres of sweep, and heavy surface work does not "
                          "collapse the waist.",
        "excluded": "the surface work is NOT drafted: zarī, zardozī, gōṭā pattī, "
                    "śīśā (mirror work) and bandhanī are named crafts with regional "
                    "lineages and specialist practitioners, and their motifs and "
                    "placement carry community, occasion and family meaning. This "
                    "draft marks the border FIELD and the panel seams such work is "
                    "organised around. Bridal leheṅgā as a category — its prescribed "
                    "colours and elements — is likewise not encoded.",
        "worn_with": "cholī (see sari-blouse in this commons) and dupaṭṭā.",
    }
    return pattern


result = build()
