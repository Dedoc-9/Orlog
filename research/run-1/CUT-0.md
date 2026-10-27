# CUT-0: the causal cut, and the session as one transition system (2026-10-26)

**Status: a proposal, supported by research probes, not settled.** Nothing here is ruled, built into `src/` or
committed, and nothing in the program reads it. The owner asked that the final decisions wait for one push.

*Ruled since, 2026-10-26 (`RULINGS.md`, the claims ruling).* E2 is the meaning of HELD for version 1. 1a's court
admits the meet R8 ∧ CUT-0, pinned to CUT-0's exact digest, and CUT-0 alone stays the target. T10 is split by row in
`ROUNDS.md`. The rest of this file stands as written.

The outside reviewer's last reply set four points that block a push:
- binding the receipt to the history (§3);
- the unfinished-tick loophole (§3);
- an adversarial log parser (§3);
- a justified continuation (§2).

Two adversaries have attacked this proposal since: Round D's (`ADVERSARY-ROUND-D.md`) and the manifold debate's
(`manifold/ADVERSARY.md`). Every finding of theirs that reproduced is repaired here, and each repair is held by a case
and a plant. The measurements are in `research/run-1/probes/` (`PROBES.md` indexes them), and their outputs are in
`evidence/`. They are evidence for a proposal, never proof that a contract holds. The reviewer is paraphrased, never
quoted.

Prior art, from memory and not re-read here:
- consistent cuts of distributed computations (Chandy and Lamport);
- continuations, and abstract interpretation's over-approximation;
- event sourcing's commands and events;
- lockstep scheduling in networked games.

No mechanism is claimed as new.

## 1. What the claim rule governs

**An evaluation's result is a fact, and it is never withdrawn.** "True in k of k" names k completed evaluations, each
true, and the court keeps reporting them.

**The rule governs a claim's standing, which is an aggregate:** whether the claim is held (and so its support and its
grounding), for the claim's id over the whole run. Three readings of that aggregate were possible:
- **E1, every completed evaluation:** held when every completed evaluation is true. This is the court as built, R8
  aside, and it holds `hoisted_omit.orl`'s claim, cut off after 16 passes.
- **E2, every evaluation the run could still have made:** held when every completed evaluation is true, none is open
  at the cut, and the run's continuation at the cut could not evaluate the claim again.
- **E3, the last evaluation:** rejected, because it reads a loop's earlier refutations as irrelevant.

**Proposed: E2.** No rule here governs an individual evaluation. A later rule that needed one would name an
evaluation by its position among the trace's `'C'` events for its claim.

## 2. The causal cut, its continuation, and the one rule

**The cut** is the run's dynamic position when it stops, recorded as the stack of statements executing, outermost
first:
- **a `For`:** whether passes remain. This is exact, because its bounds are evaluated once, at entry.
- **an If chain whose condition refused:** which arm's condition it was.
- **a `Claim` whose evaluation is open:** that claim, named by its id.

**The continuation K** is everything the run could still have executed had the refusing operation returned. It reads
every later refusal as passable too: this is **reading S2**. Values are unknown and refusals are ignored. Only a loop's
normal exit is exact, which means a `For`'s counter against its bound. K̂ is what CUT-0 computes, from the frames
outward.

**Why S2.** The manifold adversary's F1 showed that the first form mixed two readings:
- lower `While` frames were read as stopping at their fuel check;
- the top one was read as passing it (the C6 repair).

So a refusal caused by an input could raise a claim's standing. In F1, a `While`'s last allowed pass refuses on
`d = 0` and holds its claim. One literal apart, with `d = 1`, the run reaches the fuel check and withholds it, and the
pass behind that check would refute the claim. Read S2 everywhere and an earlier refusal can never raise a standing:
the adversary's cut-monotonicity check over 20,000 random laws finds 0 violations under this repair. *(Rerun on
the repaired tree, 2026-10-26: 0 violations over the 12,581 refusing laws and 125,063 earlier points,
`manifold/adversary/k_monotone-20000-current.txt`.)*

**The rule (CUT-0):** a claim is held when every completed evaluation is true, it is not open at the cut, and it is
not in K̂.

| outcome | the cut | K̂ |
|---|---|---|
| COMPLETED | after the last statement | empty |
| NOT-RUN t, or LOG-OPEN (version 1) | the tick block's head before tick t | the tick block, and every procedure performed from it |
| REFUSED inside tick t (version 1) | as below | as below; the tick block's frame may repeat, since in a live session the host stops because the run refused (§3, RUN-REFUSED). Only an input log fixed before execution began, whose end record the run read first, makes "no later tick" exact |

**The invariant: K̂ ⊇ K under S2.** Each construct of version 0 is argued below. ESTABLISHED by reading
`src/orlog/interp.py` and `src/orlog/syntax.py`. DECLARED as a whole: it is argued and sampled, not proved
mechanically. It needed two repairs on the day it was written (C6, then F1), and a proof sketch is not a proof.

| construct | what follows it in the language | what K̂ adds | why K̂ covers it |
|---|---|---|---|
| a sequence of clauses | the next sibling that is not an absorbed Otherwise; at the block's end, the owning frame | everything the remaining siblings may execute, every arm and body inside them included | values are ignored, so every path through them is included |
| an If chain | a condition refused (the If on top): that arm onward, or the Otherwise. Inside an arm: when it ends, the chain completes | the arms from the refused one onward, the Otherwise included; or the chain's following siblings | the arms before it have read false in this pass. A later pass re-enters the chain whole, through the loop |
| `For` | another pass exactly when its counter is below its bound | refused in the body: the body, if passes remain. Refused at its own clause: the body | the bit is exact, and the refused operation guards the next pass |
| `While` | another pass while the condition holds; a pass past its fuel is refused FUEL-EXHAUSTED | always the body, whether the refusal is at its own clause or inside it | S2: the condition is unknown and the fuel check is a passable refusal (F1, C6) |
| `Perform` | the procedure's body, then a return to that Perform | on the stack: a return only to the frame below, the actual caller, unique because there is no recursion. Reached in the continuation: the whole body, transitively. Refused at its own operation (version 1): the body | the frames record the actual call; procedure bodies are finite and recursion-free |
| `Claim` | its evaluation, which may refuse partway | open at the cut: that claim, by its id | R8's two readings (exact and possible) become one. Two claims can share a clause (F2), so the claim is named by id, never by clause |
| an inline statement in an arm | it runs in its If's frame | nothing between: frames of the same clause are one position | — |
| a rule use (`Define`) | an expression evaluated inside the using statement | nothing of its own | a rule holds expressions only (`Define(name, expr, proviso, overrides)`), and its refusal names the using clause, whose frame is on top |
| `Must`, `Let`, `Set`, `Increase`, `Decrease`, `Say`, `Append`, `Remove`, `Decimals` | the next sibling | the sequence's | no body |

**The assumptions it rests on:**
- version 0 refuses recursion, and control is structured, with no jump;
- `Stop` is raised only by `refuse` (`interp.py:109`, its one raise);
- the frames are captured exactly. The instrumented reference writes the same receipt, the same trace line for line
  and the same host stop as the reference in all 933 runs (MEASURED). That covers every runnable text of COMPAT-0, the
  fixtures, the examples and the cases, each at its own budget and at a third and two thirds of its run. 290 of those
  runs are host stops. The first form skipped the reference's host-budget check at a loop's entry (F4). Its
  equivalence had held only because the corpus never stopped a run there.

**Where K̂ is larger than K (sound, not complete):**
- a `While`'s condition;
- the conditions of If chains after the cut;
- loop passes whose arms cannot reach the claim by value. The Round D adversary's D08 is withheld for this reason.

### MEASURED on version 0

Run by `research/run-1/probes/cut0_claims.py`; output in `evidence/run1-cut0-claims.txt`; twice byte-identical.

| case | the cut | site rule | CUT-0 |
|---|---|---|---|
| C1: two calls; the second refuses after the claim | `5 3.3` | withheld | **held** |
| C1′: one literal apart; the first call refuses | `4 3.3` | withheld | withheld |
| C2: a loop refused at pass 17 of 20, the claim first | `2+ 2.2` | withheld | withheld |
| C2′: one literal apart; refused at pass 20 of 20 | `2. 2.2` | withheld | **held** |
| C3: nested calls; inner's second call refuses after the claim | `5 4.2 3.3` | withheld | **held** |
| C3′: one literal apart; inner's first call refuses | `5 4.1 3.3` | withheld | withheld |
| C4: the claim's own evaluation refuses, on the last pass | `2. 2.1!0` | withheld | withheld |
| C5: a claim in an arm of pass 1, refused at pass 20 of 20 | `2. 2.2` | withheld | **held** |
| C6: a `While` refused FUEL-EXHAUSTED | `2w` | withheld | withheld |
| D02, D03, D08, D11 (Round D's fixtures) | — | withheld | withheld, held, withheld (conservative), held |
| F1: a `While`'s last allowed pass refuses on `d = 0` | `3w 3.3 3.3` | withheld | withheld (held before the F1 repair) |
| F1′: one literal apart, `d = 1` | `3w` | withheld | withheld |
| A23: two claims on one clause, the second open | `3. 3.1 3.1!1` | withheld, withheld | **held**, withheld |
| A23′: one literal apart, the first open | `3. 3.1 3.1!0` | withheld, withheld | withheld, **held** |
| A09: an Otherwise-if condition refuses on the last pass | `2. 2.1?1` | withheld | **held** |

How to read the cut: each frame's clause, outermost first. `+` is a `For` with passes left and `.` one without; `w`
is a `While` (S2 needs no bit); `?n` is the If arm whose condition refused; `!n` is the open claim's id.

- **Every case reads as required (19 of 19).**
- **Three pairs, each one literal apart, that the site rule reads alike and the cut tells apart.** A23's two cuts
  differ only in the open claim's id: the manifold adversary showed that a descriptor naming only the clause cannot
  tell them apart (F2).
- **Plants, each caught by its own cases (9 of 9):**
  - context-insensitive returns: C1, C3, D03, D11;
  - a `For` that always repeats: C2′, C5;
  - an open evaluation not seen: C4;
  - a loop's own refusal read through its bit: C6;
  - a `While` below the top read through its fuel bit: F1;
  - every arm of a refused If: A09;
  - a descriptor without the claim's id: A23 and A23′;
  - the host-budget check skipped at a loop's entry: a law whose budget is spent before its `While`;
  - a reach cut at a procedure performed inside another, the lineage report's under-approximation: L1.
- **Over the 95 claims of COMPAT-0's frozen texts, the court's fixtures and the examples:**
  - the cut withholds what the site rule withholds, which is one claim, `hoisted_omit.orl`;
  - it withholds all 5 claims of R8's exact class, without consulting R8;
  - the 2 claims of R8's possible class stay withheld, because their own evaluation was open;
  - it gains nothing over the court as built.

  A gain is allowed only when R8 read "possible" and the frames show that another claim was open. A23 is that case,
  and an unexplained gain fails the probe.

**What the court needs, and no more:** each frame's clause, a `For`'s bit, a refused If's arm index, and the open
claim's id.
- A bare call path is not enough: C2′, C5, C6 and F1 turn on loops, with no call at all.
- Naming the open claim by its clause is not enough either: F2.
- Full dynamic identities for every evaluation are not needed for the standing.

*Refined later on 2026-10-26 (`CUT-SCHEMA.md`, draft 2): read from this section's own table, the rule needs a For's
bit only below the top, and an If's arm only on top. The open claim's id is read from the top frame's statement, which
holds one claim. The paragraph above stands as written.*

**Where it would live:** every execution computes the cut at the refusal, so it belongs in the `'R'` event's payload.
There the trace head commits it, and the trace head is in the receipt core, so all four executions must agree on it.
That is a choice of bytes in `orlog-trace-1`: one-way, and the owner's.

**Does not show:**
- soundness beyond the cases;
- the version-1 rows, which are DECLARED;
- `Reach` on version 1, which PREFIX's static closure would share: a statement kind it does not name adds
  nothing to the closure. That is complete for version 0, whose other statements (Let, Set, Change, Say, Must,
  Append, RemoveLast) hold neither a claim nor a Perform (read from `src/orlog/syntax.py`, not run), and fails
  open for a tick block added without its own case (noted 2026-10-26, `packets/B-PREFIX.md`, headline 5);
- any law outside version 0.

The manifold adversary's independent oracle runs a refused law on with substitute values (`manifold/adversary/
cont_oracle.py`). It can refute K̂ but never confirm it. It found no S1 counterexample in 20,000 random laws; its
S2 counterexamples were all the `While` bit that F1 repairs.

The proponent's resumption oracle (`manifold/resume_oracle.py`) makes the hypothetical run the definition names: the
refusing operation returns with a substituted value, and the reference goes on. It was judged in
`manifold/VERDICT.md` and rerun by the judge, matching its record line for line.
- **No counterexample to K̂.** In 88,950 refused runs, no claim was evaluated after the cut outside K̂, and no claim
  K̂ holds was evaluated again. That holds both under R1 (only the first refusal passable) and under Rinf (every
  refusal passable). The runs are 61,879 EXHAUSTIVE over a declared grammar and 27,071 from 10,000 random laws.
- **The plants are caught:** 10 of 10 unsound plants in K̂ and 3 of 3 in the oracle.
- **The first form failed through one door only:** the spent fuel bit, 96 random runs, before its author had read F1.

This is evidence, not proof: it covers version 0, the refusal kinds the oracle models, and its two families.

## 3. The session as a transition system

Run by `research/run-1/probes/cut0_session.py`; output in `evidence/run1-cut0-session.txt`; twice byte-identical. A
session's history is a sequence of events, and S_{n+1} = δ(S_n, e_n) is the only way its state moves:

| event | legal when | effect |
|---|---|---|
| `arrive(port, source, bytes)` | the session has not ended and its run has not refused; the port is declared | numbered in order, with its source (G5); the door judges it at once |
| `assign(arrival, tick)` | as above; the arrival was accepted and has no disposition; the tick is the open one; its port's slot is empty | it fills the slot |
| `drop(arrival)` | as above; the arrival was accepted and has no disposition | it is declined, and its source is told |
| `close()` | as above | the open tick runs if every each-tick port is filled, and the session runs it at once. Otherwise NOT-RUN with the first missing port in declaration order, and the session ends |
| `end()` | the open tick holds no assignment (**END-PENDING**), and every accepted arrival is assigned or dropped (**END-UNDISPOSED**). After the run refused, `end` is the only legal event and needs neither | the session ends, cause `closed` |

Any other move is refused by its rule's name: ASSIGN-REFUSED, DROP-REFUSED, DISPOSED-TWICE, ASSIGN-CLOSED,
ASSIGN-AHEAD, SLOT-FILLED, AFTER-END, UNKNOWN-PORT, NO-ARRIVAL, or **RUN-REFUSED**. After the run refuses, nothing is
legal but the end (G6). A host could otherwise keep closing ticks the run never reads, and a record nobody read would
decide whether the tick block may repeat.

- **A tick that has begun to fill is closed, never discarded** (the reviewer's loophole: case S8, plant
  `end-anytime`, and the exhaustive row `no-assignment-disappears`).
- **Every arrival has exactly one disposition**, derived from the history alone: refused with its code, assigned to
  its tick, dropped, or unconsumed because the session ended first.
- **No value is invented** (the row G4 proposed). Every value in a tick record is the door's value for that
  (tick, port)'s assigned arrival. Plant `hold-previous` breaks it, on named cases and in the exhaustive search.

**Three records, and the binding between them (the reviewer's first point, chosen explicitly):**

| record | binds | attests |
|---|---|---|
| the input log, `orlog-inputs 0` | the history's projection: port signature, door version, tick records, end record and cause | what the law reads |
| the receipt core, `orlog-receipt 1` without its backend line | `input-log-sha256`, and the run's results | a run over that input log, and nothing about the session. Two histories with one input log share it: **law-equivalence** |
| the session record, `orlog-session 0` | `history-sha256`, `input-log-sha256`, `receipt-core-sha256` | the session, its sources included: **session provenance** |

**Both layers, each attesting exactly one thing.** The verifier checks the chain:
- the history is legal;
- the log is its projection, or HISTORY-MISMATCH;
- the core is the log's run, or CORE-MISMATCH;
- the record names all three, or SESSION-MISMATCH.

Two cases hold it:
- **X:** two histories with one input log and one core get two session records, and a history read with the other's
  record is refused.
- **G5:** Alice's `1` and Mallory's `1` give one core and two session records. Without the source in the history
  (plant `no-source`) the records were equal.

**Law-equivalence is deliberate.** "A sent nothing" and "a's valid input was dropped by the host" give one input log
and one core, both INPUT-MISSING. Only the history and the session record tell them apart, as G7 records. That is the
design, not a defect: a receipt never stands for a session.

**The input log's grammar is strict and canonical.** `parse_log` accepts exactly what `serialize` writes, or refuses
with a code:

> LOG-NOT-ASCII, LOG-LINE, LOG-HEADER, PORT-SIGNATURE, LOG-RECORD, LOG-TICK, LOG-END, LOG-AFTER-END, LOG-UNKNOWN

- **Every field is matched whole** (`fullmatch`). The door's `$` had accepted `1` followed by LF (G2).
- **A law with no each-tick port** writes `t <n>` with no trailing space. The tick record had one (G1).
- **Under A2 the end cause is INPUT-MISSING only.** INPUT-REFUSED belongs to A1 (G3).
- **25 named malformed logs** are each refused with the code expected. An open log parses as LOG-OPEN.
- **Every single-byte replacement, deletion and duplication** of the 13 distinct logs of the one-port domain, 16,132 in
  all, is refused or is itself canonical (EXHAUSTIVE over that declared domain). The manifold adversary also tried
  217 multi-byte edits: every accepted one was canonical, and the 20 outside A2's image are now refused by G3's
  repair.

**The one declared policy, and the tick-12 question.**
- A retry is a new arrival, and the refusal before it stays in the history.
- Tick 12 runs only when the host closes it with every port filled.
- If player A has no accepted input at the close, tick 12 does not run, and the session ends NOT-RUN 12 INPUT-MISSING
  for A.
- Player B's input is not carried forward.
- The host never advances while A retries, because advancing is closing. When the host closes is recorded as the
  `close` event.

**EXHAUSTIVE over declared domains:** 76,364 legal histories, each passing every row. The domains:
- one port up to 6 events, with arrivals among `1`, `1.1`, `4` and `13`;
- no each-tick port up to 6;
- two ports up to 4.

The rows:
- the projection is a function, and it round-trips through the strict parser;
- the door replays;
- no assignment disappears, each arrival has one disposition, and no value is invented;
- execution is a function of the log;
- the four statuses partition every outcome;
- the count identities hold, the prefix's count standing when no `'T'` was emitted;
- a TICK-BUDGET tick counts N+1;
- executed is counted less the refused operation;
- the session record binds.

The manifold adversary checked further, independently: two ports to depth 6, three ports to depth 5 and one port to
depth 8, with no row failing. **The weakness it found was in the rows, not the depth.**

**Plants (13 of 13):**
- a refused arrival assigned; a missing value held over; a slot overwritten;
- the budget's refused operation uncounted;
- `end` with a pending tick; an end record without its cause;
- lenient hex; records after the end;
- a session record without the history;
- a close after the run refused;
- the door's `$`;
- no source in the history;
- an A1-only cause under A2.

**Does not show:**
- Orlog's door and execution: the law here is a stand-in;
- multi-byte log edits beyond the adversary's 217;
- a host that buffers arrivals for future ticks (refused here as ASSIGN-AHEAD);
- any timing;
- read-once ports and their record: the model declares each-tick ports only (noted 2026-10-26,
  `packets/C-read-once-ports.md` §1);
- §15.5's log grammar: the model writes the keyword `t`, each value as the 16 hex digits of its raw 64 bits with no
  RUNTIME-SPEC §5 tag byte, and a port signature of `fix each-tick` only, so its malformed logs and its mutations
  hold the model's grammar, not the draft's (noted 2026-10-26, `packets/D-LOG-refusals.md` §1);
- the host's honesty. The host writes every record, and a lying host can write a consistent set. Integrity is not
  truth.

## 4. What this asks the owner, for the final push

- **E2** as a claim's standing, and **CUT-0's one rule under reading S2** in place of four rules: R8's two readings,
  the site rule, the NOT-RUN and LOG-OPEN extension, and the PREFIX settlement. Its invariant (§2) is the proof
  obligation.
- **The cut's place:** the `'R'` event's payload. It carries each frame's clause, a `For`'s bit, a refused If's arm
  and the open claim's id.
- **A2 with the declared policy,** in place of the reviewer's earlier (a). It keeps every principle of (a): the whole
  tick blocked, nothing invented, the session ended, recovery left to SNAP-1.
- **The session's history as a record of its own:** sources, legality rules, dispositions, END-PENDING,
  END-UNDISPOSED and RUN-REFUSED.
- **The two-layer binding:** the receipt core attests the run over its input log; the session record attests the
  session.
- **The input log's strict grammar,** the cause set by policy, and the four statuses as mutually exclusive
  predicates.

Owed before any of it is called settled:
- T11's proof over the phase table. T12 stays a conjecture that the contract does not lean on.
- The resumption oracle and the log congruence (`manifold/`) carried into 1a as off-gate checks of the built rule,
  which so far is research code only.

The resumption oracle was owed here and is discharged as evidence (`manifold/VERDICT.md`).
