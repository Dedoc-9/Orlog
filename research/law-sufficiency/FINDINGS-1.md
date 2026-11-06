# LAW-SUFFICIENCY-1: findings (2026-10-30)

**Status.** These are the results of the four closure experiments [SHEET-1.md](SHEET-1.md) planned, within the scope
of the owner's paste of 2026-10-30. This report is not a ruling and authorizes nothing: no production integration, no
Rust implementation, no change to the gate or to released semantics. Every result is MEASURED on the texts and plants
named here, on one host. None is ESTABLISHED.

**Where it ran.** Here, on the Windows working copy, CPython 3.14.5, clang and rustc, at commit `2e9805a` plus the
research files. `src/`, `tests/` and `vectors/` are unchanged, which the runner checks. `closure_tests.py` ran twice,
and the two outputs were byte-identical. The evidence is [`evidence/law-sufficiency-1.txt`](../../evidence/law-sufficiency-1.txt),
with the code's and fixtures' sha256 in its header.

LAW-SUFFICIENCY-0's files and evidence are untouched. `decoder.py` is still sha256 `4f9a66b4…`. Its additions live in a
copy, `decoder1.py` (`3584f565…`).

## The answer

All four experiments held. Every prediction SHEET-1 fixed before the runs came out as written, and so did every plant.
With them, the law bytes of version 0 supply, on these texts:
- the reference interpreter, as LAW-SUFFICIENCY-0 found;
- the three backends: the Python, C99 and Rust programs generated from the decoded law are byte-identical to those
  generated from the parsed law, on every text, and each of them, built and run, agrees with the reference.

The rounded conversions, the order of a rule's definitions, and the fields only the backends read are now measured,
not assumed.

**The texts.** LAW-SUFFICIENCY-0's 290 distinct texts, unchanged, and eight fixtures in `fixtures/`: 298 in all. Seven
fixtures were written before any run. The eighth, `e3-inline-let.orl`, was added by SHEET-1's dated amendment after the
first run and before the evidence run (see "What changed between the runs").

## E1: the rounded conversion

The 290 texts hold no `rounded` conversion. The three E1 fixtures hold all six (target, source) paths: integer from
fixed and from float; fixed from integer and from float; float from integer and from fixed. They also hold one refusal:
an infinity rounded to an integer gives `REFUSED NOT-FINITE 1`.

| | result |
|---|---|
| decoded P against parsed P, by D and by D1 | equal on all three fixtures |
| round trip | exact on all three |
| rounded paths that D decoded | 6 of 6 |
| plant: D1 reads `rounded` as `as` | predicted `REFUSED INEXACT-CONVERSION 1`; got `REFUSED INEXACT-CONVERSION 1` |

So the gap LAW-SUFFICIENCY-0 reported (the `rounded` form never exercised) is closed for D, the decoder that report
used, as well as for D1.

## E2: the order of a rule's definitions

SPEC §6 says a use of a rule evaluates *"left to right, in clause order"*: every proviso first, then the remaining
values. A refusal names the clause of the use.

| fixture | predicted | parsed | decoded |
|---|---|---|---|
| `e2-provisos.orl` (the first proviso divides by zero, the second overflows) | `REFUSED DIVISION-BY-ZERO 3` | as predicted | as predicted |
| `e2-provisos-swapped.orl` | `REFUSED OVERFLOW 3` | as predicted | as predicted |
| `e2-values.orl` (both apply, neither overrides) | `REFUSED DIVISION-BY-ZERO 3` | as predicted | as predicted |
| `e2-values-swapped.orl` | `REFUSED OVERFLOW 3` | as predicted | as predicted |

Each swapped pair has two law seals: the written order is part of the law, and the law bytes write it.

**Plant:** `an.rules` reversed in the parsed path, with the law bytes fixed (verified).
- The parsed run became `REFUSED OVERFLOW 3`.
- The decoded run stayed `REFUSED DIVISION-BY-ZERO 3`.

This is the measured case test 3 lacked: there, the same reversal was equivalent on all 19 texts.

**What follows for the format.** The order a core evaluates a rule's definitions in is clause order, the order the law
bytes write. It decides which refusal a law ends in, so it belongs among the format's written obligations.

## E3: the backend-only derivations

D1 derives three fields from the law bytes:
- `an.vars`: every variable in id order;
- `an.rule_types`: each rule's first define's type;
- each variable's `top`: a let in a top-level clause outside any inline body; a for's counter never.

| check, on 298 texts | result |
|---|---|
| `an.vars` (each id, type and `top`) equal to the analysis's | 298 |
| `an.rule_types` equal | 298 |
| decoded P equal to parsed P | 298 |
| round trip exact | 298 |

**Plants:**
- `top` true for any let in a top-level clause, inline bodies included: differs on 1 text, the one text with a let in
  an inline body (`e3-inline-let.orl`). As predicted by the amendment.
- `top` always false: differs on 143 texts, exactly the texts with a top-level let. As predicted.

## E4: the backends on the decoded law

For each text, the three generators ran on `Lowered` of the parsed law and on `Lowered` of a shim holding D1's decoded
law. The shim carries:
- the sha256 of the law bytes as its law seal;
- the parsed text seal;
- `seal.seal_words` of the law seal.

| check, on 298 texts | python | c99 | rust |
|---|---|---|---|
| generated program byte-identical, parsed against decoded | 298 | 298 | 298 |
| decoded program built and run by the arbiter's `build` and `run`, its P equal to the reference's parsed P | 298 | 298 | 298 |

**Plant:** D1's `top` always false. The generated programs differ on 143 texts, exactly those with a top-level let. As
predicted.

## What changed between the runs

**The first run.** Its output is kept, git-ignored, in `work/law-sufficiency-arbiter/closure-run1.txt`. Every
prediction held. The plant for the inline clause of `top` was equivalent on all 297 texts, because none had a let in an
inline body, and the sheet allowed that outcome.

**What was found after it.** The grammar allows such a let: `§2 If x is 1, let y be 2; otherwise say 3.` compiles, and
`y` is not top. So that clause was untested, not vacuous.

**The amendment.** SHEET-1 gained a dated amendment that adds one fixture, with its prediction written before the
evidence run. Nothing else changed but the plant's expected count, which `closure_tests.py` now computes from the parsed
programs. The evidence run is the one after it.

## Failures and inconclusive results

**No experiment failed, and no plant missed.** What remains, said plainly:

1. **One value per path.** Each rounded path is exercised by one value, or two where both fixtures hold it, and one
   refusal is exercised in all. That shows D decodes the form. It does not survey rounding.
2. **E2 measures two refusal pairs** (two provisos, two values), not every way a rule's order could show.
3. **In E4, the backends are compared with the reference, not proven.**
   - The generated programs are byte-identical, so a decoded program and a parsed program are the same program.
   - The runs show that the decoded programs agree with the reference, as the self-test's four-way rows already show
     for the corpus.
4. **E4's second run built nothing new.** The arbiter found the first run's programs in its cache, and checks each
   cached program against its record (toolchain and sha256) before running it. The programs ran again.
5. **The shared dependencies, which these experiments do not attack:**
   - syntax.py's node classes, which D and D1 build;
   - the one interpreter both paths run on;
   - `seal.seal_words`, which the shim uses;
   - the lowering and the generators, which both paths pass through. Those are the code under test, not a second
     reading of it.
6. **One host, one toolchain.** E4's programs were built and run with this machine's clang and rustc only.

## Incidental findings

**The note in `examples/legal.orl` overstates.** It says *"The outcome never depends on the order the rules are written
in"*. For a rule's value that holds: two maximal definitions that disagree are refused, never settled by position. For
which refusal a law ends in, it does not hold. `e2-provisos.orl` and its swapped twin refuse differently, as SPEC §6's
clause order says they must (MEASURED).
- The note is in a committed example.
- SPEC §6 is what governs.
- The correction is the owner's to scope, beside LAW-SUFFICIENCY-0's finding about `sema.py:6`.

## What this does not show

- That the law bytes are sufficient beyond these 298 texts. This is MEASURED, not ESTABLISHED.
- That a Rust core would be correct.
- Version 1's law forms (ports, the tick block), which §15 must define before the pin.
- That Float is identical on another host (HOST-0).
- The prose printer of LAU-1.

## What closure brings back to the owner (proposals, each his to rule)

These are the decisions the paste listed for after closure:

1. **Accept `orlog-law 0` as version 0's machine-form contract.**
2. **Make its derivations and evaluation order written format obligations.** That covers the 15 run-side derivations,
   the three backend-only ones, and clause order for a rule's definitions.
3. **Authorize a separate milestone for an independent Rust core,** which reads the law bytes. Its own sheet would come
   first.
4. **Keep the Python interpreter as the reference authority** at first.
5. **Keep the prose printer as its own LAU-1 obligation.**

Version 1's path (draft 14, the version-1 reference, the containment test with P6's candidate grammar, the CUT-0 pin,
1a) goes on apart. Nothing here settles its law forms.

## How to run it

From the repository's root: `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/law-sufficiency/run_all_1.py`. It builds
in `work/law-sufficiency-arbiter/` (git-ignored). With an empty cache it takes several minutes here, since it builds
about 600 C99 and Rust programs; the second run reuses the cache.
