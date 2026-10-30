<!-- R7 re-read 9, saved by the draft's author, 2026-10-29: the twin's report, delivered as its message (it could not write files). Copied without change. -->

# R7 re-read 9: the whole of draft 11 (the twin's report)

This is the same reviewer's ninth re-read under R7. It covers **the whole draft**, as he asked. It is review evidence: not a proof and not a ruling. Every probe is **UNEXECUTED**, and every fixture outcome is **my own worked consequence**. Nothing here shows that CUT-0 is sound, or that the version-1 containment test passes, and neither is reported as shown.

## Summary

Draft 11 states the rulings of 2026-10-28 and 2026-10-29 faithfully, clause by clause, and answers all three of re-read 8's findings. Wherever it cites the S1-S7 probe, it keeps "MEASURED on version-0 stand-ins only" and claims nothing about a version-1 interpreter or a format freeze.

I have 14 findings. Five need his decision:

1. **S15.5-1.** His own T1 example gives "a fixed 3" as `580000000000000003`. Under RUNTIME-SPEC §5 (Fix = `'X'` followed by the 8-byte raw value, with value = raw × 2^-32), that hex is the fixed value 3·2^-32. The fixed number 3 is `580000000300000000`.
2. **S15.9-1.** His every-input principle says the pinned rule reads the cut "from those bytes". But F20.2 adopts only the semantic rule, not draft 2's byte grammar, and 15.15 leaves that grammar to P6's own trigger, which is not ordered before the pin.
3. **S15.3-1.** N3 says the read-once `'N'` events "are emitted there", at the first read-once declaration. RO′-3 binds each read-once port at its own declaration. When statements stand between two read-once declarations, the live trace and the replay trace would differ (probe P2).
4. **S15.1-1.** R5's law line `(tick <clause>[ budget <N>])` makes the budget optional, while B2 says "An absent budget is encoded as `0` in the law's bytes". These give two forms of the law bytes, so two law seals.
5. **S15.5-2.** PP3 allows a one-shot law with read-once ports and no tick block, but nothing says whether its log may hold tick records, or how they load or run.

## 1. Provenance

**Read whole:**
- `REREAD-9-BRIEF.md`
- `SPEC-15-DRAFT-11.md`, lines 1–732, title to last line
- `REREAD-8-DISPOSITION.md`

**Read in part:**
- `RULINGS-AS-RULED.md`: a Grep of its headings, then lines 567–2331, which is the whole of its last section, every ruling since re-read 8. Lines 1–566 were read in earlier re-reads.
- `CUT-SCHEMA.md`: a Grep, then lines 1–240, which take in §1–§4 and the whole section "Version 1's frames on version-0 stand-ins". The superseded draft 1 and the six seams beyond line 240 were not read.
- `DRAFT-11-CHANGES.md`: lines 1–60, the change table.

**Not opened:**
- `AR-REREAD-9.md`. It does not bound this re-read, and I read every clause instead.
- `T10-STATEMENTS.md`, unchanged since re-read 6. I rely on my reading in re-read 7.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before, read in full earlier.

**SOURCE NEEDED** (named, not opened):
- **SN-1.** The D1.a code table "as put to him". The draft carries it, and I cannot check it against what he saw.
- **SN-2.** The budget's and counting's "four worked examples" (B4), and E1–E12 (D2), to probe against.
- **SN-3.** `sema.py`'s `law_bytes`: how the port line spells `<type>`, and how it writes an absent budget (S15.1-1, S15.1-2).

## 2. Faithfulness: the clauses tagged with this round's rulings

**F8 (finding 8)**

| rulings | where | verdict |
|---|---|---|
| 8.1 / 8.2 | 15.7.5 (`READ-ONCE` second token; no t at the stop) | faithful |
| 8.3 | 15.5's end record and its four load conditions | faithful |
| 8.4 / 8.5 | 15.5's three-line header-only log; M1–M4 refused | faithful |
| 8.6 | 15.5 and 15.7.5 (t = n + 1, no leading zero, an each-tick port; the row chosen by the second token) | faithful |
| the `once` line | 15.5 | faithful |
| D1.a–D1.d, D2.1–D2.6, D3.1–D3.5 | 15.5 | faithful, with one omission (S15.5-3) |
| T1–T6 | 15.5 and 15.9 | faithful, including his example, which is the problem in S15.5-1 |

**F20 (finding 20)**
- F20.1–F20.4 (15.9): faithful.
- F20.2's qualification is kept: "His ruling adopts the semantic rule, not this byte grammar."

**R2**
- R2.1 and R2.2 (15.0, 15.1.1): faithful. The draft avoids his word "reserved" for `truth value` and `text`, saying "type words only within the port form". That stays clear of [fixed]'s "no word is newly reserved".
- R2.3 and its clarification (15.12.4's last bullet, 15.13.8's closing line): faithful. The clarification is explicit: "Execution of the tick body never makes an earlier top-level prefix statement run again; a procedure defined in the prefix stays in the reach when the tick body reaches it by Perform."

**PP (port place)**
- PP1–PP6 (15.0, 15.1.3, and two [follows] in 15.12.4): faithful.
- PP4 is condensed: "a read-once port only after its declaration in the execution structure". His fuller list ("later top-level statements, the tick body, or procedures reached only from those permitted contexts") is implied. This is minor.

**Counting and the budget**
- C1–C3 (15.7.1, 15.7.2), B1–B4 (15.7.3) and B3's `tick-ops` (15.8): faithful.

**N2, N3, F10**
- N2 (15.3): faithful.
- N3 (15.3): faithful to his words. Those words are the subject of S15.3-1.
- F10 (15.3, 15.4): faithful.

## 3. Coherence, section by section

**Preamble and legend.**
- The [open: X] entry still names "R2" and "R8 to R12" among the open sheet items. R2 and R9 are now ruled (S15.0-1).

**15.0.**
- PP3 allows a law with no tick block, so "Prefix: the top-level statements before the tick block" is undefined for that law (S15.0-1).
- The other terms are coherent.

**15.1.**
- **15.1.1** is coherent with SPEC §2: `given`, `each` and `at most` are reserved, so the new forms are SYNTAX in version 0.
- **15.1.3 (PP4).**
  - Under SPEC §5's scoping, a procedure defined before a port cannot name it: the reference is UNDECLARED, raised before PORT-READ. That is coherent.
  - A procedure reached from both the prefix and the tick body is PORT-READ, by its call contexts.
- **15.1.4** against B2: S15.1-1.
- **15.1.4's `<type>` spelling** in the law line is not given, and it is not listed open, although 15.6's spelling is (S15.1-2; SN-3).
- **15.1.5 and 15.1.6:** unchanged and open.

**15.2.** Unchanged. R3's details are open and listed.

**15.3.**
- N2, N3 and F10 are coherent with RO′-1–RO′-5 and with 15.4, except for two points:
  - **N3's "there"** against RO′-3's binding of each port at its own declaration (S15.3-1).
  - **N3's scope.** It covers "the top-level statements before the first read-once declaration". For a law with no read-once port it says nothing, so when the host runs the prefix of an each-tick-only law, and when a refusal there is known, is unstated (S15.3-2).
- F10's three log endings agree with 15.5's loadable forms, and with RO′-4 (a refusal before the declaration is REFUSED whatever the log holds).

**15.4.** F10's verifier is coherent.

**15.5.**
- **Values.** T1's fixed example (S15.5-1).
- **One-shot law.** Tick records for a law with read-once ports and no tick block are unaddressed (S15.5-2).
- **Exit status.** His D3 compliance requires exit 1 for each of the nine load refusals ("exit 1"). Neither the draft nor RUNTIME-SPEC §1 states it: RUNTIME-SPEC §1 gives 0 for a completed or refused run, 2 for I/O failures, and 3 for C misuse. His D2 compliance requires the same results across all four executions, so the backends' runtimes need the code too (S15.5-3).
- **Header-only status.** The parenthesis "(exactly its three LF-terminated lines, `status LOG-OPEN READ-ONCE`)" reads as unconditional. F10's own example (a header-only log whose prefix refuses, giving `REFUSED DIVISION-BY-ZERO 1`) and RO′-4 show the status depends on the run (S15.5-4).
- **`t 0` at line 4 in a read-once law.**
  - D2.4 puts the read-once placement before the `t` content, so my worked consequence is LOG-RECORD (M1).
  - The table's "(so `t 0` too)" LOG-TICK applies when the law has no read-once port.
  - These are consistent, but the table could say so (probe P5).
- **The witness.** D3.3–D3.5 are coherent with RUNTIME-SPEC §1's I/O exit (D3.5).
- **in_0** "when present" is coherent with 8.3.

**15.6.** Unchanged and open (finding 37).

**15.7.**
- C1–C3 and B1–B4 are coherent with SPEC §7 and §11 G4.
- B2's FUEL is a compile code. S7's FUEL-EXHAUSTED is a runtime code, so the two do not collide.
- 15.7.5's row choice is coherent with 15.13.8.

**15.8.** `tick-ops` (B3) and F10's unread count of 0 are coherent.

**15.9.**
- The decoding and the frames are coherent with CUT-SCHEMA:
  - the tick block's plain frame (selector 0xFFFF) equals the stand-in While's frame;
  - the port declaration has no frame, consistent with the stand-in's "never a frame's last statement";
  - in version 1 a Perform may be the last frame, as S4 states.
- **The probe's grade is kept.** "MEASURED on those stand-ins only, never on a version-1 interpreter, and it freezes no format" matches CUT-SCHEMA's own "MEASURED on version-0 stand-ins only" and its "does not show".
- **The byte grammar and the pin** (S15.9-1).
- **CUT-SCHEMA itself is stale.** Its §2 table still marks S6 "open", although F20.4 has ruled it (S15.9-2).
- **'R' at the stop, NOT-RUN and LOG-OPEN.** F20's compliance says these "emit no R". 15.13.8 says so for the stop, but 15.9 does not say it for NOT-RUN and LOG-OPEN (S15.9-2).

**15.10–15.11.**
- 15.10's invariants follow from C2. Coherent.
- 15.11's Replay requires the same trace, which bears on S15.3-1.

**15.12.** The R2.3 reach bullet is coherent with the rule table and with PP1 and PP2.

**15.13.**
- ROWS-1 and ROWS-2 are applied.
- The stop's premises now carry ruled tags (PP1, C1).
- The pin's inputs are listed. All are now ruled except the cut's byte grammar (S15.9-1).
- 15.13.4 still reads "resolve those inputs" without saying which are now resolved. That is minor and folded into S15.13-1.

**15.14.** Unchanged.

**15.15.**
- The rows reflect the round. Four items are missing:
  - S15.5-2 (the one-shot law's tick records);
  - S15.3-2 (the prefix timing with no read-once port);
  - S15.1-2 (the law line's `<type>`);
  - the timing of the cut's byte grammar against the pin (S15.9-1).

## 4. Re-read 8's findings

| finding | answered as disposed? |
|---|---|
| ROWS-1 | **Yes.** "Its rules for the version-1 kinds are R2.3's, fixed by R2's ruling before the pin ... The pin records them and does not decide them." 15.15 no longer says "the reach: the pin". |
| ROWS-2 | **Yes.** 15.13.4: "The list above is what is known now; the record checked against the candidate decides which inputs exist. What counts as a read ... is decided by 1a's specification." |
| CHANGED-1 | **Answered by ruling.** 8.2 gives the stop's NOT-RUN no t, so the sentence it concerned is gone. |

T10.0–T10.8 are unchanged and coherent with 15.13.8. T10.5's "Refused at its own operation (version 1 only)" agrees with B4. Nothing is proved.

## 5. Probes (UNEXECUTED; my worked consequences)

**P1 (S15.5-1).**
- RUNTIME-SPEC §5 encodes a Fix as `'X'` (0x58) followed by its 8-byte raw value, and a Fix's value is raw × 2^-32.
- The fixed number 3 has raw 3·2^32 = 0x0000000300000000, so its encoding is `580000000300000000`.
- `580000000000000003` decodes to 3·2^-32.
- The other two examples check out: `4201` is true, and `54000000026869` is "hi".

**P2 (S15.3-1).**

```
1. Let g be given as an integer.
2. Say 5.
3. Let h be given as an integer.
4. Say g plus h.
```

- Replaying the log (header, then `once` with g and h) gives the events N(g), S, N(h), S, by RO′-3.
- Read literally, N3 makes the live run emit N(g) and N(h) together at clause `1.`, before S. The two traces differ.

**P3 (S15.5-2).**

```
1. Let g be given as an integer.
2. Say g.
```

- The log is the header, then `once 49…07`, then `t 1`, then `end 1 closed`.
- Whether `t 1` loads (and with what code if not), or runs as an empty tick, is **not determined by §15**.

**P4 (S15.5-3).**
- A log whose first line ends in CR is refused LOG-LINE at line 1, and the witness is written.
- Exit 1 is required by his compliance, but stated nowhere in §15 or in RUNTIME-SPEC.

**P5.**
- `t 0` at line 4 for a law with a read-once port is LOG-RECORD (M1), by D2.4.
- For a law with no read-once port it is LOG-TICK.

**P6 (S15.1-1).**
- For `Each tick, do the following.`, the law line is either `(tick 2)` (by R5's brackets) or `(tick 2 budget 0)` (by B2).
- The two give different seals. **Not determined by §15.**

## 6. Findings

| # | class | finding | needs his decision |
|---|---|---|---|
| S15.0-1 | DRAFTING | The legend's [open: X] still lists R2 and "R8 to R12", though R2 and R9 are ruled. "Prefix" is undefined for a law with no tick block, which PP3 allows. | no |
| S15.1-1 | COHERENCE | R5's law line `(tick <clause>[ budget <N>])` (budget optional) against B2's "An absent budget is encoded as `0` in the law's bytes": two law-byte forms, two seals (P6). | **yes**: confirm that B2 fixes the line form as always written (`budget 0`) |
| S15.1-2 | GAP | The law line's `<type>` spelling (15.1.4) is neither given nor listed open; 15.6's is (SN-3). | no; list it open |
| S15.3-1 | COHERENCE | N3's "The read-once `N` events are emitted there when the record closes", read with RO′-3's "binds where its declaration stands": when statements stand between read-once declarations, the live trace differs from replay (P2; 15.11). | **yes**: confirm that each `'N'` comes at its own declaration as the run goes on |
| S15.3-2 | GAP | N3 covers "the top-level statements before the first read-once declaration". For a law with no read-once port, when the host runs the prefix, and when a refusal there is known, is unstated. | no; list it under A2, unless he wants to rule it |
| S15.5-1 | COHERENCE | His T1 example "Fixed 3 = `580000000000000003`" is the raw value 3, i.e. 3·2^-32, under RUNTIME-SPEC §5. The fixed number 3 is `580000000300000000` (P1). The draft quotes him faithfully. | **yes**: his words; confirm the example or correct it |
| S15.5-2 | GAP | PP3's one-shot law (read-once ports, no tick block): whether its log may hold tick records, with what load code, or how they run, is not stated. Finding 7's old 15.15 row was removed (P3). | **yes**: identity and bytes, or PP3 |
| S15.5-3 | GAP | His D3 compliance requires "exit 1" for each of the nine load refusals, and the same results across the four executions. Neither the draft nor RUNTIME-SPEC §1 states this exit code (P4). | no; state it in 15.5 and in RUNTIME-SPEC §1 |
| S15.5-4 | DRAFTING | 15.5's "(exactly its three LF-terminated lines, `status LOG-OPEN READ-ONCE`)" reads as unconditional. A prefix refusal over the same log is REFUSED (RO′-4; F10's example). | no |
| S15.5-5 | DRAFTING | The table's "(so `t 0` too)" (LOG-TICK) and M1 (LOG-RECORD) both cover `t 0` at line 4. D2.4 decides it: LOG-RECORD in a read-once law. Say so (P5). | no |
| S15.9-1 | QUESTION | The pinned rule "decodes the cut from those bytes" (his pin's-inputs answer), but F20.2 adopts the semantic rule, not draft 2's byte grammar, and 15.15 leaves the grammar to P6's own trigger, unordered against the pin. By his every-input principle, the byte grammar the decoder reads looks like an input of the pinned rule. | **yes**: whether the cut's byte grammar (separately from the general P6 freeze) is fixed before the pin, or the pin uses draft 2 with a later change making a new candidate |
| S15.9-2 | DRAFTING | F20's compliance ("Stop, NOT-RUN and LOG-OPEN emit no R") is stated for the stop only. CUT-SCHEMA §2's table still marks S6 "open", though F20.4 has ruled it; that is outside §15 but cited by it. | no |
| S15.13-1 | DRAFTING | 15.13.4 lists the pin's inputs as still to resolve. All but the cut's byte grammar are now ruled; it could say so. | no |
| S15.15-1 | DRAFTING | 15.15 lacks rows for S15.1-2, S15.3-2, S15.5-2 and the byte grammar's timing against the pin (S15.9-1). | no |

By his ruling on the re-reads, the drafting fixes (S15.0-1, S15.1-2, S15.3-2, S15.5-3, S15.5-4, S15.5-5, S15.9-2, S15.13-1, S15.15-1) are to be recorded with their re-read before the build. S15.1-1, S15.3-1, S15.5-1, S15.5-2 and S15.9-1 go to him.
