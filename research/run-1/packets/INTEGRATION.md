# The five packets, integrated (2026-10-26)

Packets A to E in this folder are research subagents' reports, saved unchanged. Each was asked one question, read the
working tree on top of 95dac79, and ran nothing. This record is the integrator's (the draft's author): where the
packets meet, which of their claims were checked against the files, which records were corrected, and what goes to the
owner first. Nothing here is ruled. The rulings are his, recorded in his words in `RULINGS.md` when he gives them.

Labels: **RULED**, **OPEN**, **INFERENCE**, and **CHECKED** (read here against the file named, with its result).

## 1. What each packet recommends

| packet | question | recommendation (OPEN) |
|---|---|---|
| A, `A-D10-R6.md` | finding 24: D10's REFERENCE-ONLY against R6's rows | **D.** Rule D10's court clause with one scope sentence. Real version-1 readings stay REFERENCE-ONLY in 1a (court R1 unchanged). R6's rows, the PREFIX row and their controls run in 1a's reference with the witness configured as agreed, each row stating that its agreement is configured, not measured. It needs two confirmations: court R1 stays beside E2, and rider 1's configured witness reaches the PREFIX row and the controls |
| B, `B-PREFIX.md` | findings 3 to 5: the licence | **B1 + 4a + 5c + K1.** R6's own boundary: the first top-level clause that is or holds a port declaration of either kind, or is the tick block. A claim is licensed exactly when it stands before that boundary, outside the tick block, and no clause from the boundary on may execute it (closure over every arm, loop body, tick body and Perform, transitively, values ignored, failing closed). It interprets R6 and declines D-18's widening |
| C, `C-read-once-ports.md` | finding 6: read-once ports | **Meaning A, RO-1 to RO-6.** Arrivals only. One read-once record, closed once before any tick. The run starts only if the record is complete; otherwise NOT-RUN naming the first empty read-once port, with no statement executed. That is a case of NOT-RUN, not a fifth status. COMPLETED never stands without the record. Every claim is UNREACHED at that NOT-RUN, and CUT-0's NOT-RUN row is scoped to t ≥ 1. Every byte form is left open |
| D, `D-LOG-refusals.md` | finding 8: load refusals | **Load whole, after the law compiles; (W).** The nine codes take the conditions as worded, in the model's phase order, with sub-choices (a) to (e) open. A load refusal writes no receipt; the witness records the code, the line, a message and a digest under a name of its own; exit 1; no court reading. The end record's t = n+1 holds for each-tick ports. A read-once line appears only when the law declares a read-once port |
| E, `E-release-gate.md` | the held push | The push still needs the amended set's 14 rows and the format-freeze disposition ruled, then the gate on the exact final tree. The 74 re-reads and every A_r are build conditions in his words, not push conditions. The partition and privacy are clean. It names 13 risks the records did not |

## 2. Where the packets meet

**I-1. A's D makes B's rows observable.** B's control row (L8, "licensed") "cannot be observed until finding 24 is
ruled". Under D it runs in 1a with the configured witness, and so do B's other licence rows. Rule 24 with or before
PREFIX.

**I-2. The reviewer's alternative C cannot be ruled before PREFIX.** Its domain (the claims R6 authorizes under the
licence) is undefined while findings 3 to 5 are open (A). B shows exactly where: the review's P13, B's L1, is licensed
under D-18's boundary (B2) and not under R6's (B1). D does not depend on the boundary.

**I-3. B and C rest on one clause that no ruling holds.** §15.7.1, "a read-once port binds where its declaration
stands", is tagged `[ruled: R5]`. R5's words fix only that the read-once `'N'` events come before the first `'T'`
(CHECKED: `RULINGS.md` R5's adopted text). "Where its declaration stands" is contract draft 0's §4.1 (CHECKED:
`CONTRACT-DRAFT.md`).
- B's recommendation states it as its one presupposition: no input is bound before the boundary's position.
- C's RO-3 relies on it.
- If binding moved to the run's start, B finds that T9's first-`'N'` reading would exempt nothing in a law with a
  read-once port, and C finds that R1's "every later claim" would become every claim.

So the finding-6 ruling should say where a read-once value binds. The draft's tag is wrong either way (section 4).

**I-4. C's "nothing runs" meets B's licence.** Under C's meaning A, a missing read-once value leaves a licensed prefix
claim UNREACHED (B's L3 §1, the review's P16 claim 0). Under A′ the prefix would run up to the declaration, and the
claim could be held, but A′ needs a new, named CUT-0 row (C's counterexample 2). D's (W) has the same shape: a
malformed log gives a prefix claim no reading at all (Round D's LOAD-ORDER law).
- INFERENCE: neither contradicts his PREFIX settlement, which speaks of a claim "that evaluated true" before a refusal
  downstream. In both cases nothing evaluated.
- It is a cost he should see when ruling finding 6: the licence gives standing only to a claim that ran.

**I-5. `not-run 0` against t = n+1.** C and D agree that Round D's F4 and F5 dispositions clash in bytes: with no tick
record, t = n+1 gives 1. D scopes t = n+1 to each-tick ports, so that finding 8 does not decide finding 6 by the back
door. Finding 6's meaning should be ruled before finding 8's read-once parts; finding 8's other codes need not wait.

**I-6. Whether a read-once line is always present.** C and D agree: only when the law declares a read-once port, against
Round D F1's "always written". That keeps every existing log, the 25 named malformed logs and the review's P01 and P02
as they are.

**I-7. When the provenance line prints.**
- C reads R6's trigger as firing at a read-once NOT-RUN, since the law declares a port. Round D F10's "only when an
  `'N'` or a `'T'` was emitted" would print nothing there (a ledger note was added).
- D's (W) prints no line for a log refused at load.
- D names its own falsifier: if the owner reads the one-seal rider as requiring a line for every log offered with a
  version-1 law, (W) conflicts with a ruling.

Question for the owner, with finding 8: is the line owed per court reading, or per log offered?

**I-8. Court R1 beside E2.** A's D rests on it (A's open question 2), and B leaves "how GROUNDED and HELD combine"
(finding 47) undecided. If E2 is read as the whole of HELD, D10 conflicts with the claims ruling with or without R6 (A).

**I-9. `Reach` fails open, and PREFIX and CUT-0 share it** (B, headline 5).
- CHECKED: in `probes/cut0_claims.py`, `inline` returns the empty set for anything but a claim or a Perform, and
  `stmt` names definitions, loops and Ifs only.
- CHECKED from `src/orlog/syntax.py`: the other version-0 statements (Let, Set, Change, Say, Must, Append, RemoveLast)
  hold neither, so the default is complete for version 0. It fails open for a version-1 tick block given no case of
  its own.
- Because the two consumers share it, comparing them cannot show a shared omission. B's oracle row is the independent
  check: every evaluation of a licensed claim precedes the first input on every fixture and log, with the trace used
  as a check, never as the rule.

Recorded in `CUT-0.md` §2's limits.

**I-10. Names that collide (drafting, not rulings).**
- §15.0's "Prefix" names every statement before the tick block, but the PREFIX licence excludes some of them (B). C's
  RO-3 uses "prefix" in §15.0's sense.
- "Door" names the input door at 15.0 and the source-text door at 15.1.5 (E).
- The court's own rule list has "R6 premises" (`src/orlog/court.py`), beside the sheet's R6, as with the two R8s (B).

**I-11. The review's probes cannot read GROUNDED as written.** A and B both found that P12, P16, P29, P31, P33 and P35
have no "by …", so their channel is computation and never grounds. P29(a), P31 and P33 expect "GROUNDED but not HELD",
which contradicts finding 47's disposition. B's laws all say "by the owner". The twin should see this at the re-read.

## 3. Checked against the files, and the records corrected

Each correction is a dated note in place; nothing earlier was rewritten.

| record | packet | check | change |
|---|---|---|---|
| `ROUNDS.md`, Round D row 1 | D | CHECKED against `serialize` and `parse_log`: the probe writes `t`, has no `once` line, no tag byte, and only `fix each-tick` in the port signature | the row's claim that the probe "holds the same grammar" is corrected |
| `ROUNDS.md`, Round D row 4 | C, D | CHECKED: `parse_log` requires t = n+1 and the probe has no read-once port | note: `not-run 0` clashes with row 5 and was never checked |
| `ROUNDS.md`, Round D row 10 | C | read against R6's adopted row | note: its last sentence conflicts with R6's trigger; R6 governs |
| `ROUNDS.md`, Round D row 18 | B | CHECKED: 5e49b18 (R6 ruled) is an ancestor of 95dac79, which ROUNDS.md cites | note: its boundary widens R6, and adopting it would amend R6 |
| `ROUNDS.md`, the held push's R7 row | E | read | its pre-ruling text marked superseded; the status reads ruled |
| `ROUNDS.md`, the held push's gate row | E | read | note: its comparison rules and its record's place are unwritten |
| `CUT-0.md`, §3's limits | C, D | CHECKED as for row 1 | added: read-once ports, and §15.5's grammar |
| `CUT-0.md`, §2's limits | B | CHECKED (I-9) | added: `Reach` on version 1 |
| `twin-r7/DISPOSITION.md`, the grouped list | E | CHECKED against rows 10, 27, 37 and 43 | added 43 and the three dropped deciders; it now covers all 29 |
| `manifold/adversary/RERUN.md`, line 13 | E | CHECKED: each current file's header hashes the two probes and its script only | corrected |
| `STATUS.md` | E | read | R7 counted as ruled; `packets/` listed |

E's risk 8 was CHECKED by bytes. The seven first-form outputs in `manifold/adversary/` have mixed line endings. The six
current reruns, evidence/ and `manifold/*.txt` are LF. (The integrator's first count, by grep, said all thirteen; that
was wrong, an artifact of grep's CR pattern on files holding non-ASCII text.)

## 4. Not changed: draft 1's errata, held for draft 2

Draft 1 (sha256 `367b1b48…`) is the object of the 74 re-reads. Changing it now would move that set. The errata below
are to be applied after the first rulings, with the clause comparison computed again:

- "Sheet R14" (L260, L278) is the speed verdict's R14. `RULINGS.md` has no R13 or R14 (E; CHECKED).
- §15.7.1's `[ruled: R5]` overstates. R5 holds only "before the first `'T'`"; "where its declaration stands" is
  contract draft 0's (B, C; I-3).
- 15.10 L259 holds finding 32's open choice under `[ruled: R5]` (E).
- Missing tags (E):
  - R10 on 15.5 (L151, L160) and 15.6;
  - D1 on 15.5; D3 on 15.5 and 15.7.5; D5 on 15.7.1; D6 on 15.10 L262; D9 on 15.3 and 15.5;
  - D10 on 15.12.5 and 15.12.6; PREFIX on 15.12.4's body;
  - port place, the statuses, A2 and the freeze on 15.13.8's tick-block and NOT-RUN/LOG-OPEN rows and on 15.13.9;
  - the codes row on 15.13.5;
  - the session record on 15.3 L117-121;
  - A2 on 15.5 L158.
- D2 and D4 have no clause at all (E).
- The twin's own tag-audit lines (`twin-r7/REPORT.md`, "Missing dependencies") were never numbered in DISPOSITION and
  never applied (E, risk 1). They are R7's D_r and enter every A_r they name.
- The collisions of I-10.

## 5. The re-reads, as the packets leave them

- **The 74.** The changed or added clauses of `twin-r7/DRAFT-1-CHANGES.md`, reproduced exactly by E.
- **Beyond the 74:** T10.5's statement, changed after the twin read it (E, risk 7). It is in R7's reading set but not
  in the 74.
- **Each A_r = T_r ∪ L_r ∪ D_r**, recorded when its ruling is. E's T_r and L_r tables (E §1 A) are a starting point,
  not the record. D_r includes the twin's tag-audit lines.
- **Timing.** One re-read after ruling r, of each clause as r leaves it, meets both the draft-1 re-read and A_r's for
  r. That is E's literal reading of R7; R7 does not say. A re-read before the ruling cannot count as A_r's.

Proposed: hold the 74 until the first batch of rulings. Then the twin reads each clause once per ruling whose A_r holds
it, and a clause in no A_r once.

## 6. Release readiness beyond the rulings

- **The push's conditions** (the held-push table in `ROUNDS.md`): the amended set's 14 rows and the format freeze, then
  the gate on the exact final tree.
- **Commit 3** gains `research/run-1/packets/*.md`.
- **The seven first-form outputs.** Under `* text=auto eol=lf` git would store them LF, not as captured. One line,
  `research/run-1/manifold/adversary/*.txt -text`, keeps them byte-exact, as `.gitattributes` already does for recorded
  runs. The owner's call, since `.gitattributes` joins a commit.
- **The gate's procedure is unwritten** (E, risks 10 and 11). Proposed, before the gate:
  - which outputs are compared byte for byte, and which are excluded and why (timings; outputs run once);
  - the seconds mask, written as a pattern in advance;
  - `make_laws.py` run in a scratch copy, never over commit 1's files;
  - the gate's output kept outside the tree, with the tree id it ran on recorded beside it.
- **P1 to P7** (the schema's compatibility policy) have no ruling item (E, risk 12).

## 7. What goes to the owner first

Finding 24, with findings 3 to 5 beside it, as the plan asked. Then finding 6 (read-once ports) and finding 8 (load
refusals), in that order, for I-5's reason. The questions are put in the conversation; his answers are recorded in
`RULINGS.md` in his words.
