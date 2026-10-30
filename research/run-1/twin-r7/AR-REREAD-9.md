# A_r for his rulings of 2026-10-28 and 2026-10-29, read with draft 11

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His rulings since draft 10 (`RULINGS.md`): finding 8 (packet G, the read-once record's line, packet D's D1 to D3 and
typed values), finding 20, R2 with R2.3's clarification, the port place, counting and the budget, N2, N3 and finding
10; and re-read 8's three fixes. He asked that the twin read the whole of draft 11, so these sets do not bound the
re-read; they record which clauses each ruling reaches, as R7 requires.

## How the sets were computed

By `ar_compute.py 10`, the same way as before, over `SPEC-15-DRAFT-10.md`, the text current when he ruled. The script
refuses any other text than sha256 `c69e7e3b02542a5cb6b320de1c5994786f2425d04bbfdb1c7e45ce1741098eb7`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 10`; its whole output is below, unedited.
Its sets 1 to 9 still print their records byte for byte. Each group's T_r, L_r and D_r are in the script's `RULINGS10`;
D_r names whole sections where a ruling rewrote one (15.0, 15.1, 15.3, 15.4, 15.5, 15.7, 15.9).

## The computed sets

Draft 10: 160 clauses; 12 changed or added since draft 9 (DRAFT-10-CHANGES.md).

## A_r for finding 8: packet G, the read-once record's line, packet D and typed values (2026-10-28, 2026-10-29)

Terms the ruling defines or newly defines: status, NOT-RUN, LOG-OPEN, end record, the read-once record, load refusal, value encoding. The closure over 15.0's definitions adds: none.

|A_r| = 34 clauses (T_r 21, L_r 24, D_r 17; a clause may be in several); 5 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 12 | preamble [ruled: F6] | 31-33 |  | T L(status) |
| 20 | 15.0 Input log | 55-55 |  | T |
| 41 | 15.3 row: `close()` | 139-139 |  | L(NOT-RUN) |
| 45 | 15.3 Read-once ports. | 147-155 |  | T L(the read-once record) |
| 55 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 180-181 |  | T D(re-read 8 and finding 8: the input log, 15.5) |
| 56 | 15.5 The header | 182-182 |  | D(re-read 8 and finding 8: the input log, 15.5) |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 183-187 |  | T L(the read-once record, value encoding) D(re-read 8 and finding 8: the input log, 15.5) |
| 58 | 15.5 Optionally, one end record | 188-189 |  | L(end record) D(re-read 8 and finding 8: the input log, 15.5) |
| 59 | 15.5 A log with no end record is open. | 190-190 |  | L(end record) D(re-read 8 and finding 8: the input log, 15.5) |
| 60 | 15.5 A well-formed log may lack the read-once record | 191-195 |  | T L(NOT-RUN, the read-once record) D(re-read 8 and finding 8: the input log, 15.5) |
| 61 | 15.5 The log is parsed whole before any execution starts. | 196-199 |  | T L(the read-once record) D(re-read 8 and finding 8: the input log, 15.5) |
| 62 | 15.5 Load refusals | 200-203 |  | T L(load refusal) D(re-read 8 and finding 8: the input log, 15.5) |
| 63 | 15.5 The chain | 204-205 |  | L(the read-once record) D(re-read 8 and finding 8: the input log, 15.5) |
| 64 | 15.5 `input-log-sha256` | 206-207 |  | L(end record) D(re-read 8 and finding 8: the input log, 15.5) |
| 65 | 15.6 ¶ [open: amended set "identity and bytes"] SHA-256 | 211-214 |  | T |
| 66 | 15.7.1 | 218-231 |  | T L(NOT-RUN, LOG-OPEN, end record, the read-once record, load refusal) |
| 70 | 15.7.5 | 247-263 | yes | T L(status, NOT-RUN, LOG-OPEN, end record, the read-once record, load refusal) D(finding 8: the statuses, 15.7.5) |
| 71 | 15.7.6 | 264-272 |  | T |
| 76 | 15.8 ¶ - status (§15.7.5) | 280-280 |  | L(status) D(finding 8: the status line, 15.8) |
| 78 | 15.8 ¶ - tick-ops <n>: the last begun tick's own count, | 282-283 |  | T |
| 79 | 15.8 ¶ - the count of tick records left unread after a  | 284-284 |  | T |
| 85 | 15.8 ¶ The line order is this draft's. [open: amended s | 291-291 |  | T |
| 91 | 15.9 `'N'`'s payload | 306-306 |  | L(value encoding) D(typed values: 'N''s payload, 15.9) |
| 97 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 329-331 |  | L(value encoding) |
| 128 | 15.13.4 | 455-474 | yes | L(status, NOT-RUN, LOG-OPEN, load refusal) |
| 132 | 15.13.8 | 484-538 | yes | T L(status, NOT-RUN, LOG-OPEN, the read-once record, load refusal) D(finding 8: the rows chosen by the status, 15.13.8) |
| 134 | 15.13.9 | 544-547 |  | T |
| 145 | 15.15 row: 15.3 and 15.4: the session, its record and the b | 596-596 |  | L(end record) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 597-597 |  | T L(the read-once record, load refusal) D(finding 8: 15.15's rows on 15.5) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 599-599 | yes | T L(status, NOT-RUN, LOG-OPEN, load refusal) D(finding 8: 15.15's row on the statuses) |
| 149 | 15.15 row: 15.7.6: out_0's reading and domain string | 600-600 |  | T |
| 154 | 15.15 row: 15.3 and 15.7.1: the events that fill and close  | 605-605 |  | L(the read-once record) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 606-606 |  | T L(status, NOT-RUN) D(finding 8: 15.15's rows on 15.5) |
| 160 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 612-621 | yes | L(status) |

## A_r for finding 20: the cut in version 1's 'R' (F20.1 to F20.4)

Terms the ruling defines or newly defines: 'R', the cut, frame, decoding. The closure over 15.0's definitions adds: none.

|A_r| = 11 clauses (T_r 2, L_r 8, D_r 6; a clause may be in several); 4 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 88 | 15.8 The frame check is versioned. | 296-299 |  | L(frame) |
| 90 | 15.9 The head. | 304-305 |  | D(finding 20: the trace, 15.9) |
| 91 | 15.9 `'N'`'s payload | 306-306 |  | D(finding 20: the trace, 15.9) |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 307-320 | yes | T L('R', the cut, frame, decoding) D(finding 20: the trace, 15.9) |
| 124 | 15.12.6 | 428-444 |  | L(frame) |
| 125 | 15.13.1 | 448-451 |  | L(the cut) |
| 128 | 15.13.4 | 455-474 | yes | L('R', the cut, decoding) |
| 130 | 15.13.6 | 478-479 |  | L(the cut) |
| 132 | 15.13.8 | 484-538 | yes | L('R', the cut, frame) D(finding 20: the cut and K-hat, 15.13.8) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 540-543 |  | D(finding 20: CUT-0's reach) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 601-601 | yes | T L('R', the cut, frame, decoding) D(finding 20: 15.15's row on 15.9) |

## A_r for R2: statement kinds, spellings and reach rules, with R2.3's clarification

Terms the ruling defines or newly defines: spelling, statement kind, tick block, port declaration, reach. The closure over 15.0's definitions adds: Boundary, Prefix, Version 1 law.

|A_r| = 38 clauses (T_r 6, L_r 32, D_r 17; a clause may be in several); 9 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 10 applies to draft 9 the fixes R7 | 3-8 | yes | L(reach) |
| 11 | preamble [fixed] | 28-30 |  | L(spelling) |
| 15 | 15.0 Version 1 law | 43-44 |  | L(tick block, Version 1 law) D(R2: the terms, 15.0) |
| 16 | 15.0 Port | 45-47 |  | T D(R2: the terms, 15.0) |
| 17 | 15.0 Prefix | 48-49 |  | T L(tick block, Prefix) D(R2: the terms, 15.0) |
| 18 | 15.0 Boundary | 50-51 |  | L(tick block, port declaration, Boundary) D(R2: the terms, 15.0) |
| 19 | 15.0 Arrival | 52-54 |  | D(R2: the terms, 15.0) |
| 20 | 15.0 Input log | 55-55 |  | D(R2: the terms, 15.0) |
| 21 | 15.0 Execution | 56-56 |  | D(R2: the terms, 15.0) |
| 22 | 15.1.1 | 60-67 | yes | T L(spelling, statement kind, tick block, reach) D(R2: the forms, 15.1) |
| 23 | 15.1.2 | 68-69 |  | D(R2: the forms, 15.1) |
| 24 | 15.1.3 | 70-79 |  | T L(tick block) D(R2: the forms, 15.1) |
| 25 | 15.1.4 | 80-80 |  | D(R2: the forms, 15.1) |
| 26 | 15.1.5 | 81-84 |  | L(reach) D(R2: the forms, 15.1) |
| 27 | 15.1.6 | 85-91 |  | L(reach, Boundary) D(R2: the forms, 15.1) |
| 33 | 15.2.4 | 115-116 |  | L(spelling) |
| 45 | 15.3 Read-once ports. | 147-155 |  | L(reach) |
| 66 | 15.7.1 | 218-231 |  | L(tick block) |
| 67 | 15.7.2 | 232-238 |  | L(tick block) |
| 70 | 15.7.5 | 247-263 | yes | L(reach) |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 307-320 | yes | L(tick block) |
| 107 | 15.12.1 | 354-355 |  | L(tick block) |
| 110 | 15.12.4 | 362-372 |  | L(tick block, port declaration) D(R2.3: the closure's table, 15.12.4) |
| 111 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 374-402 |  | L(statement kind, tick block, port declaration, reach, Boundary) D(R2.3: the licence as ruled) |
| 113 | 15.12 row: statement kind | 407-408 |  | L(statement kind) |
| 117 | 15.12 row: the tick block | 412-412 |  | L(tick block) |
| 119 | 15.12 row: To, Define, Decimals | 414-414 |  | L(reach) |
| 120 | 15.12 row: Let, Set, Increase, Decrease, Say, Append, Remov | 415-415 |  | L(port declaration, reach) |
| 128 | 15.13.4 | 455-474 | yes | L(spelling, reach) |
| 132 | 15.13.8 | 484-538 | yes | L(tick block) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 540-543 |  | L(tick block, port declaration, reach) D(R2.3 and re-read 8's ROWS-1: CUT-0's reach) |
| 134 | 15.13.9 | 544-547 |  | L(tick block) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 591-591 | yes | T L(spelling) D(R2: 15.15's row on 15.0 and 15.1) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 592-592 |  | T L(tick block) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 595-595 |  | L(spelling) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 601-601 | yes | L(tick block) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 607-607 |  | L(reach) |
| 160 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 612-621 | yes | L(reach) |

## A_r for the port place, PP1 to PP6

Terms the ruling defines or newly defines: place, top-level, compile code. The closure over 15.0's definitions adds: Boundary, Prefix, Tick block.

|A_r| = 13 clauses (T_r 6, L_r 13, D_r 3; a clause may be in several); 3 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 17 | 15.0 Prefix | 48-49 |  | T L(place, top-level, Prefix, Tick block) |
| 18 | 15.0 Boundary | 50-51 |  | L(top-level, Boundary) |
| 24 | 15.1.3 | 70-79 |  | T L(place, top-level, compile code) D(PP: the places, 15.1.3) |
| 27 | 15.1.6 | 85-91 |  | L(Boundary) |
| 66 | 15.7.1 | 218-231 |  | L(place, top-level) |
| 97 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 329-331 |  | L(top-level) |
| 111 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 374-402 |  | T L(place, top-level, Boundary) D(PP: the licence's boundary) |
| 128 | 15.13.4 | 455-474 | yes | L(place) |
| 132 | 15.13.8 | 484-538 | yes | L(place, top-level) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 591-591 | yes | T L(place) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 592-592 |  | T L(place) D(PP: 15.15's row on 15.1.3) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 598-598 |  | L(place) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 607-607 |  | T L(place) |

## A_r for counting (C1 to C3) and the budget (R9, B1 to B4)

Terms the ruling defines or newly defines: ops, count, budget, tick-ops. The closure over 15.0's definitions adds: none.

|A_r| = 22 clauses (T_r 7, L_r 19, D_r 9; a clause may be in several); 6 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 22 | 15.1.1 | 60-67 | yes | L(budget) |
| 25 | 15.1.4 | 80-80 |  | L(budget) |
| 66 | 15.7.1 | 218-231 |  | T L(count) D(counting and R9: execution, 15.7) |
| 67 | 15.7.2 | 232-238 |  | T L(count) D(counting and R9: execution, 15.7) |
| 68 | 15.7.3 | 239-244 |  | T L(count, budget) D(counting and R9: execution, 15.7) |
| 69 | 15.7.4 | 245-246 |  | D(counting and R9: execution, 15.7) |
| 70 | 15.7.5 | 247-263 | yes | D(counting and R9: execution, 15.7) |
| 71 | 15.7.6 | 264-272 |  | D(counting and R9: execution, 15.7) |
| 78 | 15.8 ¶ - tick-ops <n>: the last begun tick's own count, | 282-283 |  | L(ops, count, budget, tick-ops) D(B3: tick-ops, 15.8) |
| 79 | 15.8 ¶ - the count of tick records left unread after a  | 284-284 |  | L(count) |
| 82 | 15.8 ¶ - ops: every counted operation, the refused one  | 287-287 |  | L(ops, count) |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 307-320 | yes | L(count) |
| 94 | 15.10 ¶ - tick <t>, events <n>, ops <n> (the tick's own  | 326-326 |  | L(ops, count) |
| 99 | 15.10 ¶ These must hold, under §15.7.2's running-total r | 334-334 |  | T L(count) D(C2: the tick line's identities, 15.10) |
| 100 | 15.10 ¶ - T(t+1).c − T(t).c equals tick t's ops; | 335-335 |  | L(ops) |
| 101 | 15.10 ¶ - T(1).c is the prefix's count; | 336-336 |  | L(count) |
| 102 | 15.10 ¶ - the receipt's ops minus the last 'T''s c is th | 337-337 |  | L(ops, count) |
| 128 | 15.13.4 | 455-474 | yes | L(count) |
| 132 | 15.13.8 | 484-538 | yes | T L(count) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 598-598 |  | T L(count, budget) D(counting: 15.15's row on 15.7.1 to 15.7.3) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 599-599 | yes | L(ops, count, tick-ops) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 607-607 |  | T L(count) |

## A_r for N2, N3 and finding 10: the session's ends

Terms the ruling defines or newly defines: end(), session, history, verifier. The closure over 15.0's definitions adds: Session.

|A_r| = 24 clauses (T_r 8, L_r 20, D_r 21; a clause may be in several); 0 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 19 | 15.0 Arrival | 52-54 |  | T L(history, Session) |
| 36 | 15.3 ¶ [open: amended set "A2", with the declared polic | 131-132 |  | T D(N2, N3 and finding 10: the session's events, 15.3) |
| 37 | 15.3 row: event | 134-135 |  | D(N2, N3 and finding 10: the session's events, 15.3) |
| 38 | 15.3 row: `arrive(port, source, bytes)` | 136-136 |  | L(session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 39 | 15.3 row: `assign(arrival, tick)` | 137-137 |  | D(N2, N3 and finding 10: the session's events, 15.3) |
| 40 | 15.3 row: `drop(arrival)` | 138-138 |  | D(N2, N3 and finding 10: the session's events, 15.3) |
| 41 | 15.3 row: `close()` | 139-139 |  | L(session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 42 | 15.3 row: `end()` | 140-140 |  | L(end(), session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 43 | 15.3 Any other move is refused by its rule's name | 142-144 |  | L(session, history) D(N2, N3 and finding 10: the session's events, 15.3) |
| 44 | 15.3 Every arrival has exactly one disposition | 145-146 |  | L(history) D(N2, N3 and finding 10: the session's events, 15.3) |
| 45 | 15.3 Read-once ports. | 147-155 |  | T L(end(), session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 46 | 15.3 No value is invented, held over or defaulted, | 156-157 |  | T L(session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 47 | 15.3 A retry is a new arrival; | 158-159 |  | L(history) D(N2, N3 and finding 10: the session's events, 15.3) |
| 48 | 15.3 A door refusal or a refused move does not end the session. | 160-160 |  | T L(session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 49 | 15.3 Until SNAP-1, a refusal of the run ends the session. | 161-163 |  | L(session) D(N2, N3 and finding 10: the session's events, 15.3) |
| 50 | 15.4 ¶ [open: amended set "session record" and "binding | 167-167 |  | T L(session) D(finding 10: the verifier, 15.4) |
| 51 | 15.4 The history is a record of its own | 168-168 |  | L(history) D(finding 10: the verifier, 15.4) |
| 52 | 15.4 Three records, three authorities | 169-172 |  | L(session, history) D(finding 10: the verifier, 15.4) |
| 53 | 15.4 The verifier checks the chain | 173-174 |  | L(history, verifier) D(finding 10: the verifier, 15.4) |
| 54 | 15.4 Two histories with one input log share one core. | 175-176 |  | L(session, history) D(finding 10: the verifier, 15.4) |
| 66 | 15.7.1 | 218-231 |  | L(history, verifier) |
| 131 | 15.13.7 | 480-483 |  | L(session) |
| 145 | 15.15 row: 15.3 and 15.4: the session, its record and the b | 596-596 |  | T L(session) D(N2 and N3: 15.15's rows on 15.3) |
| 154 | 15.15 row: 15.3 and 15.7.1: the events that fill and close  | 605-605 |  | T L(end()) D(N2 and N3: 15.15's rows on 15.3) |

## A_r for re-read 8's three fixes (ROWS-1, ROWS-2, CHANGED-1)

Terms the ruling defines or newly defines: . The closure over 15.0's definitions adds: none.

|A_r| = 4 clauses (T_r 0, L_r 0, D_r 4; a clause may be in several); 2 of them changed since draft 9.

| # | clause | lines | changed since draft 9 | why |
|---|---|---|---|---|
| 70 | 15.7.5 | 247-263 | yes | D(CHANGED-1: the stop's NOT-RUN t, 15.7.5) |
| 128 | 15.13.4 | 455-474 | yes | D(ROWS-2: the inputs record, 15.13.4) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 540-543 |  | D(ROWS-1: CUT-0's reach on the version-1 kinds) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 607-607 |  | D(ROWS-1: 15.15's row on 15.13.8) |

## The union

96 clauses are in A_F8, A_F20, A_R2, A_PP, A_R9, A_SESSION or A_ROWS; 33 in more than one; 10 of them changed since draft 9; 2 of the clauses changed since draft 9 are in none.
