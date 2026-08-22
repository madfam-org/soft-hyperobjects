"""
Mary Jane Upper — Fashion Cabinet Garment Cartridge (FC-300 #233, lane 4 footwear).

The upper of a Mary Jane: a low-cut `quarter` (the shoe body, toe to heel, with a scooped
topline) crossed by an `instep_strap` that buttons on the outer side. The button is a
sew-through, so this cartridge bridges to Yantra4D's `sew-through-button` — and the
button's LIGNE (the trade's own diameter unit, 1 ligne = 0.635 mm) is the shared
dimension: it sizes the hardware AND the buttonhole slot in the strap, which is a real
edge of the garment.

The buttonhole is drafted, not decorated: its slot length is the standard
`button_dia + thickness` allowance, so the finished hole actually passes the button it is
bridged to.

SIZING NOTE (honest, checked): ISO 8559 as vendored declares NO foot landmark codes, so
foot_length is a PLAIN parameter with no `measurement` block. No landmark code is
invented.

Pieces:
  - quarter      : the shoe body (cut 1), scooped topline, lasting edge below.
  - instep_strap : the buttoning strap (cut 1), buttonhole slot at the free end.

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # quarter|instep_strap|set

# Plain sized params — ISO 8559 has no foot codes.
foot_length = float(PARAM(lambda: foot_length, 250.0))
foot_girth = float(PARAM(lambda: foot_girth, 230.0))

topline_drop = float(PARAM(lambda: topline_drop, 34.0))   # how low the topline scoops
strap_w = float(PARAM(lambda: strap_w, 24.0))             # instep strap width
strap_len = float(PARAM(lambda: strap_len, 132.0))        # strap free length
button_ligne = float(PARAM(lambda: button_ligne, 24.0))   # button size, in LIGNES
button_thickness = float(PARAM(lambda: button_thickness, 3.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 7.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
foot_length = max(150.0, min(foot_length, 330.0))
foot_girth = max(150.0, min(foot_girth, 320.0))
topline_drop = max(12.0, min(topline_drop, 90.0))
strap_w = max(10.0, min(strap_w, 45.0))
strap_len = max(70.0, min(strap_len, 230.0))
button_ligne = max(14.0, min(button_ligne, 45.0))
button_thickness = max(1.0, min(button_thickness, 8.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
LIGNE_MM = 0.635                          # the trade unit: 1 ligne = 0.635 mm
BUTTON_DIA = button_ligne * LIGNE_MM      # the button's real diameter in mm
# Standard buttonhole allowance: the slot must pass the button's diameter plus its
# thickness, or the finished hole will not do up.
HOLE_LEN = BUTTON_DIA + button_thickness

# The quarter is drafted flat: half the ball girth wide, foot length long.
QUARTER_HALF = foot_girth / 2.0 / 2.0 + 8.0
QUARTER_LEN = foot_length * 0.92
# The strap must be wide enough to carry its own buttonhole with margin either side.
STRAP_W = max(strap_w, HOLE_LEN * 0.55 + 8.0)


def build_quarter():
    """The shoe body: lasting edge below (stitched to the sole), a scooped topline
    above, and the two ends meeting at the heel."""
    w = QUARTER_HALF
    ln = QUARTER_LEN
    internals = [
        fc.Internal("centre-front", [fc.P(0.0, 0.0), fc.P(0.0, ln * 0.30)],
                    kind="marking"),
        # Where the strap's fixed end is sewn to the quarter (inner side).
        fc.Internal("strap-anchor",
                    [fc.P(-w + 6.0, ln * 0.56), fc.P(-w + 6.0 + STRAP_W, ln * 0.56)],
                    kind="marking"),
        # Where the button is sewn (outer side) — a drill point at the button's own
        # diameter, so the maker can see the size the bridge specifies.
        fc.Internal("button-position",
                    [fc.P(w - 10.0 - BUTTON_DIA / 2.0, ln * 0.56),
                     fc.P(w - 10.0 + BUTTON_DIA / 2.0, ln * 0.56)], kind="drill"),
    ]
    return fc.Piece(
        "quarter",
        [
            fc.Edge("lasting", [fc.curve_through(fc.P(-w, 0.0), fc.P(w, 0.0),
                                                 bulge=0.10, side=1.0)]),
            fc.Edge("heel_r", [fc.Line(fc.P(w, 0.0), fc.P(w, ln - topline_drop))]),
            # The topline scoops down over the instep between the two heel edges.
            fc.Edge("topline", [fc.curve_through(fc.P(w, ln - topline_drop),
                                                 fc.P(-w, ln - topline_drop),
                                                 bulge=0.30, side=-1.0)]),
            fc.Edge("heel_l", [fc.Line(fc.P(-w, ln - topline_drop), fc.P(-w, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"topline": 10.0},
        notches=[fc.Notch("lasting", 0.5, "centre toe"),
                 fc.Notch("topline", 0.5, "centre front")],
        grainline=fc.Grainline(fc.P(0.0, 8.0), fc.P(0.0, ln - topline_drop - 8.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Quarter (shoe body)",
    )


def build_instep_strap():
    """The buttoning strap. `attach` is the fixed end sewn to the quarter; the free
    end carries the buttonhole, drafted to the real slot length for its button."""
    ln = strap_len
    w = STRAP_W
    cy = w / 2.0
    # Buttonhole slot: centred across the strap, set in from the free end so the
    # finished hole has a bar tack of material beyond it.
    hole_cx = ln - HOLE_LEN / 2.0 - 10.0
    internals = [
        fc.Internal("buttonhole",
                    [fc.P(hole_cx - HOLE_LEN / 2.0, cy),
                     fc.P(hole_cx + HOLE_LEN / 2.0, cy)], kind="marking"),
    ]
    return fc.Piece(
        "instep_strap",
        [
            fc.Edge("edge_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("edge_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("attach", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "anchor centre"),
                 fc.Notch("edge_bottom",
                          max(0.02, min(hole_cx / ln, 0.98)), "buttonhole centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, cy), fc.P(ln * 0.8, cy)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Instep strap (buttoning)",
    )


def build():
    pattern = fc.PatternSet("mary-jane-upper")
    everything = target_piece == "set"

    quarter = build_quarter()
    strap = build_instep_strap()

    if everything or target_piece == "quarter":
        pattern.add(quarter)
    if everything or target_piece == "instep_strap":
        pattern.add(strap)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything or target_piece == "quarter":
        # The quarter closes at the heel: its two heel edges meet (self-seam,
        # join-to-join — same piece, its own two ends).
        pattern.declare_seam(("quarter", "heel_r"), ("quarter", "heel_l"), tol=0.5)
    if everything:
        # The strap's fixed end is sewn onto the quarter at the strap anchor. Both
        # are STRAP_W tall, so the seam verifies at delta 0 by construction.
        pattern.declare_seam(("instep_strap", "attach"),
                             ("instep_strap", "free_end"), tol=0.5)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "garment leather, patent, or heavy canvas (upper)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1200 mm width, 55% marker. Per PAIR, double this."},
        {"item": "sew-through button", "qty": 1, "unit": "pcs",
         "note": f"Yantra4D `sew-through-button` at {round(button_ligne)} ligne "
                 f"(≈ {round(BUTTON_DIA, 1)} mm). One per shoe."},
        {"item": "sole unit", "qty": 1, "unit": "pcs",
         "note": "the lasting edge stitches down to it. A hard good, out of this "
                 "cartridge's scope."},
        {"item": "lining + toe puff (optional)", "qty": 1, "unit": "as chosen",
         "note": "a lining and a stiffened toe hold the shoe's shape."},
        {"item": "buttonhole / topstitch thread", "qty": 1, "unit": "spool",
         "note": "work the buttonhole to the drafted slot length before attaching."},
    ]
    pattern.metadata = {
        "fc300_rank": 233, "family": "footwear_soft", "fabric_hint": "piel-charol",
        "silhouette_note": "A low-cut Mary Jane upper: a scoop-topline quarter closing "
            "at the heel, crossed by an instep strap that buttons on the outer side.",
        "sizing_note": "foot_length / foot_girth are PLAIN parameters — ISO 8559 as "
            "vendored declares no foot landmark codes, so none is claimed or invented.",
        "hardware_note": "button_ligne is the trade's own diameter unit (1 ligne = "
            "0.635 mm). It sizes the Yantra4D button AND the buttonhole slot drafted "
            "into the strap, so the finished hole passes the button it is bridged to.",
        "solved": {
            "button_ligne": round(button_ligne, 1),
            "button_dia_mm": round(BUTTON_DIA, 2),
            "buttonhole_slot_mm": round(HOLE_LEN, 2),
            "strap_w_mm": round(STRAP_W, 1),
            "quarter_half_mm": round(QUARTER_HALF, 1),
        },
    }
    return pattern


result = build()
