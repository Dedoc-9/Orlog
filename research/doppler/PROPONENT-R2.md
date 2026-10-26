# Debate record: the proponent's answer to the prosecution, round 2 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. It was written after the proponent read ADVERSARY.md and RESEARCH.md; its runs are in
`work/doppler-probe/` (ignored by git); its MEASURED lines are this host's.

---

# Proponent, round 2

- **Tree:** 3417949, and no tracked file changed.
- **New script:** `work/doppler-probe/round2.py`. It imports the adversary's laws, unchanged, from `work/doppler-adv/a_lattice.py`.
- **How the numbers were made:** every MEASURED line below comes from `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B work/doppler-probe/run_all.py`. All eight parts held, and their output is in `work/doppler-probe/out/`.

## 1. Counts

| count | stance | evidence |
|---|---|---|
| DP-1 | concede, against the paste | My derivations A and B read FLOWS on all seven of its laws (TERM, TEXT, MAGIC, RULE, LIST, LEN, COST). My search witnesses six. FIXED never comes from a search |
| DP-2 | concede the mechanism; concede "nearly the coarse rule" on the measured population | answered in (b) |
| DP-3 | concede | I rejected taint in round 1. My second verifier is B, a static derivation, not a monitor (survey lesson 3) |
| DP-4 | concede | it is the same repair |
| DP-5 | concede; adopt AT-5 | My round 1 implied my verdict repairs it. It does not (see §4) |
| DP-6 | narrow: the fork stands, restated | answered in (a) |
| DP-7 | concede the analogy | FIXED is not a search conjecture: MAGIC reads FLOWS from the text alone, with no shift in 22 worlds. But refuting a FIXED verdict is as hard as the search, so the "bounty" is not ruthless |
| DP-8 | concede | Convergent: 2^64 states take about 1.5 × 10^7 years at this host's reference tick rate, and the 8th translation refuses OVERFLOW (`equiv.py`). My "513 bits" counted fall.orl's constants; 321 assigned bits is the better count |
| DP-9 | concede | Tokens are the one case where its bound is small: k read-once tokens have B_k orbits, all checked (5 for 3 ports) |
| DP-10, 11, 12, 14 | concede | Convergent measurements: vx falls from 2.0 to 0.1758, and reading `-` as `+` passes both of leapfrog's guards |
| DP-13 | rebut, for my design | FIXED adds a conjunct to the court's existing base, and the horizon adds "n ≤ N". Each session's grounding stays binary. A premise with a shorter horizon caps its conclusion through the least fixed point (argued) |
| DP-15, 16, 18 | concede | I claim no novelty and drop no port from the log. One author wrote everything; B shares no code with A, and only the search runs outside the rules |
| DP-17 | concede | Nothing should be built before a trigger; (b) names one |

The adversary's LEN shifts at thrust 2^62: y overflows at tick 2, giving 1 evaluation instead of 16. Its ±1000 domain misses that value, but the analysis flags it from the text.

## 2. The four questions

**(a) DP-6: the fork stands, inside DP-6's own remedy.**

DP-6 is right that whatever grounds a tick-block claim must be an invariant over the logs it covers. The fork supplies exactly that, bounded:
- FIXED (2-safety) makes every log of length n give the same record.
- Alignment makes the n-tick record a prefix of the N-tick record.
- So one N-tick run in which the claim held proves it holds at every tick of every log of length at most N. That is a 1-safety property.

This is measured on a stand-in (`round2.py` §4), with read-once ports only, since version 0 has no per-tick values:
- §5.3 is FIXED for thrust.
- At each length, its 22 thrust values give one record. It holds through 50 ticks and is refuted at 51.
- When a thrust-dependent claim is moved inside the same tick, it masks §5.3 for thrust ≤ 0, and the analysis reads FLOWS. The coupling that R4 creates is seen.

How the fork treats DP-6's own examples:
- **LEN with no port** is the fork's example, not its counterexample. It can be grounded up to 16 ticks, where it holds for every log, and never beyond.
- **LEN with its port** FLOWS (y overflows at thrust 2^62), and the fork refuses it.
- **`b or not b`** FLOWS, so the fork loses it. That is incompleteness, not unsoundness.
- **"The text alone decides this only for the prefix"** is contradicted: FIXED is decided from the law alone.

The fork is DP-6's own remedy, "invariants proved and entered as typed terminals (fork 9)", with FIXED plus one run as the proof.
- **Repair to its statement:** the ledger line must name N and the receipt seal of the agreed N-tick run. Without that run, a short log could hide a later refutation.
- **Its one assumption:** it inherits FIXED's soundness, which is DECLARED relative to the rules, and assumes nothing else.
- **What it needs:** the owner's fork-9 ruling.

**(b) Is it worth building over the floor plus PREFIX? Not on this population.**

Measured (`round2.py` §2–3):
- PREFIX covers 0 of 107 pairs; FIXED covers 3.
- Those 3 are two copies of `We claim that true` (the court already marks it CONSTANT) and one claim that is never evaluated (UNREACHED).
- For grounding, the measured gain is nil.

What FIXED recovers that PREFIX cannot, on hand-written stand-ins only:
- **A claim after the port's declaration that no port reaches** (R6 row 4). PREFIX depends on declaration order: a law that declares its ports first, as R2's layout invites, has an empty prefix. FIXED contains PREFIX: in §7, both prefix claims read FIXED and the claim after the port FLOWS.
- **Every claim of a law whose port goes unused** (row 5).
- **Tick-block claims up to a horizon**, as in (a). PREFIX never grounds one.

On the survey's lessons:
- **Lesson 2** holds here. All 6 false positives come from refusals: they are claims made unreachable by an earlier claim that refutes for every value of the port.
- **Lesson 3:** I agree.

The case for building rests on the horizon alone. It is the only route to a grounded tick-block claim without testimony (R6 b) or a prover. The trigger is the first RUN-1 law whose owner asks for such a claim.

**(c) PSPACE and distributivity.**
- **What is hard.** The survey derives PSPACE-completeness from Godefroid & Yannakakis 2013, and it applies to exact noninterference. My "same solution" is the abstraction's: the meet over all paths of a label analysis whose facts are (location, port) pairs. That is an IFDS instance (Reps, Horwitz & Sagiv 1995): polynomial by summaries, sound, but not exact. The false positives are the gap.
- **Distributivity.** The problem stays distributive with refusals, alive and R9's operation count:
  - Every rule writes each location as a union of input labels plus constants.
  - Every choice (whether a refusal is possible, and the output, list and operation bounds) comes from the text, never from labels.
  - alive and the operation count are locations like any other.
- **Measured agreement.** A and B agree on the 73 unplanted claims, on all 361 planted cells, on the adversary's 7 laws, and on 4 procedure chains.
- **Cost.** A pays the hierarchical blowup that makes the exact problem hard: 131,090 statement visits at depth 16, against B's 16 summaries (§6). So B should be the certifier of record, and A should run under a step budget whose overflow reads as the floor.
- **The tension.** The refinements that would remove my false positives, intervals and constant propagation, are not distributive (Kam & Ullman). Adding them would end the theorem that the two methods agree.

**(d) Tokens: not now.** DP-17 applies: tokens are a port type, and nothing has failed for want of them.

The smallest version:
- RUN-1's port form gains `a token`. Measured: version 0 refuses the spelling as SYNTAX, as it does R2's forms.
- A token may be copied, and compared with another token by `equals` or `is not`, and nothing else: no lists, no literals, no printing.
- The door writes a token as an opaque identifier.
- The check over B_k runs is display only.

Proposed admission record:
- **Trigger:** a RUN-1 law whose ports carry identities (players, entities), and whose owner wants a claim checked over all assignments.
- **Discriminator:**
  - COMPAT-0 HELD;
  - the four kind-check plants refused (4 of 4 here);
  - 0 differences within an equality pattern on the fixtures (0 of 1,005 runs here), with the law's own literals in the sampler;
  - a printed token refused.
- **Scope:** sema, the door, SPEC §15, and RUNTIME-SPEC's encoding.
- **Exit:** the self-test green twice, byte-identical.

## 3. The narrowest version

- **Item 1, R6 repaired:** identical to mine.
- **Item 3, R4 in the court:** identical. I withdraw the suggestion that my verdict bears on OMIT.
- **Item 4, DOPPLER-0:** my search is that instrument. I add two things, both shown above:
  - Domains must hold the type's extremes: LEN shifts only at values like 2^62.
  - A FLOWS verdict tells the prosecutor where to look: MAGIC shows no shift in either side's domain.
- **Item 2, PREFIX:**
  - FIXED contains PREFIX and goes further.
  - The difference costs two derivations, 1,321 lines, whose soundness is DECLARED relative to their rules. PREFIX is decided by clause order and is sound by construction.
  - On the population, the difference buys nothing. I would build PREFIX now, and the analysis on the horizon trigger.

## 4. Corrections to round 1

1. "The instrument recovers 3": those 3 are worthless for grounding (see 2b).
2. "My verdict's R tracks that refusal" (DP-5): it does not repair OMIT.
3. Decidability and cost: A is exponential in procedure depth; only B is polynomial.
4. Inside a tick block, "FIXED BY THE LAW" should read "fixed by the law and the length".
5. The fork's statement lacked the N-tick run's receipt in the ledger line.
6. fall.orl's "513 bits" counted its constants.
