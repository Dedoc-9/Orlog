# A_r for his answers of 2026-10-27 on re-read 4: the stop's carrier, the owed check, the order of work

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His three answers (`RULINGS.md`, "The stop's carrier, the owed check, and the order of work") come after the one
re-read before the gate. By his ruling on that re-read, *"Any further drafting fixes must be recorded with their
required re-read before the build, as R7 requires."* So these sets are recorded now and re-read with draft 7 before
anything is built. Draft 6 is not changed by them.

## How the sets were computed

By `ar_compute.py 6`, the same way as before, over `SPEC-15-DRAFT-6.md`, the text current when he answered. The
script refuses any other text than sha256 `e9e3f442bbd51ec2e5ca7a9b45027ad3a5bb82d61581b95fde36e2cb26aa76cf`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 6`; its whole output is below, unedited.
Its sets 1 to 5 still print their records byte for byte.

- **T_r:** the clauses tagged with finding 6, which all three answers refine.
- **L_r:**
  - for the carrier: receipt, status, LOG-OPEN and the read-once stop;
  - for the check: version-1 check and stand-ins;
  - for the order: the pin, digest and 1a.
- **D_r:** the clauses re-read 4 named for each: the statuses (15.7.5), the receipt's status line, the stop's row and
  what 15.15 lists open; the stop's row and 15.15's row on the check; the meet's digest (15.13.4), 1a's rows (15.12.5,
  15.12.6, 15.13.11) and the stop's row.

## The computed sets

Draft 6: 159 clauses; 20 changed or added since draft 5 (DRAFT-6-CHANGES.md).

## A_r for the read-once stop's own receipt status (his answer on STOPROW-1)

Terms the ruling defines or newly defines: receipt, status, LOG-OPEN, the read-once stop. The closure over 15.0's definitions adds: none.

|A_r| = 44 clauses (T_r 9, L_r 23, D_r 24; a clause may be in several); 15 of them changed since draft 5.

| # | clause | lines | changed since draft 5 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 6 applies to draft 5 the drafting  | 3-8 | yes | L(the read-once stop) |
| 12 | preamble [ruled: F6] | 29-30 | yes | T L(the read-once stop) |
| 45 | 15.3 Read-once ports. | 140-148 | yes | T |
| 52 | 15.4 Three records, three authorities | 162-165 |  | L(receipt) |
| 54 | 15.4 Two histories with one input log share one core. | 168-169 |  | L(receipt) |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 176-180 | yes | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 184-188 | yes | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 189-192 | yes | T |
| 62 | 15.5 Load refusals | 193-196 |  | L(receipt) |
| 66 | 15.7.1 | 211-223 | yes | T L(LOG-OPEN) |
| 70 | 15.7.5 | 239-247 | yes | T L(receipt, status, LOG-OPEN) D(re-read 4, STOPROW-1: the statuses, 15.7.5) |
| 73 | 15.8 ¶ - orlog-receipt 1 | 261-261 |  | L(receipt) |
| 76 | 15.8 ¶ - status (§15.7.5) | 264-264 |  | L(status) D(re-read 4, STOPROW-1: the receipt's status line) |
| 87 | 15.8 The core | 278-279 |  | L(receipt) |
| 88 | 15.8 The frame check is versioned. | 280-283 |  | L(receipt) |
| 89 | 15.8 No receipt line states that a run is valid or correct. | 284-284 |  | L(receipt) |
| 102 | 15.10 ¶ - the receipt's ops minus the last 'T''s c is th | 316-316 |  | L(receipt) |
| 104 | 15.11 Replay. | 322-326 |  | L(receipt) |
| 109 | 15.12.3 | 339-340 |  | L(receipt) |
| 124 | 15.12.6 | 406-421 |  | L(receipt) |
| 132 | 15.13.8 | 445-474 | yes | T L(LOG-OPEN, the read-once stop) D(re-read 4, STOPROW-1: the stop's row, 15.13.8) |
| 134 | 15.13.9 | 480-483 | yes | T L(the read-once stop) |
| 138 | 15.14 ¶ [open: amended set "reporting"] Every authoritat | 515-520 |  | L(receipt) |
| 139 | 15.15 row: clause | 524-525 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 526-526 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 527-527 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 142 | 15.15 row: 15.1.5: the door and the forms | 528-528 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 143 | 15.15 row: 15.1.6: world properties | 529-529 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 530-530 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 145 | 15.15 row: 15.3 and 15.4: the session, its record and the b | 531-531 | yes | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 532-532 |  | L(receipt) D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 533-533 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 534-534 |  | L(status) D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 149 | 15.15 row: 15.7.6: out_0's reading and domain string | 535-535 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 536-536 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 537-537 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 152 | 15.15 row: 15.11 and 15.8: replay, and "never reported as v | 538-538 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 153 | 15.15 row: 15.13.9: the row named when two rows withhold on | 539-539 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 154 | 15.15 row: 15.3 and 15.7.1: the events that fill and close  | 540-540 | yes | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 541-541 | yes | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 check, o | 542-542 | yes | L(the read-once stop) D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 157 | 15.15 row: 15.13.11: D10's two-commit split | 543-543 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 158 | 15.15 row: 15.14: the authority rule; the labels of a confi | 544-544 |  | D(re-read 4, STOPROW-1: what 15.15 lists open) |
| 159 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 546-550 | yes | L(the read-once stop) D(re-read 4, STOPROW-1: what 15.15 lists open) |

## A_r for the owed version-1 check is containment (his answer on V1CHECK-2)

Terms the ruling defines or newly defines: version-1 check, stand-ins. The closure over 15.0's definitions adds: none.

|A_r| = 12 clauses (T_r 9, L_r 5, D_r 2; a clause may be in several); 12 of them changed since draft 5.

| # | clause | lines | changed since draft 5 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 6 applies to draft 5 the drafting  | 3-8 | yes | L(version-1 check) |
| 12 | preamble [ruled: F6] | 29-30 | yes | T L(version-1 check) |
| 45 | 15.3 Read-once ports. | 140-148 | yes | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 176-180 | yes | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 184-188 | yes | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 189-192 | yes | T |
| 66 | 15.7.1 | 211-223 | yes | T |
| 70 | 15.7.5 | 239-247 | yes | T |
| 132 | 15.13.8 | 445-474 | yes | T L(version-1 check, stand-ins) D(re-read 4, V1CHECK-2: the stop's row, 15.13.8) |
| 134 | 15.13.9 | 480-483 | yes | T |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 check, o | 542-542 | yes | L(version-1 check) D(re-read 4, V1CHECK-2: 15.15's row on the check) |
| 159 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 546-550 | yes | L(version-1 check) |

## A_r for check, then pin, then 1a (his answer on V1CHECK-3)

Terms the ruling defines or newly defines: the pin, digest, 1a. The closure over 15.0's definitions adds: none.

|A_r| = 26 clauses (T_r 9, L_r 19, D_r 5; a clause may be in several); 11 of them changed since draft 5.

| # | clause | lines | changed since draft 5 | why |
|---|---|---|---|---|
| 8 | preamble [pinned] | 19-21 |  | L(the pin, digest) |
| 12 | preamble [ruled: F6] | 29-30 | yes | T |
| 30 | 15.2.1 | 96-97 |  | L(1a) |
| 45 | 15.3 Read-once ports. | 140-148 | yes | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 176-180 | yes | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 184-188 | yes | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 189-192 | yes | T |
| 66 | 15.7.1 | 211-223 | yes | T |
| 70 | 15.7.5 | 239-247 | yes | T |
| 93 | 15.10 ¶ [ruled: R5: part of 1a] Written by an execution  | 303-304 |  | L(1a) |
| 97 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 308-310 |  | L(digest, 1a) |
| 103 | 15.10 ¶ The state digest's cost on a large state is for  | 318-318 |  | L(digest, 1a) |
| 105 | 15.11 Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity. | 327-328 |  | L(digest) |
| 123 | 15.12.5 | 402-405 |  | L(1a) D(re-read 4, V1CHECK-3: 1a's rows, 15.12.5) |
| 124 | 15.12.6 | 406-421 |  | L(1a) D(re-read 4, V1CHECK-3: 1a's rows, 15.12.6) |
| 128 | 15.13.4 | 432-435 |  | L(digest) D(re-read 4, V1CHECK-3: the meet's digest, 15.13.4) |
| 129 | 15.13.5 | 436-438 |  | L(the pin) |
| 130 | 15.13.6 | 439-440 |  | L(the pin) |
| 131 | 15.13.7 | 441-444 |  | L(the pin) |
| 132 | 15.13.8 | 445-474 | yes | T L(the pin, digest) D(re-read 4, V1CHECK-3: the stop's row, 15.13.8) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 476-479 | yes | L(the pin) |
| 134 | 15.13.9 | 480-483 | yes | T L(the pin) |
| 136 | 15.13.11 | 491-509 |  | L(1a) D(re-read 4, V1CHECK-3: 1a's rows, 15.13.11) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 530-530 |  | L(1a) |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 537-537 |  | L(digest, 1a) |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 check, o | 542-542 | yes | L(the pin) |

## The union

57 clauses are in A_CARRIER, A_CONTAIN or A_ORDER; 15 in more than one; 16 of them changed since draft 5; 4 of the clauses changed since draft 5 are in none.
