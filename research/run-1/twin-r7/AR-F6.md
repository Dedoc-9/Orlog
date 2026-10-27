# A_r for the ruling of 2026-10-27 on finding 6, read-once ports

R7, point 4: a ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow it.
His ruling (`RULINGS.md`, "Finding 6: read-once ports"): A′, as RO′-1 to RO′-6, with six conditions, the sixth *"No
implementation or build before the affected-clause set is computed and the twin rereads the affected clauses under
R7."*

## How the set was computed

By `ar_compute.py 4`, the same way as the earlier sets, over `SPEC-15-DRAFT-4.md`, the text current when he ruled. The
script refuses any other text than sha256 `f4225545ffe8766580194fdf2fbfcc2c96e3a6b9808b079788eecce48864a411`. Run with
`PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 4`; its whole output is below, unedited.
Its sets 1 to 3 still print their records byte for byte.

- **T_r:** the clauses whose tags name finding 6.
- **L_r:** the terms the ruling defines or newly defines: read-once, binds, NOT-RUN, LOG-OPEN, malformed (whole-log
  validation), the cut and K̂ (RO′-6). The closure over §15.0 added none.
- **D_r:** the clauses packet C §5 and the adversary's packet F §4 and §5 name as touched by the ruling, and the
  licence's presupposition (re-read 1, PREFIX-6). Where a packet names a whole section (§15.3 to §15.11, §15.15), every
  clause of it is taken, a new entry form of the script (a section's number); nothing narrower was used.

**Limits:** as for the earlier sets. Most of the draft is in this set, because the read-once record and the stop touch
the session, the log, execution, the receipt, the trace, the tick line and the settlement.

## What the twin reads at re-read 3

This set, the table's Perform row set (`AR-REREAD-2.md`, its third set), and every clause draft 4 and draft 5 changed,
in draft 5's text, with T10.5's statement as it now stands.

## The computed set

Draft 4: 155 clauses; 18 changed or added since draft 3 (DRAFT-4-CHANGES.md).

## A_r for finding 6: read-once ports, A′ as RO′-1 to RO′-6

Terms the ruling defines or newly defines: read-once, binds, NOT-RUN, LOG-OPEN, malformed, the cut, K̂. The closure over 15.0's definitions adds: none.

|A_r| = 104 clauses (T_r 3, L_r 22, D_r 101; a clause may be in several); 8 of them changed since draft 3.

| # | clause | lines | changed since draft 3 | why |
|---|---|---|---|---|
| 15 | 15.0 Port | 41-43 |  | D(packet C §5, packet F §5: 15.0 Port) |
| 18 | 15.0 Arrival | 48-50 |  | D(packet C §5, packet F §5: 15.0 Arrival) |
| 19 | 15.0 Input log | 51-51 |  | D(packet C §5, packet F §5: 15.0 Input log) |
| 20 | 15.0 Execution | 52-52 |  | D(packet C §5, packet F §5: 15.0 Execution) |
| 23 | 15.1.3 | 64-71 | yes | D(packet C §5: 15.1.3) |
| 26 | 15.1.6 | 77-82 | yes | L(read-once) D(packet C §5: 15.1.6) |
| 35 | 15.3 ¶ [open: amended set "A2", with the declared polic | 122-123 |  | D(packet C §5: 15.3) |
| 36 | 15.3 row: event | 125-126 |  | D(packet C §5: 15.3) |
| 37 | 15.3 row: `arrive(port, source, bytes)` | 127-127 |  | D(packet C §5: 15.3) |
| 38 | 15.3 row: `assign(arrival, tick)` | 128-128 |  | D(packet C §5: 15.3) |
| 39 | 15.3 row: `drop(arrival)` | 129-129 |  | D(packet C §5: 15.3) |
| 40 | 15.3 row: `close()` | 130-130 |  | L(NOT-RUN) D(packet C §5: 15.3) |
| 41 | 15.3 row: `end()` | 131-131 |  | D(packet C §5: 15.3) |
| 42 | 15.3 Any other move is refused by its rule's name | 133-135 |  | D(packet C §5: 15.3) |
| 43 | 15.3 Every arrival has exactly one disposition | 136-137 |  | D(packet C §5: 15.3) |
| 44 | 15.3 Read-once ports have no event in this table yet. | 138-141 | yes | T L(read-once, binds) D(packet C §5: 15.3) |
| 45 | 15.3 No value is invented, held over or defaulted, | 142-143 |  | D(packet C §5: 15.3) |
| 46 | 15.3 A retry is a new arrival; | 144-145 |  | D(packet C §5: 15.3) |
| 47 | 15.3 A door refusal or a refused move does not end the session. | 146-146 |  | D(packet C §5: 15.3) |
| 48 | 15.3 Until SNAP-1, a refusal of the run ends the session. | 147-149 |  | D(packet C §5: 15.3) |
| 49 | 15.4 ¶ [open: amended set "session record" and "binding | 153-153 |  | L(binds) D(packet C §5: 15.4) |
| 50 | 15.4 The history is a record of its own | 154-154 |  | D(packet C §5: 15.4) |
| 51 | 15.4 Three records, three authorities | 155-158 |  | D(packet C §5: 15.4) |
| 52 | 15.4 The verifier checks the chain | 159-160 |  | D(packet C §5: 15.4) |
| 53 | 15.4 Two histories with one input log share one core. | 161-162 |  | D(packet C §5: 15.4) |
| 54 | 15.5 ¶ [open: amended set "identity and bytes"] A strea | 166-167 |  | D(packet C §5, packet F §5: 15.5) |
| 55 | 15.5 The header | 168-168 |  | D(packet C §5, packet F §5: 15.5) |
| 56 | 15.5 One record for the read-once ports, then one record per tick | 169-171 |  | L(read-once) D(packet C §5, packet F §5: 15.5) |
| 57 | 15.5 Optionally, one end record | 172-173 |  | L(NOT-RUN) D(packet C §5, packet F §5: 15.5) |
| 58 | 15.5 A log with no end record is open. | 174-174 |  | D(packet C §5, packet F §5: 15.5) |
| 59 | 15.5 The log is parsed whole before any execution starts. | 175-176 |  | L(malformed) D(packet C §5, packet F §5: 15.5) |
| 60 | 15.5 Load refusals | 177-180 |  | D(packet C §5, packet F §5: 15.5) |
| 61 | 15.5 The chain | 181-182 |  | L(read-once) D(packet C §5, packet F §5: 15.5) |
| 62 | 15.5 `input-log-sha256` | 183-184 |  | D(packet C §5, packet F §5: 15.5) |
| 63 | 15.6 ¶ [open: amended set "identity and bytes"] SHA-256 | 188-191 |  | D(packet C §5: 15.6) |
| 64 | 15.7.1 | 195-200 |  | T L(read-once, binds) D(packet C §5, packet F §5: 15.7) |
| 65 | 15.7.2 | 201-207 |  | D(packet C §5, packet F §5: 15.7) |
| 66 | 15.7.3 | 208-213 |  | D(packet C §5, packet F §5: 15.7) |
| 67 | 15.7.4 | 214-215 |  | D(packet C §5, packet F §5: 15.7) |
| 68 | 15.7.5 | 216-220 |  | L(NOT-RUN, LOG-OPEN) D(packet C §5, packet F §5: 15.7) |
| 69 | 15.7.6 | 221-229 |  | D(packet C §5, packet F §5: 15.7) |
| 70 | 15.8 ¶ [ruled: R5] Lines, in order: | 233-233 |  | D(packet C §5, packet F §5: 15.8) |
| 71 | 15.8 ¶ - orlog-receipt 1 | 234-234 |  | D(packet C §5, packet F §5: 15.8) |
| 72 | 15.8 ¶ - backend <name> | 235-235 |  | D(packet C §5, packet F §5: 15.8) |
| 73 | 15.8 ¶ - law-seal, text-seal, input-log-sha256 | 236-236 |  | D(packet C §5, packet F §5: 15.8) |
| 74 | 15.8 ¶ - status (§15.7.5) | 237-237 |  | D(packet C §5, packet F §5: 15.8) |
| 75 | 15.8 ¶ - ticks <n>: the ticks begun, a refused tick inc | 238-238 |  | L(NOT-RUN) D(packet C §5, packet F §5: 15.8) |
| 76 | 15.8 ¶ - tick-ops <n>: the last begun tick's own count, | 239-240 |  | D(packet C §5, packet F §5: 15.8) |
| 77 | 15.8 ¶ - the count of tick records left unread after a  | 241-241 |  | D(packet C §5, packet F §5: 15.8) |
| 78 | 15.8 ¶ - output-bytes, output-chain | 242-242 |  | D(packet C §5, packet F §5: 15.8) |
| 79 | 15.8 ¶ - events, trace-head | 243-243 |  | D(packet C §5, packet F §5: 15.8) |
| 80 | 15.8 ¶ - ops: every counted operation, the refused one  | 244-244 |  | D(packet C §5, packet F §5: 15.8) |
| 81 | 15.8 ¶ - claims, then one claim line each, as in versio | 245-245 |  | D(packet C §5, packet F §5: 15.8) |
| 82 | 15.8 ¶ - end | 246-246 |  | D(packet C §5, packet F §5: 15.8) |
| 83 | 15.8 ¶ The line order is this draft's. [open: amended s | 248-248 |  | D(packet C §5, packet F §5: 15.8) |
| 84 | 15.8 ¶ Then: | 250-250 |  | D(packet C §5, packet F §5: 15.8) |
| 85 | 15.8 The core | 251-252 |  | D(packet C §5, packet F §5: 15.8) |
| 86 | 15.8 The frame check is versioned. | 253-256 |  | D(packet C §5, packet F §5: 15.8) |
| 87 | 15.8 No receipt line states that a run is valid or correct. | 257-257 |  | D(packet C §5, packet F §5: 15.8) |
| 88 | 15.9 The head. | 261-262 |  | D(packet C §5: 15.9) |
| 89 | 15.9 `'N'`'s payload | 263-263 |  | D(packet C §5: 15.9) |
| 90 | 15.9 The `'R'` event would carry the refusal cut. | 264-272 |  | L(the cut) D(packet C §5: 15.9) |
| 91 | 15.10 ¶ [ruled: R5: part of 1a] Written by an execution  | 276-277 |  | D(packet C §5: 15.10) |
| 92 | 15.10 ¶ - tick <t>, events <n>, ops <n> (the tick's own  | 278-278 |  | D(packet C §5: 15.10) |
| 93 | 15.10 ¶ - trace-head <hex>, or - in a play build without | 279-279 |  | D(packet C §5: 15.10) |
| 94 | 15.10 ¶ - output-chain <hex>; | 280-280 |  | D(packet C §5: 15.10) |
| 95 | 15.10 ¶ - claims <hex> and state <hex>: R5 names a claim | 281-283 |  | D(packet C §5: 15.10) |
| 96 | 15.10 ¶ - input-chain <hex>: in_t. [open: the speed verd | 284-284 |  | D(packet C §5: 15.10) |
| 97 | 15.10 ¶ These must hold, under §15.7.2's running-total r | 286-286 |  | D(packet C §5: 15.10) |
| 98 | 15.10 ¶ - T(t+1).c − T(t).c equals tick t's ops; | 287-287 |  | D(packet C §5: 15.10) |
| 99 | 15.10 ¶ - T(1).c is the prefix's count; | 288-288 |  | D(packet C §5: 15.10) |
| 100 | 15.10 ¶ - the receipt's ops minus the last 'T''s c is th | 289-289 |  | D(packet C §5: 15.10) |
| 101 | 15.10 ¶ The state digest's cost on a large state is for  | 291-291 |  | D(packet C §5: 15.10) |
| 102 | 15.11 Replay. | 295-299 |  | D(packet C §5: 15.11) |
| 103 | 15.11 Agreement, a refusal, an open log, a matching digest or a successful replay is never reported as validity. | 300-301 |  | D(packet C §5: 15.11) |
| 107 | 15.12.3 | 312-313 |  | D(packet F §5: the provenance line, 15.12.3) |
| 109 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 326-353 | yes | T L(binds) D(re-read 1, PREFIX-6: the licence's presupposition) |
| 123 | 15.13.1 | 397-400 |  | L(the cut) |
| 128 | 15.13.6 | 411-412 |  | L(the cut, K̂) |
| 129 | 15.13.7 | 413-416 |  | D(packet F §4: 15.13.7) |
| 130 | 15.13.8 | 417-435 |  | L(NOT-RUN, LOG-OPEN, the cut, K̂) D(packet F §4: 15.13.8) |
| 131 | 15.13 ¶ What "may execute" reaches includes every proced | 437-439 | yes | D(packet F §4: 15.13.8's closing line) |
| 132 | 15.13.9 | 440-442 |  | D(packet F §4: 15.13.9, the row named) |
| 135 | 15.13.12 | 469-470 |  | D(packet C §5: 15.13.12) |
| 136 | 15.14 ¶ [open: amended set "reporting"] Every authoritat | 474-479 | yes | L(binds) |
| 137 | 15.15 row: clause | 483-484 |  | D(packet C §5: 15.15) |
| 138 | 15.15 row: 15.0 and 15.1: spellings, places, float ports | 485-485 |  | D(packet C §5: 15.15) |
| 139 | 15.15 row: 15.1.3: a read outside the tick block, textual o | 486-486 |  | D(packet C §5: 15.15) |
| 140 | 15.15 row: 15.1.5: the door and the forms | 487-487 |  | D(packet C §5: 15.15) |
| 141 | 15.15 row: 15.1.6: world properties | 488-488 |  | D(packet C §5: 15.15) |
| 142 | 15.15 row: 15.2: whether the ASCII sieve governs text; the  | 489-489 |  | D(packet C §5: 15.15) |
| 143 | 15.15 row: 15.3 and 15.4: the session, read-once ports, its | 490-490 |  | L(read-once, binds) D(packet C §5: 15.15) |
| 144 | 15.15 row: 15.5 and 15.6: the log's bytes, the read-once re | 491-491 |  | L(read-once, NOT-RUN) D(packet C §5: 15.15) |
| 145 | 15.15 row: 15.7.1, 15.7.2 and 15.7.3: what binding counts;  | 492-492 |  | L(binds) D(packet C §5: 15.15) |
| 146 | 15.15 row: 15.7.5 and 15.8: the four statuses; `tick-ops`,  | 493-493 |  | D(packet C §5: 15.15) |
| 147 | 15.15 row: 15.7.6: out_0's reading and domain string | 494-494 |  | D(packet C §5: 15.15) |
| 148 | 15.15 row: 15.9: whether `'R'` carries the cut; its bytes ( | 495-495 |  | L(the cut) D(packet C §5: 15.15) |
| 149 | 15.15 row: 15.10: the digests' definitions; `input-chain`;  | 496-496 |  | D(packet C §5: 15.15) |
| 150 | 15.15 row: 15.11 and 15.8: replay, and "never reported as v | 497-497 |  | D(packet C §5: 15.15) |
| 151 | 15.15 row: 15.13.9: the row named when two rows withhold on | 498-498 |  | D(packet C §5: 15.15) |
| 152 | 15.15 row: 15.12.4 and 15.7.1: where a read-once value bind | 499-499 |  | L(read-once, binds) D(packet C §5: 15.15) |
| 153 | 15.15 row: 15.13.11: D10's two-commit split | 500-500 |  | D(packet C §5: 15.15) |
| 154 | 15.15 row: 15.14: the authority rule; the labels of a confi | 501-501 | yes | D(packet C §5: 15.15) |
| 155 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 503-505 | yes | D(packet C §5: 15.15) |

## The union

104 clauses are in A_F6; 0 in more than one set; 8 of them changed since draft 3; 10 of the clauses changed since draft 3 are not in it.
