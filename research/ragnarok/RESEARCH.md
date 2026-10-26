# Debate record: the prior-art and feasibility survey (2026-10-25)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. Its source grades ([P], [A], [F], [S], [B], [U]) are its own and say how each source was read; its
working files are in the session's scratchpad, not in this repository. Absolute paths that named the owner's home folder are given relative to the repository, or as the session's scratchpad (AGENTS.md section 8); nothing else is changed.

---

# Ragnarök, the Counterworld Court: prior art, feasibility, and graded novelty

Researched 2026-10-25 on this Windows host. Tools: the session's web search and fetch tools; standard-library Python scripts against the public Crossref and arXiv APIs; `pdftotext` for PDFs.

Read first: `research/ragnarok/PROPOSAL.md`; DOCTRINE §0, §1 (T1–T4), §6 and §8; R2 (not repeated here); `court/prosecution-novelty.md` (N1–N25 and §Q, so its queries are not re-run); SPEC §3 and item 32 (premises); AGENTS.md §3.

No tracked file was written. Working files (scripts, downloads, extracted text) are in the session scratchpad, in `rk-scripts\`, `rk-dl\` and `rk-txt\` under `the scratchpad\`.

**Grades.** These extend R2's scheme:
- **[P]**: the full text, or the tool's own source or manual file, was read here.
- **[A]**: the full abstract was read raw from the arXiv or Crossref API.
- **[F]**: the page was read through the summarizing fetch tool.
- **[S]**: a search-result extract only.
- **[B]**: the bibliographic record was confirmed through Crossref or arXiv; what the work says is stated from memory.
- **[U]**: not confirmed.

Claims about sources are paraphrases; there is one quotation.

---

## 0. Bottom line

- **Every mechanism the proposal names already exists**, mostly for 20 to 25 years:
  - bounded countermodel search: Alloy, BMC, Nitpick, QuickCheck and SmallCheck;
  - three-way verdicts that refuse to call a bounded result a proof: Nitpick, Alive2, Imandra and SV-COMP;
  - separate witness validators: certifying model checkers and SV-COMP since 2015;
  - vacuity and coverage by mutation: IBM 1997 onward, and Chockler, Kupferman and Vardi 2001;
  - missing-assumption discovery by abduction: Eiter–Gottlob 1995, Dillig et al. 2012, and DrLA 2023 for ACL2;
  - environment-assumption mining: Li, Dworkin and Seshia 2011;
  - "counterexamples to the coverage of a verification" as surviving mutants: Groce et al. 2015 and 2018.

  The owner's caveat in the proposal is correct.
- **The proposal's own safeguards are standard practice, and the literature shows they are not enough.**
  - Validators themselves confirm invalid witnesses (Beyer & Strejček 2022).
  - SV-COMP sets its validators' ground truth by a 75% vote, which is consistency, not truth.
  - A "no counterexample" verdict can come from contradictory premises (vacuity).
  - Whether a scope is large enough is undecidable, even for function-free Horn programs (Oetsch et al. 2012).
- **What may be new is integration, and two specifics** (both graded NOT FOUND in (a)).
  - (i) Checking whether a claim's *declared* support entails it, by counterworld search over a declared domain. This would add a standing beside the Kripke–Kleene court ("well-founded, yet not entailed by its declared premises"). It would directly attack T4's admitted blind spot, undeclared dependence.
  - (ii) Typing bounded verdicts by channel, so that a SURVIVED(D) can become universal only through a cutoff or small-model theorem ratified on the claim's own seal.
  - Court-graded self-coverage claims (guards, refusals, backend equivalence) are the same idea at combination level.
- **Feasibility.** A first version is feasible only exhaustively, over tiny declared domains, in standard-library Python. AGENTS.md forbids a SAT/SMT dependency.
  - Ørlǫg's closed, total runs help in one way: whether a mutant is equivalent becomes decidable by running it.
  - They hurt in another: the proposal's own example, an environment the law never constrained, cannot be expressed until there are inputs (the "capability inputs" rung, DOCTRINE §9.8) or a parameter-domain declaration.

## 1. The proposal, cut into the parts used below

| part | what PROPOSAL.md asks |
|---|---|
| P1 | The court identifies the axioms, assumptions, external facts and semantic rules the conclusion depends on |
| P2 | Counterworld search: the premises hold and the conclusion fails |
| P3 | A second verdict: FALSIFIED, SURVIVED (bounded, never universal) or UNRESOLVED |
| P4 | Return the violated implication and the smallest set of additional assumptions that excludes the counterworld |
| P5 | The generator is not its own sole verifier: a small separate checker against a frozen specification |
| P6 | Counterexamples to declared coverage ("a guard catches every instance of a class of defects") |
| P7 | Targets: refusal completeness, run-time invariants, backend equivalence, guard coverage |
| P8 | First version: tiny, exhaustive, reproducible, independently checkable; it finds a planted counterworld and refuses to call a bounded search universal |

## 2. Survey

For each item: **what it does / which part it covers / what remains uncovered.**

### 2.1 Bounded model checking and completeness thresholds (P2, P3, P8)

- **Biere, Cimatti, Clarke & Zhu**, "Symbolic Model Checking without BDDs", TACAS 1999, pp. 193–207, doi:10.1007/3-540-49059-0_14 [B].
  **Biere, Cimatti, Clarke, Strichman & Zhu**, "Bounded Model Checking", *Advances in Computers* (2003), pp. 117–148, doi:10.1016/S0065-2458(03)58003-2 [B].
  These unroll a system to depth k and ask SAT for a counterexample. A counterexample is real; silence means only "none up to k".
- **Clarke, Kroening, Ouaknine & Strichman**, "Completeness and Complexity of BMC", VMCAI 2004, LNCS 2937, pp. 85–96, doi:10.1007/978-3-540-24622-0_9 [S, [author page](https://people.mpi-sws.org/~joel/publications/compbmc04abs.html)].
  - Every finite model and LTL property has a completeness threshold (CT); search up to it is complete.
  - The paper over-approximates the CT through Büchi automata.
  - SAT-based BMC is doubly exponential, one exponent above LTL model checking.
- **Kroening & Strichman**, recurrence diameters, VMCAI 2003, pp. 298–309, doi:10.1007/3-540-36384-X_24 [B]. **Kroening, Ouaknine, Strichman, Wahl & Worrell**, linear CTs, CAV 2011, pp. 557–572, doi:10.1007/978-3-642-22110-1_44 [B]. **Reinhard, Fasse & Jacobs**, CTs for memory safety of array-traversing programs, SOAP 2023, pp. 47–54, doi:10.1145/3589250.3596143 [B]: unbounded guarantees from bounded proofs.
- **CBMC.** Clarke, Kroening & Lerda, TACAS 2004, pp. 168–176, doi:10.1007/978-3-540-24730-2_15 [B]; Kroening, Schrammel & Tautschnig, [arXiv 2302.02384](https://arxiv.org/abs/2302.02384) [A]. *Unwinding assertions* check that the bound covers every execution [S]:
  - when they pass, bounded verification is complete for that program;
  - when they fail, CBMC reports the insufficient bound explicitly.
- **Covers:** P2, and P3's line between bounded and complete.
  **Uncovered:** the bound is a tool parameter, not part of a claim's typed standing; there is no court.
  **Ørlǫg note:** every While declares a bound (at most 2^62, SPEC §3). CBMC's idea transfers exactly: a search that reaches the declared bound is complete for that program. But 2^62 is not a tractable bound.

### 2.2 The small-scope hypothesis, Alloy, and evaluations of the hypothesis (P2, P8)

- **The hypothesis** is credited to **Jackson & Damon**, "Elements of Style…", IEEE TSE 22(7):484–495, 1996, doi:10.1109/32.538605. The credit comes from Andoni et al. [P] and Oetsch et al. [P].
- **Alloy:** Jackson, ACM TOSEM 11(2):256–290, 2002, doi:10.1145/505145.505149 [B]. **Kodkod:** Torlak & Jackson, TACAS 2007, pp. 632–647, doi:10.1007/978-3-540-71209-1_49 [B].
  - The Alloy FAQ calls the analyzer a refuter: an assertion with no counterexample may still be invalid [F, [FAQ](https://alloytools.org/faq/how_does_the_alloy_analyzer_differ_from_theorem_provers.html)].
  - Its message is "No counterexample found. Assertion may be valid." [S]. This is the report's one quotation.
  - A tutorial notes that contradictory facts produce the same message [S].
- **Andoni, Daniliuc, Khurshid & Marinov**, "Evaluating the 'Small Scope Hypothesis'", MIT LCS manuscript; no date or venue is printed, and its references run to 2002 [P, [PDF](http://users.csc.calpoly.edu/~gfisher/work/specl/documentation/related-work/testing/evaluating_small_scope_hypoth.pdf)].
  - Korat-exhaustive small scopes reach full coverage and kill over 90% of mutants for most benchmarks.
  - The kill rate **kept rising after coverage saturated.**
  - A SearchTree mutant was indistinguishable on every tree of up to 4 nodes and needed 5.
  - The authors define the sufficient scope by mutant killing, not coverage.
  - They could not establish that every survivor was equivalent.
- **Oetsch, Prischink, Pührer, Schwengerer & Tompits**, KR 2012 [P, [PDF](https://cdn.aaai.org/ocs/4550/4550-21794-1-PB.pdf)].
  - A small scope suffices for their ASP benchmarks, measured by mutation analysis.
  - **Theorem 1 (p. 45):** for a function-free Horn program, deciding whether passing all inputs of scope n implies correctness is **undecidable**. The proof reduces from query equivalence (Shmueli 1987).
- **Sullivan, Yang, Coppit, Khurshid & Jackson**, ISSTA 2004, pp. 133–142, doi:10.1145/1007512.1007531 [B/S]: bounded exhaustive testing for assurance. Alloy ran out of memory, and they had to decompose and abstract.
- **Korat** (ISSTA 2002, doi:10.1145/566172.566191) and **TestEra** (ASE 2001, doi:10.1109/ASE.2001.989787) [B].
- **Newcombe et al.**, CACM 58(4):66–73, 2015, doi:10.1145/2699417 [B/S]: TLC found DynamoDB bugs that needed traces of 35 steps.
- **Which constraints a "no counterexample" depends on, and overconstraint:** Torlak, Chang & Jackson, FM 2008, pp. 326–341, doi:10.1007/978-3-540-68237-0_23; Shlyakhter et al., ASE 2003, pp. 94–105, doi:10.1109/ASE.2003.1240298 [B].
- **Lifting a bounded result** needs a small-model or cutoff theorem:
  - Emerson & Namjoshi, POPL 1995, doi:10.1145/199448.199468;
  - Emerson & Kahlon, CADE 2000, doi:10.1007/10721959_19;
  - Wolper, POPL 1986, doi:10.1145/512644.512661;
  - Momtahan, ENTCS 128(6):37–52, 2005, doi:10.1016/j.entcs.2005.04.003 [B].
  - **Alloy\*** (∃∀ by CEGIS): Milicevic, Near, Kang & Jackson, ICSE 2015, doi:10.1109/ICSE.2015.77 [B].
- **Covers:** P2 and P8. **Uncovered:** a standing semantics. Scope sufficiency is argued, never computed, and is undecidable in general.

### 2.3 CEGAR, IC3/PDR and counterexamples to induction (P2–P4)

- **CEGAR:** Clarke, Grumberg, Jha, Lu & Veith, CAV 2000, pp. 154–169, doi:10.1007/10722167_15; JACM 50(5):752–794, 2003, doi:10.1145/876638.876643 [B]. An abstract counterexample may be **spurious**. It is checked against the concrete system and drives refinement.
- **Counterexamples to induction (CTIs):**
  - Bradley & Manna, FMCAD 2007, pp. 173–180, doi:10.1109/FAMCAD.2007.15 [B/S];
  - Bradley, VMCAI 2011, pp. 70–87, doi:10.1007/978-3-642-18275-4_7 [B];
  - Eén, Mishchenko & Brayton, FMCAD 2011, pp. 125–134 [S];
  - Hassan, Bradley & Somenzi, FMCAD 2013, doi:10.1109/FMCAD.2013.6679405 [B].

  A CTI is a state that satisfies the current hypothesis and has a successor that violates it. IC3 either shows the CTI reachable, making it a real counterexample, or blocks it with a clause that is inductive relative to reachability.
- **ICE:** Garg, Löding, Madhusudan & Neider, CAV 2014, doi:10.1007/978-3-319-08867-9_5 [B].
- **Ivy:** Padon et al., PLDI 2016, pp. 614–630, doi:10.1145/2908080.2908118 [S]. It shows CTIs graphically and has the user generalize them. Its language is restricted so that verification conditions are decidable (EPR).
- **ExVerus:** Yang et al., [arXiv 2603.25810](https://arxiv.org/abs/2603.25810), 2026 [A]. An LLM generalizes validated counterexamples into inductive invariants.
- **Covers:** P2–P4. A CTI is exactly "a world where the declared hypothesis holds and the conclusion fails". IC3 adds the condition Ragnarök lacks: a blocking lemma must be *true of the actual system* (inductive). That separates a **missing lemma** from a **narrower world**.
  **Uncovered:** run-time claims and channels.

### 2.4 Certifying checkers and separate witness validation (P5, P3)

- **Namjoshi**, "Certifying Model Checkers", CAV 2001, LNCS 2102, pp. 2–13, doi:10.1007/3-540-44585-4_2 [S, [CAV'01 abstract](https://lsv.ens-paris-saclay.fr/Events/cav01/Abstracts/125.html)].
  - A counterexample is checked by simulation, independently of the model checker.
  - A success yields a deductive proof that simpler methods can check (μ-calculus).
- Related: Peled, Pnueli & Zuck, FSTTCS 2001, doi:10.1007/3-540-45294-X_25 [B]; Kupferman & Vardi, TCS 345(1):83–100, 2005, doi:10.1016/j.tcs.2005.07.021 [B]; proof-carrying code, Necula, POPL 1997, doi:10.1145/263699.263712 [B]; Pollack 1998, doi:10.1093/oso/9780198501275.003.0013 [B].
- **The de Bruijn criterion** (proofs checkable by a small independent program) is usually cited to Barendregt & Wiedijk, Phil. Trans. R. Soc. A 363(1835):2351–2375, 2005, doi:10.1098/rsta.2005.1650 [B]. Its content is [S] only; the PDF refused the connection here. T1 already cites certifying algorithms and LCF; this extends them.
- **SV-COMP witness validation.**
  - Beyer, Dangl, Dietsch, Heizmann & Stahlbauer, ESEC/FSE 2015, pp. 721–733, doi:10.1145/2786805.2786867 [S]: a second verifier re-checks a first verifier's violation witness.
  - Correctness witnesses: FSE 2016, doi:10.1145/2950290.2950351 [B].
  - Tests from witnesses: TAP 2018, doi:10.1007/978-3-319-92994-1_1 [B].
  - "Verification Witnesses": TOSEM 31(4), 2022, doi:10.1145/3477579 [B].
  - MetaVal: CAV 2020, doi:10.1007/978-3-030-53291-8_10 [B].
  - Witnesses 2.0: SPIN 2024, LNCS, pp. 184–203 (2025), doi:10.1007/978-3-031-66149-5_11 [A].
- **Beyer & Strejček, SV-COMP 2025**, TACAS 2025, LNCS 15698, pp. 151–186, doi:10.1007/978-3-031-90660-2_9 [P]:
  - a result counts as correct only if some validator confirms its witness; otherwise it is "correct-unconfirmed" and earns no points;
  - validators confirm, refute, or fail;
  - scores: +2 confirmed proof, +1 confirmed bug, −16 false alarm, **−32 wrong proof**;
  - a validation task's expected verdict is set by vote: at least 2 validator results with at least 75% agreement, otherwise the task is void;
  - 103 handcrafted witnesses were added to the validation track.
- **Validators are fallible.** Beyer & Strejček, SAS 2022, LNCS 13790, pp. 160–174, doi:10.1007/978-3-031-22308-2_8 [S]: many validators sometimes confirm invalid witnesses.
- **The no-counterexample side can also be certified.**
  - DRAT: Heule, Hunt & Wetzler, FMCAD 2013, doi:10.1109/FMCAD.2013.6679408; Wetzler et al., SAT 2014, doi:10.1007/978-3-319-09284-3_31 [B].
  - Certified checking: Cruz-Filipe et al., CADE 2017, doi:10.1007/978-3-319-63046-5_14; cake_lpr, Tan, Heule & Myreen, STTT 25(2), 2023, doi:10.1007/s10009-022-00690-y [B].
  - Certified model counting (CPOG): Bryant, Nawrocki, Avigad & Heule, JAIR 82, 2025, doi:10.1613/jair.1.15958 [B].
  - Hardware and LTL certificates: Yu, Biere & Heljanko, CAV 2021, doi:10.1007/978-3-030-81688-9_17; Griggio, Roveri & Tonetta, FMCAD 2018 and FMSD 57(2), 2021, doi:10.1007/s10703-021-00369-1 [B].
  - A verified LTL checker (CAVA): Esparza et al., CAV 2013, doi:10.1007/978-3-642-39799-8_31 [B].
  - Lean's `bv_decide` checks CaDiCaL's LRAT proof with verified algorithms, but trusts the compiler through `Lean.ofReduceBool` [S, [Lean 4.12.0 notes](https://lean-lang.org/blog/2024-10-3-lean-4120)].
- **Solvers are fallible.** YinYang found 45 confirmed bugs in Z3 and CVC4, 29 of them soundness bugs: Winterer, Zhang & Su, PLDI 2020, doi:10.1145/3385412.3385985 [S]. Also Mansur et al., ESEC/FSE 2020, doi:10.1145/3368089.3409763; Brummayer, Lonsing & Biere, SAT 2010, doi:10.1007/978-3-642-14186-7_6 [B].
- **Exemplars from 2025–2026.**
  - The Equational Theories Project decided all 22,028,942 implications between 4,694 magma laws. Every proof and countermodel was validated in Lean (Bolan et al. incl. Tao, [arXiv 2512.07087](https://arxiv.org/abs/2512.07087), 2025 [A]).
  - A solver returns certificates for both verdicts to a deterministic Lean judge, and its search stays outside the trusted base (Ma, Zhang & Cázares, [arXiv 2609.00706](https://arxiv.org/abs/2609.00706), 2026 [A]).
- **Covers:** P5 entirely, as a mechanism, and P3's confirmed/unconfirmed distinction.
  **Uncovered:** a way to grade checker agreement as consistency rather than truth; and exhaustiveness certificates without a SAT solver (see §3).

### 2.5 Vacuity, coverage and proof dependencies (P1, P3, P6)

- **Vacuity.**
  - Beer, Ben-David, Eisner & Rodeh, CAV 1997, doi:10.1007/3-540-63166-6_28; FMSD 18(2):141–163, 2001, doi:10.1023/A:1008779610539 [B].
  - Kupferman & Vardi, CHARME 1999, doi:10.1007/3-540-48153-2_8; STTT 4(2):224–233, 2003 [B].
  - Armoni et al., CAV 2003, doi:10.1007/978-3-540-45069-6_35 [B].
- **Coverage.**
  - Hoskote, Kam, Ho & Zhao, DAC 1999, doi:10.1145/309847.309936 [B].
  - Chockler, Kupferman & Vardi, TACAS 2001, doi:10.1007/3-540-45319-9_36; FMSD 28(3), 2006 [B].
  - Chockler, Kupferman, Kurshan & Vardi, CAV 2001, doi:10.1007/3-540-44585-4_7 [B].
  - Chockler, Kupferman & Vardi, CHARME 2003; STTT 8(4–5), 2006, doi:10.1007/s10009-004-0175-4 [B].
  - Kupferman, "Sanity Checks", CONCUR 2006, doi:10.1007/11817949_3 [B].
  - Chockler, Halpern & Kupferman, TOCL 9(3), 2008, doi:10.1145/1352582.1352588 [B].
  - Chockler, Kroening & Purandare, TCAD 31(5), 2012, doi:10.1109/TCAD.2011.2180382 [B].
- **Ball & Kupferman**, "Vacuity in Testing", TAP 2008, pp. 4–17, doi:10.1007/978-3-540-79124-9_2 [P]:
  - mutating the specification exposes vacuity; mutating the system exposes coverage;
  - Beer et al. report that about a fifth of specifications passed vacuously on first runs, and that vacuous passes always pointed to a real problem;
  - LTL vacuity detection is in PSPACE;
  - Hoskote's metric adapted mutation testing: a state is covered if flipping a variable's value there falsifies the specification;
  - a test suite passes vacuously if it would also pass a harder specification.
- **Kupferman, Li & Seshia**, FMCAD 2008, pp. 1–9, doi:10.1109/FMCAD.2008.ECP.29 [F]: a theory of relations among mutations, applied to vacuity, coverage and fault-tolerant circuits.
- **Deductive verification.**
  - Dafny 4.4 added `--warn-contradictory-assumptions` (a proof succeeded without using its goal) and `--warn-redundant-assumptions` (Tomb, [Dafny blog, 2023-10-27](https://dafny.org/blog/2023/10/27/proof-dependencies/) [F]).
  - Tomb & Joshi, "Static Coverage in Deductive Software Verification", FMCAD 2025, pp. 251–261 [S]: coverage is dual to vacuity; uncovered items are vacuously proved, unnecessary, or unconstrained.
  - ProofPulse, Silva, Martins & Mendes, [arXiv 2608.30818](https://arxiv.org/abs/2608.30818), 2026 [A]: a three-valued proof-coverage model.
- **Nitpick's consistency check.** Asked to falsify False under a set of axioms, Nitpick must find a model of the axioms; finding none suggests they are unsatisfiable [P, manual].
- **Covers:** P1 (which premises a verdict used), P6 (coverage by mutation), and a VACUOUS outcome for P3.
  **Uncovered:** coverage claims as claims with a standing; checked witnesses for coverage counterexamples.

### 2.6 Mutation analysis as test adequacy, and the equivalent-mutant problem (P6, P8)

- **Origin:** DeMillo, Lipton & Sayward, IEEE Computer 11(4):34–41, 1978, doi:10.1109/C-M.1978.218136 [B/S]. Mutation adequacy, the coupling effect, and the competent-programmer hypothesis.
- **Equivalent mutants are undecidable to detect** (Budd & Angluin, Acta Informatica 18(1):31–45, 1982, doi:10.1007/BF00625279). The attribution is read in Madeyski, Orzeszyna, Torkar & Józala, TSE 40(1):23–42, 2014, doi:10.1109/TSE.2013.44 [P].
  Mitigations: trivial compiler equivalence (Papadakis et al., ICSE 2015, doi:10.1109/ICSE.2015.103 [B]); Offutt & Craft, STVR 4(3), 1994 [B].
- **Validity of mutation scores.**
  - Mutant detection correlates with real-fault detection, controlling for coverage (Just et al., FSE 2014, doi:10.1145/2635868.2635929 [S]).
  - Subsumed mutants inflate results: about 62% Type I errors without countermeasures, and about 68% of surveyed studies were exposed (Papadakis et al., ISSTA 2016, doi:10.1145/2931037.2931040 [S]).
  - Mutant subsumption graphs: Kurtz et al., ICSTW 2014, doi:10.1109/ICSTW.2014.20 [B].
  - Higher-order mutants: Jia & Harman, IST 51(10), 2009, doi:10.1016/j.infsof.2009.04.016 [B].
  - Survey: Jia & Harman, TSE 37(5), 2011, doi:10.1109/TSE.2010.62 [B].
- **Counterexamples to the coverage of a verification.** Groce, Ahmed, Jensen & McKenney, ASE 2015, doi:10.1109/ASE.2015.40; with Holmes, *Automated Software Engineering* 25(4):917–960, 2018, doi:10.1007/s10515-018-0240-y [P].
  - Mutation analysis plus CBMC falsification shows what a "verification" actually verifies.
  - An unkilled mutant is a weakness in the falsifiability of the "theory" of program behaviour.
  - This is the closest prior art to P6.
- **Oracle assessment.**
  - Mutation reveals an oracle's false negatives; test generation reveals its false positives (Jahangirova, Clark, Harman & Tonella, ISSTA 2016, doi:10.1145/2931037.2931062 [S]).
  - Developers judge such oracle defects correctly only 29% of the time (TSE 47(8), 2021, doi:10.1109/TSE.2019.2934409 [S]).
  - Checked coverage: Schuler & Zeller, ICST 2011, doi:10.1109/ICST.2011.32 [B].
  - Pseudo-tested methods: Niedermayr et al. 2016, doi:10.1145/2896941.2896944; Vera-Pérez et al., EMSE 24(3), 2019, doi:10.1007/s10664-018-9653-2 [B].
- **Proof assistants.** Mutation analysis for Coq (Celik et al., ASE 2019, doi:10.1109/ASE.2019.00057 [B]). QuickChick runs tests over programmer-marked mutants [S, Software Foundations vol. 4].
- **Semantic mutation** mutates the language's semantics, modelling misreadings of the notation (Clark, Dan & Hierons, SCP 78(4):345–363, 2013, doi:10.1016/j.scico.2011.03.011 [S]). This is the analogue of counterworlds over "semantic rules" (P1, P7).
- **Specification mutation and model-checker test generation:** Ammann, Black & Majurski, ICFEM 1998, doi:10.1109/ICFEM.1998.730569; Black, Okun & Yesha, ASE 2000, doi:10.1109/ASE.2000.873653 [B].
- **Formal fault injection.**
  - Model checking decides which latches need soft-error protection; on SpaceWire it reduced protection's power overhead by 4.35× (Seshia, Li & Mitra, DATE 2007, doi:10.1109/DATE.2007.364501 [S]).
  - xSAP: Bittner et al., TACAS 2016, doi:10.1007/978-3-662-49674-9_31 [B].
- **Planted ground truth for evaluating bug finders:** LAVA, IEEE S&P 2016, doi:10.1109/SP.2016.15; Magma, SIGMETRICS 2021, doi:10.1145/3410220.3456276 [B].
- **Covers:** P6's mechanism and P8's plants.
  **Uncovered:** see §3. For closed, total programs, equivalence is decidable by running the mutant.

### 2.7 Abduction, assumption mining and weakest preconditions (P4)

- **Complexity.** Eiter & Gottlob, JACM 42(1):3–42, 1995, doi:10.1145/200836.200838 [F, [JACM abstract](https://projects.csail.mit.edu/jacm/References/eiterg1995:3.html)]. The basic abduction problems are complete for the second level of the polynomial hierarchy. Priorities raise some to the third. The minimality criteria are subset, cardinality, weight and priority. Also:
  - Bylander et al., AIJ 49, 1991, doi:10.1016/0004-3702(91)90005-5;
  - Selman & Levesque, AIJ 82, 1996, doi:10.1016/0004-3702(94)00069-7;
  - Creignou & Zanuttini, SICOMP 36(1), 2006, doi:10.1137/S0097539704446311;
  - Nordh & Zanuttini, AIJ 172(10), 2008 [B].
- **Abduction in program analysis.**
  - Dillig, Dillig & Aiken, PLDI 2012, pp. 181–192, doi:10.1145/2254064.2254087 [S]: queries ask the user for exactly the missing facts. They compute the smallest abductions (fewest variables) that are also the most general (weakest). In their user study, classification accuracy rose from 33% to 90%.
  - Explain tool: CAV 2013, doi:10.1007/978-3-642-39799-8_46 [S].
  - Abduction for invariants: OOPSLA 2013, doi:10.1145/2509136.2509511 [B].
  - Bi-abduction: JACM 58(6), 2011, doi:10.1145/2049697.2049700 [B].
  - Syntax-guided abduction (cvc5): IJCAR 2020, doi:10.1007/978-3-030-51074-9_9 [B].
- **Missing hypotheses in provers.**
  - **DrLA** (Gamboa, Manolios, Smith & Thompson, ACL2 2023, EPTCS 393:82–93, doi:10.4204/EPTCS.393.8 [A]). After ACL2s cgen counterexamples, it suggests hypotheses that make the theorem true, e.g. type predicates, by theory exploration and subsumption.
  - Brizhinev & Goré call for provers that perform abduction ([arXiv 1809.03162](https://arxiv.org/abs/1809.03162) [A]).
  - {log}'s `findh` command searches for missing hypotheses ([arXiv 2505.17350](https://arxiv.org/abs/2505.17350) [A]; `findh` itself [S]).
  - KIV: Reif, Schellhorn & Thums, IJCAR 2001, doi:10.1007/3-540-45744-5_52 [B].
  - "Learning to Disprove" removes a hypothesis from a Lean theorem; a counterexample to the result shows the hypothesis was essential (Li, Li, Yang, Ma & Su, [arXiv 2603.19514](https://arxiv.org/abs/2603.19514), 2026 [A]).
- **Environment assumptions.**
  - Chatterjee, Henzinger & Jobstmann, CONCUR 2008, doi:10.1007/978-3-540-85361-9_14 [B].
  - **Li, Dworkin & Seshia**, MEMOCODE 2011, pp. 43–50, doi:10.1109/MEMCOD.2011.5970509 [S]: for an unrealizable specification, they mine environment assumptions from a counter-strategy. This is the proposal's boundary example almost exactly.
  - Alur, Moarref & Topcu, FMCAD 2013, doi:10.1109/FMCAD.2013.6679387 [B].
  - Assumptions learned for compositional verification (L\*): Cobleigh, Giannakopoulou & Păsăreanu, TACAS 2003, doi:10.1007/3-540-36577-X_24 [B].
  - The weakest assumption: Giannakopoulou, Păsăreanu & Barringer, ASE 2002, doi:10.1109/ASE.2002.1114984 [B].
- **Preconditions.**
  - Weakest preconditions: Dijkstra, CACM 18(8), 1975, doi:10.1145/360933.360975 [B].
  - Seghir & Kroening, ESOP 2013, doi:10.1007/978-3-642-37036-6_25 [B].
  - PIE: PLDI 2016, doi:10.1145/2908080.2908099 [B].
  - **Astorga et al.**, PLDI 2019, doi:10.1145/3314221.3314641 [S]: preconditions that are safe and maximal *with respect to a test generator*. This is the honest form of "conditional on the search domain".
  - Necessary preconditions: Cousot et al., VMCAI 2013, doi:10.1007/978-3-642-35873-9_10 [B].
  - Uppar et al., [arXiv 2604.15533](https://arxiv.org/abs/2604.15533), 2026 [A]: contracts that are adequate for the client and pass a testing engine.
- **Requirements engineering.**
  - Obstacles are generated from goals and domain properties and resolved by changing goals or assumptions (van Lamsweerde & Letier, TSE 26(10):978–1005, 2000, doi:10.1109/32.879820 [S]).
  - Conflicts and boundary conditions: TSE 24(11), 1998, doi:10.1109/32.730542 [B]; Degiovanni et al., ICSE 2018, doi:10.1145/3180155.3180261 [B].
  - Model checking plus ILP learns operational requirements guaranteed to eliminate the counterexamples (Alrajeh, Kramer, Russo & Uchitel, ICSE 2009, doi:10.1109/ICSE.2009.5070527; TSE 39(3):361–383, 2013, doi:10.1109/TSE.2012.41 [S]).
- **Philosophy and argumentation.**
  - Lakatos, *Proofs and Refutations* (CUP, 1976), doi:10.1017/CBO9781139171472 [B]: counterexamples lead to incorporating the hidden lemma, i.e. "true of a narrower world".
  - Computational Lakatos: Pease et al., AIJ 246, 2017, doi:10.1016/j.artint.2017.02.006 [B].
  - In deductive argumentation, an argument's support must entail its claim by definition (Besnard & Hunter, AIJ 128, 2001, doi:10.1016/S0004-3702(01)00071-6 [B]).
- **Covers:** P4 entirely, as a problem.
  **Uncovered:** the abducibles for Ørlǫg, and the channel an abduced assumption would carry.

### 2.8 Property-based and metamorphic testing (P2, P8)

- **Random property testing:** QuickCheck, Claessen & Hughes, ICFP 2000, doi:10.1145/351240.351266 [B].
- **Exhaustive testing up to a depth:** SmallCheck, Runciman, Naylor & Lindblad, Haskell 2008, doi:10.1145/1411286.1411292 [S]. Feat, Haskell 2012, doi:10.1145/2364506.2364515 [B].
- **Hypothesis:** JOSS 4(43), 2019, doi:10.21105/joss.01891 [B].
- **QuickChick** proves in Coq the set of values a generator can produce (Paraskevopoulou et al., ITP 2015, doi:10.1007/978-3-319-22102-1_22 [B]). This bears directly on "explored domain = declared domain".
- **Generators and coverage:** Luck, POPL 2017, doi:10.1145/3009837.3009868; FuzzChick, OOPSLA 2019, doi:10.1145/3360607; combinatorial coverage, ESOP 2021, doi:10.1007/978-3-030-72019-3_10 [B].
- **Testing inside provers:** Isabelle Quickcheck (SEFM 2004, doi:10.1109/SEFM.2004.1347524; CPP 2012, doi:10.1007/978-3-642-35308-6_10); ACL2s cgen (EPTCS 70, 2011, doi:10.4204/EPTCS.70.1) [B].
- **Redex** found mistakes in all nine ICFP 2009 papers it modelled (Klein et al., POPL 2012, doi:10.1145/2103656.2103691 [S]).
- **Metamorphic testing** (R1b has Chen et al. 1998): surveys Segura et al., TSE 42(9), 2016, doi:10.1109/TSE.2016.2532875; Chen et al., ACM CSUR 51(1), online 2018, doi:10.1145/3143561 [B].
- **Covers:** P2 and P8. **Uncovered:** a standing, and an independent check of the property evaluator itself.

### 2.9 Counterfactual testing, causality, predictive analysis, assume-guarantee (P2, P4, P7)

- **Counterfactual testing.**
  - Causal testing uses counterfactual executions to isolate root causes (Johnson, Brun & Meliou, ICSE 2020, doi:10.1145/3377811.3380377 [S]).
  - Behavioural tests by perturbation (Ribeiro et al., ACL 2020, doi:10.18653/v1/2020.acl-main.442 [B]).
- **"The violated implication":**
  - Halpern & Pearl, BJPS 56(4), 2005 [B];
  - causality-based counterexample explanation, Beer et al., CAV 2009, doi:10.1007/978-3-642-02658-4_11 [B];
  - Groce et al., STTT 8(3), 2006, doi:10.1007/s10009-005-0202-0 [B];
  - Ball, Naik & Rajamani, POPL 2003, doi:10.1145/604131.604140 [B].
- **Predictive analysis.** Counterworlds anchored to one observed run: jPredictor, ICSE 2008, doi:10.1145/1368088.1368119; Smaragdakis et al., POPL 2012, doi:10.1145/2103656.2103702; Huang, Meredith & Roşu, PLDI 2014, doi:10.1145/2594291.2594315 [B].
- **Assume-guarantee.**
  - Misra & Chandy, TSE SE-7(4), 1981, doi:10.1109/TSE.1981.230844;
  - Jones, TOPLAS 5(4), 1983, doi:10.1145/69575.69577;
  - Pnueli 1985, doi:10.1007/978-3-642-82453-1_5;
  - Abadi & Lamport, TOPLAS 15(1), 1993, and 17(3), 1995;
  - McMillan, CHARME 1999, doi:10.1007/3-540-48153-2_30 [B]. Sound circular assume-guarantee; the earlier court's unread lead, still read here only as a record.
- **Symbolic execution and concolic testing** (worlds as solved path conditions): King, CACM 19(7), 1976, doi:10.1145/360248.360252; DART, PLDI 2005, doi:10.1145/1065010.1065036 [B].

### 2.10 Closer neighbours: counterexample search joined to standing, provenance or evidence (P1–P8)

| system | what it already does | gap against Ragnarök |
|---|---|---|
| **Isabelle Nitpick** (Blanchette & Nipkow, ITP 2010, doi:10.1007/978-3-642-14052-5_11 [B]; manual source [P]) | Five outcomes: *genuine*, *quasi-genuine* (genuine unless it contradicts a missing axiom or a dangerous option was used), *potentially spurious*, *none*, *unknown*. A documented list of cases that produce spurious counterexamples. An automatic mode runs on every newly entered theorem. A model-of-axioms consistency check | No claim standing; outcomes are tool messages |
| **Alive2** (Lopes et al., PLDI 2021, doi:10.1145/3453483.3454030 [B]; `llvm_util/compare.cpp` and `tools/transform.cpp` [P]) | Bounded success is worded only as *seeming* correct. A counterexample found under approximated semantics is reported as a failure to prove, not as a bug | No standing; the bound is not part of the verdict's type |
| **Imandra** (Passmore et al., IJCAR 2020, doi:10.1007/978-3-030-51054-1_30 [B]; docs [S]) | Counterexamples are reflected into the runtime as executable values (module `CX`). Bounded unrolling (`~upto`). Verify results separate proved, proved-up-to-a-bound, refuted and unknown ([S]; that docs page is now 404) | No provenance or channel discipline |
| **Dafny** (Chakarov et al., TACAS 2022, doi:10.1007/978-3-030-99524-9_23; Fedchin et al., NFM 2023 [B]) | Counterexamples, test generation, proof-dependency vacuity warnings (2.5) | No three-way verdict on claims |
| **Why3/SPARK and Frama-C** (Dailler et al., JLAMP 99, 2018, doi:10.1016/j.jlamp.2018.05.003 [B]; **Becker, Belo Lourenço & Marché**, F-IDE 2021, EPTCS 338:82–88, doi:10.4204/EPTCS.338.10 [P]; **Petiot et al.**, TAP 2016, doi:10.1007/978-3-319-41135-4_8, and FAC 30(6), 2018, doi:10.1007/s00165-018-0456-4 [S]) | An SMT counterexample is *validated* by run-time assertion checking under two semantics. A violation under normal semantics means the program is wrong. A violation only under the "giant-step" semantics (callees and loops replaced by anything their contracts allow) means the annotations are incomplete. Frama-C StaDy separates non-compliance, single or global contract weakness, and prover incapacity | **This is P4's classification, and the giant-step semantics is P2's "world consistent with the declared premises".** Missing: a court and a standing |
| **TLA+** (TLC: Yu, Manolios & Lamport, CHARME 1999, doi:10.1007/3-540-48153-2_6; Apalache: OOPSLA 2019, doi:10.1145/3360549 [B]; Quint [S]) | Finite-instance checking; Quint reports no violation found up to a maximum step count | The bound is a command-line parameter |
| **Resolute** (Gacek et al., HILT 2014, [arXiv 1409.4629](https://arxiv.org/abs/1409.4629) [A]) | An assurance-case language whose claims draw on formal analyses run on the architecture model (AGREE/JKind) | No countermodel standing |
| **Assurance 2.0** (Bloomfield & Rushby, [arXiv 2004.10474](https://arxiv.org/abs/2004.10474); with Netkachova, [arXiv 2405.15800](https://arxiv.org/abs/2405.15800); s(CASP) analysis, Murugesan et al., TPLP 24:805–824, 2024 [A]; eliminative induction, Goodenough, Weinstock & Klein, ICSE 2013, doi:10.1109/ICSE.2013.6606668 [S]; CoDefeater, Gohar et al., ASE 2024, doi:10.1145/3691620.3695296 [S]) | Explicit defeaters and counter-evidence. Confidence grows as doubts are eliminated (Baconian: eliminated over total). LLMs propose defeaters | **Closest to "SURVIVED as eliminated doubts"**, but defeaters are found by humans or LLMs, not by checked model search over a law |
| **Lara** (per prosecution-novelty N13; not re-read here) | Grounded semantics over declared claims; support is identity of normalized targets, **not entailment** | No countermodel search |
| **Hassan blog**, "Plausible Is Not Correct", Substack, **2026-10-24** [F, [link](https://aiwael.substack.com/p/plausible-is-not-correct)] | Verdicts Proved, Bounded pass, Not falsified, Counterexample, Vacuous, Unknown/error. A bounded pass is not a proof. Vacuity sanity checks include a deliberately broken version that must fail. Composed claims keep both qualifications (a partial order) | Not peer-reviewed. No separate check of counterexamples, no minimal assumptions, no coverage counterexamples. One day older than this survey |

**AI-generated code checked by countermodel search, 2023–2026**, all [A] except where noted:
- FormAI labelled 112,000 GPT-3.5 C programs with ESBMC counterexamples (Tihanyi et al., PROMISE 2023, doi:10.1145/3617555.3617874).
- Clover checks consistency among code, docstrings and annotations ([arXiv 2310.17807](https://arxiv.org/abs/2310.17807)).
- nl2postcond judges generated postconditions by correctness and by discriminative power over buggy mutants (Endres et al., FSE 2024, [arXiv 2310.01831](https://arxiv.org/abs/2310.01831)).
- Symbolic testing of specifications for intent formalization (Lahiri, FMCAD 2024, [arXiv 2406.09757](https://arxiv.org/abs/2406.09757)).
- Lemur: a calculus in which LLM proposals are checked, proved sound (ICLR 2024, [arXiv 2310.04870](https://arxiv.org/abs/2310.04870)).
- AlphaVerus filters misaligned specifications against reward hacking ([arXiv 2412.06176](https://arxiv.org/abs/2412.06176)).
- REFUTE: models create counterexamples to incorrect solutions, validated by execution; the best manage fewer than 9% ([arXiv 2502.19414](https://arxiv.org/abs/2502.19414)).
- CLEVER excludes specifications that allow vacuous solutions ([arXiv 2505.13938](https://arxiv.org/abs/2505.13938)).
- **Agentic Model Checking** (Sun, Liu, Kroening & Xue, [arXiv 2605.21434](https://arxiv.org/abs/2605.21434), May 2026):
  - agents propose and BMC decides every soundness-relevant question;
  - callees are replaced by stubs constrained only by their postconditions, i.e. worlds allowed by the declared premises;
  - counterexamples pass validation (reachability, callee feasibility, dynamic replay, realism audit);
  - each is classified as an *active in-tree* crash or a *latent public-API* failure. The latter is the proposal's "theorem true of a narrower world".
- Containment verification uses an information barrier against tautological specifications ([arXiv 2605.09045](https://arxiv.org/abs/2605.09045)).
- LLM-written RTL assertions are rejected by mutation when vacuous or not discriminating ([arXiv 2606.21451](https://arxiv.org/abs/2606.21451)); an RTL repair pipeline reports bounded-cover vacuity ([arXiv 2607.28877](https://arxiv.org/abs/2607.28877)).
- **Faults in Our Formal Benchmarking** (ICML 2026, [arXiv 2606.29493](https://arxiv.org/abs/2606.29493)): 398 mechanically certified issues in Lean benchmarks, including counterexamples, vacuous theorems, unsound axioms and missing hypotheses.
- **SWE-Proof** ([arXiv 2609.21190](https://arxiv.org/abs/2609.21190)): a quarter of test-passing patches admit counterexamples. Only 56% of specifications written by agents pass audit. The usual failure is a specification that constrains part of the behaviour and leaves the rest free, which is a coverage gap.

## 3. Feasibility in Ørlǫg as it stands (closed, total runs)

1. **What a "world" can mean when a run takes no input.** Four notions, each with its prior art.
   - **W1, inference worlds (needs nothing new).**
     - A world is a valuation of the variables a claim and its declared premises mention, over a declared finite domain. A counterworld makes every premise's condition true and the claim's false.
     - It tests whether the **declared support entails the claim**. Prior art: Alloy's facts-to-assertion check, Becker's giant-step semantics, Besnard–Hunter's entailment requirement.
     - It attacks DOCTRINE §8's admitted blind spot: undeclared dependence is invisible.
     - Example: Plankton §3 (plan equals robot, given §4: robot equals 7) has the counterworld plan = 1, robot = 7. This finding is orthogonal to CIRCULAR.
     - Open point: SPEC item 32 lets a premise be a later clause or the claim itself, so W1 needs a declared **frame rule** saying which state a variable denotes. Rely-guarantee and `old()` solve the same problem.
   - **W2, parameter worlds (needs a domain declaration).**
     - Designated literals range over finite sets. A counterworld is a completed run in which the target's premises evaluate true and the target false.
     - It is replayable byte for byte on all four executions.
     - Cost is |D| runs, each up to the fuel bound. The proposal's boundary example needs W2 or capability inputs.
   - **W3, defect worlds (P6).**
     - Mutants drawn from a finite operator set. For a closed, total law, whether a mutant changes the output is **decidable by running it**: Budd–Angluin's undecidability needs unbounded inputs.
     - So equivalent plants are detectable per corpus program.
     - Claims about all laws (a backend over every program) fall back to Rice; they can be at most SURVIVED over a corpus.
   - **W4, semantic worlds (backend equivalence).**
     - Alternative rules for rounding, contraction or NaN canonicalization.
     - Prior art: semantic mutation; translation validation (Pnueli, Siegel & Singerman, TACAS 1998, doi:10.1007/BFb0054170; Necula, PLDI 2000, doi:10.1145/349299.349314 [B]); bounded translation validation (Alive2).
2. **The checker.**
   - The generator and the checker must not share an evaluator. For example, the generator uses the reference, and the checker replays each witness on the backends, which the arbiter already runs.
   - With no SAT/DRAT path under the dependency rule, SURVIVED's certificate is the enumeration itself. An independent re-enumeration must produce the same world count and the same hash chain of per-world verdicts, which is a receipt.
   - Generator and checker written by one model family give consistency, not truth (DOCTRINE §8).
3. **Plants.** These mirror SV-COMP's handcrafted validation tasks and LAVA/Magma; the domain is calibrated by Andoni et al.'s criterion.
   - A world in D that falsifies the claim must give FALSIFIED with that world.
   - A claim that fails only just outside D must give SURVIVED(D) and nothing more.
   - Premises unsatisfiable in D must give VACUOUS.
   - A fake witness must be refused (UNRESOLVED).
   - A skipped world must break the receipt.
4. **Standing.**
   - FALSIFIED and SURVIVED(D) are computation-channel results. They can lower a claim, never ground one (T2).
   - A universal standing needs a theorem-channel claim, a cutoff or small-model theorem, ratified on its own seal. Scope sufficiency is undecidable in general (Oetsch et al. 2012).

## 4. Limits of this survey

- dblp sits behind a bot challenge, which was not bypassed. Semantic Scholar and, near the end, the arXiv API were rate-limited.
- The Barendregt & Wiedijk PDF refused the connection; Imandra's result-type page now returns 404.
- [S] items rest on search extracts; [B] items' contents are stated from memory.
- Not confirmed here: Owre's random testing in PVS; Mills 1972 error seeding; Kusner et al. 2017; the Parsons–Wooldridge–Amgoud complexity results (the PDF did not download).

---

## (a) Graded novelty of Ragnarök's possible contributions

| # | possible contribution | grade | nearest prior art | queries |
|---|---|---|---|---|
| 1 | Bounded counterworld search over a law's claims | **NOT NEW** | Jackson & Damon 1996; Alloy; BMC; Nitpick; QuickCheck/SmallCheck; ACL2s cgen; Imandra | Q9 |
| 2 | FALSIFIED / SURVIVED / UNRESOLVED; bounded is not universal; an approximated counterexample is not a falsification | **NOT NEW** | Nitpick's five outcomes; Alive2's statuses; SV-COMP confirmed/unconfirmed; Imandra; three-valued model checking (Bruns & Godefroid, CAV 1999, doi:10.1007/3-540-48683-6_25 [B]); Alloy; Hassan 2026 | Q1, Q9 |
| 3 | A small separate checker for every witness | **NOT NEW** | Namjoshi 2001; Kupferman & Vardi 2005; SV-COMP validators 2015–2025; PCC; the de Bruijn criterion; T1 | Q10 |
| 4 | A certificate for SURVIVED: an independent re-enumeration receipt in the language's own hash-chained receipt format | **PARTLY NEW** (the certificate idea exists: DRAT/LRAT, cake_lpr, CPOG, `bv_decide`, ETP; the receipt-as-certificate form was not found) | 2.4 | Q5, Q10 |
| 5 | Identifying the premises, axioms and rules a conclusion depends on | **NOT NEW** | N10's per-theorem assumption tracking; Dafny proof dependencies; static coverage; Alloy unsat cores | Q9 |
| 6 | The smallest set of additional assumptions | **NOT NEW** as a problem or as methods; a guaranteed minimum exists only for tiny instances, see (b) | Eiter–Gottlob; Dillig et al.; DrLA; Li–Dworkin–Seshia; Alrajeh et al.; obstacles; Lakatos | Q3, Q8 |
| 7 | Classifying a counterworld as defect, missing lemma or narrower world | **NOT NEW** | Petiot et al.; Becker et al.; IC3 CTIs; Agentic Model Checking 2026 | Q3, Q7 |
| 8 | Counterexamples to declared coverage (a defect of class D that passes the guard) | **NOT NEW** as a mechanism | DeMillo et al.; Hoskote; Chockler et al.; Kupferman–Li–Seshia; Ball–Kupferman; **Groce et al. 2015/2018**; OASIs; mutation analysis for Coq | Q2 |
| 9 | Applying it to the language's own refusal completeness and backend equivalence | **NOT NEW** as mechanisms | translation validation; Alive2; differential testing (R1b); the door fuzz | — |
| 10 | Entailment of *declared* support as a standing beside the Kripke–Kleene court ("well-founded, not entailed"), witnessed by a checked counterworld | **NOT FOUND** (absence of evidence) | Besnard–Hunter (entailment by definition); Lara (identity, not entailment); Alloy; giant-step semantics | Q4, Q1 |
| 11 | Bounded verdicts typed by channel, liftable only through a cutoff or small-model theorem ratified on the claim's own seal | **NOT FOUND** | cutoffs and small-model theorems; CBMC unwinding assertions; Imandra's proved-up-to; Hassan's partial order | Q5, Q1 |
| 12 | Coverage, refusal-completeness and backend-equivalence claims as first-class claims of the language about itself, each with a checked witness and a channel | **NOT FOUND** (combination of #3 and #8) | Groce et al.; SV-COMP; Dafny's backend tests (R2) | Q2, Q1 |

**Queries run** (WebSearch unless marked):
- **Q1.** `programming language claims "counterexample search" verdict "falsified" "survived" "unresolved" bounded not proof standing evidence court` (extended).
- **Q2.** `"counterexample to coverage" OR "coverage claim" falsify guard "catches every" defect class mutation formal search witness checker` (extended).
- **Q3.** `automatically discover missing assumptions theorem "holds only" narrower world counterexample environment assumption "hidden assumption" detection formal specification countermodel` (extended).
- **Q4.** `argumentation support relation entailment checked by model finder counterexample "declared premises" claims "well-founded" support graph runtime claims language` (extended).
- **Q5.** `bounded verification result lifted to unbounded proof by "small model theorem" OR "cutoff theorem" trusted assumption tagged provenance theorem prover integration bounded check certificate` (extended).
- **Q6.** `assurance case defeaters automated search model checker counterexample "Assurance 2.0" Clarissa s(CASP) defeater confirmation 2024 2025`.
- **Q7.** `2026 LLM-generated code verification counterexample search independent checker specification vacuity "countermodel" OR "counterexample" arXiv` (extended).
- **Q8.** arXiv API: `abs:"counterexample" AND abs:"LLM" AND abs:"vacuous"`; `abs:"countermodel" AND (abs:"LLM" OR abs:"language model")`; `abs:"missing assumption" AND abs:"counterexample"` (no hits).
- **Q9.** Tool queries for Nitpick's genuine/spurious outcomes, Alloy's "may be valid" message, CBMC unwinding assertions, Alive2's verdict wording, Imandra's `upto` bound, Quint's no-violation message, Dafny's `--warn-contradictory-assumptions`, Resolute/AGREE, and Lean `bv_decide`/LRAT.
- **Q10.** `SV-COMP 2025 competition report witness validation results confirmed only if validator confirms witness scoring`; Beyer–Strejček SAS 2022.

Citations were verified through the Crossref and arXiv APIs.

## (b) Hardness results that bound what Ragnarök can promise

1. **Verdict asymmetry.** Over a succinct finite domain, finding a counterworld is NP and its absence is coNP-complete (Cook, STOC 1971, doi:10.1145/800157.805047 [B]). FALSIFIED is cheap to check, by replaying one world. SURVIVED needs exhaustive search or a proof.
2. **Machine integers.** Quantifier-free bit-vector logic with binary-encoded widths is **NEXPTIME-complete** (Kovásznai, Fröhlich & Biere, ToCS 59(2):323–376, 2016, doi:10.1007/s00224-015-9653-1 [S]). Explicit enumeration costs ∏|Dᵢ| runs, each up to loop bounds of 2^62.
3. **Model checking.**
   - LTL model checking is PSPACE-complete (Sistla & Clarke, JACM 32(3), 1985, doi:10.1145/3828.3837 [B]).
   - CTL is linear in |M|·|f| (Clarke, Emerson & Sistla, TOPLAS 8(2), 1986, doi:10.1145/5397.5399 [B]), but |M| is exponential in the number of variables.
   - SAT-based BMC is doubly exponential, one exponent above LTL model checking (Clarke et al. 2004 [S]).
   - LTL vacuity detection is in PSPACE (Ball & Kupferman [P]).
4. **Scope sufficiency is undecidable**, even for function-free Horn programs (Oetsch et al. KR 2012, Thm 1 [P]).
5. **Coverage over all programs** is undecidable: Rice, TAMS 74(2):358–366, 1953, doi:10.1090/S0002-9947-1953-0053041-6 [B]; equivalent mutants, Budd & Angluin 1982. Over a closed, total corpus it is decidable, at run cost.
6. **Abduction** is Σ2P/Π2P-complete in its basic forms, and priorities reach the third level (Eiter & Gottlob 1995 [F]).
7. **The shortest conjunction of literals that, with the premises, implies the conclusion** (a shortest implicant) is Σ2P-complete. It is Σ2P-hard to approximate within n^(1/2−ε) for formula input and n^(1−ε) for circuit input (Umans, JCSS 63(4):597–611, 2001, doi:10.1006/jcss.2001.1775 [S]).
8. **The smallest subset of declared premises that still yields the conclusion** (a smallest unsatisfiable subset) is Σ2P-complete (Liberatore, AIJ 163(2), 2005, doi:10.1016/j.artint.2004.11.002, via secondary sources [S]). Recognizing a minimal unsatisfiable set is DP-complete (Papadimitriou & Wolfe, JCSS 37(1), 1988, doi:10.1016/0022-0000(88)90042-6 [S]).
9. **Over explicit counterworlds and a finite vocabulary of candidate assumptions:**
   - choosing the fewest assumptions that exclude every counterworld is minimum hitting set, which is NP-hard;
   - no polynomial-time (1−ε)·ln n approximation exists unless P = NP (Dinur & Steurer, STOC 2014, doi:10.1145/2591796.2591884 [S]; Feige, JACM 45(4), 1998, doi:10.1145/285055.285059 [S]);
   - minimal diagnoses are minimal hitting sets (Reiter, AIJ 32(1), 1987, doi:10.1016/0004-3702(87)90062-2 [B]).
10. **"There exists an assumption such that for every world"** is 2QBF, Σ2P-complete (Stockmeyer, TCS 3(1), 1976, doi:10.1016/0304-3975(76)90061-X [B]). CEGIS (Solar-Lezama et al., ASPLOS 2006, doi:10.1145/1168918.1168907 [B]) is the practical loop, with no polynomial guarantee.
11. **Ill-posedness.** Without a vocabulary of abducibles, the "smallest" assumption is trivial: the negation of the counterworlds, or premises → conclusion itself.

## (c) Three design lessons a first version must not ignore

1. **Certify both sides, and treat the checker as fallible. SURVIVED is where tools lie.**
   - Every serious tool separates *found* from *confirmed*: Nitpick's quasi-genuine and potential; Alive2's approximation refusal; SV-COMP's correct-unconfirmed; Becker's validation by run-time assertion checking.
   - The costly error is the wrong proof: −32 against −16 in SV-COMP.
   - A clean result can be vacuous (Alloy; Beer et al.; Dafny's contradictory-assumption warning).
   - Validators confirm invalid witnesses (2022), and their ground truth is a vote.
   - So the first version should ship four things:
     - a witness replay on a different evaluator;
     - an exhaustiveness receipt for SURVIVED, re-enumerated independently;
     - a VACUOUS outcome, required when the premises have no model in D, mirroring Ørlǫg's own VACUOUS;
     - plants for the searcher and the checker: a fake witness and a skipped world.
   - Checker agreement is graded as consistency.
2. **The domain is part of every verdict; calibrate it and never lift it by computation.**
   - BMC's thresholds, CBMC's unwinding assertions, Alloy's scope, Imandra's proved-up-to and Quint's step limit all qualify bounded success.
   - Scope sufficiency is undecidable (Oetsch et al.).
   - The small-scope evidence itself contains the warning. Kill rates kept rising after coverage saturated; one bug needed scope 5 where every tree up to 4 passed; DynamoDB bugs needed 35-step traces.
   - So SURVIVED must print D (with the fuel budget), and D should be calibrated by plants (Andoni et al.'s criterion).
   - A universal standing should enter only as a theorem-channel cutoff or small-model claim, ratified on the claim's own seal (T2).
3. **A diagnosis is a new claim, typed and vocabulary-bound, never a verdict the search grants itself.**
   - Prior art separates three causes of a counterworld:
     - a real defect (non-compliance);
     - an unstated lemma the program in fact satisfies (subcontract weakness; a CTI blocked by an inductive clause);
     - a genuine restriction of the world (obstacle; latent public-API failure).
   - Each needs a different repair.
   - "Smallest additional assumption" is trivial without abducibles and Σ2P-hard with them, so the vocabulary must be declared:
     - type predicates (DrLA);
     - fewest variables plus weakest (Dillig);
     - mined templates (Li–Dworkin–Seshia);
     - ILP language bias (Alrajeh);
     - inductive clauses (IC3).
   - In Ørlǫg, an abduced assumption cannot be supported by the search that proposed it, which would be circular. It enters as an owner-ratified assumption bound to its own seal, or as a lemma that must itself survive the court.
   - For coverage claims, the same discipline applies to "defects": a missed defect must be shown non-equivalent by a distinguishing run, and the mutant class enumerated without subsumption inflation (Papadakis et al. 2016).
