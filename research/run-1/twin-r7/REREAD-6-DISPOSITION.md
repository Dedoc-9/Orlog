# Re-read 6: the disposition of the twin's 10 findings (2026-10-27)

The twin's report is `REREAD-6-REPORT.md`, saved unchanged; the text saved is equal to the hand-back in the twin's own
transcript. It read draft 8 (sha256 `53d46821…`), the clauses draft 8 changes, and the three sets of `AR-REREAD-6.md`.
It finds his three answers stated faithfully and re-read 5's eight OWED fixes applied as disposed.

His word on the re-reads stands: *"Any further drafting fixes must be recorded with their required re-read before the
build, as R7 requires. Any issue needing your decision comes back to you; do not silently resolve it. Do not loop
indefinitely merely to obtain a clean report, but do not waive a required re-read or build gate either."* So draft 8
stays as the twin read it. Every fix below is recorded here, to be applied in draft 9 with his answer to the question
below, and re-read once before the build.

The report shows neither that CUT-0 is sound nor that the version-1 containment test passes, and the twin says so.
Nothing here claims either.

Classes: **ASK** (put to the owner), **OWED** (a fix recorded for draft 9, re-read before the build), **ANSWERED** (the
files already answer it; nothing changes).

## Checked against the files first

- **T10-1, the twin's SN-1.** CHECKED in `ROUNDS.md`. His Q1 answer is recorded in T10.8's last column, its notes
  (*"Added 2026-10-27 by his answer on re-read 5's Q1: …"*). `T10-STATEMENTS.md` carries each row's statement column
  only, so the twin could not see it. Nothing is missing.
- **PIN-1, the twin's SN-2.** CHECKED in `CUT-SCHEMA.md`: the cut's place is the `'R'` event's payload (draft 2), and
  P6 freezes the format "by the owner's ruling, before the first version-1 receipt is frozen anywhere". Nothing in
  `CUT-0.md`, `CUT-SCHEMA.md` or draft 8 states whether the rule the digest identifies decodes the cut from those
  bytes or takes it from the execution. The condition the twin puts on PIN-1 cannot be settled from the files, so it
  goes to him with PIN-3.
- **PIN-3.** 15.13.8's stop row rests on 15.1.3's top-level place and 15.7.1's counting, both open. 15.15 has them
  decided by "the pin; the amended set's 'port place' and 'counting'". The release record defers those rows to rulings
  before 1a's build, and says nothing of the pin. His Q2 answer gives the reason for fixing an input before the pin:
  *"Both affect the rule being identified by the digest."* It names findings 8 and 20 only.
- **PIN-4.** His word on the push, step 2: *"Resolve Finding 8 and Finding 20 before pinning CUT-0."* Step 3: *"Run
  the version-1 containment fixture test and record its limited evidence"*. Draft 8 lists the test first.
- **TEST-3.** His Q2 answer: a decision that later changes the rule makes *"a new CUT-0 candidate requiring a new
  digest and the applicable checks"*. A test run on one candidate does not stand for another.

## The dispositions

| # | disposition | what is recorded |
|---|---|---|
| TEST-1 | OWED | 15.13.8 says that V1CHECK-2's sentence names the property (every log that supplies the record) and Q1's the test that samples it, and that a pass means on the tested logs only |
| TEST-2 | OWED | 15.15's row on 15.13.8: the fixture set is fixed and recorded before the test runs, decided by 1a's specification, not by the pin |
| TEST-3 | OWED | 15.13.8 and 15.13.4: the test's record names the digest of the CUT-0 candidate it ran on; the pin pins that digest; a change between the test and the pin is a new candidate, tested again. **[follows: his answers on Q1 and Q2]** |
| PIN-1 | ASK | whether the cut's bytes in `'R'` are fixed before the pin, if finding 20 puts the cut there and the pinned rule reads it from them. Put with PIN-3 as one question |
| PIN-2 | OWED | 15.15's "15.5 and 15.6" row: its finding-8 items are resolved before the pin too, since his answer names the whole finding |
| PIN-3 | ASK | whether the stop row's premises, the port place (15.1.3) and counting (15.7.1), are fixed before the pin |
| PIN-4 | OWED | 15.13.4 follows his sequence: findings 8 and 20 resolved and recorded; then the containment test; then the pin; then 1a's rows |
| RO5-1 | OWED | 15.7.5 names the stop's status one way, his confirmation's "an explicit distinguishing status form", and keeps his STOPROW-1 words for what the form does |
| CHANGED-1 | OWED | 15.13.8's account of the version-0 result is tagged **[follows: `packets/F-read-once-adversary.md` §4, as `REREAD-4-DISPOSITION.md` checked it]**; only the grades stay under his F6-14 answer |
| T10-1 | ANSWERED | his Q1 answer is in T10.8's notes column (above); nothing changes |

**Totals:** 2 ASK, 7 OWED, 1 ANSWERED: 10, each disposed once. The two ASKs go to him as one question.

**The re-read owed before the build.** Draft 9 will apply the seven OWED fixes and state his answer. The twin re-reads
every clause draft 9 changes and the clauses his answer affects (their A_r, computed by `ar_compute.py` and recorded
before the re-read). This record is that obligation. The gate is as before: nothing of 1a against an unpinned CUT-0;
findings 8 and 20, then the containment test, before the pin; finding 8 and the amended set's 13 remaining rows each
ruled before 1a's build (the release record); and N2, N3 and every byte form open until he rules them.
