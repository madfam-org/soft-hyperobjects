"""
EMG-Electrode Sleeve Band — Fashion Cabinet E-Textile Cartridge (FC-500 #471; snap-electrode-
carrier).

A tapered compression band worn on the forearm or bicep that clamps a pair of EMG electrodes to
the muscle belly and routes their leads to a small connector tab. It is the standalone sibling of
the `ecg-monitoring-vest` and the commons `rehab-sensor-cuff`: not a whole garment, but the one
band a therapist or a maker slides onto a bare limb to hold two electrodes at a measured spacing
over a specific muscle, so the signal is clean because the electrodes do not slide.

  **This is a garment pattern, not a medical device.** It positions and clamps electrodes and
  routes their leads. It does not measure, monitor, or diagnose, and makes no clinical claim.

The grip that must SOLVE (the dead-length trap, again). The band grips by NEGATIVE ease. But the
two electrode carriers are RIGID and cannot stretch, so their combined footprint plus margins is a
DEAD length; the grip comes out of the LIVE remainder only:

    dead  = 2 * (electrode_dia + 2*electrode_margin)
    live  = limb_girth - dead
    band  = dead + live * (1 - grip)

Drafted naively as limb*(1-grip) the band is short by dead*grip and the electrodes rock on a band
stretched across them — the exact failure that turns EMG into noise. At the parameter extremes
DEAD exceeds the limb girth (two big electrodes on a thin wrist) and LIVE goes negative; the dead
island is capped at a fraction of the girth and the cap is reported.

The band is TAPERED (a limb is a cone), so it is drafted as a trapezoid from the proximal girth to
the distal girth, and the electrode spacing is placed along its length.

The DIMENSIONAL HANDSHAKE. `snap-electrode-carrier`'s `disc_dia` is driven by `electrode_dia`,
which also drives the drafted seat AND the band's `electrode_seat` interface.

Made to measure to two limb girths. FC-500 lane 8 (e-textile & smart garments III).

Sandbox contract: `fc`/`math` pre-injected; params as bare globals via PARAM; result = PatternSet.
"""

import fc


def PARAM(getter, default):
    try:
        v = getter()
        return default if v is None else v
    except Exception:
        return default


# ── Parameters ───────────────────────────────────────────────────────────────
target_piece = str(PARAM(lambda: target_piece, "set"))

proximal_girth = float(PARAM(lambda: proximal_girth, 300.0))  # nearer the body (wider)
distal_girth = float(PARAM(lambda: distal_girth, 260.0))      # farther (narrower)
band_length = float(PARAM(lambda: band_length, 120.0))        # along the limb
grip = float(PARAM(lambda: grip, 0.14))                       # negative ease on the LIVE run
electrode_dia = float(PARAM(lambda: electrode_dia, 34.0))
electrode_margin = float(PARAM(lambda: electrode_margin, 12.0))
electrode_span = float(PARAM(lambda: electrode_span, 60.0))   # spacing between the two electrodes
channel_w = float(PARAM(lambda: channel_w, 8.0))
tab_len = float(PARAM(lambda: tab_len, 50.0))                 # connector tab
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
proximal_girth = max(160.0, min(proximal_girth, 600.0))
distal_girth = max(120.0, min(distal_girth, 560.0))
band_length = max(60.0, min(band_length, 260.0))
grip = max(0.0, min(grip, 0.28))
electrode_dia = max(16.0, min(electrode_dia, 60.0))
electrode_margin = max(4.0, min(electrode_margin, 26.0))
electrode_span = max(30.0, min(electrode_span, 160.0))
channel_w = max(4.0, min(channel_w, 18.0))
tab_len = max(25.0, min(tab_len, 120.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# distal must not exceed proximal (a limb narrows outward); clamp
distal_girth = min(distal_girth, proximal_girth)

# ── The dead-length grip solve (per girth) ───────────────────────────────────
def _solve_band(girth):
    dead = 2.0 * (electrode_dia + 2.0 * electrode_margin)
    cap = girth * 0.55
    capped = dead > cap
    if capped:
        dead = cap
    live = girth - dead
    band = dead + live * (1.0 - grip)
    return dead, live, band, capped


PROX_DEAD, PROX_LIVE, PROX_BAND, PROX_CAPPED = _solve_band(proximal_girth)
DIST_DEAD, DIST_LIVE, DIST_BAND, DIST_CAPPED = _solve_band(distal_girth)
# the band is DOUBLE its finished depth (folds), depth = band_length
CUT_DEPTH = band_length * 2.0
# electrode spacing along the band length; clamp inside the finished depth
ELEC_SPAN = min(electrode_span, band_length - electrode_dia - 8.0)
ELEC_SPAN = max(ELEC_SPAN, electrode_dia * 0.5)


def build_band():
    """Tapered band: a trapezoid, proximal band length at the bottom, distal at the top,
    folding at band_length. Carries the two electrode seats and the channel between them."""
    # x runs along the girth; y is the band depth (doubled for the fold).
    # proximal at y=0, distal at y=CUT_DEPTH (fold at band_length in between).
    prox = PROX_BAND
    dist = DIST_BAND
    # centre the narrower distal over the wider proximal
    off = (prox - dist) / 2.0
    p_bl = fc.P(0.0, 0.0)
    p_br = fc.P(prox, 0.0)
    p_tr = fc.P(off + dist, CUT_DEPTH)
    p_tl = fc.P(off, CUT_DEPTH)
    edges = [
        fc.Edge("proximal", [fc.Line(p_bl, p_br)]),
        fc.Edge("join_r", [fc.Line(p_br, p_tr)]),
        fc.Edge("distal", [fc.Line(p_tr, p_tl)]),
        fc.Edge("join_l", [fc.Line(p_tl, p_bl)]),
    ]
    # two electrode seats along the band, ELEC_SPAN apart, on the finished (lower) half.
    cx = prox / 2.0
    seat_y0 = band_length * 0.5 - ELEC_SPAN / 2.0
    seat_y1 = band_length * 0.5 + ELEC_SPAN / 2.0
    r = electrode_dia / 2.0
    internals = [
        fc.Internal("fold-line",
                    [fc.P(off / 2.0, band_length), fc.P(prox - off / 2.0, band_length)],
                    kind="marking"),
        fc.Internal("channel-centre", [fc.P(cx, seat_y0), fc.P(cx, seat_y1)], kind="trace"),
        fc.Internal("dead-start", [fc.P(cx - PROX_DEAD / 4.0, 0.0),
                                   fc.P(cx - PROX_DEAD / 4.0, band_length)], kind="marking"),
        fc.Internal("dead-end", [fc.P(cx + PROX_DEAD / 4.0, 0.0),
                                 fc.P(cx + PROX_DEAD / 4.0, band_length)], kind="marking"),
    ]
    for i, sy in enumerate((seat_y0, seat_y1)):
        internals.append(fc.Internal(f"electrode-seat-{i}",
                                     [fc.P(cx - r, sy - r), fc.P(cx + r, sy - r),
                                      fc.P(cx + r, sy + r), fc.P(cx - r, sy + r),
                                      fc.P(cx - r, sy - r)], kind="marking"))
        for lx, ly in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            px = cx + lx * (r - 4.0)
            py = sy + ly * (r - 4.0)
            internals.append(fc.Internal(f"sew-{i}-{lx}-{ly}", [fc.P(px, py), fc.P(px, py)],
                                         kind="drill"))
    return fc.Piece(
        "band", edges, seam_allowance=seam_allowance,
        allowances={"distal": 0.0},   # elastic-finished top edge
        notches=[fc.Notch("proximal", 0.5, "muscle centre"),
                 fc.Notch("distal", 0.5, "muscle centre")],
        grainline=fc.Grainline(fc.P(prox * 0.5, band_length * 0.2),
                               fc.P(off + dist * 0.5, CUT_DEPTH - band_length * 0.2)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Tapered EMG band (solved grip)",
    )


_BAND = build_band()
PROX_MEASURED = _BAND.edge("proximal").length()


def build_tab():
    """Connector tab: where the two leads leave the channel for a snap connector."""
    w = tab_len
    h = channel_w + 26.0
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, h), fc.P(0.0, h)
    edges = [
        fc.Edge("lower", [fc.Line(p0, p1)]),
        fc.Edge("free", [fc.Line(p1, p2)]),
        fc.Edge("upper", [fc.Line(p2, p3)]),
        fc.Edge("attach", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("lead-path", [fc.P(0.0, h / 2.0), fc.P(w, h / 2.0)], kind="trace"),
                 fc.Internal("strain-land",
                             [fc.P(w * 0.55, 6.0), fc.P(w - 6.0, 6.0),
                              fc.P(w - 6.0, h - 6.0), fc.P(w * 0.55, h - 6.0),
                              fc.P(w * 0.55, 6.0)], kind="marking")]
    return fc.Piece(
        "tab", edges, seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "channel centre")],
        grainline=fc.Grainline(fc.P(6.0, h / 2.0), fc.P(w - 6.0, h / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Connector tab (cut 1)",
    )


def build():
    pattern = fc.PatternSet("emg-sleeve-band")
    band = build_band()
    tab = build_tab()

    picked = {"band": band, "tab": tab}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (band, tab):
            pattern.add(piece)
        # The band closes on itself (proximal ring): join_l to join_r.
        pattern.declare_seam(("band", "join_l"), ("band", "join_r"), tol=1.0)

    fabric_width = 1500.0
    area = band.area() + tab.area()
    marker_len = area / (fabric_width * 0.7)
    pattern.bom = [
        {"item": "compression knit (poly/elastane, conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"the band folds double; at {fabric_width:.0f} mm width, 70% marker. The 110 C "
                 "iron ceiling governs near the channel."},
        {"item": "snap electrode carriers (Yantra4D snap-electrode-carrier)", "qty": 2,
         "unit": "count",
         "note": f"two carriers, disc {electrode_dia:.0f} mm, seated at the marked windows "
                 f"{ELEC_SPAN:.0f} mm apart (notion.hardware_ref -> snap-electrode-carrier)."},
        {"item": "conductive thread or ribbon", "qty": round(ELEC_SPAN + tab_len + 40.0),
         "unit": "mm_length",
         "note": "laid in the channel between the layers and out to the tab, never on the face."},
        {"item": "coverstitch thread + clear stay-tape", "qty": 1, "unit": "set",
         "note": f"stay-tape along the {PROX_DEAD:.0f} mm dead length only — stops a machinist "
                 "stretching the rigid electrode zone."},
    ]
    pattern.metadata = {
        "fc500_rank": 471, "family": "etextile", "fabric_hint": "jersey-conductor",
        "not_a_device": "This positions and clamps electrodes and routes leads. It does not "
                        "measure, monitor, or diagnose. No clinical claim.",
        "silhouette_note": "A tapered compression band that clamps two EMG electrodes to a muscle "
            "belly at a measured spacing and routes their leads to a connector tab. Standalone — "
            "slides onto a bare limb.",
        "hardware": "electrode carriers via Yantra4D (hardware_ref -> snap-electrode-carrier); "
            "electrode_dia drives the carrier disc AND the drafted seat.",
        "solved": {
            "proximal_band_mm": round(PROX_BAND, 2),
            "distal_band_mm": round(DIST_BAND, 2),
            "proximal_dead_mm": round(PROX_DEAD, 2),
            "proximal_capped": PROX_CAPPED,
            "distal_capped": DIST_CAPPED,
            "grip": round(grip, 3),
            "electrode_span_mm": round(ELEC_SPAN, 1),
            "proximal_measured_mm": round(PROX_MEASURED, 2),
            "note": "band = dead + (girth - dead)*(1 - grip) at each girth; the rigid electrode "
                    "dead length takes no stretch, so the naive girth*(1-grip) is short by "
                    "dead*grip. The dead island is capped at 55% of the girth (at the extremes "
                    "two big electrodes on a thin limb make DEAD exceed the girth).",
        },
        "etextile_note": "The electrode seats, sew points, channel, dead-length markers and the "
                         "tab lead-path are MARKED. No electrode or circuit is drafted.",
    }
    return pattern


result = build()
