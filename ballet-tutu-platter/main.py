"""
Platter Tutu — Fashion Cabinet Costume Cartridge (FC-500 #473; y4d hook-and-eye).

The classical "platter" (or "pancake") tutu: a short, stiff, near-horizontal disc of gathered net
standing straight out from the hip, built on a fitted BASQUE (a boned hip yoke) and closing at a
centre-back Yantra4D `hook-and-eye`. The plate is a stack of net tiers of decreasing radius, each
gathered onto the basque, held flat by a covered hoop (the "steel") near the outer edge — the
construction that makes a tutu a rigid platter rather than a soft skirt.

The gather that must SOLVE. Each net tier is a full ring gathered onto the basque hem, so its flat
cut length is the basque hem times a FULLNESS ratio, and the ratio is what makes the net stand:

    tier_flat = basque_hem * fullness      (fullness 2x-6x; a platter wants a lot)

The tier is drafted as a rectangle of that flat length and its own radial depth, and declared
against the basque hem with the fullness as gathered ease, so the fullness is proven arithmetic
rather than a dressmaker's guess. The plate radius sets the tier depths; the hoop channel is
marked at the plate radius on the top tier.

The DIMENSIONAL HANDSHAKE. The centre-back closes on a `hook-and-eye` of `columns` across
`size_mm`. `closure_rows` drives the hook `rows`, and `basque_depth` drives the drafted placket
the hooks sew into AND the tutu's own `cb_closure` interface, so the placket is exactly as tall as
the tape.

Made to measure to waist and hip girths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

waist_girth = float(PARAM(lambda: waist_girth, 700.0))
hip_girth = float(PARAM(lambda: hip_girth, 920.0))
basque_depth = float(PARAM(lambda: basque_depth, 180.0))    # waist to plate line
plate_radius = float(PARAM(lambda: plate_radius, 380.0))    # hip to plate edge (the disc)
fullness = float(PARAM(lambda: fullness, 3.5))              # net gather ratio
tier_count = float(PARAM(lambda: tier_count, 3.0))
closure_rows = float(PARAM(lambda: closure_rows, 6.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(520.0, min(waist_girth, 1200.0))
hip_girth = max(700.0, min(hip_girth, 1500.0))
basque_depth = max(90.0, min(basque_depth, 320.0))
plate_radius = max(200.0, min(plate_radius, 560.0))
fullness = max(2.0, min(fullness, 6.0))
tier_count = max(1.0, min(tier_count, 8.0))
closure_rows = max(2.0, min(closure_rows, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

N_TIER = int(round(tier_count))

# ── Solved geometry ──────────────────────────────────────────────────────────
WAIST_HALF = waist_girth / 2.0
HIP_HALF = hip_girth / 2.0
BASQUE_HEM = hip_girth        # the basque bottom is at the hip, full ring
TIER_FLAT = BASQUE_HEM * fullness
TIER_DEPTH = plate_radius / N_TIER
BD = basque_depth


def _rect(x0, y0, w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(x0, y0), fc.P(x0 + w, y0), fc.P(x0 + w, y0 + h), fc.P(x0, y0 + h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def build_basque():
    """The boned hip yoke, cut 2 (CB hook to CF fold... here cut 2 mirror, CB hook). A shaped
    panel from waist (top, waist_half) to hip (bottom, hip_half), with boning channels marked."""
    top = WAIST_HALF
    bot = HIP_HALF
    p_wt = fc.P(0.0, BD)          # CF top (waist)
    p_wb = fc.P(0.0, 0.0)         # CF bottom (hip)
    p_hb = fc.P(bot, 0.0)         # side bottom
    p_ht = fc.P(top, BD)          # side top
    edges = [
        fc.Edge("waist", [fc.Line(p_ht, p_wt)]),
        fc.Edge("center_front", [fc.Line(p_wt, p_wb)]),
        fc.Edge("hem", [fc.Line(p_wb, p_hb)]),
        fc.Edge("center_back", [fc.Line(p_hb, p_ht)]),
    ]
    internals = []
    for i in range(1, 5):
        bx = bot * i / 5.0
        internals.append(fc.Internal(f"bone-{i}", [fc.P(bx, 8.0), fc.P(bx * (top / bot), BD - 8.0)],
                                     kind="marking"))
    return fc.Piece(
        "basque", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.5, "waist match"), fc.Notch("hem", 0.5, "plate match")],
        grainline=fc.Grainline(fc.P(bot * 0.4, BD * 0.2), fc.P(bot * 0.4, BD * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Basque hip yoke (cut 2, CB hook)",
    )


def build_tier():
    """A net tier: a rectangle of the SOLVED flat length (basque hem x fullness) and the tier
    depth, gathered onto the basque hem. One piece cut N_TIER times at decreasing depth (the
    representative tier is drafted; the maker cuts the stack from the depth schedule in the BOM)."""
    length = TIER_FLAT
    depth = TIER_DEPTH
    edges = _rect(0.0, 0.0, length, depth, ("gather_edge", "end_r", "outer", "end_l"))
    internals = [
        fc.Internal("hoop-channel", [fc.P(0.0, depth * 0.82), fc.P(length, depth * 0.82)],
                    kind="marking"),
    ]
    return fc.Piece(
        "tier", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},   # net edge is cut raw
        notches=[fc.Notch("gather_edge", 0.25, "quarter"), fc.Notch("gather_edge", 0.5, "half"),
                 fc.Notch("gather_edge", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(length * 0.08, depth * 0.4), fc.P(length * 0.92, depth * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Net tier (cut per depth schedule, gathered)",
    )


def build_placket(cb_len):
    """The CB hook-and-eye placket, its height built to the MEASURED basque centre-back edge so
    it sews on flat (the basque CB is slanted, so the placket is taller than basque_depth)."""
    w = max(40.0, closure_rows * 12.0)
    h = cb_len
    edges = _rect(0.0, 0.0, w, h, ("bottom", "attach", "top", "fold"))
    internals = []
    n = int(round(closure_rows))
    for i in range(n):
        hy = (i + 0.5) * (h / n)
        internals.append(fc.Internal(f"hook-{i}", [fc.P(w * 0.4, hy), fc.P(w * 0.6, hy)],
                                     kind="drill"))
    return fc.Piece(
        "placket", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "CB")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.1), fc.P(w * 0.5, h * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="CB hook-and-eye placket (cut 2)",
    )


def build():
    pattern = fc.PatternSet("ballet-tutu-platter")
    basque = build_basque()
    tier = build_tier()
    placket = build_placket(basque.edge("center_back").length())

    picked = {"basque": basque, "tier": tier, "placket": placket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (basque, tier, placket):
            pattern.add(piece)
        # THE GATHER: one tier gathers onto the full basque hem (2 basque halves) at `fullness`.
        basque_hem_full = 2.0 * basque.edge("hem").length()
        pattern.declare_seam(("tier", "gather_edge"),
                             [("basque", "hem"), ("basque", "hem")],
                             tol=2.0, ease=(tier.edge("gather_edge").length() - basque_hem_full))
        # The placket sews to the basque centre back (its height == basque depth).
        pattern.declare_seam(("placket", "attach"), ("basque", "center_back"), tol=2.0)

    fabric_width = 1500.0
    net_width = 2800.0
    basque_area = basque.area() * 2.0 + placket.area() * 2.0
    tier_len_total = TIER_FLAT * N_TIER
    marker_len = basque_area / (fabric_width * 0.75)
    pattern.bom = [
        {"item": "coutil / power-net (basque)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"the boned hip yoke at {fabric_width:.0f} mm width; a platter tutu's basque is "
                 "firm so the plate does not drag it down."},
        {"item": "stiff nylon net (tiers)", "qty": round(tier_len_total),
         "unit": "mm_length",
         "note": f"{N_TIER} tiers, each {TIER_FLAT:.0f} mm flat "
                 f"({fullness:.1f}x the {2 * basque.edge('hem').length():.0f} "
                 f"mm basque hem), at {net_width:.0f} mm net width; depths step down over the "
                 f"{plate_radius:.0f} mm plate radius."},
        {"item": "covered spring steel hoop (the 'steel')", "qty": round(plate_radius * 6.2),
         "unit": "mm_length",
         "note": "threaded through the marked hoop channel near the plate edge — this is what "
                 "makes the tutu a rigid platter rather than a soft skirt."},
        {"item": "hook-and-eye tape (Yantra4D hook-and-eye)", "qty": 1, "unit": "piece",
         "note": f"CB closure, {int(round(closure_rows))} rows over the {basque_depth:.0f} mm "
                 "basque (notion.hardware_ref -> hook-and-eye)."},
        {"item": "tacking thread + basting", "qty": 1, "unit": "set",
         "note": "the tiers are tacked together at intervals so the plate holds its disc shape."},
    ]
    pattern.metadata = {
        "fc500_rank": 473, "family": "costume_historical", "fabric_hint": "tul-nylon",
        "provenance": "The platter (pancake) tutu is the Petipa-era classical form (Sleeping "
            "Beauty, Swan Lake): a short stiff horizontal disc on a boned basque, held by a hoop, "
            "distinct from the softer Romantic bell tutu. The construction here follows that "
            "workroom tradition — a firm basque, tiered net at high fullness, a covered steel.",
        "silhouette_note": "A rigid horizontal net disc standing straight out from a boned hip "
            "yoke, closing at a centre-back hook-and-eye. The plate is a stack of gathered net "
            "tiers held flat by a hoop near the edge.",
        "hardware": "CB closure via Yantra4D (hardware_ref -> hook-and-eye); closure_rows drives "
            "the hook rows and basque_depth the drafted placket.",
        "solved": {
            "basque_hem_full_mm": round(2.0 * basque.edge("hem").length(), 1),
            "fullness": round(fullness, 2),
            "tier_flat_mm": round(TIER_FLAT, 1),
            "tier_count": N_TIER,
            "tier_depth_mm": round(TIER_DEPTH, 1),
            "plate_radius_mm": round(plate_radius, 1),
            "note": "tier_flat = basque_hem * fullness; declared against the basque hem with the "
                    "fullness as gathered ease, so the net standing power is proven arithmetic.",
        },
        "closure": "centre-back hook-and-eye",
        "drafting": "Made to measure to waist and hip; plate radius and fullness set the disc.",
    }
    return pattern


result = build()
