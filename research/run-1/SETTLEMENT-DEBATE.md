# What replaces the reason we built CUT-0: the successor, the rule's identity, and the stratified court (2026-10-26, late)

**Status: research. Ruled since, 2026-10-26: E2 as HELD's meaning for version 1, and option (d), the meet pinned to
CUT-0's digest (`RULINGS.md`, the claims ruling).** The owner asked: *"If CUT-0's a research only candidate then what replaces why
we started out building it?"* Then: *"Debate that design."*

He forwarded eight outside texts, paraphrased here, never quoted:
1. the reviewer's answer: R8 admitted, CUT-0 research-only;
2. its reversal: CUT-0 the target, with R8 a temporary baseline;
3. a debate concluding in three statuses (admitted, target, research candidate), with a claimed defect in the
   selector witness;
4. six ideas treating the settlement rule as auditable state;
5. a review of those six;
6. a stratified court (K0, K1, K2), with monotone composition by meet and self-application;
7. a review of the stratified court;
8. an eight-week build plan, and its review, with a K0 manifest draft.

The measurements are `probes/meet_probe.py` (output `evidence/run1-meet.txt`) and the repaired `probes/cut0_schema.py`
(output `evidence/run1-cut0-schema.txt`). Each was run twice, byte-identical.

## 1. Why CUT-0 was built, from the record

R8 (E1) holds a claim when every completed evaluation was true. C2 shows the failure. A loop is refused at pass 17 of
20, and its claim was true in 17 of 17 evaluations. R8 holds it, although the three passes cut off would have
evaluated it again (`evidence/run1-cut0-claims.txt`). In version 1 the same happens to every claim of the tick block,
which is Round D's F19. R6 a keeps those claims from GROUNDED, but they still read HELD.

**That is the problem, and both forwarded answers leave it in place.**
- Under "research-only", R8 settles every version-1 run indefinitely.
- Under "target", R8 settles every version-1 run until T10 is proved or waived.

Either way, every interrupted claim reads HELD for as long as the proof takes.

## 2. The answer proposed here: admit the meet now

**The meet:** a claim is held when R8 holds it **and** CUT-0 holds it.

| property | grade | why |
|---|---|---|
| never looser than R8 in what it holds | ESTABLISHED | by definition: a conjunction |
| never looser than R8 in what it supports | ESTABLISHED (T8) and MEASURED | support is the court's least fixed point over the held claims, monotone in them. T8, *withholding never raises a standing*, is proved in `ROUNDS.md` and checked exhaustively up to three claims. T13 already derives R8's and CUT-0's one-sidedness from it, and the meet's follows the same way. The probe measures it again on every run: 0 claims supported above R8 |
| needs no T10 | ESTABLISHED | T10 is the claim that CUT-0 withholds *enough* (K̂ ⊇ K). If T10 failed, the meet would fail to tighten somewhere. It could never hold or support above R8 |
| delivers what CUT-0 was built for | MEASURED | **TIGHTER 43,356**: claims R8 holds and CUT-0 withholds, over 79,520 refused runs and 192,894 claims. The frozen corpus and the cases give 10 of 45 claims, family E 34,523 of 110,476, family G 8,823 of 82,373. **The count does not tell a justified tightening from CUT-0's conservatism.** In a justified one, the run's continuation really evaluates the claim again, as in C2. In a conservative one, K̂ covers a pass that cannot reach the claim, as in D08. The resumption oracle (`manifold/resume_oracle.py`) can split them. *Run since: §7. 1,968 refuted, 40,141 confirmed, 1,247 unreached* |
| forgoes only CUT-0's gains | MEASURED | **LOOSER 7**: claims CUT-0 holds and R8 withholds. Two are A23's and A23′'s, the cases built to show a gain, and five are in family G; there are none in the frozen corpus or in family E. These are the only readings that rest on the cut's correctness beyond withholding |
| a forged or wrong cut gains nothing over R8 | ESTABLISHED | R8 reads the receipt's status and claim lines (`court.py` 245–247), never the cut. A forged cut can move a claim between withheld and R8's own level, and never above it. This bounds the schema's boundary (`CUT-SCHEMA.md` §3: 14 of 15 accepted single-byte mutations change a standing) by the status quo |

**What it costs:**
- The cut must be recorded. That is needed under every option already.
- CUT-0's code enters the admitted path, but only its withholdings take effect.
- A defect in CUT-0 can wrongly withhold, and nothing worse. Each such withholding shows as TIGHTER against R8, and the
  comparison lists it.
- Over-withholding costs precision. D08 is withheld "conservative by design": a claim E2 would hold, which the meet
  withholds.

**What it does not give:** the meet's claim to E2 itself. Held under the meet implies held under R8, always. It
implies held under E2 only if T10 holds. So admitting the meet changes what HELD means in version 1: R8's held,
less what the cut's continuation could evaluate again. That meaning is the owner's to rule. It is a smaller ruling
than E2, because it promises E1 tightened, not E2 reached.

**Prior art:** the meet of two sound approximations is sound (abstract interpretation's product of domains). No
mechanism is claimed as new.

**The options, now four:**

| option | 1a admits | interrupted claims in version 1 | admitted above R8, resting on the cut and T10 |
|---|---|---|---|
| (a) CUT-0 admitted, debt named | CUT-0 | withheld | CUT-0's gains (7 here) |
| (b) T10 proved first | R8 until then | **HELD** until the proof | nothing |
| (c) the fork | R8; CUT-0 an experiment | **HELD** until a later ruling | nothing |
| **(d) the meet, CUT-0 the target** (recommended) | R8 ∧ CUT-0, with its rule digest | withheld wherever CUT-0 withholds | **nothing.** The later step, replacing the meet by CUT-0, changes LOOSER claims alone, so its transition record is one delta class |

Under (d) the three statuses of text 3 are kept:
- the meet is admitted;
- CUT-0 alone is the target, admitted only by the owner's ruling, with T10 proved or explicitly waived;
- nothing is promoted by deadline or by a count of passing runs.

## 3. The selector witness (text 3's Attack B)

The reviewer read the earlier evidence correctly. The plant left the selector in the bytes, and the decoder ignored it.

The conclusion drawn from it does not follow. A decoder that does not read the selector, deciding otherwise than one
that does, is what dependence on the selector means. The claim stood; the presentation was uneven with the other three
rows.

**Repaired anyway:**
- the plant now writes only "an inline statement" (the first inline arm's index);
- A23's payload changes from `…0001` to `…0000`, and its claims 0 and 1 swap standing;
- the probe now counts a witness only when the bytes lack the field **and** a standing flips.

Rerun twice, byte-identical: `CUT SCHEMA DRAFT 2 HELD`, with 4 of 4 fields witnessed by payloads that differ, and
every other line as before.

## 4. The six ideas on the settlement rule as auditable state (texts 4 and 5)

| idea | disposition | grounded in |
|---|---|---|
| a rule digest | **in the reading, not the receipt core**, as text 5 says. It is already there in substance: the court returns its rules with every reading (`court.py` 361), and `FORK.md` §1 puts the rule set's digest beside the core digest. **On identity:** byte identity, not "semantic" identity. The semantic identity of code is undecidable in general. Verðandi pins every source of its trusted base by sha256 (`RSN_SOURCES`, 58 files): any change, even to a comment, turns its fences red until an amendment names it. That is decidable, and measured in use. Proposed: the digest of the court's import closure (`court`, `sema`, `syntax`, `numeric_ref`, `seal`: 5 files, 2,307 lines) and its settlement parameter. A comment change is an amendment, never hidden by a canonicalization | Verðandi's `AGENTS.md` §3; `FORK.md` |
| a settlement lattice | **a graph of rules; a lattice only for the held bit.** Per claim, held is a boolean ordered withheld < held, and the meet is the conjunction. That is the one place a meet is defined and provably safe here, and it gives option (d). Comparisons of whole rules stay partial (TIGHTER, LOOSER, MIXED, UNCHANGED) | §2 |
| a settlement oracle | **exists:** the resumption oracle, both adversaries and the frozen register. It never promotes, and a count of passing runs is never a proof. Text 4's sample report figures are illustrations, not measurements | `manifold/VERDICT.md`; `CUT-SCHEMA.md` (the seams) |
| per-claim election | **rejected in principle, not just deferred.** It lets a claim's author choose the rule that judges the claim: the judged choosing the judge. The scorer must not be selectable by what it scores. It would also change the law's seal and SPEC | DOCTRINE (a generator is never its own sole verifier) |
| meta-grounding | **exists as the theorem ledger** (T1–T17: proved, argued, measured, conjectured). GROUNDED is never used for a rule. In Orlog, GROUNDED means a ledger line ratifies a claim's own seal (`court.py`), which is testimony. Text 4's table calls R8 GROUNDED with "T11 proved for base cases": T11 is open, owed as a proof over SPEC §13's phase table | `ROUNDS.md`, the theorem ledger |
| a retroactive audit | **exists as the versioned history and appeals.** Text 4's figures are illustrations. Its "R8→UNGROUNDED" conflates held with grounded | `CUT-SCHEMA.md` (the seams) |

## 5. The stratified court (texts 6 to 8)

**What it gets right: its three interfaces.**
- a seal bound by digest, never by name;
- a refusal preserved, never laundered across a layer;
- a closed amendment path.

These restate rules the record already keeps: the session record's binding, the cut, and the append-only ledger.

**Adversarial findings:**

| | finding | grade |
|---|---|---|
| S-1 | **K0 is not smaller than the court.** A settlement reading depends on the front end, the interpreter and the court: 8 modules, 3,088 lines. A K1 law would run on the interpreter (1,744 lines with its imports), the same interpreter whose runs it settles. The trusted base is unchanged, and a layer is added above it | MEASURED (the import closures) |
| S-2 | **The rule does not fit the language.** CUT-0's K̂ is a reachability over the law's syntax tree, with procedures memoized. Version 0 has no trees and no recursion, and its claims are boolean conditions over the law's own state. A K1 law would be a meta-interpreter over a flattened tree, in bounded loops. Text 8's week-4 abort is likely to fire | DECLARED (a prediction) |
| S-3 | **Self-application, as written, is vacuous or contradicts grounding.** "This rule is sound" is no Orlog condition. It could only be an owner-oracle claim, and the owner's ledger can ratify any claim's seal, which makes it GROUNDED. So "must never read GROUNDED" either forbids his ratification (a new rule) or tests nothing. The record has also withdrawn an answer to Löb: a self-soundness milestone walks back into that ground | ESTABLISHED (`court.py`'s grounding); the record's withdrawals |
| S-4 | **Signatures need a dependency.** Python's standard library offers hashes and HMAC, and no general signature verification, and `AGENTS.md` forbids dependencies. The owner's authority is already recorded: his rulings quoted verbatim in `RULINGS.md`, in commits he makes and pushes | ESTABLISHED |
| S-5 | **The meet algebra** is proved where the order is a boolean per claim (§2), and unproved anywhere else, as text 7 says | — |

**What to take from it:**
- **The pinned trusted base and its amendment chain.** Verðandi runs them already (`RSN_SOURCES`, `RSN_CHAIN`, the
  fences). Its RUNG-0 computes a change's rung from its closure, and `TRANSFER.md` lists it for Orlog.
- **The "primitive-boundary inventory" text 8's review asks for first is the import closure,** measured here: 8 modules.

Proposed: port Verðandi's pinning as the settlement identity. Do not write the rule as a law.

## 6. Consensus

| question | consensus |
|---|---|
| what replaces the reason CUT-0 was built | **nothing should.** Admit the meet: CUT-0's tightening now, its gains when T10 is proved or waived (option (d)) |
| research candidate, target, admitted | the three statuses are accepted. Under (d) the meet is admitted and CUT-0 alone is the target. The step between them changes LOOSER claims only |
| the selector witness | repaired. The claim stood; the presentation did not |
| the rule's identity | a digest in the reading, of the court's source closure, pinned as Verðandi pins: any change an amendment |
| per-claim election | rejected in principle |
| meta-grounding | the theorem ledger; never GROUNDED for a rule |
| stratification | not now. Take its interfaces and Verðandi's pinning. The rule as a law fails on S-1 to S-4 |

**Does not show:**
- version 1's numbers for the tick block, which are DECLARED until version 1 runs;
- the meet's claim to E2, which is T10's;
- how many of the 43,356 tightenings are justified and how many are conservative. *Measured since, in §7.* The
  families are the manifold proponent's grammar and seed, not a sample of real laws;
- that over-withholding is harmless: the D08-type withholdings cost precision;
- any cost of the stratified court, which is unmeasured.

## 7. The critique of (d), and the measurement it asked for (2026-10-26, later)

The owner forwarded four more texts, paraphrased here, never quoted:
1. the reviewer adopting (d);
2. a critique of it: shared mistakes survive a meet; the admitted rule would be coupled to a moving artifact; a
   digest-pinned defeater set should replace it; and the 43,356 should be measured first;
3. the reviewer withdrawing (d) to wait for that measurement;
4. a pattern-first alternative (fix the structural causes, register outliers as defeaters). The reviewer asked of it:
   independent dimensions rather than one bucket per claim, and a split between missing evidence, inadequate policy
   and over-withholding.

Every text asks for one measurement first. It is made: `probes/disagree_probe.py`, with output in
`evidence/run1-disagree.txt`, twice byte-identical.

### The measurement

Each disagreeing claim's run is resumed by the manifold debate's oracle. The refusing operation returns each of eight
values, and the reference's own code goes on, under Rinf (every later refusal returns too: reading S2) and under R1 (a
later refusal ends it). That is CUT-0's own counterfactual: the same law, inputs and code, with only the refusing
operation's result supplied. Each claim is classed:
- **REFUTED:** evaluated again, and false in some resumption;
- **CONFIRMED:** evaluated again, and true in every resumption that evaluated it;
- **UNREACHED:** evaluated again in no resumption tried;
- **UNRESOLVED or UNMODELLED:** none occurred.

| R8 holds, CUT-0 withholds (TIGHTER), under Rinf | claims | REFUTED | CONFIRMED | UNREACHED |
|---|---|---|---|---|
| the cases, the frozen texts, the fixtures, the examples | 10 | 4 | 5 | 1 |
| family E | 34,523 | 0 | 34,523 | 0 |
| family G | 8,823 | 1,964 | 5,613 | 1,246 |
| **all** | **43,356** | **1,968 (4.5%)** | **40,141 (92.6%)** | **1,247 (2.9%)** |
| all but family E, whose only claim (`x is at least 0`, x never falling) cannot be false | 8,833 | 1,968 (22.3%) | 5,618 (63.6%) | 1,247 (14.1%) |
| the same, under R1 | 8,833 | 615 | 4,443 | 3,775 |

**CUT-0's 7 gains (LOOSER) are all UNREACHED:** no resumption evaluates them again, so the oracle agrees with each.

**What it says:**
1. **The feared outcome did not happen.** The critique feared that the tightenings were mostly conservatism.
   Conservatism (UNREACHED) is 2.9% of them, and 14.1% with family E set aside.
2. **R8 is contradicted outright for 1,968 claims.** Each was evaluated again past the cut and found false in some
   resumption. There, R8's HELD is wrong under any reading that looks past the refusal.
3. **The largest share is a question of meaning, not of evidence.** These are the CONFIRMED claims: 92.6%, and 63.6%
   without family E. They had evaluations still to make, and every resumption that made them found them true. E1
   holds them, as true so far. E2 withholds them, as not finished. No measurement decides this. It is what HELD means,
   and it is the owner's.
4. **Reading S2 has a visible price.** Under R1, family G's UNREACHED rises from 1,246 to 3,773. Reading every later
   refusal as passable is the F1 repair (`CUT-0.md` §2): it is sound, and it costs precision.

### The causes: the patterns are CUT-0's rows

Every disagreement is held by one or more of five parts of K̂, and each part is a row of `CUT-0.md` §2's table. The
tagged continuation equals the probe's on every run, so nothing falls outside them.

Family G, by the part that alone holds a claim (removing that part would release it):

| part of K̂ | claims held | held by it alone | of those, UNREACHED |
|---|---|---|---|
| the loop's own clause refused (the C6 repair) | 4,601 | 3,435 | 312 (9.1%) |
| a For's next pass | 2,445 | 1,231 | 88 (7.1%) |
| a While's next pass | 2,311 | 803 | **450 (56.0%)** |
| the rest of a block | 2,137 | 739 | 159 (21.5%) |
| the refused If's arms onward | 191 | 52 | 5 (9.6%) |

- **The While row carries the conservatism.** That row is S2's reading of a While: its condition unknown, its fuel
  check passable. `CUT-0.md` names "a While's condition" first among the places where K̂ exceeds K.
- **The For row's residue is 7.1%.** Its bit is exact. What is left is arms that cannot reach the claim by value,
  D08's kind.
- **The loop's own clause refused holds the most claims** in both families. Family E has 33,212 of its 34,523 there.

The pattern-first text's own table names ports, costs, the tick block, and a claim nested in a procedure called from
the tick block. None of these can occur in version 0, so none is in the measured set. The measured patterns are the
five parts.

### The critique, point by point

| point | disposition |
|---|---|
| shared mistakes survive the meet | **accepted.** The meet's false holdings are the intersection of R8's and CUT-0's. It is never looser than R8, and it is no proof of E2. §2 said so; the reviewer's "bounded safety property" overstated it |
| the admitted rule coupled to a moving artifact | **accepted for identity, rejected for receipts.** An admitted meet must name CUT-0 by its digest: R8 ∧ CUT-0 at a pinned version, the way the court is pinned. Research goes on in a copy, and a revised CUT-0 enters only by a new ruling. No receipt depends on a settlement rule, though. The receipt core attests the run, and the reading names its rule (`CUT-0.md` §3; `CUT-SCHEMA.md` P7). A revision makes new readings and touches no receipt |
| a digest-pinned defeater set in place of the meet | **rejected as the mechanism.** A defeater witnesses one execution of one law. A law written tomorrow matches none, so the set fixes the corpus and not the next law, while R8's over-holding is a class that every interrupted loop instantiates afresh. A defeater generalized to a pattern is a rule with its own proof obligation, and the five parts above are those patterns: CUT-0's rows. **Kept from it:** each withholding carries its evidence. Here the evidence is structural: every withheld claim names the part of K̂ that withholds it, printed beside "true in 17 of 17" |
| pattern-first: fix the causes, register the outliers | **accepted, in the form the data gives.** The causes are the five rows, and there are no outliers. Its consequence: **split T10 by row** (a For, a While, a block's rest, an If's arms, a loop's own clause, a Perform). Each row's argument can then be proved or waived on its own, and precision work goes where the conservatism is: the While row |
| missing evidence, inadequate policy, or over-withholding | **all three, measured apart.** **Missing evidence** (ESTABLISHED): R8 reads only the receipt's status and claim lines (`court.py` 245–247). No receipt says whether a loop had passes left, which call was active, or which arm refused: v0's `'R'` payload is the code alone, and a Perform emits no event. That evidence is the cut, which draft 2 records. **Inadequate policy:** the 1,968 REFUTED. **Over-withholding:** the 1,247 UNREACHED |
| defer 1a until measured | **measured now,** so the deferral's reason is discharged. What remains is the owner's ruling on meaning (point 3) |

### Consensus, revised

| | |
|---|---|
| the decisive question | **what HELD means, E1 or E2.** 92.6% of the disagreements turn on it alone |
| if E2 | admit (d), pinned: R8 ∧ CUT-0 at a named digest, each withholding naming its part. CUT-0 alone stays the target; its seven gains (all UNREACHED) enter with T10 proved or waived, row by row |
| if E1 | R8 stays, and is right by its own definition. CUT-0 becomes a report, not a settlement: the reading prints "the run could evaluate this claim again, by part P" beside HELD, and withholds nothing |
| either way | the cut is recorded (it is the evidence R8 lacks); T10 is split by row in the ledger; the While row is the precision target |

**Does not show:**
- values outside the eight. CONFIRMED means no resumption tried refuted the claim, not that none could, and UNREACHED
  is likewise within the eight values;
- the truth of family E's 34,523. They are CONFIRMED by their grammar: they count toward the CONFIRMED share's size,
  not its truth;
- real laws: the families are the proponent's grammar and seed, and the corpus has 10 such claims;
- version 1's tick block.

## 8. E2's meaning, sharpened (2026-10-26, later)

The owner forwarded the reviewer's recommendation of E2, and a longer reply in his own message that he marked *"my
recommendation, not an owner ruling"*. Both are paraphrased here. Both recommend E2 as the authoritative meaning of
HELD, the meet pinned to CUT-0's digest, and T10 kept open and split by row. The reply also answers proposals that are
in none of this record's files: two `held` booleans in the receipt, and a claim that E2 has zero false holdings. This
record made neither.

| point | disposition |
|---|---|
| E2 must mean "nothing pending **for this claim**", not "nothing pending anywhere" | **already E2's definition.** `CUT-0.md` §1: held when every completed evaluation is true, none is open at the cut, and the continuation "could not evaluate the claim again". K̂ is a set of claim ids, and a claim is withheld only when its own evaluation is in it. Work elsewhere in the program never withholds a claim |
| a claim whose truth no continuation can change might be settled though it would be evaluated again | **a different, stronger rule: E2 modulo invariance.** It is not E2. It needs a proof per claim that every statement the continuation could run preserves the condition, an inductive invariant. That is a cost question of T12's kind (the dependence bound, CONJECTURED). The measurement shows where it bites: family E's 34,523 CONFIRMED claims are all `x is at least 0`, which no statement of either family can make false. How many of family G's are of that kind is not counted. **Not proposed for 1a;** a precision rule of its own, with its own obligation, if ever |
| the 40,141 CONFIRMED are not necessarily claims E2 must withhold, some being the approximation's | **corrected: E2 withholds every one of them by definition.** CONFIRMED means a resumption evaluated the claim again, so the claim is in K, the true continuation for a supplied value, not merely in K̂. The approximation touches only the 1,247 UNREACHED. What could release CONFIRMED claims is a change of meaning (the invariance rule above), not a better K̂ |
| no two `held` fields in the receipt; one authoritative standing in a versioned reading; E1 shown as description | **agreed, and mostly in place.** The receipt attests the run, and the reading names its rule (`CUT-0.md` §3; `CUT-SCHEMA.md` P7). E1's descriptive fact is already in every reading: the court prints "true in k of k evaluations" (`court.py` 287), a fact `CUT-0.md` §1 says is never withdrawn. A new word for it (the reply's `NO_CONTRADICTION_OBSERVED`) is not needed. What a reading adds under E2 is the part of K̂ that withholds the claim (§7) |
| the meet does not make false holdings impossible; a digest identifies a rule and does not prove it | **agreed;** §2 and §7 say so |
| record the rejected meaning in DOCTRINE as a design choice, not a theorem | **agreed,** after the owner rules. The ledger's T-rows are for propositions; a ruling on meaning goes to `RULINGS.md` in his words, and DOCTRINE names it |
| keep T11 open | **agreed.** Nothing here touches COMPAT-0's preservation |

**What the owner is asked:** what HELD means for version 1, E1 or E2. Both texts recommend E2. If E2: (d), pinned,
each withholding naming its row, CUT-0 alone the target. If E1: R8 stays, and CUT-0 is a report beside it.
