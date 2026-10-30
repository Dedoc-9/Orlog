# RUN-1's contract: rounds A to D, the theorems under it, and the decisions for the owner (2026-10-26)

The outside reviewer's second response asked for four narrow rounds before any ruling, each closed by a falsifier:
- **A:** arrival history and refusal;
- **B:** canonical bytes and identity;
- **C:** refusal, claims and operation counts;
- **D:** an independent attack on the written contract.

It also proposed a ruling for the arrival-refusal question, option (a). The owner's word on all of this: *"let's keep
this debates final decisions for the next push."* So nothing here is ruled. Every decision below waits for him, and
they are pushed together. The commit that recorded the debate (95dac79) settled no rule and established no claim by
execution, and neither does this file, except where a result is marked MEASURED.

Files of this round:
- `CONTRACT-DRAFT.md`: the contract as rules alone, for the adversary;
- `ADVERSARY-ROUND-D.md`: the adversary's record, which read only the draft and version 0's specifications;
- `probes/completeness_probe.py`: §8.4's rule measured on version 0, with its output in `evidence/run1-completeness.txt`.

**After the reviewer's third reply** (the same day): static may-reach must not stand in for dynamic interruption; the
input boundary needs one declared policy; the theorems become a ledger of proof obligations. CUT-0 answers it:
- `CUT-0.md`, the note;
- `probes/cut0_claims.py`, the causal cut captured from version 0's reference (`evidence/run1-cut0-claims.txt`);
- `probes/cut0_session.py`, the session as a transition system (`evidence/run1-cut0-session.txt`);
- `probes/t8_monotone.py`, T8 checked against the court's code (`evidence/run1-t8-monotone.txt`).

Where this file and CUT-0.md differ, CUT-0.md is the later reading: C2's choice between a call path and replay is
replaced by the cut, and A2 gains its declared policy.

Each item uses the reviewer's record:
- the proposed rule;
- the strongest objection;
- the smallest counterexample;
- the required observable result;
- the falsifying test;
- the decision (open, ruled or deferred);
- the change class (one-way or two-way).

The reviewer's text is paraphrased, never quoted.

## Round A: arrival history and refusal

### A1. Three records, kept apart (the reviewer's model)

- **Proposed rule:** the arrival history (every arrival, refused ones included), the door's result (an accepted encoding
  or a refusal, from a pure, versioned door) and the execution's result (whether each tick ran) are three records. None
  is derived by reading another's prose. The door is replayed from the arrival history; the execution is replayed from
  the input log.
- **Strongest objection:** three records are three formats to keep, and every one is one-way.
- **Answer:** only the input log is read by the law. The arrival log is history, and the door's results are recomputed
  from it, never stored as an authority.
- **Required observable result:** the door's results, recomputed from the arrival log by the door's version, equal the
  results recorded when the session ran.
- **Falsifying test:** a refused arrival whose replayed door result differs. Its plant is a door that reads anything
  but the port's declaration and the bytes, such as a clock or the previous arrival.
- **Decision:** open. **Change class:** one-way.

### A2. What a refused arrival does: the reviewer's (a) against judging before assigning

The reviewer proposes (a): an arrival assigned to tick t that the door refuses blocks the whole of tick t, every port
of it. The tick does not run, the session ends, and nothing is invented, held over or defaulted. Recovery would be a
separate, explicit rule. The draft states this as **A1** (assign, then judge) and the alternative as **A2** (judge,
then assign: a refused arrival is answered to its source and never assigned; a tick the host closes without a value
does not run).

- **Proposed rule (this record's recommendation): A2**, keeping every principle of (a):
  - a whole tick is blocked, never a port;
  - nothing is invented;
  - the session ends at a tick that does not run;
  - recovery is SNAP-1's.
- **Strongest objection to A1, a live game with a hostile client.**
  - **Smallest counterexample:** a client sends `1.1` to a fixed-point port, which the door refuses as INPUT-GRID.
  - Under A1, its tick does not run and the session ends for every player.
  - One malformed message ends any match: a denial of service built into the contract.
  - Under A2, the arrival is refused and answered, the client can send again, and the tick waits for an accepted value
    or for the host to close it.
- **Strongest objection to A2.**
  - A hostile client can still end a match by sending nothing. That is lockstep play's old problem. It is now a host
    decision (when to close a tick), recorded as history and visible as INPUT-MISSING. It is not built into the door.
  - A2 also puts a timing decision, closing a tick, into the history. The input log's end record carries the closing
    (§2.1), so the execution stays a function of the input log alone.
- **The test harness:** A1 and A2 coincide. An offline log has one record per tick; a refused record leaves its tick
  without a value, so the tick does not run under either.
- **The editor:** under both, the invalid input stays in the arrival log. Under A2 the person corrects it before its
  tick runs, which is what an editor needs.
- **The distinction the reviewer asked to keep:** INPUT-REFUSED is the door's result, a fact about an arrival in the
  arrival log. NOT-RUN is the execution's result, a fact about a tick. Its cause in the input log is INPUT-MISSING
  under A2 and INPUT-REFUSED under A1. The arrival log says why a value was missing: refused arrivals, or none.
- **The four cases the reviewer asked for, and what A2 requires:**

  | case | arrival log | input log | outcome |
  |---|---|---|---|
  | the first arrival is refused | the arrival with INPUT-GRID, unassigned | no record yet; at closing, `end 0 not-run 1 INPUT-MISSING <port>` | NOT-RUN 1, ticks 0 |
  | a later arrival is refused, then corrected | the refused arrival, then the accepted one assigned to its tick | the tick's record, as if no refusal | the tick runs |
  | two arrivals share a tick, one is refused and not resent | one accepted and assigned, one refused | at closing, `end t−1 not-run t INPUT-MISSING <port>` | NOT-RUN t: the whole tick, the accepted port's value included |
  | replay | unchanged | unchanged | the door, replayed, refuses the same arrival with the same code and neighbours; the execution, replayed, writes the same receipt core |

- **Falsifying test:** a tick that runs with a port whose arrival was refused and never replaced. Its plants are the
  previous value held and a default given.
- **Decision:** open (A1, the reviewer's, or A2, this record's). **Change class:** one-way.

### A3. A collapse found before the adversary, and its repair already in the draft

- **Smallest counterexample:** two sessions with the same tick records 1 to t−1. In one the host closed the session
  normally after tick t−1. In the other, tick t was not run. Without a cause in the end record, both read COMPLETED.
  With one, they read COMPLETED and NOT-RUN t.
- **Required observable result:** the end record carries its cause (`closed`, or `not-run <t> <cause> <port>`), and
  the outcome reads it.
- **Falsifying test:** two logs differing only in the end record's cause, with equal outcomes. The plant is an end
  record without its cause.
- **The same for an open log:** LOG-OPEN, when every record of an open log ran, is never COMPLETED. A run that refuses
  inside an open log is REFUSED, since a refusal is final whatever follows (§4.5).
- **Decision:** open, with the draft. **Change class:** one-way.

## Round B: canonical bytes and identity

### B1. The port signature leaves out the variable number (R10)

- **MEASURED here (version 0's law bytes).** `§1 Let thrust be 3.` compiles to `(let 0 "thrust" …)`. With
  `§1 Let unrelated be 0.` inserted before it, the same variable is `(let 1 "thrust" …)`, and its read becomes
  `(var 1)`. So `(port <var> …)` moves under an unrelated edit.
- **Proposed rule:** the draft's §3. It hashes `orlog-ports 0\n`, then one `(port "<name>" <type> each-tick|once)\n`
  line per port in declaration order.
- **Strongest objection:** including the name makes a deliberate rename refuse every old log.
- **Answer:** the records are positional, and swapping the names of two ports of one type would replay them crossed.
  A rename is a semantic edit. The later port-adapter fork serves the edits that must cross it.
- **Required observable result:**
  - an unrelated `Let` before the ports leaves the signature equal;
  - renaming, retyping, reordering or changing a port's kind changes it.
- **Falsifying test:** those five rows. Their plants are the variable number kept in the signature, and the name left
  out of it.
- **Decision:** open. **Change class:** one-way.

### B2. The log's lines: what is still not fixed

- The draft fixes the header, the dense records, the end record and its causes, the chain and `input-log-sha256`.
- **It does not fix how a value encoding is written on an ASCII line.** RUNTIME-SPEC §5's encodings are bytes.
  Proposed: each value as the lowercase hex of its encoding, separated by single spaces, with a record line beginning
  `t <tick>`. That is exact and leaves no second spelling.
- **Strongest objection:** hex is unreadable to a person debugging a session. **Answer:** the door's report shows the
  values as text; the log is for machines.
- **Decision:** open. **Change class:** one-way.

### B3. The budget's bytes (R9)

- **Proposed rule:** R5's law line `(tick <clause> budget <N>)`, with N decimal, 1 ≤ N ≤ 2^63 − 1. Its semantics are
  the draft's §4.3.
- **Required observable result:** the budget is in the law's bytes, so the law seal covers it.
- **Falsifying test:** two laws differing only in N with the same seal (plant: the budget kept out of the law line).
- **Decision:** open with R9. **Change class:** one-way.

### B4. R2's line forms: three parts each, and one invariant

- Every new form is a clause of code: a port, a tick block, a tick block with a budget. So the door classifies each as
  code, and the parser parses it or refuses it with its code (PORT-PLACE, TICK-PLACE, PORT-VARIABLE, SYNTAX).
- **Proposed rule:** for each form, its recognition, its parse or refusal, and its door classification are written
  down together. A door–parser split is refused at compile time (the debate's D11). The indented `Note:` is the one
  split today. One frozen text reaches it through the door's own repair: E18's leading NBSP becomes a space before the
  marker is read. The repair moves E18 from QUOTE-BOUNDARY to LINE-FORM, a change to settle in COMPAT-0
  (`probes/door_canon_probe.py`).
- **Falsifying test:** for each form, a row at column one and a row indented. The plant is the door's `lstrip`
  restored.
- **Decision:** open with R2. **Change class:** one-way for the spellings; two-way for the guard.

### B5. The receipt's statuses and one more field

- **Proposed rule:** receipt 1's `status` line takes four forms: `COMPLETED`, `REFUSED <CODE> <clause>`,
  `NOT-RUN <t> <cause> <port>` and `LOG-OPEN`. The court must read all four; today it parses only the first two.
- **Added here:** a field `tick-ops <n>`, the last begun tick's own count, complete or partial. Without it, a refused
  tick's count is readable only from the trace's last `'T'`; with it, the receipt alone shows the reviewer's
  attempted-operation count. Under TICK-BUDGET it is exactly N+1.
- **Falsifying test:** a TICK-BUDGET receipt whose `tick-ops` is not N+1 (plant: the refused operation left uncounted).
- **Decision:** open. **Change class:** one-way.

## Round C: refusal, claims and operation counts

### C1. §8.4 measured on version 0

**MEASURED here,** twice with byte-identical output (`evidence/run1-completeness.txt`). The run covers every claim of
COMPAT-0's frozen texts, the court's fixtures and the examples that ran: 89 claims.

| | count |
|---|---|
| held by the court as built | 68 |
| withheld by §8.4 | 1: `tests/fixtures/court/hoisted_omit.orl` §2.2, "true in 16 of 16", WELL-FOUNDED today |
| held or support gained | 0 |
| plants caught, each by its own case | 2 of 2: "never withhold" on `hoisted_omit`; "no loop back edge" on a claim before the refusal in a loop with passes left |

So the rule changes no frozen text's reading. It withholds exactly the reviewer's case, and it is one-sided on this
set.

### C2. The site-based rule withholds a completed claim

- **MEASURED here** (a scratch case, not in the tree; DECLARED until written as a fixture). A procedure is performed
  twice:
  - its claim, `n is positive`, runs in both calls;
  - the second call refuses after the claim (INDEX-OUT-OF-RANGE at §3.3);
  - the court as built reads "true in 2 of 2", held;
  - §8.4 withholds it, because the end of the procedure returns after every `Perform`, so the first call's return
    reaches the second call;
  - nothing could evaluate the claim again, since the refusal came in the last call.

  This is exactly what the reviewer warned against: a completed proof withheld because its source location could be
  reached in another execution.
- **The cause:** reachability that ignores the actual call path. The receipt names only the refusing clause, not the
  stack of `Perform`s active at the refusal, nor the passes a loop had left.
- **Proposed refinement, with two ways to carry the instance:**
  - (i) receipt 1's REFUSED status names the call path, `via <clause> …`. This is one-way and cross-checked by all four
    executions.
  - (ii) the court recovers the call path by replaying the reference. It changes no format, but it is a
    reference-only fact.

  Either way, reachability returns only along the actual path. A `For` whose remaining count is known at the refusal
  takes its back edge only if passes remain.
- **Recommendation:** (i), since the court should not hold a fact that only one execution states. It must be decided
  in Round B's bytes, because it fixes receipt 1's status line.
- **Superseded the same day by CUT-0.** A call path is not enough: C2′ and C5 in `CUT-0.md` turn on a loop's
  remaining passes, with no call at all. The court needs the cut: each frame's clause, a bit per loop, and the
  open-claim mark. Every execution computes it at the refusal and commits it in the `'R'` event, so it is not a
  reference-only fact.
- **Falsifying test:**
  - the call-twice case reads held;
  - a refusal in the first of two calls withholds;
  - a claim before the refusal in a loop with passes left withholds;
  - the same claim in the loop's last pass holds.

  The plants: context-insensitive returns; no back edge; ignoring the remaining count.
- **Decision:** open. **Change class:** one-way under (i), two-way under (ii).

### C3. A gap in §8.4: NOT-RUN and LOG-OPEN also cut a claim off

- **The gap:** §8.4 speaks only of a run that ends REFUSED. A claim in the tick block of a NOT-RUN or LOG-OPEN run held
  in every tick that ran, but another tick could have come and refuted it.
- **Proposed rule:** for both outcomes, treat the end of input as a refusal at the tick block's head. Claims of the
  tick block, and of procedures performed in it, are cut off. PREFIX claims are not, since a tick cannot reach them,
  which is the owner's R6 settlement again. COMPLETED with the cause `closed` cuts nothing off.
- **Falsifying test:** a tick-block claim in a LOG-OPEN run that reads held. The plant is §8.4 applied to REFUSED
  alone.
- **Decision:** open. **Change class:** two-way (a court reading).

### C4. `'T'`, the budget, and the three-tick example as a fixture

- `'T'` carries the count from the start of the run (the draft's §4.2). The (N+1)-th operation of a tick is counted,
  then refused before it runs (§4.3), as SPEC §7 counts every operation "immediately before".
- The worked example in `CONTRACT-DEBATE.md` (D8) becomes, in 1a, an executable input vector checked against the three
  identities of §7.2. That vector holds a prefix, two ticks and a TICK-BUDGET tick, plus a variant refused by another
  code.
- **Decision:** open. **Change class:** one-way (the payload's meaning).

### C5. The reviewer's six cases

The adversary attacks §8.4 with them in Round D, from the written rule alone. This record does not pre-empt that work,
except for C2's case, which is the reviewer's case (iv) shaped as a procedure.

## Round D: the independent attack, and its disposition

`ADVERSARY-ROUND-D.md` holds 26 findings against `CONTRACT-DRAFT.md`: 9 decide a one-way format, 13 change a verdict
and 4 are wording. Its author read only the draft, SPEC.md, RUNTIME-SPEC.md and version 0's code. Its measured items
were rerun here before any was conceded:
- `work/run-1-adversary/measure.py` reproduces its recorded output byte for byte;
- `receipt_cores.py` on the three spellings reproduces Finding 23's one differing core line, `text-seal`;
- `state_probe.py` reproduces Finding 9's flags.

Its scripts sit in `work/`, which git ignores, so from the tree they are OBSERVED; the four claim fixtures this
disposition leans on are inlined in `probes/cut0_claims.py`.

| # | finding | disposition |
|---|---|---|
| 1 | the input log's record bytes are unfixed; Int 10's encoding holds an LF byte (MEASURED, reproduced) | **accepted.** One line per record, `tick <t>` (and `once` for the read-once record, always written). Each value is the lowercase hex of its RUNTIME-SPEC §5 encoding; a record's hashed bytes include its LF; the header is three lines. `probes/cut0_session.py` holds the same grammar for fixed ports. *Corrected 2026-10-26: that sentence is wrong. The probe writes `t`, not `tick`, has no `once` line, and writes each value as the 16 hex digits of its raw 64 bits, with no RUNTIME-SPEC §5 tag byte; its port signature knows only `fix each-tick` (`probes/cut0_session.py`, `serialize` and `parse_log`). It holds the header, one line per record and the end record, not this grammar (`packets/D-LOG-refusals.md` §1).* |
| 2 | the arrival log records none of the host's decisions; the smallest collapse pair is "assign then close" against "close first" | **accepted**, and answered by CUT-0 §3, derived independently: assignments, drops, closes and the end are events of the history, and a log that is not its history's projection is HISTORY-MISMATCH |
| 3 | an arrival's raw bytes can forge a record; no chain, no size bound, no field for the door's verdict | **accepted.** An arrival's bytes are written in hex, at most 2^24, a longer arrival refused INPUT-RANGE and kept as its length and sha256. The history is chained, with its head at every close. Each arrival carries the door's verdict and notes |
| 4 | a read-once port's refusal or absence has no rule | **accepted.** Tick 0 is the read-once record; the session starts only when it closes complete, and otherwise ends `not-run 0`. *Ruled otherwise 2026-10-27: finding 6, A′ (`RULINGS.md`). The prefix runs up to the first read-once declaration and stops there when the log lacks the read-once record; the bytes of that stop are finding 8's.* *Note 2026-10-26: `not-run 0` clashes with row 5's t = n+1, which gives 1 when no tick record precedes it, and the probe models no read-once port, so this disposition was never checked. Packets C and D (`packets/`) leave its bytes open and its meaning to the owner (finding 6 of the R7 review).* |
| 5 | the end record can name any tick and port | **accepted.** t = n+1, and the port is the first missing in declaration order: the strict grammar checks t, and HISTORY-MISMATCH checks the port against the projection |
| 6 | `'T'` and `'N'` have no fixed bytes | **accepted, the adversary's repair.** `'T'`: the tick block's clause, payload u64 t then u64 c, big-endian. `'N'`: the port declaration's clause, payload u32 variable id then the value encoding |
| 7 | the budget is not in the law's bytes; its range is unstated | **accepted** (B3). Range, for the owner: the adversary's 1…2^62 with N = 0 for no budget, matching `While`'s FUEL grammar, or B3's 1…2^63−1. This record leans toward the adversary's, for one numeral grammar |
| 8 | port names and type spellings are free, so two port lists can share signature bytes | **accepted.** Names `[A-Za-z][A-Za-z0-9_]*`; types `int`, `fix`, `bool`, `text` in the signature |
| 9 | the tick line's fields are under-fixed; a certificate's cost counter lies outside the state digest (flags MEASURED, reproduced) | **accepted, the adversary's repair.** `events` and `output-bytes` are running totals. `claims` is the SHA-256 of the claim lines with their LFs. `state` covers every top-level variable, the ports included, then every certificate counter |
| 10 | checking the whole log first and streaming conflict; `input-log-sha256`'s bytes; "rests on input log" for a run that read none | **accepted, with one change.** Offline, the whole log is checked before the first statement; live, the host appends only checked records, so the log is always a valid prefix. `input-log-sha256` covers every byte. The court states dependence only when an `'N'` or a `'T'` was emitted, since a tick block with no port consumes input by its length. *Note 2026-10-26: this last sentence conflicts with ruled R6, whose trigger is the law's (it declares a port or has a tick block), not an emitted event. A run that ends NOT-RUN on a missing read-once value emits neither and still has an input log (`packets/C-read-once-ports.md` §3 A). R6 governs where they differ.* |
| 11 | a concatenation's k−1 counts in one lump, so a budget crossing is ambiguous (MEASURED, reproduced) | **accepted.** Counted one at a time for the budget. The total is unchanged, so no version-0 receipt changes |
| 12 | the tick block's own count is unstated | **accepted.** The tick block counts no operation of its own |
| 13 | the clause an arm's count belongs to is unfixed (MEASURED, reproduced) | **accepted.** The arm's clause, as version 0 already gives an arm's condition |
| 14 | an each-tick port can be read before tick 1 binds it | **accepted as a gap in R2**, with two repairs for the owner, since R2 is his. (a) The adversary's: each-tick ports are declared as the tick block's first clauses. (b) R2's top-level declaration kept, with any read of an each-tick port outside the tick block refused at compile time (PORT-READ-PLACE). This record leans to (b): R2's spellings stand, at the cost of one compile rule |
| 15 | a text port admits LF, bidi controls and oversize texts | **accepted.** A text port admits exactly what a text literal may hold, within TEXT_MAX: anything else is INPUT-TEXT, above 2^24 bytes INPUT-RANGE. The ASCII grammar does not apply to text |
| 16 | the door's grammars and their precedence are unwritten | **accepted.** Each grammar written out, with the adversary's numerals as a starting point. The truth spellings are R3's open detail, for the owner |
| 17 | A1 against A2 | **agreed: A2**, with Finding 2's records (CUT-0 §3). Its one remaining failure, silence ending the session, is a language question: an optional port whose closed-empty value is a recorded absence. Proposed for later, not here |
| 18 | PREFIX's textual test grants a false GROUNDED through a procedure performed from another procedure (stand-in MEASURED, reproduced) | **the defect is accepted; the adversary's repair is rejected.** Its repair is dynamic: exempt when every `'C'` precedes the run's first `'N'`. That lets whoever chooses the log choose the standing. The counterexample, hand-worked for version 1: a claim in procedure `check` is performed in the prefix, and in the tick block only when `n equals 7`. On a log without 7 the dynamic test exempts it, and it is GROUNDED if ratified; on a log with 7 it is evaluated again and refuted. The standing depends on the log, which R6 forbids. **The repair proposed instead is static closure.** A claim is PREFIX if and only if it lies outside the may-execute closure (`Reach` in `probes/cut0_claims.py`) of the top-level clauses from the first input point on: the first read-once port declaration, or the tick block, whichever comes first. Procedures performed from there are included transitively. It is sound; it excludes d04; and it mends the other direction the adversary found, since an each-tick port's declaration is not an input point. *Note 2026-10-26: the boundary proposed here is wider than ruled R6, whose licence requires a claim to stand before the first port declaration of either kind, outside the tick block, and not in a procedure performed at or after it. Under this row an each-tick declaration is no boundary, so a claim after one is licensed (the review's P13). The row was written after R6 was ruled. Adopting its boundary would amend R6; its static closure alone interprets R6 (`packets/B-PREFIX.md` §2 and §3.1).* |
| 19 | the site rule applies to REFUSED runs only | **answered by CUT-0:** NOT-RUN and LOG-OPEN cut at the tick block's head |
| 20 | the tick block's back edge reaches past a closed log's last tick | **answered by CUT-0:** the tick block's frame bit, exact with Finding 10's whole-log reading |
| 21 | returning after every `Perform` withholds completed claims (d03, d11) | **answered by CUT-0,** MEASURED: d03 and d11 are held |
| 22 | the site rule's scope over version 0 (d02, d08) | **answered:** CUT-0 applies to every run, version 0 included. Measured one-sided over COMPAT-0, no frozen reading changes; d02 and d08 are withheld by E2's standard, d08 conservatively |
| 23 | §9.1 is false: `text-seal` is in the core (MEASURED, reproduced) | **accepted.** T1 now reads "given the text's bytes", since the core names the text seal |
| 24 | the count identity is undefined with no `'T'` | **accepted.** With no `'T'`, `ops` is the prefix's count: the session probe's row `no-T-ops-is-the-prefix` |
| 25 | no court label for a claim the rule withholds | **accepted.** "Cut off by the refusal at §s: not held (CUT-0)", and its certificate's cost reading NOT READ |
| 26 | the site rule's graph edges are undefined at an If chain and a `Perform` | **moot under CUT-0:** K̂ comes from the frames, and `Reach` takes an If chain as one unit |

**What the round changed.**
- Three findings (19, 20, 21) were already answered by CUT-0, which neither side had seen. That is the independent
  agreement the reviewer asked for, not a confirmation.
- Finding 18 found a real defect and proposed a repair that is itself unsound.
- The rest are bytes and rules the next draft must fix.

## The theorem ledger: every mathematical statement the design rests on, as a proof obligation

The owner asked that every mathematical theorem the design was built over be named, since each may deserve
refining. The reviewer asked that they become proof obligations rather than a catalogue: each with a status that
never substitutes for another, a falsifier, and whether the contract as drafted depends on it.

The statuses:
- **PROVED here:** a written argument in this file or `CUT-0.md`, checked by a person, not by a proof assistant;
- **EXHAUSTIVE:** checked for every case of a declared finite domain;
- **MEASURED:** a run on named inputs;
- **ESTABLISHED:** read in the code or the specifications;
- **DECLARED:** argued, not checked;
- **CONJECTURED:** stated without a proof;
- **ASSUMED:** taken as an axiom of the design.

| # | statement | status | falsifier | the contract depends on it | refinement it may deserve |
|---|---|---|---|---|---|
| T1 | **Replay.** A run is a function of the text's bytes (so its law), the input log's bytes and the semantics version; a toolchain is not a hypothesis. Corrected from "the law's bytes" by Round D's Finding 23 (MEASURED): the core names the text seal | DECLARED; MEASURED per session by four-way agreement, once built | two conforming executions whose cores differ under one law, log and version | yes, centrally | state it in two stages: the session's history projects to the input log (EXHAUSTIVE in the model, `cut0_session.py`), then the input log determines the run. ASSUMED under it: no clock, environment or entropy reaches a runtime (RUNTIME-SPEC §1); floats across hosts are NOT_MEASURED |
| T2 | **Alignment.** Equal port signatures replay an old log tick for tick | DECLARED; its premise MEASURED (B1: the variable number moves) | an unrelated `Let` that changes the signature; a semantic change that does not | yes (R10) | its hypothesis is signature equality. Reordering ports changes the signature on purpose, because records are positional; that is to be ruled, not left to serialization |
| T3 | **Tick termination** | ESTABLISHED by construction | a tick that does not end | yes | refine to "ends within a computable B(law)"; B can reach about 2^63 operations, so it is no usable time bound |
| T4 | **Capability.** A law reads only its declared ports | ESTABLISHED once built (a compile-time refusal) | an undeclared port read that compiles | yes | — |
| T5 | **The neighbour lemma.** With range checked before grid, every grid refusal has two in-range neighbours | PROVED (the debate's D7); MEASURED (0 of 210,115; the plant 10,007) | an off-grid value within the bounds with a neighbour outside them | yes (R3's refusal message) | ASSUMED: exact arithmetic, the 2^-32 grid, and **bounds that are grid points**. A declared port range must keep its bounds on the grid, or the lemma is proved again |
| T6 | **The count identities.** The `'T'` differences are the tick lines; `'T'(1)` is the prefix; `ops − 'T'(last)` is `tick-ops`; a TICK-BUDGET tick counts N+1 | PROVED (a telescoping sum); EXHAUSTIVE in the model (30,610 histories) | a trace breaking one identity; a budget tick not at N+1 (plant caught) | yes (R5, R9) | say that a run cannot reach 2^64 operations, by the host budget or a static bound, rather than leave the overflow unstated |
| T7 | **The chains commit and localize.** The first differing link locates the first difference | DECLARED; standard under SHA-256's collision resistance | two different prefixes with one link | yes | ASSUMED: collision resistance. A chain commits; it proves nothing about meaning. Every chain's start is domain-separated (`orlog-trace-1`, `orlog-output-1`, `orlog-inputs 0`, `orlog-history 0`) |
| T8 | **Withholding never raises a standing.** For base′ ⊆ base: lfp′ ⊆ lfp, gfp′ ⊆ gfp, and so each claim's standing (well-founded 2, circular 1, else 0) never rises | **PROVED here** (below); EXHAUSTIVE against the court's own `support_sets` for every premise graph of up to 3 claims (13,974 cases) and 20,000 sampled 4-claim cases: 0 violations | the plant, a withheld premise read as no premise: 4,464 violations; smallest, two claims, `{0: [0], 1: [0]}`, 0 withheld, and 1 becomes well-founded | yes: every one-sided measurement (R6, R8, CUT-0) is now a check of the code against this lemma | it holds for a court that computes support only from base and premises. A rule that edits premises, as the plant does, needs its own proof |
| T9 | **PREFIX soundness.** A claim whose evaluations all precede the first input has a claim line independent of the log | PROVED from T1: the run up to the first input is a function of the law | a PREFIX claim whose line moves with the log | yes (R6) | define "the first input" as the first `'N'`, or the first `'T'` when the law has no port. *Note 2026-10-26: under the PREFIX ruling (`RULINGS.md`) the licence is decided statically, from the boundary and the closure, so T9 needs a static form, graded DECLARED, resting on a new obligation: the closure over-approximates what every version-1 statement kind may execute (`packets/B-PREFIX.md` §5). The trace's "first input" stays a check, never the rule.* |
| T10 | **Completeness by the cut (CUT-0), under reading S2** (every later refusal passable; only a For's normal exit exact). A claim not open at the cut, which the cut's continuation cannot evaluate, has all the evaluations the run could make | ARGUED construct by construct (`CUT-0.md` §2's table); MEASURED on version 0 (19 cases, 95 claims, R8's exact class 5 of 5, plants 9/9, the instrumentation identical to the reference in 933 runs with 290 host stops); the manifold adversary's oracle found no counterexample under S1 in 20,000 random laws, and every S2 one was the While bit F1 repairs | a claim held whose site the continuation reaches; a completed claim withheld where it provably cannot; a refusal caused by an input that raises a standing (F1) | yes, if E2 and CUT-0 are ruled. *E2 ruled 2026-10-26 (the claims ruling, `RULINGS.md`); 1a admits the meet R8 ∧ CUT-0* | the argument needed two repairs on the day it was written (C6, then F1): a proof sketch is not a proof. Conservative for a While's condition, for If conditions after the cut, and for loops whose later passes cannot reach the claim by value. Sound, not complete. The NOT-RUN, LOG-OPEN and tick-block rows are DECLARED until version 1 runs |
| T10.0 | **T10 by row (split by the owner's claims ruling, 2026-10-26).** T10 holds when T10.1 to T10.6 hold (and T10.7 and T10.8 from version 1), the rows cover every statement kind, and the cut records the frames exactly. *T10.8 named 2026-10-27 by re-read 4's T10-1; this note moved out of the statement by re-read 5's T10-1.* | the rows: DECLARED. The coverage: ESTABLISHED by reading `src/orlog/syntax.py` against `CUT-0.md` §2's table. The capture: MEASURED, the instrumented reference identical to the reference in 933 runs. Across the rows: no oracle counterexample in 88,950 refused runs (`manifold/VERDICT.md`) | a statement kind no row covers; a frame recorded otherwise than the run stood | yes: E2 is ruled, and 1a admits the meet | each row is proved or waived on its own. The precision figures below are family G's claims held by that row alone, from `probes/disagree_probe.py`: precision, never soundness |
| T10.1 | **The rest of a block.** When a frame's statement ends, the run goes on with the next sibling that is not an absorbed Otherwise, and at the block's end with the owning frame. K̂ adds everything those siblings may execute, with values ignored | DECLARED (`CUT-0.md` §2, "a sequence of clauses") | a claim evaluated after the cut in a later sibling, and not in K̂ | yes | precision: 739 claims held by it alone, 159 unreached (21.5%). The excess is conditions after the cut |
| T10.2 | **The refused If.** A condition refused at arm i leaves arms i onward and the Otherwise able to run. The arms before i read false in this pass | DECLARED; plant `all-arms` (F3) caught | an arm before i evaluated in the same pass after the cut | yes | precision: 52 alone, 5 unreached (9.6%) |
| T10.3 | **A For.** Below the top, it repeats exactly when its bit says passes remain. Its bounds are evaluated once, at entry (ESTABLISHED, `interp.py`'s For). Refused at its own clause, its body follows | DECLARED; plants `no-count` and `header-bit` caught | a pass run after one whose bit read no passes remain | yes | precision: 1,231 alone, 88 unreached (7.1%); the loop's own clause refused, for For and While together: 3,435 alone, 312 unreached (9.1%). The residue is arms that cannot reach the claim by value (D08) |
| T10.4 | **A While.** Under S2 it always may repeat: its condition is unknown, and its fuel check is a passable refusal. Refused at its own clause, its body follows | DECLARED; the F1 repair; plant `while-bit` caught | a refusal caused by an input that raises a standing through a While (F1's shape); a later pass outside K̂ | yes | **the owner's priority for precision:** 803 alone, 450 unreached (56.0%). A sharper reading of the condition must stay sound: no row may trade soundness for precision |
| T10.5 | **A Perform.** On the stack, a procedure returns only to the frame below it, the actual caller. Since there is no recursion, each procedure has at most one activation on the stack (its Perform's frame and the frames of its body's statements, nested ones included), so the cut, whose arm selector names an inline arm's own frame, names each call without ambiguity. Reached in the continuation, its whole body counts, transitively. Refused at its own operation (version 1 only), its body follows. *(Reworded 2026-10-26 by the twin's finding 42: "since there is no recursion" had been given as the reason for the return, which holds on any stack; what it supports is the uniqueness. Reworded again 2026-10-27 by its re-read, T10.5-1 to -3: "one frame" became "one activation", the arm selector is named, and this note moved after the statement. And by its second re-read, T10.5-4: nested statements' frames named.)* | DECLARED; plants `context-free` and `shallow-reach` caught | a claim evaluated after a return to a caller other than the frame below; a procedure's body cut at a depth | yes | none measured: no version-0 disagreement is held by a Perform refused at its own operation |
| T10.6 | **The open claim.** A claim whose evaluation is open at the cut is withheld, named by its id, since two claims can share a clause (F2) | DECLARED; plants `no-open` and `descriptor-no-id` caught | an open claim held | yes | — |
| T10.7 | **The tick block (version 1; added 2026-10-26 by `SPEC-15-DRAFT.md`'s review).** Below the top, the tick block may run its body again, since another tick may run. At NOT-RUN t or LOG-OPEN, when the law declares no read-once port or its log holds the read-once record, the cut is the tick block's head before tick t, and K̂ is the tick block and every procedure performed from it; in a law with no tick block, K̂ is empty. *Scoped 2026-10-27 by finding 6's ruling (re-read 3's F6-3), the scope moved into the statement by re-read 4's T10-3; the read-once stop is T10.8; the law with no tick block added 2026-10-29 by re-read 10's S15.13-1.* | DECLARED (`CUT-0.md` §2's outcome table); not built, not measured | a claim of the tick block evaluated at a later tick and not in K̂; a NOT-RUN or LOG-OPEN run holding a tick-block claim | yes, from version 1 | its bytes wait for the format freeze: the tick block's frame is not yet in the cut's schema. *Added 2026-10-26 by the twin's finding 43:* the row depends on §15.1.3, which makes the tick block the last top-level clause and is open (the amended set's "port place", whose ruling finding 43 also needs). With the log parsed whole (§15.5 of draft 1), no load refusal happens at a tick, so the tick block is never on top for that reason. Ports and the tick block in T10.0's "every statement kind" wait for the version-1 schema |
| T10.8 | **The read-once stop (version 1; added 2026-10-27 by finding 6's ruling, re-read 3's F6-3).** At NOT-RUN or LOG-OPEN with the read-once record absent (never at a refusal before the first read-once declaration, RO′-4's case, whose cut is the refusal's own), the cut is the first read-once declaration, a top-level frame not begun, and K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored; its withholdings name the row "the read-once stop". *Scoped 2026-10-27 by re-read 4's T10-2; this note moved out of the statement by re-read 5's T10-1.* | MEASURED on version-0 stand-ins only (`packets/F-read-once-adversary.md` §4); DECLARED for version 1, not built | a claim the row holds that the same law evaluates again after the stop over a log that supplies the record | yes, from version 1 | his answer of 2026-10-27: a version-1 check of this row is owed before CUT-0's digest is pinned (a deferral, not evidence). *Added 2026-10-27 by his answer on re-read 5's Q1:* the check is a test on fixtures, run by the version-1 reference before the pin; any claim outside K̂ falsifies containment, and a pass is MEASURED on those fixtures only, closing neither containment over every log nor this row. Its premises rest on open clauses: the top-level place of read-once ports (§15.1.3) and binding counting no operation (§15.7.1) |
| T11 | **COMPAT-0's preservation.** New forms are recognized only where version 0 refuses SYNTAX at the statement, so no accepted text changes meaning | MEASURED on 3,361 texts; DECLARED in general | an accepted v0 text whose law bytes or run change under v1 | yes | **owed: a proof over SPEC §13's phase table.** It must enumerate every transformation that can change acceptance, refusal, canonicalization or meaning (the door's repairs, the parser's line forms, the analyzer's phases), say which preserve behavior and which change it on purpose, and show that a v1 form is reachable only from a v0 SYNTAX refusal at that statement |
| T12 | **The cost of deciding dependence:** coNP-complete for straight-line code; PSPACE-complete with procedures (the doppler verdict) | the first, cited (Yasuoka & Terauchi 2010); the second **CONJECTURED**. The verdict: *"a bound the survey derived itself and found in no publication"* | a proof error; a polynomial algorithm on a class claimed hard | **no**: R6 stays strict, so the contract does not depend on it | record its assumptions (runs total, values bounded, no recursion) and write the proof before any design leans on it. No relaxation of R6 may cite it until then |
| T13 | **One-sidedness** of R6, R8, §8.4 and CUT-0 | follows from T8 | a withholding rule that raises a standing | yes | none: T8 is proved |
| T14 | **The four statuses partition every outcome** | PROVED by case analysis on (a refusal, an end record, its cause); EXHAUSTIVE in the model (30,610 histories) | an outcome satisfying two predicates or none | yes | — |
| T15 | **The session's projection.** The input log is a function of the history, the door replays, and a log never pairs with another history | EXHAUSTIVE in the model (one port, 6 events, 4 values); the named cases MEASURED (12 of 12, plants 5/5) | a history with two projections; a log accepted with another history (HISTORY-MISMATCH) | yes, if A2 is ruled | the model is one or two ports and a stand-in law. Version 1 must hold the same rows over Orlog's own door and execution |
| T16 | **A static budget bound** (a later fork) | DECLARED | a proven law that refuses TICK-BUDGET | no | must count every If's worst arm, every rule's worst path, and an `and` or `or` counted after its left operand |
| T17 | **Incremental state commitments** (a later fork) | DECLARED | — | no | name the assumption before choosing (a tree: collision resistance; LtHash: a lattice assumption) |

**T8's proof.**
1. Let step_B(X) = { c ∈ B : premises(c) ⊆ X }. It is monotone in X, and B′ ⊆ B gives step_B′(X) ⊆ step_B(X) for
   every X.
2. **Least fixed points.** step_B′(lfp_B) ⊆ step_B(lfp_B) = lfp_B, so lfp_B is a pre-fixed point of step_B′. The
   least fixed point is the least pre-fixed point (Knaster–Tarski), so lfp_B′ ⊆ lfp_B.
3. **Greatest fixed points.** gfp_B′ = step_B′(gfp_B′) ⊆ step_B(gfp_B′), so gfp_B′ is a post-fixed point of step_B,
   and gfp_B′ ⊆ gfp_B.
4. **Standings.** If a claim is well-founded after, it is in lfp_B′ ⊆ lfp_B, so it was well-founded before. If it is
   circular after, it is in gfp_B′ ⊆ gfp_B, so it was at least circular before.
5. **The court's computation.** It iterates from the empty set and from the full set over finite sets. For a monotone
   step that reaches the least and greatest fixed points.
6. **Grounding.** It is the same least fixed point with base held ∧ ratified, so it falls under the same argument. ∎

## The decisions for the owner, held for one push

Every one of these is open, and they are pushed together, as he asked.

The manifold debate is judged (`manifold/VERDICT.md`). The manifold view does not earn a place as a method, but the
debate produced three things:
- the adversary's 13 findings, repaired where they reproduced (`probes/PROBES.md`);
- a resumption oracle that finds no counterexample to CUT-0's continuation in 88,950 refused runs;
- a log congruence for the session's rows.

Nothing in it is settled until he rules.

| item | proposed | change class |
|---|---|---|
| A1, A3 | the session history (arrivals, door verdicts, assignments, drops, closes, the end, chained) as its own record; the end record's cause; four statuses as exclusive predicates (CUT-0 §3) | one-way |
| A2 | A2, judge then assign, with the declared policy, END-PENDING and END-UNDISPOSED, in place of the reviewer's earlier (a) | one-way |
| binding | two layers: the receipt core attests the run over its input log; the session record binds history, log and core | one-way |
| B1, D-8 | the port signature without the variable number; identifier names; the types `int`, `fix`, `bool`, `text` | one-way |
| B2, D-1, D-3 | one line per record, values in lowercase hex; arrivals in hex, bounded; the strict canonical grammar | one-way |
| B3, D-7 | the budget in the law line; its range, 1…2^62 with N = 0 for none, or 1…2^63−1 | one-way |
| B4, D-14 | the three-part contract per form; the door–parser split refused; an each-tick port's place, (a) or (b) | one-way and two-way |
| B5, D-6, D-9 | four statuses; `tick-ops`; the bytes of `'T'` and `'N'`; the tick line's fields | one-way |
| C4, D-11, D-12, D-13 | `'T'` cumulative; the (N+1)-th counted, one at a time; the tick block counting nothing; an arm's count to its clause | one-way |
| E2, CUT-0 | a claim's standing by E2; CUT-0's one rule under reading S2, in place of R8's readings, the site rule, the NOT-RUN and LOG-OPEN extension and the PREFIX settlement; the cut (each frame's clause, a `For`'s bit, a refused If's arm, the open claim's id) in the `'R'` event | one-way (the `'R'` payload) and two-way (the court) |
| session, G1–G7 | sources in the history; RUN-REFUSED (nothing after the run refused but the end); the end cause set by the policy (INPUT-MISSING alone under A2); `fullmatch` in every grammar; the no-port record; no value invented | one-way |
| H2, E18 | the door reads `Note:` and `Title:` at column one, as the parser does; E18 settled in `tests/compat/settled.json` (QUOTE-BOUNDARY to LINE-FORM) with its reason and amendment, and its self-test row changed | one-way (a frozen text's refusal code) |
| D-18 | PREFIX by static closure from the first input point, not by the trace. *Ruled in part 2026-10-26 (`RULINGS.md`, the PREFIX licence): the static closure, started from R6's boundary. D-18's boundary, the first read-once declaration or the tick block, is not adopted.* | two-way |
| D-4, D-10, D-15, D-16 | tick 0 for read-once ports; whole-log checking; the text door; the door's grammars | one-way |
| T5, T11, T12 | the neighbour lemma's grid-bound assumption kept; T11's proof over the phase table owed; T12 a conjecture the contract does not lean on | — |
| F1–F8 (`FLOAT.md`) | bitwise reproducibility of everything committed, with no tolerance and no "same decisions, different intermediates"; determinism is not accuracy; exact decisions in the domain's own unit; floats as T5 has them; R8 b kept until HOST-0; certified enclosures later, as a library in the law; no guarantee ladder; a model proposes and the verifier decides | two-way (F6, F7, F8); one-way where they fix what is committed (F1, F4) |
| unread records | the receipt counts the tick records left unread after a refusal (`manifold/VERDICT.md`) | one-way |
| off-gate | the resumption oracle and the log congruence kept off-gate, for 1a's checks | — |

**Before the push** (the outside reviewer's conditions, which this record adopts):
- each line above, once ruled, is recorded as either a normative ruling or an implementation recommendation;
- H2's repair is made only with its COMPAT-0 settlement and E18's self-test row;
- T11 stays open and T12 stays a conjecture;
- the self-test and COMPAT-0 are run on the exact tree to be committed, and the staged diff is read before the commit.

**Run on 2026-10-26** (`evidence/run1-gate-before-push.txt`), on 95dac79 with no change under `src/`, `tests/`,
`examples/`, `vectors/`, `rt_c/`, `rt_rs/` or `orl.py`: **COMPAT-0 HELD** (3,361 the same, 0 differing) and **ORLOG
SELFTEST 210/210** (python, c99, rust). The push adds research and records only, none of which either check reads.
The staged diff is still to be read before the commit.

## The outside review of the held decisions, and the amended set (2026-10-26, late)

The owner forwarded a long review: proposed dispositions, clarifications (an F9, a `backends` field, a refusal
threshold, a memory bound), a critique of those clarifications, and a revised disposition. It is the reviewer's text,
so it is paraphrased here, and none of it is recorded as the owner's ruling.

Its general rule is adopted, because it is the reporting pass's own lesson stated as a rule: **every authoritative
report names its claim, the evidence it binds, the authority that made it, its version, and the condition on which it
passes or fails, and it attests nothing outside its authority.** Each point was checked against the code and the
records, and four are disproved by them.

| # | the review's point | disposition | the basis |
|---|---|---|---|
| 1 | a `backends` field in the receipt core | **rejected; the agreement belongs to the arbiter.** A receipt cannot attest which other executions ran. HOST-0's falsifier is "any differing receipt core" across hosts, so host identity in the core would make every second host differ by construction. The core stays portable. The arbiter's agreement record (today its witness, whose integrity line names the agreeing executions, `court.py:232`) binds the compared cores' digests, each execution's build identity (H1's envelope) and the verdict. Host context goes in the session record | ESTABLISHED (`court.py`, `research/roadmap-debate/VERDICT.md` §2) |
| 2 | a refusal threshold, counted in the input log and refused at parse; `door-refusals` and `threshold-triggered` in the receipt | **rejected as located.** The input log holds only accepted values; refusals live in the session's history (CUT-0 §3). A receipt is a function of its input log, so those fields would report what it cannot know, which is the review's own rule. No threshold is in the held decisions. If one is wanted, it is a host policy recorded as history events (a source barred after k refusals), with its own rows, never an execution outcome | ESTABLISHED (`probes/cut0_session.py`) |
| 3 | "A2's resilience is false at the parse layer: the strict parser refuses malformed logs" | **rejected: two different objects.** An *arrival* is any bytes, judged by the door. A malformed arrival (`x`, `1.1`, bytes that are not UTF-8, an LF inside) is refused and the session goes on. The strict parser reads the *input log*, the history's projection or a log offered whole for an offline run. A malformed log is refused before execution, because no session exists for it. The scope, stated plainly: A2 governs every arrival; a log offered whole is checked whole before execution | MEASURED (cases S1, H, G2 of `probes/cut0_session.py`) |
| 4 | "T11 open while the unified rule ships is a soundness debt: ship the four predecessors" | **rejected in its premise; the principle is kept.** T11 is COMPAT-0's preservation over the phase table, not CUT-0; CUT-0's obligation is T10. Nothing ships: CUT-0 runs only in research probes, and the court as built runs R8. The "four predecessors" are one built rule (R8) and three drafts. One of the drafts, the site rule, is measured to withhold completed claims (C1, D03, D11), so shipping them means shipping known imprecision. The real choice for 1a is whether to implement CUT-0 with T10 graded DECLARED (argued) and MEASURED (88,950 refused runs), the debt named in DOCTRINE and the oracle a gate row. The principle stands: the operative rule must be unambiguous, and its tests must test it | ESTABLISHED (the ledger; `src/orlog/court.py`) |
| 5 | the resumption oracle and the congruence kept off-gate is backwards | **accepted: they become self-test rows in 1a.** Their independence was assessed, not assumed. The oracle computes what a resumed run evaluates by executing the reference with substituted values, while K̂ is computed statically. They share only the frame capture, which the oracle checks against the plain reference. Its limits stay written beside it: the refusal kinds it models, and its two families | MEASURED (`manifold/VERDICT.md`) |
| 6 | HOST-0 has no corpus, threshold or failure disposition | **partly rejected; two additions accepted.** HOST-0 is defined: the corpus programs' receipt cores, outputs and trace heads, the vectors and the self-test's summary, with predictions frozen before the run, on x86-64 and ARM64. It fails on "any differing receipt core, output byte or vector", and its control is the naive C FMA loop, which must still diverge on ARM. **Added:** the 3,361 frozen texts to its corpus. **Added:** a failure disposition: T5 is falsified off this host, float ports stay deferred, the witnesses are kept, and a repair or a versioned restriction is ruled before HOST-0 runs again | ESTABLISHED (`research/roadmap-debate/VERDICT.md` §2) |
| 7 | a registry of refusal codes, since R8 keys on "any code but CLAIM-REFUTED" | **accepted for 1a.** The reference emits 18 runtime refusal codes, with 16 more at compile, and none is classified (MEASURED by reading `interp.py`, `numeric_ref.py` and the `OrlogError` codes). Each code gets a class: an evaluation refused, a claim's own verdict, a statement's verdict, or the host. A row checks that every emitted code is registered and classified. Its plant: an unregistered code must fail closed. R8 and CUT-0 dispatch on the class | MEASURED (`court.py:73`) |
| 8 | a memory bound on the session record | **rejected for RUN-1.** It is not in the held decisions; it came from the reviewer's own clarification. The history grows only by events the host chooses to append. A bound, if ever wanted, is a host policy recorded as an end cause, with its precedence among the other endings written first | — |
| 9 | the speed figures are stale | **accepted, with the scope.** P13's 4.3–4.4% measured the tick line with the fields the speed verdict proposed. `tick-ops` and the unread count are receipt-level, not per tick. The input chain proposed for the tick line (the debate's D3) adds a hash per tick and is unmeasured. If it is ruled, P13 runs again before the play tier relies on the figure | ESTABLISHED (`research/speed/VERDICT.md`) |
| 10 | transcendentals can only be identified, never certified | **accepted as a distinction; the absolute is corrected.** Identity (the same algorithm, constants and operations) gives bitwise conformance between backends, and nothing more. Accuracy can be checked without circularity on samples, against an independent computation of higher precision: Verðandi's `rules_ref.py` measures its `sin` against 70 decimal digits, and its `sqrt` and `hypot` are correctly rounded by exact integer arithmetic, checked against the midpoints. What no finite test gives is a bound over every input, which needs a proof | ESTABLISHED (Verðandi's `graybox/README.md`) |
| 11 | a rolled-back tick may vanish; the orphan is unruled | **rejected: R4 rules it.** *"The refused branch is kept, sealed and queryable."* Before SNAP-1 there is no rollback at all: a refusal ends the session. A 1a row adds that a refused branch stays queryable | ESTABLISHED (`RULINGS.md`, R4) |
| 12 | the court's summary sets `grounded` beside `claims`, inviting a ratio | **accepted, by the mechanism that exists.** The summary already carries `forbidden_interpretations`. "grounded over claims is a score" joins them, and the layout stays | ESTABLISHED (`court.py`, the summary) |
| 13 | 64 files in one commit defeat bisection | **accepted.** The lineage's evidence atomicity puts code, evidence and records each in its own commit. This push has no `src/` change. H2's repair comes later, in its own change, with its settlement | — |
| 14 | F9: compatibility is a measurement | **accepted; COMPAT-0 already works this way.** It names every changed text with its reason and amendment, and refuses an uncovered text (`tests/compat/README.md`). F9 adds the wording: a report measures; RULINGS.md says which outcomes are allowed | ESTABLISHED |
| 15 | F4: record a transcendental's algorithm and provenance | **accepted as identity metadata** in the admission record, under point 10's limit | — |
| 16 | the budget's boundary | **accepted.** N is 0 (no budget) or 1…2^62, and anything larger is refused. A tick's count never exceeds N+1 ≤ 2^62+1, so it fits in i64 by construction. Rows: N = 1; N = 2^62, which parses; N = 2^62+1, refused; and N = 0, where a bounded run asserts that no TICK-BUDGET occurs | DECLARED |
| 17 | `'T'` must not count toward its own budget | **accepted as a row for 1a.** Events are not operations: SPEC §7 counts operations, and binding a port counts 0 (D5) | ESTABLISHED (SPEC §7) |
| 18 | option (b) is "the only way" to enforce N-1 | **the decision is kept; the exclusivity claim is dropped.** (b) is chosen for its design benefit, not as the only possibility | — |

### The amended set, for the owner's ruling

Each item is marked by what kind of thing it is, as the reviewer asked:
- **N:** a normative ruling;
- **I:** a requirement on 1a's implementation;
- **R:** research, which nothing in the program reads.

| item | kind | proposed |
|---|---|---|
| A2 | N | judge before assigning, with the declared policy; every arrival in the history; a log offered whole is checked whole before execution. No threshold in RUN-1. *2026-10-27: finding 6 is ruled (A′, `RULINGS.md`); its N2 (an `end()` before the read-once record closes) and N3 (when the host runs the statements before the first read-once declaration) are left to this row.* |
| budget | N | N = 0 (none) or 1…2^62, anything larger refused; the (N+1)-th operation counted, then refused, one at a time. Rows: point 16 |
| port place | N | (b): declared at the top level; any read outside the tick block refused at compile time, with rows and broken variants |
| session record | N | its own record: sources, door verdicts, assignments, drops, closes and the end, chained; END-PENDING, END-UNDISPOSED, RUN-REFUSED; one disposition per arrival |
| binding | N | three records with three authorities: the portable receipt core (one execution over its input log); the session record (the history and the host's context); the arbiter's agreement record (the compared executions, their identities and the verdict) |
| identity and bytes | N | the port signature without the variable number, identifier names and fixed type spellings; `orlog-inputs 0` one line per record in hex, versioned and strict; the bytes of `'T'` and `'N'`; four statuses; `tick-ops`; the count of unread tick records |
| counting | N | `'T'` cumulative from the run's start; the tick block counts nothing; an arm's count to its clause; events are not operations |
| claims | N | **three options, after the fork (`FORK.md`):** (c), recommended: the court admits R8 (E1) and names its rule digest, the cut is recorded in the `'R'` event from 1a on, and CUT-0 (E2) is an experimental settlement parameter, compared by delta class and admitted only by a later ruling; (a) CUT-0 admitted, with T10 graded DECLARED and MEASURED and the debt named in DOCTRINE; (b) T10 proved first. Under every option the cut's bytes in `orlog-trace-1` are 1a's. *Added later the same day: a fourth, (d), now recommended over (c): the court admits the meet R8 ∧ CUT-0, never above R8 and resting on no T10, with CUT-0 alone the target (`SETTLEMENT-DEBATE.md`).* **RULED 2026-10-26: (d), with E2 as HELD's meaning (`RULINGS.md`, the claims ruling).** |
| PREFIX | N | by static closure from the first input point; every consumer of `Reach` states its own soundness requirement. **RULED 2026-10-26: B1 + 4a + 5c + K1, the closure failing closed, an independent structural oracle, and D-18's boundary not adopted (`RULINGS.md`, finding 24 and the PREFIX licence).** *2026-10-27: the labels' definitions (not their conclusions) and the closure's rule table ruled (`RULINGS.md`).* |
| H2 | N, then I | the door reads `Note:` and `Title:` at column one, landed only with E18's COMPAT-0 settlement and its self-test row, in a change of its own |
| codes | I | the refusal-code registry, with its exhaustiveness row and plant |
| gate rows | I | the resumption oracle and the log congruence, with their independence written down |
| HOST-0 | N | as defined, plus the frozen texts and the failure disposition (point 6) |
| F1–F9 | N | `FLOAT.md`, with F1 scoped to a declared execution profile, F6 bounding each operation on its own, F9 compatibility as measurement, and the transcendental limit (point 10) |
| reporting | N | the authority rule above, and "grounded over claims" added to the forbidden interpretations |
| T10, T11, T12 | — | T10 argued and measured, not proved; T11 open; T12 a conjecture nothing leans on. *Since the claims ruling: T10 split by row (T10.0 to T10.6), each open* |

**This push holds research only:**
- records, probes and evidence, in three commits; *since then five: the owner's claims ruling in a commit of its own,
  and the court records' privacy scrub (F42) in another*;
- the owner's rulings, quoted, in the records commit;
- no change under `src/`.

Every N item becomes 1a's work: specified in SPEC §15, then built, with its rows.

## The last pass, and the roadmap's order (2026-10-26, late)

The owner forwarded two more outside texts:
- a last adversarial pass over the amended set;
- a ruling on the roadmap verdict's ranked steps (`research/roadmap-debate/VERDICT.md`).

Both are the reviewer's, paraphrased here, and neither is the owner's ruling. The first finds the amended set **ready
for the owner's decision, not a claim that every obligation is closed**. This record agrees.

**The four pressure points, checked:**

| point | finding | basis |
|---|---|---|
| A2: one disposition per arrival | **already the model's semantics.** A retry is a new arrival with its own disposition (S1), assigning a refused arrival is illegal ASSIGN-REFUSED (S1′), and the plant that assigns one is caught. A refused arrival never becomes the accepted value | MEASURED (`probes/cut0_session.py`) |
| T10 and CUT-0 | **unchanged: the owner's choice.** 88,950 refused runs are evidence, not the theorem. Either implement CUT-0 with T10 graded DECLARED and MEASURED, the debt and its owner named in DOCTRINE, or prove T10 first | the ledger |
| HOST-0's profiles | **accepted:** the execution profiles (each build's identity) are frozen in the agreement record before the run, and a mismatch is classified at its first differing committed event, which the per-event chain localises (R5). **One clarification:** the receipt core holds no field that depends on a profile, because its one host-specific line, `backend`, is the line `receipt_core` removes. A differing core is therefore always a committed difference | ESTABLISHED (RUNTIME-SPEC's receipt; `arbiter.py`, `receipt_core`) |
| the budget's rows | **already in the set** (the review's point 16): N = 0 under a bounded run, N = 1, N = 2^62, and N = 2^62+1 refused | — |

**One correction to the review:** the vectors leave **9** lines without an independent derivation, not five. All 9
are SHA-256 lines: two are checked against published digests, and the runtimes' own SHA-256 code is held to all of them
(`evidence/vectors-independent.txt`).

**The roadmap's order.** The review keeps the verdict's ranking. HOST-0 comes second, before RUN-1's formats freeze,
the owner moved it there, and the verdict reads: *"run v0's baseline now, before RUN-1 freezes receipt 1 and the input
encodings, so that a difference between hosts changes a seal nothing yet rests on."* Its three qualifications are
accepted, and each already has a place:
- **COMPAT-0 is a gate, not a theorem.** That is T11, kept open.
- **HOST-0 never relaxes byte equality into a tolerance.** That is F1. A differing host means an implementation is
  repaired, or the contract is revised under a new version.
- **RUN-1 keeps four outcomes apart:** a malformed arrival, a refused arrival, a law's refusal, and a host's stop. The
  first two are the door's, in the history; the third is the run's, in the receipt. The fourth already writes no
  receipt at all: "the law said nothing, so there is no receipt and no event" (`src/orlog/interp.py`, `HostStop`).

**One omission in its order:** R7, the twin's paper round on §15, sits between the rulings and 1a's code and is still
unruled.

**The order, then:**
1. The owner rules the amended set, T10's choice and R7.
2. HOST-0 runs on the owner's second machine, ARM64 among the hosts, before §15 freezes anything.
3. §15 is drafted.
4. The twin's paper round runs (R7, if ruled).
5. 1a builds the reference, with its rows: the code registry, the oracle and the congruence among them.
6. Then 1b and the backends; then LEDGER-1, SNAP-1, SESSION-0 and RPC-0, in the verdict's order.

## The reviewer's proposed 1a ruling, and the format's four conditions (2026-10-26, late)

The outside reviewer proposed a ruling for 1a. It is paraphrased here, and it is a proposal, not the owner's ruling:
- R8 is the default and the sole admitted settlement rule;
- CUT-0 is experimental only, and never available to ordinary admitted runs;
- the cut is recorded directly, as its decision-relevant frame fields;
- the R6 and PREFIX rulings stand, and HELD is never conflated with GROUNDED;
- R8 and CUT-0 read the same evidence. Each difference carries a direction, a finding reference and a disposition,
  and an unexplained one blocks adoption;
- T10 is proved or explicitly waived by the owner, and a waiver is never a proof;
- a historical reading keeps its rule label, and later readings are appended;
- R7 stays a separate decision.

It would not freeze the cut's format until four conditions hold.

**In substance, this is the claims row's option (c), with the format's freeze made conditional.** HELD and GROUNDED
are already kept apart. GROUNDED requires a ledger line ratifying the claim's own seal (`src/orlog/court.py`), and R6 a
keeps every claim of the tick block from it.

| the condition | where it stands (`CUT-SCHEMA.md`) |
|---|---|
| the schema derived from CUT-0's rule as written | done (§1). It changed the bytes: draft 2 carries a For's bit only below the top and an If's arm only on top, with no flag byte |
| each field's removal reproducible and tied to a decision | done (§3): four witnesses, each a claim of a named case whose standing flips |
| only valid canonical encodings accepted | done for the form (§2, §3): canonical by structure, seven shape rules, 0 accepted outside the shapes over 390,498 byte mutations and 2,858 frame forgeries. A well-formed cut that the run never produced is still accepted |
| a compatibility policy for existing records | proposed (§4, P1–P7). No version-1 record exists, so nothing existing changes |

**Found in answering them:**
1. **Draft 1 carried values the rule never reads**, and its decoder accepted states no run reaches. Of its 15 accepted
   single-byte mutations, one was such a state. On frame forgeries, 74 of its 157 accepted lay outside the shapes.
2. **The form proves a cut well-formed, never that it happened.** Of the 15 single-byte mutations draft 2 accepts, 14
   would change a standing. Only the executions' agreement over the receipt core holds a cut to its run. A single host
   can forge a consistent one.
3. **An open question for the contract.** `CONTRACT-DRAFT.md` 4.3 refuses TICK-BUDGET "at the clause whose statement
   is executing". It does not say which clause an If's condition operation names: the head's, or the arm's, as
   version 0's refusals inside a condition do. The cut's event check (S6) depends on the answer. Nothing is decided
   here.
4. **The cut is a twin surface under every option.** It is in the receipt core, so every backend must compute the
   same frames.

**What the owner is asked is unchanged:** the amended set, the claims option (the reviewer's proposal is (c)), and
R7. The format's freeze is a later ruling of its own, due before the first version-1 receipt is frozen anywhere
(P6).

## What replaces the reason CUT-0 was built: the meet (2026-10-26, late)

The owner asked: *"If CUT-0's a research only candidate then what replaces why we started out building it?"* Then:
*"Debate that design."* The debate is `SETTLEMENT-DEBATE.md`. It covers the forwarded texts: the successor's status,
the settlement rule as auditable state, and a stratified court.

**Its answer is a fourth claims option, (d): the court admits the meet R8 ∧ CUT-0, and CUT-0 alone is the target.**
- The meet never holds or supports a claim above R8. Holding follows by definition; support follows by T8, and the
  probe measures it again: 0 of 192,894 claims (`probes/meet_probe.py`, `evidence/run1-meet.txt`).
- So the meet rests on no T10, and a forged cut gains nothing over R8.
- It delivers CUT-0's tightening, the reason CUT-0 was built: 43,356 claims R8 holds and CUT-0 withholds, over 79,520
  refused runs.
- It forgoes CUT-0's gains: 7 claims (A23, A23′, and five in family G).
- The count does not yet split justified tightenings from CUT-0's conservatism. The resumption oracle can.

**The selector witness that the forwarded debate called a defect** was a valid ablation, presented unevenly. It is
repaired: the plant now drops the field from the bytes, and the rerun holds (`CUT-SCHEMA.md`).

**The stratified court:** its interfaces are kept, and the rest is not adopted now.
- K0 is not smaller than the court: 8 modules, 3,088 lines, MEASURED.
- The rule does not fit the language.
- Self-application is vacuous under grounding by ratification.
- Signatures need a dependency.
- Verðandi's pinned trusted base is the part worth porting.

**What the owner is asked:** the amended set, the claims option (now (a), (b), (c) or (d), with (d) recommended), and
R7. Under (d), what HELD means in version 1 is his to rule: R8's held, less what the cut's continuation could evaluate
again.

## The disagreement set, classified (2026-10-26, later)

The forwarded critique of (d) and the replies to it agreed on one thing: measure the 43,356 tightenings before any
ruling. The measurement is `probes/disagree_probe.py` (`evidence/run1-disagree.txt`), and its reading is
`SETTLEMENT-DEBATE.md` §7. The resumption oracle resumes each run with the refusing operation returning each of eight
values, under reading S2:
- **REFUTED: 1,968 (4.5%).** Evaluated again and found false. R8's HELD is contradicted.
- **CONFIRMED: 40,141 (92.6%).** Evaluated again and true in every resumption. Here E1 and E2 differ on meaning alone.
- **UNREACHED: 1,247 (2.9%).** Evaluated again in no resumption. This is CUT-0's conservatism, concentrated in the
  While row.

Set family E aside, whose only claim cannot be false, and the split is 22.3%, 63.6% and 14.1% of 8,833. CUT-0's 7
gains are all UNREACHED, so the oracle agrees with each. Every disagreement is held by one or more of CUT-0's own five
rows: the measured "patterns" are its rows.

**The question this leaves the owner is what HELD means, E1 or E2:** 92.6% of the disagreements turn on it alone.
- Under E2: (d), pinned to CUT-0's digest, each withholding naming its row.
- Under E1: R8 stays, and CUT-0 is a report printed beside HELD.

Either way, the cut is recorded, and T10 is split by row.

## E2's meaning, sharpened (2026-10-26, later)

The reviewer recommended E2, and so did a longer reply the owner marked as his recommendation, not a ruling
(`SETTLEMENT-DEBATE.md` §8). Three corrections came out of answering them:
- **E2 is already claim-relative.** A claim is withheld only when its own evaluation is in K̂, never because other
  work is pending.
- **The 40,141 CONFIRMED claims are in K itself**, since a resumption evaluated each one again. So E2 withholds them
  by definition, and a better K̂ releases none of them. Only a different meaning could: settling a claim whose truth
  no continuation can change. That is a stronger rule needing an inductive invariant per claim. It is not proposed for
  1a.
- **E1's descriptive fact needs no new field.** Every reading already prints "true in k of k evaluations"
  (`court.py` 287).

The question is unchanged: what HELD means for version 1, E1 or E2.

## Ruled: the claims question (2026-10-26)

The owner ruled E2 as the meaning of HELD for version 1, and option (d): the meet R8 ∧ CUT-0, pinned to CUT-0's
exact digest, each withholding naming its row, with CUT-0 alone the target. His words are in `RULINGS.md` (the
claims ruling), and DOCTRINE §9 fork 4 refers to them. T10 is split by row above (T10.0 to T10.6), with the While row
first for precision; T10 and T11 stay open. The amended set's other rows and R7 are still his to rule.

## The held push: what remains, and how each condition closes (2026-10-26, late)

The owner's word: *"Wait for the amended set and R7. Do not push the four commits yet."* The push waits for three
things: the amended set, R7 and the format freeze resolved, and then the gate passing on that exact tree. The privacy
scrub made the set five commits.

| condition | what closes it | where it stands |
|---|---|---|
| R7 | *Ruled 2026-10-26 (`RULINGS.md`): (a), one independent review of the draft with triggered re-reads. The review is run as ruled: its reading set in `twin-r7/MANIFEST.md`, its report in `twin-r7/REPORT.md` (58 findings, provenance clean), disposed in `twin-r7/DISPOSITION.md`: 31 drafting defects for draft 1, 24 for the owner alone (29 reaching a ruling), 2 for the ledger, 1 moot; 5 block the round. Draft 1 (`SPEC-15-DRAFT-1.md`) applies the 31 drafting fixes, decides no ruling, and owes the twin a re-read of its 74 changed or added clauses (`twin-r7/DRAFT-1-CHANGES.md`).* *Corrected 2026-10-26: the row's earlier text (R7 still to rule, (a) recommended, the round unable to run before this push) is superseded by his ruling.* The re-reads are a build condition in his words (*"no §15 clause built before the required review"*), not a push condition | **ruled**; the review run and disposed; the re-reads owed after each ruling, before anything is built |
| the amended set | **his ruling** on its 12 normative rows (A2, budget, port place, session record, binding, identity and bytes, counting, PREFIX, H2, HOST-0, F1–F9, reporting) and its 2 implementation rows (codes, gate rows). The claims row is ruled. *2026-10-26: the PREFIX row is ruled too (`RULINGS.md`).* | open: 11 normative rows and the 2 implementation rows remain. *2026-10-27: each deferred to a ruling before 1a's build by his release ruling (`RULINGS.md`, "The release"; `RELEASE-DECISIONS.md` §4).* |
| the format freeze | **a ruling:** freeze draft 2 now, or defer the freeze to `CUT-SCHEMA.md` P6's trigger (before the first version-1 receipt is frozen anywhere), after the version-1 schema with its tick block and ports is derived and 4.3's TICK-BUDGET clause question is settled | open. Recommended: defer to P6's trigger, which settles the question without freezing a format not yet derived for version 1. *2026-10-27: deferred to P6's trigger by his release ruling (`RULINGS.md`, "The release").* |
| the five commits | each file in exactly one commit | **checked by a dry run:** 95 files, each in one commit (36, 22, 17, 2 and 18), none from `work/`, nothing staged. *Rechecked 2026-10-26, with `research/run-1/packets/*.md` added to commit 3: 118 files, each in one commit (37, 28, 33, 2 and 18), none from `work/`, nothing staged.* *Rechecked 2026-10-27, with drafts 2 and 3 added to commit 3 as well: 131 files, each in one commit (38, 28, 45, 2 and 18), none from `work/`, nothing staged.* Only the last commit's tree is meant to be consistent, and the gate runs on it |
| F42 | the notes agree | **checked:** the court records' notes, the verdict's F42 row and STATUS all say the current files are scrubbed and that history through 95dac79 holds the paths |
| the gate on the final tree | COMPAT-0 and the self-test, then every probe rerun and compared with its evidence, headers aside | owed after the rulings. The earlier run (`evidence/run1-gate-before-push.txt`) is a historical record. *Noted 2026-10-26: its comparison rules (timings, outputs run once, CR, the seconds printed, `make_laws.py` writing into the tree) and where its own record goes are not yet written (`packets/E-release-gate.md`, risks 10 and 11).* |
| evidence closure | every recorded output reproduces on the final tree, or is labelled as of an earlier form | **found before the gate:** each probe's own evidence is newer than the probe (draft 1's is marked superseded). The manifold adversary's seven outputs were rerun on this tree: `s_drop` reproduces byte for byte. Six differ because they record the attack on CUT-0's first form: the repairs show through (the open claim's id in the descriptor, F2; a While read under S2, F1; the session log's trailing space, G1; 26 spent-bit counterexamples now 0). `k_monotone` crashes on the repaired probe, since its snapshot frame lacks the `arm` key that F3 added. With that one key supplied by a wrapper (the file untouched), its result reproduces: 0 violations over 12,581 refusing laws and 125,063 earlier points. *Done the same day (`manifold/adversary/RERUN.md`).* The six are kept as the first form's record, with current-tree reruns beside them, each run twice and identical. Every changed outcome is tied to its repair, by plant where one exists. Three scripts carry dated compatibility fixes: `k_monotone.py`, `k_repairs.py` (whose A23 rows read DIFFERS against per-claim requirements) and `s_attacks.py` (which crashed on G6's refusal and printed the checkout's path). One change is explained but not tied to a single repair: `s_attacks`' domain sizes, whose rows hold in both runs |
