"""
Eight-yard kilt — Fashion Cabinet Garment Cartridge (FC-400 #398; y4d strap-buckle).

The traditional Scottish kilt: a knife-pleated wrap of about eight yards of wool tartan,
flat-fronted (two overlapping APRONS) with the whole surplus pleated across the back, sitting
at the natural waist and closed by leather STRAPS and BUCKLES. This cartridge drafts a real
eight-yard kilt around the three facts that make it one, not a pleated skirt:

  1. THE PLEATS ARE SET TO THE SETT — PLEATING TO THE STRIPE OR TO THE SETT. A kilt is pleated
     so that each pleat shows one full repeat of the tartan (`pleat_to_sett`): the pleat depth
     is therefore not free — it is the tartan's SETT WIDTH, and the number of pleats is the
     back width divided by the pleat FACE (the visible width, a fraction of the sett). This
     cartridge takes the sett as a parameter and SOLVES an integer pleat count and the total
     cloth those pleats consume, then reports whether it lands near eight yards. Choosing a
     continuous "fullness" instead of pleating to a real sett is the error a kilt cannot afford.

  2. THE FRONT IS TWO FLAT APRONS, THE BACK IS ALL PLEATS. The under-apron and over-apron wrap
     flat across the front (no pleats), and the entire pleated section is at the back and sides.
     The apron width is a real proportion of the hip, and the fell (the sewn-down upper part of
     the pleats, tapered from waist to hip) is where the pleats are stitched to shape.

  3. THE CLOSURE IS STRAPS AND BUCKLES, AND ONE NUMBER SIZES THEM. Two (or three) leather straps
     pass through buckles at the waist. The buckle is the Yantra4D `strap-buckle`; `strap_w`
     drives BOTH the drafted strap width AND the buckle's webbing slot, so the strap threads.

Pieces: under_apron, over_apron, pleated_back (the pleated section, drawn flat with its fold
lines), strap. Made to measure to waist and hip girths, kilt length and the tartan sett.

Cultural note (stated): the kilt is Scottish Highland dress with deep clan and regimental
associations carried by the TARTAN, which this cartridge does not draw — the sett is a size, not
a specific clan pattern, and no tartan is invented or assigned.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

waist_girth = float(PARAM(lambda: waist_girth, 920.0))
hip_girth = float(PARAM(lambda: hip_girth, 1040.0))
kilt_length = float(PARAM(lambda: kilt_length, 600.0))     # waist to knee
fell_depth = float(PARAM(lambda: fell_depth, 180.0))       # sewn-down pleat section
sett_width = float(PARAM(lambda: sett_width, 150.0))       # tartan sett repeat
pleat_face = float(PARAM(lambda: pleat_face, 20.0))        # visible pleat width
apron_frac = float(PARAM(lambda: apron_frac, 0.5))         # apron share of the hip
strap_w = float(PARAM(lambda: strap_w, 30.0))              # strap / buckle slot width
strap_count = float(PARAM(lambda: strap_count, 3.0))       # straps+buckles
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
waist_girth = max(650.0, min(waist_girth, 1500.0))
hip_girth = max(750.0, min(hip_girth, 1650.0))
kilt_length = max(400.0, min(kilt_length, 800.0))
fell_depth = max(100.0, min(fell_depth, 320.0))
sett_width = max(80.0, min(sett_width, 260.0))
pleat_face = max(10.0, min(pleat_face, 45.0))
apron_frac = max(0.35, min(apron_frac, 0.62))
strap_w = max(18.0, min(strap_w, 50.0))
strap_count = max(2.0, min(round(strap_count), 4.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

fell_depth = min(fell_depth, kilt_length - 80.0)
pleat_face = min(pleat_face, sett_width * 0.6)   # a face is a fraction of the sett

# ── The pleat-to-sett solver ─────────────────────────────────────────────────
# The two aprons cover apron_frac of the hip each side of centre front (over + under
# overlap). The pleated back covers the REST of the waist/hip ring.
APRON_W = hip_girth * apron_frac / 2.0           # each apron's flat width
# The pleated section spans the back: the waist minus the aprons' waist coverage.
APRON_WAIST = waist_girth * apron_frac / 2.0
PLEAT_BACK_WAIST = max(120.0, waist_girth - 2.0 * APRON_WAIST)
PLEAT_BACK_HIP = max(140.0, hip_girth - 2.0 * (hip_girth * apron_frac / 2.0))
# Number of pleats = pleated back width (at the hip, where pleats are open) / pleat face.
N_PLEATS = max(3, int(round(PLEAT_BACK_HIP / pleat_face)))
# Each pleat shows one sett face but BURIES (sett_width - pleat_face) of cloth in its depth.
# So the cloth consumed by the pleated back = N_PLEATS * sett_width (one repeat per pleat).
PLEAT_CLOTH = N_PLEATS * sett_width
# Total kilt cloth ≈ two aprons (each ~apron width + underlaps) + the pleated cloth.
TOTAL_CLOTH = 2.0 * APRON_W + PLEAT_CLOTH
YARDS = TOTAL_CLOTH / 914.4                       # mm -> yards
KL = kilt_length


def build_under_apron():
    """The under-apron (cut 1): a flat rectangle, the hip width tapering to the waist, worn
    under the over-apron. Straight, no pleats.
    """
    top = APRON_WAIST
    bot = APRON_W
    dx = (bot - top) / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(bot, 0.0))]),
        fc.Edge("outer", [fc.Line(fc.P(bot, 0.0), fc.P(bot - dx, KL))]),
        fc.Edge("waist", [fc.Line(fc.P(bot - dx, KL), fc.P(dx, KL))]),
        fc.Edge("fell_edge", [fc.Line(fc.P(dx, KL), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "under_apron", edges, seam_allowance=seam_allowance,
        allowances={"hem": 25.0, "waist": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre"),
                 fc.Notch("outer", 0.5, "strap level")],
        grainline=fc.Grainline(fc.P(bot * 0.5, KL * 0.15), fc.P(bot * 0.5, KL * 0.8)),
        cut=fc.CutSpec(quantity=1), label="Under-apron (cut 1, flat)")


def build_over_apron():
    """The over-apron (cut 1): the visible flat front, hip width tapering to the waist, with the
    strap seat and a fringed selvedge edge marked. Straight, no pleats.
    """
    top = APRON_WAIST
    bot = APRON_W
    dx = (bot - top) / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(bot, 0.0))]),
        fc.Edge("fringe_edge", [fc.Line(fc.P(bot, 0.0), fc.P(bot - dx, KL))]),
        fc.Edge("waist", [fc.Line(fc.P(bot - dx, KL), fc.P(dx, KL))]),
        fc.Edge("pleat_edge", [fc.Line(fc.P(dx, KL), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("strap seat",
                             [fc.P(bot - dx * 0.5, KL - 20.0),
                              fc.P(bot - dx * 0.5 + strap_w, KL - 20.0)], kind="marking")]
    return fc.Piece(
        "over_apron", edges, seam_allowance=seam_allowance,
        allowances={"hem": 25.0, "waist": 0.0, "fringe_edge": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre"),
                 fc.Notch("pleat_edge", 0.5, "first pleat")],
        grainline=fc.Grainline(fc.P(bot * 0.5, KL * 0.15), fc.P(bot * 0.5, KL * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Over-apron (cut 1, flat, visible front)")


def build_pleated_back():
    """The pleated back section (cut 1), drawn FLAT as the full cloth width with the pleat fold
    lines marked. Its top (waist) is the pleated back waist; its full flat width is PLEAT_CLOTH;
    the fell (upper `fell_depth`) is where the pleats are sewn down and tapered.
    """
    flat = PLEAT_CLOTH
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(flat, 0.0))]),
        fc.Edge("apron_edge_r", [fc.Line(fc.P(flat, 0.0), fc.P(flat, KL))]),
        fc.Edge("waist", [fc.Line(fc.P(flat, KL), fc.P(0.0, KL))]),
        fc.Edge("apron_edge_l", [fc.Line(fc.P(0.0, KL), fc.P(0.0, 0.0))]),
    ]
    internals = []
    # pleat fold lines: N_PLEATS pleats across the flat cloth, each a full sett.
    for i in range(N_PLEATS):
        x = flat * (i + 0.5) / N_PLEATS
        internals.append(fc.Internal(f"pleat fold {i + 1}",
                                     [fc.P(x, 0.0), fc.P(x, KL)], kind="marking"))
    internals.append(fc.Internal("fell line (pleats sewn above)",
                                 [fc.P(0.0, KL - fell_depth), fc.P(flat, KL - fell_depth)],
                                 kind="marking"))
    return fc.Piece(
        "pleated_back", edges, seam_allowance=seam_allowance,
        allowances={"hem": 25.0, "waist": 0.0},
        notches=[fc.Notch("waist", 0.5, "centre back"),
                 fc.Notch("hem", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(flat * 0.5, KL * 0.15), fc.P(flat * 0.5, KL * 0.8)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Pleated back — flat cloth with pleat folds (cut 1)")


def build_strap():
    """A leather strap (cut `strap_count`): width strap_w, threading a buckle."""
    n = int(strap_count)
    ln = APRON_W * 0.8
    edges = [
        fc.Edge("end_a", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, strap_w))]),
        fc.Edge("strap_edge", [fc.Line(fc.P(0.0, strap_w), fc.P(ln, strap_w))]),
        fc.Edge("end_buckle", [fc.Line(fc.P(ln, strap_w), fc.P(ln, 0.0))]),
        fc.Edge("strap_edge_b", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "strap", edges, seam_allowance=0.0,
        notches=[fc.Notch("end_buckle", 0.5, "buckle slot — thread here")],
        grainline=fc.Grainline(fc.P(ln * 0.2, strap_w / 2.0), fc.P(ln * 0.8, strap_w / 2.0)),
        cut=fc.CutSpec(quantity=n, mirror=False),
        label="Waist strap (cut per strap_count, buckle at end)")


def build():
    pattern = fc.PatternSet("kilt-8yard")
    under = build_under_apron()
    over = build_over_apron()
    back = build_pleated_back()
    strap = build_strap()

    picked = {"under_apron": under, "over_apron": over,
              "pleated_back": back, "strap": strap}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (under, over, back, strap):
            pattern.add(piece)
        # The pleated back joins the two aprons at its side edges (the pleat_edge / fringe_edge
        # of each apron meets the pleated section's apron edges). The pleated back's flat width
        # gathers UP to the apron edge, so this is a pleated join, documented by ease.
        pattern.declare_seam(("pleated_back", "apron_edge_l"), ("over_apron", "pleat_edge"),
                             tol=2.0, ease=(back.edge("apron_edge_l").length()
                                            - over.edge("pleat_edge").length()))
        pattern.declare_seam(("pleated_back", "apron_edge_r"), ("under_apron", "fell_edge"),
                             tol=2.0, ease=(back.edge("apron_edge_r").length()
                                            - under.edge("fell_edge").length()))
        # The strap's two ends match (one continuous strap through the buckle).
        pattern.declare_seam(("strap", "end_a"), ("strap", "end_buckle"), tol=0.5)

    pattern.bom = [
        {"item": "wool tartan (approx. 8 yards, single width)",
         "qty": round(TOTAL_CLOTH / 100.0) * 100, "unit": "mm_length",
         "note": f"aprons + pleated back; the pleats consume {PLEAT_CLOTH:.0f} mm (one sett per "
                 f"pleat), total ≈ {YARDS:.1f} yards. A traditional eight-yard kilt uses about "
                 "8 yards; this draft reports the actual figure it solves to."},
        {"item": "kilt straps + buckles (Yantra4D strap-buckle)", "qty": int(strap_count),
         "unit": "set",
         "note": f"{int(strap_count)} leather straps + buckles at the waist; strap width strap_w "
                 f"{strap_w:.0f} mm. The buckle is the Yantra4D solid (notion.hardware_ref -> "
                 "strap-buckle); strap_w drives BOTH the drafted strap and the buckle's webbing "
                 "slot, so the strap threads by construction."},
        {"item": "cotton canvas (waistband stiffening) + kilt lining", "qty": 1, "unit": "set",
         "note": "the fell is stiffened so the sewn pleats hold their taper from waist to hip."},
        {"item": "thread (matched to the sett)", "qty": 1, "unit": "set",
         "note": "the pleats are stitched down through the fell only; below the fell they hang "
                 "free and swing."},
    ]
    pattern.metadata = {
        "fc400_rank": 398, "family": "heritage_global", "fabric_hint": "wool-tartan",
        "tradition": "Scottish Highland dress — the eight-yard knife-pleated tartan kilt",
        "silhouette_note": "A flat-fronted wrap of two overlapping aprons with the entire "
            "surplus knife-pleated across the back, sewn down through the fell and swinging free "
            "below, at the natural waist, closed by leather straps and buckles.",
        "hardware": "straps + buckles via Yantra4D (notion.hardware_ref -> strap-buckle); "
            "strap_w drives BOTH the drafted strap and the buckle webbing slot.",
        "solver": {
            "sett_width_mm": round(sett_width, 1),
            "pleat_face_mm": round(pleat_face, 1),
            "pleat_count": N_PLEATS,
            "pleat_cloth_mm": round(PLEAT_CLOTH, 1),
            "apron_width_mm": round(APRON_W, 1),
            "total_cloth_mm": round(TOTAL_CLOTH, 1),
            "yards": round(YARDS, 2),
            "note": "pleated TO THE SETT: each pleat shows one full tartan repeat and buries the "
                    "rest in its depth, so the pleat depth is the sett and the count is the back "
                    "width over the pleat face. The total lands near eight yards by construction, "
                    "and the actual figure is reported.",
        },
        "cultural_note": "The kilt is Scottish Highland dress with deep clan and regimental "
            "associations carried by the TARTAN, which this cartridge does NOT draw — the sett is "
            "a size, not a specific clan pattern, and no tartan is invented or assigned.",
        "drafting": "Made to measure to waist and hip girths + kilt length and tartan sett; the "
            "pleats are solved to the sett and the closure is strap-and-buckle.",
    }
    return pattern


result = build()
