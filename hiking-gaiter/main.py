"""
Hiking Gaiter — Fashion Cabinet Garment Cartridge (FC-300 #235, technical & outdoor).

The full-height gaiter: a truncated-cone sleeve that wraps the boot top and the lower
leg to keep scree, snow, mud, and burrs out of the boot. It opens down the FRONT — a
lacing-hook column with an eyelet at each hook seat lets the wearer step in and cinch
the front closed over the laces — and it draws in at the TOP over the calf with a
cord run through a casing, stopped by a cord-lock. A boot-lace hook tab at the toe
end and an instep-strap channel at the base keep it from riding up.

The eyelet solid (the lacing-hook seat) and the cord-lock stopper are Yantra4D
territory (`garment-eyelet`; see the manifest's notion.hardware_ref). Fashion Cabinet
owns the sleeve: the cone that fits calf to boot, the front opening, the casing, the
hook column spacing. The eyelet's set-face flange is dimensioned from `hook_dia`, the
same parameter that drives this garment's `front_opening` interface — one dimension
flowing to both sewn edges.

Made to measure from ISO 8559 landmarks: `calf_girth` and `ankle_girth` set the two
ends of the cone; `gaiter_height` is the rise up the leg.

Pieces:
  - sleeve : the gaiter body (cut 2 — one per leg), front-opening column marked,
             top casing and instep channel marked.
  - strap  : the instep strap that passes under the boot arch (cut 2).

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
target_piece = str(PARAM(lambda: target_piece, "set"))     # sleeve|strap|set

calf_girth    = float(PARAM(lambda: calf_girth, 380.0))    # ISO 8559 calf girth
ankle_girth   = float(PARAM(lambda: ankle_girth, 250.0))   # ISO 8559 ankle girth
gaiter_height = float(PARAM(lambda: gaiter_height, 400.0))  # boot top to below the knee
boot_ease     = float(PARAM(lambda: boot_ease, 120.0))     # ease over the boot cuff
calf_ease     = float(PARAM(lambda: calf_ease, 60.0))      # ease over the trouser leg
hooks         = int(PARAM(lambda: hooks, 7))               # lacing hooks down the front
hook_dia      = float(PARAM(lambda: hook_dia, 9.0))        # eyelet/hook seat diameter
casing_depth  = float(PARAM(lambda: casing_depth, 26.0))   # top drawcord casing
strap_width   = float(PARAM(lambda: strap_width, 22.0))    # instep strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
calf_girth    = max(260.0, min(calf_girth, 560.0))
ankle_girth   = max(180.0, min(ankle_girth, 360.0))
gaiter_height = max(200.0, min(gaiter_height, 560.0))
boot_ease     = max(40.0, min(boot_ease, 220.0))
calf_ease     = max(20.0, min(calf_ease, 160.0))
hooks         = max(3, min(hooks, 14))
hook_dia      = max(5.0, min(hook_dia, 16.0))
casing_depth  = max(14.0, min(casing_depth, 45.0))
strap_width   = max(12.0, min(strap_width, 40.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

# The cone: the sleeve is cut flat as one panel whose two horizontal edges are the
# unrolled top (calf) and bottom (boot) circumferences. The front opening is the
# vertical gap, so the panel is the FULL circumference plus the front overlap.
H = gaiter_height
TOP_W = calf_girth + calf_ease          # unrolled calf circumference
BOT_W = ankle_girth + boot_ease         # unrolled boot-cuff circumference
OVERLAP = max(30.0, hook_dia * 4.0)     # front storm-flap overlap under the hooks
# Half-drafted: the panel is a symmetric trapezoid about x = 0, so the centre-back
# is the fold and the two front edges close over each other.
TOP_HALF = TOP_W / 2.0
BOT_HALF = BOT_W / 2.0
# Hook column pitch down the front edge (from the boot end up to the casing).
HOOK_RUN = H - casing_depth - 40.0
HOOK_PITCH = HOOK_RUN / max(1, hooks - 1) if hooks > 1 else HOOK_RUN


def build_sleeve():
    """The gaiter sleeve, drafted flat and cut on the centre-back fold.

    y = 0 is the boot end, y = H the calf end. x = 0 is the centre back (the fold);
    x grows toward the front opening, where the lacing-hook column sits.
    """
    internals = [
        # The top drawcord casing — the cord that the cord-lock stops runs here.
        fc.Internal("top-casing",
                    [fc.P(0.0, H - casing_depth), fc.P(TOP_HALF, H - casing_depth)],
                    kind="marking"),
        # The instep-strap channel at the boot end.
        fc.Internal("instep-channel",
                    [fc.P(0.0, 18.0), fc.P(BOT_HALF, 18.0)], kind="marking"),
        # The storm flap that sits under the hook column.
        fc.Internal("storm-flap-fold",
                    [fc.P(BOT_HALF - OVERLAP, 0.0), fc.P(TOP_HALF - OVERLAP, H)],
                    kind="fold"),
    ]
    # The lacing-hook seats: one eyelet drill per hook, marched up the front edge.
    for i in range(hooks):
        y = 30.0 + HOOK_PITCH * i
        t = y / H
        x = BOT_HALF + (TOP_HALF - BOT_HALF) * t - OVERLAP * 0.5
        r = hook_dia / 2.0
        internals.append(fc.Internal(
            "hook-seat",
            [fc.P(x - r, y), fc.P(x + r, y)], kind="drill"))

    return fc.Piece(
        "sleeve",
        [
            fc.Edge("center_back", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, H))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, H), fc.P(TOP_HALF, H))]),
            fc.Edge("front_opening", [fc.Line(fc.P(TOP_HALF, H), fc.P(BOT_HALF, 0.0))]),
            fc.Edge("boot_edge", [fc.Line(fc.P(BOT_HALF, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top": casing_depth, "boot_edge": 16.0},
        notches=[fc.Notch("front_opening", 0.0, "boot end of the hook column"),
                 fc.Notch("front_opening", 1.0, "casing end of the hook column"),
                 fc.Notch("top", 1.0, "cord exit")],
        grainline=fc.Grainline(fc.P(BOT_HALF * 0.4, 30.0), fc.P(TOP_HALF * 0.4, H - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, on_fold=True, fold_edge="center_back", mirror=True),
        label="Gaiter sleeve",
    )


def build_strap():
    """The instep strap: a webbing/self-fabric band that passes under the boot arch."""
    length = BOT_W * 0.9
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(length, 0.0))]),
            fc.Edge("end_b", [fc.Line(fc.P(length, 0.0), fc.P(length, strap_width))]),
            fc.Edge("top", [fc.Line(fc.P(length, strap_width), fc.P(0.0, strap_width))]),
            fc.Edge("end_a", [fc.Line(fc.P(0.0, strap_width), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", 0.5, "boot arch centre")],
        grainline=fc.Grainline(fc.P(length * 0.2, strap_width / 2.0),
                               fc.P(length * 0.8, strap_width / 2.0)),
        cut=fc.CutSpec(quantity=2),
        label="Instep strap",
    )


def build():
    pattern = fc.PatternSet("hiking-gaiter")
    everything = target_piece == "set"
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "strap":
        pattern.add(build_strap())
    if everything or target_piece == "sleeve":
        # Cut on the centre-back fold: the front opening closes over its own mirror
        # under the hook column — a balanced self-seam (join to join, never to fold).
        pattern.declare_seam(("sleeve", "front_opening"), ("sleeve", "front_opening"), tol=1.5)

    fabric_width = 1500.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.72)
    pattern.bom = [
        {"item": "coated nylon / ripstop (upper) + packcloth (boot end)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1500 mm width, 72% marker; a pair. Line the boot end for abrasion."},
        {"item": "lacing hooks + eyelets", "qty": hooks * 2, "unit": "count",
         "note": "Yantra4D garment-eyelet (see notion.hardware_ref) seats each front hook."},
        {"item": "drawcord + cord-lock", "qty": 1, "unit": "set",
         "note": "top casing cord; a Yantra4D cord-lock stops it over the calf."},
        {"item": "boot-lace hook + instep strap webbing", "qty": 1, "unit": "set",
         "note": "the toe hook and under-boot strap keep the gaiter from riding up."},
    ]
    pattern.metadata = {
        "fc300_rank": 235, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A full-height truncated-cone gaiter that wraps the boot top and "
            "lower leg: a front lacing-hook column to step in and cinch closed, a top drawcord "
            "casing stopped by a cord-lock, and an instep strap under the boot arch.",
        "solved": {"top_circumference_mm": round(TOP_W, 1),
                   "boot_circumference_mm": round(BOT_W, 1),
                   "hook_pitch_mm": round(HOOK_PITCH, 1),
                   "front_overlap_mm": round(OVERLAP, 1)},
        "hardware": "eyelet seats + cord-lock via Yantra4D "
                    "(notion.hardware_ref -> garment-eyelet)",
    }
    return pattern


result = build()
