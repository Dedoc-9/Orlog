# Draft 11 to draft 12, clause by clause (2026-10-29)

**The two texts:**
- draft 11: `SPEC-15-DRAFT-11.md`, sha256 `937499a6daa87ebeb483cb535d1dba2f20eecb4d3518b83d2598991db96524f5`, unchanged, as the twin re-read it
  whole (re-read 9);
- draft 12: `SPEC-15-DRAFT-12.md`, sha256 `772fda5264fd0c10c86aba95cd85e44669e4611761914700969b70fc4e86e750`.

**What draft 12 does:** it applies re-read 9's dispositions, adopted by him with his answers to its five questions
(`REREAD-9-DISPOSITION.md`; `RULINGS.md`, "Re-read 9's five questions"). It decides nothing else.

## Each change and its reason

| change | reason |
|---|---|
| the title; the status | the draft's name, and what it does |
| the legend's [open: X] | S15.0-1: R2 and R9 are ruled |
| 15.0 Prefix | S15.0-1: a law with no tick block (PP3) |
| 15.1.4 | S15.1-1: with no budget the law line omits its budget part (R5); S15.1-2: the line's `<type>` spelling open |
| 15.3 | S15.3-1: each read-once `'N'` at its own declaration, never grouped; S15.3-2: the prefix of a law with no read-once port, open |
| 15.5 | S15.5-1: the fixed example corrected to `580000000300000000`; S15.5-2: no tick records in a law with no tick block, LOG-RECORD, and its table row; S15.5-3: the command line exits 1, the 1b runtime's exit code open; S15.5-4: the header-only status conditioned on the run; S15.5-5: `t 0` at line 4 in a read-once law is M1 |
| 15.7.3 | S15.1-1: B2's sentence restated to R5's form |
| 15.9 | S15.9-1: draft 2 the candidate byte grammar, tested by the version-1 reference during the containment step before the pin, not frozen; S15.9-2: a run that does not refuse emits no `'R'` |
| 15.13.4 | S15.13-1: of the pin's inputs, all ruled but the cut's byte grammar |
| 15.15 | S15.15-1: rows for the law line's `<type>`, the prefix of a law with no read-once port, the 1b runtime's exit code; the byte grammar's row split from the format freeze's; the closing line |

**Outside the draft:** `CUT-SCHEMA.md`'s S6 row gains a dated note that F20.4 rules it (S15.9-2).

**The re-read.** He recommends a whole-draft re-read: *"I recommend another whole-draft re-read because Draft 12
changes settled semantics and the byte grammar, not merely editorial wording."* `AR-REREAD-10.md` records the affected
clauses; the twin reads every clause.

## The comparison's output

```
## preamble
   CHANGED  # SPEC §15, draft 12: version 1, the open run (2026-10-27; research, not yet in SPEC.md)
   CHANGED  **Status.** Draft 12 applies to draft 11 the dispositions of R7's ninth re-read (`twin-r7/…
   CHANGED  - **[open: X]** — not ruled. The clause gives the current proposal, and X names what decid…
## 15.0
   CHANGED  - **Prefix:** the top-level statements before the tick block, or all of them in a law with…
## 15.1
   CHANGED  4. **The law's lines.** `(port <var> "<name>" <type> each-tick|once)` and `(tick <clause>[…
## 15.3
   CHANGED  - **Read-once ports.** **[ruled: F6]** A read-once value reaches the session only as an ar…
## 15.5
   CHANGED  - **Values,** in both, are tagged: each is its full RUNTIME-SPEC §5 encoding, tag included…
   ADDED    - **A law with read-once ports and no tick block** has no tick records: a `t` line is refu…
   CHANGED  - **A well-formed log may lack the read-once record.** For a law that declares a read-once…
   CHANGED  | a tick record in a law with no tick block (his answer on S15.5-2) | LOG-RECORD |
   ADDED    | a tick number not canonical, or not one more than the ticks before it (so `t 0` too, exc…
   CHANGED  - **A load refusal writes no receipt** (D3.1). Only the nine codes count as load refusals;…
## 15.7
   CHANGED  3. **The budget.** **[ruled: R9, B1 to B4]** - The optional budget is part of the law, und…
## 15.9
   CHANGED  - **The `'R'` event carries the refusal cut** in version 1. The trace head commits it, and…
   ADDED    - **A run that does not refuse emits no `'R'`:** COMPLETED, a tick's NOT-RUN and LOG-OPEN,…
## 15.13
   CHANGED  4. **The settlement is the meet: a claim is held only when the court's R8 holds it and CUT…
## 15.15
   ADDED    | 15.1.4: the law line's `<type>` spelling | the amended set's "identity and bytes" |
   ADDED    | 15.3: when the host runs the prefix of a law with no read-once port, and when a refusal …
   ADDED    | 15.5: how a 1b runtime refuses a log, and its exit code | 1b's specification (RUNTIME-SP…
   CHANGED  | 15.9: the cut's byte grammar, draft 2 the candidate, MEASURED on version-0 stand-ins onl…
   ADDED    | 15.9: the general format freeze | P6, on its own trigger |
   CHANGED  Ruled since draft 1 (2026-10-26): 15.12.4's licence (PREFIX: findings 3, 4 and 5) and 15.1…
TOTAL {'changed': 15, 'added': 7, 'removed': 0, 'unchanged': 165}
```
