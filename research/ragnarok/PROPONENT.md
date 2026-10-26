# Debate record: the proponent's design and probe, round 1 (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the adversary's prosecution and the
prior-art survey. Its probe is in `work/ragnarok-probe/` (ignored by git); its MEASURED lines are this host's. It
notes that the four tracked files edited while it worked (orl.py, arbiter.py, court.py, interp.py) were the judge's
uncommitted repairs of that evening; its processes imported the committed tree. Absolute paths that named the owner's home folder are given relative to the repository, or as the session's scratchpad (AGENTS.md section 8); nothing else is changed.

---

# Ragnarök, the Counterworld Court: the proponent's design and a feasibility probe

## Where things stand
- **The probe:** `work\ragnarok-probe\ragnarok.py`. It is git-ignored, standard library only, and imports `src/`.
  - It is 484 lines against the ~400 target; most of the excess is output formatting.
  - Its outputs sit beside it: `run1.txt` and `run2.txt` (a determinism pair), `run3.txt`, `run4.txt` (the final run, on a fresh build cache) and `door7.txt`.
- **How it ran:** every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` on this Windows 11 host (CPython 3.14.5, clang 22.1.8). Everything marked measured below is MEASURED here.
- **Tracked files:** I modified none.

**Two things you should know:**
1. **Someone else edited tracked files while I worked.** The files are `orl.py`, `src/orlog/arbiter.py`, `src/orlog/court.py` and `src/orlog/interp.py`, about 167 lines added, uncommitted; HEAD is still fc19339.
   - The first edit, to interp.py, is stamped 22:57:46. It adds a host budget of counted operations (`HostStop`).
   - Every process of mine imported these modules before that time. run1–run3 and the length-7 search had finished; run4 started about 22:55:53, and its one Python subprocess ran about 22:57:08.
   - So every result below is of the committed tree. I did not make those edits and did not revert them.
2. **New untracked files appeared in `research/`:** `ragnarok/ADVERSARY.md` and `roadmap-debate/ARCHITECT.md`, `PROSECUTOR.md`, `SKEPTIC.md`. They are not mine and I did not read them. This case was written without seeing the adversary's.

## 1. The design

**Thesis, narrowed.** A counterworld is a program of the frozen language that meets three conditions:
- it differs from the admitted law only in literals that a separately sealed sheet declares free;
- its run reaches the claim with every earlier check passing;
- and the claim is refuted there.

The search enumerates the sheet's finite domain exhaustively and only proposes. A separate checker re-reads each witness against the sheet and re-runs it on two evaluators. Only the checker's confirmation produces FALSIFIED. Absence is SURVIVED with the domain's size, never "proved". The first slice changes no existing contract.

### 1.1 What a world is
**What a world is.** A world assigns each parameter of a sheet (`ragnarok-sheet 0`, canonical JSON, sha256-sealed) one value from that parameter's finite domain.
- The sheet names three things: the base text, one target claim (keyed by claim id), and the parameters.
- Each parameter is a top-level `Let X be <literal>` clause.
- Its domain is an ordered list of literal spellings of the same lexical type.
- The world's text is the base text with those literals rewritten. Every world is therefore an ordinary program: the same door, parser, typer, law bytes, interpreter and receipt.

**Rests on invariant W:** the world's text differs from the base only in the parameters' literals. The checker verifies this. Because each world is a program, T0 and T5 apply to it as to any law.

**Why a sheet outside the law, not a new statement:**
- The law's bytes stay `orlog-law 0`.
- The program text cannot choose, and so cannot narrow, its own counterworld domain. This is the same reason it cannot write the ledger (T2).

**The other candidates:**
- **Define rules as defeasible axioms:** a later slice. "This exception never or always applies" can be a literal rewrite of a sheet-named Define's proviso to `false`/`true`. Clause ids are kept, and RULE-CONFLICT or RULE-UNDEFINED become exclusions.
- **Cited-theorem oracles:** not a world axis. The condition is still evaluated by computation, and a name grounds nothing (T2, L4). "A world where the theorem is false" has no computational content in the language.
- **Numeric semantics:** only `Decimals are fixed|floats` is a world of the language (a one-bit axis, later). Any other numeric semantics is not a program of the frozen language, so nothing frozen could check it.

### 1.2 Premise and conclusion
**Conclusion:** the target claim's condition at every one of its evaluations in the world. This is the court's "held".

**Premises:**
- **P1:** the world's text compiles.
- **P2:** everything executed before the claim's failing evaluation completed without refusal, so every guard and every other claim reached held. Under the stopping semantics this is implied by the status `REFUSED CLAIM-REFUTED <claim's clause>`.
- **P3:** every declared premise (`given §a`, the court's own support edge) was evaluated and held before the stop.

**The counterworld rule:** a world is a counterworld when P1 holds, the run stops `REFUSED CLAIM-REFUTED` at the claim's clause with evaluations greater than trues, and P3 holds.

**No world is dropped silently.** Each is classified:
- COMPILE-REFUSED
- RULED-OUT-BY-GUARD
- MASKED-BY-ANOTHER-CLAIM (another claim was refuted first)
- RULED-OUT-BY-REFUSAL
- UNREACHED
- PREMISE-NOT-HELD
- HELD

**Rests on:** the court's operator G(X) = {c : held(c) and premises(c) ⊆ X}. Ragnarök evaluates exactly "held" and exactly the declared premises, per world, and infers nothing new. Undeclared dependence stays invisible (L10).

### 1.3 What the search enumerates; bounds; reproducibility
**What it enumerates:** D = D1 × … × Dn in the sheet's order, each world once, on the reference interpreter.

**Bounds:**
- **Domain cap:** 4096 worlds in the probe. Above it the outcome is UNRESOLVED INCOMPLETE, and nothing is ever sampled.
- **Per-world budget (the slice):** a budget of counted operations, which is deterministic across hosts. A world that exceeds it is classed BUDGET, never HELD.
  - Termination alone is not a bound: a For over the i64 range halts only in principle.
  - The probe had no budget; its largest search was 10,742 counted operations.
  - The slice's budget does not depend on the uncommitted `HostStop` edit.

**Theorem:** every run halts, because every While states its fuel, every For has a finite range, and procedures cannot recurse. So enumerating a finite D decides whether some world in D is a counterworld. SURVIVED means exactly "no counterworld in D, as the reference computes it", and the reference's authority is declared.

**Reproducibility:** each search writes a search receipt.
- It is a hash chain over one line per world: index, assignment, class, status, and the sha256 of the reference receipt core.
- The chain is seeded with sha256(`ragnarok-search-0` ‖ sheet seal ‖ base sha256).
- It is a pure function of the base bytes, the sheet bytes, the engine version and the numeric semantics (T5).

### 1.4 The independent checker
**What it is:** it reads only the witness (base bytes, sheet, assignment, witness text), never the search's classes. It has three parts:
- **Structural reading.** Every line equals the base's, except that each parameter's line is the base line with its literal replaced by the claimed value, and that value is in the sheet's domain.
  - The claim's clause id and its premises' ids are read from the text alone, by counting clause lines and reading `given` references.
- **c99.** The witness is compiled, lowered and generated to C, then built and run through the arbiter's `build`/`run`.
- **The twin.** `twin/twin.py` runs the witness.

Each evaluator is decided from its own receipt alone. CONFIRMED requires the structural reading and both receipts.

**How independent it is, exactly:**
- **c99 shares with the search:** the door, parser, typer and law bytes (canon/syntax/sema). A shared misreading of the text passes through.
  - It does not share the evaluator: lower.py, gen_c.py and rt_c (bit-level, a separate author) against interp.py and numeric_ref (exact rationals).
  - But rt_c was required to match 20,015 vectors generated from numeric_ref, so on those inputs its agreement is not independent evidence.
- **The twin shares:** numeric_ref.py and seal.py (loaded by path, so the arithmetic is identical), and the law-seal value I pass in. That value enters only the trace head and `this law's seal`.
  - It does not share: the door, parser, typer or evaluator.
- **So the two paths are complementary.** c99 is independent in arithmetic and evaluation but not in reading; the twin is independent in reading and evaluation but not in arithmetic.
- **Neither is independent in authorship or specification.** One model family wrote the reference, the twin, both runtimes and this probe, and every reader can share a misreading of SPEC (DOCTRINE §8).
- **Rests on:** the certifying-algorithm discipline (T1). A counterworld is its own certificate and cheap to re-check; absence has no certificate. So FALSIFIED is checked witness by witness, while SURVIVED is re-derived world by world by the twin and is still never proof. Coincident failures limit what diversity buys (Knight & Leveson).

### 1.5 The three outcomes, their records, and court standing
**FALSIFIED:** at least one candidate, every candidate CONFIRMED, and no rejection.
- **Per-witness record** (`ragnarok-witness 0`): the assignment, the witness text sha256, its law seal, the c99 and twin decisions and receipt hashes, and whether the reference, c99 and twin receipt cores were byte-identical.
- **Search record:** the base, the sheet seal, the claim id and claim seal (`orlog-claim-1`), the domain size, counts per class, the search head and toolchains.

**SURVIVED:** the domain was enumerated completely, at least one world reached the claim, and there was no candidate and no PREMISE-NOT-HELD.
- The record always gives the domain size, how many worlds reached the claim, how many were masked, and the twin re-derivation count.
- Its text says "exhaustive over this domain only, and not a proof".
- The verdict firewall refuses proof-shaped keys.

**UNRESOLVED,** with one reason from a closed list:
- **INCOMPLETE:** the cap or the per-world budget.
- **VACUOUS:** no world reached the claim.
- **UNCHECKED:** candidates exist but no checker ran.
- **DISSENT:** any candidate was rejected. Disagreement is the signal and is never smoothed: one rejection blocks FALSIFIED even if others were confirmed.
- **PREMISE:** the claim failed only where a declared premise was not held.

**Court standing:**
- **A new column, "counterworld",** per claim id, bound to the claim's seal, the sheet seal and the engine version. A record never lifts to an amended law, whose claim seal differs (as with L4).
- **New rule R8:** "a counterworld search is the program's own computation over worlds a sheet declares (R2): SURVIVED is never support and never grounding; FALSIFIED refutes no evaluation of this run, shows the claim's truth depends on the sheet's free parameters, and is shown beside the standing, which it does not change."
- **Why it cannot raise standing:** support and grounding are computed from receipts and the ledger before the column is joined, so a record cannot raise either. This becomes a testable row with a plant.
- **No reflection (T1):** no construct of the language can read a record, so no law can cite its own survival.
- **Forbidden interpretations added:**
  - SURVIVED means the claim holds in every world.
  - FALSIFIED means the claim is false in this run.
  - The sheet's domain is the scope the author meant.

### 1.6 The smallest set of added assumptions
**Grammar:** `P is at least k` and `P is at most k`, for each parameter P and each k in P's domain, keeping only bounds the base world satisfies.

**Problem:** find the fewest bounds such that every counterworld found violates one of them. This is set cover: NP-hard (Karp 1972).
- **Exact method:** enumerate subsets by size. The cost is the sum over i ≤ s of C(B, i) subsets, each tested against every counterworld by predicates over recorded assignments, with no reruns.
- **Ties:** among the minimal sets, rank first the weakest, the one that rules out the fewest worlds where the claim held.
- **Validation:** phrase the set as a guard, insert it as a new clause (renumbering clauses and references, so it is a new law with a new seal, never a fix), and rerun the search.
  - This checks consistency only.
  - Sufficiency outside the domain is NOT_MEASURED, and the result is a proposal to the author. Ragnarök never amends a law.
- **Beyond exact reach** (large B, or a size above 3): report "none within size s", or a greedy cover labelled NOT MINIMAL (Chvátal).

### 1.7 The second target: the system's own coverage claims
Each coverage claim is a "for all" over a class. A coverage search carries a plant from that class, which must be found inside the same bound; otherwise the bound means nothing. The outcomes are the same three.

The targets, by value:
1. **The door's retraction (T6, DECLARED).** Measured: section 2.
2. **QUOTE-BOUNDARY's coverage.** The literals the lexer reads in canon(x) should equal the literals that an independent §12 reader reads in x. Its plant is the L12 case `“a”"b"`. Designed, not built.
3. **The phase table's completeness (T10)** over a small token grammar: every text yields acceptance or one listed code, never a stray exception. Its plant is the existing STATEMENT-PERIOD plant.
4. **The court's fixed points over every support graph on 4 claims or fewer** (about 2^20 cases): Kleene's lfp and gfp should equal the Knaster–Tarski characterization, computed by brute force. Its plant is court-accepts-gfp.
5. **Mutation coverage of the self-test's plants.**
6. **Backend equivalence over an enumerated program grammar.**

### 1.8 Versions and contracts
- **Unchanged in slice 1:** `orlog-law 0`, `orlog-receipt 0`, `orlog-trace-0`, `orlog-claim-1`, the numeric semantics, the phase table and the arbiter.
- **New:** `ragnarok-sheet 0`, `ragnarok-search 0` and `ragnarok-witness 0`, plus a separate table of sheet refusal codes (SHEET-BASE, -CLAIM, -PARAMETER, -CAP).
- **Changed:**
  - The court gains R8 and the column. Its artifact text, and so its chain hash, changes for every program, so it needs a version line (`orlog-court 1`).
  - Also changed: SPEC §15, DOCTRINE T11 and its §8 non-claims, AGENTS, and new self-test rows.
- **Deferred, because they change contracts:**
  - A law that declares its own scope (`orlog-law 1`, new compile codes, a new claim-seal version, a twin round).
  - A mode that suspends the target's refusal (a new receipt version in all four executions).

## 2. What the probe measured
**D1, a planted counterworld.** The probe's own `bounce.orl`: a ball turns back at walls 0 and 10; the claim is "x stays in the room" (§4.3). The sheet varies v over -12..12. The expected set was worked by hand before the run:
```
   search  COUNTERWORLD 10  HELD 15  head 888ed0e6a9a0245d  (8473 counted ops; reference-only wall 0.03 s)
   candidates (10): -12 -11 -10 -9 -8 8 9 10 11 12
   worked by hand before the run (10): MET
   check 8      only the parameters' literals differ | c99 REFUSED CLAIM-REFUTED 7 | twin REFUSED CLAIM-REFUTED 7 | reference = c99 = twin byte for byte: True -> CONFIRMED
   OUTCOME FALSIFIED: 10 of 10 candidate(s) confirmed by c99 and the twin, each from its own receipt
   assumption: minimum 2 bound(s) of 26 candidates (351 subsets tested); 60 minimal set(s); the weakest, 'v is at least -7 and v is at most 7', also rules out 0 world(s) where the claim held
```
- **D2,** that guard inserted as §4: `HELD 15  RULED-OUT-BY-GUARD 10` → `OUTCOME SURVIVED: no counterworld among 25 worlds (15 reached the claim, 0 masked by another claim's refutation, 10 ruled out otherwise); exhaustive over this domain only, and not a proof`.
- **D3,** the amended law with v in 8..12: `OUTCOME UNRESOLVED: VACUOUS: none of the 5 worlds reached the claim`.

**D4, no counterworld in the domain.** `examples/gcd_certificate.orl`, with a and b in 1..12:
```
   search  HELD 144  head 03173fbaa50cfc70  (10742 counted ops; reference-only wall 0.23 s)
   OUTCOME SURVIVED: no counterworld among 144 worlds (144 reached the claim, 0 masked by another claim's refutation, 0 ruled out otherwise); exhaustive over this domain only, and not a proof
   twin re-derivation: 144 of 144 worlds byte-identical; wall 27.4 s
```

**D5, a modest real finding on a corpus law.** gcd with a and b in -2..2: `COUNTERWORLD 11  HELD 14`, the hand-worked set MET, and FALSIFIED with 11 of 11 confirmed.
- The counterworlds are exactly where b = 0 with a ≤ 0, or b < 0 divides a. There the law's extended Euclid returns a non-positive g, and the certificate's "g is positive" correctly refuses.
- Assumption: `minimum 1 bound(s) of 10 candidates ... the weakest, 'b is at least 1', also rules out 4 world(s) where the claim held`. The exact frontier cannot be expressed with bounds.
- **D5'**, that guard inserted as §3, with the certificate reference renumbered from §9 to §10: `HELD 10  RULED-OUT-BY-GUARD 15` → SURVIVED.

**D6 and D7, where the design is weakest** (both on `examples/plankton.orl`):
- **D6, the premise discipline.** §3 cites a later premise. With plan and robot in 6..8: `HELD 3  PREMISE-NOT-HELD 6` → `OUTCOME UNRESOLVED: PREMISE`, never FALSIFIED.
- **D7, masking.** §5 "plan is positive", with plan and robot in {-1, 7}: `HELD 1  MASKED-BY-ANOTHER-CLAIM 3` → SURVIVED "(1 reached the claim, 3 masked ...)". World (-1,-1) would refute §5 if reached (worked by hand), but §4 refutes first.

**Plants, all caught:**
```
   plant false-witness (the base world offered as a counterworld): CAUGHT, c99 COMPLETED, twin COMPLETED
   plant tampered-witness (the claim edited to 'x is at most 5'): CAUGHT by the structural reading (line 9 differs from the base where the sheet allows nothing); the C run alone would have said (True, 'REFUSED CLAIM-REFUTED 7')
   plant lying-search (HELD and COUNTERWORLD swapped): CAUGHT, outcome UNRESOLVED (DISSENT: the checker rejected 1 of the 1 candidate(s) it read; first rejected v=-7, c99 COMPLETED)
   plant no-checker (the search alone): CAUGHT, outcome UNRESOLVED (UNCHECKED: 10 candidate(s) and no checker ran)
   plant proof-shaped-record: CAUGHT (verdict-shaped field record.proved refused)
   plant oversized-domain (17^3 worlds): outcome UNRESOLVED (INCOMPLETE: 4913 worlds exceed the cap of 4096; nothing was sampled)
== reproducibility: D1's search head 888ed0e6a9a0245d, again 888ed0e6a9a0245d, under PYTHONHASHSEED=424242 888ed0e6a9a0245d: IDENTICAL
```

**Reproducibility:**
- run1 and run2 differ only in one wall-time line.
- run4, on a fresh build cache, built its 24 C executables itself and equals run3 once wall times are masked. Earlier runs had reused cached builds; the generator inlines rt_c into each source, so the cache key covers the runtime.

**Court illustration:** the §4.3 row reads support WELL-FOUNDED and grounding UNGROUNDED, with the counterworld column FALSIFIED. In the probe the column is joined after the panel is computed, so it trivially leaves support and grounding unchanged; this illustrates the format, not a test.

**Cost** (software timings):
- The reference-only search takes well under a second: 0.03 s for 25 worlds, 0.23 s for 144.
- Each witness costs one clang build (about 2.1 s, measured once) and one twin run (about 0.3 s).
- The twin's re-derivation dominates.
- All claim targets together: 58.0 s with cached builds (run1), 78.1 s with 24 fresh builds (run4).

**The door's retraction, a coverage claim.** Over every token sequence on the alphabet {`"`, U+201C, U+201D, U+201E, NBSP, SP, TAB, CR, LF, `Note:`, `a`, U+0301, ZWJ}, the test was: the second pass gives the same text, with no REPAIR and no REFUSE.
```
== door retraction: 5229043 token sequences of length 0..6 over 13 symbols {...}: 890827 accepted by the first pass, 186051 with a NOTE on the second pass, 0 counterexample(s); wall 65.7 s
door retraction k<=7: 67977560 sequences, 9586492 accepted, 2504417 NOTE on pass 2, 0 counterexample(s), wall 1180.3 s
   plant quote-boundary-off over length 0..5 (402234 sequences): 20 counterexample(s); wall 4.4 s
   first under the plant: NBSP Note: " NBSP " bytes c2a04e6f74653a22c2a022 pass1 ' Note:"\xa0"\n' pass2 ' Note:" "\n' ['R-SPACE']; the real door, in a fresh process: refused QUOTE-BOUNDARY
```
- **Result:** no real counterexample, so SURVIVED, exhaustive over this alphabet up to length 7 only.
- **The plant reaches a real defect class.** Its first counterexample is byte-identical to the red team's `court/redteam-eng/E18_door_not_idempotent.raw`. All 20 are E18's class: NBSP or TAB before `Note:`, then a literal holding an NBSP, in each of the 10 valid quote pairs.
- **What the domain exercised:** 9 of the door's 18 repair rules. It did not exercise R-BOM, R-APOSTROPHE, or the seven code-map rules (R-MINUS, R-HYPHEN, R-TIMES, R-DIVIDE, R-LEQ, R-GEQ, R-NEQ).
- **Grade:** retraction in general stays DECLARED. No small-model lifting is claimed.

## 3. The first real slice: RAGNAROK-0 (proposed, nothing admitted)
**In scope:**
- `src/orlog/ragnarok.py`: the sheet loader, the search, the judge, the search receipt, and an all-claims mode that shares one enumeration so masking is visible.
- `src/orlog/ragnarok_check.py`: imports neither `ragnarok.py` nor `interp.py`.
- `orl.py ragnarok` and `ragnarok-assume`. The second prints minimal sets and never writes a law.
- court R8 and the counterworld column.
- Fixtures, the self-test rows below, SPEC §15 and DOCTRINE T11.

**Out of scope:** sampling, solvers, law-declared scopes, Define or decimals worlds, the suspend-target mode, and lowering any standing.

**Acceptance tests, each able to fail:**
- **A1, the planted counterworld.** D1's set is exactly {-12..-8, 8..12}, held as a literal list. Every candidate is CONFIRMED by both paths, with three-way byte identity.
- **A2, bounded survival.** D4 is SURVIVED with 144 of 144 reached and 144 of 144 re-derived. The text contains "not a proof", and the proof-shaped-record plant is caught.
- **A3, vacuity.** D3 is VACUOUS. A judge that counts ruled-out worlds as reached must turn this row red.
- **A4, the premise discipline.** D6 is UNRESOLVED PREMISE. A judge that ignores premises must report FALSIFIED here and be caught.
- **A5, masking shown.** D7 reports "3 masked", and all-claims mode names the claim that refuted first in each masked world.
- **A6, the checker's plants.** False witness, tampered witness (with the kill witness: the C run alone confirms it), lying search, no checker: each caught as in section 2.
- **A7, the cap and the budget.** 17³ worlds gives INCOMPLETE with zero worlds run. A world over the per-world budget is BUDGET, never HELD.
- **A8, reproducibility.** The search heads match twice, and match under PYTHONHASHSEED 0 and 424242.
- **A9, assumptions.** bounce gives minimum 2, {v ≥ -7, v ≤ 7}, excluding 0 held worlds. gcd gives minimum 1, {b ≥ 1}, excluding 4. Each amended law's re-search gives HELD 15 / GUARD 10 and HELD 10 / GUARD 15 respectively.
- **A10, court invariance.** Over the corpus, support and grounding are identical with and without records. The plant court-grounds-survival is caught.
- **A11, the import fence.** A source scan, with a plant.
- **A12, door retraction coverage.** Up to length 5 in the self-test (up to 6 as an evidence run): 0 counterexamples. The plant yields E18's bytes, which the real door refuses QUOTE-BOUNDARY.

## 4. How the design keeps the doctrine
- **Agreement is consistency, not truth.** FALSIFIED is three implementations agreeing byte for byte on one world under one specification.
  - It is conditional on the sheet and on SPEC, and one model family wrote them all.
  - It does not show that the world is physically meaningful, or that the sheet's domain is the scope the author meant. The intent is not in the text.
- **The search never certifies itself:**
  - It only proposes; FALSIFIED needs the checker, and any rejection makes the outcome UNRESOLVED.
  - Absence is SURVIVED: bounded, labelled, and by R8 neither support nor grounding.
  - The sheet sits outside the law, and no construct can read a record.
  - Every coverage search carries an in-bound plant, and the checker's own failure modes are planted.
  - It does what the owner asked: it refuses to call a bounded search a universal proof.

## 5. Where I expect the attack, and my answer
- **FALSIFIED is only as meaningful as the sheet.** Any claim that depends on a constant falls to a wide enough sheet; D1 is planted and D5 is modest. The sheet is a person's act, sealed into every record, and no standing changes.
- **The stopping semantics hides things.** Later guards and premises are never evaluated, masking can hide a counterworld (D7), and plankton's cycle can only be UNRESOLVED. Fixing this needs the suspend-target mode, a contract change; it is named, not hidden.
- **Independence is partial,** as stated in 1.4: c99 shares the front end, the twin shares numeric_ref, and rt_c was held to numeric_ref's vectors.
- **Each world is a separate C build,** so re-deriving a whole domain on C is impractical. Capability inputs (DOCTRINE §9) would make it one build per law.
- **The bound grammar is weak.** gcd's frontier cannot be expressed in it, and minimality is relative only to the counterworlds found.
- **Probe shortcuts:**
  - The checker and the search live in one file.
  - Receipts are keyed by clause rather than claim id (L17 needs ids).
  - The assumption pre-check compares exact fractions, while a decimal parameter compares as rounded storage; the language's own re-search is the authority.
  - The door alphabet is my choice.
- **Novelty: none claimed.** Bounded exhaustive testing (Alloy's small-scope hypothesis, SmallCheck, Korat), bounded model checking, CEGAR, assumption inference, mutation testing, differential testing and certifying algorithms are prior art. Any novelty in the integration with the court is SPECULATIVE until a cited search is done.
