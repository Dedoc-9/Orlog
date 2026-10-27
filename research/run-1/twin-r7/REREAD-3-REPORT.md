<!-- R7 re-read 3, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 3: the closure table's Perform row and finding 6, read-once ports (the twin's report)

This is the same reviewer's third re-read under R7, point 4. It is review evidence: not a proof and not a ruling.

- Every probe is worked by hand and is **UNEXECUTED**.
- Every fixture outcome given here is **my own worked consequence**, never the draft's or the owner's.

## Summary

- **Perform row.** Draft 4 states it faithfully: TABLE-1 is answered and the bare-name probe is decided. One tag omission, PERFORM-1.
- **Finding 6.** Draft 5 states RO′-1 to RO′-5 faithfully. Of the four conditions the brief asked me to check:
  - **Condition 1** (whole-log validation stays mandatory) holds. The draft's paraphrase is weaker than his words (F6-6).
  - **Condition 2** (R6's law-fixed claim line) holds by my worked check, probe F6-P8: the read-once stop is never before the boundary.
  - **Conditions 4 and 5** (N2, N3 and the loadable form stay open) hold.
  - **Condition 3** (RO′-6 must state its premises and withholding) is only partly met:
    - **F6-1.** The new row reports its withholdings under the name of another row, "the rest of a block". Condition 3 says not to assume that row covers the stop without checking, and the check for version 1 is DECLARED only.
    - **F6-2.** Two of the row's premises rest on clauses that are still open.
    - **F6-3.** T10 has no obligation for the new row, and T10.7 is not scoped.

**Count:** 22 findings.

| group | findings | needing a ruling or his word |
|---|---|---|
| F6 | 14 | F6-1 and F6-14 |
| PERFORM | 1 | none |
| CHANGED | 2 | none |
| T10.5 | 0 | — |

The SOURCE NEEDED notes in §1 are separate from these 22.

## 1. Provenance

**Files opened**, Read tool unless stated, all in `twin-r7-reread3/`:

1. `REREAD-3-BRIEF.md`, whole.
2. `SPEC-15-DRAFT-5.md`, whole.
3. `DRAFT-5-CHANGES.md`, whole.
4. `DRAFT-4-CHANGES.md`, whole.
5. `RULINGS-AS-RULED.md`: a Grep of its section headings, then lines 329–379 ("The table's Perform row" and "Finding 6: read-once ports").
6. `AR-F6.md`, whole.
7. `AR-REREAD-2.md`: a Grep for its third set, then lines 100–140.
8. `T10-STATEMENTS.md`, whole.

**Not opened:**
- `RULINGS-AS-RULED.md` lines 1–328. The brief says they are as before, and I rely on my earlier reading.
- `SPEC.md` and `RUNTIME-SPEC.md`. I rely on my earlier full reading of the copies in `twin-r7-inputs/`. The brief says the bytes are the same; I did not check the sha256 myself.
- Draft 3. My comparisons with it are from my second re-read, still in context. Draft 3 is not in this folder.

**SOURCE NEEDED** (named, not opened):

| # | source | why |
|---|---|---|
| SN-1 | `packets/F-read-once-adversary.md` §4 | 15.13.8's new row cites it for its version-0 stand-in check, "MEASURED there". I cannot see what was measured. |
| SN-2 | The packets that define N2 and N3 (C, F) | His ruling only names N2 and N3. I cannot check 15.3's wording of them. |
| SN-3 | Packet C §5 and packet F §4–§5 | They are AR-F6's D_r sources. Not needed to judge the clauses. |
| SN-4 | Packet B §3.3 | Needed to confirm that 5c's "bullet 1" is R6's first licence bullet, as draft 4 now says. |
| SN-5 | Finding 8's record | It is to give the loadable form and the LOG-* codes. |

---

## 2. Ruling: the closure table's Perform row (A_PERFORM, 12 clauses)

His answer: "Yes, the bare name is Perform (Recommended)".

### 2.1 Faithfulness

**The table's row** (15.12.4), tagged "[ruled: PREFIX, 2026-10-27]":
- It reads "Perform, written `Perform <name>` or the name alone (SPEC §3) | the procedure's body, transitively".
- This states his answer faithfully, and SPEC §3's row gives both spellings. TABLE-1 is answered.

### 2.2 Coherence (every clause of A_PERFORM)

- **The table's header and its last row:** coherent. The last row no longer catches a bare-name call. Its trigger (my TABLE-2) stays moot while the table covers every kind.
- **The licence as ruled:** coherent.
- **15.9:** "a `Perform` emits no event" covers both spellings. Coherent.
- **15.13.8 and 15.13.9:** their Perform rows ("refused at its own operation", "below the top") apply to a bare-name call alike. Coherent with SPEC §3.
- **Untouched by this ruling:** the legend, 15.0 Boundary, 15.1.6, 15.3's read-once bullet, and 15.15's closing line.

### 2.3 Probe (UNEXECUTED; my worked consequence)

**PERF-P1.** The law:

```
1. To check, do the following.
1.1. We claim that 2 plus 2 equals 4.
2. Check.
3. Let g be given as an integer.
4. Each tick, do the following.
4.1. Say g.
```

- `Check.` is the Perform kind.
- The start set (clause 3 onward) reaches no claim, so the claim is **licensed**.
- This decides my R2-P2.

### 2.4 Findings

| # | class | finding | needs a ruling |
|---|---|---|---|
| PERFORM-1 | DRAFTING | The table's tag and the legend's `[ruled: PREFIX]` do not name the Perform-row answer. Only 15.15's closing line records it ("since draft 3, the table's Perform row"). | no |

---

## 3. Draft 4: the changes, and my second re-read's findings it says it answers

| finding | answered? |
|---|---|
| CHANGED-1 (the title's date) | **Yes.** |
| LABELS-1 (K1's start set) | **Yes.** "Its start set is the top-level clause that is or holds the boundary, plus every later top-level clause". With it, PX-6 / R2-P1 becomes, as my worked consequence, **licensed**: the To after the boundary adds no body. |
| LABELS-2 (5c's "bullet 1") | **Yes, as stated.** "Bullet 1" is named as R6's first licence bullet, tagged [follows], with its dependence on 15.1.3. I cannot verify the naming (SN-4). |
| LABELS-3 (the legend) | **Yes.** |
| LABELS-4 (B1's two wordings) | **Yes**, tagged open: port place. |
| LABELS-5 | **Yes.** It now uses the adopted words, "The existing version-0 default behavior is not enough to establish this". |
| LABELS-6 (conclusions tagged as ruled) | **Yes.** There is now a `[follows]` tag, used on 15.12.2, 15.1.6, the 5c identity and the presupposition. 15.1.6's restatement is narrower than the sentence it explains (CHANGED-1 below). |
| TABLE-1 | **Yes**, by ruling (§2). |
| TABLE-3, LATE-2 | **Yes.** 15.13.8's closing line now says K̂'s reach is CUT-0's own, for the pin, and is "not said to be" the table. A residue remains for the pin (F6-13). |
| TABLE-4 | **Yes.** It is "started from the top-level clauses other than the tick block". |
| TABLE-5, LATE-1 | **Yes** (15.1.1). |
| CHANGED-2 (15.3's presupposition) | **Superseded.** Draft 5 replaced that bullet. |
| CHANGED-3 (15.13.4) | **Yes.** His words: "Court R1 remains a condition of HELD alongside E2". |
| V0CTL-1 | **Yes.** His decision line is quoted. |
| V0CTL-2 | **Yes**, as an open bullet for 1a's specification. |
| V0CTL-3 | **Yes.** |
| V0CTL-4 | **Yes.** |
| LATE-3 | **Yes.** "True in k of k or refuted for a completed evaluation, and in 12's order for a claim with none". |
| T10.5-4 | **Yes** (§5). |

**Findings on draft 4's changed clauses:**

| # | class | finding | needs a ruling |
|---|---|---|---|
| CHANGED-1 | DRAFTING | 15.1.6's [follows] sentence covers only claims that *stand* after the boundary ("every claim at or after the boundary is unlicensed"). R1's "every later claim in the run" also covers a claim that stands earlier but is *evaluated* after the port (a procedure performed later), which is unlicensed by (b). The sentence should cite (a) and (b) both. | no |
| CHANGED-2 | QUESTION | That 5c's "bullet 1" is R6's first licence bullet rests on packet B §3.3 (SN-4). The identity is correctly tagged [follows]. | no |

---

## 4. Ruling: finding 6, read-once ports (A′, RO′-1 to RO′-6, six conditions; A_F6, 104 clauses)

### 4.1 Faithfulness (clauses tagged `[ruled: F6]`)

**The legend.**
- "fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′-6 (2026-10-27)".
- It omits "with six conditions", which his ruling makes part of it ("Conditions of the ruling"). The status paragraph has the conditions (F6-12).

**15.3, "Read-once ports".**
- The first two sentences are RO′-1 and RO′-2, verbatim. Faithful.
- "When the run starts and where it stops is 15.7.1's" is a pointer.
- The sub-bullet states condition 4: "N2 and N3 remain open for the A2 row". I cannot check the draft's descriptions of N2 and N3 (an `end()` before the record closes; when the host runs the statements before the first read-once declaration), because the ruling only names them (SN-2).

**15.5, the new bullet:** "[ruled: F6, condition 5, that the form is owed; open: finding 8, the form]".
- Condition 5 says: "Finding 8 must define a loadable representation for read-once `NOT-RUN` logs. Byte forms remain open."
- The draft also makes a loadable form owed for "an open log of the header alone". That obligation follows from RO′-3 ("provided the log loads", "or LOG-OPEN if the log has no end record") and RO′-5. It does not come from condition 5, so the tag adds to the condition (F6-7).

**15.5, the whole-log bullet** [ruled: F6, condition 1].
- "This stays mandatory, and a well-formed log without the read-once record is a distinct case, never a malformed one" is faithful.
- But the bullet's consequence, "so no tick of a malformed log runs", is weaker than his words, "A malformed log is rejected before any statement executes" (F6-6).

**15.7.1.**
- "A read-once port binds where its declaration stands", tagged "F6, where it binds", is RO′-3's first sentence. Faithful.
- The new bullet is RO′-3's remaining sentences and RO′-4, verbatim, with one insertion: "even when the missing value is a later port's".
- That insertion is entailed by "the run stops before the first read-once declaration", and it agrees with his words, "the run ends `NOT-RUN` there and names the first empty read-once port". It is an addition, but a faithful one.

**15.7.5, the new bullet.** RO′-5, verbatim apart from "That stop" becoming "The stop of 15.7.1". Faithful.

**15.13.8, the old NOT-RUN/LOG-OPEN row.** "This row applies only when the law declares no read-once port or its log holds the read-once record" is RO′-6's last sentence. Faithful.

**15.13.8, the new row** [ruled: F6, RO′-6 and its condition 3; pinned].
- Its core is RO′-6, verbatim: "the cut is the first read-once declaration, a top-level frame not begun; K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored".
- **Added** under the ruled tag:
  - "with no `'R'` event". This follows from RO′-3, since the stop is not a refusal.
  - "a withholding names 'the rest of a block'". RO′-6 does not say this, and condition 3 warns against assuming that row (F6-1).
  - The premises. Condition 3 asks for them, so stating them is right. Two of them rest on open clauses (F6-2).
  - The grading: "checked on version-0 stand-ins only ... for version 1 it is DECLARED". This is honest, and it bears on condition 3 (F6-14).

**The licence's presupposition** [follows: F6; 15.0 Boundary].
- "A read-once value binds where its declaration stands (15.7.1), which is never before the boundary, so the presupposition holds."
- This is correct. The boundary is the first port declaration of either kind, so every read-once declaration stands at or after it. My earlier PREFIX-6 is answered by the ruling.
- The first input's definition moves to "[open: the theorem ledger's T9]". Coherent.

### 4.2 The four checks the brief asks for

**(a) RO′-6's row states its premises and its withholding (condition 3).**
- The premises are stated:
  - binding has no effect beyond binding;
  - read-once ports are declared at the top level;
  - each is evaluated once;
  - values are unknown.
- The withholding is stated as "the rest of a block".
- Two problems remain:
  - **F6-1.** Condition 3 reads: "do not assume the existing 'rest of a block' row covers it without checking". The draft makes a new row but reports its withholdings under the existing row's name, and 15.13.9's list of row names has no name for the new row. The claims ruling requires every withholding to "identify the responsible structural row". Either the stop is its own row, and needs its own name in 15.13.9, or it is the rest-of-block row applied to a frame not begun. In the second case the only check for version 1 is DECLARED (F6-14).
  - **F6-2.** The premise "read-once ports are declared at the top level" is 15.1.3's open place rule, and RO′-6's own ruled text says "a top-level frame". The premise "it counts no operation" is 15.7.1's open counting clause. "Cannot refuse" survives either way, because the prefix has no budget.

**(b) Whole-log validation stays mandatory beside the stop (condition 1).**
- Yes. 15.5 keeps whole-log parsing before any execution, and says a well-formed log without the record is "a distinct case, never a malformed one".
- The two well-formed forms without the record (a header-only open log, and a read-once NOT-RUN log) read as an exhaustive list. If so, every other log that lacks the record is malformed, but the draft does not say so (F6-9).
- Its consequence sentence understates his words (F6-6).

**(c) Nothing weakens R6's law-fixed claim line (condition 2).**
- R6's licence text in 15.12.4 is unchanged.
- My worked check:
  - the stop is "before the first read-once declaration", which is never before the boundary;
  - the clauses before that declaration run "whatever the log holds";
  - RO′-4 makes a refusal there REFUSED regardless of the log.
- So a licensed claim, evaluated only before the boundary, has the same claim line whether the record is present or absent (F6-P8).
- At the stop, the new row's K̂ (the rest of the block from the first read-once declaration) lies wholly at or after the boundary. A licensed claim is therefore never in it, and 15.12.5's "remains historically held" agrees with the meet.
- I found nothing that weakens condition 2.

**(d) N2, N3 and the loadable form stay open (conditions 4 and 5).**
- Yes, in 15.3's sub-bullet and in 15.5's bullet, and both are in 15.15.
- Two related items are not listed: the session events that fill and close the record (F6-5), and the read-once NOT-RUN's t (F6-4).

### 4.3 Coherence (every clause of A_F6)

**Clauses draft 5 changed**

**15.3, read-once ports.**
- RO′-1 is consistent with "A door refusal or a refused move does not end the session".
- **Gap.** RO′-2's "filled by assigning accepted arrivals ... closed once before any tick record" has no event form in the table:
  - `assign(arrival, tick)` requires "the tick is the open one";
  - `close()` speaks only of each-tick ports.
- Also unstated:
  - which event closes the record;
  - whether `close()` of tick 1 is legal before the record closes;
  - what happens to the session when the record closes with a slot empty. RO′-3 implies NOT-RUN and the session's end.
- His ruling leaves "session-event semantics" open, but the draft lists only N2 and N3 as open (F6-5).

**15.5, the record line.**
- "when the law declares a read-once port and the record closed": under RO′-2 the record "is written whole or not at all", so a close with a slot empty writes nothing. "Closed" should read "written" (closed with every read-once port filled).
- The line carries no F6 tag, though it now follows from RO′-2 (F6-8).

**15.5, the new bullet.** See 4.1 and F6-7. The other cases that lack the record are F6-9.

**15.5, the whole-log bullet.** See 4.2(b) and F6-6.

**15.7.1.** Coherent with 15.7.4, 15.7.5 and RO′-4, with three points:
- **"Checked against the history" (F6-10).** This sits in the execution's clause, but an execution over a log has no history. The check is the verifier's (15.4, HISTORY-MISMATCH). Over a hand-made log, whether the loader checks that the named port is a read-once port is finding 8's.
- **Event order.** At the stop, the trace holds the prefix's events up to the declaration, with no `'N'` and no `'R'`. out_0 hashes everything said; there are no tick lines; `ticks` is 0.
- **`tick-ops`** is undefined when no tick began. That is the old finding 31, still open.

**15.7.5.**
- **Gap (F6-4).** NOT-RUN's definition ("every record before t ran, and the end record names tick t as not run") does not fit a stop in the prefix. Neither the status line (`NOT-RUN <t> INPUT-MISSING <port>`) nor the end record gives t for the read-once stop: is it 0, or 1?
- RO′-5's "COMPLETED never stands for a law with a read-once port whose log lacks the record" agrees with F6-9 only if such a log (for example `end 0 closed` with no record) is malformed.

**15.13.8, the scoped old row.** Coherent.

**15.13.8, the new row.** See 4.2(a).
- **T10 (F6-3).** No T10 obligation covers this row. T10.7's statement still says "At NOT-RUN t or LOG-OPEN, the cut is the tick block's head before tick t", unscoped, which now contradicts 15.13.8's scoped row. T10.0's "the rows cover every statement kind" also needs the stop.

**The licence's presupposition.** Coherent (4.1).

**15.15.**
- The new rows for N2/N3 and finding 8's form are coherent.
- The row "15.3 and 15.4: the session, read-once ports, its record, the binding; ... (findings 6, ...)" still lists finding 6 and the binding as open under A2, though finding 6 is now ruled apart from N2 and N3 (F6-11).
- Missing from the table: F6-2's dependence, F6-4's t, and F6-5's events.

**Status, title.** Accurate.

**Clauses draft 4 changed that are also in A_F6**
- **15.1.3:** see F6-2 (RO′-6 presupposes its open top-level rule).
- **15.1.6:** a missing world property now stops the run before its declaration. The cost sentence and its [follows] are unaffected (CHANGED-1 aside).
- **The licence as ruled:** above.
- **15.13.8's closing line:** CUT-0's own reach must, for the ordinary rest-of-block row, follow a later tick-block sibling's body and treat port declarations as adding nothing. The new row says this for the stop only; the pin should say it in general (F6-13).
- **15.14 and 15.15's closing line:** coherent.

**Clauses of A_F6 untouched by the ruling.** One line each; nothing changes.
- **15.0:** Port; Arrival; Input log; Execution.
- **15.3:**
  - the A2 paragraph;
  - the table's rows, apart from F6-5's gap;
  - "Any other move", where a second assignment to a filled read-once slot would be SLOT-FILLED by analogy;
  - dispositions;
  - "No value is invented ...", consistent with RO′-3;
  - retry;
  - "A door refusal ... does not end the session";
  - "Until SNAP-1".
- **15.4**, all four bullets. HISTORY-MISMATCH now carries RO′-3's history check (F6-10).
- **15.5:**
  - the header;
  - the end record (the read-once form's bytes are open);
  - "a log with no end record is open";
  - load refusals (open);
  - the chain, where in_0 without a record hashes the header alone, implied;
  - `input-log-sha256`.
- **15.6.**
- **15.7.2–15.7.4 and 15.7.6.** At the stop there is no `'T'`, the prefix has no budget, and out_0 covers everything said.
- **15.8**, every line:
  - the status is NOT-RUN or LOG-OPEN, with t open (F6-4);
  - `ticks` is 0;
  - `tick-ops` is open;
  - the unread count is 0, since the well-formed forms without the record have no tick records;
  - the core, the frame check and "no validity line" are unchanged.
- **15.9:**
  - the head;
  - `'N'`;
  - `'R'`: at the stop there is no `'R'`, so the cut is read from the status, as for NOT-RUN generally.
- **15.10**, every line: at the stop there are no tick lines, and "T(1).c" is vacuous.
- **15.11**, both bullets: the stop is determined by the log.
- **15.12.3:** the provenance line names the log as read.
- **15.13.1, 15.13.6, 15.13.7, 15.13.12:** unaffected. 15.13.7's continuation "relative to the law" agrees with K̂'s including the tick block.
- **15.13.9:** see F6-1, the missing row name.
- **15.15's other rows:** unchanged.

### 4.4 Probes (all UNEXECUTED; every outcome is my own worked consequence)

The counts assume the open "counting" reading (binding counts 0). "Real" means the court's real reading, REFERENCE-ONLY before 1b. "1a" means the row's reading with the configured witness.

**F6-P1. Record present, COMPLETED.**

```
1. Say 1.
2. Let g be given as an integer.
3. Say g.
4. Each tick, do the following.
4.1. Say 2.
```

- Log: the header, the record with g = 7 (bytes open), `t 1`, `end 1 closed`.
- Result: COMPLETED; ticks 1; ops 3; output "1\n7\n2\n".
- Events: S, N, S, T, S.

**F6-P2. Record absent, NOT-RUN.**
- The same law. The log ends in a read-once not-run naming g (bytes open).
- Run: `Say 1` runs (ops 1, "1\n"), then the stop before clause 2.
- Status: `NOT-RUN <t> INPUT-MISSING g`, with t **not determined by §15** (F6-4).
- ticks 0; events: S only; no `'N'`, no `'R'`; out_0 over "1\n".

**F6-P3. Record absent, open log.**
- The same law, with a header-only open log.
- Run: the same as F6-P2 up to the stop. Status LOG-OPEN; ticks 0.

**F6-P4. A refusal before the declaration (RO′-4).**
- `1. Say 1 divided by 0.` then `2. Let g be given as an integer.` and so on.
- Result: REFUSED DIVISION-BY-ZERO 1, whatever the log holds; ticks 0.

**F6-P5. Two read-once ports, the second missing.**

```
1. Let g be given as an integer.
2. Say 5.
3. Let h be given as an integer.
4. Each tick, do the following.
4.1. Say g plus h.
```

- Session: g's arrival is assigned and h's slot is empty. The record is not written, being "whole or not at all".
- Run: the stop is before clause 1, so `Say 5` does **not** run, even though g's value was sent. Status NOT-RUN naming h.
- g's arrival is disposed "assigned" but appears in no record. That is the old finding 54's case.

**F6-P6. Each-tick port first, then the read-once port; record absent.**

```
1. Let a be given each tick as an integer.
2. We claim that 1 is positive.
3. Let g be given as an integer.
4. Each tick, do the following.
4.1. Say a plus g.
```

- Run: clauses 1–2 run, the claim is true, then the stop before clause 3.
- The claim is **not licensed** (the boundary is clause 1).
- 1a: the new row's K̂ is clause 3 onward plus the tick body (`Say`), which holds no claim. R8 holds, so the claim is held (configured), but not GROUNDED.
- Real: REFERENCE-ONLY.

**F6-P7. A claim in a procedure performed from the tick block; record absent.**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Perform check.
3. Let g be given as an integer.
4. Each tick, do the following.
4.1. Perform check.
```

- Run: clauses up to `2.` run and the claim is true once; then the stop before `3.`.
- Not licensed: clause 4.1 performs `check`.
- 1a: K̂ reaches the tick body, then `Perform check`, then the claim, so it is **withheld**. Per the draft, the withholding names "the rest of a block" (F6-1).

**F6-P8. Condition 2: a licensed claim with the record absent and present.**

```
1. We claim that 2 plus 2 equals 4.
2. Let g be given as an integer.
3. Each tick, do the following.
3.1. Say g.
```

- Record absent: the claim evaluates, the run stops before clause 2, NOT-RUN. The claim line is `claim 0 1 1 1 2 0 0`.
- Record present (`t 1`, closed): COMPLETED. The claim line is the same, `claim 0 1 1 1 2 0 0`, so it is law-fixed.
- The claim is licensed in both runs. 1a: held in both (K̂ at the stop is clause 2 onward), so GROUNDED (configured). Real: REFERENCE-ONLY.

**F6-P9. Condition 1: malformed against well-formed-without-the-record.**
- F6-P1's law with a log holding `t 1` but no read-once record. That is not one of the two well-formed forms, so I read it as malformed:
  - refused at load;
  - **no statement runs**, `Say 1` included;
  - no receipt under the proposal.
- The load code is **not determined by §15** (finding 8).
- Contrast F6-P2, where `Say 1` runs.

**F6-P10. RO′-5.**
- F6-P1's law with `end 0 closed` and no record. This is never COMPLETED (RO′-5).
- I read it as malformed. §15 does not say so, and the code is open (F6-9).

**F6-P11. A law with no read-once port.**
- `1. Let a be given each tick as an integer.` with a tick block, and a header-only open log.
- No read-once record is expected. Result: LOG-OPEN, and the old row applies (the tick block's head before tick 1).

### 4.5 Findings, F6

| # | class | finding | needs a ruling |
|---|---|---|---|
| F6-1 | COHERENCE | RO′-6's row reports its withholdings as "the rest of a block", another row's name, and 15.13.9 has no name for the new row. The claims ruling requires the responsible structural row, and condition 3 says not to assume the existing row covers the stop. Decide whether the stop is its own row (named in 15.13.9) or the rest-of-block row applied to a frame not begun. | yes (or the pin's explicit choice, recorded) |
| F6-2 | GAP | RO′-6's premises, and its ruled words "a top-level frame", rest on 15.1.3's open place rule (ports at top level). The premise "counts no operation" rests on 15.7.1's open counting clause. The tags and 15.15 do not record this. | no now; yes if port place is ever ruled otherwise |
| F6-3 | GAP | T10 has no obligation for RO′-6's row, and T10.7's statement is unscoped ("At NOT-RUN t or LOG-OPEN, the cut is the tick block's head"), against 15.13.8. | no (a ledger row; scope T10.7) |
| F6-4 | GAP | The read-once NOT-RUN's t, in the status line and the end record, is undefined. 15.7.5's NOT-RUN definition does not fit a stop in the prefix. 15.15 lists only the log's loadable form. | no now (finding 8 / identity and bytes); list it |
| F6-5 | GAP | No session events fill or close the read-once record: `assign` needs "the tick is the open one", and `close()` covers each-tick ports only. Nor is it said whether tick 1 can close first, or what a close with an empty slot does. 15.3 lists only N2 and N3 as open. | no now (A2); list it |
| F6-6 | DRAFTING | 15.5's "so no tick of a malformed log runs" understates his condition 1, "A malformed log is rejected before any statement executes". | no |
| F6-7 | DRAFTING | 15.5's new bullet attributes the header-only open log's owed form to condition 5. That condition names only "read-once `NOT-RUN` logs"; the open log's form follows from RO′-3 and RO′-5. Retag it [follows]. | no |
| F6-8 | DRAFTING | 15.5's record line says "the record closed" where RO′-2 means written whole ("written whole or not at all"). It also carries no F6 tag. | no |
| F6-9 | GAP | Which logs that lack the record are malformed is implied but not stated: a log with tick records but no read-once record; `end n closed` without the record. Say that the two well-formed forms are exhaustive, and leave the codes to finding 8. | no now |
| F6-10 | QUESTION | "Checked against the history" sits in the execution's clause (15.7.1), but an execution has no history. The check is the verifier's (15.4). Whether the loader checks that the named port is a read-once port is finding 8's. | no |
| F6-11 | DRAFTING | 15.15's A2 row still lists finding 6 and "the binding" as open. | no |
| F6-12 | DRAFTING | The legend's `[ruled: F6]` omits "with six conditions". | no |
| F6-13 | GAP | CUT-0's own reach (15.13.8's closing line, pinned) must follow a later tick-block sibling's body and treat port declarations as adding nothing, in the ordinary rest-of-block row. The new row says this for the stop only. | no (pin) |
| F6-14 | QUESTION | Condition 3's "without checking" is met for version 1 only by DECLARED: the K̂ equality was "checked on version-0 stand-ins only" (SN-1). Whether that suffices before the pin is his to say. | his confirmation |

---

## 5. T10.5

The statement now includes "nested ones included". **T10.5-4 is answered.**

The statement is coherent with 15.13.8: an inline arm is its own frame, and Perform covers the bare name, by the ruling. No new finding. Nothing here is proved.

T10.7, in the same file, is out of step with draft 5. That is F6-3, not a T10.5 finding.
