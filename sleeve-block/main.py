"""
Sleeve Block (Set-in) — Fashion Cabinet Enabler Cartridge (not FC-100 counted).

A standalone woven set-in sleeve whose cap is solved to a TARGET armscye
length plus cap ease — the consumer half of the commons' first
cross-cartridge interface. CI feeds it the bodice block's measured armscye
(scripts/qa/verify_interfaces.py) and checks the produced cap length.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math`
pre-injected; params as bare globals via PARAM(lambda...); result = PatternSet.
"""

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "sleeve"))

armscye_length = float(PARAM(lambda: armscye_length, 0.0))  # 0 = auto from bust
bust_girth     = float(PARAM(lambda: bust_girth, 880.0))
cap_ease       = float(PARAM(lambda: cap_ease, 20.0))       # woven cap ease
sleeve_length  = float(PARAM(lambda: sleeve_length, 600.0))
wrist_opening  = float(PARAM(lambda: wrist_opening, 210.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

bust_girth = max(600.0, min(bust_girth, 1600.0))
armscye = armscye_length if armscye_length > 0 else bust_girth * 0.46 + 55.0
armscye = max(300.0, min(armscye, 750.0))
cap_ease = max(0.0, min(cap_ease, 60.0))
sleeve_length = max(200.0, min(sleeve_length, 780.0))
wrist_opening = max(150.0, min(wrist_opening, 420.0))

CAP_TARGET = armscye + cap_ease
CH = max(80.0, armscye * 0.21)                      # taller woven cap


def _cap_curve(hb, sl):
    apex = fc.P(0.0, sl + CH)
    return fc.Edge("cap", [
        fc.Bezier(fc.P(hb, sl), fc.P(hb * 0.72, sl + CH * 0.10),
                  fc.P(hb * 0.30, sl + CH * 0.96), apex),
        fc.Bezier(apex, fc.P(-hb * 0.30, sl + CH * 0.96),
                  fc.P(-hb * 0.72, sl + CH * 0.10), fc.P(-hb, sl)),
    ])


def build():
    sl = max(120.0, sleeve_length - CH)
    lo, hi = 20.0, CAP_TARGET / 2.0 + CH + 60.0
    for _ in range(48):
        hb = (lo + hi) / 2.0
        if _cap_curve(hb, sl).length(0.05) < CAP_TARGET:
            lo = hb
        else:
            hi = hb
    hb = (lo + hi) / 2.0
    if abs(_cap_curve(hb, sl).length(0.05) - CAP_TARGET) > 1.0:
        raise ValueError("sleeve cap solver did not converge")
    chw = max(75.0, min(wrist_opening / 2.0, hb))
    piece = fc.Piece(
        "sleeve",
        [
            fc.Edge("hem", [fc.Line(fc.P(-chw, 0.0), fc.P(chw, 0.0))]),
            fc.Edge("underarm_back", [fc.Line(fc.P(chw, 0.0), fc.P(hb, sl))]),
            _cap_curve(hb, sl),
            fc.Edge("underarm_front", [fc.Line(fc.P(-hb, sl), fc.P(-chw, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("cap", 0.5, "shoulder match")],
        grainline=fc.Grainline(fc.P(0.0, 40.0), fc.P(0.0, sl + CH * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Set-in Sleeve",
    )
    pattern = fc.PatternSet("sleeve-block")
    pattern.add(piece)
    pattern.declare_seam(("sleeve", "underarm_front"), ("sleeve", "underarm_back"), tol=1.0)
    pattern.metadata = {
        "enabler": True,
        "interface": "armscye",
        "cap_target_mm": round(CAP_TARGET, 1),
        "solved_biceps_flat_mm": round(2.0 * hb, 1),
        "cap_ease_mm": cap_ease,
        "drafting": "woven set-in sleeve; cap solved to armscye_length + cap_ease",
    }
    return pattern


result = build()
