# Verdict: Ragnarök, the Counterworld Court (2026-10-25)

The judge's verdict on the owner's proposal (PROPOSAL.md), after two rounds between a proponent, who designed it and
built a probe, and an adversary, who attacked the proposal and then the design, with a prior-art survey beside them.
Every report is saved verbatim in this folder: ADVERSARY.md and ADVERSARY-R2.md, PROPONENT.md and PROPONENT-R2.md,
RESEARCH.md. This verdict is model output, like them, and admits nothing. Their experiments ran on this host, but their
scripts sit in `work/` folders that git ignores, so from this tree their figures are OBSERVED, not reproducible.

## The verdict

**Do not build the proposal as written.** Three of its promises cannot be kept, and both sides agree after round 2:
1. **"Worlds where every claim is well-founded and the conclusion is nevertheless false"** cannot be computed in a closed
   program. If the conclusion is a claim, a world where it fails refuses CLAIM-REFUTED, so the claim is not held. If it
   is not a claim, it is intent, which is not in the text. The only coherent reading is refutation by changing an
   input (adversary R-2; the proponent concedes).
2. **"The smallest set of additional assumptions"** is ill-posed without a declared vocabulary of assumptions and hard
   with one: minimum hitting set, Σ2P-hard for abduction (the survey, (b)). Its repair loop, which adds the found
   assumption as a guard and searches the same domain again, manufactures SURVIVED by construction. The proponent's own
   gcd case printed that the guard also ruled out 4 worlds where the claim held. The proponent withdrew it.
3. **A "second verdict" beside the court's standings** would be read as a standing: SURVIVED beside CIRCULAR reads as
   vindication. Computing support and grounding before the column joins protects the computation, never the reader.
   The proponent withdrew it.

**What survives is an instrument, not a court.** RAGNARÖK-0, as both sides now describe it: a bounded refutation search
used by a prosecutor.
- **A world** rewrites the literals of top-level `Let` clauses that a separately sealed sheet declares free. Every world
  is an ordinary closed law, so there is no language change.
- **The search** enumerates the sheet's finite domain exhaustively on the reference. It runs under a cap on the number
  of worlds and a budget of counted operations per world, and writes a hash-chained search receipt.
- **Each refuting world** is checked by a structural reading, which proves the witness differs from the base only where
  the sheet allows, and is then run on c99 and on the clean-room twin.
- **It writes nothing** to the ledger or the court, proposes no assumptions, and says nothing outside its sheet.

**Admit it later, if ever, and only with a trigger.** No recorded failure needs it (adversary R-14; the proponent
concedes). Its trigger is the next prosecution that needs an exhaustive search over a declared finite domain, as L16
did, and it enters with its own admission record. Until then it is not a rung of the roadmap
(`research/roadmap-debate/VERDICT.md`).

**Novelty: none in the mechanisms.** Every mechanism the proposal names has existed for 20 to 25 years: bounded
countermodel search, three-way verdicts, separate witness validators, coverage by mutation and assumption abduction.
The owner's own caveat said so, and the survey confirms it. Two integrations were not found, which is absence of
evidence and not novelty: entailment of *declared* support as a standing beside the court (survey item 10), and bounded
verdicts typed by channel (item 11). Both are court changes, not RAGNARÖK-0. They are below, for the owner's forks.

## What the debate established

Every figure here was OBSERVED in the debaters' ignored work folders, on this host. A plant is a planted defect that must
be caught.

| result | who | what it shows |
|---|---|---|
| A planted counterworld found exactly: a bouncing ball over speeds −12..12 gives the 10 refuting speeds worked by hand. c99 and the twin each confirm every witness from its own receipt, byte-identical to the reference | proponent, round 1 | the search and the checker can find what is there |
| A search that skips its last world, against a claim refuted only there, read SURVIVED in round 1, with "1 ruled out otherwise" | adversary (E10, R2-2b); proponent concedes | a world never run was booked as excluded. Repaired by recounting the worlds run against the sheet: INCOMPLETE |
| A premise written after its claim is never evaluated when the claim fails, so "the premises held" is undefined there | adversary (R-3, R2-1); proponent concedes | now NOT DEFINED, decided from the text before any run |
| A world where another claim refutes first never tests the target: plankton §5 read SURVIVED over 1 of 100 worlds, beside the court's CIRCULAR | adversary (E8, R2-4); proponent concedes the vocabulary | masking hides counterworlds; see the decision below |
| One defect in the literal conversion, which all three readers share (`numeric_ref.round_half_even`, called by `sema.py` and by the twin), gives a FALSIFIED that the checker confirms three ways, byte-identical | adversary, R2-8 | the readers are complementary only away from what they share; the defect is a declared blind spot |
| Writing the domain into the law as a For loop works today for 6 of 10 corpus laws: four executions, one build, the domain sealed with the law. The other 4 are refused (DECIMALS-PLACE, DEFINE-PLACE, UNKNOWN-PROCEDURE) | adversary (E9); proponent, round 2 | a domain meant to carry standing belongs in the law, where R5's ratification already governs it |
| The door's retraction over 13 symbols: 0 counterexamples to length 7 (67,977,560 sequences, proponent) and to length 5 (rerun by the adversary). Under its plant, E18's exact bytes appear within length 5 | both | genuine within its alphabet. The alphabet exercises 9 of the door's 18 repair rules and cannot form a clause line, so retraction stays DECLARED |
| Cost: the reference-only search takes 0.03 s for 25 worlds; each checked witness about 2.4 s (a clang build and a twin run) | proponent | refuting worlds are cheap to check; re-deriving an absence costs the search again |

## The decisions on what remained open after round 2

1. **The vocabulary: the adversary's sentences.** They read REFUTED IN SHEET, NO REFUTATION IN SHEET, VACUOUS, NOT DEFINED,
   UNRESOLVED and INCOMPLETE, each with its counts and the sheet's seal. The values are scanned for proof-shaped words,
   not only the keys. FALSIFIED and SURVIVED are not used: a word whose natural reading must be forbidden is the wrong
   word, as CLOSED was (L10).
2. **Masked worlds: UNRESOLVED, as the adversary asks.** "No refutation" over worlds that never reached the claim would
   claim a test that did not happen. The proponent's all-claims mode, which names the claim that refuted first in each
   masked world, stays as the reason the line prints.
3. **The twin joins the readers of a refuting world, and R2-8 stays a declared row.** The twin is the one reader with
   its own front end; its rounds found 62 ambiguities and reference defects. It shares the literal conversion, so R2-8
   is kept as a row that must read CONFIRMED and is never counted as caught (the self-test's monitored negative, in
   another place).
4. **Each coverage target is an instrument of its own.** The door search, refusal completeness and fixed points over
   small support graphs each need an admission record (adversary D-10). The door search is worth keeping as a
   prosecution tool beside `doorfuzz.py`, since it re-finds E18 under its plant. It belongs to neither the self-test
   nor the court.

## The owner's research question, answered in its cheapest form

The proposal's "genuinely new" question was whether Ørlǫg could find counterexamples to its own declared coverage. As a
mechanism this is not new (surviving mutants: Groce et al. 2015 and 2018; the survey grades it NOT NEW). As claims the
language makes about itself, each with a checked witness and a channel, it was not found (survey item 12).

This round wrote the cheapest instance of it, with no search engine: the independence rows (DOCTRINE T11). Each states a
coverage claim and holds it with a plant:
- four-way agreement catches a defect in the lowering, through the reference alone;
- it does not catch a defect in the front end: a monitored negative that passes while the defect slips past;
- the vectors catch three mistakes that the reference and its own vectors would share.

The pattern generalizes: state what a guard covers, plant a defect from the class, and require the row to say who sees
it. A search adds exhaustiveness over a declared domain once a class is too large to plant by hand. That is when
RAGNARÖK-0 earns its admission record.

## For the owner's forks, not for RAGNARÖK-0

- **Entailment of declared support** (survey item 10, NOT FOUND). A claim WELL-FOUNDED on its declared premises, yet
  refuted in a world where those premises hold, would be a new standing: "well-founded, not entailed". It attacks the
  court's admitted blind spot (L10; DOCTRINE T12, limit 3). In Ørlǫg `given` is a declared support edge, not an
  implication, and the interpreter never reads premises. Entailment therefore needs a semantics over worlds, which
  means inputs or a parameter domain, so it waits for RUN-1.
- **Bounded verdicts typed by channel** (survey item 11, NOT FOUND). A bounded "no refutation" would become universal
  only through a cutoff or small-model theorem ratified on the claim's own seal. It belongs with typed terminals
  (DOCTRINE T12, limit 1; DOCTRINE §9 fork 9).

## Acceptance, if RAGNARÖK-0 is ever built

Each row can fail, and each plant must be caught by the row it breaks:
- the bouncing ball's refuting speeds held as a literal list, every witness confirmed by the structural reading, c99 and
  the twin;
- the skipped last world reads INCOMPLETE;
- a vacuous sheet reads VACUOUS;
- a premise after its claim reads NOT DEFINED;
- masked worlds read UNRESOLVED, naming the claim that refuted first;
- a refusal inside the claim's own condition reads UNRESOLVED;
- a tampered witness is refused by the structural reading, where a C run alone would confirm it;
- a lying search is refused by the checker;
- a proof-shaped value is refused by the scan;
- the court's output and the ledger's sha256 are byte-identical before and after a search;
- two searches on the same inputs give identical receipts, under PYTHONHASHSEED 0 and 424242;
- R2-8 stays CONFIRMED as declared.

## What this verdict does not show

- That any part of this is new; the survey's NOT FOUND grades are absence of evidence.
- That a sheet captures the scope its author meant: which literals a claim generalizes over is intent (R-7, R-8). The
  proponent's gcd case shows this. A law written for two consecutive Fibonacci numbers fails its certificate on
  negative inputs; whether that is "a narrower world than its author thought" or a change of subject is not in the
  text.
- That the three readers are independent. They share the literal conversion (R2-8), and one model family wrote the
  proposal's implementation, both sides, the survey and this verdict.
