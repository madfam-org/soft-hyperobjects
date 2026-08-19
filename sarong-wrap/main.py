"""
Sarong (wrap) — Fashion Cabinet Garment Cartridge (FC-200 rank #157, Southeast Asian
and pan-tropical heritage).

The sarong is a large rectangle of cloth wrapped around the waist (or chest) and tucked or
tied — worn across Southeast Asia, the Pacific, East Africa and beyond under many names
(sarong, kain, lungi, kanga, pareo). Some are worn open; many are sewn into a tube (the
Malay/Indonesian kain sarong). This cartridge offers BOTH: a flat open length, or the same
length seamed into a tube, with the fold/tuck reference marked. The printed and woven motifs
that carry regional identity are the maker's and are not reproduced here. Offered with respect.

Pieces:
  - panel : one wide rectangle; in tube mode the two short ends join into a loop.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # panel|set

waist_girth  = float(PARAM(lambda: waist_girth, 900.0))    # wrap girth (waist or chest)
wrap_turns   = float(PARAM(lambda: wrap_turns, 1.7))       # how far it wraps around (>1 overlaps)
drop_length  = float(PARAM(lambda: drop_length, 1050.0))   # waist to hem
sewn_tube    = int(  PARAM(lambda: sewn_tube, 0))          # 0 = open wrap, 1 = seamed tube
border_band  = float(PARAM(lambda: border_band, 70.0))     # marked hem/head border
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
waist_girth  = max(600.0, min(waist_girth, 1500.0))
wrap_turns   = max(1.0, min(wrap_turns, 2.4))
drop_length  = max(500.0, min(drop_length, 1500.0))
sewn_tube    = 1 if sewn_tube else 0
border_band  = max(0.0, min(border_band, 220.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

# Tube mode circumference must clear the hip; open mode uses the wrap turns.
if sewn_tube:
    Lx = max(waist_girth * 1.18, waist_girth + 120.0)   # ease to step through / tuck
else:
    Lx = waist_girth * wrap_turns
Wy = drop_length


def build_panel():
    internals = []
    if border_band > 0.0:
        internals.append(fc.Internal("hem-border", [fc.P(0.0, border_band),
                                                     fc.P(Lx, border_band)], kind="marking"))
        internals.append(fc.Internal("head-border", [fc.P(0.0, Wy - border_band),
                                                      fc.P(Lx, Wy - border_band)], kind="marking"))
    edges = [
        fc.Edge("start", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, Wy))]),
        fc.Edge("head", [fc.Line(fc.P(0.0, Wy), fc.P(Lx, Wy))]),
        fc.Edge("end", [fc.Line(fc.P(Lx, Wy), fc.P(Lx, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(Lx, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "panel", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "head": hem_allowance},
        notches=[fc.Notch("head", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(Lx * 0.5, 80.0), fc.P(Lx * 0.5, Wy - 80.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Sarong panel",
    )


def build():
    pattern = fc.PatternSet("sarong-wrap")
    panel = build_panel()
    pattern.add(panel)
    if sewn_tube:
        # The two short ends join into a tube — a real, balanced (identical-length) seam.
        pattern.declare_seam(("panel", "start"), ("panel", "end"), tol=1.0)
    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "lightweight cotton, rayon, or batik cloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 82% marker; one rectangle, "
                 + ("seamed into a tube." if sewn_tube else "worn open and tucked/tied.")},
        {"item": "matching thread", "qty": 1, "unit": "spool",
         "note": "hems all round" + ("; one join seam for the tube." if sewn_tube else ".")},
    ]
    pattern.metadata = {
        "fc200_rank": 157,
        "family": "heritage_global",
        "fabric_hint": "algodon-batik",
        "heritage_note": "The sarong (also kain, lungi, kanga, pareo across regions) is living, "
            "pan-tropical dress. This cartridge drafts the CLOTH — an open wrap or a seamed "
            "tube at customary proportions with borders marked; the printed/woven motifs that "
            "carry regional identity are the maker's and are not reproduced here. With respect.",
        "construction": ("open wrap: a single hemmed rectangle, wrapped and tucked."
                         if not sewn_tube else
                         "sewn tube: the two short ends joined into a loop, stepped into and "
                         "rolled/tucked at the waist."),
        "solved": {"panel_width_mm": round(Lx, 1), "drop_mm": round(Wy, 1),
                   "sewn_tube": bool(sewn_tube), "wrap_turns": wrap_turns},
    }
    return pattern


result = build()
