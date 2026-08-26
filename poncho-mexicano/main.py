"""
Gabán poncho (mexicano) — Fashion Cabinet Cartridge (FC-400 #400; heritage_global, Mexican).

The Mexican gabán/sarape poncho: a CLOSED rectangle of sarape wool with a central head-slit
(bocamanga), worn over the head so it hangs front and back. It differs from the FC-300 ruana in
exactly the one decisive way the ruana README names: a ruana is OPEN down the front, a poncho is
CLOSED — a whole rectangle with only a slit for the head. That single difference is the garment,
and this cartridge draws the closed poncho honestly:

  1. THE CLOTH IS A CLOSED RECTANGLE, SLIT ONLY FOR THE HEAD. The poncho is one rectangle (often
     two loom widths joined at a centre seam, leaving the head-slit unsewn at the join). The
     head-slit is the ONLY opening; there is no front opening, no sleeves, no fastening. This
     cartridge draws the rectangle and cuts only the bocamanga, solving the slit length from the
     head girth so the head passes but the neck is not swamped.

  2. THE SIZE IS THE DRAPE, FROM SHOULDER SPAN AND LENGTH. A poncho hangs from the shoulders; its
     width is chosen from the wearer's shoulder-to-elbow reach (how far it drapes over the arms)
     and its length from shoulder to the desired hem. The bocamanga sits at the centre so the
     front and back hang equal, or is offset for a longer front (the gabán often hangs longer at
     the back). The sarape's woven design and its central diamond (the ojo/centro) are the
     weaver's and are NOT drawn.

Pieces: poncho (the whole rectangle with the head-slit), and a fringe/edge-binding strip. Made to
measure to the wearer's shoulder span, poncho length, and head girth (which sizes the slit).

Cultural note (stated): the sarape and gabán are Mexican regional weaving traditions (notably
Saltillo and Tlaxcala) whose designs — the central diamond, the warp-striped ground — carry
regional identity. This cartridge draws NO sarape design and names none; it supplies the poncho's
dimensions and the head-slit, and the weave is the weaver's.

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

shoulder_span = float(PARAM(lambda: shoulder_span, 1300.0))   # width of the poncho (drape)
poncho_length = float(PARAM(lambda: poncho_length, 1000.0))   # shoulder to hem (per side)
head_girth = float(PARAM(lambda: head_girth, 580.0))          # sizes the head-slit
slit_offset = float(PARAM(lambda: slit_offset, 0.0))          # centre offset (longer back)
seam_type = float(PARAM(lambda: seam_type, 1.0))              # 1 = centre-seamed, 0 = whole
fringe_depth = float(PARAM(lambda: fringe_depth, 60.0))       # fringe at the hem
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
shoulder_span = max(900.0, min(shoulder_span, 1800.0))
poncho_length = max(600.0, min(poncho_length, 1400.0))
head_girth = max(480.0, min(head_girth, 680.0))
slit_offset = max(-150.0, min(slit_offset, 150.0))
seam_type = 1.0 if round(seam_type) >= 1 else 0.0
fringe_depth = max(0.0, min(fringe_depth, 160.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── The head-slit solver ─────────────────────────────────────────────────────
# The bocamanga must let the head pass: the slit length is a fraction of the head girth (a slit
# opens to roughly twice its length as an ellipse, so slit ~ head_girth / 2 clears the head).
SLIT_LEN = head_girth * 0.5
W = shoulder_span
FULL_H = 2.0 * poncho_length            # front + back hang, the whole rectangle height
CENTRE_Y = FULL_H / 2.0 + slit_offset   # where the slit centres (offset for a longer back)


def build_poncho():
    """The whole poncho rectangle (cut 1), with the central head-slit as an internal opening.

    The rectangle is W wide x FULL_H tall (front + back). The head-slit is a short slit at the
    centre, drawn as an internal marking (cut but not an outline hole, since the kernel outline
    stays a rectangle and the slit is a finished opening). The centre seam (if seam_type) is
    marked; it is sewn except across the slit.
    """
    edges = [
        fc.Edge("hem_front", [fc.Line(fc.P(0.0, 0.0), fc.P(W, 0.0))]),
        fc.Edge("selvedge_r", [fc.Line(fc.P(W, 0.0), fc.P(W, FULL_H))]),
        fc.Edge("hem_back", [fc.Line(fc.P(W, FULL_H), fc.P(0.0, FULL_H))]),
        fc.Edge("selvedge_l", [fc.Line(fc.P(0.0, FULL_H), fc.P(0.0, 0.0))]),
    ]
    cx = W / 2.0
    internals = [
        # the head-slit (bocamanga): a slit centred at (cx, CENTRE_Y), SLIT_LEN long across the
        # shoulder line (perpendicular to the drape).
        fc.Internal("head-slit (bocamanga) — cut and bind",
                    [fc.P(cx - SLIT_LEN / 2.0, CENTRE_Y),
                     fc.P(cx + SLIT_LEN / 2.0, CENTRE_Y)], kind="marking"),
        # the shoulder line (where the poncho folds over the shoulders)
        fc.Internal("shoulder line", [fc.P(0.0, CENTRE_Y), fc.P(W, CENTRE_Y)], kind="marking"),
    ]
    if seam_type >= 1.0:
        internals.append(fc.Internal("centre seam (sewn except across the slit)",
                                     [fc.P(cx, 0.0), fc.P(cx, FULL_H)], kind="marking"))
    return fc.Piece(
        "poncho", edges, seam_allowance=seam_allowance,
        allowances={"hem_front": 0.0, "hem_back": 0.0, "selvedge_r": 0.0, "selvedge_l": 0.0},
        notches=[fc.Notch("selvedge_l", CENTRE_Y / FULL_H, "shoulder line"),
                 fc.Notch("hem_front", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(cx, FULL_H * 0.12), fc.P(cx, FULL_H * 0.88)),
        internals=internals, cut=fc.CutSpec(quantity=1),
        label="Poncho — closed rectangle, head-slit only (cut 1)")


def build_half_web():
    """One loom half-web (cut 2) for the centre-seamed poncho: half the width, full height. The
    two are joined at the centre, leaving the head-slit open at the join.
    """
    w = W / 2.0
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("centre_seam", [fc.Line(fc.P(w, 0.0), fc.P(w, FULL_H))]),
        fc.Edge("top", [fc.Line(fc.P(w, FULL_H), fc.P(0.0, FULL_H))]),
        fc.Edge("selvedge", [fc.Line(fc.P(0.0, FULL_H), fc.P(0.0, 0.0))]),
    ]
    internals = [fc.Internal("slit half (leave open at centre seam)",
                             [fc.P(w, CENTRE_Y - SLIT_LEN / 2.0),
                              fc.P(w, CENTRE_Y + SLIT_LEN / 2.0)], kind="marking")]
    return fc.Piece(
        "half_web", edges, seam_allowance=seam_allowance,
        allowances={"hem": 0.0, "top": 0.0, "selvedge": 0.0},
        notches=[fc.Notch("centre_seam", CENTRE_Y / FULL_H, "slit centre"),
                 fc.Notch("hem", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, FULL_H * 0.12), fc.P(w * 0.5, FULL_H * 0.88)),
        internals=internals, cut=fc.CutSpec(quantity=2, mirror=True),
        label="Half-web (cut 2, centre-seamed, slit open at join)")


def build():
    pattern = fc.PatternSet("poncho-mexicano")
    poncho = build_poncho()
    half = build_half_web()

    picked = {"poncho": poncho, "half_web": half}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        pattern.add(poncho)
        pattern.add(half)
        # The two half-webs join at the centre seam (equal by construction), leaving the slit open.
        pattern.declare_seam(("half_web", "centre_seam"), ("half_web", "centre_seam"), tol=0.5)

    hem_run = 2.0 * W                    # front + back hems
    fabric_width = W / 2.0
    total_run = FULL_H * 2.0            # two half-webs
    pattern.bom = [
        {"item": "sarape wool (two loom half-webs)", "qty": round(total_run / 10.0) * 10,
         "unit": "mm_length",
         "note": f"two half-webs x {FULL_H:.0f} mm at {fabric_width:.0f} mm each; assembled "
                 f"{W:.0f} x {FULL_H:.0f} mm. The sarape is woven with the weaver's own design "
                 "and central diamond — this cartridge supplies dimensions, NOT a weave."},
        {"item": "head-slit binding (bocamanga)", "qty": round(SLIT_LEN * 2.2), "unit": "mm_length",
         "note": f"the ONLY opening; slit {SLIT_LEN:.0f} mm, bound so it does not fray. Solved "
                 "from the head girth so the head passes without swamping the neck."},
        {"item": "hem fringe / binding", "qty": round(hem_run), "unit": "mm_length",
         "note": f"the poncho's hems ({hem_run:.0f} mm total) are fringed or bound; fringe depth "
                 f"{fringe_depth:.0f} mm."},
        {"item": "wool thread", "qty": 1, "unit": "spool",
         "note": "the centre seam is sewn EXCEPT across the head-slit; there are no other seams "
                 "and no fastenings."},
    ]
    pattern.metadata = {
        "fc400_rank": 400, "family": "heritage_global", "fabric_hint": "wool-sarape",
        "tradition": "Mexican — the closed gabán/sarape poncho with a central head-slit",
        "silhouette_note": "A CLOSED rectangle of sarape wool with a central head-slit "
            "(bocamanga), worn over the head to hang front and back. It differs from the ruana in "
            "exactly one way: the ruana is OPEN down the front, the poncho is CLOSED — a whole "
            "rectangle, slit only for the head.",
        "hardware": "none — the poncho is a closed rectangle with no fastening.",
        "closed_vs_ruana": "The single decisive difference from the FC-300 poncho-ruana: a ruana "
            "hangs OPEN down the front, this poncho is a CLOSED rectangle with only the head-slit.",
        "solved": {
            "shoulder_span_mm": round(W, 1),
            "full_height_mm": round(FULL_H, 1),
            "head_girth_mm": round(head_girth, 1),
            "head_slit_mm": round(SLIT_LEN, 1),
            "slit_offset_mm": round(slit_offset, 1),
            "note": "the head-slit length is solved from the head girth (~half of it, so the "
                    "head passes as the slit opens to an ellipse) and can be offset for a longer "
                    "back; nothing else is cut.",
        },
        "cultural_note": "The sarape and gabán are Mexican regional weaving traditions (notably "
            "Saltillo and Tlaxcala) whose designs — the central diamond, the warp-striped ground "
            "— carry regional identity. This cartridge draws NO sarape design and names none; it "
            "supplies the poncho's dimensions and the head-slit, and the weave is the weaver's.",
        "drafting": "Made to measure to shoulder span, poncho length and head girth; a closed "
            "rectangle slit only for the head.",
    }
    return pattern


result = build()
