# Longline underwire bra

A three-piece wired cup on a **longline** band that reaches to the waist, boned vertically
— a deepening of the FC-300 [underwire bra](../../underwire-bra/docs/README.md) with the
same dimensional handshake to the printed Yantra4D underwire, extended down into a
structural long band.

Part of the **Fashion Cabinet Commons** (FC-400, lane 9 — structured intimates). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

> A longline is not a bra with a wider band bolted on. The long band is a structural member
> — its own negative ease and vertical boning are what let it support a larger cup without
> the straps digging.

## Why it earns its rank

**The wire handshake is inherited, and still exact.** A moulded-looking cup out of stable
cloth needs two cones at right angles — a vertical apex seam between two lower sections and
a horizontal seam under an upper section. The cradle's upper edge is the **wire line**,
**solved** to the underwire's own arc:

```
cup_width  ->  the wire's chord AND the cradle's wire-line chord   (one number)
sweep_deg  ->  the wire's arc angle AND the cradle curve's arc angle
    =>  arc length L = R·θ,  R = chord / (2 sin(θ/2))
```

The manifest's `params_map` sends `cup_width` and `sweep_deg` to `bra-underwire`, and both
also drive the garment's own `wire_line` interface, so the drafted channel run, the cup
mouth and the printed wire agree to the tenth of a millimetre — checked by `declare_seam`.

**What makes it longline (the new depth).** Below the cradle, the band runs to the natural
waist: cut at the underbust ring's negative ease at the top, tapering to the waist ring
below. It carries **vertical boning channels** (`bone_count` per side), spaced from the band
width. The long band holds the ribcage and takes support off the shoulders — the depth a
plain underwire band cannot give, and what lets a longline hold a larger cup comfortably.

## Construction notes

Pieces: **cup_lower_inner**, **cup_lower_outer**, **cup_upper** (the three-piece cup),
**cradle** (wire channel frame), **longline_band** (to the waist, boned), **back** (wing).

1. Cone the cup: join the two lower sections at the apex seam, then set the upper section
   on the horizontal cup seam.
2. Set the cup into the cradle along the solved wire line, and topstitch the wire channel
   along the cradle's marked line, closing both ends so the wire tips cannot work through.
3. Attach the cradle and the back wings to the longline band's top edge.
4. Insert vertical boning into the marked channels of the long band.
5. Finish the waist edge with plush-back elastic, the neckline with picot, and close the
   centre back with a long hook-and-eye column.

## Hardware

The underwire is a **Yantra4D solid** (`notion.hardware_ref → bra-underwire`, linked). It is
**never modelled here** — this cartridge draws the channel it lives in, solved to the wire's
own arc. `cup_width → cup_width`, `sweep_deg → sweep_deg`, `wire_d = 1.4 mm`. The boning,
ring/slider strap adjusters and the hook-and-eye column are their own separate items
(spiral steel or synthetic; Yantra4D `bra-ring-slider` and `hook-and-eye`).

## Made to measure

Drafted to **underbust**, **bust** and **waist** girths. Every slider extreme — wire chord
and sweep, longline drop, boning count, negative ease — renders watertight, and the wire /
channel / cup-mouth identity holds across the range.
