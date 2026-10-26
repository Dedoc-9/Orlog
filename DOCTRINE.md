# ØRLǪG: doctrine and design record, edition 2, revised (2026-10-25)

*Ørlǫg*, "primal law", is what the Norns laid down: *þær lǫg lǫgðu* (Völuspá 20). This is a working name, for the
owner to rule on.

**Status.** Research in its own repository, [github.com/Dedoc-9/Orlog](https://github.com/Dedoc-9/Orlog), under the
GNU AGPL v3 (moved there from a session scratch folder on 2026-10-25, the owner's choice of DOCTRINE §9 fork 2). It is
not admitted or registered anywhere, it has no Verðandi authority, and the Verðandi checkout is untouched.

**Edition 2.** It replaces edition 1 after an adversarial court:
- a logic prosecution: `court/prosecution-logic.md`, findings L1–L20, of which 4 were FATAL;
- a novelty prosecution: `court/prosecution-novelty.md`, findings N1–N25;
- an engineering red team: `court/redteam-eng/`, reproducers E1–E26;
- a clean-room twin written from SPEC.md and RUNTIME-SPEC.md, which imports the reference's `numeric_ref.py` and
  `seal.py` (so its agreement on numbers and seals is shared code): `twin/NOTES.md`, 62 ambiguities.

**Revised** the same day, after the twin's second and third rounds (SPEC §13, §14), the repair of E21, and a
foundations review run as a debate (`research/roadmap-debate/`): an architect, a use-case skeptic and a documentation
prosecutor, whose 57 findings are disposed of in its VERDICT.md. New here: T11 (what agreement measures, layer by
layer), T12 (where the ground ends) and §11 (hardening that pays twice).

Where edition 1 overclaimed, this edition says so in the stage concerned. §10 points to the court's record
(`court/RECORD.md`, the first court) and the red team's findings (`court/redteam-eng/FINDINGS.md`).

**Grades** follow AGENTS.md §6. "Here" means this Windows host, in this session, under clang 22.1.8, rustc 1.96.1 and
CPython 3.14.5. Counts are typed in this text, each beside the evidence file that records it. The self-test's summary
is the last line of `evidence/selftest-run.txt` (Urðr L16, L75).

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
- **A refused evaluation is not held (R8, 2026-10-26).** Before R8 the court counted only finished evaluations. A claim
  whose 17th evaluation refused inside its own condition read "true in 16 of 16 evaluations", WELL-FOUNDED and, with
  its seal ratified, GROUNDED, over a run REFUSED at that very claim. The doppler debate's adversary found this (DP-5);
  the judge reproduced it.
  - Every refusal names the clause whose statement is executing, a rule's refusal the clause that used the rule
    (SPEC §6, §7), and CLAIM-REFUTED is the only code that means "evaluated and false".
  - So a refusal at a claim's own clause with any other code is an evaluation that began and did not finish. The court
    names it ("REFUSED at evaluation n (CODE)"), and does not count the claim as held.
  - An inline claim shares its clause with an If's condition, and perhaps with another arm, so its refusal is withheld
    conservatively.
  - The court reads this from the receipt's status line, and no receipt changed: COMPAT-0 held.
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
- 20,015 vectors pass in two separately written runtimes (one model family), each at two optimization levels with
  byte-identical output (`evidence/rt_c-vectors-O2.txt`, `-O0.txt`, `evidence/rt_rs-vectors-O.txt`, `-O0.txt`);
- the vectors, every one generated by `numeric_ref.py`, agree with a second derivation that never imports it, with 113
  hand-worked cases and with two published SHA-256 digests; three planted mistakes that `numeric_ref.py` and its
  vectors would share are each caught (`evidence/vectors-independent.txt`, T11);
- the chaotic orbit, the physics and the falling body are byte-identical four ways;
- a naive C loop under `-ffp-contract=fast -march=native` diverges from its unfused build, while Ørlǫg's generated C
  for chaos.orl has 0 FMA instructions under the same flags (one program; the `fma` rows).

**Does not show.** Any other host (NOT_MEASURED). That an optimizer cannot fold the bit-level NaN test: LLVM folded a
float-level one at -O (the Rust author measured it); this is a managed hazard. That subnormals survive on every host:
no runtime checks that flush-to-zero is off; the vectors' subnormal cases would show it on a host where it is on, and
here it is off (MEASURED by those cases). Floats inside identity are a fork from the lineage, for the owner to rule on.

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
  needed none); the QUOTE-BOUNDARY row, for a straight and a curly next quote, and its plant; rows for E9, E18, E19
  and E26, E18's with a plant that turns the boundary check off and gets E18's double repair back; the red team's door
  fuzz rerun after the last change: 0 counterexamples in 60,000 lines (`evidence/doorfuzz-60000-5.txt`).
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
  specification, with the reference's arithmetic and seals imported, matched the reference on all 23 programs of its
  first round after one ambiguity (#37) was settled.

### T9. Chaos magnifies a recurring difference; traces localize a single one

- **Corrected** (court L16, FATAL). A single one-ulp perturbation of the Chebyshev orbit is erased by rounding about a
  quarter of the time: 1526 of 6000 perturbations (MEASURED by the prosecution, whose scripts were kept in a session
  scratch folder and not in this repository, so the figure cannot be rerun from this tree). Erasure is most likely
  where |x| < 1, which locally contracts. Since 2026-10-25 chaos.orl's own notes say so (prosecutor F1).
  - An FMA difference, repeated at every step, still escapes erasure: the measured divergence stands.
  - The explicit-fma plant is localized at its first fused operation by the trace.
- **Prior art.** Rosinski & Williamson 1997.

### T10. One code for each refused text (SPEC §11 G3, completed in §13 and §14)

- **The theorem under discussion.** For every text, the compile result (acceptance, or exactly one refusal code) is a
  function of the text alone. It is fixed by the specification, not by how an implementation happens to walk the
  text.
- **Mechanism.**
  - Eight phases in a total order, with every code in exactly one (SPEC §13's table), except INTERNAL, a defect rather
    than a verdict. A self-test row holds the table to the codes the source can raise, and a plant shows the row
    bites. The row holds the set of codes, not their phases or order.
  - An order within each phase. Within a statement, written order, post-order (§13). §14 sharpens it: which checks
    belong to a part, a loop's place first, and the nesting count and the statement's tree each defined once.
- **Evidence.** MEASURED here (`evidence/`):
  - the clean-room twin's hand-worked probes are all met: 163 from its second round and 128 from its third, five of
    them as settled against the twin, each with its reason;
  - differential runs against the round-3 twin: 0 disagreements on 20,221 programs, 221 seeds and 20,000 mutants
    (seed 1). With the round-3 probes and the E21 fixtures as seeds (20,353 programs), 47 of 48 disagreements are the
    three readings §14 settled against the twin, and the 48th timed out and, rerun without a limit, gave
    byte-identical receipts (seed 2; `evidence/difftwin-seed2-timeout.txt`). Today's `diff_twin.py` always adds those
    seeds, so seed 1's run cannot be reproduced with it;
  - a row of 15 two-fault texts for the order within a statement, and its plant.
- **Does not show.**
  - That the reference parser is a predictive reader of §4 (DECLARED, §13).
  - That the twin and the reference differ nowhere beyond the five settled readings: the runs sample texts, they do
    not enumerate them.
  - Truth: two readers from one model family agreeing is consistency.

### T11. What four-way agreement measures, layer by layer

Agreement measures what the agreeing executions do not share. A defect in a layer that several executions share moves
them all together, and their agreement then measures the sharing, not the correctness. Each row below is bound to the
evidence that records it. The plants are written as tests of this claim, not of the code: a row that expects a defect
to slip past every execution guards against anyone later reading four-way agreement as more than it is. A row that says
nothing checks a layer states an absence; no run can MEASURE an absence, so it is graded DECLARED.

| layer | shared by | a defect planted there | what can see it | grade and evidence |
|---|---|---|---|---|
| the front end: door, parser, type checker, law bytes (`canon.py`, `syntax.py`, `sema.py`, `front.py`) | all four executions | every `plus` read as `minus`: the four agree on the wrong output (NONE) | the clean-room twin, whose front end is its own: it differs from them and equals the unplanted reference. Also any claim whose certificate refuses the wrong result | MEASURED: the self-test row `independence (MONITORED NEGATIVE …)`, `evidence/selftest-run.txt`. A monitored negative: it passes while the defect slips past, and it must flip to expect detection the day the front end gains real diversity. It is not a failure to delete |
| lowering and the three generators (`lower.py`, `gen_py.py`, `gen_c.py`, `gen_rs.py`) | the three backends | one operation too many at every multiplication: the three agree with each other against the reference, REFERENCE-DISSENT; on collatz, 41 operations more, one per 3n+1 step | the reference, which walks the tree and never lowers (`lower.py:8`) | MEASURED: the row `independence: a defect planted in the shared lowering …`. The catch relocates trust to the reference rather than distributing it, so what checks the reference matters more, not less |
| arithmetic (`numeric_ref.py`; `rt_py.py`, `rt_c/`, `rt_rs/`) | one definition, written as separate code | — | the 20,015 vectors; but `numeric_ref.py` generated every one, so on their own they define the semantics rather than check it. Since this revision they are held to a second derivation that never imports it, to 113 hand-worked cases and to two published digests, and three planted mistakes that `numeric_ref.py` and its vectors would share are caught | MEASURED: `evidence/vectors-independent.txt`, `evidence/rt_*-vectors-*.txt`, the row `independence: the runtime vectors …`. The derivation is diversity of method, not of author |
| the comparison (`arbiter.py`) | everything | its own history: a lenient receipt comparison (E7); failed builds counted as dissents (prosecutor F2); false dissents when runs shared a work folder, a verdict that depended on ambient state outside its declared inputs, the defect class an open run's purity rule exists to remove | its own rows and plants: E7, E8, BUILD-FAILED, one run folder per arbitration and the race of 16 | MEASURED for each repair (`evidence/race-after.txt`: 3 × 48 concurrent arbitrations, all agreeing). Not diversified: DECLARED. Its other ambient inputs are the content-keyed build cache and the host's compilers, which the witness names |
| the specification, and the authors | everything | — | nothing in this repository. One model family wrote every part, from one SPEC.md | DECLARED, an absence. Knight & Leveson (1986) found independently developed versions failing together where a shared specification was misread: independent teams do not buy independence from the specification |

The twin is independent of the reference's code path, not of the specification or its author. It reads the same
SPEC.md, and it imports `numeric_ref.py` and `seal.py`. Its success shows code-path independence and nothing more.

### T12. Where the ground ends: a terminal, admissible ground

**The question.** If the intent is not in the text, what distinguishes a claim that bottoms out in an observation or an
axiom from one that bottoms out in nothing? Cycles are only one shape of ungroundedness.

**The court's answer is a second axis, grounding** (`court.py`):
- A claim's base for grounding: it held in an agreed run; it rests on a channel that can carry outside information
  (a certificate, a theorem or the owner, never computation or agreement: R2, R3); and a ledger line ratifies its own
  seal (its law statement, its claim id and its law seal).
- GROUNDED is the least fixed point over that base, so every claim in the declared support tree must itself be
  grounded.
- WELL-FOUNDED but UNGROUNDED is a finite, acyclic tree that bottoms out in the program's own computation or an
  unratified citation: "bottoms out in nothing", and the court says so. Every computation-only claim stays there,
  whoever signs it.

**Agrippa's trilemma.** A justification regresses forever, circles, or stops at a point it does not justify. The court
cannot regress, since claims are finite; it flags circles; and it makes the stop explicit and signed rather than
hidden. It can do no better than that.

**The trusted base is social.** A proof assistant trusts a small checker and nothing else (the de Bruijn criterion,
Barendregt & Wiedijk's name for it, 2005).
Ørlǫg inverts that on purpose: its terminal ground is a person's ratification, an attributable assertion bound to exact
bytes. The court checks the binding and the channel, never the judgment. That is coherent, but it means the
trustworthiness of Ørlǫg's ground is not auditable by reading code.

**Its limits, ranked** (the owner's ranking, 2026-10-25):
1. **Untyped terminals: the cheapest fix of high value.** A checked certificate is defeated by running a checker again;
   a cited theorem by a counterexample or a misattribution; a person's say-so by retraction or unreliability. The court
   flattens the three into one kind of ratification and throws away what it already knows. Typed terminals would turn
   GROUNDED into "grounded in a checkable certificate" or "grounded in testimony". SV-COMP's separate witness
   validators are the precedent (`research/ragnarok/RESEARCH.md`).
2. **No inference step: the most underrated.** Grounding never flows from ratified premises to a conclusion by a checked
   rule; each node needs its own ratification. A large grounded argument then needs N signatures rather than one
   ratified rule licensing its derivations, which scales socially into rubber-stamping and destroys the value of
   ratification. Moving ratification from nodes to rules is a design fork, and probably the one that decides whether
   the court is usable at scale.
3. **Only declared support is seen (L10): the one to worry about operationally.** With untyped terminals, the court can
   be satisfied by an omission: a claim with no declared support reads as a leaf even when its condition depends on
   unratified constants or rules. Until the backward slice lands, "GROUNDED" is a claim about the declared graph, not
   the real one. (The backward slice, Weiser 1981, is fork 4's proposal: `research/roadmap-debate/ARCHITECT.md`.)
4. **No observation channel.** Programs take no input, so an observation can enter only as someone's ratification. An
   open run would add input events, but an input event is still a value in a log chosen by whoever ran it: that gives
   replayable observations, not admissible ones. Unless input logs get the same ratification as every other channel,
   an open run would create the appearance of grounding in the world while grounding in whoever supplied the log.

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
| host limits reached by deep nesting (E10) | constant-depth If chains; NESTING-DEPTH (24) and LOOP-NESTING (16), each with a row at its limit on all backends (NESTING-DEPTH's added in this revision, prosecutor F17) |
| silent overrides (E13, E15) | one seal line, and one oracle per claim |
| an arbiter whose verdict read ambient files (foundations review) | one run folder per arbitration, removed after it; a race row of 16 at once |
| a run nothing bounds (foundations review) | a host budget of counted operations on the reference: STOPPED-BY-HOST, no receipt, never a refusal; a wall-clock backstop on the backends, labelled host-dependent |
| a ledger torn by a crash breaks every court reading (foundations review) | LEDGER-BROKEN at its line, read whole or not at all; a row and a plant |
| a claim whose evaluation refused, read as held and GROUNDED (the doppler debate's DP-5) | R8: the evaluation is named and the claim is not held; four fixtures, a plant that switches R8 off, and a one-sidedness measurement over COMPAT-0's frozen texts (`tests/court_monotone.py`) |
| a backend that did not build, counted as dissenting (prosecutor F2) | BUILD-FAILED, outside agreement and dissent; every claim's integrity INCOMPLETE; the sandwich VACUOUS |
| vectors that define the arithmetic and check nothing (foundations review) | a second derivation, hand-worked cases and published digests, with plants of mistakes the reference and its vectors would share (T11) |
| a later version that quietly changes what an old text means (the roadmap's first rung) | COMPAT-0: 3,361 texts frozen with their results at b4eaf11, law seal and receipt both, so a change that keeps every seal but alters a run is caught (its plant `say-counts-twice`) |

## 5. Evidence, measured here

The self-test's summary line and every row are in `evidence/selftest-run.txt`, recorded in the repository by the last
run. Two consecutive runs gave byte-identical output (`evidence/selftest-run2.txt`), the second on the first's build
cache. `evidence/probes-run.txt` holds the comparison with the twin's hand-worked probes. (Before the move these files
lived in `build/evidence/`, where the dated court records still name them.)

Other evidence:
- **Vectors:** C99 20015/20015 and Rust 20015/20015, each at two optimization levels with byte-identical output
  (`evidence/rt_c-vectors-O2.txt`, `-O0.txt`, `evidence/rt_rs-vectors-O.txt`, `-O0.txt`); the vectors held to a
  second derivation (`evidence/vectors-independent.txt`).
- **Corpus:** four-way identity on 11 programs, including chaos, physics, the falling body and the Aztec counts; their
  11 law seals are unchanged under the front ends of 83eb044 and fc19339 (`evidence/corpus-seals.txt`).
- **Twin:** round 1, 23/23 identical after #37; rounds 2 and 3, 291 hand-worked probes, all met, five of them as
  settled against the twin (`evidence/probes-run.txt`, `evidence/probes3-run.txt`).
- **Compiler determinism:** the compiler's output (law bytes and three sources) is identical under two hash seeds.
- **The arbiter's race:** 48 arbitrations at once in one work folder, three times, all agreeing, no run folder left
  (`evidence/race-after.txt`).

**Defects found and repaired**, by who found them:

| found by | defects |
|---|---|
| me | a self-performing procedure; my leapfrog draft; a typed count; a broken plant harness |
| both runtime authors | NaN docstring drift; LLVM NaN folding |
| the twin | 62 ambiguities, and the float-literal crash |
| the logic prosecution | the door's boundary merge; inline claims crashing the court; name-keyed grounding; vacuous closure; vacuous idempotence; the cost labels |
| the red team | an equality-promotion crash; hidden children; rules in procedures; nesting depth; NFC confusables in code; double seals and oracles; procedure collection; and from its report (E7–E26): a lenient receipt comparison, failed builds as dissents, curly quotes cutting a literal, a door that was not idempotent (E18), ratifying a clause that is not a claim (E22), the C backend's unbounded text and list memory (E21) |
| the twin's rounds 2 and 3 | readings the specification left open, settled in SPEC §13 and §14, with a code change where the reference was wrong |
| the foundations review | an arbiter reading ambient files; unbounded runs; a ledger torn by a crash; vectors that check nothing beyond their generator; 57 documentation findings (`research/roadmap-debate/PROSECUTOR.md`) |

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
- **R8 only withholds, and that is measured, not assumed.** Over COMPAT-0's 3,361 frozen texts it changes nothing:
  none refuses inside a claim's condition, which is a coverage gap, not a pass. Over its four fixtures it withholds 5
  standings and grants none. A plant that reverts R8 shows 5 standings gained, and is caught
  (`evidence/court-r8.txt`). A rule that withholds can be wrong only by withholding too much, and the inline case does.
  A rule that grants, such as R6's licence when it is built, needs its own soundness argument and rows that show what
  it grants. A count of what it grants is not enough.
- **COMPAT-0 holds the results of its frozen texts, and nothing else.** Every text version 0 accepted keeps its law
  bytes and its reference receipt: MEASURED on 3,361 texts, DECLARED for the rest. It sees no timing, no memory over a
  long run, no defect of the arbiter, no backend, no door event and no court reading, and it freezes what one commit
  did, defects included (`tests/compat/README.md`).
- **The language is bounded.** Clauses nest at most 24 deep, loops at most 16 within one body, expressions at most 24
  deep as SPEC §13 counts them, and lists hold at most 2^24 items. These bounds are deliberate, sized to the hosts'
  limits. §12 stated the expression bound one too generously; §13 states it as the code measures it.
- **Memory in the C backend (red team E21 and rt_c finding 8; repaired 2026-10-25).**
  - *Before.* A text made by `followed by`, and every list made or copied, stayed on the heap until the run ended,
    so the C backend's memory grew with every one it ever made. The red team measured 130, 370 and 691 MiB at
    N = 5, 20 and 40 rebuilds of a 16 MiB text, against 113 MiB for Python.
  - *The repair.* Every heap text and list now has one owner: a variable's slot, or the temp stack, which is
    released when each statement ends. No recursion and no text in a list mean one slot per variable suffices.
  - *Measured* on two programs (`evidence/e21-*.txt`, `rt_c/NOTES.md`):
    - the same text runs peak at 58 MiB;
    - a 2,000,000-item list stored 4 and 32 times peaks at 46 and 46 MiB, against 77 and 505 MiB before (the script,
      `tests/e21_list_leak.py`, is tracked from this revision; `evidence/e21-lists-rerun.txt` gives 46 and 46 again).
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
- **Four-way agreement does not test the front end** (T11). A defect in the door, the parser or the type checker
  moves all four executions together; the twin and grounded claims are what can see it.
- **"GROUNDED" is about the declared support graph** (T12, limit 3), and the ground itself is a person's act, not
  auditable by reading code.
- **A host stop is not a verdict.** STOPPED-BY-HOST says the host's budget ran out; the law said nothing, so there is
  no receipt and no refusal. The backends' stop is a wall clock and depends on the host.

## 9. Forks for the owner (nothing decided here, except where marked)

1. **Name.**
2. **Where it lives.** DECIDED by the owner, 2026-10-25: a repository of its own, beside Verðandi
   ([github.com/Dedoc-9/Orlog](https://github.com/Dedoc-9/Orlog)). Each system keeps one authority (Verðandi's gate,
   Ørlǫg's self-test and court), and any coupling between them is an interface admitted on purpose (built is not
   adopted).
3. **Floats in identity.** This is a fork from the lineage.
4. **The court's thresholds and rules R1–R7.** Includes binding grounding to claim seals.
5. **The ledger:** where it lives, and how it is protected.
6. **The nesting bounds**, 24 and 16.
7. **The readings I settled in SPEC §13 and §14**, which the owner may overturn:
   - against the twin: LEX before SYNTAX within a clause, and the door's UNTERMINATED-TEXT;
   - within a statement: written order, post-order;
   - a call is any statement whose first word is not reserved;
   - one name never stands for a variable and a procedure, or a rule and a procedure;
   - the three readings §14 settled against the twin's third round (items 6, 7 and 9).
8. **Next rungs**, each its own admission record:
   - big integers and rationals;
   - capability inputs;
   - Freivalds and Blum–Luby–Rubinfeld library certificates;
   - sheaf-style gluing across modules;
   - VERDANDI-DESIGN 0 emission through admission.
9. **Typed terminals and ratified rules** (T12, limits 1 and 2): whether a ratification names the kind of its ground
   (a checkable certificate, a cited theorem, testimony), and whether ratification may attach to a rule that licenses
   derivations rather than to each claim.

## 10. The court record

See `court/RECORD.md`, the judge's record `court/record.json`, and its computed verdict `court/VERDICT.txt`
(`python court/judge.py`: Dung's grounded semantics over the record as written). The record covers the first court;
the red team's report is `court/redteam-eng/FINDINGS.md`, and the foundations review's disposition is
`research/roadmap-debate/VERDICT.md`.

## 11. Hardening that pays twice

The owner's argument (2026-10-25): what makes a program hard to attack, that its state is a function of declared
inputs with defined semantics at every boundary, is also what makes a simulation reproducible across machines and
time. He named five measures that pay twice. Their state in this tree:

| measure | why it pays twice | state here |
|---|---|---|
| **Defined numerics:** a sealed dialect, its rounding, overflow and saturation specified, nothing left to the host's FPU | each FPU variation (contraction, x87 excess precision, flush-to-zero) is both a cross-host divergence and a "same program, different bytes" surface; bitwise reproducibility is what lockstep needs | the design already (T5): Q31.32 half-even, binary64 with one NaN, no contraction, no transcendentals, overflow refused rather than saturated. New: the vectors held to hand-written expectations, which only specified semantics allow (T11). Open: flush-to-zero is not checked (T5); a second host is NOT_MEASURED |
| **Total ordering everywhere** | iteration order is a classic nondeterminism and a timing channel; for contacts, pair order, manifolds and solver order decide whether equal starts stay equal | holds today because the language's only collection is the list, which is ordered, and the compiler's output is identical under two hash seeds. A rule for every future collection: its iteration order is defined and visible in the law (DECLARED) |
| **Bounded execution, failing closed** | an unbounded run is a denial of service and a physics overrun; "determinism of failure matters as much as determinism of success" | done in this revision for the reference: a budget of counted operations, the same stop on every run; the backends' stop is a wall clock (host-dependent, labelled); a torn ledger refuses at its line. Open: a per-tick budget written into the law, which needs an open run's tick, and whose overrun would be a refusal in the trace |
| **Event-sourced state with exact inverses** | the same machinery is an audit trail and tamper evidence, and is rollback netcode and replay: store inputs, rebuild any frame, find the first divergent tick between hosts | not built: snapshots (SNAP-1), a hash-linked ledger (LEDGER-1) and exact-inverse edits (EDIT-0) are the roadmap's; justified twice, they survive even if a use case does not |
| **Effect isolation** | a run writes only declared channels and touches only declared state; isolated transitions are race-free, so disjoint bodies can step concurrently with identical results | begun in the arbiter (one run folder per arbitration); a program already writes only its output and receipt and reads nothing. Declared input ports and state regions wait for the open run |

His caveats stand: four-way checking belongs at admission, and a live loop runs one backend; determinism gives
reproducibility, not stability, as chaos.orl shows (T9); and replayable inputs are not admissible ones (T12, limit 4).
Where this reorders the roadmap (a second host as the test that defines the numeric and ordering seals, bounded runs
first), the ranking is in `research/roadmap-debate/VERDICT.md`.
