"""
Kilt (wrap) — Fashion Cabinet Garment Cartridge (FC-200 rank #155, Scottish heritage).

The kilt is the knee-length wrapped garment of Scottish Highland dress: a long length of
(traditionally tartan) cloth with a flat un-pleated apron at the front, deep knife pleats
across the back, wrapped around the waist and buckled at the side. This cartridge drafts
the GARMENT GEOMETRY as a single flat length whose back section is marked for knife pleats
and whose front is the flat apron, with the wrap overlap and strap positions marked. The
tartan sett, the pleating-to-the-stripe, and the regional/clan meaning are the maker's and
are not reproduced here. Offered with respect for the living tradition.

Pieces:
  - length : one long rectangle (the kilt cloth), pleat lines + apron + straps marked.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # length|set

waist_girth  = float(PARAM(lambda: waist_girth, 880.0))    # fitted waist
hip_girth    = float(PARAM(lambda: hip_girth, 1000.0))     # seat (pleats give hip room)
kilt_length  = float(PARAM(lambda: kilt_length, 570.0))    # waist to mid-knee
apron_width  = float(PARAM(lambda: apron_width, 360.0))    # flat front apron width
pleat_depth  = float(PARAM(lambda: pleat_depth, 130.0))    # depth folded into each knife pleat
pleats       = int(  PARAM(lambda: pleats, 24))            # number of back knife pleats
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(600.0, min(waist_girth, 1500.0))
hip_girth    = max(700.0, min(hip_girth, 1600.0))
kilt_length  = max(420.0, min(kilt_length, 750.0))
apron_width  = max(250.0, min(apron_width, 520.0))
pleat_depth  = max(60.0, min(pleat_depth, 220.0))
pleats       = max(12, min(pleats, 40))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

# Flat length = under-apron + flat apron + pleated back (each pleat consumes pleat_depth of
# extra cloth folded to a face-width). The pleated back covers roughly half the seat.
UNDER_APRON = apron_width * 0.9
BACK_COVER = hip_girth / 2.0
PLEAT_FACE = BACK_COVER / pleats
FLAT_LEN = UNDER_APRON + apron_width + pleats * (PLEAT_FACE + pleat_depth)
L = kilt_length


def build_length():
    internals = []
    # apron edge (front apron begins after the under-apron)
    x_apron = UNDER_APRON
    internals.append(fc.Internal("apron-fold", [fc.P(x_apron, 0.0), fc.P(x_apron, L)],
                                 kind="fold"))
    x_pleats = UNDER_APRON + apron_width
    internals.append(fc.Internal("pleats-begin", [fc.P(x_pleats, 0.0), fc.P(x_pleats, L)],
                                 kind="marking"))
    # each knife pleat: a fold line + a placement line, one PLEAT_FACE+pleat_depth apart
    x = x_pleats
    for i in range(pleats):
        internals.append(fc.Internal(f"pleat-fold-{i}",
                                     [fc.P(x, 0.0), fc.P(x, L)], kind="fold"))
        x += pleat_depth
        internals.append(fc.Internal(f"pleat-place-{i}",
                                     [fc.P(x, 0.0), fc.P(x, L)], kind="marking"))
        x += PLEAT_FACE
    # strap positions at the waist (buckled at the right side)
    internals.append(fc.Internal("strap-hi",
                                 [fc.P(x_apron, L - 20.0), fc.P(x_apron + 40.0, L - 20.0)],
                                 kind="marking"))
    return fc.Piece(
        "length",
        [
            fc.Edge("under_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(FLAT_LEN, L))]),
            fc.Edge("over_end", [fc.Line(fc.P(FLAT_LEN, L), fc.P(FLAT_LEN, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(FLAT_LEN, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.0, "under-apron edge"),
                 fc.Notch("waist", 1.0, "over-apron edge")],
        grainline=fc.Grainline(fc.P(FLAT_LEN * 0.5, 60.0), fc.P(FLAT_LEN * 0.5, L - 60.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Kilt length",
    )


def build():
    pattern = fc.PatternSet("kilt-wrap")
    pattern.add(build_length())
    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.80)
    pattern.bom = [
        {"item": "tartan or worsted wool (or wool-blend)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 80% marker; one long length, back knife-pleated."},
        {"item": "kilt straps + buckles", "qty": 2, "unit": "sets",
         "note": "two straps buckle the apron over at the right side; positions marked."},
        {"item": "waistband canvas / stiffening", "qty": 1, "unit": "as needed",
         "note": "the waist is stabilised; interfacing is the maker's choice."},
        {"item": "all-purpose + buttonhole thread", "qty": 1, "unit": "set",
         "note": "pleats are stitched down over the hip, free below."},
    ]
    pattern.metadata = {
        "fc200_rank": 155,
        "family": "heritage_global",
        "fabric_hint": "lana-tartan",
        "heritage_note": "The kilt is part of living Scottish Highland dress. This cartridge "
            "drafts the GARMENT GEOMETRY only — the tartan sett, pleating-to-the-stripe or "
            "-to-the-sett, and clan/regional meaning are the maker's and are not reproduced "
            "here. Offered with respect.",
        "construction": "one flat length: an under-apron and a flat front apron, then knife "
            "pleats across the back stitched down over the hip; buckled at the side.",
        "solved": {"flat_length_mm": round(FLAT_LEN, 1), "pleats": pleats,
                   "pleat_face_mm": round(PLEAT_FACE, 1), "pleat_depth_mm": round(pleat_depth, 1),
                   "back_cover_mm": round(BACK_COVER, 1)},
    }
    return pattern


result = build()
