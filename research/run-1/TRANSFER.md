# Where the designs derived for RUN-1 could apply elsewhere (2026-10-26, research only)

The owner asked whether the designs derived in RUN-1's contract debate could apply elsewhere. This record names each
design, where it could apply, and what it would add or catch there.

Grades:
- **MEASURED:** a probe ran;
- **ESTABLISHED:** the code it would meet was read;
- **DECLARED:** argued only.

Nothing outside `research/` is changed. The owner's other repositories are being read by a lineage researcher, whose
section "Where Orlog's designs could apply" in `manifold/LINEAGE.md` extends this record.

## The designs

| # | design | where it was derived | what it is, in one line |
|---|---|---|---|
| 1 | the causal cut | `CUT-0.md` §2 | a stopped run's frames, and a continuation that over-approximates what it could still execute |
| 2 | fact against standing (E2) | `CUT-0.md` §1 | an evaluation's result is never withdrawn; reliance on the aggregate waits for completeness |
| 3 | the session as a transition system | `CUT-0.md` §3 | one δ over named events; illegal moves refused by name; nothing pending may disappear (END-PENDING) |
| 4 | the projection under a strict canonical grammar | `probes/cut0_session.py` | a derived record has one byte form or a named refusal, checked over every single-byte mutation |
| 5 | the two-layer binding | `CUT-0.md` §3 | one record attests the computation over its input; a second binds the provenance of that input |
| 6 | range before grid | the debate's D7, ledger T5 | a fixed-point door whose refusal always names two in-range neighbours, provided its bounds lie on the grid |
| 7 | monotonicity of withholding | ledger T8, `probes/t8_monotone.py` | a rule that only removes held items can never raise a fixed-point standing |
| 8 | static may-execute closure | Round D, Finding 18's repair | log-independence decided by what code could run from an input point, never by what a run happened to do |
| 9 | stand-ins one literal apart | `probes/cut0_claims.py` | a version-0 pair that differs in one literal measures what a version-1 port will vary |
| 10 | an instrumentation held to the original | `probes/cut0_claims.py` | a research subclass trusted only after it writes the same receipts and traces as the original over the whole corpus |

## Inside Orlog

| design | where | what it would add or catch | grade |
|---|---|---|---|
| 2, 1 | the court, version 0, today | E2 answers the reporting pass's open question for closed runs (a claim held in a run refused elsewhere) without waiting for RUN-1, by one rule rather than one per shape | MEASURED on version 0 (`probes/cut0_claims.py`: 95 claims, no frozen reading changed) |
| 7 | `tests/court_monotone.py` | with T8 proved, the one-sided measurements of R6, R8 and CUT-0 check the code against a theorem, not stand alone | proved by hand; MEASURED against the code |
| 4 | the door (`src/orlog/canon.py`) against the parser | the H2 split was found in the review by reading. A sweep finds only what its mutations can make: one-byte replacements, deletions and duplications cannot make an indented `Note:`, and that sweep over 145,089 mutants found nothing (MEASURED, first run). The door-aware sweep, which inserts and replaces one character of each class the door repairs or refuses, finds H2 in 33 of its 58,968 mutants. The first is an NBSP before `Note:`, E18's own route. Under the repair, run in memory, it finds nothing, and over COMPAT-0 the repair moves exactly one frozen verdict, E18's, which a reading of the raw bytes had missed. E18 and H2 are one defect (MEASURED) | `probes/door_canon_probe.py`, `evidence/run1-door-canon.txt` |
| 5 | the arbiter's receipt and the court's witness | H1's repair is design 5: the core stays the executions' agreement, and each execution's build identity goes in an envelope that follows the cached artifact | ESTABLISHED (`arbiter.py`, `receipt_core`; the H1 record) |
| 8 | the doppler verdict's dependence analysis (fork 4) | `Reach` is the first sound, static may-execute closure in the tree. A backward slice for R6's wider licence would extend it. T12's conjecture stays a conjecture, and nothing leans on it | DECLARED |
| 10 | any later probe that instruments the reference | the precedent: equality of receipts and traces over all runnable texts before a probe's reading is believed | MEASURED once (356 of 356) |

## In Verðandi (read from its AGENTS.md; its code is unchanged and was not run)

| design | where it would meet | what it would add or catch | grade |
|---|---|---|---|
| 4 | the graybox's input contract: `admit` in `graybox/web/sim.js` and `graybox/tick_ref.py`, with its cases in `input_cases.json` | `admit` already has a versioned contract and two validators. A sweep of every single-byte mutation of every case would check that the two agree on every neighbour of a case, not only on the cases | DECLARED |
| 4 | `tick_ref.py verify`'s door (VERIFY-DOOR-0), with its ordered refusal codes | its rules already say a malformed trace never ends in a traceback and is refused before the door. A mutation sweep is the systematic check of that rule, as P3 is here | DECLARED |
| 3 | the director's ledger (LEDGER-SAFE-0: `held_head`, `append_checked`) and the studio's transaction (`studio_txn.py`, which enumerates crash points) | an enumeration of legal event histories (evaluate, admit, approve, refuse, rebase) up to a depth, with design 3's rows: replay is a function of the ledger; no admission begun disappears; every event has one disposition. The crash-point enumeration covers failure, and this would cover legality | DECLARED |
| 5 | CERT-0, a certificate derived from the ledger and never the ledger from it | the same two-layer shape already stands there. It is a precedent for design 5, not a gap | ESTABLISHED (its AGENTS.md row) |
| 6 | the art file's number grammar (`art/dress.py`, NUMBER) and any fixed-point field | if a field refuses an off-grid value with its neighbours, range-before-grid keeps that message exact at the ends | DECLARED |

## From Verðandi into Orlog (the other direction)

| Verðandi's design | where it would meet Orlog | what it would add | grade |
|---|---|---|---|
| RUNG-0 (`tools/rung.py classify`: a change's rung from the trusted base's closure and the change's meaning) | a change to a normative rule, a format or a frozen file | the "contract-difference impact engine" the reviewer proposed: which proofs, fixtures and records a change touches, computed rather than remembered | DECLARED (Verðandi's AGENTS.md row) |
| rules 1's deterministic math layer (fdlibm written in correctly rounded operations, `math-fence`, a counterfactual last-bit engine) | a law that ever needs `sin`, `cos` or `atan2` | transcendentals built from T5's basic operations, so that they stay bitwise reproducible; never a platform libm (`FLOAT.md` F4) | MEASURED in Verðandi (R-6) |

## In the owner's other repositories

The lineage researcher's section of `manifold/LINEAGE.md` covers them, read from their code. Candidates named from
their descriptions alone (DECLARED until read):
- dvsm-meta-kernel's lockstep command buffering and S_ECHO hash finality, against design 3 (arrivals, assignment,
  closing) and design 5;
- the Q16, Q31 and Q64 fixed-point kernels (DQSDv2, Q64), against design 6;
- Dentatus's "nondeterminism captured at the boundary and replayed", against designs 3 and 4;
- executable-epistemics' forbidden interpretations, against the rule that no receipt line claims validity.

## What this record does not show

- That any transfer works there: every row but the measured ones is a hypothesis.
- Anything of Verðandi's code, which was not read or run here.
