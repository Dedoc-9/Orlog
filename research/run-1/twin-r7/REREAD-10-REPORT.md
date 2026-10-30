<!-- R7 re-read 10, saved by the draft's author, 2026-10-29: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 10: the whole of draft 12 (the twin's report)

This is the same reviewer's tenth re-read under R7, again of **the whole draft**. It is review evidence, not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound or that the containment test passes, and neither is reported as shown.

## Summary

Draft 12 states his five answers faithfully and answers all fourteen of my ninth re-read's findings as the adopted dispositions record.

**The S1–S7 probe keeps its grade wherever it is cited.** It is "MEASURED on those stand-ins only, never on a version-1 interpreter, and it freezes no format". Draft 2 is presented everywhere as the candidate to test, never as adopted or frozen.

I have 6 findings. **One needs his decision:**

- **S15.3-1.** His S15.5-2 answer says a law with read-once ports and no tick block "cannot have tick records". But the A2 session table, which is still open, lets `close()` run a tick in any law: with no each-tick port, "every each-tick port is filled" holds vacuously. So a live one-shot session can project a log its own loader refuses (probe P3). The A2 row has to forbid it. Whether that waits for A2 or is ruled now is his choice.

The other five are drafting points, listed in §6.

## 1. Provenance

**Read whole:**
- `REREAD-10-BRIEF.md`
- `SPEC-15-DRAFT-12.md`, lines 1–757, title to last line, in two reads
- `REREAD-9-DISPOSITION.md`

**Read in part:**
- `RULINGS-AS-RULED.md`: a Grep, then lines 2332–2379, which is the whole of its last section ("Re-read 9's five questions"). The section before it, every ruling since re-read 8, I relied on from my whole reading of it in re-read 9 and did not reopen here.
- `CUT-SCHEMA.md`: a Grep for S6, then lines 72–83 (the shape table, with S6's new dated note), 165–176 (its "Does not show") and 206–241 (the stand-in section, whole).

**Not opened:**
- `AR-REREAD-10.md` and `DRAFT-12-CHANGES.md`. They do not bound this re-read, and I read every clause of the draft instead.
- `T10-STATEMENTS.md`, unchanged since re-read 6.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before, read in full earlier.

**Source needed** (named, not opened):
- **SN-1.** 1a's specification of the containment step's S1–S7 test: its fixtures and its pass condition (S15.9-1).

## 2. Faithfulness: the clauses tagged with his five answers

- **S15.5-1** (15.5): "the fixed number 3 is `580000000300000000`", with the rule unchanged. Faithful.
- **S15.3-1** (15.3, the N3 bullet): "each read-once `'N'` is emitted at its own declaration as execution reaches it, never grouped at the first, so the live trace equals replay's (RO′-3)". Faithful.
- **S15.1-1** (15.1.4 and 15.7.3): "With no budget the ` budget <N>` part is omitted, and no budget of zero is encoded". Faithful. His later answer supersedes B2's adopted "encoded as `0`", and the draft follows the later answer.
- **S15.5-2** (15.5, a new bullet and a new table row): "has no tick records: a `t` line is refused LOG-RECORD, and its end records are `end 0 closed` and the read-once stop's". Faithful.
  - The table row says "a law with no tick block". Under PP3 a version-1 law with no tick block must have read-once ports, so this is equivalent to his wording.
- **S15.9-1** (15.9): "The pinned decoding rule identifies the exact byte grammar it decodes. Draft 2 is the candidate to test, not an adopted or frozen format: the version-1 reference tests S1 to S7 against it during the containment step, and a discrepancy is resolved before the pin. That is a prerequisite of the pin, not the general format freeze." Faithful, his qualification included.
- **His scope** (15.15 and 15.5). The two items he kept open, the law line's `<type>` and the prefix of a law with no read-once port, are listed open. The 1b runtime's exit code is listed open. Faithful.

## 3. Coherence, section by section

**Preamble, legend, 15.0.**
- The [open: X] list now reads "R1, R8, R10 to R12". Coherent.
- "Prefix ... or all of them in a law with none (PP3) [follows: PP3]". Coherent.

**15.1.**
- 15.1.4's omitted budget part is coherent with R5's `[ budget <N>]` and with 15.7.3's B2.
- The `<type>` spelling is open, and listed.

**15.2.** Unchanged.

**15.3.**
- N3's "at its own declaration" agrees with RO′-3 and with 15.11's replay.
- The open A2 table conflicts with the S15.5-2 ruling for one-shot laws (S15.3-1).

**15.4.** Unchanged and coherent.

**15.5.** Six changes; five are coherent, and one has an ordering gap:
- the corrected example;
- the one-shot rule;
- the conditioned header-only status ("`status LOG-OPEN READ-ONCE` when the run reaches the first read-once declaration, REFUSED when it refuses before it, RO′-4"), which is coherent;
- the table's `t 0` note;
- exit 1 [follows: G2], which is also his D3 compliance's "exit 1" and could cite it;
- the 1b exit code, listed open.

The gap: **the new "no tick block" check has no place in D2's order** (S15.5-1).
- D2.4 orders a line's checks, and D2.5 orders a tick record's: the value count, then the tick number, then the values.
- Take `t 2` at line 5 in a one-shot law. It is "a tick record in a law with no tick block" (LOG-RECORD), but it is also "not one more than the ticks before it" (LOG-TICK).
- His words, "A `t` line is refused as `LOG-RECORD`", decide it as LOG-RECORD. The draft should place that check with the read-once placement, before the tick number (probe P1).

**15.6.** Unchanged.

**15.7.** C1–C3, B1–B4 (with B2 restated) and 8.1–8.6 are coherent.

**15.8.** Unchanged and coherent.

**15.9.**
- The decoding, the frames and the byte candidate are coherent with CUT-SCHEMA §2 and its stand-in section.
- The probe's grade is kept.
- "A run that does not refuse emits no `'R'`: COMPLETED, a tick's NOT-RUN and LOG-OPEN, the read-once stop's included" answers S15.9-2.
- The new S1–S7 test on the version-1 reference sits "during the containment step". That step's fixtures are read-once-stop logs, but S1–S7 concern refusal cuts in general (TICK-BUDGET, If conditions, Perform last). Neither the S1–S7 test's fixtures and pass condition, nor who resolves a discrepancy and how, are stated (S15.9-1; SN-1).
- CUT-SCHEMA's S6 row has its dated note. Its "Does not show" still says "S6 is open under 4.3" (S15.9-2).

**15.10–15.12.** Unchanged and coherent.
- For a one-shot law, the boundary is its first port declaration, and "outside the tick block" is vacuous.

**15.13.**
- 15.13.4's "Of these, all are now ruled but the cut's byte grammar, whose candidate, draft 2, the containment step tests" is accurate against the list it closes.
- 15.13.8's NOT-RUN/LOG-OPEN row presumes a tick block ("the tick block's head before tick t"). A one-shot law whose log holds the record but no end record reads plain `LOG-OPEN` and so takes this row, although it has no tick block.
  - My reading is that K̂ is then empty, since nothing remains to run. The row should say so (S15.13-1; probe P2).
  - T10.7 has the same wording.

**15.14.** Unchanged.

**15.15.**
- The new rows are present.
- Three rows (15.1.4, 15.3's prefix, 15.5's 1b exit) were inserted ahead of 15.1.5, out of section order (S15.15-1).

## 4. My ninth re-read's findings

| finding | answered as adopted? |
|---|---|
| S15.0-1 | Yes: the legend's list, and Prefix [follows: PP3]. |
| S15.1-1 | Yes, by his answer: R5's form. |
| S15.1-2 | Yes: listed open. |
| S15.3-1 | Yes, by his answer: each `'N'` at its own declaration. |
| S15.3-2 | Yes: listed open under A2. |
| S15.5-1 | Yes: the example is corrected. |
| S15.5-2 | Yes, by his answer. The A2 table's `close()` now conflicts with it (S15.3-1). |
| S15.5-3 | Yes: the command line exits 1; the 1b runtime's code is listed open. |
| S15.5-4 | Yes: the status is conditioned. |
| S15.5-5 | Yes, in the table. |
| S15.9-1 | Yes, by his answer, his qualification kept. |
| S15.9-2 | Yes in 15.9, and CUT-SCHEMA's S6 note. Its "Does not show" is still stale. |
| S15.13-1 | Yes. |
| S15.15-1 | Yes. |

T10.0–T10.8 are unchanged. Nothing is proved.

## 5. Probes (UNEXECUTED; my worked consequences)

**P1 (S15.5-1).**
- Law: `1. Let g be given as an integer.` `2. Say g.`
- Log: the header, `once 490000000000000007`, `t 2`.
- By his words this is LOG-RECORD at line 5. By D2.5's order, if the "no tick block" check came after the tick number, it would be LOG-TICK.

**P2 (S15.13-1).**
- The same law, with the log the header plus `once ...` and no end record.
- The run binds g and runs `Say g`. The status is plain `LOG-OPEN`, so the court takes the NOT-RUN/LOG-OPEN row.
- With no tick block, I read K̂ as empty, so a claim at clause 2 would not be withheld by CUT-0.

**P3 (S15.3-1).**
- A one-shot session: g's arrival is assigned to the record, the record closes, then `close()`.
- By the A2 table, "every each-tick port is filled" vacuously, so "the open tick runs" and the projection holds `t 1`.
- The loader refuses that log LOG-RECORD (S15.5-2), so the session's own log does not load.

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| S15.3-1 | COHERENCE | The open A2 table's `close()` ("if every each-tick port is filled, the open tick runs") lets a one-shot law's session run a tick and project a `t` line, which S15.5-2 refuses at load (P3). | **yes**: whether `close()` is refused in a law with no tick block now, or within A2 |
| S15.5-1 | DRAFTING | The S15.5-2 check ("a tick record in a law with no tick block") has no place in D2.4 and D2.5's order. Place it before the tick number, so every `t` line in a one-shot law is LOG-RECORD, as his words say (P1). | no |
| S15.9-1 | GAP | The S1–S7 test "during the containment step" has no stated fixtures or pass condition. The containment step's fixtures are read-once-stop logs, but S1–S7 cover all refusal cuts. Who resolves "a discrepancy", and how, is unstated (SN-1). | no; 1a's specification |
| S15.9-2 | DRAFTING | CUT-SCHEMA's "Does not show" still reads "S6 is open under 4.3", beside the new dated note that F20.4 rules it. | no |
| S15.13-1 | DRAFTING | 15.13.8's NOT-RUN/LOG-OPEN row, and T10.7, presume a tick block. For a one-shot law's plain `LOG-OPEN`, say that K̂ is empty (P2). | no |
| S15.15-1 | DRAFTING | Three new rows of 15.15 stand out of section order, before 15.1.5. | no |

By his ruling on the re-reads, the drafting fixes (S15.5-1, S15.9-2, S15.13-1, S15.15-1, and S15.9-1 when 1a's specification is written) are to be recorded with their re-read before the build. S15.3-1 goes to him.
