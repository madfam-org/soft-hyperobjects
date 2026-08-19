"""
Dirndl — Fashion Cabinet Garment Cartridge (FC-200 rank #154, Alpine heritage).

The dirndl is the traditional dress of the Alpine regions (Bavaria, Austria, and
neighbouring lands): a close-fitting bodice laced or buttoned at the front, joined at a
seamed waist to a full gathered skirt, and worn with a separate apron tied over it. This
cartridge drafts the GARMENT GEOMETRY — a shaped bodice, a gathered skirt rectangle, and
an apron panel — and marks (but does not reproduce) the regional trims, lacing, and apron
decoration that carry local identity. Offered with respect for the living tradition.

Pieces:
  - bodice : fitted front+back bodice half (cut on fold at CF/CB), waist-seamed.
  - skirt  : one wide gathered rectangle (cut on fold), gathered to the bodice waist.
  - apron  : a gathered apron panel narrower than the skirt, tied at the waist.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # bodice|skirt|apron|set

bust_girth   = float(PARAM(lambda: bust_girth, 920.0))     # full bust
waist_girth  = float(PARAM(lambda: waist_girth, 740.0))    # fitted waist
bodice_len   = float(PARAM(lambda: bodice_len, 380.0))     # shoulder to waist seam
skirt_length = float(PARAM(lambda: skirt_length, 700.0))   # waist to hem
gather_ratio = float(PARAM(lambda: gather_ratio, 2.2))     # skirt width / waist (fullness)
neck_width   = float(PARAM(lambda: neck_width, 180.0))     # square-ish neckline width
apron_ratio  = float(PARAM(lambda: apron_ratio, 0.62))     # apron width as fraction of skirt
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(700.0, min(bust_girth, 1400.0))
waist_girth  = max(550.0, min(waist_girth, 1300.0))
bodice_len   = max(300.0, min(bodice_len, 480.0))
skirt_length = max(400.0, min(skirt_length, 1100.0))
gather_ratio = max(1.6, min(gather_ratio, 3.2))
neck_width   = max(130.0, min(neck_width, 300.0))
apron_ratio  = max(0.45, min(apron_ratio, 0.85))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

BUST_HALF  = (bust_girth / 2.0) / 2.0      # quarter (on-fold half-panel)
WAIST_HALF = (waist_girth / 2.0) / 2.0
NECK_HALF  = neck_width / 2.0
SHOULDER   = BUST_HALF
ARMSCYE_DROP = 210.0
SKIRT_W = waist_girth * gather_ratio
SKIRT_HALF = SKIRT_W / 2.0
APRON_HALF = SKIRT_HALF * apron_ratio


def build_bodice(name, neck_dip, label):
    """A fitted bodice half: waist nipped from bust, square-ish neckline, armscye at
    the side. Cut on fold at centre. Front and back share the structural width."""
    top_y = bodice_len
    neck_pt = fc.P(0.0, top_y - neck_dip)
    neck_out = fc.P(NECK_HALF, top_y)
    shoulder_end = fc.P(SHOULDER, top_y - 40.0)
    armscye_bot = fc.P(BUST_HALF, top_y - ARMSCYE_DROP)
    waist_side = fc.P(WAIST_HALF, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
        fc.Edge("neck", [fc.curve_through(neck_pt, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0), side=-1.0)]),
        fc.Edge("shoulder", [fc.Line(neck_out, shoulder_end)]),
        fc.Edge("armscye", [fc.curve_through(shoulder_end, armscye_bot,
                                             bulge=0.16, side=-1.0)]),
        fc.Edge("side", [fc.Line(armscye_bot, waist_side)]),
        fc.Edge("waist", [fc.Line(waist_side, fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("shoulder", 0.0, "neck"), fc.Notch("waist", 1.0, "side")],
        grainline=fc.Grainline(fc.P(WAIST_HALF * 0.5, 40.0), fc.P(WAIST_HALF * 0.5, top_y - 60.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_skirt():
    """Full gathered skirt rectangle, cut on fold at CB, gathered to the bodice waist."""
    L = skirt_length
    internals = [fc.Internal("waist-gather",
                             [fc.P(0.0, L), fc.P(SKIRT_HALF, L)], kind="marking")]
    return fc.Piece(
        "skirt",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(SKIRT_HALF, L))]),
            fc.Edge("side", [fc.Line(fc.P(SKIRT_HALF, L), fc.P(SKIRT_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(SKIRT_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "quarter"), fc.Notch("side", 1.0, "waist")],
        grainline=fc.Grainline(fc.P(SKIRT_HALF * 0.5, 80.0), fc.P(SKIRT_HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Skirt",
    )


def build_apron():
    """A gathered apron panel, narrower than the skirt, gathered to a waist tie."""
    L = skirt_length - 60.0                     # apron sits a touch above the hem
    internals = [fc.Internal("apron-band",
                             [fc.P(0.0, L - 90.0), fc.P(APRON_HALF, L - 90.0)], kind="marking")]
    return fc.Piece(
        "apron",
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, L))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, L), fc.P(APRON_HALF, L))]),
            fc.Edge("side", [fc.Line(fc.P(APRON_HALF, L), fc.P(APRON_HALF, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(APRON_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "centre")],
        grainline=fc.Grainline(fc.P(APRON_HALF * 0.5, 70.0), fc.P(APRON_HALF * 0.5, L - 100.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label="Apron",
    )


def build():
    pattern = fc.PatternSet("dirndl")
    all_pieces = target_piece == "set"
    bodice_front = build_bodice("bodice_front", 70.0, "Bodice Front")
    bodice_back = build_bodice("bodice_back", 30.0, "Bodice Back")
    if all_pieces or target_piece == "bodice":
        pattern.add(bodice_front)
        pattern.add(bodice_back)
    if all_pieces or target_piece == "skirt":
        pattern.add(build_skirt())
    if all_pieces or target_piece == "apron":
        pattern.add(build_apron())
    if all_pieces:
        pattern.declare_seam(("bodice_front", "shoulder"), ("bodice_back", "shoulder"), tol=1.0)
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "cotton, linen, or wool-blend dress fabric",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 72% marker; bodice + gathered skirt + apron."},
        {"item": "apron fabric (contrast)", "qty": 1, "unit": "as chosen",
         "note": "traditionally a contrasting cotton; the apron is a separate tied panel."},
        {"item": "front lacing or hooks", "qty": 1, "unit": "set",
         "note": "the bodice closes with lacing, hooks, or buttons — maker's choice."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "seams + gathering."},
    ]
    pattern.metadata = {
        "fc200_rank": 154,
        "family": "heritage_global",
        "fabric_hint": "algodon-lino",
        "heritage_note": "The dirndl is part of living Alpine (Bavarian/Austrian) dress. "
            "This cartridge drafts the GARMENT GEOMETRY only — the regional trims, apron "
            "prints, bodice lacing styles, and the meaning carried by how the apron bow is "
            "tied are the maker's and are not reproduced here. Offered with respect.",
        "construction": "fitted bodice waist-seamed to a gathered skirt, with a separate "
            "gathered apron tied over it; fullness from the gather ratio, not shaped seams.",
        "solved": {"skirt_full_width_mm": round(SKIRT_W, 1),
                   "apron_full_width_mm": round(APRON_HALF * 2.0, 1),
                   "gather_ratio": gather_ratio, "waist_girth_mm": round(waist_girth, 1)},
    }
    return pattern


result = build()
