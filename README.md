<!-- SPDX-License-Identifier: AGPL-3.0-only -->
# Ørlǫg

*Ørlǫg*, "primal law", is what the Norns laid down (Völuspá 20).

Ørlǫg is a prose programming language. A program is a numbered legal text: each clause is one statement, and the
text spells a typed law. One law compiles to Python, C99 and Rust, and the four executions (a reference
interpreter and the three backends) are held to byte-identical output and byte-identical run receipts (compared
without the line that names the backend). Claims written in a program are checked while it runs, and a court reports
what each claim rests on.

> **The rule under every rule: integrity is not truth.** Ørlǫg can show that runs agree byte for byte, that a claim's
> condition held in a run, and what supports that claim. It cannot show that a condition says what its author meant:
> the intent is not in the text.

**Author:** Daniel J. Dillberg · **Contact:** [bigdilly95@gmail.com](mailto:bigdilly95@gmail.com)
**License:** [AGPL-3.0-only](LICENSE)

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
- **Its guards are tested by breaking them.** Where a guard could pass by accident, the self-test plants the defect
  that guard exists to catch and requires the catch: a C remainder that truncates, a Rust fixed-point multiply that
  floors, a reference that truncates its quotient, temporaries the C runtime never releases, a ledger read past a torn
  line. Other guards are held by rows alone.
- **Its own agreement is tested too.** A defect planted in the lowering, which the three backends share, moves all
  three together, and only the reference catches it. A defect planted in the front end, which all four executions
  share, slips past every one of them; only the clean-room twin, whose front end is its own, sees it. The self-test
  keeps both results as rows, so that nobody later reads four-way agreement as more than it is
  ([what agreement measures](#what-agreement-measures)).
- **Its own verifiers are not independent.** The clean-room twin, both runtimes, the prosecutors and the reference
  were all written by one model family. Their agreement shows consistency, not truth; that is the paradox this
  language was built around, applied to this repository first. What such verifiers can do is disagree. In three
  rounds (notes on 23 programs, then 163 and 128 hand-worked probes), the twin found defects in the reference and
  readings the specification had left open (SPEC §11, §13, §14). Each disagreement is settled in writing, and no
  agreement is ever counted as proof.
- **Its author's intent is not consulted.** Ørlǫg judges only what is written. What its author meant is not in the
  text, so it is never checked and never assumed.

**How to read this README.** Nothing here is claimed beyond what is shown, unless marked otherwise. A statement about
behaviour names the evidence file that records it. Anything else carries a grade, as AGENTS.md §6 defines them:
**MEASURED** (seen in a recorded run, on one host), **OBSERVED** (seen once, not recorded), **ESTABLISHED** (a cited
result), **DECLARED** (a design commitment, not proven), **NOT_MEASURED**, or **SPECULATIVE**. Each row's boundary is
under "What is not claimed"; its falsifier is its evidence, run again. "Here" means one Windows 11 host with clang
22.1.8, rustc 1.96.1 and CPython 3.14.5.

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
- A claim only in the greatest is CIRCULAR, and the court names the cycle when the claim lies on one. This is
  Fitting's Kripke–Kleene reading of a Horn program: prior art, cited in [DOCTRINE.md](DOCTRINE.md) §1 T4.
- A claim resting on the program's own computation can never be grounded, whoever ratifies it.

Ørlǫg does not solve the paradox. It keeps integrity, a run's formal truth, and outside ratification apart, and it
never reports a standing higher than the channel behind it.

## What agreement measures

Agreement measures what the agreeing executions do not share. A defect in a layer they share moves them together, and
their agreement then measures the sharing. Each row is bound to the evidence that records it; a row that says nothing
checks a layer states an absence, which no run can measure, so it is DECLARED.

| layer | shared by | what four-way agreement shows there | what does check it | evidence |
|---|---|---|---|---|
| the front end: door, parser, type checker, law bytes | all four executions | **nothing.** A defect planted there (every `plus` read as `minus`) slips past all four, which agree | the clean-room twin, whose front end is its own; claims whose certificates refuse a wrong result | the self-test's `independence (MONITORED NEGATIVE …)` row, kept on purpose: the day the front end gains real diversity, it must flip to expect detection |
| lowering and the three generators | the three backends | **real evidence.** A defect planted there moves all three together against the reference: REFERENCE-DISSENT | the reference, which never lowers. Trust moves to the reference here, it is not spread | the `independence: … shared lowering` row |
| arithmetic | one definition, written as separate code. In the reference, Fix is exact rational arithmetic, and Float is the host's binary64 arithmetic (`+ − × ÷` and `math.sqrt`, then the NaN made canonical); the runtimes use bit-level code | **method diversity** for Fix. For Float, the reference and the runtimes compute on one host's floating-point hardware, so their agreement there is not an independent derivation. And the reference generated all 20,015 vectors, so alone they define the arithmetic rather than check it | since 2026-10-25, a second derivation that never imports the reference and holds no float (`tests/numeric_oracle.py`, exact rationals only). It reproduces all 9,913 Float lines of the vectors with no difference, among the 20,006 lines it derives (MEASURED on one host). With it come 113 hand-worked cases and two published SHA-256 digests, and three planted mistakes that the reference and its vectors would share are caught. It does not show identity on another host, nor that a runtime checks its floating-point state (flush-to-zero, rounding mode) when it runs: neither is shown | [`evidence/vectors-independent.txt`](evidence/vectors-independent.txt); the `independence: … runtime vectors` row |
| the comparison itself (the arbiter) | everything | **not diversified.** It has produced a false agreement (a lenient receipt check), dissents that were failed builds, and false dissents when runs shared a work folder, all repaired | its own rows and plants | [`evidence/race-after.txt`](evidence/race-after.txt); the arbiter rows |
| the specification and the authors | everything | **nothing.** One model family wrote every part from one SPEC.md | nothing in this repository (DECLARED, an absence) | Knight & Leveson (1986): independently written versions fail together where a shared specification was misread |

The twin is independent of the reference's code path, not of the specification or its author: it reads the same
SPEC.md and imports the reference's arithmetic and seals. Its agreement shows code-path independence and nothing more.
The full table is [DOCTRINE.md](DOCTRINE.md) §1 T11.

## Where the ground ends

Non-circular is not as far as the court goes. A claim is GROUNDED only when it rests on a channel that can carry outside
information (a certificate, a theorem or the owner), a person has ratified its own seal in a ledger the program cannot
write, and every claim it is declared to rest on is grounded too. A finite, acyclic tree that bottoms out in the
program's own computation or an unratified citation reads WELL-FOUNDED but UNGROUNDED: it rests on nothing, and the
court says so.

That answers Agrippa's trilemma the only way a closed program can: no regress (claims are finite), circles flagged, and
the stopping point made explicit and signed. The trusted base is therefore social, not mechanical, and the
trustworthiness of Ørlǫg's ground is not auditable by reading code. Its limits, in the order they matter: terminals are
untyped (a checked certificate, a cited theorem and testimony all need the same ratification); there is no inference
step (every node needs its own signature, which invites rubber-stamping); and only declared support is seen, so until
a backward slice lands, GROUNDED is a claim about the declared graph, not the real one. [DOCTRINE.md](DOCTRINE.md) §1
T12 gives each limit with its remedy.

## What is shown, and where

All of the following is MEASURED here, on 2026-10-25. The self-test's recorded summary, in
[`evidence/selftest-run.txt`](evidence/selftest-run.txt), reads `ORLOG SELFTEST 210/210  (backends: python,c99,rust)`.
Two consecutive runs gave byte-identical output ([`evidence/selftest-run2.txt`](evidence/selftest-run2.txt)). With
`--backends python` and no compiler, it reads `194/194` ([`evidence/selftest-python-only.txt`](evidence/selftest-python-only.txt)).

| what | evidence |
|---|---|
| The corpus gives byte-identical outputs and receipts on the reference and on the Python, C99 and Rust backends. It is 11 programs, among them chaotic float orbits, fixed-point physics, a certified gcd, defeasible rules, Aztec tilings and three spellings of one law | `evidence/selftest-run.txt`, the `corpus` rows |
| The C99 and Rust runtimes each reproduce all 20,015 conformance vectors generated from the reference (which computes Fix in exact rationals and Float in the host's binary64 arithmetic), at two optimization levels each, with byte-identical output. They were written by separate authors of one model family, each recording that it did not read the other's code. The vectors themselves agree with a second derivation that never imports the reference, and with 113 hand-worked cases | [`evidence/rt_c-vectors-O2.txt`](evidence/rt_c-vectors-O2.txt), [`-O0`](evidence/rt_c-vectors-O0.txt), [`evidence/rt_rs-vectors-O.txt`](evidence/rt_rs-vectors-O.txt), [`-O0`](evidence/rt_rs-vectors-O0.txt), [`evidence/vectors-independent.txt`](evidence/vectors-independent.txt); [`rt_c/NOTES.md`](rt_c/NOTES.md), [`rt_rs/NOTES.md`](rt_rs/NOTES.md) |
| Three spellings of one program (words, symbols, phrases) give three text seals and one law seal. A byte-mangled copy (BOM, CRLF, curly quotes, NBSP, ×) is repaired to the same law seal, each repair noted | the `spellings` rows |
| The door repairs typographic variants and notes each repair. It refuses bidi controls, confusable letters in code, ambiguous dashes and bytes that are not UTF-8, and it keeps text literals byte for byte. A second pass over repaired texts changes nothing. (That each repair rule preserves meaning is DECLARED, rule by rule) | the `door` rows |
| A defect planted in each backend is caught and located at its first divergent event. A defect planted in the reference reads REFERENCE-DISSENT when two or more backends run | the `plant` rows |
| A later version cannot quietly change what an old text means. 3,361 texts are frozen with their results at commit b4eaf11: every version of every corpus program, the twin's probes, the fixtures and 3,000 mutants. Each must give the same law seal, text seal and reference receipt, or the same refusal, unless the change is declared with its amendment. Every corpus version has the same law seal, text seal and receipt under all four pushed commits. What this gate does not protect (timings, memory, the arbiter, the backends) is listed in [`tests/compat/README.md`](tests/compat/README.md) | [`evidence/compat-check.txt`](evidence/compat-check.txt), [`evidence/compat-history.txt`](evidence/compat-history.txt), [`evidence/seal-audit.txt`](evidence/seal-audit.txt); the `compat` rows |
| A run that does not finish says so. A backend that did not build is counted neither agreeing nor dissenting, and every claim reads INCOMPLETE. A run past the host's budget of counted operations is STOPPED-BY-HOST at the same operation every time, with no receipt and no refusal. A ledger torn in mid-line is refused whole, LEDGER-BROKEN at its line. A claim whose own evaluation refused partway is named and not held (the court's R8, repaired 2026-10-26: before it, such a claim read GROUNDED over a run refused at it) | the `arbiter`, `host budget`, `ledger` and `court R8` rows; [`evidence/court-r8.txt`](evidence/court-r8.txt) |
| Parts of the specification are held to the code. Its table of refusal codes equals the set of 43 the front end can raise (the set, not each code's phase or order). The clean-room twin's hand-worked probes are met: 163 from its second round (161 as worked, 2 as settled in SPEC §13) and 128 from its third (125 as worked, 3 as settled in SPEC §14) | the `spec` rows; [`evidence/probes-run.txt`](evidence/probes-run.txt), [`evidence/probes3-run.txt`](evidence/probes3-run.txt) |
| On 20,221 programs (221 seeds and 20,000 mutants), the reference and the twin refuse with the same code or run byte-identically, every time. With the round-3 probes and the E21 fixtures added as seeds (20,353 programs), 47 of 48 disagreements are the three readings settled against the twin in SPEC §14; the 48th timed out and, run again without a limit, gave byte-identical receipts | [`evidence/difftwin-seed1.txt`](evidence/difftwin-seed1.txt), [`evidence/difftwin-seed2.txt`](evidence/difftwin-seed2.txt), [`evidence/difftwin-seed2-timeout.txt`](evidence/difftwin-seed2-timeout.txt) |
| On two programs, the C backend's memory did not grow with the run. A 16 MiB text rebuilt 5, 20 and 40 times peaks at 58 MiB each time; before red team finding E21 was repaired it peaked at 130, 370 and 691 MiB. A 2,000,000-item list stored 4 and 32 times peaks at 46 MiB both times, where it had peaked at 77 and 505 MiB. (The `memory` row measures smaller versions of both. Flat in general is DECLARED: see below) | [`evidence/e21-memleak-before.txt`](evidence/e21-memleak-before.txt), [`e21-memleak-after.txt`](evidence/e21-memleak-after.txt), [`e21-lists-before.txt`](evidence/e21-lists-before.txt), [`e21-lists-after.txt`](evidence/e21-lists-after.txt), [`e21-lists-rerun.txt`](evidence/e21-lists-rerun.txt) |
| The C backend runs clean under AddressSanitizer on 29 programs, and a store planted to free before it copies is caught | [`evidence/e21-asan.txt`](evidence/e21-asan.txt), [`e21-asan-plant.txt`](evidence/e21-asan-plant.txt) |

Each `plant` row plants a defect and requires the self-test to catch it, so that guard is shown to bite, not merely
to pass. One plant is declared equivalent (a rewrite that changes nothing), and is never counted as caught.

**Since then (2026-10-27).** The push 95dac79..9de2792 added the open run's research records and their evidence, and
changed no code: `src/`, `tests/`, `twin/`, `rt_c/`, `rt_rs/`, `vectors/`, `examples/` and `orl.py` are as they were
at 95dac79. Before its commits, the gate ran on its exact tree (`7a766f5e632564b06841ba5b8bf52c9ed6b7ee02`):
COMPAT-0 HELD over 3,361 texts and `ORLOG SELFTEST 210/210`, MEASURED here and recorded in the message of commit
9de2792, which names that tree on its `Gated-Tree:` line. No file of the tree holds that run.

## What is not claimed

- **Truth or intent.** Integrity is not truth.
- **Any other host.** Identity on another machine, operating system, compiler version or flag set is NOT_MEASURED.
- **The reference's correctness.** The reference interpreter is the authority by declaration (DECLARED). The
  backends are held to it, and nothing holds it to the world.
- **Independence.** The twin, both runtimes, the prosecutors and the reference were all written by one model family.
  Their agreement shows consistency, not truth. Four-way agreement does not test the front end, which all four
  executions share ([what agreement measures](#what-agreement-measures)).
- **That GROUNDED reaches the world.** It reaches a person's ratification of exact bytes, over the support the author
  declared ([where the ground ends](#where-the-ground-ends)).
- **Time, speed, security.** NOT_MEASURED. A host stop (STOPPED-BY-HOST) is a budget running out, not a verdict.
- **Memory beyond what is measured.** The bound on the C backend's text and list memory comes from the program, not
  from how long it runs (shown above), and it is DECLARED in general. The stack, the code and the host's allocator are
  outside it.
- **Novelty.** The mechanisms are prior art: certifying algorithms and the LCF discipline, Fitting's semantics,
  Dung's argumentation, IEEE 754 and more. Whether the combination is new is SPECULATIVE. The graded case, with its
  prior-art search, is in [DOCTRINE.md](DOCTRINE.md) §6.

The full list is [DOCTRINE.md](DOCTRINE.md) §8.

## Run it

Python 3, standard library only. clang (C99) and rustc build the C and Rust backends. `orl.py run`, `orl.py court`
and the self-test take `--backends python` and then need no compiler; a backend whose compiler is missing is reported
as not built, never as agreeing. Set `PYTHONHASHSEED=0` for every run, and `PYTHONUTF8=1` on Windows.

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
- [SPEC.md](SPEC.md) and [RUNTIME-SPEC.md](RUNTIME-SPEC.md): the language, read with its amendments (§11–§14).
- [court/RECORD.md](court/RECORD.md): the first court's findings against the design, and their disposition.
- [research/run-1/](research/run-1/): version 1, the open run (a law with a tick block or ports, inputs read once or each tick), as
  research.
  SPEC §15 is drafted there and is not yet part of SPEC.md: each draft is kept as it was, and the highest-numbered
  `SPEC-15-DRAFT-N.md` is current. The owner's rulings are in [RULINGS.md](research/run-1/RULINGS.md), in his words.
  `twin-r7/` holds R7's independent review of the drafts and its re-reads, each report saved word for word and each
  finding disposed. Nothing of §15 is built (DECLARED): no clause before its required re-read, and nothing of 1a
  before the read-once stop's containment check is done and CUT-0's digest is pinned.
- [research/roadmap-debate/VERDICT.md](research/roadmap-debate/VERDICT.md): the next steps, ranked by foundational
  value, after a debate between an architect, a use-case skeptic and a documentation prosecutor.
- [research/ragnarok/VERDICT.md](research/ragnarok/VERDICT.md): a proposed counterworld search, argued by a proponent
  and an adversary, with a prior-art survey.

**Status.** Research. It is not admitted to or registered in any other system, and its specification is DECLARED.
Version 1, the open run, exists only as drafts and rulings, and is not built.
It continues a line of earlier work:
[executable-epistemics](https://github.com/Dedoc-9/executable-epistemics) → Semiotic core →
[Dentatus](https://github.com/Dedoc-9/Dentatus) → [Ursprung](https://github.com/Dedoc-9/Ursprung) → Urðr →
Verðandi → Ørlǫg.

## License

[AGPL-3.0-only](LICENSE): the GNU Affero General Public License, version 3, and no later version.
