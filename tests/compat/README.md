# COMPAT-0: the conservative-extension gate

**What it holds.** Every text that version 0 of the language accepted keeps its law bytes and its run. Every text
version 0 refused keeps its refusal, or becomes accepted. This is MEASURED on the frozen set below and DECLARED for
every other text. It is the first rung of the roadmap (`research/roadmap-debate/VERDICT.md`), built at the owner's word
of 2026-10-26.

**Why the run, not only the seal.** A law seal says the law's bytes are the same. It does not say the law does the same
thing. The plant `say-counts-twice` makes the reference count one more operation per Say: no law seal moves, and 99
receipts do. So the baseline holds the core of each text's reference receipt: its status, output, events, trace head,
operations and claims.

## The files

| file | what |
|---|---|
| `texts-v0.json.gz` | the 3,361 frozen texts, their bytes in base64, gzip written with mtime 0. Every version of every corpus program in the history (13, chaos and leapfrog's notes before and after b4eaf11 among them); the twin's hand-worked probes (291); the red team's and E21's fixtures and the twin's inputs (57); and 3,000 mutants, diff_twin's seed 1, the same mutants as `evidence/difftwin-n3000-seed1.txt` |
| `baseline-v0.jsonl` | line 1, the header: the commit (b4eaf11), the texts file's sha256, the budgets and the note that records the owner's word; then one line per text: its id, its bytes' sha256 and its result. A result is a refusal code and line; or a law seal, a text seal, a status and the sha256 of the receipt's core; or a stop by the host at an operation; or a crash, frozen as found. v0 holds 3,061 refusals and 300 completed runs, and no stop or crash |
| `settled.json` | declared changes, empty at v0 |

The budgets of counted operations are 10^7 for the corpus and 10^6 for the rest. A run past its budget is recorded as
stopped, at its operation, which is the same on every run.

## Running it

```
PYTHONHASHSEED=0 python -B tests/compat.py check --jobs 8         # the gate: COMPAT-0 HELD
PYTHONHASHSEED=0 python -B tests/compat.py selftest               # its plants: COMPAT SELFTEST 6/6
PYTHONHASHSEED=0 python -B tests/compat.py history REV [REV ...]  # the audit: the frozen texts under each revision
```

The self-test runs the first two as its `compat` rows. `history` takes each revision's `src/` from git into `build/`,
leaves the working tree alone, and computes the frozen texts there. For revisions older than the host budget, it runs
unbounded only the texts whose baseline finished within its budget, and skips the others.

## A change, declared

`check` reads a text's verdict as one of these:
- **same**;
- **newly accepted**: refused at v0, accepted now. This is an extension: it is allowed, counted and listed;
- **settled**: a declared change;
- **differs**: the gate fails;
- **input changed**: the frozen text itself was altered. The gate fails, and names the input, never the compiler.

A deliberate change of a v0 text's result goes into `settled.json` as `{"id", "now", "reason", "amendment"}`:
- `now` is the text's exact new result;
- `amendment` names the SPEC section or rung that made the change, recorded before the code it governs.

The gate passes the text only when its result equals `now` exactly; the self-test plants a declaration one line off,
and it fails. A rung that changes many texts (a new law version, say) freezes a new version, `freeze --version v1
--note …`, at the owner's word. It never rewrites v0, which `history` keeps checkable.

## What COMPAT-0 does not protect

The owner asked for this list on 2026-10-26, naming the first three. Each line says why the gate cannot see the thing,
and what does see it, if anything.

| not protected | why the gate cannot see it | what does, if anything |
|---|---|---|
| **Performance.** For example the four-way check of a just-edited law, 5.6 s cold and 0.66 s warm, or the reference's 0.67–1.74 M counted operations a second (the architect's figures, OBSERVED) | the gate compares results, never timings: a change ten times slower passes | nothing. Timings are software timings on one host and no row asserts one. PERF-0 would add a benchmark that prints and asserts nothing |
| **Memory over long runs**, still relevant after bounded execution | the gate runs only the reference, under a budget of counted operations; it never runs a compiled backend, nor a run long enough to grow | the self-test's `memory` row and the E21 measurements, on two programs (`evidence/e21-*.txt`); the bound is DECLARED in general (RUNTIME-SPEC §4a) |
| **The arbiter**: false dissents from runs sharing a work folder (the defect found on 2026-10-25), and any other defect of the comparison | the gate calls the reference in process and never the arbiter | the self-test's isolation rows (one folder per arbitration, its plant, a race of 16) and the race of 48 (`evidence/race-after.txt`) |
| **The backends** | the baseline holds the reference's receipts; whether Python, C99 and Rust still produce them is not compared here | the self-test's `corpus` rows (four executions) and the arbiter on every run |
| **Texts outside the frozen set** | the gate samples; it does not enumerate | the differential run against the twin; new texts join through a new version |
| **The door's events** | the gate holds refusal codes, text seals and receipts. A door that turned the same bytes into the same text with different repairs or notes would pass | the self-test's `door` rows |
| **Refusal messages** | only the code and the line are held | nothing: a message is not part of the contract |
| **The court's readings** | standings come from the receipts and the ledger, outside the receipt | the self-test's `court` rows |
| **Other hosts** | everything here ran on one host | HOST-0, not yet run: NOT_MEASURED |
| **The baseline's correctness** | it freezes what b4eaf11 did, defects included: a wrong result there is held as right until a declared change repairs it | the twin's probes, the vectors' derivation, the courts; nothing mechanical |

It is a regression gate, not a proof of meaning. Two compilers agreeing on these texts' law bytes and receipts shows
that the language kept its word over time. It does not show that the word was right.

## The audit trail, at the freeze (`evidence/compat-history.txt`)

- **fc19339 and b4eaf11** reproduce the baseline on all 3,361 texts.
- **83eb044 and 7186e50** differ on exactly two: the probe `ln-place-before-condition` and one mutant of it. Each
  reads refused UNDECLARED where v0 reads LOOP-NESTING. That is SPEC §14 item 8's code change in fc19339, a loop's
  place checked first.
- **Every version of every corpus program** has the same law seal, text seal and receipt core under all four commits.
- **The sealing path's code** (canon, syntax, sema, seal, front) is the same through every revision but that one change
  to sema at fc19339 (`evidence/seal-audit.txt`, from `tests/corpus_seals.py`).

## Plants (`selftest`)

| plant | the defect | its witness |
|---|---|---|
| reserve-tick | a word newly reserved that fall.orl names its loop variable with | fall.orl now refused SYNTAX at line 15 |
| law-line-format | one law line respelled, `(decimals` as `(decimal` | of 142 accepted texts, 141 law seals move, and the one sealed text (E13b) is refused SEAL-MISMATCH |
| say-counts-twice | the reference counts one more operation per Say | 0 law seals move; 99 receipt cores do |
| frozen-text-altered | a byte appended to one frozen text | that text, and only it, reads INPUT CHANGED |

Two further rows: a control with no plant (every text the same), and a declared change, which passes only with its exact
new result.
