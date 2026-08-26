"""
Quick-Change Stage Gown — Fashion Cabinet Costume Cartridge (FC-500 #482; y4d magnetic-clasp).

The quick-change stage gown of the illusion act and the musical: a fitted gown whose centre-back
and one side seam are BREAKAWAY seams held by a column of Yantra4D `magnetic-clasp` clasps instead
of a zip or hooks, so a dresser (or the performer) can rip the whole gown off in one motion for a
reveal or a change in the wings in a few seconds. It is drafted as a bodice and a gathered skirt
whose breakaway seam runs unbroken from the collar to the hem, seated with evenly-spaced magnetic
clasps strong enough to hold under movement yet release under a firm pull.

The clasp-count SOLVE. A breakaway seam holds only if the clasps are close enough that no gap sags
open under stage movement, but each clasp adds pull-apart force, so the count is solved from the
seam length and a clasp pitch tuned to the fabric weight:

    clasps = round(breakaway_length / clasp_pitch)

so a longer gown gets more clasps and the holding force per unit length stays constant, whatever
the size. The clasp seats are placed by fraction along the breakaway seam, drafted, not guessed.

The DIMENSIONAL HANDSHAKE. `magnetic-clasp`'s sewn `sew_face` flange is driven by `disc_dia`.
`clasp_dia` drives the clasp's `disc_dia` AND the drafted clasp seat AND the gown's own
`breakaway_seam` interface, so the printed clasp is exactly the size of the seat it sews to.

Made to measure to bust, waist, hip and lengths. FC-500 lane 9 (costume, dance & performance).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
waist_girth = float(PARAM(lambda: waist_girth, 760.0))
hip_girth = float(PARAM(lambda: hip_girth, 980.0))
bodice_length = float(PARAM(lambda: bodice_length, 400.0))
skirt_length = float(PARAM(lambda: skirt_length, 950.0))
skirt_fullness = float(PARAM(lambda: skirt_fullness, 1.8))
clasp_dia = float(PARAM(lambda: clasp_dia, 18.0))
clasp_pitch = float(PARAM(lambda: clasp_pitch, 70.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

bust_girth = max(700.0, min(bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1200.0))
hip_girth = max(720.0, min(hip_girth, 1500.0))
bodice_length = max(300.0, min(bodice_length, 560.0))
skirt_length = max(500.0, min(skirt_length, 1400.0))
skirt_fullness = max(1.3, min(skirt_fullness, 3.5))
clasp_dia = max(10.0, min(clasp_dia, 30.0))
clasp_pitch = max(30.0, min(clasp_pitch, 140.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# seam allowance must hold the clasp with margin
seam_allowance = max(seam_allowance, clasp_dia * 0.7)

BUST_HALF = bust_girth / 2.0
WAIST_HALF = waist_girth / 2.0
HIP_HALF = hip_girth / 2.0
BODICE_PANEL = BUST_HALF / 2.0
WAIST_PANEL = WAIST_HALF / 2.0
BL = bodice_length
SKIRT_CIRC = hip_girth * skirt_fullness
BREAKAWAY_LEN = BL + skirt_length     # collar to hem down the breakaway seam
N_CLASP = max(1, int(round(BREAKAWAY_LEN / clasp_pitch)))


def _rect(w, h, names):
    w = max(w, 1.0)
    h = max(h, 1.0)
    p0, p1, p2, p3 = fc.P(0.0, 0.0), fc.P(w, 0.0), fc.P(w, h), fc.P(0.0, h)
    return [fc.Edge(names[0], [fc.Line(p0, p1)]), fc.Edge(names[1], [fc.Line(p1, p2)]),
            fc.Edge(names[2], [fc.Line(p2, p3)]), fc.Edge(names[3], [fc.Line(p3, p0)])]


def _bodice(is_front):
    top = BODICE_PANEL
    bot = WAIST_PANEL
    neck_w = max(60.0, BODICE_PANEL * 0.5)
    neck_drop = (BODICE_PANEL * 0.75) if is_front else (BODICE_PANEL * 0.2)
    p_cf_waist = fc.P(0.0, 0.0)
    p_side_waist = fc.P(bot, 0.0)
    p_underarm = fc.P(top, BL * 0.55)
    p_shoulder = fc.P(neck_w + (top - neck_w) * 0.5, BL)
    p_neck = fc.P(neck_w, BL)
    p_cf_neck = fc.P(0.0, BL - neck_drop)
    edges = [
        fc.Edge("waist", [fc.Line(p_cf_waist, p_side_waist)]),
        fc.Edge("side", [fc.Line(p_side_waist, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm, fc.P(top * 0.95, BL * 0.78),
                                      fc.P(p_shoulder.x + 10.0, BL - 20.0), p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.6, BL - neck_drop * 0.4),
                                   fc.P(neck_w * 0.2, BL - neck_drop * 0.85), p_cf_neck)]),
        fc.Edge("center", [fc.Line(p_cf_neck, p_cf_waist)]),
    ]
    name = "bodice_front" if is_front else "bodice_back"
    internals = []
    if not is_front:
        # the breakaway seam clasps down the CB of the bodice (its share of the total)
        n_bod = max(1, int(round(BL / clasp_pitch)))
        for i in range(n_bod):
            cy = (i + 0.5) * (BL / n_bod)
            internals.append(fc.Internal(f"clasp-bodice-{i}",
                                         [fc.P(clasp_dia / 2.0, cy), fc.P(clasp_dia / 2.0, cy)],
                                         kind="drill"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"armscye": 0.0, "neck": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"), fc.Notch("waist", 0.5, "skirt match")],
        internals=internals,
        grainline=fc.Grainline(fc.P(top * 0.4, BL * 0.2), fc.P(top * 0.4, BL * 0.8)),
        cut=fc.CutSpec(quantity=(1 if is_front else 2), mirror=(not is_front),
                       on_fold=is_front, fold_edge=("center" if is_front else None)),
        label=("Bodice front (cut 1 on fold)" if is_front
               else "Bodice back (cut 2, breakaway CB)"),
    )


def build_skirt():
    edges = _rect(SKIRT_CIRC, skirt_length, ("hem", "cb_r", "waist", "cb_l"))
    internals = []
    n_skirt = max(1, int(round(skirt_length / clasp_pitch)))
    for i in range(n_skirt):
        cy = (i + 0.5) * (skirt_length / n_skirt)
        internals.append(fc.Internal(f"clasp-skirt-{i}",
                                     [fc.P(clasp_dia / 2.0, cy), fc.P(clasp_dia / 2.0, cy)],
                                     kind="drill"))
    return fc.Piece(
        "skirt", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("waist", 0.5, "CF"), fc.Notch("cb_r", 0.5, "breakaway")],
        internals=internals,
        grainline=fc.Grainline(fc.P(SKIRT_CIRC * 0.08, skirt_length * 0.4),
                               fc.P(SKIRT_CIRC * 0.92, skirt_length * 0.4)),
        cut=fc.CutSpec(quantity=1),
        label="Gathered skirt (cut 1, breakaway CB)",
    )


def build():
    pattern = fc.PatternSet("stage-quick-change-gown")
    b_front = _bodice(True)
    b_back = _bodice(False)
    skirt = build_skirt()

    picked = {"bodice_front": b_front, "bodice_back": b_back, "skirt": skirt}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (b_front, b_back, skirt):
            pattern.add(piece)
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=2.0)
        # Skirt gathers onto the bodice waist ring.
        bodice_waist = 2.0 * (b_front.edge("waist").length() + b_back.edge("waist").length())
        pattern.declare_seam(("skirt", "waist"),
                             [("bodice_front", "waist"), ("bodice_front", "waist"),
                              ("bodice_back", "waist"), ("bodice_back", "waist")],
                             tol=3.0, ease=(skirt.edge("waist").length() - bodice_waist))
        # The breakaway seam runs collar-to-hem: the two bodice-back halves meet at CB (clasps),
        # and the skirt's two CB edges meet (clasps) — one continuous magnetic seam. Each closes
        # on its own opposite, so both are equal-length self-seams.
        pattern.declare_seam(("bodice_back", "center"), ("bodice_back", "center"), tol=2.0)
        pattern.declare_seam(("skirt", "cb_r"), ("skirt", "cb_l"), tol=2.0)

    fabric_width = 1450.0
    area = b_front.area() * 2.0 + b_back.area() * 2.0 + skirt.area()
    marker_len = area / (fabric_width * 0.66)
    pattern.bom = [
        {"item": "stage satin / duchess", "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"a fabric with body so the gown holds its shape between the clasps; at "
                 f"{fabric_width:.0f} mm width."},
        {"item": "magnetic clasps (Yantra4D magnetic-clasp)", "qty": N_CLASP, "unit": "count",
         "note": f"{N_CLASP} clasps down the {BREAKAWAY_LEN:.0f} mm breakaway seam at "
                 f"{clasp_pitch:.0f} mm pitch (hardware_ref -> magnetic-clasp); clasp_dia drives "
                 "the clasp AND the seat."},
        {"item": "reinforcement tape (breakaway seam)", "qty": round(BREAKAWAY_LEN * 1.05),
         "unit": "mm_length",
         "note": "stay-tape the breakaway seam so the repeated rip does not stretch the cloth."},
        {"item": "lining + boning (bodice)", "qty": 1, "unit": "set",
         "note": "a fully boned, lined bodice holds the clasps flat so the seam reads closed."},
    ]
    pattern.metadata = {
        "fc500_rank": 482, "family": "costume_historical", "fabric_hint": "raso-poliester",
        "provenance": "The quick-change gown is the working garment of the illusion act, the "
            "quick-change variety turn, and the musical with fast on-stage transformations: the "
            "whole engineering is the breakaway seam, historically hooks or Velcro, here a "
            "magnetic seam that closes clean and releases in one motion.",
        "silhouette_note": "A fitted gown whose centre-back runs unbroken from collar to hem as a "
            "magnetic BREAKAWAY seam, so the whole gown comes away in one pull for a reveal or a "
            "wing change. Bodice + gathered skirt, clasp count solved to the seam.",
        "hardware": "breakaway clasps via Yantra4D (hardware_ref -> magnetic-clasp); clasp_dia "
            "drives the clasp sew face AND the drafted seat.",
        "solved": {
            "breakaway_length_mm": round(BREAKAWAY_LEN, 1),
            "clasp_pitch_mm": round(clasp_pitch, 1),
            "clasp_count": N_CLASP,
            "clasp_dia_mm": round(clasp_dia, 1),
            "skirt_circ_mm": round(SKIRT_CIRC, 1),
            "note": "clasps = round(breakaway_length / clasp_pitch), so the holding force per unit "
                    "length stays constant whatever the size; the seam allowance is floored to "
                    "hold the clasp with margin.",
        },
        "closure": "magnetic breakaway seam (collar to hem)",
        "drafting": "Made to measure to bust, waist, hip and lengths; clasp count solved.",
    }
    return pattern


result = build()
