> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on REREAD-9's ASK 9-2): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-8, reader 2 of 3: the protocol, the runner and the evidence, its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-8 ran
as three readers working at the same time, under the owner's F2 (RULINGS.md): reader 1 the format and the checker,
reader 2 the protocol, the runner and the evidence, with the hash closure of `r6-reference-5.txt`, reader 3 the rulings
and cross-document consistency. Each started fresh, had its own scratch folder and its own letter for findings (ZA, ZB,
ZC), and saw nothing of the others' work. Each was briefed:
- to check, before reading, the sha256 of every file it read against the brief's pins, among them draft 8 (`94a989a6…`),
  SHEET.md (`b9a3057e…`, Amendment 7 with the record `r6-reference-5.txt`, `636a2873…`) and RULINGS.md (`387ef2e8…`);
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, run at most two processes of its own at
  once, and change nothing in the repository; reader 2 was told not to run mutant 09729, which commits about 24 GiB.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-8, reader 2 of 3: the protocol, the runner and the evidence (findings ZB1–ZB12)

## 1. What I read and ran, and what I could not check

**Pins.** All 24 pinned files have the sha256 values the brief gives (MEASURED, `sha256sum`). `research/law-sufficiency/decoder1.py` is `3584f565f6929879…` (MEASURED). HEAD is 2e9805aaa1ce….

**Read.**
- SHEET.md, whole, with Amendments 5–7 read closely.
- RULINGS.md, the sections "REREAD-7 as three readers", "REREAD-7's dispositions adopted, A to F" and "The R6 remake".
- REREAD-7-DISPOSITION.md, ASK C and ASK D and the lines on X10, X5 and B3.
- The code: `ref_run.py`, `ref_run_paths.py`, `ref_run_variants.py`, `gen_r6_reference.py`, `gen_r2_fixtures.py`, `run_format.py`, and the functions `mutants`, `refuse_if_moved`, `sources` and `checker` of `gen_r6_mutants.py` (`ae64f829…`, as Amendment 3 pins).
- The records: `r6-reference-5.txt`, `r6-reference-3.txt` and `research/rust-core/r6-reference-4.txt`; `r2-writeback-fixtures.txt`; the evidence files `-8` (ref-run-paths, ref-run-variants, r6-checker, r2b-checker).
- Under `work/rust-core/`: all four attempt folders (`attempt.json`, `runs.jsonl`, `host.jsonl`, `end.json`), the three generation files, and the two generator logs.

**Ran.** Every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, with TEMP and TMP set to my scratch folder. I never ran more than two processes of my own at once. No process failed to start (no WinError 1450).
- **R6 sample.** I froze the sampling rule before looking at any outcome, then re-ran 93 mutants, each twice through the runner, in two passes (A and B).
- **14 generator plants**, in a byte-identical copy (`cc63252d…`) outside the repository.
- **Runner stand-ins** (a `SystemExit` while the reference's modules import).
- `ref_run_paths.py`, twice.
- **The runner variants**, run one at a time: the repository's 15, plus 5 of mine.
- **R2 fixtures:** `gen_r2_fixtures.py`, twice, into scratch, and an independent check of each fixture through `format_check`.
- **The checker records `-8`**, remade into scratch.
- **Analyses:** the records against each other; the rows rebuilt from `runs.jsonl` through `classify`; the timings and host readings; a simulation of the four-worker pool.

**Not checked.**
- **Mutant 09729: I did not run it** (the brief). I read its rows from the attempt records. So its 24.06 GiB peak and 42.5 s when run alone are not re-measured.
- The source of generator `48d88b21…`, which made `r6-reference-4`, is not where I may read. So I cannot check that the generator changed "only where this ruling asks".
- Amendment 6's figures of 1,673 s and 1,752 s.
- What else ran on the host during the generations: only host totals are recorded.
- The `r6-reference-4` attempts keep no time for each run.
- No UNSTABLE case exists in the record, so none was sampled.

**Disclosures.**
- **First `git status`.** At the start I ran `git status --porcelain=v2 --untracked-files=all` without `GIT_OPTIONAL_LOCKS=0`, so git may have refreshed `.git/index`. No tracked content changed. Its output listed file names under `research/law-sufficiency/`; I opened none of them and relied on none.
- **`work/` listing.** One `ls -la work/` listed `work/`'s top-level folder names, which is outside the `work/rust-core/` my part allows. I opened nothing there.
- **decoder1 lines.** The tracebacks stored in `runs.jsonl` quote short lines of `decoder1.py`. I saw them in passing while reading run records the brief allows.
- **Clean state.** Afterwards: no `__pycache__` in `src/orlog` or `research/rust-core`, and the runner raises no bytecode fault, so there is none in `research/law-sufficiency` either. No file in `research/rust-core`, `evidence` or `work/rust-core` is newer than SHEET.md (23:03). `git status -- src tests vectors` is empty.

## 2. Verdict

**`r6-reference-5.txt` is what Amendment 7 says, and its hash closure passes.**
- It is byte for byte both generations' files.
- Each generation's file has the sha256 its attempt's `end.json` names.
- Its rows equal `r6-reference-3.txt`'s and `r6-reference-4` generation 1's, all 10,000.
- Its header names the runner, generator, decoder1, `interp.py`, the mutants and the five ENV modules by their current sha256.
- Generation 1 ran to completion before generation 2 started (gap 0.489 s), four workers each. Every figure in Amendment 7's tables reproduces from the attempt records.
- My frozen sample of 93 mutants reproduces its rows exactly, twice.

**The protocol holds, with gaps.**
- **One MAJOR finding (ZB1):** a harness fault in the first lines of an attempt, before `attempt.json` is written, leaves no record and does not count toward the stop rule. It did not happen in the `r6-reference-5` attempts, so the record is unaffected.
- **Eleven MINOR findings:** a runner edge that `classify` would mis-class, gaps in the runner check's power, wrong counts and wording in the sheet, a figure that undercounts, and attempt records that would not be pushed with the record.
- No BLOCKER.

## 3. Answers

### Q2: the experiment (his B1–B5) and his R6 remake ruling

**Is an experiment one complete attempt, and are B1–B5 stated alike?** Yes, in substance (MEASURED for the code paths below, REASONED for the wording).
- The sheet states the experiment as one complete attempt (SHEET.md:783–788).
- The runner's docstring says the attempt is kept and repeated whole, and that a second interruption of any cause stops it (ref_run.py:30–32).
- The generator implements this per generation: an experiment is `r6-reference-5-gen<N>`, with `next_attempt` at :196–206 and `generation` at :290–434.
- B1 and B3 (stop when the repeat is interrupted, by any cause), B2 and B4 agree across all three, apart from ZB1 and ZB11.
- B5 (a slow build) concerns the core's build, and neither the runner nor the generator builds anything.
- The generator also records causes the sheet does not list: ENV-MISMATCH, RUN-LEFT-FILES, and the STOPPED-ANOMALY disposition. All of them stop the attempt. That is consistent with D5 and with "one terminal disposition with its cause".

**What the generator does with interruptions** (all MEASURED by plants):

| plant | what was planted | what happened |
|---|---|---|
| P2a | a process fails to start | attempt INTERRUPTED with cause HARNESS-FAULT; runs and the `start_failure` line kept; no generation file; generation 2 NOT STARTED |
| P2b | run again | attempt `a2`, `retry_of a1`, all cases run again: the repeat is whole |
| P3 | interrupted twice | a third attempt is REFUSED: "interrupted on its repeat; it stops, and goes to the owner" |
| P4 | a real runner fault (BUDGET written `05`) | INTERRUPTED with cause RUNNER-FAULT |
| P5 | `classify` raises an anomaly | STOPPED-ANOMALY, then later attempts refused |
| P6 | `classify` raises an interruption | INTERRUPTED, then `a2` |
| P7 | an operator's interrupt | INTERRUPTED with cause OPERATOR-INTERRUPT |
| P8 | an attempt folder with no `end.json` | counted as interrupted: the next attempt is `a2` |

- Workers are never reduced. `WORKERS` is a constant, and after a start failure the attempt stops; only the case already running finishes.
- A generation file is written only by a COMPLETED attempt.
- **The exception is P11 (ZB1):** a harness fault before `attempt.json` leaves no record and is not counted.

**His R6 remake ruling, items 1–5.**
- **Generation 2 starts only once generation 1 has completed.**
  - In code: :462–463 and :489–494. P12: `--only 2` first is refused.
  - In the records: no generation-2 run starts before generation 1's last run ends. The gap is 0.489 s, and the host readings' spans are disjoint (generation 1's last reading at …759.642, generation 2's first at …760.656).
- **Each run's start and end are kept:** all 40,000 run lines of `r6-reference-5` have `start` and `end`.
- **The host's commit before, during and after:** `host_before` in `attempt.json`; 5,072 and 5,421 readings in `host.jsonl`, 0.49–0.60 s apart; `host_after` in `end.json`.
- **A record only from two completed, byte-identical generations, never one selected:** code at :530–557. P9 (generations differ): NOT EQUAL, no record. P10 (generation 1's file changed after completion): "not the one … completed with", no record. P2 and P3 (incomplete): nothing compared. The record is written only when generation 1's bytes equal generation 2's.

### Q4: his D5

**Every failure before the reference begins is a runner fault:** yes, for every path tested, with one exception.
- Tested: usage errors, budget and seal forms, an unreadable input, imports of `orlog` and decoder1 that raise ValueError or ImportError, the platform query failing or interrupted, a wrong pin, a plant, a `__pycache__` folder.
- **The exception (ZB2):** a `SystemExit` raised while the reference's modules import escapes, and `classify` returns NO-REFERENCE-RESULT.

**Exit 3 without the runner's line is an anomaly:** yes. `classify` raises it (:108–109); the generator ends STOPPED-ANOMALY and refuses later attempts (P5).

**An undefined exit status with KeyboardInterrupt is an interruption:** yes (:110–111; made-up runs both ways; P6).

**The ENV line carries the `orlog` modules by sha256:** yes, every module loaded when it is printed, each matching its file. That is five in law mode and eight in text mode; the sheet's "eight" is wrong (ZB4).

**It refuses a `__pycache__`:** yes, in all three folders (:77, :163–165).

**Does `ref_run_paths.py` hold all this?** Mostly. It reproduces its record byte for byte: 43 of 43, twice. It does not hold the `SystemExit` edge, the completeness of the ENV line, which folders the bytecode check covers, or the implementation and version (ZB2, ZB3).

**Does `ref_run_variants.py` show what it says?** Yes. Run one at a time here, it gives 14 of 15 changes caught and V11 not caught, with every row's "n of 43" equal to the record's. But it makes four of REREAD-6's five changes, not five (ZB5).

A note, not a finding: the docstring says the runner reads no environment variable. Its own source reads none, which is what the check's syntax-tree rows hold. But `platform.platform()` reads `PROCESSOR_*` environment variables on Windows (`platform.py:877–892`).

### Q6: the remakes and the hash closure

**`r6-reference-4` failed verification as Amendment 7 says** (MEASURED).
- Exactly one row of 10,000 differs: 09729, `crash exit 1 type builtins.TypeError` in generation 1 against `builtins.MemoryError` in generation 2. Its class is the same in both.
- Generation 1's rows are `-3`'s, every one.
- Generation 2's two runs of 09729 ended in MemoryError after 1.35 s and 0.98 s of wall (0.23 s and 0.34 s of CPU). Generation 1's runs ran 38.4 s and 39.5 s and ended in TypeError ("both arguments should be Rational instances").
- Its figures equal `end.json` exactly:

  | | wall | CPU | workers | start failures | runs past 30 s |
  |---|---|---|---|---|---|
  | generation 1 | 3,931.01 s | 4,290.3 s | 4 | 0 | 38.407 s and 39.521 s (both 09729) |
  | generation 2 | 3,928.778 s | 4,238.885 s | 4 | 0 | none (longest 14.58 s) |

  Peak commit 49,050,554,368 B (45.68 GiB); peak physical memory 12,474,916,864 B (11.62 GiB).
- **The cause.** The 24.06 GiB peak alone was not re-run. It agrees with `r6-reference-5`'s peak less its baseline, 45.30 − 21.26 ≈ 24.0 GiB (REASONED).
- **The timing.** "About four seconds before" is not supported (ZB8).
- **Named nowhere as a record.** SHEET.md:994 says so in terms. RULINGS.md:741 and REREAD-7-DISPOSITION.md:385 name it only as the record then planned. The way its two files are kept is uneven (ZB12).

**`r6-reference-5` was made as his ruling says** (MEASURED unless marked).
- Generation 1 ran to completion with four workers, then generation 2 with four workers. Both attempts list the same runner (`822c826e…`) and generator (`cc63252d…`).
- The two generations do not overlap.
- **Nothing heavy beside either.** The host's commit outside 09729's 72 s window stayed between 20.99 and 21.59 GiB in generation 1, and between 20.97 and 21.47 GiB in generation 2. Its median by tenths of each generation was 21.0–21.3 GiB. The records cannot show load other than memory commit, and two things go unexplained:
  - generation 2 took 6.9% more wall time for about the same CPU;
  - the median physical memory in use was 8.47 GiB in generation 1 and 7.22 GiB in generation 2.

  "Nothing is run beside either generation but edits of the documents and reading" is DECLARED (RULINGS "As kept").
- **Every figure in the table reproduces:**

  | | wall | CPU | commit before | peak commit | commit after |
  |---|---|---|---|---|---|
  | generation 1 | 2,573.1 s | 3,519.1 s | 21.24 GiB | 45.30 GiB | 21.04 GiB |
  | generation 2 | 2,749.7 s | 3,532.3 s | 20.98 GiB | 45.29 GiB | 21.13 GiB |

  - Each generation: 4 workers, 0 start failures, one attempt and no interruption.
  - Runs past 30 s: 09729's alone, at 37.0 s and 34.6 s in generation 1, 36.4 s and 35.2 s in generation 2.
  - Peak physical memory in use: 11.62 GiB in each.
  - The commit limit read 47.62 GiB throughout.
  - The peak fell inside 09729's first run, with 2.32 GiB and 2.33 GiB of commit left.
  - 09729's two runs were 5 ms and 7 ms apart.
  - In generation 2, 09758 took 22.5 s of wall for 0.45 s of CPU.
  - Generation 2's "commit before" was read after generation 1's "commit after" (…760.513 against …760.206).
- **09729's rows, from the attempt records:** TypeError in all four runs of `r6-reference-5`.

**Hash closure: passed** (MEASURED).
- `sha256(r6-reference-5.txt)` is `636a287364982201638149bd318169cd4d2a8e49bd3ec1bb23222de508f88be5`. That is the value at both places Amendment 7 states it, SHEET.md:950 and :989. No other document states it.
- It equals `work/rust-core/r6-reference-5.gen1.txt` and `.gen2.txt` byte for byte. Both attempts' `end.json` give that `output_sha256`.
- Its rows equal `r6-reference-3.txt`'s: 10,000 rows, none different.
- **Its header against the files now:**

  | header names | sha256 | equals the file now |
  |---|---|---|
  | generator | `cc63252d…` | yes |
  | runner | `822c826e…` | yes |
  | decoder1 | `3584f565…` | yes |
  | `src/orlog/interp.py` | `f8432918…` | yes |
  | `r6-mutants.txt` | `a8f704fb…` | yes |
  | the five ENV modules | each its own | yes, each |

- The rows rebuilt by `classify` from each attempt's raw `runs.jsonl` equal that generation's file, for all four attempts. Each attempt has one distinct ENV line, which is the header's.

### Q1, part: R2's write-back fixtures

The answer is yes, measured on every count:
- There are 11 fixtures.
- Each row's bytes have the sha256 the row states.
- `format_check` (`3bc07ca8…`) accepts each and writes each back exactly: 11 of 11.
- `gen_r2_fixtures.py` (`0336d05e…`, as named in the header and in Amendment 7's table) makes the file twice, byte for byte equal to the frozen `2e13265a…`.
- The generator's claims about the 298 laws hold: three texts (two distinct laws) hold an `over` list of two or more, all in order; three texts (two laws) hold a `given` list of two or more, two of them `(given 2 1)`.
- One fixture of the 11 does not match the description "out of order or repeats an entry" (ZB7).

**The checker's records `-8`.**
- `gen_r6_mutants.py --checker` remakes `rust-core-r6-checker-8.txt` byte for byte (`58fcdf5e…`; 538 accepted, 0 crashed).
- `gen_r2b_twins.py --checker` remakes `rust-core-r2b-checker-8.txt` byte for byte (`f17f5365…`; 1,558 of 1,558).
- The rows of both equal the `-7` records' rows (MEASURED).

## 4. Findings

**ZB1 (MAJOR): a harness fault before `attempt.json` is written leaves no record and is not counted.**
- **Where.** `gen_r6_reference.py:295–313`; the docstring at :28–30; SHEET.md:800–803.
- **What.** The recursion-limit probe at :295 is a child process started before `Attempt(ident, meta)` at :313. Any exception in :292–312 has the same effect, because `generation` raises before the attempt folder exists. This contradicts the claim in both the docstring and Amendment 7: "written before any child process starts".
- **Evidence (P11).** The probe was made to raise `OSError 1450`. The output was "generation 1: NOT ENDED: None"; the exception went to the thread's hook only; no attempt folder was made. Run again, the next attempt was `plant-p11-gen1-a1`, `retry_of=None`, and it COMPLETED.
- **Why it matters.** Under the very fault seen at 17:40 (WinError 1450), an interruption vanishes from the count that B1 and B3 stop on. Against him:
  - U2: *"Do not … allow it to disappear into an interruption count"*;
  - B4: *"Keep its error and any records already produced"*.
- **Did it bite?** No. `r6-reference-5` had one attempt per generation, both COMPLETED.
- **Proposal.**
  - Make the attempt folder and write `attempt.json` first, and run the probe after it, recording its result.
  - Wrap everything after `next_attempt` so that any exception writes `end.json` INTERRUPTED, cause HARNESS-FAULT.
  - Keep P11 as a plant.

**ZB2 (MINOR): a `SystemExit` while the reference's modules import is not a runner fault.**
- **Where.** `ref_run.py:166–191` and :245–254. `setup` catches `Exception`, and `main` catches `KeyboardInterrupt` and `Exception`, so a `SystemExit` escapes.
- **Evidence.** A stand-in raised `SystemExit` while decoder1, or `orlog.interp`, was being found. The runs ended with exit 0 (or exit 1 with the message), with no runner line on stdout or stderr. In all three modes `classify` returned NO-REFERENCE-RESULT.
- **Against.** D5(1), and the docstring's "not importable, whatever the exception". `ref_run_paths.py` has no case for it.
- **Who it affects.** The generator stops it (P14: INTERRUPTED, ENV-MISMATCH), because it requires the ENV line on exit 0 or 1. A harness that relies on `classify` alone, as the sheet prescribes, would class it.
- **Proposal.**
  - Catch `BaseException` in the block before the reference, after the KeyboardInterrupt case, and make it a fault.
  - Add a stand-in row for it to `ref_run_paths.py`.
  - Optionally, have `classify` treat an exit 0 or 1 with no ENV line as a runner fault or an anomaly.

**ZB3 (MINOR): the runner's check does not hold the ENV line's completeness, the bytecode check's folders, or the implementation and version.**
- **Where.** `ref_run_paths.py:136–152`, :260–261 and :297–301; against SHEET.md:818–821 and :827–831 ("both conditions lines").
- **Evidence.** Three of my variants pass the check 43 of 43:
  - X1: the ENV line lists `orlog.interp` alone;
  - X2: the `__pycache__` check covers `research/rust-core` alone;
  - X4: the ENV line omits the implementation and version.

  X3 (the platform left out) is caught only incidentally, by the platform stand-ins.
- **The runner itself is right today.** It reads every module loaded (:198) and checks three folders (:77). MEASURED: the record's ENV line lists the five modules loaded in law mode.
- **Proposal.**
  - Have the check compute the module set a fresh import loads, and require equality.
  - Plant one `__pycache__` copy for each folder of `BYTECODE`, by name.
  - Compare the implementation, version and platform with the check's own values.

**ZB4 (MINOR): law mode's ENV line lists five modules, not eight.**
- **Where.** SHEET.md:819 ("in law mode, the eight decoder1 brings in") and :924 ("the runner now hashes eight modules in each run").
- **Evidence.** Law mode lists five: `orlog`, `interp`, `numeric_ref`, `seal`, `syntax` (the record's header, line 6, and my run of the runner). Text mode lists eight, adding `canon`, `front` and `sema`.
- **Proposal.** Correct both places to "five in law mode, eight in text mode". His D5 says "the eight `orlog` modules"; the runner's "every module loaded" meets it.

**ZB5 (MINOR): the variant script makes four of REREAD-6's five changes, not five.**
- **Where.** `ref_run_variants.py:7–9` and :22–69; SHEET.md:832–834 ("REREAD-6's five and REREAD-7's eleven").
- **Evidence.** It makes 15 changes, not 16. REREAD-6's "P keeping the text-seal line", in both modes, is missing; V10 is REREAD-7's law-mode-only form. Made here as v20, the check catches it, 40 of 43.
- **Proposal.** Add it, so the record reads 15 of 16; or correct the wording.

**ZB6 (MINOR): the F1 figure "process-start failures" counts only the first stop.**
- **Where.** `gen_r6_reference.py:364–368` and :398–399.
- **Evidence (P13).** With two workers and every `Popen` failing, `runs.jsonl` has two `start_failure` lines and `end.json` says `process_start_failures 1`.
- **Proposal.** Count the `start_failure` lines in `runs.jsonl`, as CPU time is already summed from it.

**ZB7 (MINOR): one of the 11 write-back fixtures is in order and has no repeated entry.**
- **Where.** `r2-writeback-fixtures.txt:5`, `mutant/s1/0026 | given reversed: (given 2 1) -> (given 1 2)`; against SHEET.md:776–777 and `gen_r2_fixtures.py:8`, which call every fixture out of order or repeating an entry.
- **Evidence (MEASURED).** Ten of the 11 fit that description; this one ends in ascending order with no repeat. A writer that sorts, or removes repeats, writes it back exactly, so it tests neither. R2 loses no power by it: two of the 298 texts hold `(given 2 1)`.
- **Proposal.** Say "10 of the 11". Dropping variants that end in canonical order would mean a new file and a new freeze, which is the owner's call.

**ZB8 (MINOR): the timing in Amendment 7's account of `r6-reference-4` is not supported.**
- **Where.** SHEET.md:909–911: "Generation 2's two runs of 09729 ended about four seconds before generation 1's first run of it ended."
- **Evidence (REASONED).** I simulated the four-worker pool from the recorded wall times. The simulation reproduces `r6-reference-5`'s recorded run ends to within 9.5 s over 2,572 s. It puts both generations starting 09729 together at 3,726.6 s. Generation 2's runs end at 3,728.0 s and 3,729.0 s, and generation 1's first run at 3,765.1 s: about 36 s before it, not about 4 s. "Inside it" stands; the figure does not.
- **Proposal.** State the method behind the figure, or reword: both generations reached 09729 together, and generation 2's runs failed within about 1.4 s, inside generation 1's first run.

**ZB9 (MINOR): the attempt records would not travel with the record.**
- **Where.** `.gitignore:3` (`work/`); SHEET.md:800–808, which names the attempts by id only.
- **What.** His ruling's item 3 asks that each run's start and end, and the host's commit, be recorded "so overlap and resource contention can be established rather than inferred". After a push, nothing pinned holds the data behind Amendment 7's 0.489 s, 2.32 GiB, or 5 ms and 7 ms. Neither the record's header nor the sheet names the attempt files by sha256.
- **Evidence.** `git check-ignore` matches `work/` for `runs.jsonl`.
- **Proposal.** Name each `r6-reference-5` attempt file by sha256 in the sheet: for example `end.json` is `6a69fe97…` (generation 1) and `ef5aafa8…` (generation 2). Ask him whether attempt records are to be kept in the tracked tree; each `runs.jsonl` is about 38 MB, under GitHub's 100 MB limit.

**ZB10 (MINOR): `workers may rise` still ignores memory.**
- **Where.** `gen_r6_reference.py:401`.
- **What.** The flag reads True for both generations of `r6-reference-5`, with 2.32 GiB of commit left at the peak. SHEET.md:926–928 and :970–971 disclose this, and it remains unfixed. His F1: *"The measured process and memory limits govern."*
- **Proposal.** Add the commit headroom at the peak to the rule, or rename the field to say it applies F1's two conditions alone.

**ZB11 (MINOR, for reader 3): an interrupt reaching a reference run is recorded as a runner fault.**
- **Where.** `ref_run.py:24–29` and :251–258, and `ref_run_paths.py:244`, against REREAD-7-DISPOSITION.md:293 (B3's recommended text, adopted with A–F).
- **What.** The adopted text says reference runs "never become a runner fault or a reference crash". The runner turns a KeyboardInterrupt into `RUNNER-FAULT interrupted`, so the generator records its cause as RUNNER-FAULT. The disposition is INTERRUPTED either way and the stop rule is the same, so no outcome changes; only the cause's label differs. The sheet's B3 (SHEET.md:792–794) does not say "never a runner fault".
- **Proposal.** Either give the runner its own interruption line, which `classify` raises as Interrupted, or record that B3 is read as the sheet states it.

**ZB12 (MINOR): the two generations of `r6-reference-4` are kept unevenly.**
- **Where.** `research/rust-core/r6-reference-4.txt` (generation 1) sits in the records folder, while generation 2's file is in `work/`. SHEET.md:951 compares `r6-reference-5` with "`r6-reference-4.txt`'s" rows only, which belong to the generation whose 09729 row agrees.
- **What.** The sentence is true, and SHEET.md:994 disclaims any record. But the asymmetry leans toward a selection his ruling 1 forbids: *"Neither generation is selected."*
- **Proposal.** Keep both files side by side. Write "`r6-reference-4`'s generation 1" at :951, with generation 2's one differing row beside it.

## 5. Files I created

All are under `⟦HOME83⟧\AppData\Local\Temp\reread8-2\`, which Python resolves to `⟦HOME⟧\AppData\Local\Temp\reread8-2\`. Nothing was written in the repository.

**The sample and its re-runs**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\sample-rule.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\sample.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\frozen-rule.sha256`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\sample.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\rerun.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passA\result.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passA\runs.jsonl`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passB\result.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passB\runs.jsonl`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passA.log` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\passB.log`

**The generator plants**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\gen_copy.py` (byte-identical to the repository's generator)
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plants.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plants.log`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plant13.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plant13.log`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plant14.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\plant14.log`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\wrap\ref_run.py`
- the plants' attempt trees, under `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\out\`, `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\out13\` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\genplant\out14\`

**The runner stand-ins**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\runnerplant\standin.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\runnerplant\drive.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\runnerplant\drive.log`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\runnerplant\empty.law` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\runnerplant\say.orl`

**The runner check and its variants**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\paths-1.out`, `⟦HOME83⟧\AppData\Local\Temp\reread8-2\paths-2.out` (with `.lf` and `.err` beside each)
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\make.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\make20.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\names.txt`, `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\results.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\v20.txt`
- the variant folders `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\v00\` to `⟦HOME83⟧\AppData\Local\Temp\reread8-2\variants\v20\`

**R2 fixtures and the checker records**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r2-fixtures-1.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r2-fixtures-2.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r2check.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r2lists.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r6-checker-8.again.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\r2b-checker-8.again.txt`

**The Q6 analyses**
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\q6.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\q6.log`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\sim4.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-2\host.py` and `⟦HOME83⟧\AppData\Local\Temp\reread8-2\host.log`

## 6. Appendix: commands and outputs (abridged, faithful)

**A1. Pins.**
`sha256sum` of the 24 pinned files: every value equals the brief's.
`sha256sum research/law-sufficiency/decoder1.py` → `3584f565f6929879c3d942a45b3fa8d5c09cc2382b67772559109e38930ab877`.

**A2. The sample, frozen before any outcome was looked at.**
`sha256sum sample-rule.txt sample.py` → `9e7f26fb0181ad59b9b96fb98c4d742807f66aa3e86777827f33046c6568b07a` and `0b699338f2fa770719d5326abd7c97576c0e6e3fc65bf00b85b32b648e0cde5c`.

The rule:
- **Strata:** each crash type (up to 5); RESULT by operator and kind (3 each); REFERENCE-REFUSED by operator (4 each); UNSTABLE (all); the 10 slowest by wall and the 10 slowest by CPU from the `r6-reference-5` attempt records.
- **Draw:** `random.Random(20261108)`.
- **Excluded:** 09729.

Then `python -B sample.py sample.txt` → 93 mutants; `sample.txt` sha256 `5f22eaf8708066956cb8d8748fab61f2b573142f305e860a2ca9a2212a9d44ce`.

The 93, by stratum:

| stratum | mutants |
|---|---|
| AttributeError | 09829 |
| IndexError | 00973, 01229, 01366, 01998 |
| KeyError | 01314, 01711, 01977, 06189, 09915 |
| RecursionError | 05023, 06901, 07007, 07285, 09798 |
| TypeError | 00062, 00521, 00603, 00778, 09441 |
| UnicodeDecodeError | 00363, 01017, 01185, 01632, 01869 |
| ValueError | 00885, 01242, 01962, 02214, 02270 |
| struct.error | 00115, 01963, 08862 |
| flip COMPLETED | 00028, 01518, 02146 |
| flip REFUSED | 00457, 00950, 01153 |
| id COMPLETED | 08772, 09298, 09607 |
| id REFUSED | 07911, 09140, 09785 |
| id STOPPED | 08636, 09737, 09929 |
| swap COMPLETED | 05914, 06920, 07378 |
| swap REFUSED | 05085, 06531, 06949 |
| swap STOPPED | 05418, 06960, 07345 |
| refused, flip | 00254, 01841, 01991, 02329 |
| refused, id | 07779, 08188, 08624, 09860 |
| refused, swap | 05035, 05732, 06232, 06899 |
| refused, truncate | 02709, 03625, 03967, 04534 |
| slowest by wall | 09739, 09742, 09743, 09744, 09757, 09758, 09759, 09767, 09768, 09769 (all neighbours of 09729, slowed by contention there) |
| slowest by CPU | 05364, 05498, 06081, 06403, 06412, 06577, 06973, 07315, 07492, 09270 |

No RESULT exists for truncate, and no STOPPED for flip.

**A3. The re-runs.**
`python -B rerun.py sample.txt passA`, then the same into `passB`. Each mutant is run twice, one process at a time, through `ref_run.py` with the generator's arguments, environment, process group, empty folder and 60 s limit.
- Pass A: `RERUN: 93 mutants, 93 rows equal to the record, 0 differ` (`result.txt` `077800eb…`).
- Pass B: the same (`e74fd779…`); its verdicts and classes equal pass A's.
- Every run's ENV line equals the record header's.
- Walls 0.27–5.24 s; the largest commit peak of a run was 371 MiB (06403); 95.9 s of runs in all.

**A4. The generator plants** (`python -B genplant/plants.py`, one worker):

| plant | result |
|---|---|
| P1 | both COMPLETED; record == gen1 == gen2 |
| P2a | `a1` INTERRUPTED, HARNESS-FAULT; 3 run lines, 1 of them a `start_failure`; `psf=1`; no files; generation 2 NOT STARTED |
| P2b | `a2 retry_of=a1` COMPLETED, 6 runs; generation 2 COMPLETED; record written |
| P3a, P3b | INTERRUPTED twice |
| P3c | "REFUSED: plant-p3-gen1 was interrupted on its repeat; it stops, and goes to the owner (his B1, B3)" |
| P4 | INTERRUPTED, "RUNNER-FAULT: … BUDGET is not none or a canonical decimal" |
| P5 | STOPPED-ANOMALY, then "REFUSED: an attempt … stopped on an anomaly" |
| P6 | INTERRUPTED, cause INTERRUPTED, then `a2` COMPLETED |
| P7 | INTERRUPTED, OPERATOR-INTERRUPT |
| P8 | `a2 retry_of=a1` (the folder with no `end.json`) |
| P9 | both COMPLETED; "NOT EQUAL (1 lines differ: 00003) … no record is written"; files gen1 and gen2 only |
| P10b | "generation 1's file is not the one plant-p10-gen1-a1 completed with; no record is written" |
| P11a | thread exception "OSError: [Errno 1450] planted…"; "generation 1: NOT ENDED"; no attempt folder |
| P11b | `plant-p11-gen1-a1 retry_of=None` COMPLETED |
| P12 | "generation 2 starts only once generation 1 has completed" |
| P13 | 2 `start_failure` lines; `end.json process_start_failures 1` |
| P14 | "INTERRUPTED ENV-MISMATCH run 1 of mutant 00001: its ENV line is not the attempt's" |

**A5. The runner stand-ins** (`python -B runnerplant/drive.py`):

| mode | exit | stdout | stderr's last line | `classify` |
|---|---|---|---|---|
| exit0-decoder1 | 0 | `''` | `''` | NO-REFERENCE-RESULT |
| exitmsg-decoder1 | 1 | `''` | `'a decoder1 whose import exits'` | NO-REFERENCE-RESULT |
| exit0-orlog | 0 | `''` | `''` | NO-REFERENCE-RESULT |

**A6. The runner's check.**
`python -B research/rust-core/ref_run_paths.py`, twice: exit 0 both times, stdout identical, and equal to the body of `evidence/rust-core-ref-run-paths-8.txt` (`cmp`). Last line: `REF-RUN PATHS HELD: 43 of 43 as stated`.

**A7. The variants, run one at a time** (`python -B vNN/paths.py`):

| variant | result |
|---|---|
| v00, control | HELD 43 of 43 |
| REREAD-6: the ENV line removed | FAILED, 33 of 43 |
| REREAD-6: the recursion limit raised | 30 |
| REREAD-6: `format_check` imported | 25 |
| REREAD-6: BUDGET read from `os.environ` | 42 |
| V1 | 42 |
| V2 | 40 |
| V3 | 41 |
| V4–V7 | 42 each |
| V8 | 30 |
| V9 | 42 |
| V10 | 41 |
| V11 | HELD 43 of 43 (not caught) |
| X1, the ENV line lists `orlog.interp` alone | HELD 43 of 43 |
| X2, the `__pycache__` check covers `research/rust-core` alone | HELD 43 of 43 |
| X3, the ENV line without the platform | FAILED, 41 of 43 (the platform stand-ins only) |
| X4, the ENV line without the implementation and version | HELD 43 of 43 |
| v20, P keeps the text-seal line in both modes | FAILED, 40 of 43 |

The repository's 15 rows equal `evidence/rust-core-ref-run-variants-8.txt`'s counts.

**A8. The ENV line's modules.**
- `ref_run.py text none say.orl` → `orlog orlog.canon orlog.front orlog.interp orlog.numeric_ref orlog.seal orlog.sema orlog.syntax`.
- `ref_run.py law none 0…0 empty.law` → `orlog orlog.interp orlog.numeric_ref orlog.seal orlog.syntax`.

**A9. The write-back fixtures.**
- `GIT_OPTIONAL_LOCKS=0 python -B research/rust-core/gen_r2_fixtures.py OUT`, twice: both "11 fixtures, each accepted and written back exactly by the checker; sha256 2e13265aae132ba6e62411999e55c99d2c85caacc05e1a1603466c26d2feb5a0"; `cmp` with the frozen file shows them equal.
- `r2check.py`: "11 of 11 fixtures: sha256 as stated, accepted and written back exactly". Fixture 1, `mutant/s1/0026 given reversed`: "IN ORDER, NO REPEAT".
- `r2lists.py`: `over` lists in 3 texts, 2 distinct laws, all `1 2 3 4`; `given` lists in 3 texts, 2 distinct laws, `0026` and `n32-premise-later-and-self` with `2 1`.

**A10. The checker records.**
- `gen_r6_mutants.py --checker r6-mutants.txt OUT` → "accepted 538; crashed 0; sha256 58fcdf5e…"; `cmp` equal.
- `gen_r2b_twins.py --checker r2b-twins.txt OUT` → "agrees on 1558 of 1558 … sha256 f17f5365…"; `cmp` equal.
- The rows of `-7` and `-8` are equal for both.

**A11. `q6.py`.**
- `-5 == gen1 == gen2 byte for byte: True`.
- `rows -3 vs -5: 0 differ`; `rows -4gen1 vs -4gen2: 1 differ: 09729 … TypeError || … MemoryError`.
- `-5's sha equals each -5 attempt's output_sha256: True`.
- In every attempt: 20,000 run lines; 0 start failures, 0 timeouts, 0 runs that left files; the rows rebuilt from `runs.jsonl` equal the generation's file; 1 distinct ENV line, which is the `-5` header's.
- `-5: gen2's first start - gen1's last end = 0.489 s; any gen2 run starting before gen1's last end: False`.
- 09729 in generation 1: run 1 wall 37.0 s, run 2 34.6 s, 0.005 s apart. In generation 2: 36.4 s and 35.2 s, 0.007 s apart.
- The peaks, 45.30 and 45.29 GiB, fall inside 09729's first run; 2.32 and 2.33 GiB left; the limit 47.62 GiB.
- 09758 in generation 2: run 2, wall 22.5 s, CPU 0.453 s.

**A12. The pool simulation** (`sim4.py`).
- `r6-reference-4` generation 1: 09729's first run from 3,726.6 s to 3,765.1 s.
- `r6-reference-4` generation 2: 09729's first run from 3,726.6 s to 3,728.0 s, its second ending at 3,729.0 s.
- Check against `r6-reference-5` generation 1's recorded ends: 09729 simulated 2,468.7 s against 2,477.6 s recorded; 09999 simulated 2,562.9 s against 2,572.4 s.

**A13. Host readings outside 09729's window** (`host.py`):
- Generation 1: commit 20.99–21.59 GiB, median 21.26; physical memory in use, median 8.47 GiB.
- Generation 2: commit 20.97–21.47 GiB, median 21.18; physical memory in use, median 7.22 GiB.

**A14. Tally of `r6-reference-5`'s rows.**
- Classes: RESULT 2,374; REFERENCE-REFUSED 6,994; NO-REFERENCE-RESULT 632, all exit 1.
- Crash types: UnicodeDecodeError 326, ValueError 119, KeyError 117, RecursionError 43, TypeError 19, IndexError 4, struct.error 3, AttributeError 1.

**A15. Is it named anywhere as a record?** Grep for `r6-reference-4|1b10b1a0|18134261|636a2873` over the repository (excluding `research/law-sufficiency`; the tool skips git-ignored `work/`):
- SHEET.md:897, :902–904, :950–951, :988–989, :994;
- RULINGS.md:741, :765, :795;
- REREAD-7-DISPOSITION.md:385;
- LAW-FORMAT-0-DRAFT-8.md:1024.

None names `r6-reference-4` as a record.

HASH CLOSURE: PASSED: `r6-reference-5.txt` has sha256 636a287364982201638149bd318169cd4d2a8e49bd3ec1bb23222de508f88be5, the value at both places Amendment 7 states it (SHEET.md:950 and :989). It is byte for byte both generations' files, each at its attempt record's `output_sha256`. Its 10,000 rows equal `r6-reference-3.txt`'s. Its header names the runner (822c826e…) and the generator (cc63252d…) by their current sha256.
