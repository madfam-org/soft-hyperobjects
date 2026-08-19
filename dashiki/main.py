"""
Dashiki — Fashion Cabinet Garment Cartridge (FC-200 rank #141, West African heritage).

The dashiki is the widely-worn West African pullover tunic: a loose rectangular-cut top
with a distinctive V-neck (often faced with an embroidered panel), short or elbow sleeves
grown from the body, and an ornate woven or printed border. Its construction is close to
rectangular — the elegance is the bold neck facing and the border print, which the maker
supplies.

This cartridge drafts the garment geometry: front + back rectangular panels with a
faced V-neck (deeper in front), grown-on cap sleeves, and marked neck-facing + hem-border
zones. Offered with respect for the living tradition; the maker supplies the cloth and
embroidery.

Pieces:
  - front : one panel cut on fold at CF, faced V-neck (deep), grown-on cap sleeve.
  - back  : one panel cut on fold at CB, shallow neck, grown-on cap sleeve.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|set

chest_girth   = float(PARAM(lambda: chest_girth, 1080.0))   # full chest
dashiki_length = float(PARAM(lambda: dashiki_length, 800.0))  # shoulder to hem
neck_v_depth  = float(PARAM(lambda: neck_v_depth, 180.0))   # front V-neck depth
neck_width    = float(PARAM(lambda: neck_width, 200.0))     # neck opening across
sleeve_grown  = float(PARAM(lambda: sleeve_grown, 180.0))   # grown-on cap sleeve extension
body_ease     = float(PARAM(lambda: body_ease, 220.0))      # loose fit ease
facing_depth  = float(PARAM(lambda: facing_depth, 200.0))   # marked V-neck facing panel depth
border_depth  = float(PARAM(lambda: border_depth, 120.0))   # marked hem/sleeve border depth
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 25.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth    = max(700.0, min(chest_girth, 1600.0))
dashiki_length = max(500.0, min(dashiki_length, 1200.0))
neck_v_depth   = max(40.0, min(neck_v_depth, 320.0))
neck_width     = max(120.0, min(neck_width, 340.0))
sleeve_grown   = max(80.0, min(sleeve_grown, 320.0))
body_ease      = max(120.0, min(body_ease, 460.0))
facing_depth   = max(0.0, min(facing_depth, 300.0))
border_depth   = max(0.0, min(border_depth, 250.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = dashiki_length
HALF = (chest_girth + body_ease) / 2.0 / 2.0     # half-width per panel (cut on fold)
SHOULDER_X = HALF                                  # body half-width at the shoulder
SLEEVE_X = HALF + sleeve_grown                     # grown-on cap sleeve extends past body
NECK_HALF = neck_width / 2.0
SLEEVE_DROP = 240.0                                # where the grown sleeve meets the side


def _panel(name, v_depth, label):
    """A rectangular body panel with a grown-on cap sleeve. Top edge: neck scoop (V of
    depth v_depth) from CF/CB out to the shoulder-neck point, then a straight shoulder to
    the grown sleeve tip; the sleeve underside steps back down to the side seam."""
    top_y = L
    neck_pt = fc.P(0.0, top_y - v_depth)
    neck_out = fc.P(NECK_HALF, top_y)
    sleeve_tip_top = fc.P(SLEEVE_X, top_y)
    sleeve_tip_bot = fc.P(SLEEVE_X, top_y - 120.0)         # cap-sleeve opening height
    body_side_top = fc.P(SHOULDER_X, top_y - SLEEVE_DROP)  # where sleeve underside meets body
    internals = []
    if facing_depth > 0.0 and name == "front":
        internals.append(fc.Internal("neck-facing",
                                     [fc.P(0.0, top_y - v_depth - facing_depth),
                                      fc.P(NECK_HALF, top_y)], kind="marking"))
    if border_depth > 0.0:
        internals.append(fc.Internal("hem-border",
                                     [fc.P(0.0, border_depth), fc.P(SLEEVE_X, border_depth)],
                                     kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_pt)]),
            fc.Edge("neck", [fc.Line(neck_pt, neck_out)]),   # straight V limb (facing covers)
            fc.Edge("shoulder", [fc.Line(neck_out, sleeve_tip_top)]),
            fc.Edge("sleeve_end", [fc.Line(sleeve_tip_top, sleeve_tip_bot)]),
            fc.Edge("sleeve_under", [fc.Line(sleeve_tip_bot, body_side_top)]),
            fc.Edge("side", [fc.Line(body_side_top, fc.P(SHOULDER_X, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(SHOULDER_X, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("shoulder", 0.0, "shoulder-neck"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.5, 80.0), fc.P(HALF * 0.5, L - 120.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("dashiki")
    front = _panel("front", neck_v_depth, "Front Panel")
    back = _panel("back", neck_v_depth * 0.28, "Back Panel")

    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(front)
    if all_pieces or target_piece == "back":
        pattern.add(back)

    if all_pieces:
        # Front and back are identical rectangles apart from neck depth, so the shoulder,
        # sleeve, and side seams all balance by construction.
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)
        pattern.declare_seam(("front", "sleeve_under"), ("back", "sleeve_under"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "printed / woven cotton (often wax-print or brocade)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 70% marker; the border print and neck facing are "
                 "positioned by the maker to frame the neck and hem."},
        {"item": "neck-facing panel", "qty": 1, "unit": "pc",
         "note": "the embroidered V-neck facing — the dashiki's signature — is the maker's."},
        {"item": "all-purpose thread", "qty": 1, "unit": "spool", "note": "straight seams."},
    ]
    pattern.metadata = {
        "fc200_rank": 141,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "heritage_note": "The dashiki is a living West African garment, widely worn across "
            "the diaspora. This cartridge drafts the GARMENT GEOMETRY only — the wax-print "
            "or brocade cloth and the embroidered V-neck facing that carry its identity are "
            "the maker's to supply and are not reproduced here. Offered with respect.",
        "near_rectangular": "Front and back are near-identical panels with grown-on cap "
            "sleeves; the signature is the faced V-neck and the framed border print, both "
            "marked here for the maker.",
        "drafting": "faced V-neck (deep front, shallow back); grown-on cap sleeves; "
            "straight shoulder/sleeve/side seams balanced by construction; facing + border "
            "zones marked.",
    }
    return pattern


result = build()
