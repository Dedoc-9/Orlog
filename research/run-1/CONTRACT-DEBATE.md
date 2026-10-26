# RUN-1's contract, debated against an outside review (2026-10-26, at 9cb21f6)

An outside reviewer read `DESIGN-BRIEF.md` and argued for a contract-first review before 1a. The owner asked for a
debate of better solutions, pioneering ones included. The review is paraphrased here, never quoted. Each item gives:
- the review's position;
- the better solution proposed here;
- the strongest objection to that solution;
- a grade, and a falsifier that can fail.

Nothing here is ruled or built. The sheet (`RULINGS.md`) stays the source of truth. This record is one session's model
output. The review is the debate's other side, but no adversary has attacked this record yet.

**Prior art.** Where a design has prior art, the source is named from memory and was not re-read here. No novelty is
claimed for any mechanism. What is new is only its place in this project.

## Where the review and this record agree

- Settle the permanent formats before 1a; the frozen corpus is a compatibility check, never coverage (H9).
- Every new guarantee gets its own falsifier and a plant; a clean corpus run substitutes for none.
- Fix H1 in 1b with R11. Keep R6 conservative.
- Separate a record of what happened from a later replay's ability to recompute it.

## D1. What a trace proves: the theorem's conditions

**The review.** Replay's conditions should name the law bytes, the input-log bytes, the runtime contract and the
declared semantics. Two claims should be kept apart: replay determinism (the same conditions give the same records)
and execution validity (the records follow the semantics). The receipt should carry the distinction.

**Better.** Agree on the split, with one correction and one addition.
- **Correction: a toolchain is never a condition of the theorem.** The theorem quantifies over conforming executions:
  *given the law's bytes, the input log's bytes and the semantics version the law's header names, every conforming
  execution writes the same receipt core and the same trace*. If a compiler, a runtime build or a host were a
  condition, a disagreement under a new compiler would read as a changed condition, an excuse. Under this reading it is
  a dissent: a defect in one execution. The runtime contract is part of the declared semantics (RUNTIME-SPEC), so it is
  covered.
- **The core commits to the conditions; the envelope carries the witnesses.** The receipt core, the part every
  execution must match byte for byte, names the law seal, `input-log-sha256` and the semantics version. Today's
  `backend` line, the one line `receipt_core` removes, grows into a per-execution envelope: the backend, its build
  record and the identity coverage of H1 (D6). Agreement is decided on the core alone, as now.
- **Validity is never written into a receipt.** No receipt line may say "valid" or "correct". This mirrors the court's
  `forbidden_interpretations`. Validity is held only by independent readings: the twin's rounds, hand-worked probes,
  and vectors with a second derivation.
- **Pioneering, proposed for later: per-run spec coverage.** The reference knows which rules of §15 a run exercised:
  the operation kinds, the event kinds, the refusal paths taken. A per-run coverage statement would list them and mark
  each as held by an independent reading (a twin probe or a hand-worked vector) or by the reference alone. That turns
  the review's validity caveat from a README sentence into a computed, falsifiable line. Prior art: specification
  coverage in conformance suites; requirements traceability; MC/DC coverage in DO-178C (from memory).

**Strongest objection.** The coverage statement is theorem decoration, the overclaim the courts found most often.
**Answer.** It must sit outside the core, raise no standing, and be held by plants:
- a rule that was exercised but is not listed;
- a rule listed as independently held that has no probe.

Until those plants exist it stays DECLARED, a later fork.

**Grade:** DECLARED. **Falsifier:** two conforming executions whose cores differ under one law, one log and one
semantics version (a dissent the theorem forbids), or a core line that differs by toolchain.

## D2. Is the trace a record of what happened, or of what can be recomputed? (the review's challenge)

**The review.** The trace should be authoritative about the inputs and outcomes actually recorded, and the replay
contract about whether they can be reproduced. A successful replay must never rewrite the meaning of a refusal.

**Better: confine all nondeterminism to one sealed record, and make the door a replayed pure stage.**
- **The arrival log is the history.** It holds everything that reached the door, in order, with the tick the host
  assigned it to. That includes records the door refused, with their refusal code. The host's scheduling (which tick
  an input lands on) is the only nondeterministic decision in a session, and it is recorded here and nowhere else.
- **The door is a pure, versioned function of the arrival log.** Its refusals (R3 a) become reproducible facts, not
  side effects. Run again, the door refuses the same arrivals with the same codes and the same neighbours.
- **The input log is the door's output,** the law's replay basis, as R5's receipt names it.
- **A replay never rewrites history.** It yields a new receipt, compared with the recorded one. A dissent is recorded
  beside the history, never in place of it (R4's refused branch, the speed verdict's VOID).

This answers each of the review's three uses:
- a live game records an event even when execution later refuses: it is in the arrival log;
- a test harness gets exact replay: two pure stages;
- an editing interface keeps invalid user input without accepting it: the input is an arrival, refused by the door,
  and the law never sees it.

Prior art: event sourcing's split between commands, which may be rejected, and events, which are accepted facts;
record-and-replay debugging; lockstep game networking (from memory).

**Strongest objection.** Two logs double a one-way format. **Answer.** Keep one file:
- a stream of two record kinds, accepted tick records and refused arrivals;
- the input log is the projection of the accepted records, so `input-log-sha256` names the projection.

The arrival log's own hash goes into the envelope as history, beside the core.

**A ruling it surfaces.** When an arrival is refused but its tick must still run (D1 makes records dense), what does
the port read? This is the speed verdict's open item. Three options:
- (a) the tick does not run, and the session ends as at a refusal;
- (b) the port holds its previous value, marked `held` in the input log;
- (c) a declared default, marked the same way.

R3 a's principle, that the log holds only values the supplier sent, favours (a), or (b) and (c) only with their mark.

**Grade:** DECLARED. **Falsifier:** an arrival log and a door version whose input log differs between two runs, or a
replay that changes a recorded receipt instead of recording a dissent.

## D3. The log's framing: a stream with a mandatory end record

**The review.** Prefer a stream with an explicit end record, mandatory for a completed run. It would bind the trace
head, the output chain, the tick count and the terminal status, and refuse missing, duplicated, malformed or trailing
records.

**Better.** Agree on the stream and the end record, with two corrections and one addition.
- **Dense and stream are not rivals.** D1, dense records, says what each tick record holds: every each-tick port. The
  stream says how records are framed. RUN-1 can and should have both.
- **The input log's end cannot bind execution results.** The door writes the log before, and apart from, any
  execution; the trace head and the output chain are results. The log's end record binds the log's own facts:
  - the tick count;
  - the log's running chain head;
  - why it closed (the host closed it, or the client ended).

  The results are already bound by receipt 1 and by the last tick line.
- **An open log is its own status.** A log with no end record (a crash, a live session still running) replays as a
  prefix, with the status `LOG-OPEN`, never COMPLETED. D3, "a run completes when its log ends", then means that the end
  record was read.
- **Addition: the tick line binds three chains.** `orlog-ticks 0` already carries the output chain and the trace head.
  Add the input chain at tick t. Each tick line then commits the input prefix, the event prefix and the output prefix
  together. A watcher locates a truncated or altered input at its tick, and a client holds a per-tick acknowledgment
  that its input was consumed as sent. Prior art: the per-frame sync checksums of lockstep RTS netcode, which detect a
  desync at its frame (from memory).

**Strongest objection.** One more field on every tick line costs a hash per tick. **Answer.** It costs one SHA-256 of
one record per tick, against the per-event chain's one per event, which the owner kept (R5).

**Grade:** DECLARED. **Falsifier:** a truncated log that replays to COMPLETED, or a tick line that does not move when
its tick's input record is changed.

## D4. R10: what the port signature is

**The review.** Bind the log to the canonical port declarations, under a versioned serialization, tested with altered
signatures.

**Better: reuse the law's own canonical lines, with one field projected out.** R5's law line is
`(port <var> "<name>" <type> each-tick|once)`, and SPEC §5 numbers variables "in textual order of declaration (Let,
For counter), including inside procedure bodies". So `<var>` moves when an unrelated `Let` is added before a port. A
signature over the law line as written would refuse every old log after such an edit, which is the edit R10 a exists to
allow. The signature is then:

```
SHA-256( "orlog-ports 0\n" || for each port in declaration order: (port "<name>" <type> each-tick|once)\n )
```

Each field is there for a reason:
- the order, because the records are positional (D1);
- the name, because swapping the names of two ports of one type would otherwise replay with their meanings crossed;
- a declared port range, if the speed verdict's door range is ruled, because it changes what the door accepts.

The rows:
- an unrelated `Let` inserted before the ports, after which the old log must replay (plant: `<var>` kept in the
  signature);
- two same-typed ports with their names swapped, which must be refused PORT-SIGNATURE (plant: the name left out);
- a kind changed from once to each tick, which must be refused.

**Pioneering, for later: sealed port adapters.** An edit that adds a port (a new `wind`) can never replay an old
session under R10 a. A preview in EDIT-0 could name a tiny sealed adapter, itself a law, that maps the old log onto the
new ports (`wind` is 0 each tick). It would be named in the preview's receipt and never written into the world's
history. That keeps the App Studio's cheap exploration across signature changes without loosening R10.

**Strongest objection.** Adapters are a second language in the replay path. **Answer.** They are laws, under the same
semantics and seals, and only a preview names one. The proposal is DECLARED, for after RUN-1.

**Grade:** ESTABLISHED for the `<var>` defect (SPEC §5 and R5's law line, read); DECLARED for the rest. **Falsifier:**
an unrelated edit that changes the signature, or a semantically different declaration that does not.

## D5. R9: the budget's semantics, and a static bound

**The review.** Before freezing `budget <N>`, settle five things:
- which operations count;
- whether the exhausting operation is counted;
- whether the budget is per tick;
- whether exhaustion is an ordinary transactional refusal;
- whether every execution counts the same abstract operations.

**Answers from what exists.** Most are already fixed:
- the operations are v0's counted operations (SPEC §7);
- every execution counts them alike, since `ops` is in the receipt core;
- the budget is per tick (R9 b);
- exhaustion is a refusal like any other under R4 a, its partial output hashed (R5, amendment 2).

The one open point gets the rule v0 already uses: SPEC §7 adds 1 to `ops` "immediately before" each operation. So the
(N+1)-th operation of a tick is counted, then refused before it runs, and a TICK-BUDGET tick's count is exactly N+1.
That is an exact row (below, D8).

**Pioneering: the budget as a compile-time obligation.**
- Every loop is bounded and there is no recursion, so a tick's worst-case count can often be computed from the text:
  the loop bounds times the bodies' counted operations.
- A law whose computed bound is at most its budget is BUDGET-PROVEN. It cannot refuse TICK-BUDGET.
- In a proven law, a TICK-BUDGET at run time is an implementation defect, a dissent of its own class, never a verdict.
- That removes H11's hazard for every proven law. A shared lowering defect cannot move when a match ends by budget,
  because no match ends by budget.
- A law whose bound depends on state (a loop to a variable, a list that grows) keeps the runtime budget, with the
  speed verdict's three conditions.

Prior art: WCET analysis for hard real-time code, automatic resource-bound analysis such as RAML, and gas metering (from
memory).

**Strongest objection.** The bound is useless where loop bounds are variables: an i64 bound proves nothing. **Answer.**
That is why the runtime budget stays. How many laws the proof covers is a measurement not yet made: compute the bound
for the corpus's 11 programs and compare it with their measured per-tick counts. Until then, DECLARED.

**Grade:** ESTABLISHED for the answers read from SPEC §7 and the sheet; DECLARED for the static obligation.
**Falsifier:** a proven law that refuses TICK-BUDGET on any execution, or a computed bound below a measured count (an
unsound analysis).

## D6. H1: build identity

**The review.** Key the cache on the effective build environment: tool paths and digests, full version output, flags,
headers, libraries and target. Record what could be identified. Never claim a complete identity without a hermetic
build. Fix it in 1b with R11, and test it with two stand-ins and a changed dependency.

**Better.** Agree, and add one rule: **provenance follows the artifact.**
- The witness names the identity recorded when the cached program was built, never the compiler now on PATH. Today the
  two are equal only because a record mismatch rebuilds.
- The record lists its identity coverage: what was hashed (the compiler binary, the source, the flags), what only
  reported a version (the linker), and what was not identified (system headers, dynamically loaded components).
- The witness repeats that coverage instead of a bare toolchain line.

**Strongest objection.** None of substance. A hermetic toolchain would close the gap, and it is out of scope.

**Grade:** ESTABLISHED for the defect (`arbiter.py`, read; `DESIGN-BRIEF.md` H1); DECLARED for the repair. **Falsifier:**
a cache hit across two compiler binaries that report one version line.

## D7. H3: the neighbour refusal at the ends of the range

**The review.** Do not promise two neighbours where one exists. Report one, with a marker for the other, and let a
range refusal take precedence over a grid refusal.

**Better: the precedence alone makes the owner's rule exact, with no marker.** Fix's bounds, raw −2^63 and 2^63−1, are
themselves on the grid. Take a value v off the grid with MIN < v < MAX:
- floor(v·2^32) ≥ MIN·2^32, because MIN·2^32 is an integer below v·2^32;
- ceil(v·2^32) ≤ MAX·2^32, likewise.

So once the range is checked first, every grid refusal has two in-range neighbours, exactly as his ruling says. A value
outside the range is a range refusal, which names the nearest in-range value, the bound.

**MEASURED here,** with exact rationals against `numeric_ref.I64_MIN` and `I64_MAX`, over 220,136 values (both ends,
inside and out, and random values in range):

| order | grid refusals | with a neighbour out of range |
|---|---|---|
| range first (proposed) | 210,115 | 0 |
| plant: grid first | 220,122 | 10,007 (e.g. −2147483648.1) |

The script is in the session's scratch folder, not the tree; the row for 1a is its proof and both ends worked by hand.

**Strongest objection.** None: the review's precedence is the repair, and the marker is unnecessary.

**Grade:** MEASURED, with a proof. **Falsifier:** an off-grid value within the bounds with a neighbour outside them.

## D8. H4: what `'T'` counts

**The review.** `'T'` carries the cumulative count before the tick's body; the tick line carries that tick's own count.
Successive boundaries reconcile with the tick lines. Settle a refused tick, and work a three-tick trace by hand before
freezing the wire format.

**Better.** Agree. The cumulative count runs from the start of the run, so `'T'` of tick 1 carries the prefix's count,
and a counting defect in the prefix is located at tick 1. The reconciliation is three identities:
- `T(t+1).ops − T(t).ops` equals tick t's line's `ops`;
- `T(1).ops` is the prefix's count;
- the receipt's `ops` minus the last `T`'s is the last tick's count, or a refused tick's partial count.

**Worked by hand** (DECLARED: arithmetic, not run). The prefix counts 5 operations, tick 1 counts 10 and tick 2 counts
7. Tick 3, under `budget 12`, reaches its 13th counted operation:

| record | content |
|---|---|
| `'T'` 1 | (1, 5) |
| line, tick 1 | ops 10 |
| `'T'` 2 | (2, 15) |
| line, tick 2 | ops 7 |
| `'T'` 3 | (3, 22) |
| line, tick 3 | none: a refused tick writes no line (R5, amendment 3) |
| receipt | `ticks 3`, `status REFUSED TICK-BUDGET <clause>`, `ops 35` |

The checks:
- 15 − 5 = 10 and 22 − 15 = 7;
- 35 − 22 = 13 = N + 1, the exact count of a TICK-BUDGET tick (D5).

If tick 3 had refused otherwise after 4 operations, the receipt would read `ops 26`.

**Grade:** DECLARED. **Falsifier:** a trace in which any of the three identities fails, or a TICK-BUDGET tick whose
count is not N+1.

## D9. H5: the state digest

**The review.** Do not trade per-tick localization for speed without saying so. Keep the authoritative frequency apart
from a performance profile, label sampled evidence as sampled, measure before changing, and prefer an incremental
commitment over a weaker claim.

**Better.** Agree. Make the guarantee a named field of the tick line, so a sampled digest can never pass for a
per-tick one: `state per-tick`, `state every <k>` or `state write-set`.

**Pioneering, for the authoritative build: an incremental state root.**
- A Merkle tree over the variable slots costs O(writes × log n) per tick instead of O(n).
- Its root at tick t localizes a silent write to its tick.
- It also gives inclusion proofs for single slots. That is what the speed verdict's view rule needs: a view could
  verify exactly the slots it draws against the tick's root (the speed verdict's "The view verifies what it receives", O2).
- It also prepares per-player output, the speed verdict's precondition for any competitive use. A player receives only
  the slots that player may see, each with its proof. "Never disclose" then becomes a check, not a hope.
- Prior art: per-block state roots with account proofs in Ethereum; incremental multiset hashes such as Bellare and
  Micciancio's, and LtHash (from memory). The lineage already asked when a session's content needs a tree commitment
  (Verðandi's DSC-0 probe).

**Strongest objection.** A Merkle root multiplies the hashing per write. The per-event chain is already 91–98% of a
compiled tick, and the speed verdict exists because of that cost. **Answer.** Measure first, as the review says.
Compare writes per tick with the state's size on the corpus programs. The tree wins only where writes per tick are
small against n / log n. A write-set chain, a hash of each tick's writes in order, is the cheap alternative: exact
localization, but no single-slot proof.

**Grade:** DECLARED. **Falsifier:** a sampled digest reported as per-tick, or a silent write that leaves the tick's root
unchanged.

## D10. The PREFIX edge, and the reporting pass's question in general: completeness by reachability

**The review.** Distinguish three cases:
- a claim whose evaluations all completed before any input;
- a claim whose sequence of evaluations a refusal interrupted;
- a claim with no completed evaluation.

Only the first earns the PREFIX exemption. An interrupted sequence must not earn grounding on its completed subset.

**Better: one rule that decides interruption for every run, closed or open, and contains the owner's R6 ruling as a
special case.**
- **R8′:** a claim's sequence of evaluations is complete when the refusal's site cannot reach the claim's site. A claim
  whose site the refusal's site can reach is withheld as interrupted.
- Runs are total, control is structured and there is no recursion, so reachability is a small static question. The
  claim's site is reachable from the refusal's site when:
  - it follows the refusal in an enclosing statement sequence;
  - the two share an enclosing loop;
  - or the claim is in a procedure performed at a reachable site.
- **R8 is its special case:** a refusal at the claim's own clause reaches the claim.
- **The owner's PREFIX ruling is its special case:** a tick cannot reach a PREFIX claim, so the claim stays held.

Classified by reading (ESTABLISHED by reading, not run through an implementation):

| case | the refusal | reachable? | today | under R8′ |
|---|---|---|---|---|
| `mutant/s1/2127` §3, the corpus's one claim held in a run refused elsewhere (`research/compat-status.md`) | §4, CLAIM-REFUTED, a later top-level statement | no: no loop holds both, and §3 comes first | held, "true in 1 of 1" | held: unchanged |
| `tests/fixtures/court/hoisted_omit.orl` §2.2 | §2.1, in the 17th iteration of §2's loop | yes: the next statement, in the same iteration | held, "true in 16 of 16", WELL-FOUNDED | withheld, interrupted |

So R8′ changes nothing on the frozen corpus, by this classification, and withholds exactly the review's case. It
settles the reporting pass's open question for closed runs too, without a separate ruling for each shape.

**Strongest objection.** It is conservative. A refusal in a loop's last iteration, after which the claim would never
have run again, still withholds. **Answer.** It is sound, not complete, as R6 is. It only withholds, so it is measured
one-sided, as R8 was. A later dependence analysis could narrow it (the doppler verdict).

**Grade:** DECLARED for the rule; ESTABLISHED by reading for the two cases. **Falsifier:** a claim withheld whose site
the refusal cannot reach, or a claim held whose site it can (plants: reachability by textual order alone, which misses
the shared loop; and "never withhold", today's court).

## D11. H2, made an invariant instead of a test

**The review.** Read the marker at column one, as the parser does. Give each new line form a three-part contract:
lexical recognition, parse or refusal, and canonicalization. Hold it with paired rows and a plant that splits the door
from the parser.

**Better.** Agree, and enforce it at compile time as well. The parser reports each line's kind, and the door's
classification is compared with it on every compile. A disagreement is refused with its own code, a door–parser split.
It is never written into a repair report as if it had been read. Paired rows still test each form, but the invariant
then also holds for forms nobody wrote a row for. Under today's two rules a split happens only on an indented `Note:`
or `Title:`, and the corpus has no indented line (MEASURED, `DESIGN-BRIEF.md` H2), so the guard changes no frozen
verdict.

**Strongest objection.** A guard that should never fire is dead code. **Answer.** Its plant makes it fire (the door's
`lstrip` restored), and R2's new forms are where it earns its place.

**Grade:** DECLARED. **Falsifier:** a compile in which the door and the parser read a line differently and no refusal
results.

## The order proposed

The review's order, with three changes:
- the authority question first, because it decides the log's model;
- H3 closed now, because the precedence settles it;
- R8′ and H2 placed by what they touch.

| step | work | why there |
|---|---|---|
| 0 | D2: the arrival log, the door as a pure stage, and a refused arrival's tick (a, b or c) | it decides the log's model, which every later format serves |
| 1 | The one-way formats: D3's framing and end record, D4's signature, D5's budget rule, R2's three-part contracts | they become every session's bytes |
| 2 | D7 (closed by precedence), D8's identities | the door's and the trace's arithmetic, worked by hand |
| 3 | D9: the named state guarantee, and the measurement of writes against state size | so the guarantee cannot weaken silently |
| 4 | Draft §15, then R7's paper round over it, then 1a | the round reads the contract the steps above fixed |
| any time | D11 (H2's repair and the split guard); R8′ as a court change before RUN-1 | each is independent of the formats |
| 1b | D6 with R11 | both revise the runtime contract |
| later forks | D1's spec coverage, D4's port adapters, D5's static budget, D9's state root | each needs a measurement or a trigger first |

## Rulings this needs from the owner

- **D2:** the arrival log as the history, the door as a pure, versioned stage, and what a refused arrival's tick does
  (a, b or c).
- **D3:** the stream with an end record, `LOG-OPEN`, and the input chain in the tick line.
- **D4:** the signature over the port lines without `<var>`.
- **D5:** the (N+1)-th operation counted and refused before it runs; the static budget as a later fork.
- **D7:** range before grid.
- **D8:** `'T'` cumulative from the run's start.
- **D10:** R8′, as a court change.
- **D11:** the door–parser split as a compile-time refusal.

## What this record does not show

- That any of these designs is correct. The theorems stay DECLARED, and nothing is built.
- That any mechanism is novel. The prior art named is from memory.
- An adversary's attack on this record. The review is the only other side so far.
