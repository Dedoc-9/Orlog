# ØRLǪG (Orlog): status, 2026-10-25, after the second round (SPEC v0.3)

Start here when resuming. The project lives in its own repository, [github.com/Dedoc-9/Orlog](https://github.com/Dedoc-9/Orlog)
(local folder `Desktop\Orlog`), under the GNU AGPL v3. It moved there from a session scratch folder on 2026-10-25.
Nothing is admitted or registered anywhere, and the Verðandi checkout is untouched. The owner makes every commit and
push.

## Read in this order
1. **AGENTS.md**: the brief for any agent working here (what to read, never touch, run, and how to claim).
2. **DOCTRINE.md, edition 2** (revised for the second round): each stage's theorem as narrowed by the court; the
   non-claims (§8, with E21 and the one undecided fault order); the owner's forks (§9).
3. **SPEC.md**: the body, then §11 (v0.1), §12 (v0.2, red team), §13 (v0.3, the twin's second round). §13 holds the
   complete phase table: every compile code in one phase, and the order within each phase.
4. **court/RECORD.md** and court/VERDICT.txt (first court; not yet updated for the second round: see below).
5. **ADMISSION.md**: the proposed admission record. Not admitted.

## Measured here (2026-10-25, in the repository)
- `python -B tests/selftest.py`: **ORLOG SELFTEST 140/140** (reference, python, c99, rust). Two consecutive runs,
  the second on the first's build cache, byte-identical: `evidence/selftest-run.txt` and `selftest-run2.txt`, sha256
  b808c1ea69c21c69….
- `python -B tests/compare_probes.py`: 161/163 of the twin's hand-worked probes met as worked, 2 met as §13 settled
  them against the twin (`twin/probes/settled.json`), 0 different (`evidence/probes-run.txt`).
- `python -B tests/diff_twin.py --n 20000 --seed 1 --minimize` (run in scratch, before the §13 order repairs):
  20,221 texts; 18,749 refused alike, 1,185 ran byte-identically, 287 disagreed: 282 from the twin predating §12–§13,
  1 harness artifact (fixed), 4 within-statement orders (settled in §13: 3 repaired in the reference, 1 the twin's).
  Rerun it here; its report goes to `work/difftwin/` (ignored).
- `court/redteam-eng/doorfuzz.py 60000 5`: 0 counterexamples after the door change.
- All 11 corpus law seals unchanged after every change this round.

## Changed this round
- Reference: `Sealed: ` exact prefix; LINE-FORM before SEAL-PLACE; SEAL-FORM before SEAL-PLACE; Sealed line is
  content; missing period is LINE-FORM (STATEMENT-PERIOD gone); calls by any non-reserved first word
  (UNKNOWN-PROCEDURE), PROCEDURE-NAME and UNKNOWN-PROCEDURE after the parse; empty names SYNTAX; item 47 both ways
  plus rule/procedure; within-statement written order, post-order; no false QUOTE-BOUNDARY on a refused line.
- Tests: rows for E7, E8, E9, E11, E16b/d/e/f, E19, E20, E24/E25, E26, the bounds at their limits, the CONSTANT
  reading, the probes, the phase table against the source (plant), the within-statement order (plant); two stale
  rows fixed. The FMA row now generates chaos.orl's C itself: on a reused build cache it had picked the
  c99-explicit-fma plant's copy of chaos and counted that plant's FMA (found moving into the repository).
- Repository: LICENSE (AGPL-3.0, the owner's text), `.gitattributes` (LF; byte-exact files `-text`), `.gitignore`
  (generated output, the red team's fuzz output, clones of other repositories, downloaded papers), `evidence/`.
  Left out of the move: `build/`, `work/`, executables, `upstream/` (clones of Dentatus, Ursprung and
  executable-epistemics), `r1a-work/` and `research/dl*` (downloaded papers), the fuzz output.

## Still open
- **Twin round 3** (a clean-room agent updating twin/twin.py to §12–§13 and writing hand-worked probes in
  twin/probes3/) stopped at the session limit having written nothing. Start it again in this repository's `twin/`,
  under the clean-room rule in AGENTS.md §3; then rerun its probes, compare the reference with them, rerun
  tests/diff_twin.py, and treat its ambiguity findings as attacks on §13.
- Court record for the second round: add E7–E26, the twin's rounds 2 and 3 and the differential run to
  court/build_record.py, add the revised claims, rerun `python -B court/build_record.py && python -B court/judge.py`,
  update RECORD.md.
- DOCTRINE: add the stage "T10, one code per refused text" with its evidence; update §5's counts and defect table.
- The owner's rulings on DOCTRINE §9 (fork 2, where it lives, is settled: this repository).
