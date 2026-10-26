# Ørlǫg

*Ørlǫg*, "primal law", is what the Norns laid down (Völuspá 20).

Ørlǫg is a prose programming language. A program is a numbered legal text: each clause is one statement, and the
text spells a typed law. One law compiles to Python, C99 and Rust, and the four executions (a reference
interpreter and the three backends) are held to byte-identical output and run receipts. Claims written in a program
are checked while it runs, and a court reports what each claim rests on.

> **The rule under every rule: integrity is not truth.** Ørlǫg can show that runs agree byte for byte, that a claim's
> condition held in a run, and what supports that claim. It cannot show that a condition says what its author meant:
> the intent is not in the text.

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
[`evidence/selftest-run.txt`](evidence/selftest-run.txt), reads `ORLOG SELFTEST 140/140  (backends: python,c99,rust)`.
Two consecutive runs gave byte-identical output ([`evidence/selftest-run2.txt`](evidence/selftest-run2.txt)).

| what | evidence |
|---|---|
| The corpus gives byte-identical outputs and receipts on the reference and on the Python, C99 and Rust backends. It is 11 programs, among them chaotic float orbits, fixed-point physics, a certified gcd, defeasible rules, Aztec tilings and three spellings of one law | `evidence/selftest-run.txt`, the `corpus` rows |
| The C99 and Rust runtimes each reproduce all 20,015 conformance vectors generated from the exact-rational reference. They were written by separate authors, each recording that it did not read the other's code | [`rt_c/NOTES.md`](rt_c/NOTES.md), [`rt_rs/NOTES.md`](rt_rs/NOTES.md) |
| Three spellings of one program (words, symbols, phrases) give three text seals and one law seal. A byte-mangled copy (BOM, CRLF, curly quotes, NBSP, ×) is repaired to the same law seal, each repair noted | the `spellings` rows |
| The door repairs typographic variants and notes each repair. It refuses bidi controls, confusable letters in code, ambiguous dashes and bytes that are not UTF-8, and it keeps text literals byte for byte. A second pass over repaired texts changes nothing. (That each repair rule preserves meaning is DECLARED, rule by rule) | the `door` rows |
| A defect planted in each backend is caught and located at its first divergent event. A defect planted in the reference reads REFERENCE-DISSENT | the `plant` rows |
| The specification is held to the code: its table of refusal codes equals the 43 the front end can raise, and a clean-room twin's 163 hand-worked probes are met (161 as worked, 2 as settled in SPEC §13) | the `spec` rows; [`evidence/probes-run.txt`](evidence/probes-run.txt) |

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
- **Memory in the C backend.** The C runtime never frees a text it builds (red team finding E21, MEASURED by the red
  team, not repaired). A long run that builds many texts can exhaust memory.
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
