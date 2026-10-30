# A_r for his answer of 2026-10-27 on re-read 7: the principle reaches every row of CUT-0

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answer (`RULINGS.md`, "The principle reaches every row of CUT-0") comes after re-read 7. This set is
recorded before draft 10 is re-read.

## How the set was computed

By `ar_compute.py 9`, the same way as before, over `SPEC-15-DRAFT-9.md`, the text current when he answered. The script
refuses any other text than sha256 `8a1ccf5ce22895d0106884b1208603315c80704f781adb87c3b2e520289d0e8e`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 9`; its whole output is below, unedited.
Its sets 1 to 8 still print their records byte for byte.

- **T_r:** the clauses tagged with what the clarification brings before the pin: the claims ruling, whose pin it is;
  finding 6, whose rows read the statuses; R2; and the amended set's "identity and bytes" and "four statuses".
- **L_r:** the pin, status, NOT-RUN, LOG-OPEN, R2, spelling, statement kind and inputs; closed over §15.0's
  definitions.
- **D_r:** the clauses re-read 7 named: the order and the inputs (15.13.4), the NOT-RUN/LOG-OPEN row and the test's
  record (15.13.8), CUT-0's reach on the version-1 kinds, the statuses (15.7.5) and the status line, the spellings
  (15.1.1) and the closure's table (15.12.4), 15.15's rows on spellings and on the four statuses (INPUTS-2); `'R'` and
  its frames (15.9) and 15.15's row on it (INPUTS-1).

## The computed set

Draft 9: 160 clauses; 15 changed or added since draft 8 (DRAFT-9-CHANGES.md).

## A_r for the principle reaches every row of CUT-0 (his clarification on INPUTS-2)

Terms the ruling defines or newly defines: the pin, status, NOT-RUN, LOG-OPEN, R2, spelling, statement kind, inputs. The closure over 15.0's definitions adds: Execution, Port.

|A_r| = 72 clauses (T_r 36, L_r 57, D_r 11; a clause may be in several); 14 of them changed since draft 8.

| # | clause | lines | changed since draft 8 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 9 applies to draft 8 the fixes R7' | 3-8 | yes | L(the pin, inputs) |
| 5 | preamble [ruled: claims] | 13-15 | yes | T L(the pin, inputs) |
| 8 | preamble [pinned] | 21-23 |  | L(the pin) |
| 10 | preamble [open: X] | 25-27 |  | L(R2) |
| 11 | preamble [fixed] | 28-30 |  | L(spelling) |
| 12 | preamble [ruled: F6] | 31-33 |  | T L(status) |
| 16 | 15.0 Port | 45-47 |  | T L(R2, inputs, Port) |
| 17 | 15.0 Prefix | 48-49 |  | T L(R2) |
| 20 | 15.0 Input log | 55-55 |  | T |
| 21 | 15.0 Execution | 56-56 |  | L(inputs, Execution) |
| 22 | 15.1.1 | 60-65 |  | T L(R2, statement kind) D(re-read 7, INPUTS-2: the spellings, 15.1.1) |
| 24 | 15.1.3 | 68-77 | yes | T L(the pin, R2, inputs) |
| 28 | 15.2 ¶ [ruled: R3] The door never rounds: a decimal tha | 93-96 |  | L(inputs) |
| 29 | 15.2 ¶ [open: contract draft 0 §1.2–§1.3] The door is a | 98-100 |  | L(inputs) |
| 33 | 15.2.4 | 113-114 |  | L(spelling) |
| 34 | 15.2.5 | 115-121 |  | L(inputs) |
| 35 | 15.2 ¶ [ruled: R3] The log holds typed encodings only ( | 123-125 |  | L(inputs) |
| 41 | 15.3 row: `close()` | 137-137 |  | L(NOT-RUN) |
| 45 | 15.3 Read-once ports. | 145-153 |  | T |
| 52 | 15.4 Three records, three authorities | 167-170 |  | L(inputs) |
| 54 | 15.4 Two histories with one input log share one core. | 173-174 |  | L(inputs) |
| 55 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 178-179 |  | T |
| 56 | 15.5 The header | 180-180 |  | L(inputs) |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 181-185 |  | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 189-193 |  | T L(NOT-RUN) |
| 61 | 15.5 The log is parsed whole before any execution starts. | 194-197 |  | T |
| 63 | 15.5 The chain | 202-203 |  | L(inputs) |
| 64 | 15.5 `input-log-sha256` | 204-205 |  | L(inputs) |
| 65 | 15.6 ¶ [open: amended set "identity and bytes"] SHA-256 | 209-212 |  | T |
| 66 | 15.7.1 | 216-229 | yes | T L(the pin, NOT-RUN, LOG-OPEN, inputs) |
| 70 | 15.7.5 | 245-259 | yes | T L(the pin, status, NOT-RUN, LOG-OPEN, inputs) D(re-read 7, INPUTS-2: the statuses, 15.7.5) |
| 71 | 15.7.6 | 260-268 |  | T |
| 75 | 15.8 ¶ - law-seal, text-seal, input-log-sha256 | 275-275 |  | L(inputs) |
| 76 | 15.8 ¶ - status (§15.7.5) | 276-276 |  | L(status) D(re-read 7, INPUTS-2: the status line, 15.8) |
| 78 | 15.8 ¶ - tick-ops <n>: the last begun tick's own count, | 278-279 |  | T |
| 79 | 15.8 ¶ - the count of tick records left unread after a  | 280-280 |  | T |
| 85 | 15.8 ¶ The line order is this draft's. [open: amended s | 287-287 |  | T |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 303-315 | yes | T L(the pin, inputs) D(re-read 7, INPUTS-1: 'R' and its frames, 15.9) |
| 98 | 15.10 ¶ - input-chain <hex>: in_t. [open: the speed verd | 327-327 |  | L(inputs) |
| 104 | 15.11 Replay. | 338-342 |  | L(inputs) |
| 107 | 15.12.1 | 349-350 |  | L(inputs) |
| 109 | 15.12.3 | 355-356 |  | L(inputs) |
| 110 | 15.12.4 | 357-367 |  | L(inputs) D(re-read 7, INPUTS-2: the closure's table, 15.12.4) |
| 111 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 369-397 |  | L(statement kind, inputs) |
| 113 | 15.12 row: statement kind | 402-403 |  | L(statement kind) |
| 123 | 15.12.5 | 418-422 |  | T L(the pin) |
| 124 | 15.12.6 | 423-439 |  | T L(the pin) |
| 125 | 15.13.1 | 443-446 |  | T |
| 126 | 15.13.2 | 447-448 |  | T |
| 127 | 15.13.3 | 449-449 |  | T |
| 128 | 15.13.4 | 450-463 | yes | T L(the pin, inputs) D(re-read 7, INPUTS-2: the order and the inputs, 15.13.4) |
| 129 | 15.13.5 | 464-466 |  | L(the pin) |
| 130 | 15.13.6 | 467-468 |  | L(the pin) |
| 131 | 15.13.7 | 469-472 |  | L(the pin, inputs) |
| 132 | 15.13.8 | 473-525 | yes | T L(the pin, status, NOT-RUN, LOG-OPEN, inputs) D(re-read 7, INPUTS-2: the NOT-RUN/LOG-OPEN row and the test's record, 15.13.8) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 527-530 |  | L(the pin) D(re-read 7, INPUTS-2: CUT-0's reach on the version-1 kinds) |
| 134 | 15.13.9 | 531-534 |  | T L(the pin) |
| 135 | 15.13.10 | 535-541 |  | T |
| 136 | 15.13.11 | 542-561 |  | T L(the pin) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 578-578 |  | T L(R2, spelling) D(re-read 7, INPUTS-2: 15.15's row on spellings) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 579-579 | yes | T L(the pin, R2, inputs) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 582-582 |  | L(spelling) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 584-584 | yes | T L(the pin, inputs) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 585-585 | yes | L(the pin, inputs) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 586-586 |  | T L(status) D(re-read 7, INPUTS-2: 15.15's row on the four statuses) |
| 149 | 15.15 row: 15.7.6: out_0's reading and domain string | 587-587 |  | T |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 588-588 | yes | L(the pin, inputs) D(re-read 7, INPUTS-1: 15.15's row on 'R') |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 589-589 |  | L(inputs) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 593-593 |  | T L(the pin, status, NOT-RUN) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 594-594 | yes | L(the pin) |
| 157 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 595-595 |  | L(the pin, inputs) |
| 160 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 599-607 | yes | L(the pin, status, inputs) |

## The union

72 clauses are in A_ROWS; 0 in more than one set; 14 of them changed since draft 8; 1 of the clauses changed since draft 8 are not in it.
