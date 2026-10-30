# R7's eleventh re-read: the brief to the twin (2026-10-29)

Since your tenth re-read, the owner has adopted its dispositions and answered its question (`RULINGS-AS-RULED.md`, its
last section): in a law with no tick block, `close()` is refused; it runs no tick, emits no `t` record, and never makes
a log its own loader refuses. Draft 13 applies that and your four drafting fixes.

**This re-read is targeted, with one condition.** His words: *"For Draft 13, I agree that a targeted re-read of changed
clauses and their affected clauses is sufficient, provided the twin checks the cross-section consistency with the
one-shot log and close rules."*

## Your reading set

These files, in this folder. Open nothing else, and list every file you open, saying which you read whole.

- `SPEC-15-DRAFT-13.md`: the draft.
- `RULINGS-AS-RULED.md`: its last section holds his answer.
- `AR-REREAD-11.md`: the answer's affected clauses, computed over draft 12 (77 clauses).
- `DRAFT-13-CHANGES.md`: what draft 13 changed, and why.
- `REREAD-10-DISPOSITION.md`: your tenth re-read's findings, proposed and adopted.
- `T10-STATEMENTS.md`: T10.0 to T10.8 now; T10.7 gains the law with no tick block.
- `CUT-SCHEMA.md`, `SPEC.md` and `RUNTIME-SPEC.md`, as before (CUT-SCHEMA's "does not show" carries a new dated note).

## What to read

- Every clause draft 13 changed or added.
- Every clause of `AR-REREAD-11.md`'s set.
- **The cross-section check he requires:** every clause, in any section, that bears on a law with read-once ports and
  no tick block, or on `close()`: at least 15.0 (Prefix, Tick block), 15.1.3 (PP3), 15.3 (the session table and its
  bullets, N2, N3, finding 10), 15.4, 15.5 (the record-less logs, the one-shot rule, the table, the order of checks),
  15.7.1 and 15.7.5, 15.12 (the boundary for a one-shot law), 15.13.8 and T10.7, and 15.15. Say whether they agree:
  that a one-shot session can produce only logs its loader accepts, and that the loader, the statuses and CUT-0's rows
  treat those logs alike.

## What to report

- **Faithfulness** for every clause tagged with his answer; **coherence** for every clause you read.
- For each of your tenth re-read's findings, whether draft 13 answers it as its adopted disposition records.
- The result of the cross-section check, clause by clause.

A clean report would show neither that CUT-0 is sound nor that the containment test passes; do not report either as
shown. Mark every probe unexecuted, and every fixture's outcome as your own worked consequence.

Number the findings by section (S15.3-1, …). Give each a class (DRAFTING, GAP, COHERENCE, QUESTION), and say whether
it needs his decision. Name any further source you need, without opening it.

Deliver the report as text in your reply.
