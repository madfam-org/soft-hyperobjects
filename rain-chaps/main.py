"""
Rain Chaps — Fashion Cabinet Garment Cartridge (FC-300 #237, technical & outdoor).

Rain chaps are rain trousers with the seat and crotch left out: two independent
waterproof leg tubes, each hung from the waist belt by a webbing hanger that ends in
a side-release buckle. Cyclists, anglers, and field crews pull them on over boots
without taking anything off, and the open seat vents the heat that full rain trousers
trap. Each tube tapers from thigh to ankle and closes on a single outseam that runs
the full leg; a side zip or hook-loop gusset at the ankle is the maker's option.

The side-release buckle solid is Yantra4D territory (`strap-buckle`; see the
manifest's notion.hardware_ref). Fashion Cabinet owns the chaps — the tapered tube
solved to ISO 8559 thigh, knee, and ankle girths, the hanger geometry, the outseam.

Pieces:
  - leg    : the tapered leg tube (cut 2, on the inseam fold), hanger placement marked.
  - hanger : the webbing waist hanger that carries the buckle (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))       # leg|hanger|set

thigh_girth  = float(PARAM(lambda: thigh_girth, 590.0))      # ISO 8559 thigh girth
knee_girth   = float(PARAM(lambda: knee_girth, 380.0))       # ISO 8559 knee girth
ankle_girth  = float(PARAM(lambda: ankle_girth, 250.0))      # ISO 8559 ankle girth
inside_leg   = float(PARAM(lambda: inside_leg, 790.0))       # ISO 8559 inside leg length
rain_ease    = float(PARAM(lambda: rain_ease, 160.0))        # ease over trousers and boots
hem_flare    = float(PARAM(lambda: hem_flare, 70.0))         # extra width to clear a boot
webbing      = float(PARAM(lambda: webbing, 25.0))           # hanger webbing width
hanger_drop  = float(PARAM(lambda: hanger_drop, 180.0))      # waist belt to the tube top
hem_allowance = float(PARAM(lambda: hem_allowance, 24.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
thigh_girth  = max(380.0, min(thigh_girth, 900.0))
knee_girth   = max(280.0, min(knee_girth, 620.0))
ankle_girth  = max(180.0, min(ankle_girth, 420.0))
inside_leg   = max(550.0, min(inside_leg, 1000.0))
rain_ease    = max(60.0, min(rain_ease, 320.0))
hem_flare    = max(0.0, min(hem_flare, 220.0))
webbing      = max(15.0, min(webbing, 50.0))
hanger_drop  = max(80.0, min(hanger_drop, 340.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))
seam_allowance = max(0.0, min(seam_allowance, 24.0))

# The tube is cut on the inseam fold, so each drafted edge is a HALF circumference.
THIGH_HALF = (thigh_girth + rain_ease) / 2.0
KNEE_HALF  = (knee_girth + rain_ease) / 2.0
ANKLE_HALF = (ankle_girth + rain_ease + hem_flare) / 2.0
L = inside_leg
KNEE_Y = L * 0.52                # knee height up the tube from the hem


def build_leg():
    """One tapered leg tube, cut on the inseam fold.

    y = 0 is the ankle hem, y = L the thigh top. x = 0 is the inseam fold; the
    outseam runs thigh → knee → ankle down the outer edge.
    """
    hem_pt   = fc.P(ANKLE_HALF, 0.0)
    knee_pt  = fc.P(KNEE_HALF, KNEE_Y)
    thigh_pt = fc.P(THIGH_HALF, L)
    internals = [
        fc.Internal("knee-line", [fc.P(0.0, KNEE_Y), knee_pt], kind="marking"),
        # Where the webbing hanger lands on the tube top.
        fc.Internal("hanger-place",
                    [fc.P(THIGH_HALF * 0.45 - webbing / 2.0, L - 12.0),
                     fc.P(THIGH_HALF * 0.45 + webbing / 2.0, L - 12.0)], kind="drill"),
        # Optional ankle gusset opening, marked not cut.
        fc.Internal("ankle-gusset",
                    [fc.P(ANKLE_HALF, 0.0), fc.P(KNEE_HALF * 0.92, KNEE_Y * 0.55)],
                    kind="marking"),
    ]
    return fc.Piece(
        "leg",
        [
            fc.Edge("inseam_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, L), thigh_pt)]),
            fc.Edge("outseam", [fc.Line(thigh_pt, knee_pt), fc.Line(knee_pt, hem_pt)]),
            fc.Edge("hem", [fc.Line(hem_pt, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 20.0},
        notches=[fc.Notch("outseam", 0.0, "thigh top"),
                 fc.Notch("outseam", 1.0, "ankle hem"),
                 fc.Notch("inseam_fold", KNEE_Y / L, "knee")],
        grainline=fc.Grainline(fc.P(ANKLE_HALF * 0.5, 30.0), fc.P(THIGH_HALF * 0.5, L - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="inseam_fold", mirror=True),
        label="Leg tube",
    )


def build_hanger():
    """The webbing waist hanger: belt loop at one end, side-release buckle at the other."""
    length = hanger_drop
    internals = [
        fc.Internal("buckle-seat",
                    [fc.P(0.0, length - webbing * 1.6), fc.P(webbing, length - webbing * 1.6)],
                    kind="marking"),
        fc.Internal("belt-fold", [fc.P(0.0, webbing * 1.6), fc.P(webbing, webbing * 1.6)],
                    kind="fold"),
    ]
    return fc.Piece(
        "hanger",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(webbing, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(webbing, 0.0), fc.P(webbing, length))]),
            fc.Edge("buckle_end", [fc.Line(fc.P(webbing, length), fc.P(0.0, length))]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, length), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("side_r", 0.5, "adjuster travel")],
        grainline=fc.Grainline(fc.P(webbing / 2.0, length * 0.15),
                               fc.P(webbing / 2.0, length * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Waist hanger",
    )


def build():
    pattern = fc.PatternSet("rain-chaps")
    everything = target_piece == "set"
    if everything or target_piece == "leg":
        pattern.add(build_leg())
    if everything or target_piece == "hanger":
        pattern.add(build_hanger())
    if everything or target_piece == "leg":
        # Cut on the inseam fold: the outseam closes on its own mirror, one seam per
        # leg — join to join, never join to fold.
        pattern.declare_seam(("leg", "outseam"), ("leg", "outseam"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "coated / laminated waterproof shell",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 70% marker; seal or tape the outseam."},
        {"item": "webbing for the waist hangers", "qty": round(hanger_drop * 2.0 + 200.0),
         "unit": "mm_length",
         "note": f"{webbing:.0f} mm webbing; two hangers plus buckle tails."},
        {"item": "side-release buckle pair", "qty": 2, "unit": "set",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) sized to the webbing."},
        {"item": "seam tape + polyester thread", "qty": 1, "unit": "set",
         "note": "tape the outseam or the chaps leak where they matter most."},
    ]
    pattern.metadata = {
        "fc300_rank": 237, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "Rain trousers with the seat and crotch left out: two waterproof leg "
            "tubes tapered thigh→knee→ankle on a single outseam, each hung from the waist belt "
            "by a webbing hanger that ends in a side-release buckle. The open seat vents.",
        "solved": {"thigh_half_mm": round(THIGH_HALF, 1), "knee_half_mm": round(KNEE_HALF, 1),
                   "ankle_half_mm": round(ANKLE_HALF, 1), "knee_height_mm": round(KNEE_Y, 1)},
        "hardware": "side-release buckles via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()
