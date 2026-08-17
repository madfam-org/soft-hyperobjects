"""
Maxi Dress — FC-100 rank #24. Fashion Cabinet Garment Cartridge.

Empire-line strappy maxi in woven fabric. A camisole-lineage BODICE (front and
back cut on fold, bound top edges with zero allowance, two separate spaghetti
strap strips) ends at the underbust, where gathered rectangular SKIRT panels
(the maxi-skirt lineage) join at the EMPIRE SEAM. The gathered surplus is a
computed parameter: each skirt half-panel is (hip + ease) / 4 × gather_ratio
wide, so the declared empire seam carries ease = skirt waists − bodice hems,
derived from the same width formulas — delta is 0 by construction. A
soft-elastic channel is marked internal on the skirt panels just below the
seam, and the top binding strip is derived from the measured top openings
times a stretch ratio.

Sandbox contract (apps/api/services/engine/fc_runner.py):
  - `fc` and `math` are pre-injected globals.
  - Manifest parameters are injected as BARE globals.
  - Access them via PARAM(lambda: <name>, <default>). No globals()/eval/getattr.
  - Assign the final fc.PatternSet to a top-level name `result`.
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
_KNOWN = ("bodice_front", "bodice_back", "skirt_front", "skirt_back",
          "straps", "binding", "set")
target_piece = str(PARAM(lambda: target_piece, "set"))

bust_girth     = float(PARAM(lambda: bust_girth, 900.0))
hip_girth      = float(PARAM(lambda: hip_girth, 960.0))
bodice_length  = float(PARAM(lambda: bodice_length, 260.0))  # strap point to empire seam
skirt_length   = float(PARAM(lambda: skirt_length, 900.0))   # empire seam to hem
gather_ratio   = float(PARAM(lambda: gather_ratio, 1.5))     # skirt panel / body quarter
dress_ease     = float(PARAM(lambda: dress_ease, 60.0))      # total ease at bust and hip
strap_length   = float(PARAM(lambda: strap_length, 400.0))   # cut length per strap
binding_ratio  = float(PARAM(lambda: binding_ratio, 0.92))
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 35.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth = max(600.0, min(bust_girth, 1700.0))
hip_girth = max(600.0, min(hip_girth, 1700.0))
bodice_length = max(200.0, min(bodice_length, 360.0))
skirt_length = max(600.0, min(skirt_length, 1300.0))
gather_ratio = max(1.2, min(gather_ratio, 2.0))
dress_ease = max(0.0, min(dress_ease, 200.0))
strap_length = max(250.0, min(strap_length, 650.0))
binding_ratio = max(0.75, min(binding_ratio, 1.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

FRONT_DROP = 90.0    # CF neckline below the strap point
BACK_DROP = 35.0     # CB edge below the strap point
STRAP_CUT_W = 24.0   # strap strip folds into 8 mm spaghetti
BINDING_W = 10.0     # finished binding height; the strip is cut 2x tall
CHANNEL_DROP = 14.0  # elastic-channel stitching below the empire stitch line

BW = (bust_girth + dress_ease) / 4.0                     # bodice half-width
SK_HALF = (hip_girth + dress_ease) / 4.0 * gather_ratio  # skirt half-panel width
SK_HALF = max(SK_HALF, BW)      # a gathered waist is never narrower than its bodice
SURPLUS = 2.0 * (SK_HALF - BW)  # gathered surplus across the empire seam (front+back)

TOP_Y = bodice_length                        # empire seam sits at bodice y = 0
AH = (bust_girth + dress_ease) / 16.0 + 55.0  # shallow camisole armhole
AH = max(80.0, min(AH, bodice_length - 100.0))
STRAP_PT = fc.P(max(40.0, BW * 0.5), TOP_Y)  # strap attachment point
UNDERARM = fc.P(BW, TOP_Y - AH)              # side seam top


def _bodice(name, drop, bulge, label):
    """Camisole-lineage bodice half: fold-cut, bound top, ends at the empire seam."""
    top_start = fc.P(0.0, TOP_Y - drop)
    origin = fc.P(0.0, 0.0)
    edges = [
        fc.Edge("center", [fc.Line(origin, top_start)]),
        fc.Edge("top", [fc.curve_through(top_start, STRAP_PT, bulge=bulge, side=-1.0)]),
        fc.Edge("armhole", [fc.curve_through(STRAP_PT, UNDERARM, bulge=0.16, side=-1.0)]),
        fc.Edge("side", [fc.Line(UNDERARM, fc.P(BW, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(BW, 0.0), origin)]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"top": 0.0},  # bound top edge; the hem IS the empire seam, keeps sa
        notches=[fc.Notch("top", 1.0, "strap"), fc.Notch("side", 0.5),
                 fc.Notch("hem", 0.5, "empire quarter")],
        grainline=fc.Grainline(fc.P(BW * 0.5, 25.0), fc.P(BW * 0.5, UNDERARM.y - 30.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _skirt(name, label):
    """Rectangular gathered panel (maxi-skirt lineage), center line on the fold."""
    w, ln = SK_HALF, skirt_length
    edges = [
        fc.Edge("hem", [fc.Line(fc.P(0.0, 0.0), fc.P(w, 0.0))]),
        fc.Edge("side", [fc.Line(fc.P(w, 0.0), fc.P(w, ln))]),
        fc.Edge("waist", [fc.Line(fc.P(w, ln), fc.P(0.0, ln))]),
        fc.Edge("center", [fc.Line(fc.P(0.0, ln), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("waist", 0.5, "empire quarter"), fc.Notch("side", 0.5)],
        grainline=fc.Grainline(fc.P(w * 0.5, ln * 0.1), fc.P(w * 0.5, ln * 0.9)),
        internals=[fc.Internal("elastic channel",
                               [fc.P(0.0, ln - CHANNEL_DROP), fc.P(w, ln - CHANNEL_DROP)])],
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def _strip(name, length, height, label, quantity):
    """A straight-grain strip cut net (allowances already folded into `length`)."""
    edges = [
        fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
        fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, height))]),
        fc.Edge("top", [fc.Line(fc.P(length, height), fc.P(0.0, height))]),
        fc.Edge("end_a", [fc.Line(fc.P(0.0, height), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,
        grainline=fc.Grainline(fc.P(length * 0.2, height / 2.0),
                               fc.P(length * 0.8, height / 2.0)),
        cut=fc.CutSpec(quantity=quantity),
        label=label,
    )


def build():
    pattern = fc.PatternSet("maxi-dress")
    b_front = _bodice("bodice_front", FRONT_DROP, 0.06, "Bodice Front")
    b_back = _bodice("bodice_back", BACK_DROP, 0.03, "Bodice Back")
    known = target_piece in _KNOWN
    add_bf = not known or target_piece in ("bodice_front", "set")
    add_bb = not known or target_piece in ("bodice_back", "set")
    add_sf = not known or target_piece in ("skirt_front", "set")
    add_sb = not known or target_piece in ("skirt_back", "set")
    add_straps = not known or target_piece in ("straps", "set")
    add_binding = not known or target_piece in ("binding", "set")
    if add_bf:
        pattern.add(b_front)
    if add_bb:
        pattern.add(b_back)
    if add_sf:
        pattern.add(_skirt("skirt_front", "Skirt Front (gathered)"))
    if add_sb:
        pattern.add(_skirt("skirt_back", "Skirt Back (gathered)"))
    if add_straps:
        pattern.add(_strip("strap", strap_length, STRAP_CUT_W, "Strap (8 mm spaghetti)", 2))
    if add_binding:
        # Fold-cut halves → the garment openings are twice the drafted edges.
        top_opening = 2.0 * (b_front.edge("top").length() + b_back.edge("top").length())
        binding_len = top_opening * binding_ratio + 2.0 * seam_allowance
        pattern.add(_strip("top_binding", binding_len, 2.0 * BINDING_W, "Top Binding", 1))
    if add_bf and add_bb:
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.5)
    if add_sf and add_sb:
        pattern.declare_seam(("skirt_front", "side"), ("skirt_back", "side"), tol=1.5)
    if add_bf and add_bb and add_sf and add_sb:
        # Empire seam: the gathered skirt waists sew to the bodice hems; the
        # computed surplus is declared as intentional ease, so delta is 0 by
        # construction and any drift in either lineage breaks the render.
        pattern.declare_seam(
            [("skirt_front", "waist"), ("skirt_back", "waist")],
            [("bodice_front", "hem"), ("bodice_back", "hem")],
            ease=SURPLUS, tol=2.5,
        )
        pattern.bom.append({
            "item": "soft elastic (empire channel)",
            "qty": round(max(bust_girth - 60.0, 400.0) + 20.0),
            "unit": "mm",
            "note": "approx underbust (bust - 60) + 20 mm join overlap; threaded "
                    "through the marked channel under the empire seam",
        })
    pattern.metadata = {
        "fc100_rank": 24,
        "fabric_hint": "popelina-algodon",
        "empire_surplus_mm": round(SURPLUS, 1),
        "drafting": "camisole-lineage bodice joins gathered maxi-skirt panels at the "
                    "empire seam; the seam ease is computed from the same width formulas",
    }
    return pattern


result = build()
