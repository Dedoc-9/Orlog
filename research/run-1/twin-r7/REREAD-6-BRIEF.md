# R7's sixth re-read: the brief to the twin (2026-10-27)

Since your fifth re-read, the owner has answered the questions it raised:
- **Q1 (your CONTAIN-2 and ORDER-2):** the containment check is a test on fixtures, run by the version-1 reference
  before the pin, with no court row run against an unpinned CUT-0. Its result is MEASURED on those fixtures only, and
  it closes neither containment in general nor T10.8.
- **Q2 (your ORDER-1):** findings 8 and 20 are resolved and recorded before CUT-0 is pinned. A later decision that
  changes the rule makes a new CUT-0 candidate, with a new digest.
- **RO′-5 (your CARRIER-1):** confirmed. The stop is NOT-RUN or LOG-OPEN with an explicit distinguishing status form,
  never a fifth status word, and finding 8 defines the form's encoding.

He also ruled when to push. That decides no clause of §15.

His words: *"Draft 8 should incorporate the eight owed fixes and these decisions, record the affected clauses, and
undergo re-read 6."* Draft 8 applies your fifth re-read's dispositions. Seven fixes are in the draft: CARRIER-1,
CARRIER-2, CARRIER-3, CONTAIN-1, CONTAIN-3, ORDER-3 and CHANGED-1. The eighth, T10-1, is in the theorem ledger. Draft 8
also states his answers. This is that re-read.

## Your reading set

These files, in this folder. Open nothing else, and list every file you open.

- `SPEC-15-DRAFT-8.md`: the draft.
- `RULINGS-AS-RULED.md`: its last section holds his answers, each with its question as put to him, and his word on the
  push.
- `AR-REREAD-6.md`: the three answers' sets.
  - Sizes: 19, 40 and 17 clauses; 46 in their union.
  - They were computed over draft 7, the text current when he answered, so the line numbers are draft 7's.
  - Of the 46 clause names, 44 name a clause of draft 8 as they stand. The other two begin with words draft 8
    changed:
    - the status paragraph ("Status. Draft 7 applies…", now "Status. Draft 8 applies…");
    - 15.15's row on 15.13.8 ("the read-once stop's version-1 containment check", now "the version-1 containment
      test's fixtures").

    Both are among the changed clauses.
- `DRAFT-8-CHANGES.md`: what draft 8 changed, and why.
- `REREAD-5-DISPOSITION.md`: your fifth re-read's findings as disposed.
- `T10-STATEMENTS.md`: T10.0 to T10.8 now, after T10-1.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before.

## What to read

- Every clause draft 8 changed (16).
- Every clause of the three answers' sets, once for each answer that names it.
- T10.0 and T10.8.

## What to report

For each answer in turn:
- **Faithfulness**, for each clause tagged with it: whether it states the answer as given, or adds to it, narrows it or
  alters it. Quoted words must be his.
- **Coherence**, for every clause of its set.

For each of your fifth re-read's OWED findings, say whether draft 8 (or `T10-STATEMENTS.md`) answers it as its
disposition records.

A clean report would show neither that CUT-0 is sound nor that the version-1 containment test passes; do not report
either as shown. Mark every probe unexecuted, and every fixture's outcome as your own worked consequence.

Number the findings (TEST-1, …; PIN-1, …; RO5-1, …; CHANGED-1, …; T10-…). Give each a class (DRAFTING, GAP,
COHERENCE, QUESTION), and say whether it needs his decision. Name any further source you need, without opening it.

Deliver the report as text in your reply.
