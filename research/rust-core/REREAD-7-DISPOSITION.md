# REREAD-7: the dispositions of its findings, the three readers' in one (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted the recommended dispositions of A to F, with one qualification to D1:
*"the expression-depth bound must not be changed until the actual front-end limit has been measured"* (recorded whole
in [RULINGS.md](RULINGS.md)). His precisions, among others:
- A: *"A load refusal does not count as catching either plant."*
- B2: each generation of an evidence record is its own experiment, so *"the 17:40 failure of generation 2 could be
  repeated as generation 2 alone"*. The failure to keep the interrupted generation's records *"remains a protocol
  violation to correct in the generator"*, and the disclosure is kept;
- D1: *"Keep 130 provisionally until measurement."*
- E4: *"Do not saturate at \\(2^{64}-1\\)."*
- F1: per generation, wall time, CPU time, peak host memory or commit, worker count, process-start failures and
  interruptions are recorded.

They are applied in draft 8, the checker, the runner, its check, the generator and SHEET.md's Amendment 7. The text
below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 39 findings in REREAD-7's three reports. As his fifth condition
asks: *"Merge the three reports, preserve every finding and its provenance, resolve overlaps explicitly, and bring me
one disposition with clearly separated rulings required."*

The three reports:
- [REREAD-7-READER-1-REPORT.md](REREAD-7-READER-1-REPORT.md): the format and the checker, findings V1–V10 (3 MAJOR,
  7 MINOR);
- [REREAD-7-READER-2-REPORT.md](REREAD-7-READER-2-REPORT.md): the protocol and the evidence, X1–X13 (6 MAJOR, 7
  MINOR). Its [addendum](REREAD-7-READER-2-ADDENDUM.md) holds the hash closure;
- [REREAD-7-READER-3-REPORT.md](REREAD-7-READER-3-REPORT.md): the rulings and cross-document consistency, Y1–Y16 (4
  MAJOR, 12 MINOR).

In all: 0 BLOCKER, 13 MAJOR, 26 MINOR.

**What they read:**
- LAW-FORMAT-0 draft 7 (`05010e01…`);
- its checker (`5103fd39…`) and `plant_reverts.py` (`23f9cccd…`);
- the reference runner (`162d4ec7…`), its check (`5f415e84…`) and `gen_r6_reference.py` (`eda21973…`);
- SHEET.md (`4d2dca8c…`), with Amendment 6 holding its two placeholders. It is `26bf1fce…` since they were filled;
- RULINGS.md (`2cb28949…`). It is `a2265ca9…` since his parallel-reader ruling was recorded, after the readers
  finished.

**What happens next.** Nothing changes until he rules. He answers ASK A to F. Then:
- draft 8 applies every DRAFT item and his answers;
- the checker, `plant_reverts.py`, `ref_run.py`, `ref_run_paths.py` and `gen_r6_reference.py` are amended to match;
- SHEET.md gains Amendment 7, and the records it fixes are made again;
- a fresh independent re-read follows.

No core code is written before its findings are resolved. In his words: *"Authorization remains unchanged: Phase 0
only."*

**The hash closure passed** (his fourth condition). Reader 2, resumed after the remade record was installed, checked
four things:
- `r6-reference-3.txt` hashes to `bbfcddb5…`, the value Amendment 6 states, at both places;
- its 10,000 rows equal `r6-reference-2.txt`'s, in the same order;
- its header names `ref_run.py` and `gen_r6_reference.py` by their sha256 as they now are;
- SHEET.md, with the filled text put back as placeholders, hashes to `4d2dca8c…`, the version the readers read.

Its last line: *"HASH CLOSURE: PASSED"*. By his condition 4, the re-read is complete.

## What the re-read found holds

**The format and the checker** (reader 1, MEASURED there):
- **Phases 1–3 and the gates' precedence** are implemented as written. An independent reading of phase 3, written from
  the text, agrees with the checker on 400,000 random structural laws. Nothing crashed, and the coverage assertion
  never fired.
- **The plants and the laws:** 88 of 88 plants caught. 304 of 304 laws pass and are written back exactly.
- **About 34,000 corpus mutants:** no checker crash. Every mutant the checker accepted (12,893), decoder1 also
  accepted, and none raised an exception in the reference under a budget of 10,000.
- **B1's obligations hold:**
  - termination, by reasoning;
  - the budget positions, 134 of 134 runs against the reference;
  - the explicit stacks: perform and rule chains of 100,000 are accepted and written back exactly. The reference fails
    at 1,000 with a RecursionError, its known limit.

**The evidence** (reader 2, MEASURED there):
- every generator makes its frozen file byte for byte, twice;
- `ref_run_paths.py` gives 31 of 31, twice, equal to its record;
- 390 mutants, chosen by a rule frozen before any of them ran (sha256 `aa177198…`), each give their row in two fresh
  runs;
- L2's and L3's classifications hold on every path tested. A text the front end refuses, and the budgets `1e6`, `-1`,
  `05` and `+5`, each end exit 3 with a `RUNNER-FAULT` line, and `classify` raises on them;
- the writer plants reach what the sheet says: 154 texts and 3 texts. Those are texts, not laws (X9).

**The rulings** (reader 3): every ruling is carried in substance. Every frozen count it could recompute is right but
two (Y7, Y11): the findings of each re-read, the record's classes and crash types, R2b's 1,558 twins, S3's 2,100
values, and the verdicts that moved between records.

## The measurements (MEASURED, once each; software timings, from the session's own records)

His words: *"treat the one-hour estimate and threefold speedup as hypotheses until measured."*

| | wall time | tokens |
|---|---|---|
| reader 1 | 1,974.6 s (32.9 min) | 400,712 |
| reader 2 | 1,688.4 s (28.1 min) | 277,210 |
| reader 3 | 1,430.3 s (23.8 min) | 394,080 |
| **the three at once** | **32.9 min** (the three started within 39 s; the slowest governs) | **1,072,002** |
| the hash closure (reader 2 resumed) | 73.7 s | 286,025 |
| REREAD-4, one reader | 1,708.1 s (28.5 min) | 462,105 |
| REREAD-5, one reader | 2,929.8 s (48.8 min) | 448,013 |
| REREAD-6, one reader | 3,278.0 s (54.6 min) | 469,077 |

**What the numbers show:**
- **The one-hour estimate held for the reading:** 33 minutes. From the readers' start to the closure took about 65
  minutes. Most of that was the remake's second generation, made again alone after the process-creation failure
  below.
- **The threefold speedup was not borne out:**
  - 1.66 times faster than REREAD-6;
  - 1.34 times faster than the mean of REREAD-4 to REREAD-6 (44.0 min);
  - at 2.33 times their mean tokens (459,732).
- **What this does not show:** a controlled comparison.
  - Each re-read read a different draft, with more material each time.
  - Each figure is one run.
  - The disposition's time is not counted, and it is about the same either way.

**The remake** (`gen_r6_reference.py`, 8 workers, one generation after the other):
- **Generation 1:** 1,673 s, made beside the three readers and reader 2's six-worker sample.
- **Generation 2:** at 17:40 it ended with `WinError 1450` (CreateProcess: insufficient system resources), beside the
  same load, and wrote nothing.
- **Generation 2, made again alone:** 1,752 s, byte for byte equal to the first.
- **So** running alone was not faster. The readers' load did not slow the generator measurably, but it used up process
  creation. On this host, memory and process limits bound parallel work, not the CPU count (X5, ASK F).

**Mutant 09729 against the 60-second limit:**

| conditions | run time |
|---|---|
| here, nothing else of mine running | 33.5 s |
| reader 2, one process of its own, the other readers running | 44.00 s and 48.47 s |
| reader 2's six-worker sample, beside the generator and the readers | 56.89 s and 53.57 s |

## Disclosures

1. **Condition 1 was breached once, by me.** I saved reader 3's report into `research/rust-core/` while reader 1 was
   still reading. One of reader 1's greps, for the sheet's placeholders, matched one line of it. Reader 1 said so and
   did not open the file. Only V10b (the placeholders unfilled) touches that line, and reader 1 found V10b in SHEET.md
   itself. Its independence on that one point is not established. **Lesson:** every report is kept outside the
   reviewed folder until every reader has finished.
2. **The 17:40 event was handled as follows:**
   - the generator ended uncaught and kept no runs (X8, X10), against Amendment 6's rule that an interruption's records
     are kept;
   - generation 1 was kept, and generation 2 alone was made again.

   Whether that is "the whole experiment repeated" depends on what an experiment is (ASK B2). Under the reading
   recommended there, it is. Under the other reading, both generations should have been made again.
3. **Reader 2's sample timings include load.** The sample ran with six workers before my note on capacity, beside the
   generator and the other readers. Its timings carry that load (X5).
4. **Reader 3 ran none of the checker, the runner or their checks.** That ground was readers 1 and 2's, as its report
   says.
5. **The hash closure was checked by reader 2, resumed, not by a fresh reader.** His condition 4 asks for the check,
   not for a new reader.
6. **The saved reports name each reader's scratch folder** under the account's temp directory, which carries the
   account name. Every saved report since REREAD-1 does. They are kept word for word. Before a commit he may want those
   paths redacted, with a note in each header.

## Which findings are mine

- **V1, X1, X2 and Y2: I missed three things** when I wrote Amendment 6's *"R2 must catch each through the byte
  mismatch it causes"* and *"A core whose write-back copies its input would let both pass, so R7 fails it"*:
  - the equivalence route of sections 6 and 7;
  - a W3 judged by writing back;
  - a consequence for the provenance reading.
- **Y1: I checked his bullets, not the option text he adopted** ((iii) in REREAD-6-DISPOSITION.md), and wrote that a
  different runner fault on the repeat *"is not covered by his words"*. That is L1's mechanism again.
- **Y7:** my corrected count, twelve, should be thirteen.
- **Y8:** my note says M3 *"changes the checker's verdict, not the format's text"*. But M3 added words to W5's row,
  and 61 verdicts moved to another line.
- **Y11:** draft 7 says "draft 5's fourteen" and lists fifteen. I dropped draft 5's "and one of draft 4's".
- **X3:** Amendment 6 says the check holds the runner *"to its run conditions as well as its endings"*. Eleven runner
  changes pass it.
- **X10:** Amendment 6 keeps an interruption's records. My generator deletes its folder and writes nothing.
- **The rest:** wording, records and readings of mine.

## The overlaps, resolved

Each finding keeps its own row below. Where several findings are one issue, they point to one disposition:

| cluster | findings | the one issue | disposed by |
|---|---|---|---|
| C1, U1's writer plants | V1, X1, X2, Y2; with V8, X9, Y15's first part | the plants do not show that OUT comes from the writer: an echoing core escapes by equivalence; a core whose W3 runs its writer meets them as load refusals; and the provenance reading has no consequence | ASK A |
| C2, the experiment | Y1, X6, Y5, X7, Y6, X8, X12; with X10's records | U2's procedure has no unit, no rule for a different fault or another cause on the repeat, and no place for a harness fault or a slow build | ASK B |
| C3, the runner's edges | X4, Y14, X13 | a failure before the reference runs, an interrupt, or a broken `src/` reads as a reference crash; SIGABRT reads as a runner fault | DRAFT, D5 |
| the trace digest | V10a, X11 | the digest omits the final LF that RUNTIME-SPEC §5 writes | DRAFT (X11) |
| M3's note | V10c, Y8 | the note says the format's text did not change | DRAFT and D4 (Y8) |
| the placeholders | V10b, and reader 3's "could not check" | unfilled at the reading | resolved by the closure |
| load and limits | X5 and his remake optimization | a reference outcome within seconds of its limit under load | DRAFT (X5), ASK F |

**Where the readers differ:**
- **On facts:** nowhere.
- **On severity:**
  - X6 (MAJOR) and Y5 (MINOR) are one issue. It is kept MAJOR, since it decides how acceptance is counted.
  - X4 (MAJOR) is a wider form of Y14 (MINOR). It is kept MAJOR.

## The findings, each with its reader

Each concrete claim was run again here, read-only:
- scratch `rr7_check.py`: V2's and V3's laws through `format_check.read`;
- scratch `rr7_heavy.py`: two of X3's runner copies through a copy of the check; the exit status of a SIGABRT; the
  `(over …)` lists of the 298 laws; mutant 09729 alone;
- greps of the text.

Where a claim was not run here, the row says so.

| | reader, severity | finding | re-run here | disposition |
|---|---|---|---|---|
| V1 | 1, MAJOR | R7's writer plants cannot tell an echoing core from a writing one when W3 is judged by writing back, and "through the byte mismatch" would fail a compliant core | **CONFIRMED** by reasoning. Section 2 states W3 by writing back (*"writing back gives the rest exactly if and only if W3 holds"*), so a writer plant in such a core refuses the law at load. Reader 1's toy cores (154 and 3 load refusals, 0 byte mismatches) were not re-run | **ASK A** (C1) |
| V2 | 1, MAJOR | W8's numbering after a repeated id is undetermined; the checker departs from the literal reading | **CONFIRMED:** T1a gives W8 line 5, T1b W8 line 3 | **ASK E1** |
| V3 | 1, MAJOR | "underived" is broader in the checker than in section 8; W9 moves to W10 on the same line | **CONFIRMED:** T2a gives W10 line 3, T2c W9 line 4, T7 W10 line 3 | **ASK E2** |
| V4 | 1, MINOR | two readings that agree with the text are unpinned: W14(b)'s reset at a procedure; a block naming another clause | not re-run. Reader 1 measured that neither moves a plant, a law or an R6 verdict | **DRAFT:** both planted, each undone in `plant_reverts.py` |
| V5 | 1, MINOR | J9's "only by a crash" is overstated: a fixed-width reader bites three of its four plants without a crash | not re-run | **DRAFT:** the non-crashing undoing added; the clause-number plant recorded as pinning only "no crash"; section 11's sentence corrected |
| V6 | 1, MINOR | W8's row names only variables; the checker files claims and musts under W8 | **CONFIRMED** by the text (draft 7 :519) | **ASK E3** |
| V7 | 1, MINOR | M10's count cannot fail apart from W3 | **CONFIRMED** by the text: the draft's own *"which W1–W3 imply by construction"* | **DRAFT:** section 11 says so, and that its plant tests that the comparison exists |
| V8 | 1, MINOR | how fine "never copied from the input bytes" is, is undefined | **CONFIRMED** by the text | **ASK A** (C1): defined under either option |
| V9 | 1, MINOR | what happens when the operation count passes 2^64−1 is unstated | **CONFIRMED** by the text: SPEC §7's `u64`; a `for` may run 2^64 times | **ASK E4** |
| V10a | 1, MINOR | the trace digest omits the final LF | = X11 | **DRAFT** (X11) |
| V10b | 1, MINOR | the placeholders were unfilled at the reading | **RESOLVED:** filled, and the closure passed | none |
| V10c | 1, MINOR | M3's note | = Y8 | **DRAFT** and **D4** (Y8) |
| X1 | 2, MAJOR | the equivalent-mutant route lets an echoing core through R7's writer plants | **CONFIRMED** by the text: SHEET :107 and section 7 (*"Every plant caught or declared equivalent by measurement"*). Amendment 6 does not except the writer plants | **ASK A** (C1) |
| X2 | 2, MAJOR | the reading of OUT's provenance has no consequence and no place in acceptance | **CONFIRMED** by the text. Compare exit 5's reading, which has both (Amendment 3) | **ASK A** (C1), **ASK C** |
| X3 | 2, MAJOR | `ref_run_paths.py` does not hold the runner to what Amendment 6 says: eleven changes pass 31 of 31 | **CONFIRMED for four.** The V1 and V9 copies pass 31 of 31 here. V6's and V7's changes would pass: `classify` is right today (two unequal RESULTs, and two unequal refusals, each give UNSTABLE), and the check has no made-up case for either. The other seven were not re-run | **DRAFT:** law-mode outcome lines, the STOPPED line's content and the refusal's message are checked against the check's own computation. Made-up cases are added for two unequal results and two unequal refusals. A second conditions line follows the reference's imports and its run. The source check works on the syntax tree: no `environ`, `getenv` or `setrecursionlimit` name, and no `getattr` on `os` or `sys`. Amendment 6's sentence is corrected in place, with a note |
| X4 | 2, MAJOR | runner faults and reference crashes cross into each other at the edges | **CONFIRMED for SIGABRT:** exit 3 here, and `classify` raises "exit 3 without its line". The interrupt and `OSError` cases were not re-run | **DRAFT** (C3), **D5** |
| X5 | 2, MAJOR | some reference outcomes depend on host load, within seconds of the 60-second limit | **CONFIRMED:** 09729 took 33.5 s alone here, and its row, `crash exit 1 type builtins.TypeError`, is the record's; reader 2 measured 44.0–56.9 s. 05498 and 09270 run 20,000,060 and 20,000,059 operations under a budget of 1,000,000: their `while` loops hold no statement, so the check at a statement's entry is never reached. W5 refuses such laws (a `while` has children), so R6 adjudicates them against section 8 | **DRAFT:** every run's wall time is recorded, as a software timing. Runs past half the limit are flagged and listed with the record. The sheet says these outcomes depend on load, and predicts "rows equal" with that caveat. Worker counts: **ASK F** |
| X6 | 2, MAJOR | "the experiment" and "the repeat" are undefined | **CONFIRMED** by the text | **ASK B2** (C2) |
| X7 | 2, MINOR | the recurring-fault rule leaves cases open: a fault with no line; another cause on the repeat; the draft and the docstring | **CONFIRMED** by the text: `ref_run.py` :73; SHEET :696; draft 7 :780–783; the docstring :27–28 | **ASK B1, B3** (C2). **DRAFT:** the draft and the docstring made to say what the sheet says |
| X8 | 2, MINOR | a run the harness cannot start has no place in the protocol | **CONFIRMED:** it happened here (17:40, WinError 1450). The generator ended uncaught and wrote nothing | **ASK B4** (C2) |
| X9 | 2, MINOR | R2's power on list order is thin, and its counts are of texts, not laws | **CONFIRMED:** 95 `over` lists; 3 of two entries or more, all `(over 1 2 3 4)`; none out of order; none with a repeat. The `given` lists were not re-run | **ASK A** (the fixtures). **DRAFT:** "texts", with the distinct counts (91 laws; 2 byte strings) |
| X10 | 2, MINOR | `gen_r6_reference.py` contradicts the records rule and checks no run's ENV line | **CONFIRMED** by the code. It makes all 20,000 runs, then classifies, then deletes its folder in a `finally`. It gathers the ENV lines into a set | **DRAFT:** classify each run as it finishes; stop at the first fault; keep the raw runs; refuse a run whose ENV line differs from the expected |
| X11 | 2, MINOR | the `trace` digest is not of a trace file's bytes | **CONFIRMED:** the digest, and `--files`, omit the final LF that RUNTIME-SPEC §5 writes | **DRAFT:** the sheet states the comparison. R4 compares by lines; the runner's digest is of the lines joined by LF, with no final LF. The runner is unchanged, since the digest stands in every RESULT row of the record |
| X12 | 2, MINOR | the 600-second build limit has no outcome | **CONFIRMED** by grep: SHEET :125. The other 600-second mentions are R8's arbiter | **ASK B5** (C2) |
| X13 | 2, MINOR | the runner pins decoder1 alone, and a broken `src/` reads as reference crashes | **CONFIRMED** by the code for decoder1: only `ImportError` is caught (:149–151). The `orlog` case was not re-run | **DRAFT** (C3), **D5** |
| Y1 | 3, MAJOR | the stop on a different runner fault at the repeat is attributed to no ruling, though the adopted option (iii) covers it; his point 2 points the other way; the docstring and draft 7 disagree with the sheet | **CONFIRMED.** REREAD-6-DISPOSITION.md :118: *"after one repetition that ends in a fault again, the experiment stops, and the fault goes to him. No third run"*. RULINGS.md's "As kept" says the opposite | **ASK B1** (C2). **DRAFT:** the note corrected in place, and the docstring and draft 8 made to say the same |
| Y2 | 3, MAJOR | U1's "R2 must catch both defects" can be escaped | = X1, X2 | **ASK A** (C1) |
| Y3 | 3, MAJOR | conditions 5 and 6 of his first ruling are not in the sheet | **CONFIRMED** by grep: SHEET.md has no "cache", "compiler" or "rustc version" | **DRAFT:** Amendment 7 states them as evidence-record rules, in his words |
| Y4 | 3, MAJOR | section 7 was never updated for the predictions his later rulings added | **CONFIRMED** by the text: section 7 says "R1–R8 held", and only Amendment 3 amends section 7 | **ASK C** |
| Y5 | 3, MINOR | "the experiment" and "counted" are undefined, though REREAD-6 raised it | = X6 | **ASK B2** |
| Y6 | 3, MINOR | "handled the same way" stretches N3(3); one interrupt is classed two ways | **CONFIRMED** by the text. SHEET :696. An operator's interrupt is a runner fault during a reference run, and another cause during a core run | **ASK B3** |
| Y7 | 3, MINOR | the corrected count is itself wrong; M2's DRAFT part rode outside his named scope | **CONFIRMED:** L1's row reads *"ASK N1. And DRAFT, whatever he rules"*. With L2, L3 and L5–L14, that makes thirteen | **DRAFT:** corrected in place, with notes; **D3** |
| Y8 | 3, MINOR | M3's "As kept" note overclaims; the 61 verdicts are not listed | **CONFIRMED:** draft 7's W5 row carries M3's added words; RULINGS.md :495–497 | **DRAFT:** the note corrected in place; the 61 listed from the records' diff; **D4** |
| Y9 | 3, MINOR | K15 replaced E2's adopted exception-type rule without his word; RULINGS notes are stale | **CONFIRMED:** RULINGS.md :317; SHEET :506–507 | **DRAFT:** in-place notes; **D2** |
| Y10 | 3, MINOR | current-state text that later rulings overtook, with no note, in five places | **CONFIRMED**, each read | **DRAFT:** in-place notes |
| Y11 | 3, MINOR | section 11's "draft 5's fourteen" lists fifteen | **CONFIRMED** by reading. The total, 88, is the checker's | **DRAFT:** "and one of draft 4's" restored |
| Y12 | 3, MINOR | B1's two scope items, the reference's recursion failure and the HostStop docstring, are recorded as owed nowhere | **CONFIRMED** by grep: they appear only in RULINGS.md and REREAD-1 to REREAD-3 | **DRAFT:** both added to SHEET §9 |
| Y13 | 3, MINOR | W14(c)'s bound departs from his "actual expression-depth limit", through REREAD-1 rows adopted only by implication | **CONFIRMED.** Draft 7: *"So 99 levels suffice"*, then *"The bound 130 is kept, as safe and not tight."* | **D1** |
| Y14 | 3, MINOR | "an import failure is a runner fault" holds only for `ImportError` | = X13's first part | **DRAFT** (C3), **D5** |
| Y15 | 3, MINOR | three adopted texts applied differently, with no note: U1(a)'s plant wording; M9's `-6` record; M7's "each a case" | **CONFIRMED** | **DRAFT:** notes in place. The name plant is stated in his words, *"dropping a name"*, with the empty string as its form, reaching the same 154 texts. `-6` is named. M7's folding is noted |
| Y16 | 3, MINOR | draft 7's history leaves out REREAD-0; the F tags collide | **CONFIRMED** | **DRAFT:** REREAD-0 added to draft 8's history; the legend's tags kept apart |

## The questions for the owner

### ASK A (C1: V1, X1, X2, Y2; with V8, X9). How do R7's writer plants show that OUT comes from the writer?

His words (U1): *"R2 must catch both defects through the resulting byte mismatch"*, and *"so the evidence establishes
that the writer—not an input-byte copy—produced it."*

As written, the plants fail in three ways:
- **An echoing core whose writer never runs** is untouched by a writer plant. By measurement that plant is an
  equivalent mutant, and sections 6 and 7 let such a plant be declared equivalent. So the echoing core passes R7 (X1,
  Y2).
- **A core that judges W3 by writing back**, as section 2 states W3, meets a writer plant as a load refusal, never as
  a byte mismatch. So "through the byte mismatch" fails a compliant core. An echoing core that judges W3 the same way
  is caught alike, so the plants cannot tell it from a writing one (V1).
- **The provenance reading** finds whatever it finds, and nothing follows from it. Section 7 does not name it, while
  exit 5's reading has both a consequence and a place there (X2, Y2).

| | what it entails |
|---|---|
| (a) any failure of R2 catches a writer plant | A byte mismatch, or a load refusal of a law the format accepts. The plants then show only that a writer runs somewhere in the core, not that OUT comes from it. OUT's provenance rests on the source reading alone. It departs from his *"through the resulting byte mismatch"*. It puts no constraint on the core's design |
| **(b) W3 decided without the writer** | The core decides W3 by code that does not call the writer that makes OUT. Then a writer plant can show only as a byte mismatch, as his words say, and only a byte mismatch catches it. Without a writer, OUT can only be a copy, so an echoing core fails R7 mechanically. So does a core whose W3 calls its writer: it meets the plant as a load refusal, which does not count. The source reading records both facts: OUT comes from the writer, and W3 is decided without it. The cost: the core's author writes W3's check apart from the writer, a second reading of section 3's encodings. W3 is stated over bytes, so the format allows that |

**Under either option:**
- **No equivalence:** neither writer plant may be declared equivalent. A writer plant that R2 does not catch fails R7
  and goes to him.
- **The reading's consequence:** if the source reading finds any path that copies the bytes read into OUT (or, under
  (b), a W3 that calls the writer), R2 fails and the finding goes to him. The reading is recorded before R2 counts, as
  exit 5's is, and section 7 names it (ASK C).
- **Defining "never copied"** (V8): every atom is decoded to its value and re-encoded by section 3. No slice of the
  bytes read reaches OUT.
- **R2 gains write-back fixtures** (X9): laws whose `over` and `given` lists are out of order or repeat an entry. The
  format accepts them, and none of the 298 holds one. A writer that sorts a list, or writes it as a set, then fails R2.
  The fixtures are frozen by sha256 before any core exists.

**Recommended: (b).** It makes his words hold as he wrote them. It lets the plants, not a reading alone, fail an
echoing core.

### ASK B (C2). The experiment, its repeat, and what interrupts it

His U2 words: *"Treat a runner fault as an interruption of the entire experiment. Retain the records, discard all
partial results for acceptance purposes, and repeat the whole experiment."* And: *"If the same runner fault occurs
again on the repeat, stop and bring it back for a ruling."*

| | recommended | the other way |
|---|---|---|
| **B1, a different runner fault on the repeat** (Y1, X7) | Option (iii), as he adopted it, governs: *"after one repetition that ends in a fault again, the experiment stops, and the fault goes to him. No third run"*. Any runner fault on the repeat stops the experiment. "The same" is recorded but decides nothing: the same line at the same case, or "no line" with its exit status | his word "same" governs. A different fault is repeated again under his point 2, with no bound but a later same fault |
| **B2, the unit** (X6, Y5) | An **experiment** is one attempt: every prediction's cases (R1–R8, R2b, S1–S4, the fixtures) in a fixed order, from fresh builds. Section 7's "each run twice" is two experiments. An interruption voids the attempt it occurs in, which is repeated whole; a complete attempt stands. "Counted" means counted in a tally of interruptions, each with its cause, kept with the evidence and never used toward acceptance. The same holds for making an evidence record twice: each generation is an experiment. The 17:40 event was handled this way | the experiment is the pair of attempts, and an interruption in either voids both. The 17:40 remake should then have made both generations again |
| **B3, other interruptions** (Y6, X7) | The stop after one repeat applies to an interruption of any cause. A second interruption of the same experiment stops it, and it goes to him. An operator's interrupt is an interruption wherever it lands: reference runs start in a process group of their own, as the core's do (X4), and never become a runner fault or a reference crash | N3's point 3 as it stands: an interruption by another cause is repeated without limit, and only a runner fault stops |
| **B4, a harness fault** (X8) | A run the harness cannot start, or the harness's own failure, is a **harness fault**: an interruption under B3, kept with its error, and never retried case by case | none named. It stays outside the protocol, as at 17:40 |
| **B5, a build past 600 s** (X12) | The build is the core's, so the attempt fails, recorded with its wall time. It is not an interruption | an interruption, as host load can slow a build (X5) |

Recommended: **all five as in the middle column**. Since a different fault stops anyway, B1 changes nothing in what
the sheet does, only whose rule it is. B2 to B5 give U2's procedure the unit and the edges it needs before any
harness is written.

### ASK C (Y4; with X2). The milestone's acceptance list

His words: *"Passing R1–R8 establishes the milestone only."* His later rulings added:
- R2b: *"For every fixture, the core must refuse with the correct W code and line."*
- S1: *"For S1, any outcome other than completion with the constructed operation count fails."*
- the do-nothing fixtures (Amendment 3);
- exit 5's source reading (Amendment 3);
- OUT's provenance reading (Amendment 6).

Section 7 still reads "R1–R8 held". By the sheet's own words, a core that fails R2b, or crashes on S1 at depth 30,000,
could meet section 7.

| | what it entails |
|---|---|
| **(a) section 7 lists them all** | R1–R8, R2b, S1–S4, the do-nothing fixtures, both source readings and the evidence-record rules (Y3), each held twice where it runs. His *"establishes the milestone only"* stays as the scope sentence: passing them all establishes the milestone and nothing more |
| (b) section 7 as it is | the later predictions count as evidence only. Then a core that fails one of them could still meet section 7 |

Recommended: **(a)**.

### ASK D. Five things the writer settled beyond his words, to confirm or reverse

| | as settled | recommended |
|---|---|---|
| **D1, W14(c)'s bound** (Y13) | His words: *"W14 must specify the front end's actual expression-depth limit."* Draft 7 derives that 99 levels suffice, but keeps 130, *"as safe and not tight"*, following REREAD-1's G9 and G11. Those rows were adopted only by *"Proceed with draft 2 and its checker amendments"* | **tighten to the actual limit.** Measure the front end at its edge (texts 98 to 101 levels deep), specify what it does, and plant both sides of the edge. 130 stands until that is measured. It changes which laws are accepted, so it is his to rule. The other way: confirm 130 as not his words, and say so in the draft |
| **D2, a crash's exception type** (Y9) | E2's adopted text: *"the last line of the traceback names it"*. K15 replaced that with the text before the first `:` of stderr's last line, under the thirteen minor findings. Since Amendment 5 the runner prints `REFERENCE-EXCEPTION <module>.<qualname>` itself, and that rule was extended to every reference run, R8 excepted | **confirm the runner's own line** as replacing E2's rule, with in-place notes at RULINGS.md :317 and :385–387 |
| **D3, M2's DRAFT part** (Y7) | The miscount's correction rode on *"Adopt … U2"*, as M2's ask, though it is none of U2's three points. The corrected count is thirteen, not twelve | **confirm**, and correct the count in place |
| **D4, M3's settling of W5's row** (Y8) | M3 added words to W5's row (*"every arm and every else whose ⟨C⟩ is an absorbed clause names it, a first arm too"*) under his proviso to *"preserve the existing language and outcome semantics"*. On R6's mutants, 61 refusals stayed W5 but moved line, and a line is part of a load refusal's result | **confirm** that the row's own words, *"named by exactly one arm or else"*, are read as written. The other reading leaves a sound chain and a W4 chain naming differently |
| **D5, the runner's edges** (C3: X4, Y14, X13) | Today a failure before the reference runs reads as a reference crash. That covers: the ENV line or the platform query failing; an import of `orlog` raising anything; an import of `decoder1` raising anything but `ImportError`. SIGABRT reads as a runner fault | **confirm under his U2(1)** (*"Keep runner faults distinct from reference exceptions"*): see below |

The three changes D5 confirms:
- every failure before `reference()` is a runner fault;
- exit 3 without its line is an anomaly of its own, stopped and reported;
- an undefined exit status with `KeyboardInterrupt` is an interruption.

The ENV line also records the eight `orlog` modules' sha256, and the harness checks that no `__pycache__` stands in
`src/orlog` or `research/rust-core`. No row of `r6-reference-3.txt` is any of these cases. Its 632 crashes are of eight
exception types, none `ModuleNotFoundError`, `KeyboardInterrupt` or "none" (MEASURED). So no row moves.

### ASK E (V2, V3, V6, V9). Four readings the text leaves open

Each changes only which W, or which line, a law is refused with. Reader 1 measured each one alone on the whole check
and on R6's 10,000 mutants: none moves a plant, a corpus law or an R6 verdict.

| | the question | recommended |
|---|---|---|
| **E1** (V2) | After a repeated or misnumbered id, which id is next? The text says *"ids 0, 1, … in the order the walk meets their declarations"*. The checker counts distinct ids | **the literal reading:** the i-th declaration met has id i, for variables, claims and musts alike. The checker changes, and T1a is planted (W8 at line 3) |
| **E2** (V3) | Is a rule's type fixed by its first `define` wherever its use stands (derivation 17), and is each part of W9 checked once its own inputs are derived? The checker types rules as the walk meets them, and skips a whole check when any operand is underived | **yes to both.** The underived list is made exhaustive. A first `define` that uses its own rule leaves the type underived, and its use stays W10. The checker changes, and T2a and T3a are planted (W9) |
| **E3** (V6) | Are claims' and musts' ids W8's, as the checker files them? | **yes:** the row says "ids of variables, claims and musts" |
| **E4** (V9) | What happens when the operation count passes 2^64−1? | **it is an unbounded count,** as the reference's is. No run reaches 2^64 operations within its 60-second limit; a core that counts in 128 bits meets the rule at no cost. The other way: the count saturates at 2^64−1 |

### ASK F. The future remakes, and REREAD-8's form

His words: *"run the two independent generations concurrently and increase worker counts to use available CPU
capacity"*, and *"record resource usage so the speedup is measured rather than assumed."*

Since then, two things were measured:
- 8 workers beside three readers used up process creation (WinError 1450);
- 09729 comes within 3.1 s of the 60-second limit under load. Two timeouts change its row, and the hash closure would
  then fail.

| | what it entails |
|---|---|
| **F1 (a) concurrency set by measurement** | Both generations run at once, 4 workers each: 8 reference processes, the count both completed generations used. Every run's wall time and the host's peak commit are recorded. Workers are raised only while no run passes 45 s and no process fails to start. A process that fails to start is a harness fault (B4) |
| F1 (b) as approved, more workers | faster when it works. When a run times out or a process fails to start, the remake fails, and the closure catches it rather than letting it pass |
| F1 (c) a longer reference limit for records | No row of the record reads `timeout` today (MEASURED), so a longer limit changes no row and removes the load risk. It changes Amendment 1's class input, so it is his to rule |
| **F2, REREAD-8** | three readers again, split as in REREAD-7, each report kept outside the reviewed folder until all three have finished; or one reader, as before REREAD-7 |

Recommended: **F1 (a), and F2 three readers.** The split was measured at 1.3 to 1.7 times faster, for about 2.3 times
the tokens.

## What follows his answers

1. **LAW-FORMAT-0 draft 8:** every DRAFT item and his answers, each change marked with its finding. Drafts 0–7 and the
   re-read reports stay as they are.
2. **The checker and `plant_reverts.py`:** E's readings, V4's plants, V5's undoing and V7's wording. Each is run twice,
   and each new plant bites.
3. **`ref_run.py`, `ref_run_paths.py` and `gen_r6_reference.py`:**
   - C3's edges, under D5;
   - X3's stronger check;
   - X10's per-run classing and kept runs;
   - X5's wall times;
   - F's worker counts;
   - B's rules, once he rules them.

   A changed runner makes a new record: `r6-reference-4.txt`, its header naming the runner that made it, made twice
   under B and F, and hash-closed against Amendment 7.
4. **SHEET.md Amendment 7:**
   - A, B, C, D and F as he rules them;
   - Y3's conditions 5 and 6, in his words;
   - X11's trace comparison;
   - X9's fixtures and counts;
   - Y12's two items in section 9;
   - section 7's list.
5. **In-place notes,** each saying what it corrects and why:
   - in RULINGS.md, Y1, Y7, Y8, Y9 and Y10;
   - REREAD-0-DISPOSITION.md's header (Y10);
   - Amendment 6's sentences (X3, Y15).
6. **A fresh independent re-read** of all of it, in the form F2 settles.
