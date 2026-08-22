# Hakama (袴)

The pleated over-garment worn from the waist down over a kimono: formal wear, and the
working dress of **kendō**, **aikidō**, **kyūdō** and Shintō practice. This cartridge
drafts the **馬乗り** (*umanori*, "horse-riding") form — the **divided** hakama, split into
two legs.

Part of the **Fashion Cabinet Commons** (FC-300, long-tail — heritage — Japanese). Official
visualizer and configurator: [Fashion Cabinet](https://fashioncabinet.app).

> An open, made-to-measure draft puts the pleat geometry back in the hands of the people
> who wear the garment — practitioners who need it to fit their own body and their own
> height, not a size chart.

## Provenance

The hakama descends from the divided riding trousers of the Heian court and became, over
the Kamakura and Edo periods, both the formal lower garment of the samurai class and the
practical one of anyone who worked or rode. Today it is worn at graduations and weddings,
by Shintō priests and *miko*, and as everyday practice dress across the classical and
modern budō.

Two forms exist and they are **not** variants of one another. The **umanori** (馬乗り) is
divided into two legs; the **andon** (行灯, "lantern") is undivided — a skirt. This
cartridge drafts the umanori only. An andon hakama is a different garment with a different
construction, not this pattern with a switch turned off, and pretending otherwise would
teach the maker something false.

This is an original draft made from the garment's published construction logic. It is not
a copy of any particular school's or maker's pattern.

## Why it earns its rank

**It has no crotch curve, and that is the point.** Every Western trouser draft in this
commons begins with a rise and a seat curve. The hakama has neither. The leg is a straight
panel; the division is a straight vertical seam that stops partway up. The unsewn
remainder above that stop is the **相引き** (*aibiki*) — the open side gap that lets the
garment wrap and lets the wearer move. Drafting a rise here would be importing a solution
to a problem the tradition solved differently.

**The pleating is asymmetric and structural, not decorative.** Five pleats in front
(read traditionally as five virtues), two behind. This is not a stylistic default that
could be set to 4/4 — the front carries the wrap overlap and the back is bounded by the
koshiita board, so the two sides pleat into **genuinely different finished spans**. Each
side's pleat depth is therefore back-solved *independently* from its own integer count
against its own span, so both pleatings tile their bands exactly. The manifest warns if
you try to make the counts equal.

**The koshiita is a trapezoid, and the draft respects the consequence.** The 腰板
(*koshiita*) back board tapers inward down its sides, which means its **bottom edge is
shorter than its top**. The bottom is the edge the back pleating actually sews to. This
draft *measures* that bottom edge from the drafted polygon and reconciles the back
pleating against the measurement — rather than reusing the top width and quietly
accumulating an error equal to twice the taper.

**Loom width is real, and it is narrow.** Traditional 反物 (*tanmono*) bolt is roughly
380 mm wide. That narrowness is exactly why a hakama is always pieced from multiple
widths, and the panel counts here are solved from the actual `fabric_width` you enter.

## Construction notes

Pieces: **front** (maemigoro), **back** (ushiromigoro), **koshiita** (board, cut 2 —
outer and facing), **himo_long** (front straps, cut 2), **himo_short** (back straps,
cut 2).

1. Join the front widths into one flat front; the same for the back. Hem both while flat.
2. Sew the leg-division seam up each `inner` edge from the hem, **stopping** at the
   `aibiki-stop` marking. Do not continue past it — the opening above is the garment.
3. Close the side seams (`outer` to `outer`), also stopping to leave the aibiki open.
4. Pleat the front to its marked repeat (five knife pleats) and the back to its own
   (two). Baste, then edge-stitch each pleat down its full visible length — this is what
   makes hakama pleats hold through years of practice.
5. Set the back pleating into the koshiita's **bottom** edge. Interface or insert a
   stiffener into the board; it must hold its shape in the small of the back.
6. Attach the two long himo at the front panel's upper corners and the two short himo at
   the board's upper corners (`himo-anchor` markings).

The straps are tied in a fixed sequence — front straps wrap back, cross, and return to
the front; back straps come forward over them — which is why the two pairs are
deliberately different lengths, both solved here as real wrap circuits.

## Hardware

**None.** The hakama is entirely self-fastening by its four himo. There is no
`notion.hardware_ref` on this cartridge and there should not be: adding a buckle, snap or
hook would be an invention, not a hakama.

## What is deliberately excluded

- **行灯袴** (*andon hakama*) — the undivided, skirt-like form. A different garment, not a
  parameter.
- **長袴** (*nagabakama*) — the long trailing hakama of the court and of Noh theatre.
- The **colours, crests and specific forms marking Shintō office or martial rank.** These
  carry standing and religious meaning. They are earned or conferred, not selected, and a
  cartridge that offered them as options would be misrepresenting what they are.

Surface treatment, crests and dyeing are left to the maker.
