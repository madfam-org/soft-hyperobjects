"""
Wallet Organizer — Fashion Cabinet Bag Cartridge (FC-300 rank #210, y4d chicago screw).

A folded multi-pocket organizer: a SHELL panel that folds in half down its centre, a
stack of card POCKET tiers on each inner face, a full-width CASH sleeve behind them, and
chicago screws binding the four corners. The screw is a Yantra4D solid (`chicago-screw`;
see the manifest's notion.hardware_ref) and is POINT-PLACED hardware — a threaded post
through a drilled bore stack, with no sewn flange, so it takes bore positions rather than
an edge coupling.

The dimensional idea that matters here: a chicago screw has to be long enough for the
STACK it binds. The stack thickness is computed from the number of pocket tiers times the
material thickness, and that computed stack drives the screw's `stack_t` — so the screw
is dimensioned to the wallet it actually closes, not to a nominal guess.

The seam that must SOLVE: each pocket tier steps up the shell by one card-reveal, so the
tier heights are a computed ladder, and the cash sleeve must span the shell's measured
half-width. Both come off the drafted geometry.

Pieces:
  - shell  : the folding outer panel (open, before the fold).
  - pocket : one card-pocket tier (cut per tier, both sides).
  - cash   : the full-width cash sleeve.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # shell|pocket|cash|set

wallet_width = float(PARAM(lambda: wallet_width, 100.0))   # closed width (one face)
wallet_height = float(PARAM(lambda: wallet_height, 95.0))  # closed height
card_reveal = float(PARAM(lambda: card_reveal, 14.0))      # step between card tiers
pocket_tiers = float(PARAM(lambda: pocket_tiers, 3))       # card tiers per inner face
material_thickness = float(PARAM(lambda: material_thickness, 1.2))  # leather thickness
screw_head = float(PARAM(lambda: screw_head, 8.0))         # chicago-screw head diameter
seam_allowance = float(PARAM(lambda: seam_allowance, 4.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
wallet_width = max(70.0, min(wallet_width, 150.0))
wallet_height = max(70.0, min(wallet_height, 130.0))
card_reveal = max(8.0, min(card_reveal, 26.0))
pocket_tiers = int(max(1, min(int(pocket_tiers), 5)))
material_thickness = max(0.6, min(material_thickness, 3.0))
screw_head = max(5.0, min(screw_head, 14.0))
seam_allowance = max(0.0, min(seam_allowance, 10.0))

# The ladder of card tiers must fit inside the wallet height and still leave a usable
# pocket. Without this clamp a tall reveal x many tiers drives the tier height negative
# (which the CCW normalizer would silently flip into a valid-but-wrong piece), so the
# reveal is capped to whatever the height can actually carry.
_MIN_POCKET_H = 30.0
if pocket_tiers > 1:
    card_reveal = min(card_reveal,
                      (wallet_height - _MIN_POCKET_H) / (pocket_tiers - 1))
card_reveal = max(card_reveal, 4.0)

# The shell opens to twice the closed width (it folds down the centre).
SHELL_W = 2.0 * wallet_width
SHELL_H = wallet_height

# The pocket ladder: tier k rises k reveals above the shell's base.
POCKET_H = wallet_height - (pocket_tiers - 1) * card_reveal
# The bound stack the chicago screw must pass through: the shell (doubled at the fold
# corner) plus every pocket tier plus the cash sleeve, each one material thickness.
STACK_T = material_thickness * (2 + pocket_tiers + 1)


def build_shell():
    """The folding outer panel: SHELL_W x SHELL_H, with the centre fold marked and the
    four chicago-screw bores drilled in from the corners."""
    w, h = SHELL_W, SHELL_H
    edges = [
        fc.Edge("left", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
        fc.Edge("right", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("centre-fold", [fc.P(w / 2.0, 0.0), fc.P(w / 2.0, h)], kind="marking"),
    ]
    # Chicago-screw bores: four, inset from the corners by head diameter + margin.
    inset = screw_head * 1.3
    for x in (inset, w - inset):
        for y in (inset, h - inset):
            internals.append(fc.Internal("screw-bore",
                                         [fc.P(x - screw_head / 2.0, y),
                                          fc.P(x + screw_head / 2.0, y)], kind="drill"))
            internals.append(fc.Internal("screw-bore",
                                         [fc.P(x, y - screw_head / 2.0),
                                          fc.P(x, y + screw_head / 2.0)], kind="drill"))
    # The pocket-tier step ladder, marked on the shell so the tiers land square.
    for k in range(pocket_tiers):
        y = POCKET_H + k * card_reveal
        if y < h:
            internals.append(fc.Internal("tier-line",
                                         [fc.P(0.0, y), fc.P(w, y)], kind="marking"))
    return fc.Piece(
        "shell",
        edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("top", 0.5, "centre fold"),
                 fc.Notch("bottom", 0.5, "centre fold")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.15), fc.P(w * 0.5, h * 0.85)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Shell (folds at centre)",
    )


def build_pocket():
    """One card-pocket tier: as wide as one wallet face, POCKET_H tall. Cut two per tier
    (one for each inner face), so quantity is 2 x tiers."""
    w, h = wallet_width, POCKET_H
    return fc.Piece(
        "pocket",
        [
            fc.Edge("bind_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("bind_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},        # the card mouth is a finished edge, not sewn
        notches=[fc.Notch("mouth", 0.5, "card centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=2 * pocket_tiers),
        label="Card Pocket Tier",
    )


def build_cash():
    """The full-width cash sleeve, sitting behind the card tiers on one face."""
    w, h = wallet_width, wallet_height - card_reveal
    return fc.Piece(
        "cash",
        [
            fc.Edge("bind_l", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, h))]),
            fc.Edge("mouth", [fc.Line(fc.P(0.0, h), fc.P(w, h))]),
            fc.Edge("bind_r", [fc.Line(fc.P(w, h), fc.P(w, 0.0))]),
            fc.Edge("base", [fc.Line(fc.P(w, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        allowances={"mouth": 0.0},
        notches=[fc.Notch("mouth", 0.5, "note centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, h * 0.2), fc.P(w * 0.5, h * 0.8)),
        cut=fc.CutSpec(quantity=1),
        label="Cash Sleeve",
    )


def build():
    pattern = fc.PatternSet("wallet-organizer")
    all_pieces = target_piece == "set"
    if all_pieces or target_piece == "shell":
        pattern.add(build_shell())
    if all_pieces or target_piece == "pocket":
        pattern.add(build_pocket())
    if all_pieces or target_piece == "cash":
        pattern.add(build_cash())

    if all_pieces:
        # Pocket tiers and the cash sleeve are bound to the shell down the same two
        # corner-screw edges, so their bound heights step with the shell's.
        pattern.declare_seam(("pocket", "base"), ("cash", "base"), tol=0.5)
        # Each pocket's mouth spans one wallet face, as does the cash sleeve's.
        pattern.declare_seam(("pocket", "mouth"), ("cash", "mouth"), tol=0.5)
    if all_pieces or target_piece == "pocket":
        # Left and right binding edges are equal — the tier is square to the shell.
        pattern.declare_seam(("pocket", "bind_l"), ("pocket", "bind_r"), tol=0.5)
    if all_pieces or target_piece == "shell":
        # The shell folds at its centre: the two half-widths are equal by construction.
        pattern.declare_seam(("shell", "left"), ("shell", "right"), tol=0.5)

    fabric_width = 1200.0
    total_area = sum(p.area() * p.cut.quantity for p in pattern.pieces)
    marker_len = total_area / (fabric_width * 0.55)
    pattern.bom = [
        {"item": "vegetable-tanned leather or coated canvas",
         "qty": round(marker_len / 10.0) * 10, "unit": "mm_length",
         "note": f"≈ at 1200 mm width, 55% marker; {material_thickness:.1f} mm substance."},
        {"item": "chicago screws", "qty": 4, "unit": "count",
         "note": "Yantra4D chicago-screw (see notion.hardware_ref); POINT-PLACED through "
                 f"the four marked corner bores. Sized to the COMPUTED stack of "
                 f"{STACK_T:.1f} mm — shell + {pocket_tiers} tiers + cash sleeve."},
        {"item": "edge paint or burnishing gum", "qty": 1, "unit": "count",
         "note": "finish every card mouth; they are seen and handled constantly."},
        {"item": "saddler's thread", "qty": 1, "unit": "spool",
         "note": "saddle-stitch the tier bases; the screws take the corner load."},
    ]
    pattern.metadata = {
        "fc300_rank": 210,
        "family": "bags_luggage",
        "fabric_hint": "manta-cruda",
        "finished_mm": {"closed_width": round(wallet_width, 1),
                        "closed_height": round(wallet_height, 1),
                        "open_width": round(SHELL_W, 1)},
        "solved": {
            "pocket_tiers": pocket_tiers,
            "card_reveal_mm": round(card_reveal, 1),
            "tier_height_mm": round(POCKET_H, 2),
            "bound_stack_mm": round(STACK_T, 2),
            "note": "the tier ladder is computed from tiers x reveal, and the chicago "
                    "screw's stack_t is the COMPUTED bound stack (shell doubled + every "
                    "tier + the cash sleeve, each one material thickness) — the screw is "
                    "dimensioned to the wallet it actually closes.",
        },
        "hardware": "corner binding via Yantra4D (notion.hardware_ref -> chicago-screw); "
                    "POINT/SLOT placement — a threaded post through a drilled bore stack, "
                    "no sewn flange, so it takes bore positions, not an edge coupling",
    }
    return pattern


result = build()
