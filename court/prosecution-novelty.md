# Prosecution, novelty: the ØRLǪG OL-0 design record (2026-10-25)

**Under trial.** `DOCTRINE.md` §2 (what Ørlǫg does that its lineage did not) and §6 (Not new, Not found, and the five
items graded SPECULATIVE as pioneering), read against `src/orlog/court.py` for what the court computes. Court claim
ids from `court/claims.json` are given as **attacks:** lines (P1 to P5, NF, T1 to T4, T8), so the judge can write the
attack relation.

**What was read before searching.** DOCTRINE §§0 to 9; R1a, R1b, R2 and R3 in `research/`; `court.py`;
`prosecution-logic.md` (L1 to L20) to avoid duplicating it. Where R1a to R3 already hold a source, the finding says so,
and claims only what is new. Several defeaters were already in the record's own research and were not carried into §6
(N1, N11, N14): that is part of the case.

**How sources were read.** Every source graded [P] or [F] was opened this session; [S] and [U] are marked as such and
never carry a finding alone. Grades:
- **[P]**: the PDF was downloaded, its text extracted here with `pdftotext`, and the cited passage read directly.
- **[F]**: the page was fetched and read through the fetch tool, which returns quotations and summaries of the page.
- **[S]**: a search-result extract only.
- **[U]**: not read; cited by a source that was read. Never used alone as evidence.

Quotations are kept out of this file; every claim about a source is a paraphrase with a locator (proposition,
example, section, file line), so the defence can check it.

**Severity.** DEFEATS: the item, as worded, is not new. NARROWS: part of it exists; what remains is stated.
NO-PRIOR-ART-FOUND: searched and not found, with the queries listed in §Q (absence of evidence only).

## At a glance

| id | target | severity | one line |
|---|---|---|---|
| N1 | §6.1 (P1, T4) | DEFEATS | WELL-FOUNDED / CIRCULAR / UNSUPPORTED are exactly Fitting's Kripke–Kleene true / undefined / false for a Horn program (Fitting & Ben-Jacob 1988, Prop. 3.1) |
| N2 | §6.1 (P1) | DEFEATS | circular support as the region Kripke–Kleene leaves open and well-founded or stable semantics removes: positive loops, cyclic support, self-supported arguments (2001, 2013, 2024) |
| N3 | §6.1 (P1, T4) | DEFEATS | lfp = well-founded derivations or support, gfp = arbitrary ones: textbook (Leroy & Grall 2009; Keiren & Cleaveland 2023) |
| N4 | §6.1 (P1) | DEFEATS | "sandwich closed" is exactness of the Kripke–Kleene fixpoint, which brackets every fixpoint (Denecker, Marek & Truszczyński 2002) |
| N5 | §6.1 (P1) | NARROWS | a running belief system that refuses support that is only circular: Doyle's TMS, 1979 (formalized by Beck 2017) |
| N6 | §6.1, not-found 3 | NARROWS | circularity is a named safety-argument fallacy (2006); assurance arguments in Datalog (ETB 2014); three-valued assurance verdicts (2025); grounded claim standing (Lara 2026); lfp trust webs (Weeks 2001; Carbone et al. 2003) |
| N7 | §6.2 (P2, T1) | NARROWS | check every theorem, with no expressible way to trust the prover: LCF's abstract theorem type, contrasted with reflection principles and Löb (Harrison 1995) |
| N8 | §6.2 (P2) | NARROWS | "Artemov as language design" is Artemov's own programme: reflective λ-calculus (2001); Justification Logic as a certifying language's type system (Bonelli & Feller 2012) |
| N9 | §6.2 (P2) | NARROWS | a specific checked proof avoids the Löbian obstacle, an unspecified one does not, and the cost is seeing every proof (Yudkowsky & Herreshoff 2013, §5.1) |
| N10 | §6.3 (P3) | NARROWS | the external inputs a claim rests on are computed per theorem (Rocq, Lean with one axiom per native computation, ACL2 trust tags granted by the certifier, Dafny audit) |
| N11 | §6.3 (P3) | NARROWS | an oracle whose expectation flows from the judged code cannot fail; anchoring is a decidable provenance property (Canedo, Aug 2026; already in R3) |
| N12 | §6.3 (P3) | NARROWS | claims that only an outside principal can support (a signature), typed by source and logged at run time (Aura, ICFP 2008) |
| N13 | §6 combination, P3, NF | NARROWS | Lara (Sep 2026): claims language, evidence typed by kind and provenance, grounded standing, untrusted prose binding, byte-identical Haskell and Lean reports |
| N14 | §6.4 (P4, T3) | NARROWS | the ratio of cost with checks to cost without, in counted resolution steps, declared and verified (Klemen et al. 2018, static; R3 had the abstract) |
| N15 | §6.4 (P4) | NARROWS | run-time overhead budgets for checks, as a share of the computation (QVM, OOPSLA 2008; by cycle counter) |
| N16 | §6.4 (P4) | NARROWS | deterministic resource counters bounding checkers (Z3 rlimit in F* and Dafny) |
| N17 | not-found 1 (NF), §6.5, §2 | NARROWS | one expected output per program across every backend, with per-backend override files and declared unsupported features (Dafny's test harness) |
| N18 | not-found 1 (NF), §6.5 | NARROWS | a declared reference semantics with listed deviations (Scala.js); byte-identical reports from two implementations (Lara) |
| N19 | §6.5 (P5, T8) | NARROWS | one meaning, several spellings: ALGOL 60's three representations (1960); Catala's language-dependent keywords |
| N20 | §6.5 (P5, T8), not-found 5 | NARROWS | meaning-level hashes unchanged by reformatting or renaming, written in source (Dhall 2017; Unison) |
| N21 | not-found 5 | NARROWS | numbers as words in source (Hoon @q), hashes as words (S/KEY 1995; US 10,467,392): only the conjunction is unfound |
| N22 | not-found 2 | NO-PRIOR-ART-FOUND | a general-purpose language runtime grading its own run-time claims by channel (nearest: Lara, Lean) |
| N23 | not-found 3 | NO-PRIOR-ART-FOUND | an assurance tool reporting gfp ∖ lfp of support as circularity (the report itself is N1) |
| N24 | not-found 4 | NO-PRIOR-ART-FOUND | run-time deterministic counting that grades a certificate against the clause it certifies (nearest: N14, N15) |
| N25 | §2 | NARROWS | each of §2's six "lineage did not" items has prior art outside the lineage |

---

## N1. The court's three standings are Fitting's Kripke–Kleene values — DEFEATS

**Target.** §6 item 1 ("self-certification reported as gfp ∖ lfp of the support operator, with the sandwich closed
certificate"), §T4's mechanism. **attacks:** P1, T4.

**Sources.**
- M. Fitting and M. Ben-Jacob, *Stratified and Three-valued Logic Programming Semantics*, Proc. 5th Int. Conf. and
  Symp. on Logic Programming, MIT Press, 1988, pp. 1054–1068 (bibliography [S]); author's copy read [P]:
  https://id144254.securedata.net/melvinfitting/bookspapers/pdf/papers/Stratified.pdf . Expanded as *Stratified, Weak
  Stratified, and Three-valued Semantics*, Fundamenta Informaticae 13(1):19–33, 1990 [S].
- M. Fitting, *A Kripke–Kleene semantics for logic programs*, J. Logic Programming 2(4):295–312, 1985 [U; cited by the
  above and by R1a §7].

**Finding.** `court.py` defines G(X) = {c : base(c) and premises(c) ⊆ X}. That is the immediate-consequence operator
T_P of the Horn program P = {c ← premises(c) : base(c)}. Fitting and Ben-Jacob, Proposition 3.1: for a Horn program,
an atom is true in Fitting's least three-valued fixed point exactly when it is in lfp(T_P), and false there exactly when
it is outside gfp(T_P). So, claim by claim:

| court.py standing | set | Kripke–Kleene value (Fitting) |
|---|---|---|
| WELL-FOUNDED | lfp(G) | true |
| CIRCULAR | gfp(G) ∖ lfp(G) | undefined |
| UNSUPPORTED | outside gfp(G) | false |
| `sandwich_closed` | lfp(G) = gfp(G) | the Kripke–Kleene model is two-valued |

The paper's abstract and §1 make the point in general: the classical fixed-point semantics of Horn programs gives both
the least and the greatest fixed point a role (success set and ground failure set, crediting Apt & van Emden 1982 and
Jaffar, Lassez & Maher 1986), and reading them together leaves some atoms without a value, so a three-valued logic
emerges. The well-founded model of a Horn program is its least model, so CIRCULAR is precisely where Kripke–Kleene says
undefined and the well-founded semantics says false. R1a §7 already records that difference on p ← p; §6 did not use
it.

**How much it defeats.** All of the formal content of item 1: the report (the undefined set), the three-way split and
the closure condition. What survives is an application: feeding this operator with a program's own run-time claims
(base(c) = held in every backend; premises declared by the author), calling the undefined set self-certification, and
printing a cycle witness.

**Corrected wording.** Move to *Not new*: "the court's three standings for a Horn support operator (lfp, gfp ∖ lfp,
outside gfp) are the true, undefined and false values of Fitting's Kripke–Kleene semantics (Fitting 1985; Fitting &
Ben-Jacob 1988, Prop. 3.1)". Keep as speculative only: "applying the Kripke–Kleene / well-founded distinction to a
program's own run-time claims, reported as self-certification".

## N2. Circular support is the Kripke–Kleene / well-founded difference, named and removed since 2001 — DEFEATS

**Target.** §6 item 1, as a *detector* of claims "supported only by their own cycle". **attacks:** P1.

**Sources.**
- S. Brass, J. Dix, B. Freitag, U. Zukowski, *Transformation-Based Bottom-Up Computation of the Well-Founded Model*,
  TPLP 1(5):497–538, 2001; arXiv cs/0011013 [P]: https://arxiv.org/abs/cs/0011013 .
- G. Brewka, S. Ellmauthaler, H. Strass, J. P. Wallner, S. Woltran, *Abstract Dialectical Frameworks Revisited*, IJCAI
  2013 [P]: https://www.ijcai.org/Proceedings/13/Papers/125.pdf .
- G. Alfano, S. Greco, F. Parisi, I. Trubitsyna, *Cyclic Supports in Recursive Bipolar Argumentation Frameworks:
  Semantics and LP Mapping*, TPLP (2024); arXiv 2408.08916 [F]: https://arxiv.org/abs/2408.08916 .
- Van Gelder, Ross & Schlipf, J. ACM 38(3), 1991 [U here; read through Brass et al., and recorded in R1a §7].

**Finding.**
- Brass et al. (Theorem 15, the remark after it, Example 16, Definition 17, Lemma 18): Fitting's operator already
  computes the well-founded model for programs without positive loops; positive loops must be found and removed by a
  separate loop-detection step. That step removes the greatest unfounded set, which is the base minus the least fixed
  point of the positive part. Their Example 16 (q ← r, r ← q, beside facts) is a two-claim Plankton: Fitting's rules
  cannot delete the loop, and loop detection does.
- Brewka et al. (§3, Definition 6, Examples 1 and 2): stable models must give every accepted statement a non-cyclic
  justification; the grounded semantics leaves the cyclically supported statements undefined. Example 2 is three
  statements whose only two-valued model makes all of them true through mutual support, which the paper calls
  unintended cyclic support and refuses as stable: Plankton's shape, in 2013.
- Alfano et al.: their acceptability explicitly excludes self-supported arguments, those in a support cycle or supported
  by one; the single loop a ← a maps to a program whose unique minimal model is empty; grounded corresponds to the
  well-founded model.

**How much it defeats.** The detector, as a concept: the set of claims supported only through support cycles is the
standard object that well-founded, stable and argumentation semantics exist to remove, and that Kripke–Kleene leaves
undefined. Nothing in item 1's mechanism survives; the cycle witness is ordinary loop detection.

**Corrected wording.** Add to *Not new*: "claims supported only by positive loops are the unfounded atoms of the
well-founded semantics (Van Gelder, Ross & Schlipf 1991; Brass et al. 2001), the cyclic support that stable semantics of
argumentation frameworks rejects (Brewka et al. 2013), and the self-supported arguments of bipolar frameworks (Alfano et
al. 2024)".

## N3. "gfp ∖ lfp is support only by each other" is a textbook characterization — DEFEATS

**Target.** §T4's statement and §6 item 1's mathematics. **attacks:** P1, T4.

**Sources.**
- X. Leroy and H. Grall, *Coinductive big-step operational semantics*, Information and Computation 207(2):284–304,
  2009 [P]: https://xavierleroy.org/publi/coindsem-journal.pdf (§2.1 and §2.2).
- J. J. A. Keiren and R. Cleaveland, *Extensible Proof Systems for Infinite-State Systems*, ACM TOCL, 2023; arXiv
  2207.12953 [P]: https://arxiv.org/abs/2207.12953 (§3, Definition 18).

**Finding.** Leroy and Grall define the inference operator of a rule system (the set of judgments inferable in one step
from a set), and state that its least fixed point is the inductive interpretation, the conclusions of well-founded
derivations, while its greatest fixed point is the coinductive interpretation, the conclusions of arbitrary, possibly
ill-founded derivations. Keiren and Cleaveland give the same in the language of *support*: an element is in the least
fixed point of a monotone set operator exactly when some well-founded support ordering contains it, and in the greatest
exactly when some support ordering, not necessarily well-founded, does. With finitely many claims, an ill-founded
support is a cycle (or depends on one). So "WELL-FOUNDED = lfp" and "CIRCULAR = gfp ∖ lfp" restate this.

**How much it defeats.** Any novelty in the identification itself. (Prosecution-logic L9 separately finds "its own
cycle" too strong: a claim can depend on a cycle without lying on one; Leroy and Grall's "ill-founded derivation"
wording is the correct one.)

**Corrected wording.** In §T4's *theorems*, add: "the least fixed point of a rule operator is the set of conclusions
with well-founded derivations, the greatest those with arbitrary ones (Leroy & Grall 2009; in terms of support
orderings, Keiren & Cleaveland 2023)".

## N4. "Sandwich closed" is exactness in approximation fixpoint theory — DEFEATS

**Target.** §6 item 1's "sandwich closed" certificate. **attacks:** P1, T4.

**Source.** M. Denecker, V. W. Marek, M. Truszczyński, *Ultimate approximations in nonmonotonic knowledge
representation systems*, KR 2002; arXiv cs/0205014 [F]: https://arxiv.org/abs/cs/0205014 (§2, §3). R1a §7 cites the
2004 journal version for the stable-fixpoint form.

**Finding.** Approximation fixpoint theory works with pairs (x, y), read as a lower and an upper bound on every element
between them; pairs (x, x) are called exact. The paper states that the Kripke–Kleene fixpoint approximates all
fixpoints of the operator, and the well-founded fixpoint all its stable fixpoints. For a monotone G iterated from the
least precise pair (trust nothing, trust everything), the Kripke–Kleene fixpoint is (lfp G, gfp G) (by N1's Prop. 3.1;
my derivation for the general monotone case). When it is exact, every fixpoint equals it: that is the record's
"every self-consistent assignment of trust between trust nothing and trust everything gives the same standing".

**How much it defeats.** The certificate as a concept. The record's own remark that "the theorem used is only
Knaster–Tarski" is correct, and is the reason this is a corollary, not a contribution. (Prosecution-logic L10 shows the
flag is also issued vacuously on an empty lfp; in AFT terms, exact is not informative.)

**Corrected wording.** "When lfp = gfp the Kripke–Kleene fixpoint is exact, so the support operator has one fixed point
(Knaster–Tarski; approximation fixpoint theory, Denecker, Marek & Truszczyński 2002). Reported only when lfp is
non-empty."

## N5. A running reasoning system that refuses circular support: Doyle's TMS — NARROWS

**Target.** §6 item 1, as a self-certification guard inside a running system. **attacks:** P1.

**Sources.**
- H. Beck, *Reviewing Justification-based Truth Maintenance Systems from a Logic Programming Perspective*, INFSYS RR
  17-02, TU Wien, July 2017 [P]: https://haendel.kr.tuwien.ac.at/tr-reports/files/rr1702.pdf (§1, §2, Theorem 1,
  Example 4).
- J. Doyle, *A Truth Maintenance System*, Artificial Intelligence 12(3), 1979 [U; through Beck]. Elkan 1990 [U; through
  Beck].

**Finding.** Beck credits Doyle's JTMS with maintaining consistent beliefs and their well-foundedness. A model must be
*founded*: its believed nodes admit an order in which each has a valid justification resting only on earlier nodes,
which excludes support that is only circular. Elkan's theorem (Beck's Theorem 1) identifies admissible models with
answer sets. Beck's Example 4 has the loop d ← c, c ← d; once c's outside justification is defeated, the loop alone
keeps neither node in.

**How much it narrows.** A belief system that runs, updates incrementally, and will not believe a claim whose only
support is its own cycle, dates from 1977–79. What remains: the JTMS labels such nodes OUT; it does not report them as a
separate class beside the unsupported ones. That separate report is N1's undefined set.

**Corrected wording.** Add to *Not new*: "refusing beliefs whose only justifications are circular (Doyle's truth
maintenance system, 1979)".

## N6. Assurance and trust: circularity known, least-fixed-point verdicts used, the gap report absent — NARROWS

**Target.** §6 not-found item 3 ("assurance verdicts under grounded or well-founded semantics that report circular
support as the lfp/gfp gap") and item 1's application. **attacks:** P1.

**Sources.**
- W. S. Greenwell, J. C. Knight, C. M. Holloway, J. J. Pease, *A Taxonomy of Fallacies in System Safety Arguments*,
  24th International System Safety Conference, 2006 [P]: https://ntrs.nasa.gov/citations/20060027794 (Table 6 and the
  category list after it).
- S. Cruanes, S. Heymans, I. Mason, S. Owre, N. Shankar, *The Semantics of Datalog for the Evidential Tool Bus*, LNCS
  8373, 2014, pp. 256–275 [F, abstract]:
  https://www.sri.com/publication/information-computer-science-pubs/the-semantics-of-datalog-for-the-evidential-tool-bus/ .
- A. Hafver, D. McGeorge, E. Stensrud, F. B. Pedersen, T. Skramstad, R. Flage, *Propagating Knowledge Strength Through
  Assurance Arguments using Three-Valued Logic to Assess Confidence in Claims*, ESREL SRA-E 2025 [F]:
  https://rpsonline.com.sg/proceedings/esrel-sra-e2025/html/ESREL-SRA-E2025-P0625.html .
- Y. He and J. Liu, *Beyond Natural Language: An Agent-Native Language for Autonomous Science*, arXiv 2609.25421, 21
  Sep 2026 [F] (see N13).
- M. Carbone, M. Nielsen, V. Sassone, *A Formal Model for Trust in Dynamic Networks*, BRICS RS-03-4, January 2003
  (SEFM 2003) [P]: https://www.brics.dk/RS/03/4/BRICS-RS-03-4.pdf ; S. Weeks, *Understanding trust management
  systems*, IEEE S&P 2001 [U; through Carbone et al.].
- Already in R3 F1: CLARISSA (s(CASP)), Bloomfield, Netkachova & Rushby, Assurance 2.0, eliminative argumentation.

**Finding.**
- Greenwell et al. put circular reasoning (an argument that reasserts its claim as a premise, or defines a term so the
  claim is trivially true) first in their safety-argument fallacy taxonomy, to be checked by reviewers.
- The Evidential Tool Bus represents assurance arguments and workflows in Datalog, that is, Horn clauses, whose standard
  semantics is the least model: assurance claims are already established under least-fixed-point semantics.
- Hafver et al. propagate three verdicts (true, false, uncertain) through assurance arguments.
- Lara assigns research claims justified, defeated, contested or gap under Dung's grounded semantics; unresolved attack
  cycles leave claims contested.
- In trust management, global trust is the least fixed point of mutually recursive (possibly circular) policies (Weeks
  2001, per Carbone et al.), and Carbone et al. compute it in an information order whose bottom is "no knowledge", over
  trust intervals, so that missing information is not read as distrust. Over a two-element trust lattice those intervals
  are Kleene's three values (my observation, not stated in the paper).

**How much it narrows.** Not-found item 3 shrinks to its last clause. Assurance verdicts under least-fixed-point and
grounded semantics exist (ETB; Lara), three-valued assurance verdicts exist, and circularity is a recognized assurance
fallacy. What remains unfound is a tool that *reports* gfp ∖ lfp of a support relation as circular support (N23).

**Corrected wording.** Not-found item 3 becomes: "an assurance tool that reports the Kripke–Kleene-undefined
(gfp ∖ lfp) claims of a support relation as circular support (least-fixed-point and grounded assurance verdicts exist:
ETB 2014, Lara 2026; circularity is a known safety-argument fallacy: Greenwell et al. 2006)".

## N7. LCF made "check every theorem, never trust the prover" a programming-language rule — NARROWS

**Target.** §6 item 2 ("explicit per-certificate reflection is expressible; wholesale reflection is not ... a syntactic
answer to Löb's obstacle at the level of a programming language"), §T1. **attacks:** P2, T1.

**Source.** J. Harrison, *Metatheory and Reflection in Theorem Proving: A Survey and Critique*, Technical Report
CRC-053, SRI International Cambridge Computer Science Research Centre, dated 15 February 1995 [P]:
https://www.cl.cam.ac.uk/~jrh13/papers/reflect.pdf (§1; the section on reflection principles). Edinburgh LCF (Gordon,
Milner & Wadsworth 1979) [U; through Harrison].

**Finding.** Harrison's §1: in LCF provers, theorems are an ML abstract datatype whose only constructors are the
primitive inference rules, so anything of type `thm` arose by primitive inference; derived rules and tactics are
ordinary, untrusted programs, and users can have equal confidence in their results because those results must still
decompose into primitives. There is no way, in the language, to make a theorem from "the prover says so". His later
section sets out the alternative, reflection principles (local reflection: if φ is provable then φ), and Löb's theorem
that such an instance is provable only when φ already is; the survey weighs LCF's fully expansive checking against
reflection.

**How much it narrows.** "Per-certificate checking expressible, wholesale trust in the checker inexpressible", enforced
by the type system of a programming language, is the LCF architecture of the 1970s, and its relation to reflection
principles and Löb is laid out in 1995. The record's §1 already cites "Urðr's LCF discipline" as lineage; §6 should not
then call the same discipline pioneering. What remains: carrying the discipline from theorems in a logic to the run-time
claims of a general-purpose language. (Prosecution-logic L3 argues independently that Ørlǫg has no provability
predicate, so "an answer to Löb" is outside Löb's hypotheses.)

**Corrected wording.** Item 2 becomes: "LCF's discipline (Milner; see Harrison 1995) carried to run-time claims: a claim
may cite a checked certificate, and no construct can express trust in the checker. Not an answer to Löb's theorem."

## N8. Artemov's Logic of Proofs as language design is Artemov's own programme, and was built — NARROWS

**Target.** §6 item 2's title, "Artemov as language design". **attacks:** P2.

**Sources.**
- S. Artemov, *Research Statement* [F]: https://sartemov.ws.gc.cuny.edu/research-statement/ .
- J. Alt and S. Artemov, *Reflective λ-calculus*, Proof Theory in Computer Science (PTCS 2001), LNCS 2183, pp. 22–37
  [S]; S. Artemov and E. Bonelli, *The intensional lambda calculus*, LFCS 2007 [S].
- E. Bonelli and F. Feller, *Justification Logic as a foundation for certifying mobile computation*, Annals of Pure and
  Applied Logic 163(7):935–950, 2012, doi:10.1016/j.apal.2011.09.007 [F, abstract]:
  https://researchwith.stevens.edu/en/publications/justification-logic-as-a-foundation-for-certifying-mobile-computa/ .

**Finding.** Artemov's statement says explicit reflection is provable inside the system and so avoids the tower of ever
stronger theories that Gödel-style reflection needs; that formal verification with the implicit rule is impossible; that
the work bears on the appropriate syntax and semantics of typed programming languages; and that a reflective
λ-calculus matching proof polynomials was built (confluent, strongly normalizing) for its core. Bonelli and Feller use an
intuitionistic fragment of Justification Logic as the type system of a programming language whose mobile units carry
both code and a certificate, typing certificate construction alongside code, with type safety and strong normalization.

**How much it narrows.** "Artemov as language design" names a research line of 2000–2012, with implemented calculi. What
remains is a different thing: Ørlǫg's certificates are Boolean checks evaluated at run time, not proof terms, so (with
L3) the item borrows Artemov's name without his mechanism.

**Corrected wording.** Drop "Artemov as language design" as a pioneering title; cite Artemov (2001), Alt & Artemov
(2001) and Bonelli & Feller (2012) under *Not new* as "the Logic of Proofs as the basis of programming calculi with
explicit, per-proof reflection".

## N9. "A specific proof escapes Löb, an unspecified one does not" is stated, with its price, in 2013 — NARROWS

**Target.** §6 item 2, "a syntactic answer to Löb's obstacle". **attacks:** P2, T1.

**Source.** E. Yudkowsky and M. Herreshoff, *Tiling Agents for Self-Modifying AI, and the Löbian Obstacle*, MIRI early
draft, 7 October 2013 [P]: https://intelligence.org/files/TilingAgentsDraft.pdf (§5.1, footnote 31). R1a §3 cites this
draft for the obstacle only.

**Finding.** §5.1: if the parent agent knew in advance the particular proof its successor would produce, it could check
that proof itself (given axioms at least as strong), and the Löbian obstacle would not arise at all. Footnote 31: the
forbidden schema stops a theory from concluding φ from the bare existence of some unspecified proof; a theory shown an
actual proof of φ may of course conclude φ. The authors then reject this route for their purpose, because it requires the
parent to foresee each specific proof (their Vingean principle), which a verifier weaker than the producer cannot do.

**How much it narrows.** The design response "trust specific checked certificates, never the checker wholesale" to the
Löbian obstacle is explicit in the 2013 literature the record already cites, together with its cost: the verifier must
see, and be able to check, every certificate. What remains is only the claim that a programming language makes that the
sole syntactic form, which is N7.

**Corrected wording.** In §T1: "Per-certificate trust avoids the Löbian obstacle at the price of checking each
certificate (Yudkowsky & Herreshoff 2013, §5.1); Ørlǫg pays that price on every claim."

## N10. The external inputs a claim rests on are computed per theorem in four mainstream systems — NARROWS

**Target.** §6 item 3 ("'zero external bits' is a computed property of a claim"). **attacks:** P3, T2.

**Sources.**
- Lean Language Reference, *Axioms* [F]: https://lean-lang.org/doc/reference/latest/Axioms/ .
- Rocq reference manual, *Print Assumptions* [F]:
  https://rocq-prover.org/doc/master/refman/proof-engine/vernacular-commands.html .
- ACL2 documentation, DEFTTAG (version 3.1 mirror) [F]:
  https://planet.racket-lang.org/package-source/cce/dracula.plt/2/7/docs/DEFTTAG.html .
- The Dafny maintainers, *Dafny 4 is released*, 3 March 2023 [F]: https://dafny.org/blog/2023/03/03/dafny-4-released/ .
- Already in R2: HOL4 oracle tags, Isabelle's oracle mark, Lean's `#print axioms` (from an extract).

**Finding.**
- Lean tracks automatically which axioms each proof depends on; `#print axioms` lists them, for example exposing a
  transitive `sorry`. Proofs by native evaluation get a dedicated axiom for each computation the compiled code asserts,
  so dependence on the whole compiler, not only the kernel, is recorded per computation.
- Rocq's `Print Assumptions` lists the axioms, parameters and variables a theorem depends on, and reports that it is
  closed under the global context when there are none.
- ACL2's trust tags mark potentially unsafe acts; `certify-book` admits a tag only if the certifier passes it in
  `:ttags`, outside the book, and admits none otherwise; a certifier checks that no `:ttags` were supplied or reads every
  TTAG NOTE.
- `dafny audit` reports the explicit and implicit assumptions a program's proofs depend on.

**How much it narrows.** Computing, per claim, the set of external inputs it rests on, and requiring the grant of
external trust to come from outside the text (ACL2), are standard. The valuation is opposite to Ørlǫg's: these systems
treat zero external assumptions as the best case, Ørlǫg treats zero external bits as unable to ground. That inversion
(N11) is what remains.

**Corrected wording.** Extend *Not new*'s "oracle-tagged theorems: HOL4" to: "per-theorem assumption tracking (HOL4
tags, Isabelle oracles, Rocq Print Assumptions, Lean `#print axioms` with one axiom per natively evaluated computation,
ACL2 trust tags granted at certification, `dafny audit`)".

## N11. "Zero external bits cannot ground" is published for test oracles, as decidable provenance — NARROWS

**Target.** §6 item 3. **attacks:** P3, T2.

**Sources.**
- A. Canedo, *Oracles That Cannot Fail: Anchoring and the Expectation That Moves With the Fault*, arXiv 2608.17214, 17
  August 2026 [F, full text]: https://arxiv.org/abs/2608.17214 (abstract, §1, §2, §11).
- C. Huo and J. Clause, *Improving oracle quality by detecting brittle assertions and unused inputs in tests*, FSE 2014,
  doi:10.1145/2635868.2635917 [S, abstract].
- Already in R3 F2 (Canedo, OraclePolish, the test-smell catalogue). §6 did not carry it.

**Finding.** Canedo: an oracle that takes its expected value from the system it judges cannot fail, because a fault moves
the measurement and the expectation together. He calls an expectation specification-anchored when it is built from
values fixed outside the code under mutation, and state-anchored when it flows from that code; he calls anchoring a
provenance property, binary and decidable without running anything (the reaching half on the import-and-call graph),
reports that a sweep of linters found no implementation, and measures the effect on an air-traffic-control simulator.
Huo and Clause had already used dynamic taint tracking on oracles (2014), in the opposite direction (assertions that
depend on uncontrolled inputs).

**How much it narrows.** The DPI reading of a check, that a check carrying no bits from outside the judged artefact adds
nothing, is published as a computable provenance property of oracles two months before this record. What remains: making
it a typed channel of every claim in a language, enforced by the runtime court; Canedo recommends review, not refusal.

**Corrected wording.** Item 3 becomes: "Canedo's anchoring (2026), as a typing rule: a claim checked only by the
author's own computation is state-anchored, carries zero external bits, and can never be GROUNDED; grounding needs a
ledger line outside the program text."

## N12. Claims only an outside authority can support, typed by source and logged at run time: Aura — NARROWS

**Target.** §6 item 3, "ratification comes from outside the program text". **attacks:** P3, T2.

**Sources.**
- L. Jia, J. A. Vaughan, K. Mazurak, J. Zhao, L. Zarko, J. Schorr, S. Zdancewic, *AURA: A programming language for
  authorization and audit*, ICFP 2008 [F, abstract]: https://www.icfpconference.org/icfp2008/accepted/80.html .
- S. Zdancewic, *AURA: A language with authorization and audit*, IFIP WG 2.8 talk, 2008 [P]:
  https://www.cs.ox.ac.uk/ralf.hinze/WG2.8/25/slides/steve.pdf .

**Finding.** Aura joins ordinary programming with an authorization logic (principals, "A says P") through dependent
types. Its atomic assertion constants carry no proof evidence, so authorization proofs cannot be forged inside a
program; evidence that A says T is A's digital signature on T, which only the holder of A's key can make; proofs are
first-class values, and the runtime logs them for audit.

**How much it narrows.** A typed language in which certain claims can be supported only by an authority outside the
program text, keyed by their source, with a run-time evidence log, exists since 2008, and its outside evidence is
authenticated, which Ørlǫg's ledger is not (§8). What remains: using it for truth claims and theorem ratification rather
than authorization.

**Corrected wording.** Add to *Not new*: "claims whose only evidence is an outside principal's signature, logged at run
time (Aura, 2008; authenticated, unlike Ørlǫg's ledger)".

## N13. Lara (September 2026) is the closest prior combination — NARROWS

**Target.** §6's "what I think is pioneering: the combination as one language"; item 3; not-found items 1 and 2; item
1's application. **attacks:** P1, P3, P5, NF.

**Source.** Y. He and J. Liu, *Beyond Natural Language: An Agent-Native Language for Autonomous Science*, arXiv
2609.25421, 21 September 2026 [F, abstract and full HTML in three parts]: https://arxiv.org/abs/2609.25421 .

**Finding.** Lara is a machine-checkable language and protocol for research claims:
- authors declare claims, evidence, assumptions and objections; each evidence leaf has a kind (observed, attested,
  assumed or certified) and a provenance, and admission is decided on the pair (admit, quarantine or reject; a
  quarantined premise leaves its claim a gap);
- a deterministic checker evaluates the arguments under Dung's grounded semantics and gives each claim one of justified,
  defeated, contested or gap;
- support is identity of normalized formal targets, not entailment, so no solver is trusted; the binding of prose to
  formal atoms is untrusted by design, and an auditor must confirm that the atom says what the prose says;
- a Haskell and a Lean implementation are held to byte-identical reports and exit codes, which the authors state does
  not prove the implementations equivalent; replay bundles are pinned by digest; the metatheory is in Lean 4, and some
  examples trust native evaluation; the related work cites the Logic of Proofs and proof-carrying code.

**How much it narrows.** One month before this record, a claims language already grades standing by evidence channel and
provenance under grounded semantics, keeps prose outside the trusted base, and holds two implementations to
byte-identical output. Not in Lara: claims about the program's own computation, evaluated at run time; floats; counted
cost; support cycles as gfp ∖ lfp; three compiled host languages; a ledger outside the text.

**Corrected wording.** Add to *Not new*: "a claims language with evidence typed by kind and provenance, grounded
standing (justified, defeated, contested, gap), an untrusted prose binding, and byte-identical reports from two
implementations (Lara, 2026)". The combination claim should name Lara as its nearest neighbour and state the
differences above.

## N14. Counted-step bounds on check cost relative to program cost, declared and verified (2018) — NARROWS

**Target.** §6 item 4 ("counted cost asymmetry ... enforces Blum's 'different' by measurement"), not-found item 4, §T3.
**attacks:** P4, T3.

**Source.** M. Klemen, N. Stulova, P. López-García, J. F. Morales, M. V. Hermenegildo, *An Approach to Static
Performance Guarantees for Programs with Run-time Checks*, ICLP 2018 technical communication; arXiv 1804.02380 [P]:
https://arxiv.org/abs/1804.02380 (§4.2, §4.3, §5). R3 F3 cited it from the abstract; §6 did not carry it.

**Finding.** Klemen et al. extend the Ciao assertion language so a programmer can state an admissible run-time-checking
overhead, including a bound on the ratio between a predicate's cost with its run-time checks and its cost without them
(the `rtc_ratio` qualifier), for example "at most linear", for one predicate or for all. The cost is counted in
resolution steps (each clause body costs one), a deterministic operation count, and the bound is checked statically by
cost analysis over all inputs; the experiments report the inferred ratios and the verdicts.

**How much it narrows.** Using deterministic operation counts to enforce that checking costs no more than a declared
function of the checked computation's cost is published, statically and for all inputs. What remains: run-time,
per-input measurement (one input, as §T3 admits), applied to a certificate against the clause it certifies, and used to
grade epistemic standing (CERTIFIED or RECOMPUTATION) rather than performance admissibility. (Prosecution-logic L6 and
L8 find the guard itself misfires.)

**Corrected wording.** Add to *Not new*'s "checks cheaper than computation": "a declared bound on the ratio of cost with
checks to cost without, in counted resolution steps, verified statically (Klemen et al. 2018)". Not-found item 4
becomes: "run-time, per-input operation counting used to grade a certificate against the clause it certifies".

## N15. Run-time enforcement of a check-to-computation budget (2008, by time) — NARROWS

**Target.** §6 item 4, not-found item 4. **attacks:** P4.

**Source.** M. Arnold, M. Vechev, E. Yahav, *QVM: An Efficient Runtime for Detecting Defects in Deployed Systems*,
OOPSLA 2008 [P]: https://csaws.cs.technion.ac.il/~yahave/papers/oopsla08.pdf (§1, §4, §4.1).

**Finding.** QVM's overhead manager lets the user set the overhead that checks may impose (the paper suggests 5–10% in
production and up to 100% in testing), measures the time spent in checks with the processor's cycle counter, and
adjusts per-site sampling so that the checks stay within that share of the program's execution.

**How much it narrows.** Enforcing at run time that checks cost no more than a stated fraction of the computation exists,
measured by time and enforced by dropping checks. What remains: deterministic counts instead of time, and a verdict on the
claim instead of a sampling rate.

**Corrected wording.** Add to *Not new*: "run-time overhead budgets for checks (QVM, 2008; by time, enforced by
sampling)".

## N16. Deterministic counters bounding checkers are standard in verifiers — NARROWS

**Target.** §6 item 4's "deterministic operation counting". **attacks:** P4.

**Sources.** F* wiki, *rlimits: Machine Independent Resource Limits for Deterministic Execution* [F]:
https://github.com/FStarLang/FStar/wiki/rlimits:-Machine-Independent-Resource-Limits-for-Deterministic-Execution ;
Dafny's resource units [S].

**Finding.** F* replaced wall-clock time-outs, which varied with machine speed, by Z3 resource limits, which make
execution deterministic regardless of machine or load and track time well but not perfectly; Dafny exposes the same
counter. This is in addition to Wasmtime fuel and Ethereum gas, already in §6.

**How much it narrows.** Deterministic counting to bound a checker's work is established; the bound there is absolute,
not relative to the checked computation. Small narrowing; it supports N14.

**Corrected wording.** Extend "operation meters (Wasmtime fuel, Ethereum gas)" with "and deterministic solver resource
limits (Z3 rlimit, as used by F* and Dafny)".

## N17. Dafny already holds every backend to one expected output per program, with declared exceptions — NARROWS

**Target.** Not-found item 1 ("a stated contract of byte-identical output across Python, C99 and Rust, with a declared
authority and localized mismatch notes"), §6 item 5, §2's first bullet. **attacks:** NF, P5.

**Source.** Dafny source, `Source/TestDafny/MultiBackendTest.cs` [F, exact lines]:
https://raw.githubusercontent.com/dafny-lang/dafny/master/Source/TestDafny/MultiBackendTest.cs . Backends listed in R2:
C#, Java, JavaScript, Go, Python, C++ (limited), Rust (experimental).

**Finding.** Dafny's multi-backend test verifies each test program, then compiles and runs it on every stable backend
and diffs each output against the program's one common expected-output file, `<file>.expect`. A backend may have its own
`<file>.<target>.expect`. A mismatch is tolerated only where the output reports a feature that the backend declares in
its `UnsupportedFeatures` list. The run succeeds only when every backend matched the expected output or reported a known
unsupported feature.

**How much it narrows.** One expected output per program across many backends, Python among them, with an authority (the
expected file) and declared, localized exceptions (per-backend files, per-feature declarations), is Dafny's integration
contract. R2 recorded Dafny's fuzzers and judged agreement "tested, not promised"; the harness is the promise, at the
level of the test suite. What remains: identity stated per run of any program (not per test file), a reference
interpreter as authority (not a frozen file), mismatch notes localized to an event, C99 and Rust, floats under an
envelope, and receipts.

**Corrected wording.** Not-found item 1 becomes: "identity of every run's output and receipt across Python, C99 and Rust,
with a reference interpreter as authority and mismatch notes localized to the first divergent event (Dafny holds its
backends to one expected file per test program, with per-backend overrides and declared unsupported features)".

## N18. Declared reference semantics with listed deviations; byte-identical dual implementations — NARROWS

**Target.** Not-found item 1, §6 item 5. **attacks:** NF, P5.

**Sources.** Scala.js, *Semantics of Scala.js* [F]: https://www.scala-js.org/doc/semantics.html ; Lara (N13) [F];
Catala 1.3.0's trace-identity goal (R2).

**Finding.** Scala.js declares its semantics to be those of Scala on the JVM except for a listed set of differences
(among them the string form of Float and Double, undefined behaviours, and non-strict floats, removed in 1.19.0). Lara
holds a Haskell and a Lean implementation to byte-identical reports.

**How much it narrows.** "A declared authority with localized mismatch notes" exists as language documentation
(Scala.js) and as a differential harness over two implementations (Lara). What remains: as N17.

**Corrected wording.** Cite Scala.js and Lara beside Catala and Dafny in the not-found item's parenthesis.

## N19. One meaning in several spellings is as old as ALGOL 60 — NARROWS

**Target.** §6 item 5 ("prose as a measured lossless spelling"), §T8. **attacks:** P5, T8.

**Sources.**
- P. Naur (ed.), *Revised Report on the Algorithmic Language Algol 60*, approved by IFIP in 1962 [F]:
  https://www.masswerk.at/algol60/report.htm (introduction, "three different levels of language").
- Catala 0.3.0, `Surface.Lexer` documentation [F]: https://ocaml.org/p/catala/0.3.0/doc/Surface/Lexer/index.html .
- Hedy (F. Hermans): keywords in some fifty natural languages over one core [S only].

**Finding.** The ALGOL 60 report recognizes a reference language (the defining one), a publication language (variations
for printing and handwriting) and several hardware representations (condensed character sets with transliteration
rules), and requires the same structure and content in all of them; it notes that the preliminary report already had the
three levels. Catala's lexer keeps punctuation tokens common to all
input languages and keyword tokens whose spelling varies with the input language (English, French, and others), over one
parser.

**How much it narrows.** Typographic and lexical spellings of one meaning, defined by a language, are old (1960) and
current in a legal DSL. What remains: a measurement of that losslessness (the law-seal, N20) across phrasings in a closed
prose grammar, not just keyword substitution. (Prosecution-logic L15: "lossless" is shown on one program.)

**Corrected wording.** Add to *Not new*: "one meaning in several spellings (ALGOL 60's reference, publication and
hardware representations; Catala's language-dependent keywords)".

## N20. Meaning-level hashes that ignore spelling, written in source — NARROWS

**Target.** §6 item 5, §T8's law-seal, not-found item 5. **attacks:** P5, T8.

**Sources.** G. Gonzalez, *Semantic integrity checks are next*, Haskell for all, 3 November 2017 [F]:
https://www.haskellforall.com/2017/11/semantic-integrity-checks-are-next.html ; Unison, *The big idea* [F]:
https://www.unison-lang.org/docs/the-big-idea/ . R3 F4 noted that Dhall pins hashes of normalized imports.

**Finding.** Dhall's semantic integrity check summarizes an imported expression's value, and does not change under
cosmetic edits such as refactoring, reformatting or commenting; the hash is written in source beside the import. Unison
identifies each definition by a hash of its syntax tree, with names kept as separate metadata that does not affect the
hash.

**How much it narrows.** A seal of meaning that is invariant under spelling, and a hash written in source, both exist.
What remains: a seal over a closed prose grammar's phrasings, shown as words (N21).

**Corrected wording.** Add to *Not new*: "meaning-level hashes unchanged by reformatting or renaming (Dhall's semantic
integrity checks, 2017; Unison's content-addressed definitions)".

## N21. Words for numbers in source, and words for hashes, both exist — NARROWS

**Target.** Not-found item 5 ("hashes written as words inside source"). **attacks:** none in `claims.json` (§6 text).

**Sources.** Urbit, *Auras* [F]: https://docs.urbit.org/hoon/auras ; N. Haller, RFC 1760, *The S/KEY One-Time Password
System*, February 1995 [F]: https://www.rfc-editor.org/rfc/rfc1760.txt ; E. J. Gale (Microsoft), US 10,467,392 B2,
*Verifying and controlling computer system state using pronounceable recognizable hash words*, filed 2 May 2017, granted
5 November 2019 [F]: https://patents.google.com/patent/US10467392B2/en . R3 F4 had Hoon's @p and @q from a secondary
source.

**Finding.** Hoon's @p and @q auras write numbers as pronounceable syllable words, with literal syntax in source. S/KEY
renders each 64-bit one-time password, an iterated-hash output, as six short English words from a 2048-word list. The
Microsoft patent derives pronounceable hash words from computer state and compares them with target phrases, showing them
beside the code they summarize, not inside it.

**How much it narrows.** Each half exists: words for numbers inside source (Hoon), words for hashes (S/KEY, the patent),
and hashes inside source (Dhall, N20). Only their conjunction, a hash written as words inside the source it seals, was not
found (queries in §Q). That is a composition of known parts.

**Corrected wording.** Not-found item 5 becomes: "a program's own seal written as words inside that program (words for
numbers in source: Hoon; words for hashes: S/KEY, US 10,467,392; hashes in source: Dhall)".

## N22. A language runtime that grades its own run-time claims by channel — NO-PRIOR-ART-FOUND

**Target.** Not-found item 2. **attacks:** none (supports the not-found claim, narrowed).

**Searched** (queries Q2 in §Q). **Nearest:** Lara grades declared research claims by evidence kind and provenance with a
checker, not a runtime (N13); Lean separates kernel trust from compiler trust per computation, statically (N10); the
Evidential Tool Bus links assurance claims to the tools that produced their evidence (N6); `dafny audit` lists
assumptions (N10).

**Corrected wording.** "A general-purpose language runtime that grades its own run-time claims by channel (Lara grades
declared claims with a checker; Lean tracks kernel and compiler trust statically)."

## N23. An assurance tool reporting gfp ∖ lfp of support as circularity — NO-PRIOR-ART-FOUND

**Target.** Not-found item 3, narrowed by N6. **Searched** (queries Q1). The report itself is Fitting's Kripke–Kleene
undefined set (N1), and its removal is standard (N2); what was not found is its use in an assurance or trust tool.

## N24. Run-time deterministic counting that grades a certificate — NO-PRIOR-ART-FOUND

**Target.** Not-found item 4, narrowed by N14 and N15. **Searched** (queries Q3). Nearest: counted-step ratio bounds
checked statically (Klemen et al. 2018) and run-time budgets by time (QVM 2008).

## N25. §2's "what Ørlǫg does that the lineage did not" all have outside prior art — NARROWS

**Target.** §2's six bullets. They are graded "judged from the sweeps (OBSERVED, not exhaustive)" and are claims about
the lineage, which this finding does not contest. None is new outside it.

| §2 bullet | outside prior art |
|---|---|
| one program compiled to three host languages, with a declared authority and mismatch notes | Dafny's per-program expected file across backends with overrides and unsupported-feature declarations (N17); Catala's interpreter and backends (R2); fiat-crypto generating C, Rust, Go, Java, Zig and JSON from one source, its C and Rust output tested against outside suites, with no claim that the outputs agree (README [F]: https://raw.githubusercontent.com/mit-plv/fiat-crypto/master/README.md) |
| floats inside identity, under a declared envelope | Wasm 3.0's deterministic profile, Rust RFC 3514, JEP 306, Box2D v3, Rapier (all R2) |
| a prose surface | Catala, Inform 7, Lexon, Logical English, ACE, L4 (R2); multilingual keywords (N19) |
| the court's fixed-point standing | Fitting's Kripke–Kleene semantics and the well-founded semantics (N1 to N4); grounded claim standing in Lara (N13) |
| counted cost asymmetry | Klemen et al. 2018 (N14); QVM 2008 (N15) |
| the door's receipts | ftfy's explained, replayable fixes; UTS #55; Rust and GCC bidi lints (R2) |

**Corrected wording.** Keep the list, retitled "What Ørlǫg does that the lineage did not (each has prior art outside the
lineage; see prosecution-novelty N25)".

---

## Proposed §6, consolidated

**Not new**, with the prior art found (R2, R3, prosecution-novelty), added to the present list:
- the court's three standings for a Horn support operator (lfp, gfp ∖ lfp, outside gfp) are the true, undefined and
  false values of Fitting's Kripke–Kleene semantics (Fitting 1985; Fitting & Ben-Jacob 1988, Prop. 3.1); the undefined
  region is the positive loops that the well-founded semantics declares unfounded (Van Gelder, Ross & Schlipf 1991;
  Brass et al. 2001), the cyclic support that stable semantics of argumentation frameworks rejects (Brewka et al. 2013),
  and the self-supported arguments of bipolar frameworks (Alfano et al. 2024); lfp and gfp as well-founded and arbitrary
  derivations is textbook (Leroy & Grall 2009; Keiren & Cleaveland 2023); refusing beliefs whose only support is
  circular is Doyle's truth maintenance (1979);
- "sandwich closed": the Kripke–Kleene fixpoint brackets every fixpoint, so an exact one is the only one (Denecker,
  Marek & Truszczyński 2002);
- trusting each checked theorem, with no expressible trust in the prover: LCF (Milner; Harrison 1995); the Logic of
  Proofs as a basis for programming calculi (Artemov 2001; Alt & Artemov 2001; Bonelli & Feller 2012); a specific proof
  avoids the Löbian obstacle where an unspecified one cannot (Yudkowsky & Herreshoff 2013);
- an expectation's provenance as a decidable property, and the observation that a self-anchored oracle cannot fail
  (Canedo 2026); per-theorem assumption tracking (Rocq, Lean, ACL2, Dafny, besides HOL4); claims whose only evidence is
  an outside principal's signature, logged at run time (Aura 2008); a claims language with evidence typed by kind and
  provenance, grounded standing, an untrusted prose binding and byte-identical reports from two implementations (Lara
  2026);
- a declared bound on the ratio of cost with checks to cost without, in counted resolution steps (Klemen et al. 2018,
  static); run-time overhead budgets for checks (QVM 2008, by time); deterministic solver resource limits (Z3 rlimit);
- one expected output per program for every backend, with per-backend overrides and declared unsupported features
  (Dafny); a declared reference semantics with listed deviations (Scala.js);
- one meaning in several spellings (ALGOL 60; Catala's keywords); meaning-level hashes unchanged by reformatting or
  renaming (Dhall 2017; Unison); numbers as words in source (Hoon); hashes as words (S/KEY 1995; US 10,467,392).

**Not found** (absence of evidence, not evidence of novelty; the queries are in prosecution-novelty §Q):
- identity of every run's output and receipt across Python, C99 and Rust, with a reference interpreter as authority and
  mismatch notes localized to the first divergent event;
- a general-purpose language runtime that grades its own run-time claims by channel;
- an assurance or trust tool that reports gfp ∖ lfp of a support relation as circular support;
- run-time, per-input operation counting used to grade a certificate against the clause it certifies;
- a program's own seal written as words inside that program.

**What may be new** (SPECULATIVE until the courts and the owner rule): applications and the combination, not mechanisms.
1. The Kripke–Kleene / well-founded distinction (Fitting; Van Gelder, Ross & Schlipf) applied to a program's own
   run-time claims, reporting the undefined set as self-certification with a cycle witness, and exactness as "sandwich
   closed" (reported only when lfp is non-empty).
2. LCF's discipline carried from theorems to run-time claims: a claim may cite a checked certificate, and nothing can
   express trust in the checker. Not an answer to Löb's theorem (prosecution-logic L3; N9).
3. Canedo's anchoring as a typing rule: a claim checked only by the author's computation carries zero external bits and
   can never be GROUNDED; grounding needs a ledger line outside the program text.
4. Per-input deterministic operation counts at run time as the criterion of a certificate's standing (against Klemen et
   al.'s static ratio bounds and QVM's time budgets).
5. A closed prose grammar whose phrasings share one law-seal, compiled to Python, C99 and Rust, with receipts and event
   chains equal across them.

The combination's nearest neighbour is Lara (2026); the differences are listed in N13.

## §Q. Queries run for the NO-PRIOR-ART findings

Searches used the session's web search; pages were then fetched as graded above.

**Q1 (N23, and N6).** `assurance case argument "grounded semantics" OR "well-founded semantics" circular argument
detection fixpoint`; `"circular support" claims evidence graph "least fixed point" OR "greatest fixed point" verification
assurance`; `safety case argument cycle "circular argument" GSN tool check acyclic semantics formal "assurance case" logic
programming`; `"assurance case" OR "safety case" "three-valued" OR "Kripke-Kleene" OR "unfounded" circular claims support
evaluation semantics`; `self-certification circular verification claims "greatest fixed point" "least fixed point" gap
report tool certificate trust`; `bipolar argumentation "support cycles" "greatest fixed point" OR "greatest fixpoint"
"least fixed point" evidential support arguments supported only by cycle`; `trust management policy "least fixed point"
"greatest fixed point" circular trust dependencies credential cycle semantics`; `Carbone Nielsen Sassone "A formal model
for trust in dynamic networks" least fixed point information ordering unknown circular`; `"Tool Integration with the
Evidential Tool Bus" VMCAI 2013 Datalog claims evidence`. The fortiss ExplicitCase help page, which a search extract says
checks for circular argumentation, refused the connection and was not read.

**Q2 (N22).** `programming language runtime assertions graded by evidence source provenance "epistemic" status claims
checked computation vs external oracle`; `Evidential Tool Bus Rushby claims evidence provenance tools "evidential tool
bus" Cruanes Hamon Owre Shankar 2013`; `Dafny "dafny audit" command report assumptions axiom extern assume trusted`;
`Lean 4 reference "#print axioms" "ofReduceBool" native_decide trust compiler axiom sorryAx`.

**Q3 (N24).** `runtime verification monitoring overhead budget "instruction count" OR "operation count" deterministic
bound monitor cost relative to program cost enforcement`; `QVM "an efficient runtime for detecting defects in deployed
systems" Arnold Vechev Yahav overhead manager budget sampling`; `Dafny "resource limit" rlimit deterministic instead of
time limit verification "resource count" Z3 documentation`.

**Q4 (N21).** `source code literal content hash written as pronounceable words mnemonic encoding of sha256 in program text
checksum words identifier`; `Hoon aura "@q" phonemic base literal syntax ...` (no Urbit page returned; the Urbit
documentation was then fetched directly).

**Q5 (N17, the not-found residue).** `Dafny "testDafnyForEachCompiler" expect file each backend output compared
integration tests` (then the Dafny repository files were fetched directly); `Catala programming language legal DSL
"French" "English" "Polish" localized syntax keywords documentation`.

## Unread leads (not used as evidence)

Cited by sources read here, not opened: Fitting 1985 (J. Logic Programming 2(4)); Lassez & Maher 1983/85, *Optimal
fixedpoints of logic programs* (cited by Fitting & Ben-Jacob for making the three values explicit); Apt & van Emden 1982;
Van Gelder, Ross & Schlipf 1991 (read only through Brass et al. and R1a); Doyle 1979 and his 1978 TR-419 (MIT DSpace
returned 403 and 429); Elkan 1990; Weeks 2001; Edinburgh LCF 1979; Alt & Artemov 2001 and Artemov & Bonelli 2007 (search
extracts only); Rushby, *An Evidential Tool Bus* (ICFEM 2005; SRI's server refused the connection); McMillan 1999 on
circular assume-guarantee reasoning, a sound form of circular support that the court's CIRCULAR label would not
distinguish from a vicious one.

## Where this happened

Run here: this Windows host, 2026-10-25, with the session's web search and fetch tools; PDFs were saved under the
session scratchpad (`pn-dl/`, outside the ØRLǪG root) and read with `pdftotext`. No ØRLǪG file other than this one was
written or changed.
