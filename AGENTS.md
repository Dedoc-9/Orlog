# AGENTS.md — working in Ørlǫg

Ørlǫg is a prose programming language in which a program is a numbered legal text. Each clause is one statement, and
the text spells a typed law. One law is held to byte-identical output on a reference interpreter and three backends:
Python, C99 and Rust. The door repairs, notes or refuses every byte that could read two ways. Every run writes a
receipt and a hash chain of its events. Claims made in a program are checked during the run, and a court reads each
claim's standing from the channel that supports it. Ørlǫg lives in its own repository and has no authority anywhere
else, Verðandi included.

This file is the brief for a coding agent: what to read, what never to touch, what to run, and how to write a claim.
It is plain Markdown in the [agents.md](https://agents.md/) format. A user's own instructions override it.

The rule under every rule: **integrity is not truth.** Ørlǫg computes integrity, and the truth of a claim's formal
condition in one run. It cannot compute whether a condition says what its author meant. `declared ≠ verified`.
`built ≠ adopted`. A claim's standing never exceeds its channel. Read the code, not the prose, and that includes this
file.

**Agreement is not grounding.** A green self-test, matching hashes, four executions agreeing, or the twin, the
runtimes and the prosecutors agreeing: all of these are integrity. They rule out disagreement, and nothing more.
Every verifier in this repository comes from one model family, so their agreement is consistency by construction.
Treat what a generator makes, your own work here included, as a well-made fiction until something outside the
program grounds it: a checked certificate, a cited result, or the owner's ratification. Disagreement is the signal.
Never smooth one away to make a run agree, and never count agreement as proof.

## 1. Where the truth is

- **What a run computes:** the reference interpreter (`src/orlog/interp.py`, with `src/orlog/numeric_ref.py` in exact
  rationals) is the authority, by declaration. That is not proven, and it is not a vote. The backends must match it
  byte for byte. A backend that disagrees is a dissent the arbiter localizes to its first divergent event.
- **What the language is:** `SPEC.md`, read with its amendments §11 (v0.1), §12 (v0.2) and §13 (v0.3), which govern the
  body where they differ, and `RUNTIME-SPEC.md`.
- **Where the specification and the code disagree,** that is a finding, and neither is presumed right. Settle it in
  writing, as §11–§13 do: "Code changed", or a reading settled with its reason.

| read | when |
|---|---|
| [`STATUS.md`](STATUS.md) | first: where the work stands and what is open |
| [`DOCTRINE.md`](DOCTRINE.md) | before any claim: each stage's theorem as the court narrowed it, the non-claims (§8), the owner's forks (§9) |
| [`SPEC.md`](SPEC.md) §13 | before touching the front end: every compile code's phase and the order within each phase |
| [`RUNTIME-SPEC.md`](RUNTIME-SPEC.md) | before touching a runtime, a generator, the receipt or the event chain |
| [`court/RECORD.md`](court/RECORD.md) | every finding against the design and its disposition |
| `rt_c/NOTES.md`, `rt_rs/NOTES.md`, `twin/NOTES.md` | each independent author's own record |

## 2. The map

| folder | what |
|---|---|
| `src/orlog/` | the door (`canon.py`), the clause tree and parser (`syntax.py`), types and the law (`sema.py`), seals and check syllables (`seal.py`), the reference (`interp.py`, `numeric_ref.py`), lowering and the three generators (`lower.py`, `gen_py.py`, `gen_c.py`, `gen_rs.py`, `rt_py.py`), the arbiter (`arbiter.py`), the court (`court.py`) |
| `rt_c/`, `rt_rs/` | the C99 and Rust runtimes, each written by a separate author who did not read the other's work, each held to the vectors |
| `vectors/` | `runtime-vectors.txt`, 20,015 lines generated from `numeric_ref.py` by `src/gen_vectors.py`: the contract every runtime meets |
| `tests/` | `selftest.py` (every self-claim a row, every guard a plant), `compare_probes.py`, `diff_twin.py` and `diff_worker.py`, `asan_c.py`, `fixtures/redteam/`, `fixtures/e21/` |
| `twin/` | the clean-room twin: a second interpreter written from the specification alone, its hand-worked probes, and `probes/settled.json` |
| `court/` | the prosecutions, the red team (`redteam-eng/`), the judge and its record |
| `examples/` | the corpus: Collatz, a certified gcd, leapfrog physics, chaos, defeasible law, the plankton parable, Aztec tilings, a falling body, three spellings of one law |
| `research/` | the literature behind the theorems; prior art is cited there |
| `evidence/` | recorded runs, tracked: the self-test twice, the probe comparison |
| `build/`, `work/` | generated output, ignored by git |

## 3. Never, without the owner's word

- **Edit the twin's hand-worked expectations** (`twin/probes*/expected.json`, `EXPECTED.md`). If a reading is settled
  against the twin, record it in `twin/probes/settled.json` with its reason and amendment.
- **Read the reference while acting as the twin.** A twin round is a separate author who reads only `SPEC.md`,
  `RUNTIME-SPEC.md`, `src/orlog/numeric_ref.py`, `src/orlog/seal.py` and `twin/`. One read of `src/` makes the twin
  worthless.
- **Edit the vectors to fit a runtime.** The vectors are generated. A change to `numeric_ref.py` regenerates them, and
  both runtimes are then run against them again.
- **Change the meaning of an existing law.** These are versioned, and a change is a new version, never a fix to
  existing seals:
  - the law's bytes (`law_bytes` in `sema.py`, header `orlog-law 0`);
  - the receipt (`orlog-receipt 0`);
  - the event chain (`orlog-trace-0`);
  - the claim seal (`orlog-claim-1`);
  - the numeric semantics.
- **Write a ratification or a theorem line to a ledger.** `orl.py ratify` and `ratify-theorem` are a person's act. A
  self-test fixture says so in its note.
- **Let a standing exceed its channel.** Computation and agreement never ground a claim, and grounding binds to the
  claim's own seal.
- **Relax a bound or a check to make something pass:** NESTING-DEPTH 24, LOOP-NESTING 16, EXPRESSION-DEPTH 24/64,
  the quote boundary, the strictness of the receipt, a self-test row, a plant.
- **Add a dependency.** Python is the standard library. C is C99, built by the system's clang with
  `-ffp-contract=off -fno-fast-math`. Rust is std-only, built by bare `rustc`. There is no pip, and there is no
  Cargo.
- **Rewrite the court record or a finding.** Records are appended. A record that was wrong is corrected in place,
  with a note saying so.
- **Claim** a timing, or determinism on a host, compiler or flag set nobody ran. "Here" means the host where the
  output was produced.
- **Commit or push.**

## 4. What to run, by what changed

Set `PYTHONHASHSEED=0` and `PYTHONUTF8=1` for every run, and use `python -B`.

| what changed | run | expect |
|---|---|---|
| anything | `python -B tests/selftest.py` (`--backends python` without compilers) | `ORLOG SELFTEST n/n`; read every FAIL line, and when a row fails, check first whether its expectation is stale |
| the door (`canon.py`) | the self-test, then `python -B court/redteam-eng/doorfuzz.py 60000 5` | `0 distinct minimal counterexamples` |
| the front end (`syntax.py`, `sema.py`, `front.py`) | the self-test; `python -B tests/compare_probes.py` and `python -B tests/compare_probes.py --dir probes3`; `python -B tests/diff_twin.py --n 3000 --seed 1` | the probes: 0 different (settled ones named); the differential run: every disagreement explained in `work/difftwin/report.md`. A new or removed compile code changes SPEC §13's table in the same change, and the self-test holds the table to the source |
| the numeric semantics (`numeric_ref.py`) | `python -B src/gen_vectors.py`, then both runtimes' vector checks below, then the self-test | `RUNTIME VECTORS 20015 / 20015` from each runtime at both optimization levels (or the new count, said) |
| the C runtime (`rt_c/`) | in `rt_c/`: `clang -std=c99 -pedantic -Wall -Wextra -O2 -ffp-contract=off -fno-fast-math test_rt.c -o test_rt.exe`, then `test_rt.exe ../vectors/runtime-vectors.txt`, then the same at `-O0`; then `python -B tests/asan_c.py` and `python -B tests/asan_c.py --plant`; then the self-test | `RUNTIME VECTORS 20015 / 20015` twice, outputs byte-identical; `ASAN C n/n clean`; `plant free-before-copy: CAUGHT`; the `memory` row flat and its plant caught. A text or list the runtime makes has one owner, a variable's slot or the temp stack (E21): never let a store free before it copies, and never add a maker of heap texts or lists that does not push onto the temp stack |
| the Rust runtime (`rt_rs/`) | in `rt_rs/`: `rustc --edition 2021 -O test_rt.rs -o test_rt.exe`, then `test_rt.exe ../vectors/runtime-vectors.txt`, then the same without `-O` | `RUNTIME VECTORS 20015 / 20015` twice |
| the event chain | `python -B src/check_chain.py` | the four heads each runtime's harness prints |
| a generator or `lower.py` | the self-test | the corpus four-way identical; codegen identical under two hash seeds; every backend plant caught |
| the arbiter | the self-test | the receipt rows (E7), the masking row (E8), the non-ASCII work folder (E11) |
| the court or its record | the self-test; `python -B court/build_record.py && python -B court/judge.py` | the court rows; `court/VERDICT.txt` recomputed, never typed |
| the specification | the self-test and the probes | the phase-table row; a settled reading recorded in `settled.json` |

Before believing a surprising result, rerun clean: delete the stale `build/` cache, and use `python -B`.

## 5. Environment

- Seen in use: Windows 11, CPython 3.14.5, clang 22.1.8, rustc 1.96.1. No version is pinned.
- Line endings are LF. Write planted files and stdin as binary, because text mode on Windows turns LF into CR LF and a
  law's seals are of exact bytes.
- Git Bash heredocs drop backslashes from Python sources. Write such files with an editor tool.
- A redirected stdout on Windows uses a legacy code page. Set `PYTHONUTF8=1`.

## 6. Writing a claim

- **Grade it:** MEASURED, ESTABLISHED, DECLARED, OBSERVED (seen once) or NOT_MEASURED. Give it a `does_not_show`
  boundary and a falsifier that can fail.
- **Read counts from the evidence files; never type them.** The self-test's last line is its summary.
- **Say where it happened, and stay inside the channel.** A program's claim stands no higher than its channel, and a
  doc's claim stands no higher than its check.
- **No scalar scorecards.** Report witnesses side by side.
- **Novelty needs a prior-art search, cited.** The court withdrew every unsearched claim of novelty.
- **Quote the owner's rulings in his words.**
- **A test asserts the apparatus.** Plant the defect and require the refusal. A plant that changes nothing is an
  equivalent mutant, declared as such and never counted as caught.

## 7. Lessons that cost something

- **A row written before a repair goes stale without a sound.** E16c expected SYNTAX after the repair made it
  PROCEDURE-PLACE, and the L12 input stopped reaching its case after E9. Rerun the self-test after every repair.
- **A false event is a defect, even under a true verdict.** E19's line logged a QUOTE-BOUNDARY that never happened,
  and E26 logged a note about a literal that did not exist.
- **A harness can manufacture agreement.** A zero law seal's words are `babab-babab-babab-babab`, so a text sealed with
  them looked accepted to the twin.
- **State a bound as it is measured.** §12 said "more than 24 nested parentheses"; the code refuses 24.
- **An unlisted code hides in a phase.** STATEMENT-PERIOD was raised but listed nowhere, until the table was held to
  the source.
- **An optimizer can fold a NaN test.** Decide NaN on the bits.
- **A compiler flag can miss its target.** FMA flags did not fuse Ørlǫg's generated C; an explicit `fma()` plant did.
- **A build cache serves the old build.** Twice a check picked a cached source by its law's seal words, and both
  times it got the wrong file. The FMA row counted a plant's FMA, and the red team's `memleak.py` reported the leak
  unchanged after its repair. Measure the build you just made, never one you find; clear the cache before believing
  a result that did not change.
- **A repair is only as wide as what it measured.** E21 named texts; the C runtime's author had also named lists
  (finding 8). The lists leaked until a measurement looked.
- **One model family wrote every independent part:** the twin, both runtimes, the prosecutors and the reference.
  Their agreement shows consistency, not truth.

## 8. Privacy

Record about a host only what its own output establishes. Do not write the owner's personal details or hardware into
the repository.
