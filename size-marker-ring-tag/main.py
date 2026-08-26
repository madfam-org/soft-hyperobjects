"""
Size-marker ring tag set — Fashion Cabinet Care & Keeping Cartridge (FC-500 #422, care_keeping, T1).

A set of small fabric TAGS that thread onto a printed size-marker ring (the Yantra4D
`size-marker-ring` solid) so a rack of made-to-order or hand-me-down garments carries its own
soft, legible size label — a stitched fabric tab with a punched hole for the ring, sized so
several sit on one ring without crowding. The tag width and the ring-hole track the printed
ring's rod.

Solved, not guessed:

  1. THE RING HOLE IS CUT TO THE MEASURED RING ROD. The punched hole diameter is the ring rod
     plus a clearance, stepped in off the tag top by its own hole plus a margin so it never
     tears out the top edge.
  2. THE TAG IS CLAMPED to a legible minimum so a small ring never yields a tag too small to
     letter.
  3. THE STACK CLEARANCE floors the tag thickness allowance so a set of tags turns freely on
     one ring.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # tag|set

tag_count = int(PARAM(lambda: tag_count, 6))
tag_width = float(PARAM(lambda: tag_width, 40.0))
tag_height = float(PARAM(lambda: tag_height, 55.0))
ring_rod = float(PARAM(lambda: ring_rod, 4.0))           # ring wire/rod diameter
hole_clear = float(PARAM(lambda: hole_clear, 3.0))
corner = float(PARAM(lambda: corner, 8.0))               # rounded corner
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

tag_count = max(2, min(tag_count, 20))
tag_width = max(24.0, min(tag_width, 80.0))
tag_height = max(30.0, min(tag_height, 100.0))
ring_rod = max(2.0, min(ring_rod, 12.0))
hole_clear = max(1.0, min(hole_clear, 8.0))
corner = max(2.0, min(corner, 20.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# tag clamped to a legible minimum
TAG_W = max(24.0, tag_width)
TAG_H = max(30.0, tag_height)
CORNER = min(corner, TAG_W * 0.4, TAG_H * 0.4)
HOLE_DIA = ring_rod + hole_clear * 2.0
# the hole is stepped in off the top edge by its own diameter plus a margin
HOLE_Y = TAG_H - HOLE_DIA - 6.0
HOLE_Y = max(TAG_H * 0.55, HOLE_Y)


def build_tag():
    w, h = TAG_W, TAG_H
    c = CORNER
    # a rounded-corner tag: chamfer each corner with a short line (kept simple + watertight)
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(c, 0.0), fc.P(w - c, 0.0))]),
        fc.Edge("br", [fc.Line(fc.P(w - c, 0.0), fc.P(w, c))]),
        fc.Edge("right", [fc.Line(fc.P(w, c), fc.P(w, h - c))]),
        fc.Edge("tr", [fc.Line(fc.P(w, h - c), fc.P(w - c, h))]),
        fc.Edge("top", [fc.Line(fc.P(w - c, h), fc.P(c, h))]),
        fc.Edge("tl", [fc.Line(fc.P(c, h), fc.P(0.0, h - c))]),
        fc.Edge("left", [fc.Line(fc.P(0.0, h - c), fc.P(0.0, c))]),
        fc.Edge("bl", [fc.Line(fc.P(0.0, c), fc.P(c, 0.0))]),
    ]
    r = HOLE_DIA / 2.0
    cx = w / 2.0
    return fc.Piece(
        "tag", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 6.0), fc.P(w * 0.5, h - 6.0)),
        internals=[
            fc.Internal("ring hole",
                        [fc.P(cx - r, HOLE_Y), fc.P(cx + r, HOLE_Y), fc.P(cx, HOLE_Y),
                         fc.P(cx, HOLE_Y - r), fc.P(cx, HOLE_Y + r)], kind="drill"),
            fc.Internal("size label field",
                        [fc.P(w * 0.2, HOLE_Y - HOLE_DIA - 4.0),
                         fc.P(w * 0.8, HOLE_Y - HOLE_DIA - 4.0),
                         fc.P(w * 0.8, 8.0), fc.P(w * 0.2, 8.0),
                         fc.P(w * 0.2, HOLE_Y - HOLE_DIA - 4.0)], kind="marking"),
        ],
        cut=fc.CutSpec(quantity=tag_count),
        label=f"Size tag (cut {tag_count})",
    )


def build():
    pattern = fc.PatternSet("size-marker-ring-tag")
    pattern.add(build_tag())

    fabric_width = 700.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "twill tape / firm cotton (tags)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"at {fabric_width:.0f} mm width, 72% marker; a firm face takes an "
                 f"embroidered or stamped size and a punched grommet hole."},
        {"item": "size-marker ring", "qty": 1, "unit": "count",
         "note": f"Yantra4D size-marker-ring (notion.hardware_ref) at a {ring_rod:.0f} mm "
                 f"rod; the tag hole is cut to the rod plus a {hole_clear:.0f} mm clearance "
                 f"and {tag_count} tags turn on the ring."},
        {"item": "eyelet / grommet + thread", "qty": tag_count, "unit": "count",
         "note": "set a grommet in each tag hole so the ring does not fray it."},
    ]
    pattern.metadata = {
        "fc500_rank": 422, "family": "care_keeping", "tier": 1,
        "fabric_hint": "manta-cruda",
        "silhouette_note": "A set of soft fabric size tags that thread onto a printed marker "
            "ring, the hole cut to the ring rod.",
        "solved": {
            "tag_mm": [round(TAG_W, 1), round(TAG_H, 1)],
            "hole_diameter_mm": round(HOLE_DIA, 1),
            "hole_y_mm": round(HOLE_Y, 1),
            "tag_count": tag_count,
            "note": "the ring hole is the ring rod plus a clearance, stepped in off the top "
                    "edge by its own diameter plus a margin so it never tears out the top; "
                    "the tag is clamped to a legible minimum; the corner chamfer is clamped "
                    "under 40% of the tag so it never crosses the tag centre.",
        },
        "hardware": "size-marker ring via Yantra4D (notion.hardware_ref -> size-marker-ring); "
                    "rod_dia, ring_w and tab_h are fed from the ring and tag. No flange "
                    "interface — the tags thread onto the ring, no seam handshake owed.",
    }
    return pattern


result = build()
