# SPEC §15, draft 0: version 1, the open run (2026-10-26; research, not yet in SPEC.md)

*Superseded the same day by draft 1 (`SPEC-15-DRAFT-1.md`), after R7's review. The text the twin reviewed is kept
byte for byte in `twin-r7/SPEC-15-DRAFT-0-AS-REVIEWED.md`. This file stands as written, with the author's review
appended.*

**Status.** This is the scope the twin's paper round would read (R7). It moves into `SPEC.md` as §15 only once its
open clauses are ruled. Everything not stated here is version 0, as SPEC §1–§14 and RUNTIME-SPEC.md define it. Nothing
here is built.

**How to read the tags.** Every clause carries one:
- **[ruled: R3, R4, R5, R6]** — fixed by the owner's ruling of that name in `research/run-1/RULINGS.md`. The clause
  states what the ruling fixes; his words are there, not here.
- **[ruled: claims]** — fixed by "The claims ruling" in `RULINGS.md`: E2, and the meet.
- **[open: X]** — not ruled. The clause gives the current proposal, and X names what decides it: a sheet item (R1,
  R2, R8 to R12, D1 to D10), a row of `ROUNDS.md`'s amended set, or a question found here. The twin's round must not
  read an open clause as settled.
- **[fixed]** — holds whatever is ruled (`RULINGS.md`, "Fixed whatever is ruled").

**Two names clash, and are kept apart here.** "R8" in the ruling sheet is **float ports** (open). "R8" in the court
is **the settlement rule for a refused evaluation** (built, `src/orlog/court.py`). This draft writes the first as
*sheet R8* and the second as *the court's R8*.

## 15.0 Terms

- **Version 1 law:** a law whose source has a port or a tick block. Its header line reads `orlog-law 1`; every other
  law keeps `orlog-law 0` and its version-0 bytes. **[ruled: R5]**
- **Port:** a declared input, read **each tick** or **once**, with a name and a type: `an integer`, `a fixed`,
  `a truth value` or `a text`. A port is read-only. Float ports are not in version 1 unless sheet R8 rules them.
  **[open: R2; sheet R8]**
- **Prefix:** the top-level statements before the tick block. **Tick block:** the last top-level clause. **Input
  point:** the first place a port is read in evaluation order.
- **Arrival:** bytes sent toward a port by a source. **Door:** the pure function that judges an arrival. **Host:**
  the program that receives arrivals, keeps the records and starts an execution.
- **Session:** the history of one host's events (§15.4). **Input log:** what the law reads (§15.5). **Execution:** the
  reference or a compiled backend running one law over one input log.

## 15.1 The forms

1. **Spellings.** **[open: R2]**
   - A port read each tick: `Let thrust be given each tick as a fixed.`
   - A port read once: `Let gravity be given as a fixed.`
   - The tick block: `Each tick, do the following.`
   - With a budget: `Each tick, at most N operations, do the following.`
2. **Every form is spelled only where version 0 refuses SYNTAX at the statement**, so no accepted version-0 text
   changes meaning. No word is newly reserved. **[fixed]**
3. **Places.** **[open: R2; amended set "port place"]** Ports are declared at the top level, before the tick block.
   There is one tick block, the last top-level clause. A read of an each-tick port outside the tick block is refused
   at compile time. The new compile codes, entered in SPEC §13's phase table:
   - PORT-PLACE: a port elsewhere;
   - TICK-PLACE: a tick block elsewhere, or a second one;
   - PORT-VARIABLE: a port assigned.
4. **The law's lines.** `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`. **[ruled: R5]**
5. **The door and the forms agree.** Each form's recognition, its parse or refusal, and its line classification are
   one decision. A form indented, or behind a repaired byte, reads as it reads at column one. **[open: amended set
   "H2", in a change of its own]**
6. **A world property** (gravity, a constant of the scene) is proposed as a port read once. Its cost: every claim
   evaluated after the port is read is stripped of grounding by §15.13, whether or not it reads the property.
   **[open: R1; the cost sentence is ruled: R6]**

## 15.2 The door

**[ruled: R3]** The door never rounds. It is a pure function of (the port's declaration, the arrival's bytes). Its
version is named in the input log's header. Its rules, in order; the first rule a value breaks is its refusal:
1. **The bytes must match the port type's ASCII grammar exactly**, before any number is parsed. Otherwise
   INPUT-SYNTAX.
2. **`an integer`:** any fraction or decimal point refuses INPUT-NOT-INTEGER, and a value outside [−2^63, 2^63−1]
   refuses INPUT-RANGE.
3. **`a fixed`:**
   - The exact rational the text names is checked against the raw bounds first: raw −2^63 and raw 2^63−1, ×2^−32.
     Outside them refuses INPUT-RANGE.
   - Then a value off the 2^−32 grid refuses INPUT-GRID. The refusal names the two nearest grid values.
   - A raw value has a prefix of its own in the grammar. **[open: its spelling and sign]**
4. **`a truth value`:** exactly one spelling for true and one for false. Case variants and `1`/`0` refuse
   INPUT-SYNTAX. **[open: the two spellings]**
5. **`a text`:**
   - The bytes are kept as sent.
   - Bytes that are not UTF-8 refuse INPUT-NOT-UTF8.
   - A text not in NFC is accepted, with a note in the door's report, recomputable from the bytes.
   - **[open: whether text also refuses what the literal door refuses]**

The log holds only values exactly as sent. A later version may relax a refusal into acceptance; the reverse is never
allowed (COMPAT-0's rule). **[ruled: R3]**

## 15.3 The session's events

**[open: amended set "A2", with the declared policy]** The door judges each arrival before any assignment, and the
host's events are these:

| event | legal when | effect |
|---|---|---|
| `arrive(port, source, bytes)` | the session has not ended, its run has not refused, and the port is declared | numbered in order, with its source; the door judges it at once |
| `assign(arrival, tick)` | as above; the arrival was accepted and has no disposition; the tick is the open one; its port's slot is empty | it fills the slot |
| `drop(arrival)` | as above; the arrival was accepted and has no disposition | declined; its source is told |
| `close()` | as above | if every each-tick port is filled, the open tick runs at once. Otherwise the tick does not run, NOT-RUN with the first missing port in declaration order, and the session ends |
| `end()` | the open tick holds no assignment (else END-PENDING) and every accepted arrival is assigned or dropped (else END-UNDISPOSED). After the run refused, `end` is the only legal event and needs neither | the session ends |

- **Any other move is refused by its rule's name:** ASSIGN-REFUSED, DROP-REFUSED, DISPOSED-TWICE, ASSIGN-CLOSED,
  ASSIGN-AHEAD, SLOT-FILLED, AFTER-END, UNKNOWN-PORT, NO-ARRIVAL, END-PENDING, END-UNDISPOSED, RUN-REFUSED.
- **Every arrival has exactly one disposition**, derived from the history: refused with its code, assigned to its
  tick, dropped, or unconsumed.
- **No value is ever invented, held over or defaulted.** A tick that does not run stops every port of it, and the
  session. **[fixed: R4 and the draft's §1.5]**
- **A retry is a new arrival;** the refusal before it stays in the history. The host never advances while a source
  retries, because advancing is closing.
- **Until SNAP-1, a refusal ends the session.** A refusal ends its branch at the tick. The refused branch is kept,
  sealed and queryable. **[ruled: R4]**

## 15.4 The session record, `orlog-session 0`

**[open: amended set "session record" and "binding"]**
- **The history is a record of its own:** sources, door verdicts, assignments, drops, closes and the end, chained.
- **Three records, three authorities:**
  - the receipt core attests one execution over its input log (§15.8);
  - the session record attests the session: `history-sha256`, `input-log-sha256` and `receipt-core-sha256`;
  - the arbiter's agreement record attests the compared executions, their identities and the verdict.
- **The verifier checks the chain:** the history is legal; the log is its projection, or HISTORY-MISMATCH; the core
  is the log's run, or CORE-MISMATCH; the record names all three, or SESSION-MISMATCH.
- **Two histories with one input log share one core.** That is law-equivalence, by design: a receipt never stands for
  a session.

## 15.5 The input log, `orlog-inputs 0`

**[open: amended set "identity and bytes"]** A stream of LF-terminated ASCII lines, parsed strictly. Every field is
matched whole, and the parser accepts exactly what the serializer writes:
- **The header:** `orlog-inputs 0`; `ports <the port signature's sha256>` (§15.6); `door <the door's version>`.
- **One record for the read-once ports, then one record per tick**, in tick order from 1. A tick record holds every
  each-tick port's value in declaration order, densely: `t <n>`, then each value's encoding (RUNTIME-SPEC §5) as
  lowercase hex, separated by single spaces. With no each-tick port the line is `t <n>`, with no trailing space.
- **Optionally, one end record:** `end <n>`, n the number of tick records, and a cause: `closed`, or
  `not-run <t> INPUT-MISSING <port>`. INPUT-REFUSED belongs to the candidate A1, not to A2.
- **A log with no end record is open.**
- **Load refusals:** LOG-NOT-ASCII, LOG-LINE, LOG-HEADER, PORT-SIGNATURE, LOG-RECORD, LOG-TICK, LOG-END,
  LOG-AFTER-END, LOG-UNKNOWN. These replace contract draft 0's single LOG-MALFORMED.
- **The chain:** in_0 = SHA-256("orlog-inputs 0" ‖ the header's bytes, with the read-once record);
  in_t = SHA-256(in_{t−1} ‖ SHA-256(tick record t's bytes)).
- **`input-log-sha256`** is the SHA-256 of the log's bytes as read: to the end record inclusive, or to the end of an
  open log.

## 15.6 The port signature

**[open: amended set "identity and bytes"]** SHA-256 of `orlog-ports 0\n`, followed, for each port in declaration
order, by `(port "<name>" <type> each-tick|once)\n`. The variable number is left out; the name, the type and the kind
are in. An unrelated statement before the ports leaves the signature equal. Renaming, retyping, reordering or changing
a port's kind changes it.

## 15.7 Execution

1. **The order.** **[ruled: R5]** A run executes the prefix, then one tick per tick record, then stops.
   - A read-once port binds where its declaration stands, emitting its `'N'` event before the first `'T'`.
   - Each tick emits `'T'`, then one `'N'` per each-tick port in declaration order, then runs the tick block's body.
   - Binding a port counts no operation. **[open: amended set "counting"]**
2. **`'T'`'s payload is (t, c), both u64.** **[ruled: R5, amendment 1]**
   - c is the number of operations counted from the start of the run up to the moment `'T'` is emitted: the running
     total. **[open: amended set "counting"]**
   - R5 left a reading open between the running total and the previous tick's own count. This draft proposes the
     running total, the counting row's.
   - The tick block counts nothing of its own. An If arm's count belongs to the arm's clause. Events are not
     operations. **[open: amended set "counting"]**
3. **The budget.** **[open: amended set "budget"; sheet R9]**
   - N is 0 (no budget) or 1…2^62; a larger N is refused at compile time.
   - A tick's count starts at 0 at its `'T'`. When adding an operation makes the count N+1, that operation is counted
     and then refused before it executes: TICK-BUDGET, at the clause whose statement is executing.
   - **[open, found by the cut's schema:** for an If's condition operation, which clause is "the clause whose
     statement is executing": the If's head, or the arm's, as version 0's refusals inside a condition name the arm's?
     The cut's event check depends on it (`CUT-SCHEMA.md` S6).**]**
4. **A refusal of any code ends the run at once,** and later records are not read. **[ruled: R4]**
5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]**
   - COMPLETED: every tick record ran, and the end record's cause is `closed`.
   - REFUSED <CODE> <clause>: a refusal in the prefix or in a tick. The tick is the receipt's `ticks` (§15.8).
   - NOT-RUN <t> <cause> <port>: every record before t ran, and the end record names tick t as not run.
   - LOG-OPEN: every record of an open log ran, with no refusal. A refusal inside an open log is REFUSED.
6. **The output chain.** **[ruled: R5, amendment 2]**
   - out_0 = SHA-256("orlog-output-1" ‖ SHA-256(the bytes said before the first `'T'`)). The domain string is
     contract draft 0's, not R5's. **[open: amended set "identity and bytes"]**
   - out_t = SHA-256(out_{t−1} ‖ SHA-256(the bytes said during tick t)).
   - A refused tick's partial output is its out_t, the chain's last link.

## 15.8 The receipt, `orlog-receipt 1`

**[ruled: R5]** Lines, in order:
- `orlog-receipt 1`
- `backend <name>`
- `law-seal`, `text-seal`, `input-log-sha256`
- `status` (§15.7.5)
- `ticks <n>`: the ticks begun, a refused tick included and a not-run tick not **[ruled: R5, amendment 3]**
- `tick-ops <n>`: the last begun tick's own count, complete or partial; exactly N+1 under TICK-BUDGET **[open:
  amended set "identity and bytes"]**
- the count of tick records left unread after a refusal **[open: amended set "identity and bytes"; its name too]**
- `output-bytes`, `output-chain`
- `events`, `trace-head`
- `ops`: every counted operation, the refused one included
- `claims`, then one `claim` line each, as in version 0
- `end`

Then:
- **The core** is the receipt without its `backend` line. Executions agree when their cores are byte-identical.
- **The frame check is versioned.** **[ruled: R5, amendment 4]** A law headed `orlog-law 0` requires a receipt
  beginning `orlog-receipt 0`; a law headed `orlog-law 1` requires `orlog-receipt 1`. Never either for any law. Its
  plants: a version-1 receipt checked under the version-0 frame must fail, and a version-0 receipt under the
  version-1 frame must be refused.
- **No receipt line states that a run is valid or correct.** **[fixed]**

## 15.9 The trace, `orlog-trace-1`

- **The head.** head_0 = SHA-256("orlog-trace-1" ‖ law_seal). Each event extends the head as in version 0, with
  version 0's events and `'T'` and `'N'`. The per-event chain is kept, not replaced by a stream head. **[ruled: R5]**
- **`'N'`'s payload** is the port's variable number (u32) and the value encoding of RUNTIME-SPEC §5. **[ruled: R5]**
- **The `'R'` event carries the refusal cut** (§15.13.4), because the claims ruling's withholding reads the cut, and a
  `Perform` emits no event from which it could be recovered. **[ruled: claims; the bytes are open]**
  - The proposed bytes are `CUT-SCHEMA.md`'s draft 2: the code's length and the code, the frame count, then per
    frame a u32 clause, a u16 selector, a bit for a For that is not the last frame, and an arm for an If that is the
    last frame.
  - **[open: the format freeze, due before the first version-1 receipt is frozen anywhere (`CUT-SCHEMA.md` P6); the
    tick block's frame, and the ports', not yet derived]**
  - Version 0's `'R'` payload stays the code alone. The law's header chooses the grammar, never the payload's look.

## 15.10 The tick line, `orlog-ticks 0`

**[ruled: R5: part of 1a]** Written by an execution given a path: one line per tick that ran to its end, and none for
a refused tick. Its fields:
- `tick <t>`, `events <n>`, `ops <n>` (the tick's own count), `output-bytes <n>`;
- `trace-head <hex>`, or `-` in a play build without the chain (sheet R14 if ruled);
- `output-chain <hex>`;
- `claims <hex>`: the SHA-256 of the claim lines as they would read at the tick's end;
- `state <hex>`: the SHA-256 of every top-level variable's value encoding, in variable order;
- `input-chain <hex>`: in_t. **[open: speed verdict's proposal, not named in R5's ruling]**

These must hold, under §15.7.2's running-total reading of c:
- T(t+1).c − T(t).c equals tick t's `ops`;
- T(1).c is the prefix's count;
- the receipt's `ops` minus the last `'T'`'s c is the last tick's count, or a refused tick's partial count.

The state digest's cost on a large state is for 1a's specification. **[open: 1a's specification, as R5 leaves it]**

## 15.11 What a run establishes

- **Replay.** Given the law's bytes, the input log's bytes and the version the law's header names, every conforming
  execution writes the same receipt core, the same trace and the same tick lines. A compiler, a runtime build or a
  host is not a condition: a difference under the same three is a defect of an execution.
- **Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity.**
  **[fixed]**

## 15.12 The court in a run with an input log: grounding

**[ruled: R6]**
1. **The trigger.** A run has an input log when its law declares a port or has a tick block. A tick block with no
   port still takes input: the log's length sets how many ticks run.
2. **No claim of such a run is GROUNDED, whatever its channel and whatever is ratified, except under PREFIX.**
3. **The provenance line** prints exactly `rests on input log <input-log-sha256>, unratified`, the receipt's own
   value.
4. **PREFIX.** A claim is exempt only if every evaluation of it precedes the first input. It stands before the first
   port declaration and outside the tick block, and it is not in a procedure performed at or after the first port
   declaration. The licence is decided by evaluation, never by position alone. **[open: amended set "PREFIX": by
   static closure from the input point, every consumer of the reachability stating its own soundness requirement]**
5. **A PREFIX claim that evaluated true stays held** when the run is later refused at a tick.
6. **The rows are paired with controls,** and each runs with its witness configured as agreed. The control is the same
   claim without an active log, or wrapped in PREFIX, and it must read GROUNDED.

## 15.13 The court in a version-1 run: HELD

**[ruled: claims]**
1. **HELD means E2:** every completed evaluation of the claim was true, no evaluation of that claim remains open at
   the cut, and the continuation at the cut could not evaluate that claim again.
2. **Only continuation that could evaluate the particular claim again affects its standing.** Unrelated pending
   execution does not withhold it.
3. **"True in k of k evaluations" stays in every reading,** as descriptive evidence, never as settlement.
4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT-0 holds it.** The meet
   names the exact digest of the CUT-0 it uses. A digest identifies the rule; it does not prove it sound.
5. **The court's R8** (built): when the run refuses at a claim's own clause with any code but CLAIM-REFUTED, an
   evaluation of the claim began and did not finish, and the claim is not held. A claim inline in another statement
   shares its clause with a condition or another arm, so the refusal may come from there. It is not held either.
6. **CUT-0** holds a claim when every completed evaluation is true, it is not open at the cut, and it is not in K̂.
7. **The cut** is the stack of statements executing at the refusal, outermost first. An arm's inline statement
   stands in its If's frame, named by its arm. **K̂** is computed from it:
   - **the open claim:** a claim whose evaluation is open at the cut is in K̂, named by its id (T10.6);
   - **a refused If** (the If on top): the arms from the refused one onward, the Otherwise included (T10.2);
   - **a loop's own clause refused:** its body (T10.3, T10.4);
   - **a Perform refused at its own operation:** its body (T10.5);
   - **the rest of a block,** for each frame outward: the following siblings that are not absorbed Otherwise
     clauses, everything they may execute included, values ignored (T10.1);
   - **a For below the top:** its body again, exactly when its bit says passes remain (T10.3);
   - **a While below the top:** its body again, always (reading S2: its condition is unknown, and its fuel check is a
     passable refusal) (T10.4);
   - **a Perform below the top:** a return only to the frame below it, the actual caller (T10.5);
   - **the tick block below the top:** its body again, since another tick may run (T10.7);
   - **NOT-RUN t, or LOG-OPEN:** the cut is the tick block's head before tick t, and K̂ is the tick block and every
     procedure performed from it (T10.7).

   What "may execute" reaches includes every procedure performed, transitively.
8. **Every withholding by CUT-0 names its row:** the open claim, the refused If's arms onward, the loop's own clause
   refused, a Perform refused, the rest of a block, a For's next pass, a While's next pass, or the tick block's next
   tick.
9. **No proof obligation is closed by this section.** T10 stays open, split into T10.0 to T10.7 in `ROUNDS.md`, and
   no test result or measurement alone closes it. T11 stays open. **[ruled: claims]**
10. **Until 1b, the court reads version-1 runs as REFERENCE-ONLY and holds no claim.** **[open: D10]**
11. **A claim with no evaluation is UNREACHED,** as in version 0.

## 15.14 Reporting

**[open: amended set "reporting"]** Every authoritative report names its claim, the evidence it binds, the authority
that made it, its version, and the condition on which it passes or fails, and it attests nothing outside its
authority. "Grounded over claims" joins the court summary's forbidden interpretations.

## 15.15 What is open, for the owner, before the twin reads this

| clause | decided by |
|---|---|
| 15.0 and 15.1: spellings, places, float ports | R2; the amended set's "port place"; sheet R8 |
| 15.1.5: the door and the forms | the amended set's "H2" (its own change, with E18's COMPAT-0 settlement) |
| 15.1.6: world properties | R1 |
| 15.2: the raw prefix and sign; the two truth spellings; text's extra refusals | details R3 leaves to 1a's specification |
| 15.3 and 15.4: the session, its record, the binding | the amended set's "A2", "session record" and "binding" |
| 15.5 and 15.6: the log's bytes, the signature | the amended set's "identity and bytes" |
| 15.7.2 and 15.7.3: counting, the budget, and TICK-BUDGET's clause at an If's condition | the amended set's "counting" and "budget"; sheet R9; the clause question, new |
| 15.7.5 and 15.8: the four statuses, `tick-ops`, the unread count | the amended set's "identity and bytes" |
| 15.9: the cut's bytes | the format freeze (P6), after the tick block's and the ports' frames are derived |
| 15.10: `input-chain`, the state digest's cost | the speed verdict's proposals; 1a |
| 15.12.4: PREFIX by static closure | the amended set's "PREFIX" |
| 15.13.10: REFERENCE-ONLY until 1b | D10 |
| 15.14: the authority rule | the amended set's "reporting" |

## Review of this draft against the rulings, CUT-0, the schema and T10 (2026-10-26)

Done the same day the draft was written, by reading each source against the clauses. One author wrote both the draft
and this review, so it shows consistency with the records, not that the records are right. The twin's round is the
independent reading.

| source | what it requires | where §15 states it | finding |
|---|---|---|---|
| R3 | the door never rounds; its grammar sieve before parsing; integer, fixed (raw bounds, grid with two neighbours), truth value, text rules | 15.2 | matches. Three spellings are left to 1a by R3 itself, and are marked open |
| R4 | a refusal ends its branch at the tick; the branch kept, sealed and queryable; until SNAP-1 a refusal ends the session | 15.3, 15.7.4 | matches. R4's option text also says "the receipt says REFUSED code, clause and tick". §15 meets it with the status line and `ticks` together. **This is a reading, for the owner to confirm** |
| R5 | `orlog-law 1` only with a version-1 form; the law lines; `'T'` as (t, c); `'N'`; the output chain and its edges; `ticks` at a refusal; the versioned frame check; the tick line in 1a; the per-event chain | 15.0, 15.1.4, 15.7, 15.8, 15.9, 15.10 | matches, after correction: the draft first marked out_0's domain string and "binding counts no operation" as R5's, and they are contract draft 0's (now open). The tick line's identities hold under the running-total reading only, now said |
| R6 | the trigger; no GROUNDED outside PREFIX; the provenance line exactly; PREFIX by evaluation; a PREFIX claim held past a refusal at a tick; paired controls | 15.12 | matches. PREFIX by static closure stays open, as the amended set's row |
| the claims ruling | E2; claim-specific continuation; "true in k of k" descriptive; the meet pinned to CUT-0's digest; every withholding names its row; T10 open and split; T11 open | 15.13 | matches |
| `CUT-0.md` §2 | the cut's frames; K̂ construct by construct; the outcome rows (NOT-RUN, LOG-OPEN, a refusal inside a tick) | 15.13.6, 15.13.7 | matches after one addition: an arm's inline statement stands in its If's frame |
| `CUT-0.md` §3 | the session's events, legality, the refusal names, dispositions, no value invented, the strict log grammar, the three records | 15.3, 15.4, 15.5 | matches, all marked open (A2, session record, binding, identity and bytes) |
| `CUT-SCHEMA.md` | draft 2's bytes; S6's question for TICK-BUDGET at an If's condition; P4 (the header chooses the grammar); P6 (the freeze before the first version-1 receipt) | 15.7.3, 15.9 | matches; all marked open |
| T10.0 to T10.6 | each row of K̂ an obligation | 15.13.7, each rule citing its row | **a gap, repaired:** §15 has a tick-block rule that no T10 row covered. T10.7 is added to the ledger, DECLARED and not built |

**Findings, beyond the matches:**
1. **The ruling sheet's "R8" (float ports) and the court's R8 (a refused evaluation) share a name.** The meet is
   "R8 ∧ CUT-0" in the court's sense. §15 writes *sheet R8* for the first. The sheet's later items should be renamed
   or always qualified, or a reader will mix them.
2. **"Port place" is read here as forbidding a read of an each-tick port outside the tick block.** The amended set's
   row says "any read outside the tick block". A read-once port is read in the prefix by design (R1's proposal), so
   "any read" cannot mean every port. To confirm with the row's ruling.
3. **R4's "code, clause and tick"** is met by two receipt lines, not one (the R4 row above).
4. **The open set is large.** Thirteen clause groups wait on rulings (15.15). Under R7 (a), the twin's round reads
   §15 alone. A round run now would read proposals as if they were rules, or record every open clause as a question.
   So the rulings should come first, or the round should be told which clauses are proposals.
