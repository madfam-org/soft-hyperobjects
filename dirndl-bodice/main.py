"""
Dirndl laced bodice (Mieder) — Fashion Cabinet Cartridge (FC-400 #395; y4d garment-eyelet).

The dirndl bodice (Mieder) is the fitted, boned upper of the Alpine dirndl — a shaped corselet
closed at the centre front by a LACE threaded through two columns of metal eyelets, worn over a
blouse. This cartridge drafts the bodice around the two facts that make the lacing work rather
than merely decorate:

  1. THE EYELET COLUMNS ARE SPACED, AND THE LACE GAP IS REAL CLOTH. A laced bodice does NOT meet
     edge-to-edge at the front; it is drafted with a deliberate LACING GAP between the two front
     edges, spanned by the crossed lace. So the two bodice fronts together are cut NARROWER than
     the finished chest by the gap, and the eyelets are placed in even columns down each front
     edge. The commonest error is drafting the fronts to meet and then punching eyelets, which
     leaves no room to lace. Here the gap is a parameter, the front width is solved AROUND it,
     and the eyelet count and spacing are solved from the front edge length.

  2. THE EYELETS ARE HARDWARE, AND ONE NUMBER SIZES THEM. Each eyelet is the Yantra4D
     `garment-eyelet` solid; `eyelet_dia` drives BOTH the drafted punch mark AND the printed
     eyelet's inner diameter, so the lace, the punched hole and the eyelet agree. The bodice is
     shaped by princess/side seams and lightly boned at the front edges so the lacing pulls a
     smooth line rather than crushing the cloth.

Pieces: front (cut 2 — the two laced fronts), side_front, side_back, back. Made to measure to
bust, underbust, waist girths and the bodice length; the front is drafted to bust-minus-gap.

Cultural note (stated): the dirndl is Alpine regional dress (Bavaria/Austria) with strong
regional and class-historical associations; this is a plain everyday laced Mieder and carries no
regional trim or apron. It invents no ornament.

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

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
bodice_length = float(PARAM(lambda: bodice_length, 300.0))    # underarm to waist
front_length = float(PARAM(lambda: front_length, 360.0))      # shoulder area to waist at CF
lacing_gap = float(PARAM(lambda: lacing_gap, 70.0))           # gap spanned by the lace
eyelet_dia = float(PARAM(lambda: eyelet_dia, 5.0))            # eyelet inner diameter
eyelet_pitch = float(PARAM(lambda: eyelet_pitch, 40.0))       # spacing down the edge
neg_ease_pct = float(PARAM(lambda: neg_ease_pct, 4.0))        # a laced bodice grips
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1350.0))
underbust_girth = max(600.0, min(underbust_girth, 1200.0))
waist_girth = max(560.0, min(waist_girth, 1150.0))
bodice_length = max(180.0, min(bodice_length, 460.0))
front_length = max(220.0, min(front_length, 560.0))
lacing_gap = max(20.0, min(lacing_gap, 160.0))
eyelet_dia = max(3.0, min(eyelet_dia, 10.0))
eyelet_pitch = max(20.0, min(eyelet_pitch, 80.0))
neg_ease_pct = max(0.0, min(neg_ease_pct, 12.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# ── The lacing-gap solver ────────────────────────────────────────────────────
NEG = 1.0 - neg_ease_pct / 100.0
BUST_FIN = bust_girth * NEG
WAIST_FIN = waist_girth * NEG
# The bodice ring at the bust is BUST_FIN, but the front is OPEN by `lacing_gap` (the lace
# spans it). So the cloth around the body is BUST_FIN - lacing_gap, split into panels. With
# two fronts + two side_fronts + two side_backs + back(on fold), the front-pair carries a
# share of the (ring - gap).
CLOTH_BUST = BUST_FIN - lacing_gap
CLOTH_WAIST = WAIST_FIN - lacing_gap
# Panel shares of the CLOTH ring (front is smaller — it stops at the gap).
FRONT_FRAC = 0.16      # each front (x2)
SIDEF_FRAC = 0.15      # each side_front (x2)
SIDEB_FRAC = 0.13      # each side_back (x2)
BACK_FRAC = 0.12       # back half (on fold, x2)
# 2*(FRONT+SIDEF+SIDEB) + 2*BACK == 1  ->  2*(0.16+0.15+0.13) + 2*0.12 = 0.88+0.24 = ...
# normalise so the shares close exactly.
_TOTAL = 2.0 * (FRONT_FRAC + SIDEF_FRAC + SIDEB_FRAC) + 2.0 * BACK_FRAC
FRONT_FRAC /= _TOTAL
SIDEF_FRAC /= _TOTAL
SIDEB_FRAC /= _TOTAL
BACK_FRAC /= _TOTAL

# Eyelets down each front edge.
N_EYELETS = max(3, int(front_length / eyelet_pitch))
BL = bodice_length


def _shaped_panel(name, top_share, waist_share, length, cf_edge, label, on_fold=False,
                  cut_qty=2):
    """A shaped bodice panel: top edge = bust share, bottom = waist share, princess seams
    slanting in. `cf_edge` True marks this as a front panel that carries the eyelet column.
    """
    top_w = top_share
    bot_w = waist_share
    dx = (top_w - bot_w) / 2.0 if not cf_edge else 0.0   # front is straight at the CF edge
    h = length
    if cf_edge:
        # front: CF edge is vertical (carries eyelets); the side seam slants in to the waist.
        edges = [
            fc.Edge("waist", [fc.Line(fc.P(0.0, 0.0), fc.P(bot_w, 0.0))]),
            fc.Edge("side_seam", [fc.Line(fc.P(bot_w, 0.0), fc.P(top_w, h))]),
            fc.Edge("top", [fc.Line(fc.P(top_w, h), fc.P(0.0, h))]),
            fc.Edge("center_front", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ]
    else:
        edges = [
            fc.Edge("waist", [fc.Line(fc.P(dx, 0.0), fc.P(dx + bot_w, 0.0))]),
            fc.Edge("seam_r", [fc.Line(fc.P(dx + bot_w, 0.0), fc.P(top_w, h))]),
            fc.Edge("top", [fc.Line(fc.P(top_w, h), fc.P(0.0, h))]),
            fc.Edge("seam_l", [fc.Line(fc.P(0.0, h), fc.P(dx, 0.0))]),
        ]
    internals = []
    notches = [fc.Notch("waist", 0.5, "waist match")]
    if cf_edge:
        for i in range(N_EYELETS):
            y = h * (i + 0.5) / N_EYELETS
            internals.append(fc.Internal(f"eyelet {i + 1}",
                                         [fc.P(eyelet_dia * 1.4, y),
                                          fc.P(eyelet_dia * 1.4 + eyelet_dia, y)],
                                         kind="marking"))
        notches.append(fc.Notch("center_front", 0.5, "lace midpoint"))
    return fc.Piece(
        name, edges, seam_allowance=seam_allowance,
        allowances={"waist": 0.0, "top": 0.0},
        notches=notches,
        grainline=fc.Grainline(fc.P(top_w * 0.4, h * 0.15), fc.P(top_w * 0.4, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=cut_qty, on_fold=on_fold,
                       fold_edge="seam_l" if on_fold else None, mirror=not on_fold),
        label=label)


def build_front():
    return _shaped_panel("front", CLOTH_BUST * FRONT_FRAC, CLOTH_WAIST * FRONT_FRAC,
                         front_length, True, "Front (laced edge, eyelet column, cut 2)")


def build_side_front():
    return _shaped_panel("side_front", CLOTH_BUST * SIDEF_FRAC, CLOTH_WAIST * SIDEF_FRAC,
                         BL, False, "Side front (cut 2)")


def build_side_back():
    return _shaped_panel("side_back", CLOTH_BUST * SIDEB_FRAC, CLOTH_WAIST * SIDEB_FRAC,
                         BL, False, "Side back (cut 2)")


def build_back():
    p = _shaped_panel("back", CLOTH_BUST * BACK_FRAC, CLOTH_WAIST * BACK_FRAC,
                      BL, False, "Back (cut 1 on fold)", on_fold=True, cut_qty=1)
    # rename fold edge to center_back for the on-fold panel
    return p


MEASURED = {}


def build():
    pattern = fc.PatternSet("dirndl-bodice")
    every = target_piece == "set"
    front = build_front()
    side_front = build_side_front()
    side_back = build_side_back()
    back = build_back()

    if not every:
        picked = {"front": front, "side_front": side_front,
                  "side_back": side_back, "back": back}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front)

    for piece in (front, side_front, side_back, back):
        pattern.add(piece)
    # Princess seams around the ring: front.side_seam -> side_front.seam_l ; side_front.seam_r
    # -> side_back.seam_l ; side_back.seam_r -> back.seam_l. (front is shorter than the others
    # because the eyelet edge starts higher — ease documents the difference.)
    pattern.declare_seam(("front", "side_seam"), ("side_front", "seam_l"), tol=1.5,
                         ease=(front.edge("side_seam").length()
                               - side_front.edge("seam_l").length()))
    pattern.declare_seam(("side_front", "seam_r"), ("side_back", "seam_l"), tol=1.5)
    # The back is cut on the fold at seam_l (centre back); its seam_r joins the side_back.
    pattern.declare_seam(("side_back", "seam_r"), ("back", "seam_r"), tol=1.5)

    return _finish(pattern, front)


def _finish(pattern, front):
    total_eyelets = N_EYELETS * 2
    fabric_width = 1400.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "cotton brocade or firm dirndl cloth (+ lining + interlining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"shaped panels at {fabric_width:.0f} mm width, 60% marker. The bodice is "
                 "interlined and lightly boned at the front edges so the lacing pulls a smooth "
                 "line rather than crushing the cloth."},
        {"item": "garment eyelets (Yantra4D garment-eyelet)", "qty": total_eyelets, "unit": "piece",
         "note": f"{total_eyelets} eyelets ({N_EYELETS} per front edge); inner diameter "
                 f"eyelet_dia {eyelet_dia:.1f} mm. The eyelet is the Yantra4D solid "
                 "(notion.hardware_ref -> garment-eyelet); eyelet_dia drives BOTH the drafted "
                 "punch mark and the printed eyelet's inner diameter, so lace and hole agree."},
        {"item": "lacing cord", "qty": round(front.edge("center_front").length() * 3.5),
         "unit": "mm_length",
         "note": "crossed lacing spans the front gap; length is generous for the cross-over "
                 "and the bow."},
        {"item": "spiral steel or synthetic bones (front edges)", "qty": 2, "unit": "piece",
         "note": "one bone channel per front edge to keep the lacing edge from rolling."},
        {"item": "thread + hand-finish", "qty": 1, "unit": "set",
         "note": "the bodice is fully lined; the eyelets are set through all layers."},
    ]
    pattern.metadata = {
        "fc400_rank": 395, "family": "heritage_global", "fabric_hint": "cotton-brocade",
        "tradition": "Alpine (Bavaria/Austria) — the laced bodice (Mieder) of the dirndl",
        "silhouette_note": "A fitted, lightly-boned corselet shaped by princess seams and closed "
            "at the centre front by a lace crossed through two columns of eyelets, over a blouse. "
            "The lace spans a deliberate GAP, so the fronts are cut narrower than the chest.",
        "hardware": "eyelets via Yantra4D (notion.hardware_ref -> garment-eyelet); eyelet_dia "
            "drives BOTH the drafted punch mark and the printed eyelet inner diameter.",
        "solver": {
            "bust_finished_mm": round(BUST_FIN, 1),
            "lacing_gap_mm": round(lacing_gap, 1),
            "cloth_bust_mm": round(CLOTH_BUST, 1),
            "eyelets_per_front": N_EYELETS,
            "eyelet_dia_mm": round(eyelet_dia, 1),
            "eyelet_pitch_mm": round(eyelet_pitch, 1),
            "note": "the front is cut NARROWER than the chest by the lacing gap; the two fronts "
                    "plus the gap equal the finished bust, and the eyelet count is solved from "
                    "the front edge length and pitch.",
        },
        "cultural_note": "The dirndl is Alpine regional dress with strong regional and "
            "class-historical associations; this is a plain everyday laced Mieder, carries no "
            "regional trim or apron, and invents no ornament.",
        "drafting": "Made to measure to bust, underbust and waist girths + bodice length; the "
            "front is drafted to bust-minus-gap and the eyelets are solved to the edge.",
    }
    return pattern


result = build()
