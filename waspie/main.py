"""
Waspie — Fashion Cabinet Garment Cartridge (FC-300 #223; y4d boning-stay).

A waspie is a SHORT corset: a waist cincher that spans roughly from the lower ribs to
the upper hip and does one job — nip the waist — without the bust engineering of a full
corset or the length of a longline. Being short changes two things structurally:

  1. IT MUST BE MORE STRONGLY BONED PER MILLIMETRE. A short garment has less area to
     spread the compression over, so it wants a bone at every seam — six panels around
     the half-body means six seams and six channels — or it rolls at the top and bottom
     edges instead of holding the waist.
  2. IT CAN SKIP THE BUSK. A full corset opens on a rigid steel busk because it is long
     enough that hooks alone would gap between them. A waspie is short enough to close
     on a HOOK-AND-EYE front instead — which is also why this cartridge does not
     reference `corset-busk` (see `structured-corset` for that lineage). The front
     closure is a point/slot notion: hooks and eyes have no sewn flange, so they need
     no edge coupling.

Drafting. Six shaped panels per half-body, each nipped at the waist: top edge carries a
share of the underbust ring, the waist line a share of the (reduced) waist ring, and the
bottom edge a share of the high-hip ring. Every panel shares the SAME per-panel
increments, so all paired vertical seams are congruent and balance by construction —
the lesson the garter-belt's verifier taught this lane.

The DIMENSIONAL HANDSHAKE (`boning-stay`). As in `longline-bra`, the stay length is
derived, never guessed:

    channel_len = waspie_len - 2 * bone_clearance

`waspie_len` also drives the garment's own `boning_channels` and `panel_seams`
interfaces, so the same dimension reaches the printed stay and the drafted channel —
a coupled handshake, which is what `hardware_dimensional_rules` requires. The channel
internals are marked at that literal solved length.

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

underbust_girth = float(PARAM(lambda: underbust_girth, 780.0))
waist_girth   = float(PARAM(lambda: waist_girth, 720.0))   # natural waist
hip_girth     = float(PARAM(lambda: hip_girth, 960.0))
waist_reduction = float(PARAM(lambda: waist_reduction, 50.0))  # mm taken out at waist
waspie_len    = float(PARAM(lambda: waspie_len, 200.0))    # top edge -> bottom edge
waist_pos     = float(PARAM(lambda: waist_pos, 105.0))     # top edge -> waist line
bone_clearance = float(PARAM(lambda: bone_clearance, 10.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1300.0))
waist_girth   = max(500.0, min(waist_girth, 1400.0))
hip_girth     = max(600.0, min(hip_girth, 1700.0))
waist_reduction = max(0.0, min(waist_reduction, 150.0))
waspie_len    = max(110.0, min(waspie_len, 320.0))
waist_pos     = max(45.0, min(waist_pos, 240.0))
bone_clearance = max(3.0, min(bone_clearance, 25.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# keep the waist line inside the panel with room for the curve either side
waist_pos = max(30.0, min(waist_pos, waspie_len - 30.0))

L = waspie_len
WY = L - waist_pos                       # waist line height measured from the bottom

# ── THE BONING SOLVER ────────────────────────────────────────────────────────
# A short garment is boned hard; every seam gets a stay, and the stay must clear both
# edges so its tips cannot work through. This is the number the hardware receives.
CHANNEL_LEN = max(20.0, L - 2.0 * bone_clearance)

# ── Ring shares ──────────────────────────────────────────────────────────────
# Six panels around the HALF body (cf, side-front, side, side-back, back, plus the
# mirror supplies the rest). Each panel carries an equal share of each ring, so every
# vertical seam edge is congruent — paired seams balance to the micron.
PANELS_PER_HALF = 3                      # cf, side, back (each cut as a mirrored pair)
RING_DIV = PANELS_PER_HALF * 2.0         # six panels close the full body ring
# Each panel is drafted symmetric about x=0, so these are HALF-widths: the panel's
# full width is 2x, and 6 panels x (2x) sums back to the ring.
TOP_W = underbust_girth / RING_DIV / 2.0
WAIST_W = (waist_girth - waist_reduction) / RING_DIV / 2.0
BOT_W = hip_girth / RING_DIV / 2.0


def _bone_channel(label, x):
    """A boning channel internal drawn at the SOLVED stay length.

    Marked from `bone_clearance` upward for exactly CHANNEL_LEN mm — the same number
    the manifest maps to the hardware's `stay_length`.
    """
    return fc.Internal(label, [fc.P(x, bone_clearance),
                               fc.P(x, bone_clearance + CHANNEL_LEN)], kind="marking")


def _panel(name, is_cf, label):
    """One shaped waspie panel, nipped at the waist.

    All panels share the same top/waist/bottom half-widths, so `seam_l` of one panel is
    congruent with `seam_r` of its neighbour and every paired seam balances exactly.
    Both vertical seams carry a boning channel; the CF panel also carries the hook line.
    """
    edges = [
        fc.Edge("seam_l", [fc.Line(fc.P(-TOP_W, L), fc.P(-WAIST_W, WY)),
                           fc.Line(fc.P(-WAIST_W, WY), fc.P(-BOT_W, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(-BOT_W, 0.0), fc.P(BOT_W, 0.0))]),
        fc.Edge("seam_r", [fc.Line(fc.P(BOT_W, 0.0), fc.P(WAIST_W, WY)),
                           fc.Line(fc.P(WAIST_W, WY), fc.P(TOP_W, L))]),
        fc.Edge("top", [fc.Line(fc.P(TOP_W, L), fc.P(-TOP_W, L))]),
    ]
    internals = [
        _bone_channel("bone channel — left seam", -WAIST_W + 7.0),
        _bone_channel("bone channel — right seam", WAIST_W - 7.0),
    ]
    if is_cf:
        # The hook-and-eye front: a marked closure line at the centre front. No busk —
        # a waspie is short enough to close on hooks alone.
        internals.append(fc.Internal("hook-and-eye front line",
                                     [fc.P(0.0, bone_clearance),
                                      fc.P(0.0, L - bone_clearance)], kind="marking"))
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"top": 12.0, "bottom": 12.0},
        notches=[fc.Notch("seam_r", 0.5, "waist line"),
                 fc.Notch("seam_l", 0.5, "waist line")],
        grainline=fc.Grainline(fc.P(0.0, 15.0), fc.P(0.0, L - 15.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label=label,
    )


def build():
    pattern = fc.PatternSet("waspie")
    cf = _panel("cf_panel", True, "Centre-front panel (hook-and-eye front, boned)")
    side = _panel("side_panel", False, "Side panel (boned)")
    back = _panel("back_panel", False, "Back panel (lacing, boned)")

    picked = {"cf_panel": cf, "side_panel": side, "back_panel": back}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (cf, side, back):
            pattern.add(piece)
        # The panel ring: cf -> side -> back. All panels share the same three widths
        # and the same waist line, so paired seams balance by construction.
        pattern.declare_seam(("cf_panel", "seam_r"), ("side_panel", "seam_l"), tol=1.0)
        pattern.declare_seam(("side_panel", "seam_r"), ("back_panel", "seam_l"), tol=1.0)

    # Measured rings. Each panel is drafted symmetric about x=0, so its top edge spans
    # the panel's FULL width (2 * TOP_W); six such panels close the body.
    top_ring = 6.0 * cf.edge("top").length()
    bottom_ring = 6.0 * cf.edge("bottom").length()
    waist_ring = waist_girth - waist_reduction
    # bones: two channels per panel, three panel types each cut as a mirrored pair
    bone_count = 2 * 2 + 2 * 2 + 2 * 2

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "coutil or firm cotton twill (+ lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"panels at {fabric_width:.0f} mm width, 68% marker; fully lined in "
                 "coutil. A waspie compresses hard over a short span — the cloth must "
                 "be stable, never stretch."},
        {"item": "boning stays (Yantra4D boning-stay)", "qty": bone_count, "unit": "piece",
         "note": f"stay_length {CHANNEL_LEN:.1f} mm = waspie_len {L:.0f} mm minus 2 x "
                 f"{bone_clearance:.0f} mm clearance. A short corset is boned at EVERY "
                 "seam — less area to spread the compression, so it rolls at the edges "
                 "without them. The stay and its channel are the Yantra4D solid "
                 "(notion.hardware_ref -> boning-stay), never modelled here."},
        {"item": "hook-and-eye front closure (busk-free)", "qty": 1, "unit": "set",
         "note": "a waspie is short enough to close on hooks alone — no rigid busk "
                 "(contrast structured-corset, which needs one). Set along the marked "
                 "centre-front line; Yantra4D hook-and-eye, point/slot, no sewn flange."},
        {"item": "back lacing + grommets", "qty": 1, "unit": "set",
         "note": "the back laces for adjustable reduction; grommets set between the "
                 "centre-back bones."},
        {"item": "waist tape 25 mm", "qty": round(waist_ring * 1.05), "unit": "mm_length",
         "note": f"a non-stretch stay tape at the marked waist line, cut to the reduced "
                 f"waist {waist_ring:.0f} mm; this is what actually holds the reduction "
                 "and stops the panel seams stretching out over time."},
        {"item": "bias binding 25 mm", "qty": round((top_ring + bottom_ring) * 1.08),
         "unit": "mm_length",
         "note": f"top {top_ring:.0f} mm + bottom {bottom_ring:.0f} mm edges bound."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "bone channels topstitched both sides before the panels join."},
    ]
    pattern.metadata = {
        "fc300_rank": 223, "family": "underwear_lounge", "fabric_hint": "coutil-algodon",
        "silhouette_note": "A short 6-panel waist cincher: ribs to upper hip, nipped at "
            "the waist, boned at every seam, closing on hooks at the front and lacing "
            "at the back. Short means MORE boning per millimetre, and short means it "
            "can skip the busk a full corset needs.",
        "hardware": "boning via Yantra4D (notion.hardware_ref -> boning-stay); "
            "stay_length is derived as waspie_len - 2*bone_clearance, and waspie_len "
            "also drives the garment's channel and seam interfaces — the dimensional "
            "handshake. The front hook-and-eye is point/slot (no flange, no coupling).",
        "solver": {
            "waspie_len_mm": round(L, 1),
            "bone_clearance_mm": round(bone_clearance, 1),
            "channel_len_mm": round(CHANNEL_LEN, 2),
            "bone_count": bone_count,
            "note": "channel_len == stay_length: what is chalked is what is printed.",
        },
        "solved": {
            "top_ring_mm": round(top_ring, 1),
            "waist_ring_mm": round(waist_ring, 1),
            "bottom_ring_mm": round(bottom_ring, 1),
            "waist_reduction_mm": round(waist_reduction, 1),
            "waist_line_from_bottom_mm": round(WY, 1),
        },
        "closure": "hook-and-eye centre front (busk-free) + back lacing",
        "drafting": "Made to measure to underbust, waist and hip girths, with an "
            "explicit waist reduction. Six equal panels: every vertical seam congruent.",
    }
    return pattern


result = build()
