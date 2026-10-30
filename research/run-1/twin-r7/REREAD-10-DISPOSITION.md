# Re-read 10: PROPOSED dispositions of the twin's 6 findings (2026-10-29)

**Status: proposed, then adopted.** *Adopted 2026-10-29: he chose S15.3-1 (a) and accepted the four drafting fixes and the 1a item, with a targeted re-read of draft 13, recorded in `RULINGS.md`, "Re-read 10's question".* As for draft 11, his instruction stands: findings and proposed dispositions come to
him before the draft is treated as settled. Nothing below is applied until he accepts it.

The twin's report is `REREAD-10-REPORT.md`, saved unchanged; the text saved is equal to the hand-back in the twin's own
transcript. It read draft 12 (sha256 `772fda52…`) whole, title to last line. It finds his five answers stated
faithfully, all fourteen of re-read 9's findings answered as adopted, the S1-S7 probe kept at its grade everywhere, and
draft 2 never presented as adopted or frozen. The report shows neither that CUT-0 is sound nor that the containment test
passes. The findings have fallen from 14 to 6, one of them for him.

Classes: **ASK** (his decision), **OWED** (a drafting fix for draft 13), **OPEN** (listed open, decided elsewhere).

## Checked against the files first

- **S15.3-1.** CHECKED in draft 12's 15.3: `close()` is "legal when … as above", with the effect "if every each-tick
  port is filled, the open tick runs at once". In a law with no each-tick port that condition holds vacuously, so a
  one-shot session can run a tick and project a `t` line, which his S15.5-2 answer refuses at load.
- **S15.9-2.** CHECKED in `CUT-SCHEMA.md`, line 170: its "does not show" still reads S6 "open under 4.3", beside the
  S6 row's dated note.

## Proposed dispositions

| # | proposed | what would be recorded |
|---|---|---|
| S15.3-1 | ASK | (a) now: in a law with no tick block, `close()` is refused (a move refusal of its own, or the existing AFTER-END-style refusal by name), so a one-shot session can never project a `t` line, recommended because his S15.5-2 answer already forbids the result and a session that writes a log its loader refuses is a defect today; or (b) within the A2 row, listed open with this conflict named |
| S15.5-1 | OWED | 15.5's order: a `t` line in a law with no tick block is refused LOG-RECORD with the read-once placement (D2.4), before any of D2.5's tick checks, so every such line is LOG-RECORD, as his words say **[follows: his answer on S15.5-2; D2.4]** |
| S15.9-1 | OPEN | the S1-S7 test's fixtures and pass condition on the version-1 reference, and who resolves a discrepancy and how, listed for 1a's specification |
| S15.9-2 | OWED | CUT-SCHEMA's "does not show" gains a dated note beside its "S6 open under 4.3": ruled by F20.4 on 2026-10-29 |
| S15.13-1 | OWED | 15.13.8's NOT-RUN/LOG-OPEN row: in a law with no tick block (a one-shot law's plain LOG-OPEN), nothing remains to run and K̂ is empty; T10.7's statement gains the same scope, with a dated note in `ROUNDS.md` **[follows: PP3; his answer on S15.5-2]** |
| S15.15-1 | OWED | 15.15's three new rows moved into section order |

**Totals proposed:** 1 ASK, 4 OWED, 1 OPEN: 6.

**What follows, if he accepts.** Draft 13 applies these. His word on convergence: *"Do not loop indefinitely merely to
obtain a clean report, but do not waive a required re-read or build gate either."* Draft 13's changes are small and touch
no settled semantics beyond S15.3-1's answer, so the re-read owed could cover draft 13's changes and their affected
clauses rather than the whole draft; that is his choice. After its disposition, the publication decision is his.
