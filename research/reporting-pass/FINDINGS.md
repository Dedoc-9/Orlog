# The reporting pass: findings (2026-10-26)

An adversarial review of the parts of Ørlǫg that report: the code that turns runs into a reading a person trusts. The
question was every way a report can say more than its run establishes:
- a false GROUNDED, WELL-FOUNDED, AGREED or HELD;
- a dissent or a refusal hidden, or one invented;
- a count that absorbs what it should not;
- a row whose PASS is the hoped outcome, not the apparatus's.

Calibrated against three earlier instances of the class: E7 (a lenient receipt comparison), the arbiter's shared work
folder (false dissent, b4eaf11) and DP-5 (a claim whose evaluation refused read GROUNDED, repaired as R8).

**The tree reviewed** is f16dc26. When this pass began, the R8 repair was uncommitted on 3417949; it was committed as
6ea2f13 (then f16dc26) in the pass's first minutes. Every evidence file's header gives the sha256 of the seven reporting
files it read, and each equals the file at f16dc26, with no uncommitted change to any tracked file.

**The host** was Windows 11, CPython 3.14.5, clang 22.1.8 and rustc 1.96.1, with `PYTHONHASHSEED=0` and `PYTHONUTF8=1`
throughout. Nothing tracked was changed, and nothing was repaired.

This report is model output. One model family wrote the code under review, the reproducers and this report.
Agreement among them is consistency, not grounding (AGENTS.md).

## How to read it

- **Severity** is the kind of wrong reading, in the order asked for:
  1. grants a standing it should not;
  2. hides a dissent or a refusal;
  3. misreports a count;
  4. only miswords.
- **Live** means the reading is wrong today, on the tree as it stands. **Latent** means the code reads right today, but
  no self-test row can fail if it regresses. That is shown by planting the regression in a full copy of the tree and
  running the whole self-test there: it still reads 169/169. A latent finding takes the severity of what it would let
  through.
- **Grades** are as AGENTS §6 defines them. Every numbered finding below is MEASURED: a run named beside it shows the
  defect. Statements that something is absent from the code, and the wordings found by reading alone, are graded
  DECLARED where they are made.
- **Commands** run from the repository's root, with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` before each script.
  `research/reporting-pass/reproducers/run_all.py` runs the fourteen quick reproducers and writes each one's output to
  `research/reporting-pass/evidence/<name>.txt`, headed by its command and tree. Two consecutive runs were
  byte-identical on all fourteen. Add `--with-mutants` for `court_mutants.py`, which takes about 15 minutes.
- **The mutation harness.** `court_mutants.py` copies the working tree, tracked and unignored files as they stand, into
  `work/reporting-pass/mut/tree`, along with the self-test's compile cache. For each plant it replaces one or more
  exact lines of the copy and runs the copy's own `tests/selftest.py`. The copy's subprocesses (compat.py,
  court_monotone.py, orl.py) import the copy's `src/`, so a plant reaches them too.
  - It has two controls: no plant, which must read 169/169, and `held-ignores-unreached`, which the inline row must
    catch. Both held.
  - Each surviving plant is shown to be no equivalent mutant: a named reproducer runs the planted code and the code as
    built on one fixture, and the readings differ.
  - The table is in `evidence/court_mutants.txt`, and the self-test's own output under each plant is in
    `evidence/mutants/`. A first run, in two passes, gave the same verdict for every plant (the passes are kept in
    `work/`).

| # | finding | severity | live or latent |
|---|---|---|---|
| 1 | R8's shipped switch is never read by a row: set it to False and `orl.py court` reads DP-5's fixture WELL-FOUNDED (GROUNDED with its seal ratified), the self-test 169/169 | 1 | latent |
| 2 | R1 (no claim held unless every backend agreed) has no row | 1 | latent |
| 3 | A refuted claim's exclusion from "held" has no row | 1 | latent |
| 4 | E7's lenient comparison put back into the arbiter's verdict: 169/169, and the E7 plant still reads CAUGHT | 1 | latent |
| 5 | Two of the four agreement conditions (exit status 0, the output file) have no row | 1 | latent |
| 6 | The court's reading never names a refusal outside R8; `orl.py court` exits 0 over a refusal and over a failed build | 2 | live |
| 7 | A warm build cache answers for a compiler that cannot build; the witness names that compiler | 2 | live |
| 8 | 21 rows pass with a backend that did not build; both compilers refusing the 600-arm chain (E10's class) reads 169/169 | 2 | latent |
| 9 | The court's summary counts five different failures as `unsupported`; a refuted and an R8-withheld claim give one summary | 3 | live |
| 10 | A certificate's cost reading drops the evaluation R8 names: CHEAPER where the operations spent say NOT CHEAPER | 3 | live |
| 11 | COMPAT-0 checks only the frozen texts that have a baseline row: one row removed reads HELD; a settled entry needs no reason | 3 | live (an edit to a tracked file) |
| 12 | court_monotone counts no CIRCULAR change, and its plant is the measurement read backwards | 3 | live (the instrument) |
| 13 | `orl.py court` never prints the CONSTANT note | 4 | live |
| 14 | AGREED names no backend: one backend and three print the same reading | 4 | live |
| 15 | R8 reads a plain Otherwise clause's claim as "possible", naming a condition and an arm the clause does not have | 4 | live |
| 16 | The witness's receipt hashes cannot be compared, and a CR LF dissent's summary equals an agreeing run's | 4 | live |
| 17 | A ledger line that is a JSON object of the wrong shape ends `orl.py court` in a traceback | 4 | live |
| 18 | The isolation row and its plant pass with the shared-folder defect live; only the race row saw it | 4 | the row only: the self-test caught the plant through the race row |

**No live false GROUNDED, WELL-FOUNDED or AGREED was found on the paths examined, and no false HELD without an edit to
a tracked frozen file** (finding 11). Severity 1 holds only latent findings: rules that read right today and that no
row holds. The live findings are hidden refusals and failures (6, 7), counts (9 to 12) and words (13 to 17).

---

## Severity 1: grants a standing it should not (all latent)

### 1. R8's shipped switch is never read by a row

- **What.** `REFUSED_EVALUATION_CHECK` (`src/orlog/court.py:54`) switches R8 on and off. `orl.py court` reads it at its
  shipped value, since orl.py never names it. Every row that reads R8 sets the switch first and puts it back after:
  - `tests/selftest.py:1015` and `:1019`;
  - `tests/court_monotone.py:53` and `:57`.

  The shipped value is therefore never what a row reads. With it set to False (plant `r8-default-off`), the whole
  self-test reads 169/169, the R8 rows and the R8 plant among them, and `orl.py court` is the court before DP-5's
  repair.
- **Reproducers.**
  - `research/reporting-pass/reproducers/court_mutants.py --only r8-default-off` (about three minutes with its two
    controls).
  - `research/reporting-pass/reproducers/r8_default.py`.
- **Measured here** (`evidence/court_mutants.txt`, `evidence/r8_default.txt`).
  - The self-test under the plant: `r8-default-off SURVIVED ORLOG SELFTEST 169/169`.
  - `orl.py court tests/fixtures/r8/omit.orl --backends python`:
    - as the tree stands: `REFUSED at evaluation 17 (INDEX-OUT-OF-RANGE), after 16 true: not held (R8)`, UNSUPPORTED;
    - with the shipped value False: `true in 16 of 16 evaluations`, WELL-FOUNDED, sandwich CLOSED.
  - The planted module read as orl.py reads it, with every seal ratified (in memory): GROUNDED. Read as the R8 row reads
    it (the switch set first), it is withheld, whatever the shipped value.
- **Does not show** that the switch is wrong today. It is True, and orl.py reads R8 on.
- **Falsifier.** A self-test row that fails when the shipped value is False.
- **Smallest repair.** A row that reads R8 the way a person does: `orl.py court tests/fixtures/r8/omit.orl` must print
  `REFUSED at evaluation 17`. Alternatively, make R8 a parameter of `panel()` that only the plant passes, so that there is
  no shipped value to flip.
- **Row and plant.** "court R8 as orl.py reads it: omit.orl reads REFUSED at evaluation 17". It must catch
  `r8-default-off`.

### 2. R1 (no claim held unless every backend agreed) has no row

- **What.** `held` (`court.py:261`) requires `row["integrity"] == "AGREED"`. With that conjunct removed (plant
  `held-ignores-integrity`), the self-test reads 169/169. Only two rows give the court a witness that is not agreed, and
  both look at the wrong thing:
  - the BUILD-FAILED row (`tests/selftest.py:894`) checks the integrity text and that the sandwich starts VACUOUS;
  - the contested row (`:548-553`) checks only that the sandwich starts VACUOUS. Its claim, `q equals -4`, is also
    refuted by the planted reference itself, so it is not held for a second reason.

  The same row cannot see the sandwich's reason either. With the contested branch removed (plant
  `sandwich-ignores-dissent`, `court.py:311`), the sandwich reads "VACUOUS (no claim is well-founded)" and the row
  passes.
- **Reproducers.** `court_mutants.py --only held-ignores-integrity,sandwich-ignores-dissent`; `unguarded_held.py`.
- **Measured here** (`evidence/court_mutants.txt`, `evidence/unguarded_held.txt`). Under the plant,
  `fixtures/contested_true.orl` is read with every seal ratified:
  - when contested (the self-test's own reference plant, BACKEND-DISSENT): integrity CONTESTED, and yet WELL-FOUNDED and
    GROUNDED;
  - when INCOMPLETE (c99 planted not to build): the same.

  The court as built reads both UNSUPPORTED, UNGROUNDED.
- **Does not show** a contested claim reading WELL-FOUNDED in the court as built. It does not.
- **Falsifier.** A self-test row that fails under `held-ignores-integrity`.
- **Smallest repair.** The rows, not the court. The BUILD-FAILED and contested rows also require every claim UNSUPPORTED
  and UNGROUNDED with every seal ratified, on a claim true in every execution (`fixtures/contested_true.orl`). The
  contested row also requires the reason `(the backends did not all agree)`.
- **Row and plant.** Those rows. They must catch `held-ignores-integrity` and `sandwich-ignores-dissent`.

### 3. A refuted claim's exclusion from "held" has no row

- **What.** No row reads the court over a refuted claim with the backends agreeing. Two rows run a refuted claim, and
  both check only the status line:
  - the CLAIM-REFUTED runtime-refusal row (`tests/selftest.py:259`, `:271`);
  - the two law plants (`:1248`, `:1258`).

  With `r["trues"] == r["evals"]` removed from `held` (plant `held-ignores-refutation`), the self-test reads 169/169.
- **Reproducers.** `court_mutants.py --only held-ignores-refutation`; `unguarded_held.py`.
- **Measured here.** Under the plant, `fixtures/refuted_claim.orl` with its seal ratified reads `REFUTED at evaluation 1
  (REFUSED CLAIM-REFUTED 2)` together with WELL-FOUNDED and GROUNDED, and the sandwich CLOSED: one row saying both. The
  court as built reads UNSUPPORTED, UNGROUNDED and VACUOUS.
- **Does not show** the court as built doing this.
- **Falsifier.** A self-test row that fails under `held-ignores-refutation`.
- **Smallest repair, row and plant.** A court row: "a refuted claim, its seal ratified, reads UNSUPPORTED and
  UNGROUNDED, the sandwich VACUOUS". It must catch `held-ignores-refutation`.

### 4. E7's lenient comparison put back into the arbiter's verdict: 169/169

- **What.** The E7 row and its plant never reach the verdict:
  - the row (`tests/selftest.py:626-637`) calls `receipt_core` on hand-made receipts;
  - its plant (`:639-643`) runs a stand-in function, `lenient`.

  The verdict itself is `arbiter.py:233`. Plant `agreement-lenient-receipts` makes the verdict compare `parse_receipt`'s
  lines (split on any line end, every `backend ` line dropped), which is the comparison before E7. The self-test then
  reads 169/169, and among its rows `[PASS] plant arbiter-lenient-receipts: CAUGHT`: the row for E7, and the plant that
  shows the row can fail, both pass with E7 live.
- **Reproducers.** `court_mutants.py --only agreement-lenient-receipts`; `agreement_conditions.py`, third case.
- **Measured here** (`evidence/agreement_conditions.txt`). A python backend that writes its receipt with CR LF reads
  BACKEND-DISSENT under the arbiter as built. Under the planted arbiter it reads NONE, `agreeing [python]`.
  - (`evidence/court_mutants.txt` labels this plant's non-equivalence "witness_receipt_sha.py": that run started
    before the third case was added. The witness is `agreement_conditions.py`.)
- **Does not show** a false AGREED from the arbiter as built. Its comparison is exact (see the sound section).
- **Falsifier.** A self-test row that fails under `agreement-lenient-receipts`.
- **Smallest repair, row and plant.** The E7 row also arbitrates backends, through the mutate hook, that write their
  receipt with CR LF, without its final LF, and with an extra `backend` line, and requires BACKEND-DISSENT for each. It
  must catch `agreement-lenient-receipts`.

### 5. Two of the four agreement conditions have no row

- **What.** A backend agrees only if all four hold (`arbiter.py:233-234`):
  - a receipt exists;
  - its core equals the reference's;
  - its output file equals the reference's output;
  - it exited with status 0.

  No row has a backend that fails only the third, or only the fourth. Remove either condition (plants
  `agreement-ignores-output` and `agreement-ignores-exit`) and the self-test reads 169/169.
- **Reproducers.** `court_mutants.py --only agreement-ignores-exit,agreement-ignores-output`;
  `agreement_conditions.py`.
- **Measured here.** Both cases use collatz and a python backend made through the mutate hook:
  - a runtime that writes its files whole, then exits 5: BACKEND-DISSENT as built, NONE (agreeing) under the plant;
  - a runtime that appends to its output file after its receipt's sha256 was taken: BACKEND-DISSENT as built, NONE
    under the plant.
- **Does not show** that any backend does either today.
- **Falsifier.** A self-test row that fails under either plant.
- **Smallest repair, row and plant.** Two arbiter rows, those two backends reading BACKEND-DISSENT. They must catch the
  two plants.

## Severity 2: hides a dissent or a refusal

### 6. The court's reading never names a refusal outside R8; `orl.py court` exits 0 over a refusal and a failed build

- **What.** `cmd_court` (`orl.py:85-111`) prints each claim's row and the summary. Neither holds the run's status
  (`court.py:317-326`), and neither does `court_artifact`. A refusal reaches the printed reading only through a refuted
  claim's `evaluation` text or through R8. Any other refused run reads like one that completed. `cmd_court` always
  returns 0 after a reading. `cmd_run` returns 0 whenever every backend agreed, the law's refusal included
  (`orl.py:80-82`).
- **Reproducer.** `refusal_hidden.py`.
- **Measured here** (`evidence/refusal_hidden.txt`).
  - `fixtures/hoisted_omit.orl`. This is DP-5's own loop with the item read hoisted into a Let, so the same
    INDEX-OUT-OF-RANGE comes at the same iteration, one clause before the claim. The claim reads `true in 16 of 16
    evaluations`, WELL-FOUNDED and, ratified, GROUNDED; the sandwich reads CLOSED; neither `REFUSED` nor
    `INDEX-OUT-OF-RANGE` appears anywhere in the printed reading. omit.orl, the R8 control, names its refusal.
  - `fixtures/must_after_claim.orl`. A claim holds, then `It must hold that a is odd` fails (`REFUSED MUST-FAILED 3`).
    - `orl.py court`: WELL-FOUNDED, CLOSED, exit 0, and no MUST-FAILED in its output.
    - `orl.py run`: exit 0. Its line does print `ref REFUSED MUST-FAILED 3`.
  - collatz, `--backends c99`, with clang's folder off PATH. `orl.py run` exits 2 (`BUILD-FAILED did not build [c99]`).
    `orl.py court` exits 0 (`integrity INCOMPLETE (did not build: c99)`).
- **Does not show** a false standing under the court's own rules. "Held" means true at every evaluation that finished,
  and R8 covers only an evaluation of the claim that began, as DP-5's verdict drew it. Whether a claim evaluated in a
  run refused elsewhere should still be held is for the owner to rule.
- **Falsifier.** The printed reading of a refused run names the refusal, or `orl.py court` exits non-zero there.
- **Smallest repair.**
  - The summary carries the run's status (`"run": "REFUSED MUST-FAILED at §3"`), `cmd_court` prints it first, and
    `court_artifact` records it.
  - `orl.py court` exits as `run` does when integrity is not AGREED.
  - What exit status a law's own refusal gets, under `run` and `court` alike, is for the owner to rule. Today a script
    sees 0.
- **Row and plant.** `orl.py court fixtures/must_after_claim.orl` prints `REFUSED MUST-FAILED`, and `orl.py court
  --backends c99` with no clang exits as `run` does. It must catch two plants: `cmd_court` without the status line, and
  `cmd_court` returning 0 after an INCOMPLETE reading.

### 7. A warm build cache answers for a compiler that cannot build

- **What.** The arbiter keys a compiled build by its generated source and flags (`arbiter.py:133`), and returns a
  cached binary without calling the compiler (`:142-143`). The witness's provenance names `toolchains()`, which is the
  compiler on PATH now (`:365`).
  - The self-test's work folder, `build/selftest`, keeps its cache from run to run. STATUS records the second
    consecutive run made "on the first's build cache", so a self-test after a compiler upgrade would compare binaries
    the old compiler built.
  - The Python backend runs the cached source file as it finds it (`:136-140`: written only if absent), and the
    witness's `source_sha256` is the sha256 of the source generated in memory (`:224`).
- **Reproducer.** `provenance_cache.py`. It compiles a stand-in `clang` that answers `--version` with "clang version
  0.0.0 (a stand-in ...)" and builds nothing.
- **Measured here** (`evidence/provenance_cache.txt`), on collatz with c99:
  1. Folder A, real clang: built, NONE.
  2. Folder A, the stand-in first on PATH: `NONE, build cached, agreeing [c99]`, and the witness's provenance names
     clang as `'clang version 0.0.0 (a stand-in written by the reporting pass; it builds nothing)'`.
  3. Folder A, the stand-in, `fall.orl` (not cached): BUILD-FAILED.
  4. Folder B (empty), the stand-in, collatz again: BUILD-FAILED.

  The same law under the same named toolchain reads NONE in one folder and BUILD-FAILED in the other.
  - Python. With collatz's cached source overwritten by fall's program, the backend runs fall (BACKEND-DISSENT), and
    `source_sha256` names collatz's generated source. This case needs a hand on the cache, and shows only what
    `source_sha256` attests.
- **Does not show** that any binary cached on this host was built by another compiler, or that two compilers differ
  on any law. The witness does mark the build `cached`; it does not say which toolchain made it.
- **Falsifier.** A warm cache reads BUILD-FAILED under the stand-in, or the witness names the toolchain that built each
  binary.
- **Smallest repair.**
  - Put the compiler's `--version` line, the one `toolchains()` reports, into the build key.
  - Record beside each binary the toolchain that built it.
  - Run the Python backend's source from memory, or refuse a cached file whose sha256 is not the generated source's.
- **Row and plant.** With the stand-in first on PATH and a warm cache, the arbiter reads BUILD-FAILED, as it does with
  an empty folder. It must catch the present key (without the toolchain).

### 8. 21 rows pass with a backend that did not build; E10's class on both compilers reads 169/169

- **What.** 21 rows decide PASS by `not w["dissenting"]` alone, and a backend that did not build is neither agreeing nor
  dissenting:
  - the 13 runtime-refusal rows (`tests/selftest.py:271`);
  - the 600-arm If chain (`:618`);
  - E9 (`:656`);
  - the 4 R8 rows (`:1024`);
  - the 2 law plants (`:1248`, `:1258`).

  The corpus and bounds rows require every backend (`:281` and seven more sites). The chain row exists for E10's class:
  the hosts' limits on deep nesting. On C and Rust, a compiler refusing the chain is how that class would show.
  - Plant `chain-600-refused-by-compilers` adds `#error` to the c99 source, and `compile_error!` to the Rust source,
    of any law of 600 clauses or more. The self-test reads 169/169, with the row `[PASS] bounds: a 600-arm If chain
    runs byte-identically on the reference and [python]`.
- **Reproducer.** `court_mutants.py --only chain-600-refused-by-compilers`.
- **Measured here.** `evidence/court_mutants.txt`, and the self-test's own output under the plant,
  `evidence/mutants/selftest-chain-600-refused-by-compilers.txt`.
- **Does not show** any build failing today. The control's row reads `[c99,python,rust]`.
- **Falsifier.** The chain row fails under the plant.
- **Smallest repair.** Those 21 rows require `len(w["agreeing"]) == len(arb.backends)`, as the corpus rows do, or
  `not w["build_failed"]`.
- **Row and plant.** The chain row so amended. It must catch `chain-600-refused-by-compilers`.

## Severity 3: misreports a count

### 9. The court's summary counts five different failures as `unsupported`

- **What.** The summary (`court.py:317-326`) counts support values. A refutation and R8's readings are evaluation values,
  so they fall into `unsupported`, along with contested claims, claims whose backend did not build, and claims whose
  premise never ran. The summary is the last line `orl.py court` prints.
  - Latent: no row holds the summary's `well_founded` or `grounded` count; only `unreached` is asserted
    (`tests/selftest.py:539`). Plants `summary-grounded-counts-all` and `summary-well-founded-counts-unsupported` each
    read 169/169.
- **Reproducers.** `summary_absorbs.py`; `court_mutants.py --only summary-grounded-counts-all,summary-well-founded-counts-unsupported`;
  and `unguarded_held.py`, which shows the two plants change the summary.
- **Measured here** (`evidence/summary_absorbs.txt`). A refuted one-claim text and omit.orl, which R8 withholds, give
  byte-identical summaries, sandwich included. Five reasons give two distinct summaries once the sandwich is set aside.
- **Does not show** a wrong row. Each row states its own reason.
- **Falsifier.** A refuted claim and an R8-withheld claim give different summaries.
- **Smallest repair.** The summary gains `refuted` and `refused_evaluation` (R8) counts and the integrity. A row holds
  every summary count to the rows it counts.
- **Row and plant.** "The summaries of refuted_claim.orl and omit.orl differ; every count equals its rows' count on
  plankton, the inline text and R8's fixtures". It must catch both summary plants.

### 10. A certificate's cost reading drops the evaluation R8 names

- **What.** The reference adds a claim's cost only when its evaluation finishes (`src/orlog/interp.py:264`). R8 names
  the evaluation that refused and withholds the claim, but the court still prints the cost line and the CHEAPER or NOT
  CHEAPER reading, from the finished evaluations alone (`court.py:266-273`).
- **Reproducer.** `cost_over_refusal.py`. It searches the length of the certified loop for a law whose reading moves.
- **Measured here** (`evidence/cost_over_refusal.txt`), at loop length 43:
  - the court prints `check 64 ops / certified clause 130 ops`, `CHEAPER (at most 1/2 ...)`;
  - the claim's evaluations spent 67 counted operations, the refused one included, and 67 against 130 reads NOT
    CHEAPER.
- **Does not show** a standing: the claim is not held either way.
- **Falsifier.** The cost reading of a withheld claim counts its refused evaluation, or reads nothing.
- **Smallest repair.** When R8 names an evaluation, the reading says `NOT READ: evaluation n refused (R8); the line
  counts its m finished evaluations`. Counting the refused evaluation in the receipt instead would change the receipt,
  which is a new version.
- **Row and plant.** "This text's certificate reads no CHEAPER". It must catch the present reading.

### 11. COMPAT-0 checks only the frozen texts that have a baseline row; a settled entry needs no reason

- **What.**
  - `compare` (`tests/compat.py:168-191`) walks the baseline's rows. Nothing checks that every frozen text has a row,
    or that the rows number the header's `count` (3,361). A frozen text without a row is never compared, and `check`
    prints HELD over the rest.
  - A settled entry is read for `now` alone (`:187`). The README requires `{"id", "now", "reason", "amendment"}`, but
    an entry of only id and now settles a change.
  - `check` prints the settled count and names no settled text.
- **Reproducer.** `compat_gate.py`. It runs on a copy of `tests/compat/` under `work/reporting-pass/compat-copy/`, and
  the tracked files are only read.
- **Measured here** (`evidence/compat_gate.txt`).
  - (a) One row removed. `cmd_check --jobs 8` prints `3360 texts ... COMPAT-0 HELD` and exits 0. The texts file
    still holds 3,361 texts, and the self-test's compat row (its own test applied to the output) reads PASS.
  - (b) compat.py's own plant `reserve-tick` makes fall.orl's frozen version differ. With its row removed, all 360
    remaining texts read the same.
  - (c) `{"id": ..., "now": {...}}`, with no reason and no amendment, settles it.
- **Does not show** any such edit in the history. Each needs an edit to a tracked frozen file, which AGENTS forbids
  and git shows.
- **Falsifier.** `check` reads BROKEN with a row removed, or with a settled entry that has no reason.
- **Smallest repair.**
  - `check` refuses unless the baseline's ids are exactly the texts file's ids, as many as the header's count.
  - `compare` refuses a settled entry whose reason or amendment is empty.
  - `report` names every settled text.
- **Rows and plants.** COMPAT selftest gains `baseline-row-removed` and `settled-without-reason`, each of which must
  read BROKEN, against the present `cmd_check` and `compare`.

### 12. court_monotone counts no CIRCULAR change, and its plant is the measurement read backwards

- **What.**
  - `standing()` (`tests/court_monotone.py:71-72`) reads WELL-FOUNDED and GROUNDED only, so a claim that moves between
    CIRCULAR and UNSUPPORTED (held, or not) counts neither as gained nor as lost.
  - The plant (`:138`) is `compare(..., swap=True)`. Its gains are the losses read the other way, claim for claim, so
    it reads CAUGHT exactly when something was lost, which `ok` already requires. It tests the comparator, never a
    court that grants.
  - The docstring (`:6`) says the texts run "under COMPAT-0's budget". The code gives every text 10^6 (`:30`); COMPAT-0
    gives the corpus 10^7.
- **Reproducer.** `monotone_blind.py`.
- **Measured here** (`evidence/monotone_blind.txt`).
  - (a) `fixtures/cycle_refusal.orl` holds two claims that support each other; the second refuses inside its
    condition at its second evaluation. R8 moves both from CIRCULAR to UNSUPPORTED: 2 readings changed, 0 gained,
    0 lost. Read in the plant's direction, a court granting "held", there are 0 gains, so the plant would read NOT
    CAUGHT on this text.
  - (c) Over R8's four fixtures and this one: lost 5, the plant's gains 5, the same claims.
  - (b) No frozen text with claims stops under 10^6 today: 0 dropped. The budget affects nothing measured today;
    only the docstring miswords it.
- **Does not show** that R8 grants anything. It does not, on these texts.
- **Falsifier.** A granting rule that moves a claim from UNSUPPORTED to CIRCULAR reads NOT ONE-SIDED.
- **Smallest repair.**
  - Count every move up the order UNSUPPORTED < CIRCULAR < WELL-FOUNDED, and every change of held.
  - Add `cycle_refusal.orl` to R8's fixtures.
  - Replace the mirror with a court that grants: for instance `held-ignores-refutation` as the court after R8, which
    must show gains.
  - Use COMPAT-0's budget for each kind.
- **Row and plant.** The R8 one-sidedness row, with cycle_refusal.orl's two moves counted as lost. It must catch two
  plants: `standing()` without CIRCULAR, and a court that grants.

## Severity 4: only miswords

### 13. `orl.py court` never prints the CONSTANT note

- **What.** The panel marks a claim that reads no variable CONSTANT (red team E5, TRIAGE's tautology airlock). The note
  is in the row as `condition`, but `cmd_court` prints a fixed list of keys without it (`orl.py:103-104`).
  - The CONSTANT row (`tests/selftest.py:699-705`) reads the panel in process.
  - No row reads `orl.py court`'s rows at all. Its only row stops at LEDGER-BROKEN (`:920`), and no row runs
    `orl.py run`.
- **Reproducer.** `cli_omissions.py` (a).
- **Measured here** (`evidence/cli_omissions.txt`). `fixtures/constant_claim.orl`, §2 `We claim that 1 equals 1, by
  the owner.`: the panel's row reads CONSTANT, while `orl.py court` prints channel, integrity, evaluation, ratification,
  external_bits, support and grounding, and no CONSTANT. Ratified, it would read GROUNDED with no note.
- **Does not show** that the JSON artifact omits it. `--json` writes the whole row, note included.
- **Falsifier.** `orl.py court` prints CONSTANT for §2.
- **Smallest repair.** Add `condition`, and the claim's seal, to the printed keys.
- **Row and plant.** `orl.py court fixtures/constant_claim.orl` prints CONSTANT for §2 and not for §3. It must catch the
  present key list.

### 14. AGREED names no backend

- **What.** Integrity reads `AGREED` whichever backends ran, and neither the printed reading nor the `--json` artifact
  names them.
- **Reproducer.** `cli_omissions.py` (b).
- **Measured here.** `orl.py court examples/collatz.orl` with `--backends python` and with `python,c99,rust`: the
  printed readings are byte-identical, and so are the artifacts once the chain hash is set aside. No backend's name
  appears anywhere in the printed reading.
- **Does not show** a false AGREED. The backends that ran did agree.
- **Falsifier.** The two readings differ.
- **Smallest repair.** `AGREED (reference, c99, python, rust)`, and the witness's backends and toolchains in the
  artifact's provenance.
- **Row and plant.** `orl.py court --backends python` names python and no other backend. It must catch an integrity
  string without names.

### 15. R8 reads a plain Otherwise clause's claim as "possible"

- **What.** A plain Otherwise clause keeps its RawIf as its statement (`src/orlog/syntax.py:279-281`), so
  `refusal_in_claim` (`court.py:68`) reads its inline claim "possible". The row then says the refusal "may come from the
  condition or the other arm its clause holds". An Otherwise clause has no condition and holds no other arm: the If's
  condition is evaluated at the If's own clause. The standing is the same (withheld); the words are wrong. An "Otherwise,
  if" clause and an If's own clause are correctly "possible".
- **Reproducer.** `r8_wording.py`.
- **Measured here** (`evidence/r8_wording.txt`).
  - `fixtures/otherwise_claim.orl`: status `REFUSED INDEX-OUT-OF-RANGE 4`, which is §2.2, the Otherwise; R8 reads
    'possible', with the wording above.
  - The control, in which the If's condition before an Otherwise refuses: the status names §2.1, the If's own clause.
- **Does not show** any change of standing.
- **Falsifier.** A plain Otherwise clause that evaluates something besides its arm at its own id.
- **Smallest repair.** `refusal_in_claim` reads "exact" also for a plain Otherwise clause whose arm is the claim
  (`RawIf`, kind `otherwise`, not a block). Both readings withhold, so no standing moves.
- **Row and plant.** otherwise_claim.orl reads `REFUSED at evaluation 17`. It must catch the present predicate.

### 16. The witness's receipt hashes cannot be compared

- **What.** The two hashes are taken over different things, and neither is the core the verdict compares:
  - the reference's `receipt_sha256` is the sha256 of its whole receipt (`arbiter.py:266`);
  - a backend's is the sha256 of `parse_receipt`'s lines (`:287-295`), split on any line end, every `backend ` line
    dropped, joined by LF.

  So the two never match, even when the backends agree.
- **Reproducer.** `witness_receipt_sha.py`.
- **Measured here** (`evidence/witness_receipt_sha.txt`).
  - An agreeing run: the reference's d5d2c4a1… against python's f0068755….
  - A python backend writing its receipt with CR LF is, correctly, BACKEND-DISSENT. Yet every field of its summary
    equals an agreeing run's: status, output_sha256, events, trace_head, ops, exit and receipt_sha256. The note reads
    `traces equal; the difference is outside the event chain (exit 0)`. The witness reports a dissent and shows nothing
    that differs. This is E7's leniency, alive in the display.
- **Does not show** a wrong verdict.
- **Falsifier.** An agreeing run's two hashes are equal.
- **Smallest repair.** Both hashes are of `receipt_core` (None when the frame is wrong), and `localize` names a core
  mismatch when traces and outputs are equal.
- **Row and plant.** An agreeing run's reference and backend hashes are equal, and the CR LF backend's differs. It must
  catch the present `_summary`.

### 17. A ledger line that is a JSON object of the wrong shape ends `orl.py court` in a traceback

- **What.** `read_ledger` (`court.py:177-195`) refuses a line that is not JSON or not an object. A line that is an
  object passes, and `panel` then indexes `e["claim_seal"]` and `e["name"]` (`:218-219`). LEDGER-BROKEN exists so that
  failure is deterministic and never a traceback (AGENTS §7).
- **Reproducer.** `ledger_malformed.py`. Its fixture ledgers are written under `work/reporting-pass/ledgers/`; none is
  the default ledger, and none ratifies anything.
- **Measured here** (`evidence/ledger_malformed.txt`):
  - `{"kind": "claim"}`: exit 1, `KeyError: 'claim_seal'`, a traceback;
  - `{"kind": "theorem"}`: `KeyError: 'name'`;
  - a `claim_seal` that is a list: `TypeError`;
  - the torn control: LEDGER-BROKEN, with no traceback.
- **Does not show** a reading from a malformed ledger. There is none: the run fails.
- **Falsifier.** Each of the three refuses LEDGER-BROKEN.
- **Smallest repair.** `read_ledger` checks each entry's shape (a claim's `claim_seal` 64 lowercase hex, a theorem's
  `name` a string) and refuses LEDGER-BROKEN at its line.
- **Row and plant.** The three lines refuse `LEDGER-BROKEN at line 1` by the reader and by `orl.py court` (exit 1, no
  traceback). It must catch the reader without the shape check.

### 18. The isolation row and its plant pass with the shared-folder defect live

- **What.**
  - The isolation row (`tests/selftest.py:852-857`) checks that each arbitration made a folder and removed it. It does
    not check where the runs happened.
  - Its plant (`:874-881`) hands both arbitrations one folder, and is caught when they got one folder: by
    construction.

  Plant `run-folder-made-but-shared` lets each arbitration make and remove its own folder while running in a shared
  one. Under it, in both runs, the isolation row read PASS and its plant CAUGHT, and the race row read FAIL, out of 16
  arbitrations:

  | run | BACKEND-DISSENT | FileNotFoundError | PermissionError | NONE |
  |---|---|---|---|---|
  | first | 9 | 4 | 1 | 2 |
  | consolidated | 6 | 4 | 3 | 3 |

  The two error columns are tracebacks. The self-test did catch the defect, through the race row, which has no plant of
  its own and whose counts depend on timing.
- **Reproducer.** `court_mutants.py --only run-folder-made-but-shared`.
- **Measured here.** `evidence/mutants/selftest-run-folder-made-but-shared.txt` (the consolidated run) and
  `evidence/court_mutants.txt`.
- **Does not show** the arbiter as built sharing a folder. It does not.
- **Falsifier.** The isolation row fails under the plant.
- **Smallest repair.** Give the race row this plant as its own. The isolation row should either check that a run's
  files appear only in its own folder, or say that it checks the folder's making and removal.
- **Row and plant.** The race row, which must catch `run-folder-made-but-shared`.

### Wordings found by reading alone (DECLARED; no effect measured)

- `COURT_RULES` R1 (`court.py:31-32`) says that without agreement "the integrity column reads CONTESTED". The column
  also reads INCOMPLETE and REFERENCE-ONLY (`:241-246`). The rule's text travels in every court artifact.
- compat.py's `receipt_core` docstring (`tests/compat.py:58`) calls it "the same rule as the arbiter's". It is laxer:
  no head, final LF or CR check. That the laxity reaches no verdict is measured (sound section, COMPAT-0).
- court_monotone's docstring budget (finding 12 (b)).

---

## What was examined and found sound

This section gives the absence of findings a stated scope. "Measured" names a run; "read" means only the code was read
(DECLARED).

- **The arbiter's comparison** (`arbiter.py:70-84`, `:226-235`).
  - `receipt_core` is the exact bytes without the second line, and only that line. A CR LF receipt, one without its
    final LF, one with an extra line and one with a wrong head are all refused. Measured: compat_gate.py (d), and the
    CR LF backend in witness_receipt_sha.py, which reads BACKEND-DISSENT.
  - E7's repair holds in the verdict as built. Finding 4 concerns its row.
- **The arbiter's kinds.**
  - The kind is read over the backends that built.
  - A failed build or a host stop counts neither as agreeing nor as dissenting.
  - REFERENCE-DISSENT needs two or more backends agreeing against the reference.

  Read, and held by the E8, honesty and reference-plant rows. Plant `agreed-always` was caught by the BUILD-FAILED row
  (measured).
- **Backends exit 0 on a refusal** (`rt_py.py:119-126`; `rt_c/orlog_rt.h:431-456`; `rt_rs/orlog_rt.rs:1326-1384`), so
  the exit-status condition never turns a refusal into a dissent. Read, and measured on the runtime-refusal rows.
- **R8's exact branch is sound.** A clause whose statement is the claim evaluates nothing else under its id:
  - an If arm's condition runs at that arm's clause (`interp.py:212-214`);
  - a rule's refusal names the clause that used the rule (`:423-440`);
  - a performed procedure's clauses run under their own ids (`:242-244`);
  - a claim refuses CLAIM-REFUTED only after its counts are taken (`:261-267`);
  - HostStop is checked at a statement's entry, and no expression holds a statement.

  So "exact" never reads a refusal that began elsewhere, and "REFUSED at evaluation evals+1" numbers it right, since
  evals counts finished evaluations.
  - Measured (`r8_exact_sites.py`, `evidence/r8_exact_sites.txt`): with the claim's condition refusing at its 17th
    evaluation, the status names the claim's clause, R8 reads 'exact' and the row reads `REFUSED at evaluation 17` in
    all 7 places tried. They are: the clause's own statement; a procedure performed in a loop; a block If's
    sub-clause; an Otherwise block's sub-clause; a While body; a rule whose proviso refuses; and a rule whose value
    refuses.
  - Measured (`r8_wording.py`): inline_claim, inline_condition and an "Otherwise, if" clause read 'possible'. In the
    control, the If's condition is named at its own clause.

  The "possible" branch withholds, as declared, and is wider than needed only for a plain Otherwise (finding 15).
- **The status line's parse** (`court.py:214-216`). The reference writes `REFUSED <CODE> <clause>`, and no code holds
  a space. Read.
- **Premises name claim clauses only** (PREMISE-TARGET, `sema.py:226-229`), so `by_label[p].stmt.id` is always a claim
  id. Read.
- **GROUNDED** is the least fixed point of: held, an admissible channel, and the claim's own seal ratified, over
  premises. It is held by the L4, L8 and R2 rows. Plants `court-grounds-computation` (the self-test's own) and
  `grounding-skips-premises` are caught (measured).
- **R7.** `held` requires an evaluation, and plant `held-ignores-unreached` is caught by the inline row (measured, the
  harness's control).
- **LEDGER-BROKEN** for a torn line or a non-object line (row and plant). Finding 17 is the gap beside it.
- **COMPAT-0's verdicts.**
  - Results are compared as whole records.
  - "Newly accepted" applies only to a refusal that becomes something other than a crash, and a crash reads DIFFERS.
  - A settled entry must give the exact new result; its self-test plants a declaration one line off.
  - INPUT CHANGED is decided by sha256.

  Read, and measured by its self-test (6/6 within the self-test's compat row). compat.py's own `receipt_core`
  (`:57-64`) is laxer than the arbiter's, though its docstring calls it "the same rule as the arbiter's". It hashes
  everything but the second line, so every framing change still reads DIFFERS (measured, compat_gate.py (d)): a
  miswording with no effect.
- **COMPAT-0's history table** prints `skipped` for a stopped run as well as a skipped one (`compat.py:315`). No corpus
  text stops at v0's budgets, so no cell is affected today. Read; DECLARED.
- **The twin probes' comparison** (`tests/compare_probes.py`) compares the fields each probe holds. Every accepted probe
  holds all seven, and every refused one its code: 163 probes in round 2 and 128 in round 3, counted here. So no probe
  is counted identical on no field today.
- **court_monotone's synthesized witness.** It is agreed by construction. Under a witness that is not agreed nothing
  is held, so R8 can change nothing there. Its fixture ledger ratifies every seal, so GROUNDED is reachable. Read, and
  measured in finding 12 (b).
- **The witness firewall** (`VERDICT_KEYS`): row exists, read.

## What was not examined

These are reporters too, outside this pass's scope, so nothing is said of them:
- `court/judge.py` and `court/build_record.py`, the court record's judge;
- `src/check_chain.py`;
- `tests/diff_twin.py`'s grouping of signatures (its worker compares through the arbiter's strict `receipt_core`);
- `tests/vectors_independent.py`, `tests/race_arbiter.py`, `tests/asan_c.py` and the E21 measurements;
- the twin;
- the runtimes beyond their exit statuses.

Nothing was run on another host, and no timing is claimed.

## The reproducers

All are in `research/reporting-pass/reproducers/`. Each writes only under `work/reporting-pass/` (run_all.py also writes
`research/reporting-pass/evidence/`). Each loads a planted module in memory (`_common.planted`) or plants in a copy of
the tree, and no tracked file is written.

| reproducer | what it runs | findings |
|---|---|---|
| `court_mutants.py` | the whole self-test once per plant, on a copy of the tree, with two controls | 1–5, 8, 9, 18 |
| `unguarded_held.py` | the court plants against the court as built, one fixture each | 2, 3, 9 |
| `agreement_conditions.py` | the arbiter plants against the arbiter as built, three mutant backends | 4, 5 |
| `r8_default.py` | R8's shipped value, as orl.py reads it and as the R8 rows read it | 1 |
| `refusal_hidden.py` | refused runs through the court's printed reading, and the exit statuses | 6 |
| `provenance_cache.py` | the build cache under a stand-in compiler | 7 |
| `summary_absorbs.py` | the summary for five reasons a claim is not held | 9 |
| `cost_over_refusal.py` | a certificate's cost reading over a refused evaluation | 10 |
| `compat_gate.py` | COMPAT-0 on a copy of its files | 11, sound section |
| `monotone_blind.py` | court_monotone's comparator, plant and budget | 12 |
| `cli_omissions.py` | what `orl.py court` prints | 13, 14 |
| `r8_wording.py` | R8's split between exact and possible | 15, sound section |
| `r8_exact_sites.py` | R8's exact branch in the 7 places a claim can stand | sound section |
| `witness_receipt_sha.py` | the witness's receipt hashes | 16, sound section |
| `ledger_malformed.py` | ledger lines of the wrong shape | 17 |
| `run_all.py` | runs the others and records `evidence/` | — |
| `fixtures/*.orl` | the texts named above | — |

## The self-test, after

Nothing tracked was changed. `python -B tests/selftest.py` read `ORLOG SELFTEST 169/169 (backends: python,c99,rust)`
before this pass and again after it, with no FAIL row (`evidence/selftest-before.txt`, `evidence/selftest-after.txt`).
