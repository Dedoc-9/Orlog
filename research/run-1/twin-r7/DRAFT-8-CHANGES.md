# Draft 7 to draft 8, clause by clause (2026-10-27)

**The two texts:**
- draft 7: `SPEC-15-DRAFT-7.md`, sha256 `130480cafc0002377088da4de99c6cb11e5ded253efa20f900eaecf54a190a60`, unchanged, as the twin re-read it
  (re-read 5);
- draft 8: `SPEC-15-DRAFT-8.md`, sha256 `53d468213392da911d3b1fc5a50597b61b5c12bbb495c1368c0032f1f0e491c0`.

**What draft 8 does:** it applies the seven of re-read 5's eight OWED fixes that are in the draft
(`REREAD-5-DISPOSITION.md`; the eighth, T10-1, is in the theorem ledger) and states his answers on it (`RULINGS.md`,
"The containment test, findings 8 and 20 before the pin, and the push"): the check as a fixture test, findings 8 and
20 resolved before the pin, and RO′-5 confirmed. It decides nothing else. Finding 8's encoding, finding 20, the
fixtures, the pin's rules, N2, N3 and the amended set's 13 remaining rows stay open, as listed in 15.15.

**The comparison is computed, not remembered:** `clause_diff.py`. Its output is below, unchanged.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's `[ruled: claims]` | his answers that order the claims ruling's pin (V1CHECK-3, and Q2) |
| the legend's `[ruled: F6]` | his answer on Q1 and his confirmation of RO′-5 |
| 15.7.5 | CARRIER-1: his words, "an explicit receipt status that distinguishes", in place of the drafter's "of its own"; his confirmation: NOT-RUN or LOG-OPEN with an explicit distinguishing status form, never a fifth status word; CARRIER-3: a NOT-RUN at the stop names a read-once port (RO′-3) and carries a distinguishing form too; Q2: finding 8 resolved and recorded before the pin |
| 15.9's `'R'` bullet | Q2: whether `'R'` carries the cut, resolved and recorded before the pin |
| 15.12.5, 15.12.6, 15.13.11 | ORDER-3: 1a's rows run once CUT-0's digest is pinned (15.13.4) |
| 15.13.4 | ORDER-3: his omitted words quoted, and the order tagged with the claims ruling's pin; Q1: the version-1 reference runs the test before the pin, and no court row runs against an unpinned CUT-0; Q2: findings 8 and 20 before the pin, and a later change to the rule a new candidate with a new digest |
| 15.13.8 | CARRIER-2: the NOT-RUN/LOG-OPEN row and the stop's row chosen by the receipt's status; CONTAIN-1: the version-0 results stated (CUT-0's K̂ as RO′-6 states it, and containment), the equality holding by definition in version 1, containment owed, his grades quoted; Q1: the check a fixture test, MEASURED on its fixtures only, closing neither containment over every log nor T10.8 |
| 15.15: four rows and the closing line | Q2 on finding 8's row and 15.9's; Q1 on 15.13.8's; CHANGED-1 (the quoted words attributed to re-read 4) and CONTAIN-3 (his V1CHECK-2 words cited, the pin's wording still open) on 15.13.7's; the closing line names what draft 8 adds |

**Outside the draft,** in `ROUNDS.md`, each with a dated note: re-read 5's T10-1, the dated notes inside T10.0's and
T10.8's statements moved out into italic notes; and his answer on Q1 recorded in T10.8's notes. `T10-STATEMENTS-7.md`
holds the statements as they now read.

**The re-read.** His words: *"Draft 8 should incorporate the eight owed fixes and these decisions, record the affected
clauses, and undergo re-read 6."* The twin re-reads every clause draft 8 changes, the affected clauses of his answers
(`AR-REREAD-6.md`), and T10.0 and T10.8, before anything is built (R7, point 5). A drafting fix found then is recorded
with its re-read owed before the build; a question that needs his decision goes back to him.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 8: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 8 applies to draft 7 the fixes R7's fifth re-read recorded (`twin-r7/RER…
   CHANGED  - **[ruled: claims]** — fixed by the claims ruling: E2, and the meet; and by his answers t…
   CHANGED  - **[ruled: F6]** — fixed by his ruling on finding 6, read-once ports: A′, as RO′-1 to RO′…
## 15.7
   CHANGED  5. **The four outcomes.** **[open: amended set "identity and bytes", "four statuses"]** - …
## 15.9
   CHANGED  - **The `'R'` event would carry the refusal cut.** **[open: whether version 1's `'R'` payl…
## 15.12
   CHANGED  5. **A PREFIX claim that evaluated true** "remains historically held, regardless of whethe…
   CHANGED  6. **The rows and their controls.** "Every row testing an ungrounded port violation must r…
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
   CHANGED  11. **Until 1b, the court's reading of a version-1 run, read with the witness the arbiter …
## 15.15
   CHANGED  | 15.9: whether `'R'` carries the cut; its bytes (finding 20) | whether it carries the cut…
   CHANGED  | 15.5 and 15.7.5: a form that loads for a header-only open log and for a log ending in a …
   CHANGED  | 15.13.8: the version-1 containment test's fixtures, owed before the pin, its result MEAS…
   CHANGED  | 15.13.7: the continuation at a stop where no operation refused (in re-read 4's words, V1…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 16, 'added': 0, 'removed': 0, 'unchanged': 144}
```
