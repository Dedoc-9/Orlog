# Debate record: the proponent's design for the doppler, round 1 (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the adversary's prosecution and the
prior-art survey. Its probe is in `work/doppler-probe/` (ignored by git); its MEASURED lines are this host's.

---

# The doppler, redesigned: FIXED BY THE LAW (proponent)

The tree is at 3417949. The untracked files in research/doppler/ are not mine, and no tracked file changed. The probe is `work/doppler-probe/`, which git ignores: 2,521 lines, standard library only, importing `src/`. MEASURED means run on this host: Windows 11, CPython 3.14.5, `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`. `python -B work/doppler-probe/run_all.py` reruns all seven parts and writes their output to `work/doppler-probe/out/`; each part also runs alone as `python -B work/doppler-probe/<part>.py`. Two full runs were byte-identical except for the two lines that print software timings.

## The answer

Yes, by inverting the pasted design. A search cannot certify that a dependence is absent. A static analysis can, soundly, if it tracks every way a port can change which evaluations exist. So the certifier here is a refusal-sensitive dependence analysis, computed twice by two different methods, and the doppler becomes its prosecutor.

The payoff is a theorem, not a domain. For a claim the analysis reads FIXED, every log of a given length gives the same record. One run therefore settles what a search would need |D|^(ports×ticks) runs to sample, and it settles it for every log. That is the only ruthlessness on offer: soundness proved relative to a stated model of the semantics (that the model is interp.py's is DECLARED), and completeness measured, never claimed.

## 1. The design

**What a verdict certifies.** FIXED BY THE LAW, for claim k and port p, means: any two runs that differ only in p's values (and, in a tick block, have the same length) give k the same evaluation record. The record covers:
- whether k is evaluated at all;
- how many times;
- the truth of each evaluation, including where a refusal ends the run.

Certifying only the truth of each evaluation is unsound. A port that ends the run early (R4) hides a later false evaluation, and so raises the standing (R6 rows 2 and 3 below).

| verdict | reached by | licenses |
|---|---|---|
| FIXED BY THE LAW | derivations A and B both | before the tick block: the claim's ratification counts, as in v0. Inside it: display only, unless the owner takes the horizon fork |
| FLOWS FROM p | a dependence path in both A and B | nothing: the floor |
| SHIFTS WITH p | the search's witness: two values and the first divergent evaluation | nothing: the floor |
| DISPUTED | A and B differ | nothing; recorded as a finding |

Each word's natural reading is what it certifies. FIXED says the record is fixed by the law, not that the claim is true. SHIFTS says a shift was seen. There is no PORT-FREE and no ACCIDENTALLY-CONSTANT.

The licensed set contains the adversary's PREFIX: a claim before every port declaration is FIXED by construction. It adds two more cases:
- claims before the tick block that no port reaches (R6 row 4);
- laws whose ports go unused (R6 row 5).

**Channels.** These come from SPEC §3–§7 and interp.py. Each has one rule, and between them they carry 19 plants.
- **Data:** Let, Set, Increase, Say, conversions and promotions. A value's label is its operands' labels plus pc.
- **Control:**
  - If, Unless, Otherwise and else-if arms: each arm's pc includes every earlier condition.
  - While: a fixed point at the loop head.
  - For: both bounds, evaluated once.
- **Procedures:** inlined in the caller's state, so their writes to top-level variables are the caller's.
- **Rules:** a use reads every proviso and every value. It can refuse RULE-UNDEFINED or RULE-CONFLICT, which is decided statically from the provisos and the notwithstanding order.
- **Lists:** length and items are tracked separately. An index taints both the value read and the range check. Append writes at the current length, so the items take the length's label.
- **Text:**
  - A concatenation can refuse TEXT-TOO-LONG when its parts' longest prints pass 2^24. The longest prints are: int 20 bytes, fix 44, float 1077, text 2^24, list unbounded.
  - Say adds OUTPUT-TOO-LONG when the program's static output bound passes 2^30.
- **Refusals end the run (R4):**
  - An `alive` location collects the label of every possible refusal before a point, and is carried around loop back edges.
  - It covers overflow, division, conversion, index, size, rule, fuel, MUST-FAILED and CLAIM-REFUTED.
  - A claim's record reads pc, alive, its condition, and its condition's own refusal.
- **R9's budget:** one more location, the operation count.
  - Every tainted branch, loop count, short circuit and proviso feeds it, and it is checked at each statement.
  - The channel is closed when the static bound of counted operations is at most N.
  - Built in A only.

**Checking.**
- **Derivation A** walks the typed tree forward and inlines procedures.
- **Derivation B** reads only the law's bytes, the sealed text, with its own parser and type inference. It composes relational summaries bottom-up: a loop is a closure, and a procedure is summarized once. B imports nothing.
- **Agreement:** for a distributive problem the two methods compute the same solution, so any difference is a defect in one of them. FIXED needs both.
- **The search** then attacks every FIXED verdict; a witness against one is a CONTRADICTION. A witness is two logs, which any execution can rerun.
- **Limits:** one author wrote all three. A and B agreeing is consistency; only the search stands outside the rules, and only within its domain.

**R6.**
- **The floor:** the coarse rule is the case where nothing is FIXED.
- **The plug-in:** court.py is untouched. In a law with ports, a ledger line ratifying a claim's seal reaches `court.panel` only if that claim is FIXED for every declared port. The filter acts before the court's fixed point, so a FIXED claim with a shifting premise stays UNGROUNDED.
- **A repair to the floor:** the log's length is input even when there is no port. The analysis showed this, and the adversary's DP-4 reaches the same point. The trigger must read "declares any port or has a tick block".

**The length, and a fork.**
- **The problem:** inside the tick block, the log chooses the number of ticks. In the stand-in, a claim that holds for 50 ticks is refuted at 51 (MEASURED). So inside the tick block, FIXED licenses display only.
- **The fork:** a ratification line may name a horizon N. A FIXED claim's N-tick record is the same for every log, so one agreed run of N ticks, with any log, settles it for all of them.
- **The reading:** if the claim held over N ticks, it reads GROUNDED (up to N ticks) in every session of at most N ticks, and the floor applies beyond N.
- **The theorem:** independence is 2-safety and the invariant is 1-safety (Clarkson & Schneider 2010). Together they turn an exponential search into one run. This is argued; the length row measures its premise.

**Unused ports** cost nothing (MEASURED: the wind row), whereas the floor charges every claim for them. The analysis knows which ports reach no claim, so the door-level warning the first paste asked for comes free. No port is ever dropped from the log, because replay needs them all (DP-16).

**When it runs.** At admission, once per law seal and port signature, never per session: the verdict is a function of the law's bytes, which is all B reads. The search runs on demand and licenses nothing.

**Decidability and cost.**
- **The analysis** is decidable for every law: the label lattices are finite, loops are structured, and there is no recursion. Both derivations together took 0.027 s for all 49 texts (MEASURED).
- **The exact question at R9's bound** is also decidable, since it is finite. It costs |D|^(ports×ticks) runs of up to N operations each.
- **The search** took 26 s for 1,520 worlds (software timings).

**The second design's parts.**
- **PORT-FREE from search silence plus dynamic taint:** rejected. Dynamic taint misses branches not taken and runs cut short, and silence is not support.
- **PORT-REACHABLE:** survives, as SHIFTS.
- **Symmetry certificates, Noether and ACCIDENTALLY-CONSTANT:** see §5.

## 2. Theorems and prior art (none claimed new)

- **Noninterference:** Goguen & Meseguer 1982.
- **Implicit flows:** Denning 1976; Denning & Denning 1977.
- **Type-system soundness:** Volpano, Smith & Irvine 1996.
- **Flow-sensitivity:** Hunt & Sands 2006.
- **Termination-sensitivity:** Askarov, Hunt, Sabelfeld & Sands 2008. It is exact here, since every loop is bounded and every abnormal end is a refusal.
- **The backward slice** (Weiser 1981; fork 4) is the same analysis read backward.
- **MFP equals MOP for distributive problems:** Kam & Ullman 1977. Call strings and summaries agree: Sharir & Pnueli 1981.
- **Static worst-case bounds:** Wilhelm et al. 2008.

Soundness is DECLARED relative to the rules matching interp.py. The plants and the search are the evidence.

## 3. Measured

**A and B** (`agree.py`):
- 49 texts with claims: the 11 corpus programs and COMPAT-0's accepted texts.
- 73 claims and 107 (claim, port) pairs.
- A and B differ on 0 claims.

**Coverage** (`measure.py --list`), each candidate port taken alone:
- 3 FIXED, 104 FLOWS, 0 DISPUTED, 0 CONTRADICTION.
- The search witnessed 98 of the 104 flags.
- The other 6 are false positives, proven by hand. In plankton mutants 2127 and 2700, each of these claims follows a claim that refutes for every value of the port, so it is never evaluated.
- The corpus alone gives 19 pairs, all flagged and all witnessed. Counting distinct laws only: 44 pairs, 2 of them FIXED.
- 94 flags run through data or control. The other 10 run only through masking, where another claim's refutation ends the run first.
- So 9 pairs are independent: the 3 FIXED (no shift seen) and the 6 proven by hand. The floor recovers none of them; the instrument recovers 3.

**R6 rows** (`r6rows.py`):
1. r6's own claim FLOWS; thrust 6 refutes it at evaluation 17.
2. A claim that reads only the loop counter SHIFTS: thrust 2^62 overflows at tick 2, giving 1 evaluation instead of 20.
3. A second concern in the same loop is masked: 16 evaluations instead of 20.
4. A claim before any use of the port is FIXED. Ratified, it reads GROUNDED through court.py; under the floor it reads UNGROUNDED.
5. An unused port (wind) leaves the claim FIXED.
6. With the length as the port: 50 ticks hold, and the claim is refuted at 51.
7. A guarded port (|thrust| at most 1000, over 20 ticks) FLOWS with no shift. That is a false positive a range analysis would remove.

**R9** (`budget.py`, derivation A only):
- A claim after `If p is greater than 2, say "a"` is FIXED with no budget, and FLOWS at budget 4.
- R9 emulated at 4 refuses TICK-BUDGET at p 3 and completes at p 0.
- On the population, no FIXED pair is lost at N = 10 or N = 10^5.
- 40 of 41 static operation bounds are finite; the largest is 168,078.

## 4. Plants (`plants.py`)

There are nineteen plants, one per rule: then-pc, else-pc, while-pc, for-pc, perform-writes, rule-proviso, rule-refusal, list-length, list-index, list-items, text-data, arith-refusal, claim-masking, must-masking, list-size, text-size, output-size, fuel-refusal, and loop-alive (alive not carried around a loop back edge).

- **Fixtures:** each plant has one, whose target claim both A and B flag and the search witnesses.
- **The matrix:** in each derivation, the 19 × 19 matrix of plants against fixtures has 0 cells off the diagonal. Only its own plant lets a fixture pass.
- **Planted in one derivation:** each plant in A is caught by B (DISPUTED), and each plant in B is caught by A.
- **Planted in both:**
  - The search catches 18 of the 19.
  - It misses output-size: OUTPUT-TOO-LONG needs 2^30 bytes of output, and the search's cap is 64 MiB.
  - That is a declared blind spot of the shared rules, like the self-test's monitored negative.
- **The court plug-in's plant** filters the ledger after the fixed point instead of before. It reads a FIXED claim with a shifting premise as GROUNDED, and is caught.

## 5. The fourth paste: sealed equivariance, and the feature I would pioneer

**Sealed equivariance: change it.** Two of its ideas stay: generators rather than groups, and a standing refuter. Five parts go:
- **Exhaustive discharge.**
  - R9 bounds a tick's operations, not its states, and fall.orl's top-level state is 513 bits.
  - At this host's 34,000 to 38,500 reference ticks a second, the 2^64 states of a single integer take 1.5–1.7 × 10^7 years to enumerate (`equiv.py`).
- **Exactness.** fall.orl commutes bit for bit with 7 of 8 translations of x. The 8th refuses OVERFLOW at §12.5. In bounded arithmetic, translations are partial.
- **Noether**, measured. The quantity conserved under that very symmetry would be vx, which falls from 2.0 to 0.1758, because drag is dissipative. DOCTRINE T7 withdrew Noether once already.
- **Conservation as an independent check of the front end.**
  - Reading every `-` as `+` in leapfrog completes with different output, yet its momentum guard holds at every step and its reversibility claim stays true.
  - Reading `+` as `-` is caught, but by an index refusal, not by the guard.
- **"Rides the certificate channel, already groundable."** It does not.
  - Grounding needs a person's ratification of the claim's own seal (T1, T2), and a checker's result is computation.
  - Nor can a certificate computed from a law sit inside the bytes its seal hashes.

**By construction, not after the fact.** A symmetry can hold by typing (Reynolds' abstraction theorem, 1983). Give a value a kind whose only operations preserve a relation, and invariance becomes a theorem about every law the type checker accepts.
- **Permutations of opaque values:** in Ørlǫg's exact arithmetic this holds without caveat.
- **Translations:** they hold only up to overflow (above), so an affine kind needs declared ranges first.
- **Rotations and boosts:** they fail on a fixed-point grid. This is argued, not measured.

**The feature: tokens.** The spelling is `Let player be given as a token.`, in R2's port form, and "token" is reserved nowhere else. A token can be copied, and compared with another token by `equals` or `is not`. Nothing else is allowed: no arithmetic, ordering, printing, concatenation, conversion or literal. These are Ip & Dill's scalarsets, from Murφ.

- **What it entails:** a sema rule that refuses TYPE for any other use, and tokens carried in the log as opaque identifiers.
- **What it decides:**
  - For k read-once token ports, B_k runs (the Bell number: 5 for 3 ports) decide exactly whether a claim's record depends on them.
  - A bounded search's silence becomes support here, because the bound is a theorem about the type, not a choice.
  - FIXED-BY-KIND licenses what FIXED does.
- **What it does for later automorphism work:**
  - Every accepted law carries the symmetric group on its tokens by construction.
  - A log's canonical form is first-occurrence renaming, in linear time.
  - So sessions can be cached per orbit, a law can be quotiented before any search, and the kinds can be given to nauty-style tools as their initial colouring.
- **Not solved:** each-tick token ports cost B_{k·n} runs.
- **Theorem:** data independence (Wolper 1986) for the equality-only algebra; also Lazić 1999 and Emerson & Sistla 1996. Every run commutes with every permutation of token values, so a claim's record depends only on the ports' equality pattern.
- **Falsifier:** two logs with the same equality pattern and different records.
- **Probe** (`kind.py`): version 0 Int ports are designated as tokens, and the kind is checked on the tree.
  - In a pass-the-token law, "holder equals a or b or c" FLOWS for the static analysis and is FIXED-BY-KIND over the 5 patterns.
  - Of 1,005 runs, 0 differ within their pattern. "Holder equals a" shifts between patterns.
  - Four kind-check plants (ordering, arithmetic, an integer literal, concatenation) are each refused by the correct check and caught by within-pattern samples.
  - The literal plant is caught only because the sampler draws the law's own literals.
- **Instead of R13 as pasted:** a port may be declared a token, under the falsifier above. Nothing is sealed and nothing is exhaustive.

## 6. Where I expect the attack

1. **"Nearly the coarse rule again" (DP-2).** On this population, yes: 3 of 107 pairs. But only 9 pairs are independent at all, the population is small (44 distinct-law pairs) and single-concern, and RUN-1's multi-concern laws are NOT_MEASURED.
2. **The rules' fidelity to the interpreter.** One author wrote A, B, the plants and the reading of the semantics. A channel absent from both derivations is invisible to the plants by construction. Only the search stands outside the rules, and it is bounded.
3. **B shares the front end.** It reads sema's law bytes, so a front-end defect changes the law for both derivations, as it changes the seal.
4. **The horizon fork** adds a field to the ledger line. That is fork 9's territory, and the owner's call.
5. **Tokens suit identities, not quantities,** so they may model few RUN-1 ports.
6. **DP-5, orthogonal to this design.** The receipt omits an evaluation that refused mid-condition, so the court reads "true in 16 of 16". My verdict's R label tracks that refusal, but the court still needs R4's repair.
