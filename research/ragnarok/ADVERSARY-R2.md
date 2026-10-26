# Debate record: the adversary's report on the proponent's design, round 2 (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the adversary read PROPONENT.md; its experiments are in `work/ragnarok-adv/round2/`
(ignored by git) and ran on the tree holding the judge's uncommitted repairs; its MEASURED lines are this host's. Absolute paths that named the owner's home folder are given relative to the repository, or as the session's scratchpad (AGENTS.md section 8); nothing else is changed.

---

# Round 2: the adversary's report on the proponent's design as built

**Bottom line.** The design answers 5 of my 15 counts, partly answers 7, leaves 2 standing, and makes 1 worse. I found ten new defects in it. Two matter most:
- A world the search never ran is reported as "ruled out otherwise", and nothing outside the fixtures catches it.
- One defect in code all three paths share produces a FALSIFIED that the checker confirms, three ways byte-identical.

**How I ran it.** Every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` in `work\ragnarok-adv\round2\`, against an exact copy of the probe (`probe_copy.py`; only its ROOT line changed; the original's sha256 starts 2a0c073f).
- The tree included the judge's uncommitted repairs. The probe passes no budget, so HostStop never fired.
- Commands: `r2.py` (R2-1 to R2-7), `r2.py --plant-literal` (R2-8), `door5.py` (the door search).
- Outputs are in `round2\out\`. `r2.py` ran twice with byte-identical output. Everything below is MEASURED here.
- I changed no tracked file.

## 1. My counts against the design

**Answered (5):**
- R-1: a world is a rewrite of top-level `Let` literals named in a sealed sheet, with no language change.
- R-2: the thesis is narrowed.
- R-7: the court is now described correctly.
- R-10: no novelty is claimed.
- R-13: solvers and sampling are out of scope.

**Partly answered (7):**
- R-3: WALL_FWD now reads UNRESOLVED PREMISE instead of SURVIVED (R2-1), but see D-2, D-3 and D-6 below.
- R-5: VACUOUS exists (R2-3a reads it), but see question (a).
- R-6: there is now a real checker with planted failure modes, but see D-1 and D-8.
- R-9: the sheet is sealed into every record, but nothing binds it to a person, or to a time before the results were seen.
- R-11: a cap, a per-world budget of counted operations, and a search on the reference only.
- R-12: see question (b).
- R-15: the checker plants are good, but A1 would catch an enumerator that skips a world only because D1's last world (v=12) happens to be a counterworld.

**Still standing (2):**
- R-8: the sheet and the door alphabet are the author's own vocabulary; see question (d).
- R-14: there is no admission record and no trigger. D5's "finding" is a Fibonacci gcd failing on negative inputs it was never written for, which is R-7's change of subject.

**Made worse (1): R-4.**
- The repair loop I called FATAL is now a demonstration (D2, D5′) and an acceptance row (A9). Ragnarök fits a guard to the counterworlds, searches the same domain again, and prints SURVIVED.
- D5′ prints SURVIVED although, by the proponent's own D5 line, its guard rules out 4 worlds where the claim held.
- Section 1.1 plans Define-proviso worlds in which RULE-CONFLICT and RULE-UNDEFINED "become exclusions". That files a defeasible law's own defect class as "not admissible" (see R2-6b).

## 2. New defects in the design

- **D-1. A skipped world is reported as ruled out (R2-2b).**
  - I ran my E10 plant (the search skips its last world) on a claim refuted only at v=10. The result: `SURVIVED … among 10 worlds (9 reached the claim, … 1 ruled out otherwise)`, and the twin re-derivation reads "9 of 9".
  - "Ruled out otherwise" is computed as size − reached − masked (ragnarok.py:262–265), so a world never run counts as ruled out.
  - `rederive` (ragnarok.py:316–323) replays the search's own rows. It never enumerates the sheet.
- **D-2. A false reason (R2-1).** The PREMISE reason says "the claim failed only where a declared premise did not hold". But §6 ("v is not zero") held in all six worlds; it was never evaluated. That is a false event in the record.
- **D-3. The premise rule applies only to refutations (R2-1b).** In WALL_FWD with v=0, the declared premise is refuted after the claim, yet the world is counted HELD and "reached the claim" (ragnarok.py:91–92).
- **D-4. SURVIVED over masked worlds (R2-3b, R2-4).**
  - SURVIVED with 1 of 10 worlds reached (9 masked).
  - plankton §5: SURVIVED with 1 of 100 worlds reached (99 masked), shown beside the court's CIRCULAR.
  - The proponent's own D7 is SURVIVED over a masked world that would refute the claim. "Exhaustive" there means enumerated, not tested.
- **D-5. A refusal inside the claim itself counts as ruled out (R2-6a/b).** `REFUSED OVERFLOW 2` (in the claim's own condition) and `REFUSED RULE-CONFLICT 4` (in a rule the claim uses) both name the claim's clause. Both are filed RULED-OUT-BY-REFUSAL, and SURVIVED is issued.
- **D-6. Guards are read as assumptions (R2-5).** WALL_MUST, a guard restating the conclusion, gives SURVIVED with "6 ruled out otherwise".
- **D-7. The firewall scans keys only (R2-7).** It refuses a key named `proved`, but passes `{"outcome": "PROVED", "reason": "the claim holds in every world; proved"}` (ragnarok.py:224–232).
- **D-8. A FALSIFIED the checker confirms, from one shared defect (R2-8).** See question (c).
- **D-9. A court contract change for a display.** The new column changes the court artifact of every program (`orlog-court 1`).
- **D-10. Six instruments under one name.** Section 1.7 lists six coverage targets. Each is a separate instrument and needs its own admission record.

## 3. The four questions

**(a) The vocabulary is not acceptable as built.**
1. Outcome words and reasons are never checked (D-7).
2. The court row shows FALSIFIED beside WELL-FOUNDED for a claim that held in its own run (the probe's own court line). The design has to add "FALSIFIED means the claim is false in this run" and "SURVIVED means the claim holds in every world" to the forbidden interpretations. Words whose natural reading must be forbidden are the wrong words; L10's CLOSED was the same mistake.
3. SURVIVED is issued over masked worlds, over worlds a guard excluded, and over refusals at the claim's own clause (D-4 to D-6), and its text still says "exhaustive".
4. Item 5 of section 1.7 applies SURVIVED to mutation coverage, where PIT's SURVIVED means the opposite.

**(b) A10 answers half of R-12.**
- With its plant, A10 covers the computational half: a record cannot raise support or grounding. The probe's own invariance is trivial, by its own account, because it joins the column after the panel.
- A10 does not stop the column from being read as a standing: plankton §5 would show CIRCULAR next to SURVIVED.
- Anyone who writes a sheet can paint FALSIFIED on any claim that depends on a constant (conceded), beside an owner's GROUNDED.
- It also costs a court contract change (D-9).
- Records belong beside the court record, not in the panel.

**(c) The independence claim is partly accurate.**
- Accurate: c99 shares canon, syntax and sema, and does not use `interp.py`. The twin has its own parser, typer and evaluator, loads `numeric_ref.py` and `seal.py` by path, and is handed the law seal.
- Inaccurate, three ways:
  1. **The paths share the varied axis.** Decimal literals are converted in the shared `sema.py`, by `numeric_ref.round_half_even` (sema.py:341) or CPython `float`, and the twin calls the same function (twin.py:2050). So all three paths share the conversion of every parameter value.
     - R2-8: I made that one function send ties up, in this process and in a scratch copy of the twin.
     - World x = 2^-33 then reads COUNTERWORLD: c99 `REFUSED CLAIM-REFUTED 2`, twin `REFUSED CLAIM-REFUTED 2`, byte-identical, CONFIRMED, so FALSIFIED.
     - Without the plant, both worlds are HELD and the outcome is SURVIVED.
     - Calling the paths complementary implies every defect is seen by at least one of them. This one is seen by none.
  2. **Neither path reads raw bytes.** The twin has no door (twin.py:9–10), and worlds are written as canonical text.
  3. **Receipt identity is partly built in.** The twin's law line and trace-head seed come from the shared front end.

**(d) The door search result is genuine, within its alphabet.**
- Rerun here to length 5:
  - the real door: 402,234 sequences, 83,328 accepted, 0 counterexamples;
  - under the plant: 20 counterexamples, the first byte-identical to E18 (`c2a04e6f74653a22c2a022`), all 20 of E18's kind.
- What it does not show:
  - The alphabet has no digit, no `§` and no `Title:`, so no clause line and no title line can ever be formed. `doorfuzz.py`'s random alphabet does contain them.
  - It exercises 9 of the door's 18 repair rules, by its own count.
  - It says nothing about whether repairs preserve meaning.
- The positive control re-finds a defect whose ingredients the alphabet was built from, through the self-test's existing plant hook (canon.py:218; selftest.py:105). It shows the harness works, not how far the alphabet reaches. That is R-8 in miniature.
- The length-7 result is the proponent's measurement; I did not rerun it. Retraction stays DECLARED, as the design itself says.

## 4. My narrowest acceptable version, revised

The design changed my mind on three points, and I adopt them:
- the sealed sheet limited to top-level `Let` literals: narrower than my domain file, and checkable by structure;
- the structural reading of each witness: its tampered-witness plant shows that a C run alone confirms what the structural reading refuses;
- the search receipt, with its cap and its budget of counted operations.

**RAGNARÖK-0, revised:** the proponent's sheet, search, structural checker and receipt, used as an instrument by a prosecutor and never as a court. With these changes:
- No court column.
- No assumption search judged by searching its own domain again. Bounds may be printed, labelled "separators, not assumptions".
- The number of worlds run must equal the size of the domain, and the checker enumerates the domain from the sheet itself. Otherwise the outcome is INCOMPLETE.
- Masked worlds, and refusals at the claim's own clause, block NO REFUTATION.
- A premise at or after its claim makes the outcome NOT DEFINED.
- Outcome values are scanned, not only keys.
- The shared literal conversion is declared as the checker's known blind spot. R2-8 holds it as a declared row that must read CONFIRMED and is never counted as caught.
- It is admitted only with its own admission record and a named trigger.

**The exact words** (s is the first 16 hex digits of the sheet's seal):
1. `REFUTED IN SHEET s=… law=…: r of N worlds refute §k; first witness p=v; confirmed by the structural reading, c99 and the twin. §k in law … is not changed by this.`
2. `NO REFUTATION IN SHEET s=…: 0 of N worlds refute §k; m reached it with its premises held; g were stopped by a guard and o by another refusal before it. Not a proof: nothing is said of any world outside s.`
3. `VACUOUS IN SHEET s=…: 0 of N worlds reached §k with its premises held; nothing was tested.`
4. `NOT DEFINED for §k: its premise §j stands at or after it, and a claim's later premises are not evaluated whenever it fails.`
5. `UNRESOLVED IN SHEET s=…: x worlds masked by another claim and y refused while evaluating §k; no outcome.`
6. `INCOMPLETE s=…: n of N worlds run; no outcome.`

**Acceptance:** my round-1 tests AT-1 to AT-3 carried over to sheets, plus rows that must read as follows:
- R2-1 reads NOT DEFINED;
- R2-2b reads INCOMPLETE;
- R2-3b, and R2-4 for §5, read UNRESOLVED because of masked worlds;
- R2-6a and R2-6b read UNRESOLVED because of a refusal at the claim;
- in R2-7, the value scan refuses PROVED;
- R2-8 stays the declared row.
