"""Original shield-shaped beadwork foundation and flush backing, in millimetres."""

import fc


def PARAM(getter, default):
    try:
        value = getter()
        return default if value is None else value
    except NameError:
        return default


length = float(PARAM(lambda: length, 70.0))
width = float(PARAM(lambda: width, 45.0))
embroidery_margin = float(PARAM(lambda: embroidery_margin, 5.0))
attachment_spacing = float(PARAM(lambda: attachment_spacing, 18.0))
if not 35 <= length <= 140 or not 25 <= width <= 100:
    raise ValueError("Foundation length or width outside the declared range")
if not 3 <= embroidery_margin <= 12 or embroidery_margin >= min(width, length) / 4:
    raise ValueError("Embroidery margin must be below one quarter of the smaller dimension")
if not 8 <= attachment_spacing <= 50 or attachment_spacing > width * 0.6:
    raise ValueError("Attachment spacing must fit within 60 percent of the width")

# Seven straight edges define a shield with a pointed lower end and flat top.
# Counterclockwise vertices; all edge names remain stable as dimensions change.
vertices = [(-width / 2, length * 0.35), (0, 0),
            (width / 2, length * 0.35), (width / 2, length * 0.8),
            (width * 0.3, length), (-width * 0.3, length),
            (-width / 2, length * 0.8)]
edge_names = ["lower-left", "lower-right", "right", "shoulder-right",
              "top", "shoulder-left", "left"]
# The beading field is a homothetic inset, NOT an equidistant offset.
# The margin controls the contraction on the bounding rectangle explicitly.
scale = 1 - 2 * embroidery_margin / min(width, length)
field = [fc.P(x * scale, length / 2 + (y - length / 2) * scale)
         for x, y in vertices]
field.append(field[0])
attachment_y = length * 0.83


def piece(name, label):
    edges = [fc.Edge(edge_names[i], [fc.Line(fc.P(*vertices[i]),
                                           fc.P(*vertices[(i + 1) % len(vertices)]))])
             for i in range(len(vertices))]
    marks = [fc.Internal("beading-field-homothetic", field, kind="trace"),
             fc.Internal("vertical-registration", [fc.P(0, length * 0.2),
                                                    fc.P(0, length * 0.7)])]
    for i, x in enumerate([-attachment_spacing / 2, attachment_spacing / 2]):
        marks.append(fc.Internal(f"attachment-{i}-horizontal",
                                 [fc.P(x - 1, attachment_y), fc.P(x + 1, attachment_y)],
                                 kind="marking"))
        marks.append(fc.Internal(f"attachment-{i}-vertical",
                                 [fc.P(x, attachment_y - 1), fc.P(x, attachment_y + 1)],
                                 kind="marking"))
    return fc.Piece(name, edges, seam_allowance=0,
                    notches=[fc.Notch("top", 0.5, "centre registration")],
                    grainline=fc.Grainline(fc.P(0, length * 0.35),
                                          fc.P(0, length * 0.65)),
                    internals=marks, cut=fc.CutSpec(quantity=1), label=label)


result = fc.PatternSet("bead-embroidery-foundation")
result.add(piece("foundation", "Beadwork foundation"))
result.add(piece("backing", "Flush backing"))
# Edge-overcast assembly: same cut/stitch perimeter on both layers, no turned seam.
for edge in edge_names:
    result.declare_seam(("foundation", edge), ("backing", edge), tol=0.2)
result.bom = [
    {"item": "non-fraying beadwork foundation", "qty": 1, "unit": "piece"},
    {"item": "non-fraying soft backing", "qty": 1, "unit": "piece"},
    {"item": "beads and stitching thread", "qty": 1, "unit": "design-dependent set",
     "note": "Bead layout, mass and thread consumption are not solved by this pattern."},
]
result.metadata = {
    "classification": "unranked jewellery technique enabler",
    "resolved_parameters": {"length": length, "width": width,
                            "embroidery_margin": embroidery_margin,
                            "attachment_spacing": attachment_spacing},
    "solved": {"field_scale": scale, "attachment_y_mm": attachment_y,
               "attachment_spacing_mm": attachment_spacing,
               "foundation_area_mm2": result.piece("foundation").area()},
    "construction": ["Cut one foundation and one flush backing from non-fraying material.",
                     "Transfer centre, beading field and attachment crosses; crosses are marks, not holes.",
                     "Embroider the foundation, keeping thread ends away from the outer edge.",
                     "Align the backing and edge-overcast every corresponding named perimeter edge.",
                     "Use the two marks to plan attachment; choose and test attachment hardware separately."],
    "limits": ["The field is a proportional inset, not a constant-width edge clearance.",
               "Bead layout, attachment strength, skin contact and wear durability remain unverified.",
               "No hard goods or cultural pattern are modelled; no production or maker qualification."],
}
