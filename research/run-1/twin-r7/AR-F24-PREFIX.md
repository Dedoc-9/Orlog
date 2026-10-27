# A_r for the rulings of 2026-10-26 on finding 24 and the PREFIX licence

R7, point 4: a ruling being made triggers the re-read of A_r = T_r ∪ L_r ∪ D_r, once per triggering ruling, before
anything is built. The set is recorded, and the builder may not narrow it. This record holds the two sets his rulings
of 2026-10-26 trigger (`RULINGS.md`, "Finding 24 and the PREFIX licence"). His instruction: *"After recording, compute
each ruling’s affected-clause set \(A_r = T_r \cup L_r \cup D_r\), including dependencies identified by the twin’s tag
audit, and have the twin perform the required rereads before any build."*

## How the sets were computed

`ar_compute.py` (this folder) computes them over `SPEC-15-DRAFT-1.md`, and refuses to run on any other text than sha256
`367b1b4866e795d44141a87ef23579237fe414cf1fe61817fd47df135bd99d47`. Run with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B
research/run-1/twin-r7/ar_compute.py`; its whole output is below, unedited.

- **A clause** is `clause_diff.py`'s unit: a top-level item of a section, its continuation lines included. The same
  splitting finds 74 clauses of draft 1 changed or added since draft 0, which equals `DRAFT-1-CHANGES.md` (61 + 13).
- **T_r:** the clauses whose bracket tag names the ruling (`D10`; `PREFIX`), and the §15.15 rows whose "decided by"
  cell names it.
- **L_r:** the clauses containing a term the ruling defines or newly defines, closed over §15.0's formal definitions (a
  term defined there in words of the ruling's terms joins them). The terms:
  - finding 24: REFERENCE-ONLY (its scope), configured and witness (the configured witness), agreement (configured is
    not measured), HELD (court R1 stays a condition of it beside E2), control (the witness covers the controls);
  - PREFIX: PREFIX (matched in any case, since §15.0's "Prefix" collides with it), licence, exempt, boundary, first
    input, first port declaration, closure, Reach, may execute, statement kind, oracle.
  The closure added no term: no definition in §15.0 is written in these terms.
- **D_r:** the clauses named as dependent on the ruling, each by its source, given by draft 1's line numbers and mapped
  to every clause whose lines meet them:
  - R7's review (`REPORT.md`): findings 3, 4, 5 and 24; A19 and A20; B14 items 4 to 6; and its tag audit, the
    "Missing dependencies" lines that name PREFIX (15.0 Port, 15.1.3, 15.1.6) or that A19 and A20 record. A20's names
    R6 and the claims ruling as missing from 15.13.11. A19's names 15.1.3 and draft 0's "Input point", a term draft 1
    dropped, so it maps to no clause of draft 1;
  - dependencies identified after the review, which R7 says enter D_r and are recorded: packet A §6, packet B §5,
    packet E (the tags it found incomplete, and its L_r candidates), and the integration's I-3 (the binding place B's
    licence presupposes) and I-9 (`Reach`, shared with K̂).

**Limits.** The term closure runs over §15.0's formal definitions only, so a term defined informally elsewhere is not
followed. The matching is textual: it takes in clauses where a word has another sense (15.2.3's "raw prefix", 15.3's
"held over"), and R7 does not let the builder take them out. A_r makes no claim to hold every semantic dependency (R7,
point 4). A dependency found later enters D_r and is recorded here.

## What the twin reads

The set's clauses as the rulings leave them: `SPEC-15-DRAFT-2.md`, which states the two rulings in the clauses they
decide (`DRAFT-2-CHANGES.md`). It changes no clause outside A_F24 ∪ A_PREFIX but its title and status paragraph,
which name the draft. The two §15.15 rows it removes are in the sets, and the line it adds there in their place
says they are ruled. The rulings as ruled are added to
`RULINGS-AS-RULED.md`.

- A clause in both sets is read once for each ruling.
- The 40 clauses of the union that are among draft 1's 74 are read here in their current text, which meets their
  draft-1 re-read too.
- The other 34 of the 74 wait for the next rulings (findings 6 and 8), so that a clause those rulings change is read
  once, in the text they leave. A clause of the 74 that no ruling reaches is read on its own before it is built.

## The computed sets

Draft 1: 139 clauses; 74 changed or added since draft 0, so owed a re-read before any ruling (DRAFT-1-CHANGES.md gives 61 + 13 = 74).

## A_r for finding 24: D10's court clause scoped (D)

Terms the ruling defines or newly defines: REFERENCE-ONLY, configured, witness, agreement, HELD / held, control. The closure over 15.0's definitions adds: none.

|A_r| = 25 clauses (T_r 2, L_r 13, D_r 20; a clause may be in several); 23 of them among the 74.

| # | clause | lines | in the 74 | why |
|---|---|---|---|---|
| 4 | preamble [ruled: R3, R4, R5, R6] | 10-11 | yes | D(packet A §6: the tag legend) |
| 5 | preamble [ruled: claims] | 12-12 | yes | D(packet A §6: the tag legend) |
| 6 | preamble [pinned] | 13-15 | yes | D(packet A §6: the tag legend) |
| 7 | preamble [v0] | 16-16 | yes | D(packet A §6: the tag legend) |
| 8 | preamble [open: X] | 17-19 | yes | D(packet A §6: the tag legend) |
| 21 | 15.1.5 | 59-62 | yes | L(agreement) |
| 41 | 15.3 No value is invented, held over or defaulted, | 125-126 | yes | L(HELD / held) |
| 47 | 15.4 Three records, three authorities | 138-141 |  | L(agreement) |
| 81 | 15.8 The core | 232-233 | yes | L(agreement) D(packet A §6: §15.8's core) |
| 86 | 15.9 The `'R'` event would carry the refusal cut. | 245-253 | yes | D(packet A §6: §15.9) |
| 98 | 15.11 Replay. | 276-280 | yes | D(packet A §6: §15.11) |
| 99 | 15.11 Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity. | 281-282 | yes | D(packet A §6: §15.11) |
| 102 | 15.12.2 | 289-290 | yes | L(HELD / held) D(packet A §6: §15.12.2) |
| 103 | 15.12.3 | 291-292 | yes | D(packet A §6: §15.12.3) |
| 106 | 15.12.5 | 311-312 | yes | L(HELD / held) D(packet A §6: §15.12.5; packet E: 15.12.5 and 15.12.6, tagged R6 only; review finding 24 and B14 items 5-6: 15.12.5) |
| 107 | 15.12.6 | 313-316 | yes | L(configured, witness, agreement, control) D(packet A §6: §15.12.6; packet E: 15.12.5 and 15.12.6, tagged R6 only; review finding 24 and B14 item 6: 15.12.6) |
| 108 | 15.13.1 | 320-321 | yes | L(HELD / held) D(packet A §6: §15.13.1-4) |
| 109 | 15.13.2 | 322-323 | yes | D(packet A §6: §15.13.1-4) |
| 110 | 15.13.3 | 324-324 | yes | D(packet A §6: §15.13.1-4) |
| 111 | 15.13.4 | 325-327 | yes | L(HELD / held) D(packet A §6: §15.13.1-4) |
| 112 | 15.13.5 | 328-330 | yes | L(HELD / held) |
| 119 | 15.13.11 | 368-373 | yes | T L(REFERENCE-ONLY, agreement, HELD / held, control) D(packet A §6: §15.13.11; review finding 24 and A20: 15.13.11) |
| 121 | 15.14 ¶ [open: amended set "reporting"] Every authoritat | 379-381 |  | D(packet A §6: §15.14) |
| 128 | 15.15 row: 15.3 and 15.4: the session, read-once ports, its | 392-392 | yes | L(HELD / held) |
| 138 | 15.15 row: 15.13.11: REFERENCE-ONLY until 1b, against R6 (f | 402-402 | yes | T L(REFERENCE-ONLY) D(packet A §6: the §15.15 row) |

## A_r for the PREFIX licence (B1 + 4a + 5c + K1)

Terms the ruling defines or newly defines: PREFIX / prefix, licence, exempt, boundary, first input, first port declaration, closure, Reach, may execute, statement kind, oracle. The closure over 15.0's definitions adds: none.

|A_r| = 39 clauses (T_r 2, L_r 16, D_r 36; a clause may be in several); 24 of them among the 74.

| # | clause | lines | in the 74 | why |
|---|---|---|---|---|
| 11 | 15.0 Version 1 law | 30-31 |  | D(packet B §5: §15.0) |
| 12 | 15.0 Port | 32-34 |  | D(packet B §5: §15.0; review audit A1: 15.0 Port) |
| 13 | 15.0 Prefix | 35-36 | yes | L(PREFIX / prefix) D(packet B §5: §15.0) |
| 14 | 15.0 Arrival | 37-39 | yes | D(packet B §5: §15.0) |
| 15 | 15.0 Input log | 40-40 | yes | D(packet B §5: §15.0) |
| 16 | 15.0 Execution | 41-41 | yes | D(packet B §5: §15.0) |
| 19 | 15.1.3 | 52-57 |  | D(packet B §5: §15.1.3; review A19's missing dependency: 15.1.3; review audit: 15.1.3) |
| 22 | 15.1.6 | 63-66 | yes | D(packet B §5: §15.1.6; packet E: L_r candidates; review audit: 15.1.6) |
| 27 | 15.2.3 | 82-89 | yes | L(PREFIX / prefix, boundary) |
| 40 | 15.3 Read-once ports have no event in this table yet. | 122-124 | yes | L(PREFIX / prefix) D(packet B §5: §15.3's read-once bullet) |
| 50 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 149-150 |  | D(packet B §5: §15.5) |
| 51 | 15.5 The header | 151-151 |  | D(packet B §5: §15.5) |
| 52 | 15.5 One record for the read-once ports, then one record per tick | 152-154 |  | D(packet B §5: §15.5) |
| 53 | 15.5 Optionally, one end record | 155-156 |  | D(packet B §5: §15.5) |
| 54 | 15.5 A log with no end record is open. | 157-157 |  | D(packet B §5: §15.5) |
| 55 | 15.5 The log is parsed whole before any execution starts. | 158-159 | yes | D(packet B §5: §15.5) |
| 56 | 15.5 Load refusals | 160-163 | yes | D(packet B §5: §15.5) |
| 57 | 15.5 The chain | 164-165 |  | D(packet B §5: §15.5) |
| 58 | 15.5 `input-log-sha256` | 166-167 |  | D(packet B §5: §15.5) |
| 60 | 15.7.1 | 178-181 |  | L(PREFIX / prefix) D(integration I-3: the binding place, 15.7.1; packet B §5: §15.7.1) |
| 64 | 15.7.5 | 197-201 |  | L(PREFIX / prefix) D(packet B §5: §15.7.5) |
| 95 | 15.10 ¶ - T(1).c is the prefix's count; | 269-269 |  | L(PREFIX / prefix) |
| 101 | 15.12.1 | 287-288 |  | D(packet B §5: §15.12.1-6; review finding 4: the trigger and the licence in a tick-only law, 15.12.1) |
| 102 | 15.12.2 | 289-290 | yes | L(licence) D(packet B §5: §15.12.1-6) |
| 103 | 15.12.3 | 291-292 | yes | D(packet B §5: §15.12.1-6) |
| 104 | 15.12.4 | 293-303 | yes | L(PREFIX / prefix, licence, exempt, first input, first port declaration) D(packet B §5: §15.12.1-6; packet E: L_r candidates; review finding 3, A19, B14 item 4: 15.12.4 and its open note) |
| 105 | 15.12 ¶ [open: amended set "PREFIX": the licence by stat | 305-310 | yes | T L(PREFIX / prefix, licence, exempt, first input, first port declaration, closure) D(packet B §5: §15.12.1-6; review finding 3, A19, B14 item 4: 15.12.4 and its open note) |
| 106 | 15.12.5 | 311-312 | yes | L(PREFIX / prefix) D(packet B §5: §15.12.1-6; packet E: L_r candidates) |
| 107 | 15.12.6 | 313-316 | yes | L(PREFIX / prefix, licence) D(packet B §5: §15.12.1-6; packet E: L_r candidates) |
| 114 | 15.13.7 | 333-336 | yes | D(packet B §5: §15.13.7-8) |
| 115 | 15.13.8 | 337-355 | yes | L(may execute) D(integration I-9: Reach shared with K-hat, 15.13.8; packet B §5: §15.13.7-8) |
| 116 | 15.13 ¶ What "may execute" reaches includes every proced | 357-357 |  | L(may execute) D(integration I-9: Reach shared with K-hat, 15.13.8; packet B §5: §15.13.7-8) |
| 119 | 15.13.11 | 368-373 | yes | L(PREFIX / prefix) D(packet B §5: §15.13.11; packet E: L_r candidates) |
| 124 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 388-388 | yes | D(packet B §5: §15.15 row) |
| 127 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 391-391 | yes | L(PREFIX / prefix) |
| 128 | 15.15 row: 15.3 and 15.4: the session, read-once ports, its | 392-392 | yes | D(packet B §5: §15.15 rows) |
| 129 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 393-393 | yes | D(packet B §5: §15.15 rows) |
| 136 | 15.15 row: 15.12.4: PREFIX by static closure; a law with no | 400-400 | yes | T L(PREFIX / prefix, closure) D(packet B §5: §15.15 row) |
| 138 | 15.15 row: 15.13.11: REFERENCE-ONLY until 1b, against R6 (f | 402-402 | yes | D(packet B §5: §15.15 row) |

## The union

57 clauses are in A_F24 or A_PREFIX; 7 in both; 40 of the union are among the 74; 34 of the 74 are in neither.

## Dependencies found later (2026-10-26, from re-read 1)

R7, point 4: "A dependency identified later enters D_r and is recorded." The twin's re-read found five
(`REREAD-1-REPORT.md`; disposed in `REREAD-1-DISPOSITION.md`):

- **A_F24 gains** 15.13.6 (CUT-0 "holds" a claim: the term match took "held" and missed "holds"), 15.13.10 (T10, T11
  and CUT-0's soundness, which his scope sentence names) and 15.13.12 (the order of standings beside REFERENCE-ONLY).
  The twin's F24-9.
- **A_PREFIX gains** 15.1.1 (the forms: the port declaration and the budgeted tick block are statement kinds the closure
  needs rules for) and 15.13.6. The twin's PREFIX-13. SPEC §3's statement table, which it also names, is the source of
  the closure's rule table and not a clause of §15.

They are read at the next re-read, in the text the next draft leaves.
