<!-- R7 re-read 11, saved by the draft's author, 2026-10-29: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 11: draft 13, targeted, with his cross-section check (the twin's report)

This is the same reviewer's eleventh re-read under R7. As he set it, it is targeted (draft 13's changed clauses and AR-REREAD-11's set) plus the cross-section check he requires on the one-shot law and `close()`. It is review evidence: not a proof, and not a ruling. Every probe is **UNEXECUTED**, and every fixture outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound or that the containment test passes, and neither is reported as shown.

## Summary

**The cross-section check holds.**
- A one-shot law has read-once ports and no tick block. On every session path the draft states, its session produces only logs its loader accepts.
- The loader, the four statuses and CUT-0's rows treat those logs alike.

**His answer is stated faithfully.** All four of my tenth re-read's findings are answered as adopted.

**There are 4 findings, and none needs his decision.**
- The most important, **S15.3-1**: with `close()` refused in a one-shot law, the record's closing event is still open under A2. The A2 row should say that event cannot be `close()`. Nor does 15.3 say that an ordinary `end()` projects `end <n> closed`.

## 1. Provenance

**Read whole:**
- `REREAD-11-BRIEF.md`
- `DRAFT-13-CHANGES.md`

**Read in part:**
- `RULINGS-AS-RULED.md`: a Grep, then lines 2380–2411, which is the whole of its last section ("Re-read 10's question").
- `SPEC-15-DRAFT-13.md`:
  - a Grep over the whole file for `close()`, "no tick block", one-shot, Prefix, "K̂ is empty", PP3, the stop's records and `end 0 closed`;
  - lines 1–10, 155–314 (15.3, 15.4 and 15.5 whole), 314–388 (15.7 whole), 470–509 (15.12's trigger and boundary), 612–651 (15.13.8's rows) and 720–763 (15.15 whole);
  - every changed clause, and every clause of the cross-section list.
- `AR-REREAD-11.md`: its clause list, by Grep. Of its 77 clauses, all lie in the ranges above except four that the diff shows unchanged since my whole reading of draft 12: the preamble's F8 and PP tags, 15.8's unread-count line, and 15.9's `'N'` payload.
- `T10-STATEMENTS.md`: lines 19–22, T10.7 and T10.8.
- `CUT-SCHEMA.md`: a Grep for "S6 is", finding its new dated note.

**Not opened:**
- `REREAD-10-DISPOSITION.md`. `DRAFT-13-CHANGES.md` and his answer give its adopted content.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before, read in full earlier.

**Source needed:** none for this check.

## 2. Faithfulness

His words:

> * If the law has no tick block, `close()` does not run a tick.
> * It must not emit a `t` record.
> * It must not create a log that its own loader rejects under the adopted one-shot rule.
> * The existing one-shot completion and stop behavior remains unchanged.

He adopted "option (a): refuse `close()` in a law with no tick block".

- **15.3, the `close()` row.** It now reads "legal when: as above, in a law with a tick block". **Faithful.**
- **15.3, the new bullet.** "In a law with no tick block, `close()` is refused. It runs no tick, emits no `t` record, and never makes a log its own loader refuses; a one-shot law's completion and its read-once stop are unchanged. The refusal's name is A2's. [ruled: his answer on re-read 10's S15.3-1; open: amended set "A2", the name]". **Faithful.**
  - The code is left open, which matches his scope: "It does not decide the remaining open A2 session mechanics".
  - It sits within "A door refusal or a refused move does not end the session" and "A refused move is not appended to the history". That is coherent.

## 3. The cross-section check, clause by clause

**15.0 (Prefix, Tick block).** "or all of them in a law with none (PP3)"; "at most one". Agrees.

**15.1.3 (PP3).**
- A one-shot law is allowed.
- An each-tick port without a tick block is PORT-PLACE, so a one-shot law has no each-tick port.
- Agrees.

**15.3, the session table and its bullets.**
- `close()` is ruled out in a one-shot law.
- `end()`'s "the open tick holds no assignment" is vacuous in a one-shot law.
- **N2:** an `end()` before the record closes is the stop, projecting `end 0 not-run read-once INPUT-MISSING <port>`.
- **N3:** the prefix runs at the session's opening. A refusal there leaves the log with the header alone, by F10.
- **F10:** a refusal after the record closed leaves the header and the `once` line.

Each of those logs loads under 15.5.

One gap (S15.3-1):
- The completion path needs the record to close, and that event is still open ("the events that fill and close the record"). In a one-shot law that event cannot be `close()`.
- After the record closes, `end()` must project `end 0 closed`. 15.3 states no ordinary `end()` projection; 15.5 and 15.7.5 imply it.

**15.4.**
- F10's verifier applies unchanged.
- A refused `close()` is not appended to the history, so it can raise no HISTORY-MISMATCH.
- Agrees.

**15.5, the logs a one-shot law can have.**

| log | loads? |
|---|---|
| header alone | yes (8.4) |
| header + stop record | yes (8.3) |
| header + `once` (open) | yes |
| header + `once` + `end 0 closed` | yes |
| any `t` line | LOG-RECORD |
| `end 0 closed` without `once` | M2, LOG-END |
| stop record after `once` | 8.3 fails, LOG-END |

- The one-shot bullet ("its end records are `end 0 closed` and the read-once stop's"), the table row, and the order of checks all agree.
- The order now reads: "the read-once placement and, in a law with no tick block, any `t` line (LOG-RECORD ...)", before D2.5's tick checks. So `t 2` at line 5 is LOG-RECORD, as his S15.5-2 words say. This answers S15.5-1 (my re-read 10 probe P1).

**15.7.1 and 15.7.5.**
- The prefix is the whole law, and there are no tick records.

| one-shot log | status |
|---|---|
| header + `once` + `end 0 closed` | COMPLETED ("every tick record ran" is vacuous; the cause is closed) |
| header + `once`, open | plain `LOG-OPEN` |
| header alone | `LOG-OPEN READ-ONCE`, or REFUSED by RO′-4 |
| header + stop record | `NOT-RUN READ-ONCE INPUT-MISSING <port>` |

- No tick NOT-RUN is possible (8.6).
- Agrees with 15.5.

**15.8.**
- `ticks` is 0, and the unread count is 0, in a one-shot law.
- `tick-ops` with no tick begun is listed open.
- Agrees.

**15.12.**
- The trigger holds, since a port is declared.
- The boundary is the first port declaration.
- "Outside the tick block" is vacuous.
- Agrees.

**15.13.8, and T10.7.**
- COMPLETED gives an empty K̂.
- The new line reads "In a law with no tick block, a one-shot law's plain LOG-OPEN, nothing remains to run and K̂ is empty [follows: PP3; his answer on S15.5-2]". That answers S15.13-1. T10.7 gains the same: "in a law with no tick block, K̂ is empty".
- The stop row's "the tick block's body ... included" contributes nothing when there is none.
- REFUSED takes the ordinary rows.

The statuses and the rows agree. One wording gap remains (S15.13-1 below):
- The NOT-RUN/LOG-OPEN row still gives the cut as "the tick block's head before tick t", which is undefined in a one-shot law.

**15.15.**
- The rows are now in section order.
- `close()`'s refusal name, left open under A2 in 15.3, has no row (S15.15-1).

## 4. My tenth re-read's findings

| finding | answered as adopted? |
|---|---|
| S15.3-1 | Yes, by his answer: `close()` is refused in a law with no tick block. |
| S15.5-1 | Yes: the check is placed with the read-once placement, before D2.5. |
| S15.9-1 | Yes, as adopted: it is 1a's specification. 15.15's row for the S1–S7 test is still decided by "the containment step", and could name 1a's specification for its fixtures. |
| S15.9-2 | Yes: CUT-SCHEMA's "does not show" now notes that F20.4 rules S6. |
| S15.13-1 | Yes, in 15.13.8 and T10.7. |
| S15.15-1 | Yes. |

## 5. Probes (UNEXECUTED; my worked consequences)

All four use a one-shot law with a read-once port `g` and no tick block.

- **Q1 (completion).** The session assigns `g`. The record closes, by the open A2 event. Then `end()`.
  - The projection should be header + `once` + `end 0 closed`.
  - That gives COMPLETED, with K̂ empty.
  - The projection itself is not stated in 15.3 (S15.3-1).
- **Q2 (`close()`).** The session calls `close()`.
  - It is refused with A2's code (open), not appended, and does not end the session.
  - The log is unchanged.
- **Q3 (live, never ended).** The session assigns `g`, and the record closes.
  - The log is header + `once`, open.
  - That gives plain `LOG-OPEN`, with K̂ empty.
- **Q4 (stop).** The session calls `end()` before the record closes.
  - That gives `end 0 not-run read-once INPUT-MISSING g` and `NOT-RUN READ-ONCE`.
  - CUT-0 takes the stop row.

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| S15.3-1 | GAP | In a one-shot law the record's closing event (open, A2) cannot be `close()`; the open row should say so. Separately, 15.3 never states that an ordinary `end()` projects `end <n> closed`, although 15.5 and 15.7.5 rely on it (Q1). | no; within A2 |
| S15.3-2 / S15.15-1 | DRAFTING | 15.3 leaves the name of `close()`'s refusal open under A2, but 15.15's A2 rows do not list it. | no |
| S15.13-1 | DRAFTING | The NOT-RUN/LOG-OPEN row's cut, "the tick block's head before tick t", is undefined for a one-shot law's plain `LOG-OPEN`. Say that the cut is after the last statement, as for COMPLETED, with K̂ empty. | no |
| S15.9-1 | DRAFTING | 15.15's row for the S1–S7 test on the version-1 reference is decided by "the containment step" only. Name 1a's specification for its fixtures, as adopted. | no |

By his ruling on the re-reads, these are to be recorded with their re-read before the build.
