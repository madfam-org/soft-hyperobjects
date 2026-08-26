# Eight-yard kilt

The traditional Scottish kilt: a knife-pleated wrap of about **eight yards** of wool tartan,
flat-fronted (two overlapping aprons) with the whole surplus pleated across the back, at the
natural waist, closed by leather **straps and buckles**.

Part of the **Fashion Cabinet Commons** (FC-400, lane 10 — heritage). Official visualizer and
configurator: [Fashion Cabinet](https://fashioncabinet.app).

> What makes an eight-yard kilt correct is **pleating to the sett** — each pleat showing one full
> tartan repeat. That is a discrete count tied to the cloth's own repeat, not a free "fullness".

## Provenance

The kilt is Scottish Highland dress with deep clan and regimental associations — carried by the
**tartan**, which this cartridge does **not** draw. The sett is treated as a **size**, not a
specific clan pattern, and no tartan is invented or assigned.

## Why it earns its rank

**The pleats are set to the sett.** A kilt is pleated so each pleat shows one full tartan repeat,
so the pleat **depth is the sett width** and the number of pleats is the back width over the
pleat **face** (the visible width, a fraction of the sett). This cartridge takes the sett as a
parameter, **solves an integer pleat count** and the total cloth those pleats consume, and
reports how close it lands to eight yards — so a maker can pleat to the stripe with confidence.

**The front is two flat aprons, the back is all pleats.** The under- and over-apron wrap flat
across the front (no pleats); the entire pleated section is at the back and sides, sewn down
through the tapered **fell** and swinging free below it.

**The closure is straps and buckles.** Two or three leather straps pass through buckles at the
waist. The buckle is the Yantra4D `strap-buckle`, and `strap_w` drives both the drafted strap and
the buckle's webbing slot, so the strap threads by construction.

## Construction notes

Pieces: **under_apron** (cut 1, flat), **over_apron** (cut 1, flat, visible front),
**pleated_back** (cut 1, flat cloth with pleat folds marked), **strap** (cut per `strap_count`).

1. Knife-pleat the back section along the marked fold lines, each pleat a full sett; the flat
   cloth gathers up to the apron edges (a pleated join, so the seam carries the take-up as ease).
2. Sew the pleats down through the fell, tapering them from the waist to the hip; below the fell
   they hang free.
3. Set the aprons and finish the waist with a stiffened band.
4. Fit the straps and buckles at the waist.

## Hardware

The straps and buckles are **Yantra4D solids** (`notion.hardware_ref → strap-buckle`, linked):
`webbing → strap_w`, `web_t = 3.0 mm`.

## Made to measure

Drafted to **waist** and **hip** girths, **kilt** length and the tartan **sett**. The pleats are
solved to the sett and the yardage is reported; every slider extreme renders watertight.
