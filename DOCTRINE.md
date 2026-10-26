# ØRLǪG: doctrine and design record, edition 2 (2026-10-25, after the first court)

*Ørlǫg*, "primal law", is what the Norns laid down: *þær lǫg lǫgðu* (Völuspá 20). This is a working name, for the
owner to rule on.

**Status.** Research in its own repository, [github.com/Dedoc-9/Orlog](https://github.com/Dedoc-9/Orlog), under the
GNU AGPL v3 (moved there from a session scratch folder on 2026-10-25, the owner's choice of DOCTRINE §9 fork 2). It is
not admitted or registered anywhere, it has no Verðandi authority, and the Verðandi checkout is untouched.

**Edition 2.** It replaces edition 1 after an adversarial court:
- a logic prosecution: `court/prosecution-logic.md`, findings L1–L20, of which 4 were FATAL;
- a novelty prosecution: `court/prosecution-novelty.md`, findings N1–N25;
- an engineering red team: `court/redteam-eng/`, reproducers E1–E22;
- a clean-room twin written from SPEC.md alone: `twin/NOTES.md`, 62 ambiguities.

Where edition 1 overclaimed, this edition says so in the stage concerned. §10 lists every finding and its disposition,
and the verdict computed by the court engine.

**Grades** follow AGENTS.md §6. "Here" means this Windows host, in this session, under clang 22.1.8, rustc 1.96.1 and
CPython 3.14.5. Counts are not typed in this text. They are read from `evidence/selftest-run.txt`, whose last line
is the self-test's summary (Urðr L16, L75).

**The rule under every rule.** Integrity is not truth. Ørlǫg computes integrity, and it computes the truth of each
claim's formal condition in a run. It cannot compute whether a condition says what its author meant: the intent is not
in the text (the oracle problem).

---

## 0. The request, and the paradox it names

**The request.** The owner asked for a prose language, byte for byte compatible across Python, C99 and Rust, that
repairs byte mismatches safely and says so, is deterministic in fixed and floating point, and carries verification
when it runs. He wanted it as a built-in answer to the verification paradox in the Plankton parable: a verifier that
shares the generator's priors rubber-stamps it, and a fully independent verifier costs as much as generation.

**Horn A: shared priors.** These are motivation and context, not theorems the mechanism instantiates (court L1, L2):
- **Löb (1955)** is about formal provability. The robot's "looks perfect, boss" is an analogy to it, not an instance.
- **Montague (1963).** A theory with a self-applicable factive predicate, closed under necessitation, is inconsistent.
- **The data processing inequality.** A verdict computed only from the artefact cannot carry more about the truth than
  the artefact does. It is a necessity bound.
- **Aumann (1976)**, on common priors.
- **Correlated judges.** Ladha (1992); Dietrich & List (2004); the lineage's GEN-010 and law 12.
- **An empirical warning.** Language-model judges favour models similar to themselves (Goel et al., ICML 2025).

**Horn B: cost.** Generation is search, and an independent re-run repeats it. Coincident failures make diversity
weaker than independence: Knight & Leveson (1986); Eckhardt & Lee (1985).

**What Ørlǫg does instead.** It does not solve the paradox, and nothing could: Rice's theorem is context. It does three
things:
1. It computes what can be computed: integrity, and the formal truth of each claim in a run.
2. It types every claim by the channel it rests on.
3. It refuses to let a claim's standing exceed its channel. Truth about intent enters only through a ledger the
   program text cannot write.

---

## 1. The stages, each with its theorem, as narrowed by the court

### T0. What is computed, and what is not

- **Mechanism.**
  - Three identities: raw-seal, text-seal and law-seal (the typed meaning, §T8).
  - A receipt per run: output sha256, event hash chain, operation count, claim tallies.
  - The arbiter compares the reference and the three backends byte for byte.
- **Theorems.** None is instantiated (court L2). Tarski's undefinability, Rice and Gödel II have no instance in a
  closed, total language whose claims cannot refer to claims. They are context for why intent cannot be computed in
  general.
- **Standing.** Non-factive because its inputs can be wrong: the author's declared premises and channel labels, and a
  forgeable ledger. Edition 1 cited Montague for this; that reason was wrong (L2).
- **Evidence.** MEASURED here: the self-test's corpus and refusal rows (four executions byte-identical).
- **Does not show.** Intent. Identity on other hosts.

### T1. Certificates checked at run time, and no way to express trust in the checker

Theorems: certifying algorithms (McConnell, Mehlhorn, Näher & Schweitzer 2011); the LCF discipline (Milner; Harrison
1995), carried from theorems to run-time claims.

- **Mechanism.**
  - `by the certificate of §k` attaches a check to a clause. The runtime evaluates the check when it is reached, and
    the court records its counted cost against the clause.
  - The language contains no construct that refers to the verifier, the runtime or the court, so neither wholesale nor
    per-proof reflection exists in it.
  - The court never infers that §k is correct from the check. A person must ratify the claim's own seal: that is where
    a characterization such as Bézout's is accepted for this exact check.
- **Withdrawn from edition 1** (court L3, FATAL). "Artemov's Logic of Proofs against Löb", and "a syntactic answer to
  Löb's obstacle". Ørlǫg has no provability predicate, so it lies outside Löb's hypotheses rather than answering them.
  Artemov's distinction between per-proof and wholesale trust remains a motivating analogy (N8, N9).
- **Evidence.** MEASURED here:
  - the Bézout certificate is evaluated in all four executions;
  - the plant `law-gcd-wrong-answer` (g doubled) makes it refuse at §12;
  - the prosecution's weak check under Bézout's name (D2) stays UNGROUNDED.
- **Does not show.** That a certificate condition characterizes the clause's result. The court cannot see that; the
  ratifying person must judge it.

### T2. A claim's standing never exceeds its channel

The theorem is the DPI, read as a necessity bound only (court L4).

- **Mechanism.**
  - `by computation` and `by agreement of` (an author's label, read as computation: L5) carry no bits about intent
    beyond the text. They can be WELL-FOUNDED, never GROUNDED.
  - Any other channel is GROUNDED only through a ledger line that ratifies **this claim's own seal**: its law
    statement, its claim id and its law-seal.
  - A theorem ratified by name alone grounds nothing. One name-keyed line had grounded every claim quoting the name
    (L4, D3), including a one-operation check (L8, D2). Repaired.
- **Evidence.** MEASURED here, in self-test rows:
  - computation and agreement claims stay UNGROUNDED with their seals ratified;
  - the plant `court-grounds-computation` is caught;
  - name-only theorem ratifications ground nothing;
  - a weak claim's seal differs from the full certificate's, so a ratification cannot be lifted.
- **Does not show.** Who wrote a ledger line: nothing authenticates a person.

### T3. A counted reading, not Blum's little-oh

- **Mechanism.** The court reports the check's counted operations against the certified clause's at this input:
  CHEAPER (at most ½), NOT CHEAPER, or CLAUSE NOT RUN.
- **Withdrawn from edition 1** (court L6, FATAL, and L7):
  - "cheaper forces different" and "enforces Blum's 'different'". Operations are counted at unit cost, so one `square
    root` can hide unbounded work, and a recomputation by a built-in reads CHEAPER (D1).
  - Blum's rule (Blum 1988; Wasserman & Blum 1997, who call the independence it buys a "heuristic contention")
    compares with the fastest program for the task, and is undefined on Ørlǫg's bounded domains.
  - "RECOMPUTATION" as a label: reading the converse of Blum's rule is denying the antecedent.
- **Prior art** (N14–N16): counted-step ratio bounds checked statically (Klemen et al. 2018); run-time overhead budgets
  by time (QVM 2008); deterministic solver limits (Z3 rlimit).
- **Evidence.** MEASURED here: Bézout reads CHEAPER; a costly check reads NOT CHEAPER; a clause that never ran reads
  CLAUSE NOT RUN.
- **Does not show.** Independence, or difference. Those must be argued from the check's characterization.

### T4. Circular support as the Kripke–Kleene undefined set

**The theorem, correctly attributed** (court N1–N4, L9, L11):
- For a Horn support operator G, the standings lfp(G), gfp(G) ∖ lfp(G) and outside gfp(G) are the true, undefined and
  false values of Fitting's Kripke–Kleene semantics (Fitting 1985; Fitting & Ben-Jacob 1988).
- The undefined region is the positive loops that the well-founded semantics declares unfounded (Van Gelder, Ross &
  Schlipf 1991).
- When lfp = gfp, G has exactly one fixed point and iteration from any assignment reaches it: Denecker, Marek &
  Truszczyński's (2002) exactness, by monotonicity and finite height.
- Cousot's chaotic-iteration result (IMAG R.R. 88, 1977) needs monotonicity and a start below the least fixed point.
  The verdicts here use one deterministic schedule, and the chaotic row tests `chaotic_lfp` on a fixture, not a
  verdict.
- "Tight" dates from Lifschitz 1996.

**Mechanism.**
- CIRCULAR means held, with all declared support held, and some support chain reaching a cycle: on one, or resting on
  one. The court names the cycle when there is one.
- UNREACHED is its own standing.
- The sandwich is reported CLOSED only when the backends agreed and lfp is non-empty; otherwise it is VACUOUS. Edition
  1 reported "closed" over a backend bug, and over nothing (L10).

**Does not show.** Undeclared dependence. Premises are what the author declared; the parable's robot declares nothing
(L10, D7).

**Evidence.** MEASURED here:
- Plankton's cycle, with `§3 -> §4 -> §5 -> §3` named;
- `court-accepts-gfp` caught;
- VACUOUS on an empty program and on a contested run;
- inline claims each keyed by claim id (L17).

### T5. Determinism by construction, in fixed and floating point

The court found this sound: S-rows, including the prosecutor's own control experiment on the FMA cause.

**Mechanism.**
- **Int:** checked i64, exact `divided by`, and Euclidean quotient and remainder (Boute 1992).
- **Fix:** Q31.32, each product and quotient rounded once, half to even, symmetric under negation.
- **Float:** binary64 basic operations, every NaN canonical and decided on the bits.
- No library transcendentals.
- No contraction.
- Exact decimal printing.
- Conversions are exact or refused, unless `rounded` is written.
- Literals are rounded once, and noted.

**Evidence.** MEASURED here:
- 20,015 vectors pass in two independently written runtimes, verified by me;
- the chaotic orbit, the physics and the falling body are byte-identical four ways;
- a naive C loop under `-ffp-contract=fast -march=native` uses 12 FMA instructions and diverges, while Ørlǫg's
  generated C under the same flags uses 0.

**Does not show.** Any other host (NOT_MEASURED). That an optimizer cannot fold the bit-level NaN test: LLVM folded a
float-level one at -O (the Rust author measured it); this is a managed hazard. Floats inside identity are a fork from the
lineage, for the owner to rule on.

### T6. The door: repair what the grammar reads identically; never move a literal; refuse the rest

- **Repairs** (court L12 FATAL, L13; red team E9, E17, E19, E26; the second round, SPEC §13):
  - The door re-segments every repaired line and refuses QUOTE-BOUNDARY if any literal boundary moved. `“a”"b"` had
    become one literal printing `a"b`. (Edition 2 gave `"a”"b"` as the example; since E9 a curly quote inside a
    straight-quoted literal is text, so only a curly-opened literal can reach the case.)
  - A literal opened by a straight quote closes only at a straight quote (E9: `"Use “followed by” to join"` had lost
    its middle words).
  - Code is no longer NFC-normalized: a Kelvin sign had become `K`, and a Greek question mark `;`. It is refused
    NON-ASCII-CODE.
  - Format characters, Hangul fillers and line separators inside literals and free text are refused (E19).
  - The door's events say only what happened: no LITERAL-NOT-NFC note on a line with no literal (E26), and no
    QUOTE-BOUNDARY on a line already refused, whose refused characters had made its literals differ with no quote
    involved (found settling §13).
  - The door repairs code and free text, and never literal contents.
- **Evidence.** MEASURED here: idempotence on texts that needed repairs (edition 1's row had tested only texts that
  needed none); the QUOTE-BOUNDARY row, for a straight and a curly next quote, and its plant; rows for E9, E19 and
  E26; the red team's door fuzz rerun after the last change: 0 counterexamples in 60,000 lines (seed 5).
- **Does not show.** That each repair rule preserves meaning (DECLARED rule by rule). That the door is a retraction in
  general (DECLARED).

### T7. Physics as properties of the update (Levesque & Verlet 1993; Newton's third law)

- **Corrected** (court L14). Momentum is conserved because each impulse is applied as +J and −J in exact arithmetic:
  Newton's third law, written into the code. It is not Noether's theorem.
- **Both guards accept any position-dependent pairwise force**, including non-physical ones (D10). Reversibility and
  conservation are properties of the update, not of the physics.
- **Evidence.** MEASURED here:
  - exact return after 1000 steps forward and 1000 back;
  - the momentum guard held on all steps;
  - the plant `law-leapfrog-asymmetric-drift` breaks exact return and is caught.

### T8. Prose as a lossless spelling of a typed law

- **Narrowed** (court L15).
  - "Impossible by construction" is DECLARED; the twin and the arbiter hold it.
  - Losslessness is measured on one program: three spellings, one law-seal.
  - The law includes identifier names (variables, rules, procedures), so renaming changes the law-seal.
- **Prior art** (N19, N20): ALGOL 60's reference, publication and hardware representations; Catala's
  language-dependent keywords; Dhall's semantic hashes; Unison's content-addressed definitions.
- **Evidence.** MEASURED here: three spellings, three text-seals, one law-seal. A clean-room twin written from the
  spec alone matches the reference on all 23 programs after one ambiguity (#37) was settled (§10).

### T9. Chaos magnifies a recurring difference; traces localize a single one

- **Corrected** (court L16, FATAL). A single one-ulp perturbation of the Chebyshev orbit is erased by rounding about a
  quarter of the time: 1526 of 6000 perturbations (MEASURED by the prosecution; reproduced here in kind). Erasure is
  most likely where |x| < 1, which locally contracts.
  - An FMA difference, repeated at every step, still escapes erasure: the measured divergence stands.
  - The explicit-fma plant is localized at its first fused operation by the trace.
- **Prior art.** Rosinski & Williamson 1997.

### T10. One code for each refused text (SPEC §11 G3, completed in §13 and §14)

- **The theorem under discussion.** For every text, the compile result (acceptance, or exactly one refusal code) is a
  function of the text alone. It is fixed by the specification, not by how an implementation happens to walk the
  text.
- **Mechanism.**
  - Eight phases in a total order, with every code in exactly one (SPEC §13's table). A self-test row holds the
    table to the codes the source can raise, and a plant shows the row bites.
  - An order within each phase. Within a statement, written order, post-order (§13). §14 sharpens it: which checks
    belong to a part, a loop's place first, and the nesting count and the statement's tree each defined once.
- **Evidence.** MEASURED here (`evidence/`):
  - the clean-room twin's hand-worked probes are all met: 163 from its second round and 128 from its third, five of
    them as settled against the twin, each with its reason;
  - differential runs against the round-3 twin: 0 disagreements on 20,221 mutants (seed 1). With the third round's
    probes as seeds, every disagreement is one of the three readings §14 settled against the twin (seed 2);
  - a row of 15 two-fault texts for the order within a statement, and its plant.
- **Does not show.**
  - That the reference parser is a predictive reader of §4 (DECLARED, §13).
  - That the twin and the reference differ nowhere beyond the five settled readings: the runs sample texts, they do
    not enumerate them.
  - Truth: two readers from one model family agreeing is consistency.

---

## 2. The lineage this inherits (each item also has prior art outside the lineage: N25)

**executable-epistemics → Semiotic core → Dentatus → Ursprung → Urðr → Verðandi → Ørlǫg.**

| ancestor | what Ørlǫg takes from it |
|---|---|
| executable-epistemics | The five-field artifact. The verdict firewall (a selftest row). Mandatory failure conditions. Observer families. |
| Semiotic core | GEN-004 (tamper evidence, never truth). GEN-005 (a selector is imported policy: the ledger). GEN-008 (categorical DPI). Law 12. TRIAGE's verdicts. |
| Dentatus | The `!=` spine and the cardinal rules, e.g. "a benchmark that cannot fail is decoration". |
| Ursprung | The provenance principle. Twin goldens. BRIP. Proof-carrying production reverses the throughput asymmetry. |
| Urðr | Epistemic typing. LCF evidence. Q32.32 physics. Fuel. Placements. Glyph laws (lossless, earned, `signum ≠ rēs`). Lessons L15, L16, L19, L23, L28, L56–58, L61, L75. |
| Verðandi | Integrity ≠ truth. Literal targets against shared mistakes (G23, HERMENEUTICS-0). Owner acts. A new language needs registration. An intent never carries code. |

## 3. Binding verdicts honoured

TRIAGE's DECORATIVE and FALSIFIED rulings stand:
- the Aztec diamond appears only as an oracle source;
- no tautological guards;
- standing is non-factive;
- free natural language is refused: the grammar is closed;
- refusals cannot be caught;
- counts are derived.

## 4. Falsifier inheritance (lineage failure → built-in rule), extended by the court

The edition-1 rows stand, with these added:

| failure (where found) | rule now |
|---|---|
| a name-keyed ratification grounds unrelated claims (L4, L8) | grounding binds to the claim's own seal |
| a guard plant that touches nothing (L5) | `court-grounds-computation` plant, with a row that sees it |
| an idempotence row over inputs that needed no repair (L13) | the row runs over repaired inputs, and requires a non-zero repair count |
| a closure certified over nothing (L10) | VACUOUS, never CLOSED |
| hidden children never checked or run (E3) | UNEXPECTED-CHILDREN for absorbed clauses too |
| host limits reached by deep nesting (E10) | constant-depth If chains; NESTING-DEPTH (24) and LOOP-NESTING (16), each with a row at its limit on all backends |
| silent overrides (E13, E15) | one seal line, and one oracle per claim |

## 5. Evidence, measured here

The self-test's summary line and every row are in `evidence/selftest-run.txt`, recorded in the repository by the last
run. Two consecutive runs gave byte-identical output (`evidence/selftest-run2.txt`), the second on the first's build
cache. `evidence/probes-run.txt` holds the comparison with the twin's hand-worked probes. (Before the move these files
lived in `build/evidence/`, where the dated court records still name them.)

Other evidence:
- **Vectors:** C99 20015/20015 and Rust 20015/20015, both re-run by me.
- **Corpus:** four-way identity on 11 programs, including chaos, physics, the falling body and the Aztec counts.
- **Twin:** 23/23 identical after #37.
- **Compiler determinism:** the compiler's output (law bytes and three sources) is identical under two hash seeds.

**Defects found and repaired**, by who found them:

| found by | defects |
|---|---|
| me | a self-performing procedure; my leapfrog draft; a typed count; a broken plant harness |
| both runtime authors | NaN docstring drift; LLVM NaN folding |
| the twin | 62 ambiguities, and the float-literal crash |
| the logic prosecution | the door's boundary merge; inline claims crashing the court; name-keyed grounding; vacuous closure; vacuous idempotence; the cost labels |
| the red team | an equality-promotion crash; hidden children; rules in procedures; nesting depth; NFC confusables in code; double seals and oracles; procedure collection |

## 6. Novelty, graded (adopting the novelty prosecution's consolidation, N1–N25)

**Not new.**
- **The court's mechanisms:**
  - the three standings are Fitting's Kripke–Kleene values for a Horn operator, and the undefined region is the
    well-founded semantics' unfounded loops (Van Gelder, Ross & Schlipf 1991; Brass et al. 2001; Brewka et al. 2013;
    Alfano et al. 2024);
  - lfp and gfp as well-founded and arbitrary support is textbook (Leroy & Grall 2009; Keiren & Cleaveland 2023);
  - Doyle's TMS (1979) refuses support that is only circular;
  - "sandwich closed" is exactness (Denecker, Marek & Truszczyński 2002).
- **No expressible trust in the checker:** LCF (Milner; Harrison 1995); Artemov-based calculi (Alt & Artemov 2001;
  Bonelli & Feller 2012); a specific proof escapes the Löbian obstacle (Yudkowsky & Herreshoff 2013).
- **Provenance and evidence:**
  - oracle anchoring as provenance (Canedo 2026);
  - per-theorem assumption tracking (Rocq, Lean, ACL2, Dafny, HOL4);
  - outside-signature evidence logged at run time (Aura 2008);
  - the nearest neighbour, **Lara** (He & Liu, arXiv 2609.25421, September 2026), a claims language with typed
    evidence, grounded standing, an untrusted prose binding, and byte-identical reports from two implementations.
- **Cost:** counted-step ratio bounds (Klemen et al. 2018, static); run-time check budgets by time (QVM 2008); Z3
  rlimit.
- **Backends:** one expected output per program across backends, with declared exceptions (Dafny); declared
  deviations (Scala.js).
- **Spellings and hashes:** one meaning in several spellings (ALGOL 60; Catala); meaning-level hashes (Dhall; Unison);
  numbers and hashes as words (Hoon; S/KEY; US 10,467,392).
- **Edition 1's list** (R2, R3) also stands: Catala and L4 for legal operators; ftfy; COMPUTE!'s 1983 per-line
  checksums; ISO 7064; Rosinski & Williamson; Wasm, JEP 306 and RFC 3514.

**Not found** (absence of evidence, not evidence of novelty; the queries are in prosecution-novelty §Q):
- identity of every run's output and receipt across Python, C99 and Rust, with a reference interpreter as authority
  and mismatch notes localized to the first divergent event;
- a general-purpose language runtime that grades its own run-time claims by channel;
- an assurance or trust tool reporting gfp ∖ lfp of support as circular support;
- run-time, per-input operation counting used to grade a certificate against the clause it certifies (and the court
  found this reading weak: §T3);
- a program's own seal written as words inside that program.

**What may be new** (SPECULATIVE until the owner rules): applications and the combination, not mechanisms.
1. The Kripke–Kleene / well-founded distinction applied to a program's own run-time claims, with a cycle witness, and
   VACUOUS where edition 1 said "closed".
2. LCF's discipline carried to run-time claims, with grounding bound to each claim's own seal.
3. Canedo's anchoring as a typing rule: zero external bits, never GROUNDED.
4. A closed prose grammar whose phrasings share one law-seal, compiled to Python, C99 and Rust, with receipts and
   event chains equal across them.
5. The combination, against its nearest neighbour Lara. Lara has no claims about the program's own computation
   evaluated at run time, no floats, no counted cost, no gfp ∖ lfp report, no three compiled hosts and no ledger
   outside the text.

**Withdrawn from edition 1:** "a syntactic answer to Löb's obstacle" (L3, N9); "enforces Blum's 'different' by
measurement" (L6, N14); the circular-support detector as a new mechanism (N1–N4).

## 7. The encodings the owner named

Unchanged from edition 1. Letter sums are replaced by a GF(2^8) totally anti-symmetric fold, an ISO 7064-family code
that catches accidents, not adversaries. Katapayadi became speakable seal words. Chronograms became runtime
self-reference (`this law's seal`). Polybius and stoicheia earned no place. Legal operators are adopted (Catala and L4
are prior art). The Aztec diamond is an oracle source only.

## 8. Non-claims (does_not_show), in one place

Edition 1's list stands, and the court adds:
- **Theorem ratifications are names.** They ground nothing by themselves, and nothing checks that a claim instantiates
  its theorem (L4, L8, L18). This is repaired so that grounding needs this claim's own seal, and that seal's ratifier
  must judge the instantiation.
- **Counted operations are a unit-cost model.** They are not time or work, and their ratio is not little-oh (L6).
- **The support graph is the author's declared premises.** Undeclared dependence is invisible (L10).
- **The language is bounded.** Clauses nest at most 24 deep, loops at most 16 within one body, expressions at most 24
  deep as SPEC §13 counts them, and lists hold at most 2^24 items. These bounds are deliberate, sized to the hosts'
  limits. §12 stated the expression bound one too generously; §13 states it as the code measures it.
- **Memory in the C backend (red team E21 and rt_c finding 8; repaired 2026-10-25).**
  - *Before.* A text made by `followed by`, and every list made or copied, stayed on the heap until the run ended,
    so the C backend's memory grew with every one it ever made. The red team measured 130, 370 and 691 MiB at
    N = 5, 20 and 40 rebuilds of a 16 MiB text, against 113 MiB for Python.
  - *The repair.* Every heap text and list now has one owner: a variable's slot, or the temp stack, which is
    released when each statement ends. No recursion and no text in a list mean one slot per variable suffices.
  - *Measured* (`evidence/e21-*.txt`, `rt_c/NOTES.md`):
    - the same text runs peak at 58 MiB;
    - a 2,000,000-item list stored 4 and 32 times peaks at 46 and 46 MiB, against 77 and 505 MiB before.
  - *The bound.* Live text is at most (text variables + the text temporaries along one chain of active statements
    + the builder) × 2^24 bytes, and lists likewise with × 8. The bound is DECLARED in general and MEASURED for
    these programs. It covers texts and lists, not the stack, the code or the host's allocator.
  - A run that still exhausts memory does not finish, and the arbiter reports the C backend as dissenting.
- **Which of two faults is reported.** SPEC §13 fixes it everywhere but in one place: within a statement, SYNTAX and
  the nesting part of EXPRESSION-DEPTH are met in the order of a left-to-right predictive reading of the grammar.
  That the reference parser is such a reader is DECLARED.
- **The twin, both runtimes, the prosecutors and I are one model family.** Our agreement is consistency. The twin's
  probes and the differential run find slips and readings the specification leaves open, never a misreading that
  every reader shares.

## 9. Forks for the owner (nothing decided here)

1. **Name.**
2. **Where it lives.** Recommended: a repository of its own, beside Verðandi, as each earlier step of the lineage
   is. Each system then keeps one authority (Verðandi's gate, Ørlǫg's self-test and court), and any coupling between
   them is an interface admitted on purpose (built is not adopted). The alternative is one off-gate patch to Verðandi
   under BATCH-0, with the admission record (ADMISSION.md). That needs a sheet for work already built, the owner's
   word on a C compiler as a new toolchain (AGENTS.md: no dependency without it), the rung classifier, and the
   landing check, and its 20,015-line vector file and court material would pass through the owner's host checks.
3. **Floats in identity.** This is a fork from the lineage.
4. **The court's thresholds and rules R1–R7.** Includes binding grounding to claim seals.
5. **The ledger:** where it lives, and how it is protected.
6. **The nesting bounds**, 24 and 16.
7. **The readings I settled in SPEC §13**, which the owner may overturn:
   - against the twin: LEX before SYNTAX within a clause, and the door's UNTERMINATED-TEXT;
   - within a statement: written order, post-order;
   - a call is any statement whose first word is not reserved;
   - one name never stands for a variable and a procedure, or a rule and a procedure.
8. **Next rungs**, each its own admission record:
   - big integers and rationals;
   - capability inputs;
   - Freivalds and Blum–Luby–Rubinfeld library certificates;
   - sheaf-style gluing across modules;
   - VERDANDI-DESIGN 0 emission through admission.

## 10. The court record

See `court/RECORD.md`, the judge's record `court/record.json`, and its computed verdict `court/VERDICT.txt`
(`python court/judge.py`: Dung's grounded semantics over the record as written).
