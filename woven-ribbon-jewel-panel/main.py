"""Original ribbon-weave ornament: flat cut strips and a marked textile backing.

This is a 2D cutting/placement guide. It does not solve ribbon take-up, drape,
adhesive strength, hand tacks, skin contact or attachment to jewellery hardware.
"""

import math

import fc


def PARAM(getter, default):
    try:
        value = getter()
        return default if value is None else value
    except NameError:
        return default


def dimension(value, low, high, name):
    value = float(value)
    if not math.isfinite(value) or value < low or value > high:
        raise ValueError(name + " is outside the supported range")
    return value


ribbon_width = dimension(PARAM(lambda: ribbon_width, 6), 4, 12, "ribbon_width")
gap = dimension(PARAM(lambda: gap, 0.5), 0, 3, "gap")
tail = dimension(PARAM(lambda: tail, 12), 10, 30, "tail")
columns_value = dimension(PARAM(lambda: columns, 5), 4, 12, "columns")
rows_value = dimension(PARAM(lambda: rows, 7), 4, 16, "rows")
if columns_value != int(columns_value) or rows_value != int(rows_value):
    raise ValueError("rows and columns must be integers")
columns = int(columns_value)
rows = int(rows_value)
target_piece = str(PARAM(lambda: target_piece, "set"))
if target_piece not in ("set", "warp", "weft", "backing"):
    raise ValueError("unknown target_piece")

pitch = ribbon_width + gap
panel_width = columns * ribbon_width + (columns - 1) * gap
panel_height = rows * ribbon_width + (rows - 1) * gap
warp_length = panel_height + 2 * tail
weft_length = panel_width + 2 * tail


def rectangle(name, width, height, quantity, marks, label):
    points = [fc.P(0, 0), fc.P(width, 0), fc.P(width, height), fc.P(0, height)]
    names = ["bottom", "right", "top", "left"]
    return fc.Piece(
        name,
        [fc.Edge(names[i], [fc.Line(points[i], points[(i + 1) % 4])]) for i in range(4)],
        seam_allowance=0,
        grainline=fc.Grainline(fc.P(width / 2, height * 0.15), fc.P(width / 2, height * 0.85)),
        internals=marks,
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def strip(name, length, quantity, crossings):
    marks = [fc.Internal("tail boundary", [fc.P(0, y), fc.P(ribbon_width, y)])
             for y in (tail, length - tail)]
    for i in range(crossings):
        y = tail + i * pitch + ribbon_width / 2
        marks.append(fc.Internal("crossing centre " + str(i + 1),
                                 [fc.P(0, y), fc.P(ribbon_width, y)]))
    return rectangle(name, ribbon_width, length, quantity, marks,
                     name + ": cut " + str(quantity) + "; flat length " + str(length) + " mm")


pattern = fc.PatternSet("woven-ribbon-jewel-panel")
if target_piece in ("set", "warp"):
    pattern.add(strip("warp", warp_length, columns, rows))
if target_piece in ("set", "weft"):
    pattern.add(strip("weft", weft_length, rows, columns))
if target_piece in ("set", "backing"):
    marks = []
    for c in range(columns):
        x = tail + c * pitch
        marks.append(fc.Internal("warp " + str(c + 1) + " placement",
                                 [fc.P(x, tail), fc.P(x + ribbon_width, tail),
                                  fc.P(x + ribbon_width, tail + panel_height),
                                  fc.P(x, tail + panel_height), fc.P(x, tail)]))
    for r in range(rows):
        y = tail + r * pitch + ribbon_width / 2
        marks.append(fc.Internal("weft " + str(r + 1) + " centre",
                                 [fc.P(tail, y), fc.P(tail + panel_width, y)]))
    pattern.add(rectangle("backing", weft_length, warp_length, 1, marks,
                         "Textile backing: cut 1; marked placement guide"))

crossings = []
for r in range(rows):
    for c in range(columns):
        crossings.append({"row": r + 1, "column": c + 1,
                          "weft": "over" if (r + c) % 2 == 0 else "under",
                          "centre_mm": [tail + c * pitch + ribbon_width / 2,
                                        tail + r * pitch + ribbon_width / 2]})

pattern.bom = [
    {"item": "Finished-edge ribbon, warp", "qty": columns * warp_length, "unit": "mm_length",
     "note": str(columns) + " strips x " + str(warp_length) + " mm, width " + str(ribbon_width) + " mm"},
    {"item": "Finished-edge ribbon, weft", "qty": rows * weft_length, "unit": "mm_length",
     "note": str(rows) + " strips x " + str(weft_length) + " mm, width " + str(ribbon_width) + " mm"},
    {"item": "Non-fraying textile backing", "qty": weft_length * warp_length, "unit": "mm2",
     "note": "One backing rectangle; no automatic waste or purchasing allowance"},
]
pattern.metadata = {
    "family": "jewellery_ribbon_weave", "ranked": False,
    "representation": "2d-cutting-and-placement-guide", "manufacturing_qualified": False,
    "resolved_params": {"ribbon_width": ribbon_width, "gap": gap, "tail": tail,
                        "columns": columns, "rows": rows},
    "solved": {"panel_width_mm": panel_width, "panel_height_mm": panel_height,
               "warp_strip_length_mm": warp_length, "weft_strip_length_mm": weft_length,
               "ribbon_total_length_mm": columns * warp_length + rows * weft_length,
               "crossing_count": rows * columns, "cut_ribbon_count": rows + columns},
    "crossings": crossings,
    "construction": [
        "Cut the strip quantities on the templates from finished-edge ribbon. Cut one textile backing.",
        "Place warp strips vertically on the backing marks; tails extend beyond the marked panel.",
        "Starting at the bottom, weave row 1 over column 1, under column 2; alternate every crossing.",
        "Reverse the starting order on every next row; consult the numbered crossing table.",
        "Secure loose ends to the backing by hand tacks after sampling. No continuous sewn seam is claimed.",
        "Check the sample and choose an independently validated attachment before wearing.",
    ],
    "limits": ["Flat lengths exclude material-dependent weave take-up; tails are adjustable reserves, not a prediction.",
               "No drape or friction solver, no tested tacks, no hardware attachment or wearable safety qualification.",
               "Subset exports retain the full-assembly BOM and crossing table."],
}
result = pattern
