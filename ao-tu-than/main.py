"""
Áo tứ thân (four-panel dress) — Fashion Cabinet Heritage Cartridge (FC-500 #487,
heritage_global; northern Vietnam).

The áo tứ thân is the four-panel long dress of northern Vietnam's countryside — the everyday
and festival dress of the Kinh before the fitted áo dài, worn with the yếm (bib), a wide
waist sash, and the flat nón quai thao hat. Its name is its construction: TỨ THÂN, "four
panels" — two BACK panels seamed at centre back, and two FRONT panels left free as flaps that
are knotted or crossed low over the sash. The cloth was narrow, so each panel is close to a
loom width, and the fit comes from the panels and the sash, not from shaping.

Two facts govern the draft:

  1. IT IS FOUR PANELS, AND THE BACK CENTRE SEAM IS REAL. The garment is not a fold-cut
     body: it is four separate panels. The two back panels are seamed at centre back (so that
     seam is declared and MEASURED against the neck run), and the two front flaps hang free.
     The panel width is a real parameter; a loom too narrow to make the flap overlap is
     reported rather than silently widened.

  2. THE FRONT IS FLAPS, NOT A CLOSED FRONT. The two front panels are worn open, crossed low,
     and tied — there is no buttoned placket up the chest. A small hook-and-eye or tie holds
     the collar band at the throat; the rest is the sash.

Pieces:
  - back   : the back, two panels seamed at CB (drafted as one on-fold half + a CB seam mark).
  - flap   : one front flap (cut 2), the free panel that crosses low.
  - collar : the narrow stand band at the neck, cut to the MEASURED neckline.

Hardware: a throat hook-and-eye — Yantra4D hook-and-eye, LINKED.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # back|flap|collar|set

panel_width = float(PARAM(lambda: panel_width, 380.0))    # loom-width panel
chest_girth = float(PARAM(lambda: chest_girth, 880.0))
dress_length = float(PARAM(lambda: dress_length, 1180.0))  # shoulder to hem
neck_girth = float(PARAM(lambda: neck_girth, 360.0))
collar_height = float(PARAM(lambda: collar_height, 30.0))
shoulder_slope = float(PARAM(lambda: shoulder_slope, 40.0))  # shoulder drop from neck
sleeve_reach = float(PARAM(lambda: sleeve_reach, 480.0))   # one-piece sleeve run past panel
armhole_depth = float(PARAM(lambda: armhole_depth, 260.0))
flap_overlap = float(PARAM(lambda: flap_overlap, 0.55))    # flap reach across (fraction)
closure_span = float(PARAM(lambda: closure_span, 18.0))    # throat hook size
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
panel_width = max(300.0, min(panel_width, 520.0))
chest_girth = max(720.0, min(chest_girth, 1200.0))
dress_length = max(950.0, min(dress_length, 1450.0))
neck_girth = max(300.0, min(neck_girth, 440.0))
collar_height = max(18.0, min(collar_height, 55.0))
shoulder_slope = max(20.0, min(shoulder_slope, 70.0))
sleeve_reach = max(300.0, min(sleeve_reach, 640.0))
armhole_depth = max(200.0, min(armhole_depth, 340.0))
flap_overlap = max(0.35, min(flap_overlap, 0.8))
closure_span = max(10.0, min(closure_span, 34.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# ── The panel solve — four panels, narrow cloth ──────────────────────────────
HALF_PANEL = panel_width / 2.0
NECK_HALF = (neck_girth + 20.0) / 4.0
# The back is two panels (each a loom width) seamed at CB, covering the back and wrapping to
# the sides; the two front flaps each a loom width, crossing low. The body circuit is the two
# back panels plus the two flaps' effective wrap (their overlap fraction).
BODY_CIRCUIT = panel_width * 2.0 + panel_width * 2.0 * flap_overlap
CHEST_EASE = BODY_CIRCUIT - chest_girth
PANEL_SUFFICIENT = CHEST_EASE >= 40.0
FRONT_NECK_DROP = min(NECK_HALF * 0.9 + 10.0, armhole_depth * 0.45)
BACK_NECK_DROP = 18.0
SHOULDER_Y = dress_length
UNDERARM_Y = dress_length - armhole_depth
NECK_HALF = min(NECK_HALF, HALF_PANEL - 20.0)


def build_back():
    """The back, drafted as one on-fold HALF at centre back (the CB seam is declared against
    the neck). One-piece sleeve run out past the panel; no armscye."""
    hp = HALF_PANEL
    p_hem_cb = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hp, 0.0)
    p_underarm = fc.P(hp, UNDERARM_Y)
    p_sleeve_end = fc.P(hp + sleeve_reach, UNDERARM_Y + armhole_depth * 0.35)
    p_sleeve_top = fc.P(hp + sleeve_reach, SHOULDER_Y - shoulder_slope)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y - shoulder_slope * 0.4)
    p_neck_cb = fc.P(0.0, SHOULDER_Y - BACK_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_cb, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end, p_sleeve_top)]),
        fc.Edge("shoulder", [fc.Line(p_sleeve_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.55, SHOULDER_Y - shoulder_slope * 0.4 - 3.0),
                                   fc.P(NECK_HALF * 0.25, p_neck_cb.y + 3.0),
                                   p_neck_cb)]),
        fc.Edge("cb", [fc.Line(p_neck_cb, p_hem_cb)]),
    ]
    internals = [
        fc.Internal("cb-seam", [fc.P(4.0, 30.0), fc.P(4.0, SHOULDER_Y - BACK_NECK_DROP - 20.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "back", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", 0.5, "side mid")],
        grainline=fc.Grainline(fc.P(hp * 0.3, hem_allowance + 30.0),
                               fc.P(hp * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label="Back (two panels seamed at CB), cut on fold",
    )


def build_flap():
    """One front flap (cut 2): a free front panel that crosses low over the sash. Its inner
    edge is the free (crossing) edge; its side seam joins the back."""
    hp = HALF_PANEL
    inner_x = hp * flap_overlap        # how far the flap crosses toward centre
    p_hem_inner = fc.P(0.0, 0.0)
    p_hem_side = fc.P(hp, 0.0)
    p_underarm = fc.P(hp, UNDERARM_Y)
    p_sleeve_end = fc.P(hp + sleeve_reach, UNDERARM_Y + armhole_depth * 0.35)
    p_sleeve_top = fc.P(hp + sleeve_reach, SHOULDER_Y - shoulder_slope)
    p_neck_shoulder = fc.P(NECK_HALF, SHOULDER_Y - shoulder_slope * 0.4)
    p_neck_inner = fc.P(inner_x, SHOULDER_Y - FRONT_NECK_DROP)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_inner, p_hem_side)]),
        fc.Edge("side", [fc.Line(p_hem_side, p_underarm)]),
        fc.Edge("sleeve_under", [fc.Line(p_underarm, p_sleeve_end)]),
        fc.Edge("cuff", [fc.Line(p_sleeve_end, p_sleeve_top)]),
        fc.Edge("shoulder", [fc.Line(p_sleeve_top, p_neck_shoulder)]),
        fc.Edge("neck", [fc.Bezier(p_neck_shoulder,
                                   fc.P(NECK_HALF * 0.6, SHOULDER_Y - shoulder_slope * 0.4 - 6.0),
                                   fc.P(inner_x + (NECK_HALF - inner_x) * 0.3,
                                        p_neck_inner.y + 8.0),
                                   p_neck_inner)]),
        # the free crossing edge, from the inner neck down to the inner hem.
        fc.Edge("crossing", [fc.Line(p_neck_inner, p_hem_inner)]),
    ]
    internals = [
        fc.Internal("tie-point", [fc.P(inner_x * 0.5, UNDERARM_Y - 40.0),
                                  fc.P(inner_x * 0.5 + 30.0, UNDERARM_Y - 40.0)],
                    kind="marking"),
    ]
    return fc.Piece(
        "flap", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.5, "sleeve mid"),
                 fc.Notch("side", 0.5, "side mid")],
        grainline=fc.Grainline(fc.P(hp * 0.3, hem_allowance + 30.0),
                               fc.P(hp * 0.3, UNDERARM_Y - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front flap (free crossing panel)",
    )


# ── The collar band, cut to the MEASURED neckline ────────────────────────────
_BACK = build_back()
_FLAP = build_flap()
BACK_NECK = _BACK.edge("neck").length(0.2)     # one back quarter
FLAP_NECK = _FLAP.edge("neck").length(0.2)     # one front flap neck
NECK_RUN = 2.0 * BACK_NECK + 2.0 * FLAP_NECK
NECK_NAIVE = neck_girth + 20.0


def build_collar():
    """The narrow stand band at the neck, cut to the MEASURED neckline run."""
    ln = NECK_RUN
    h = collar_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", FLAP_NECK / ln, "left shoulder"),
                 fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking"),
                   fc.Internal("throat-hook", [fc.P(ln - closure_span, collar_height * 0.5),
                                               fc.P(ln - 5.0, collar_height * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Neck band (cut to the measured neckline)",
    )


def build():
    pattern = fc.PatternSet("ao-tu-than")
    everything = target_piece == "set"
    if everything or target_piece == "back":
        pattern.add(_BACK)
    if everything or target_piece == "flap":
        pattern.add(_FLAP)
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The side seam: back side to flap side (both a loom width, equal by construction).
        pattern.declare_seam(("back", "side"), ("flap", "side"), tol=1.0)
        pattern.declare_seam(("back", "shoulder"), ("flap", "shoulder"), tol=1.0)
        pattern.declare_seam(("back", "sleeve_under"), ("flap", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("back", "cuff"), ("flap", "cuff"), tol=1.0)
        # THE seam that solves: the collar band against the MEASURED neckline (both back
        # quarters + both flap necks).
        pattern.declare_seam(("collar", "neck_edge"),
                             [("back", "neck"), ("back", "neck"),
                              ("flap", "neck"), ("flap", "neck")], tol=1.5)

    pattern.bom = [
        {"item": "narrow-loom cotton or silk (four panels)", "qty": round(
            (dress_length + hem_allowance) * 4.0 / 10.0) * 10, "unit": "mm_length",
         "note": f"four panels of ~{panel_width:.0f} mm loom width: two seamed at centre "
                 f"back, two hanging free as front flaps. panel_sufficient={PANEL_SUFFICIENT}."},
        {"item": "throat hook-and-eye", "qty": 1, "unit": "count",
         "note": f"{closure_span:.0f} mm hook-and-eye at the collar band; the Yantra4D "
                 f"hook-and-eye solid, linked. The body is held by the waist sash and the "
                 f"crossed, tied flaps, not by a buttoned front."},
        {"item": "waist sash (thắt lưng)", "qty": 1, "unit": "length",
         "note": "the wide sash is the real closure of the dress; worn with a yếm bib beneath."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 487,
        "family": "heritage_global",
        "fabric_hint": "seda-satinada",
        "finished_mm": {
            "panel_width": round(panel_width, 1),
            "dress_length": round(dress_length, 1),
            "sleeve_reach": round(sleeve_reach, 1),
            "collar_height": round(collar_height, 1),
        },
        "solved": {
            "half_panel_mm": round(HALF_PANEL, 2),
            "body_circuit_mm": round(BODY_CIRCUIT, 2),
            "chest_ease_mm": round(CHEST_EASE, 2),
            "panel_sufficient": PANEL_SUFFICIENT,
            "back_neck_quarter_mm": round(BACK_NECK, 3),
            "flap_neck_mm": round(FLAP_NECK, 3),
            "collar_run_mm": round(NECK_RUN, 3),
            "collar_naive_estimate_mm": round(NECK_NAIVE, 3),
            "collar_vs_neck_estimate_mm": round(NECK_RUN - NECK_NAIVE, 3),
            "note": "the áo tứ thân is FOUR PANELS: two back panels seamed at centre back "
                    "(the CB seam declared and the neck matched), and two front flaps that "
                    "hang free and cross low over the waist sash. The body circuit is computed "
                    "from the panel width, so a loom too narrow to make the flap overlap is "
                    "reported as panel_sufficient=false. The neck band is cut to the MEASURED "
                    "neckline (both back quarters + both flap necks). The front is flaps, not "
                    "a buttoned placket; only a throat hook holds the collar.",
        },
        "heritage": {
            "garment": "áo tứ thân — northern Vietnamese four-panel dress",
            "worn": "with the yếm bib, a wide waist sash (thắt lưng), and the flat nón quai "
                    "thao hat; the everyday and festival dress of the Kinh before the áo dài",
            "construction": "four panels (tứ thân) — two seamed at CB, two free front flaps "
                            "crossed low; one-piece sleeves; a narrow stand band",
            "excluded": "no yếm bib or brocade motif is drafted here — the bib is a separate "
                        "garment and the cloth's pattern is the maker's",
        },
        "hardware": "a throat hook-and-eye: Yantra4D hook-and-eye, linked, sized from the "
                    "closure span; the dress is otherwise held by the sash and tied flaps.",
    }
    return pattern


result = build()
