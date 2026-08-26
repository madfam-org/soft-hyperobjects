"""
Huipil (three-web blouse) — Fashion Cabinet Cartridge (FC-400 #397; heritage_global, Mesoamerican).

The huipil is one of the oldest and most widely worn Indigenous garments of Mexico and Central
America: a rectangular tunic assembled from straight-woven webs. The FC-300 `huipil` is a
two-web tunic-length garment; THIS is the classic THREE-WEB BLOUSE-length huipil of the Maya and
other highland peoples — a centre web with the neck opening flanked by two side webs, joined by
the decorative join-stitch (randa), and hemmed at the hip rather than the knee. It is a distinct
member of the huipil family, and it is drafted around the two facts that make a three-web huipil
what it is:

  1. THREE WEBS, JOINED BY THE RANDA — AND THE WEB WIDTH IS REAL. The garment is three loom
     widths sewn side by side: a centre web and two side webs. The backstrap or treadle loom's
     usable `web_width` is a real dimension, so the body width is `3 * web_width` and this
     cartridge solves it from that, not from a chest measurement. The two vertical joins are the
     RANDA — a decorative insertion-stitch join that IS part of the garment's identity; this
     cartridge marks the randa lines but draws no randa motif (the stitch pattern is the maker's).

  2. THE NECK IS CUT INTO THE CENTRE WEB ONLY, AND THE GARMENT IS OTHERWISE UNCUT. The boat or
     round neck opening is the only cut; everything else is straight webs used whole, folded at
     the shoulder. So the cartridge cuts the neck and nothing else, honouring the loom-web economy.
     The sleeves are the web overhang past the body (a short cap), not a set-in sleeve.

Pieces: centre_web (with the neck), side_web (cut 2). Made to measure to the loom web width,
blouse length and the neck opening; the body width is solved from the web width.

Cultural note (stated): the huipil is Indigenous Mesoamerican dress; its woven designs and the
randa are specific to communities and weavers and carry identity and meaning. This cartridge
draws NO woven design and NO randa pattern — it supplies the web dimensions and the neck, and the
weave and the join-stitch are the weaver's.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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

web_width = float(PARAM(lambda: web_width, 340.0))          # loom web usable width
blouse_length = float(PARAM(lambda: blouse_length, 560.0))  # shoulder fold to hem
neck_width = float(PARAM(lambda: neck_width, 220.0))        # boat-neck span
neck_drop_front = float(PARAM(lambda: neck_drop_front, 60.0))
neck_drop_back = float(PARAM(lambda: neck_drop_back, 20.0))
sleeve_overhang = float(PARAM(lambda: sleeve_overhang, 120.0))  # cap past the body
randa_width = float(PARAM(lambda: randa_width, 12.0))       # join-stitch band width (marking)
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
web_width = max(200.0, min(web_width, 500.0))
blouse_length = max(360.0, min(blouse_length, 900.0))
neck_width = max(120.0, min(neck_width, 320.0))
neck_drop_front = max(20.0, min(neck_drop_front, 160.0))
neck_drop_back = max(0.0, min(neck_drop_back, 100.0))
sleeve_overhang = max(0.0, min(sleeve_overhang, 300.0))
randa_width = max(4.0, min(randa_width, 40.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# the neck cannot be wider than the centre web
neck_width = min(neck_width, web_width - 40.0)

# ── The three-web solver ─────────────────────────────────────────────────────
# The huipil is folded at the shoulder. Each web is drafted as a HALF (front), cut on the fold
# at the shoulder (top edge = fold). The body width is three webs.
BODY_WIDTH = 3.0 * web_width
H = blouse_length                        # shoulder fold to hem (drafted half)


def build_centre_web():
    """The centre web (cut 1 on the fold at the shoulder): a web_width panel with the boat neck
    scooped into the top (shoulder-fold) edge. The front neck drops more than the back — drawn
    here as the front scoop; the back is the shallower marking.
    """
    w = web_width
    cx = w / 2.0
    nl = cx - neck_width / 2.0
    nr = cx + neck_width / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side_r", [fc.Line(fc.P(w, 0.0), fc.P(w, H))]),
        fc.Edge("shoulder_r", [fc.Line(fc.P(w, H), fc.P(nr, H))]),
        fc.Edge("neck", [fc.Bezier(fc.P(nr, H),
                                   fc.P(nr - neck_width * 0.18, H - neck_drop_front),
                                   fc.P(nl + neck_width * 0.18, H - neck_drop_front),
                                   fc.P(nl, H))]),
        fc.Edge("shoulder_l", [fc.Line(fc.P(nl, H), fc.P(0.0, H))]),
        fc.Edge("side_l", [fc.Line(fc.P(0.0, H), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("back neck (shallower, marked)",
                    [fc.P(nl, H - neck_drop_back), fc.P(nr, H - neck_drop_back)],
                    kind="marking"),
    ]
    return fc.Piece(
        "centre_web", edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "side_l": 0.0, "side_r": 0.0, "neck": 0.0},
        notches=[fc.Notch("hem", 0.5, "centre"),
                 fc.Notch("side_r", 0.5, "randa join / underarm")],
        grainline=fc.Grainline(fc.P(cx, H * 0.12), fc.P(cx, H * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="shoulder_r"),
        label="Centre web (with neck, cut 1 on fold)")


def build_side_web():
    """A side web (cut 2 on the fold at the shoulder): a plain web_width panel joined to the
    centre web by the randa. Its overhang past the body is the short sleeve cap.
    """
    w = web_width
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("selvedge", [fc.Line(fc.P(w, 0.0), fc.P(w, H))]),
        fc.Edge("shoulder", [fc.Line(fc.P(w, H), fc.P(0.0, H))]),
        fc.Edge("randa_join", [fc.Line(fc.P(0.0, H), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("randa band", [fc.P(randa_width * 0.5, 0.0),
                                   fc.P(randa_width * 0.5, H)], kind="marking"),
        fc.Internal("underarm (side seam closes below)",
                    [fc.P(w, H - sleeve_overhang), fc.P(w - 20.0, H - sleeve_overhang)],
                    kind="marking"),
    ]
    return fc.Piece(
        "side_web", edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "selvedge": 0.0},
        notches=[fc.Notch("hem", 0.5, "centre"),
                 fc.Notch("randa_join", 0.5, "randa match")],
        grainline=fc.Grainline(fc.P(w * 0.5, H * 0.12), fc.P(w * 0.5, H * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="shoulder", mirror=True),
        label="Side web (randa-joined, cut 2 on fold)")


def build():
    pattern = fc.PatternSet("huipil-blouse")
    centre = build_centre_web()
    side = build_side_web()

    picked = {"centre_web": centre, "side_web": side}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        pattern.add(centre)
        pattern.add(side)
        # The randa joins the centre web's sides to the side webs' randa edges. Both are the
        # full height, equal by construction.
        pattern.declare_seam(("centre_web", "side_l"), ("side_web", "randa_join"), tol=1.0)
        pattern.declare_seam(("centre_web", "side_r"), ("side_web", "randa_join"), tol=1.0)

    fabric_width = web_width
    total_web_run = (2.0 * H) * 3.0
    pattern.bom = [
        {"item": "backstrap or treadle-loom cotton (three webs)",
         "qty": round(total_web_run / 10.0) * 10, "unit": "mm_length",
         "note": f"three webs x {2.0 * H:.0f} mm at {fabric_width:.0f} mm web width; body width "
                 f"{BODY_WIDTH:.0f} mm. The webs are woven with the weaver's own design — this "
                 "cartridge supplies dimensions, NOT a weave."},
        {"item": "randa thread (join-stitch)", "qty": 1, "unit": "set",
         "note": "the two vertical joins are the randa, a decorative insertion stitch that is "
                 "part of the garment's identity; the stitch pattern is the maker's, not drawn "
                 "here."},
        {"item": "neck binding + thread", "qty": 1, "unit": "set",
         "note": "the boat/round neck is the ONLY cut; bind it. Everything else is whole webs."},
    ]
    pattern.metadata = {
        "fc400_rank": 397, "family": "heritage_global", "fabric_hint": "manta-cruda",
        "tradition": "Mesoamerican (Maya & highland peoples) — the three-web blouse huipil",
        "silhouette_note": "A blouse-length huipil of THREE loom webs — a centre web carrying the "
            "neck flanked by two side webs, joined by the randa, folded at the shoulder, with a "
            "short sleeve overhang. The neck is the only cut; the rest is whole webs.",
        "hardware": "none — the huipil is a pull-over with no fastening.",
        "no_cut": "Only the neck is cut into the centre web; the garment is otherwise whole loom "
            "webs used entire, honouring the web economy.",
        "solved": {
            "web_width_mm": round(web_width, 1),
            "body_width_mm": round(BODY_WIDTH, 1),
            "blouse_length_mm": round(blouse_length, 1),
            "neck_width_mm": round(neck_width, 1),
            "sleeve_overhang_mm": round(sleeve_overhang, 1),
            "note": "the body width is solved as THREE loom webs (3 * web_width), not from a "
                    "chest measurement; the fit is the web width and the drape.",
        },
        "cultural_note": "The huipil is Indigenous Mesoamerican dress; its woven designs and the "
            "randa are specific to communities and weavers and carry identity and meaning. This "
            "cartridge draws NO woven design and NO randa pattern — it supplies the web dimensions "
            "and the neck, and the weave and the join-stitch are the weaver's.",
        "drafting": "Made to measure to the loom web width, blouse length and neck opening; the "
            "body width is three webs and only the neck is cut.",
    }
    return pattern


result = build()
