<!-- R7 re-read 2, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 2: the labels' definitions, the closure's rule table, and R6's control (the twin's report)

This is the same reviewer's second re-read under R7, point 4. It is review evidence: not a proof and not a ruling. Every probe is worked by hand and is **UNEXECUTED**. Every fixture outcome given below is **my own worked consequence**. None is the draft's or the owner's: his words are that the table *"does not establish that any individual claim, including PX-6, is licensed"*.

## Summary

Draft 3 answers most of my first re-read's findings, but two gaps remain that matter before anything is built:

- **LABELS-1.** K1's start set is adopted but not written into the draft. Without it, the draft's own words still leave PX-6 (the unperformed To after the boundary) undecided, so PREFIX-4 is not yet answered in the text.
- **TABLE-1.** The ruled table names only "Perform". If the bare procedure-name call is read as a different kind, its last row would leave every law that uses one with no licensed claim. This needs a one-line confirmation.

Findings by group:

| group | findings |
|---|---|
| LABELS | 6 |
| TABLE | 5 |
| V0CTL | 4 |
| LATE | 3 |
| CHANGED | 4 |
| T10.5 | 1 |

None needs a ruling outright. TABLE-1 needs his confirmation of a reading, and V0CTL-1 and V0CTL-2 would need a ruling only if their default readings are not what he meant.

## 1. Provenance

**Files opened**, Read tool unless stated, all in `twin-r7-reread2/`:

1. `REREAD-2-BRIEF.md`, whole.
2. `SPEC-15-DRAFT-3.md`, whole.
3. `DRAFT-3-CHANGES.md`, whole.
4. `RULINGS-AS-RULED.md`, lines 165–330: the end of the claims ruling, the 2026-10-26 section, and the 2026-10-27 section.
5. `AR-REREAD-2.md`, whole.
6. `T10-STATEMENTS.md`, whole.
7. `AR-F24-PREFIX.md`, one Grep search for its section heading, then lines 140–158.

**Not reopened:**
- `RULINGS-AS-RULED.md` lines 1–164 (R3–R6 and the claims ruling). The brief says they are as before, and I rely on my reading of them in re-read 1.
- `SPEC.md` and `RUNTIME-SPEC.md`. I rely on my earlier full reading of the copies in `twin-r7-inputs/`. The brief says the bytes are the same; I did not check the sha256 values myself.
- `SPEC-15-DRAFT-2.md`, as I read it in re-read 1 and still have it in context, used only for comparisons. It is not in this folder.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** Packet B §3.3 in context. 5c's adopted definition says "bullet 1, plus the closure in §3.4", and I cannot tell which bullet "bullet 1" is (LABELS-2).
- **SN-2.** The court as built. It is needed for 15.13.11's new [v0] sentence, "REFERENCE-ONLY is the integrity column, as the court as built prints it".
- **SN-3.** `REREAD-1-DISPOSITION.md`. It would show how F24-7, PREFIX-15 and PREFIX-16 were disposed; draft 3 does not claim to answer them.
- **SN-4.** Court R1's text. This is still needed, as before.

---

## 2. Ruling 1: the labels' definitions (D, B1, 4a, 5c, K1), adopted without their conclusions

### 2.1 Faithfulness (clauses carrying the labels ruling)

**The legend, `[ruled: PREFIX]`.**
- "and by his rulings on the labels' definitions and the closure's rule table ... A label's definition is ruled, not the conclusions drawn from it."
- Faithful to "adopt the definitions, but do not automatically accept the claimed downstream conclusions".

**The legend, `[ruled: F24]`.**
- It names his control ruling. It does not name the labels ruling, which adopts D's definition (LABELS-3).

**15.0 Boundary [ruled: PREFIX].**
- This is B1's adopted "PROPOSED WORDING" and 4a. Faithful.
- B1's own label line defines the boundary differently (LABELS-4).

**15.12.4, "The licence as ruled".**
- "'Reach fails closed on unknown statement kinds, including the version-1 tick-block case.' 'The tick block must have its own closure rule that follows its body.'" Both are his words, verbatim. PREFIX-1 is answered, as reading B.
- "A default that adds nothing for a kind it does not name does not establish either."
  - This is the draft's gloss, not his words.
  - It is close to the adopted "The existing version-0 default behavior is not enough to establish this".
  - "Either" widens "this" to cover both quotations. That is harmless (LABELS-5).
- "R6's word exempt and the ruling's word licensed name one thing, as 5c's adopted definition writes it (*Exempt exactly when the static test holds*). [ruled: PREFIX, 5c's definition]"
  - The italics are 5c's adopted text, correctly not presented as his words.
  - But the identity is drawn from the definition, not stated in it: it depends on what "bullet 1" is (LABELS-2).

**K1's definition is stated only in part.**
- Stated in draft 3:
  - "It follows every If arm and the Otherwise, every loop body, the tick block's body, and every Perform transitively" (by packet B's text and the table);
  - "A statement kind it does not know licenses no claim (fail closed)".
- **Not stated anywhere in draft 3:** "Its start set is the top-level clause that is or holds the boundary, plus every later top-level clause" (LABELS-1).

**D's definition** is stated in substance in 15.13.11, as before.

### 2.2 Coherence (every clause of A_LABELS, in draft 3's text)

**Status paragraph; legend.**
- Interpretable. The status names all three rulings correctly.
- The title's date is stale (CHANGED-1).

**15.0 Prefix.**
- Now a pointer: "(Not the PREFIX licence: which claims are licensed is 15.12.4's.)". PREFIX-7 is answered.
- The parenthesis stands after the clause's [open] tag, so a reader could take it as part of the open proposal. That is harmless, because it only points.

**15.0 Boundary.**
- Interpretable. It agrees with 15.1.3's open places.

**15.2.3.**
- A textual match only ("lower negative boundary"). Unaffected.

**15.7.1.**
- Unchanged. The binding-place presupposition is tagged open and cross-referenced. Coherent.

**15.12.2.**
- The new sentence "So before 1b no claim of a version-1 run, a licensed one included, reads GROUNDED in a real court reading ... [ruled: F24]" follows from "holds no claim" and "GROUNDED also requires held [v0]".
- It is a conclusion carrying a ruled tag (LABELS-6).

**15.12.4 (R6's text).**
- Unchanged and verbatim. Coherent with B1 and 5c, under 15.1.3's open places.

**"The licence as ruled".**
- Interpretable, except for one gap: without K1's start set, "(b) no clause from the boundary on may execute it" still allows the textual reading I raised as PREFIX-4.
  - On that reading, a `Perform` inside a To's body that stands after the boundary is itself "a clause from the boundary on".
  - The table's "To | no further reachable body" does not reach that `Perform` on either reading. The question is only whether the inner clause is a starting point.
  - K1's start set (top-level clauses only) settles it. The draft does not state it (LABELS-1; probe R2-P1).
- R6's "first input", defined in the open bullet as "the first port value bound, or the first 'T' in a law with no port; never the loading of the log". This answers PREFIX-5, as a proposal, consistently with 15.7.1 and 15.5 (probe R2-P10).

**15.12.5; 15.12.6.**
- Coherent with D. Read under V0CTL below.

**15.13.8.**
- The altered closing line is removed, and draft 1's "What 'may execute' reaches includes every procedure performed, transitively" is back. PREFIX-1 and PREFIX-2 are answered.
- Now nothing ties K̂'s "may execute" to the ruled table (TABLE-3).

**15.13.11.**
- Coherent with D. Read under V0CTL.

**15.15's closing line.**
- Accurate.

### 2.3 Findings, LABELS

| # | class | finding | needs a ruling |
|---|---|---|---|
| LABELS-1 | GAP | K1's adopted start set ("the top-level clause that is or holds the boundary, plus every later top-level clause") is not in draft 3. Without it, (b)'s "no clause from the boundary on" still has the textual reading under which PX-6's claim is unlicensed (R2-P1). So PREFIX-4 is answered by the adopted definition but not by the draft's text. | no (adopted text; state it) |
| LABELS-2 | QUESTION | 5c's "bullet 1" is unidentified (SN-1). Whether it is packet B's (a) or R6's first bullet, "exempt = licensed" is equivalent to (a)+(b) only while 15.1.3's open places hold: ports before the tick block, and the tick block last. The draft tags the identity as 5c's definition, but it is a conclusion. | no; state the dependence |
| LABELS-3 | DRAFTING | The legend's `[ruled: F24]` does not name the labels ruling's adoption of D, on which 15.13.11 rests (AR's D_r for 15.13.11). | no |
| LABELS-4 | DRAFTING | B1 is adopted with two definitions of the boundary. The label ("The first port declaration of either kind, else the tick block") makes it a declaration; the proposed wording and 15.0 make it the top-level clause that is or holds one. K1's "the top-level clause that is or holds the boundary" follows the label. They differ only for a nested port declaration, which 15.1.3 (open) refuses. | no |
| LABELS-5 | DRAFTING | "A default that adds nothing ... does not establish either" is a gloss under a ruled tag, not his words. It is faithful in substance. | no |
| LABELS-6 | DRAFTING | Conclusions carry ruled tags. In 15.12.2 the new sentence is tagged [ruled: F24]. In 15.1.6, "which claims are later is the PREFIX licence's" is tagged [ruled: R6; PREFIX] and is imprecise: R6 also strips claims after an earlier boundary that come before the world-property port, and those are not "later" than it. This runs against the legend's own rule that conclusions are not ruled. | no |

---

## 3. Ruling 2: the closure's rule table

### 3.1 Faithfulness ("[ruled: PREFIX, 2026-10-27]")

The table's rows match the table as put to him, in the wording of his clarification ("add no further reachable body under this rule"):
- a claim: the claim itself;
- If, Unless, Otherwise: every arm, the Otherwise included (also K1's wording);
- For, While: the body;
- the tick block: its body;
- Perform: the procedure's body, transitively;
- To, Define, Decimals: no further reachable body;
- Let, Set, Increase, Decrease, Say, Append, Remove, Must, a port declaration: no further reachable body;
- any other kind: no claim of the law is licensed.

The text around the table:
- "The closure follows the source alone, with values ignored." Faithful to condition 1 ("Structural closure only ... ignoring runtime values").
- "This does not exempt their surrounding clauses from the boundary or licensing test." His condition 2, verbatim.
- "An unperformed `To` adds no procedure body because the closure is source-structural—not because a particular execution skipped it." His condition 4, verbatim.
- "The table establishes no individual claim's licence or standing. Each follows from applying the whole rule to a law's source, then the settlement rules, and the structural oracle tests it on its fixtures."
  - A faithful paraphrase of "it does not establish that any individual claim, including PX-6, is licensed or GROUNDED/HELD. Those outcomes must follow from applying the full rule to the source structure and then the existing settlement rules".
  - "And the structural oracle tests it on its fixtures" comes from the earlier condition 3. That is consistent.
- Condition 3, "Any statement kind without an explicit rule licenses no claim of the law", is stated by the last row.
- His reason (that a port declaration needs a rule, or the licence fails for every law with a port) is not stated. It is a reason, so leaving it out is acceptable.

### 3.2 Coherence (every clause of A_TABLE)

**The table against SPEC §3.**
- Every form of SPEC §3 (relied on from my earlier reading), and both version-1 forms, has a row. That includes Set item and Increase item, the else-if arm, Unless's Otherwise, and the budgeted tick block.
- One exception, "the name alone as a statement" (SPEC §3: "`Perform <name>` or the name alone as a statement | calls the procedure"):
  - The table says only "Perform".
  - If an implementation classifies the bare name as a kind of its own, the last row makes every law that contains one unlicensable (TABLE-1; R2-P2).
  - My reading is that it is the Perform row, since the table was put to him as "proposed from K1 and SPEC §3".

**The last row's trigger.**
- "Any other kind" with "no claim of the law" reads as acting on the whole law, wherever the kind stands. It does not say whether it fires on a kind anywhere in the law, or only on one the closure meets.
- Today the table covers every kind, so the question is moot. It will matter as soon as R2 (open) rules a new form (TABLE-2).

**15.1.1 (late dependency; open R2).**
- Any new form R2 rules is a statement kind that needs a row of the ruled table. Otherwise the last row removes every licence in a law that uses it.
- Its tag does not say this (TABLE-5).

**15.1.3 (open).**
- "If a read is judged by evaluation instead of by its text, it uses the PREFIX licence's closure." The closure's **rules** fit this use; its **start set** does not.
- The licence starts from the boundary on, which includes the tick block. "Outside the tick block" needs the same rules started from the top-level clauses other than the tick block (TABLE-4).

**15.1.6.** See LABELS-6.

**15.3's read-once bullet.**
- The presupposition is now cross-referenced. Its tag is mixed (CHANGED-2).

**15.12.4 and "The licence as ruled".**
- Coherent with the table. PREFIX-3 is answered.
- One caveat: the table makes the licence decidable only together with K1's start set (LABELS-1).

**15.13.6 and 15.13.8 (K̂).**
- With draft 2's altered line removed, K̂'s "may execute" (pinned) is no longer said to use the ruled table.
- The rest-of-block row needs these rules for siblings such as a later tick block (its body) or a To (nothing).
- Either K̂ uses the table's rules, which the integration's I-9 intended, or the pin states its own (TABLE-3).

**15.0 Prefix and Boundary; the legend; 15.15's closing line.**
- Coherent with the table.

### 3.3 Findings, TABLE

| # | class | finding | needs a ruling |
|---|---|---|---|
| TABLE-1 | QUESTION | The table's "Perform" should be read as SPEC §3's row "`Perform <name>` or the name alone as a statement". If the bare name is a kind of its own, the last row makes every law with one unlicensable (R2-P2). | his confirmation of the reading; no new rule |
| TABLE-2 | GAP | The last row's trigger (a kind anywhere in the law, or one the closure meets) is unstated. It is moot while the table is complete, and live once R2 adds a form. | no, not now |
| TABLE-3 | GAP | K̂'s "may execute" (15.13.6, 15.13.8, pinned) is no longer said to use the ruled table. State which reach the pin uses. | no (pinned) |
| TABLE-4 | COHERENCE | 15.1.3's "uses the PREFIX licence's closure" fits the rules but not the start set: judging "outside the tick block" needs a start set without the tick block. | no (open clause) |
| TABLE-5 | DRAFTING | Tag audit: 15.1.1 (open R2) now depends on the table, because a new form needs a row. Its tag does not say so. | no |

---

## 4. Ruling 3: R6's row and control on the configured witness, a measured version-0 control apart

### 4.1 Faithfulness ("[ruled: F24, R6's control, 2026-10-27]", 15.12.6)

- "The row and its paired control share the configured witness: 'the only intended difference is R6.'" His bullet, verbatim in the quoted part. Faithful.
- "A separate version-0 control 'may use the arbiter's own measured witness, clearly labelled as a distinct measurement—not as the paired R6 control.'" Verbatim. Faithful.
- **Omitted:** his decision line, "keep the configured witness for the R6 row and its control; add the measured version-0 control as a separate row". The draft gives only that the separate control "may use" the measured witness. His "add" reads as a directive that the separate row exists. The draft leaves open whether it is required (V0CTL-1).
- His interpretation, "configured agreement is not measured agreement, and neither establishes the reference's version-1 arithmetic independently", is in 15.13.11, verbatim. Faithful.

### 4.2 Coherence (every clause of A_V0CTL)

**The legend, `[ruled: F24]`.** Names the control ruling. Coherent.

**15.12.5.**
- Tags are now split: "[ruled: R6]" on his sentence, and "[ruled: F24, for the real reading and the 1a row]" on the rest. F24-4 is answered.
- "In a real court reading the claim is held only once court R1 is met, which before 1b it is not". F24-3 is answered.

**15.12.6.**
- Coherent for the PREFIX-wrapped control, which stays a version-1 law and differs from the row only in being licensed.
- The control "without an active log declaration" is a version-0 law. Beside R6 it necessarily changes:
  - the header (`orlog-law 0`);
  - the receipt frame (`orlog-receipt 0`);
  - the trace's domain string;
  - the claim's clause id, when the port lines are removed;
  - the court's HELD rule (version 0's, against version 1's E2 meet);
  - D10's scope.
- "The only intended difference is R6" says "intended", which allows these. But at a refusal the two HELD rules can differ, so the comparison is clean only for runs where they agree, such as COMPLETED. The row design should state which differences it expects (V0CTL-2; R2-P7).

**15.13.11.**
- "R6's rows, the PREFIX row and each row's control run in 1a's reference with the witness configured as agreed". This could be read to include the separate version-0 control, which 15.12.6 lets use a measured witness. A cross-reference would close that (V0CTL-3).

**15.14.**
- Names the label of a configured result. It does not name the separately ruled label of the measured control, "clearly labelled as a distinct measurement" (V0CTL-4).

### 4.3 Findings, V0CTL

| # | class | finding | needs a ruling |
|---|---|---|---|
| V0CTL-1 | DRAFTING | His decision line ("... add the measured version-0 control as a separate row") is omitted. "May use" leaves open whether the separate row is required. | no (quote his decision line); yes only if "add" was not meant as a requirement |
| V0CTL-2 | QUESTION | The paired control "without an active log declaration" differs from the row in law version, receipt frame, trace domain, clause ids and HELD rule, not only in R6. "Only intended difference" holds strictly for the PREFIX-wrapped control. | no, unless he wants the paired control limited to the PREFIX-wrapped variant |
| V0CTL-3 | DRAFTING | 15.13.11's "each row's control" should exclude the separate measured version-0 control explicitly. | no |
| V0CTL-4 | DRAFTING | 15.14 omits the ruled label of the separate measured control. | no |

---

## 5. The late dependencies, once for each ruling that named them

| # | clause, ruling | reading | class | needs a ruling |
|---|---|---|---|---|
| LATE-1 | 15.1.1, PREFIX | As TABLE-5: a form R2 adds needs a table row. | DRAFTING | no |
| LATE-2 | 15.13.6, F24 and PREFIX | Under F24 it is coherent. CUT-0 "holds" a claim is not HELD, and 15.13.4 now says HELD needs R8, CUT-0 and court R1. Under PREFIX, its K̂ reach is no longer tied to the table (TABLE-3). | GAP (via TABLE-3) | no |
| LATE-3 | 15.13.12, F24 | 15.13.11 now prints "each claim's evaluation ... beside it, in 12's order". But 12 orders only claims with **no completed** evaluation (R8, then UNREACHED). Claims with completed evaluations ("true in k of k", refuted) have no stated order. | DRAFTING | no |

15.13.10 under F24 is coherent. His scope sentence is now in 15.13.11 and agrees with it. No finding.

---

## 6. Every clause draft 3 changed, and the first re-read's findings it says it answers

| first re-read finding | answered by draft 3? |
|---|---|
| F24-1 (overclaim) | **Yes.** "Only 1b's agreement can show that" is removed, and his interpretation is quoted. |
| F24-2 (E2 and R1) | **Yes.** 15.13.1 has the adopted sentence; 15.13.4 and 15.12.2 are tagged F24. |
| F24-3, F24-4 (15.12.5) | **Yes.** |
| F24-5 (REFERENCE-ONLY's place) | **Partly.** It is answered by a [v0] claim, that it is the integrity column as built, which I cannot verify here (SN-2). The evaluation "in 12's order" covers only claims with no completed evaluation (LATE-3). |
| F24-6 | **By ruling.** Stated, but with his decision line omitted (V0CTL-1). |
| F24-8, F24-10, F24-12 | **Yes.** |
| F24-11 | **Yes.** It is left to open 15.14, which still lacks the measured control's label (V0CTL-4). |
| PREFIX-1 | **Yes**, by his words: "The tick block must have its own closure rule that follows its body." |
| PREFIX-2 | **Yes.** The altered line is removed, which leaves TABLE-3. |
| PREFIX-3 | **Yes**, by the ruled table. |
| PREFIX-4 | **Not in the draft's text.** Only with K1's start set, which is adopted but unstated (LABELS-1). |
| PREFIX-5 | **Yes**, as an open proposal. |
| PREFIX-6 | **Yes.** 15.15 now records that finding 6 is constrained not to bind before the boundary. |
| PREFIX-7, -8, -9, -11, -12, -14 | **Yes.** Caveats: PREFIX-11 under LABELS-2; PREFIX-12 under LABELS-6 and CHANGED-2. |
| PREFIX-10 | **Tagged [v0].** Whether version 0 requires "a ratified seal" is still unverifiable here. |
| T10.5-1 to -3 | **Yes** (Section 8). |

Not claimed as answered, and still as I left them: F24-7 ("may run" against "run"), PREFIX-15 (the vacuous "holds"), PREFIX-16 (a pre-boundary refusal withholding a licensed claim) (SN-3).

**Other changed clauses:**

| # | class | finding | needs a ruling |
|---|---|---|---|
| CHANGED-1 | DRAFTING | The title still reads "(2026-10-26; ...)". DRAFT-3-CHANGES dates draft 3 to 2026-10-27. | no |
| CHANGED-2 | DRAFTING | 15.3's read-once bullet tags the presupposition "PREFIX" inside an [open] tag, while 15.12.4 tags the same presupposition "[open: finding 6]". A reader may take it as ruled. | no |
| CHANGED-3 | DRAFTING | 15.13.4's "Court R1 remains a condition of HELD beside them" paraphrases his "alongside E2" (beside R8 and CUT-0 rather than E2). It is consistent, but not his words. | no |
| CHANGED-4 | QUESTION | 15.13.11's "REFERENCE-ONLY is the integrity column, as the court as built prints it [v0]" rests on the built court, which is outside this set (SN-2). SPEC §12's "the court reads every claim's integrity INCOMPLETE" supports an integrity column existing in version 0. | no |

---

## 7. Probes (all UNEXECUTED; every outcome is my own worked consequence)

The grounding probes assume the claim's default `computation` channel can ground and its seal is ratified. "Real" means the reading with the arbiter's witness; "1a" means the row's reading with the configured witness.

**R2-P1 (PX-6: an unperformed To after the boundary).**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Perform check.`
  - `3. Let g be given as an integer.`
  - `4. To later, do the following.`
  - `4.1. Perform check.`
  - `5. Each tick, do the following.`
  - `5.1. Say g.`
- With K1's start set (top-level clauses from clause `3.` on):
  - port declaration: adds nothing;
  - To: adds nothing;
  - tick block: its body, `Say` adds nothing.
  - The claim is not reached, (a) holds, so it is **licensed**.
- With the draft's text read literally, clause `4.1.` is "a clause from the boundary on" that performs `check`, so it is **not licensed**.
- So the draft alone does not decide it (LABELS-1).
- If licensed: 1a is held at COMPLETED and GROUNDED (configured). Real reading: REFERENCE-ONLY.

**R2-P2 (bare-name call).**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 2 plus 2 equals 4.`
  - `2. Check.`
  - `3. Let g be given as an integer.`
  - `4. Each tick, do the following.`
  - `4.1. Say g.`
- If `Check.` is the Perform kind: **licensed**.
- If it is a kind of its own: the last row applies and **no claim of the law** is licensed (TABLE-1).

**R2-P3 (tick-only law).**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Each tick, do the following.`
  - `2.1. Say 1.`
- The tick-block row follows the body, which reaches no claim, so the claim is **licensed**.
- 1a at COMPLETED: held (K̂ empty), GROUNDED (configured).
- Real: REFERENCE-ONLY in the integrity column, "true in 1 of 1" beside it (15.13.11).

**R2-P4 (procedure performed from the tick block).**
- Law: R2-P3 with `1.` a To holding the claim, and `2.1. Perform check.`
- The tick-block row reaches the body, then the Perform row reaches the procedure, then the claim, so it is **not licensed**.

**R2-P5 (Define after the boundary).**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Let g be given as an integer.`
  - `3. Define r as g.`
  - `4. Each tick, do the following.`
  - `4.1. Say r.`
- The Define row adds nothing, so the claim is **licensed**.

**R2-P6 (Decimals before the boundary; re-read 1's PX-7).**
- Law:
  - `1. Decimals are fixed.`
  - `2. We claim that 2 plus 2 equals 4.`
  - `3. Each tick, do the following.`
  - `3.1. Say 1.`
- Decimals has a rule, so the claim is **licensed**. PREFIX-2's divergence no longer arises.

**R2-P7 (R6's row and its controls).**
- The row's law:
  - `1. Let a be given each tick as an integer.`
  - `2. We claim that 2 plus 2 equals 4.`
  - `3. Each tick, do the following.`
  - `3.1. Say a.`
- Log: `t 1 490000000000000003`, `end 1 closed`.
- The row: COMPLETED. The claim is not licensed (boundary at clause `1.`).
  - 1a: held (meet; R1 configured), **not GROUNDED**, the provenance line printed, labelled "configured, not measured".
  - Real: REFERENCE-ONLY.
- Paired control (a), "without an active log declaration": the law `1. We claim that 2 plus 2 equals 4.`
  - A version-0 law under the same configured witness: GROUNDED (configured).
  - It also differs from the row in header, receipt frame, clause id (1 against 2) and HELD rule (V0CTL-2).
- Paired control (b), PREFIX-wrapped: the claim moved above clause `1.`. Still version 1.
  - It is licensed, so GROUNDED (configured). This is the only variant whose sole difference is R6.
- Separate version-0 control: law (a) with the arbiter's measured witness.
  - GROUNDED (measured), "clearly labelled as a distinct measurement".

**R2-P8 (a licensed claim, then a refusal at a tick).**
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Let a be given each tick as an integer.`
  - `3. Each tick, do the following.`
  - `3.1. Say 10 divided by a.`
- Log: `t 1 490000000000000000`.
- Run: `REFUSED DIVISION-BY-ZERO 4`; ticks 1.
- 1a: R8 holds; CUT-0's K̂ is {clause 4}, so the claim is held and GROUNDED (configured). This is 15.12.5's row.
- Real: not held, because R1 is not met before 1b (15.12.5), and REFERENCE-ONLY.

**R2-P9 (first input in a tick-only law).**
- In R2-P3, the open 15.12.4 sets "first input" to the first `'T'`.
- The claim evaluates before it, so R6's necessary condition holds. This agrees with the licence.

**R2-P10 (first input against the boundary).**
- Law:
  - `1. Let a be given each tick as an integer.`
  - `2. We claim that 1 is positive.`
  - `3. Let g be given as an integer.`
  - `4. Each tick, do the following.`
  - `4.1. Say a plus g.`
- The first port value bound is `g` at clause `3.`, if read-once ports bind where declared (open). The claim precedes it, so R6's first sentence holds.
- But it stands after the first port declaration (`1.`), so it is **not licensed**. That is consistent: the boundary is stricter than the first input.

**R2-P11 (15.1.3 judged by evaluation).**
- Law:
  - `1. Let a be given each tick as an integer.`
  - `2. To show, do the following.`
  - `2.1. Say a.`
  - `3. Perform show.`
  - `4. Each tick, do the following.`
  - `4.1. Perform show.`
- With the licence's start set (clause `1.` on), the closure reaches `show` from `3.` and from the tick block alike. It cannot tell the prefix read at `3.` from the tick read.
- With a start set of the non-tick top-level clauses, `3.` reaches the read outside the tick block, which the open rule would refuse.
- So the start set matters (TABLE-4).

**R2-P12 (K̂ with a later tick block).**
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Perform check.`
  - `3. Say 1 divided by 0.`
  - `4. Each tick, do the following.`
  - `4.1. Perform check.`
- Run: `REFUSED DIVISION-BY-ZERO 4`; ticks 0.
- K̂'s rest-of-block includes the tick block, then its body, then `check`, so the claim is withheld, row "the rest of a block". That is my consequence if K̂ uses the table's rules (TABLE-3).
- The claim is also not licensed (clause `4.1.` performs it), so it is not GROUNDED in either reading.

---

## 8. T10.5, apart

The statement now reads: "each procedure has at most one activation on the stack (its Perform's frame and the frames of its body's statements), so the cut, whose arm selector names an inline arm's own frame, names each call without ambiguity", with the note moved after the statement.

- **T10.5-1 is answered**: "activation".
- **T10.5-2 is answered**: the arm selector is named. This agrees with 15.13.8's "An arm's inline statement is a frame of its own ... named by the If's clause and its arm".
- **T10.5-3 is answered**: the note is placed after.
- The uniqueness argument is valid given SPEC §5's no-recursion rule. Calls follow definition order, so no procedure recurs on one stack. Clause ids are global, so a frame's clause id together with its selector is unique on the stack.

| # | class | finding | needs a ruling |
|---|---|---|---|
| T10.5-4 | DRAFTING | "The frames of its body's statements" should say "including nested statements" (for example, a statement inside an If in the body). Read narrowly, it covers only the body's top-level statements. Minor. | no |

Nothing here is proved.
