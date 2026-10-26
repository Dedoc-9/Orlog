# ØRLǪG (Orlog): status, 2026-10-26, after COMPAT-0, the court's R8 and the reporting pass (SPEC v0.4)

Start here when resuming. The project lives in its own repository, [github.com/Dedoc-9/Orlog](https://github.com/Dedoc-9/Orlog)
(local folder `Desktop\Orlog`), under the GNU AGPL v3 (AGPL-3.0-only, as Verðandi). It moved there from a session
scratch folder on 2026-10-25. Nothing is admitted or registered anywhere, and the Verðandi checkout is untouched. The
owner makes every commit and push.

## Read in this order
1. **AGENTS.md**: the brief for any agent working here (what to read, never touch, run, and how to claim).
2. **DOCTRINE.md, edition 2, revised**: each stage's theorem as narrowed by the court; T11 (what four-way agreement
   measures, layer by layer); T12 (where the ground ends); the non-claims (§8); the owner's forks (§9); §11 (the
   hardening that pays twice).
3. **SPEC.md**: the body, then §11 (v0.1), §12 (v0.2, red team), §13 (v0.3, the twin's second round) and §14 (v0.4,
   its third). §13 holds the phase table.
4. **research/roadmap-debate/VERDICT.md**: the next steps ranked by foundational value, after a debate between an
   architect, a use-case skeptic and a documentation prosecutor, and the disposition of the prosecutor's 57 findings.
5. **research/run-1/RULINGS.md**: the rulings the open run needs (R1–R12 and ten defaults), each with its options,
   what each entails, the theorem under it, a falsifier and a recommendation. R3 is ruled (a, exact or refused),
   R4 (a, at tick granularity) and R5 (with four amendments, the per-tick line in 1a, the per-event chain kept), all
   2026-10-26; the rest await the owner.
6. **research/doppler/VERDICT.md**: whether incompleteness can be ruled out "as ruthlessly as sha256". A sound,
   refusal-sensitive dependence analysis certifies and a doppler search only prosecutes; nothing is built before
   RUN-1. It also records a defect in the court as built (DP-5) and three holes in R6's amendment.
7. **research/speed/VERDICT.md**: the owner's speed reconciler, language swap, graphics and headroom requests, argued
   over two rounds with a survey and the judge's reruns. No language swap: the per-event SHA-256 is 91–98% of a
   compiled tick. A play build without it, writing a per-tick line, runs at about 4% and names 12 of 13 planted
   defects at their tick. Graphics stay in a view that must neither write back nor disclose. RUN-1 proposals for the
   owner, and a finding about Verðandi's renderer.
8. **research/ragnarok/VERDICT.md**: the counterworld search, argued by a proponent and an adversary over two rounds,
   with a prior-art survey. Proposed, not admitted.
9. **court/RECORD.md** and court/VERDICT.txt (the first court; the second round's record is still open, below).
10. **ADMISSION.md**: the proposed admission record. Not admitted.

## Measured here, COMPAT-0 (2026-10-26)
- `python -B tests/selftest.py`: **ORLOG SELFTEST 163/163** (reference, python, c99, rust), two consecutive runs
  byte-identical, sha256 37a9eadd2cb885d5… of the file as captured (CR LF); with `--backends python`, **153/153**. The
  two new rows are COMPAT-0's.
- **The gate**, `python -B tests/compat.py check --jobs 8`: COMPAT-0 HELD. 3,361 texts frozen at b4eaf11 with their
  results all reproduce. They are 13 corpus versions, 291 probes, 57 fixtures and 3,000 mutants; the results are 300
  completed runs and 3,061 refusals, with no stop and no crash. `selftest`: COMPAT SELFTEST 6/6, four plants caught
  (`evidence/compat-check.txt`).
- **The audit trail**, `tests/compat.py history 83eb044 7186e50 fc19339 b4eaf11`: fc19339 and b4eaf11 reproduce all
  3,361. 83eb044 and 7186e50 differ on exactly two texts, both SPEC §14 item 8's code change in fc19339. Every version
  of every corpus program has the same law seal, text seal and receipt core under all four
  (`evidence/compat-history.txt`). The sealing path's code is unchanged through every revision but that one change to
  sema (`evidence/seal-audit.txt`).
- **What it does not protect** (timings, memory over long runs, the arbiter, the backends, and more) is in
  `tests/compat/README.md`.

## Measured here, the foundations review (2026-10-25, commit b4eaf11)
- `python -B tests/selftest.py`: **ORLOG SELFTEST 161/161** (reference, python, c99, rust). Two consecutive runs, the
  second on the first's build cache, byte-identical: `evidence/selftest-run.txt` and `selftest-run2.txt`, sha256
  e181601f0ac530d0… of the file as captured (with the CR LF line ends Python writes to a redirected stdout on
  Windows). With `--backends python`, **151/151** (`evidence/selftest-python-only.txt`).
- **What agreement measures** (DOCTRINE T11), as self-test rows: a defect planted in the shared lowering moves the
  three backends together against the reference (REFERENCE-DISSENT; 41 operations more on collatz, one per 3n+1
  step); a defect planted in the shared front end passes all four executions and only the twin sees it (a monitored
  negative, kept on purpose).
- **The vectors checked by something other than their generator**: `python -B tests/vectors_independent.py`. 20,006
  of the 20,015 lines are derived again by `tests/numeric_oracle.py`, which imports only `fractions`; 0 differ, and
  numeric_ref as it runs differs from the derivation on none. 113 hand-worked cases (105 of them in the vectors), the
  smallest subnormal's 1074-digit print and two published SHA-256 digests agree. Five plants caught, three of them
  mistakes that numeric_ref and vectors regenerated from it would share. Two runs byte-identical
  (`evidence/vectors-independent.txt`). The first run caught one plant by the derivation alone: no hand case routed a
  non-canonical NaN through the canonicalization. Three cases were added.
- **Runtimes**: C 20,015/20,015 at -O2 and -O0, Rust 20,015/20,015 with and without -O, each pair byte-identical, no
  build warnings (`evidence/rt_c-vectors-*.txt`, `evidence/rt_rs-vectors-*.txt`).
- **The arbiter**: one run folder per arbitration; 48 arbitrations of two programs at once in one work folder, three
  times, all agreeing, none left (`evidence/race-after.txt`); a failed build counted neither agreeing nor dissenting;
  the reference stopped by the host's budget at the same operation twice (STOPPED-BY-HOST, no receipt); a torn ledger
  refused at its line (LEDGER-BROKEN).
- **Corpus seals**: all 11 law seals equal under the front ends of 83eb044 and fc19339 (`evidence/corpus-seals.txt`).
  The chaos and leapfrog notes changed (prosecutor F1, F54); notes are not law.
- **Twin**: probes 161 + 2 settled (round 2) and 125 + 3 settled (round 3) (`evidence/probes-run.txt`,
  `evidence/probes3-run.txt`; the round-3 first run, 124/128, in `evidence/probes3-first-run.txt`).
- **Differential runs**: seed 1, 20,221 programs, 0 disagreements; seed 2, 20,353 programs, 47 of 48 the readings
  settled against the twin and 1 timeout identical without a limit (`evidence/difftwin-*`). At AGENTS' size,
  `--n 3000 --seed 1` (354 seeds, E22's fixture now among them): 10 disagreements in 4 signatures, all three settled
  readings (`evidence/difftwin-n3000-seed1.txt`).
- **Door**: `doorfuzz.py 60000 5`, 0 counterexamples (`evidence/doorfuzz-60000-5.txt`); E18 now has a row and a plant.
- **E21**: the list measurement, now tracked as `tests/e21_list_leak.py`, gives 46 and 46 MiB again
  (`evidence/e21-lists-rerun.txt`).

## Changed in COMPAT-0 (2026-10-26)
- `tests/compat.py` and `tests/compat/` (v0's frozen texts, baseline and an empty `settled.json`, with a README of what
  the gate does and does not protect); two self-test rows; `tests/corpus_seals.py` also compares the sealing path's code
  revision to revision; `.gitattributes` keeps the frozen files byte for byte.

## Changed in the foundations review (b4eaf11)
- **Arbiter** (`arbiter.py`): a run folder per arbitration, removed after it; builds published atomically from the
  source in memory; a failed build or missing compiler is `build_failed`, outside agreement and dissent; a host budget
  of counted operations on the reference (`interp.py`, HostStop) and a wall clock on the backends; `orl.py court` takes
  `--backends`.
- **Court** (`court.py`): INCOMPLETE integrity when a backend did not build or was stopped; LEDGER-BROKEN, fail-closed.
- **Tests**: `tests/vectors_independent.py` and `tests/numeric_oracle.py`; rows for the lowering and front-end plants,
  the vectors, arbiter isolation and its plant, the race, BUILD-FAILED, the host budget, the torn ledger and its plant,
  E18 and its plant, E22, NESTING-DEPTH at its limit; F55–F57's texts; `tests/corpus_seals.py`,
  `tests/race_arbiter.py`, `tests/e21_list_leak.py`; E18's and E22's reproducers copied into `tests/fixtures/redteam/`.
- **Documents**: the prosecutor's findings applied as `research/roadmap-debate/VERDICT.md` lists; README and DOCTRINE
  gain the independence table and the grounding section; README gains the author and contact line.
- **Debates**: `research/roadmap-debate/` (architect, skeptic, prosecutor, verdict) and `research/ragnarok/` (the
  proposal, the proponent's and adversary's two rounds, the survey, the verdict), each report saved verbatim.

## Repaired 2026-10-26, after the doppler debate
- `python -B tests/selftest.py`: **ORLOG SELFTEST 169/169**, two consecutive runs byte-identical, sha256
  367ef35a14de8ffd… as captured (CR LF); with `--backends python`, **159/159**. The six new rows are R8's.
- **The court's R8** (DP-5). Before it, a claim whose evaluation refused partway through its own condition was not
  counted, and read GROUNDED with its seal ratified over a run REFUSED at it. The court now names that evaluation and
  does not count the claim as held. An inline claim is withheld conservatively.
  - **No receipt changed:** COMPAT-0 HELD.
  - **Blast radius on the 3,361 frozen texts:** nothing. None refuses inside a claim, which is a coverage gap.
    Counted (`research/compat-status.md`): of the 44 texts that run with claims, 38 complete and 6 refuse
    CLAIM-REFUTED, so no claim's evaluation is ever cut off. R8's class has no member there: no exercise in the corpus.
  - **Its four fixtures:** 5 standings withheld and none granted; the plant that reverts R8 is caught
    (`evidence/court-r8.txt`).
- **R6 in the RUN-1 sheet.** The trigger is now any input log (DP-4). The exemption, PREFIX, is decided by evaluation
  (N-1) and covers the whole claim line (N-2). R12 gains the court's one-sidedness row.

## Repaired 2026-10-26, after the reporting pass
- **The pass** (`research/reporting-pass/FINDINGS.md`): an adversarial review of the code that reports. 18 findings,
  none a live false GROUNDED, WELL-FOUNDED or AGREED. Before anything was changed, its 14 quick reproducers gave
  byte-identical output here, and its mutation harness gave the same verdicts: 10 of its 14 planted regressions left
  the self-test at 169/169.
- **Integrated** at the owner's word ("review and integrate the adversarial reporting passes lessons/fixes"); each
  finding's disposition is in `research/reporting-pass/DISPOSITION.md`. Every repair has a row, and every row a plant
  that is the pass's own regression, made in memory (`tests/plants.py`). The largest:
  - R8 is panel's parameter, read by `orl.py` and every row at one value;
  - the reading prints the run's status and integrity first, naming the backends; `orl.py court` exits 2 over a
    dissent, a failed build or a host stop;
  - the compiler's version is in the build key, and a record is checked before a cached program runs;
  - COMPAT-0 refuses an uncovered frozen text or a settlement without its reason (COMPAT SELFTEST 8/8, HELD:
    `evidence/compat-after-reporting-pass.txt`);
  - the one-sidedness measurement sees CIRCULAR and plants a court that grants: 0 gained, 9 withheld
    (`evidence/court-r8.txt`).
- `python -B tests/selftest.py`: **ORLOG SELFTEST 210/210**, two consecutive runs byte-identical, sha256
  670235733a34a92c… as captured (CR LF); with `--backends python`, **194/194**. No receipt changed.
- **Found while integrating:** the first version of the Python cache check kept a wrong cached source on Windows (a
  rename onto a file still open for reading). Its own row caught it, and it is repaired.

## Still open
- **The reporting pass's two questions for the owner** (`research/reporting-pass/DISPOSITION.md`): what a law's own
  refusal exits with, and whether a claim that held stays held in a run refused elsewhere.
- **The speed verdict's proposals** (`research/speed/VERDICT.md`), for the RUN-1 sheet:
  - a per-tick line;
  - `ops` in the `'T'` event;
  - port ranges at the door;
  - R9 b's three conditions;
  - snapshots holding every accumulator;
  - R13 (what a live outcome is) and R14 (a play build without the event chain).

  None is on the sheet until the owner rules.
- **Verðandi's floor-mirror leak** (the speed verdict). Its native renderer shows a target hidden behind a wall
  (MEASURED twice, one browser engine and GPU). The rule about blocking holds; a view's disclosure is unchecked.
  Recording it in Verðandi is the owner's call.
- **The owner's rulings**: RUN-1's sheet (`research/run-1/RULINGS.md`, R1–R12); DOCTRINE §9 (fork 2 is decided);
  HOST-0, which needs a second machine; whether Ragnarök's narrow instrument is admitted at all
  (`research/ragnarok/VERDICT.md`); and prosecutor F42, below.
- **Privacy (prosecutor F42)**: 16 tracked files under `court/` still embed the home folder's path (the prosecution's
  header and 15 captured observations of the red team). They are records "kept as captured"; redacting them rewrites a
  record, so it waits for the owner's word. `research/scripts-r1b/x.sh` was pointed at the repository (F36).
- **The twin's readings**: it holds its own on the three probes settled against it (SPEC §14 items 6, 7, 9). Whether
  its author adopts §14 is a fourth round's question.
- **The twin's inputs**: `tests/make_twin_inputs.py` now writes 24, since examples/fall.orl joined the corpus after
  round 1, whose record covers 23. The tracked inputs keep the 23, with chaos's and leapfrog's notes updated.
- **Court record for the second round**: add E7–E26, E21's repair, the twin's rounds 2 and 3, the differential runs
  and this review's findings to court/build_record.py; rerun `python -B court/build_record.py && python -B
  court/judge.py`; update RECORD.md.
