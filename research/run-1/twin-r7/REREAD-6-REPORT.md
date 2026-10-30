<!-- R7 re-read 6, saved by the draft's author, 2026-10-27: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 6: draft 8, the containment test, findings 8 and 20 before the pin, and RO′-5 (the twin's report)

This is the same reviewer's sixth re-read under R7. It is review evidence: not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture's outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound or that the version-1 containment test passes, and neither is reported as shown.

## Summary

Draft 8 states his three answers faithfully. It applies all eight OWED fixes as their dispositions record; CARRIER-3 is settled by his RO′-5 confirmation rather than left to finding 8. ORDER-2's question is answered: the version-1 reference runs the test before the pin, and nothing runs *against* an unpinned CUT-0.

There are 10 findings. Two need his decision:

- **PIN-3.** The stop row's premises rest on 15.1.3's open place rule (read-once ports at the top level) and on 15.7.1's open counting. By his own Q2 reasoning ("Both affect the rule being identified by the digest ... so CUT-0's digest identifies a rule with those inputs fixed"), the place rule changes the rule itself: "a top-level frame". Should it, and counting, also be fixed before the pin?
- **PIN-1 (conditional).** If CUT-0 reads the cut from `'R'`'s bytes, the format freeze (P6) is also an input of the pinned rule. The draft leaves P6 untimed against the pin.

The rest are drafting points. Two matter most:

- **PIN-4.** The draft's order lists the test before findings 8 and 20. His push sequence puts findings 8 and 20 first (his step 2), then the test (step 3).
- **TEST-3.** The test's result should be tied to the exact candidate whose digest is then pinned.

## 1. Provenance

**Opened**, all in `twin-r7-reread6/`:
- `REREAD-6-BRIEF.md`, whole.
- `DRAFT-8-CHANGES.md`, whole.
- `REREAD-5-DISPOSITION.md`, whole.
- `RULINGS-AS-RULED.md`: a Grep of its section headings, then lines 442–497.
- `T10-STATEMENTS.md`, whole.
- `AR-REREAD-6.md`, whole.
- `SPEC-15-DRAFT-8.md`, whole.

**Not opened:**
- `SPEC.md` and `RUNTIME-SPEC.md`. I rely on my earlier full reading; the brief says the bytes are the same.
- `RULINGS-AS-RULED.md` lines 1–441. I rely on my earlier reading.
- Draft 7. My comparisons with it are from re-read 5.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** `ROUNDS.md`'s T10.8 notes column. DRAFT-8-CHANGES says his Q1 answer is "recorded in T10.8's notes", but the statement shown here does not carry it (T10-1).
- **SN-2.** `CUT-SCHEMA.md` P6, and whether CUT-0 reads the cut from `'R'`'s bytes (PIN-1).
- **SN-3.** The containment test's fixture set and who fixes it (TEST-2).

---

## 2. Q1: the containment check is a fixture test (A_TEST, 19 clauses)

His words: "a fixture-based containment test run by the version-1 reference before the pin ... every claim the same law evaluates after the read-once stop, over each tested log that supplies the required record, lies within K̂. Any claim outside K̂ falsifies containment ... without running any court rows against an unpinned CUT-0. Record the result as MEASURED on those fixtures only. It does not establish universal containment or close T10.8 ..."

### 2.1 Faithfulness

**15.13.8.** "The check is a test on fixtures, run by the version-1 reference before the pin: for each tested log that supplies the record, every claim ... must lie in K̂, and any claim outside K̂ falsifies containment. No court row runs against an unpinned CUT-0. Its result is MEASURED on those fixtures only: it establishes neither containment over every log nor T10.8, and no test result or measurement alone closes T10 (15.13.10). [ruled: F6, his answer on Q1]"
- **Faithful.**

**15.13.4.** "The version-1 reference runs the containment test before the pin; no court row runs against an unpinned CUT-0, and nothing of 1a is built or run against it."
- **Faithful.** It answers re-read 5's ORDER-2: the reference may exist and run before the pin, and only what runs *against* CUT-0 waits.

**The legend's F6 entry** names "the check as a fixture test". Faithful.

### 2.2 Coherence (every clause of A_TEST)

**15.13.8.**
- **Two scopes.** The V1CHECK-2 sentence, which is ruled, still reads "over any log that supplies the record ... the check passes only if none falls outside". The Q1 sentence reads "for each tested log".
- Read together, V1CHECK-2 names the property and Q1 the test that samples it. But "passes" appears only in the any-log sentence (TEST-1).

**15.15's row on 15.13.8.**
- "The version-1 containment test's fixtures, owed before the pin" is "decided by: the pin". The fixtures must exist before the pin, so the pin cannot decide them.
- Nothing says who fixes and records the fixture set (TEST-2; SN-3).

**15.13.4 and 15.13.8.**
- The test computes K̂ with a CUT-0 candidate. If the candidate's code changes between the test and the pin, the pinned digest is not the code that was tested.
- The test's record should name the candidate's digest. Q2's "the applicable checks" for a new candidate supports this (TEST-3).

**15.13.10.** "T10.0 to T10.8 ... no test result or measurement alone closes it". Coherent with Q1.

**The 15.15 rows on 15.13.7 and 15.13.11.**
- Coherent. 15.13.7's continuation is the pin's wording.
- The test is operational ("the same law evaluates after the stop") and does not need 15.13.7's wording.

**15.0 Execution, 15.12.5, 15.12.6, 15.13.11.**
- Coherent. 1a's rows run after the pin, and the reference that runs the test is an execution.

**The F6-tagged 15.3, 15.5 (×3), 15.7.1, 15.7.5 and 15.13.9.** Untouched by Q1.

**15.12.4's table bullet** (matched on the word "fixture"). Its "the structural oracle tests it on its fixtures" is the PREFIX oracle, a different fixture set. Untouched.

### 2.3 Probes (UNEXECUTED; my worked consequences)

**T-P1. A fixture that holds.**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Perform check.
3. Let g be given as an integer.
4. Perform check.
5. Each tick, do the following.
5.1. Say g.
```

- Tested logs:
  - record g = 0, `end 0 closed`;
  - record g = 5, `t 1`, `end 1 closed`.
- After the stop point, at clause `3.`, the claim at 1.1 is evaluated through `4. Perform check`. K̂, the rest of the block from `3.`, includes it.
- So the claim lies inside K̂ on these two fixtures. Nothing beyond them follows.

**T-P2. A fixture that can falsify.**

```
1. To check, do the following.
1.1. We claim that 1 is positive.
2. Let g be given as an integer.
3. Each tick, do the following.
3.1. Perform check.
```

- Tested log: record g = 1, `t 1`, `end 1 closed`.
- The claim is evaluated in tick 1, through the tick body's `Perform check`.
- A CUT-0 candidate whose reach omitted the tick block's body would leave the claim outside K̂, which falsifies containment. A candidate that follows the tick body, as RO′-6 requires, contains it.
- This shows what the test can catch. It shows nothing about the real candidate.

---

## 3. Q2: findings 8 and 20 resolved before the pin (A_PIN, 40 clauses)

His words: "resolve Finding 8 and Finding 20 before pinning CUT-0. Both affect the rule being identified by the digest ... Resolve and record both before pinning ... Then run 1a's rows against that pinned rule. If either decision later changes the rule, treat it as a new CUT-0 candidate requiring a new digest and the applicable checks—not as a silent change under the old pin."

### 3.1 Faithfulness

- **The legend's `[ruled: claims]`.** "and by his answers that order its pin: the order of work, and findings 8 and 20 resolved before the pin". Faithful.
- **15.7.5.** "finding 8 defines the form's encoding, and is resolved and recorded before CUT-0's digest is pinned". Faithful.
- **15.9.** "Whether it carries the cut is resolved and recorded before CUT-0's digest is pinned, since the rule the digest identifies depends on it. [ruled: claims, his answer on Q2]". Faithful.
- **15.13.4.** It gives the order; quotes his V1CHECK-3 words ("The claims ruling requires the meet to be pinned ... The check belongs on 1a's build path"); and states "A later decision on finding 8 or 20 that changes the rule makes a new CUT-0 candidate, with a new digest and the applicable checks, never a silent change under the old pin." **Faithful.**
- **15.12.5, 15.12.6, 15.13.11.** "once CUT-0's digest is pinned (15.13.4)", tagged "claims, the pin's order". Faithful.
- **15.15's 15.9 row and 15.5/15.7.5 row.** "before the pin (his answer on Q2)". Faithful.

### 3.2 Coherence (every clause of A_PIN)

**15.9 and its 15.15 row.**
- Whether `'R'` carries the cut comes before the pin. "Its bytes: the format freeze (P6), after the tick block's and the ports' frames are derived" carries no timing against the pin.
- If CUT-0 reads the cut from `'R'`'s bytes, the byte format is an input of the pinned rule, just as finding 8's encoding is (PIN-1; SN-2).

**15.15's rows on finding 8.**
- The 15.5/15.7.5 row says "finding 8, before the pin".
- The 15.5/15.6 row also lists finding 8's items (the LOG-* conditions and order, a load refusal's receipt), decided by "the amended set's 'identity and bytes'", with no timing.
- His "resolve Finding 8 ... before pinning" reads as the whole finding (PIN-2).

**15.13.8, the stop row's premises.**
- They are "[open: 15.1.3's top-level place and 15.7.1's counting, on which the first two rest]", and 15.15 says they are decided by "the pin; the amended set's 'port place' and 'counting'".
- The place rule changes the rule itself: RO′-6's cut is "a top-level frame".
- By his Q2 reasoning, inputs that affect the rule the digest identifies are fixed before the pin. Q2 names only findings 8 and 20 (PIN-3).

**15.13.4, the order against his push sequence.**
- The draft reads: "the version-1 containment test ..., and findings 8 and 20 resolved and recorded ...; then the pin".
- His push sequence reads: "2. Resolve Finding 8 and Finding 20 before pinning CUT-0. 3. Run the version-1 containment fixture test ... 4. Pin".
- If the test runs before findings 8 and 20 and they then change the candidate, his Q2 requires "the applicable checks" again. The draft should follow his sequence, or say that a candidate changed by them is tested again (PIN-4).

**The legend's `[pinned]`.**
- "It can change until the pin" is coherent. After the pin, a change is a new candidate (Q2).

**The 15.13 closing line (the pin's reach rules) and 15.13.7 (the pin's wording).**
- Both are decided at the pin. Coherent.

**One line each, untouched by Q2 or using a word in another sense:**
- 15.2.1;
- 15.5's record line, end record ("candidate A1"), forms and load refusals;
- 15.7.1;
- 15.8's status line;
- 15.10's digests;
- 15.11 ("a matching digest");
- 15.13.1–3, 15.13.5–6, 15.13.9 and 15.13.10;
- 15.15's 15.2 and 15.10 rows;
- 15.15's rows on 15.13.8 and 15.13.7.

---

## 4. RO′-5 confirmed (A_RO5, 17 clauses)

His words: "Your reading is correct. The read-once stop does not introduce a fifth status word. It remains `NOT-RUN` or `LOG-OPEN`, with an explicit distinguishing status form; Finding 8 must define its encoding. Do not revise RO′-5."

### 4.1 Faithfulness

**15.7.5.**
- "The stop has an explicit receipt status that distinguishes it from a LOG-OPEN run that holds the read-once record but ran no tick. [ruled: F6, his answer on STOPROW-1]". This uses his STOPROW-1 words, so CARRIER-1 is answered.
- "It remains NOT-RUN or LOG-OPEN, with an explicit distinguishing status form, never a fifth status word; finding 8 defines the form's encoding". **Faithful** to his confirmation.
- "A NOT-RUN at the stop names a read-once port (RO′-3), and it too carries a distinguishing form." His confirmation, "It remains `NOT-RUN` or `LOG-OPEN`, with an explicit distinguishing status form", covers both cases, so this follows. It answers CARRIER-3 more definitely than its disposition foresaw ("whether ... is finding 8's"), and the encoding stays finding 8's.

**15.13.8.**
- The old row: "The court applies this row when the receipt's status is not in the read-once stop's distinguishing form (15.7.5)". CARRIER-2 is answered.
- The stop row's heading: "NOT-RUN or LOG-OPEN in the stop's distinguishing form". Faithful.

### 4.2 Coherence (every clause of A_RO5)

**15.7.5.**
- One term would serve better. "An explicit receipt status" in one sentence and "an explicit distinguishing status form" in the next name one thing. The first can still be read as a status word (RO5-1).

**15.13.8, the old row's "which is so when the law declares no read-once port or its log holds the read-once record".**
- This is a drawn statement under a ruled tag. It is correct for NOT-RUN and LOG-OPEN statuses: a refusal before the declaration is REFUSED, not this row's.

**The 15.15 row "the four statuses"; 15.8's status line.**
- Coherent: there is no fifth status.

**One line each, untouched:**
- 15.3's `close()`, which is a tick's NOT-RUN;
- 15.5 (×3);
- 15.7.1;
- 15.13.4;
- 15.13.9;
- 15.15's rows on 15.5/15.7.5 and 15.13.8;
- the closing line;
- the status paragraph.

### 4.3 Probe (UNEXECUTED; my worked consequence)

**R-P1.** T-P1's law.
- Log A (the record present, open, no ticks) gives plain LOG-OPEN, so the old row applies.
- Log B (header only) gives LOG-OPEN in the stop's form (encoding open), so the stop row applies.
- A read-once NOT-RUN naming g carries the stop's form as well.
- The court reads only the status.

---

## 5. Re-read 5's OWED findings

| finding | answered as disposed? |
|---|---|
| CARRIER-1 | **Yes.** His words, "an explicit receipt status that distinguishes", and RO′-5 beside them. |
| CARRIER-2 | **Yes.** Both rows are chosen by the status form. |
| CARRIER-3 | **Yes.** It is stated more definitely than disposed, on his confirmation; the encoding stays finding 8's. |
| CONTAIN-1 | **Yes.** The version-0 results are stated; the equality holds by definition in version 1; containment is owed; his grades are quoted. The version-0 results sentence carries a ruled tag (CHANGED-1). |
| CONTAIN-3 | **Yes.** The 15.15 row on 15.13.7 cites his V1CHECK-2 words, "bears on it and does not word it". |
| ORDER-3 | **Yes.** The pointers, the claims tag, and his omitted words quoted. |
| CHANGED-1 | **Yes.** "In re-read 4's words, V1CHECK-4". |
| T10-1 | **Yes.** The notes in T10.0 and T10.8 are moved out. |

**T10.0, T10.8.** Coherent with 15.13.8. Nothing here is proved.

---

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| TEST-1 | DRAFTING | 15.13.8 gives the check two scopes: V1CHECK-2's "over any log ... passes only if none falls outside" and Q1's "for each tested log". Say that the first is the property and the second the test that samples it, with "passes" meaning on the tested logs. | no |
| TEST-2 | DRAFTING | 15.15 has the test's fixtures "decided by: the pin", which comes after the test. Name who fixes and records the fixture set before the test (SN-3). | no |
| TEST-3 | GAP | The test runs against a CUT-0 candidate. Its record should name that candidate's digest, so that the pinned digest is the code tested. Any change between the test and the pin is a new candidate, by his Q2 ("the applicable checks"). | no |
| PIN-1 | QUESTION | Finding 20 ("whether `'R'` carries the cut") comes before the pin, but the cut's bytes (P6) carry no timing against it. If CUT-0 reads the cut from `'R'`'s bytes, P6 is an input of the pinned rule (SN-2). | **only if** CUT-0 reads the cut from the trace's bytes |
| PIN-2 | DRAFTING | 15.15's 15.5/15.6 row lists finding 8's LOG-* conditions and a load refusal's receipt with no "before the pin". His "resolve Finding 8 ... before pinning" reads as the whole finding, as the 15.5/15.7.5 row has it. | no (default: the whole finding) |
| PIN-3 | QUESTION | The stop row's premises rest on 15.1.3's open place rule and 15.7.1's open counting. The place rule changes the rule itself (RO′-6's "a top-level frame"). By his Q2 reasoning, should these be fixed before the pin too? Q2 names only findings 8 and 20. | **yes** |
| PIN-4 | DRAFTING | 15.13.4 lists the test before findings 8 and 20. His push sequence has findings 8 and 20 (step 2) before the test (step 3). Follow his sequence, or say that a candidate they change is tested again. | no (his sequence decides) |
| RO5-1 | DRAFTING | 15.7.5 names one thing two ways, "an explicit receipt status" and "an explicit distinguishing status form". Use the second, his confirmation's term, so that no reader takes a status word. | no |
| CHANGED-1 | DRAFTING | 15.13.8's account of the version-0 result ("CUT-0 as built ... gave the K̂ ..., and containment held") reports packet F §4, but sits under "[ruled: F6, his answer on F6-14 ...]". Tag it [follows] with its source. Only the grades are his. | no |
| T10-1 | QUESTION | DRAFT-8-CHANGES says his Q1 answer is "recorded in T10.8's notes". T10.8's note in `T10-STATEMENTS.md` does not carry it. Either it is in another column (SN-1) or it is missing. | no |

By his ruling on the re-reads, the drafting fixes (TEST-1, TEST-2, TEST-3, PIN-2, PIN-4, RO5-1, CHANGED-1, and T10-1 if missing) are to be recorded with their re-read owed before the build. PIN-3 goes to him, and PIN-1 goes to him only if CUT-0 reads the cut from `'R'`'s bytes.
