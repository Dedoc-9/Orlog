# Draft 12 to draft 13, clause by clause (2026-10-29)

**The two texts:**
- draft 12: `SPEC-15-DRAFT-12.md`, sha256 `772fda5264fd0c10c86aba95cd85e44669e4611761914700969b70fc4e86e750`, unchanged, as the twin re-read it
  whole (re-read 10);
- draft 13: `SPEC-15-DRAFT-13.md`, sha256 `60bc7cdfb292a28be7de98a11c3114cc68b72446d959712611a96e801e4edae6`.

**What draft 13 does:** it applies re-read 10's dispositions, adopted by him with his answer to its question
(`REREAD-10-DISPOSITION.md`; `RULINGS.md`, "Re-read 10's question"). It decides nothing else.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| 15.3: the `close()` row and a new bullet | his answer on S15.3-1: in a law with no tick block, `close()` is refused, runs no tick, emits no `t` record; the refusal's name is A2's, open |
| 15.5: the order of checks | S15.5-1: a `t` line in a law with no tick block is LOG-RECORD with the read-once placement, before D2.5's tick checks |
| 15.13.8 | S15.13-1: in a law with no tick block, a one-shot law's plain LOG-OPEN, K̂ is empty |
| 15.15 | S15.15-1: two rows moved into section order (shown by the comparison as removed and added); the closing line |

**Outside the draft,** each with a dated note: T10.7's statement in `ROUNDS.md` gains "in a law with no tick block, K̂
is empty" (S15.13-1); `CUT-SCHEMA.md`'s "does not show" notes that F20.4 rules S6 (S15.9-2). `T10-STATEMENTS-8.md`
holds T10.0 to T10.8 as they now read. S15.9-1 (the S1-S7 test's fixtures) is 1a's specification, as adopted.

**The re-read.** His words: *"For Draft 13, I agree that a targeted re-read of changed clauses and their affected
clauses is sufficient, provided the twin checks the cross-section consistency with the one-shot log and close rules."*

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 13: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 13 applies to draft 12 the dispositions of R7's tenth re-read (`twin-r7/…
## 15.3
   CHANGED  | `close()` | as above, in a law with a tick block | if every each-tick port is filled, th…
   ADDED    - **In a law with no tick block, `close()` is refused.** It runs no tick, emits no `t` rec…
## 15.5
   CHANGED  - **The order of checks.** The law compiles first; a compile fault means the log is never …
## 15.13
   CHANGED  8. **The cut** is the stack of statements executing at the refusal, outermost first. An ar…
## 15.15
   REMOVED  | 15.3: when the host runs the prefix of a law with no read-once port, and when a refusal …
   REMOVED  | 15.5: how a 1b runtime refuses a log, and its exit code | 1b's specification (RUNTIME-SP…
   ADDED    | 15.3: when the host runs the prefix of a law with no read-once port, and when a refusal …
   ADDED    | 15.5: how a 1b runtime refuses a log, and its exit code | 1b's specification (RUNTIME-SP…
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 6, 'added': 3, 'removed': 2, 'unchanged': 179}
```
