# ØRLǪG (Orlog): status, 2026-10-25, after the foundations review (SPEC v0.4)

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
5. **research/ragnarok/VERDICT.md**: the counterworld search, argued by a proponent and an adversary over two rounds,
   with a prior-art survey. Proposed, not admitted.
6. **court/RECORD.md** and court/VERDICT.txt (the first court; the second round's record is still open, below).
7. **ADMISSION.md**: the proposed admission record. Not admitted.

## Measured here (2026-10-25, in the repository)
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

## Changed this round
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

## Still open
- **The owner's rulings**: DOCTRINE §9 (fork 2 is decided); the roadmap's first rung
  (`research/roadmap-debate/VERDICT.md`); whether Ragnarök's narrow instrument is admitted at all
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
