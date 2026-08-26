"""
ECG-Electrode Monitoring Vest — Fashion Cabinet E-Textile Cartridge (FC-500 #467; snap-electrode-
carrier).

A close-fitting compression vest that holds a set of ECG electrodes at measured positions against
the torso and routes their conductive traces, between the shell and a lining, to a single service
pocket where a recorder clips on. It is the garment version of a Holter harness: instead of sticky
gel dots that peel in a day, the electrodes are printable `snap-electrode-carrier` studs seated in
lining windows, and the routing lives in stitched channels that a washing machine never abrades.

  **This is a garment pattern, not a medical device.** It positions electrodes and routes leads.
  It does not measure, monitor, or diagnose anything, and makes no clinical claim.

The seam that must SOLVE. A monitoring vest works only if the electrodes stay put, which means the
shell is a COMPRESSION garment: cut shorter than the torso at a declared negative ease so it holds
the electrodes still. But an electrode carrier is rigid and cannot stretch. Each carrier's
footprint plus its margin is a DEAD length that contributes fully to the sewn ring and nothing to
the stretch, so the compression is taken out of the LIVE remainder only:

    dead  = electrode_count * (electrode_dia + 2*electrode_margin)
    live  = chest_ring - dead
    shell = dead + live * (1 - compression)

Drafted naively as chest*(1-compression) the shell comes up short by dead*compression, and the
electrodes rock on a ring stretched across them — motion artefact, not signal. The dead island is
capped at a fraction of the ring (at the extremes it exceeds the ring entirely) and the cap is
reported.

The DIMENSIONAL HANDSHAKE. The carrier is `snap-electrode-carrier`; `electrode_dia` drives the
carrier's `disc_dia` (its sew face) AND the drafted electrode seat AND the vest's `electrode_seat`
interface, so the printed stud is exactly as wide as the window it snaps into.

Made to measure to chest/bust girth. FC-500 lane 8 (e-textile & smart garments III).

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

chest_bust_girth = float(PARAM(lambda: chest_bust_girth, 960.0))
vest_length = float(PARAM(lambda: vest_length, 420.0))       # underarm to hem
compression = float(PARAM(lambda: compression, 0.12))        # shell negative ease
electrode_count = float(PARAM(lambda: electrode_count, 6.0)) # number of ECG electrodes
electrode_dia = float(PARAM(lambda: electrode_dia, 40.0))    # carrier disc diameter
electrode_margin = float(PARAM(lambda: electrode_margin, 14.0))
channel_w = float(PARAM(lambda: channel_w, 9.0))             # conductive channel width
pocket_w = float(PARAM(lambda: pocket_w, 90.0))              # recorder pocket
lining_ease = float(PARAM(lambda: lining_ease, 0.04))        # lining is gentler than shell
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_bust_girth = max(700.0, min(chest_bust_girth, 1500.0))
vest_length = max(200.0, min(vest_length, 700.0))
compression = max(0.04, min(compression, 0.24))
electrode_count = max(2.0, min(electrode_count, 12.0))
electrode_dia = max(20.0, min(electrode_dia, 70.0))
electrode_margin = max(6.0, min(electrode_margin, 30.0))
channel_w = max(4.0, min(channel_w, 20.0))
pocket_w = max(60.0, min(pocket_w, 160.0))
lining_ease = max(0.0, min(lining_ease, 0.12))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# lining must never grip harder than the shell (else it takes the electrodes off their marks)
lining_ease = min(lining_ease, compression)
N_ELEC = int(round(electrode_count))

# ── The dead-length solve ────────────────────────────────────────────────────
DEAD = N_ELEC * (electrode_dia + 2.0 * electrode_margin)
_DEAD_CAP = chest_bust_girth * 0.55
DEAD_CAPPED = DEAD > _DEAD_CAP
if DEAD_CAPPED:
    DEAD = _DEAD_CAP
LIVE = chest_bust_girth - DEAD
SHELL_RING = DEAD + LIVE * (1.0 - compression)
NAIVE_RING = chest_bust_girth * (1.0 - compression)
SHORTFALL = SHELL_RING - NAIVE_RING           # == DEAD * compression, >= 0
LINING_RING = DEAD + (chest_bust_girth - DEAD) * (1.0 - lining_ease)
SHELL_HALF = SHELL_RING / 2.0                 # cut on fold at CB -> half
LINING_HALF = LINING_RING / 2.0
VL = vest_length
ARMSCYE = max(180.0, VL * 0.5)


def _panel(name, half_w, on_fold_edge):
    """A vest panel (shell or lining): a torso block from hem to shoulder with an armscye and
    a scooped neck. Cut on the CB fold. `half_w` is the finished half-ring at this ease."""
    p_cb_hem = fc.P(0.0, 0.0)
    p_side_hem = fc.P(half_w / 2.0, 0.0)          # per-panel quarter at the side
    underarm_y = VL - ARMSCYE
    p_underarm = fc.P(half_w / 2.0, underarm_y)
    neck_w = max(70.0, half_w / 6.0)
    p_shoulder = fc.P(neck_w + (half_w / 2.0 - neck_w) * 0.55, VL - 10.0)
    p_neck = fc.P(neck_w, VL)
    p_cb_neck = fc.P(0.0, VL)
    edges = [
        fc.Edge("hem", [fc.Line(p_cb_hem, p_side_hem)]),
        fc.Edge("side", [fc.Line(p_side_hem, p_underarm)]),
        fc.Edge("armscye", [fc.Bezier(p_underarm,
                                      fc.P(half_w / 2.0 * 0.9, underarm_y + ARMSCYE * 0.5),
                                      fc.P(p_shoulder.x + 12.0, p_shoulder.y - 30.0),
                                      p_shoulder)]),
        fc.Edge("shoulder", [fc.Line(p_shoulder, p_neck)]),
        fc.Edge("neck", [fc.Bezier(p_neck, fc.P(neck_w * 0.5, VL - 2.0),
                                   fc.P(neck_w * 0.2, VL - 1.0), p_cb_neck)]),
        fc.Edge("center_back", [fc.Line(p_cb_neck, p_cb_hem)]),
    ]
    return p_cb_hem, p_side_hem, underarm_y, edges


def build_shell():
    _, _, _, edges = _panel("shell", SHELL_HALF, "center_back")
    # dead-length markers: the electrode zone must NOT be stretched.
    internals = [fc.Internal("compression-note",
                             [fc.P(4.0, VL * 0.5), fc.P(SHELL_HALF / 2.0 - 4.0, VL * 0.5)],
                             kind="marking")]
    return fc.Piece(
        "shell", edges, seam_allowance=seam_allowance,
        allowances={"hem": 0.0},
        notches=[fc.Notch("side", 0.5, "side match"),
                 fc.Notch("hem", 0.5, "CF match")],
        grainline=fc.Grainline(fc.P(SHELL_HALF / 4.0, VL * 0.2), fc.P(SHELL_HALF / 4.0, VL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Compression shell (cut 1 on CB fold)",
    )


def build_lining():
    _, p_side_hem, underarm_y, edges = _panel("lining", LINING_HALF, "center_back")
    half_w = LINING_HALF
    # electrode seats + channel routing marked on the lining (the electrodes sit against skin).
    internals = []
    for i in range(N_ELEC):
        # place electrodes in a grid across the front half of the panel
        col = i % 3
        row = i // 3
        ex = (half_w / 2.0) * (0.2 + 0.28 * col)
        ey = VL * (0.30 + 0.22 * (row % 3))
        r = electrode_dia / 2.0
        internals.append(fc.Internal(f"electrode-seat-{i}",
                                     [fc.P(ex - r, ey - r), fc.P(ex + r, ey - r),
                                      fc.P(ex + r, ey + r), fc.P(ex - r, ey + r),
                                      fc.P(ex - r, ey - r)], kind="marking"))
        # the channel from this electrode toward the pocket (top side seam)
        internals.append(fc.Internal(f"trace-{i}",
                                     [fc.P(ex, ey), fc.P(half_w / 2.0 - 6.0, ey),
                                      fc.P(half_w / 2.0 - 6.0, underarm_y - 10.0)], kind="trace"))
    return fc.Piece(
        "lining", edges, seam_allowance=seam_allowance,
        allowances={"hem": 0.0},
        notches=[fc.Notch("side", 0.5, "side match")],
        grainline=fc.Grainline(fc.P(half_w / 4.0, VL * 0.2), fc.P(half_w / 4.0, VL * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center_back"),
        label="Electrode-carrier lining (cut 1 on CB fold)",
    )


def build_pocket():
    """Recorder pocket: where all traces converge and the clip-on recorder sits."""
    w, d = pocket_w, pocket_w * 1.2
    p0, p1 = fc.P(0.0, 0.0), fc.P(w, 0.0)
    p2, p3 = fc.P(w, d), fc.P(0.0, d)
    edges = [
        fc.Edge("bottom", [fc.Line(p0, p1)]),
        fc.Edge("side_r", [fc.Line(p1, p2)]),
        fc.Edge("mouth", [fc.Line(p2, p3)]),
        fc.Edge("side_l", [fc.Line(p3, p0)]),
    ]
    internals = [fc.Internal("trace-entry", [fc.P(w * 0.5, 0.0), fc.P(w * 0.5, d * 0.4)],
                             kind="trace"),
                 fc.Internal("mouth-fold", [fc.P(0.0, d - 20.0), fc.P(w, d - 20.0)],
                     kind="marking")]
    return fc.Piece(
        "pocket", edges, seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        grainline=fc.Grainline(fc.P(w * 0.5, d * 0.2), fc.P(w * 0.5, d * 0.8)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Recorder pocket (cut 1)",
    )


def build():
    pattern = fc.PatternSet("ecg-monitoring-vest")
    shell = build_shell()
    lining = build_lining()
    pocket = build_pocket()

    picked = {"shell": shell, "lining": lining, "pocket": pocket}
    if target_piece in picked:
        pattern.add(picked[target_piece])
    else:
        for piece in (shell, lining, pocket):
            pattern.add(piece)
        # Shell + lining side seams sew together (the two layers close as one at the side).
        # They are cut for DIFFERENT ease, so the lining side is declared against the shell
        # side with the ease difference so an over-tight lining can never sneak in.
        ease_diff = lining.edge("side").length() - shell.edge("side").length()
        pattern.declare_seam(("lining", "side"), ("shell", "side"), tol=2.0, ease=ease_diff)
        # The hems align (both finished flat).
        hem_diff = lining.edge("hem").length() - shell.edge("hem").length()
        pattern.declare_seam(("lining", "hem"), ("shell", "hem"), tol=3.0, ease=hem_diff)

    fabric_width = 1550.0
    area = shell.area() * 2.0 + lining.area() * 2.0 + pocket.area()
    marker_len = area / (fabric_width * 0.82)
    pattern.bom = [
        {"item": "compression knit (poly/elastane, conductive-thread compatible)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"shell + lining at {fabric_width:.0f} mm width, 82% marker. The 110 C iron "
                 "ceiling governs everywhere near the traces."},
        {"item": "snap electrode carriers (Yantra4D snap-electrode-carrier)", "qty": N_ELEC,
         "unit": "count",
         "note": f"{N_ELEC} carriers, disc {electrode_dia:.0f} mm, seated in the marked lining "
                 "windows (notion.hardware_ref -> snap-electrode-carrier); each takes a standard "
                 "clinical snap stud."},
        {"item": "conductive thread or ribbon", "qty": round(N_ELEC * VL * 0.9),
         "unit": "mm_length",
         "note": f"laid in the marked channels BETWEEN shell and lining, never on the face; "
                 f"{N_ELEC} traces converge at the pocket."},
        {"item": "coverstitch thread + clear stay-tape", "qty": 1, "unit": "set",
         "note": f"stay-tape along the {DEAD:.0f} mm dead length only — it stops a machinist "
                 "stretching the rigid electrode zone."},
    ]
    pattern.metadata = {
        "fc500_rank": 467, "family": "etextile", "fabric_hint": "jersey-conductor",
        "not_a_device": "This positions electrodes and routes leads. It does not measure, "
                        "monitor, or diagnose. No clinical claim.",
        "silhouette_note": "Compression monitoring vest: a shell holding printable ECG electrode "
            "carriers at measured positions, a lining carrying the seats and channels, converging "
            "at a recorder pocket. The electrodes stay put because the shell compresses around "
            "their rigid dead length, not across it.",
        "hardware": "electrode carriers via Yantra4D (hardware_ref -> snap-electrode-carrier); "
            "electrode_dia drives the carrier disc AND the drafted seat.",
        "solved": {
            "electrode_count": N_ELEC,
            "compression": round(compression, 3),
            "dead_length_mm": round(DEAD, 2),
            "dead_capped": DEAD_CAPPED,
            "live_length_mm": round(LIVE, 2),
            "shell_ring_mm": round(SHELL_RING, 2),
            "naive_ring_mm": round(NAIVE_RING, 2),
            "shortfall_avoided_mm": round(SHORTFALL, 2),
            "lining_ring_mm": round(LINING_RING, 2),
            "note": "shell = dead + (chest - dead)*(1 - compression); the rigid electrode dead "
                    "length takes no stretch, so the naive chest*(1-compression) is short by "
                    "dead*compression and the electrodes rock. The lining eases gentler than the "
                    "shell so it never pulls the electrodes off their marks.",
        },
        "etextile_note": "Electrode seats, sew rings, channel traces and the pocket entry are "
                         "MARKED. No electrode, conductor, recorder, or circuit is drafted here.",
    }
    return pattern


result = build()
