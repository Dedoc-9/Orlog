# SPEC §15, draft 12: version 1, the open run (2026-10-27; research, not yet in SPEC.md)

**Status.** Draft 12 applies to draft 11 the dispositions of R7's ninth re-read (`twin-r7/REREAD-9-DISPOSITION.md`),
adopted by the owner on 2026-10-29 with his answers to its five questions (`RULINGS.md`, "Re-read 9's five
questions"). Draft 6 is the draft of the release pushed as 9de2792; drafts 0 to 11 are kept as they were.
`twin-r7/DRAFT-12-CHANGES.md` lists what draft 12 changes, and the twin reads the whole of it before it is built
(R7). The draft moves into `SPEC.md` as §15 only once its open clauses are ruled. Everything not stated here is version 0, as
SPEC §1–§14 and RUNTIME-SPEC.md define it. Nothing here is built, and nothing here clears a blocker.

**How to read the tags.** Every clause carries one:
- **[ruled: R2, R3, R4, R5, R6, R9]** — fixed by the owner's ruling of that name. The clause states what the ruling
  fixes; quoted words are his. R2 includes his clarification of R2.3; R9 is his ruling on the budget, B1 to B4.
- **[ruled: F8]** — fixed by his rulings on finding 8: packet G's 8.1 to 8.6, the read-once record's line, packet
  D's D1 to D3 and typed values, T1 to T6 (2026-10-28 and 2026-10-29).
- **[ruled: F20]** — fixed by his rulings on finding 20, F20.1 to F20.4 (2026-10-29).
- **[ruled: PP]** — fixed by his port-place ruling, PP1 to PP6 (2026-10-29).
- **[ruled: counting]** — fixed by his counting rulings, C1 to C3 (2026-10-29).
- **[ruled: N2]**, **[ruled: N3]**, **[ruled: F10]** — fixed by his rulings of those names (2026-10-29).
- **[ruled: claims]** — fixed by the claims ruling: E2, and the meet; and by his answers that order its pin: the
  order of work, findings 8 and 20 resolved before the pin, and every input the pinned rule reads, in every row of
  CUT-0, fixed before it (2026-10-27).
- **[ruled: F24]** — fixed by his ruling on finding 24 of R7's review: D10's court clause, scoped to real court
  readings; and by his rulings of 2026-10-27 on R6's control and on the labels' definitions, which adopt D's.
- **[ruled: PREFIX]** — fixed by his ruling on the PREFIX licence: B1 + 4a + 5c + K1, with its conditions; and by his
  rulings on the labels' definitions, the closure's rule table and its Perform row (2026-10-27). A label's definition is ruled, not
  the conclusions drawn from it.
- **[pinned]** — fixed by the artifacts the claims ruling names, not by its words: the exact CUT-0 digest the meet
  must name, and the court's R8 as built. No digest is pinned yet, so a [pinned] clause states what is proposed for
  pinning, and it can change until the pin.
- **[v0]** — as version 0 already defines it (SPEC §1–§14, RUNTIME-SPEC.md, the court as built).
- **[open: X]** — not ruled. The clause gives the current proposal, and X names what decides it: a sheet item (R1,
  R8, R10 to R12, D1 to D10), a row of the amended set, contract draft 0 (the source of a proposal no ruling has
  adopted), or a question found here. An open clause is a proposal, never a rule.
- **[fixed]** — holds whatever is ruled. The ruling sheet's list "Fixed whatever is ruled" has three entries: COMPAT-0
  must hold, so every version-1 form is spelled only where version 0 refuses SYNTAX at the statement; no word is newly
  reserved; and the spellings' measurement.
- **[ruled: F6]** — fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′-6, with six conditions; and
  by his answers on the read-once stop's row, its version-1 check, its receipt status, the owed check, the order of
  work, the check as a fixture test, and RO′-5 confirmed (2026-10-27).
- **[follows: X]** — not ruled itself: a statement drawn from the rulings and clauses X names, as sound as they are,
  and changed when they change.

**Two names clash, and are kept apart here.** "R8" in the ruling sheet is **float ports** (open). "R8" in the court
is **the settlement rule for a refused evaluation** (built). This draft writes the first as *sheet R8* and the second
as *the court's R8*.

## 15.0 Terms

- **Version 1 law:** a law whose source has a port or a tick block. Its header line reads `orlog-law 1`; every other
  law keeps `orlog-law 0` and its version-0 bytes. **[ruled: R5]**
- **Port:** a declared input, read **each tick** or **once**, with a name and a type: `an integer`, `a fixed`,
  `a truth value` or `a text`. A port is read-only. A port declaration is one statement kind; its mode, type and name
  are its attributes (R2.1). Float ports are not in version 1 unless sheet R8 rules them. **[ruled: R2; open: sheet
  R8]**
- **Prefix:** the top-level statements before the tick block, or all of them in a law with none (PP3). **Tick
  block:** the last top-level clause, at most one. **[ruled: R2; PP, PP2; follows: PP3]** (Not the PREFIX licence: which claims are licensed is 15.12.4's.)
- **Boundary:** the first top-level clause, in the text, that is or holds a port declaration, or is the tick block.
  A law with a tick block and no port has its boundary at the tick block. **[ruled: PREFIX]**
- **Arrival:** bytes sent toward a port by a source. **Door:** the function that judges an arrival. **Host:** the
  program that receives arrivals, keeps the records and starts an execution. **Session:** the history of one host's
  events (§15.4). **[open: amended set "A2"]**
- **Input log:** what the law reads (§15.5). **[open: amended set "identity and bytes"]**
- **Execution:** the reference or a compiled backend running one law over one input log. **[v0, with the input log]**

## 15.1 The forms

1. **Spellings.** **[ruled: R2, R2.1 and R2.2]** Version 1 adds exactly two statement kinds: the port declaration,
   with a mode (each tick or once), a type and a name; and the tick block, with its body and an optional budget, the
   budget an attribute. Kind and mode are in version 1's law bytes, so a change of a port's mode alone changes the
   law seal. The spellings are exactly:
   - a port read each tick: `Let <name> be given each tick as <type>.`
   - a port read once: `Let <name> be given as <type>.`
   - the tick block: `Each tick, do the following.`
   - with a budget: `Each tick, at most <N> operations, do the following.`
   `<type>` is `an integer`, `a fixed`, `a truth value` or `a text`; `truth value` and `text` are type words only
   within the port form, and `a float` is excluded until sheet R8. `<N>` is written as version 0 writes a numeric
   bound; capitals, punctuation and the door's repairs are version 0's sentence treatment, a clause a sentence ending
   in a period. `For each tick, …`, `On each tick, …`, `Receive …` and `Take …` are rejected, and no `Input` keyword
   is added. Each kind has its row of the closure's table (15.12.4). R2 is ruled before CUT-0's digest is pinned,
   so CUT-0's closure is defined across every supported statement kind. **[ruled: R2; claims, his clarification
   that the principle reaches every row]**
2. **Every form is spelled only where version 0 refuses SYNTAX at the statement**, so no accepted version-0 text
   changes meaning. No word is newly reserved. **[fixed]**
3. **Places.** **[ruled: PP, PP1 to PP6]**
   - A port is declared only as a top-level clause, before the tick block; prefix statements may stand before,
     between and after port declarations. A declaration in an If, a loop, a procedure, the tick body or an inline
     arm is refused PORT-PLACE (PP1).
   - At most one tick block, the last top-level clause; a second, a nested one, or one followed by a top-level
     clause is refused TICK-PLACE (PP2).
   - Read-once ports alone are allowed, a one-shot law with inputs; an each-tick port with no tick block is refused
     PORT-PLACE; a tick block with no port is allowed (PP3).
   - An each-tick port is read only in the tick body or in a procedure reached only from it; a read-once port only
     after its declaration in the execution structure. Both the text and the evaluation reach are checked, by the
     closure's rules (15.12.4); a procedure's reachable call contexts, not its place in the text, decide its reads.
     A violation is PORT-READ (PP4).
   - Set, Increase, Decrease, Append or Remove on a port, and a port as a For counter, are PORT-VARIABLE; a second
     declaration of a port's name, a second `Let` included, is REDECLARED, version 0's code, since every
     `Let X be E` declares X (PP5).
   - PORT-PLACE, TICK-PLACE, PORT-READ and PORT-VARIABLE are phase-6 codes of SPEC §13, in its document walk order,
     the first faulty clause winning; SPEC §13's table and the self-test's row change with them (PP6).
   The read-once stop's row (15.13.8) reads this place, so it is resolved before CUT-0's digest is pinned. **[ruled:
   claims, his answer on the pin's inputs]**
4. **The law's lines.** `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`. **[ruled: R5]**
   With no budget the ` budget <N>` part is omitted, and no budget of zero is encoded. **[ruled: R5; his answer on
   S15.1-1]** How `<type>` is spelled in the line is open. **[open: amended set "identity and bytes"]**
5. **The door and the forms agree.** SPEC §1 reads a line as a label, one space, then the statement. A form whose line
   reaches its label only past leading spaces, or only after the door repairs a byte, is classified as the same line
   written at column one is. Each form's recognition, its parse or refusal, and that classification are one decision.
   **[open: amended set "H2", in a change of its own, with E18's COMPAT-0 settlement]**
6. **A world property** (gravity, a constant of the scene) is proposed as a port read once. **[open: R1]** Its cost is
   his sentence: "Moving a world property out of the law and into a read-once port means the cost of rule a reaches
   every later claim in the run, stripping them of grounding even if they never touch that property directly."
   Grounding is §15.12. **[ruled: R6]** Under the PREFIX licence a claim is unlicensed if it stands at or after the
   boundary, or if a clause from the boundary on may execute it, and the boundary is never after this port's
   declaration; so every later claim is among them, whether it stands later or is evaluated later (15.12.4).
   **[follows: R6; PREFIX; 15.0 Boundary]**

## 15.2 The door

**[ruled: R3]** The door never rounds: a decimal that is not exactly a Fix value is refused, and inputs arrive on the
2^-32 grid or as raw values. "The entrance tool filters all incoming port streams using a restrictive ASCII regular
expression sieve", before any number is parsed. **[open: whether the ASCII sieve governs text ports, whose bytes R3
also keeps as sent (finding 13)]**

**[open: contract draft 0 §1.2–§1.3]** The door is a pure function of (the port's declaration, the arrival's bytes),
and its version is named in the input log's header. Its rules apply in order, and the first rule a value breaks is
its refusal:
1. **The bytes must match the port type's grammar exactly.** Otherwise INPUT-SYNTAX. The integer and decimal
   grammars are not given here. **[open: R3's details for 1a]**
2. **`an integer`:** any fraction or decimal component refuses INPUT-NOT-INTEGER; "Truncation or automatic
   floor-rounding at the gate is blocked." A value outside [−2^63, 2^63−1] refuses INPUT-RANGE. **[ruled: R3]**
3. **`a fixed`:** **[ruled: R3, except where marked]**
   - The value must sit within the raw bounds of a Fix, raw −2^63 to raw 2^63−1 (×2^−32), "actively protecting the
     lower negative boundary against floor overflow errors down to −2147483648.5". Outside them refuses INPUT-RANGE.
   - A value off the 2^−32 grid refuses INPUT-GRID, and the refusal names "the two nearest valid representable grid
     coordinates".
   - The range is checked before the grid. **[open: contract draft 0]**
   - A raw value is written in hexadecimal, with a prefix of its own in the grammar: "Raw hexadecimal scalar strings
     are given an isolated syntactic prefix". **[open: the prefix, and how a sign is written]**
4. **`a truth value`:** exactly one spelling for true and one for false. "Alternative representations, case
   variations, or numeric bits (`1`/`0`) are refused", as INPUT-SYNTAX. **[ruled: R3; open: the two spellings]**
5. **`a text`:** **[ruled: R3, except where marked]**
   - "String inputs are preserved byte-for-byte as sent."
   - A text not in NFC is accepted, with a note in the door's report. The note is recomputable from the bytes.
     **[open: contract draft 0]**
   - "CP1252 character maps are rejected outright." Bytes that are not UTF-8 refuse INPUT-NOT-UTF8. **[open: the code
     for CP1252 text whose bytes are valid UTF-8]**
   - **[open: whether text also refuses what the literal door refuses]**

**[ruled: R3]** The log holds typed encodings only (RUNTIME-SPEC §5), written once by a Python input door, so no
runtime ever parses decimal text. **[open: contract draft 0; R3 gives reversibility under COMPAT-0 as a reason, not
this rule]** A later version may relax a refusal into acceptance, never the reverse.

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
  ASSIGN-AHEAD, SLOT-FILLED, AFTER-END, UNKNOWN-PORT, NO-ARRIVAL, END-PENDING, END-UNDISPOSED, RUN-REFUSED. A refused
  move is not appended to the history, and the session's state does not change.
- **Every arrival has exactly one disposition**, derived from the history: refused with its code, assigned to its
  tick, dropped, or unconsumed.
- **Read-once ports.** **[ruled: F6]** A read-once value reaches the session only as an arrival, judged by the door
  at once; a refused arrival is never assigned; a retry is a new arrival; neither ends the session. The read-once
  ports have one record, filled by assigning accepted arrivals, at most one per port, and closed once before any tick
  record; it is written whole or not at all. A law with no read-once port is unchanged. When the run starts and
  where it stops is 15.7.1's.
  - An `end()` before the read-once record closes is legal and is the read-once stop. It projects to `end 0 not-run
    read-once INPUT-MISSING <port>`, the first empty read-once port in declaration order, and the receipt reads
    `status NOT-RUN READ-ONCE INPUT-MISSING <port>`. END-UNDISPOSED still applies; a partly filled record is not
    written to the log, its assignments staying in the history; the verifier checks the port against the history.
    **[ruled: N2]**
  - At the session's opening, before it accepts its first event, the host runs the top-level statements before the
    first read-once declaration. A refusal there is known at once and writes `'R'` with its cut, and every later
    move but `end()` is refused RUN-REFUSED. If they complete, the run waits at the first read-once declaration until
    the record closes; then each read-once `'N'` is emitted at its own declaration as execution reaches it, never
    grouped at the first, so the live trace equals replay's (RO′-3). **[ruled: N3; his answer on S15.3-1]**
  - When the host runs the prefix of a law with no read-once port, and when a refusal there is known, is open.
    **[open: amended set "A2"]**
  - Still open: the events that fill and close the record (an `assign` names a tick, and `close()` covers each-tick
    ports only); whether tick 1 may close before the record; a close with a slot empty. **[open: amended set
    "A2"]**
- **No value is invented, held over or defaulted,** until SNAP-1's continuation rule. A tick that does not run stops
  every port of it, and the session. **[open: contract draft 0 §1.5; amended set "A2"]**
- **A retry is a new arrival;** the refusal before it stays in the history. The host never advances while a source
  retries, because advancing is closing.
- **A door refusal or a refused move does not end the session.** **[open: amended set "A2"]**
- **Until SNAP-1, a refusal of the run ends the session.** A refusal ends its branch at the tick. The refused branch
  is kept, sealed and queryable. The court reads each branch on its own and names every abandoned branch. **[ruled:
  R4]**
- **A refused session's log carries no end record.** The projection of an `end()` after a refusal appends nothing:
  the log ends with the refused tick's record, or, for a refusal before any tick, with the header alone, or the
  header and the `once` line if the record closed whole. The log asserts no refusal: running it gives `status
  REFUSED <CODE> <clause>`, `ticks` counting the refused tick, the unread count 0, and `'R'` with its cut. Whether
  `end()` happened is the session record's (15.4), never the log's. **[ruled: F10]**

## 15.4 The session record, `orlog-session 0`

**[open: amended set "session record" and "binding"]**
- **The history is a record of its own:** sources, door verdicts, assignments, drops, closes and the end, chained.
- **Three records, three authorities:**
  - the receipt core attests one execution over its input log (§15.8);
  - the session record attests the session: `history-sha256`, `input-log-sha256` and `receipt-core-sha256`;
  - the arbiter's agreement record attests the compared executions, their identities and the verdict.
- **The verifier checks the chain:** the history is legal; the log is its projection, or HISTORY-MISMATCH; the core
  is the log's run, or CORE-MISMATCH; the record names all three, or SESSION-MISMATCH.
- **For a refused session** the verifier also checks that the history reaches a refusal and then `end()`, that the
  log is exactly its projection with no end record, and that running the log gives the live run's receipt core and
  refusal place; a log with an end record, a record after the refused tick, or a refusal elsewhere is
  HISTORY-MISMATCH. **[ruled: F10]**
- **Two histories with one input log share one core.** That is law-equivalence, by design: a receipt never stands for
  a session.

## 15.5 The input log, `orlog-inputs 0`

**[open: amended set "identity and bytes"]** A stream of LF-terminated ASCII lines, parsed strictly. Every field is
matched whole, and the parser accepts exactly what the serializer writes:
- **The header:** `orlog-inputs 0`; `ports <the port signature's sha256>` (§15.6); `door <the door's version>`.
- **The read-once record:** `once <v1> <v2> …`, written only when the law declares a read-once port and the record
  closed whole, as the fourth line, straight after the header and before any tick record; one value per read-once
  port, in declaration order. It is never a tick record and n does not count it. **[ruled: F6, when present; F8,
  the line]** Then one record per tick, in tick order from 1: `t <n>`, then every each-tick port's value in
  declaration order, densely. With no each-tick port the line is `t <n>`, with no trailing space.
- **Values,** in both, are tagged: each is its full RUNTIME-SPEC §5 encoding, tag included, as lowercase hex, equal
  to the value part of its `'N'` payload (the fixed number 3 is `580000000300000000`, true `4201`, the text "hi"
  `54000000026869`). Only `I`, `X`, `B` and `T`; `F` only if sheet R8 rules float ports; `L` never. Each value has
  exactly one spelling. One space between tokens. **[ruled: F8, T1, T2, T5 and T6; the example as corrected by his
  answer on S15.5-1]**
- **Optionally, one end record,** n the number of tick records:
  - `end <n> closed`;
  - `end <n> not-run <t> INPUT-MISSING <port>`: t = n + 1, in decimal ASCII without a leading zero, and the port an
    each-tick port of the law; a law with no each-tick port has no such record (8.6);
  - `end 0 not-run read-once INPUT-MISSING <port>`, the read-once stop's: it loads only when the law declares a
    read-once port, the log holds no read-once record and no tick record, and the port is one of its read-once
    ports; whether it is the first empty one is the verifier's (8.3).
  **[ruled: F8, 8.3 and 8.6]** INPUT-REFUSED belongs to the candidate A1, not to A2.
- **A law with read-once ports and no tick block** has no tick records: a `t` line is refused LOG-RECORD, and its
  end records are `end 0 closed` and the read-once stop's. **[ruled: his answer on S15.5-2]**
- **A log with no end record is open.**
- **A well-formed log may lack the read-once record.** For a law that declares a read-once port, such a log loads
  only as the header alone (exactly its three LF-terminated lines; `status LOG-OPEN READ-ONCE` when the run reaches the first read-once
  declaration, REFUSED when it refuses before it, RO′-4) or as the header
  with the read-once stop's end record. Every other log lacking the record is malformed, refused at load: a tick
  record where the record should be (M1), `end 0 closed` (M2), a tick's NOT-RUN (M3), and the stop's record naming
  an each-tick port (M4). For a law with no read-once port, a `not-run read-once` end record is refused. **[ruled:
  F6, condition 5; F8, 8.4 and 8.5]**
- **The log is parsed whole before any execution starts.** A malformed log is refused at load, before any execution
  starts (contract draft 0 §2.2): "A malformed log is rejected before any statement executes." This stays mandatory,
  and a well-formed log without the read-once record is a distinct case, never a malformed one. **[ruled: F6,
  condition 1]**
- **Load refusals.** Nine codes replace contract draft 0's single LOG-MALFORMED, and no other is added (D1.a): the
  read-once record's faults take these codes. LOG-NOT-ASCII is a byte above 0x7F, a CR being LOG-LINE (D1.b); a
  leading LF is LOG-LINE (D1.c); an input log offered with a version-0 law is a usage error, outside the codes
  (D1.d). Each case's code is the table below, as put to him with D1.a. A value's faults are LOG-RECORD (T4).
  **[ruled: F8, D1.a to D1.d, the table as put; T4]**

| case | code |
|---|---|
| a byte above 0x7F | LOG-NOT-ASCII |
| a CR, no final LF, or an empty line (a leading LF included) | LOG-LINE |
| a missing or wrong header line, or an unknown door version | LOG-HEADER |
| the ports line's digest is not the law's port signature | PORT-SIGNATURE |
| a line whose kind is not `t`, `end` or `once` | LOG-UNKNOWN |
| a `once` line with the wrong number of values, a value of the wrong form, in a law with no read-once port, not at line 4, or twice | LOG-RECORD |
| M1: a tick record where the read-once record should be | LOG-RECORD |
| a tick record with the wrong value count, or a value of the wrong form | LOG-RECORD |
| a tick record in a law with no tick block (his answer on S15.5-2) | LOG-RECORD |
| a tick number not canonical, or not one more than the ticks before it (so `t 0` too, except at line 4 in a read-once law, which is M1, LOG-RECORD, by D2.4) | LOG-TICK |
| M2 `end 0 closed`, M3, M4, a failed condition of the stop's end record (8.3), or of a tick's NOT-RUN (8.6) | LOG-END |
| any line after the end record | LOG-AFTER-END |

- **The order of checks.** The law compiles first; a compile fault means the log is never read (D2.1). Then
  LOG-NOT-ASCII, LOG-LINE, LOG-HEADER (line 1, the line count, line 3, then line 2's form; D2.6), PORT-SIGNATURE, and
  the lines from line 4 (D2.2), the earliest faulty line winning (D2.3). Within a line: LOG-AFTER-END, the line's
  kind (LOG-UNKNOWN), the read-once placement (LOG-RECORD), a `once` line's content, a `t` line's content, an `end`
  line's conditions (D2.4); in a tick record, the value count, then the tick number, then the values (D2.5); in a
  value, the hex's form, the tag, the exact length, then a text's UTF-8 and door rules, those R3's (T3). **[ruled:
  F8, D2.1 to D2.6 and T3; open: R3, the text's door rules]**
- **A load refusal writes no receipt** (D3.1). Only the nine codes count as load refusals; a compile refusal, a
  version-0 usage error and a log I/O failure do not (D3.2). After its code and line are final, it writes a refusal
  witness through a temporary file renamed into place, beside the receipt's place under its own name (D3.3): the
  LF-terminated ASCII lines `orlog-load-refusal 0`, `law-seal <seal>`, `code <CODE>`, `line <n>` (1-based; for
  LOG-NOT-ASCII the line of the first byte above 0x7F; for LOG-LINE that of the first CR or empty line, or the last
  line without its LF; for LOG-HEADER the faulty header line, or the count of lines plus 1; for PORT-SIGNATURE 2),
  `log-bytes-sha256 <hex>` (every byte as read, never named `input-log-sha256`) and `end`, with no timestamp or host
  detail; diagnostics go to standard error, and it is not a court record (D3.4). A failed witness write gives
  RUNTIME-SPEC §1's I/O-failure exit, the code and line kept on standard error (D3.5). **[ruled: F8, D3.1 to
  D3.5]** The command line exits 1 on a load refusal, as on a compile refusal (SPEC §11 G2). How a 1b runtime
  refuses a log, and its exit code, is open: RUNTIME-SPEC §1 gives 0, 2 and 3. **[follows: G2; open: 1b's
  specification]**
- **The chain:** in_0 = SHA-256("orlog-inputs 0" ‖ the header's bytes, with the read-once record, when present);
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
   - A read-once port binds where its declaration stands, emitting its `'N'` event before the first `'T'`. **[ruled:
     R5, that its `'N'` comes before the first `'T'`; F6, where it binds]** The PREFIX licence presupposes this place
     (15.12.4).
   - A run executes the top-level clauses before the first read-once declaration whatever the log holds, provided
     the log loads. If the log holds the read-once record, the run goes on. If it does not, the run stops before the
     first read-once declaration, even when the missing value is a later port's: NOT-RUN naming the read-once port
     the end record names (the first empty one in declaration order, checked against the history), or LOG-OPEN if
     the log has no end record. No `'N'` is emitted, and no value is invented, held over, defaulted or bound from
     another read-once port. A refusal before that declaration is REFUSED, whatever the log holds. **[ruled: F6]**
     The check against the history is the verifier's (15.4): an execution over a log has none. **[follows: 15.4]**
   - Each tick emits `'T'`, then one `'N'` per each-tick port in declaration order, then runs the tick block's body.
   - Binding a port counts no operation, and reading a port counts none, as reading a variable. **[ruled: counting,
     C1]** The read-once stop's row (15.13.8) reads it, and it is resolved before CUT-0's digest is pinned. **[ruled:
     claims, his answer on the pin's inputs]**
2. **`'T'`'s payload is (t, c), both u64.** **[ruled: R5, amendment 1]**
   - c is the running total of `ops` from the start of the run to the moment `'T'` is emitted. It never decreases and
     includes the prefix; a tick's own count is the difference between consecutive `'T'` counts, and the receipt's
     `ops` is the final total. **[ruled: counting, C2]**
   - Nothing new is counted: the tick block adds no operation, emitting `'T'` or `'N'` counts none, and an empty tick
     body costs none. Version 0's rule stands: the single `ops` counter gains 1 immediately before each counted
     operation, and an If arm's count belongs to the arm's own clause. **[ruled: counting, C1 and C3]**
3. **The budget.** **[ruled: R9, B1 to B4]**
   - The optional budget is part of the law, under its seal. A tick past it refuses TICK-BUDGET at the same counted
     operation in every execution; a host stop stays STOPPED-BY-HOST, never a verdict, never an `'R'` (B1).
   - N is an integer literal from 1 to 2^62; `at most 0` and anything above 2^62 are refused at compile time, with
     version 0's FUEL. With no budget the law line omits its budget part (R5's form), and a written budget of zero is not allowed (B2;
     his answer on S15.1-1).
   - A tick's count starts at 0 at its `'T'`, and the prefix is never charged. When an increment makes the tick's
     count N + 1, that operation is counted, in `ops`, and refused before it executes: TICK-BUDGET, at the clause
     whose statement is executing, an If condition's arm's own clause (SPEC §11 item 18; F20.4); `tick-ops` is
     exactly N + 1 (B3).
   - TICK-BUDGET is an ordinary refusal under finding 20: `'R'` carries the code and the statement stack at the
     refused operation, its last frame any permitted kind, a Perform included; the status is `REFUSED TICK-BUDGET
     <clause>`, and `ticks` counts the refused tick; a claim whose evaluation holds the refused operation is open at
     the cut, and the court's R8 does not hold it (B4).
4. **A refusal of any code ends the run at once.** **[ruled: R4]** The tick records after it are not executed; the log
   was parsed whole (§15.5), so their number is known. **[open: contract draft 0 §4.4]**
5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]**
   - COMPLETED: every tick record ran, and the end record's cause is `closed`.
   - REFUSED <CODE> <clause>: a refusal in the prefix or in a tick. The tick is the receipt's `ticks` (§15.8).
   - `NOT-RUN <t> INPUT-MISSING <port>`: every record before t ran, and the end record names tick t as not run; t in
     decimal ASCII without a leading zero, equal to the end record's, and the port an each-tick port. **[ruled: F8,
     8.6]**
   - `LOG-OPEN`, with nothing after it: every record of an open log ran, with no refusal. A refusal inside an open
     log is REFUSED. **[ruled: F8, 8.6, the form]**
   - The stop of 15.7.1 is a case of NOT-RUN or LOG-OPEN, not a fifth status. COMPLETED never stands for a law with
     a read-once port whose log lacks the record. **[ruled: F6]** The stop's receipt status is NOT-RUN or LOG-OPEN in
     an explicit distinguishing status form, never a fifth status word, distinguishing the stop from a LOG-OPEN run
     that holds the read-once record but ran no tick. **[ruled: F6, RO′-5; his answer on STOPROW-1 and his
     confirmation of RO′-5]** The form is the keyword `READ-ONCE` in the second token place: `status NOT-RUN
     READ-ONCE INPUT-MISSING <port>`, naming a read-once port (RO′-3), and `status LOG-OPEN READ-ONCE`. The stop's
     NOT-RUN carries no t: the stop comes before any tick. **[ruled: F8, 8.1 and 8.2]**
   - CUT-0 chooses its row by the status's second token: a decimal number, a tick's NOT-RUN; `READ-ONCE`, the
     read-once stop; none, the ordinary LOG-OPEN. These encodings are fixed before CUT-0's digest is pinned. **[ruled:
     F8, 8.6; claims, his clarification that the principle reaches every row]**
6. **The output chain.** **[ruled: R5, amendment 2]**
   - out_0 hashes what was written before the first `'T'`. His words for it: "the initial hash of any visual bytes or
     metadata written before the first tick". This draft reads the output as holding nothing but the bytes said, and
     writes out_0 = SHA-256("orlog-output-1" ‖ SHA-256(the bytes said before the first `'T'`)). The reading and the
     domain string are contract draft 0's. **[open: amended set "identity and bytes"]**
   - out_t = SHA-256(out_{t−1} ‖ SHA-256(the bytes said during tick t)).
   - A refused tick's partial output is its out_t, the chain's last link: "if a tick encounters a transactional
     refusal, its partial output is formally hashed into the chain before the rollback logic clears the volatile
     state".

## 15.8 The receipt, `orlog-receipt 1`

**[ruled: R5]** Lines, in order:
- `orlog-receipt 1`
- `backend <name>`
- `law-seal`, `text-seal`, `input-log-sha256`
- `status` (§15.7.5)
- `ticks <n>`: the ticks begun, a refused tick included and a not-run tick not **[ruled: R5, amendment 3]**
- `tick-ops <n>`: the last begun tick's own count, complete or partial; exactly N+1 under TICK-BUDGET **[ruled: R9,
  B3, under TICK-BUDGET; open: amended set "identity and bytes", when no tick began]**
- the count of tick records left unread after a refusal **[open: amended set "identity and bytes"; its name too]**
- `output-bytes`, `output-chain`
- `events`, `trace-head`
- `ops`: every counted operation, the refused one included
- `claims`, then one `claim` line each, as in version 0
- `end`

The line order is this draft's. **[open: amended set "identity and bytes"]**

Then:
- **The core** is the receipt without its `backend` line. Executions agree when their cores are byte-identical.
  **[v0]**
- **The frame check is versioned.** **[ruled: R5, amendment 4]** A law headed `orlog-law 0` requires a receipt
  beginning `orlog-receipt 0`; a law headed `orlog-law 1` requires `orlog-receipt 1`. Never either for any law. Its
  plants: a version-1 receipt checked under the version-0 frame must fail, and a version-0 receipt under the
  version-1 frame must be refused.
- **No receipt line states that a run is valid or correct.** **[open: contract draft 0 §5.4]**

## 15.9 The trace, `orlog-trace-1`

- **The head.** head_0 = SHA-256("orlog-trace-1" ‖ law_seal). Each event extends the head as in version 0, with
  version 0's events and `'T'` and `'N'`. The per-event chain is kept, not replaced by a stream head. **[ruled: R5]**
- **`'N'`'s payload** is the port's variable number (u32) and the value encoding of RUNTIME-SPEC §5. **[ruled: R5]**
  Its value bytes are the log's value bytes, tag included. **[ruled: F8, T1]**
- **The `'R'` event carries the refusal cut** in version 1. The trace head commits it, and the receipt core binds the
  head, so the four executions agree on it; the court decodes the recorded cut, never reruns the reference for it:
  "The court must not silently derive it from execution instead." Version 0's `'R'` payload stays the code alone.
  **[ruled: F20, F20.1; claims, his answer on the pin's inputs]**
  - **The decoding.** The law's header selects the grammar, never the payload's look; the code must equal the status
    line's; at least one frame; the frames hold to shapes S1 to S7 (`CUT-SCHEMA.md`); only each frame's clause and
    selector, a For's bit where it is not the last frame, and a last-frame If's arm are read, and the pinned rule
    computes K̂ from them, reading no value or operation count. A malformed payload is refused with its reason, with
    no fall-back to version 0's grammar. **[ruled: F20, F20.2]**
  - **Version 1's frames.** The tick block is a plain frame, its clause with selector 0xFFFF and no extra field; a
    port declaration has no frame; a Perform may be the last frame, TICK-BUDGET's case included; a refusal inside an
    If's condition names the arm's clause, as in version 0. **[ruled: F20, F20.3 and F20.4]**
  - **The bytes.** The proposal is `CUT-SCHEMA.md`'s draft 2: the code's length and the code, the frame count, then
    per frame a u32 clause, a u16 selector, a bit for a For that is not the last frame, and an arm for an If that is
    the last frame. His ruling adopts the semantic rule, not this byte grammar. On version-0 stand-ins the layout
    holds version 1's frame kinds as the rulings read them (`evidence/run1-cut0-schema-v1-standins.txt`,
    2026-10-29): MEASURED on those stand-ins only, never on a version-1 interpreter, and it freezes no format.
    The pinned decoding rule identifies the exact byte grammar it decodes. Draft 2 is the candidate to test, not an
    adopted or frozen format: the version-1 reference tests S1 to S7 against it during the containment step, and a
    discrepancy is resolved before the pin. That is a prerequisite of the pin, not the general format freeze.
    **[ruled: F20, F20.2's qualification; his answer on S15.9-1; open: the format freeze (P6), on its own
    trigger]**
  - Why it needed a ruling: R5 names `'T'` and `'N'` as version 1's new events and does not change `'R'`.
- **A run that does not refuse emits no `'R'`:** COMPLETED, a tick's NOT-RUN and LOG-OPEN, the read-once stop's
  included. **[follows: F20's compliance; F8, 8.6]**

## 15.10 The tick line, `orlog-ticks 0`

**[ruled: R5: part of 1a]** Written by an execution given a path: one line per tick that ran to its end, and none for
a refused tick. Its fields:
- `tick <t>`, `events <n>`, `ops <n>` (the tick's own count), `output-bytes <n>`;
- `trace-head <hex>`, or `-` in a play build without the chain (sheet R14 if ruled);
- `output-chain <hex>`;
- `claims <hex>` and `state <hex>`: R5 names a claims digest and a state digest. Their definitions here are proposals:
  the SHA-256 of the claim lines as they would read at the tick's end, and the SHA-256 of every top-level variable's
  value encoding in variable order. **[open: 1a's specification]**
- `input-chain <hex>`: in_t. **[open: the speed verdict's proposal, not named in R5's ruling]**

These must hold, under §15.7.2's running total: **[follows: counting, C2]**
- T(t+1).c − T(t).c equals tick t's `ops`;
- T(1).c is the prefix's count;
- the receipt's `ops` minus the last `'T'`'s c is the last tick's count, or a refused tick's partial count.

The state digest's cost on a large state is for 1a's specification. **[open: 1a's specification, as R5 leaves it]**

## 15.11 What a run establishes

- **Replay.** Given the law's bytes, the input log's bytes and the version the law's header names, every conforming
  execution that ends with a receipt writes the same receipt core, the same trace and the same tick lines. A host
  stop writes no receipt (SPEC §12), and a play build without the chain (sheet R14, open) is outside this. A compiler,
  a runtime build or a host is not a condition: a difference under the same three is a defect of an execution.
  **[open: contract draft 0 §9.1]**
- **Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity.**
  **[open: contract draft 0 §9.2]**

## 15.12 The court in a run with an input log: grounding

**[ruled: R6]**
1. **The trigger.** A run has an input log when its law declares a port or has a tick block. A tick block with no
   port still takes input: the log's length sets how many ticks run.
2. **No claim of such a run is GROUNDED, whatever its channel and whatever is ratified, except under the licence
   (4).** GROUNDED also requires held, as in version 0. **[v0, for the second sentence]** So before 1b no claim of a
   version-1 run, a licensed one included, reads GROUNDED in a real court reading, where none is held (15.13.11).
   **[follows: F24 (15.13.11); v0]**
3. **The provenance line.** The court shows the log's seal as provenance for the run, printing exactly
   `rests on input log <input-log-sha256>, unratified`, the receipt's own value.
4. **The licence, PREFIX, decided from the text:** a claim is exempt only if every evaluation of it precedes the
   first input.
   - It must stand before the first port declaration, outside the tick block.
   - It must not sit in a procedure performed at or after the first port declaration. The licence is decided by
     evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still
     runs during it.
   - Nothing the log sets exists before its first input, so a prefix claim's whole claim line is fixed by the law: its
     evaluations, its trues, its cost and its certified clause's cost.
   - A wider licence would exempt a claim with no path from any port, shown by two independent derivations, and must
     then cover the whole claim line, since a certificate's cost reading can move with a port while its truth does not.
     It waits for a trigger (`research/doppler/VERDICT.md`).

   **The licence as ruled.** **[ruled: PREFIX]** The licence is decided from the law's text alone, never from a log
   or a trace. The boundary is the first top-level clause, in the text, that is or holds a port declaration, or is
   the tick block. A claim is licensed exactly when (a) it stands before the boundary and outside the tick block,
   and (b) no clause from the boundary on may execute it. The closure follows every arm, the body of every loop and
   of the tick block, and every procedure performed, transitively, with values ignored. A statement kind the
   closure has no rule for licenses no claim of the law. Its start set is the top-level clause that is or holds the
   boundary, plus every later top-level clause, as K1's adopted definition gives it.
   - A law with a tick block and no port has its boundary at the tick block.
   - B1's label names the boundary as the first port declaration, its wording as the top-level clause that is or
     holds one. They differ only for a port declared inside another clause, which PP1 refuses; 15.0's wording is used
     here. **[follows: PP, PP1]**
   - A claim after an each-tick port declaration is not licensed merely because it never reads that port. D-18's
     alternative boundary is not adopted; using it would widen R6.
   - "Reach fails closed on unknown statement kinds, including the version-1 tick-block case." "The tick block
     must have its own closure rule that follows its body." The existing version-0 default behavior is not enough to
     establish this.
   - "An independent structural oracle checks PREFIX licensing; the trace is a check, not the rule."
   - A licence is not a standing. A licensed claim still needs held, a ratified seal and a channel that can ground
     to read GROUNDED (2). **[v0, for what GROUNDED needs]**
   - Sound, not complete: a claim may be conservatively excluded even when a particular execution would never reach
     an input-dependent path.
   - R6's word exempt and the ruling's word licensed name one thing. 5c's adopted definition makes a claim exempt
     exactly when the static test holds, that test being R6's first licence bullet above plus the closure, and (a)
     restates that bullet. The identity holds while 15.1.3's places hold: ports before the tick block, and the tick
     block last. **[follows: PREFIX (5c); PP, PP1 and PP2]**
   - The licence presupposes that no input binds before the boundary's position. A read-once value binds where its
     declaration stands (15.7.1), which is never before the boundary, so the presupposition holds. **[follows: F6;
     15.0 Boundary]** R6's first input is then the first port value bound, or the first `'T'` in a law with no port;
     never the loading of the log (15.5). **[open: the theorem ledger's T9, its definition of the first input]**

   **The closure's rule table.** **[ruled: PREFIX, 2026-10-27; its Perform row, his answer of the same day]** The closure follows the source alone, with values
   ignored.

| statement kind | what the closure adds |
|---|---|
| a claim | the claim itself |
| If, Unless, Otherwise | every arm, the Otherwise included |
| For, While | the body |
| the tick block | its body |
| Perform, written `Perform <name>` or the name alone (SPEC §3) | the procedure's body, transitively |
| To, Define, Decimals | no further reachable body |
| Let, Set, Increase, Decrease, Say, Append, Remove, Must, a port declaration | no further reachable body |
| any other kind | no claim of the law is licensed |

   - "This does not exempt their surrounding clauses from the boundary or licensing test."
   - "An unperformed `To` adds no procedure body because the closure is source-structural—not because a particular
     execution skipped it."
   - The table establishes no individual claim's licence or standing. Each follows from applying the whole rule to
     a law's source, then the settlement rules, and the structural oracle tests it on its fixtures.
   - **The reach of version 1's kinds.** A port declaration contains no statement and adds nothing, never itself. The
     tick block contains its numbered body, which may hold If, For, While and Perform; reached as a later top-level
     sibling, it adds its body and everything that may execute from it, transitively, reached Performs included; its
     budget never restricts reach. Execution of the tick body never makes an earlier top-level prefix statement run
     again; a procedure defined in the prefix stays in the reach when the tick body reaches it by Perform. **[ruled:
     R2, R2.3 and its clarification]**
5. **A PREFIX claim that evaluated true** "remains historically held, regardless of whether the execution loop
   encounters a subsequent transactional refusal downstream." **[ruled: R6]** In a real court reading the claim is
   held only once court R1 is met, which before 1b it is not (15.13.11). In 1a its row runs in the reference with the
   agreed witness configured (15.13.11), once CUT-0's digest is pinned (15.13.4). **[ruled: F24, for the real reading
   and the 1a row; claims, the pin's order]**
6. **The rows and their controls.** "Every row testing an ungrounded port violation must run with the witness
   explicitly configured as agreed." "Each test row is structurally paired with an internal control variant. The
   control evaluates the exact same claim without an active log declaration, or wraps it securely within the `PREFIX`
   license parameters. The control must return a clean `GROUNDED` standing".
   - "The configured witness covers the PREFIX row and its controls, not only ungrounded rows; results say
     configured, not measured." **[ruled: F24]**
   - In 1a these rows and their controls run in the reference with the agreed witness configured, once CUT-0's
     digest is pinned (15.13.4). No such row is evidence that the reference's version-1 arithmetic is right
     (15.13.11). **[ruled: F24; claims, the pin's order]**
   - "keep the configured witness for the R6 row and its control; add the measured version-0 control as a separate
     row." The row and its paired control share the configured witness: "the only intended difference is R6." The
     separate version-0 control "may use the arbiter’s own measured witness, clearly labelled as a distinct
     measurement—not as the paired R6 control." **[ruled: F24, R6's control, 2026-10-27]**
   - A control "without an active log declaration" is a version-0 law, so removing the declaration also changes
     the law's header, the receipt's frame, the trace's domain string, the claim's clause id and the HELD rule
     (version 0's, not 15.13's). The row names these and compares only standings both rules define alike, a
     COMPLETED run's among them. **[open: 1a's specification]**

## 15.13 The court in a version-1 run: HELD

1. **HELD means E2:** every completed evaluation of the claim was true, no evaluation of that claim remains open at
   the cut, and the continuation at the cut could not evaluate that claim again. **[ruled: claims]** E2 defines the
   claim-specific continuation condition; it does not erase the court's backend-agreement requirement (15.13.11).
   **[ruled: F24]**
2. **Only continuation that could evaluate the particular claim again affects its standing.** Unrelated pending
   execution does not withhold it. **[ruled: claims]**
3. **"True in k of k evaluations" remains descriptive evidence,** not a substitute for settlement. **[ruled: claims]**
4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT-0 holds it.** The meet
   names the exact digest of the CUT-0 it uses. A digest identifies the rule; it does not prove it sound. CUT-0 alone
   remains the target for further development. **[ruled: claims]** "Court R1 remains a condition of HELD
   alongside E2" (15.13.11). **[ruled: F24]** The order of work, in his words: "resolve those inputs, complete the
   version-1 containment fixture test against the resulting candidate, pin that exact candidate’s digest, then run
   1a’s rows against the pinned rule." Every input the pinned rule reads, in every row of CUT-0, is fixed before
   the pin. The read-once stop's row reads, in his list, the amended set's "port place" (15.1.3) and "counting"
   (15.7.1), finding 8 (15.7.5), finding 20 and, if the cut is in `'R'`, its decoding (15.9); the other rows read
   the version-1 NOT-RUN and LOG-OPEN status encoding (15.7.5); and CUT-0's closure reads R2's statement-kind
   spellings and reach rules (15.1.1). Of these, all are now ruled but the cut's byte grammar, whose candidate,
   draft 2, the containment step tests (15.9). **[follows: the rulings since draft 10; his answer on S15.9-1]**
   "The claims ruling requires the meet to be pinned to the exact CUT-0 digest;
   labelling an unpinned proposal does not satisfy that condition. The check belongs on 1a’s build path". The
   version-1 reference runs the containment test before the pin; no court row runs against an unpinned CUT-0, and
   nothing of 1a is built or run against it. "If a later ruling changes an input or the rule, it requires a new
   candidate and digest, with the applicable checks repeated." The general format freeze (P6) keeps its own
   trigger. "This settles the ordering question, not the underlying open rows themselves. They still require their
   own rulings and evidence before the build gate opens." **[ruled: claims, the pin's order; his answers on
   V1CHECK-3, Q1, Q2 and the pin's inputs, and his clarification that the principle reaches every row]** The test's record names the digest of the candidate it ran
   on, and the pin pins that digest. **[follows: his answers on Q1, Q2 and the pin's inputs]** The record also
   enumerates the inputs the candidate actually reads, and that list is checked against the candidate, not drawn
   up by hand. **[ruled: claims, his clarification]** The list above is what is known now; the record checked
   against the candidate decides which inputs exist. What counts as a read (receipt fields, trace events, statement
   kinds) is decided by 1a's specification. **[follows: his clarification; open: 1a's specification]**
5. **The court's R8:** when the run refuses at a claim's own clause with any code but CLAIM-REFUTED, an evaluation of
   the claim began and did not finish, and the claim is not held. A claim inline in another statement shares its
   clause with a condition or another arm, so the refusal may come from there. It is not held either. **[pinned]**
6. **CUT-0** holds a claim when every completed evaluation is true, it is not open at the cut, and it is not in K̂.
   **[pinned]**
7. **The continuation** is everything the run could still have executed had the refusing operation returned. Every
   later refusal is read as passable, values are unknown, and only a For's normal exit is exact (reading S2). It is
   relative to the law, any further input included, not to the session, which ends at the refusal until SNAP-1.
   **[pinned]**
8. **The cut** is the stack of statements executing at the refusal, outermost first. An arm's inline statement is a
   frame of its own, directly above its If's frame, named by the If's clause and its arm. The two count as one
   position for the rest of the block. **A claim is open** at the cut when its statement is the top frame: its
   evaluation began and did not complete, including a claim refused at its own operation before its condition is
   evaluated. **K̂** is computed from the cut: **[pinned]**
   - **COMPLETED:** the cut is after the last statement, and K̂ is empty;
   - **the open claim:** in K̂, named by its id (T10.6);
   - **a refused If** (the If on top, a condition refused): the arms from the refused one onward, the Otherwise
     included (T10.2);
   - **a loop's own clause refused:** its body (T10.3, T10.4);
   - **a Perform refused at its own operation:** its body (T10.5);
   - **the rest of a block,** for each frame outward: the following siblings that are not absorbed Otherwise
     clauses, everything they may execute included, values ignored (T10.1);
   - **a For below the top:** its body again, exactly when its bit says passes remain (T10.3);
   - **a While below the top:** its body again, always (T10.4);
   - **a Perform below the top:** a return only to the frame below it, the actual caller (T10.5);
   - **the tick block below the top:** its body again, since another tick may run (T10.7);
   - **NOT-RUN t, or LOG-OPEN:** the cut is the tick block's head before tick t, and K̂ is the tick block and every
     procedure performed from it (T10.7). The court applies this row when the receipt's status is not in the
     read-once stop's distinguishing form (15.7.5): its second token a decimal t, or absent. That is so when the law
     declares no read-once port or its log holds the read-once record. **[ruled: F6; his answer on STOPROW-1; F8,
     8.6]**
   - **The read-once stop (15.7.1), NOT-RUN or LOG-OPEN in the stop's distinguishing form, the read-once record
     absent:** the cut is the first
     read-once declaration, a top-level frame not begun, with no `'R'` event; K̂ is the rest of the block from it,
     the tick block's body and every procedure performed included, transitively, values ignored (T10.8). A withholding
     names this row, "the read-once stop", never "the rest of a block". **[ruled: F6, RO′-6; his answer on F6-1;
     pinned]** The court chooses this row from the receipt's status (15.7.5), its second token `READ-ONCE`, never by
     inspecting the log or by inferring the record's absence from the trace. **[ruled: F6, his answer on STOPROW-1;
     F8, 8.1 and 8.6]**
     Its premises: binding has no effect beyond binding (it counts no operation, emits only `'N'`, and cannot
     refuse); read-once ports are declared at the top level, each evaluated once; values are unknown, as in reading
     S2. **[ruled: F6, condition 3, that they are stated; PP, PP1, the top-level place; counting, C1, that binding
     counts none]** On version-0 stand-ins (`packets/F-read-once-adversary.md` §4), CUT-0 as built, at
     a version-0 refusal, gave the K̂ RO′-6's formula states, and containment held: every claim the resumed run
     evaluated after the cut was in K̂. In version 1 RO′-6 defines K̂, so that equality holds by definition, and what
     version 1 owes is containment. **[follows: `packets/F-read-once-adversary.md` §4, as
     `twin-r7/REREAD-4-DISPOSITION.md` checked it; RO′-6]** The grades, in his words: "MEASURED on version-0 stand-ins; DECLARED for version
     1." A version-1 check is owed before CUT-0's digest is pinned: a deferral, not evidence. "It does not close the
     format-freeze question or authorize pinning before the check." **[ruled: F6, his answer on F6-14; the check
     named by his answer on V1CHECK-2]** The owed check is containment: every
     claim the same law evaluates after the stop, over any log that supplies the record, lies in K̂, and the check
     passes only if none falls outside. Precision is not part of it, since a structural closure that ignores values
     may hold claims a particular continuation cannot evaluate. It is an obligation, not a result the definition of
     K̂ establishes. **[ruled: F6, his answer on V1CHECK-2]** The check is a test on fixtures, run by the version-1
     reference before the pin: for each tested log that supplies the record, every claim the same law evaluates
     after the stop must lie in K̂, and any claim outside K̂ falsifies containment. No court row runs against an
     unpinned CUT-0. Its result is MEASURED on those fixtures only: it establishes neither containment over every
     log nor T10.8, and no test result or measurement alone closes T10 (15.13.10). **[ruled: F6, his answer on Q1]**
     The sentence before names the property, over every log that supplies the record; the test samples it, and its
     pass means on the tested logs only. **[follows: his answers on V1CHECK-2 and Q1]** The fixture set is fixed and
     recorded before the test runs, and the test runs against the candidate the pin's inputs give (15.13.4).
     **[ruled: claims, his answer on the pin's inputs, that the test runs against the resulting candidate; open: 1a's
     specification, the fixtures]** Its record names that candidate's digest **[follows: his answers on Q1, Q2 and
     the pin's inputs]** and enumerates the inputs the candidate actually reads, checked against the candidate.
     **[ruled: claims, his clarification]**

   What "may execute" reaches includes every procedure performed, transitively. It is CUT-0's own reachability,
   the one the pin is to name, with the version-1 rows above. The PREFIX licence's closure has its own ruled table
   (15.12.4), and the two are not said to be one. **[pinned]** Its rules for the version-1 kinds are R2.3's, fixed by
   R2's ruling before the pin and stated in the pinned rule: a later tick block adds its body, and below the top its
   body again; a port declaration adds nothing. The pin records them and does not decide them. **[ruled: R2, R2.3;
   follows: his clarification that the principle reaches every row]**
9. **Every withholding by CUT-0 names its row:** the open claim, the refused If's arms onward, the loop's own clause
   refused, a Perform refused, the rest of a block, a For's next pass, a While's next pass, the tick block's next
   tick, or the read-once stop. **[ruled: claims, that a row is named; pinned, the rows; F6, the read-once stop's
   name]**
10. **What stays open.** **[ruled: claims]**
    - No proof obligation is closed by this section. T10 stays open, split into T10.0 to T10.8 in `ROUNDS.md`, and
      no test result or measurement alone closes it. "The `While` next-pass row is the priority for precision
      investigation."
    - T11 stays open. The ruling "establishes neither compatibility preservation nor general soundness."
    - "Releasing claims whose truth cannot change would require a separate, stronger invariance rule; that is not
      part of this version 1 ruling."
11. **Until 1b, the court's reading of a version-1 run, read with the witness the arbiter makes, is REFERENCE-ONLY
    and holds no claim (court R1, unchanged).** **[ruled: F24]** This governs readings of runs, not the court's rows:
    R6's rows, the PREFIX row and each row's control run in 1a's reference with the witness configured as agreed, as
    R6's first rider requires, and each such row states that its agreement is configured, not measured. They run
    once CUT-0's digest is pinned (15.13.4). **[ruled: claims, the pin's order]**
    - "Court R1 remains a condition of HELD alongside E2." The claims ruling is not amended. E2 defines the
      claim-specific continuation condition; it does not erase the court's backend-agreement requirement.
    - "The configured witness covers the PREFIX row and its controls, not only ungrounded rows; results say
      configured, not measured."
    - The separate version-0 control of 15.12.6 is not one of these rows' controls: it may use the arbiter's
      measured witness, labelled as a distinct measurement.
    - A configured witness does not constitute independent backend agreement. No such row is evidence that the
      reference's version-1 arithmetic is right: "configured agreement is not measured agreement, and neither
      establishes the reference’s version-1 arithmetic independently."
    - The ruling's scope, in his words: it "does not close T10/T11, establish CUT-0’s soundness, or independently
      verify reference arithmetic."
    - In a real reading REFERENCE-ONLY is the integrity column, as the court as built prints it, and each claim's
      evaluation prints beside it: true in k of k or refuted for a completed evaluation, and in 12's order for a
      claim with none. **[v0]**
    - D10's two-commit split is not ruled here. **[open: D10, the split]**
12. **A claim with no completed evaluation** reads in the court's order as built: R8's refused evaluation first (an
    evaluation began at the refusing clause and did not finish), then UNREACHED (no evaluation began). **[v0]**

## 15.14 Reporting

**[open: amended set "reporting"]** Every authoritative report names its claim, the evidence it binds, the authority
that made it, its version, and the condition on which it passes or fails, and it attests nothing outside its
authority. "Grounded over claims" joins the court summary's forbidden interpretations. Also this row's: how a
result of a row run with the configured witness is labelled, so that it is never read as an agreement record
(15.4) or a receipt core (15.8). So is the label of the separate measured version-0 control (15.12.6), "clearly
labelled as a distinct measurement".

## 15.15 What is open, for the owner, before the twin reads this

| clause | decided by |
|---|---|
| 15.0: float ports | sheet R8 |
| 15.1.4: the law line's `<type>` spelling | the amended set's "identity and bytes" |
| 15.3: when the host runs the prefix of a law with no read-once port, and when a refusal there is known | the amended set's "A2" |
| 15.5: how a 1b runtime refuses a log, and its exit code | 1b's specification (RUNTIME-SPEC §1) |
| 15.1.5: the door and the forms | the amended set's "H2" (its own change, with E18's COMPAT-0 settlement) |
| 15.1.6: world properties | R1 |
| 15.2: whether the ASCII sieve governs text; the integer and decimal grammars; the raw prefix and sign; the two truth spellings; CP1252 text that is valid UTF-8; text's extra refusals; the order of the door's rules (findings 13, 14, 15) | R3's details for 1a; contract draft 0 |
| 15.3 and 15.4: the session, its record and the binding of the three records; precedence among refused moves; an arrival assigned to a tick that does not run; an arrival held across ticks (findings 12, 54, 55) | the amended set's "A2", "session record" and "binding" |
| 15.3: the events that fill and close the read-once record; whether tick 1 may close before it; a close with a slot empty | the amended set's "A2" |
| 15.5: a text value's door rules in the loader's checks (T3) | R3 |
| 15.6: the port signature's `<name>` and `<type>` spellings (finding 37) | the amended set's "identity and bytes" |
| 15.7.6: out_0's reading and domain string | the amended set's "identity and bytes" |
| 15.8: `tick-ops` when no tick began; the unread count's name; the line order (finding 31) | the amended set's "identity and bytes" |
| 15.9: the cut's byte grammar, draft 2 the candidate, MEASURED on version-0 stand-ins only; its test of S1 to S7 on the version-1 reference | the containment step, before the pin (his answer on S15.9-1) |
| 15.9: the general format freeze | P6, on its own trigger |
| 15.10: the digests' definitions; `input-chain`; per-tick or running `events` and `output-bytes`; the state digest's cost (finding 32) | 1a's specification; the speed verdict's proposals |
| 15.11 and 15.8: replay, and "never reported as validity", "no line states validity" | contract draft 0, until ruled |
| 15.13.4 and 15.13.8: the version-1 containment test's fixtures, fixed and recorded before the test runs, its result MEASURED on them alone; what counts as a read in the inputs record | 1a's specification |
| 15.13.7: the continuation at a stop where no operation refused (in re-read 4's words, V1CHECK-4: "had the missing input arrived, with any value"), which the containment test, T10.7 and T10.8 need; his answer on V1CHECK-2 states the check over what "the same law evaluates after the read-once stop, over any log that supplies the required record", which bears on it and does not word it | the pin's wording |
| 15.13.9: the row named when two rows withhold one claim (finding 45) | minor; the proposal is every row |
| 15.13.11: D10's two-commit split | D10 |
| 15.14: the authority rule; the labels of a configured result and of the measured control | the amended set's "reporting" |

Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.13.11, D10's court
clause (finding 24). Since draft 2 (2026-10-27): the labels' definitions, the closure's rule table (15.12.4) and R6's
control (15.12.6); since draft 3, the table's Perform row; since draft 4, finding 6, read-once ports (15.3, 15.5,
15.7.1, 15.7.5, 15.13.8); since draft 5, the read-once stop's row and its version-1 check (15.13.8, 15.13.9); since draft 6, its receipt
status, the owed check and the order of work (15.7.5, 15.13.4, 15.13.8); since draft 7, the check as a fixture
test, findings 8 and 20 before the pin, and RO′-5 confirmed (15.7.5, 15.9, 15.12.5, 15.12.6, 15.13.4, 15.13.8,
15.13.11); since draft 8, every input the pinned rule reads fixed before the pin (15.1.3, 15.7.1, 15.7.5, 15.9,
15.13.4, 15.13.8); since draft 9, that principle reaching every row of CUT-0 (15.1.1, 15.7.5, 15.9, 15.13.4,
15.13.8); since draft 10, finding 8, finding 20, R2, the port place, counting and the budget, N2, N3 and finding 10
(15.0, 15.1.1, 15.1.3, 15.3, 15.4, 15.5, 15.7, 15.8, 15.9, 15.10, 15.12.4, 15.13.4, 15.13.8); since draft 11, re-read
9's five answers and fixes (15.0, 15.1.4, 15.3, 15.5, 15.7.3, 15.9, 15.13.4).
`RULINGS.md` holds every one.
