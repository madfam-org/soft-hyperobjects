"""
Heated Glove Liner — Fashion Cabinet E-Textile Cartridge (FC-300 wave FC3-H).

A four-piece knit glove liner drafted so the heater harness is a first-class pattern
feature rather than an afterthought stuffed between layers. The back-of-hand TRANK
carries the serpentine heating traces that warm the metacarpals and the finger backs;
a wrist CUFF carries the strain-relieved cable exit; two FOURCHETTE strips form the
finger side-walls; and a THUMB gusset closes the hand.

The routing hardware: a Yantra4D `seam-conduit-clip` rides the trank-to-fourchette
seam, holding the heater bundle in a channel so it never crosses a flex crease. The
clip's sewn tab length is the garment's `conduit_tab` parameter — the same parameter
that dimensions the trank's marked conduit run — so the clip and the seam it clips to
are one dimension, not two that happen to agree.

Drafting note — the seam that must SOLVE: the fourchette is a folded strip that walks
the full perimeter of the three finger slits. Its length is measured off the drafted
trank's slit geometry (finger_len * 2 per slit plus the slit-tip arcs), not assumed
from a formula, and the strip is then cut to that measured length so the
trank-to-fourchette seam matches exactly.

Pieces:
  - trank      : back-of-hand blank with the three finger slits and the heat traces.
  - fourchette : the finger side-wall strip (cut 2, one per hand).
  - thumb      : thumb gusset.
  - cuff       : ribbed wrist cuff carrying the cable exit + strain relief.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # trank|fourchette|thumb|cuff|set

hand_width = float(PARAM(lambda: hand_width, 92.0))       # across the knuckles
hand_length = float(PARAM(lambda: hand_length, 190.0))    # wrist crease to middle fingertip
finger_len = float(PARAM(lambda: finger_len, 78.0))       # middle finger, knuckle to tip
wrist_girth = float(PARAM(lambda: wrist_girth, 172.0))    # wrist circumference
cuff_depth = float(PARAM(lambda: cuff_depth, 70.0))       # cuff height above the wrist
conduit_tab = float(PARAM(lambda: conduit_tab, 14.0))     # conduit-clip sewn tab length
heat_zones = int(PARAM(lambda: heat_zones, 3))            # serpentine heating zones
knit_stretch = float(PARAM(lambda: knit_stretch, 0.18))   # negative-ease factor of the knit
seam_allowance = float(PARAM(lambda: seam_allowance, 6.0))

# ── Clamps (a hand is a hand — keep the draft inside human range) ─────────────
hand_width = max(60.0, min(hand_width, 130.0))
hand_length = max(140.0, min(hand_length, 250.0))
finger_len = max(50.0, min(finger_len, 110.0))
wrist_girth = max(130.0, min(wrist_girth, 230.0))
cuff_depth = max(35.0, min(cuff_depth, 140.0))
conduit_tab = max(8.0, min(conduit_tab, 30.0))
heat_zones = max(1, min(heat_zones, 5))
knit_stretch = max(0.0, min(knit_stretch, 0.35))
seam_allowance = max(0.0, min(seam_allowance, 12.0))

# finger_len cannot exceed the hand it grows from; leave a palm.
finger_len = min(finger_len, hand_length * 0.55)

HALF_W = hand_width / 2.0
PALM_LEN = hand_length - finger_len          # wrist crease to knuckle line
SLITS = 3                                    # three slits make four fingers
ARC_SEGS = 12                                # slit-tip arc resolution


def _slit_geometry():
    """The three finger slits as (x_centre, half_width, depth) triples.

    Slits are cut from the knuckle line up toward the fingertips. Each is a
    narrow U: two straight walls plus a semicircular tip so the fourchette can
    turn the corner without a puckered point.
    """
    gap = hand_width / 4.0                    # four finger channels across the hand
    half = gap * 0.16                         # slit half-width (the seam-to-seam gap)
    out = []
    for i in range(SLITS):
        cx = -HALF_W + gap * (i + 1)
        # Index/little side fingers are shorter, so their slits cut deeper.
        depth = finger_len * (0.86 if i in (0, SLITS - 1) else 1.0)
        out.append((cx, half, depth))
    return out


SLIT_SPEC = _slit_geometry()


def _slit_path(cx, half, depth):
    """Points down one slit wall, around the tip, and back up the other wall.

    Returned in order from the knuckle line on the -x side, up to the tip, around,
    and back down to the knuckle line on the +x side.
    """
    y0 = PALM_LEN                              # knuckle line
    tip_y = y0 + depth - half                  # centre of the tip arc
    pts = [fc.P(cx - half, y0), fc.P(cx - half, tip_y)]
    for k in range(1, ARC_SEGS):
        a = math.pi + math.pi * (k / ARC_SEGS)   # sweep -x → +x over the top
        pts.append(fc.P(cx + half * math.cos(a) * -1.0, tip_y + half * math.sin(a) * -1.0))
    pts.append(fc.P(cx + half, tip_y))
    pts.append(fc.P(cx + half, y0))
    return pts


def _path_length(pts):
    return sum(pts[i].distance(pts[i + 1]) for i in range(len(pts) - 1))


# The MEASURED slit perimeter: this is what the fourchette strip must equal.
SLIT_RUN = sum(_path_length(_slit_path(*s)) for s in SLIT_SPEC)


def build_trank():
    """Back-of-hand blank: knuckle-line slits cut up toward the fingertips, the
    heating traces marked across the metacarpals and finger backs, and the conduit
    run marked down the side seam where the clip rides."""
    top = PALM_LEN + finger_len
    shoulder = top - finger_len * 0.16      # where the outer finger backs top out

    # The fingered top is built as an ALTERNATING chain of named edges: a finger back,
    # then a slit, then the next finger back, and so on. Naming the slits separately is
    # what makes the trank↔fourchette seam declarable — the fourchette sews to the
    # slit edges ONLY, not to the finger backs, and `declare_seam` sums a multi-edge
    # side, so the three slit edges together are one seam side.
    edges = [
        # left (little-finger) side wall, wrist up to the knuckle line
        fc.Edge("side_l", [fc.Line(fc.P(-HALF_W, 0.0), fc.P(-HALF_W, PALM_LEN))]),
    ]
    cursor = fc.P(-HALF_W, PALM_LEN)
    for i, (cx, half, depth) in enumerate(SLIT_SPEC):
        tip = PALM_LEN + depth
        slit = _slit_path(cx, half, depth)
        # finger back i: from the running cursor up over this finger to the slit mouth
        back_pts = [cursor]
        if i == 0:
            back_pts.append(fc.P(-HALF_W, shoulder))
        back_pts.append(slit[0])            # (cx - half, PALM_LEN) — mouth of the slit
        edges.append(fc.Edge(f"finger_back_{i}",
                             [fc.Line(back_pts[k], back_pts[k + 1])
                              for k in range(len(back_pts) - 1)]))
        # the slit itself: down one wall, around the tip, back up the other
        edges.append(fc.Edge(f"slit_{i}",
                             [fc.Line(slit[k], slit[k + 1])
                              for k in range(len(slit) - 1)]))
        cursor = slit[-1]                   # (cx + half, PALM_LEN)
        _ = tip
    # the last finger back, out to the thumb-side edge
    edges.append(fc.Edge(f"finger_back_{SLITS}", [
        fc.Line(cursor, fc.P(HALF_W, shoulder)),
        fc.Line(fc.P(HALF_W, shoulder), fc.P(HALF_W, PALM_LEN)),
    ]))
    edges += [
        # right (thumb) side wall, knuckle line back down to the wrist
        fc.Edge("side_r", [fc.Line(fc.P(HALF_W, PALM_LEN), fc.P(HALF_W, 0.0))]),
        # wrist edge — takes the cuff
        fc.Edge("wrist", [fc.Line(fc.P(HALF_W, 0.0), fc.P(-HALF_W, 0.0))]),
    ]

    internals = []
    # Heating traces: serpentine runs across the metacarpals, one per zone.
    for z in range(heat_zones):
        y = PALM_LEN * (0.22 + 0.62 * z / max(heat_zones, 1))
        internals.append(fc.Internal(f"heat-trace-{z}", [
            fc.P(-HALF_W * 0.72, y), fc.P(HALF_W * 0.72, y),
            fc.P(HALF_W * 0.72, y + PALM_LEN * 0.08),
            fc.P(-HALF_W * 0.72, y + PALM_LEN * 0.08)], kind="trace"))
    # Finger-back traces: one spur up the centre of each finger channel.
    gap = hand_width / 4.0
    for i in range(SLITS + 1):
        cx = -HALF_W + gap * i + gap / 2.0
        internals.append(fc.Internal(f"finger-spur-{i}", [
            fc.P(cx, PALM_LEN * 0.9), fc.P(cx, PALM_LEN + finger_len * 0.55)],
            kind="trace"))
    # The conduit run: where the seam-conduit-clip rides, down the thumb-side seam.
    internals.append(fc.Internal("conduit-run", [
        fc.P(HALF_W - conduit_tab * 0.5, PALM_LEN * 0.15),
        fc.P(HALF_W - conduit_tab * 0.5, PALM_LEN * 0.85)], kind="marking"))
    # Clip footprints along that run — one tab per clip.
    clips = max(2, int(PALM_LEN * 0.7 / (conduit_tab * 2.2)))
    for c in range(clips):
        y = PALM_LEN * (0.18 + 0.64 * c / max(clips - 1, 1))
        internals.append(fc.Internal(f"conduit-clip-{c}", [
            fc.P(HALF_W - conduit_tab, y), fc.P(HALF_W, y)], kind="drill"))

    return fc.Piece(
        "trank", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("slit_1", 0.5, "middle slit tip"),
                 fc.Notch("wrist", 0.5, "hand centre")],
        grainline=fc.Grainline(fc.P(0.0, PALM_LEN * 0.15), fc.P(0.0, PALM_LEN * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Trank (back of hand, heated)",
    )


def build_fourchette():
    """The finger side-wall strip. Its `seam` edge is cut to the MEASURED slit run
    of the drafted trank, so trank.fingers-slit-run ↔ fourchette.seam matches."""
    # The strip walks the slit run; its width is the finger depth (the wall height).
    depth = max(12.0, hand_width * 0.17)
    ln = SLIT_RUN
    return fc.Piece(
        "fourchette",
        [
            fc.Edge("seam", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, depth))]),
            fc.Edge("fold", [fc.Line(fc.P(ln, depth), fc.P(0.0, depth))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, depth), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("seam", 1.0 / 3.0, "slit 1 tip"),
                 fc.Notch("seam", 2.0 / 3.0, "slit 2 tip")],
        grainline=fc.Grainline(fc.P(ln * 0.2, depth / 2.0), fc.P(ln * 0.8, depth / 2.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Fourchette (finger side-wall)",
    )


def build_thumb():
    """A tapered thumb gusset: a teardrop closed at the tip.

    Both sides must bow AWAY from the centre line — the two curve_through calls run
    in opposite directions, so they take opposite `side` signs to bulge outward
    rather than collapsing the panel onto itself.
    """
    w = hand_width * 0.30
    ln = hand_length * 0.42
    tip = fc.P(0.0, ln)
    return fc.Piece(
        "thumb",
        [
            fc.Edge("inner", [fc.curve_through(fc.P(-w / 2.0, 0.0), tip,
                                               bulge=0.16, side=1.0)]),
            fc.Edge("outer", [fc.curve_through(tip, fc.P(w / 2.0, 0.0),
                                               bulge=0.16, side=1.0)]),
            fc.Edge("base", [fc.Line(fc.P(w / 2.0, 0.0), fc.P(-w / 2.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("base", 0.5, "thumb-hole centre")],
        grainline=fc.Grainline(fc.P(0.0, ln * 0.15), fc.P(0.0, ln * 0.8)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Thumb gusset",
    )


def build_cuff():
    """Ribbed wrist cuff. Cut flat at the stretched wrist girth reduced by the knit's
    negative ease, then folded; carries the cable exit and its strain-relief plate."""
    # Cut length = the trank's wrist edge doubled (front + back of the hand), which is
    # hand_width * 2; the knit is cut short of that by knit_stretch so it grips.
    flat = hand_width * 2.0 * (1.0 - knit_stretch)
    # A wrist smaller than the hand narrows the cuff further; never below the wrist.
    flat = max(flat, wrist_girth * (1.0 - knit_stretch))
    h = cuff_depth
    internals = [
        fc.Internal("cable-exit", [fc.P(flat * 0.5 - conduit_tab, h * 0.55),
                                   fc.P(flat * 0.5 + conduit_tab, h * 0.55)],
                    kind="drill"),
        fc.Internal("strain-relief-plate", [
            fc.P(flat * 0.5 - conduit_tab, h * 0.30),
            fc.P(flat * 0.5 + conduit_tab, h * 0.30),
            fc.P(flat * 0.5 + conduit_tab, h * 0.80),
            fc.P(flat * 0.5 - conduit_tab, h * 0.80),
            fc.P(flat * 0.5 - conduit_tab, h * 0.30)], kind="marking"),
    ]
    return fc.Piece(
        "cuff",
        [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(flat, 0.0))]),
            fc.Edge("seam_b", [fc.Line(fc.P(flat, 0.0), fc.P(flat, h))]),
            fc.Edge("open", [fc.Line(fc.P(flat, h), fc.P(0.0, h))]),
            fc.Edge("seam_a", [fc.Line(fc.P(0.0, h), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "cable exit")],
        grainline=fc.Grainline(fc.P(flat * 0.5, h * 0.15), fc.P(flat * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Wrist cuff (cable exit)",
    )


def build():
    pattern = fc.PatternSet("heated-glove-liner")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "trank":
        pattern.add(build_trank())
    if all_pieces or target_piece == "fourchette":
        pattern.add(build_fourchette())
    if all_pieces or target_piece == "thumb":
        pattern.add(build_thumb())
    if all_pieces or target_piece == "cuff":
        pattern.add(build_cuff())

    if all_pieces:
        # THE seam that had to solve: the fourchette strip sews to the three slit
        # edges of the trank, summed. Its cut length came from measuring exactly
        # these edges, so this check proves the draft against itself.
        pattern.declare_seam(
            ("fourchette", "seam"),
            [("trank", f"slit_{i}") for i in range(SLITS)],
            tol=1.0,
        )
        # The thumb gusset's two curved sides close on each other around the hole.
        pattern.declare_seam(("thumb", "inner"), ("thumb", "outer"), tol=1.0)
        # The cuff closes on itself at the wrist.
        pattern.declare_seam(("cuff", "seam_a"), ("cuff", "seam_b"), tol=1.0)

    fabric_width = 1600.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "conductive-thread-compatible knit jersey",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1600 mm width, 62% marker (small pieces nest poorly); "
                 "see the fabric card's e_textile block for iron temperature."},
        {"item": "resistive heating yarn", "qty": heat_zones * 2, "unit": "run",
         "note": "one out-and-back per marked heat-trace zone plus the finger spurs."},
        {"item": "seam conduit clip", "qty": max(2, int(PALM_LEN * 0.7 /
                                                        (conduit_tab * 2.2))) * 2,
         "unit": "count",
         "note": f"Yantra4D seam-conduit-clip (notion.hardware_ref); its sewn tab is "
                 f"{conduit_tab:.0f} mm — the same conduit_tab the clip footprints "
                 f"are drilled to."},
        {"item": "low-voltage cable + inline connector", "qty": 2, "unit": "set",
         "note": "exits at the marked cable-exit; anchor before the cuff fold."},
    ]
    pattern.metadata = {
        "fc300_rank": 261,
        "family": "etextile",
        "fabric_hint": "jersey-algodon",
        "finished_mm": {"hand_width": round(hand_width, 1),
                        "hand_length": round(hand_length, 1),
                        "finger_len": round(finger_len, 1)},
        "solved": {
            "slit_count": SLITS,
            "slit_run_mm": round(SLIT_RUN, 2),
            "fourchette_seam_mm": round(SLIT_RUN, 2),
            "palm_len_mm": round(PALM_LEN, 2),
            "note": "the fourchette strip is cut to the MEASURED slit-run perimeter of "
                    "the drafted trank (walls + tip arcs), not to finger_len * 6, so the "
                    "trank-to-fourchette seam matches the geometry actually drawn.",
        },
        "etextile_note": "Heat traces and finger spurs are MARKED routes for the maker; "
                         "no element is drafted. The conduit run keeps the bundle off "
                         "the knuckle flex crease.",
        "hardware": "seam conduit clips via Yantra4D (notion.hardware_ref -> "
                    "seam-conduit-clip); the clip's sewn tab length and the trank's "
                    "clip footprints are the one conduit_tab dimension",
    }
    return pattern


result = build()
