"""
Tudor Kirtle — Fashion Cabinet Costume Cartridge (FC-300 rank #271, y4d eyelet bridged).

The fitted kirtle of the 16th century, c. 1500–1560. The kirtle is the supportive gown worn
over the smock and under the outer gown, and it is the garment that does the WORK: in the
16th century the bust support comes from a stiffened, close-laced kirtle bodice, not from a
separate foundation garment. There is no bra underneath, and drafting one in is the standard
modern error.

The documented construction this draft reproduces:

  - a bodice STIFFENED with boned or heavily-corded channels and laced closed, which is what
    supports the bust — the shaping is compressive and comes from the lacing, not from cups,
    darts, or a shaped bust seam;
  - a bodice and skirt made SEPARATELY and joined at a waist seam — unlike the medieval
    cotehardie, the Tudor kirtle does have a waist seam, and the skirt is a rectangle
    controlled onto the bodice waist by CARTRIDGE PLEATS rather than shaped by gores;
  - cartridge (organ-pipe) pleating, in which the skirt is gathered over a stiff roll so the
    pleats stand out from the waist as tubes rather than lying flat. This is why a Tudor
    skirt springs away from the body at the waist instead of hanging straight down;
  - front or back LACING through worked eyelets in a stiffened edge, spiral-laced.

Drafting note — the seam that must SOLVE. Cartridge pleating is a length problem, and it is
the one thing a kirtle draft can get provably wrong. The skirt is a flat rectangle of hem
width W; pleated up, it must reduce to exactly the bodice's waist run. Each pleat consumes
its pitch, so:

    pleats_that_fit  =  floor(W / pleat_pitch)
    pleated_length   =  pleats_that_fit * take_up_per_pleat

This cartridge does NOT assume the skirt width. It builds the bodice first, MEASURES the
bodice's waist edge off the built polygons, and then SOLVES the skirt rectangle's width by
bisection so that its pleated-up length equals that measured waist run. The number of whole
pleats is an integer, so the solve is done on the continuous width with the pleat count
rounded, then the residual is reported honestly rather than hidden.

Pieces:
  - bodice_front : stiffened front, cut on the fold (cut 1) — boning channels.
  - bodice_back  : stiffened back carrying the lacing (cut 2, mirrored).
  - skirt        : the pleated skirt panel, width SOLVED against the measured waist (cut 2).
  - strap        : shoulder strap, tied or pinned in the period manner (cut 2, mirrored).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # bodice_front|bodice_back|skirt|strap|set

bust_girth = float(PARAM(lambda: bust_girth, 940.0))
waist_girth = float(PARAM(lambda: waist_girth, 760.0))
bodice_length = float(PARAM(lambda: bodice_length, 340.0))   # shoulder strap seam to waist
skirt_length = float(PARAM(lambda: skirt_length, 980.0))     # waist to hem
pleat_pitch = float(PARAM(lambda: pleat_pitch, 26.0))        # cartridge-pleat spacing
pleat_takeup = float(PARAM(lambda: pleat_takeup, 7.0))       # waist run each pleat occupies
lacing_gap = float(PARAM(lambda: lacing_gap, 20.0))          # gap left between the laced edges
eyelet_pitch = float(PARAM(lambda: eyelet_pitch, 24.0))      # lacing eyelet spacing
bone_count = float(PARAM(lambda: bone_count, 6))             # boning channels per bodice half
seam_allowance = float(PARAM(lambda: seam_allowance, 12.0))

# ── Clamps (sane 16th-c kirtle ranges) ───────────────────────────────────────
bust_girth = max(700.0, min(bust_girth, 1400.0))
waist_girth = max(560.0, min(waist_girth, 1300.0))
bodice_length = max(220.0, min(bodice_length, 480.0))
skirt_length = max(600.0, min(skirt_length, 1400.0))
pleat_pitch = max(14.0, min(pleat_pitch, 55.0))
pleat_takeup = max(3.0, min(pleat_takeup, 18.0))
lacing_gap = max(0.0, min(lacing_gap, 80.0))
eyelet_pitch = max(14.0, min(eyelet_pitch, 45.0))
bone_count = int(max(2, min(bone_count, 14)))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# A pleat can never take up more waist than its own pitch — that would be a negative fold.
pleat_takeup = min(pleat_takeup, pleat_pitch * 0.75)

BL = bodice_length
SL = skirt_length

# The bodice is drafted in quarters around the torso. The kirtle is COMPRESSIVE: the bust
# is reduced onto the body by the lacing, so the bodice is drafted under the body measure.
BUST_4 = (bust_girth - 30.0) / 4.0 / 2.0     # half-width of one bodice quarter at the bust
WAIST_4 = (waist_girth - 40.0) / 4.0 / 2.0   # laced-in waist; the reduction is the point

# The back is split for the lacing, so half the gap comes off each back half.
BACK_INSET = lacing_gap / 2.0


def _bodice_side_edge(top_w, bot_w):
    """The shaped side edge from the underarm down to the waist.

    Curved, not straight: the kirtle's shaping is a smooth compressive taper, and a straight
    side seam on a boned bodice reads as a cone.
    """
    return [fc.curve_through(fc.P(top_w, BL), fc.P(bot_w, 0.0), 0.10, -1.0)]


def build_bodice_front():
    """Stiffened front, cut on the fold. Boning channels run vertically, waist to top edge."""
    internals = []
    for i in range(bone_count):
        t = (i + 1) / (bone_count + 1)
        x = BUST_4 * t
        internals.append(fc.Internal("boning-channel",
                                     [fc.P(x, 12.0), fc.P(x, BL - 12.0)], kind="marking"))
    return fc.Piece(
        "bodice_front",
        [
            fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BL))]),
            fc.Edge("top", [fc.curve_through(fc.P(0.0, BL), fc.P(BUST_4, BL), 0.07, -1.0)]),
            fc.Edge("side", _bodice_side_edge(BUST_4, WAIST_4)),
            fc.Edge("waist", [fc.Line(fc.P(WAIST_4, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cf": 0.0, "top": 8.0},
        notches=[fc.Notch("side", 0.5, "side balance"),
                 fc.Notch("waist", 0.5, "waist quarter")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.5, 18.0), fc.P(BUST_4 * 0.5, BL - 18.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cf"),
        label="Bodice front (cut 1 on fold, boned)",
    )


# How many lacing eyelets fit up the back edge, at the requested pitch.
N_EYELETS = max(4, int((BL - 40.0) / eyelet_pitch))


def build_bodice_back():
    """Stiffened back (cut 2, mirrored) carrying the lacing field at the centre-back edge."""
    internals = []
    for i in range(bone_count):
        t = (i + 1) / (bone_count + 1)
        x = BACK_INSET + (BUST_4 - BACK_INSET) * t
        internals.append(fc.Internal("boning-channel",
                                     [fc.P(x, 12.0), fc.P(x, BL - 12.0)], kind="marking"))
    for i in range(N_EYELETS):
        y = 20.0 + i * eyelet_pitch
        if y < BL - 12.0:
            internals.append(fc.Internal("lacing-eyelet",
                                         [fc.P(BACK_INSET + 9.0, y),
                                          fc.P(BACK_INSET + 9.0, y + 1.0)], kind="drill"))
    return fc.Piece(
        "bodice_back",
        [
            fc.Edge("cb", [fc.Line(fc.P(BACK_INSET, 0.0), fc.P(BACK_INSET, BL))]),
            fc.Edge("top", [fc.curve_through(fc.P(BACK_INSET, BL), fc.P(BUST_4, BL),
                                             0.05, -1.0)]),
            fc.Edge("side", _bodice_side_edge(BUST_4, WAIST_4)),
            fc.Edge("waist", [fc.Line(fc.P(WAIST_4, 0.0), fc.P(BACK_INSET, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": 18.0, "top": 8.0},  # the laced edge takes a stiffened turn-back
        notches=[fc.Notch("side", 0.5, "side balance"),
                 fc.Notch("waist", 0.5, "waist quarter")],
        grainline=fc.Grainline(fc.P((BACK_INSET + BUST_4) * 0.5, 18.0),
                               fc.P((BACK_INSET + BUST_4) * 0.5, BL - 18.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Bodice back (cut 2 mirrored, boned, laced)",
    )


BODICE_FRONT = build_bodice_front()
BODICE_BACK = build_bodice_back()

# The MEASURED waist run the skirt must be pleated onto. The bodice is a front on the fold
# (so its waist edge covers half the front) plus two backs — the full waist is:
#   2 x front waist edge  +  2 x back waist edge
WAIST_RUN = (BODICE_FRONT.edge("waist").length() * 2.0
             + BODICE_BACK.edge("waist").length() * 2.0)


def _pleated_length(width):
    """The waist run a flat skirt of `width` reduces to when cartridge-pleated.

    Whole pleats only — a half pleat is not a thing you can sew — so the count is floored,
    and the residual fabric beyond the last whole pleat is reported rather than pretended
    away.
    """
    n = int(width / pleat_pitch)
    return n * pleat_takeup, n


def _solve_skirt_width(target):
    """Bisect the flat skirt width so its pleated-up length equals the MEASURED waist run.

    The bodice waist is a fixed, measured quantity; the skirt is solved to match it. Doing
    it the other way round — picking a skirt width from a fullness ratio and hoping the
    pleats land — is what leaves a skirt that will not go onto the bodice.
    """
    lo, hi = pleat_pitch, target * (pleat_pitch / max(pleat_takeup, 0.5)) * 2.0 + pleat_pitch
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if _pleated_length(mid)[0] < target:
            lo = mid
        else:
            hi = mid
    # The pleat count is an INTEGER — a half pleat is not a thing you can sew — so the
    # continuous solve lands between two whole-pleat widths. Take whichever whole count
    # pleats up CLOSEST to the measured waist, rather than always rounding one way: the
    # residual is then at worst half a pleat's take-up, and it is eased in at the centre
    # back the way a period skirt is.
    n_lo = max(1, int(lo / pleat_pitch))
    best_n, best_err = n_lo, abs(n_lo * pleat_takeup - target)
    for n in (n_lo + 1, n_lo - 1):
        if n >= 1 and abs(n * pleat_takeup - target) < best_err:
            best_n, best_err = n, abs(n * pleat_takeup - target)
    return best_n * pleat_pitch, best_n


# The skirt is cut in TWO panels (front and back), so each carries half the solved width.
SKIRT_WIDTH_TOTAL, PLEAT_COUNT = _solve_skirt_width(WAIST_RUN)
# A skirt narrower than the waist it mounts to cannot exist. This only bites at extreme
# parameter combinations (a huge take-up against a tiny pitch); widen to whole pleat
# pitches until the flat width clears the waist run, so the piece stays cuttable.
while SKIRT_WIDTH_TOTAL < WAIST_RUN:
    PLEAT_COUNT += 1
    SKIRT_WIDTH_TOTAL = PLEAT_COUNT * pleat_pitch
PLEATED_LENGTH, PLEAT_COUNT = _pleated_length(SKIRT_WIDTH_TOTAL)
SKIRT_PANEL_W = SKIRT_WIDTH_TOTAL / 2.0


def build_skirt():
    """One skirt panel (cut 2). A rectangle — the fullness is made by pleating, not cutting.

    Its width is SOLVED, not chosen: half the total width whose cartridge-pleated length
    equals the measured bodice waist run.
    """
    w, h = SKIRT_PANEL_W, SL
    internals = []
    # Every pleat fold on this panel, marked at the true pitch. Cartridge pleats are gathered
    # on two or three parallel rows of running stitch, so the fold marks matter.
    n_here = int(w / pleat_pitch)
    for i in range(n_here):
        x = pleat_pitch * (i + 0.5)
        internals.append(fc.Internal("pleat-fold",
                                     [fc.P(x, h), fc.P(x, h - 55.0)], kind="marking"))
    # The gathering rows themselves.
    for row in (18.0, 34.0, 50.0):
        internals.append(fc.Internal("gathering-row",
                                     [fc.P(6.0, h - row), fc.P(w - 6.0, h - row)],
                                     kind="trace"))
    return fc.Piece(
        "skirt",
        [
            fc.Edge("seam_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("waist", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("seam_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("hem", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"hem": 45.0, "waist": 18.0},  # a deep hem weights the pleats down
        notches=[fc.Notch("waist", 0.25, "pleat quarter"),
                 fc.Notch("waist", 0.5, "pleat centre"),
                 fc.Notch("waist", 0.75, "pleat quarter")],
        grainline=fc.Grainline(fc.P(w * 0.5, 30.0), fc.P(w * 0.5, h - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2),
        label=f"Skirt panel (cut 2, {n_here} cartridge pleats each)",
    )


def build_strap():
    """Shoulder strap (cut 2, mirrored) — tied or pinned to the front in the period manner."""
    ln = BL * 0.85
    w = 44.0
    return fc.Piece(
        "strap",
        [
            fc.Edge("back_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("outer", [fc.curve_through(fc.P(0.0, w), fc.P(ln, w), 0.05, -1.0)]),
            fc.Edge("front_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("inner", [fc.curve_through(fc.P(ln, 0.0), fc.P(0.0, 0.0), 0.05, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"front_end": 20.0},  # extra to turn under for the tie or the pin
        notches=[fc.Notch("outer", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w * 0.5), fc.P(ln * 0.8, w * 0.5)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Shoulder strap (cut 2 mirrored)",
    )


def build():
    pattern = fc.PatternSet("tudor-kirtle")
    everything = target_piece == "set"
    if everything or target_piece == "bodice_front":
        pattern.add(BODICE_FRONT)
    if everything or target_piece == "bodice_back":
        pattern.add(BODICE_BACK)
    if everything or target_piece == "skirt":
        pattern.add(build_skirt())
    if everything or target_piece == "strap":
        pattern.add(build_strap())

    if everything:
        # The bodice side seams: front to back, both sides.
        pattern.declare_seam(("bodice_front", "side"), ("bodice_back", "side"), tol=1.0)
        # The skirt's side seams close the tube: panel to panel.
        pattern.declare_seam(("skirt", "seam_l"), ("skirt", "seam_r"), tol=1.0)

    fabric_width = 1000.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "wool or linen kirtle cloth",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1000 mm width, 72% marker. A firm wool holds the cartridge pleats "
                 "standing; a soft cloth lets them collapse flat, which is the wrong look."},
        {"item": "boning or heavy cording", "qty": bone_count * 3, "unit": "count",
         "note": f"{bone_count} channels per bodice half (front on the fold plus two backs). "
                 f"Period stock is whalebone, reed, or bundled cord — the bodice supports the "
                 f"bust by compression, so the channels must be filled, not decorative."},
        {"item": "lacing eyelets (Yantra4D garment-eyelet)", "qty": N_EYELETS * 2,
         "unit": "count",
         "note": f"{N_EYELETS} per back half at {eyelet_pitch:.0f} mm pitch, spiral-laced. "
                 f"Hand-worked thread eyelets are the period finish."},
        {"item": "lacing cord", "qty": round(BL * 2.6), "unit": "mm_length",
         "note": "one continuous cord — the period back is spiral-laced from the top, not "
                 "criss-crossed with two ends and a bow."},
        {"item": "linen thread", "qty": 2, "unit": "spool",
         "note": "two or three parallel rows of running stitch gather the cartridge pleats; "
                 "use a strong thread, because the whole skirt hangs from those rows."},
    ]
    pattern.metadata = {
        "fc300_rank": 271,
        "family": "costume_historical",
        "period": "c. 1500–1560 (Tudor)",
        "fabric_hint": "lana-peinada-traje",
        "silhouette_note": "The bust support comes from the stiffened, close-laced BODICE — "
            "there is no separate foundation garment and no bra underneath. The skirt springs "
            "away from the waist because the cartridge pleats stand out as tubes rather than "
            "lying flat; a skirt gathered flat onto the waist reads as a later garment.",
        "construction_note": "Bodice and skirt made separately and joined at a waist seam "
            "(unlike the medieval cotehardie, which has none). The skirt is a rectangle "
            "controlled onto the waist by cartridge pleats, not shaped by gores.",
        "hardware": "lacing eyelets via Yantra4D (notion.hardware_ref -> garment-eyelet); the "
            "eyelet pitch bounds flange_dia — the dimensional handshake.",
        "solved": {
            "waist_run_measured_mm": round(WAIST_RUN, 2),
            "skirt_width_solved_mm": round(SKIRT_WIDTH_TOTAL, 1),
            "skirt_panel_width_mm": round(SKIRT_PANEL_W, 1),
            "pleat_count": PLEAT_COUNT,
            "pleated_length_mm": round(PLEATED_LENGTH, 2),
            "pleat_residual_mm": round(PLEATED_LENGTH - WAIST_RUN, 2),
            "fullness_ratio": round(SKIRT_WIDTH_TOTAL / max(WAIST_RUN, 1.0), 3),
            "note": "the skirt width is SOLVED by bisection so its cartridge-pleated length "
                    "matches the MEASURED bodice waist run, then rounded down to a whole "
                    "number of pleat pitches. The residual is reported, not hidden: whole "
                    "pleats are an integer constraint, so the last fraction of a pleat is "
                    "eased at the centre back in the period manner.",
        },
    }
    return pattern


result = build()
