# A_r for his answers of 2026-10-27 on re-read 5: the containment test, findings 8 and 20, RO′-5

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answers (`RULINGS.md`, "The containment test, findings 8 and 20 before the pin, and the push") come after re-read 5.
His words: *"Draft 8 should incorporate the eight owed fixes and these decisions, record the affected clauses, and
undergo re-read 6."* These sets are those affected clauses, recorded before draft 8 is re-read. His word on the push
decides no clause of §15 and has no set.

## How the sets were computed

By `ar_compute.py 7`, the same way as before, over `SPEC-15-DRAFT-7.md`, the text current when he answered. The script
refuses any other text than sha256 `130480cafc0002377088da4de99c6cb11e5ded253efa20f900eaecf54a190a60`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 7`; its whole output is below, unedited.
Its sets 1 to 6 still print their records byte for byte.

- **T_r:** for the test and for RO′-5, the clauses tagged with finding 6, whose check and status they refine; for
  findings 8 and 20, also the clauses tagged with the claims ruling, whose pin it orders, and those tagged with
  either finding.
- **L_r:**
  - for the test: fixture, MEASURED, the version-1 reference, containment, falsifies, T10.8;
  - for findings 8 and 20: the pin, digest, candidate, finding 8, finding 20, `'R'` and 1a;
  - for RO′-5: status, NOT-RUN, LOG-OPEN, the read-once stop, fifth status.
- **D_r:** the clauses re-read 5 named for each: for the test (CONTAIN-2, ORDER-2), the stop's row and 15.15's row on
  the check, T10's open list (15.13.10), the order of work (15.13.4) and 1a's rows (15.12.5, 15.12.6, 15.13.11 and
  15.15's row on it); for findings 8 and 20 (ORDER-1), the order, the stop's row, the pin's reach, the statuses
  (15.7.5), the status line, `'R'` (15.9) and 15.15's rows on them; for RO′-5 (CARRIER-1 to CARRIER-3), the stop
  (15.7.1), the statuses, the status line, the stop's row and 15.15's rows on the statuses and the stop's form.

## The computed sets

Draft 7: 160 clauses; 12 changed or added since draft 6 (DRAFT-7-CHANGES.md).

## A_r for the containment check is a fixture test on the version-1 reference (his answer on Q1)

Terms the ruling defines or newly defines: fixture, MEASURED, the version-1 reference, containment, falsifies, T10.8. The closure over 15.0's definitions adds: Execution.

|A_r| = 19 clauses (T_r 10, L_r 10, D_r 8; a clause may be in several); 7 of them changed since draft 6.

| # | clause | lines | changed since draft 6 | why |
|---|---|---|---|---|
| 12 | preamble [ruled: F6] | 29-31 | yes | T |
| 21 | 15.0 Execution | 54-54 |  | L(the version-1 reference, Execution) |
| 45 | 15.3 Read-once ports. | 141-149 |  | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 177-181 |  | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 185-189 |  | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 190-193 |  | T |
| 66 | 15.7.1 | 212-224 |  | T |
| 70 | 15.7.5 | 240-251 | yes | T |
| 122 | 15.12 ¶ - "This does not exempt their surrounding clause | 401-405 |  | L(fixture) |
| 123 | 15.12.5 | 406-409 |  | L(the version-1 reference) D(re-read 5, ORDER-2: 1a's rows, 15.12.5) |
| 124 | 15.12.6 | 410-425 |  | L(the version-1 reference) D(re-read 5, ORDER-2: 1a's rows, 15.12.6) |
| 128 | 15.13.4 | 436-441 | yes | T L(containment) D(re-read 5, ORDER-2: the order of work, 15.13.4) |
| 132 | 15.13.8 | 451-487 | yes | T L(MEASURED, containment, T10.8) D(re-read 5, CONTAIN-2: the stop's row and its check, 15.13.8) |
| 134 | 15.13.9 | 493-496 |  | T |
| 135 | 15.13.10 | 497-503 | yes | L(T10.8) D(re-read 5, CONTAIN-2: T10 stays open, 15.13.10) |
| 136 | 15.13.11 | 504-522 |  | L(the version-1 reference) D(re-read 5, ORDER-2: 1a and its rows, 15.13.11) |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 containm | 555-555 | yes | L(containment) D(re-read 5, CONTAIN-2: 15.15's row on the check) |
| 157 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 556-556 | yes | L(containment, T10.8) |
| 158 | 15.15 row: 15.13.11: D10's two-commit split | 557-557 |  | D(re-read 5, ORDER-2: 15.15's row on the two-commit split) |

## A_r for findings 8 and 20 resolved before the pin (his answer on Q2)

Terms the ruling defines or newly defines: the pin, digest, candidate, finding 8, finding 20, 'R', 1a. The closure over 15.0's definitions adds: none.

|A_r| = 40 clauses (T_r 18, L_r 28, D_r 9; a clause may be in several); 9 of them changed since draft 6.

| # | clause | lines | changed since draft 6 | why |
|---|---|---|---|---|
| 5 | preamble [ruled: claims] | 13-13 |  | T |
| 8 | preamble [pinned] | 19-21 |  | L(the pin, digest) |
| 12 | preamble [ruled: F6] | 29-31 | yes | T |
| 30 | 15.2.1 | 97-98 |  | L(1a) |
| 45 | 15.3 Read-once ports. | 141-149 |  | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 177-181 |  | T |
| 58 | 15.5 Optionally, one end record | 182-183 |  | L(candidate) |
| 60 | 15.5 A well-formed log may lack the read-once record | 185-189 |  | T L(finding 8) |
| 61 | 15.5 The log is parsed whole before any execution starts. | 190-193 |  | T |
| 62 | 15.5 Load refusals | 194-197 |  | T L(finding 8) |
| 66 | 15.7.1 | 212-224 |  | T |
| 70 | 15.7.5 | 240-251 | yes | T L(finding 8) D(re-read 5, ORDER-1: the statuses, 15.7.5) |
| 76 | 15.8 ¶ - status (§15.7.5) | 268-268 |  | D(re-read 5, ORDER-1: the status line, 15.8) |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 295-303 |  | T L(finding 20, 'R') D(re-read 5, ORDER-1: 'R' and the cut, 15.9) |
| 93 | 15.10 ¶ [ruled: R5: part of 1a] Written by an execution  | 307-308 |  | L(1a) |
| 97 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 312-314 |  | L(digest, 1a) |
| 103 | 15.10 ¶ The state digest's cost on a large state is for  | 322-322 |  | L(digest, 1a) |
| 105 | 15.11 Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity. | 331-332 |  | L(digest) |
| 123 | 15.12.5 | 406-409 |  | L(1a) |
| 124 | 15.12.6 | 410-425 |  | L(1a) |
| 125 | 15.13.1 | 429-432 |  | T |
| 126 | 15.13.2 | 433-434 |  | T |
| 127 | 15.13.3 | 435-435 |  | T |
| 128 | 15.13.4 | 436-441 | yes | T L(the pin, digest, candidate, 1a) D(re-read 5, ORDER-1: the order of work, 15.13.4) |
| 129 | 15.13.5 | 442-444 |  | L(the pin) |
| 130 | 15.13.6 | 445-446 |  | L(the pin) |
| 131 | 15.13.7 | 447-450 |  | L(the pin) |
| 132 | 15.13.8 | 451-487 | yes | T L(the pin, digest, 'R') D(re-read 5, ORDER-1: the stop's row, chosen from the status, 15.13.8) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 489-492 |  | L(the pin) D(re-read 5, ORDER-1: the pin's reach, 15.13) |
| 134 | 15.13.9 | 493-496 |  | T L(the pin) |
| 135 | 15.13.10 | 497-503 | yes | T |
| 136 | 15.13.11 | 504-522 |  | L(1a) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 543-543 |  | L(1a) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 545-545 | yes | L(finding 8) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 547-547 |  | D(re-read 5, ORDER-1: 15.15's row on the four statuses) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 549-549 |  | L(finding 20, 'R') D(re-read 5, ORDER-1: 15.15's row on 'R') |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 550-550 |  | L(digest, 1a) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 554-554 | yes | T L(finding 8) D(re-read 5, ORDER-1: 15.15's row on the stop's form) |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 containm | 555-555 | yes | L(the pin) |
| 157 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 556-556 | yes | L(the pin) |

## A_r for RO′-5 confirmed: no fifth status word (his confirmation)

Terms the ruling defines or newly defines: status, NOT-RUN, LOG-OPEN, the read-once stop, fifth status. The closure over 15.0's definitions adds: none.

|A_r| = 17 clauses (T_r 10, L_r 14, D_r 6; a clause may be in several); 8 of them changed since draft 6.

| # | clause | lines | changed since draft 6 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 7 applies to draft 6 the six fixes | 3-8 | yes | L(status, the read-once stop) |
| 12 | preamble [ruled: F6] | 29-31 | yes | T L(status, the read-once stop) |
| 41 | 15.3 row: `close()` | 133-133 |  | L(NOT-RUN) |
| 45 | 15.3 Read-once ports. | 141-149 |  | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 177-181 |  | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 185-189 |  | T L(NOT-RUN) |
| 61 | 15.5 The log is parsed whole before any execution starts. | 190-193 |  | T |
| 66 | 15.7.1 | 212-224 |  | T L(NOT-RUN, LOG-OPEN) D(re-read 5, CARRIER-1: the stop, 15.7.1) |
| 70 | 15.7.5 | 240-251 | yes | T L(status, NOT-RUN, LOG-OPEN, fifth status) D(re-read 5, CARRIER-1 and CARRIER-3: the statuses, 15.7.5) |
| 76 | 15.8 ¶ - status (§15.7.5) | 268-268 |  | L(status) D(re-read 5, CARRIER-1: the status line, 15.8) |
| 128 | 15.13.4 | 436-441 | yes | T L(the read-once stop) |
| 132 | 15.13.8 | 451-487 | yes | T L(status, NOT-RUN, LOG-OPEN, the read-once stop) D(re-read 5, CARRIER-2: the stop's row and the NOT-RUN/LOG-OPEN row, 15.13.8) |
| 134 | 15.13.9 | 493-496 |  | T L(the read-once stop) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 547-547 |  | L(status) D(re-read 5, CARRIER-1: 15.15's row on the four statuses) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 554-554 | yes | L(status, NOT-RUN, the read-once stop) D(re-read 5, CARRIER-3: 15.15's row on the stop's form) |
| 156 | 15.15 row: 15.13.8: the read-once stop's version-1 containm | 555-555 | yes | L(the read-once stop) |
| 160 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 560-565 | yes | L(status, the read-once stop) |

## The union

46 clauses are in A_TEST, A_PIN or A_RO5; 19 in more than one; 11 of them changed since draft 6; 1 of the clauses changed since draft 6 are in none.
