"""
Boot-hook pull tab — Fashion Cabinet Cartridge (FC-500 #425, footwear_soft, T2).

The finger loop sewn at the back top of a tall boot that a boot-hook (the Yantra4D
`boot-hook-puller`) catches to pull the boot on. A folded leather TAB with a reinforced
HOLE that the hook's blade passes through, and a stitched ATTACH end that beds into the boot
back seam. Sized to the hook blade so the tool always passes cleanly.

Solved, not guessed:

  1. THE HOLE IS CUT TO THE MEASURED HOOK BLADE. The hole width is the blade width plus a
     clearance and the hole is stepped in off the loop end by its own width plus a margin so
     it never tears out the fold.
  2. THE TAB LENGTH clears the hook reach so the loop stands proud of the boot back for the
     hook to catch, floored so it always makes a real loop.
  3. THE TAB WIDTH is clamped to at least the hole width plus the reinforcement.

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


target_piece = str(PARAM(lambda: target_piece, "set"))  # tab|facing|set

blade_width = float(PARAM(lambda: blade_width, 16.0))
blade_thick = float(PARAM(lambda: blade_thick, 5.0))
hook_reach = float(PARAM(lambda: hook_reach, 60.0))
tab_width = float(PARAM(lambda: tab_width, 34.0))
hole_clear = float(PARAM(lambda: hole_clear, 4.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

blade_width = max(8.0, min(blade_width, 40.0))
blade_thick = max(2.0, min(blade_thick, 12.0))
hook_reach = max(30.0, min(hook_reach, 120.0))
tab_width = max(20.0, min(tab_width, 60.0))
hole_clear = max(2.0, min(hole_clear, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

HOLE_W = blade_width + hole_clear * 2.0
HOLE_H = blade_thick + hole_clear * 2.0
TAB_W = max(HOLE_W + 16.0, tab_width)
# the tab length clears the hook reach so the loop stands proud, floored to a real loop
TAB_L = max(hook_reach + HOLE_H + 30.0, HOLE_H + 60.0)


def build_tab():
    w, h = TAB_W, TAB_L
    hole_y = h - HOLE_H - 12.0
    hole_y = max(h * 0.5, hole_y)
    return fc.Piece(
        "tab", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
            fc.Edge("right", [fc.Line(fc.P(w, 0.0), fc.P(w, h))]),
            fc.Edge("loop_end", [fc.Line(fc.P(w, h), fc.P(0.0, h))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CB seam")],
        grainline=fc.Grainline(fc.P(w * 0.5, 8.0), fc.P(w * 0.5, h - 8.0)),
        internals=[
            fc.Internal("hook hole",
                        [fc.P(w / 2.0 - HOLE_W / 2.0, hole_y),
                         fc.P(w / 2.0 + HOLE_W / 2.0, hole_y),
                         fc.P(w / 2.0 + HOLE_W / 2.0, hole_y + HOLE_H),
                         fc.P(w / 2.0 - HOLE_W / 2.0, hole_y + HOLE_H),
                         fc.P(w / 2.0 - HOLE_W / 2.0, hole_y)], kind="cut"),
            fc.Internal("fold line", [fc.P(0.0, h * 0.5), fc.P(w, h * 0.5)],
                        kind="marking"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Pull tab (cut 1, folded)",
    )


def build_facing():
    """A hole reinforcement facing, cut 1 (leather patch behind the hole)."""
    w = HOLE_W + 24.0
    h = HOLE_H + 24.0
    return fc.Piece(
        "facing", [
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 6.0), fc.P(w * 0.5, h - 6.0)),
        internals=[],
        cut=fc.CutSpec(quantity=1),
        label="Hole facing (cut 1)",
    )


def build():
    pattern = fc.PatternSet("boot-hook-pull-tab")
    everything = target_piece == "set"
    if everything or target_piece == "tab":
        pattern.add(build_tab())
    if everything or target_piece == "facing":
        pattern.add(build_facing())

    fabric_width = 800.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.5)
    pattern.bom = [
        {"item": "vegetable-tanned leather (tab)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"≈ at {fabric_width:.0f} mm width, 50% marker (small piece); a firm leather "
                 f"so the loop stands proud for the hook."},
        {"item": "boot-hook puller", "qty": 1, "unit": "count",
         "note": f"Yantra4D boot-hook-puller (notion.hardware_ref): the hole is cut to the "
                 f"hook blade ({blade_width:.0f} mm) plus a {hole_clear:.0f} mm clearance."},
        {"item": "waxed thread + rivet", "qty": 1, "unit": "set",
         "note": "the attach end beds into the boot back seam; the fold is riveted."},
    ]
    pattern.metadata = {
        "fc500_rank": 425, "family": "footwear_soft", "tier": 2,
        "fabric_hint": "cuero-vegetal",
        "silhouette_note": "A finger-loop pull tab sewn at the boot back, its hole cut to the "
            "boot-hook blade.",
        "solved": {
            "hole_mm": [round(HOLE_W, 1), round(HOLE_H, 1)],
            "tab_mm": [round(TAB_W, 1), round(TAB_L, 1)],
            "note": "the hole is the hook blade plus a clearance, stepped in off the loop end "
                    "so it never tears out the fold; the tab length clears the hook reach so "
                    "the loop stands proud, floored to a real loop; the tab width is clamped "
                    "to at least the hole plus reinforcement.",
        },
        "hardware": "boot-hook puller via Yantra4D (notion.hardware_ref -> boot-hook-puller); "
                    "blade_w and hook_r are fed from the blade and reach. No flange interface "
                    "— the hook passes through the tab hole, no seam handshake owed.",
    }
    return pattern


result = build()
