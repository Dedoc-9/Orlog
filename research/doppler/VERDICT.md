# Verdict: the doppler, and what does better (2026-10-26)

The judge's verdict on the owner's question of 2026-10-26, "what if we add something like a doppler that rules out non
completeness as ruthlessly as sha256?", and on the four texts he pasted with it (PROPOSAL.md). It weighs three things:
- two rounds between a proponent, who designed an alternative and built a probe, and an adversary, who attacked the
  pastes and then the design (PROPONENT.md and PROPONENT-R2.md; ADVERSARY.md and ADVERSARY-R2.md);
- a prior-art survey made with real searches, every source graded by how it was read (RESEARCH.md);
- the judge's own reruns.

All are saved verbatim beside this file. This verdict is model output, like them, and admits nothing. The debaters'
scripts sit in `work/` folders that git ignores, so from this tree their figures are OBSERVED. The judge reran the two
that decide the most:
- the adversary's round-2 fixtures;
- the court defect DP-5, against the court as built.

## The answer: yes, but not with a doppler

**Nothing rules out incompleteness.** For Ørlǫg, whether a claim depends on an input is decidable, because runs are
total and every value is bounded. The pasted "cannot exist" is wrong here. But it is expensive:
- coNP-complete for straight-line code (Yasuoka & Terauchi 2010);
- PSPACE-complete with procedures, a bound the survey derived itself and found in no publication.

So any cheap instrument is incomplete. What can be had is SHA-256's *structure*, on each side of the question:
- **Dependence** is proved by a witness: two logs and the first evaluation where the claim's record differs. Anyone can
  replay it. A doppler finds such witnesses.
- **Independence** is proved by a sound static analysis whose verdict comes from the law's text alone and is
  recomputed by a second derivation. A search cannot prove it. The adversary built one law whose dependence fires at a
  single value of thrust out of 2^64; a 2,001-value search finds it with probability about 1e-16. The analysis flagged
  it from the text.
- **What remains**, a path in the analysis with no witness found, is the incompleteness. It is named, counted and open
  to attack from both sides: a witness makes it a dependence, and a finer analysis can show it is none.

So the better design inverts the pasted one. A refusal-sensitive dependence analysis, computed twice by two methods,
certifies; the doppler only prosecutes. **Measured** in the proponent's probe, then rerun against it by the adversary:
- the two derivations agree on all 107 claim-and-port pairs of the corpus and COMPAT-0's accepted texts;
- each catches all 19 rules planted wrong in the other;
- both flag every one of the adversary's seven trap laws, the 2^64 needle among them.

**What it does not yet buy: grounding.** On the measured population it certifies 3 of 107 pairs, and all 3 are
worthless for grounding: two copies of `We claim that true` and one claim that is never evaluated. Both sides now agree
on what to build:
- a narrow licence now, once RUN-1 exists;
- the analysis only when a RUN-1 law's owner asks for a grounded claim the narrow licence cannot reach.

## What the debate established

| result | found by | judge |
|---|---|---|
| The pasted lattice grants PORT-FREE from a bounded search plus dynamic taint. Six built laws read PORT-FREE and GROUNDED over one log and are refuted over another; "UNKNOWN never reads GROUNDED" saves nothing, because each failure reads PORT-FREE | adversary DP-1 | conceded by the proponent |
| Dynamic taint is not "sound for the observed run": it never sees a branch not taken, and it is incomparable with noninterference (Schoepe et al. 2016) | adversary DP-3; survey lesson 3 | conceded |
| Refusals and evaluation counts are a channel. A port that ends a run early (R4) hides a later false evaluation, so a design that certifies only "the truth per evaluation" is unsound (Askarov et al. 2008) | both | conceded; the proponent's analysis tracks it |
| Checking a symmetry "exhaustively over the R9-bounded state space" cannot be done. R9 bounds operations per tick, not states: one integer and one integer port make 2^128 cases. Overflow makes translations partial, and Q31.32 rounding breaks scaling | adversary DP-8; proponent; survey (b8, b9) | measured by both |
| Orbits do not collapse a universal. Invariance makes a claim constant on each orbit, and independence needs it constant across orbits: at least \|logs\|/\|G\| checks | adversary DP-9; survey | conceded |
| Noether does not apply. fall.orl is translation-equivariant while friction takes vx from 2.0 to 0.1758, and leapfrog's energy drifts. A conservation guard caught the shared-front-end plant only where the plant rewrote the guard itself; one planted leapfrog completed with wrong output, all four executions agreeing. T7's "Newton's third law, not Noether" stands (Marsden & West 2001) | adversary DP-10, DP-11; proponent; survey lesson 6 | measured by both |
| Sealed equivariance fails four ways. A certificate inside the seal of the law it certifies needs a SHA-256 fixed point. Imported by name, it repeats L4's name-keyed ratification. Its falsifier cannot fire, since every Ørlǫg domain is bounded. "No language" is contradicted by Murφ's scalarsets (1993), UPPAAL, Essence, TLC and parametricity | adversary DP-14, DP-15; survey (d) | conceded |
| "Log only the ports that matter" breaks RUN-1's Replay theorem: a port wrongly judged free would be read without being logged | adversary DP-16 | conceded; no port is ever dropped |
| A refusal-sensitive static analysis flags every trap law, including the one no search finds; two derivations agree, and cross-catch 19 plants each | proponent; rerun by the adversary | judge reran the adversary's fixtures: confirmed |
| Coverage on the population: 3 of 107 pairs certified, none useful for grounding; 98 of 104 flags witnessed, 6 proven false positives | proponent rounds 1 and 2 | conceded by the proponent |
| Two derivations by one author show consistency, and diversity of code paths within one rule table, not that the table is complete. A rule both lack is invisible to both: the cost fields (N-2) | adversary (c) | the judge agrees (T11) |

## Found against what is already built, or already written

These are the debate's most useful results, and none of them is about the doppler.

1. **DP-5, a defect in the court as built (version 0).** A claim whose evaluation refuses partway through its own
   condition is not counted. It reads "true in 16 of 16 evaluations", WELL-FOUNDED and, with its seal ratified,
   GROUNDED, though the run is REFUSED at that claim.
   - **Reproduced by the judge** on the current tree: `§2.1 We claim that item i of xs equals 1, by the owner.` inside
     a loop to 17 over a 16-item list.
   - **Both sides agree on the repair:** the court names the evaluation that refused, and does not count the claim as
     held.
   - **It can be made in the court alone.** The receipt's status line names the refusing clause, and a claim clause
     refusing with any code but CLAIM-REFUTED marks an evaluation that refused. Receipts then stay unchanged, and
     COMPAT-0 holds.
   - **The inline case:** a claim inline in an If arm, whose clause also evaluates the arm's condition, is withheld
     conservatively. That is sound, and incomplete.
2. **DP-4, against R6 as amended.** A tick block with no port still takes input, because the log's length sets how many
   ticks run. "Declares any port" misses it. The trigger must be **any input log: a port or a tick block.**
3. **N-1, against any licence by position.** A claim inside a procedure stands textually before the tick block but
   runs during it. In the adversary's fixture, judge-rerun, it reads GROUNDED over 16 ticks and is refuted at 17. A
   licence must be decided **by evaluation:** every evaluation of the claim precedes the first tick.
4. **N-2, against any certificate narrower than the court's claim line.** A certificate claim certified port-free by
   both derivations still flips between NOT CHEAPER and CHEAPER with the input, as judge-rerun:
   - receipt `claim 0 6 1 1 1 4 1` at thrust 0;
   - receipt `claim 0 6 1 1 1 4 11` at thrust 5.

   What a licence covers must be the **whole claim line**: evaluations, trues, cost, and the certified clause's cost.

## Decisions on what remained open

1. **The words are the adversary's.** "FIXED BY THE LAW" reads as settled or true; "FLOWS FROM p" reads as "depends
   on", and that is false for the six proven false positives. The verdicts read:
   - `NO PATH FROM <p> (A, B)` / `PATH FROM <p>` / `A AND B DIFFER`
   - `SHIFTS WITH <p>: <a> → <b>, claim line <x> → <y>, evaluation <n>`
   - `GROUNDED (no path from any port; §k is evaluated before the first tick)`
   - `UNGROUNDED (rests on input log <seal>, unratified: R6)`
   - `REFUSED at evaluation <n> (<CODE>): not held`

   None is a new grounding state; grounding stays binary. There is no PORT-FREE, ACCIDENTALLY-CONSTANT or SYMMETRY in
   any court output.
2. **The licence, once RUN-1 exists** (the adversary's revised item 2, which the proponent's design contains): a claim
   with no path from any port in both derivations, every evaluation before the first tick, its whole claim line
   covered. PREFIX, decided by clause order, is the cheap first form of it. It is sound only with N-1's condition:
   evaluated before the first tick, not merely written before it.
3. **The horizon fork is deferred, not rejected.** Both sides now agree it is sound in principle. A claim certified
   independent at length N, plus one agreed N-tick run in which it held, holds at every tick of every log up to N.
   That is the invariant DP-6 asks for, bounded at N. It waits on four things:
   - R9's channel in the second derivation (N-3);
   - each-tick ports, measured (N-4);
   - a premise rule for horizons (N-5);
   - the owner's fork-9 ruling, since the ledger line would name N and the N-tick run's receipt.
4. **The doppler is an instrument, DOPPLER-0, for prosecutors.**
   - It compares whole claim lines over a sealed domain of port values and lengths, and its domains must hold the
     type's extremes.
   - It re-runs each shift on four executions.
   - It writes neither court nor ledger, and licenses nothing.
   - It is admitted only on a trigger.
5. **When to build.** Nothing here is built before RUN-1's first commit (DP-17): there is no port to analyse. DP-5's
   repair is the exception, because it is a defect in the court today.

## The owner's other question: one feature to pioneer now for automorphisms

His question: "what is one feature we can pioneer here now that will streamline Computing automorphism groups later?
be ambitious". The pasted answer, sealed equivariance, fails as shown above.

**What survives both rounds: tokens.** A token is a port type whose values can be copied and compared with `equals` or
`is not`, and nothing else: no arithmetic, ordering, printing, concatenation or literal. These are Ip & Dill's
scalarsets, from the Murφ model checker (1993). It is not new, and was not claimed new.
- **Symmetry by construction.** Every law the type checker accepts commutes with every permutation of token values
  (Wolper 1986, data independence). The symmetry is a theorem about the language, never a check on one law.
- **What it buys for automorphism work:**
  - for k read-once token ports, B_k runs (the Bell number: 5 for 3 ports) decide exactly whether a claim's record
    depends on them;
  - a log's canonical form is first-occurrence renaming, in linear time;
  - claim records can be cached per orbit;
  - the kinds can seed nauty-style tools as their initial colouring.
  - Measured in the proponent's probe: 0 differences within an equality pattern over 1,005 runs, and four kind-check
    plants refused.
- **Its limits** (adversary, judge-rerun):
  - it holds for claim records, not for sessions: two assignments with one equality pattern give equal claim lines
    and different trace heads;
  - it needs a value tag in the event encoding, a definition of a token's identity as exact bytes after the door, and
    a twin round;
  - tokens suit identities (players, entities), not quantities;
  - each-tick tokens cost B_{k·n} runs.
- **When:** with RUN-1's port types, on a trigger: a law whose ports carry identities and whose owner wants a claim
  checked over every assignment. The proponent's proposed admission record is in PROPONENT-R2.md §2(d).

## Acceptance, if any of this is built

Each plant must be caught by the row it breaks:
- **DP-5:** the OMIT fixture reads `REFUSED at evaluation 17`, not GROUNDED. Plant: today's tally.
- **DP-4:** a law with a tick block and no port, its claim's seal ratified, reads UNGROUNDED. Plant: R6's present
  trigger.
- **N-1:** a claim inside a procedure performed in the tick block reads UNGROUNDED. Plant: licensing by clause position.
  And a claim before every port declaration, in a procedure performed after a port is used, reads PATH. Plant: "before
  every port declaration is enough".
- **N-2:** a certificate claim's licensed line is byte-identical across port values, or it reads PATH. Plant: a record
  without the certified clause's cost.
- **The trap laws:** the seven read PATH in both derivations. The 2^64 needle stays NO SHIFT under any feasible
  search, kept as a monitored negative and never counted as a pass.
- **No new words:** no court output contains PORT-FREE, ACCIDENTALLY-CONSTANT or SYMMETRY, and a DOPPLER-0 run leaves
  the court's output and the ledger's sha256 unchanged.

## What this verdict does not show

- **That the analysis is sound.** Soundness is DECLARED relative to its rule table, and one model family wrote the
  table, both derivations, the plants and the fixtures. N-2 shows a rule both derivations lacked.
- **That it helps on RUN-1's real laws.** Each-tick ports and multi-concern laws are NOT_MEASURED.
- **Novelty.** Every mechanism is prior art. The survey's NOT FOUND items are absence of evidence:
  - grounding withheld for a dependence on input and restored by a checked independence certificate;
  - bounded, refusal-sensitive noninterference over tick logs;
  - a published PSPACE bound for noninterference of recursion-free programs.
