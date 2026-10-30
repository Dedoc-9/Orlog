<!-- R7 re-read 7, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 7: draft 9, every input the pinned rule reads, fixed before the pin (the twin's report)

This is the same reviewer's seventh re-read under R7. It is review evidence: not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture's outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound, or that the version-1 containment test passes, and neither is reported as shown.

## Summary

Draft 9 states his answer faithfully, with one exception (INPUTS-2), and applies all seven OWED fixes as their dispositions record. Re-read 6's T10-1 is answered by the notes column, which I cannot see; I take the disposition's word for it.

**Findings:** 5 in all, one of which needs his decision.

- **INPUTS-2, needs his decision.** 15.13.4 says: "The inputs are every input the pinned rule reads: [port place, counting, finding 8, finding 20, the cut's decoding]".
  - His answer gives a principle ("every input the pinned rule reads must be fixed before the pin") and then lists "The stop row's inputs".
  - Equating the two narrows the principle. CUT-0's other rows also read things that are still open and not ordered before the pin:
    - the version-1 status forms NOT-RUN and LOG-OPEN, which the NOT-RUN/LOG-OPEN row reads (the "four statuses" row of 15.15);
    - the version-1 statement kinds that R2's open spellings define, which CUT-0's reach must traverse.
  - Whether his principle covers these is his to confirm.

**Other findings:**

- **INPUTS-1.** If the cut is in `'R'`, specifying its decoding before the pin needs the tick block's and the ports' frames. 15.9 says those are "not yet derived", and the draft ties their derivation only to P6's own trigger.
- **INPUTS-3, CHANGED-1, CHANGED-2.** Drafting points; see §4.

## 1. Provenance

**Opened**, all in `twin-r7-reread7/`:
- `REREAD-7-BRIEF.md`, whole.
- `DRAFT-9-CHANGES.md`, whole.
- `REREAD-6-DISPOSITION.md`, whole.
- `RULINGS-AS-RULED.md`: a Grep of its section headings, then lines 497–531.
- `AR-REREAD-7.md`, whole.
- `SPEC-15-DRAFT-9.md`, whole.
- `T10-STATEMENTS.md`, whole.

**Not opened:**
- `SPEC.md` and `RUNTIME-SPEC.md`. I rely on my earlier full reading; the brief says the bytes are the same.
- `RULINGS-AS-RULED.md` lines 1–496, as read in earlier re-reads.
- Draft 8. My comparisons with it are from re-read 6.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** `ROUNDS.md`, T10.8's notes column, which the disposition says records his Q1 answer.
- **SN-2.** `CUT-0.md`: which receipt fields and trace events the pinned rule reads. This decides the scope of INPUTS-2.
- **SN-3.** `CUT-SCHEMA.md`: the cut's frames, and in particular the tick block's and the ports' (INPUTS-1).

---

## 2. His answer: every input the pinned rule reads, fixed before the pin (A_INPUTS, 48 clauses)

His words, in part:
- "Adopt (a): every input the pinned rule reads must be fixed before the pin. The stop row's inputs must be settled before CUT-0 is pinned".
- The stop row's inputs: port place and counting; finding 8 ("the receipt's explicit distinguishing status form and its encoding"); finding 20; the cut's decoding ("The court must not silently derive it from execution instead").
- "The order is: resolve those inputs, complete the version-1 containment fixture test against the resulting candidate, pin that exact candidate's digest, then run 1a's rows against the pinned rule."
- "Keep the general format-freeze trigger as its own obligation".
- "If a later ruling changes an input or the rule, it requires a new candidate and digest, with the applicable checks repeated."
- "This settles the ordering question, not the underlying open rows themselves."

### 2.1 Faithfulness

**The legend's `[ruled: claims]`.** "And every input the pinned rule reads fixed before it". **Faithful.**

**15.1.3.** "The read-once stop's row (15.13.8) reads this place, so the amended set's 'port place' is resolved before CUT-0's digest is pinned." **Faithful.** His words name the rows themselves ("resolve the open amended-set rows governing the top-level-frame boundary"), so the whole "port place" row comes before the pin. 15.15's row says the same.

**15.7.1.** "The read-once stop's row (15.13.8) reads it, so the amended set's 'counting' is resolved before CUT-0's digest is pinned." **Faithful.** 15.15's row extends "before the pin" to the whole counting row: 15.7.2's c, the If-arm clause of 15.7.3, and 15.10's invariants. That is consistent with "counting rules".

**15.7.5.**
- "Finding 8 settles the form and its encoding, and is resolved and recorded before CUT-0's digest is pinned." **Faithful.**
- The stop's status is now named one way, his "explicit distinguishing status form", which answers RO5-1.

**15.9.**
- "If it does, whether and how the pinned rule decodes the cut from those bytes is specified before the pin: 'The court must not silently derive it from execution instead.' The general format freeze keeps its own trigger, and is not settled by this." **Faithful.**

**15.13.4.**
- His order is quoted. "If a later ruling changes an input or the rule ..." is quoted. "The general format freeze (P6) keeps its own trigger" is stated. The test's record names the candidate's digest, and the pin pins it.
- **Faithful, with one alteration:** "The inputs are every input the pinned rule reads: the amended set's 'port place' (15.1.3) and 'counting' (15.7.1), finding 8 (15.7.5), finding 20 and, if the cut is in `'R'`, its decoding (15.9)."
  - His list is introduced as "The stop row's inputs", under a general principle that covers every input of the pinned rule.
  - Presenting the stop row's list as all of "every input the pinned rule reads" narrows the principle (INPUTS-2).
- **Omitted:** his "This settles the ordering question, not the underlying open rows themselves. They still require their own rulings and evidence before the build gate opens." DRAFT-9-CHANGES says it, but the draft does not (INPUTS-3).

**15.13.8.** "Both are resolved before CUT-0's digest is pinned (15.13.4)", and "the test runs against the candidate the pin's inputs give". **Faithful.**

**15.15's rows on 15.1.3, 15.5/15.6, 15.7.1–3, 15.9 and 15.13.8, and the closing line.** **Faithful.**

### 2.2 Coherence (every clause of A_INPUTS)

**15.13.4, the scope of "every input".**
- CUT-0's NOT-RUN/LOG-OPEN row "applies when the receipt's status is not in the read-once stop's distinguishing form", so it reads the version-1 statuses NOT-RUN and LOG-OPEN.
- The encoding of those statuses sits under 15.15's row "15.7.5 and 15.8: the four statuses; `tick-ops` ...; the line order", decided by "identity and bytes", with no timing against the pin.
- CUT-0's reach ("Its rules for the version-1 kinds ... are the pin's to state") traverses the version-1 statement kinds. 15.1.1 says "A form R2 adds is a statement kind", and R2 is still open.
- By his principle, both look like inputs of the pinned rule. The draft's list leaves them out (INPUTS-2; SN-2).

**15.9 and its 15.15 row.**
- If finding 20 puts the cut in `'R'`, "how the pinned rule decodes it from those bytes" cannot be specified without the cut's frames.
- 15.9 says "The tick block's frame, and the ports', are not yet derived". 15.15 places that derivation only before P6 ("after the tick block's and the ports' frames are derived").
- So that derivation falls before the pin, while P6 keeps its own trigger. The draft does not say so (INPUTS-1; SN-3).

**15.7.5, the last sentence.**
- "Its NOT-RUN's t ... is open [open: finding 8; amended set 'identity and bytes']" carries no "before the pin".
- It is finding 8's, and the sentence before says finding 8 comes before the pin. 15.15's 15.5/15.7.5 row lists it there.
- Coherent.

**15.13.8, the test's record.**
- "Its record names that candidate's digest" sits under a tag that marks as ruled only "that the test runs against the resulting candidate". The disposition recorded the digest's naming as **[follows: his answers on Q1 and Q2]** (CHANGED-1).

**15.0 Prefix and Tick block** (`[open: R2; amended set "port place"]`).
- The port place row is now before the pin, so these definitions are fixed before it too. Coherent.

**The licence as ruled.**
- Its B1 bullet and its 5c identity ("holds while 15.1.3's places hold") are open on port place, which now comes before the pin. Coherent.
- The licence is not an input of CUT-0.

**The legend's `[pinned]`.**
- "It can change until the pin" is coherent with "a new candidate and digest" after it.

**15.12.5, 15.12.6, 15.13.11.**
- 1a's rows run "once CUT-0's digest is pinned". Coherent with his order.

**One line each, untouched or matching a word in another sense:**
- 15.0 Boundary;
- 15.1.6;
- 15.3;
- 15.5's record line, end record ("candidate A1"), forms, whole-log bullet and load refusals ("what of it is finding 8's, before the pin");
- 15.7.2 and 15.7.3, under the counting row;
- 15.10's digests;
- 15.11;
- 15.13.1–3 and 15.13.5–7;
- the closing line of 15.13;
- 15.13.9 and 15.13.10;
- 15.15's rows on 15.0/15.1 and 15.10;
- the status paragraph.

### 2.3 Probes (UNEXECUTED; my worked consequences)

**I-P1 (INPUTS-2).**

```
1. Let a be given each tick as an integer.
2. We claim that 1 is positive.
3. Each tick, do the following.
3.1. Say a.
```

- The log has `t 1 490000000000000003` and `end 1 not-run 2 INPUT-MISSING a`.
- The status is the tick's NOT-RUN, in an encoding that is still open.
- CUT-0 must tell this status from COMPLETED, REFUSED and the stop's form before it applies the NOT-RUN/LOG-OPEN row. If the NOT-RUN encoding were ruled after the pin and differed from the candidate's parser, the pinned rule would read a different status.

**I-P2 (INPUTS-1).**

```
1. Let a be given each tick as an integer.
2. Each tick, do the following.
2.1. Say 10 divided by a.
```

- The log supplies a = 0, so the run is `REFUSED DIVISION-BY-ZERO 3`.
- The cut is [the tick block, Say 3]. If `'R'` carries it, decoding it needs the tick block's frame, which 15.9 says is not yet derived.

---

## 3. Re-read 6's OWED findings

| finding | answered as disposed? |
|---|---|
| TEST-1 | **Yes.** "The sentence before names the property ...; the test samples it, and its pass means on the tested logs only", tagged [follows]. |
| TEST-2 | **Yes.** The fixtures are fixed and recorded before the test, and decided by 1a's specification, not by the pin. |
| TEST-3 | **Yes.** The record names the candidate's digest, and the pin pins that digest. A later change follows his "If a later ruling changes an input or the rule ...". |
| PIN-2 | **Yes.** "What of it is finding 8's, before the pin". |
| PIN-4 | **Yes.** His own order is quoted in 15.13.4. |
| RO5-1 | **Yes.** One term, "explicit distinguishing status form". |
| CHANGED-1 | **Yes.** The version-0 account is tagged [follows: packet F §4 ...; RO′-6], and only the grades stay his. |
| T10-1 | **Answered**, per the disposition's check of the notes column (SN-1). |

T10.0 to T10.8 are unchanged and coherent with draft 9.

---

## 4. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| INPUTS-1 | GAP | If finding 20 puts the cut in `'R'`, specifying its decoding before the pin needs the tick block's and the ports' frames, which 15.9 says are "not yet derived". Their derivation then falls before the pin. 15.15 ties it only to P6's own trigger. | no, it follows from his answer; state it |
| INPUTS-2 | QUESTION | 15.13.4 calls the stop row's inputs "every input the pinned rule reads". By his principle, CUT-0's other rows also read inputs still open and not ordered before the pin: the version-1 NOT-RUN and LOG-OPEN encodings (15.15's "four statuses" row) and the statement kinds R2's spellings define (15.1.1), which CUT-0's reach traverses (SN-2). | **yes**: confirm whether his principle covers these |
| INPUTS-3 | DRAFTING | 15.13.4 omits his "This settles the ordering question, not the underlying open rows themselves. They still require their own rulings and evidence before the build gate opens." | no |
| CHANGED-1 | DRAFTING | 15.13.8's "its record names that candidate's digest" carries no [follows] tag. The disposition recorded it as [follows: his answers on Q1 and Q2]. | no |
| CHANGED-2 | DRAFTING | 15.7.5's last sentence on the stop's NOT-RUN t carries no "before the pin". It is finding 8's, so the timing holds through the sentence before and through 15.15, but the clause could say it. | no |

By his ruling on the re-reads, INPUTS-1, INPUTS-3, CHANGED-1 and CHANGED-2 are to be recorded with their re-read before the build. INPUTS-2 goes to him.
