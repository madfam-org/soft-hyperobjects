"""
Structured Corset — Fashion Cabinet Garment Cartridge (FC-200 #196; y4d corset-busk).

A structured, boned corset drafted as a ring of shaped panels that curve in at the waist and out
over bust and hip, with boning channels marked at each seam and a front busk closure. The BUSK
(the rigid steel front-opening hardware) is Yantra4D territory (`corset-busk`; see the manifest's
notion.hardware_ref) — Fashion Cabinet owns the fabric panels and the busk placement. The corset's
centre-front length drives the busk length (dimensional handshake), so the printed busk fits the
drafted panel.

This is a foundation garment; it uses several shaped panels whose vertical seams balance in pairs
by construction (each panel's right seam equals the next panel's left seam, all cut to the same
panel height).

Pieces:
  - cf_panel / side_panel / back_panel : shaped corset panels (cut in mirrored pairs).

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # cf_panel|side_panel|back_panel|set

bust_girth   = float(PARAM(lambda: bust_girth, 920.0))
waist_girth  = float(PARAM(lambda: waist_girth, 680.0))    # corset waist (reduced)
hip_girth    = float(PARAM(lambda: hip_girth, 960.0))
corset_len   = float(PARAM(lambda: corset_len, 340.0))     # CF length (== busk length)
waist_pos    = float(PARAM(lambda: waist_pos, 180.0))      # top edge to waist on the panel
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
bust_girth   = max(680.0, min(bust_girth, 1400.0))
waist_girth  = max(500.0, min(waist_girth, 1200.0))
hip_girth    = max(720.0, min(hip_girth, 1500.0))
corset_len   = max(220.0, min(corset_len, 480.0))
waist_pos    = max(120.0, min(waist_pos, 300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

L = corset_len
WY = L - waist_pos                                     # waist line height (from bottom)
# six panels around the half-body (CF, side, back per side). Each panel gets 1/6 of each girth.
BUST_6 = bust_girth / 6.0 / 2.0                        # half-panel bust contribution
WAIST_6 = waist_girth / 6.0 / 2.0
HIP_6 = hip_girth / 6.0 / 2.0


def _panel(name, bust_w, waist_w, hip_w, is_cf, is_back, label):
    # a shaped panel: top edge = bust_w, waist (nipped) = waist_w, bottom = hip_w. Both vertical
    # seam edges follow the SAME shape so paired seams balance (right of one == left of next).
    internals = []
    if is_cf:
        internals.append(fc.Internal("busk-line", [fc.P(0.0, 0.0), fc.P(0.0, L)], kind="marking"))
    internals.append(fc.Internal("bone-channel-l",
                                 [fc.P(-waist_w + 6.0, 0.0), fc.P(-bust_w + 6.0, L)],
                                 kind="marking"))
    internals.append(fc.Internal("bone-channel-r",
                                 [fc.P(waist_w - 6.0, 0.0), fc.P(bust_w - 6.0, L)], kind="marking"))
    return fc.Piece(
        name,
        [
            fc.Edge("seam_l", [fc.Line(fc.P(-bust_w, L), fc.P(-waist_w, WY)),
                               fc.Line(fc.P(-waist_w, WY), fc.P(-hip_w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(-hip_w, 0.0), fc.P(hip_w, 0.0))]),
            fc.Edge("seam_r", [fc.Line(fc.P(hip_w, 0.0), fc.P(waist_w, WY)),
                               fc.Line(fc.P(waist_w, WY), fc.P(bust_w, L))]),
            fc.Edge("top", [fc.Line(fc.P(bust_w, L), fc.P(-bust_w, L))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"bottom": 12.0, "top": 12.0},
        notches=[fc.Notch("seam_r", 0.5, "waist"), fc.Notch("seam_l", 0.5, "waist")],
        grainline=fc.Grainline(fc.P(0.0, 20.0), fc.P(0.0, L - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1 if is_cf else 2, mirror=not is_cf),
        label=label,
    )


def build():
    pattern = fc.PatternSet("structured-corset")
    everything = target_piece == "set"
    # all panels share the SAME seam-edge widths (bust/waist/hip per-sixth), so every vertical
    # seam edge is identical and all paired panel seams balance exactly by construction.
    cf = _panel("cf_panel", BUST_6, WAIST_6, HIP_6, True, False, "Centre-front panel (busk)")
    side = _panel("side_panel", BUST_6, WAIST_6, HIP_6, False, False, "Side panel")
    back = _panel("back_panel", BUST_6, WAIST_6, HIP_6, False, True, "Back panel (lacing)")
    if everything or target_piece == "cf_panel":
        pattern.add(cf)
    if everything or target_piece == "side_panel":
        pattern.add(side)
    if everything or target_piece == "back_panel":
        pattern.add(back)
    if everything:
        # panels seam in a ring: cf.seam_r -> side.seam_l, side.seam_r -> back.seam_l. All panels
        # share the same height L and the same waist line, so paired seams balance in length.
        pattern.declare_seam(("cf_panel", "seam_r"), ("side_panel", "seam_l"), tol=1.5)
        pattern.declare_seam(("side_panel", "seam_r"), ("back_panel", "seam_l"), tol=1.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    pattern.bom = [
        {"item": "coutil or heavy cotton twill (+ lining)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 68% marker; a firm, stable foundation fabric, fully lined."},
        {"item": "spiral + flat steel bones", "qty": 1, "unit": "set",
         "note": "boning in the marked channels at every seam and the busk line."},
        {"item": "front busk (Yantra4D corset-busk)", "qty": 1, "unit": "set",
         "note": "the rigid front-opening busk is the Yantra4D solid (see notion.hardware_ref); "
                 "its length is driven by the corset's CF length."},
        {"item": "back lacing + grommets", "qty": 1, "unit": "set",
         "note": "the back closes with laced grommets for adjustable reduction."},
        {"item": "topstitch + all-purpose thread", "qty": 1, "unit": "set",
         "note": "bone channels are topstitched; seams are flat-felled or bound."},
    ]
    pattern.metadata = {
        "fc200_rank": 196, "family": "underwear_lounge", "fabric_hint": "coutil-algodon",
        "silhouette_note": "A boned foundation corset as a ring of shaped panels nipping the "
            "waist, boning channels marked at each seam, a front busk closure and back lacing. "
            "Paired vertical seams balance by construction (same panel height + waist line).",
        "hardware": "front busk via Yantra4D (notion.hardware_ref -> corset-busk); CF length "
            "drives busk_len (dimensional handshake).",
        "solved": {"bust_6_mm": round(BUST_6, 1), "waist_6_mm": round(WAIST_6, 1),
                   "hip_6_mm": round(HIP_6, 1), "cf_length_mm": round(L, 1)},
    }
    return pattern


result = build()
