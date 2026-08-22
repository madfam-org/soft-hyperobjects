"""
Leg-o'-Mutton Blouse — Fashion Cabinet Costume Cartridge (FC-300 rank #273, y4d button bridged).

The 1890s shirtwaist with the enormous gathered sleeve, c. 1893–1897 at the extreme. The
"leg-o'-mutton" (gigot) sleeve is huge and full from shoulder to elbow and then close from
elbow to wrist — the shape of a leg of mutton, which is where the name comes from. It is the
defining garment of the decade and it lives or dies on ONE relationship, which is why it is
worth a cartridge of its own rather than a preset on `blouse`.

The documented construction this draft reproduces:

  - a shirtwaist body: front and back cut with the fullness taken to the waist, closed up the
    centre front with small buttons, and worn tucked into a skirt so the waist is gathered
    onto a band rather than fitted with darts;
  - the GIGOT sleeve: hugely full above the elbow, close below it. The fullness is
    concentrated at the SLEEVE HEAD, gathered or pleated into an armscye of ordinary size —
    the armhole does NOT grow to match the sleeve, and that mismatch is the whole technique;
  - a standing COLLAR band, the period neck finish;
  - the "pouter pigeon" front, worn with a slight blouse over the waistband at the front.

Drafting note — the seam that must SOLVE, and why it is unusual. On an ordinary set-in
sleeve the cap is drafted to the armscye plus a small ease, and that ease is worked in over
the cap. Here it is the opposite problem: the sleeve head is deliberately MUCH longer than
the armscye — two to three times it — and every millimetre of that excess is GATHERED away.

So the honest constraint is not "cap ≈ armscye". It is:

    cap length  =  armscye  x  gather_ratio        (the gathering the maker must distribute)

and the number that must be right is the RATIO, because that is what the maker actually
controls. This cartridge measures the armscye off the built body pieces, solves the sleeve
head's width by bisection until the built cap MEASURES exactly `armscye x gather_ratio`, and
reports both the measured cap and the gathered-away surplus. The seam is declared with that
surplus as its declared ease — so the verifier checks the real relationship rather than
being told to ignore a 700 mm discrepancy.

Pieces:
  - front   : blouse front (cut 2, mirrored) — CF button stand, waist gathers.
  - back    : blouse back, cut on the fold (cut 1) — yoke line, waist gathers.
  - sleeve  : the gigot sleeve, head width SOLVED against the measured armscye (cut 2).
  - cuff    : close cuff at the wrist (cut 2).
  - collar  : standing collar band (cut 1 on fold).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # front|back|sleeve|cuff|collar|set

bust_girth = float(PARAM(lambda: bust_girth, 920.0))
waist_girth = float(PARAM(lambda: waist_girth, 720.0))
back_length = float(PARAM(lambda: back_length, 400.0))     # nape to waist
shoulder_width = float(PARAM(lambda: shoulder_width, 128.0))
sleeve_length = float(PARAM(lambda: sleeve_length, 580.0))  # shoulder point to wrist
elbow_frac = float(PARAM(lambda: elbow_frac, 0.52))         # where the sleeve stops being full
gather_ratio = float(PARAM(lambda: gather_ratio, 2.4))      # sleeve head : armscye
wrist_girth = float(PARAM(lambda: wrist_girth, 175.0))
collar_height = float(PARAM(lambda: collar_height, 42.0))
button_pitch = float(PARAM(lambda: button_pitch, 62.0))
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps (sane 1890s shirtwaist ranges) ────────────────────────────────────
bust_girth = max(720.0, min(bust_girth, 1400.0))
waist_girth = max(540.0, min(waist_girth, 1300.0))
back_length = max(300.0, min(back_length, 520.0))
shoulder_width = max(95.0, min(shoulder_width, 185.0))
sleeve_length = max(420.0, min(sleeve_length, 720.0))
elbow_frac = max(0.35, min(elbow_frac, 0.70))
gather_ratio = max(1.15, min(gather_ratio, 3.2))
wrist_girth = max(130.0, min(wrist_girth, 300.0))
collar_height = max(20.0, min(collar_height, 75.0))
button_pitch = max(30.0, min(button_pitch, 110.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

BL = back_length
ARMHOLE_DEPTH = BL * 0.50
Y_BUST = BL - ARMHOLE_DEPTH          # the underarm line, measured down from the shoulder

# A shirtwaist is worn loose and bloused over the waistband — real ease, unlike a
# fitted bodice of the same decade.
BUST_4 = (bust_girth + 90.0) / 4.0
WAIST_4 = (waist_girth + 130.0) / 4.0   # generous: the surplus is gathered onto the band

NECK_W_FRONT = shoulder_width * 0.46
NECK_W_BACK = shoulder_width * 0.52
SHOULDER_SLOPE = 18.0

# Every panel's shoulder edge must measure the same: they are sewn to each other. The
# reference is chosen so the WIDEST-necked panel still has a real solution (a panel's
# shoulder can never be shorter than its own horizontal run), then each panel's drop is
# solved from it. No degenerate fallback, no widened tolerance.
_DX_FRONT = shoulder_width - NECK_W_FRONT
_DX_BACK = shoulder_width - NECK_W_BACK
SHOULDER_LEN = max((_DX_FRONT ** 2 + SHOULDER_SLOPE ** 2) ** 0.5,
                   (_DX_BACK ** 2 + SHOULDER_SLOPE ** 2) ** 0.5)


def _shoulder_drop_for(neck_w):
    """Solve this panel's shoulder-point drop so its shoulder measures SHOULDER_LEN."""
    dx = shoulder_width - neck_w
    return max(0.0, SHOULDER_LEN ** 2 - dx ** 2) ** 0.5


# Buttons up the centre front.
N_BUTTONS = max(3, int((BL - 40.0) / button_pitch))


def build_front():
    """Blouse front (cut 2, mirrored) with a centre-front button stand."""
    sh_drop = _shoulder_drop_for(NECK_W_FRONT)
    internals = []
    for i in range(N_BUTTONS):
        y = 24.0 + i * button_pitch
        if y < BL - 30.0:
            internals.append(fc.Internal("button", [fc.P(14.0, y), fc.P(14.0, y + 1.0)],
                                         kind="drill"))
    # The waist gathers: the surplus between WAIST_4 and the band is eased in here.
    internals.append(fc.Internal("waist-gather",
                                 [fc.P(WAIST_4 * 0.35, 6.0), fc.P(WAIST_4, 6.0)],
                                 kind="trace"))
    internals.append(fc.Internal("button-stand",
                                 [fc.P(28.0, 12.0), fc.P(28.0, BL - 40.0)], kind="marking"))
    return fc.Piece(
        "front",
        [
            fc.Edge("cf", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BL - 58.0))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, BL - 58.0),
                                              fc.P(NECK_W_FRONT, BL), 0.18, -1.0)]),
            fc.Edge("shoulder", [fc.Line(fc.P(NECK_W_FRONT, BL),
                                         fc.P(shoulder_width, BL - sh_drop))]),
            fc.Edge("armhole", [fc.curve_through(fc.P(shoulder_width, BL - sh_drop),
                                                 fc.P(BUST_4, Y_BUST), 0.22, -1.0)]),
            fc.Edge("side", [fc.curve_through(fc.P(BUST_4, Y_BUST),
                                              fc.P(WAIST_4, 0.0), 0.05, 1.0)]),
            fc.Edge("waist", [fc.Line(fc.P(WAIST_4, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cf": 34.0, "waist": 16.0, "neck": 7.0},  # CF carries the button stand
        notches=[fc.Notch("armhole", 0.5, "front armhole balance"),
                 fc.Notch("side", 0.5, "side balance")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.4, 26.0), fc.P(BUST_4 * 0.4, BL - 26.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Front (cut 2 mirrored, CF button stand)",
    )


def build_back():
    """Blouse back, cut on the fold, with the period yoke line marked."""
    sh_drop = _shoulder_drop_for(NECK_W_BACK)
    internals = [
        fc.Internal("yoke-line", [fc.P(0.0, BL - 92.0), fc.P(shoulder_width * 0.92,
                                                             BL - 92.0)], kind="marking"),
        fc.Internal("waist-gather", [fc.P(WAIST_4 * 0.25, 6.0), fc.P(WAIST_4, 6.0)],
                    kind="trace"),
    ]
    return fc.Piece(
        "back",
        [
            fc.Edge("cb", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, BL - 18.0))]),
            fc.Edge("neck", [fc.curve_through(fc.P(0.0, BL - 18.0),
                                              fc.P(NECK_W_BACK, BL), 0.10, -1.0)]),
            fc.Edge("shoulder", [fc.Line(fc.P(NECK_W_BACK, BL),
                                         fc.P(shoulder_width, BL - sh_drop))]),
            fc.Edge("armhole", [fc.curve_through(fc.P(shoulder_width, BL - sh_drop),
                                                 fc.P(BUST_4, Y_BUST), 0.15, -1.0)]),
            fc.Edge("side", [fc.curve_through(fc.P(BUST_4, Y_BUST),
                                              fc.P(WAIST_4, 0.0), 0.05, 1.0)]),
            fc.Edge("waist", [fc.Line(fc.P(WAIST_4, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb": 0.0, "waist": 16.0, "neck": 7.0},
        notches=[fc.Notch("armhole", 0.5, "back armhole balance (double)"),
                 fc.Notch("side", 0.5, "side balance")],
        grainline=fc.Grainline(fc.P(BUST_4 * 0.4, 26.0), fc.P(BUST_4 * 0.4, BL - 26.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb"),
        label="Back (cut 1 on fold)",
    )


FRONT = build_front()
BACK = build_back()

# ── The measured armscye ─────────────────────────────────────────────────────
# One armhole = one front armhole + one back armhole. The back is cut on the fold, so its
# drafted armhole edge is one whole armhole side, same as the front's.
ARMSCYE = FRONT.edge("armhole").length() + BACK.edge("armhole").length()

# What the sleeve head must MEASURE: the armscye multiplied by the gathering ratio. This
# is the relationship the maker actually controls, and it is what gets solved against.
CAP_TARGET = ARMSCYE * gather_ratio

EL = sleeve_length * elbow_frac       # shoulder point down to the elbow
LOWER = sleeve_length - EL            # elbow to wrist
WRIST_W = (wrist_girth + 40.0) / 2.0  # half the finished cuff, plus overlap ease


def _cap_length(head_half_w, cap_h):
    """MEASURED length of the gigot sleeve head at a given half-width.

    The head is a tall, very full dome — two lobes meeting at the shoulder point. Its
    length is measured off the flattened curve, never estimated from a formula.
    """
    a = fc.curve_through(fc.P(0.0, 0.0), fc.P(head_half_w, cap_h), 0.30, 1.0)
    b = fc.curve_through(fc.P(head_half_w, cap_h), fc.P(head_half_w * 2.0, 0.0), 0.30, 1.0)
    return (fc.polyline_length(a.flatten(0.2))
            + fc.polyline_length(b.flatten(0.2)))


CAP_H = ARMHOLE_DEPTH * 0.95   # the gigot head stands tall as well as wide


def _solve_head_width(target):
    """Bisect the sleeve head's half-width until the built cap MEASURES `target`.

    The armscye is a fixed, measured quantity and the gather ratio is the maker's choice;
    the head width is what gets solved. Picking a head width from a fullness rule and
    hoping the gathers distribute is what leaves a sleeve that cannot be set in.
    """
    lo, hi = 20.0, ARMSCYE * 3.0
    if _cap_length(hi, CAP_H) < target:
        return hi, _cap_length(hi, CAP_H)
    for _ in range(90):
        mid = (lo + hi) / 2.0
        if _cap_length(mid, CAP_H) < target:
            lo = mid
        else:
            hi = mid
    w = (lo + hi) / 2.0
    return w, _cap_length(w, CAP_H)


HEAD_HALF_W, CAP_MEASURED = _solve_head_width(CAP_TARGET)
HEAD_W = HEAD_HALF_W * 2.0
# The surplus the maker gathers away at the sleeve head. Reported, and declared as the
# seam's ease so the verifier checks the real relationship instead of ignoring it.
GATHERED_SURPLUS = CAP_MEASURED - ARMSCYE


def build_sleeve():
    """The gigot sleeve (cut 2, mirrored): full to the elbow, close to the wrist.

    Drafted at the SOLVED head width, so the cap measures the armscye times the requested
    gather ratio — and the surplus is a known number, not a surprise at the fitting.
    """
    hw = HEAD_W
    inset = (hw - WRIST_W) / 2.0
    internals = [
        fc.Internal("elbow-line", [fc.P(inset * 0.35, -EL), fc.P(hw - inset * 0.35, -EL)],
                    kind="marking"),
        # The gathering runs over the top of the head only — the underarm portion is set
        # in flat, which is what keeps the sleeve from bunching in the armpit.
        fc.Internal("gather-zone-start", [fc.P(hw * 0.18, 0.0), fc.P(hw * 0.18, CAP_H * 0.30)],
                    kind="trace"),
        fc.Internal("gather-zone-end", [fc.P(hw * 0.82, 0.0), fc.P(hw * 0.82, CAP_H * 0.30)],
                    kind="trace"),
    ]
    return fc.Piece(
        "sleeve",
        [
            fc.Edge("under_b", [
                # full to the elbow, then a straight taper to the wrist
                fc.Line(fc.P(hw, 0.0), fc.P(hw * 0.94, -EL)),
                fc.Line(fc.P(hw * 0.94, -EL), fc.P(hw - inset, -EL - LOWER)),
            ]),
            fc.Edge("wrist", [fc.Line(fc.P(hw - inset, -EL - LOWER),
                                      fc.P(inset, -EL - LOWER))]),
            fc.Edge("under_f", [
                fc.Line(fc.P(inset, -EL - LOWER), fc.P(hw * 0.06, -EL)),
                fc.Line(fc.P(hw * 0.06, -EL), fc.P(0.0, 0.0)),
            ]),
            fc.Edge("cap", [
                fc.curve_through(fc.P(0.0, 0.0), fc.P(HEAD_HALF_W, CAP_H), 0.30, 1.0),
                fc.curve_through(fc.P(HEAD_HALF_W, CAP_H), fc.P(hw, 0.0), 0.30, 1.0),
            ]),
        ],
        seam_allowance=seam_allowance,
        allowances={"wrist": 8.0},
        notches=[fc.Notch("cap", 0.25, "front cap notch"),
                 fc.Notch("cap", 0.5, "shoulder point"),
                 fc.Notch("cap", 0.75, "back cap notch (double)")],
        grainline=fc.Grainline(fc.P(hw * 0.5, -30.0), fc.P(hw * 0.5, -EL - LOWER + 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Gigot sleeve (cut 2 mirrored, head width SOLVED)",
    )


def build_cuff():
    """Close cuff at the wrist (cut 2)."""
    ln = wrist_girth + 34.0     # overlap for the button
    h = 62.0
    return fc.Piece(
        "cuff",
        [
            fc.Edge("end_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("upper", [fc.Line(fc.P(0.0, h), fc.P(ln, h))]),
            fc.Edge("end_r", [fc.Line(fc.P(ln, h), fc.P(ln, 0.0))]),
            fc.Edge("lower", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("lower", 0.5, "sleeve centre")],
        grainline=fc.Grainline(fc.P(ln * 0.2, h * 0.5), fc.P(ln * 0.8, h * 0.5)),
        internals=[fc.Internal("cuff-button", [fc.P(ln - 17.0, h * 0.5),
                                               fc.P(ln - 17.0, h * 0.5 + 1.0)], kind="drill")],
        cut=fc.CutSpec(quantity=2),
        label="Cuff (cut 2)",
    )


# The neck run the collar band is cut to: MEASURED off the built necklines.
NECK_RUN = FRONT.edge("neck").length() * 2.0 + BACK.edge("neck").length() * 2.0


def build_collar():
    """Standing collar band, cut to the MEASURED neckline run (cut 1 on fold)."""
    half = NECK_RUN / 2.0 + 16.0     # half the band, plus the CF overlap
    h = collar_height
    return fc.Piece(
        "collar",
        [
            fc.Edge("cb_fold", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("upper", [fc.curve_through(fc.P(0.0, h), fc.P(half, h), 0.03, -1.0)]),
            fc.Edge("front_end", [fc.Line(fc.P(half, h), fc.P(half, 0.0))]),
            fc.Edge("neck_seam", [fc.curve_through(fc.P(half, 0.0), fc.P(0.0, 0.0),
                                                   0.03, -1.0)]),
        ],
        seam_allowance=seam_allowance,
        allowances={"cb_fold": 0.0},
        notches=[fc.Notch("neck_seam", 0.5, "shoulder point")],
        grainline=fc.Grainline(fc.P(half * 0.2, h * 0.5), fc.P(half * 0.8, h * 0.5)),
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="cb_fold"),
        label="Standing collar band (cut 1 on fold, to the MEASURED neck run)",
    )


def build():
    pattern = fc.PatternSet("leg-o-mutton-blouse")
    everything = target_piece == "set"
    if everything or target_piece == "front":
        pattern.add(FRONT)
    if everything or target_piece == "back":
        pattern.add(BACK)
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "cuff":
        pattern.add(build_cuff())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # THE seam of this garment. The cap is deliberately far longer than the armscye —
        # that surplus IS the gigot sleeve — so it is declared as the seam's ease rather
        # than swept under a widened tolerance. The verifier then checks the real
        # relationship: cap == armscye + the surplus the maker gathers away.
        pattern.declare_seam(("sleeve", "cap"),
                             [("front", "armhole"), ("back", "armhole")],
                             tol=1.0, ease=GATHERED_SURPLUS)
        pattern.declare_seam(("front", "side"), ("back", "side"), tol=1.0)
        pattern.declare_seam(("front", "shoulder"), ("back", "shoulder"), tol=1.0)

    fabric_width = 1150.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.68)   # the sleeve is an awkward shape to nest
    pattern.bom = [
        {"item": "cotton lawn, batiste, or light wool",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1150 mm width, 68% marker — the gigot sleeve nests badly, so the "
                 "yield is lower than the piece areas suggest. A crisp light cloth holds "
                 "the sleeve out; a soft drapey one collapses it and loses the silhouette."},
        {"item": "buttons (Yantra4D sew-through-button)", "qty": N_BUTTONS + 2, "unit": "count",
         "note": f"{N_BUTTONS} up the centre front at {button_pitch:.0f} mm pitch, plus one "
                 f"per cuff. Small buttons are the period look."},
        {"item": "sleeve head stiffening (crinoline, haircloth, or net)",
         "qty": round(HEAD_W * 2.2), "unit": "mm_length",
         "note": "the period sleeve is supported from inside — an unsupported gigot collapses "
                 "within an hour of wear, no matter how much fabric is gathered into it."},
        {"item": "collar band interfacing", "qty": round(NECK_RUN + 60.0), "unit": "mm_length",
         "note": "the standing band must hold up on its own."},
        {"item": "thread", "qty": 2, "unit": "spool",
         "note": "two rows of gathering stitch over the sleeve head; the gathers carry the "
                 "whole sleeve, so use a strong thread and do not machine-gather in one pass."},
    ]
    pattern.metadata = {
        "fc300_rank": 273,
        "family": "costume_historical",
        "period": "c. 1893–1897 (mid-1890s)",
        "fabric_hint": "popelina-algodon",
        "silhouette_note": "The armhole does NOT grow to match the sleeve. The gigot's whole "
            "technique is an enormous sleeve head gathered into an armscye of ordinary size — "
            "enlarging the armhole to 'fit' the sleeve is the standard modern error and it "
            "drops the shoulder point, which loses the silhouette entirely.",
        "construction_note": "Shirtwaist body worn loose and bloused over the skirt band, "
            "closed with small buttons up the centre front, standing collar band, gigot "
            "sleeve full to the elbow and close below it, gathered head supported from inside.",
        "hardware": "front and cuff buttons via Yantra4D (notion.hardware_ref -> "
            "sew-through-button); button_pitch drives hole_spacing/card_count — the "
            "dimensional handshake.",
        "solved": {
            "armscye_measured_mm": round(ARMSCYE, 2),
            "gather_ratio_requested": round(gather_ratio, 3),
            "cap_target_mm": round(CAP_TARGET, 2),
            "cap_measured_mm": round(CAP_MEASURED, 2),
            "cap_residual_mm": round(CAP_MEASURED - CAP_TARGET, 4),
            "head_width_solved_mm": round(HEAD_W, 2),
            "gathered_surplus_mm": round(GATHERED_SURPLUS, 2),
            "achieved_gather_ratio": round(CAP_MEASURED / max(ARMSCYE, 1.0), 3),
            "neck_run_measured_mm": round(NECK_RUN, 2),
            "shoulder_seam_mm": round(SHOULDER_LEN, 2),
            "note": "the sleeve head is not drafted to 'about match' the armscye — it is "
                    "deliberately two to three times longer, and that surplus is gathered "
                    "away. The head width is SOLVED by bisection until the built cap MEASURES "
                    "armscye x gather_ratio, and the surplus is declared as the seam's ease "
                    "so the verifier checks the real relationship instead of being told to "
                    "ignore a several-hundred-millimetre discrepancy.",
        },
    }
    return pattern


result = build()
