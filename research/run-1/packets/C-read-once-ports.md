<!-- Packet C, saved by the draft's author, 2026-10-26: a research subagent's final report, delivered as its message (subagents cannot write files). Copied without change. -->

# Decision packet: read-once ports (finding 6 of the twin's review, which blocks the round)

This is research only. I edited, created, built and ran nothing. Line numbers refer to the working tree on top of HEAD 95dac79. Most of `research/run-1/` is untracked there, and `RULINGS.md` is modified against HEAD.

Each statement carries one label:
- **RULED**: the owner's decision, or text he adopted.
- **OPEN**: proposed and not yet ruled.
- **INFERENCE**: my reading.
- **PROPOSED WORDING**: text for him to accept, amend or refuse.

---

## 1. The governing wording

### RULED

- **R5, ruling words** (`research/run-1/RULINGS.md:192`): *"I rule `R5` as written, augmented by your four explicit amendments"*.
- **R5 as written, adopted text** (`RULINGS.md:180-184`):
  - the law line `(port <var> "<name>" <type> each-tick|once)`;
  - "`'N'`, a port's value (u32 var and the value encoding of RUNTIME-SPEC §5)";
  - "Each tick emits `'T'`, then one `'N'` per each-tick port in declaration order, then the body. The read-once ports' `'N'` events come before the first `'T'`."
- **R5 amendment 2** (`RULINGS.md:200-204`). His words for out_0: *"the initial hash of any visual bytes or metadata written before the first tick"*.
- **R5 amendment 3** (`RULINGS.md:205-207`): `ticks <n>` counts the ticks begun.
- **R3** (`RULINGS.md:96`, `111-112`): *"I rule in favor of Option a (The Conversion Rule) for R3."* Also: *"The entrance tool filters all incoming port streams using a restrictive ASCII regular expression sieve."*
- **R4** (`RULINGS.md:151-152`): *"I rule R4 as written in your proposed ruling text: (a) at tick granularity, with automatic continuation deferred until SNAP-1, and the refused branch permanently sealed and queryable."* The adopted text is at `155-159`, ending "until then a refusal ends the session".
- **R6, ruling words** (`RULINGS.md:284-286`): *"I rule Option a (Data, never a channel) for `RUN-1`. The primary principle is unyielding: replayable data is not admissible testimony."*
- **R6, adopted option row** (`RULINGS.md:233`): "in a run with an input log (the law declares a port, or has a tick block), no claim is GROUNDED … except under the licence". The licence is at `239-249`.
- **R6, one seal** (`RULINGS.md:289-290`): *"The court's generated provenance output line must print exactly the `input-log-sha256` value defined in `receipt 1`."*
- **R6, riders** (`RULINGS.md:293-297`): *"Every row testing an ungrounded port violation must run with the witness explicitly configured as agreed"*, and the control *"must return a clean `GROUNDED` standing"*.
- **R6, PREFIX past a refusal** (`RULINGS.md:300-302`): *"A claim wrapped within the `PREFIX` license parameters that evaluated true remains historically held, regardless of whether the execution loop encounters a subsequent transactional refusal downstream."*
- **R1's cost sentence, ruled under R6** (`RULINGS.md:56-58`, `288`): *"Moving a world property out of the law and into a read-once port means the cost of rule a reaches every later claim in the run, stripping them of grounding even if they never touch that property directly."*
- **The claims ruling** (`RULINGS.md:324-325`):
  - *"`HELD` means that every completed evaluation of the claim was true, no evaluation of that claim remains open at the cut, and the continuation at the cut could not evaluate that claim again."*
  - *"admit the meet … pinned to the exact CUT-0 digest, with each withholding identifying its structural row."*
- **R7's build gate** (`RULINGS.md:370-371`): *"no §15 clause built before the required review."*

### OPEN

- **R1 itself is not ruled** (`RULINGS.md:13-16`, `288`). Its option b row reads "the value lives in the input log's header" (`RULINGS.md:49`).
  - INFERENCE: ruling R1 b "as written" could be read as fixing where the read-once record sits. That would decide part of finding 6 by the way.
- **The defaults D1–D10 are sheet items, open** (`SPEC-15-DRAFT-1.md:18`; `RULINGS.md:484-504`). The ones that touch read-once ports:
  - D1, dense records, worded for each-tick ports only;
  - D3, "A run completes when its log ends";
  - D5, binding counts 0;
  - D7, "Randomness is a seeded read-once port";
  - D9, "one JSON object per tick", which is silent on read-once ports;
  - D10, REFERENCE-ONLY until 1b.
- **Draft 1, §15.3** (`SPEC-15-DRAFT-1.md:106-115`). `close()`: "if every each-tick port is filled, the open tick runs at once". The gap itself is stated at `122-124`: "Read-once ports have no event in this table yet. No event fills a read-once port, and nothing says when the prefix runs, or what happens when a read-once value never arrives."
- **Draft 1, §15.5** (`SPEC-15-DRAFT-1.md:152`, `155-156`, `164-165`):
  - "One record for the read-once ports, then one record per tick";
  - the end causes are `closed` or `not-run <t> INPUT-MISSING <port>`;
  - in_0 = SHA-256("orlog-inputs 0" ‖ the header's bytes, with the read-once record).
- **Draft 1, §15.7.1** (`SPEC-15-DRAFT-1.md:178-179`): "A read-once port binds where its declaration stands, emitting its `'N'` event before the first `'T'`", tagged [ruled: R5].
  - INFERENCE: only "before the first `'T'`" is R5. "Where its declaration stands" is contract draft 0 §4.1's (`CONTRACT-DRAFT.md:88-89`). The twin noted the addition (`twin-r7/REPORT.md:237`), but no numbered finding or disposition row covers it. Every alternative below depends on it.
- **Contract draft 0** (`CONTRACT-DRAFT.md`):
  - `57`: "one record for the read-once ports, holding each read-once port's value encoding in declaration order";
  - `45-48`: A2 is defined only for "some each-tick port";
  - `67-68`: the chain;
  - `63-65`: refused at load "before any execution starts".
- **Round D's dispositions in `research/run-1/ROUNDS.md`, all accepted, none ruled:**
  - `268` (F1): "`once` for the read-once record, always written";
  - `271` (F4): "Tick 0 is the read-once record; the session starts only when it closes complete, and otherwise ends `not-run 0`";
  - `272` (F5): "t = n+1, and the port is the first missing in declaration order";
  - `277` (F10): "The court states dependence only when an `'N'` or a `'T'` was emitted".
- **The held decisions list tick 0 as "D-4, … tick 0 for read-once ports", one-way** (`ROUNDS.md:384`).
  - INFERENCE: the amended set (`ROUNDS.md:440-457`) does not name it. Neither does its "identity and bytes" row (`447`), draft 0 or draft 1. The record does not say whether it was dropped or folded in.
- **The adversary's proposals** (`research/run-1/ADVERSARY-ROUND-D.md`):
  - Finding 4 (`127-147`): "Tick 0 is the read-once record. A read-once value that is refused (A1) or missing at the first close (A2) ends the session with `not-run 0`."
  - Finding 14 (`411-413`): read-once ports declared "only by a top-level clause of the prefix".
- **The twin and its disposition:**
  - finding 6 (`twin-r7/REPORT.md:744`), filed RULING under A2 and identity and bytes (`twin-r7/DISPOSITION.md:40`);
  - A7 (`REPORT.md:87-100`) and A9 (`106-115`);
  - P16 (`560-569`): a read-once world property with no tick block;
  - P35 (`717-721`): LOG-OPEN with zero ticks.

### INFERENCE: what the session model implements

`research/run-1/probes/cut0_session.py` does not model read-once ports at all:
- `Session.ports` holds "each-tick ports, in declaration order" (`:82`), and the open tick starts at 1 (`:87`).
- `close` checks only `self.ports` (`:123-139`). `legal_moves` makes arrivals only for those ports (`:161`).
- `port_signature` writes every port as `fix each-tick` (`:193-194`).
- `serialize` writes the header, then `t` lines only (`:203-205`). There is no read-once record.
- `parse_log` accepts only `t` and `end` after the header. A `once` line would be refused LOG-UNKNOWN (`:269`).
- `parse_log` enforces t = len(records)+1 (`:262`), so `end 0 not-run 0 …` would be refused LOG-END. The end record's port must be an each-tick port (`:264`).
- The stand-in prefix is a constant 3 operations that read no input and cannot refuse (`:50`, `:277`).
- The prefix "runs" only inside `execute`, which is called on the whole log at each successful close (`:143`) and at verification.

The manifold adversary says so: "What the model leaves out: read-once ports and their record" (`research/run-1/manifold/ADVERSARY.md:448`). CUT-0 §3's "Does not show" list (`research/run-1/CUT-0.md:293-299`) omits it. The 76,364 exhaustive histories (`CUT-0.md:263-266`) contain no read-once port.

---

## 2. Settled versus open

**RULED: what R5 fixes.**
- The kind `once` is in version 1's law bytes.
- A read-once port's `'N'` carries its variable and its value encoding.
- Every read-once `'N'` comes before the first `'T'`.

**INFERENCE: other rulings that reach read-once ports.**
- R3's door ("all incoming port streams") judges read-once arrivals.
- R6 fires for any law that declares one. R1's cost sentence then applies whether or not R1 is ruled.
- Because the kind exists by R5, finding 6 must be settled whatever R1 becomes.

**OPEN: what R5 does not fix.**
- Where before the first `'T'` the `'N'` stands: at the declaration, at the run's start, or just before `'T'`(1).
- The order of the read-once `'N'` events among themselves.
- What "before the first `'T'`" means when there is no `'T'`: a law with no tick block, NOT-RUN 1, or LOG-OPEN with zero ticks.
- Any session event, the record's bytes, and whether the record is present when no read-once port is declared.
- The rule for a refused or missing value.
- When the prefix runs.

**OPEN: what contract draft 0 proposed.** One read-once record after the header, in declaration order. It is inside in_0, and each port binds at its declaration. It gave no event and no rule for a missing value.

**OPEN: what Round D added.** An always-written `once` line, and tick 0 with `not-run 0`.

**INFERENCE: two accepted Round D dispositions clash in bytes.** `end 0 not-run 0` (`ROUNDS.md:271`) breaks t = n+1 (`ROUNDS.md:272`). The model's parser enforces t = n+1 (`cut0_session.py:262`).

**INFERENCE: what the model implements.** Nothing of read-once ports.

---

## 3. The alternatives

There are three choices underneath:
- how the value enters (an arrival plus an assignment, a new event, or outside the history);
- what a missing value does (a NOT-RUN with nothing run, a NOT-RUN with part of the prefix run, NOT-RUN 1, or a load refusal);
- when the prefix runs.

### A. The read-once record closed before tick 1 ("tick 0": `ROUNDS.md:271`, adversary F4)

**How it works (OPEN).**
- The value is an ordinary `arrive`, judged by the door at once (A2), and then assigned into the read-once record.
- In a law with a read-once port, the first `close()` closes that record.
- If the record is complete, the run starts: the prefix executes, and each `'N'` comes at its declaration.
- If it is not, the session ends NOT-RUN, naming the first empty read-once port in declaration order, and no statement executes. This reads D-4's "the session starts only when it closes complete" as "nothing runs".

**History and dispositions.**
- A refusal followed by a retry works exactly as S1 does for each-tick ports.
- If assignment reuses `assign(i, 0)`, every legality rule carries over unchanged: ASSIGN-AHEAD, ASSIGN-CLOSED, SLOT-FILLED, END-PENDING, END-UNDISPOSED.
- The model's history line `assign %d %d` (`:323-324`) can already write `assign i 0`.
- A new disposition, "assigned to the read-once record", is needed. An assigned value whose record never closes complete reaches no record, which is finding 54 again.

**Input log and chain.**
- The read-once record sits between the header and `t 1`. in_0 already absorbs it (`SPEC-15-DRAFT-1.md:164-165`).
- An open log has an in_0 before the record closes and another after it.
- The end record needs a read-once marker that breaks t = n+1, or a second form.
- OPEN, at the byte level: `once …` against `t 0 …`; whether the line is written when no read-once port is declared; the marker.

**The four outcomes.**
- NOT-RUN gains a case for the read-once record, not a fifth status. T14's case analysis is unchanged.
- The receipt for that case: `ticks 0`, `ops 0`, `events 0`, out_0 over nothing, trace-head = head_0, unread count 0. `tick-ops` is finding 31.
- §15.7.5's "every record before t ran" becomes vacuous, and needs "and no statement ran".

**Session record.** Same three bindings. "g never sent" and "g's valid arrival dropped" give one log and one core but two session records (G7's pattern).

**Court.**
- R6's trigger fires: the law declares a port. The provenance line is printed.
- Every claim has no evaluation, so every claim reads UNREACHED (§15.13.12). CUT-0 withholds nothing.
- INFERENCE: CUT-0's NOT-RUN row puts the cut at "the tick block's head before tick t" (`CUT-0.md:76`; §15.13.8, `SPEC-15-DRAFT-1.md:354-355`). That row must be scoped to t ≥ 1.
- INFERENCE: here the cut stands before the first statement. That is a change to the artifact to be pinned, which is possible while no digest is pinned (`SPEC-15-DRAFT-1.md:13-15`).
- INFERENCE: ROUNDS F10's "only when an `'N'` or a `'T'` was emitted" (`ROUNDS.md:277`) would print no provenance line here. That contradicts R6's ruled trigger, so the ruled trigger governs.

**Failure cases.**
- (a) An input-independent prefix refusal is masked. Take `1. Say 1 divided by 0.`, `2. Let g be given as a fixed.`: with g missing it reads NOT-RUN, not REFUSED. That is the same pattern as an each-tick NOT-RUN t hiding a tick that would have refused.
- (b) A host needs two closes before tick 1 runs. An early `assign(…, 1)` is refused ASSIGN-AHEAD, which fails cleanly.
- (c) Spelled `not-run 0`, it collides with t = n+1. The word "tick" also invites a `'T'`(0), which would put a `'T'` before the read-once `'N'`s and break R5. Plant: an execution that emits `'T'`(0).
- (d) An always-written empty `once` line changes every log of every law. That includes the model's 13 distinct logs, its 16,132 mutation tests (`CUT-0.md:249-250`) and its 25 malformed-log cases.
- (e) PREFIX claims before the declaration get no evaluations when the value is missing.
- (f) The T6 identity "With no `'T'`, `ops` is the prefix's count" (`ROUNDS.md:291`; the model's row at `:415-416`) fails, since ops is 0.

**A′, a variant: the prefix runs up to the first read-once declaration, then stops NOT-RUN.**
- **Counterexample 1.** Two read-once ports g and h, with g supplied and h missing. Under the "whole record blocked" principle (`ROUNDS.md:66`) no read-once record is written. The run therefore stops at g's declaration while the end record names h.
- **Counterexample 2.** Take this law:
  - `1. To check, do the following.`
  - `1.1. We claim that 1 is positive.`
  - `2. Perform check.`
  - `3. Let g be given as a fixed.`
  - `4. Perform check.`
  - a tick block.

  With g missing, the run stops at 3. If CUT-0's NOT-RUN row is reused, `check` is not performed from the tick block, so the claim is held 1 of 1. But the continuation from 3 performs `check` again, which violates E2. A′ therefore needs a new, named CUT-0 row in the pinned digest (claims ruling item 3).
- **Counterexample 3.** For the law in failure case (a), the same log reads REFUSED under A′ and NOT-RUN under A. The receipt cores differ.

### B. A bind event before the first close, checked by tick 1's close

**How it works (OPEN).**
- The value is an `arrive` plus a new `bind(arrival)`, legal until the first close.
- The first `close()` checks the read-once slots, then tick 1's.
- A missing read-once value gives `NOT-RUN 1 INPUT-MISSING <read-once port>`, the only cause form in the draft today, and no read-once record.

**Consequences.**
- History: a new line kind and new refused moves (a bind after the close, a slot already bound). Finding 12's precedence question grows.
- Log: tick numbering is untouched, with no `'T'`(0) temptation and no t = n+1 clash.
- Outcomes: NOT-RUN 1 now means two things. For an each-tick port, the prefix ran. For a read-once port, nothing ran or part of the prefix did. The status line alone cannot tell them apart; only the port's kind, read from the law, can.
- Session record: like A.
- Court: like A if nothing runs. If part of the prefix runs, counterexample 2 above applies directly, because the status is literally NOT-RUN 1 and T10.7's row then holds a claim wrongly.

**Failure case.** P16, a read-once port with no tick block, has no tick-1 close. Either `close()` becomes legal without a tick block (finding 7), or `end()` gains a NOT-RUN ending, which changes what `end` means. A host also cannot run the prefix, say a scene's setup, before the inputs for tick 1 exist. That timing is visible to the host but not in the replay.

### C. The read-once record in the header, given when the session opens

**How it works (OPEN).** The values are fixed when the session or the offline log is created. A run always has them. A missing value means no session (live) or a load refusal (offline). R1 b's "lives in the input log's header" (`RULINGS.md:49`) reads this way.

**Consequences.**
- Outcomes: the four outcomes are untouched, there is no partial-prefix case, and T10.7 is unchanged.
- History: unless the opening is itself a recorded event, a door refusal of a read-once value is in no history. That breaks the A2 row "every arrival in the history" (`ROUNDS.md:442`).
- Session record: the source is lost.
  - Counterexample: alice's `9.8` and mallory's `9.8` give one core and one session record, so the G5 property (`CUT-0.md:233-234`) fails for read-once ports.
  - Adding an opening event collapses C into A with different bytes.
- Load refusals: a missing value becomes a LOG-* condition, with the receipt-or-none question attached. That decides part of finding 8.
- Live hosts: a session "waiting for its seed" (adversary F4) has no log.

**Court.**
- R6 and R1's cost are unchanged only if the `'N'` stays at the declaration.
- INFERENCE: if "in the header" were read as binding at the run's start, T9's "first input = the first `'N'`" (`ROUNDS.md:326`) would precede every statement. The licence would then exempt nothing in any law with a read-once port, widening R1's "every later claim" to every claim. That decides PREFIX (findings 3–5).
- INFERENCE: his "every later claim" presupposes claims earlier than the port, which tells against binding at the start.

---

## 4. The narrowest recommended decision: A's meaning, with every byte left open

The text below would fill the A2 and identity-and-bytes rows for read-once ports.

> **PROPOSED WORDING (OPEN until ruled):**
> - **RO-1.** A value for a read-once port reaches the session only as an arrival: `arrive`, judged by the door at once (R3). A refused arrival is never assigned, a retry is a new arrival, and neither ends the session.
> - **RO-2.** The read-once ports have one record. The host fills it by assigning accepted arrivals, at most one per port, and closes it once, before any tick record. In a law that declares a read-once port, the first close closes that record. In a law that declares none, nothing changes.
> - **RO-3.** The run starts at that close, and only if every read-once port is filled: the prefix executes from its first statement, each port binding where §15.7.1 places it. That close is when the session learns of a refusal in the prefix (RUN-REFUSED from then on). If a read-once port is empty, no statement executes, and the session ends NOT-RUN, naming the first empty read-once port in declaration order. Nothing is invented, held over or defaulted, and an accepted value for another read-once port is not used.
> - **RO-4.** That ending is a case of NOT-RUN, not a fifth status. Its end record tells it apart from every tick's.
> - **RO-5.** COMPLETED never stands for a law with a read-once port whose log has no read-once record.
> - **RO-6.** At that NOT-RUN no claim has an evaluation, and every claim reads UNREACHED. CUT-0's NOT-RUN row (the tick block's head) is for a tick t ≥ 1. [pinned: to enter the CUT-0 digest before it is pinned.]

**Marked OPEN, at the byte level.**
- `assign(i, 0)` against a distinct event.
- The name "tick 0".
- `once …` against `t 0 …`.
- An empty line when no read-once port is declared. INFERENCE: "always" is not narrow, by failure case (d).
- The NOT-RUN marker and how it meets t = n+1 (finding 35).

**Also OPEN.**
- Whether `end()` before the read-once close is a refused move or reads NOT-RUN (A2's move set).
- When the prefix runs in a law with no read-once port.
  - The model runs it at the first tick's close (`:143`). Running it at the session's start is the other reading.
  - INFERENCE: the two differ only when the prefix refuses: tick 1's record is present but unread in one, absent in the other. That changes the unread count and `input-log-sha256`.
  - I would leave this to the A2 row.

**What the decision must not decide, and where it touches each.**
- **D10 against R6 (finding 24).** Not decided. The court rows for read-once laws (R1's cost, PREFIX before the declaration) inherit the conflict and cannot pass non-vacuously in 1a until it is ruled.
- **PREFIX (findings 3–5).** Not decided. It touches PREFIX only by keeping §15.7.1's binding place. That place is contract draft 0's, carried under an [R5] tag that should be retagged. Moving it would change PREFIX (section 3, C).
- **The LOG-* conditions (finding 8).** Not decided. Unavoidably, the loader must refuse:
  - a tick record before a required read-once record;
  - an `end … closed` with that record absent (RO-5's loader branch);
  - a read-once record in a law with no read-once port, if the bytes say "only when declared";
  - a read-once NOT-RUN marker naming an each-tick port, and `not-run t≥1` naming a read-once port.

  The codes, their order and receipt-or-none belong to finding 8.

**Also touched.**
- Finding 7 (P16, a law with no tick block).
- Finding 10 (a prefix refusal at the read-once close is a new place where it arises).
- Finding 54.
- Finding 12 (an assignment of the wrong kind against ASSIGN-AHEAD).
- R2's place rule. RO assumes a top-level declaration evaluated exactly once, so if R2's place changes, this reopens.
- The later "optional port" (`ROUNDS.md:284`), which RO does not foreclose.

---

## 5. What a ruling affects

**Clauses of `SPEC-15-DRAFT-1.md`.**
- §15.0, the terms "port", "session" and "input log", plus "read-once record" (`32-41`).
- §15.1.3, which assumes top-level read-once ports (`52-57`).
- §15.1.6, only if R1 b is ruled (`63-66`).
- §15.2, read-once arrivals at the door.
- §15.3: the table (`109-115`); the gap bullet (`122-124`); "no value invented" (`125-126`); retry (`127-128`); a door refusal (`129`); R4 (`130-132`).
- §15.4, the history and HISTORY-MISMATCH (`134-145`).
- §15.5: `152`, `155-157`, `158-163` (finding 8), `164-167`.
- §15.6 (`171-174`).
- §15.7.1, including the retag (`178-181`).
- §15.7.4 (`195-196`).
- §15.7.5 (`197-201`).
- §15.7.6, out_0 when nothing ran.
- §15.8: `ticks` excludes the read-once record, and `tick-ops` (`214-229`).
- §15.9: there is no `'T'`(0).
- §15.10: no tick line for the record, and the identities (`257-270`).
- §15.11 (`276-280`).
- §15.12.1, 15.12.3 and 15.12.4 (touched only, `287-303`).
- §15.13.8 and 15.13.9 (`354-360`), 15.13.11 (D10) and 15.13.12.
- §15.15, rows `392-393` and `395`.

**Ledger rows in `ROUNDS.md`.**
- T1 (`318`), T6 together with F24 (`323`, `291`), T7 (`324`), T9 (`326`), T10.0 (`328`), T10.7 (`335`), T14 (`339`), T15 (`340`).
- The amended set's A2, session record and identity-and-bytes rows (`442`, `445`, `447`).
- D-4 (`384`).
- Round D's F1, F4, F5, F10, F14, F17 and F18 (`268-285`).

**Elsewhere.**
- `twin-r7/DISPOSITION.md` rows 6, 7, 8, 10, 12, 31, 35, 36, 54 and 56.
- In `RULINGS.md`: R1, R2's places, D1, D3, D5, D7, D9 and D10.
- Under R7, the ruling triggers a re-read of A_r over all of these.

**Regression cases a session model would need.** All are UNEXECUTED, with expected outcomes under the recommendation, DECLARED, and every byte form open.

1. **A law with only read-once ports.**
   - With a tick block: arrive g, assign, close (the read-once record), close (tick 1), end. Expected: COMPLETED, and the `'N'` for g comes before `'T'`(1, c).
   - Without a tick block (P16): read-once close, then end. Expected: COMPLETED, `ticks 0`, no `'T'`. Depends on finding 7.
   - `end()` with nothing supplied: must not read COMPLETED. Plant: the loader accepts `end 0 closed` with no read-once record.
2. **Read-once and each-tick ports together.**
   - An `assign(…, 1)` before the read-once close is refused ASSIGN-AHEAD.
   - A complete read-once record with the tick-1 port missing gives NOT-RUN 1 naming the each-tick port. The prefix ran, and the read-once record is in the log.
   - An assignment of the wrong kind, either way, is refused. The code is open.
3. **A read-once value refused by the door, then retried.**
   - `0.1` is refused INPUT-GRID, then `0.5` is accepted, assigned and closed.
   - The log is as if no refusal had happened, and the refusal stays in the history.
   - Against a history without the refusal: one core, two session records.
   - Assigning the refused arrival is refused ASSIGN-REFUSED.
4. **A read-once value missing at the first close.**
   - Expected: NOT-RUN naming g; ops, events and output all 0; every claim UNREACHED; the provenance line printed.
   - Plants: a default or held value; a writer that names tick 1; a run of part of the prefix; a cut at the tick block's head.
5. **Two read-once ports, g given and h missing.** The NOT-RUN names h, and no `'N'` is emitted for g.
6. **The procedure case** (counterexample 2 in section 3, A′). The claim is UNREACHED, never held.
7. **A prefix refusal before the declaration.** With g given: REFUSED, then RUN-REFUSED. With g missing: NOT-RUN. This row pins A against A′.
8. **An open log without the read-once record.** LOG-OPEN, nothing run.
9. **An open log with the read-once record only.** LOG-OPEN with the prefix run (P35's analogue).
10. **A read-once arrival after the record has closed.** Assigning it is refused ASSIGN-CLOSED, and it must be dropped before `end` (END-UNDISPOSED).
11. **A filled read-once slot, then `end()`.** Refused END-PENDING.
12. **No read-once port.** Every existing case and domain of `cut0_session.py` stays byte-identical, if the empty line is not written.
13. **Log grammar.** The four refusals listed in section 4, with codes open.
14. **Projection.**
    - HISTORY-MISMATCH for the read-once record.
    - Two accepted read-once arrivals, each assigned in a different history: two logs.
    - Alice against mallory: one core, two session records.
15. **Court** (blocked by finding 24 in 1a).
    - A claim after the declaration that never reads g: UNGROUNDED, with the witness agreed, beside a GROUNDED control.
    - A prefix claim before the declaration: GROUNDED.

---

## 6. A falsifier for the recommendation

Any one of these refutes RO-1 to RO-6:

- A legal history whose projection's read-once record holds a value that is not the door's value of an assigned, accepted arrival.
- Two conforming executions that differ over a log with an incomplete read-once record. For example, one runs part of the prefix.
- A claim with a completed evaluation in a read-once NOT-RUN run.
- A law with no read-once port whose log, history or outcome changes under the rule.
- An outcome under the rule that satisfies two status predicates, or none.
- A law the rulings accept that the rule leaves undefined. For example, if R2's place rule were to admit a declaration reached twice.
- A use case the owner requires that needs the prefix's output before every read-once value exists, which "nothing runs" forbids. For example, a live host showing the scene before its seed arrives. That would show A′'s meaning is wanted, along with its new CUT-0 row.
