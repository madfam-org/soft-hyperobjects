# Overcoat / Abrigo — FC-100 #63

**EN.** A classic single-breasted tailored **overcoat** in the Chesterfield
idiom: a long, roomy coat cut to layer over a suit. It is the
[blazer](../../blazer/) (rank #30) grown to full coat length and given two
coat upgrades — a **peak lapel** and a **two-piece sleeve** — drafted in wool
**melton** with a coat's wider seam allowances and generous hem.

**ES.** Un **abrigo** clásico de sastrería de un solo pecho al estilo
Chesterfield: largo y holgado para usarse sobre un traje. Es el saco (blazer,
rango #30) crecido a largo completo de abrigo, con dos mejoras propias del
abrigo — **solapa de pico** y **manga de dos piezas** — trazado en **melton**
de lana con márgenes más anchos y bajo amplio.

Official visualizer and configurator: **Fashion Cabinet** ·
Visualizador y configurador oficial: **Fashion Cabinet**.

## Pieces / Piezas

| id | EN | ES | cut |
|----|----|----|-----|
| `front` | Front | Delantero | 2 mirror |
| `back` | Back | Espalda | 2 mirror (CB seam + deep vent) |
| `sleeve_upper` | Upper Sleeve | Manga Superior | 2 mirror |
| `sleeve_under` | Under Sleeve | Manga Inferior | 2 mirror |
| `collar` | Upper Collar | Cuello Superior | 1 on fold at CB |
| `facing` | Front Facing | Vista Delantera | 2 mirror |

Fully lined: the **lining pieces are derived from the shell** (front lining =
front minus the facing; back lining = back with a centre-back ease pleat; two
sleeve linings from the upper + under sleeves). Their yardage is in the BOM;
they are not separately drafted in v0 — see *Honest simplifications*.

## How it is drafted / Cómo se traza

- **Peak lapel + roll line.** The front centre edge runs up the button stand to
  the **roll point**, then breaks into the **lapel** — a straight diagonal out
  and *up* to the peak point (past the gorge line) — then a short two-segment
  **gorge** back in to the neck point (the peak notch). The roll line is an
  internal marking from the roll point to the neck point. This mirrors the
  blazer's notch front and pushes the lapel point above the gorge to make the
  peak.
- **Two-piece sleeve (the coat sleeve).** The sleeve tube is split into an
  **upper** and an **under** sleeve sharing two vertical seams — the **forearm**
  (front) and **hindarm** (back) — and two cap junction points: the hindarm top
  `H` and the forearm top `F`. Each cap arc runs `H↔F`: `sleeve_upper.cap` goes
  the long way over the crown apex; `sleeve_under.cap` goes the short way, a
  shallow bow across the underarm. Together they trace the whole armscye, so the
  armhole seam **sums both cap arcs**. The crown breadth is **bisection-solved**
  so `upper.cap + under.cap = front armhole + back armhole + cap ease` (28 mm by
  default). The forearm and hindarm seams are built from *identical* calls on
  both pieces, so each vertical seam's length delta is **0** by construction.
- **Upper collar** — a collar-band solve: its neck edge is bisection-solved to
  the measured **front gorge + back neck** per half, cut on the fold at CB.
- **Front facing** — a straight strip whose length equals the measured
  **centre + lapel + gorge** run plus end allowances (declared as the seam
  ease), verified against the front edge.
- **Shaped CB seam + deep vent** on the back, with a **half-belt** marking at
  the waist; **welt** breast pocket and **flap** hip pockets as markings.
- **Melton allowances.** Seam allowance defaults to **13 mm** and the hem to
  **50 mm** because the 420 gsm fulled coating (`lana-melton-abrigo`) eats seam
  room; press with heavy steam and a clapper, and trim the undercollar layer to
  shed bulk.

## Construction order / Orden de confección

1. Interface fronts, lapels, undercollar and hems (fusible, teaching-grade).
2. Darts/shaping — none on the front block here; the fit lives in the CB seam
   and side seams.
3. Sew the **CB seam** (15 mm), press open, form the **vent**; sew side seams
   and shoulders.
4. **Sleeves:** join `sleeve_upper` to `sleeve_under` along the **forearm** and
   **hindarm** seams; set the combined cap into the armhole, easing the 28 mm
   with sleeve heads so the cap rolls.
5. Build and attach the **upper collar** to the gorge + back neck (collar-band).
6. Attach the **front facing** to the centre + lapel + gorge; understitch/turn.
7. Set the **lining** (derived pieces), bag the hem, finish buttonholes, sew on
   the coat buttons (a **Yantra4D** shank-button reference — the hardware is a
   Yantra4D cartridge, never re-implemented here).

## Honest simplifications (teaching-grade) / Simplificaciones honestas

- **No pad-stitched canvas.** A fusible stands in for a full haircloth chest
  canvas; a pad-stitched canvas front is future work.
- **Lining not separately drafted.** The lining pieces are *derived* from the
  shell and costed in the BOM, not drawn as their own pattern pieces in v0.
- **Straight facing.** The facing is a straight strip verified against the front
  edge length; a shaped facing that mirrors the peak is future work.
- **Pockets are markings.** The welt breast and flap hip pockets are drawn as
  placement markings; jetting/bagging is future work.
- **Notch gap.** The classic collar/lapel notch gap is a construction detail,
  not drawn into the flat pattern.

## Fabric / Tela

`lana-melton-abrigo` — wool melton coating, 420 gsm, 1500 mm wide. Cuts true but
bulky; dry-clean, steam-press, brush after wear. Its lighter sibling
`lana-peinada-traje` tailors the suit worn underneath.
