"""Ruffled mesh collar strip. Original flat construction study.
Gather the mesh along the marked line onto the shorter binding. The 2.22 gathering ratio is intentional; the gathered seam is a manual operation, not a matched-edge claim.
"""

SLUG = "ruffled-mesh-collar"
DEFAULT_L = 500
DEFAULT_W = 70

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


rect("mesh", L, W, marks=[[(0, W * 0.2), (L, W * 0.2)]])
rect("binding", L * 0.45, W * 0.12, sa=2)
result.metadata = {
    "length_mm": L,
    "width_mm": W,
    "making_qualified": False,
    "representation": "native flat pattern or construction guide",
    "construction": "Gather the mesh along the marked line onto the shorter binding. The 2.22 gathering ratio is intentional; the gathered seam is a manual operation, not a matched-edge claim.",
}

# Verify the complete construction before selecting a single-piece export.
# Cross-piece seams omitted from a subset are not claimed as subset checks.
selected = str(PARAM(lambda: target_piece, "pattern"))  # noqa: F821
if selected not in ["pattern", "mesh", "binding"]:
    raise ValueError("Unknown target_piece")
full_pattern = result
if any(issue["level"] == "error" for issue in full_pattern.verify()):
    raise ValueError("Full pattern verification failed before piece selection")
full_seam_count = len(full_pattern.seam_checks)
if selected != "pattern":
    result = fc.PatternSet(full_pattern.name)
    result.add(full_pattern.piece(selected))
    for seam in full_pattern.seam_checks:
        if all(name == selected for name, edge in seam.side_a + seam.side_b):
            result.declare_seam(
                seam.side_a, seam.side_b, tol=seam.tol_mm, ease=seam.ease_mm
            )
    result.bom = [item for item in full_pattern.bom if item["item"] == selected]
    result.metadata = dict(full_pattern.metadata)
result.metadata["dispatch"] = {
    "target_piece": selected,
    "scope": "full-set" if selected == "pattern" else "single-piece",
    "full_set_seams_verified": full_seam_count,
    "exported_seams": len(result.seam_checks),
    "cross_piece_seams_excluded": full_seam_count - len(result.seam_checks),
    "bom_scope": "full-assembly" if selected == "pattern" else "selected-pieces",
}
