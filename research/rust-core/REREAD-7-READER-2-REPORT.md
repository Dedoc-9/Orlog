> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-7, reader 2 of 3: the protocol and its evidence (first hand-back, before hash closure), its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-7 ran
as three readers working at the same time, by the owner's approval (to be recorded in RULINGS.md once the readers have
finished, since reader 3 read that file under a pinned sha256): reader 1 the format and the checker, reader 2 the
protocol and evidence, reader 3 the rulings and cross-document consistency. Each started fresh, had its own scratch
folder and its own letter for findings (V, X, Y), and saw nothing of the others' work. Each was briefed:
- to read draft 7 (sha256 `05010e01…`), SHEET.md (`4d2dca8c…`, Amendment 6 holding the two placeholders of the record
  being remade) and RULINGS.md (`2cb28949…`) as its part required, with the code, the records and the specifications;
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, and change nothing in the repository.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-7, reader 2 of 3: the protocol and its evidence

HEAD stayed `2e9805aaa1ceeae0beb443d527680796b66f39c7` the whole time. I wrote nothing in the repository, and I opened nothing under `research/law-sufficiency/` apart from running `sha256sum` on `decoder1.py` and running scripts that import from there. Everything was run here, on the owner's Windows host (CPython 3.14.5, rustc 1.96.1), as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` from the repository root, with `TEMP`/`TMP` pointed at my scratch folder.

## Verdict

The evidence reproduces. Every generator I ran makes its frozen file byte for byte, twice. `ref_run_paths.py` gives 31 of 31, twice, equal to its record. All 390 preregistered mutants give their `r6-reference-2.txt` rows in two fresh runs each.

The protocol does **not yet do what U1 and U2 ask**. I found 6 MAJOR findings and 7 MINOR ones. None is a BLOCKER: each can be fixed by an amendment before phase 1.
- **The echoing core (U1).** The sheet does not reliably make an echoing core fail.
  - The equivalent-mutant escape in section 6 and section 7 covers the two writer plants (X1).
  - The reading of OUT's provenance has no consequence and is not an acceptance criterion (X2).
- **The runner and its check (U2).** `ref_run_paths.py` does not hold the runner to what Amendment 6 says it holds (X3). At the edges, runner faults and reference crashes cross into each other (X4).
- **Two more MAJOR gaps.**
  - Two reference outcomes depend on host load, within a few seconds of the 60-second limit (X5).
  - "The experiment" and "the repeat" are not defined against section 7's "each run twice" (X6).

## What I read

- **The sheet.** `research/rust-core/SHEET.md`, whole (sha256 `4d2dca8c…`, verified), Amendments 1 to 6.
- **The runner and its check.** `ref_run.py` (`162d4ec7…`), `ref_run_paths.py` (`5f415e84…`) and `evidence/rust-core-ref-run-paths-7.txt`.
- **The generators.** `gen_r6_reference.py` (`eda21973…`), `gen_r6_mutants.py`, `gen_r2b_twins.py`, `gen_stress_texts.py`, `gen_r5_budgets.py` and `gen_s3_budgets.py`: their docstrings and their code.
- **The records.** The headers and rows of `r6-reference.txt` and `r6-reference-2.txt`, plus `r6-mutants.txt`, read by script only.
- **The checker's records.** The checker-6 and checker-7 records, both for R6 and for R2b.
- **LAW-FORMAT-0 draft 7.** Sections 0, 2–4 and 9–10, section 8's rows on `over` lists, and section 12.
- **The rulings.** RULINGS.md: the REREAD-5 and REREAD-6 rulings.
- **The reference.** `src/orlog/interp.py` and `src/orlog/arbiter.py` (`run`, `reference`, the timeouts).
- **The trace format.** RUNTIME-SPEC.md §5.

## What I could not check

- **No core exists.** I measured the writer plants by applying, to the 298 laws, the byte change a planted writer would make. I did not run them in a core.
- **No experiment harness exists.** I could not check how the interruption and repeat rules, the retained records or the recurring-fault stop are carried out. Only `gen_r6_reference.py` calls `classify` today.
- **`r6-reference-3.txt` is not yet installed.** Hash closure is pending (see the end).
- **The real decoder1's internals.** By the rules of this re-read, I only ran it.

## Answers to the questions

### 1(a). OUT's provenance and R7's two writer plants

- **The counts (MEASURED, `writer_plants.py`).**
  - *A `let`'s name written as the empty string:* this changes the bytes of 154 of the 298 texts, as the sheet says. Those 154 texts are 91 distinct laws. Every `let` in them has a non-empty name.
  - *An `(over …)` list reversed:* this changes exactly 3 texts, the three the sheet names. They are 2 distinct byte strings: `mutant/s1/0485` and `n23-notwithstanding-four.orl` are identical. All three hold the same single list, `(over 1 2 3 4)`.
  - So R2 does meet each plant through a byte mismatch.
- **The echoing core.** The sheet does not make one fail with certainty: see X1 and X2. R2's power on list order is thin: see X9.

### 1(b). The L2/L3 classifications

MEASURED: these hold on every path tested. A text the front end refuses, and the budgets `1e6`, `-1`, `05` and `+5`, each end exit 3 with a `RUNNER-FAULT` line, and `classify` raises on them. That is so in `ref_run.py`, in `classify` and in Amendments 5 and 6.

At the edges the line breaks. An interrupt, or a platform query that fails, outside the runner's two guarded blocks is classed NO-REFERENCE-RESULT. A reference that ends by SIGABRT is classed a runner fault (X4).

### 1(c). Interruption of the whole experiment

The sheet states the rule: an interruption voids the whole experiment, its records are kept, its partial results never count, and it is repeated. But what "the experiment" covers is undefined (X6).

The one existing harness does the opposite of keeping records. On a runner fault it writes nothing and deletes its folders, and it detects the fault only after all 20,000 runs are made (X10).

### 1(d). The recurring-fault stop

- **What holds.** "The same" is defined (the same `RUNNER-FAULT` line, at the same case). A second fault of any kind stops the procedure and goes to the owner, so nothing can be retried on its own.
- **Relabelled.** Possible at the edges (X4).
- **Lost.** Possible for three kinds of fault (X7, X8):
  - a runner fault with no line;
  - an interruption from another cause on the repeat;
  - a process that could not be started.

### 2. The runner: every exit path

The documented ends all work as documented:
- exit 0 with a `RUN` line or a `DECODER-REFUSED` line;
- exit 1 with `REFERENCE-EXCEPTION`;
- exit 3 with `RUNNER-FAULT`.

The undocumented ends, all MEASURED (`interrupts.py`, `exitcodes.py`, `edges.py`):

| how it ends | what `classify` makes of it |
|---|---|
| an interrupt during the ENV line, or during the runner's own module imports | exit `0xC000013A`, "KeyboardInterrupt": NO-REFERENCE-RESULT |
| an `OSError` from `platform.platform()` | exit 1: NO-REFERENCE-RESULT |
| an interrupt inside the crash handler | exit 1 with no `REFERENCE-EXCEPTION` line: NO-REFERENCE-RESULT, type `none` |
| the reference raising SIGABRT | exit 3 (Windows' C runtime): `RunnerFault("exit 3 without its line")` |
| `orlog` cannot be imported | `REFERENCE-EXCEPTION builtins.ModuleNotFoundError`: NO-REFERENCE-RESULT (decoder1's import failure is a runner fault) |

Eleven runner changes pass `ref_run_paths.py` 31 of 31 (X3).

Runner faults are kept apart from core faults and from external termination. A reference timeout is a class input, as Amendment 1 says.

### 3. The generators (MEASURED: each run twice into my scratch folder and compared with `cmp`)

- **Byte-identical twice:**
  - `gen_r5_budgets` gives `r5-budgets.txt` (`27b38350…`);
  - `gen_stress_texts` gives `stress-texts-2.txt` (`ea542dd1…`);
  - `gen_r2b_twins` gives `r2b-twins.txt` (`ef204d4d…`);
  - `gen_r6_mutants` gives `r6-mutants.txt` (`a8f704fb…`, 17,155,925 bytes);
  - `gen_s3_budgets` gives `s3-budgets.txt` (`86f3a7b0…`).
- **Identical to the -7 records:**
  - the R2b checker mode gives `evidence/rust-core-r2b-checker-7.txt` (`f53bed40…`), agreeing on 1,558 of 1,558;
  - the R6 checker mode gives `evidence/rust-core-r6-checker-7.txt` (`8a47f8fc…`), accepting 538 and crashing on none.
- **The 61 moved verdicts** between checker-6 and checker-7 are all swap mutants, each W5 to W5 on another line, as the sheet says.
- **`r6-reference.txt` and `r6-reference-2.txt`** have equal rows. Only their headers differ.

### 4. The preregistered sample

- **The rule and the list** are in `%TEMP%\reread7-2\sample.txt` (`⟦HOME83⟧\AppData\Local\Temp\reread7-2\sample.txt`), sha256 **`aa177198f74e02e6d9b3e01db660477c6e6af4e81d2410775b0e45877c629874`**. I wrote it before running any mutant.
- **The rule** is the union of nine strata:
  - **A:** all 43 RecursionError mutants;
  - **B:** every mutant of a crash type with fewer than 20 members (AttributeError, IndexError, struct.error, TypeError: 27);
  - **C:** all 17 RUN STOPPED mutants;
  - **D:** all 61 mutants whose checker verdict moved between -6 and -7;
  - **E:** for each (operator, outcome kind) cell, its 3 lowest- and 3 highest-numbered mutants (132);
  - **F:** for each operator, the 5 lowest- and 5 highest-numbered mutants the checker accepts (30; truncate has none);
  - **G:** the 5 smallest and 5 largest mutants by bytes;
  - **H:** the 10 RESULT mutants with the greatest ops;
  - **I:** 120 more by `random.Random(20261102).sample` of the rest.
- **What it covers.** 390 mutants:
  - the classes: RESULT 165, REFERENCE-REFUSED 120, NO-REFERENCE-RESULT 105;
  - all 8 crash types;
  - all 4 operators;
  - all three RUN kinds.
- **The results.** `sample-results.txt` (`4f68e5dd…`). Each mutant ran twice, each run a fresh process in a fresh empty folder, under a 60-second limit, classed by `ref_run.classify`.
  - **390 of 390 rows equal to `r6-reference-2.txt`.**
  - 0 runner faults, 0 folders not empty, 1 environment.
  - The slowest runs (software wall time, 6 workers):

| mutant | run 1 | run 2 |
|---|---|---|
| 09729 | 56.89 s | 53.57 s |
| 09270 | 12.25 s | 16.92 s |
| 05498 | 10.26 s | 10.80 s |

  - I timed 09729 again alone: 44.00 s and 48.47 s. See X5.
- **Concurrency.** The sample ran with 6 worker threads, before your note on capacity. No process creation failed (WinError 1450 or otherwise), so I re-ran no case. Everything after your note ran at most one process at a time.

### 5. Hash closure

Pending; see the last line.

## Findings

### X1 — MAJOR. The equivalent-mutant route lets an echoing core through R7's writer plants. (Reasoned.)

- **Where.**
  - SHEET.md:107: *"R7 requires each to be caught. One that is not is reported, and measured as equivalent where it is."*
  - SHEET.md:748–749: *"Every plant caught or declared equivalent by measurement."*
  - SHEET.md:668–676 (Amendment 6): *"R2 must catch each … A core whose write-back copies its input would let both pass, so R7 fails it."*
- **The problem.** In an echoing core, a plant in the writer changes no output on any input. That is exactly an equivalent mutant, so section 7's route can declare it equivalent. Amendment 6 asserts that R7 fails such a core, but it does not take the writer plants out of that route.
- **Proposal.** State that neither writer plant may ever be declared equivalent. A writer plant that R2 does not catch fails R7, and it goes to the owner as evidence that the write-back does not come from the writer.

### X2 — MAJOR. The reading of OUT's provenance has no consequence, no ordering in the sheet, and no place in acceptance. (Reasoned.)

- **Where.**
  - SHEET.md:677–679: *"The provenance of OUT is recorded by the independent source reading"*.
  - LAW-FORMAT-0-DRAFT-7.md:103–106: the same.
  - Section 7 (SHEET.md:746–750) is not amended.
- **Compare exit 5.** SHEET.md:383–386: *"If it finds another path, no exit 5 is RESOURCE-EXHAUSTED: each is CORE-FAULT, and the finding goes to the owner"*, and Amendment 3 adds that reading to acceptance (:390).
- **What is missing.** Nothing says what follows if the reader finds a path that copies the input into OUT.
- **Proposal.**
  - Add to section 7: "OUT's provenance reading recorded, before R2 counts."
  - If the reading finds such a path: no WRITTEN-BACK counts toward R2, R2 fails, and the finding goes to the owner.

### X3 — MAJOR. `ref_run_paths.py` does not hold the runner to what Amendment 6 says. Eleven changes pass 31 of 31. (MEASURED.)

- **Where.**
  - SHEET.md:704–705: *"holds it to its run conditions as well as its endings"*.
  - SHEET.md:711–714: the five changes REREAD-6 showed now fail.
  - ref_run_paths.py:159: the only check of an outcome line's content, `run_ok = what != "text: a text the front end accepts" or …`.
  - ref_run_paths.py:175–182: the made-up cases have no pair of unequal results and no pair of unequal refusals.
  - ref_run_paths.py:188–193: the source check is a substring search.
- **What I ran.** `variants.py` and `variants2.py` make copies in my scratch folder and run each copy of the runner through a copy of the check. The control prints `REF-RUN PATHS HELD: 31 of 31`. Each of these also prints 31 of 31:

| change | changes a deterministic record's rows? |
|---|---|
| V1: law mode ignores BUDGET | yes (17 STOPPED rows) |
| V2: law mode's law seal taken from the bytes less their last LF | yes |
| V3: decoder1's message dropped | yes |
| V4: a `KeyError` from `decode` taken as decoder1's refusal | yes (117 rows) |
| V5: the STOPPED line reports one operation more | yes |
| V6: `classify` makes two different RUN lines RESULT | **no** |
| V7: `classify` makes two different refusals REFERENCE-REFUSED | **no** |
| V8: the recursion limit raised after the ENV line, by `getattr(sys, 'setrecursion'+'limit')` | **no** |
| V9: BUDGET read from an environment variable via `from os import environ` | **no** |
| V10: P keeps the text-seal line in law mode only | yes |
| V11: an `IndexError` in law mode's run reported as decoder1's refusal | yes |

  V8, V9 and V10 are the same kinds of change as REREAD-6's five, in another form.
- **Why it matters.** The ENV line is printed before the reference's modules are imported (ref_run.py:189–193, then `reference()`), so it cannot witness what those imports do. Today they change nothing: limit 1000, `format_check` not imported (MEASURED, `conditions.py`).
- **Proposal.**
  - Check law-mode outcome lines (completed, stopped with a numeric budget, refused, the refusal's message) against the check's own computation.
  - Check the STOPPED line's content.
  - Add made-up cases for two unequal results and two unequal refusals.
  - Print a second conditions line after the imports and after the run.
  - Replace the substring check with an AST check (no `environ`, `getenv` or `setrecursionlimit` name; no `getattr` on `os` or `sys`), or describe it as a substring check.

### X4 — MAJOR. Runner faults and reference crashes cross into each other at the edges. (MEASURED.)

- **Where.**
  - ref_run.py:184–191: the arguments are in a `try`, but the ENV `print` and `platform.platform()` are outside any `try`.
  - ref_run.py:39–44: the module imports run before `main`.
  - ref_run.py:197–204: the crash handler.
  - ref_run.py:72–73: `if status == 3 or err.startswith("RUNNER-FAULT "): raise RunnerFault(...)`.
- **The cases** (`interrupts.py`: the real runner, run by `runpy` after one library call is made to fail; two fresh runs each):

| case | exit | stderr's last line | `classify` |
|---|---|---|---|
| env-interrupt | 3221225786 | `KeyboardInterrupt` | NO-REFERENCE-RESULT |
| env-oserror | 1 | `OSError: a platform query that fails` | NO-REFERENCE-RESULT |
| import-interrupt | 3221225786 | `KeyboardInterrupt` | NO-REFERENCE-RESULT |
| handler-interrupt | 1 | (empty) | NO-REFERENCE-RESULT |
| sigabrt | 3 | (empty) | RunnerFault raised: exit 3 without its line |

- **What makes them possible.**
  - `exitcodes.py`: `faulthandler._sigabrt()` ends with status 3 on Windows.
  - The sheet gives a process group of its own only to the core (SHEET.md:536–537), so a console interrupt still reaches every reference run.
- **Against his words.** *"Keep runner faults distinct from reference exceptions"*; *"Do not … relabel it as a reference outcome."*
- **Proposal.**
  - Guard all of `main` (the ENV line included) and the module imports, so that any failure before `reference()` is a runner fault.
  - Start reference runs in their own process group, as the core's.
  - Treat exit 3 without the line as an anomaly of its own: stop and report it, recorded apart from the recurring-fault rule's runner faults.
  - Treat any exit status the runner does not define (other than 0, 1 and 3) together with "KeyboardInterrupt" on stderr as an interruption, never a reference crash.

### X5 — MAJOR. Some reference outcomes depend on host load, within seconds of the 60-second limit. (MEASURED.)

- **Where.**
  - SHEET.md:123: a 60-second limit for each reference run.
  - SHEET.md:633–634: the rows equal *"as predicted, since no mutant's run meets a fault of the runner"*.
  - gen_r6_reference.py:33: `WORKERS = 8`.
- **Mutant 09729** (TypeError, NO-REFERENCE-RESULT): 44.00 s and 48.47 s alone; 56.89 s and 53.57 s in my 6-worker sample. One timeout makes it UNSTABLE. Two make the row read `timeout`. Either changes the record's row, which puts hash closure and "made twice with identical bytes" at risk.
- **`s2-doubling-24`:**
  - with no budget: 36.83 s alone;
  - with budget 10: 30.44 s, then RUN STOPPED at **25,165,823** operations.
- **Mutants 05498 and 09270:** RESULT with 20,000,060 and 20,000,059 operations under a budget of 1,000,000. Their `while` loops run with no statement inside, so the check at each statement's entry (interp.py:151, :221–228) is never reached.
- **Proposal.**
  - Record every run's wall time.
  - Flag every case with a run over half the limit, and list it with the record.
  - Make records with at most 4 workers.
  - Say in the sheet that these outcomes depend on load.
  - Predict "rows equal" only with that caveat.

### X6 — MAJOR. "The experiment" and "the repeat" are undefined. (Reasoned.)

- **Where.**
  - SHEET.md:536–538 (K14), :600–601 (N3), :620–621 and :686–697 (U2).
  - SHEET.md:748: *"R1–R8 held, each run twice with byte-identical output"*.
- **Questions the text does not answer.**
  - Is an experiment one prediction's run, or every one of R1–R8 and S1–S4?
  - Section 7 needs two whole runs. Does a fault in the second void the first?
  - Is the re-run of the second run "the repeat"?
  - Is a void attempt one of the two?
- **Proposal.** Define an "attempt": every prediction's cases, in a fixed order, from fresh builds. Ask the owner whether an interruption voids only the attempt in progress or both.

### X7 — MINOR. The recurring-fault rule leaves cases open. (Reasoned.)

- **Where.**
  - SHEET.md:693: *"the same `RUNNER-FAULT` line, at the same case"*. A fault with no line (`classify`'s "exit 3 without its line", ref_run.py:73) has no line to compare.
  - SHEET.md:696–697: an interruption by another cause is *"handled the same way"*. It does not say whether the stop after one repeat applies, or what happens to a runner fault followed by a console interrupt.
  - LAW-FORMAT-0-DRAFT-7.md:780–783: *"run again from its start"*, with no stop.
  - ref_run.py:27–28: the docstring omits the different-fault-on-the-repeat case.
- **Proposal.**
  - Apply the stop after one repeat to every interruption.
  - Key "the same" on the fault's record: its line, or "no line" with its exit status.
  - Align the draft and the docstring with the sheet.

### X8 — MINOR. A run the harness cannot start has no place in the protocol. (Reasoned; you reported that it occurred at 17:40, WinError 1450.)

- **Where.**
  - No class for it in the sheet.
  - gen_r6_reference.py:57–59: `subprocess.run` raising `OSError` in a worker thread ends the generator uncaught and writes nothing.
- **The gap.** Such a run is not a runner fault (no line, and `classify` never sees it), not a reference class, and not a core class.
- **Proposal.** Name it a harness fault: an interruption, kept with its `OSError`, under the same repeat and stop rules, and never retried case by case.

### X9 — MINOR. R2's power on list order is thin, and its counts are of texts, not laws. (MEASURED, `list_orders.py`, `over_distinct.py`.)

- **`over` lists.** Of 95 lists, 3 have two or more entries, and all are `(over 1 2 3 4)`. None of the 95 is out of ascending order, and none repeats an entry. So a writer that writes `over` lists sorted, or as a set, passes R2 on every text. Section 8 allows any order and repeats; section 9 requires the written order.
- **`given` lists.** 2 laws hold one that is not ascending.
- **The counts.** SHEET.md:670–674 says "154 of the 298 laws" and "3 of the 298 laws". These are texts: 91 and 2 distinct laws.
- **Proposal.**
  - Add write-back fixtures with `over` and `given` lists that are unsorted and that repeat an entry.
  - Say "texts" and give the distinct counts.

### X10 — MINOR. `gen_r6_reference.py` contradicts the rule that records are kept, and its own docstring. (Reasoned, from code.)

- **Where.**
  - gen_r6_reference.py:10–11: *"A fault of the runner stops it, and nothing is written."*
  - gen_r6_reference.py:107–120: it makes all 20,000 runs, then classifies, then exits and deletes its folder.
  - gen_r6_reference.py:114–116 and :139: the ENV lines are only collected into one set in the header, never checked per run. A run under a raised recursion limit would be recorded, not refused.
- **Proposal.**
  - Classify as runs finish.
  - Stop at the first fault.
  - Keep raw runs.
  - Refuse any run whose ENV line differs from the expected default.

### X11 — MINOR. The `trace` digest is not of a trace file's bytes. (MEASURED, `edges.py`.)

- **Where.**
  - ref_run.py:165–171: the digest is of `"\n".join(it.trace)`, and `--files` writes `reference.trace` the same way, with no final LF.
  - RUNTIME-SPEC.md:144: each trace line ends with `\n`.
- **Measured.** The RUN line's digest equals sha256 of `reference.trace` (`True`), and does not equal the digest of the file as RUNTIME-SPEC §5 writes it (`False`).
- **Effect.** A harness that compares sha256 of the core's TRACE file with the digest disagrees on every case with an event.
- **Proposal.** The sheet states how the trace is compared.

### X12 — MINOR. The 600-second build limit has no outcome. (Reasoned.)

- **Where.** SHEET.md:125 is the only mention.
- **Proposal.** Say what a build past the limit is: an interruption, or a failure of the milestone.

### X13 — MINOR. The runner pins decoder1 alone, and treats a broken `src/` as reference crashes. (MEASURED.)

- **Where.** ref_run.py:132–133 imports `orlog` inside the guarded block.
- **Measured.**
  - `orlog` not importable: exit 1, `REFERENCE-EXCEPTION builtins.ModuleNotFoundError`, classed NO-REFERENCE-RESULT. Every case of a broken `src/` would read so.
  - decoder1's import failure is a runner fault (ref_run.py:149–152).
  - decoder1 brings in 8 `orlog` modules and nothing else from `research/law-sufficiency/` (`conditions.py`). None of the 8 is pinned by the runner.
  - `-B` stops Python writing bytecode, not reading it (reasoned). No `__pycache__` exists in `src/orlog` or `research/rust-core` today.
- **Proposal.**
  - Make an import failure of `src/` a runner fault.
  - Record the `orlog` modules' sha256 in each run's ENV line, or hold them to the commit in the harness, as the generators do.

## Files created

All are under `⟦HOME83⟧\AppData\Local\Temp\reread7-2\`.
- **Scripts:** `exitcodes.py`, `writer_plants.py`, `over_distinct.py`, `list_orders.py`, `select_sample.py`, `run_sample.py`, `variants.py`, `variants2.py`, `conditions.py`, `interrupts.py`, `edges.py`.
- **Sample:** `sample.txt` and `sample-results.txt`; the logs `run_sample.log`, `gen\gen.log` and `gen\s3.log`.
- **ref_run_paths output:** `paths-run1.txt` and `paths-run2.txt`.
- **Regenerated files, in `gen\`:** `r5-1.txt`, `r5-2.txt`, `stress-1.txt`, `stress-2.txt`, `r2b-1.txt`, `r2b-2.txt`, `r2b-checker.txt`, `r6m-1.txt`, `r6m-2.txt`, `r6-checker.txt`, `s3-1.txt`, `s3-2.txt`.
- **Copies for X3:** `variants\v00`–`v10` and `variants2\v00`–`v01`, each holding a `ref_run.py` and a `ref_run_paths.py`.
- **Other inputs:** `solo\09270.law` and `solo\09729.law`; `stress\` (the 14 texts and their law bytes, 28 files).
- **`tmp\`:** empty at the end.

## Appendix: commands and their outputs

- **The runner's check, twice.** `python -B research/rust-core/ref_run_paths.py` (twice): exit 0, the two outputs identical, and equal to the evidence file's body once CR is removed. Last line: `REF-RUN PATHS HELD: 31 of 31 as stated`.
- **`writer_plants.py`:**
  - `let-name plant changes the bytes of 154 of the 298 laws; 91 distinct laws`
  - `over-reversal plant changes the bytes of 3 laws` (each `[['1','2','3','4']]`)
- **`over_distinct.py`:** `mutant/s1/0485 c464c0777b47ea54`, `n23… c464c0777b47ea54`, `mutant/s1/2049 bfaf583389deddb2`.
- **`list_orders.py`:**
  - `over lists 95; of 2 or more entries 3; … not in ascending order 0; with a repeated entry 0`
  - `given lists 57; of 2 or more entries 3; … not in ascending order 2; with a repeated entry 0`
- **`variants.py` and `variants2.py`:** the control and V1–V11 each print `exit 0  REF-RUN PATHS HELD: 31 of 31 as stated []`.
- **`conditions.py`:**
  - `recursion limit before 1000, after the imports 1000`
  - `format_check in sys.modules after the imports: False`
  - `modules imported from research/law-sufficiency: 1: decoder1`
  - and from `src`: 8 modules.
- **`exitcodes.py`:** `os.abort()` 3221226505; `faulthandler._sigabrt()` **3**; uncaught `KeyboardInterrupt` 3221225786; `sys.exit(3)` 3.
- **`interrupts.py`:** the table under X4.
- **`edges.py`:**
  - `(1) reference.trace: 151 bytes, 1 LF, ends with LF: False`, digest equals the file `True`, equals the line-per-LF form `False`
  - `(2) orlog not importable: exit 1, stderr last 'REFERENCE-EXCEPTION builtins.ModuleNotFoundError', classify: NO-REFERENCE-RESULT`
- **`run_sample.py`:** `sample 390 mutants, 2 runs each; rows equal to r6-reference-2.txt: 390; differing: 0; runner faults: 0; folders not empty before or after: 0`; slowest `09729 56.89 s, 09270 16.92 s, 05498 10.80 s`.
- **Solo timing:** `09729 … exit 1 44.00 s alone`, `48.47 s alone` (`TypeError: both arguments should be Rational instances`, then `REFERENCE-EXCEPTION builtins.TypeError`); `09270 … 10.21 s`, `9.14 s`.
- **Stress timing** (text mode, one run each):
  - `s1-*-300` complete with 301 operations;
  - `s1-*-600/3000/30000` end in `REFERENCE-EXCEPTION builtins.RecursionError`;
  - `s2-doubling-24 budget none 36.83 s RUN COMPLETED ops 25165824`;
  - `s2-doubling-24 budget 10 30.44 s RUN STOPPED ops 25165823`.
- **Generators:** see question 3 (`GEN-R5 … 27b38350`, `GEN-STRESS … ea542dd1`, `GEN-R2B … ef204d4d`, `GEN-R2B --checker … f53bed40`, `GEN-R6 … a8f704fb`, `GEN-R6 --checker … accepted 538; crashed 0; 8a47f8fc`, `GEN-S3 … RESULT 298; 2100 values; 86f3a7b0`). Each was `cmp`-identical to its frozen file.
- **The two reference records:** `diff <(tail -n +8 r6-reference.txt) <(tail -n +8 r6-reference-2.txt)` reports `ROWS-EQUAL`.

HASH CLOSURE: PENDING
