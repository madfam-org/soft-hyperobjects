"""
Webbing Belt — Fashion Cabinet Accessory Cartridge (Yantra4D-bridged hardware).

A made-to-measure belt: one strap piece running from a folded buckle end, through the
body, to a pointed billet with punched adjustment eyelets. The buckle SOLID is Yantra4D
territory (`strap-buckle`; see the manifest's notion.hardware_ref). Fashion Cabinet owns
the belt — total length from the waist measurement, the taper, and the eyelet spacing so
the middle hole lands at the measured waist.

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
waist_girth   = float(PARAM(lambda: waist_girth, 900.0))
strap_width   = float(PARAM(lambda: strap_width, 38.0))
tip_length    = float(PARAM(lambda: tip_length, 60.0))
eyelets       = int(  PARAM(lambda: eyelets, 5))
eyelet_pitch  = float(PARAM(lambda: eyelet_pitch, 25.0))
buckle_return = float(PARAM(lambda: buckle_return, 80.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth   = max(550.0, min(waist_girth, 1400.0))
strap_width   = max(15.0, min(strap_width, 50.0))
tip_length    = max(0.0, min(tip_length, 120.0))
eyelets       = max(1, min(eyelets, 9))
eyelet_pitch  = max(15.0, min(eyelet_pitch, 40.0))
buckle_return = max(40.0, min(buckle_return, 140.0))

# ── Belt length math ──────────────────────────────────────────────────────────
# Total strap length = the fold-back at the buckle + the run to the middle eyelet
# (which sits at the measured waist, past the buckle) + half the eyelet field + tip.
# The middle eyelet lands at `waist_girth` measured from the buckle bar.
half_field   = (eyelets - 1) / 2.0 * eyelet_pitch
body_length  = buckle_return + waist_girth + half_field
total_length = body_length + tip_length
W            = strap_width


def _eyelet_xs():
    """X positions of the eyelets, centered on the measured waist (buckle_return +
    waist_girth from the fold end)."""
    center = buckle_return + waist_girth
    start = center - half_field
    return [start + i * eyelet_pitch for i in range(eyelets)]


def build_strap():
    # The strap lies along +X. The buckle end (x=0) folds back `buckle_return`; the
    # billet tip tapers to a point at x=total_length.
    tip_apex = fc.P(total_length, W / 2.0)
    if tip_length <= 0.0:
        # Square end.
        edges = [
            fc.Edge("buckle", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, W))]),
            fc.Edge("top",    [fc.Line(fc.P(0.0, W), fc.P(body_length, W))]),
            fc.Edge("tip",    [fc.Line(fc.P(body_length, W), fc.P(body_length, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(body_length, 0.0), fc.P(0.0, 0.0))]),
        ]
    else:
        edges = [
            fc.Edge("buckle",   [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, W))]),
            fc.Edge("top",      [fc.Line(fc.P(0.0, W), fc.P(body_length, W))]),
            fc.Edge("tip_up",   [fc.Line(fc.P(body_length, W), tip_apex)]),
            fc.Edge("tip_down", [fc.Line(tip_apex, fc.P(body_length, 0.0))]),
            fc.Edge("bottom",   [fc.Line(fc.P(body_length, 0.0), fc.P(0.0, 0.0))]),
        ]

    internals = []
    for x in _eyelet_xs():
        c = fc.P(x, W / 2.0)
        internals.append(fc.Internal("eyelet-h",
                                     [fc.P(c.x - 4.0, c.y), fc.P(c.x + 4.0, c.y)], kind="drill"))
        internals.append(fc.Internal("eyelet-v",
                                     [fc.P(c.x, c.y - 4.0), fc.P(c.x, c.y + 4.0)], kind="drill"))
    # The fold line where the strap wraps the buckle bar.
    internals.append(fc.Internal(
        "buckle-fold", [fc.P(buckle_return, 0.0), fc.P(buckle_return, W)], kind="marking"))

    return fc.Piece(
        "strap",
        edges,
        seam_allowance=0.0,  # webbing edge-finished, not seamed — cut line == edge
        notches=[fc.Notch("bottom", buckle_return / total_length, "buckle fold"),
                 fc.Notch("bottom", (buckle_return + waist_girth) / total_length, "waist")],
        grainline=fc.Grainline(fc.P(total_length * 0.15, W / 2.0),
                               fc.P(total_length * 0.85, W / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Belt Strap",
    )


def build():
    pattern = fc.PatternSet("webbing-belt")
    pattern.add(build_strap())
    pattern.bom = [
        {"item": "webbing or leather strip", "qty": round(total_length / 10.0) * 10,
         "unit": "mm_length", "note": f"{W:.0f} mm wide"},
        {"item": "eyelets", "qty": eyelets, "unit": "count", "note": "punched + set"},
        {"item": "buckle", "qty": 1, "unit": "count",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) or off-the-shelf"},
        {"item": "rivets", "qty": 2, "unit": "count", "note": "secure the buckle fold"},
    ]
    pattern.metadata = {
        "total_length_mm": round(total_length, 1),
        "waist_girth_mm": round(waist_girth, 1),
        "strap_width_mm": round(W, 1),
        "eyelets": eyelets,
        "hardware": "buckle solid delegated to Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()
