# Draft 5 to draft 6, clause by clause (2026-10-27)

**The two texts:**
- draft 5: `SPEC-15-DRAFT-5.md`, sha256 `3322571640426cafc10f445a9d606a6df4829c4151ac30fd3ba63d5ed3f53400`, unchanged, as
  the twin re-read it;
- draft 6: `SPEC-15-DRAFT-6.md`, sha256 `e9e3f442bbd51ec2e5ca7a9b45027ad3a5bb82d61581b95fde36e2cb26aa76cf`.

**What draft 6 does:** it applies the DRAFT dispositions of R7's third re-read (`REREAD-3-DISPOSITION.md`) and his
answers on the read-once stop's row and its version-1 check (`RULINGS.md`). It decides nothing else. What re-read 3
found open stays open, listed in §15.15: finding 8's forms and the stop's t, the record's events, N2, N3, the pin's
rules, and the stop's dependence on open clauses.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's `[ruled: PREFIX]` | PERFORM-1: it names the Perform row |
| the legend's `[ruled: F6]` | F6-12: "with six conditions"; and his answers |
| 15.1.6 | CHANGED-1: a claim standing later, or evaluated later, both unlicensed |
| 15.3's read-once bullet | F6-5: the record's events listed open, with N2 and N3 |
| 15.5's record line | F6-8: the record written whole, tagged F6 |
| 15.5's bullet on logs without the record | F6-7: the open log's form follows from RO′-3 and RO′-5; F6-9: which other logs are malformed is open |
| 15.5's whole-log bullet | F6-6: his words, "A malformed log is rejected before any statement executes" |
| 15.7.1 | F6-10: the check against the history is the verifier's, beside RO′-3's adopted words |
| 15.7.5 | F6-4: the read-once NOT-RUN's t is open |
| the rule table's tag | PERFORM-1 |
| 15.13.8's new row | his answer on F6-1: its own row, "the read-once stop", never "the rest of a block"; F6-2: its premises' dependence on open clauses; his answer on F6-14: MEASURED on version-0 stand-ins, DECLARED for version 1, a version-1 check owed before the pin |
| 15.13.8's closing line | F6-13: CUT-0's reach on the version-1 kinds in its other rows is the pin's, open |
| 15.13.9 | his answer on F6-1: the read-once stop named in the list of rows |
| 15.15: three rows changed, one added, the closing line | F6-11, F6-4, F6-5, F6-9, F6-13, F6-2; his answers |

**Outside the draft:** T10.7 is scoped and T10.8 added in `ROUNDS.md` (F6-3).

**The re-read.** His answer: the twin re-reads once the clauses draft 6 changes and the clauses his answers affect.
A drafting fix found then is applied and recorded with its re-read owed before the build.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 6: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 6 applies to draft 5 the drafting fixes of R7's third re-read (`twin-r7/…
   CHANGED  - **[ruled: PREFIX]** — fixed by his ruling on the PREFIX licence: B1 + 4a + 5c + K1, with…
   CHANGED  - **[ruled: F6]** — fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′…
## 15.1
   CHANGED  6. **A world property** (gravity, a constant of the scene) is proposed as a port read once…
## 15.3
   CHANGED  - **Read-once ports.** **[ruled: F6]** A read-once value reaches the session only as an ar…
## 15.5
   CHANGED  - **The read-once record, when the law declares a read-once port and the record was writte…
   CHANGED  - **A well-formed log may lack the read-once record:** an open log of the header alone, or…
   CHANGED  - **The log is parsed whole before any execution starts.** A malformed log is refused at l…
## 15.7
   CHANGED  1. **The order.** **[ruled: R5]** A run executes the prefix, then one tick per tick record…
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.12
   CHANGED  **The closure's rule table.** **[ruled: PREFIX, 2026-10-27; its Perform row, his answer of…
## 15.13
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
   CHANGED  What "may execute" reaches includes every procedure performed, transitively. It is CUT-0's…
   CHANGED  9. **Every withholding by CUT-0 names its row:** the open claim, the refused If's arms onw…
## 15.15
   CHANGED  | 15.3 and 15.4: the session, its record and the binding of the three records; the end rec…
   CHANGED  | 15.3 and 15.7.1: the events that fill and close the read-once record; an `end()` before …
   CHANGED  | 15.5 and 15.7.5: a form that loads for a header-only open log and for a log ending in a …
   ADDED    | 15.13.8: the read-once stop's version-1 check, owed before the pin; CUT-0's reach on the…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 19, 'added': 1, 'removed': 0, 'unchanged': 139}
```
