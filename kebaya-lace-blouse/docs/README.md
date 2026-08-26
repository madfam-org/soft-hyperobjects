# Kebaya lace blouse

The fitted front-opening blouse of Indonesia, Malaysia, Brunei, Singapore and the Peranakan
world — worn over a **kemben** or camisole with a batik or **songket** sarong, and made in
sheer embroidered voile, lace, or fine cotton.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — Nusantara / Southeast Asia).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> A fitted draft with a set-in sleeve hung from a *measured* armscye — instead of a boxy
> lace top that keeps neither the kebaya's close fit nor its clean-hanging sleeve.

## Provenance

The **kebaya** is a fitted, front-opening blouse worn across maritime Southeast Asia — Java
and the rest of Indonesia, the Malay Peninsula, Brunei, Singapore, and among the Peranakan
(Straits Chinese) as the **kebaya nyonya**. It is worn over a **kemben** or camisole with a
batik or songket wrapped skirt, and its cloth is sheer — embroidered voile, lace, or fine
cotton. It is held closed not by buttons but by a row of hooks or by **kerongsang** — the
linked brooches that are the kebaya's signature jewellery. In 2023 the kebaya was jointly
inscribed on UNESCO's Representative List of Intangible Cultural Heritage by Brunei,
Indonesia, Malaysia, Singapore and Thailand.

This cartridge drafts the fitted blouse as an original construction draft, not a copy of any
particular dressmaker's pattern, and draws **no** lace or embroidery.

## Why it earns its rank

**The body is fitted, through the bust and waist.** A bust dart and a waist take-in give the
kebaya its close fit; the waist is *solved* from the three girths (48.8 mm of suppression per
panel at the defaults), with a clamp that yields no dart — never a reversed one — when the
waist exceeds the bust.

**The sleeve is set in, to the measured armscye.** The long fitted sleeve's cap is iterated
until the drawn cap curve equals the measured front + back armhole plus ease:

| armscye | cap target | cap drawn |
|---:|---:|---:|
| 436.3 mm | 450.3 mm | 450.3 mm |

The declared seam `sleeve.cap ↔ front.armhole + back.armhole` proves it. The front opens
straight down centre front and curves away to a point below the level side hem, and it is held
by **hooks** (bridged to the Yantra4D `hook-and-eye` solid, driven from `closure_span`) or by
**kerongsang** brooches.

## What is deliberately out of scope

No lace pattern or embroidery motif is drawn, and no region-specific design is reproduced. The
lace and embroidery — the identity of a kebaya — are the maker's and the fabric's.

## Parameters

`bust_girth`, `waist_girth`, `hip_girth`, `kebaya_length`, `neck_girth`, `shoulder_width`,
`armhole_depth`, `bust_to_waist`, `sleeve_length`, `wrist_girth`, `front_point`, `bust_ease`,
`closure_span`, `closure_count`, `seam_allowance`, `hem_allowance`.

## Pieces

- **front** — fitted front (cut 2), bust dart, curved-away front opening.
- **back** — fitted back, cut on the CB fold, waist shaping.
- **sleeve** — long sleeve (cut 2), cap measured to the armscye.

## Hardware

Front hook-and-eye via the Yantra4D `hook-and-eye` cartridge (linked), sized from the closure
span. Kerongsang brooches are the traditional alternative — those are jewellery, not drafted.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the shared, UNESCO-inscribed heritage of the kebaya; the lace, the
embroidery and their meaning are the makers' and the communities'.
