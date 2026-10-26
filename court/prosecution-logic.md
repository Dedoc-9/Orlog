# Prosecution, logic: the ØRLǪG OL-0 design record (2026-10-25)

**Under trial.** `DOCTRINE.md` (sha256 `dfd4e372…`), read against `SPEC.md` (`bd9811c5…`), `src/orlog/court.py`
(`10b43063…`), `tests/selftest.py` (`575a166f…`), `src/orlog/canon.py` (`583bbfc0…`), `src/orlog/sema.py`
(`4353d7e4…`) and `src/orlog/interp.py` (`33e956cf…`), as they stood from 16:21 to 16:49 PDT. `court.py` and
`selftest.py` were last changed at 16:21, after DOCTRINE's last write (16:15); `examples/fall.orl` appeared at 16:20.
Other agents rewrote STATUS.md (16:18) and `orl.py` (16:21) and added ADMISSION.md (16:18) while this review ran.
Where the record and the code disagree, both are quoted.

**How the evidence was made.** MEASURED means run here by the prosecution, on this Windows host (CPython 3.14.5,
clang 22.1.8), with the record's own code, unmodified on disk. The scripts and their outputs are in
`C:\Users\DILLB_~1\AppData\Local\Temp\claude\C--Users-dillb-lzxy763-Desktop-Verdandi\c3c597f5-fd74-40a1-bfa3-a31b0538ea72\scratchpad\prosecution-logic-work\`
(`demo.py` → `demo-output.txt`, `demo_r7.py` → `r7-output.txt`, `fma_cause.py` → `fma-output.txt`,
`chaos_erasure.py` → `chaos-output.txt`, `chaos_merge.py` → `chaos-merge-output.txt`). The arbiter there is given
the python backend alone, so AGREED means the reference and the python backend agree, which court R1 accepts. Plants
are made on in-memory copies of the code. CODE means read in the code; SOURCE means a cited source (R1a, R1b, R3, or
a page named). Every demonstration program is printed below, so the defence can rerun it with `python orl.py court`.

**Severity.** FATAL: the stage's conclusion does not follow (or its own falsifier fires). OVERREACH: claims more than
the evidence. IMPRECISION: wording or attribution. SOUND: tried, and it held.

## At a glance

| id | section | severity | finding |
|---|---|---|---|
| L1 | §0 | IMPRECISION | Horns A and B cite theorems for what they do not say |
| L2 | T0, §0 | OVERREACH | Tarski, Rice and Gödel II have no instance in a closed, total language; "truth" is used in two senses |
| L3 | T1, §6.2 | FATAL | Artemov against Löb is a category error: Ørlǫg makes no reflection of either kind |
| L4 | T2, §6.3 | OVERREACH | the DPI gives "no ledger, no external bits", not "a ledger line grounds this claim"; theorem ratification is keyed by name alone |
| L5 | T2 | OVERREACH | T2's falsifier is not guarded; R3's "CORROBORATES" is a label nothing computes |
| L6 | T3, §6.4 | FATAL | T3's own falsifier fires: certificates that recompute read "cheap" |
| L7 | T3 | OVERREACH | RECOMPUTATION is denying the antecedent; R4 prints "Blum-Kannan's little-oh" |
| L8 | T3, §6.4 | OVERREACH | L28 is not enforced: a check that decides nothing is CERTIFIED and GROUNDED, and so is a wrong gcd |
| L9 | T4 | IMPRECISION | the sandwich statement holds for fixed points only; "its own cycle" is wrong |
| L10 | T4, §6.1 | OVERREACH | the "sandwich closed" certificate is issued by a backend bug and by emptiness; the detector is defeated by omission |
| L11 | T4 | IMPRECISION | Cousot's start hypothesis dropped; "tight" misattributed; the chaotic row tests a function no verdict uses |
| L12 | T6 | FATAL | the door turns a delimiter into literal content and records a false reason |
| L13 | T6 | OVERREACH | the retraction evidence exercised zero repairs; free text is repaired too |
| L14 | T7 | IMPRECISION | Noether is decoration: a non-conservative, translation-breaking force passes both guards |
| L15 | T8, §6.5 | IMPRECISION | "impossible by construction" is DECLARED; "lossless" is one program; the law holds names |
| L16 | T9 | FATAL | T9's own falsifier fires: 1526 of 6000 one-ulp perturbations leave every output unchanged |
| L17 | court R1–R7 | OVERREACH | claims written inline crash the court; R1 and R7 say one thing, the rows another |
| L18 | §8 | OVERREACH | the non-claims "in one place" omit what L4–L17 found |
| L19 | §5, T1, T7 | IMPRECISION | the self-test counts are prose numbers that deserted |
| L20 | §7 (outside the brief) | IMPRECISION | "Kleene-style … no fixed point"; "Damm's construction" |
| S1–S10 | several | SOUND | tried, and held (listed at the end) |

---

## L1. §0, Horns A and B — IMPRECISION

- **Löb.** "The robot's 'looks perfect' is Löb's theorem at work." Löb's theorem needs a theory whose provability
  predicate meets the derivability conditions (R1a §2). Its content is that a consistent theory cannot adopt the
  reflection schema wholesale. A clone that agrees with its maker is not a theory proving Prov(φ) → φ: its failure is
  shared evidence and correlated error, which the DPI, Aumann and Goel bullets of the same horn describe. The Löbian
  obstacle (R1a §3) concerns the opposite behaviour: a consistent reasoner cannot license its own kind.
- **Montague.** "A theory whose verdicts are factive (N⌜φ⌝ → φ) and which certifies its own theorems is
  inconsistent." The theorem (R1a, obscure result 1) needs the theory to extend Q, so that N applies by diagonalization
  to sentences about N, and to *prove* the schema N⌜φ⌝ → φ. Without self-application, factivity plus necessitation is
  consistent: the modal logic KT has the axiom □φ → φ and the necessitation rule, and it is sound on reflexive frames.
  Verdicts that merely *are* factive (a sound verifier) are consistent too. The dropped hypothesis is the one that
  carries the theorem.
- **Aumann.** Clones with one prior and one body of information agree without any theorem. Aumann's content is that
  agents with *different* private information cannot agree to disagree once their posteriors are common knowledge.
  Applied to the robot, it is decoration.
- **Condorcet and Ladha.** "Condorcet's jury theorem needs independence" is contradicted by the next clause: Ladha
  gives sufficient conditions under correlation (R1b §3, which records "the inequality NOT seen"). A sufficient
  condition is not a tolerance bound, and Kaniovski (R1b, obscure result 3) shows that pairwise correlation does not
  fix majority accuracy.
- **The DPI's headline.** "A verifier that shares the generator's priors adds nothing" is not the DPI's hypothesis. The
  DPI needs the verdict to be a function of the artefact, that is, no other route to the truth. A verifier with shared
  priors and its own observations can add information.
- **Horn B.** "Independent recomputation costs what generation cost": both citations (Knight & Leveson; Eckhardt & Lee)
  measure coincident failure, not cost. The horn is "a theorem or measured fact" only as a near-tautology (recomputing
  costs computing), which T3 then sets out to avoid.

**Correction.** Keep Löb as context for "wholesale self-trust is inconsistent"; restore Montague's hypotheses ("extends
Q; proves the factivity schema for a self-applicable N"); drop Aumann from the clone case or state its
private-information content; write "Ladha gives sufficient conditions under correlation"; headline the DPI as "a
verifier whose verdict is a function of the artefact"; restate Horn B as "independently written versions are not
independent (Knight & Leveson; Eckhardt & Lee)".

## L2. T0, and §0's impossibility frontier — OVERREACH

**Argument.** T0 says its mechanism follows from Tarski. Tarski's theorem needs a language that represents its own
syntax and proves the diagonal lemma (R1a §2). Ørlǫg's claims cannot quote claims. Its programs are closed, since SPEC
§3 has no input statement, and total, since every While carries a bound of at most 2^62 and recursion is refused
(SPEC §5). The theorem has no instance in the language. The same holds for §0's frontier: Rice's theorem concerns
partial computable functions, and every semantic property of a closed, total Ørlǫg program is decided by running it,
which is what the runtime does.

The record then uses "truth" in two senses. The truth of each claim's *formal condition* is computed: the runtime
evaluates it, refuses `CLAIM-REFUTED` on false, and the court prints "true in 1 of 1 evaluations" (MEASURED, every
panel in `demo-output.txt`). What is not computed is whether the condition expresses what the author meant. That is
not Tarski's object-language truth; it is the oracle problem (Barr et al. 2015, R1b §12), because the intent is not in
the bytes. Likewise "integrity is definable inside" is false of the language: no program can compare receipts, and
the arbiter, written in Python, does. It is true of the toolchain, where formal truth is computed as well.

Montague is misapplied in "named non-factive: GROUNDED does not mean true (Montague)". Standing is computed outside
the language and no claim can mention it, so no self-applicable N exists. A factive GROUNDED would not be
inconsistent; it would be false, because a ledger line can be forged (§8) and a theorem name is not bound to its claim
(L4, L8). Calling standing non-factive is right; the reason given is not.

**Correction.** "Ørlǫg computes the truth of every claim's formal condition in the run. It cannot compute whether the
condition says what the author meant, because the intent is not in the text (the oracle problem). Tarski, Rice and
Gödel II are context: they have no instance in a closed, total language whose claims cannot refer to claims. Standing
is non-factive because its inputs (the author's premises and channel labels, and the ledger) can be wrong."

## L3. T1, and §6 item 2 — FATAL

**Argument.** T1 says its mechanism follows from Artemov: for each explicit proof p, T ⊢ Proof(p, ⌜φ⌝) → φ, while T
does not prove Prov_T(⌜φ⌝) → φ. Both are statements about a formal theory with a proof predicate; the first holds
because T is Σ1-complete and proof-checking is decidable. Ørlǫg has no theory, no proof predicate and no provability
predicate, so Löb's theorem has no instance for it to answer.

The mechanism exhibits neither side of Artemov's distinction. If "trust" is read factively, the court trusts the
runtime wholesale. Its base(c) is the runtime's own evaluation (`held = r["evals"] > 0 and r["trues"] == r["evals"]
and row["integrity"] == "AGREED"`, court.py:184), for every claim of every channel. The only discount is agreement
among implementations that §8 itself grades as one model family's consistency. If "trust" is read non-factively, as
the record insists (GROUNDED is not true), then nothing is trusted per certificate either, and no reflection is made,
explicit or implicit. Nor is "per-certificate reflection" expressible. `by the certificate of §k` attaches to any
Boolean condition: `g is positive` is accepted as the Bezout certificate and GROUNDED (L8, D2). No construct or rule
states "if the check passes, §k's result is right". The step from check to correctness is McConnell et al.'s
characterization, imported by name. That is a theorem about gcd, not a reflection principle.

T1's evidence (12/724 operations; the characterization) supports certifying algorithms, which stand without Artemov.

**Correction.** Rebase T1 on certifying algorithms (McConnell, Mehlhorn, Näher & Schweitzer 2011) and Blum's checkers.
State Artemov and Löb as motivation, by analogy. Withdraw §6 item 2 ("a syntactic answer to Löb's obstacle"): a
language without a provability predicate does not answer Löb; it lies outside Löb's hypotheses.

## L4. T2, and §6 item 3 — OVERREACH

**Argument.** The DPI is a necessity bound. Without a channel to the truth that bypasses the artefact, the verdict
carries no more truth than the artefact (R1b §1). It does not say that a new channel carries bits about the claim: a
channel independent of the claim adds nothing. The court turns necessity into sufficiency, because a ledger line makes
a held claim GROUNDED. For the theorem channel the line is keyed by the name alone (`ratified_theorems = {e["name"]: e
…}`, court.py:158, read at :193 and :210), not by the law-seal or the claim's law line. The owner channel, by
contrast, is bound (`claim_seal`, :185–191). One theorem ratification therefore grounds every claim, in every program,
that quotes the string.

**D3 (MEASURED).**
```
§1 Let plan be 7.
§2 We claim that plan is odd, by the theorem "the multiplication table: 7 times 7 is 49".
```
With the self-test's own fixture ledger the row reads "theorem ratified, ledger line 1", GROUNDED.

The DPI is also used in two senses. For a closed program, the formal truth X of a computational claim is a function of
the text Y, so I(X; Y) = H(X), and "computation adds no external bits" is true and empty. Yet the court grants computed
claims WELL-FOUNDED: computation does add support, of an epistemic kind the Shannon bound cannot see. And runs do carry
bits from outside the author (other authors' runtimes, two compilers, the hardware): R1 reads exactly those. What
computation cannot add is bits about the author's intent. Nothing in the court measures those bits, the ledger
included.

**Correction.** R2's gloss: "carries no bits about the author's intent beyond the text". R5 for theorems: "GROUNDED
means it cites a theorem name that a ledger line ratifies; the court does not check that the claim instantiates the
theorem", or else bind theorem ratifications to (law-seal, claim law line) as the owner's are. §6 item 3: "external
bits" is read from the author's channel label and the ledger, and those bits concern the cited name, not the claim.

## L5. T2's falsifier guard, and R3 — OVERREACH

**Argument.** T2 says: "Falsifier. Any path to GROUNDED without a ledger line. The court-accepts-gfp plant and the
grounding rows guard this." The gfp plant swaps lfp for gfp, but grounding still requires `ext`, which only a ledger
line sets (CODE: court.py:222 and :227). The plant therefore never touches this falsifier. The grounding rows cannot see
a breach of R2 either: the only computation claims in the court fixtures are Plankton's three, and their cycle keeps
them ungrounded whatever R2 says.

**D4 (MEASURED).** Plant `ext = (o[0] == "computation")` (computation claims ground with no ledger) into an in-memory
copy of court.py and replay the seven self-test rows that read the panel (the chaotic and Dung rows do not). All seven
pass: Plankton CIRCULAR and open; its cycle named;
§6 UNGROUNDED; §6 GROUNDED with the circle not; gcd cheap and UNGROUNDED; gcd GROUNDED with its fixture; the costly
row. The plant is not an equivalent mutant (D4b): `§1 Let a be 2.` / `§2 We claim that a equals 2.` reads UNGROUNDED
honestly and GROUNDED under the plant, with `ledger_entries 0`. That is a path to GROUNDED without a ledger line,
equivalent only in the fixtures' state, as AGENTS.md §6 warns.

R3 ("two clauses computing one value by different methods CORROBORATE") is a label. sema checks only that the two
clauses come earlier (sema.py:192–196). The condition need not mention them, no code emits CORROBORATES, and no
example, twin input or self-test row contains `by agreement`.

**D11 (MEASURED).** `§1 Let a be 1.` / `§2 Let b be 2.` / `§3 We claim that true, by agreement of §1 and §2.` reads
WELL-FOUNDED, with external bits "two of the author's representations".

**Correction.** Add a well-founded computation claim and an agreement claim to the court fixture, with the plant
above as a row. Either implement R3 (the condition must compare §a's and §b's values) or restate the table row as "a
label the author writes, treated as computation".

## L6. T3, and §6 item 4 — FATAL

**Argument.** T3's falsifier is "A certificate that recomputes and is read as cheap. Guarded by its row." It fires.

**D1 (MEASURED).** An integer square root by binary search, certified by recomputing the integer square root:
```
§1 Let n be 1000000007.
§2 Let lo be 0.
§3 Let hi be n.
§4 While lo is less than hi, at most 100 times, do the following.
§4.1 Let mid be the quotient of lo plus hi plus 1 by 2.
§4.2 If mid times mid is at most n, set lo to mid; otherwise set hi to mid minus 1.
§5 Say lo.
§6 We claim that lo equals the square root of n, by the certificate of §4.
```
The court reads "check 2 ops / certified clause 326 ops", "cheap (at most 1/2, this input)", certified true.

**D1b (MEASURED).** The check reruns the very operation the clause runs:
```
§1 Let n be 1000000007.
§2 Let r be 0.
§3 For each i from 1 to 40, do the following.
§3.1 Set r to the square root of n.
§4 We claim that r equals the square root of n, by the certificate of §3.
```
The court reads "check 2 ops / certified clause 121 ops", cheap, certified true.

**Why.** Blum's rule compares the checker with the fastest known program for the task (R1b §4: "T the least possible
(informally, least known) time for f"; R3 F3: "below that of any correct program"). The court compares it with this
clause's own cost on one input. That cost is counted in a unit-cost model, in which one operation can hide unbounded
work: an integer or fixed square root, a text comparison, an exact decimal print inside `followed by`, and
`a list of N copies of x` (up to 2^24 items) each count at most 1 (SPEC §7). Ørlǫg's domains are also bounded (i64;
lists of at most 2^24), so o(T(n)) as n → ∞ has no meaning in the language at all: "one input was measured" understates
the gap. "Cheap" shows only "fewer counted operations than this clause, here", and a recomputation of the task, by a
built-in or by repetition, meets that.

**Correction.** Drop "forces different", and drop §6 item 4's "enforces Blum's 'different' by measurement". Call the
reading "the check costs at most half this clause's counted operations at this input". Say that counted operations are
not time, and that difference must be argued from the check's characterization, never read off the ratio.

## L7. T3's RECOMPUTATION label, and R4's attribution — OVERREACH

**Argument.** Blum's rule runs one way: o(T) implies the checker cannot be a recomputation, and DOCTRINE states it so.
The court reads the converse: a ratio above ½ is labelled "RECOMPUTATION (little-oh not shown)" (court.py:199). That is
denying the antecedent. The self-test's own row shows it. `§2 We claim that a times a times a plus a equals 130 and a
is odd, by the certificate of §1` certifies `§1 Let a be 5`; the check recomputes nothing, yet it reads RECOMPUTATION
("check 6 ops / certified clause 1 ops", `build/evidence/selftest-run.txt`).

**D8 (MEASURED).** A check of a clause that never ran:
```
§1 Let a be 1.
§2 If a equals 2, do the following.
§2.1 Let b be a times 1000.
§3 We claim that a equals 1, by the certificate of §2.1.
```
The court reads "check 1 ops / certified clause 0 ops", RECOMPUTATION.

The inversion matches a lineage paraphrase the court seems to implement. The STATUS.md read at the start of this
review (6493 bytes, written at 14:06, then rewritten at 16:18 without the line) said that the little-oh rule "is
necessary for independence, never sufficient for standing". Wasserman and Blum say no such thing: they give a
sufficient condition for difference and call independence of errors a "heuristic contention" (R1b §4). The argument
above does not depend on that paraphrase. Urðr's L28 itself is not in this folder, so I have not checked its wording.

R4, printed into every court artifact, cites "Blum-Kannan's little-oh". R1b lists exactly this as a misattribution
trap, and DOCTRINE T3 itself credits Blum 1988 and Wasserman & Blum 1997.

**Correction.** Label the reading "NOT CHEAPER (ratio above ½ at this input)", and "CLAUSE NOT RUN" when the certified
clause never ran. In R4, write "Blum 1988 (Wasserman & Blum 1997)". Do not write "necessary" in any paraphrase of the
little-oh rule.

## L8. T3's L28 bound, and §6 item 4 — OVERREACH

**Argument.** T3 says: "It is GROUNDED only if its determinacy theorem is ratified, because cheapness without a
determinacy proof is 'affordability wearing the costume of a decision' (Urðr L28)." Two parts of the mechanism make
that bound decorative.

1. "No declared plant survived" is vacuous. No caller passes `plants`: `selftest.py` and `orl.py:87` call `panel`
   without it. Every measured certificate reads "plants: none declared" and is CERTIFIED on cost alone
   (`build/evidence/court-gcd_certificate.json`: `"certified": true`, `"plants": "none declared"`). The branch that
   would read plants prints "caught %d of %d" with the caught count twice (court.py:206–207); it has never run.
2. The determinacy theorem is matched by name and never bound to the check.

**D2 (MEASURED).** In `examples/gcd_certificate.orl`, replace §12 with
`§12 We claim that g is positive, by the certificate of §9 under the theorem "Bezout characterization: a positive common divisor of a and b that is an integer combination of a and b is their greatest common divisor".`
With a fixture ledger ratifying that name, the court reads "check 1 ops / certified clause 724 ops", cheap, certified
true, "determinacy theorem ratified, ledger line 1", GROUNDED. Add the self-test's own plant (`§10 Let g be old_r times
2.`): the program prints "gcd: 2, Bezout coefficients 24157817 and -39088169", and §12 is still GROUNDED.

A one-operation check that decides nothing, under a theorem about a different predicate, is exactly what L28 forbids,
and the court grounds it. The T2 table's "by the certificate of §k: cheap and characterizing" is likewise unchecked.
T2's own does-not-show ("Nor that a cited theorem says what the claim uses it for") concedes the gap. Having conceded
it, the record cannot claim in T3 and §6 item 4 that the cost reading is "bounded by L28's determinacy requirement".

**Correction.** Either bind a determinacy theorem to the exact check (for example, ratify the pair of theorem and claim
law line), or restate it: "GROUNDED requires a ratified theorem name; whether the check is the one the theorem
characterizes is not checked, so L28 is not enforced". Wire the law plants into `plants`, or drop the plant clause from
R4.

## L9. T4's statements — IMPRECISION

**Argument.** T4 says: "When lfp = gfp … every self-consistent assignment of trust between 'trust nothing' and 'trust
everything' gives the same standing." Every subset lies between ∅ and the universe, so the qualifier says nothing.

- If "self-consistent" means a fixed point of G, the statement is true: Knaster–Tarski puts every fixed point between
  lfp and gfp, so there is only one.
- If it means X ⊆ G(X) ("trust nothing whose premises you do not trust", the usual reading of consistent trust), it is
  false. ∅ is always such a set (∅ ⊆ G(∅)), and it differs from lfp whenever lfp is non-empty.
- The docstring's version ("reaches the same standing", court.py:10) is a different statement, and also true for the
  operator court.py computes. Iterating G from any start X gives G^n(∅) ⊆ G^n(X) ⊆ G^n(U), so every run converges to lfp
  when lfp = gfp. That rests on monotonicity and finite height (the deterministic analogue of Propp–Wilson), not on
  Knaster–Tarski alone.

T4 (and R6, printed into every artifact) also says: "gfp ∖ lfp is CIRCULAR: claims supported only by their own cycle".
For this operator that is wrong. gfp ∖ lfp is the set of held claims whose declared support is all held, with some
support chain reaching a cycle.

**D6 (MEASURED).** Plankton plus `§7 We claim that robot is odd, by computation, given §3.`: §7 lies on no cycle and
reads CIRCULAR. The current court.py now says so itself (`"cycle": "(depends on a cycle)"`, `find_cycle`,
court.py:84–97), contradicting the R6 printed in the same artifact. The module docstring's "exactly the set of claims
supported only by each other" is wrong in the same way.

**Correction.** "When lfp = gfp, G has exactly one fixed point, and iteration from any assignment reaches it." In R6
and DOCTRINE: "CIRCULAR: held, with all declared support held, and some support chain reaching a cycle (on one, or
resting on one)."

## L10. T4's certificate, and §6 item 1 — OVERREACH

**Argument.** §6 item 1 sells "the Plankton detector. Self-certification reported as gfp ∖ lfp …, with the 'sandwich
closed' certificate when lfp = gfp". The certificate is issued in exactly the states it should not certify.

**D5 (MEASURED).** A Plankton cycle:
```
§1 Let plan be the quotient of -7 by -2.
§2 Let robot be 4.
§3 We claim that plan equals robot, by computation, given §4.
§4 We claim that robot equals 4, by computation, given §5.
§5 We claim that plan is positive, by computation, given §3.
```
With an honest backend it reads CIRCULAR three times, sandwich open. Plant the self-test's python-quotient-floors
defect into the backend and the run becomes BACKEND-DISSENT: every claim CONTESTED and UNSUPPORTED, and
`sandwich_closed: true`. A wrong backend closes the sandwich. It is also closed with no claims at all (D5b), with no
backend (Plankton, reference only: REFERENCE-ONLY, UNSUPPORTED ×4, closed; `r7-output.txt`), and when claims are
unreached (the R7 demonstration, closed). Here lfp = gfp = ∅: the closure is vacuous, the vacuity that §4 of the record
itself warns against (Urðr L19, L61).

The detector also sees only declared premises.

**D7 (MEASURED).** Delete Plankton's three `given` clauses, and all four claims read WELL-FOUNDED, sandwich closed.
The robot in the parable declares nothing; its failure is undeclared shared priors, which no support graph contains.
The analogy is inverted as well: each of Plankton's three claims is checked by computation and is true in every
execution, and the court downgrades them because the author honestly declared a cycle.

**Correction.** Report `sandwich_closed` only when lfp is non-empty and integrity is AGREED, and "VACUOUS" otherwise.
Restate §6 item 1 as "declared circular support is reported as gfp ∖ lfp; undeclared dependence is invisible to it".

## L11. T4's citations — IMPRECISION

- **Cousot (R.R. 88).** The record omits the start condition (⊥, or any D ≤ F(D)) that R1a states, and that R1a lists
  as a trap: "Schedule-independence needs monotonicity and a start below the least fixed point."
- **Fages.** The record says "Erdem & Lifschitz (2003) named this 'tight'". Babovich, Erdem & Lifschitz (2000, arXiv
  cs/0003042, introduction) already write "'positive-order-consistency,' also called 'tightness'", and credit the name
  to Lifschitz 1996 (SOURCE, fetched this session). R1a says only "now called 'tight'".
- **Decoration.** The court computes each verdict by one deterministic Kleene schedule (court.py:42–57). `chaotic_lfp`,
  the function the 200-schedule row tests, is used by no verdict. For a definite operator, the fact the record needs
  is elementary (an acyclic held support graph has one fixed point); Fages's theorem, about normal programs with
  negation, adds nothing to it.

**Correction.** Restore Cousot's hypothesis. Write that the name "tight" dates from Lifschitz 1996, with extensions by
Babovich, Erdem & Lifschitz 2000 and Erdem & Lifschitz 2003. Grade the chaotic row as a test of `chaotic_lfp`, not of
the court.

## L12. T6 — FATAL

**Argument.** T6 says the door "repairs only what the grammar interprets". canon.py says: "REPAIR: the bytes are
changed; the rule names why the change cannot alter meaning", and "preserve what the program outputs, refuse what
neither can vouch for".

**D13 (MEASURED).** The raw line is `§1 Say "a”"b".`: U+201D followed by a straight quote.

1. The door's own segmentation (`_segments` in canon.py, where a curly double quote closes a literal) reads two
   literals, `a` and `b`.
2. It records one REPAIR, R-QUOTE-DELIM at column 10: "U+201D RIGHT DOUBLE QUOTATION MARK delimits a text literal;
   the grammar reads it as \"".
3. The canonical text is `§1 Say "a""b".` The grammar reads this as one literal containing an escaped quote, and the
   run prints `a"b`.
4. The same two literals written with straight quotes (`§1 Say "a" "b".`) are refused SYNTAX.

The repair turned a delimiter into output text, and a program the grammar refuses into one it accepts, and its
recorded reason is false of the canonical text. The second pass changes nothing, so idempotence holds here; what fails
is the second half of T6's title.

**Correction.** Refuse a repaired delimiter that is adjacent to a straight quote, or re-segment the canonical text
and refuse whenever the literal boundaries moved. Add the case as a door row with a plant.

## L13. T6's evidence — OVERREACH

**Argument.** The idempotence row's corpus needed no repair. D12 (MEASURED) counts the first-pass repairs over the 11
corpus files: 0. The row therefore shows that canonical text passes through, the trivial half of a retraction. It
never applies the door twice to a text that needed repairing. The universal claim "the door is a retraction" is
DECLARED (no termination or confluence argument is given; STATUS's Newman's lemma was dropped) and measured only on
canonical input.

"Repairs only what the grammar interprets" is also contradicted by the door's own row "non-NFC free text repaired to
NFC", and by R-SPACE in free text (canon.py:174–179 and :204–215). Notes and Titles are not part of the law.

**Correction.** Run the idempotence check over the outputs of the door rows and of the mangled spelling (and over a
generated fuzz). Grade "retraction" DECLARED. Write "repairs code and free text; never literal contents".

## L14. T7 — IMPRECISION

**Argument.** Momentum is conserved because each impulse is computed once and applied as +J and −J in exact
arithmetic: Newton's third law, written into the code. R3 §C derives exactly this, marked [D], without Noether.
Noether's theorem (a continuous symmetry of an action yields a conserved quantity) plays no part.

**D10 (MEASURED).** In `leapfrog.orl`, change §9.2.1 to `Let stretch be item (i plus 1) of x minus rest.` The force now
depends on an absolute position, so translation symmetry is gone, and its Jacobian is not symmetric, so there is no
potential and no action at all. The run completes. The momentum guard holds on all 2000 steps, and the state returns
exactly (`after reversal: x = [0.0, 1.0, 2.5], v = [0.25, -0.5, 0.125]`), although the positions reach ±20 on the way
(`after 1000 steps: x = [-19.09…, 20.10…, 0.538…]`).

Both "physics oracles" accept unphysical dynamics: they test how the update is built, not physics. The record's
does-not-show admits that the model may be physically inaccurate, but not that the guards cannot tell a non-physical
force from a physical one.

**Correction.** Write "Newton's third law, as a pairwise antisymmetric update (not Noether)", and "reversibility and
conservation are properties of the update; they accept any position-dependent pairwise force".

## L15. T8, and §6 item 5 — IMPRECISION

**Argument.** "Two spellings with one law-seal and different behaviour (impossible by construction)" depends on
`law_bytes` covering every field the lowering reads. That is argued, not proven. I checked by reading that the backends
read no label or text field, but nothing checks it mechanically. Grade it DECLARED.

"Lossless" is measured in one direction on one program (three spellings, one seal), so §6 item 5's "measured lossless
spelling" overstates.

DOCTRINE says the law holds "resolved types, values and ids", and SPEC §9 says "variable ids and clause ids". But
`law_stmt` also writes variable names (`(let %d %s …)`, sema.py:503) and rule and procedure names (:475, :521, :539).
Renaming a variable therefore changes the law-seal. That is harmless for T8's list of spellings, but the description
is wrong.

**Correction.** "Impossible by construction (DECLARED; held by the twin and the arbiter)"; "lossless (one program
measured)"; SPEC §9 and T8 should name the identifiers the law holds.

## L16. T9 — FATAL

**Argument.** T9 says: "Comparing outputs alone therefore detects a one-ulp difference anywhere in the first steps".
`chaos.orl`'s note says: "A one-ulp difference in any single operation of any backend reaches the whole value within
about 60 steps". The falsifier is "A divergence present in the traces but absent from the outputs". It fires.

**MEASURED** (`chaos_erasure.py`). The script recomputes chaos.orl's orbit in CPython binary64, with two roundings per
step as Ørlǫg specifies. The printed values equal chaos.orl's to every digit; for example, step 3000 is
−1.99455473586439691047189626260660588741302490234375. For each step s from 1 to 3000, the value after step s is moved
one ulp up and, separately, one ulp down.

- Of the 6000 perturbations, 1526 leave every printed output unchanged.
- 1477 of those happen at steps ≤ 2900, far from the end.
- Example: step 7, x = −0.10449955806871913, erased in both directions.

Each erased perturbation would change an assignment event in the trace, and no output.

**The mechanism** (`chaos_merge.py`). This is not the two-to-one "coincidence" that the does-not-show names.

- 1210 of the 1530 perturbations that merge back do so at the very next step.
- Every value whose square absorbed a difference has |x| < 1 (the largest is 0.992).
- For |x| < 1, x² − 2 lies in [−2, −1), whose ulp is at least twice ulp(x). The stretch |2x| < 2 then leaves the
  perturbation below one ulp of the result, and rounding can absorb it.

The Lyapunov exponent ln 2 is an average, and "doubles a small difference at each step" holds only on average. The
measured FMA divergence stands, because a difference repeated at every step escapes absorption.

**Correction.** "Chaos amplifies a difference that recurs. A single one-ulp difference is erased by rounding about a
quarter of the time on this orbit (measured). Traces, not outputs, localize single differences."

## L17. Court rules R1–R7 against court.py — OVERREACH

**Argument.** SPEC §3 allows the claim form as an inline statement (`If C, S; otherwise S`). The court cannot read such
claims: for a claim inside an If clause, `an.claims` holds the If clause, and `c.stmt` is the IfS.

**D9 (MEASURED).** `§1 Let a be 1.` / `§2 If a equals 1, we claim that a is positive; otherwise we claim that a is
negative.` Here `panel` raises "AttributeError: 'IfS' object has no attribute 'id'". A claim the grammar permits gets
no standing at all, against T2's "every claim names its channel, and the court reads the channel". Fixing `s` would
not be enough (CODE): rows, premises and claim seals are keyed by clause id, so two inline claims in one clause would
collide, and `claim_law_lines` would seal the whole If line for both.

R7 says a claim never evaluated has "no standing, neither support nor refutation". The code gives it UNSUPPORTED,
counts it among the unsupported, and strips support from every claim that cites it.

**The R7 demonstration (MEASURED).**
```
§1 Let a be 1.
§2 If a equals 2, do the following.
§2.1 We claim that a is odd.
§3 We claim that a equals 1, given §2.1.
```
§2.1 is UNREACHED and reads UNSUPPORTED. §3 is true in 1 of 1 evaluations and also reads UNSUPPORTED. The summary
reads `"unsupported": 2`. The record's §4 ("UNREACHED is its own standing") holds only in the evaluation column.
Likewise, R1 says the standing of a disagreeing run's claims "is CONTESTED", but the support column says UNSUPPORTED
(D5).

**Correction.** Key court rows by claim id rather than clause id, and seal each claim's own law statement. Make
UNREACHED a support value, not counted as UNSUPPORTED. Align R1's wording with the columns.

## L18. §8, the non-claims "in one place" — OVERREACH

These are missing:

1. A theorem ratification is a name, bound neither to the program nor to the claim, so one line grounds every claim
   that quotes it (L4, L8). The court artifact's `does_not_certify` has half of this; §8 has none.
2. Counted operations are a unit-cost model, not time or work. The ratio is taken against the clause's own cost, not
   the task's fastest program, and little-oh is undefined on bounded domains (L6).
3. The support graph is the author's declared premises. Undeclared dependence is invisible, and omitting `given` makes
   a claim WELL-FOUNDED (L10). T4 says the first part; §8 does not.
4. `sandwich_closed` is vacuous when nothing is supported, including when a backend dissents (L10).
5. The court gives no standing to claims written inline (L17).
6. No plant has ever decided CERTIFIED (L8).
7. On the measured orbit, chaos erases about a quarter of single one-ulp differences (L16).
8. The door can move a literal boundary (L12), and retraction is measured only on canonical text (L13).

**Correction.** Add them.

## L19. The counts in §5, T1 and T7 — IMPRECISION

**Argument.** DOCTRINE (last written at 16:15) reports "ORLOG SELFTEST 78/78" and "9 plants caught", and says at T1
that the planted wrong g "is not yet in the self-test". The earliest run in the folder,
`build/evidence/selftest-run.txt` (16:17:18), reads "ORLOG SELFTEST 80/80", with 10 plants caught and 1 equivalent;
among them is "law-gcd-wrong-answer (g doubled): CAUGHT". "9 plants" matches neither file. Since then `selftest.py`
has gained a cycle row and a codegen row (16:21), and the corpus has gained an eleventh program (`fall.orl`, 16:20), so
"10 programs" is stale too.

The record's §3 says its counts are derived, because prose numbers desert (Urðr L16); these deserted within minutes.
The evidence is stronger than the record says, but the record is not current.

**Correction.** Derive the counts from a dated run and cite that run's file. Strike "not yet in the self-test" for the
gcd plant. The leapfrog plant in the self-test is a constant drift, not T7's "velocity-dependent rounding"; say which
plant is meant.

## L20. §7, outside the brief's sections — IMPRECISION

- "`this law's seal` …: Kleene-style self-reference with no fixed point." Kleene's recursion theorem *is* a fixed-point
  theorem (φ_e = φ_h(e); R1a §6). Here the runtime hands the program a hash of law bytes that hold the expression
  `(seal)`, not its value (sema.py:472–473), so no fixed point is needed. This is reflection supplied by the
  interpreter, not Kleene's construction.
- "x∘y = 2x ⊕ y over GF(2^8), Damm's construction." R3 §B says: "No source found calls it *the* standard construction;
  Damm's constructions target orders 4k+2". It is the ISO/IEC 7064 pure family (Horner's rule).

**Correction.** Write "self-reference supplied by the runtime; no fixed point is needed, because the law holds the
expression, not the value", and "the ISO 7064 pure system: a totally anti-symmetric quasigroup, in Damm's sense of the
property".

---

## Tried, and held (SOUND)

- **S1. Knaster–Tarski, and court.py's computation.** The theorem is stated and attributed correctly (Tarski 1955;
  Knaster 1928 proved existence, on power sets). court.py's `lfp` and `gfp` are Kleene iteration, from ∅ and from the
  universe, of a monotone G on a finite power set, and both are correct. gfp ∖ lfp is the set of held claims whose
  declared support reaches a cycle (CODE; D5 and D6 agree).
- **S2. Dung.** The characteristic function and the grounded labelling are implemented as Dung defines them
  (court.py:100–108, and the self-test's five-argument fixture). `court/judge.py` (16:17, after the record) now uses
  them for the court of findings. The judgment lives in the attack relation the judge writes, as support lives in the
  declared premises.
- **S3. The DPI.** It is stated with its hypothesis and attributed correctly (Cover & Thomas, Thm 2.8.1). "No external
  bits" for computation is true for closed programs, since there is no input statement.
- **S4. A run on a machine as a channel.** The record handles this consistently. A run carries bits about the machines
  (under R1 a dissent removes support), none about the author's intent beyond the text, and nothing lets agreement add
  grounding.
- **S5. The Bezout check.** It characterizes gcd: g | a, g | b, g > 0 and g = as + bt imply g = gcd(a, b) when a and b
  are not both 0. Checked i64 arithmetic refuses rather than wrapping, so no overflow escapes. McConnell et al. is the
  right attribution, and the g-doubled plant is refused at §12 (80/80 run).
- **S6. T5's causal claim.** "Because each rounded intermediate is observed by the canonicalization" held under a
  control the record lacked (MEASURED, `fma_cause.py`). For chaos.orl's generated C under clang 22.1.8 with `-std=c99
  -O2 -ffp-contract=fast -march=native`, the code as generated has 0 FMA mnemonics; with `orl_f_canon` made the
  identity, it has 1. Under `-ffp-contract=fast`, clang disregards the FP_CONTRACT pragma (LLVM Discourse, "fp-contract=fast
  and pragmas"), so the canonicalization is what prevents the fusion. Two wording notes: "by construction" holds for
  the semantics, while for compiled backends it is a measurement on one host; and the 0-FMA count covers one program.
  Add the control as a plant row.
- **S7. Levesque & Verlet.** The stated conditions are right: forces depending only on positions, plus rounding
  symmetric under negation, suffice for exact reversal. D10 shows they suffice even for a non-conservative force.
- **S8. T8's mechanism.** The backends read no label, text or spelling field (CODE: `lower.py`, `gen_*.py`). The three
  spellings' receipts differ only in their text-seal lines (`build/runs/*-python.receipt`).
- **S9. Löb and Artemov as theorems.** Löb's theorem, Artemov's explicit reflection (for each numeral p,
  PA ⊢ Proof(p, ⌜φ⌝) → φ, by Σ1-completeness) and the realization of S4 by LP are stated correctly, with hypotheses
  abbreviated. Only their application fails (L1, L3).
- **S10. Blum and the reliability results.** T3's statement of Blum's rule (ICSI TR-88-009; Wasserman & Blum 1997;
  "heuristic contention") matches R1b, as do the Knight & Leveson and Eckhardt & Lee summaries. The Chebyshev map's
  conjugacy and its Lyapunov exponent ln 2 match R3 §E.

Sources fetched this session: Babovich, Erdem & Lifschitz, "Fages' Theorem and Answer Set Programming",
<https://ar5iv.labs.arxiv.org/html/cs/0003042>; LLVM Discourse, "fp-contract=fast and pragmas",
<https://discourse.llvm.org/t/fp-contract-fast-and-pragmas/58529>.
