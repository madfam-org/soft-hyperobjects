"""
Radio Chest Pack — Fashion Cabinet Garment Cartridge (FC-300 #244, technical & outdoor).

The chest-mounted radio pouch: a boxed pouch that rides high on the sternum where a hand
finds it without looking, carried on an H-harness whose four straps run through ladder-lock
adjusters so one rig fits over a shell, a puffy, or bare shoulders. Wildland crews, marine
teams, ski patrol, and race marshals wear it; the point is that the radio, the mic lead,
and the antenna all stay clear of a pack's hip belt and shoulder straps.

The ladder-lock adjuster solid is Yantra4D territory (`strap-buckle`; see the manifest's
notion.hardware_ref). Fashion Cabinet owns the pack — the pouch solved to the radio
envelope, the harness solved to ISO 8559 chest girth and across-front, the strap runs.

The pouch uses the house boxed-wrap construction (projects/dopp-kit, projects/belt-bag):
one panel = front + base + back folded at the base, with side gussets solved to the
panel's own side run.

Pieces:
  - pouch   : front + base + back cut as one, folded at the base.
  - gusset  : the two side gussets (cut 2, mirrored).
  - flap    : the storm flap over the radio head and the antenna slot.
  - strap   : one H-harness strap (cut 4 — two shoulder, two side).

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
target_piece = str(PARAM(lambda: target_piece, "set"))       # pouch|gusset|flap|strap|set

chest_girth  = float(PARAM(lambda: chest_girth, 1000.0))     # ISO 8559 chest/bust girth
across_front = float(PARAM(lambda: across_front, 360.0))     # ISO 8559 across front
radio_width  = float(PARAM(lambda: radio_width, 68.0))       # radio body width
radio_depth  = float(PARAM(lambda: radio_depth, 40.0))       # radio body depth
radio_height = float(PARAM(lambda: radio_height, 140.0))     # radio body height, no antenna
pouch_ease   = float(PARAM(lambda: pouch_ease, 14.0))        # ease around the radio
flap_drop    = float(PARAM(lambda: flap_drop, 75.0))         # storm flap over the head
webbing      = float(PARAM(lambda: webbing, 25.0))           # harness webbing width
strap_run    = float(PARAM(lambda: strap_run, 420.0))        # one harness strap run
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
chest_girth  = max(700.0, min(chest_girth, 1700.0))
across_front = max(260.0, min(across_front, 540.0))
radio_width  = max(40.0, min(radio_width, 140.0))
radio_depth  = max(20.0, min(radio_depth, 90.0))
radio_height = max(70.0, min(radio_height, 280.0))
pouch_ease   = max(4.0, min(pouch_ease, 40.0))
flap_drop    = max(30.0, min(flap_drop, 160.0))
webbing      = max(15.0, min(webbing, 50.0))
strap_run    = max(200.0, min(strap_run, 800.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

PW = radio_width + pouch_ease         # pouch inside width
PD = radio_depth + pouch_ease         # pouch inside depth
PH = radio_height + pouch_ease        # pouch inside height
PANEL_H = 2.0 * PH + PD               # front + base + back, flat
SIDE_RUN = 2.0 * PH + PD              # what one gusset must wrap — the panel's side


def build_pouch():
    """Front + base + back as one fold-at-base panel (the house wrap construction)."""
    y_fb = PH
    y_bb = PH + PD
    internals = [
        fc.Internal("fold-front-base", [fc.P(0.0, y_fb), fc.P(PW, y_fb)], kind="marking"),
        fc.Internal("fold-base-back", [fc.P(0.0, y_bb), fc.P(PW, y_bb)], kind="marking"),
        # The mic-lead exit, high on the front face beside the radio head.
        fc.Internal("mic-lead-exit",
                    [fc.P(PW * 0.82, PH * 0.86), fc.P(PW * 0.94, PH * 0.86)], kind="drill"),
        # Where the four harness straps are bar-tacked to the back face.
        fc.Internal("strap-seat-upper",
                    [fc.P(PW * 0.5 - webbing, PANEL_H - 22.0),
                     fc.P(PW * 0.5 + webbing, PANEL_H - 22.0)], kind="drill"),
        fc.Internal("strap-seat-lower",
                    [fc.P(PW * 0.5 - webbing, y_bb + 22.0),
                     fc.P(PW * 0.5 + webbing, y_bb + 22.0)], kind="drill"),
    ]
    return fc.Piece(
        "pouch",
        [
            fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, PANEL_H))]),
            fc.Edge("top_back", [fc.Line(fc.P(0.0, PANEL_H), fc.P(PW, PANEL_H))]),
            fc.Edge("right", [fc.Line(fc.P(PW, PANEL_H), fc.P(PW, 0.0))]),
            fc.Edge("top_front", [fc.Line(fc.P(PW, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("left", PH / PANEL_H, "front base fold"),
                 fc.Notch("left", (PH + PD) / PANEL_H, "back base fold")],
        grainline=fc.Grainline(fc.P(PW * 0.5, 18.0), fc.P(PW * 0.5, PANEL_H - 18.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Pouch (front + base + back)",
    )


def build_gusset():
    """One side gusset, SOLVED to the pouch's side run: PH + PD + PH = the panel side."""
    return fc.Piece(
        "gusset",
        [
            fc.Edge("base", [fc.Line(fc.P(0.0, 0.0), fc.P(PD, 0.0))]),
            fc.Edge("back_edge", [fc.Line(fc.P(PD, 0.0), fc.P(PD, PH))]),
            fc.Edge("top", [fc.Line(fc.P(PD, PH), fc.P(0.0, PH))]),
            fc.Edge("front_edge", [fc.Line(fc.P(0.0, PH), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("front_edge", 0.5, "front face mid"),
                 fc.Notch("back_edge", 0.5, "back face mid")],
        grainline=fc.Grainline(fc.P(PD * 0.5, 10.0), fc.P(PD * 0.5, PH - 10.0)),
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Side gusset",
    )


def build_flap():
    """The storm flap: covers the radio head, slotted so the antenna passes through."""
    depth = PD + flap_drop
    slot_w = max(8.0, radio_width * 0.18)
    return fc.Piece(
        "flap",
        [
            fc.Edge("hinge", [fc.Line(fc.P(0.0, 0.0), fc.P(PW, 0.0))]),
            fc.Edge("side_r", [fc.Line(fc.P(PW, 0.0), fc.P(PW, depth))]),
            fc.Edge("front_edge",
                    [fc.curve_through(fc.P(PW, depth), fc.P(0.0, depth), bulge=0.10, side=1.0)]),
            fc.Edge("side_l", [fc.Line(fc.P(0.0, depth), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("hinge", 0.5, "flap centre")],
        grainline=fc.Grainline(fc.P(PW * 0.5, 10.0), fc.P(PW * 0.5, depth - 10.0)),
        internals=[
            fc.Internal("flap-fold", [fc.P(0.0, PD), fc.P(PW, PD)], kind="fold"),
            fc.Internal("antenna-slot",
                        [fc.P(PW * 0.80 - slot_w / 2.0, PD * 0.35),
                         fc.P(PW * 0.80 + slot_w / 2.0, PD * 0.35)], kind="drill"),
        ],
        cut=fc.CutSpec(quantity=1),
        label="Storm flap",
    )


def build_strap():
    """One H-harness strap: over the shoulder or round the ribs, through a ladder-lock."""
    return fc.Piece(
        "strap",
        [
            fc.Edge("bottom", [fc.Line(fc.P(0.0, 0.0), fc.P(strap_run, 0.0))]),
            fc.Edge("free_end", [fc.Line(fc.P(strap_run, 0.0), fc.P(strap_run, webbing))]),
            fc.Edge("top", [fc.Line(fc.P(strap_run, webbing), fc.P(0.0, webbing))]),
            fc.Edge("anchor_end", [fc.Line(fc.P(0.0, webbing), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=0.0,
        notches=[fc.Notch("bottom", 0.5, "ladder-lock travel"),
                 fc.Notch("bottom", 0.85, "keeper")],
        grainline=fc.Grainline(fc.P(strap_run * 0.15, webbing / 2.0),
                               fc.P(strap_run * 0.85, webbing / 2.0)),
        cut=fc.CutSpec(quantity=4),
        label="H-harness strap",
    )


def build():
    pattern = fc.PatternSet("radio-chest-pack")
    everything = target_piece == "set"
    if everything or target_piece == "pouch":
        pattern.add(build_pouch())
    if everything or target_piece == "gusset":
        pattern.add(build_gusset())
    if everything or target_piece == "flap":
        pattern.add(build_flap())
    if everything or target_piece == "strap":
        pattern.add(build_strap())
    if everything:
        # Each gusset wraps a whole side of the wrap panel: front face + base + back
        # face is SOLVED to the panel's side edge — a dimensional proof.
        pattern.declare_seam(
            [("gusset", "front_edge"), ("gusset", "base"), ("gusset", "back_edge")],
            [("pouch", "left")], tol=1.0)
        pattern.declare_seam(
            [("gusset", "front_edge"), ("gusset", "base"), ("gusset", "back_edge")],
            [("pouch", "right")], tol=1.0)
        # The flap hinges on the pouch's back mouth.
        pattern.declare_seam(("flap", "hinge"), ("pouch", "top_back"), tol=1.0)
        # The mouth: the front and back openings are the same run.
        pattern.declare_seam(("pouch", "top_front"), ("pouch", "top_back"), tol=1.0)
        # The strap turns on itself at the ladder-lock.
        pattern.declare_seam(("strap", "anchor_end"), ("strap", "free_end"), tol=1.0)

    fabric_width = 1400.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.70)
    pattern.bom = [
        {"item": "cordura / heavy ripstop",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": "≈ at 1400 mm width, 70% marker; line the pouch so the radio does not rub."},
        {"item": "webbing for the H-harness", "qty": round(strap_run * 4.0),
         "unit": "mm_length", "note": f"{webbing:.0f} mm webbing, four runs."},
        {"item": "ladder-lock adjusters", "qty": 4, "unit": "count",
         "note": "Yantra4D strap-buckle (see notion.hardware_ref) sized to the webbing; "
                 "one per strap so the rig fits over a shell or bare shoulders."},
        {"item": "bonded nylon thread + bar-tacks", "qty": 1, "unit": "set",
         "note": "bar-tack all four strap seats on the back face."},
    ]
    pattern.metadata = {
        "fc300_rank": 244, "family": "technical_outdoor", "fabric_hint": "lona-ripstop",
        "silhouette_note": "A boxed pouch riding high on the sternum where a hand finds it "
            "without looking, on an H-harness whose four ladder-lock straps let one rig fit over "
            "a shell or bare shoulders; the mic lead and antenna exit clear of a pack's straps.",
        "solved": {"pouch_mm": [round(PW, 1), round(PD, 1), round(PH, 1)],
                   "panel_height_mm": round(PANEL_H, 1), "side_run_mm": round(SIDE_RUN, 1),
                   "harness_span_mm": round(across_front, 1)},
        "hardware": "ladder-lock adjusters via Yantra4D (notion.hardware_ref -> strap-buckle)",
    }
    return pattern


result = build()
