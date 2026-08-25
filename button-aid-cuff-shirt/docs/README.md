# Button-Aid Cuff Shirt

A shirt whose cuffs are drafted for the hand that cannot help. Wave FC3-K (long-tail
band, rank 298) of the FC-300 commons.

## What it is

| Piece | Cut | Role |
|---|---|---|
| `front` | 2 mirrored | Shirt front, placket cut on. Deliberately ordinary. |
| `back` | 1 on fold | Shirt back; the back neck width is solved from the measured front shoulder. |
| `sleeve` | 2 mirrored | One-piece sleeve, cap solved to the measured armholes, with a long placket slit. |
| `cuff` | 2 mirrored | **The piece.** Solved open circuit, aid loop tab, long buttonhole, stiffened underlap. |

## Why it earns a commons rank

One-handed dressing has a specific, asymmetric problem that most adaptive shirts miss.
A front placket can be managed slowly, badly, but managed. **The cuff of the working
arm cannot be buttoned at all** — the only hand that could close it is inside it.

The two commercial answers both give something away:

- **Sew the cuff shut.** It then has to pass over the hand, so it must be enormous, so
  it flaps all day and the shirt stops looking like a shirt.
- **Sell a button hook separately.** Fine, except no shirt is drafted to receive one,
  and an ordinary cuff fights the tool in three separate ways.

Neighbours in this commons that are adjacent and different: **`magnetic-placket-shirt`**
(rank 246) removes the pinch from the *front* with magnetic covers — it is the same
family and the opposite half of the garment; **`one-hand-wrap-top`** (248) avoids
fastenings altogether. This cartridge takes the harder position: keep the buttons, keep
the shirt looking like a shirt, and make the *pattern* do the accommodating.

## What a button hook needs, and how the cuff provides it

A hook (`yantra4d/button-hook-aid`) is a wire loop on a handle. It needs three things
an ordinary cuff does not give, and all three are drafted:

**1. Somewhere to pull.** The hook must catch something, and the buttonhole is already
occupied — by the hook. So the cuff carries a sewn **`loop-tab`** at the overlap end,
sized to the aid's `hook_loop`, sitting *past* the buttonhole so pulling it drags the
hole onto the button in a straight line rather than twisting the cuff.

**2. Room for the wire to enter.** The wire passes on **both** sides of the button's
shank, so the buttonhole is cut for the wire twice over plus a working clearance:

```python
BUTTONHOLE = button_dia + 2 * hook_wire + 2.5     # not the usual button_dia + 2
```

| case | button | naive hole | **cut hole** | gain |
|---|---:|---:|---:|---:|
| default | 15 | 17.0 | **21.9 mm** | +4.9 |
| `big_button_low_dexterity` | 24 | 26.0 | **32.9 mm** | +6.9 |

Five millimetres sounds trivial until it is the difference between a loop that passes
and a loop that jams while a person is holding the tool in their teeth.

**3. A cuff that stays open while it is worked.** An unbuttoned cuff collapses under
its own drape and puts the button *behind* the buttonhole, where nothing can reach it.
So the underlap is interfaced to its end (`underlap-stiffening`), holding the two ends
apart in the plane the hook works in.

## The seam that had to solve

**The cuff is a two-position closure, and the pattern owes the maker both positions.**

Closed, it sits at the wrist. Open — flat, while the hook works — it must clear the
**hand**, because a one-handed wearer puts the arm in *before* the cuff can be closed.
Those are two different girths. The naive draft sets the cuff to the wrist, adds a
fixed 30 mm extension, and discovers at the fitting that the hand does not go through.

So `hand_girth` is a real parameter and the underlap is **solved upward**:

```python
CLOSED       = wrist_girth + wrist_ease
OVERLAP      = button_dia + 14                  # fixed by the button it carries
PASS_NEEDED  = hand_girth * (1 - 0.03)          # a woven cuff gives a little
UNDERLAP     = max(22, PASS_NEEDED - CLOSED - OVERLAP)
OPEN_CIRCUIT = CLOSED + OVERLAP + UNDERLAP
```

| case | wrist | hand | closed | underlap | **open** | clearance | grew |
|---|---:|---:|---:|---:|---:|---:|---:|
| default | 175 | 215 | 203.0 | 22.0 | **254.0** | 45.5 | 0 |
| `large_hand_narrow_wrist` | 170 | 290 | 185.0 | **67.3** | **281.3** | 0.0 | **+45.3 mm** |
| extreme (130 wrist, 340 hand) | 130 | 340 | 140.0 | **160.8** | **329.8** | 0.0 | **+138.8 mm** |

`underlap_grew_mm` is reported, so the accommodation is a number on the pattern rather
than a surprise at the fitting. And the cuff's `attach` edge is declared against the
sleeve hem with the two extensions as ease — so a cuff cut to the wrist alone, the naive
draft, cannot pass the seam check.

Declared seams: `front.side ↔ back.side`, `front.shoulder ↔ back.shoulder`,
`sleeve.cap ↔ front.armhole + back.armhole` (ease 14 mm), and
`cuff.attach ↔ sleeve.hem` with the solved extensions as declared ease.

## Clamping, and a bug the extremes sweep caught

Three derived dimensions are clamped, and one of them was found the hard way.

- **The sleeve hem is capped at the biceps.** A 340 mm hand on a 760 mm chest solves a
  cuff wider than the sleeve it hangs from — an inverted taper whose edges cross, which
  the kernel CCW-normalizes into a piece that has positive area, closed edges, and no
  complaint. It verifies. It cannot be sewn.
- **The cuff depth is floored** at `button_dia + hook_loop/2 + 24`, so neither the
  buttonhole run nor the pull tab lands on an edge.
- **The back neck rise is clamped on the drawn value, not on the solve.** The back neck
  width is solved from the front's measured shoulder using a right triangle whose
  vertical leg is the rise. A narrow shoulder with a deep neck (340 mm / 520 mm) makes
  that rise *exceed* the shoulder length — 76.5 mm of rise against an 86.3 mm shoulder.
  Clamping only the solve's local variable while drawing the piece at the unclamped rise
  gives a drafted back shoulder of 126.9 mm against a front of 86.3 mm: a 40.6 mm
  mismatch that the seam check catches and no amount of care at the defaults would ever
  reveal. The clamp therefore lands on `BACK_NECK_Y` itself, and every use reads that
  one value:

  ```python
  _dy = SHOULDER_SLOPE + _BACK_NECK_Y_OFF
  if _dy >= _SHOULDER_LEN * 0.94:
      _dy = _SHOULDER_LEN * 0.94
  BACK_NECK_Y = _dy - SHOULDER_SLOPE          # the DRAWN rise is the SOLVED rise
  ```

  At that combination `back_neck_clamped: true` and the rise is reported as 39.1 mm
  against the 76.5 mm requested.

The cartridge was probed at the **minimum and maximum of all 14 parameters**, plus
all-min, all-max, cross extremes, and every `target_piece` at both defaults and all-max
— 69 cases, all `errors=0`, every declared seam ok, no degenerate bbox. The back-neck
bug surfaced at case 24 of that sweep and nowhere else.

## Hardware bridge

`notion.hardware_ref` → **`yantra4d/button-hook-aid`**.

`hook_loop` and `hook_wire` are the shared dimensions: they drive the aid's `loop_dia`
and `loop_t`, and they are exactly what the buttonhole length and the pull tab are
drafted from. `loop_depth` follows the button, and the handle (`grip_len`, `grip_w`,
`grip_t`, `finger_scallops`) derives from the loop, so there is one set of numbers.

The aid's `cdg_interfaces` are a `custom` (the button capture) and a `profile` (the hand
grip) — no `flange` — which is correct: **the aid is never sewn to the garment.** It is
a hand tool the cuff is drafted to accept. The dimensional-handshake lane therefore has
no sewn edge to couple and reports nothing to check, which is the honest result here
rather than a gap.

## Construction notes

- **Fabric.** `popelina-algodon` — poplin presses a crisp cuff, and a crisp cuff is what
  stays open under a hook. A soft fabric here undoes the underlap stiffening.
- **Interface the underlap twice.** Full-cuff fusible, plus a second layer over the
  solved underlap. That stiffening is load-bearing in the dressing sense, not the
  structural one.
- **The placket slit is longer than a dress shirt's** (`cuff_depth × 1.6`), on the
  little-finger side, so the cuff opens far enough to lie flat while it is worked.
- **`closed-line` is the maker's check.** It marks where the overlap end lands when
  buttoned; check the cuff against it before closing the sleeve, and the two-position
  geometry is confirmed while it is still fixable.
- **Both cuffs are drafted the same.** The problem is one-sided, but the wearer's
  circumstance may change sides, and a shirt with one odd cuff announces itself.
- **The buttons are real buttons.** Nothing about this shirt says "adaptive" from across
  a room, which is the part of the design most worth keeping.

## Provenance

Original draft for Fashion Cabinet. Button hooks are old — Victorian glove and boot
hooks are the same tool — and extended cuff underlaps are ordinary shirtmaking. Neither
is novel. The contribution is drafting the cuff *for* the tool instead of leaving the
two to meet at the fitting: sizing the buttonhole to the aid's wire rather than to the
button, giving the hook a tab to catch that is not the hole it occupies, stiffening the
underlap so the cuff holds its own working position, and solving the open circuit
against the wearer's measured hand so the accommodation is a number on the pattern
rather than an apology.
