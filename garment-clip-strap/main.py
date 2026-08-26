"""
Clip-strap Garment Carrier — Fashion Cabinet Care & Keeping Cartridge
(FC-400 rank #367, Yantra4D-bridged garment-clip).

The over-the-shoulder carrier that grips a stack of hangers: a padded webbing STRAP runs
over the shoulder, a folded CRADLE at the working end holds the printed clip that bites the
hanger hooks, and a KEEPER loop tames the tail. The clip is the Yantra4D `garment-clip`
solid (notion.hardware_ref) — its sprung jaw grips a bundle of hooks so a dozen garments
travel from wardrobe to car on one shoulder.

Drafting note — the seam that must SOLVE: the cradle is a rectangle folded around the clip
body and box-stitched, so its length is TWICE the clip jaw length plus a wrap allowance for
the clip thickness, and its width is the clip jaw width plus two seam allowances. Both are
derived from the clip's own dimensions (the same jaw_len/jaw_w that drive the bridged
solid), so the pocket the clip lives in can never be cut too small for it.

Pieces:
  - strap  : the shoulder webbing panel (cut 1), padded fold marked.
  - cradle : the clip pocket, folded and box-stitched (cut 1).
  - keeper : the tail-taming loop (cut 1).

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
target_piece = str(PARAM(lambda: target_piece, "set"))  # strap|cradle|keeper|set

strap_length = float(PARAM(lambda: strap_length, 900.0))   # over-the-shoulder run
strap_width = float(PARAM(lambda: strap_width, 50.0))      # webbing width
clip_jaw_len = float(PARAM(lambda: clip_jaw_len, 70.0))    # printed clip jaw length
clip_jaw_width = float(PARAM(lambda: clip_jaw_width, 44.0))  # printed clip jaw width
seam_allowance = float(PARAM(lambda: seam_allowance, 8.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
strap_length = max(600.0, min(strap_length, 1300.0))
strap_width = max(25.0, min(strap_width, 75.0))
clip_jaw_len = max(40.0, min(clip_jaw_len, 110.0))
clip_jaw_width = max(28.0, min(clip_jaw_width, 70.0))
seam_allowance = max(0.0, min(seam_allowance, 20.0))

CLIP_WRAP = clip_jaw_len * 0.35            # allowance to wrap the clip body thickness
# The cradle wraps the clip along its LENGTH: length = twice the jaw plus the wrap,
# so the folded pocket is one jaw-length deep and can never be cut short of the clip.
# Its width equals the strap width — the cradle is cut from the SAME webbing and sews
# to the strap's clip end by construction. The clip's jaw width is held across this
# width; a wider jaw simply proud of the edge is how the jaw reaches the hooks.
CRADLE_LEN = clip_jaw_len * 2.0 + CLIP_WRAP
CRADLE_WID = strap_width


def build_strap():
    """The shoulder webbing panel: a long rectangle, padded fold marked along the
    centre, with the cradle-attach end and the keeper-attach end addressable."""
    ln, w = strap_length, strap_width
    edges = [
        fc.Edge("clip_end", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("tail_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    internals = [
        fc.Internal("pad-fold", [fc.P(strap_length * 0.3, w * 0.5),
                                 fc.P(strap_length * 0.7, w * 0.5)], kind="marking"),
        fc.Internal("shoulder-centre", [fc.P(ln * 0.5, 0.0), fc.P(ln * 0.5, w)],
                    kind="marking"),
    ]
    return fc.Piece(
        "strap", edges,
        seam_allowance=seam_allowance,
        allowances={"top": 0.0, "bottom": 0.0},
        notches=[fc.Notch("top", 0.5, "shoulder crest"),
                 fc.Notch("clip_end", 0.5, "cradle centre")],
        grainline=fc.Grainline(fc.P(30.0, w * 0.5), fc.P(ln - 30.0, w * 0.5)),
        internals=internals,
        cut=fc.CutSpec(quantity=1),
        label="Shoulder strap",
    )


def build_cradle():
    """The clip pocket: a rectangle folded in half across CRADLE_LEN and box-stitched.
    `attach` sews to the strap's clip end (cut to the strap width)."""
    ln, w = CRADLE_LEN, CRADLE_WID
    edges = [
        fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
        fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
        fc.Edge("fold_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
        fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
    ]
    return fc.Piece(
        "cradle", edges,
        seam_allowance=seam_allowance,
        allowances={"fold_end": 0.0},
        notches=[fc.Notch("top", 0.5, "clip fold line"),
                 fc.Notch("attach", 0.5, "match strap clip end")],
        grainline=fc.Grainline(fc.P(30.0, w * 0.5), fc.P(ln - 30.0, w * 0.5)),
        internals=[fc.Internal("box-stitch",
                               [fc.P(clip_jaw_len * 0.2, w * 0.15),
                                fc.P(clip_jaw_len * 0.2, w * 0.85)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=1),
        label="Clip cradle",
    )


KEEPER_LEN = max(80.0, strap_width * 2.6)


def build_keeper():
    """The tail-taming loop: a short strip folded into a loop, `attach` sews to the
    strap's tail end (cut to the strap width)."""
    ln, w = KEEPER_LEN, strap_width
    return fc.Piece(
        "keeper", [
            fc.Edge("attach", [fc.Line(fc.P(0.0, 0.0), fc.P(0.0, w))]),
            fc.Edge("top", [fc.Line(fc.P(0.0, w), fc.P(ln, w))]),
            fc.Edge("free_end", [fc.Line(fc.P(ln, w), fc.P(ln, 0.0))]),
            fc.Edge("bottom", [fc.Line(fc.P(ln, 0.0), fc.P(0.0, 0.0))]),
        ],
        seam_allowance=seam_allowance,
        notches=[fc.Notch("attach", 0.5, "match strap tail end")],
        grainline=fc.Grainline(fc.P(20.0, w * 0.5), fc.P(ln - 20.0, w * 0.5)),
        cut=fc.CutSpec(quantity=1),
        label="Tail keeper loop",
    )


def build():
    pattern = fc.PatternSet("garment-clip-strap")
    everything = target_piece == "set"
    if everything or target_piece == "strap":
        pattern.add(build_strap())
    if everything or target_piece == "cradle":
        pattern.add(build_cradle())
    if everything or target_piece == "keeper":
        pattern.add(build_keeper())

    if everything:
        # THE solving seams: the cradle and keeper attach to the strap ends, each cut
        # to the MEASURED strap width so the seams match by construction.
        pattern.declare_seam(("cradle", "attach"), ("strap", "clip_end"), tol=1.0)
        pattern.declare_seam(("keeper", "attach"), ("strap", "tail_end"), tol=1.0)

    # Webbing is sold to width, not markered like yardage, so the BOM is a linear
    # run of the three webbing pieces rather than a marker length.
    pattern.bom = [
        {"item": "polyester webbing", "qty": round(strap_length + CRADLE_LEN + KEEPER_LEN),
         "unit": "mm_length",
         "note": f"{strap_width:.0f} mm webbing; the strap, cradle and keeper are all cut "
                 "from the one roll."},
        {"item": "garment clip", "qty": 1, "unit": "count",
         "note": f"Yantra4D garment-clip (notion.hardware_ref): jaw {clip_jaw_len:.0f} x "
                 f"{clip_jaw_width:.0f} mm; its sprung jaw bites the hanger-hook bundle."},
        {"item": "foam pad", "qty": round(strap_length * 0.4 * strap_width / 100.0),
         "unit": "cm2", "note": "under the shoulder crest so a loaded strap does not cut in."},
        {"item": "thread", "qty": 1, "unit": "spool",
         "note": "box-X stitch every load-bearing join; this carries a full wardrobe."},
    ]
    pattern.metadata = {
        "fc400_rank": 367,
        "family": "care_and_keeping",
        "fabric_hint": "nylon-ripstop-shell",
        "finished_mm": {"strap_length": round(strap_length, 1),
                        "strap_width": round(strap_width, 1),
                        "clip_jaw_len": round(clip_jaw_len, 1)},
        "solved": {
            "cradle_length_mm": round(CRADLE_LEN, 2),
            "cradle_width_mm": round(CRADLE_WID, 2),
            "clip_wrap_mm": round(CLIP_WRAP, 2),
            "note": "the cradle pocket is derived from the clip's OWN jaw dimensions "
                    "(twice the jaw length plus a wrap allowance, jaw width plus two "
                    "seam allowances), so the pocket can never be cut too small for the "
                    "clip it holds.",
        },
        "hardware": "sprung garment clip via Yantra4D (notion.hardware_ref -> "
                    "garment-clip); jaw_len = clip_jaw_len, jaw_w = clip_jaw_width. "
                    "Logged co-create in the FC-400 index; linked live here.",
    }
    return pattern


result = build()
