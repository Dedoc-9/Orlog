<!-- Packet B, saved by the draft's author, 2026-10-26: a research subagent's final report, delivered as its message (subagents cannot write files; its output file is empty). Copied without change. -->

# Decision packet: PREFIX (review findings 3, 4 and 5)

This was research only. I edited, built and ran nothing, and committed nothing. Line numbers are from the working tree. `RULINGS.md` has uncommitted changes, but the licence text matches the ruling commit 5e49b18 (checked with `git show`). `ROUNDS.md`, `SPEC-15-DRAFT-1.md` and `twin-r7/` are untracked.

**Labels used throughout:**
- **RULED**: fixed by one of the owner's rulings.
- **OPEN**: a proposal no ruling has adopted.
- **INFERENCE**: my reading of the sources.
- **PROPOSED WORDING**: text I am offering for a ruling.

## Headline findings

1. **[INFERENCE] Finding 3 is not caused by draft 0's term.** The proposal's origin is the disposition of Round D's finding 18 (`research/run-1/ROUNDS.md:285`). It defines the point as "the first read-once port declaration, or the tick block, whichever comes first". It also says the closure "mends the other direction the adversary found, since an each-tick port's declaration is not an input point". Under that definition the twin's P13 claim is licensed too. So the open row is wider than ruled R6 under both readings. Draft 1's open bracket (`SPEC-15-DRAFT-1.md:305-310`) names only the "first place a port is read" reading.
2. **[INFERENCE] D-18 was proposed after R6 was ruled.** R6 was ruled in commit 5e49b18. `ROUNDS.md`'s header cites 95dac79, a later commit. ROUNDS.md is untracked, so git does not date its sections; this rests on commit order only.
3. **[INFERENCE] R6 as ruled already decides P15, the case behind finding 4.** Three parts of R6 settle it: the licence's head sentence, the trigger sentence (`RULINGS.md:237-238`), and the acceptance row "a claim in a procedure performed in the tick block reads UNGROUNDED" (`RULINGS.md:254`). Only the two position bullets go vacuous. The gap is in the decidable test, not in the rule.
4. **[INFERENCE] For finding 5, "necessary only, never sufficient" is not an available reading.** The owner's control rider and his PREFIX settlement both require some claims to be licensed.
5. **[INFERENCE, from code] `Reach` fails open on statement kinds it does not know.** In `research/run-1/probes/cut0_claims.py:159-167` and `139-146`, any statement it does not name returns the empty set. A version-1 tick block added without its own case would drop out of the closure silently and license every claim in it.

## 1. The governing wording

**RULED, by reference.** Option a's row reads: "in a run with an input log (the law declares a port, or has a tick block), no claim is GROUNDED, whatever its channel and whatever is ratified, except under the licence below" (`research/run-1/RULINGS.md:233`).

The owner's words: *"I rule Option a (Data, never a channel) for `RUN-1`. The primary principle is unyielding: replayable data is not admissible testimony."* (`RULINGS.md:285-286`).

The trigger, the licence and the acceptance rows are the sheet's text under "Recommended: a". They were adopted by that ruling, but the words are the sheet's, not his.

**RULED (sheet's text), the trigger** (`RULINGS.md:237-238`): "A tick block with no port still takes input, because the log's length sets how many ticks run (D3)."

**RULED (sheet's text), the licence** (`RULINGS.md:239-249`):
- "The licence, PREFIX, decided from the text: a claim is exempt only if every evaluation of it precedes the first input."
- "It must stand before the first port declaration, outside the tick block."
- "It must not sit in a procedure performed at or after the first port declaration. The licence is decided by evaluation, never by position alone: a claim inside a procedure stands textually before the tick block and still runs during it."
- "Nothing the log sets exists before its first input, so a prefix claim's whole claim line is fixed by the law: its evaluations, its trues, its cost and its certified clause's cost."
- The wider licence (a claim with no path from any port) "waits for a trigger".

**RULED (sheet's text), the acceptance rows** (`RULINGS.md:250-256`), each with its plant:
- a claim that reads only `x`, where `x` is updated from a port, reads UNGROUNDED;
- a claim in a tick block with no port reads UNGROUNDED (plant: the trigger "declares any port");
- a claim in a procedure performed in the tick block reads UNGROUNDED (plant: licensing by clause position);
- "a claim before the first port, in a procedure performed after a port is read, is not licensed (plant: 'before the first port declaration is enough')".

"Sound, not complete" is at `RULINGS.md:258-260`.

**RULED, the owner's own words:**
- Witness rider: *"Every row testing an ungrounded port violation must run with the witness explicitly configured as agreed"* (`RULINGS.md:293-294`).
- Control rider: *"Each test row is structurally paired with an internal control variant. The control evaluates the exact same claim without an active log declaration, or wraps it securely within the `PREFIX` license parameters. The control must return a clean `GROUNDED` standing"* (`RULINGS.md:295-297`).
- Settlement: *"A claim wrapped within the `PREFIX` license parameters that evaluated true remains historically held, regardless of whether the execution loop encounters a subsequent transactional refusal downstream."* (`RULINGS.md:300-302`).
- R1's cost sentence, ruled with R6: *"Moving a world property out of the law and into a read-once port means the cost of rule a reaches every later claim in the run, stripping them of grounding even if they never touch that property directly."* (`RULINGS.md:56-57`).
- **RULED, R5:** "The read-once ports' 'N' events come before the first 'T'." (`RULINGS.md:184`).

**OPEN:**
- The amended set's row, kind N: "by static closure from the first input point; every consumer of `Reach` states its own soundness requirement" (`ROUNDS.md:450`). Its decision-table entry is "D-18 | PREFIX by static closure from the first input point, not by the trace | two-way" (`ROUNDS.md:383`). Its origin is `ROUNDS.md:285`, quoted in §2.
- T9's refinement (`ROUNDS.md:326`): "define 'the first input' as the first `'N'`, or the first `'T'` when the law has no port".
- The disposition's two proposals (`twin-r7/DISPOSITION.md:38-39`): "in such a law the first input is the tick block's start"; "a claim is exempt exactly when they all hold".
- The author's gloss on R1's sentence, which is not the owner's words (`RULINGS.md:57-59`): "a claim in a procedure performed after the port is read is stripped too".
- `SPEC-15-DRAFT-1.md:179`, "A read-once port binds where its declaration stands". It is tagged [ruled: R5], but those words are not R5's (`twin-r7/REPORT.md:235-237`).
- Draft 0's term, dropped in draft 1: "Input point: the first place a port is read in evaluation order" (`twin-r7/SPEC-15-DRAFT-0-AS-REVIEWED.md:27-28`). The disposition calls it "the author's own term" (`DISPOSITION.md:37`).

## 2. What is settled and what is open

**Settled.** The licence is decided from the text, by evaluation, never by position alone. It has three necessary conditions (the head sentence and the two bullets). It covers the whole claim line. The four acceptance rows and the riders stand.

**Open.** Three things:
- what "the first input" is in a law with no port;
- whether any condition is sufficient;
- the decision procedure.

**What "the first input point" meant where the proposal was written.** The origin is `ROUNDS.md:285`. The adversary's dynamic repair is "rejected" because "That lets whoever chooses the log choose the standing… which R6 forbids". The repair it proposes instead: "A claim is PREFIX if and only if it lies outside the may-execute closure (`Reach`…) of the top-level clauses from the first input point on: the first read-once port declaration, or the tick block, whichever comes first. Procedures performed from there are included transitively."

The "other direction" it claims to mend is `ADVERSARY-ROUND-D.md:515-516`: with each-tick ports declared at the top, "no prefix claim qualifies, although every prefix evaluation precedes the first 'N'".

**[INFERENCE]** D-18 therefore has three parts:
- a decision procedure (`Reach`), which stays within R6;
- an "if and only if", which stays within R6 (see §3.3);
- a boundary that leaves out each-tick declarations, which widens R6.

One author has produced four readings of where the boundary falls:
- R6's bullet: the first port declaration.
- D-18 and T9: the first read-once declaration or the tick block (as a dynamic event, the first 'N' or 'T').
- Draft 0: the first place a port is read.
- The doppler debate: "every evaluation of the claim precedes the first tick" (`research/doppler/VERDICT.md:79-81`, `101-104`).

**How R6's words treat a procedure performed after the first port declaration.** Bullet 2 (RULED) excludes such a claim, wherever its text stands:
- (a) a procedure performed both before and after the declaration (the twin's P14) is excluded;
- (b) **[INFERENCE]** so is one performed after an each-tick declaration but before tick 1 (law L2 below), although every evaluation of it precedes the first input in the dynamic sense;
- (c) **[INFERENCE]** read "by evaluation", "performed" is transitive, so a procedure performed only through another procedure performed later (law L10, Round D's d04) is excluded. Acceptance row 4 is an instance of this.

The "at" in "at or after" has no case under the proposed forms, unless port place lets a port stand inside a procedure (INFERENCE).

## 3. Decision matrix

The laws use the draft's spellings (`SPEC-15-DRAFT-1.md:45-49`). Each claim is "by the owner", so its channel can ground (`src/orlog/court.py:96-98`). "Licensed" means exempt from R6. GROUNDED also needs held, ratified and an agreed witness.

**L1** (the twin's P13):
```
§1 Let thrust be given each tick as an integer.
§2 We claim that 2 plus 2 equals 4, by the owner.
§3 Each tick, do the following.
§3.1 Say thrust.
```

**L2** (a procedure performed between the each-tick declaration and the tick block):
```
§1 To check, do the following.
§1.1 We claim that 2 plus 2 equals 4, by the owner.
§2 Let thrust be given each tick as an integer.
§3 Perform check.
§4 Each tick, do the following.
§4.1 Say thrust.
```

**L3** (R1's cost sentence: a read-once port that is never read):
```
§1 We claim that 3 is odd, by the owner.
§2 Let gravity be given as a fixed.
§3 We claim that 4 is even, by the owner.
§4 Each tick, do the following.
§4.1 Say 1.
```

**L4** (the first read across a procedure):
```
§1 Let thrust be given each tick as an integer.
§2 To show, do the following.
§2.1 Say thrust.
§3 We claim that 2 plus 2 equals 4, by the owner.
§4 Each tick, do the following.
§4.1 Perform show.
```

**L5** (D-18's own counterexample, run on two logs: n = 1, 2 and n = 7):
```
§1 Let x be 0.
§2 To check, do the following.
§2.1 We claim that x is less than 7, by the owner.
§3 Perform check.
§4 Let n be given each tick as an integer.
§5 Each tick, do the following.
§5.1 Set x to n.
§5.2 If n equals 7, do the following.
§5.2.1 Perform check.
```

**L6** (the twin's P15):
```
§1 To check, do the following.
§1.1 We claim that 2 plus 2 equals 4, by the owner.
§2 Each tick, do the following.
§2.1 Perform check.
```

**L7** (no port; claim before the tick block):
```
§1 We claim that 2 plus 2 equals 4, by the owner.
§2 Each tick, do the following.
§2.1 Say 1.
```

**L8** (the control's shape; the twin's P12 without the refusal):
```
§1 We claim that 2 plus 2 equals 4, by the owner.
§2 Let thrust be given each tick as an integer.
§3 Each tick, do the following.
§3.1 Say thrust.
```

**L9** (a call behind a constant-false condition):
```
§1 To check, do the following.
§1.1 We claim that 2 plus 2 equals 4, by the owner.
§2 Perform check.
§3 Let thrust be given each tick as an integer.
§4 Each tick, do the following.
§4.1 If 1 equals 2, do the following.
§4.1.1 Perform check.
§4.2 Say thrust.
```

**L10** (Round D's d04 in the draft's spellings):
```
§1 Let x be 1.
§2 To inner, do the following.
§2.1 We claim that x equals 1, by the owner.
§3 To outer, do the following.
§3.1 Perform inner.
§4 Let n be given as an integer.
§5 Set x to n.
§6 Perform outer.
```

**L11** (hypothetical): a port declared inside a top-level While, after a claim in the same body. The twin's P21 expects this to be refused PORT-PLACE, and I did not check how `Let` scopes inside a loop. It matters only if port place permits nested ports.

### 3.1 Where the first input falls (finding 3)

**B1. The first port declaration of either kind, else the tick block.**
- PROPOSED WORDING: "the first top-level clause that is, or holds, a port declaration, or is the tick block".
- L1: not licensed. L2: not licensed. L3 §3: not licensed. L5: not licensed on either log.
- **Within R6:** these are its own words, with the portless case covered in §3.2.

**B2. The first read-once declaration or the tick block (D-18's origin).**
- L1: licensed. L2: licensed. L3 §3: not licensed. L5: not licensed.
- **Widens R6:** it contradicts both bullets, so it needs an amendment of R6.
- [INFERENCE] It is sound only once port place (b) is ruled, which refuses reads of each-tick ports outside the tick block (Round D finding 14). Under port place (a), where each-tick ports are declared inside the tick block, it gives the same results as B1.

**B3. The first place a port is read (draft 0).**
- L1: licensed. L2: licensed. L3 §3: licensed, though his cost sentence strips it.
- L4: undefined. The first read is §2.1 in the text but §4.1 in evaluation, so claim §3 is either licensed or not. Under port place's textual reading §2.1 is itself refused (finding 28, the twin's P18).
- **Widens R6** and contradicts his ruled cost sentence. With read-once binding at its declaration, it also breaks R6's head sentence. Needs an amendment.

**B4. Tick 1 as a static boundary (the doppler debate's "first tick").**
- L1: licensed. L2: licensed. L3 §3: licensed. L5: not licensed.
- **Widens R6** and contradicts his cost sentence on L3. Needs an amendment.

**B5. A dynamic test** ("every 'C' event precedes the first 'N'", `ADVERSARY-ROUND-D.md:524-525`).
- L5: licensed on the log with n = 1, 2; not licensed on the log with n = 7, so the standing depends on the log.
- **Outside R6:** it breaks "decided from the text".
- As T9's definition of the term "first input" it is coherent. As the test that decides the licence, it is not.

### 3.2 A law with a tick block and no port (finding 4)

**4a. The boundary is the tick block** (the "or is the tick block" in B1's wording).
- L6: not licensed. L7: licensed.
- **Interprets R6:** it follows from R6's head, its trigger sentence and its row at `RULINGS.md:254`.

**4b. The bullets alone, read vacuously.**
- L6: licensed. L7: licensed.
- Contradicts R6's head and its row at line 254, the doppler debate's N-1 plant "licensing by clause position". Not available.

**4c. No licence at all without a port.**
- L6: not licensed. L7: not licensed.
- **Narrows R6.** The "only if" text tolerates it, but reading "before the first port declaration" as unsatisfiable when none exists is strained. It needs his explicit choice. His control can still be met with a law that has a port.

### 3.3 Necessary only, or also sufficient (finding 5)

**5a. Necessary only; nothing is sufficient.**
- L8: not licensed. L9: not licensed.
- Contradicts his control rider (`RULINGS.md:295-297`) and his settlement (`300-307`). Not available.

**5b. Exempt exactly when R6's conditions hold, judged by actual evaluation over every log.**
- L8: licensed. L9: licensed (§4.1.1 never runs).
- Within R6 in what it licenses, but it is not a usable decision procedure: it needs value analysis over every log. T12 is CONJECTURED, and the ledger says "No relaxation of R6 may cite it" (`ROUNDS.md:337`).

**5c. Exempt exactly when the static test holds:** bullet 1, plus the closure in §3.4.
- L8: licensed. L9: not licensed.
- **Within R6.** [INFERENCE] It implies every necessary condition, provided `Reach` over-approximates what may execute and no input binds before the boundary's position. It licenses less than 5b. It is an interpretation he would confirm.

### 3.4 How the static closure is computed

**K1. `Reach`, with values ignored.**
- It follows every If arm and the Otherwise, every loop body, the tick block's body, and every Perform transitively.
- Its start set is the top-level clause that is or holds the boundary, plus every later top-level clause.
- A statement kind it does not know licenses no claim (fail closed).
- L10: not licensed. L5: not licensed on either log. L9: not licensed. L11: not licensed.
- **Within R6** (5c).

**K2. Position plus direct Performs only** (the textual test of `CONTRACT-DRAFT.md:160-162`).
- L10: licensed, a false GROUNDED. This is Round D's finding 18; d04 lives under the ignored `work/` folder, so from the tree it is only OBSERVED (`ROUNDS.md:263-264`).
- Breaks "never by position alone". Usable as a plant.

**K3. Decided from the trace.**
- Fails on L5. Breaks "decided from the text". Usable as a plant.

**K4. K1 plus value analysis** (constant conditions).
- L9: licensed.
- Within R6 if sound, but it adds a second analysis with its own soundness obligation. Not needed.

**K5. K1 started at the declaration's own clause, or without a tick-block case.**
- L11: licensed. On L6, `Reach` returns the empty set for the tick block (`cut0_claims.py:159-167`), so §1.1 is licensed.
- Unsound. Two plants.

**Facts the closure would rest on:**
- [INFERENCE] SPEC's PERFORM-BEFORE-DEFINITION rule (`SPEC.md:165-166`, `344`) means a claim outside K1's closure either stands before the boundary or is never evaluated. A never-evaluated claim is UNREACHED and never GROUNDED, so keeping bullet 1 in the test costs nothing.
- [INFERENCE] `Reach` is research code for version 0 only ("nothing in the program reads it", `cut0_claims.py:1-2`). It has no case for ports or the tick block.

## 4. The narrowest recommended decision

It combines B1, 4a, 5c and K1.

**PROPOSED WORDING:** "The licence is decided from the law's text alone, never from a log or a trace. The boundary is the first top-level clause, in the text, that is or holds a port declaration, or is the tick block. A claim is licensed exactly when (a) it stands before the boundary and outside the tick block, and (b) no clause from the boundary on may execute it. The closure follows every arm, the body of every loop and of the tick block, and every procedure performed, transitively, with values ignored. A statement kind the closure has no rule for licenses no claim of the law."

**[INFERENCE] It interprets R6; it does not amend it:**
- (a) is bullet 1 word for word.
- "Or is the tick block" comes from R6's head and trigger sentence.
- (b) is bullet 2 read "by evaluation" and "decided from the text".
- "Exactly when" is the narrowest sufficiency the riders require.

It needs his ruling on the open amended-set row (kind N), and it declines D-18's widening.

**The cost.** Claims like L1 and L2 stay UNGROUNDED. This is R6's "sound, not complete". An author can get the licence back by moving the claim above the first port declaration, at the price of a new law seal and so a new claim seal (`court.py:171-180`). If he wants L1 and L2 licensed, that is B2: an amendment of R6's two bullets, ruled together with port place (b).

**It must state one presupposition and decide nothing beyond it.** The presupposition is that no input is bound before the boundary's position. That rests on `SPEC-15-DRAFT-1.md:179`.

It must not decide:
- **D10 against R6 (finding 24).** Under the open D10, nothing is held in 1a, so licensed claims still read UNGROUNDED there.
- **Read-once ports (finding 6).** If they bound at the run's start, T9's "first 'N'" reading would exempt nothing in a law with a read-once port, and L3 §1 (the twin's P16, claim 0) would need deciding again.
- **The LOG-* refusals (finding 8)**, and a refusal before the first input (`RULINGS.md:166-169`, `308-311`).
- **Port place** (findings 7, 27 and 28; L11). B1 does not depend on it.
- **The wider licence**, and any value-sensitive closure.
- **How GROUNDED and HELD combine** (finding 47).

## 5. What it touches

**Clauses of `SPEC-15-DRAFT-1.md`:**
- §15.0 (28-41): the term "Prefix" (35-36) collides with "PREFIX" claim. A claim in the prefix after a port is not licensed. The boundary would need a term of its own.
- §15.1.3 (52-57).
- §15.1.6 (63-66): L3 is its row.
- §15.3, the read-once bullet (122-124).
- §15.5 (147-167).
- §15.7.1 (178-181): its [ruled: R5] tag overstates.
- §15.7.5 (197-201).
- §15.12.1 to §15.12.6 (287-316), including the open bracket at 305-310.
- §15.13.7 and §15.13.8 (333-357): `Reach` is shared with K̂ (357). [INFERENCE] K̂'s tick-block rows fall inside the closure from the boundary, so a licensed claim is never in them, which matches the R6 settlement.
- §15.13.11 (368-373), not decided here.
- §15.15, rows 400, 402, 388, 392 and 393.

**Ledger and records:**
- `ROUNDS.md:285` (Round D finding 18), `229-238` (C3), `325-326` (T8 and T9), `328-335` (T10.0, T10.1, T10.5, T10.7), `337-338` (T12, T13), `383` (D-18), `444` (port place), `450` (the PREFIX row).
- T9 would need a static form, graded DECLARED, resting on a new obligation: that `Reach` over-approximates for every version-1 statement kind.
- `RULINGS.md` R6 (230-314), the R1 note (55-59), the R12 measure (473: "The licence grants by design"), the claims ruling (348-349), D10 (503-504).
- `FORK.md:22`, `59`.
- `src/orlog/court.py`: GROUNDED is currently the least fixed point over premises on a base of held and ratified claims (288, 308-322, 337). Nothing of R6 is built; no PREFIX appears in `src/` or `tests/`. [PROPOSED] The licence would enter that base. By T8 this never raises a standing, but a licensed claim that cites an unlicensed premise stays UNGROUNDED. The court's own rule list also has an "R6 premises" (`court.py:45`), which clashes with the sheet's R6 the way the two R8s already do.

**Probes and rows:**
- **The twin's probes** (`twin-r7/REPORT.md`):
  - P12 (511-524): licensed under every candidate.
  - P13 (526-535): not licensed under B1; licensed under B2 and B3.
  - P14 (537-549): not licensed; the variant without §4.1 is licensed.
  - P15 (551-558): not licensed under 4a.
  - P16 (560-569): claim 0 licensed and claim 1 not, given binding at the declaration; B3 licenses claim 1, against his cost sentence.
  - P29, P31, P33 (647-706): licensed under 4a. Their "GROUNDED but not HELD" contradicts GROUNDED requiring held (`DISPOSITION.md:81`).
  - P35 (717-721): licensed. P09: not licensed. P18 and P19: B3's dependence on port place.
- **Existing rows and plants:** R6's four acceptance rows; the doppler debate's N-1 rows (`VERDICT.md:155-157`); Round D's PREFIX-TRANSITIVE row (`ADVERSARY-ROUND-D.md:522-523`); `cut0_claims.py`'s L1 case and its "shallow-reach" plant (`60`, `143`, `311`, `346`); `tests/court_monotone.py` and `research/r8_coverage.py` for the witness configuration; `tests/fixtures/court/hoisted_omit.orl`, which stays the open case.
- **[PROPOSED] New rows,** each with its plant:
  - L1 and L2 not licensed (plant: B2's boundary);
  - L3: §1 licensed, §3 not (plant: B3 or B4);
  - L6 not licensed (plants: the vacuous bullets, and `Reach` without a tick-block case);
  - L7 licensed (plant: 4c), or the reverse if he rules 4c;
  - L8 licensed (plant: a licence that never grants). It cannot be observed until finding 24 is ruled;
  - L10 not licensed (plant: K2);
  - L5 gives the same licence verdict on both logs (plant: K3);
  - an unknown statement kind licenses nothing (plant: the empty-set default);
  - an oracle row: on every fixture and log, every 'C' event of a licensed claim comes before the first 'N', or the first 'T' when there is no port. The trace is used only as a check here, never as the rule. This is the independent check the amended set asks for when it says each consumer of `Reach` states its soundness requirement: PREFIX and CUT-0 share `Reach`, so a shared omission cannot be seen by comparing them.

## 6. Falsifier for the recommendation

Any one of these would show it wrong:
1. **Not sound.** A licensed claim has a 'C' event after the first 'N' (or the first 'T') on some log. Or its claim line (evaluations, trues, cost, certified clause's cost) differs between two logs of one law; this is the N-2 test, `VERDICT.md:82-87`.
2. **Not within R6.** It licenses a claim that stands at or after the first port declaration, sits in the tick block, or sits in a procedure that a clause from the boundary on may perform.
3. **Not his reading.** He rules that L1 or L2 must be licensed. That is B2, an amendment, not this interpretation.
4. **Its presupposition breaks.** A ruling on finding 6 binds read-once values before their declaration's position.

## What this packet does not show

Nothing was run or measured. `Reach`'s soundness is DECLARED, for version 0 only. The laws are hand-worked and not compiled; L11 is hypothetical. Whether D-18 came after R6 rests on commit order only. Findings 6, 8 and 24, and the question of a refusal before the first input, all stay open for the owner.
