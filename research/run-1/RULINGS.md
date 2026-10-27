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
then the closure table's Perform row, and finding 6, read-once ports: A′, as RO′-1 to RO′-6 (2026-10-27).

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
