> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-4: the independent re-read of LAW-FORMAT-0 draft 4, its checker and SHEET Amendment 3, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document, the checker,
the sheet or the files it fixes. Its brief:
- read draft 4 (sha256 `0978c7f1…`) whole, appendix A included, and draft 3 for the changes; RULINGS.md's B1,
  REREAD-2 and REREAD-3 sections, the "As kept" notes open to challenge; SHEET.md with Amendments 1-3 (`fff19111…`);
  REREAD-3's report and dispositions; `format_check.py`, `plant_reverts.py`, `run_format.py` and their records; the
  files Amendment 3 fixes and their generators; SPEC.md, RUNTIME-SPEC.md, and `src/orlog/` for faithfulness;
- never open, read, list or grep anything under `research/law-sufficiency/` (it could run the scripts that import from
  there, and compute decoder1's sha256);
- write only under its own scratch folder in the system's temp directory, and change nothing in the repository;
- answer draft 4's Q1-Q6 with evidence, covering the owner's rulings E1-E3, the twelve dispositions J6-J17 and his
  four B1 requirements, and list its findings, K1 onward, by severity.

Its report follows, unedited, taken from its own transcript rather than retyped. Its section "What I could not check"
discloses two slips touching `research/law-sufficiency/` (names only; no file opened); see REREAD-4-DISPOSITION.md.

---

# REREAD-4: an independent re-read of LAW-FORMAT-0 draft 4, its checker, and SHEET Amendment 3 (2026-10-30)

LAW-FORMAT-0-DRAFT-4.md read: sha256 `0978c7f180ea76573061a37e85c7093d4a48752c150d22f6b48e2afe05dd3815`. SHEET.md read: sha256 `fff191114ecff0fc57e4c39b3fa789ded2fa685b676e553fea05f1c3adec614f`. Both match the brief. HEAD was `2e9805aaa1ceeae0beb443d527680796b66f39c7` at the start and is still that at the end. I changed no file in the repository.

## What I read and ran

**Read whole:**
- LAW-FORMAT-0-DRAFT-4.md, appendix A included, and a `diff` against draft 3.
- RULINGS.md, all of it.
- SHEET.md, Amendments 1–3 included.
- REREAD-3-DISPOSITION.md; REREAD-3-REPORT.md, J1–J7 in full and the rest skimmed.
- `format_check.py` (sha256 `b39bbd05…`), `plant_reverts.py`, `run_format.py`.
- `gen_r5_budgets.py`, `gen_r6_mutants.py`, `gen_stress_texts.py`, `gen_s3_budgets.py`, `gen_worked.py`.
- `evidence/rust-core-format-4.txt` and `-4-reverts.txt`; the headers of `r6-mutants.txt` and `rust-core-r6-checker.txt`.
- `src/orlog/interp.py`, `sema.py` and `front.py`; `arbiter.py` at its run and reference parts.
- RUNTIME-SPEC.md whole; SPEC.md §3–§9 and the items cited.

**Ran**, all from the repository root as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B …`, CPython 3.14.5, Windows 11, default recursion limit 1,000. Commands and outputs are in the appendix.
- `format_check.py`: equal to the evidence's body byte for byte (CR stripped). 304 of 304 laws, 64 of 64 plants. **MEASURED.**
- `plant_reverts.py`: equal to its evidence byte for byte, `PLANT REVERTS HELD`. **MEASURED.**
- Every generator, into my scratch folder, compared byte for byte with the repository (**MEASURED**):

  | file | regenerated | sha256 matches the sheet |
  |---|---|---|
  | `r5-budgets.txt` | yes | yes |
  | `r6-mutants.txt` | yes | yes |
  | `rust-core-r6-checker.txt` (`--checker`) | yes | yes |
  | `stress-texts.txt` (and `--write`) | yes | yes |
  | `s3-budgets.txt` | yes | yes |

- `sha256sum research/law-sufficiency/decoder1.py` gives `3584f565…ab877`, equal to the sheet.
- My own scripts:
  - odd cases through `format_check.read`;
  - two in-memory variants of the checker (a "whole tree" reading, and "no chain gate, no crash");
  - the reference's budget stop against section 5's positions;
  - appendix A reproduced without `gen_worked.py`, which writes into the repository;
  - S2 timing, and the exception type of S1's reference crashes;
  - 100,000-long chains through the checker.

## What I could not check

- **decoder1's behaviour.** I opened nothing under `research/law-sufficiency/`. So I cannot say:
  - whether decoder1 refuses malformed bytes with a `DecodeError` (or whether such a class exists);
  - whether it accepts non-canonical forms;
  - whether it crashes with other exceptions on mutants;
  - whether it changes the recursion limit.

  R6's power to falsify an accepting core depends on all of these (K3).
- **Any core.** None exists. Rust's behaviour on overflow and abort is documented, not measured.
- **Linux.**
- **The full R5 and R6 reference runs.** Not run; R6 needs decoder1.
- **R8 through the arbiter.** Not run.

**Two slips, disclosed:**
- My first `git status --porcelain=v2 --untracked-files=all` printed the names of the untracked files under `research/law-sufficiency/` (names only).
- One `find . -name __pycache__ -not -path "./research/law-sufficiency/*"` descended into that folder. Its filter printed nothing from it.

No file there was opened, read or grepped.

## Verdict

**Not ready.** Count: 0 BLOCKER, 3 MAJOR (K1–K3), 13 MINOR (K4–K16), 16 in all.

- **The format** should not go to the clean-room author until K1, and preferably K4, are settled. Both are one or two sentences, or one ruling.
- **The protocol** should not be used until K2 and K3 are fixed.

**What holds:**
- **E1's depth gate**, as ruled.
- **The chain gate,** as a literal reading of his fifth point.
- **Twelve dispositions.** Each is applied, with residuals named.
- **Every file Amendment 3 fixes** reproduces byte for byte.
- **The budget** equals the reference at every position, J15's sentence included: 0 mismatches.
- **No limit on chains.**
- **Exit 5 and the Windows rule** are no broader than his words.

## Q1. E1's gates

**W14(a) and (b): a bounded, non-recursive pass that does not depend on the walk.** Yes.
- **Where.** Draft4:556-560. In the checker (`format_check.py:555-570`), one loop computes `depth[k] = depth[p] + 1` and the loop count, and returns before any sibling table or walk.
- **Deep trees (MEASURED).** At the default recursion limit, nested If-block trees are refused W14 line 27, in time linear in depth:

  | depth | time |
  |---|---|
  | 30,000 | 0.60 s |
  | 100,000 | 1.67 s |
  | 300,000 | 5.35 s |

- **Without the gate,** both 30,000-deep plants raise `RecursionError` (the reverts evidence, reproduced).
- **A law that fails the gate reaches no walk.** Confirmed. The gate also wins over an earlier-line phase-5 failure: an undeclared variable on line 3 and a clause 25 deep on line 28 give W14 line 28 (D5).

**Is a chain failing W4 "likewise rejected before traversal"?** Yes: phase 4 (`format_check.py:625-639`). Measured (D1–D4):

| law | reported |
|---|---|
| an inline `if` in an arm (which also fails W7) whose own arm names 99 | W4 line 3 |
| a `(block 99)` under an arm whose clause exists | W4 line 3 |
| an else naming clause 0 | W4 line 3 |
| `(perform 99)` on line 3, then a chain naming 99 on line 4 | W4 line 4: the gate wins over the earlier phase-5 W4 |

**Gates against earlier phases.** A W1–W3 failure wins even on a later line. W14(c) on line 28 is reported over W14(a) on line 27, and W2 on line 28 over W14(a) on line 27 (D6, D7). This is what "each phase runs only when every earlier phase has passed" says.

**Is the writer's reading the right one?** It is the most literal reading, and the only one consistent with his fourth point, "the subsequent walk covers the entire tree". A chain that is merely skipped would truncate the walk. Draft 4 does not overreach on the gate's scope. Two points still need his confirmation (K5):
- **The gates' order is the writer's.** Depth before chain is the writer's choice; either order is "before traversal".
- **G8's skip keeps J1's mechanism.** The skip of a W5-failing chain's blocks still produces J1's cross-line effect. MEASURED: a sound outer inline else on line 3 is reported W8 because an inner chain on line 4 fails W5.

**Once the gates pass, does the walk cover the whole tree?** No (K1). A third kind of part is never entered, which the document does not list: the children of a clause that has children and no body. Two readings give different (line, W).

**Does anything still claim that truncating a walk preserves numbering?** No, not in draft 4: the withdrawal is explicit (draft4:577-580). Only a stale checker comment remains (K16).

**Can phases 3–5 be read two ways?**
- **The gates' precedence:** no. It is stated clearly (draft4:548-549, 582-585).
- **What phase 5 walks and checks:** yes. K1 (the unlisted skip) and K4 (W6 or W7 for an inline `define`).

**Does the checker do exactly what the document says?** Except for three things:
- K1: it follows section 7's definition of the walk, not the sentence "Only two parts are not entered".
- K4: it reports W7, where the least-W rule gives W6.
- W11 is judged against the procedures the walk has met (`L.procs`, :949), not against procedure clauses as the document says (K1's case C1).

It handled every 5,000-digit number in twelve more positions without a crash, and its int-string limit was 4,300 before and after.

## Q2. The twelve dispositions

| | disposition | draft 4 | checker | Amendment 3 | plant: does it bite? | residual |
|---|---|---|---|---|---|---|
| J6 | the list of stores; the sentence's end | yes, :71-74 and :656-658 | n/a | n/a | n/a | K8: no exhaustion kind for some stores |
| J7 | by E1's fifth point: the chain gate | yes, phase 4 and W4's row | yes, :625-639 | n/a | W4 line 4. Bites only against draft 3's skip (W8 line 3). Without the gate and without a crash, it is also W4 line 4 | K5, K6 |
| J8 | a literal judged under line 2 | yes, section 6 and W6 | yes (unchanged) | n/a | W6 line 3; undone, W6 line 4: bites | none |
| J9 | lift the int-string limit inside `read` | yes, section 11 | yes, :452-462 | n/a | 4 plants; undone, `ValueError`: bites | none (12 more positions tested) |
| J10 | the closure by search; sibling positions once | the change table only | yes, :571-574 and :1019-1036 | n/a | no plant (none proposed) | K16 |
| J11 | a byte fixture and its twin | yes | yes | n/a | both bite | none |
| J12 | one taxonomy | yes, section 10 | n/a | yes | n/a | K9, K10 |
| J13 | a fresh empty folder per run | n/a | n/a | yes | n/a | K11 |
| J14 | R8 in the arbiter's process; `platform.platform()` per run; s3 kept | n/a | n/a | yes | n/a | K12 |
| J15 | the inline check sentence; fixtures; an R7 plant | yes, :336-338 | n/a | yes | fixtures held to the reference again | K2 |
| J16 | the law's bytes defined by this document | yes, :53-54 | n/a | n/a | n/a | none |
| J17 | stdout; LAW equal to an output path | yes, :613, :644, :653 | n/a | not carried into the sheet | n/a | K10 |

**J10 timings (MEASURED, one run each, software timings):**

| input | this checker | REREAD-3 measured |
|---|---|---|
| 400 / 800 / 1,600 / 3,200 defines, each overriding the one before | 0.01 / 0.04 / 0.13 / 0.48 s | 0.06 / 0.44 / 3.42 / 26.5 s |
| 10k / 20k / 40k top-level inline Ifs | 0.25 / 0.55 / 0.94 s | 0.39 / 1.15 / 3.80 s (fixed by J10) |

**Are the reverts faithful?**
- **Faithful:**
  - the capped walk (`depth[j] > 25`), which reproduces REREAD-3's draft-3 results exactly;
  - the whole tree walked;
  - draft 3's skip of a W4-failing chain;
  - J8's, J9's and J11's undoings.
- **Not faithful:** "E1 undone: no chain gate, nothing skipped". It "bites" only because the reverted checker crashes with `KeyError` on `C[99]`. A version without the gate that does not crash gives the same W4 line 4 on J7's law (K6).

## Q3. E2 and E3

**Are the files fixed, and do they reproduce? (MEASURED)**

| file | sha256 | contents |
|---|---|---|
| `r5-budgets.txt` | `27b38350…` | 254 texts with a B, 44 with none |
| `r6-mutants.txt` | `a8f704fb…` | 17,155,925 bytes; 10,000 distinct mutants, none a source |
| `evidence/rust-core-r6-checker.txt` | `4365d26b…` | accepted 538, crashed 0 |
| `stress-texts.txt` | `d698ed6e…` | 14 texts; `--write` gives each text and its law bytes equal to the manifest |
| `s3-budgets.txt` | `86f3a7b0…` | RESULT 298, 2,100 values |

- R6's redraws: flip 34, truncate 413, swap 30,644, id 11,239.
- **Observed, not findings:**
  - The 298 sources are only 182 distinct law byte strings.
  - S2 at 24 runs in the reference in about 21 s of wall time, twice under each budget: STOPPED 25,165,823 under B = 10, COMPLETED 25,165,824 with none. OBSERVED on this host only.
  - S1 at 600 and 3,000: the reference exits 1 with type `RecursionError`, twice each. MEASURED.

**What a harness would still have to decide:**
- How R6's reference is run (K3): decoder1's entry point, the law seal given to `Interp`, and how a `DecodeError` is reported. That boundary decides REFERENCE-REFUSED against NO-REFERENCE-RESULT (MEASURED: an uncaught `DecodeError` ends a process with exit 1 and the type `module.DecodeError`, which is a crash under Amendment 3's rule).
- What a "message" is (K3).
- Who judges "an accepted non-canonical form" (K3).
- Which prediction catches R7's decoder plant (K2).
- Where LAW lives under the fresh-folder rule, and the working directory (K11).
- Edge cases of the exception-type rule (K15).
- The core's conditions in R8 (K12).
- Who reads exit 5 in the source (K13).

**Are the four kinds kept apart?** Yes, in the tables. I found no path by which one becomes a successful comparison. The only conversion path is the unwritten R6 runner (K3): it can turn a would-be falsifier into stress evidence.

**Exit 5 and the Windows rule.** Both are as narrow as his words. Draft 4 adds three conservative extensions:
- another system's evidence needs his ruling;
- an exit 5 found off a fallible allocation becomes CORE-FAULT;
- EXTERNAL-TERMINATION only at the 60-second kill (K14).

I found no overpromise.

## Q4. The B1 requirements

- **Termination:** unchanged and right. I re-derived P < Q for performs and last-define order for rules. Reasoned.
- **The budget (MEASURED).** I ran 13 laws at every B from 0 to ops + 1, comparing the reference's stop with the first of section 5's positions where ops > B. Result: **0 mismatches.**
  - J15's sentence holds: `If 1 plus 1 = 2, say 5.` stops after 3 operations with 0 events for B = 0–2.
  - So do the inline otherwise, an absorbed arm's and an absorbed else's inline statement, and stops inside While, For and Perform bodies.
  - A rule use followed by a define, and do-nothing tails (a procedure, a decimals clause), stop at the check before the do-nothing clause.
- **Explicit stacks:** no limit anywhere. The checker accepts 100,000-long perform and rule chains (2.39 s and 2.33 s) at limit 1,000, and writes them back exactly. MEASURED.
- **Detected exhaustion, external termination and core faults:** kept apart, with small gaps (K8, K10, K14).
- **Did draft 4 break any?** No.

## Q5. The checker against sections 2–4 and 8

- **Phases 1–2:** as written, measured by the 64 plants and by D6 and D7.
- **Phase 3:** as written.
- **Phase 4:** as written, inline `if` forms included.
- **Phase 5, W by W:**
  - W4, W8, W9, W10, W12, W13: as written.
  - W5 and W7: as written for G8's two skips. A third skip is unwritten (K1).
  - W6: not checked on a W7-failing inline `define`, `procedure` or `decimals` (K4).
  - W11: requires the procedure to have been met by the walk (K1, case C1).

## Q6. What a clean-room author would still have to guess

1. Whether the children of a clause with children and no body are walked, numbered and checked (K1).
2. W6 or W7 for an inline `define`, `procedure` or `decimals` (K4).
3. Which RESOURCE-EXHAUSTED kind to print for variables, claim accumulators, cost counters and event payloads (K8).
4. What "result" means for UNSTABLE-CORE outside the compared classes (K9).
5. What counts, beyond `try_reserve`, as "the like" (`Box::new`, `format!`, BTreeMap and `fs::read` are infallible) (K8).

---

## Findings

### K1: MAJOR. The walk skips a third kind of part, which section 7 and phase 5 say it does not, and the two readings report different (line, W)

**Document:**
- draft4:438-442: *"The walk covers the whole tree … Only two parts are not entered (G8): the blocks of an If chain that fails W5, and an inline statement that fails W7."*
- draft4:566-573, phase 5: *"The walk covers the whole tree (section 7)."*
- But the walk's own definition (draft4:418-423) enters children only *"for a While, a For or a procedure"* and through a block.
- W11 (draft4:472): *"names a `procedure` clause whose id is less than …"*.

**Code:** `format_check.py:1009-1010` walks only those; `:949` uses `L.procs`, the procedures the walk has met.

**Evidence (MEASURED,** `whole_reading.py`**).** I compared the checker with a copy in memory that also walks the children of a body-less clause:

| law | checker | that whole-tree reading |
|---|---|---|
| A1: If (line 3), its block holds a `say` (line 4) with a child `let 0` (line 5); the inline else declares `let 1` | W8 line 3 | W5 line 4 |
| A2: the same, numbered the other way | W5 line 4 | W8 line 3 |
| A4: the same with claims | W8 line 3 | W5 line 4 |
| C1: an inline-else `perform 3`, where clause 3 is a procedure under a `say` | W11 line 3 | W5 line 4 |

B1 (an absorbed arm clause with an inline body and a `let` child) gives W8 line 3. This is J1's mechanism again: an early line's inline statement is numbered after a part that may or may not be walked.

**Proposal**, one of:
- **(a) Say it.** State the third skip: the children of a clause that has children and no body, absorbed or not, are not entered, numbered or checked. Make W11 read "a procedure clause the walk has met", or make the checker test procedure clauses. Plant A1, A2 and C1.
- **(b) Ask him for a structure gate.** W5 and W7 are both computable from the parsed lines and the parent links, with no walk. Making them a third gate, after the chain gate, would make "the walk covers the whole tree" literally true. It would also remove G8's skips and settle K4 and K5(ii).

### K2: MAJOR. R7's own plant "a decoder accepting a non-canonical number" cannot be caught by any prediction R7 lists

**Sheet:**
- SHEET:95: R7, *"caught, by R1, R3 or R4"*.
- SHEET:105: the plant *"a decoder accepting a non-canonical number (`(lit int 07)`)"*.
- SHEET:373-375: Amendment 3 now reads *"caught by R1, R3, R4, R5, S3 or the do-nothing fixtures"*.

**Evidence (reasoned from the text, with one measurement):**
- R1 runs arithmetic vectors.
- R3, R4, R5, S3 and the fixtures run only law bytes the front end wrote, which are canonical.
- R2 (also canonical texts only) and R6 are not in the list.

So the plant passes by construction. R7 then fails, since the plant is not equivalent. The only prediction that holds non-canonical numbers is R6. MEASURED (`leading_zero2.py`): 9 of the 10,000 mutants are refused first by the checker for a leading zero, all flips (for example 00234, 00473, 00848). R6 catches the plant only where decoder1 refuses them (K3).

**Proposal:**
- Either add R6 to R7's list, or add a fixed, hashed set of non-canonical byte strings with an expected LOAD-REFUSED (an R2b). Each would be derived from a canonical law by one canonicity break: a leading zero, two spaces, uppercase hex, `\u{41}`.
- Also define "at the event where it was planted" for plants that have no event (budget plants, decoder plants).

### K3: MAJOR. R6's reference runner is not fixed, the refusal-or-crash boundary is the harness's, and "an accepted non-canonical form" has no judge

**Sheet:**
- SHEET:282: REFERENCE-REFUSED is *"both runs end in decoder1's own refusal, its `DecodeError`, with the same message"*.
- SHEET:328-331: *"decoder1 … run by the interpreter. Each run is a fresh process."*
- SHEET:342: NO-REFERENCE-RESULT: an acceptance is only *"recorded"*.
- SHEET:349: the falsifier *"an accepted non-canonical form"*.
- SHEET:350-353: the checker *"decides nothing"*.

**Evidence:**
- **The runner is unwritten.** Nothing names it: decoder1's entry point, the law seal given to `Interp` (the trace head and `(seal)` depend on it), or what the child prints.
- **The boundary moves with the runner (MEASURED).** An uncaught `DecodeError` from a module ends the process with exit 1 and the last line `fakedecoder.DecodeError: line 3: a refusal message`. By Amendment 3's crash rule, two such runs are NO-REFERENCE-RESULT, not REFERENCE-REFUSED. There, a core that accepts the mutant is merely recorded, not a falsifier. So the runner's design decides whether his E2 falsifier applies.
- **"Message" is undefined.** `str(e)`, or the stderr line?
- **No judge.** No procedure decides "non-canonical": the core's interface has no re-encoding output, and the checker decides nothing.
- **R6's power is unknown.** Whether decoder1 checks W4–W14 at all: could not check. If it does not, R6 cannot falsify a core that accepts canonical but ill-formed mutants. Where decoder1 crashes, his condition 3 (*"accepted only if its execution agrees with the decoded reference"*) is not enforced.

**Proposal:**
- Write and hash the R6 runner before the experiment:
  - the law seal is the sha256 of the mutant bytes;
  - the trace is on, under budget 1,000,000;
  - it catches only `decoder1.DecodeError`, printing `REFUSED <str(e)>` with exit 0;
  - everything else propagates.
- Define the message as `str(e)`.
- Ask the owner who judges "non-canonical". Options: decoder1's re-encoding compared with the bytes, or the checker's W1–W3 for canonicity only.
- Run decoder1 on the 10,000 now, and record its class per mutant in a hashed file. List for the owner the mutants decoder1 accepts or crashes on that the checker refuses.

### K4: MINOR. An inline `define`, `procedure` or `decimals` fails W6 and W7 on one line; the least-W rule gives W6, and the checker gives W7

**Document and code:**
- W6 (draft4:467): *"`define`, `procedure` and `decimals` are top-level clause statements, never inline"*, on *"its own line"*.
- W7 (draft4:468): *"the If's line"*.
- Phase 5: the least W on the line. Draft4:572-573: an inline statement that fails W7 has *"parts … not … checked"*. Whether its own place is a part is unsaid.
- `format_check.py:884-888` returns at W7 before W6.

**Evidence (MEASURED,** G1–G3**):** each gives W7 line 3. The document's least-W rule gives W6. The case has been present since draft 1 and was never planted.

**Proposal:** say which W wins (or settle it by K1(b)), and plant it.

### K5: MINOR. E1's reading needs two confirmations from the owner

**RULINGS.md:310-316** reads *"likewise"* as a second gate. Two points:

1. **The order of the two gates is the writer's, not ruled.** The "E1: the depth gate before the chain gate" plant fixes it.
2. **His fourth point is met only modulo the skips.** *"The subsequent walk covers the entire tree"* holds only modulo G8's skips, which keep J1's cross-line effect. MEASURED (`g8_cross.py`): with a sound inner chain the law is accepted. With an inner chain that fails W5 on line 4, it is W8 on line 3, a sound line.

The adopted disposition predicted J7's law at W8 line 3; draft 4 gives W4 line 4. That change is disclosed in "As kept", but he has not seen its consequence.

**Proposal:** put both points, and K1(b), to him.

### K6: MINOR. The chain gate's defining property is unplanted, and one "bite" is a crash of the reverted checker

**Code and document:**
- `plant_reverts.py:37-38`.
- Evidence: *"E1 undone: no chain gate, nothing skipped … undone CRASHED (KeyError) BITES"*.
- Draft4:720-722: *"Each bites"*.

**Evidence (MEASURED,** `chain_gate_revert.py`**).** With the gate removed and no crash:
- J7's plant: W4 line 4 either way.
- `perform 99` on line 3 and a chain naming 99 on line 4: W4 line 4 with the gate, W4 line 3 without.
- An undeclared variable on line 3 and `(block 99)` on line 4: W4 line 4 with the gate, W8 line 3 without.

**Proposal:** plant the last two, and count a crash of an undone checker separately from a changed report.

### K7: MINOR. S2's falsifier was not restated as a comparison of class and result

**Sheet:**
- SHEET:169: *"a stop at another count than the reference's where the reference has a RESULT"*.
- SHEET:362-363: *"S2's falsifier is Amendment 1's"*.

**Evidence:** by its letter, two cases are not falsifiers:
- a core completing with a wrong P or trace at 18 or 24 with no budget;
- a core completing where the reference stopped under B = 10.

Amendment 2's coverage text is generic. MEASURED: the reference gives RESULTs there, for example STOPPED after 25,165,823 at 24 under B = 10.

**Proposal:** give S2 R5's wording (STOPPED with the same count and trace, or COMPLETED with the same P and trace).

### K8: MINOR. The exhaustion kinds do not cover the stores J6 added

Draft4:71-74 lists *"variables"* among the stores. Section 10's kinds (:640) are *`law`, `stack`, `list`, `text`, `output`, `trace`*. Claim accumulators, cost counters and event payloads (an `'A'` payload can be about 134 MB) have no kind either. A kind outside the list is CORE-FAULT (SHEET:202, a stderr line not its row's). "And the like" leaves the infallible standard-library allocators (`Box::new`, `format!`, BTreeMap, `fs::read`) to guess.

**Proposal:** map each store to a kind, and name which standard-library allocations are forbidden.

### K9: MINOR. UNSTABLE-CORE's "result" is undefined outside COMPLETED, REFUSED and STOPPED

Draft4:680 and SHEET:269-270: *"differ in class or in result"*. For LOAD-REFUSED (`W<k> line <n>`, while `<reason>` is "free text which no comparison reads"), RESOURCE-EXHAUSTED (its kind) and EXTERNAL-TERMINATION, nothing defines the result.

**Proposal:** define it per class.

### K10: MINOR. J17's stdout rule was not carried into the sheet

Draft4:644 and :653 make anything on stdout contradict the row. The sheet's CORE-FAULT row (SHEET:202, *"files or stderr"*) and its evidence record (SHEET:253, *"the exit status, the stderr line, the files written"*) omit stdout, and Amendment 3 does not add it.

**Proposal:** add stdout to both.

### K11: MINOR. The fresh-folder rule leaves LAW's location and the working directory open

SHEET:297-300: *"has a fresh empty folder … where it must be empty … It runs nothing in a folder that is not empty"*. LAW is an input path. If it is placed in the folder, the folder is not empty. The working directory is not given.

**Proposal:** LAW lies outside the folder (or its listing is exempt), and the working directory is the folder.

### K12: MINOR. R8's exception covers only the reference; the arbiter's `run` sets the core's conditions too

SHEET:303-305 covers the reference only. In `arbiter.py:135` and `:219-240`, the core run under phase 3's *"arbiter's own build and run"* gets:
- a 600-second timeout, returned as `"stopped"`, *"never a dissent"*;
- the arbiter's own removal of stale files.

Both differ from the 60-second limit, EXTERNAL-TERMINATION and the fresh-folder rule.

**Proposal:** state R8's conditions for the core.

### K13: MINOR. Exit 5's source reading names neither who reads nor what a reading records

Draft4:75-77 (*"the milestone reads the core's source"*) and SHEET:383-390. If the core's author reads, it is self-certification.

**Proposal:** name an independent reader. The record should list every exit-5 site and its guard, and show that no panic hook or alloc-error path reaches it.

### K14: MINOR. A harness-caused end other than the 60-second kill is unclassed, so it defaults to CORE-FAULT

Draft4:663-666 and SHEET:378-382 give EXTERNAL-TERMINATION *"only when it ended the run itself, at its 60-second limit"*. His words (*"Any termination not caused by the harness is a core fault"*) do not class a harness-caused end. An operator's Ctrl-C reaches a child on the same Windows console.

**Proposal:** such a run is void and rerun, recorded as such.

### K15: MINOR. The exception-type rule's edge cases

SHEET:286-289. MEASURED:
- an exception with a note prints the note last (`KeyError: 99`, then the note line);
- a bare `raise AssertionError` prints a line with no `:`;
- a module's exception is qualified (`fakedecoder.DecodeError`).

**Proposal:** take the type from the last line of the form `Name: message` or `Name`, notes excluded. Say what happens with no `:`.

### K16: MINOR. Stale or missing wording

- `format_check.py:47`: *"its walk (25)"*, from draft 3.
- Draft 4's change table cites J10 in section 11, which says nothing of it.
- `stress-texts.txt` says of s2-doubling-64 *"compared with the reference"*, where SHEET:169 says *"recorded as stress evidence only"*.

**Proposal:** correct each.

## Files created

All are under `⟦HOME⟧\AppData\Local\Temp\reread4\` (also `⟦HOME83⟧\AppData\Local\Temp\reread4\`):

| what | files |
|---|---|
| checker runs | `fc-run.txt`, `fc-time.txt`, `ev-body.txt`, `run-body.txt` |
| plant-revert runs | `pr-run.txt`, `pr-ev-body.txt`, `pr-run-body.txt` |
| regenerated files | `r5-budgets.txt`, `r6-mutants.txt`, `r6-checker.txt`, `s3-budgets.txt`, `s3-gen.log`, `stress-texts.txt` |
| written stress texts | `stress\` (28 files: the 14 texts' `.orl` and `.law`) |
| my scripts and outputs | `odd_cases.py`/`.out`, `odd_cases2.py`/`.out`, `whole_reading.py`/`.out`, `budget_positions.py`/`.out`, `chain_gate_revert.py`/`.out`, `chains.py`/`.out`, `crash_type.py`/`.out`, `g8_cross.py`/`.out`, `leading_zero.py`/`.out`, `leading_zero2.py`/`.out`, `appendix_a.py`/`.out`, `time_s2.py` |
| S2 timing | `s2-timing.txt`, `s2-timing2.txt`, `s2-18-10.out`, `s2-18--1.out`, `s2-24-10.out`, `s2-24--1.out` |
| a fake decoder module | `fakemod\fakedecoder.py` |

The tool harness also saved the output of background runs in its own tasks folder.

No repository file was created or changed: `git rev-parse HEAD` gives `2e9805a…`, and no repository file is newer than 11:26 (my runs began after it).

## Appendix: commands and outputs behind the findings

```
$ python -B research/rust-core/format_check.py > fc-run.txt; cmp (evidence body, CR stripped) (run body)
IDENTICAL   # FORMAT CHECK (DRAFT 4) HELD: 304 of 304 …; plants 64 of 64 caught, 0 not run
$ python -B research/rust-core/plant_reverts.py   → IDENTICAL to evidence; "E1 undone: no chain gate, nothing skipped … undone CRASHED (KeyError) BITES"
$ python -B research/rust-core/gen_r5_budgets.py --out r5-budgets.txt   → 27b38350… IDENTICAL
$ python -B research/rust-core/gen_r6_mutants.py --out r6-mutants.txt   → a8f704fb…; drawn again: flip 34, truncate 413, swap 30644, id 11239; IDENTICAL
$ python -B research/rust-core/gen_r6_mutants.py --checker research/rust-core/r6-mutants.txt r6-checker.txt → accepted 538; crashed 0; 4365d26b… IDENTICAL
$ python -B research/rust-core/gen_stress_texts.py --out stress-texts.txt → d698ed6e… IDENTICAL; --write stress --manifest … → 14 texts equal
$ python -B research/rust-core/gen_s3_budgets.py --out s3-budgets.txt → RESULT 298; 2100 values; 86f3a7b0… IDENTICAL
$ sha256sum research/law-sufficiency/decoder1.py → 3584f565f6929879c3d942a45b3fa8d5c09cc2382b67772559109e38930ab877
$ python -B odd_cases.py .
A1 … inline else let 1                       W8 line 3 (variable 1 declared where 0 is next in the walk)
A2 … the other way round                     W5 line 4 (clause 2 has children and no body)
A3 control: clause 2 a while                 accepted
A4 claims                                    W8 line 3 (claim 1 where 0 is next in the walk)
B1 absorbed arm clause with a let child      W8 line 3
C1 perform of a procedure under a say        W11 line 3 (perform of clause 3, not a procedure defined before)
D1 inline if (W7) whose arm names 99         W4 line 3
D2 (block 99) under an existing arm          W4 line 3
D3 an else naming clause 0                   W4 line 3
D4 perform 99 line 3, chain 99 line 4        W4 line 4
D5 W8 line 3, W14(a) line 28                 W14 line 28
D6 W14(a) line 27, W14(c) line 28            W14 line 28 (parentheses nested deeper than 130)
D7 W14(a) line 27, W2 line 28                W2 line 28
E 5,000-digit (12 positions)                 no crash; int-string limit 4300 before and after
J10 defines 400/800/1600/3200: 0.01/0.04/0.13/0.48 s; Ifs 10k/20k/40k: 0.25/0.55/0.94 s; nested 30k/100k/300k: 0.60/1.67/5.35 s
$ python -B whole_reading.py .
A1 checker W8 line 3 | whole-tree W5 line 4;  A2 W5 line 4 | W8 line 3;  A4 W8 line 3 | W5 line 4;  C1 W11 line 3 | W5 line 4
$ python -B odd_cases2.py .
G1 inline define → W7 line 3;  G2 inline procedure → W7 line 3;  G3 inline decimals → W7 line 3
G7 floats line, float literal, then (decimals fixed) → W6 line 4
$ python -B chain_gate_revert.py .
J7's plant: W4 line 4 | without the gate (no crash): W4 line 4
perform 99 line 3 + chain 99 line 4: W4 line 4 | W4 line 3
undeclared var line 3 + (block 99) line 4: W4 line 4 | W8 line 3
$ python -B g8_cross.py .
inner chain sound → accepted;  inner chain fails W5 (line 4) → W8 line 3
$ python -B budget_positions.py .   (never imports format_check; limit 1000)
J15 inline arm: B=0..2 STOPPED/3/0; B=3 STOPPED/4/1; B=4 COMPLETED/5/2 … BUDGET POSITIONS: 0 mismatches (13 laws, every B 0..ops+1)
$ python -B chains.py .   → perform and rule chains of 100,000 accepted, written back exactly, 2.39 s / 2.33 s; limit 1000
$ python -B appendix_a.py .   → A.1–A.4 law bytes, seals, seal words, receipts, traces all verbatim in the draft; all-zero → babab-babab-babab-babab
$ python -B time_s2.py . stress/s2-doubling-24.orl
budget 10: STOPPED ops 25165823, 21.0 s / 21.2 s;  no budget: COMPLETED ops 25165824, 21.2 s / 21.3 s
$ python -B crash_type.py . stress   → s1-{perform,rule}-{600,3000}: exit 1, type 'RecursionError', both runs
$ python -B leading_zero2.py . research/rust-core/r6-mutants.txt → 9 mutants refused W2 for a leading zero, all flips (00234, 00473, 00848 …)
$ python -c "e=KeyError(99); e.add_note('a note…'); raise e" → last stderr line is the note
$ python -c "raise AssertionError" → 'AssertionError' (no ':')
$ (fakemod) python -c "import fakedecoder; fakedecoder.decode(b'')" → 'fakedecoder.DecodeError: line 3: a refusal message', exit 1
$ sha256sum SPEC.md RUNTIME-SPEC.md vectors/runtime-vectors.txt research/rust-core/vectors-as-integer.txt → 27dfff0c…, 0bd571d6…, 841240b7…, 2bff1c69… (446 lines; refusals 189: 143/6/40)
```
