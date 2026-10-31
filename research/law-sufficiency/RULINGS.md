# The owner's rulings on LAW-SUFFICIENCY (in his words)

Recorded as he gave them, whole, on 2026-10-30, after [FINDINGS-1.md](FINDINGS-1.md). They govern the version-0
machine-form contract only. Earlier, on 2026-10-30, he accepted [SHEET.md](SHEET.md): *"Accepted. You may build the
three tests."*

## The five decisions after LAW-SUFFICIENCY-1 (2026-10-30)

> I rule yes on all five, with one important distinction: the evidence is sufficient to establish a version-0
> machine-form contract and authorize the next milestone, but it does not establish universal backend independence,
> cross-machine identity, or a completed Rust implementation.
>
> Five rulings
>
> 1. Contract — ACCEPTED, scoped to version 0.
> Accept `orlog-law 0` as the machine-form contract for version 0.
> The basis is stronger than the original LAW-SUFFICIENCY-0 result: LAW-SUFFICIENCY-1 closes the four identified gaps
> across 298 texts. The decoded representation reproduces the parsed interpreter's receipts, round-trips to identical
> law bytes, and supplies inputs from which the arbiter generates byte-identical Python, C99, and Rust programs.
> This acceptance is bounded by the tested corpus and environment. It is not a claim that every possible law, host,
> compiler, or runtime has been verified.
>
> 2. Format obligations — ACCEPTED.
> The format must make explicit obligations of:
>
> * Every execution-relevant derivation required by the interpreter and backends, including `Analysis.vars`,
>   `Analysis.rule_types`, and `VarInfo.top`.
> * The order of a rule's definitions, because that order can determine which refusal terminates execution.
> * Exact reconstruction from law bytes, including the round-trip requirement.
>
> The format must not leave these as accidental properties of the current Python analysis implementation. The measured
> order result also means the claim in `examples/legal.orl` that outcomes never depend on written rule order needs a
> separate correction proposal. Do not silently edit it as part of this ruling.
>
> 3. Rust core — AUTHORIZED AS A SEPARATE MILESTONE, SHEET FIRST.
> Authorize a Rust-core milestone with its own preregistered sheet, predictions, tests, and acceptance criteria.
> This authorizes the milestone's design and experimental planning, not immediate production implementation or
> integration. The sheet should specify the core's boundary, its inputs from `orlog-law 0`, its relationship to the
> arbiter, and the independent evidence required before it can replace or supplement any production path.
> No gate changes, release changes, or authority transfer follow from this authorization.
>
> 4. Reference authority — ACCEPTED.
> The Python interpreter remains the reference authority.
> The decoded-law tests establish that the law bytes can supply its execution inputs; they do not establish that the
> C99 or Rust backend should become an authority. Backend agreement remains evidence against the Python reference, not
> a vote that can overrule it.
>
> 5. Prose printer — ACCEPTED AS A SEPARATE LAU-1 OBLIGATION.
> Keep the prose printer separate from the machine-form contract.
> Its obligations remain byte-based:
>
> * LAU-1: printing a law and recompiling it yields the same law, seal for seal.
> * LAU-2: compiling, printing, and compiling again yields the same law as compiling once, allowing only omissions the
>   specification explicitly permits.
>
> LAW-SUFFICIENCY-1 does not discharge either obligation. It establishes the machine-form boundary, not canonical
> human-readable reconstruction.
>
> What this does not settle
> The findings still leave real limits:
>
> * One tested host and its clang/rustc toolchains.
> * Shared syntax node classes, interpreter, seal machinery, lowering, and generators.
> * Limited measured rounding cases and rule-order refusal pairs.
> * E4's second run used cached builds, with cache records checked before execution.
>
> Those are limitations to carry forward, not reasons to withhold the five decisions. In particular, byte-identical
> generated programs establish that the decoded law supplies the same backend inputs; they do not independently
> validate the shared generators.
>
> Boundary with version 1
> These rulings apply to the version-0 machine-form contract only. They do not freeze version 1's law representation,
> settle P6, or replace the existing version-1 critical path. That work continues independently.
>
> Disposition: LAW-SUFFICIENCY-1 is accepted as the evidence basis for the five decisions above. The next authorized
> work is the Rust-core milestone sheet, not core implementation. Keep the findings, original sheet, dated amendment,
> first-run output, and two-run evidence together and uncommitted unless separately authorized.

## What follows from them, as recorded

- **The next authorized work is the Rust-core milestone sheet, not the core.**
- **The format obligations are owed, as a written document.** It covers every derivation, the order of a rule's
  definitions, and exact reconstruction with the round trip. The decision is made; the document is not yet written.
- **Two correction proposals are owed, each separate and narrowly scoped:**
  - `examples/legal.orl`'s note on rule order, which he names (*"Do not silently edit it"*);
  - `src/orlog/sema.py:6`'s docstring, found by LAW-SUFFICIENCY-0.
- **These files stay together and uncommitted** unless he authorizes otherwise: the findings, the sheets, the dated
  amendment, the first run's output (`work/law-sufficiency-arbiter/closure-run1.txt`, git-ignored) and the two-run
  evidence.
