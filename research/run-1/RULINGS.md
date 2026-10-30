# RUN-1, the open run: the rulings it needs (a sheet for the owner, 2026-10-26)

RUN-1 gives a program declared input ports and a tick block, and records every input as an event in the trace. It is
the roadmap's fourth rung, after COMPAT-0 (built, b85df56), HOST-0 and these rulings
(`research/roadmap-debate/VERDICT.md`). Every one of the five uses (a game or reality engine, a language, an API, an
editing interface, tools for testing) needs it, and none can be reached from today's closed programs. It is also the
hardest thing to add later: it fixes the next receipt, the next trace and the shape of every API built after it.

This sheet asks for the owner's word on each choice RUN-1 must make. Each ruling gives its options, what each entails,
the theorem or design under it, a falsifier, and a recommendation. Rule with the numbers ("R1 b, R2 as written, …"), or
"as recommended" for any group. Nothing here is built, and nothing changes until he rules.

**Ruled so far:** R3 a; R4 a, at tick granularity; R5 with four amendments, the per-tick line in 1a and the
per-event chain kept; R6 a, with three riders, R1's cost sentence and a PREFIX claim held past a later refusal;
the claims ruling, E2 as HELD's meaning with option (d), the meet R8 ∧ CUT-0 pinned to CUT-0's digest; R7 (a),
one independent review of §15's draft with triggered re-reads; and, from that review, D for finding 24 (D10's court
clause scoped to real readings) with B1 + 4a + 5c + K1 for the PREFIX licence, under four conditions (all
2026-10-26); and on 2026-10-27, the labels' definitions adopted (not their conclusions), the closure's rule table,
and R6's row and control sharing the configured witness, with a measured version-0 control as a separate row;
then the closure table's Perform row, and finding 6, read-once ports: A′, as RO′-1 to RO′-6 (2026-10-27). Later the
same day: the release's narrow scope, the seven first-form outputs kept byte for byte; the read-once stop's own row,
its distinguishing receipt status, the owed check (containment) and the order of work (the check, then the pin, then
1a); then the check as a fixture test on the version-1 reference, MEASURED on its fixtures only, findings 8 and 20
resolved before the pin, RO′-5 confirmed (no fifth status word), and the next push only after the full gate on the
next release's exact tree; then every input the pinned rule reads fixed before the pin (the port place, counting,
findings 8 and 20, and the cut's decoding if it is in `'R'`), P6 left to its own trigger; and, as a clarification,
that principle reaching every row of CUT-0 (the version-1 NOT-RUN/LOG-OPEN status encoding, and R2 ruled before
the pin), the containment test's record enumerating the inputs the candidate reads; and on 2026-10-28, finding 8's 8.1 and 8.2: the
read-once stop written `NOT-RUN READ-ONCE …` or `LOG-OPEN READ-ONCE`, its NOT-RUN with no t; then 8.3 (a1), its log's end record `end 0 not-run read-once INPUT-MISSING <port>`; then 8.4 (a), the header-only log the three header lines alone; then 8.5 (a), every other record-less log malformed; then 8.6 (a), the tick case's `NOT-RUN <t> INPUT-MISSING <port>` and bare `LOG-OPEN`, CUT-0's row chosen by the second token; then the read-once record's line, `once <v1> <v2> …`, written only when declared then packet D's D1.a to D1.d, each (i): the existing nine codes, NOT-ASCII above 0x7F, a leading LF
LOG-LINE, a log with a version-0 law a usage error; and on 2026-10-29, D2.1 to D2.6, each (a): compile
first, the whole-log order, the earliest faulty line, the order within a line and a tick record, the header's order; then D3.1 to D3.5: no receipt for a refused load, a deterministic refusal witness; then typed values,
T1 to T6: every value tagged, canonical lowercase hex, LOG-RECORD on a mismatch (finding 8 ruled; R3 and R8 open); then finding 20, F20.1 to F20.4: the
cut carried in version 1's `'R'`, decoded under the header's grammar, the tick block a plain frame, ports none, an If-condition refusal naming the arm (its byte layout still to be probed); then R2, R2.1 to R2.3: two
kinds (the port declaration with its mode, and the tick block), the four spellings, the reach rules; then the port place,
PP1 to PP6: ports at the top level before the tick block, one tick block last, PORT-READ by text and by reach, PORT-VARIABLE; then counting
and the budget, C1 to C3 and B1 to B4: nothing new counted, `'T'`'s running total, R9 (b), N in 1 to 2^62 (FUEL), TICK-BUDGET at operation N + 1; then N2 (a),
an `end()` before the record closes being the read-once stop, and N3 (a), the statements before the first read-once declaration run at the session's opening; then finding 10 (c), a refused session's log carrying no end record; then re-read 9's five questions, each as
recommended, draft 2 the candidate byte grammar to test before the pin; then `close()` refused in a law with no tick block.

**Fixed whatever is ruled:**
- **COMPAT-0 must hold.** Every text v0 accepted keeps its law bytes and its run. RUN-1's forms are therefore spelled
  only where v0 refuses SYNTAX at the statement itself, so they take no meaning away from an existing text.
- **No word is newly reserved.** fall.orl names its loop variable `tick`, and COMPAT-0's plant reserve-tick shows that
  reserving the word would break it.
- **Measured** by `research/run-1/probe_spellings.py`, output in `probe-spellings.txt`:
  - every recommended spelling below is refused SYNTAX at the statement by v0;
  - no line of COMPAT-0's 3,361 frozen texts has any of these forms;
  - the call-shaped candidates ("Receive …", "Take …") are refused UNKNOWN-PROCEDURE instead, because v0 reads a
    statement whose first word is not reserved as a call. They are excluded.

## The theorems RUN-1 rests on

| theorem | what it says | what would falsify it |
|---|---|---|
| **Replay** | every value from outside becomes an event before it is read, so a run is a function of the law and its input log alone, and the trace head commits to both | a recorded log whose receipt differs between two runs, or between two of the four executions |
| **Alignment** | inputs are addressed by (tick, port), never by the order a law happens to read them, so an edited law re-runs over an old log tick for tick | a law edited outside its port declarations that reads an old log out of step (a plant: a misaligned entry, which must be refused, not shifted) |
| **Tick termination** | every loop is bounded and there is no recursion, so every tick ends | a tick that does not end: impossible by construction, held by SPEC's bounds |
| **Capability** | a law reads only the ports it declares | a port read that is not declared, refused at compile time |

These are DECLARED. The arbiter would MEASURE replay per session, four ways.

## Before 1a: the reference and the specification

### R1. Where a world's properties live
The skeptic's question: is a property such as gravity part of the law, of its inputs, or of a data section sealed
apart?

| option | entails | design |
|---|---|---|
| a. In the law, as today | nothing new | the seal names the whole world, but every property change makes a new law: previews rebuild (0.33–1.3 s, the skeptic's measurement), and every ratification of its claims ends |
| **b. A port read once, before the first tick:** `Let gravity be given as a fixed.` | the value lives in the input log's header; the law's seal stays the same when the value changes; the receipt names the log's seal | one mechanism for both kinds of port: one input door, one encoding, one event kind. A "data section" is the log's read-once ports |
| c. A third file, a data section sealed apart | a new artifact type with its own seal, door and receipt line | the same effect as b, with one more format to keep |

**Recommended: b.** The trade-off is that a property moved out of the law leaves the law's claims conditional on the
log, and the court must say so (R6). **Falsifier:** change a read-once value and the law seal moves, or a claim reads
GROUNDED on the strength of the log.

*Added 2026-10-26 by his R6 ruling, before R1 is ruled.* His sentence: *"Moving a world property out of the law and
into a read-once port means the cost of rule a reaches every later claim in the run, stripping them of grounding even
if they never touch that property directly."* "Later" is in the order of evaluation: a claim in a procedure performed
after the port is read is stripped too, wherever its text stands (R6's licence).

### R2. The spellings
| form | spelling | v0 (measured) |
|---|---|---|
| a port read each tick | `Let thrust be given each tick as a fixed.` | SYNTAX at the statement |
| a port read once | `Let gravity be given as a fixed.` | SYNTAX at the statement |
| the tick block | `Each tick, do the following.` | SYNTAX at the statement |
| the tick block with a budget (R9) | `Each tick, at most 100000 operations, do the following.` | SYNTAX at the statement |

- **Types:** `an integer` and `a fixed` are v0's own words. `a truth value` and `a text` are new, inside the port form
  only, and reserved nowhere else. Float ports are R8.
- **Places:** ports at the top level, before the tick block; one tick block, the last top-level clause. New compile
  codes go into SPEC §13's phase table in the same change:
  - PORT-PLACE: a port elsewhere;
  - TICK-PLACE: a tick block elsewhere, or a second one;
  - PORT-VARIABLE: a port assigned. A port is read-only, as a For counter is.
- **Rejected spellings:**
  - `For each tick, do the following.` is SYNTAX in v0 too, but a For loop that lost its bounds would silently become
    a tick block.
  - `On each tick, …` is SYNTAX in v0, but its first word is not reserved.
  - `Receive …` and `Take …` are calls in v0.

**Recommended: the spellings above.** **Falsifier:** COMPAT-0 BROKEN after 1a, or any frozen text newly refused with a
v1 code.

### R3. How input text becomes a value
| option | entails | design |
|---|---|---|
| a. Exact or refused (the conversion rule) | a decimal that is not exactly a Fix value is refused at the door; the log never holds a rounded value | rounding is forbidden. Inputs must arrive already on the 2^-32 grid, or as raw values |
| **b. Rounded once and noted (the literal rule)** | the door rounds half-even, as for a literal, writes the rounded value into the log and a note into its report | rounding is visible and recorded, never silent. An input is text someone wrote, and a literal is treated the same way |

Either way the log holds typed encodings only (RUNTIME-SPEC §5), written once by a Python input door, so no runtime
ever parses decimal text and no host's strtod can diverge. **Recommended: b**, consistent with literals (SPEC §5:
"Fix stores the nearest raw value, ties to even"). **Falsifier:** a backend that parses decimal input (a plant, which
must be caught), or a rounded value with no note.

**Ruled 2026-10-26: a, against the recommendation.** His words: *"I rule in favor of Option a (The Conversion Rule) for
R3."* His reasons, in his words: *"The true, structural differentiator is reversibility under COMPAT-0 and the
preservation of data provenance."* Option a *"treats rounding as a client-side capability rather than an engine-side
compromise."*
- **What it settles.**
  - The door never rounds. A decimal that is not exactly a Fix value is refused, and inputs arrive on the 2^-32 grid
    or as raw values.
  - The log holds only values the supplier sent.
  - A later version may relax this to rounding as an extension, refused becoming accepted. The reverse would break
    every recorded log (COMPAT-0's rule).
- **What falls away.** The rider proposed under b, keeping the supplier's original text under a seal so that a rounding
  stays auditable, is not needed: no value is rounded.
- **The falsifier, under a.**
  - A value in the log that is not exactly the one its text names (a plant: a door that rounds).
  - A backend that parses decimal input.
- **The enactment.** His message opened with the door's grammar: *"The entrance tool filters all incoming port streams
  using a restrictive ASCII regular expression sieve. This occurs before passing strings to Python's Fraction
  constructor, neutralizing format exploitation"* (Python's `Fraction` alone accepts `1e3`, `3/4`, ` 1.5 `, `+1`,
  `1_000` and the Arabic-Indic digit `٣`: measured in the walk-through). The message was cut off there, and he gave
  the other five the same day, as "now finalized for the input door under Option a", in his words:
  - *"Double-Bounded Range Checks: The door must explicitly validate that the parsed value sits securely within the
    strict raw storage parameters of the `Fix` bounds (`MIN_FIX_RAW` and `MAX_FIX_RAW`), actively protecting the lower
    negative boundary against floor overflow errors down to −2147483648.5."* In the code the bounds are
    `numeric_ref.I64_MIN` and `I64_MAX` on the raw value: `-2147483648` is accepted (raw −2^63), and
    `-2147483648.5` is refused.
  - *"Integer Port Restrictions: An incoming string hitting a port explicitly typed as `an integer` must fail
    instantly if a fraction or decimal component is detected. Truncation or automatic floor-rounding at the gate is
    blocked."*
  - *"Boolean Uniqueness: Truth-value channels accept exactly one invariant string spelling for `true` and one for
    `false`. Alternative representations, case variations, or numeric bits (`1`/`0`) are refused."*
  - *"Text Byte Purity: String inputs are preserved byte-for-byte as sent. Non-NFC unicode payloads generate an
    explicit report note; CP1252 character maps are rejected outright."* The note needs no seal of its own: it can
    be recomputed from the logged bytes.
  - *"Raw Value Spellings & Neighbor Refusals: Raw hexadecimal scalar strings are given an isolated syntactic prefix
    that the text grammar tracks separately from standard base-10 decimals. When a user input is rejected for
    non-alignment with the 2^-32 fixed-point grid, the door's refusal message must explicitly compute and output the
    two nearest valid representable grid coordinates to the client."*

  Left for 1a's specification, each a detail his words fix in kind but not in spelling:
  - the one spelling each for true and false;
  - the raw prefix, and how a raw value's sign is written;
  - whether text also refuses what the literal door refuses (format characters other than ZWJ and ZWNJ, Hangul
    fillers, line and paragraph separators).

### R4. What a refusal does in a run with ticks
| option | entails | design |
|---|---|---|
| **a. It ends the branch** | the run stops at the refusing tick; the receipt says REFUSED code, clause and tick; recovery is a new branch from an earlier snapshot (SNAP-1), and the refused branch stays in the record | the refuted claim's evaluation stands |
| b. It rolls the tick back and the run goes on | friendlier to a game loop | it erases the refutation: the court would read "true in n of n" for ever. A rolled-back refusal is a laundered verdict |

**Recommended: a.** **Falsifier:** a session whose court reading omits an evaluation that refused. *(Note,
2026-10-26: the doppler debate found this falsifier already firing in version 0 (DP-5). A claim whose evaluation
refused partway read "true in 16 of 16" and GROUNDED. The court's R8 now names that evaluation and does not hold the
claim: `evidence/court-r8.txt`.)*

**Ruled 2026-10-26: a, at tick granularity, as recommended.** His words: *"I rule R4 as written in your proposed
ruling text: (a) at tick granularity, with automatic continuation deferred until SNAP-1, and the refused branch
permanently sealed and queryable."* The text he ruled:

> R4: a, at tick granularity. A refusal ends its branch at tick t. The session may continue on a new branch from tick
> t−1, rebuilt by replay from the nearest checked snapshot and checked against the tick line's state digest, reading
> tick t by a declared continuation rule written into the log. The refused branch is kept, sealed and queryable. The
> court reads each branch on its own and names every abandoned branch. Automatic continuation waits for SNAP-1; until
> then a refusal ends the session.

- **What it settles.**
  - Until SNAP-1 a refusal ends the session, as the table's a.
  - A rollback is a branch, never an erasure. The refusal stays in the record, so the court never reads a laundered
    "true in n of n".
  - A continued branch reads tick t by a rule written into the log, so a run stays a function of its law and log.
- **What it leaves open.** The reporting pass's question stays the owner's: whether a claim that held stays held on a
  branch refused elsewhere, and in any run before SNAP-1. On a continued branch it does not arise. *(Note,
  2026-10-26: his R6 ruling settles it for a PREFIX claim and a refusal at a tick: the claim stays held. It stays open
  for a refusal before the first input and for every closed run.)*
- **Proposed with it for SNAP-1, not ruled.** From a review the owner relayed the same day, and the speed debate:
  - the rebuild runs in a fresh process, and is checked against the state digest of an execution other than the one
    that restores (the reference's line), so the restorer is never its own sole verifier;
  - the court's summary counts abandoned branches beside `refuted` and `refused_evaluation`;
  - the restore is held by plants: a corrupted restore must be caught against the state digest (the speed verdict's
    O3);
  - the continuation record's form, and what tick t reads (the previous value or a declared default), ruled with
    SNAP-1.

### R5. Versions and headers
- `orlog-law 1`, only when a v1 form appears, so v0 laws stay byte-identical. It adds the law lines
  `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`.
- `orlog-trace-1`: `head0 = SHA-256("orlog-trace-1" || law_seal)`. New events: `'T'`, the tick number (u64); `'N'`, a
  port's value (u32 var and the value encoding of RUNTIME-SPEC §5). Each tick emits `'T'`, then one `'N'` per
  each-tick port in declaration order, then the body. The read-once ports' `'N'` events come before the first `'T'`.
- `orlog-receipt 1` adds `ticks <n>` and `input-log-sha256 <hex>`. It replaces `output-sha256` with `output-chain
  <hex>`, where out_t = SHA-256(out_{t−1} || SHA-256(the output of tick t)). A snapshot then carries the output as one
  hash; a plain running SHA-256 would need a hash midstate, which CPython's hashlib cannot export.

**Recommended: as written.** **Falsifier:** any v0 receipt or law byte changed (COMPAT-0), or a snapshot that cannot
reproduce the output chain.

**Ruled 2026-10-26: as written, with four amendments, and two choices fixed.** His words: *"I rule `R5` as written,
augmented by your four explicit amendments"*. The amendments, proposed in the walk-through:
1. **`'T'`'s payload is the tick and the operation count** (u64, u64). Per-tick heads as written cannot see an
   operation-count defect: in P12, rerun by the speed debate's judge, a shared counting defect under a budget was named
   at tick 246 when the executions parted at tick 1, and at tick 1 with ops in `'T'`. *(Note, 2026-10-26: the
   speed debate's proposal reads "the operation count at the boundary" (`research/speed/PROPONENT-R2.md`). `'T'` is
   emitted before its tick's body runs, so it cannot carry its own tick's count. Whether it carries the running total
   at the boundary or the previous tick's own count is a reading for §15, and for R7's round.)*
2. **The output chain's start and edges are defined:** out_0, the output said before the first tick, and a refused
   tick's partial output. On the last, his words: *"if a tick encounters a transactional refusal, its partial output is
   formally hashed into the chain before the rollback logic clears the volatile state"*, so a refused tick's partial
   output is the chain's last link. He wrote of out_0 as *"the initial hash of any visual bytes or metadata written
   before the first tick"*. Read as the bytes said before the first tick: the output holds nothing else.
3. **`ticks <n>` at a refusal counts the ticks begun,** and a refused tick writes no per-tick line; its record is the
   receipt's status and the trace's `'R'` event. This is R4 a, ruled at tick granularity. His message calls it
   "R4 c", which no ruling names.
4. **The receipt frame check is versioned, with its plants.** Today `src/orlog/arbiter.py` (`receipt_core`) accepts only
   a receipt that begins `orlog-receipt 0`. As written, every v1 receipt would fail it and every backend read as
   dissenting. His words: *"The arbiter must accept both `orlog-receipt 0` and `orlog-receipt 1` formats depending on
   the code path. To keep this defensive, we implement the requested inverse plants: a `v1` receipt checked under a
   `v0` template must fail, and a `v0` payload evaluated under `v1` rules must be caught and refused."* Read as: the
   check requires the version the law's own header names (`orlog-law 0`, a v0 receipt; `orlog-law 1`, a v1 receipt),
   never either one for any law. Accepting either would be a lenient comparison, E7's class, and his two plants
   already require this reading. The runtimes write receipts and parse none; each writes the header its law's version
   requires. *Confirmed the same day:* *"Tying the receipt frame check strictly to the law's own header (`orlog-law 0`
   demands `orlog-receipt 0`, and `orlog-law 1` demands `orlog-receipt 1`) is the only sound option."*

The two choices R5 fixed now or never:
- **The per-tick line, `orlog-ticks 0`, is part of 1a.** His words: *"We include this artifact now within the `1a`
  specification. Do not defer it to a later version."* Its fields are the speed verdict's (`research/speed/VERDICT.md`):
  the tick, events, ops, output bytes, the trace head (`-` in a play build without the chain), the output chain, a
  claims digest, a state digest. The state digest's cost on a large state (linear in the state; a digest every k
  ticks names a silent write's window) is for 1a's specification.
- **The trace keeps the per-event chain; no stream head.** His words: *"We keep the per-event chain exactly as written
  instead of switching to a compressed stream head."* His reason: losing event-level localization of a defect in the
  commitment's own code (the speed debate's O5) *"destroys our core epistemic edge"*, and *"The safety margin of the
  per-event chain is worth the processing cost."*

### R6. What the input log is to the court
| option | entails | design |
|---|---|---|
| **a. Data, never a channel** | in a run with an input log (the law declares a port, or has a tick block), no claim is GROUNDED, whatever its channel and whatever is ratified, except under the licence below; the court shows the log's seal as provenance: "rests on input log <seal>, unratified" | replayable is not admissible (DOCTRINE T12, limit 4). A log is a value chosen by whoever ran the session, and it can never raise a standing |
| b. Testimony | a person may ratify a log's seal ("this is what the sensor recorded"); a claim over that log could be GROUNDED only with both its own seal and the log's ratified | the supplier's word becomes explicit and signed, as the ledger makes a ratification. That is a court change, in the territory of typed terminals (DOCTRINE §9, fork 9) |

**Recommended: a for RUN-1; b as a later fork.**
- **The trigger is any input log.** A tick block with no port still takes input, because the log's length sets how
  many ticks run (D3). A claim in it can hold over 16 ticks and be refuted at 17.
- **The licence, PREFIX**, decided from the text: a claim is exempt only if every evaluation of it precedes the first
  input.
  - It must stand before the first port declaration, outside the tick block.
  - It must not sit in a procedure performed at or after the first port declaration. The licence is decided by
    evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still
    runs during it.
  - Nothing the log sets exists before its first input, so a prefix claim's whole claim line is fixed by the law: its
    evaluations, its trues, its cost and its certified clause's cost.
  - A wider licence would exempt a claim with no path from any port, shown by two independent derivations, and must
    then cover the whole claim line, since a certificate's cost reading can move with a port while its truth does not.
    It waits for a trigger (`research/doppler/VERDICT.md`).
- **Falsifier:** a claim in a run with an input log that reads GROUNDED outside the licence. The acceptance rows:
  - a claim that reads only `x`, where `x` is updated from a port, rests on the owner and has its own seal ratified,
    reads UNGROUNDED;
  - a claim in a tick block with no port reads UNGROUNDED (plant: the trigger "declares any port");
  - a claim in a procedure performed in the tick block reads UNGROUNDED (plant: licensing by clause position);
  - a claim before the first port, in a procedure performed after a port is read, is not licensed (plant: "before the
    first port declaration is enough").
  The narrow wording below is that row's plant, and must be caught.
- **Sound, not complete.** Rule a never reads a false GROUNDED, but it also withholds grounding from a claim that
  depends on no port at all. That is a known limit. The backward slice (fork 4) lifts it: a claim whose evaluation
  provably depends on no port could be groundable again.
- **Time and randomness add no second case.** No runtime reads a clock, the environment or entropy (RUNTIME-SPEC §1).
  Under RUN-1 they could enter only as ports (D7), so they fall under this same rule.

*Amended 2026-10-26, before any ruling.* The first wording read: "a claim whose condition reads a port stays a claim of
the program's computation and is never GROUNDED". It misses dependence through state. A claim about `x` never reads the
port, but its truth depends on the log once `x` is updated from the port, and the court sees only direct, declared
dependence (L10). `research/run-1/r6_indirect.py` measures this in version 0, with the port played by a variable set
once from a literal (`evidence/run1-r6-indirect.txt`):
- the claim's condition reads `x` alone;
- its truth turns on the stand-in, holding at 1 and 2 and refuted at the 17th tick at 6;
- with its own seal ratified it reads GROUNDED. That is legitimate in version 0, where the value is in the ratified law
  and a different value gives a different claim seal.

With a real port the law and the claim seal stay the same for every log, so the narrow wording would let that claim
read GROUNDED over a log nobody vouched for. A control shows the narrow check itself works: it does withhold grounding
from a claim that reads the stand-in directly.

*Amended again 2026-10-26, after the doppler debate, before any ruling* (`research/doppler/VERDICT.md`):
- **The trigger** was "declares any port". It missed a tick block with no port, whose log's length is input (DP-4).
- **The licence (PREFIX)** was added, decided by evaluation (N-1) and covering the whole claim line (N-2). The debate's
  proponent and adversary both arrived at it, and the adversary's fixtures measured each hole. The judge reran the
  procedure case and the cost case.

**Ruled 2026-10-26: a, with three riders and the R1 sentence; b a later fork.** His words: *"I rule Option a (Data,
never a channel) for `RUN-1`. The primary principle is unyielding: replayable data is not admissible testimony."* And:
*"`Option b` stays held as a later potential fork for a future court update."* What he ruled with it, nothing of it
built:
- **R1's cost sentence**, appended to R1 below his ruling of it (R1 is not yet ruled).
- **One seal.** *"The court's generated provenance output line must print exactly the `input-log-sha256` value defined
  in `receipt 1`."* The line reads `rests on input log <input-log-sha256>, unratified`.
- **No vacuous row.** Until 1b every v1 run reads REFERENCE-ONLY (D10), nothing is held, and GROUNDED needs held
  (`src/orlog/court.py`, `panel`), so a row expecting UNGROUNDED would pass whether R6 works or not. His two riders:
  - *"Every row testing an ungrounded port violation must run with the witness explicitly configured as agreed"*, as
    `tests/court_monotone.py` and `research/r8_coverage.py` do;
  - *"Each test row is structurally paired with an internal control variant. The control evaluates the exact same
    claim without an active log declaration, or wraps it securely within the `PREFIX` license parameters. The control
    must return a clean `GROUNDED` standing"*, so that the withholding is shown to come from R6.

  *Answered 2026-10-26 by the finding-24 ruling (below): real readings stay REFERENCE-ONLY until 1b, and these rows,
  the PREFIX row and their controls run in 1a with the agreed witness configured, each saying so.*
- **R12's note**, made there: the one-sided measure over COMPAT-0's texts cannot exercise R6, and the withholding is
  held by R6's own fixtures alone.
- **The reporting pass's question, for a PREFIX claim.** His words: *"A claim wrapped within the `PREFIX` license
  parameters that evaluated true remains historically held, regardless of whether the execution loop encounters a
  subsequent transactional refusal downstream."* His reason: its claim line is fixed by the law, and *"a downstream
  failure on frame t cannot retrospectively invalidate a pure, law-bound proof that completed before the timeline even
  initiated."* The court as built already reads it so: a refusal outside a claim's clause leaves it held (`panel`'s
  `held`). The ruling makes that reading a requirement for RUN-1. Its rows: a PREFIX claim with its own seal ratified,
  in a session refused at tick t, reads held and GROUNDED; a claim of the tick block in the same session reads
  UNGROUNDED. A court that withholds every claim of a refused run is the plant, and the first row must catch it.
  - **Its scope is his reason's.** Every evaluation of a PREFIX claim precedes the first input, and a refusal at a tick
    comes after the first input, so that refusal cuts off none of the claim's evaluations. A refusal inside the prefix,
    before the first input, can: a PREFIX claim in a loop, refused between two of its evaluations, reads "true in 1 of
    1". That is the closed run's case (`tests/fixtures/court/hoisted_omit.orl`), and it stays his open question.
- **Proposed with it, not ruled.** The tightest control is the same run read by the court with R6's fence off (a
  parameter, as `panel`'s `r8`). A control without the log is another law with another claim seal; the same run with
  the fence off shows that this very claim, in this very run, would read GROUNDED but for R6.

### The claims ruling: what HELD means in version 1, and the settlement rule

*Added 2026-10-26 by his ruling. It is not one of R1–R12. Its options and measurements are in `ROUNDS.md` (the
amended set's claims row, and the sections after it) and in `SETTLEMENT-DEBATE.md`.*

**Ruled 2026-10-26: E2, and option (d).** His words:

> My ruling: E2 is the meaning of `HELD` for version 1.
> `HELD` means that every completed evaluation of the claim was true, no evaluation of that claim remains open at the cut, and the continuation at the cut could not evaluate that claim again.
> I adopt option (d): admit the meet \(R8 \land CUT\text{-}0\), pinned to the exact CUT-0 digest, with each withholding identifying its structural row. CUT-0 alone remains the target for further development.
> The scope of this ruling is:
>
> 1. Authoritative standing: E2 governs `HELD`. E1's “true in \(k\) of \(k\) evaluations” remains descriptive evidence, not a substitute for settlement.
> 2. Claim-specific continuation: Only continuation that could evaluate the particular claim again affects its standing. Unrelated pending execution does not withhold it.
> 3. Withholding explanations: Every CUT-0 withholding must identify the responsible structural row.
> 4. Rule identity: The admitted meet must identify the exact CUT-0 digest. A digest identifies the rule; it does not prove the rule sound.
> 5. Proof obligations: T10 remains open and must be split into row-specific obligations. The `While` next-pass row is the priority for precision investigation. No test result or measurement alone closes T10.
> 6. Unchanged obligations: T11 remains open. This ruling establishes neither compatibility preservation nor general soundness.
> 7. Governance record: Record this semantic decision in `RULINGS.md` in the owner's words, and have DOCTRINE refer to it. Do not represent the decision as a theorem-ledger result.
>
> The 40,141 `CONFIRMED` cases remain withheld under E2 because their tested resumptions actually evaluated the claims again. Releasing claims whose truth cannot change would require a separate, stronger invariance rule; that is not part of this version 1 ruling.
> This is the normative decision. It does not claim that I have edited files, committed changes, or discharged the outstanding proof obligations.

**What it fixes.** None of it is built:
- **HELD in version 1 is E2,** as `CUT-0.md` §1 defines it. Every reading keeps "true in k of k evaluations"
  (`src/orlog/court.py`), as description.
- **1a's court admits the meet R8 ∧ CUT-0, naming CUT-0's exact digest.** Under the meet, nothing is held above R8.
  Every withholding names its row: one of the five parts of K̂ measured in `SETTLEMENT-DEBATE.md` §7, or, in version 1,
  a Perform refused at its own operation, or the open claim.
- **CUT-0 alone is the target.** Its 7 gains over R8, all unreached by the oracle, enter only by a later ruling.
- **T10 is split by row** in `ROUNDS.md`'s theorem ledger (T10.1–T10.6, done with this record), with the While row
  first for precision. T11 stays open. The ledger records no result from this ruling: it is a decision on meaning.
- **His R6 settlement for a PREFIX claim holds under it.** A refusal at a tick leaves a claim of the prefix out of K̂
  (`FORK.md` §1).

**What it supersedes:**
- D8's reading below. "True in n of n" stays as description, and standing is E2.
- The claims row of `ROUNDS.md`'s amended set.

**What stays open:** the amended set's other rows; R7; the cut's format freeze, which is due before the first
version-1 receipt is frozen anywhere (`CUT-SCHEMA.md` P6); and the invariance rule, which his ruling leaves out of
version 1.

### R7. A twin round before the backends
| option | entails | design |
|---|---|---|
| **a. A paper round first** | the twin's author reads SPEC §15 alone and hand-works probes before 1a's code is final; each difference is settled in writing, as in rounds 1 to 3 | the cheapest time to find a misreading of §15 is before three generators and two runtimes encode it. Every earlier round found reference defects and open readings (62 notes; then 163 and 128 probes) |
| b. After 1b | faster to a first session | readings would be settled against code that already exists in five places |

**Recommended: a**, the skeptic's "hold the twin's paper round first". **Falsifier:** a §15 reading that the twin and
the reference work differently and that §15 does not settle.

**Ruled 2026-10-26: (a), as one independent review with triggered re-reads.** His words: *"Record R7 in `RULINGS.md`
using the final agreed wording."* And: *"The key constraint is unchanged: no push before the final gate, and no §15
clause built before the required review."*

**Where the wording comes from.** The final agreed wording below was not written by him; he adopted it by the
instruction above. It combines two texts:
- the proposal made to him the same day, after a debate he forwarded (single round against staged rounds, gates
  against rounds);
- the three annotations of the consensus he forwarded next: the tag audit's timing, the union of the re-read sets,
  and the probe-source falsifier. That consensus also drew the "as ruled" distinction and stated the operative
  principle.

> **R7: one independent review of `SPEC-15-DRAFT.md`, then triggered re-reads.**
>
> 1. **The reading set.** The twin reads SPEC §1–§14, `RUNTIME-SPEC.md`, `SPEC-15-DRAFT.md`, the statements of
>    T10.0–T10.7, and the rulings the draft's tags cite, as ruled. "As ruled" means the owner's decision and the text
>    it explicitly adopts by reference, to the extent adopted: not every statement in the referenced document, and
>    not the sheet's options, recommendations or notes. It reads no other research record, probe or evidence. Any
>    further source it needs is recorded with its reason, as a scope expansion R7 permits.
> 2. **The report has two sections.**
>    - **Coherence:** for each open clause, whether it is interpretable, where it conflicts with established rules,
>      its missing cases and invalid inferences, and whether each clause's tags name every ruling it depends on.
>      Open clauses are proposals, never rules.
>    - **Faithfulness:** whether each ruled clause states its ruling, with no verdict on clauses not yet ruled.
>
>    The twin records hand-worked probes with their expected outcomes, marked unexecuted. It analyzes R4's "code,
>    clause and tick" and the reading of "port place" as findings, not rulings: their plausible readings, and whether
>    the draft selects one unambiguously.
> 3. **The tag audit comes first.** It is done before the owner relies on the report to rule on, or to build, the
>    clause concerned, and its findings feed the re-read sets.
> 4. **The re-reads.** A ruling being made triggers the re-read of A_r = T_r ∪ L_r ∪ D_r:
>    - T_r, the clauses tagged with ruling r;
>    - L_r, the clauses containing terms r defines or newly defines, by recorded term closure;
>    - D_r, the clauses the review recorded as dependent on r.
>
>    Each clause of A_r is re-read once per triggering ruling, before it is built. The set is recorded, and the
>    builder may not narrow it. A dependency identified later enters D_r and is recorded. A_r makes no claim to hold
>    every semantic dependency.
> 5. **The build gate.** No §15 clause is built before the twin has read it, and no clause of A_r before its re-read.
> 6. **The scope.** R7 settles review timing only. It closes no theorem, promotes no open clause, and does not move
>    the draft into `SPEC.md`. Running the recorded probes against 1a falls under the existing probe obligation. The
>    review is review evidence, not proof of correctness.
>
> **The operative principle:** the twin reviews the draft against established rules and actual rulings; the tags
> declare dependencies, term closure adds a mechanical net, and the independent audit can expand the affected set.
> The builder cannot narrow it.
>
> **Falsifiers:**
> - a clause of a recorded A_r built before its re-read;
> - a clause that depends on a ruling its tags do not name, built without the audit catching it;
> - a faithfulness verdict on an unruled clause;
> - a finding or probe that relies on an excluded research record, probe or evidence without a recorded, justified
>   scope expansion permitted by R7.
>
> **Limits:** the twin and the author are one model family, so a shared misreading can survive. The tags are
> declared dependence, audited but not proved.

### Finding 24 and the PREFIX licence: the first rulings from R7's review

*Added 2026-10-26 by his ruling. It is not one of R1–R12. It decides findings 3, 4, 5 and 24 of R7's review
(`twin-r7/REPORT.md`, disposed in `twin-r7/DISPOSITION.md`), from the decision packets `packets/A-D10-R6.md` and
`packets/B-PREFIX.md`, integrated in `packets/INTEGRATION.md`.*

**Ruled 2026-10-26: D for finding 24, and B1 + 4a + 5c + K1 for PREFIX, as two linked rulings with four conditions.**
He had forwarded a proposal that called itself "proposed rulings for you to adopt or reject", and was asked whether he
adopts it as his ruling. His words, his whole answer:

> Adopt as written (Recommended).
>
> I adopt D for finding 24 and B1 + 4a + 5c + K1 for PREFIX (findings 3–5) as my rulings, subject to the four stated conditions. The scope is limited: this resolves the D10/R6 interaction and the PREFIX licensing boundary; it does not close T10/T11, establish CUT-0’s soundness, or independently verify reference arithmetic.
>
> The four conditions are part of the ruling:
> 1. The configured witness covers the PREFIX row and its controls, not only ungrounded rows; results say configured, not measured.
> 2. Reach fails closed on unknown statement kinds, including the version-1 tick-block case.
> 3. An independent structural oracle checks PREFIX licensing; the trace is a check, not the rule.
> 4. Nothing is built before the twin rereads the affected clauses under R7.
> The adopted text must preserve the distinction between a real court reading (REFERENCE-ONLY until 1b, holding no claim) and 1a test rows that exercise the reference with the agreed witness configured. Court R1 remains a condition of HELD alongside E2.
>
> I authorize recording this answer as my ruling, with the cited packet A §5 and packet B §4 wording adopted verbatim as specified. After recording, compute each ruling’s affected-clause set \(A_r = T_r \cup L_r \cup D_r\), including dependencies identified by the twin’s tag audit, and have the twin perform the required rereads before any build.

**The text he adopted, verbatim, as his answer specifies.** Three texts. Their first person is their authors', not
his.

1. **The proposal he forwarded**, an outside review's, written to him the same day:

> My ruling is D for finding 24, paired with B1 + 4a + 5c + K1 for PREFIX (findings 3–5), subject to one important qualification: D10 governs real court readings, while the R6 test rows may exercise the 1a reference with a configured witness. This does not make those test rows evidence that the reference's version-1 arithmetic is correct.
> I would record these as two linked but distinct rulings. D resolves the scope conflict; PREFIX defines the licence the rows test. Neither settles read-once ports or load-refusal behavior.
> 1. Finding 24 — D10 against R6
> Adopt packet A's proposed scope distinction:
>
> * Until 1b, a real court reading of a version-1 run remains `REFERENCE-ONLY` and holds no claim.
> * R6's rows, the PREFIX row, and their controls may run in 1a against the reference with the agreed witness configured.
> * Each such row must explicitly say that its agreement is configured, not measured.
> * Court R1 remains a condition of `HELD` alongside E2. The claims ruling is not amended.
>
> That last point is essential. E2 defines the claim-specific continuation condition; it does not erase the court's backend-agreement requirement. A configured witness does not constitute independent backend agreement.
> Scope: this changes D10's wording as a default for real court readings versus test execution. It does not overrule R6 or establish version-1 execution correctness.
> 2. PREFIX — findings 3–5
> Adopt packet B's proposed interpretation of R6, not D-18's wider boundary.
> The boundary is the first top-level clause that is or holds a port declaration of either kind, or is the tick block. A claim is licensed exactly when:
>
> 1. It stands before that boundary and outside the tick block.
> 2. No clause from the boundary onward can execute it.
>
> The closure follows all branches, loop bodies, tick bodies, and procedure calls transitively; it ignores runtime values and fails closed for statement kinds without a closure rule.
> Consequences:
>
> * A law with a tick block but no port still has a boundary at the tick block.
> * A claim after an each-tick port declaration is not licensed merely because it never reads that port.
> * D-18's alternative boundary is not adopted; using it would widen R6.
> * A licensed claim must still satisfy the existing settlement rules. Licensing is not `GROUNDED` or `HELD` by itself.
>
> This interpretation preserves R6's sound-but-not-complete posture: a claim may be conservatively excluded even when a particular execution would never reach an input-dependent path.
> 3. Conditions attached to these rulings
> I would require the following to be recorded alongside the decisions:
>
> * Witness scope: explicitly confirm that the configured witness covers the PREFIX row and its controls, not only the ungrounded rows.
> * Reach implementation: the version-1 closure must fail closed on the tick block and unknown statement kinds. The existing version-0 default behavior is not enough to establish this.
> * Independent oracle: the PREFIX test oracle must establish the licence from source structure across its fixtures and logs; trace data may check the result, but must not define the rule.
> * No premature build: the twin must reread the affected clauses under R7 before they are built.
>
> 4. What remains open
> These rulings do not settle:
>
> * Finding 6: read-once binding position, missing-value behavior, or session event representation.
> * Finding 8: `LOG-*` conditions, load-refusal receipts, or provenance-line obligations.
> * The version-1 format freeze.
> * T10/T11 or the soundness of CUT-0.
> * Whether the reference's version-1 execution arithmetic agrees with an independent backend.
>
> The read-once question should come next, followed by the load-refusal ruling, as your integration record recommends.
> Recordkeeping note: these are my proposed rulings for you to adopt or reject, not changes made to `RULINGS.md`. Once you record them in your own words, compute the affected-clause sets \(A_r=T_r\cup L_r\cup D_r\), including the twin's missing-dependency audit findings. Then have the twin reread the resulting clauses before implementation.

2. **Packet A §5's wording**, D10's court clause (`packets/A-D10-R6.md`):

> D10, the court clause: until 1b, the court's reading of a version-1 run, read with the witness the arbiter makes, is REFERENCE-ONLY and holds no claim (court R1, unchanged). This governs readings of runs, not the court's rows: R6's rows, the PREFIX row and each row's control run in 1a's reference with the witness configured as agreed, as R6's first rider requires, and each such row states that its agreement is configured, not measured.

3. **Packet B §4's wording**, the licence (`packets/B-PREFIX.md`):

> The licence is decided from the law's text alone, never from a log or a trace. The boundary is the first top-level clause, in the text, that is or holds a port declaration, or is the tick block. A claim is licensed exactly when (a) it stands before the boundary and outside the tick block, and (b) no clause from the boundary on may execute it. The closure follows every arm, the body of every loop and of the tick block, and every procedure performed, transitively, with values ignored. A statement kind the closure has no rule for licenses no claim of the law.

**What it fixes.** None of it is built:
- **D10's court clause, scoped.** A real court reading of a version-1 run is REFERENCE-ONLY until 1b and holds no
  claim (court R1, unchanged). R6's rows, the PREFIX row and their controls run in 1a's reference with the agreed
  witness configured, and each says its agreement is configured, not measured. No such row is evidence that the
  reference's version-1 arithmetic is right. D10's two-commit split is not ruled with it.
- **Court R1 stays a condition of HELD beside E2.** The claims ruling is not amended.
- **The configured witness covers the PREFIX row and its controls** (condition 1), not only the rows of an ungrounded
  port violation.
- **The licence.** The boundary is the first top-level clause, in the text, that is or holds a port declaration of
  either kind, or is the tick block, so a law with a tick block and no port has its boundary there. A claim is licensed
  exactly when it stands before the boundary, outside the tick block, and no clause from the boundary on may execute
  it. The closure follows every arm, loop body, tick body and procedure performed, transitively, with values ignored.
- **The closure fails closed** on the tick block and on any statement kind it has no rule for (condition 2). This
  record reads packet B's last sentence, "a statement kind the closure has no rule for licenses no claim of the law",
  as the form that failing closed takes. `Reach`'s version-0 default does not establish it (`CUT-0.md` §2's limits).
- **An independent structural oracle** checks the licence from the source across its fixtures and logs. A trace may
  check the result and never defines the rule (condition 3).
- **D-18's boundary is not adopted** (`ROUNDS.md`: the decisions table, and Round D's row 18). Using it would widen R6.
- **A licence is not a standing.** A licensed claim still needs held, a ratified seal and a channel that can ground to
  read GROUNDED. R6's riders and his PREFIX settlement stand.
- **Nothing is built before the twin's re-read** of each ruling's A_r under R7 (condition 4).

**What it refines:** D10's court clause (the defaults, below), and R6's "No vacuous row" note (above), which it
answers. The amended set's PREFIX row in `ROUNDS.md` is ruled by it.

**What stays open**, as his answer and the proposal name it: finding 6 (where a read-once value binds, a missing value,
the session event); finding 8 (the LOG-* conditions, a load refusal's receipt, the provenance line's obligations); the
version-1 format freeze; T10, T11 and CUT-0's soundness; whether the reference's version-1 arithmetic agrees with an
independent backend; and the amended set's other rows.

**Its re-reads:** each ruling's A_r, computed after this record, is in `twin-r7/AR-F24-PREFIX.md`.

### The labels' definitions, the closure's rule table, and R6's control (2026-10-27)

*Added 2026-10-27 by his rulings on three questions R7's first re-read raised (`twin-r7/REREAD-1-REPORT.md`, disposed
in `twin-r7/REREAD-1-DISPOSITION.md`: PREFIX-1 and PREFIX-4, PREFIX-3, and F24-6). Each question is given as it was put
to him, then his answer, whole and unchanged.*

**1. The labels.** Asked: "Your answer adopted the labels D and B1 + 4a + 5c + K1, which packet A §4 and packet B §3
define. Do the labels adopt those definitions? If so, K1's definition settles two of the twin's findings: the closure
follows the tick block's body (PREFIX-1), and an unperformed To after the boundary adds nothing (PREFIX-4)." His words:

> Other — adopt the definitions, but do not automatically accept the claimed downstream conclusions.
>
> My ruling is that adopting D and B1 + 4a + 5c + K1 adopts the definitions those labels designate in packets A and B, not merely the labels or their headline wording. Otherwise the ruling would refer to options without specifying their operative meaning.
>
> However, that does not mean every conclusion drawn from those definitions is automatically established. In particular:
>
> - PREFIX-1: The tick block must have its own closure rule that follows its body. The closure must fail closed on unknown statement kinds. This does not by itself establish that PX-6 is licensed; that result must follow from the complete source-structure rule and fixture.
> - PREFIX-4: An unperformed `To` after the boundary contributes no executed call to the transitive closure. But licensing is determined from source structure with values ignored, so the fact that a call is unperformed at runtime is not, by itself, sufficient to establish that a claim is licensed.
> - Port declarations: Do not infer that the absence of a closure rule for port declarations licenses claims—or automatically makes every law with a port unlicensable. The adopted rule requires an explicit, sound closure treatment of the relevant statement kinds. If the packets' definitions leave that point unresolved, return it as a precise ruling question rather than silently extending K1.
>
> Record the definitions as adopted text, preserve the distinction between the ruling and its tested consequences, and have the twin reread the affected clauses before any build. Do not mark PX-6 licensed merely because the label was adopted.

**2. The closure's rule table.** Asked: "The closure's rule table (PREFIX-3), proposed from K1 and SPEC §3: a claim adds
itself; If/Unless/Otherwise add every arm; For and While add their body; the tick block adds its body; Perform adds the
procedure's body, transitively; To, Define and Decimals add nothing when reached; Let, Set, Increase, Decrease, Say,
Append, Remove, Must and a port declaration add nothing; any other kind licenses no claim of the law. Adopt it?" His
words:

> Adopt the table, with one clarification to its wording.
>
> The closure needs an explicit rule for every known statement kind; otherwise, “fail closed” would treat a port declaration as unknown and exclude every claim in a law containing a port. That would be unnecessarily conservative and would not implement the intended PREFIX licence.
>
> Adopt the proposed table for PREFIX-3 / §15.12.4, with these conditions:
>
> 1. Structural closure only. Follow every arm, loop body, tick-block body, and performed procedure transitively, ignoring runtime values.
> 2. Known no-addition kinds are explicit. `To`, `Define`, `Decimals`, and the listed simple statements and port declarations add no further reachable body under this rule. This does not exempt their surrounding clauses from the boundary or licensing test.
> 3. Unknown kinds fail closed. Any statement kind without an explicit rule licenses no claim of the law.
> 4. No runtime shortcut. An unperformed `To` adds no procedure body because the closure is source-structural—not because a particular execution skipped it.
>
> This adopts the closure table; it does not establish that any individual claim, including PX-6, is licensed or `GROUNDED`/`HELD`. Those outcomes must follow from applying the full rule to the source structure and then the existing settlement rules. The twin must reread the affected clauses before anything is built.

**3. R6's version-0 control.** Asked: "R6's control 'without an active log declaration' is a version-0 run, which could
have a measured witness. Your condition 1 says the configured witness covers the controls. Which should it be?" His
words:

> Other — keep the configured witness for the R6 row and its control; add the measured version-0 control as a separate row.
>
> The R6 comparison must isolate one variable: R6 versus no active log declaration. Both rows therefore use the same configured witness. Otherwise the comparison changes both the rule and the witness, making the result ambiguous.
>
> Record these distinctions:
>
> - R6 row and paired control: same configured witness; the only intended difference is R6.
> - Separate version-0 control: may use the arbiter’s own measured witness, clearly labelled as a distinct measurement—not as the paired R6 control.
> - Interpretation: configured agreement is not measured agreement, and neither establishes the reference’s version-1 arithmetic independently.
>
> This preserves condition 1 while allowing the measured version-0 result to provide additional evidence without confounding the R6 comparison.

**The definitions his first answer adopts**, verbatim from the packets. Each label's defining text is given; its verdicts
on the packets' worked laws (L1–L11), on the review's probes and its grade ("Within R6", "Interprets R6"), and D's "In
1a", "In 1b" and "Failures" lines, are the packets' consequences. His answer leaves them to be tested, not ruled: *"do
not automatically accept the claimed downstream conclusions."*

- **D**, packet A §4:
  > **D (preferred). Rule D10's court clause with a scope sentence: real readings stay REFERENCE-ONLY; R6's rows, the PREFIX row and their controls run in 1a with the configured witness.**
- **B1**, packet B §3.1:
  > **B1. The first port declaration of either kind, else the tick block.**
  > - PROPOSED WORDING: "the first top-level clause that is, or holds, a port declaration, or is the tick block".
- **4a**, packet B §3.2:
  > **4a. The boundary is the tick block** (the "or is the tick block" in B1's wording).
- **5c**, packet B §3.3:
  > **5c. Exempt exactly when the static test holds:** bullet 1, plus the closure in §3.4.
- **K1**, packet B §3.4:
  > **K1. `Reach`, with values ignored.**
  > - It follows every If arm and the Otherwise, every loop body, the tick block's body, and every Perform transitively.
  > - Its start set is the top-level clause that is or holds the boundary, plus every later top-level clause.
  > - A statement kind it does not know licenses no claim (fail closed).

**What they fix.** None of it is built:
- **The labels adopt their definitions; the conclusions drawn from them are not ruled.** A fixture's outcome, the twin's
  PX-6 included, follows only from applying the whole rule to its source structure, and then the settlement rules.
  Nothing records PX-6 as licensed.
- **The tick block has its own closure rule, which follows its body.** Unknown kinds fail closed.
- **The closure's rule table** (§15.12.4), under his four conditions: structural only, with values ignored; the
  no-addition kinds explicit (To, Define, Decimals, Let, Set, Increase, Decrease, Say, Append, Remove, Must, and a port
  declaration), which does not exempt their surrounding clauses from the boundary or the licensing test; any other kind
  licenses no claim of the law; and an unperformed To adds no body because the closure is source-structural, not
  because an execution skipped it.
- **Port declarations.** K1's definition leaves them unresolved; his second answer settles it: a port declaration adds
  no further reachable body. So the question his first answer would have had returned is answered by the table.
- **R6's row and its paired control share the configured witness**, R6 being their only intended difference. A separate
  version-0 control may use the arbiter's own measured witness, labelled as a distinct measurement and never as the
  paired control. Configured agreement is not measured agreement, and neither establishes the reference's version-1
  arithmetic.

**Its re-reads:** the A_r of these three rulings, in `twin-r7/AR-REREAD-2.md`.

### The table's Perform row (2026-10-27)

*Added 2026-10-27 by his answer to one question R7's second re-read raised (`twin-r7/REREAD-2-REPORT.md`, TABLE-1;
disposed in `twin-r7/REREAD-2-DISPOSITION.md`).* Asked: "The rule table's "Perform" row: is it SPEC §3's row
"`Perform <name>` or the name alone as a statement", so a bare procedure-name call is the Perform kind? SPEC §3 gives
both spellings one row, and the built parser makes the same Perform node for both (syntax.py lines 456 and 558)." His
answer, whole:

> Yes, the bare name is Perform (Recommended)

**What it fixes.** None of it is built. The closure's table's Perform row is SPEC §3's row, "`Perform <name>` or the
name alone as a statement": a call by the procedure's bare name adds the procedure's body, as Perform does. Nothing
else changes. **Its re-read:** with draft 4's changed clauses (`twin-r7/AR-REREAD-2.md`, its third set).

### Finding 6: read-once ports (2026-10-27)

*Added 2026-10-27 by his ruling. It is not one of R1–R12. It decides finding 6 of R7's review (`twin-r7/REPORT.md`),
from packet C (`packets/C-read-once-ports.md`) and the adversarial comparison he asked for
(`packets/F-read-once-adversary.md`), summarized in `RELEASE-DECISIONS.md` §2.*

**Ruled 2026-10-27: A′, as RO′-1 to RO′-6, with six conditions.** His words, whole:

> I rule for A′, as RO′-1 to RO′-6, with the stated limits.
> The prefix runs up to the first read-once declaration. If the required read-once value is missing, the run ends `NOT-RUN` there and names the first empty read-once port. Add the RO′-6 row to CUT-0 before its digest is pinned.
> Conditions of the ruling:
>
> 1. Whole-log validation remains mandatory. A malformed log is rejected before any statement executes. A well-formed log missing a required read-once value is a distinct case: the permitted prefix may execute, then stop at the declaration.
> 2. R6 remains unchanged. Do not weaken the law-fixed PREFIX claim-line invariant to accommodate design A.
> 3. CUT-0 must explicitly cover this stop point. RO′-6 must state the applicable premises and withholding behavior; do not assume the existing “rest of a block” row covers it without checking.
> 4. N2 and N3 remain open for the A2 row. This ruling does not settle their behavior.
> 5. Finding 8 must define a loadable representation for read-once `NOT-RUN` logs. Byte forms remain open.
> 6. No implementation or build before the affected-clause set is computed and the twin rereads the affected clauses under R7.
>
> This settles the design choice, not the remaining byte format, session-event semantics, finding 8, or CUT-0's overall soundness.
> Next: record this ruling, update the decision sheet, and include finding 6's dependencies in the batched reread. The three-turn push target remains conditional on resolving the remaining release blockers and passing the final gate on the exact tree.

**The text he adopted**, packet F §6, verbatim:

> **RO′-1.** A read-once value reaches the session only as an arrival, judged by the door at once; a refused arrival is never assigned; a retry is a new arrival; neither ends the session.
> **RO′-2.** The read-once ports have one record, filled by assigning accepted arrivals, at most one per port, and closed once before any tick record; it is written whole or not at all. A law with no read-once port is unchanged.
> **RO′-3.** A read-once port binds where its declaration stands. A run executes the top-level clauses before the first read-once declaration whatever the log holds, provided the log loads. If the log holds the read-once record, the run goes on. If it does not, the run stops before the first read-once declaration: NOT-RUN naming the read-once port the end record names (the first empty one in declaration order, checked against the history), or LOG-OPEN if the log has no end record. No `'N'` is emitted, and no value is invented, held over, defaulted or bound from another read-once port.
> **RO′-4.** A refusal before that declaration is REFUSED, whatever the log holds.
> **RO′-5.** That stop is a case of NOT-RUN or LOG-OPEN, not a fifth status. COMPLETED never stands for a law with a read-once port whose log lacks the record.
> **RO′-6 [pinned].** At that stop the cut is the first read-once declaration, a top-level frame not begun; K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored. The NOT-RUN t / LOG-OPEN row applies only when the record is present or no read-once port is declared.

**What it fixes.** None of it is built:
- **A read-once port binds where its declaration stands** (RO′-3). Until now that was contract draft 0's proposal under
  an R5 tag; it is ruled.
- **The run** executes the top-level clauses before the first read-once declaration, whatever the log holds, provided
  the log loads. If the log lacks the read-once record, the run stops before the first read-once declaration, even when
  the missing value belongs to a later port: NOT-RUN naming the first empty read-once port, or LOG-OPEN with no end
  record. No `'N'` is emitted, and no value is invented, held over, defaulted or bound from another port.
- **Whole-log validation stays mandatory** (his condition 1). A malformed log runs nothing; a well-formed log without
  the read-once record is the distinct case above.
- **R6 is unchanged** (his condition 2): a licensed claim's whole claim line stays fixed by the law.
- **CUT-0 gains RO′-6 before its digest is pinned**, stating its premises and its withholding (his condition 3). The
  premises are those the adversary checked: binding has no effect beyond binding (it counts no operation, emits only
  `'N'`, and cannot refuse); read-once ports are declared at the top level, each evaluated once; values are unknown, as
  in reading S2. K̂ was checked equal to the rest of the block on version-0 stand-ins only (MEASURED there); for version
  1 it is DECLARED.
- **N2 and N3 stay open for the A2 row** (his condition 4).
- **Finding 8 must give a read-once NOT-RUN log a form that loads** (his condition 5). Byte forms stay open.
- **Nothing is built before the affected clauses are re-read** (his condition 6).

**What stays open**, in his words: "the remaining byte format, session-event semantics, finding 8, or CUT-0's overall
soundness".

**Its re-reads:** its A_r, in `twin-r7/AR-F6.md`.

### The release: its scope, and the seven first-form outputs (2026-10-27)

*Added 2026-10-27 by his ruling on the decision sheet `RELEASE-DECISIONS.md` (§1, the scope; §6, the line ends).* His
words, whole:

> I rule for the narrow release scope and preserving the seven historical adversary outputs byte-for-byte as captured.
> 1. Release scope
> Proceed with the planned five-commit release, limited to the already partitioned 142 files. Do not expand into unrelated refactors or reopen settled rulings.
> The scope restriction does not waive any normative release blocker. Before the final gate:
>
> * Finish and dispose R7 re-read 3.
> * Resolve the remaining release decisions that affect the candidate.
> * Keep N2, N3, the read-once `NOT-RUN` byte form, and other explicitly open questions from being silently treated as settled.
> * Run the gate against the exact final tree.
>
> If an unresolved question changes version-1 behavior or makes the candidate's specification internally inconsistent, stop and bring that question back rather than hiding it inside the narrow scope.
> 2. Historical adversary output line endings
> Preserve the seven original outputs byte-for-byte as captured. Do not normalize their line endings merely because `.gitattributes` currently specifies `text=auto eol=lf`.
> Use a narrowly scoped `.gitattributes` exception for those seven historical output files, such as `-text` on their matching paths, provided the exact patterns cover only those files. Keep the current rerun outputs under their existing normalization policy unless a separate decision requires otherwise.
> Verify this with a byte-level comparison after staging and again before pushing. The historical records and current reruns serve different evidentiary purposes; preserving the originals prevents a repository policy from silently rewriting the captured evidence.
> 3. Sequence
>
> 1. Finish re-read 3 and resolve its findings.
> 2. Apply the narrow scope and line-ending decision.
> 3. Recheck the 142-file, five-commit partition and privacy scan.
> 4. Run the final gate on the exact candidate tree.
> 5. Inspect staged bytes, commit boundaries, and outgoing history.
> 6. Commit and push only if every required gate passes.
>
> The three-turn target remains a target, not permission to skip a gate. Nothing is authorized to be committed or pushed until the exact final tree passes.

**What it fixes.** Nothing is built, committed or pushed by it:
- **The narrow scope** of `RELEASE-DECISIONS.md` §1. Finding 6 is ruled. Finding 8 is deferred to the amended set's
  "identity and bytes" row, with packet D as its record and finding 6's condition 5 (a loadable form for a read-once
  NOT-RUN log) as a constraint on it. The amended set's 13 remaining rows are each deferred to a ruling before 1a's
  build, with the disposition §4 gives it. The format freeze is deferred to `CUT-SCHEMA.md` P6's trigger. None of
  these is decided by being deferred; N2, N3 and every byte form stay open.
- **The seven first-form outputs** keep their captured bytes: `.gitattributes` gains one `-text` line for each of their
  seven exact paths, and no pattern that reaches any other file. The six current reruns keep the repository's
  normalization.
- **Files beyond the 142.** His sequence itself makes three: `.gitattributes` (his point 2), and re-read 3's report and
  its disposition (his point 3, step 1). Any other file is outside his scope and is not added.
  *Added the same day: his three answers below, on re-read 3's questions, add the files they call for: draft 6 and its
  changes record, the A_r of these answers, and re-read 4's brief, report and disposition with its T10 statements.
  And after re-read 4, the A_r of his three answers on it, `twin-r7/AR-REREAD-5.md`.*

### The read-once stop's row, its version-1 check, and the last re-read (2026-10-27)

*Added 2026-10-27 by his answers to three questions R7's third re-read raised (`twin-r7/REREAD-3-REPORT.md`, F6-1 and
F6-14; disposed in `twin-r7/REREAD-3-DISPOSITION.md`) and to how the re-reads converge before the push. Each question
is given as it was put to him, then his answer, whole and unchanged.*

**1. The stop's row.** Asked: "F6-1: when the read-once stop withholds a claim, which row does the withholding name?
The claims ruling requires the responsible structural row, and your condition 3 says not to assume 'the rest of a
block' covers the stop." His words:

> 1. F6-1 — The read-once stop’s withholding row
>
> Adopt “Its own row.” Name it “the read-once stop” in §15.13.9’s row list. Compute its \(\hat K\) as RO′-6 specifies: the rest of the block from the first read-once declaration. Do not attribute this withholding to the existing “rest of a block” row or imply that row covers a frame that never began. This preserves the requirement that each withholding identify its responsible structural row.

**2. The version-1 check.** Asked: "F6-14: RO′-6's K̂ was checked equal to the rest of the block on version-0 stand-ins
only; for version 1 it is DECLARED. Is that enough for now?" His words:

> 2. F6-14 — Is the version-0 check enough for now?
>
> Adopt “Enough now; check before the pin.” Keep the evidence grades explicit: MEASURED on version-0 stand-ins; DECLARED for version 1. Record a version-1 check of RO′-6 as owed before CUT-0’s digest is pinned. This is a deferral, not evidence that version 1 satisfies the equality. It does not close the format-freeze question or authorize pinning before the check.

**3. How the re-reads converge before the push.** Asked: "How do re-reads converge before the push? Each re-read has
found drafting fixes, and each fix needs reading again before the build." His words:

> 3. Re-read convergence before the push
>
> Adopt “One more re-read, then gate.” Draft 6 should apply the dispositions from re-read 3 and these rulings. The twin then re-reads the clauses changed by draft 6 and the clauses affected by these rulings once. Any further drafting fixes must be recorded with their required re-read before the build, as R7 requires. Any issue needing your decision comes back to you; do not silently resolve it. Do not loop indefinitely merely to obtain a clean report, but do not waive a required re-read or build gate either.

**What they fix.** None of it is built:
- **The read-once stop is a row of its own**, named "the read-once stop" in 15.13.9's list. Its K̂ is RO′-6's: the rest
  of the block from the first read-once declaration. No withholding at the stop is attributed to "the rest of a block".
- **The evidence stays graded as it is:** MEASURED on version-0 stand-ins, DECLARED for version 1. A version-1 check of
  RO′-6 is owed before CUT-0's digest is pinned. That is a deferral, not evidence; it neither closes the format freeze
  nor authorizes a pin before the check.
- **One more re-read, then the gate.** Draft 6 applies re-read 3's dispositions and these answers. The twin re-reads
  once the clauses draft 6 changes and the clauses these answers affect. A drafting fix found then is applied and
  recorded with its re-read owed before the build. A question needing his decision comes back to him.

**Its re-reads:** the A_r of these answers, in `twin-r7/AR-REREAD-4.md`.

### The stop's carrier, the owed check, and the order of work (2026-10-27)

*Added 2026-10-27 by his answers to three questions R7's fourth re-read raised (`twin-r7/REREAD-4-REPORT.md`,
STOPROW-1, V1CHECK-2, V1CHECK-3; disposed in `twin-r7/REREAD-4-DISPOSITION.md`). Each question is given as it was put
to him, then his answer, whole and unchanged. The third answer arrived beginning ". V1CHECK-3"; it is kept so.*

**1. The carrier.** Asked: "STOPROW-1: a header-only log and a log holding the read-once record can both end LOG-OPEN
with no tick run, yet only the first takes the read-once stop's row. What tells the court the record was absent?" His
words:

> 1. STOPROW-1 — How does the court know the read-once record was absent?
>
> Adopt “The receipt’s status.” The read-once stop must have an explicit receipt status that distinguishes a stop caused by the absent record from a LOG-OPEN run in which the read-once record exists but no tick ran. The exact receipt bytes and status encoding remain for Finding 8; do not invent them now. The court selects the responsible row from the receipt, not by inspecting the log or inferring absence from trace events. This preserves R6’s rule that the log is data, never a channel, and avoids making the row depend on an unruled inference about whether an N event must exist.

**2. The owed check.** Asked: "V1CHECK-2: what must the owed version-1 check of RO′-6 compare? In version 1 K̂ is
defined as the rest of the block, so 'K̂ equals the rest of the block' holds by definition." His words:

> 2. V1CHECK-2 — What must the version-1 check compare?
>
> Adopt “Containment.” The owed check is whether every claim that the same law evaluates after the read-once stop, over any log that supplies the required record, lies within \(\hat K\). It passes only if no such claim falls outside \(\hat K\). Do not require precision as part of this check: because the closure is structural and ignores runtime values, \(\hat K\) may include claims that a particular continuation cannot evaluate. Record the check as a version-1 obligation, not as a result already established by the definition of \(\hat K\).

**3. The order of work.** Asked: "V1CHECK-3: the claims ruling admits the meet 'pinned to the exact CUT-0 digest', and
the version-1 check is owed before the pin. May 1a's rows run against the proposed, unpinned CUT-0?" His words:

> . V1CHECK-3 — May 1a run rows against an unpinned CUT-0?
>
> Adopt “No: check, then pin, then 1a.” Complete the version-1 containment check first, pin the exact CUT-0 digest second, and only then run 1a’s rows against that pinned candidate. The claims ruling requires the meet to be pinned to the exact CUT-0 digest; labelling an unpinned proposal does not satisfy that condition. The check belongs on 1a’s build path, and real court readings still hold no claims before 1b. Do not build or run 1a against an unpinned CUT-0.

**What they fix.** None of it is built, and draft 6 is not changed by them: by his ruling on the last re-read, they are
stated in draft 7 and re-read before the build (`twin-r7/REREAD-4-DISPOSITION.md`).
- **The read-once stop has a receipt status of its own**, distinct from a LOG-OPEN run that holds the record. The court
  chooses the row from the receipt, never from the log or the trace. The bytes and the encoding are finding 8's.
- **The owed version-1 check is containment:** every claim the same law evaluates after the stop, over any log that
  supplies the record, lies in K̂; it passes only if none falls outside. Precision is not part of it. It is an obligation,
  not a result.
- **The order of work:** the version-1 containment check, then the pin of CUT-0's exact digest, then 1a's rows against
  that pinned candidate. Nothing of 1a is built or run against an unpinned CUT-0.

**Its re-reads:** the A_r of these answers, in `twin-r7/AR-REREAD-5.md`, owed before the build with draft 7.

### The containment test, findings 8 and 20 before the pin, and the push (2026-10-27)

*Added 2026-10-27 by his answers to the questions R7's fifth re-read raised (`twin-r7/REREAD-5-REPORT.md`, CONTAIN-2,
ORDER-1, ORDER-2, and CARRIER-1's confirmation; disposed in `twin-r7/REREAD-5-DISPOSITION.md`), and by his word on when
to push. Each question is given as it was put to him, then his answer, whole and unchanged. His `\\(\hat K\\)` is kept
as it arrived.*

**1. The containment check.** Asked: "Q1. What is the containment check, and what runs it before the pin? 1a holds the
version-1 reference. The check, if it runs anything, needs that reference, so 'nothing of 1a before the pin' could be
circular." The options put: (a) a test on fixtures, run by the version-1 reference built before the pin, with nothing
run against CUT-0 until it's pinned, a pass MEASURED on its fixtures only and T10.8 staying open; (b) a paper argument
over the closure as T10.8's proof obligation, running nothing, the reference waiting for the pin; (c) both.

**2. Findings 8 and 20.** Asked: "Q2. Where do findings 8 and 20 fall relative to the pin? Finding 8 is the encoding of
the stop's status. Finding 20 is whether `'R'` carries the cut. Draft 7 has CUT-0 choose the stop's row 'from the
receipt's status', so the rule being pinned depends on that encoding." The options put: (a) rule both before the pin,
so the digest names a rule whose inputs are fixed; (b) pin over abstract inputs, rule both before 1a's rows, and treat
any later change as a new pin.

**3. RO′-5.** Put for confirmation: "I've read your RO′-5 ('not a fifth status') as binding finding 8. On that reading
the stop stays a NOT-RUN or LOG-OPEN whose status marks it apart. If you meant a separate status word, that would revise
RO′-5, and only you can do that."

His words:

> Q1 — Adopt (a): a fixture-based containment test run by the version-1 reference before the pin.
>
> The test must check that every claim the same law evaluates after the read-once stop, over each tested log that supplies the required record, lies within \\(\hat K\\). Any claim outside \\(\hat K\\) falsifies containment. Run it against fixtures using the version-1 reference, without running any court rows against an unpinned CUT-0. Record the result as MEASURED on those fixtures only. It does not establish universal containment or close T10.8; the claims ruling remains in force that no test result or measurement alone closes T10.
>
> Q2 — Adopt (a): resolve Finding 8 and Finding 20 before pinning CUT-0.
>
> Both affect the rule being identified by the digest. Finding 8 must settle the receipt encoding that distinguishes the read-once stop, and Finding 20 must settle whether `R` carries the cut. Resolve and record both before pinning, so CUT-0’s digest identifies a rule with those inputs fixed. Then run 1a’s rows against that pinned rule. If either decision later changes the rule, treat it as a new CUT-0 candidate requiring a new digest and the applicable checks—not as a silent change under the old pin.
>
> RO′-5 confirmation: Your reading is correct. The read-once stop does not introduce a fifth status word. It remains `NOT-RUN` or `LOG-OPEN`, with an explicit distinguishing status form; Finding 8 must define its encoding. Do not revise RO′-5.
>
> These rulings authorize the next drafting step, not a build. Draft 8 should incorporate the eight owed fixes and these decisions, record the affected clauses, and undergo re-read 6. Keep the build gate closed until the remaining normative obligations are resolved and the required checks pass.

**4. The push.** His words, in the same message:

> Yes — push later. Keep `9de2792` as the published, gated baseline. Draft 7, draft 8, the re-reads, and the documentation changes remain uncommitted until the next release is ready.
> The sequence is:
>
> 1. Finish draft 8 and re-read 6; resolve any findings that need your decision.
> 2. Resolve Finding 8 and Finding 20 before pinning CUT-0.
> 3. Run the version-1 containment fixture test and record its limited evidence; do not treat it as closing T10.8.
> 4. Pin the exact CUT-0 digest, then run 1a against that pinned rule.
> 5. Resolve the remaining normative blockers and run the full gate on the exact final tree.
> 6. Verify the staged bytes, commit boundaries, privacy, and outgoing history; then push.
>
> The README and AGENTS changes can stay local alongside the specification work. No need to push them separately unless you explicitly decide to publish a documentation-only update.

**What they fix.** None of it is built; they authorize draft 8, not a build:
- **The containment check is a test** on fixtures, run by the version-1 reference before the pin. Any claim outside K̂
  falsifies it; a pass is MEASURED on those fixtures only. It establishes neither containment in general nor T10.8,
  and no court row runs against an unpinned CUT-0.
- **Findings 8 and 20 are resolved and recorded before the pin,** so the digest names a rule with those inputs fixed.
  A later change to either that changes the rule is a new CUT-0 candidate, with a new digest and its checks.
- **RO′-5 stands:** the stop is NOT-RUN or LOG-OPEN with an explicit distinguishing status form, never a fifth status
  word; finding 8 defines the form's encoding.
- **The order of work**, his six steps: draft 8 and re-read 6; findings 8 and 20; the containment test; the pin, then
  1a; the remaining blockers and the full gate on the exact final tree; the staged bytes, the commit boundaries,
  privacy and the outgoing history, then the push. Everything after 9de2792 stays uncommitted until that release.

**Its re-reads:** the A_r of these answers, in `twin-r7/AR-REREAD-6.md`, read with draft 8 by re-read 6 before the build.

### Every input the pinned rule reads, fixed before the pin (2026-10-27)

*Added 2026-10-27 by his answer to the question R7's sixth re-read raised (`twin-r7/REREAD-6-REPORT.md`, PIN-1 and
PIN-3; disposed in `twin-r7/REREAD-6-DISPOSITION.md`). The question is given as it was put to him, then his answer,
whole and unchanged.*

**The question.** Asked: "Which further inputs of the stop's row are fixed before the pin? Your Q2 reasoning was 'Both
affect the rule being identified by the digest', but it named only findings 8 and 20." Two more inputs were named: the
port place and counting (15.1.3, 15.7.1), on which the stop row's "a top-level frame" rests, both open; and the cut's
bytes in `'R'`, where CUT-SCHEMA puts the cut, with no record saying whether the pinned rule reads the cut from those
bytes or from the execution. The options put: (a) every input the pinned rule reads is fixed before the pin: port place
and counting, plus the cut's bytes if finding 20 puts the cut in `'R'` and the rule decodes it there, the general format
freeze keeping its own trigger; (b) only port place and counting before the pin, the cut's bytes staying with P6; (c)
pin with all three open, a later change making a new candidate with a new digest under his Q2 rule.

His words:

> Adopt (a): every input the pinned rule reads must be fixed before the pin.
> The stop row’s inputs must be settled before CUT-0 is pinned:
>
> * Port place and counting — resolve the open amended-set rows governing the top-level-frame boundary and counting rules. These determine where the stop row applies.
> * Finding 8 — settle the receipt’s explicit distinguishing status form and its encoding.
> * Finding 20 — settle whether `R` carries the cut.
> * Cut decoding — if Finding 20 places the cut in `R`, specify whether and how the pinned rule decodes it from those bytes. The court must not silently derive it from execution instead.
>
> The order is: resolve those inputs, complete the version-1 containment fixture test against the resulting candidate, pin that exact candidate’s digest, then run 1a’s rows against the pinned rule.
> Keep the general format-freeze trigger as its own obligation; this ruling does not silently settle P6.
> Reason: the digest should identify a rule whose inputs are fixed, not a rule whose interpretation may change after pinning. If a later ruling changes an input or the rule, it requires a new candidate and digest, with the applicable checks repeated.
> This settles the ordering question, not the underlying open rows themselves. They still require their own rulings and evidence before the build gate opens.

**What it fixes.** Nothing is built, and no open row is decided by it:
- **Every input the pinned rule reads is fixed before the pin:** the amended set's rows on the port place and on
  counting, finding 8 (the distinguishing status form and its encoding), finding 20 (whether `'R'` carries the cut),
  and, if the cut is in `'R'`, whether and how the pinned rule decodes it from those bytes. In his words, *"The court
  must not silently derive it from execution instead."*
- **The order of work:** those inputs resolved; the containment fixture test run against the candidate they give; that
  exact candidate's digest pinned; then 1a's rows against the pinned rule. A later change to an input or the rule is a
  new candidate and digest, with the applicable checks repeated.
- **P6 is not settled by it:** the general format freeze keeps its own trigger.
- **The rows themselves stay open,** each owed its own ruling and evidence before the build gate opens.

**Its re-reads:** the A_r of this answer, in `twin-r7/AR-REREAD-7.md`, read with draft 9 by re-read 7 before the build.

### The principle reaches every row of CUT-0 (2026-10-27)

*Added 2026-10-27 by his answer to the question R7's seventh re-read raised (`twin-r7/REREAD-7-REPORT.md`, INPUTS-2;
disposed in `twin-r7/REREAD-7-DISPOSITION.md`). He gives it as a clarification of his principle of the same day, "Every
input the pinned rule reads, fixed before the pin", above. The question is given as it was put to him, then his answer,
whole and unchanged.*

**The question.** Asked: "Does 'every input the pinned rule reads' reach CUT-0's other rows too? You gave a principle
('every input the pinned rule reads must be fixed before the pin') and then listed 'The stop row's inputs'. CUT-0's
other rows read two more open things": the version-1 statuses' encoding, by which the NOT-RUN/LOG-OPEN row picks
itself, under "identity and bytes" with no timing against the pin; and the statement kinds R2's spellings add, which
CUT-0's reach has to cover, R2 being open. The options put: (a) the principle reaches every row, so both are fixed
before the pin, and the containment test's record lists every input the candidate reads, checked against the candidate
rather than drawn up by hand, at the cost of ruling R2 before the pin; (b) only the stop row's inputs before the pin,
the others before 1a's build, a later change making a new candidate and digest.

His words:

> Adopt (a): yes. “Every input the pinned rule reads” applies to every CUT-0 row, not just the read-once stop row.
> Before pinning CUT-0:
>
> * Fix the version-1 `NOT-RUN`/`LOG-OPEN` status encoding that determines which row applies.
> * Resolve R2’s statement-kind spellings and reach rules so CUT-0’s structural closure is defined across every supported statement kind.
> * Keep the previously ruled stop-row inputs, Finding 8, Finding 20, and cut decoding in the same pre-pin requirement.
> * Have the containment-test record enumerate the inputs the candidate actually reads. Check that list against the candidate, rather than constructing it by hand.
>
> Reason: the governing principle is general. If a row’s interpretation depends on an unresolved input, the pinned digest does not yet identify a fully fixed rule. The same discipline must apply to every row, or a later decision could change the rule while leaving its apparent pin unchanged.
> This brings R2 forward: it must be ruled before the pin, not merely before 1a’s build. P6 retains its own trigger. If any later ruling changes CUT-0’s rule or inputs, create a new candidate, compute a new digest, and repeat the applicable checks.
> Record this as a clarification of the existing principle, not as a claim that the newly identified encodings or statement-kind rules are already settled. Draft 10 and re-read 8 can proceed; the build gate remains closed until those obligations are satisfied.

**What it fixes,** as a clarification of the principle above, and settling none of the rows it names:
- **The principle reaches every row of CUT-0,** not only the read-once stop's. Before the pin, besides the stop row's
  inputs, finding 8, finding 20 and the cut's decoding: the version-1 NOT-RUN/LOG-OPEN status encoding by which a row
  is chosen, and R2's statement-kind spellings and reach rules, so that CUT-0's closure is defined across every
  supported statement kind.
- **R2 is ruled before the pin,** not only before 1a's build.
- **The containment test's record enumerates the inputs the candidate actually reads,** and the list is checked
  against the candidate, not drawn up by hand.
- **P6 keeps its own trigger.** A later ruling that changes CUT-0's rule or inputs makes a new candidate, a new digest,
  and the applicable checks repeated.
- **Nothing it names is settled by it:** the encodings and the statement-kind rules stay open, each owed its ruling.

**Its re-reads:** the A_r of this answer, in `twin-r7/AR-REREAD-8.md`, read with draft 10 by re-read 8 before the build.

### Finding 8: the read-once stop's status form (8.1 and 8.2) (2026-10-28)

*Added 2026-10-28. The questions were packet G's (`packets/G-stop-status.md` §3, 8.1 and 8.2). A reviewer's text
proposed a ruling; he adopted it as his ruling on 8.1 and 8.2 "exactly as proposed". Below: the proposal, whole and
unchanged; his own words adopting it; and the note he pasted with them, whole and unchanged.*

**The questions.** 8.1: which status form marks the read-once stop: (a) the keyword `READ-ONCE` in the second token
place, (b) t = 0, or (c) a separate receipt line. 8.2: the stop's NOT-RUN t (under (a), none).

**The proposal he adopted:**

> Rule 8.1(a): use the explicit `READ-ONCE` keyword in the second token position.
>
> * `status NOT-RUN READ-ONCE INPUT-MISSING <port>`
> * `status LOG-OPEN READ-ONCE`
>
> The distinguishing token must identify the read-once stop without inventing a tick number or conflating it with an ordinary open run. The stop precedes any tick, so its `NOT-RUN` status has no \(t\) value under 8.2.
> Keep the ruling narrow: 8.1(a) does not decide 8.3–8.6. In particular, the loadable end-record encoding, malformed record-less log cases, and tick-case `NOT-RUN`/`LOG-OPEN` encoding remain separate decisions. The read-once `NOT-RUN` log must still satisfy the previously fixed loadability condition.
> This is the proposed ruling for you to adopt, not a claim that `RULINGS.md` has been changed. Nothing should be pinned or committed until the ruling is recorded and the downstream checks pass.

**His words:**

> Yes, adopt it as my ruling on 8.1 and 8.2, exactly as proposed.
>
> Leave 8.3–8.6 open. Nothing is pinned or committed.

**The note he pasted with them:**

> “Open” means undecided—not settled by this ruling.
> Your ruling settles only:
>
> * 8.1: The read-once stop uses the explicit `READ-ONCE` keyword in the second token position.
> * 8.2: The stop’s `NOT-RUN` status carries no \(t\) value.
>
> The remaining decisions are still pending:
>
> * 8.3: The exact loadable end-record format for a read-once `NOT-RUN` log.
> * 8.4: The exact bytes for a header-only log that is already classified as `LOG-OPEN`.
> * 8.5: Which other record-less log forms are malformed, including the unresolved read-once record format.
> * 8.6: The encoding of tick-case `NOT-RUN` and `LOG-OPEN` statuses.
>
> Open does not mean optional or waived. Those questions still need explicit rulings before the specification can be finalized. Existing constraints—including that the read-once `NOT-RUN` log must load—remain binding.
> Nothing about 8.3–8.6 is authorized by your 8.1–8.2 ruling, and nothing is pinned or committed.

**What it fixes,** and nothing more:
- **8.1:** the read-once stop's status is `status NOT-RUN READ-ONCE INPUT-MISSING <port>` or `status LOG-OPEN
  READ-ONCE`: the keyword `READ-ONCE` in the second token place.
- **8.2:** the stop's NOT-RUN carries no t.
- **Open, and not waived:** 8.3 (the loadable end record of a read-once NOT-RUN log), 8.4 (the header-only log's
  bytes), 8.5 (which other record-less logs are malformed, the read-once record's own line included) and 8.6 (the
  tick-case NOT-RUN and LOG-OPEN encoding). Condition 5 still binds: the read-once NOT-RUN log must load. Finding 8's
  other parts (packet D) stay open too.
- Nothing is pinned, built or committed by it.

**Its re-reads:** stated in draft 11 with re-read 8's fixes and re-read whole before the build; its affected clauses
are computed by `ar_compute.py` before that re-read.

### Finding 8: the read-once NOT-RUN log's end record (8.3) (2026-10-28)

*Added 2026-10-28. The question was packet G's (`packets/G-stop-status.md` §3, 8.3), as put to him in the session. His answer, whole and unchanged.*

**The question.** Which end record a read-once NOT-RUN log carries, and when it loads: (a1) `end 0 not-run read-once INPUT-MISSING <port>`, (a2) the same with `READ-ONCE`, (b) `end 0 not-run 0 INPUT-MISSING <port>`, (c) `end 0 not-run 1 INPUT-MISSING <port>`.

**His words:**

> I adopt 8.3(a1):
>
> `end 0 not-run read-once INPUT-MISSING <port>`
>
> The end record uses lowercase `read-once`, consistent with the log’s lowercase keywords, while retaining the uppercase `INPUT-MISSING` cause code.
>
> The record loads only when all four stated conditions hold: the law declares at least one read-once port; the log contains no read-once record; the log contains no tick record and \\(n=0\\); and the named port is a read-once port of that law. The verifier, not the loader, determines whether it is the first empty read-once port in declaration order.
>
> The record maps exactly to the already-ruled receipt status:
>
> `status NOT-RUN READ-ONCE INPUT-MISSING <port>`
>
> The corresponding `input-log-sha256` coverage remains unchanged. The chain’s `in_0` uses the header without a read-once record in this case, and §15.5 must say “with the read-once record, when present.”
>
> Still open: the LOG-\* refusal codes and check ordering, whether refusal writes a receipt, and the tick-case encoding under 8.6. This ruling does not settle those questions.
>
> Only 8.3(a1) is adopted. Nothing is pinned or committed.

**What it fixes,** and nothing more:
- **8.3 (a1):** the end record is `end 0 not-run read-once INPUT-MISSING <port>`. It loads only when the law declares a read-once port, the log holds no read-once record and no tick record (n = 0), and the port is a read-once port of the law; whether it is the first empty one is the verifier's.
- It maps exactly to `status NOT-RUN READ-ONCE INPUT-MISSING <port>`. `input-log-sha256` is unchanged; in_0 is taken over the header without a read-once record here, and 15.5 says "with the read-once record, when present".
- **Open:** the LOG-* codes and their order, whether a load refusal writes a receipt (packet D), and 8.4 to 8.6. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Finding 8: the header-only log's bytes (8.4) (2026-10-28)

*Added 2026-10-28. The question was packet G's (`packets/G-stop-status.md` §3, 8.4), as put to him in the session. His answer, whole and unchanged.*

**The question.** For a law that declares a read-once port, the exact bytes of the log that holds only its header: (a) the three LF-terminated header lines and nothing after them; (b) the header and a marker line such as `open read-once`.

**His words:**

> I adopt 8.4(a): the header-only log consists of exactly the three LF-terminated header lines—
>
> ```
> orlog-inputs 0
> ports <sha256>
> door <version>
> ```
>
> —with nothing after them.
> No `open read-once` marker or other additional line is permitted.
> For a law declaring a read-once port, this header-only log produces `status LOG-OPEN READ-ONCE`, `ticks 0`, and no `'N'` or `'T'` in the trace. For a law without a read-once port, it produces plain `status LOG-OPEN`. If the read-once record is present and there are no ticks, the status is also plain `status LOG-OPEN`.
> The existing prefix-loadability requirement remains in force. This ruling does not decide damaged-header handling or refusal codes.
> Only 8.4(a) is adopted. Nothing is pinned or committed.

**What it fixes,** and nothing more:
- **8.4 (a):** the header-only log is exactly the three LF-terminated lines `orlog-inputs 0`, `ports <sha256>`, `door <version>`, with nothing after them; no marker or other line.
- For a law declaring a read-once port it gives `status LOG-OPEN READ-ONCE`, `ticks 0`, and no `'N'` or `'T'`; for a law without one, plain `status LOG-OPEN`; with the record present and no tick, plain `status LOG-OPEN`. Every prefix of a log still loads.
- **Open:** a damaged header and the refusal codes (packet D), and 8.5 and 8.6. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Finding 8: the malformed record-less logs (8.5) (2026-10-28)

*Added 2026-10-28. The question was packet G's (`packets/G-stop-status.md` §3, 8.5), as put to him in the session. His answer, whole and unchanged.*

**The question.** For a law that declares a read-once port, whether every log lacking the read-once record other than the header alone (8.4) and the header with 8.3's end record is refused at load: (a) a closed list, refusing M1 (a tick record), M2 (`end 0 closed`), M3 (a tick NOT-RUN naming an each-tick port) and M4 (8.3's form naming an each-tick port); (b) some such logs load.

**His words:**

> I adopt 8.5(a): the closed list.
> For a law declaring at least one read-once port, with no read-once record in the log, the only two forms permitted to load are:
>
> 1. The three-line header alone, as ruled in 8.4.
> 2. The header followed by `end 0 not-run read-once INPUT-MISSING <port>`, subject to the conditions ruled in 8.3.
>
> Every other log lacking the read-once record is malformed and must be refused at load, before any statement runs. This includes M1–M4. For a law with no read-once port, a `not-run read-once` end record is refused.
> This ruling does not settle the read-once record's own line, its keyword, or its value list. Those remain open and must be resolved separately if needed. Packet D's refusal codes, check ordering, and refusal-receipt behavior also remain open.
> Only 8.5(a) is adopted. Nothing is pinned or committed.

**What it fixes,** and nothing more:
- **8.5 (a):** for a law declaring a read-once port, with no read-once record in the log, only the header alone (8.4) and the header with `end 0 not-run read-once INPUT-MISSING <port>` under 8.3's conditions load. Every other such log, M1 to M4 included, is malformed and refused at load, before any statement runs. For a law with no read-once port, a `not-run read-once` end record is refused.
- **Open:** the read-once record's own line, its keyword and its value list; packet D's codes, their order and the refusal receipt; and 8.6. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Finding 8: the tick case's NOT-RUN and LOG-OPEN (8.6) (2026-10-28)

*Added 2026-10-28. The question was packet G's (`packets/G-stop-status.md` §3, 8.6), as put to him in the session. His answer, whole and unchanged.*

**The question.** The exact bytes of a tick's NOT-RUN status and of an ordinary LOG-OPEN status, and the t the status copies from the end record: (a) `status NOT-RUN <t> INPUT-MISSING <port>`, bare `status LOG-OPEN`, the end record `end <n> not-run <t> INPUT-MISSING <port>`, t = n+1 in decimal with no leading zero, the port an each-tick port's name; (b) a registered cause set; (c) `LOG-OPEN <n>`; (d) the port by its variable number.

**His words:**

> I adopt 8.6(a).
> The exact tick-case status forms are:
>
> * Tick `NOT-RUN`: `status NOT-RUN <t> INPUT-MISSING <port>`
> * Ordinary `LOG-OPEN`: `status LOG-OPEN`
> * Tick `NOT-RUN` end record: `end <n> not-run <t> INPUT-MISSING <port>`
>
> The following rules are part of this ruling:
>
> 1. \(t=n+1\), where \(n\) is the number of tick records in the log.
> 2. \(t\) is decimal ASCII without leading zeros.
> 3. `<port>` names an each-tick port declared by the law.
> 4. A law with no each-tick port cannot produce a tick `NOT-RUN`.
> 5. Tokens are separated by exactly one space.
> 6. The receipt's tick value must match the end record's tick value.
>
> CUT-0 selects its row using the status's second token: a decimal number means tick `NOT-RUN`; `READ-ONCE` means the read-once stop; and the absence of a second token means ordinary `LOG-OPEN`.
> Options (b), (c), and (d) are not adopted.
> Still open: the read-once record's own line, including its keyword, value list, and when it is written; and packet D's refusal codes, check ordering, and whether a load refusal writes a receipt.
> Record only this ruling. Nothing is pinned or committed.

**What it fixes,** and nothing more:
- **8.6 (a):** a tick's NOT-RUN is `status NOT-RUN <t> INPUT-MISSING <port>`, an ordinary open run `status LOG-OPEN`, and the tick NOT-RUN's end record `end <n> not-run <t> INPUT-MISSING <port>`; t = n+1, decimal ASCII without leading zeros; the port an each-tick port of the law; no tick NOT-RUN without an each-tick port; one space between tokens; the receipt's t equal to the end record's. (b), (c) and (d) are not adopted.
- CUT-0 chooses its row by the status's second token: a decimal number, the tick's NOT-RUN; `READ-ONCE`, the read-once stop; none, the ordinary LOG-OPEN.
- It settles, for the tick case, packet D's proposals of t = n+1 and of no tick NOT-RUN without an each-tick port (`packets/D-LOG-refusals.md` §4.5).
- **Open:** the read-once record's own line (its keyword, value list and when it is written); packet D's codes, their order and the refusal receipt. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Finding 8: the read-once record's line (8.5's dependency) (2026-10-28)

*Added 2026-10-28. The question was packet G's (`packets/G-stop-status.md` §3, 8.5's dependency), as put to him in the session. His answer, whole and unchanged.*

**The question.** The read-once record's line in the input log, its values, and when it is present: (a) `once <v1> <v2> …`, written only when the law declares a read-once port; (b) `t 0 <v1> <v2> …`; (c) `once …` written always.

**His words:**

> I adopt option (a) for the read-once record's own line.
> The line is:
> `once <v1> <v2> …`
> The ruling fixes these requirements:
>
> 1. Presence: Write the line only when the law declares at least one read-once port. A law with no read-once ports remains byte-for-byte unchanged.
> 2. Position: The line immediately follows the three-line header, before any tick record. It is the fourth line.
> 3. Values: Include exactly one value per read-once port, in declaration order. The record is complete or absent; partial records are invalid.
> 4. Encoding: Use the RUNTIME-SPEC §5 value encoding, represented as lowercase hexadecimal with one space between tokens. Whether values carry type tags remains subject to the separate typed-values ruling.
> 5. Chain: Include the line in `in_0` when present. It is not a tick-chain link, and it does not increment the tick count.
> 6. Malformed forms: Refuse `t 0`, a `once` line for a law without read-once ports, a misplaced or duplicate `once` line, and a line with the wrong number of values.
>
> The existing requirements remain in force: read-once `'N'` events precede the first tick's `'T'` event, version 0 remains untouched, and existing logs for laws without read-once ports remain byte-identical.
> Still open: packet D's refusal codes, check ordering, and whether a load refusal writes a receipt. The typed-values question also remains unresolved and is not decided here.
> Record this ruling as adopted. Nothing is pinned or committed.

**What it fixes,** and nothing more:
- **The read-once record's line (a):** `once <v1> <v2> …`, written only when the law declares a read-once port, as the fourth line, straight after the header and before any tick record; one value per read-once port in declaration order, whole or absent; each value in RUNTIME-SPEC §5's encoding as lowercase hex, one space between tokens; in in_0 when present, never a tick-chain link, never counted in n.
- Refused: `t 0`, a `once` line in a law with no read-once port, a misplaced or duplicate `once` line, and a wrong number of values. A law with no read-once port is byte for byte unchanged; read-once `'N'` events precede the first `'T'`; version 0 is untouched.
- **Open:** packet D's codes, their order and the refusal receipt; whether values carry type tags (the typed-values ruling). Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Finding 8: packet D's D1.a, the read-once record's faults take the existing codes (2026-10-28)

*Added 2026-10-28. The question was packet D's (`packets/D-LOG-refusals.md`, D1), as put to him in the session. He adopted D1.a to D1.d in one message as four separate rulings; this section quotes his opening line, his line for D1.a, and his closing line, each unchanged.*

**The question.** Which codes the read-once record's faults take: (i) the existing nine LOG-* codes, as in the table put to him (a `once` line's faults, and M1, LOG-RECORD; `t 0`, LOG-TICK; M2 to M4 and 8.3's conditions, LOG-END); (ii) a new code, LOG-ONCE.

**His words:**

> I adopt D1.a–D1.d, option (i) for each, as four separate rulings.
>
> * D1.a(i): Read-once record faults use the existing nine LOG-* codes. No `LOG-ONCE` code is added.
>
> Record each ruling separately in `RULINGS.md`. D2, D3, and typed values remain open. Nothing is pinned or committed.

**What it fixes,** and nothing more: The read-once record's faults take the existing nine LOG-* codes; no LOG-ONCE is added. The per-case codes of the table put to him go into draft 11 as that table states them, and the twin re-reads them there. Open: D2 (the order of checks), D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D1.b, what counts as not ASCII (2026-10-28)

*Added 2026-10-28. The question was packet D's (`packets/D-LOG-refusals.md`, D1), as put to him in the session. He adopted D1.a to D1.d in one message as four separate rulings; this section quotes his opening line, his line for D1.b, and his closing line, each unchanged.*

**The question.** What LOG-NOT-ASCII covers: (i) a byte above 0x7F, as the research model does; (ii) any byte outside 0x20–0x7E other than LF.

**His words:**

> I adopt D1.a–D1.d, option (i) for each, as four separate rulings.
>
> * D1.b(i): `LOG-NOT-ASCII` applies to bytes above `0x7F`. CR is handled by `LOG-LINE`.
>
> Record each ruling separately in `RULINGS.md`. D2, D3, and typed values remain open. Nothing is pinned or committed.

**What it fixes,** and nothing more: LOG-NOT-ASCII is a byte above 0x7F. A CR is LOG-LINE. Open: D2 (the order of checks), D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D1.c, a leading LF (2026-10-28)

*Added 2026-10-28. The question was packet D's (`packets/D-LOG-refusals.md`, D1), as put to him in the session. He adopted D1.a to D1.d in one message as four separate rulings; this section quotes his opening line, his line for D1.c, and his closing line, each unchanged.*

**The question.** Which code a log beginning with LF takes: (i) LOG-LINE, an empty line wherever it falls; (ii) LOG-HEADER, as the research model does.

**His words:**

> I adopt D1.a–D1.d, option (i) for each, as four separate rulings.
>
> * D1.c(i): A leading LF is `LOG-LINE`.
>
> Record each ruling separately in `RULINGS.md`. D2, D3, and typed values remain open. Nothing is pinned or committed.

**What it fixes,** and nothing more: A leading LF is LOG-LINE. Open: D2 (the order of checks), D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D1.d, a log offered with a version-0 law (2026-10-28)

*Added 2026-10-28. The question was packet D's (`packets/D-LOG-refusals.md`, D1), as put to him in the session. He adopted D1.a to D1.d in one message as four separate rulings; this section quotes his opening line, his line for D1.d, and his closing line, each unchanged.*

**The question.** What happens when an input log is offered with a version-0 law: (i) a usage error before load, outside the LOG-* codes; (ii) PORT-SIGNATURE.

**His words:**

> I adopt D1.a–D1.d, option (i) for each, as four separate rulings.
>
> * D1.d(i): An input log supplied with a version-0 law is a usage error outside the LOG-* codes.
>
> Record each ruling separately in `RULINGS.md`. D2, D3, and typed values remain open. Nothing is pinned or committed.

**What it fixes,** and nothing more: An input log offered with a version-0 law is a usage error, outside the LOG-* codes. Open: D2 (the order of checks), D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.1, compile first (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.1 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.1 | (a)    | Compile the law first. A compile fault prevents the log from being read. |
>
> D2.1 — Compile first. The law's validity is a prerequisite to interpreting its input log.

**What it fixes,** and nothing more: The law is compiled before its log is read; a compile fault means the log is never read. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.2, the whole-log order (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.2 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.2 | (a)    | NOT-ASCII → LINE → HEADER → PORT-SIGNATURE → records.                    |
>
> D2.2 — Whole-log precedence. The global checks precede record inspection. Header validation precedes digest comparison because the ports line must be structurally valid before its digest can be interpreted.

**What it fixes,** and nothing more: The whole-log checks run LOG-NOT-ASCII, LOG-LINE, LOG-HEADER, PORT-SIGNATURE, then the records from line 4. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.3, the earliest faulty line wins (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.3 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.3 | (a)    | The earliest faulty line wins, starting at line 4.                       |
>
> D2.3 — Earliest faulty line. This is the most useful diagnostic rule: a later fault cannot displace an earlier one. I reject phase-by-phase precedence.

**What it fixes,** and nothing more: From line 4 down, the first line with any fault decides the code; phase-by-phase precedence is rejected. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.4, the order within a line (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.4 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.4 | (a)    | Adopt the proposed within-line precedence.                               |
>
> D2.4 — Within-line precedence. Adopt:
>
> 1. LOG-AFTER-END
> 2. LOG-UNKNOWN
> 3. Read-once placement, LOG-RECORD
> 4. `once` content
> 5. `t` content
> 6. `end` conditions

**What it fixes,** and nothing more: Within a line: LOG-AFTER-END, then LOG-UNKNOWN, then the read-once placement (LOG-RECORD), then a `once` line's content, then a `t` line's content, then an `end` line's conditions. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.5, a tick record's fields (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.5 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.5 | (a)    | Value count → tick number → values.                                      |
>
> D2.5 — Tick records. Count precedes tick number, which precedes values. This deliberately makes E8 LOG-RECORD rather than LOG-TICK.

**What it fixes,** and nothing more: In a tick record: the value count, then the tick number, then the values. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2.6, the header's order (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D2). He adopted D2.1 to D2.6 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D2.6 and his reason for it, each unchanged.*

**The question.** Put to him in the session with the proposed order, the alternatives (phase by phase; the ports line first; fields in written order; the header in strict line order) and twelve overlapping-fault examples, E1 to E12.

**His words:**

> I adopt the recommended ordering for all six parts of D2, with the following scope and qualifications.
>
> | Part | Ruling | Decision                                                                 |
> | ---- | ------ | ------------------------------------------------------------------------ |
> | D2.6 | (a)    | Header order: line 1 → line count → line 3 → line 2 form.                |
>
> D2.6 — Header. Adopt the research model's ordering, including its line-reporting consequence.

**What it fixes,** and nothing more: In the header: line 1, then the line count, then line 3, then line 2's form; this decides only which line a refusal reports. It changes no code D1 assigns. Open: D3 (the refusal receipt) and the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D2, its twelve expected outcomes and compliance requirements (2026-10-29)

*Added 2026-10-29, from the same message: his adoption of E1 to E12's outcomes as put to him, and the compliance requirements he approved, each unchanged.*

**His words:**

> ## E1–E12
>
> I adopt the proposed expected outcomes for all twelve examples.
>
> In particular:
>
> - E3: LOG-HEADER at line 3.
> - E7: LOG-RECORD at line 4 (M1).
> - E8: LOG-RECORD.
> - E9: LOG-TICK.
> - E12: LOG-TICK at line 5.
>
> ## Compliance requirements
>
> I also approve the proposed compliance tests for 1a:
>
> - E1–E12 become individual fixtures.
> - Each adjacent precedence pair gets a swapped-order plant demonstrating that the ordering changes the result.
> - Repeated runs must produce identical code and line.
> - 1b must preserve those results across all four executions.
>
> These are implementation and verification requirements, not permission to change the classifications established by D1.
>
> Scope remains strictly limited to D2. D3 (load-refusal receipts) and typed values remain open. No pinning, committing, or additional rulings are authorized.
>
> You may record these six rulings separately in `RULINGS.md`, with the twelve expected outcomes and compliance requirements.

**What it fixes:** E1 to E12's outcomes, as put to him in the session (E1 LOG-NOT-ASCII; E2 LOG-LINE; E3 LOG-HEADER at line 3; E4 PORT-SIGNATURE; E5 LOG-UNKNOWN at line 5; E6 LOG-AFTER-END at line 7; E7 LOG-RECORD at line 4; E8 LOG-RECORD; E9 LOG-TICK; E10 LOG-RECORD at line 6; E11 the compile code; E12 LOG-TICK at line 5); and for 1a: each example a fixture, a swapped-order plant for each adjacent pair, the same code and line on repeated runs, and the same across the four executions in 1b. These verify D2 and change no D1 classification.

### Finding 8: packet D's D3.1, no receipt, a refusal witness (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D3). He adopted D3.1 to D3.5 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D3.1 and his reason for it, each unchanged.*

**The question.** Put to him in the session: D3.1 (N) no record, (W) a witness and no receipt, or (R) a receipt with a status; D3.2 to D3.5 as proposed under (W), D3.5 offering (a) the refusal's own exit or (b) the I/O-failure exit.

**His words:**

> I adopt (W): no receipt for a refused load; a separate witness records the refusal. I adopt the recommended provisions of D3.2 through D3.5, subject to the qualifications below.
>
> | Part | Ruling      | Decision                                                             |
> | ---- | ----------- | -------------------------------------------------------------------- |
> | D3.1 | (W)         | No receipt. Write a separate refusal witness.                        |
>
> D3.1 — Separate witness, not receipt.
>
> This preserves the four existing outcomes under 15.7.5. A refused load cannot produce an execution receipt because no statement ran.
>
> The witness is diagnostic evidence of the refusal, not an execution record.

**What it fixes,** and nothing more: A refused load writes no receipt; a separate refusal witness records it. The four outcomes of 15.7.5 are unchanged; the witness is diagnostic evidence, not an execution record. Open: the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D3.2, which refusals count (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D3). He adopted D3.1 to D3.5 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D3.2 and his reason for it, each unchanged.*

**The question.** Put to him in the session: D3.1 (N) no record, (W) a witness and no receipt, or (R) a receipt with a status; D3.2 to D3.5 as proposed under (W), D3.5 offering (a) the refusal's own exit or (b) the I/O-failure exit.

**His words:**

> I adopt (W): no receipt for a refused load; a separate witness records the refusal. I adopt the recommended provisions of D3.2 through D3.5, subject to the qualifications below.
>
> | Part | Ruling      | Decision                                                             |
> | ---- | ----------- | -------------------------------------------------------------------- |
> | D3.2 | As proposed | Exactly the nine LOG-\* refusals qualify.                            |
>
> D3.2 — Exactly nine refusal codes.
>
> The qualifying codes are:
>
> 1. LOG-NOT-ASCII
> 2. LOG-LINE
> 3. LOG-HEADER
> 4. PORT-SIGNATURE
> 5. LOG-RECORD
> 6. LOG-TICK
> 7. LOG-END
> 8. LOG-AFTER-END
> 9. LOG-UNKNOWN
>
> Compile refusals, version-0 usage errors, and log I/O failures are excluded. Loadable record-less forms remain successful loads.

**What it fixes,** and nothing more: Exactly the refusals carrying one of the nine LOG-* codes; not a compile refusal, a version-0 usage error or a log I/O failure. The two loadable record-less forms load. Open: the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D3.3, the witness written after the refusal is final (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D3). He adopted D3.1 to D3.5 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D3.3 and his reason for it, each unchanged.*

**The question.** Put to him in the session: D3.1 (N) no record, (W) a witness and no receipt, or (R) a receipt with a status; D3.2 to D3.5 as proposed under (W), D3.5 offering (a) the refusal's own exit or (b) the I/O-failure exit.

**His words:**

> I adopt (W): no receipt for a refused load; a separate witness records the refusal. I adopt the recommended provisions of D3.2 through D3.5, subject to the qualifications below.
>
> | Part | Ruling      | Decision                                                             |
> | ---- | ----------- | -------------------------------------------------------------------- |
> | D3.3 | As proposed | Write the witness only after the refusal code and line are final.    |
>
> D3.3 — Finalize before writing.
>
> The loader must settle the code and line under D1 and D2 before constructing the witness. Write through a temporary file and rename into place. No partial witness may stand.

**What it fixes,** and nothing more: The code and line are settled under D1 and D2 first; the witness is then written through a temporary file and renamed into place; no partial witness stands. Open: the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D3.4, the witness's contents and place (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D3). He adopted D3.1 to D3.5 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D3.4 and his reason for it, each unchanged.*

**The question.** Put to him in the session: D3.1 (N) no record, (W) a witness and no receipt, or (R) a receipt with a status; D3.2 to D3.5 as proposed under (W), D3.5 offering (a) the refusal's own exit or (b) the I/O-failure exit.

**His words:**

> I adopt (W): no receipt for a refused load; a separate witness records the refusal. I adopt the recommended provisions of D3.2 through D3.5, subject to the qualifications below.
>
> | Part | Ruling      | Decision                                                             |
> | ---- | ----------- | -------------------------------------------------------------------- |
> | D3.4 | As proposed | Adopt the specified deterministic witness format and destination.    |
>
> D3.4 — Witness contents.
>
> Adopt the proposed fields:
>
> ```
> orlog-load-refusal 0
> law-seal <the law's seal>
> code <CODE>
> line <n>
> log-bytes-sha256 <hex>
> end
> ```
>
> Requirements:
>
> - LF-terminated ASCII.
> - No timestamp or host-specific information.
> - One-based line number.
> - Whole-log line attribution as specified in the proposal.
> - SHA-256 covers every byte of the log as read.
> - The digest field must remain `log-bytes-sha256`, never `input-log-sha256`.
> - Human-readable diagnostics go to standard error.
>
> The witness belongs beside the normal receipt destination, under its own name. It is not a court receipt and is not consumed as an execution record.

**What it fixes,** and nothing more: The witness is the LF-terminated ASCII lines `orlog-load-refusal 0`, `law-seal`, `code`, `line` (1-based, the whole-log attribution as put to him), `log-bytes-sha256` (every byte as read, never named `input-log-sha256`) and `end`, with no timestamp or host detail; diagnostics on standard error; beside the receipt's place under its own name; not a court receipt. Open: the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D3.5, a failed witness write (2026-10-29)

*Added 2026-10-29. The question was packet D's (`packets/D-LOG-refusals.md`, D3). He adopted D3.1 to D3.5 in one message and said they may be recorded separately; this section quotes his opening line, his table's row for D3.5 and his reason for it, each unchanged.*

**The question.** Put to him in the session: D3.1 (N) no record, (W) a witness and no receipt, or (R) a receipt with a status; D3.2 to D3.5 as proposed under (W), D3.5 offering (a) the refusal's own exit or (b) the I/O-failure exit.

**His words:**

> I adopt (W): no receipt for a refused load; a separate witness records the refusal. I adopt the recommended provisions of D3.2 through D3.5, subject to the qualifications below.
>
> | Part | Ruling      | Decision                                                             |
> | ---- | ----------- | -------------------------------------------------------------------- |
> | D3.5 | (b)         | Witness-write failure produces the RUNTIME-SPEC §1 I/O-failure exit. |
>
> D3.5 — Witness-write failure: (b).
>
> A failed witness write must produce the RUNTIME-SPEC §1 I/O-failure exit, while preserving the original refusal's code and line on standard error.
>
> This prevents missing diagnostic evidence from being silently presented as an ordinary clean refusal.

**What it fixes,** and nothing more: A failed witness write gives RUNTIME-SPEC §1's I/O-failure exit, the refusal's code and line kept on standard error. Open: the typed-values question. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: packet D's D3, its compliance requirements (2026-10-29)

*Added 2026-10-29, from the same message: the compliance requirements he adopted, and his scope, each unchanged.*

**His words:**

> ## Compliance requirements
>
> I adopt all proposed 1a tests:
>
> - All nine codes: no receipt, exact witness code and line, correct full-log digest, exit 1.
> - Byte-identical witnesses on repeated runs.
> - No witnesses for compile refusals, version-0 usage errors, or unreadable logs.
> - Receipts and no witnesses for the two loadable record-less forms.
> - Write-failure test with no receipt or partial witness.
> - All five specified mutation plants must be detected.
>
> ## Scope
>
> D3 is now ruled. Typed values remain entirely open.
>
> No implementation changes, pinning, or commits are authorized by this ruling. You may record D3 as five separate rulings, plus its compliance requirements, in `RULINGS.md`.

**What it fixes:** for 1a, the tests put to him for D3: for each of the nine codes no receipt, the witness's exact code and line, its full-log digest, exit 1; byte-identical witnesses on repeated runs; no witness for a compile refusal, a version-0 usage error or an unreadable log; a receipt and no witness for the two loadable record-less forms; the write-failure test; and the five plants detected. D3 is ruled; typed values stay open.

### Finding 8: typed values, T1, the wire form, tagged (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T1 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T1   | (a)         | Full tagged encoding, lowercase hex.                                   |
>
> T1 — Wire representation: (a).
>
> Every value includes its tag byte. Examples adopted:
>
> | Value       | Required lowercase hex |
> | ----------- | ---------------------- |
> | Fixed 3     | `580000000000000003`   |
> | True        | `4201`                 |
> | Text `"hi"` | `54000000026869`       |
>
> The value bytes in the log must equal the value portion of the corresponding `'N'` event payload.
>
> I reject untagged encoding. In particular, integer and fixed values must not become interchangeable merely because both have eight-byte bodies.

**What it fixes,** and nothing more: Every value in the input log is its full RUNTIME-SPEC §5 encoding, tag included, in lowercase hex (fixed 3 `580000000000000003`, true `4201`, the text "hi" `54000000026869`), equal to the value part of the matching `'N'` payload. Untagged encoding is rejected. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, T2, the permitted types (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T2 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T2   | As proposed | Only `I`, `X`, `B`, and `T` are permitted.                             |
>
> T2 — Permitted types.
>
> Adopt exactly:
>
> - `I` — integer
> - `X` — fixed
> - `B` — truth value
> - `T` — text
>
> `F` remains prohibited pending sheet R8. `L` is always prohibited. Lists do not become port types.

**What it fixes,** and nothing more: Only `I`, `X`, `B` and `T`; `F` stays prohibited pending sheet R8; `L` is always prohibited, and lists do not become port types. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, T3, the loader's checks (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T3 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T3   | As proposed | Validate spelling, tag, length, and text validity in the stated order. |
>
> T3 — Loader validation.
>
> Adopt the four validation stages in the proposed order:
>
> 1. Nonempty, even-length, lowercase hexadecimal.
> 2. Tag matches the declared port type.
> 3. Exact encoded length and valid representation.
> 4. Text bytes satisfy UTF-8 and the applicable door rules.
>
> The text-door validation remains subject to R3. This ruling does not settle R3.

**What it fixes,** and nothing more: In order: nonempty, even-length, lowercase hex; the tag the port's declared type's; the exact length and a valid representation; a text's bytes UTF-8 and the door's rules, those rules R3's and not settled here. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, T4, a mismatch is LOG-RECORD (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T4 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T4   | Yes         | Every listed malformed or mismatched value is LOG-RECORD.              |
>
> T4 — Classification.
>
> Adopt LOG-RECORD for every listed failure, including:
>
> - Wrong type tag.
> - Invalid encoded length.
> - Boolean byte other than `00` or `01`.
> - Invalid UTF-8.
> - Uppercase hexadecimal.
> - Odd-length hexadecimal.
> - Empty value.
>
> This applies D1's existing classification. It creates no new error code.

**What it fixes,** and nothing more: Every listed failure (a wrong tag, a wrong length, a boolean byte other than 00 or 01, invalid UTF-8, uppercase hex, odd-length hex, an empty value) is LOG-RECORD, D1's code; no new code. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, T5, the same rules for `once` and `t` (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T5 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T5   | As proposed | Identical tagged-value rules for `once` and `t` records.               |
>
> T5 — Record consistency.
>
> Adopt identical encoding and validation for both record types:
>
> - `once`: one tagged value per read-once port, in declaration order.
> - `t`: one tagged value per each-tick port, in declaration order.
>
> Every tag must match its corresponding port.

**What it fixes,** and nothing more: A `once` line carries one tagged value per read-once port and a `t` line one per each-tick port, each in declaration order, each tag its own port's. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, T6, canonical encoding (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the typed-values question, finding 8's last part). He ruled T1 to T6 in one message; this section quotes his opening, his table's row for T6 and his ruling on it, each unchanged.*

**The question.** Put to him in the session as T1 to T6: the wire form, (a) tagged or (b) untagged; the permitted types; the loader's checks; whether a mismatch is LOG-RECORD; `once` and `t` records; canonical encoding.

**His words:**

> I adopt T1(a): every input-log value carries its complete RUNTIME-SPEC §5 encoding, including its type tag, represented as lowercase hexadecimal.
>
> This is the correct choice because it preserves the exact encoded value bytes used by the `'N'` event. The loader can validate the type at the value's actual port position without translating or guessing its intended type.
>
> | Part | Ruling      | Decision                                                               |
> | ---- | ----------- | ---------------------------------------------------------------------- |
> | T6   | Required    | Exactly one canonical spelling for every accepted value.               |
>
> T6 — Canonical encoding.
>
> Adopt canonical encoding as mandatory.
>
> Every accepted value has exactly one permitted spelling. No alternate capitalization, omitted tags, shortened widths, or invalid representations are accepted.
>
> This establishes a consistent byte representation for the input log, `in_0`, `in_t`, `'N'` payloads, and receipts.

**What it fixes,** and nothing more: Every accepted value has exactly one spelling; no other capitalization, no omitted tag, no shortened width, no invalid representation. The log, in_0, in_t, the `'N'` payloads and the receipts have one byte form. D1, D2 and D3 are unchanged. R3 and R8 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 8: typed values, the compatibility, compliance, affected clauses and scope (2026-10-29)

*Added 2026-10-29, from the same message, each part unchanged.*

**His words:**

> ### Compatibility and implementation requirements
>
> I adopt the compatibility provisions:
>
> - Version 0 and COMPAT-0 remain untouched.
> - Version-0 laws still have no ports.
> - The 13 existing research logs and mutation fixtures must be rewritten into tagged form for 1a.
> - Those fixtures are not frozen texts.
>
> I also adopt all proposed compliance tests:
>
> 1. All four permitted types load successfully.
> 2. Their bytes match the corresponding `'N'` payload value bytes.
> 3. All eleven specified malformed or prohibited cases are refused with LOG-RECORD.
> 4. The same validation tests cover both `once` and `t`.
> 5. All three mutation plants must be detected:
>    - Tag left unchecked.
>    - Tag stripped before checking.
>    - Uppercase hexadecimal accepted.
>
> ### Affected clauses
>
> The authorized affected locations are:
>
> - §15.5 — value representation.
> - §15.9 — `'N'` event payload.
> - §15.15 — corresponding rows for §§15.5 and 15.6.
> - Sheet R12 — misaligned-log plant.
>
> No other clauses are implicitly reopened.
>
> ## Final scope of the ruling
>
> Typed-values question ruled
>
> The typed-values question is now settled in all six parts, T1–T6.
>
> Finding 8 is therefore fully ruled across D1, D2, D3, and typed values.
>
> The remaining work is exactly the sequence you identified:
>
> 1. Finding 20: R2, port place, counting, N2 and N3.
> 2. Draft 11: incorporate the settled rulings and the table originally put to me.
> 3. One complete re-read of Draft 11 before pinning.
>
> No pinning, committing, or implementation authorization is included in this ruling. R3 and R8 retain their independent open status.

**What it fixes:** version 0 and COMPAT-0 untouched; the research model's 13 logs and mutation fixtures rewritten in tagged form for 1a, not being frozen texts; the 1a tests put to him (the four types loading with their `'N'` bytes, the eleven refused cases LOG-RECORD, the same tests for `once` and `t`, the three plants detected); the affected places 15.5, 15.9, 15.15's rows on 15.5 and 15.6, and sheet R12's misaligned-log plant, and no other clause reopened. With it finding 8 is ruled across D1, D2, D3 and typed values. His list of the remaining work is recorded as he wrote it; finding 20 (whether `'R'` carries the cut) and R2, the port place, counting, N2 and N3 are each still owed their own ruling.

### Finding 20: F20.1, where the cut lives (2026-10-29)

*Added 2026-10-29. The question was put to him in the session. He ruled F20.1 to F20.4 in one message and said they may be recorded separately; this section quotes his opening, his table's row(s) for F20.1 and his ruling on it, each unchanged.*

**The question.** Put to him in the session: F20.1, where the cut lives ((a) `'R'`'s payload, (b) a new event, (c) a receipt line, (d) derived by replay); F20.2, the decoding rule; F20.3, the tick block's and the ports' frames; F20.4, which clause an If-condition refusal names (S6).

**His words:**

> I adopt F20.1(a): version 1's `R` event carries the cut in its payload.
>
> The cut must be committed by the refusal event itself, included in the trace head, and therefore bound into the receipt core. The court must decode the recorded cut, not reconstruct it by rerunning the reference.
>
> | Part               | Ruling      | Decision                                                          |
> | ------------------ | ----------- | ----------------------------------------------------------------- |
> | F20.1              | (a)         | Cut carried in version 1's `R` payload.                           |
>
> ### F20.1 — Where the cut lives
>
> Adopt (a).
>
> I reject:
>
> - (b) A separate event, because it unnecessarily splits one refusal across two events.
> - (c) A receipt-only cut, because it separates the cut from the event-chain commitment.
> - (d) Replay-based derivation, because the court must read the committed record rather than depend on another execution.
>
> Version 0 remains unchanged: its `R` payload contains the refusal code alone.

**What it fixes,** and nothing more: Version 1's `'R'` event carries the cut in its payload, committed by the trace head and so bound into the receipt core; the court decodes the recorded cut and never reruns the reference for it. (b), (c) and (d) are rejected. Version 0's `'R'` stays the code alone. Finding 8 is unchanged. R2, the port place, counting, N2 and N3 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 20: F20.2, the decoding rule (2026-10-29)

*Added 2026-10-29. The question was put to him in the session. He ruled F20.1 to F20.4 in one message and said they may be recorded separately; this section quotes his opening, his table's row(s) for F20.2 and his ruling on it, each unchanged.*

**The question.** Put to him in the session: F20.1, where the cut lives ((a) `'R'`'s payload, (b) a new event, (c) a receipt line, (d) derived by replay); F20.2, the decoding rule; F20.3, the tick block's and the ports' frames; F20.4, which clause an If-condition refusal names (S6).

**His words:**

> I adopt F20.1(a): version 1's `R` event carries the cut in its payload.
>
> The cut must be committed by the refusal event itself, included in the trace head, and therefore bound into the receipt core. The court must decode the recorded cut, not reconstruct it by rerunning the reference.
>
> | Part               | Ruling      | Decision                                                          |
> | ------------------ | ----------- | ----------------------------------------------------------------- |
> | F20.2              | As proposed | Decode the recorded frames under the law-header-selected grammar. |
>
> ### F20.2 — Decoding
>
> Adopt the proposed decoding principles:
>
> 1. The law header selects the grammar.
> 2. The refusal code must match the receipt's status line.
> 3. At least one frame is required.
> 4. Frames must satisfy the applicable S1–S7 shapes.
> 5. The decoder extracts only the specified structural information:
>    - Clause.
>    - Selector.
>    - For bit when applicable.
>    - Last-frame If arm when applicable.
> 6. The pinned rule computes \\(\hat K\\) from those decoded fields.
> 7. No value or operation count is read to derive the cut.
> 8. A malformed payload is refused with its applicable reason. There is no fallback to version 0's grammar.
>
> One qualification: this adopts the semantic decoding rule, not an independent certification of the exact draft-2 byte grammar. The actual S1–S7 byte layouts and their probe results must still be verified before the format is frozen.

**What it fixes,** and nothing more: The law's header selects the grammar; the code must equal the status line's; at least one frame; the frames hold to S1 to S7; only clause, selector, a For's bit where it applies and a last-frame If's arm are read, and the pinned rule computes K̂ from them, reading no value or operation count; a malformed payload is refused with its reason, with no fall-back to version 0. This adopts the semantic rule, not the draft-2 byte grammar, whose S1-S7 layouts and probe results are still to be verified before the format freezes. Finding 8 is unchanged. R2, the port place, counting, N2 and N3 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 20: F20.3, the version-1 frames (2026-10-29)

*Added 2026-10-29. The question was put to him in the session. He ruled F20.1 to F20.4 in one message and said they may be recorded separately; this section quotes his opening, his table's row(s) for F20.3 and his ruling on it, each unchanged.*

**The question.** Put to him in the session: F20.1, where the cut lives ((a) `'R'`'s payload, (b) a new event, (c) a receipt line, (d) derived by replay); F20.2, the decoding rule; F20.3, the tick block's and the ports' frames; F20.4, which clause an If-condition refusal names (S6).

**His words:**

> I adopt F20.1(a): version 1's `R` event carries the cut in its payload.
>
> The cut must be committed by the refusal event itself, included in the trace head, and therefore bound into the receipt core. The court must decode the recorded cut, not reconstruct it by rerunning the reference.
>
> | Part               | Ruling      | Decision                                                          |
> | ------------------ | ----------- | ----------------------------------------------------------------- |
> | F20.3 — tick block | As proposed | Plain frame, clause with `sel = 0xFFFF`, no extra field.          |
> | F20.3 — ports      | As proposed | No frame for port declarations.                                   |
>
> ### F20.3 — Version 1 frame shapes
>
> Tick block: Adopt the plain frame with selector `0xFFFF` and no additional field. Its body is repeated when another tick may run.
>
> Ports: Adopt no frame. Port declarations do not contribute an operation or a refusal stack frame under the stated §15.13.8 premises.
>
> Perform: Adopt the proposed allowance for a Perform as the last frame, including the TICK-BUDGET refusal case.

**What it fixes,** and nothing more: The tick block is a plain frame, its clause with selector 0xFFFF and no extra field; a port declaration has no frame; a Perform may be the last frame, TICK-BUDGET's case included. Finding 8 is unchanged. R2, the port place, counting, N2 and N3 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 20: F20.4, an If-condition refusal names the arm (2026-10-29)

*Added 2026-10-29. The question was put to him in the session. He ruled F20.1 to F20.4 in one message and said they may be recorded separately; this section quotes his opening, his table's row(s) for F20.4 and his ruling on it, each unchanged.*

**The question.** Put to him in the session: F20.1, where the cut lives ((a) `'R'`'s payload, (b) a new event, (c) a receipt line, (d) derived by replay); F20.2, the decoding rule; F20.3, the tick block's and the ports' frames; F20.4, which clause an If-condition refusal names (S6).

**His words:**

> I adopt F20.1(a): version 1's `R` event carries the cut in its payload.
>
> The cut must be committed by the refusal event itself, included in the trace head, and therefore bound into the receipt core. The court must decode the recorded cut, not reconstruct it by rerunning the reference.
>
> | Part               | Ruling      | Decision                                                          |
> | ------------------ | ----------- | ----------------------------------------------------------------- |
> | F20.4              | Arm         | An If-condition refusal names the arm, consistent with version 0. |
>
> ### F20.4 — If-condition refusal
>
> Adopt the arm's clause, not the If head's clause.
>
> This preserves version 0's convention and makes S6 consistent across versions.

**What it fixes,** and nothing more: A refusal inside an If's condition names the arm's clause, not the head's, as in version 0, so S6 is the same in both versions. Finding 8 is unchanged. R2, the port place, counting, N2 and N3 stay open. Nothing is pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Finding 20: its compliance requirements and scope (2026-10-29)

*Added 2026-10-29, from the same message, each part unchanged.*

**His words:**

> ## Compliance requirements
>
> I adopt the proposed tests:
>
> - Encoder/decoder round-trip.
> - S1–S7 forgery rejection with the correct reason.
> - Refusal-code mismatch rejection.
> - Version 0 `R` unchanged.
> - COMPAT-0 remains HOLDS.
> - Stop, NOT-RUN and LOG-OPEN emit no `R`.
> - Grammar selected by header, never payload inspection.
> - Four identical `R` byte sequences in 1b.
>
> All four mutation plants must be caught:
>
> 1. Court reruns the reference to derive the cut.
> 2. Decoder sniffs the payload instead of reading the header.
> 3. For bit is dropped.
> 4. If arm is dropped.
>
> ## Scope and remaining work
>
> Finding 20 is ruled at the semantic level described above. The exact S1–S7 encoding still requires its probe.
>
> The following remain separate and open:
>
> - R2: statement kinds, spellings and reach rules.
> - Port place.
> - Counting.
> - N2 and N3: read-once session events.
>
> Finding 8 remains closed and unchanged.
>
> No pinning, committing, or implementation authorization is included. You may record these Finding 20 rulings separately, preserving the distinction between adopted semantics and the still-required byte-level verification.

**What it fixes:** the 1a tests put to him (the round trip; S1 to S7's forgeries refused with their reasons; a code mismatch refused; version 0's `'R'` unchanged and COMPAT-0 HELD; no `'R'` at the stop, NOT-RUN or LOG-OPEN; the grammar by the header; four identical `'R'` byte sequences in 1b) and the four plants caught. Finding 20 is ruled at the semantic level; the exact S1-S7 encoding still needs its probe, before the format freezes.

### R2, as ruled: R2.1, statement kinds (2026-10-29)

*Added 2026-10-29. Sheet R2 (above) proposed the forms; the question was put to him in the session. He ruled R2.1 to R2.3 in one message; this section quotes his line adopting them and his ruling on R2.1, each unchanged.*

**The question.** Put to him in the session: R2.1, the statement kinds ((a) two, (b) three, (c) four); R2.2, the spellings and type words; R2.3, the reach rules ((a) as proposed, (b) each tick its own scope, (c) the budget able to stop reach).

**His words:**

> I adopt the recommended option for all three parts: R2.1(a), R2.2 as proposed, and R2.3(a).
>
> ## R2.1 — Statement kinds: (a)
>
> Adopt exactly two kinds:
>
> 1. Port declaration, carrying:
>    - Mode: each tick or once.
>    - Type.
>    - Name.
> 2. Tick block, carrying its body and optional budget.
>
> The budget is an attribute, not a separate statement kind. Each-tick and read-once ports are one kind with different modes.
>
> Adopt the examples and compliance requirements:
>
> - Each form parses into the correct kind and mode.
> - Kind and mode are represented in version 1 law bytes.
> - Changing only a port's mode changes the law seal.

**What it fixes,** and nothing more: Version 1 adds exactly two statement kinds: the port declaration, carrying a mode (each tick or once), a type and a name; and the tick block, carrying its body and an optional budget, the budget an attribute. Kind and mode are in version 1's law bytes; a change of mode alone changes the law seal. The port place, counting and the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open; findings 8 and 20 are unchanged. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### R2, as ruled: R2.2, spellings (2026-10-29)

*Added 2026-10-29. Sheet R2 (above) proposed the forms; the question was put to him in the session. He ruled R2.1 to R2.3 in one message; this section quotes his line adopting them and his ruling on R2.2, each unchanged.*

**The question.** Put to him in the session: R2.1, the statement kinds ((a) two, (b) three, (c) four); R2.2, the spellings and type words; R2.3, the reach rules ((a) as proposed, (b) each tick its own scope, (c) the budget able to stop reach).

**His words:**

> I adopt the recommended option for all three parts: R2.1(a), R2.2 as proposed, and R2.3(a).
>
> ## R2.2 — Spellings
>
> Adopt the four exact proposed spellings:
>
> | Form                | Accepted spelling                                      |
> | ------------------- | ------------------------------------------------------ |
> | Each-tick port      | `Let <name> be given each tick as <type>.`             |
> | Read-once port      | `Let <name> be given as <type>.`                       |
> | Tick block          | `Each tick, do the following.`                         |
> | Budgeted tick block | `Each tick, at most <N> operations, do the following.` |
>
> Adopt the permitted type words:
>
> - `an integer`
> - `a fixed`
> - `a truth value`
> - `a text`
>
> `a float` remains excluded pending R8.
>
> Additional decisions:
>
> - `<N>` uses the version-0 decimal representation for numeric bounds.
> - Capitalization, punctuation and door repairs follow version-0 sentence treatment.
> - Clauses remain sentences ending in a period.
> - `truth value` and `text` are reserved as type words only within the port form.
> - No new `Input` keyword is introduced.
>
> Reject the proposed alternative spellings:
>
> - `For each tick, ...`
> - `On each tick, ...`
> - `Receive ...`
> - `Take ...`
>
> The first must not become a tick block, and existing version-0 calls must retain their meanings.
>
> Adopt the compliance requirements, including:
>
> - COMPAT-0 remains HOLDS over all 3,361 frozen texts.
> - New spellings parse only under version 1.
> - Rejected spellings remain SYNTAX.
> - Existing version-0 uses of `truth value` and `text` remain unchanged.
> - The specified `For each tick` mutation plant is detected.

**What it fixes,** and nothing more: The four spellings `Let <name> be given each tick as <type>.`, `Let <name> be given as <type>.`, `Each tick, do the following.` and `Each tick, at most <N> operations, do the following.`; the type words `an integer`, `a fixed`, `a truth value` and `a text`, the last two reserved only within the port form; `a float` excluded pending R8; `<N>` in version 0's decimal form for bounds; version 0's sentence treatment; no `Input` keyword; `For each tick, …`, `On each tick, …`, `Receive …` and `Take …` rejected. The port place, counting and the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open; findings 8 and 20 are unchanged. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### R2, as ruled: R2.3, reach rules (2026-10-29)

*Added 2026-10-29. Sheet R2 (above) proposed the forms; the question was put to him in the session. He ruled R2.1 to R2.3 in one message; this section quotes his line adopting them and his ruling on R2.3, each unchanged.*

**The question.** Put to him in the session: R2.1, the statement kinds ((a) two, (b) three, (c) four); R2.2, the spellings and type words; R2.3, the reach rules ((a) as proposed, (b) each tick its own scope, (c) the budget able to stop reach).

**His words:**

> I adopt the recommended option for all three parts: R2.1(a), R2.2 as proposed, and R2.3(a).
>
> ## R2.3 — Reach rules: (a)
>
> Adopt the recommended reach semantics.
>
> Port declarations
>
> - Contain no statements.
> - Add nothing to closure or CUT-0 reach.
> - Do not add themselves as reachable claims.
> - Do not create a refusal frame.
>
> This preserves the already-settled PREFIX ruling and F20.3.
>
> Tick block
>
> - Contains its numbered body clauses.
> - Its body may contain If, For, While and Perform.
> - Reached as a later sibling at the top level, it adds its body and everything that body may execute, transitively, including reached Performs.
> - Below the top of the cut, its body is included again because another tick may run.
> - Its budget does not restrict reach.
>
> I reject alternative (b), which would make reach depend on individual tick identity.
>
> I reject alternative (c), which would make reach depend on the operation budget and counting.
>
> Control-flow boundary
>
> Adopt the rule that execution within the tick body does not reach backward into the prefix. The prefix is executed once before the first tick.
>
> One boundary is important: the proposed requirement that the tick block occupy the last top-level position belongs to the separate port-place ruling. I am not deciding its placement under R2.
>
> ### Examples and compliance
>
> Adopt both proposed examples:
>
> 1. A prefix refusal whose reachable set includes the claim at 2.1 through a Perform reached from the tick body.
> 2. A refusal at 3.1 during tick 1 whose reachable set includes that prefix claim again.
>
> Adopt the compliance requirements:
>
> - Both closure and CUT-0 calculations worked by hand and checked by the probe.
> - Port declarations add nothing in either calculation.
> - Detect all three mutation plants:
>   - Tick block adds nothing below the top.
>   - Port declaration adds itself.
>   - Reach calculation skips Performs reached from the tick body.

**What it fixes,** and nothing more: A port declaration contains no statement, adds nothing to the closure or to CUT-0's reach, does not add itself and makes no refusal frame. The tick block contains its numbered body, which may hold If, For, While and Perform; reached as a later top-level sibling it adds its body and everything that may execute from it, transitively, reached Performs included; below the top of the cut it adds its body again; its budget does not restrict reach. Execution in the tick body does not reach back into the prefix, which runs once before the first tick. Alternatives (b) and (c) are rejected. The tick block's last top-level place is the port-place ruling's, not decided here. The port place, counting and the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open; findings 8 and 20 are unchanged. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### R2, as ruled: the order of work, the publication decision and the scope (2026-10-29)

*Added 2026-10-29, from the same message: his opening on the order of work and the publication decision, and his scope, each unchanged.*

**His words:**

> First, the correction about sequencing is accepted: the containment fixture test precedes pinning the exact candidate digest. The version-1 reference must exist and pass that test before its candidate is pinned. Pinning first would reverse the dependency established by the earlier ruling.
>
> The publication decision remains deferred until Draft 11 has been completely re-read and its findings disposed of.
>
> ## Scope and remaining work
>
> R2 ruled
>
> All three R2 parts are now settled.
>
> The following remain independently open:
>
> 1. Port place.
> 2. Counting and budget semantics, including R9.
> 3. N2 and N3.
> 4. S1–S7 byte-layout probe.
>
> Finding 8 and Finding 20 remain closed.
>
> Implementation sequence remains: complete the remaining specification rulings and probes, produce Draft 11, conduct the complete re-read, build and pass the containment fixture against the version-1 reference, and only then pin the exact candidate digest.
>
> No implementation, pinning, committing, or publication authorization is included in this ruling.

**What it fixes:** it confirms the order already ruled (the containment fixture test passes on the version-1 reference before the exact candidate's digest is pinned) and defers the publication decision until draft 11 is wholly re-read and its findings disposed. Nothing is authorized by it.

### R2, as ruled: R2.3's wording clarified (2026-10-29)

*Added 2026-10-29. Put to him: R2.3's "does not reach backward into the prefix" is about the prefix's statements running again, not about procedures defined before the tick block, which the tick body reaches by Perform. His words, from the message that also asked for the port-place packet, unchanged.*

**His words:**

> Your proposed clarification to R2.3 is correct: “does not reach backward into the prefix” should mean that execution of the tick body does not cause earlier top-level prefix statements to run again. It must not exclude procedures defined in the prefix from the reach closure when the tick body reaches them through `Perform`. In your example, claim 2.1 is reachable because the tick body performs the procedure containing it—not because the prefix is re-executed.
>
> That distinction should be explicit in Draft 11 and checked during the whole re-read.
>
> R2 remains ruled; this is a wording clarification, not a reopening. The other open items remain as listed. Nothing about this authorizes implementation, pinning, committing, or publication.

**What it fixes,** and nothing more: in R2.3, execution of the tick body never makes an earlier top-level prefix statement run again; a procedure defined in the prefix stays in the reach closure when the tick body reaches it by Perform. A wording clarification, not a reopening: draft 11 states it, and the whole re-read checks it.

### The port place, as ruled: PP1, where a port may be declared (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP1, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP1 — Where ports may be declared
> Adopted: (a)
> Port declarations are permitted only as top-level clauses, before the tick block. Prefix statements may appear before, between, and after port declarations.
> A declaration inside an `If`, loop, procedure, tick body, or inline arm is refused PORT-PLACE.
> This preserves RO′-3 and the once-only binding premise. Options (b) and (c) are rejected.

**What it fixes,** and nothing more: Port declarations stand only as top-level clauses, before the tick block; prefix statements may stand before, between and after them; a declaration in an If, a loop, a procedure, the tick body or an inline arm is refused PORT-PLACE. (b) and (c) rejected. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: PP2, the tick block's place (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP2, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP2 — Tick-block placement
> Adopted: (a)
> There may be at most one tick block, and it must be the last top-level clause.
> A second tick block, a nested tick block, or a tick block followed by another top-level clause is refused TICK-PLACE.
> Option (b), requiring a tick block in every v1 law, is rejected.

**What it fixes,** and nothing more: At most one tick block, the last top-level clause; a second, a nested one, or one followed by a top-level clause is refused TICK-PLACE. (b) rejected. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: PP3, ports without a tick block (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP3, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP3 — Ports without a tick block
> Adopted: (a)
>
> * Read-once ports alone are allowed. They form a one-shot law with inputs.
> * An each-tick port without a tick block is refused PORT-PLACE.
> * A tick block without ports remains allowed.
>
> Options (b) and (c) are rejected.

**What it fixes,** and nothing more: Read-once ports alone are allowed (a one-shot law with inputs); an each-tick port with no tick block is refused PORT-PLACE; a tick block with no port stays allowed. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: PP4, which reads are allowed (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP4, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP4 — Permitted reads
> Adopted: recommended rule, with clarification
>
> * An each-tick port may be read only in the tick body or in a procedure reached only from the tick body.
> * A read-once port may be read only after its declaration in the execution structure: later top-level statements, the tick body, or procedures reached only from those permitted contexts.
> * Both textual placement and evaluation reach must be checked. A procedure definition's physical position in the document does not, by itself, determine whether its reads are permitted. Its reachable call contexts determine that.
>
> A read violating either requirement is PORT-READ.
> This means the procedure in your evaluation example cannot evade the rule merely because its body is textually separate from the top-level call that reaches it. The read is rejected because the procedure is reached before the read-once declaration.
> I reject folding these cases into PORT-PLACE. Misplaced declarations and impermissible reads are distinct faults and deserve distinct codes.

**What it fixes,** and nothing more: An each-tick port is read only in the tick body or a procedure reached only from it; a read-once port only after its declaration in the execution structure; both textual placement and evaluation reach are checked, a procedure's reachable call contexts, not its place in the text, deciding its reads; a violation is PORT-READ, not PORT-PLACE. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: PP5, assigning and redeclaring a port (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP5, and his settlement of it, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP5 — Port mutation
> Partially adopted; one collision needs resolution
> I adopt the read-only rule and the proposed PORT-VARIABLE coverage for:
>
> * `Set`, `Increase`, `Decrease`, `Append`, or `Remove` applied to a port.
> * A port used as a `For` counter.
>
> I also adopt REDECLARED for a second declaration of an existing port name.
> There is, however, an overlap in the proposal: it assigns a second `Let` of a port's name to PORT-VARIABLE, while assigning a second declaration of that name to REDECLARED. Those descriptions can refer to the same source construct.
> My ruling: a second declaration of the same name is REDECLARED; an assignment or mutation through an existing port binding is PORT-VARIABLE. Do not classify a duplicate declaration as PORT-VARIABLE merely because it uses `Let`. If the language has a distinct non-declaration `Let` form, specify it separately before assigning it a code.
>
> PP5 is now fully settled:
>
> * PORT-VARIABLE: `Set`, `Increase`, `Decrease`, `Append`, or `Remove` applied to a port, and a port used as a `For` counter.
> * REDECLARED: a second declaration of a port's name, including a second `Let`, using version 0's existing redeclaration rule.
> * There is no assignment-form `Let`; every `Let X be E` declares `X`.
>
> I withdraw my earlier qualification that a further distinction for `Let` might be needed. Your correction resolves the collision without adding a new rule or code.

**What it fixes,** and nothing more: PORT-VARIABLE: Set, Increase, Decrease, Append or Remove on a port, and a port used as a For counter. REDECLARED: a second declaration of a port's name, a second `Let` included, by version 0's rule; every `Let X be E` declares X. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: PP6, the codes and their order (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "port place"). He adopted a text as his complete ruling, with PP5 corrected; this section quotes his adoption and the text's PP6, each unchanged.*

**The question.** Put to him in the session as PP1 to PP6: where a port may be declared; the tick block's place; a law with ports and no tick block; which reads are allowed (PORT-READ or folded into PORT-PLACE); what counts as assigning a port; the codes and their order.

**His words:**

> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
>
> PP6 — Codes and phase ordering
> Adopted
> Add the four new codes:
>
> * PORT-PLACE
> * TICK-PLACE
> * PORT-READ
> * PORT-VARIABLE
>
> They belong in phase 6 of SPEC §13, in document walk order. The first faulty clause in that order wins.
> REDECLARED remains its existing code; it is not one of the four new codes.
> The phase-table row must match the codes the front end can actually raise, and the self-test must verify that equality. The self-test count must be updated to reflect the added checks; do not assume the resulting total is 43.

**What it fixes,** and nothing more: Four new phase-6 codes, PORT-PLACE, TICK-PLACE, PORT-READ and PORT-VARIABLE, in SPEC §13's document walk order, the first faulty clause winning; REDECLARED stays version 0's code; the phase-table row equals the codes the front end can raise, the self-test holding it, its count updated. Counting, the budget's meaning (R9), N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### The port place, as ruled: its compliance, and his adoption (2026-10-29)

*Added 2026-10-29: the text's compliance paragraph, and his adoption of the whole, each unchanged.*

**His words:**

> Compliance
> I adopt the proposed compliance requirements, including the three mutation plants. Add a test that distinguishes a procedure definition's textual position from the call contexts that reach it; that is essential to the PP4 clarification.
> The examples should produce the stated outcomes, including the evaluation-based PORT-READ in the procedure example.
>
> Yes. I adopt the text as the complete port-place ruling, including your PP5 correction.
> PP5 is now fully settled:
>
> * PORT-VARIABLE: `Set`, `Increase`, `Decrease`, `Append`, or `Remove` applied to a port, and a port used as a `For` counter.
> * REDECLARED: a second declaration of a port's name, including a second `Let`, using version 0's existing redeclaration rule.
> * There is no assignment-form `Let`; every `Let X be E` declares `X`.
>
> I withdraw my earlier qualification that a further distinction for `Let` might be needed. Your correction resolves the collision without adding a new rule or code.
> Adopted as a whole:
>
> * PP1–PP3: declaration and tick-block placement, including read-once-only laws.
> * PP4: permitted reads checked by both textual placement and evaluation reach; a procedure's reachable call contexts, not merely its textual position, determine whether its reads are legal.
> * PP5: the corrected mutation and redeclaration rules above.
> * PP6: four new phase-6 codes, with first-fault document walk order.
> * Compliance: the proposed tests and the additional test distinguishing procedure position from its reachable call contexts.
>
> The port-place item is now ruled. No implementation, pinning, commit, or publication is authorized.

**What it fixes:** the 1a tests put to him (each example's code at its clause, the phase-table row, COMPAT-0 HELD, the three plants), and a test telling a procedure's place in the text from the call contexts that reach it. The port place is ruled.

### Counting and the budget, as ruled: C1, what version 1 adds to counting (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (counting). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on C1, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> C1 — What v1 adds
> Adopted: (a)
> Nothing new is counted:
>
> * Port binding counts 0, whether read-once or each-tick.
> * Port reads count 0, like variable reads.
> * The tick block itself adds no operation.
> * Emitting `T` or `N` events counts 0.
> * An empty tick body costs 0 operations.
>
> Options (b) and (c) are rejected. This preserves the binding premise underlying §15.13.8's \(\hat K\) argument.

**What it fixes,** and nothing more: Nothing new is counted: binding a port (each tick or once) counts 0, reading a port counts 0, the tick block adds no operation, emitting `'T'` or `'N'` counts 0, and an empty tick body costs 0. (b) and (c) rejected. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: C2, what `'T'`'s count means (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (counting). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on C2, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> C2 — Meaning of `T`'s count
> Adopted: (a)
> The `c` in `T(t,c)` is the running total of `ops` from the start of the run through the moment `T` is emitted.
> It never decreases and includes prefix operations. A tick's own operation count is the difference between consecutive `T` counts. The receipt's `ops` is the final running total.
> Option (b) is rejected.

**What it fixes,** and nothing more: In `'T'`(t, c), c is the running total of `ops` from the start of the run to the moment `'T'` is emitted; a tick's own count is the difference between consecutive `'T'` counts; the receipt's `ops` is the final total. (b) rejected. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: C3, when the count goes up (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (counting). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on C3, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> C3 — When counting occurs
> Adopted
> The existing version-0 rule remains unchanged: increment the single `ops` counter by 1 immediately before each counted operation. Use that same counter in v1.
> An If arm's count belongs to its own clause, not the If head.

**What it fixes,** and nothing more: Version 0's rule unchanged: the single `ops` counter gains 1 immediately before each counted operation, the same counter in version 1; an If arm's count belongs to its own clause. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: B1, the budget in the law (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the budget (R9)). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on B1, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> B1 — Where the budget lives
> Adopted: R9 (b)
> The optional budget is part of the law. Its value is covered by the law's seal.
> A tick exceeding the budget refuses with TICK-BUDGET at the same counted operation in every execution. A host stopping a run remains a separate STOPPED-BY-HOST outcome and never constitutes a verdict or emits `R`.
> Option (a) is rejected.

**What it fixes,** and nothing more: R9 (b): the optional budget is part of the law, under its seal; a tick past it refuses TICK-BUDGET at the same counted operation in every execution; a host stop stays STOPPED-BY-HOST, never a verdict, never an `'R'`. (a) rejected. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: B2, the range of N (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the budget (R9)). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on B2, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> B2 — Range of N
> Adopted: (a)
> The budget must be an integer literal in the range \(1\) through \(2^{62}\), inclusive.
>
> * `at most 0` is refused at compile time.
> * Any value above \(2^{62}\) is refused at compile time.
> * An absent budget is encoded as `0` in the law's bytes; a written budget of zero is not permitted.
> * Out-of-range values use the existing FUEL code.
>
> Option (b), introducing TICK-BUDGET-RANGE, is rejected.

**What it fixes,** and nothing more: N is an integer literal from 1 to 2^62; `at most 0` and anything above 2^62 are refused at compile time with version 0's FUEL; no budget is written 0 in the law's bytes, and a written budget of zero is not allowed. (b) rejected. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: B3, where the refusal falls (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the budget (R9)). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on B3, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> B3 — Where the refusal falls
> Adopted
> The tick's count starts at zero at its `T`. Prefix operations are never charged against the tick budget.
> Immediately before each counted operation, increment `ops`. If that increment makes the tick's count \(N+1\), refuse with TICK-BUDGET before executing that operation.
> Consequently:
>
> * The refused operation is included in `ops`.
> * `tick-ops` is exactly \(N+1\).
> * The refusal is attributed to the clause whose statement is executing.
> * For an If-condition refusal, that is the arm's clause, consistent with F20.4.
> * Refusing before incrementing is rejected.

**What it fixes,** and nothing more: A tick's count starts at 0 at its `'T'`; the prefix is never charged; when an increment makes the tick's count N + 1, TICK-BUDGET refuses before that operation executes, the operation counted in `ops`, `tick-ops` exactly N + 1, at the clause whose statement is executing (an If condition's arm, as F20.4). R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: B4, the cut and `'R'` (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the budget (R9)). He ruled C1 to C3 and B1 to B4 in one message; this section quotes his opening and his ruling on B4, each unchanged.*

**The question.** Put to him in the session as part C, counting (C1 what version 1 adds, C2 what `'T'`'s count means, C3 when the count goes up), and part B, the budget (B1 in the law or not, B2 the range of N, B3 where the refusal falls, B4 the cut and `'R'`).

**His words:**

> I adopt the recommended choices for all seven parts: C1–C3 and B1–B4. The counting rules and budget semantics are now settled separately.
>
> B4 — Cut and `R`
> Adopted
> TICK-BUDGET is an ordinary refusal under Finding 20.
>
> * `R` carries the code `TICK-BUDGET` and the stack of statements at the refused operation.
> * Its last frame may be any permitted frame kind, including `Perform`.
> * Status is `REFUSED TICK-BUDGET <clause>`.
> * The refused tick is included in `ticks`.
> * If the refused operation lies inside a claim's evaluation, that claim is open at the cut and court R8 does not hold it.
> * A host stop remains separate and emits no `R`.
>
> The four worked examples are adopted with their stated statuses, counts, and cut frames.

**What it fixes,** and nothing more: TICK-BUDGET is an ordinary refusal under finding 20: `'R'` carries the code and the statement stack at the refused operation, its last frame any permitted kind (a Perform included); the status is `REFUSED TICK-BUDGET <clause>`; `ticks` counts the refused tick; a claim whose evaluation holds the refused operation is open at the cut and court R8 does not hold it; a host stop emits no `'R'`. The four worked examples are adopted. R2.2, R2.3, PP2, R4, finding 20 and finding 8 are unchanged. N2, N3 and the S1-S7 byte probe stay open. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### Counting and the budget, as ruled: the compliance and the scope (2026-10-29)

*Added 2026-10-29, from the same message, each part unchanged.*

**His words:**

> Compliance
> I adopt the proposed compliance tests:
>
> * Each worked budget example must produce its stated status, `tick-ops`, `ops`, and `R` frames.
> * Exactly \(N\) counted operations pass; operation \(N+1\) is refused before execution.
> * Prefix operations do not count against a tick.
> * Binding and port reads add zero to `ops`; an empty tick leaves consecutive `T` counts unchanged.
> * Out-of-range budget values produce FUEL.
> * The four 1b executions refuse at the same operation and produce identical `R` bytes.
> * All four mutation plants must be caught: binding counted, refusal before increment, budget counted from run start, and If refusal attributed to the head rather than the arm.
>
> Scope and remaining work
> C1–C3 and B1–B4 are ruled. The named dependencies—R2.2, R2.3, PP2, R4, Finding 20, and Finding 8—remain as settled; none is reopened.
> Still open before Draft 11:
>
> 1. N2 and N3.
> 2. The S1–S7 byte-layout probe.
>
> No implementation, pinning, commit, or publication is authorized. Draft 11 must incorporate these rulings and then receive its complete re-read. The containment fixture still precedes pinning the exact candidate digest.

**What it fixes:** the 1a tests put to him (each worked example's status, `tick-ops`, `ops` and `'R'` frames; N operations pass and the (N + 1)th is refused before it executes; the prefix uncharged; binding and port reads adding 0; FUEL for an out-of-range N; the four 1b executions alike) and the four plants caught.

### N2 and N3, as ruled: N2, `end()` before the read-once record closes (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "A2" row, N2 and N3). He ruled N2 and N3 in one message as two separate rulings; this section quotes his opening and his ruling on N2, each unchanged.*

**The question.** Put to him in the session as two independent rulings: N2, an `end()` before the read-once record closes, (a) legal, the read-once stop, or (b) refused; N3, when the host runs the statements before the first read-once declaration, (a) at the session's opening or (b) at the record's close or at `end()`.

**His words:**

> I adopt N2 (a) and N3 (a) as two separate rulings. Neither reopens the previously settled rules.
>
> N2 — `end()` before the read-once record closes
> Adopted: (a)
> Ending the session while the read-once record is incomplete is legal. It is the read-once stop.
> The projection is:
>
> ```
> end 0 not-run read-once INPUT-MISSING <port>
> ```
>
> The port named is the first empty read-once port in declaration order. The receipt reports:
>
> ```
> status NOT-RUN READ-ONCE INPUT-MISSING <port>
> ```
>
> The following are also adopted:
>
> * END-UNDISPOSED still applies. An accepted arrival that has neither been assigned nor dropped prevents `end()`.
> * A partly filled read-once record is not written to the log. Its assignments remain in the history.
> * The verifier checks the named port against the history; the loader does not independently establish which port was first empty.
> * After a refusal, `end()` remains the only legal move.
>
> The `g`-assigned, `h`-empty example therefore produces the stated `INPUT-MISSING h` result, without writing `g`'s assignment into the log.
> Option (b), refusing `end()` while the record is open, is rejected.
> Scope: this does not settle which event fills or closes the record, nor whether tick 1 can close before the record. Those lifecycle questions remain open.

**What it fixes,** and nothing more: An `end()` while the read-once record is incomplete is legal and is the read-once stop: it projects to `end 0 not-run read-once INPUT-MISSING <port>`, the first empty read-once port in declaration order, and the receipt reads `status NOT-RUN READ-ONCE INPUT-MISSING <port>`. END-UNDISPOSED still applies; a partly filled record is not written to the log, its assignments staying in the history; the verifier checks the port against the history; after a refusal `end()` stays the only legal move. (b) rejected. Which event fills or closes the record, and whether tick 1 may close before it, stay open. RO′-2 to RO′-5, 8.3, 8.5, PP1 to PP4, counting and finding 20 are unchanged. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### N2 and N3, as ruled: N3, when the host runs the statements before the first read-once declaration (2026-10-29)

*Added 2026-10-29. The question was put to him in the session (the amended set's "A2" row, N2 and N3). He ruled N2 and N3 in one message as two separate rulings; this section quotes his opening and his ruling on N3, each unchanged.*

**The question.** Put to him in the session as two independent rulings: N2, an `end()` before the read-once record closes, (a) legal, the read-once stop, or (b) refused; N3, when the host runs the statements before the first read-once declaration, (a) at the session's opening or (b) at the record's close or at `end()`.

**His words:**

> I adopt N2 (a) and N3 (a) as two separate rulings. Neither reopens the previously settled rules.
>
> N3 — When the host executes the prefix
> Adopted: (a)
> At session opening, before accepting its first event, the host executes the top-level statements preceding the first read-once declaration.
> If the prefix refuses:
>
> * The refusal is known immediately.
> * Subsequent moves other than `end()` are refused with RUN-REFUSED.
> * The refusal writes `R` with its cut under Finding 20.
>
> If the prefix completes, the run waits at the first read-once declaration. The read-once `N` events are emitted there when the record closes.
> Option (b), delaying prefix execution until record closure or `end()`, is rejected.
> The following are adopted:
>
> * Prefix operations precede all `T` events and are not charged against the tick budget.
> * PP1's permitted prefix statements run as specified by RO′-3.
> * A refusal during prefix execution is an ordinary refusal with its Finding 20 cut.
>
> The division-by-zero example is adopted: clause 1 refuses at session opening, before any arrival is accepted; a later arrival is refused RUN-REFUSED; `end()` ends the session; the receipt reports `REFUSED DIVISION-BY-ZERO 1`.
> Finding 10 qualification: I agree that Finding 10 remains an open dependency. N3 does not decide the exact end-record representation for a refused session. That must be ruled before Draft 11, or explicitly identified as unresolved in it.

**What it fixes,** and nothing more: At the session's opening, before it accepts its first event, the host runs the top-level statements before the first read-once declaration. A refusal there is known at once, writes `'R'` with its cut (finding 20), and every later move but `end()` is refused RUN-REFUSED; if they complete, the run waits at the first read-once declaration and the read-once `'N'` events are emitted there when the record closes. Their operations precede every `'T'` and are not charged to a tick budget. (b) rejected. A refused session's end record is finding 10's, still open: ruled before draft 11 or named open in it. RO′-2 to RO′-5, 8.3, 8.5, PP1 to PP4, counting and finding 20 are unchanged. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build.

### N2 and N3, as ruled: the compliance and the remaining work (2026-10-29)

*Added 2026-10-29, from the same message, each part unchanged.*

**His words:**

> Compliance
> I adopt the proposed tests for both rulings:
>
> * N2's exact projection and receipt.
> * END-UNDISPOSED for an accepted, undisposed arrival.
> * Verifier rejection when the named missing port is not the first empty one.
> * The plant detecting `end()` projected as `end 0 closed`.
> * N3's prefix refusal before arrival acceptance.
> * Byte-identical histories and identical `input-log-sha256` from two hosts given the same law and arrivals.
> * No `N` before the record closes after a completed prefix.
> * The plant detecting a host that delays prefix execution until record closure.
>
> Remaining work
> N2 and N3 are ruled. Finding 10 remains open as identified. The record-filling and record-closing mechanics, and the relationship between tick 1 and record closure, remain outside these rulings.
> Before Draft 11, the remaining work is:
>
> 1. Resolve Finding 10, or explicitly carry it as open.
> 2. Write and run the S1–S7 byte-layout probe. Its measured results—not a semantic ruling—must establish the required evidence.
>
> Nothing is implemented, pinned, committed, or authorized for publication.

**What it fixes:** the 1a tests put to him for N2 and N3, both plants included. Before draft 11: finding 10 ruled or carried open, and the S1-S7 byte-layout probe written and run, its measured results the evidence.

### Finding 10: a refused session's end record (2026-10-29)

*Added 2026-10-29. The question was the twin's first review's finding 10 (`twin-r7/DISPOSITION.md`, row 10), as put to
him in the session. His answer, whole and unchanged.*

**The question.** When a session's run has refused and the host then calls `end()`, what the projected log ends with: (a) `end <n> closed`; (b) a new cause, `end <n> refused`; (c) no end record, the log ending with the last record that ran; with the verifier's checks against the history.

**His words:**

> I adopt Finding 10 (c): a refused session's projected log has no end record. I also adopt the verifier checks as specified.
> Finding 10 — Refused-session end record
> Adopted: (c)
> When the host calls `end()` after the run has refused, the projection appends nothing to the log.
> The log ends with the last record that actually ran:
>
> * The refused tick's record, if refusal occurred during a tick.
> * The header alone if refusal occurred before any tick and the read-once record did not close.
> * The header and `once` line only if the read-once record closed whole.
>
> Options (a) and (b) are rejected.
> Status and refusal evidence
> The log does not assert that a refusal occurred. Execution derives the refusal.
> Running the log produces:
>
> * `status REFUSED <CODE> <clause>`;
> * `ticks` including the refused tick, if applicable;
> * unread count 0;
> * the corresponding `R` event with its cut.
>
> The receipt carries the status. The execution produces `R`. Neither is duplicated in the log.
> Verifier obligations
> I adopt all three checks:
>
> 1. The history reaches a refusal, followed by `end()`.
> 2. The log is exactly the history's projection: closed tick records, the `once` line only if the record closed whole, and no end record.
> 3. Running the log produces the same receipt core and refusal location as the live run.
>
> A log with an appended end record, a record after the refused tick, or a refusal at a different operation must fail verification with the history-mismatch verdict.
> The fact that a refused session's log can have the same bytes as a session still open at that point is accepted. The session record, `orlog-session 0`, records whether `end()` occurred; the log is not a substitute for that history.
> Examples and compliance
> I adopt both examples as stated:
>
> * N3 prefix refusal: three header lines; running them yields `REFUSED DIVISION-BY-ZERO 1`, zero ticks, and an `R` cut at clause 1.
> * Tick refusal: the header, `once` line, and records for ticks 1 and 2; running them yields the refusal at the same operation, with two ticks.
>
> I adopt all compliance tests and mutation plants, including rejection of:
>
> * `end 0 closed` for a read-once law refused before record closure;
> * a fabricated `refused` end cause;
> * a verifier accepting a log whose execution refuses somewhere other than the history.
>
> Scope
> Finding 10 is ruled. N2, N3, and Finding 20 remain unchanged.
> The S1–S7 byte-layout probe remains outstanding empirical work. It must be written and run; this ruling supplies no substitute evidence.
> Nothing is implemented, pinned, committed, or authorized for publication.

**What it fixes,** and nothing more:
- **Finding 10 (c):** the projection of an `end()` after a refusal appends nothing; the log ends with the refused tick's record, or the header alone, or the header and the `once` line if the record closed whole. (a) and (b) rejected.
- The log asserts no refusal: running it gives `status REFUSED <CODE> <clause>`, `ticks` counting the refused tick, the unread count 0, and `'R'` with its cut.
- The verifier checks that the history reaches a refusal then `end()`, that the log is exactly its projection (no end record), and that running the log gives the live run's receipt core and refusal place; otherwise the history-mismatch verdict. Whether `end()` happened is the session record's, never the log's.
- The examples, tests and plants put to him are adopted. N2, N3 and finding 20 are unchanged; the S1-S7 byte probe stays owed. Nothing is implemented, pinned or committed.

**Its re-reads:** stated in draft 11 and re-read whole before the build; its affected clauses are computed by `ar_compute.py` before that re-read.

### Re-read 9's five questions (2026-10-29)

*Added 2026-10-29 by his answers to the five questions of R7's ninth re-read (`twin-r7/REREAD-9-REPORT.md`; proposed in
`twin-r7/REREAD-9-DISPOSITION.md`): S15.5-1, S15.3-1, S15.1-1, S15.5-2 and S15.9-1, each put to him with options and a
recommendation. His answer, whole and unchanged.*

**His words:**

> I accept all five recommendations, with one important qualification on S15.9: Draft 2 is the candidate byte grammar to test, not an already-adopted or frozen format. The version-1 reference must validate it during the containment step before the exact candidate digest can be pinned.
> The five dispositions are:
> 1. S15.5-1 — ACCEPT. Correct the fixed-value example to `580000000300000000`, representing fixed 3 under RUNTIME-SPEC §5. The encoding rule itself does not change.
> 2. S15.3-1 — ACCEPT. Each `N` event is emitted at its own port declaration as execution reaches it. Do not group read-once events at the first declaration. This preserves RO′-3 and replay ordering.
> 3. S15.1-1 — ACCEPT. The optional budget portion is omitted from the law line when there is no budget. There is no budget value of zero encoded in the law. This follows R5 and avoids two byte representations for the same law.
> 4. S15.5-2 — ACCEPT. A law with read-once ports but no tick block cannot have tick records. A `t` line is refused as `LOG-RECORD`. The permitted end records remain `end 0 closed` and the applicable stop record. This closes the one-shot log ambiguity without introducing a new record type.
> 5. S15.9-1 — ACCEPT, subject to the qualification above. The pinned decoding rule must identify the exact byte grammar it decodes. Use Draft 2 as the candidate and test S1–S7 against the actual version-1 reference during containment. If the reference does not support the candidate, resolve the discrepancy before pinning. This is a prerequisite for pinning, not a declaration that the general format freeze has occurred.
> Scope and next steps
>
> * Apply these five dispositions and the nine drafting fixes in Draft 12.
> * Keep the two genuinely open items open: law-line `<type>` spelling and prefix execution for a law without read-once ports.
> * Keep the version-1 runtime's log-refusal exit code open for the 1b specification.
> * Record the F20.4/S6 dated note in `CUT-SCHEMA.md`.
> * Preserve the stand-in-only qualification on the existing S1–S7 measurement. It is not a substitute for the actual version-1 containment test.
>
> Then have the twin re-read Draft 12. I recommend another whole-draft re-read because Draft 12 changes settled semantics and the byte grammar, not merely editorial wording.
> No implementation, digest pinning, commit, or publication is authorized by these dispositions.

**What it fixes,** and nothing more:
- **S15.5-1:** the fixed number 3 is `580000000300000000` under RUNTIME-SPEC §5; T1's example is corrected, its rule
  unchanged.
- **S15.3-1:** each read-once `'N'` is emitted at its own declaration as execution reaches it, never grouped at the
  first; RO′-3 and replay's ordering are kept.
- **S15.1-1:** with no budget, the law line omits its budget part (R5's form); no budget of zero is encoded.
- **S15.5-2:** a law with read-once ports and no tick block has no tick records; a `t` line is refused LOG-RECORD; its
  end records are `end 0 closed` and the stop's.
- **S15.9-1:** the pinned decoding rule identifies the exact byte grammar it decodes. Draft 2 is the candidate to test,
  not an adopted or frozen format; the version-1 reference tests S1 to S7 against it during the containment step, and a
  discrepancy is resolved before the pin. The general format freeze (P6) has not occurred.
- The re-read's seven drafting fixes and two open items are accepted; the 1b runtime's exit code on a refused log stays
  open; CUT-SCHEMA gains a dated S6 note; the stand-in measurement keeps its grade. He recommends a whole-draft re-read
  of draft 12. Nothing is implemented, pinned, committed or published by it.

**Its re-reads:** draft 12 states it, its affected clauses are computed by `ar_compute.py` before the re-read, and the
twin reads the whole of draft 12.

### Re-read 10's question: `close()` in a law with no tick block (2026-10-29)

*Added 2026-10-29 by his answer to the question of R7's tenth re-read (`twin-r7/REREAD-10-REPORT.md`, S15.3-1; proposed
in `twin-r7/REREAD-10-DISPOSITION.md`): the open A2 table's `close()` runs a tick when "every each-tick port is
filled", which holds vacuously in a law with no each-tick port. His answer, whole and unchanged.*

**His words:**

> I adopt option (a): refuse `close()` in a law with no tick block.
> A one-shot law has no tick phase. The fact that it has zero each-tick ports must not make the condition “every each-tick port is filled” vacuously authorize a tick.
> The rule should be explicit:
>
> * If the law has no tick block, `close()` does not run a tick.
> * It must not emit a `t` record.
> * It must not create a log that its own loader rejects under the adopted one-shot rule.
> * The existing one-shot completion and stop behavior remains unchanged.
>
> Scope: This settles S15.3-1. It does not decide the remaining open A2 session mechanics for laws that do have a tick block.
> The four drafting fixes and the 1a specification item can proceed as proposed. For Draft 13, I agree that a targeted re-read of changed clauses and their affected clauses is sufficient, provided the twin checks the cross-section consistency with the one-shot log and close rules. Publication remains deferred until that disposition.

**What it fixes,** and nothing more: in a law with no tick block, `close()` is refused; it runs no tick, emits no `t`
record, and never makes a log its own loader refuses; a one-shot law's completion and stop are unchanged. The rest of
A2's session mechanics for a law with a tick block stays open. The four drafting fixes and the 1a item are accepted; the
re-read of draft 13 is targeted (its changed clauses and their affected clauses), and the twin checks the consistency
across sections of the one-shot log and `close()` rules. Publication stays deferred until that disposition.

**Its re-reads:** draft 13 states it; its affected clauses are computed by `ar_compute.py` before the targeted re-read.

## Before 1b: the backends

### R8. Float ports
| option | entails | design |
|---|---|---|
| a. Allowed | the door converts decimal text to binary64 (correctly rounded, noted) or takes the bits; a NaN is refused at the door | floats meet inputs before any second host has measured them |
| **b. Deferred** | v1 ports are Int, Fix, Bool and Text; Float ports wait for HOST-0 and for fork 3 (floats in identity) | the owner's "pays twice" argument favours a sealed fixed-point dialect for simulation. Floats across hosts are NOT_MEASURED, and flush-to-zero is not checked (DOCTRINE T5) |

**Recommended: b.**

### R9. A budget per tick
| option | entails | design |
|---|---|---|
| a. None in the law | every tick ends anyway (bounded loops, no recursion), and the host's budget stops a session without a verdict (STOPPED-BY-HOST) | the host's stop is not the law's verdict, so a slow tick is never a refusal |
| **b. Optional in the law:** `Each tick, at most N operations, do the following.` | a tick past N refuses TICK-BUDGET: an event in the trace, at the same operation on every execution, because operations are counted, not timed | the owner's measure: "a tick that exceeds its budget produces a signed refusal event, never an overrun". The budget is in the law, so the seal covers it |

**Recommended: b.** **Falsifier:** a tick over its budget that runs on, or whose refusal comes at a different
operation in two executions.

### R10. What an input log is bound to
| option | entails | design |
|---|---|---|
| **a. The port signature** (names, types, kinds, order; its sha256 in the log's header) | an edited law with the same ports replays an old log; a different signature is refused PORT-SIGNATURE | alignment: an edit's preview runs the candidate law over the world's own log. That is EDIT-0's preview and the App Studio's cheap exploration |
| b. The law seal | every edit invalidates every log | strict, but no edit could ever be previewed against a recorded session |

**Recommended: a.** **Falsifier:** a log replayed against a law whose ports differ, without a refusal.

### R11. Build identity by the law
The skeptic's step: pass the text seal to the compiled program at run time instead of compiling it in, so that editing
a note stops rebuilding both compiled backends (1.71 s measured). It changes `orl_init`'s arguments, which 1b changes
anyway for the input log's path, so the two changes become one revision of the runtime contract. **Recommended: yes, in
1b.** **Falsifier:** a note edit that rebuilds a backend, or a receipt whose text seal differs from the reference's.

### R12. RUN-1's admission record (DOCTRINE §9, fork 8)
Proposed record:
- **Trigger:** all five uses need input, and none is reachable from a closed program (the architect and the skeptic
  independently).
- **Discriminator:**
  - COMPAT-0 HELD after 1a and after 1b;
  - a recorded 1,000-tick log gives byte-identical receipt 1 on all four executions;
  - each plant caught: a dropped `'N'` event, located at its first divergent event; a backend that parses decimal
    input; a misaligned log entry, refused rather than shifted; a tick over its budget that runs on; R6's narrow
    wording, which lets a claim that depends on a port only through state read GROUNDED; R6's present trigger, which
    misses a tick block with no port; licensing by clause position;
  - **the court one-sided.** RUN-1's floor (R6) only withholds. Measure it as `tests/court_monotone.py` measures R8:
    over COMPAT-0's frozen texts and its own fixtures, no standing may be gained in any of the three orders (support
    with CIRCULAR, grounding, held), every changed reading must be counted, and two plants must be caught: a comparator
    blind to CIRCULAR, and a court that grants (the reporting pass's finding 12 replaced a plant that read the
    measurement backwards). The licence grants by design, so it is held instead by its own rows above.
    *(Noted 2026-10-26, by his R6 ruling.)* No line of COMPAT-0's frozen texts has a port or a tick block
    (`probe-spellings.txt`), so over them this measure reads 0 changed by construction, as R8's reads 0 of 65
    (`research/compat-status.md`). That half checks only that the trigger never fires without a log. The withholding
    is held by R6's own fixtures alone, run with the witness made agreed and each beside its control.
- **Scope:** `src/`, `rt_c/`, `rt_rs/`, `tests/`, SPEC §15, a RUNTIME-SPEC section for v1, a new
  `vectors/input-vectors.txt`. `runtime-vectors.txt` is untouched.
- **Exit:** the discriminator met; the twin's round settled; the self-test green twice and byte-identical.

**Recommended: approve as written.**

## Defaults, stated so they can be overruled

- **D1. Dense records.** Every tick record holds every each-tick port. The door may accept a sparse convenience form,
  but it writes the log dense.
- **D2. The tick number is not visible to the law.** A law that needs it counts ticks itself, so no new expression is
  added.
- **D3. No end-of-session block.** A run completes when its log ends.
- **D4. OUTPUT-TOO-LONG per tick**, 2^30 bytes, not per run: SPEC §7's total would end any long session.
- **D5. Binding a port counts 0 operations**, as reading a variable does.
- **D6. State.** Persistent state is the top-level variables declared before the tick block. The tick block opens a
  scope, as every block does (SPEC §5), so its own Lets are made afresh each tick.
- **D7. Not in v1:** list ports; clock, random and file ports. Randomness is a seeded read-once port and a PRNG written
  in the law. Also not in v1: a pull-style input statement, which would break alignment.
- **D8. Claims.** A claim in the tick block is evaluated each tick, and the court reads it as "true in n of n" over the
  session. A claim before the tick block is evaluated once.
  *Refined 2026-10-26 by the claims ruling (above): "true in n of n" stays as description; the claim's standing is
  E2, settled by the meet.*
- **D9. The log's source.** Input values arrive as strings, never as JSON numbers, since an i64 above 2^53 does not
  survive a JavaScript client. The door reads one JSON object per tick and writes `orlog-inputs 0`.
- **D10. Two commits.** 1a holds the reference and SPEC §15, with COMPAT-0 green; until 1b, the court reads v1 runs as
  REFERENCE-ONLY and holds no claim. 1b holds the backends, the runtimes and the input vectors.
  *Refined 2026-10-26 by the finding-24 ruling (above): its court clause governs real court readings of version-1
  runs; R6's rows, the PREFIX row and their controls run in 1a's reference with the agreed witness configured, each
  saying its agreement is configured, not measured. The two-commit split stays a default.*

## What this sheet does not decide

- Snapshots, sessions and the test socket (SNAP-1, SESSION-0, RPC-0): later rungs, which RUN-1's formats are shaped to
  serve.
- Distribution: networked play, a remote ledger, a listener reachable from another machine.
- Whether a log can ground a claim: R6 keeps it from doing so in RUN-1.
- Anything about intent. A port declares what a law reads, not what its author meant the world to be.
