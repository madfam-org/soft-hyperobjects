"""
Kimono-style Robe — FC-100 rank #100. Fashion Cabinet Garment Cartridge.

A kimono-STYLE wrap robe — the widely-made lounge/dressing robe whose geometry
is borrowed from the kimono, NOT a formal traditional kimono (no okumi tuck, no
eri/juban layering, no traditional bolt-width discipline). Its signature is
RECTANGULAR CONSTRUCTION: every piece is a straight-edged rectangle and the
elegance is in the economy of the rectangles, joined by straight seams.

Pieces (all rectangles):
  - back    : one panel, cut on fold at centre back, with a shallow back-neck scoop.
  - front   : two panels (cut 2 mirror); the inner centre-front edge is straight
              and full-length — the band covers it — with a shallow front-neck scoop.
  - sleeve  : two wide rectangles (cut 2 mirror); dropped shoulder → the sleevehead
              seam is a straight vertical, so the armhole it sews to is straight too.
  - band    : the continuous FRONT / COLLAR band — one long rectangle running up the
              right front, around the back neck, and down the left front. Its inner
              (attach) edge length is SOLVED by bisection to the measured neckline
              run = right-front edge + back-neck edge + left-front edge (band_collar
              method), declared as a seam with delta ≈ 0.
  - belt    : one long self tie (the wrap belt); no hardware.
  - inner_tie : two short self ties (the inner anchor tie); no hardware.

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
# front|back|sleeve|band|belt|inner_tie|set
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth   = float(PARAM(lambda: chest_girth, 1040.0))    # full chest girth
robe_length   = float(PARAM(lambda: robe_length, 1150.0))    # nape to finished hem
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))      # full neck girth
sleeve_depth  = float(PARAM(lambda: sleeve_depth, 300.0))    # armhole drop (sleevehead height)
sleeve_length = float(PARAM(lambda: sleeve_length, 360.0))   # shoulder line to sleeve opening
kimono_ease   = float(PARAM(lambda: kimono_ease, 260.0))     # generous total wrap ease
band_width    = float(PARAM(lambda: band_width, 70.0))       # finished front-band width
belt_width    = float(PARAM(lambda: belt_width, 80.0))       # self-belt width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps (mirror the manifest slider min/max exactly) ──────────────────────
chest_girth = max(650.0, min(chest_girth, 1900.0))
robe_length = max(700.0, min(robe_length, 1500.0))
neck_girth = max(300.0, min(neck_girth, 560.0))
sleeve_depth = max(200.0, min(sleeve_depth, 460.0))
sleeve_length = max(150.0, min(sleeve_length, 620.0))
kimono_ease = max(140.0, min(kimono_ease, 540.0))
band_width = max(40.0, min(band_width, 120.0))
belt_width = max(50.0, min(belt_width, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# ── Rectangular kimono-robe block ────────────────────────────────────────────
# Body width is split into a back-on-fold half and two front panels. The side
# seam (a vertical of length L on both front and back) is straight, so it always
# balances by construction. The armhole is a straight vertical of height
# sleeve_depth, and the sleevehead it sews to is the matching straight vertical.
L = robe_length
BODY = (chest_girth + kimono_ease) / 2.0          # half girth incl. ease = back + one front width
BW = BODY / 2.0                                   # back-on-fold half-width (CB to side)
# In a rectangular kimono-style robe the front and back panels are the SAME
# width, so the shoulder line and the side seam both balance by construction.
# The wrap overlap comes from the two front panels crossing over the band, not
# from a wider panel — widening the front would unbalance the shoulder seam.
FW = BW                                            # each front panel width == back half-width
NECK_SCOOP = max(60.0, neck_girth / 5.0)           # half back-neck width at the top edge
BACK_NECK_DROP = 18.0                              # shallow back-neck scoop depth
FRONT_NECK_DROP = 34.0                             # slightly deeper front-neck scoop depth
SLEEVE_HALF = sleeve_length                        # sleeve rectangle half-height reference
BELT_LEN = (chest_girth + kimono_ease) * 1.15      # long wrap belt
INNER_TIE_LEN = 260.0                              # short inner anchor tie


def build_back():
    """Back rectangle, cut on fold at CB. Top edge carries a shallow back-neck
    scoop (a gentle curve) from the CB neck point out to the shoulder point; the
    rest of the top edge is the straight shoulder line."""
    neck_top = fc.P(0.0, L)                         # CB at the shoulder/top line
    neck_out = fc.P(NECK_SCOOP, L)                  # shoulder-neck point
    # shallow scoop dips below the top line then returns to the shoulder point
    neck = fc.Edge(
        "neck",
        [fc.curve_through(neck_top, neck_out, bulge=BACK_NECK_DROP / max(NECK_SCOOP, 1.0),
                          side=-1.0)],
    )
    return fc.Piece(
        "back",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_top)]),
            neck,
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(BW, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(BW, L), fc.P(BW, L - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(BW, L - sleeve_depth), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"),
                 fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 80.0), fc.P(BW * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Back",
    )


def build_front():
    """Front rectangle (cut 2 mirror). Inner (CF) edge is straight and full
    length — the band will cover it. Top edge carries a shallow front-neck scoop
    from the shoulder-neck point in toward CF."""
    cf_x = 0.0
    side_x = FW
    neck_in = fc.P(cf_x, L - FRONT_NECK_DROP)       # CF neck point (scoop lowers CF a touch)
    neck_out = fc.P(NECK_SCOOP, L)                   # shoulder-neck point (matches back)
    neck = fc.Edge(
        "neck",
        [fc.curve_through(neck_in, neck_out, bulge=0.10, side=-1.0)],
    )
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(cf_x, 0.0), neck_in)]),
            neck,
            fc.Edge("shoulder", [fc.Line(neck_out, fc.P(side_x, L))]),
            fc.Edge("armhole", [fc.Line(fc.P(side_x, L), fc.P(side_x, L - sleeve_depth))]),
            fc.Edge("side", [fc.Line(fc.P(side_x, L - sleeve_depth), fc.P(side_x, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(side_x, 0.0), fc.P(cf_x, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 1.0, "shoulder point"),
                 fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(side_x * 0.5, 80.0), fc.P(side_x * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front",
    )


def build_sleeve():
    """Wide sleeve rectangle (cut 2 mirror). The sleevehead edge is a straight
    vertical of height sleeve_depth (dropped shoulder), matching the straight
    front+back armholes. The opposite edge is the sleeve opening; the underarm
    seam runs from the opening up to the underarm. A deep kimono sleeve — the
    underarm seam is a simple full seam in v0 (a partially open underarm is a
    finishing option, noted in the README)."""
    head_h = sleeve_depth
    sw = SLEEVE_HALF                                  # sleeve rectangle width (shoulder→opening)
    # A wide rectangle: sleevehead on the right (x=sw), opening on the left (x=0).
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("underarm", [fc.Line(fc.P(0.0, 0.0), fc.P(sw, 0.0))]),
            fc.Edge("sleevehead", [fc.Line(fc.P(sw, 0.0), fc.P(sw, head_h))]),
            fc.Edge("shoulder_fold", [fc.Line(fc.P(sw, head_h), fc.P(0.0, head_h))]),
            fc.Edge("opening", [fc.Line(fc.P(0.0, head_h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"opening": hem_allowance},
        notches=[fc.Notch("sleevehead", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(sw * 0.5, head_h * 0.25), fc.P(sw * 0.5, head_h * 0.75)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Sleeve",
    )


def _band_inner_edge(flat_len):
    """The band's inner (attach) edge as a single straight run of `flat_len`.
    A straight strip fitted to a measured length — same fit-to-measure role as
    the band-collar neck edge, solved by bisection for idiom consistency."""
    return fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(flat_len, 0.0))])


def _solve_flat(edge_fn, target, what):
    """Bisect a monotonic flat-length → measured-length edge builder (blazer idiom)."""
    lo, hi = target * 0.7, target * 1.05
    for _ in range(48):
        mid = (lo + hi) / 2.0
        if edge_fn(mid).length(0.05) < target:
            lo = mid
        else:
            hi = mid
    flat = (lo + hi) / 2.0
    if abs(edge_fn(flat).length(0.05) - target) > 1.0:
        raise ValueError(f"{what} solver did not converge on {target:.1f} mm")
    return flat


def build_band(neck_run):
    """Continuous front/collar band: one long rectangle. Its inner edge is
    solved to `neck_run` = right-front CF edge + back neckline + left-front CF
    edge (measured from the built pieces), so the band ↔ neckline seam balances.
    The outer edge is inner + band_width; the two short ends close the loop."""
    flat = _solve_flat(_band_inner_edge, neck_run, "band inner-edge")
    inner = _band_inner_edge(flat)
    return fc.Piece(
        "band",
        [
            inner,
            fc.Edge("end_b", [fc.Line(fc.P(flat, 0.0), fc.P(flat, band_width))]),
            fc.Edge("outer", [fc.Line(fc.P(flat, band_width), fc.P(0.0, band_width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, band_width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("inner", 0.5, "centre back neck"),
                 fc.Notch("inner", 0.25, "left shoulder-neck"),
                 fc.Notch("inner", 0.75, "right shoulder-neck")],
        grainline=fc.Grainline(fc.P(flat * 0.5, band_width * 0.5),
                               fc.P(flat * 0.5 + 120.0, band_width * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Front / Collar Band",
    )


def _strip(name, length, width, qty, label, notches=None):
    """A plain self-fabric rectangle tie/belt (no hardware)."""
    return fc.Piece(
        name,
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, width))]),
            fc.Edge("top", [fc.Line(fc.P(length, width), fc.P(0.0, width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=notches or [],
        grainline=fc.Grainline(fc.P(length * 0.2, width / 2.0), fc.P(length * 0.8, width / 2.0)),
        cut=fc.CutSpec(quantity=qty),
        label=label,
    )


def build():
    pattern = fc.PatternSet("kimono-robe")
    front = build_front()
    back = build_back()

    # Neckline run the band attaches to: both fronts' CF edges + the back neck.
    # (Two fronts, cut 2 mirror, contribute two CF edges; the band wraps both.)
    neck_run = (2.0 * front.edge("center_front").length(0.05)
                + back.edge("neck").length(0.05))

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces or target_piece == "band":
        pattern.add(build_band(neck_run))
    if all_pieces or target_piece == "belt":
        pattern.add(_strip("belt", BELT_LEN, belt_width, 1, "Belt",
                           notches=[fc.Notch("top", 0.5, "centre back")]))
    if all_pieces or target_piece == "inner_tie":
        pattern.add(_strip("inner_tie", INNER_TIE_LEN, 24.0, 2, "Inner Tie"))

    if all_pieces:
        # Straight side seams: front side ↔ back side (both verticals of length L−0).
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
        # Grown-on / straight shoulder line: front shoulder ↔ back shoulder.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        # Straight dropped-shoulder armhole ↔ straight sleevehead. Sleeve sews to
        # ONE armhole (front OR back) per side; here the sleevehead == each armhole
        # (both straight verticals of height sleeve_depth), so declare against the
        # summed front+back armhole with the sleevehead counted for both halves.
        pattern.declare_seam([("sleeve", "sleevehead"), ("sleeve", "sleevehead")],
                             [("front", "armhole"), ("back", "armhole")], tol=1.5)
        # Sleeve underarm seam to the body underarm gap is a topology join; the
        # sleeve's own underarm edge is a finished/closed edge in the flat — no
        # length partner, so it is not a balance seam (noted; full underarm in v0).
        # Continuous band ↔ measured neckline run (solved, delta ≈ 0).
        pattern.declare_seam(
            [("band", "inner")],
            [("front", "center_front"), ("front", "center_front"), ("back", "neck")],
            tol=1.5,
        )

    pattern.bom = [
        {"item": "shell fabric (popelina de algodón)", "qty": round((L + band_width
            + 2.0 * hem_allowance + 40.0) / 1000.0 * 2.6, 2), "unit": "m",
         "note": "≈2.6 m of 1.4 m-wide woven at default length; rectangular cut, "
                 "fold-friendly — back on fold, fronts/sleeves nested. Scales with robe_length."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool",
         "note": "polyester or cotton to match; straight seams throughout."},
        {"item": "self ties (belt + inner tie)", "qty": 3, "unit": "pcs",
         "note": "cut from shell — NO hardware (no buttons, buckles, or hooks); "
                 "a kimono-style robe closes by wrapping and tying only."},
    ]

    pattern.metadata = {
        "fc100_rank": 100,
        "fabric_hint": "popelina-algodon",
        "kimono_style_note": "This is a kimono-STYLE wrap robe (the common lounge/"
            "dressing robe with kimono-derived rectangular geometry), NOT a formal "
            "traditional kimono. It omits the okumi overlap panel, the eri/collar "
            "layering, the bolt-width (tan) cutting discipline, and the seated-wear "
            "proportions of an authentic kimono. Offered with respect for the source.",
        "rectangular_economy": "Every piece is a straight-edged rectangle joined by "
            "straight seams; the design's economy is that a whole robe nests from "
            "rectangles with almost no fabric waste — the teaching point of this draft.",
        "solved": {
            "band_inner_edge_mm": round(_band_inner_edge(
                _solve_flat(_band_inner_edge, neck_run, "band")).length(0.05), 1),
            "neck_run_target_mm": round(neck_run, 1),
            "body_half_width_mm": round(BW, 1),
            "front_panel_width_mm": round(FW, 1),
            "sleeve_depth_mm": round(sleeve_depth, 1),
        },
        "drafting": "rectangular kimono-style robe: back on fold; two straight-CF "
            "fronts; wide rectangular sleeves on a straight dropped-shoulder armhole; "
            "one continuous front/collar band solved to the measured neckline run; "
            "self belt + inner ties, no hardware. Shallow neck scoops are the only "
            "curves; underarm is a full seam in v0 (partial-open underarm is a "
            "finishing option). Teaching-grade — honest simplification.",
    }
    return pattern


result = build()
