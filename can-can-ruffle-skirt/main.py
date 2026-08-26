"""
Can-Can Ruffle Skirt — Fashion Cabinet Costume Cartridge (FC-500 #481; y4d hook-and-eye).

The high-kick can-can skirt: a full gathered skirt on a fitted waistband, carrying tier upon tier
of net RUFFLES (the froufrou) that flash when the skirt is lifted and kicked, closing at a
side/back Yantra4D `hook-and-eye`. It is the archetype of the Moulin Rouge chorus line, and its
whole engineering is the ruffle stack: enough tiers, at enough fullness, that the underside is a
wall of white when the hem goes overhead.

The tier SOLVE. The skirt is a gathered rectangle of the hip girth times a body fullness, on a
waistband cut to the waist. Each ruffle tier is placed at a fraction down the skirt and cut to the
skirt's circumference AT THAT LEVEL times the ruffle fullness — a lower tier is longer than an
upper one because the skirt is a cone, so cutting every tier the same length (the naive error)
leaves the lower tiers straining and the upper ones drooping. The tier length is solved per level:

    tier_len(level) = skirt_circ_at(level) * ruffle_fullness

and the representative (widest, lowest) tier is drafted; the depth schedule is in the BOM.

The DIMENSIONAL HANDSHAKE. The waistband closes on a `hook-and-eye`; `closure_rows` drives the
hook `columns` and `waistband_height` drives the drafted placket AND the skirt's own `wb_closure`
interface.

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

waist_girth = float(PARAM(lambda: waist_girth, 720.0))
hip_girth = float(PARAM(lambda: hip_girth, 960.0))
skirt_length = float(PARAM(lambda: skirt_length, 700.0))
skirt_fullness = float(PARAM(lambda: skirt_fullness, 2.6))    # skirt gather on the waistband
ruffle_fullness = float(PARAM(lambda: ruffle_fullness, 2.4))
ruffle_depth = float(PARAM(lambda: ruffle_depth, 130.0))
tier_count = float(PARAM(lambda: tier_count, 4.0))
waistband_height = float(PARAM(lambda: waistband_height, 60.0))
closure_rows = float(PARAM(lambda: closure_rows, 5.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth = max(520.0, min(waist_girth, 1200.0))
hip_girth = max(700.0, min(hip_girth, 1500.0))
skirt_length = max(400.0, min(skirt_length, 1100.0))
skirt_fullness = max(1.8, min(skirt_fullness, 4.0))
ruffle_fullness = max(1.6, min(ruffle_fullness, 4.0))
ruffle_depth = max(60.0, min(ruffle_depth, 240.0))
tier_count = max(2.0, min(tier_count, 10.0))
waistband_height = max(30.0, min(waistband_height, 120.0))
closure_rows = max(2.0, min(closure_rows, 10.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

N_TIER = int(round(tier_count))

# ── Solved geometry ──────────────────────────────────────────────────────────
WB = waistband_height
SKIRT_CIRC = hip_girth * skirt_fullness      # gathered flat circumference at the top
# the hem circumference of a flared skirt (grows toward the hem)
HEM_CIRC = SKIRT_CIRC * 1.4
# widest (lowest) ruffle tier length
LOW_TIER_LEN = HEM_CIRC * ruffle_fullness


def _rect(w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def build_skirt():
    """The skirt body: a trapezoid panel, waist (top, SKIRT_CIRC) to hem (bottom, HEM_CIRC),
    of the skirt length. Cut 1 (joined at the CB closure)."""
    top, bot = SKIRT_CIRC, HEM_CIRC
    off = (bot - top) / 2.0
    p_wl = fc.P(off, skirt_length)
    p_wr = fc.P(off + top, skirt_length)
    p_hr = fc.P(bot, 0.0)
    p_hl = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("hem", [fc.Line(p_hl, p_hr)]),
        fc.Edge("cb_r", [fc.Line(p_hr, p_wr)]),
        fc.Edge("waist", [fc.Line(p_wr, p_wl)]),
        fc.Edge("cb_l", [fc.Line(p_wl, p_hl)]),
    ]
    internals = []
    for t in range(1, N_TIER + 1):
        ty = skirt_length * t / (N_TIER + 1)
        internals.append(fc.Internal(f"tier-line-{t}", [fc.P(0.0, ty), fc.P(bot, ty)],
                                     kind="marking"))
    return fc.Piece(
        "skirt", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.5, "CF"), fc.Notch("hem", 0.5, "CF")],
        grainline=fc.Grainline(fc.P(bot * 0.5, skirt_length * 0.1),
                               fc.P(bot * 0.5, skirt_length * 0.9)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Skirt panel (cut 1, CB closure)",
    )


def build_ruffle():
    """The representative (lowest, widest) net ruffle tier, cut to the hem circumference times
    the ruffle fullness. Upper tiers are shorter per the depth schedule in the BOM."""
    edges = _rect(LOW_TIER_LEN, ruffle_depth, ("gather_edge", "end_r", "outer", "end_l"))
    return fc.Piece(
        "ruffle", edges, seam_allowance=seam_allowance,
        allowances={"outer": 0.0},
        notches=[fc.Notch("gather_edge", 0.25, "q"), fc.Notch("gather_edge", 0.5, "half"),
                 fc.Notch("gather_edge", 0.75, "q")],
        grainline=fc.Grainline(fc.P(LOW_TIER_LEN * 0.08, ruffle_depth * 0.4),
                               fc.P(LOW_TIER_LEN * 0.92, ruffle_depth * 0.4)),
        cut=fc.CutSpec(quantity=1),
        label="Net ruffle tier (widest; cut stack per schedule)",
    )


def build_waistband():
    """Fitted waistband cut to the waist, folded, closing at the hook-and-eye."""
    length = waist_girth + 40.0    # + overlap for the closure
    cut_depth = WB * 2.0
    edges = _rect(length, cut_depth, ("attach", "join_r", "top", "join_l"))
    internals = [fc.Internal("fold-line", [fc.P(0.0, WB), fc.P(length, WB)], kind="marking")]
    n = int(round(closure_rows))
    for i in range(n):
        hx = length - 20.0
        hy = WB + (i + 0.5) * (WB / n)
        internals.append(fc.Internal(f"hook-{i}", [fc.P(hx - 8.0, hy), fc.P(hx + 8.0, hy)],
                                     kind="drill"))
    return fc.Piece(
        "waistband", edges, seam_allowance=seam_allowance,
        allowances={"top": 0.0},
        notches=[fc.Notch("attach", 0.5, "CF"), fc.Notch("join_r", 0.5, "hook")],
        grainline=fc.Grainline(fc.P(length * 0.08, WB * 0.4), fc.P(length * 0.92, WB * 0.4)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waistband (cut 1, folded, hook closure)",
    )


def build():
    pattern = fc.PatternSet("can-can-ruffle-skirt")
    skirt = build_skirt()
    ruffle = build_ruffle()
    waistband = build_waistband()

    picked = {"skirt": skirt, "ruffle": ruffle, "waistband": waistband}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (skirt, ruffle, waistband):
            pattern.add(piece)
        # Skirt gathers onto the waistband at skirt_fullness.
        wb_attach = waistband.edge("attach").length()
        pattern.declare_seam(("skirt", "waist"), ("waistband", "attach"),
                             tol=3.0, ease=(skirt.edge("waist").length() - wb_attach))
        # The lowest ruffle gathers onto the skirt hem at ruffle_fullness.
        pattern.declare_seam(("ruffle", "gather_edge"), ("skirt", "hem"),
                             tol=3.0, ease=(ruffle.edge("gather_edge").length()
                                            - skirt.edge("hem").length()))

    fabric_width = 1400.0
    net_width = 2800.0
    tier_total = LOW_TIER_LEN * N_TIER * 0.8
    area = skirt.area() + waistband.area()
    marker_len = area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "satin / taffeta (skirt + waistband)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"the skirt body at {fabric_width:.0f} mm width; a crisp fabric flashes better "
                 "when kicked."},
        {"item": "stiff white net (ruffle tiers)", "qty": round(tier_total),
         "unit": "mm_length",
         "note": f"{N_TIER} tiers; the lowest is {LOW_TIER_LEN:.0f} mm flat "
                 f"({ruffle_fullness:.1f}x the {HEM_CIRC:.0f} mm hem), stepping shorter up the "
                 f"skirt at {net_width:.0f} mm net width — the froufrou wall."},
        {"item": "hook-and-eye tape (Yantra4D hook-and-eye)", "qty": 1, "unit": "piece",
         "note": f"waistband closure, {int(round(closure_rows))} rows (hook-and-eye)."},
        {"item": "petticoat hoop / horsehair", "qty": round(HEM_CIRC * 1.05), "unit": "mm_length",
         "note": "a stiff petticoat under the skirt makes the hem fly up rather than fall."},
    ]
    pattern.metadata = {
        "fc500_rank": 481, "family": "costume_historical", "fabric_hint": "tul-nylon",
        "provenance": "The can-can skirt is the costume of the 1890s Parisian dance-hall chorus "
            "(Moulin Rouge, Folies Bergere): the point is the froufrou — a wall of white net "
            "ruffles revealed on the high kick and the grand ecart. The engineering is the ruffle "
            "stack, cut per level so the underside is dense.",
        "silhouette_note": "A full flared skirt on a fitted waistband, faced underneath with tier "
            "upon tier of net ruffles, closing at a hook-and-eye. Built for the high kick.",
        "hardware": "waistband closure via Yantra4D (hardware_ref -> hook-and-eye); closure_rows "
            "drives the hook columns and waistband_height the drafted placket.",
        "solved": {
            "skirt_fullness": round(skirt_fullness, 2),
            "skirt_top_circ_mm": round(SKIRT_CIRC, 1),
            "hem_circ_mm": round(HEM_CIRC, 1),
            "ruffle_fullness": round(ruffle_fullness, 2),
            "low_tier_len_mm": round(LOW_TIER_LEN, 1),
            "tier_count": N_TIER,
            "note": "each tier is cut to the skirt circumference at its level times ruffle "
                    "fullness — a lower tier is longer because the skirt is a cone; cutting them "
                    "all equal (the naive error) strains the low tiers and droops the high ones.",
        },
        "closure": "waistband hook-and-eye",
        "drafting": "Made to measure to waist and hip; fullness sets the flash.",
    }
    return pattern


result = build()
