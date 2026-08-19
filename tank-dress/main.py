"""
Tank Dress — Fashion Cabinet Garment Cartridge (FC-200 #173, dress silhouette gap).

The sleeveless knit column dress: a tank bodice (wide shoulder straps, scooped neck, deep
armholes) extended straight to dress length in a soft knit — the everyday pull-on dress. Front
and back share the body width so the shoulder and side seams balance by construction; the
gentle A-line release at the hem is built into both side seams equally.

Pieces:
  - front / back : one-piece tank-to-hem panels (cut on fold), scoop neck + armholes.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # front|back|set

chest_girth  = float(PARAM(lambda: chest_girth, 940.0))
hip_girth    = float(PARAM(lambda: hip_girth, 1000.0))
dress_length = float(PARAM(lambda: dress_length, 980.0))   # shoulder to hem
neck_width   = float(PARAM(lambda: neck_width, 200.0))     # tank neck width
strap_width  = float(PARAM(lambda: strap_width, 70.0))     # shoulder strap width
armhole_drop = float(PARAM(lambda: armhole_drop, 240.0))   # deep tank armhole
a_line       = float(PARAM(lambda: a_line, 60.0))          # extra hem width per side (flare)
ease         = float(PARAM(lambda: ease, 120.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance  = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(640.0, min(chest_girth, 1500.0))
hip_girth    = max(700.0, min(hip_girth, 1600.0))
dress_length = max(700.0, min(dress_length, 1400.0))
neck_width   = max(150.0, min(neck_width, 360.0))
strap_width  = max(30.0, min(strap_width, 140.0))
armhole_drop = max(160.0, min(armhole_drop, 360.0))
a_line       = max(0.0, min(a_line, 220.0))
ease         = max(40.0, min(ease, 360.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance  = max(0.0, min(hem_allowance, 60.0))

L = dress_length
CHEST_HALF = (chest_girth + ease) / 4.0
HIP_HALF   = (hip_girth + ease) / 4.0
HEM_HALF   = HIP_HALF + a_line
NECK_HALF  = neck_width / 2.0
STRAP_OUT  = NECK_HALF + strap_width


def _panel(name, neck_dip, label):
    top_y = L
    neck_in = fc.P(0.0, top_y - neck_dip)
    strap_in = fc.P(NECK_HALF, top_y)
    strap_out = fc.P(STRAP_OUT, top_y)
    armhole_bot = fc.P(CHEST_HALF, top_y - armhole_drop)
    # side seam: chest -> hip -> hem with A-line release, as a polyline
    side_pts = [armhole_bot, fc.P(HIP_HALF, L * 0.32), fc.P(HEM_HALF, 0.0)]
    side_edge = fc.Edge("side", [fc.Line(side_pts[i], side_pts[i + 1]) for i in range(2)])
    return fc.Piece(
        name,
        [
            fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_in)]),
            fc.Edge("neck", [fc.curve_through(neck_in, strap_in, bulge=0.22, side=-1.0)]),
            fc.Edge("strap", [fc.Line(strap_in, strap_out)]),
            fc.Edge("armhole", [fc.curve_through(strap_out, armhole_bot, bulge=0.26, side=-1.0)]),
            side_edge,
            fc.Edge("hem", [fc.Line(fc.P(HEM_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("strap", 0.5, "shoulder"), fc.Notch("side", 0.0, "underarm")],
        grainline=fc.Grainline(fc.P(CHEST_HALF * 0.5, 80.0), fc.P(CHEST_HALF * 0.5, L - 120.0)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("tank-dress")
    everything = target_piece == "set"
    front = _panel("front", 90.0, "Front")
    back = _panel("back", 45.0, "Back")
    if everything or target_piece == "front":
        pattern.add(front)
    if everything or target_piece == "back":
        pattern.add(back)
    if everything:
        pattern.declare_seam(("front", "strap"), ("back", "strap"), tol=1.0)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.76)
    pattern.bom = [
        {"item": "soft jersey or modal knit",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 76% marker; a fluid knit drapes the column."},
        {"item": "neck + armhole binding", "qty": 1, "unit": "set",
         "note": "self-fabric or fold-over-elastic binds the scoop neck and armholes."},
        {"item": "ballpoint / stretch thread", "qty": 1, "unit": "spool",
         "note": "knit seams; twin-needle or coverstitch the hem."},
    ]
    pattern.metadata = {
        "fc200_rank": 173, "family": "dresses_jumpsuits", "fabric_hint": "jersey-modal",
        "silhouette_note": "A sleeveless tank bodice extended straight to dress length in a soft "
            "knit, with a gentle A-line release built equally into both side seams so they "
            "balance. The everyday pull-on knit dress.",
        "solved": {"chest_q_mm": round(CHEST_HALF, 1), "hem_half_mm": round(HEM_HALF, 1)},
    }
    return pattern


result = build()
