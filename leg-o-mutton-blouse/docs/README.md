# Leg-o'-Mutton Blouse

**FC-300 · Costume & historical · c. 1893–1897**

The 1890s shirtwaist with the enormous gigot sleeve, drafted on period construction logic.

## What it is

The leg-o'-mutton (gigot) sleeve is hugely full from shoulder to elbow and close from
elbow to wrist — the shape of a leg of mutton, which is where the name comes from. It is
the defining garment of the decade, and it lives or dies on **one relationship**, which is
why it earns a cartridge of its own rather than a preset on `blouse`.

The body is a shirtwaist: worn loose, gathered onto the skirt band and bloused over it as
the period "pouter pigeon" front, closed with small buttons up the centre front under a
standing collar band.

## Why it earns a commons rank

This garment is the case where the **usual pattern-checking rule is exactly wrong**.

On an ordinary set-in sleeve, the cap is drafted to the armscye plus a small ease, and any
larger discrepancy is a defect. Apply that rule here and it destroys the garment: the
armhole gets enlarged to "fit" the enormous sleeve, the shoulder point drops off the
shoulder, and the silhouette is gone. **The armhole does not grow to match the sleeve.**
The whole technique is a sleeve head two to three times the armscye gathered into an
armhole of *ordinary* size.

Encoding the real relationship — rather than the general rule — is what keeps the
technique from being quietly normalised away by automated checking.

## Construction notes

### The seam that must solve, and why it is unusual

The honest constraint here is not `cap ≈ armscye`. It is:

```
cap length  =  armscye × gather_ratio
```

because the **ratio** is what the maker actually controls, and the surplus is what they
have to distribute with their fingers over two rows of gathering stitch.

So the cartridge:

1. **measures** the armscye off the built front and back pieces;
2. **solves** the sleeve head's width by bisection until the built cap *measures* exactly
   `armscye × gather_ratio`;
3. declares the seam with the gathered-away surplus as its **declared ease**.

That third step is the important one. The verifier then checks the real relationship —
cap equals armscye plus the surplus the maker gathers away — instead of being told to
ignore a several-hundred-millimetre discrepancy behind a widened tolerance.

At default settings the numbers are: armscye 447.8 mm, cap 1074.8 mm, **residual
0.0000 mm**, surplus gathered away **627.0 mm**. The achieved gather ratio comes out at
exactly the requested value across the whole parameter range, from 1.15 to 3.2.

That surplus figure is the practically useful output. 627 mm of gathering distributed over
a 448 mm armhole is a real amount of work, and knowing it before cutting is the difference
between planning the sleeve and discovering it.

### The gathers do not go all the way round

The gathering zone runs over the **top** of the head only; the underarm portion is set in
flat. This is what keeps the sleeve from bunching in the armpit, and it is marked on the
piece as two trace internals rather than left to judgement.

### The sleeve must be supported from inside

A gigot is held out by **stiffening inside the head** — crinoline, haircloth, or net. An
unsupported gigot collapses within an hour of wear no matter how much fabric is gathered
into it, and no amount of extra gathering substitutes for the support. It is in the BOM
for that reason.

A crisp light cloth holds the sleeve out; a soft drapey one collapses it and loses the
silhouette even with the stiffening in.

The marker estimate assumes only a 68% yield, lower than the other cartridges in this
wave — the gigot sleeve is an awkward shape and nests badly, so the piece areas flatter
the real fabric requirement.

### Shoulder seams

Front and back carry different neck widths, so each panel's shoulder-point drop is solved
against a shared reference length chosen so the wider-necked panel still has a real
solution. Both shoulder seams therefore measure the same by construction, with no
degenerate fallback and no widened tolerance.

## Provenance

This is an original draft built on the documented construction tradition of the mid-1890s
shirtwaist: a loose body bloused over the skirt band, centre-front buttons, a standing
collar band, and a gigot sleeve full above the elbow and close below it whose head is
gathered into an armscye of ordinary size and supported from inside. It is **not** traced
from any single extant garment, and it is not a transcription of any published pattern.
The features above are the well-attested general characteristics of the type, described
here as a construction tradition rather than attributed to a specific source.

The sleeve fullness of the 1890s changed year by year, and `gather_ratio` is offered as a
dial across that range rather than as a claim about any particular season.

Anyone working toward museum-grade accuracy should measure an extant garment or consult a
scholarly pattern-drafting source; this cartridge is a faithful working draft of the
*type*, not a reproduction of a particular object.

## Pieces

| Piece | Cut | Notes |
|---|---|---|
| `front` | 2 mirrored | CF button stand, waist gather trace |
| `back` | 1 on fold | yoke line, waist gather trace |
| `sleeve` | 2 mirrored | head width SOLVED; gather-zone limits marked |
| `cuff` | 2 | close cuff with a button |
| `collar` | 1 on fold | cut to the MEASURED neck run |

## Hardware bridge

- `sew-through-button` — front and cuff buttons; `hole_spacing` ← `button_pitch ÷ 10`,
  `card_count` ← `round(back_length ÷ button_pitch) + 2`

## Fabric

Cotton lawn, batiste, or a light wool is the period cloth. `popelina-algodon` is the
closest card in the Fashion Cabinet material set. Crispness matters more than weight here:
the cloth has to help hold the sleeve out.
