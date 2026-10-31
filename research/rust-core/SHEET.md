# RUST-CORE-0: an independent core that runs `orlog-law 0`. A milestone sheet (2026-10-30)

**Status.** A preregistered milestone sheet. It is not a ruling, and it authorizes no implementation: nothing it names
is written until the owner accepts it. *[Note, 2026-10-31, REREAD-8's ZC5, adopted by his ruling on the ruling sheet:
since Amendment 1 his rulings, not this status line, say what is authorized, and none authorizes implementation]* It
rests on his ruling 3 of 2026-10-30 (recorded whole in
[research/law-sufficiency/RULINGS.md](../law-sufficiency/RULINGS.md)):

> *"Authorize a Rust-core milestone with its own preregistered sheet, predictions, tests, and acceptance criteria. This
> authorizes the milestone's design and experimental planning, not immediate production implementation or
> integration."*

It touches no gate, no release, no `src/`, `tests/` or `vectors/` file, and no part of version 1's path. Ruling 4 stands
throughout: *"The Python interpreter remains the reference authority."*

## 1. What the core is, and is not

**It is** a std-only Rust program, built by bare `rustc` (`AGENTS.md`: no Cargo, no crate). It reads a law's bytes in
`orlog-law 0` and runs them as SPEC §6–§7 and RUNTIME-SPEC §2–§8 define, writing the output, the receipt and, if asked,
the trace, as a backend program does. It is a second, independent reading of version 0's execution, of the kind the
twin and the runtimes are of their parts.

**It is not:**
- an authority: its agreement is evidence about the reference, never a vote over it (ruling 4);
- a generator: it does not take the generated Rust backend's place, and `gen_rs.py` and `rt_rs/` stay as they are;
- a version-1 engine: ports, the tick block and the read-once record wait for §15 and the pin;
- the prose printer (ruling 5).

## 2. The boundary and its inputs

| | the core receives | why |
|---|---|---|
| the law | the law bytes, exactly: `orlog-law 0`, the decimals line, one `(clause …)` line per clause | ruling 1's contract |
| the text seal | 64 hex characters, passed by the caller | the receipt prints it, and the law bytes do not hold it (LAW-SUFFICIENCY-0, test 2) |
| a budget | optional, counted operations | the reference's host stop: no receipt and no event, at the first statement past the budget (`interp.py:31-39`). *[Note, 2026-10-31, REREAD-8's ZC5, adopted by his ruling on the ruling sheet: the budget's form and its outcome are fixed by Amendments 1 and 2 and LAW-FORMAT-0's section 5, which govern]* |
| paths | output, receipt, and an optional trace | the generated programs' interface (RUNTIME-SPEC §6), so that the arbiter's `run` could drive it unchanged |

**What it writes.** The receipt of RUNTIME-SPEC §7, with the backend line `backend rust-core`. The trace and the event
chain are those of RUNTIME-SPEC §5. On a host stop, no receipt, and one line on stderr naming the operations counted and
the budget.

**What it computes.** The law seal: the sha256 of the bytes it read. It never takes the seal on trust.

**What it refuses.** Bytes that are not well-formed law bytes, refused with a load code before anything runs. It
accepts only bytes it would write itself: decoding then re-encoding must give the bytes back. What "well-formed" means
is D3's question.

## 3. Phase 0, owed before any core: LAW-FORMAT-0, the format's written obligations

Ruling 2 requires the format to make explicit what the Python analysis now does implicitly. LAW-FORMAT-0 is that
document, and it is the core's specification for the law bytes. It states:
- the grammar of the bytes, with the string escapes and the float bits;
- each of the 15 run-side derivations and the 3 backend-only ones (LAW-SUFFICIENCY-0's test 1, LAW-SUFFICIENCY-1's
  E3); *[Note, 2026-10-31, REREAD-8's ZC5, adopted by his ruling on the ruling sheet: LAW-FORMAT-0 states 19 derivations
  (its section 6), and its count governs]*
- the clause order of a rule's definitions, for provisos and then values (SPEC §6; E2);
- exact reconstruction, the round trip;
- the well-formedness the core must check (D3).

Each obligation names the test that holds it. An independent re-read in the manner of R7 checks the document, and its
findings are disposed before phase 1. It is written in `research/rust-core/`. Whether it later joins RUNTIME-SPEC is
the owner's to rule.

## 4. Design choices, each the owner's

| | choice | what each way entails | recommended |
|---|---|---|---|
| D1 | who writes the core, and from what | (a) a clean-room author: an isolated agent given only a manifest of LAW-FORMAT-0, SPEC.md, RUNTIME-SPEC.md and `vectors/runtime-vectors.txt`, each by sha256, and never `src/`, `rt_rs/`, `rt_c/`, `twin/` or the decoders. Agreement is then evidence of more than shared code, though not of more than one model family (README, *Independence*). (b) The core reuses `rt_rs/orlog_rt.rs`'s arithmetic and SHA-256: faster to build, but any shared defect moves the core and the Rust backend together | (a) |
| D2 | Float | (a) host binary64, as the runtimes do (Rust `f64`, canonical NaN), held to the vectors. (b) A software binary64 that shares no FPU path: slower, and it answers Track B's question, not this one | (a), with (b) left to Track B |
| D3 | what the core checks on the bytes | (a) the grammar alone. (b) The grammar and every derivation succeeding: types consistent, every variable declared before use, ids dense, every override target a define of the same name, the claim and must ids dense. Under (b), any bytes it accepts are the image of a typed law, so a run of untrusted bytes cannot meet a state the front end would have refused | (b) |
| D4 | where it lives | (a) `research/rust-core/`, off the gate. (b) A top-level `rt_core/` beside `rt_rs/` | (a) until a ruling moves it |
| D5 | its name in the receipt | `backend rust-core` | as written; P drops the line, so it decides no comparison |

## 5. Phases

0. **LAW-FORMAT-0**, re-read and disposed (section 3).
1. **The core**, written by the author D1 chooses. The author records the reading set by sha256, as `rt_rs/NOTES.md`
   does.
2. **Conformance**: section 6's predictions, run twice, with the evidence in `evidence/rust-core-*.txt`.
3. **Beside the arbiter, off the gate.** A research harness runs the reference, the three backends and the core on the
   corpus and the 298 texts, with the arbiter's own `build` and `run`, and localizes any dissent to its first divergent
   event. The arbiter's verdict logic is not changed. The core is never one of its four executions.
4. **The findings, and the decisions they bring back.**

## 6. Predictions, fixed now

Each runs on LAW-SUFFICIENCY's 298 texts (the 290 accepted COMPAT-0 texts and the 8 fixtures) unless it says
otherwise. P is the receipt without its `backend` and `text-seal` lines (LAW-SUFFICIENCY-0).

| | prediction | falsifier |
|---|---|---|
| R1 | the core's arithmetic meets `RUNTIME VECTORS 20015 / 20015`, built with `-O` and without | any line differs |
| R2 | it re-encodes the law bytes it read exactly, on every text | one byte differs |
| R3 | its P equals the reference's P on every text | any text whose P differs |
| R4 | its trace equals the reference's line for line on every text | the first differing line, named |
| R5 | under a budget of half each text's operations (texts of 2 operations or more), it stops where the reference stops: same count, no receipt | a different count, or a receipt |
| R6 | on 10,000 mutated law byte strings (bytes flipped, lines truncated, clauses swapped, ids changed; seed fixed), it either refuses with a load code, or accepts exactly the bytes it would write and runs them with the same P as the reference interpreter running decoder1's decoding. It never panics, never hangs past the budget, never reads past its input | a panic, a hang, an accepted non-canonical form, or a P unlike the decoded reference's |
| R7 | every planted defect in the core is caught, by R1, R3 or R4, at the event where it was planted | a plant that passes |
| R8 | beside the arbiter (phase 3), on the corpus: the core agrees with the reference wherever the three backends do, and a defect planted in the reference reads as dissent against both the backends and the core | a disagreement, or a planted reference defect the core misses |

**Plants, in copies of the core, never in its source:**
- a Fix rounding (ties away from even);
- a Float NaN not canonical;
- an event's payload encoding (a u32 written little-endian);
- the rule order (definitions taken in reverse);
- a claim's cost read without `cost_tracked`;
- a budget checked after the statement, not before;
- a decoder accepting a non-canonical number (`(lit int 07)`).

R7 requires each to be caught. One that is not is reported, and measured as equivalent where it is.

**Measured, not predicted.** The core's operations per second against the reference interpreter and the compiled
backends, on the corpus. These are software timings, labelled as such, with the clock's step stated. No frame rate or
latency is claimed.

### Amendment 1: the comparison protocol, fixed before any experiment (2026-10-30, the owner's ruling B1)

This amendment is written before any core exists and before any of R1–R8 has run, as his third correction requires:
*"The time limit, repeat count, and classification rules must be written into the sheet before experiments begin."*
It narrows R3, R5 and R6. It adds stress evidence, and changes nothing else.

**The time limits** are wall-clock and enforced by the harness, never by the core, which reads no clock.

| | limit |
|---|---|
| each reference run (the Python interpreter, or `decoder1` with the interpreter) | 60 seconds |
| each core run | 60 seconds |
| each build of the core | 600 seconds |

**The repeat count.** Each case runs twice: the reference twice, the core twice. A case's class is decided by both
runs.

**The reference's classes** for each case:

| class | when |
|---|---|
| RESULT | both runs end within the limit and give the same result: the receipt projection P (or the stop's operation count, under a budget) and the trace |
| NO REFERENCE RESULT | both runs crash (Python's `RecursionError` among them) or both time out |
| UNSTABLE | anything else: one result and one crash or timeout, two different results, or a crash and a timeout |

**The core's outcomes** for each case. The harness classifies each by the exit status and stderr that section 10 of
LAW-FORMAT-0 defines, and by what it observes from outside:
- the language outcomes: completed and refused (exit 0, with a receipt), and stopped by the budget (exit 4, no
  receipt);
- the format's outcome: load-refused (exit 3);
- the operational outcomes:
  - usage or I/O error (exit 2);
  - **detected resource exhaustion** (exit 5, `RESOURCE-EXHAUSTED: <kind>`, no receipt), which the core reports when
    an allocation it attempts with a fallible call fails;
  - **external termination**: the harness's own time limit kills the process, or the process ends by the operating
    system or any other way that gives none of the exit statuses above. The harness records which, and never expects a
    diagnostic from it.

Nothing promises that the core detects every process-level memory failure (his second correction).

**What is compared, and what is not:**
- **R3, R4, R5:** the core's language outcome is compared with the reference's only where the reference's class is
  RESULT. There, every difference in P, the trace or the stop's count is a disagreement.
- **NO REFERENCE RESULT and UNSTABLE** are counted and listed, and are neither passes nor failures of R3–R5. The core's
  outcomes on them are kept as stress evidence. Agreement or disagreement is never claimed there.
- **An operational outcome is never a semantic disagreement.** That covers detected exhaustion, external termination,
  and usage and I/O errors. On a case where the reference's class is RESULT, it is reported as such and counted
  against R3–R5's coverage, not their agreement.
- **R6** still records, for every mutant, refused or accepted. An accepted mutant is compared as above, with decoder1
  and the interpreter as its reference.

**Stress evidence** (new; predicted, and run with the rest):

| | prediction | falsifier |
|---|---|---|
| S1 | deep nesting: perform chains and rule chains of 300, 600, 3,000 and 30,000, built from texts the front end accepts. The core completes each, within the time limit and without exhaustion. At 300, where the reference's class is RESULT, its P and trace equal the reference's | a crash, a detected exhaustion or external termination at any of these depths, or a difference at 300 |
| S2 | explosive work: doubling rule chains of 18 and 24 under budgets of 10 and of none, and of 64 with none. At 18 and 24 the core stops (budget 10) or completes (no budget) as the reference does, where the reference's class is RESULT. At 64 the reference's class is expected to be NO REFERENCE RESULT, and the core's outcome is recorded as stress evidence only | a stop at another count than the reference's where the reference has a RESULT, or any outcome at 64 reported as a semantic result |
| S3 | budget boundaries: for each of the 298 texts and each B from 0 to its operation count, by a fixed sample of 20 values of B per text (seed 20261030), the core stops exactly where the reference stops, at the same statement and the same count | any differing stop |
| S4 | separation: no operational outcome is ever printed or recorded as a receipt, a refusal code or a budget stop | any such record |

### Amendment 2: core faults, the reference as shipped, and S3's values (2026-10-30, the owner's rulings C1(a) and C2(a))

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his answers to
REREAD-2's two questions (recorded whole in [RULINGS.md](RULINGS.md)). Where it and Amendment 1 differ, it governs.
Amendment 1 stays as written.

**The reference's runs** *[C2(a)]*. Each reference run is one fresh `python -B` process, with:
- `PYTHONHASHSEED=0`;
- Python's default recursion limit and thread stack;
- no import of `format_check` or of any module that changes either.

Each run records the exact Python implementation and version, and the operating system and its release. In his words:
*"Do not raise the recursion limit to manufacture reference results."* The classes are Amendment 1's, read as he put
them:
- RESULT needs both runs;
- *"A reference crash or timeout must reproduce in both runs to qualify as no reference result"*;
- *"Inconsistent reference outcomes are unstable."*

**The core's classes** *[C1(a)]*. The harness puts every run of the core in exactly one of these. They replace the core
outcome list of Amendment 1.

| class | when | what it counts as |
|---|---|---|
| COMPLETED, REFUSED | exit 0, a receipt, files and stderr as LAW-FORMAT-0 section 10's row says | a language outcome, compared |
| STOPPED | exit 4, the stop's stderr line, no receipt | a language outcome (the budget), compared |
| LOAD-REFUSED | exit 3, the `LAW-REFUSED` line, no file | the format's outcome |
| USAGE-ERROR, IO-ERROR | exit 2, its stderr prefix | operational |
| RESOURCE-EXHAUSTED | exit 5, the `RESOURCE-EXHAUSTED: <kind>` line, no receipt: an allocation the core made by a fallible call failed, and the core said so | operational: recognized resource exhaustion |
| EXTERNAL-TERMINATION | the harness's own 60-second limit killed the run; or the run ended by an act the harness attributes to the host, on evidence it records with the case (an operating system's record of a kill, say) | operational |
| CORE-FAULT | any other end. That includes an exit status no row gives (a panic's 101, say), a stack overflow or abort, and any end the harness neither caused nor can attribute to the host by recorded evidence. It also includes an end whose files or stderr contradict its row: exit 0 without a receipt, a receipt after exit 4 or 5, or a stderr line that is not its row's | **fails the prediction being tested** |
| UNSTABLE-CORE | the core's two runs of one case differ in class or in result | **fails the prediction being tested** |

In his words: *"An unknown exit status, panic, stack overflow, or other unexpected core termination is a core fault,
not an unlisted operational outcome."* External termination is never relabeled: *"External termination, such as an OS
kill, must not be relabeled as a successful resource-handling result."* Nor is it ever relabeled RESOURCE-EXHAUSTED.

**What counts:**
- **Coverage.** On every case whose reference class is RESULT, the core must give a comparable result: COMPLETED,
  REFUSED or STOPPED, compared as R3–R5 say. A LOAD-REFUSED where the reference read the law is a disagreement. Any
  operational outcome there fails the prediction as a **coverage failure**, never as a semantic disagreement. So R3–R5
  hold only at full coverage.
- **No pass for stopping.** No outcome counts toward agreement but a compared language outcome on a RESULT case. In his
  words: *"it must never award a pass merely because execution stopped."*
- **Elsewhere.** On a case whose reference class is NO-REFERENCE-RESULT or UNSTABLE, the core's class is recorded as
  stress evidence. A CORE-FAULT or UNSTABLE-CORE there still fails the prediction under test (S1, S2).

**R6, its third sentence and falsifier** *[C2(a)]*. "It never panics, never hangs past the budget, never reads past its
input" is replaced by: *it never ends in CORE-FAULT or UNSTABLE-CORE, it never reads past its input, and where the
reference's class is RESULT it never exceeds the 60-second core execution limit.* The falsifier "a panic, a hang" reads
"a CORE-FAULT, an UNSTABLE-CORE, or EXTERNAL-TERMINATION where the reference's class is RESULT". Outside RESULT, a run
the limit ends is recorded as EXTERNAL-TERMINATION and is never a pass. In his words: *"The 60-second core limit is an
experimental safeguard, not a language budget or a semantic timeout."*

**S3's values and their procedure** *[C2(a)]*. In his words: *"Write S3's exact budget-sampling values and procedure
into the sheet before testing."*
- **The texts:** the 298, sorted by id in Python's string order.
- **Each text's reference run:** under its own budget (COMPAT-0's: corpus 10,000,000, fixture 1,000,000, mutant
  1,000,000, probe 1,000,000), twice, as above, each under the 60-second limit. Its class is decided by both runs.
- **For a RESULT text:** let ops be the count its run reports (the receipt's `ops`, or the stop's count), and max =
  min(ops, budget).
  - When max + 1 ≤ 20, the values are every B from 0 to max.
  - Otherwise they are `sorted(rng.sample(range(max + 1), 20))`, where `rng = random.Random(20261030)` is one generator,
    drawn through the RESULT texts in that order.
- **For a text of any other class:** it is listed with both runs' outcomes, and draws nothing.

The cap at the budget keeps every sampled run within the text's own budgeted run: the first check where ops > B never
comes later than the first where ops > budget, when B ≤ budget.

**The values** are the file `research/rust-core/s3-budgets.txt`, sha256
`86f3a7b08f6713b240b3705fdf5fe3abb93b4d75de104fad7c5e194c4bb578bd`, part of this amendment. They were produced by
`research/rust-core/gen_s3_budgets.py` (sha256 `adb50cf0…`), run twice with identical bytes. Every one of the 298 texts
is RESULT (237 completed, 61 refused, none stopped under its budget), and there are 2,100 values in all. The file's
header records the generator's and the reference's sha256 and the environment each run reported: CPython 3.14.5,
recursion limit 1,000, `format_check` not imported, Windows 11. S3 runs exactly these
values. The experiment never draws them again, so they do not depend on any later Python's `random`.

**The evidence records** *[his further requirement]*. In his words: *"preserve the distinction between no reference
result, unstable, core fault, recognized resource exhaustion, and external termination in the evidence records. They
must not collapse into a generic failure category."*
- Every case's record names the reference's class (RESULT, NO-REFERENCE-RESULT, UNSTABLE) and the core's class for each
  run, by the words of the table above, with the evidence for it: the exit status, the stderr line, the files written,
  and for EXTERNAL-TERMINATION what the harness did or what it recorded of the host.
- Every summary gives each class a count of its own.
- No record or summary puts "failed", "error" or "crash" in place of one of these words.

### Amendment 3: R5, R6, S1, S2 and the do-nothing fixtures fixed; a crash's reproduction; no host evidence on Windows (2026-10-30, the owner's rulings E2 and E3(a))

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his answers to
REREAD-3's questions E2 and E3, and the dispositions J12–J15 he adopted with them (recorded whole in
[RULINGS.md](RULINGS.md)). Where it and Amendments 1 and 2 differ, it governs. They stay as written. Its rule over every
comparison, in his words: *"Keep reference refusals, reference crashes, core faults, and operational outcomes distinct.
None may be silently converted into a successful comparison."*

**One taxonomy** *[J12]*. LAW-FORMAT-0 draft 4 and this sheet now name the outcomes alike:
- **The core's classes are of one run:** COMPLETED, REFUSED, STOPPED, LOAD-REFUSED, USAGE-ERROR, IO-ERROR,
  RESOURCE-EXHAUSTED, EXTERNAL-TERMINATION, CORE-FAULT.
- **UNSTABLE-CORE is a class of a case,** not of a run: the core's two runs of the case differ in class or in result. It
  fails the prediction under test.
- **The compared outcomes are COMPLETED, REFUSED and STOPPED.** STOPPED is the host's budget, not a language outcome,
  and it is compared all the same. Amendment 2's table gives STOPPED as *"a language outcome (the budget), compared"*;
  read it as "the host's budget, not a language outcome; compared". Its sentence *"No outcome counts toward agreement but
  a compared language outcome on a RESULT case"* reads: no outcome counts toward agreement but a compared outcome
  (COMPLETED, REFUSED or STOPPED) on a RESULT case, with an equal result.

**The reference's classes** *[E2]*. They replace Amendment 1's table, read with Amendment 2:

| class | when |
|---|---|
| RESULT | both runs end within the limit and give the same result: the receipt projection P (or the stop's count) and the trace |
| REFERENCE-REFUSED | R6 only: both runs end in decoder1's own refusal, its `DecodeError`, with the same message |
| NO-REFERENCE-RESULT | both runs crash with the same exit status and the same exception type, or both time out |
| UNSTABLE | anything else: one result and one crash or timeout, two different results, a crash and a timeout, or two crashes that differ in exit status or in exception type |

- **A crash's exception type** is the text before the first `:` of the last line the run wrote to stderr that is not
  empty (Python names the exception there: `RecursionError`), or `none` when the run wrote nothing there. In his words:
  *"A reference crash counts as reproducible only when both fresh reference runs have the same exit status and exception
  type. Otherwise classify it as unstable, not as an established absence of a reference result."*
- **`s3-budgets.txt` stays as Amendment 2 fixed it.** No S3 text crashed: all 298 are RESULT, which is the same under
  either rule. `gen_s3_budgets.py`'s `classify`, which takes any two crashes as one, made that record and classifies no
  experiment.
- **Outside R6** every text is one the front end accepts, checked when its values were fixed, so REFERENCE-REFUSED does
  not arise there.

**Every run's record** *[J13, J14]*:
- **A fresh folder.** Each run of the core, and each reference run, has a fresh empty folder made for it. The harness
  records the folder's listing (each file's name, length and sha256) before the run, where it must be empty, and after.
  It runs nothing in a folder that is not empty, and reads the core's class from the files that run wrote alone. So no
  run is scored by another run's files.
- **The environment** is recorded by each run's own process: `platform.platform()`, and for the reference the Python
  implementation and version, its recursion limit, and that `format_check` is not imported.
- **R8 is the exception.** Phase 3 runs the reference as the arbiter ships it: the arbiter runs the interpreter in its own
  process (`arbiter.py`), not a fresh one. R8's reference conditions are those, and its records say so. Amendment 2's
  fresh-process rule governs R1–R7 and S1–S4.

**R5** *[E2, J2]*. R5's row reads:

| | prediction | falsifier |
|---|---|---|
| R5 | under B = ⌊ops / 2⌋ for each text of 2 operations or more, where ops is the count of its RESULT run under its own budget (the values in `r5-budgets.txt`), the core gives the reference's class and result at that B: STOPPED with the same count and trace, or COMPLETED or REFUSED with the same P and trace | where the reference's class at that B is RESULT, a different class, or a different count, P or trace; anywhere, a CORE-FAULT or an UNSTABLE-CORE |

In his words: *"Compare outcome classes, not an assumed universal STOPPED result. If the reference completes at a sampled
budget, a comparable core completion is valid."* The reference is run again at each B, twice, and its class there
decides, as everywhere.

**R6** *[E2, J3]*. The mutants are a file, fixed now, never drawn again. In his words: *"Freeze the 10,000 mutants.
Identify `decoder1.py` by exact path and SHA-256."*
- **The mutants:** 10,000 distinct byte strings, none of them one of the 298 laws, 2,500 from each operator in this
  order:
  - flip one bit of one byte;
  - cut one line short;
  - exchange the rests of two clause lines;
  - change one id by one.

  They are made by one `random.Random(20261031)` from the law bytes of the 298 texts, as the generator's docstring
  states. A mutant equal to a source or to an earlier mutant was drawn again; the file's header counts those draws.
- **The reference** for a mutant is decoder1, `research/law-sufficiency/decoder1.py`, sha256
  `3584f565f6929879c3d942a45b3fa8d5c09cc2382b67772559109e38930ab877`, run by the interpreter. Each run is a fresh
  process as Amendment 2 says, under the mutant budget, 1,000,000 (COMPAT-0's), and the 60-second limit. The core runs
  each mutant under `--budget 1000000`.
- **The outcomes,** per mutant:

| the reference's class | the core's class | what it counts as |
|---|---|---|
| REFERENCE-REFUSED | LOAD-REFUSED | agreement: both refuse |
| REFERENCE-REFUSED | COMPLETED, REFUSED or STOPPED | **a falsifier**: the core accepts a mutant the reference refuses |
| REFERENCE-REFUSED | any other class | **fails**: not the refusal the prediction requires |
| RESULT | LOAD-REFUSED | recorded "refused", as his condition 3 allows; never counted as agreement on P |
| RESULT | COMPLETED, REFUSED or STOPPED | compared as R3–R5: an equal result agrees, any other is a disagreement |
| RESULT | an operational outcome | a coverage failure |
| NO-REFERENCE-RESULT or UNSTABLE | any | recorded as stress evidence, never a pass; an acceptance there is recorded as one |
| any | CORE-FAULT, or the case UNSTABLE-CORE | **fails** |

- **R6's falsifier** reads:
  - a CORE-FAULT or an UNSTABLE-CORE;
  - on a REFERENCE-REFUSED mutant, any class but LOAD-REFUSED;
  - on a RESULT mutant, an operational outcome or a result unlike the decoded reference's;
  - an accepted non-canonical form.
- **The checker's verdicts** on the 10,000 are recorded beside them, as evidence only: `evidence/rust-core-r6-checker.txt`,
  sha256 `4365d26bab665dfc1921e143788bc45cf4af835962e767865d308e8f87ac32e2`. It accepts 538, refuses 9,462, and crashes on
  none. A mutant the core accepts and the checker refuses is listed for the owner, and decides nothing: the checker is
  evidence, not authority.

**S1, S2 and the do-nothing fixtures** *[E2, J4, J15]*. Their texts are fixed now, each by its sha256 and the sha256 of
the law bytes the front end writes for it. In his words: *"S1/S2: Freeze the texts. For S1, any outcome other than
completion with the constructed operation count fails."*
- **S1's falsifier** reads: at any depth, any class but COMPLETED, or an output or count other than the constructed one
  (a chain of n says `1` and counts n + 1 operations); at 300, where the reference's class is RESULT, a P or trace unlike
  the reference's. The constructions were held to the reference at 300 when the texts were fixed. Each chain completed,
  saying `1`, with 301 operations.
- **S2's texts** are REREAD-1's doubling chains of 18, 24 and 64. Each is followed by `Say 2.`, which lets a budget of
  10 stop the run at the check before it. S2's falsifier is Amendment 1's.
- **Every stress prediction's own falsifier applies whatever the reference's class.** Amendment 2's sentence that off
  RESULT only CORE-FAULT and UNSTABLE-CORE fail does not narrow S1's or S2's falsifiers *[J4]*.
- **"A crash"** in any falsifier of this sheet means CORE-FAULT *[J4]*.
- **The do-nothing fixtures** *[J15]*. Three texts, each `Say 1.` followed by a last clause that does nothing at run time:
  a procedure, a define, a decimals clause. They are run as S3 runs, at every B from 0 to their count (0 and 1). When
  they were fixed, the reference stopped after 1 operation under B = 0, at the check before the last clause, and
  completed with 1 operation under B = 1.
- **R7's new plant.** R7 gains the plant *no check before a do-nothing clause*, caught when the core completes a
  do-nothing fixture under B = 0.
- **R7's catching predictions.** R7's *"caught, by R1, R3 or R4"* reads "caught by R1, R3, R4, R5, S3 or the do-nothing
  fixtures". A budget plant can only be caught by a budget comparison: so it already was for the plant *a budget checked
  after the statement*.

**No host evidence on Windows, and exit 5 read in the source** *[E3, J5]*:
- **External termination.** Amendment 2's EXTERNAL-TERMINATION row reads: *the harness's own 60-second limit killed the
  run, as the harness records*. On Windows, the host this milestone runs on, no evidence of a host's act is admissible,
  so every end the harness did not cause is CORE-FAULT. Admitting a host's evidence on any other system needs his ruling
  first. In his words: *"No host evidence is accepted on Windows for this experiment. Any termination not caused by the
  harness is a core fault."*
- **Exit 5.** RESOURCE-EXHAUSTED counts only after a reading of the core's source, recorded with the evidence before any
  of R1–R8 or S1–S4 counts. The reading must show that exit 5 is reached only from a detected failed fallible
  allocation (the `try_reserve` family): never from a panic handler, an abort hook, or any other path. If it finds
  another path, no exit 5 is RESOURCE-EXHAUSTED: each is CORE-FAULT, and the finding goes to the owner. In his words:
  *"That last condition is a narrow classification rule, not a claim that every possible memory failure can be caught.
  An OS kill or unexplained process termination does not become `RESOURCE-EXHAUSTED` merely because memory pressure is
  suspected."*
- **The milestone's acceptance** (section 7) gains: exit 5's source reading recorded, before R1–R8 count.

**The evidence records** keep every class word above apart. That includes the reference's four classes, a reference
crash's exit status and exception type, and the case's UNSTABLE-CORE. Amendment 2's rule stands: no record puts
"failed", "error" or "crash" in place of a class word.

**The files this amendment fixes.** Each was made twice with identical bytes. Each is named here by its sha256 and is
part of this amendment:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/r5-budgets.txt` | `27b383508b5fec8e3bb4639d2cebc949684f77c288acca394043d2de70a5ffab` | `gen_r5_budgets.py` (`f7195b28…`), from `s3-budgets.txt`'s counts: no new run and no draw | 254 texts with their B; the 44 of fewer than 2 operations draw none |
| `research/rust-core/r6-mutants.txt` | `a8f704fbba7ec3bcebc662de076c0ff0b52e101479dff98618ee84880bd8e155` | `gen_r6_mutants.py` (`ae64f829…`), seed 20261031 | the 10,000 mutants whole, in hex, each with its sha256, and the 298 sources' sha256; 17,155,925 bytes |
| `research/rust-core/stress-texts.txt` | `d698ed6e7d50e9f72ed82e8eb3ab9f6ad39abccd81829d8f13027e76373bed6b` | `gen_stress_texts.py` (`4ca4d634…`) | 14 texts (S1's 8, S2's 3, the 3 fixtures) by sha256, their law bytes by sha256, and what is expected of each; `--write DIR` makes them for an experiment, each held to it |

### Amendment 4: the gates' precedence frozen; R6 adjudicated against section 8; R2b; the reference runner; the thirteen corrections (2026-10-30, the owner's rulings F1(b), F2(a) and R2b)

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his answers to
REREAD-4's questions F1 and F2, R2b, and the thirteen minor findings he accepted as wording corrections, *"provided they
do not change the adopted format rules or evidence classifications"* (recorded whole in [RULINGS.md](RULINGS.md)).
Where it and Amendments 1–3 differ, it governs. They stay as written. In his words: *"The R2b fixtures and reference
runner are research evidence infrastructure, not permission to implement the Rust core."*

**The gates' precedence, frozen for the next evidence run** *[F1]*. In his words: *"If the specification does not
determine the order, propose and freeze one explicitly before the next evidence run; do not silently treat Draft 4's
order as authoritative."*
- **The rule.** LAW-FORMAT-0 draft 5, section 8, phase 3: the failures of the three gates (depth, chains, structure)
  are collected together, and the one reported is on the least line, and on that line the least W.
- **Its derivation,** from the specification, not from draft 4: REREAD-0's adopted F8 (*"A load refusal reports the
  first failing line, and within it the lowest W."*), which no later ruling overrides among the gates. *[Corrected
  2026-10-30, REREAD-5's L1: this derivation was wrong. The E1(b) text he adopted puts the depth gate first. He then
  confirmed it (N1); Amendment 5 states the precedence, and governs. This paragraph is kept as it was written.]*
- **Frozen.** Every evidence run of this milestone uses it until he rules otherwise. The checker's records
  (`evidence/rust-core-format-5.txt`) and its verdicts on R6's mutants (`evidence/rust-core-r6-checker-5.txt`) are made
  under it.
- **Put to him.** If he rules an order, draft 5's phase 3, the checker, its precedence plants and those records change
  with it before any experiment.

**R6, adjudicated against section 8** *[F2]*. In his words: *"The checker is an evidence-selection mechanism, not the
authority deciding correctness."* Amendment 3's sentence that a mutant the core accepts and the checker refuses
*"is listed for the owner, and decides nothing"* is replaced by:
- **The comparison.** For every mutant, the core's verdict is compared with the checker's: accepted, or LOAD-REFUSED
  with W and line. The checker's verdicts are `evidence/rust-core-r6-checker-5.txt`, sha256
  `852ead1da87f878af10b60779fa8634e7cbb91d3b616103708bce4c7716df4c7`, made by draft 5's checker: 538 accepted, 0
  crashed.
- **Every mutant where they differ is adjudicated** by an independent reader: a fresh agent with no part in writing
  the core, the checker or LAW-FORMAT-0. It is given LAW-FORMAT-0's sections 2–4 and 8, the mutant's bytes, and the
  two verdicts, without being told which is the core's.
- **The record, per case,** in the reader's words *[his "Record the reader's determination and the exact applicable
  rule and diagnostic"]*:
  - the determination: the first verdict is right, the second is right, both are wrong, or section 8 does not decide;
  - the exact rule: the W, the gate or phase, and the lines of section 8 it rests on;
  - the diagnostic section 8 gives: accepted, or W and line.
- **What each determination counts as.** A core found wrong fails R6. A checker found wrong is a checker finding; it
  changes no verdict of the core. Where section 8 does not decide, the case goes to the owner as a format finding, and
  counts for nothing until he rules.
- **"An accepted non-canonical form"**, in R6's falsifier, is decided this way and no other: a mutant the core accepts
  and the checker refuses is read like any other disagreement.
- **Checker agreement is never proof.** In his words: *"Do not count checker agreement as proof that the core is
  correct when both could share the same defect."* Where the core and the checker agree, the record says that the two
  readings agree, never that the core is correct. Every R6 claim of agreement names what it does not show: a defect
  both share.
- **Unchanged:** the rest of R6 stands as Amendment 3 put it (the reference's classes, its outcome table, P compared
  on what both accept).

**R2b, the canonicity twins** *[R2b]*. In his words: *"For every fixture, the core must refuse with the correct W code
and line. Freeze the fixtures and expected outcomes before testing."* A new prediction:

| | prediction | falsifier |
|---|---|---|
| R2b | on each of the 1,558 canonicity twins in `r2b-twins.txt`, the core is LOAD-REFUSED with the W and the line the file gives | any other class, W or line |

- **The twins.** Each is one of the experiment's laws with exactly one non-canonical change. There are 15 kinds, in
  three groups:
  - **W1:** a leading zero in the prefix; the decimals line's word in capitals;
  - **W2:** a leading zero in an Int or Fix literal, an id or a while bound; an uppercase hex digit; a printable
    character escaped; a `\u{h}` with a leading zero or an uppercase digit; the statement's word in capitals;
  - **W3:** two spaces; a space after `(` or before `)`; `(given)` or `(over)` without its space; two spaces before
    `absorbed`.

  Each applies at its first place in each of the 181 distinct laws among the 298, as `gen_r2b_twins.py`'s docstring
  states. Nothing is drawn.
- **The expected refusals** are fixed by construction from section 8, never by a checker: a law passes every check,
  and its twin changes one line and keeps its parentheses, so the first failure is on that line, and its W is the
  kind's.
- **The checker's verdicts** are recorded beside them as evidence only: `evidence/rust-core-r2b-checker.txt`, sha256
  `89b5b886884306eb09f77754f7618c9141441cca2c0187f7cf7f11cebb145d0c`. It agrees on 1,558 of 1,558, which shows the
  construction and the checker agree, and nothing more.
- **R7's catching predictions** read "R1, R2b, R3, R4, R5, R6, S3 or the do-nothing fixtures". The plant *"a decoder
  accepting a non-canonical number (`(lit int 07)`)"* is caught by R2b's `literal-zero` twins, which no other
  prediction held (K2).
- **"At the event where it was planted"** (R7): a plant that has no event, a budget plant or a decoder plant, is caught
  by its prediction's own falsifier on a case that holds its site.

**The reference runner** *[F2, K3, K15]*. In his words: *"Its classification of reference refusal versus crash must be
fixed and independently reviewable; the harness must not silently decide that distinction."*
- **The program.** Every reference run of the experiment is `research/rust-core/ref_run.py`, sha256
  `d55ce7567dc843afee32d6481be969e1b98208e399fcfdd47e3c8fe4f05f4392`, in a fresh process:
  - the texts go through the front end;
  - R6's mutants go through decoder1 (`research/law-sufficiency/decoder1.py`, sha256 `3584f565…`), with the text seal
    64 zeros (the core is given the same) and the mutant budget, 1,000,000.
- **Its line between a refusal and a crash,** fixed in its code:
  - decoder1's `DecodeError`, caught only where `decode` is called, prints `DECODER-REFUSED <ascii(str(e))>` and exits
    0. That printed message is what REFERENCE-REFUSED compares;
  - any other exception, anywhere, prints its traceback, then as the last line on stderr `REFERENCE-EXCEPTION
    <module>.<qualname>`, and exits 1. The line is written by the runner's own top-level handler, never parsed from a
    traceback.
- **The classes from two runs** are its function `classify`. A harness calls it and decides nothing itself:

  | class | when |
  |---|---|
  | RESULT | two equal `RUN …` lines |
  | REFERENCE-REFUSED | two equal `DECODER-REFUSED …` lines |
  | NO-REFERENCE-RESULT | two crashes with the same exit status and the same type, the type read from the `REFERENCE-EXCEPTION` line, or `none` where there is none; or two timeouts |
  | UNSTABLE | anything else |

- **It replaces** Amendment 3's rule for a crash's exception type (the text before the first `:` of the last line on
  stderr) *[K15]*.
- **The record.** The reference's class on each of R6's mutants, by this runner, two fresh runs each, is
  `research/rust-core/r6-reference.txt`:
  - RESULT 2,374;
  - REFERENCE-REFUSED 6,994;
  - NO-REFERENCE-RESULT 632, crashes repeated alike in both runs: `UnicodeDecodeError` 326, `ValueError` 119,
    `KeyError` 117, `RecursionError` 43, `TypeError` 19, `IndexError` 4, `struct.error` 3, `AttributeError` 1;
  - UNSTABLE none.

  It is a record of what the reference did when the mutants were fixed, so that R6's power is known. The experiment
  runs the reference again, twice, and its own runs decide. On the 632, a core that accepts a mutant is only recorded
  by the reference's classes; the adjudication above decides it against section 8 wherever the checker refuses it.

**The thirteen corrections, as they bear on the protocol** *[K7–K15]*:
- **S2** *[K7]*. Its falsifier reads like R5's. Under each budget, where the reference's class is RESULT, the core
  gives the reference's class and result: STOPPED with the same count and trace, or COMPLETED with the same P and trace.
  At 64, any outcome reported as a semantic result fails. Anywhere, a CORE-FAULT or UNSTABLE-CORE fails.
- **A run's result,** for UNSTABLE-CORE, is by its class, as LAW-FORMAT-0 draft 5's section 10 states *[K9]*. It
  changes no class. *[Corrected 2026-10-30, REREAD-5's L12 and REREAD-6's M9: "changes no class" could not be
  shown. The definition decided cases the earlier text left undefined, and he confirmed that reading (N3); Amendment 5
  states it.]*
- **stdout** *[K10]*. CORE-FAULT's row reads "an end whose files, stderr or stdout contradict its row", and anything
  on stdout does. Every run's record includes what the run wrote to stdout.
- **The run's folder** *[K11]*. LAW lies outside it. The working directory is the folder, and OUT, RECEIPT and TRACE
  are names in it.
- **R8's conditions for the core** *[K12]*. They are the arbiter's as shipped: its `run`, its 600-second timeout, and
  its removal of stale files. A core run the arbiter stops at its 600 s is recorded in R8's records as
  EXTERNAL-TERMINATION: a coverage failure where the reference has a result, never a dissent and never agreement.
- **Exit 5's reading** is made by an independent reader, as LAW-FORMAT-0 draft 5's section 0 states *[K13]*.
- **An interrupted experiment** *[K14]*. The harness starts the core in a process group of its own (on Windows,
  `CREATE_NEW_PROCESS_GROUP`), so that a console's interrupt does not reach it. If the experiment itself is interrupted,
  the whole run of the experiment is void and is run again from the start. No single case's run is ever voided.
- **The stress manifest** *[K16]*. `stress-texts-2.txt` replaces `stress-texts.txt`. It holds the same 14 texts, each
  with the same sha256, and its note on `s2-doubling-64` reads as S2 does: stress evidence only.

**The files this amendment fixes.** Each generated file was made twice with identical bytes. Each is named here by its
sha256 and is part of this amendment:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/ref_run.py` | `d55ce7567dc843afee32d6481be969e1b98208e399fcfdd47e3c8fe4f05f4392` | written | the reference runner and `classify` |
| `research/rust-core/r6-reference.txt` | `255477ca49720938567c768bace98884f89a827b1ca1a28c39c0be3b0fa8ff40` | `gen_r6_reference.py` (`3e99443c…`) | the reference's class on each of R6's 10,000 mutants, by the runner |
| `research/rust-core/r2b-twins.txt` | `ef204d4d050da730ca97b2af2d5edfbfde540cc7dfb372655cc0720f543a979f` | `gen_r2b_twins.py` (`a3fc89d4…`) | 1,558 twins, each with its expected refusal |
| `research/rust-core/stress-texts-2.txt` | `ea542dd1d4693cf7f0c0ff1c914ef0fa3178118b7c52085be2af5e27a6dacc87` | `gen_stress_texts.py` (`2c3787a1…`) | Amendment 3's 14 texts, unchanged, with the note on doubling 64 corrected |

### Amendment 5: the gates' precedence as E1(b) gives it; R2 observed by write-back; N3's three readings; the runner's faults (2026-10-30, the owner's rulings N1(a), N2(a) and N3)

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his answers to
REREAD-5's questions N1, N2 and N3, and the ten minor findings he accepted *"as mechanical wording, test and runner
corrections, provided they do not alter adopted semantics or classifications"* (recorded whole in
[RULINGS.md](RULINGS.md)). Where it and Amendments 1–4 differ, it governs. They stay as written. In his words: *"These
dispositions preserve the earlier rulings; they do not authorize implementation or change the language's semantics."*

**The gates' precedence** *[N1]*. It replaces Amendment 4's frozen rule, whose derivation was wrong (REREAD-5's L1;
Amendment 4 carries a note in place). In his words: *"The adopted E1(b) wording already establishes this precedence"*;
*"F1 did not supersede E1(b)."*
1. **The depth gate first.** If any clause fails W14(a) or (b), the least such line is reported as W14, and no
   W4–W13 check is made.
2. **Then the chain and structure gates together.** The least line among their failures is reported, and on it the
   lowest W.
3. **Then the walk,** only after both.

Every evidence run of this milestone uses it. The checker's records (`evidence/rust-core-format-6.txt`) and its
verdicts on R6's mutants (`evidence/rust-core-r6-checker-6.txt`, sha256
`6031e11f1a1a6cd8e4f739b02a0e85b28c24de89b272f00751e89c96062b5023`) are made under it. One verdict changed from
Amendment 4's record, from W5 to W14, as the depth gate now reports first.

**R2, observed by write-back** *[N2]*. R2's row reads:

| | prediction | falsifier |
|---|---|---|
| R2 | on each of the 298 texts' law bytes, `rust-core --write-back LAW OUT` (LAW-FORMAT-0 draft 6, section 10) ends WRITTEN-BACK, and OUT equals LAW byte for byte | any byte of OUT that differs; any other class, a load refusal included |

- **The write-back run's classes:**
  - WRITTEN-BACK: exit 0, OUT written, nothing on stdout or stderr. It is compared, by OUT's bytes against LAW's.
  - LOAD-REFUSED, USAGE-ERROR, IO-ERROR, RESOURCE-EXHAUSTED, EXTERNAL-TERMINATION and CORE-FAULT, as Amendment 2
    defines them.
  - UNSTABLE-CORE, for a case whose two runs differ in class or in result. A written-back run's result is OUT's
    bytes.
- **What does not count.** In his words: *"A mismatch fails the round-trip obligation. A load refusal does not count
  as a successful round trip."*
- **Kept apart.** The write-back mode is a separate command line. It writes no output, receipt or trace, and runs
  nothing. No other prediction reads it. In his words: *"Keep this separate from ordinary output, receipts and traces.
  It is an observable format obligation, not a new semantic execution path or a change of authority."*

**N3's three readings, confirmed:**
- **W5's block** *[N3, L8]*. Only the block of an If that is a clause's own statement names a clause. LAW-FORMAT-0
  draft 6 states it in W5's row, and the checker holds it with a plant. In his words: *"do not generalize it to
  arbitrary nested blocks."*
- **A run's result, by class** *[N3, L12]*. As draft 6's section 10 states it. So two runs of a case that differ only
  in a load refusal's (W, line), or only in an exhaustion kind, make the case UNSTABLE-CORE, which fails. In his words:
  *"Two runs differing only in a load-refusal line or an exhaustion kind are `UNSTABLE`, not equivalent."* The six
  kinds stay; no kind is added.
- **An interrupted experiment** *[N3, L12]*. It is discarded whole and repeated. Its runs are kept in the evidence
  record and counted there. In his words, *"never use their partial results toward acceptance."*

**The adjudicator's reading set** *[L2]*. Amendment 4's R6 adjudicator is given the whole of the exact LAW-FORMAT-0
draft the core was built from, named by sha256, not sections 2–4 and 8 alone. The adjudicator decides against section
8 as that draft states it, with every section section 8 rests on.

**The runner, corrected** *[L3, L5]*. The reference runner is now `research/rust-core/ref_run.py`, sha256
`33914074cfd7c0bf1ce84b0d166a97b0e9baacd1e57b3a05affe50ee33828a18`:
- **`classify` reads raw runs.** It takes each run as the process gave it: (exit status, stdout bytes, stderr bytes),
  or TIMEOUT. It reads their lines itself (CR LF as LF, the last line that is not empty), so no harness extracts
  anything.
- **A runner fault is never a reference class.** The runner checks its own arguments before anything runs:
  - BUDGET is `none` or a canonical decimal;
  - TEXTSEAL is 64 lowercase hex digits;
  - the input can be read.

  A fault of its own prints `RUNNER-FAULT <reason>` as its last line on stderr and exits 3. That covers a bad argument,
  an unreadable input, decoder1 holding a plant, an interrupt, or a text the front end refuses. `classify` raises on
  it.
- **When a runner fault occurs,** the experiment stops, and it is discarded whole and repeated, as an interrupted one
  is: its runs are kept and counted, and never used toward acceptance.
- **A `SystemExit` inside the reference** is a crash like any other, `REFERENCE-EXCEPTION builtins.SystemExit`, exit 1.
- **Its check.** `research/rust-core/ref_run_paths.py` (sha256
  `e1edf642de6c547e865e0bc88d7be8b135b4efa45bfd447aa4c8e6c34887b87c`) runs every way the runner ends, each twice in
  fresh processes, through `classify`, and requires the class, the exit status and, for a crash, the type. Its record
  is `evidence/rust-core-ref-run-paths.txt`, 25 of 25 as stated.
- **The test it passes, and one it would have failed.** A copy of the runner held in memory, with the old `except
  SystemExit: raise` restored, fails it at "decode calls sys.exit(0)": it ends 0, not 1 (MEASURED, once, outside the
  record).
- **The record remade.** The reference's class on each of R6's mutants was made again with this runner, twice:
  `research/rust-core/r6-reference-2.txt`, sha256 `e2483cf52d9016e07241a8be8e4dcf451349f181af3574585676add04cd9c6e1`. Amendment 4's `r6-reference.txt` is kept as
  its record. Its rows are those of Amendment 4's record, every
  one (MEASURED: the two made twice with identical bytes, and their rows compared), as predicted, since no mutant's run meets a
  fault of the runner. Only its header changed: the runner's and the generator's sha256.

**R8's exceptions** *[L13]*. R8 runs beside the arbiter, by the arbiter's own build and run (section 5, phase 3). So:
- R8's reference is the arbiter's own, not `ref_run.py`;
- its core runs under the arbiter's `run`. The arbiter's 600-second stop is EXTERNAL-TERMINATION in R8 alone, and its
  `run` records no stdout and starts no process group.

R8's records say so for every run. Amendment 4's runner and the 60-second limit govern every other prediction.

**R7, two words** *[L7]*. R7's plants are the core's and stand as Amendments 1–4 list them. L7's three structure
plants are the checker's (LAW-FORMAT-0 draft 6, section 11), not R7's.

**The files this amendment fixes.** Each generated file was made twice with identical bytes. Each is named here by its
sha256 and is part of this amendment:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/ref_run.py` | `33914074cfd7c0bf1ce84b0d166a97b0e9baacd1e57b3a05affe50ee33828a18` | written | the reference runner and `classify`, replacing Amendment 4's |
| `research/rust-core/ref_run_paths.py` | `e1edf642de6c547e865e0bc88d7be8b135b4efa45bfd447aa4c8e6c34887b87c` | written | the runner's check |
| `research/rust-core/r6-reference-2.txt` | `e2483cf52d9016e07241a8be8e4dcf451349f181af3574585676add04cd9c6e1` | `gen_r6_reference.py` (`0a100c1e…`) | the reference's class on each of R6's mutants, by this runner, replacing Amendment 4's record |

### Amendment 6: OUT from the writer, and R7's two writer plants; the runner's faults as interruptions; the recurring-fault stop (2026-10-30, the owner's rulings U1(a) and U2)

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his answers to
REREAD-6's questions U1 and U2, and the remaining minor dispositions he accepted *"as text, test, and evidence-record
corrections, provided they preserve the existing language and outcome semantics"* (recorded whole in
[RULINGS.md](RULINGS.md)). Where it and Amendments 1–5 differ, it governs. They stay as written. In his words:
*"Authorization remains unchanged: Phase 0 only."*

**R2, against a writer that ran** *[U1]*. In his words: *"The write-back obligation must test actual serialization, not
echoing"*, and *"a successful byte comparison alone does not prove that a writer ran."*
- **OUT** is produced by the core's writer from the decoded law representation, never copied from the input bytes
  (LAW-FORMAT-0 draft 7, section 10). R2's row stands as Amendment 5 put it: OUT compared byte for byte with LAW, a
  difference or any class but WRITTEN-BACK failing it.
- **R7 gains two writer plants,** in copies of the core, never in its source. R2 must catch each through the byte
  mismatch it causes:
  - *the writer drops a name*: it writes a `let`'s name as the empty string. 154 of the 298 laws hold a `let` with a
    name, so R2 meets it there; *[Note, 2026-10-30, REREAD-7's Y15 and X9: his words were "dropping a name", and the
    adopted option's "omits a `let`'s name"; the empty string is the form this plant takes, and it reaches the same 154.
    Those are texts: 91 distinct laws. The `over` plant's 3 are 2 distinct byte strings (Amendment 7).]*
  - *the writer reverses an `(over …)` list*. 3 of the 298 laws hold an `(over …)` list of two entries or more that
    differ (`mutant/s1/0485`, `mutant/s1/2049`, `probe/twin/probes/n23-notwithstanding-four.orl`), so R2 meets it
    there.

  A core whose write-back copies its input would let both pass, so R7 fails it.
- **The provenance of OUT** is recorded by the independent source reading (LAW-FORMAT-0 draft 7, section 0): by lines,
  that OUT's bytes come from the writer, and that no path copies the bytes read into OUT. In his words: *"so the
  evidence establishes that the writer—not an input-byte copy—produced it."*
- **R7's catching predictions** read "R1, R2, R2b, R3, R4, R5, R6, S3 or the do-nothing fixtures".

**The runner's faults** *[U2]*. In his words: *"Keep runner faults distinct from reference exceptions, core faults, and
externally caused termination. The repeat rule is experimental procedure, not a new semantic outcome class."*
- **L2's and L3's corrections, as applied** in Amendment 5, are confirmed. In his words: *"A front-end refusal and an
  invalid budget argument must not be misclassified as reference crashes or successful results."*
- **A runner fault is an interruption of the whole experiment.** The experiment stops at it. Its records are retained:
  every run made, and the fault itself, by its `RUNNER-FAULT` line, its case and its run. Its partial results are never
  used toward acceptance. The whole experiment is then repeated from its start. In his words: *"Retain the records,
  discard all partial results for acceptance purposes, and repeat the whole experiment."*
- **The recurring-fault stop.** If the same runner fault occurs again on the repeat, the experiment stops, and the
  fault is brought back to him for a ruling. In his words: *"Do not keep retrying, relabel it as a reference outcome, or
  allow it to disappear into an interruption count."*
  - "The same runner fault" is one with the same `RUNNER-FAULT` line, at the same case.
  - A different runner fault on the repeat is not covered by his words. It too stops the experiment and goes to him:
    the procedure never repeats a second time on its own. *[Corrected 2026-10-30, REREAD-7's Y1: the option he adopted,
    (iii) of REREAD-6-DISPOSITION.md, covers it: "after one repetition that ends in a fault again, the experiment stops,
    and the fault goes to him. No third run". His B1 confirmed it (Amendment 7).]*
- **An interruption by any other cause** (Amendment 5, *[N3]*) is handled the same way, and its runs are retained and
  counted alike.

**The runner, corrected** *[M7]*. It is now `research/rust-core/ref_run.py`, sha256
`162d4ec776f0c02d1fdc32ff8b6cbc0a65b039511fa51d4997125a37329a0d16`:
- it holds `research/law-sufficiency/decoder1.py` to its pinned sha256, `3584f565…` (Amendment 3), before importing it.
  A mismatch, a file it cannot read, or an import failure is a runner fault;
- its check, `research/rust-core/ref_run_paths.py`, sha256
  `5f415e8493d26a43f86c747e176b6a15450e5e906a0dc2ab7ef9c8ffe03843e0`, holds it to its run conditions as well as its
  endings *[Note, 2026-10-30, REREAD-7's X3: it did not hold them all; eleven runner changes passed it. Its ENV and P
  checks were folded into the run rows rather than given a case each (Y15). Amendment 7 replaces it.]*:
  - every run that reaches the reference prints the ENV line, with a fresh interpreter's default recursion limit and
    `format_check not-imported`;
  - one run's outcome line equals the one the check computes itself, by the interpreter;
  - the runner's source reads no environment variable, sets no recursion limit and imports no `format_check`.

  Its record is `evidence/rust-core-ref-run-paths-7.txt`, 31 of 31 as stated. Each of the five runner changes REREAD-6
  showed passing the old check fails the new one: the ENV line removed, the recursion limit raised, `format_check`
  imported, P keeping the text-seal line, BUDGET read from an environment variable (MEASURED, once, outside the
  record).

**The adjudicator's reading set** *[M6]*. Amendment 5's adjudicator is given the core author's whole reading set,
each by sha256: the exact LAW-FORMAT-0 draft the core was built from, SPEC.md, RUNTIME-SPEC.md,
`vectors/runtime-vectors.txt` and `research/rust-core/vectors-as-integer.txt`. Section 8 rests on SPEC in W9, in the
promote rule and in section 7's order.

**The write-back's files** *[M5]*. A write-back run's files are judged against LAW-FORMAT-0 draft 7's write-back table,
not the run mode's. The written-back row's end (exit 0, OUT written, no receipt) is not a CORE-FAULT, as *"exit 0
without a receipt"* is in the run mode (Amendment 2).

**The records, kept current** *[M9]*:
- **The checker's verdicts** on R6's mutants are now `evidence/rust-core-r6-checker-7.txt` (sha256
  `8a47f8fc6378cf3ac02cacf84916e7c79c79d1480973420bdc030fe89680f18f`), made under draft 7's checker. 61 verdicts
  moved from Amendment 5's record, all swap mutants, each still W5 on another line, as W5's naming is now read as its
  row is written (M3).
- **Its verdicts on R2b's twins** are now `evidence/rust-core-r2b-checker-7.txt` (sha256
  `f53bed4097cf96e61f721e5d3742c6c18965e82ca7912087649e7222ff6ec54a`), agreeing on 1,558 of 1,558, as evidence only.
  *[Note, 2026-10-30, REREAD-7's Y15: M9's adopted text named `-6.txt` (`48d62f24…`), draft 6's, whose rows are the
  same; this names draft 7's instead.]*
- **The reference's record** on R6's mutants was made again with this runner, twice: `research/rust-core/r6-reference-3.txt`,
  sha256 `bbfcddb589ed272c11d51d69a0254c2ac17f499c9480f914502783f7c8a42f6a`. Its header names Amendments 4 to 6. Its rows are those of Amendment 5's record, every one (MEASURED). Its
  first generation ran beside REREAD-7's three readers (1,673 s of wall time). A second, at the same time, ended at
  17:40 when Windows could not create a process (`WinError 1450`, insufficient system resources) and wrote nothing.
  The second generation was then made alone (1,752 s), byte for byte equal to the first. Amendment 5's `r6-reference-2.txt` is kept
  as its record.
- **Amendment 4's sentence** that K9 *"changes no class"* carries a note in place.

**The files this amendment fixes.** Each generated file was made twice with identical bytes. Each is named here by its
sha256 and is part of this amendment:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/ref_run.py` | `162d4ec776f0c02d1fdc32ff8b6cbc0a65b039511fa51d4997125a37329a0d16` | written | the reference runner and `classify`, replacing Amendment 5's |
| `research/rust-core/ref_run_paths.py` | `5f415e8493d26a43f86c747e176b6a15450e5e906a0dc2ab7ef9c8ffe03843e0` | written | the runner's check, replacing Amendment 5's |
| `research/rust-core/r6-reference-3.txt` | `bbfcddb589ed272c11d51d69a0254c2ac17f499c9480f914502783f7c8a42f6a` | `gen_r6_reference.py` (`eda21973…`) | the reference's class on each of R6's mutants, by this runner |

### Amendment 7: the writer plants by the byte mismatch; the experiment and its attempts; the full acceptance list; D1 measured; the records (2026-10-30, the owner's rulings A to F on REREAD-7)

This amendment is written before any core exists and before any of R1–R8 or S1–S4 has run. It applies his rulings A
to F on REREAD-7's questions, and the DRAFT dispositions of [REREAD-7-DISPOSITION.md](REREAD-7-DISPOSITION.md) (his
ruling is recorded whole in [RULINGS.md](RULINGS.md)). Where it and Amendments 1–6 differ, it governs. They stay as
written, with notes in place where REREAD-7 found them wrong. In his words: *"They do not authorize Rust-core
implementation. Phase 0 remains the limit."*

**R2 and R7's writer plants** *[R7-A]*. In his words: *"This preserves the intended distinction: the plants test the
writer's actual behavior; the source reading establishes its provenance. Neither substitutes for the other."*
- **W3** is decided by code independent of the writer that produces OUT (LAW-FORMAT-0 draft 8, section 10).
- **A writer plant is caught only through the byte mismatch it causes.** In his words: *"A load refusal does not count
  as catching either plant."*
- **Neither writer plant may be declared equivalent.** Sections 6 and 7's route for an equivalent mutant does not
  apply to them. In his words: *"If R2 does not catch a writer plant, R7 fails and the result comes to me."*
- **The source reading** (draft 8, section 0) establishes that OUT is produced by decoding each atom to its value and
  re-encoding it under section 3, that no slice of the input bytes reaches OUT, and that W3 does not call the writer.
  It is recorded before R2's acceptance is counted. A finding of an input-byte copy path, or of a writer-dependent W3,
  fails R2 and is reported.
- **R2's write-back fixtures** (his point 6; REREAD-7's X9): `research/rust-core/r2-writeback-fixtures.txt`, made by
  `gen_r2_fixtures.py`, frozen here before any core exists. Its 11 fixtures are laws whose `over` or `given` list is out
  of order or repeats an entry *[Note, 2026-10-31, REREAD-8's ZB7, adopted by his ruling on the ruling sheet: 10 of the
  11; the first, `(given 2 1)` written as `(given 1 2)`, is in order with no repeat. The generator's docstring says the
  same and is pinned by the fixtures' header, so it stays as it is]* (none of the 298 laws holds an `over` list so). R2
  expects each written back byte for
  byte; a difference or a load refusal fails R2. The checker accepts each and writes it back exactly, as evidence only.
- **The plants' reach is of texts:** 154 texts, 91 distinct laws, for the name; 3 texts, 2 distinct byte strings, for
  the `over` list (X9).

**The experiment** *[R7-B1–B5]*. In his words: *"This closes the distinction between an unsuccessful build and an
interrupted experiment."*
- **The unit** (B2). An experiment is one complete attempt, its prescribed cases in a fixed order, from fresh builds.
  The two runs a prediction requires are two experiments. The two generations of an evidence record are separate
  experiments. An interruption voids the attempt in which it occurs, and that entire attempt is repeated, never only
  the failed case or what remained. A completed attempt stands. Interruption counts and causes are kept with the
  evidence and never count toward acceptance.
- **A fault on the repeat** (B1). In his words: *"After one repetition that ends in a fault again, the experiment stops
  and returns to me. No third run."* A fault's identity (its line, if it has one, and its exit status) is recorded, but
  decides nothing: *"identity does not determine whether the stop rule applies."*
- **Any cause** (B3). The rule applies to interruptions of every cause, not only runner faults. An operator's interrupt
  is an interruption wherever it lands. Reference runs and core runs each start in a process group of their own, so
  that an operator's or a harness's interrupt cannot be read as a reference crash.
- **Harness faults** (B4). A process that cannot start, or a failure of the harness itself, is a harness fault, and so
  an interruption. Its error and every record already made are kept. It is never classed as a reference outcome, and
  no case is retried alone.
- **A slow build** (B5). A core build that takes more than 600 seconds fails the attempt, its wall time recorded. It is
  not an interruption.
- **How a harness keeps an attempt.** The reference record's generator, `gen_r6_reference.py`, keeps each attempt of
  each generation in an append-only attempt record under `work/rust-core/attempts/` (outside the tracked files): its
  identity and `retry_of`, its inputs, sources, command, environment and workers, written before any child process
  starts *[Note, 2026-10-31, REREAD-8's ZB1, adopted by his ruling on the ruling sheet: not quite: the generator starts
  one child process, the recursion-limit probe, before `attempt.json` is written. The generator is pinned by the
  record's header and stays as it is; the next generator writes its record first (Amendment 9)]*; each run as it ends,
  raw; and one terminal disposition with its cause. Nothing in it is ever deleted, and only
  a completed attempt writes its generation's file. This is how the generator keeps what B2 and B4 require (and
  REREAD-7's X10). Since his R6 remake ruling it also keeps each run's start and end, and the host's commit before,
  during and after each generation. It writes the record only from two completed generations whose files are byte for
  byte equal (below). Beside his ruling came a proposal to make such a record a rule of every attempt. It is not
  recorded as his ruling; it is put to him. *[Note, 2026-10-30: he ruled it later that day, as ATTEMPT-RECORD-0, for
  every remaining LAW-FORMAT-0 Phase 0 attempt (RULINGS.md), recorded after REREAD-8's readers had finished.]*

**The runner** *[R7-D2, R7-D5; X3, X4, X13, Y14]*. It is now `research/rust-core/ref_run.py`, sha256
`822c826ee2033df257832ff07b3ee74d6d71941880b4db72c83955d4918915b9`:
- **Every failure before the reference begins is a runner fault:** its own imports, the arguments, the input, the ENV
  line, a `__pycache__` folder, the reference's modules not importable (whatever the exception), decoder1's pin or plant.
  *[Note, 2026-10-31: not a `SystemExit` raised while those modules import, which escapes, a documented limitation
  (Amendment 8, his J; REREAD-8's ZB2, ZC4).]*
- **An exit 3 without the runner's line** is an anomaly of its own: `classify` raises `Anomaly`, the experiment stops,
  and it is reported, never classed.
- **An exit status the runner never gives,** with `KeyboardInterrupt` last on stderr, is an interruption: `classify`
  raises `Interrupted`.
- **The conditions.** The ENV line is printed once the reference's modules are imported. It carries every `orlog`
  module loaded, each by its file's sha256 (in law mode, the eight decoder1 brings in). *[Note, 2026-10-31: five in law
  mode, eight in text mode; "the eight" is every applicable module (his L2; REREAD-8's ZB4, ZC3).]* A line of the same
  conditions follows the run, before the outcome. No `__pycache__` folder may stand in `src/orlog` or
  `research/rust-core`, as he
  ruled, nor in `research/law-sufficiency`, the folder decoder1 is imported from (the writer's extension, said here).
- **A crash's exception type** is the runner's own `REFERENCE-EXCEPTION <module>.<qualname>` line (his D2), replacing
  E2's earlier wording.
- **None of the 632 crashes recorded** is one of these cases: they are of eight exception types, none
  `ModuleNotFoundError` or `KeyboardInterrupt`, and none without a type (MEASURED). His words: *"The existing 632
  recorded reference crashes do not need reclassification based on these changes."* *[Note 2026-10-31 (REREAD-9's
  NC14, his D7): in his words the sentence goes on after a colon; the period here is the sheet's.]*
- **Its check,** `research/rust-core/ref_run_paths.py`, sha256
  `87d93a4946ff40235e1c5f49a9bd698a57310b74a55bca42fb86335fbbf7aeb2`, holds 43 cases: the outcome lines of law mode
  computed by the check itself; made-up runs with two different results and two different refusals, the anomaly and
  the interruption; the new runner-fault paths; both conditions lines; the source read by its syntax tree. Its record is
  `evidence/rust-core-ref-run-paths-8.txt`. *[Note, 2026-10-31, REREAD-8's ZB3: it held each module the conditions
  lines list by its file's sha256, but not that the list was complete, nor the implementation, version and platform,
  nor each of the three bytecode folders by name; it does since Amendment 12.]*
- **The changes the re-reads showed,** against the check: `research/rust-core/ref_run_variants.py` (sha256
  `b85295dc5379ea90d78baab1f15f328cc191d71c75466d72f7cb75260090e17f`) makes each of REREAD-6's five and REREAD-7's
  eleven in a copy and runs the check on it. It catches 14 of the 15 changes. V11 (an `IndexError` in law mode's run
  taken as a refusal) is not caught: no input of the check makes the interpreter raise it. The record's rows would
  change, so the hash closure of a record made by such a runner would fail. Its record is
  `evidence/rust-core-ref-run-variants-8.txt`. *[Note, 2026-10-31, REREAD-8's ZB5: it made four of REREAD-6's five, so
  15 changes, not 16; the fifth, P keeping the text-seal line in both modes, was added by Amendment 12.]*

**The trace's comparison** *[X11]*. R4 compares traces line by line. The runner's trace digest, and its `--files`
trace, are the trace's lines joined by LF, with no LF after the last. That is not a trace file's bytes as RUNTIME-SPEC
§5 writes them. A harness compares a core's TRACE with the reference's by their lines.

**Load and the limits** *[R7-F1; X5]*. A reference outcome near the 60-second limit depends on host load: mutant 09729
ran from 33.5 s alone to 56.9 s beside other work (REREAD-7). Each run's wall time is recorded, the runs past 30 s
listed, and "rows equal" predicted with that caveat. For each remake (his F1):
- the initial configuration is four workers per generation, the two independent generations running at once;
- each generation records its wall time, CPU time, peak host memory or commit, worker count, process-start failures and
  interruptions;
- workers may be increased only while no run exceeds 45 seconds and no process fails to start; *[Note, 2026-10-31:
  and, in his words, "The measured process and memory limits govern" (Amendment 8, his K).]*
- a process that cannot start is a harness fault (B4). In his words: *"Do not silently reduce workers and continue a
  partial experiment. Repeat the complete affected generation under the corrected configuration."*

**The evidence records** *[Y3; his first ruling, conditions 5 and 6]*. In his words: *"Cache use must be disclosed and
verified. Cached artifacts must be checked against their recorded inputs and outputs. The evidence must distinguish
fresh builds from cached runs."* And: *"Twice-identical results are necessary, not sufficient. Preserve the exact
commands, compiler versions, host details, seeds, inputs, outputs, and plant results."* So every core build's record
names whether it was fresh or cached, and for a cached one the cache's inputs and outputs, checked against their
records. Every run's record keeps:
- the exact command;
- the compiler's full version (`rustc -vV`);
- the host's details, as the host reports them;
- the seeds;
- the inputs and outputs, by sha256; *[Note, 2026-10-31: kept themselves, beside their sha256 (Amendment 8, his I).]*
- the plant results.

**Section 7, as it now reads** *[R7-C; X2, Y4]*. *[Note, 2026-10-31: replaced by Amendment 8's list, his I.]* For the
milestone, every one of these holds, each under its own
repetition requirement:
1. R1–R8, each run twice with byte-identical output, on the owner's host;
2. R2b: for every fixture, the correct refusal code and line;
3. S1–S4 (Amendment 1), each as its row states;
4. the do-nothing fixtures (Amendment 3);
5. R2's write-back fixtures (above);
6. the exit-5 source reading (Amendment 3), recorded before R1–R8 count;
7. the OUT provenance source reading (Amendments 6 and 7), recorded before R2 counts;
8. the evidence-record requirements above, conditions 5 and 6 in their adopted wording;
9. every plant caught, or declared equivalent by measurement; the two writer plants caught through the byte mismatch,
   and never declared equivalent;
10. LAW-FORMAT-0's re-read disposed, and the core's reading-set record checked against its manifest.

*"Passing R1–R8 establishes the milestone only"* stays, now of the whole list. In his words: *"Passing them does not
authorize production integration, reference-authority transfer, or release."*

**D1, measured** *[R7-D1; Y13]*. `research/rust-core/depth_probe.py` (sha256
`886ca9223155cd844761123f8c2b169989ca97add22c097c21a6c40aa5390e6a`; record `evidence/rust-core-depth-8.txt`) measured
the front end's two expression limits at their edges, and a deepest law line of 90 over its search: a lower bound, by a
witness. The derived bound, 99, is an upper bound. W14(c) stays 130 (draft 8, section 8).

**E1–E4** *[R7-E; V2, V3, V6, V9]* are format and checker clarifications, in draft 8. Draft 8's checker moves none of
its verdicts on R6's mutants from draft 7's (MEASURED), and agrees with all of R2b's twins:
- **The checker's verdicts** on R6's mutants are now `evidence/rust-core-r6-checker-8.txt` (sha256
  `58fcdf5e3459e5ebb19b1ebaf7cfff35236818976dd8b886f61e8f6a88947d4b`), made under draft 8's checker. Its rows are draft
  7's record's, every one.
- **Its verdicts on R2b's twins** are now `evidence/rust-core-r2b-checker-8.txt` (sha256
  `f17f536517e86b40508bde1868fdd1da3a25c22b0118086d0cb49492d1f33f47`), agreeing on 1,558 of 1,558, as evidence only.

**The reference's record** *[R7-F1]*. It was made again with this runner and the generator then (sha256 `48d88b21…`),
as two generations at once, four workers each: attempts `r6-reference-4-gen1-a1` and `r6-reference-4-gen2-a1`, both
COMPLETED, with no interruption and no process that failed to start. **The two generations are not byte for byte
equal,** so this amendment names no record from it; he ruled on it (the next attempt, below). His approval of the concurrent remake
reads *"Verify byte-identical outputs"*; a completed attempt stands (B2), so neither is repeated and neither is chosen.
- **The one row of 10,000 that differs.** Mutant 09729 reads `crash exit 1 type builtins.TypeError` in generation 1
  (`research/rust-core/r6-reference-4.txt`, sha256 `1b10b1a09768f107f2046bbeb051af01ee9e49c29347420e2f7c2ea6c4efcf92`)
  and `crash exit 1 type builtins.MemoryError` in generation 2 (`work/rust-core/r6-reference-4.gen2.txt`, sha256
  `18134261860896ecf416e0cd42f0445c2c43699bd360b1f83e79129eb67700f2`). Its class, NO-REFERENCE-RESULT, is the same in
  both. Generation 1's rows are `r6-reference-3.txt`'s, every one (MEASURED).
- **Why.** 09729's mutation (`id 4 to 3`) makes clause 11 multiply an integer by a list, which Python takes as the
  list's repetition. Run alone here, 09729 committed 24.06 GiB at its peak and ended in `TypeError` after 42.5 s
  (MEASURED). Two such runs at once need more commit than this host can give (MEASURED). The two generations went
  through the cases in the same order at the same pace. Generation 2's two runs of 09729 ended about four seconds
  before generation 1's first run of it ended, so inside it, and each failed its allocation within about a second.
  That timing is REASONED from the runs' positions in the attempt records, which keep no time for each run. *[Note,
  2026-10-31, REREAD-8's ZB8, adopted by his ruling on the ruling sheet: the figure is withdrawn. A simulation of the
  pool by REREAD-8's reader 2 put it at about 36 s; neither is a measurement. What stands: both generations reached
  09729 together, and generation 2's runs failed within about 1.4 s, inside generation 1's first run]* The
  reference's crash type on 09729 depends on the host's free memory, as its time depends on load (X5).
- **His F1's figures** (software readings). Peak commit and peak physical memory are read across the host, so they
  are one figure for both generations.

  | | wall | CPU | workers | start failures | interruptions | runs past 30 s |
  |---|---|---|---|---|---|---|
  | generation 1 | 3,931.0 s | 4,290.3 s | 4 | 0 | 0 | 2 (09729's, 38.4 s and 39.5 s) |
  | generation 2 | 3,928.8 s | 4,238.9 s | 4 | 0 | 0 | none (longest 14.6 s) |

  The host's peak commit was 45.7 GiB, and its peak physical memory in use 11.6 GiB.
- **The speedup** (his *"measured rather than assumed"*). There was none. Amendment 6's remake ran 8 workers, one
  generation after the other, and took 1,673 s and 1,752 s, 3,425 s in all. This one ran the same 8 processes and
  took 3,931 s, 1.15 times as long (software timings). Two things differ between them: the runner now hashes eight
  modules in each run, and Amendment 6's first generation ran beside three readers. *[Note 2026-10-31 (REREAD-8's
  ZB4, REREAD-9's NC4, his D4): five modules in law mode, eight in text mode; R6's runs are law mode.]*
- **The rule for more workers.** The generator reports `workers may rise: True` for both generations, by his two
  conditions: no run past 45 s, and no process that failed to start. Yet the host's commit had reached its limit. His
  *"The measured process and memory limits govern"* is not in the generator's rule. Workers were not raised.

**The next attempt** *[his R6 remake ruling, RULINGS.md, 2026-10-30]*. In his words: *"The concurrent attempt fails
verification. Both generations completed, but their outputs differ. Neither generation is selected as the
authoritative record, and neither is silently repeated under B2."* For the next attempt only, his ruling supersedes
F1's concurrent generations:
- generation 1 runs to completion with four workers, then generation 2 with four workers, under the same runner,
  inputs, environment and worker count;
- nothing heavy runs beside either generation;
- the host's commit is recorded before, during and after each generation, and each run's start and end are recorded;
- B2 and B3 govern a harness fault or an interruption;
- *"If both complete but differ, the attempt fails verification again: do not select one, normalize exception types,
  or discard the differing row."*
- *"Only a byte-identical pair may proceed to hash closure and REREAD-8."*

It is the experiment `r6-reference-5`. The generator changes only to keep what his ruling asks (RULINGS.md, "As kept").
In his words: *"This does not establish that sequential execution guarantees identical results under every host
condition."*

**The record** *[his R6 remake ruling, 5]*. Attempts `r6-reference-5-gen1-a1` and `r6-reference-5-gen2-a1` both
COMPLETED, with no interruption and no process that failed to start. **The two generations are byte for byte equal**
(MEASURED). Each file was held to the sha256 its attempt's end record names, and the generator then wrote the record
`research/rust-core/r6-reference-5.txt`, sha256 `636a287364982201638149bd318169cd4d2a8e49bd3ec1bb23222de508f88be5`.
- **Its rows** are `r6-reference-3.txt`'s and `r6-reference-4.txt`'s, every one. *[Note, 2026-10-31, REREAD-8's ZB12,
  adopted by his ruling on the ruling sheet: `r6-reference-4.txt` is generation 1 of `r6-reference-4`; generation 2,
  kept in `kept/`, differs from it on one row, 09729, which reads `MemoryError` there]* Mutant 09729 reads
  `crash exit 1 type builtins.TypeError` in both generations (MEASURED).
- **One after the other.** Generation 1's last run ended 0.489 s before generation 2's first run started, by the runs'
  own times. The clock is `time.time`, which here is `GetSystemTimePreciseAsFileTime()` with a resolution of 1e-07 s.
  Generation 2's commit before was read after generation 1's commit after (MEASURED).
- **His F1's figures**, with the host's commit before, during and after each generation (software readings; commit
  read twice a second across the host, its limit 47.62 GiB throughout):

  | | wall | CPU | workers | start failures | interruptions | runs past 30 s | commit before | peak | after |
  |---|---|---|---|---|---|---|---|---|---|
  | generation 1 | 2,573.1 s | 3,519.1 s | 4 | 0 | 0 | 2 (09729's, 37.0 s and 34.6 s) | 21.24 GiB | 45.30 GiB | 21.04 GiB |
  | generation 2 | 2,749.7 s | 3,532.3 s | 4 | 0 | 0 | 2 (09729's, 36.4 s and 35.2 s) | 20.98 GiB | 45.29 GiB | 21.13 GiB |

  Peak physical memory in use was 11.62 GiB in each.
- **The contention, measured.** In each generation the peak came during 09729's first run. The commit left was then
  2.32 GiB and 2.33 GiB. 09729's two runs followed one another, 5 ms and 7 ms apart. The runs beside it slowed: in
  generation 2, 09758 took 22.5 s of wall for 0.45 s of CPU (software timings), against a 60 s limit.
- **What it does not show.** One pair on this host, with 2.32 GiB to spare at 09729's peak. A load beside it of more
  than that could again end 09729 in `MemoryError`, and one heavy enough to slow its neighbours past the 60 s limit
  would move them to timeout (both REASONED). The generator again reports `workers may rise: True`; its rule's
  omission stands (above), and workers were not raised.

By his ruling's item 5 the pair proceeds to hash closure and REREAD-8. `r6-reference-5.txt` is this amendment's record.

Amendment 6's `r6-reference-3.txt` is kept as its record. In his words, the failure to keep the interrupted
generation's records at 17:40 *"remains a protocol violation to correct in the generator. It does not, by itself,
invalidate the completed record whose two successful generations were reported byte-identical and whose hash closure
passed."*

**The files this amendment fixes.** Each generated file was made twice with identical bytes. Each is named here by its
sha256 and is part of this amendment:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/ref_run.py` | `822c826ee2033df257832ff07b3ee74d6d71941880b4db72c83955d4918915b9` | written | the reference runner and `classify`, replacing Amendment 6's |
| `research/rust-core/ref_run_paths.py` | `87d93a4946ff40235e1c5f49a9bd698a57310b74a55bca42fb86335fbbf7aeb2` | written | the runner's check, replacing Amendment 6's |
| `research/rust-core/ref_run_variants.py` | `b85295dc5379ea90d78baab1f15f328cc191d71c75466d72f7cb75260090e17f` | written | the runner changes the re-reads showed, against the check |
| `research/rust-core/gen_r6_reference.py` | `cc63252de51790cc920ca14630139b9405b01c5981f0442b8afb1de04991ff00` | written | the reference record's generator, its attempt records, replacing Amendment 6's; as his R6 remake ruling asks (the generator that made `r6-reference-4` was sha256 `48d88b2167c2c676ebcbda70804753b4b72bbaa90729e2e05348a95ba66abc87`) |
| `research/rust-core/r6-reference-5.txt` | `636a287364982201638149bd318169cd4d2a8e49bd3ec1bb23222de508f88be5` | `gen_r6_reference.py` (`cc63252d…`) | the reference's class on each of R6's mutants, by this runner, from two generations made one after the other, byte for byte equal |
| `research/rust-core/gen_r2_fixtures.py` | `0336d05edb193e35c99c0c9429e69dbb9058617a5b8ec7a5133ec783e39579fa` | written | the write-back fixtures' generator |
| `research/rust-core/r2-writeback-fixtures.txt` | `2e13265aae132ba6e62411999e55c99d2c85caacc05e1a1603466c26d2feb5a0` | `gen_r2_fixtures.py` | R2's 11 write-back fixtures |
| `research/rust-core/depth_probe.py` | `886ca9223155cd844761123f8c2b169989ca97add22c097c21a6c40aa5390e6a` | written | D1's measurement of the front end's limits |

`research/rust-core/r6-reference-4.txt` is not in this table: it is generation 1's file, not a record (above).

### Amendment 8: E2 followed literally; W9's parts; W14(c) at 91; the acceptance list complete; the evidence kept; the runner's limitation; F1's memory sentence (2026-10-31, the owner's rulings G to L on REREAD-8)

His rulings on REREAD-8's questions are recorded whole in RULINGS.md, section "REREAD-8's dispositions ruled, G to L".
His principle: *"the checker must implement the adopted wording, not a more permissive interpretation that happens to
pass the existing corpus."* This amendment governs where it differs from Amendments 1 to 7. His scope: *"For Draft 9,
the authorized work is limited to these corrections, the checker changes required by G and L3, and the corresponding
evidence and documentation updates."* The disposition's other DRAFT items are not applied; they are put to him.

**G, H and L3: the format** *[R8-G, R8-H, R8-L3]*. LAW-FORMAT-0 draft 9 applies them:
- a rule is typed by its first define in clause order alone, and a first define that uses its own rule, directly or
  through other rules' first defines, types none; a promote's own two parts are made wherever it stands. Six plants,
  each undone in `plant_reverts.py`;
- W9's parts are enumerated, each with the inputs it needs. Four questions are open and go to him (draft 9, section
  8): (A), whether "⟨type⟩ is numeric" is a part of `neg`, `abs` and `sqrt`; (B), whether a comparison's operand kind
  is a part made with the other operand underived; (C), what type a variable read in a rule's first define has when
  the walk has not met its declaration by the define's clause; (D), which declaration types an id declared twice. (A)
  and (B) move no plant, corpus law or verdict on R6's mutants (MEASURED). His L3 asks that the checker be held to the
  enumeration by a reading made independently of it. A fresh agent wrote its own decider from draft 9 alone, never
  reading the checker's typing code, and agreed with the checker on every law outside the open questions: 258 targeted
  cases, a sweep of 168,596 laws, 300,000 random laws and 2,379 laws in floats mode, under the checker's present
  readings (MEASURED there; `W9-VERIFICATION-REPORT.md`). It found (C) and (D), and a sentence of draft 9 that was
  false, corrected (its D2); its witnesses were run again here and confirmed;
- W14(c) is 91, the candidate limit: a line 91 deep is measured, the bound above it reasoned and not yet established
  independently. In his words: *"REREAD-9 must actively try to produce a valid front-end law with a line deeper than
  91."* A deeper line goes back to him; the bound is never raised, and the counterexample never refused, without his
  ruling.
- **The checker's verdicts** on R6's 10,000 mutants are now `evidence/rust-core-r6-checker-9.txt` (sha256
  `3b90928d89405b833c84eccdb936154e3723c1e2ecbabacdc8858ecef51770d4`), made under draft 9's checker, twice alike. Its
  rows are draft 8's record's, every one. Its verdicts on
  R2b's twins are `evidence/rust-core-r2b-checker-9.txt` (sha256
  `7efae393cb7c51e0f6c629d7523204e48b50bfb28999d8810b4a8e73adc4488f`), agreeing on 1,558 of 1,558, as evidence
  only (MEASURED).

**Section 7, as it now reads** *[R8-I; ZC1]*. It replaces Amendment 7's list. In his words: *"Every acceptance item has
an explicit repetition requirement. Do not leave the reader to infer which tests repeat."* For the milestone, every one
of these holds, each under the repetition requirement stated with it. A run is repeated as two experiments (B2), each a
complete attempt from fresh builds, on the owner's host; "byte-identical" means every file the run writes, and its
stdout and stderr, the same bytes in both:
1. R1–R8: each run in two experiments, with byte-identical output;
2. R2b, for every fixture the correct refusal code and line: run in two experiments, with byte-identical output;
3. S1–S4 (Amendment 1), each as its row states: each run in two experiments, with byte-identical output;
4. the do-nothing fixtures (Amendment 3): run in two experiments, with byte-identical output;
5. R2's write-back fixtures (Amendment 7): run in two experiments, with byte-identical output;
6. the exit-5 source reading (Amendment 3): made once, and recorded before R1–R8 count. It is a reading of the core's
   source, not a run, so it is not repeated; a change of the source makes it again;
7. the OUT provenance source reading (Amendments 6 and 7): made once, and recorded before R2 counts; made again on any
   change of the source;
8. every adopted evidence-record requirement, kept for every run of items 1 to 5, in each of its two experiments
   *[replaced, with this list's sentence on byte identity, by Amendment 13 (his ruling on REREAD-9's ASK 9-1)]*:
   - Amendment 2: each class word kept apart, and each class counted on its own *[his further requirement]*;
   - Amendment 3: every run's record, its fresh folder listed before and after, its environment as its own process
     reports it *[J13, J14]*, and a crash's exit status and exception type among the class words;
   - Amendment 4: what each run wrote to stdout *[K10]*;
   - Amendment 5: an interrupted experiment's runs kept and counted, never used toward acceptance *[N3, L12]*;
   - Amendment 7: the interruptions' counts and causes (B2); each run's wall time, the runs past half the limit listed
     (X5); conditions 5 and 6 of his first ruling, in his words;
   - ATTEMPT-RECORD-0: every experiment attempt's append-only record, in its six points;
   - this amendment: the inputs and outputs kept themselves, beside their sha256 (below);
9. every plant caught, or declared equivalent by measurement, in each of the two experiments of the prediction it
   belongs to; the two writer plants caught through the byte mismatch, and never declared equivalent;
10. LAW-FORMAT-0's re-read disposed, and the core's reading-set record checked against its manifest: each once, before
    the milestone is claimed.

*"Passing R1–R8 establishes the milestone only"* stays, now of the whole list. In his words: *"Passing them does not
authorize production integration, reference-authority transfer, or release."*

**The inputs and outputs, kept** *[R8-I; ZC11, ZB9]*. Condition 6's "Preserve … inputs, outputs" keeps them
themselves, each named by its sha256. In his words: *"Hashes establish identity; they do not substitute for retaining
the evidence."* And: *"The compressed storage proposal is acceptable if it preserves the actual contents losslessly and
the evidence can be independently recovered and checked."* So every file the records so far rest on that lies outside
the tracked tree is kept in it, in `research/rust-core/kept/`:
- each compressed by Python's own gzip at level 9, with no timestamp, under its own path with `.gz` added;
- each named in `kept/MANIFEST.txt` by its path, its length and its sha256, and the kept file by its own sha256;
- `research/rust-core/kept_evidence.py check` decompresses every one with the standard library alone and checks it
  against the manifest, and against the source where it still stands. It never writes over a kept file.

Kept now: the four attempts' `attempt.json` and `end.json`, and `r6-reference-5`'s two `host.jsonl`; the three
generations' files, `r6-reference-4`'s second among them; the generators' two logs and the four logs of the evidence and
records runs; the generator that made `r6-reference-4`, made again (below), with its diff and the script that made it;
the trial and the 09729 measurement's scripts, and 09729's law; and the retention check's own plants with their two runs
(each of six tamperings refused, the two runs alike). In all 4,314,387 bytes, kept in 925,357; `check` reads
`KEPT EVIDENCE HELD: 29 of 29 files recovered exactly` (MEASURED). *[Note 2026-10-31 (REREAD-9's NC13, his D3):
the account above adds up to 28; the 29 rows hold five logs of the evidence and records runs (`records-9`,
`run-format-8`, `-8b`, `-9`, `-9b`), not four.]* **Not kept yet, and put to him:** the four attempts' `runs.jsonl` and
the trial's two outputs. Their tracebacks hold the repository's absolute path, which names the owner's account; kept
losslessly, they would put it in the tracked tree, which is his to allow, and a redacted copy would not be lossless. Not
kept, because it was printed and never written: the output of the run of mutant 09729 alone that
measured its 24.06 GiB peak (Amendment 7). Its law and its script are kept; a later run would be a new measurement.

**J: the runner** *[R8-J; ZB2, ZC4, ZB11]*. It is unchanged: `r6-reference-5.txt`'s header pins it (`822c826e…`), and
the two cases change no row of that record. His words: *"But this is not a ruling that the runner satisfies every
possible D5 failure path. In particular, the uncaught `SystemExit` case remains a documented limitation. Do not
describe it as covered or resolved."* The limitation, as it stands:
- a `SystemExit` raised while the reference's modules are imported, before the reference begins, is not caught: the
  run ends with exit 0, or 1 with its message, and no runner line, and `classify` gives NO-REFERENCE-RESULT (MEASURED by
  REREAD-8's readers 2 and 3, apart). The generator refuses such a run as ENV-MISMATCH, since it has no ENV line, so no
  row of `r6-reference-5.txt` is one (reader 2's plant P14);
- an interrupt that reaches a reference run is labelled RUNNER-FAULT, where B3's adopted text says reference runs
  never become a runner fault. The disposition is INTERRUPTED either way.

And: *"If a later Phase 0 experiment relies on the runner handling every pre-reference failure as a runner fault, that
limitation must be resolved before relying on that claim. No silent reclassification."*

**K: F1's memory sentence** *[R8-K; ZB10, ZC9]*. F1's list gains, in his words: *"The measured process and memory
limits govern."* The present generator's `workers may rise` applies his two conditions alone (no run past 45 s, no
process that failed to start), reads no memory, and read True for both generations of `r6-reference-5` with 2.32 GiB of
commit left at the peak. It is noted here, not changed: the record's header pins the generator. The next generator
reports what it checks, by name, with the commit left at the peak beside it, and never that workers may rise on the
time and start conditions alone. In his words: *"No numeric memory cap is authorized. The R6-5 result gives us a
measured peak and headroom, not a generally safe concurrency threshold."*

**L1 and L2, confirmed** *[R8-L1, R8-L2; ZC10, ZB4, ZC3]*. The R6 remake's item 2 reads whole: *"Keep the same runner,
generator, inputs, environment, and worker configuration."* He confirmed the reading of it, in his words: *"Accept the
statement that the generator was changed only as required to carry out the one-time sequential remake ruling, subject
to the recorded diff and test evidence. This does not authorize unrelated generator changes."* The diff is now
recorded: the generator that made `r6-reference-4` (sha256 `48d88b21…`) was not kept, and is made again exactly, its
sha256 equal, by undoing from `cc63252d…` the edits the session's transcript records. It is kept, with the diff between
the two and the reconstruction's script, in `kept/` (above). The test evidence is the generator's trial on 20 mutants
with its plants, 13 of 13 in each of two runs (only its timings differ between the runs, as a clock's readings do), kept
beside it. And L2, in his words: *"“Eight modules” means every applicable `orlog` module
is hashed. The number is not a fixed requirement for every mode: law mode loads and hashes five. The record must
identify the actual modules and hashes for that run."* `r6-reference-5.txt`'s header names the five, each by its sha256.

**ATTEMPT-RECORD-0** *[his ruling, 2026-10-30]*. Every remaining LAW-FORMAT-0 Phase 0 experiment attempt keeps the
durable, append-only record his ruling sets out in six points (RULINGS.md), created before execution begins. It is an
evidence-provenance rule, not a new outcome and not a change to B2 or B3.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `98796b8d35cf00eed08c2329315ab994dfdfd2ff4b14c99643b1f65e75184bee` | written | LAW-FORMAT-0 draft 9: G, H and L3 |
| `research/rust-core/format_check.py` | `073b4ebc5ba1720663735a1a608d95c3041882395d90452817dda970ea2963ed` | written | the checker, amended to draft 9 |
| `research/rust-core/plant_reverts.py` | `adab85f668bd528df0695a956d918305bde96212b486d25cf217ce8688fe58c6` | written | the plants' undoings, G's four and H's two added |
| `research/rust-core/depth_probe.py` | `6db7a0487c70978d8affb39dbf8fd0af5be12fe41e84edb5b3847fe53a613909` | written | D1 and H: the family that reaches 91, and a deeper line refused |
| `research/rust-core/run_format.py` | `7dab3af74c99c2faf03f2c78070b972c1a98227e3922a0c5d78a8a383c3bcfdf` | written | draft 9's evidence runner |
| `research/rust-core/kept_evidence.py` | `a447671787a596d5a4344118c7fbee8eb5aa0ff6023fcdd18454de692b28e6ac` | written | the evidence kept itself, and its check |
| `research/rust-core/kept/MANIFEST.txt` | `10614486bfb3ef93c4e8466339b89f8605de9d7c0ae88724b96a53eb07de9474` | `kept_evidence.py make` | the kept files, each by its sha256 |
| `research/rust-core/W9-VERIFICATION-REPORT.md` | `08862fb3b0a582242ea524ed676df1afaacea24c25e082b4ec1ad6c8c5e05542` | the verifier, saved word for word | L3's reading made independently of the checker |
| `evidence/rust-core-format-9.txt` | `59002283ac4af7b3a884d851c3ac5839deb3775494a5a312dfe378573fcdb623` | `run_format.py` | the checker on draft 9: 305 of 305 laws, 100 of 100 plants |
| `evidence/rust-core-format-9-reverts.txt` | `d9fb37b7f01da5ea76aa5bd92776b3b3faea0751949dd3d9d48ab22b9846be7d` | `run_format.py` | 56 of 56 plants and fixtures changed by an undoing, 4 only by a crash |
| `evidence/rust-core-depth-9.txt` | `599b1f163c2823c293cc92d73b49579ce85385231c1153e67f0f6627bcaf9e10` | `run_format.py` | the deepest line found, 91, and its edges refused |
| `evidence/rust-core-ref-run-paths-9.txt` | `34cf2490963965c20dc04f36bb9b615e5a62bfbfacd0a5c7f332d34db2efa9e0` | `run_format.py` | the runner's check, 43 of 43 |
| `evidence/rust-core-ref-run-variants-9.txt` | `f78d1a1de977a7fb435b2968240bf75f18e020ab7bdfe43d7d078b0cf3a37716` | `run_format.py` | the runner variants, 14 of 15 caught |
| `evidence/rust-core-r6-checker-9.txt` | `3b90928d89405b833c84eccdb936154e3723c1e2ecbabacdc8858ecef51770d4` | `gen_r6_mutants.py --checker` | the checker's verdicts on R6's mutants, draft 8's rows every one |
| `evidence/rust-core-r2b-checker-9.txt` | `7efae393cb7c51e0f6c629d7523204e48b50bfb28999d8810b4a8e73adc4488f` | `gen_r2b_twins.py --checker` | 1,558 of 1,558 twins agreeing |

### Amendment 9: W9's four questions ruled; the six files kept, tokened; the corrections adopted (2026-10-31, the owner's ruling on the ruling sheet)

His ruling on `research/RULING-SHEET-2026-10-31.md` is recorded whole in RULINGS.md. It governs where it differs from
Amendments 1 to 8. His qualification: *"The final sheet must preserve these dispositions without silently broadening
them."*

**W9's four questions** *[RS-A to RS-D]*. Draft 9 carries his rulings (section 8, "The four questions, ruled"):
- (A) `neg`, `abs`, `sqrt`: only the two stated parts, both on the operand;
- (B) the comparisons, `==` and `!=`: the kind is a part of the pair, checked with the equality;
- (C) a variable's type is read as the prescribed walk meets its declaration; rule typing stays E2's. His four points
  stand in draft 9 in his words, among them *"The variable convention does not establish a general order-free or
  least-fixed-point typing system."*
- (D) an id declared twice keeps the type of the first declaration the walk meets.

The checker makes (A) and (B) its own, and already did (C) and (D). Seven plants hold the witnesses, and the reading he
did not choose for each is an undoing that changes its plant, (C) two ways. Its verdicts on R6's 10,000 mutants and on
R2b's 1,558 twins move none from draft 8's (MEASURED: the records below, each made twice alike). The checker is not
the authority for its own correctness: the reading made independently of it, set to his rulings and never reading the
checker's code, agrees with it on about 500,000 laws, with no disagreement (MEASURED there;
`W9-VERIFICATION-REPORT-2.md`).

**Two questions brought back** by that re-verification, each with its witness in draft 9 and each his:
- (R1) his (C) names the variable's declaration *and scope*; the rule as applied leaves scope out of typing. Is an
  out-of-scope variable's type underived?
- (R4) is a second `let 0`, the second declaration met, variable 1, or a repeated variable 0? The checker reads written
  ids.

Its R2 is applied as wording: derivation 17's cycle sentence now names only the result, underived, and says it sets up
no fixed-point typing of variables. Its R3 is a note on the evidence: the 83 mutants measure that first attempt's
formulation, an unmet variable typed by its declaration in the last walk; a formulation that starts every type
underived and only adds types settled on all of the verifier's laws (R6's mutants were not run). His ruling cites them
as evidence against the literal reading *"without a separately specified termination and fixed-point contract"*; that
stands. Its R5 is applied as wording. *[Note 2026-10-31 (REREAD-9's NC5; his ruling on its disposition, ASK 9-6,
question 1): R2 and R5 were applied here without his disposition. He has deferred both until their exact wording is
brought back with L3's context; neither is an adopted rule (Amendment 13).]* *[Note 2026-10-31, later: he has since
ruled, R2 adopted and R5 adopted as a description of the checker's measured behaviour only (Amendment 15). That both
were first applied here without his disposition stands.]*

**The six files, kept tokened** *[RS-II]*. His conditions, each met before the files were kept:
- every spelling of the prefix has a token of its own: `HOME_ESC` (the JSON-escaped long form of the home folder's
  path), `HOME83` (its short 8.3 form), `REL83` (a relative path through the short form) and `SLUG` (the account written
  with hyphens inside a folder's name), the four spellings the six files hold (MEASURED);
- restoration takes each prefix as an explicit input, `--prefix NAME=VALUE`, and derives none from another;
- replacement changes only the matched prefixes; the restored file must have the original's length and sha256;
- a missing, ambiguous or incorrect input refuses;
- `research/rust-core/kept_tokens_plants.py` plants every spelling, partial matches, multiple occurrences and incorrect
  inputs, on made-up files and on the six real ones: `KEPT-TOKENS PLANTS: 39 of 39 as stated`, twice, byte-identical.

The six are kept in `kept/` with the manifest `kept/TOKENED.txt`, which names each by the original's length and sha256
and holds no prefix. With his four prefixes given, `kept_tokens.py check` reads `TOKENED EVIDENCE HELD: 6 of 6 restored
exactly`; without them it checks that each kept file is intact. No file in `kept/`, compressed or not, names his account
(MEASURED). The prefixes are his to give, and are written nowhere.

**The corrections adopted** *[RS-III]*, each implementing a ruling already adopted:
- draft 9: E1's wording, each kind numbered on its own (ZA6); the operation count unbounded whatever SPEC's `u64` says,
  as E4 rules (ZA7's first part); W3 decided by the spacing rule, never by writing back (ZA9); and, in his words, *"A
  writer plant must actually exercise the named writer implementation; unrelated injected defects cannot count as
  evidence that the writer test works."* (ZA9); the W9 verification's D5 and the re-verification's R5, as wording;
- in-place notes: Amendment 7's attempt record and its one child process (ZB1), R2's fixtures, ten of eleven (ZB7), the
  withdrawn "about four seconds" (ZB8), `r6-reference-4`'s two generations named (ZB12), three notes REREAD-7's Y10
  asked
  for (ZC5), and the Y9 note's history in RULINGS.md (ZC6);
- the names in pinned code (ZC12): the runner's "his D5", the generator's "F2 … F" and "his B1–B4", and the record's
  first line refer to REREAD-7's rulings, R7-D5, R7-F2 and R7-B1 to B4. The pinned files stay as they are;
- **the next generator**, whenever a record is made again: ATTEMPT-RECORD-0's six points; its record written before any
  child process starts (ZB1); every start failure counted from `runs.jsonl` (ZB6); an unexpected harness exception kept
  with its message and traceback (AR-1); every variable the runs are given recorded (AR-2); and his K, what it checks
  reported by name.

**Withheld:** ZA7's extension to the cost counters, a claim's cost and evaluations, and a stop's printed count. In his
words: *"Bring back the exact counters, their overflow behavior, and witnesses before adoption."*

**Named apart, not wording** (his: *"It cannot enter under the label of a wording correction."*):
- ZA5's six plants (E1 for musts and claims; W9's parts made alone in `+`, `not`, `item`, `list-of`) are applied as test
  additions. They change no verdict, acceptance condition or semantics (MEASURED: no R6 or R2b row moves). They are his
  to confirm or remove.
- ZB3 (a stronger runner check) and ZB5 (a fifth runner variant) change the runner's test apparatus, and wait for his
  word.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `1518796d910a5759cf870a9d8cffa74b8d5157278f193ff3aba8ce7cd8d078b4` | written | draft 9 with his rulings A to D, R1 and R4 brought back |
| `research/rust-core/format_check.py` | `2965ed15c824a638b01874846dc3233de9264807680055bdc1b5541031e2279c` | written | the checker: A and B its own, thirteen plants added |
| `research/rust-core/plant_reverts.py` | `922e31c38be7b915ea4f863d92b80925e336b5d2c462ac454350446ceee50378` | written | the undoings: A to D's and ZA5's |
| `research/rust-core/kept_tokens.py` | `6de01db3a65cc9aa345a7251479cb0dad8c83d1d2ab3414928f0429b5a460339` | written | the six files tokened, and their restoration |
| `research/rust-core/kept_tokens_plants.py` | `bf6d458cc8dd952f31afa67caf15bf32e495812cf5a0689e671b2d0ee071843c` | written | its plants: 39 of 39, twice |
| `research/rust-core/kept/TOKENED.txt` | `9d1e0207218c076804787f64b26d02a24373fb2ed8298b1c979e372cf7d1c997` | `kept_tokens.py make` | the six, each by the original's length and sha256 |
| `research/rust-core/kept/MANIFEST.txt` | `d2a8f78ba7b3581ea3d8ad90dfa4eb4912fa25f6a00d49ad0c617eb1a34b54ec` | `kept_evidence.py make` | 34 kept files, each by its sha256 |
| `research/rust-core/W9-VERIFICATION-REPORT-2.md` | `e76bfc6058b200a90005394165307a2b529fc501410e22625ab4d95ecf6f5562` | the verifier, saved word for word | the re-verification at his rulings |
| `evidence/rust-core-format-9.txt` | `5df9c18a824b11f1be23ff8dbb606a34133cf44cb70657a42bf5465962f9904b` | `run_format.py` | 305 of 305 laws, 113 of 113 plants |
| `evidence/rust-core-format-9-reverts.txt` | `7d3b17877c3fbdc9558c37324d924eb30d7ca60b279e25632c05213cc170c9d4` | `run_format.py` | 69 of 69 plants and fixtures changed by an undoing, 4 only by a crash |
| `evidence/rust-core-depth-9.txt` | `1829e1f244cf7d7a8ba53aba36fa038595056532937b1528758e82ddba324bea` | `run_format.py` | the deepest line found, 91, its edges refused |
| `evidence/rust-core-ref-run-paths-9.txt` | `6b1b9a40db800c66819f330923454794314494b21be556135e411a805c488916` | `run_format.py` | the runner's check, 43 of 43 |
| `evidence/rust-core-ref-run-variants-9.txt` | `5af03a6fbca90dd96797e777611741382a20e4d153f43c58fa590c7964c2ae8e` | `run_format.py` | the runner variants, 14 of 15 caught |
| `evidence/rust-core-r6-checker-9.txt` | `b206c8b2c6aa4292221b2fbad617669aee31be66b3050b8a63b691cc7aaaacdf` | `gen_r6_mutants.py --checker` | the checker's verdicts on R6's mutants, draft 8's rows every one |
| `evidence/rust-core-r2b-checker-9.txt` | `59b26346e82538f46000af970299434185737b187aef00b3c59bfb59acd1ddab` | `gen_r2b_twins.py --checker` | 1,558 of 1,558 twins agreeing |

### Amendment 10: R1 and R4 confirmed as the corrected checker reads them (2026-10-31, the owner's confirmation)

His confirmation is recorded whole in RULINGS.md. It answers the two questions Amendment 9 brought back, and nothing
else. In his words: *"These confirmations settle R1 and R4 only. They do not authorize REREAD-9, the Verðandi
experiment, ZA5, or the runner changes ZB3/ZB5. Those remain separate decisions. Nothing here authorizes a commit."*

- **(R1)** Scope is not a part of typing. In his words: *"Type derivation follows the declaration encountered by the
  checker. Scope is a separate validity question, checked under W8."* An out-of-scope variable keeps its declaration's
  type, and its use is W8's failure alone. Draft 9's witness gives W9 at line 3. It is a plant (`RS-C: a first define
  reads a variable met earlier, out of scope`), and the reading he did not choose is the undoing `RS-C undone: reading
  (ii), in scope at the use`, which moves it to W10 at line 3 (MEASURED: the reverts record below).
- **(R4)** In his words: *"The identifier written in the declaration is authoritative; declaration order does not
  renumber it."* A second `let 0` declares variable 0 again, and is W8's failure; variable 1 stays undeclared. Draft
  9's witness gives W10 at line 3 (MEASURED: the checker's verdict on the witness's bytes, run here once, outside the
  records). It is not a plant, and none is added without his word.

The checker, its plants and its undoings are unchanged (`format_check.py` 2965ed15…, `plant_reverts.py` 922e31c3…).
Draft 9 states the two as ruled, and its status line no longer lists ZA5 among the corrections that implement adopted
rulings: ZA5 is applied as test additions, named apart and waiting for his word, as Amendment 9 says (corrected in
place in the draft, with a note). The draft's bytes change, and with them the line of each record `run_format.py`
writes that hashes it, and the draft's sha256 line in the checker's record. Each of the five, with draft 9's old sha256
put back, has exactly the bytes Amendment 9 fixed (MEASURED): no row moved. The records of R6's mutants and R2b's twins
hash only the checker, and stand as Amendment 9 fixed them.

**Still waiting:** ZA5, confirmed or removed; ZB3 and ZB5; ZA7's extension, withheld until the counters, their overflow
behaviour and witnesses are brought back; the Verðandi experiment's two decisions; and REREAD-9, not authorized.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `33285ad4b2e4ccb3ab04e7efeed1e780375eec232d42d3746e252b660e87e9c4` | written | draft 9 with R1 and R4 ruled |
| `evidence/rust-core-format-9.txt` | `8245734d258beafe51cf9beeb6f9a7ad0e20767310f953563aed3b00eb2ef287` | `run_format.py` | 305 of 305 laws, 113 of 113 plants; draft 9's old sha put back, Amendment 9's bytes |
| `evidence/rust-core-format-9-reverts.txt` | `9420a0bdb6038a8e195436b04a654041b8c3f7d0f1e99f7571397eeee4236c71` | `run_format.py` | 69 of 69 plants and fixtures changed by an undoing, 4 only by a crash; draft 9's old sha put back, Amendment 9's bytes |
| `evidence/rust-core-depth-9.txt` | `485cb2f67566cea675e7372967472a289480e6ed747eac414ef3963b87bd000d` | `run_format.py` | the deepest line found, 91, its edges refused; draft 9's old sha put back, Amendment 9's bytes |
| `evidence/rust-core-ref-run-paths-9.txt` | `8dbb7b0f44a23e3c5be1a50eddb8793ed833c8457245ab2546205f4e562bf01a` | `run_format.py` | the runner's check, 43 of 43; draft 9's old sha put back, Amendment 9's bytes |
| `evidence/rust-core-ref-run-variants-9.txt` | `c9d441725e9b8b86502516b60640fa5e4689472f3d5ecb539c1ade678c829853` | `run_format.py` | the runner variants, 14 of 15 caught; draft 9's old sha put back, Amendment 9's bytes |

### Amendment 11: ZA5's six plants kept as test additions (2026-10-31, the owner's ruling on ZA5)

His ruling is recorded whole in RULINGS.md. In his words: *"Record them as test additions under ZA5, preserving their
provenance and their status as non-semantic changes."*

- **What they are:** six plants in `format_check.py`, each named `ZA5: …`, and their six undoings in `plant_reverts.py`,
  `ZA5 undone: …`: E1 for musts and for claims, counted as met (W8 at line 3, where counting distinct ids gave line 5);
  and W9's parts made alone in `+`, `not`, `item` and `list-of` (W9, where a check made whole or not at all gave W10).
- **Their provenance:** REREAD-8's ZA5 (reader 1, MINOR: no plant pinned E1 for claims and musts, or W9's parts outside
  `set` and `change`); its disposition's DRAFT, the six witnesses planted, each with its undoing; applied under his
  ruling on the ruling sheet and named apart as not wording (Amendment 9); kept by this ruling.
- **Their status:** test coverage only. In his words: *"not adopting a new semantic rule or changing any verdict,
  acceptance condition, or checker behavior."* When they were applied, no row of R6's 10,000 mutants or R2b's 1,558
  twins moved (MEASURED, Amendment 9).

The checker, its plants and its undoings are unchanged (`format_check.py` 2965ed15…, `plant_reverts.py` 922e31c3…). Its
comment over the six still reads `(adopted as test corrections under E1 and E2)`, written when they were applied,
before his word; it names the rulings they test, and stands, since changing it would change the checker's bytes and
every record that hashes it. Draft 9 records ZA5 as kept, in the status and in section 11. The draft's bytes change,
and with them the line of each record `run_format.py` writes that hashes it, and the draft's sha256 line in the
checker's record. Each of the five, with draft 9's old sha256 put back, has exactly the bytes Amendment 10 fixed
(MEASURED): no row moved. The records of R6's mutants and R2b's twins hash only the checker, and stand as Amendment 9
fixed them.

**What it does not authorize**, in his words: *"This does not authorize ZB3, ZB5, the Verðandi experiment, or
REREAD-9."* **Still waiting:** ZB3 and ZB5; ZA7's extension, withheld until the counters, their overflow behaviour and
witnesses are brought back; the Verðandi experiment's two decisions; R4's witness as a plant, not added without his
word; and REREAD-9, not authorized.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `12d95962b116cc0f364eb6100a458ea978d5fe0e85a6003c8e6cb757adfb257a` | written | draft 9 with ZA5 kept |
| `evidence/rust-core-format-9.txt` | `e4f3aa0d268e6d3f5957fda79fb2a6e44b75a31295bcd542a5b3436b59f3321c` | `run_format.py` | 305 of 305 laws, 113 of 113 plants; draft 9's old sha put back, Amendment 10's bytes |
| `evidence/rust-core-format-9-reverts.txt` | `c46dce7892048228e8e689e22298244990f5d865b4765fd081661686f42f2564` | `run_format.py` | 69 of 69 plants and fixtures changed by an undoing, 4 only by a crash; draft 9's old sha put back, Amendment 10's bytes |
| `evidence/rust-core-depth-9.txt` | `0e6627df37befa6cbd12e3837020e41e7141199bf5f83f327a2c4761684e736a` | `run_format.py` | the deepest line found, 91, its edges refused; draft 9's old sha put back, Amendment 10's bytes |
| `evidence/rust-core-ref-run-paths-9.txt` | `98f92a44ef18e0857e2bdf41ada2c3847c5cc189bb0cf8c5f35903fe582d22d3` | `run_format.py` | the runner's check, 43 of 43; draft 9's old sha put back, Amendment 10's bytes |
| `evidence/rust-core-ref-run-variants-9.txt` | `147a12db1c387d3a1edc9cd2c657f3f9b5b17f3ad8a4286094465f537d2e91a3` | `run_format.py` | the runner variants, 14 of 15 caught; draft 9's old sha put back, Amendment 10's bytes |

### Amendment 12: ZB3 and ZB5 applied to the runner's check; the records made anew beside the old (2026-10-31, the owner's ruling on ZB3 and ZB5)

His ruling is recorded whole in RULINGS.md. In his words: *"These are runner-check changes, not changes to the
checker’s semantics, the reference, or the accepted laws."* The runner, `ref_run.py`, is unchanged (sha256
822c826e…), and so are the checker, the reference and the laws.

**ZB3**, in `ref_run_paths.py`:
- **The environment record complete.** The check makes the ENV line and the after-run line itself, whole, and each
  run's must equal them. They hold the implementation, version and platform a fresh interpreter reports when it is run
  as the runner is (`python -B`, the same environment, a fresh folder), its default recursion limit, `format_check
  not-imported`, and exactly the `orlog` modules a fresh import of the runner's setup loads, each by its file's sha256:
  eight for a text, five for a law, five under a stand-in decoder1 (MEASURED). Before, the check held each listed
  module's sha256 and that `orlog.interp` was among them, and nothing else of the line.
- **A bytecode cache in each folder, by name.** Three cases, one for each of `src/orlog`, `research/rust-core` and
  `research/law-sufficiency`, the folders the runner's docstring names. Each runs a copy of the runner whose root is a
  folder made here, holding the three folders with the cache in that one, and the fault must name it. The earlier
  case, a cache in a fourth folder put into the runner's list, stays.
- **His words *"against the runner’s own recorded environment"*,** read so: the check compares what the runner's ENV
  line records with what a fresh interpreter, run as the runner is run, reports. *[Note 2026-10-31 (his ruling on
  REREAD-9's ASK 9-6, question 4): not this reading alone. The comparison is against the ENV line `r6-reference-5`
  records; a fresh interpreter's is further evidence, never a substitute. Amendment 13.]*

Against the real runner the check holds 46 of 46, twice. Its 43 earlier rows read exactly as before; added are the
three cases and a line saying how many modules a fresh import loads, which is not a row (MEASURED: the record).

**ZB3's plants.** Reader 2's four changes, made against the runner's code now, stand in `ref_run_variants.py`,
counted on their own and outside the 16: X1, the conditions lines list `orlog.interp` alone; X2, the bytecode check
covers `research/rust-core` alone; X3, the ENV line leaves out the platform; X4, it leaves out the implementation and
version. Against the check as it was before ZB3 (sha256 87d93a49…, from a copy taken before the change), X1, X2 and X4
pass it 43 of 43, as reader 2 found, and X3 is caught, 41 of 43, by the platform stand-ins alone (MEASURED once, here;
kept as `work/rust-core/zb3-old-check.txt`). Against the check now, each is caught: X1 34 of 46, X2 44 of 46, X3 32 of
46, X4 34 of 46. The record reads `ZB3'S PLANTS HELD: 4 of 4 caught`.

**ZB5.** REREAD-6's fifth change, P keeping the text-seal line in both modes, is made, and caught: 43 of 46 (40 of 43
against the check before ZB3, as reader 2 measured). The record reads as he ruled: `REF-RUN VARIANTS HELD: 15 of 16
changes caught by the check; the control passes; 1 not caught, each said`. V11 is still the one not caught: no input
of the check makes the interpreter raise `IndexError`.

**The records, old and new.** `run_format.py` now writes draft 9's five records to new names, the `-9-zb` files, each
made twice with identical bytes; the `-9` files stand as Amendment 11 fixed them, with their sha256 there (MEASURED:
unchanged). The format, reverts and depth records differ from Amendment 11's only in the header line that hashes the
draft and the scripts, and the draft's sha256 line in the checker's record (MEASURED). The paths and variants records
are the runs described above.

**Kept late, under his I.** The runs of Amendments 9 to 11 rewrote the `-9` records in place, so of those three only
Amendment 11's stood as files. Amendments 9's and 10's are now kept in `kept/`, from `work/rust-core/superseded/`:
Amendment 10's from a copy taken before the run that replaced them; Amendment 9's rebuilt from Amendment 10's by
putting the draft's old sha256 back. Each has exactly the sha256 its amendment recorded (MEASURED). Amendment 8's and
earlier cannot be rebuilt so, since the checker changed between them, and stand by their sha256 and their run logs
alone. The run logs of Amendments 10 and 11 went to a scratch folder at the time and are kept now, as
`run-format-9e.log` and `run-format-9f.log`; this run's is `run-format-9g.log`. `kept_evidence.py check` reads `KEPT
EVIDENCE HELD: 48 of 48 files recovered exactly`, and no kept file, decompressed, names his account (MEASURED).

**In place:** Amendment 7's account of the check and of its variants each carry a note (ZB3, ZB5).

**What it does not authorize**, in his words: *"It does not authorize REREAD-9 itself, the Verðandi experiment, ZA7
counter changes, or any commit."* **Still waiting:** ZA7's extension, withheld until the counters, their overflow
behaviour and witnesses are brought back; the Verðandi experiment's two decisions; R4's witness as a plant; and
REREAD-9, which needs his word.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/ref_run_paths.py` | `b8208c7f767644d7e27dc53e8538477f1bf819ca008160e3e1b4ec2e04b310b8` | written | the runner's check: ZB3 |
| `research/rust-core/ref_run_variants.py` | `420ae184fb407f52159c78b07a08f40a11d22c7765df032e52496c40de94b44e` | written | the variants: ZB5's fifth; ZB3's four plants, apart |
| `research/rust-core/run_format.py` | `44e16707d9e271ad79786592318d0f3a217b1af00949e8bb151418329de86a85` | written | the five records written to new names |
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `86716702cb3012db5e50bef4b95bf3a8ef82f06a034b17d422313e268ee782ec` | written | draft 9 with ZB3 and ZB5 named |
| `evidence/rust-core-format-9-zb.txt` | `5afc248624372d0534a9d334ca106efb415d88d1fe93946a9b9779db02140c97` | `run_format.py` | 305 of 305 laws, 113 of 113 plants |
| `evidence/rust-core-format-9-zb-reverts.txt` | `3d2b39bb01c816402a15d6783d82977a7d374887e75795a98fe4a760f26c5792` | `run_format.py` | 69 of 69 plants and fixtures changed by an undoing, 4 only by a crash |
| `evidence/rust-core-depth-9-zb.txt` | `b2a7d0b56c022c4fbbf5e97e6328202d0b2db848eaf0f0175df77f759211fabb` | `run_format.py` | the deepest line found, 91, its edges refused |
| `evidence/rust-core-ref-run-paths-9-zb.txt` | `0c44460d0ae11ed39c383b4161d569181f4d608bc2b1c94e31fc89f5fe1fffff` | `run_format.py` | the runner's check, 46 of 46 |
| `evidence/rust-core-ref-run-variants-9-zb.txt` | `d23da015c74ee0b6097f8b3e8963d2476925537318b337029b18ad59e937bcd4` | `run_format.py` | 15 of 16 caught, V11 not; ZB3's plants 4 of 4 |
| `research/rust-core/kept/MANIFEST.txt` | `8aa132855239055351123fbf473feb021432a834c1a244759dd9674ea7d6f1e0` | `kept_evidence.py make` | 48 kept files, each by its sha256 |

### Amendment 13: REREAD-9's disposition ruled: item 8 named amendment by amendment; five reports tokened; the runner's check extended; the keeping tools' plants; the corrections (2026-10-31, the owner's ruling on REREAD-9's disposition)

His ruling is recorded whole in RULINGS.md. Its boundary, in his words: *"This is not authorization to change checker
semantics, the reference, the runner, the laws, the gate, or release files beyond the specific actions stated below.
Nothing here authorizes a commit."* The checker (`format_check.py`, `2965ed15…`), the runner (`ref_run.py`,
`822c826e…`), the reference and the laws are unchanged.

**The findings and the bound.** REREAD-9's 34 findings are 33 issues, NB1 and NC2 being one. In his words: *"The 91
bound remains REASONED, not proven."* And: *"The checker and runner findings are accepted as measurements of the tested
versions and conditions. They are not blanket certification of every behavior outside those tests."*

**Section 7's byte identity and item 8, as they now read** *[ASK 9-1; NB1 = NC2, NB2, NB3, NB4]*. They replace
Amendment 8's sentence on byte identity and its item 8; items 1 to 7, 9 and 10 stand. In his words: *"The list must name
every adopted evidence-record requirement, not merely conditions 5 and 6."*

A run is repeated as two experiments (B2), each a complete attempt from fresh builds, on the owner's host. **For a core
run, byte identity covers the core's output and each case's class:** every file the core run writes, and its stdout and
stderr, the same bytes in both experiments, and each case classed alike. **A reference run is held by its class**, not
by its raw output's bytes; the 09729 reference runs stay held as `r6-reference-5` holds them, run alone, since their
crash type can vary with the memory free. In his words: *"This resolves the ambiguity without imposing a false
reproducibility requirement on the reference's raw crash output."*

8. every adopted evidence-record requirement, kept for every run of items 1 to 5, in each of its two experiments, each
   by the ruling or amendment that adopted it:
   - **his first ruling, condition 3:** *"Record which outcome occurred for every case."* (R6: refused, or accepted and
     agreeing);
   - **his first ruling, conditions 5 and 6:** *"The evidence must distinguish fresh builds from cached runs."* And:
     *"Preserve the exact commands, compiler versions, host details, seeds, inputs, outputs, and plant results."*;
   - **Amendment 2:** each class word kept apart, and each class counted on its own; every case's record names the
     reference's class and the core's class for each run, with the evidence for it: the exit status, the stderr line,
     the files written, and for EXTERNAL-TERMINATION what the harness did or recorded of the host;
   - **Amendment 3:** every run's record, its fresh folder listed before and after, and a crash's exit status and
     exception type among the class words; and its environment: a reference run's as its own process reports it, its
     ENV line, and a core run's recorded by the harness beside the run, the host's platform and the build's `rustc
     -vV`, never through the core's output. In his words: *"This is a harness requirement, not a new core-output
     requirement."*;
   - **Amendment 4:** what each run wrote to stdout *[K10]*; and, for every R6 mutant where the core and the checker
     differ, the independent reader's record of the case, F2's *"Record the reader's determination and the exact
     applicable rule and diagnostic"*: the determination, the exact rule (the W, the gate or phase, and section 8's
     lines it rests on) and the diagnostic; where the two agree, the record says only that the readings agree;
   - **Amendment 4 (K12) and Amendment 5 (L13):** R8's records state R8's conditions for every run: the arbiter's `run`
     and its 600-second stop, EXTERNAL-TERMINATION in R8 alone, no stdout recorded, no process group;
   - **Amendment 5:** an interrupted experiment's runs kept and counted, never used toward acceptance *[N3, L12]*;
   - **Amendment 6 (U2):** a runner fault's records retained: every run made, and the fault itself, by its
     `RUNNER-FAULT` line, its case and its run; its partial results never used toward acceptance;
   - **Amendment 7:** the interruptions' counts and causes (B2); each run's wall time, the runs past half the limit
     listed (X5); a different fault on the repeat, B1's *"Record its identity, line if available, and exit status"*; a
     harness fault, B4's *"Keep its error and any records already produced"*; a core build past 600 seconds, B5's
     *"Record its wall time"*;
   - **Amendment 8:** the inputs and outputs kept themselves, beside their sha256;
   - **every harness that classes runs** (his ruling on ASK 9-6, question 3): *"Any harness that classes runs, the
     core's included, refuses a run without the runner's ENV line, as the generator does."* His clarification: *"the
     harness is responsible for obtaining and recording that line. This does not require the core to emit or inspect
     its environment."*

   ATTEMPT-RECORD-0 is not named here: its adopted scope stays every remaining LAW-FORMAT-0 Phase 0 experiment attempt,
   and the milestone's runs keep the requirements above in their own right. In his words: *"it means those requirements
   must be stated independently rather than attributed to ATTEMPT-RECORD-0."* The list names Amendment 8's requirements
   and each one REREAD-9's readers 2 and 3 found missing; it claims no more than that search.

**The five reports, tokened** *[ASK 9-2; NC1]*. In his words: *"The no-home-path rule takes precedence over
convenience."* And: *"This is a controlled sanitization of the repository copies, not permission to rewrite the
historical reports or alter their findings."*
- **The originals,** `W9-VERIFICATION-REPORT.md`, `-2.md` and REREAD-8's three reports, moved with their bytes unchanged
  to `work/rust-core/originals/`, outside the tracked tree, where the six files' originals stand.
- **Tokened** by `kept_tokens.py make`, each spelling they hold a token: HOME, the long form, and HOME83, the short 8.3
  form, 3, 3, 25, 49 and 12 times (MEASURED). `kept/TOKENED.txt` names each original by its length and sha256.
- **The repository copies** in `research/rust-core/` are a one-line note, a blank line, and the kept tokened bytes
  exactly. The note says it is a tokened copy, not the original hand-back, and that its line numbers are the original's
  plus two; no copy is described as the original's bytes.
- **Restored:** with the prefixes, `kept_tokens.py check` reads `TOKENED EVIDENCE HELD: 14 of 14 restored exactly` (the
  six, the five, and the three briefs below), and each copy is the note and the kept bytes (MEASURED). The REREAD-9
  reports are unchanged.
- **The search,** of the whole research tree and `evidence/`: 666 views (every file, and every compressed one
  decompressed), 189,463,560 bytes, each spelling and part of the path in UTF-8 and UTF-16, without case (MEASURED).
  Beyond the five, **ten more name the account**: REREAD-1 to REREAD-6's reports and REREAD-7's four, 3 or 6 times each.
  His ruling named five, so these are put to him, untouched. No file under `research/rust-core/` is tracked.
- **My error, found by the search and corrected.** At REREAD-9's end I had kept its three briefs in `kept/` as plain
  files; they name the repository's and the readers' folders by absolute paths. Their three rows and files were taken
  out of `kept/` (copies kept outside the tree first) and the briefs kept tokened instead. No document named the
  manifest that held them.

**W3 and the writer's code** *[ASK 9-3; NA1 = NC3]*. Draft 9's W3 row now gives R7-A's rule, *"W3 must be determined by
code independent of the writer used to produce `OUT`."*, without "never by writing back"; section 11 says the checker
decides W3 with its own writer, and why no verdict differs; section 0's provenance reading names the writer's code by
its files and lines. Option (b), a stricter rule for the core, is not adopted.

**The runner's check, extended** *[ASK 9-4; NB5, NB6, NB7]*, the runner pinned. `ref_run_paths.py` now also holds:
stdout exactly the ENV line and, for a result, the after-run line and the outcome; every law run's ENV line equal to the
line `r6-reference-5.txt` records (his ruling on ASK 9-6, question 4), and a text run's agreeing with it; the conditions
seen inside the run by an observing stand-in (the recursion limit, the `orlog` modules, `format_check`,
`sys.pycache_prefix` and `sys.flags` as the reference begins, a module loaded during it, the modules after); law mode
with `--files` and a TEXTSEAL not zeros, its files and receipt held to the interpreter's; a text stop's outcome
computed; a crash beside a timeout; a BUDGET with a trailing LF; and source rows refusing the forbidden names in
constants, `getattr` by a computed name, dynamic imports, `exec`, `eval` and clocks. Against the real runner: 56 of 56.
In his words: *"The eleven planted changes must actually be caught by the revised check."* They are (MEASURED, the
variants' record):
- K1 to K11, reader 2's changes as it made them: 11 of 11 caught. Against the check before this amendment
  (`b8208c7f…`, kept) each passed 46 of 46 (MEASURED; `work/rust-core/k-plants-old-check.txt`, kept);
- two environment plants, a sitecustomize raising the default recursion limit and `PYTHONPYCACHEPREFIX` set: 2 of 2,
  where the check before passed both;
- ZB3's four, 4 of 4; and the 16, 15 of 16, V11 still the one no case reaches. Each group is counted on its own.

What it does not hold (REASONED): it holds only in the environment `r6-reference-5` was recorded in, and fails
elsewhere, saying where; a runner reaching a forbidden name through a computed key, such as a module's `__dict__`,
passes the source rows, and only the effects the stand-in observes are checked inside the run.

**The keeping tools** *[ASK 9-5; NB10 = NC10, NB11, NB12, NA2]*, test apparatus only:
- `kept_tokens.py`: `make` refuses two tokens side by side; `check` refuses a NAME no kept file holds; both checks read
  the kept file's sha256 before decompressing and report damage. `kept_tokens_plants.py`: a same-length wrong prefix
  for each of seven spellings, refused by the sha256 alone; REL83 and SLUG with near misses and repeats; adjacency,
  unheld NAME and two kinds of damage. 71 of 71 on the made-up and real files, twice, byte-identical (MEASURED). The
  earlier `kept_tokens.py` fails five of the new plants, and a `restore` that compares lengths alone fails all seven
  same-length ones (MEASURED, once);
- `kept_evidence.py`: the kept file's sha256 first, and `zlib.error` caught. Its plants, `kept_evidence_plants.py`,
  count a raise as missed: 9 of 9; the earlier `kept_evidence.py` raises on the `zlib.error` plant, 8 of 9 (MEASURED,
  once);
- M10 compares the count written back with the number of laws read, from the checker's own line. In his words: *"The
  test must demonstrate that the intended failure condition is meaningful, not merely that a fixed constant happens to
  compare equal."* With the writer broken, 0 of 305; the same test does not call the unbroken checker's 305 of 305
  fallen.

**ASK 9-6, question by question.** R2 and R5: marked in draft 9 as applied without his disposition and not adopted;
their exact wording, with L3's context, is brought back to him. *[Note 2026-10-31: brought back and ruled,
Amendment 15.]* NA6's two places: described in draft 9 as the checker's
measured behaviour, no rule added. J's harness sentence: adopted, in item 8 above. The recorded baseline: the check
compares with `r6-reference-5`'s line (above), and Amendment 12's reading carries a note. The GLUE card: a note in
RULINGS.md; no card work.

**D1 to D12**, each in place with a dated note: D1, D2, D3 and D5 in draft 9 (the `-9-r9` records cited, the `-9` and
`-9-zb` records kept as history; step 3's wording; five undoings, 0 of 305; the six conditions named), D3's kept-file
count and D4's two notes in this sheet and RULINGS.md, D6 and D7 by the three messages kept word for word in
`research/rust-core/messages/` and the corrected provenance, D10 and D11 by notes in RULINGS.md, and:
- **D8, the `SystemExit` limitation.** `ref_run.py`'s docstring (lines 24 to 27) says a failure while the reference's
  modules import is a runner fault "whatever the exception"; a `SystemExit` raised there escapes handlers that catch
  `Exception`, and is classed NO-REFERENCE-RESULT. The docstring overstates. The limitation stands, neither covered nor
  resolved, and the runner stays pinned. His J: *"Do not describe it as covered or resolved."*
- **D9, the inputs kept.** 25 hash-named versions that still existed are kept from `work/rust-core/superseded/`, each of
  the sha256 that names it (MEASURED): draft 9 at `98796b8d…`, `1518796d…`, `33285ad4…`, `12d95962…` and `86716702…`;
  the runner's check at `87d93a49…` and `b8208c7f…`, its variants at `b85295dc…` and `420ae184…`, `run_format.py` at
  `7dab3af7…` and `44e16707…`; `plant_reverts.py`, `kept_evidence.py`, `kept_tokens.py` and its plants as REREAD-9
  pinned them; SHEET.md, RULINGS.md, the ruling sheet, the disposition and `TOKENED.txt` as pinned or recorded;
  Amendment 8's two checker records; and the kept manifest of Amendments 8 and 9 and of REREAD-9's pins, rebuilt
  exactly as the current manifest's first 29, 34 and 48 rows. **Two are not recovered:** the drafts the two verifiers
  read, `5880ca54…` and `d86a2aeb…`. Their bytes were not recovered; they stand by their sha256 alone, which does not
  preserve their contents. In his words: *"From this point forward, preserve every hash-identified input before
  overwriting it."*
- **D12.** `gen_r2b_twins.py --checker` refuses no moved HEAD or changed tree, though its docstring says the tool does;
  `gen_r6_mutants.py` makes the check. The tool stays, pinned by `r2b-twins.txt`'s header.

D13 is deferred until a checker change he authorizes. NA5 stays with ZA7's withheld bring-back, a stop's printed count
among the matters then brought back.

**REREAD-9's six conditions, with the evidence each rested on** *[D5; NC6]*:
1. (A) to (D) in the sheet's exact language: draft 9, section 8, "The four questions, ruled"; Amendment 9.
2. The checker implementing his (C): its witnesses V1 (W10 at line 3) and V2 (W9 at line 3), plants with their undoings;
   the checker's records, made twice alike.
3. The independent verifier checking it: `W9-VERIFICATION-REPORT-2.md`, no disagreement on the 474,249 laws it ran
   (REREAD-9 reader 3's count); it read draft 9 at `d86a2aeb…`, whose bytes are not recovered (D9).
4. The six files resolved, option (c) passing its restoration plants: Amendment 9, 39 of 39 twice.
5. Every remaining DRAFT item disposed: Amendments 9 to 12, ZA7's extension withheld; his words, *"ZA7’s extension being
   explicitly withheld is a disposition"*.
6. The 91 challenge and every earlier prerequisite ready: draft 9's Q3; the challenge in reader 1's brief, kept.

**The two disclosures,** kept as he ruled. Reader 1 opened the agent environment's notes on this project before its
search, the first 421 lines, which hold nothing on the 91 bound; its search was not fully isolated from the project's
history. Reader 3's report stood briefly in `research/rust-core/` while the other readers worked, and was moved out. In
his words: *"These disclosures do not, on the evidence presented, invalidate the three reports or the measured hash
closure."* From now on, in his words: *"Future briefs must forbid access to the agent environment's working notes and
summaries by name."*

*[Note 2026-10-31: the five `-9-r9` records this amendment fixes were made again on draft 9's final text
(Amendment 16); the bytes named below are kept in `kept/`.]*
**Kept:** the run logs `run-format-9h.log` (this amendment's records), the plants' runs, the old checks' outputs, the
superseded versions, the messages and the briefs; `kept_evidence.py check` reads `KEPT EVIDENCE HELD: 83 of 83 files
recovered exactly`.

**Still outside his authorization:** R4's witness as a plant; ZA7's counters and a stop's printed count; the two
Verðandi decisions; D13; the ten older reports that name the account; and any commit or push.

**The files this amendment fixes.** Each generated file was made twice with identical bytes:

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `f86ed1ec5b2d2f5e1e3ddc09a1d7fbe6eed0c185d210b3a546826a17d51bb99d` | written | draft 9 with his ruling on REREAD-9's disposition |
| `research/rust-core/ref_run_paths.py` | `bd1cbf1489b64782f1b60e8135b6e5dfb0b85d2032db0a914b3666746ebc3d11` | written | the runner's check, extended (ASK 9-4) |
| `research/rust-core/ref_run_variants.py` | `b9b29564fa02c3233d63ba1fb6d2415dbfb407f6fb218fe452db5c019619ff89` | written | its variants, with K1-K11 and two environment plants |
| `research/rust-core/run_format.py` | `365174676d372a868e9f4f346c50c518b6a5c70f94b7bb02797178fd539f4da0` | written | the -9-r9 records written beside the earlier ones |
| `research/rust-core/plant_reverts.py` | `25cfb7048b545b01be2a3a901dfbeaa98a1bcfc6925c1794661bebe203509a3d` | written | M10 against the laws read (ASK 9-5) |
| `research/rust-core/kept_tokens.py` | `f4d441a7eedebb42afb845b70db6f1ba1e97180869632829df2b60f193671ceb` | written | adjacent tokens and unheld NAMEs refused; damage reported |
| `research/rust-core/kept_tokens_plants.py` | `76a0dd658a3f694654f01efe8410fb2e9efcfa68b570bc671436d36e5f3397e2` | written | same-length, REL83, SLUG, adjacency, NAME, damage plants |
| `research/rust-core/kept_evidence.py` | `088d1316d1651df153756846f6ada866fa112ec2489cf28cd4662426c62450a1` | written | the kept file's sha256 first; damage reported |
| `research/rust-core/kept_evidence_plants.py` | `50f2691a7a662bba0024df2e66dff32c552404e5c32d2e1db37ee323eb392ec5` | written | its plants, a raise never a catch |
| `research/rust-core/kept/TOKENED.txt` | `e281fa9f1a93a9a0bc4f712e13b13ed5c26310f64308caf187b1cd8c43be22db` | `kept_tokens.py make` | 14 files tokened, each by its original |
| `research/rust-core/kept/MANIFEST.txt` | `ed770adc4ac24d9411306135699637e5541463fd4570831012f3ad23d10eb82e` | `kept_evidence.py make` | the kept files, each by its sha256 |
| `research/rust-core/W9-VERIFICATION-REPORT.md` | `44be6ec0cc474622d4b18e8e26fca8b15a6d9cd02240458505370357c96217ed` | `tokens_r9 make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/W9-VERIFICATION-REPORT-2.md` | `56d4818b19c05b50910803b3330ce49c929af0ccbcd2a0aa8e6798199546e024` | `tokens_r9 make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-8-READER-1-REPORT.md` | `5327112e9d9d09df1e74a8f970504b612017ddd55e548008f48bc57068c68528` | `tokens_r9 make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-8-READER-2-REPORT.md` | `97b9429eaee92dbfc72b9d795e77c1ae28b3e338db6ed8d67bc819dda0d44299` | `tokens_r9 make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-8-READER-3-REPORT.md` | `9d1e1452f14deefda2e8a57fc5c3d1f8eea7bf8c31f737fa4bc5688cf50c8598` | `tokens_r9 make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/messages/2026-10-31-put-for-the-sheet-ruling.md` | `ddd7ed4191f4ddffc4d5fe3a69aa825d0431e7a7b96d78a7c72110bd0fd439cd` | the transcript, by a script | D6 |
| `research/rust-core/messages/2026-10-31-put-for-reread-9.md` | `ab4cacb3815b20198644ed1b664ceb69f6f26de6e2042d0d51d23da49b230d90` | the transcript, by a script | D6 |
| `research/rust-core/messages/2026-10-31-his-consolidated-sheet.md` | `d2b1bfcf5fbd9a3bdf2766c3398aeb3d339e3a67e024998ff59d5f94147e057c` | the transcript, by a script | D7 |
| `evidence/rust-core-format-9-r9.txt` | `84a319031a27ecfee10cac4a2389fdc4dc31770d3a766bd34910c33eebb18224` | `run_format.py` | 305 of 305 laws, 113 of 113 plants |
| `evidence/rust-core-format-9-r9-reverts.txt` | `e4a1ff93d9dcb9c9dc53e03201aebbe89afcf1701af5be73bf468e43f4c4fac4` | `run_format.py` | 69 of 69 changed by an undoing; M10 against 305 |
| `evidence/rust-core-depth-9-r9.txt` | `2c63635646b1f7e48a15d3c683dbe8e1e6a537d30b906679ca0c1e630b93991a` | `run_format.py` | the deepest line found, 91, its edges refused |
| `evidence/rust-core-ref-run-paths-9-r9.txt` | `210d3b8d453678e6b9b5308960dbf033a4905d2e204b10d372ba076e2873f1b4` | `run_format.py` | the runner's check, 56 of 56 |
| `evidence/rust-core-ref-run-variants-9-r9.txt` | `b226f0e284b4a236db39096d57b707fecbbb8a3083f71a34f29b830741ad6023` | `run_format.py` | 15 of 16; ZB3's 4, K 11, environment 2, all caught |

### Amendment 14: the ten older reports tokened as the five were (2026-10-31, the owner's ruling on the ten older reports)

His ruling is recorded whole in RULINGS.md. In his words: *"This is a reversible privacy-preservation correction, not a
change to the reports’ evidentiary status, findings, or wording."* And: *"Bring back the results before treating the
ten reports as fully handled."* So they are not yet called handled. *[Note 2026-10-31: he accepted them as
handled, on the evidence reported (RULINGS.md, "The ten reports accepted as handled").]*

- **The ten,** exactly: REREAD-1 to REREAD-6's reports, and REREAD-7's reader 1 and reader 3 reports and reader 2's
  report and addendum. Nothing else was touched.
- **The originals** moved with their bytes unchanged to `work/rust-core/originals/` (ignored, outside the tracked tree),
  beside the five; none was tracked, and nothing stood there under their names.
- **Tokened** by `kept_tokens.py make` in `kept/`, the two spellings they hold, HOME (the long form) 9 times and HOME83
  (the short 8.3 form) 8 times, no other (MEASURED). `kept/TOKENED.txt` names each original by its length and sha256.
- **The repository copies** in `research/rust-core/` are a note line marking each as a tokened copy, not the original
  hand-back, a blank line, and the kept tokened bytes exactly; their line numbers are the originals' plus two, so a line
  a document cites in one of them is two lower in the copy.
- **The restoration map,** each token with its prefix, stands beside the originals,
  `work/rust-core/originals/TOKEN-MAP.txt`, in the ignored folder; it names the account, so it is never tracked.
- **Restored:** each of the ten from the map alone, byte for byte equal to its original, with the manifest's length and
  sha256: `TEN REPORTS HELD: 10 of 10`. With every prefix, `TOKENED EVIDENCE HELD: 24 of 24 restored exactly` (the six,
  the five, the three briefs and the ten) (MEASURED).
- **The search,** of the whole research tree and `evidence/`, every file and every compressed one decompressed, the 24
  tokened files among them: 706 views, 190,004,094 bytes, each spelling and part of the path, UTF-8 and UTF-16, without
  case. **No file names the account** (MEASURED).
- **Exceptions:** none. No restoration failed, no spelling outside the two was found, and no new reference was exposed.

**The files this amendment fixes:**

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/REREAD-1-REPORT.md` | `36b2dcf2f264c8d48ff6a7fd1b60bfae36de374058128990116e3fa36ccb9b87` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-2-REPORT.md` | `4db9a7bf7b1a408f89de0faf09ed8a12f6aefa94f60381df3a0d5142e436949a` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-3-REPORT.md` | `1684c2825e5b5c7125429715fab60f0b8ac2746ec7ee1e1b265e3c6c5a72c678` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-4-REPORT.md` | `734455d4f5d8a2cb0df3989b668344cdd9a45464a5ea1c59329e0d67ee7f494f` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-5-REPORT.md` | `d282dabb1a5acf56278d8f5348e3fe0546b08dbfb8e6c8c9fe7d03fd353f5526` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-6-REPORT.md` | `89932777905d67dd53b80a33a2981a8bffc89816813d9dc4b86ae2e1db09d0e5` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-7-READER-1-REPORT.md` | `83943152d61ef10ba2f19518c844f3a3685578048750cc7d42de530e73cad72a` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-7-READER-2-ADDENDUM.md` | `e5933f12a53d64d739fc0a57a1fb7028382e4315d9a695f6fce4d8385364ed92` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-7-READER-2-REPORT.md` | `c0b35879458ff1dc05136c72fdf43c5d1f5583e2e0380bb433783c9cd8d4ebc9` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/REREAD-7-READER-3-REPORT.md` | `c6f376a93bd8f480cd043590b8aa4e76f0aec02c823b8fa706b436d5f4d337d3` | `tokens_ten make` | a tokened copy: the note, then the kept bytes |
| `research/rust-core/kept/TOKENED.txt` | `8a66fc42dc7a152fe5e2b692f6041ac6b9b4918f5b63989ac8ed000a3a4216c4` | `kept_tokens.py make` | 24 files tokened, each by its original |

### Amendment 15: R2 adopted; R5 adopted as a description of the checker's measured behaviour only (2026-10-31, the owner's ruling on R2 and R5)

His ruling is recorded whole in RULINGS.md. In his words: *"Neither ruling changes a verdict, checker behavior, or the
underlying semantic rules."*

- **R2, adopted:** derivation 17's sentence as draft 9 states it, from "is underived;" to "(his ruling C)". In his
  words: *"This is a documentary correction, not a new theorem or a change to the checker."* The former wording, "least
  fixed point", stays in the historical drafts and their kept evidence (draft 9 at `98796b8d…`, kept).
- **R5, adopted as a description only:** "the variable's type; with an index, made only when the variable is a list"
  describes the checker's measured behaviour, and is no rule of the W9 table. Draft 9 says so in the four points he set:
  the checker makes the indexed numeric part only when the variable is a list; for one that is not, the part is not
  made and the same-line list condition fails; it describes the implementation measured; it settles no broader question
  of semantics and authorizes no new rule. In his words: *"Do not adopt option (b), which would elevate the wording
  into a normative rule."*
- **The history kept:** both were applied without his disposition (REREAD-9's NC5), deferred (Amendment 13), and now
  ruled. The notes in draft 9 and at Amendments 9 and 13 keep each step.
- **Preserved:** draft 9 as Amendment 13 fixed it, `f86ed1ec…`, kept before this change
  (`work/rust-core/superseded/`, `kept_evidence.py check`: 84 of 84) (MEASURED).
- **The records:** the `-9-r9` records were made on draft 9 at `f86ed1ec…`. Since then the draft differs only in R2's
  and R5's notes and status lines, which no record reads: the checker prints the draft's sha256, and `run_format.py`
  hashes it. Proposed, for his word with the commit's other decisions: the records made once more on the final text,
  twice, before anything is staged, so that the committed draft and its records agree.

No checker, runner, reference, law, gate or release change; nothing staged or committed. Still his: the
law-sufficiency files, the kept evidence's tracking, `LATER.md`, and the commit's shape.

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` | `2c0224d1f0a742e8b242ce835c8b7b0a9b1c6a850497cdc8f802492e75289eb7` | written | draft 9 with R2 adopted and R5 described |
| `research/rust-core/kept/MANIFEST.txt` | `9eb8711236b29aac62ccf1551745289a68906c420d978d96cca53e5ef5bafb81` | `kept_evidence.py make` | the kept files, draft 9 at `f86ed1ec…` among them |

### Amendment 16: draft 9's records made again on its final text (2026-10-31, the owner's commit roadmap)

In his words: *"The next step is to reconcile the inventory and staging proposal, then regenerate draft 9’s records
twice against the final text before the final audit and dry-run review."*

- **Kept first:** the five `-9-r9` records Amendment 13 fixed (`84a31903…`, `e4a1ff93…`, `2c636356…`, `210d3b8d…`,
  `b226f0e2…`), each of the sha256 that amendment states, from `work/rust-core/superseded/` into `kept/` (D9)
  (MEASURED).
- **Made again** by `run_format.py` on draft 9 at `2c0224d1…`, its final text since his ruling on R2 and R5, each record
  twice with identical bytes: 305 of 305 laws and 113 of 113 plants; 69 of 69 changed by an undoing; the runner's check
  56 of 56; its variants 15 of 16, with ZB3's 4, K1-K11 and both environment plants caught; the deepest line 91. The
  run's log, `run-format-9i.log`, is kept.
- **Agreement** (MEASURED): each record differs from Amendment 13's only where it names the draft's sha256, the
  header's code line and, in the checker's record, its draft line; every other line is equal.
- **Unchanged:** the checker's verdicts on R6's mutants and R2b's twins, which hash only the checker (Amendment 9); and
  draft 9's citations, which name the `-9-r9` records.
- **Nothing is staged or committed.** Next, his list's steps 4 to 6: the final read-only audit with a clean-clone
  reproduction, the exact staging set with its dry run, and his authorization.

| file | sha256 | made by | what it holds |
|---|---|---|---|
| `evidence/rust-core-format-9-r9.txt` | `56eee017b1db949868907648c2e478668ca6b9b076bab84f8c1daa800285fba2` | `run_format.py` | 305 of 305 laws, 113 of 113 plants |
| `evidence/rust-core-format-9-r9-reverts.txt` | `92d8fa1a903318dbf1fb0dd8c9ea6f59f710943e64b5758d64e0e78c0bd553c9` | `run_format.py` | 69 of 69 changed by an undoing |
| `evidence/rust-core-depth-9-r9.txt` | `ef9a3d5cdfee017546268b306d2ce7975379dedb3fcd22accdf19d35976d0e40` | `run_format.py` | the deepest line found, 91, its edges refused |
| `evidence/rust-core-ref-run-paths-9-r9.txt` | `818a12797acbf81dd38881698fe9d9c156e294279b17f0271de7f59c7b4e7ce2` | `run_format.py` | the runner's check, 56 of 56 |
| `evidence/rust-core-ref-run-variants-9-r9.txt` | `eb131449f474c4a4efa51356b86eaacfa8548f10b16510758801af5fbd358be9` | `run_format.py` | 15 of 16; ZB3's 4, K 11, environment 2, all caught |
| `research/rust-core/kept/MANIFEST.txt` | `d68fe64de05f44836e30ab78ad9e11333d4d427511d02bd91952a077770c8bd3` | `kept_evidence.py make` | the kept files, the five earlier records and the run log among them |

## 7. Acceptance criteria

*[Note, 2026-10-30: the paragraph below is replaced by Amendment 7's list, his ruling C. It stays as written.]*
*[Note, 2026-10-31: Amendment 7's list is replaced in turn by Amendment 8's, his I.]*

**For the milestone.** R1–R8 held, each run twice with byte-identical output, on the owner's host. Every plant caught
or declared equivalent by measurement. LAW-FORMAT-0's re-read disposed. The core's reading-set record checked against
its manifest.

**Before the core may supplement any production path.** For example, as a fifth execution in the arbiter, or as a play
runtime once version 1 exists. Each needs:
1. the milestone's criteria met;
2. HOST-0: R1–R5 on a second machine, or the supplement scoped to this host and saying so;
3. an independent re-read of the core against LAW-FORMAT-0, its findings disposed;
4. the owner's ruling for that path by name, with whatever gate change it needs ruled separately.

**Never.** Replacing the reference. Ruling 4 makes the Python interpreter the authority. A core that disagrees with it
is a dissent to localize, not a correction.

## 8. What the milestone would not show

- That the core is correct beyond the texts and mutants run. It would be MEASURED, never ESTABLISHED.
- That Float is identical on another host without HOST-0.
- Independence beyond one model family.
- Anything of version 1.
- That the shared front end is right. The core reads what the front end wrote, so a defect there would pass it, as it
  passes all four executions now (README, *What agreement measures*).

## 9. Owed separately, not in this milestone

- The correction proposal for `examples/legal.orl`'s note on rule order (ruling 2).
- The one for `src/orlog/sema.py:6`'s docstring (LAW-SUFFICIENCY-0).
- The gate's exact output matching, exit codes and stored outputs (before the next release).
- The exact-rational wording in SPEC.md, RUNTIME-SPEC.md and `numeric_ref.py`'s docstring.
- Version 1's path, which goes on apart.
- *[Added 2026-10-30, REREAD-7's Y12]* The two scope items of his B1 ruling, recorded as owed nowhere until now: the
  reference's recursion failure, a limit of the reference and not of the language, and the correction proposal for
  the HostStop docstring's *"no statement runs unbounded"* (`src/orlog/interp.py:32-35`).
