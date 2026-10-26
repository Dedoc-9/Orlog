# Verdict: a speed reconciler, no language swap, and a view that must not disclose (2026-10-26)

The judge's verdict on the owner's two requests of 2026-10-26 (PROPOSAL.md, verbatim):

> Also we will need something like a speed reconciler or language swap for competitive latency and graphics ie compatible with shaders and spherical harmonics or other high requiring methods

> reference verdani speed records for competitive headroom standards

It weighs four things, all saved beside this file:
- two rounds between a proponent, who designed and measured (PROPONENT.md, PROPONENT-R2.md), and an adversary, who
  prosecuted and measured (ADVERSARY.md, ADVERSARY-R2.md);
- a prior-art survey made with real searches, every source graded by how it was read (RESEARCH.md);
- the judge's own measurements (`judge/`) and reruns (`judge/reruns/`).

This verdict is model output, like the reports, and admits nothing. Every party ran on this host against a snapshot of
f16dc26, checked file by file; nothing touched Verðandi but reading. The debaters' scripts are in `work/` folders that
git ignores, so from this tree their figures are OBSERVED, except where the judge reran them (below). One model family
wrote every party: agreement among them is consistency, not truth (DOCTRINE T11; the survey's Knight and Leveson).

## The answer, short

1. **A speed reconciler: yes, as three tiers over one input log.**
   - **Play** is the law's own C program, resident, built without the per-event chain, and writing one line per tick.
   - **The watcher** is the reference, replaying the durable log behind play and writing the same line. It works in
     parallel segments where it cannot keep pace alone.
   - **Admission** runs the four executions with the full chain over the closed log, as today.

   The line is what RUN-1's formats lack. Two things are missing:
   - **the line's fields:** the operation count, a digest of the claims, a digest of the persistent state;
   - **a check on the bytes received:** the receiver recomputes the output chain over the bytes it was actually sent.

   Measured on stand-ins, the line names 13 of 13 planted defects at the tick they were planted in. RUN-1's per-tick
   commitments as written name 4. The adversary's shared-lowering defect under a per-tick budget is named at tick 1
   by the line and at tick 246 by the sheet.
2. **A language swap: no.**
   - On four laws and three measurers, the per-event SHA-256 is 91–98% of a compiled tick.
   - Across eight laws, compiled time follows SHA-256 compressions (0.159–0.181 µs each), not operations, whose cost
     varies by a factor of 5.3×10^5.
   - A faster language could touch only what remains: 1.5–9% of a tick.
   - Play built without the chain, writing the line, runs at 4.3–4.4% of the compiled tick at 1,000 bodies (measured
     by the proponent; rerun by the judge).
   - A GPU is never the authority. At most it could be a fifth execution, integer and fixed-point only, for many worlds
     at once.
3. **Graphics: in a view that may never write back and must never disclose.**
   - Shaders, spherical-harmonic lighting and post-processing stay in the view, in floats, hashed by nothing. No GPU API
     the survey read fixes a float result to the bit.
   - What decides play, or what a player may know, is computed in the law in Fix. Bands 0–2 of the spherical harmonics
     run byte-identically on the four executions.
   - The lineage's own renderer showed why "never writes back" is not enough. Verðandi's floor mirror puts a target
     hidden behind a wall on screen. No disclosure holds only by construction: each player's view is given only what
     that player may see (per-player output).
4. **A competitive headroom standard: none exists to adopt, and a number cannot be one.**
   - The survey found no standards body that publishes a competitive input-to-photon requirement.
   - Verðandi's own records refuse the competitive claim.
   - What can be had is a preregistered method on one component, the play tick against a declared period on a named
     host. It must count every tick that overruns, since a p99 label passed ten ticks that each took longer than the
     whole period.

## What the judge reran

| claim | made by | rerun here | result |
|---|---|---|---|
| the tick line names 13 of 13 planted defects at their tick; R5's pair 4; the shared-lowering budget case at tick 1 against 246 | proponent, P12 | the matrix, from its script on its snapshot | identical, but for a closing "P12 DONE" line (`judge/reruns/p12-plant-matrix.txt`) |
| segmented admission accepts a wrong receipt: ref-cost 2,000 against the sequential 32,000, every check passing | adversary, B1 | its script on its snapshot | identical (`judge/reruns/q3b-certificate.txt`) |
| the stream head, as prototyped, commits nothing of a refused tick: two different runs, byte-identical receipts | adversary, B2 | its script on its snapshot | identical (its output file rewritten, equal byte for byte) |
| play with no event chain, writing the line, costs 4.3% of the as-built 1,000-body landed tick | proponent, P13 | its script, three runs a cell | 0.044 (K = 1,000) and 0.048 (K = 100) against its 0.043 and 0.048 (`judge/reruns/p13-line-cost.txt`) |
| the reference keeps pace at 1,000 bodies and 1/120 s with four lanes of segments, not two | proponent, P14 | its script, three rounds | 202 and 114 ticks a second against 120 needed; its 197 and 109. Both plants caught the same (`judge/reruns/p14-segments.txt`) |
| Verðandi's renderer leaks a hidden target through its floor mirror | adversary, A10 | not rendered a third time; the proponent rendered it again | the two runs' three result files are byte-identical, checked here. One browser engine, one GPU: a reproduction, never a second platform |
| per-tick heads are blind to the operation count (named at 246 when the runs part at tick 1) | adversary, A1/A3 | not rerun by the judge | the proponent's rerun was identical, and P12 (rerun above) holds the same case |
| bands 0–2 in Fix agree four ways; 67.2 operations a direction; worst 1.23 units of 2^-32 against binary64; the event chain 91% of the compiled cost | the judge | `judge/make_sh.py`, `run_sh.py` and `analyze_sh.py`, run from this tree on the repaired code | identical to the record made on f16dc26 (`judge/analyze.txt`) |

## Q1: the speed reconciler

**The design (DECLARED; each part measured on stand-ins in version 0).**

| tier | runs | commits per tick | standing |
|---|---|---|---|
| play | the law's C program, resident, built without the event chain | the tick line, with `-` for the head | testimony: never one of the four executions |
| watch | the reference, behind play over the durable log; in segments from play's checked snapshots where it must | the tick line, head included | the record, by declaration |
| admission | the four executions over the closed log, the arbiter, the court | receipt 1, four ways | "replayed four ways over log ⟨seal⟩, unratified" |

**The line** (the proponent's `orlog-ticks 0`): `<t> <events> <ops> <output-bytes> <trace-head|-> <output-chain>
<claims> <state>`.
- Each field catches what the others miss: `ops` counting defects, `claims` a certificate's cost, `state` a silent
  write, the head a divergence that heals inside its tick.
- The receiver recomputes the output chain over the bytes it was sent. Without that, a byte written but never hashed is
  invisible: the runtime's own receipt reads equal. A self-report cannot convict itself.
- The reconciler compares lines in order. If every line agrees, it compares the final records, and a refusal names the
  tick after the last line.
- MEASURED (P12, rerun identical): 13 of 13 planted defects named at their tick, 12 without the head. Play's own
  no-chain build names 9 of its 10. The one it misses is the transient, which only admission sees.

**What the reconciler still cannot do, each found by the adversary in round 2 and MEASURED there.**
- **A truth value's storage flipped (1 to 3) is named 63 ticks late.** The encoding normalizes any nonzero to 1, and C's
  comparison reads the raw byte. Remedy: canonicalize at every write, or check each slot at the boundary. Its plant is
  this case.
- **Bytes shown are not bytes committed.** A defect between the hashed buffer and the bytes a view reads leaves every
  commitment equal. Remedy: the view verifies what it receives against the line's output chain.
- **A fault that does not recur** is named live, and a re-run of play localizes nothing. Remedy: play keeps a ring of its
  last ticks' events, written out when its line is contradicted.
- **The state digest is linear in the state.** About 20 ns an element in C and 134 ns in the reference, the binding
  side: at 2^16 Fix values the reference's digest alone exceeds 1/120 s. Large worlds trade "names the tick" for "names
  the window" (both parties agree).

**Segments (the watcher's speed) are credible and not yet safe.**
- The boundary induction is sound over what a snapshot holds, and a forged snapshot is caught (P11, P14; rerun).
- But the probe's snapshot omitted the certificate-cost accumulators. Segmented admission then passed every check and
  gave the wrong receipt (B1, rerun identical). In RUN-1's shape the same omission gives a false dissent against a
  correct play, and the wrong record stands.
- A restore defect turns a correct play into a dissenter (O3): the restore joins the authority.
- **The judge's reading:** SNAP-1 must hold every accumulator the receipt reads, and its restore needs a court of its
  own (the survey's GGPO sync test is the pattern) before a segmented watcher confirms anything. Live pipelining
  (lanes starting as play reaches them) is NOT_MEASURED.

**Live outcomes.** Both sides now agree that a live outcome is one execution's testimony until the watcher confirms it
(A4, conceded). The proponent's standings are the clearest statement found:
- **PLAYED:** shown, marked provisional;
- **WATCHED:** confirmed on this host;
- **REPLAYED:** four ways;
- **VOID:** at or after a tick a dissent names.

From the dissent's tick neither record is the match. Play's is void, and the reference's replays inputs that answered a
picture the law did not produce. What happens to play at a dissent is the owner's policy. The replay proves the
computation over the log, never the log's fidelity to what players did (A5; DOCTRINE T12, limit 4).

**R9 b's per-tick budget.** It is unsafe as written for a live outcome: a shared lowering defect moves when a match ends,
the compiled executions agreeing and only the reference dissenting (MEASURED: the sheet's commitments name tick 246,
the line tick 1). It is safe on three conditions (the proponent's; DECLARED):
- `ops` committed per tick, including in R5's `'T'` payload;
- the watcher is the reference;
- no refusal is declared before the watcher has refused at the same tick with the same record.

A budget in counted operations bounds no time (A16, conceded: one operation cost 10^5 times another). Committed SHA-256
blocks track compiled time within 1.13× across eight laws (P15b), so the unit is the owner's choice.

## Q2: a language swap

**No, MEASURED three ways.**
- My ablation: 91% of a compiled direction is the event chain, on the spherical-harmonics law.
- The proponent: 93–95% on fall and its bodies laws.
- The adversary: 95–98% on its bodies law, by regime.
- The proponent: compiled time per compression 0.159–0.181 µs across eight laws spanning five orders of magnitude of
  tick time.

What a faster language could remove is the remainder. The cost is the commitment's form:
- **For play:** no event chain at all, and the line: 0.043–0.048 of the compiled tick (P13; rerun 0.044 and 0.048).
- **For admission's compiled executions:** the stream head, one SHA-256 per tick over the tick's event records. It
  costs 0.29–0.31 of the chain on list-heavy ticks (P7, reproduced by the adversary). Two prices: it must be finalized
  into the receipt at a refusal and at the end (B2, rerun identical, a cheap fix); and a defect in the commitment's own
  code is located to its tick, never its event (O5). It is the owner's option for `orlog-trace-1`, no longer needed for
  play.
- **Hardware SHA-256** would be cheaper still. RUNTIME-SPEC §1 forbids compiler intrinsics, so it would be a contract
  amendment (NOT_MEASURED).

**A GPU is never the authority.** The parties agree, and the survey's reading of the specifications supports them:
- no GPU API fixes a float to the bit;
- WGSL has no 64-bit integer;
- a Fix multiply from 32-bit operations took 108–159 of them in two emulations, exact on every vector tried;
- order is meaning (products and refusals move with the order: MEASURED by the adversary).

At most a GPU could be a fifth execution, Int and Fix only, held byte for byte to the reference, used for many
independent worlds (previews, sweeps). It must beat the CPU baseline of P8: 64 worlds as 16 processes, 3.8–3.9×10^6
world-ticks a second, both parties.

## Q3: graphics and the view tier

- **What the view is.** It reads each tick's output (and, after SNAP-1, snapshots) one way, and reaches the law only as
  an input record of a later tick through the door. In it: shaders, spherical-harmonic lighting, fog, reflections and
  post-processing, in floats, hashed by nothing. R8 b, floats out of ports, stands untouched.
- **What goes into the law, in Fix:** whatever decides play or what a player may know: a line of sight, a visible set, a
  light level a rule reads. Its spelling, sign convention, constants and precision at the scales it meets must be
  declared.
  - The judge's law: four-way agreement, 67.2 operations and worst 1.23 units of 2^-32, for directions normalized from
    lattice vectors.
  - The adversary showed that short vectors lose precision, then refuse (A12): 0.276 at 2^-15 m, DIVISION-BY-ZERO below.
  - The proponent's pre-scaling by exact doublings repairs it: at most 3.8 units from 2^-28 m to 2^24 m, zero refusals,
    four-way agreement through the arbiter (P17; not rerun by the judge).
- **What it costs.** Per-pixel work in the law is out by orders of magnitude (A13, agreed). Light probes in the hundreds
  are affordable in C, about 0.8 µs each. The reference's 51 µs each bounds a sequential watcher to about 160 a 1/120 s
  tick.
- **Two clauses, only one checkable.**
  - **No write-back** is witnessed every tick by the state field (P12), as Verðandi holds `render-readonly` (the
    survey).
  - **No disclosure** fails in the lineage's own renderer (below) and holds only by construction: the door hands each
    view only its player's share. Per-player output is a precondition of any competitive use, and RUN-1 does not have
    it.

## Q4: headroom standards

- **There is nothing to adopt** (the survey): no standards body publishes a competitive input-to-photon requirement. What
  exists are vendor definitions (NVIDIA), a display certification (VESA), a QoE model (ITU-T) and studies (Spjut et al.).
  Instruments start and stop at different events, which is Verðandi's G4 rule. Verðandi itself makes no low-latency,
  competitive or input-to-photon claim (G7), and its numbers drift by 40–60% the same day (G13).
- **HEADROOM-0**, the proponent's preregistered method, is a falsifiable test of one component: the play tick against a
  declared period, on a named host, with:
  - a same-run comparator and a VOID gate;
  - 1,000 samples a cell;
  - a confirmation set over two sittings.

  Its r2 draft's sha256 (`a77a6424…`) and file time precede the pilot's first run, both checked here. But the
  adversary measured three ways its label misleads (O6, C2):
  - a p99 of 1,000 samples passes ten ticks that each overran the whole 1/60 s period;
  - a window of the first ticks passes a law whose later regime fails;
  - its 50‰ margin is smaller than the 29–60% the instrument's own p99 moved between sittings.
- **The judge's reading.** A headroom standard of the lineage's kind is a preregistered method, never a number. Its
  label is held to:
  - counts beyond the bound over every tick of the recorded session, falsifiable by one tick;
  - each regime ruled apart, with too few samples marked as such;
  - a margin wider than the drift measured on that host;
  - a confirmation across sittings;
  - a `does_not_show` naming any tick past the samples, the network, the display and every competitive meaning.

  It is the owner's to register or not. Verðandi's records give it its method (G4, G5, G10, G13), never a number to
  meet.

## Proposed changes to the RUN-1 sheet (for the owner's ruling; none is an edit)

From both parties, as the judge weighs them. The grades are of the evidence for each, not of the design.

| | proposal | evidence |
|---|---|---|
| must | **A tick line** (`orlog-ticks 0`) written by every execution given a path: events, ops, output bytes, the head (`-` in a play build), the output chain, a claims digest, a state digest | MEASURED (P12, rerun) |
| must | **`ops` in R5's `'T'` payload** | MEASURED (P12; the adversary's A1) |
| must | **The reconciler's rule**: lines in order, then the final records; the output chain recomputed by the receiver | MEASURED (P12's out-unhashed and refusal-code rows) |
| must | **The output chain's start and edges**: out_0, the prefix's output, a refused tick's partial output | ESTABLISHED (R5 leaves them undefined) |
| must | **The log as a stream with an end record**; D3's "a run completes when its log ends" to mean that record | ESTABLISHED |
| must | **What `ticks` counts at a refusal** (ticks begun; a refused tick writes no line) | ESTABLISHED |
| must | **A port range the door enforces**, refusing a record whole without ending the session; what the tick then receives is the owner's | MEASURED (A9's stand-ins, both parties) |
| must | **R9 b's three conditions**: ops committed per tick, the reference as the live watcher, no refusal declared before the watcher confirms it | MEASURED (P12); conditions DECLARED |
| must | **Snapshots hold every accumulator the receipt reads**, with B1's law as their plant (for SNAP-1) | MEASURED (B1, rerun) |
| must, if the stream head is adopted | **The stream finalized into the receipt** at a refusal and at the end, with B2's two laws as plants | MEASURED (B2, rerun) |
| new ruling | **R13, what a live outcome is**: PLAYED, WATCHED, REPLAYED, VOID; never "verified", "final" or "fair"; admission's phrase "replayed four ways over log ⟨seal⟩, unratified" | DECLARED (A4, A21, conceded) |
| new ruling | **R14, play's build**: the c99 program may be built without the event chain for play, its record testimony and never one of the four executions | MEASURED (P13, rerun; P12) |
| should | **A truth value's representation** canonicalized at every write or checked at each boundary | MEASURED (O1) |
| should | **The view verifies what it receives** against the line's output chain | MEASURED (O2) |
| should | **Play keeps a ring of its last ticks' events**, written out when its line is contradicted | MEASURED (O4) |
| should | **The restore held by its own court** before a segmented watcher confirms anything | MEASURED (O3) |
| should | **R12's discriminator gains P12's plants**, and B1's, B2's and O1's | MEASURED |
| should | **"What this sheet does not decide" names per-player output** as a precondition of any competitive use | MEASURED (A10); DECLARED |
| option | **R9 b's unit**: committed SHA-256 blocks beside or instead of operations | MEASURED (P15, P15b) |
| option | **The stream head in `orlog-trace-1`**, for admission's throughput | MEASURED (P7, reproduced) |

## Found about Verðandi (the owner's to weigh)

**The native renderer shows a target hidden behind a wall** (`art/web/scene_render.js`, through its floor-mirror pass).
- **The setup.** Under plaza-night's air, a target of the graybox's size stood wholly behind a 4 m wall. It changed
  76–457 pixels, by up to 30 of 255 in a channel, at the wall's foot, at every tested distance from 6 m to 40 m. On a dry
  rough floor it changed 162–1,076 pixels, by 1–3.
- **The cause.** Two one-line ablations of the copied renderer isolate it. The mirror pass discards everything below
  2 cm and culls front faces, so the reflected scene behind the wall is drawn into the texture the floor samples.
- **Grade:** MEASURED twice (the adversary's run and the proponent's; their result files byte-identical), on one browser
  engine and one GPU, in a synthetic scene in the renderer's schema.
- **Does not show:** that it occurs in plaza-night's own geometry or on another platform; that a person would notice it;
  that any player was affected.
- **What it means.** The owner's rule, as Verðandi keeps it, governs where walls, cover and blocking objects exist, and
  the leak decides none of them. The rule holds. Its short form, read as "cannot affect play", overclaims. The
  graybox page already hands its live state to the browser's console as `window.GRAYBOX` for tests (Verðandi's
  `docs/BOUNDARIES.md`, the interface's row, read here), so nothing there is hidden from its player today. The leak
  matters for any world that claims to hide something.
- **Proposed:** a ghost in Verðandi's `docs/GHOSTS.md` (disclosure is unchecked; the floor mirror leaks), or a pixel
  court of the adversary's kind, before any world claims to hide state. It is written here only because Verðandi is
  read-only to this debate.

## What this verdict does not show

- **Hosts and machines:** any other host, operating system, GPU or browser. Every timing is a software timing of one
  component on this host, under heavy memory load (93–98%) and other sessions, labelled so.
- **Experience:** a latency, a frame rate, input-to-photon, feel, or any competitive property; nothing here may be read
  as one.
- **RUN-1 as built.** Every measurement ran on stand-ins in version 0: a For loop for a tick block, a literal for a port.
- **Figures from this tree alone:** the debaters' figures not rerun here are OBSERVED, since their scripts are in
  ignored `work/` folders.
- **That twelve kinds of defect are all.** P12's falsifier stands open: a defect that changes the receipt, the output or
  carried state and is named at no tick.
- **That one model family's agreement is truth.** The front end, which every execution shares, is seen only by the twin
  (DOCTRINE T11).

## The records

| file | what |
|---|---|
| PROPOSAL.md | the owner's words verbatim, the four questions, what was fixed, the records the debate started from |
| RESEARCH.md | the prior-art survey (nine topics; sources graded [P], [A], [S], [U]) |
| PROPONENT.md, PROPONENT-R2.md | the design, round 1 (P0–P11) and round 2 (P12–P17, the adversary's experiments rerun) |
| ADVERSARY.md, ADVERSARY-R2.md | the prosecution, round 1 (22 findings) and round 2 (B1, B2, O1–O9, C1, C2, W1; the proponent's probes rerun) |
| `judge/` | the judge's spherical-harmonics measurement, runnable from this tree: `make_sh.py`, `run_sh.py`, `analyze_sh.py`, `time_sh.py 21`, `ablate_hash.py 21`, with their recorded outputs |
| `judge/reruns/` | the judge's reruns of the debaters' decisive probes, as records (their scripts are in `work/`) |
