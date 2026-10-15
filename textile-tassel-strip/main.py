"""Textile tassel strip. Original flat construction study.
Cut the outer rectangle and the nineteen marked fringe slits, preserving the upper 20 percent as an uncut header. Roll and bind the header; joining and shedding need making tests.
"""

SLUG = "textile-tassel-strip"
DEFAULT_L = 100
DEFAULT_W = 45

import fc


def PARAM(getter, default):
    try:
        return getter()
    except NameError:
        return default


L = float(PARAM(lambda: length, DEFAULT_L))  # noqa: F821
W = float(PARAM(lambda: width, DEFAULT_W))  # noqa: F821
if (
    not DEFAULT_L * 0.8 <= L <= DEFAULT_L * 1.2
    or not DEFAULT_W * 0.8 <= W <= DEFAULT_W * 1.2
):
    raise ValueError("Dimensions outside the reviewed study domain")
if L <= W:
    raise ValueError("Length must exceed width")
result = fc.PatternSet(SLUG)


def poly(name, points, sa=0, qty=1, marks=None):
    p = [fc.P(x, y) for x, y in points]
    edges = [
        fc.Edge("e" + str(i), [fc.Line(p[i], p[(i + 1) % len(p)])])
        for i in range(len(p))
    ]
    internals = [
        fc.Internal("mark-" + str(i), [fc.P(x, y) for x, y in line], kind="marking")
        for i, line in enumerate(marks or [])
    ]
    xmin = min(x for x, y in points)
    xmax = max(x for x, y in points)
    ymin = min(y for x, y in points)
    ymax = max(y for x, y in points)
    gx = (xmin + xmax) / 2
    gy = (ymin + ymax) / 2
    span = (xmax - xmin) * 0.1
    piece = fc.Piece(
        name,
        edges,
        seam_allowance=sa,
        cut=fc.CutSpec(quantity=qty),
        label=name,
        internals=internals,
        grainline=fc.Grainline(fc.P(gx - span, gy), fc.P(gx + span, gy)),
    )
    result.add(piece)
    result.bom.append(
        {
            "item": name,
            "qty": qty,
            "unit": "count",
            "note": "Cut in selected textile; physical making unqualified",
        }
    )
    return piece


def rect(name, l, w, sa=0, qty=1, marks=None):
    return poly(name, [(0, 0), (l, 0), (l, w), (0, w)], sa, qty, marks)


rect(
    "fringe",
    L,
    W,
    marks=[[(L * i / 20, 0), (L * i / 20, W * 0.8)] for i in range(1, 20)],
)
result.metadata = {
    "length_mm": L,
    "width_mm": W,
    "making_qualified": False,
    "representation": "native flat pattern or construction guide",
    "construction": "Cut the outer rectangle and the nineteen marked fringe slits, preserving the upper 20 percent as an uncut header. Roll and bind the header; joining and shedding need making tests.",
}
