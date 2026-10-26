# COMPAT-0 status: what the frozen texts exercise of the court's R8 (2026-10-26)

**The question.** A review the owner relayed asked what lies behind "R8 changes nothing on the 3,361 frozen texts"
(`evidence/court-r8.txt`). Either no claim's evaluation ever refuses in the corpus, or claims do refuse and none reads
held or GROUNDED anyway. The two say different things about coverage.

**The count** (`research/r8_coverage.py`; output `evidence/r8-coverage.txt`; MEASURED, two runs byte-identical). Every
frozen text runs on the reference under COMPAT-0's budget for its kind. Every claim's seal is ratified by a fixture
line and the witness is made agreed, as `tests/court_monotone.py` does, so that only the court's rules are read. The
court before R8 is `panel(..., r8=False)`.

| the 3,361 frozen texts | count |
|---|---|
| refused at compile | 3,061 |
| accepted, with no claim | 256 |
| stopped by the host | 0 |
| ran, with claims | 44: 38 completed, 6 refused CLAIM-REFUTED |

| their 65 claims | count | what R8 does to it |
|---|---|---|
| R8's class: the run refused at the claim's own clause with a code other than CLAIM-REFUTED | **0** | — |
| refuted: the run refused CLAIM-REFUTED at the claim | 6 | nothing (a finished, false evaluation) |
| held in a run refused elsewhere | 1 | nothing (the refusal is not at its clause) |
| held in a completed run | 52 | nothing |
| never evaluated | 6 | nothing |

**The answer: no exercise in the corpus.** In the frozen texts, no run with a claim refuses with any code but
CLAIM-REFUTED, which is a claim's own false verdict, counted before the run refuses. So no claim's evaluation is ever
cut off. R8's class has no member, and R8 could change nothing there, whether the claim was held or GROUNDED. R8 is
exercised only by its fixtures, all of them held by the self-test and by `tests/court_monotone.py`:
- the six in `tests/fixtures/r8/`;
- `tests/fixtures/court/certificate_refused.orl`.

**Beside it: one claim held in a run refused elsewhere.** `mutant/s1/2127`, §3: "true in 1 of 1 evaluations",
UNSUPPORTED, while the run refused CLAIM-REFUTED at another claim, §4. Whether a claim that held stays held in a run
that refused elsewhere is the question the reporting pass left for the owner (`research/reporting-pass/DISPOSITION.md`).
The frozen set holds one instance of it. The court's fixture for it is `tests/fixtures/court/hoisted_omit.orl`.

**Does not show:**
- any text outside the frozen set;
- the compiled backends, since the witness was made agreed;
- that the frozen set is a fair sample of laws people will write.

New texts join only through a new COMPAT version (`tests/compat/README.md`).

**Falsifier:** a frozen text whose run refuses at a claim's own clause with a code other than CLAIM-REFUTED. The count
above would then read it in R8's class, and `tests/court_monotone.py` would show its reading change.
