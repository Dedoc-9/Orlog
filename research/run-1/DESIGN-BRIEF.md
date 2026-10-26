# RUN-1: a design brief for review (2026-10-26, at 5e49b18)

This brief gathers what RUN-1 has ruled, what it has not, and where the plan needs hardening, for a reviewer reading it
beside the repository. Nothing in it is built. Its source of truth is `research/run-1/RULINGS.md` at 5e49b18; where the
two differ, the sheet wins.

How to read it:
- **Quoted text is verbatim.** Text in a block quote, or in italics inside quotation marks, is copied from the sheet or
  from the record it names: the owner's words, or the sheet's own text.
- **Everything else is this session's reading**, model output, graded where it claims anything: MEASURED (run here,
  output below or in the file named), ESTABLISHED (read in the code or the records, not run), DECLARED (argued, not
  checked).
- **An outside review is paraphrased**, never quoted.

## 1. What RUN-1 is

> RUN-1 gives a program declared input ports and a tick block, and records every input as an event in the trace. It is
> the roadmap's fourth rung, after COMPAT-0 (built, b85df56), HOST-0 and these rulings
> (`research/roadmap-debate/VERDICT.md`). Every one of the five uses (a game or reality engine, a language, an API, an
> editing interface, tools for testing) needs it, and none can be reached from today's closed programs. It is also the
> hardest thing to add later: it fixes the next receipt, the next trace and the shape of every API built after it.

Fixed whatever is ruled (the sheet, verbatim):

> - **COMPAT-0 must hold.** Every text v0 accepted keeps its law bytes and its run. RUN-1's forms are therefore spelled
>   only where v0 refuses SYNTAX at the statement itself, so they take no meaning away from an existing text.
> - **No word is newly reserved.** fall.orl names its loop variable `tick`, and COMPAT-0's plant reserve-tick shows that
>   reserving the word would break it.

The theorems it rests on (the sheet, verbatim; graded there: *"These are DECLARED. The arbiter would MEASURE replay per
session, four ways."*):

| theorem | what it says | what would falsify it |
|---|---|---|
| **Replay** | every value from outside becomes an event before it is read, so a run is a function of the law and its input log alone, and the trace head commits to both | a recorded log whose receipt differs between two runs, or between two of the four executions |
| **Alignment** | inputs are addressed by (tick, port), never by the order a law happens to read them, so an edited law re-runs over an old log tick for tick | a law edited outside its port declarations that reads an old log out of step (a plant: a misaligned entry, which must be refused, not shifted) |
| **Tick termination** | every loop is bounded and there is no recursion, so every tick ends | a tick that does not end: impossible by construction, held by SPEC's bounds |
| **Capability** | a law reads only the ports it declares | a port read that is not declared, refused at compile time |

## 2. The rulings so far (all 2026-10-26)

### R3. How input text becomes a value: a, the conversion rule (against the recommendation)

> *"I rule in favor of Option a (The Conversion Rule) for R3."*

> *"The true, structural differentiator is reversibility under COMPAT-0 and the preservation of data provenance."*
> Option a *"treats rounding as a client-side capability rather than an engine-side compromise."*

The door's grammar, in his words:

> *"The entrance tool filters all incoming port streams using a restrictive ASCII regular expression sieve. This occurs
> before passing strings to Python's Fraction constructor, neutralizing format exploitation"*

> - *"Double-Bounded Range Checks: The door must explicitly validate that the parsed value sits securely within the
>   strict raw storage parameters of the `Fix` bounds (`MIN_FIX_RAW` and `MAX_FIX_RAW`), actively protecting the lower
>   negative boundary against floor overflow errors down to −2147483648.5."*
> - *"Integer Port Restrictions: An incoming string hitting a port explicitly typed as `an integer` must fail instantly
>   if a fraction or decimal component is detected. Truncation or automatic floor-rounding at the gate is blocked."*
> - *"Boolean Uniqueness: Truth-value channels accept exactly one invariant string spelling for `true` and one for
>   `false`. Alternative representations, case variations, or numeric bits (`1`/`0`) are refused."*
> - *"Text Byte Purity: String inputs are preserved byte-for-byte as sent. Non-NFC unicode payloads generate an explicit
>   report note; CP1252 character maps are rejected outright."*
> - *"Raw Value Spellings & Neighbor Refusals: Raw hexadecimal scalar strings are given an isolated syntactic prefix
>   that the text grammar tracks separately from standard base-10 decimals. When a user input is rejected for
>   non-alignment with the 2^-32 fixed-point grid, the door's refusal message must explicitly compute and output the
>   two nearest valid representable grid coordinates to the client."*

The sheet's reading of the bound: `-2147483648` is accepted (raw −2^63), and `-2147483648.5` is refused.

### R4. What a refusal does in a run with ticks: a, at tick granularity

> *"I rule R4 as written in your proposed ruling text: (a) at tick granularity, with automatic continuation deferred
> until SNAP-1, and the refused branch permanently sealed and queryable."*

The text he ruled:

> R4: a, at tick granularity. A refusal ends its branch at tick t. The session may continue on a new branch from tick
> t−1, rebuilt by replay from the nearest checked snapshot and checked against the tick line's state digest, reading
> tick t by a declared continuation rule written into the log. The refused branch is kept, sealed and queryable. The
> court reads each branch on its own and names every abandoned branch. Automatic continuation waits for SNAP-1; until
> then a refusal ends the session.

The design under it, from the sheet's table: a rollback that runs on *"erases the refutation: the court would read
"true in n of n" for ever. A rolled-back refusal is a laundered verdict"*.

### R5. Versions and headers: as written, with four amendments; two choices fixed

The text as written:

> - `orlog-law 1`, only when a v1 form appears, so v0 laws stay byte-identical. It adds the law lines
>   `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`.
> - `orlog-trace-1`: `head0 = SHA-256("orlog-trace-1" || law_seal)`. New events: `'T'`, the tick number (u64); `'N'`, a
>   port's value (u32 var and the value encoding of RUNTIME-SPEC §5). Each tick emits `'T'`, then one `'N'` per
>   each-tick port in declaration order, then the body. The read-once ports' `'N'` events come before the first `'T'`.
> - `orlog-receipt 1` adds `ticks <n>` and `input-log-sha256 <hex>`. It replaces `output-sha256` with `output-chain
>   <hex>`, where out_t = SHA-256(out_{t−1} || SHA-256(the output of tick t)). A snapshot then carries the output as one
>   hash; a plain running SHA-256 would need a hash midstate, which CPython's hashlib cannot export.

His ruling: *"I rule `R5` as written, augmented by your four explicit amendments"*. The amendments, as the sheet
records them:
1. `'T'`'s payload is the tick and the operation count (u64, u64).
2. The output chain's start and edges: out_0, the output written before the first tick, and a refused tick's partial
   output. His words on the last: *"if a tick encounters a transactional refusal, its partial output is formally hashed
   into the chain before the rollback logic clears the volatile state"*.
3. `ticks <n>` at a refusal counts the ticks begun, and a refused tick writes no per-tick line.
4. The receipt frame check is versioned. His words: *"The arbiter must accept both `orlog-receipt 0` and
   `orlog-receipt 1` formats depending on the code path. To keep this defensive, we implement the requested inverse
   plants: a `v1` receipt checked under a `v0` template must fail, and a `v0` payload evaluated under `v1` rules must be
   caught and refused."* Confirmed the same day, in the reading the sheet records: *"Tying the receipt frame check
   strictly to the law's own header (`orlog-law 0` demands `orlog-receipt 0`, and `orlog-law 1` demands
   `orlog-receipt 1`) is the only sound option."*

The two choices fixed now:
- *"We include this artifact now within the `1a` specification. Do not defer it to a later version."* The artifact is
  the per-tick line, `orlog-ticks 0`: the tick, events, ops, output bytes, the trace head, the output chain, a claims
  digest and a state digest (`research/speed/VERDICT.md`).
- *"We keep the per-event chain exactly as written instead of switching to a compressed stream head."* His reason:
  losing event-level localization *"destroys our core epistemic edge"*, and *"The safety margin of the per-event chain
  is worth the processing cost."*

### R6. What the input log is to the court: a, data never a channel; b a later fork

> *"I rule Option a (Data, never a channel) for `RUN-1`. The primary principle is unyielding: replayable data is not
> admissible testimony."*

> *"`Option b` stays held as a later potential fork for a future court update."*

Option a, as the sheet's table states it:

> in a run with an input log (the law declares a port, or has a tick block), no claim is GROUNDED, whatever its channel
> and whatever is ratified, except under the licence below; the court shows the log's seal as provenance: "rests on
> input log <seal>, unratified"

The licence, PREFIX, as the sheet states it: *"a claim is exempt only if every evaluation of it precedes the first
input."*

What he ruled with it:
- **R1's cost sentence:** *"Moving a world property out of the law and into a read-once port means the cost of rule a
  reaches every later claim in the run, stripping them of grounding even if they never touch that property
  directly."*
- **One seal:** *"The court's generated provenance output line must print exactly the `input-log-sha256` value defined
  in `receipt 1`."*
- **No vacuous row:** *"Every row testing an ungrounded port violation must run with the witness explicitly configured
  as agreed"*, and *"Each test row is structurally paired with an internal control variant. The control evaluates the
  exact same claim without an active log declaration, or wraps it securely within the `PREFIX` license parameters. The
  control must return a clean `GROUNDED` standing"*.
- **A PREFIX claim past a later refusal:** *"A claim wrapped within the `PREFIX` license parameters that evaluated true
  remains historically held, regardless of whether the execution loop encounters a subsequent transactional refusal
  downstream."* His reason: *"a downstream failure on frame t cannot retrospectively invalidate a pure, law-bound proof
  that completed before the timeline even initiated."*

## 3. The one-way doors

A choice is a one-way door when recorded logs, receipts or laws will carry its bytes: changing it later is a new
version, and every earlier record stays in the old one. A two-way door can be widened later without breaking a record.
This sorting is this session's reading (DECLARED).

| choice | what it fixes | state | door |
|---|---|---|---|
| R2, the spellings | the words of every law with ports or ticks | open | one-way: a law written with them is frozen text |
| R3, the door | which input text a log can hold | ruled a | one-way toward strictness: the sheet allows relaxing later (refused becoming accepted), never the reverse |
| R4, a refusal | what the record holds of a refused tick and branch | ruled a | one-way |
| R5, the formats | `orlog-law 1`, `orlog-trace-1`, `orlog-receipt 1`, `orlog-ticks 0` | ruled | one-way |
| R6, the court | a reading, which records nothing | ruled a | two-way: b, or a backward slice, may widen it later |
| R8, float ports | the port types | open (recommended b, deferred) | two-way: adding floats later is an extension |
| R9, a tick budget | `budget <N>` in the law's bytes, and the refusal's place | open | one-way |
| R10, the log's binding | the port signature's sha256 in the log's header | open | one-way |
| R11, build identity | `orl_init`'s arguments | open | two-way: an internal runtime contract |
| D1, D3, D9, the log | dense records; the end of a run; `orlog-inputs 0`, strings never JSON numbers | defaults | one-way |
| the speed verdict's "log as a stream with an end record" | what ends a run (D3) | proposed, unruled | one-way |

**What this says about order:** the one-way doors still open are R2, R9, R10 and the log's form (D1, D3, D9 and the
speed verdict's end record). They fix bytes every session will carry, so they deserve the hardest review before 1a.
R6 was the one ruled choice that stays reversible.

## 4. Hardening: what this session found or carries forward

Each item has a grade, what it does not show, and how it would be falsified.

### H1. The compiled-program cache trusts the compiler's word about itself (an outside review's finding 1)

An outside review of `main`, static and not run, found this. Its finding, paraphrased: the cache key holds the
compiler's first `--version` line, the flags and the source, so two different compiler binaries reporting the same
line share a cached program. The review proposed a stronger identity (the resolved path, a digest of the binary) and
a row with two wrapper compilers that report one version line.

- **ESTABLISHED by reading**, not run: `src/orlog/arbiter.py`, `toolchain` (lines 66–81), the key (line 160) and the
  record check (lines 183–188). A cached program is reused when its record's toolchain line and its own sha256 match.
  Neither names the compiler binary.
- **It reaches further than the review says.** The linker, the C headers and the runtime libraries are in no key at
  all. `rustc --version` names its commit; `clang --version`'s first line names only a version.
- **What it means for the claims.** The toolchain the witness names is the compiler's own word (DECLARED). A stale
  program from another compiler would still run and agree, so four-way agreement would be measured for a compiler the
  record does not name.
- **Proposed repair, in 1b with R11, since both revise the runtime contract.**
  - The key and the record take the whole version output, the resolved path and the executable's sha256.
  - A row: two stand-in compilers that report one version line and build different programs must miss the cache.
  - Its plant: a key of the first line alone.
- **Does not show:** that any cached run so far was built by another compiler. **Falsifier:** a cache hit across two
  compiler binaries after the repair.

### H2. The door and the parser classify an indented `Note:` or `Title:` line differently (the review's finding 2)

The review found that the canonicalizer's `_context_marker` strips leading spaces before it looks for `Note:` and
`Title:`, while the parser accepts them only at column one.

**MEASURED here.** The probe runs each text through `compile_bytes` (`src/orlog/front.py`); the probe's script is in
the session's scratch folder, not the tree.

| text (line 2) | the door's events | verdict |
|---|---|---|
| `Note: plain` | none | ACCEPTED |
| `  Note: plain` (indented) | none | REFUSED LINE-FORM at line 2 |
| `Note: café` (not NFC) | REPAIR R-NFC | ACCEPTED |
| `  Note: café` (indented) | REPAIR R-NFC | REFUSED LINE-FORM at line 2 |
| `Note: 300 K` with U+212A KELVIN SIGN | REPAIR R-NFC | ACCEPTED |
| `  Note: 300 K` with U+212A (indented) | REPAIR R-NFC | REFUSED LINE-FORM at line 2 |
| a clause with U+212A (control) | REFUSE NON-ASCII-CODE | REFUSED NON-ASCII-CODE |
| `  Title: T.` (line 1, indented) | none | REFUSED LINE-FORM at line 1 |
| an indented clause (control) | none | REFUSED LINE-FORM at line 2 |

- **No acceptance bypass.** Every indented case is refused. But the door's report says it repaired, as free text, a
  line the parser then refused as no form at all. For U+212A it reports an NFC repair where code would refuse
  NON-ASCII-CODE (red team E17).
- **Indentation is illegal everywhere.** The parser refuses an indented clause too, so the repair is the door's: read
  the marker at column one, as the parser does.
- **The repair changes no frozen verdict. MEASURED here:** 0 of COMPAT-0's 3,361 frozen texts has any line that begins
  with a space or a tab. That is also a coverage gap: the corpus never exercises indentation.
- **For RUN-1.** R2 adds line forms. Every line form should be classified the same by the door and the parser, held by
  a row for each form and a plant that splits them.
- **Falsifier:** a line the door reads as free text that the parser reads otherwise.

### H3. R3's neighbour refusal fails at the ends of Fix's range

**MEASURED here** (exact fractions against `numeric_ref.I64_MIN` and `I64_MAX`). His ruling requires *"the two nearest
valid representable grid coordinates"*. At each end of the range only one exists:
- `-2147483648.0000000001` lies between raw −2^63−1 (not an i64) and raw −2^63;
- `2147483647.9999999999` lies between raw 2^63−1 and raw 2^63 (not an i64).

§15 must say what the refusal names there, and which refusal wins when a value is both off the grid and out of range.
**Falsifier:** a §15 text that settles both, worked by hand at both ends.

### H4. What `'T'`'s operation count is

ESTABLISHED by reading the sheet. `'T'` is emitted before its tick's body runs, so it cannot carry that tick's own
count. The speed debate wrote *"the operation count at the boundary"* (`research/speed/PROPONENT-R2.md`). That leaves two
readings, the running total so far or the previous tick's own count, for §15 and R7's round.

### H5. The per-tick line's state digest has a cost

DECLARED. A state digest is linear in the state each tick, and a digest every k ticks names only the window a silent
write fell in. 1a's specification must choose, and say what the window does not show.

### H6. R1 b and R6 a together

Recorded on the sheet with his sentence (section 2). If R1 b is ruled, every claim evaluated after a read-once port is
read loses grounding in RUN-1, including claims that never touch the property.

### H7. R6's rows would pass vacuously in 1a without his riders

ESTABLISHED by reading `src/orlog/court.py`, `panel`: GROUNDED needs held, held needs the backends agreed, and D10 reads
every v1 run REFERENCE-ONLY until 1b. His two riders close this. Proposed with them, not ruled: the tightest control is
the same run read with R6's fence off, as `panel` takes `r8`, since a control without the log is another law with
another claim seal.

### H8. The scope of the PREFIX settlement

ESTABLISHED by reasoning from the licence's definition. Every evaluation of a PREFIX claim precedes the first input, so
a refusal at a tick cuts off none of them, and his reason holds. A refusal inside the prefix, before the first input,
can cut evaluations off: a PREFIX claim in a loop, refused between two evaluations, reads "true in 1 of 1". That is the
closed run's case, and it stays open.

### H9. The frozen corpus proves no regression, never coverage

MEASURED here and in the records. COMPAT-0's 3,361 texts exercise:
- none of R8's class (0 of 65 claims, `research/compat-status.md`);
- none of R6, by construction (no text has a port or a tick block, `probe-spellings.txt`);
- no indented line (H2).

Each floor is held by its own fixtures alone. R12's note records this for R6.

### H10. The input door has one author

DECLARED. No runtime parses decimal text, so the door is written once, in Python. Nothing re-derives it but
hand-worked probes. The twin imports `numeric_ref.py` (AGENTS.md permits it), so if the conversion lives there, the
twin's agreement on it is shared code. Proposed for R7: the round hand-works the door's probes from §15 alone. Every
author is one model family, so agreement shows consistency, never truth.

### H11. R9 b is unsafe as written for a live outcome

MEASURED by the speed debate and rerun by its judge (P12), quoted from `research/speed/VERDICT.md`: *"It is unsafe as
written for a live outcome: a shared lowering defect moves when a match ends, the compiled executions agreeing and only
the reference dissenting"*. Its three conditions are DECLARED there and must be ruled with R9: ops committed per tick
(ruled into R5), the reference as the live watcher, and no refusal declared before the watcher confirms it.

## 5. The outside review's other points

- **The court's repair for DP-5 (its R8).** The review found it has the right shape: a named failure, a minimal witness,
  an expected reading, and a plant that disables the guard. It proposed keeping that shape as the model for future
  guards. R12 already asks it of R6.
- **Ragnarök.** The review agreed with the verdict not to build the proposal as written, and to keep only a bounded
  refutation search used by a prosecutor, admitted only with a trigger. The verdict, verbatim:
  *"**Do not build the proposal as written.**"* and *"**Admit it later, if ever, and only with a trigger.**"*
  (`research/ragnarok/VERDICT.md`).
- **Its own limit, which it stated:** it did not run the self-test.

## 6. Still open, for the owner

- RUN-1's rulings R1, R2, R7 to R12 and the defaults D1 to D10.
- The speed verdict's unruled proposals: the reconciler's rule, the log as a stream with an end record, a port range at
  the door, R9 b's conditions, complete snapshots, R13 (what a live outcome is), R14 (a play build without the chain),
  and its "should" items.
- The reporting pass's other question: what a law's own refusal exits with (`run` and `court` both exit 0 today).
- Whether a claim that held stays held after a refusal before the first input, and in every closed run (H8).
- H1 and H2's repairs: neither is made.
- HOST-0 (a second machine), Ragnarök's instrument, prosecutor F42 (home paths in 16 records under `court/`).

## 7. What this brief does not show

- That any rule here is correct: the rulings are the owner's choices, and the theorems are DECLARED.
- Any measurement of RUN-1, which is not built.
- That the outside review saw the same tree: it read `main` on GitHub, and its line numbers for `syntax.py` differ from
  the tree's (the parser's check is at lines 186–188 of `src/orlog/syntax.py` at 5e49b18).
