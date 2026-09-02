# Chaleco Charro

The waistcoat of the **traje de charro** — the Mexican horseman's suit. Short, close,
cut in worsted wool, with peaked lapels and a hook-and-bar front that closes edge to
edge.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail band — heritage — Mexican).
**Rank 300: the closing entry of the FC-300 catalog.** Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabi.net).

> The length is set by the trouser, not by the torso, and the front closes edge to edge.
> Get either wrong and it reads as a costume from across an arena.

## Provenance

**Charrería** is Mexico's national sport and a living practice, recognised by UNESCO in
2016 as Intangible Cultural Heritage. The **traje de charro** is its working and formal
dress: a short jacket or waistcoat, high-waisted trousers held by a wide band,
botonadura down the outer leg, boots, and the sombrero. It is regulated — the
**Federación Mexicana de Charrería** sets what may be worn in which category — and it is
worn by charros and charras, by mariachi musicians, and at weddings and civic occasions
across Mexico and the Mexican diaspora.

The chaleco is the piece most often bought badly. What is usually sold is a generic
waistcoat block with soutache added on top, and it reads wrong for two structural
reasons that have nothing to do with the trim.

This cartridge drafts an **everyday to media-gala** chaleco. It is an original draft
made from the garment's construction logic, not a copy of any particular sastre's
pattern.

## Why it earns its rank — and why it is not the waistcoat

The commons already has **`waistcoat`** (FC-100 rank 69), an English single-breasted
suit waistcoat. This is a different garment, and the differences are structural, not
decorative:

| | `waistcoat` (English) | `chaleco-charro` |
|---|---|---|
| Front edge | Button stand beyond centre front | **At centre front — no stand** |
| Closure | 5 buttons through worked holes | **Hook-and-bar sets behind the edge** |
| Hem | Pointed at centre front | **Straight, above the trouser band** |
| Length from | Torso (nape to waist) | **The trouser's waistband** |
| Back | Lining weight, cinch belt | **Cut in the suiting, shaped CB seam, no belt** |
| Neckline | Deep front V to the top button | **Peaked lapel breaking high** |

## The two things that must solve

### 1. The length comes from the trouser

The charro trouser rides high and is held by a wide band. The chaleco must finish
**above** that band — a waistcoat that laps over it breaks the long unbroken line from
shoulder to boot that the whole suit is built around, and that line is the silhouette.

So `waist_rise` — how far the trouser band sits above the natural waist — is a real
parameter, and the length is solved from it:

```python
LENGTH_RAW   = nape_to_waist - waist_rise - CLEARANCE
LENGTH_FLOOR = ARMHOLE_DEPTH + 70            # below this there is no waistcoat left
LENGTH       = max(LENGTH_RAW, LENGTH_FLOOR)
```

| case | nape→waist | rise | raw | floor | **length** | floored? |
|---|---:|---:|---:|---:|---:|:--|
| default | 445 | 40 | 393.0 | 324.1 | **393.0** | no |
| `high_trouser_band` | 445 | 90 | 343.0 | 324.1 | **343.0** | no |
| extreme | 360 | 110 | **238.0** | 324.1 | **324.1** | **yes** |

That last row is why the floor exists. A short torso under a high band solves to 238 mm
— less than the armhole depth, which is a garment made entirely of armhole. The floor
fires, and `length_floored: true` reports it rather than shipping a hole with shoulders.

### 2. The front closes edge to edge

There is **no button stand**. The two fronts meet at centre front and are held by
hook-and-bar sets sewn behind the edge, so the closure is invisible and the greca runs
uninterrupted to the hem. The front edge is therefore drafted **at** x = 0, which is the
whole difference between a chaleco that closes and a copied waistcoat that gapes.

The consequence for the draft is that **there is no overlap to absorb error**. Every
millimetre of shaping shows as a gap or a strain on the closure line. So both facings are
cut to the **measured** runs off the drawn front, and declared against them:

| edge | measured | facing cut to | match |
|---|---:|---:|:--|
| `front.centre_front` | 227.94 mm | `facing.front_edge` 227.94 | ✅ |
| `front.lapel` | 224.31 mm | `lapel.attach` 224.31 | ✅ |

Declared seams: `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
`facing.front_edge ↔ front.centre_front`, `lapel.attach ↔ front.lapel`.

## The hook column rounds up

`hook_pitch` is a request; the kernel divides the **measured** closure run into whole
intervals and recomputes the pitch so the column lands exactly on the lapel-break and
hem clearances instead of drifting off the last hook.

The rounding goes **up**, not to-nearest, and that is a deliberate correction. A closure
run of 186 mm at a requested 78 mm pitch rounds to-nearest at 2 intervals — a solved
pitch of **93 mm**, well above the request, giving a chaleco with visibly sparse hooks
and a front that pulls open between them. Rounding up gives 3 intervals and **62 mm**,
which tightens the pitch instead. On an edge-to-edge front, tighter is the safe
direction; sparser is a gaping front.

## Clamping

Beyond the length floor, two more bounds that each answer a real combination:

- **The waist is ordered against the chest.** A waist larger than the chest inverts the
  side-seam shaping — the curve bulges outward from the armhole — into a piece whose
  edges cross, which the kernel CCW-normalizes into geometry that has positive area,
  closed edges, and no complaint. It verifies. It cannot be made.
- **The lapel width is capped** at 55% of the front's half-chest. A 130 mm lapel on an
  800 mm chest runs the peak clean off the piece it is cut from; the cap holds it at
  114 mm and reports `lapel_width_capped: true`.
- **The back neck rise is clamped on the drawn value**, not on a local solve variable —
  the same discipline as `button-aid-cuff-shirt`, and for the same reason: clamping the
  solve while drawing the piece at the unclamped rise gives a back shoulder that
  measures something the solve never agreed to, and the seam check catches it at a
  parameter combination that testing the defaults never reaches.

The cartridge was probed at the **minimum and maximum of all 14 parameters**, plus
all-min, all-max, cross extremes, and every `target_piece` at both defaults and all-max
— 69 cases, all `errors=0`, every declared seam ok, no degenerate bbox.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/trouser-hook-bar`**.

`hook_width` is the shared dimension: it drives the solid's `hook_width` and, through
it, the plate length, thickness, wire diameter and gap. The count and the pitch are not
parameters of the hardware at all — they come from the **measured** closure run, which
is the right place for them.

The solid declares `sew_plate` as a `flange` cdg_interface driven by `hook_width`,
`plate_t` and `sew_holes`, and the garment's `edge_to_edge_front` interface is driven by
`hook_width` and `hook_pitch` — so the dimensional-handshake lane has a real coupling on
both sides of the seam.

The set is sewn **behind** the edge. Nothing shows on the face, which is the point of
choosing a hook over a button here.

## Construction notes

Pieces: **front** (cut 2 mirrored), **back** (cut 2 mirrored, joined at centre back),
**facing** (cut 2 mirrored), **lapel** facing (cut 2 mirrored).

- **Fabric.** `lana-peinada-traje` — worsted suiting, 160 °C iron. The **back is cut in
  the suiting**, not in lining: unlike an English waistcoat under a coat, this back is
  part of the suit's face and is seen.
- **Canvas the fronts.** An edge-to-edge closure with no stand shows every ripple, and
  fusible alone will not hold the lapel roll. Haircloth or canvas through the front and
  lapel.
- **Press the lapel roll, never crease it.** The roll line is marked on the lapel
  facing; it is shaped over a ham.
- **Order.** Canvas and pad the fronts. Apply the greca while the fronts are flat —
  soutache over a made-up edge is a different and much harder job. Then the facings,
  then the shoulders and sides, then the hooks, then line.
- **The greca is placement only.** `greca-row-N` are marked lines following the front
  edge and the lapel. `soutache_rows: 0` is the faena chaleco and is a legitimate
  finished garment, not an unfinished one.
- **`trouser-band-clearance`** is marked on both front and back. It is where the trouser
  band starts, and the chaleco's hem must stay above it.

## What is deliberately excluded

**No botonadura de plata. No escudo. No association or team insignia. No braid pattern.**

The silverwork of the gala categories, the greca designs themselves, and the badges of
associations and equipos are the work and the property of the artisans and the families
who own them. The competition dress codes belong to the **Federación Mexicana de
Charrería**. A pattern generator should draw the structure and stop — which is what this
one does.

## Honest simplifications

- The hem is drafted straight. Some chalecos carry a shallow shaping at the side; it is
  regional and is left to the maker.
- The welts are **marked**, not drafted as separate pieces: two lower and one breast, in
  the standard positions. Their bags are cut from the lining.
- The armhole is a bound/faced edge; no sleeve and no armhole facing piece is drafted.
- Lining is noted, not drafted.

---

*Rank 300 of 300. The FC-300 catalog closes here.*
