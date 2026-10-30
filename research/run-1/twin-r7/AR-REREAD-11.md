# A_r for his answer to re-read 10's question, read with draft 13

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His answer (`RULINGS.md`, "Re-read 10's question") and re-read 10's adopted fixes reach these clauses. He set the
re-read of draft 13 as targeted: its changed clauses and their affected clauses, with the one-shot log and `close()`
rules checked for consistency across sections.

## How the set was computed

By `ar_compute.py 12` over `SPEC-15-DRAFT-12.md`, the text current when he answered (sha256
`772fda5264fd0c10c86aba95cd85e44669e4611761914700969b70fc4e86e750`). Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 12`; its whole output is below, unedited.
Its sets 1 to 11 still print their records byte for byte.

## The computed set

Draft 12: 187 clauses; 22 changed or added since draft 11 (DRAFT-12-CHANGES.md).

## A_r for close() refused in a law with no tick block, with re-read 10's fixes

Terms the ruling defines or newly defines: close(), no tick block, tick record, the one-shot law. The closure over 15.0's definitions adds: none.

|A_r| = 77 clauses (T_r 22, L_r 16, D_r 67; a clause may be in several); 14 of them changed since draft 11.

| # | clause | lines | changed since draft 11 | why |
|---|---|---|---|---|
| 5 | preamble [ruled: F8] | 13-14 |  | T |
| 7 | preamble [ruled: PP] | 16-16 |  | T |
| 22 | 15.0 Prefix | 55-56 | yes | T |
| 24 | 15.0 Arrival | 59-61 |  | T |
| 29 | 15.1.3 | 84-102 |  | T L(no tick block, the one-shot law) |
| 41 | 15.3 ¶ [open: amended set "A2", with the declared polic | 156-157 |  | T D(S15.3-1: the session's events, 15.3) |
| 42 | 15.3 row: event | 159-160 |  | D(S15.3-1: the session's events, 15.3) |
| 43 | 15.3 row: `arrive(port, source, bytes)` | 161-161 |  | D(S15.3-1: the session's events, 15.3) |
| 44 | 15.3 row: `assign(arrival, tick)` | 162-162 |  | D(S15.3-1: the session's events, 15.3) |
| 45 | 15.3 row: `drop(arrival)` | 163-163 |  | D(S15.3-1: the session's events, 15.3) |
| 46 | 15.3 row: `close()` | 164-164 |  | L(close()) D(S15.3-1: the session's events, 15.3) |
| 47 | 15.3 row: `end()` | 165-165 |  | D(S15.3-1: the session's events, 15.3) |
| 48 | 15.3 Any other move is refused by its rule's name | 167-169 |  | D(S15.3-1: the session's events, 15.3) |
| 49 | 15.3 Every arrival has exactly one disposition | 170-171 |  | D(S15.3-1: the session's events, 15.3) |
| 50 | 15.3 Read-once ports. | 172-191 | yes | T L(close(), tick record) D(S15.3-1: the session's events, 15.3) |
| 51 | 15.3 No value is invented, held over or defaulted, | 192-193 |  | T D(S15.3-1: the session's events, 15.3) |
| 52 | 15.3 A retry is a new arrival; | 194-195 |  | D(S15.3-1: the session's events, 15.3) |
| 53 | 15.3 A door refusal or a refused move does not end the session. | 196-196 |  | T D(S15.3-1: the session's events, 15.3) |
| 54 | 15.3 Until SNAP-1, a refusal of the run ends the session. | 197-199 |  | D(S15.3-1: the session's events, 15.3) |
| 55 | 15.3 A refused session's log carries no end record. | 200-204 |  | D(S15.3-1: the session's events, 15.3) |
| 62 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 225-226 |  | D(S15.5-1: the input log and its order, 15.5) |
| 63 | 15.5 The header | 227-227 |  | D(S15.5-1: the input log and its order, 15.5) |
| 64 | 15.5 The read-once record | 228-232 |  | T L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 65 | 15.5 Values, | 233-237 | yes | T D(S15.5-1: the input log and its order, 15.5) |
| 66 | 15.5 Optionally, one end record, | 238-245 |  | T L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 67 | 15.5 A law with read-once ports and no tick block | 246-247 | yes | L(no tick block, tick record) D(S15.5-1: the input log and its order, 15.5) |
| 68 | 15.5 A log with no end record is open. | 248-248 |  | D(S15.5-1: the input log and its order, 15.5) |
| 69 | 15.5 A well-formed log may lack the read-once record. | 249-255 | yes | T L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 70 | 15.5 The log is parsed whole before any execution starts. | 256-259 |  | D(S15.5-1: the input log and its order, 15.5) |
| 71 | 15.5 Load refusals. | 260-264 |  | T D(S15.5-1: the input log and its order, 15.5) |
| 72 | 15.5 row: case | 266-267 |  | D(S15.5-1: the input log and its order, 15.5) |
| 73 | 15.5 row: a byte above 0x7F | 268-268 |  | D(S15.5-1: the input log and its order, 15.5) |
| 74 | 15.5 row: a CR, no final LF, or an empty line (a leading L | 269-269 |  | D(S15.5-1: the input log and its order, 15.5) |
| 75 | 15.5 row: a missing or wrong header line, or an unknown do | 270-270 |  | D(S15.5-1: the input log and its order, 15.5) |
| 76 | 15.5 row: the ports line's digest is not the law's port si | 271-271 |  | D(S15.5-1: the input log and its order, 15.5) |
| 77 | 15.5 row: a line whose kind is not `t`, `end` or `once` | 272-272 |  | D(S15.5-1: the input log and its order, 15.5) |
| 78 | 15.5 row: a `once` line with the wrong number of values, a | 273-273 |  | D(S15.5-1: the input log and its order, 15.5) |
| 79 | 15.5 row: M1: a tick record where the read-once record sho | 274-274 |  | L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 80 | 15.5 row: a tick record with the wrong value count, or a v | 275-275 |  | L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 81 | 15.5 row: a tick record in a law with no tick block (his a | 276-276 | yes | L(no tick block, tick record) D(S15.5-1: the input log and its order, 15.5) |
| 82 | 15.5 row: a tick number not canonical, or not one more tha | 277-277 | yes | D(S15.5-1: the input log and its order, 15.5) |
| 83 | 15.5 row: M2 `end 0 closed`, M3, M4, a failed condition of | 278-278 |  | D(S15.5-1: the input log and its order, 15.5) |
| 84 | 15.5 row: any line after the end record | 279-279 |  | D(S15.5-1: the input log and its order, 15.5) |
| 85 | 15.5 The order of checks. | 281-287 |  | T L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 86 | 15.5 A load refusal writes no receipt | 288-299 | yes | T D(S15.5-1: the input log and its order, 15.5) |
| 87 | 15.5 The chain | 300-301 |  | L(tick record) D(S15.5-1: the input log and its order, 15.5) |
| 88 | 15.5 `input-log-sha256` | 302-303 |  | D(S15.5-1: the input log and its order, 15.5) |
| 90 | 15.7.1 | 314-328 |  | L(tick record) |
| 93 | 15.7.4 | 350-351 |  | L(tick record) |
| 94 | 15.7.5 | 352-369 |  | T L(tick record) |
| 103 | 15.8 ¶ - the count of tick records left unread after a  | 390-390 |  | L(tick record) |
| 115 | 15.9 `'N'`'s payload | 412-413 |  | T |
| 157 | 15.13.8 | 612-667 |  | T D(S15.13-1: the NOT-RUN/LOG-OPEN row, 15.13.8) |
| 164 | 15.15 row: clause | 720-721 |  | D(S15.15-1: what is open, 15.15) |
| 165 | 15.15 row: 15.0: float ports | 722-722 |  | D(S15.15-1: what is open, 15.15) |
| 166 | 15.15 row: 15.1.4: the law line's `<type>` spelling | 723-723 | yes | D(S15.15-1: what is open, 15.15) |
| 167 | 15.15 row: 15.3: when the host runs the prefix of a law wit | 724-724 | yes | T D(S15.15-1: what is open, 15.15) |
| 168 | 15.15 row: 15.5: how a 1b runtime refuses a log, and its ex | 725-725 | yes | D(S15.15-1: what is open, 15.15) |
| 169 | 15.15 row: 15.1.5: the door and the forms | 726-726 |  | D(S15.15-1: what is open, 15.15) |
| 170 | 15.15 row: 15.1.6: world properties | 727-727 |  | D(S15.15-1: what is open, 15.15) |
| 171 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 728-728 |  | D(S15.15-1: what is open, 15.15) |
| 172 | 15.15 row: 15.3 and 15.4: the session, its record and the b | 729-729 |  | T D(S15.15-1: what is open, 15.15) |
| 173 | 15.15 row: 15.3: the events that fill and close the read-on | 730-730 |  | T D(S15.15-1: what is open, 15.15) |
| 174 | 15.15 row: 15.5: a text value's door rules in the loader's  | 731-731 |  | D(S15.15-1: what is open, 15.15) |
| 175 | 15.15 row: 15.6: the port signature's `<name>` and `<type>` | 732-732 |  | D(S15.15-1: what is open, 15.15) |
| 176 | 15.15 row: 15.7.6: out_0's reading and domain string | 733-733 |  | D(S15.15-1: what is open, 15.15) |
| 177 | 15.15 row: 15.8: `tick-ops` when no tick began; the unread  | 734-734 |  | D(S15.15-1: what is open, 15.15) |
| 178 | 15.15 row: 15.9: the cut's byte grammar, draft 2 the candid | 735-735 | yes | D(S15.15-1: what is open, 15.15) |
| 179 | 15.15 row: 15.9: the general format freeze | 736-736 | yes | D(S15.15-1: what is open, 15.15) |
| 180 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 737-737 |  | D(S15.15-1: what is open, 15.15) |
| 181 | 15.15 row: 15.11 and 15.8: replay, and "never reported as v | 738-738 |  | D(S15.15-1: what is open, 15.15) |
| 182 | 15.15 row: 15.13.4 and 15.13.8: the version-1 containment t | 739-739 |  | D(S15.15-1: what is open, 15.15) |
| 183 | 15.15 row: 15.13.7: the continuation at a stop where no ope | 740-740 |  | D(S15.15-1: what is open, 15.15) |
| 184 | 15.15 row: 15.13.9: the row named when two rows withhold on | 741-741 |  | D(S15.15-1: what is open, 15.15) |
| 185 | 15.15 row: 15.13.11: D10's two-commit split | 742-742 |  | D(S15.15-1: what is open, 15.15) |
| 186 | 15.15 row: 15.14: the authority rule; the labels of a confi | 743-743 |  | D(S15.15-1: what is open, 15.15) |
| 187 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 745-756 | yes | D(S15.15-1: what is open, 15.15) |

## The union

77 clauses are in A_CLOSE; 0 in more than one set; 14 of them changed since draft 11; 8 of the clauses changed since draft 11 are not in it.
