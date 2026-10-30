# Re-read 5: the disposition of the twin's 11 findings (2026-10-27)

The twin's report is `REREAD-5-REPORT.md`, saved unchanged; the text saved is equal to the hand-back in the twin's own
transcript. It read draft 7 (sha256 `130480ca…`), the clauses draft 7 changes, and the three sets of `AR-REREAD-5.md`.
By his ruling on the re-reads: *"Any further drafting fixes must be recorded with their required re-read before the
build, as R7 requires. Any issue needing your decision comes back to you; do not silently resolve it. Do not loop
indefinitely merely to obtain a clean report, but do not waive a required re-read or build gate either."*

So draft 7 stays as the twin read it. Every fix below is recorded here, to be applied in draft 8 together with his
answers to the questions below, so that one draft and one re-read carry both. Nothing is built: the build gate stays
closed.

The report shows neither that CUT-0 is sound nor that the version-1 containment check passes, and the twin says so.
Nothing here claims either.

Classes: **ASK** (put to the owner), **OWED** (a fix recorded for draft 8, or for the theorem ledger, re-read before
the build).

## Checked against the files first

- **CHANGED-1.** CHECKED. The phrase 15.15's row quotes, "had the missing input arrived, with any value", is the
  twin's own, from re-read 4's V1CHECK-4 (`REREAD-4-REPORT.md`), not his.
- **CARRIER-2.** CHECKED. 15.13.8's NOT-RUN/LOG-OPEN row reads "This row applies only when the law declares no
  read-once port or its log holds the read-once record", a condition on the log's content.
- **CARRIER-3.** CHECKED in RO′-3 (`RULINGS.md`, finding 6): at the stop the run ends "NOT-RUN naming the read-once
  port the end record names … or LOG-OPEN if the log has no end record". A NOT-RUN at the stop names a read-once
  port, whose kind the law declares.
- **CONTAIN-1.** CHECKED. His F6-14 answer names the object "the equality"; his V1CHECK-2 answer then makes the owed
  check containment. On the version-0 stand-ins, `packets/F-read-once-adversary.md` §4 MEASURED containment ("every
  claim the resumed run evaluated after the cut was in K̂"), as `REREAD-4-DISPOSITION.md` records.
- **ORDER-2, the twin's SN-1.** CHECKED in `RULINGS.md`. The default D10 (stated there so it can be overruled) puts
  the reference and SPEC §15 in 1a, and his finding-24 ruling speaks of *"the 1a reference"*. A containment check that
  executes version-1 laws over logs needs the version-1 reference, which is 1a's.
  His V1CHECK-3 answer says *"The check belongs on 1a’s build path"* and *"Do not build or run 1a against an unpinned
  CUT-0."* Whether the reference may be built before the pin, with nothing run against CUT-0 until it, is his.
- **CONTAIN-2.** The claims ruling, his words: *"No test result or measurement alone closes T10."* A check over
  fixtures can refute containment and cannot establish it "over any log". What the check is goes to him with ORDER-2.
- **ORDER-1, the twin's SN-3.** 15.15 lists finding 8 (the status's bytes and encoding) and finding 20 (whether `'R'`
  carries the cut) open. His order places the containment check before the pin and says nothing of either.
- **CARRIER-1.** RO′-5, ruled: *"That stop is a case of NOT-RUN or LOG-OPEN, not a fifth status."* His STOPROW-1
  answer: *"an explicit receipt status that distinguishes a stop caused by the absent record from a LOG-OPEN run"*,
  its encoding finding 8's. Read together, the stop is a NOT-RUN or LOG-OPEN whose status tells it apart. The draft's
  "of its own" is the drafter's, and leans toward a fifth status.

## The dispositions

| # | disposition | what is recorded |
|---|---|---|
| CARRIER-1 | OWED | 15.7.5 uses his words, "an explicit receipt status that distinguishes" the stop, in place of "of its own", and says beside RO′-5 that the stop stays a case of NOT-RUN or LOG-OPEN, not a fifth status; how the status shows it is finding 8's. Put to him as a confirmation in the message that carries the questions: a fifth status word would revise RO′-5, which only he can do |
| CARRIER-2 | OWED | 15.13.8's NOT-RUN/LOG-OPEN row applies when the receipt's status is not the read-once stop's, and the stop row's heading says the same by the status; the record's absence stays its cause, never what the court reads |
| CARRIER-3 | OWED | 15.7.5 says that a NOT-RUN at the stop names a read-once port (RO′-3), and that whether its status carries the same distinguishing mark as the LOG-OPEN case is finding 8's encoding; 15.15's finding-8 row lists it |
| CONTAIN-1 | OWED | 15.13.8's grades: in version 1 the equality holds by RO′-6's definition; the owed check is containment (his V1CHECK-2 answer); containment was MEASURED on the version-0 stand-ins and is DECLARED for version 1. His F6-14 sentence stays quoted as he gave it |
| CONTAIN-2 | ASK | what the containment check is: a test whose pass is MEASURED on its fixtures, T10.8 staying open; an argument over the closure, T10.8's obligation; or both. Put with ORDER-2 as one question |
| CONTAIN-3 | OWED | 15.15's row on 15.13.7 cites his V1CHECK-2 words ("the same law evaluates after the read-once stop, over any log that supplies the required record") as bearing on the continuation at the stop; the pin's wording stays open |
| ORDER-1 | ASK | where finding 8 (the stop status's encoding) and finding 20 (whether `'R'` carries the cut) fall in his order: before the pin, or after it and before 1a's rows |
| ORDER-2 | ASK | whether "Nothing of 1a is built or run against an unpinned CUT-0" lets the version-1 reference be built before the pin, so that it can run the check, with nothing run against CUT-0 until the pin. Put with CONTAIN-2 |
| ORDER-3 | OWED | 15.12.5, 15.12.6 and 15.13.11 point to 15.13.4's order; the order is tagged with the claims ruling's pin and his answer on V1CHECK-3, since it governs every row of 1a; 15.13.4 quotes his omitted words, *"labelling an unpinned proposal does not satisfy that condition"* and *"The check belongs on 1a’s build path"* |
| CHANGED-1 | OWED | 15.15's row on 15.13.7 attributes "had the missing input arrived, with any value" to re-read 4's V1CHECK-4 |
| T10-1 | OWED | in `ROUNDS.md`, the dated notes inside T10.0's and T10.8's statements move out into italic notes after them, as T10.7's did, each with a dated note saying so |

**Totals:** 3 ASK, 8 OWED: 11, each disposed once. The three ASKs go to him as two questions, with CARRIER-1's
confirmation beside them.

**The re-read owed before the build.** Draft 8 will apply the eight OWED fixes and state his answers. The twin
re-reads every clause draft 8 changes, the clauses his answers affect (their A_r, computed by `ar_compute.py` and
recorded before the re-read), and T10.0 and T10.8. This record is that obligation. Beyond it the gate stays as ruled:
nothing of 1a against an unpinned CUT-0, the containment check before the pin, and finding 8 and the amended set's 13
remaining rows each ruled before 1a's build (the release record). N2, N3 and every byte form stay open until he rules
them.
