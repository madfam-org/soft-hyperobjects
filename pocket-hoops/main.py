"""
Pocket Hoops — Fashion Cabinet Costume Cartridge (FC-300 rank #268, y4d boning-stay bridged).

Paired side hoops (small panniers, "pocket hoops") of the mid-18th century, c. 1740–1770.
These are the understructure that gives the period gown its width at the hips while leaving
the front and back nearly flat — the silhouette is WIDE, not round. A full round farthingale
or a bell hoop is a different garment entirely; the defining feature of pocket hoops is that
they are TWO separate baskets, one tied at each hip, joined only by a waist tape.

The documented construction this draft reproduces:

  - each hoop is a flat-bottomed bag of two shaped SIDE panels joined by a GUSSET strip that
    runs around the curved outer edge, giving the bag its depth;
  - horizontal CASINGS stitched across the side panels carry the hoop stays (cane, whalebone
    or, here, printed stay stock), each casing a different length as the bag widens downward;
  - the top edge gathers or pleats onto a WAIST TAPE that ties around the body, so one tape
    carries both hoops and the wearer can shed them independently of the stays;
  - the inner face is left open at the top as a genuine POCKET — this is why they are called
    pocket hoops and not simply side hoops.

Drafting note — the seam that must SOLVE. The gusset strip is what turns two flat side panels
into a bag with depth, so its length must equal the panel's curved outer run EXACTLY, or the
bag will not close. That run is not a formula: the side panel's outer edge is drafted as a
polyline through the hip curve, its length is MEASURED off the built piece, and the gusset is
then cut to precisely that measured length. Both side panels of a hoop share the one gusset,
so the gusset is drafted at the measured run and the seam is declared against each panel.

Pieces:
  - side_panel : the shaped face of one hoop bag (cut 4 — two per hoop, mirrored).
  - gusset     : the depth strip around the curved outer edge (cut 2 — one per hoop).
  - waist_tape : the single tape that carries both hoops and ties at the waist (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # side_panel|gusset|waist_tape|set

hoop_width = float(PARAM(lambda: hoop_width, 340.0))    # how far ONE hoop stands out sideways
hoop_depth = float(PARAM(lambda: hoop_depth, 210.0))    # front-to-back thickness of the bag
hoop_drop = float(PARAM(lambda: hoop_drop, 380.0))      # waist tape down to the bottom stay
top_width = float(PARAM(lambda: top_width, 150.0))      # width at the waist, before it flares
stay_count = float(PARAM(lambda: stay_count, 4))        # horizontal hoop stays per side panel
waist_girth = float(PARAM(lambda: waist_girth, 700.0))  # for the tape length
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane 18th-c side-hoop ranges) ────────────────────────────────────
hoop_width = max(180.0, min(hoop_width, 620.0))
hoop_depth = max(110.0, min(hoop_depth, 340.0))
hoop_drop = max(240.0, min(hoop_drop, 560.0))
top_width = max(90.0, min(top_width, 260.0))
stay_count = int(max(2, min(stay_count, 7)))
waist_girth = max(500.0, min(waist_girth, 1300.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The top can never be wider than the hoop stands out, or there is no flare at all.
top_width = min(top_width, hoop_width * 0.85)

W = hoop_width
H = hoop_drop
TW = top_width
CURVE_STEPS = 24  # polyline resolution of the flaring outer edge


def _outer_edge_points():
    """The flaring outer edge of a side panel, from the waist down to the bottom stay.

    Drafted as an eased curve: the hoop flares fast just below the waist, then carries
    almost straight down to the widest bottom stay. The points are what get MEASURED —
    the gusset length is taken from this polyline, never from a formula.
    """
    pts = []
    for i in range(CURVE_STEPS + 1):
        t = i / CURVE_STEPS
        # ease-out flare: most of the width is gained in the upper third
        flare = 1.0 - (1.0 - t) ** 2.2
        x = TW + (W - TW) * flare
        y = H - H * t
        pts.append(fc.P(x, y))
    return pts


OUTER_PTS = _outer_edge_points()


def build_side_panel():
    """One face of a hoop bag (cut 4: two faces per hoop, two hoops).

    `outer` is the curved edge that takes the gusset. `top` gathers to the waist tape,
    `inner` is the body side (left open at the top as the pocket mouth), `bottom` is the
    flat base of the bag carrying the widest stay.
    """
    outer_segs = [fc.Line(OUTER_PTS[i], OUTER_PTS[i + 1]) for i in range(len(OUTER_PTS) - 1)]
    internals = []
    # Horizontal stay casings. Each sits at a different height, so each is a DIFFERENT
    # length as the bag widens downward — that difference is the point of the draft.
    casing_lengths = []
    for i in range(stay_count):
        t = (i + 1) / (stay_count + 1)
        y = H - H * t
        flare = 1.0 - (1.0 - t) ** 2.2
        x_out = TW + (W - TW) * flare
        casing_lengths.append(x_out)
        internals.append(fc.Internal("stay-casing",
                                     [fc.P(0.0, y), fc.P(x_out, y)], kind="marking"))
    # The pocket mouth: the inner face is left unstitched at the top so the bag is usable.
    internals.append(fc.Internal("pocket-mouth",
                                 [fc.P(0.0, H - 20.0), fc.P(0.0, H - 20.0 - hoop_drop * 0.30)],
                                 kind="trace"))
    edges = [
        fc.Edge("inner", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, H), fc.P(TW, H))]),
        fc.Edge("outer", outer_segs),
        fc.Edge("bottom", [fc.Line(fc.P(W, 0.0), fc.P(0.0, 0.0))]),
    ]
    piece = fc.Piece(
        "side_panel",
        edges,
        seam_allowance=seam_allowance,
        allowances={"top": 16.0},  # extra at the top: it pleats onto the tape
        notches=[fc.Notch("outer", 0.5, "gusset midpoint"),
                 fc.Notch("outer", 0.25, "gusset quarter")],
        grainline=fc.Grainline(fc.P(TW * 0.4, 24.0), fc.P(TW * 0.4, H - 24.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=4, mirror=True),
        label="Side panel (cut 4: 2 per hoop, mirrored)",
    )
    piece._casing_lengths = casing_lengths
    return piece


SIDE_PANEL = build_side_panel()
# The MEASURED curved outer run — this, not a formula, is the gusset's length.
OUTER_RUN = SIDE_PANEL.edge("outer").length()


def build_gusset():
    """The depth strip sewn around the curved outer edge, giving the bag its thickness.

    Cut to exactly the MEASURED outer run of the side panel, `hoop_depth` wide.
    One per hoop; it joins the hoop's two side panels into a bag.
    """
    ln, d = OUTER_RUN, hoop_depth
    internals = []
    # The stays continue around the gusset at the same heights, so the hoop is a
    # continuous ring rather than two stiffened faces flapping against a soft strip.
    for i in range(stay_count):
        t = (i + 1) / (stay_count + 1)
        x = ln * (1.0 - t)
        internals.append(fc.Internal("stay-crossing", [fc.P(x, 0.0), fc.P(x, d)],
                                     kind="marking"))
    return fc.Piece(
        "gusset",
        [
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_top", [fc.Line(fc.P(ln, 0.0), fc.P(ln, d))]),
            fc.Edge("seam_b", [fc.Line(fc.P(ln, d), fc.P(0.0, d))]),
            fc.Edge("end_bottom", [fc.Line(fc.P(0.0, d), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("seam_a", 0.5, "gusset midpoint"),
                 fc.Notch("seam_a", 0.25, "gusset quarter"),
                 fc.Notch("seam_b", 0.5, "gusset midpoint"),
                 fc.Notch("seam_b", 0.75, "gusset quarter")],
        grainline=fc.Grainline(fc.P(ln * 0.2, d * 0.5), fc.P(ln * 0.8, d * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label="Outer gusset (cut 2: one per hoop)",
    )


def build_waist_tape():
    """One tape carrying both hoops, long enough to go round the waist and tie."""
    ln = waist_girth + 500.0  # generous tying ends, in the period manner
    w = 28.0
    internals = []
    # Where each hoop's pleated top is stitched to the tape: two runs, one per hip.
    for cx in (ln * 0.5 - waist_girth * 0.22, ln * 0.5 + waist_girth * 0.22):
        internals.append(fc.Internal("hoop-attachment",
                                     [fc.P(cx - TW * 0.5, w * 0.5),
                                      fc.P(cx + TW * 0.5, w * 0.5)], kind="marking"))
    return fc.Piece(
        "waist_tape",
        [
            fc.Edge("end_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=8.0,
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Waist tape (cut 1, carries both hoops)",
    )


def build():
    pattern = fc.PatternSet("pocket-hoops")
    everything = target_piece == "set"
    if everything or target_piece == "side_panel":
        pattern.add(SIDE_PANEL)
    if everything or target_piece == "gusset":
        pattern.add(build_gusset())
    if everything or target_piece == "waist_tape":
        pattern.add(build_waist_tape())

    if everything:
        # The bag seam: the gusset's two long edges each take one side panel's curved
        # outer edge. The gusset was cut to the MEASURED run, so both balance exactly.
        pattern.declare_seam(("gusset", "seam_a"), ("side_panel", "outer"), tol=1.0)
        pattern.declare_seam(("gusset", "seam_b"), ("side_panel", "outer"), tol=1.0)

    fabric_width = 900.0  # period linen is narrow
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    total_stays = stay_count * 2 * 2  # per side panel, 2 panels per hoop, 2 hoops
    pattern.bom = [
        {"item": "linen or cotton ticking",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 900 mm width, 70% marker. A firm plain weave; period hoops are "
                 "linen or a striped cotton ticking, unlined."},
        {"item": "hoop stays (Yantra4D boning-stay)", "qty": total_stays, "unit": "count",
         "note": f"{stay_count} per side panel. Each casing is a DIFFERENT length as the bag "
                 f"widens downward — cut each stay to its own casing, do not batch one length. "
                 f"Period stock is cane or whalebone; the printed stay is the open equivalent."},
        {"item": "twill tape for casings", "qty": round(OUTER_RUN * stay_count * 2.0),
         "unit": "mm_length",
         "note": "if the casings are applied as tape rather than stitched channels."},
        {"item": "linen thread", "qty": 1, "unit": "spool",
         "note": "the outer bag seam takes the whole load of the flared hoop — backstitch "
                 "it by hand or use a short machine stitch."},
    ]
    pattern.metadata = {
        "fc300_rank": 268,
        "family": "costume_historical",
        "period": "c. 1740–1770 (mid-18th century)",
        "fabric_hint": "manta-cruda",
        "silhouette_note": "WIDE, not round. Two separate baskets tied at the hips leave the "
            "front and back of the gown nearly flat — that flatness is the whole point, and "
            "it is what distinguishes pocket hoops from a bell hoop or a farthingale.",
        "construction_note": "Two shaped side panels joined by a depth gusset around the "
            "curved outer edge; horizontal casings carry stays of graduated length; the top "
            "pleats onto a shared waist tape; the inner face is left open as a real pocket.",
        "hardware": "hoop stays via Yantra4D (notion.hardware_ref -> boning-stay); the "
            "measured outer run drives stay_length — the dimensional handshake.",
        "solved": {
            "outer_run_measured_mm": round(OUTER_RUN, 2),
            "gusset_cut_length_mm": round(OUTER_RUN, 2),
            "casing_lengths_mm": [round(c, 1) for c in SIDE_PANEL._casing_lengths],
            "hoop_depth_mm": round(hoop_depth, 1),
            "note": "the gusset is cut to the MEASURED length of the side panel's curved "
                    "outer polyline, so the bag closes exactly. Casing lengths are reported "
                    "individually because every stay in a hoop is a different length.",
        },
    }
    return pattern


result = build()
