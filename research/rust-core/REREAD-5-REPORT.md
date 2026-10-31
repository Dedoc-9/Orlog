> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-5: the independent re-read of LAW-FORMAT-0 draft 5, its checker and SHEET Amendment 4, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document, the checker,
the sheet, the reference runner or the files they fix. Its brief:
- read draft 5 (sha256 `f6e871b9…`) whole, appendix A included, and draft 4 for the changes; RULINGS.md whole, the
  "As kept" notes open to challenge, and the earlier dispositions; SHEET.md with Amendments 1-4 (`b0400caf…`);
  REREAD-4's report and dispositions; the checker, `plant_reverts.py`, `run_format.py` and their records;
  `ref_run.py`; the files Amendment 4 fixes and their generators; SPEC.md, RUNTIME-SPEC.md and `src/orlog/`;
- judge independently the writer's answer on the order of the three gates;
- never open, read, list or grep anything under `research/law-sufficiency/` (it could run scripts that import from
  there, and compute decoder1's sha256);
- write only under its own scratch folder in the system's temp directory, and change nothing in the repository;
- answer draft 5's Q1-Q6 with evidence, and list its findings, L1 onward, by severity.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-5: an independent re-read of LAW-FORMAT-0 draft 5, its checker, and SHEET Amendment 4

## What I read and ran

**Read, whole:** `LAW-FORMAT-0-DRAFT-5.md` (sha256 `f6e871b9…`, as stated), compared with draft 4 using `diff`; `RULINGS.md`; `SHEET.md` (`b0400caf…`, as stated), Amendments 1–4; `REREAD-4-REPORT.md` (K4–K16 in full); `REREAD-4-DISPOSITION.md`; the ASK E1 section of `REREAD-3-DISPOSITION.md`; the F8 line of `REREAD-0-DISPOSITION.md`; `format_check.py`; `plant_reverts.py`; `run_format.py`; `ref_run.py`; `gen_r6_reference.py`; `gen_r2b_twins.py`; the docstring, `id_tokens`, `sources` and `mutants` of `gen_r6_mutants.py`; `src/orlog/interp.py`; `arbiter.py:136-243`.

**Not read:** SPEC.md and RUNTIME-SPEC.md beyond their sha256, and `sema.py`, `front.py`, `syntax.py`.

**Hashes, all MEASURED.** Every hash the sheet and draft pin matches: SPEC, RUNTIME-SPEC, both vector files, `interp.py`, `numeric_ref.py`, `gen_worked.py`, `ref_run.py` `d55ce756…`, `r6-reference.txt` `255477ca…`, `r2b-twins.txt` `ef204d4d…`, `stress-texts-2.txt` `ea542dd1…`, `r6-checker-5` `852ead1d…`, `r2b-checker` `89b5b886…`, `decoder1.py` `3584f565…` (sha256 only). `format_check.py` is `97df27a1…`.

**Ran.** Every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, from the repository root or from my scratch folder. All results below are MEASURED:

| what | result |
|---|---|
| `format_check.py` | 304/304 laws, 78/78 plants. Its output is byte-identical to the body of `evidence/rust-core-format-5.txt` |
| `plant_reverts.py` | byte-identical to the body of `-5-reverts.txt`. PLANT REVERTS HELD: 29 plants and fixtures, 6 of them only by a crash |
| `gen_r2b_twins.py --out` | byte-identical to `r2b-twins.txt` |
| `gen_r2b_twins.py --checker` | byte-identical to `rust-core-r2b-checker.txt` |
| `gen_stress_texts.py --out` | byte-identical to `stress-texts-2.txt`. Its diff from `stress-texts.txt` is the generator's hash and the doubling-64 note only |
| `gen_r6_mutants.py --checker` | byte-identical to `rust-core-r6-checker-5.txt` |
| `gen_r6_reference.py --out`, full run (21 min) | byte-identical to `r6-reference.txt` (R6REF_IDENTICAL) |
| sample of 422 mutants through `ref_run.py`, twice each | 422/422 rows identical |
| my own scripts | listed under "Files created" |

**State at the end.** HEAD is `2e9805a`. Nothing changed under src/, tests/, vectors/, SPEC, RUNTIME-SPEC, research/rust-core/ or evidence/; all 27 hashes I recorded re-check OK. I never opened, listed or grepped anything under `research/law-sufficiency/`. To exercise decoder1's paths, I put a fake `decoder1` module in `sys.modules`, so the real file was never loaded.

## What I could not check
- **Draft 4's checker** (`b39bbd05…`) is not kept. Where I compare against draft 4, I compare against draft 4's text.
- **decoder1's source** is forbidden to me. I saw its behaviour only through `ref_run.py` and the fake module.
- **No core exists.** The Rust standard library's allocation and randomness behaviour (L11) is documented behaviour, NOT MEASURED.
- **SPEC and RUNTIME-SPEC** were checked for faithfulness only on the points named here. Other hosts and Linux were not run.

## Verdict
- **No BLOCKER. 4 MAJOR, 10 MINOR.**
- **What holds:**
  - The three gates come before any walk and recurse over nothing.
  - Once they pass, the walk reaches every clause exactly once: 220,000 fuzzed laws, about 89,000 of them reaching the walk, with 0 coverage assertions and 0 crashes.
  - Every frozen file reproduces byte for byte.
  - The R2b twins' expected refusals are what section 8 gives.
  - The budget positions and B1 are intact.
- **What does not:**
  - The gates' precedence is presented as derived from the specification, yet it contradicts the adopted E1(b) text, which the derivation never cites (L1).
  - R6's adjudicator is given too little of the document to adjudicate (L2).
  - `ref_run`'s refusal-versus-crash classification is not closed in its code (L3).
  - R2 has no observable at all (L4).

## Q1. F1's three gates
- **Before any traversal, no recursion: yes.** Spec :586-599. Checker :555-712: one pass for depth, then loops; the only recursion is over inline ifs nested within one line, bounded by W14(c).
- **Linear on big trees (MEASURED).** I built 30,000- and 300,000-clause trees that fail each gate: deep loops after an orphan, deep blocks plus a missing clause, flat orphans, flat bad chains. Time grows about tenfold for ten times the clauses (0.39 s → 3.95 s; 9.72 s at worst). No RecursionError.
- **A law failing any gate reaches no walk: yes.** Checker :711-712.
- **Every clause exactly once: yes, on everything I tried.**
  - The coverage assertion never fired: 100,000 fuzzed laws in `fuzz_cover.py` and 120,000 in `fuzz_cover2.py`, about 89,000 reaching the walk.
  - 20 hand-built odd cases (`odd_cases.py`) and 5 more (`bad_chain_named.py`) all give the literal reading of the W5 text. They cover inline ifs, absorbed clauses with children, blocks naming other clauses, three blocks naming one clause, chains naming missing clauses together with shape failures, procedures nested under while/if/procedure, and deep trees with structure failures.
  - Section 7's argument has one unstated step (L14).
- **Anything left of a skipped part?** No skip remains in the text or the checker. But W5 itself was narrowed in draft 5 (L8).
- **The structure gate is only partly planted (L7).**

## Q2. The gates' precedence
- **Is the derivation right? No.**
  - The adopted E1(b) text orders the depth gate before every W4–W13 check: *"If any clause fails, the least such line is reported as W14, and no W4–W13 check is made … one with an earlier W4–W13 failure now reports W14."*
  - Draft 5's claim that *"none of them orders one gate before another"* (:613) is therefore wrong (L1).
  - The strongest support for least-(line, W) is draft 3's adopted phase 3 pool. The derivation does not cite it.
- **Is the rule stated unambiguously? The rule itself, yes** (:598-599). Its basis is contested.
- **Does any earlier adopted rule require another order? E1(b) arguably does**, depth first. The owner's F1 remark that draft 4's order was *"the author's choice"* sits in tension with it. That is for him to rule.
- **Do the plants pin it?**
  - Against the six sequential orders: yes, each differs on at least one plant (MEASURED).
  - Against "least line, then the depth gate first on a line": no (L6).

## Q3. F2 and R2b
- **The adjudication.** It fixes who reads (a fresh agent, told neither verdict's source), what is recorded, and that checker agreement is never proof (SHEET :426-451). But the reader gets only sections 2–4 and 8, which cannot decide W4 labels, W6, W8, W10, W11 or W12. The draft is not pinned by sha256 either (L2).
- **The twins.** Fixed and hashed, and reproduced byte for byte. They do not trip W14(c), another W, or an earlier line.
  - I hand-checked one twin of each of the 15 kinds against sections 2, 3 and 8, with `r2b_sample.py`. All are correct.
  - Under the other reading of section 2's final `)` (L9), 0 of 1,558 twins change.
  - The construction argument needs W2 to parse with any spacing. That is implied by W3's sentence *"Once W2 holds, writing back gives the rest exactly if and only if W3 holds"*, but never stated (L9).
- **The runner.** It is pinned by path and sha256. Its line between a refusal and a crash is not closed in its own code (L3, L5).
- **Generators.** All reproduce byte for byte, the full `r6-reference.txt` included.

## Q4. The thirteen minor corrections

| | disposition | applied | his proviso |
|---|---|---|---|
| K4 | W7 through the gate; three plants | yes: three plants W7 line 3, which bite under "draft 4's text" (MEASURED). W6's row (:497) still says "never inline", which can now never be reached | consequence of F1 |
| K5 | ASK F1 | F1(b) ruled; precedence frozen | see L1 |
| K6 | two plants; chain gate undone without a crash; crashes counted apart | yes: both plants bite under both chain undoings, and the evidence names the crash-only ones (MEASURED) | no change |
| K7 | S2's falsifier in R5's words | yes (SHEET :519-521) | brings the falsifier in line with S2's own prediction |
| K8 | kinds by store; the fallible calls named; forbidden list; `state` dropped | yes (:82-88, :690-697), no new kind | respected. Residual guesses in L11 |
| K9 | a run's result, by class | yes (:738-740) | the "changes no class" claim cannot be shown (L12) |
| K10 | stdout in CORE-FAULT and in every record | yes (SHEET :524-525) | in line with J17. R8 gap in L13 |
| K11 | LAW outside the folder; working directory is the folder | yes | no change |
| K12 | R8's conditions for the core | yes (:528-530) | contradicts draft 5 :719 (L13) |
| K13 | an independent reader for exit 5 | yes (:89-93; SHEET :531) | no change |
| K14 | own process group; an interrupted experiment void whole | yes (:721-723; SHEET :532-534) | voiding replaces E3's CORE-FAULT, and voided records are not kept (L12) |
| K15 | REFERENCE-EXCEPTION line written by the runner | yes, but SystemExit is excluded (L5), and classify's inputs are left open (L3) | — |
| K16 | the comment, the change table, `stress-texts-2` | yes (`format_check.py` :42-43; :899; diff MEASURED) | no change |

**New plants bite (MEASURED).**
- K1's five each change under at least one structure undoing.
- K4's three change under "draft 4's text".
- K6's two change under both chain undoings.
- The precedence five change under all six sequential orders.
- The W11 change is equivalent:
  - it changes no plant;
  - fuzzing 28,934 laws (10,965 of which report W11), the two W11 rules differ on 0 (`w11_equiv.py`).

## Q5. B1, again
- **Termination.** The text is unchanged and the argument holds. The step *"P < Q"* needs W6 and the tree's pre-order, which the text leaves implicit; it is correct.
- **Budget positions (MEASURED).**
  - Probes: 6 laws through `ref_run.py` at every B from 0 to ops + 1, 40 runs, 0 mismatches against counts worked by hand from section 5.
  - What they cover: inline arms after two conditions, an absorbed clause, procedure, perform and define tails, the inline otherwise, a block arm, an absorbed else block, a for, and a while.
  - My first count for the while law was wrong: I forgot that `<` counts an operation. I corrected it and say so.
  - `interp.py` makes the check at every statement's entry, which agrees with section 5.
- **Explicit stacks, no limit on chains.** The text is unchanged. The checker accepts perform and rule chains of 100,000 and writes them back exactly (MEASURED).
- **Exhaustion against external termination and core faults.** Preserved, with the K12/K14 caveats (L12, L13).
- **Draft 5 broke none of them.**

## Q6. The checker against sections 2–4 and 8, and what a clean-room author must guess
- **The checker implements phases 1–4 W by W as written**, on everything I fuzzed or built.
- **What an author would still have to guess:**
  - how R2 is observed (L4);
  - whether section 2's final `)` is the last byte or the clause form's closing parenthesis (457 R6 mutants), and how W2 splits items written with no space (L9);
  - whether a bad chain's block makes the clause it names subject to EMPTY-BLOCK (L10);
  - HashMap's random seed against "no randomness", and whether the standard library's own allocations count (L11);
  - the narrowed W5 (L8).

## Findings

### L1: MAJOR. The frozen precedence is presented as derived, but it contradicts the adopted E1(b) text
- **The draft's claim.** Draft 5 :611-614 and SHEET :418-419 say F8 governs and *"none of them orders one gate before another"*. RULINGS "As kept" says E1 and F1 override F8 *"only by placing the three gates before the walk"*.
- **The adopted text.** `REREAD-3-DISPOSITION.md:93`, option (b), which he adopted (*"E1 — Adopt (b)"*, RULINGS :268) reads: *"If any clause fails, the least such line is reported as W14, and no W4–W13 check is made … one with an earlier W4–W13 failure now reports W14."* At that time the chain and structure checks (W4, W5, W7) were W4–W13 checks.
- **His own words in E1:** *"If either check fails, the checker reports the failure and does not walk the tree."*
- **Evidence (MEASURED):**
  - Precedence plant 1 (`format_check.py:1403`, a chain on line 3 and a clause 25 deep on line 28) expects W4 line 3. E1(b) gives W14 line 28, which is what draft 4's plant expected.
  - Plant 4 (a W7 on line 3, and a clause 25 deep on line 28) expects W7 line 3. E1(b) gives W14 line 28.
- **Proposal:**
  - Put both readings to the owner, quoting E1(b) beside F1's *"the author's choice"*.
  - Until he rules, call phase 3's rule a proposal frozen for evidence, not a derivation.
  - If E1(b) governs: whenever any W14(a)/(b) failure exists, report the least W14 line; otherwise take the least (line, W) between chain and structure. Plants 1 and 4 change with it.

### L2: MAJOR. R6's adjudicator cannot apply section 8 from sections 2–4 and 8 alone
- **The sheet:** SHEET :434: *"It is given LAW-FORMAT-0's sections 2–4 and 8"*.
- **What section 8 rests on:**
  - section 1, line numbers (:126);
  - section 5, *"checked at"*: W8 scope :541, W10–W12;
  - section 6, the derivations Labels (W4) and Decimals (W6 :497);
  - section 7, the walk's numbering of ids (W8 :499, phase 4 :602).
- **What is at stake:** the draft-5 checker's own counts on R6 (r6-checker-5 header): W8 1,485, W10 143, W11 73, W6 31, W12 12, W4 54.
- **Why it matters:** an "undecided" case *"counts for nothing until he rules"*, so a too-narrow reading set weakens R6. No draft version or sha256 is pinned either.
- **Proposal:** give the reader sections 1–8 of the exact draft the core was built from, by sha256.

### L3: MAJOR. `ref_run`'s refusal-versus-crash line is not closed in its code
- **The sheet and the runner say it is:** SHEET :495 *"A harness calls it and decides nothing itself"*. `ref_run.py:26-28` defines a run as *"(exit status, stdout's last line, stderr's last line)"*, with "last line" undefined.
- **(a) The extraction is the harness's (MEASURED, `naive_extract.py`).**
  - `gen_r6_reference.py:66-69` drops empty lines and turns CR LF into LF.
  - `split("\n")[-1]` on the same two processes turns RESULT into NO-REFERENCE-RESULT, and REFERENCE-REFUSED into NO-REFERENCE-RESULT. Windows stdout ends `\r\n`.
- **(b) Runner and harness faults are classed as reference crashes (MEASURED, `runner_paths.py`).** Each of these comes out NO-REFERENCE-RESULT:
  - a usage error, which exits 1 with `usage:`;
  - BUDGET `1e6`, giving `builtins.ValueError`;
  - a missing PATH, giving `FileNotFoundError`;
  - `decoder1.PLANT` set, giving the runner's own guard `RuntimeError` (`:95-96`);
  - KeyboardInterrupt.
- **Consequence:** a planted decoder turns all 10,000 mutants into NO-REFERENCE-RESULT, where *"a core that accepts a mutant is only recorded"*.
- **Proposal:**
  - `classify` takes the raw (returncode, stdout bytes, stderr bytes) and extracts the lines itself.
  - Runner faults (usage, a bad BUDGET, an unreadable input, the plant guard) get their own exit status and line, classed as an experiment fault that stops the run, never NO-REFERENCE-RESULT.

### L4: MAJOR. R2 has no defined observable
- **The prediction:** SHEET :90, R2: *"it re-encodes the law bytes it read exactly … one byte differs"*. R6 likewise says *"accepts exactly the bytes it would write"*.
- **The gap:** section 10 (:644-743) writes no re-encoding. The receipt's law seal is the hash of the bytes read.
- **Consequence:** R2 cannot be measured as preregistered, and a clean-room author must guess whether to add a mode. This goes against B1's *"Fix the comparison protocol before testing."*
- **Proposal:** define a write-back mode in section 10 (arguments, files, exit statuses), or restate R2 in terms of R2b, R6 and the seal, and say what it no longer shows.

### L5: MINOR. `ref_run` against its docstring and Amendment 4 (MEASURED, `runner_paths.py`)
- `FRONT-END-REFUSED` exits 0, yet `classify` calls it a crash, NO-REFERENCE-RESULT. The sheet's table (:497-502) gives it to UNSTABLE as "anything else".
- `except SystemExit: raise` (`:139-140`): a `sys.exit` inside the reference ends without the REFERENCE-EXCEPTION line (fake decoder, `exit0` gives status 0, type none). The docstring (:22) and the sheet (:492) say *"any other exception, anywhere"*.
- BUDGET `-1` is accepted and gives `RUN STOPPED ops 0`, a RESULT no core run can match. `05` and `+5` are accepted too.
- The usage exit path (exit 1, `usage:` on stderr) is undocumented.
- **Proposal:** fix the code to match the table, or the table to match the code; validate BUDGET as a canonical decimal.

### L6: MINOR. The precedence plants do not pin the rule on same-line ties with the depth gate
- **Evidence (`precedence_variant.py`, MEASURED).** "Least line, then depth, chain, structure on a line" gives all five precedence plants unchanged, but differs on:
  - a clause 25 deep whose own If names 99: frozen W4 line 27, variant W14 line 27;
  - the same clause with an inline while: frozen W7 line 27, variant W14 line 27.
- **Proposal:** add these two plants.

### L7: MINOR. Only part of the structure gate is planted
- **Evidence (`shape_in_walk.py`, `struct_parts_in_walk.py`, MEASURED).** Each of these, moved alone from the gate into phase 4, changes 0 of the 78 plants:
  - the W5 chain-shape checks;
  - ORPHAN-OTHERWISE;
  - EMPTY-BLOCK.
- **The probes do tell them apart.** Each is a W8 on line 3 with the structure failure on a later line: draft 5 gives W5 on the later line (5, 4 and 4); each undoing gives W8 line 3.
- **What was promised:** `REREAD-4-DISPOSITION.md:177`, *"one law per structure failure that the gate reports before an earlier phase-6 failure"*. Only UNEXPECTED-CHILDREN (K1), and W7 by way of K4, are planted.
- **Proposal:** plant the three probes.

### L8: MINOR. Draft 5 narrows W5 without its own tag or a note to the owner
- **The change:** :496, in three places: *"of an If that is a clause's statement"*, *"such If"*, *"(An inline `if` fails W7, and its parts name nothing here.)"*.
- **Evidence (`inline_block_names.py`, MEASURED):** a `say` with a child, named only by an inline if's block on line 5, gives W5 line 3. Under draft 4's text the clause *"is named by a (block ⟨C⟩)"*, so the failures sit on line 5.
- **Note:** F1 made W5 a gate; it did not narrow it.
- **Proposal:** tag the change and put it to him.

### L9: MINOR. Section 2's "final )" and W2's splitting of items are each readable two ways
- **The final `)`.** Section 2 (:149) does not say whether it is the line's last byte or the parenthesis that closes the clause form.
  - Evidence (`w1_w2_boundary.py`, MEASURED): 457 R6 mutants have a different first failure under the two readings, the checker giving W2 where the other reading gives W1. R2b is unaffected (0 of 1,558).
  - Only the H5 sentence at :563 hints at the checker's reading.
- **Missing spaces.** `(say(lit int 1))`, `(str"a")` and two forms with no space between them all give W3 in the checker. Section 1 never says W2 can split items that have no space between them.
- **Proposal:** one sentence for each.

### L10: MINOR. A chain naming a missing clause: are the clauses its block names subject to EMPTY-BLOCK?
- **The text:** :594-596, *"taken as named, so that none of them fails W5 for want of a chain or a block"*.
- **Evidence (`bad_chain_named.py` B1):** a `say` on line 3 with no child, named by the block of a chain on line 4 that also names 99. The checker gives W5 line 3 (*"has a body and no children"*). *"The W5 checks … are not made"* could equally give W4 line 4.
- **Proposal:** say explicitly.

### L11: MINOR. Section 0's allocation rules leave guesses (NOT MEASURED)
- **Randomness.** :83 lists `HashMap::try_reserve`, but `HashMap`'s default `RandomState` seeds from the OS, against :68 *"no randomness"*. Iteration order could then vary between runs and make cases UNSTABLE-CORE.
- **What counts as a store.** It is unclear whether *"every store whose size depends on … the run"* covers the standard library's own allocations: `env::args`, the path conversion inside `File::open`. Without `unsafe`, those cannot be made fallible.
- **Other gaps.** Whether `TryReserveError::CapacityOverflow` counts as a failed allocation. Which kind the receipt's buffer reports, since its size depends on the number of claims.
- **Proposal:** name a deterministic hasher; say whether standard-library temporaries sized by arguments are in scope.

### L12: MINOR. K9 and K14 against his proviso
- **K9.** It decides cases Amendment 3 left undefined: two RESOURCE-EXHAUSTED runs with different kinds, or two LOAD-REFUSED runs with different W or line, now make the case UNSTABLE-CORE, which fails. RULINGS' *"changes no class"* cannot be shown.
- **K14.** "Void whole" replaces E3's *"Any termination not caused by the harness is a core fault"* for an interrupt that reaches the core. It also does not say voided runs are kept (his condition 6).
- **Proposal:** put both to him, and record every voided run and its count.

### L13: MINOR. R8's conditions conflict
- SHEET :484, *"Every reference run of the experiment is `ref_run.py`"*, against Amendment 3's R8 exception (:303). Amendment 4 governs where they differ.
- K12 makes the arbiter's 600 s stop EXTERNAL-TERMINATION, against draft 5 :719, *"only when it ended the run itself, at its 60-second limit"*.
- The arbiter's `run` (`arbiter.py:219-243`) neither records stdout (K10) nor starts a process group (K14).
- **Proposal:** state R8's exceptions in Amendment 4 and in section 10.

### L14: MINOR. Section 7's "only once" leaves one step unstated
- **The text:** :465-466 cites only *"no clause is named by two blocks"*.
- **The missing step:** no `while`, `for` or procedure clause is named by a block. Otherwise its children would sit in two sequences. It follows from the shape rule (a block names its arm's own clause, which is the If's clause or an absorbed one), but the argument should say so.

## Files created
All under `⟦HOME⟧\AppData\Local\Temp\reread5\`:
- **Run outputs:** `fc_run1.txt`, `fc_run1.err`, `ev5_body.txt`, `pr_run1.txt`, `pr_run1.err`, `ev5r_body.txt`, `budget_positions.out`, `hashes_end.txt`.
- **Regenerated files:** `r2b-twins.regen.txt`, `r2b-checker.regen.txt`, `stress-texts.regen.txt`, `r6-checker.regen.txt`, `r6-reference.regen.txt`, `r6-reference.regen.log`.
- **Scripts:** `fuzz_cover.py`, `fuzz_cover2.py`, `odd_cases.py`, `bad_chain_named.py`, `gates_scale.py`, `chains.py`, `fake_decoder_run.py`, `runner_paths.py`, `naive_extract.py`, `sample_r6.py`, `budget_positions.py`, `w1_w2_boundary.py`, `r2b_readingB.py`, `r2b_sample.py`, `precedence_variant.py`, `inline_block_names.py`, `shape_in_walk.py`, `struct_parts_in_walk.py`, `w11_equiv.py`.
- **Inputs (`inputs\`):** `good.law`, `say1.orl`, `bad.orl`, `rulechain3000.orl`, `X1.law`, `X2.law`, `X4.law`, `X5.law`, `X6.law`, `X7.law`.
- **Sample:** `r6sample\laws\` holds 422 `.law` files.
- **Folders:** `runs\` and `r6sample\runs\` are empty. They held per-run folders, each removed after its run. `gen_r6_reference.py` also made and removed its own `r6ref-*` folder in the temp folder.

## Appendix: commands and outputs behind the findings
```
# full regeneration of r6-reference.txt
python -B research/rust-core/gen_r6_reference.py --out %TEMP%\reread5\r6-reference.regen.txt
GEN-R6-REF: 10000 mutants; NO-REFERENCE-RESULT 632, REFERENCE-REFUSED 6994, RESULT 2374; environments 1; sha256 255477ca…  (cmp: identical)

# the other generators and checkers
gen_r2b_twins.py --out ...      -> sha256 ef204d4d… (identical)
gen_r2b_twins.py --checker ...  -> agrees 1558/1558, 89b5b886… (identical)
gen_stress_texts.py --out ...   -> ea542dd1… (identical)
gen_r6_mutants.py --checker ... -> accepted 538, crashed 0, 852ead1d… (identical)
sample_r6.py 400                -> 422 re-run twice, rows identical 422, differing 0

# L1, L6: precedence_variant.py
F1 gates: … (all 5 plants)                         frozen = variant   same
a clause 25 deep whose own If names 99             frozen W4 line 27  variant W14 line 27  DIFFERS
a clause 25 deep, own If with an inline while      frozen W7 line 27  variant W14 line 27  DIFFERS

# L3, L5: runner_paths.py and naive_extract.py
text mode, a text the front end refuses            NO-REFERENCE-RESULT  (0, 'FRONT-END-REFUSED SYNTAX', '')
usage: no arguments                                NO-REFERENCE-RESULT  (1, '', 'usage: ref_run.py …')
a budget that is not a decimal                     NO-REFERENCE-RESULT  … 'REFERENCE-EXCEPTION builtins.ValueError'
a negative budget                                  RESULT  (0, 'RUN STOPPED ops 0 …')
PATH missing                                       NO-REFERENCE-RESULT  … builtins.FileNotFoundError
fake decoder1: holds a plant                       NO-REFERENCE-RESULT  … builtins.RuntimeError
fake decoder1: decode calls sys.exit(0)            NO-REFERENCE-RESULT  (0, 'ENV …', '')
fake decoder1: KeyboardInterrupt                   NO-REFERENCE-RESULT  … builtins.KeyboardInterrupt
A.2 law:               filtered last line -> RESULT;            naive last line -> NO-REFERENCE-RESULT
fake decoder1 refuses: filtered last line -> REFERENCE-REFUSED; naive last line -> NO-REFERENCE-RESULT

# L7
shape_in_walk.py:        plants changed 0 of 78; probe: draft 5 W5 line 5, shape-in-walk W8 line 3
struct_parts_in_walk.py: orphan, plants changed 0 of 78, probe W5 line 4 vs W8 line 3
                         empty,  plants changed 0 of 78, probe W5 line 4 vs W8 line 3

# L8, L9, L10
inline_block_names.py: draft 5's checker: W5 line 3 (clause 1 has children and no body)
w1_w2_boundary.py:     457 R6 mutants differ between the two readings; missing spaces -> W3; clause form closed early -> W2
r2b_readingB.py:       0 of 1558 differ
bad_chain_named.py B1: W5 line 3 (clause 1 has a body and no children)

# Q1, Q5
fuzz_cover.py 20000×5:  TOTAL PROBLEMS 0
fuzz_cover2.py:         120000 laws, problems 0
gates_scale.py:         300,000 clauses: W5 line 3 3.95 s, W14 line 27 6.45 s, W5 line 3 1.79 s, W4 line 3 9.72 s
chains.py:              perform and rule chains of 100,000 accepted and written back exactly
budget_positions.py:    40 runs, 0 mismatches
w11_equiv.py:           28,934 laws; 10,965 W11; the two rules differ on 0

# timings are software timings (perf_counter), not measurements of any core
```
