# Draft 1 to draft 2, clause by clause (2026-10-26)

**The two texts:**
- draft 1: `SPEC-15-DRAFT-1.md`, sha256 `367b1b4866e795d44141a87ef23579237fe414cf1fe61817fd47df135bd99d47`, unchanged;
- draft 2: `SPEC-15-DRAFT-2.md`, sha256 `43f6a725831308b9dc5b671d67b807e9366615310761fac6cf33710704ba66d5`.

**What draft 2 does:** it states the owner's two rulings of 2026-10-26 in the clauses they decide (`RULINGS.md`,
"Finding 24 and the PREFIX licence"). It applies none of draft 1's errata (`packets/INTEGRATION.md` §4), except the tag
on 15.7.1's binding place, which the PREFIX licence presupposes. It decides nothing else.

**The comparison is computed, not remembered:** `clause_diff.py`, as for draft 1. Its output is below, unchanged.

## Each change, and the set it lies in

The clause numbers in brackets are the rows of `AR-F24-PREFIX.md`, which name draft 1's clauses.

| change | what it states | set |
|---|---|---|
| the title; the status paragraph | the draft's name, and what it does | neither: they name the draft |
| the legend: `[ruled: F24]` and `[ruled: PREFIX]` added | the two rulings' tags | A_F24 (the legend, rows 4–8) |
| 15.0 Prefix | the prefix is not the PREFIX licence | A_PREFIX (13) |
| 15.0 Boundary, added | the boundary, as ruled | A_PREFIX (15.0, rows 11–16) |
| 15.7.1 | its binding place tagged open (finding 6), R5 holding only "before the first `'T'`"; the licence presupposes it | A_PREFIX (60) |
| 15.12.4's note | the open proposal replaced by the licence as ruled, its conditions 2 and 3 in his words | A_PREFIX (105) |
| 15.12.5 | in 1a its row runs with the agreed witness configured | both (106) |
| 15.12.6 | his condition 1 in his words; in 1a the rows run configured, and are no evidence of the reference's arithmetic | both (107) |
| 15.13.8's closing line | the PREFIX licence shares the reachability, which fails closed | A_PREFIX (116) |
| 15.13.11 | D10's court clause as ruled; court R1 beside E2 in his words; condition 1; the split left open | both (119) |
| 15.15: two rows removed, one line added | 15.12.4 and 15.13.11 leave the open table; the line says they are ruled | A_PREFIX (136); both (138) |

**Built after the twin's re-read only.** Every clause above, the two added clauses and the line added in 15.15
included, is a clause the twin has not read in this text. Under R7 none is built before it is read.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 2: version 1, the open run (2026-10-26; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 2 states the owner's two rulings of 2026-10-26 on R7's review in the cla…
   ADDED    - **[ruled: F24]** — fixed by his ruling on finding 24 of R7's review: D10's court clause,…
   ADDED    - **[ruled: PREFIX]** — fixed by his ruling on the PREFIX licence: B1 + 4a + 5c + K1, with…
## 15.0
   CHANGED  - **Prefix:** the top-level statements before the tick block. **Tick block:** the last top…
   ADDED    - **Boundary:** the first top-level clause, in the text, that is or holds a port declarati…
## 15.7
   CHANGED  1. **The order.** **[ruled: R5]** A run executes the prefix, then one tick per tick record…
## 15.12
   CHANGED  **The licence as ruled.** **[ruled: PREFIX]** The licence is decided from the law's text a…
   CHANGED  5. **A PREFIX claim that evaluated true** "remains historically held, regardless of whethe…
   CHANGED  6. **The rows and their controls.** "Every row testing an ungrounded port violation must r…
## 15.13
   CHANGED  What "may execute" reaches includes every procedure performed, transitively. The PREFIX li…
   CHANGED  11. **Until 1b, the court's reading of a version-1 run, read with the witness the arbiter …
## 15.15
   REMOVED  | 15.12.4: PREFIX by static closure; a law with no port; sufficiency (findings 3, 4, 5) | …
   REMOVED  | 15.13.11: REFERENCE-ONLY until 1b, against R6 (finding 24) | D10 |
   ADDED    Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 9, 'added': 4, 'removed': 2, 'unchanged': 128}
```
