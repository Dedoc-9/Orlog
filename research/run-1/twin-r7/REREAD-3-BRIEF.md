# R7's third re-read: the brief to the twin (2026-10-27)

Since your second re-read the owner has made two more rulings:
- the closure table's Perform row (your TABLE-1): SPEC §3's row, the bare name included;
- finding 6, read-once ports: A′, as RO′-1 to RO′-6, with six conditions.

Draft 4 applied the drafting fixes your second re-read led to and the Perform row. Draft 5 states finding 6's ruling.
Under R7, point 4, each ruling triggers the re-read of its A_r. His sixth condition on finding 6: *"No implementation or
build before the affected-clause set is computed and the twin rereads the affected clauses under R7."* This is that
re-read, by the same reviewer.

## Your reading set

These files, in this folder. Open nothing else, and list every file you open.

- `SPEC-15-DRAFT-5.md`: the draft.
- `RULINGS-AS-RULED.md`: its last two sections hold the Perform row and finding 6, each his words first, then the text
  he adopted. The earlier sections are as you read them.
- `AR-F6.md`: finding 6's set (104 clauses; line numbers draft 4's, names holding in draft 5).
- `AR-REREAD-2.md`: its third set, the Perform row's (12 clauses; line numbers draft 3's).
- `DRAFT-4-CHANGES.md` and `DRAFT-5-CHANGES.md`: what each draft changed, and why.
- `T10-STATEMENTS.md`: T10.0 to T10.7 now. T10.5 is reworded after your T10.5-4.
- `SPEC.md` and `RUNTIME-SPEC.md`, the same bytes as before.

## What to read

- Every clause of A_F6, in draft 5's text, once for finding 6.
- Every clause of the Perform row's set, once for that ruling.
- Every clause draft 4 or draft 5 changed or added.
- T10.5's statement.

A clause in several of these is read once for each ruling that names it.

## What to report

For each ruling in turn, R7's two sections:
- **Faithfulness**, for each clause tagged with that ruling: whether it states the ruling as ruled, or adds to it,
  narrows it or alters it. Quoted words must be his. His conditions are part of finding 6's ruling.
- **Coherence**, for every clause of the set: whether the ruling leaves it interpretable and consistent with the
  established rules; its missing cases and invalid inferences; and whether its tags name every ruling it now depends
  on.

For each of your second re-read's findings that draft 4 says it answers, say whether the change answers it.

On finding 6, check in particular:
- that RO′-6's row in 15.13.8 states its premises and its withholding, as his condition 3 requires;
- that whole-log validation stays mandatory beside the read-once stop (condition 1);
- that nothing weakens R6's law-fixed claim line (condition 2);
- that N2, N3 and the loadable form stay open (conditions 4 and 5).

Record hand-worked probes, marked unexecuted. Mark a fixture's outcome as your own worked consequence, never as the
draft's or his.

Number the findings (F6-1, …; PERFORM-1, …; CHANGED-1, …; T10.5-…). Give each a class (DRAFTING, GAP, COHERENCE,
QUESTION), and say whether it needs a ruling. If you need a source outside this set, name it and why, as R7 permits, and
do not open it.

Deliver the report as text in your reply.
