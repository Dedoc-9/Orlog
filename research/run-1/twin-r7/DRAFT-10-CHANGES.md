# Draft 9 to draft 10, clause by clause (2026-10-27)

**The two texts:**
- draft 9: `SPEC-15-DRAFT-9.md`, sha256 `8a1ccf5ce22895d0106884b1208603315c80704f781adb87c3b2e520289d0e8e`, unchanged, as the twin re-read it
  (re-read 7);
- draft 10: `SPEC-15-DRAFT-10.md`, sha256 `c69e7e3b02542a5cb6b320de1c5994786f2425d04bbfdb1c7e45ce1741098eb7`.

**What draft 10 does:** it applies re-read 7's four OWED fixes, corrects 15.13.4's naming of the inputs
(`REREAD-7-DISPOSITION.md`), and states his clarification on it (`RULINGS.md`, "The principle reaches every row of
CUT-0"). It decides nothing else. The clarification settles none of the rows it names: the version-1 status encoding,
R2's spellings and reach rules, the port place, counting, findings 8 and 20, the cut's decoding, the fixtures, P6, N2
and N3 stay open, as listed in 15.15.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's `[ruled: claims]` | his clarification: every input, in every row of CUT-0 |
| 15.1.1 | his clarification: R2's statement-kind spellings and reach rules resolved before the pin |
| 15.7.5 | CHANGED-2: the stop's NOT-RUN t is finding 8's, before the pin; his clarification: the NOT-RUN and LOG-OPEN status encoding fixed before the pin |
| 15.9's `'R'` bullet | INPUTS-1: if the cut is in `'R'`, the tick block's and the ports' frames derived before the pin, tagged `[follows]` |
| 15.13.4 | INPUTS-2: the stop row's inputs named as his list, beside the other rows' inputs and R2; INPUTS-3: his words that the ordering settles no open row; CHANGED-1: the record's naming of the digest tagged `[follows]`; his clarification: the record enumerates the inputs the candidate reads, checked against it |
| 15.13.8 | CHANGED-1 and his clarification, as in 15.13.4 |
| 15.15: three rows and the closing line | his clarification on the rows for 15.0 and 15.1 (R2) and for 15.7.5 and 15.8 (the status encoding); INPUTS-1 on 15.9's; the closing line names what draft 10 adds |

**Outside the draft:** nothing.

**The re-read.** The twin re-reads every clause draft 10 changes and the affected clauses of his clarification
(`AR-REREAD-8.md`), before anything is built (R7, point 5). A drafting fix found then is recorded with its re-read owed
before the build; a question that needs his decision goes back to him.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 10: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 10 applies to draft 9 the fixes R7's seventh re-read recorded (`twin-r7/…
   CHANGED  - **[ruled: claims]** — fixed by the claims ruling: E2, and the meet; and by his answers t…
## 15.1
   CHANGED  1. **Spellings.** **[open: R2]** A form R2 adds is a statement kind, which needs a row of …
## 15.7
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.9
   CHANGED  - **The `'R'` event would carry the refusal cut.** **[open: whether version 1's `'R'` payl…
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
## 15.15
   CHANGED  | 15.0 and 15.1: spellings, places, float ports | R2, before the pin (his clarification); …
   CHANGED  | 15.7.5 and 15.8: the four statuses; `tick-ops`, including when no tick began; the unread…
   CHANGED  | 15.9: whether `'R'` carries the cut; its bytes (finding 20) | whether it carries the cut…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 12, 'added': 0, 'removed': 0, 'unchanged': 148}
```
