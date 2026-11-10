# research/stepwalk — the graybox's walk onto and off a ledge, in Ørlǫg

`examples/stepwalk.orl` states the Verðandi graybox's **rules-1 ground-and-step rule** as an Ørlǫg program and
checks it two ways: against an exact prediction written first, and against Verðandi's own tick (`graybox/tick_ref.py`)
driven through the same scenario, bit for bit. It is the next rung after `research/jump` (the vertical jump): the jump
exercised step 6's vertical integration and landing on flat ground; this adds **horizontal motion, the moving ground
lookup, and both branches of the step clause** — mounting a low ledge and following the ground down off it — while
staying free of trigonometry.

```
python -B research/stepwalk/compare.py                       # the prediction and the clean-room twin
python -B research/stepwalk/compare.py --verdandi DIR        # and the bit-level comparison with tick_ref.py
python -B research/stepwalk/compare.py --verdandi DIR --plant NAME   # a planted defect, which must end NOT HELD, exit 1
```

Run from the repository root with `PYTHONHASHSEED=0` (`PYTHONUTF8=1` if stdout is redirected). It writes nothing.
The harness resolves the compiler and the twin relative to the repository root, loads the requested `tick_ref.py`
**explicitly** from the given tree (no `sys.modules` reuse), reports its provenance (the Orlog repository git HEAD and
the loaded `tick_ref.py`'s path, sha256 and git HEAD), and fails loudly on a row-count mismatch before comparing rows.
The recorded run is `evidence/stepwalk-tick-ref.txt`, against Verðandi
`95a9731b3ce8cf6a516b116fd6d7ec1d9e0bacf5` (rules-1 `walk`/`fall`/`land`, `tick_ref.py` lines 390–415).

## The scenario

A body on a cell-center line (x = 0.5, a 1 m grid) at **yaw 0**, forward held, for 125 ticks. The world's z-cell tops
are `[0, 0, 0.5, 0.5, 0, 0, 0, 0]`; the body starts at z = 7.52, feet 0, on the ground, and walks in −z across the
0.5 m ledge. At yaw 0 the forward step is trig-free in value — `sin 0 = 0`, `cos 0 = 1`, `hypot(0, 1) = 1`, each exact
in the graybox's fdlibm — so the walk is a pure `z ← z − 6·TICK` each tick, and no 0.5 ledge is ever a wall
(`is_blocked` stays false, `move` never halves).

**The ground reduction, and its scope.** On this line `world.ground` reduces exactly to a one-interval test:
`ground = 0.5 ⟺ 1.65 < z < 4.35`, else 0.0. This reduction holds **only for this fixture** — the single cell-center
line x = 0.5, radius 0.35, 1 m grid and two-cell 0.5 ledge; it is **not** a general implementation of `world.ground`,
which is a max over every cell a radius-0.35 circle overlaps. The bit-for-bit agreement with `tick_ref.py`'s own
circle-rectangle geometry is what certifies the reduction for this fixture.

The step clause is `feet ← ground when feet ≤ ground OR (was-grounded AND vy ≤ 0 AND feet − ground ≤ step)`.
`was-grounded` is the body's grounded state **from the end of the previous tick**, captured (§13.1) before the walk
and the fall — not a value recomputed after moving (the walk never changes it). That previous-tick state is what makes
the step allowance a *was-on-the-ground* rule rather than an after-the-fact one. The walk fires both branches: the
**mount** at tick 64 through `feet ≤ ground` (the body dips below the newly raised ground and snaps up onto the ledge),
and the **step-down follow** at tick 118 through the step allowance (`feet − ground = 0.5 ≤ step = 0.55`, so the body
follows the ground down without leaving it). `grounded` holds true at every tick — the point of the step allowance is
that a rise or drop of at most the step height never puts the body in flight.

## The plants

The plants change the program's bytes in memory before it is compiled (the file is not touched). Each must end
`STEPWALK NOT HELD`, exit 1:

- **step-shrunk** — `step` 0.55 → 0.45. The step-down follow (branch B) fails, `grounded` goes false, and the
  program's own guard `It must hold that grounded` refuses (`MUST-FAILED`); the clean-room twin refuses identically.
- **ledge-interval** — the ground's upper edge 4.35 → 4.30. The mount lands one tick late (65, not 64), one bit
  different from `tick_ref.py` at tick 64.

Two plants that bite the jump are **equivalent mutants here** and are not used: because the body is grounded every
tick (vy is reset to 0 and feet to the ground exactly before they are said), a plant in the gravity constant, or one
swapping the vy and feet updates (explicit vs semi-implicit Euler), changes nothing observable on this walk. They are
declared equivalent rather than passed off as caught.

**Plant coverage limitation.** No plant isolates the mount's `feet ≤ ground` branch (branch A). On this grounded
fixture the mount is **double-covered**: when feet dips below the newly raised ledge, the step allowance (branch B,
`feet − ground ≤ step`) also accepts it, so disabling branch A alone does not change the output. Branch A's distinct
role — an airborne landing, where `was` is false and only `feet ≤ ground` fires — is not exercised on this grounded
walk; the vertical jump (`research/jump`) exercises it. The two plants here therefore cover the step bound (branch B,
`step-shrunk`) and the ground interval (`ledge-interval`), not branch A's independent necessity.

## What this shows, and what it does not

Graded **MEASURED**. Two comparisons, reported apart:

- **Against the prediction** (a mathematical comparison): the prediction is exact arithmetic, independent of both
  implementations but **not of their author**. It fixes the mount and step-down ticks, the feet trajectory, and
  vy = 0 every tick.
- **Against `tick_ref.py`** (an implementation comparison, **not physical validation**): bit-for-bit agreement in z,
  feet and vy across all 125 ticks shows the Ørlǫg program and Verðandi's reference compute the same rule the same way;
  it does not show either is physically right.

**Does not show.** Only the rules-1 ground-and-step rule on one cell-center line at yaw 0, with a mountable ledge.
It does **not** exercise: a ledge taller than the step (a wall, where `is_blocked` halves the move and the body does
not climb); walking off a drop greater than the step (leaving the ground into flight); the halving slide itself;
targets, movers, or box tops (rules 2 and 3); and any turn or diagonal walk. **Turning and diagonal motion need
trigonometry, which Ørlǫg does not have** — the same boundary `research/jump` records. A trig-free axis-aligned walk is
as far as the movement bridge reaches today; carrying it to turning, strafing or flight (the graybox's rules-4 flight
law) waits on trigonometry in the language. **Falsifier:** any tick whose z, feet or vy differs from `tick_ref.py`'s in
one bit, or a mount or step-down at a tick other than the predicted 64 or 118.
