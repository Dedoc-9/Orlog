# A_r for his answers of 2026-10-27 on re-read 3: the read-once stop's row, and its version-1 check

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answers (`RULINGS.md`, "The read-once stop's row, its version-1 check, and the last re-read") are three. Two of
them decide something in the draft, and their sets are below.

The third, on how the re-reads converge, governs the review and decides no clause of the draft. So it has no A_r.
His words in it: *"The twin then re-reads the clauses changed by draft 6 and the clauses affected by these rulings
once."*

## How the sets were computed

By `ar_compute.py 5`, the same way as before, over `SPEC-15-DRAFT-5.md`, the text current when he answered. The
script refuses any other text than sha256 `3322571640426cafc10f445a9d606a6df4829c4151ac30fd3ba63d5ed3f53400`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 5`; its whole output is below, unedited.
Its sets 1 to 4 still print their records byte for byte.

- **T_r:** the clauses tagged with finding 6, which both answers refine.
- **L_r, for the row:** "the read-once stop" (its new name), "the rest of a block" (the name it must not take) and
  "withholding".
- **L_r, for the check:** "stand-ins" and "the pin".
- **D_r:** 15.13.8's rows and 15.13.9's list (re-read 3's F6-1), and 15.13.8's rows and what 15.15 lists open
  (re-read 3's F6-14).

## The computed sets

Draft 5: 158 clauses; 14 changed or added since draft 4 (DRAFT-5-CHANGES.md).

## A_r for the read-once stop's own row (his answer on F6-1)

Terms the ruling defines or newly defines: the read-once stop, the rest of a block, withholding. The closure over 15.0's definitions adds: none.

|A_r| = 11 clauses (T_r 7, L_r 5, D_r 2; a clause may be in several); 7 of them changed since draft 4.

| # | clause | lines | changed since draft 4 | why |
|---|---|---|---|---|
| 12 | preamble [ruled: F6] | 29-29 | yes | T |
| 45 | 15.3 Read-once ports. | 138-144 | yes | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 179-181 | yes | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 182-184 | yes | T |
| 66 | 15.7.1 | 203-214 | yes | T |
| 70 | 15.7.5 | 230-236 | yes | T |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 280-288 |  | L(withholding) |
| 126 | 15.13.2 | 418-419 |  | L(withholding) |
| 132 | 15.13.8 | 434-461 | yes | T L(the read-once stop, the rest of a block, withholding) D(re-read 3, F6-1: 15.13.8's rows) |
| 134 | 15.13.9 | 466-468 |  | L(the rest of a block, withholding) D(re-read 3, F6-1: 15.13.9's list of rows) |
| 153 | 15.15 row: 15.13.9: the row named when two rows withhold on | 524-524 |  | L(withholding) |

## A_r for the read-once stop's version-1 check, owed before the pin (his answer on F6-14)

Terms the ruling defines or newly defines: stand-ins, the pin. The closure over 15.0's definitions adds: none.

|A_r| = 33 clauses (T_r 7, L_r 7, D_r 21; a clause may be in several); 10 of them changed since draft 4.

| # | clause | lines | changed since draft 4 | why |
|---|---|---|---|---|
| 8 | preamble [pinned] | 19-21 |  | L(the pin) |
| 12 | preamble [ruled: F6] | 29-29 | yes | T |
| 45 | 15.3 Read-once ports. | 138-144 | yes | T |
| 60 | 15.5 A well-formed log may lack the read-once record | 179-181 | yes | T |
| 61 | 15.5 The log is parsed whole before any execution starts. | 182-184 | yes | T |
| 66 | 15.7.1 | 203-214 | yes | T |
| 70 | 15.7.5 | 230-236 | yes | T |
| 129 | 15.13.5 | 425-427 |  | L(the pin) |
| 130 | 15.13.6 | 428-429 |  | L(the pin) |
| 131 | 15.13.7 | 430-433 |  | L(the pin) |
| 132 | 15.13.8 | 434-461 | yes | T L(stand-ins, the pin) D(re-read 3, F6-14: 15.13.8's rows) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 463-465 |  | L(the pin) |
| 134 | 15.13.9 | 466-468 |  | L(the pin) |
| 139 | 15.15 row: clause | 509-510 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 511-511 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 512-512 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 142 | 15.15 row: 15.1.5: the door and the forms | 513-513 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 143 | 15.15 row: 15.1.6: world properties | 514-514 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 144 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 515-515 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 145 | 15.15 row: 15.3 and 15.4: the session, read-once ports, its | 516-516 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 517-517 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 518-518 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 148 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 519-519 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 149 | 15.15 row: 15.7.6: out_0's reading and domain string | 520-520 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 521-521 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 522-522 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 152 | 15.15 row: 15.11 and 15.8: replay, and "never reported as v | 523-523 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 153 | 15.15 row: 15.13.9: the row named when two rows withhold on | 524-524 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 154 | 15.15 row: 15.3 and 15.7.1: an `end()` before the read-once | 525-525 | yes | D(re-read 3, F6-14: what 15.15 lists open) |
| 155 | 15.15 row: 15.5: a form that loads for a header-only open l | 526-526 | yes | D(re-read 3, F6-14: what 15.15 lists open) |
| 156 | 15.15 row: 15.13.11: D10's two-commit split | 527-527 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 157 | 15.15 row: 15.14: the authority rule; the labels of a confi | 528-528 |  | D(re-read 3, F6-14: what 15.15 lists open) |
| 158 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 530-533 | yes | D(re-read 3, F6-14: what 15.15 lists open) |

## The union

35 clauses are in A_STOPROW or A_V1CHECK; 9 in both; 10 of them changed since draft 4; 4 of the clauses changed since draft 4 are in neither.
