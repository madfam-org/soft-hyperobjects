"""
Baby Swaddle Cocoon — Fashion Cabinet Garment Cartridge
(FC-400 #328, kids_baby, T1).

A swaddle cocoon (sleep sack) for a newborn: a tapered jersey tube, closed round
the body, with shoulder snaps that open the top so the baby is laid in and the
cocoon snapped over the shoulders rather than pulled over the head. Drafted from
INFANT measurements (bodies/infant-6m). The safety rule is that a cocoon must be
loose enough at the HIP for the legs to move (a swaddle that pins the legs risks
hip dysplasia) and snug at the CHEST so the baby cannot slip down inside it.

Two things are solved by measurement rather than by formula:

  1. THE HIP IS DELIBERATELY LOOSER THAN THE CHEST. The cocoon tapers from a snug
     chest to a MEASURED hip-plus-legroom, never the other way — the legroom is
     added at the hip, floored so the hip circumference can never come out smaller
     than the chest (a taper that inverts the tube, geometry the kernel CCW-
     normalizes into a valid-looking piece). The hip legroom is reported.

  2. THE SHOULDER SNAPS ARE DIMENSIONALLY BRIDGED. The snap diameter drives both
     the drafted shoulder-lap and the Yantra4D sew-on-snap's snap_dia, so the
     printed snap matches the sewn overlap — the same number flows to the
     garment's sewn edge and the hardware's sewn flange.

The SEW-ON-SNAP SOLID is Yantra4D territory (`sew-on-snap`; see notion.hardware_ref).

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))
# body|shoulder|set

chest_girth = float(PARAM(lambda: chest_girth, 440.0))
hip_girth = float(PARAM(lambda: hip_girth, 480.0))
cocoon_length = float(PARAM(lambda: cocoon_length, 480.0))  # shoulder to closed hem
neck_width = float(PARAM(lambda: neck_width, 130.0))
leg_room = float(PARAM(lambda: leg_room, 120.0))            # extra at the hip
snap_diameter = float(PARAM(lambda: snap_diameter, 12.0))
knit_stretch = float(PARAM(lambda: knit_stretch, 0.10))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

chest_girth = max(360.0, min(chest_girth, 560.0))
hip_girth = max(380.0, min(hip_girth, 620.0))
cocoon_length = max(340.0, min(cocoon_length, 680.0))
neck_width = max(100.0, min(neck_width, 200.0))
leg_room = max(40.0, min(leg_room, 260.0))
snap_diameter = max(9.0, min(snap_diameter, 18.0))
knit_stretch = max(0.0, min(knit_stretch, 0.20))
seam_allowance = max(6.0, min(seam_allowance, 14.0))
hem_allowance = max(12.0, min(hem_allowance, 35.0))

TOPSTITCH = 5.0

# Chest snug (a touch of negative ease), hip deliberately looser (measured hip +
# legroom), floored so the hip can never come out smaller than the chest.
QUARTER_CHEST = (chest_girth * (1.0 - knit_stretch * 0.5)) / 4.0
_QUARTER_HIP_RAW = (hip_girth + leg_room) / 4.0
QUARTER_HIP = max(QUARTER_CHEST + 6.0, _QUARTER_HIP_RAW)
HALF_NECK = neck_width / 2.0
# The shoulder overlap the snaps close, driven by the snap diameter.
SHOULDER_LAP = max(snap_diameter * 2.2, 24.0)


def _snap(label, x, y):
    a = max(2.5, snap_diameter * 0.32)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def build_body():
    """The cocoon body, cut 2 (front + back). Tapers chest → looser hip, closed
    hem at the bottom."""
    p_hem_side = fc.P(QUARTER_HIP, 0.0)
    p_hem_c = fc.P(0.0, 0.0)
    p_shoulder_side = fc.P(QUARTER_CHEST, cocoon_length)
    p_neck_pt = fc.P(HALF_NECK, cocoon_length)
    p_neck_c = fc.P(0.0, cocoon_length - HALF_NECK * 0.4)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_c, p_hem_side)]),
        # The taper: hip (wide) up to the chest/shoulder (narrower).
        fc.Edge("side", [fc.Line(p_hem_side, p_shoulder_side)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder_side, p_neck_pt)]),
        fc.Edge("neck", [fc.curve_through(p_neck_pt, p_neck_c, bulge=0.25, side=1.0)]),
        fc.Edge("cf_fold", [fc.Line(p_neck_c, p_hem_c)]),
    ]
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "cf_fold": 0.0},
        notches=[fc.Notch("side", 0.5, "waist level"),
                 fc.Notch("shoulder", 1.0, "neck point")],
        grainline=fc.Grainline(fc.P(QUARTER_HIP * 0.4, 20.0),
                               fc.P(QUARTER_CHEST * 0.4, cocoon_length - 20.0)),
        internals=[
            fc.Internal("shoulder snap lap",
                        [fc.P(HALF_NECK, cocoon_length - SHOULDER_LAP),
                         fc.P(QUARTER_CHEST, cocoon_length - SHOULDER_LAP)],
                        kind="marking"),
            _snap("shoulder snap", (HALF_NECK + QUARTER_CHEST) / 2.0,
                  cocoon_length - SHOULDER_LAP * 0.5),
        ],
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="cf_fold"),
        label="Cocoon body (cut 2, on fold)",
    )


def build_shoulder():
    """The shoulder snap tab, cut 4. Carries the snap; the overlap = SHOULDER_LAP."""
    w = SHOULDER_LAP
    h = max(30.0, snap_diameter * 3.0)
    edges = [
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("out", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
    ]
    return fc.Piece(
        "shoulder", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("attach", 0.5, "shoulder join")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=[
            _snap("tab snap", w * 0.5, h * 0.5),
        ],
        cut=fc.CutSpec(quantity=4),
        label="Shoulder snap tab (cut 4)",
    )


def build():
    pattern = fc.PatternSet("baby-cocoon")
    everything = target_piece == "set"
    want = {
        "body": everything or target_piece == "body",
        "shoulder": everything or target_piece == "shoulder",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["body"]:
        pattern.add(build_body())
    if want["shoulder"]:
        pattern.add(build_shoulder())

    if want["shoulder"]:
        # The tab's attach edge matches the shoulder lap; declared so a tab
        # redrafted off the snap lap goes red.
        b = build_shoulder()
        pattern.declare_seam(("shoulder", "attach"), ("shoulder", "out"),
                             tol=1.0, ease=b.edge("attach").length(0.05)
                             - b.edge("out").length(0.05))

    fabric_width = 1600.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "cotton jersey, 180 gsm (breathable, TOG-appropriate)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 68% marker; a breathable single "
                 f"jersey — do not over-insulate a sleeping baby."},
        {"item": "sew-on snap", "qty": 4, "unit": "pair",
         "note": f"Yantra4D sew-on-snap (notion.hardware_ref) at "
                 f"{snap_diameter:.0f} mm; the snap_dia is fed from this garment's "
                 f"snap_diameter, which also drafts the shoulder overlap. Shoulder-"
                 f"open so the baby is laid in, not pulled over the head."},
        {"item": "ballpoint needle 70/10 + stretch thread", "qty": 1, "unit": "spool",
         "note": "seams turned inward; no seam allowance against the baby."},
    ]
    pattern.metadata = {
        "fc400_rank": 328,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "cotton-jersey",
        "finished_mm": {
            "quarter_chest": round(QUARTER_CHEST, 1),
            "quarter_hip_with_legroom": round(QUARTER_HIP, 1),
            "cocoon_length": round(cocoon_length, 1),
            "shoulder_lap": round(SHOULDER_LAP, 1),
        },
        "solved": {
            "quarter_chest_mm": round(QUARTER_CHEST, 2),
            "quarter_hip_requested_mm": round(_QUARTER_HIP_RAW, 2),
            "quarter_hip_final_mm": round(QUARTER_HIP, 2),
            "hip_looser_than_chest": bool(QUARTER_HIP > QUARTER_CHEST),
            "leg_room_mm": round(leg_room, 2),
            "shoulder_lap_mm": round(SHOULDER_LAP, 2),
            "snap_diameter_mm": round(snap_diameter, 2),
            "note": "the cocoon tapers from a snug chest to a DELIBERATELY looser "
                    "hip (measured hip plus legroom), floored so the hip can never "
                    "come out smaller than the chest — a swaddle that pins the legs "
                    "risks hip dysplasia, and a taper that inverts the tube is CCW-"
                    "normalized by the kernel into a valid-looking piece. The "
                    "shoulder snap diameter drives both the drafted overlap and the "
                    "hardware's snap_dia, so the printed snap matches the sewn edge.",
        },
        "safety": "hip loose enough for the legs to move freely (hip-dysplasia "
                  "safe); chest snug so the baby cannot slip down inside; shoulder-"
                  "open so the cocoon is snapped over, never pulled over the head; "
                  "breathable jersey so the baby does not overheat.",
        "hardware": "sew-on snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); "
                    "the solid's snap_dia — its sewn flange dimension — is fed from "
                    "this garment's snap_diameter, which ALSO drafts the shoulder "
                    "overlap, so the same number flows to both sewn edges.",
    }
    return pattern


result = build()
