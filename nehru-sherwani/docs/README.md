# Sherwani

The fitted long formal coat of South Asia — the men's ceremonial dress of weddings and state
occasions across India, Pakistan and Bangladesh, worn over a kurta and churidar. A **tailored,
made-to-measure** garment: fitted through the waist, buttoned all the way up to a raised stand
collar (the **Nehru** / **bandhgala** collar), with set-in sleeves and a flared skirt.

Part of the **Fashion Cabinet Commons** (FC-500, heritage — South Asian; made-to-measure).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A made-to-measure coat block — waist solved from the body, sleeve hung from a measured
> armscye, collar cut to the measured neckline — for a garment that has to fit: a wedding coat.

## Provenance

The **sherwani** is the men's formal coat of the Indian subcontinent, descended from the
court dress of the Mughal and princely eras and now the standard **wedding and ceremonial**
coat across India, Pakistan and Bangladesh. Its close relative the **bandhgala** ("closed
neck", also called the Jodhpuri or, in its jacket form, the "Nehru jacket") shares the raised
stand collar. It is a fitted, canvassed coat, buttoned the full length of the front to the
collar, with set-in sleeves and a skirt that flares gently below the waist, worn over a
**kurta** and **churidar**.

This cartridge drafts the coat as a made-to-measure block and draws no surface embroidery.

## Why it earns its rank

**The body is fitted, and the waist is solved from the measures.** The waist is solved from
the chest-waist-hip measurements and suppressed with a side take-in plus a vertical dart; the
skirt flares to a hem quarter of `390.8 mm` at the defaults. It is drafted from the body, not a
size chart — the point of a made-to-measure tier.

**The sleeve cap is cut to the measured armscye.** The cap is iterated until it equals the
measured front + back armhole (509.2 mm) plus a real tailored ease (cap drawn 529.2 mm), and
the declared seam proves it.

**The stand collar is cut to the measured neckline.** The bandhgala stand is cut to the
measured neck run (`collar_run_mm = 474.6`), off the naive `neck_girth + ease` estimate by
`collar_vs_neck_estimate_mm = 38.6`, so it closes cleanly at the throat. The full front carries
real **shank buttons**, bridged to the Yantra4D `shank-button-solid` and driven by
`button_diameter`.

## What is deliberately out of scope

No **zardozi** or thread-embroidery motif is drawn. The surface work that makes a particular
sherwani is the **karigar**'s (the embroiderer's) — this cartridge draws the tailored coat and
none of its ornament.

## Parameters

`chest_girth`, `waist_girth`, `hip_girth`, `sherwani_length`, `nape_to_waist`, `neck_girth`,
`shoulder_width`, `sleeve_length`, `armhole_depth`, `wrist_girth`, `collar_height`,
`skirt_flare`, `chest_ease`, `button_diameter`, `button_count`, `back_vent`, `seam_allowance`,
`hem_allowance`. The girth and length parameters carry ISO 8559 measurement codes for
made-to-measure fitting.

## Pieces

- **front** — fitted front (cut 2), full button front, waist dart, flared skirt.
- **back** — fitted back, cut on the CB fold, waist dart, flared skirt, centre vent.
- **sleeve** — long sleeve (cut 2), cap measured to the armscye.
- **collar** — bandhgala stand collar (cut 2), cut to the measured neckline.

## Hardware

Full front shank buttons via the Yantra4D `shank-button-solid` cartridge (linked), driven by
the button diameter.

## License & provenance

Original draft for Fashion Cabinet. Licensed **CERN-OHL-W-2.0** (Fashion Cabinet commons).
Offered with respect for the living formal-dress traditions of South Asia; the zardozi and
embroidery are the karigars'.
