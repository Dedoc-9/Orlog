# Re-read 9: PROPOSED dispositions of the twin's 14 findings (2026-10-29)

**Status: proposed, then adopted.** *Adopted 2026-10-29: he accepted all five recommendations and the drafting fixes and open items, with a qualification on S15.9-1 (draft 2 the candidate byte grammar to test, not adopted or frozen), recorded in `RULINGS.md`, "Re-read 9's five questions".* His instruction for draft 11: *"Report findings and proposed dispositions before
treating the draft as settled."* Nothing below is applied until he accepts it, and the five ASKs are his decisions.

The twin's report is `REREAD-9-REPORT.md`, saved unchanged; the text saved is equal to the hand-back in the twin's own
transcript. It read draft 11 (sha256 `937499a6…`) whole, title to last line, as he asked. It finds every ruling of
2026-10-28 and 2026-10-29 stated faithfully, re-read 8's three findings answered, and the S1-S7 probe cited at its grade
(MEASURED on version-0 stand-ins only) everywhere. The report shows neither that CUT-0 is sound nor that the
containment test passes.

Classes: **ASK** (his decision), **OWED** (a drafting fix for draft 12, re-read before the build), **OPEN** (listed open
in 15.15).

## Checked against the files first

- **S15.5-1.** CHECKED in RUNTIME-SPEC §5 and its numeric table (`x_from_i`: "raw = n·2³²"). A Fix is `'X'` and its
  8-byte raw value, so the fixed number 3 is raw 0x0000000300000000, written `580000000300000000`. The example
  `580000000000000003` is the fixed value 3·2⁻³². The example was the drafter's, in the typed-values packet put to him;
  he adopted it. The rule (the full tagged encoding) is unaffected.
- **S15.3-1.** N3's "the read-once `'N'` events are emitted there when the record closes" was the drafter's wording,
  adopted by him. RO′-3: "A read-once port binds where its declaration stands", and 15.11's replay requires the same
  trace. The twin's probe P2 holds on the text: with a statement between two read-once declarations, "emitted there"
  read literally puts both `'N'`s before it.
- **S15.1-1.** R5's law line, ruled earlier, is `(tick <clause>[ budget <N>])`, the budget optional. B2's "No budget is
  written 0 in the law's bytes" was the drafter's wording, adopted by him; it gives a second form of the line.
- **S15.5-3.** SPEC §11 G2: a compile refusal writes no receipt, and "the command line exits 1". RUNTIME-SPEC §1 gives
  the runtimes 0, 2 and 3 only. D2's compliance requires the same code and line across the four executions in 1b, so
  each runtime's loader refuses the log too, with an exit code no document states.
- **S15.9-1.** His answer on the pin's inputs: "if Finding 20 places the cut in `R`, specify whether and how the pinned
  rule decodes it from those bytes". F20.2 adopts the semantic rule, "not an independent certification of the exact
  draft-2 byte grammar". 15.15 leaves the grammar to P6, whose trigger is not ordered against the pin.

## Proposed dispositions

| # | proposed | what would be recorded |
|---|---|---|
| S15.0-1 | OWED | the legend's [open: X] list drops R2 and R9; Prefix: the top-level statements before the tick block, or all of them in a law with none (PP3) **[follows: PP3]** |
| S15.1-1 | ASK | which form the law line takes with no budget: (a) R5's, the ` budget <N>` part absent, B2's sentence restated to say so (recommended: R5 ruled the law's lines, and B2's point was that a written zero is refused); or (b) always `budget 0` |
| S15.1-2 | OPEN | the law line's `<type>` spelling, listed in 15.15 beside 15.6's, decided by "identity and bytes" |
| S15.3-1 | ASK | confirm that each read-once `'N'` is emitted at its own declaration as the run goes on past the first one, the live trace equal to replay (recommended); N3's "there" read as "from there on" |
| S15.3-2 | OPEN | when the host runs the prefix of a law with no read-once port, and when a refusal there is known, listed under "A2" unless he wants to rule it now |
| S15.5-1 | ASK | correct his T1 example: the fixed number 3 is `580000000300000000` (recommended), the rule unchanged |
| S15.5-2 | ASK | a one-shot law (read-once ports, no tick block): (a) its log holds no tick record, a `t` line refused LOG-RECORD, its end records only `end 0 closed` and 8.3's stop record (recommended); or (b) tick records allowed and ignored |
| S15.5-3 | OWED, part OPEN | 15.5 states that the command line exits 1 on a load refusal, as G2 for a compile refusal; how a 1b runtime refuses a log, and its exit code, listed open for 1b's specification (RUNTIME-SPEC §1) |
| S15.5-4 | OWED | 15.5's header-only status conditioned: `status LOG-OPEN READ-ONCE` when the run reaches the first read-once declaration; a refusal before it is REFUSED (RO′-4) |
| S15.5-5 | OWED | the table says `t 0` at line 4 in a read-once law is M1, LOG-RECORD, by D2.4; LOG-TICK otherwise |
| S15.9-1 | ASK | (a) the cut's byte grammar the pinned rule decodes is fixed before the pin, apart from P6's general freeze, draft 2 its candidate and its S1-S7 check on the version-1 reference part of the containment step (recommended: his every-input principle); or (b) pin over draft 2, a later change making a new candidate |
| S15.9-2 | OWED | 15.9 says NOT-RUN and LOG-OPEN emit no `'R'`, as F20's compliance does; CUT-SCHEMA's S6 row gains a dated note that F20.4 rules it |
| S15.13-1 | OWED | 15.13.4 says which of the pin's inputs are ruled, and that the cut's byte grammar is not (or is, per S15.9-1) |
| S15.15-1 | OWED | 15.15 gains rows for S15.1-2, S15.3-2, the one-shot law if not ruled, and the byte grammar's timing |

**Totals proposed:** 5 ASK, 7 OWED (one with an open part), 2 OPEN: 14.

**What follows, if he accepts:** draft 12 applies the OWED fixes and his five answers, its affected clauses are
computed, and the twin re-reads it. By his word (*"Do not loop indefinitely merely to obtain a clean report, but do not
waive a required re-read or build gate either"*) that re-read covers draft 12's changes and their affected clauses;
whether it is whole again is his choice. The publication decision is his, after that disposition.
