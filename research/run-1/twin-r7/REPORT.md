<!-- Saved verbatim by the draft's author, 2026-10-26: the twin's report, delivered as its final message because the harness refused its file write (its note below). Nothing in it is changed. -->

R7 TWIN REVIEW OF SPEC §15 DRAFT 0. This is review evidence, not proof and not a ruling.

NOTE ON DELIVERY: the harness refused to let me write `twin-r7-out\REPORT.md` ("Subagents should return findings as text, not write report files"). The whole report is therefore below, and no file was written. Please save it to that path yourself if you need the file.

SUMMARY
- Findings by tag: FAITHFULNESS 14, COHERENCE 13, GAP 17, T10 6, QUESTION 3, FIXED 2. Total 55.
- By severity: blocks the round 6; needs a ruling 26; minor 23.
- The three most important findings:
  1. **The PREFIX proposal is wider than the ruling (F3).** 15.12.4's open proposal, "static closure from the input point", read with 15.0's "Input point: the first place a port is read", would exempt a claim placed after an each-tick port's declaration but before the port's first read. R6's ruled licence says "It must stand before the first port declaration". In the same clause, the draft also drops R6's "decided from the text" and weakens "must stand" to "stands" (F2).
  2. **Read-once ports, logs without ticks, and LOG-* load refusals are undefined (F6–F9).** No session event fills a read-once port, and the read-once record has no syntax. The LOG-* codes are named but have no conditions and no precedence. Nothing says whether a load refusal writes a receipt, or whether the log is validated whole or read record by record. And "later records are not read" contradicts a receipt count of "tick records left unread".
  3. **The 'R' event and the CUT-0 rows are tagged ruled but are not in the cited rulings (F20, F21).** The claim that 'R' carries the cut is tagged [ruled: claims], but the claims ruling says nothing about the trace, and R5 fixes v1's new events as 'T' and 'N' only. 15.13.5–8 and 15.13.11 are also tagged [ruled: claims], but the ruling names R8 and CUT-0 only by name and digest. Separately, the open REFERENCE-ONLY proposal (15.13.10) collides with ruled R6: the PREFIX claim "stays held", and the PREFIX control "must read GROUNDED" (F24).

==================================================================
1. PROVENANCE
==================================================================
Files opened, Read tool only:
- twin-r7-inputs/SPEC.md
- RUNTIME-SPEC.md
- SPEC-15-DRAFT.md
- RULINGS-AS-RULED.md
- T10-STATEMENTS.md

I opened, searched and listed nothing else. My one Write attempt was refused, so no file was written.

SOURCE NEEDED:
- SN-1. ROUNDS.md's amended-set rows: port place, H2, A2 (and "the declared policy"), session record, binding, identity and bytes, four statuses, counting, budget, PREFIX, reporting. I judged every open clause on the draft's own proposal only.
- SN-2. RULINGS.md's sheet items R1, R2, sheet R8, R9, R14 and D1–D10, and its section "Fixed whatever is ruled", which defines the [fixed] tag. I cannot check that any [fixed] clause is on that list.
- SN-3. CUT-SCHEMA.md: S6, P6, draft 2 of the 'R' payload, and what the "selector" is.
- SN-4. The text and digest of CUT-0, and the court's R8 as built (court.py).
- SN-5. "Contract draft 0": the domain string `orlog-output-1`, LOG-MALFORMED, and probably "the draft's §1.5" that 15.3 cites.
- SN-6. Where R4 says the receipt must give the refusal's "code, clause and tick". Those words are not in RULINGS-AS-RULED.md (see E(i)).
- SN-7. The court's v0 standings: GROUNDED, UNREACHED, INCOMPLETE, VACUOUS, channels, ratification, the witness.
- SN-8. COMPAT-0, SNAP-1, A1, E18, the speed verdict, 1a/1b, S2 (cited by T10.4), F2 (cited by T10.6), DOCTRINE T12.
- SN-9. T10's own statement as it stood before the split.

==================================================================
2. SECTION A — COHERENCE (open clauses)
==================================================================

A1. §15.0 "Port" [open: R2; sheet R8], and the untagged terms
- Port has one reading.
- The bullets for Prefix, Tick block, Input point, Arrival, Door, Host, Session, Input log and Execution carry NO tag, against "Every clause carries one". Two of them are normative:
  - "Tick block: the last top-level clause" restates 15.1.3's open place rule as a definition.
  - "Input point: the first place a port is read in evaluation order" is what 15.12.4's open proposal turns on. It has two readings: a static first read site, or the first read that actually executes. "In evaluation order" suggests the dynamic reading; "static closure from" suggests the static one. It is also undefined in a tick-only law, which 15.12.1 says "still takes input".
- Missing dependencies: R3 (the types the door judges); R5 (the type's spelling in the law line); the PREFIX row.

A2. §15.1.1 Spellings [open: R2]
- One reading per form. They are consistent with 15.1.2: `given` and `each` are reserved (SPEC §2), so in v0 `Let x be given ...` fails the expression grammar, and `Each tick, ...` is SYNTAX (SPEC §13, "A call cannot begin with a reserved word ... SYNTAX").
- Missing:
  - how N is written (an integer literal only? Is a decimal SYNTAX, as SPEC §11 item 19 rules for While?);
  - whether `at most 0 operations` is legal;
  - examples for `a truth value` and `a text`;
  - where the law line's `"<name>"` comes from, as distinct from `<var>`. No form shows a name. I infer the name is the identifier.

A3. §15.1.3 Places [open: R2; "port place"]
- Several readings of "a read of an each-tick port outside the tick block":
  - Textual: every procedure body and every Define is outside the tick block, since To and Define are top-level only and the tick block is last. On this reading, no procedure or rule can ever read an each-tick port.
  - By evaluation: this needs reachability, and must settle a procedure performed from both the prefix and the tick block.
- Conflicts with SPEC §13's rule that "Every compile refusal belongs to exactly one phase": PORT-PLACE, TICK-PLACE and PORT-VARIABLE are given no phase and no order.
- Missing cases:
  - There is no code for the read itself. PORT-PLACE is "a port elsewhere", which reads as a declaration.
  - A port after the tick block breaks both PORT-PLACE and TICK-PLACE; the order between them is unsettled.
  - With two tick blocks, is the refusal at the first (not last) or at the second ("a second one")?
  - A port form in an inline arm: PORT-PLACE, or SYNTAX under SPEC §11 item 28?
  - Append or Remove on a port: PORT-VARIABLE, or TYPE as SPEC §13 rules for a For counter?
  - A law with ports and no tick block (or each-tick ports and no tick block) is neither allowed nor refused. If allowed, close(), the tick records and "one tick per tick record" have no body to run.
- Missing dependencies: the PREFIX row (the same reachability) and the budget (its compile refusal sits in 15.7.3).

A4. §15.1.5 [open: H2]
- Several readings. "Indented ... reads as it reads at column one" has no meaning in v0's line grammar: a statement follows "a label, one space" (SPEC §1), and v0 gives no rule for spaces before a label.
- "One decision" spans phases 2 and 3 of SPEC §13 without saying how they order.
- 15.15 adds "E18's COMPAT-0 settlement", which the clause's own tag omits.

A5. §15.1.6 [open: R1; cost sentence ruled: R6]
- It cites "§15.13" for grounding; grounding is §15.12.
- "Every claim evaluated after the port is read" understates R6. R6 strips every claim of the run except under PREFIX, including claims evaluated before the read: a claim in a procedure performed later, or a claim after an earlier port.
- Missing dependencies: R2, PREFIX.

A6. §15.2's open details
- The decimal and integer ASCII grammars are not given and not tagged open: leading +, leading zeros, -0, .5, 5., exponents. They decide INPUT-SYNTAX versus acceptance, and so the history.
- The form in which INPUT-GRID "names the two nearest grid values" is not given.
- The tag "details R3 leaves to 1a" (15.15) is unauditable: the reading set excludes "the details left for 1a".
- The ruled rules around these details do not cohere (B4): rule 1 vs rule 5, and the reachability of rule 2.

A7. §15.3 Session [open: A2]
- Read-once ports have no event:
  - assign(arrival, tick) needs "the tick is the open one" and the port's slot, but a read-once port belongs to no tick.
  - No rule says when the prefix runs, or what happens when a read-once port never arrives.
- "The open tick" is undefined. I infer it starts at 1 and advances at each close() that runs a tick.
- "Until SNAP-1, a refusal ends the session" [ruled: R4]: read literally, it covers run refusals, door refusals (INPUT-*) and move refusals. The retry bullet requires that door refusals do NOT end the session. Whether move refusals do is unsaid.
- "[fixed: R4 and the draft's §1.5]":
  - In this file, §1.5 resolves to 15.1.5 (the door and the forms), which is unrelated (SN-5).
  - "Never held over", fixed whatever is ruled, may bind R4's future "declared continuation rule written into the log".
- No precedence among move refusals: assign(door-refused arrival, tick ahead) could be ASSIGN-REFUSED or ASSIGN-AHEAD. END-PENDING vs END-UNDISPOSED are only listed in an order.
- An arrival assigned to a tick that then is NOT-RUN is disposed "assigned to its tick", but its value reaches no record.
- assign lets the host hold an accepted arrival across closes and assign it to a later tick. That reads against "never ... held over" unless the phrase means slots only.
- The end record of a refused session's log is undefined. end() is legal after a refusal, but the only causes are `closed` and `not-run`. Closed or open changes input-log-sha256, and so the receipt.
- Missing dependencies: R4, R3, "identity and bytes", R2/R5.

A8. §15.4 [open: session record, binding]
- Coherent with 15.8: the core holds law-seal, text-seal and input-log-sha256, not the history.
- HISTORY-MISMATCH ("the log is its projection") is undefined while the projection of read-once arrivals and of a refused session is undefined.

A9. §15.5 Input log [open: identity and bytes]
- Missing: the read-once record's syntax, and whether it is present when there are no read-once ports.
- Missing: the spelling of `<port>` in `not-run`.
- Missing: whether t must equal n+1 in `end n not-run t ...`.
- Missing: whether a record's LF is inside the chain hashes. in_0's domain string also repeats the header's first line, and its LF is unstated.
- Missing: an open log whose last line has no LF.
- The load codes (LOG-LINE, -RECORD, -TICK, -END, -UNKNOWN) are named but no condition is mapped to any of them, and they have no order.
- Nothing says whether a load refusal writes a receipt (cf. SPEC §11 G2: "A compile refusal writes no receipt"), with what status and which clause, or whether the log is validated whole or read record by record. 15.7.4's "later records are not read" implies record by record, so ticks 1–4 could run and say their output before LOG-* at record 5.
- The loader's validation of values is unspecified: a hand-made 'T' with non-UTF-8 bytes, a 'B' byte of 2, or an 'I' at a fixed port.
- Missing dependencies: R3 (typed encodings written by the door), A2 (the causes), R5.

A10. §15.6 [open]
- The spelling of `<type>` is unstated (`an integer` or `integer`), and so is the escaping of the name (moot if names are identifiers).
- Missing dependency: R2.

A11. §15.7.1 "binding counts no operation" [open: counting]
- It does not say what an each-tick port's declaration does at its own place: +1 and 'A' like a v0 Let (SPEC §7), or nothing. The answer changes ops, events and T(1).c.

A12. §15.7.2 [open: counting]
- Internal inconsistency. "An If arm's count belongs to the arm's clause" answers what 15.7.3 calls open. SPEC §11 item 18 already settles v0: "An absorbed arm's condition, inline statement and events carry its own clause id."
- Unless TICK-BUDGET is meant to depart from v0, the question is closed.

A13. §15.7.3 Budget [open: budget; sheet R9]
- The count rule is consistent with SPEC G4 and with 15.8 (tick-ops N+1; ops includes the refused operation).
- "N is 0 (no budget)" has two readings: the form without a budget, or a literal `at most 0`. If both are legal, two texts with one meaning could give two law lines (`budget 0` or no budget), and so two seals.
- No code is named for N > 2^62 or for a non-integer N.
- "No budget in the prefix" is implied, not stated.
- The tag omits "counting".

A14. §15.7.5 Four outcomes [open]
- Missing: the status of a LOG-* refusal; a log ending before its read-once record; `not-run` in a tick-only law; and the clause of a REFUSED whose cause is the log.
- The convention "`ticks 0` means a prefix refusal" is implied, not stated.
- Missing dependency: A2.

A15. §15.7.6 domain string [open]
- The receipt's output-chain when no tick began is unstated. I infer out_0 over the prefix output.
- This row is missing from 15.15.

A16. §15.8 tick-ops and the unread count [open]
- tick-ops is undefined when no tick began: a prefix refusal, zero records, or NOT-RUN 1.
- The unread count conflicts with 15.7.4's "later records are not read".
- The tag omits "budget".

A17. §15.9 cut bytes [open: P6]
- Unreadable without SN-3.
- Whether 'R' carries the cut at all is tagged ruled but is not in the ruling (B12).
- A record-time LOG-* refusal, if it is a run refusal, needs a frame too.

A18. §15.10 [open: input-chain]
- Whether `events` and `output-bytes` are per tick or running totals is unsaid; `ops` is said to be the tick's own.
- "These must hold" is untagged, and rests on the open running-total reading.

A19. §15.12.4 PREFIX by static closure [open]
- Ambiguous through "input point" (A1).
- It conflicts with ruled R6's "must stand before the first port declaration" (probe P13).
- It is undefined in a tick-only law.
- "Every consumer of the reachability stating its own soundness requirement" is uninterpretable without SN-1.
- Missing dependencies: 15.1.3 and 15.0's Input point.

A20. §15.13.10 REFERENCE-ONLY [open: D10]
- It conflicts with ruled 15.12.5 (the PREFIX claim "stays held") and 15.12.6 (the PREFIX-wrapped control in a v1 run "must read GROUNDED").
- It also suspends the claims ruling's "E2 is the meaning of HELD for version 1".
- Missing dependencies: R6 and the claims ruling.

A21. §15.14 [open: reporting]
- "Grounded over claims joins the court summary's forbidden interpretations" has no clear reading: a phrase never printed, or a reading never drawn?

A22. §15.15
- Missing rows:
  - 15.7.6;
  - 15.7.1's binding count;
  - whether 'R' carries the cut at all;
  - the unnamed compile codes;
  - the decimal grammar;
  - the untagged 15.0 terms, 15.8 "The core", 15.10 invariants and 15.11 Replay.

==================================================================
3. SECTION B — FAITHFULNESS (ruled clauses)
==================================================================

B1. 15.0 "Version 1 law" [R5]
- R5: "`orlog-law 1`, only when a v1 form appears, so v0 laws stay byte-identical."
- Draft: "a law whose source has a port or a tick block ... every other law keeps orlog-law 0 and its version-0 bytes."
- Faithful. "v1 form = port or tick block" is an inference, consistent with R6's trigger.

B2. 15.1.4 law lines [R5]
- Verbatim. Faithful.

B3. 15.1.6 cost sentence [R6, via R1]
- R6: "the cost of rule a reaches every later claim in the run, stripping them of grounding even if they never touch that property directly."
- Draft: "every claim evaluated after the port is read is stripped of grounding by §15.13, whether or not it reads the property."
- Altered in two ways:
  - "later claim in the run" becomes "evaluated after the port is read". That is an interpretation, and narrower than R6's actual trigger, which is PREFIX.
  - The reference is wrong: it says §15.13 (HELD) where grounding is §15.12.

B4. 15.2 the door [R3]
- Faithful parts:
  - "never rounds" matches "rounding is forbidden";
  - the ASCII sieve before parsing;
  - integer: a fraction refuses;
  - fixed: raw bounds, with the grid refusal naming the two nearest values;
  - truth: one spelling each, case variants and 1/0 refused;
  - text: bytes as sent, with a non-NFC note.
- ADDED under the ruled tag:
  - "a pure function of (declaration, bytes)";
  - "Its version is named in the input log's header";
  - the rule order "the first rule a value breaks";
  - range checked before grid;
  - "recomputable from the bytes";
  - "A later version may relax a refusal into acceptance; the reverse is never allowed (COMPAT-0's rule)". R3 cites COMPAT-0 only as a reason ("reversibility under COMPAT-0 and the preservation of data provenance"), not as this rule.
- OMITTED:
  - R3 says "Raw hexadecimal scalar strings". The draft drops "hexadecimal" and lists the raw spelling as open.
  - R3's adopted common text: "the log holds typed encodings only (RUNTIME-SPEC §5), written once by a Python input door, so no runtime ever parses decimal text". The draft writes "The log holds only values exactly as sent", which loses the Python door and the rule that no runtime parses decimal text, and reads as if the spelling were kept. It is not: "007" and "7", or a raw spelling and a decimal spelling, give one encoding.
- ALTERED:
  - "CP1252 character maps are rejected outright" becomes INPUT-NOT-UTF8. That is narrower: mojibake that is valid UTF-8 passes.
- INCOHERENT, both in the ruling and in the draft:
  - Rule 1, "must match the port type's ASCII grammar" (R3: "filters all incoming port streams using a restrictive ASCII regular expression sieve"), versus text ports that keep UTF-8 bytes. Since rule 1 comes first, non-UTF-8 text is INPUT-SYNTAX and INPUT-NOT-UTF8 is dead, unless text's "grammar" is not ASCII.
  - INPUT-NOT-INTEGER is reachable only if the integer grammar admits a decimal point.

B5. 15.3 last bullet [R4]
- R4: "A refusal ends its branch at tick t. ... The refused branch is kept, sealed and queryable. The court reads each branch on its own and names every abandoned branch. Automatic continuation waits for SNAP-1; until then a refusal ends the session."
- Draft: "Until SNAP-1, a refusal ends the session. A refusal ends its branch at the tick. The refused branch is kept, sealed and queryable."
- OMITS "The court reads each branch on its own and names every abandoned branch". It appears nowhere in §15, not in 15.12 or 15.13.
- Leaving out the continuation mechanism is fine, since it waits for SNAP-1.
- "a refusal" is left unscoped (A7).

B6. 15.3 "[fixed: R4 and the draft's §1.5]"
- "No value is ever invented, held over or defaulted. A tick that does not run stops every port of it, and the session." R4 says neither sentence. Attributing them to R4 adds.

B7. 15.7.1 [R5]
- R5: "Each tick emits 'T', then one 'N' per each-tick port in declaration order, then the body. The read-once ports' 'N' events come before the first 'T'."
- Faithful. It adds "binds where its declaration stands", which is consistent but not in R5, and "then stops".

B8. 15.7.2 [R5 amendment 1]
- "(t, c), both u64" is faithful.
- The note "R5 left a reading open" rests on text the reading set excludes ("the record's notes on amendment 1's reading of c").

B9. 15.7.4 [R4]
- "A refusal of any code ends the run at once" is faithful.
- "later records are not read" is added, and conflicts with 15.8's unread count.

B10. 15.7.6 [R5 amendment 2]
- out_t and the refused tick's partial output as the last link are faithful.
- His out_0 words: "the initial hash of any visual bytes or metadata written before the first tick". The draft uses "the bytes said", which drops "or metadata". This is minor, and flagged as a QUESTION.

B11. 15.8 [R5]
- The line set is faithful: ticks, input-log-sha256, and output-chain replacing output-sha256.
- The line order is the draft's.
- `ticks` matches amendment 3, plus "a not-run tick not", an extension to the open NOT-RUN status.
- The frame check is faithful to amendment 4 and to "orlog-law 0 demands orlog-receipt 0 ...". The plants are stated faithfully.

B12. 15.9 [R5; claims]
- The head, 'N''s payload and the kept per-event chain are faithful ("We keep the per-event chain exactly as written").
- "The 'R' event carries the refusal cut [ruled: claims]" is NOT in the claims ruling. The ruling admits "the meet ... pinned to the exact CUT-0 digest, with each withholding identifying its structural row" and says nothing of the trace.
- Changing v1's 'R' payload also goes beyond R5, whose new events are 'T' and 'N'.
- Added. Needs a ruling.

B13. 15.10 [R5, part of 1a]
- The fields are faithful (R5: tick, events, ops, output bytes, trace head or `-`, output chain, a claims digest, a state digest).
- Added under the ruled tag: the definitions of the claims and state digests ("claim lines as they would read at the tick's end"; "every top-level variable's value encoding") and "written by an execution given a path".

B14. 15.12 [R6]
- 1: The trigger is faithful. "the log's length sets how many ticks run" is an added inference.
- 2: Faithful.
- 3: Faithful, from R6's row plus "must print exactly the input-log-sha256 value".
- 4: ALTERED.
  - R6: "The licence, PREFIX, decided from the text: a claim is exempt only if every evaluation of it precedes the first input. It must stand before the first port declaration, outside the tick block. It must not sit in a procedure performed at or after the first port declaration. The licence is decided by evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still runs during it."
  - The draft drops "decided from the text". Without it, "decided by evaluation" can be read as a runtime observation.
  - The draft changes "must stand" / "must not sit" to the indicative "stands" / "is not".
  - It drops the sentence that the prefix claim's "whole claim line is fixed by the law".
  - It drops the wider licence that "waits for a trigger". That sentence signals that a no-path-from-port licence is not in v1.
- 5: NARROWED. R6: "regardless of whether the execution loop encounters a subsequent transactional refusal downstream". The draft writes "when the run is later refused at a tick", which drops a later prefix refusal. "historically held" becomes "stays held"; with 15.13's E2 meaning of HELD, that may not be the same word.
- 6: GENERALIZED. R6: "Every row testing an ungrounded port violation must run with the witness explicitly configured as agreed". The draft writes "each runs with its witness configured as agreed". The control's GROUNDED is faithful.

B15. 15.13 [claims]
- 1: Faithful to E2, word for word.
- 2: Faithful.
- 3: Adds "stays in every reading". The ruling says only "remains descriptive evidence".
- 4: Faithful on the meet, the digest, and "does not prove it sound". It omits "CUT-0 alone remains the target for further development".
- 9: Faithful on T10 and T11 staying open, but it omits:
  - "The While next-pass row is the priority";
  - "establishes neither compatibility preservation nor general soundness";
  - "Releasing claims whose truth cannot change would require a separate, stronger invariance rule; that is not part of this version 1 ruling."
- 5–8 and 11: The content (the court's R8 definition, the cut, the K̂ rows, the row names, UNREACHED) is NOT in the claims ruling. The ruling names R8 and CUT-0 only by name and pinned digest. Labelling these clauses "ruled" makes the twin read them as settled; at most, they are fixed by the digest (SN-4).

==================================================================
4. SECTION C — FIXED CLAUSES
==================================================================

C1. 15.1.2: "spelled only where version 0 refuses SYNTAX; no word newly reserved"
- Consistent with SPEC §2 and §13 for the proposed spellings (A2).
- Caveat: "at the statement" assumes the v0 refusal of such a text is SYNTAX. Within a clause, LEX comes first (SPEC §13 phase 3), but these forms lex cleanly.
- `tick`, `operations` and `given each tick` used as identifiers: `Let tick be 1.` stays v0 and legal.

C2. 15.3: "No value is ever invented, held over or defaulted ..."
- Consistent with close()'s NOT-RUN rule.
- It may constrain R4's declared continuation rule (A7).
- Its tag cites an unresolvable "§1.5".

C3. 15.8: "No receipt line states that a run is valid or correct"
- Consistent with SPEC and RUNTIME-SPEC: status words name outcomes.

C4. 15.11, second bullet
- Consistent.
- The untagged first bullet (Replay) is inconsistent with:
  - 15.10, which allows trace-head `-` "in a play build", so tick lines differ by build;
  - SPEC §12's STOPPED-BY-HOST, where the host's budget decides whether any receipt exists at all, which is a difference under the same three inputs that is not a defect.

==================================================================
5. SECTION D — T10.0 TO T10.7 (nothing here is proved)
==================================================================

T10.0
- "T10 holds when ..." cannot be checked against T10 itself (SN-9).
- "Every statement kind" must now include the port declaration, the tick block, and a record-time LOG-* refusal if that is a run refusal. None of these has a row.
- "The cut records the frames exactly" cannot yet be stated for v1: the tick block's and the ports' frames are not derived (15.9).
- "(and T10.7 from version 1)" omits that T10.5 also has a v1-only part.
- Unstated assumptions:
  - Expressions and rules contain no claim and no Perform. This is true by SPEC §4/§6.
  - No +1 can refuse in v0, so a refusal at a Perform's own operation is TICK-BUDGET only.

Across all rows
- The continuation semantics the rows quantify over ("passable refusal", "values ignored", S2) is not defined in the set.
- Nothing says whether E2's "continuation" is relative to the law (any further input) or to the session, which ends at NOT-RUN and, until SNAP-1, at any refusal. T10.7's "since another tick may run" needs the first reading. Under the second, nothing may run after NOT-RUN.

T10.1
- Sound as an over-approximation.
- It should state that "the owning frame" of a procedure body is the dynamic Perform frame, never the To clause's textual siblings.
- "Transitively" is stated only in T10.5 and after 15.13.7's list.

T10.2
- MISSING CASE: an If on top refused in an arm's inline statement whose condition was true. T10.2 covers only "a condition refused at arm i".
- 15.13.7's "a refused If" is broader and would include later arms, which is sound but imprecise. The two scopes differ.

T10.3
- "ESTABLISHED, interp.py's For" grades a premise by an implementation. SPEC §7's For row supports it too ("evaluate lo, then hi" once).
- "Exactly when its bit says passes remain" also relies on the read-only counter (SPEC §5, LOOP-VARIABLE). That should be named.

T10.4
- No gap. Always repeating is sound and coarse.

T10.5
- INVALID INFERENCE: "returns only to the frame below ... since there is no recursion". Returning to the caller holds on any call stack. What the absence of recursion supplies is at most one frame per procedure, which matters for the static slots and for an unambiguous cut.

T10.6
- "Open" is undefined for a claim refused at its own +1 (TICK-BUDGET) before s = ops.
- If that claim is not "open", CUT-0 alone misses it as a row. In v1 the tick-block row masks the miss, and R8 catches it in the meet.

T10.7
- It depends on open 15.1.3 (the tick block is last). If that were relaxed, a rest-of-block after the tick block would be needed.
- The tick block on top (a refusal at 'T' or 'N' time, e.g. LOG-* while streaming) is not covered.
- NOT-RUN in a law with ports but no tick block has no "tick block's head".

Does 15.13.7 match T10? Row for row, yes, with these differences:
- the refused-If scope (above);
- 15.13.7 gives no explicit "a simple statement on top" or "If below the top" row (both are covered by the rest-of-block row via "the owning frame");
- 15.13.7 does not define the cut at COMPLETED;
- 15.13.8 does not say which row is named when two withhold one claim.

==================================================================
6. SECTION E — TWO QUESTIONS (findings, not rulings)
==================================================================

E(i). Do `status REFUSED <CODE> <clause>` and `ticks <n>` give the "code, clause and tick"?

FIRST FINDING: the quoted words are not in RULINGS-AS-RULED.md's R4. R4's decision and ruling text say only "at tick granularity" and "A refusal ends its branch at tick t". If the words come from option a's row, that row is excluded "which the adopted ruling text replaces", so it is not in force as this set presents R4 (SN-6). The nearest ruled text is R5 amendment 3: "a refused tick writes no per-tick line; its record is the receipt's status and the trace's 'R' event".

Readings:
- (A) The receipt as a whole states them. `ticks` counts the ticks begun, the refused one included, so in a tick refusal `ticks` = t. A prefix refusal gives `ticks 0`, read as "the prefix" by convention. On this reading the pair satisfies the requirement, as long as:
  - the convention "0 = prefix" is stated (it is implied, not stated);
  - no refusal can fall between ticks. A record-time LOG-* refusal makes "begun" unclear.
- (B) "Say" requires an explicit field naming the tick. A count equals the tick only by inference, so the pair is not enough, and a `tick <t>` field or a status field would be needed.
- (C) The trace's 'R' event, preceded by its 'T', gives the tick, and R5 amendment 3 names it as part of the record.

The draft selects (A) explicitly: 15.7.5, "The tick is the receipt's `ticks` (§15.8)". Whether (A) satisfies R4 cannot be judged without SN-6.

E(ii). Does the "port place" rule forbid reading only each-tick ports outside the tick block, or any port?

Literal text: "A read of an each-tick port outside the tick block is refused at compile time."
- Reading (a), each-tick only, is the text. Read-once ports may be read anywhere after their declaration. Probe P19 is accepted.
- Reading (b), any port, has no textual support. It would forbid read-once ports in the prefix, which 15.1.6's world-property proposal needs.

The draft selects (a) on the port-kind axis. It does NOT select on the place axis: whether "outside" is textual (procedures and Defines can never read an each-tick port) or by evaluation (P18).
- Under the evaluation reading, a procedure performed from both the prefix and the tick block needs a rule.
- Under either reading, the refusal has no named code (PORT-PLACE names a declaration).

==================================================================
7. SECTION F — HAND-WORKED PROBES (all UNEXECUTED)
==================================================================

Conventions:
- Labels are `1.` and `1.1.`, and clause ids are in document order.
- Every probe uses the open spellings of 15.1.1 (R2). Every probe that prints ops assumes the open "counting" readings: c is the running total, binding counts 0, and the tick block counts 0.
- Unless stated otherwise, a log has a header and an (unspecified) read-once record. "Undetermined" marks a finding, not a guess.
- Values are hex of the RUNTIME-SPEC §5 encodings: Int 3 = 490000000000000003; Fix 1.5 = 580000000180000000; Int 0 = 490000000000000000.

P01 COMPLETED, tick-only law
- Law:
  - `1. Let n be 0.`
  - `2. Each tick, do the following.`
  - `2.1. Increase n by 1.`
  - `2.2. Say n.`
- Log: `t 1`, `t 2`, `end 2 closed`.
- Run:
  - ops: prefix 1, so 'T'(1,1).
  - Tick 1: Increase 2, Say 1, so 3 own.
  - 'T'(2,4). Tick 2: 3 own.
- Receipt: COMPLETED; ticks 2; tick-ops 3; ops 7; events 7 (A,T,A,S,T,A,S); output "1\n2\n" (4 bytes).
- Tick lines: ops 3 and 3. Invariants: 4−1=3; T(1).c=1=prefix; 7−4=3=tick-ops.
- Header `orlog-law 1`.
- Open dependencies: R2, counting, the read-once record (absent?).
- Clauses: 15.0, 15.7.1–2, 15.8, 15.10.

P02 LOG-OPEN
- Law: P01's. Log: header + `t 1`, no end record.
- Expected: LOG-OPEN; ticks 1; tick-ops 3; ops 4.
- Clauses: 15.5 (open log), 15.7.5. Depends on "four statuses".

P03 not-run in a tick-only law
- Law: P01's. Log: `t 1`, `end 1 not-run 2 INPUT-MISSING x`.
- No port exists, and close() can never NOT-RUN, so the outcome is UNDETERMINED: LOG-END? NOT-RUN? (F56)

P04 NOT-RUN with a door refusal
- Law:
  - `1. Let thrust be given each tick as a fixed.`
  - `2. Let v be 0.0.`
  - `3. Each tick, do the following.`
  - `3.1. Increase v by thrust.`
  - `3.2. Say v.`
- Session:
  - arrive(thrust,s,"1.5") accepted; assign(a1,1); close() runs tick 1.
  - arrive(thrust,s,"0.1") gives INPUT-GRID, naming raw 429496729 and 429496730 (×2^-32). The spelling of those two values is undetermined.
  - close() gives NOT-RUN 2 INPUT-MISSING thrust, and the session ends.
- Log: `t 1 580000000180000000`, `end 1 not-run 2 INPUT-MISSING thrust`.
- Run: assuming the each-tick declaration does nothing at its place (UNDETERMINED, F30), ops are prefix 1, 'T'(1,1), N, Increase 2, Say 1.
- Receipt: `status NOT-RUN 2 INPUT-MISSING thrust`; ticks 1; tick-ops 3; ops 4; events 5 (A,T,N,A,S); output "1.5\n".
- Variable ids: thrust 0, v 1 (assumed).
- Dispositions: a1 assigned; a2 refused INPUT-GRID.
- Depends on A2 and "identity and bytes". Clauses: 15.2.3, 15.3, 15.5, 15.7.5.

P05 END-PENDING / END-UNDISPOSED
- P04's law. arrive a1 accepted, assign(a1,1), end() gives END-PENDING.
- Separately: arrive a1 accepted, end() gives END-UNDISPOSED.
- Both at once: the order is UNDETERMINED (F12).
- Does a refused move end the session? UNDETERMINED (F11).

P06 move refusals
- P04's law, open tick 2.
- assign(a, 1) gives ASSIGN-CLOSED. assign(a, 3) gives ASSIGN-AHEAD. assign(refused arrival) gives ASSIGN-REFUSED. A second assign of a gives DISPOSED-TWICE. A second arrival assigned to tick 2's filled slot gives SLOT-FILLED.
- arrive(nosuch,...) gives UNKNOWN-PORT. assign(99,...) gives NO-ARRIVAL. Any move after end gives AFTER-END. A move other than end after a run refusal gives RUN-REFUSED.
- assign(refused arrival, 3): ASSIGN-REFUSED or ASSIGN-AHEAD is UNDETERMINED.

P07 TICK-BUDGET at a Say
- Law: P01 with `2. Each tick, at most 2 operations, do the following.`
- Tick 1: Increase makes the count 2; Say's +1 makes it 3 = N+1, refused.
- Expected: `REFUSED TICK-BUDGET 4`; ticks 1; tick-ops 3; ops 4; events 4 (A,T,A,R); output-bytes 0; out_1 = SHA(out_0 ‖ SHA("")). No tick line.
- With N=3 instead: COMPLETED.
- Depends on "budget". Clauses: 15.7.3, 15.8.

P08 TICK-BUDGET at an absorbed arm (the open clause question)
- Law:
  - `1. Let n be 0.`
  - `2. Each tick, at most 2 operations, do the following.`
  - `2.1. If n = 1, say 1.`
  - `2.2. Otherwise, if n = 0, say 0.`
- Arm 1: +1, compare +1, so count 2. Arm 2's +1 makes 3, refused.
- Clause: 4 by SPEC §11 item 18 and 15.7.2; 3 by 15.7.3's alternative. UNDETERMINED by the draft (F26).
- ticks 1; tick-ops 3; ops 4.
- Cut: the If on top, named by arm 2. K̂ is arm 2 onward.

P09 tick block's next tick, R6 provenance
- Law:
  - `1. Let n be 0.`
  - `2. Each tick, do the following.`
  - `2.1. Increase n by 1.`
  - `2.2. We claim that n is positive.`
  - `2.3. If n = 2, do the following.`
  - `2.3.1. Say 1 divided by 0.`
- Log: t 1, t 2, end 2 closed.
- ops:
  - prefix 1; tick 1 is 6 own (Increase 2, claim 2, If 2); 'T'(2,7);
  - tick 2: Increase 9, claim 11, If 13, Say +1 14, divide +1 15, DIVISION-BY-ZERO.
- Receipt: `REFUSED DIVISION-BY-ZERO 6`; ticks 2; tick-ops 8; ops 15; events 8; `claim 0 4 2 2 2 0 0`. One tick line (tick 1, ops 6). Unread 0.
- Court:
  - not GROUNDED (not PREFIX); line `rests on input log <input-log-sha256>, unratified`;
  - R8 holds (the refusal is at 6, not 4);
  - CUT-0 cut [tick block, If 5 arm 1, Say 6]; K̂ via "the tick block's next tick" includes clause 4, so withheld, row "the tick block's next tick";
  - meet: withheld; "true in 2 of 2" descriptive;
  - under the open D10: REFERENCE-ONLY.

P10 open claim, TICK-BUDGET inside the condition
- Law:
  - `1. Let n be 5.`
  - `2. Each tick, at most 2 operations, do the following.`
  - `2.1. We claim that n plus 1 is greater than 0.`
- claim +1 (1), plus +1 (2), compare +1 (3), refused.
- Receipt: `REFUSED TICK-BUDGET 3`; tick-ops 3; ops 4; `claim 0 3 0 0 0 0 0`.
- Court: R8 does not hold (the claim's clause, code ≠ CLAIM-REFUTED). CUT-0: the open claim.
- Standing: UNREACHED (no completed evaluation, 15.13.11) or withheld (open claim / R8)? UNDETERMINED (F44).

P11 claim refused at its own +1
- Law: `2. Each tick, at most 1 operations, ...`, then `2.1. Say n.` and `2.2. We claim that n is positive.`
- Say makes count 1; the claim's +1 makes 2, refused at clause 4 before s = ops.
- R8 withholds. CUT-0: "open"? UNDETERMINED (F40). The tick-block row withholds it anyway.

P12 PREFIX held after a tick refusal
- Law:
  - `1. We claim that 2 plus 2 equals 4.`
  - `2. Let thrust be given each tick as an integer.`
  - `3. Each tick, do the following.`
  - `3.1. Say 10 divided by thrust.`
- Log: `t 1 490000000000000000`.
- ops: claim 3 (cost 2); 'T'(1,3); Say 4; divide 5, DIVISION-BY-ZERO.
- Receipt: `REFUSED DIVISION-BY-ZERO 4`; ticks 1; tick-ops 2; ops 5; `claim 0 1 1 1 2 0 0`.
- Court:
  - PREFIX-exempt, so GROUNDED (if its channel grounds);
  - R8 holds; CUT-0 holds (clause 1 is not in K̂ = clause 4); meet: held;
  - 15.12.5 says it stays held. Under the open 15.13.10 it is not held. CONFLICT (F24).
- Whether the provenance line is printed for this claim is UNDETERMINED (F47).

P13 claim after a port declaration, before the first read (PREFIX)
- Law:
  - `1. Let thrust be given each tick as an integer.`
  - `2. We claim that 1 is positive.`
  - `3. Each tick, do the following.`
  - `3.1. Say thrust.`
- Ruled R6: not exempt (after the first port declaration), so not GROUNDED, with the provenance line.
- Open proposal with 15.0's Input point (the first read is at 3.1 in tick 1): exempt, so GROUNDED.
- The two contradict (F3).
- HELD by the meet, apart from grounding.

P14 procedure performed before and after the port
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Perform check.`
  - `3. Let thrust be given each tick as an integer.`
  - `4. Each tick, do the following.`
  - `4.1. Perform check.`
  - `4.2. Say thrust.`
- Not exempt (performed at 4.1, after the first port declaration), so not GROUNDED.
- At LOG-OPEN: K̂ = the tick block and procedures performed from it, so withheld, row "the tick block's next tick".
- At COMPLETED: the cut is undefined (F46). I infer held.
- Variant without 4.1: exempt.

P15 tick-only law, procedure performed only from the tick block
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Each tick, do the following.`
  - `2.1. Perform check.`
- The position conditions are vacuous (no port declaration), but every evaluation follows the first input (tick 1).
- Exempt? UNDETERMINED (F4, F5).

P16 read-once world property, no tick block
- Law:
  - `1. We claim that 3 is odd.`
  - `2. Let gravity be given as a fixed.`
  - `3. We claim that 4 is even.`
  - `4. Say gravity.`
- Log: the read-once record (syntax unspecified), `end 0 closed`.
- Expected: COMPLETED; ticks 0; tick-ops UNDETERMINED; N event at clause 2's place, no 'T'.
- Claim 0: GROUNDED (PREFIX). Claim 1: not GROUNDED, though it never reads gravity (15.1.6's cost; the draft cites §15.13 wrongly).
- Whether a law without a tick block may have tick records or call close() is UNDETERMINED (F7).

P17 each-tick read in the prefix
- Law: `1. Let thrust be given each tick as an integer.`, `2. Say thrust.`, `3. Each tick, do the following.`, `3.1. Say 1.`
- A compile refusal (15.1.3), so no receipt (G2).
- The code and phase are UNDETERMINED (F27).

P18 each-tick read in a procedure performed only from the tick block
- Law: `1. Let thrust be given each tick as an integer.`, `2. To show, do the following.`, `2.1. Say thrust.`, `3. Each tick, do the following.`, `3.1. Perform show.`
- Textual reading: refused. Evaluation reading: accepted. UNDETERMINED (F28, E(ii)).

P19 read-once read in the prefix and the tick block
- Law: `1. Let g be given as an integer.`, `2. Say g.`, `3. Each tick, do the following.`, `3.1. Say g.`
- Accepted by the literal text. Reading E(ii)(b) would refuse clause 2.

P20 PORT-VARIABLE
- `1. Let g be given as an integer.` then `2. Set g to 3.` gives PORT-VARIABLE (phase undetermined).
- `2. Append 1 to g.`: PORT-VARIABLE or TYPE, UNDETERMINED (F58).

P21 places
- `1. If true, do the following.` with `1.1. Let g be given as an integer.` gives PORT-PLACE.
- `1. Each tick, do the following.`, `1.1. Say 1.`, `2. Let g be given as an integer.`: PORT-PLACE or TICK-PLACE, UNDETERMINED.
- Two tick blocks give TICK-PLACE, at clause 1 or at the second, UNDETERMINED.
- `If true, let g be given as an integer.` (inline): PORT-PLACE or SYNTAX, UNDETERMINED (F57).

P22 budget bounds
- `at most 0 operations`: no budget? Is the law line `budget 0` or omitted? UNDETERMINED (F29).
- `at most 4611686018427387905 operations` (2^62+1): a compile refusal, code unnamed.
- `at most 2.5 operations`: SYNTAX by analogy with SPEC §11 item 19, not stated.

P23 door, integer port
- "12": accept.
- "9223372036854775808": INPUT-RANGE. "-9223372036854775808": accept.
- "12.0": INPUT-NOT-INTEGER or INPUT-SYNTAX (rule 1), UNDETERMINED (F14).
- " 12", "+12", "012", "-0": UNDETERMINED (F15).

P24 door, fixed port
- "0.5": accept (raw 2^31).
- "0.1": INPUT-GRID (neighbours 429496729 and 429496730 raw).
- "-2147483648": accept (raw −2^63).
- "2147483647.99999999976716935634613037109375": accept (raw 2^63−1).
- "2147483648": INPUT-RANGE.
- "-2147483648.5": INPUT-RANGE (R3's named boundary).
- "2147483648.1": INPUT-RANGE (range before grid).
- A raw spelling: UNDETERMINED (open prefix; R3 says hexadecimal).

P25 door, truth and text ports
- Truth: case variants and "1"/"0" give INPUT-SYNTAX. The spellings are open.
- Text:
  - "caf\xC3\xA9": accept.
  - NFD "cafe\xCC\x81": accept with a note.
  - a lone "\xE9": INPUT-NOT-UTF8 (rule 5) or INPUT-SYNTAX (rule 1 first). UNDETERMINED (F13).
  - "\xE2\x80\xAE" (bidi): open.

P26 log grammar
- Header ports hash ≠ the law's: PORT-SIGNATURE. Receipt or none: UNDETERMINED (F8).
- First record `t 2`: LOG-TICK? `t 1 ` with a trailing space and no each-tick port: LOG-RECORD or LOG-LINE?
- CRLF: LOG-LINE? A byte 0xC3: LOG-NOT-ASCII. A line after `end`: LOG-AFTER-END. `x 1`: LOG-UNKNOWN? `end 2 closed` over 3 records: LOG-END?
- `end 1 not-run 3 ...`: UNDETERMINED.
- An 'I' value at a fixed port: UNDETERMINED (F36).
- Code mapping UNDETERMINED except where the name is self-evident (F8).
- Malformed record 3 while the run refuses at tick 2: REFUSED <run code> (15.7.4) or LOG-* (if validated whole), UNDETERMINED. Does the unread count include record 3? UNDETERMINED (F9).

P27 NOT-RUN with two ports
- Law:
  - `1. Let a be given each tick as an integer.`
  - `2. Let b be given each tick as an integer.`
  - `3. Each tick, do the following.`
  - `3.1. Say a plus b.`
- Session: arrive(b,"1"), assign(·,1), close().
- Expected: NOT-RUN 1 INPUT-MISSING a (the first missing in declaration order); ticks 0; ops 0; tick-ops UNDETERMINED.
- b's arrival is disposed "assigned" but appears in no record (F54).

P28 prefix refusal
- Law: `1. Let thrust be given each tick as an integer.`, `2. Say 1 divided by 0.`, `3. Each tick, ...`
- Expected: `REFUSED DIVISION-BY-ZERO 2`; ticks 0; ops 2; output-chain = out_0 (inferred).
- Unread count: all n records ("not read" yet counted?). Does the log header load before the prefix (PORT-SIGNATURE first)? UNDETERMINED.

P29 For row, both ways
- Law (a):
  - `1. For each i from 1 to 3, do the following.`
  - `1.1. We claim that i is positive.`
  - `1.2. Say 10 divided by (2 minus i).`
  - `2. Each tick, do the following.`
  - `2.1. Say 1.`
- Pass 2 refuses at clause 3 with passes remaining, so the bit is set and the claim is withheld, row "a For's next pass". PREFIX-exempt, so GROUNDED but not HELD.
- Law (b): "from 1 to 2".
  - The refusal is in the last pass, so no bit. K̂ = the tick block only. CUT-0 holds, R8 holds: held. GROUNDED.
  - ops 13; `claim 0 2 2 2 2 0 0`; output "10\n"; `REFUSED DIVISION-BY-ZERO 3`; ticks 0.

P30 While row
- Law:
  - `1. Let k be 0.`
  - `2. While k < 5, at most 10 times, do the following.`
  - `2.1. Increase k by 1.`
  - `2.2. We claim that k is positive.`
  - `2.3. If k = 5, do the following.`
  - `2.3.1. Say 1 divided by 0.`
  - `3. Each tick, do the following.`
  - `3.1. Say k.`
- Refused at 6. The While is below the top, so the body is in K̂ always (S2). Withheld, row "a While's next pass", though k=5 would end the loop.
- `REFUSED DIVISION-BY-ZERO 6`; ticks 0.

P31 refused-If row
- Law:
  - `1. For each i from 1 to 2, do the following.`
  - `1.1. If i = 3, say 0.`
  - `1.2. Otherwise, if 6 divided by (2 minus i) = 0, do the following.`
  - `1.2.1. Say 6.`
  - `1.3. Otherwise, do the following.`
  - `1.3.1. We claim that i is positive.`
  - `2. Each tick, do the following.`
  - `2.1. Say 1.`
- Pass 1 takes the Otherwise: the claim is true. Pass 2 refuses at the arm-2 condition, clause 3.
- Cut [For (no passes remain), If arm 2]. K̂ = arm 2 onward plus the Otherwise, so withheld, row "the refused If's arms onward". GROUNDED (PREFIX). `REFUSED DIVISION-BY-ZERO 3`.

P32 Perform rows
- Law:
  - `1. To probe, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Each tick, at most 3 operations, do the following.`
  - `2.1. Perform probe.`
  - `2.2. Perform probe.`
- Perform 1, claim 3 (true), then Perform 2.2's +1 makes 4, refused.
- `REFUSED TICK-BUDGET 5`; ticks 1; tick-ops 4; ops 4; `claim 0 2 1 1 1 0 0`.
- R8 holds. CUT-0: "a Perform refused" AND "the tick block's next tick" both withhold. Which row is named? UNDETERMINED (F45).

P33 rest-of-block row
- Law:
  - `1. To check, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Perform check.`
  - `3. Say 1 divided by 0.`
  - `4. Perform check.`
  - `5. Each tick, do the following.`
  - `5.1. Say 1.`
- Refused at clause 4. The rest of the block includes Perform at clause 5, so the claim is withheld, row "the rest of a block".
- PREFIX: no port, outside the tick block, every evaluation before any input, so GROUNDED but not HELD. `REFUSED DIVISION-BY-ZERO 4`.

P34 R8, inline shared clause
- Law:
  - `1. Let x be 2.`
  - `2. Each tick, do the following.`
  - `2.1. Decrease x by 1.`
  - `2.2. If 1 divided by x = 1, we claim that x = 1; otherwise we claim that x is positive.`
- Tick 1: claim 0 is true. Tick 2: x=0, DIVISION-BY-ZERO at clause 4.
- R8 withholds claim 0 (a shared clause). CUT-0: the If on top, arm 1 onward, plus the tick block. Claim 1: UNREACHED.

P35 LOG-OPEN with zero ticks
- Law: `1. We claim that 1 is positive.`, `2. Let a be given each tick as an integer.`, `3. Each tick, do the following.`, `3.1. Say a.`
- Open log, header only.
- Expected: LOG-OPEN; ticks 0; tick-ops UNDETERMINED.
- Claim: GROUNDED (PREFIX). The cut is the tick block's head before tick 1, so it is not in K̂: held by the meet. Not held under the open D10.

P36 refused session's log
- P09 run live. After the refusal: arrive gives RUN-REFUSED; end() is legal.
- Is the log's end record `closed`, absent (open), or other? UNDETERMINED. input-log-sha256 and the provenance line differ by reading. Status REFUSED either way (F10).

P37 frame check and v0 stability
- A v1 law with an `orlog-receipt 0` receipt: the frame check fails. A v0 law with `orlog-receipt 1`: refused.
- `1. Let tick be 1.` stays an `orlog-law 0` law with v0 bytes.
- `1. Each tick, do the following.` in v0 is SYNTAX.

P38 arrival held across ticks
- P04's law: arrive a1, arrive a2, assign(a2,1), close(), assign(a1,2), close(). Legal by the table.
- An arrival is held over by the host (F55).

==================================================================
8. FINDINGS (numbered; tag; severity)
==================================================================
1. QUESTION — "code, clause and tick" is not in R4 as ruled; if it is from option a's row, that row is excluded as replaced — needs a ruling.
2. FAITHFULNESS — 15.12.4 drops R6's "decided from the text" and weakens "must stand / must not sit" — blocks the round.
3. COHERENCE — The open PREFIX-by-closure proposal, with 15.0's Input point, exempts claims after the first port declaration, wider than ruled R6 — blocks the round.
4. GAP — PREFIX in a tick-only law: the position conditions are vacuous and "first input" is undefined — needs a ruling.
5. QUESTION — R6's licence gives only necessary conditions ("only if"); neither text says when a claim IS exempt — needs a ruling.
6. GAP — Read-once ports: no session event, no log-record syntax, no NOT-RUN, no rule for when the prefix runs — blocks the round.
7. GAP — Laws with ports but no tick block (or each-tick ports without one): tick records, close() and execution undefined — needs a ruling.
8. GAP — LOG-* codes have no conditions or order; whether a load refusal writes a receipt, and whether the log is streamed or validated whole, is unsaid — blocks the round.
9. COHERENCE — "later records are not read" (15.7.4) vs the receipt's count of records "left unread" (15.8) — needs a ruling.
10. GAP — The end record of a refused session's log (closed/open/cause) is undefined; it changes input-log-sha256 — needs a ruling.
11. COHERENCE — "a refusal ends the session" covers run, door and move refusals; the retry rule needs door refusals not to — needs a ruling.
12. GAP — No precedence among session move refusals (ASSIGN-REFUSED vs ASSIGN-AHEAD; END-PENDING vs END-UNDISPOSED) — minor.
13. COHERENCE — Door rule 1 (ASCII grammar first) vs text's UTF-8 bytes; INPUT-NOT-UTF8 is dead; the same tension is in R3 — needs a ruling.
14. COHERENCE — INPUT-NOT-INTEGER is reachable only if the integer grammar admits decimals — minor.
15. GAP — The integer and decimal ASCII grammars are neither given nor tagged open — needs a ruling.
16. FAITHFULNESS — Omits that R3's raw values are hexadecimal — minor.
17. FAITHFULNESS — "values exactly as sent" replaces R3's "typed encodings only ... written once by a Python input door, so no runtime ever parses decimal text" — needs a ruling.
18. FAITHFULNESS — "CP1252 maps rejected outright" narrowed to INPUT-NOT-UTF8 — minor.
19. FAITHFULNESS — Under [ruled: R3], adds the pure function, the door version in the header, the rule order, range before grid, and turns COMPAT-0 (a reason) into a rule — minor.
20. FAITHFULNESS — "'R' carries the cut" is tagged ruled: claims but is not in the ruling, and goes beyond R5's event set — needs a ruling.
21. FAITHFULNESS — 15.13.5–8 and 11 (the R8 definition, CUT-0's rows, UNREACHED) are tagged ruled but are absent from the ruling — needs a ruling.
22. FAITHFULNESS — R4's "court reads each branch on its own and names every abandoned branch" is omitted from §15 — needs a ruling.
23. FAITHFULNESS — 15.12.5 narrows "subsequent ... refusal downstream" to "at a tick"; "historically held" becomes "held" — minor.
24. COHERENCE — The open D10 REFERENCE-ONLY contradicts ruled 15.12.5 and 15.12.6's PREFIX control "must read GROUNDED" — blocks the round.
25. FAITHFULNESS — 15.1.6 cites §15.13 for grounding and rewrites "every later claim" — minor.
26. COHERENCE — 15.7.3's open clause question is answered by SPEC §11 item 18 and by 15.7.2's own proposal — minor.
27. GAP — No code for an each-tick read outside the tick block or for N>2^62; no phase or order for PORT-PLACE, TICK-PLACE and PORT-VARIABLE — needs a ruling.
28. COHERENCE — "outside the tick block": textual vs by evaluation (procedures, Defines) — needs a ruling.
29. GAP — Budget 0: a legal spelling? The law line's budget 0 or omitted (two seals for one meaning) — minor.
30. GAP — What an each-tick port's declaration does at its place (+1, 'A' or nothing) — needs a ruling.
31. GAP — tick-ops when no tick began — minor.
32. GAP — Tick line `events` and `output-bytes`: per tick or cumulative — minor.
33. FIXED — The untagged 15.11 Replay vs 15.10's `-` play build and SPEC §12's STOPPED-BY-HOST — minor.
34. GAP — Untagged normative clauses: the 15.0 terms, 15.8 "core", 15.10 invariants, 15.11 Replay — minor.
35. GAP — 15.5's details: the read-once record, `<port>` spelling, t=n+1, LF in the chain hashes, the doubled domain string, a partial last line — needs a ruling.
36. GAP — The loader's validation of value encodings against port types and door rules — needs a ruling.
37. GAP — 15.6: the source of `"<name>"` in the forms, and the `<type>` spelling — minor.
38. FIXED — 15.3's "[fixed: R4 and the draft's §1.5]" cites an unresolvable §1.5, and may bind R4's continuation rule — needs a ruling.
39. T10 — The refused-If row and T10.2 omit (or over-include) a refusal in a true arm's inline statement — needs a ruling.
40. T10 — "Open" is undefined for a claim refused at its own +1 before evaluation — minor.
41. T10 — The continuation semantics (passable refusal, values ignored, S2) and its scope (law vs session) are undefined in the set — needs a ruling.
42. T10 — T10.5's "since there is no recursion" does not support "returns only to the frame below" — minor.
43. T10 — T10.7 depends on open 15.1.3; the tick block on top, ports and a record-time refusal have no row (T10.0 "every statement kind") — needs a ruling.
44. COHERENCE — UNREACHED vs withheld for a claim whose only evaluation was cut off: no order — needs a ruling.
45. COHERENCE — Which CUT-0 row is named when two withhold one claim — minor.
46. GAP — The cut and K̂ at COMPLETED are undefined — minor.
47. GAP — How GROUNDED (R6) and HELD (15.13) combine into one standing, and whether a PREFIX claim gets the provenance line — needs a ruling.
48. GAP — 15.15 omits 15.7.6, 15.7.1, whether 'R' carries the cut, the unnamed codes and the grammar — minor.
49. COHERENCE — 15.1.5's "indented / column one" has no meaning in v0's line grammar — minor.
50. FAITHFULNESS — 15.13.3 adds "in every reading"; 15.13 omits "CUT-0 alone remains the target", the While priority, "neither compatibility preservation nor general soundness", and the no-invariance-release sentence — minor.
51. FAITHFULNESS — 15.12.6 generalizes the witness configuration from "rows testing an ungrounded port violation" to all rows — minor.
52. QUESTION — 15.7.6 omits "or metadata" from his out_0 words — minor.
53. FAITHFULNESS — 15.10 adds the claims and state digest definitions under [ruled: R5] — minor.
54. GAP — An arrival assigned to a NOT-RUN tick is "assigned" but reaches no record — minor.
55. COHERENCE — assign allows host-held arrivals across ticks vs "never held over" — minor.
56. GAP — A `not-run` end record in a tick-only law (impossible in a session) has no defined outcome — minor.
57. GAP — A port form in an inline arm: PORT-PLACE or SYNTAX — minor.
58. GAP — Append/Remove on a port: PORT-VARIABLE or TYPE — minor.

(The list runs to 58 items, but numbers 33 and 38 are the two FIXED findings. The tallies in the summary at the top cover items 1–55. Items 56–58 are minor GAPs added after the tally: with them, GAP is 20, minor is 26, and the total is 58.)