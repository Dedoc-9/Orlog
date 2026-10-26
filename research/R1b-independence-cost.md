# R1b: verifier independence, correlated judges, cost of checking

ØRLǪG fact check, 2026-10-25; no design. Tags: **CHECKED-P** read in the primary source or the authors' full text; **CHECKED-S** read in a named secondary source; **MEMORY** not confirmed here. Bearing: *(a)* a verifier shares the generator's blind spots; *(b)* checking is cheaper than generating.

## 1. Data processing inequality
If X → Y → Z is a Markov chain (p(x,y,z) = p(x)p(y|x)p(z|y)), then I(X;Y) ≥ I(X;Z), with equality iff I(X;Y|Z) = 0; since X → Y → g(Y) for any function g, I(X;Y) ≥ I(X;g(Y)). The corollary I(X;Y|Z) ≤ I(X;Y) needs the chain: independent fair bits X, Y with Z = X+Y give I(X;Y) = 0 < I(X;Y|Z) = ½. Cover & Thomas, *Elements of Information Theory*, Wiley 1991; 2nd ed. 2006, §2.8, Thm 2.8.1.

*(a)* A verifier whose only route to the truth X runs through the generator's artefact Y cannot know more about X than Y does; a digest g(Y) carries no more truth than its bytes. Independence needs a channel to X that bypasses Y.

CHECKED-S (the book's contents page; Thm 2.8.1 as used in Stanford EE276 solutions); corollary wording MEMORY.

## 2. Aumann 1976, "Agreeing to disagree"
(Ω, 𝔅, p) is a probability space, p the *common prior*; P₁, P₂ are partitions whose join consists of positive-probability events; at state ω person i learns the cell Pᵢ(ω). E is *common knowledge* at ω iff E contains the cell of the meet P₁∧P₂ (finest common coarsening) containing ω. If it is common knowledge at ω that p(A|P₁(ω)) = a and p(A|P₂(ω)) = b, then a = b. Mutual knowledge of the posteriors is not enough (a four-state counterexample); the partitions are tacitly common knowledge; no finiteness is assumed. *Annals of Statistics* 4(6):1236–1239.

*(a)* Verifiers sharing a prior and exchanging posteriors must agree whatever their evidence, so their agreement certifies nothing; Aumann traces real disagreement to ascribed errors or biases.

CHECKED-P.

## 3. Correlated votes, coincident failures
**Condorcet** (1785, *Essai sur l'application de l'analyse…*). Simple majority on a binary question; the events "voter i is right" independent, each of probability p > ½: for odd n the majority's accuracy rises with n and tends to 1. CHECKED-S (Stanford Encyclopedia, "Jury Theorems").

**Ladha 1992** (*Am. J. Political Science* 36:617–634): sufficient conditions for both conclusions as an upper bound on the *average* pairwise correlation of votes (Corollary, p. 628). CHECKED-S (Kaniovski 2010; Pivato 2016); the inequality NOT seen. Perfect correlation reduces a jury to one juror; Pólya-urn contagion (Berg 1993) defeats the asymptotic part.

**Knight & Leveson 1986** (*IEEE TSE* SE-12(1):96–109): 27 independently written versions of one specification (Virginia, UC Irvine), one million random tests against a gold version. Inputs failing two or more versions far exceeded the independence prediction, and independence was rejected (99% level, per secondary accounts). Yet the average 2-out-of-3 system was an order of magnitude more reliable than the average version, though some were worse than some single versions. CHECKED-P (abstract); CHECKED-S (Littlewood, Popov & Strigini, *ACM Comput. Surv.* 33(2):177–208, 2001: "LPS").

**Eckhardt & Lee 1985** (*IEEE TSE* SE-11(12):1511–1517): programs are random draws; *difficulty* θ(x) = probability that a random program fails on x. Independent draws give P(both fail | x) = θ(x)², yet over random inputs P(both fail) = E[θ²] = (Eθ)² + Var θ, above independence unless θ is constant. CHECKED-S (LPS).

**Littlewood & Miller 1989** (*IEEE TSE* 15(12):1596–1614): methodologies A, B give P(both fail) = Eθ_A·Eθ_B + Cov(θ_A, θ_B), beating independence when the covariance is negative; EL is the most pessimistic case. In 1-out-of-n systems spread methodologies evenly; in 2-out-of-3 voting, diversity can be worse than none. CHECKED-S (LPS).

*(a)* Process independence is not failure independence; dependence "must be measured" (LPS).

## 4. Program checkers; self-testing/correcting
**Blum & Kannan** (STOC 1989, 86–97; *J. ACM* 42(1):269–291, 1995). A checker is a probabilistic expected-polynomial-time oracle program C: for every program P halting everywhere, instance x and security parameter k (unary), if P is correct everywhere then C^P(x,k) says CORRECT, and if P(x) ≠ π(x) it says BUGGY, each with probability ≥ 1−2^−k. Through interactive proofs with oracle-simulable provers, all PSPACE-complete problems are checkable. CHECKED-S (Arvind & Torán 1996, Def. 4; McConnell et al. 2011; Fortnow 2004); BK95 not read.

**Little-oh.** Wasserman & Blum (*J. ACM* 44(6):826–849, 1997) define the *simple checker*, credited to Blum's ICSI TR-88-009 (1988): decide whether y = f(x) in time o(T(n)), T the least possible (informally, least known) time for f. Their reason: besides efficiency, the bound bars recomputing f, so the checker must differ from the program; they grade the resulting error independence a "heuristic contention" and concede that shared subroutines or hardware can still correlate errors. BLR's *different* is the same rule: incremental time (calls to P excluded) below the fastest known program (their introduction: any correct program), since after Blum 88 a quantifiably different checker is unlikely to err the same way. CHECKED-P. An o(·) clause in BK's own definition is NOT CONFIRMED: Arvind & Torán say BK stressed efficiency; McConnell et al. and Fortnow give polynomial time.

**BLR** (STOC 1990, 73–83; *JCSS* 47(3):549–595, 1993). A self-tester w.h.p. passes P if it errs on at most a β₁ fraction of a distribution and fails it at β₂ or more; a self-corrector computes f(x) correctly w.h.p. for *every* x from a mostly-right P, via random self-reducibility (f(x) is an easy function of f at points each uniformly distributed). Linear f: test P(x+y) = P(x)+P(y); over finite groups rejection ≥ (2/9)·(distance to the nearest homomorphism) (BLR with Coppersmith), over GF(2) ≥ distance (Bellare, Coppersmith, Håstad, Kiwi & Sudan, FOCS 1995). Correct with P(x+r) − P(r): error ≤ 2ε when P is ε-close (union bound). CHECKED-P (BLR; BCHKS).

*(a)+(b)* The o(·) rule buys cheapness and forbids recomputation, but its authors call the independence it buys heuristic. Self-correction gives every-input correctness at constant-factor cost.

## 5. Freivalds; Schwartz–Zippel
**Freivalds** ("Probabilistic machines can use less running time", *Information Processing 77*, IFIP, 839–842, 1977). For n×n matrices draw x uniform in {0,1}ⁿ and compare A(Bx) with Cx, O(n²); if AB ≠ C, acceptance has probability ≤ ½, so k trials err with probability ≤ 2^−k, one-sidedly. CHECKED-S (McConnell et al. 2011).

**Schwartz–Zippel.** P ∈ F[x₁,…,xₙ] nonzero of total degree d, S ⊆ F finite, r uniform on Sⁿ: Pr[P(r) = 0] ≤ d/|S|. Schwartz, *J. ACM* 27(4):701–717, 1980 (this bound); Zippel, EUROSAM '79, LNCS 72 (per-variable degree); DeMillo & Lipton, *IPL* 7(4):193–195, 1978 (earlier, weaker). CHECKED-S (Lipton 2009; Isabelle AFP).

*(b)+(a)* Checking costs O(n²) or one evaluation, and the bound holds against *every* wrong claim because it is over the checker's private coins: independence by randomness, valid only if the challenge is drawn after the claim and hidden from its maker.

## 6. Certifying algorithms; de Bruijn; PCC; translation validation
**McConnell, Mehlhorn, Näher & Schweitzer** (*Computer Science Review* 5(2):119–161, 2011). Output y comes with a witness w; the witness predicate must imply the postcondition, be trivial to evaluate (*checkability*), and have a simple proof (*simplicity*); checkers should be correct, ideally linear-time, and simple. Examples: bipartiteness (a 2-colouring or an odd cycle); gcd (g = xa + yb with g dividing a and b); shortest paths with positive costs (D(s) = 0, D(v) ≤ D(u) + c(u,v) on every edge, a tight edge into each v ≠ s); LP duality (feasible primal and dual with equal objectives are optimal). Thm 5: with a formal correctness proof, every deterministic program with trivial precondition has an efficient certifying counterpart; Thm 6: some behaviours with nontrivial preconditions cannot be certified. CHECKED-P (2010 preprint).

**de Bruijn criterion:** proofs independently checkable by a small program (Barendregt & Wiedijk, *Phil. Trans. R. Soc. A* 363:2351–2375, 2005). CHECKED-P.

**Proof-carrying code:** code ships with a proof that it obeys the host's safety policy, which the host checks cheaply (Necula, POPL '97, 106–119). CHECKED-S.

**Translation validation:** check each compiler run, not the compiler, against a common semantics and a refinement relation (Pnueli, Siegel & Singerman, TACAS 1998, LNCS 1384, 151–166). CHECKED-S.

*(b)* The producer searches; the consumer runs a short check judged on its own. What is proved is the formal postcondition, not that it is the intended one.

## 7. Newman's lemma
In a terminating abstract rewriting system, local confluence (every fork b ← a → c rejoins) implies confluence, hence unique normal forms. Weak normalization is not enough: b→a, b→c, c→b, c→d. Newman, *Annals of Mathematics* 43:223–243, 1942; short proof Huet, *J. ACM* 27(4):797–821, 1980. CHECKED-S (counterexample checked by hand).

*(b)* Order-independence reduces to checking one-step forks plus a termination proof, which carries the global weight.

## 8. Rado–Edmonds theorem
For a nonempty subset-closed family 𝓘 on a finite S: (S, 𝓘) is a matroid iff for every w : S → ℝ₊ the greedy algorithm (add the heaviest y keeping I + y ∈ 𝓘) ends at a maximum-weight member. Schrijver (*Combinatorial Optimization*, 2003, Thm 40.1) credits Rado 1957 (*Proc. LMS*) with matroid ⇒ greedy, and Gale 1968 and Edmonds 1971 (*Math. Programming* 1) with the converse. CHECKED-P. Rank: 0 ≤ r(X) ≤ |X|, monotone, r(X∪Y) + r(X∩Y) ≤ r(X) + r(Y). Closure: extensive, monotone, idempotent, and y ∈ cl(X+x) − cl X ⇒ x ∈ cl(X+y). MEMORY (Oxley, *Matroid Theory*).

*(b)* Only on matroids does local greedy acceptance certify global optimality under every weighting.

## 9. Propp & Wilson 1996, coupling from the past
For an ergodic finite chain driven by i.i.d. random maps, compose the maps from time −T to 0; if the composite is constant, its value is exactly stationary; otherwise go further back, reusing the randomness already drawn. Monotone case: a partial order with bottom 0̂ and top 1̂ and an update with x ≤ y ⇒ φ(x,U) ≤ φ(y,U); once the runs from 0̂ and 1̂ meet by time 0, every sandwiched run has met, so two runs suffice (T = 1, 2, 4, …; overshooting is harmless). *Random Structures & Algorithms* 9(1–2):223–252. CHECKED-P (preprint).

*(b)* Two extremal runs certify a claim about all starting states, with an exact, self-determined stopping time.

## 10. Contextuality as failure to glue
Abramsky & Brandenburger (*New J. Phys.* 13:113036, 2011): a model's supports form a presheaf over a cover of measurement contexts; non-locality or contextuality is the absence of a global section consistent with all local ones (Bell < Hardy < GHZ in strength). Abramsky, Mansfield & Barbosa (*EPTCS* 95:1–14, 2012): a local section's Čech-cohomology obstruction (an abelian presheaf over ℤ) vanishes when a global section extends it, so nonvanishing witnesses contextuality, sufficiently but not necessarily: nonzero for the PR box, GHZ, Peres–Mermin and an 18-vector Kochen–Specker set; zero for the contextual Hardy model. CHECKED-P.

*(a)* Views agreeing on every overlap need not glue; the cheap witness can only refute, and its silence proves nothing.

## 11. PCP theorem
NP = PCP(O(log n), O(1)): each NP language has a polynomial-time verifier that, with O(log n) coins and O(1) queries to a purported proof, accepts some proof surely when x ∈ L and any proof with probability ≤ ½ when x ∉ L. Arora & Safra, *J. ACM* 45(1); Arora, Lund, Motwani, Sudan & Szegedy, *J. ACM* 45(3), 1998 (FOCS 1992); Dinur, *J. ACM* 54(3), 2007. CHECKED-S.

*(b)* The prover must re-encode the proof, and soundness is over the verifier's coins. Related: Goldwasser, Kalai & Rothblum (STOC 2008) verify depth-d uniform circuits in (n + d)·polylog n time against a poly(n) prover (CHECKED-S).

## 12. Oracle problem; metamorphic, differential testing
Barr, Harman, McMinn, Shahbaz & Yoo (*IEEE TSE* 41(5):507–525, 2015): the oracle problem is telling correct from incorrect behaviour on an input; oracles are specified, derived (pseudo-oracles, i.e. independent alternative versions, after Davis & Weyuker 1981; N-version majority; metamorphic relations), implicit, or human. A preprint's full text never cites Knight & Leveson. CHECKED-P. Metamorphic testing derives follow-up tests from passed ones through relations a correct program must satisfy (e.g. e^a·e^−a = 1), with no oracle (Chen, Cheung & Yiu, HKUST-CS98-01, 1998; CHECKED-P). Differential testing runs one input through comparable implementations and flags disagreement (McKeeman, *Digital Technical Journal* 10(1):100–107, 1998; citation CHECKED-S, content MEMORY).

*(a)* Agreement among independent builds serves as the oracle: the Knight–Leveson setting. Metamorphic relations check necessary conditions only.

## Obscure results
1. **Verifier diversity.** Littlewood, Popov, Strigini & Shryane (*IEEE TSE* 26(12):1157–1167, 2000) carry EL/LM over to fault-finding procedures: repeated applications of one procedure are not independent, and assuming so is always optimistic. It models diverse verifiers, not generators. CHECKED-S.
2. **Shared evidence caps a jury.** Dietrich & List (*Synthese* 142(2):175–202, 2004): with common evidence, majority accuracy tends to P(evidence not misleading), usually below 1. Dietrich & Spiekermann (2013), assuming independence given the common causes and a weak competence condition, get P(facts truth-conducive) + ½·P(facts neutral). CHECKED-S.
3. **Pairwise correlation underdetermines majority accuracy.** Kaniovski (*Theory and Decision* 69(3):453–468, 2010): equal competence and pairwise correlation do not fix the majority's accuracy; in one family correlation has no effect, under Bahadur's law positive correlation hurts, and linear programs bound it. Pairwise agreement cannot measure what aggregation buys. CHECKED-P (preprint).
4. **Dependent sources have a ceiling.** Clemen & Winkler (*Operations Research* 33(2):427–442, 1985): positive dependence sharply cuts precision and value, and many sources may fall well short of perfect information. Illustration (attribution MEMORY): n estimates with error correlation ρ are worth n/(1 + (n−1)ρ) < 1/ρ independent ones. CHECKED-S.
5. **Similar models judge kindly.** Goel et al. (ICML 2025, arXiv:2502.04313): by CAPA (chance-adjusted error overlap), LLM judges favour models similar to themselves at fixed capability, and errors grow more alike as capability rises. Current empirical evidence for *(a)*. CHECKED-P (abstract).
6. **Sublinear checks certify only closeness.** Ergün, Kannan, Kumar, Rubinfeld & Viswanathan, "Spot-checkers" (*JCSS* 60(3):717–751, 2000): time o(|input| + |output|), passing correct outputs and failing outputs far from correct, each w.p. ≥ ¾; close-but-wrong outputs may pass (e.g. sorting). Going below the cost of reading the output buys distance, not correctness. CHECKED-P (preprint).

## Misattribution traps
- **Little-oh "in Blum–Kannan":** explicit in Wasserman & Blum 1997 (credited to Blum 1988) and in BLR's "different"; accounts of BK's definition say polynomial time.
- **Schwartz–Zippel:** d/|S| is Schwartz's; DeMillo–Lipton were first but weaker; Zippel's is per-variable; Ore (1922) had a finite-field version (CHECKED-S).
- **Freivalds:** matrix checking is the 1977 IFIP paper; BLR cite his 1979 "Fast probabilistic algorithms" (LNCS 74).
- **BLR's 2/9:** general-group bounds (tight by Coppersmith's example); "rejection ≥ distance" and the knee 45/128 over GF(2) are BCHKS's.
- **Rado–Edmonds:** Schrijver gives Rado matroid ⇒ greedy and Gale/Edmonds the converse; a search summary of Jukna's textbook reverses this (unread); Gale is usually dropped.
- **de Bruijn criterion:** Barendregt's label, not de Bruijn's words (MEMORY).
- **Aumann:** common, not mutual, knowledge; no finiteness. Convergence by repeated exchange is Geanakoplos & Polemarchakis (*J. Econ. Theory* 28(1):192–200, 1982; CHECKED-S).
- **Knight & Leveson** is not "N-version fails": 2-out-of-3 systems averaged an order of magnitude better.
- **AMB's "false positives"** are, for detecting contextuality, misses.
- **Differential testing** has precursors: pseudo-oracles (Davis & Weyuker 1981; Weyuker 1982).
- **Ladha:** sources word his bound as average correlation or average covariance; check the original.
- **PCP:** O(1) counts proof bits; the verifier still reads all of x.
