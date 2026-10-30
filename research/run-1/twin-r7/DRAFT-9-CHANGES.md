# Draft 8 to draft 9, clause by clause (2026-10-27)

**The two texts:**
- draft 8: `SPEC-15-DRAFT-8.md`, sha256 `53d468213392da911d3b1fc5a50597b61b5c12bbb495c1368c0032f1f0e491c0`, unchanged, as the twin re-read it
  (re-read 6);
- draft 9: `SPEC-15-DRAFT-9.md`, sha256 `8a1ccf5ce22895d0106884b1208603315c80704f781adb87c3b2e520289d0e8e`.

**What draft 9 does:** it applies re-read 6's seven OWED fixes (`REREAD-6-DISPOSITION.md`) and states his answer on it
(`RULINGS.md`, "Every input the pinned rule reads, fixed before the pin"). It decides nothing else. His answer orders
the open rows before the pin and settles none of them: the port place, counting, finding 8's form and encoding, finding
20, the cut's decoding, the fixtures, P6, N2, N3 and the amended set's other rows stay open, as listed in 15.15.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's `[ruled: claims]` | his answer that every input the pinned rule reads is fixed before the pin |
| 15.1.3 | his answer: the stop's row reads the place, so the amended set's "port place" is resolved before the pin |
| 15.7.1 | his answer: the stop's row reads counting, so the amended set's "counting" is resolved before the pin |
| 15.7.5 | RO5-1: the stop's status named one way, his confirmation's "explicit distinguishing status form", with his STOPROW-1 words for what it does; his answer: finding 8 settles the form and its encoding before the pin |
| 15.9's `'R'` bullet | his answer: if `'R'` carries the cut, whether and how the pinned rule decodes it is specified before the pin, in his words that the court must not silently derive it from execution; P6 keeps its own trigger |
| 15.13.4 | PIN-4 and his answer: the order in his words, the inputs listed; TEST-3: the test's record names the candidate's digest, and the pin pins that digest; his words on a later change |
| 15.13.8 | his answer: the premises (place and counting) resolved before the pin; CHANGED-1: the version-0 account tagged `[follows]`, only the grades his; TEST-1: the property over every log, the test sampling it; TEST-2 and TEST-3: the fixtures fixed and recorded before the test, the test run against the candidate the inputs give |
| 15.15: five rows and the closing line | his answer on the rows for 15.1.3, 15.7.1 to 15.7.3, 15.9 and 15.13.8; PIN-2: finding 8's part of the "15.5 and 15.6" row before the pin; TEST-2: the fixtures decided by 1a's specification, not by the pin; the closing line names what draft 9 adds |

**Outside the draft:** nothing. Re-read 6's T10-1 needed no change (`REREAD-6-DISPOSITION.md`), and T10.0 to T10.8 read
as they did for re-read 6.

**The re-read.** The twin re-reads every clause draft 9 changes and the affected clauses of his answer
(`AR-REREAD-7.md`), before anything is built (R7, point 5). A drafting fix found then is recorded with its re-read owed
before the build; a question that needs his decision goes back to him.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 9: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 9 applies to draft 8 the fixes R7's sixth re-read recorded (`twin-r7/RER…
   CHANGED  - **[ruled: claims]** — fixed by the claims ruling: E2, and the meet; and by his answers t…
## 15.1
   CHANGED  3. **Places.** **[open: R2; amended set "port place"]** Ports are declared at the top leve…
## 15.7
   CHANGED  1. **The order.** **[ruled: R5]** A run executes the prefix, then one tick per tick record…
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.9
   CHANGED  - **The `'R'` event would carry the refusal cut.** **[open: whether version 1's `'R'` payl…
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
## 15.15
   CHANGED  | 15.1.3: a read outside the tick block, textual or by evaluation; the codes and phases; a…
   CHANGED  | 15.5 and 15.6: the log's bytes, the read-once record, the LOG-* conditions and order, a …
   CHANGED  | 15.7.1, 15.7.2 and 15.7.3: what binding counts; counting; the budget; `at most 0`; the c…
   CHANGED  | 15.9: whether `'R'` carries the cut; its bytes (finding 20) | whether it carries the cut…
   CHANGED  | 15.13.8: the version-1 containment test's fixtures, fixed and recorded before the test r…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 15, 'added': 0, 'removed': 0, 'unchanged': 145}
```
