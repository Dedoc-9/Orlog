# Debate record: the adversary's prosecution, round 1 (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority; the judge's verdict (VERDICT.md in this folder) weighs it against the proponent's design and the prior-art
survey. Its experiments are in `work/ragnarok-adv/` (ignored by git); its MEASURED lines are this host's.

---

# Adversary's prosecution of "Ragnarök, the Counterworld Court"

**What I read.** `research/ragnarok/PROPOSAL.md`, set against README, DOCTRINE (§0, T1–T4, §6, §8, §9), SPEC (§3, §7, §11 item 32), `src/orlog/court.py`, `interp.py`, `sema.py`, the corpus and the court record.

**What I changed.** No tracked file.

**Where the experiments are.** `work/ragnarok-adv/` (ignored by git): the scripts `rk.py`, `fixtures.py`, `experiments.py`, `experiments2.py`, `fourway.py`, `cost.py`, `write_fixtures.py`, and every printed line in `out/*.txt`. Both experiment scripts ran twice with byte-identical output.

**Grades.** MEASURED here means this Windows host, CPython 3.14.5, clang 22.1.8 and rustc 1.96.1. Runs used the reference interpreter unless "four executions" is said. A MEASURED line is falsified if a rerun of its script prints something else. One model family wrote the language, the proposal and these experiments, so this report is consistency-checked argument, not ground truth.

**The toy.** `rk.py` defines a "world" as the only thing a closed Ørlǫg program can vary without a language change: a substitution of marked literal positions in the text. Each world is compiled and run as an ordinary closed law, and classified from its receipt alone.

**The main fixture is the proposal's own example (line 36), made concrete.** A ball moves v cells per tick toward a wall one cell thick at 10. If it lands inside the wall it is put back at 9 and turned around. The conclusion "x is less than wall" fails exactly when the ball steps over the wall (tunnelling): for v in 1..10 it holds for {1, 2, 5, 10} and fails for {3, 4, 6, 7, 8, 9}. In `WALL_FWD` the conclusion (§5) cites a premise that stands after it (`§5 We claim that x is less than wall, given §6.` and `§6 We claim that v is not zero.`); in `WALL_BACK` the premise stands first.

## Experiments (MEASURED here)

| id | what was run | result |
|---|---|---|
| E1 | collatz with n=27 and with n=28 | n=27: law barap-futug-zojul-vuzup, COMPLETED. n=28: law butan-polid-komim-tudaf, REFUSED CLAIM-REFUTED 9. The claim seal of §6 changes from 35102a89… to 9ef6e49d…. |
| E2 | WALL_FWD, v in 1..10 | 6 worlds refute §5, and in each §6 is UNREACHED. Reading UNREACHED as the court's R7 does, the literal verdict is SURVIVED. WALL_BACK gives FALSIFIED with counterworlds [3, 4, 6, 7, 8, 9]. |
| E3 | one law, three exhaustive domains | The author's speeds {1, 2}: SURVIVED. v in 1..10: FALSIFIED, 6 counterworlds. Speeds {1, 2} with start x0 in 0..12: FALSIFIED, 11 of 26 worlds, including the author's own speed 2 from x0=1. |
| E4 | WALL_MUST: the conclusion restated as a `must` before the claim | If a failed must makes a world inadmissible: SURVIVED (4 hold, 6 inadmissible). If a failed must is a counterexample: FALSIFIED. With a must keeping only speeds 1..2: SURVIVED (2 hold, 8 inadmissible). |
| E5 | WALL_VAC: a premise no world in v in 2..10 meets | SURVIVED; 0 of 9 worlds reach the conclusion. |
| E6 | the "smallest set of additional assumptions", by brute force | Interval atoms: 2 minimum solutions of size 1, "v ≤ 1" (rules out 2, 5 and 10, where the claim holds) and "v ≤ 2" (rules out 5 and 10). Exclusion atoms (v ≠ c): the minimum is the list of the six counterworlds. Any condition at any clause: the conclusion itself as a must. |
| E7 | the repair loop: add "v ≤ 2" as a must and search the same domain again | SURVIVED; worlds 5 and 10, where the claim holds, became inadmissible. |
| E8 | Plankton with plan and robot in 1..10 | All three circular claims read SURVIVED, each established by one world (7, 7); the other 99 worlds are UNDEFINED, cut short, or have a failed premise. |
| E9 | the domain written into the law as a For loop (no new feature) | Speeds 1..10: REFUSED CLAIM-REFUTED; the court reads "REFUTED at evaluation 3"; the four executions AGREED. Speeds 1..2: COMPLETED and WELL-FOUNDED. A counting version prints the six speeds. |
| E10 | a defective enumerator that skips the last world | Finds a counterworld planted at v=3; reports SURVIVED for one planted at v=10. |
| E11 | WALL_FWD under two readings of an UNREACHED premise | Not held: SURVIVED. Held: FALSIFIED. |
| E12 | the corpus | 8 claims; 5 have no premises; 3 do, and 2 of those have a premise at or after the claim (Plankton §3 and §4); 1 claim stands inside a loop. |
| cost | timings (software; clock resolution 1e-7 s) | Reference alone: 10 worlds in 0.009 s, both runs. Four executions per substituted world: 1.55–1.94 s (run 1), 1.72–4.07 s (run 2), one fresh C and Rust build per world. One law holding 10 worlds: 4.81 s and 4.32 s; holding 1000 worlds: 4.95 s. Every literal free at ±10: plankton 21^4 ≈ 1.9e5 worlds, collatz 21^10 ≈ 1.7e13, fall 21^15 ≈ 6.8e19, leapfrog 21^44 ≈ 1.5e58. |

## Count 1. Logic and semantics

**R-1 · FATAL (as written). There is no second world.** A closed deterministic program has exactly one run. The proposal never defines "world", "environment" or "admissible", and its example ("the environment changes in a way the law never constrained", line 36) names something Ørlǫg has no construct for. Three possible definitions, none chosen:
- (A) Substituting literals in a harness: no language change, but every world is a different law (E1: the law seal and every claim seal change), so the owner's ratification, bound to a claim's own seal (court.py:141–144, R5), never covers a counterworld; the "family" of worlds has no identity inside the language; four-way checking per world costs about 2,000–4,500 times the reference alone, because each world needs its own builds.
- (B) Free parameters as a new language form: "today a program takes no input" ends; a new statement and new versions of the law bytes, the receipt, the event chain and the claim seal (AGENTS.md:67–74); inputs in all three generators and both runtimes. That is DOCTRINE §9's "capability inputs" rung, unadmitted (DOCTRINE.md:425–427); it needs a new twin round, new refusal codes, and a rule for what a standing means over a family of runs.
- (C) The domain as a loop in the law: works today (E9), four-way checked with one build, and the domain is sealed into the law, so the existing ratification of a claim's seal also binds the domain.

**R-2 · FATAL (as written). The headline contradicts itself or cannot be computed.** Line 11 asks for worlds where "every claim is well-founded—and the conclusion is nevertheless false". If the conclusion is a claim, a world where it is false refuses CLAIM-REFUTED (SPEC.md:249; interp.py:252–253): not held, so not well-founded. If it is not a claim, it is intent ("the intent is not in the text", README.md:11–12). The only coherent reading uses two worlds: everything green in the law's own world, and the claim refuted in another. That is ordinary refutation by changing an input (E1, E3), not the "astonishing" case of lines 27–28.

**R-3 · FATAL (as written; repairable only by restriction). "Premises hold but the conclusion fails" is undefined for claims Ørlǫg can write.** `given` is a declared support edge, not an implication: the interpreter never reads premises (interp.py:237–253); they are parsed, checked as targets and sealed into the law (sema.py:226, :586), and only the court reads them, for support, never checking entailment (court.py:5–9). A premise may stand after the claim, or be the claim itself (SPEC.md:357). The first false claim stops the run, so a later premise is UNREACHED exactly when the conclusion fails (E2). Under the court's R7, an UNREACHED claim is "neither supported nor refuted" (court.py:45–46), so the literal proposal reports SURVIVED on WALL_FWD although six of ten worlds refute its conclusion. The verdict then depends on unstated readings: an UNREACHED premise as not held or held (SURVIVED or FALSIFIED, E11), or UNRESOLVED through line 44's "its semantics were insufficient"; swapping two claims flips the result (E2); a must as an assumption or an assertion flips SURVIVED and FALSIFIED (E4). Even where it works, "premises hold" means "held at every evaluation before the run stopped": a prefix property, weaker than the court's "held". In the corpus, 2 of the 3 claims with premises have a forward premise, and 5 of 8 claims have no premises at all (E12); for those five, step 3 is simply "refute the claim by changing an input".

**R-4 · OVERREACH, and FATAL for "discover its own missing axioms". The smallest set of assumptions.** On a finite domain the weakest assumption excluding every counterworld is computable: the set of worlds where the claim holds, which as an "assumption" is just the list (E6, exclusion atoms). Measured by size, the minimum depends on the grammar, need not be unique, and can rule out worlds where the claim holds (E6: two size-1 solutions, both too strong). If the grammar allows run-time conditions, the minimum is the conclusion restated (E4): the tautology airlock TRIAGE already forbids. In general this is minimum set cover or minimum DNF, NP-hard (Karp 1972; Masek 1979 [unpublished, unsure]); over Int domains, abduction, Σ2P-complete in the propositional case (Eiter & Gottlob, JACM 1995), or a weakest precondition (Dijkstra 1975): prover territory. The repair loop manufactures SURVIVED: adding the found assumption as a guard and searching the same domain must succeed by construction, and it silently excludes good worlds (E7). This is Lakatos's monster-barring and lemma-incorporation (1976), automated.

**R-5 · OVERREACH. No label can make SURVIVED safe from being read as proof.** The project's own record shows labels misread: "CLOSED" over nothing (L10); edition 1's "No declared plant survived" was vacuous and removed (court/prosecution-logic.md:264–267; court/RECORD.md:37); CHEAPER and RECOMPUTATION (L6, L7); court.py:286–288 had to add forbidden interpretations. A VACUOUS outcome is missing: E5 reports SURVIVED over 0 of 9 reached worlds, and E8 reports SURVIVED for Plankton's three CIRCULAR claims. SURVIVED collides with mutation testing, where a "survived" mutant (PIT's status) means a defect the tests missed. FALSIFIED names the wrong object: the claim held in its own law (E1, n=27); what is refuted is a generalization over the search domain that nobody wrote in the law.

**R-6 · OVERREACH. A separate checker does not end self-certification; it moves it.** A FALSIFIED witness of a closed deterministic program is checked by running it: the existing reference and arbiter, from the same family (the substituted world v=3 agrees on four executions, `out/fourway-run1.txt`). This shows the run is as reported, relative to the specification. SURVIVED has no witness short of the whole enumeration; checking it costs the search again (Horn B, DOCTRINE §0). What decides the verdict is the domain (E3), the reading of musts (E4), the reading of UNREACHED (E11) and the grammar (E6), all in the "frozen specification" the same family writes. Line 46 concedes the result is conditional; in practice the conditions carry the whole verdict.

**R-7 · IMPRECISION. The proposal misdescribes the court.** "Reasoning is formally sound" (line 28) and "the court could show that the conclusion follows from the program's rules" (line 36): the court evaluates and computes support, never derivation ("Never truth", court.py:1). Claims about one instance are "falsified" by any world that changes their subject: Collatz's claim is about 27, so n=28 refutes it (E1). Which literals a claim generalizes over is intent.

## Count 2. The verification paradox, turned on Ragnarök

**R-8 · OVERREACH, against line 9 ("discover its own missing axioms") and line 55. The search looks where its author looked.** Whoever writes a collision test sampling only at tick ends is least likely to put fast speeds in the domain: the author's {1, 2} SURVIVES (E3). Tunnelling appears only for v ≥ 3, or from starts the author never varied (v=2 from x0=1); someone who suspected it would already have fixed the test. This is coincident failure (Eckhardt & Lee; Knight & Leveson, already in DOCTRINE §0) applied to the search domain. Anything not already a literal (a second ball, a moving wall, a different tick order) is in no domain at all: the search space is the author's vocabulary. The grammar decides the "missing axiom" (E6); the reading of musts and of UNREACHED decides the verdict (E4, E11). The planted-counterworld test is placed by the same hands as the enumerator: a broken enumerator passes a plant at the bottom of the domain (E10).

**R-9 · IMPRECISION.** By T2's own theorem, the DPI (DOCTRINE.md:97–102), a verdict carries no bits beyond the law text plus the domain file. The domain file is the only place outside bits could enter, and the proposal gives it no channel and no standing.

**The record agrees.** The counterworld searches that mattered here were all scripts outside the language: L16 (6,000 single-ulp perturbations, 1,526 erased, FATAL; court/prosecution-logic.md:432–460), `doorfuzz.py` and `diff_twin.py`. In each, the decisive step was choosing the domain, and the enumeration was a loop. The targets were Notes, doctrine prose or properties of the implementation, which Ørlǫg claims cannot express (T1, DOCTRINE.md:81–82; refusals cannot be caught, DOCTRINE.md:279).

**What breaks the loop.** Nothing entirely (README.md:119). Four things weaken it: (1) the domain written in the law (E9), so the owner's ratification of the claim's seal is a person outside the family judging the domain (the existing R5, available today); (2) domain and grammar fixed and hashed before the law is read, by someone other than the law's author; (3) worlds from outside the family: owner-written literal targets (Verðandi's G23/G29 lesson), a human or other-family red team, recorded incidents; (4) domains derived mechanically from the text, such as the boundary values of every comparison: a heuristic, chosen independently of any one law.

## Count 3. Novelty

**R-10 · OVERREACH.** Line 54's caveat is right, but the "genuinely new research question" (lines 49–51), counterexamples to declared coverage, is not new. Prior art the proposal must not claim ([V] verified by search or fetch in this session; [C] confident from memory; [U] unsure):
- Bounded model checking: Biere, Cimatti, Clarke & Zhu, TACAS 1999 [C]; CBMC (Clarke, Kroening & Lerda, TACAS 2004) [C].
- Alloy and the small-scope hypothesis: Jackson, *Software Abstractions* (2006) [C]; Jackson & Damon 1996 [C]. Alloy already prints "No counterexample found. Assertion may be valid." [V]; its FAQ says the bound can still miss one [V], and false facts make every check pass, the vacuity trap [V, tutorial]. Andoni, Daniliuc, Khurshid & Marinov evaluated the hypothesis [U: venue not found].
- Bounded exhaustive testing: TestEra (2001), Korat (ISSTA 2002) [C]; SmallCheck (2008) [C].
- Finite countermodel finders: Mace4, Paradox, Kodkod (TACAS 2007) [C]; Nitpick (Blanchette & Nipkow, ITP 2010), which separates genuine from candidate counterexamples [V].
- CEGAR (spurious counterexamples, refinement predicates): Clarke, Grumberg, Jha, Lu & Veith, CAV 2000 / JACM 2003 [C].
- Vacuity: Beer, Ben-David, Eisner & Rodeh, CAV 1997 [C]; Kupferman & Vardi, CHARME 1999 [C].
- Coverage in model checking: Chockler, Kupferman & Vardi, TACAS 2001 [C]; Hoskote et al., DAC 1999 [C].
- Mutation testing: Hamlet 1977; DeMillo, Lipton & Sayward 1978 [C]; equivalent mutants (Budd & Angluin 1982; Offutt & Pan 1997) [C]; Jia & Harman 2011 [C].
- Witness validation: Beyer et al., FSE 2015, FSE 2016, TAP 2018 [C]. SV-COMP has required violation witnesses since 2015 and correctness witnesses since 2017; a result no validator confirms is "unconfirmed" [V, sv-comp.sosy-lab.org/faq.txt].
- Assumption mining and abduction: Eiter & Gottlob 1995 [C]; Dillig, Dillig & Aiken, PLDI 2012 (missing assumptions found by abduction and classified by a person) [C]; minimum satisfying assignments, CAV 2012 [C]; weakest environment assumptions (Giannakopoulou et al., ASE 2002; Cobleigh et al., TACAS 2003) [C]; Chatterjee, Henzinger & Jobstmann, CONCUR 2008; Li, Dworkin & Seshia 2011 [C]; Daikon; Cousot et al., VMCAI 2013 [C].
- Property-based testing: QuickCheck (ICFP 2000, with shrinking) [C]; Hypothesis [C].
- Backend equivalence: McKeeman 1998; Csmith (PLDI 2011); EMI (PLDI 2014) [C].
- Assurance that searches for defeaters: eliminative argumentation (Goodenough, Weinstock & Klein, SEI TR 2012-002 and 2015-005; "x of y defeaters eliminated") [V]; Assurance 2.0 (arXiv 2004.10474 and 2405.15800) [V]. Already in research/R3-encodings-physics-novelty.md:91, not carried into the proposal.
- Philosophy: "true of a narrower world than its author thought" is Lakatos 1976 [C]; SURVIVED is Popper's corroboration [C].
- Inside the repository: L16, `doorfuzz.py`, `diff_twin.py`, the plants (AGENTS.md already names equivalent mutants), and the removed reading "No declared plant survived".

What could remain new (SPECULATIVE; applications, not mechanisms): (1) a refuting world emitted as a sealed closed law and re-run on four executions; (2) the domain inside the law, so seal-bound ratification also ratifies the domain; (3) an outcome vocabulary with NOT DEFINED and VACUOUS kept outside the standing columns.

## Count 4. Engineering and governance

**R-11 · OVERREACH. Cost and blow-up.** "Every execution agrees" in every world (line 11) is affordable only for a domain written into the law: 1000 worlds in 4.95 s, against about 1.6–4 s per substituted world. One free i64 parameter is 2^64 worlds, about 5.8e8 years for the reference alone at about 1 ms per world.

**R-12 · OVERREACH; FATAL if it enters the court's panel. A second authority.** The proposal calls it "A second verdict" (line 21); Ørlǫg keeps one authority for standing (DOCTRINE.md:411–412). The owner's words in a 2026-10-22 ruling on another rung, quoted by the adversary from a file outside this repository: "Enforcement layer only; it never becomes the authority for the evidence it enforces". Under T2/R2 a Ragnarök outcome is the tool's own computation, so it can never raise or ground a standing. If it lowers one, it is a court with a veto (wrong for Collatz, E1). If it stands beside the standings, it will be read as one: CIRCULAR next to SURVIVED (E8).

**R-13 · OVERREACH. Creep toward a theorem prover.** Line 53's "every admissible world the claim purports to describe" quantifies over intent and over infinite domains. Step 2's "external facts, and semantic rules" would require formalizing the semantics. Line 52's finite first version can never meet line 53.

**R-14 · FATAL (procedural: it blocks admission, not the idea). No trigger and no admission record.** The proposal names no recorded failure that Ragnarök would have caught and the plants, the twin, `diff_twin`, `doorfuzz` and the prosecutions missed; L16 was handled by two ad hoc scripts. The rung it depends on is unadmitted (DOCTRINE.md:425–427); DOCTRINE §9's rulings and the round-2 court record are still open (STATUS.md). The owner's words, quoted by the adversary from records outside this repository: "Make research findings—not the backlog—authorize new patches", and "Every new work item should have a short admission record". The named-trigger rule appears in those records only in a judge's and an attack's words, not the owner's own sentence.

**R-15 · OVERREACH. What a first version could falsely appear to show.** That a planted counterworld proves the search works (E10); that an exhaustive search means a universal result (E3); that four-way agreement validates the counterworld, when it validates only the run (E1); that SURVIVED after a repair is evidence (E7); that the minimal assumption is a discovered axiom (E6); that Plankton's claims are vindicated (E8). Edition 1's vacuous "plant survived" reading (L8) is the precedent.

## The narrowest version I would not oppose

**RAGNARÖK-0: a bounded refutation instrument for prosecutions. Neither a court nor a language feature.**
- No language change. A world is a substitution of literal positions, named by clause label and literal index, listed with finite value lists in a domain file. Each world is an ordinary closed law.
- The domain file's sha256 is recorded before the run (that it was fixed before the law was read is DECLARED). Every world in the product is run on the reference, in the domain file's order. The budget is in counted operations, never time (T3).
- Each refuting world is re-run on four executions through the existing arbiter.
- Each world is classified from its receipt into exactly one class: refutes; holds; stopped by a must before the claim; a premise refuted; another refusal; claim never reached.
- A claim with a premise at or after it is NOT DEFINED and is not searched.
- It never writes the ledger, changes a standing, adds a column to the court's panel, proposes assumptions, or says anything outside its domain.
- A domain meant to carry standing is written into the law (E9), where the court and R5 already govern it.
- It enters with its own admission record. Its trigger is the next prosecution that needs an exhaustive search over a declared finite domain, as L16 did.

**Acceptance tests (each can fail; each plant must be caught):**
- **AT-1. An exact refutation.** WALL_BACK with domain {v: 1..10, x0: 0} must print the REFUTED line with 6 of 10, first witness v=3, x0=0, witness law pukak-gobad-magor-sipuj agreeing on 4 executions, list v ∈ {3, 4, 6, 7, 8, 9}, and class counts 6 refute and 4 hold. Plant: skip the last world; on a fixture where only v=10 refutes, the outcome must be INCOMPLETE, never NO REFUTATION. Plant: count a MUST-FAILED world as a refutation; WALL_MUST must then not read REFUTED.
- **AT-2. Vacuity, exclusion and undefined premises are named.** WALL_VAC with v in 2..10 reads VACUOUS, 0 of 9 reached. WALL_MUST with v in 1..10 reads NO REFUTATION, 4 of 10 reached, 6 of 10 stopped by a must. WALL_FWD reads NOT DEFINED for §5. Plant: read an UNREACHED premise as held (WALL_FWD would then read REFUTED, E11); caught. Plant: drop the VACUOUS branch; caught by WALL_VAC.
- **AT-3. No authority, determinism, vocabulary.** Two runs on the same inputs are byte-identical. Each report names the base law's seal words, the domain file's sha256 and the instrument's version. `orl.py court` output and the ledger file's sha256 are identical before and after a run. No report contains: proved, proven, verified, valid, survived, safe, "holds for all", FALSIFIED, WELL-FOUNDED, GROUNDED; "proof" only in the exact phrase "Not a proof". Plants: insert "survived" into a report; append a line to the ledger. Both caught.

**The exact outcome words** (`d` is the first 16 hex digits of the domain file's sha256):
1. `REFUTED IN DOMAIN d=<d> law=<seal words>: <r> of <N> worlds refute §<k>; first witness <p>=<v>[, …]; its law <seal words> agrees on <n> executions. §<k> as written in law <seal words> is not changed by this.`
2. `NO REFUTATION IN DOMAIN d=<d> law=<seal words>: 0 of <N> worlds refute §<k>; <m> of <N> reached §<k> with its premises held; <e> of <N> were stopped by a must before §<k>. Not a proof: nothing is said of any world outside d.`
3. `VACUOUS IN DOMAIN d=<d> law=<seal words>: 0 of <N> worlds reached §<k> with its premises held; nothing was tested.`
4. `NOT DEFINED for §<k>: its premise §<j> stands at or after it, and a claim's later premises are UNREACHED whenever it fails.`
5. `INCOMPLETE d=<d>: <n> of <N> worlds run within <B> counted operations; no outcome.`
