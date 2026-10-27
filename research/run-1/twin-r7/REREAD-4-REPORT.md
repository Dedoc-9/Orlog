<!-- R7 re-read 4, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 4: the read-once stop's row and its version-1 check (the twin's report)

This is the same reviewer's fourth re-read under R7. By his third answer it is the one re-read before the gate. It is review evidence: not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture outcome is **my own worked consequence**.

## Summary

Draft 6 states both answers faithfully, apart from small omissions. It also answers every third re-read finding it claims, except F6-3, which T10.0 leaves half done.

There are 10 findings. Three need his decision, as his third answer requires ("Any issue needing your decision comes back to you"):

- **STOPROW-1.** The court cannot choose between the read-once stop's row and the old LOG-OPEN row from the receipt alone. Probe S-P2 gives two runs with the same status line, `LOG-OPEN`, and different K̂. Something has to carry "record absent": a receipt or status form (finding 8), or the court reading the log.
- **V1CHECK-3.** 1a's rows read HELD through a meet that "names the exact digest", but the digest cannot be pinned before the owed version-1 check. Unless rows may run against an unpinned CUT-0, that check sits on the build's path despite "Enough now".
- **V1CHECK-2 (conditional).** The owed check is not defined: "K̂ equals the rest of the block" is true by RO′-6's own definition. His decision is needed only if he meant equality with the true continuation rather than containment.

## 1. Provenance

**Opened**, all in `twin-r7-reread4/`:
- `REREAD-4-BRIEF.md`, whole.
- `DRAFT-6-CHANGES.md`, whole.
- `AR-REREAD-4.md`, whole.
- `RULINGS-AS-RULED.md`: a Grep of its section headings, then lines 378–411.
- `T10-STATEMENTS.md`, whole.
- `SPEC-15-DRAFT-6.md`, whole.

**Not opened:**
- `SPEC.md` and `RUNTIME-SPEC.md`. I rely on my earlier full reading of the copies in `twin-r7-inputs/`. The brief says the bytes are the same; I did not check this myself.
- `RULINGS-AS-RULED.md` lines 1–377, as read before.
- Draft 5. My comparisons with it are from re-read 3, still in context.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** `packets/F-read-once-adversary.md` §4: what was MEASURED on the version-0 stand-ins, and therefore what the version-1 check must check (V1CHECK-2).
- **SN-2.** The court as built: how it would choose a CUT-0 row for a LOG-OPEN or NOT-RUN receipt (STOPROW-1).
- **SN-3.** `REREAD-3-DISPOSITION.md`: the disposition of my third re-read's findings that draft 6 does not mention, such as re-read 3's CHANGED-2.

---

## 2. Answer 1: the stop's own row (F6-1) — A_STOPROW, 11 clauses

### 2.1 Faithfulness

His words: "Adopt 'Its own row.' Name it 'the read-once stop' in §15.13.9's row list. Compute its K̂ as RO′-6 specifies ... Do not attribute this withholding to the existing 'rest of a block' row or imply that row covers a frame that never began."

- **15.13.8, the new row.** "A withholding names this row, 'the read-once stop', never 'the rest of a block'. [ruled: F6, RO′-6; his answer on F6-1; pinned]". **Faithful.**
  - K̂ is still described as "the rest of the block from it". Those are RO′-6's words and his own ("Compute its K̂ as RO′-6 specifies: the rest of the block from the first read-once declaration"), not the row's name. So the draft does not imply that the existing row covers a frame not begun.
- **15.13.9.** "... the tick block's next tick, or the read-once stop. [... F6, the read-once stop's name]". **Faithful.**
- **The legend's `[ruled: F6]`.** It now adds "and by his answers on the read-once stop's row and its version-1 check". **Faithful.**

### 2.2 Coherence (every clause of A_STOPROW)

**15.13.8, the new row.**
- It is interpretable and has one row name.
- The general rows are defined for "the cut ... at the refusal". The stop has no refusal, so they do not apply to it, and the stop's K̂ is this row's alone. That is consistent with "never 'the rest of a block'".
- **Missing:**
  - **STOPROW-1 (needs his decision).** The row is selected by "the read-once record absent", and nothing says what the court reads to know that.
    - For LOG-OPEN, a log with the record and no ticks gives the same status line as a header-only log, `LOG-OPEN` with `ticks 0`, but a different row and a different K̂ (probe S-P2).
    - For NOT-RUN, the status names a port, and its kind could tell the two apart, but t is open (F6-4).
  - **STOPROW-2.** The row cites no T10 obligation, while every other row cites its own; it should cite T10.8.

**15.13.9.** Coherent.

**15.9 ('R').**
- At the stop there is no `'R'` event. Withholding can still name its row only if the court can recognise the stop (STOPROW-1).
- Otherwise untouched.

**15.13.2.** Untouched. It is consistent: the stop's K̂ withholds only claims it can reach.

**The 15.15 row on 15.13.9 (two rows withholding one claim).**
- At the stop only one row applies, so the question does not arise there.

**The legend; 15.3; the two 15.5 bullets; 15.7.1; 15.7.5.**
- Tagged F6 and changed for other reasons; read in §4. The row name touches none of them.

### 2.3 Probes (UNEXECUTED; my worked consequences)

**S-P1. The stop withholds a claim.**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Perform check.
3. Let g be given as an integer.
4. Each tick, do the following.
4.1. Perform check.
```

- Record absent, so NOT-RUN naming g.
- K̂ runs from clause `3.` through the tick body and `Perform check` to the claim, so the claim is **withheld**, named "the read-once stop".
- Real reading: REFERENCE-ONLY.

**S-P2. The same status line, two rows.**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Perform check.
3. Let g be given as an integer.
4. Perform check.
5. Each tick, do the following.
5.1. Say g.
```

- **Log A** (header and the record g = 7, open, no tick records):
  - the run binds g, the claim is true twice, the status is `LOG-OPEN`;
  - the old row applies, and K̂ = the tick block, whose `Say` adds nothing;
  - so the claim is **held** in a 1a reading.
- **Log B** (header only):
  - the claim is true once, then the run stops before `3.`; the status is `LOG-OPEN`;
  - the stop row applies, and K̂ includes `4. Perform check`;
  - so the claim is **withheld** ("the read-once stop").
- Both receipts read `status LOG-OPEN` and `ticks 0`. They differ only in `input-log-sha256`, events (`'N'`), ops and output.

---

## 3. Answer 2: the version-1 check (F6-14) — A_V1CHECK, 33 clauses

### 3.1 Faithfulness

His words: "Keep the evidence grades explicit: MEASURED on version-0 stand-ins; DECLARED for version 1. Record a version-1 check of RO′-6 as owed before CUT-0's digest is pinned. This is a deferral, not evidence that version 1 satisfies the equality. It does not close the format-freeze question or authorize pinning before the check."

**15.13.8.** "MEASURED on version-0 stand-ins only ...; for version 1 it is DECLARED, and a version-1 check is owed before CUT-0's digest is pinned: a deferral, not evidence."
- The grades and the deferral are **faithful**.
- **Omitted:** "It does not close the format-freeze question" (V1CHECK-1). "Or authorize pinning before the check" is implied by "owed before ... pinned".
- The tag reads "[ruled: his answer on F6-14]". It drops "F6", which the legend now covers.

**15.15's new row.** It lists "the read-once stop's version-1 check, owed before the pin". **Faithful.**

### 3.2 Coherence (every clause of A_V1CHECK)

**15.13.8, the grades.**
- **V1CHECK-2.** RO′-6 defines K̂ as "the rest of the block from" the declaration, so "K̂ equals the rest of the block from the declaration" is true by definition. The equality that was MEASURED, and that the owed check must check, is something else (SN-1). It could be either:
  - that every claim a continuation from the stop could evaluate lies in K̂ (soundness, containment); or
  - that this set equals K̂ (precision).
- The draft should state which, with the check's fixtures and pass condition.

**The legend's `[pinned]`.**
- "No digest is pinned yet ... it can change until the pin" is coherent with the deferral.
- **V1CHECK-3 (needs his decision).** 15.13.4 says the meet "names the exact digest of the CUT-0 it uses". 1a's rows (15.12.5, 15.12.6, 15.13.11) read HELD through that meet. If a row must name a pinned digest, the version-1 check is on the build's path, despite "Enough now". If rows may run against the proposed, unpinned CUT-0, that should be said.

**15.13.7 (continuation, pinned).**
- **V1CHECK-4.** "Everything the run could still have executed had the refusing operation returned" defines the continuation only at a refusal. At the read-once stop, NOT-RUN and LOG-OPEN there is no refusing operation.
- The version-1 check, T10.7 and T10.8 all need the continuation as "had the missing input arrived, with any value".
- This is the pin's wording.

**15.13.5, 15.13.6.** Untouched.

**15.13.8's closing line.** "Its rules for the version-1 kinds in the other rows ... are the pin's to state. [open: the pin]". This answers F6-13.

**15.13.9.** Coherent.

**15.15:**
- **Changed rows:** coherent.
  - The 15.3/15.4 row now reads "Finding 6 is ruled, its open parts in the next row", and "binding" now means the binding of the three records, not a port's binding.
  - The 15.3/15.7.1 row lists the record's events, N2 and N3.
  - The 15.5/15.7.5 row lists the forms, which logs are malformed, and t.
  - The 15.13.8 row is added.
  - The closing line names the answers.
- **CHANGED-1.** The "15.5 and 15.6" row still cites finding 6 among its findings.
- **Untouched rows:**
  - 15.0/15.1;
  - 15.1.3;
  - 15.1.5;
  - 15.1.6;
  - 15.2;
  - 15.7.1–3;
  - 15.7.5/15.8;
  - 15.7.6;
  - 15.9 (the open format freeze; consistent with "does not close the format-freeze question");
  - 15.10;
  - 15.11/15.8;
  - 15.13.9;
  - 15.13.11;
  - 15.14.

**The legend's F6 entry; 15.3; 15.5; 15.7.1; 15.7.5.**
- Tagged F6. The version-1 check touches none of them (see §4).

---

## 4. Draft 6's changed clauses, and the third re-read's findings it answers

| finding | answered? |
|---|---|
| PERFORM-1 | **Yes.** The legend's PREFIX entry and the table's tag now name the Perform row. |
| F6-12 | **Yes.** "With six conditions". |
| CHANGED-1 (15.1.6) | **Yes.** "Whether it stands later or is evaluated later". This holds because a claim evaluated after the port runs inside a top-level clause at or after the boundary, which is in the start set, and the closure over-approximates. |
| F6-5 | **Yes.** The record's events, tick 1 before the record, a close with a slot empty, N2 and N3 are all listed open. |
| F6-8 | **Yes.** "Written (closed with every read-once port filled ...)", tagged F6. |
| F6-7 | **Yes.** Condition 5 for the NOT-RUN log; `[follows: F6 (RO′-3, RO′-5)]` for the header-only log. |
| F6-9 | **Yes**, as open: "which other logs lacking the record are malformed". |
| F6-6 | **Yes.** His words are quoted. |
| F6-10 | **Yes.** The check is the verifier's, tagged `[follows: 15.4]`. |
| F6-4 | **Yes.** t is open, in 15.7.5 and in 15.15. |
| F6-2 | **Yes.** The premises are tagged open on 15.1.3's place and 15.7.1's counting, and listed in 15.15. |
| F6-13 | **Yes** (closing line). |
| F6-11 | **Yes.** |
| F6-1, F6-14 | **By his answers** (§2, §3). |
| F6-3 | **Partly.** T10.7 is scoped and T10.8 added, but T10.0 and 15.13.10 still stop at T10.7 (T10-1). |

**The status paragraph and the title** are accurate. His third answer governs this review and changes no clause.

**Untouched by either answer:** every other clause of the draft.

---

## 5. T10.7 and T10.8

**T10.7.**
- Scoped: "this holds only when the law declares no read-once port or its log holds the read-once record". Consistent with 15.13.8.
- But the scope sits in the italic note, not in the statement itself (T10-3).

**T10.8.**
- It agrees with 15.13.8's row: the cut, K̂, and the name "the read-once stop".
- But "When the log lacks the read-once record" also covers RO′-4's refusal before the declaration. There the cut is the refusal's own stack, not the declaration. T10.8 should be scoped as 15.13.8 is: "NOT-RUN or LOG-OPEN with the record absent" (T10-2).

**T10.0** still reads "T10.1 to T10.6 hold (and T10.7 from version 1)", which omits T10.8. 15.13.10 says "split into T10.0 to T10.7". 15.13.10 is in neither set; I record it as a dependency found now (T10-1).

Nothing here is proved.

---

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| STOPROW-1 | QUESTION | The stop's row is chosen by "the read-once record absent", which a LOG-OPEN receipt does not show (S-P2: one status line, two K̂). Its carrier must be fixed: a receipt or status form (finding 8 / identity and bytes), or the court reading the log. | **yes**: the carrier, since reading the log in the court touches R6's "data, never a channel" |
| STOPROW-2 | DRAFTING | 15.13.8's new row cites no T10 row; it should cite T10.8. | no |
| V1CHECK-1 | DRAFTING | Omits his "It does not close the format-freeze question". The tag lacks "F6". | no |
| V1CHECK-2 | GAP | The owed check's object is undefined: "K̂ equals the rest of the block" holds by RO′-6's definition. State what is compared (containment or equality with the continuation's reach), on which fixtures, and its pass condition (SN-1). | **only if** he meant equality (precision) rather than containment (soundness) |
| V1CHECK-3 | QUESTION | 1a's rows read HELD through the meet, which "names the exact digest". With the pin waiting on the version-1 check, can 1a's rows run against the unpinned, proposed CUT-0? If not, the check is on the build's path. | **yes**: the order of work |
| V1CHECK-4 | GAP | 15.13.7 defines the continuation only "had the refusing operation returned". The stop, NOT-RUN and LOG-OPEN have no refusing operation, and the version-1 check, T10.7 and T10.8 need the continuation "had the missing input arrived, with any value". | no (the pin's wording) |
| T10-1 | DRAFTING | T10.0 omits T10.8, and 15.13.10 says "T10.0 to T10.7". 15.13.10 is a dependency found now. | no |
| T10-2 | COHERENCE | T10.8's "When the log lacks the read-once record" covers RO′-4's refusal before the declaration. Scope it to the stop (NOT-RUN or LOG-OPEN with the record absent). | no |
| T10-3 | DRAFTING | T10.7's scope sits in its italic note rather than in its statement. | no |
| CHANGED-1 | DRAFTING | 15.15's "15.5 and 15.6" row still cites finding 6, while the 15.3/15.4 row says finding 6 is ruled with its open parts listed elsewhere. | no |

As his third answer requires, the drafting fixes above (STOPROW-2, V1CHECK-1, T10-1 to T10-3, CHANGED-1, and V1CHECK-4 when the pin is worded) should be recorded with the re-read each one needs before the build.
