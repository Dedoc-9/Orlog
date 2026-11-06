# The vertical jump: a game-simulation update, checked two ways (2026-11-06)

`examples/jump.orl` states one rule of a real game's simulation in Ørlǫg: the vertical jump of Verðandi's
first-person graybox (rules 1, step 6, on flat ground at height 0). It is run by the reference and by the Python, C99
and Rust backends. Its result is checked against two things that do not depend on each other:

- **another implementation**: Verðandi's own tick (`graybox/tick_ref.py`, Verdandi commit
  `b441a1e5ccc33351ed0307a7062bd65423b3db90`), compared bit for bit on every tick;
- **a prediction** in exact rational arithmetic (`PREDICTION.txt`), written down before either program was run.

## The rule

On tick 1 the jump sets `vy = 7`. Every tick then does `vy ← vy − gravity·TICK`, then `feet ← feet + vy·TICK`
(symplectic Euler), with `gravity = 20` and `TICK = 1/120`; when `feet` is at most the ground, `feet = 0` and `vy = 0`.
The program does these operations in the same order as `tick_ref.py`'s `fall` and `land`, and `TICK` is `1.0 / 120.0`
in both. It is unit-free: the numbers are the game's constants, not metres and seconds.

## The prediction (`PREDICTION.txt`, sha256 `09aaa9a911a60055411681c7dc75a378e668ebad466b9bbc3d3f70078b1d3227`)

With g·Δt = 1/6, in exact arithmetic: v_n = 7 − n/6 and feet_n = 7n/120 − n(n+1)/1440. So:

- the discrete maximum is feet_41 = feet_42 = **287/240**, an exact tie (v_42 = 0);
- the continuous apex v₀²/(2g) is **49/40**;
- their difference is **7/240** = v₀·Δt/2, the symplectic-Euler offset when v₀/(gΔt) is a whole number (here 42);
- in binary64 the maximum lies within a few ulps of 287/240, at tick 41 or 42.

## The result (`evidence/jump-tick-ref.txt`)

| | predicted | measured |
|---|---|---|
| bit-level, Ørlǫg against `tick_ref.py` | — | 100 ticks, **0** with any differing bit in `feet` or `vy` |
| Ørlǫg's backends | — | reference COMPLETED; c99, python and rust agree, no dissent |
| the clean-room twin | — | output byte-identical to the reference's |
| discrete maximum | 287/240 | 1.1958333333333322 (bits `3ff322222222221d`), 5.13 ulp below 287/240 |
| at ticks | 41 and 42 | 41 and 42: the tie held in binary64 |
| continuous apex − measured | 7/240 | 0.029166666667 |

Run it again from the repository's root (`PYTHONHASHSEED=0`):

```
python -B research/jump/compare.py --verdandi PATH-TO-A-VERDANDI-TREE
python -B research/jump/compare.py --verdandi PATH-TO-A-VERDANDI-TREE --plant explicit-euler
python -B research/jump/compare.py --verdandi PATH-TO-A-VERDANDI-TREE --plant gravity-ulp
python -B orl.py run examples/jump.orl --backends python,c99,rust
```

`JUMP HELD` (exit 0) clean, and `JUMP NOT HELD` (exit 1) under each plant. A plant changes the program's bytes in
memory, never the file. Without `--verdandi`, `compare.py` checks the prediction alone and says the bit-level
comparison was not run. Nothing in the program reads this folder, and no gate runs it.

## Graded

- **MEASURED:** bit-level agreement of Ørlǫg's reference with `tick_ref.py` on all 100 ticks; agreement of the three
  backends; the twin's output equal to the reference's; the maximum at the predicted ticks, 5.13 ulp from 287/240.
- **MEASURED, plants:** two defects planted in copies of the program are each caught (`JUMP NOT HELD`, exit 1):
  the update order swapped to explicit Euler (84 ticks differ; the prediction fails), and `gravity` one ulp high
  (47 ticks differ). The second is caught by the bit-level comparison only: the prediction check alone passes it.
  The twin's comparison has no plant of its own; the twin is given the door's canonical text, since it has no door.
- **DECLARED:** that the prediction was written first. It was recorded at 14:24:15 and the first run was at 14:25:27,
  by file times on the author's machine. This repository cannot prove the order.
- **Disclosed:** `compare.py`'s bound of 8 ulp was chosen after the run measured 5.13. The prediction itself said
  "a few ulps".

## What it does not show

- **Physical validity.** `gravity = 20` and `jump = 7` are the game's constants. The check is of the rule's
  arithmetic and its discrete behaviour.
- **Independence of the implementations from one another.** Ørlǫg, its twin, `tick_ref.py` and the prediction were
  written by agents of one model family. Their agreement is corroboration, not proof. The prediction is independent
  of the implementations, not of their author.
- **Anything beyond one axis on flat ground:** walking, steps, ceilings, movers, collisions and turning are not
  exercised. Turning needs trigonometry, which Ørlǫg does not have.
- **Fix mode.** The program declares `Decimals are floats.` In Q31.32 it would not match `tick_ref.py`'s binary64.
- **More than one machine.** It ran on one Windows host.
- **Units.** The program is unit-free by design.
