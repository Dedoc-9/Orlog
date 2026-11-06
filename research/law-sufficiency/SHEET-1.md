# LAW-SUFFICIENCY-1: closing the gaps before any core. An experiment sheet (2026-10-30)

**Status.** An experiment plan, written and fixed before any of its runs. It is not a ruling. Its scope is the four
closure experiments in the owner's paste of 2026-10-30, which ended:

> *"My recommendation: authorize the four closure experiments, with no production integration, Rust implementation,
> gate changes, or semantic changes."*

It starts from `2e9805a` plus LAW-SUFFICIENCY-0's uncommitted files. It leaves those files and their evidence exactly as
they are: `decoder.py` is not edited, and the new derivations live in a copy, `decoder1.py`. It touches nothing in
`src/`, `tests/`, `vectors/`, the gate or version 1's path (draft 14, the version-1 reference, the containment test,
the CUT-0 pin, 1a), which goes on apart.

**The provisional conclusion it starts from (proposed for his record, not a ruling).** `orlog-law 0` is a measured
candidate execution boundary. Its bytes appear sufficient to reconstruct the reference interpreter's executable
representation across the tested corpus. A future independent core should be designed to consume law bytes rather
than prose or Python's analysis structures. That depends on these four experiments closing, and on a separate
architectural ruling.

**The texts.** LAW-SUFFICIENCY-0's 290 distinct accepted texts, unchanged, and seven new fixtures in `fixtures/`. The
fixtures were checked here only to compile, and to hold each conversion path they were written for. None was run
before this sheet. No variant is added: a fixture is added only for a path the 290 texts do not reach.

## The four experiments, each with its prediction fixed now

### E1: the rounded conversion

The 290 texts hold no `rounded` conversion. Three fixtures do:
- `e1-rounded-fixed.orl` holds each of the six (target, source) paths: integer from fixed and from float; fixed from
  integer and from float; float from integer and from fixed;
- `e1-rounded-floats.orl` holds the four reached from float literals;
- `e1-rounded-refuses.orl` holds an infinity rounded to an integer.

**Predicted.**
- On each fixture, the decoded P equals the parsed P, and the round trip is exact.
- The six paths each appear at least once in D's decoded trees.
- **Plant:** D made to read `rounded` as `as`. The decoded run of `e1-rounded-fixed.orl` refuses
  `INEXACT-CONVERSION 1`: `2.5 as an integer` is inexact where `2.5 rounded to an integer` is 2. The parsed run
  completes.

### E2: the order of a rule's definitions

SPEC §6: a use of a rule evaluates *"left to right, in clause order"*. Every proviso is evaluated first, then the
remaining values, and *"a refusal inside a rule names the clause of the statement that used the rule"*.

**Predicted on the parsed and the decoded run alike:**

| fixture | status |
|---|---|
| `e2-provisos.orl` (the first proviso divides by zero, the second overflows) | `REFUSED DIVISION-BY-ZERO 3` |
| `e2-provisos-swapped.orl` (the same two definitions, swapped) | `REFUSED OVERFLOW 3` |
| `e2-values.orl` (both apply, neither overrides; the first value divides by zero) | `REFUSED DIVISION-BY-ZERO 3` |
| `e2-values-swapped.orl` | `REFUSED OVERFLOW 3` |

**Predicted for the plant:** `an.rules` reversed in the parsed path of `e2-provisos.orl` and `e2-values.orl`, with the
law bytes fixed.
- The parsed status becomes `REFUSED OVERFLOW 3`.
- The decoded status stays `REFUSED DIVISION-BY-ZERO 3`.
- The law bytes do not move.

This is the measured case test 3 lacked: there, the reversal was equivalent on all 19 texts.

**Predicted for the two swapped fixtures:** they have different law seals and different refusals. This agrees with
SPEC §6. It shows that `examples/legal.orl`'s note, *"The outcome never depends on the order the rules are written
in"*, does not hold for which refusal a law ends in.

### E3: the backend-only derivations

`decoder1.py` is `decoder.py` with three fields added, each derived from the law bytes:
- `an.vars`: every variable in id order;
- `an.rule_types`: each rule's first define's type;
- `VarInfo.top`: a let in a top-level clause, outside any inline body; a for's counter never.

**Predicted.**
- On all 290 texts and the seven fixtures, D1's `an.vars` (each variable's id, type and `top`) and `an.rule_types`
  equal the analysis's.
- D1 still meets test 3: decoded P equal and the round trip exact.
- **Plant:** D1's `top` made true for any let in a top-level clause, inline bodies included. It differs from the
  analysis on every text with a let in an inline body of a top-level if, or it is equivalent on this set if no text
  has one. Measured, not assumed.
- **Plant:** D1's `top` always false. It differs on every text with a top-level let.

### E4: the backends on the decoded law

For every text and fixture, the Python, C99 and Rust generators are run on `Lowered` of the parsed law and of D1's
decoded law. The decoded law's `comp` is a shim: D1's program and analysis, the sha256 of the law bytes as its law
seal, the parsed text seal, and `seal.seal_words` of the law seal. Its seal-word function is a dependency the shim
shares.

**Predicted.**
- The three generated programs are byte-identical between the parsed and the decoded law, on every text.
- Each program built from the decoded law, run by the arbiter's own `build` and `run`, gives a receipt whose P equals
  the reference's parsed P.
- **Plant:** D1's `top` always false. The generated programs differ from the parsed law's on the texts with a
  top-level let.

### Amendment (2026-10-30, after the first run, before the evidence run)

**Why.** On the first run, every prediction above held. The plant that makes `top` true for a let in an inline body
was equivalent on all 297 texts, as the sheet allowed, because no text has such a let. The grammar does allow one:
`§2 If x is 1, let y be 2; otherwise say 3.` compiles, and the analysis makes `y` not top. So the inline clause of the
`top` derivation was untested, not vacuous.

**The fix.** One fixture is added, `e3-inline-let.orl`, holding that clause. Nothing else changes: no prediction above,
no other fixture, no code but the plant's expected count.

**Predicted for it.**
- D1's `an.vars` equals the analysis's: `y` not top.
- The plant `top-includes-inline` now differs from the analysis on exactly the texts that have a let in an inline
  body of a top-level clause: this fixture alone, one text.
- E4 builds and runs it with the rest.

The first run's output is kept in `work/law-sufficiency-arbiter/closure-run1.txt` (git-ignored). The evidence run is
the one after this amendment.

## What would count against

| outcome | means |
|---|---|
| any E1 to E4 prediction above fails | the boundary is not closed there; that failure is reported first, investigated, and not rerun away |
| a plant does not come out as stated | the experiment that holds it shows nothing until that is understood |
| E2's swapped fixtures refuse alike | SPEC §6's clause order is not what the run does |

## What closure would not show

- That a Rust core is correct.
- Version 1's law forms.
- Float identity on another host.
- That the backends are correct. E4 compares them with the reference, as the self-test's four-way rows already do on
  the corpus.
- That the law bytes are sufficient beyond these texts. The result is MEASURED, never ESTABLISHED.

## What closure would bring back to the owner

These are the decisions the paste listed:
- `orlog-law 0` as the version-0 machine-form contract;
- its derivations and evaluation order as written format obligations;
- a separate milestone for an independent Rust core;
- Python kept as the reference;
- the prose printer kept as its own LAU-1 obligation.

Each is his to rule. None follows from this sheet.
