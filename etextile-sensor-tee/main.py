"""
E-Textile Sensor Tee — Fashion Cabinet Garment Cartridge (FC-200 rank #145, y4d mount).

A relaxed knit tee prepared for wearable sensing: a boxy front + back with grown-on cap
sleeves (the base garment), overlaid with CONDUCTIVE-THREAD ROUTES (marked traces from a
chest sensor patch to a hem-hub bus) and a SENSOR-MOUNT POCKET whose opening is sized to
the Yantra4D `sensor-mount-plate` enclosure that snaps in. Fashion Cabinet owns the
garment + the routing plan; Yantra4D owns the printable mount.

The fabric card supplies the e_textile block (conductive-thread compatibility); this
cartridge draws the routes and the mount pocket the maker embroiders/sews with conductive
thread and a washable sensor.

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

chest_girth  = float(PARAM(lambda: chest_girth, 1000.0))  # full chest
tee_length   = float(PARAM(lambda: tee_length, 680.0))    # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 180.0))    # neck opening
sleeve_grown = float(PARAM(lambda: sleeve_grown, 150.0))  # grown cap sleeve
knit_ease    = float(PARAM(lambda: knit_ease, 60.0))      # close knit ease
mount_size   = float(PARAM(lambda: mount_size, 40.0))     # sensor-mount pocket opening
route_count  = int(  PARAM(lambda: route_count, 3))       # conductive trace count
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(700.0, min(chest_girth, 1500.0))
tee_length   = max(450.0, min(tee_length, 950.0))
neck_width   = max(120.0, min(neck_width, 320.0))
sleeve_grown = max(60.0, min(sleeve_grown, 260.0))
knit_ease    = max(0.0, min(knit_ease, 200.0))
mount_size   = max(20.0, min(mount_size, 90.0))
route_count  = max(1, min(route_count, 8))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = tee_length
HALF = (chest_girth + knit_ease) / 2.0 / 2.0
SHOULDER_X = HALF
SLEEVE_X = HALF + sleeve_grown
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 220.0


def _panel(name, neck_dip, with_etextile, label):
    top_y = L
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_top = fc.P(SLEEVE_X, top_y)
    sleeve_bot = fc.P(SLEEVE_X, top_y - 110.0)
    body_side_top = fc.P(SHOULDER_X, top_y - SLEEVE_DROP)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, sleeve_top)]),
        fc.Edge("sleeve_end", [fc.Line(sleeve_top, sleeve_bot)]),
        fc.Edge("sleeve_under", [fc.Line(sleeve_bot, body_side_top)]),
        fc.Edge("side", [fc.Line(body_side_top, fc.P(SHOULDER_X, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(SHOULDER_X, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = []
    if with_etextile:
        # Sensor-mount pocket (a square opening) centred high on the chest.
        mx, my = HALF * 0.45, L * 0.68
        h = mount_size / 2.0
        internals.append(fc.Internal("sensor-mount-pocket", [
            fc.P(mx - h, my - h), fc.P(mx + h, my - h),
            fc.P(mx + h, my + h), fc.P(mx - h, my + h), fc.P(mx - h, my - h)], kind="marking"))
        # Conductive-thread routes: traces from the mount down to a hem-hub bus.
        hub_y = L * 0.10
        for i in range(route_count):
            rx = HALF * (0.25 + 0.5 * i / max(route_count - 1, 1))
            internals.append(fc.Internal(f"conductive-route-{i}", [
                fc.P(mx, my - h), fc.P(rx, L * 0.4), fc.P(rx, hub_y)], kind="trace"))
        internals.append(fc.Internal(
            "hem-hub-bus", [fc.P(HALF * 0.2, hub_y), fc.P(HALF * 0.8, hub_y)], kind="trace"))
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"), fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 60.0), fc.P(HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("etextile-sensor-tee")
    front = _panel("front", 70.0, True, "Front (with e-textile routing)")
    back = _panel("back", 25.0, False, "Back")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)
    if all_pieces:
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "jersey knit (conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 75% marker; see the fabric card's e_textile block."},
        {"item": "conductive thread", "qty": 1, "unit": "spool",
         "note": "embroider the marked routes from the sensor mount to the hem-hub bus."},
        {"item": "sensor-mount enclosure", "qty": 1, "unit": "count",
         "note": "Yantra4D sensor-mount-plate (see notion.hardware_ref) snaps into the pocket."},
        {"item": "washable sensor + snaps", "qty": 1, "unit": "set", "note": "maker's choice."},
    ]
    pattern.metadata = {
        "fc200_rank": 145, "family": "etextile", "fabric_hint": "jersey-algodon",
        "etextile_note": "Base tee + a conductive-thread routing plan (traces from a chest "
            "sensor mount to a hem-hub bus) + a sensor-mount pocket sized to the Yantra4D "
            "sensor-mount-plate. The routes and pocket are MARKED for the maker to embroider "
            "with conductive thread; no electronics are drafted here.",
        "hardware": "sensor enclosure via Yantra4D (notion.hardware_ref -> sensor-mount-plate)",
    }
    return pattern


result = build()
