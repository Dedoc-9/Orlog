> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-7, reader 3 of 3: the rulings and cross-document consistency, its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-7 ran
as three readers working at the same time, by the owner's approval (to be recorded in RULINGS.md once the readers have
finished, since reader 3 read that file under a pinned sha256): reader 1 the format and the checker, reader 2 the
protocol and evidence, reader 3 the rulings and cross-document consistency. Each started fresh, had its own scratch
folder and its own letter for findings (V, X, Y), and saw nothing of the others' work. Each was briefed:
- to read draft 7 (sha256 `05010e01…`), SHEET.md (`4d2dca8c…`, Amendment 6 holding the two placeholders of the record
  being remade) and RULINGS.md (`2cb28949…`) as its part required, with the code, the records and the specifications;
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, and change nothing in the repository.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-7, reader 3 of 3: the rulings, and whether the documents agree with each other

## What I read and ran
- **Read whole:** `RULINGS.md` (sha256 `2cb28949…`, checked), `SHEET.md` (`4d2dca8c…`, checked) and `LAW-FORMAT-0-DRAFT-7.md` (`05010e01…`, checked). Also all seven dispositions (REREAD-0 to REREAD-6), with every option text that an "Adopt (x)" adopted.
- **Read in part:** the reports' findings, verdicts and counts; REREAD-6-REPORT whole from its verdict on; earlier drafts where I needed to trace a rule (W5 in drafts 4–6, W14 in draft 1, the heads of drafts 1 and 2, the plant list in draft 5); `LATER.md`.
- **Code read:** the docstrings of `format_check.py`, `plant_reverts.py`, `ref_run.py` (whole) and `ref_run_paths.py`; the checker's plant table near line 1408.
- **Evidence read:** the headers and summary lines of every `evidence/rust-core-*-7*.txt` and of the records the sheet names; the headers of `r6-mutants.txt`, `r2b-twins.txt`, `s3-budgets.txt`, `r5-budgets.txt`, `stress-texts-2.txt` and `vectors-as-integer.{txt,manifest}`.
- **Ran (read-only):**
  - sha256 of every file in rust-core and of the evidence files;
  - two scripts in my scratch folder:
    - `diff_records.py` compares each frozen record with the one before it, row by row;
    - `count_writer_plants.py` rebuilds the 181 distinct laws from the `mode-upper` twins in `r2b-twins.txt` (all 181 match the source sha256s in `r6-mutants.txt`, 298 with multiplicity) and recounts how many laws each writer plant reaches;
  - awk and grep counts.
- HEAD is still `2e9805a`, and src/, tests/, vectors/, research/rust-core and evidence are unmodified. I opened nothing under research/law-sufficiency/ and no other reader's folder.

## What I could not check
- No core exists, so every claim about a core is REASONED.
- I did not run `format_check.py`, `plant_reverts.py`, `ref_run.py` or `ref_run_paths.py`. The first two put research/law-sufficiency on sys.path, and `ref_run` in law mode reads decoder1. Those are readers 1 and 2's ground.
- `r6-reference-3.txt` and the placeholders `<R6REF7_SHA>` and `<R6REF7_NOTE>` do not exist yet.
- The sheet hashes the dispositions cite for earlier versions (`fff19111…`, `b0400caf…`, `fb505ccf…`) cannot be checked: the sheet has no history.
- I did not re-measure Amendment 6's claim that each of the five runner changes fails the new check.
- I only grepped SPEC.md and RUNTIME-SPEC.md.

## Verdict
**Not ready, on the rulings' side: 0 BLOCKER, 4 MAJOR, 12 MINOR.**
- Every ruling is carried in substance, and every frozen count I could recompute is right.
- **But one of his four checks, the recurring-fault stop, carries the L1 failure again.** The sheet says a case is "not covered by his words", while the option text he adopted covers it, and his own point 2 points the other way (Y1).
- **U1's requirement that R2 catch both writer plants can be escaped** through the sheet's rule that a plant may be "declared equivalent" (Y2).
- **Conditions 5 and 6 of his first ruling were never put into the sheet** (Y3).
- **The milestone's acceptance criteria were never updated** for the predictions his later rulings added (Y4).

## Q1. Each ruling against the documents
✓ means carried. A cross means missing or departed from. MEASURED means recounted here.

| ruling / requirement | where it is carried | carried? |
|---|---|---|
| D1 clean room; reading set | draft 7 §0, allow-list (:47-59); `gen_rs.py` is in `src/orlog`, so `src/` covers it | ✓ |
| D2 host binary64 | not stated in draft 7; it reaches the author through RUNTIME-SPEC (`f64`, binary64) | ✓, indirectly |
| D3 full validation; only bytes the core could write | §8, §9 | ✓ |
| D4, D5 (`backend rust-core`) | sheet §4; draft §10 :805 | ✓ |
| Text seal is caller input | §10 :671-673 | ✓ |
| Conditions 1–4 | phase 0; §0; A3's R6 table; A3's R5 | ✓ |
| Condition 5: cache disclosed and verified, fresh and cached builds told apart | nowhere in the sheet | ✗ **Y3** |
| Condition 6: commands, compiler versions, host, seeds, inputs, outputs, plant results | host and seeds yes (A2, A3); compiler version and exact commands of the core no | partial, **Y3** |
| "Passing R1–R8 establishes the milestone only" | §7 :748, never amended for R2b or S1–S4 | **Y4** |
| A1(a) | §3 :192-206 | ✓ |
| A2(a), conditions 1–5 | §0 :53-56; the manifest records command, generator sha and numeric_ref sha | ✓ |
| REREAD-0's accepted corrections | §2, §4, §5, §7, §10, derivation 19 | ✓, but W14(c) departs from "the front end's actual expression-depth limit" (**Y13**) |
| B1 parts 1–6 | §0, §5, §8, §10; A1 (S1–S4) | ✓ |
| B1 corrections 1–3 | §5 :357-379; §10 :772-789; A1 and A2 | ✓ (one stale budget sentence in the sheet, Y10) |
| B1 scope: recursion failure, HostStop docstring, fuel, clause ontology | fuel §5 :378; ontology in LATER.md; **the first two are listed as owed nowhere** | **Y12** |
| C1(a) | A2's table; §10 :761-770 | ✓ |
| C2(a) | A2; the runner's ENV line; S3's sampler | ✓. Two writer additions to the sampler change nothing: max = min(ops, budget), drawn through RESULT texts only. MEASURED: max = ops on all 298 rows |
| C's three qualifications, and the five classes kept apart | §5; §8 and plants; §10; A2's and A3's records | ✓ |
| E1(b) | §8 phase 3; checker | ✓ |
| E2 | A3 | ✓. The exception-type rule was later replaced by K15 without his word (**Y9**) |
| E3(a) | A3, A4; §0; §10 | ✓ |
| J6–J17 (the twelve) | drafts 4 to 7; A3 | ✓ (11 DRAFT rows plus J7; count right) |
| F1(b), F2(a), R2b | §8 (order settled by N1); A4 to A6; A4 | ✓. R2b is not in acceptance (**Y4**) |
| K4–K16 (the thirteen) | draft 5 on; A4 | ✓. K8's `state` kind dropped under his proviso; K9 and K14 confirmed by N3; **K15 never confirmed (Y9)** |
| N1(a), N2(a), N3's three | §8 :618-626; §10 :728-759; W5's row, §10 :796-803, §10 :780-783; A5 | ✓ |
| The L DRAFT rows | draft 6 on; A5 | ✓. The count is wrong (**Y7**) |
| U1, bullets 1–3 (OUT from the writer; R2 compares; R7 gains two plants) | §10 :732-733, word for word; A6 :665-676 | ✓. The name plant's text was substituted (**Y15**) |
| U1, bullet 4 ("R2 must catch both defects") | A6 :668-676 | **escapable: Y2** |
| U1, bullet 5 (provenance recorded) | §0 :103-106; A6 :677-679 | recorded, **with no consequence (Y2)** |
| U2 point 1 | A6 :684-685; ref_run; ref_run_paths | ✓. A residual path classes a setup fault as a reference crash (**Y14**) |
| U2 point 2 | A6 :686-689; docstring :25-28 | ✓. "The experiment" is never defined (**Y5**) |
| U2 point 3 | A6 :690-695 | **Y1** |
| U2: runner faults kept distinct; procedure, not a class | A6 :682-683 | ✓ |
| M3–M10 | draft 7; checker; runner; A6 | ✓. Deviations in M3 (**Y8**), M7 and M9 (**Y15**), and M7's import failure (**Y14**) |

## Q2. His four checks
1. **OUT's provenance and the two writer plants.**
   - Section 10 states U1's sentence word for word.
   - §0 records provenance.
   - A6 names both plants, and its reach claims are right. MEASURED: 154 of 298 laws hold a let with a non-empty name; exactly 3 hold an `(over …)` list whose reversal differs, the 3 A6 names.
   - But an echo core can pass R7 by having its writer plants "declared equivalent", and a provenance reading that finds a copy path decides nothing (Y2).
   - The adopted text "omits a `let`'s name" became "writes a `let`'s name as the empty string". The reach is unchanged: all 154 laws with a let hold a named let (Y15).
2. **The corrected L2/L3 classifications.** Stated as he put them (A6 :684-685), and the runner faults the front-end refusal and the bad budget. One residual: "an import failure is a runner fault" holds only for `ImportError` (Y14).
3. **Whole-experiment interruption and repeat.**
   - Stated as he put it in A6 and in the docstring.
   - Draft 7 states none of U2: it speaks only of K14/N3 interrupts, yet its Q3 asks whether "the draft, the sheet and the runner's docstring" agree.
   - "The experiment" is undefined (Y5).
   - "Handled the same way" stretches N3 (Y6).
4. **The recurring-fault stop.** His words are quoted, but the writer's two readings go beyond them (Y1):
   - "the same" defined as the same line at the same case;
   - a different fault stops too, presented as "not covered by his words".

   Since any runner fault on the repeat now stops the experiment, the definition of "same" changes nothing in the procedure, only the label. The real question, which text governs a different fault, was never put to him.

## Q3. Precedence
- **Each amendment names what it governs** ("Where it and Amendments 1–n differ, it governs"), and its replacements are explicit. That is clear.
- **Not clear:**
  - for a different runner fault on the repeat, U2(2) and option (iii) point opposite ways (Y1);
  - "R1–R8" (his D-ruling; §7) against R2b's "must" and S1's "fails" (Y4);
  - §6 and §7's equivalence allowance against A6's "R2 must catch each" (Y2);
  - K15 against E2's adopted option text (Y9).
- **Stated as settled when he left it open:** the definition of "the same runner fault" (A6 :693) is written as protocol, and only draft 7's Q4 says it is open.
- **Stated as ruled though only implied:** REREAD-1's G rows are called "adopted" (Y13).

## Q4. Counts
**Right (MEASURED):**
- Findings per re-read: F 17, G 19, H 15, J 17, K 16, L 14, M 10, with the severity splits as the dispositions state. The REREAD-0 and REREAD-1 reports' own miscounts are noted in their dispositions.
- REREAD-2's 13 DRAFT items; REREAD-3's twelve; REREAD-4's thirteen minor.
- Plants 88 (evidence: "plants 88 of 88 caught"); fixtures 6 laws plus 3 byte fixtures; reverts 40, of which 6 bite only by a crash; 31 of 31 runner paths; 25 of 25 before.
- R2b: 1,558 twins over 15 kinds and 181 laws.
- R6: 10,000 mutants, 2,500 per operator. Reference classes 2,374 / 6,994 / 632, with crash types summing to 632. Checker 538 accepted, 9,462 refused, 0 crashed.
- Checker verdicts that moved: 1 from A4's record (W5 to W14) and 61 from A5's (all swap mutants, all W5 to W5). Unstated but measured: 40 moved from A3's record to A4's.
- `r6-reference-2.txt` has the same rows as `r6-reference.txt`; the R2b checker records `-6` and `-7` are equal to the first.
- S3: 2,100 values; 237 completed, 61 refused. R5: 254 texts plus 44 that draw none. Stress texts: 14.
- vectors-as-integer: 446 lines (178 and 268), 189 refusals (6, 143 and 40).

**Wrong:**
- "the DRAFT items were twelve" should be thirteen (Y7).
- Section 11's "draft 5's fourteen" lists fifteen (Y11).

## Q5. Earlier text that later rulings overtook, with no note
- RULINGS :317 (E2's traceback rule; Y9).
- RULINGS :385-387 (one runner for every reference run, before R8's exception; Y9).
- RULINGS :444-445 (Y10).
- REREAD-0-DISPOSITION's "Proposed, not adopted".
- SHEET's status line.
- SHEET §3's "15 run-side derivations and the 3 backend-only ones".
- SHEET :33's budget prose (all Y10).

## Findings

### Y1 — MAJOR. The rule that a different runner fault on the repeat also stops is attributed to no ruling, though U2's adopted option text covers it; his point 2 points the other way; the runner's docstring and draft 7 disagree with the sheet
- **The adopted text.** REREAD-6-DISPOSITION :118, option (iii), adopted by "Adopt U2, including the recurring-runner-fault rule" and "Adopt all three points" (RULINGS :452, :466):
  > "after one repetition that ends in a fault again, the experiment stops, and the fault goes to him. No third run".
- **His own words.**
  - RULINGS :472: "If the same runner fault occurs again on the repeat, stop and bring it back for a ruling".
  - :469-471: "Treat a runner fault as an interruption of the entire experiment … repeat the whole experiment."
- **The documents.**
  - SHEET :694: "A different runner fault on the repeat is not covered by his words. It too stops the experiment and goes to him".
  - RULINGS :492-493: "the writer does not read his rule as covering it".
  - ref_run.py :27-28 gives only "If the same runner fault occurs again on the repeat, the experiment stops and goes to the owner". It is silent on a different fault, so read with :26-27 ("repeated whole"), a different fault would be repeated again.
  - Draft 7 states no runner-fault rule at all. Its change table (:961) puts U2 in the docstring and the sheet, but Q3 (:946-947) asks whether "the draft, the sheet and the runner's docstring" agree.
- **Evidence (read).**
  - The case is covered twice, in opposite directions: by (iii)'s "a fault again … No third run", which means stop, and by his point 2, which means repeat.
  - The writer checked his bullets and not the option text he adopted. That is the L1 mechanism (REREAD-5-DISPOSITION :56-58).
  - The sheet's outcome matches (iii), but it is presented as the writer's gap-filling.
  - A6 :693 writes the writer's definition of "the same" (same line at the same case) as protocol.
  - The RUNNER-FAULT line carries no case (ref_run.py :93), so "at the same case" is an extra condition. Because a different fault stops too, it changes nothing in the procedure.
- **Proposal.**
  - Cite (iii)'s text as the source of the different-fault stop.
  - State that his point 2 and his word "the same" pull the other way, and put that to him before any experiment, as B1 correction 3 requires.
  - Mark the definition of "the same" as the writer's reading pending his word.
  - Make the docstring and draft 7 say the same thing, or have draft 7 say that U2 lives only in the sheet.

### Y2 — MAJOR. U1's "R2 must catch both defects" can be escaped: the writer plants may be "declared equivalent", and the provenance reading carries no consequence
- **His words.**
  - RULINGS :461: "R2 must catch both defects through the resulting byte mismatch."
  - :463: "so the evidence establishes that the writer—not an input-byte copy—produced it."
- **The documents.**
  - SHEET :107: "R7 requires each to be caught. One that is not is reported, and measured as equivalent where it is."
  - §7 :748-749: "Every plant caught or declared equivalent by measurement."
  - A6 :676: "A core whose write-back copies its input would let both pass, so R7 fails it."
  - A6 :677-679 and draft 7 :103-106 record OUT's provenance and say nothing of what follows if a copy path is found.
- **Evidence (REASONED).**
  - In an echo core, a plant in the writer changes no observable output on any of the 298 laws. By measurement it is an equivalent mutant, which §6 and §7 accept, so R7 and the milestone hold.
  - A6 does not take the equivalence allowance away from these two plants.
  - Compare exit 5's reading, whose finding has a stated consequence (SHEET :385-386: "If it finds another path … each is CORE-FAULT, and the finding goes to the owner"). OUT's reading has none, and §7 was never given it.
- **Proposal.** In A6 and §7:
  - the two writer plants may not be declared equivalent;
  - a provenance reading that finds any path copying the input into OUT fails R2 and goes to him;
  - that reading is recorded before R2 counts, as exit 5's is.

### Y3 — MAJOR. Conditions 5 and 6 of his first ruling are not in the sheet
- **His words.**
  - RULINGS :35-36: "Cache use must be disclosed and verified. Cached artifacts must be checked against their recorded inputs and outputs. The evidence must distinguish fresh builds from cached runs."
  - :37-38: "Preserve the exact commands, compiler versions, host details, seeds, inputs, outputs, and plant results."
- **The documents.** A grep of SHEET.md for "cache", "compiler" and "rustc version" finds nothing (Appendix A). The only build rule is "each build of the core | 600 seconds" (:125). RULINGS :508-509 lists the conditions under "What follows, as recorded", but that is not the protocol.
- **Evidence (MEASURED by grep).**
  - No amendment requires recording the core's rustc version or build commands, telling fresh builds from cached ones, or checking a cache.
  - Conditions 3 and 4 were carried (Amendment 3); 5 and 6 were not.
- **Proposal.** Add a sheet amendment that states conditions 5 and 6 as evidence-record rules. Do it before the core.

### Y4 — MAJOR. Section 7's acceptance criteria were never updated for the predictions his later rulings added
- **His words.**
  - RULINGS :49: "Passing R1–R8 establishes the milestone only."
  - Later: :354, R2b, "For every fixture, the core must refuse with the correct W code and line"; :286, "For S1, any outcome other than completion … fails."
- **The documents.**
  - SHEET :748: "R1–R8 held, each run twice …".
  - The only amendment to §7 is A3 :390 (exit 5's reading).
  - R2b (A4 :455-460), S1–S4 (A1 :164-171), the do-nothing fixtures (A3) and OUT's provenance reading (A6) never enter §7.
- **Evidence (read).** By the sheet's own words, a core that fails R2b, or crashes on S1 at depth 30,000, could meet §7.
- **Proposal.** Put the acceptance list to him: R1–R8, R2b, S1–S4, the do-nothing fixtures, and both source readings. Amend §7 to match.

### Y5 — MINOR. "The experiment" and "counted" are never defined, though REREAD-6 raised it
- REREAD-6-REPORT :166 names, as a guess left to the harness author: "what 'the experiment' and 'counted' mean in granularity (M2)".
- The M2 row of REREAD-6-DISPOSITION (:81) does not dispose of it.
- SHEET :686-689 says "The whole experiment is then repeated from its start" without saying whether that means one prediction, phase 2 or every prediction.
- **Proposal.** Define the experiment's unit and the unit of counting in A6, before any run.

### Y6 — MINOR. "Handled the same way" stretches N3(3); one interrupt is classified two ways
- SHEET :696-697: "An interruption by any other cause … is handled the same way". It is ambiguous whether that brings in :690-695 (stop on recurrence; "never repeats a second time on its own").
- N3(3) (RULINGS :426-427) puts no limit on repeats.
- ref_run.py :24 and SHEET :617-618 make a `KeyboardInterrupt` in the runner a RUNNER-FAULT. Only the core gets its own process group (A4), so an operator's interrupt is a runner fault if it lands during a reference run, and "any other cause" if it lands during a core run.
- **Proposal.** Say whether the recurrence stop applies to other interruptions, and classify an interrupt the same way whenever it lands.

### Y7 — MINOR. The corrected count of DRAFT items is itself wrong; M2's DRAFT part rode outside his named scope
- RULINGS :391-393 says "the DRAFT items were twelve, L2 and L3 … and L5–L14". Draft 7 :10-12 and REREAD-6-DISPOSITION :61-62 say the same.
- REREAD-5-DISPOSITION :76, L1: "ASK N1. And DRAFT, whatever he rules". Applied at RULINGS :369-371 and SHEET :419-421. That makes thirteen DRAFT items.
- Likewise, the M2 row (REREAD-6-DISPOSITION :81, "And DRAFT: the miscount is corrected in place") was applied (RULINGS :391-393; draft 7 :10-12). It is not one of "the remaining minor dispositions" and not one of U2's three points. RULINGS :450 lists only "DRAFT items for M3–M10".
- **Proposal.** Correct to thirteen, and note which ruling each MAJOR finding's DRAFT part rides on.

### Y8 — MINOR. M3's "As kept" note overclaims
- RULINGS :496: "That changes the checker's verdict, not the format's text." But draft 7 :516 adds a clause to W5's row, tagged [M3], and draft 7's own change table (:962) says "section 8, W5's row (a first arm names too)".
- REREAD-6-REPORT :209 called the row "ambiguous". Settling an ambiguity under a proviso to preserve semantics is the L12/K9 pattern (RULINGS :383-384).
- RULINGS :497 says "the verdicts that move are listed". No list exists; only diffing the records gives the 61 (MEASURED).
- **Proposal.** Correct the note in place, and list the 61, or point to the diff.

### Y9 — MINOR. K15 replaced E2's adopted exception-type rule without his word; the RULINGS notes are stale
- The adopted E2 option (REREAD-3-DISPOSITION :117): "the last line of the traceback names it". RULINGS :317 still states it as current.
- SHEET :506-507 replaced it under "the thirteen minor findings as wording corrections, provided they do not change … evidence classifications".
- His F2 words cover "the now-written R6 reference-running program" (RULINGS :357). Extending the runner "for every reference run of the experiment" (RULINGS :385-387) is the writer's, and A5 :636-641 has since excepted R8, with no note at :385.
- **Proposal.** Add in-place notes, and put K15's extension to the text runs to him.

### Y10 — MINOR. Current-state text that later rulings overtook, with no note
- RULINGS :444-445 still says runner faults are repeated "as his third N3 point says of an interrupt". M2 called that the writer's extension, and U2(2) has since adopted it.
- REREAD-0-DISPOSITION :1-6 still reads "PROPOSED … Proposed, not adopted". Every later disposition has an "Adopted" header.
- SHEET :3-4: "nothing it names is written until the owner accepts it". He accepted it.
- SHEET :51-52: "each of the 15 run-side derivations and the 3 backend-only ones". There are 19 since A-ruling's derivation 19.
- SHEET :33: "at the first statement past the budget". That is prose about the budget, against B1 correction 1 ("Do not redefine the budget in prose").
- **Proposal.** Add in-place notes.

### Y11 — MINOR. Section 11's itemization miscounts
- Draft 7 :860: "draft 5's fourteen". It then lists "the gates' precedence, five" plus 5, 3 and 2, which is 15.
- The first precedence plant is draft 4's "gates' order" (:893). The checker holds only one such plant (evidence: the single "N1 gates: a chain on line 3…"; format_check.py :1408).
- Draft 5 :770 had said "draft 5's fourteen …, and one of draft 4's changed". Draft 7 dropped that clause.
- The total of 88 is right (MEASURED).
- **Proposal.** Restore "and one of draft 4's".

### Y12 — MINOR. B1's scope items are recorded as owed nowhere
- RULINGS :172-173: "Python recursion failure … HostStop docstring: correction proposal".
- SHEET §9 (:771-777) lists the legal.orl note, sema.py:6, the gate, rational wording and version 1, and neither of these. REREAD-1-DISPOSITION :61-69 said they "join the two correction proposals already owed". STATUS.md does not mention RUST-CORE-0 at all.
- **Proposal.** Add both items to §9.

### Y13 — MINOR. W14(c)'s bound departs from his accepted correction, through REREAD-1 rows whose adoption is only implied
- His words, RULINGS :98: "W14 must specify the front end's actual expression-depth limit." The adopted F3 row (REREAD-0-DISPOSITION :19): "W14 bounds what the front end bounds".
- Draft 7 :594 says "So 99 levels suffice", and :596 says "The bound 130 is kept, as safe and not tight", following G9 and G11.
- His only words adopting REREAD-1's DRAFT rows are "Proceed with draft 2 and its checker amendments" (RULINGS :181). Yet G8 is called "adopted" (RULINGS :314; REREAD-4-DISPOSITION :117, in F1(b)'s adopted text).
- **Proposal.** Put to him whether a bound that is not tight satisfies his correction, and record how REREAD-1's rows were adopted.

### Y14 — MINOR. "An import failure is a runner fault" holds only for `ImportError`
- SHEET :701-702: "A mismatch, a file it cannot read, or an import failure is a runner fault". The docstring at :23 says "or not importable".
- ref_run.py :149-152 catches only `ImportError`. Any other exception at import reaches :197-204, giving REFERENCE-EXCEPTION and exit 1, a crash. Twice alike, that is NO-REFERENCE-RESULT on every mutant, which empties R6's compared set without a word (REASONED).
- That is the misclassification U2(1) forbids, in kind. M7's own change of an import failure from NO-REFERENCE-RESULT to RUNNER-FAULT (REREAD-6-REPORT, M7) is also not marked as a classification change.
- **Proposal.** Either catch every exception raised by the import, or narrow the sheet's words to what the code does.

### Y15 — MINOR. Adopted texts applied differently, without a note
- **U1(a)** (REREAD-6-DISPOSITION :101): "the write-back omits a `let`'s name". A6 :670: "writes a `let`'s name as the empty string". The reach is the same 154 laws (MEASURED).
- **M9** (:88): "Amendment 6 names evidence/rust-core-r2b-checker-6.txt". A6 :730-731 names `-7`, so `-6` is still named nowhere, which was M9's own complaint. Its rows are equal to `-7`'s (MEASURED).
- **M7** (:86): "Each a case". The ENV and P checks are folded into the run rows; the 31 rows have no case of their own for them.
- **Proposal.** Note each departure, or apply the adopted text.

### Y16 — MINOR. Draft 7's history leaves out REREAD-0; the F tags collide
- Draft 7 :5-16, "What it applies", starts at REREAD-1. A1(a), A2(a) and REREAD-0's 17 dispositions are absent, and the change tables stop at "from draft 1" (:1039).
- The legend (:39-41) gives *[F1]* and *[F2]* to his rulings. But :598 tags *[F8]* (REREAD-0's finding), and RULINGS uses "F1" for both REREAD-0's BLOCKER (:106) and his ruling (:329).
- **Proposal.** Add REREAD-0 to the history and give the legend separate tags.

## Files created
- `⟦HOME83⟧\AppData\Local\Temp\reread7-3\count_writer_plants.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread7-3\diff_records.py`

## Appendix: the commands and outputs behind the findings
```
sha256sum RULINGS.md SHEET.md DRAFT-7      -> 2cb28949…, 4d2dca8c…, 05010e01… (as briefed)
sha256sum ref_run.py ref_run_paths.py       -> 162d4ec7…, 5f415e84… (= Amendment 6); gen_r6_reference.py eda21973…

count_writer_plants.py (mode-upper twins -> laws):
  sources listed: 298; distinct laws restored: 181; matching a listed source sha256: 181 of 181
  sources holding a let with a non-empty name: 154 of 298; holding any let: 154
  over list of 2+ entries whose reversal differs: 3 ['mutant/s1/0485', 'mutant/s1/2049',
    'probe/twin/probes/n23-notwithstanding-four.orl']

diff_records.py:
  r6-checker -> -5: differing 40 {swap 39, id 1}; -5 -> -6: 1 (05813 W5 line 20 -> W14 line 20);
  -6 -> -7: 61 {swap 61}; join: "61 W5 -> W5"
  r2b-checker -> -6: 0; -6 -> -7: 0; r6-reference -> -2: 0
  r6-checker-7: 538 accepted; r2b-checker-7: 1558 agree
  r6-reference-2 classes: REFERENCE-REFUSED 6994, RESULT 2374, NO-REFERENCE-RESULT 632

s3-budgets.txt: 298 RESULT; 237 COMPLETED, 61 REFUSED; values 2100; "298 rows; 0 with max != ops"
r5-budgets.txt rows: 254; stress-texts-2.txt rows: 14 (8 S1, 3 S2, 3 do-nothing)
vectors-as-integer.txt: 446 lines; x_as_i 178; f_as_i 268; refusals 189 (143 INEXACT, 6 NOT-FINITE, 40 OVERFLOW)
format-7: "plants 88 of 88 caught"; reverts-7: "40 plants and fixtures, 40 changed …, 6 of them only by a crash";
  draft 5's rule: 4 BITES, 3 same; ref-run-paths-7: "31 of 31"
grep -n -i "cache|compiler|rustc version" SHEET.md -> no hit; grep "HostStop" *.md -> RULINGS:173, REREAD-1-DISPOSITION only
grep "N1 gates" format_check.py -> 7 plants (:1424-1449); :1408 comment "E1's two gates in their order"
git rev-parse HEAD -> 2e9805aaa1ceeae0beb443d527680796b66f39c7 (unchanged); no tracked file modified
```
