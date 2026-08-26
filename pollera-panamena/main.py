"""
Pollera panameña — Fashion Cabinet Heritage Cartridge (FC-500 #495, heritage_global; Panama;
made-to-measure, tier 4).

The pollera panameña is the elaborate national dress of Panama — a two-piece of extraordinary
fullness: the CAMISA, an off-shoulder blouse of two gathered flounces (the arandela superior
and arandela inferior) worn off the shoulders, and the POLLERÓN, a two-tier gathered skirt of
several loom widths, both worked in fine white cotton or linen with drawn-thread (calado) and
appliqué (sombreado / marcado) embroidery and edged with lace. It is the pollera de gala (the
formal, embroidered pollera) and the pollera montuna (the everyday one), and it is the pride of
Panamanian folkloric dress. This is the made-to-measure tier of the FC-500 heritage lane.

Two things the draft solves honestly:

  1. THE FULLNESS IS SOLVED AT EVERY GATHERED SEAM. The camisa flounces are gathered onto the
     neckline/shoulder band, and the two skirt tiers are gathered onto the waistband and onto
     each other. Every gathered panel width is SOLVED from the band it gathers onto times its
     gather ratio, so each gathered seam matches by construction — the pollera's volume is real
     and reported, tier by tier.

  2. THE CAMISA IS OFF-SHOULDER, SO THE NECK BAND IS SOLVED FROM THE SHOULDER SPAN, NOT THE
     NECK. The blouse sits off the shoulders on a wide gathered band; that band's length is
     solved from the shoulder-to-shoulder span plus the arm room, not from a neck girth.

Pieces:
  - camisa_top : the upper camisa flounce (arandela superior), gathered onto the shoulder band.
  - camisa_bot : the lower camisa flounce (arandela inferior).
  - band       : the off-shoulder neck/shoulder band the camisa gathers onto.
  - pollera_up : the upper skirt tier, gathered onto the waistband.
  - pollera_lo : the lower skirt tier, gathered onto the upper tier.

Hardware: waist hook-and-eye — Yantra4D hook-and-eye, LINKED (the pollera also laces with the
lana wool cords, drafted as ties elsewhere).

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
target_piece = str(PARAM(lambda: target_piece, "set"))
# camisa_top|camisa_bot|band|pollera_up|pollera_lo|set

shoulder_span = float(PARAM(lambda: shoulder_span, 420.0))   # shoulder to shoulder (off-shoulder)
arm_room = float(PARAM(lambda: arm_room, 220.0))
waist_girth = float(PARAM(lambda: waist_girth, 760.0))
camisa_top_drop = float(PARAM(lambda: camisa_top_drop, 200.0))   # upper flounce depth
camisa_bot_drop = float(PARAM(lambda: camisa_bot_drop, 240.0))   # lower flounce depth
camisa_gather = float(PARAM(lambda: camisa_gather, 2.4))
pollera_up_drop = float(PARAM(lambda: pollera_up_drop, 420.0))
pollera_lo_drop = float(PARAM(lambda: pollera_lo_drop, 460.0))
skirt_gather = float(PARAM(lambda: skirt_gather, 3.4))
tier_gather = float(PARAM(lambda: tier_gather, 1.6))         # lower tier vs upper tier
band_height = float(PARAM(lambda: band_height, 30.0))
closure_span = float(PARAM(lambda: closure_span, 20.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 20.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
shoulder_span = max(340.0, min(shoulder_span, 520.0))
arm_room = max(140.0, min(arm_room, 320.0))
waist_girth = max(600.0, min(waist_girth, 1080.0))
camisa_top_drop = max(120.0, min(camisa_top_drop, 300.0))
camisa_bot_drop = max(140.0, min(camisa_bot_drop, 340.0))
camisa_gather = max(1.6, min(camisa_gather, 3.4))
pollera_up_drop = max(300.0, min(pollera_up_drop, 560.0))
pollera_lo_drop = max(320.0, min(pollera_lo_drop, 600.0))
skirt_gather = max(2.2, min(skirt_gather, 4.8))
tier_gather = max(1.3, min(tier_gather, 2.4))
band_height = max(20.0, min(band_height, 50.0))
closure_span = max(12.0, min(closure_span, 34.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 40.0))

# ── The fullness solve, tier by tier ─────────────────────────────────────────
# The off-shoulder band spans both shoulders plus arm room (front and back), gathered.
BAND_LEN = (shoulder_span + arm_room) * 2.0
CAMISA_TOP_WIDTH = BAND_LEN * camisa_gather        # upper flounce gathered onto the band
CAMISA_BOT_WIDTH = CAMISA_TOP_WIDTH * 1.15         # lower flounce, a touch fuller
# The skirt: the upper tier gathered onto the waistband, the lower tier onto the upper.
WAIST_BAND = waist_girth + 40.0
POLLERA_UP_WIDTH = WAIST_BAND * skirt_gather
POLLERA_LO_WIDTH = POLLERA_UP_WIDTH * tier_gather


def _flounce(name, width, drop, label, gather_on_top=True):
    """A gathered flounce/tier: a rectangle width x drop, gathered along its top edge (marked).
    The top edge carries the full flat width; it is gathered onto its band in make-up."""
    w, h = width, drop
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(w, 0.0)
    p2 = fc.P(w, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("hem", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("top", [fc.Line(p2, p3)]),      # gathered edge
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [
        fc.Internal("gather-line", [fc.P(0.0, h - 12.0), fc.P(w, h - 12.0)], kind="marking"),
        fc.Internal("calado-band", [fc.P(0.0, hem_allowance + 30.0),
                                    fc.P(w, hem_allowance + 30.0)], kind="marking"),
    ]
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "top": 0.0},
        notches=[fc.Notch("top", 0.25, "quarter"), fc.Notch("top", 0.5, "half"),
                 fc.Notch("top", 0.75, "quarter")],
        grainline=fc.Grainline(fc.P(w * 0.5, hem_allowance + 20.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals, cut=fc.CutSpec(quantity=1), label=label)


def build_band():
    """The off-shoulder neck/shoulder band the camisa gathers onto."""
    ln = BAND_LEN
    h = band_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("gathered_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("gathered_edge", 0.25, "shoulder"),
                 fc.Notch("gathered_edge", 0.5, "centre"),
                 fc.Notch("gathered_edge", 0.75, "shoulder")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, band_height + 2.0),
                                        fc.P(ln, band_height + 2.0)], kind="marking"),
                   fc.Internal("lana-cord", [fc.P(0.0, band_height * 0.5),
                                             fc.P(ln, band_height * 0.5)], kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Off-shoulder camisa band")


def build_waistband():
    """The pollera waistband the upper skirt tier gathers onto; the hook-and-eye closes it."""
    ln = WAIST_BAND
    h = band_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("gathered_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "waistband", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("gathered_edge", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, band_height + 2.0),
                                        fc.P(ln, band_height + 2.0)], kind="marking"),
                   fc.Internal("waist-hook", [fc.P(ln - closure_span, band_height * 0.5),
                                              fc.P(ln - 5.0, band_height * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Pollera waistband (hook-and-eye)")


def build():
    pattern = fc.PatternSet("pollera-panamena")
    everything = target_piece == "set"
    if everything or target_piece == "camisa_top":
        pattern.add(_flounce("camisa_top", CAMISA_TOP_WIDTH, camisa_top_drop,
                             "Camisa upper flounce (arandela superior)"))
    if everything or target_piece == "camisa_bot":
        pattern.add(_flounce("camisa_bot", CAMISA_BOT_WIDTH, camisa_bot_drop,
                             "Camisa lower flounce (arandela inferior)"))
    if everything or target_piece == "band":
        pattern.add(build_band())
    if everything or target_piece == "pollera_up":
        pattern.add(_flounce("pollera_up", POLLERA_UP_WIDTH, pollera_up_drop,
                             "Pollerón upper tier"))
    if everything or target_piece == "pollera_lo":
        pattern.add(_flounce("pollera_lo", POLLERA_LO_WIDTH, pollera_lo_drop,
                             "Pollerón lower tier"))
    if everything or target_piece == "waistband":
        pattern.add(build_waistband())
    # Every join here is a GATHER (an intentionally unequal seam: a wide flat panel gathered
    # onto a shorter band), so there is no equal-length pattern seam to declare. Each gather
    # ratio is the design and is reported in the metadata.

    total_cloth = (CAMISA_TOP_WIDTH * camisa_top_drop + CAMISA_BOT_WIDTH * camisa_bot_drop
                   + POLLERA_UP_WIDTH * pollera_up_drop + POLLERA_LO_WIDTH * pollera_lo_drop)
    pattern.bom = [
        {"item": "fine white cotton or linen (pollera cloth)", "qty": round(total_cloth / 1000.0),
         "unit": "cm2",
         "note": "the pollera is extraordinarily full — every panel is gathered, so the cloth "
                 "quantity is very high. Fine white cotton or linen for the pollera de gala."},
        {"item": "calado / sombreado embroidery + lace", "qty": 1, "unit": "set",
         "note": "the drawn-thread (calado) and appliqué (sombreado / marcado) embroidery and "
                 "the lace edging are the maker's — a pollera de gala can take a year to work. "
                 "None is drafted here."},
        {"item": "waist hook-and-eye + lana wool cords", "qty": 1, "unit": "set",
         "note": f"{closure_span:.0f} mm hook-and-eye at the waist; the pollera also laces "
                 f"with the coloured lana wool cords (drafted as ties elsewhere)."},
    ]
    pattern.metadata = {
        "fc500_rank": 495,
        "family": "heritage_global",
        "fabric_hint": "algodon-percal",
        "made_to_measure": True,
        "finished_mm": {
            "shoulder_span": round(shoulder_span, 1),
            "waist_girth": round(waist_girth, 1),
            "camisa_top_width": round(CAMISA_TOP_WIDTH, 1),
            "pollera_up_width": round(POLLERA_UP_WIDTH, 1),
        },
        "solved": {
            "band_length_mm": round(BAND_LEN, 2),
            "camisa_top_width_mm": round(CAMISA_TOP_WIDTH, 2),
            "camisa_bot_width_mm": round(CAMISA_BOT_WIDTH, 2),
            "camisa_gather_ratio": round(camisa_gather, 2),
            "waist_band_mm": round(WAIST_BAND, 2),
            "pollera_up_width_mm": round(POLLERA_UP_WIDTH, 2),
            "pollera_lo_width_mm": round(POLLERA_LO_WIDTH, 2),
            "skirt_gather_ratio": round(skirt_gather, 2),
            "tier_gather_ratio": round(tier_gather, 2),
            "note": "the pollera's FULLNESS is solved at EVERY gathered seam: the camisa "
                    "flounces are gathered onto the off-shoulder band (camisa_gather_ratio), "
                    "the upper skirt tier onto the waistband (skirt_gather_ratio), and the "
                    "lower tier onto the upper (tier_gather_ratio). Each gathered panel width "
                    "is solved from the band it gathers onto, so every gathered seam matches by "
                    "construction. The camisa is OFF-SHOULDER, so its band is solved from the "
                    "shoulder span plus arm room, not from a neck girth.",
        },
        "heritage": {
            "garment": "pollera panameña — the national dress of Panama",
            "worn": "the off-shoulder camisa of two flounces over the two-tier pollerón skirt, "
                    "worked in calado and sombreado embroidery and edged with lace; the "
                    "pollera de gala (formal) and pollera montuna (everyday)",
            "construction": "gathered flounces and skirt tiers, each solved onto its band; an "
                            "off-shoulder band; a hook-and-eye and lana-cord waist",
            "excluded": "no specific calado, sombreado, or tembleque (the beaded head "
                        "ornaments) design is drawn — those are the maker's and can take a "
                        "year to work by hand",
        },
        "hardware": "waist hook-and-eye: Yantra4D hook-and-eye, linked, sized from the closure "
                    "span; the pollera also laces with the lana wool cords.",
    }
    return pattern


result = build()
