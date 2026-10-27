# The rulings §15's draft cites, as ruled (the twin's reading set under R7)

R7 has the twin read the rulings the draft's tags cite (R3, R4, R5, R6 and the claims ruling) **as ruled**: the
owner's decision and the text it explicitly adopts by reference, to the extent adopted. Not the sheet's options,
recommendations or notes.

This file is that selection. It was **assembled by the draft's author**, so it is a choice and not a neutral copy.
Each excerpt cites its line in `research/run-1/RULINGS.md` so the choice can be audited there, and every exclusion is
named. The owner's words are in quotation marks; adopted text is labelled as such.

## R3. How input text becomes a value

**The decision** (line 96): "I rule in favor of Option a (The Conversion Rule) for R3."

**The option row it adopts** (line 88): *a. Exact or refused (the conversion rule) — a decimal that is not exactly a
Fix value is refused at the door; the log never holds a rounded value — rounding is forbidden. Inputs must arrive
already on the 2^-32 grid, or as raw values*

**The sheet's text common to both options, adopted with either** (line 91): *Either way the log holds typed encodings
only (RUNTIME-SPEC §5), written once by a Python input door, so no runtime ever parses decimal text and no host's
strtod can diverge.*

**His reasons** (lines 96–98): "The true, structural differentiator is reversibility under COMPAT-0 and the
preservation of data provenance." Option a "treats rounding as a client-side capability rather than an engine-side
compromise."

**His enactment for the door** (lines 111–131):
- "The entrance tool filters all incoming port streams using a restrictive ASCII regular expression sieve. This occurs
  before passing strings to Python's Fraction constructor, neutralizing format exploitation"
- "Double-Bounded Range Checks: The door must explicitly validate that the parsed value sits securely within the
  strict raw storage parameters of the `Fix` bounds (`MIN_FIX_RAW` and `MAX_FIX_RAW`), actively protecting the lower
  negative boundary against floor overflow errors down to −2147483648.5."
- "Integer Port Restrictions: An incoming string hitting a port explicitly typed as `an integer` must fail instantly if
  a fraction or decimal component is detected. Truncation or automatic floor-rounding at the gate is blocked."
- "Boolean Uniqueness: Truth-value channels accept exactly one invariant string spelling for `true` and one for
  `false`. Alternative representations, case variations, or numeric bits (`1`/`0`) are refused."
- "Text Byte Purity: String inputs are preserved byte-for-byte as sent. Non-NFC unicode payloads generate an explicit
  report note; CP1252 character maps are rejected outright."
- "Raw Value Spellings & Neighbor Refusals: Raw hexadecimal scalar strings are given an isolated syntactic prefix that
  the text grammar tracks separately from standard base-10 decimals. When a user input is rejected for non-alignment
  with the 2^-32 fixed-point grid, the door's refusal message must explicitly compute and output the two nearest valid
  representable grid coordinates to the client."

**Excluded:** the options table's option b; the recommendation; the record's notes on the code's bounds, the
`Fraction` measurement, "what it settles", "what falls away", the falsifier and the details left for 1a.

## R4. What a refusal does in a run with ticks

**The decision** (line 151): "I rule R4 as written in your proposed ruling text: (a) at tick granularity, with automatic
continuation deferred until SNAP-1, and the refused branch permanently sealed and queryable."

**The ruling text it adopts** (lines 155–159):

> R4: a, at tick granularity. A refusal ends its branch at tick t. The session may continue on a new branch from tick
> t−1, rebuilt by replay from the nearest checked snapshot and checked against the tick line's state digest, reading
> tick t by a declared continuation rule written into the log. The refused branch is kept, sealed and queryable. The
> court reads each branch on its own and names every abandoned branch. Automatic continuation waits for SNAP-1; until
> then a refusal ends the session.

**Excluded:** the options table (including option a's own row, which the adopted ruling text replaces); the
recommendation; "what it settles", "what it leaves open", and the proposals for SNAP-1.

## R5. Versions and headers

**The decision** (line 192): "I rule `R5` as written, augmented by your four explicit amendments"

**R5 as written** (lines 180–189):
- `orlog-law 1`, only when a v1 form appears, so v0 laws stay byte-identical. It adds the law lines
  `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[ budget <N>])`.
- `orlog-trace-1`: `head0 = SHA-256("orlog-trace-1" || law_seal)`. New events: `'T'`, the tick number (u64); `'N'`, a
  port's value (u32 var and the value encoding of RUNTIME-SPEC §5). Each tick emits `'T'`, then one `'N'` per
  each-tick port in declaration order, then the body. The read-once ports' `'N'` events come before the first `'T'`.
- `orlog-receipt 1` adds `ticks <n>` and `input-log-sha256 <hex>`. It replaces `output-sha256` with `output-chain
  <hex>`, where out_t = SHA-256(out_{t−1} || SHA-256(the output of tick t)).

**The four amendments it adopts** (lines 194–218), as proposed, with his words inside them:
1. `'T'`'s payload is the tick and the operation count (u64, u64).
2. The output chain's start and edges are defined: out_0, the output said before the first tick, and a refused tick's
   partial output. On the last, his words: "if a tick encounters a transactional refusal, its partial output is
   formally hashed into the chain before the rollback logic clears the volatile state", so a refused tick's partial
   output is the chain's last link. He wrote of out_0 as "the initial hash of any visual bytes or metadata written before the first tick".
3. `ticks <n>` at a refusal counts the ticks begun, and a refused tick writes no per-tick line; its record is the
   receipt's status and the trace's `'R'` event. This is R4 a, ruled at tick granularity.
4. The receipt frame check is versioned, with its plants. His words: "The arbiter must accept both `orlog-receipt 0`
   and `orlog-receipt 1` formats depending on the code path. To keep this defensive, we implement the requested inverse
   plants: a `v1` receipt checked under a `v0` template must fail, and a `v0` payload evaluated under `v1` rules must be
   caught and refused." Confirmed the same day: "Tying the receipt frame check strictly to the law's own header
   (`orlog-law 0` demands `orlog-receipt 0`, and `orlog-law 1` demands `orlog-receipt 1`) is the only sound option."

**The two choices he fixed** (lines 220–228):
- The per-tick line, `orlog-ticks 0`, is part of 1a. His words: "We include this artifact now within the `1a`
  specification. Do not defer it to a later version." The artifact as proposed carries the tick, events, ops, output
  bytes, the trace head (`-` in a play build without the chain), the output chain, a claims digest and a state digest.
- The trace keeps the per-event chain; no stream head. His words: "We keep the per-event chain exactly as written
  instead of switching to a compressed stream head."

**Excluded:** the recommendation; the reasons given with amendment 1 (P12); the record's notes on amendment 1's
reading of c, on amendment 2's reading of out_0, on amendment 3's "R4 c", and on amendment 4's arbiter code and
"read as"; the snapshot-midstate reasoning; and the cost remarks on the state digest.

## R6. What the input log is to the court

**The decision** (line 284): "I rule Option a (Data, never a channel) for `RUN-1`. The primary principle is unyielding:
replayable data is not admissible testimony." And: "`Option b` stays held as a later potential fork for a future court
update."

**The option row it adopts** (line 233): *a. Data, never a channel — in a run with an input log (the law declares a
port, or has a tick block), no claim is GROUNDED, whatever its channel and whatever is ratified, except under the
licence below; the court shows the log's seal as provenance: "rests on input log <seal>, unratified" — replayable is
not admissible (DOCTRINE T12, limit 4). A log is a value chosen by whoever ran the session, and it can never raise a
standing*

**The licence the row adopts by "the licence below"** (lines 239–249), exactly as there:

> - **The licence, PREFIX**, decided from the text: a claim is exempt only if every evaluation of it precedes the first
>   input.
>   - It must stand before the first port declaration, outside the tick block.
>   - It must not sit in a procedure performed at or after the first port declaration. The licence is decided by
>     evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still
>     runs during it.
>   - Nothing the log sets exists before its first input, so a prefix claim's whole claim line is fixed by the law: its
>     evaluations, its trues, its cost and its certified clause's cost.
>   - A wider licence would exempt a claim with no path from any port, shown by two independent derivations, and must
>     then cover the whole claim line, since a certificate's cost reading can move with a port while its truth does not.
>     It waits for a trigger (`research/doppler/VERDICT.md`).

**What he ruled with it, in his words** (lines 284–305):
- R1's cost sentence (appended to R1, line 56): "Moving a world property out of the law and into a read-once port means
  the cost of rule a reaches every later claim in the run, stripping them of grounding even if they never touch that
  property directly."
- One seal: "The court's generated provenance output line must print exactly the `input-log-sha256` value defined in
  `receipt 1`."
- "Every row testing an ungrounded port violation must run with the witness explicitly configured as agreed"
- "Each test row is structurally paired with an internal control variant. The control evaluates the exact same claim
  without an active log declaration, or wraps it securely within the `PREFIX` license parameters. The control must
  return a clean `GROUNDED` standing"
- "A claim wrapped within the `PREFIX` license parameters that evaluated true remains historically held, regardless of
  whether the execution loop encounters a subsequent transactional refusal downstream." His reason: "a downstream
  failure on frame t cannot retrospectively invalidate a pure, law-bound proof that completed before the timeline even
  initiated."

**Excluded:** option b's row; the recommendation's other bullets (the trigger's elaboration, the falsifier and its
acceptance rows, "sound, not complete", time and randomness); the two dated amendments of the proposal before the
ruling; the record's notes ("no vacuous row", R12's note, "its scope is his reason's", "proposed with it, not ruled").

## The claims ruling

**The decision, in full** (lines 323–336): his ruling text, quoted there whole, begins "My ruling: E2 is the meaning of
`HELD` for version 1." It is reproduced here without change:

> My ruling: E2 is the meaning of `HELD` for version 1.
> `HELD` means that every completed evaluation of the claim was true, no evaluation of that claim remains open at the cut, and the continuation at the cut could not evaluate that claim again.
> I adopt option (d): admit the meet \(R8 \land CUT\text{-}0\), pinned to the exact CUT-0 digest, with each withholding identifying its structural row. CUT-0 alone remains the target for further development.
> The scope of this ruling is:
>
> 1. Authoritative standing: E2 governs `HELD`. E1's “true in \(k\) of \(k\) evaluations” remains descriptive evidence, not a substitute for settlement.
> 2. Claim-specific continuation: Only continuation that could evaluate the particular claim again affects its standing. Unrelated pending execution does not withhold it.
> 3. Withholding explanations: Every CUT-0 withholding must identify the responsible structural row.
> 4. Rule identity: The admitted meet must identify the exact CUT-0 digest. A digest identifies the rule; it does not prove the rule sound.
> 5. Proof obligations: T10 remains open and must be split into row-specific obligations. The `While` next-pass row is the priority for precision investigation. No test result or measurement alone closes T10.
> 6. Unchanged obligations: T11 remains open. This ruling establishes neither compatibility preservation nor general soundness.
> 7. Governance record: Record this semantic decision in `RULINGS.md` in the owner's words, and have DOCTRINE refer to it. Do not represent the decision as a theorem-ledger result.
>
> The 40,141 `CONFIRMED` cases remain withheld under E2 because their tested resumptions actually evaluated the claims again. Releasing claims whose truth cannot change would require a separate, stronger invariance rule; that is not part of this version 1 ruling.
> This is the normative decision. It does not claim that I have edited files, committed changes, or discharged the outstanding proof obligations.

**Excluded:** the record's "what it fixes", "what it supersedes" and "what stays open" notes.

## Finding 24 and the PREFIX licence

*Added 2026-10-26 for R7's first re-read. The draft's tags `[ruled: F24]` and `[ruled: PREFIX]` cite it.*

**The decision, in full** (lines 440–451): his answer, when asked whether he adopts as his ruling a proposal he had forwarded. It is reproduced here without change:

> Adopt as written (Recommended).
>
> I adopt D for finding 24 and B1 + 4a + 5c + K1 for PREFIX (findings 3–5) as my rulings, subject to the four stated conditions. The scope is limited: this resolves the D10/R6 interaction and the PREFIX licensing boundary; it does not close T10/T11, establish CUT-0’s soundness, or independently verify reference arithmetic.
>
> The four conditions are part of the ruling:
> 1. The configured witness covers the PREFIX row and its controls, not only ungrounded rows; results say configured, not measured.
> 2. Reach fails closed on unknown statement kinds, including the version-1 tick-block case.
> 3. An independent structural oracle checks PREFIX licensing; the trace is a check, not the rule.
> 4. Nothing is built before the twin rereads the affected clauses under R7.
> The adopted text must preserve the distinction between a real court reading (REFERENCE-ONLY until 1b, holding no claim) and 1a test rows that exercise the reference with the agreed witness configured. Court R1 remains a condition of HELD alongside E2.
>
> I authorize recording this answer as my ruling, with the cited packet A §5 and packet B §4 wording adopted verbatim as specified. After recording, compute each ruling’s affected-clause set \(A_r = T_r \cup L_r \cup D_r\), including dependencies identified by the twin’s tag audit, and have the twin perform the required rereads before any build.

**The texts it adopts, verbatim, as his answer specifies.** Their first person is their authors', not his.

1. **The proposal he forwarded** (lines 458–504):

> My ruling is D for finding 24, paired with B1 + 4a + 5c + K1 for PREFIX (findings 3–5), subject to one important qualification: D10 governs real court readings, while the R6 test rows may exercise the 1a reference with a configured witness. This does not make those test rows evidence that the reference's version-1 arithmetic is correct.
> I would record these as two linked but distinct rulings. D resolves the scope conflict; PREFIX defines the licence the rows test. Neither settles read-once ports or load-refusal behavior.
> 1. Finding 24 — D10 against R6
> Adopt packet A's proposed scope distinction:
>
> * Until 1b, a real court reading of a version-1 run remains `REFERENCE-ONLY` and holds no claim.
> * R6's rows, the PREFIX row, and their controls may run in 1a against the reference with the agreed witness configured.
> * Each such row must explicitly say that its agreement is configured, not measured.
> * Court R1 remains a condition of `HELD` alongside E2. The claims ruling is not amended.
>
> That last point is essential. E2 defines the claim-specific continuation condition; it does not erase the court's backend-agreement requirement. A configured witness does not constitute independent backend agreement.
> Scope: this changes D10's wording as a default for real court readings versus test execution. It does not overrule R6 or establish version-1 execution correctness.
> 2. PREFIX — findings 3–5
> Adopt packet B's proposed interpretation of R6, not D-18's wider boundary.
> The boundary is the first top-level clause that is or holds a port declaration of either kind, or is the tick block. A claim is licensed exactly when:
>
> 1. It stands before that boundary and outside the tick block.
> 2. No clause from the boundary onward can execute it.
>
> The closure follows all branches, loop bodies, tick bodies, and procedure calls transitively; it ignores runtime values and fails closed for statement kinds without a closure rule.
> Consequences:
>
> * A law with a tick block but no port still has a boundary at the tick block.
> * A claim after an each-tick port declaration is not licensed merely because it never reads that port.
> * D-18's alternative boundary is not adopted; using it would widen R6.
> * A licensed claim must still satisfy the existing settlement rules. Licensing is not `GROUNDED` or `HELD` by itself.
>
> This interpretation preserves R6's sound-but-not-complete posture: a claim may be conservatively excluded even when a particular execution would never reach an input-dependent path.
> 3. Conditions attached to these rulings
> I would require the following to be recorded alongside the decisions:
>
> * Witness scope: explicitly confirm that the configured witness covers the PREFIX row and its controls, not only the ungrounded rows.
> * Reach implementation: the version-1 closure must fail closed on the tick block and unknown statement kinds. The existing version-0 default behavior is not enough to establish this.
> * Independent oracle: the PREFIX test oracle must establish the licence from source structure across its fixtures and logs; trace data may check the result, but must not define the rule.
> * No premature build: the twin must reread the affected clauses under R7 before they are built.
>
> 4. What remains open
> These rulings do not settle:
>
> * Finding 6: read-once binding position, missing-value behavior, or session event representation.
> * Finding 8: `LOG-*` conditions, load-refusal receipts, or provenance-line obligations.
> * The version-1 format freeze.
> * T10/T11 or the soundness of CUT-0.
> * Whether the reference's version-1 execution arithmetic agrees with an independent backend.
>
> The read-once question should come next, followed by the load-refusal ruling, as your integration record recommends.
> Recordkeeping note: these are my proposed rulings for you to adopt or reject, not changes made to `RULINGS.md`. Once you record them in your own words, compute the affected-clause sets \(A_r=T_r\cup L_r\cup D_r\), including the twin's missing-dependency audit findings. Then have the twin reread the resulting clauses before implementation.

2. **Packet A §5's wording** (line 508):

> D10, the court clause: until 1b, the court's reading of a version-1 run, read with the witness the arbiter makes, is REFERENCE-ONLY and holds no claim (court R1, unchanged). This governs readings of runs, not the court's rows: R6's rows, the PREFIX row and each row's control run in 1a's reference with the witness configured as agreed, as R6's first rider requires, and each such row states that its agreement is configured, not measured.

3. **Packet B §4's wording** (line 512):

> The licence is decided from the law's text alone, never from a log or a trace. The boundary is the first top-level clause, in the text, that is or holds a port declaration, or is the tick block. A claim is licensed exactly when (a) it stands before the boundary and outside the tick block, and (b) no clause from the boundary on may execute it. The closure follows every arm, the body of every loop and of the tick block, and every procedure performed, transitively, with values ignored. A statement kind the closure has no rule for licenses no claim of the law.

**Excluded:** the record's notes after them, "what it fixes", "what it refines", "what stays open" and "its re-reads" (lines 514–544).

## The labels' definitions, the closure's rule table, and R6's control

*Added 2026-10-27 for R7's second re-read. The lines below are `RULINGS.md` lines 548–623, unchanged: each question as it was put to him, his answer whole, and the labels' definitions his first answer adopts.*

*Added 2026-10-27 by his rulings on three questions R7's first re-read raised (`twin-r7/REREAD-1-REPORT.md`, disposed
in `twin-r7/REREAD-1-DISPOSITION.md`: PREFIX-1 and PREFIX-4, PREFIX-3, and F24-6). Each question is given as it was put
to him, then his answer, whole and unchanged.*

**1. The labels.** Asked: "Your answer adopted the labels D and B1 + 4a + 5c + K1, which packet A §4 and packet B §3
define. Do the labels adopt those definitions? If so, K1's definition settles two of the twin's findings: the closure
follows the tick block's body (PREFIX-1), and an unperformed To after the boundary adds nothing (PREFIX-4)." His words:

> Other — adopt the definitions, but do not automatically accept the claimed downstream conclusions.
>
> My ruling is that adopting D and B1 + 4a + 5c + K1 adopts the definitions those labels designate in packets A and B, not merely the labels or their headline wording. Otherwise the ruling would refer to options without specifying their operative meaning.
>
> However, that does not mean every conclusion drawn from those definitions is automatically established. In particular:
>
> - PREFIX-1: The tick block must have its own closure rule that follows its body. The closure must fail closed on unknown statement kinds. This does not by itself establish that PX-6 is licensed; that result must follow from the complete source-structure rule and fixture.
> - PREFIX-4: An unperformed `To` after the boundary contributes no executed call to the transitive closure. But licensing is determined from source structure with values ignored, so the fact that a call is unperformed at runtime is not, by itself, sufficient to establish that a claim is licensed.
> - Port declarations: Do not infer that the absence of a closure rule for port declarations licenses claims—or automatically makes every law with a port unlicensable. The adopted rule requires an explicit, sound closure treatment of the relevant statement kinds. If the packets' definitions leave that point unresolved, return it as a precise ruling question rather than silently extending K1.
>
> Record the definitions as adopted text, preserve the distinction between the ruling and its tested consequences, and have the twin reread the affected clauses before any build. Do not mark PX-6 licensed merely because the label was adopted.

**2. The closure's rule table.** Asked: "The closure's rule table (PREFIX-3), proposed from K1 and SPEC §3: a claim adds
itself; If/Unless/Otherwise add every arm; For and While add their body; the tick block adds its body; Perform adds the
procedure's body, transitively; To, Define and Decimals add nothing when reached; Let, Set, Increase, Decrease, Say,
Append, Remove, Must and a port declaration add nothing; any other kind licenses no claim of the law. Adopt it?" His
words:

> Adopt the table, with one clarification to its wording.
>
> The closure needs an explicit rule for every known statement kind; otherwise, “fail closed” would treat a port declaration as unknown and exclude every claim in a law containing a port. That would be unnecessarily conservative and would not implement the intended PREFIX licence.
>
> Adopt the proposed table for PREFIX-3 / §15.12.4, with these conditions:
>
> 1. Structural closure only. Follow every arm, loop body, tick-block body, and performed procedure transitively, ignoring runtime values.
> 2. Known no-addition kinds are explicit. `To`, `Define`, `Decimals`, and the listed simple statements and port declarations add no further reachable body under this rule. This does not exempt their surrounding clauses from the boundary or licensing test.
> 3. Unknown kinds fail closed. Any statement kind without an explicit rule licenses no claim of the law.
> 4. No runtime shortcut. An unperformed `To` adds no procedure body because the closure is source-structural—not because a particular execution skipped it.
>
> This adopts the closure table; it does not establish that any individual claim, including PX-6, is licensed or `GROUNDED`/`HELD`. Those outcomes must follow from applying the full rule to the source structure and then the existing settlement rules. The twin must reread the affected clauses before anything is built.

**3. R6's version-0 control.** Asked: "R6's control 'without an active log declaration' is a version-0 run, which could
have a measured witness. Your condition 1 says the configured witness covers the controls. Which should it be?" His
words:

> Other — keep the configured witness for the R6 row and its control; add the measured version-0 control as a separate row.
>
> The R6 comparison must isolate one variable: R6 versus no active log declaration. Both rows therefore use the same configured witness. Otherwise the comparison changes both the rule and the witness, making the result ambiguous.
>
> Record these distinctions:
>
> - R6 row and paired control: same configured witness; the only intended difference is R6.
> - Separate version-0 control: may use the arbiter’s own measured witness, clearly labelled as a distinct measurement—not as the paired R6 control.
> - Interpretation: configured agreement is not measured agreement, and neither establishes the reference’s version-1 arithmetic independently.
>
> This preserves condition 1 while allowing the measured version-0 result to provide additional evidence without confounding the R6 comparison.

**The definitions his first answer adopts**, verbatim from the packets. Each label's defining text is given; its verdicts
on the packets' worked laws (L1–L11), on the review's probes and its grade ("Within R6", "Interprets R6"), and D's "In
1a", "In 1b" and "Failures" lines, are the packets' consequences. His answer leaves them to be tested, not ruled: *"do
not automatically accept the claimed downstream conclusions."*

- **D**, packet A §4:
  > **D (preferred). Rule D10's court clause with a scope sentence: real readings stay REFERENCE-ONLY; R6's rows, the PREFIX row and their controls run in 1a with the configured witness.**
- **B1**, packet B §3.1:
  > **B1. The first port declaration of either kind, else the tick block.**
  > - PROPOSED WORDING: "the first top-level clause that is, or holds, a port declaration, or is the tick block".
- **4a**, packet B §3.2:
  > **4a. The boundary is the tick block** (the "or is the tick block" in B1's wording).
- **5c**, packet B §3.3:
  > **5c. Exempt exactly when the static test holds:** bullet 1, plus the closure in §3.4.
- **K1**, packet B §3.4:
  > **K1. `Reach`, with values ignored.**
  > - It follows every If arm and the Otherwise, every loop body, the tick block's body, and every Perform transitively.
  > - Its start set is the top-level clause that is or holds the boundary, plus every later top-level clause.
  > - A statement kind it does not know licenses no claim (fail closed).

**Excluded:** the record's notes after them, "what they fix" and "its re-reads" (lines 624–641).

## The table's Perform row

*Added 2026-10-27 for R7's third re-read. `RULINGS.md` lines 645–653, unchanged: the question as it was put to him, and his answer.*

*Added 2026-10-27 by his answer to one question R7's second re-read raised (`twin-r7/REREAD-2-REPORT.md`, TABLE-1;
disposed in `twin-r7/REREAD-2-DISPOSITION.md`).* Asked: "The rule table's "Perform" row: is it SPEC §3's row
"`Perform <name>` or the name alone as a statement", so a bare procedure-name call is the Perform kind? SPEC §3 gives
both spellings one row, and the built parser makes the same Perform node for both (syntax.py lines 456 and 558)." His
answer, whole:

> Yes, the bare name is Perform (Recommended)

**Excluded:** the record's note after it, "what it fixes" (line 654 on).

## Finding 6: read-once ports

*Added 2026-10-27 for R7's third re-read. `RULINGS.md` lines 659–688, unchanged: his ruling whole, then the text he adopted, packet F §6's RO′-1 to RO′-6.*

*Added 2026-10-27 by his ruling. It is not one of R1–R12. It decides finding 6 of R7's review (`twin-r7/REPORT.md`),
from packet C (`packets/C-read-once-ports.md`) and the adversarial comparison he asked for
(`packets/F-read-once-adversary.md`), summarized in `RELEASE-DECISIONS.md` §2.*

**Ruled 2026-10-27: A′, as RO′-1 to RO′-6, with six conditions.** His words, whole:

> I rule for A′, as RO′-1 to RO′-6, with the stated limits.
> The prefix runs up to the first read-once declaration. If the required read-once value is missing, the run ends `NOT-RUN` there and names the first empty read-once port. Add the RO′-6 row to CUT-0 before its digest is pinned.
> Conditions of the ruling:
>
> 1. Whole-log validation remains mandatory. A malformed log is rejected before any statement executes. A well-formed log missing a required read-once value is a distinct case: the permitted prefix may execute, then stop at the declaration.
> 2. R6 remains unchanged. Do not weaken the law-fixed PREFIX claim-line invariant to accommodate design A.
> 3. CUT-0 must explicitly cover this stop point. RO′-6 must state the applicable premises and withholding behavior; do not assume the existing “rest of a block” row covers it without checking.
> 4. N2 and N3 remain open for the A2 row. This ruling does not settle their behavior.
> 5. Finding 8 must define a loadable representation for read-once `NOT-RUN` logs. Byte forms remain open.
> 6. No implementation or build before the affected-clause set is computed and the twin rereads the affected clauses under R7.
>
> This settles the design choice, not the remaining byte format, session-event semantics, finding 8, or CUT-0's overall soundness.
> Next: record this ruling, update the decision sheet, and include finding 6's dependencies in the batched reread. The three-turn push target remains conditional on resolving the remaining release blockers and passing the final gate on the exact tree.

**The text he adopted**, packet F §6, verbatim:

> **RO′-1.** A read-once value reaches the session only as an arrival, judged by the door at once; a refused arrival is never assigned; a retry is a new arrival; neither ends the session.
> **RO′-2.** The read-once ports have one record, filled by assigning accepted arrivals, at most one per port, and closed once before any tick record; it is written whole or not at all. A law with no read-once port is unchanged.
> **RO′-3.** A read-once port binds where its declaration stands. A run executes the top-level clauses before the first read-once declaration whatever the log holds, provided the log loads. If the log holds the read-once record, the run goes on. If it does not, the run stops before the first read-once declaration: NOT-RUN naming the read-once port the end record names (the first empty one in declaration order, checked against the history), or LOG-OPEN if the log has no end record. No `'N'` is emitted, and no value is invented, held over, defaulted or bound from another read-once port.
> **RO′-4.** A refusal before that declaration is REFUSED, whatever the log holds.
> **RO′-5.** That stop is a case of NOT-RUN or LOG-OPEN, not a fifth status. COMPLETED never stands for a law with a read-once port whose log lacks the record.
> **RO′-6 [pinned].** At that stop the cut is the first read-once declaration, a top-level frame not begun; K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored. The NOT-RUN t / LOG-OPEN row applies only when the record is present or no read-once port is declared.

**Excluded:** the record's notes after them, "what it fixes", "what stays open" and "its re-reads" (lines 689–711).

## The read-once stop's row, its version-1 check, and the last re-read

*Added 2026-10-27 for R7's fourth re-read. `RULINGS.md` lines 759–785, unchanged: each question as it was put to him, and his answer.*

*Added 2026-10-27 by his answers to three questions R7's third re-read raised (`twin-r7/REREAD-3-REPORT.md`, F6-1 and
F6-14; disposed in `twin-r7/REREAD-3-DISPOSITION.md`) and to how the re-reads converge before the push. Each question
is given as it was put to him, then his answer, whole and unchanged.*

**1. The stop's row.** Asked: "F6-1: when the read-once stop withholds a claim, which row does the withholding name?
The claims ruling requires the responsible structural row, and your condition 3 says not to assume 'the rest of a
block' covers the stop." His words:

> 1. F6-1 — The read-once stop’s withholding row
>
> Adopt “Its own row.” Name it “the read-once stop” in §15.13.9’s row list. Compute its \(\hat K\) as RO′-6 specifies: the rest of the block from the first read-once declaration. Do not attribute this withholding to the existing “rest of a block” row or imply that row covers a frame that never began. This preserves the requirement that each withholding identify its responsible structural row.

**2. The version-1 check.** Asked: "F6-14: RO′-6's K̂ was checked equal to the rest of the block on version-0 stand-ins
only; for version 1 it is DECLARED. Is that enough for now?" His words:

> 2. F6-14 — Is the version-0 check enough for now?
>
> Adopt “Enough now; check before the pin.” Keep the evidence grades explicit: MEASURED on version-0 stand-ins; DECLARED for version 1. Record a version-1 check of RO′-6 as owed before CUT-0’s digest is pinned. This is a deferral, not evidence that version 1 satisfies the equality. It does not close the format-freeze question or authorize pinning before the check.

**3. How the re-reads converge before the push.** Asked: "How do re-reads converge before the push? Each re-read has
found drafting fixes, and each fix needs reading again before the build." His words:

> 3. Re-read convergence before the push
>
> Adopt “One more re-read, then gate.” Draft 6 should apply the dispositions from re-read 3 and these rulings. The twin then re-reads the clauses changed by draft 6 and the clauses affected by these rulings once. Any further drafting fixes must be recorded with their required re-read before the build, as R7 requires. Any issue needing your decision comes back to you; do not silently resolve it. Do not loop indefinitely merely to obtain a clean report, but do not waive a required re-read or build gate either.

**Excluded:** the record's notes after them, "what they fix" and "its re-reads" (lines 786–796).
