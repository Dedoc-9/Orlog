# The owner's rulings on RUST-CORE-0 (in his words)

Recorded as he gave them, whole, on 2026-10-30, after [SHEET.md](SHEET.md). The rulings that authorized the milestone
sheet are in [research/law-sufficiency/RULINGS.md](../law-sufficiency/RULINGS.md).

## RUST-CORE-0 accepted, with D1–D5 (2026-10-30)

> Yes. I accept RUST-CORE-0 with the recommended choices D1–D5. The Rust core is authorized as a separate, off-gate
> research milestone, subject to the boundaries below.
>
> ## D1–D5 rulings
>
> | Choice | Ruling |
> | --- | --- |
> | D1 — Authoring | Accepted. Clean-room implementation, derived only from LAW-FORMAT-0, the two specifications, and the vectors. No copying or translating `numeric_ref.py`, `gen_rs.py`, or `rt_rs/`. |
> | D2 — Float | Accepted. Host binary64, matching the existing runtime model. Software Float remains Track B, outside this milestone. |
> | D3 — Validation | Accepted. Full well-formedness validation: grammar and every specified derivation. The core accepts only canonical law bytes it could itself write. |
> | D4 — Location | Accepted. `research/rust-core/`, entirely off the gate. |
> | D5 — Receipt identity | Accepted. Receipt identifies the backend as `rust-core`. |
>
> ## Conditions on the experiment
>
> I accept R1–R8 as the milestone's predictions, with these clarifications:
>
> 1. LAW-FORMAT-0 is a prerequisite. Write the format obligations first, including all 18 derivations, ordered
>    definitions, canonical encoding, and round-trip requirements. Then obtain the independent re-read before
>    implementation begins.
> 2. Independence must be real. The author must not use the existing decoder, interpreter, generators, or numerical
>    reference as implementation material. The specifications and vectors are the permitted authority.
> 3. Mutation testing must distinguish refusal from agreement. A mutated byte string may be refused, or accepted only if
>    its execution agrees with the decoded reference. Record which outcome occurred for every case. Do not count an
>    accepted malformed encoding as a successful refusal.
> 4. Budget tests must compare stopping behavior, not merely final output. The first stopping point and resulting
>    receipt/trace must agree with the reference.
> 5. Cache use must be disclosed and verified. Cached artifacts must be checked against their recorded inputs and
>    outputs. The evidence must distinguish fresh builds from cached runs.
> 6. Twice-identical results are necessary, not sufficient. Preserve the exact commands, compiler versions, host
>    details, seeds, inputs, outputs, and plant results.
>
> ## Acceptance boundary
>
> Authorized
>
> RUST-CORE-0 research milestone
>
> - LAW-FORMAT-0 and its independent re-read come first.
> - The core may then be implemented and tested under the accepted sheet.
> - It remains off-gate and does not replace or modify `gen_rs.py`, `rt_rs/`, the Python reference, or version 1.
> - Passing R1–R8 establishes the milestone only.
> - Supplementing a production path requires the additional evidence and a separate ruling naming that path.
> - Replacing the Python reference is not authorized.
>
> One additional distinction: the supplied text seal is external input because it is not contained in the law bytes.
> The core computes the law seal itself; it must not imply that it independently derives or validates the text seal.
>
> Final disposition: D1–D5 accepted. RUST-CORE-0 accepted. Proceed with Phase 0, then the clean-room implementation and
> experiments. No production integration, gate changes, release changes, or authority transfer.

## REREAD-0's dispositions accepted, with A1(a) and A2(a) (2026-10-30)

> Yes. I accept the proposed dispositions, including A1(a) and A2(a). LAW-FORMAT-0 remains in Phase 0; this does not
> authorize core implementation. The blocker and all listed major and minor findings must be resolved before the
> clean-room author receives the format.
>
> A1 — Accept (a): allow otherwise-refused text characters
> A law-format reader may accept text-literal characters that the current front end refuses, including control
> characters and bidi controls, provided the format defines their encoding and execution unambiguously.
> The distinction is important:
>
> * Format validity determines whether law bytes are structurally valid and executable.
> * Source-language admissibility determines whether the current front end can produce those bytes from source text.
>
> Those are not necessarily identical sets. Do not freeze a particular Python version's Unicode acceptance table into
> the machine format merely to make them identical.
> The checker must still enforce the format's actual byte, encoding, and scalar-value constraints. A1(a) is not
> permission to accept malformed UTF-8 or invalid Unicode scalar values.
>
> A2 — Accept (a): supplementary integer-conversion vectors
> Authorize a supplementary vector file under `research/rust-core/`, generated from `numeric_ref.py`, without modifying
> the contract vector file.
> Conditions:
>
> 1. Preserve the original contract vectors unchanged.
> 2. Keep supplementary vectors separately identified and hashed.
> 3. Record their generation provenance, exact generation command, and numeric-reference version or source hash.
> 4. Give the clean-room author the generated vector data, not `numeric_ref.py` or its implementation.
> 5. Treat these as supplementary test evidence, not as a change to the version-0 contract or an expansion of the
>    reference authority.
>
> This is consistent with D1: the author receives specifications and vectors as data, not another implementation to
> translate.
>
> Accepted dispositions
> The proposed technical corrections are accepted:
>
> * Clause order must preserve tree order.
> * The ID-numbering walk must be specified exactly, including the valid forward-declaration case.
> * W14 must specify the front end's actual expression-depth limit.
> * Promotions must be restricted to those the front end inserts.
> * Both invalid If-chain shapes must be excluded.
> * Budget-check positions must be exact, including do-nothing clauses.
> * The run interface must tabulate every outcome.
> * Seal words become the nineteenth derivation.
> * Build constraints and vector-file line format must be documented for the clean-room author.
>
> F1 is the release-blocking issue: a reader that accepts a different clause order can produce a law that crashes
> through a read-before-assignment. That must be fixed at the format level, not worked around in the implementation.
>
> Conditions for the next re-read
> I authorize the following Phase 0 work:
>
> 1. Produce LAW-FORMAT-0 draft 1 with the accepted dispositions.
> 2. Extend `format_check.py` to accept the re-reader's valid laws and reject the counterexamples.
> 3. Keep the original re-read report and first draft intact.
> 4. Obtain a fresh, targeted independent re-read of the revised document and checker.
> 5. Resolve its findings before authorizing any core code.
>
> One additional requirement: the checker is evidence for the format, not the format's authority. Its agreement with
> the document cannot substitute for the independent re-read.
>
> Phase 0 work authorized
> Final boundary: draft 1, checker amendments, and another independent re-read are authorized. Rust-core
> implementation, production integration, gate changes, and release changes remain unauthorized.

**As kept:**
- Draft 0 is `LAW-FORMAT-0-DRAFT-0.md`, renamed from `LAW-FORMAT-0.md` with its bytes unchanged (sha256 `1ae57ee8…`,
  the version REREAD-0 read).
- Draft 1 is `LAW-FORMAT-0-DRAFT-1.md`. The highest-numbered draft is current.
- REREAD-0's report is unchanged (sha256 `5bb1494f…`).
- `evidence/rust-core-format.txt` stays the record of draft 0's checker run. Draft 1's goes to
  `evidence/rust-core-format-1.txt`.

## B1, the merged six-part formulation, with three precision corrections (2026-10-30)

He first chose B1(a) with a qualification. He then asked for the best approach to be evaluated with a web search, and
the merged six-part formulation was put to him. His ruling on it:

> Yes. Adopt the merged six-part B1 as the basis for LAW-FORMAT-0 draft 2, with three precision corrections. The
> six-part structure is better than either earlier formulation because it separates language guarantees from
> implementation behavior and experimental comparison.
> Accepted
>
> 1. Language: No artificial nesting limit on procedure calls or rule uses. Given the existing no-recursion and
>    bounded-loop rules, every accepted execution terminates after finitely many operations. This is a structural
>    guarantee, not a practical-completion guarantee.
> 2. Evaluation: Explicit-stack evaluation in Rust. Host recursion depth is not a language restriction.
> 3. Budget: Preserve the existing statement-budget semantics exactly. Work inside one statement may exceed the budget
>    by an arbitrary amount.
> 4. Resources: Resource exhaustion is an operational failure, never a language refusal, budget result, or completed
>    execution.
> 5. Reference comparison: Compare only where Python produces a result within the preregistered time limit. Repeat
>    crashes and timeouts are classified as no reference result; inconsistent outcomes are unstable.
> 6. Evidence: Test deep nesting, explosive work growth, exact budget boundaries, and separation of operational failures
>    from semantic outcomes.
>
> Three precision corrections
> 1. Do not redefine the budget in prose.
> Use the exact check position already established in LAW-FORMAT-0. The phrase "no statement begins once counted
> operations exceed B" must not accidentally change when the counter increments or whether a do-nothing clause is
> counted.
> 2. Distinguish detected exhaustion from external termination.
> An explicitly detected allocation failure may produce a dedicated operational exit status and diagnostic, with no
> receipt. But an OS kill or externally enforced timeout cannot necessarily produce that diagnostic. The harness must
> classify those outcomes separately. Do not promise that Rust can catch every possible process-level memory failure.
> 3. Fix the comparison protocol before testing.
> The time limit, repeat count, and classification rules must be written into the sheet before experiments begin. A
> timeout or crash counts as no reference result only when reproduced in both runs; otherwise classify it as unstable.
> Never count an operational failure as a semantic disagreement.
> Scope
> The following remain separate:
>
> * Python recursion failure: reference implementation defect/limitation, not a language restriction.
> * `HostStop` docstring: correction proposal, not an authorized source edit.
> * Future deterministic fuel accounting: a possible new, versioned language feature, not a reinterpretation of the
>   current budget.
> * Clause ontology: noted for later, not part of this draft unless separately authorized.
>
> B1 merged formulation accepted
> Proceed with draft 2 and its checker amendments. The fresh independent re-read must specifically verify termination
> reasoning, budget preservation, explicit-stack requirements, and the distinction between detected resource failure
> and external process termination.
> No core implementation, `src/` changes, gate changes, or release changes are authorized yet.

His earlier text, *"I choose B1(a), with an important qualification: unbounded language nesting does not mean
unbounded execution resources or a guarantee of completion"*, is what this formulation merged. Its terms are kept in
the merged six parts and in the three corrections.

## REREAD-2's dispositions accepted, with C1(a) and C2(a) and three qualifications (2026-10-30)

He was put [REREAD-2-DISPOSITION.md](REREAD-2-DISPOSITION.md): 13 DRAFT items, ASK C1 (H3, an end of the core that no
row of section 10 gives) and ASK C2 (H4, the reference's run conditions and the protocol's other gaps). His ruling,
whole:

> Yes. Adopt the proposed dispositions, with C1(a) and C2(a). Both are necessary to make the milestone's evidence
> meaningful. I also accept the other proposed document and checker corrections, subject to the following precision
> rulings.
> C1 — Accept (a): core faults fail
> An unknown exit status, panic, stack overflow, or other unexpected core termination is a core fault, not an unlisted
> operational outcome.
>
> * A core fault fails the prediction being tested.
> * On every case where Python produces a reference result, the core must produce a comparable result. Any operational
>   failure is a coverage failure, not a semantic disagreement.
> * Recognized resource exhaustion remains separately classified.
> * External termination, such as an OS kill, must not be relabeled as a successful resource-handling result.
>
> This prevents a core that crashes on difficult inputs from passing simply because its exit status was not anticipated.
> C2 — Accept (a): use the reference as shipped
> Run Python in a fresh process at its default recursion limit, without importing the checker. Record the exact Python
> version and execution environment.
>
> * Do not raise the recursion limit to manufacture reference results.
> * A reference crash or timeout must reproduce in both runs to qualify as no reference result.
> * Inconsistent reference outcomes are unstable.
> * A core whose repeated runs differ is unstable and fails.
> * Replace R6's ambiguous "never hangs past the budget" with a fixed 60-second core execution limit.
> * Write S3's exact budget-sampling values and procedure into the sheet before testing.
>
> The 60-second core limit is an experimental safeguard, not a language budget or a semantic timeout.
> Three important qualifications
>
> 1. Correct the budget statement.
> H1 exposes a real error in the draft. The phrase "a statement that begins with ops ≤ B runs to its end" is not
> acceptable.
> The governing rule is the exact sequence of operation counting and budget checks already established by the
> reference and specification. A `While` body can contain its own check point. Work may exceed the budget between
> check points, but not necessarily throughout an entire enclosing statement.
> Do not generalize beyond those exact positions.
> 2. Separate syntactic depth from execution nesting.
> Accept H2's bounded checker walk: W14's existing clause-tree depth restriction must be checked before any unbounded
> recursive traversal. The checker must refuse an over-depth clause tree without crashing.
> That does not introduce a depth limit on `perform` or rule-use chains. Those remain the explicit-stack evaluation
> requirement.
> 3. Keep operational outcomes honest.
> A detected allocation failure can produce the specified resource-exhaustion status and diagnostic. An OS kill,
> external timeout, or process crash may not. The harness must distinguish these outcomes; it must never award a pass
> merely because execution stopped.
>
> Disposition
> C1(a) and C2(a) accepted
> Proceed with:
>
> 1. Draft 3 incorporating the accepted REREAD-2 dispositions.
> 2. Checker amendments, including the bounded clause-tree walk and new 30,000-deep plants.
> 3. SHEET Amendment 2, fixing the comparison protocol before experiments.
> 4. A fresh targeted independent re-read covering the four original B1 requirements and these new corrections.
>
> One further requirement: preserve the distinction between no reference result, unstable, core fault, recognized
> resource exhaustion, and external termination in the evidence records. They must not collapse into a generic failure
> category.
> No core implementation, `src/` changes, gate changes, or release changes are authorized. Phase 0 continues.

**As kept.** H1's replacement in draft 3 states the check positions and nothing beyond them, as his first qualification
requires. The proposed sentence about "the work no check position separates" is not used as a rule. W14(a) is checked
before the walk, from the parent links. The walk then stays within the depth W14(a) allows, and no limit is added on
`perform` or rule-use chains (his second qualification). The five classes he names are kept apart in SHEET Amendment 2,
and in every evidence record it governs.

## REREAD-3's dispositions accepted, with E1(b), E2 and E3(a) (2026-10-30)

He was put [REREAD-3-DISPOSITION.md](REREAD-3-DISPOSITION.md): its DRAFT items, ASK E1 (J1 and J7, what phase 3 walks
when the tree is too deep or a chain is malformed), ASK E2 (J2, J3, J4 and J14, the predictions the sheet had not
fixed) and ASK E3 (J5, the evidence that decides two class boundaries). His ruling, whole:

> Yes. Adopt E1(b), E2 as proposed, and E3(a). I also adopt the twelve document, checker, and sheet dispositions
> recorded in `REREAD-3-DISPOSITION.md`.
> The three rulings are:
> E1 — Adopt (b): depth validation is a gate
>
> * Phase 3 checks W14(a) and W14(b) before traversing the clause tree.
> * If either check fails, the checker reports the failure and does not walk the tree.
> * The depth check itself must be bounded and non-recursive; it cannot depend on the traversal it is intended to
>   protect.
> * Once the checks pass, the subsequent walk covers the entire tree. No claim that truncating a walk preserves
>   declaration numbering is needed.
> * A chain failing W4 is likewise rejected before traversal.
>
> This preserves the distinction between syntactic depth restrictions and unbounded execution nesting.
> E2 — Adopt the proposed fixed evidence protocol
>
> * R5: Freeze and hash the budget values in advance. Compare outcome classes, not an assumed universal STOPPED
>   result. If the reference completes at a sampled budget, a comparable core completion is valid.
> * R6: Freeze the 10,000 mutants. Identify `decoder1.py` by exact path and SHA-256. Add `REFERENCE-REFUSED` as a
>   distinct reference outcome; if the reference refuses a mutant, a core that accepts it fails that prediction.
> * S1/S2: Freeze the texts. For S1, any outcome other than completion with the constructed operation count fails.
> * A reference crash counts as reproducible only when both fresh reference runs have the same exit status and
>   exception type. Otherwise classify it as unstable, not as an established absence of a reference result.
>
> Keep reference refusals, reference crashes, core faults, and operational outcomes distinct. None may be silently
> converted into a successful comparison.
> E3 — Adopt (a): no Windows host evidence
>
> * No host evidence is accepted on Windows for this experiment.
> * Any termination not caused by the harness is a core fault.
> * Before accepting results, inspect the core's source and verify that exit code 5 is used exclusively for a
>   detected failed fallible allocation.
>
> That last condition is a narrow classification rule, not a claim that every possible memory failure can be caught.
> An OS kill or unexplained process termination does not become `RESOURCE-EXHAUSTED` merely because memory pressure is
> suspected.
> Authorization boundary
> Proceed with Draft 4, the checker amendments, and SHEET Amendment 3 implementing these rulings and the twelve
> accepted dispositions. Then run a fresh independent re-read against the revised artifacts.
> No Rust-core implementation, production-source changes, gate changes, release changes, commit, or push is authorized
> by this ruling. Phase 0 remains the active scope.

**As kept.**
- **The twelve dispositions** are J6 to J17. Eleven are DRAFT rows of the disposition's table (J6, J8–J17). J7 is
  disposed under E1's second part, which he adopted in its fifth point.
- **E1's gates.** The first is W14(a) and (b), computed from the parent links in one pass with no recursion, before
  any walk. His fifth point, *"A chain failing W4 is likewise rejected before traversal"*, is read with "likewise" as a
  second gate after it: a law with a chain whose arm, else or block names no clause is refused with W4 before any walk.
  So J7's law now reports W4 at line 4, where the disposition, which proposed only that such a chain's blocks be
  skipped, predicted W8 at line 3. The walk that follows covers the whole tree. G8's adopted rule still applies within
  it: the blocks of a chain failing W5, and an inline statement failing W7, are not entered. He made no ruling that
  W5 or W7 be gates.
- **E2's "exception type"** is read from the last line of the reference's traceback, as the disposition proposed.
  *[Note, 2026-10-30, REREAD-7's Y9: superseded, first by K15 (Amendment 4: the text before the first `:` of stderr's
  last line), then by the runner's own `REFERENCE-EXCEPTION <module>.<qualname>` line (Amendment 5). His D2 confirmed
  the runner's line as the record (below).]* *[Note, 2026-10-31, REREAD-8's ZC6, adopted by his ruling on the ruling
  sheet: the history in this note is corrected: the colon rule was Amendment 3's; K15, in Amendment 4, brought the
  runner's own line; Amendment 5 brought the raw `classify`]*
- **E3's source reading** is recorded before R1–R8 count, and it is a classification rule only, in his words *"not a
  claim that every possible memory failure can be caught"*.

## REREAD-4's dispositions accepted, with F1(b) and F2(a), R2b included (2026-10-30)

He was put [REREAD-4-DISPOSITION.md](REREAD-4-DISPOSITION.md): its DRAFT items for the thirteen minor findings, ASK F1
(K1, K4, K5: whether the walk covers the whole tree) and ASK F2 (K2, K3: what decides, in R6, that the core accepted
or refused a mutant wrongly). His ruling, whole:

> Yes. Adopt F1(b) and F2(a), including R2b. I also accept the thirteen minor findings as wording corrections, provided
> they do not change the adopted format rules or evidence classifications.
> F1 — Adopt (b): W5 and W7 become a third pre-walk gate
> The checker must complete three validation gates before traversing the clause tree:
>
> 1. Depth gate: W14(a) and W14(b).
> 2. Chain gate: W4, covering every If arm, else and block reference.
> 3. Structure gate: W5 and W7.
>
> If any gate fails, report the applicable failure and do not begin the tree walk. If all three pass, traverse the
> entire tree without a depth cap or skipped subtrees.
> This replaces the earlier arrangement in which W5/W7 failures could cause portions of the tree to be skipped. The
> purpose is to make declaration numbering and reported diagnostics independent of partial traversal.
> One point remains deliberately unsettled: the order of the three gates. The order in Draft 4 was the author's choice,
> not an adopted ruling. Preserve any validation precedence already required by the specification. If the
> specification does not determine the order, propose and freeze one explicitly before the next evidence run; do not
> silently treat Draft 4's order as authoritative.
> F2 — Adopt (a): independent adjudication
> The checker is an evidence-selection mechanism, not the authority deciding correctness.
>
> * Whenever the core's verdict on a mutant differs from the checker, an independent reader adjudicates the case
>   against Section 8.
> * Record the reader's determination and the exact applicable rule and diagnostic.
> * Do not count checker agreement as proof that the core is correct when both could share the same defect.
>
> R2b — Adopt
> Add a fixed, hashed set of laws, each containing exactly one non-canonical change.
> For every fixture, the core must refuse with the correct W code and line. Freeze the fixtures and expected outcomes
> before testing. This directly tests the decoder's canonicality enforcement rather than relying on R7 predictions that
> cannot detect that defect.
> Also include the now-written R6 reference-running program by exact path and SHA-256 in the sheet. Its classification
> of reference refusal versus crash must be fixed and independently reviewable; the harness must not silently decide
> that distinction.
> Authorization boundary
> Proceed with Draft 5, the checker changes, and SHEET Amendment 4, incorporating these rulings and the thirteen minor
> corrections. Then commission a fresh independent re-read of the revised artifacts.
> The R2b fixtures and reference runner are research evidence infrastructure, not permission to implement the Rust
> core. No Rust-core implementation, production-source changes, gate or release changes, commit, or push is authorized.
> Phase 0 remains the scope.

**As kept.**
- **The gates' precedence** is settled in draft 5's section 8, frozen in SHEET Amendment 4, and put to him there.
  *[Corrected 2026-10-30, REREAD-5's L1: this reading was wrong. The E1(b) text he adopted puts the depth gate
  first: "If any clause fails, the least such line is reported as W14, and no W4–W13 check is made." He then
  confirmed it (N1, below). The note is kept as it was written.]*
  In the writer's reading the specification determines it, and nothing is taken from draft 4's order:
  - the adopted rule is REREAD-0's F8: *"A load refusal reports the first failing line, and within it the lowest W."*
    Later rulings refined it in two ways only: phases 1 and 2 (W1, then W14(c), W2 and W3, line by line; G6 and G9),
    and the gates before the walk (E1, F1);
  - E1 and F1 override it only by placing the three gates before the walk;
  - so among the gates' failures the least (line, W) still governs. The three gates are one pre-walk phase, and no
    gate's failure outranks another's but by line, then W.
- **The thirteen minor findings, held to his proviso.** One proposed correction would have changed the run interface:
  K8's new exhaustion kind `state`. It is dropped, and each of J6's stores is mapped to one of section 10's existing
  six kinds instead. K9's definition of a result fills in what *"differ in class or in result"* left undefined, and
  changes no class: a case already unstable stays unstable, and one that is not stays not. *[Corrected 2026-10-30,
  REREAD-5's L12: "changes no class" could not be shown. K9 decided cases the earlier text left undefined, and he then
  confirmed that reading (N3, below).]*
- **The reference runner** is written once, for every reference run of the experiment: the texts through the front
  end, and R6's mutants through decoder1. Its line between a refusal and a crash is fixed in its code, and recorded in
  the sheet by path and sha256. *[Note, 2026-10-30, REREAD-7's Y9: his F2 words named the R6 runner; extending it to
  every reference run was the writer's, and Amendment 5 has since excepted R8, whose core runs under the arbiter.]*

## REREAD-5's dispositions accepted, with N1(a), N2(a) and the three N3 confirmations (2026-10-30)

He was put [REREAD-5-DISPOSITION.md](REREAD-5-DISPOSITION.md): its DRAFT items for the ten minor findings *[corrected
2026-10-30, REREAD-6's M2: the DRAFT items were twelve, L2 and L3 (both MAJOR) and L5–L14; he then confirmed L2's and
L3's as applied (U2, below)]* *[corrected again 2026-10-30, REREAD-7's Y7: thirteen, since L1's row also carried a
DRAFT part ("ASK N1. And DRAFT, whatever he rules"); his D3 confirmed thirteen (below)]*, ASK N1
(L1, L6: the gates' precedence), ASK N2 (L4: how R2 is observed) and ASK N3 (L8, L12: three readings that touch his
proviso). His ruling, whole:

> Yes. Adopt N1(a), N2(a), and all three N3 confirmations. These dispositions preserve the earlier rulings; they do
> not authorize implementation or change the language's semantics.
> N1 — Adopt (a): depth gate has precedence
> The adopted E1(b) wording already establishes this precedence:
>
> 1. W14 depth gate first. If any clause fails W14(a) or W14(b), report the earliest failing line as W14. Do not run
>    W4–W13 checks.
> 2. Chain and structure gates second. If the depth gate passes, collect W4, W5 and W7 failures and report the
>    earliest line, breaking ties by the lowest W.
> 3. Full tree walk last. Only after both stages pass; no cap and no skipped subtrees.
>
> This resolves the apparent conflict with F1. F1 did not supersede E1(b). The five order fixtures should encode this
> precedence, including the two cases that now report W14 at line 28.
> N2 — Adopt (a): observable write-back
> Add a research-mode write-back path to the core:
>
> * The core writes back the exact law bytes it successfully loaded.
> * The harness compares those bytes byte-for-byte with the original input.
> * A mismatch fails the round-trip obligation.
> * A load refusal does not count as a successful round trip.
>
> Keep this separate from ordinary output, receipts and traces. It is an observable format obligation, not a new
> semantic execution path or a change of authority.
> N3 — Confirm all three
>
> 1. W5: It counts only blocks of Ifs that are a clause's own statement. Preserve that narrow interpretation
>    explicitly in Draft 6 and its tests; do not generalize it to arbitrary nested blocks.
> 2. Stability: Two runs differing only in a load-refusal line or an exhaustion kind are `UNSTABLE`, not equivalent.
>    Preserve the existing six-kind interface; do not introduce a new exhaustion kind.
> 3. Interrupted experiments: Discard the experiment as a whole and repeat it. Retain the interrupted runs and count
>    them in the evidence record, but never use their partial results toward acceptance.
>
> Next step and boundary
> Proceed with Draft 6, checker and runner corrections, and the updated frozen evidence protocol. Then conduct a fresh
> independent re-read, including explicit review of the gate precedence, write-back observability, and all three N3
> interpretations.
> The ten minor findings may be applied as mechanical wording, test and runner corrections, provided they do not alter
> adopted semantics or classifications.
> No Rust-core implementation, production-source changes, gate or release changes, commit, or push is authorized.
> Phase 0 remains active.

**As kept.**
- **N3's second point.** His `UNSTABLE` is read as the core's case class, UNSTABLE-CORE, since the runs he names (a
  load refusal, an exhaustion kind) are the core's. The reference's UNSTABLE is unchanged.
- **N2's write-back** is a mode of the core's command line of its own: it reads and checks the law, writes back what
  it loaded, and runs nothing. A load refusal there fails R2 for that text, in his words *"does not count as a
  successful round trip"*.
- **The runner's faults (L3, L5)** stop the experiment, which is then repeated whole, as his third N3 point says of an
  interrupt. The runs before the fault are kept and counted, and never used toward acceptance. *[Note, 2026-10-30,
  REREAD-7's Y10: this extension was the writer's (REREAD-6's M2). His U2(2) then adopted it, and his B1–B4 (below)
  define the experiment, its repeat and its stop.]*

## REREAD-6's dispositions accepted, with U1(a) and U2, the recurring-runner-fault rule included (2026-10-30)

He was put [REREAD-6-DISPOSITION.md](REREAD-6-DISPOSITION.md): ASK U1 (M1: how R2 tells a re-encoding from an echo),
ASK U2 (M2: three points of the runner's faults), and DRAFT items for M3–M10. His ruling, whole:

> Yes. Adopt U1(a) and U2, including the recurring-runner-fault rule. I also accept the remaining minor dispositions as
> text, test, and evidence-record corrections, provided they preserve the existing language and outcome semantics.
> U1 — Adopt (a): OUT must come from the writer
> The write-back obligation must test actual serialization, not echoing.
>
> * Section 10 must state that OUT is produced by the writer from the decoded law representation, never copied from
>   the input bytes.
> * R2 compares that independently produced OUT byte-for-byte with the original law bytes.
> * R7 gains the two writer-defect plants: dropping a name and reversing an `over` list.
> * R2 must catch both defects through the resulting byte mismatch.
> * The independent source review records the actual provenance of OUT, so the evidence establishes that the
>   writer—not an input-byte copy—produced it.
>
> The distinction is important: a successful byte comparison alone does not prove that a writer ran.
> U2 — Adopt all three points
>
> 1. L2 and L3: Accept the proposed corrections as applied. A front-end refusal and an invalid budget argument must
>    not be misclassified as reference crashes or successful results.
> 2. Runner faults: Treat a runner fault as an interruption of the entire experiment. Retain the records, discard all
>    partial results for acceptance purposes, and repeat the whole experiment.
> 3. Recurring runner fault: If the same runner fault occurs again on the repeat, stop and bring it back for a
>    ruling. Do not keep retrying, relabel it as a reference outcome, or allow it to disappear into an interruption
>    count.
>
> Keep runner faults distinct from reference exceptions, core faults, and externally caused termination. The repeat
> rule is experimental procedure, not a new semantic outcome class.
> Next step
> Proceed with Draft 7, checker and runner corrections, R7's two writer plants, and the corresponding sheet amendment.
> Then run a fresh independent re-read, specifically checking:
>
> * OUT's provenance and the two writer-defect plants;
> * the corrected L2/L3 classifications;
> * whole-experiment interruption and repeat behavior;
> * the recurring-fault stop condition.
>
> Authorization remains unchanged: Phase 0 only. No Rust-core implementation, production-source changes, gate or
> release changes, commit, or push.

**As kept.**
- **"The same runner fault"** is read as a runner fault with the same `RUNNER-FAULT` line, at the same case. A
  different runner fault on the repeat is not the same one, and the writer does not read his rule as covering it. The
  sheet leaves that case to him: it says what happens to the same fault, and puts the other to him at once rather than
  repeat again (Amendment 6). *[Corrected 2026-10-30, REREAD-7's Y1: the option he adopted, (iii) of
  REREAD-6-DISPOSITION.md, covers the case: "after one repetition that ends in a fault again, the experiment stops,
  and the fault goes to him. No third run". The writer checked his bullets and not that text, L1's mechanism again. His
  B1 confirmed that (iii) governs, and that a fault's identity is recorded but decides nothing (below).]*
- **M3's correction** reads W5's row as written (*"named by exactly one arm or else"*): a first arm counts as naming an
  absorbed clause, in a sound chain as in a W4 chain. That changes the checker's verdict, not the format's text. It is
  measured on R6's mutants, and the verdicts that move are listed. *[Corrected 2026-10-30, REREAD-7's Y8: M3 also added
  words to W5's row (draft 7, *[M3]*), and 61 refusals stayed W5 but moved line. No list was written: they are the
  rows that differ between `evidence/rust-core-r6-checker-6.txt` and `-7.txt`. His D4 confirmed the reading (below).]*

## REREAD-7 as three readers working at once, and the future remakes (2026-10-30)

*Recorded after the three readers had finished. He gave it before they started; reader 3 read this file under its
pinned sha256 (`2cb28949…`), so nothing was added to it while the readers worked.*

He was asked whether the re-reads and the remakes could be made faster by assigning several agents, or by running
several programs at once. His answer, whole:

> Yes. Adopt the three-reader parallel approach for REREAD-7. Start all three now, before the current reference-record remake finishes. The expected wall-time reduction is reasonable, but treat the one-hour estimate and threefold speedup as hypotheses until measured.
>
> I approve the following division:
>
> | Reader                      | Responsibility                                                                                                                                                                                            |
> | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | 1 — Format and checker      | Draft 7's format rules, validation phases, checker implementation, plants, and reversibility tests.                                                                                                       |
> | 2 — Protocol and evidence   | Sheet amendments, runner, frozen records, generators, outcome classifications, and a preregistered representative sample of mutants.                                                                      |
> | 3 — Rulings and consistency | Independently compare adopted rulings against every relevant draft, sheet amendment, checker obligation, and evidence claim. Own cross-document conflicts, precedence, omissions, and disposition counts. |
>
> ### Conditions
>
> 1. Independent review: Each reader starts fresh and receives the authoritative materials for its assignment. Do not share other readers' findings or conclusions before their reports are complete.
> 2. Cross-document review is mandatory: Reader 3 must explicitly check the adopted ruling text, not merely compare the latest documents with one another. L1 and M2 are examples of the exact failure this assignment must catch.
> 3. Sampling is evidence review, not regeneration: Reader 2 should freeze its sample selection before inspecting outcomes, cover the relevant reference classes and edge cases, and rerun those cases independently. The build remains responsible for generating the complete 10,000-mutant record twice.
> 4. Hash closure: The readers may review the generator, runner, and existing record while the remake runs. Once the final record is installed, verify its exact SHA-256 against Amendment 6. The re-read is not complete until that check passes.
> 5. One consolidated disposition: Merge the three reports, preserve every finding and its provenance, resolve overlaps explicitly, and bring me one disposition with clearly separated rulings required.
>
> ### Future remake optimization
>
> Approved in principle: run the two independent generations concurrently and increase worker counts to use available CPU capacity. Every individual reference execution must still use a fresh process. Do not share mutable state, caches, or generated outputs between the two generations. Verify byte-identical outputs and record resource usage so the speedup is measured rather than assumed.
>
> Authorization: This changes only the research review and evidence-generation workflow. It does not authorize Rust-core implementation, production changes, gate or release changes, commits, or pushes.
>
> I approve the plan; you can launch REREAD-7 locally under those conditions.

**As kept.**
- **The readers' wall time and cost were measured** (REREAD-7-DISPOSITION.md, *The measurements*): about 33 minutes
  from the first reader's start to the last report, and 1,072,002 tokens for the three, against single re-reads of
  28 to 55 minutes. The threefold speedup was not borne out.
- **Condition 1 was breached once, by the writer:** reader 3's report was saved into the reviewed folder while reader
  1 still read, and one of reader 1's greps matched a line of it. Reader 1 said so and did not open the file
  (REREAD-7-DISPOSITION.md, *Disclosures*).
- **Condition 4 passed** (`REREAD-7-READER-2-ADDENDUM.md`, *"HASH CLOSURE: PASSED"*).
- **The future remake optimization is not yet applied.** Two measurements bear on *"increase worker counts"*: a
  process the generator could not start (WinError 1450) beside the readers, and a reference run that comes within
  seconds of the 60-second limit under load. They are put to him before it is used (REREAD-7-DISPOSITION.md, ASK F).

## REREAD-7's dispositions adopted, A to F, with D1 qualified (2026-10-30)

He was put [REREAD-7-DISPOSITION.md](REREAD-7-DISPOSITION.md), the three readers' findings in one: ASK A (the writer
plants), B (the experiment and its interruptions), C (the acceptance list), D (five confirmations), E (four readings),
F (the remakes and REREAD-8), and DRAFT items for the rest. His ruling, whole:

> I rule in favor of the recommended dispositions for A–F, with one important qualification to D1: the expression-depth bound must not be changed until the actual front-end limit has been measured.
>
> These rulings adopt the six questions in REREAD-7. They authorize Draft 8, the corresponding checker and harness amendments, Amendment 7, and the fresh evidence generation and reread described in the disposition.
>
> They do not authorize Rust-core implementation. Phase 0 remains the limit.
>
> ## A — Writer plants: adopt (b)
>
> Ruled: adopt
>
> The core must decide W3 without calling the writer that produces `OUT`.
>
> Specifically:
>
> 1. W3 must be determined by code independent of the writer used to produce `OUT`.
> 2. R7's two writer plants must be caught through the resulting byte mismatch. A load refusal does not count as catching either plant.
> 3. Neither writer plant may be declared equivalent. If R2 does not catch a writer plant, R7 fails and the result comes to me.
> 4. The independent source reading must establish both:
>    - `OUT` is produced by decoding each atom to its value and re-encoding it under section 3.
>    - No slice of the input bytes reaches `OUT`, and W3 does not call the writer.
> 5. The source reading must be recorded before R2 acceptance is counted. A finding of an input-byte copy path or a writer-dependent W3 fails R2 and is reported.
> 6. Add the proposed R2 write-back fixtures for out-of-order and repeated `over` and `given` entries. Freeze their hashes before any core exists.
>
> This preserves the intended distinction: the plants test the writer's actual behavior; the source reading establishes its provenance. Neither substitutes for the other.
>
> ## B — Experiment and interruption protocol: adopt all five recommended dispositions
>
> Ruled: adopt
>
> B1 — A different fault on the repeat
>
> Adopt option (iii) from REREAD-6. After one repetition that ends in a fault again, the experiment stops and returns to me. No third run.
>
> The fault need not be identical. Record its identity, line if available, and exit status, but identity does not determine whether the stop rule applies.
>
> B2 — Unit of experiment
>
> An experiment is one complete attempt containing the prescribed cases in fixed order, from fresh builds.
>
> - The two runs required by a prediction are two experiments.
> - The two generations of an evidence record are separate experiments.
> - An interruption voids the attempt in which it occurs.
> - Repeat that entire attempt, not merely the failed case or a partial remainder.
> - A completed attempt stands.
> - Interruption counts and causes are retained with the evidence but never count toward acceptance.
>
> Thus, the 17:40 failure of generation 2 could be repeated as generation 2 alone: each generation is its own experiment. It does not require remaking a completed generation 1.
>
> B3 — Other interruptions
>
> The stop-after-one-repeat rule applies to interruptions of any cause, not just runner faults.
>
> A second interruption of the same experiment stops it and returns to me. An operator interruption is an interruption wherever it occurs. Reference and core runs must each use their own process group so an operator or harness interruption cannot be misclassified as a reference crash.
>
> B4 — Harness faults
>
> A process that cannot start, or a failure of the harness itself, is a harness fault and therefore an interruption.
>
> Keep its error and any records already produced. Do not classify it as a reference outcome or retry individual cases independently.
>
> B5 — Build exceeding 600 seconds
>
> A core build exceeding 600 seconds fails the attempt. Record its wall time. It is not an interruption.
>
> This closes the distinction between an unsuccessful build and an interrupted experiment.
>
> ## C — Milestone acceptance: adopt (a)
>
> Ruled: adopt
>
> Section 7 must list the full acceptance obligations, not merely R1–R8.
>
> The list must include:
>
> - R1–R8;
> - R2b, including the correct refusal code and line for every fixture;
> - S1–S4;
> - the do-nothing fixtures;
> - the exit-5 source reading;
> - the `OUT` provenance source reading;
> - the adopted evidence-record requirements, including Y3's conditions 5 and 6, in their previously adopted wording.
>
> Each applicable obligation must be held under its specified repetition requirements.
>
> The sentence that passing these requirements establishes the milestone only remains. Passing them does not authorize production integration, reference-authority transfer, or release.
>
> ## D — Confirm the five additional decisions
>
> Ruled: confirm, subject to D1 measurement
>
> | Item                    | Ruling                                                                                                                                                                                    |
> | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
> | D1 — W14(c) depth bound | Measure the actual front-end expression-depth limit. Keep 130 provisionally until measurement. Then specify and test the actual limit, including cases on both sides of the boundary.     |
> | D2 — Exception type     | Confirm the runner's own `REFERENCE-EXCEPTION module.qualname` line as the adopted exception-type record, replacing E2's earlier traceback-last-line wording. Correct the notes in place. |
> | D3 — Finding count      | Confirm thirteen, not twelve. Correct the count and record the reason.                                                                                                                    |
> | D4 — M3 and W5          | Confirm the literal reading: a rule is named by exactly one arm or `else`, as the row states. Preserve the corresponding line-sensitive refusal behavior.                                 |
> | D5 — Runner edges       | Confirm the three proposed changes below.                                                                                                                                                 |
>
> D1 deserves particular care: the derivation that 99 levels suffice does not itself establish that 99 is the front end's actual limit. The 130 bound remains until that limit is measured. Do not silently substitute 99.
>
> For D5:
>
> 1. Every failure before `reference()` begins is a runner fault, not a reference crash.
> 2. Exit 3 without its required line is a separate anomaly. Stop and report it; do not guess its classification.
> 3. An undefined exit status accompanied by `KeyboardInterrupt` is an interruption.
>
> Also adopt the proposed environment safeguards: record the eight `orlog` modules' SHA-256 values in the ENV line, and check that no `__pycache__` directory stands in `src/orlog` or `research/rust-core`.
>
> The existing 632 recorded reference crashes do not need reclassification based on these changes: the reported evidence establishes that none has the newly specified exceptional cases.
>
> ## E — Four ambiguous format readings: adopt all four recommendations
>
> Ruled: adopt
>
> E1 — Declaration numbering
>
> The \\(i\\)-th declaration encountered in the walk has ID \\(i\\), including variables, claims, and musts. Do not count distinct IDs to determine the next ID.
>
> E2 — Rule typing and W9
>
> A rule's type is fixed by its first `define`, wherever its use occurs.
>
> Each part of W9 is checked once its own inputs are derived. Make the underived list exhaustive. A first definition that uses its own rule leaves the type underived; the relevant use remains W10.
>
> E3 — Claims and musts
>
> Claims' and musts' IDs are governed by W8, as the checker currently assumes and the row specifies.
>
> E4 — Operation count
>
> The operation count is unbounded, as in the reference. Do not saturate at \\(2^{64}-1\\).
>
> The core must preserve the reference's counting semantics. The absence of a practical run reaching that value within the fixed time limit does not authorize a different semantic rule.
>
> These are format/checker clarifications. The reported measurements show that none changes a plant, corpus law, or R6 verdict, but that does not make the clarifications optional.
>
> ## F — Future remakes and REREAD-8
>
> Ruled: adopt F1(a) and F2
>
> F1 — Measurement-based concurrency
>
> Adopt four workers per generation, with the two independent generations running concurrently, as the initial configuration.
>
> Record for each generation:
>
> - wall time;
> - CPU time;
> - peak host memory/commit;
> - worker count;
> - process-start failures and interruptions.
>
> Workers may be increased only while no run exceeds 45 seconds and no process fails to start. The 45-second threshold preserves margin below the 60-second reference limit.
>
> If a process cannot start, treat it as a harness fault under B4. Do not silently reduce workers and continue a partial experiment. Repeat the complete affected generation under the corrected configuration.
>
> The 16 logical CPUs do not establish that 16 workers are safe. The measured process and memory limits govern.
>
> F2 — REREAD-8
>
> Use three parallel readers again:
>
> 1. format and checker;
> 2. protocol, runner, and evidence;
> 3. rulings and cross-document consistency.
>
> Each reader gets its own scratch folder and independent brief. Reports must remain outside the reviewed folder until all three readers have finished. Reader 3 owns cross-document consistency and must compare the actual adopted option text, not merely summaries of rulings.
>
> Merge the findings into one disposition, retaining each finding's reader and provenance and explicitly resolving overlaps. Any hash closure must be completed before declaring the reread complete.
>
> ## Authorization and next work
>
> The following work is now authorized:
>
> 1. Draft 8, applying every DRAFT disposition and these A–F rulings.
> 2. Corresponding amendments to the checker, `plant_reverts.py`, `ref_run.py`, `ref_run_paths.py`, and `gen_r6_reference.py`.
> 3. SHEET.md Amendment 7, including the complete acceptance list and the newly specified evidence-record rules.
> 4. The in-place notes and corrections to RULINGS.md and the historical disposition notes.
> 5. Regeneration of the evidence records under B and F, including the new `r6-reference-4.txt`, with its runner/generator provenance and hash closure.
> 6. A fresh independent reread under F2.
>
> The disclosed failure to retain the interrupted generation's partial records remains a protocol violation to correct in the generator. It does not, by itself, invalidate the completed record whose two successful generations were reported byte-identical and whose hash closure passed. Preserve the disclosure; do not rewrite the historical account as though the interrupted run had retained records.
>
> Still not authorized:
>
> - Rust-core implementation.
> - Production integration.
> - Replacement of Python as reference authority.
> - Gate or release changes outside their own authorization.
> - Commit or push.
>
> Final ruling: A–F are adopted as stated above. Proceed with Draft 8 and the corresponding Phase 0 corrections and evidence work. The next decision point is the fresh reread—not implementation.

**As kept.**
- **The same message carried a second pasted text**, proposing that every experiment attempt get a durable,
  append-only attempt record. It speaks as a proposal (*"I would add"*) and is not recorded here as his ruling; it is
  put to him. What it asks lies within what he ruled here: B4's *"Keep its error and any records already produced"*,
  B2's retained counts and causes, and X10's correction of the generator. The generator meets those by such a record.
- **D1:** 130 stays until the front end's limit is measured; draft 8 says what was measured and what follows.
  *[Note 2026-10-31 (REREAD-8's ZC2, REREAD-9's NC4, his D4): draft 8 said what was measured, not what follows
  from it; the bound's second step was neither done nor brought back (ZC2).]*

## The R6 remake: the two generations one after the other, once (2026-10-30)

He was put the remake of `r6-reference-4.txt` (SHEET.md Amendment 7): two generations made at once, four workers each,
both completed, not byte for byte equal. Mutant 09729 crashed with `TypeError` in generation 1 and `MemoryError` in
generation 2. Three ways on: (a) a declared memory limit for each reference run, (b) the generations one after the
other, (c) a crash's type left out of the comparison. His ruling, whole:

> I recommend (b): remake the two generations sequentially, with four workers per generation. I approve that as a narrow, one-time exception to F1 for the next reference-record attempt.
> The evidence now argues against concurrent generations:
>
> * They took 3,931 seconds, versus 3,425 seconds for the earlier sequential remake. There was no demonstrated speedup.
> * The two concurrent generations overlapped on mutant 09729. Its measured standalone peak was 24.06 GiB; two such runs would require 48.1 GiB, exceeding the host's 47.6 GiB commit limit.
> * The resulting `TypeError` versus `MemoryError` is not an acceptable byte-identical result. Sharing the same `NO-REFERENCE-RESULT` classification does not cure the discrepancy.
> * A memory cap is not yet justified. We have one measured peak, not evidence for a cap that reliably produces the same Python-level outcome rather than process termination. It would also change the reference conditions and apparently change 09729's recorded outcome.
>
> Ruling: R6 remake
>
> 1. The concurrent attempt fails verification. Both generations completed, but their outputs differ. Neither generation is selected as the authoritative record, and neither is silently repeated under B2.
> 2. For the next attempt only, supersede F1's concurrent-generation instruction. Run generation 1 to completion with four workers, then generation 2 with four workers. Keep the same runner, generator, inputs, environment, and worker configuration.
> 3. Do not run readers or other heavy jobs alongside either generation. Record host commit usage before, during, and after each generation, and record per-mutant start/end times so overlap and resource contention can be established rather than inferred.
> 4. If either generation has a harness fault or interruption, apply the existing B2/B3 rules. If both complete but differ, the attempt fails verification again: do not select one, normalize exception types, or discard the differing row.
> 5. Only a byte-identical pair may proceed to hash closure and REREAD-8.
>
> This does not establish that sequential execution guarantees identical results under every host condition. It removes the specific demonstrated cross-generation memory collision while preserving the four-worker setting and the existing reference runner.
> Why I reject the memory-cap option for now
> A cap would introduce a new resource condition into the reference experiment. Choosing it from the 24.06 GiB observation alone would be premature, and a cap-induced `MemoryError` would be a changed reference outcome, not a faithful reproduction of the prior `TypeError`. If sequential runs still disagree, then we can investigate a controlled resource boundary with dedicated measurements and a separate ruling.
> Scope: This exception applies only to the next R6 remake. It does not generally repeal F1's concurrent-generation rule for future experiments. Draft-8 evidence remains as reported; REREAD-8 waits for a verified reference record and hash closure. Nothing is committed or promoted by this ruling.
> The important principle is that byte identity is the acceptance condition, not a preference that can be waived because both outcomes share a broad classification.

**As kept.**
- **The generator** changes only where this ruling asks or its scope requires; a run is made as before (its command,
  environment, limit, budget and workers, and the cases' order). The changes:
  - the experiment is named `r6-reference-5`. The attempts of `r6-reference-4` stand completed (B2), and the generator
    refuses any attempt after a completed one, so the next attempt is an experiment of its own;
  - generation 2 starts only once generation 1 has completed (his 2);
  - each run's start and end, and the host's commit before, during and after each generation, are kept in the attempt
    record (his 3);
  - each generation's file is written outside the tracked files, and the record only when both generations completed
    and are byte for byte equal (his 1 and 5: no generation is selected).
- **His 3, "other heavy jobs":** nothing is run beside either generation but edits of the documents and reading.
- **The attempt-record proposal** that came beside the A-F ruling is still put to him; this ruling does not answer it.
  *[Note, 2026-10-30: he answered it later that day with ATTEMPT-RECORD-0, below.]*

## ATTEMPT-RECORD-0: an append-only record for every remaining Phase 0 attempt (2026-10-30)

He ruled on the attempt-record proposal that had come beside his A-F ruling, and that the R6 remake's section left put
to him. He ruled it while REREAD-8's three readers were at work, and asked that it be recorded only after the re-read;
it is recorded here after all three had finished and reader 2's hash closure had passed. His ruling, whole:

> I adopt the append-only attempt-record invariant, with one scope qualification: it applies to every remaining LAW-FORMAT-0 Phase 0 experiment attempt, not automatically to every future harness in the project.
> Ruling: ATTEMPT-RECORD-0
> Every experiment attempt must have a durable, append-only record that:
>
> 1. Is created before execution begins, so even a process-start failure leaves evidence.
> 2. Identifies the experiment and attempt, including `retry_of` where applicable.
> 3. Records the frozen inputs, source hashes, command, environment, and worker configuration.
> 4. Records start and end times and per-run completion.
> 5. Preserves raw output and diagnostics produced, including partial output from interrupted attempts.
> 6. Records the terminal disposition and the reason for any interruption or failure.
>
> The record must never erase or overwrite evidence from an earlier attempt. Completed attempts remain distinguishable from partial or interrupted attempts. Only completed attempts satisfying their stated acceptance conditions count toward acceptance. An interrupted attempt remains inspectable but cannot be promoted to a completed result.
> This is an evidence-provenance rule, not a new outcome category or a change to B2/B3. It does not authorize retries beyond those rules.
> Application to the current work
> The R6 generator already implements the central invariant, so this ruling does not require changing its pinned implementation or restarting REREAD-8.
> Do not modify any pinned REREAD-8 inputs while the readers are working. Record this ruling in the next appropriate amendment or ruling record after the current reread is complete, then include it in subsequent Phase 0 experiment protocols.
> The R6-5 result is encouraging: the two generations are byte-identical, 09729 agrees, and the measured sequential gap establishes no overlap. But the 2.32 GiB remaining commit headroom is narrow; Amendment 7's qualification that heavier concurrent load could change the outcome should remain.
> REREAD-8 remains the next gate. I would not add further process rules until its three reports and proposed disposition are available.

**As kept.**
- **Scope:** every remaining LAW-FORMAT-0 Phase 0 experiment attempt, not every future harness in the project. It is
  an evidence-provenance rule: no new outcome, no change to B2 or B3, and no retry beyond them.
- **Nothing pinned changed while the readers worked.** The generator (`cc63252d…`) is not changed for this ruling, and
  REREAD-8 is not restarted.
- **The generator's edges against the six points** (its record begun after one child process, a harness exception kept
  by its type alone, a start-failure count that stops at one, the environment's `PYTHONUTF8` unrecorded) go to him in
  REREAD-8's disposition, beside the readers' ZB1 and ZB6. This ruling changes nothing in the generator.
- **Amendment 7's qualification stays:** the 2.32 GiB of commit left at 09729's peak, and that a heavier load beside it
  could change its outcome.
- **Further process rules** wait for REREAD-8's three reports and its proposed disposition (his last sentence).

## REREAD-8's dispositions ruled, G to L (2026-10-30)

He was put REREAD-8's disposition (REREAD-8-DISPOSITION.md): 34 findings, six questions, G to L. His ruling, whole:

> I would resolve G–L as follows. The central principle is that the checker must implement the adopted wording, not a more permissive interpretation that happens to pass the existing corpus.
>
> ## G — E2 self-reference
>
> Adopt
>
> If a rule's first `define` uses that same rule, its type is underived. It does not acquire a type from the expression's apparent form. The checker must report W10.
>
> This resolves the contradiction in Draft 8 section 8 in favor of the adopted E2 ruling.
>
> Also correct the other E2 departures:
>
> - ZA1: use the actual first `define`, not the first define whose type can be inferred. The checker must not fall back to a later definition.
> - ZA3: a `promote` must receive its own applicable type checks even when the surrounding expression's type is unknown.
> - ZA4: do not leave the W9 per-part checks to checker interpretation. Their exact parts must be stated in the format document.
>
> The four-clause crash must also be fixed. These are checker corrections, not new language rules.
>
> ## H — W14(c)
>
> Adopt provisionally
>
> Set W14(c) to 91 in Draft 9, not 90.
>
> The important distinction is:
>
> - Measured: the front end accepts a law with a 91-deep line.
> - Reasoned: the front end cannot produce a line deeper than 91.
>
> The first is established; the second is not yet established independently. REREAD-9 must actively try to produce a valid front-end law with a line deeper than 91.
>
> Until that challenge is complete, 91 is the candidate limit, not a proven maximum. If REREAD-9 finds a deeper valid line, return the matter for a new ruling. Do not silently increase the bound or reject the counterexample.
>
> ## I — Acceptance list and evidence
>
> Adopt
>
> Correct section 7 so that:
>
> 1. Every acceptance item has an explicit repetition requirement. Do not leave the reader to infer which tests repeat.
> 2. Every adopted evidence-record requirement is named, not merely conditions 5 and 6.
> 3. The actual inputs and outputs are retained alongside their hashes.
>
> The compressed storage proposal is acceptable if it preserves the actual contents losslessly and the evidence can be independently recovered and checked. Hashes establish identity; they do not substitute for retaining the evidence.
>
> This is a documentation and evidence-retention correction, not an expansion of the runtime format.
>
> ## J — Runner
>
> Adopt with qualification
>
> Leave the runner unchanged for `r6-reference-5.txt`. Its hash is pinned, the remake is complete, and changing it now would require a new reference-record experiment. The two reported edge cases do not change any row in this record.
>
> But this is not a ruling that the runner satisfies every possible D5 failure path. In particular, the uncaught `SystemExit` case remains a documented limitation. Do not describe it as covered or resolved.
>
> If a later Phase 0 experiment relies on the runner handling every pre-reference failure as a runner fault, that limitation must be resolved before relying on that claim. No silent reclassification.
>
> ## K — F1 and worker limits
>
> Adopt
>
> Add the sentence:
>
> > The measured process and memory limits govern.
>
> The generator must report what it actually checks when deciding whether workers may increase. It must not report that workers may rise merely because a time threshold was met while ignoring memory.
>
> No numeric memory cap is authorized. The R6-5 result gives us a measured peak and headroom, not a generally safe concurrency threshold.
>
> ## L — Additional confirmations
>
> L1 — Generator changes:&#x20;
>
> Confirm
>
>
>
> Accept the statement that the generator was changed only as required to carry out the one-time sequential remake ruling, subject to the recorded diff and test evidence. This does not authorize unrelated generator changes.
>
> L2 — Module hashes:&#x20;
>
> Confirm with clarification
>
>
>
> “Eight modules” means every applicable `orlog` module is hashed. The number is not a fixed requirement for every mode: law mode loads and hashes five. The record must identify the actual modules and hashes for that run.
>
> L3 — W9 split:&#x20;
>
> Do not confirm yet
>
>
>
> The checker’s current split cannot become authoritative merely because it is implemented. Reader 1 specifically found that Draft 8 does not enumerate the parts, leaving the checker’s split unsupported.
>
> Write down the exact W9 parts and their individual type checks in Draft 9. Then independently verify that the checker implements that enumeration. Bring back any ambiguity rather than resolving it by implementation convention.
>
> ## Scope and next gate
>
> The resulting disposition is:
>
> | Ask | Ruling                                                             |
> | --- | ------------------------------------------------------------------ |
> | G   | Adopt                                                              |
> | H   | Adopt provisionally at 91; REREAD-9 must challenge the upper bound |
> | I   | Adopt                                                              |
> | J   | Leave the pinned runner unchanged; retain the limitation           |
> | K   | Adopt                                                              |
> | L1  | Confirm                                                            |
> | L2  | Confirm with clarification                                         |
> | L3  | Withhold confirmation pending explicit W9 enumeration              |
>
> For Draft 9, the authorized work is limited to these corrections, the checker changes required by G and L3, and the corresponding evidence and documentation updates.
>
> Do not begin REREAD-9 until the checker follows E2 literally, the W9 parts are explicit, the section 7 acceptance list is complete, and the 91-depth challenge is prepared. REREAD-9 must independently challenge the 91 bound rather than merely reproduce the argument for it.
>
> No Rust-core implementation, production integration, authority transfer, release change, commit, or push is authorized.

**As kept.**
- **His scope:** *"For Draft 9, the authorized work is limited to these corrections, the checker changes required by G
  and L3, and the corresponding evidence and documentation updates."* The disposition's DRAFT items that none of G to L
  carries (among them ZA5's E1 plants, ZA6, ZA7, ZA9, ZB3, ZB5, ZB7, ZB8, ZB12, ZC5, ZC6 and ZC12) are not read into
  it; they are put to him.
- **K and the generator:** the generator that made `r6-reference-5.txt` stays as it is, pinned by the record's header
  (ATTEMPT-RECORD-0; his J for the runner, alike). His K binds the next generator, as option (a) said; Amendment 8
  notes that the present one's `workers may rise` reports his two time and start conditions alone.
- **L3:** the checker's split is not written down as the enumeration. Draft 9 enumerates W9's parts from the rules'
  own words; where they do not decide a part, it is brought back to him, and the checker is then held to the
  enumeration by a reading made independently of it.
- **REREAD-9** does not begin until his four conditions hold.
- The paste holds three HTML references for a space (`&#x20;`), kept as they came; Markdown shows each as a space.

## The ruling sheet of 2026-10-31 ruled: W9's (A) to (D), the six files, the remaining items, the debate (2026-10-31)

He was put a message describing `research/RULING-SHEET-2026-10-31.md` (PROPOSED), kept word for word in
`messages/2026-10-31-put-for-the-sheet-ruling.md`. His ruling, whole: *[Corrected 2026-10-31 (REREAD-9's NC7,
his D6): this said he was put the sheet itself; he ruled on the message's descriptions.]*

> My ruling is to accept most of the proposed corrections, with two important qualifications: (C) must explicitly preserve the distinction between variable typing and rule typing, and option (c) for the six files must prove exact reversibility rather than merely claim it.
>
> I would issue the following dispositions.
>
> # Ruling on RULING-SHEET-2026-10-31
>
> ## I. W9: A–D
>
> | Item | Ruling                                                                       | Reason                                                                                                                           |
> | ---- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
> | A    | Adopt                                                                        | Apply the words actually specified for `neg`, `abs`, and `sqrt`. Do not add an inferred numeric-type requirement.                |
> | B    | Adopt                                                                        | Interpret “one numeric type” as a requirement on the operand pair, with kind checked together with equality.                     |
> | C    | Adopt the checker’s current variable convention, with an explicit amendment. | Variables have their own numbering and scope under E1/W8. Their treatment need not inherit E2's first-definition rule for rules. |
> | D    | Adopt                                                                        | Retain first declaration encountered, consistent with E1's numbering convention.                                                 |
>
> ### C — exact limitation
>
> The ruling must explicitly say that:
>
> - Variable typing follows the variable's declaration and scope as encountered by the prescribed walk.
> - Rule typing continues to follow E2: the first `define` determines the rule's type, even if that type is underived.
> - The variable convention does not establish a general order-free or least-fixed-point typing system.
> - The 83-mutant result is evidence against adopting the alternative literal reading without a separately specified termination and fixed-point contract.
>
> I accept the measured distinction as a reason to reject the alternative for this amendment. I do not accept the checker under test as the authority for its own correctness. The independent verifier's finding must remain the source of the discrepancy, and the corrected checker must be independently checked against the amended wording.
>
> A and B reportedly move no existing verdict. That is useful regression evidence, not proof that their interpretations are correct.
>
> ## II. Six files containing home paths
>
> Conditional adoption
>
> I prefer option (c), but only under these conditions:
>
> 1. Every spelling of the home-path prefix receives an unambiguous token, including the short 8.3 AppData form.
> 2. Restoration accepts the exact corresponding prefixes as explicit inputs. Do not assume the short alias can be regenerated from the long path.
> 3. Replacement is byte-preserving outside the matched prefix.
> 4. The restored six files must match their original SHA-256 hashes.
> 5. Missing, ambiguous, or incorrect restoration inputs must cause failure.
> 6. Plants must cover every spelling, partial matches, multiple occurrences, and incorrect restoration inputs.
>
> Retain the original hashes and the transformation procedure. The restored evidence must be byte-for-byte identical.
>
> No use of option (c) until those tests pass. If they cannot be satisfied cleanly, keep the six originals outside the repository. The no-home-path rule takes precedence over convenience.
>
> ## III. Remaining DRAFT items
>
> I would distinguish corrections from new obligations.
>
> - Wording, count, and documentation corrections: adopt where they faithfully implement already-adopted rulings.
> - ZA7 — extend unbounded operation counting to other counters: withhold. This extends a substantive rule beyond the currently established E4 disposition. Bring back the exact counters, their overflow behavior, and witnesses before adoption.
> - ZA9 — confine R7 writer plants to the writer's named code: adopt as a test-scope constraint. A writer plant must actually exercise the named writer implementation; unrelated injected defects cannot count as evidence that the writer test works.
>
> Any remaining DRAFT item that changes checker behavior, acceptance conditions, or language semantics must be separately identified. It cannot enter under the label of a wording correction.
>
> ## IV. Debate dispositions
>
> I retain the earlier proposed dispositions:
>
> - Reject ISPT-0 and archive its reductions.
> - Show GLUE-0 verdicts on admission cards as non-decisional evidence.
> - Authorize the one Verðandi graybox scratch experiment, subject to its sheet and hand predictions first.
> - Keep DOCTRINE fork 9 behind typed terminals and RUST-CORE-0.
> - Defer compositional identity until a composition construct exists.
>
> These do not authorize repository changes or gate rows.
>
> ## V. REREAD-9 authorization
>
> Not yet authorized
>
> REREAD-9 may begin only after:
>
> 1. A–D are incorporated into the exact sheet language.
> 2. The checker implements the adopted C distinction.
> 3. The independent verifier checks that implementation.
> 4. The six-file treatment is resolved and, if option (c) is used, passes its restoration plants.
> 5. Every remaining DRAFT item has an explicit disposition.
> 6. The 91-depth challenge and all existing REREAD-9 prerequisites are ready.
>
> No implementation outside that scope, no Rust-core work, no production integration, no gate changes, no commit, and no push.
>
> One qualification about this ruling: I am ruling on the exact descriptions and measured consequences supplied in your message, not certifying the unseen contents of `RULING-SHEET-2026-10-31.md`. The final sheet must preserve these dispositions without silently broadening them.
>
> The most important decision is C: variable typing follows its own established walk and scope; rule typing retains E2's first-definition convention. That resolves the apparent inconsistency without introducing an unbounded fixed-point mechanism into Phase 0.

**As kept.**
- **His qualification** stands over the sheet: he ruled on the descriptions and measured consequences put to him, and
  the sheet's wording preserves his dispositions without broadening them.
- **(C)** is written into draft 9 with each of his four points, and the corrected checker is checked against the amended
  wording by the reading made independently of it, never by the checker itself.
- **The six files** stay outside the tracked tree until option (c) passes its restoration plants; if it cannot, they
  stay outside.
- **The remaining items:** the wording, count and documentation corrections are applied where they implement adopted
  rulings. Every item that changes a checker's behaviour, an acceptance condition or the language's semantics is named
  apart, and waits. ZA7 is withheld, ZA9 adopted as he scoped it. *[Note 2026-10-31 (REREAD-9's NC5, his D10):
  ZA5's six plants did not wait. They were applied in Amendment 9, named apart, before his disposition, and he then
  kept them as test additions (his ruling on ZA5).]*
- *[Note 2026-10-31 (REREAD-9's NC8, his D11): his IV authorized one Verðandi graybox scratch experiment, its sheet
  and hand predictions first. Two decisions are his before it runs: whether the Python twin alone is enough, and
  whether fixtures the exporter would refuse are acceptable. The rulings since leave both open. On the card, his
  ruling on REREAD-9's ASK 9-6: GLUE-0 verdicts may be shown as non-decisional evidence, as IV says, and no card
  work is authorized by that alone.]*
- **The debate:** "Show GLUE-0 verdicts on admission cards as non-decisional evidence" is recorded as the rule that a
  glue verdict never decides an admission. Showing it on a card would be a change to Verðandi's studio, and his section
  IV says these dispositions *"do not authorize repository changes or gate rows"*, so no card is built until he says
  so. The Verðandi experiment's sheet and hand predictions come first, in scratch.
- **Beside his ruling** came two pastes that are not rulings: a commentary on what the surviving composition work could
  give a user, and a proposed execution protocol, RDE-0, recommended for a pilot on the remaining Phase 0 work. Neither
  is recorded here as his ruling.

## R1 and R4 confirmed as the corrected checker reads them (2026-10-31)

The re-verification of W9 at his rulings (`W9-VERIFICATION-REPORT-2.md`) brought back two questions, each with its
witness in draft 9: R1, whether scope in his (C) makes an out-of-scope variable's type underived; and R4, whether a
second `let 0` declares variable 1. He was asked to confirm both as the corrected checker reads them. His ruling, whole:

> Yes. Confirmed: R1 and R4 are to be resolved as the corrected checker currently reads them, with the following exact qualifications.
>
> ### R1 — Declaration typing versus scope
>
> Confirm. Type derivation follows the declaration encountered by the checker. Scope is a separate validity question, checked under W8.
>
> Therefore, an out-of-scope variable can still have a derivable type. Its out-of-scope use is not converted into an underived-type result merely because the scope check fails.
>
> To avoid ambiguity, read my earlier phrase “declaration and scope” as describing two distinct checks—not as making scope a prerequisite for type derivation.
>
> ### R4 — Repeated declaration ID
>
> Confirm. The identifier written in the declaration is authoritative; declaration order does not renumber it.
>
> A second `let 0` is another declaration of variable 0, not an implicit declaration of variable 1. Variable 1 remains undeclared unless explicitly declared.
>
> These confirmations settle R1 and R4 only. They do not authorize REREAD-9, the Verðandi experiment, ZA5, or the runner changes ZB3/ZB5. Those remain separate decisions. Nothing here authorizes a commit.

**As kept.**
- **R1:** a variable's type is the type of its declaration as the walk meets it, in scope at the use or not. Scope is
  W8's question alone. Draft 9's witness stands as the checker reads it: W9 at line 3. It is a plant, and the reading he
  did not choose is an undoing that changes it (`RS-C undone: reading (ii), in scope at the use`).
- **R4:** the id written in a declaration is the id it declares. Section 7's count says which id each declaration
  must carry, and a misnumbered or repeated one is W8's failure; it never renumbers the declaration. Draft 9's witness
  stands as the checker reads it: W10 at line 3. It is not a plant, and none is added without his word.
- **What it does not authorize**, in his words: *"They do not authorize REREAD-9, the Verðandi experiment, ZA5, or the
  runner changes ZB3/ZB5."* The checker is unchanged; draft 9 and SHEET.md (Amendment 10) record the two as ruled.

## ZA5's six plants kept as test additions (2026-10-31)

REREAD-8's ZA5 (reader 1, MINOR): no plant pinned E1 for claims and musts, or W9's parts outside `set` and `change`.
Its disposition proposed the six witnesses planted, each with its undoing (DRAFT). They were applied under his ruling on
the ruling sheet, named apart as not wording (SHEET.md, Amendment 9), and he was asked whether to keep them. His
ruling, whole:

> Yes. Keep ZA5’s six plants as test additions.
>
> The distinction is important: I’m authorizing the six plants to remain as additional test coverage, not adopting a new semantic rule or changing any verdict, acceptance condition, or checker behavior.
>
> Record them as test additions under ZA5, preserving their provenance and their status as non-semantic changes. This does not authorize ZB3, ZB5, the Verðandi experiment, or REREAD-9.

**As kept.**
- **The six plants** stay in `format_check.py`, each named `ZA5: …`, and their six undoings in `plant_reverts.py`,
  `ZA5 undone: …`, as they are: E1 for musts and for claims, counted as met; and W9's parts made alone in `+`, `not`,
  `item` and `list-of`. They are test coverage, under ZA5: they adopt no semantic rule, and change no verdict, no
  acceptance condition and no checker behaviour (MEASURED when applied: no row of R6's 10,000 mutants or R2b's 1,558
  twins moved; Amendment 9).
- **Their provenance:** REREAD-8's ZA5, its disposition's DRAFT, his ruling on the ruling sheet, and this ruling.
- **What it does not authorize**, in his words: *"This does not authorize ZB3, ZB5, the Verðandi experiment, or
  REREAD-9."* Draft 9 and SHEET.md (Amendment 11) record ZA5 as kept.

## ZB3 and ZB5 applied to the runner's check (2026-10-31)

REREAD-8's reader 2 found two gaps in the runner's verification (both MINOR). ZB3: the runner's check,
`ref_run_paths.py`, did not hold the ENV line's completeness, which folders the bytecode check covers, or the
implementation and version; three of the reader's runner changes passed it 43 of 43. ZB5: `ref_run_variants.py` made
four of REREAD-6's five changes, not five. Both were put to him as changes to the runner's test apparatus, named apart
(SHEET.md, Amendment 9). His ruling, whole:

> Yes. Apply both ZB3 and ZB5 to the runner’s check, as recommended.
> Keep the scope strictly to runner verification:
>
> * ZB3: Check that the environment record is complete; plant a bytecode cache in each folder by name; and compare the Python implementation, version, and platform against the runner’s own recorded environment. The runner itself remains pinned.
> * ZB5: Add the fifth REREAD-6 runner check: a run that retains the text-seal line. Record the resulting coverage accurately as 15 of 16, not 16 of 16.
>
> These are runner-check changes, not changes to the checker’s semantics, the reference, or the accepted laws. Re-run the affected evidence under the revised runner and preserve the old records and hashes so the change is auditable.
> This settles ZB3 and ZB5’s disposition. It does not authorize REREAD-9 itself, the Verðandi experiment, ZA7 counter changes, or any commit.

**As kept.**
- **The scope:** the runner's check and its variants, and the evidence they make. The runner, `ref_run.py`, stays
  pinned and unchanged; the checker, the reference and the accepted laws are untouched.
- **ZB5's count** is recorded as he ruled it: 15 of 16, V11 the one change no case of the check reaches.
- **The old records and hashes** stay as they are; the new records are written beside them under new names (SHEET.md,
  Amendment 12).
- **What it does not authorize**, in his words: *"It does not authorize REREAD-9 itself, the Verðandi experiment, ZA7
  counter changes, or any commit."*

## REREAD-9 authorized: three readers, the reports and a proposed disposition back to him (2026-10-31)

He was told that each condition he set for REREAD-9 read as met, ZA7's extension withheld rather than adopted, and
asked whether to begin (the message, word for word: `messages/2026-10-31-put-for-reread-9.md`, kept by his D6). His
ruling, whole:

> Yes. Begin REREAD-9.
> I accept the stated prerequisites as met. In particular, ZA7’s extension being explicitly withheld is a disposition; it does not need to be adopted to close that item for this reread.
> Keep the authorization narrow:
>
> 1. Three independent readers, working in parallel, review Draft 9 and the sheet.
> 2. Preserve each report word for word, with its source hashes and provenance.
> 3. Include the proposed challenge to write a line deeper than 91. Treat the result as evidence about the depth boundary, not permission to change it.
> 4. Do not open `research/law-sufficiency/`.
> 5. Do not change the checker, runner, reference, laws, gate, or release files.
> 6. Bring the reports and a proposed disposition back to me before applying findings.
>
> Keep R4’s witness, ZA7’s counters, and the two Verðandi decisions separate. This authorization does not settle them.
> REREAD-9 is authorized to start. It is not authorization to adopt its findings or commit anything.

**As kept.**
- **The readers:** three, fresh, working at once, each with its own part and letter (NA, NB, NC), seeing nothing of the
  others' work; reader 1 makes the 91 challenge, searching before it reads the argument. They read draft 9 and the
  sheet, never `research/law-sufficiency/`, and change nothing.
- **Nothing pinned changes while they work:** every file a brief pins keeps its sha256 until the three reports are in.
- **The reports** are saved word for word from the readers' own transcripts, each under a header naming its brief's
  sha256, the files it pinned and how it was saved. A deeper line, if one is found, is evidence about the depth
  boundary; in his words, *"not permission to change it."*
- **Then** a proposed disposition goes to him, and no finding is applied before he rules. R4's witness, ZA7's counters
  and the two Verðandi decisions stay apart: in his words, *"This authorization does not settle them."*

## REREAD-9's disposition adopted with qualifications (2026-10-31)

He was put `REREAD-9-DISPOSITION.md` (PROPOSED) and the three reports. His ruling, whole:

> # Ruling on REREAD-9
>
> Disposition adopted with qualifications
>
> I adopt the recommended direction on ASK 9-1 through 9-5, with the scope qualifications below. ASK 9-6 receives separate decisions for each of its five questions. I authorize D1–D12 as documentary corrections implementing these rulings and existing rulings. D13 is deferred until a checker change is independently authorized.
>
> This is not authorization to change checker semantics, the reference, the runner, the laws, the gate, or release files beyond the specific actions stated below. Nothing here authorizes a commit.
>
> ## I. The findings and the 91 bound
>
> The 34 finding labels represent 33 distinct underlying issues because NB1 and NC2 are the same issue. I accept the findings as reported, subject to the dispositions below.
>
> The 91 bound remains REASONED, not proven. The search is substantial: 41 families, approximately 53,900 texts, and 77,000 random and hill-climbed texts, with the deepest reached line at 91. The argument's three steps were also checked against the implementation. That supports the current boundary; it does not establish that no deeper line exists.
>
> The two loosely worded sentences in the argument may be corrected under D2. That correction must not upgrade the epistemic status of the bound or alter the bound itself.
>
> The checker and runner findings are accepted as measurements of the tested versions and conditions. They are not blanket certification of every behavior outside those tests.
>
> ## II. ASK 9-1 — Section 7, item 8
>
> Adopt option (a), with scope clarification
>
> 1\. Evidence-record list: Adopt the amendment-by-amendment enumeration. The list must name every adopted evidence-record requirement, not merely conditions 5 and 6. It must include the requirements identified in the disposition: condition 3, F2, U2, B1, B4, B5, Amendment 2, and R8. The list must identify their actual source amendments and preserve their operative wording. It must not claim completeness until those requirements are all accounted for.
>
> 2\. Environment: Adopt the division of responsibility. The reference process records its environment through its own ENV line. For a core run, the harness records the host platform and the build's `rustc -vV` alongside the run. The core is not required to inspect or report its own environment. This is a harness requirement, not a new core-output requirement.
>
> 3\. ATTEMPT-RECORD-0: Do not extend ATTEMPT-RECORD-0 to the milestone's future core runs. Its adopted scope remains every remaining LAW-FORMAT-0 Phase 0 experiment attempt. Remove the misplaced reference to it from the milestone's item 8. This does not exempt milestone runs from their own evidence-record requirements; it means those requirements must be stated independently rather than attributed to ATTEMPT-RECORD-0.
>
> 4\. Byte identity: Adopt the narrower distinction:
>
> - For core runs, byte identity covers the core's output and each case's class.
> - Reference runs are held by their classes, not by a universal byte-identity requirement for raw output.
> - The 09729 reference runs remain separately held as specified in `r6-reference-5`, because their crash type can vary with available memory.
>
> This resolves the ambiguity without imposing a false reproducibility requirement on the reference's raw crash output.
>
> ## III. ASK 9-2 — Absolute paths in five reports
>
> Adopt option (a), with preservation conditions
>
> Token the five reports using the established reversible token procedure.
>
> The no-home-path rule takes precedence over convenience. The fact that the reports are verbatim records does not authorize leaving account-identifying paths in the repository.
>
> Conditions:
>
> - Preserve the original report bytes outside the repository.
> - Preserve each original's exact length and SHA-256 in the manifest.
> - Make the tokenized copies reversible to the exact original bytes.
> - Clearly distinguish the tokenized repository copies from the original hand-backs. Do not describe the tokenized copies themselves as byte-for-byte originals.
> - Verify restoration against each original hash.
> - Search the whole research tree and `evidence/` for every spelling and form, not merely `kept/`.
> - Preserve the existing REREAD-9 reports unchanged; they contain no such paths.
>
> This is a controlled sanitization of the repository copies, not permission to rewrite the historical reports or alter their findings.
>
> ## IV. ASK 9-3 — W3 and the writer's code
>
> Adopt option (a)
>
> Use R7-A's actual rule:
>
> W3 must be determined by code independent of the writer used to produce `OUT`.
>
> Remove the overbroad phrase “never by writing back.” The checker may use its own independent writer to decide W3. Its result remains evidence, not authority over the rule.
>
> Section 11 should accurately describe what the checker does and why that implementation does not change any verdict. Section 0's source reading should name the writer's code and its relevant lines, so the writer plants have an identifiable implementation target.
>
> Option (b) would create a stricter new core requirement. It is not adopted.
>
> ## V. ASK 9-4 — The runner's check
>
> Adopt option (a), runner pinned
>
> Authorize the runner-check apparatus to be extended. The runner itself remains unchanged.
>
> The revised check must include:
>
> - Exact stdout expectations: the ENV line, after-run line, and outcome.
> - Source checks that reject the prohibited constant strings and dynamic-import routes.
> - Conditions observed from inside the run using the stand-in, rather than inferred solely from the checker's own environment.
> - Explicit cases for K7–K11.
> - Comparison of the ENV line against the recorded `r6-reference-5` line.
> - Recording and checking `sys.pycache_prefix` and `sys.flags`.
> - K1–K11 retained as plants, with the plant count distinguished from the existing 16.
>
> The eleven planted changes must actually be caught by the revised check. The present 46/46 result is not sufficient to claim that the runner's documented prohibitions are enforced.
>
> This is a runner-check change only. Do not edit `ref_run.py` or weaken its pin. Rerun and preserve the evidence under the established record procedure.
>
> ## VI. ASK 9-5 — The keeping tools and their plants
>
> Adopt option (a), test apparatus only
>
> Authorize the proposed changes to the keeping tools and their tests. They do not change any verdict or substantive rule.
>
> Required coverage:
>
> 1. Each spelling gets a same-length wrong-prefix plant, so a length-only comparison cannot pass.
> 2. REL83 and SLUG get partial-match and repeat plants.
> 3. `make` refuses two tokens side by side.
> 4. `check` refuses an unheld NAME.
> 5. Both checks verify the kept file's SHA-256 before decompression and report damage rather than raising an uncontrolled exception. Include a damaged-file plant.
> 6. M10 compares against the actual number of laws read, not a stale constant.
>
> The stale “fell” comparison must be corrected as part of this work. The test must demonstrate that the intended failure condition is meaningful, not merely that a fixed constant happens to compare equal.
>
> ## VII. ASK 9-6 — Decisions previously left unsettled
>
> ### 1. R2 and R5
>
> Defer exact wording
>
> I do not confirm their prior application as adopted wording yet.
>
> The disposition identifies the subjects but does not reproduce the exact proposed sentences. R2 concerns the cycle sentence for derivation 17; R5 concerns when `change`'s numeric part is made with an index. R5 in particular may determine a substantive interpretation, even if the verifier found no verdict dependent on it.
>
> Record that these were applied without my disposition. Bring back the exact R2 and R5 wording, with the relevant L3 context, before treating either as adopted. Until then, neither is an independently adopted rule.
>
> ### 2. NA6's two places
>
> Adopt the explanatory clarification
>
> Record the checker behavior:
>
> - The promote's place part is made even at a slot with no element type; the checker then fails it.
> - The place-3 “at least one item not a promote” condition is checked on the list as a whole, not separately for each promote.
>
> State that these are descriptions of the measured checker behavior and that no verdict changes. Do not turn this clarification into a new semantic requirement.
>
> ### 3. J's harness sentence
>
> Confirm adopted
>
> The sentence is adopted:
>
> > Any harness that classes runs, the core's included, refuses a run without the runner's ENV line, as the generator does.
>
> Clarification: the harness is responsible for obtaining and recording that line. This does not require the core to emit or inspect its environment. It is consistent with the ASK 9-1 division of responsibility.
>
> ### 4. “Against the runner's own recorded environment”
>
> Confirm the recorded-baseline reading
>
> The comparison is against the ENV line recorded by `r6-reference-5`, not merely against whatever environment happens to exist when the check is run.
>
> A fresh interpreter comparison is useful additional evidence, but it is not a substitute for the pinned recorded baseline. ASK 9-4(a)'s explicit comparison to that baseline is therefore required.
>
> ### 5. GLUE card
>
> Confirm the non-decisional interpretation
>
> GLUE-0 verdicts may be shown on admission cards as non-decisional evidence, as IV says. They do not decide admission, create gate rows, or authorize repository changes.
>
> The disposition's restraint is correct: no additional card implementation or repository work is authorized by this clarification alone. The stated display authorization does not become authority to change the gate.
>
> ## VIII. The DRAFT corrections
>
> I authorize the following documentary corrections:
>
> | Item | Ruling                                                                                                                                                                                                                                                                                                                                                                                     |
> | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
> | D1   | Adopt. Cite the `-9-zb` records as the current evidence and retain the `-9` records as history.                                                                                                                                                                                                                                                                                            |
> | D2   | Adopt. Correct the third step's wording without changing the 91 bound or its REASONED status.                                                                                                                                                                                                                                                                                              |
> | D3   | Adopt. Correct five RS undoings, 0 of 305, and the 29 kept-file count, with its explanatory note.                                                                                                                                                                                                                                                                                          |
> | D4   | Adopt. Restore the missing ZB4 and ZC2 notes in the specified locations.                                                                                                                                                                                                                                                                                                                   |
> | D5   | Adopt. Record all six REREAD-9 conditions and the evidence supporting each; ensure Draft 9 names all six.                                                                                                                                                                                                                                                                                  |
> | D6   | Adopt. Correct the description of what I ruled on and preserve the two source messages word for word beside `RULINGS.md`.                                                                                                                                                                                                                                                                  |
> | D7   | Adopt. Correct the quotation's provenance and the punctuation discrepancy as described.                                                                                                                                                                                                                                                                                                    |
> | D8   | Adopt. Record the `SystemExit` limitation accurately. Keep the runner pinned; do not claim the limitation is covered or resolved.                                                                                                                                                                                                                                                          |
> | D9   | Adopt with a limitation. Preserve the nine recoverable items and the two rebuilt manifests with their verified hashes. Record the two missing verifier-input drafts by their known hashes and explicitly say their bytes were not recovered. Do not imply that a hash alone preserves their contents. From this point forward, preserve every hash-identified input before overwriting it. |
> | D10  | Adopt. Record that ZA5 was applied before my disposition and that I subsequently retained it. Do not conceal the sequence.                                                                                                                                                                                                                                                                 |
> | D11  | Adopt. Record the limited Verðandi authorization and identify the two decisions that remain mine. Do not decide them here.                                                                                                                                                                                                                                                                 |
> | D12  | Adopt. Record the `--checker` moved-HEAD limitation; keep the tool pinned as specified.                                                                                                                                                                                                                                                                                                    |
> | D13  | Defer. Correct the checker comment only at a future checker change that I separately authorize. No checker change is authorized by this ruling.                                                                                                                                                                                                                                            |
>
> NA5 remains with the withheld ZA7 bring-back. Include the stop's printed count among the matters to be addressed when ZA7 is brought back. Do not open or resolve ZA7 now.
>
> ## IX. The two process disclosures
>
> Both disclosures must remain in the record.
>
> 1. Reader 1's access to working notes: The notes contained no information about the 91 bound or its argument, which supports the conclusion that the depth search was not primed by them. But the reader did access material outside its brief, and its search was not fully isolated from project history. Record both facts. Future briefs must forbid access to the agent environment's working notes and summaries by name.
> 2. Reader 3's temporary report placement: Record that the report briefly stood in `research/rust-core/` while the other readers were still working, and was moved out. The later search finding no exposure is relevant, but does not erase the placement.
>
> These disclosures do not, on the evidence presented, invalidate the three reports or the measured hash closure. They do qualify the provenance description and must not be omitted from the permanent record.
>
> ## X. Scope and authorization
>
> The following work is authorized:
>
> - Apply ASK 9-1 through ASK 9-5 as ruled above.
> - Apply the five ASK 9-6 decisions as ruled, except R2 and R5, which remain deferred.
> - Apply D1–D12, subject to D9's explicit unrecovered-input limitation.
> - Preserve the two process disclosures.
> - Keep NA5 with ZA7's withheld bring-back.
>
> The following remain outside this authorization:
>
> - R4's witness as a plant.
> - ZA7's counters and stop-count clarification.
> - The two Verðandi experiment decisions.
> - D13's checker-comment edit.
> - Any checker, runner, reference, law, gate, or release change not expressly authorized above.
> - Any commit or push.
>
> Final status: REREAD-9's findings are accepted as findings; the disposition is adopted with the qualifications above. The 91 bound remains reasoned. The five path-bearing reports are to be reversibly tokenized for repository storage, with their originals preserved outside the tree. Documentary corrections D1–D12 are authorized; D13 and the R2/R5 wording are not. Nothing is to be applied or committed beyond those boundaries.

**As kept.**
- **ASK 9-1 to 9-5:** the recommended options, with his scope qualifications: item 8's records named amendment by
  amendment; a core run's environment recorded by the harness, never by the core; ATTEMPT-RECORD-0 not extended to the
  milestone's runs, its reference removed from item 8; byte identity for a core run's output and each case's class,
  the reference's runs held by their classes and 09729 as in `r6-reference-5`. The five path-bearing reports tokened,
  their originals kept outside the tree. W3 in R7-A's words. The runner's check extended, the runner pinned. The keeping
  tools' plants extended, and M10 fixed.
- **ASK 9-6:** R2 and R5 deferred, their exact wording to be brought back with L3's context; NA6 recorded as the
  checker's measured behaviour, no new rule; J's harness sentence adopted; the recorded-baseline reading; the GLUE card
  non-decisional, no card work authorized.
- **D1 to D12** authorized, D9 with his limitation; **D13** deferred; NA5 kept with ZA7's withheld bring-back.
- **Draft 9, not a draft 10.** The disposition proposed a draft 10. The checker reads draft 9 by name
  (`format_check.py`'s `main`), and he authorized no checker change, so the corrections are made in draft 9, each with
  a dated note.
- **Outside it,** in his words: *"Any commit or push."*, and R4's witness, ZA7's counters, the two Verðandi decisions,
  D13, and any change he did not expressly authorize.

## The ten older reports tokened as the five were (2026-10-31)

The search his ruling on REREAD-9's ASK 9-2 required found ten more reports in the research tree that name his
account, REREAD-1 to REREAD-7's. His ruling had named five, so they were put to him, untouched. His ruling, whole:

> Yes. I authorize tokenizing the ten older reports (REREAD-1 through REREAD-7) under the same procedure adopted for ASK 9-2.
> The authorization is limited to those ten reports and their account-name references. Apply these conditions:
>
> 1. Preserve each original unchanged, outside the repository, in the ignored originals location. Do not overwrite or discard it.
> 2. Create tokenized copies in `kept/`, using the established reversible tokenization procedure. Mark each copy clearly as a tokenized copy, not the original hand-back.
> 3. Record each original’s byte length and SHA-256 in the manifest. Keep the mapping needed for restoration with the preserved originals.
> 4. Restore each tokenized copy and verify byte-for-byte identity against its original.
> 5. Search the full research tree and `evidence/` for every spelling of the account name, including the tokenized copies and any newly exposed references.
> 6. Report the exact file count, restoration results, search results, and any exceptions. Do not silently expand the scope to other reports or files.
>
> This is a reversible privacy-preservation correction, not a change to the reports’ evidentiary status, findings, or wording. It authorizes no checker, runner, reference, law, gate, or release changes, and no commit or push.
> Bring back the results before treating the ten reports as fully handled.

**As kept.**
- **The scope:** those ten reports and their account-name references, nothing else; in his words, *"Do not silently
  expand the scope to other reports or files."*
- **The procedure** is ASK 9-2's: originals unchanged in `work/rust-core/originals/`; tokened copies kept in `kept/`
  and named in `kept/TOKENED.txt` by each original's length and sha256; each repository copy marked as a tokened copy;
  each restored and compared byte for byte; the whole research tree and `evidence/` searched.
- **The restoration map,** each token with its prefix, is kept beside the preserved originals, in the ignored
  `work/rust-core/originals/`, never in the tracked tree, as he asked: *"Keep the mapping needed for restoration with the
  preserved originals."*
- **Not yet fully handled:** the results go back to him first (SHEET.md, Amendment 14).

## The ten reports accepted as handled; the commit roadmap (2026-10-31)

He was given the ten reports' results (SHEET.md, Amendment 14) and asked whether to accept them as handled. He also
answered what is left before the next commit. His ruling, whole:

> Yes. I accept the ten older reports' results as handled, on the evidence you have reported.
>
> The preservation procedure satisfies the conditions of my authorization:
>
> - Exactly ten reports were handled, with no additional files touched.
> - Originals remain unchanged in the ignored originals directory.
> - All ten restore byte-for-byte from the restoration map alone.
> - All 24 tokened files, including their prefixes, restore exactly.
> - The 17 path occurrences are accounted for: nine long-form and eight short-form.
> - The full search covered 706 file views, including decompressed tokened copies, and found no remaining account-name occurrences in `research/` or `evidence/`.
> - No exceptions were reported.
>
> Amendment 14 records the result. This closes the ten-report follow-up; it does not change the reports' evidentiary status or authorize any broader work.
>
> ## Does the commit roadmap change?
>
> Yes. Lane A is complete. The roadmap can now move to commit-scope review. But there is an important issue in the inventory you reported.
>
> Reported commit inventory
>
> # 154 files
>
> 28 MB · all untracked · nothing tracked modified
>
> | Location                    | Files |
> | --------------------------- | ----- |
> | `research/rust-core/`       | 82    |
> | `research/law-sufficiency/` | 22    |
> | `evidence/`                 | 49    |
> | Ruling sheet                | 1     |
> | Total                       | 154   |
>
> The 22 files under `research/law-sufficiency/` are a scope concern. The REREAD-9 authorization expressly excluded that directory. The fact that those files are untracked, searched, or included in the inventory does not authorize committing them. Keep them out of the proposed commit unless you establish that they are independently authorized under a separate decision.
>
> The 49 evidence records also need to be mapped to the specific adopted requirements or authorized follow-ups they support. In particular, preserve the distinction between current records and historical records; do not include something merely because it is present.
>
> ## Revised roadmap
>
> 1.
>
>    Accepted
>
>    &#x20;Ten-report preservation. Closed under Amendment 14.
>
> 2. R2 and R5. Your decision is still needed. You may adopt both, reject either, or leave them explicitly unadopted in the commit. My recommendation is to rule on them first, so the committed record does not carry avoidable ambiguity.
>
> 3. Commit inventory audit. Produce a path-by-path list of the 154 files, their purpose, and the authorization supporting their inclusion. Separate the 22 excluded-directory files.
>
> 4. Reconcile the documentary record. Confirm Amendment 13, Amendment 14, `SHEET.md`, and `RULINGS.md` agree, including the R2/R5 status.
>
> 5. Final read-only audit. Confirm protected files and directories are unchanged, ignored originals and the restoration map are excluded, and only approved paths are staged.
>
> 6. Bring back the exact proposed commit contents. No commit or push until you approve them.
>
> ## What can happen in parallel now?
>
> - The path-by-path inventory and authorization audit.
> - The R2/R5 decision packet, with exact before/after wording and L3 context.
> - The ZA7 counters and stop-count bring-back, provided it remains separate and read-only.
> - The Verðandi decisions can be prepared independently; they are not commit prerequisites.
>
> R4's witness, D13, and the stale `depth_probe.py` summary line remain open and outside this commit's scope. The Ørlǫg release-gate fixes remain release prerequisites, not commit prerequisites.
>
> My recommendation: do not commit all 154 files as one undifferentiated batch. First resolve R2/R5, then make the commit inventory prove the authorization of every included path—especially the 22 files in the expressly excluded directory. The next milestone should be a proposed, auditable staging set, not a commit yet.

**As kept.**
- **The ten reports:** handled, on the evidence reported; the follow-up is closed. In his words: *"it does not change the
  reports' evidentiary status or authorize any broader work."*
- **The commit:** no commit, and nothing staged. Next is a proposed staging set that proves the authorization of every
  path, with `research/law-sufficiency/`'s files kept out unless a separate decision is established, and every evidence
  record mapped to the requirement it supports, current apart from historical. R2 and R5 are his to rule first, by his
  recommendation.

## R2 adopted; R5 adopted as a description of the checker's measured behaviour only (2026-10-31)

He was brought R2's and R5's exact wording, before and after, with L3's context (the proposed staging set, decision
1), as his ruling on REREAD-9's disposition asked. His ruling, whole:

> I rule R2 adopted and R5 adopted as a description of measured checker behavior only. Neither ruling changes a verdict, checker behavior, or the underlying semantic rules.
> R2 — Adopt option (a)
> Adopted
> Adopt the revised derivation-17 sentence:
> A type that would come round a cycle, through a variable as through rules, is underived; the mentions alone do not find a cycle through a variable. Walking again until the types hold still settles within one walk more than there are rules. This states what the walk gives here, and sets up no order-free or least-fixed-point typing of variables (his ruling C).
> Reason: The former phrase “least fixed point” risks asserting a general typing system that ruling C expressly says has not been established. The revised wording describes the actual iterative walk without making that broader claim.
> This is a documentary correction, not a new theorem or a change to the checker. Preserve the former wording in the historical draft and its kept evidence.
> R5 — Adopt option (a), with an explicit limitation
> Adopted — descriptive only
> Adopt:
> the variable's type; with an index, made only when the variable is a list
> But classify this strictly as a description of the checker's measured behavior, not as a newly adopted rule of the W9 table.
> The record must make clear:
>
> * The checker makes the indexed numeric part only when the variable is a list.
> * For a non-list variable, that part is not made, and the same-line list condition fails.
> * This describes the implementation that was measured.
> * It does not independently settle any broader question of language semantics or authorize a new rule.
>
> Do not adopt option (b), which would elevate the wording into a normative rule.
> Record and scope
>
> 1. Update draft 9's disposition of R2 and R5 to reflect these rulings.
> 2. Reconcile Amendment 9's dated deferral note with the new dispositions. Preserve the history; do not erase the fact that both were previously applied without my disposition.
> 3. Update the proposed staging set and inventory only as needed to reflect the adopted wording and its status.
> 4. Preserve the old draft and hash-identified versions under the existing evidence-preservation requirements.
>
> No checker, runner, reference, law, gate, or release changes are authorized. No staging, commit, or push is authorized.
> The two wording decisions are now closed. The remaining commit decisions are the law-sufficiency files, kept-evidence tracking, `LATER.md`, and the proposed four-commit structure.

**As kept.**
- **R2:** adopted, a documentary correction; the former wording, "least fixed point", stays in the historical drafts
  and their kept evidence.
- **R5:** adopted as a description of the checker's measured behaviour only, never a rule of the W9 table; option (b) is
  not adopted. It settles no question of the language's semantics.
- **The history stays:** both were applied without his disposition (REREAD-9's NC5), then deferred, and now ruled; the
  notes in draft 9 and Amendments 9 and 13 keep each step.
- **Still his:** the law-sufficiency files, the kept evidence's tracking, `LATER.md`, and the commit's shape.

## The law-sufficiency files carried in the commit plan, as a commit of their own (2026-10-31)

He was put the proposed staging set's decision 2: eleven `rust-core` scripts import `decoder1.py`, `common.py` and
`fixtures/` from `research/law-sufficiency/`, which REREAD-9 had excluded from reading. His ruling, whole:

> I rule option (a), with a scope restriction: commit all 26 law-sufficiency files together as a distinct, separately identified commit, provided the inventory confirms that all 26 are the complete set governed by the existing `research/law-sufficiency/RULINGS.md`.
> The reason is reproducibility. Eleven Rust-core scripts import `decoder1.py`, `common.py`, or `fixtures/` from that directory. Committing only the Rust-core records and apparatus while omitting those dependencies would leave the committed repository unable to reproduce the recorded checks from a clean clone.
> I would not choose option (b). Committing only the imported dependencies would preserve some execution paths while omitting the supporting law-sufficiency record and its context. That creates a less intelligible partial snapshot.
> Conditions:
>
> 1. Keep the law-sufficiency material in its own commit, separate from the four proposed Rust-core commits.
> 2. Preserve its existing internal structure and ruling history. Do not rewrite its findings merely to make it fit the Rust-core staging.
> 3. Inventory all 26 paths individually and confirm their hashes and dispositions against `research/law-sufficiency/RULINGS.md`.
> 4. Do not treat their inclusion as adoption of any new legal or technical conclusion beyond the decisions already recorded there.
> 5. If any of the 26 lacks a clear disposition in that ruling record, leave that path out and bring the specific exception back before staging.
>
> This authorizes carrying the law-sufficiency files in the proposed commit plan, not staging or committing them yet. The exact path list and clean-clone reproduction check still need review before staging.

**As kept.**
- **The plan:** the law-sufficiency files form a fifth commit of their own, apart from the four `rust-core` ones,
  their structure and ruling history as they stand; `research/law-sufficiency/` is not edited, and this ruling is
  recorded here, not in its RULINGS.md.
- **Each of the 26** is confirmed against `research/law-sufficiency/RULINGS.md` by name or by the words of its
  disposition; a path without a clear disposition there is left out and brought back to him before staging.
- **Nothing is staged.** The exact path list and a clean-clone reproduction check come before any staging.

## The fourteen law-sufficiency exceptions covered as reproducibility apparatus (2026-10-31)

Checked against `research/law-sufficiency/RULINGS.md`, which disposes of files by kind and names no code file, twelve of
the 26 were confirmed and fourteen, all code or fixtures, were left out and brought back to him, with the first-run
output that is governed by the record but git-ignored. His ruling, whole:

> Yes. I rule all fourteen code and fixture files covered as the apparatus supporting the law-sufficiency evidence. They may be included in the separate fifth commit.
> The basis is the reproducibility purpose of the existing ruling: the findings and evidence should remain intelligible and reproducible, not merely be preserved as disconnected outputs. The apparatus that generated and tested those outputs belongs with them.
> This covers:
>
> * `decoder.py`
> * `decoder1.py`
> * `common.py`
> * `closure_tests.py`
> * `run_all.py`
> * `run_all_1.py`
> * All eight files under `research/law-sufficiency/fixtures/`
>
> Two distinctions matter:
>
> 1. This is a supplemental disposition of the fourteen exceptions, not a claim that the original ruling explicitly named or already disposed of every code file. In particular, `common.py` is included because of its demonstrated dependency role, despite not being named in the original record.
> 2. Their inclusion is as reproducibility apparatus. It does not independently adopt new findings, test conclusions, or legal propositions.
>
> Record this supplemental ruling in `rust-core/RULINGS.md` and the staging proposal, preserving the original twelve-confirmed/fourteen-exception history. Keep the fourteen together with the twelve in commit five.
> The first-run output remains a separate unresolved item. This ruling does not authorize its inclusion or exclusion.

**As kept.**
- **A supplemental disposition:** the original record did not name or dispose of these fourteen; the twelve were
  confirmed by it, and these are covered by this ruling. `common.py` by its dependency role, named in no record.
- **As apparatus only:** no new finding, test conclusion or legal proposition is adopted with them.
- **Commit five** holds all 26, the twelve and the fourteen together, apart from the four `rust-core` commits.
- **Still open:** the first-run output, `work/law-sufficiency-arbiter/closure-run1.txt`; this ruling neither includes
  nor excludes it.

## The kept evidence made visible to git: one negation in `.gitignore` (2026-10-31)

The commit audit found that `.gitignore`'s line `work/` matches every folder named `work`, so git saw none of the kept
files under `research/rust-core/kept/work/`. He was put the choice (the proposed staging set, decision 3). His ruling,
whole:

> I rule option (a): add the single negation rule to `.gitignore`:
>
> ```
> !research/rust-core/kept/work/
> ```
>
> This is preferable to force-adding the directory because it makes the preservation rule durable: Git will see the 108 existing kept files and future files placed there, without requiring someone to remember `git add -f` each time.
> Conditions:
>
> 1. Make only that targeted `.gitignore` change; do not broaden the exception to other `work/` directories.
> 2. Verify with `git check-ignore` that the kept directory and its contents are no longer ignored, while unrelated `work/` directories remain ignored.
> 3. Confirm all 108 kept files appear in the proposed staging inventory, with their hashes and manifest references intact.
> 4. Keep the ignored originals and restoration map excluded.
>
> This also permits the later clean-clone check to test the kept evidence as committed, and makes the first-run output eligible for consideration—but does not decide whether `closure-run1.txt` belongs in commit five.
> This authorizes the `.gitignore` change and its verification only. Nothing is staged or committed.

**As kept.**
- **The change:** one line, `!research/rust-core/kept/work/`, after `work/`, and nothing else in `.gitignore`.
- **Verified** with `git check-ignore`: the kept folder and its files no longer ignored; every other folder named `work`
  still ignored, the originals and the restoration map among them.
- **Nothing is staged or committed.** The first-run output stays undecided; this ruling makes it eligible, no more.

## The law-sufficiency first-run output carried in commit five (2026-10-31)

The law-sufficiency record keeps the *"first-run output"* with the findings and evidence; it lies under the ignored
top-level `work/`, outside the 26. He was put whether commit five carries it. His ruling, whole:

> Yes. Carry `work/law-sufficiency-arbiter/closure-run1.txt` in commit five.
> The existing law-sufficiency ruling expressly says to keep the first-run output together with the findings, original sheet, dated amendment, and two-run evidence. This file is the identified first-run output, and the inventory confirms its size and that it contains no account name.
> The fact that it sits under the ignored top-level `work/` does not change its evidentiary disposition.
> Conditions:
>
> 1. Include only this identified file from the top-level `work/` directory.
> 2. Force-add this exact path for commit five; do not broaden `.gitignore` to expose unrelated working files.
> 3. Record its path, size, and SHA-256 in the inventory and staging proposal.
> 4. Preserve its original contents; no rewriting or regeneration.
>
> This authorizes its inclusion in the proposed fifth commit, not staging or committing yet.

**As kept.**
- **The file:** `work/law-sufficiency-arbiter/closure-run1.txt`, 3646 bytes, sha256 `766ed0090e47789f6770fa97b5b25255ff28644ff915df0a99a7e0863c60f070`, its contents as they stand, never rewritten or made again.
- **How it will enter:** added by force, by this exact path, in commit five; `.gitignore` is not changed for it, and
  no other file under the top-level `work/` enters.
- **Nothing is staged or committed.**

## LATER.md carried in the record commit, as his note (2026-10-31)

`LATER.md` records his note of 2026-10-30, kept at his word as a note for later: not started, not a ruling. He was put
whether the commit carries it (the proposed staging set, decision 4). His ruling, whole:

> Yes. Include `LATER.md` in the proposed commit set, as a record of my 2026-10-30 note.
> Conditions:
>
> 1. Preserve its wording and contents exactly; do not turn the note into a ruling or imply that the work has begun.
> 2. Identify it in the inventory as a user note, not an adopted decision, finding, or technical artifact.
> 3. Place it in the fourth Rust-core commit (the record), not the law-sufficiency commit.
> 4. Keep its historical date and provenance.
>
> This authorizes inclusion in the proposed staging set only. No staging or committing is authorized.
> All five commit groups now have a proposed disposition. The next step is to reconcile the inventory and staging proposal, then regenerate draft 9’s records twice against the final text before the final audit and dry-run review.

**As kept.**
- **The file** is carried as it stands (sha256 `93dfabe5…`), its date and provenance with it, in the fourth `rust-core`
  commit, the record; in the inventory it is his note, not a decision, finding or technical artifact, and nothing says
  its work has begun.
- **Next, in his words:** *"The next step is to reconcile the inventory and staging proposal, then regenerate draft 9’s
  records twice against the final text before the final audit and dry-run review."* Nothing is staged or committed.

## The final read-only audit and the clean-clone check authorized (2026-10-31)

Every commit group had a proposed disposition and draft 9's records had been made again on its final text (SHEET.md,
Amendment 16). He was asked whether to run the final read-only audit with the clean-clone check. His ruling, whole:

> Yes. I authorize the final read-only audit and clean-clone check now.
> Keep the scope strictly to verification:
>
> 1. Verify all 270 inventory entries against their actual paths, sizes, hashes, and assigned commit.
> 2. Check quotations, line lengths, amendment references, and the consistency of the staging proposal.
> 3. Verify all 114 kept files against their manifests, including the six newly kept files.
> 4. Check dependencies across the five proposed commit groups.
> 5. Build the clean clone outside the working repository from the exact proposed file set, then rerun the relevant checks and records.
> 6. Report every pass, failure, exception, and reproduction limitation. Do not silently repair discrepancies.
>
> Two boundaries remain:
>
> * Nothing may be staged, committed, or pushed.
> * The R6-reference placement and commit order remain proposals for my review with the exact dry-run output. In particular, test whether commit five must precede commit two for a runnable intermediate repository.
>
> Bring back the audit results and dry-run proposal separately. This authorization is for the audit only.

**As kept.**
- **Verification only:** nothing is repaired in passing; a discrepancy is reported, not fixed. Nothing is staged,
  committed or pushed, in the repository or anywhere else.
- **The clean clone** is built outside the working repository from the exact proposed file set; the commit order and
  the R6 reference records' placement are tested there, and stay proposals for his review.
- **Two reports:** the audit's results and the dry-run proposal, apart.

## The commit order: 5, 1, 3, 2, 4 (2026-10-31)

He was given the audit's results and, apart, the dry-run proposal: measured in a clean clone, commit five must precede
commit two, and with the R6 reference records and the kept files in commit three, only the order 5, 1, 3, 2, 4 lets
every check run once the apparatus lands. His ruling, whole:

> I rule for option (a): `5 → 1 → 3 → 2 → 4`.
>
> The clean-clone measurements establish that this is the only proposed order in which every check runs once the apparatus lands:
>
> | Order | Commit | Contents                                                |
> | ----- | ------ | ------------------------------------------------------- |
> | 1     | 5      | Law-sufficiency (27 paths)                              |
> | 2     | 1      | Format                                                  |
> | 3     | 3      | Evidence, including R6 reference records and kept files |
> | 4     | 2      | Apparatus                                               |
> | 5     | 4      | Documentary record                                      |
>
> R6 reference records stay in commit 3, with the evidence. Keep the frozen generator inputs in commit 2, with the apparatus.
>
> I accept the trade-off: the evidence appears in history before the scripts that generated it. That is preferable to an intermediate repository state in which the runner's check or kept-evidence checks cannot run.
>
> Conditions:
>
> 1. Preserve the five commit groups' exact path membership; change only their order.
> 2. Rebuild the five path lists for this order and verify their hashes.
> 3. Repeat the dry run from a short-path clone, confirming all 270 paths and the one exact force-added first-run output.
> 4. Report the five exceptions from the audit without silently repairing them. In particular, do not change draft 9 or its hash-dependent records.
> 5. Do not stage, commit, or push.
>
> This authorizes the reordered staging proposal and its verification only. Bring back the refreshed lists and dry-run results for review.

**As kept.**
- **The order** is 5, 1, 3, 2, 4; the five groups' membership is unchanged; the R6 reference records stay in commit
  three, the frozen generator inputs in commit two.
- **The audit's five exceptions** stay as reported, unrepaired; draft 9 and its hash-dependent records are not changed.
- **Next:** the five lists rebuilt and their sha256 verified, and the dry run repeated from a short-path clone in this
  order. Nothing is staged, committed or pushed.

## What follows, as recorded

- **Phase 0 comes first:** LAW-FORMAT-0, then its independent re-read, then the disposition of the re-read's findings.
  No core code before the re-read (his condition 1).
- **The core's author** works from LAW-FORMAT-0, SPEC.md, RUNTIME-SPEC.md and the vectors only. It never takes the
  decoder, the interpreter, the generators or `numeric_ref.py` as implementation material (D1, condition 2).
- **R6** records each mutant's outcome: refused, or accepted and agreeing. It never counts an accepted malformed
  encoding as a refusal (condition 3).
- **R5** compares the stopping point and the receipt or trace (condition 4).
- **The evidence** names each build fresh or cached, with the cache checked (condition 5). It keeps every command,
  compiler version, host detail, seed, input, output and plant result (condition 6).
- **The text seal is the caller's input.** The core prints it, and does not derive or validate it.
