"""
Five-Panel Cap — Fashion Cabinet Accessory Cartridge (Yantra4D-bridged hardware).

A made-to-measure five-panel cap from the head girth: five crown gores (a front, two
side, two back — the side and back cut x2 mirrored), a stiffened PEAK (half-ellipse on
fold), and a SNAP-BACK TAB with punched holes. The snap SOLID is Yantra4D territory
(`snap-fit`; see the manifest's notion.hardware_ref). Fashion Cabinet owns the cap
geometry — the five gores summing to the head girth, the crown height, the peak.

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
head_girth   = float(PARAM(lambda: head_girth, 580.0))
crown_height = float(PARAM(lambda: crown_height, 130.0))
peak_length  = float(PARAM(lambda: peak_length, 70.0))
snap_dia     = float(PARAM(lambda: snap_dia, 12.0))
ease         = float(PARAM(lambda: ease, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
head_girth   = max(500.0, min(head_girth, 640.0))
crown_height = max(90.0, min(crown_height, 170.0))
peak_length  = max(40.0, min(peak_length, 90.0))
snap_dia     = max(8.0, min(snap_dia, 16.0))
ease         = max(0.0, min(ease, 24.0))

head_eff  = head_girth + ease
gore_base = head_eff / 5.0        # each of the 5 gores spans this at the headband
GB        = gore_base / 2.0       # half-base (gores are symmetric about x=0)


def _gore(name, qty, mirror, label):
    """A symmetric crown gore: base width gore_base at y=0, curving to an apex point at
    (0, crown_height). Left and right edges are Beziers so panels seam smoothly."""
    apex = fc.P(0.0, crown_height)
    left = fc.Bezier(fc.P(-GB, 0.0), fc.P(-GB * 0.95, crown_height * 0.45),
                     fc.P(-GB * 0.4, crown_height * 0.85), apex)
    right = fc.Bezier(apex, fc.P(GB * 0.4, crown_height * 0.85),
                      fc.P(GB * 0.95, crown_height * 0.45), fc.P(GB, 0.0))
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(GB, 0.0), fc.P(-GB, 0.0))]),  # headband seam
        fc.Edge("seam_l", [left]),
        fc.Edge("seam_r", [right]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=10.0,
        notches=[fc.Notch("bottom", 0.5, "center")],
        grainline=fc.Grainline(fc.P(0.0, crown_height * 0.1), fc.P(0.0, crown_height * 0.8)),
        cut=fc.CutSpec(quantity=qty, mirror=mirror),
        label=label,
    )


def build_peak():
    """The stiffened peak: a half-ellipse (width = head_eff * 0.45, projection =
    peak_length) cut on the straight back edge (fold) and mirrored."""
    half_w = head_eff * 0.225
    front = fc.Bezier(fc.P(-half_w, 0.0), fc.P(-half_w * 0.6, peak_length),
                      fc.P(half_w * 0.6, peak_length), fc.P(half_w, 0.0))
    edges = [
        fc.Edge("back",  [fc.Line(fc.P(half_w, 0.0), fc.P(-half_w, 0.0))]),  # fold/headband edge
        fc.Edge("front", [front]),
    ]
    return fc.Piece(
        "peak",
        edges,
        seam_allowance=8.0,
        allowances={"front": 6.0},
        grainline=fc.Grainline(fc.P(0.0, peak_length * 0.1), fc.P(0.0, peak_length * 0.8)),
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="back", mirror=True),
        label="Peak",
    )


def build_snap_tab():
    """The snap-back adjustment tab: a strip with two rows of snap holes."""
    w, h = 90.0, 28.0
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top",    [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("end",    [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    for i in range(4):
        x = 25.0 + i * 18.0
        internals.append(fc.Internal(
            "snap-h", [fc.P(x - 4.0, h / 2.0), fc.P(x + 4.0, h / 2.0)], kind="drill"))
        internals.append(fc.Internal(
            "snap-v", [fc.P(x, h / 2.0 - 4.0), fc.P(x, h / 2.0 + 4.0)], kind="drill"))
    return fc.Piece(
        "snap-tab",
        edges,
        seam_allowance=8.0,
        internals=internals,
        grainline=fc.Grainline(fc.P(w * 0.2, h / 2.0), fc.P(w * 0.8, h / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Snap-back Tab",
    )


def build():
    pattern = fc.PatternSet("five-panel-cap")
    pattern.add(_gore("front-panel", 1, False, "Front Panel"))
    pattern.add(_gore("side-panel", 2, True, "Side Panel"))
    pattern.add(_gore("back-panel", 2, True, "Back Panel"))
    pattern.add(build_peak())
    pattern.add(build_snap_tab())
    pattern.bom = [
        {"item": "shell fabric (twill)", "qty": 300, "unit": "mm_length",
         "note": "≈ at 1400 mm width for all panels + peak + tab"},
        {"item": "peak stiffener", "qty": 1, "unit": "count", "note": "buckram or PE insert"},
        {"item": "snap closure", "qty": 1, "unit": "count",
         "note": "Yantra4D snap-fit (see notion.hardware_ref) or off-the-shelf"},
    ]
    pattern.metadata = {
        "head_girth_mm": round(head_girth, 1),
        "head_opening_mm": round(head_eff, 1),
        "gore_base_mm": round(gore_base, 1),
        "crown_height_mm": round(crown_height, 1),
        "hardware": "snap-back closure delegated to Yantra4D (notion.hardware_ref -> snap-fit)",
    }
    return pattern


result = build()
