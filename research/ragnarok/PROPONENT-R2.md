# Debate record: the proponent's answer to the prosecution, round 2 (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the proponent read ADVERSARY.md; its runs are in `work/ragnarok-probe/round2*`
(ignored by git) and used the judge's uncommitted repairs (the host budget and isolated run folders); its MEASURED
lines are this host's. The untracked tests/numeric_oracle.py it mentions is the judge's. Absolute paths that named the owner's home folder are given relative to the repository, or as the session's scratchpad (AGENTS.md section 8); nothing else is changed.

---

# Ragnarök round 2: the proponent answers the prosecution

**What I ran.** Here (Windows 11, CPython 3.14.5, clang 22.1.8, rustc 1.96.1):

`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B work/ragnarok-probe/round2.py`

- It ran three times, and the outputs (`round2-run{1,2,3}.txt`) are identical once wall times are masked.
- Part 1 runs my round-1 rules unchanged on the adversary's fixtures. Part 2 runs the rules corrected below.
- It uses the judge's uncommitted repairs: `Interp(budget=)`/`HostStop`, and the arbiter's per-arbitration run folders.
- I touched no tracked file. An untracked `tests/numeric_oracle.py` has appeared; it is not mine.

## 1. The counts

- **R-1, narrow.** I chose (A) and accept that every world is another law; records never lift across laws.
  - The cost figure assumes four executions in every world. Only refuting worlds need them: WALL_BACK cross-checked 6 of its 10 worlds.
  - (C) is not always available. Wrapping each corpus law in a `For` refuses 4 of 10: `chaos REFUSED DECIMALS-PLACE`, `fall`/`legal REFUSED DEFINE-PLACE`, `leapfrog REFUSED UNKNOWN-PROCEDURE`.
- **R-2, concede.** The only computable reading is refutation by changing an input. That is all my design ever did.
- **R-3, narrow.**
  - Rebuttal for my design: my round-1 rules gave WALL_FWD `UNRESOLVED PREMISE`, not SURVIVED. They also fixed the reading of a must placed before the claim (`WALL_MUST ... 6 ruled out otherwise`).
  - Concession, including a defect the adversary missed: a world where the claim held and its later premise then failed counted as reached (`R1 WALL_FWD §5, v in {0, 1} SURVIVED ... 2 reached`).
  - Corrected: the case is now decided from the text alone (`R2 WALL_FWD §5 ... NOT DEFINED`).
- **R-4, concede.** My own D5 printed the problem: "also rules out 4 world(s) where the claim held". The assumption search leaves the first slice.
- **R-5, concede on vocabulary.**
  - E5 does not apply to my design, which already had VACUOUS (`R1 WALL_VAC ... UNRESOLVED VACUOUS`).
  - E8 does apply: `R1 PLANKTON §5 SURVIVED ... 1 reached the claim, 99 masked`.
  - I adopt the adversary's five sentences. My part-2 lines use them and pass its forbidden-word list.
- **R-6, narrow.**
  - Concede: running a witness validates the run, not the domain, the readings or the grammar. Re-deriving an absence costs about the search again; in round 1 the twin took 27.4 s for 144 worlds, about 100 times the search.
  - What the checker adds beyond rerunning:
    - It binds the witness to the sheet. The C run alone accepted a tampered witness: `(True, 'REFUSED CLAIM-REFUTED 7')`.
    - It bites on misclassification. With the plant "a failed must counted as a refutation", it printed `DISSENT IN DOMAIN ...: the checker rejected 6 refuting world(s)`.
- **R-7, concede.** Which literals a claim generalizes over is intent. A sheet is a hypothesis, not the author's meaning.
- **R-8, concede the loop; narrow on E10.**
  - E10 broke my round-1 judge too: `skips the last world → SURVIVED ... 1 ruled out otherwise`, booking a world never run as excluded.
  - Repaired by recounting the domain separately from the enumerator: `INCOMPLETE ... 4 of 5 worlds run`.
- **R-9, concede.** The sheet carries no standing by design. A domain meant to carry standing belongs in the law.
- **R-10, concede.** I claimed no novelty. SV-COMP's "unconfirmed" and Nitpick's genuine/candidate split are my UNCHECKED/CONFIRMED.
- **R-11, narrow.**
  - Concede the blow-up. The cap and the budget give INCOMPLETE, for example `SUM_LAW ... 2 of 3 worlds run within 100000 counted operations`.
  - Rebut "every execution in every world": only refuting worlds are cross-checked.
  - Where (C) applies, it is far cheaper: `BOUNCE_LOOP, 25 speeds in one law ... agree [c99,python,rust] ... 2.7 s (three builds)`. A checked substituted world costs about 2.4 s each (a 2.1 s clang build plus a 0.3 s twin run).
- **R-12, concede: withdrawn.** See (a).
- **R-13, concede.** The assumption search was my only step toward abduction. Everything left is finite: cap, budget, INCOMPLETE.
- **R-14, concede.** No recorded failure needs Ragnarök. My door search found nothing new (its 20 planted counterexamples are all E18's class), and D5 is no recorded failure.
- **R-15, concede**, with my own instances: E10 (above), E7 (see b), E8 (above), E6 (D5).

## 2. RAGNARÖK-0
**Already met, and now measured:**
- AT-1 exactly: `REFUTED IN DOMAIN ... 6 of 10 worlds refute §6; first witness v=3; its law pukak-gobad-magor-sipuj`. The witness on four executions: `agree [c99,python,rust]`.
- AT-1's skip-last plant reads INCOMPLETE.
- AT-2: `VACUOUS ... 0 of 9`, `NO REFUTATION ... 4 of 10 reached ... 6 of 10 stopped by a must`, and `NOT DEFINED for §5`.
- AT-3: the court output and ledger hashes are `IDENTICAL` around a run.
- Also adopted: no language change, the sheet's sha256, a budget in counted operations, no ledger writes, no court column, no assumptions, and its trigger rule.

**Where I differ, and why each is worth its cost:**
1. **The twin and the structural reading join the four executions.**
   - The four executions share the door, parser and typer. The twin is the one reader that does not, and its rounds found 62 ambiguities and reference defects (SPEC §11, §13, §14).
   - The cost is about 0.3 s per refuting world.
   - The structural reading caught the tampered witness that execution alone accepted.
2. **One added clause in the NO REFUTATION sentence:** "q of N by another claim before it". Without it, Plankton §5 reads like a test of 100 worlds; with it, the line says 99 of them never reached §5.
3. **Coverage targets, each with an in-bound plant** (the proposal's own new question, kept small).
   - The door retraction: 67,977,560 sequences, 0 counterexamples. The planted door yields E18's exact bytes within length 5.
   - This turned a DECLARED claim into a bounded MEASURED one for one script and about 20 CPU-minutes.

## 3. The four questions
**(a) Withdrawn.**
- R8 computed support and grounding before the join. That protected the computation, never the reader.
- Placed beside the court's CIRCULAR, my own `R1 PLANKTON §5 SURVIVED ... 1 reached the claim, 99 masked` reads as vindication, exactly as E8 says.
- Reports stay separate. AT-3 (the court's output and the ledger byte-identical before and after a run) replaces my A10.

**(b) Nothing about the claim.**
- That the found counterworlds are excluded is true by construction. With the right guard, `10 of 25 were stopped by a must`, and those are the 10 counterworlds.
- What the re-search can show is that the guard, as phrased in the language and inserted with renumbering, means what the search's predicate meant. Phrased one off (`at most 8`), it gives `REFUTED IN DOMAIN ... 1 of 25 ... first witness v=8`.
- That tests the amendment pipeline, not the law.
- It also excludes good worlds (4 in gcd). So the step leaves the slice.

**(c) Each serves a different job.**
- **A domain the author asserts belongs in the law.**
  - It costs one build per backend: 2.7 s for 25 worlds on four executions.
  - Its seal binds the domain to the claim, and under R5 the owner's ratification judges the domain.
  - The loop reproduced my frontier exactly: `speed -12 … -8, 8 … 12 leave the room`.
  - But the author must restate the claim as a counter, and the language refuses the loop around Decimals, Defines and procedures (4 of 10 corpus laws).
- **A sheet serves a prosecutor's hypothesis about a law as written.**
  - It needs no rewrite.
  - It enumerates the whole frontier.
  - Each refuting world is a standalone sealed law anyone can rerun.
  - It carries no standing.

**(d) Nothing, in my design.**
- Sealing the sheet records who wrote it and authenticates no one.
- What weakens the loop is a domain rule fixed before any law is read. "Every Let integer w over [w−10, w+10]" finds what the author's {1, 2} missed:
  - `7 of 21 worlds refute §6`. Worked by hand, these are v = 3, 4, 6, 7, 8, 9 and 11.
  - With x0 free as well, `174 of 441` refute on the reference alone (unchecked).
- The rule's author is still the same model family, so coincident failure remains. Three free literals already exceed the cap.
- The other ways to weaken it are owner-written domains, and (C) with the owner's ratification.

## 4. What I got wrong in round 1, corrected
1. **Domain size.** The judge took it from the sheet rather than from the worlds actually run (E10). Corrected: an independent recount, which gives INCOMPLETE.
2. **Later premises.** A world whose later premise failed after the claim held counted as reached. Corrected: NOT DEFINED, decided from the text before any run.
3. **MASKED.** It merged a refuted premise with a different claim refuted first; WALL_VAC's 9 worlds were stopped by its own premise §2. Corrected: those now read `PREMISE-REFUTED 9`.
4. **R8 and the counterworld column:** withdrawn.
5. **The assumption search and its re-search (A9) in RAGNAROK-0:** withdrawn.
6. **SURVIVED and FALSIFIED:** replaced by the adversary's sentences. My door result now reads NO REFUTATION in its domain.
7. **The per-world budget:** only proposed in round 1; now measured, using the judge's HostStop.

**Files** (git-ignored):
- `work\ragnarok-probe\round2.py` (270 lines)
- `round2-run1.txt`, `round2-run2.txt`, `round2-run3.txt` beside it. run3 rebuilt the loop and four-execution builds fresh, for the timings.
