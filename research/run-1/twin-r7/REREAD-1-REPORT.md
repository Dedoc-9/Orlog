<!-- R7 re-read 1, saved by the draft's author, 2026-10-26: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 1: finding 24 (D) and the PREFIX licence — the twin's report

This is the reviewer's re-read under R7, point 4. It is review evidence: not a proof and not a ruling. Every probe in it is worked by hand and is **UNEXECUTED**. I say where I infer rather than read. I could not write files, so the whole report is below.

## 1. Provenance

**Files opened**, Read tool only, all in `twin-r7-reread1/`:

1. `REREAD-1-BRIEF.md`, whole.
2. `SPEC-15-DRAFT-2.md`, whole.
3. `RULINGS-AS-RULED.md`, whole.
4. `AR-F24-PREFIX.md`, whole.
5. `DRAFT-2-CHANGES.md`, whole.
6. `T10-STATEMENTS.md`, whole.
7. `SPEC.md`, lines 1–60 only.
8. `RUNTIME-SPEC.md`, lines 1–12 only.

**Partial reads.** For the rest of SPEC.md and RUNTIME-SPEC.md I relied on my full reading of the copies in `twin-r7-inputs/` during the review. I did not reopen those copies. The opening lines I read here match them, but I have not checked that the bodies are identical. Any difference in the parts I did not read would escape this re-read.

**Nothing else was opened.** I have the review and its report in context from the earlier task; I did not reopen them.

**SOURCE NEEDED** (named, not opened):
- **SN-A.** Court R1's text: what it requires, and when a reading is REFERENCE-ONLY. 15.13.11 says "(court R1, unchanged)" and "read with the witness the arbiter makes", and his words make R1 "a condition of HELD alongside E2". I cannot tell what witness the arbiter makes for a version-1 run before 1b.
- **SN-B.** The definitions of 1a and 1b.
- **SN-C.** D-18. 15.12.4 describes its boundary; the ruling texts only name it.
- **SN-D.** The version-0 court's grounding conditions (channels, ratified seal) and its order of standings. These are needed for "a ratified seal" (15.12.4) and for REFERENCE-ONLY's place among the standings.
- **SN-E.** `SPEC-15-DRAFT-1.md`, to check DRAFT-2-CHANGES' diff. I take the diff as computed and given.
- **SN-F.** D10's "two-commit split" (15.13.11, open).
- **SN-G.** The CUT-0 digest and the reach implementation, which 15.13.8 says is shared.

## 2. Ruling F24 (D for finding 24)

### 2.1 Faithfulness (clauses tagged `[ruled: F24]`)

- **Legend, `[ruled: F24]`.** "fixed by his ruling on finding 24 of R7's review: D10's court clause, scoped to real court readings." Faithful to his words, "the distinction between a real court reading (REFERENCE-ONLY until 1b, holding no claim) and 1a test rows".

- **15.12.5.**
  - Its first sentence quotes R6 word for word: "remains historically held, regardless of whether the execution loop encounters a subsequent transactional refusal downstream". The review's finding 23 is resolved.
  - "In 1a its row runs in the reference with the agreed witness configured (15.13.11). **[ruled: F24, for 1a]**" is faithful to packet A §5: "the PREFIX row ... run in 1a's reference with the witness configured as agreed".
  - Tag scope: the item's only tag is F24, while its first sentence is R6's, carried by the section tag. Read alone, the item tag seems to cover both (F24-4).

- **15.12.6, bullet 1.** "The configured witness covers the PREFIX row and its controls, not only ungrounded rows; results say configured, not measured." This is his condition 1, verbatim. Faithful.

- **15.12.6, bullet 2.** "In 1a these rows and their controls run in the reference with the agreed witness configured. No such row is evidence that the reference's version-1 arithmetic is right (15.13.11)."
  - Faithful to packet A §5.
  - Faithful to the forwarded proposal: "This does not make those test rows evidence that the reference's version-1 arithmetic is correct."
  - The adopted texts differ on mood. The proposal says the rows "may run in 1a"; packet A says they "run ... as R6's first rider requires". The draft follows packet A. Both texts are adopted (F24-7).

- **15.13.11, the main sentence and its rider.**
  - Verbatim packet A §5, without its label "D10, the court clause:". Faithful.

- **15.13.11, bullets.**
  - "'Court R1 remains a condition of HELD alongside E2.' The claims ruling is not amended (1 to 4)."
    - The first sentence is his.
    - "The claims ruling is not amended" is the proposal's.
    - "(1 to 4)" is added, and has two readings: 15.13.1–4, or the claims ruling's scope items 1–4 (F24-8).
  - Condition 1: verbatim. Faithful.
  - "A configured witness is not backend agreement" is faithful to the proposal's "A configured witness does not constitute independent backend agreement".
  - "No such row is evidence that the reference's version-1 arithmetic is right" is faithful.
  - "**only 1b's agreement can show that**" is ADDED. Neither adopted text says it. His scope sentence says the rulings do not "independently verify reference arithmetic", and the proposal lists as open "Whether the reference's version-1 execution arithmetic agrees with an independent backend". The added clause also overclaims against established doctrine (F24-1).
  - "D10's two-commit split is not ruled here. [open: D10, the split]" is consistent with the ruling, which does not mention a split.

- **Omitted from the adopted text.** The proposal's "E2 defines the claim-specific continuation condition; it does not erase the court's backend-agreement requirement." This is the sentence that reconciles 15.13.1 ("HELD means E2") with "Court R1 remains a condition of HELD alongside E2", and draft 2 does not carry it (F24-2).

- **Partly omitted.** His scope sentence, "it does not close T10/T11, establish CUT-0's soundness, or independently verify reference arithmetic", is stated for arithmetic only (F24-10).

### 2.2 Coherence (every clause of A_F24, in draft 2's text)

**Tag legend** (AR rows 4–8: R3–R6, claims, pinned, v0, open).
- Interpretable.
- "quoted words are his" holds for the quotes in 15.12 and 15.13.11. Packet B's text in 15.12.4 is adopted verbatim but not quoted, and that fits the legend.
- `[ruled: claims]` reads "E2, and the meet". After F24, holding also requires court R1, and the legend could say so. Minor.

**15.1.5; 15.3 "No value is invented, held over or defaulted"; the 15.15 row for 15.3/15.4.**
- These are textual matches only ("agree", "held over", "held across ticks"). The ruling does not affect them.

**15.4 "Three records, three authorities"; 15.8 "The core".**
- Unaffected in their text.
- One gap: a 1a row's configured witness is neither an execution's core nor "the arbiter's agreement record", and nothing says how a configured result is recorded or labelled so that it is never read as one. Condition 1 says "results say configured, not measured", but 15.4 has no slot for it (F24-11).

**15.9 (the 'R' event).**
- Unaffected. A 1a row still has to name CUT-0's withholding row, so the open question of whether 'R' carries the cut (finding 20) bears on 1a rows. The reference can compute the row internally without the trace.

**15.11 Replay; "never reported as validity".**
- Consistent with "configured, not measured".
- 15.11's second bullet, "Agreement ... is never reported as validity", conflicts with 15.13.11's added "only 1b's agreement can show that [the arithmetic is right]" (F24-1).

**15.12.2.**
- "GROUNDED also requires held, as in version 0" combines with 15.13.11 to give this consequence: before 1b, **no claim of a version-1 run reads GROUNDED in a real court reading, a licensed one included.**
- That follows from the text but is stated nowhere. The tag (`[ruled: R6]`; `[v0]`) does not name F24, on which it now depends (F24-2's tag audit).

**15.12.3.**
- "The court shows the log's seal as provenance for the run". Read per run, it holds in a REFERENCE-ONLY reading as in a 1a row. Coherent.
- The review's finding 47, on whether the line prints for PREFIX claims, is resolved as "for the run".

**15.12.5.**
- The R6 sentence ("remains historically held") has no scope. In a real reading before 1b, 15.13.11 holds no claim.
- The draft scopes only the row ("In 1a its row runs ..."). It does not say what the R6 sentence means in a real reading: held once R1 is met (after 1b), and not before. A reader must infer that 15.13.11 governs (F24-3).

**15.12.6.**
- Coherent with 15.13.11.
- Condition 1 extends the configured witness to "the PREFIX row and its controls". One of R6's controls "evaluates the exact same claim without an active log declaration": that is a version-0 run, outside D10, for which the arbiter can make a real witness. Read literally, the condition makes that control "configured, not measured" too (F24-6).

**15.13.1–15.13.4.**
- "HELD means E2" (15.13.1) and "a claim is held only when the court's R8 holds it and CUT-0 holds it" (15.13.4) now sit beside "Court R1 remains a condition of HELD alongside E2".
- 15.13.4's "only when" gives necessary conditions, so adding R1 is consistent with it.
- 15.13.1's "means" reads as a definition, and with R1 that looks like a contradiction. The ruling resolves it in words the draft omits (F24-2).
- Neither clause's tag names F24.

**15.13.5 (the court's R8, pinned).** Unaffected.

**15.13.11.**
- One reading for real readings and for rows.
- Undefined here: what "the witness the arbiter makes" is for a version-1 run before 1b (SN-A). I infer it shows only the reference, so court R1 yields REFERENCE-ONLY.
- Missing: where REFERENCE-ONLY stands among the standings a real reading prints for a claim that is refuted (CLAIM-REFUTED), refused at its own clause (R8), UNREACHED, or ungrounded. 15.13.12 orders only "R8's refused evaluation first ... then UNREACHED" (F24-5).

**15.14.**
- Open. Consistent. "configured presented as measured" would fit its forbidden interpretations; not required.

**15.15's closing line** (replacing the removed row).
- Accurate about what is now ruled.
- But the table has no row for D10's two-commit split, which 15.13.11 tags open (DRAFTING, F24-12).

**Clauses outside A_F24 that the ruling touches.** These are D_r candidates, recorded under AR's rule that a dependency found later enters D_r:
- 15.13.6: "CUT-0 holds a claim". The term match took "held/HELD" and missed "holds".
- 15.13.10: T10/T11 and CUT-0's soundness, which his scope sentence covers.
- 15.13.12: the order of standings, which REFERENCE-ONLY enters (F24-9).

### 2.3 Probes for F24 (UNEXECUTED)

The grounding probes assume the claim's channel can ground and its seal is ratified. I write the default `computation` oracle; whether it grounds is SN-D.

**FP-1. Licensed claim, COMPLETED.**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Each tick, do the following.`
  - `2.1. Say 1.`
- Log: `t 1`, `end 1 closed`.
- Run: COMPLETED; ticks 1.
- Real reading:
  - REFERENCE-ONLY; holds no claim;
  - so the claim is not GROUNDED (15.12.2);
  - provenance line printed for the run;
  - "true in 1 of 1" as description.
- 1a row:
  - witness configured, so R1 is met by configuration;
  - meet: R8 holds, and CUT-0 at COMPLETED has K̂ empty (15.13.8), so held;
  - licensed (PX-1 below), so GROUNDED if the channel grounds;
  - the row states "configured, not measured".
- Exercises: 15.12.2, 15.12.5, 15.12.6, 15.13.4, 15.13.11.

**FP-2. Unlicensed claim (the ungrounded-port row).**
- Law:
  - `1. Let a be given each tick as an integer.`
  - `2. We claim that 2 plus 2 equals 4.`
  - `3. Each tick, do the following.`
  - `3.1. Say a.`
- Log: `t 1 490000000000000003`, `end 1 closed`.
- Real reading: REFERENCE-ONLY.
- 1a row: held (meet; K̂ empty at COMPLETED); NOT GROUNDED (R6, unlicensed); provenance line; configured.
- Its PREFIX control moves the claim above clause 1, and reads GROUNDED, configured.

**FP-3. The version-0 control.**
- Law: `1. We claim that 2 plus 2 equals 4.` alone.
- A version-0 run, outside D10.
- Under condition 1, its witness is configured, so it reads GROUNDED "configured, not measured", although a measured version-0 witness exists. Whether that is intended is F24-6.

**FP-4. A claim with no completed evaluation.**
- Law:
  - `1. Let n be 5.`
  - `2. Each tick, at most 2 operations, do the following.`
  - `2.1. We claim that n plus 1 is greater than 0.`
- Run: `REFUSED TICK-BUDGET 3`; ticks 1; tick-ops 3; ops 4; `claim 0 3 0 0 0 0 0`.
- 1a row: R8's refused evaluation first (15.13.12).
- Real reading: REFERENCE-ONLY, or R8's refused evaluation? **Not determined by §15** (F24-5).

### 2.4 Findings, F24

| # | class | finding | needs a ruling |
|---|---|---|---|
| F24-1 | COHERENCE | "only 1b's agreement can show that" is added to the ruling. It contradicts SPEC §14 ("Agreement on these samples is consistency between two readers of one text ...; it is not a proof that either reads the text rightly") and 15.11's "never reported as validity". | no (drafting fix) |
| F24-2 | DRAFTING | 15.13.1's "HELD means E2" next to R1 as a condition of HELD. The adopted reconciling sentence ("E2 defines the claim-specific continuation condition; it does not erase the court's backend-agreement requirement") is omitted, and 15.13.1, 15.13.4 and 15.12.2 do not tag F24. | no |
| F24-3 | DRAFTING | 15.12.5's R6 sentence is not scoped for real readings before 1b, where 15.13.11 holds no claim. | no |
| F24-4 | DRAFTING | 15.12.5's item tag "[ruled: F24, for 1a]" reads as covering its R6 sentence. | no |
| F24-5 | GAP | Where REFERENCE-ONLY stands among the standings a real reading prints (refuted, R8, UNREACHED, ungrounded) is not stated (SN-A, SN-D). | yes, unless the court as built already decides it |
| F24-6 | QUESTION | Condition 1 makes even the version-0 control (no log) configured, though a measured witness exists for version 0. | yes, if a measured version-0 control is wanted |
| F24-7 | QUESTION | The adopted texts differ: the rows "may run" (proposal) or "run ... as R6's first rider requires" (packet A). The draft follows packet A. | no (both adopted; noted) |
| F24-8 | DRAFTING | "(1 to 4)" after "The claims ruling is not amended" is not his and has two readings. | no |
| F24-9 | GAP | A_F24 misses 15.13.6 ("holds"), 15.13.10 (his scope: T10/T11, CUT-0's soundness) and 15.13.12 (the order of standings). D_r candidates. | no |
| F24-10 | DRAFTING | His scope sentence is stated only for arithmetic. | no |
| F24-11 | GAP | Nothing records or labels a configured witness so that it can never be read as an arbiter's agreement record (15.4) or a core (15.8). | no (reporting row) |
| F24-12 | DRAFTING | 15.15 has no row for D10's open two-commit split. | no |

## 3. Ruling PREFIX (B1 + 4a + 5c + K1)

### 3.1 Faithfulness (clauses tagged `[ruled: PREFIX]`)

**Legend.** "B1 + 4a + 5c + K1, with its conditions" are his words. Faithful.

**15.0 Prefix, its last sentence.** "The prefix is not the PREFIX licence: a claim of the prefix is licensed only as 15.12.4 says. [ruled: PREFIX, for this sentence]"
- No adopted text says this. It is a correct gloss, but a gloss tagged as ruled (PREFIX-7).

**15.0 Boundary.** "the first top-level clause, in the text, that is or holds a port declaration, or is the tick block. A law with a tick block and no port has its boundary at the tick block."
- Verbatim from packet B §4 and the proposal. Faithful.
- The proposal's "of either kind" is implied by the unqualified "a port declaration".

**15.12.4, "The licence as ruled".**
- Packet B §4 verbatim, from "The licence is decided from the law's text alone" to "licenses no claim of the law". Faithful.
- R6's own licence text above it is now verbatim too: "decided from the text" and "must stand" are restored. The review's finding 2 is resolved.
- Its bullets:
  - "A law with a tick block and no port has its boundary at the tick block." Faithful.
  - "A claim after an each-tick port declaration is not licensed merely because it never reads that port." Faithful.
  - "D-18's boundary, the first read-once declaration or the tick block, is not adopted: it would widen R6." The adopted text says only "D-18's alternative boundary is not adopted; using it would widen R6." The description of D-18's boundary comes from outside the ruling texts (SN-C; PREFIX-8).
  - "'Reach fails closed on unknown statement kinds, including the version-1 tick-block case.'" Condition 2, verbatim.
  - "The version-0 default, a statement kind with no rule adding nothing to the closure, does not establish it." This paraphrases "The existing version-0 default behavior is not enough to establish this". The gloss on what the v0 default is is the draft's. Minor.
  - "'An independent structural oracle checks PREFIX licensing; the trace is a check, not the rule.'" Condition 3, verbatim.
  - "A licence is not a standing. A licensed claim still needs held, a ratified seal and a channel that can ground to read GROUNDED (2)." The adopted text says "A licensed claim must still satisfy the existing settlement rules. Licensing is not `GROUNDED` or `HELD` by itself." The draft names the settlement rules. I cannot check "a ratified seal" against version 0 (SN-D; PREFIX-10).
  - "Sound, not complete: a claim may be excluded although no execution of it reaches a path that depends on input." **ALTERED.** The adopted text is "a claim may be conservatively excluded even when a particular execution would never reach an input-dependent path." "No execution" quantifies over all executions where his text speaks of "a particular execution" (PREFIX-9).
  - "The licence presupposes that no input binds before the boundary's position (15.7.1). [open: finding 6]" Not in the ruling, and correctly tagged open.

**15.13.8's closing line.** Tagged "[ruled: PREFIX, condition 2; pinned, its use here]".
- Text: "The PREFIX licence uses this same reachability (15.12.4), and it fails closed: a statement kind it has no rule for, the tick block's case included, is taken to be able to execute every claim of the law."
- **ALTERS the ruled text in two ways.**
  - (i) Packet B §4, adopted verbatim: "A statement kind the closure has no rule for licenses no claim of the law." That acts on the whole law. The draft's "is taken to be able to execute every claim" acts only where the clause of that kind stands. The two differ when an unknown kind stands before the boundary (PX-7; PREFIX-2).
  - (ii) "the tick block's case included" makes the tick block a kind "it has no rule for". The adopted texts give the closure a rule for it: packet B, "The closure follows every arm, the body of every loop and of the tick block"; the proposal, "The closure follows all branches, loop bodies, tick bodies". (PREFIX-1)
- "The PREFIX licence uses this same reachability" is an integration claim (I-9), not ruled text.

### 3.2 Coherence (every clause of A_PREFIX, in draft 2's text)

**Findings 3, 4 and 5 against the ruled licence (verified by hand only).**
- Finding 3: a claim after any port declaration is unlicensed, since the boundary is at the first declaration of either kind (PX-2).
- Finding 4: in a tick-only law the boundary is the tick block. A claim in a procedure performed from the tick block fails (b) (PX-3).
- Finding 5: "licensed exactly when" gives sufficiency.
- B1 implies R6's necessary conditions:
  - (a), "before the boundary", implies "before the first port declaration";
  - (b) implies "not in a procedure performed at or after the first port declaration";
  - (b), together with 15.12.4's presupposition, implies "every evaluation of it precedes the first input".
- So the ruled licence is no wider than R6, **provided** the presupposition holds (PREFIX-6).

**15.0 Version 1 law, Port, Arrival, Input log, Execution.**
- Unaffected and interpretable.

**15.0 Prefix and Tick block.**
- "Prefix" (statements before the tick block) and "boundary" (which may come earlier) are kept apart. The sentence that says so is correct.
- The licence uses both "exempt" (R6) and "licensed" (PREFIX) without saying they name one thing (PREFIX-11).

**15.0 Boundary.**
- One reading, with one vacuous part: "holds a port declaration" can never apply under 15.1.3's proposal, which allows ports only at top level. It is harmless, and robust if port places change (PREFIX-15).
- A law with ports and no tick block (open finding 7) has a defined boundary.

**15.1.3 (open).**
- Consistent with the boundary.
- If the open "by evaluation" reading of a read outside the tick block is chosen, it should use the same reach. Its tag does not name PREFIX (tag audit).

**15.1.6.**
- His sentence, "every later claim in the run ... even if they never touch that property directly", agrees with B1: a claim stands after the port, or is executed from the boundary on.
- Its tags (R1 open, R6) do not name PREFIX, which now decides which claims are "later" (tag audit).

**15.2.3.** A textual match only ("raw prefix"). Unaffected.

**15.3, the read-once bullet; 15.7.1.**
- 15.7.1 now records that "The PREFIX licence presupposes this place". 15.3's bullet does not.
- More important: the licence **constrains** the open choice in finding 6. R5 allows a read-once binding anywhere before the first 'T'. A binding placed before the boundary (for example at the start of the run) would leave B1 licensing claims that R6's "every evaluation of it precedes the first input" excludes (PX-12). The draft calls this a presupposition; it does not say that finding 6 must respect it (PREFIX-6).

**15.5 (the log).**
- "The licence is decided from the law's text alone, never from a log" is independent of the log. Coherent.
- Problem: draft 2 says "The log is parsed whole before any execution starts". Draft 1 dropped "Input point" (AR's note), and draft 2 defines no "first input". A reader can then take the load as R6's "first input": no evaluation would precede it, R6's necessary condition could never be met, and the licence would be empty.
- 15.12.4's presupposition ("no input binds before the boundary's position") implies that first input means first binding. The draft should say so (PREFIX-5).
- 15.5's other clauses are unaffected.

**15.7.5; 15.10's T(1).c.**
- "Prefix" in its own sense. Unaffected.
- One check: for NOT-RUN and LOG-OPEN, K̂ is "the tick block and every procedure performed from it". By (b), no licensed claim is in it. For any refusal at or after the boundary, K̂ is built from frames at or after the boundary, so again no licensed claim is in it. 15.12.5's "remains historically held" therefore agrees with CUT-0 for every refusal from the boundary on.
- A refusal **before** the boundary can withhold a licensed claim that evaluated true, through the rest-of-block row (PX-10). This agrees with R6 only if his "the execution loop" means the ticks, as his reason ("a downstream failure on frame t") suggests (PREFIX-16).

**15.12.1–15.12.3.**
- Coherent. The tick-only trigger matches the tick-only boundary. Licence and standing are kept apart.

**15.12.4.**
- Interpretable, except for four points:
  - which kinds the closure "has a rule for" (PREFIX-3);
  - the two fail-closed effects (PREFIX-2);
  - the tick-block reading (PREFIX-1);
  - what "no clause from the boundary on may execute it" reaches inside a To body, or from a Define, that stands after the boundary and is never performed (PREFIX-4).
- On PREFIX-4: draft 2's "uses this same reachability" (K̂'s "may execute", where a To clause executes nothing at run time, SPEC §7) favours the reading that an unperformed To adds nothing. The packet's textual words "no clause from the boundary on" favour the stricter reading.

**15.12.5–15.12.6.**
- "A PREFIX claim" and "wraps it ... within the PREFIX license parameters" now mean B1-licensed. Coherent.
- Under reading A of PREFIX-1, **no claim of any law with a tick block is licensed**. R6's ruled control ("wraps it securely within the PREFIX license parameters ... must return a clean GROUNDED standing") could then never be met in such a law.

**15.13.7 (the continuation, pinned).**
- "values are unknown" and "relative to the law" agree with the licence's "with values ignored".

**15.13.8 (the cut and K̂, pinned) and its closing line.**
- K̂'s rows include rules for the tick block: "its body again" and "K̂ is the tick block and every procedure performed from it".
- The closing line counts the tick block among the kinds "it has no rule for". That contradicts these rows inside the same clause (PREFIX-1).

**15.13.11.**
- The PREFIX row runs in 1a with the witness configured. Coherent.

**15.15 rows (15.1.3, 15.2, 15.3/15.4, 15.5/15.6) and the closing line.**
- Coherent.
- The table has no row for the closure's rule table (PREFIX-3) or for the condition-2 reading (PREFIX-1).
- Finding 6's presupposition sits only implicitly under the 15.3/15.4 row.

**Tag audit, PREFIX.**
- 15.1.6 should name PREFIX.
- 15.3's read-once bullet should name PREFIX (its presupposition).
- 15.1.3's open "by evaluation" reading shares the reach.
- 15.1.1's forms are statement kinds the closure must have rules for, so condition 2 reaches them.
- 15.0's Prefix sentence is tagged ruled but is a gloss.
- 15.13.8's closing line is tagged ruled but alters the ruled text.

**D_r candidates missing from A_PREFIX:**
- 15.1.1 (the port declaration and the budgeted tick block are statement kinds that need closure rules);
- SPEC §3's statement table (every version-0 kind needs an explicit rule, since "The version-0 default ... does not establish it");
- 15.13.6.

### 3.3 Probes for PREFIX (UNEXECUTED)

Grounding probes assume the channel can ground and the seal is ratified (SN-D). Two readings, used throughout:
- "1a" means the row's reading, with the witness configured.
- "Real" means the reading with the arbiter's witness: REFERENCE-ONLY before 1b, so no claim is held or GROUNDED.

**PX-1. Tick-only law, claim in the prefix.**
- Law: FP-1's law.
- Boundary: clause 2. The claim is at clause 1, so (a) holds. The tick body executes no claim, so (b) holds. **Licensed** under reading B of PREFIX-1; **not licensed** under reading A (15.13.8's literal closing line).
- 1a: held at COMPLETED; GROUNDED (configured) under B.
- Real: REFERENCE-ONLY.

**PX-2. Claim after an each-tick port declaration.**
- Law: FP-2's law. Boundary: clause 1.
- The claim stands after the boundary, so it is **not licensed**, though it never reads `a`.
- 1a: held, not GROUNDED, provenance line.

**PX-3. Tick-only law, procedure performed only from the tick block.**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Each tick, do the following.`
  - `2.1. Perform check.`
- Boundary: the tick block (id 3).
- (a) holds. (b) fails, since clause 4 performs `check`. **Not licensed**. The review's P15 is now decided.
- 1a: held at COMPLETED; withheld at LOG-OPEN (row "the tick block's next tick").

**PX-4. Procedure performed only before the boundary.**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Perform check.`
  - `3. Let g be given as an integer.`
  - `4. Each tick, do the following.`
  - `4.1. Say g.`
- Boundary: id 4.
- No clause from it on performs `check`. **Licensed**, given rules for each kind present (PREFIX-3).

**PX-5. Performed again after the boundary.**
- Law: PX-4 with `4. Perform check.` inserted after the port, and the tick block renumbered 5.
- **Not licensed** (b).

**PX-6. A To after the boundary that is never performed.**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Perform check.`
  - `3. Let g be given as an integer.`
  - `4. To later, do the following.`
  - `4.1. Perform check.`
  - `5. Each tick, do the following.`
  - `5.1. Say g.`
- `later` is never performed.
- Textual reading: clause 4.1 is a clause from the boundary on that may execute the claim, so **not licensed**.
- Reachability reading (a To executes nothing; reach follows Performs from the top-level clauses from the boundary on): **licensed**.
- **Not determined by §15** (PREFIX-4). And if To has no closure rule, fail-closed removes the licence anyway (PREFIX-3).

**PX-7. An unknown kind before the boundary.**
- Law:
  - `1. Decimals are fixed.`
  - `2. We claim that 2 plus 2 equals 4.`
  - `3. Each tick, do the following.`
  - `3.1. Say 1.`
- If the closure has no rule for Decimals:
  - 15.12.4 (packet B) says "licenses no claim of the law", so **not licensed**;
  - 15.13.8's form makes Decimals "able to execute every claim", but it stands before the boundary, so (b) is untouched and the claim is **licensed**.
  - The two readings diverge (PREFIX-2).
- If the closure has a rule for Decimals: licensed under both. The outcome waits on the rule table (PREFIX-3).

**PX-8. The tick block under 15.13.8's literal closing line.**
- Any law with a tick block: the tick block stands at or after the boundary and "is taken to be able to execute every claim of the law", so **no claim is licensed**.
- R6's PREFIX-wrapped control cannot then read GROUNDED in a version-1 run (PREFIX-1).

**PX-9. Licensed claim; a refusal at a tick.**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Let a be given each tick as an integer.`
  - `3. Each tick, do the following.`
  - `3.1. Say 10 divided by a.`
- Log: `t 1 490000000000000000`.
- Run: `REFUSED DIVISION-BY-ZERO 4`; ticks 1; tick-ops 2; ops 5; `claim 0 1 1 1 2 0 0`.
- Licensed (boundary at 2).
- 1a: R8 holds (4 ≠ 1). CUT-0's K̂ is clause 4 only, so the claim is not in it: held, and GROUNDED (configured). This is 15.12.5's row.
- Real: REFERENCE-ONLY.

**PX-10. Licensed claim; a refusal before the boundary.**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Perform check.`
  - `3. Say 1 divided by 0.`
  - `4. Perform check.`
  - `5. Let g be given as an integer.`
  - `6. Each tick, do the following.`
  - `6.1. Say g.`
- Licensed (both Performs stand before the boundary at id 6).
- Run: `REFUSED DIVISION-BY-ZERO 4`; ticks 0.
- CUT-0: the rest of the block includes `4. Perform check`, so the claim is withheld, row "the rest of a block". A licensed claim that evaluated true is **not held**.
- This agrees with 15.12.5 only if "the execution loop" means the ticks (PREFIX-16).

**PX-11. A claim in a loop before the boundary.**
- Law:
  - `1. For each i from 1 to 2, do the following.`
  - `1.1. We claim that i is positive.`
  - `2. Each tick, do the following.`
  - `2.1. Say 1.`
- **Licensed**. 1a: held at COMPLETED; GROUNDED (configured).

**PX-12. Binding before the boundary (depends on open finding 6).**
- PX-4 with `g` bound at the start of the run, which R5 allows ("before the first 'T'").
- B1, decided from the text, still licenses the claim. R6's "every evaluation of it precedes the first input" fails.
- B1 would then be wider than R6 (PREFIX-6).

**PX-13. Ports and no tick block (open finding 7).**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Let g be given as an integer.`
  - `3. Say g.`
- Boundary: id 2. **Licensed**, if the law is accepted at all (15.1.3, open).

**PX-14. Two port kinds, each-tick first.**
- Law: `1. Let a be given each tick as an integer.`, `2. We claim that 1 is positive.`, `3. Let g be given as an integer.`, `4. Each tick, do the following.`, `4.1. Say a plus g.`
- Boundary: clause 1 (either kind).
- The claim at 2 is **not licensed**, though it precedes the read-once declaration. Under D-18's boundary it would be licensed, which is why D-18 widens R6.

### 3.4 Findings, PREFIX

| # | class | finding | needs a ruling |
|---|---|---|---|
| PREFIX-1 | COHERENCE | Condition 2's "including the version-1 tick-block case" has two readings. (A) The tick block is a kind with no rule, so no claim of any tick-block law is licensed, and R6's PREFIX control can never read GROUNDED. (B) The closure must have an explicit rule for the tick block (follow its body), as packet B and the proposal say ("follows ... tick bodies"), and must not fall to the version-0 default. 15.13.8's closing line states (A), against its own K̂ rows. | **yes** (his confirmation of B, or a ruling) |
| PREFIX-2 | COHERENCE | Two fail-closed effects: packet B, verbatim, "licenses no claim of the law" (the whole law), against 15.13.8's "able to execute every claim" (only where the clause stands). They differ for an unknown kind before the boundary (PX-7). 15.13.8 is tagged as ruled but alters. | no for PREFIX (packet B governs); the K̂ form is pinned |
| PREFIX-3 | GAP | The closure's rule table is not given: which kinds have a rule, and what rule (version-0 simple statements, If/Unless/Otherwise, loops, Perform, To, Define, Decimals, port declarations, the budgeted tick block). Without it, fail-closed is undetermined in effect, and could license nothing. | yes, or a pinned artifact the ruling names |
| PREFIX-4 | QUESTION | "No clause from the boundary on may execute it" for a To body or a Define that stands after the boundary and is never performed (PX-6): the textual reading excludes the claim, the reachability reading licenses it. | yes |
| PREFIX-5 | DRAFTING | "First input" (R6) is undefined since "Input point" was dropped. 15.5's whole-log parse before execution can be read as the first input, which would empty the licence. The presupposition implies first binding; state it. | no (depends on finding 6) |
| PREFIX-6 | COHERENCE | B1 agrees with R6's "every evaluation precedes the first input" only if no input binds before the boundary. R5 permits earlier binding, so the PREFIX ruling constrains finding 6's open choice. The draft does not say so. | yes (with finding 6) |
| PREFIX-7 | DRAFTING | 15.0's "The prefix is not the PREFIX licence ..." is tagged ruled but is a gloss. | no |
| PREFIX-8 | DRAFTING | 15.12.4 describes D-18's boundary under a ruled tag; the ruling texts only name D-18 (SN-C). | no |
| PREFIX-9 | DRAFTING | "excluded although no execution of it reaches" alters the adopted "even when a particular execution would never reach". | no (restore his text) |
| PREFIX-10 | QUESTION | "held, a ratified seal and a channel that can ground" specifies "the existing settlement rules". I cannot check "ratified seal" against version 0 (SN-D). | no, if version 0 confirms |
| PREFIX-11 | DRAFTING | "exempt" (R6) and "licensed" (PREFIX) are used without being equated. | no |
| PREFIX-12 | DRAFTING | Tag audit: 15.1.6, 15.3's read-once bullet and 15.1.3 do not name PREFIX. 15.0's sentence and 15.13.8's closing line carry ruled tags for text that is not his. | no |
| PREFIX-13 | GAP | A_PREFIX misses 15.1.1, SPEC §3's statement table (as the source of the kinds needing rules) and 15.13.6. D_r candidates. | no |
| PREFIX-14 | DRAFTING | 15.15 has no row for the rule table or the condition-2 reading. Finding 6's presupposition is only implicit there. | no |
| PREFIX-15 | DRAFTING | "holds a port declaration" can never apply under 15.1.3's proposal. Harmless. | no |
| PREFIX-16 | QUESTION | A licensed claim can be withheld by a refusal before the boundary (PX-10). This agrees with R6's "regardless of ... a subsequent transactional refusal downstream" only if "the execution loop" means the ticks. | no, if that reading is confirmed |

## 4. T10.5, apart

The statement: "On the stack, a procedure returns only to the frame below it, the actual caller. Since there is no recursion, each procedure has at most one frame on the stack, so the cut names each call without ambiguity. Reached in the continuation, its whole body counts, transitively. *(Reworded ...)* Refused at its own operation (version 1 only), its body follows".

- **The review's finding 42 is resolved.** "Since there is no recursion" now supports uniqueness, not the return.
- **The inference is valid given SPEC §5.** A procedure may perform only procedures it follows, so calls follow definition order and the call graph has no cycle. Along one stack, a procedure appears at most once, and with it every clause id inside its body. Top-level clauses and the tick block appear at most once.
- **T10.5-1, DRAFTING.** "Each procedure has at most one frame" should say "one activation". A procedure's activation spans several frames: its Perform, then the statements of its body, such as an If or a For inside it. Read literally, a body with a nested If already has two frames. No ruling needed.
- **T10.5-2, DRAFTING.** "Names each call without ambiguity" also needs the arm selector. Draft 2's 15.13.8 makes an inline arm's statement "a frame of its own, directly above its If's frame, named by the If's clause and its arm", so two frames share a clause id. That is consistent with 15.9's "u16 selector", but T10.5's uniqueness argument does not mention it. No ruling needed.
- **T10.5-3, DRAFTING.** The editorial parenthesis sits inside the statement, before its last sentence. No ruling needed.
- **Match with 15.13.8.** The row "a Perform below the top: a return only to the frame below it, the actual caller (T10.5)" matches. An inline Perform now has its own frame, which removes my earlier doubt about inline Performs.
- **Nothing here is proved.**

## 5. The added clauses, title and status

- **Title and status paragraph.** These are accurate against DRAFT-2-CHANGES. "nothing here clears a blocker" and "read again before it is built (R7)" carry his condition 4. I could not verify the claim that no clause outside the two sets changed (SN-E).
- **The legend's two entries.** Read in 2.1 and 3.1.
- **15.0 Boundary.** Read in 3.1 and 3.2.
- **15.15's closing line.** Read in 2.2: accurate, but the table lacks rows for D10's split, the rule table and the condition-2 reading.

## 6. What needs a ruling, in order of weight

1. **PREFIX-1:** the tick-block reading of condition 2. Reading A empties the licence for every law with a tick block.
2. **PREFIX-3:** the closure's rule table, without which fail-closed is undetermined.
3. **PREFIX-6:** the binding place (finding 6) must not precede the boundary, or B1 is wider than R6.
4. **PREFIX-4:** whether an unperformed To or a Define after the boundary excludes a claim.
5. **F24-5:** REFERENCE-ONLY's place among printed standings, unless the court as built decides it.
6. **F24-6:** whether the version-0 control is to be measured rather than configured.

Everything else is drafting that needs no ruling, with one exception: F24-1, the added "only 1b's agreement can show that", needs no ruling but should come out before anything is built, because it contradicts the established doctrine that agreement is consistency, not proof.
