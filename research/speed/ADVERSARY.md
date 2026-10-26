# Debate record: the adversary's report on the speed debate, round 1 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the proponent's design and the
prior-art survey. Its experiments ran against a snapshot of f16dc26 and are in `work/speed-adv/` (ignored by git);
its MEASURED lines are this host's. Its Verðandi experiment ran a copy of Verðandi's renderer; Verðandi was read,
never written.

---

# The speed debate, round 1: the adversary's report (2026-10-26)

A subagent's report for the debate PROPOSAL.md opens (`research/speed/PROPOSAL.md`). It is model output, not the owner's
words, and carries no authority. Round 1 prosecutes the premise and the designs that PROPOSAL.md and the skeptic's
"two speeds" (`research/roadmap-debate/SKEPTIC.md`) imply. The proponent's report has not been read.

**Where this ran.** On this host, with other sessions running: the debate's other parties, and another session that
was editing `src/`, `orl.py` and `tests/`. Toolchains as AGENTS.md §5 names them (CPython 3.14.5, clang 22.1.8,
rustc 1.96.1).
- **Ørlǫg** was imported and built only from a snapshot of the last commit, `f16dc26`, made with `git archive HEAD` into
  `work/speed-adv/tree`, never from the working copy. Every script refuses to run if `orlog` imports from anywhere else.
  The arbiter's build folders were kept under `work/speed-adv/tmp`. Documents are cited as committed at `f16dc26`.
- **Verðandi** was read and never written. Its native renderer, `art/web/scene_render.js` (sha256 `0b5cae9d…`, last
  changed in 33558d6, Verðandi HEAD b441a1e), was copied into `work/speed-adv/webleak/` and run there. It ran in this
  host's built-in browser pane, whose user agent names a Chrome 152 engine. The GPU's name is not recorded.
- **Clocks.** `time.perf_counter` (QueryPerformanceCounter, resolution 1e-7 s), or QueryPerformanceCounter read directly
  by an instrumented program.
- **Environment.** PYTHONHASHSEED=0, PYTHONUTF8=1, `python -B`, scripts run from `work/speed-adv/`.
- **Files.** No tracked file was changed. Scripts and their outputs are in `work/speed-adv/` (ignored by git); each
  output's first line names its script and the tree. The first attempt's outputs are kept in `work/speed-adv/attempt1/`
  for comparison, and §8 says what was wrong in them.

**Grades.** MEASURED (a run here; the command is the script named), ESTABLISHED (read from code or a cited record),
DECLARED (an argument, or a statement that nothing checks something), OBSERVED, SPECULATIVE, NOT_MEASURED. DERIVED marks
arithmetic on measured numbers. **Severity**, worst first: *breaks a guarantee*, *overclaims*, *costs more than
stated*, *only words*. Every timing is a software timing on this host. None is a latency, a frame rate, an
input-to-photon figure or a feel, and no number here carries to another host, law or regime.

---

## The findings at a glance

Witnesses side by side, not a score. The rows are in the order of severity the brief sets; the numbers are only names,
used in the text. Each finding is argued in the section named.

| # | finding | grade | severity | § |
|---|---|---|---|---|
| A1 | Per-tick trace heads, as R5 specifies them, are blind to the operation counter and the claims' cost. A divergence there is named at the tick where it first changes an event (tick 246 in the fixture), not where the executions part (tick 1). Committing `ops` at each `'T'` names tick 1 | MEASURED (an emulation of RUN-1) | **breaks a guarantee**: the one Q1 asks for, "name the first tick where two executions part" | 2.3 |
| A3 | Under R9 b, operations become outcome-relevant (a refusal). A counting defect in the shared lowering therefore moves the end of a live match identically on every compiled execution. R9's "at the same operation on every execution" then holds among the compiled executions and fails against the reference | MEASURED (A1, A2) and DECLARED | **breaks a guarantee** | 2.3 |
| A4 | A live outcome is one execution's. After a later divergence the record that stands is the reference's (the arbiter quarantines the backend's run), so the run quarantined is the match the players played | ESTABLISHED (`arbiter.py`) | **breaks a guarantee**, if live outcomes are called final or verified | 2.1 |
| A2 | A reconciler made of the compiled backends cannot see a defect in the lowering they share with a compiled fast path. The three agree (2,406 ops) against the reference (1,806), and no event says where | MEASURED | overclaims | 2.2 |
| A5 | The log is the fast path host's. Which tick an input lands in is decided by a clock no runtime reads. A replay reproduces the log, not the match | DECLARED (DOCTRINE T12, limit 4) | overclaims | 2.1 |
| A10 | The lineage's own renderer puts a hidden target on the screen. Under plaza-night's air, a target wholly behind a 4 m wall changes 76–457 pixels, by up to 30 of 255 in a channel, at the wall's foot, at every tested distance from 6 m to 40 m (a dry rough floor: 162–1,076 pixels, by 1–3). Two ablations of the copied renderer, one line and then one more, isolate the mechanism: the floor mirror's pass. No check in Verðandi looks at this | MEASURED (the leak: one browser engine, one GPU, this host); DECLARED (that no check looks at it) | overclaims ("decorates, never decides") | 3.2 |
| A11 | The view rule covers where blocking things exist, not what a player can see. Field of view, fog, light and reflections decide visibility, and the fog is set by the art file, which a model may write. "Never writes back" holds for the program and fails for the system, because the player is the channel | ESTABLISHED (code and records); DECLARED | overclaims | 3.1, 3.3, 3.4 |
| A12 | In Q31.32, a spherical-harmonic basis is exact only at unit-scale directions. The worst error is 3 units of 2^-32 at length 1, 1.45e-5 at 2^-8 m and 0.276 at 2^-15 m. It refuses below 2^-16 m and above 2^15.5 m, and a triangle's normal refuses at 3 mm edges | MEASURED | overclaims, if the judge's 1.23 units is generalized | 4.1 |
| A14 | A language swap attacks the 2–5% of a compiled tick that is not the chain. RUNTIME-SPEC §1 keeps the hardware path to a cheaper chain out of both compiled runtimes (standard headers only, no compiler extensions, no `unsafe`) | MEASURED (A7); ESTABLISHED; DERIVED | overclaims (a category error) | 5.1 |
| A15 | A GPU backend can be at most a fifth witness, not an authority. The chain is serial by definition. Q31.32 needs 64-bit products, about 155 32-bit operations each in an emulation. Fix products and refusals depend on order, and a float32 projection's bits move with the reduction order | MEASURED; ESTABLISHED | overclaims | 5.2 |
| A16 | A budget of counted operations does not bound a tick's time. One tick of 2 counted operations takes 352 ms in C, and one counted operation can cost 10^5 times another. On the skeptic's own law, from tick 91 operations grow 15% while time grows 80% | MEASURED | overclaims (the owner's "never an overrun", read in time) | 6.2 |
| A19 | A "headroom standard" stated as a number is a scalar scorecard over numbers Verðandi's own ghosts say do not carry (G4, G5, G10, G12, G13, G21). A falsifiable one is a preregistered method over one component, and it can never speak to competitiveness | ESTABLISHED; DECLARED | overclaims | 6.4 |
| A20 | "Competitive latency" is not a property a language or its backends can have. What is achievable is a tick that fits a declared period on a named host, and an after-the-fact replay | DECLARED | overclaims (the premise, in part a category error) | 1 |
| A6 | Locating a divergence the arbiter's way is infeasible at session length. At K = 1,000: 3,001 trace lines (339 KB) a tick, the C fast path 3.03 times slower with its trace on, and 161 bytes of Python memory a line held. Ten minutes at 60 ticks a second is 12.2 GB a trace and 17.4 GB held for each of two | MEASURED; DERIVED | costs more than stated | 2.3 |
| A7 | On the K-bodies law, the event chain is 95–98% of a compiled tick. A fast path that keeps the chain is not fast, and one that drops it has no heads to compare | MEASURED | costs more than stated | 2.3, 5.1 |
| A8 | The reference, the only reconciler independent of the lowering, runs a K = 1,000 tick in a median of 11.9 ms falling and 14.7 ms landed. Every landed tick exceeds the lineage's 1/120 s, so a ten-minute match's verdict comes 7.6 minutes after it | MEASURED; DERIVED | costs more than stated | 2.2 |
| A9 | A refusal reachable from a port ends the match on every execution, at the same event. Nothing on the sheet refuses a hostile input record at the door, as Verðandi's input contract does | MEASURED (v0 stand-ins); ESTABLISHED | costs more than stated; missing from the sheet | 2.4 |
| A13 | Per-pixel visual work in the law costs about 10^3 ticks' budgets a frame. On the judge's measurement, a 1080p frame of bands 0–2 per pixel is 9.9 s of C and 220 s of the reference | DERIVED | costs more than stated | 4.3 |
| A17 | The skeptic's body ceilings (about 19,000 in C, 1,300 in the reference) were measured while every body was still falling. Landed, the same law costs 1.8 times as much a tick in C and 1.23 times in the reference | MEASURED | costs more than stated | 6.2 |
| A18 | Slopes hide tails. In-process, a K = 1,000 tick's maximum was 2.4–3.3 times its median, and a K = 100 tick's 13–20 times. The spread between sittings was 3% in this session and 24% in the first attempt's, so one session's spread is no margin for another | MEASURED | costs more than stated | 6.3 |
| A22 | A view must be given only what its player may see, or any renderer artifact leaks what A10 leaks. Ørlǫg has one output stream for every observer, and RUN-1 has no per-player output | DECLARED | costs more than stated (a missing piece) | 3.5 |
| A21 | Reconciling a played session adds integrity and never grounding (R6 a). "Admitted" or "verified" would say more than "replayed four ways over log <seal>, unratified" | ESTABLISHED (the sheet) | only words, until a document says more | 2.1 |

---

## 1. The target: what in the request is achievable, and what is a category error

The owner asked (PROPOSAL.md, verbatim): *"something like a speed reconciler or language swap for competitive latency
and graphics ie compatible with shaders and spherical harmonics or other high requiring methods"* and *"reference
verdani speed records for competitive headroom standards"*.

**Achievable, in the lineage's terms:**
- A tick whose compute fits a declared period on a named host. This is a software timing of one component, per tick,
  with its tail, in a preregistered apparatus (§6.4).
- Deterministic replay of a recorded session four ways (RUN-1's replay theorem; DECLARED until 1b).
- A budget in counted operations that refuses deterministically (R9 b). It refuses operations, not time (§6.2).
- A view that reads each tick's output and writes no program state (§3).
- After-the-fact adjudication: a dispute about a recorded match settled by replay. This is the competitive use a
  verification language can serve without overclaiming.

**Category errors:**
1. **Latency as a property of the language.** Latency in play is end to end: input sampling, the host's assignment of
   inputs to ticks, the network, the tick, the render, the present and the panel. Verðandi measured only pieces of it
   and makes "no low-latency, competitive or input-to-photon claim" (its `docs/GHOSTS.md`, G7). Its live loop "has no
   latency, frame-rate or feel number" (G21). Ørlǫg has no input device, display or network path at all. Grade:
   DECLARED.
2. **A language swap for speed.** On a game-like law the commitment, not the language, is the cost: 95–98% of a
   compiled tick is the event chain (A7). A faster language for the rest buys at most a few percent (§5.1).
3. **Shaders and spherical harmonics inside what the receipts certify.** GPU floats have no fixed reduction order
   (A15), and the lineage's own shader calls a GLSL built-in outside the range in which, as recalled, the
   specification defines it (§5.2). A per-pixel frame in the law costs about 10^3 ticks' budgets (A13). Graphics can
   be *compatible* with the law as a consumer of its outputs, not as part of its receipts.
4. **Verðandi's speed records as a competitive standard.** The records refuse the competitive claim (G7). They measure
   a modelled loop the shipped shell does not run (G12). They do not carry across runs (G13: 40–60% slower the same day)
   or apparatus (G4: one emit read 4,734, 7,734 or 5,019 µs by harness). Their labels flipped on three samples (G10).
   What carries is the method (§6.4), not a number.

**Lockstep, prediction and rollback.** "Competitive" across machines also means networked play, which RUN-1 leaves
undecided ("What this sheet does not decide: … Distribution: networked play"). Ørlǫg's determinism suits lockstep.
That needs byte-identical receipts across hosts, which is NOT_MEASURED (DOCTRINE T5: "Any other host (NOT_MEASURED)").
A lockstep game's input delay is a network round trip. The usual way to hide it is prediction and rollback, which run
the law on guessed inputs and discard the result (DECLARED: general practice, nothing here measures it). There,
divergence from the authoritative run is the normal case, not a defect. RUN-1's single branch and R4 a have no place
for it, and snapshots (SNAP-1) are not built.
- Rolling back 8 ticks at K = 1,000 re-executes 8 ticks: 11.4 ms of C with the chain, against a 1/120 s period
  (DERIVED from §6.3's in-process median, 1.43 ms).
- Without the chain it is about 0.5 ms (DERIVED from §2.3's ablation, a different apparatus).
- So at this size a predicting path can roll back 8 ticks within the period only without the chain, and then it
  commits nothing.

Grade: DERIVED. Severity: costs more than stated.

---

## 2. The two-speed design

The design under attack: play runs on one resident compiled execution that records the input log, and the reference
and the other backends replay the log behind it, for admission (SKEPTIC.md, "two speeds"). DOCTRINE §11 records the
owner's caveats in the same direction: "four-way checking belongs at admission, and a live loop runs one backend".
The question is what this design can and cannot claim.

### 2.1 What a reconciler behind play cannot protect

- **Outcomes decided in real time (A4).** A hit, a score or the end of a match is decided by the fast path and shown
  to players before any reconciler runs. If the reconciler later dissents, the arbiter has already said whose record
  stands. Its localization note reads "the reference's bytes are kept (declared authority); this backend's run is
  quarantined" (`src/orlog/arbiter.py`, `localize`). In two-speed play the quarantined run is the match the players
  played, and the record that stands is a game nobody saw. There is no third option. Either the reference is the
  authority, and a live outcome is provisional until reconciled, or the fast path's record stands, and the reference
  is not the authority. Grade: ESTABLISHED (the code). Severity: breaks a guarantee, if any document calls a live
  outcome final, verified or admitted. Falsifier: a design in which a live outcome and a later REFERENCE-DISSENT
  over the same log can both stand.
- **A refusal mid-match.** R4 a (recommended) makes a refusal end the branch, and the fast path must refuse where the
  reference refuses or it diverges. So a refusal, whether hostile or a defect's, ends the live match at once (§2.4).
- **Trust in the log (A5).** The input log is written by the fast path's host. The reconciler checks the law's
  computation over that log, never the log's fidelity to what players did. DOCTRINE T12, limit 4: an input event "is
  still a value in a log chosen by whoever ran it: that gives replayable observations, not admissible ones".
  - In competitive play the decisive part of the log is the tick each input lands in: who fired first, who peeked.
    That assignment is made by the host's clock, which no runtime reads (RUNTIME-SPEC §1; RUN-1 D7 keeps clocks out
    of v1).
  - A host that writes the log before it consumes it agrees with its replay by construction, whatever the players
    pressed.
  - Grade: DECLARED. Severity: overclaims, if "replayed four ways" is read as "the match was fair".
- **Grounding (A21).** Under R6 a no claim in a run with an input log is GROUNDED outside the PREFIX licence.
  Reconciling a played session therefore adds integrity and never truth. "Admission" of a session should say "replayed
  four ways over log <seal>, unratified" and nothing more. Grade: ESTABLISHED (the sheet). Severity: only words, until
  a document says more.

### 2.2 Who reconciles, and how far behind

- **The compiled backends share the fast path's lowering (A2).** The self-test's lowering plant (one operation counted
  too many at every multiplication) was run on a 200-tick law with a claim, through the arbiter, with all three
  compiled backends (`work/speed-adv/chain_blind.py`, `chain_blind.txt`).
  - Result: REFERENCE-DISSENT. python, c99 and rust agree with each other at 2,406 operations against the reference's
    1,806.
  - Their events, trace head (`cb5b2d59…`) and output equal the reference's. For each backend the arbiter's
    localization reads "traces equal; the difference is outside the event chain".
  - So a reconciler made of the other compiled backends, the cheap ones, agrees with a compiled fast path that shares
    their defect. Only the reference sees it, as T11 says, and its dissent has no event to point at.
  - Grade: MEASURED. Does not show: other defect classes, or that the lowering has such a defect today. Falsifier: the
    same plant caught by python, c99 and rust against a compiled fast path.
- **The reference cannot keep pace (A8).** The lineage's own tick is 1/120 s (8.33 ms; Verðandi
  `docs/BOUNDARIES.md`, "simulation"). `ref_lag.py` stamps every tick of the reference's run in process, three runs
  each.
  - K = 1,000: a falling tick takes a median of 11.9–12.0 ms and a landed tick 14.7 ms (p99 17.0–17.2, max 17.2–18.8).
    Every landed tick, 99 of 99 in each run, exceeds the period.
  - K = 100: a landed tick takes 1.44–1.45 ms, and none exceeds the period.
  - DERIVED: at K = 1,000 a ten-minute match at 120 ticks a second (72,000 ticks) takes the reference 17.6 minutes to
    replay, so its verdict comes 7.6 minutes after the match.
  - The compiled fast path runs the same landed tick in 1.43 ms (§6.3), about a tenth of the reference's.
  - The stamps added under 3% to a whole run.
  - Why stamps, not slopes. A first version took slopes between whole runs (median of 3) and read a landed K = 100
    tick at 0.79 ms against 1.49 ms falling, which the law's work cannot explain. OBSERVED once; its output was
    overwritten by the stamped version. A rerun with five runs at each of five bounds (`ref_slopes.txt`) agrees with
    the stamps: at K = 1,000, 12.0–12.3 ms falling and 14.5–14.8 ms landed. Stamping every tick removes the
    dependence on which runs happened to be quiet.

  Grade: MEASURED; the lag DERIVED. Does not show: other laws, sizes or hosts. Severity: costs more than stated. Above
  some size the only reconciler that sees lowering defects (A2) cannot finish before the match does.
- **Verðandi has paid for this already.** Its live loop recomputes one free-heading frame in 64 off the loop, and
  "a fast-path defect that struck only unsampled frames would be caught at the save and not while the run was live"
  (G15). Its shell replays the session with a second copy of the workshop's fold, and the two are held together at
  the save (G17). The lineage's two-speed design catches at the end, not during play.

### 2.3 Can RUN-1's formats name the first tick where two executions part?

Q1 asks what RUN-1 must commit per tick. The sheet commits the trace head at each `'T'` event (R5) and an output
chain whose per-tick values reach only the final receipt. Three things fail.

**(a) The heads are blind to state outside the chain (A1, A3).** RUNTIME-SPEC §5's events carry assignments, items,
pushes and pops, output, the results of claims and musts, and refusals. The receipt also holds `ops`, each claim's
cost and each certificate's reference cost (§7), and no event commits them. With R9 b, `ops` decides an event:
TICK-BUDGET.

`chain_blind.py` part B emulates RUN-1 in the reference: a `'T'` boundary (the tick counter's own `'A'` event), a
per-tick budget checked at each statement's entry, and the same counting defect. It is an emulation, since nothing on
the sheet is built.
- Without a budget the two runs' events are identical, all 300 per-tick heads equal, and the operation counters part
  in tick 1 (27 against 32 operations).
- With a budget equal to the clean run's largest tick (2,717), the planted run refuses TICK-BUDGET in tick 246. Its
  heads equal the clean run's through tick 246, and the first differing boundary is the start of tick 247. A
  reconciler reading per-tick heads names tick 246; the executions parted in tick 1.
- Part C commits `(head, ops)` at each boundary instead, and names tick 1.
- With a budget above both runs (3,321), both complete, their traces are equal, and the receipts differ in `ops`
  (411,760 against 502,960) and in the claim's cost (900 against 1,200). No event, tick or head says where.

A3 follows. The ops count is computed by the lowering, which every compiled execution shares, so under R9 b a
counting defect moves the end of a live match identically on every compiled execution. R9 promises TICK-BUDGET "at the
same operation on every execution", and the compiled executions keep that promise among themselves while breaking it
against the reference. Only the reference sees it, and it cannot keep pace (A8). Grade: MEASURED (an emulation of
RUN-1's boundary and budget); A3's consequence DECLARED. Severity: breaks a guarantee, the one Q1 asks for. R12's
plant, "a dropped 'N' event, located at its first divergent event", tests events only and would pass. Falsifier: a
RUN-1 build whose per-tick commitments localize a planted operation-count defect to the tick where the counts part.

**(b) Locating by the trace as specified does not scale (A6).** The arbiter's `localize` reads both traces whole into
lists of text lines and walks them (`arbiter.py`). Measured on the K-bodies law at K = 1,000 (`trace_cost.py`; the C
backend; ticks 11–40, the falling regime):
- 3,001 lines and 338,772 bytes a tick (113 bytes a line);
- the C fast path takes 0.813 ms a tick without its trace and 2.464 ms with it (3.03 times);
- 161 bytes of Python memory a line held, as the arbiter holds it, and 62 ns a line to walk two equal traces.

DERIVED for ten minutes at 60 ticks a second (36,000 ticks), falling regime: 1.08e8 events, 12.2 GB a trace, and
17.4 GB of Python memory for each of the two the arbiter holds. The landed regime has 5,001 events a tick, so these
grow by two thirds. A per-tick list of 32-byte heads is 1.15 MB. Grade: MEASURED and DERIVED. Severity: costs more
than stated.

**(c) A head needs the chain, and the chain is the fast path's cost (A7).** `hash_share.py` builds the K-bodies law
twice through the arbiter's own build path: once as built, and once with the SHA-256 compression replaced by one XOR
(that receipt is wrong by construction; only its time is read).

| K | regime (ticks) | events a tick | as built | compression removed | the chain's share |
|---|---|---|---|---|---|
| 1,000 | falling (11–80) | 3,001 | 675.7 µs | 12.8 µs | 98% |
| 1,000 | landed (101–400) | 5,001 | 1,463.7 µs | 62.7 µs | 96% |
| 100 | landed (101–2,000) | 501 | 144.9 µs | 7.1 µs | 95% |

The K = 100 falling window (ticks 11–80) read 51%, but it is 70 ticks of about 60 µs, under the jitter of starting a
process, and is not used. The judge's spherical-harmonic law measured about 91% (`work/speed/JUDGE-MEASUREMENTS.md`
§3). So the two-speed fast path faces a dilemma:
- if it keeps the chain, so that it has heads to compare, it is 20 to 50 times slower than its own arithmetic;
- if it drops the chain, it commits nothing per tick but its outputs, and a divergence in state that never reaches
  the output is found only when it does, or never.

Grade: MEASURED (this law; the share depends on events per operation). Severity: costs more than stated.

**What the sheet would need, so that a reconciler can name the first tick where two executions part:**
1. `ops` committed at every `'T'`, for example in its payload beside the tick number. Each claim's cost should go into
   `'C'`'s payload, or a per-tick digest of the claim accumulators and certificate counters into `'T'`. This is a new
   trace version, `orlog-trace-1`, which RUN-1 introduces anyway.
2. A tick ledger as an output of every execution: per tick the head, `ops` and `out_t`, about 72 bytes, in place of a
   full trace. The arbiter's localization then becomes: compare ledgers, then replay only the first divergent tick
   with its trace on. That needs SNAP-1's snapshots, or a replay from the start that costs O(t).
3. A rule written down for what a live session's outcome is when a later reconciliation dissents (A4).
4. If the fast path drops the chain, a statement of which divergences become unlocatable: everything not in the
   output.

### 2.4 Refusals in a live match, and the missing input contract (A9)

Version 0 takes no input, so a literal stands in for a port value, as `research/run-1/r6_indirect.py` does
(`refusal_ends_match.py`, all four executions through the arbiter):
- a body pushed by a thrust of 2,000,000 for 7,200 ticks refuses OVERFLOW at tick 5,932;
- a speed claimed in the tick block (D8: evaluated each tick) is refuted at tick 1 when the client asks for 12.5;
- in both, python, c99 and rust agree with the reference.

Determinism of failure is what verification wants. In a match it is a switch that any client able to drive the law
into a refusal holds, because Fix refuses overflow rather than saturating (DOCTRINE §11) and R4 a ends the branch.

Verðandi's graybox has the missing piece. Its input "is admitted or refused whole before the tick touches anything …
a refused record changes nothing and its category is returned" (its `docs/BOUNDARIES.md`, "simulation"). RUN-1 has no
range or admission rule for a port. R3 settles rounding and R10 the signature, so a hostile value is admitted and
ends the match inside the law. Grade: MEASURED (stand-ins), ESTABLISHED (the sheet). Severity: costs more than
stated; missing from the sheet. Falsifier: a RUN-1 port declaration that refuses an out-of-range record at the door
without ending the run.

Also missing for live play: RUN-1's run model ends when its log ends (D3), and the generated programs run from `main`
to `finish`. A resident fast path needs a log that grows while it runs. That is SESSION-0's territory and not on the
sheet. ESTABLISHED.

---

## 3. The view tier

### 3.1 What the lineage's view rule covers

The owner's rule, as Verðandi's `docs/BOUNDARIES.md` keeps it: *"The renderer can add bolts, trim, decals, surface
detail, particles, lighting, and decorative meshes. It must not silently decide where walls, cover, or
player-blocking objects exist. If visual decoration is intended to affect gameplay, that change must be represented
in the authoritative world and checked."*

- **What it covers:** where things that block exist. Its checks hold geometry: `render-conforms` (the lit mesh against
  C face by face), and `art/check.py` (no dressing where a player can be; decoration flush, inside rock, or above the
  reach ceiling).
- **What it does not cover:** what a player can see. Lighting is on its list of permitted decorations. Fog, darkness,
  bloom, reflections and the field of view decide visibility without blocking anything.
- **What it cannot check:** its last sentence turns on *intended*, and intent is not in the text (AGENTS.md: Ørlǫg
  "cannot compute whether a condition says what its author meant"). Verðandi's renderer is judged by a person and
  hashed by nothing (`art/README.md`). The renderer conformance plants "were refused once, in the build container;
  nothing in the tree re-runs them" (BOUNDARIES.md).

Grade: ESTABLISHED (read). Severity: overclaims, wherever "decorates, never decides" is read as "cannot affect play".

### 3.2 Measured: the native renderer shows a target hidden behind a wall (A10)

`work/speed-adv/webleak/` builds a synthetic scene in the renderer's own schema, with plaza-night's air and materials
(`art/briefs/plaza-night.art`: fog 0.045, rain 0.8, floor_wet roughness 0.16, concrete walls):
- one wall, one cell (2 m) thick and 4 m high, across the view;
- a target of the graybox's size (0.8 × 0.8 × 1.9 m, `graybox/web/sim.js`) one metre behind it;
- the eye at 1.62 m (sim.js), looking at the wall, on a 1920 × 1080 canvas.

The line from the eye to the target's top stays below 1.9 m and the wall is 4 m high, so the target is wholly hidden.
Each case renders the same frame (the same time, so the same rain) with and without the target, and counts the
differing pixels of the final image. Results are posted by the page itself to `webleak/results/*.txt`; the server is
`webleak/serve.py`.
- **Controls.** The frame rendered twice without the target: 0 differing pixels in each of 5 pairs. In an earlier
  version of the page, the one pair that included the renderer's construction differed in 5 scattered pixels by 1
  level. The target in plain view with no wall: 4,942 pixels, by up to 55.
- **The renderer as Verðandi ships it** (`index.txt`), pixels that differ and the largest difference in any channel:

| wall at | plaza air, a lamp behind the wall | plaza air, no lamp | dry floor, roughness 0.43 |
|---|---|---|---|
| 6 m | 456 px, 19 | 457 px, 19 | 1,076 px, 2 |
| 10 m | 304 px, 30 | 303 px, 29 | 695 px, 3 |
| 14 m | 133 px, 16 | 134 px, 16 | 421 px, 3 |
| 20 m | 104 px, 24 | 108 px, 24 | 291 px, 2 |
| 26 m | 110 px, 15 | 106 px, 15 | 210 px, 1 |
| 30 m | 111 px, 17 | 110 px, 17 | 495 px, 1 |
| 40 m | 76 px, 9 | 76 px, 9 | 162 px, 1 |

  Every differing pixel lies at or below the row where the floor meets the wall. They form a band of 5 to 21 rows
  across the target's columns. At 20 m, across eight times of the rain, the count is 106–109 and the largest
  difference 22–27. Two earlier runs of the same page gave the same count and largest difference in every cell.
- **Ablation 1** (`ablate.txt`): the mirror pass's discard moved from 0.02 m to 0.0001 m. The leak stays at every
  distance, smaller (at 20 m: 103 px, largest 10).
- **Ablation 2** (`ablate2.txt`): that change, and the mirror pass drawn without face culling. Every wet case reads 0
  pixels at every distance. The dry rough floor keeps 140 and 98 pixels, at 1 level, at 20 m and 26 m.

**The mechanism, from the code and the ablations.** Pass 1 renders the scene reflected in the floor's plane into a
half-size, mipmapped texture. It discards everything below 2 cm (`wP.y < 0.02`), which takes away the reflected
wall's footing and lowest 2 cm, and it culls front faces, which drops the reflected wall's back face. So in the rows
where the wall stands, the texture holds the reflected scene behind the wall. Pass 2's floor samples the texture at
its own position, bilinearly, at a level of detail set by roughness, with the rain's rings offsetting it by up to 4.5
rows (`view_geometry.py` B). At the wall's foot that sample brings the hidden target in.

`view_geometry.py` C models the column both ways. The first attempt modelled a closed reflected wall and predicted no
leak at 6–14 m; the render refutes that model. Modelling the wall as pass 1 draws it predicts a leak at every
distance, as measured.

- **Grade:** MEASURED, on one browser engine and one GPU on this host, in a synthetic scene in the renderer's schema.
- **Does not show:**
  - that a person would notice it (NOT_MEASURED: no person looked);
  - that it occurs in plaza-night's own geometry, or on another GPU or browser;
  - that any Verðandi player was ever affected.
- **Severity:** overclaims. The renderer writes no game state, exactly as its contract says. What it does decide is
  what a player can learn of hidden state. In a competitive game that is a wallhack its author never intended, and
  nothing in the tree hashes or checks the picture that carries it.
- **Falsifier:** `webleak/index.html` on another platform, reading 0 differing pixels beyond the control's noise at
  every distance. Or a check in Verðandi's tree that refuses such a scene; none was found.

### 3.3 Other visibility the view decides (A11)

All from `view_geometry.py`, arithmetic on the renderer's code (ESTABLISHED):
- **Field of view by canvas shape.** `persp(fov, w / h, …)` fixes the vertical angle at 66°, so the horizontal one is
  81.8° at 4:3, 98.2° at 16:9, 113.2° at 21:9 and 133.2° at 32:9. A wider window sees players a narrower one cannot.
- **Fog.** FS_SCENE's height fog, with uFogD = 0.55 × density, leaves a target's own colour at 0.488 at 30 m under
  plaza-night's fog (0.045). Twice that density leaves 0.238, and half of it 0.698. The fog is an art statement, and
  an intent may change it (Verðandi `art/director/README.md`, statement keys). The art checks hold geometry, so how far
  players can see is set by the art file, which a model may write.
- **Resolution.** At 1080 rows a 0.8 m target spans one row at 665 m. The law's line of sight and the screen's
  visibility differ, and neither is what the player saw.

### 3.4 How a view reads each tick and never writes back, and why that is not enough

- **The only channel out is `Say`.** Lines of exact decimal text, each also an `'S'` event folded into the chain and
  the output hash. At K = 1,000, saying every body's height every tick cost 1.29 times the quiet tick, and one list
  line 1.11 times, with about 15–16 KB of text a tick (`view_cost.py`, the C backend, one run, ratios within it). So
  the law pays to commit what the view only decorates. Grade: MEASURED. Severity: costs more than stated (small).
- **The player is the channel back.** The view's picture reaches a person, whose next input is recorded in the log
  and decides the next outcome. The program never writes back, but the system does, through the player. Receipts and
  replay are exact about a game whose inputs were shaped by the view, and cannot say the view was fair. Grade:
  DECLARED. Severity: overclaims, if "never writes back" is offered as a fairness property.

### 3.5 What graphical, if anything, must be computed in the law

Whatever decides an outcome or what a player may know:
- line of sight for gameplay (spotting, AI perception, fog of war);
- above all, the set of entities each player's view is given.

A view cannot leak what it never received (A22). The renderer of A10 leaks a hidden target only because the view has
the target at all, and the usual remedy is to send each client only what its line of sight admits. Ørlǫg's output is
one stream for every observer, and RUN-1 has no per-player output. That is a missing piece for any competitive use,
and it sits under the distribution RUN-1 does not decide. Shading, spherical harmonics and post-processing do not
belong in the law unless a light level decides an outcome, as in stealth (§4.3 prices it). Grade: DECLARED. Severity:
costs more than stated (a missing piece).

---

## 4. Floats and fixed point

R8 b defers float ports. That is not in tension with float shaders, as long as nothing returns from the view except as
a recorded input. An aim computed in floats by a client and sent as a Fix is rounded once and noted (R3 b). The
pressure is the other way: anything graphical the law must compute, it computes in Fix.

### 4.1 The precision of spherical harmonics in Q31.32 depends on the input's scale (A12)

The judge measured bands 0–2 in Fix at integer lattice directions, worst 1.23 units of 2^-32
(`work/speed/JUDGE-MEASUREMENTS.md` §1). Those directions start from vectors of length at least 1. Q31.32 has one
absolute step at every magnitude, so a direction made from a short vector loses relative precision before the basis
is evaluated, and a long one overflows when squared.

`sh_fix.py` does what a law would do, with numeric_ref: |v|^2 by x_mul and x_add, x_sqrt, the components by x_div, and
the nine functions with the constants as Fix literals. It compares against binary64 at the direction of the very Fix
vector given. Over 2,000 random directions per length:

| length | worst error | refused |
|---|---|---|
| 1 m | 6.6e-10 (3 units) | 0 |
| 2^-4 m | 6.4e-8 | 0 |
| 2^-8 m | 1.45e-5 | 0 |
| 2^-12 m | 3.7e-3 | 0 |
| 2^-15 m | 0.276 | 0 |
| 2^-16 m | — | 235 DIVISION-BY-ZERO |
| 2^-17 m | — | all |
| 2^15 m | 4.3e-10 | 0 |
| 2^15.5 m | — | 1,072 OVERFLOW |
| 2^16 m | — | all |

A triangle's unit normal by a cross product refuses 14 of 2,000 at 1 cm edges and all at 3 mm.

A direction taken from one tick's displacement of a slow body is such a short vector: 1 mm/s at 120 ticks a second is
8.3e-6 m a tick, about 2^-17. Under R4 a, a refusal there ends the session unless the law guards it.

Grade: MEASURED, deterministic: rerun identical to attempt 1. Does not show: the error of any law that normalizes
first and then evaluates, which is the judge's case. Severity: overclaims, if 1.23 units is offered as Fix's precision
for SH in general. Falsifier: a law evaluating the basis from short difference vectors within 1e-6 of binary64.

### 4.2 Fix sums are order-independent; float32 sums are not

`sh_order.py` projects one seeded environment (4,096 samples) onto the nine coefficients four ways: a fold, a pairwise
tree, 64 strided lanes, and 32 blocks then a tree.
- **float32**, every operation rounded: 9 of 9 coefficients differ between the orders, by up to 23 ulp.
- **Q31.32**, with numeric_ref's x_mul and x_add: 0 of 9 differ.

This is a point *for* Fix: a fixed-point reduction is schedule-free, until a partial sum overflows (§5.2). Grade:
MEASURED.

### 4.3 What visual work in the law costs (A13)

DERIVED from the judge's MEASURED cost of bands 0–2 per direction (c99 4.78 µs, rust 5.31 µs, reference 106 µs; 0.44
µs with the chain's hashing removed):
- one tick of 1/120 s holds about 1,740 directions in C and about 79 in the reference;
- a 1080p frame, 2,073,600 pixels, would take 9.9 s of C (0.91 s without the chain) and 220 s of the reference.

So per-pixel or per-vertex graphics in the law is out by two to four orders of magnitude, while light probes counted
in hundreds are affordable in C and not, at 120 ticks a second, in the reference that must replay them.

---

## 5. A language swap, and a GPU backend

### 5.1 The language is not the cost (A7, A14)

On the K-bodies law the chain is 95–98% of a compiled tick (§2.3c). Replace everything else with an infinitely fast
implementation and the tick shrinks by 2–5%, and by about 9% on the judge's SH law (DERIVED, Amdahl). The fast
lever is the commitment: what is hashed per event, and how. RUNTIME-SPEC §1's constraints keep the hardware path to a
cheaper SHA-256 out of both compiled runtimes. C allows "only the standard library" and "no compiler extensions …
no `__builtin_*`"; Rust allows "standard library only, no crates, no `unsafe`". A cheaper commitment is therefore a new
trace version or a runtime-contract amendment, not a language swap. Any new execution is held to the same receipts:
the same `ops`, the same events in the same order, the same refusal at the same operation. Otherwise it is not an
execution of Ørlǫg and four-way agreement no longer covers it. Grade: MEASURED, ESTABLISHED and DERIVED. Severity:
overclaims (the premise of a speed-giving swap).

### 5.2 Could a GPU backend be authoritative? (A15)

- **The chain is serial by definition.** RUNTIME-SPEC §5 defines `head = SHA-256(head || event)`, and it is most of
  the work (A7). A GPU computes the arithmetic in parallel and then hashes 3,001–5,001 events a tick (K = 1,000) on
  one lane. ESTABLISHED.
- **No 64-bit integers.** As recalled and not re-read here (NOT_MEASURED in this session), GLSL ES 3.00, which WebGL 2
  uses, and WGSL have no 64-bit integer type, and Q31.32's x_mul needs a 128-bit product of two int64 raws. The first
  attempt's extraction of the GLSL ES text failed (`work/speed-adv/spec/` holds empty pages) and is not relied on.
  `gpu_mul.py` emulates x_mul with 32-bit operations (16-bit limbs). It matches numeric_ref on 200,324 pairs, with 0
  mismatches and 20,855 OVERFLOW refusals reproduced, at 153–159 32-bit operations a multiply in this emulation, not a
  proven minimum. MEASURED.
- **Order is meaning** (`order_refusal.py`, numeric_ref):
  - checked Int sums of 8 terms, as a left fold against a pairwise tree: the refusal moves on 1,998 of 20,000;
  - Fix products: (a·b)·c ≠ a·(b·c) for 77.7% of triples in [−8, 8) and 18.3% in [−1, 1), by up to 7 units;
  - Fix sums are exact, but [max−1, 1, 1, −1] refuses as a fold and completes as a tree.

  A GPU backend must therefore follow the text's order for every product and every refusal. That is serial
  semantics on a parallel machine. MEASURED.
- **Floats.** float32 reductions move with the schedule (§4.2). The lineage's own shader calls `smoothstep(0.1, 0.0,
  x)`, `smoothstep(0.08, 0.0, x)` and `smoothstep(1.0, 0.92, x)`, with edge0 > edge1. As recalled and not re-read,
  GLSL specifications leave that case undefined. A picture from such code is not a candidate for any receipt.
  ESTABLISHED (the calls are in FS_SCENE). The specification's wording is NOT_MEASURED here, and what this browser
  computes for those calls was not isolated.
- **Authority is declared, not voted** (AGENTS.md §1). A GPU "authority" would replace the reference and relocate
  trust (T11). At most a GPU can be a fifth witness for an integer subset, held to the same receipts.

Severity: overclaims, if the debate concludes that a GPU backend could be authoritative.

---

## 6. Headroom standards

### 6.1 What Verðandi's records say about their own numbers

| record | what it says |
|---|---|
| G4 | cross-apparatus numbers are not comparable; "cite the *ratio within a run*, never the absolute across runs" |
| G5 | every number is one host and one corpus |
| G10 | p99 of 200 samples is the third-largest; a label flipped on three samples; a zero-margin boundary flipped on 2 vs 24 µs |
| G12 | the render-loop courts measure a loop the shipped shell does not run |
| G13 | the same court ran 40–60% slower the same day; the cause UNDERDETERMINED |
| G21 | the live loop has no latency, frame-rate or feel number |

Its brief forbids claiming a latency, a frame rate, input-to-photon or feel. A standard that takes Verðandi's numbers
as headroom imports what those ghosts disclaim. ESTABLISHED.

### 6.2 Counted operations are not time (A16, A17)

- **One counted operation can take a third of a second.** `one_op.py`: `Set b to a`, with a a list of 2^24 Fix (the
  language's largest), counts 2 operations a tick and takes 352 ms of C a tick, 42 periods of 1/120 s.
  `ops_not_time.py`: one counted operation of a 2^20-item copy costs 1.04e5 times one of an addition in C, and 4.34e3
  times in the reference. Each item is hashed into the `'A'` event, and the operation count sees one statement.
- **On the skeptic's own law, the first 90 ticks are the cheap ones.** `tick_tail.py` stamps every tick of the C
  program in-process. In all six runs the tick time steps up at tick 91: 0.082 → 0.147 ms at K = 100, and 0.80 →
  1.43 ms at K = 1,000. The receipts say why: the bodies land at tick 91, the If's branch runs every tick after, and
  a tick goes from 13,002 operations and 3,001 events to 15,002 and 5,001 (K = 1,000). Operations grow 15%, events 67%
  and time 80%.
- **R9 b refuses operations, not time.** The sheet is honest about this ("counted, not timed"). The reading is not,
  if it is "never an overrun" in time: the owner's measure, as the sheet quotes it, is "a tick that exceeds its budget
  produces a signed refusal event, never an overrun". A tick within any operation budget can overrun its period.
- **The skeptic's ceilings come from the cheap regime.** The skeptic's K-bodies table (`work/arch-redteam/tick.txt`)
  measured K = 1,000 over ticks 20–60 and K = 10,000 over ticks 4–12, all falling, and K = 100 over ticks 120–360,
  landed. Its rows are not like for like, and its ceilings of about 19,000 bodies in C and 1,300 in the reference are
  for a world in which nothing has landed. Landed, the same law costs 1.8 times as much a tick in C (in-process
  stamps, §6.3) and 1.23 times in the reference (§2.2), whose cost follows operations more than events (A17).

Grade: MEASURED. Severity: overclaims (the budget as a guard against time overruns); costs more than stated (the
ceilings). Falsifier: a per-tick budget in counted operations under which every tick of these two laws fits its
period on this host.

### 6.3 Slopes hide tails, and the per-tick figure drifts (A18)

`tick_tail.py`, three runs per configuration, every tick timed by QueryPerformanceCounter (step 0.1 µs) in the
compiled program itself. Receipts equal the uninstrumented build's. Landed regime (ms):

| K, run | p50 | p90 | p99 | p99.9 | max | ticks over 2 × p50 |
|---|---|---|---|---|---|---|
| 1,000, 1 | 1.435 | 1.472 | 1.958 | 2.750 | 4.684 | 3 of 2,999 |
| 1,000, 2 | 1.432 | 1.452 | 1.605 | 2.624 | 4.199 | 1 of 2,999 |
| 1,000, 3 | 1.435 | 1.458 | 1.781 | 2.688 | 3.489 | 2 of 2,999 |
| 100, 1 | 0.147 | 0.149 | 0.185 | 0.358 | 2.004 | 43 of 29,999 |
| 100, 2 | 0.147 | 0.149 | 0.173 | 0.376 | 1.890 | 46 of 29,999 |
| 100, 3 | 0.147 | 0.149 | 0.176 | 0.402 | 2.920 | 64 of 29,999 |

The maximum is 2.4–3.3 times the median at K = 1,000 and 13–20 times at K = 100. No tick here exceeded 1/120 s, so
this law at these sizes fits that period on this host, in these runs. That is the strongest statement these numbers
allow, and it is a software timing of one component.

**The same figure in eight sittings** (`drift.py`: the per-tick slope of the landed regime between T = 100 and 300,
median of 7 runs, sittings about 50 s apart, with the same law at K = 100 as the same-run comparator):
- the C tick at K = 1,000 read 1.460–1.498 ms (max/min 1.03);
- the ratio to K = 100 read 9.74–10.27 (max/min 1.05).

The first attempt's sittings, earlier the same day on a window that straddled tick 91, spread 1.232–1.533 ms
(max/min 1.24), and their ratio 7.64–9.17 (max/min 1.20). The windows differ, so this is not a drift measurement
between the two sessions. What it does show is that the spread one session sees is no margin for another's. A margin
must be measured beside each run, as G13 found. The cause is NOT_MEASURED: no host state was recorded.

Grade: MEASURED. Does not show: any other host, law or build; a frame; anything a person perceives. Severity: costs
more than stated, for any headroom figure taken from slopes or from one session.

### 6.4 What a falsifiable headroom standard would need, and what it can never say (A19)

A "headroom standard" stated as one number ("the tick uses X% of its budget") is a scalar scorecard, which the lineage
forbids. Q4's sketch — sample size, a declared margin, a same-run comparator, the clock's step and a named host — is
the right start. On the measurements above, it also needs:
1. **The observable named exactly.** "The C fast path's per-tick compute of law L, from the tick's first event to the
   next tick's, stamped in-process", not a slope of process times. The slope hides both regimes (A17) and tails (A18).
2. **The regime named.** Which ticks, in which state of the law. Better, every tick of a recorded session, so that no
   regime is chosen.
3. **Counts beyond thresholds, beside the quantiles.** "Ticks over 50% of the period: 0 of 9,000" is falsifiable by one
   tick. A p99.9 over 3,000 ticks is the third-largest sample, as G10 found for a p99 over 200.
4. **A same-run, interleaved comparator in the same regime.** Here the drift fixture uses the same law at K = 100,
   whose ratio itself moved between sittings (9.74–10.27 in this session, 7.64–9.17 in the first attempt's).
5. **A margin declared before the number, wider than the drift measured on that host** (G13: 40–60%; §6.3 here).
6. **The host's state beside every run** (Verðandi's HOST-STATE-0 and HOST-STATE-1), recorded and never read by the
   rule.
7. **The clock's step**, reported, and far under the quantity timed (0.1 µs here against ticks of 0.08–4.7 ms).
8. **What it does not show, in the registration:** anything past the tick's compute (input sampling, the host's tick
   assignment, the network, the render, the present, the panel), any other host, law, size, regime or build, and
   anything about competitiveness, which has no same-apparatus comparator in this repository.

Grade: DECLARED (a method). Severity: overclaims, for any version that publishes a single headroom figure or calls
the result competitive.

---

## 7. What the round-1 designs will be asked to survive

Each likely proposal, the finding that tests it, and the falsifier it must face:

| likely proposal | tested by | its falsifier |
|---|---|---|
| a tick ledger of heads and out_t | A1, A3, A7 | a planted operation-count defect localized to the tick where the counts part, by a fast path that keeps its speed |
| the fast path without the chain, the reconciler computing it | A7, A4, §2.3's list (item 4) | a divergence in unprinted state named within its tick |
| the other backends as the reconciler | A2, A8 | the lowering plant caught without the reference |
| a fixed-point or integer GPU backend | A15, A14 | byte-identical receipts from a GPU execution on the corpus, faster per tick than C |
| "the view decorates and never decides" | A10, A11 | `webleak/` reading 0 pixels on the shipped renderer; a view given only what its player may see |
| visual quantities in the law, in Fix | A12, A13 | a per-tick light-probe count with its precision bound at the vectors' real scales |
| a headroom standard | A16, A17, A18, A19 | §6.4's eight items, preregistered before any number |

---

## 8. The first attempt's fixtures: checked, rerun, corrected

The first attempt left fixtures in `work/speed-adv/`. Each was read before use and rerun against `tree/`. The
deterministic ones reproduced byte for byte below their header line: `order_refusal`, `gpu_mul`, `sh_fix` and
`refusal_ends_match`. Corrections:
1. **The view model was wrong in the direction that hid the leak.** It assumed the reflected wall is solid, and so
   predicted no leak at 5–10 m. The renderer's pass 1 draws the wall without its footing and back face. The render
   leaks at every distance, and the corrected model agrees (§3.2).
2. **Its rain offsets were overstated**, by about 2 and 5.5 times: 0.0084 and 0.0120 of the screen, against 0.00414
   and 0.00220 by a search of the ring formulas. Its target was 1.8 m high instead of sim.js's 1.9 m.
3. **"The per-tick cost is not one number" was the law, not the host.** `linearity.py` and `linearity2.py` found the
   slope near 0.5–0.9 ms in short runs and 1.5 ms in long ones, with CPU time following wall time. The cause is the
   law's own regime change at tick 91 (§6.2), not drift or the scheduler.
4. **`hash_share.py` said "events a tick 3001"** over a window mostly in the landed regime, which has 5,001. It now
   reads both regimes from the receipts.
5. **`chain_blind.py` part A ran one backend.** It now runs all three, which turns its BACKEND-DISSENT into the
   REFERENCE-DISSENT that A2 rests on.
6. **The extracted GLSL ES text in `spec/` is empty**, and nothing here relies on it.

---

## 9. Evidence

Every script is run from `work/speed-adv/` as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B <script>`, and writes the
`.txt` of the same name there.

| file | what it holds | grade |
|---|---|---|
| `chain_blind.txt` | the lowering plant through the arbiter, three backends (A2); RUN-1's per-tick heads and budget emulated (A1) | MEASURED |
| `trace_cost.txt` | trace size, tracing's cost, the arbiter's memory and walk; the reference's tick (A6, A8) | MEASURED; DERIVED |
| `hash_share.txt` | the chain's share of a compiled tick, by regime (A7) | MEASURED |
| `ref_lag.txt`, `ref_slopes.txt` | the reference's every tick stamped, by regime, against 1/120 s; the slopes beside them (A8, A17) | MEASURED; DERIVED |
| `tick_tail.txt` | every tick stamped in the C program; the regime step at tick 91 (A17, A18) | MEASURED |
| `drift.txt`, `drift.log` | the same per-tick slope in eight sittings (`python -B drift.py 8 45`), with a same-run comparator (A18) | MEASURED |
| `ops_not_time.txt`, `one_op.txt` | counted operations against time (A16) | MEASURED |
| `refusal_ends_match.txt` | refusals reachable from a stand-in port, four executions (A9) | MEASURED |
| `view_geometry.txt` | field of view, fog, the rain's offsets, the mirror's model (A11, §3.2) | ESTABLISHED (arithmetic); a model |
| `webleak/results/index.txt`, `ablate.txt`, `ablate2.txt` | the renderer's leak and its two ablations (A10); run by opening `webleak/index.html`, `ablate.html` and `ablate2.html` from `python -B webleak/serve.py 8766` | MEASURED |
| `view_cost.txt` | the cost of handing each tick to a view through `Say` (§3.4) | MEASURED |
| `sh_fix.txt`, `sh_order.txt` | Fix SH precision by scale; projection order in float32 and Q31.32 (A12, §4.2) | MEASURED |
| `gpu_mul.txt`, `order_refusal.txt` | Q31.32 multiply in 32-bit operations; order and refusal (A15) | MEASURED |
| `linearity.txt`, `linearity2.txt` | the slope by run length: the first attempt's run (`linearity.txt`, on a partial snapshot of the same commit), and `linearity2.py` rerun here; both explained in §8 | MEASURED, reinterpreted |
| `attempt1/` | the first attempt's outputs, kept for comparison | — |
