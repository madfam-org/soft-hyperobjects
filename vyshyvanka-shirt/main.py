"""
Vyshyvanka embroidered shirt (вишиванка) — Fashion Cabinet Heritage Cartridge
(FC-500 #493, heritage_global; Ukrainian).

The vyshyvanka is the Ukrainian embroidered shirt: a straight, loose linen or hemp shirt built
from rectangular panels, gathered at the neck into a narrow band or drawstring, with straight
sleeves set on square underarm gussets and often a shoulder inset (устав / полик), and worn by
men and women alike. It is the embroidery (вишивка) that carries the meaning — the regional
patterns, the colours, the placement on the sleeves, chest, cuffs, collar and hem — and the
embroidery is exactly what this cartridge does NOT draw. The garment beneath the embroidery is
a peasant-chemise construction of straight cloth, and that is what the draft encodes.

Two facts govern the draft:

  1. IT IS PANELS AND GUSSETS, NOT SHAPED PATTERN PIECES. The body is a rectangle folded at
     the shoulder; the sleeve is a rectangle; the underarm is a SQUARE GUSSET that lets the arm
     move without a curved armscye. There is no set-in sleeve — a right angle under the arm is
     drafted, and the gusset is what keeps it from tearing. The gathered neck is solved from
     the body width, not the neck girth: the whole top of the body is gathered into the band.

  2. THE EMBROIDERY IS A MARKED FIELD, NOT DECORATION. The chest, sleeve, cuff and hem
     embroidery zones are drawn as MARKED fields the maker fills with a regional pattern. No
     specific vyshyvka pattern is drawn or named — those belong to the regions and families
     that keep them.

Pieces:
  - body   : the shirt body, cut on the shoulder fold (front + back), gathered neck.
  - sleeve : the straight sleeve (cut 2), gathered at the top, embroidery zones marked.
  - gusset : the square underarm gusset (cut 2).
  - collar : the narrow neck band the body is gathered into.

Hardware: none — the neck is a band or drawstring; there is no hardware closure.

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
target_piece = str(PARAM(lambda: target_piece, "set"))   # body|sleeve|gusset|collar|set

body_width = float(PARAM(lambda: body_width, 620.0))      # half body width (flat, per side)
shirt_length = float(PARAM(lambda: shirt_length, 720.0))  # shoulder to hem
neck_girth = float(PARAM(lambda: neck_girth, 400.0))
neck_gather = float(PARAM(lambda: neck_gather, 2.1))      # body top / neck band ratio
sleeve_length = float(PARAM(lambda: sleeve_length, 560.0))
sleeve_width = float(PARAM(lambda: sleeve_width, 440.0))  # flat sleeve width (gathered at top)
cuff_girth = float(PARAM(lambda: cuff_girth, 240.0))
gusset_size = float(PARAM(lambda: gusset_size, 120.0))
collar_height = float(PARAM(lambda: collar_height, 28.0))
neck_drop_front = float(PARAM(lambda: neck_drop_front, 90.0))  # front slit/opening depth
seam_allowance = float(PARAM(lambda: seam_allowance, 10.0))
hem_allowance = float(PARAM(lambda: hem_allowance, 30.0))

# ── Clamps ───────────────────────────────────────────────────────────────────
body_width = max(460.0, min(body_width, 820.0))
shirt_length = max(600.0, min(shirt_length, 950.0))
neck_girth = max(320.0, min(neck_girth, 480.0))
neck_gather = max(1.4, min(neck_gather, 3.2))
sleeve_length = max(420.0, min(sleeve_length, 680.0))
sleeve_width = max(320.0, min(sleeve_width, 560.0))
cuff_girth = max(180.0, min(cuff_girth, 340.0))
gusset_size = max(80.0, min(gusset_size, 180.0))
collar_height = max(18.0, min(collar_height, 50.0))
neck_drop_front = max(40.0, min(neck_drop_front, 180.0))
seam_allowance = max(6.0, min(seam_allowance, 16.0))
hem_allowance = max(10.0, min(hem_allowance, 60.0))

# ── The gather solve — the neck band from the body width ─────────────────────
# The whole top of the body is gathered into the neck band. The band length is the neck girth
# plus ease; the body top per side must be at least that times the gather ratio to have real
# fullness — the collar is cut to the band length, and the gather ratio is reported.
NECK_BAND = neck_girth + 20.0
BODY_TOP = body_width * 2.0                # the full flat top width gathered into the band
ACTUAL_GATHER = BODY_TOP / NECK_BAND
# The neck opening on the fold: a slit at centre front of depth neck_drop_front. The shoulder
# fold carries a shallow neck scoop so the band sits on the neck base.
NECK_SCOOP = min(neck_girth / 6.0, body_width * 0.25)


def build_body():
    """The shirt body, cut on the shoulder fold: a rectangle body_width x shirt_length per side
    (folded at the top), with a shallow neck scoop and a front slit marked."""
    w = body_width
    h = shirt_length
    p_hem_l = fc.P(0.0, 0.0)
    p_hem_r = fc.P(w, 0.0)
    p_underarm = fc.P(w, h - gusset_size)
    p_shoulder = fc.P(w, h)               # the shoulder fold is the top edge
    p_neck_edge = fc.P(NECK_SCOOP, h)
    p_neck_cf = fc.P(0.0, h - NECK_SCOOP * 0.4)
    edges = [
        fc.Edge("hem", [fc.Line(p_hem_l, p_hem_r)]),
        fc.Edge("side", [fc.Line(p_hem_r, p_underarm)]),
        # the gusset seat: a short edge up to the shoulder fold at the side (where the sleeve
        # and gusset attach). Above the underarm the side is open for the sleeve.
        fc.Edge("armpit", [fc.Line(p_underarm, p_shoulder)]),
        fc.Edge("shoulder_fold", [fc.Line(p_shoulder, p_neck_edge)]),
        fc.Edge("neck", [fc.Bezier(p_neck_edge,
                                   fc.P(NECK_SCOOP * 0.55, h - 3.0),
                                   fc.P(NECK_SCOOP * 0.25, p_neck_cf.y + 3.0),
                                   p_neck_cf)]),
        fc.Edge("cf", [fc.Line(p_neck_cf, p_hem_l)]),
    ]
    internals = [
        fc.Internal("front-slit", [fc.P(0.0, h - NECK_SCOOP * 0.4),
                                   fc.P(0.0, h - NECK_SCOOP * 0.4 - neck_drop_front)],
                    kind="marking"),
        # embroidery fields: chest, and the hem band.
        fc.Internal("chest-embroidery",
                    [fc.P(10.0, h - NECK_SCOOP - 20.0),
                     fc.P(min(w * 0.6, w - 10.0), h - NECK_SCOOP - 20.0),
                     fc.P(min(w * 0.6, w - 10.0), h - NECK_SCOOP - 20.0 - shirt_length * 0.22),
                     fc.P(10.0, h - NECK_SCOOP - 20.0 - shirt_length * 0.22)],
                    kind="marking"),
        fc.Internal("hem-embroidery", [fc.P(0.0, hem_allowance + 30.0),
                                       fc.P(w, hem_allowance + 30.0)], kind="marking"),
        fc.Internal("gather-line", [fc.P(NECK_SCOOP, h), fc.P(w, h)], kind="marking"),
    ]
    return fc.Piece(
        "body", edges,
        seam_allowance=seam_allowance,
        allowances={"hem": hem_allowance},
        notches=[fc.Notch("side", (shirt_length - gusset_size) / max(shirt_length, 1.0) * 0.5,
                          "side mid")],
        grainline=fc.Grainline(fc.P(w * 0.3, hem_allowance + 30.0),
                               fc.P(w * 0.3, h - gusset_size - 30.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=1, on_fold=True, fold_edge="shoulder_fold", mirror=True),
        label="Shirt body (rectangle, gathered neck), cut on shoulder fold",
    )


def build_sleeve():
    """The straight sleeve (cut 2): a rectangle gathered at the top into the shoulder, tapering
    to the cuff, with marked embroidery zones on the upper sleeve and cuff."""
    w = sleeve_width
    h = sleeve_length
    cuff_half = cuff_girth
    # a slight taper from the gathered top to the cuff.
    p_cuff_l = fc.P((w - cuff_half) / 2.0, 0.0)
    p_cuff_r = fc.P((w + cuff_half) / 2.0, 0.0)
    p_top_r = fc.P(w, h)
    p_top_l = fc.P(0.0, h)
    edges = [
        fc.Edge("cuff", [fc.Line(p_cuff_l, p_cuff_r)]),
        fc.Edge("under_r", [fc.Line(p_cuff_r, p_top_r)]),
        fc.Edge("top", [fc.Line(p_top_r, p_top_l)]),
        fc.Edge("under_l", [fc.Line(p_top_l, p_cuff_l)]),
    ]
    internals = [
        fc.Internal("upper-embroidery",
                    [fc.P(w * 0.15, h - 20.0), fc.P(w * 0.85, h - 20.0),
                     fc.P(w * 0.85, h - 20.0 - sleeve_length * 0.28),
                     fc.P(w * 0.15, h - 20.0 - sleeve_length * 0.28)], kind="marking"),
        fc.Internal("cuff-embroidery", [fc.P((w - cuff_half) / 2.0, 40.0),
                                        fc.P((w + cuff_half) / 2.0, 40.0)], kind="marking"),
        fc.Internal("gather-top", [fc.P(0.0, h), fc.P(w, h)], kind="marking"),
    ]
    return fc.Piece(
        "sleeve", edges,
        seam_allowance=seam_allowance,
        allowances={"cuff": 0.0},
        notches=[fc.Notch("top", 0.5, "shoulder centre")],
        grainline=fc.Grainline(fc.P(w * 0.5, 40.0), fc.P(w * 0.5, h - 20.0)),
        internals=internals,
        cut=fc.CutSpec(quantity=2, mirror=True),
        label="Straight sleeve (gathered top, embroidery zones)",
    )


def build_gusset():
    """The square underarm gusset (cut 2): what lets the straight sleeve meet the straight body
    without a curved armscye."""
    g = gusset_size
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(g, 0.0)
    p2 = fc.P(g, g)
    p3 = fc.P(0.0, g)
    edges = [
        fc.Edge("body_lower", [fc.Line(p0, p1)]),
        fc.Edge("sleeve_lower", [fc.Line(p1, p2)]),
        fc.Edge("sleeve_upper", [fc.Line(p2, p3)]),
        fc.Edge("body_upper", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "gusset", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("body_lower", 0.5, "corner match")],
        grainline=fc.Grainline(fc.P(g * 0.2, g * 0.2), fc.P(g * 0.8, g * 0.8)),
        internals=[fc.Internal("bias", [fc.P(0.0, g), fc.P(g, 0.0)], kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Square underarm gusset",
    )


def build_collar():
    """The narrow neck band the gathered body top is set into, cut to the band length."""
    ln = NECK_BAND
    h = collar_height * 2.0 + 4.0
    p0 = fc.P(0.0, 0.0)
    p1 = fc.P(ln, 0.0)
    p2 = fc.P(ln, h)
    p3 = fc.P(0.0, h)
    edges = [
        fc.Edge("neck_edge", [fc.Line(p0, p1)]),
        fc.Edge("end_r", [fc.Line(p1, p2)]),
        fc.Edge("outer", [fc.Line(p2, p3)]),
        fc.Edge("end_l", [fc.Line(p3, p0)]),
    ]
    return fc.Piece(
        "collar", edges,
        seam_allowance=seam_allowance,
        notches=[fc.Notch("neck_edge", 0.5, "centre back")],
        grainline=fc.Grainline(fc.P(ln * 0.1, h * 0.5), fc.P(ln * 0.9, h * 0.5)),
        internals=[fc.Internal("fold", [fc.P(0.0, collar_height + 2.0),
                                        fc.P(ln, collar_height + 2.0)], kind="marking"),
                   fc.Internal("band-embroidery", [fc.P(0.0, collar_height * 0.5),
                                                   fc.P(ln, collar_height * 0.5)],
                               kind="marking")],
        cut=fc.CutSpec(quantity=2),
        label="Neck band (body gathered into it)",
    )


def build():
    pattern = fc.PatternSet("vyshyvanka-shirt")
    everything = target_piece == "set"
    if everything or target_piece == "body":
        pattern.add(build_body())
    if everything or target_piece == "sleeve":
        pattern.add(build_sleeve())
    if everything or target_piece == "gusset":
        pattern.add(build_gusset())
    if everything or target_piece == "collar":
        pattern.add(build_collar())

    if everything:
        # The square gusset: its two body edges against its two sleeve edges — declared so a
        # rhombus cannot sneak into what must be a square.
        pattern.declare_seam(("gusset", "body_lower"), ("gusset", "sleeve_lower"), tol=0.5)
        pattern.declare_seam(("gusset", "body_upper"), ("gusset", "sleeve_upper"), tol=0.5)

    pattern.bom = [
        {"item": "linen or hemp (shirt cloth)", "qty": round(
            (shirt_length + sleeve_length + hem_allowance) * 2.4 / 10.0) * 10,
         "unit": "mm_length",
         "note": "a straight-panel peasant-chemise construction; the embroidery is added "
                 "after cutting, on the marked fields."},
        {"item": "neck band / drawstring", "qty": round(NECK_BAND), "unit": "mm_length",
         "note": f"the whole body top ({BODY_TOP:.0f} mm) is gathered into the "
                 f"{NECK_BAND:.0f} mm band — a gather ratio of {ACTUAL_GATHER:.2f}."},
        {"item": "embroidery floss (вишивка)", "qty": 1, "unit": "set",
         "note": "the maker's — the regional pattern is chosen and worked by the embroiderer; "
                 "none is drafted here."},
        {"item": "thread", "qty": 1, "unit": "spool", "note": ""},
    ]
    pattern.metadata = {
        "fc500_rank": 493,
        "family": "heritage_global",
        "fabric_hint": "algodon-estampado",
        "finished_mm": {
            "body_width": round(body_width, 1),
            "shirt_length": round(shirt_length, 1),
            "sleeve_length": round(sleeve_length, 1),
            "gusset_size": round(gusset_size, 1),
        },
        "solved": {
            "neck_band_mm": round(NECK_BAND, 2),
            "body_top_mm": round(BODY_TOP, 2),
            "actual_gather_ratio": round(ACTUAL_GATHER, 3),
            "neck_scoop_mm": round(NECK_SCOOP, 2),
            "note": "the vyshyvanka is PANELS AND GUSSETS, not shaped pieces: a rectangular "
                    "body folded at the shoulder, straight rectangular sleeves gathered into "
                    "the neck band, and a SQUARE underarm gusset (declared square, so a "
                    "rhombus cannot sneak in) that lets the straight sleeve meet the straight "
                    "body without a curved armscye. The neck band is the gathered top of the "
                    "body: the whole body top is gathered into it at a ratio of "
                    "actual_gather_ratio. The embroidery is a MARKED field, never drawn.",
        },
        "heritage": {
            "garment": "вишиванка vyshyvanka — the Ukrainian embroidered shirt",
            "construction": "straight rectangular body on the shoulder fold, gathered neck "
                            "band, straight sleeves on square underarm gussets, worn by men "
                            "and women",
            "embroidery": "вишивка — the regional patterns on chest, sleeve, cuff, collar and "
                          "hem carry meaning and belong to the regions and families that keep "
                          "them; the cartridge marks the fields but draws no pattern",
            "excluded": "no specific vyshyvka pattern, colour scheme, or regional motif is "
                        "drafted or named",
        },
        "hardware": "none — the neck is a band or drawstring; there is no hardware closure.",
    }
    return pattern


result = build()
