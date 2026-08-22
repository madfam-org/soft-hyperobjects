# Baju Kurung

A loose, unfitted tunic worn over a wrapped skirt (*kain sarung* or *kain lepas*),
drafted in the traditional gusseted cut.

## Provenance

The baju kurung is the national dress of Malaysia and Brunei, and is widely worn in
Singapore, southern Thailand and the Indonesian Riau islands. Its name is literal:
*kurung* means **enclosed**, and the whole design logic of the garment is that it
skims the body rather than tracing it. A fitted baju kurung is a contradiction in
terms — which is why this cartridge warns when `body_ease` drops below 120 mm.

The form is generally credited to the 15th-century Melaka sultanate and took its
modern silhouette over the following centuries; the paired *baju kurung Teluk Belanga*
(a plain round neck with a rolled, hand-stitched finish) and *baju kurung Cekak
Musang* (a full stand collar with a placket) are the two classic neck treatments. This
cartridge drafts the **plain slit neck** (*belah*) with a single throat button, which
is the everyday form and the one whose geometry generalises; a Cekak Musang stand
collar is a genuinely different draft and is left to a future cartridge rather than
faked with a parameter.

The baju kurung is everyday and festive dress rather than restricted or ceremonial
wear, so drafting it for the commons raises no appropriation concern of the kind that
would apply to, say, ranked or religious garments. What it does deserve is accuracy:
the *kekek* and *pesak* are not decorative flourishes to be dropped for convenience,
they are the construction.

## Why this earns a commons rank

This is one of the clearest surviving examples of **rectangular-cut clothing** — a
whole garment engineered around the loom's output and the scissors' limits.

Every seam is straight. There is no curved armscye, no dart, no shaped shoulder, and
no bias. The shaping is done entirely by two small inserted pieces:

- the **kekek**, a square underarm gusset, and
- the **pesak**, a triangular side gore.

That matters to the commons for three reasons. It **wastes almost no cloth** — the
pieces nest as rectangles and triangles. It can be **cut by hand** without a curved
ruler or a printer. And the kekek is a **repair strategy**: the underarm is the first
place any shirt fails, and here it is a replaceable square rather than a rebuilt
armscye.

## Construction notes

Four pieces: **body** (badan, cut 2 on the fold), **sleeve** (lengan, cut 2 on the
fold), **kekek** (cut 2) and **pesak** (cut 2).

**The underarm junction is solved, not assumed.** The body's armhole is a *slanted*
edge running from the shoulder end down to the side seam, so its true length is the
hypotenuse — not the vertical drop, which is the easy mistake. The kernel measures
that hypotenuse and then solves the sleeve head **from** it, less one kekek side. The
declared seam is therefore three-way — `body.armhole` ↔ `sleeve.head + kekek.to_body_a`
— and it proves the junction actually closes. If a large `kekek_side` would leave less
than 40 mm of sleeve head, the kernel reduces the gusset rather than emitting a
pattern that cannot be sewn.

**The gore sets in flat.** The pesak's slant edge is measured from its own geometry,
and the body's `side_lower` edge is then solved to that measured length. Both of the
gore's slants are checked against the body edge, so a pesak that would pucker fails
the run rather than reaching the cutting table.

**The kekek is square and stays square.** A seam check asserts `to_body_a` equals
`to_sleeve_a`. Squareness is what converts two straight seams into a joint that lifts;
a "gusset" cut as a diamond or a rectangle does not do the same work.

**Order of work.** Set the kekek into the sleeve underarm first, then join that unit
to the body armhole, matching the notch. Insert the pesak into each side seam, gore
point to the marked notch. Flat-fell the straight seams. Finish the belah with a
facing and set the single throat button last.

## Hardware

The throat button bridges to the Yantra4D **`sew-through-button`** solid. `button_ligne`
drives the printed button and the body's marked button seat together. Two holes rather
than four — a light throat closure on a fine cloth, matching the scale of the garment.

## Honest simplifications

- **Neck treatment.** Only the plain *belah* slit is drafted. Both the Teluk Belanga
  rolled finish and the Cekak Musang stand collar are distinct constructions; naming
  them here and not faking them is the honest choice.
- **The skirt is not included.** The baju kurung is a two-piece outfit; the lower
  *kain* is a separate wrapped garment and is not drafted by this cartridge.
- **No songket or embroidery placement is marked.** Ornament, and especially woven
  songket motif placement, belongs to the maker and the tradition, not to a default.
- The sleeve is drafted as a straight taper. Some regional cuts use a second small
  gore at the cuff; that is a variant rather than the common form.
