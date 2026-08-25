# Moccasin

The classic **plug-vamp moccasin**: one piece of hide wrapped up from *under* the foot to
be sole and sides at once (the true moccasin construction), an apron **plug** set into the
gathered throat with a **whipstitch**, and an ankle **collar** band.

Part of the **Fashion Cabinet Commons** (FC-300, Lane 4 — footwear soft goods). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

| Piece | Cut | Notes |
| :-- | :-- | :-- |
| `vamp` | 1 **on fold** (centre line), mirrored | Sole and both sides opened out flat; solved `throat`. |
| `plug` | 1 | Apron panel; its two sides are whipstitched into the throat. |
| `collar` | 1 | Ankle band, sized to clear `ankle_girth`. |

Cut all three again for the second shoe.

## The whipstitch is declared, not hidden

A moccasin's signature is that the vamp throat is **deliberately longer** than the plug it
sews to — the whipstitch (an over-the-edge stitch through both edges, not a turned seam)
gathers that extra length in as it goes. This cartridge drafts the throat to
`gather_ratio ×` the plug side and then declares the difference as explicit seam **ease**:

| Side A | Side B | Ease |
| :-- | :-- | :-- |
| `vamp.throat` | `plug.side_r` | the solved gather (≈ 29 mm at defaults) |
| `vamp.throat` | `plug.side_l` | same run, mirrored by the fold |
| `collar.attach` | `vamp.collar_line` ×2 | the band's joins + ankle clearance |

At `gather_ratio = 1.0` the gather goes to zero and the seam is a plain edge-to-edge
whipstitch. Nothing is rounded away to make the numbers agree: `verify()` records the real
lengths and confirms each seam is `ok`.

## Sizing — no invented landmark codes

`foot_length` and `foot_girth` are **plain sized parameters** carrying no `measurement`
block: ISO 8559, as vendored in `packages/schemas/body-measurements.schema.json`, declares
no foot landmark codes at all. `ankle_girth` **is** canonical and **is** claimed with
`{"standard": "iso_8559", "code": "ankle_girth"}` — the collar genuinely reaches the
ankle, so that one measurement is real.

## Solving

The throat is a Bézier whose bulge is bisected until its arc length equals
`plug_side × gather_ratio`. Because an arc is always longer than its chord, the throat's
end point is placed on the **throat budget** (scaled back along its own line when
`plug_length` would overrun it) rather than on `plug_length` alone — otherwise a short
plug with no gather demands a straight-line throat longer than the seam it sews to, which
the solver correctly refuses to draft.

## Cross-commons bridge

**None.** Rank 229 asks for `pattern` only, and a moccasin is genuinely hardware-free —
that is much of its point. No `hardware_ref` is claimed where no hardware exists.

## Parameters

`foot_length`, `foot_girth`, `ankle_girth`, `plug_width`, `plug_length`, `gather_ratio`,
`collar_height`, `seam_allowance`.

## Provenance
Original draft for Fashion Cabinet. `CERN-OHL-W-2.0`.
