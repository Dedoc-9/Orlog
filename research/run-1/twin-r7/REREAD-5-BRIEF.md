# R7's fifth re-read: the brief to the twin (2026-10-27)

Since your fourth re-read, the release your third and fourth re-reads preceded has been pushed (9de2792), and the owner
has answered the three questions your fourth re-read raised:
- **STOPROW-1:** the receipt's status tells the court the read-once record was absent; its bytes and encoding are
  finding 8's.
- **V1CHECK-2:** the owed version-1 check is containment, without precision.
- **V1CHECK-3:** the containment check, then the pin of CUT-0's exact digest, then 1a; nothing of 1a against an
  unpinned CUT-0.

Draft 7 applies the six fixes your fourth re-read's disposition recorded (STOPROW-2, V1CHECK-1, T10-1, T10-2, T10-3,
CHANGED-1), lists its one OPEN item (V1CHECK-4) in 15.15, and states these three answers. By his ruling on the re-reads,
*"Any further drafting fixes must be recorded with their required re-read before the build, as R7 requires."* This is
that re-read.

## Your reading set

These files, in this folder. Open nothing else, and list every file you open.

- `SPEC-15-DRAFT-7.md`: the draft.
- `RULINGS-AS-RULED.md`: its last section holds the three answers, each with its question as put to him.
- `AR-REREAD-5.md`: the three answers' sets (44, 12 and 26 clauses; 57 in their union). They were computed over draft
  6, the text current when he answered: the line numbers are draft 6's. Of their 57 clause names, 55 name a clause of
  draft 7 as they stand; the other two begin with words draft 7 changed, the status paragraph ("Status. Draft 6
  applies…", now "Status. Draft 7 applies…") and 15.15's row on 15.13.8 ("version-1 check", now "version-1 containment
  check"), and both are among the changed clauses.
- `DRAFT-7-CHANGES.md`: what draft 7 changed, and why.
- `REREAD-4-DISPOSITION.md`: your fourth re-read's findings as disposed.
- `T10-STATEMENTS.md`: T10.0 to T10.8 now, after T10-1, T10-2 and T10-3.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before.

## What to read

- Every clause draft 7 changed or added (12).
- Every clause of the three answers' sets, once for each answer that names it. 15.13.10 enters D_r by T10-1; it is
  also among the changed clauses.
- T10.0, T10.7 and T10.8.

## What to report

For each answer in turn:
- **Faithfulness**, for each clause tagged with it: whether it states the answer as given, or adds to it, narrows it or
  alters it. Quoted words must be his.
- **Coherence**, for every clause of its set.

For each of your fourth re-read's OWED and OPEN findings, say whether draft 7 (or `T10-STATEMENTS.md`) answers it as
its disposition records.

A clean report would show neither that CUT-0 is sound nor that the version-1 containment check passes; do not report
either as shown. Mark every probe unexecuted, and every fixture's outcome as your own worked consequence.

Number the findings (CARRIER-1, …; CONTAIN-1, …; ORDER-1, …; CHANGED-1, …; T10-…). Give each a class (DRAFTING, GAP,
COHERENCE, QUESTION), and say whether it needs his decision. Name any further source you need, without opening it.

Deliver the report as text in your reply.
