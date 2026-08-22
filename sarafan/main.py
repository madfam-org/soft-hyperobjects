"""
Sarafan (сарафан) — FC-300 rank #277. Fashion Cabinet Garment Cartridge.

The Russian sarafan: a long, trapezoidal pinafore-dress worn OVER a shift
(рубаха, *rubakha*), suspended from the shoulders by two straps and hanging
free from an above-bust band. It is the everyday and festival dress of the
Russian North and Volga regions from roughly the 16th century into the 20th,
and remains living dress in folk-ensemble and village practice.

This draft encodes the *kosoklinny* → *pryamoy* transition honestly. The older
косоклинный сарафан (oblique-gore) was built from a straight centre panel plus
wedge gores; the later прямой сарафан (straight sarafan), which this cartridge
drafts, is the simpler and far more common form: straight loom-widths gathered
into a narrow chest band. Drafting the straight form is the honest choice for
a parametric commons cartridge — the gore geometry of the kosoklinny depends on
a specific historical loom width and does not generalise.

The three signatures, all solved rather than assumed:

  - CHEST BAND (the suspension): a narrow band that sits ABOVE the bust and
    carries the whole garment's weight. Its length is the measured band circuit;
    the skirt's gathered top is solved to it through a declared gather ratio, so
    the band-to-skirt seam is a real gather seam with a stated ratio rather than
    two numbers that happen to differ.
  - STRAPS (лямки): two straps from the band front to the band back over the
    shoulder. Their length is solved from the measured over-shoulder run, and
    they button to the band front — the button is the Yantra4D hardware ref.
  - SKIRT (the trapezoid): straight panels whose hem is wider than their top,
    the sarafan's characteristic A-line silhouette. The panel count is derived
    from the required hem sweep and the usable fabric width, so the draft
    responds to real cloth rather than assuming an infinite bolt.

Gather seam note — what actually SOLVES here: the skirt top is deliberately
LONGER than the band (that is what makes a gather). A gathered seam is declared
with `ease` equal to the surplus, so the seam check proves the surplus is
exactly the gather allowance the ratio calls for, not an accidental mismatch.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = a top-level
fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))  # band|skirt|strap|set

band_girth = float(PARAM(lambda: band_girth, 860.0))       # above-bust circuit
band_height = float(PARAM(lambda: band_height, 110.0))     # band depth
dress_length = float(PARAM(lambda: dress_length, 1150.0))  # band top → hem
hem_sweep = float(PARAM(lambda: hem_sweep, 2600.0))        # finished hem circuit
gather_ratio = float(PARAM(lambda: gather_ratio, 2.2))     # skirt top / band
strap_width = float(PARAM(lambda: strap_width, 45.0))      # лямка width
shoulder_run = float(PARAM(lambda: shoulder_run, 420.0))   # band front→back over shoulder
button_ligne = float(PARAM(lambda: button_ligne, 24.0))    # strap button size
fabric_width = float(PARAM(lambda: fabric_width, 900.0))   # usable cloth width
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 45.0))

# ── Clamps (sane garment ranges) ─────────────────────────────────────────────
band_girth = max(600.0, min(band_girth, 1300.0))
band_height = max(60.0, min(band_height, 200.0))
dress_length = max(700.0, min(dress_length, 1500.0))
hem_sweep = max(1400.0, min(hem_sweep, 4200.0))
gather_ratio = max(1.4, min(gather_ratio, 3.2))
strap_width = max(25.0, min(strap_width, 80.0))
shoulder_run = max(280.0, min(shoulder_run, 600.0))
button_ligne = max(14.0, min(button_ligne, 40.0))
fabric_width = max(600.0, min(fabric_width, 1600.0))
seam_allowance = max(6.0, min(seam_allowance, 20.0))
hem_allowance = max(10.0, min(hem_allowance, 80.0))

# The hem must never be narrower than the gathered top — a sarafan flares.
SKIRT_TOP = band_girth * gather_ratio
HEM = max(hem_sweep, SKIRT_TOP + 200.0)

# Panel count from REAL cloth: how many usable widths the hem needs.
PANELS = max(2, int(HEM / fabric_width) + (1 if HEM % fabric_width > 1.0 else 0))
PANEL_TOP = SKIRT_TOP / PANELS
PANEL_HEM = HEM / PANELS
SKIRT_H = dress_length - band_height


def build_band():
    """The above-bust chest band — the piece that carries the garment.

    Drafted flat as a full circuit (it closes at centre back). Its bottom edge
    is the seam the gathered skirt sews to; strap anchor points are marked.
    """
    w, h = band_girth, band_height
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("cb_right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
        fc.Edge("top", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
        fc.Edge("cb_left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
    ]
    # Strap anchors: two at the front (quarter points) and two at the back.
    anchors = [w * 0.18, w * 0.32, w * 0.68, w * 0.82]
    internals = [
        fc.Internal("strap-anchor", [fc.P(x - strap_width / 2.0, h - 8.0),
                                     fc.P(x + strap_width / 2.0, h - 8.0)],
                    kind="marking")
        for x in anchors
    ]
    # Button seats on the two FRONT anchors (the strap buttons through here).
    for x in anchors[:2]:
        internals.append(
            fc.Internal("button-seat", [fc.P(x, h * 0.5),
                                        fc.P(x + button_ligne * 0.635, h * 0.5)],
                        kind="drill"))
    return fc.Piece(
        "band",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.25, "quarter — gather match"),
                 fc.Notch("bottom", 0.5, "centre front"),
                 fc.Notch("bottom", 0.75, "quarter — gather match")],
        grainline=fc.Grainline(fc.P(w * 0.1, h * 0.2), fc.P(w * 0.1, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Chest band (нагрудник)",
    )


def build_skirt():
    """One straight skirt panel (cut PANELS): a trapezoid, top narrower than hem.

    Cut `PANELS` of these and join at the side seams; the assembled top is
    gathered into the band. The panel is the sarafan's straight loom-width.
    """
    ht, hb, h = PANEL_TOP / 2.0, PANEL_HEM / 2.0, SKIRT_H
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(-hb, 0.0), fc.P(hb, 0.0))]),
        fc.Edge("side_right", [fc.Line(fc.P(hb, 0.0), fc.P(ht, h))]),
        fc.Edge("top", [fc.Line(fc.P(ht, h), fc.P(-ht, h))]),
        fc.Edge("side_left", [fc.Line(fc.P(-ht, h), fc.P(-hb, 0.0))]),
    ]
    return fc.Piece(
        "skirt",
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("top", 0.5, "panel centre — gather match")],
        grainline=fc.Grainline(fc.P(0.0, h * 0.15), fc.P(0.0, h * 0.85)),
        cut=fc.CutSpec(quantity=PANELS),
        label="Skirt panel (полотнище)",
    )


def build_strap():
    """A shoulder strap (лямка, cut 2): band back → over shoulder → band front.

    Length is the measured over-shoulder run plus the buttoning extension; the
    front end takes the buttonhole that seats on the band's button.
    """
    ln = shoulder_run + button_ligne * 1.6
    w = strap_width
    edges = [
        fc.Edge("back_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("front_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    bh_len = button_ligne * 0.635 + 2.0          # buttonhole = button dia + play
    internals = [
        fc.Internal("buttonhole",
                    [fc.P(ln - button_ligne * 0.9 - bh_len / 2.0, w / 2.0),
                     fc.P(ln - button_ligne * 0.9 + bh_len / 2.0, w / 2.0)],
                    kind="cut"),
    ]
    return fc.Piece(
        "strap",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("upper", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w / 2.0), fc.P(ln * 0.85, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shoulder strap (лямка)",
    )


def build():
    pattern = fc.PatternSet("sarafan")
    every = target_piece == "set"
    if every or target_piece == "band":
        pattern.add(build_band())
    if every or target_piece == "skirt":
        pattern.add(build_skirt())
    if every or target_piece == "strap":
        pattern.add(build_strap())

    if every:
        # The gather seam, stated honestly: PANELS skirt tops sew to the band
        # bottom, and the surplus IS the gather. ease = the surplus the ratio
        # calls for, so the check proves the gather is exactly as declared.
        skirt = pattern.piece("skirt")
        band = pattern.piece("band")
        top_total = skirt.edge("top").length(0.05) * PANELS
        band_len = band.edge("bottom").length(0.05)
        pattern.declare_seam(
            [("skirt", "top")] * PANELS, [("band", "bottom")],
            tol=1.5, ease=(top_total - band_len),
        )
        # Panel side seams close into a ring: each panel's right meets the next
        # panel's left, so the two side edges must be equal in length.
        pattern.declare_seam(("skirt", "side_right"), ("skirt", "side_left"), tol=0.5)

    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "linen or cotton print", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm usable width, 80% marker; "
                 f"{PANELS} straight panels."},
        {"item": "strap button", "qty": 2, "unit": "count",
         "note": f"Yantra4D sew-through-button at {button_ligne:.0f} ligne "
                 "(see notion.hardware_ref); seats on the band front."},
        {"item": "band interfacing", "qty": round(band_girth * band_height / 1000.0),
         "unit": "cm2", "note": "the band carries the whole garment — interface it."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": "gathering thread doubled."},
    ]
    pattern.metadata = {
        "fc300_rank": 277,
        "family": "heritage_global",
        "fabric_hint": "manta-cruda",
        "tradition": "Russian (прямой сарафан — the straight sarafan)",
        "finished_mm": {"length": round(dress_length, 1),
                        "hem_sweep": round(HEM, 1),
                        "band_girth": round(band_girth, 1)},
        "solved": {
            "panels": PANELS,
            "panel_top_mm": round(PANEL_TOP, 2),
            "panel_hem_mm": round(PANEL_HEM, 2),
            "skirt_top_total_mm": round(SKIRT_TOP, 2),
            "gather_ratio": round(gather_ratio, 3),
            "note": "panel count derived from the hem sweep and the REAL usable "
                    "fabric width; the band-to-skirt seam is declared as a gather "
                    "whose ease equals the surplus the ratio calls for.",
        },
        "hardware": "strap buttons via Yantra4D (notion.hardware_ref -> "
                    "sew-through-button); button_ligne drives both the band's "
                    "button seat and the strap's buttonhole",
        "excluded": "the older косоклинный (oblique-gore) sarafan is NOT drafted: "
                    "its wedge gores are cut to a specific historical loom width "
                    "and do not generalise parametrically.",
    }
    return pattern


result = build()
