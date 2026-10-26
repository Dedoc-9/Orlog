# Debate record: the prior-art and limits survey for the doppler (2026-10-26)

A subagent's report, saved verbatim by the judge. It is model output, not the owner's words, and carries no
authority. Its source grades ([P], [A], [F], [S], [B], [U]) are its own and say how each source was read; "derived
here" marks its own reasoning. Its working files, among them refs.tsv with every confirmed DOI, are in the session's
scratchpad, not in this repository.

---

# The doppler: prior art and limits (survey, 2026-10-26)

**Bottom line.**
- For Ørlǫg, the question is decidable, because runs are total and finite-state.
- It is coNP-complete for straight-line code and PSPACE-complete once there are procedures (derived from published results). So no instrument removes incompleteness cheaply.
- Three things can be ruthless:
  - a sound analysis whose certificate a separate checker accepts;
  - exhaustive search over a published domain;
  - refutation that anyone can attempt.
- Symmetry does not change this arithmetic. Certifying one generator costs as much as the question itself, unless the symmetry holds by typing.
- Noether's theorem does not apply to updates that are non-variational, discrete and rounded.

**Read first:**
- `research/doppler/PROPOSAL.md`, all four pastes;
- `research/ragnarok/RESEARCH.md`, whose ground is not repeated here;
- RULINGS R4, R6, R9 and D8; DOCTRINE T5, T7 and T12; SPEC's caps;
- `evidence/run1-r6-indirect.txt`.

No tracked file was written. Scripts, PDFs, extracted text and `refs.tsv` (every confirmed DOI) are in the scratchpad's `doppler-research` folder.

**Grades.**
- [P]: full text obtained, and the cited theorem or section read in it.
- [A]: abstract read raw from Crossref, OpenAlex or arXiv.
- [F]: page read through the summarizing fetch.
- [S]: search extract only.
- [B]: record confirmed, content from memory.
- [U]: unconfirmed.

"Derived here" marks my own reasoning. One model family wrote it, so it shows consistency, not truth.

## (a) Approaches, graded

| approach and sources | guarantee | cost | fit for Ørlǫg |
|---|---|---|---|
| **Security types.** Denning & Denning 1977, 10.1145/359636.359712 [A]; Volpano, Irvine & Smith 1996, 10.3233/JCS-1996-42-304 [P] (Thm 6.8: in a well-typed program, terminating runs from low-equal memories end low-equal); Hunt & Sands 2006 [A]; survey: Sabelfeld & Myers 2003 [P] | sound (termination-insensitive), incomplete, decidable | polynomial; the derivation is a certificate | high: R6 without the coarse rule |
| **Their false alarms.** King, Hicks, Hicks & Jaeger 2008, 10.1007/978-3-540-89862-7_4 [P]: 870 of 887 alarms were implicit flows and 725 were false; 30% false for conditionals, 85% for exception-induced flows | measured | — | expect refusals to behave like exceptions |
| **Termination sensitivity.** Askarov, Hunt, Sabelfeld & Sands 2008, 10.1007/978-3-540-88313-5_22 [P]: with output, termination-insensitive noninterference can leak a whole secret, though only by brute force | progress-sensitive is stronger | — | refusals and evaluation counts are Ørlǫg's termination channel |
| **Slicing.** Weiser 1984 [A] (minimal slices uncomputable); Hammer & Snelting 2009 [B]; Wasserrab, Lohner & Snelting 2009, 10.1145/1554339.1554345 [A] (machine-checked PDG-based noninterference) | sound, incomplete, decidable | polynomial | high: fork 4's slice has a checked precedent |
| **Dependency semantics.** Abadi et al. 1999, DCC [A]; Cousot 2019, 10.1007/978-3-030-32304-2_19 [P]: dependency is a hyperproperty and exactly uncomputable (Rice); definite dependency under-approximates, potential over-approximates | framework | — | names the lattice |
| **Dynamic slicing, taint.** Korel & Laski 1988 [B]; Agrawal & Horgan 1990 [A]; relevant slicing, Gyimóthy et al. 1999 [S]; Schoepe, Balliu, Pierce & Sabelfeld 2016, 10.1109/EuroSP.2016.14 [P]: taint enforces *explicit secrecy*, which is incomparable with noninterference | per run; unsound for independence | linear | low |
| **Sound monitors.** Austin & Flanagan 2009/2010 [A] (no-sensitive-upgrade stops a run that would partly leak); Russo & Sabelfeld 2010 [A] (no purely dynamic sound monitor accepts every flow-sensitively typable program) | sound per run; refuses | small | can withhold grounding, never grant it |
| **Multi-execution.** Devriese & Piessens 2010, 10.1109/SP.2010.15 [P] (Thm 1: sound for every program, termination included; Thm 2: transparent for noninterferent ones); faceted values, Austin & Flanagan 2012 [A] | sound and precise, by construction | runs × security levels | a shadow claim with ports set to defaults is port-free, but it is about another run |
| **Self-composition, product programs, relational logic.** Barthe, D'Argenio & Rezk 2004/2011 [A]; Terauchi & Aiken 2005 [B]; Benton 2004 [A]; Barthe, Crespo & Kunz 2011 [S]; Clarkson & Schneider 2010, 10.3233/JCS-2009-0393 [P] (k-safety reduces to safety of the k-fold product); Sousa & Dillig 2016 [A]; Pick et al. 2018 [A] | sound, relatively complete | PSPACE (b4) | the relational invariant is the certificate |
| **Unwinding.** Goguen & Meseguer 1984, 10.1109/SP.1984.10019 [A] (a necessary and sufficient condition, for their MLS model) | sound and complete there | the relation may be as large as the state space | a per-tick obligation |
| **HyperLTL model checking.** Clarkson et al. 2014, 10.1007/978-3-642-54792-8_15 [P]; Finkbeiner, Rabe & Sánchez 2015 [B] | decidable for finite state | ∀∀ formulas: NLOGSPACE in the number of states | explicit-state self-composition only |
| **Relational symbolic execution, differential fuzzing.** Milushev et al. 2012 [B]; Farina, Chong & Gaboardi 2019 [A]; DifFuzz 2019 [A] | refutation; bounded proof | needs an SMT solver | low |
| **Testing noninterference.** Hritcu et al., ICFP 2013 [A] and JFP 2016, 10.1017/S0956796816000058 [P]: test pairs are made by varying the secret part; the generator changes time-to-failure by orders of magnitude; testing single-step unwinding caught every planted bug in under 20 ms but needed a hand-found invariant; states that are too small miss bugs | refutation | cheap | this is the doppler, with a method for evaluating it |
| **Certified checkers.** Barthe, Pichardie & Rezk 2007 [S]; Beringer & Hofmann 2007 [A] (typing derivations become program-logic proofs); Besson, Jensen & Pichardie 2006 [A] (small fixpoint certificates); Murray et al. 2013 [A] (machine-checked noninterference for seL4's C) | checkable | linear checks | item 6: yes, for sound analyses |
| **Quantitative flow.** Smith 2009 [B]; Clark, Hunt & Malacaria 2007 [A]; Backes, Köpf & Rybalchenko 2009 [A]; Yasuoka & Terauchi 2010/2011 [P]; Černý, Chatterjee & Henzinger 2011 [P] | zero leakage = noninterference | harder (b7) | low: a claim is one bit |
| **Symmetry reduction.** Emerson & Sistla 1993/1996 [B]; Ip & Dill 1993 [P]/1996 [B]; Clarke et al. 1993/1996 [B]; Jha 1996 thesis [P]; Donaldson & Miller 2006, 10.1007/11813040_36 [P]; surveys: Miller et al. 2006 [A], Wahl & Donaldson 2010 [A] | exact for G-invariant properties when G ≤ Aut(M) | gain ≤ \|G\|; computing orbit representatives is NP-hard | speeds up state search; does not test independence |
| **Symmetry declared in the model text.** Murφ scalarsets (Ip & Dill [P]: assignment, equality and indexing only; no arithmetic, constants or order); SymmSpin [S]; UPPAAL scalars [S]; Essence unnamed types [S]; FDR, Gibson-Robinson & Lowe 2019 [A]; data independence, Wolper 1986 [A]; TLC's SYMMETRY declaration, which is not checked [F] | sound by typing; TLC's can hide errors | a type check | ports used only through equality |
| **Parametricity, indexed types.** Reynolds 1983 [S]; Wadler 1989 [A]; Kennedy 1997 [A]; Atkey, Johann & Kennedy 2013, 10.1145/2429069.2429082 [P] (translation, rotation and scaling invariance from types; formalized in Coq; no checker built); nominal sets, Pitts 2003 [B]; noninterference from parametricity: Tse & Zdancewic 2004, Bowman & Ahmed 2015, Algehed & Bernardy 2019 [A] | free theorems over exact arithmetic | type checking | long term |
| **Metamorphic testing.** Chen, Cheung & Yiu 1998 [A]; Segura et al. 2016 [A]; Kanewala & Bieman 2014 [P]; PhyFu 2023 [A][F] | refutation; relations chosen by hand | cheap | the doppler is one such relation |
| **Discrete mechanics.** Marsden & West 2001, 10.1017/S096249290100006X [P]; Dehnen 2002 [P]; Levesque & Verlet 1993 [S] (integer arithmetic, bit-reversible); Earn 1994 [A]; Rein & Tamayo 2017 [A] | exact momentum maps for variational integrators | — | T7 stands |
| **Checked declarations.** Eiffel, Meyer 1992 [A]; Dafny, Leino 2010 [B]; Why3 [B]; SPARK `Depends` [F], after Bergeretti & Carré 1985 [A]; Liquid Haskell class laws, Liu et al. 2020 [A]; Nominal Isabelle `[eqvt]` [S]; ACL2 certificates [S] | declared and checked | varies | precedents for sealed equivariance |
| **Public falsification.** Naor 2003 [S] (grades assumptions by challenges whose answers can be checked efficiently); the SHA-1 collision, Stevens et al. 2017 [B]; Agora 2024 [A] (bounties for checking untrusted proofs) | incentives to refute | — | PORT-FREE(D) is falsifiable like collision resistance, but a bounty measures search effort, not truth |

## (b) Decidability and complexity in Ørlǫg's setting

1. **Undecidable for Turing-complete languages.**
   - Sabelfeld & Myers 2003, 10.1109/JSAC.2002.806121 [P], reduce divergence to confidentiality.
   - Dam 2006, 10.1145/1111037.1111044 [P], Thm 3: trace-based and input-output noninterference are undecidable for while-programs. Strong low bisimulation is decidable relative to a decidable expression theory.
   - Rice 1953 [B].
   - Every reduction needs unbounded loops or unbounded data.
   - Goguen & Meseguer 1982 [B] defined noninterference; they proved no undecidability.
2. **Ørlǫg is finite.**
   - Runs are total, While bounds are at most 2^62, and lists and texts are at most 2^24 (SPEC).
   - A RUN-1 session is therefore a finite-state transducer over its log, and port-independence is decidable, both per session length and for all lengths.
   - "Cannot exist" is false here. What holds is intractability.
3. **Straight-line code: coNP-complete.** Yasuoka & Terauchi 2010, 10.1109/CSF.2010.9, Thm 3.9 [P], reduce it to UNSAT by self-composition and back.
4. **Code with recursion-free procedures: PSPACE-complete (derived here).**
   - Reachability is PSPACE-complete even for deterministic, acyclic, hierarchical Boolean programs, and NP-complete when the depth is bounded (Godefroid & Yannakakis 2013, 10.1007/978-3-642-36742-7_16, Thms 3–4 [P]).
   - Self-composition reduces noninterference to that reachability. Reachability reduces back by copying the port into the observed variable at the target.
   - So noninterference is PSPACE-complete in program size, treating the caps as constants.
5. **Explicit state.**
   - For deterministic systems, noninterference is a safety property of the |S|² product, decidable in polynomial time (van der Meyden & Zhang 2007 [P]).
   - ∀∀ HyperLTL is NLOGSPACE in the number of states (Clarkson et al. 2014 [P]).
   - Here |S| is 2^(64 × the number of 64-bit state words).
6. **Certificates.**
   - Unwinding relations are complete (Goguen & Meseguer 1984 [A]), but they may be as large as the state space.
   - Short certificates for every independent program would put a coNP-complete problem in NP (derived from item 3).
7. **Quantitative flow is harder.**
   - Bounding the leakage is PSPACE-complete for finite-state programs (Černý et al. 2011 [P]).
   - It is not k-safety for any k, and it is PP-hard for loop-free programs (Yasuoka & Terauchi 2011 [P]).
8. **Symmetry.**
   - An orbit has at most |G| states, so the quotient keeps at least |S|/|G| of them. Ip & Dill's reduction equals the average class size.
   - Deciding whether a permutation preserves a succinct Boolean transition relation is coNP-complete (Jha 1996, Thm 4.4.1 [P]).
   - On canonical OBDDs it is a comparison, but OBDDs of integer multiplication are exponential (Bryant 1991 [B]).
   - The orbit problem is at least as hard as graph isomorphism (Jha Thm 3.4.1; Ip & Dill [P]).
   - The bounded orbit problem is NP-complete (Jha Thm 3.4.2).
   - Computing orbit representatives is NP-hard (Donaldson & Miller 2006 [P]).
   - OBDDs of the orbit relation are exponential for transitive groups (Jha).
   - Proving symbolically that σ∘tick = tick∘σ is an equivalence check between two closely related programs, the setting of regression verification (Godlin & Strichman 2009 [A]).
   - Certifying one generator can cost as much as the independence question.
9. **The cost of exhaustive search.**
   - It takes |D|^(p·T) runs: p ports, T ticks, domain D.
   - One i64 port for one tick is 2^64 ≈ 1.8×10^19 runs, about 585 years at 10^9 runs a second.
   - Bounded verdicts therefore need a small declared D.

## (c) Design lessons

1. **The axis is cost, not possibility.** The honest verdicts are:
   - PORT-REACHABLE: a witness pair that can be replayed;
   - PORT-FREE: only from a sound analysis whose certificate a separate checker accepts (a typing derivation, a slice, an unwinding relation);
   - SURVIVED(D): from exhaustive search over a declared domain D;
   - UNKNOWN otherwise.

   This is Cousot's definite and potential dependency.
2. **Refusals and evaluation counts are observations.**
   - Under R4, a port can move a refusal earlier and so change "true in n of n" (D8).
   - A PORT-FREE that ignores this is only termination-insensitive (Askarov et al.).
   - Flows through refusals will dominate the false alarms, as exceptions did (King et al.).
3. **Taint is not a second verifier.** "Ignoring implicit flows makes taint trackers unsound" (Schoepe et al. 2016). Use a sound monitor or the slice instead.
4. **Test per tick; prove with a relation.**
   - Variation pairs and single-step unwinding tests find planted defects fastest (Hritcu et al.).
   - Take a group that fixes the initial state, commutes with the tick and preserves the claim. The claim is then constant on each orbit of logs; this is an unwinding argument whose relation is the orbit relation. Independence still needs orbits that join every pair of logs differing in the port (derived here).
   - ACCIDENTALLY-CONSTANT is the incompleteness of that certificate language, like `if h then l:=1 else l:=1` under typing.
5. **Get symmetry by typing, not by enumeration.**
   - Scalarsets, unnamed types and indexed types make symmetry hold by restricting the operations allowed.
   - TopSPIN checks proposed generators against the model text (Donaldson & Miller 2006).
   - TLC's unchecked declarations hide errors.
   - In Ørlǫg, checked overflow makes translation partial, and rounding breaks scaling and rotation: discretized rotations are bijective only for one family of angles (Nouvel & Rémila 2004 [S]).
   - Negation is exact under T5's symmetric half-even rounding, except at the most negative value.
6. **Conservation belongs to the update, not to Noether.**
   - Discrete Noether needs a discrete Lagrangian invariant under a Lie group. With forcing, it holds only when the forces are orthogonal to the group action (Marsden & West, Thms 1.3.3 and 3.2.1 [P]).
   - For translations, orthogonal means the forces sum to zero. Newton's third law is the content, so T7 stands (derived).
   - Fixed-step symplectic integrators cannot conserve energy exactly for non-integrable systems (Ge & Marsden 1988, via Marsden & West).
   - Roundoff makes the energy error a random walk (Hairer, McLachlan & Razakarivony 2008 [S]).
   - Exact symplecticity under rounding needs lattice maps (Earn 1994 [A]).
   - Particle codes get exact momentum from evaluating each pair symmetrically (Dehnen 2002 [P]).
   - A conservation guard is a metamorphic oracle with D10's blind spot.

## (d) The pasted claims against the literature

*First paste.*
- Declaring a port is a global grounding cost: SUPPORTED, as a known conservative default (SPARK, without a `Depends` contract, assumes every output depends on every input [F]).

*Second paste (the doppler).*
- Noninterference is Rice's canonical undecidable case (Goguen–Meseguer): SUPPORTED for Turing-complete languages; the attribution is loose (b1).
- A static doppler that decides independence "cannot exist": CONTRADICTED for Ørlǫg (b2–b4).
- R9 makes runs finite-state: MIXED. Finiteness comes from i64 and the 2^24 caps; R9 only bounds operations.
- Independence cannot be witnessed: MIXED. Certificates exist; short ones do not in general (b6).
- The witness is a pair of runs differing in one port: SUPPORTED (2-safety; Hritcu; DifFuzz).
- Silence is not proof, so D must be published: SUPPORTED.
- A dependence constant across D is "invisible, not absent": CONTRADICTED when D is the whole domain, since a constant claim is independent; OPEN otherwise.
- The domain as a standing bounty: MIXED (table, last row); no precedent found for program independence.
- PORT-FREE / PORT-REACHABLE / UNKNOWN, with UNKNOWN never grounding: SUPPORTED (Cousot).
- Taint is "sound for the observed run": CONTRADICTED (lesson 3; Sabelfeld & Myers: confidentiality is not a property of one path).
- A witness with clean taint means taint is broken: CONTRADICTED; a branch not taken explains it.
- Taint says reachable but no witness is found, so investigate: SUPPORTED.
- Nothing technical mitigates a shared author: MIXED. Exhaustive search over a declared D and separately checked certificates do.
- Cost is exponential, so the doppler is an admission-time tool on small domains: SUPPORTED, with Hritcu's caveat that states that are too small miss bugs.
- Log only the ports that reach state: OPEN; the replay literature was not surveyed, and RUN-1 logs every port (D1).
- Slice and doppler agreeing is "much stronger": MIXED. Once a sound slice proves independence, the doppler serves only to test the slicer.

*Third paste (symmetry, Noether).*
- Quotienting makes properties independent of the frame: SUPPORTED in spirit (Atkey et al.).
- Emerson & Sistla 1993/1996 is textbook symmetry reduction: SUPPORTED.
- One representative per orbit "gives invariance everywhere": CONTRADICTED. Invariance makes the claim constant within each orbit; independence needs it constant across orbits too, and the checks number at least |logs|/|G|.
- A handful of generators is the trick: MIXED. Generators suffice to verify a symmetry group (Jha), but the gain is bounded by |G| and computing representatives is NP-hard.
- σ must commute with the tick: SUPPORTED. The claim must also be invariant, and σ must fix the initial state (derived).
- The check is exhaustive because R9 caps each tick: CONTRADICTED (b8, b9).
- A discharged symmetry is a certificate, not testimony: SUPPORTED; TLC shows what happens when it is not discharged.
- The certificate rides a channel that can ground: OPEN; this is a question for the court, since T12 grounds only ratified seals and never computation.
- The doppler serves as the certificate's refuter: SUPPORTED (witness validators, RESEARCH.md).
- Accidental constancy as a named residue: SUPPORTED, but silence over a partial D cannot establish it.
- A certified continuous symmetry "is a conservation law": CONTRADICTED (lesson 6); Ørlǫg's grids admit no continuous groups.
- Conservation is the only channel that needs no oracle: CONTRADICTED; metamorphic relations need none either.
- Conservation catches a bug in the shared front end: MIXED; only bugs that break the conserved structure (D10).
- Directions in the log space found inert by a subgroup tell replay what to log: OPEN.
- Laws declare their symmetries, or a small search finds them: SUPPORTED (scalarsets; automorphisms of a small static graph, Donaldson & Miller 2006 [P]).

*Fourth paste (sealed equivariance).*
- The obligation is discharged exhaustively over R9-bounded state: CONTRADICTED (b8, b9).
- The certificate becomes part of the law seal: OPEN. ACL2 keeps its `.cert` files apart from the book, checksummed, and voids them under another ACL2 version [S].
- Typical symmetry work is external and never ratified: CONTRADICTED. Scalarsets, SymmSpin, UPPAAL, Essence and TLC all declare symmetry in the model text; ratification is Ørlǫg's own notion.
- Imported certificates need no new discharge: MIXED. A commutation certificate is about one tick function; reusing it across laws needs a typed, compositional argument (Atkey et al.; Kennedy).
- Generators compose algebraically: SUPPORTED (Jha).
- The certificate carries equal weight in all three backends: OPEN; it holds only where the executions are byte-identical.
- Noether yields energy and momentum, and "energy cannot drift": CONTRADICTED (lesson 6).
- "No language" makes structural invariants first-class: CONTRADICTED (the table's rows on checked declarations and on symmetry declared in the text). Invariants ratified by an owner: NOT FOUND.
- Goguen & Meseguer 1982 is symmetry prior art: misattributed; it is about noninterference.
- R13's falsifier, a domain that is unbounded: ill-posed, since Ørlǫg's domains are bounded. The real hazard is a σ that is not a bijection, because of overflow.

## (e) NOT FOUND: candidate novelty, graded only as absence of evidence

- A claim's standing that is withheld when the claim depends on a port, and restored by a checked independence certificate.
- Symmetry certificates used as evidence of noninterference outside typing; parametricity gives it through types.
- Bounded-independence verdicts, with their domain published, as a public challenge.
- A program identity that seals its own equivariance certificate.
- Bounded noninterference over tick logs that is sensitive to refusals (progress sensitivity exists: Askarov et al.).
- Conservation laws evaluated as test oracles for physics code. PhyFu uses other physical laws as oracles, with thresholds tuned by hand [F]. Symmetry-based metamorphic relations beyond permutation relations in machine learning [S].
- A published PSPACE bound for noninterference of recursion-free programs; it is only derived here.

## Queries run

**Web searches:**
- noninterference undecidable, Rice's theorem;
- complexity of noninterference for finite-state systems;
- Godefroid–Yannakakis, Boolean programs;
- Ip–Dill scalarsets;
- TLC SYMMETRY;
- Atkey–Johann–Kennedy;
- Volpano–Irvine–Smith PDF;
- Austin–Flanagan no-sensitive-upgrade;
- Marsden–West discrete Noether;
- Finkbeiner–Rabe–Sánchez;
- Clarke et al. orbit problem;
- Emerson–Sistla;
- Brouwer's law;
- Earn–Tremaine;
- Levesque–Verlet;
- conservation laws as test oracles (three phrasings);
- Kanewala–Bieman;
- symmetry metamorphic relations;
- physics-engine testing;
- Naor, falsifiable assumptions;
- verification bounties;
- Nominal Isabelle `[eqvt]`;
- SPARK `Depends`;
- Liquid Haskell class laws;
- Cousot, abstract semantic dependency;
- Barthe–Crespo–Kunz;
- King et al., implicit flows;
- Schoepe et al., explicit secrecy;
- Reynolds 1983;
- Nouvel–Rémila;
- relevant slicing;
- Barthe–Pichardie–Rezk;
- short noninterference certificates;
- ACL2 certificates;
- SymmSpin and UPPAAL;
- Essence unnamed types.

**APIs:** Crossref, by DOI and by title (about 140 records); OpenAlex; arXiv; Semantic Scholar (which returned no abstracts).

**Page fetches:** PhyFu (ar5iv), the TLA+ learning page on symmetry, AdaCore's flow-analysis chapter.

**Limits.**
- Springer pages refused the fetch.
- These PDFs did not download: Emerson–Sistla 1996, Ip–Dill 1996, Finkbeiner et al. 2015, Naor 2003, Austin–Flanagan 2009.
- The JAIR PDF of Lang et al. 2003 has no text layer.
- Contents graded [B] are stated from memory.
- `refs.tsv` was cleaned of search mismatches; one DOI (Gyimóthy et al.) comes from a search extract and is marked as such.
