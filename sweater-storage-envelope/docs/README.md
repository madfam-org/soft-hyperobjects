# Sweater Storage Envelope

The flat folder that keeps **knitwear off a hanger**. A hung sweater grows shoulder horns
and stretches at the yoke; the answer is to store it flat, and this is the envelope that
does it — one body panel that folds up into a shallow tray, four corner wall wedges that
give the tray depth without a hard corner seam, and a shaped flap that closes over the top
on Yantra4D [`sew-on-snap`](https://app.yantra4d.com) fasteners.

Part of the **Fashion Cabinet Commons** (FC-300, rank #255 — care & keeping). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabi.net).

## Why it earns its rank

The damage a hanger does to knitwear is slow, invisible for a season, and permanent — and
the retail answer is a zip-top vinyl box that yellows and cracks. A cotton tray cut to the
shelf someone actually has stores the sweater in the one position that does not stretch
it, and can go through a wash when the shelf gets dusty.

## Pieces

`body` (tray floor plus walls, cut 1 — fold lines marked, not cut) + `wall` (corner wedge,
cut 4, two per end) + `flap` (closing lid with snap positions marked, cut 1).

## The seam that solves

The tray is a **wrapped box**: the body's two side edges each fold up by `wall_height`,
and a trapezoidal wedge fills the corner. The wedge's sloped edge and the body's
fold-relief notch must be the **same length**, or the corner either gapes or buckles. The
wedge slope is drafted as a measured polyline and the body's relief cut is built from the
**same points**, so the corner closes exactly. The flap's curved lip is measured too — its
front edge must equal the tray's mouth width.

## Construction notes

Press the fold lines before sewing the wedges; the tray's shape comes from the creases,
not from the seams. Interface the flap only — a stiffened floor makes the envelope hard to
slide onto a shelf. Snap positions are marked on `flap` rather than drafted as holes, so
the maker can shift them once the folded sweater's real bulk is known.

## Cross-commons bridge

`notion.hardware_ref` → `sew-on-snap`, mapping `snap_dia → snap_diameter`, `sew_holes → 4`,
and `stud_dia → snap_diameter * 0.4`. **Dimensional**: the snap's sewn `sew_face` flange is
driven by `snap_dia`, and the same `snap_diameter` drives this envelope's `snap_seat`
interface — so the handshake is dimensional, not nominal.

## Provenance

Original draft for Fashion Cabinet. `LicenseRef-FC1-pending`.
