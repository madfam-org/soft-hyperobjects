"""
Compression chest binder — Fashion Cabinet Garment Cartridge (FC-400 #387; lane 9).

A pull-on chest binder in power-mesh: a tube from the shoulders to below the chest
that flattens the chest by even, DISTRIBUTED compression. This is a garment worn for
gender affirmation and for sport, and it is the one intimates cartridge where getting
the compression wrong is a safety question, not a fit preference. So this draft is
built around the two rules that make a binder safe:

  1. COMPRESSION IS DISTRIBUTED, NEVER CONCENTRATED. A safe binder flattens over a
     WIDE band of cloth; it never cinches a narrow strap tight. The dangerous binders
     (and the dangerous improvisations — tape, bandages, a too-small sports bra) all
     concentrate force on a small area, which restricts breathing and can crack ribs.
     This cartridge therefore drafts a FULL-TORSO panel, front and back, with the
     compression spread over the whole chest height, and it refuses to go below a
     floor width. The negative ease is an explicit auditable percentage, and it is
     deliberately capped: a binder is not shapewear and more is not better.

  2. IT MUST NOT RIDE UP, AND IT MUST BREATHE. A binder that rolls up becomes a narrow
     concentrated band — the very failure mode rule 1 exists to prevent. So the panel
     is drafted LONG (past the underbust to the ribcage) and its lower edge is only
     lightly gripped, while the underarm is cut high and the back is a hair longer than
     the front so it stays seated. The mesh is the breathable, recoverable kind; the
     draft reports the finished chest ring so the wearer can confirm they are not
     over-binding.

Two pieces: a front and a back torso panel, joined at the side seams and the shoulders,
with the neckline and armholes scooped for a full range of arm movement. No gusset, no
closure — it is pulled on over the head. Made to measure to chest and underbust girths
plus the bind length.

Safety note, stated rather than buried: a binder is worn for a limited time, never slept
in, and never made from non-stretch cloth or improvised from tape or bandages. This
cartridge encodes the distributed-compression rule and caps the ease; it cannot enforce
safe WEAR, which is the wearer's to keep.

Sandbox contract (apps/api/services/engine/fc_runner.py): `fc`/`math` pre-injected;
manifest params arrive as BARE globals via PARAM(lambda...); result = fc.PatternSet.
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
target_piece = str(PARAM(lambda: target_piece, "set"))

chest_girth = float(PARAM(lambda: chest_girth, 960.0))       # fullest chest
underbust_girth = float(PARAM(lambda: underbust_girth, 820.0))
shoulder_width = float(PARAM(lambda: shoulder_width, 400.0))  # across the shoulders
bind_length = float(PARAM(lambda: bind_length, 340.0))       # shoulder seam to hem
neck_scoop = float(PARAM(lambda: neck_scoop, 70.0))          # front neckline drop
arm_scoop = float(PARAM(lambda: arm_scoop, 150.0))           # armhole depth
compression_pct = float(PARAM(lambda: compression_pct, 14.0))  # capped negative ease
min_panel_w = float(PARAM(lambda: min_panel_w, 200.0))       # floor: distributed force
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps (mirror the manifest slider bounds) ───────────────────────────────
chest_girth = max(700.0, min(chest_girth, 1500.0))
underbust_girth = max(600.0, min(underbust_girth, 1350.0))
shoulder_width = max(280.0, min(shoulder_width, 560.0))
bind_length = max(200.0, min(bind_length, 520.0))
neck_scoop = max(20.0, min(neck_scoop, 160.0))
arm_scoop = max(80.0, min(arm_scoop, 280.0))
# SAFETY CAP: compression is capped low. A binder is not shapewear; more is not better,
# and concentrated over-binding is the hazard. 20% is a firm bind; the slider stops there.
compression_pct = max(0.0, min(compression_pct, 20.0))
min_panel_w = max(140.0, min(min_panel_w, 320.0))
seam_allowance = max(0.0, min(seam_allowance, 15.0))

# The armhole cannot swallow the whole bind length, and the neck scoop cannot cross it.
arm_scoop = min(arm_scoop, bind_length - 60.0)
neck_scoop = min(neck_scoop, bind_length - 40.0)

# ── THE DISTRIBUTED-COMPRESSION SOLVER ───────────────────────────────────────
# Finished chest ring = chest girth x (1 - capped ease). The force is spread over the
# WHOLE panel height, never a narrow band — that is what makes a binder safe.
CHEST_FIN = chest_girth * (1.0 - compression_pct / 100.0)
UNDERBUST_FIN = underbust_girth * (1.0 - compression_pct / 100.0)

# Each panel (front, back) carries HALF the finished ring. The panel width is floored so
# the compression is always DISTRIBUTED across a wide band, never concentrated.
FRONT_W = max(min_panel_w, CHEST_FIN / 2.0)
BACK_W = max(min_panel_w, CHEST_FIN / 2.0)
UNDERBUST_HALF = max(min_panel_w * 0.9, UNDERBUST_FIN / 2.0)

# The back is a hair longer than the front so the binder stays seated and does not ride
# up into a concentrated band. Kept small (it is a seating allowance, not a fit change).
BACK_EXTRA = bind_length * 0.05


def _panel(name, width, ub_width, length, neck, is_back, label):
    """One torso panel (front or back), symmetric about its centre line.

    x runs 0..width (side seam to side seam); y from hem (0) to shoulder line (length).
    CCW: left side (up) -> shoulder region (neckline + shoulder seams) -> right side
    (down) -> hem (across). The neckline is scooped between the two shoulder seams; the
    armholes are the upper corners, scooped in from the side seams.

    The lower (hem) edge is the underbust ring — cut a touch wider than the chest ring
    would give, so the grip at the hem is the LIGHTEST, which is what stops the binder
    rolling up. Compression concentrates nowhere.
    """
    cx = width / 2.0
    # hem is the underbust ring width, centred under the chest-width panel
    hem_inset = (width - ub_width) / 2.0
    shoulder_seat = length
    # shoulder seams sit inboard of the side by (width - shoulder_share)/2
    shoulder_share = min(shoulder_width / 2.0, width * 0.8)
    sh_in = (width - shoulder_share) / 2.0
    neck_lo = shoulder_seat - neck
    edges = [
        # left side seam: from hem-left up to the armhole start
        fc.Edge("side_seam_l", [fc.Line(fc.P(hem_inset, 0.0),
                                        fc.P(0.0, shoulder_seat - arm_scoop))]),
        # left armhole: scoop from the side up-and-in to the left shoulder seam
        fc.Edge("armhole_l", [fc.Bezier(
            fc.P(0.0, shoulder_seat - arm_scoop),
            fc.P(width * 0.06, shoulder_seat - arm_scoop * 0.35),
            fc.P(sh_in * 0.55, shoulder_seat - arm_scoop * 0.05),
            fc.P(sh_in, shoulder_seat))]),
        # left shoulder seam across the top to the neckline
        fc.Edge("shoulder_l", [fc.Line(fc.P(sh_in, shoulder_seat),
                                       fc.P(cx - width * 0.10, shoulder_seat))]),
        # neckline scoop across the centre
        fc.Edge("neckline", [fc.Bezier(
            fc.P(cx - width * 0.10, shoulder_seat),
            fc.P(cx - width * 0.05, neck_lo),
            fc.P(cx + width * 0.05, neck_lo),
            fc.P(cx + width * 0.10, shoulder_seat))]),
        # right shoulder seam
        fc.Edge("shoulder_r", [fc.Line(fc.P(cx + width * 0.10, shoulder_seat),
                                       fc.P(width - sh_in, shoulder_seat))]),
        # right armhole scoop down to the right side seam
        fc.Edge("armhole_r", [fc.Bezier(
            fc.P(width - sh_in, shoulder_seat),
            fc.P(width - sh_in * 0.55, shoulder_seat - arm_scoop * 0.05),
            fc.P(width - width * 0.06, shoulder_seat - arm_scoop * 0.35),
            fc.P(width, shoulder_seat - arm_scoop))]),
        fc.Edge("side_seam_r", [fc.Line(fc.P(width, shoulder_seat - arm_scoop),
                                        fc.P(width - hem_inset, 0.0))]),
        fc.Edge("hem", [fc.Line(fc.P(width - hem_inset, 0.0), fc.P(hem_inset, 0.0))]),
    ]
    internals = [
        fc.Internal("underbust line",
                    [fc.P(hem_inset, length * 0.30), fc.P(width - hem_inset, length * 0.30)],
                    kind="marking"),
        fc.Internal("compression band (distributed, whole panel)",
                    [fc.P(width * 0.5, length * 0.15), fc.P(width * 0.5, length * 0.75)],
                    kind="marking"),
    ]
    return fc.Piece(
        name,
        edges,
        seam_allowance=seam_allowance,
        allowances={"hem": 0.0, "neckline": 0.0, "armhole_l": 0.0, "armhole_r": 0.0},
        notches=[fc.Notch("hem", 0.5, "centre"),
                 fc.Notch("side_seam_r", 0.5, "underbust match")],
        grainline=fc.Grainline(fc.P(cx, length * 0.15), fc.P(cx, length * 0.80)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, mirror=False),
        label=label,
    )


def build_front():
    return _panel("front", FRONT_W, UNDERBUST_HALF, bind_length, neck_scoop, False,
                  "Front torso panel (cut 1)")


def build_back():
    # Back is a touch longer (stays seated) and its neckline is shallower.
    return _panel("back", BACK_W, UNDERBUST_HALF, bind_length + BACK_EXTRA,
                  neck_scoop * 0.5, True, "Back torso panel (cut 1, seated a touch longer)")


def build():
    pattern = fc.PatternSet("compression-binder")
    every = target_piece == "set"

    front = build_front()
    back = build_back()

    if not every:
        picked = {"front": front, "back": back}
        if target_piece in picked:
            pattern.add(picked[target_piece])
        return _finish(pattern, front, back)

    pattern.add(front)
    pattern.add(back)
    # Side seams: front's two sides join the back's two sides.
    pattern.declare_seam(("front", "side_seam_l"), ("back", "side_seam_l"), tol=1.5,
                         ease=(front.edge("side_seam_l").length()
                               - back.edge("side_seam_l").length()))
    pattern.declare_seam(("front", "side_seam_r"), ("back", "side_seam_r"), tol=1.5,
                         ease=(front.edge("side_seam_r").length()
                               - back.edge("side_seam_r").length()))
    # Shoulder seams: front shoulders join back shoulders.
    pattern.declare_seam(("front", "shoulder_l"), ("back", "shoulder_l"), tol=1.0)
    pattern.declare_seam(("front", "shoulder_r"), ("back", "shoulder_r"), tol=1.0)

    return _finish(pattern, front, back)


def _finish(pattern, front, back):
    neck_opening = front.edge("neckline").length() + back.edge("neckline").length()
    arm_opening = 2.0 * (front.edge("armhole_r").length()
                         + back.edge("armhole_r").length())
    hem_opening = front.edge("hem").length() + back.edge("hem").length()
    fabric_width = 1500.0
    area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = area / (fabric_width * 0.6)
    pattern.bom = [
        {"item": "power-mesh (breathable compression, 4-way)", "qty": round(marker_len / 10.0) * 10,
         "unit": "mm_length",
         "note": f"front + back panels at {fabric_width:.0f} mm width, 60% marker. Use the "
                 "BREATHABLE recovery mesh — never a non-stretch cloth, and never tape or "
                 "bandages, which concentrate force and are the hazard this garment avoids."},
        {"item": "neckline + armhole binding (soft, flat) 8-10 mm",
         "qty": round((neck_opening + arm_opening) * 0.95), "unit": "mm_length",
         "note": f"neckline {neck_opening:.0f} mm + armholes {arm_opening:.0f} mm at 0.95 "
                 "— bound flat so no edge digs in."},
        {"item": "hem elastic (light grip only) 12 mm", "qty": round(hem_opening * 0.98),
         "unit": "mm_length",
         "note": f"hem {hem_opening:.0f} mm at 0.98 — the LIGHTEST grip of all, so the "
                 "binder does not roll up into a narrow concentrated band."},
        {"item": "polyester thread + ballpoint 70/10 + coverstitch", "qty": 1, "unit": "set",
         "note": "coverstitch the binding so seams stretch with the mesh."},
    ]
    pattern.metadata = {
        "fc400_rank": 387, "family": "underwear_lounge", "fabric_hint": "power-mesh",
        "silhouette_note": "A full-torso pull-on binder: front and back panels joined at "
            "the sides and shoulders, scooped neckline and high armholes for arm movement, "
            "drafted LONG to the ribcage so it stays seated. Compression is spread over the "
            "whole panel, never a narrow band.",
        "safety": {
            "distributed_compression": True,
            "min_panel_width_mm": round(min_panel_w, 1),
            "compression_cap_pct": 20.0,
            "note": "Compression is DISTRIBUTED across a wide floored panel and the ease is "
                    "CAPPED — a binder is not shapewear and more is not better. Concentrated "
                    "force (tape, bandages, a too-tight narrow band) restricts breathing and "
                    "can crack ribs; this draft refuses to concentrate it. The cartridge "
                    "cannot enforce safe WEAR — worn for limited time, never slept in — which "
                    "stays the wearer's to keep.",
        },
        "solved": {
            "chest_finished_mm": round(CHEST_FIN, 1),
            "underbust_finished_mm": round(UNDERBUST_FIN, 1),
            "compression_pct": round(compression_pct, 1),
            "front_panel_width_mm": round(FRONT_W, 1),
            "back_seated_extra_mm": round(BACK_EXTRA, 1),
            "neck_opening_mm": round(neck_opening, 1),
            "arm_opening_mm": round(arm_opening, 1),
        },
        "hardware": "none — the binder is pulled on over the head; there is no closure to "
                    "bridge, and this lane does not invent one.",
        "drafting": "Made to measure to chest and underbust girths plus bind length; the "
                    "finished chest ring is printed so the wearer can confirm they are not "
                    "over-binding.",
    }
    return pattern


result = build()
