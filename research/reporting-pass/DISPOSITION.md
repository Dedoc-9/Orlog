# The reporting pass: what became of each finding (2026-10-26)

The disposition of the 18 findings in `FINDINGS.md`, written by the session that proposed the pass and integrated it, at
the owner's word: "review and integrate the adversarial reporting passes lessons/fixes".

**Reviewed before anything was changed.** On the tree the pass reviewed (f16dc26), unchanged:
- its 14 quick reproducers gave byte-identical output to the pass's evidence, headers apart
  (`reproducers/run_all.py --out`);
- its mutation harness gave the same verdict for every plant: 10 of 14 regressions left the self-test at 169/169,
  and both controls held.

So every MEASURED finding was reproduced here before any was conceded.

**How each is held now.** Every repair has a row in `tests/selftest.py`, and every row has a plant. The plant is the
pass's own regression, made in a copy of the module in memory (`tests/plants.py`), so it lands in the code the row is
about and never in a stand-in. None of the receipts changed, and COMPAT-0 holds.

| # | finding | disposition | its row's plant |
|---|---|---|---|
| 1 | R8's switch never read at its shipped value | repaired: R8 is panel's parameter `r8=True`; the module switch is gone, so `orl.py` and every row read one value. A row runs `orl.py court` on omit.orl | `r8-default-off` |
| 2 | R1 had no row | rows: a claim true in every execution, its seal ratified, reads UNSUPPORTED and UNGROUNDED when the backends dissent and when one did not build; the contested sandwich must give its own reason | `held-ignores-integrity`, `sandwich-ignores-dissent` |
| 3 | a refuted claim's exclusion had no row | row: refuted_claim.orl, ratified, reads UNSUPPORTED, UNGROUNDED, VACUOUS, and the summary counts it refuted | `held-ignores-refutation` |
| 4 | E7's plant never reached the verdict | rows: three Python backends with a CR LF receipt, one without its final LF and one with a second backend line, each BACKEND-DISSENT in the arbiter's verdict. The stand-in plant is removed | `arbiter-lenient-receipts (in the verdict)` |
| 5 | two agreement conditions had no row | rows: a backend that exits 5 after a whole run, and one whose output grew after its receipt, each BACKEND-DISSENT | `agreement-ignores-exit`, `agreement-ignores-output` |
| 6 | a refusal outside R8 was invisible; `orl.py court` exited 0 over a failed build | repaired: the reading prints `run <status>` and `integrity` first, and the summary carries both; `orl.py court` exits 2 over a dissent, a failed build or a host stop, as `run` does. Two questions stay open for the owner, below | `court-prints-no-run-status`, `court-exits-0-over-a-failed-build` |
| 7 | a warm cache answered for a compiler that could not build | repaired: the compiler's `--version` line is in the build key; beside each binary a record of its toolchain and sha256 is checked before it runs; a cached Python source that is not this law's is written again and read back, or refused | `cache-ignores-toolchain` (a stand-in compiler first on PATH), `python-cache-runs-as-found` |
| 8 | 21 rows passed with a backend that did not build | repaired: they require every backend that ran to agree | `chain-600-refused-by-compilers` |
| 9 | the summary counted five failures as one | repaired: the summary gains `run`, `integrity`, `refuted` and `refused_evaluation`, and a row recounts every count from the rows on six texts | `summary-grounded-counts-all`, `summary-well-founded-counts-unsupported` |
| 10 | a certificate's cost read over a refused evaluation | repaired: NOT READ when R8 withholds the claim, and R4's text says so. The receipt is unchanged; counting the refused evaluation there would be a new version | `cost-read-over-a-refused-evaluation` |
| 11 | COMPAT-0 compared only the texts with a row; a settlement needed no reason | repaired in `tests/compat.py`: `check` refuses unless the rows are exactly the frozen texts, as many as the header counts; a settled entry needs its reason and amendment; every settled text is named. COMPAT SELFTEST gains two plants | `baseline-row-removed`, `settled-without-reason` |
| 12 | the one-sidedness count was blind to CIRCULAR, and its plant was a mirror | repaired in `tests/court_monotone.py`: three orders (support with CIRCULAR, grounding, held), every changed reading counted, COMPAT-0's budgets by kind, cycle_refusal.orl among the fixtures, and a court that grants as the plant | `standing-without-circular`, `court-grants-a-refuted-claim` |
| 13 | `orl.py court` never printed CONSTANT | repaired: it prints `condition` and the claim's seal | `court-prints-no-condition` |
| 14 | AGREED named no backend | repaired: `AGREED (the reference and …)` | `integrity-names-no-backend` |
| 15 | a plain Otherwise clause read "possible" | repaired: its claim's refusal is read exactly | `r8-otherwise-read-as-possible` |
| 16 | the witness's receipt hashes could not be compared | repaired: `receipt_core_sha256` for the reference and every backend, none when the frame is wrong; the divergence note says where a difference outside the event chain lies | `witness-hashes-parsed-lines` |
| 17 | a ledger line of the wrong shape ended in a traceback | repaired: `read_ledger` checks each line's kind and shape, and refuses LEDGER-BROKEN at its line | `ledger-reads-any-object` |
| 18 | the isolation row could not see where runs happened | repaired: the row records each run's folder and requires every run inside its own arbitration's | `run-folder-made-but-shared` |
| — | three wordings found by reading | repaired: R1's text names INCOMPLETE and REFERENCE-ONLY, compat.py's `receipt_core` says it is laxer and why that is harmless, court_monotone states its budgets | — |

The fixtures the rows read were copied from `reproducers/fixtures/` into `tests/fixtures/court/` and
`tests/fixtures/r8/` (cycle_refusal.orl, otherwise_claim.orl), with one added: `certificate_refused.orl`, the
certificate whose 17th evaluation refuses.

## Found while integrating

The first version of finding 7's Python check published the source while the file was still open for reading. On
Windows the rename failed, `publish` kept the copy already there, and the wrong source ran. That copy then made
`--backends python` read CONTESTED. Its own row caught it on the first run, as did the names row (208/210). The file is
now closed first and read back after writing, and a source that cannot be written again refuses BUILD-FAILED.

## The checks, after

On f16dc26 with these repairs:
- `python -B tests/selftest.py`: `ORLOG SELFTEST 210/210`, two consecutive runs byte-identical; `194/194` with
  `--backends python` (`evidence/selftest-run.txt`, `selftest-run2.txt`, `selftest-python-only.txt`).
- `python -B tests/compat.py check --jobs 8`: `COMPAT-0 HELD`; `selftest`: `COMPAT SELFTEST 8/8`
  (`evidence/compat-after-reporting-pass.txt`).
- `python -B tests/court_monotone.py --jobs 8`, twice, identical: `COURT R8 ONE-SIDED: 0 gained, 9 lost (frozen texts
  0, fixtures 9; cycle_refusal.orl 2)` (`evidence/court-r8.txt`).
- The pass's quick reproducers, rerun on the repaired tree (`evidence-after/`):
  - eight read the repaired behaviour outright. For example:
    - `cli_omissions`: a backend's name in the printed reading, True;
    - `ledger_malformed`: 0 of 3 malformed objects read and then raised;
    - `provenance_cache`: a warm cache answers for a compiler that cannot build, False;
    - `cost_over_refusal`: the withheld certificate reads NOT READ;
    - `summary_absorbs`: 5 distinct summaries for 5 reasons a claim is not held.
  - four stop with an error, because the code they target was repaired: `unguarded_held` (its plant's text no longer
    occurs), `r8_default` (the switch is gone), `witness_receipt_sha` (the field is now `receipt_core_sha256`) and
    `monotone_blind` (`readings` now takes a budget).
  - two read it with a caveat:
    - `refusal_hidden` reads one command-line case exiting 0: a law's own refusal, the owner's question below;
    - `compat_gate` (b) still shows that `compare` alone cannot see a removed row. `check` now refuses before
      comparing, (a).
  - The `evidence-after/` headers name the tree through `run_all.py`, which calls any uncommitted change "the R8
    repair". The integrating session corrected that phrase in the copies, and says so in each header.

## Open, for the owner

- **What a law's own refusal exits with.** `run` and `court` both exit 0 today.
- **Whether a claim that held stays held in a run refused elsewhere.** hoisted_omit.orl's claim reads "true in 16 of 16
  evaluations" and WELL-FOUNDED, and the run refused one clause before it. The reading now says so on its first line;
  the standing is unchanged. R8 covers only an evaluation of the claim that began. *(Note, 2026-10-26: settled for
  RUN-1's PREFIX claims and a refusal at a tick by his R6 ruling, `research/run-1/RULINGS.md`: the claim stays held.
  Open for a refusal before the first input and for every closed run, this fixture's case.)*
- **The pass's own reproducers target f16dc26.** Several of its plant texts no longer occur in the repaired code, so its
  mutation harness reads them NOT APPLIED. Their regressions live on as the self-test's plants.
