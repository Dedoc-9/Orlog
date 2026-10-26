# The speed reconciler and the graphics view tier: the owner's words and the questions (2026-10-26)

On 2026-10-26, during the walk-through of the RUN-1 sheet (`research/run-1/RULINGS.md`, read as an observation stage
while another session ran an adversarial pass over the reporting layer), the owner wrote the two requests below. The
first came after a pasted review of R1 and R2, which is not about speed and is not reproduced here. The judge mapped
the requests onto RUN-1 in that session and proposed this debate as a separate session; the owner asked for it to be
done in the same session instead. The debate's reports and the judge's verdict sit beside this file. Nothing in it is
built or admitted.

---

## The owner's words (verbatim)

> Also we will need something like a speed reconciler or language swap for competitive latency and graphics ie compatible with shaders and spherical harmonics or other high requiring methods

> reference verdani speed records for competitive headroom standards

> Do this task here: “Research: speed reconciler and graphics view tier”

---

## The questions the debate answers (the judge's)

1. **The two-speed design.** Play runs on one resident fast execution (compiled C or Rust) that records the input
   log; the reference and the other backends replay that log behind it, for admission (the skeptic's "two speeds",
   `research/roadmap-debate/SKEPTIC.md`). What must RUN-1's formats commit per tick (RULINGS.md R5: the output chain,
   the trace head at each `'T'` event; D4) for a reconciler to name the first tick where two executions part? Is
   anything missing from the sheet?
2. **A language swap.** Does the law need a faster language at all? Could a GPU backend ever be authoritative, for
   instance integer or fixed-point only?
3. **The view tier.** Shaders and spherical harmonics run in floating point, outside receipts. How does a view read
   each tick's output and never write back? What, if anything graphical, must be computed in the law, in Fix?
4. **A competitive headroom standard, written Verðandi's way.** From Verðandi's speed records, a preregistered
   measurement rather than a number: its sample size, a declared margin, a same-run comparator, the clock's step and a
   named host.

---

## Fixed before the debate

- **No competitive claim.** Verðandi makes "no low-latency, competitive or input-to-photon claim" (its
  `docs/GHOSTS.md`, G7), and its brief forbids claiming a latency, a frame rate, input-to-photon or feel without
  measurement. Neither may this debate.
- **Verðandi is read, never written.** Its records are cited by document and section.
- **Floats stay out of ports for now.** The sheet recommends deferring float ports (R8 b) until a second host has
  measured floats; nothing on the sheet is ruled yet.
- **The view rule of the lineage.** In Verðandi the renderer and the art may decorate and must not decide where walls,
  cover or anything that blocks exist (`docs/BOUNDARIES.md`); its native renderer's picture is judged by a person and
  hashed by nothing.
- **Nothing here is built.** RUN-1 (ports, the tick block, the input log) is a ruling sheet, not code.

## The records it starts from

Numbers from different apparatus are compared in orders of magnitude only (Verðandi's G4), and every number is one
host and one corpus (G5).

| record | value | grade, source |
|---|---|---|
| the refresh period of the host Verðandi measured on | 13.1–13.9 ms, five runs, the median of eight idle `DwmFlush` intervals each | MEASURED, Verðandi `docs/GHOSTS.md` G10 |
| Verðandi's software frame, render start to frame ready | 14.8–15.7 ms at p50; no single phase dominant, the blit largest at 427–434‰ | MEASURED twice, G8 (`LATENCY-1R`, `FRAME-SPLIT-0`) |
| render start to composited output | 21.4–25.6 ms at p50, by the phase at which the render starts | MEASURED twice, G7 (`LATENCY-1R`) |
| Verðandi's threaded texel pass | p99 stops improving past about eight threads (T8 2,360 / 2,355 µs) | the plateau MEASURED by `GAUNTLET-2`; its cause SPECULATIVE (G2) |
| the same court on another run the same day | 40–60% slower; the cause unmeasured | MEASURED (the drift), UNDERDETERMINED (the cause), G13 |
| one tick of fall.orl | 28 µs in the reference, 1.3 µs in C | MEASURED once, `research/roadmap-debate/SKEPTIC.md` |
| starting a process | 12.5 ms native, 107 ms Python, about 300 ms for `orl.py` before any work | MEASURED once, the same |
| a round trip to a resident process | 0.053 ms by pipe, 0.214 ms by localhost TCP (p50) | MEASURED once, the same |
| a text change | a rebuild: c99 0.33–0.53 s, Rust 0.83–1.3 s per corpus program | MEASURED once, the same |
