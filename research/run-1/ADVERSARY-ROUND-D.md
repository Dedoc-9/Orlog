# Adversary round D against the RUN-1 contract draft 0 (2026-10-26)

**What was attacked:** `research/run-1/CONTRACT-DRAFT.md` (draft 0, untracked in the working tree at commit 95dac79),
read with `SPEC.md`, `RUNTIME-SPEC.md` and the code under `src/orlog/`. The draft's interpretations elsewhere
(`RULINGS.md`, `DESIGN-BRIEF.md`, `CONTRACT-DEBATE.md`, `ROUNDS.md`, `STATUS.md`, `research/speed/`,
`research/doppler/`) were not read. Neither were the untracked `research/run-1/completeness_probe.py` and
`evidence/run1-completeness.txt`, because they looked like the drafter's own probe of §8.4. The point was to test
whether the written rules decide every result on their own.

**How:** version 0 was run on the reference. Version 1 is not built, so every version-1 case below is worked by hand
and graded DECLARED. Some version-1 cases have a version-0 stand-in that can be run (one clause stands in for a port
declaration or an input). In those cases the stand-in is MEASURED and the version-1 reading is DECLARED. The scripts
are under `work/run-1-adversary/` (git ignores `work/`, so their output is quoted here):

- `make_fixtures.py` writes the fixtures `fixtures/d01…d12` in binary with LF endings.
- `measure.py` runs each fixture on the reference (`orlog.interp.Interp`) and prints its receipt lines, its trace and
  the court's evaluation and support columns. The court's witness says all executions agreed, because the court's
  rules are what is under test here, not the backends.
- `receipt_cores.py` compares receipt cores.
- `state_probe.py` lists which variables the front end marks as top-level.

Every command ran with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`. No backend was built.

A version-1 port declaration has no spelling in the draft. The sketches write it as a placeholder clause,
`<port NAME: TYPE, each tick>` or `<port NAME: TYPE, once>`.

## Findings

### Finding 1 (severity: decides a one-way format)
- **Rule attacked:** §2.1, §2.3, §2.4 (with §1.2 and RUNTIME-SPEC §5).
- **Smallest counterexample:** a law with one each-tick integer port, and one tick whose value is 10. §1.2 says the
  door returns "an accepted value encoding (RUNTIME-SPEC §5)", and §2.1 says each record holds "value encodings" in "a
  stream of LF-terminated ASCII lines". Int 10's value encoding is `49 00 00 00 00 00 00 00 0a`, so it carries an LF
  byte. A text's encoding carries a binary u32 length (a length of 10 is `…0a`), a Bool carries `00` or `01`, and any
  byte ≥ 0x80 is not ASCII. The record's own layout is also unstated:
  - the separator between ports;
  - whether a record carries its tick number (§2.2 refuses "a duplicated or missing tick number", but §2.1 puts no
    number in a record);
  - what the read-once record is when there are no read-once ports;
  - whether the header is one line or three, and the case of its hex;
  - what "with" means in in_0's "the header's bytes, with the read-once record";
  - whether a record's LF is part of "tick record t's bytes" in in_t.
- **What the draft requires, or the two readings:**
  - (a) Raw encodings: then 10 splits its record in two and §2.2 refuses the log, LOG-MALFORMED.
  - (b) A textual or hex spelling, chosen by each host.

  Two hosts that saw the same arrivals write different bytes, so they produce a different `input-log-sha256`, a
  different in_t and a different receipt core. §9.1 assumes that "the input log's bytes" are a well-defined object.
- **Required observable result:** one byte form per record. A value must never be able to end its line, and the bytes
  hashed by in_t must be exactly the bytes of one record.
- **Falsifying test:** row LOG-BYTES writes the log for an each-tick integer port carrying 10 and a text port carrying
  a 10-byte text. It requires that splitting the log at LF gives exactly the header, the read-once record, one tick
  record and the end record, and that reading the records back gives the values. *Plant:* write the raw RUNTIME-SPEC §5
  encodings. The record splits at both 0x0A bytes, and the row must fail.
- **Proposed repair:** "A record is one line: `tick <t>` (`once` for the read-once record, written even when empty),
  then, per port in declaration order, one space and its value encoding in lowercase hex. A record's hashed bytes
  include its LF. The header is three lines."
- **Change class:** one-way.
- **Grade:**
  - MEASURED: Int 10 encodes with a 0x0A byte (`fixtures/d12_int10.orl`, trace line `1 A 1 0000000049000000000000000a …`)
    and text "ab" as `54 00000002 6162` (trace line `2 A 2 0000000154000000026162 …`).
  - ESTABLISHED: the gaps in the draft's text.

### Finding 2 (severity: decides a one-way format): the headline
- **Rule attacked:** §1.1, §1.4 (A1 and A2), §2.5.
- **Smallest counterexample:** a law with one each-tick integer port `p`, whose tick block says `p`. The arrival log
  holds exactly one line, arrival 1: port `p`, source `alice`, bytes `3`.
  - **H1:** the host assigns arrival 1 to (1, p), closes tick 1 and ends the session. The input log is
    `tick 1 = 3; end 1 closed`. The outcome is COMPLETED, with output `3\n`.
  - **H2:** the host closes tick 1 before it assigns arrival 1 (the arrival came late, or the host failed to assign
    it), then ends the session. The input log is `end 0 not-run 1 INPUT-MISSING p`. The outcome is NOT-RUN 1
    INPUT-MISSING p, with no output.

  Both histories satisfy A2. Their arrival logs are byte-identical, because §1.1 records arrivals and nothing else: no
  assignment, no close and no drop. Under A1 the pair needs two arrivals (`3`, then `4`): the host may assign them in
  either order, giving outputs `3 4` or `4 3` from one arrival log. §2.5 calls the input log "a projection of the
  arrival log … with the host's closing of each tick", but the arrival log has no record of any closing.
- **What the draft requires, or the two readings:** the input log carries information found in no other record: the
  host's assignments, its closes and its choice among several accepted arrivals for one slot. So it is an authority,
  not a projection, and no checker can recompute it from the arrival log.
- **Required observable result:** two things.
  - Every arrival's disposition: refused (with its code), assigned (to which tick and port) or dropped (with its
    reason).
  - Every close, in one ordered sequence with the arrivals.

  With these, the input log is a pure function of the arrival log and can be checked byte for byte. H2 is then visible
  as "close 1" before "assign 1" (a late arrival), or as an accepted arrival with no assignment and no drop record (a
  host fault).
- **Falsifying test:** row PROJECTION recomputes the input log from an arrival log that holds assign, drop and close
  records, and requires byte equality. *Plant:* a host that leaves an accepted arrival unassigned and writes no drop
  record. The projection check must fail and name the arrival.
- **Proposed repair:** "The arrival log is one sequence of records: `arrival <seq> <port> <source> <hex bytes>
  <verdict>`, `assign <seq> <t>`, `drop <seq> <reason>`, `close <t>`, `end`. The input log is the projection of the
  assign, close and end records, and a log that differs from the projection is refused."
- **Change class:** one-way.
- **Grade:** DECLARED (worked by hand from §1.1, §1.4 and §2.5; ESTABLISHED that §1.1 lists no record kind other than
  an arrival).

### Finding 3 (severity: decides a one-way format)
- **Rule attacked:** §1.1, §1.2, §1.3.5.
- **Smallest counterexample:** a hostile client sends to an integer port the bytes `5`, LF, `7 p alice 9`. §1.1
  appends "the bytes as received" to a log whose format is not fixed. If the host writes them raw into a line-oriented
  log (as the input log's form invites), the arrival log now holds a forged arrival "7" from `alice` that never
  reached the door. Under A2 the door refuses the real arrival (INPUT-SYNTAX), and the forged line reads as an
  accepted one.

  The arrival log has other gaps too:
  - It has no chain, and nothing binds it to the input log or the receipt. An arrival log rewritten after the session
    cannot be told from the true one.
  - It has no bound on an arrival's size: a 2 GB arrival must be kept whole.
  - It has no field for the door's verdict or note. §1.3.5's NFC note has nowhere to go, and A2's "recorded with its
    refusal" has no field.
- **What the draft requires, or the two readings:** the format is left to the host, so a forged line and a true line
  have the same bytes.
- **Required observable result:**
  - Each arrival is exactly one record, whatever its bytes.
  - The log is tamper-evident: its head at each close is recorded in the log itself.
  - Each arrival carries the door's verdict, including its notes.
- **Falsifying test:** row ARRIVAL-FRAME sends the bytes above and requires exactly one arrival record, with its
  refusal. *Plant:* a raw writer. The row must see two arrivals.
- **Proposed repair:** "An arrival's bytes are written in lowercase hex, at most 2^24 of them (more is refused
  INPUT-RANGE and kept as its length and sha256). Each record extends a chain like §2.3's, and each close record
  carries the chain's head."
- **Change class:** one-way.
- **Grade:** DECLARED.

### Finding 4 (severity: decides a one-way format)
- **Rule attacked:** §1.4, §2.1, §4.5.
- **Smallest counterexample:** `<port seed: an integer, once>` receives `x`.
  - Under A1, "assigns each arrival to a (tick, port)" has no tick to assign a read-once arrival to.
  - Under A2, only "If the host closes tick t without a value for some each-tick port" is defined. A read-once port
    with no value has no rule.
  - The end record `not-run <t> …` needs a tick number, and none exists for the read-once record.

  An open log that has a header but no read-once record yet (a live session waiting for its seed) has no status
  either. Is the log malformed, or does the run stop at the declaration? §4.5's LOG-OPEN says "every record … was
  run", which does not cover a run stopped part-way through its prefix.
- **What the draft requires, or the two readings:** nothing. An implementer writes `not-run 0`, `not-run 1` or
  LOG-MALFORMED.
- **Required observable result:** a refused or missing read-once value has its own end cause, and its status is
  distinct from a tick's.
- **Falsifying test:** row ONCE-REFUSED: a read-once arrival `x` gives `end 0 not-run 0 INPUT-REFUSED seed` and
  status `NOT-RUN 0 INPUT-REFUSED seed`. *Plant:* a writer that names tick 1.
- **Proposed repair:** "Tick 0 is the read-once record. A read-once value that is refused (A1) or missing at the
  first close (A2) ends the session with `not-run 0`."
- **Change class:** one-way.
- **Grade:** DECLARED.

### Finding 5 (severity: decides a one-way format)
- **Rule attacked:** §2.1, §2.2, §4.5.
- **Smallest counterexample:** each of these logs passes §2.2 as written:
  - `end 3 not-run 7 INPUT-MISSING p` after three tick records;
  - `end 3 not-run 4 INPUT-MISSING q`, where `q` is no port of the signature, or is a read-once port;
  - a tick in which two ports both lack values, which can name either of them.

  §4.5 then reads `NOT-RUN 7 …` with "every record before t was run", although ticks 4 to 6 never existed. Under A1,
  a refused arrival for a future tick t+5, while ticks t to t+4 are still open, gives exactly such a log, because A1
  does not say when "the session ends".
- **What the draft requires, or the two readings:** the named tick and port are the host's choice. Two hosts write
  different end records, different `input-log-sha256` values and different status lines for one history.
- **Required observable result:** the end record is a function of the arrival log and the rule.
- **Falsifying test:** row END-RECORD requires each of the three logs to be refused LOG-MALFORMED or named
  canonically. *Plant:* §2.2's checks as written. All three are accepted.
- **Proposed repair:** "In an end record, t is n+1. The port is the first port in declaration order whose value was
  refused (A1) or is missing (A2), and it is a port of t's kind. Anything else is LOG-MALFORMED."
- **Change class:** one-way.
- **Grade:** ESTABLISHED (by reading §2.2's list of malformations).

### Finding 6 (severity: decides a one-way format)
- **Rule attacked:** §4.1, §4.2, §6.1.
- **Smallest counterexample:** one tick of one each-tick port. Every event's head covers its kind, its clause (u32),
  its length and its payload (RUNTIME-SPEC §5). For `'T'`, §4.2 gives the payload as "(t, c), both u64", but no byte
  order and no clause. For `'N'`, neither its clause (the port's declaration? the tick block? 0?) nor its payload
  (u32 var and value, like `'A'`? the port's index?) is given.
- **What the draft requires, or the two readings:** any choice satisfies §4. Each choice gives another trace head, and
  so another receipt core.
- **Required observable result:** the bytes of both events.
- **Falsifying test:** row T-N-BYTES compares a one-tick trace with hand-written hex. *Plant:* a little-endian `c`.
- **Proposed repair:** "`'T'`: clause = the tick block's clause id; payload u64 t then u64 c, big-endian. `'N'`:
  clause = the port's declaration clause; payload u32 variable id then the value encoding, as `'A'`."
- **Change class:** one-way.
- **Grade:** ESTABLISHED.

### Finding 7 (severity: decides a one-way format)
- **Rule attacked:** §0, §3.2, §4.3, §9.1.
- **Smallest counterexample:** two laws that differ only in `at most 2 operations` versus `at most 3 operations`.
  §3.2 gives the law's line for a port, but nothing gives the tick block's line in the law's bytes, or whether N is in
  it. If N is not in the law, the two laws share a law-seal, yet one input log makes one of them REFUSED TICK-BUDGET
  and the other COMPLETED. That contradicts §9.1, which says the law's bytes and the log's bytes decide the core.
  Neither N's range nor its literal form is stated (version 0's While bound is 1…2^62, FUEL). Is `at most 0
  operations` accepted?
- **What the draft requires, or the two readings:** nothing.
- **Required observable result:** the tick block, its kind (with or without a budget) and N are in the law's bytes.
- **Falsifying test:** row TICK-LAW requires the two laws' seals to differ. *Plant:* a tick line without N.
- **Proposed repair:** "The tick block is the clause `(tick N)`, with N = 0 for no budget, N an integer literal in
  1…2^62, else FUEL."
- **Change class:** one-way.
- **Grade:** ESTABLISHED (`law_bytes` writes every clause's statement and the While's fuel: `src/orlog/sema.py`
  600–608, 566–567; the draft gives no tick line).

### Finding 8 (severity: decides a one-way format)
- **Rule attacked:** §3.1, §3.2.
- **Smallest counterexample:** §3.1 writes `(port "<name>" <type> each-tick|once)\n` with the name between quotes, but
  it never says what a name may be or how a `"` inside one is written. If names may hold `"` and LF, two different
  port lists give identical signature bytes:
  - one port named `a" an integer each-tick)` LF `(port "b`, of type `a truth value`, read once;
  - two ports, `a` (an integer, each tick) and `b` (a truth value, once).

  Both write `(port "a" an integer each-tick)\n(port "b" a truth value once)\n`. The type's spelling is not fixed
  either: keywords are case-insensitive (SPEC §2), so `An Integer` and `an integer` may be written differently.

  The properties the brief asked for hold by §3.1's text:
  - An unrelated Let does not change the signature.
  - Renaming, retyping, reordering or changing a port's kind changes it.
  - Moving a read-once port's declaration changes only the law-seal, which is right.
  - Reordering a read-once port against an each-tick port changes the signature without changing any record's layout.
    That is over-sensitive but harmless.
- **What the draft requires, or the two readings:** the name's grammar and the type's spelling are open.
- **Required observable result:** distinct port lists have distinct signature bytes.
- **Falsifying test:** row PORT-SIG checks the bytes of hand-written signatures, and requires that a name holding `"`
  be refused or escaped. *Plant:* unescaped names. The pair above collides.
- **Proposed repair:** "A port's name is an identifier, `[A-Za-z][A-Za-z0-9_]*`, and its type is written `int`,
  `fix`, `bool` or `text`."
- **Change class:** one-way.
- **Grade:** ESTABLISHED, for the gaps and the listed properties. DECLARED, for the collision, which assumes free-form
  names.

### Finding 9 (severity: decides a one-way format)
- **Rule attacked:** §7.1.
- **Smallest counterexample:** the tick line's fields are under-fixed.
  - `events <n>` and `output-bytes <n>`: running totals or the tick's own? Only `ops` is said to be "the tick's own".
  - `claims <hex>`: the claim lines joined how? With the `claims n` line or without it, and with LF or without?
  - `state per-tick <hex>`: is `per-tick` a literal token?
  - "Every top-level variable": the front end's flag (`VarInfo.top`) excludes a top-level For's counter (MEASURED
    below). Are ports top-level variables?
  - Is `orlog-ticks 0` a header line?
  - Equal tick lines do not mean equal continuations. A certificate's cost counter (SPEC §7, "one cost counter per
    clause named by a certificate") persists across ticks, appears in no field, and changes later claim lines'
    `ref-cost`. A backend that miscounts it agrees on every tick line until the claim is next evaluated, so the lines
    cannot place the divergence.
- **What the draft requires, or the two readings:** each field has at least two byte forms.
- **Required observable result:** every field's bytes, and a state hash that covers everything a later tick can read.
- **Falsifying test:** row TICK-LINE compares a two-tick run with a hand-written line. *Plant:* per-tick `events`.
  Second plant: a cost counter perturbed between evaluations. The tick lines must differ at the tick of the
  perturbation.
- **Proposed repair:**
  - `events` and `output-bytes` are running totals.
  - `claims` is the SHA-256 of the receipt's `claim` lines, each with its LF.
  - `state` is the SHA-256 of u32 id ‖ value encoding for every variable whose front-end flag is top-level (ports
    included), then u32 clause ‖ u64 counter for each certificate counter, in id order.
  - The literal `per-tick` is dropped.
- **Change class:** one-way.
- **Grade:**
  - ESTABLISHED: the gaps.
  - MEASURED: the flag. `state_probe.py` prints `var 0 total top=True`, `var 1 i top=False loop=True … NO`,
    `var 2 j top=False loop=True … yes, 2`. A top-level For's counter is not top-level, and it holds a value after its
    loop only if the loop ran.

### Finding 10 (severity: changes a verdict)
- **Rule attacked:** §2.2, §2.4, §3.3, §4.4, §4.5, §8.2.
- **Smallest counterexample:** the law below refuses before its first input. Its log's third tick record has the
  wrong port count.

  ```
  §1 We claim that 2 equals 2.
  §2 Let z be 1 divided by 0.
  §3 <port seed: an integer, once>
  §4 Each tick, do the following.
  §4.1 We claim that seed is positive.
  ```

  The draft's rules on reading the log conflict:
  - §2.2 says a malformed log is "refused at load, LOG-MALFORMED, before any execution starts".
  - §4.4 says "Later records are not read."
  - §2.4 says the receipt's `input-log-sha256` is of "the log's bytes as read".
- **What the draft requires, or the two readings:**
  - (a) Check the whole log first: LOG-MALFORMED, with no receipt and no court reading. The PREFIX claim §1, which
    needs no input, gets no standing, because of a record the run would never reach.
  - (b) Stream: `REFUSED DIVISION-BY-ZERO` at §2, with a receipt. Its `input-log-sha256` is either of all the bytes or
    of none of them, since nothing was read.

  §8.2 then prints "rests on input log <sha>" for a run that read no input: a false statement of dependence.

  Neither §2.2 nor §3.3 says which code wins when a log has both a wrong `ports` line and a malformed record, or
  whether either refusal writes a receipt (§4.5 lists neither). A live session cannot be "refused at load before any
  execution starts" at all: by the time a bad record arrives at tick 50, ticks 1 to 49 have run and said their output.
- **Required observable result:** one reading of the log for every execution, one byte range for `input-log-sha256`,
  and a court line that states dependence only when an input was read.
- **Falsifying test:** row LOAD-ORDER runs the law above on the log above and requires the chosen outcome, with
  `input-log-sha256` over the chosen bytes. *Plant:* a streaming reader (if (a) is chosen) or a loading reader (if
  (b) is). Second row: a log with both faults reports the one code the repair names.
- **Proposed repair:** "An execution checks the whole log, its ports line first, before its first statement.
  `input-log-sha256` is of every byte. A live host appends only records it has checked. The court says 'rests on input
  log' only if an `'N'` event was emitted."
- **Change class:** one-way.
- **Grade:** ESTABLISHED (the three rules conflict as written). DECLARED (the outcomes).

### Finding 11 (severity: changes a verdict)
- **Rule attacked:** §4.3, with SPEC §7 ("A concatenation of k parts adds k−1 after all its parts are evaluated").
- **Smallest counterexample:**

  ```
  §1 Each tick, at most 2 operations, do the following.
  §1.1 Say "a" followed by "b" followed by "c" followed by "d".
  ```

  One empty tick record, then `end 1 closed`. The Say counts 1, and the concatenation adds 3. §4.3 refuses "when the
  addition makes the tick's count N+1".
  - **Reading A:** one addition of 3 takes the count from 1 to 4. It never equals 3, so there is no refusal: the run
    is COMPLETED, with output `abcd\n`, a tick count of 4 and the budget exceeded silently.
  - **Reading B:** the same addition, refused because it reaches or passes N+1: REFUSED TICK-BUDGET, with 4 counted
    in the tick.
  - **Reading C:** three additions of 1, refused at the second: REFUSED TICK-BUDGET, with 3 counted in the tick.
- **What the draft requires, or the two readings:** three receipts (status, `ops`, output), all consistent with §4.3
  and SPEC §7. In version 0 the difference cannot be seen: the reference and all three backends add k−1 in one step.
- **Required observable result:** the budget refuses at a single, defined unit, and the receipt's `ops` says how many
  were counted.
- **Falsifying test:** row BUDGET-UNITS runs the law above and requires reading C (REFUSED, tick count 3).
  *Plants:* the version-0 lump with an equality test (it comes back COMPLETED), and the lump with a ≥ test (tick
  count 4).
- **Proposed repair:** "A concatenation of k parts is k−1 operations counted one at a time. The budget refuses at the
  operation that makes the tick's count N+1."
- **Change class:** one-way.
- **Grade:**
  - MEASURED: version 0 lumps the count. `d07_concat.orl` gives `ops 4` and `d07b_say_only.orl` gives `ops 1`.
  - ESTABLISHED: the lump in the code (`src/orlog/interp.py` 367 `self.ops += len(e.parts) - 1`; `src/orlog/lower.py`
    390 `self.emit("ops", len(parts) - 1)`).
  - DECLARED: the three version-1 readings.

### Finding 12 (severity: changes a verdict)
- **Rule attacked:** §4.1, §4.2, §4.3, §7.2.
- **Smallest counterexample:**

  ```
  §1 Let n be 0.
  §2 Each tick, at most 2 operations, do the following.
  §2.1 Increase n by 1.
  ```

  Two ticks. SPEC §7 gives every executable statement its own count, every loop iteration included (While's "+1;
  evaluate C", For's per-iteration "+1"), and lists only "Define, To, Decimals" as counting nothing. The tick block is
  a new statement with no row. §4.1 says only that "Binding a port counts 0 operations".
  - **Reading R0:** the tick block counts nothing. Each tick counts 2, the run is COMPLETED, and T(2).c = 3.
  - **Reading R1:** the tick block counts 1 per tick after its `'T'`, as For does. The tick's count reaches 3 = N+1 at
    the Increase's second unit, so the run is REFUSED TICK-BUDGET at §2.1, with T(2).c never emitted.
  - **Reading R2:** the tick block counts its 1 before `'T'`. §7.2 rules this out (T(1).c would not be the prefix's
    count), but §7.2 decides nothing between R0 and R1.
- **What the draft requires, or the two readings:** R0 and R1 give different statuses, `'T'` payloads, trace heads and
  tick lines.
- **Required observable result:** the tick block's own count is stated.
- **Falsifying test:** row TICK-HEAD-COUNT runs the law above and requires COMPLETED with T(2).c − T(1).c = 2.
  *Plant:* +1 at each tick's head. The row must see REFUSED.
- **Proposed repair:** "The tick block counts no operation of its own, so a tick's count is its body's."
- **Change class:** one-way.
- **Grade:** ESTABLISHED (SPEC §7's table, lines 237–252, has no row for it). DECLARED (the outcomes).

### Finding 13 (severity: changes a verdict)
- **Rule attacked:** §4.3 ("TICK-BUDGET, at the clause whose statement is executing"), with SPEC §3 ("Otherwise
  clauses that are absorbed into an If chain are not separate statements") and §11 item 18.
- **Smallest counterexample:**

  ```
  §1 <port x: an integer, each tick>
  §2 Each tick, at most 2 operations, do the following.
  §2.1 If x equals 1, say 1.
  §2.2 Otherwise, if x equals 2, say 2.
  ```

  One tick with x = 0. Arm 1 counts 1, its comparison 1, and it is false. Arm 2's count makes 3 = N+1. In version 0 no
  refusal can ever fall on a bare count, so the clause a count belongs to has never been fixed. The lowering emits the
  arm's `tick` with no clause, before it lowers the condition under `ac.id`. With TICK-BUDGET it has to be fixed:
  - §2.1, because the chain is one statement (SPEC §3);
  - §2.2, because the arm's condition carries its own clause (item 18).
- **What the draft requires, or the two readings:** the status reads `REFUSED TICK-BUDGET <id of §2.1>` or
  `<id of §2.2>`, and the `'R'` event's clause and the trace head differ with it.
- **Required observable result:** each counted unit's clause.
- **Falsifying test:** row ARM-UNIT-CLAUSE requires the arm's clause. *Plant:* attribute the count to the chain's
  first clause.
- **Proposed repair:** "A counted unit belongs to the clause whose condition or statement it serves. An arm's count
  belongs to the arm's clause."
- **Change class:** one-way.
- **Grade:**
  - MEASURED: version 0 gives an arm's condition the arm's clause. `d05_elseif_clause.orl` gives
    `status REFUSED DIVISION-BY-ZERO 3`, and clause 3 is the `Otherwise, if` arm.
  - ESTABLISHED: the count carries no clause (`src/orlog/lower.py` 229–230; `src/orlog/interp.py` 212–214).

### Finding 14 (severity: changes a verdict)
- **Rule attacked:** §0, §4.1, §8.3 (the place of a port declaration).
- **Smallest counterexample:**

  ```
  §1 <port speed: an integer, each tick>
  §2 Say speed.
  §3 Each tick, do the following.
  §3.1 Say speed.
  ```

  §2 reads an each-tick port before tick 1 binds it. §1.5 forbids an invented or defaulted value, and no compile code
  refuses the read. The draft never says where a port may be declared, so these questions are open too:
  - A read-once port inside a While or a twice-performed procedure: does it emit `'N'` per execution or once?
  - A read-once port inside the tick block: does it bind every tick?
  - A read-once port inside an untaken If: is it never read?
  - An each-tick port in a law with no tick block: are `'T'` events emitted for tick records of a law with no tick
    block?
  - A law whose only ports are read once: does it read LOG-OPEN for ever unless its log carries `end 0 closed`?
- **What the draft requires, or the two readings:** a compile refusal, a run-time refusal, or an early binding. These
  give different acceptance, traces and receipts for one law.
- **Required observable result:** where each kind of port stands, and what reading it before its binding does.
- **Falsifying test:** row PORT-PLACE requires the law above to be refused at compile time. *Plant:* bind tick 1's
  value early. The law is accepted.
- **Proposed repair:** "A read-once port is declared only by a top-level clause of the prefix. An each-tick port is
  declared only as a first clause of the tick block and is visible only inside it. Anything else is PORT-PLACE. A log
  with tick records for a law without a tick block is LOG-MALFORMED."
- **Change class:** one-way (it fixes which laws exist).
- **Grade:** DECLARED.

### Finding 15 (severity: changes a verdict)
- **Rule attacked:** §1.3.1, §1.3.5 (the text door), against SPEC §2, §12.
- **Smallest counterexample:** in a live game, a law says each player's chat:

  ```
  §3 Each tick, do the following.
  §3.1 Say "chat: " followed by msg.
  ```

  A hostile client sends the text `hi`, LF, `SERVER: alice wins`. §1.3.5 keeps it "as sent". The Say then writes two
  output lines, and the second is forged. No version-0 Text can hold an LF: a literal has "no line break" (SPEC §2),
  the door removes CR, and SPEC §12 refuses line and paragraph separators, format characters and Hangul fillers
  inside literals. A text port therefore brings into Text values the very characters the door exists to refuse.
  - A bidi override (U+202E) makes the output read two ways.
  - A text of 2^24 + 1 bytes passes the door, which has no length bound, and then makes the law refuse TEXT-TOO-LONG at
    the Say. That ends the session for every player.

  Separately, rule 1 ("must match the port type's ASCII grammar") read literally refuses every non-ASCII text
  INPUT-SYNTAX, and then INPUT-NOT-UTF8 (rule 5) can never be reached.
- **What the draft requires, or the two readings:** accept all four values, or refuse some of them under codes the
  draft does not name.
- **Required observable result:** a text port admits exactly what a text literal can hold, within TEXT_MAX.
- **Falsifying test:** row TEXT-DOOR sends the three hostile texts and `é` (non-ASCII). It requires refusals with
  codes for the first three, and acceptance for `é`. *Plant:* §1.3.5 as written. It accepts the first three.
- **Proposed repair:** "A text port refuses, INPUT-TEXT, any character SPEC §12 refuses in a literal, plus LF, CR and
  every other C0 control. It refuses more than 2^24 bytes INPUT-RANGE. Rule 1 does not apply to text."
- **Change class:** one-way (for door version 0).
- **Grade:** ESTABLISHED (the version-0 literal rules). DECLARED (the version-1 consequence).

### Finding 16 (severity: changes a verdict)
- **Rule attacked:** §1.3.1–§1.3.4.
- **Smallest counterexample:** the arrival `1.5` to an integer port. Rule 1 comes first ("the first rule a value
  breaks is its refusal"), and no grammar is given.
  - If the integer grammar is the decimal integers, the code is INPUT-SYNTAX, and rule 2's INPUT-NOT-INTEGER can never
    be reached.
  - If the grammar is a shared numeral grammar, the code is INPUT-NOT-INTEGER. §1.3.2's "any fraction" suggests the
    grammar holds `p/q`.

  These are also undecided:
  - `+5`, `05`, `-0`, `1e3`, a leading space, a trailing LF;
  - the truth value's two spellings;
  - §1.3.3's raw prefix, which the draft itself leaves open;
  - the spelling of the bound and of the "two nearest grid values" that INPUT-RANGE and INPUT-GRID name.
- **What the draft requires, or the two readings:** two door codes, and so two arrival-log verdicts (A2) or two
  door reports (A1), for one input.
- **Required observable result:** each type's grammar, written out.
- **Falsifying test:** row DOOR-GRAMMAR gives a table of arrivals, each with its one code. *Plant:* swap rules 1 and
  2.
- **Proposed repair:** "Integer: `-?(0|[1-9][0-9]*)`. Fixed and integer ports share the numeral
  `-?[0-9]+(\.[0-9]+)?(/[0-9]+)?`, checked before rule 2. Truth: `true` and `false`." (The raw prefix still needs its
  own ruling.)
- **Change class:** one-way (door 0).
- **Grade:** ESTABLISHED.

### Finding 17 (severity: changes a verdict)
- **Rule attacked:** §1.4 (A1 and A2), §1.5.
- **Smallest counterexample:** see the section on A1 and A2 below. In short:
  - Under A1, one garbage arrival ends a multiplayer session for everyone. A1 has no rule for a missing value, for two
    arrivals assigned to one (tick, port), or for an arrival to an undeclared port.
  - Under A2, a silent client (a disconnect) ends the session at the close. An accepted arrival left unassigned has no
    disposition and no answer. A refusal can never be tied to a tick.
- **What the draft requires, or the two readings:** A1 and A2 each leave cases with no outcome. Where both define an
  outcome, it often ends the session.
- **Required observable result:** for each arrival, one disposition that its source is told. For each tick, a close
  that is recorded.
- **Falsifying test:** the rows of the A1/A2 section: L1–L5, H1–H3, E1–E3.
- **Proposed repair:** take A2, add Finding 2's records, and answer every disposition, a drop included, to its
  source.
- **Change class:** one-way.
- **Grade:** DECLARED.

### Finding 18 (severity: changes a verdict): a false GROUNDED
- **Rule attacked:** §8.3 (PREFIX), with §8.2.
- **Smallest counterexample:**

  ```
  §1 Let x be 1.
  §2 To inner, do the following.
  §2.1 We claim that x equals 1.
  §3 To outer, do the following.
  §3.1 Perform inner.
  §4 <port n: an integer, once>
  §5 Set x to n.
  §6 Perform outer.
  ```

  The claim §2.1 meets every condition in §8.3's second sentence:
  - it stands in the prefix;
  - it stands before the first port declaration (§4);
  - it stands outside the tick block;
  - its procedure `inner` is performed only at §3.1, which is before §4.

  But its only evaluation comes at §6, after the input, and it reads x = n. With a ratification of its claim seal it
  would be GROUNDED, although its truth depends on the input log, which §8.2 forbids.

  §8.3's two sentences are both *necessary* conditions ("only if", "must"), and neither states a *sufficient* one. A
  court that takes the decidable second sentence as the test grants this grounding.

  The test fails the other way too. If each-tick ports are declared at the top of the prefix, no prefix claim
  qualifies, although every prefix evaluation precedes the first `'N'`. A port declared inside a prefix While would
  let a claim before it in the same body pass the textual test while its second evaluation follows the input.
- **What the draft requires, or the two readings:**
  - (a) Textual test: exempt, so the claim can be GROUNDED.
  - (b) Evaluation test: not exempt.
- **Required observable result:** a claim is exempt exactly when no evaluation of it followed an input.
- **Falsifying test:** row PREFIX-TRANSITIVE runs the law above with a ledger ratifying §2.1, and requires
  UNGROUNDED. *Plant:* the textual test.
- **Proposed repair:** "A claim is exempt if and only if every `'C'` event of its id in the trace precedes the run's
  first `'N'` event, and the run emitted at least one `'N'`."
- **Change class:** two-way (a court reading).
- **Grade:**
  - MEASURED: the version-0 stand-in, `d04_transitive_perform.orl`, with §4 `Set x to 2` standing in for the port and
    the Set. Output: `trace 2 A 6 …0002` (the Set, clause 6), then `trace 3 C 3 0000000000` (the claim, clause 3),
    `status REFUSED CLAIM-REFUTED 3`. The claim's only evaluation follows a clause that stands after both the claim
    and its only Perform.
  - DECLARED: the version-1 reading.

### Finding 19 (severity: changes a verdict): interrupted claims held
- **Rule attacked:** §8.4 (it applies only "in a run that ends REFUSED"), §4.5.
- **Smallest counterexample:**

  ```
  §1 <port cmd: an integer, each tick>
  §2 Let score be 0.
  §3 Each tick, do the following.
  §3.1 We claim that score is at least 0.
  §3.2 It must hold that cmd is at least 0.
  §3.3 Increase score by cmd.
  ```

  - **Log A:** ticks `1`, `2`, `-5`, then `end 3 closed`. Tick 3 evaluates the claim (true), then the must fails, so
    the run is REFUSED MUST-FAILED at §3.2. §8.4 applies: §3.1 is reachable through the tick loop, so the claim is
    **not held**, although it was true in 3 of 3 evaluations.
  - **Log B:** the same client sends `-5.0` at tick 3, which A1 refuses (INPUT-NOT-INTEGER) and which ends the session
    as `end 2 not-run 3 INPUT-REFUSED cmd`. The run is NOT-RUN. §8.4 does not apply, so the claim is **held** (2 of 2
    true).
  - **Log C:** the session is still live, with ticks `1` and `2` and no end record. The run is LOG-OPEN, and the claim
    is held.

  In all three runs the claim would be evaluated again had the session continued. The run with the most evidence is
  the only one withheld. A door refusal and a law refusal of the same bad input therefore flip the standing of an
  unrelated claim.
- **What the draft requires, or the two readings:** as above. If "completeness of a claim's evaluations" is the
  standard, NOT-RUN and LOG-OPEN hold incomplete claims.
- **Required observable result:** one completeness reading for every way a run can stop short.
- **Falsifying test:** row STOP-ALIKE runs logs A and B and requires the same reading of §3.1. *Plant:* §8.4 as
  written. The two readings differ.
- **Proposed repair:** "For §8.4, a NOT-RUN at t, and a LOG-OPEN run, stop at the head of the tick block. Every
  tick-block claim is then reachable, and none is held."
- **Change class:** two-way.
- **Grade:** DECLARED.

### Finding 20 (severity: changes a verdict)
- **Rule attacked:** §8.4 ("the tick block is a loop").
- **Smallest counterexample:**

  ```
  §1 <port d: an integer, each tick>
  §2 Let total be 0.
  §3 Each tick, do the following.
  §3.1 We claim that d is at least 0.
  §3.2 Increase total by 10 divided by d.
  ```

  The log is `5`, `2`, `0`, then `end 3 closed`. Tick 3 evaluates the claim (true), then refuses DIVISION-BY-ZERO at
  §3.2. The tick loop's back edge makes §3.1 reachable, so the claim is withheld. But this closed log holds no tick 4,
  and §3.1 does not follow §3.2 within a tick. The claim's three evaluations are every evaluation this log can cause.
  A deterministic harness that runs a fixed script whose last tick refuses can never hold a tick-block claim. Under
  §4.4 ("later records are not read") the court cannot even know whether tick 4 exists. That is Finding 10 again.
- **What the draft requires, or the two readings:** withheld, by an edge that has no target.
- **Required observable result:** the back edge exists only when there is a later tick.
- **Falsifying test:** row LAST-TICK requires the claim to be held on log `5,2,0,end 3 closed`, and withheld on
  `5,2,0,7,end 4 closed`. *Plant:* an unconditional back edge.
- **Proposed repair:** "The tick block's back edge from tick t exists only if the log holds a tick record after t, or
  ends open, or ends not-run." (This needs Finding 10's whole-log reading.)
- **Change class:** two-way.
- **Grade:** DECLARED.

### Finding 21 (severity: changes a verdict): completed claims withheld, PREFIX claims included
- **Rule attacked:** §8.4 ("the end of a body returns after every `Perform` of that procedure").
- **Smallest counterexample:** a version-0 stand-in, `d03_two_performs.orl`:

  ```
  §1 Let x be 2.
  §2 To step, do the following.
  §2.1 Say 10 divided by (x minus 1).
  §3 Perform step.
  §4 We claim that x equals 2.
  §5 Set x to 1.
  §6 Perform step.
  ```

  The run refuses at §2.1 on the second Perform. By §8.4: from §2.1, the end of `step`'s body returns after every
  Perform, so after §3 as well, then to §4, which is the claim. The claim is reachable and withheld. The actual
  continuation is the return after §6 and then the end, so §4 can never be evaluated again.

  In version 1, put a port declaration and a tick block after §4, and `Set x to d. Perform step.` in the tick block.
  Claim §4 is then PREFIX-exempt and ratifiable, yet an input value (d = 1) withdraws its standing. That is the input
  dependence PREFIX exists to exclude. `d11_otherwise_twice.orl` does the same through an Otherwise arm: its claim
  §2.2.1 ran on the first Perform, the second Perform refuses in the then arm, and the return edge reaches the claim.
- **What the draft requires, or the two readings:** withheld, by a context-insensitive return.
- **Required observable result:** a claim is withheld only if the run's own continuation from s can reach it.
- **Falsifying test:** row RETURN-STACK runs the version-1 form of d03 and requires claim §4 held. *Plant:* the
  context-insensitive return.
- **Proposed repair:** "The end of a procedure's body returns only to after the Perform that entered it. For the body
  s stands in, that is the Performs on the run's stack at s, innermost first. For a body entered along the path, it is
  the Perform that entered it."
- **Change class:** two-way.
- **Grade:**
  - MEASURED (version 0 holds both claims):
    - `d03`: `status REFUSED DIVISION-BY-ZERO 3`, `claim 0 5 1 1 1 0 0`, court `§4 … support=WELL-FOUNDED`;
    - `d11`: `status REFUSED DIVISION-BY-ZERO 4`, court `§2.2.1 … support=WELL-FOUNDED`.
  - DECLARED: the §8.4 reading.

### Finding 22 (severity: changes a verdict)
- **Rule attacked:** §8 heading ("The court, in a run with an input log") against §8.4, which states no scope.
- **Smallest counterexample:** `d02_loop_unrelated.orl`:

  ```
  §1 Let i be 0.
  §2 While i is less than 5, at most 10 times, do the following.
  §2.1 Increase i by 1.
  §2.2 We claim that i is positive.
  §2.3 If i equals 3, say i divided by 0.
  ```

  Version 0's R8 holds §2.2 (true in 3 of 3 evaluations), because the refusal is not at the claim's clause. §8.4
  withholds it: §2.2 is reachable from §2.3 through the While, and the fourth iteration would have evaluated it. Two
  readings follow:
  - §8.4 applies to every run. Then version 0's court readings change: d02 and `d08_guarded_once.orl` lose
    WELL-FOUNDED.
  - §8.4 applies only to runs with an input log. Then adding an unused tick block to d02 flips §2.2's standing,
    although the prefix runs exactly as before.
- **What the draft requires, or the two readings:** as above.
- **Required observable result:** one completeness rule for a prefix loop, whether or not a tick block follows.
- **Falsifying test:** row SCOPE runs d02 alone, and d02 with an empty tick block and `end 0 closed`, and requires the
  same reading of §2.2. *Plant:* scope §8.4 to input-log runs.
- **Proposed repair:** "§8.4 applies to every run, version 0 included, measured one-sided over COMPAT-0's texts (as
  AGENTS.md §4 requires of a rule that withholds)."
- **Change class:** two-way.
- **Grade:**
  - MEASURED (version 0 holds both claims):
    - `d02`: `claim 0 4 3 3 3 0 0`, court `§2.2 evaluation=true in 3 of 3 evaluations support=WELL-FOUNDED`;
    - `d08`: `§2.2 … true in 1 of 1 … WELL-FOUNDED`.
  - DECLARED: the §8.4 reading.

### Finding 23 (severity: wording only)
- **Rule attacked:** §9.1 ("given the law's bytes … every conforming execution writes the same receipt core").
- **Smallest counterexample:** `examples/spellings/words.orl`, `symbols.orl` and `phrases.orl` are three texts of one
  law. They share law-seal `fc88a8eb…`, but their receipt cores differ in one line, `text-seal` (§5.1 keeps
  `text-seal` in the core).
- **What the draft requires, or the two readings:** §9.1 is false as stated. The law's bytes do not determine the
  core; the text does.
- **Required observable result:** §9.1 names the text, or the core drops `text-seal`.
- **Falsifying test:** row REPLAY-INPUTS checks §9.1's statement on the spellings. *Plant:* none; the statement itself
  is the defect.
- **Proposed repair:** "given the text's bytes, the input log's bytes and …".
- **Change class:** two-way (wording). Dropping `text-seal` from the core would be one-way.
- **Grade:** MEASURED. `receipt_cores.py` prints `words.orl vs symbols.orl: 1 of 11 core lines differ` (the
  `text-seal` line), and likewise for `phrases.orl`.

### Finding 24 (severity: wording only)
- **Rule attacked:** §7.2, third identity.
- **Smallest counterexample:** a run refused in its prefix, a run with `end 0 closed`, or a run NOT-RUN at tick 1.
  None of them emits a `'T'`, so "the last `'T'`'s c" does not exist, and a checker either crashes or skips the
  identity. (The identities can fail only under reading R2 of Finding 12, which they rule out. They do not decide
  between R0 and R1.)
- **What the draft requires, or the two readings:** undefined.
- **Required observable result:** an identity for runs with no tick.
- **Falsifying test:** row IDENTITY-NO-T runs the identity checker on a prefix refusal. *Plant:* a checker that indexes
  the last `'T'`.
- **Proposed repair:** "When no `'T'` was emitted, the receipt's `ops` is the prefix's count, the refused operation
  included."
- **Change class:** two-way.
- **Grade:** ESTABLISHED.

### Finding 25 (severity: wording only)
- **Rule attacked:** §8.4, §8.5, and the court's R4.
- **Smallest counterexample:** d02 under §8.4. The court must print something for a claim §8.4 withholds. Version 0
  has labels only for R8 ("REFUSED at evaluation …", "may come from …"). R4 reads a certificate's cost as "NOT READ
  when R8 withholds the claim", and is silent when §8.4 withholds it.
- **What the draft requires, or the two readings:** the evaluation column's text and the certificate reading are
  unstated.
- **Required observable result:** a label naming §8.4, and NOT READ for its certificates.
- **Falsifying test:** row S84-LABEL. *Plant:* the version-0 "true in 3 of 3" label with support UNSUPPORTED.
- **Proposed repair:** "A claim §8.4 withholds reads 'reachable from the refusal at §s: not held (8.4)'. Its cost reading
  is NOT READ."
- **Change class:** two-way.
- **Grade:** ESTABLISHED (`src/orlog/court.py` 275–281, 295–297).

### Finding 26 (severity: wording only)
- **Rule attacked:** §8.4's edges.
- **Smallest counterexample:** an absorbed `Otherwise` clause is a sibling in the label tree. "After a clause, its next
  sibling" therefore leads from an If to its own Otherwise arm, but no rule says whether such a visit enters the arm's
  children. Likewise, "entering s's own body" is undefined when s is a Perform (does a Perform have a body?).
  Neither gap changes a verdict today:
  - every path that needs these edges also passes through a loop's back edge, or through a Perform the path arrives
    at, and those edges enter every arm and body;
  - `d11` reaches its Otherwise claim through the return edge;
  - a refusal at a Perform's own count is possible only under TICK-BUDGET, inside the tick loop.
- **What the draft requires, or the two readings:** two graphs with the same verdicts on every case found.
- **Required observable result:** the graph's edges.
- **Falsifying test:** row S84-GRAPH builds the graph of d11 and compares it with a hand-drawn one. *Plant:* treat the
  Otherwise clause as a plain sibling.
- **Proposed repair:** "An If chain, its absorbed arms included, is one node whose successors are each arm's first
  clause and the clause after the chain. A Perform's body, for 'entering s's own body', is its procedure's."
- **Change class:** two-way.
- **Grade:** DECLARED.

## §8.4: the six cases asked for

Each case gives the law, version 0's reading (MEASURED, run with `measure.py`) and §8.4's reading (DECLARED, worked
by hand).

| case | law | v0 reading | §8.4 reading | right? |
|---|---|---|---|---|
| (i) refusal while evaluating the claim | `d10_in_claim.orl`: `§2 We claim that 1 divided by x equals 1` with x = 0 | `REFUSED at evaluation 1 … not held (R8)` | c = s: not held | yes |
| (ii) refusal on a path to the claim, which is never evaluated | `d09_never_evaluated.orl`: refusal at §2, claim at §3 | `UNREACHED` | reachable, no evaluation: UNREACHED (§8.5) | yes |
| (iii) claim true, then an unrelated refusal | `d01_straight.orl` (straight line) | `true in 1 of 1`, WELL-FOUNDED | not reachable: held | yes. In a tick block it is withheld even at a closed log's last tick (Finding 20). |
| (iv) loop, refusal between evaluations | `d02_loop_unrelated.orl` | WELL-FOUNDED (3 of 3) | reachable through the While: not held | §8.4 is right by its own standard; version 0 disagrees, and the scope is undecided (Finding 22) |
| (v) branch makes the claim unreachable | `d08_guarded_once.orl` (claim guarded by `i equals 1`, refusal at i = 3) | WELL-FOUNDED (1 of 1) | reachable "whatever the values": not held | over-withheld by design: the guard can never hold again. `d11` (an Otherwise arm, two Performs) is over-withheld by the return edge (Finding 21). |
| (vi) refusal before the first input; a run that never reaches it | Finding 10's law (refusal at §2, port at §3) | n/a (version 1) | §1 held and PREFIX-exempt; §4.1 UNREACHED | the log's load (Finding 10) and the court's "rests on input log" are wrong |

**An interrupted claim held.** I looked for one in a REFUSED run and found none. In a REFUSED run, a claim with an
evaluation before s that could be evaluated again after s lies on a cycle of the real control flow through c and s.
Ørlǫg has no recursion and no jump, so every such cycle passes through a loop's back edge (While, For, the tick block)
or through a procedure re-entered by a second Perform. The graph over-approximates both: it treats every loop as
re-enterable and every return as going to every Perform. A refusal during a claim's own evaluation always names the
claim's clause, so c = s:
- rules name their use site (SPEC §6);
- an absorbed arm's condition and inline statement carry the arm's clause (item 18);
- TICK-BUDGET falls on "the clause whose statement is executing".

This is DECLARED (argued, not checked by enumeration). The interrupted claims that are held come from outside the
rule's trigger, or from PREFIX:
- NOT-RUN and LOG-OPEN (Finding 19);
- the scope of §8.4 (Finding 22);
- PREFIX's textual test (Finding 18, the only case that can produce a false GROUNDED).

**Completed claims withheld:**
- the context-insensitive return (Finding 21, with PREFIX claims among its victims);
- the back edge past a closed log's last tick (Finding 20);
- by design, "whatever the values" (case v).

## A1 against A2

Cases are worked by hand (DECLARED). The law has one each-tick port per player, `p1` and `p2`.

**A live multiplayer game with a hostile client:**
- **L1, garbage.** Player 2 sends `x` for tick 7.
  - A1: the arrival is assigned to (7, p2), then refused, and the session ends for every player. A1 does not let the
    host shield the session: it "assigns each arrival … first".
  - A2: the arrival is refused, answered and never assigned. Player 2 can send a valid value before the close, and the
    game goes on.
- **L2, silence or a disconnect.**
  - A2: the host must close tick 7 eventually. It closes without p2's value, and the session ends NOT-RUN 7
    INPUT-MISSING p2. An honest dropped connection ends everyone's game, and silence costs a hostile client less than
    garbage does.
  - A1: no rule. A1 defines no missing value, so the host waits for ever or borrows A2's cause. A1 is incomplete here.
- **L3, flooding.**
  - A1: every arrival is assigned. A client can fill ticks 7 to 16 with valid values and put garbage in tick 17. A1
    does not say whether ticks 8 to 16 still run before the session ends (Finding 5).
  - A2: assigns at most one arrival per slot, and the choice of which one is unrecorded (Finding 2).
- **L4, a valid but hostile value.** The value is 2^63−1, fed into the law's arithmetic. Both doors accept it, the
  law refuses OVERFLOW, and the session ends. Neither candidate helps. A declared port range at the door would help
  only under A2, where a refusal can be retried; under A1 a range refusal is just as fatal.
- **L5, an undeclared port name.**
  - A1: cannot assign the arrival.
  - A2: has no door for it (§1.2's door is a function of a declaration that does not exist).

  Both are incomplete.

**A deterministic test harness:**
- **H1, assert that the door refused a value at tick t.**
  - A1: the refusal reaches the input log's end record, `not-run t INPUT-REFUSED p`, and so the receipt. The harness
    can test it from the receipt alone.
  - A2: the refusal is only in the arrival log, and it is tied to no tick. Arrivals carry no tick, and closes are not
    recorded.

  A1 is better for this case.
- **H2, replay.** Both need the assignments recorded; A2 needs the closes as well (Finding 2). Equal.
- **H3, a script with an invalid value, then a valid one, for one tick (a retry test).** A1 cannot express it, because
  the first value is fatal. A2 can.

**An editor that must keep invalid user input:**
- **E1, a typo sent.**
  - A1: the editor's session ends at the first invalid keystroke it sends. To survive, the editor has to judge every
    value with a door of its own before sending, which is A2 moved outside the contract.
  - A2: the typo is refused and answered. The bytes are kept in the arrival log "as received", and the session
    continues.
- **E2, a non-NFC text.** Neither candidate records the door's note (Finding 3).
- **E3, edit-driven ticks.** The editor closes a tick only when a value is committed. Both candidates survive, provided
  invalid values are never assigned.

**Verdict: A2 survives better.** It has a total rule for each arrival (refuse and continue) and for each tick (close),
so garbage and typos are survivable. Under A1 every malformed arrival is fatal, and A1 is silent on missing values,
duplicate assignments and future ticks.

A2 still fails three of its own cases:
- **L2:** silence is fatal. With no "absent" value, and §1.5 forbidding defaults, a live game cannot survive a
  disconnect. A recorded absence is a fact, not an invented value, so an optional port whose closed-empty value is an
  explicit absence would answer this; that is a language change, proposed only.
- **H1:** a refusal is invisible to the receipt, and the arrival log cannot tie it to a tick unless it records closes.
- **An accepted arrival left unassigned** has no disposition and no answer.

A2 together with Finding 2's records answers all three except L2's.

## The headline challenge: does the arrival log suffice?

**Not as written.** §1.1's arrival log records arrivals and nothing the host decides. The input log is a function of
three things: the arrivals, the host's assignments (and its choice among several accepted arrivals for one slot), and
the host's closes. The last two are recorded only in the input log. So the input log *is* an authority, and §2.5's
"projection" cannot be computed or checked.

**The smallest collapse pair.** One law, one each-tick port, one arrival (`3` from `alice`):
- H1: assign it to tick 1, close, end. COMPLETED, output `3\n`.
- H2: close tick 1 first, then end. NOT-RUN 1 INPUT-MISSING p.

The arrival logs are byte-identical. The input logs and the receipts differ (Finding 2).

The converse collapse is on the input log, with outcomes that a game needs to tell apart. `end 0 not-run 1
INPUT-MISSING p` is written alike for:
- an honest client that was late;
- a client whose only arrivals were refused;
- a host that closed early, or never assigned an arrival it had accepted.

A game must wait for the first, may kick the second, and must fix the third. Under A2 the arrival log separates the
second (its refusals are recorded). It cannot separate the first from the third, because it has no close records.

**With the repair, it can.** Record every arrival's disposition and every close in the arrival log, in one chained
sequence (Findings 2 and 3). Then the input log is a pure projection, which a third party recomputes byte for byte.
It stops being an authority, and the receipt still binds only the input log. Everything the execution contract reads
is then decided by the arrival log, and the late-versus-host-fault pair is told apart by where the close stands in the
sequence.

Two things remain beyond any format:
- **Timing.** Whether an arrival was "late" in wall-clock terms is a host clock, which is not a contract fact.
- **The host's honesty.** The host writes both logs, nothing authenticates a source label, and a lying host can write
  a consistent pair. The integrity of the logs is not their truth.

## What I did not check

- **Version 1 itself.** It is not built, so every version-1 outcome above is worked by hand. The version-0 stand-ins
  show the mechanism (where a refusal lands, what the court holds, how operations are counted), not version 1's
  behaviour.
- **Only the reference ran.** No C or Rust build was made, and the court readings use a witness that states agreement.
  Nothing here tests the arbiter.
- **No test suites.** `tests/selftest.py`, COMPAT-0 and the door fuzz were not run, because no file under `src/` was
  changed.
- **The fixed-point door.** The exact rational comparison, the grid and the bounds of §1.3.3 were read, not computed.
- **Earlier objections.** No prior-art search was made, and the twin was not consulted. Some findings may repeat
  points the drafter's unread records already settle; the files I did not read are listed at the top.
- **The completeness argument.** That §8.4 never wrongly holds a claim in a REFUSED run is argued, not checked by
  enumerating programs.

## Count by severity

| severity | count | findings |
|---|---|---|
| decides a one-way format | 9 | 1–9 |
| changes a verdict | 13 | 10–22 |
| wording only | 4 | 23–26 |
| total | 26 | |
