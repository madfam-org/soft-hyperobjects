"""
Harness Vest — Fashion Cabinet Garment Cartridge (FC-300 #241, technical & outdoor).

A load-carrying harness vest: a shoulder YOKE that spans the trapezius and takes the
whole load, with webbing channels running down the front and back panels through
ladder-lock adjusters that let one vest fit a range of torsos and layer thicknesses.
Guides, surveyors, camera crews, and search teams wear it over anything, and the load
sits on the yoke rather than dragging on the neck.

The ladder-lock adjuster solid is Yantra4D territory (`strap-buckle`; see the
manifest's notion.hardware_ref). Fashion Cabinet owns the vest — the yoke solved to
ISO 8559 across-back and shoulder-length, the panels solved to chest girth, the webbing
channel runs.

Front and back share the body quarter, so the shoulder and side seams balance by
construction and their declared seam checks are dimensional proofs.

Pieces:
  - yoke    : the load-bearing shoulder yoke (cut 1 on the centre-back fold).
  - front   : the front panel (cut 2, mirrored), webbing channels marked.
  - back    : the back panel (cut 1 on fold), webbing channels marked.
  - webbing : the adjuster strap run (cut 4 — two front, two back).

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
target_piece = str(PARAM(lambda: target_piece, "set"))      # yoke|front|back|webbing|set

chest_girth   = float(PARAM(lambda: chest_girth, 1000.0))   # ISO 8559 chest/bust girth
across_back   = float(PARAM(lambda: across_back, 380.0))    # ISO 8559 across back
shoulder_len  = float(PARAM(lambda: shoulder_len, 140.0))   # ISO 8559 shoulder length
neck_girth    = float(PARAM(lambda: neck_girth, 400.0))     # ISO 8559 neck girth
panel_length  = float(PARAM(lambda: panel_length, 460.0))   # yoke to panel hem
yoke_depth    = float(PARAM(lambda: yoke_depth, 130.0))     # yoke drop over the trapezius
layer_ease    = float(PARAM(lambda: layer_ease, 240.0))     # ease over layers
webbing       = float(PARAM(lambda: webbing, 25.0))         # channel webbing width
adjust_run    = float(PARAM(lambda: adjust_run, 200.0))     # adjuster travel
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth   = max(700.0, min(chest_girth, 1700.0))
across_back   = max(280.0, min(across_back, 560.0))
shoulder_len  = max(90.0, min(shoulder_len, 220.0))
neck_girth    = max(300.0, min(neck_girth, 560.0))
panel_length  = max(280.0, min(panel_length, 700.0))
yoke_depth    = max(80.0, min(yoke_depth, 240.0))
layer_ease    = max(100.0, min(layer_ease, 420.0))
webbing       = max(15.0, min(webbing, 50.0))
adjust_run    = max(80.0, min(adjust_run, 400.0))
seam_allowance = max(0.0, min(seam_allowance, 24.0))

BODY = chest_girth + layer_ease
BW = BODY / 4.0                       # body quarter — front and back share it
NECK_HALF = neck_girth / 6.0          # neck half-width at the yoke
YOKE_HALF = across_back / 2.0
L = panel_length


def build_yoke():
    """The load-bearing yoke: spans the trapezius, cut on the centre-back fold.

    x = 0 is the centre back (the fold); x = YOKE_HALF is the shoulder point. The
    neck edge scoops; the shoulder edge carries the yoke's drop.
    """
    neck_pt     = fc.P(0.0, yoke_depth)
    shoulder_in = fc.P(NECK_HALF, yoke_depth)
    shoulder_pt = fc.P(YOKE_HALF, yoke_depth - shoulder_len * 0.30)
    hem_out     = fc.P(YOKE_HALF, 0.0)
    internals = [
        fc.Internal("channel-front",
                    [fc.P(YOKE_HALF * 0.45 - webbing / 2.0, 0.0),
                     fc.P(YOKE_HALF * 0.45 - webbing / 2.0, yoke_depth * 0.85)],
                    kind="marking"),
        fc.Internal("channel-back",
                    [fc.P(YOKE_HALF * 0.45 + webbing / 2.0, 0.0),
                     fc.P(YOKE_HALF * 0.45 + webbing / 2.0, yoke_depth * 0.85)],
                    kind="marking"),
    ]
    return fc.Piece(
        "yoke",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.curve_through(neck_pt, shoulder_in, bulge=0.18, side=-1.0)]),
            fc.Edge("shoulder", [fc.Line(shoulder_in, shoulder_pt)]),
            fc.Edge("armscye", [fc.curve_through(shoulder_pt, hem_out, bulge=0.14, side=-1.0)]),
            fc.Edge("panel_seam", [fc.Line(hem_out, fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 1.0, "shoulder point"),
                 fc.Notch("panel_seam", 0.5, "panel centre")],
        grainline=fc.Grainline(fc.P(YOKE_HALF * 0.4, 12.0),
                               fc.P(YOKE_HALF * 0.4, yoke_depth - 12.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Load-bearing yoke",
    )


def _channel_internals(width):
    """Two webbing channels running the panel's length, with the adjuster seats."""
    out = []
    for sign, tag in ((-1.0, "left"), (1.0, "right")):
        cx = width * 0.5 + sign * width * 0.26
        out.append(fc.Internal(f"channel-{tag}",
                               [fc.P(cx - webbing / 2.0, 20.0),
                                fc.P(cx - webbing / 2.0, L - 20.0)], kind="marking"))
        out.append(fc.Internal(f"channel-{tag}-b",
                               [fc.P(cx + webbing / 2.0, 20.0),
                                fc.P(cx + webbing / 2.0, L - 20.0)], kind="marking"))
        out.append(fc.Internal(f"ladder-lock-{tag}",
                               [fc.P(cx - webbing / 2.0, L - adjust_run),
                                fc.P(cx + webbing / 2.0, L - adjust_run)], kind="drill"))
    return out


def build_front():
    """The front panel: hangs from the yoke, webbing channels down its length."""
    return fc.Piece(
        "front",
        [
            fc.Edge("center_front", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("yoke_seam", [fc.Line(fc.P(0.0, L), fc.P(BW, L))]),
            fc.Edge("side", [fc.Line(fc.P(BW, L), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0},
        notches=[fc.Notch("side", 0.0, "yoke joint"),
                 fc.Notch("side", (L - adjust_run) / L, "adjuster")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 20.0), fc.P(BW * 0.5, L - 20.0)),
        internals=_channel_internals(BW),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front panel",
    )


def build_back():
    """The back panel: same body quarter as the front, so the side seams balance."""
    return fc.Piece(
        "back",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("yoke_seam", [fc.Line(fc.P(0.0, L), fc.P(BW, L))]),
            fc.Edge("side", [fc.Line(fc.P(BW, L), fc.P(BW, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 22.0},
        notches=[fc.Notch("side", 0.0, "yoke joint"),
                 fc.Notch("side", (L - adjust_run) / L, "adjuster")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 20.0), fc.P(BW * 0.5, L - 20.0)),
        internals=_channel_internals(BW),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back", mirror=True),
        label="Back panel",
    )


def build_webbing():
    """One adjuster strap run: through a channel, round the ladder-lock, back on itself."""
    length = L + adjust_run
    return fc.Piece(
        "webbing",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(length, 0.0), fc.P(length, webbing))]),
            fc.Edge("top", [fc.Line(fc.P(length, webbing), fc.P(0.0, webbing))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, webbing), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", L / length, "ladder-lock turn")],
        grainline=fc.Grainline(fc.P(length * 0.15, webbing / 2.0),
                               fc.P(length * 0.85, webbing / 2.0)),
        cut=fc.CutSpec(quantity=4),
        label="Adjuster webbing",
    )


def build():
    pattern = fc.PatternSet("harness-vest")
    everything = target_piece == "set"
    if everything or target_piece == "yoke":
        pattern.add(build_yoke())
    if everything or target_piece == "front":
        pattern.add(build_front())
    if everything or target_piece == "back":
        pattern.add(build_back())
    if everything or target_piece == "webbing":
        pattern.add(build_webbing())
    if everything:
        # Front and back share the body quarter — the side seam is a dimensional proof.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        # Both panels hang from the yoke on the same run.
        pattern.declare_seam(("front", "yoke_seam"), ("back", "yoke_seam"), tol=1.0)
        # The yoke's own shoulder meets its mirror across the fold-cut pair.
        pattern.declare_seam(("yoke", "shoulder"), ("yoke", "shoulder"), tol=1.0)
        # The webbing tail turns on itself at the ladder-lock.
        pattern.declare_seam(("webbing", "anchor_end"), ("webbing", "free_end"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cordura / heavy ripstop",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 70% marker; double the yoke — it takes the load."},
        {"item": "webbing for the channels", "qty": round((L + adjust_run) * 4.0),
         "unit": "mm_length", "note": f"{webbing:.0f} mm webbing, four runs."},
        {"item": "ladder-lock adjusters", "qty": 4, "unit": "count",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) sized to the webbing."},
        {"item": "bonded nylon thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "bar-tack every webbing anchor and the yoke seam — the whole load path."},
    ]
    pattern.metadata = {
        "fc300_rank": 241, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A load-carrying vest whose shoulder yoke takes the whole weight off "
            "the neck, with webbing channels down front and back panels through ladder-lock "
            "adjusters so one vest fits a range of torsos and layer thicknesses.",
        "solved": {"body_quarter_mm": round(BW, 1), "yoke_half_mm": round(YOKE_HALF, 1),
                   "neck_half_mm": round(NECK_HALF, 1), "panel_length_mm": round(L, 1)},
        "hardware": "ladder-lock adjusters via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()
