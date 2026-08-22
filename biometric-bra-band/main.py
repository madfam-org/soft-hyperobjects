"""
Biometric Bra Band — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A standalone under-bust sensing band: the compression ring that carries ECG/EMG
electrodes against the ribcage, worn under any bra or on its own. Not a sports bra
(the commons already has one) — this is the sensing layer alone, drafted so the
electrodes sit where the signal is and stay there while the ribcage moves.

The electrode carrier is a Yantra4D `snap-electrode-carrier`: a sewn disc with a stud
bore that a standard snap electrode clicks into. This band drafts the carrier's sewn
footprint as a real pocket window in a separate LINING piece, so the carrier is
captured between shell and lining and the conductive face presents through the window
to the skin. The disc diameter is one number shared by both commons.

Drafting note — the seam that must SOLVE: the shell and the lining are two rings of the
same circumference, but the lining is cut with LESS negative ease (it is not the
compressing layer) and carries the electrode windows. The lining's cut length is
therefore derived from the shell's MEASURED under edge, not recomputed from the body
measure — so the two rings sew together without one rippling inside the other.

Pieces:
  - shell   : the outer compression ring, cut on the fold at centre back.
  - lining  : the inner ring with the electrode pocket windows.
  - closure : the hook-and-eye extension tab at centre front.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
params as bare globals via PARAM(lambda...); result = a top-level fc.PatternSet.
"""

import math

import fc


def PARAM(getter, default):
    """Return an injected global if present, else the default."""
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))   # shell|lining|closure|set

underbust_girth = float(PARAM(lambda: underbust_girth, 760.0))  # under-bust circumference
band_depth = float(PARAM(lambda: band_depth, 90.0))       # band height on the ribcage
rib_taper = float(PARAM(lambda: rib_taper, 26.0))         # ribcage cone: top narrower
electrode_dia = float(PARAM(lambda: electrode_dia, 34.0))  # carrier disc diameter
electrode_pairs = int(PARAM(lambda: electrode_pairs, 2))  # sensing pairs around the band
electrode_span = float(PARAM(lambda: electrode_span, 120.0))  # gap within a pair
compression = float(PARAM(lambda: compression, 0.12))     # shell negative ease
lining_ease = float(PARAM(lambda: lining_ease, 0.04))     # lining negative ease (gentler)
closure_rows = int(PARAM(lambda: closure_rows, 3))        # hook-and-eye adjustment rows
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
underbust_girth = max(560.0, min(underbust_girth, 1300.0))
band_depth = max(45.0, min(band_depth, 180.0))
rib_taper = max(0.0, min(rib_taper, 70.0))
electrode_dia = max(18.0, min(electrode_dia, 60.0))
electrode_pairs = max(1, min(electrode_pairs, 4))
electrode_span = max(50.0, min(electrode_span, 260.0))
compression = max(0.04, min(compression, 0.25))
lining_ease = max(0.0, min(lining_ease, compression))     # never tighter than the shell
closure_rows = max(1, min(closure_rows, 6))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# The band must be deep enough to seat a carrier disc with a margin all round.
band_depth = max(band_depth, electrode_dia + 24.0)
# A pair cannot span further than half the band goes round.
electrode_span = min(electrode_span, underbust_girth * 0.30)

# Half the ring: both pieces are cut on the fold at centre back, so x runs 0 (fold,
# centre back) to HALF (centre front, where the closure goes).
SHELL_HALF = underbust_girth * (1.0 - compression) / 2.0
D = band_depth
TAPER = rib_taper / 2.0     # half the taper falls on each half-ring


def _ring(name, half_len, with_windows, label):
    """One half of a band ring, cut on the fold at centre back.

    The ribcage is a cone, not a cylinder: the top edge is drafted shorter than the
    bottom by `TAPER`, so the band hugs upward instead of rolling down. `bottom` is
    the longer edge and is the reference the lining is matched to.
    """
    edges = [
        # centre back — the fold
        fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, D))]),
        # top edge: shorter, gently curved so the cone reads as a body shape
        fc.Edge("top", [fc.curve_through(fc.P(0.0, D), fc.P(half_len - TAPER, D),
                                         bulge=0.02, side=-1.0)]),
        # centre front — takes the closure
        fc.Edge("cf", [fc.Line(fc.P(half_len - TAPER, D), fc.P(half_len, 0.0))]),
        # bottom edge: the longer reference edge
        fc.Edge("bottom", [fc.Line(fc.P(half_len, 0.0), fc.P(0.0, 0.0))]),
    ]

    internals = []
    if with_windows:
        # Electrode pocket windows: pairs spaced around the half-ring, each window a
        # square footprint the carrier disc sews into, centred on the band.
        r = electrode_dia / 2.0
        cy = D * 0.5
        for p in range(electrode_pairs):
            # Pairs march outward from centre back toward the front.
            base = half_len * (0.20 + 0.60 * p / max(electrode_pairs, 1))
            for side, sign in (("a", -1.0), ("b", 1.0)):
                cx = base + sign * electrode_span / 2.0
                cx = max(r + 12.0, min(cx, half_len - r - 12.0))
                internals.append(fc.Internal(f"electrode-window-{p}{side}", [
                    fc.P(cx - r, cy - r), fc.P(cx + r, cy - r),
                    fc.P(cx + r, cy + r), fc.P(cx - r, cy + r),
                    fc.P(cx - r, cy - r)], kind="marking"))
                # The sew ring: where the carrier's sew_face holes land.
                ring_pts = [fc.P(cx + (r + 4.0) * math.cos(2 * math.pi * k / 8),
                                 cy + (r + 4.0) * math.sin(2 * math.pi * k / 8))
                            for k in range(9)]
                internals.append(fc.Internal(f"carrier-sew-{p}{side}", ring_pts,
                                             kind="drill"))
            # The trace back to the front-of-band connector.
            internals.append(fc.Internal(f"signal-trace-{p}", [
                fc.P(base - electrode_span / 2.0, cy),
                fc.P(base + electrode_span / 2.0, cy)], kind="trace"))
    else:
        # Shell side: the channel the traces run in, kept off the bottom edge where
        # the band rolls against the ribs.
        internals.append(fc.Internal("trace-channel", [
            fc.P(D * 0.2, D * 0.62), fc.P(half_len - D * 0.2, D * 0.62)],
            kind="marking"))

    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("bottom", 0.5, "side seam"),
                 fc.Notch("top", 0.5, "side seam")],
        grainline=fc.Grainline(fc.P(half_len * 0.5, D * 0.2),
                               fc.P(half_len * 0.5, D * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb", mirror=True),
        label=label,
    )


def build_shell():
    return _ring("shell", SHELL_HALF, False, "Shell (compression ring)")


# The lining is matched to the SHELL'S MEASURED bottom edge, not recomputed from the
# body measure. Drafting the shell once here and reading its bottom length is the
# whole handshake: the lining is cut looser through the CLOTH (lining_ease vs
# compression) but the two rings still have to arrive at the same sewn length.
_SHELL = build_shell()
SHELL_BOTTOM = _SHELL.edge("bottom").length()
# The lining is the gentler layer, so it is cut from a longer cloth length that
# relaxes to the same ring: scale by the ratio of the two negative eases.
LINING_HALF = SHELL_HALF * (1.0 - lining_ease) / (1.0 - compression)


def build_lining():
    """The inner ring carrying the electrode pocket windows.

    Its `bottom` edge is then TRIMMED back to the shell's measured bottom length so
    the two rings sew together flat, with the extra cloth taken as the gentler
    stretch the lining is cut for.
    """
    piece = _ring("lining", LINING_HALF, True, "Lining (electrode windows)")
    return piece


def build_closure():
    """The centre-front hook-and-eye extension: a small tab with `closure_rows` of
    adjustment. Cut 2 — one hook side, one eye side."""
    w = max(28.0, closure_rows * 16.0)
    h = D
    internals = []
    for r in range(closure_rows):
        x = w * (0.5 + 0.5 * r / max(closure_rows, 1)) - w * 0.25
        internals.append(fc.Internal(f"closure-row-{r}",
                                     [fc.P(x, h * 0.2), fc.P(x, h * 0.8)],
                                     kind="drill"))
    return fc.Piece(
        "closure",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("free", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "centre-front match")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Closure extension",
    )


def build():
    pattern = fc.PatternSet("biometric-bra-band")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "lining":
        pattern.add(build_lining())
    if all_pieces or target_piece == "closure":
        pattern.add(build_closure())

    if all_pieces:
        # Shell ↔ lining at both long edges. These are the seams that must solve:
        # two rings cut for DIFFERENT stretch must still arrive at the same length.
        # The declared ease is the deliberate difference the lining relaxes out.
        lining_extra = LINING_HALF - SHELL_HALF
        pattern.declare_seam(("lining", "bottom"), ("shell", "bottom"),
                             tol=1.0, ease=lining_extra)
        pattern.declare_seam(("lining", "top"), ("shell", "top"),
                             tol=1.0, ease=lining_extra)
        # The closure tab sews to the centre-front edge of the shell.
        pattern.declare_seam(("closure", "attach"), ("shell", "cf"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)
    n_electrodes = electrode_pairs * 2 * 2   # pairs x 2 sides x both halves of the ring
    pattern.bom = [
        {"item": "compression knit (conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 68% marker; shell and lining both."},
        {"item": "snap electrode carrier", "qty": n_electrodes, "unit": "count",
         "note": f"Yantra4D snap-electrode-carrier (notion.hardware_ref); "
                 f"{electrode_dia:.0f} mm disc, sewn to the marked carrier-sew ring, "
                 f"presenting through the lining's electrode window."},
        {"item": "snap electrodes", "qty": n_electrodes, "unit": "count",
         "note": "standard clinical snap studs; they click into the carrier bore."},
        {"item": "conductive thread", "qty": electrode_pairs * 2, "unit": "run",
         "note": "one run per marked signal-trace, carrier to the front connector."},
        {"item": "hook-and-eye tape", "qty": closure_rows, "unit": "row",
         "note": "on the closure extension; rows give the band its adjustment range."},
    ]
    pattern.metadata = {
        "fc300_rank": 263,
        "family": "etextile",
        "fabric_hint": "poliester-elastano-compresion",
        "finished_mm": {"underbust": round(underbust_girth, 1),
                        "band_depth": round(band_depth, 1),
                        "electrode_dia": round(electrode_dia, 1)},
        "solved": {
            "shell_half_mm": round(SHELL_HALF, 2),
            "shell_bottom_measured_mm": round(SHELL_BOTTOM, 2),
            "lining_half_mm": round(LINING_HALF, 2),
            "lining_ease_mm": round(LINING_HALF - SHELL_HALF, 2),
            "note": "the lining's cut length is derived from the SHELL'S MEASURED "
                    "geometry scaled by the ratio of the two negative eases, and the "
                    "difference is declared as seam ease — so the two rings, cut for "
                    "different stretch, still sew flat instead of one rippling.",
        },
        "etextile_note": "Electrode windows and sew rings are MARKED footprints for the "
                         "carrier; signal traces are marked routes. No circuit, amplifier, "
                         "or electrode is drafted here.",
        "hardware": "electrode carriers via Yantra4D (notion.hardware_ref -> "
                    "snap-electrode-carrier); the carrier's disc diameter is this band's "
                    "electrode_dia, which is also the marked window size",
        "not_a_medical_device": "This is a garment pattern. It carries electrodes; it "
                                "does not measure, diagnose, or monitor anything.",
    }
    return pattern


result = build()
