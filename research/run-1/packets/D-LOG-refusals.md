<!-- Packet D, saved by the draft's author, 2026-10-26: a research subagent's final report, delivered as its message (subagents cannot write files; its output file is empty). Copied without change. -->

## Finding 8 decision packet: load refusals for a malformed input log (research only; nothing ruled)

**Provenance.** I read the files in the working tree at HEAD 95dac79. Several are not committed: `research/run-1/probes/`, `SPEC-15-DRAFT-1.md`, `CUT-0.md`, `CONTRACT-DRAFT.md`, `ROUNDS.md`, `ADVERSARY-ROUND-D.md` and `twin-r7/` are untracked, `RULINGS.md` is modified, and `evidence/run1-cut0-session.txt` is untracked. Line numbers refer to those working copies. I ran nothing: no probe, no build. Every statement below about what the model does comes from reading its code. Each statement carries a label: RULED, OPEN, INFERENCE or PROPOSED WORDING.

---

### 1. The governing wording

**RULED, or version 0 in force**
- SPEC.md:303-304 (§11 G2): "A compile refusal writes no receipt. The arbiter's witness records its code, line and message; the command line exits 1."
- SPEC.md:453-455 (§12): a host stop gives "no receipt, no refusal, and no agreement or dissent".
- SPEC.md:470-483 (§13 G3): compile refusals are ordered by a phase table. "The first refusal in the first phase that has one is reported." Phase 1 checks `BYTES-NOT-UTF8` "for the whole text first; then line by line". This is the existing precedent for ordering refusals.
- RUNTIME-SPEC.md:147-149 (§5): a value encoding includes its tag byte: Int `'I'`+8 bytes, Fix `'X'`+8, Bool `'B'`+1 byte (0/1), Text `'T'`+u32 length+bytes. SPEC.md:54 (§11 item 54) agrees.
- RUNTIME-SPEC.md:26-31 (§1): exit 0 for a completed or refused run, 2 for a file that cannot be opened; "none writes a receipt that claims one".
- RULINGS.md:91-92, tagged [ruled: R3] at SPEC-15-DRAFT-1.md:100 and adopted by DISPOSITION row 17: "the log holds typed encodings only (RUNTIME-SPEC §5), written once by a Python input door". RULINGS.md:96-105 (R3 a): the door never rounds.
- RULINGS.md:185 and 208-217 (R5): receipt 1 carries `input-log-sha256`, and the frame check is tied to the law's own header.
- RULINGS.md:289-290 (R6 rider): the provenance line "must print exactly the `input-log-sha256` value defined in `receipt 1`".
- arbiter.py:246-252, as built: on a compile refusal, `w["refusal"] = {code, line, message}`, and the function returns `(comp, w, None)`. No reference run and no backend build happen. orl.py:58-61 (`run`) prints the refusal and `continue`s before the witness file is written at orl.py:75-79. orl.py:89-91 (`court`) prints `REFUSED` and returns 1. INFERENCE: on a compile refusal today, the witness exists only in memory.

**OPEN**
- SPEC-15-DRAFT-1.md:147-167 (§15.5) is tagged [open: identity and bytes] as a whole. That covers the grammar (149-157), "parsed whole before any execution starts … no tick of a malformed log runs" (158-159), the nine codes (160-161), and the open tag naming finding 8 (161-163).
- CONTRACT-DRAFT.md:63-65 (§2.2) is the source of "refused at load … before any execution starts", under its single code LOG-MALFORMED. Note that it lists "port count **or types**". CONTRACT-DRAFT.md:84 (§3.3): PORT-SIGNATURE "before execution".
- ROUNDS.md:442 (amended set, A2): "a log offered whole is checked whole before execution". ROUNDS.md:447 (identity and bytes). Both still read "open" at ROUNDS.md:635.
- R10 (RULINGS.md:444-450) is not ruled. PORT-SIGNATURE's binding rests on it.
- SPEC-15-DRAFT-1.md:75-77 (§15.2, open): the door is a pure function, and its version is named in the header.
- Round D's dispositions are research records, not rulings: `tick <t>` and `once` always written (ROUNDS.md:268); "Tick 0 is the read-once record … `not-run 0`" (ROUNDS.md:271); "t = n+1" (ROUNDS.md:272); whole log offline, valid prefix live (ROUNDS.md:277).
- Round D's repair says "checks the whole log, **its ports line first**" (ADVERSARY-ROUND-D.md:292).
- CONTRACT-DEBATE.md:109-113 (D3): the end record may also bind "the log's running chain head".

**INFERENCE: the model is not the draft's grammar**
- The model writes the record keyword `t` and each value as 16 lowercase hex digits: the raw u64, with no tag byte (cut0_session.py:205, 222, 252). The draft says "each value's encoding (RUNTIME-SPEC §5) as lowercase hex" (SPEC-15-DRAFT-1.md:153). With the tag, a fixed value is `58`+16 digits; the twin reads it so ("Fix 1.5 = 580000000180000000", twin-r7/REPORT.md:400).
- ROUNDS.md:268 says the probe "holds the same grammar for fixed ports". Read against the code, it does not: `t` is not `tick`, there is no `once` line, and there is no tag byte.
- The model has one type (fixed), each-tick ports only, one door (`door-0`), and its port signature hardcodes `fix each-tick` (L192-194). So its LOG-RECORD checks, and its 16,132 mutations, run over a value form that is not the draft's.

---

### 2. The refusal-condition matrix

Each code gives: the model's condition (cut0_session.py); what that condition misses; a PROPOSED WORDING; and an example that should take the code.

**LOG-NOT-ASCII**
- Model: any byte above 0x7F, checked first over the whole log (L227-230).
- Misses: ASCII control bytes pass it. A CR goes to LOG-LINE. A NUL, TAB or DEL takes the code of the field it lands in, for example `t\t1` gives LOG-UNKNOWN.
- PROPOSED WORDING: "The log holds a byte above 0x7F." OPEN alternative: any byte outside 0x20–0x7E other than LF.
- Example: `door door-\xc3\xb8` (L502).

**LOG-LINE**
- Model: a CR anywhere; a last byte that is not LF (an empty log included); or LF LF (L231-232).
- Misses: a LF as the very first byte is not caught. The first line is then empty, and the log is refused LOG-HEADER (L234). An empty log is refused LOG-LINE, not LOG-HEADER.
- PROPOSED WORDING: "The log holds a CR, does not end with LF, or holds an empty line (a LF at its start or two in a row)." Including the leading LF changes the model's code for that one case; that choice is OPEN.
- Examples: CR LF line ends (L495); `GOOD[:-1]` (L496).

**LOG-HEADER**
- Model: line 1 ≠ `orlog-inputs 0`, or fewer than 3 lines, or line 3 ≠ `door door-0`, or line 2 not `ports `+64 lowercase hex (L234-237). Line 3 is checked before line 2.
- Misses: the spelling of the door version, and which versions a loader accepts. The draft's relax-only rule (L101-102, open) implies reading older doors' logs under their own rules.
- PROPOSED WORDING: "Fewer than three lines; line 1 not exactly `orlog-inputs 0`; line 2 not exactly `ports ` and 64 lowercase hex; line 3 not exactly `door ` and a version the loader implements."
- Example: `orlog-inputs 1` (L500).

**PORT-SIGNATURE**
- Model: line 2 is well formed, but its digest differs from the law's signature (L238-239).
- Misses:
  - types other than fixed, and the once kind (§15.6's `<type>`, finding 37);
  - R10 is unruled;
  - a log offered with an `orlog-law 0` law: a version-0 law and a tick-only law both have no port, so they share the signature SHA-256(`orlog-ports 0\n`). No clause says whether such a log is refused or ignored.
- PROPOSED WORDING: "Line 2's digest is not the law's port signature (§15.6)."
- Example: L501.

**LOG-RECORD**
- Model, in a `t` line:
  - the field count is not 2+ the number of each-tick ports (L246-247), checked before the tick number;
  - then a value that is not exactly 16 lowercase hex digits (L251-253);
  - any 16 hex digits is accepted as an i64 (L254-255).
- Misses everything that depends on type (findings 36 and 6):
  - a wrong tag (an `'I'` at a fixed port);
  - a wrong length;
  - a `'B'` byte of 02;
  - a text whose length field disagrees with its bytes, or whose bytes are not UTF-8 or break other text-door rules (R3 details, open);
  - an odd hex length, or an empty field;
  - an `'F'` tag (sheet R8 unruled) or an `'L'` tag (D7);
  - the read-once record.
  - INFERENCE: every 8-byte `'I'`/`'X'` value is already in the door's image (the range is all of i64, and raw values sit on the grid). So the door-dependent check only bites for truth and text values, and for any future port range or float.
- PROPOSED WORDING: "A tick record whose number of values is not the law's number of each-tick ports, or a value that is not the lowercase hex of exactly one RUNTIME-SPEC §5 encoding of its port's type that the door named on line 3 can write." Folding type errors into LOG-RECORD follows contract draft 0 §2.2's "count or types"; a separate code (LOG-VALUE) is OPEN.
- Examples: `t 2` with one port (L479); `t 1 490000000000000003` at a fixed port; `t 1 4202` at a truth port; `t 1 5400000001e9` (a text that is not UTF-8).

**LOG-TICK**
- Model: the tick field is not canonical decimal (`^(0|[1-9][0-9]*)$`), or is not the count of earlier records plus 1 (L248-249, L221).
- Misses: nothing in scope; only its order relative to LOG-RECORD is open.
- PROPOSED WORDING: "A tick record whose number is not canonical decimal or not one more than the tick records before it."
- Examples: L485-488 (a number skipped, repeated, from 0, `t 02`).

**LOG-END**
- Model:
  - an `end` line with fewer than 3 fields, or n not canonical decimal, or n ≠ the number of tick records (L258-259);
  - otherwise exactly `closed`, or six fields `not-run t cause port` with t canonical and = n+1 (L262), the cause INPUT-MISSING only (L263), and the port in the law's each-tick list (L264);
  - anything else is LOG-END (L266-267);
  - with no each-tick port, every `not-run` record is LOG-END (L264).
- Misses:
  - whether the port named is the first missing in declaration order: only the history can tell (HISTORY-MISMATCH, ROUNDS.md:272);
  - the spelling of `<port>` (finding 35);
  - a read-once port's `not-run`, or `not-run 0` (finding 6);
  - a refused session's end record (finding 10);
  - D3's chain head, if ruled.
- PROPOSED WORDING: "An end record other than `end <n> closed` or `end <n> not-run <t> INPUT-MISSING <port>`, with n the number of tick records and t = n+1, both canonical, and <port> the name of one of the law's each-tick ports. A law with no each-tick port has no `not-run` record."
- Examples: L489, L490, L503; and `end 1 not-run 2 INPUT-MISSING x` in a tick-only law (twin P03; no named case covers it).

**LOG-AFTER-END**
- Model: any line after an end record, checked before the line's kind (L243-244).
- Misses: nothing.
- PROPOSED WORDING: "Any line after the end record."
- Examples: L477, L478.

**LOG-UNKNOWN**
- Model: a line after the header whose first field is neither `t` nor `end`, a leading space included (L268-269).
- Misses: Round D's `tick` and `once` spellings are LOG-UNKNOWN here.
- PROPOSED WORDING: "A line after the header whose text before its first space is not a record kind of `orlog-inputs 0`."
- Example: `note hello` (L499).

**The read-once record (no code assigned)**
- Model: absent from both the serializer and the parser (L201-213, L241-269).
- Draft: "One record for the read-once ports" (SPEC-15-DRAFT-1.md:152), with no syntax given.
- Example: `once 490000000000000003` for `Let g be given as an integer.` is LOG-UNKNOWN under the model.

**The other cases the brief asked about**
- **An open log with no final LF:** LOG-LINE (L231); no named case covers it (the case to add is `OPEN_LOG[:-1]`). PROPOSED: keep it LOG-LINE, so a reader never truncates to the last LF and "the bytes as read" never depends on timing.
- **CRLF:** LOG-LINE, for any CR anywhere. The loader repairs nothing, unlike the law-text door, which removes CR (SPEC.md:335).
- **t ≠ n+1 in `end n not-run t`:** LOG-END (L262). The draft is silent on it (finding 35).
- **A `not-run` record in a law with no port:** LOG-END (L264). DISPOSITION.md:90 proposes refusal at load.
- **A value whose hex does not decode to its port's type:** LOG-RECORD under the wording above. The model does not implement it.

**Precedence: what the model does (INFERENCE)**

| phase | scope | codes, in order |
|---|---|---|
| 1 | the whole log | LOG-NOT-ASCII |
| 2 | the whole log | LOG-LINE |
| 3 | lines 1–3 | LOG-HEADER: line 1, the line count, line 3, then line 2's form |
| 4 | line 2's value | PORT-SIGNATURE |
| 5 | lines 4 onward; the first faulty line wins | LOG-AFTER-END; then the line's kind (LOG-UNKNOWN); in a `t` line: LOG-RECORD for the count, then LOG-TICK, then LOG-RECORD for the values; in an `end` line: LOG-END |

Under whole-log loading, a load refusal always beats a run refusal: `execute` parses before anything else (L276).

**Held incidentally by a named case:** each named log is the good log with one edit, but some edits also break a later check, which pins the order between the two:
- NOT-ASCII before HEADER (L502);
- LINE before HEADER (L495);
- LINE before END (L496);
- LINE before UNKNOWN (L497);
- AFTER-END before acceptance (L477-478, plant `after-end`).

**Held by no case and no plant:**
- NOT-ASCII against LINE;
- the door line against PORT-SIGNATURE;
- PORT-SIGNATURE against any record code;
- the field count against the tick number;
- the tick number against the values;
- an earlier faulty line against a later one;
- AFTER-END against UNKNOWN.

The mutation sweep (L606-624) counts only refused against accepted, and canonicity. It holds no code and no order.

**Unsettled**
- (a) Is the ports line checked first (Round D's wording) or fourth (the model)?
- (b) Within a tick record: count before tick number (the model), or strict field order?
- (c) Line-major order (the model) or phase-major order (SPEC §13's precedent)?
- (d) What do a leading LF and an empty log take?
- (e) Is compile checked before load? The loader needs the law's ports (`parse_log(b, ports)`), but no text states the order. PROPOSED: compile first.

---

### 3. What a load refusal writes

**(N) Nothing.** No receipt and no witness; an exit status and a message only, as RUNTIME-SPEC §1 does for an unopenable file.
- Outcomes: the four are unchanged.
- Arbiter: has nothing to record; a malformed log cannot be told from an I/O failure.
- Court: no reading.
- Counterexample: a loader defect of the door-dollar class (L64), where a canonical log is refused, leaves no code and no line. The nine codes would have no surface to test but stderr text.

**(W) Witness only: G2's analogue.** No receipt; the witness records the code, the line, a message and a digest of the bytes; the command exits 1.
- Outcomes: the four are unchanged. T14 (ROUNDS.md:339) is scoped to logs that load. §15.11's Replay already covers only executions that end with a receipt.
- Arbiter: runs no execution, so 1b's runtimes never see a refused log in arbitration.
- Court: no reading and no provenance line, as `court` does for a compile refusal. Nothing reaches D10 or R6's rows.
- Counterexamples:
  - Round D finding 10's LOAD-ORDER law (ADVERSARY-ROUND-D.md:264-282): a PREFIX claim §1, a refusal in the prefix at §2, and a malformed record 3. The claim gets no reading at all, although nothing it depends on reaches record 3.
  - "As a compile refusal" literally leaves no file record today (orl.py:58-61 runs before 75-79).
  - If the witness names the log by §15.5's `input-log-sha256` ("to the end record inclusive", L166-167), then `GOOD+"t 3 …\n"` (LOG-AFTER-END) is named by GOOD's digest.

**(R) A receipt with a status.** For example `status LOG-REFUSED <CODE> <line>`, or `REFUSED <CODE> 0`.
- Outcomes: five, not four. §15.7.5 and T14 must change, and the court must parse the new status.
- Arbiter: every runtime must implement the loader and the order byte for byte, so the order becomes a one-way, cross-backend contract.
- Court: every claim reads UNREACHED, and R6's line is printed for bytes that are not a log.
- Counterexamples:
  - LOG-AFTER-END: a refused receipt and GOOD's COMPLETED receipt would share one `input-log-sha256`.
  - A CRLF log has no defined record count, so `ticks` and the unread count have no value.
  - §15.4 says "the receipt core attests one execution over its input log" (L139), and here none happened.
  - The two kinds of refusal before execution would be treated differently: G2 writes no receipt for compile.

INFERENCE: under (N) or (W), the code mapping and the order among refusals stay out of every one-way format, so either could be corrected later without breaking a recorded receipt. The accept set, meaning the grammar itself, is one-way under all three.

---

### 4. The narrowest recommended decision (PROPOSED; the owner rules)

1. **Load whole.** A log offered whole is loaded after the law compiles and before any statement runs. A live session's log is its history's projection, appended record by record, and every prefix of it loads (ROUNDS.md:277). OPEN until ruled.
2. **The nine codes** take the conditions in §2's PROPOSED WORDING. Values are checked as LOG-RECORD, by reference to the image of the door named on line 3. That wording inherits R3's open text rules and decides none of them.
3. **The order** is the model's phase table, stated as SPEC §13 states G3. Sub-choices (a)–(e) stay OPEN. My lean is to keep the model's order wherever no case holds it, because it is what was run.
4. **Receipts: (W).** No receipt. The witness records the code, the 1-based line and a message, plus a digest of every byte under a name of its own, never `input-log-sha256`. Exit 1, as G2. No court reading. OPEN: whether the witness file is persisted; how a 1b runtime behaves when handed such a log, and with what exit status.
5. **The end record:** t = n+1 for each-tick ports; `<port>` is the port's name; a law with no each-tick port has no `not-run`.
6. **The read-once record:** only a presence rule. PROPOSED: no read-once line when the law has no read-once port. That keeps the model's 13 logs, the 25 named cases and the twin's P01/P02 as they are. The OPEN alternative is always present (ROUNDS.md:268).

**It must not decide:**
- read-once ports' session event (finding 6): when the value fills, when the prefix runs, what happens when it never arrives;
- D10 against R6 (finding 24). Under (W) nothing here depends on it. Note that "D10" here is RULINGS.md:503-504, not CONTRACT-DEBATE's D10;
- a refused session's end record (finding 10);
- R3's text rules (findings 13 and 15), R10, §15.6's spellings (finding 37), D3's chain head, and float ports.

**Where read-once ports unavoidably touch the grammar:**
1. Whether line 4 of **every** log is a read-once record. This decides LOG-RECORD, LOG-TICK and LOG-UNKNOWN at line 4 even for tick-only laws.
2. The record's keyword and its value list.
3. Whether a header-only log for a law with a read-once port is open or malformed.
4. `not-run 0` (ROUNDS.md:271) against t = n+1 (L262). With zero records, t = n+1 gives 1, so an unqualified t = n+1 would decide finding 6's NOT-RUN by the back door.
5. A tick `not-run` that names a read-once port ("of t's kind", ADVERSARY-ROUND-D.md:164-165).
6. in_0's bytes "with the read-once record" (SPEC-15-DRAFT-1.md:164).

---

### 5. What the decision touches

**Clauses of SPEC-15-DRAFT-1.md**
- §15.0 (L40-41): a load refusal is not an execution.
- §15.2 (L75-77, L100-102): the value check rests on the door's version and purity.
- §15.4 (L142-143): the verifier needs a verdict for a log that does not load. The model's verdict, `LOG-MALFORMED %s` (L355-356), still carries draft 0's old single code.
- §15.5 (L147-167), all of it: the value form (tag byte), the keyword, the read-once presence rule, t = n+1, `<port>`, the offline/live scope, the codes, the order, the receipt, and the digest of a refused log.
- §15.6 (L169-174).
- §15.7.4 (L195-196): finding 9 reopens if streaming is chosen instead.
- §15.7.5 (L197-201).
- §15.8 (L218, L222).
- §15.11 (L276-280).
- §15.12.3 (L291-292).
- §15.15 (L393, L395).

**Ledger rows**
- ROUNDS.md:
  - the amended set: identity and bytes (L447), A2 (L442), codes (L452: register the LOG-* codes with a class);
  - the decisions table: L375, L381, L384, L387;
  - the theorem ledger: T1 (L318: add the load verdict as a function of the law and the log's bytes), T10.7 (L335), T14 (L339), T15 (L340);
  - Round D: L268 (the discrepancy above), L271, L272, L277.
- DISPOSITION.md rows 8, 9, 35, 36 and 56 (L42, L43, L69, L70, L90); also 6, 31, 37 and 43.
- RULINGS.md:466 (R12's plant: "a misaligned log entry, refused rather than shifted").

**Tests a 1a build would need**
- Carry over the probe's 25 named malformed logs and the open-log case (L476-506), the mutation sweep (L606-624), the parser plants `lenient-hex`, `after-end` and `a1-cause-under-a2` (L654-658), and the rows `log-round-trips` and `projection-parses` (L376-381). The hex cases and the good log need rewriting if values carry their tag.
- **Typed values:** an `'I'` at a fixed port; an `'X'` at an integer port; `'B'` 02; a text length mismatch either way; a text that is not UTF-8; an odd hex length; an empty value; an `'F'` or `'L'` tag. Plant: the tag left unchecked.
- **End record:** a `not-run` in a tick-only law; t = n and t = n+2.
- **Order:** one two-fault log per unsettled pair, each with a plant that swaps the pair. Also a leading LF, an empty log, the open log without its final LF, and an unknown door version.
- **Load order:** Round D's LOAD-ORDER row: no event, no output, no receipt. Plant: a streaming reader.
- **Receipt:** no receipt file is written; the witness holds its fields; the court gives no reading. Plants: a receipt written with a status; a digest taken "to the end record".
- **Compile before load:** a text with a compile refusal and a malformed log reports the compile code.

---

### 6. A falsifier for the recommendation

The recommendation is wrong if any of these happens:
- Two loaders written apart from the ruled table refuse the same bytes with different codes, or the table names two codes for one log. Test it over every pairwise combination of the named single-fault edits.
- The loader accepts a byte string whose re-serialization differs from it.
- On any load-refused log, the 1a reference emits an event, counts an operation, says a byte, or writes a receipt.
- A refused log's recorded digest equals the `input-log-sha256` of a log that loads.
- The owner reads R6's rider as requiring a provenance line for every log offered with a version-1 law. Under that reading, (W) conflicts with a ruling.
