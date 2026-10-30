# Draft 6 to draft 7, clause by clause (2026-10-27)

**The two texts:**
- draft 6: `SPEC-15-DRAFT-6.md`, sha256 `e9e3f442bbd51ec2e5ca7a9b45027ad3a5bb82d61581b95fde36e2cb26aa76cf`, unchanged, the draft of the
  release pushed as 9de2792 (tree `7a766f5e632564b06841ba5b8bf52c9ed6b7ee02`);
- draft 7: `SPEC-15-DRAFT-7.md`, sha256 `130480cafc0002377088da4de99c6cb11e5ded253efa20f900eaecf54a190a60`.

**What draft 7 does:** it applies the six OWED fixes of R7's fourth re-read (`REREAD-4-DISPOSITION.md`), lists its one
OPEN item in 15.15, and states his three answers on it (`RULINGS.md`, "The stop's carrier, the owed check, and the
order of work"). It decides nothing else. The receipt status's bytes and encoding stay finding 8's; N2, N3, the
read-once NOT-RUN's t, the pin's rules and the 13 deferred rows of the amended set stay open, as listed in 15.15.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's `[ruled: F6]` | his three answers named among the ruling's parts |
| 15.7.5 | his answer on STOPROW-1: the stop has an explicit receipt status of its own; its bytes and encoding open under finding 8 |
| 15.13.4 | his answer on V1CHECK-3: the containment check, then the pin of CUT-0's digest, then 1a; nothing of 1a against an unpinned CUT-0 |
| 15.13.8's new row | STOPROW-2: it cites T10.8; his answer on STOPROW-1: the row chosen from the receipt's status, never from the log or the trace; V1CHECK-1: his "It does not close the format-freeze question or authorize pinning before the check.", tagged F6; his answer on V1CHECK-2: the owed check is containment, without precision, an obligation and not a result |
| 15.13.10 | T10-1: "T10.0 to T10.8" |
| 15.15: three rows changed, one added, the closing line | CHANGED-1: finding 6 off the "15.5 and 15.6" row; STOPROW-1: the receipt status's bytes and encoding on finding 8's row; V1CHECK-2: "containment check"; V1CHECK-4 (OPEN): 15.13.7's continuation at a stop where no operation refused, the pin's wording; the closing line names what draft 7 adds |

**Outside the draft,** in `ROUNDS.md`, each with a dated note: T10-1, T10.0 names T10.8; T10-2, T10.8's statement
scoped to NOT-RUN or LOG-OPEN with the read-once record absent, never RO′-4's refusal before the first read-once
declaration; T10-3, T10.7's scope moved from its note into its statement. `T10-STATEMENTS-6.md` holds the statements
as they now read.

**The re-read.** Re-read 4's disposition: the twin re-reads every clause draft 7 changes and the affected clauses of
his answers (`AR-REREAD-5.md`), before anything is built (R7, point 5). 15.13.10 enters D_r by T10-1; it is also among
the clauses draft 7 changes. A drafting fix found then is applied and recorded with its re-read owed before the build;
a question that needs his decision goes back to him.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 7: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 7 applies to draft 6 the six fixes R7's fourth re-read recorded (`twin-r…
   CHANGED  - **[ruled: F6]** — fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′…
## 15.7
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
   CHANGED  10. **What stays open.** **[ruled: claims]** - No proof obligation is closed by this secti…
## 15.15
   CHANGED  | 15.5 and 15.6: the log's bytes, the read-once record, the LOG-* conditions and order, a …
   CHANGED  | 15.5 and 15.7.5: a form that loads for a header-only open log and for a log ending in a …
   CHANGED  | 15.13.8: the read-once stop's version-1 containment check, owed before the pin; CUT-0's …
   ADDED    | 15.13.7: the continuation at a stop where no operation refused ("had the missing input a…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 11, 'added': 1, 'removed': 0, 'unchanged': 148}
```
