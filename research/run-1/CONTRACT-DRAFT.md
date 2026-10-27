# RUN-1 contract, draft 0 (2026-10-26): the rules alone, for attack

This is the proposed contract as normative rules, with no reasons and no preferred readings. It is written for an
adversary. Where a rule has two candidates still open, both are stated (A1 and A2), and an attack may take either.
Everything not stated here is version 0 as SPEC.md and RUNTIME-SPEC.md define it. Nothing here is ruled or built.

## 0. Terms

- **Law:** a compiled program. Its header reads `orlog-law 1` when it declares a port or has a tick block, and
  `orlog-law 0` otherwise.
- **Port:** a declared input. It is read **each tick** or **once**, has a name and a type (`an integer`, `a fixed`,
  `a truth value`, `a text`), and is read-only in the law.
- **Prefix:** the law's top-level statements before the tick block. **Tick block:** the last top-level clause,
  `Each tick, do the following.` or `Each tick, at most N operations, do the following.`
- **Arrival:** a value sent toward a port by a source. **Door:** the function that judges an arrival. **Host:** the
  program that receives arrivals, keeps the logs and starts the execution.
- **Input log:** what the law reads. **Arrival log:** what reached the door.
- **Execution:** one of the reference and the compiled backends, running one law over one input log.
- **Receipt**, **trace** and **tick line:** an execution's records (§5–§7).

## 1. Arrivals and the door

1.1. The host appends every arrival to the arrival log, in the order received: its sequence number, the port's name,
the source's label and the bytes as received.

1.2. The door is a pure function of (the port's declaration, the arrival's bytes) and of nothing else. Its version is
named in the arrival log's header and in the input log's header. It returns either an accepted value encoding
(RUNTIME-SPEC §5) or a refusal with a code.

1.3. The door's rules, in this order. The first rule a value breaks is its refusal.
1. The bytes must match the port type's ASCII grammar exactly. Otherwise INPUT-SYNTAX.
2. `an integer`: any fraction or decimal point refuses, INPUT-NOT-INTEGER. Outside [−2^63, 2^63−1] refuses,
   INPUT-RANGE.
3. `a fixed`: the exact rational the text names is compared with the bounds raw −2^63 and raw 2^63−1 (×2^−32) first.
   Outside them refuses INPUT-RANGE, naming the nearest bound. Then, off the 2^−32 grid refuses INPUT-GRID, naming the
   two nearest grid values. A raw value has its own prefix; its spelling and sign are not yet fixed.
4. `a truth value`: exactly one spelling for true and one for false; anything else refuses INPUT-SYNTAX.
5. `a text`: the bytes are kept as sent. Bytes that are not UTF-8 refuse INPUT-NOT-UTF8. A text that is not in NFC is
   accepted, with a note in the door's report.

1.4. **Assignment and refusal: two candidates.**
- **A1 (assign, then judge).** The host assigns each arrival to a (tick, port) first, and the door judges it. If the
  door refuses an arrival assigned to tick t, tick t does not run (status NOT-RUN, cause INPUT-REFUSED) and the session
  ends.
- **A2 (judge, then assign).** The door judges each arrival before any assignment. A refused arrival is recorded with
  its refusal, answered to its source, and never assigned. The host assigns accepted arrivals to (tick, port), at most
  one per (tick, port), and closes each tick. If the host closes tick t without a value for some each-tick port, tick t
  does not run (status NOT-RUN, cause INPUT-MISSING) and the session ends.

1.5. In both candidates a not-run tick stops the whole tick, every port of it, and the session. No value is ever
invented, held over from an earlier tick or defaulted. RUN-1 has no recovery rule; continuing a session is SNAP-1's.

## 2. The input log, `orlog-inputs 0`

2.1. The input log is a stream of LF-terminated ASCII lines:
- a header: `orlog-inputs 0`, `ports <the port signature's sha256>` (§3), and `door <the door's version>`;
- one record for the read-once ports, holding each read-once port's value encoding in declaration order;
- then one record per tick, in tick order from 1, holding every each-tick port's value encoding in declaration order
  (dense);
- then, optionally, one end record: `end <n>`, where n is the number of tick records, followed by a cause, either
  `closed` or `not-run <t> <INPUT-REFUSED|INPUT-MISSING> <port name>`.

2.2. A log with no end record is **open**. A log with records after its end record, a duplicated or missing tick
number, a record whose port count or types do not match its header's signature, or an end record whose n differs
from the records' count is refused at load, LOG-MALFORMED, before any execution starts.

2.3. Its chain: in_0 = SHA-256("orlog-inputs 0" || the header's bytes, with the read-once record);
in_t = SHA-256(in_{t−1} || SHA-256(tick record t's bytes)).

2.4. `input-log-sha256` is the SHA-256 of the log's bytes as read: to the end record inclusive, or to the end of an
open log.

2.5. The input log is a projection of the arrival log: under A1, of its assigned arrivals; under A2, of its accepted
and assigned arrivals, with the host's closing of each tick.

## 3. The port signature

3.1. SHA-256 of the bytes `orlog-ports 0\n`, followed, for each port in declaration order, by the line
`(port "<name>" <type> each-tick|once)\n`. A declared range, if ports gain one, follows the type.

3.2. The law's own port line, `(port <var> "<name>" <type> each-tick|once)`, carries the variable number; the
signature does not.

3.3. A log whose `ports` line differs from the law's signature is refused PORT-SIGNATURE before execution.

## 4. Execution

4.1. A run executes the prefix, then one tick per tick record in order, then stops. A read-once port binds where its
declaration stands, emitting its `'N'` event. Each tick t emits `'T'`, then one `'N'` per each-tick port in
declaration order, then runs the tick block's body. Binding a port counts 0 operations.

4.2. `'T'`'s payload is (t, c), both u64. c is the number of operations counted (SPEC §7) from the start of the run up
to the moment `'T'` is emitted.

4.3. **The budget.** Under `at most N operations`, a tick's count starts at 0 at its `'T'`. SPEC §7 adds 1 to the
count immediately before each counted operation. When the addition makes the tick's count N+1, the operation is
counted and then refused before it executes: TICK-BUDGET, at the clause whose statement is executing.

4.4. A refusal of any code ends the run at once. Later records are not read.

4.5. **Outcomes.**
- **COMPLETED:** every tick record was run, and the end record's cause is `closed`.
- **REFUSED <CODE> <clause>:** a refusal in the prefix or in a tick.
- **NOT-RUN <t> <cause> <port>:** every record before t was run, and the end record names tick t as not run.
- **LOG-OPEN:** every record of an open log was run with no refusal. A run that refuses inside an open log is
  REFUSED, not LOG-OPEN.

4.6. **Output.** out_0 = SHA-256("orlog-output-1" || SHA-256(the bytes said before the first `'T'`)).
out_t = SHA-256(out_{t−1} || SHA-256(the bytes said during tick t)). A tick that refuses contributes its partial
output as its out_t, and that is the chain's last link.

## 5. The receipt, `orlog-receipt 1`

5.1. Lines, in order:
- `orlog-receipt 1`
- `backend <name>`
- `law-seal`, `text-seal`, `input-log-sha256`
- `status`
- `ticks <n>`, the number of `'T'` events emitted, a refused tick included and a not-run tick not
- `output-bytes`, `output-chain`
- `events`, `trace-head`
- `ops`, every counted operation, the refused one included
- `claims`, then one `claim` line each, as v0
- `end`

5.2. The **core** is the receipt with its `backend` line removed. Executions agree when their cores are byte-identical.

5.3. **The frame check.** A law whose header is `orlog-law 0` requires a receipt beginning `orlog-receipt 0`; a law
whose header is `orlog-law 1` requires `orlog-receipt 1`. Any other receipt has no core.

5.4. No receipt line states that a run is valid or correct.

## 6. The trace, `orlog-trace-1`

6.1. head_0 = SHA-256("orlog-trace-1" || law_seal). Each event extends the head as in version 0, with v0's events and
`'T'` and `'N'`.

## 7. The tick line, `orlog-ticks 0`

7.1. Written by an execution given a path, one line per tick that ran to its end, none for a refused tick:
`tick <t> events <n> ops <n> output-bytes <n> trace-head <hex> output-chain <hex> input-chain <hex> claims <hex>
state per-tick <hex>`.
- `ops`: the tick's own count.
- `input-chain`: in_t.
- `claims`: the SHA-256 of the claim lines as they would read at the tick's end.
- `state`: the SHA-256 of every top-level variable's value encoding in variable-id order.

7.2. These must hold:
- T(t+1).c − T(t).c equals tick t's line's `ops`;
- T(1).c is the prefix's count;
- the receipt's `ops` minus the last `'T'`'s c is the last tick's count, or a refused tick's partial count.

## 8. The court, in a run with an input log

8.1. A run has an input log when its law declares a port or has a tick block.

8.2. No claim of such a run is GROUNDED, except under PREFIX. The court prints, for the run, `rests on input log
<input-log-sha256>, unratified`.

8.3. **PREFIX:** a claim is exempt only if every evaluation of it precedes the first input. It must stand in the
prefix, before the first port declaration, outside the tick block, and not in a procedure performed at or after the
first port declaration.

8.4. **Completeness of a claim's evaluations.** In a run that ends REFUSED at clause s, a claim at clause c is not held
when c is reachable from s. Reachability is over the clauses, whatever the values:
- after a clause, its next sibling, or the end of its parent;
- the end of a loop's body leads back to the loop's head, which may enter the body or leave it;
- an If may enter any arm or none;
- a `Perform` enters the procedure's body, and the end of a body returns after every `Perform` of that procedure;
- the tick block is a loop.

c is reachable from s if c = s, or if some path from s, entering s's own body if it has one, visits c. Every claim
held before this rule (true in all of n ≥ 1 evaluations, no refusal at its clause, the executions agreeing) and not
removed by it is held.

8.5. A claim with no evaluation is UNREACHED, as in version 0.

## 9. What a run establishes

9.1. **Replay:** given the law's bytes, the input log's bytes and the version the law's header names, every conforming
execution writes the same receipt core, the same trace and the same tick lines. A compiler, a runtime build or a host
is not a condition: a difference under the same three is a defect of an execution.

9.2. Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity.
