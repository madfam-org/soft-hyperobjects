"""
LED Trim Jacket — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A hip-length jacket whose illuminated trim is a drafted seam, not a strip stuck on
afterwards. A separate TRIM BAND is cut for the raglan seams and the hem: the band is
the carrier the Yantra4D `led-channel` extrusion clips into, and it is cut to the
MEASURED length of the seams it follows.

The whole point of this draft is that the LED run is a closed dimensional loop. The
raglan seam is a curve; you cannot know how long a strip of LED channel to print
until you have measured the curve you actually drew. So the kernel drafts the raglan
front/back/sleeve, measures the raglan seam lengths off the drawn Bezier, and cuts
the trim band to that sum — which is also the `length` fed to the led-channel solid.

Drafting note — the seam that must SOLVE: the raglan sleeve's two cap edges sew to the
front raglan edge and the back raglan edge respectively. Both are drafted from the SAME
control points (the raglan line runs neck-point to underarm on both bodice and sleeve),
so the pair matches by construction — and is then declared and machine-checked rather
than assumed.

Pieces:
  - front  : raglan front, cut on the fold, with the LED trim path marked.
  - back   : raglan back, cut on the fold.
  - sleeve : raglan sleeve with front and back cap edges.
  - trim   : the LED carrier band, cut to the measured raglan + hem run.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # front|back|sleeve|trim|set

chest_girth = float(PARAM(lambda: chest_girth, 1000.0))    # full chest
jacket_length = float(PARAM(lambda: jacket_length, 660.0))  # nape to hem
neck_width = float(PARAM(lambda: neck_width, 180.0))       # neck opening width
sleeve_length = float(PARAM(lambda: sleeve_length, 610.0))  # neck point to wrist
bicep_girth = float(PARAM(lambda: bicep_girth, 360.0))     # full bicep
raglan_depth = float(PARAM(lambda: raglan_depth, 250.0))   # neck point down to underarm
jacket_ease = float(PARAM(lambda: jacket_ease, 140.0))     # wearing ease at the chest
strip_w = float(PARAM(lambda: strip_w, 10.0))              # LED strip width
trim_width = float(PARAM(lambda: trim_width, 26.0))        # carrier band cut width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth = max(760.0, min(chest_girth, 1500.0))
jacket_length = max(480.0, min(jacket_length, 900.0))
neck_width = max(130.0, min(neck_width, 280.0))
sleeve_length = max(420.0, min(sleeve_length, 780.0))
bicep_girth = max(240.0, min(bicep_girth, 560.0))
raglan_depth = max(170.0, min(raglan_depth, 360.0))
jacket_ease = max(60.0, min(jacket_ease, 320.0))
strip_w = max(5.0, min(strip_w, 20.0))
trim_width = max(14.0, min(trim_width, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))
hem_allowance = max(0.0, min(hem_allowance, 60.0))

# The carrier band must be wide enough to take the channel plus a sewing margin.
trim_width = max(trim_width, strip_w + 10.0)

L = jacket_length
HALF = (chest_girth + jacket_ease) / 4.0     # quarter chest = half a folded panel
NECK_HALF = neck_width / 2.0
BICEP_HALF = bicep_girth / 2.0

# The raglan line, shared by bodice and sleeve: it runs from a point on the neckline
# out and down to the underarm. Both sides are drafted from these two endpoints with
# the same bulge, so the sleeve cap and the bodice armhole match by construction.
RAGLAN_BULGE = 0.14


def _raglan_edge(neck_pt, underarm_pt, side):
    return fc.curve_through(neck_pt, underarm_pt, bulge=RAGLAN_BULGE, side=side)


def _bodice(name, neck_dip, label, is_front):
    """A raglan bodice panel, cut on the fold at centre front/back.

    x = 0 is the fold (centre); x = HALF is the side seam. The raglan runs from the
    neckline out to the underarm, replacing the armhole entirely.
    """
    top_y = L
    neck_in = fc.P(0.0, top_y - neck_dip)          # centre neck, at the fold
    neck_out = fc.P(NECK_HALF, top_y)              # neck point where the raglan starts
    underarm = fc.P(HALF, top_y - raglan_depth)    # where the raglan lands

    edges = [
        fc.Edge("center", [fc.Line(fc.P(0.0, 0.0), neck_in)]),
        fc.Edge("neck", [fc.curve_through(neck_in, neck_out,
                                          bulge=neck_dip / max(NECK_HALF, 1.0) * 0.5,
                                          side=-1.0)]),
        fc.Edge("raglan", [_raglan_edge(neck_out, underarm, 1.0)]),
        fc.Edge("side", [fc.Line(underarm, fc.P(HALF, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(HALF, 0.0), fc.P(0.0, 0.0))]),
    ]

    internals = []
    if is_front:
        # The LED trim path: it follows the raglan seam and then turns along the hem.
        internals.append(fc.Internal("led-trim-path", [
            neck_out, fc.P(HALF * 0.7, top_y - raglan_depth * 0.5),
            underarm, fc.P(HALF, 0.0)], kind="marking"))
        # Driver + power-tap pocket, low on the inside front.
        bx, by = HALF * 0.55, L * 0.18
        w2, h2 = trim_width * 1.6, trim_width * 1.2
        internals.append(fc.Internal("driver-pocket", [
            fc.P(bx - w2, by - h2), fc.P(bx + w2, by - h2),
            fc.P(bx + w2, by + h2), fc.P(bx - w2, by + h2),
            fc.P(bx - w2, by - h2)], kind="marking"))
    else:
        # Back trim path mirrors the front's raglan run.
        internals.append(fc.Internal("led-trim-path", [
            neck_out, fc.P(HALF * 0.7, top_y - raglan_depth * 0.5), underarm],
            kind="marking"))

    return fc.Piece(
        name, edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance, "center": 0.0},
        notches=[fc.Notch("raglan", 0.5, "raglan midpoint"),
                 fc.Notch("side", 1.0, "underarm")],
        grainline=fc.Grainline(fc.P(HALF * 0.45, 60.0), fc.P(HALF * 0.45, L - 90.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="center", mirror=True),
        label=label,
    )


def build_front():
    return _bodice("front", 95.0, "Raglan Front (LED trim path)", True)


def build_back():
    return _bodice("back", 30.0, "Raglan Back", False)


def build_sleeve():
    """The raglan sleeve, drafted so its cap edges MATCH the bodice raglan edges.

    The raglan seam is one seam sewn from two pieces, so the sleeve cap is not free
    geometry: it must reproduce the bodice raglan's chord. The bodice raglan runs from
    the neck point to the underarm — a chord of (HALF - NECK_HALF) across by
    raglan_depth down. The sleeve cap is drafted on that SAME chord, opened out from
    the apex to each side, so cap ↔ raglan matches by construction rather than by
    fudge. The bicep width then follows from where the underarms land.
    """
    top_y = sleeve_length
    # The bodice raglan chord, component-wise — the shape the cap has to reproduce.
    chord_x = HALF - NECK_HALF
    chord_y = raglan_depth

    apex = fc.P(0.0, top_y)
    ua_l = fc.P(-chord_x, top_y - chord_y)
    ua_r = fc.P(chord_x, top_y - chord_y)
    # Bicep: the cap's landing width is fixed by the raglan chord, so a requested
    # bicep larger than that is honoured by flaring the sleeve BELOW the underarm —
    # widening the underseam rather than distorting the cap that has to match.
    bicep_flare = max(0.0, BICEP_HALF - chord_x)
    wrist_half = max(BICEP_HALF * 0.62, 55.0)
    flare_l = fc.P(-chord_x - bicep_flare, top_y - chord_y - raglan_depth * 0.12)
    flare_r = fc.P(chord_x + bicep_flare, top_y - chord_y - raglan_depth * 0.12)

    edges = [
        fc.Edge("underseam_l", [fc.Line(fc.P(-wrist_half, 0.0), flare_l),
                                fc.Line(flare_l, ua_l)]),
        # cap_front sews to front.raglan; cap_back sews to back.raglan. Both are drawn
        # with the same endpoints and bulge as the bodice raglan edges — the chain runs
        # ua_l → apex → ua_r, so cap_front is drawn in that travel direction and the
        # `side` sign is flipped to keep the bow on the same physical side of the curve.
        fc.Edge("cap_front", [_raglan_edge(ua_l, apex, -1.0)]),
        fc.Edge("cap_back", [_raglan_edge(apex, ua_r, -1.0)]),
        fc.Edge("underseam_r", [fc.Line(ua_r, flare_r),
                                fc.Line(flare_r, fc.P(wrist_half, 0.0))]),
        fc.Edge("wrist", [fc.Line(fc.P(wrist_half, 0.0), fc.P(-wrist_half, 0.0))]),
    ]

    internals = [
        # The trim runs down the sleeve from the cap apex toward the wrist.
        fc.Internal("led-trim-path", [
            fc.P(0.0, top_y - raglan_depth * 0.2), fc.P(0.0, sleeve_length * 0.12)],
            kind="marking"),
        # Cable pass-through just inside the underarm — the run into the bodice.
        fc.Internal("cable-pass", [
            fc.P(chord_x - trim_width, top_y - chord_y + 12.0),
            fc.P(chord_x, top_y - chord_y + 12.0)], kind="drill"),
    ]

    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"wrist": hem_allowance},
        notches=[fc.Notch("cap_front", 0.5, "front raglan midpoint"),
                 fc.Notch("cap_back", 0.5, "back raglan midpoint")],
        grainline=fc.Grainline(fc.P(0.0, sleeve_length * 0.15),
                               fc.P(0.0, sleeve_length * 0.7)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Raglan Sleeve",
    )


# ── The measured LED run ─────────────────────────────────────────────────────
# Draft the pieces once, off-pattern, purely to MEASURE the seams the trim follows.
# This is the closed loop: the trim band and the led-channel `length` both come from
# the geometry actually drawn, not from an estimate of it.
_F = build_front()
_B = build_back()
_S = build_sleeve()

RAGLAN_RUN = (_F.edge("raglan").length() + _B.edge("raglan").length()) * 2.0
HEM_RUN = _F.edge("hem").length() * 2.0 + _B.edge("hem").length() * 2.0
TRIM_RUN = RAGLAN_RUN + HEM_RUN


def build_trim():
    """The LED carrier band: one continuous strip cut to the MEASURED trim run.

    Drafted as a folded strip; it is topstitched over the raglan seams and the hem,
    and the Yantra4D led-channel clips into it. Its length is TRIM_RUN, which is the
    same number the manifest maps into the solid's `length` parameter.
    """
    ln, w = TRIM_RUN, trim_width
    internals = [
        # The channel seat: where the extrusion sits, centred in the band.
        fc.Internal("channel-seat", [
            fc.P(0.0, w / 2.0 - strip_w / 2.0), fc.P(ln, w / 2.0 - strip_w / 2.0),
            fc.P(ln, w / 2.0 + strip_w / 2.0), fc.P(0.0, w / 2.0 + strip_w / 2.0)],
            kind="marking"),
    ]
    # Segment marks: where to cut the continuous band into the four seam runs.
    marks = [_F.edge("raglan").length(), _B.edge("raglan").length(),
             _F.edge("raglan").length(), _B.edge("raglan").length()]
    run = 0.0
    for i, m in enumerate(marks):
        run += m
        internals.append(fc.Internal(f"segment-mark-{i}",
                                     [fc.P(run, 0.0), fc.P(run, w)], kind="drill"))

    return fc.Piece(
        "trim",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", RAGLAN_RUN / TRIM_RUN, "raglan run ends, hem begins")],
        grainline=fc.Grainline(fc.P(ln * 0.15, w / 2.0), fc.P(ln * 0.85, w / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="LED Carrier Trim Band",
    )


def build():
    pattern = fc.PatternSet("led-trim-jacket")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "front":
        pattern.add(build_front())
    if all_pieces or target_piece == "back":
        pattern.add(build_back())
    if all_pieces or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if all_pieces or target_piece == "trim":
        pattern.add(build_trim())

    if all_pieces:
        # The raglan pair: sleeve cap edges into the bodice raglan edges. Drafted
        # from shared endpoints, declared here so the kernel proves it.
        pattern.declare_seam(("sleeve", "cap_front"), ("front", "raglan"), tol=1.0)
        pattern.declare_seam(("sleeve", "cap_back"), ("back", "raglan"), tol=1.0)
        # Side seams and the sleeve underseam.
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("sleeve", "underseam_l"), ("sleeve", "underseam_r"), tol=1.0)
        # The trim band's attach edge = the measured raglan + hem run it is cut from.
        pattern.declare_seam(
            ("trim", "attach"),
            [("front", "raglan"), ("back", "raglan"),
             ("front", "raglan"), ("back", "raglan"),
             ("front", "hem"), ("front", "hem"),
             ("back", "hem"), ("back", "hem")],
            tol=1.0,
        )

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.74)
    pattern.bom = [
        {"item": "conductive-thread-compatible outerwear cloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 74% marker; the trim band is cut on the same cloth."},
        {"item": "LED channel", "qty": round(TRIM_RUN), "unit": "mm_length",
         "note": f"Yantra4D led-channel (notion.hardware_ref) printed to the MEASURED "
                 f"{TRIM_RUN:.0f} mm trim run, for a {strip_w:.0f} mm strip."},
        {"item": "addressable LED strip", "qty": round(TRIM_RUN), "unit": "mm_length",
         "note": f"{strip_w:.0f} mm wide; seats in the channel's marked seat line."},
        {"item": "driver + battery", "qty": 1, "unit": "set",
         "note": "lives in the marked driver-pocket on the inside front."},
        {"item": "low-voltage cable", "qty": 2, "unit": "run",
         "note": "sleeve-to-bodice runs pass at the marked cable-pass drill points."},
    ]
    pattern.metadata = {
        "fc300_rank": 262,
        "family": "etextile",
        "fabric_hint": "popelina-algodon",
        "finished_mm": {"chest": round(chest_girth, 1),
                        "length": round(jacket_length, 1),
                        "sleeve": round(sleeve_length, 1)},
        "solved": {
            "raglan_run_mm": round(RAGLAN_RUN, 2),
            "hem_run_mm": round(HEM_RUN, 2),
            "trim_run_mm": round(TRIM_RUN, 2),
            "note": "the trim band and the led-channel length are the MEASURED raglan "
                    "curve + hem run of the drafted pieces — the raglan is a Bezier, so "
                    "its length can only be known by measuring what was drawn.",
        },
        "etextile_note": "LED trim is a drafted CARRIER BAND, not a stuck-on strip. The "
                         "channel seat and the segment marks are marked for the maker; "
                         "no circuit or driver is drafted here.",
        "hardware": "LED channel via Yantra4D (notion.hardware_ref -> led-channel); the "
                    "channel's length is this jacket's measured trim run and its strip "
                    "width is the band's channel seat",
    }
    return pattern


result = build()
