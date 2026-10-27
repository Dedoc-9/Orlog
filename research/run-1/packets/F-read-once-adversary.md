<!-- Packet F, saved by the draft's author, 2026-10-27: the finding-6 adversary's final report (A against A′), delivered as its message (subagents cannot write files). Copied without change. Its scratch scripts and outputs (f6_cut_analog.py, f6_model_grammar.py and their .out.txt) stayed in the session's scratch folder, outside the repository; their results are quoted in the report. -->
<!-- Paths masked when filed: the session's scratch folder reads {scratch}, the checkout reads {repo}; nothing else changed. -->

# Finding 6, read-once ports: A against A′, an adversary's report

I edited, staged and deleted nothing in Orlog. Running `git status --porcelain=v1 --untracked-files=all` gave the same digest before and after (3ab856e6…). The tree already had uncommitted changes before I started; I left them alone.

**What I ran (MEASURED, once each, from the scratch folder):**
- `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B f6_cut_analog.py {repo}`. It imports `cut0_claims.py`'s own `judge`, `Reach` and `continuation`. Output: `{scratch}\f6-adversary\f6_cut_analog.out.txt`.
- `... python -B f6_model_grammar.py <same path>`. It imports `cut0_session.py`'s `parse_log`, `execute` and `settle`. Output: `{scratch}\f6-adversary\f6_model_grammar.out.txt`.

I did not run either probe's `main`. Labels: RULED, OPEN, INFERENCE, MEASURED, UNEXECUTED.

## 1. Verdict

1. **A fails R6's adopted claim-line sentence.** [INFERENCE]
   - The sentence (RULINGS.md:248-249, adopted sheet text; draft 4 L320-321) says a prefix claim's whole claim line is fixed by the law. T9's falsifier (ROUNDS.md:326) also fires.
   - Take two logs of one law that both load. With the read-once value, a licensed claim's receipt line reads n evaluations, n true. Without it, the line reads 0 of 0.
   - A escapes in two ways only:
     - (i) its read-once NOT-RUN gives the court no claim line, like a load refusal. That is not RO-4, and not C's receipt (C:153, 159-160).
     - (ii) "the first input" moves to the run's start. Then the licence exempts nothing in any law with a read-once port (I-3; C:217-218), so A is caught either way.
   - Reading "fixed" as "fixed whenever the claim is evaluated" contradicts the sentence's own list (evaluations, trues) and T9's wording. It also makes the sentence's premise false under A: the log's completeness acts before the first statement.
2. **A′ survives the whole-log attack.** [INFERENCE]
   - Loading the whole log fixes when the log is checked, not which logs are well formed. The missing record is visible in the log's bytes, so the loader decides it before any statement.
   - Under the current proposals as worded, no read-once-absent closed log loads at all (MEASURED in the model; D's LOG-END wording). That blocks A's NOT-RUN receipt exactly as much as A′'s partial run.
3. **The CUT-0 row holds in computation** (MEASURED on version-0 analogs). It does not hold as the integrator worded it. Four things are missing:
   - a cut defined at a stop that is not a refusal;
   - LOG-OPEN with the record absent (counterexample 2 returns through LOG-OPEN otherwise);
   - the existing "NOT-RUN t, or LOG-OPEN" row scoped to logs that have the record;
   - a tick-block case in CUT-0's own reach.
4. **A′ must stop at the first read-once declaration, never at the declaration of the port the end record names** (case 4b). It must also say when the host learns of a refusal before that declaration (N3).
5. **Neither design is excluded by whole-log loading. A is excluded by adopted R6 text unless the owner amends it.**

## 2. The whole-log analysis

**The texts.**
- Draft 4 §15.5 (SPEC-15-DRAFT-4.md:166-184) [OPEN]:
  - "One record for the read-once ports, then one record per tick", stated unconditionally (L169);
  - end causes `closed` or `not-run <t> INPUT-MISSING <port>` (L172-173);
  - a log with no end record is open (L174);
  - the log is parsed whole before any execution, and a malformed log is refused at load before any execution starts (L175-176).
- Contract draft 0 §2.1-§2.2 (CONTRACT-DRAFT.md:54-65) [OPEN]: the same.
- The amended set's A2 row (ROUNDS.md:442) [OPEN]: a log offered whole is checked whole before execution.

**Can a log with an absent or incomplete read-once record load under the current proposals?** No text makes it so.
- **An incomplete (partial) record has no form anywhere.** [INFERENCE] Records are dense, and a whole record is blocked, never a port (ROUNDS.md:66). In the log, "incomplete" can only mean "absent".
- **Absent and open (header only).**
  - Draft 4 is silent, and its record sentence is unconditional.
  - D leaves it as an open question (D-LOG-refusals.md:220).
  - The model accepts it as LOG-OPEN, with the whole stand-in prefix run, ops 3 [MEASURED]. The model has no read-once ports, though.
- **Absent and closed by a read-once NOT-RUN end record.** Refused:
  - D's proposed LOG-END wording requires the named port to be an each-tick port and says a law with no each-tick port has no `not-run` (D:105, D:208) [OPEN].
  - The model refuses each form I tried with LOG-END [MEASURED]: `end 0 not-run 1 INPUT-MISSING g` (g not an each-tick port), Round D's `end 0 not-run 0 …`, and any `not-run` with no each-tick port.
  - A `once` line is refused LOG-UNKNOWN [MEASURED].
- **So as worded, the read-once NOT-RUN log is malformed for both designs.** [INFERENCE] A's receipt (`ticks 0`, `ops 0`, C:153) needs a log that loads, just as A′'s partial run does. If that log is malformed, both designs collapse into C's option C, a load refusal (C:202-212).

**The distinction, stated without contradiction** (my proposal, OPEN). For a law that declares a read-once port, a log loads only if it is one of these. H is the header, R the read-once record, T a tick record:
- H
- H R T*
- H R T* `end n closed`
- H R T* `end n not-run (n+1) INPUT-MISSING <each-tick port>`
- H `end 0 not-run ‹ro› INPUT-MISSING <read-once port>`

Every other log is refused at load:
- a T, a `closed` end, or a tick `not-run`, with R absent;
- a partial R;
- R followed by a read-once `not-run`;
- a read-once `not-run` that names an each-tick port, or a tick `not-run` that names a read-once port;
- in a law with no read-once port, any R or read-once `not-run`.

Every one of these checks reads only the bytes and the law's port kinds, so it runs before execution. "Parsed whole" and "a malformed log runs nothing" hold unchanged. A′'s stop is read from the loaded log, never discovered during the run. [INFERENCE]

**The cost whole-log loading puts on both designs.** [INFERENCE] A malformed line anywhere, even past where A′ would stop, runs nothing. That is the LOAD-ORDER law (ADVERSARY-ROUND-D.md:264-282). So R6's sentence must already be read over logs that load, under (W), in both designs (I-4). Within that scope A′ satisfies it and A does not.

**The end record.** [INFERENCE] It is `end 0 not-run ‹ro› INPUT-MISSING p`, with the marker's bytes open.
- An unscoped t = n+1 makes the marker 1, and the status line then reads like a NOT-RUN of tick 1 (C §3 B's ambiguity).
- D already scopes t = n+1 to each-tick ports (D:208; I-5).

**A session that ends before its record closes** [INFERENCE from C's RO-2/RO-3 and the model]:
- a failing read-once close gives H + E(p);
- a session still open gives H;
- `end()` before any close is legal in the model and projects to `end 0 closed` [MEASURED]. RO-5 makes that log malformed, so a legal history projects to a log that does not load (N2).

## 3. The cases

**Conventions.**
- Laws use the draft's spellings. All version-1 results are hand-worked [UNEXECUTED].
- E(p) is `end 0 not-run ‹ro› INPUT-MISSING p`. NR(p) is the status NOT-RUN naming read-once port p.
- k is the claim's own counted operations, fixed by the law.
- Real court readings are REFERENCE-ONLY until 1b (15.13.11, RULED F24). "Held" below is CUT-0 and the meet, as a 1a configured row would read it.
- Under A′ the stop emits no `'R'`, so R8 holds every claim and CUT-0 alone withholds.

**Case 1.** The law: §1 claim A (licensed); §2 `Let g be given as an integer.`; §3 `Let x be given each tick as an integer.`; §4 the tick block, `Say x plus g.` g is missing; the log is H + E(g).

| | A | A′ |
|---|---|---|
| status | NR(g) | NR(g) |
| claim A | 0 of 0, UNREACHED (15.13.12) | 1 evaluation, 1 true, cost k |
| events | none | `'C'`(A, true) only; no `'N'`, no `'T'` |
| ticks / ops / output | 0 / 0 / 0 bytes | 0 / k / 0 bytes |
| end record | E(g) | E(g) |
| CUT-0 | no claim has an evaluation; nothing withheld | cut [§2, not begun]; K̂ = §2 to §4 and the tick body, which hold no claim; A held |
| with g supplied | A reads 1 of 1, so its line moves with the log (R6's sentence fails) | A's line is identical |

**Case 2a: a refusal before the declaration.** The law: §1 claim A; §2 `Let z be 1 divided by 0.`; §3 g read once; §4 the tick block.

| | A | A′ |
|---|---|---|
| g missing | NR(g), nothing ran, A 0 of 0. The refusal is masked (C's failure a) | REFUSED DIVISION-BY-ZERO at §2; events `'C'`, `'R'`; ticks 0; A 1 of 1 |
| g supplied | REFUSED at §2, A 1 of 1 | the same as with g missing |
| CUT-0 | — | cut [§2]; K̂ = §3, §4 and the tick body; A held |

- Under A′ the end record is whatever the session wrote: E(g), or a refused session's end record (finding 10). See N3.

**Case 2b: a refusal between the boundary and the declaration.** The law: §1 claim A; §2 an each-tick port x (the boundary); §3 `Let z be 1 divided by 0.`; §4 g read once; §5 the tick block.
- A: as case 2a.
- A′: REFUSED at §3 with either log; A 1 of 1, held.
- **Variant 2b′:** §2 is a read-once port h, supplied, and g is missing.
  - A′ stops at §2, because the record is absent: NR(g), A held, and §3 never runs. With g supplied the run is REFUSED at §3.
  - So A′ also masks a refusal, but only one standing after the first input point. R6's sentence is untouched.

**Case 3: a malformed log with an executable prefix** (CR LF line ends; a tick record without the read-once record; LOAD-ORDER's wrong port count). A and A′ are identical:
- the log is refused at load, with the code finding 8 rules;
- no statement runs; under (W) there is no receipt and no claim line;
- no events, no court reading, no provenance line, and no CUT-0.

**Case 4: two read-once ports** (packet C's counterexample 1). The law: §1 claim A; §2 g read once; §3 claim B; §4 h read once; §5 the tick block.
- **4a, g missing:**
  - A: NR(g), A and B 0 of 0.
  - A′: stops at §2, NR(g); A 1 of 1, held; B 0 of 0, UNREACHED (in K̂ through the rest of the block).
- **4b, g supplied and h missing:**
  - A: NR(h), nothing ran, no `'N'`.
  - A′: the record is absent, so the run stops at §2, g's declaration, and names h. A is held; B is UNREACHED; no `'N'` is emitted.
- A′ is coherent only if the stop is "the first read-once declaration". Stopping at h's declaration would bind g with a value the log does not hold: an invented value (plant).
- g's assigned value reaches no record in either design (finding 54).

**Case 5: no PREFIX claims.** The law: §1 g read once; §2 claim B (reads g); §3 the tick block.
- A and A′ give byte-identical receipts: NR(g), B 0 of 0, ops 0, events 0, output 0, E(g).
- **Variant 5′:** `Say "ready".` before §1.
  - A: output 0.
  - A′: 6 bytes, an `'S'` event, out_0 over them.
  - The claim lines are equal; only A′ hashes the bytes said before the stop.

**Case 6: a claim reachable at or after the boundary** (packet C's counterexample 2). The law: §1 `To check, do the following.`, §1.1 claim A; §2 Perform check; §3 g read once (fixed); §4 Perform check; §5 the tick block, `Say g.` A is not licensed in any variant, so it is UNGROUNDED whatever HELD says.
- A: NR(g); A 0 of 0, UNREACHED.
- A′: NR(g); A 1 of 1, evaluated by §2. With the new row, A is in K̂ through §4: withheld, the row named being "the rest of a block".
  - Plant: reusing the existing NOT-RUN row holds A. MEASURED on the analog V6: the plant holds the claim, and the resumed run evaluates it again after the cut, an E2 violation. The rest of the block withholds it.
- **6b:** check is performed only in the tick body. A is withheld only if CUT-0's reach follows the tick block's body.
  - MEASURED (V6b, with a For as the tick block's stand-in): a reach that adds nothing for the stand-in holds the claim, and the resumed run evaluates it 3 more times.
- **6c:** `If 1 equals 2, perform check.` after the declaration. Withheld, conservatively, because values are ignored (MEASURED, V6c).

**Case 7: a read-once port and a tick block, no other port.** The law: §1 claim A; §2 g read once; §3 the tick block.
- Each design gives what it gives in case 1.
- Under D's present wording and the model, this law has no NOT-RUN end record that loads at all (MEASURED: LOG-END). The session's projection is malformed in both designs until finding 8 scopes "has no not-run" to tick NOT-RUNs.

**New cases that break the proposals as worded.**
- **N1: LOG-OPEN with the record absent** (Round D's F4 asked this; ADVERSARY-ROUND-D.md:135-137). This breaks A′ as worded.
  - Take case 6's law, live, before g's close. The log is H; the model accepts H as LOG-OPEN [MEASURED].
  - A′ runs to §3; A reads 1 of 1.
  - The integrator's row covers only the NOT-RUN stop, so the existing LOG-OPEN row (cut at the tick block's head) holds A. The continuation, once the record arrives, performs check at §4: E2 is violated.
  - Under A: LOG-OPEN, A 0 of 0. A licensed claim then reads 0 of 0 until the record closes, so A's R6 failure is visible live too.
- **N2: `end()` before the read-once close** (both designs). The history is legal in the model and projects to `end 0 closed` [MEASURED]. RO-5 makes that log malformed. A2's move set must refuse the move or read it as a read-once NOT-RUN.
- **N3: when the host learns of a refusal before the first read-once declaration** (A′ only).
  - If the host runs that part at the session's start: RUN-REFUSED before any arrival, and the log is H plus a refused session's end record.
  - If it runs it at the read-once close: the session ends NR(g) while the core reads REFUSED.
  - Both are coherent. Two hosts that choose differently give two input-log-sha256 values for one law and one sequence of arrivals.
  - A pins this in RO-3. A′ must pin it in the A2 row.
- **N4: CUT-0's reach on the tick block** (6b). This is also owed for any version-1 refusal in the prefix.

## 4. The CUT-0 row

**What it must say** [OPEN, for the pin]:
1. **The cut at the stop.** At a read-once NOT-RUN, or at LOG-OPEN with the read-once record absent, the cut is the first read-once declaration's top-level clause, as the only frame, not begun. There is no `'R'` event; the cut is a function of the law and the status.
2. **K̂ by the existing rows.**
   - The frame's own rows add nothing, since a port declaration has no body.
   - "The rest of a block" adds every later top-level clause and everything it may execute: the tick block's body, every procedure performed, transitively, values ignored.
   - Withholdings name "the rest of a block".
3. **Scope the existing row.** "NOT-RUN t, or LOG-OPEN" (draft 4 L434-435; CUT-0.md:76) applies only when the law declares no read-once port or its record is present.
4. **CUT-0's own reach** follows a tick block's body wherever the block is reached and fails closed on unknown kinds. The ruled closure table governs only the licence; CUT-0's reach is separate (L437-439), and the probe's `Reach.stmt` fails open (cut0_claims.py:159-167).

**Does "rest of a block" fit?** [INFERENCE, MEASURED on analogs] It fits in computation, not in premise.
- The continuation from the stop, with the declaration returning and binding an unknown value, is exactly the rest of the top level. S2 already reads values as unknown.
- On the analogs (V1, V4, V6, V6b, V6c), every claim the resumed run evaluated after the cut was in K̂, and K̂ equalled the rest of the block. V6c is conservative.
- But CUT-0 defines the cut at a refusal (CUT-0.md:48-49; L417), and the stop is not a refusal, so item 1 is a new pinned definition.
- T10.1's argument carries over only because binding has no other effect (15.7.1: it counts no operation, emits only `'N'`). It stays DECLARED until version 1 runs.
- The analog's limits: a version-0 refusal at `Let g be 1 divided by d.` stands in for the stop; a For stands in for the tick block; the resumed run uses one bound value, not all values.

**The row's falsifier.** Find a law with a read-once port and a log whose read-once record is absent, in which a claim the row holds is evaluated again by the same law run over any log that supplies the record (any values, any tick records). Plants, each with the case that catches it:
- the NOT-RUN row reused: case 6 / V6;
- a reach without a tick-block case: 6b / V6b;
- an unscoped LOG-OPEN row: N1;
- a stop at the named port's declaration: 4b.

## 5. What each design forces on finding 8

**Both designs:**
- A form that loads for H + E(ro) and for H alone, with the refusals listed in §2.
- D's LOG-END wording scoped to tick NOT-RUNs, both "the port is an each-tick port" and "a law with no each-tick port has no not-run" (D:105, 208).
- t = n+1 for each-tick causes only; the read-once marker distinct; its bytes open.
- The read-once line present exactly when the law declares a read-once port and the record closed (I-6), never "always" (ROUNDS.md:268).
- in_0 over the header alone when the record is absent (L181 assumes the record).
- A receipt for the read-once NOT-RUN: ticks 0, unread count 0, `tick-ops` (finding 31) open.
- The provenance line printed, since R6's trigger is the law's; Round D's row 10 is overruled there (ROUNDS.md:277).
- 15.7.5's NOT-RUN predicate gains the read-once case.
- T6 / row 24, "with no `'T'`, ops is the prefix's count", holds literally in neither design.
- `end()` before the read-once close (N2).

**A:** ops 0, events 0, output 0, out_0 over nothing, trace-head head_0, every claim line 0 of 0. RO-3 fixes when a prefix refusal is learned.

**A′:**
- ops, events, output, out_0 and trace-head are those of the prefix up to the first read-once declaration, all fixed by the law.
- REFUSED whenever that part refuses, whatever the log.
- The end record names the first empty read-once port while the cut is the first read-once declaration (they differ in 4b).
- Header-only LOG-OPEN runs that part.
- N3 must be pinned.

## 6. The narrowest wording, for A′ (every byte form left open) [PROPOSED]

> **RO′-1.** A read-once value reaches the session only as an arrival, judged by the door at once; a refused arrival is never assigned; a retry is a new arrival; neither ends the session.
> **RO′-2.** The read-once ports have one record, filled by assigning accepted arrivals, at most one per port, and closed once before any tick record; it is written whole or not at all. A law with no read-once port is unchanged.
> **RO′-3.** A read-once port binds where its declaration stands. A run executes the top-level clauses before the first read-once declaration whatever the log holds, provided the log loads. If the log holds the read-once record, the run goes on. If it does not, the run stops before the first read-once declaration: NOT-RUN naming the read-once port the end record names (the first empty one in declaration order, checked against the history), or LOG-OPEN if the log has no end record. No `'N'` is emitted, and no value is invented, held over, defaulted or bound from another read-once port.
> **RO′-4.** A refusal before that declaration is REFUSED, whatever the log holds.
> **RO′-5.** That stop is a case of NOT-RUN or LOG-OPEN, not a fifth status. COMPLETED never stands for a law with a read-once port whose log lacks the record.
> **RO′-6 [pinned].** At that stop the cut is the first read-once declaration, a top-level frame not begun; K̂ is the rest of the block from it, the tick block's body and every procedure performed included, transitively, values ignored. The NOT-RUN t / LOG-OPEN row applies only when the record is present or no read-once port is declared.

**It must not decide:**
- the marker, the record's keyword (`once` or `t 0`), t = n+1 beyond each-tick causes, a refused session's end record (finding 10);
- the LOG-* codes and their order, and the load-refusal receipt (finding 8);
- D10 (finding 24) and R1;
- port place. RO′ presupposes top-level read-once declarations, each evaluated once.

**Open beside it, for the A2 row:** when the host runs the part before the declaration (N3), and `end()` before the read-once close (N2).

**For A, if the owner wants its meaning:** it needs either an amendment of R6's adopted sentence and T9, or its read-once NOT-RUN taken out of the court's reading (no claim lines). The second is a different outcome class from RO-4.

## 7. Falsifiers for this verdict

- The owner reads R6's sentence as conditional on the claim being evaluated, or as explanation rather than rule. A then does not fail, and the choice becomes one of preference.
- A ruling, for example R1 b as written ("lives in the input log's header", RULINGS.md:52), makes a log without the read-once record malformed. Neither A's receipt nor A′'s partial run then exists, and the design is C.
- A pair of loading logs of one law under A′ in which a licensed claim's receipt line differs. Executable: enumerate laws with read-once ports, run each with and without the record, and compare the licensed claims' lines.
- A claim RO′-6 holds that the resumed run evaluates again after the stop.
- A port declaration's binding has an effect beyond binding: it counts an operation, can refuse, or a port-place ruling admits a declaration inside a loop or a procedure. T10.1's transfer then fails.
- The owner requires that no output precede the read-once values (the inverse of C's last falsifier, C:350).
