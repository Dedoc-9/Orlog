# R1a: logic results behind ØRLǪG (citation check)

Checked 2026-10-25. **CHECKED**: a source read this session states it (in brackets). **MEMORY**: not confirmed this session. Statements are paraphrased. No design.

## 1. Fixed points of monotone maps

**Knaster–Tarski.** If (L, ≤) is a complete lattice and f: L → L is monotone, the fixed points of f form a non-empty complete lattice. Its least element is ⋀{x : f(x) ≤ x} and its greatest is ⋁{x : x ≤ f(x)}. *Source:* Tarski, Pacific J. Math. 5(2) (1955) 285–309, Thm 1. Tarski dates the power-set case to joint work in 1927, published as Knaster, Ann. Soc. Polon. Math. 6 (1928) 133–134 (existence only). Converse: A. C. Davis, Pacific J. Math. 5 (1955) 311–319. **CHECKED** [Tarski text].

**Kleene.** Let D have a least element ⊥ and suprema of ω-chains, and let f: D → D preserve them. Then sup{fⁿ(⊥)} is the least fixed point of f. *Source:* a folk theorem of unclear credit (Feferman, Logical Methods in CS 2(3), 2006, citing Lassez, Nguyen & Sonenberg, Inf. Proc. Lett. 14(3) (1982) 112–116, unread). It is named after the first recursion theorem in Kleene's *Introduction to Metamathematics* (1952). **CHECKED** [nLab; Feferman].

**Cousot & Cousot 1979.** For monotone F on a complete lattice, with no continuity assumed, the least fixed point is the limit of the transfinite iteration from ⊥. The fixed-point set is the image of L under preclosures built from such iterations. *Source:* Pacific J. Math. 82(1) (1979) 43–57. **CHECKED** [text].

**Chaotic/asynchronous iteration.** Take a system xᵢ = Fᵢ(x₁…xₙ) of monotone maps on a complete lattice. Start at ⊥ (or any D ≤ F(D)) and update components in any order, even from outdated values, provided none is abandoned forever. Every such run increases to the least fixed point above the start, whatever the schedule, stabilizing finitely if the lattice has finite height. *Precise source:* P. Cousot, "Asynchronous iterative methods for solving a fixed point system of monotone equations in a complete lattice", R.R. 88, Laboratoire IMAG, Grenoble, Sept. 1977. It assumes no continuity or chain condition. Theorem 2.2 of P. & R. Cousot, SIGPLAN Notices 12(8) (1977) 1–12, covers the continuous case, but Cousot's own page calls its proof erroneous. Origins: Chazan & Miranker, Linear Algebra Appl. 2 (1969) 199–222. Finite-chain version: Apt, Theor. Comp. Sci. 221 (1999) 179–210. **CHECKED** [R.R. 88 scan; Cousot page; Apt].

*Bearing (a):* checkers that share a monotone operator must agree whatever their order, so their agreement says nothing about the operator. Stage-wise iteration lets an outsider recompute the fixed point.

## 2. Self-reference in arithmetic

**Löb.** Let T be r.e. and contain enough arithmetic. Let its provability predicate Pr satisfy three conditions: T ⊢ A implies T ⊢ Pr⌜A⌝; Pr distributes over →; and T ⊢ Pr⌜A⌝ → Pr⌜Pr⌜A⌝⌝. Then T ⊢ Pr⌜A⌝ → A implies T ⊢ A. The internal form is □(□A → A) → □A. *Source:* Löb, J. Symbolic Logic 20(2) (1955) 115–118, answering Henkin, JSL 17 (1952) 160. Löb proves the rule form from five conditions on Hilbert–Bernays's arithmetic, and credits the general form to the referee. **CHECKED** [Löb text; SEP].

**Gödel II.** Let T be consistent, Σ₁-axiomatized and strong enough for those conditions. That takes about PRA; for Q, see Bezboruah & Shepherdson, JSL 41 (1976) 503–512. Then T does not prove ¬Pr_T⌜0=1⌝ for the canonical Pr_T. This is Löb's theorem with A = ⊥. *Source:* Gödel, Monatshefte Math. Phys. 38 (1931) 173–198. First full proof: Hilbert & Bernays, *Grundlagen der Mathematik II* (1939). It depends on the representation (Feferman, Fund. Math. 49 (1960) 35–92). **CHECKED** [SEP].

**Tarski.** If T is consistent and proves the diagonal lemma, no formula Tr(x) has T ⊢ Tr⌜A⌝ ↔ A for every sentence A. So arithmetical truth is not arithmetically definable. *Source:* Tarski, Warsaw 1933 (Polish); German: Studia Philosophica 1, 261–405, dated 1935, though Milne argues 1936. Gödel had it in 1930–31, unpublished (Murawski, Hist. Philos. Logic 19 (1998) 153–160). **CHECKED** [SEP; Milne and Murawski records]. Where it sits in the monograph: MEMORY.

*Bearing (b):* a theory certifies its own soundness only for claims it already proves. It can name its provability, which is Σ₁, but not its truth.

## 3. Self-trust between agents

**Löbian obstacle.** An agent that acts only on proofs in T could license a successor reasoning in T only if T ⊢ ∀φ(Pr_T⌜φ⌝ → φ), which Löb forbids. Trust passes from T+α to T+β only when β < α, so chains of successors are finite. Partial escapes: descending soundness schemas, and Fallenstein's "parametric polymorphism". *Source:* Yudkowsky & Herreshoff, MIRI early draft (June 2013; version of 7 Oct 2013), unrefereed. **CHECKED** [draft].

**Critch.** Let □ₖφ mean "φ has an S-proof of at most k characters". Let p(k) have one free variable, and let f be computable and eventually above E·O(lg k), where E is an encoding constant. If S ⊢ ∀k (□_{f(k)} p(k) → p(k)), then S ⊢ ∀k > k̂, p(k) for some k̂. Hence bounded FairBots cooperate. *Source:* J. Symbolic Logic 84(4) (2019) 1368–1381 (arXiv:1602.04184). **CHECKED** [arXiv Thm 3].

**Barasz et al. 2014.** FairBot cooperates iff PA proves its opponent cooperates. Against itself, PA ⊢ □[FB(FB)=C] → FB(FB)=C, so Löb gives PA ⊢ FB(FB)=C. It is unexploitable if PA is sound. *Source:* Barasz, Christiano, Fallenstein, Herreshoff, LaVictoire & Yudkowsky, arXiv:1401.5577 (2014). They credit self-cooperation first to V. Slepnev's unpublished draft. **CHECKED** [arXiv].

**Payor's lemma** exists. In any normal modal logic, if ⊢ □(□x → x) → x then ⊢ x. The proof uses necessitation and distribution alone, without a diagonal sentence. *Source:* a LessWrong/Alignment Forum post by A. Critch, 5 Feb 2023, crediting James Payor. I found no peer-reviewed version. **CHECKED** [post].

*Bearing (a)/(b):* when two copies of one prover "agree" to trust each other, they reach a Löbian fixed point, not independent confirmation. Certifying an equally strong successor is blocked, bounded or not.

## 4. Grounded truth

**Kripke 1975.** Give the truth predicate an extension and an anti-extension. The jump re-evaluates every sentence under strong Kleene. The jump is monotone, so iterating it from (∅, ∅), with unions at limits, reaches a least fixed point. A sentence is grounded if it has a value there, and paradoxical if it has a value in no fixed point. The liar is both; the truth-teller is ungrounded but not paradoxical. The intrinsic fixed points form a complete lattice with a largest member. *Source:* J. Philosophy 72(19) (1975) 690–716. Independently: Martin & Woodruff, Philosophia 5 (1975) 213–217 (maximal fixed points, weak Kleene). **CHECKED** [Kripke text].

**Revision theory.** A classical revision rule, built from the T-biconditionals, is iterated transfinitely. A sentence is categorically true if it is stably true in every revision sequence. Sources: Gupta; Herzberger; Belnap, J. Phil. Logic 11 (1982); Gupta & Belnap, MIT Press 1993. **CHECKED** [SEP].

*Bearing (a):* a claim that vouches for its own correctness has the truth-teller's shape, so it gets no value in the least fixed point.

## 5. Diagonal arguments

**Lawvere 1969.** In a cartesian closed category, call g: A → Y^A weakly point-surjective if for every f: A → Y some point x has g(x)(a) = f(a) for every point a. If such a g exists, every endomorphism of Y has a fixed point. Contrapositively, a fixed-point-free endomap rules g out; with Y = 2 this is Cantor's theorem. *Source:* Lecture Notes in Math. 92 (1969) 134–145; TAC Reprints 15 (2006). Lawvere derives Cantor, Russell, satisfaction, Tarski and Gödel I, and says Gödel II may need more. **Yanofsky** restates the theorem with sets and adds the liar, halting, Löb's paradox, the recursion theorem and Rice: Bull. Symbolic Logic 9(3) (2003) 362–386. **CHECKED** [TAC; arXiv].

*Bearing (b):* a system that represents all its own predicates cannot contain a negating self-check that has no fixed point.

## 6. Computability

**Rice 1953.** If P is a set of partial computable functions, neither empty nor all of them, then {e : φₑ ∈ P} is undecidable. P must depend only on the function computed. *Source:* Trans. AMS 74(2) (1953) 358–366. **CHECKED** [publisher PDF via search].

**Second recursion theorem.** For every partial computable f(e, y, x) there is a total computable z(y) with φ_{z(y)}(x) ≃ f(z(y), y, x). In particular, every total computable h has an e with φₑ = φ_{h(e)}. *Source:* Kleene, J. Symbolic Logic 3(4) (1938) 150–155, stated without a name at the end of §2 (Moschovakis, Bull. Symbolic Logic 16(2) (2010) 189–239). **CHECKED**.

*Bearing (a)/(b):* no total checker decides non-trivial program behaviour. Self-referential checkers always exist, sound or not.

## 7. Well-founded semantics

**Van Gelder, Ross & Schlipf 1991.** Take a ground normal program P and a partial interpretation I. A set U is unfounded if every rule with head in U has a body literal false in I or a positive body atom in U. A greatest unfounded set U_P(I) exists, and W_P(I) = T_P(I) ∪ ¬U_P(I) is monotone. Its least fixed point is the well-founded model (WFM). For p ← p, the set {p} is unfounded, so p is false. Fitting's Kripke–Kleene semantics (J. Logic Programming 2(4) (1985) 295–312) leaves p undefined. *Source:* J. ACM 38(3) (1991) 620–650 (Crossref: 619–649). **CHECKED** [Hitzler–Wendt, arXiv cs/0210027; Dung].

**Alternating fixpoint.** S_P(I), the least model of the reduct P^I, is antitone. The least fixed point L of S_P² gives the true atoms, and S_P(L) gives the atoms that are not false. *Source:* Van Gelder, J. Comput. System Sci. 47(1) (1993) 185–221. **CHECKED**.

**Total WFM ⇒ unique stable model.** Stable models (Gelfond & Lifschitz, ICLP/SLP 1988) agree with the WFM wherever it is defined, so a total WFM is the only stable model. The converse fails: {a ← not b; b ← not a; b ← not b} has one stable model, {b}, but its WFM leaves every atom undefined (worked here). General form: the well-founded fixpoint approximates every stable fixpoint (Denecker, Marek & Truszczyński, Information and Computation 192(1) (2004) 84–121). **CHECKED** for the general form; VRS 1991 attribution only secondary, theorem number not found.

*Bearing (a):* self-supporting loops are rejected, not left open. A claim may not certify itself.

## 8. Tightness

**Fages 1994.** Call a normal program "positive-order-consistent", now called "tight", if its positive dependencies have no infinite descending chain. Then its stable models are exactly the models of Clark's completion. *Source:* J. Methods of Logic in Computer Science 1 (1994) 51–60. **Erdem & Lifschitz 2003** allow nested expressions in bodies. If Π is tight on a consistent set of literals X, then X is an answer set iff X is closed under and supported by Π. *Source:* TPLP 3(4–5) (2003) 499–518. **CHECKED** [Erdem–Lifschitz].

*Bearing (a):* {p ← p} has the supported model {p}, which is not stable. A consistency-only checker accepts self-supporting claims.

## 9. Argumentation

**Dung 1995.** Let F(S) be the set of arguments whose attackers are all attacked by S. F is monotone, and the grounded extension is its least fixed point. It equals ⋃ₙFⁿ(∅) when every argument has finitely many attackers. If there is no infinite backward chain of attacks, there is exactly one complete extension, and it is grounded, preferred and stable. For logic programs, the well-founded model matches the grounded extension, and stable models match stable extensions. *Source:* Artificial Intelligence 77(2) (1995) 321–357 (Def. 20, Lemma 28, Thms 30, 49, 50). **CHECKED**.

*Bearing (a):* nothing is accepted unless already-accepted arguments defend it.

## 10. Closure operators

The fixed points of a closure operator on a complete lattice L form a complete lattice closed under all meets of L. Every meet-closed subset arises this way. The two composites of a Galois connection are closure operators whose closed sets are anti-isomorphic. *Sources:* Ward, Annals of Math. 43 (1942) 191–196; Ore, Trans. AMS 55 (1944) 493–513 (antitone "connexions"). **Formal concept analysis (FCA):** the concepts of a context form a complete lattice, and every complete lattice is the concept lattice of some context (the Basic Theorem). *Source:* Wille, in Rival (ed.), *Ordered Sets*, Reidel 1982, 445–470. **CHECKED** [nLab; Ward via secondary sources; Ignatov, arXiv:1703.02819].

*Bearing (a):* a fixed set of checks certifies only what its vocabulary can express.

## Obscure results

1. **Montague 1963.** Extend Q with a predicate N such that N⌜φ⌝ → φ for all φ, and close the theory under "from ⊢ φ infer ⊢ N⌜φ⌝". The result is inconsistent (Acta Philos. Fennica 16, 153–167; knower form: Kaplan & Montague, NDJFL 1 (1960) 79–90). A verifier that declares its verdicts factive while certifying its own theorems collapses. **CHECKED** [secondary].
2. **Artemov.** In general T does not prove Pr⌜φ⌝ → φ, yet T ⊢ Proof(p, ⌜φ⌝) → φ for each specific proof p. His Logic of Proofs realizes S4 (Bull. Symbolic Logic 7(1) (2001) 1–36). Self-trust works per certificate, never wholesale. **CHECKED** [Artemov's 2000 slides; SEP].
3. **Willard 2001.** Arithmetics with subtraction and division as primitives, which do not prove multiplication total, prove their own tableaux consistency (JSL 66(2), 536–596). Self-certification costs strength. **CHECKED** [abstract].
4. **Friedman 1979; Pudlák 1986.** A finitely axiomatized sequential T proves Con_T(n), "no contradiction has a proof of length ≤ n", in length polynomial in n. A strong enough NP-axiomatized T needs length at least n^ε (Logic Colloquium '84, 165–196; Handbook of Proof Theory ch. VIII). Bounded self-verification exists; its cost grows with the bound. **CHECKED** [Pudlák's chapter].
5. **Turing 1939; Feferman 1962.** Iterating reflection along notations in Kleene's O proves each true Π₁ sentence at some notation for ω+1 (Turing). With uniform reflection, it proves every true arithmetical sentence along notations of order type at most ω^ω^(ω+1) (Feferman). The results depend on the notation (Proc. LMS (2) 45 (1939) 161–228; JSL 27(3) (1962, issued 1963) 259–316). Stratified trust is complete only through notation choices nobody can verify. **CHECKED** [Pakhomov–Rathjen–Rossegger, arXiv:2405.09275].
6. **De Jongh–Sambin; Bernardi.** If p occurs in A(p) only under □, there is a p-free H with GL ⊢ H ↔ A(H), and H is computable and unique (Studia Logica 35 (1976) 345–361 and 335–343). With Solovay (Israel J. Math. 25 (1976) 287–304), self-referential provability claims become decidable. Modalized self-reference is eliminable, hence grounded. **CHECKED** [SEP]. De Jongh's own paper: MEMORY.

## Misattribution traps

- Knaster 1928 (sole author) proves only existence, for power sets. The fixed-point lattice is Tarski's; the converse is Davis's.
- "Kleene's theorem" is folklore. Plain monotone maps need transfinite iteration.
- Chaotic iteration is often cited to Cousot & Cousot 1979, which lacks it; the source is R.R. 88. Schedule-independence needs monotonicity and a start below the least fixed point.
- The three "HBL" conditions and the internal form are later distillations of Löb's five-condition rule form.
- "No system proves its own consistency" holds only for canonical Σ₁ representations. Feferman 1960, Rosser-style predicates and Willard all escape it.
- Tarski's theorem concerns truth, not provability. Gödel had it first, and the German edition likely appeared in 1936.
- "Second recursion theorem" is Rogers's 1967 name; Kleene said "the recursion theorem".
- Slepnev first showed FairBot's self-cooperation. FairBot need not halt; Critch's version does.
- Ungrounded is not paradoxical. Martin & Woodruff worked independently, and Kripke credits "grounded" to Herzberger (1970).
- Ore's connexions are antitone, and Ward (1942) is earlier. *Lattice Theory* (1940) is Garrett Birkhoff's, not G. D. Birkhoff's.
- Dates: Feferman 1962 was issued in 1963; Turing's thesis is 1938, printed 1939; Cousot 1979 is PJM vol. 82, not 81; JACM pages appear as 620–650 or 619–649.
