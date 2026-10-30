# A_r for his answers to re-read 9's five questions, read with draft 12

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answers (`RULINGS.md`, "Re-read 9's five questions") and the adopted drafting fixes of re-read 9 reach these
clauses. He recommends that the twin read the whole of draft 12, so they do not bound the re-read.

## How the set was computed

By `ar_compute.py 11` over `SPEC-15-DRAFT-11.md`, the text current when he answered (sha256
`937499a6daa87ebeb483cb535d1dba2f20eecb4d3518b83d2598991db96524f5`). Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 11`; its whole output is below, unedited.
Its sets 1 to 10 still print their records byte for byte.

## The computed set

Draft 11: 180 clauses; 57 changed or added since draft 10 (DRAFT-11-CHANGES.md).

## A_r for his answers to re-read 9's five questions, with its drafting fixes and open items

Terms the ruling defines or newly defines: the fixed example, 'N', budget, tick record, byte grammar, exit. The closure over 15.0's definitions adds: none.

|A_r| = 95 clauses (T_r 37, L_r 28, D_r 70; a clause may be in several); 50 of them changed since draft 10.

| # | clause | lines | changed since draft 10 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 11 applies to draft 10 the fixes R | 3-9 | yes | L(budget) |
| 4 | preamble [ruled: R2, R3, R4, R5, R6, R9] | 12-13 | yes | T L(budget) |
| 5 | preamble [ruled: F8] | 14-15 | yes | T |
| 6 | preamble [ruled: F20] | 16-16 | yes | T |
| 7 | preamble [ruled: PP] | 17-17 | yes | T |
| 9 | preamble [ruled: N2] | 19-19 | yes | T |
| 15 | preamble [open: X] | 32-34 |  | D(S15.0-1: the legend) |
| 17 | preamble [ruled: F6] | 38-40 |  | T |
| 20 | 15.0 Version 1 law | 50-51 |  | T |
| 22 | 15.0 Prefix | 56-57 | yes | T D(S15.0-1: Prefix) |
| 27 | 15.1.1 | 68-82 | yes | L(budget) |
| 29 | 15.1.3 | 85-103 | yes | T |
| 30 | 15.1.4 | 104-104 |  | T L(budget) D(S15.1-1: the law's lines, 15.1.4) |
| 41 | 15.3 ¶ [open: amended set "A2", with the declared polic | 155-156 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 42 | 15.3 row: event | 158-159 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 43 | 15.3 row: `arrive(port, source, bytes)` | 160-160 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 44 | 15.3 row: `assign(arrival, tick)` | 161-161 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 45 | 15.3 row: `drop(arrival)` | 162-162 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 46 | 15.3 row: `close()` | 163-163 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 47 | 15.3 row: `end()` | 164-164 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 48 | 15.3 Any other move is refused by its rule's name | 166-168 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 49 | 15.3 Every arrival has exactly one disposition | 169-170 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 50 | 15.3 Read-once ports. | 171-187 | yes | T L('N', tick record) D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 51 | 15.3 No value is invented, held over or defaulted, | 188-189 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 52 | 15.3 A retry is a new arrival; | 190-191 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 53 | 15.3 A door refusal or a refused move does not end the session. | 192-192 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 54 | 15.3 Until SNAP-1, a refusal of the run ends the session. | 193-195 |  | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 55 | 15.3 A refused session's log carries no end record. | 196-200 | yes | D(S15.3-1, S15.3-2: the session's events, 15.3) |
| 62 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 221-222 |  | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 63 | 15.5 The header | 223-223 |  | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 64 | 15.5 The read-once record | 224-228 | yes | T L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 65 | 15.5 Values, | 229-232 | yes | T L(the fixed example, 'N') D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 66 | 15.5 Optionally, one end record, | 233-240 | yes | T L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 67 | 15.5 A log with no end record is open. | 241-241 |  | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 68 | 15.5 A well-formed log may lack the read-once record. | 242-247 | yes | T L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 69 | 15.5 The log is parsed whole before any execution starts. | 248-251 |  | T D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 70 | 15.5 Load refusals. | 252-256 | yes | T D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 71 | 15.5 row: case | 258-259 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 72 | 15.5 row: a byte above 0x7F | 260-260 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 73 | 15.5 row: a CR, no final LF, or an empty line (a leading L | 261-261 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 74 | 15.5 row: a missing or wrong header line, or an unknown do | 262-262 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 75 | 15.5 row: the ports line's digest is not the law's port si | 263-263 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 76 | 15.5 row: a line whose kind is not `t`, `end` or `once` | 264-264 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 77 | 15.5 row: a `once` line with the wrong number of values, a | 265-265 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 78 | 15.5 row: M1: a tick record where the read-once record sho | 266-266 | yes | L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 79 | 15.5 row: a tick record with the wrong value count, or a v | 267-267 | yes | L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 80 | 15.5 row: a tick number not canonical, or not one more tha | 268-268 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 81 | 15.5 row: M2 `end 0 closed`, M3, M4, a failed condition of | 269-269 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 82 | 15.5 row: any line after the end record | 270-270 | yes | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 83 | 15.5 The order of checks. | 272-278 | yes | T L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 84 | 15.5 A load refusal writes no receipt | 279-288 | yes | T L(exit) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 85 | 15.5 The chain | 289-290 | yes | L(tick record) D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 86 | 15.5 `input-log-sha256` | 291-292 |  | D(S15.5-1 to S15.5-5: the input log, 15.5) |
| 88 | 15.7.1 | 303-317 | yes | T L('N', tick record) D(S15.3-1: the order, 15.7.1) |
| 89 | 15.7.2 | 318-324 | yes | T L('N') |
| 90 | 15.7.3 | 325-337 | yes | T L(budget) D(S15.1-1: the budget, 15.7.3) |
| 91 | 15.7.4 | 338-339 |  | L(tick record) |
| 92 | 15.7.5 | 340-357 | yes | T L(tick record) |
| 93 | 15.7.6 | 358-366 |  | T |
| 94 | 15.8 ¶ [ruled: R5] Lines, in order: | 370-370 |  | T |
| 99 | 15.8 ¶ - ticks <n>: the ticks begun, a refused tick inc | 375-375 |  | T |
| 100 | 15.8 ¶ - tick-ops <n>: the last begun tick's own count, | 376-377 | yes | T |
| 101 | 15.8 ¶ - the count of tick records left unread after a  | 378-378 |  | L(tick record) |
| 110 | 15.8 The frame check is versioned. | 390-393 |  | T |
| 112 | 15.9 The head. | 398-399 |  | T L('N') D(S15.9-1, S15.9-2: the trace, 15.9) |
| 113 | 15.9 `'N'`'s payload | 400-401 | yes | T L('N') D(S15.9-1, S15.9-2: the trace, 15.9) |
| 114 | 15.9 The `'R'` event carries the refusal cut | 402-420 | yes | T L('N', byte grammar) D(S15.9-1, S15.9-2: the trace, 15.9) |
| 115 | 15.10 ¶ [ruled: R5: part of 1a] Written by an execution  | 424-425 |  | T |
| 120 | 15.10 ¶ - input-chain <hex>: in_t. [open: the speed verd | 432-432 |  | T |
| 125 | 15.10 ¶ The state digest's cost on a large state is for  | 439-439 |  | T |
| 144 | 15.12 ¶ - "This does not exempt their surrounding clause | 518-528 | yes | L(budget) |
| 150 | 15.13.4 | 561-582 | yes | D(S15.13-1: the pin's inputs, 15.13.4) |
| 153 | 15.13.7 | 588-591 |  | L(exit) |
| 154 | 15.13.8 | 592-647 | yes | T L('N') D(S15.9-1: the stop's row and the cut, 15.13.8) |
| 156 | 15.13.9 | 655-658 |  | T |
| 161 | 15.15 row: clause | 700-701 |  | D(S15.15-1: what is open, 15.15) |
| 162 | 15.15 row: 15.0: float ports | 702-702 | yes | D(S15.15-1: what is open, 15.15) |
| 163 | 15.15 row: 15.1.5: the door and the forms | 703-703 |  | D(S15.15-1: what is open, 15.15) |
| 164 | 15.15 row: 15.1.6: world properties | 704-704 |  | D(S15.15-1: what is open, 15.15) |
| 165 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 705-705 |  | D(S15.15-1: what is open, 15.15) |
| 166 | 15.15 row: 15.3 and 15.4: the session, its record and the b | 706-706 | yes | D(S15.15-1: what is open, 15.15) |
| 167 | 15.15 row: 15.3: the events that fill and close the read-on | 707-707 | yes | D(S15.15-1: what is open, 15.15) |
| 168 | 15.15 row: 15.5: a text value's door rules in the loader's  | 708-708 | yes | D(S15.15-1: what is open, 15.15) |
| 169 | 15.15 row: 15.6: the port signature's `<name>` and `<type>` | 709-709 | yes | D(S15.15-1: what is open, 15.15) |
| 170 | 15.15 row: 15.7.6: out_0's reading and domain string | 710-710 |  | D(S15.15-1: what is open, 15.15) |
| 171 | 15.15 row: 15.8: `tick-ops` when no tick began; the unread  | 711-711 | yes | D(S15.15-1: what is open, 15.15) |
| 172 | 15.15 row: 15.9: the cut's byte grammar, MEASURED on versio | 712-712 | yes | L(byte grammar) D(S15.15-1: what is open, 15.15) |
| 173 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 713-713 |  | D(S15.15-1: what is open, 15.15) |
| 174 | 15.15 row: 15.11 and 15.8: replay, and "never reported as v | 714-714 |  | D(S15.15-1: what is open, 15.15) |
| 175 | 15.15 row: 15.13.4 and 15.13.8: the version-1 containment t | 715-715 | yes | D(S15.15-1: what is open, 15.15) |
| 176 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 716-716 |  | D(S15.15-1: what is open, 15.15) |
| 177 | 15.15 row: 15.13.9: the row named when two rows withhold on | 717-717 |  | D(S15.15-1: what is open, 15.15) |
| 178 | 15.15 row: 15.13.11: D10's two-commit split | 718-718 |  | D(S15.15-1: what is open, 15.15) |
| 179 | 15.15 row: 15.14: the authority rule; the labels of a confi | 719-719 |  | D(S15.15-1: what is open, 15.15) |
| 180 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 721-731 | yes | T L(budget, byte grammar) D(S15.15-1: what is open, 15.15) |

## The union

95 clauses are in A_RR9; 0 in more than one set; 50 of them changed since draft 10; 7 of the clauses changed since draft 10 are not in it.
