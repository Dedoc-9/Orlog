# Packet G: finding 8, the read-once stop's status form and encoding (2026-10-28)

Research only. *Ruled since, 2026-10-28: 8.1 (a) and 8.2, by his adoption of a reviewer's proposed ruling, recorded in `RULINGS.md` ("Finding 8: the read-once stop's status form"). 8.3 (a1), 8.4 (a), 8.5 (a) and 8.6 (a), the same day, recorded beside it. The read-once record's own line, ruled the same day: `once <v1> <v2> …`, written only when the law declares a read-once port.* This packet sets out the parts of finding 8 that concern the read-once stop: how
its receipt status is written, what its NOT-RUN carries in place of a tick, and which logs that lack the read-once
record load. The other parts of finding 8 stay in packet D (`D-LOG-refusals.md`) for a later decision: the LOG-*
codes, their conditions and order, and whether a load refusal writes a receipt.

The text read is `SPEC-15-DRAFT-10.md` (sha256 `c69e7e3b…`). Clause numbers are its own.

## 1. What is already fixed, and must not be reopened here

- **RO′-3:** at the stop, *"NOT-RUN naming the read-once port the end record names (the first empty one in
  declaration order, checked against the history), or LOG-OPEN if the log has no end record. No `'N'` is emitted"*.
- **RO′-5:** *"That stop is a case of NOT-RUN or LOG-OPEN, not a fifth status. COMPLETED never stands for a law with a
  read-once port whose log lacks the record."*
- **STOPROW-1:** the stop *"must have an explicit receipt status that distinguishes a stop caused by the absent record
  from a LOG-OPEN run in which the read-once record exists but no tick ran"*, and *"The court selects the responsible
  row from the receipt, not by inspecting the log or inferring absence from trace events."*
- **His confirmation of RO′-5:** *"It remains `NOT-RUN` or `LOG-OPEN`, with an explicit distinguishing status form;
  Finding 8 must define its encoding."*
- **Condition 5:** *"Finding 8 must define a loadable representation for read-once `NOT-RUN` logs. Byte forms remain
  open."*
- **The pin:** finding 8 is resolved and recorded before CUT-0's digest is pinned, and so is the version-1 NOT-RUN and
  LOG-OPEN status encoding by which CUT-0's rows are chosen.

So the first word of the status is NOT-RUN or LOG-OPEN, and something after it must tell the stop apart. What that
something is, and its bytes, is the decision.

## 2. The current forms (draft 10, all open)

- Receipt (15.8): one `status` line. Version 0 writes `status COMPLETED` or `status REFUSED <CODE> <clause>`
  (RUNTIME-SPEC). 15.7.5 adds `NOT-RUN <t> <cause> <port>` and `LOG-OPEN`.
- Input log (15.5): an optional end record, `end <n>` and a cause, `closed` or `not-run <t> INPUT-MISSING <port>`. The
  research model enforces t = n+1 and an each-tick port (packet C, `C-read-once-ports.md`).
- MEASURED by packet F on the research model: every read-once NOT-RUN form tried is refused LOG-END, and a `once` line
  is refused LOG-UNKNOWN. So no read-once NOT-RUN log loads today, which condition 5 forbids.

## 3. The decisions, numbered separately

A ruling on one does not decide another unless it says so.

### 8.1 The stop's status form in the receipt

| option | the two stop statuses | entails |
|---|---|---|
| **(a) a keyword in the second place** (PROPOSED) | `status NOT-RUN READ-ONCE INPUT-MISSING <port>` and `status LOG-OPEN READ-ONCE` | The first word is still NOT-RUN or LOG-OPEN (RO′-5). The second token tells the stop apart: a decimal t for a tick's NOT-RUN, `READ-ONCE` for the stop. A plain `LOG-OPEN` stays the open run that held the record. No number is overloaded, and the stop's NOT-RUN carries no t at all (so 8.2 follows). |
| (b) t = 0 as the mark | `status NOT-RUN 0 INPUT-MISSING <port>` and `status LOG-OPEN 0` | Reads the read-once record as "tick 0" (Round D, `ROUNDS.md`:271). But `LOG-OPEN 0` invites the reading "an open run with no tick", which is exactly the case STOPROW-1 says the status must tell apart; and `0` in NOT-RUN collides with t = n+1. |
| (c) a separate receipt line | `status LOG-OPEN` plus a line such as `read-once absent` | Keeps the status words unchanged, but his STOPROW-1 answer puts the mark in "the receipt's status"; a separate line would need his word that it counts as the status. |

### 8.2 The read-once NOT-RUN's t (15.7.5, 15.5)

- Under 8.1 (a): **no t.** The stop is before any tick, so the field is replaced by `READ-ONCE`. PROPOSED.
- Under 8.1 (b): t = 0.
- Otherwise: t = n+1 = 1, which names a tick that the stop never reaches.

### 8.3 The end record of a read-once NOT-RUN log (condition 5)

| option | the record | entails |
|---|---|---|
| **(a)** (PROPOSED, with 8.1 (a)) | `end 0 not-run read-once INPUT-MISSING <port>` | Loads only when `<port>` is a read-once port of the law and the log holds no tick record. Mirrors 8.1 (a) in the log's lowercase style. |
| (b) | `end 0 not-run 0 INPUT-MISSING <port>` | Round D's form; breaks t = n+1 for this one case. |
| (c) | `end 0 not-run 1 INPUT-MISSING <port>` | Keeps t = n+1, but names tick 1 for a stop before every tick. |

### 8.4 The header-only log of a law with a read-once port

RO′-3 already makes it LOG-OPEN when the log has no end record. **[follows: RO′-3, RO′-5]** What needs ruling is only
its status bytes, which 8.1 decides: under (a), `status LOG-OPEN READ-ONCE`. Shown here so that no ruling on 8.1 is
read as silent about it.

### 8.5 Which other logs lacking the read-once record are malformed (15.5)

PROPOSED, after packet F's list: for a law that declares a read-once port, a log that lacks the read-once record loads
only as the header alone (8.4) or the header with the end record of 8.3. Every other such log is refused at load,
before any statement runs:
- the header then a tick record (no read-once record before it);
- the header then `end 0 closed` (COMPLETED never stands for it, RO′-5);
- the header then a `not-run` naming an each-tick port.

Which LOG-* code each refusal carries is packet D's (§2), not this packet's. This also presupposes the read-once
record's own line, its keyword (`once` or `t 0`) and its presence rule, which stay open in packets C and D; a ruling
here should name the record's line as still open or rule it alongside.

### 8.6 The version-1 NOT-RUN and LOG-OPEN status encoding (the tick case)

Separate, as his safeguard asks. 8.1 (a) presupposes that the tick case keeps the forms 15.7.5 states. PROPOSED:
- `status NOT-RUN <t> INPUT-MISSING <port>`: t in decimal ASCII with no leading zero, `<port>` the each-tick port's
  name, one space between tokens;
- `status LOG-OPEN`, with nothing after it.

A ruling on 8.1 does not rule 8.6, and a ruling on 8.6 does not rule 8.1.

## 4. What the decisions touch

- **Clauses of draft 10:** 15.5 (the end record; logs lacking the record), 15.7.1 (the stop), 15.7.5 (the statuses),
  15.8 (the status line), 15.11 (replay), 15.13.8 (the court chooses the row from the status), and 15.15's rows on 15.5
  and 15.6, 15.5 and 15.7.5, and 15.7.5 and 15.8.
- **CUT-0:** the row choice reads the status's second token. Under 8.1 (a) the rule is: `READ-ONCE`, the stop's row;
  otherwise the NOT-RUN/LOG-OPEN row. This is an input of the pinned rule, so it is fixed before the pin.
- **The ledger:** T10.7 and T10.8 (`ROUNDS.md`) state their cases by the record's presence; they would cite the status
  form as the court's way of knowing it. T14 (the outcomes) gains no fifth outcome.
- **Version 0:** untouched. Every form here is version 1's, so COMPAT-0's frozen texts are not affected.

## 5. The tests and records that would establish compliance (for 1a; none run)

- Serializer and parser round-trip every status form of 8.1 and 8.6, and every end record of 8.3.
- **Row choice from the receipt alone:** the court picks the stop's row from `READ-ONCE` and the NOT-RUN/LOG-OPEN row
  otherwise. Plant: a reader that infers the stop from the log or the trace; the row must fail.
- **Telling the cases apart:** a law with a read-once port, a header-only log, gives `status LOG-OPEN READ-ONCE`; the
  same law, its record present and no tick, gives `status LOG-OPEN`. Plant: the stop written as plain `LOG-OPEN`.
- **The loadable stop log:** `end 0 not-run read-once INPUT-MISSING g` loads for a law whose g is read once, and is
  refused for a law whose g is read each tick. Plant: the parser's t = n+1 check left applying to it.
- **Malformed logs of 8.5:** each refused at load, before any event. Plant: one of them accepted.
- **Version 0:** COMPAT-0 HELD unchanged.
- In 1b: the four executions write these status lines byte for byte alike.

## 6. A falsifier for the recommendation

8.1 (a) fails if some version-1 run would need a status whose second token is neither a decimal t nor `READ-ONCE`,
and so could not be told apart by that token: for example a stop that also names a tick. None is known; a probe over
the research model's logs, extended with read-once ports, would look for one.

## 7. The questions for him

1. **8.1:** which status form marks the stop: (a) `READ-ONCE` in the second place, (b) t = 0, or (c) a separate line?
2. **8.2 and 8.3:** with it, the stop's NOT-RUN t, and the end record of a read-once NOT-RUN log.
3. **8.5:** which other logs lacking the record are malformed, and whether the read-once record's own line is ruled now
   or named open.
4. **8.6:** the tick case's NOT-RUN and LOG-OPEN encoding, as its own ruling.

8.4 follows from RO′-3 once 8.1 is ruled. Nothing is pinned, built or committed on an assumed answer.
