# Draft 4 to draft 5, clause by clause (2026-10-27)

**The two texts:**
- draft 4: `SPEC-15-DRAFT-4.md`, sha256 `f4225545ffe8766580194fdf2fbfcc2c96e3a6b9808b079788eecce48864a411`, unchanged;
- draft 5: `SPEC-15-DRAFT-5.md`, sha256 `3322571640426cafc10f445a9d606a6df4829c4151ac30fd3ba63d5ed3f53400`.

**What draft 5 does:** it states his ruling on finding 6 (`RULINGS.md`, "Finding 6: read-once ports") in the clauses it
decides. It decides nothing else: the byte forms, N2, N3, finding 8 and CUT-0's overall soundness stay open, as his
ruling says.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged. It pairs a changed
clause with the one at the same position, so 15.5's last bullets show as one CHANGED and one ADDED where two changed and
one was added.

## Each change, and the set it lies in

| change | what it states | set |
|---|---|---|
| the title; the status | the draft's name, and what it does | neither: they name the draft |
| the legend's `[ruled: F6]`, added | the ruling's tag | the legend |
| 15.3's read-once bullet | RO′-1 and RO′-2; N2 and N3 open for the A2 row | A_F6 |
| 15.5's record line | the read-once record present when declared and closed | A_F6 |
| 15.5, a bullet added | a well-formed log may lack the record; finding 8 owes its loadable form (condition 5) | A_F6 |
| 15.5's whole-log bullet | whole-log validation stays mandatory; the missing record is a distinct case (condition 1) | A_F6 |
| 15.7.1 | the binding place ruled (RO′-3); the run, its stop and a refusal before it (RO′-3, RO′-4) | A_F6 |
| 15.7.5 | the stop is a case of NOT-RUN or LOG-OPEN; COMPLETED never without the record (RO′-5) | A_F6 |
| the licence's presupposition | it holds by the ruling (`[follows]`); the first input's definition left to T9 | A_F6, A_PREFIX, A_LABELS, A_TABLE |
| 15.13.8 | the old NOT-RUN and LOG-OPEN row scoped; the read-once stop's row with its premises and withholding (RO′-6, condition 3) | A_F6 |
| 15.15 | the binding row replaced by N2 and N3 (A2) and finding 8's loadable form; the closing line | A_F6 |

**Built after the twin's re-read only.** Every change above is a clause the twin has not read in this text.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 5: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 5 states the owner's ruling of 2026-10-27 on finding 6, read-once ports …
   ADDED    - **[ruled: F6]** — fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′…
## 15.3
   CHANGED  - **Read-once ports.** **[ruled: F6]** A read-once value reaches the session only as an ar…
## 15.5
   CHANGED  - **The read-once record, when the law declares a read-once port and the record closed; th…
   CHANGED  - **A well-formed log may lack the read-once record:** an open log of the header alone, or…
   ADDED    - **The log is parsed whole before any execution starts.** A malformed log is refused at l…
## 15.7
   CHANGED  1. **The order.** **[ruled: R5]** A run executes the prefix, then one tick per tick record…
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.12
   CHANGED  **The licence as ruled.** **[ruled: PREFIX]** The licence is decided from the law's text a…
## 15.13
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
## 15.15
   CHANGED  | 15.3 and 15.7.1: an `end()` before the read-once record closes (N2); when the host runs …
   ADDED    | 15.5: a form that loads for a header-only open log and for a log ending in a read-once N…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 11, 'added': 3, 'removed': 0, 'unchanged': 144}
```
