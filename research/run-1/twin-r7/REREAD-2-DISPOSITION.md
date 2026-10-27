# Re-read 2: the disposition of the twin's 23 findings (2026-10-27)

The twin's report is `REREAD-2-REPORT.md`, saved unchanged: 6 findings on the labels ruling, 5 on the rule table, 4 on
R6's control, 3 on the late dependencies, 4 on draft 3's other changes, and 1 on T10.5. Each is disposed below by the
draft's author. Nothing here is ruled.

Classes: **DRAFT** (fixed in draft 4), **ASK** (put to the owner), **LEDGER** (`ROUNDS.md`), **NOTED** (no change).

## Checked against the files first

- **LABELS-1.** CHECKED: draft 3 does not contain "start set". K1's adopted start set is missing from the text, so the
  draft alone does not decide the twin's R2-P1.
- **TABLE-1.** CHECKED: SPEC §3 has one row for the form, "`Perform <name>` or the name alone as a statement | calls
  the procedure" (SPEC.md line 83). The built parser makes the same node, `Perform`, for both spellings
  (`src/orlog/syntax.py`, lines 456 and 558, the second commented "the name alone calls the procedure (§3, §13)"). So
  the table's "Perform", put to him as "proposed from K1 and SPEC §3", reads as SPEC §3's row. That is still put to him
  to confirm (ASK), as his answer of 2026-10-27 asked for any point the definitions leave open: *"return it as a
  precise ruling question rather than silently extending K1."*
- **LABELS-2.** CHECKED: packet B names its "bullet 1" in its own §4: "(a) is bullet 1 word for word", which makes it
  R6's first licence bullet ("It must stand before the first port declaration, outside the tick block").
- **CHANGED-4.** Checked in re-read 1 against `src/orlog/court.py` (`panel`): integrity is its own column
  (`REREAD-1-DISPOSITION.md`). The twin cannot see the court; the draft's [v0] tag stands.
- **V0CTL-2.** His words already name the comparison's variable: *"The R6 comparison must isolate one variable: R6
  versus no active log declaration."* A control with no log declaration is a version-0 law, so the header, the receipt
  frame, the trace's domain, the clause ids and the HELD rule change with it. Those are what removing the declaration
  entails. The row must say so; no ruling is needed.

## The dispositions

| # | disposition | what is done |
|---|---|---|
| LABELS-1 | DRAFT | K1's start set stated in the licence, in its adopted words: the top-level clause that is or holds the boundary, plus every later top-level clause. No fixture's outcome is stated |
| LABELS-2 | DRAFT | the exempt-and-licensed line says what bullet 1 is (R6's first licence bullet, which (a) restates) and that the identity rests on 15.1.3's open places; it is tagged as following, not ruled |
| LABELS-3 | DRAFT | the legend's `[ruled: F24]` names the labels ruling's adoption of D's definition |
| LABELS-4 | DRAFT | a note that B1's label and its proposed wording differ only for a nested port declaration, which 15.1.3's proposal refuses; 15.0's wording stands |
| LABELS-5 | DRAFT | the gloss replaced by the adopted words: "The existing version-0 default behavior is not enough to establish this" (unquoted, adopted text) |
| LABELS-6 | DRAFT | a new legend tag, `[follows: …]`, for a statement drawn from named rules and clauses and not ruled itself; 15.12.2's sentence and the exempt-and-licensed line take it; 15.1.6's sentence is corrected (claims at or after the boundary are unlicensed, and the boundary is never after this port) and takes it |
| TABLE-1 | ASK | whether the table's "Perform" is SPEC §3's row, the bare name included |
| TABLE-2 | NOTED | the last row's trigger is moot while the table covers every kind; TABLE-5's fix makes a form R2 adds bring its own row |
| TABLE-3 | DRAFT | 15.13.8 says K̂'s "may execute" is CUT-0's own reachability, as built and proposed for the pin, with its version-1 rows above; it is not the PREFIX table |
| TABLE-4 | DRAFT | 15.1.3's open sentence: the closure's rules, started from the top-level clauses other than the tick block |
| TABLE-5 | DRAFT | 15.1.1's tag: a form R2 adds needs a row of the closure's table (15.12.4) |
| V0CTL-1 | DRAFT | his decision line quoted in 15.12.6: "add the measured version-0 control as a separate row" |
| V0CTL-2 | DRAFT | 15.12.6: a control with no log declaration is a version-0 law, and what that changes is named; the row compares standings both rules define alike. Tagged [open: 1a's specification] for the row's design |
| V0CTL-3 | DRAFT | 15.13.11's "each row's control" excludes the separate measured control |
| V0CTL-4 | DRAFT | 15.14 names the measured control's label too |
| LATE-1 | DRAFT | as TABLE-5 |
| LATE-2 | DRAFT | as TABLE-3 |
| LATE-3 | DRAFT | 15.13.11: a completed evaluation prints as true in k of k or refuted, and one with none in 12's order |
| CHANGED-1 | DRAFT | the title dated 2026-10-27 |
| CHANGED-2 | DRAFT | 15.3's tag: the presupposition named as 15.12.4's, open with finding 6, never as ruled |
| CHANGED-3 | DRAFT | 15.13.4 in his words: "Court R1 remains a condition of HELD alongside E2" |
| CHANGED-4 | NOTED | checked above |
| T10.5-4 | LEDGER | "the frames of its body's statements, nested ones included" |

**Totals:** 19 DRAFT, 1 ASK, 2 NOTED, 1 LEDGER: 23, each disposed once. The findings re-read 2 found still open from
re-read 1 stay as disposed there: F24-7 and PREFIX-15 noted, PREFIX-16 open (`REREAD-1-DISPOSITION.md`).

## What follows

Draft 4 applies the DRAFT dispositions and his answer to TABLE-1. Its changed clauses are not built before the twin
reads them. That read is proposed to go with finding 6's re-read, so that a clause the next ruling also changes is read
once, in the text it leaves; nothing is being built meanwhile.
