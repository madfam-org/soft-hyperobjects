# Bucket Hat

A **made-to-measure bucket hat** drafted from the head girth: a circular **crown**, a
rectangular **side band** (head circumference × crown depth), and a down-sloping
**brim** — a half-annulus cut on the fold (fold + mirror = the full ring). Fashion
Cabinet's classic reversible summer hat, sized to the wearer. A pure soft-goods garment
— **no hardware**.

Part of the **Fashion Cabinet Commons** (FC-200, Lane 3 — accessories). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

## Modes

| Mode | Pieces | Description |
| :--- | :--- | :--- |
| **Bucket Hat** | `crown`, `side-band`, `brim` | Crown circle + side wall + brim ring. |

## Parameters

| Parameter | Default | Notes |
| :--- | :--- | :--- |
| `head_girth` | 570 mm | Head circumference where the hat sits (bound to the `head_girth` landmark). |
| `crown_depth` | 90 mm | How deep the side band sits down the head. |
| `brim_width` | 60 mm | How far the brim extends past the head. |
| `ease` | 10 mm | Added to the head girth for comfort. |

## Drafting

The head opening radius is `(head_girth + ease) / 2π`. The **crown** is a full circle
of that radius; the **side band** is a `head_eff × crown_depth` rectangle that wraps to
a tube and seams to the crown at the top and the brim at the bottom; the **brim** is a
half-annulus (inner = head radius, outer = head radius + brim width) cut on the straight
center edge and mirrored into the full ring. All circular edges are 48-segment polygon
approximations.

## Provenance

Original draft for Fashion Cabinet. Commons license **CERN-OHL-W-2.0** (ruled FC1, 2026-08-25).
