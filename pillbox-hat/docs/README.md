# Pillbox Hat

The **classic pillbox**: a flat circular tip on a straight cylindrical side band, no
brim. Cut to the actual head girth and **fully lined**, so the head opening is a clean
bagged-out edge rather than a raw one. Sizing is delegated to the Yantra4D
[`hat-size-reducer`](https://app.yantra4d.com) strip that clips inside the band.

Part of the **Fashion Cabinet Commons** (FC-300 #211, Lane 2 — millinery). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Pieces

Tip (crown) + side band, each repeated in lining — four pieces for the lined hat, two
for the `shell` mode.

## Parameters

`head_girth` (ISO 8559, drives both the band length and the tip radius), `band_height`,
`ease`, `lined`, `seam_allowance`.

## Drafting

The tip is a **48-gon whose radius is corrected** so its perimeter equals the target
head opening exactly — `r = C / (2n·sin(π/n))`. A naive `C/2π` radius under-runs the
circumference by ~0.4 mm at head size, which is enough to show up as seam-check noise;
the correction makes the tip↔band seam exact. The band is a plain rectangle
`head_girth + ease` wide that wraps into a tube, its two end seams joining each other.

## Cross-commons bridge

`notion.hardware_ref` → `hat-size-reducer`, mapping `head_circ → head_girth + ease` and
`strip_height → min(band_height, 40)`. The reducer is **point/slot hardware** — it clips
inside the band rather than being sewn into a garment edge, so it declares no `flange`
interface and the dimensional-coupling rule does not apply. Name resolution is still
enforced by `verify_hardware_links`.

## Provenance
Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.
