"""Original planar cord-couching ornament; mm, y-up, no assembly solver."""
import math

import fc


def PARAM(getter, default):
    try:
        value = getter()
        return default if value is None else value
    except NameError:
        return default


width = float(PARAM(lambda: width, 50))
height = float(PARAM(lambda: height, 26))
amplitude = float(PARAM(lambda: amplitude, 6))
waves = float(PARAM(lambda: waves, 3))
cord_diameter = float(PARAM(lambda: cord_diameter, 1.5))
stitch_spacing = float(PARAM(lambda: stitch_spacing, 4))
tail_allowance = float(PARAM(lambda: tail_allowance, 8))

for value, low, high in [
    (width, 30, 150), (height, 16, 80), (amplitude, 2, 25),
    (waves, 1, 6), (cord_diameter, 0.5, 3),
    (stitch_spacing, 2, 8), (tail_allowance, 3, 25),
]:
    if not math.isfinite(value) or value < low or value > high:
        raise ValueError("Parameter outside the declared finite range")
if waves != int(waves):
    raise ValueError("waves must be a whole number")
waves = int(waves)
margin = 4 + cord_diameter / 2
if 2 * (amplitude + margin) > height:
    raise ValueError("Foundation height must contain the route and cord margin")
run = width - 2 * margin
if run / waves < 4 * cord_diameter:
    raise ValueError("Wave pitch must be at least four cord diameters")

# The exported polyline IS the authored route; its measured length drives the BOM.
samples = waves * 96
route = [fc.P(margin + run * i / samples,
              height / 2 + amplitude * math.sin(2 * math.pi * waves * i / samples))
         for i in range(samples + 1)]
lengths = [math.hypot(route[i + 1].x - route[i].x,
                      route[i + 1].y - route[i].y) for i in range(samples)]
route_length = sum(lengths)
stitch_intervals = math.ceil(route_length / stitch_spacing)
marks = [fc.Internal("cord-center-route", route, kind="trace")]
# Equal arc-length attachment stations; mark spans show stitch direction only.
segment = 0
before = 0.0
for station in range(stitch_intervals + 1):
    distance = route_length * station / stitch_intervals
    while segment < samples - 1 and before + lengths[segment] < distance:
        before += lengths[segment]
        segment += 1
    a, b = route[segment], route[segment + 1]
    fraction = min(1.0, max(0.0, (distance - before) / lengths[segment]))
    x, y = a.x + (b.x - a.x) * fraction, a.y + (b.y - a.y) * fraction
    nx, ny = -(b.y - a.y) / lengths[segment], (b.x - a.x) / lengths[segment]
    half_span = cord_diameter / 2 + 0.75
    marks.append(fc.Internal(f"couch-stitch-{station + 1}", [
        fc.P(x - nx * half_span, y - ny * half_span),
        fc.P(x + nx * half_span, y + ny * half_span)], kind="marking"))

corners = [fc.P(0, 0), fc.P(width, 0), fc.P(width, height), fc.P(0, height)]
edges = [fc.Edge(name, [fc.Line(corners[i], corners[(i + 1) % 4])])
         for i, name in enumerate(["bottom", "right", "top", "left"])]
piece = fc.Piece("foundation", edges, seam_allowance=0,
                 internals=marks, cut=fc.CutSpec(quantity=1),
                 grainline=fc.Grainline(fc.P(2, 3), fc.P(2, height - 3)),
                 label="Cord-couching ornament foundation")
result = fc.PatternSet("cord-couching-ornament")
result.add(piece)
result.bom = [
    {"item": "non-fraying textile foundation", "quantity": 1, "unit": "piece",
     "area_mm2": width * height},
    {"item": "ornamental cord", "quantity": route_length + 2 * tail_allowance,
     "unit": "mm", "diameter_mm": cord_diameter,
     "route_length_mm": route_length, "tail_allowance_each_mm": tail_allowance},
    {"item": "couching attachment stations", "quantity": stitch_intervals + 1,
     "unit": "station", "thread_length": "not estimated; choose by material trial"},
]
result.metadata = {
    "resolved_parameters": {"width": width, "height": height, "amplitude": amplitude,
                            "waves": waves, "cord_diameter": cord_diameter,
                            "stitch_spacing": stitch_spacing, "tail_allowance": tail_allowance},
    "solved": {"route_length_mm": route_length,
               "cord_cut_length_mm": route_length + 2 * tail_allowance,
               "stitch_stations": stitch_intervals + 1,
               "actual_stitch_spacing_mm": route_length / stitch_intervals,
               "route_segments": samples},
    "construction": ["Cut one non-fraying textile foundation along its outline.",
                     "Transfer the cord center route and transverse stitch marks.",
                     "Cut the cord to the BOM length including two tail allowances.",
                     "Lay cord on the route; couch at each transverse station.",
                     "Turn both tails to the reverse and secure by a material-tested finish."],
    "verification_scope": "Planar foundation and route only; surface stitches are not paired edge seams.",
    "limits": "No closure, wear attachment, knot topology, drape, thread consumption, minimum bend radius or strength qualification.",
    "manufacturing_qualified": False,
}
