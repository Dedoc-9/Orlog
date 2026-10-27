# Re-read 3: the disposition of the twin's 17 findings (2026-10-27)

The twin's report is `REREAD-3-REPORT.md`, saved unchanged. Its summary says 22 findings, but its table and its lists
hold 17: 14 on finding 6, 1 on the Perform row, 2 on draft 4's changes, none on T10.5. This disposition takes the 17.
Each is disposed by the draft's author; nothing here is ruled.

His release ruling governs how they are handled: *"If an unresolved question changes version-1 behavior or makes the
candidate's specification internally inconsistent, stop and bring that question back rather than hiding it inside the
narrow scope."* And: *"Keep N2, N3, the read-once `NOT-RUN` byte form, and other explicitly open questions from being
silently treated as settled."*

Classes: **DRAFT** (fixed in draft 6), **ASK** (put to the owner), **LEDGER** (`ROUNDS.md`), **OPEN** (left open and
listed in §15.15, so it is not silently settled), **NOTED** (no change).

## Checked against the files first

- **F6-1.** CHECKED: draft 5's 15.13.9 lists the rows a withholding may name, and the new row is not among them, while
  the new row reports its withholdings as "the rest of a block". The claims ruling requires each withholding to name
  its structural row, and his condition 3 says not to assume that row covers the stop without checking. That is a
  question about what version 1 reports, so it goes to him.
- **F6-3.** CHECKED: T10.7's statement in `ROUNDS.md` still reads "At NOT-RUN t or LOG-OPEN, the cut is the tick
  block's head before tick t", unscoped, against draft 5's scoped row.
- **CHANGED-2.** CHECKED: packet B names its bullet 1 in its own §4, "(a) is bullet 1 word for word"
  (`packets/B-PREFIX.md`).

## The dispositions

| # | disposition | what is done |
|---|---|---|
| F6-1 | ASK | the stop's row: its own row, named in 15.13.9, or the rest-of-block row applied to a frame not begun |
| F6-2 | DRAFT | the new row's premises name the open clauses they rest on: 15.1.3's top-level place and 15.7.1's counting; 15.15 lists the dependence |
| F6-3 | LEDGER | T10.7 scoped to logs that hold the read-once record or laws with no read-once port; a new obligation, T10.8, for the stop's row, DECLARED and open |
| F6-4 | DRAFT, OPEN | 15.7.5's NOT-RUN line says the read-once stop's t is open; 15.15 lists it under finding 8 and "identity and bytes" |
| F6-5 | DRAFT, OPEN | 15.3 says the session events that fill and close the read-once record are open, with N2 and N3; 15.15 lists them under A2 |
| F6-6 | DRAFT | 15.5's whole-log bullet in his words: "A malformed log is rejected before any statement executes" |
| F6-7 | DRAFT | the header-only open log's loadable form retagged `[follows: F6 (RO′-3, RO′-5)]`; condition 5 tags the read-once NOT-RUN log only |
| F6-8 | DRAFT | 15.5's record line: the record "written" (closed with every read-once port filled), tagged F6 |
| F6-9 | OPEN | which other logs lacking the record are malformed is finding 8's; listed in 15.15, not decided here |
| F6-10 | DRAFT | 15.7.1: the named port is checked against the history by the verifier (15.4), not by the execution |
| F6-11 | DRAFT | 15.15's A2 row: finding 6 and the binding place are ruled; N2, N3 and the record's events stay |
| F6-12 | DRAFT | the legend's `[ruled: F6]` adds "with six conditions" |
| F6-13 | OPEN | CUT-0's own reach on the version-1 kinds in its ordinary rows (a later tick block's body; nothing for a port declaration) is the pin's; listed in 15.15 |
| F6-14 | ASK | whether the version-0 stand-in check is enough for now, with a version-1 check owed before the pin |
| PERFORM-1 | DRAFT | the legend's `[ruled: PREFIX]` and the table's tag name the Perform row |
| CHANGED-1 | DRAFT | 15.1.6's `[follows]` sentence cites both (a) and (b): a claim standing after the boundary, or one a clause from the boundary on may execute |
| CHANGED-2 | NOTED | checked above |

**Totals:** 11 DRAFT (F6-4 and F6-5 also listed open), 2 ASK, 1 LEDGER, 2 OPEN, 1 NOTED: 17, each disposed once.

## What follows

Draft 6 applies the DRAFT dispositions and his answers to F6-1 and F6-14. Its changed clauses are not built before the
twin reads them.
