# Draft 2 to draft 3, clause by clause (2026-10-27)

**The two texts:**
- draft 2: `SPEC-15-DRAFT-2.md`, sha256 `43f6a725831308b9dc5b671d67b807e9366615310761fac6cf33710704ba66d5`, unchanged, as
  the twin re-read it;
- draft 3: `SPEC-15-DRAFT-3.md`, sha256 `59ec11c1b7f710f5e613b9865ac447257748f8aa1c5d5f9f1919443a29575f7c`.

**What draft 3 does:** it applies the DRAFT dispositions of R7's first re-read (`REREAD-1-DISPOSITION.md`) and states
the owner's three rulings of 2026-10-27 (`RULINGS.md`, "The labels' definitions, the closure's rule table, and R6's
control"). It decides nothing else. It states no fixture's outcome: his words, *"Do not mark PX-6 licensed merely
because the label was adopted."*

**The comparison is computed, not remembered:** `clause_diff.py`, as before. Its output is below, unchanged. It pairs a
changed clause with the one at the same position, so the table's rows show as ADDED and 15.12.5 and 15.12.6, which
changed, show among them.

## Each change, its reason, and the set it lies in

Sets: A_F24 and A_PREFIX are `AR-F24-PREFIX.md`'s, with their later dependencies; A_LABELS, A_TABLE and A_V0CTL are
`AR-REREAD-2.md`'s.

| change | reason | set |
|---|---|---|
| the title; the status paragraph | the draft's name, and what it does | neither: they name the draft |
| the legend's `[ruled: F24]` and `[ruled: PREFIX]` | they now cover the rulings of 2026-10-27; a label's definition is ruled, not its conclusions | A_F24, A_LABELS, A_TABLE, A_V0CTL |
| 15.0 Prefix | PREFIX-7: a gloss under a ruled tag, made a pointer | A_PREFIX, A_LABELS, A_TABLE |
| 15.1.3 | PREFIX-12: a read judged by evaluation would use the licence's closure | A_TABLE |
| 15.1.6 | PREFIX-12: which claims are later is the licence's; its tag names PREFIX | A_PREFIX, A_TABLE |
| 15.3's read-once bullet | PREFIX-12: the licence's presupposition, tagged | A_PREFIX, A_TABLE |
| 15.12.2 | F24-2: no claim of a version-1 run reads GROUNDED in a real reading before 1b | A_F24, A_PREFIX, A_LABELS |
| the licence as ruled | PREFIX-8 (D-18 in the adopted words), PREFIX-9 (his "particular execution" restored), PREFIX-10 (tagged [v0]), PREFIX-11 (exempt and licensed are one, by 5c's definition), PREFIX-5 (the first input, open with finding 6), and the labels ruling (the tick block's own rule, in his words) | A_PREFIX, A_LABELS, A_TABLE |
| the closure's rule table, and its three bullets, added | the rule-table ruling, two of its conditions in his words; no claim's licence stated | A_PREFIX, A_TABLE |
| 15.12.5 | F24-3 (its real reading), F24-4 (its tags split) | A_F24, A_PREFIX, A_LABELS, A_V0CTL |
| 15.12.6 | the control ruling, in his words | A_F24, A_PREFIX, A_LABELS, A_V0CTL |
| 15.13.1 | F24-2: the adopted sentence that E2 does not erase the backend-agreement requirement | A_F24 |
| 15.13.4 | F24-2: court R1 beside the meet | A_F24 |
| 15.13.8's closing line | PREFIX-1 and PREFIX-2: the line that altered the ruling removed; draft 1's text restored | A_PREFIX, A_LABELS, A_TABLE |
| 15.13.11 | F24-1 (the overclaim removed), F24-8 ("(1 to 4)" removed), F24-2, F24-10 (his scope sentence), F24-5 (REFERENCE-ONLY is the integrity column, [v0]), and the control ruling's interpretation, in his words | A_F24, A_PREFIX, A_LABELS, A_V0CTL |
| 15.14 | F24-11: the label of a configured result, left to this open row | A_F24 |
| 15.15: two rows added, one row widened, the closing line extended | F24-12 (D10's split), PREFIX-14 (finding 6's presupposition), F24-11 | A_PREFIX (the table's rows); all five (the closing line) |

**Outside the draft:** T10.5's statement is reworded in `ROUNDS.md` (T10.5-1 to -3), and the late dependencies are
recorded in `AR-F24-PREFIX.md`.

**Built after the twin's re-read only.** Every change above, the added table rows included, is a clause the twin has
not read in this text.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 3: version 1, the open run (2026-10-26; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 3 applies to draft 2 (`SPEC-15-DRAFT-2.md`, kept as the twin re-read it)…
   CHANGED  - **[ruled: F24]** — fixed by his ruling on finding 24 of R7's review: D10's court clause,…
   CHANGED  - **[ruled: PREFIX]** — fixed by his ruling on the PREFIX licence: B1 + 4a + 5c + K1, with…
## 15.0
   CHANGED  - **Prefix:** the top-level statements before the tick block. **Tick block:** the last top…
## 15.1
   CHANGED  3. **Places.** **[open: R2; amended set "port place"]** Ports are declared at the top leve…
   CHANGED  6. **A world property** (gravity, a constant of the scene) is proposed as a port read once…
## 15.3
   CHANGED  - **Read-once ports have no event in this table yet.** No event fills a read-once port, an…
## 15.12
   CHANGED  2. **No claim of such a run is GROUNDED, whatever its channel and whatever is ratified, ex…
   CHANGED  **The licence as ruled.** **[ruled: PREFIX]** The licence is decided from the law's text a…
   CHANGED  **The closure's rule table.** **[ruled: PREFIX, 2026-10-27]** The closure follows the sour…
   CHANGED  | statement kind | what the closure adds | |---|---|
   ADDED    | a claim | the claim itself |
   ADDED    | If, Unless, Otherwise | every arm, the Otherwise included |
   ADDED    | For, While | the body |
   ADDED    | the tick block | its body |
   ADDED    | Perform | the procedure's body, transitively |
   ADDED    | To, Define, Decimals | no further reachable body |
   ADDED    | Let, Set, Increase, Decrease, Say, Append, Remove, Must, a port declaration | no further…
   ADDED    | any other kind | no claim of the law is licensed |
   ADDED    - "This does not exempt their surrounding clauses from the boundary or licensing test." - …
   ADDED    5. **A PREFIX claim that evaluated true** "remains historically held, regardless of whethe…
   ADDED    6. **The rows and their controls.** "Every row testing an ungrounded port violation must r…
## 15.13
   CHANGED  1. **HELD means E2:** every completed evaluation of the claim was true, no evaluation of t…
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
   CHANGED  What "may execute" reaches includes every procedure performed, transitively.
   CHANGED  11. **Until 1b, the court's reading of a version-1 run, read with the witness the arbiter …
## 15.14
   CHANGED  **[open: amended set "reporting"]** Every authoritative report names its claim, the eviden…
## 15.15
   CHANGED  | 15.12.4 and 15.7.1: where a read-once value binds, which the licence presupposes is not …
   CHANGED  | 15.13.11: D10's two-commit split | D10 |
   ADDED    | 15.14: the authority rule; the label of a configured result | the amended set's "reporti…
   ADDED    Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 19, 'added': 13, 'removed': 0, 'unchanged': 122}
```
