> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-6: the independent re-read of LAW-FORMAT-0 draft 6, its checker and runner, and SHEET Amendment 5, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document, the checker,
the runner, the sheet or the files they fix. Its brief:
- read draft 6 (sha256 `c5435579…`) whole, appendix A included, and draft 5 for the changes; RULINGS.md whole, the
  "As kept" and correction notes open to challenge, and the adopted option texts; SHEET.md with Amendments 1-5
  (`fb505ccf…`); REREAD-5's report and dispositions; the checker, `plant_reverts.py`, `run_format.py`, `ref_run.py`,
  `ref_run_paths.py` and their records; the files Amendments 4 and 5 fix; SPEC.md, RUNTIME-SPEC.md and `src/orlog/`;
- review explicitly, in the owner's words, *"the gate precedence, write-back observability, and all three N3
  interpretations"*, and check his proviso on the minor corrections;
- never open, read, list or grep anything under `research/law-sufficiency/` (it could run scripts that import from
  there, and compute decoder1's sha256);
- write only under its own scratch folder in the system's temp directory, and change nothing in the repository;
- answer draft 6's Q1-Q6 with evidence, and list its findings, M1 onward, by severity.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-6: an independent re-read of LAW-FORMAT-0 draft 6, its checker and runner, and SHEET Amendment 5

## What I read and ran

**Read in full:**
- `LAW-FORMAT-0-DRAFT-6.md` (sha256 `c5435579…`, as stated), appendix A included, and `diff` against draft 5.
- `RULINGS.md`, `REREAD-5-REPORT.md`, `REREAD-5-DISPOSITION.md`.
- The adopted option texts: E1(b) (`REREAD-3-DISPOSITION.md:93`) and F1(b) (`REREAD-4-DISPOSITION.md:117`).
- `SHEET.md` (`fb505ccf…`, as stated), Amendments 1–5.
- `format_check.py`, `plant_reverts.py`, `run_format.py`, `ref_run.py`, `ref_run_paths.py`, `gen_r6_reference.py`, the docstring of `gen_r6_mutants.py`, and the -6 evidence files.
- From the specifications and source: SPEC §3, §6, §7; RUNTIME-SPEC §6–§7; `interp.py:85-330`; `arbiter.py:130-243`.

**Not read:** `sema.py`, `front.py` and `syntax.py`. The checker's derivations are compared with the analysis on 304 laws, and I re-ran that comparison. I opened nothing under `research/law-sufficiency/`. Its only touch was `sha256sum decoder1.py`, plus scripts that import from there.

**Hashes (MEASURED).** Every hash the draft and the sheet pin matches:
- SPEC, RUNTIME-SPEC, both vector files, `interp.py`, `numeric_ref.py`, `gen_worked.py`;
- `ref_run.py` `33914074…`, `ref_run_paths.py` `e1edf642…`, `gen_r6_reference.py` `0a100c1e…`;
- `r6-reference-2.txt` `e2483cf5…`, `r6-checker-6` `6031e11f…`, `r2b-twins.txt` `ef204d4d…`, `stress-texts-2.txt` `ea542dd1…`;
- `decoder1.py` `3584f565…`.
- `format_check.py` is `3c3ad0b6…`.
- The supplementary vectors count 446 lines (x_as_i 178, f_as_i 268), of which 189 are refusals (6 NOT-FINITE, 143 INEXACT-CONVERSION, 40 OVERFLOW), as stated.

**Ran (MEASURED).** Every run used `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`. Windows 11, CPython 3.14.5.

| what | result |
|---|---|
| `format_check.py` | identical to the body of `evidence/rust-core-format-6.txt` (CR LF made LF): 304/304 laws, plants 84/84 |
| `plant_reverts.py` | identical to the body of `-6-reverts.txt`: PLANT REVERTS HELD, 35 changed, 6 only by a crash |
| `ref_run_paths.py` | identical to the body of `rust-core-ref-run-paths.txt`: 25 of 25 |
| `gen_r2b_twins.py --out` / `--checker` | identical to `r2b-twins.txt` / `rust-core-r2b-checker-6.txt`: agrees 1558/1558 |
| `gen_r6_mutants.py --checker` | identical to `rust-core-r6-checker-6.txt`: accepted 538, crashed 0 |
| `gen_stress_texts.py --out` | identical to `stress-texts-2.txt` |
| `gen_r6_reference.py --out`, full run (26 min) | **identical to `r6-reference-2.txt`** (R6REF_IDENTICAL) |
| `diff r6-reference.txt r6-reference-2.txt` | only header lines 2–3 (the generator's and the runner's sha256) differ |
| `r6_sample.py`: 242 mutants (every 50th, and all 43 RecursionError ones) through `ref_run.py`, twice each | 242/242 rows identical, 0 runner faults |
| my own probes | listed under "Files created" |

**State at the end.**
- HEAD is `2e9805a`, and src/, tests/ and vectors/ are clean.
- A combined sha256 over every research and evidence file is the same before and after (`db904eef…`).
- The temporary folders that I and the tools made are all removed.

## What I could not check
- **No core exists.** R2's observation (M1), the exit-5 source reading and the write-back mode's behaviour are REASONED, not measured.
- **decoder1's source is forbidden to me.** So is whether it imports other files. Its behaviour was seen only through `ref_run.py`, and through stand-in modules put in `sys.modules`.
- **Draft 4's checker is not kept.**
- **Only one host.** Linux and other hosts were not run.
- **SPEC and RUNTIME-SPEC** were checked only on the points named below: budget positions, If and rule counting, and the receipt.

## Verdict
**No BLOCKER. 2 MAJOR (M1, M2), 8 MINOR (M3–M10).**

**What holds (MEASURED):**
- **N1 is stated unambiguously,** is faithful to E1(b) and to his words, and is implemented exactly.
  - My independent phase 3, written from section 8's text, agrees with the checker on 80,000 fuzzed laws.
  - A control using draft 5's rule differs on 4,406 of 40,000, so the comparison has power.
  - The gates are linear on 300,000-clause trees with several gates failing, and no RecursionError occurs.
  - plant_reverts pins N1 against draft 5's rule and all six sequential orders.
- **Every frozen file reproduces byte for byte,** the full R6 reference included.
- **The budget positions hold:** 60 runs at every B, 0 mismatches.
- **Chains of 100,000 are accepted.**
- **Appendix A reproduces through the reference.**

**What does not:**
- **R2's write-back cannot tell a re-encoding from an echo of LAW (M1).** So the gap N2 was adopted to close (a core that drops a name no run reads) is still unseen.
- **L2 and L3 were applied outside his words (M2).** They are MAJOR findings, applied under a ruling that names "the ten minor findings". L3's and L5's changes alter the adopted reference classification. The runner-fault rule extends his N3(3) beyond what he said.

## Q1. The gates' precedence (N1)
- **The statement: unambiguous.**
  - §8:611-619 states the depth gate first ("no W4–W13 check is made"), then the least (line, W) among W4 chain refs, W5 and W7, then the walk.
  - §5:321-325, §7:465, the W14 and W4 rows, §11 and SHEET A5:561-565 all agree with it.
  - It matches E1(b)'s option text and N1's words (RULINGS:400-404).
  - One precision point: the stated reason omits F1(b)'s option text (M8). The rule is unaffected.
- **The checker does exactly that.**
  - The depth gate is one pass and returns before any chain or structure check (`format_check.py:571-583`). The chain and structure failures are collected together (638-720), and `min` takes the least (line, W) (525-527).
  - Ties (MEASURED, plants and `ties6.py`): W14 against W4 or W7 on one line gives W14; W4 against W7 gives W4; W4 against W5 gives W4; W5 against W7 gives W5.
  - Huge trees (MEASURED, `gates_big.py`): every case is as N1 says, from 30,000 to 300,000 clauses. A chain on line 3 with a 25-deep tail gives W14; an orphan on line 3 above a 300,000-deep tree gives W14 line 28; chain-then-orphan gives W4; orphan-then-chain gives W5; W7 on line 3 with 17 loops gives W14. Times run 0.27→2.78 s, 5.25 s at worst.
  - Fuzz (MEASURED, `fuzz6.py`, 60,000 laws): 0 coverage assertions, 0 crashes.
- **The plants pin it.**
  - Draft 5's rule changes 4 of the 7 precedence plants, as stated.
  - Every sequential order changes at least one. The two depth-first orders are each pinned by a single plant: "W5 body on line 3" and "W4 and W7 on one line".

## Q2. Write-back observability (N2)
- **Kept apart, and runs nothing:** yes (§10:720-742). It is a separate command line, writes OUT only, and has no budget, receipt or trace.
- **SHEET A5's R2 row** fails on a difference and on any class but WRITTEN-BACK, a load refusal included (SHEET:576).
- **Not a new semantic path or a change of authority:** nothing reads it but R2.
- **But R2 cannot distinguish OUT written from the core's structures from OUT copied from the bytes it read (M1).** The mode also leaves three guesses (M5).

## Q3. The three N3 interpretations
- **(a) W5's narrow reading.**
  - It is stated explicitly in W5's row (§8:509), tagged [N3, L8], and planted.
  - The plant bites: undone, it reports W7 line 5.
  - Nothing contradicts it. §7's generic "named by one block" concerns only clause-statement Ifs, the only ones that reach the walk. The chain gate's treatment of inline ifs' ⟨C⟩s as references is W4's, not W5's ("here").
  - The checker builds blocks and absorbed-clause naming from clause-statement Ifs only (662-704).
  - **Gap:** the same narrowness for an inline if's arms and else (ORPHAN-OTHERWISE) is untested (M4). A related W5 naming ambiguity is M3.
- **(b) A run's result by class.**
  - §10:781-786 defines a result for all ten classes, written back included.
  - It says two runs differing only in a load refusal's (W, line), or in an exhaustion kind, are UNSTABLE-CORE, in his words (SHEET A5:594-597 alike).
  - The six kinds are unchanged. L11 maps the receipt's buffer to `output`, and the write-back's bytes to `law`.
  - Reading "UNSTABLE" as UNSTABLE-CORE (RULINGS:437-438) is sound.
  - **But:** the write-back's kind of a load failure is not fixed (M5a), which matters under (b). SHEET A4:524-525 still says K9 "changes no class" (M9).
- **(c) Interrupted experiments.**
  - The draft (§10:763-766) and SHEET A5:598-599 are consistent and quote him: discarded whole, runs kept and counted, never used toward acceptance.
  - Runner faults are given the same treatment (SHEET A5:618-619; `ref_run.py:25-26`). That is the writer's extension (RULINGS:442-443), not his words.
  - A runner fault that recurs on every repetition has no end (M2).

## Q4. The ten minor corrections

**First, the count.** Draft 6 §12 (:919) and the brief call "L2, L3 and L5–L14" ten. That is twelve items. L2 and L3 are MAJOR (REREAD-5-DISPOSITION:51, 76-77). See M2.

| | disposition | applied? | evidence | his proviso |
|---|---|---|---|---|
| L2 (MAJOR) | adjudicator gets the whole draft, by sha256 | yes, SHEET:601-603 | text | not one of the ten minor ones. Incomplete: SPEC.md is not given (M6) |
| L3 (MAJOR) | `classify` raw; RUNNER-FAULT exit 3; experiment void | yes (`ref_run.py` `33914074`) | ref_run_paths 25/25 reproduced | alters Amendment 4's adopted classify (M2) |
| L5 | front-end refusal a runner fault; SystemExit a crash; BUDGET canonical; usage documented | yes | ref_run_paths rows. Restoring `except SystemExit: raise` gives 24/25, confirming A5's claim | front-end refusal and budget −1 change class: were NO-REFERENCE-RESULT / RESULT (REREAD-5-REPORT:279, 282), now RUNNER-FAULT (M2). SystemExit stays NO-REFERENCE-RESULT |
| L6 | two ties planted | yes | both bite under draft 5's rule | with N1 |
| L7 | three probes planted, each undone alone | yes | each bites: undone gives W8 line 3 | mechanical |
| L8 | tag and plant | yes | bites | block side only (M4) |
| L9 | final `)` the last byte; how items split | yes (§1:132-134, §2:159-161) | the checker matches | mechanical |
| L10 | a W4 chain's names count for both children rules | yes (W5 row; phase 3) | P6 gives W4 line 3 | the row ("children rules") and phase 3 ("still named") differ on the orphan rule (M3b) |
| L11 | hasher; "the run"; capacity overflow; receipt buffer is `output` | yes (§0:90-94; §10:712) | text only | no new kind. Counting capacity overflow toward exit 5 decides a point E3 left open, consistent with "failed fallible call" |
| L12 | RULINGS corrected; voided runs kept and counted | RULINGS and §10 yes | | SHEET A4:524-525 not corrected (M9) |
| L13 | R8's exceptions | yes (§10:761-763; SHEET:634-639) | `arbiter.py:136` timeout 600; `run` keeps no stdout and makes no process group | mechanical |
| L14 | section 7's missing step | yes (§7:477-479) | | mechanical |
| L1, its DRAFT part | corrected in place: RULINGS, draft 5 §8, A4 | RULINGS and A4 yes, draft 5 no | draft 5 still `f6e871b9` | M9 |

**Does ref_run_paths hold the runner to its docstring?** It holds the ways it ends, not the docstring's run conditions (M7).

## Q5. B1 requirements
None is broken by draft 6.
- **Termination.** The text is unchanged. I re-derived "P < Q" from W6, W11 and pre-order, and the rule measure from W10.
- **Budget.** The text is unchanged. Through `ref_run.py` at every B from 0 to ops+1, 8 laws and 60 runs give 0 mismatches against hand-worked check lists (MEASURED, `budget_probe.py`). The laws cover: an inline else after counted conditions, a while, a for, procedure/define/decimals checks, a perform, a rule use, an absorbed else block, an else-if inline, the inline otherwise, and an and/or condition. `interp.py:151` checks at every `stmt` entry.
- **Explicit stacks.** The text is unchanged. The checker accepts perform and rule chains of 100,000 and writes them back exactly (MEASURED, `chains6.py`).
- **Exhaustion against external termination and core faults.** Unchanged. R8's 600 s stop is consistent with E3, since there the arbiter's `run` is the harness.
- **The write-back mode** adds exit-5 sites, which §0's "every exit-5 site" reading covers.

## Q6. Checker against sections 2–4 and 8; what a clean-room author would still guess
- **The checker implements phases 1–4 as written** on everything I ran, except W5's naming of absorbed clauses (M3).
- **Its "written back exactly" line is not measured as printed** (M10).
- **The core author would still guess:**
  - whether OUT may come from the bytes read (M1);
  - which If parts name an absorbed clause (M3);
  - the write-back's exhaustion kind, and `--`-prefixed paths (M5).
- **The harness author would still guess:**
  - the CORE-FAULT example's applicability in write-back (M5c);
  - what ends a recurring runner fault (M2);
  - what "the experiment" and "counted" mean in granularity (M2).

## Findings

### M1 — MAJOR. R2 cannot tell a write-back from an echo of the input
- **Text.**
  - Draft 6:723-724: *"On a pass it writes to OUT the bytes it writes back from what it loaded, by sections 2–4"*.
  - :656-657: *"For the core, the round trip is observed through its write-back mode … byte for byte, by R2"*.
  - :741: *"R2 compares OUT with LAW byte for byte"*.
  - SHEET:576 (R2).
  - His words, quoted at :720: *"The core writes back the exact law bytes it successfully loaded."* That sentence itself admits the echo reading.
- **Evidence (REASONED; no core exists).**
  - Every byte string that passes section 8 is canonical, so a correct writer gives OUT = LAW.
  - A core that writes back the buffer it read gives the same OUT.
  - Nothing else distinguishes them: R2b's twins never reach OUT, and R3/R4 read no name.
  - So L4's case — *"A core that runs every law correctly, yet drops a part no run reads (a name, say), would pass R3 and R4 and break section 9's round trip unseen"* (REREAD-5-DISPOSITION, ASK N2) — passes R2 as well if its write-back echoes.
  - Corroboration (MEASURED, M10): in the checker, passing phases 1–2 already implies the exact write-back by construction. So for a canonical law, writer and echo coincide.
- **Proposal (ASK).**
  - (a) §10: OUT is produced only by the writer of sections 2–4 from the loaded structure, never from the bytes read.
  - (b) R7 gains a writer plant, e.g. "write-back omits a `let`'s name" or "reverses an `(over …)` list", required to be caught by R2. An echoing core lets it pass, so R7 exposes the echo.
  - (c) §0's independent source reading also records where OUT's bytes come from.
  - Or else: R2's record states that it does not show the core keeps every written part.

### M2 — MAJOR. L2 and L3 applied under "the ten minor findings"; L3 and L5 change the adopted classification; runner faults handled as interrupts by the writer's extension
- **Text.**
  - RULINGS:391: *"its DRAFT items for the ten minor findings"*.
  - His words, :431-432: *"The ten minor findings may be applied … provided they do not alter adopted semantics or classifications."*
  - REREAD-5-DISPOSITION:51: *"4 MAJOR (L1–L4), 10 MINOR (L5–L14)"*. :76-77: L2 and L3 are MAJOR, disposed DRAFT.
  - Draft 6:919: *"the ten minor corrections. Is each of L2, L3 and L5–L14"*.
  - SHEET:610-619 (RUNNER-FAULT; the experiment *"discarded whole and repeated, as an interrupted one is"*).
  - RULINGS:442-443 (As kept).
- **Evidence (MEASURED).**
  - Amendment 4's adopted classify (SHEET:499-504, fixed under F2) had four classes.
  - Under it, REREAD-5 measured a front-end refusal as NO-REFERENCE-RESULT and budget `-1` as RESULT (REREAD-5-REPORT:279, 282).
  - Now both are RUNNER-FAULT (ref_run_paths, reproduced): a new outcome outside the classes, with a new consequence, a voided experiment.
  - His N3(3) speaks of interrupted experiments only.
  - A deterministic runner fault recurs on every repetition, and nothing ends the loop. Examples: decoder1 holding a plant, or a frozen text the front end refuses after an environment change.
- **Proposal (ASK).**
  - (i) Did "Yes. Adopt…" adopt L2's and L3's DRAFT rows?
  - (ii) Is a runner fault to be handled as an interrupted experiment?
  - (iii) What ends a runner fault that recurs? For example: stop and report to him after one repetition.
  - Correct "the ten minor corrections" in draft 6 (:11, :905, :919).

### M3 — MINOR. W5's naming of absorbed clauses is ambiguous, and the checker is inconsistent
- **Text and code.**
  - W5 row (:509): *"each absorbed clause is named by exactly one arm or else of exactly one such If"*, and *"still names the clauses it does name, for both of the children rules"*.
  - Phase 3 (:608-609): *"The clauses it does name are still named"*.
  - `format_check.py:669-675`: in a chain naming a missing clause, every part, the first arm included, names an absorbed clause.
  - `format_check.py:680-695`: in a sound chain, only the later arms and the else do.
- **Evidence (MEASURED).**
  - P1 (`probe_w5.py`): a first arm names absorbed clause 2. The checker gives W5 line 4 ("in no If chain"). Counting the first arm, as the text reads, gives W5 line 5.
  - P2: the same, its else naming 99. The checker gives W4 line 5. Not counting the first arm, the checker's own sound-chain reading, gives W5 line 4.
  - So the checker is wrong under either reading on one of P1 and P2.
  - On R6: counting first arms changes 61 of 10,000 verdicts, all swap mutants (`w5_variants.py`, `w5_v1_ops.py`). The opposite reading for bad chains changes 0 (`w5_v3.py`).
  - Separately, a W4 chain whose later arm names an absorbed clause on an earlier line: the checker gives W4 line 5. The W5 row read narrowly gives W5 line 4. 0 mutants differ (`w5_v4.py`).
  - None of the three is planted: 0 of 71 raw plants and 3 byte fixtures change (`w5_v4_plants.py`).
- **Proposal.**
  - W5 names the parts that name an absorbed clause, the same in sound and W4 chains, and the row and phase 3 say it alike.
  - Make the checker consistent and plant each case.
  - Re-make `r6-checker`.

### M4 — MINOR. N3's narrow reading is pinned for blocks only
- **Text and code.** :509: *"its parts name nothing here"*. The single N3 plant (:831-832). `plant_reverts.py:116-123` undoes blocks only.
- **Evidence (MEASURED, `w5_variants.py` V2).** An inline if's else names absorbed clause 2. The checker gives W5 line 4. Letting inline ifs' arms and else name gives W7 line 5. Under that undoing, 0 of 71 raw plants and 0 of 10,000 mutants change.
- **Proposal.** Plant this law, and undo it in `plant_reverts.py`.

### M5 — MINOR. The write-back mode leaves three guesses
- **(a) The exhaustion kind of a load failure.**
  - :684: *"Running out of memory while reading or loading LAW is resource exhaustion (kind `law`)"*.
  - :738: *"`RESOURCE-EXHAUSTED: law` (or `stack`, if a stack the load uses fails)"*.
  - `stack` means the explicit stacks (:709), and §0 (:74-76) defines those for performs and rule uses only. No load stack is defined.
  - Under N3(b) a kind difference is UNSTABLE-CORE, so the kind must be fixed.
- **(b) Arguments beginning with `--`.** A positional beginning with `--` is a usage error in the run mode (:671). Write-back says only *"any other arguments"* (:728).
- **(c) The CORE-FAULT example.** Amendment 2's CORE-FAULT example *"exit 0 without a receipt"* (SHEET:202) is the written-back row's normal end. Amendment 5 says the write-back's classes are *"as Amendment 2 defines them"* (SHEET:580-581).
- **Proposal.**
  - Write-back's load failure reports `law` only, in both modes.
  - A `--`-prefixed positional is a usage error in both modes.
  - Amendment 5 says files are judged against the written-back row.

### M6 — MINOR. L2's correction is incomplete
- **Text.** SHEET:601-603 gives the adjudicator the draft only. Yet section 8 rests on SPEC:
  - W9 (:529): *"`as`, `rounded`: SPEC §5's table"*;
  - the promote rule (:546): *"exactly as SPEC §5 promotes"*;
  - section 7's numbering (:447): *"in SPEC §7's order"*.
- **Evidence.** The R6 checker record counts 33 W9 and 1,485 W8 verdicts.
- **Proposal.** Give the adjudicator the core author's whole reading set, by sha256.

### M7 — MINOR. ref_run_paths.py holds the runner's endings, not its docstring
- **Text and code.**
  - `ref_run.py:28-29` (the ENV line) and :35 (*"sets no recursion limit, never imports format_check, reads no clock and no environment variable"*).
  - `ref_run_paths.py:117-119` checks only the class, the exit status and stderr.
  - SHEET:622: *"runs every way the runner ends"*.
- **Evidence (MEASURED, `mutate_runner.py`).**
  - Five copies each pass with *"REF-RUN PATHS HELD: 25 of 25"*:
    - the ENV line removed;
    - `sys.setrecursionlimit(100000)`, which C2(a) forbids;
    - `format_check` imported;
    - P keeping the text-seal line;
    - BUDGET read from an environment variable.
  - The P change would show in regenerated RESULT rows. The first three would show only in r6-reference's header ENV lines, which nothing compares.
- **Evidence (MEASURED, `runner_paths6.py`).**
  - decoder1's import failing ends exit 1 with `REFERENCE-EXCEPTION builtins.ModuleNotFoundError`, classed NO-REFERENCE-RESULT. That is a setup fault classed as the reference's crash, unlike "decoder1 holds a plant".
  - A reference ending 3 with no line is classed RUNNER-FAULT.
  - `os.abort()` ends 3221226505 (0xC0000409) and is classed NO-REFERENCE-RESULT.
  - Neither `ref_run.py` nor `gen_r6_reference.py` checks decoder1.py against its pinned sha256. The generator only records it (:131).
- **Proposal.**
  - `ref_run_paths.py` checks the ENV fields: the default recursion limit, and `format_check not-imported`.
  - The runner checks decoder1.py's sha256. A mismatch, or an import failure, is a RUNNER-FAULT.
  - Add these endings as cases.

### M8 — MINOR. The precedence's stated reason omits F1(b)'s text
- **Text.** :629-630: *"Between the chain and structure gates no adopted rule orders"*.
- **Evidence.** The adopted F1(b) option text (REREAD-4-DISPOSITION:117) reads *"a third gate, after the depth gate and the chain gate"*. His F1 words set that order aside (*"deliberately unsettled"*, RULINGS:340), and N1 decides it (:402).
- **Proposal.** The rule stands. The reason should cite F1(b)'s text, his unsettling of it, and N1, as L1 asked of E1(b).

### M9 — MINOR. Records not kept current
- SHEET A4:524-525, *"It changes no class"*, has no in-place note, though L12 proved it false.
- SHEET:475-477 still names draft 5's R2b checker record (`89b5b886`). `evidence/rust-core-r2b-checker-6.txt` (`48d62f24…`, reproduced) is named nowhere.
- L1's DRAFT row (REREAD-5-DISPOSITION:75) says draft 5 §8 would be corrected in place. Draft 5 is unchanged (`f6e871b9`), and :139-140 of the same document says the drafts stay as they are.
- `r6-reference-2.txt` line 1 says *"SHEET.md Amendment 4"*.
- Draft 6:864-865, *"In draft 5, W4 at line 3, above"*, gives no draft-6 expectation.

### M10 — MINOR. "written back exactly: 304 of 304" is the pass count
- **Code and text.** `format_check.py:1560-1565, 1575, 1616` never calls `write()` on the 304 laws. Draft 6:796 says *"it writes them back"*.
- **Evidence (MEASURED, `writeback_claim.py`).** With `write()` appending "X", the checker still prints *"written back exactly: 304 of 304"* and *"304 of 304 laws pass and come back exactly"*. The run fails only through the byte fixtures and 10 plants.
- **Proposal.** Compare `write(L)` with the bytes for every law.

## Files created
All files are in `⟦HOME⟧\AppData\Local\Temp\reread6\` (short form `⟦HOME83⟧\AppData\Local\Temp\reread6\`).
- **Scripts:** `probe_w5.py`, `gates_big.py`, `dbg_c.py`, `dbg_c2.py`, `budget_probe.py`, `w5_variants.py`, `w5_v1_ops.py`, `w5_v3.py`, `w5_v4.py`, `w5_v4_plants.py`, `r6_sample.py`, `runner_paths6.py`, `mutate_runner.py`, `chains6.py`, `fuzz6.py`, `phase3_diff.py`, `writeback_claim.py`, `appendix_a.py`, `ties6.py`.
- **Outputs:** `fc_run1.txt`, `fc_run1.err`, `fc_run1.lf`, `ev6_body.txt`, `pr_run1.lf`, `pr_run1.err`, `ev6r_body.txt`, `rrp_run1.lf`, `rrp_run1.err`, `evrrp_body.txt`, `budget_probe.out`, `w5_variants.out`, `w5_v1_ops.out`, `w5_v3.out`, `w5_v4.out`, `w5_v4_plants.out`, `r6_sample.out`, `runner_paths6.out`, `mutate_runner.out`, `fuzz6.out`, `writeback_claim.out`, `appendix_a.out`, `ties6.out`.
- **Regenerated files:** `r2b-twins.regen.txt`, `r2b-checker.regen.txt`, `r6-checker.regen.txt`, `stress-texts.regen.txt`, `r6-reference.regen.txt`, `r6-reference.regen.log`.
- **Folders made and removed:**
  - `rr6budget-*`, `rr6r6-*`, `rr6paths-*`, `rr6app-*` and `mut_runner`, all in the scratch folder;
  - the tools' own `refrunpaths-*` and `r6ref-*`, in the system temp folder.
- Nothing was written in the repository.

## Appendix: the commands and outputs behind the findings
```
# reproduction (from the repository root)
python -B research/rust-core/format_check.py | tr -d '\r'   -> identical to evidence body; "plants 84 of 84 caught"
python -B research/rust-core/plant_reverts.py               -> identical; "PLANT REVERTS HELD: 35 ... 6 of them only by a crash"
python -B research/rust-core/ref_run_paths.py               -> identical; "REF-RUN PATHS HELD: 25 of 25"
python -B research/rust-core/gen_r6_reference.py --out <tmp> -> "NO-REFERENCE-RESULT 632, REFERENCE-REFUSED 6994, RESULT 2374; sha256 e2483cf5..."  R6REF_IDENTICAL (26 min)
r6_sample.py                -> "242 mutants re-run twice; rows identical 242, differing 0, runner faults 0"

# N1 (Q1)
phase3_diff.py 40000 66 / 67 -> agrees 40000, differs 0 (each seed); RR6_DRAFT5_RULE=1 control: differs 4406
gates_big.py (N=300000)      -> A W14 line 300026; B W14 line 28 (5.25 s); C W4 line 300002; D W5 line 300002; E W14 line 300018
fuzz6.py 60000 6             -> assertions 0; crashes 0

# M1 / M10
writeback_claim.py -> "read, W1-W14 passed, written back exactly: 304 of 304" with write() broken; the run fails only via byte fixtures and plants (74 of 84)

# M2
ref_run_paths: "text: a text the front end refuses ... RUNNER-FAULT"; "usage: budget -1 ... RUNNER-FAULT"
REREAD-5-REPORT:279  text mode, a text the front end refuses  NO-REFERENCE-RESULT ; :282 a negative budget RESULT

# M3 / M4
probe_w5.py:  P1 W5 line 4 (absorbed clause 2 is in no If chain); P2 W4 line 5
w5_variants:  V1 probe W5 line 5; V2 probe W7 line 5; raw plants changed none; R6 differing V1 61, V2 0
w5_v1_ops:    differing by operator [('swap', 61)]; checker message 'absorbed in no If chain' 61
w5_v3:        P2 V3 W5 line 4; R6 differing 0
w5_v4:        probe checker W4 line 5, V4 W5 line 4; R6 differing 0
w5_v4_plants: V1 and V4: 74 raw plants and byte fixtures, changed none

# M7
mutate_runner.py: ENV line removed / recursion limit 100000 / format_check imported / P keeps text-seal /
                  budget from env -> each "REF-RUN PATHS HELD: 25 of 25"; old except SystemExit restored -> "FAILED: 24 of 25"
runner_paths6.py: os.abort() exit 3221226505 -> NO-REFERENCE-RESULT; os._exit(3) -> RUNNER-FAULT (exit 3 without its line);
                  import decoder1 fails -> exit 1 REFERENCE-EXCEPTION builtins.ModuleNotFoundError -> NO-REFERENCE-RESULT;
                  MemoryError -> NO-REFERENCE-RESULT

# Q5
budget_probe.py -> "60 runs, 0 mismatches"
chains6.py      -> perform chain 100000 and rule chain 100000 accepted, written back exactly (recursion limit 1000)
appendix_a.py   -> A.1-A.4: checker accepts, written back exactly; law seal, receipt and trace equal to the draft's
ties6.py        -> W5/W7 one line: W5; W4/W5 one line: W4; depth with earlier chain and W7: W14 at the least depth line

# timings are software timings (perf_counter / time), not measurements of any core
```
