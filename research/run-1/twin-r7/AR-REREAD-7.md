# A_r for his answer of 2026-10-27 on re-read 6: every input the pinned rule reads, fixed before the pin

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answer (`RULINGS.md`, "Every input the pinned rule reads, fixed before the pin") comes after re-read 6. This set is
recorded before draft 9 is re-read.

## How the set was computed

By `ar_compute.py 8`, the same way as before, over `SPEC-15-DRAFT-8.md`, the text current when he answered. The script
refuses any other text than sha256 `53d468213392da911d3b1fc5a50597b61b5c12bbb495c1368c0032f1f0e491c0`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 8`; its whole output is below, unedited.
Its sets 1 to 7 still print their records byte for byte.

- **T_r:** the clauses tagged with what the answer orders before the pin: the claims ruling, whose pin it is; finding
  6, whose stop row reads the inputs; findings 8 and 20; and the amended set's "port place" and "counting".
- **L_r:** the pin, digest, candidate, port place, top-level, counting, finding 8, finding 20, `'R'`, decoding and the
  format freeze; closed over §15.0's definitions.
- **D_r:** the clauses re-read 6 named: the stop row's premises (15.13.8), the place of ports (15.1.3), counting
  (15.7.1) and 15.15's rows on them (PIN-3); `'R'` and the cut (15.9) and 15.15's row on it (PIN-1); 15.15's row on
  15.5 and 15.6 (PIN-2); the order of work (15.13.4; PIN-4, TEST-3); and the legend's `[pinned]`.

## The computed set

Draft 8: 160 clauses; 16 changed or added since draft 7 (DRAFT-8-CHANGES.md).

## A_r for every input the pinned rule reads, fixed before the pin (his answer on PIN-1 and PIN-3)

Terms the ruling defines or newly defines: the pin, digest, candidate, port place, top-level, counting, finding 8, finding 20, 'R', decoding, the format freeze. The closure over 15.0's definitions adds: Boundary, Prefix, Tick block.

|A_r| = 48 clauses (T_r 32, L_r 40, D_r 11; a clause may be in several); 15 of them changed since draft 7.

| # | clause | lines | changed since draft 7 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 8 applies to draft 7 the fixes R7' | 3-8 | yes | L(the pin, finding 8) |
| 5 | preamble [ruled: claims] | 13-14 | yes | T L(the pin, finding 8) |
| 8 | preamble [pinned] | 20-22 |  | L(the pin, digest) D(re-read 6, the legend's [pinned]) |
| 12 | preamble [ruled: F6] | 30-32 | yes | T |
| 17 | 15.0 Prefix | 47-48 |  | T L(port place, top-level, Prefix, Tick block) |
| 18 | 15.0 Boundary | 49-50 |  | L(top-level, Boundary) |
| 24 | 15.1.3 | 67-74 |  | T L(port place, top-level) D(re-read 6, PIN-3: the place of ports, 15.1.3) |
| 27 | 15.1.6 | 80-86 |  | L(Boundary) |
| 45 | 15.3 Read-once ports. | 142-150 |  | T |
| 57 | 15.5 The read-once record, when the law declares a read-once port and the record was written (closed with every read-once port filled; it is written whole or not at all); then one record per tick | 178-182 |  | T |
| 58 | 15.5 Optionally, one end record | 183-184 |  | L(candidate) |
| 60 | 15.5 A well-formed log may lack the read-once record | 186-190 |  | T L(finding 8) |
| 61 | 15.5 The log is parsed whole before any execution starts. | 191-194 |  | T |
| 62 | 15.5 Load refusals | 195-198 |  | T L(finding 8) |
| 66 | 15.7.1 | 213-225 |  | T L(top-level, counting) D(re-read 6, PIN-3: counting, 15.7.1) |
| 67 | 15.7.2 | 226-232 |  | T L(counting) |
| 68 | 15.7.3 | 233-238 |  | T L(counting) |
| 70 | 15.7.5 | 241-255 | yes | T L(the pin, digest, finding 8) |
| 92 | 15.9 The `'R'` event would carry the refusal cut. | 299-308 | yes | T L(the pin, digest, finding 20, 'R', the format freeze) D(re-read 6, PIN-1: 'R' and the cut, 15.9) |
| 97 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 317-319 |  | L(digest, top-level) |
| 99 | 15.10 ¶ These must hold, under §15.7.2's running-total r | 322-322 |  | T L(counting) |
| 103 | 15.10 ¶ The state digest's cost on a large state is for  | 327-327 |  | L(digest) |
| 105 | 15.11 Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity. | 336-337 |  | L(digest) |
| 111 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 362-390 |  | T L(port place, top-level, Boundary) |
| 123 | 15.12.5 | 411-415 | yes | T L(the pin, digest) |
| 124 | 15.12.6 | 416-432 | yes | T L(the pin, digest) |
| 125 | 15.13.1 | 436-439 |  | T |
| 126 | 15.13.2 | 440-441 |  | T |
| 127 | 15.13.3 | 442-442 |  | T |
| 128 | 15.13.4 | 443-453 | yes | T L(the pin, digest, candidate, finding 8) D(re-read 6, PIN-4 and TEST-3: the order of work, 15.13.4) |
| 129 | 15.13.5 | 454-456 |  | L(the pin) |
| 130 | 15.13.6 | 457-458 |  | L(the pin) |
| 131 | 15.13.7 | 459-462 |  | L(the pin) |
| 132 | 15.13.8 | 463-508 | yes | T L(the pin, digest, top-level, counting, 'R', the format freeze) D(re-read 6, PIN-3: the stop row's premises, 15.13.8) |
| 133 | 15.13 ¶ What "may execute" reaches includes every proced | 510-513 |  | L(the pin) |
| 134 | 15.13.9 | 514-517 |  | T L(the pin) |
| 135 | 15.13.10 | 518-524 |  | T |
| 136 | 15.13.11 | 525-544 | yes | T L(the pin, digest) |
| 140 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 561-561 |  | T L(port place) |
| 141 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 562-562 |  | T L(port place) D(re-read 6, PIN-3: 15.15's row on the place) |
| 146 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 567-567 |  | L(finding 8) D(re-read 6, PIN-2: 15.15's row on 15.5 and 15.6) |
| 147 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 568-568 |  | T L(counting) D(re-read 6, PIN-3: 15.15's row on counting) |
| 150 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 571-571 | yes | L(the pin, finding 20, 'R', the format freeze) D(re-read 6, PIN-1: 15.15's row on 'R') |
| 151 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 572-572 |  | L(digest) |
| 155 | 15.15 row: 15.5 and 15.7.5: a form that loads for a header- | 576-576 | yes | T L(the pin, finding 8) |
| 156 | 15.15 row: 15.13.8: the version-1 containment test's fixtur | 577-577 | yes | T L(the pin, port place, counting) D(re-read 6, PIN-3: 15.15's row on the stop's premises) |
| 157 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 578-578 | yes | L(the pin) |
| 160 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 582-589 | yes | T L(the pin, finding 8) |

## The union

48 clauses are in A_INPUTS; 0 in more than one set; 15 of them changed since draft 7; 1 of the clauses changed since draft 7 are not in it.
