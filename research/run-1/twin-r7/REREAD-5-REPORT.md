<!-- R7 re-read 5, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 5: draft 7, the stop's carrier, the owed check and the order of work (the twin's report)

The same reviewer's fifth re-read under R7. It is review evidence: not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture's outcome is **my own worked consequence**. Nothing in this report shows that CUT-0 is sound, or that the version-1 containment check passes. Neither is reported as shown.

## Summary

Draft 7 applies all six OWED fixes of re-read 4 as their dispositions record. It lists V1CHECK-4 open and states his three answers mostly faithfully.

There are 11 findings. Two need his decision, and both concern the order of work he set (check, then pin, then 1a):

- **ORDER-1.** CUT-0 is to choose the stop's row "from the receipt's status", and that status's encoding belongs to finding 8. If the row choice is part of CUT-0, finding 8's encoding must come before the pin. Finding 20 (the cut's carrier) may also bear on the pin. The order does not place either.
- **ORDER-2.** The containment check evaluates version-1 laws over logs, so it needs a version-1 execution. "Nothing of 1a is built or run against an unpinned CUT-0" can be read as "no part of 1a before the pin". On that reading the order is circular. His word "against" supports the narrower reading: only what runs against CUT-0 waits.

Two more need his decision only conditionally:

- **CARRIER-1.** The draft's "a status of its own" sits beside RO′-5's "not a fifth status". It needs his decision only if finding 8 would encode the stop as a fifth status word.
- **CONTAIN-2.** "Over any log" cannot be established by a check on a sample. It needs his decision only if he meant a proof over every log, rather than a test, before the pin.

## 1. Provenance

**Opened**, all in `twin-r7-reread5/`:
- `REREAD-5-BRIEF.md`, whole.
- `DRAFT-7-CHANGES.md`, whole.
- `REREAD-4-DISPOSITION.md`, whole.
- `AR-REREAD-5.md`, whole.
- `T10-STATEMENTS.md`, whole.
- `RULINGS-AS-RULED.md`: a Grep of its section headings, then lines 410–443.
- `SPEC-15-DRAFT-7.md`, whole.

**Not opened:**
- `SPEC.md` and `RUNTIME-SPEC.md`. I relied on my earlier full reading; the brief says the bytes are the same.
- `RULINGS-AS-RULED.md` lines 1–409. I relied on my earlier reading.
- Draft 6. My comparisons with it are from re-read 4.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** What 1a comprises, and what executes the containment check (ORDER-2).
- **SN-2.** `packets/F-read-once-adversary.md` §4: the sample behind the version-0 MEASURED containment (CONTAIN-1, CONTAIN-2).
- **SN-3.** Finding 8's record (the stop status's encoding) and finding 20 / CUT-SCHEMA P6 (the cut's carrier), for ORDER-1.

---

## 2. Answer 1: the carrier (STOPROW-1). A_CARRIER, 44 clauses

His words: "The read-once stop must have an explicit receipt status that distinguishes a stop caused by the absent record from a LOG-OPEN run in which the read-once record exists but no tick ran. The exact receipt bytes and status encoding remain for Finding 8; do not invent them now. The court selects the responsible row from the receipt, not by inspecting the log or inferring absence from trace events."

### 2.1 Faithfulness

**15.7.5.** "The stop has an explicit receipt status of its own, which tells it from a LOG-OPEN run that holds the read-once record but ran no tick; its bytes and its encoding are finding 8's. [ruled: F6, his answer on STOPROW-1; open: finding 8, the encoding]"
- Faithful, with one addition: "**of its own**" is the draft's wording. He wrote "an explicit receipt status that distinguishes".
- Two lines above, RO′-5 (ruled) says the stop "is a case of NOT-RUN or LOG-OPEN, not a fifth status" (CARRIER-1).

**15.13.8.** "The court chooses this row from the receipt's status (15.7.5), never by inspecting the log or by inferring the record's absence from the trace. [ruled: F6, his answer on STOPROW-1]" **Faithful.**

**The legend's [ruled: F6] and 15.15.** Both name the answer. Faithful.

### 2.2 Coherence (every clause of A_CARRIER)

**15.7.5 against RO′-5.** The two ruled texts are compatible if the stop's status is a marked form of NOT-RUN or LOG-OPEN, with its marker's encoding left to finding 8. They clash if the stop's status is a distinct status word. The draft's "of its own" leans toward the second reading (CARRIER-1). 15.15's row "the four statuses" agrees only with the first.

**15.13.8.**
- The selection is now by status.
- The old row's condition still reads by the log: "This row applies only when the law declares no read-once port or its log holds the read-once record". So does the stop row's heading, "with the read-once record absent". Under his answer, the court must choose between them from the status (CARRIER-2).

**NOT-RUN.**
- His answer speaks only of LOG-OPEN. For a read-once NOT-RUN, the status names the port, and the port's kind (read from the law) already tells the stop from a tick's NOT-RUN.
- The draft's general sentence ("an explicit receipt status of its own") covers both cases, which is consistent. It does not say how the NOT-RUN case is told apart (CARRIER-3).

**15.8.** The status line, the core, the frame check and "no validity line" are coherent. The stop's status is in the core, so backends must agree on it.

**15.11 Replay.** Coherent. The execution derives the status from the log it loaded, deterministically.

**15.7.1 and 15.5's three F6 bullets.** Untouched. 15.7.1's "NOT-RUN ... or LOG-OPEN" is consistent with the marked-form reading.

**One line each, untouched:**
- 15.3;
- 15.4 (three records; two histories);
- 15.5 load refusals;
- 15.10 (no `'T'` at the stop, so the invariant is vacuous);
- 15.12.3;
- 15.12.6;
- 15.13.9;
- 15.14;
- the status paragraph;
- 15.15's untouched rows: 15.0/15.1, 15.1.3, 15.1.5, 15.1.6, 15.2, 15.7.1–3, 15.7.6, 15.9, 15.10, 15.11/15.8, 15.13.9, 15.13.11, 15.14.

### 2.3 Probes (UNEXECUTED; my worked consequences)

**C-P1 (re-read 4's S-P2, now by status).**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Perform check.
3. Let g be given as an integer.
4. Perform check.
5. Each tick, do the following.
5.1. Say g.
```

- **Log A** (the record present, open, no tick records):
  - status: plain LOG-OPEN;
  - row: the old row;
  - K̂: the tick block;
  - so, in 1a after the pin, the claim is held.
- **Log B** (header only):
  - status: the stop's own status (encoding open);
  - row: the stop's row;
  - K̂: includes `4. Perform check`;
  - so the claim is withheld, as "the read-once stop".
- The court tells the two logs apart from the status alone.

**C-P2 (a read-once NOT-RUN).**
- Law: `1. Let g be given as an integer.` then a tick block.
- Log: ends in a read-once NOT-RUN naming g.
- The status names g, whose kind is "once", so it is the stop. That holds whatever finding 8's marker turns out to be.

---

## 3. Answer 2: the owed check is containment (V1CHECK-2). A_CONTAIN, 12 clauses

His words: "The owed check is whether every claim that the same law evaluates after the read-once stop, over any log that supplies the required record, lies within K̂. It passes only if no such claim falls outside K̂. Do not require precision ... Record the check as a version-1 obligation, not as a result already established by the definition of K̂."

### 3.1 Faithfulness

**15.13.8.** "The owed check is containment: every claim the same law evaluates after the stop, over any log that supplies the record, lies in K̂, and the check passes only if none falls outside. Precision is not part of it ... It is an obligation, not a result the definition of K̂ establishes. [ruled: F6, his answer on V1CHECK-2]" **Faithful.**

**15.15's row** ("version-1 containment check, owed before the pin"). Faithful.

### 3.2 Coherence (every clause of A_CONTAIN)

**15.13.8, the grades sentence.** It still reads "That K̂ equals the rest of the block from the declaration was MEASURED on version-0 stand-ins only ...; for version 1 it is DECLARED".
- In version 1 that equality holds by RO′-6's definition. Re-read 4's disposition records that what the version-0 stand-ins MEASURED was containment: "every claim the resumed run evaluated after the cut was in K̂".
- So the grades should attach to containment, and the sentence should say so. His F6-14 answer called the object "the equality", so the restatement should note that his V1CHECK-2 answer has defined it (CONTAIN-1).

**"Over any log that supplies the record".** This ranges over infinitely many logs.
- A check on a finite sample can refute containment, but cannot establish it for every log.
- The draft should say what the check runs on and what its pass means. A pass is MEASURED on its sample, and T10.8 stays open, as the claims ruling requires ("No test result or measurement alone closes T10") (CONTAIN-2).

**15.15's 15.13.7 row (V1CHECK-4).** His containment definition already gives the continuation at the stop an operational meaning: the same law, over logs that supply the record. The row could cite it (CONTAIN-3).

**Untouched by this answer:**
- the status paragraph, the legend and 15.13.9: coherent;
- the F6-tagged 15.3, 15.5 (×3), 15.7.1 and 15.7.5;
- 15.15's closing line.

### 3.3 Probes (UNEXECUTED; my worked consequences)

**K-P1.**
- C-P1's law, over logs that supply g with any value and any tick records.
- The claims evaluated after the stop are the claim at 1.1, reached by `4. Perform check`. It is in K̂, so it is contained on this fixture.
- This one fixture shows nothing in general.

**K-P2.**
- C-P1's law with `4.` removed.
- After the stop, the claim is never evaluated (`check` is performed only at `2.`), and K̂ (port declaration, tick body `Say`) does not hold it.
- Containment is unaffected. This is consistent with "precision is not part of it".

---

## 4. Answer 3: the order of work (V1CHECK-3). A_ORDER, 26 clauses

His words: "Complete the version-1 containment check first, pin the exact CUT-0 digest second, and only then run 1a's rows against that pinned candidate. The claims ruling requires the meet to be pinned to the exact CUT-0 digest; labelling an unpinned proposal does not satisfy that condition. The check belongs on 1a's build path, and real court readings still hold no claims before 1b. Do not build or run 1a against an unpinned CUT-0."

### 4.1 Faithfulness

**15.13.4.** "The order of work: the version-1 containment check of the read-once stop's row (15.13.8), then the pin of CUT-0's exact digest, then 1a's rows against that pinned candidate. Nothing of 1a is built or run against an unpinned CUT-0. [ruled: F6, his answer on V1CHECK-3]"
- **Faithful.**
- Omitted, in his words: "labelling an unpinned proposal does not satisfy that condition" and "The check belongs on 1a's build path". His "real court readings still hold no claims before 1b" is in 15.13.11.

### 4.2 Coherence (every clause of A_ORDER)

**15.13.4 against 15.13.8 and finding 8.**
- 15.13.8 has the court choose the stop's row "from the receipt's status", and that status's encoding belongs to finding 8.
- If the row choice is part of CUT-0, the CUT-0 to be pinned depends on finding 8's encoding, so finding 8 comes before the pin.
- 15.9 also says withholding rows need the cut, whose carrier is finding 20 ("Changing 'R''s payload therefore needs a ruling").
- The order names only the check before the pin (ORDER-1).

**15.13.4, "Nothing of 1a is built or run against an unpinned CUT-0".** Two readings:
- (a) no part of 1a is built before the pin;
- (b) only what runs against CUT-0 (the court's rows) waits.
- The containment check evaluates claims of version-1 laws over logs, so it needs a version-1 execution. If that execution is part of 1a, reading (a) makes the order circular: the check needs the execution, the pin needs the check, and 1a needs the pin.
- His "against an unpinned CUT-0" supports reading (b). The draft should state it, and name what executes the check (ORDER-2; SN-1).

**15.12.5, 15.12.6 and 15.13.11 (1a's rows).**
- Coherent with the order, but none of them points to 15.13.4's pinned candidate.
- The order also sits under an F6 tag, although it governs every 1a row (ORDER-3).

**The legend's [pinned].** "No digest is pinned yet ... it can change until the pin". Coherent.

**15.13.5–15.13.7, the closing line and 15.13.9.** Untouched. The pin's open wording (15.13.7, V1CHECK-4) and its version-1 reach rules are content of the pin, consistent with "the pin's to state".

**15.2.1, 15.10 (×3), 15.11's "digest", and 15.15's rows on 15.2 and 15.10.** Untouched. Under reading (b) these 1a items do not wait for the pin.

**The F6-tagged 15.3, 15.5 (×3), 15.7.1 and 15.7.5.** Untouched by the order.

---

## 5. Re-read 4's OWED and OPEN findings

| finding | disposition | answered in draft 7 / T10-STATEMENTS? |
|---|---|---|
| STOPROW-2 | OWED | **Yes.** The stop row cites "(T10.8)". |
| V1CHECK-1 | OWED | **Yes.** His "It does not close the format-freeze question or authorize pinning before the check.", tagged "[ruled: F6, his answer on F6-14]". |
| T10-1 | OWED | **Yes.** T10.0 names T10.8, and 15.13.10 reads "T10.0 to T10.8". |
| T10-2 | OWED | **Yes.** T10.8 is scoped: "never at a refusal before the first read-once declaration, RO′-4's case". |
| T10-3 | OWED | **Yes.** T10.7's scope is in its statement. |
| CHANGED-1 | OWED | **Yes.** The "15.5 and 15.6" row lists findings 8, 35, 36, 37 and 56. |
| V1CHECK-4 | OPEN | **Yes, listed** as 15.15's row on 15.13.7, decided by the pin's wording. Its quoted phrase is mine, not his (CHANGED-1 below). |

Title and status are accurate. The closing line names what draft 7 adds.

**T10.0, T10.7, T10.8.** Coherent with 15.13.8. T10.0 and T10.8 now carry dated editorial notes inside their statements, which T10-3 moved out of T10.7 for the same reason (T10-1 below). Nothing here is proved.

---

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| CARRIER-1 | COHERENCE | 15.7.5's "an explicit receipt status **of its own**" (the draft's words; his are "an explicit receipt status that distinguishes ...") sits two lines after RO′-5's "not a fifth status". Read it as a marked form of NOT-RUN or LOG-OPEN, its marker finding 8's, and say so. | only if finding 8 would encode the stop as a fifth status word |
| CARRIER-2 | DRAFTING | The old NOT-RUN/LOG-OPEN row's condition ("its log holds the read-once record") and the stop row's heading are phrased by the log's content. Under his answer, the row is chosen from the status; restate the old row's condition as "when the status is not the stop's". | no |
| CARRIER-3 | DRAFTING | His answer covers LOG-OPEN. The draft does not say how a read-once NOT-RUN is told apart: by the read-once port its status names, or by the same explicit marker. | no |
| CONTAIN-1 | DRAFTING | The grades sentence still says "K̂ equals the rest of the block ... DECLARED for version 1", which in version 1 holds by definition. Per the disposition, the version-0 stand-ins MEASURED containment. Attach the grades to containment, noting that his V1CHECK-2 answer defines what his F6-14 answer called "the equality". | no |
| CONTAIN-2 | QUESTION | "Over any log that supplies the record" cannot be established by a check on a sample. State the check's fixtures, and that its pass is MEASURED on them, with T10.8 still open. | only if he meant a proof over every log, rather than a test, before the pin |
| CONTAIN-3 | DRAFTING | His containment definition gives the stop's continuation an operational meaning (the same law over logs supplying the record). 15.15's V1CHECK-4 row could cite it. | no |
| ORDER-1 | QUESTION | If CUT-0 itself chooses the stop's row "from the receipt's status", the pinned digest depends on finding 8's status encoding. The withholding rows also need the cut, whose carrier is finding 20 (unruled). "Check, pin, 1a" places neither. | **yes**: where findings 8 and 20 fall in the order |
| ORDER-2 | COHERENCE | The containment check needs a version-1 execution. If that is part of 1a and "nothing of 1a is built" before the pin, the order is circular. His "against an unpinned CUT-0" supports "only what runs against CUT-0 waits". State it, and name what executes the check (SN-1). | **yes**: confirm the narrower reading, or name the check's executor |
| ORDER-3 | DRAFTING | 15.12.5, 15.12.6 and 15.13.11 do not point to 15.13.4's pinned candidate. The order, which governs every 1a row, is tagged only F6. His "labelling an unpinned proposal does not satisfy that condition" is omitted. | no |
| CHANGED-1 | DRAFTING | 15.15's 15.13.7 row puts the twin's words ("had the missing input arrived, with any value") in quotation marks, which in this draft mark his words. Attribute them, or drop the quotes. | no |
| T10-1 | DRAFTING | T10.0 and T10.8 carry dated editorial notes inside their statements' parentheses; T10-3 moved T10.7's out of its statement for that reason. | no |

By his ruling on the re-reads, the drafting fixes above (CARRIER-2, CARRIER-3, CONTAIN-1, CONTAIN-3, ORDER-3, CHANGED-1, T10-1) are to be recorded with their re-read before the build. CARRIER-1 can be settled in the draft, unless finding 8 would make the stop a fifth status. ORDER-1 and ORDER-2 go to him. CONTAIN-2 goes to him only if he meant a proof.
