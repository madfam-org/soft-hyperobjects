"""
Rebozo — Fashion Cabinet Garment Cartridge (FC-200 rank #139, MX heritage).

The rebozo is the long rectangular Mexican shawl — worn over the shoulders and head,
used to carry children or goods, and finished with the rapacejo, an elaborate hand-knotted
fringe that can be as prized as the weave itself. Its construction is a single long
rectangle; the artistry is the ikat-dyed (jaspe) or brocade weave and the knotted fringe,
both the maker's to supply.

This cartridge drafts the garment geometry: one long rectangle sized in length and width,
with marked fringe (rapacejo) zones at both ends and optional weave bands. Offered with
respect for the living tradition.

Pieces:
  - body : one long rectangle, finished all round (fringed ends). No sewn seam.

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
rebozo_length = float(PARAM(lambda: rebozo_length, 2500.0))  # end to end, EXCLUDING fringe (mm)
rebozo_width  = float(PARAM(lambda: rebozo_width, 700.0))    # loom width of the web (mm)
rapacejo      = float(PARAM(lambda: rapacejo, 250.0))        # knotted-fringe length per end (mm)
band_count    = int(  PARAM(lambda: band_count, 7))          # marked weave bands (jaspe/brocade)

# ── Clamps ───────────────────────────────────────────────────────────────────
rebozo_length = max(1500.0, min(rebozo_length, 3500.0))
rebozo_width  = max(400.0, min(rebozo_width, 1000.0))
rapacejo      = max(0.0, min(rapacejo, 600.0))
band_count    = max(0, min(band_count, 30))

W = rebozo_width
Lc = rebozo_length            # cloth length (fringe is added knotted thread, not woven cloth)


def build_body():
    edges = [
        fc.Edge("start", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, W))]),      # fringed end A
        fc.Edge("top", [fc.Line(fc.P(0.0, W), fc.P(Lc, W))]),          # selvedge
        fc.Edge("end", [fc.Line(fc.P(Lc, W), fc.P(Lc, 0.0))]),         # fringed end B
        fc.Edge("bottom", [fc.Line(fc.P(Lc, 0.0), fc.P(0.0, 0.0))]),   # selvedge
    ]
    internals = []
    if rapacejo > 0.0:
        # Rapacejo (knotted-fringe) zones marked in from each end.
        internals.append(fc.Internal("rapacejo-a",
                                     [fc.P(rapacejo, 0.0), fc.P(rapacejo, W)], kind="marking"))
        internals.append(fc.Internal("rapacejo-b",
                                     [fc.P(Lc - rapacejo, 0.0), fc.P(Lc - rapacejo, W)],
                                     kind="marking"))
    for i in range(1, band_count + 1):
        x = Lc * i / (band_count + 1)
        internals.append(fc.Internal(f"weave-band-{i}",
                                     [fc.P(x, 0.0), fc.P(x, W)], kind="marking"))
    return fc.Piece(
        "body",
        edges,
        seam_allowance=0.0,   # selvedge sides + fringed ends — no sewn seam
        grainline=fc.Grainline(fc.P(Lc * 0.1, W / 2.0), fc.P(Lc * 0.9, W / 2.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Rebozo",
    )


def build():
    pattern = fc.PatternSet("rebozo")
    pattern.add(build_body())
    fabric_width = max(W, 500.0)
    pattern.bom = [
        {"item": "woven web (jaspe/ikat or brocade cloth)",
         "qty": round(Lc / 10.0) * 10, "unit": "mm_length",
         "note": f"one web at {fabric_width:.0f} mm loom width; woven as a single length, "
                 "no cutting into panels."},
        {"item": "rapacejo (knotted fringe)", "qty": 2, "unit": "ends",
         "note": "the hand-knotted fringe at both ends — often as prized as the weave; "
                 "added as knotted warp thread, the knotter's to supply."},
    ]
    pattern.metadata = {
        "fc200_rank": 139,
        "family": "heritage_global",
        "fabric_hint": "popelina-algodon",
        "heritage_note": "The rebozo is a living Mexican garment. This cartridge drafts "
            "the one-rectangle GARMENT GEOMETRY only — the jaspe (ikat) or brocade weave "
            "and the rapacejo (knotted fringe) that carry its identity are the maker's to "
            "supply and are not reproduced here. Offered with respect.",
        "single_rectangle": "One long web, finished at the selvedge sides and fringed at "
            "both ends; no sewn seam. Length and width to the wearer; the rest is weave.",
        "drafting": "one rebozo_length x rebozo_width rectangle; rapacejo (fringe) zones "
            "and weave bands marked for the maker.",
    }
    return pattern


result = build()
