# Ørlǫg

*Ørlǫg*, "primal law", is what the Norns laid down (Völuspá 20).

Ørlǫg is a prose programming language. A program is a numbered legal text: each clause is one statement, and the
text spells a typed law. One law compiles to Python, C99 and Rust, and the four executions (a reference
interpreter and the three backends) are held to byte-identical output and run receipts. Claims written in a program
are checked while it runs, and a court reports what each claim rests on.

> **The rule under every rule: integrity is not truth.** Ørlǫg can show that runs agree byte for byte, that a claim's
> condition held in a run, and what supports that claim. It cannot show that a condition says what its author meant:
> the intent is not in the text.

## A green build is a statement about the build

The checks that make a system look healthy compare it with itself: tests with their expectations, backends with each
other, hashes with hashes, replays with recordings. Every one of them can pass while the system rests on nothing.
A generator can produce an open world, an asset pipeline or a codebase in which every check is green and every
subsystem confirms its neighbour, and the whole can still stand on an invariant nobody ever grounded. A generator is a
consistency machine, not a truth machine. Until something outside it grounds its output, treat that output as a
well-made fiction. (This is the oracle problem: [DOCTRINE.md](DOCTRINE.md) §0 and §1 T0.)

Ørlǫg is built to keep these apart in the language itself, and it never lets one stand in for another:
- **Integrity: do the four executions agree, byte for byte?** Ørlǫg computes this. Agreement can only ever rule out
  disagreement.
- **Formal truth: did each written condition hold in this run?** Ørlǫg computes this. It says nothing about whether
  the condition was the right one to write.
- **Standing: what does a claim rest on?** The program's own computation, a checked certificate, a cited theorem, or
  a person's ratification recorded outside the program. Ørlǫg reports this, and a claim that rests only on the
  program's own computation can never be grounded, whoever signs it.

[The Plankton example](#the-paradox-it-was-built-around) is the trap at its smallest. Three claims, all true, all
agreeing on every backend, each resting only on the next: every integrity check is green. The court reports all
three CIRCULAR and names the cycle.

**Ørlǫg turns the same suspicion on itself.**
- **Its guards are tested by breaking them.** For each guard, the self-test plants the defect that guard exists to
  catch, and requires the catch: a C remainder that truncates, a Rust fixed-point multiply that floors, a reference
  that truncates its quotient, temporaries the C runtime never releases.
- **Its own verifiers are not independent.** The clean-room twin, both runtimes, the prosecutors and the reference
  were all written by one model family. Their agreement shows consistency, not truth; that is the paradox this
  language was built around, applied to this repository first. What such verifiers can do is disagree. In three
  rounds, the twin's hand-worked probes found defects in the reference and readings the specification had left
  open (SPEC §11, §13, §14). Each disagreement is settled in writing, and no agreement is ever counted as proof.
- **Its author's intent is not consulted.** Ørlǫg judges only what is written. What its author meant is not in the
  text, so it is never checked and never assumed.

**How to read this README.** Nothing here is claimed beyond what is shown, unless marked otherwise. A statement about
behaviour names the evidence file that records it. Anything else carries a grade: **MEASURED** (seen in a recorded
run, on one host), **DECLARED** (a design commitment, not proven), **NOT_MEASURED**, or **SPECULATIVE**. "Here"
means one Windows 11 host with clang 22.1.8, rustc 1.96.1 and CPython 3.14.5.

## A program

[`examples/collatz.orl`](examples/collatz.orl):

```
Title: The Collatz Witness.
Note: The orbit of 27 under the Collatz map, and a claim about its length whose oracle is cited, not ratified.
§1 Let n be 27.
§2 Let steps be 0.
§3 Let peak be n.
§4 While n is not 1, at most 1000 times, do the following.
§4.1 If n is even, set n to n divided by 2; otherwise set n to 3 times n plus 1.
§4.2 Increase steps by 1.
§4.3 Set peak to the larger of peak and n.
§5 Say "steps: " followed by steps followed by ", peak: " followed by peak.
§6 We claim that steps equals 111, by the theorem "OEIS A006577: the stopping time of 27 is 111".
§7 It must hold that peak is at least 27.
```

- Every loop is bounded: a While states its bound, and a For its range.
- `It must hold that` stops the run if it fails.
- `We claim that` makes a claim and names its oracle. Here the oracle is a cited theorem: cited, not ratified, so
  the claim is not grounded.

Run on all four executions, here:

```
$ python -B orl.py run examples/collatz.orl --backends python,c99,rust
collatz            law barap-futug-zojul-vuzup  ref COMPLETED  agree [c99,python,rust]  dissent [] NONE
```

`barap-futug-zojul-vuzup` is the law's seal in words: the first 64 bits of the sha256 of its typed law.

## The paradox it was built around

A verifier that shares the generator's priors inherits its blind spots. A verifier fully independent of the
generator costs as much as generating again. [`examples/plankton.orl`](examples/plankton.orl) is that parable as a
program. Three claims each evaluate true, every backend agrees, and each rests only on the next:

```
§3 We claim that plan equals robot, by computation, given §4.
§4 We claim that robot equals 7, by computation, given §5.
§5 We claim that plan is positive, by computation, given §3.
§6 We claim that plan times robot equals 49, by the theorem "the multiplication table: 7 times 7 is 49".
```

The court's reading, here (`python -B orl.py court examples/plankton.orl`, first block):

```
§3  We claim that plan equals robot, by computation, given §4.
    channel       computation
    integrity     AGREED
    evaluation    true in 1 of 1 evaluations
    ratification  not admissible for this channel (R2, R3)
    external_bits none beyond the text
    support       CIRCULAR (in gfp, not in lfp)
    cycle         §3 -> §4 -> §5 -> §3
    grounding     UNGROUNDED
```

The court computes support as a fixed point:
- A claim supported in the least fixed point is WELL-FOUNDED.
- A claim only in the greatest is CIRCULAR, and the court names its cycle. This is Fitting's Kripke–Kleene reading
  of a Horn program: prior art, cited in [DOCTRINE.md](DOCTRINE.md) §1 T4.
- A claim resting on the program's own computation can never be grounded, whoever ratifies it.

Ørlǫg does not solve the paradox, and nothing could. It keeps integrity, a run's formal truth, and outside
ratification apart, and it never reports a standing higher than the channel behind it.

## What is shown, and where

All of the following is MEASURED here, on 2026-10-25. The self-test's recorded summary, in
[`evidence/selftest-run.txt`](evidence/selftest-run.txt), reads `ORLOG SELFTEST 147/147  (backends: python,c99,rust)`.
Two consecutive runs gave byte-identical output ([`evidence/selftest-run2.txt`](evidence/selftest-run2.txt)).

| what | evidence |
|---|---|
| The corpus gives byte-identical outputs and receipts on the reference and on the Python, C99 and Rust backends. It is 11 programs, among them chaotic float orbits, fixed-point physics, a certified gcd, defeasible rules, Aztec tilings and three spellings of one law | `evidence/selftest-run.txt`, the `corpus` rows |
| The C99 and Rust runtimes each reproduce all 20,015 conformance vectors generated from the exact-rational reference. They were written by separate authors, each recording that it did not read the other's code | [`rt_c/NOTES.md`](rt_c/NOTES.md), [`rt_rs/NOTES.md`](rt_rs/NOTES.md) |
| Three spellings of one program (words, symbols, phrases) give three text seals and one law seal. A byte-mangled copy (BOM, CRLF, curly quotes, NBSP, ×) is repaired to the same law seal, each repair noted | the `spellings` rows |
| The door repairs typographic variants and notes each repair. It refuses bidi controls, confusable letters in code, ambiguous dashes and bytes that are not UTF-8, and it keeps text literals byte for byte. A second pass over repaired texts changes nothing. (That each repair rule preserves meaning is DECLARED, rule by rule) | the `door` rows |
| A defect planted in each backend is caught and located at its first divergent event. A defect planted in the reference reads REFERENCE-DISSENT | the `plant` rows |
| The specification is held to the code. Its table of refusal codes equals the 43 the front end can raise. The clean-room twin's hand-worked probes are met: 163 from its second round (161 as worked, 2 as settled in SPEC §13) and 128 from its third (125 as worked, 3 as settled in SPEC §14) | the `spec` rows; [`evidence/probes-run.txt`](evidence/probes-run.txt), [`evidence/probes3-run.txt`](evidence/probes3-run.txt) |
| On 20,221 mutated programs, the reference and the twin refuse with the same code or run byte-identically, every time. With the third round's probes added as seeds, every disagreement found is one of the three readings settled against the twin in SPEC §14 | [`evidence/difftwin-seed1.txt`](evidence/difftwin-seed1.txt), [`evidence/difftwin-seed2.txt`](evidence/difftwin-seed2.txt) |
| The C backend's memory stays flat however many texts and lists a run makes. A 16 MiB text rebuilt 5, 20 and 40 times peaks at 58 MiB each time; before red team finding E21 was repaired it peaked at 130, 370 and 691 MiB. A 2,000,000-item list stored 4 and 32 times peaks at 46 MiB both times, where it had peaked at 77 and 505 MiB | [`evidence/e21-memleak-before.txt`](evidence/e21-memleak-before.txt), [`e21-memleak-after.txt`](evidence/e21-memleak-after.txt), [`e21-lists-before.txt`](evidence/e21-lists-before.txt), [`e21-lists-after.txt`](evidence/e21-lists-after.txt); the `memory` row |
| The C backend runs clean under AddressSanitizer on 29 programs, and a store planted to free before it copies is caught | [`evidence/e21-asan.txt`](evidence/e21-asan.txt), [`e21-asan-plant.txt`](evidence/e21-asan-plant.txt) |

Each `plant` row plants a defect and requires the self-test to catch it, so that guard is shown to bite, not merely
to pass.

## What is not claimed

- **Truth or intent.** Integrity is not truth.
- **Any other host.** Identity on another machine, operating system, compiler version or flag set is NOT_MEASURED.
- **The reference's correctness.** The reference interpreter is the authority by declaration (DECLARED). The
  backends are held to it, and nothing holds it to the world.
- **Independence.** The twin, both runtimes, the prosecutors and the reference were all written by one model family.
  Their agreement shows consistency, not truth.
- **Time, speed, security.** NOT_MEASURED.
- **Memory beyond what is measured.** The bound on the C backend's text and list memory comes from the program, not
  from how long it runs (shown above), and it is DECLARED in general. The stack, the code and the host's allocator are
  outside it.
- **Novelty.** The mechanisms are prior art: certifying algorithms and the LCF discipline, Fitting's semantics,
  Dung's argumentation, IEEE 754 and more. Whether the combination is new is SPECULATIVE. The graded case, with its
  prior-art search, is in [DOCTRINE.md](DOCTRINE.md) §6.

The full list is [DOCTRINE.md](DOCTRINE.md) §8.

## Run it

Python 3, standard library only. clang (C99) and rustc build the C and Rust backends; `--backends python` runs
without them. Set `PYTHONHASHSEED=0` for every run, and `PYTHONUTF8=1` on Windows.

```bash
python -B tests/selftest.py
```

```bash
python -B orl.py run examples/collatz.orl --backends python,c99,rust
```

```bash
python -B orl.py court examples/plankton.orl
```

## Read next

- [AGENTS.md](AGENTS.md): the working brief (what to read, never touch, run, and how to write a claim).
- [STATUS.md](STATUS.md): where the work stands.
- [DOCTRINE.md](DOCTRINE.md): each stage's theorem, as an adversarial court narrowed it.
- [SPEC.md](SPEC.md) and [RUNTIME-SPEC.md](RUNTIME-SPEC.md): the language, read with its amendments (§11–§13).
- [court/RECORD.md](court/RECORD.md): every finding against the design, and its disposition.

**Status.** Research. It is not admitted to or registered in any other system, and its specification is DECLARED.
It continues a line of earlier work:
[executable-epistemics](https://github.com/Dedoc-9/executable-epistemics) →
[Dentatus](https://github.com/Dedoc-9/Dentatus) → [Ursprung](https://github.com/Dedoc-9/Ursprung) → Urðr →
Verðandi → Ørlǫg.

## License

GNU Affero General Public License v3: [LICENSE](LICENSE).
