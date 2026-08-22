# Leheṅgā (लहंगा)

The long, full, **gored** skirt of northern and western South Asia — also **ghāgrā**
(घाघरा), Gujarati **chaniya**, Tamil **pāvāḍai**. It is worn with a fitted **cholī** blouse
(drafted in this commons as [`sari-blouse`](../../sari-blouse/)) and a **dupaṭṭā** draped
over.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — South Asian).
Official visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> Solving the true cone puts a correct, made-to-measure leheṅgā within reach of anyone
> with cloth and a table — at any waist and any height, not only at the sizes a shop
> stocks.

## Provenance

The leheṅgā is both an everyday and a ceremonial garment. In its plain form it is the
working skirt of Rajasthan and Gujarat, worn daily and repaired for years. In its worked
form it is the standard festival and bridal skirt across much of northern and western
South Asia. The two share one cut and differ in cloth and in surface work.

This is an original draft made from the garment's construction logic — the gored,
cut-in-fullness skirt — not a copy of any particular workshop's or region's pattern.

## Why it earns its rank

**A leheṅgā is not a gathered rectangle, and this commons already has those.** The chima,
the sarafan and the dirndl all get their fullness by pleating or gathering a straight
panel into a band. The leheṅgā gets it from the **cut**: the skirt is assembled from
**kalī**, tapered gores narrow at the waist and wide at the hem. That is why the waist
stays flat and fitted while the hem carries several metres of sweep — and why heavy zarī
work does not collapse the waistline the way it would on a gathered skirt.

**The cone is solved properly, and this is the whole point of the cartridge.** A gored
skirt is a section of a **conical frustum**. Here is the mistake almost every amateur draft
makes:

> Draw a trapezoid whose *height* is the requested skirt length.

That trapezoid's **side edges are longer than its height** — and the side edge is what the
wearer actually measures down the finished skirt. So the skirt comes out too long, and
because the error grows with the sweep, the hem does not level. On paper it is invisible.
In silk it is expensive.

This draft inverts the relationship:

1. The radii come from the two circuits directly — `r = C / 2π` for waist and hem.
2. The **slant** — the distance down the cone's own surface — *is* the finished length the
   wearer asked for.
3. The drafted panel **height** is then back-solved by Pythagoras from the slant and the
   radial run.

At the defaults, slant = 1000 mm but drafted panel height = **836.8 mm**, with a radial run
of 547.5 mm. Push the sweep to 6500 mm and the radial run grows to 913.6 mm, so the panel
flattens to 406.7 mm — real cone behaviour, not a scaled trapezoid. The equal-sides seam
check on the gore seams is what proves the geometry closed.

**The hem is a circuit, not a width.** `hem_sweep` is the full circumference the hem
describes; the integer gore count divides it. The manifest warns when a requested sweep
would need more length than given — i.e. when the cone would have to flatten past a full
circle.

## Construction notes

Pieces: **waistband** (kamarband, cut 2 — outer and facing), **kali** (gore, cut *n*), and
**border** (hem strip, cut only when `border_depth` > 0).

1. Cut the gores nested **tip up, tip down** across the cloth — the draft reports how many
   fit per width. This alternation is what keeps a gored skirt's yardage reasonable.
2. Join the gores at their side seams. These seams are long and run close to the bias;
   sew them with a walking foot or plenty of pins, and let the assembled skirt **hang for
   a day** before hemming so the bias settles.
3. Set the assembled gore tops into the waistband. The band carries an underlap for the
   closure, so the small surplus is declared as ease rather than reading as a mismatch.
4. Insert the invisible zip at the left side seam, running down from the band.
5. If working a border, apply it after the skirt hangs and before the final hem, following
   the assembled hem curve. The `border-field` markings on each gore show where the field
   sits relative to the gore seams — surface work is organised around those seams.
6. Hem last, trueing the hem against the floor rather than against the pattern.

A worked leheṅgā is always **lined**, and the lining takes the same gores.

## Hardware

The side closure bridges to the Yantra4D `invisible-zipper` solid via
`notion.hardware_ref`. `zip_length` and `tape_width` drive both the drafted zip seat on
the waistband and the printed solid's `tape_edge` flange, so the garment's edge and the
hardware's sewn edge are dimensionally coupled rather than merely named.

## What is deliberately excluded

**The surface work is not drafted.** **Zarī**, **zardozī**, **gōṭā pattī**, **śīśā**
(mirror work) and **bandhanī** are named crafts with distinct regional lineages and
specialist practitioners, and their motifs and placement carry community, occasion and
family meaning. This cartridge marks the **border field** and the panel seams that such
work is organised around, and leaves the work itself to the artisans whose knowledge it is.

**Bridal leheṅgā as a category is not encoded** — its prescribed colours and elements vary
by community and are not properties of a skirt. This is a skirt draft, not a wedding.
