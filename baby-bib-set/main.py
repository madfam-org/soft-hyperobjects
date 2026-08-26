"""
Bandana Feeding Bib — Fashion Cabinet Garment Cartridge
(FC-400 #325, kids_baby, T1).

A bandana-style feeding bib for a baby: a rounded triangle that sits like a
kerchief over the chest, backed with terry towelling to catch drool, closing at
the neck on a two-position snap so one bib fits a growing neck. The number that
has to be right is the NECK BAND against the two snap positions — a band cut with
one snap position outgrows the baby in weeks.

Two things are solved by measurement rather than by formula:

  1. THE NECK BAND CARRIES TWO SOLVED SNAP POSITIONS. The band spans the MEASURED
     neck girth (plus the overlap the snap needs), and TWO snap studs are placed
     — a tight and a loose setting — solved from the neck girth so the bib fits a
     range as the baby grows, and neither stud lands off the band.

  2. THE TRIANGLE IS CLAMPED SO IT COVERS BUT DOES NOT SWАДDLE. The bandana drop
     (how far the point hangs) is floored against the band width so it always
     covers the chest, and clamped against a maximum so it cannot reach the lap
     and trail in the food — a drop larger than the piece inverts it, geometry
     the kernel CCW-normalizes into a valid-looking piece.

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
# bandana|band|set

neck_girth = float(PARAM(lambda: neck_girth, 240.0))       # baby neck
bandana_width = float(PARAM(lambda: bandana_width, 260.0))  # across the top
bandana_drop = float(PARAM(lambda: bandana_drop, 180.0))    # point drop
band_width = float(PARAM(lambda: band_width, 32.0))
snap_diameter = float(PARAM(lambda: snap_diameter, 11.0))
snap_step = float(PARAM(lambda: snap_step, 20.0))          # growth step between snaps
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

neck_girth = max(180.0, min(neck_girth, 340.0))
bandana_width = max(180.0, min(bandana_width, 360.0))
bandana_drop = max(100.0, min(bandana_drop, 300.0))
band_width = max(22.0, min(band_width, 55.0))
snap_diameter = max(9.0, min(snap_diameter, 16.0))
snap_step = max(10.0, min(snap_step, 40.0))
seam_allowance = max(6.0, min(seam_allowance, 14.0))

TOPSTITCH = 5.0

HALF_WIDTH = bandana_width / 2.0
# The bandana drop floored above the band and clamped below a maximum so it covers
# but does not trail.
_DROP_RAW = bandana_drop
DROP = max(band_width * 2.0, min(_DROP_RAW, HALF_WIDTH * 1.8))
# The neck band: neck girth plus the snap overlap. Two snap positions, snap_step
# apart, both solved so neither lands off the band.
SNAP_OVERLAP = max(snap_diameter * 3.0, 30.0)
BAND_LEN = neck_girth + SNAP_OVERLAP
SNAP1_X = BAND_LEN - seam_allowance - snap_diameter * 1.2    # tight setting
SNAP2_X = max(seam_allowance + snap_diameter, SNAP1_X - snap_step)  # loose setting


def _snap(label, x, y):
    a = max(2.5, snap_diameter * 0.32)
    return fc.Internal(
        label,
        [fc.P(x - a, y), fc.P(x + a, y), fc.P(x, y), fc.P(x, y - a), fc.P(x, y + a)],
        kind="drill")


def build_bandana():
    """The bandana body, cut 2 (face + terry backing). A rounded triangle."""
    edges = [
        fc.Edge("top", [fc.Line(fc.P(-HALF_WIDTH, 0.0), fc.P(HALF_WIDTH, 0.0))]),
        # Right side down to the point.
        fc.Edge("side_r", [fc.curve_through(
            fc.P(HALF_WIDTH, 0.0), fc.P(0.0, -DROP), bulge=0.12, side=1.0)]),
        # Left side back up.
        fc.Edge("side_l", [fc.curve_through(
            fc.P(0.0, -DROP), fc.P(-HALF_WIDTH, 0.0), bulge=0.12, side=1.0)]),
    ]
    return fc.Piece(
        "bandana", edges,
        seam_allowance=seam_allowance,
        allowances={},
        notches=[fc.Notch("top", 0.5, "CF / band centre")],
        grainline=fc.Grainline(fc.P(0.0, -10.0), fc.P(0.0, -DROP + 10.0)),
        internals=[
            fc.Internal("point topstitch",
                        [fc.P(-HALF_WIDTH * 0.3, -DROP * 0.6),
                         fc.P(0.0, -DROP + TOPSTITCH),
                         fc.P(HALF_WIDTH * 0.3, -DROP * 0.6)], kind="trace"),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Bandana (cut 2: face + terry)",
    )


def build_band():
    """The neck band, cut 2. Two solved snap positions for growth."""
    ln = BAND_LEN
    w = band_width * 2.0 + 2.0 * seam_allowance
    edges = [
        fc.Edge("lower", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
        fc.Edge("snap_end", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
        fc.Edge("upper", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
        fc.Edge("stud_end", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "band", edges,
        seam_allowance=seam_allowance,
        allowances={"lower": 0.0, "upper": 0.0},
        notches=[fc.Notch("lower", 0.5, "CF / bandana centre"),
                 fc.Notch("lower", 1.0 - SNAP_OVERLAP / ln, "overlap start")],
        grainline=fc.Grainline(fc.P(ln * 0.1, w / 2.0), fc.P(ln * 0.9, w / 2.0)),
        internals=[
            fc.Internal("fold line", [fc.P(0.0, w / 2.0), fc.P(ln, w / 2.0)],
                        kind="marking"),
            _snap("snap socket (cap)", seam_allowance + snap_diameter, w / 2.0),
            _snap("snap stud tight", SNAP1_X, w / 2.0),
            _snap("snap stud loose (grow)", SNAP2_X, w / 2.0),
        ],
        cut=fc.CutSpec(quantity=2),
        label="Neck band (cut 2)",
    )


def build():
    pattern = fc.PatternSet("baby-bib-set")
    everything = target_piece == "set"
    want = {
        "bandana": everything or target_piece == "bandana",
        "band": everything or target_piece == "band",
    }
    if not any(want.values()):
        want = dict.fromkeys(want, True)
    if want["bandana"]:
        pattern.add(build_bandana())
    if want["band"]:
        pattern.add(build_band())

    if want["band"]:
        pattern.declare_seam(("band", "lower"), ("band", "upper"), tol=0.3)

    fabric_width = 1400.0
    total_area = sum(
        p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
        for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "cotton face + cotton terry backing",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 62% marker; a printed cotton "
                 f"face over a terry backing — the terry catches drool."},
        {"item": "sew-on snap", "qty": 2, "unit": "pair",
         "note": f"Yantra4D sew-on-snap (notion.hardware_ref) at "
                 f"{snap_diameter:.0f} mm; TWO stud positions ({snap_step:.0f} mm "
                 f"apart) so one bib fits a growing neck. snap_dia fed from "
                 f"snap_diameter, the same number that sets the band overlap."},
        {"item": "ballpoint needle 70/10 + thread", "qty": 1, "unit": "spool",
         "note": f"bind the bandana edge; {TOPSTITCH:.0f} mm topstitch at the point."},
    ]
    pattern.metadata = {
        "fc400_rank": 325,
        "family": "kids_baby",
        "tier": 1,
        "fabric_hint": "cotton-terry",
        "finished_mm": {
            "bandana_width": round(bandana_width, 1),
            "bandana_drop": round(DROP, 1),
            "band_length": round(BAND_LEN, 1),
            "band_width": round(band_width, 1),
        },
        "solved": {
            "band_length_mm": round(BAND_LEN, 2),
            "snap_overlap_mm": round(SNAP_OVERLAP, 2),
            "snap_tight_x_mm": round(SNAP1_X, 2),
            "snap_loose_x_mm": round(SNAP2_X, 2),
            "snap_growth_step_mm": round(snap_step, 2),
            "drop_requested_mm": round(_DROP_RAW, 2),
            "drop_clamped_mm": round(DROP, 2),
            "drop_was_clamped": bool(abs(DROP - _DROP_RAW) > 0.01),
            "note": "the neck band carries TWO solved snap positions (tight and "
                    "loose, a growth step apart), both placed so neither lands off "
                    "the band, so one bib fits a range as the baby grows. The "
                    "bandana drop is floored above the band so it always covers the "
                    "chest and clamped below a maximum so it cannot trail in the "
                    "food — a drop larger than the piece inverts it, geometry the "
                    "kernel CCW-normalizes into a valid-looking piece.",
        },
        "hardware": "sew-on snaps via Yantra4D (notion.hardware_ref -> sew-on-snap); "
                    "the solid's snap_dia — its sewn flange dimension — is fed from "
                    "this garment's snap_diameter, which ALSO sets the band overlap, "
                    "so the same number flows to both sewn edges.",
    }
    return pattern


result = build()
