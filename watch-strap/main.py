"""
Watch Strap — Fashion Cabinet Accessory Cartridge (Yantra4D-bridged hardware).

A two-piece watch strap sized to the lug width and wrist: the buckle half (lug end →
tapered body → billet with eyelets) and the keeper half (lug end → tapered body →
folded buckle tab, plus a floating keeper loop marked on it). The lug adapter and
buckle SOLIDS are Yantra4D territory (`watch-adapter`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the strap geometry — lug width, wrist-sized
split, and taper.

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
lug_width   = float(PARAM(lambda: lug_width, 20.0))
wrist_girth = float(PARAM(lambda: wrist_girth, 180.0))
taper       = float(PARAM(lambda: taper, 4.0))
eyelets     = int(  PARAM(lambda: eyelets, 6))

# ── Clamps ───────────────────────────────────────────────────────────────────
lug_width   = max(12.0, min(lug_width, 26.0))
wrist_girth = max(120.0, min(wrist_girth, 240.0))
taper       = max(0.0, min(taper, 8.0))
eyelets     = max(3, min(eyelets, 9))

# The strap wraps the wrist; the two halves + the watch case span it. Reserve ~50 mm
# for the case + buckle overlap, split the rest ~60/40 (buckle half is longer).
EYELET_PITCH = 8.0
usable       = max(60.0, wrist_girth - 50.0)
buckle_len   = usable * 0.60
keeper_len   = usable * 0.40
W_lug        = lug_width
W_buckle     = max(8.0, lug_width - taper)   # narrowed end


def _tapered_half(name, length, w_end, label, with_eyelets):
    """A strap half from the lug end (x=0, full lug width) tapering to the far end
    (x=length, width w_end). Symmetric about the X axis."""
    y0 = W_lug / 2.0
    y1 = w_end / 2.0
    edges = [
        fc.Edge("lug",   [fc.Line(fc.P(0.0, -y0), fc.P(0.0, y0))]),
        fc.Edge("top",   [fc.Line(fc.P(0.0, y0), fc.P(length, y1))]),
        fc.Edge("far",   [fc.Line(fc.P(length, y1), fc.P(length, -y1))]),
        fc.Edge("bottom", [fc.Line(fc.P(length, -y1), fc.P(0.0, -y0))]),
    ]
    internals = []
    if with_eyelets:
        # Eyelets centered along the last third of the buckle half.
        start = length - (eyelets - 1) * EYELET_PITCH - 12.0
        for i in range(eyelets):
            x = start + i * EYELET_PITCH
            internals.append(fc.Internal(
                "eyelet-h", [fc.P(x - 3.0, 0.0), fc.P(x + 3.0, 0.0)], kind="drill"))
            internals.append(fc.Internal(
                "eyelet-v", [fc.P(x, -3.0), fc.P(x, 3.0)], kind="drill"))
    else:
        # Keeper half: mark the buckle-tab fold + a floating keeper loop position.
        internals.append(fc.Internal(
            "buckle-tab-fold",
            [fc.P(length - 20.0, -y1), fc.P(length - 20.0, y1)], kind="marking"))
        internals.append(fc.Internal(
            "keeper-loop", [fc.P(length * 0.5, -y1), fc.P(length * 0.5, y1)], kind="marking"))
    return fc.Piece(
        name,
        edges,
        seam_allowance=0.0,   # edge-finished strap — cut line == edge
        notches=[fc.Notch("lug", 0.5, "spring bar")],
        grainline=fc.Grainline(fc.P(length * 0.2, 0.0), fc.P(length * 0.8, 0.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label=label,
    )


def build():
    pattern = fc.PatternSet("watch-strap")
    pattern.add(_tapered_half("buckle-half", buckle_len, W_buckle, "Buckle Half", True))
    pattern.add(_tapered_half("keeper-half", keeper_len, W_buckle, "Keeper Half", False))
    pattern.bom = [
        {"item": "strap material (leather or webbing)",
         "qty": round((buckle_len + keeper_len) / 10.0) * 10, "unit": "mm_length",
         "note": f"{W_lug:.0f} mm at the lug"},
        {"item": "spring bars", "qty": 2, "unit": "count", "note": f"{W_lug:.0f} mm lug width"},
        {"item": "buckle", "qty": 1, "unit": "count", "note": "with the Yantra4D watch-adapter"},
        {"item": "eyelets", "qty": eyelets, "unit": "count", "note": "buckle half"},
    ]
    pattern.metadata = {
        "lug_width_mm": round(W_lug, 1),
        "wrist_girth_mm": round(wrist_girth, 1),
        "buckle_half_mm": round(buckle_len, 1),
        "keeper_half_mm": round(keeper_len, 1),
        "hardware": "lug adapter + buckle delegated to Yantra4D "
                    "(notion.hardware_ref -> watch-adapter)",
    }
    return pattern


result = build()
