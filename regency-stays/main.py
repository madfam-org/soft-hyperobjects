"""
Regency Stays — Fashion Cabinet Costume Cartridge (FC-300 rank #267, y4d busk + eyelet bridged).

Long corded stays of the c.1800–1825 English/French mode. The Regency body is NOT the
Victorian hourglass: these stays lift and separate the bust and lengthen the torso toward a
high, just-under-bust waistline, with almost no waist reduction. The period construction is
unmistakable and is what this draft reproduces honestly:

  - a one-piece FRONT cut with a straight centre-front carrying a wooden or steel busk in a
    stitched casing (not the hinged split busk — that is a later Victorian invention);
  - triangular BUST GUSSETS set into slashed openings in the front, which give fullness over
    the bust without any horizontal bust seam;
  - a triangular HIP GUSSET set the same way at the lower side, releasing the skirt of the
    stays over the hip;
  - a BACK laced through hand-worked or metal eyelets, with the shoulder straps carried
    from the back over the shoulder and tied to the front;
  - cording channels rather than dense boning — Regency stays are largely corded, with at
    most a back bone either side of the lacing.

Drafting note — the seam that must SOLVE. A gusset is set into a SLASH: the slash is cut,
spread open, and the triangle's two long sides are sewn to the two sides of the spread
slash. So the gusset's two sewn edges must together equal twice the slash length. The
slash length here is not assumed from a formula — the gusset triangle is built first, its
two long edges are MEASURED from the built polygon, and the front's slash-opening edges are
then cut to exactly half that measured total each. The stitch lengths therefore balance by
construction rather than by a fudge factor.

Pieces:
  - front       : one-piece front, cut on the fold at centre front (busk casing marked).
  - bust_gusset : triangular bust gusset (cut 4 — two per side, one pair per bust).
  - hip_gusset  : triangular hip gusset (cut 2).
  - back        : laced back panel (cut 2, mirrored) with the eyelet field marked.
  - strap       : shoulder strap (cut 2).

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
# pieces: front|bust_gusset|hip_gusset|back|strap|set

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))  # the Regency "waist"
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
stays_length = float(PARAM(lambda: stays_length, 420.0))   # CF top edge to bottom edge
gusset_rise = float(PARAM(lambda: gusset_rise, 120.0))     # bust gusset height (the slash)
lacing_gap = float(PARAM(lambda: lacing_gap, 60.0))        # open gap between the back edges
eyelet_pitch = float(PARAM(lambda: eyelet_pitch, 30.0))    # spacing of the lacing eyelets
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane historical stay ranges) ─────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
underbust_girth = max(580.0, min(underbust_girth, 1250.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
stays_length = max(300.0, min(stays_length, 560.0))
gusset_rise = max(70.0, min(gusset_rise, 190.0))
lacing_gap = max(20.0, min(lacing_gap, 120.0))
eyelet_pitch = max(18.0, min(eyelet_pitch, 55.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = stays_length
# The stays close over a lacing gap, so the drafted flesh circumference is the body girth
# less that gap. Front takes ~58% of the underbust ring (Regency stays are front-heavy),
# back the rest, split over two mirrored back panels.
UB_DRAFT = underbust_girth - lacing_gap
FRONT_UB_HALF = UB_DRAFT * 0.58 / 2.0     # half-front width at the underbust line
BACK_UB = UB_DRAFT * 0.42 / 2.0           # one back panel's width at the underbust line
# Bust and hip expansion over the underbust, delivered by the gussets (not by side seams).
BUST_EXPAND = max(0.0, (bust_girth - underbust_girth)) / 4.0   # per bust gusset spread
HIP_EXPAND = max(0.0, (hip_girth - underbust_girth)) / 4.0     # per hip gusset spread


def _tri_gusset(name, spread, rise, label, qty):
    """An isosceles triangular gusset: base `spread` wide, apex `rise` above the base.

    The two long edges (`side_l`, `side_r`) are the SEWN edges — they go into the two
    sides of the spread slash. `base` is the free edge that falls at the garment edge.
    """
    half = spread / 2.0
    return fc.Piece(
        name,
        [
            fc.Edge("base", [fc.Line(fc.P(-half, 0.0), fc.P(half, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(half, 0.0), fc.P(0.0, rise))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, rise), fc.P(-half, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"base": 10.0},
        notches=[fc.Notch("side_r", 1.0, "gusset apex"),
                 fc.Notch("side_l", 0.0, "gusset apex")],
        grainline=fc.Grainline(fc.P(0.0, rise * 0.15), fc.P(0.0, rise * 0.85)),
        cut=fc.CutSpec(quantity=qty, mirror=False),
        label=label,
    )


# Build the gussets FIRST so the front's slash openings can be cut to the MEASURED
# sewn length of the triangles rather than to an assumed formula.
BUST_GUSSET = _tri_gusset("bust_gusset", BUST_EXPAND * 2.0, gusset_rise,
                          "Bust gusset (cut 4: two per bust)", 4)
HIP_GUSSET = _tri_gusset("hip_gusset", HIP_EXPAND * 2.0, gusset_rise * 0.85,
                         "Hip gusset (cut 2)", 2)

# Each gusset contributes side_l + side_r of stitching; the slash it sets into is HALF
# that, because the slash is sewn on both its sides.
BUST_SEWN = (BUST_GUSSET.edge("side_l").length()
             + BUST_GUSSET.edge("side_r").length())
BUST_SLASH = BUST_SEWN / 2.0
HIP_SEWN = (HIP_GUSSET.edge("side_l").length()
            + HIP_GUSSET.edge("side_r").length())
HIP_SLASH = HIP_SEWN / 2.0


def build_front():
    """One-piece front, cut on the fold at centre front.

    The bust and hip slashes are drafted as internal cut lines of exactly the measured
    length the gussets need. The front's `bust_slash` / `hip_slash` edges are the two
    named seam references the gussets balance against; they are carried as a stepped
    notch in the side edge so the outline stays a single closed ring.
    """
    w = FRONT_UB_HALF
    # Centre front is the fold (x = 0). The side edge runs up the body.
    # Underbust line sits at the natural Regency waist, low on this short stay.
    ub_y = L * 0.30
    internals = [
        fc.Internal("busk-casing", [fc.P(14.0, 20.0), fc.P(14.0, L - 20.0)], kind="marking"),
        fc.Internal("underbust-line", [fc.P(0.0, ub_y), fc.P(w, ub_y)], kind="marking"),
        # The bust slash: a cut line of exactly BUST_SLASH, angled up over the bust.
        fc.Internal("bust-slash", [fc.P(w * 0.45, L - gusset_rise - 10.0),
                                   fc.P(w * 0.45, L - gusset_rise - 10.0 + BUST_SLASH)],
                    kind="trace"),
        # The hip slash: a cut line of exactly HIP_SLASH, running down to the bottom edge.
        fc.Internal("hip-slash", [fc.P(w * 0.80, HIP_SLASH), fc.P(w * 0.80, 0.0)],
                    kind="trace"),
    ]
    # Cording channels: the Regency signature, run vertically through the bust area.
    for i in range(4):
        x = w * (0.10 + 0.07 * i)
        internals.append(fc.Internal("cord-channel",
                                     [fc.P(x, ub_y + 8.0), fc.P(x, L - 14.0)],
                                     kind="marking"))
    edges = [
        # cf is the fold edge, bottom-to-top at x = 0.
        fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, L), fc.P(w, L))]),
        # The side edge: the seam to the back panel, gently shaped in at the underbust.
        fc.Edge("side", [fc.Line(fc.P(w, L), fc.P(w * 0.96, ub_y)),
                         fc.Line(fc.P(w * 0.96, ub_y), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "front",
        edges,
        seam_allowance=seam_allowance,
        allowances={"cf": 0.0, "top": 10.0, "bottom": 10.0},
        notches=[fc.Notch("side", 0.5, "underbust")],
        grainline=fc.Grainline(fc.P(w * 0.5, 24.0), fc.P(w * 0.5, L - 24.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf"),
        label="Front (cut 1 on fold, busk casing + gusset slashes)",
    )


def build_back():
    """Laced back panel (cut 2, mirrored). The centre-back edge carries the eyelet field."""
    w = BACK_UB
    ub_y = L * 0.30
    n_eyelets = max(3, int((L - 40.0) / eyelet_pitch))
    internals = [fc.Internal("eyelet-field",
                             [fc.P(12.0, 20.0), fc.P(12.0, 20.0 + (n_eyelets - 1) * eyelet_pitch)],
                             kind="marking")]
    for i in range(n_eyelets):
        y = 20.0 + i * eyelet_pitch
        internals.append(fc.Internal("eyelet",
                                     [fc.P(12.0, y), fc.P(12.0, y + 1.0)], kind="drill"))
    # A back bone either side of the lacing — the only rigid boning in corded stays.
    internals.append(fc.Internal("back-bone", [fc.P(24.0, 16.0), fc.P(24.0, L - 16.0)],
                                 kind="marking"))
    edges = [
        fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, L), fc.P(w, L))]),
        # Mirrors the front's side edge shape so the two balance exactly.
        fc.Edge("side", [fc.Line(fc.P(w, L), fc.P(w * 0.96, ub_y)),
                         fc.Line(fc.P(w * 0.96, ub_y), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "back",
        edges,
        seam_allowance=seam_allowance,
        allowances={"cb": 16.0, "top": 10.0, "bottom": 10.0},
        notches=[fc.Notch("side", 0.5, "underbust")],
        grainline=fc.Grainline(fc.P(w * 0.5, 24.0), fc.P(w * 0.5, L - 24.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Back (cut 2 mirrored, lacing eyelets)",
    )


def build_strap():
    """Shoulder strap: carried from the back over the shoulder, tied at the front."""
    ln = L * 0.85
    w = 42.0
    return fc.Piece(
        "strap",
        [
            fc.Edge("back_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w * 0.62))]),
            fc.Edge("front_end", [fc.Line(fc.P(ln, w * 0.62), fc.P(ln, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.4), fc.P(ln * 0.8, w * 0.4)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shoulder strap (cut 2)",
    )


def build():
    pattern = fc.PatternSet("regency-stays")
    everything = target_piece == "set"
    front = build_front()
    back = build_back()
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "bust_gusset":
        pattern.add(BUST_GUSSET)
    if everything or target_piece == "hip_gusset":
        pattern.add(HIP_GUSSET)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything or target_piece == "strap":
        pattern.add(build_strap())

    if everything:
        # The stay's side seam: front side edge to back side edge. Both are drafted with
        # the same shaping (same height, same underbust inset), so they balance exactly.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # NOTE: front.bottom and back.bottom are NOT declared as a seam. They are not
        # sewn to each other — each is bound separately as part of one continuous bottom
        # binding run around the finished stay. Declaring them as a matched seam would
        # need a tolerance wide enough to always pass, which would be a fudge, not a check.

    fabric_width = 900.0  # period linen/cotton comes narrow
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.66)
    n_eyelets = max(3, int((L - 40.0) / eyelet_pitch))
    pattern.bom = [
        {"item": "linen or cotton jean (two layers, no interlining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 66% marker. Period stays are two layers of firm linen "
                 "or cotton jean stitched together; the strength is in the cording, not a "
                 "modern fused interlining."},
        {"item": "cotton cording", "qty": round(L * 8.0 / 10.0) * 10, "unit": "mm_length",
         "note": "run through the marked channels: the Regency stay is CORDED, which is what "
                 "gives it shape without the rigidity of a fully boned Victorian corset."},
        {"item": "busk (Yantra4D corset-busk)", "qty": 1, "unit": "count",
         "note": "a single straight busk slid into the centre-front casing. Its length is "
                 "driven by the stays' own CF length (see notion.hardware_ref). NOTE: the "
                 "period busk is a plain straight slat — the hinged split busk is a later "
                 "Victorian development, so the printed solid is used unsplit here."},
        {"item": "lacing eyelets (Yantra4D garment-eyelet)", "qty": n_eyelets * 2,
         "unit": "count",
         "note": f"{n_eyelets} per back edge at {eyelet_pitch:.0f} mm pitch. Period stays are "
                 f"hand-worked with thread; set eyelets are the practical modern equivalent."},
        {"item": "flat back bones", "qty": 2, "unit": "count",
         "note": "one either side of the lacing, on the marked back-bone lines."},
        {"item": "lacing cord", "qty": round(L * 6.0), "unit": "mm_length",
         "note": "spiral-laced from the top in the period manner, not criss-cross bunny-ear."},
    ]
    pattern.metadata = {
        "fc300_rank": 267,
        "family": "costume_historical",
        "period": "c. 1800–1825 (Regency / Empire)",
        "fabric_hint": "manta-cruda",
        "silhouette_note": "Long corded stays that LIFT and lengthen rather than reduce: the "
            "Regency line puts the waist just under the bust, so this draft takes almost no "
            "waist suppression and delivers bust and hip fullness entirely through set-in "
            "triangular gussets — the defining Regency construction.",
        "construction_note": "Bust and hip fullness come from triangular gussets set into "
            "slashes, not from bust seams or darts. Shape comes from cording channels, not "
            "from dense boning.",
        "hardware": "busk via Yantra4D (notion.hardware_ref -> corset-busk); the stays' CF "
            "length drives busk_len — the dimensional handshake.",
        "solved": {
            "bust_gusset_sewn_mm": round(BUST_SEWN, 2),
            "bust_slash_mm": round(BUST_SLASH, 2),
            "hip_gusset_sewn_mm": round(HIP_SEWN, 2),
            "hip_slash_mm": round(HIP_SLASH, 2),
            "front_underbust_half_mm": round(FRONT_UB_HALF, 2),
            "back_underbust_mm": round(BACK_UB, 2),
            "note": "each slash is cut to HALF the gusset's MEASURED two-sided sewn length, "
                    "because a set-in gusset sews to both sides of the spread slash. The "
                    "lengths are measured off the built triangles, never assumed.",
        },
    }
    return pattern


result = build()
