# The twin's 58 findings, disposed (2026-10-26)

**What this is.** The twin's report is `REPORT.md`, saved verbatim. Its provenance lists the five files of
`MANIFEST.md` and nothing else. The text it reviewed is `SPEC-15-DRAFT-0-AS-REVIEWED.md`, sha256-equal to the
manifest's entry. Each finding below was checked by its author against the draft, the rulings and SPEC. The
dispositions are the author's; the rulings remain the owner's. Findings are review evidence, not rulings and not proof.

**The dispositions:**
- **DRAFT:** a defect of the draft (wording, a tag, an omission against a ruling), accepted and fixed in draft 1.
  A fixed clause is changed, so under R7's build gate it is read again before it is built.
- **RULING:** a question only the owner can settle, filed under the open row or sheet item it belongs to. Under R7 its
  ruling triggers a re-read of A_r.
- **LEDGER:** the wording of a T10 row in `ROUNDS.md`.
- **MOOT:** dissolved once the rulings are read as ruled.

None is rejected.

**Two discrepancies in the report itself:**
- Its summary counts 6 findings that block the round; its list marks 5 (2, 3, 6, 8, 24).
- Its tallies cover items 1–55; items 56–58 were added after, as it says.

Neither changes a finding.

**SPEC facts the dispositions rest on, verified in `SPEC.md`:**
- §11 item 18: "An absorbed arm's condition, inline statement and events carry its own clause id."
- §11 G2: "A compile refusal writes no receipt."
- G3: "Every compile refusal belongs to exactly one phase".
- §11 item 19: "A While bound must be an integer literal; a decimal one is SYNTAX. A bound outside 1…2^62 is FUEL."
- `each`, `given` and `most` are reserved words (§2).

## The findings

| # | twin's tag, severity | disposition | what follows |
|---|---|---|---|
| 1 | QUESTION, ruling | **MOOT** | R4's "code, clause and tick" comes from R4's option row, which the as-ruled reading excludes, because R4's adopted ruling text replaces it. The draft's question to the owner is withdrawn. 15.7.5's sentence stays only as where the tick is read |
| 2 | FAITHFULNESS, blocks | **DRAFT** | 15.12.4 quotes R6's licence verbatim: "decided from the text"; "must stand" and "must not sit"; the whole claim line fixed by the law; the wider licence that waits for a trigger |
| 3 | COHERENCE, blocks | **DRAFT and RULING** | 15.0's "input point" was the author's own term, and with it the open proposal exempts more than R6 allows (the twin's P13). Draft 1 drops the term and states the static test by R6's own words, "before the first port declaration". The amended set's "static closure from the first input point" goes to the owner with this conflict named |
| 4 | GAP, ruling | **RULING** (PREFIX) | In a law with a tick block and no port, R6's position conditions are vacuous, while "precedes the first input" (tick 1) is not (P15). Proposal: in such a law the first input is the tick block's start |
| 5 | QUESTION, ruling | **RULING** (PREFIX) | R6 gives necessary conditions ("only if"). Proposal: a claim is exempt exactly when they all hold |
| 6 | GAP, blocks | **RULING** (A2; identity and bytes) | Read-once ports have no session event and no record syntax, and nothing says when the prefix runs or what happens when a read-once value never arrives. Draft 1 names the gap |
| 7 | GAP, ruling | **RULING** (port place; R2) | a law with ports and no tick block |
| 8 | GAP, blocks | **DRAFT and RULING** (identity and bytes) | Draft 1 restores contract draft 0's rule, which draft 0 dropped: a malformed log "is refused at load … before any execution starts", so the log is parsed whole first. The mapping of each LOG-* code to its conditions, and whether a load refusal writes a receipt (proposal: none, as a compile refusal writes none, G2), go to the owner |
| 9 | COHERENCE, ruling | **DRAFT** | "Later records are not read" means not executed. With the log parsed whole (8), the unread count is known |
| 10 | GAP, ruling | **RULING** (A2; session record) | the end record of a refused session's log |
| 11 | COHERENCE, ruling | **DRAFT** | "A refusal ends the session" means the run's refusal. A door refusal or a refused move does not end it |
| 12 | GAP, minor | **RULING** (A2) | precedence among the move refusals |
| 13 | COHERENCE, ruling | **RULING** (R3's own text) | R3's "all incoming port streams" are sieved as ASCII, yet text inputs are "preserved byte-for-byte". Proposal: the sieve governs integer, fixed and truth ports, and text has rule 5 |
| 14 | COHERENCE, minor | **RULING** (R3's details, with 15) | INPUT-NOT-INTEGER is reachable only if the integer grammar admits a point |
| 15 | GAP, ruling | **RULING** (R3's details) and **DRAFT** (tag them open) | the integer and decimal grammars |
| 16 | FAITHFULNESS, minor | **DRAFT** | R3's raw values are "hexadecimal" |
| 17 | FAITHFULNESS, ruling | **DRAFT** | R3's adopted text replaces "values exactly as sent": "typed encodings only (RUNTIME-SPEC §5), written once by a Python input door, so no runtime ever parses decimal text" |
| 18 | FAITHFULNESS, minor | **DRAFT** | His "CP1252 character maps are rejected outright" is stated as his; which code it takes is open |
| 19 | FAITHFULNESS, minor | **DRAFT** | Under the R3 tag the draft added the pure function, the door's version in the header, the rule order, range before grid, and COMPAT-0's one-way rule (a reason in R3, not a rule). These are retagged open, as contract draft 0's |
| 20 | FAITHFULNESS, ruling | **DRAFT and RULING** | "The `'R'` event carries the cut" is retagged open. The claims ruling requires each withholding to name its row, which needs the cut, but it says nothing of the trace, and R5's new events are `'T'` and `'N'`. Whether version 1's `'R'` payload changes goes to the owner, with the format freeze (P6) |
| 21 | FAITHFULNESS, ruling | **DRAFT** | 15.13.5–8 and 11 are retagged. The court's R8 and CUT-0's rows are fixed by the pinned digest the ruling requires, not by the ruling's words. Until a digest is pinned, they state what is proposed to be pinned |
| 22 | FAITHFULNESS, ruling | **DRAFT** | R4's "The court reads each branch on its own and names every abandoned branch" is added |
| 23 | FAITHFULNESS, minor | **DRAFT** | 15.12.5 quotes "regardless of whether the execution loop encounters a subsequent transactional refusal downstream" and "historically held" |
| 24 | COHERENCE, blocks | **RULING** (D10 against R6) | D10's REFERENCE-ONLY until 1b holds no claim, so R6's PREFIX claim cannot "stay held" and R6's control cannot read GROUNDED in 1a. The R6 record already saw the vacuity ("no vacuous row"). The owner must say whether R6's rows run in 1a's reference, D10 lifted for them, or wait for 1b |
| 25 | FAITHFULNESS, minor | **DRAFT** | 15.1.6 quotes R6's cost sentence and cites §15.12 |
| 26 | COHERENCE, minor | **DRAFT** | 15.7.3's clause question is closed by SPEC §11 item 18, verified: an absorbed arm's condition carries its own clause id, so TICK-BUDGET at an arm's condition names the arm's clause. The cut's event check (S6) follows |
| 27 | GAP, ruling | **RULING** (port place; budget; the code registry) | the codes for an each-tick read outside the tick block and for N above 2^62 (by item 19's analogy), and the phases of the three compile codes |
| 28 | COHERENCE, ruling | **RULING** (port place) | "outside the tick block": textual, so procedures and Defines can never read an each-tick port, or by evaluation (P18) |
| 29 | GAP, minor | **RULING** (budget) | `at most 0`: a legal spelling, and one law line or two |
| 30 | GAP, ruling | **RULING** (counting) | what an each-tick port's declaration does at its own place |
| 31 | GAP, minor | **RULING** (identity and bytes) | `tick-ops` when no tick began |
| 32 | GAP, minor | **RULING** (1a's specification) | the tick line's `events` and `output-bytes`: per tick or running |
| 33 | FIXED, minor | **DRAFT** | Replay is scoped to executions that end with a receipt: a host stop writes none (SPEC §12). A play build without the chain is sheet R14, open |
| 34 | GAP, minor | **DRAFT** | the untagged clauses are tagged: 15.0's terms, 15.8's core, 15.10's identities, 15.11's Replay |
| 35 | GAP, ruling | **RULING** (identity and bytes) | the read-once record, `<port>`'s spelling, t = n+1, the LF inside the chain hashes, the domain string, a partial last line |
| 36 | GAP, ruling | **RULING** (identity and bytes) | the loader's check of each value against its port's type and the door's rules |
| 37 | GAP, minor | **RULING** (R2; identity and bytes) | the source of `"<name>"` and the spelling of `<type>` |
| 38 | FIXED, ruling | **DRAFT** | "the draft's §1.5" is cited as contract draft 0's §1.5. "Never held over" is scoped "until SNAP-1's continuation rule", so as not to bind R4's later rule |
| 39 | T10, ruling | **DRAFT** | 15.13.7's sentence "an arm's inline statement stands in its If's frame" misled. An inline statement is a frame of its own, directly above its If's frame, named by the If's clause and its arm, and the two count as one position for the rest of the block. A refusal in a true arm's inline statement is then the rest-of-block row, not a gap in T10.2 |
| 40 | T10, minor | **DRAFT** | "Open" is defined: a claim is open when its statement is the top frame of the cut. That includes a claim refused at its own operation before its condition is evaluated |
| 41 | T10, ruling | **DRAFT** | §15.13 defines the continuation: reading S2 (every later refusal passable, values unknown, only a For's normal exit exact), relative to the law (any further input) and not to the session |
| 42 | T10, minor | **LEDGER** | T10.5 is reworded. Return to the frame below holds on any stack; what no recursion gives is at most one frame per procedure, so the cut names each call without ambiguity |
| 43 | T10, ruling | **LEDGER and RULING** | T10.7 names its dependence on 15.1.3. With the log parsed whole (8), no load refusal happens at a tick, so the tick block is never on top for that reason. Ports and the tick block in "every statement kind" wait for the version-1 schema |
| 44 | COHERENCE, ruling | **DRAFT** | the court's order as built (`court.py`): R8's reading of a refused evaluation comes before UNREACHED, so a claim whose only evaluation was cut off reads as R8's refusal |
| 45 | COHERENCE, minor | **RULING** (minor) | the row named when two rows withhold one claim. Proposal: name every row |
| 46 | GAP, minor | **DRAFT** | at COMPLETED, K̂ is empty (`CUT-0.md` §2's outcome table) |
| 47 | GAP, ruling | **DRAFT** | GROUNDED requires held, as in version 0 (`court.py`, `panel`). The provenance line is printed for the run, as R6's row says |
| 48 | GAP, minor | **DRAFT** | 15.15 gains the missing rows |
| 49 | COHERENCE, minor | **DRAFT** | 15.1.5 is restated in SPEC §1's line terms |
| 50 | FAITHFULNESS, minor | **DRAFT** | the claims ruling's omitted sentences are added: CUT-0 alone the target; the While priority; "neither compatibility preservation nor general soundness"; no release by invariance in version 1 |
| 51 | FAITHFULNESS, minor | **DRAFT** | the witness rider is scoped to "every row testing an ungrounded port violation", as he said |
| 52 | QUESTION, minor | **DRAFT** | his out_0 words are quoted ("any visual bytes or metadata"); "the output holds nothing else" is marked as a reading |
| 53 | FAITHFULNESS, minor | **DRAFT** | the claims and state digests' definitions are retagged open |
| 54 | GAP, minor | **RULING** (A2) | an arrival assigned to a tick that does not run |
| 55 | COHERENCE, minor | **RULING** (A2) | an accepted arrival held by the host across ticks, against "never held over" |
| 56 | GAP, minor | **RULING** (identity and bytes) | a `not-run` end record in a law with no port. Proposal: refused at load |
| 57 | GAP, minor | **RULING** (port place) | a port form in an inline arm |
| 58 | GAP, minor | **RULING** (port place; counting) | Append or Remove on a port |

**Totals,** counted from the table:
- **DRAFT:** 31, of which 4 also go to a ruling (3, 8, 15 and 20).
- **RULING alone:** 24. Counting the four with DRAFT and the one with LEDGER, 29 findings reach a ruling.
- **LEDGER:** 2 (42 and 43), of which 43 also goes to a ruling.
- **MOOT:** 1.

31 + 24 + 2 + 1 = 58.

## What the owner's rulings must now cover

Grouped by the row or item that decides them. Each, once ruled, triggers a re-read of its A_r:
- **PREFIX:** findings 3, 4 and 5. *Ruled 2026-10-26 (`RULINGS.md`).*
- **A2:** 6, 10, 12, 54 and 55. *Finding 6 ruled 2026-10-27 (`RULINGS.md`).*
- **Session record:** 10.
- **Identity and bytes:** 6, 8, 31, 35, 36, 37 and 56.
- **D10 against R6:** 24, which blocks the round. *Ruled 2026-10-26 (`RULINGS.md`).*
- **Port place and R2:** 7, 27, 28, 43, 57 and 58; R2 also decides 37.
- **R3's details:** 13, 14 and 15.
- **Budget and counting:** 27, 29, 30 and 58.
- **The code registry:** 27.
- **The `'R'` payload and the format freeze (P6):** 20.
- **1a's specification:** 32.
- **Minor:** 45.

*Corrected 2026-10-26: the list omitted finding 43 (port place, beside its ledger half) and dropped a decider each for 10 (session record), 27 (the code registry) and 37 (R2) that their own rows name. Packet E found it (`packets/E-release-gate.md` §1 A). The list now covers all 29 findings that reach a ruling.*

## What happens to the draft

*Done the same day: draft 1 is `SPEC-15-DRAFT-1.md`, and its changes are recorded clause by clause in
`DRAFT-1-CHANGES.md` (74 clauses changed or added, all owed a re-read). Findings 42 and 43 are applied to the ledger.*

Draft 1 applies the 31 DRAFT dispositions, and the two LEDGER ones are made in `ROUNDS.md`. Draft 0, as reviewed,
stays as `SPEC-15-DRAFT-0-AS-REVIEWED.md`. Every clause draft 1 changes is recorded, by a clause-by-clause comparison
of the two, and read again by the twin before it is built. That is R7's build gate: a changed clause is a clause the
twin has not read.
