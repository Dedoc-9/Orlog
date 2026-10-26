# Debate record: the proponent's answer to the prosecution, round 2 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the proponent read ADVERSARY.md, RESEARCH.md and the judge's measurements and
reran the adversary's experiments; its runs are in `work/speed-probe/` (ignored by git); its MEASURED lines are
this host's.

---

# The speed reconciler and the view tier: the proponent, round 2 (2026-10-26)

A subagent's report for the judge of the debate set out in `research/speed/PROPOSAL.md`. It answers the adversary's
round 1 (`work/speed/ADVERSARY.md`, 22 findings) finding by finding, gives revised answers to the four questions, and
proposes changes to the RUN-1 sheet (`research/run-1/RULINGS.md`) for the owner's ruling. It is model output, not the
owner's words, and it decides nothing. No tracked file was changed; nothing is built into the language.

**Where it ran.** On this host, against my snapshot of `f16dc26` (tree `8be71851`) in `work/speed-probe/tree`, checked
again before this round: all 719 files hash to the commit's blobs, 0 differ, no other file present. Never against the
working copy (another session has changed `src/` since). Python 3.14.5, clang 22.1.8, rustc 1.96.1; `PYTHONHASHSEED=0`,
`PYTHONUTF8=1`, `python -B`. Clock: `time.perf_counter_ns` (QueryPerformanceCounter), declared resolution 0.1 µs,
smallest positive step observed 100 ns; in-program stamps read QueryPerformanceCounter directly (step 0.1 µs). Host
state beside every timing run (`common.host_state`, recorded, read by no rule): memory load 93–98% throughout, CPU busy
41–301‰ over one second around the runs, other sessions active. Every timing is a software timing of this host, one
sitting, one corpus. No latency, frame rate, input-to-photon figure or feel is claimed or implied.

**Files.** The adversary's scripts were copied, never edited, into `work/speed-probe/adv-rerun/` (their sha256 in
`COPIED-FROM-SPEED-ADV.sha256`, checked equal to the originals); only `_common.py` there is mine, pointing them at my
snapshot and my folders. Nothing was written in `work/speed-adv/`, nor in `../Verdandi`, which was read only (its
renderer `art/web/scene_render.js` hashes to the adversary's copy, sha256 `0b5cae9d…`). Round 2's own probes are in
`work/speed-probe/r2/` (P12–P17), each writing its `.txt` and `.json` there.

**Grades.** MEASURED (a run here: command, samples, median, spread, clock), ESTABLISHED (read from code or a cited
record), DECLARED (a design or an argument), DERIVED (arithmetic on measured inputs), OBSERVED, SPECULATIVE,
NOT_MEASURED. Survey items keep the survey's source grades ([P], [A], [S], [U], `work/speed/RESEARCH.md`).

---

## 0. The settlements, short

1. **What a per-tick line must commit.** The tick, the event count, the operation count, the output bytes and the
   output chain, a digest of the claim accumulators, a digest of the persistent state, and the trace head where the
   execution keeps one; and the reconciler recomputes the output chain itself over the bytes it received. MEASURED
   (P12): 13 planted defects of 12 kinds (both parties' and five new) and 3 controls. The line, read by the
   reconciler's rule, names all 13 at the tick they were planted in and no control; R5's pair (head and output chain)
   names 4, the head alone 3. Without the head it names 12: the one it misses is a divergence that heals inside its
   tick, which only the trace sees and admission names. **Cost** (P13, the adversary's own law, every tick stamped): at
   K = 1,000 landed, play with no event chain and the full line runs a tick in 62.6 µs at p50 (4.3% of the 1,440 µs
   the arbiter's build takes); with the chain and the line 1,512 µs (105%); with round 1's stream head and the line
   440 µs (31%). The reference pays 11% more for the line (16.5 against 14.9 ms).
2. **R9 b is unsafe as written for a live outcome and safe for admission.** MEASURED (P12): with the adversary's
   shared-lowering defect and the budget, the compiled program refuses TICK-BUDGET in tick 246; R5's per-tick commitments
   name tick 246, and the line names tick 1. Three conditions make it safe: the operation count in every tick's
   commitment (and in R5's `'T'` payload), the reference as the live watcher (never a compiled-only comparison, A2),
   and no live refusal declared before the watcher has refused at the same tick with the same record. P14 measured
   that the reference can keep pace at the adversary's size with four lanes of segments (197 ticks a second of
   software time against 120 needed). A16 stands: a budget in operations bounds no time; across eight laws P15 and
   P15b measured time per SHA-256 compression within 1.13× while time per operation spread 5.3×10^5, so the owner may
   prefer to count committed blocks.
3. **A live outcome is testimony until the watcher confirms it**, and it is never "verified" or "final". Concession of
   A4: once a dissent names tick t*, every outcome from t* on is void, and the reference's record from t* on is not the
   match either, because every later input answered a picture the law did not produce. Outcomes before t* stand as
   confirmed. Admission adds integrity, never grounding (A21): "replayed four ways over log ⟨seal⟩, unratified".
4. **The floor-mirror leak reproduced, cell for cell** (my rerun of the adversary's pages, the same engine and GPU).
   Verðandi's rule, as the owner wrote it, governs where walls, cover and blocking objects exist, and the leak decides
   none of them, so the rule holds. "Decorates, never decides", read as "cannot affect play", overclaims: the renderer
   decided what a player can learn of hidden state. A view rule needs two clauses, no write-back (witnessed by the
   state field) and no disclosure, and the second holds by construction only if a view is never given what its player
   may not know (per-player output). A renderer that is given more can be convicted by a pixel court on one platform
   and never acquitted on all.
5. **HEADROOM-0 after G10 and G13** needs, besides round 1's draft: a rule per regime with 1,000 samples in each (a
   regime with fewer is TOO FEW TO RULE, never averaged), counts beyond the bound beside every percentile, a
   calibration cell for within-run ratios, a confirmation set of three runs over two sittings, and a drift panel that is
   recorded and never voids a slow run. The r2 draft (sha256 `a77a6424…`) was hashed before its pilot; the pilot shows
   the rule can return PASS, FAIL and the TOO-FEW mark on this host, and its confirmation set (three runs, two
   sittings) reads HELD for the no-chain play cell and NOT HELD for the chain at 1/120 s: a pilot's labels on a
   stand-in, not a reading. Accepted from the adversary after the pilot, and so not credited as preregistered: a margin
   wider than the drift the host has shown.

---

## 1. The adversary's decisive experiments, rerun

Each from my byte-identical copy, against my snapshot (`work/speed-probe/adv-rerun/`, `python -B <script>`;
`run_timed.py` ran the timing ones one at a time with the host state beside each, `run_timed.log`).

| finding | script | rerun here | against the adversary's output |
|---|---|---|---|
| A1, A2, A3 | `chain_blind.py` | REFERENCE-DISSENT, python, c99 and rust agreeing at 2,406 operations against 1,806; per-tick heads name tick 246, `(head, ops)` names tick 1 | identical below the header line |
| A9 | `refusal_ends_match.py` | OVERFLOW at tick 5,932; CLAIM-REFUTED at tick 1; dissent NONE in each | identical |
| A12 | `sh_fix.py` | every row | identical |
| A15 | `gpu_mul.py`, `order_refusal.py`, `sh_order.py` | every row | identical |
| A11 | `view_geometry.py` | every row | identical |
| A10 | `webleak/index.html`, `ablate.html`, `ablate2.html`, from my copy served on 127.0.0.1 in the built-in browser pane | every cell: counts, largest differences, rows | the three result files byte-identical (same browser engine, same GPU, this host) |
| A7 | `hash_share.py` (9 runs a bound) | the chain 95% of the K = 1,000 falling tick (822.2 µs as built), 96% landed (1,529.0 µs), 95% at K = 100 landed; K = 100 falling read −9.7 µs without the compression | shares equal to ±3 points; the K = 100 falling window is noise in both, as the adversary said |
| A8 | `ref_lag.py` (3 runs) | K = 1,000 landed median 15.78–15.98 ms, 99 of 99 ticks over 1/120 s in each run; K = 100 1.55–1.56 ms, none over | 8% slower here than its 14.65–14.76 ms |
| A6 | `trace_cost.py` | C 0.882 → 2.519 ms a tick with the trace (2.86×); 3,001 lines and 338,772 bytes a tick; 161 bytes a line held | its 3.03×; the rest equal |
| A16 | `one_op.py`, `ops_not_time.py` | 371 ms a tick for 2 counted operations (2^24 items); one operation 1.02×10^5 times another in C, 4.06×10^3 in the reference | its 352 ms, 1.04×10^5, 4.34×10^3 |
| A17, A18 | `tick_tail.py` (3 runs) | the step at tick 91 in every run; K = 1,000, ticks 1–2,999 (landed from 91): p50 1.435–1.437 ms, p99 2.13–2.24, max 3.67–4.61; K = 100, ticks 1–29,999: p50 0.151–0.153, max 2.52–3.31 | p50 equal; p99 wider than its 1.61–1.96 |
| A18 | `drift.py 8 45` | K = 1,000: 1.475–1.747 ms a tick (max/min 1.18); ratio to K = 100: 9.89–11.13 (1.13) | its 1.03 and 1.05: this sitting drifted more |
| §3.4 | `view_cost.py` | each body said: 1.25× quiet; one list line: 1.07× | its 1.29× and 1.11× |
| A8, A17 | `ref_slopes.py` | K = 1,000: 13.1–15.3 ms a tick by window (1.17); K = 100: 1.26–1.58 (1.25) | same shape |

What this shows: every deterministic finding reproduces exactly, and every timing finding reproduces within this
session's drift, which was larger than the adversary's in two scripts (drift, tick_tail's p99). That difference is
itself A18's point. Grade: MEASURED (the reruns); does not show any other host, engine or GPU.

---

## 2. The findings, one by one

Witnesses side by side, in the adversary's order. For each: concede, repair, or rebut, and what my design becomes.

**A1. Per-tick heads are blind to the operation counter and the claims' cost — CONCEDED, REPAIRED.** It is round 1's
P4 seen from the other side, and the rerun reproduces it. Repair: the tick line commits `ops` and a claims digest, and
R5's `'T'` payload carries `ops` (the adversary's own candidate). MEASURED (P12): with the adversary's shared-lowering
plant on its projectiles law and on fall, the line names tick 1, and so does `(head, out chain, ops)`; the claim's cost
(900 against 1,200 in the adversary's run) is named at tick 1 by the claims field.

**A2. A reconciler made of the compiled backends cannot see a shared lowering defect — CONCEDED.** Round 1's watch
tier was already the reference, but I state the rule plainly now: a comparison that leaves out the reference is a
consistency check, never a reconciliation, and it never confirms a live outcome. The doctrine already records this
very plant and its catch (DOCTRINE T11, the lowering's row: the three agree against the reference, which "walks the
tree and never lowers"; and "The catch relocates trust to the reference rather than distributing it"; ESTABLISHED).
The same table's first row bounds my answer: a defect in the front end, which all four executions share, is seen by
none of them, the reference included, and only by the twin. Knight and Leveson's rejection of independence among
versions written from one specification is the survey's background too ([A]/[S], RESEARCH §8).

**A3. Under R9 b a shared counting defect moves when a live match ends — CONCEDED for R9 b as written; REPAIRED.** §3.2.

**A4. A live outcome is one execution's; after a dissent the record that stands is a game nobody saw — CONCEDED.**
I take the adversary's first horn: the reference is the authority, and a live outcome is provisional until the watcher
confirms it. §3.3 says what that means tick by tick. The adversary's falsifier, a design in which a live outcome and a
later REFERENCE-DISSENT over the same log both stand, is not met by mine: a dissent at t* voids every outcome from t*.

**A5. The log is the fast path host's; which tick an input lands in is a clock no runtime reads — CONCEDED (DECLARED).**
Replay proves the computation over the log, not the log's fidelity to what players did (DOCTRINE T12, limit 4). What
the design can add: the door is the log's only writer, write-ahead (round 1), and the dissent record names the log's
seal. Fairness of tick assignment is a property of the door's protocol, as it is in the lockstep games the survey read,
where commands are scheduled for a later turn by rule (Age of Empires, OpenTTD: [P], RESEARCH §1); it belongs to
SESSION-0 and to distribution, which RUN-1 leaves undecided. Never "the match was fair"; only "replayed four ways".

**A6. Locating a divergence the arbiter's way does not scale to a session — AGREED.** My design never reads whole
traces in play: lines for detection, a windowed re-run from the nearest snapshot for localization (round 1, P4: 30 ms
against 1,219 ms at 40,000 ticks, one run each). The survey's systems split the two layers the same way ([P], RESEARCH
§1).

**A7. "Keep the chain and be slow, or drop it and commit nothing" — REBUTTED by measurement: a third option.** Play
drops the event chain and commits the line. MEASURED (P13): the K = 1,000 landed tick falls from 1,440 µs as built to
62.6 µs with the full line, state digest included (p99 75–128 µs over three runs, 299 ticks each); with the chain's
hashing removed and no line (the arithmetic and the events' bookkeeping) it is 22.3 µs, so the chain's hashing is
98.5% of the as-built tick here, an ablation that removes the calls rather than XOR-ing the compression (the
adversary's 96%). MEASURED (P12): without any event commitment the line still names value, ops, out, claim cost,
silent scalar and list writes, refusals and the shared-lowering defect at their tick, and, with the receiver's own
output chain, a byte the runtime never counted; "a divergence in state that never reaches the output" is named by the
state digest at its tick. What it gives up: a divergence that heals inside its tick (P12's transient) is invisible to
play and named at admission, where the four executions keep the chain. The adversary's §2.3 item 4 asked for exactly
this statement; that is it. The same numbers answer its §1 note on rollback ("a predicting path can roll back 8 ticks
within the period only without the chain, and then it commits nothing"): 8 landed ticks at 62.6 µs are about 0.5 ms
with the line committed at every one (DERIVED from P13; the restore itself is SNAP-1's and NOT_MEASURED).

**A8. The reference cannot keep pace at K = 1,000 — CONCEDED for the sequential reference; REBUTTED for the watcher
in segments.** Rerun: 15.8–16.0 ms a landed tick, every tick over 1/120 s. MEASURED (P14, the adversary's law, K =
1,000, T = 1,600, 16 segments of 100 ticks, medians of 3 rounds): sequential reference with the full line 60 ticks a
second of software time; 2 lanes 109; 4 lanes 197; 8 lanes 267; 16 lanes 381. At 1/120 s, 120 ticks a second are
needed: 4 lanes keep pace, 2 do not (my round-1 DERIVED claim that two lanes would keep pace was wrong for this law;
corrected in §8). Every segment's lines equalled play's, every boundary reproduced; a value defect at tick 523 was
named at 523; a snapshot forged at tick 800 broke boundary 800 (and 900, computed from it), and the one differing line,
tick 801, came from a segment that boundary had made untrusted, so no divergence of play was reported: the snapshot,
not play, was wrong. *Does not show:* a live pipeline (P14 admits a closed log in batch; live, lane j can start only
when play reaches tick jL, and W lanes keep pace in steady state when W ≥ c_ref/P with perfect scaling, 1.98 here at
16.5 ms a tick, DERIVED; P14's two lanes scaled 1.81×, so the margin matters); play and the lanes running at once on
this host (play's lines were made first; play's own share at 1/120 s would be about 0.75% of one core at 62.6 µs a
tick, DERIVED from P13, and the view's share is NOT_MEASURED); SNAP-1's real restore; any other size.

**A9. A refusal reachable from a port ends the match; nothing refuses a hostile record at the door — AGREED.** Round 1
had a port range as a "should"; I move it to a "must" for any session with more than one player (§5). Rerun
reproduces the stand-ins (OVERFLOW at tick 5,932; CLAIM-REFUTED at tick 1, four executions agreeing). Verðandi's input
contract is the model: a record admitted or refused whole before the tick touches anything (its `docs/BOUNDARIES.md`,
"simulation"; ESTABLISHED).

**A10. The lineage's renderer puts a hidden target on the screen — REPRODUCED; the overclaim CONCEDED.** §3.4.

**A11. The view rule covers blocking, not seeing; the player is the channel — CONCEDED, with one precision.** Round 1's
fence covered write-back only. The precision: Verðandi's fog is an art statement that a model may *propose*; it
reaches the brief only through the director's verdict and an admission the designer makes (Verðandi `AGENTS.md`, the
studio's row: "A provider proposes; nothing it says reaches the world but through the gateway's reading and the
director's verdict"; ESTABLISHED). The substance stands: no check in Verðandi holds what a player can see.

**A12. SH in Q31.32 is exact only at unit scale — CONCEDED as a reading of my round-1 claim; REPAIRED.** The loss is
the normalization's, not Fix's. MEASURED (P17, the adversary's seed, scales and comparison): doubling the vector
exactly until its largest component reaches one half (at most 31 `x_add(a, a)`, each exact), or halving it, before
normalizing, brings the worst error to 1.8–3.8 units of 2^-32 at every scale from 2^-28 m to 2^24 m, with 0 refusals,
where the plain normalization reads 1.19×10^9 units at 2^-15 m, refuses some vectors at 2^-16 m and 2^15.5 m and all
at 2^-17 m and below and at 2^16 m and above (the "without" column reproduces the adversary's table exactly). A
triangle's unit normal: 0 refusals down to 0.1 mm edges, worst 1.21×10^-6 degrees at every size. Written as a law (a
bounded loop of doublings), eight short vectors from 2^-28 to 2^-6 m through the arbiter: dissent NONE, every value
equal to the model's, worst 0.4–1.8 units of 2^-32. *Does not show:* the input's own quantization (a component of a 2^-28 m vector has about four significant bits; the
repair is exact relative to the vector it is given, never to the vector meant), or any law that does not pre-scale:
the precision is a property of the law's text, which a lint could check and nothing checks today (DECLARED).

**A13. Per-pixel visual work in the law costs about 10^3 ticks a frame — AGREED** (round 1 already put only decisions
in the law).

**A14. A language swap attacks the few percent that is not the chain — AGREED** (round 1 §2). P13 sharpens it: the
tick without the chain's hashing is 1.5% of the as-built K = 1,000 tick.

**A15. A GPU can be at most a fifth witness — AGREED** (round 1 §2.3–2.4). The two emulations differ in their counts
(108 32-bit primitives a Fix multiply in round 1's guarded model, 153–159 in the adversary's); both say two orders of
magnitude more steps than one native multiply.

**A16. A budget of counted operations does not bound a tick's time — CONCEDED; an alternative unit MEASURED.** §3.2.

**A17. The skeptic's ceilings came from the cheap regime — CONCEDED.** My round-1 bodies law had no floor and so no
landed regime. Round 2 uses the adversary's law and reports both regimes (P13, P14, P16).

**A18. Slopes hide tails; one session's spread is no margin for another's — CONCEDED.** My rerun of `drift.py` drifted
more than the adversary's (§1). Round 2 stamps every tick (P13) and samples every tick through the pipe (P16).

**A19. A headroom standard as a number is a scalar scorecard — AGREED.** §3.5.

**A20. "Competitive latency" is not a property of a language — AGREED.** Achievable: a tick that fits a declared
period on a named host, measured by a preregistered method, and after-the-fact adjudication by replay.

**A21. Reconciling adds integrity, never grounding — AGREED.** The phrase goes into the sheet (§5).

**A22. A view must be given only what its player may see — AGREED, and raised.** Round 1 placed per-player output at
a later rung (§3.4 there). With A10 measured, it becomes a precondition of any competitive use (§5).

**The adversary's §7 falsifiers, met or not.**

| its "likely proposal" | its falsifier | here |
|---|---|---|
| a tick ledger of heads and out_t | a planted operation-count defect localized to the tick where the counts part, by a fast path that keeps its speed | met: P12 names tick 1; P13's play build runs at 4.3% of the as-built tick |
| the fast path without the chain, the reconciler computing it | a divergence in unprinted state named within its tick | met: P12's silent scalar and list writes named at tick 237 by a build with no chain |
| the other backends as the reconciler | the lowering plant caught without the reference | not met, and not proposed (A2 conceded) |
| a fixed-point or integer GPU backend | byte-identical receipts from a GPU execution, faster per tick than C | not attempted; no GPU authority is proposed |
| "the view decorates and never decides" | the leak page reading 0 on the shipped renderer; a view given only what its player may see | the first not met (reproduced); the second DECLARED, not built |
| visual quantities in the law, in Fix | a per-tick light-probe count with its precision bound at the vectors' real scales | met for bands 0–2: within 3.8 units of 2^-32 from 2^-28 m to 2^24 m (P17), 0.78 µs an evaluation in C (P15b); the reference's 51 µs (round 1) bounds a 1/120 s tick to about 160 evaluations sequentially (DERIVED) |
| a headroom standard | §6.4's eight items, preregistered before any number | seven of the eight in the r2 draft, hashed before its pilot; the eighth (a margin wider than the host's drift) proposed after the pilot, so not credited as preregistered (§3.5) |

**Where the adversary's round 1 and this round now coincide** (as I read its report; it has not seen this one): the
operation count committed per tick (A1, its §2.3 item 1; my round 1's P4); a per-tick ledger instead of whole traces
(its item 2); a written rule for a live outcome (its item 3; mine takes its first horn, §3.3); the reference as the one
reconciler independent of the lowering (A2); no language swap (A14); a GPU at most a fifth witness (A15); per-pixel
graphics out of the law (A13); a door that refuses hostile records (A9); headroom as a preregistered method on one
component (A19, A20). Still in dispute, each with a measurement on my side for the judge to weigh: A7's dilemma (P12,
P13: a third option); A8's "cannot keep pace" (P14: it can, in segments, which need SNAP-1); and what A10 means for
the rule (§3.4: the rule as written holds; its short form, read alone, overclaims).

---

## 3. The five points to settle

### 3.1 What a per-tick line must commit, and at what cost

**The line** (`orlog-ticks 0`, round 1's, with one field changed in meaning): one per tick boundary,

```
<t> <events> <ops> <output-bytes> <trace-head | -> <output-chain> <claims> <state>
```

`trace-head` is `-` in a play build without the chain. `claims` is the SHA-256 of the receipt's claim lines at the
boundary (or `-` when the law declares none). `state` is the SHA-256 of every persistent variable (D6), lists included,
in RUNTIME-SPEC §5's encoding. The reconciler compares lines in order; if every line agrees, it compares the final
records, and a refusal there names the tick after the last line; the output chain it compares is the one it computes
itself over the bytes it received in each tick.

**The plants (MEASURED, P12, `work/speed-probe/r2/p12_plant_matrix.py`, deterministic).** The fast execution is a law's
C program as the snapshot generates it, with the line and one planted defect; the reference writes the same line and is
never planted. A reading names the tick at which its fields first differ (or one side has no line); `*` marks the tick
the defect was planted at. Readings: H the head alone; R5 the head and the output chain; FULL the whole line; NOHEAD
the line without the head (a play build with no chain); +RECV with the output chain the receiver computes itself.

| class (law) | planted | H | R5 | R5+ops | R5+ops+claims | FULL | NOHEAD | FULL+RECV | NOHEAD+RECV | receipt differs | output differs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| control (fall + a claim) | — | — | — | — | — | — | — | — | — | no | no |
| value: vx +1, no event | 237 | 237* | 237* | 237* | 237* | 237* | 237* | 237* | 237* | yes | no |
| ops: one more, no event | 237 | — | — | 237* | 237* | 237* | 237* | 237* | 237* | yes | no |
| out: one byte, hashed, no event | 237 | — | 237* | 237* | 237* | 237* | 237* | 237* | 237* | yes | yes |
| claim cost +1 | 237 | — | — | — | 237* | 237* | 237* | 237* | 237* | yes | no |
| silent scalar: landed_at +1 | 237 | — | — | — | — | 237* | 237* | 237* | 237* | yes | yes |
| shared lowering (the adversary's) | 1 | — | — | 1* | 1* | 1* | 1* | 1* | 1* | yes | no |
| out-unhashed: a byte in the file only | 237 | — | — | — | — | — | — | 237* | 237* | **no** | yes |
| refusal where the reference goes on | 237 | 237* | 237* | 237* | 237* | 237* | 237* | 237* | 237* | yes | yes |
| control (the adversary's projectiles law) | — | — | — | — | — | — | — | — | — | no | no |
| shared lowering (projectiles) | 1 | — | — | 1* | 1* | 1* | 1* | 1* | 1* | yes | no |
| budget, no plant (projectiles, budget 2,713) | — | — | — | — | — | — | — | — | — | no | no |
| **shared lowering + budget (A1, A3)** | 1 | **246** | **246** | 1* | 1* | 1* | 1* | 1* | 1* | yes | yes |
| silent list item +1 (a list read each tick) | 237 | — | — | — | — | 237* | 237* | 237* | 237* | yes | yes |
| transient: wrong in its event, right by the boundary | 237 | 237* | 237* | 237* | 237* | 237* | **—** | 237* | **—** | yes | no |
| refusal code (both refuse in tick 63) | 63 | — | — | — | — | — | — | — | — | yes | no |
| stream head: lowering / lowering + budget / transient / silent list | 1 / 1 / 237 / 237 | as the chain's rows | | | | | | | | | |
| **play's no-chain build**, 11 rows: a control and 10 defects (value, ops, claim cost, silent, out-unhashed, refusal, lowering + budget, silent list, transient, refusal code) | as above | head meaningless | | | | | 7 of 10 by the lines | | **8 of 10 by the lines, 9 with the rule** (not the transient) | without its head, the transient's record is equal too | |

The refusal-code row is named by the rule's second step: every line agrees, the records differ, both refused, so the
tick after the last line, 63. Each field catches a class the others miss: `ops` the counting defects, `claims` the
cost, `state` the silent writes, the head the transient, the receiver's chain a byte the runtime never counted (its
receipt reads equal: a self-report cannot convict itself, Verðandi G25's lesson; the arbiter already compares output
bytes and not only the receipt's hash, `src/orlog/arbiter.py`, and the receiver's chain carries that rule to each
tick). Of the 13 planted rows, FULL+RECV with the rule names 13, NOHEAD+RECV with the rule 12 (not the transient),
R5's pair 4 (value, out, refusal, transient), and R5 names the budget case at the end the defect caused, not where it
began. The last eleven rows run
play's proposed build itself, a program with no event chain at all (`r2common.nochain`): its line, without the head
and with the receiver's chain, names 9 of its 10 planted defects at their tick (the shared lowering with the budget at
tick 1, the refusal code by the rule's second step) and its control nowhere; the transient leaves its record, read
without the meaningless head, equal as well, so only admission sees it.

**What it costs (MEASURED, P13, `p13_line_cost.py`).** The adversary's K-bodies law, every tick stamped inside the
program; 3 runs a cell in a seeded shuffled order; falling = ticks 11–80 (70 samples a run), landed = ticks 101–399
(299) at K = 1,000 and 101–2,999 (2,899) at K = 100. Witnesses first: every line of every cell equal to the reference's
(the no-chain cells in every field but the head), every output equal. Medians of the three runs' p50; spread = the
three runs' range; µs a tick.

| K, regime | as built (chain, no line) | chain + line | stream + line | **no chain + line** | no chain, no line |
|---|---|---|---|---|---|
| 1,000 falling | 802.3 (801.3–805.6) | 857.1 (855.9–861.0) | 274.6 (274.1–274.9) | **55.0** (55.0–55.1) | 14.9 |
| 1,000 landed | 1,439.5 (1,439.0–1,442.3) | 1,512.2 (1,510.9–1,513.3) | 439.8 (438.3–439.8) | **62.6** (62.6–62.6) | 22.3 |
| 1,000 landed p99 | 1,619–2,085 | 1,710–2,336 | 514–582 | **75–128** | 25–34 |
| 100 landed | 146.7 (145.9–147.0) | 151.5 (151.4–151.5) | 44.8 (44.7–44.9) | **7.0** (7.0–7.1) | 2.3 |
| 100 landed p99 | 167–196 | 181–219 | 58–62 | **10–18** | 2.3–3.1 |
| relative to as built (landed p50) | 1.000 | 1.051 / 1.033 | 0.306 / 0.305 | **0.043 / 0.048** | 0.015 / 0.016 |

The reference, in process, each tick stamped (3 runs, interleaved): K = 1,000 landed 14,859 µs plain (14,779–15,024),
16,548 with the full line (16,444–16,571), 1.11×; K = 100 landed 1,469 and 1,635 µs, 1.11×. The line is 212 bytes a
tick at K = 1,000 (DERIVED: 7.6 MB for 36,000 ticks). The state digest is most of the line's cost (62.6 − 22.3 µs at
K = 1,000, about 250 compressions of 16 KB); it is linear in the state (round 1's weakness 1 stands: a world of
megabytes digested every k ticks names a silent write's window of k ticks, and every other class still at its tick).

**One more option, not measured.** The survey notes that a per-tick state digest that is not chained lets a difference
"heal", so that only a linear scan finds it (RESEARCH §12, its own reasoning, SPECULATIVE there). The live watcher scans
linearly anyway (round 1, P4: 40,000 lines compared in 1.6 ms); for a later binary search over two long line files,
each line can carry L_t = SHA-256(L_{t−1} ‖ line_t), one compression a tick (about 0.17 µs here, DERIVED from P15b),
and no difference then heals (DECLARED).

**What it does not show.** Any other law, size or host; a resident loop (P13 runs whole programs; P16 is resident);
SNAP-1's real restore; that twelve kinds are all. **Falsifier:** a defect that changes the final receipt, the output
or a later tick's carried state and that no field of the line names at its tick.

### 3.2 Whether R9 b's per-tick budget is safe

**The adversary's case, measured with the line (P12, the shared-lowering + budget row).** The budget is the clean
reference's largest per-tick count at a statement's entry (2,713, my emulation of the check; the adversary's emulation
read 2,717). The compiled program, carrying `orlog.lower`'s one-more-operation-per-multiplication defect, refuses
TICK-BUDGET in tick 246 (245 lines); the reference completes all 300. R5's commitments name tick 246, the tick where the
end moved. The line names tick 1, fields `ops` and `claims`.

**Why the line always names the dissent no later than a moved end (ESTABLISHED, by the budget's definition).** The
budget fires at tick t from operations counted inside tick t. If two executions' cumulative counts agree at every
boundary before t, a refusal that moves to tick t makes one side lack line t, and the reconciler names t; if the counts
parted earlier, the line names the earlier tick. So with `ops` committed, no budget refusal can move without the
reconciler naming a tick at or before it.

**What makes R9 b safe in a live session (DECLARED, each condition held by a measurement).**
1. `ops` in every tick's commitment: the line, and R5's `'T'` payload (P12).
2. The watcher is the reference, never only compiled executions (A2, the rerun: three compiled backends agree at 2,406
   against the reference's 1,806).
3. No refusal is declared before the watcher has reached its tick and refused the same way (the same code, clause,
   tick and operation count in its record), every line before it equal. In live play a TICK-BUDGET (or any) refusal
   ends play's branch (R4 a); its standing is "refused, unconfirmed" until then. In the adversary's case the dissent
   at tick 1 is raised one durability group after tick 1 is played (16 ticks in round 1's design: DERIVED from P10's
   group commit), about 230 ticks before the false end; the policy (§3.3) acts first.

The price of condition 3 is the watcher's lag: a declared outcome waits for the watcher to reach its tick. The
sequential reference at K = 1,000 admits 60 ticks a second, so the wait grows with the match; with 4 lanes of
segments, 197 (P14), so it stays about one segment. Without
SNAP-1 there are no segments, and at that size a declared end of match waits minutes (A8's DERIVED lag stands for that
case).

**A16, conceded.** A budget in counted operations refuses operations, never time; the owner's measure, as the sheet
quotes it, "a tick that exceeds its budget produces a signed refusal event, never an overrun", holds in operations
only. **What does track a compiled tick's time (MEASURED, P15 `p15_work_counted.py` and P15b `p15b_stamped.py`):**
eight laws as the arbiter builds them; counts exact, by difference between two loop bounds of a build that counts every
call of the compression function and every committed byte (P15); time per tick stamped inside the program for the six
laws whose ticks are long enough (P15b: 3 runs, the median of each run's per-tick p50 over the window shown), and the
slope of medians of 7 process runs for the two whose ticks are a few clock steps long (P15: adds over 2,000,000 ticks,
fall over 36,000; their bound differences, 669 and 48 ms, far above the spreads). P15's slopes for the six long laws
are in `p15.txt`; the shortest of them (sh-64: 7.3 ms of difference against a 12–26 ms spread at its lower bound) was
soft, which is why P15b exists.

| law | µs a tick | ops | events | SHA-256 compressions | µs per op | µs per compression | timed by |
|---|---|---|---|---|---|---|---|
| adds | 0.335 | 3 | 2 | 2 | 0.112 | 0.167 | slope |
| fall | 1.349 | 22 | 8 | 8 | 0.061 | 0.169 | slope |
| sh-64 (round 1's P5 law), ticks 11–1,999 | 49.9 | 2,236 | 286 | 286 | 0.022 | 0.175 | stamps |
| bodies, K = 100, landed, ticks 101–1,999 | 147.1 | 1,502 | 501 | 901 | 0.098 | 0.163 | stamps |
| bodies, K = 1,000, falling, ticks 11–80 | 799.4 | 13,002 | 3,001 | 5,001 | 0.061 | 0.160 | stamps |
| bodies, K = 1,000, landed, ticks 101–399 | 1,434.9 | 15,002 | 5,001 | 9,001 | 0.096 | 0.159 | stamps |
| bodies saying every height, landed, ticks 101–299 | 1,686.9 | 17,002 | 6,001 | 10,063.5 | 0.099 | 0.168 | stamps |
| copy of a 2^20-item list, ticks 3–23 | 23,708.5 | 2 | 2 | 131,074 | 11,854 | 0.181 | stamps |
| **spread, largest / smallest** | | | | | **5.3×10^5** | **1.13** | |

Across five orders of magnitude of tick time, the compiled tick is its compressions at 0.159–0.181 µs each on this host.
So if the owner wants the budget to say something about work, it can count committed blocks, Σ over a tick's events of
⌊(49 + payload length)/64⌋ + 1 (the chain's own block count, a function of the trace alone), beside or instead of
operations. That counter lives in each of the four runtimes, not in the shared lowering, so a lowering defect cannot
move it without changing the events the head commits (ESTABLISHED, read: `gen_c.py` emits `orl_ev_*` calls; the
runtime builds every payload). Does not show: the reference's time per block (not measured in one apparatus), a play
build without the chain, any other host. Falsifier: a law whose compiled time per compression on this host lies
outside 0.10–0.25 µs.

**Verdict on R9 b.** Keep it, as a deterministic refusal bound and never as a time guard, with conditions 1–3 written
into the sheet and the unit left to the owner (§5). Without condition 3 it is unsafe for any outcome that matters,
since the end of a match would rest on a count the authority may dispute.

### 3.3 What a live outcome is

A definition, proposed for the sheet (DECLARED):

| standing | when | may be shown | may be declared (scored, ranked, settled) |
|---|---|---|---|
| PLAYED | play executed the tick | yes, marked provisional | no |
| WATCHED | the reference's line for the tick equals play's in every field play commits, and every earlier one did | yes | yes, "confirmed on this host" |
| REPLAYED | the closed log through all four executions, the arbiter's verdict | yes | yes, "replayed four ways over log ⟨seal⟩, unratified" |
| VOID | at or after a tick a dissent names | as history only | never |

- **Whose record stands.** Before t*, the reference's and play's agree, so either. From t* on, play's record is void,
  and so is the reference's as a record of the match: it replays inputs that answered a picture the law did not
  produce. It stays as the reference's computation over the logged inputs, a fact about the law, not about the match.
- **What play does at a dissent:** the owner's policy, as round 1 put it: (a) stop; (b) resynchronize from the
  reference's state at t* − 1, which starts a new branch; (c) go on, unadmitted. In the genre this is what
  reconciliation already means: the authority's state overwrites the client's prediction and pending inputs are
  replayed (Gambetta, [P], RESEARCH §3). Here a mismatch is a defect to record, not an expected event.
- **How long PLAYED lasts:** about one durability group while the watcher keeps pace (round 1, P10: 16 records, 0.27 s
  at 60 ticks a second, DERIVED); about one segment where it keeps pace only in segments (P14: 100 ticks of 16.5 ms of
  software time, DERIVED); unbounded where it cannot keep pace at all.
- **Never.** "Verified", "final", "fair" or "admitted" for a PLAYED outcome; "grounded" for anything over an input log
  (R6 a).

### 3.4 Verðandi's floor-mirror leak, and "decorates, never decides"

**Reproduced (MEASURED twice on this host: the adversary's run and mine, identical in every cell).** A target wholly
behind a 4 m wall changes 76–457 pixels by up to 30 levels at plaza-night's wet floor, 162–1,076 pixels by 1–3 levels
on a dry rough floor; the render's own noise is 0 pixels in 5 pairs. The first ablation shrinks it; the second removes
the wet leak and leaves 140 and 98 pixels at 1 level on the dry floor at 20 and 26 m. Same browser engine (a Chrome
152 engine, as the adversary recorded) and the same GPU: a reproduction, not a second platform.

**What it means for the rule.** The owner's words, in Verðandi's `docs/BOUNDARIES.md`: the renderer "must not silently
decide where walls, cover, or player-blocking objects exist". The leak decides none of those: it adds no solid and
moves none, and C is untouched. The checks that hold the rule (`render-conforms`, `art/check.py`) look at geometry,
and the leak is not geometry (ESTABLISHED by reading what they check; not run here, since running them would write in
Verðandi's tree). The record's own short form, "The render world may decorate and may not decide (the owner's rule,
FPS-VISUAL-0)", is followed at once by what it means there (every solid drawn is a column of C at C's height), and the
graybox README says exactly that much: the renderer "decorates, decides nothing that blocks". Read with its next
sentence, the short form holds. Read alone as "cannot affect play", it overclaims: here the renderer decided what a
player can learn about hidden state, and the rule's last sentence, about decoration "intended" to affect gameplay,
cannot reach an effect nobody intended. So the lineage's view rule has two properties, and only the first is checked
today:

1. **No write-back** (program non-interference). Checked by the state field (P12: silent writes named at their tick)
   and, as Verðandi does, by holding the state equal with and without a view (`render-readonly`; RESEARCH §10).
2. **No disclosure** (information non-interference): a pixel depends on nothing the viewer's player may not know. It
   holds by construction when the view is given only that player's visible set and has no other way to the hidden
   state, since a deterministic renderer's picture is a function of its inputs (DECLARED; the render's own noise was 0
   pixels in every control pair here, MEASURED). For a renderer given more, the adversary's page is the court: for
   each entity the law marks hidden from the viewer, the frame with it must equal the frame without it, pixel for
   pixel. One differing pixel convicts on that platform. No run acquits
   on another GPU, driver or engine (the survey's reading of the specifications: no API fixes a GPU float to the bit,
   [P], RESEARCH §4). The same construction answers A11's field of view: when the law decides the visible set with its
   own field of view, a wider canvas shows more of that set's surroundings and never an entity the law withheld.

**For Ørlǫg** (DECLARED): what a player may see is decided in the law, in Fix, and the door hands each view only its
player's share (per-player output, A22); the renderer may then reflect, fog and bloom as it likes. For Verðandi, the
owner's to weigh: its page already hands the whole live state to the browser's console as `window.GRAYBOX`, for tests
(its `docs/BOUNDARIES.md`, the interface's row; ESTABLISHED), so nothing there is hidden from its player in the first
place and the leak adds nothing; it would matter in any world that claims to hide something. A falsifier of the claim that matters: a competitive client built on a renderer given hidden
entities, with the pixel court reading 0 at every hidden entity on every platform it ships to.

### 3.5 HEADROOM-0 after G10 and G13

G10: at n = 200 a p99 is the third-largest sample, labels flipped on three samples, zero-margin boundaries flipped on
2 against 24 µs; the remedies are 1,000 samples a cell, a same-run comparator, a declared margin, counts beyond the
threshold beside the percentile, and host state. G13: a preregistered second run read 41% and 59% slower the same day;
within-run comparisons absorbed the common shift, a shift not common to both cells moved a label, and no millisecond
figure carries between runs; DRIFT-0 is its designed panel (Verðandi `docs/GHOSTS.md`, ESTABLISHED).

**What a falsifiable standard needs**, as the r2 draft writes it
(`work/speed-probe/r2/headroom0-r2-draft.json`, sha256
`a77a6424b5d6072d1ee41a7e207f65ebc19e64debb3f784fb1f6396329fb894c`, hashed at 09:48:45, before the pilot existed):

1. **A question that can come out FAIL**, about one component on one host: does the play tier's per-tick service time,
   for a named law over a named log, stay within B of P at p99 in every regime and in every run of a confirmation set?
   Never "competitive" (A19, A20).
2. **The observable per tick**, never a slope (A18): from the input record written to the line read, through the
   resident pipe.
3. **Regimes ruled separately, 1,000 samples each** (A17, G10); a regime with fewer is TOO FEW TO RULE, reported by its
   maximum and 12 largest, never averaged into another.
4. **Counts beside the percentile** (G10): samples over B·P and over 2·B·P, with p50, p90, p99.9 and the maximum.
5. **Same-run comparators** (G4, G13): FLOOR (the transport, the VOID gate) and CALIB (a fixed workload; PLAY's ratio
   to it reported, never ruled).
6. **A confirmation set** (G13): HELD iff PASS in every run of at least three, over at least two sittings 30 minutes
   apart. A label is never carried to another run.
7. **A drift panel before the first registered run** (DRIFT-0's shape: three sittings of four runs of CALIB, host state
   beside each, no verdict); a run outside the panel's range is marked so, and its label stands: a host's slow states
   are part of the host.
8. **What it does not show**, written into the entry; and the apparatus's own falsifiers (synthetic samples at the bound
   read PASS, one step above FAIL; a dropped line refused by the witness, never timed).
9. **Proposed after the pilot, so not preregistered against it: a margin wider than the host's drift** (the adversary's
   §6.4 item 5). The bound becomes 950‰ × B × P / (1 + d), where 1 + d is the largest between-run ratio of CALIB's p50
   (slowest over fastest) in the host's drift panel, registered before the first run. At G13's worst recorded drift
   (d = 0.59) the 1/120 s
   bound would be 498 µs. The r2 draft's hash does not cover this item; a revision that adds it is a new draft, hashed
   before its own first run.

**The pilot (MEASURED; the instrument on a stand-in, not a reading: RUN-1 is not built and one byte gates each tick;
G12's warning applies).** `p16_headroom_pilot.py`: the adversary's law at K = 1,000, 1,100 gated ticks; five processes
alive at once, one sample each per round in a seeded shuffled order; witness first (every line of every cell equal to
the reference's). Landed regime, 1,000 samples a cell; the falling regime has 80 samples after warm-up and is TOO FEW
TO RULE by construction of the law. The apparatus's own falsifiers first, on synthetic samples (`p16_apparatus.py`,
deterministic): the 11th largest of 1,000 at the bound reads PASS and one 0.1 µs step above reads FAIL; a lower half
moved from a p50 of 50 to 361 µs under the same tail leaves the label unchanged.

µs per tick, landed regime, 1,000 samples a cell a run (`p16_table.py run1 run2 run3`, from the runs' own JSON; their
12 largest samples a cell are there too); "over" counts samples over the 1/120 s and 1/60 s bounds; host CPU busy
49–151‰ and memory load 96–98% around the runs; clock step 0.1 µs.

| run (started) | cell | landed p50 | p90 | p99 | p99.9 | max | over 792 µs | over 1,583 µs | 1/60 s | 1/120 s | falling: n, max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| run1 (09:56:29) | FLOOR | 23.1 | 55.0 | 99.0 | 1250.8 | 1594.1 | 2 | 1 | — | — | 80, 96.1 |
| run1 (09:56:29) | PLAY | 91.8 | 194.3 | 367.7 | 778.3 | 3588.9 | 1 | 1 | PASS | PASS | 80, 252.3 |
| run1 (09:56:29) | STREAM | 487.0 | 874.2 | 1281.4 | 2251.5 | 2471.1 | 129 | 4 | PASS (beside) | FAIL (beside) | 80, 1022.7 |
| run1 (09:56:29) | CHAIN | 1717.1 | 2514.7 | 3392.0 | 4450.8 | 6413.6 | 1000 | 933 | FAIL (beside) | FAIL (beside) | 80, 2267.5 |
| run1 (09:56:29) | CALIB | 32.6 | 71.2 | 129.0 | 1262.9 | 1357.0 | 2 | 0 | — | — | 80, 130.5 |
| run2 (09:57:33) | FLOOR | 18.5 | 40.3 | 110.7 | 1768.5 | 2710.3 | 2 | 2 | — | — | 80, 62.4 |
| run2 (09:57:33) | PLAY | 83.3 | 191.5 | 329.1 | 1394.0 | 1494.5 | 3 | 0 | PASS | PASS | 80, 257.1 |
| run2 (09:57:33) | STREAM | 462.1 | 899.6 | 1207.6 | 2352.4 | 4521.6 | 150 | 6 | PASS (beside) | FAIL (beside) | 80, 808.9 |
| run2 (09:57:33) | CHAIN | 1590.3 | 2285.2 | 3100.5 | 4287.6 | 5991.4 | 1000 | 519 | FAIL (beside) | FAIL (beside) | 80, 2070.8 |
| run2 (09:57:33) | CALIB | 27.6 | 57.3 | 117.6 | 208.8 | 506.8 | 0 | 0 | — | — | 80, 215.4 |
| run3 (10:28:02) | FLOOR | 16.7 | 38.5 | 112.8 | 145.3 | 167.4 | 0 | 0 | — | — | 80, 98.9 |
| run3 (10:28:02) | PLAY | 81.5 | 184.1 | 322.7 | 1114.0 | 2271.9 | 2 | 1 | PASS | PASS | 80, 405.1 |
| run3 (10:28:02) | STREAM | 460.4 | 915.6 | 1276.0 | 2272.3 | 2360.5 | 156 | 3 | PASS (beside) | FAIL (beside) | 80, 719.7 |
| run3 (10:28:02) | CHAIN | 1640.2 | 2272.3 | 3076.4 | 4587.2 | 7207.3 | 1000 | 553 | FAIL (beside) | FAIL (beside) | 80, 1657.1 |
| run3 (10:28:02) | CALIB | 25.4 | 52.1 | 141.8 | 209.9 | 1488.1 | 1 | 0 | — | — | 80, 53.9 |

Within-run ratios of the landed p50 to CALIB's: PLAY 2.82, 3.02, 3.21; STREAM 14.9, 16.7, 18.1; CHAIN 52.7, 57.6,
64.6. The confirmation set is complete (runs 1 and 2 in one sitting, run 3 in a second sitting 30.5 minutes after run
2): PLAY reads HELD at both periods; beside it, never ruled, the stream head HELD at 1/60 s and NOT HELD at 1/120 s,
and the chain NOT HELD at both. These are a pilot's labels on a stand-in, not a registered reading.

What the pilot shows about the method: the rule returns PASS for PLAY and FAIL for CHAIN at both periods, and splits
the stream head between them; a confirmation set across sittings is cheap to run; the transport's extreme tail
(FLOOR's p99.9 1.3 and 1.8 ms in the first sitting, 0.15 ms in the second) reaches past the 1/120 s bound in some runs
while its p99 stays near 0.1 ms, which is why the VOID gate reads p99 and the counts are reported beside it; even the
within-run ratios moved 14% (PLAY) and 23% (CHAIN) between runs, so a ratio, too, belongs to its run; and a law with a
short regime cannot be ruled in it, whatever its p99 would read. In orders of magnitude only (another apparatus),
PLAY's p99 through the pipe, about 3×10^-4 s, lies two orders below the refresh period Verðandi measured, about
1.3×10^-2 s (G10). That says nothing about a frame, a latency or a player.

---

## 4. The four questions, revised

**Q1. The two-speed design.** Three tiers over one log, as in round 1, with play changed: play is the law's C program
built without the event chain, resident, writing the line every tick (P13: 4.3% of the as-built tick at K = 1,000
landed; P12: it names every planted class but the transient). The watcher is the reference, replaying the durable log
behind play and writing the same line with its head, in segments from play's checked snapshots once SNAP-1 exists
(P14: 4 lanes keep pace at K = 1,000). Admission runs the four executions with the full chain over the closed log.
RUN-1's formats must commit per tick: the line's fields (`ops`, the claims digest and the state digest are what R5
lacks), `ops` in `'T'`, the output chain's edges, and the receiver's own chain over the bytes it got. Missing from the
sheet: the line, the live-outcome standings, the door's port ranges, the log as a stream with an end record, and the
meaning of `ticks` at a refusal.

**Q2. A language swap.** No. The tick without the chain's hashing is 1.5% of the compiled K = 1,000 tick (P13) and
5–7% of fall's (round 1); the lever was the commitment, and the largest saving is not to commit events in play at
all. Across eight laws the compiled tick is its SHA-256 compressions at 0.159–0.181 µs each (P15b). The stream head (round
1's "now or never") is no longer needed for play's speed; it remains an option for the throughput of the compiled
admission executions (0.29–0.73 of the chain's commitment cost, round 1's P7), the owner's to take or leave in
`orlog-trace-1`. A GPU backend is never authoritative: at most a fifth execution, Int and Fix only, held byte for byte
to the reference (both parties, A15); its only use is many worlds at once (previews, sweeps), measured against round
1's P8 baseline.

**Q3. The view tier.** It reads each tick's output (and, after SNAP-1, snapshots) one way, and reaches the law only as
an input record of a later tick through the door. Its fence has two parts: no write-back, witnessed every tick by the
state field (P12); and no disclosure, which holds by construction only when the door hands it its player's share. What
must be in the law, in Fix: whatever decides an outcome or what a player may know (line of sight, visible sets, light
levels that a rule reads), with its precision stated at the scales it meets: P17's pre-scaled normalization gives the
nine SH basis values within 3.8 units of 2^-32 of binary64 from 2^-28 m to 2^24 m. Shaders, SH lighting and
post-processing stay in the view, in floats, hashed by nothing. `Say` stays the law's only channel to the view; in a
play build without the chain, a said line costs its bytes and the output hash, not an event commitment (DECLARED;
NOT_MEASURED here); after SNAP-1, a view that draws many bodies reads typed snapshots instead (round 1).

**Q4. A headroom standard, Verðandi's way.** A preregistered method, never a number (§3.5): per-tick samples through
the resident pipe, per regime, 1,000 each, p99 against 950‰ of B·P with counts beside, FLOOR and CALIB in the same
run, a confirmation set across sittings, a drift panel recorded and never voiding, a margin wider than that drift (the
adversary's item, proposed after the pilot), and a list of what it cannot show. The owner registers it or does not;
the r2 draft's hash fixes what the pilot ran against.

---

## 5. Proposed changes to the RUN-1 sheet (for the owner's ruling; none is an edit)

| | proposal | why | grade | falsifier |
|---|---|---|---|---|
| **must** | **A tick line**, `orlog-ticks 0`: every execution given a path writes one line per tick boundary (fields as §3.1); a play build may write `-` for the head; one more argument in R11's revision of `orl_init` | of 13 planted defects, R5's per-tick commitments name 4 at their tick; the line with the rule names 13 (12 without the head) | MEASURED (P12) | a defect that changes the receipt, the output or later carried state, and no field names its tick |
| **must** | **R5's `'T'` payload: the tick and the operation count at the boundary** (u64, u64) | the trace alone then names an operation-count divergence at its tick (the adversary's item 1, P12's R5+ops column) | MEASURED (P12) | a counting defect whose first differing per-tick head is not the tick where the counts part |
| **must** | **The reconciler's rule**: lines first; if all agree, the final records, a refusal naming the tick after the last line; the output chain recomputed by the receiver over the bytes it received in each tick, never taken from play's line | the refusal-code and out-unhashed rows: the lines agree or the receipts agree while the executions differ | MEASURED (P12) | two executions differing in output bytes or in a refusal's record that the rule leaves unnamed |
| **must** | **The output chain's start and edges** (round 1): out_0, the prefix's output, a refused tick's partial output | R5 leaves them undefined | ESTABLISHED | two executions equal in every byte and different in chain |
| **must** | **The log as a stream with an explicit end record**; D3's "a run completes when its log ends" to mean that record (round 1; the adversary's §2.4) | a replay of a log still being written would complete early | ESTABLISHED | a truncated log that yields COMPLETED |
| **must** | **What `ticks <n>` counts at a refusal**: ticks begun; a refused tick writes no line | the reconciler counts lines | ESTABLISHED | two executions refusing at one operation that disagree on `ticks` |
| **must** (was should) | **A port may declare a range the door enforces**, refusing an out-of-range record whole without ending the session; the owner rules what the tick then receives (the previous value, a declared default, or no tick until a valid record), and the spelling, which R2's probe must show v0 refuses at the statement (for instance `Let thrust be given each tick as a fixed from -10.0 to 10.0.`: the snapshot's front end refuses it SYNTAX at the statement, checked once here; COMPAT-0's frozen texts not searched) | A9: any client able to drive the law into a refusal ends the match for all | MEASURED (stand-ins, rerun); remedy DECLARED | an out-of-range value that reaches the law |
| **must** | **R9 b's three conditions**: `ops` committed per tick; the live watcher is the reference; no live refusal declared before the watcher has refused at the same tick with the same record, every earlier line equal | A3: the false end at tick 246 with the compiled executions agreeing | MEASURED (P12, P14); conditions DECLARED | a budget refusal that moves and is declared before any tick at or before it is named |
| **option** | **R9 b's unit**: committed blocks beside or instead of operations | time per compression spread 1.13× over eight laws, per operation 5.3×10^5; the counter is the runtimes', not the lowering's | MEASURED (P15, P15b) | a law whose compiled time per compression lies outside 0.10–0.25 µs here |
| **new ruling** | **R13, what a live outcome is**: PLAYED, WATCHED, REPLAYED, VOID (§3.3); never "verified", "final" or "fair"; the admission phrase "replayed four ways over log ⟨seal⟩, unratified" (A21) | A4 | DECLARED | a design in which a PLAYED outcome and a later dissent over the same tick both stand |
| **new ruling** | **R14, play's build**: the c99 program may be built without the event chain for play (a runtime-contract option); such a build's record is testimony, never one of the four executions | 4.3% of the as-built tick; the build itself names 9 of its 10 planted defects at their tick, not the within-tick transient | MEASURED (P12, P13) | a defect that changes carried state or output and that the no-chain line does not name at its tick |
| **option, lowered** | **The stream head in `orlog-trace-1`**: an admission-throughput option, no longer needed for play | R14 removes the chain from play | MEASURED (round 1 P7, P13) | a class the chain names at its tick and the stream does not (none in P7 or P12) |
| **should** | **SNAP-1 next after RUN-1**, with snapshots that hold lists | the watcher keeps pace at K = 1,000 only in segments; localization from a snapshot | MEASURED (P14; round 1 P4, P11) | a restored run whose later lines differ from the sequential run's |
| **should** | **R12's discriminator gains P12's plants**: ops at a tick, claim cost, silent scalar and list writes, a byte in the output only, a transient, a refusal moved, the shared lowering with a budget, each named at its tick | the dropped-`'N'` plant tests events only | MEASURED (P12, on stand-ins) | any such plant not named at its tick in the built RUN-1 |
| **should** | **"What this sheet does not decide" names per-player output** as a precondition of any competitive use | A10, A22 | MEASURED (the leak); DECLARED | a competitive claim made on one output stream for every observer |
| unchanged | R1–R4, R6 a (the phrase above added), R7, R8 b, R10, R11 (one argument more), D1, D2, D4–D10 | | | |

---

## 6. The probes, as run

From `work/speed-probe/r2/` unless said, `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B <script>`, one at a time, nothing
else of this round running. Clock step 0.1 µs everywhere; every median below is at least 10 steps.

| probe | what | samples | result |
|---|---|---|---|
| reruns | the adversary's 16 scripts and 3 pages, from byte-identical copies (`adv-rerun/`) | each script's own | §1; `adv-rerun/*.txt`, `adv-rerun/webleak/results/` |
| P12 `p12_plant_matrix.py` | 13 planted defects, 3 controls, 4 stream variants and 11 rows of play's no-chain build × 8 readings | deterministic | `p12.txt`, `p12.json` |
| P13 `p13_line_cost.py` | 5 commitments × 2 sizes × 2 regimes, every tick stamped in the program; the reference stamped | 3 runs a cell; 70/299 (K = 1,000) and 70/2,899 (K = 100) ticks a run; reference 70/99 and 70/899 | `p13.txt`, `p13.json` |
| P14 `p14_segments_bodies.py` | the watcher in segments at K = 1,000, T = 1,600; two plants | 3 rounds a cell | `p14.txt`, `p14.json` |
| P15 `p15_work_counted.py` | eight laws: ops, events, compressions, committed bytes (exact) against time (slopes) | 7 process runs a bound | `p15.txt`, `p15.json` |
| P15b `p15b_stamped.py` | the six long-tick laws of P15, every tick stamped | 3 runs; 21 to 1,989 ticks a run | `p15b.txt`, `p15b.json` |
| P16 `p16_headroom_pilot.py` | HEADROOM-0 r2's instrument, 5 cells, 1,100 gated ticks | 1,000 landed samples a cell a run; 3 runs, 2 sittings | `p16-run*.txt`, `.json` |
| P16 `p16_apparatus.py`, `p16_table.py` | the rule's apparatus falsifiers on synthetic samples; the runs as one table with the confirmation set | deterministic | `p16-apparatus.txt`; §3.5 |
| P17 `p17_sh_prescale.py` | A12 with and without the pre-scale; the law through the arbiter | 2,000 directions or triangles a scale; 8 laws | `p17.txt`, `p17.json` |

The measured lines behind §3 (µs; spread = range over runs, or minimum–maximum for process runs):

| probe | cell | n | median | spread |
|---|---|---|---|---|
| P13 | K = 1,000 landed, as built, p50 per run | 3 × 299 | 1,439.5 | 1,439.0–1,442.3 |
| P13 | K = 1,000 landed, no chain + line, p50 per run | 3 × 299 | 62.6 | 62.6–62.6 (p99 74.9–127.5) |
| P13 | reference K = 1,000 landed, plain / line, p50 per run | 3 × 99 | 14,859 / 16,548 | 14,779–15,024 / 16,444–16,571 |
| P14 | sequential / 2 / 4 / 8 / 16 lanes, ms for 1,600 ticks | 3 rounds | 26,479 / 14,625 / 8,117 / 5,998 / 4,199 | 25,824–27,928 / 13,784–15,068 / 8,025–8,965 / 5,073–6,519 / 4,102–4,580 |
| P15 | adds, ms at T = 100,000 / 2,100,000 | 7 / 7 | 49.87 / 718.98 | 44.47–58.94 / 711.33–729.58 |
| P15 | fall, ms at T = 4,000 / 40,000 | 7 / 7 | 18.63 / 67.18 | 17.35–28.49 / 64.79–82.45 |
| P15b | sh-64, per-tick p50 of each run | 3 × 1,989 | 49.9 | 49.9–50.0 |
| P15b | copy 2^20, per-tick p50 of each run | 3 × 21 | 23,708.5 | 23,409.5–23,812.2 |
| P15b | bodies K = 1,000 landed, per-tick p50 of each run | 3 × 299 | 1,434.9 | 1,434.7–1,436.2 |

**Commands**, all with `PYTHONHASHSEED=0 PYTHONUTF8=1`, between 09:32 and about 10:30 local time on 2026-10-26:
from `work/speed-probe/adv-rerun/`, `python -B <script>.py` for the deterministic copies and `python -B run_timed.py`
for the timing ones (`run_timed.log` holds each start, end and host state); `python -B webleak/serve.py 8767`, then
the pages `index.html`, `ablate.html` and `ablate2.html` opened from 127.0.0.1:8767 in the built-in browser pane (each
posts its own result file); from `work/speed-probe/r2/`, `python -B p12_plant_matrix.py`, `p13_line_cost.py`,
`p14_segments_bodies.py`, `p15_work_counted.py`, `p15b_stamped.py`, `p17_sh_prescale.py`, and
`p16_headroom_pilot.py run1`, `run2` (09:56 and 09:57) and `run3` (10:28), then `p16_table.py run1 run2 run3`.

Disk: `work/speed-probe/runs2/` (about 0.4 GB, both rounds' builds) and `adv-rerun/runs/` (about 66 MB) can be deleted.

---

## 7. The claims, graded

| # | claim | grade | does not show | falsifier |
|---|---|---|---|---|
| 1 | The line (§3.1), read by the reconciler's rule, names all 13 planted defects at their tick and no control; without the head, 12 (not the within-tick transient), and play's no-chain build itself 9 of its 10; R5's pair 4 | MEASURED (P12, stand-in laws) | that 12 kinds are all; RUN-1 as built | a class that changes the receipt, output or carried state and is not named at its tick |
| 2 | Play without the chain, with the line, runs the K = 1,000 landed tick at 62.6 µs p50, 4.3% of the as-built 1,440 µs | MEASURED (P13, 3 × 299 ticks) | other laws, hosts; a resident loop's tail (P16 pilots it) | a confirmation run here whose ratio lies outside 0.03–0.06 |
| 3 | With the shared-lowering defect and R9 b's budget, R5 names tick 246 and the line tick 1 | MEASURED (P12) | RUN-1's real budget check | the built RUN-1 naming 246 with `ops` committed |
| 4 | The reference keeps pace at K = 1,000 and 1/120 s with 4 lanes of segments (197 ticks a second), not with 2 (109) | MEASURED (P14) | play running at once; SNAP-1's restore; other sizes | a rerun here where 4 lanes read under 120 |
| 5 | Compiled time per SHA-256 compression lies within 1.13× across eight laws (0.159–0.181 µs); per operation 5.3×10^5 | MEASURED (P15, P15b) | the reference; a no-chain build; another host | a law outside 0.10–0.25 µs a compression here |
| 6 | The pre-scale brings SH bands 0–2 within 3.8 units of 2^-32 from 2^-28 m to 2^24 m, 0 refusals; the law agrees four ways | MEASURED (P17) | input quantization; bands above 2 | a vector in that range whose basis differs by more, or refuses |
| 7 | The floor-mirror leak reproduces cell for cell | MEASURED (twice, one engine and GPU) | another platform; that a person would see it | a rerun here differing in any cell |
| 8 | HEADROOM-0 r2's rule can return PASS, FAIL and TOO FEW TO RULE on this host; its confirmation set (3 runs, 2 sittings) holds PLAY and not CHAIN at 1/120 s | MEASURED (P16, a stand-in; 3 × 1,000 samples a cell) | any registered reading; any shipped play loop | the rule unable to return FAIL for CHAIN at 1/120 s here, or a fourth run here in which PLAY's p99 exceeds 792 µs |
| 9 | Live outcome standings, R9 b's conditions, play's no-chain build, the view's two clauses, the sheet's changes | DECLARED | that any of it works as built | each row of §5 |

---

## 8. What round 1 got wrong, and where this is weakest

**Corrections to round 1.**
1. Round 1 DERIVED that two lanes would keep the 1,000-body reference at pace at 1/120 s, from fall's 1.94× and a
   reference tick of 12.5 ms measured on my own law, which has no landed regime. On the adversary's law the reference
   takes 14.9 ms a landed tick plain and 16.5 ms with the line (P13); two lanes read 109 ticks a second, under the 120
   needed; four keep pace (P14).
2. Round 1's per-tick costs (P1, P3, P7) were slopes on laws with one regime; A17 and A18 apply to them. Round 2's
   figures are per tick, in both regimes.
3. Round 1 offered the stream head as the way to make play fast, "now or never". Play is faster with no event
   commitment at all and the line (0.043 against 0.31 of the as-built tick); the stream head is now an admission
   option.
4. Round 1's 1.5 units of 2^-32 for SH held for unit-scale directions only (A12); with the pre-scale, 3.8 units at
   every scale tried.
5. Round 1's view fence was write-back only; disclosure is a separate property, and the leak shows it failing.
6. Round 1 said the reference's record stands after a dissent; after t* neither record is the match.
7. Round 1's P5 put an SH evaluation at 1.22 µs in C, a slope whose upper bound's p10–p90 spanned 38–181 ms; stamped
   per tick, the same law reads 49.9 µs a tick of 64 evaluations, 0.78 µs each (P15b). The order of magnitude stands;
   the figure was soft, as A18 says slopes are.

**Weakest points.**
1. **The state digest is linear in the state**, and a cheaper incremental digest would miss exactly the silent writes
   it exists for. Large worlds trade "names the tick" for "names the window" on silent writes.
2. **Segments need SNAP-1 in all four executions**, and P14 never ran play and the lanes at once on this host.
3. **The watcher's lag is a policy cost**: a PLAYED outcome waits a durability group or a segment, and longer where the
   reference cannot keep pace.
4. **Play without the chain is a new build mode** in the runtime contract, and its record must never be confused with
   one of the four executions.
5. **The receiver's own output chain** was modelled in P12 by the C library's file position at each tick boundary,
   written by the play process itself; a real tap would be another process.
6. **Fairness is out of reach** of every check here: the door's tick assignment (A5) and what the player saw (A11)
   are not in any receipt.
7. **Every timing is this host, one sitting**, under 93–98% memory load and other sessions; the pilot's confirmation
   across sittings is one confirmation set, not a panel.
8. **Everything here leans harder on the reference**, as T11 warns: the watcher, the live confirmation and the line's
   meaning all take the reference's line as the standard. A defect the reference shares with play (the front end, the
   specification) passes every check in this report; only the twin's independent reading stands against it.
