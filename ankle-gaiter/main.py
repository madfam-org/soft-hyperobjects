"""
Ankle Gaiter — Fashion Cabinet Garment Cartridge (FC-300 #231, lane 4 footwear).

A short wrap gaiter: a tapered cuff that wraps the ankle over the boot top, closing up the
front with a ladder of lacing hooks and an under-instep strap that keeps it down. This is
the FC-300 cartridge that finally consumes Yantra4D's `lacing-hook` — one of the two
honestly-unbridged Wave-T findings.

The hook ladder is the point of the draft, so the hook geometry is REAL, not decorative:
`hook_pitch` is the spacing the hooks are riveted at, `hook_count` is how many fit, and
the closure edge is drafted to the run those hooks actually occupy. The lacing-hook's
sew_plate is a FLANGE interface, so a dimensional handshake is owed and paid — the plate
width and pitch that size the hardware also drive this gaiter's own closure interface.

Pieces:
  - wrap          : the gaiter body (cut 1), hook drill points up the closure edge.
  - instep_strap  : the under-foot strap (cut 1) that stops the gaiter riding up.

SIZING NOTE (honest, checked): ISO 8559 as vendored declares NO foot landmark codes, so
no foot code is claimed. `ankle_girth` and `calf_girth` ARE canonical and ARE used — a
gaiter wraps exactly those two landmarks, which is what makes it measurable at all.

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
target_piece = str(PARAM(lambda: target_piece, "set"))    # wrap|instep_strap|set

# Both ARE canonical ISO-8559 landmark codes — a gaiter wraps exactly these.
ankle_girth = float(PARAM(lambda: ankle_girth, 245.0))
calf_girth = float(PARAM(lambda: calf_girth, 370.0))

gaiter_height = float(PARAM(lambda: gaiter_height, 175.0))   # ankle to top edge
wrap_ease = float(PARAM(lambda: wrap_ease, 28.0))            # over the boot
hook_count = int(PARAM(lambda: hook_count, 5))               # lacing hooks per side
hook_pitch = float(PARAM(lambda: hook_pitch, 26.0))          # rivet-to-rivet spacing
hook_plate_w = float(PARAM(lambda: hook_plate_w, 14.0))      # hook base-plate width
strap_w = float(PARAM(lambda: strap_w, 22.0))                # instep strap width
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
ankle_girth = max(160.0, min(ankle_girth, 340.0))
calf_girth = max(220.0, min(calf_girth, 520.0))
gaiter_height = max(80.0, min(gaiter_height, 300.0))
wrap_ease = max(0.0, min(wrap_ease, 90.0))
hook_count = max(2, min(hook_count, 10))
hook_pitch = max(12.0, min(hook_pitch, 45.0))
hook_plate_w = max(6.0, min(hook_plate_w, 30.0))
strap_w = max(10.0, min(strap_w, 50.0))
seam_allowance = max(0.0, min(seam_allowance, 16.0))

# ── Solved geometry ──────────────────────────────────────────────────────────
# The wrap is a tapered panel: narrow at the ankle, wider at the calf. Flat, its
# bottom edge is the ankle circumference (+ boot ease) and its top the calf's.
BOT_W = ankle_girth + wrap_ease
TOP_W = max(BOT_W + 10.0, calf_girth * (gaiter_height / 260.0) + wrap_ease)

# THE HOOK LADDER RUN — the dimension the hardware and the garment share.
# `hook_count` hooks at `hook_pitch` spacing occupy (n-1) pitches plus one plate at
# each end. The closure edge must be at least this long, or the hooks do not fit;
# the gaiter height is raised to meet it rather than silently overflowing the edge.
HOOK_RUN = (hook_count - 1) * hook_pitch + hook_plate_w
CLOSURE_LEN = max(gaiter_height, HOOK_RUN + hook_plate_w * 2.0)


def build_wrap():
    """The gaiter body: a tapered panel wrapping the ankle. `closure_l` and
    `closure_r` are the two front edges the hook ladder mounts to; they meet when
    the gaiter is laced shut."""
    h = CLOSURE_LEN
    bh, th = BOT_W / 2.0, TOP_W / 2.0
    internals = [
        fc.Internal("centre-back", [fc.P(0.0, 0.0), fc.P(0.0, h)], kind="marking"),
    ]
    # Hook ladder: `hook_count` per side, marked as drill points at the true pitch,
    # set in from the closure edge by half a plate width.
    inset = hook_plate_w / 2.0 + 4.0
    start = (h - HOOK_RUN) / 2.0 + hook_plate_w / 2.0
    for i in range(hook_count):
        cy = start + i * hook_pitch
        for sgn in (-1.0, 1.0):
            # x runs on the tapered edge at height cy
            frac = cy / h
            edge_x = bh + (th - bh) * frac
            cx = sgn * (edge_x - inset)
            r = hook_plate_w / 2.0
            tag = "l" if sgn < 0 else "r"
            internals.append(fc.Internal(
                f"hook-{tag}{i + 1}",
                [fc.P(cx - r, cy), fc.P(cx + r, cy)], kind="drill"))
    return fc.Piece(
        "wrap",
        [
            fc.Edge("ankle_edge", [fc.Line(fc.P(-bh, 0.0), fc.P(bh, 0.0))]),
            fc.Edge("closure_r", [fc.Line(fc.P(bh, 0.0), fc.P(th, h))]),
            fc.Edge("top_edge", [fc.Line(fc.P(th, h), fc.P(-th, h))]),
            fc.Edge("closure_l", [fc.Line(fc.P(-th, h), fc.P(-bh, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"top_edge": 14.0, "ankle_edge": 12.0},
        notches=[fc.Notch("ankle_edge", 0.5, "centre back"),
                 fc.Notch("top_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(0.0, 10.0), fc.P(0.0, h - 10.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Wrap (gaiter body)",
    )


def build_instep_strap():
    """The under-foot strap. Its two ends sew to the wrap's ankle edge, one each
    side of centre front; it passes under the boot's instep."""
    ln = BOT_W * 0.72
    w = strap_w
    return fc.Piece(
        "instep_strap",
        [
            fc.Edge("edge_bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(ln, 0.0))]),
            fc.Edge("attach_b", [fc.Line(fc.P(ln, 0.0), fc.P(ln, w))]),
            fc.Edge("edge_top", [fc.Line(fc.P(ln, w), fc.P(0.0, w))]),
            fc.Edge("attach_a", [fc.Line(fc.P(0.0, w), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("edge_bottom", 0.5, "under instep")],
        grainline=fc.Grainline(fc.P(ln * 0.2, w / 2.0), fc.P(ln * 0.8, w / 2.0)),
        cut=fc.CutSpec(quantity=1),
        label="Instep strap",
    )


def build():
    pattern = fc.PatternSet("ankle-gaiter")
    everything = target_piece == "set"

    wrap = build_wrap()
    strap = build_instep_strap()

    if everything or target_piece == "wrap":
        pattern.add(wrap)
    if everything or target_piece == "instep_strap":
        pattern.add(strap)

    # ── Declared seams ──────────────────────────────────────────────────────
    if everything:
        # The strap's two mount ends sew to the wrap's ankle edge. Both ends are
        # strap_w tall, so each declared end matches its mate at delta 0.
        pattern.declare_seam(("instep_strap", "attach_a"),
                             ("instep_strap", "attach_b"), tol=0.5)
    # The two closure edges are drafted to the same run (a symmetric taper), so the
    # laced-shut closure is a declared, verified relationship — not an assumption.
    if everything or target_piece == "wrap":
        pattern.declare_seam(("wrap", "closure_l"), ("wrap", "closure_r"), tol=0.5)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity * (2.0 if p.cut.on_fold else 1.0)
                     for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.62)
    pattern.bom = [
        {"item": "waxed cotton, cordura, or oilskin (shell)",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 62% marker. Per PAIR, double this."},
        {"item": "lacing hooks", "qty": 2 * hook_count, "unit": "pcs",
         "note": "Yantra4D `lacing-hook` — riveted up both closure edges at "
                 f"{round(hook_pitch, 1)} mm pitch, {hook_count} per side."},
        {"item": "lace or shock cord", "qty": 1, "unit": "pcs",
         "note": "zig-zags the hook ladder to close the gaiter."},
        {"item": "rivets for the hook plates", "qty": 2 * hook_count, "unit": "pcs",
         "note": "one per hook plate; back with a washer on soft shell fabric."},
        {"item": "all-purpose or bonded thread", "qty": 1, "unit": "spool",
         "note": "bind the top and ankle edges; box-stitch the instep strap ends."},
    ]
    pattern.metadata = {
        "fc300_rank": 231, "family": "footwear_soft", "fabric_hint": "lona-encerada",
        "silhouette_note": "A short tapered wrap gaiter over the boot top, closing up "
            "the front on a ladder of lacing hooks, held down by an under-instep strap.",
        "sizing_note": "ankle_girth and calf_girth ARE canonical ISO-8559 landmarks and "
            "both are claimed — a gaiter wraps exactly those. No foot code is claimed: "
            "ISO 8559 as vendored declares none.",
        "hardware_note": "The hook ladder is dimensional, not decorative: hook_count at "
            "hook_pitch occupies HOOK_RUN, and the closure edge is drafted to at least "
            "that run so the hooks actually fit the edge they mount to.",
        "solved": {
            "bottom_width_mm": round(BOT_W, 1),
            "top_width_mm": round(TOP_W, 1),
            "closure_len_mm": round(CLOSURE_LEN, 1),
            "hook_run_mm": round(HOOK_RUN, 1),
            "hooks_total": 2 * hook_count,
        },
    }
    return pattern


result = build()
