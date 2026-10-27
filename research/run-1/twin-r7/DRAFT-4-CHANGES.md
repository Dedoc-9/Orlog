# Draft 3 to draft 4, clause by clause (2026-10-27)

**The two texts:**
- draft 3: `SPEC-15-DRAFT-3.md`, sha256 `59ec11c1b7f710f5e613b9865ac447257748f8aa1c5d5f9f1919443a29575f7c`, unchanged, as
  the twin re-read it;
- draft 4: `SPEC-15-DRAFT-4.md`, sha256 `f4225545ffe8766580194fdf2fbfcc2c96e3a6b9808b079788eecce48864a411`.

**What draft 4 does:** it applies the DRAFT dispositions of R7's second re-read (`REREAD-2-DISPOSITION.md`) and his
answer on the closure table's Perform row (`RULINGS.md`, 2026-10-27). It decides nothing else, and it states no
fixture's outcome.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change, its reason, and the set it lies in

Sets: A_F24 and A_PREFIX (`AR-F24-PREFIX.md`, with their later dependencies); A_LABELS, A_TABLE, A_V0CTL and A_PERFORM
(`AR-REREAD-2.md`).

| change | reason | set |
|---|---|---|
| the title (now dated 2026-10-27); the status | CHANGED-1; the draft's name | neither: they name the draft |
| the legend's `[ruled: F24]` | LABELS-3: it names the labels ruling's adoption of D | A_F24, A_LABELS, A_V0CTL |
| the legend's `[follows: X]`, added | LABELS-6: a statement drawn from rules is not ruled itself | the legend (A_F24) |
| 15.1.1 | TABLE-5, LATE-1: a form R2 adds needs a row of the table | A_PREFIX (late), A_TABLE |
| 15.1.3 | TABLE-4: the closure's rules, started from the clauses other than the tick block | A_TABLE |
| 15.1.6 | LABELS-6: corrected and tagged `[follows]` | A_PREFIX, A_TABLE, A_PERFORM |
| 15.3's read-once bullet | CHANGED-2: the presupposition is 15.12.4's and open, not ruled | A_PREFIX, A_TABLE, A_PERFORM |
| 15.12.2 | LABELS-6: its consequence tagged `[follows]` | A_F24, A_PREFIX, A_LABELS |
| the licence as ruled | LABELS-1 (K1's start set, in its adopted words), LABELS-4 (B1's label and wording), LABELS-5 (the adopted words), LABELS-2 (bullet 1 named; the identity's dependence on 15.1.3; `[follows]`) | A_PREFIX, A_LABELS, A_TABLE, A_PERFORM |
| the table's Perform row | his answer: SPEC §3's row, the bare name included | A_TABLE, A_PERFORM |
| 15.12.6 | V0CTL-1 (his decision line), V0CTL-2 (what removing the declaration changes; open for 1a's specification) | A_F24, A_PREFIX, A_LABELS, A_V0CTL |
| 15.13.4 | CHANGED-3: his words, "alongside E2" | A_F24 |
| 15.13.8's closing line | TABLE-3, LATE-2: K̂'s reach is CUT-0's own, for the pin; not said to be the table | A_PREFIX, A_LABELS, A_TABLE |
| 15.13.11 | V0CTL-3 (the measured control excluded), LATE-3 (completed evaluations' reading) | A_F24, A_PREFIX, A_LABELS, A_V0CTL |
| 15.14 | V0CTL-4: the measured control's label | A_F24 |
| 15.15: a row and the closing line | V0CTL-4; his answer | all (the closing line) |

**Outside the draft:** T10.5's statement in `ROUNDS.md` gains "nested ones included" (T10.5-4).

**Built after the twin's re-read only.** Every change above is a clause the twin has not read in this text. That read
is proposed to go with finding 6's re-read (`REREAD-2-DISPOSITION.md`, "What follows").

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 4: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 4 applies to draft 3 (`SPEC-15-DRAFT-3.md`, kept as the twin re-read it)…
   CHANGED  - **[ruled: F24]** — fixed by his ruling on finding 24 of R7's review: D10's court clause,…
   ADDED    - **[follows: X]** — not ruled itself: a statement drawn from the rulings and clauses X na…
## 15.1
   CHANGED  1. **Spellings.** **[open: R2]** A form R2 adds is a statement kind, which needs a row of …
   CHANGED  3. **Places.** **[open: R2; amended set "port place"]** Ports are declared at the top leve…
   CHANGED  6. **A world property** (gravity, a constant of the scene) is proposed as a port read once…
## 15.3
   CHANGED  - **Read-once ports have no event in this table yet.** No event fills a read-once port, an…
## 15.12
   CHANGED  2. **No claim of such a run is GROUNDED, whatever its channel and whatever is ratified, ex…
   CHANGED  **The licence as ruled.** **[ruled: PREFIX]** The licence is decided from the law's text a…
   CHANGED  | Perform, written `Perform <name>` or the name alone (SPEC §3) | the procedure's body, tr…
   CHANGED  6. **The rows and their controls.** "Every row testing an ungrounded port violation must r…
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  What "may execute" reaches includes every procedure performed, transitively. It is CUT-0's…
   CHANGED  11. **Until 1b, the court's reading of a version-1 run, read with the witness the arbiter …
## 15.14
   CHANGED  **[open: amended set "reporting"]** Every authoritative report names its claim, the eviden…
## 15.15
   CHANGED  | 15.14: the authority rule; the labels of a configured result and of the measured control…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 17, 'added': 1, 'removed': 0, 'unchanged': 137}
```
