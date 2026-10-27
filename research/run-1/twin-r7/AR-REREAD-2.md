# A_r for the rulings of 2026-10-27: the labels' definitions, the closure's rule table, R6's control

R7, point 4: each ruling triggers the re-read of its A_r = T_r ∪ L_r ∪ D_r, recorded, and the builder may not narrow
it. His three answers of 2026-10-27 are three rulings (`RULINGS.md`, "The labels' definitions, the closure's rule
table, and R6's control"). His words, in his first: *"have the twin reread the affected clauses before any build."*

## How the sets were computed

As for the first set (`AR-F24-PREFIX.md`), by `ar_compute.py 2`, now over `SPEC-15-DRAFT-2.md`, the text current when
he ruled. The script refuses any other text than sha256 `43f6a725831308b9dc5b671d67b807e9366615310761fac6cf33710704ba66d5`.
Run with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B research/run-1/twin-r7/ar_compute.py 2`; its whole output is below,
unedited. The same script with no argument still prints the first set exactly as recorded (checked byte for byte).

- **T_r:** the clauses tagged with the rulings these refine: PREFIX for the labels and the table, F24 for the labels
  and the control.
- **L_r:** the terms each ruling defines or newly defines, closed over §15.0's formal definitions:
  - the labels: boundary, exempt, licence, closure, Reach, may execute, fail closed (B1, 5c, K1), REFERENCE-ONLY and
    configured (D);
  - the table: closure, statement kind, Reach, may execute, fail closed, port declaration, and To;
  - the control: control, configured, measured, witness.
  The closure added §15.0's "Boundary" for the labels and the table: its definition uses "port declaration" and
  "boundary".
- **D_r:** the clauses the re-read's findings name, now given by clause name (the line numbers moved in draft 2):
  PREFIX-1, -2, -3, -4, -12, -13 and F24-6, with D's definition at 15.13.11 and the reachability 15.13.8 shares. A
  D_r entry that names no clause makes the script refuse.

**Limits:** as for the first set. The term closure follows §15.0's formal definitions only, and the matching is
textual. "To" occurs nowhere in draft 2, so it adds no clause.

## What the twin reads at re-read 2

The union of these three sets and of the five clauses re-read 1 added to the first sets (`AR-F24-PREFIX.md`,
"Dependencies found later"). It reads them in draft 3's text, which applies the re-read's DRAFT dispositions and these
rulings. It also reads every clause draft 3 changes.

## The computed sets

Draft 2: 141 clauses; 13 changed or added since draft 1 (DRAFT-2-CHANGES.md).

## A_r for the labels' definitions (D, B1, 4a, 5c, K1), adopted without their conclusions

Terms the ruling defines or newly defines: boundary, exempt, licence, closure, Reach, may execute, fail closed, REFERENCE-ONLY, configured. The closure over 15.0's definitions adds: Boundary.

|A_r| = 16 clauses (T_r 10, L_r 15, D_r 5; a clause may be in several); 12 of them changed since draft 1.

| # | clause | lines | changed since draft 1 | why |
|---|---|---|---|---|
| 2 | preamble ¶ Status. Draft 2 states the owner's two rulings o | 3-11 | yes | L(licence) |
| 6 | preamble [ruled: F24] | 17-18 | yes | T |
| 7 | preamble [ruled: PREFIX] | 19-19 | yes | T L(licence) |
| 15 | 15.0 Prefix | 42-44 | yes | T L(licence) |
| 16 | 15.0 Boundary | 45-46 | yes | T L(boundary, Boundary) D(re-read 1: 15.0 Boundary, B1's wording) |
| 30 | 15.2.3 | 92-99 |  | L(boundary) |
| 63 | 15.7.1 | 188-193 | yes | L(licence) |
| 105 | 15.12.2 | 301-302 |  | L(licence) |
| 107 | 15.12.4 | 305-315 |  | L(exempt, licence) |
| 108 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 317-332 | yes | T L(boundary, licence, closure, Reach, may execute, fail closed) D(re-read 1, PREFIX-1 and PREFIX-4: the licence as ruled) |
| 109 | 15.12.5 | 333-335 | yes | T L(configured) |
| 110 | 15.12.6 | 336-343 | yes | T L(licence, configured) |
| 118 | 15.13.8 | 364-382 |  | L(may execute) D(re-read 1, PREFIX-1: K-hat's tick-block rows, 15.13.8) |
| 119 | 15.13 ¶ What "may execute" reaches includes every proced | 384-386 | yes | T L(licence, may execute, fail closed) D(re-read 1, PREFIX-1 and PREFIX-2: 15.13.8's closing line) |
| 122 | 15.13.11 | 397-406 | yes | T L(REFERENCE-ONLY, configured) D(D's definition: 15.13.11) |
| 141 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 436-437 | yes | T L(licence) |

## A_r for the closure's rule table

Terms the ruling defines or newly defines: closure, statement kind, Reach, may execute, fail closed, port declaration, To. The closure over 15.0's definitions adds: Boundary.

|A_r| = 13 clauses (T_r 6, L_r 5, D_r 8; a clause may be in several); 6 of them changed since draft 1.

| # | clause | lines | changed since draft 1 | why |
|---|---|---|---|---|
| 7 | preamble [ruled: PREFIX] | 19-19 | yes | T |
| 15 | 15.0 Prefix | 42-44 | yes | T |
| 16 | 15.0 Boundary | 45-46 | yes | T L(port declaration, Boundary) |
| 20 | 15.1.1 | 55-59 |  | D(re-read 1, PREFIX-13: 15.1.1, the forms) |
| 22 | 15.1.3 | 62-67 |  | D(re-read 1, PREFIX-12: 15.1.3) |
| 25 | 15.1.6 | 73-76 |  | D(re-read 1, PREFIX-12: 15.1.6) |
| 43 | 15.3 Read-once ports have no event in this table yet. | 132-134 |  | D(re-read 1, PREFIX-12: 15.3's read-once bullet) |
| 107 | 15.12.4 | 305-315 |  | L(port declaration) |
| 108 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 317-332 | yes | T L(closure, statement kind, Reach, may execute, fail closed, port declaration) D(re-read 1, PREFIX-3: the licence as ruled) |
| 116 | 15.13.6 | 358-359 |  | D(re-read 1, PREFIX-13: 15.13.6) |
| 118 | 15.13.8 | 364-382 |  | L(may execute) D(the shared reachability: 15.13.8 and its closing line) |
| 119 | 15.13 ¶ What "may execute" reaches includes every proced | 384-386 | yes | T L(statement kind, may execute, fail closed) D(the shared reachability: 15.13.8 and its closing line) |
| 141 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 436-437 | yes | T |

## A_r for R6's row and control on the configured witness, a measured version-0 control apart

Terms the ruling defines or newly defines: control, configured, measured, witness. The closure over 15.0's definitions adds: none.

|A_r| = 4 clauses (T_r 4, L_r 3, D_r 2; a clause may be in several); 4 of them changed since draft 1.

| # | clause | lines | changed since draft 1 | why |
|---|---|---|---|---|
| 6 | preamble [ruled: F24] | 17-18 | yes | T |
| 109 | 15.12.5 | 333-335 | yes | T L(configured, witness) |
| 110 | 15.12.6 | 336-343 | yes | T L(control, configured, measured, witness) D(re-read 1, F24-6: 15.12.6) |
| 122 | 15.13.11 | 397-406 | yes | T L(control, configured, measured, witness) D(re-read 1, F24-6: condition 1 in 15.13.11) |

## The union

21 clauses are in A_LABELS, A_TABLE or A_V0CTL; 12 in more than one; 12 of the union changed since draft 1; 1 of the clauses changed since draft 1 are in none.

## The third set: the table's Perform row (2026-10-27)

His answer to TABLE-1 (`RULINGS.md`, "The table's Perform row") is a ruling, so it has an A_r of its own. It was
computed by `ar_compute.py 3` over `SPEC-15-DRAFT-3.md`, the text current when he answered (sha256
`59ec11c1b7f710f5e613b9865ac447257748f8aa1c5d5f9f1919443a29575f7c`), the same way:
- T_r: the clauses tagged PREFIX;
- L_r: "Perform" and "the name alone";
- D_r: the table's Perform row and last row, and the licence, from TABLE-1.
The twin reads it with draft 4's changed clauses. The script's sets 1 and 2 still print their records byte for byte.

Draft 3: 154 clauses; 32 changed or added since draft 2 (DRAFT-3-CHANGES.md).

## A_r for the table's Perform row: SPEC §3's row, the bare name included

Terms the ruling defines or newly defines: Perform, the name alone. The closure over 15.0's definitions adds: none.

|A_r| = 12 clauses (T_r 7, L_r 4, D_r 3; a clause may be in several); 8 of them changed since draft 2.

| # | clause | lines | changed since draft 2 | why |
|---|---|---|---|---|
| 7 | preamble [ruled: PREFIX] | 17-19 | yes | T |
| 16 | 15.0 Boundary | 44-45 |  | T |
| 25 | 15.1.6 | 73-76 | yes | T |
| 43 | 15.3 Read-once ports have no event in this table yet. | 132-135 | yes | T |
| 89 | 15.9 The `'R'` event would carry the refusal cut. | 258-266 |  | L(Perform) |
| 108 | 15.12 ¶ The licence as ruled. [ruled: PREFIX] The licenc | 320-341 | yes | T D(re-read 2, TABLE-1: the licence as ruled) |
| 109 | 15.12 ¶ The closure's rule table. [ruled: PREFIX, 2026-1 | 343-344 | yes | T |
| 115 | 15.12 row: Perform | 352-352 | yes | L(Perform) D(re-read 2, TABLE-1: the table's Perform row) |
| 118 | 15.12 row: any other kind | 355-355 | yes | D(re-read 2, TABLE-1: the table's last row) |
| 129 | 15.13.8 | 400-418 |  | L(Perform) |
| 131 | 15.13.9 | 421-423 |  | L(Perform) |
| 154 | 15.15 ¶ Ruled since draft 1 (2026-10-26): 15.12.4's lice | 480-482 | yes | T |

## The union

12 clauses are in A_PERFORM; 0 in more than one set; 8 of them changed since draft 2; 24 of the clauses changed since draft 2 are not in it.
