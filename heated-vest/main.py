"""
Heated Vest — Fashion Cabinet Garment Cartridge (FC-200 rank #146, y4d battery-holder).

A softshell vest prepared for heating: a sleeveless front + back with a front opening,
overlaid with CONDUCTIVE HEATING ROUTES (marked serpentine traces across the back and
chest that a heating element follows) and a BATTERY POCKET whose opening is sized to the
Yantra4D `battery-holder`. Fashion Cabinet owns the vest + routing; Yantra4D owns the
printable battery holder.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 1040.0))  # full chest
vest_length  = float(PARAM(lambda: vest_length, 640.0))   # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 190.0))    # neck opening
shoulder_w   = float(PARAM(lambda: shoulder_w, 120.0))    # half shoulder
armhole_drop = float(PARAM(lambda: armhole_drop, 280.0))  # armhole depth
vest_ease    = float(PARAM(lambda: vest_ease, 120.0))     # layering ease
battery_w    = float(PARAM(lambda: battery_w, 80.0))      # battery-pocket opening width
heat_zones   = int(  PARAM(lambda: heat_zones, 3))        # heating-route zones
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(700.0, min(chest_girth, 1600.0))
vest_length  = max(420.0, min(vest_length, 900.0))
neck_width   = max(120.0, min(neck_width, 320.0))
shoulder_w   = max(80.0, min(shoulder_w, 200.0))
armhole_drop = max(200.0, min(armhole_drop, 420.0))
vest_ease    = max(40.0, min(vest_ease, 360.0))
battery_w    = max(40.0, min(battery_w, 160.0))
heat_zones   = max(1, min(heat_zones, 6))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = vest_length
HALF = (chest_girth + vest_ease) / 2.0 / 2.0
NECK_HALF = neck_width / 2.0


def _panel(name, neck_dip, is_front, with_battery, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_pt = fc.P(shoulder_w, top_y - 8.0)
    underarm = fc.P(HALF, top_y - armhole_drop)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, shoulder_pt)]),
        fc.Edge("armhole", [fc.curve_through(shoulder_pt, underarm, bulge=0.18, side=1.0)]),
        fc.Edge("side", [fc.Line(underarm, fc.P(HALF, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # Heating routes: serpentine traces (zones) across the panel.
    for z in range(heat_zones):
        y0 = L * (0.25 + 0.5 * z / max(heat_zones, 1))
        internals.append(fc.Internal(f"heat-route-{z}", [
            fc.P(HALF * 0.15, y0), fc.P(HALF * 0.85, y0),
            fc.P(HALF * 0.85, y0 + 30.0), fc.P(HALF * 0.15, y0 + 30.0)], kind="trace"))
    if with_battery:
        # Battery pocket low on the front (near the hem/side).
        bx, by = HALF * 0.55, L * 0.22
        h = battery_w / 2.0
        internals.append(fc.Internal("battery-pocket", [
            fc.P(bx - h, by - h * 0.6), fc.P(bx + h, by - h * 0.6),
            fc.P(bx + h, by + h * 0.6), fc.P(bx - h, by + h * 0.6),
            fc.P(bx - h, by - h * 0.6)], kind="marking"))
    if is_front:
        internals.append(fc.Internal("front-opening",
                                     [fc.P(0.0, 0.0), fc.P(0.0, top_y - neck_dip)], kind="marking"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("armhole", 0.0, "shoulder"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=(not is_front), fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("heated-vest")
    front = _panel("front", 90.0, True, True, "Front (with battery pocket)")
    back = _panel("back", 25.0, False, False, "Back (with heating zones)")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.5)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.5)
    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "softshell (conductive-thread compatible lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; see the fabric card's e_textile block."},
        {"item": "heating element + conductive thread", "qty": 1, "unit": "set",
         "note": "route the element along the marked serpentine heat zones."},
        {"item": "battery holder", "qty": 1, "unit": "count",
         "note": "Yantra4D battery-holder (see notion.hardware_ref) drops into the pocket."},
        {"item": "front zip + controller", "qty": 1, "unit": "set", "note": "maker's choice."},
    ]
    pattern.metadata = {
        "fc200_rank": 146, "family": "etextile", "fabric_hint": "nylon-ripstop-shell",
        "etextile_note": "Base vest + marked serpentine HEATING ROUTES (the element path) + "
            "a BATTERY POCKET sized to the Yantra4D battery-holder. Routes and pocket are "
            "MARKED for the maker; no electronics/heating element is drafted here.",
        "hardware": "battery holder via Yantra4D (notion.hardware_ref -> battery-holder)",
    }
    return pattern


result = build()
