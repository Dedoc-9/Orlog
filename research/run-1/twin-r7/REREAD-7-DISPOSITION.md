# Re-read 7: the disposition of the twin's 5 findings (2026-10-27)

The twin's report is `REREAD-7-REPORT.md`, saved unchanged; the text saved is equal to the hand-back in the twin's own
transcript. It read draft 9 (sha256 `8a1ccf5c…`), the clauses draft 9 changes, and the set of `AR-REREAD-7.md`. It finds
his answer stated faithfully but for one narrowing, and re-read 6's seven OWED fixes applied as disposed.

His word on the re-reads stands: *"Any further drafting fixes must be recorded with their required re-read before the
build, as R7 requires. Any issue needing your decision comes back to you; do not silently resolve it. Do not loop
indefinitely merely to obtain a clean report, but do not waive a required re-read or build gate either."* So draft 9
stays as the twin read it. Every fix below is recorded here, to be applied in draft 10 with his answer to the question
below, and re-read once before the build.

The report shows neither that CUT-0 is sound nor that the version-1 containment test passes, and the twin says so.
Nothing here claims either.

Classes: **ASK** (put to the owner), **OWED** (a fix recorded for draft 10, re-read before the build).

## Checked against the files first

- **INPUTS-2, the twin's SN-2.** CHECKED in draft 9.
  - The NOT-RUN/LOG-OPEN row of 15.13.8 applies "when the receipt's status is not in the read-once stop's
    distinguishing form", so it reads the version-1 statuses.
  - Their encoding is under 15.15's row "15.7.5 and 15.8: the four statuses; …", decided by the amended set's
    "identity and bytes", with no timing against the pin.
  - 15.1.1: "A form R2 adds is a statement kind". The closing line of 15.13.8 leaves CUT-0's rules for the version-1
    kinds "the pin's to state".
  - His answer states the principle, *"every input the pinned rule reads must be fixed before the pin"*, then lists
    *"The stop row’s inputs"*. Draft 9's 15.13.4 calls that list every input of the pinned rule. Whether the principle
    reaches the other rows' inputs, and so puts R2 and the statuses' encoding before the pin, is his.
- **INPUTS-1, the twin's SN-3.** CHECKED. 15.9 says of the cut's bytes: "The tick block's frame, and the ports', are not
  yet derived." A decoding of the cut from `'R'` cannot be specified without them, so, if finding 20 puts the cut
  there, their derivation falls before the pin by his answer. P6 keeps its own trigger.
- **INPUTS-3.** His words, *"This settles the ordering question, not the underlying open rows themselves. They still
  require their own rulings and evidence before the build gate opens."*, are in `RULINGS.md`, not in draft 9.
  `DRAFT-9-CHANGES.md` says the same in the drafter's words ("orders the open rows before the pin and settles none of
  them").
- **CHANGED-1.** `REREAD-6-DISPOSITION.md` recorded TEST-3 as **[follows: his answers on Q1 and Q2]**. Draft 9 puts
  "its record names that candidate's digest" under a ruled tag, and 15.13.4's "The test's record names the digest of the
  candidate it ran on" too. His answer rules the test run against the resulting candidate and that candidate's digest
  pinned; that the record names the digest follows from it.

## The dispositions

| # | disposition | what is recorded |
|---|---|---|
| INPUTS-1 | OWED | 15.9 and 15.15's row on it: if finding 20 puts the cut in `'R'`, the tick block's and the ports' frames are derived before the pin, since its decoding needs them; P6 keeps its own trigger. **[follows: his answer on the pin's inputs]** |
| INPUTS-2 | ASK | whether his principle reaches the inputs of CUT-0's other rows: the version-1 statuses' encoding (the "four statuses" of the amended set's "identity and bytes") and the statement kinds R2's spellings add. 15.13.4 is corrected whatever he answers: the stop row's inputs are named as his list, never as every input of the pinned rule |
| INPUTS-3 | OWED | 15.13.4 quotes his *"This settles the ordering question, not the underlying open rows themselves. They still require their own rulings and evidence before the build gate opens."* |
| CHANGED-1 | OWED | in 15.13.4 and 15.13.8, that the test's record names the candidate's digest is tagged **[follows: his answers on Q1, Q2 and the pin's inputs]**; the ruled tag keeps the test run against the resulting candidate and that digest pinned |
| CHANGED-2 | OWED | 15.7.5's last sentence: the stop's NOT-RUN t is finding 8's, before the pin |

**Totals:** 1 ASK, 4 OWED: 5, each disposed once.

**The re-read owed before the build.** Draft 10 will apply the four OWED fixes, correct 15.13.4's naming of the inputs,
and state his answer. The twin re-reads every clause draft 10 changes and the clauses his answer affects (their A_r,
computed by `ar_compute.py` and recorded before the re-read). This record is that obligation. The gate is as before:
nothing of 1a against an unpinned CUT-0; every input the pinned rule reads, then the containment test, before the pin;
finding 8 and the amended set's 13 remaining rows each ruled before 1a's build (the release record); and N2, N3 and
every byte form open until he rules them.
