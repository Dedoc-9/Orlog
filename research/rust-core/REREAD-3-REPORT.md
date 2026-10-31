> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-3: the targeted independent re-read of LAW-FORMAT-0 draft 3, its checker and SHEET Amendment 2, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document, the checker or
the sheet. Its brief:
- read draft 3 (sha256 `4947bdec…`) whole, appendix A included, and draft 2 for the changes; RULINGS.md's B1 and
  REREAD-2 sections; SHEET.md with Amendments 1 and 2; REREAD-2's report and dispositions; `format_check.py` and its
  recorded run; `gen_s3_budgets.py` and `s3-budgets.txt`; SPEC.md, RUNTIME-SPEC.md, and `src/orlog/` for
  faithfulness;
- never open `research/law-sufficiency/` (it could run the two scripts that import their corpus from there);
- write nothing but one output of `gen_s3_budgets.py` under the system's temp directory, and run only read-only
  commands;
- cover, in the owner's words, *"the four original B1 requirements and these new corrections"*;
- answer draft 3's Q1–Q8 with evidence, and list its findings, J1 onward, by severity.

Its report follows, unedited, taken from its own transcript rather than retyped. Its section "Files created" discloses
one file beyond the brief, outside the repository; see REREAD-3-DISPOSITION.md.

---

LAW-FORMAT-0-DRAFT-3.md read: sha256 `4947bdec26cbd939ace5d640a3257c6edd306d42beed8f5adeccdb50a2250485`

# REREAD-3: an independent re-read of LAW-FORMAT-0 draft 3, its checker and SHEET Amendment 2 (2026-10-30)

## What I read, what I ran, and what I could not check

**Read in full:**
- `research/rust-core/LAW-FORMAT-0-DRAFT-3.md`, appendix A included, plus a `diff` against draft 2.
- `RULINGS.md` (the B1 section and the REREAD-2 section).
- `SHEET.md` (sections 1–9, with Amendments 1 and 2).
- `REREAD-2-REPORT.md` and `REREAD-2-DISPOSITION.md`.
- `format_check.py` (sha256 `6ae82f52…3422`) and `evidence/rust-core-format-3.txt`.
- `gen_s3_budgets.py` (sha256 `adb50cf0…`) and `s3-budgets.txt`.
- `src/orlog/interp.py`.

**Read in part:**
- `SPEC.md`: §1–§9, §11 and §12.
- `RUNTIME-SPEC.md`: §4–§9.
- `syntax.py`: its limits and `ast_depth`.
- `front.py`.
- `arbiter.py`, for how it runs the reference.

**Ran, read-only:** I ran everything from the repository root at HEAD `2e9805a`, in Git Bash on Windows 11 with CPython 3.14.5, as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, with scripts fed on stdin. Every run that tests the reference's recursion ran in a process that never imported `format_check`, at the default recursion limit of 1,000. Commands and outputs are in the appendix.

**Files created:**
- `s3-budgets.repro.txt` in my session's scratchpad, the one file the brief allowed.
- **A slip, disclosed.** I also redirected one run of `format_check.py` to `fc-run.txt` in the same scratchpad, so I could diff it against the evidence. That file is outside the repository, but it is a second file the brief did not allow.
- The tool harness saved one long output in its own folder.
- No repository file was created or changed: `git status` is as it was at the start, and HEAD is still `2e9805a`.

**Could not check:**
1. **`decoder1`, and anything else under `research/law-sufficiency/`.** I did not open those files. `format_check.py` and `gen_s3_budgets.py` import their corpus from there when they run. So I could not see whether `decoder1` refuses mutants, or whether it changes Python's recursion limit (J3).
2. **Any core.** None exists. What a Rust process does on a panic, a stack overflow or an aborting allocation is Rust's documented behaviour, NOT MEASURED.
3. **Linux.** Nothing was run there.
4. **The 298 texts at R5's half budget.** I did not run them all. I ran the fixtures that live under `tests/` (J2).
5. **S1's and S2's texts.** The sheet does not fix them, so they could not be reproduced (J4).

## Verdict

Draft 3, its checker and SHEET Amendment 2 are **not ready**: the format should not go to the clean-room author yet, and the protocol should not be used for experiments yet.

- **0 BLOCKER.**
- **6 MAJOR: J1–J6.**
  - J1 and J6 are in the document.
  - J2–J5 are in the comparison protocol.
- **11 MINOR: J7–J17.**
- **17 in all.**

**What holds (measured here unless marked):**
- **Termination (Q1).** The reasoning is complete and right. Seven more attempts at recursion or unbounded loops through the format were each refused.
- **Budget (Q2).** The reference's stop equals section 5's positions. I tested 11 laws at every B from 0 to ops + 1, with 0 mismatches. That covers stops inside a While body, a performed body, a block and an absorbed else's block; before an inline arm, an inline otherwise and an absorbed arm's inline statement; and at a define, a procedure and a decimals clause. No sentence redefines the budget.
- **Explicit stacks (Q3).**
  - They are stated as implementation obligations.
  - Nothing in the document, the sheet or the checker limits chains: the checker accepts perform and rule chains of 100,000 at the default limit.
  - Syntactic depth is kept apart from execution nesting.
  - The checker refuses a 300,000-deep tree in 6.5 s without crashing, and its time is linear in depth.
- **Recursion limit.** The checker no longer raises it: it reads 1,000 after import, and nothing in `src/` or the checker calls `setrecursionlimit`.
- **The reference as shipped.** In a process without the checker, perform and rule chains of 300 complete (`ops 301`). Chains of 600 and 3,000 raise `RecursionError`.
- **S3.** `s3-budgets.txt` reproduces byte for byte (sha256 `86f3a7b0…`). Recomputing it from the sheet's own words gives 0 differing rows. All 298 texts are RESULT: 237 completed, 61 refused, 2,100 values.
- **H-findings.** H1 and H3–H15 are resolved, with residuals named below. H2's crash is resolved. Its claim that the reported refusal is unchanged is false (J1).
- **Appendix A.** A.1–A.4 reproduce: law bytes, seal words, receipt without its `text-seal` line, and trace. The checker's run equals the recorded evidence: 304 of 304 laws, 52 of 52 plants.

**What must change before handoff:**
- **J1.** Phase 3's depth cap changes the reported (line, W). The document's proof that it does not is wrong, and four laws show it.
- **J6.** Section 0's list of fallibly allocated stores omits the law's own storage, while section 10 gives that kind (`law`) its own exhaustion report. One sentence also promises what the owner's correction forbids.

**What must change before the experiments:**
- **J2.** R5's falsifier fails a correct core: on E16a and E16b the reference completes at half budget.
- **J3.** R6 leaves open the reference's own refusal, its seed value, its mutation procedure, its budget and decoder1's identity.
- **J4.** S1's falsifier, read with Amendment 2's "Elsewhere", does not fail a core that load-refuses or exhausts at depths 600 and beyond. S1's and S2's texts are not fixed.
- **J5.** Two boundaries of CORE-FAULT rest on evidence the protocol does not fix in advance: the core's own claim of exit 5, and the "evidence" of a host's kill.

---

## Q1. Termination

**Is section 5's reasoning complete and right?** Yes (draft3:244-264).

- **Performs.** W6 makes procedures top-level, and W11 requires P < U with U outside P's body. Inside Q's body, Q is U's top-level ancestor. P is top-level, P ≠ Q, and P < U. A top-level clause between Q and U would have to lie in Q's subtree, so P < Q. Procedure ids strictly decrease.
- **Rules.** For a use of r in a define d of s, L(r) < d ≤ L(s).
- **Expressions** hold no perform, so the combined graph is acyclic.
- **Loops.**
  - A While refuses past N ≤ 2^62 (`interp.py:219-228`).
  - A For breaks at `hi` (`interp.py:233-241`), so −2^63…2^63−1 is 2^64 iterations, as the draft now says.
- **Uncounted work.** Every loop iteration, perform and rule use counts at least one operation (`interp.py:222, 235, 243, 424`).

**Attempts, each refused (C15):**

| attempt | refused |
|---|---|
| perform P from an absorbed arm's inline statement inside P | W11 line 4 |
| perform P from the inline otherwise inside P | W11 line 4 |
| P's body performs a later Q, and Q performs P | W11 line 4 |
| a perform from an absorbed else block placed outside P's body | W5 line 4 |
| a rule's proviso using a rule defined after it | W10 line 3 |
| a rule used in a procedure body, its last define between the procedure and the use | W10 line 5 |
| a While bound of 2^62 + 1 (2^62 itself accepted) | W13 line 5 |

**A note, not counted.** SPEC §7 makes `ops` a u64, and the draft's own example of 2^64 For iterations would take ops past 2^64 − 1. That is unreachable in practice, as REREAD-2 said.

## Q2. Budget preservation

**The positions equal the reference.**
- `seq` calls `stmt` for each non-absorbed clause (`interp.py:132-141`).
- `body` calls `stmt` for an inline arm or else statement (143-147).
- `stmt` checks `ops > budget` (151-152) before the do-nothing return (153-154).

This is draft3:308-316.

**Measured (C5).** For each law, the reference's stop was compared with the first check position, by the document's list, at which ops > B. I recorded those positions by instrumenting `seq` and `body` in an unbudgeted run. Every B from 0 to ops + 1 was tried, with **0 mismatches**. Samples:

| law | B | the reference |
|---|---|---|
| stop inside a While body: `Let n be 0. While n < 100, at most 200 times: increase n; say n. Say 7.` | 3 | STOPPED after 5 at the check before §2.2, last event `2 A 3` (unbudgeted: COMPLETED ops 504) |
| inside a performed body: `To p: say 1; say 2. Perform p. Say 3.` | 1 | STOPPED after 2 before §1.2 (clause 3), last event `1 S 2` |
| inside a block: `If true, do the following: say 1; say 2. Say 3.` | 1 | STOPPED after 2 before §1.2 |
| inside an absorbed else's block | 0 | STOPPED after 1 before §2.1, 0 events: no check for the absorbed clause |
| before an inline arm statement: `If 1 plus 1 = 2, say 5. Say 6.` | 0–2 | STOPPED after 3 before the inline Say, which runs as clause 1, 0 events |
| before an inline otherwise | 0–2 | STOPPED after 3, as clause 1 |
| before an absorbed arm's inline statement | 0–3 | STOPPED after 4, as clause 2 (SPEC §11 item 18) |
| at a define / a procedure / a decimals clause, after `Say 1 plus 1` | 0, 1 | STOPPED after 2 at clause 2 in each |
| inside a For body | 2 / 3 | STOPPED after 3 at clause 3 / after 6 at clause 2 |

**The rest of the budget's account:**
- **Counting** is delegated to SPEC §7 (draft3:315-316). Section 5a's `and`, `or` and `not` rows equal `interp.py:310-317` and `340-345`.
- **The stop's report** (draft3:595) is `HostStop`'s message (`interp.py:38`).
- **No sentence redefines the budget or generalizes beyond the positions.** Draft3:317-323 derives its consequence from the positions and quotes his words. The withdrawn sentence survives only in the withdrawal note (draft3:323).
- **One derived sentence is incomplete (J15).** It lists the bodies a run can stop inside, and not the If's inline arm or else check.
- **The check at a do-nothing clause is observable only when nothing but do-nothing or absorbed clauses follows it (J15).** Elsewhere the next statement's check reads the same ops, and the trace is the same.

## Q3. Explicit stacks, and the depth bound

**The obligations:**
- **Stated as implementation obligations: yes.** Draft3:58-69 says *"These are implementation obligations, not language constructs"*. Draft3:278-280 covers chains, and draft3:282-285 and 429-432 keep W14 to how a law is written.
- **The host call stack** is bounded by a constant from W14's bounds alone (draft3:62-63), and the expression evaluator must not recurse through a rule use (draft3:59-61).

**No limit on chains:**
- The document: W14 bounds the clause tree and the parentheses of a line, and W10 and W11 add none.
- The sheet: S1's depths are test points.
- The checker (C11), at the default limit:

| law | size | result | time |
|---|---|---|---|
| perform chain of 100,000 | 7.7 MB | ACCEPTED, written back exactly | 2.3 s |
| rule chain of 100,000 | 6.1 MB | ACCEPTED, written back exactly | 2.3 s |
| 5,000 procedures, each perform under 22 nested If blocks | 7.8 MB | ACCEPTED, written back exactly | 2.9 s |

**The reference as shipped (C10):** in a fresh process without the checker, at limit 1,000, chains of 300 give COMPLETED ops 301, and chains of 600 and 3,000 give `RecursionError`, for performs and for rules alike.

**Over-deep trees without crashing (C9):** 100,000 nested If blocks are refused W14 line 27 in 2.0 s, and 300,000 (20.9 MB) in 6.5 s. Time is linear in depth.

**Is the walk's bound shown to leave every reported (line, W) unchanged? No (J1).** The proof (draft3:533-538) covers failures *of* skipped parts. It misses failures of *walked* parts whose verdict depends on skipped parts.

How it breaks:
- Ids are numbered in walk order (draft3:396-407).
- The inline statements of an If's later arms and else are written on the If's own line, but walked after the first arm's block.
- So a declaration on an early line is numbered after declarations deep in the block.

The checker's answer, beside the answer of the whole tree walked plus W14(a) (C6):

| law (an If on line 3 whose block is 25 nested If blocks; a statement at depth 26; an absorbed clause 27) | walk capped at 25 (the document, the checker) | whole tree walked |
|---|---|---|
| deep `let 0`, inline else `let 1` | **W8 line 3** | **W14 line 27** |
| deep `let 1`, inline else `let 0` | **W14 line 27** | **W8 line 3** |
| deep `claim 0`, inline else `claim 1` | **W8 line 3** | **W14 line 27** |
| deep `must 0`, inline else `must 1` | **W8 line 3** | **W14 line 27** |
| control: the same at depth 24 | ACCEPTED | ACCEPTED |

**What held (C7).** These gave the same (line, W) both ways:
- labels naming deep clauses, including a `given` label naming a later claim at depth 26 (W14 line 28 both ways);
- a variable declared at depth 26 and used at a later top-level clause (W14 line 27);
- a certificate naming a clause at depth 26;
- rule defines around the deep subtree, with a deep use (W14 line 28).

**Crashes and time:**
- **Crash (C8, J9).** Any ⟨n⟩ or label part longer than 4,300 digits raises `ValueError` (Python's int-string limit), in phase 1 and in `nat()` and `labelled()`.
- **Super-linear time (C9, J10).**

| input | measurements | growth |
|---|---|---|
| one rule, m defines each overriding the one before | 400: 0.06 s; 800: 0.43 s; 1,600: 3.44 s; 3,200 (174 KB): 26.5 s | cubic |
| the same, each overriding the one after | 800: 1.27 s; 1,600: 10.35 s | about 8× per doubling |
| n top-level inline Ifs | 5k: 0.15 s; 10k: 0.39 s; 20k: 1.15 s; 40k: 3.80 s (40k top-level Says: 0.53 s) | quadratic |
| a 200,000-part label in a 30,000-deep tree | 0.59 s | — |
| a line of 2,000,000 `cat` parts | 8.2 s | one point, so no claim of linearity |

## Q4. Detected exhaustion, external termination, core fault

**Kept apart from each other and from the language outcomes: yes, by observable criteria.** Draft3:599 and 606-621, and SHEET:191-207:
- RESOURCE-EXHAUSTED is exit 5 with its line and no receipt.
- EXTERNAL-TERMINATION is the harness's own 60 s kill, or a host act with recorded evidence.
- CORE-FAULT is any other end, including an end whose files or stderr contradict its row.
- UNSTABLE-CORE is two runs that differ.
- On the reference's side, NO-REFERENCE-RESULT and UNSTABLE are kept apart from both.

**Where two classes can still fold (J5):**
- **RESOURCE-EXHAUSTED and CORE-FAULT** are told apart only by the core's own claim. A core that turns a panic into exit 5 is classed RESOURCE-EXHAUSTED. Nothing in the milestone checks where an exit 5 comes from.
- **EXTERNAL-TERMINATION and CORE-FAULT** turn on "evidence it records ... (an operating system's record of a kill, say)", and no standard for that evidence is fixed before testing.

**Promising to catch nothing that cannot be caught: nearly.**
- Section 0 (draft3:68) and section 10 (draft3:620-621) disclaim it.
- Draft3:613-614 claims the obligations exist *"so that a law cannot drive the core to such an end"*. That is false under memory overcommit, and for stores the list omits (J6).

**Can an end pass merely because it stopped? On a RESULT case, no.**
- COMPLETED, REFUSED and STOPPED are compared.
- LOAD-REFUSED is a disagreement.
- USAGE-ERROR, IO-ERROR, RESOURCE-EXHAUSTED and EXTERNAL-TERMINATION are coverage failures.
- CORE-FAULT and UNSTABLE-CORE fail.
- A pair of runs with one result and one kill is UNSTABLE-CORE.

**Off RESULT cases:** only CORE-FAULT and UNSTABLE-CORE fail (SHEET:216-217). So a load refusal, a detected exhaustion or a kill there is not a failure unless the prediction's own falsifier names it. For S1 it does not name a load refusal (J4).

**Two smaller residuals:**
- The draft calls STOPPED *"not a language outcome"*, while the sheet scores agreement only by "a compared language outcome" (J12).
- A stale receipt from an earlier run is not excluded by the protocol (J13).

## Q5. The protocol

**Fixed before any experiment:**
- the reference runs as shipped: fresh `python -B`, `PYTHONHASHSEED=0`, the default limit and stack, no import of the checker, version and OS recorded (SHEET:179-190);
- the core's classes (191-207);
- coverage (209-213) and no pass for stopping (214-215);
- R6's 60-second limit (219-224);
- S3's procedure and values (226-247);
- the evidence records (249-256).

**`s3-budgets.txt` and `gen_s3_budgets.py` match the sheet:**
- **Reproduced:** sha256 `86f3a7b08f6713b240b3705fdf5fe3abb93b4d75de104fad7c5e194c4bb578bd`, equal to the sheet's (C3).
- **Recomputed independently** from the sheet's words (sorted ids, max = min(ops, budget), one `random.Random(20261030)` over the RESULT texts): 0 rows differ, 298 rows, 2,100 values, none capped (C4).
- **ENV line:** CPython 3.14.5, recursion limit 1000, `format_check` not imported.

**Not fixed, or wrong:**
- R5's values, and its falsifier, which fails a correct core (J2).
- R6's seed value, operators, proportions, budget and decoder1's identity, and the class of a reference that refuses (J3).
- S1's and S2's exact texts, and S1's falsifier under the new classes (J4).
- The standard of host evidence, and the provenance of exit 5 (J5).
- Fresh output paths per run (J13).
- R8's in-process reference, the per-run OS record, and what a crash must share to "reproduce" (J14).

## Q6. H1–H15

| | disposition | resolved? | evidence |
|---|---|---|---|
| H1 | the budget stated by its positions | **yes** | draft3:317-323. C5: 0 mismatches; stops inside a While, a perform, a block, before inline statements, at do-nothing clauses |
| H2 | linear depth pass; walk capped at 25; (line, W) unchanged; plants | **partly** | Checker: `format_check.py:669-681` (one pass), `981-988` (cap). 300,000-deep refused, no crash. Plants caught (evidence; C17). **The claim "(line, W) unchanged" is false: J1.** The two plants test "no crash" only, on chains where nothing else fails |
| H3 | ASK C1 → core fault, full coverage | **yes, with residuals** | SHEET:191-217; draft3:606-614. Residual J5 |
| H4 | ASK C2 → as shipped, unstable core, R6, S3 | **mostly** | SHEET:179-190, 219-247; S3 reproduced. Residuals J2, J3, J4, J13, J14 |
| H5 | the count defined; two plants | **yes; plants partial** | draft3:502-507 equals `paren_depth` (`format_check.py:66-87`). Plants W2 and W14, line 3. The escape rule is untested: J11 |
| H6 | W8 on `remove-last`; plant | **yes** | `format_check.py:970-973`. Plant W8 line 4. Before the fix W9 line 4 (REREAD-2 C6), so it discriminates |
| H7 | the later If's line; plant | **yes** | `format_check.py:655-662`. Plant W5 line 6. Before the fix line 4 (REREAD-2 C7), so it discriminates |
| H8 | no placement check on an underived type; plant | **yes** | `format_check.py:90-98, 702-711, 752-757, 843-846`. Plant W10 line 3. Before the fix W9 line 3, so it discriminates |
| H9 | sums by place | **yes** | draft3:508-520. Checked: 63+32 = 95; Unless 96; 3+96 = 99; inline 62+31 = 93 and 4+93 = 97. `ast_depth` (`syntax.py:79-93`, 412) puts the statement at 1 and its expressions at 2 |
| H10 | the measures; 2^64 | **yes** | draft3:244-264; Q1 |
| H11 | wording, constant, list of stores | **yes, one residual** | draft3:58-66, 278-280. Residual J6 |
| H12 | section 10's lost lines and edges | **yes, residuals** | draft3:557-604: every line REREAD-2 named is restored. Residuals J6, J12, J17 |
| H13 | lists, third G5 plant, docstrings | **yes** | draft3:648-678 equals the checker's 8 fixtures and 52 plants (13 + 9 + 22 + 8). Evidence: 52 of 52. Docstring line 9 states the checker's W4-or-W5 skip, which the document does not (J7) |
| H14 | W10's line column | **yes** | draft3:445. The checker uses the define's line |
| H15 | sha256s; item 18 | **yes** | `SPEC.md` `27dfff0c…6de5`, `RUNTIME-SPEC.md` `0bd571d6…ec35`, both matching; SPEC.md:341 is item 18 |

## Q7. The checker against sections 2–4 and 8

**Phase 1** is as written: line by line, each line completely, the prefix byte by byte (`format_check.py:446-482`). An empty input is W1 line 1; a missing final LF belongs to the last line; the ancestor walk is amortized linear.

**Phase 2** is as written: W14(c)'s count, then W2, then W3 (485-495). The count equals draft3:502-507.

**Phase 3**, W by W:

| W | the checker against the document |
|---|---|
| W4 | as written. It crashes on a label part of more than 4,300 digits (J9) |
| W5 | **differs (J7).** It walks no block of a chain that fails **W4** (619-621, 884), where the document says W5 only (draft3:544-545). That is observable: W8 line 3 against W4 line 4. Such a chain also gets a spurious "has children and no body" (hidden behind W4 on the same line) |
| W6 | **differs (J8).** It judges a literal's mode by line 2 (694, 716), not by derivation "Decimals". That is observable: W6 line 3 against line 4 |
| W7 | as written |
| W8 | as written, `remove-last` included |
| W9 | as written, H8 included |
| W10 | as written |
| W11 | as written |
| W12 | as written |
| W13 | as written, but it crashes on a number of more than 4,300 digits (J9) |
| W14 | as written. The cap is as the document says, but the document's equivalence claim is false (J1) |

**Re-run (C17).** The run's output equals the evidence's body with CRs stripped: 304 of 304 laws, derivations equal, 52 of 52 plants.

## Q8. What a clean-room author would still have to guess

1. Which failures phase 3 collects: those of the capped walk, or of the whole tree (J1).
2. Which stores must grow by fallible allocation, and whether loading LAW is among them (J6).
3. Under which mode a decimal literal is judged when line 2 and the `decimals` clause disagree (J8).
4. Whether SPEC §9's and item 61–62's "the law's bytes are defined by `sema.py`" binds them (J16).
5. What stdout may hold, and whether LAW may equal an output path (J17).
6. **Not counted:**
   - a ⟨n⟩ and a u32 event field for a law of more than 2^32 clauses;
   - `ops` past 2^64 − 1.

   Both are unreachable in practice.

---

## Findings

### J1 — MAJOR: phase 3's depth cap changes the reported (line, W), and the document says it does not
- **Document:**
  - draft3:529-530: *"Phase 3, among every failure of W4–W14 (W14(c) excepted): the one on the least line"*.
  - draft3:532-538: *"The walk enters no clause deeper than 25. … The reported (line, W) is the same as if the whole tree were walked"*, proved by "every clause it skips … lies on a later line" and "every line this table gives a failure of a skipped part is later still".
  - draft3:396-407: ids numbered by the walk.
- **Evidence (C6):** four laws, in the table under Q3. The cap moves the report from W14 line 27 to W8 line 3, or the reverse, through variables, claims and musts.
  - **The mechanism.** The inline statements of an If's later arms and else are written on the If's own (early) line but walked after the first arm's block. Their ids count declarations inside that block, skipped ones included.
  - **The gap in the proof.** It considers failures *of* skipped parts, never failures of walked parts that depend on them.
  - **The plants.** No plant tests the claim: H2's two plants are plain chains.
  - **The ruling.** The owner accepted H2 on this premise (*"Accept H2's bounded checker walk"*; the disposition: *"The reported (line, W) is unchanged"*).
- **Proposal (owner's choice):**
  - (a) Define the failure set as that of the capped walk: "the walk of section 7, and so the numbering of ids, does not enter a clause deeper than 25". Delete the equivalence claim and its proof. The checker already does this. Or:
  - (b) Make W14(a) and (b) a gate before W4–W13. That changes the precedence for laws with an earlier W4–W13 failure.
  - Either way, plant the four laws above.
  - Note in the document that G8's skip (draft3:544-545) has the same cross-line effect by definition (J7's law).

### J2 — MAJOR: R5's falsifier fails a correct core
- **Sheet:** SHEET:93, R5: *"under a budget of half each text's operations (texts of 2 operations or more), it stops where the reference stops: same count, no receipt | a different count, or a receipt"*. Amendment 2 keeps "compared as R3–R5 say" (SHEET:210-211).
- **Evidence (C14):**
  - `tests/fixtures/redteam/E16a_upper_to.orl` and `E16b_to_two_spaces.orl` are among the 298 (`s3-budgets.txt`: ops 2).
  - At B = 1, the reference gives **COMPLETED ops 2, with a receipt**. The only check after ops reaches 1 is before §1.1, where ops is 1, not more than 1.
  - A correct core writes a receipt, and R5's falsifier ("a receipt") fires.
  - `self_store.orl` (ops 14, B = 7) stops after 9, as R5 expects.
  - "Half" is not given a rounding, and R5's values, unlike S3's, are not fixed in a file.
- **Proposal:**
  - R5 compares class and result as Amendment 2 does: a stop with the same count and trace, or a completion or refusal with the same P and trace.
  - B = ⌊ops/2⌋, with ops from the RESULT run under the text's own budget.
  - List R5's values in a hashed file, as for S3.

### J3 — MAJOR: R6 is not fixed, and a reference refusal has no class
- **Sheet:**
  - SHEET:94, *"10,000 mutated law byte strings (bytes flipped, lines truncated, clauses swapped, ids changed; seed fixed)"*.
  - SHEET:161-162, *"An accepted mutant is compared as above, with decoder1 and the interpreter as its reference"*.
  - SHEET:130-136, the reference's classes RESULT, NO REFERENCE RESULT, and UNSTABLE as *"anything else"*.
  - SHEET:216-217, off RESULT only CORE-FAULT and UNSTABLE-CORE fail.
- **Evidence:**
  - "seed fixed" has no value (`grep -n seed SHEET.md`: only S3's 20261030).
  - decoder1 is named by neither path nor sha256.
  - Nothing states the operators' proportions, the source texts, or the budget for mutant runs.
  - A mutant decoder1 refuses has no P, so it is not RESULT. By the table's letter it is UNSTABLE (or NO-REFERENCE-RESULT, if the refusal is an exception). Either way, a core that **accepts** a mutant the reference refuses is only "stress evidence", while the owner's condition 3 says *"accepted only if its execution agrees with the decoded reference"*.
  - Whether decoder1 refuses canonical bytes the core could accept: **could not check** (`research/law-sufficiency/` not opened). If it can, the protocol scores a falsifying case as no failure.
- **Proposal:**
  - Add a reference class, REFERENCE-REFUSED: both runs refuse, with the same code.
  - State R6's outcome table: core refuses and reference refuses, agreement; core refuses and reference RESULT, recorded "refused" (his condition 3); core accepts and reference refuses, **falsifier**.
  - Fix the seed's value, the operators and their counts, the source texts, the budget, and decoder1's path and sha256. Better: fix the 10,000 mutants themselves as a hashed file.

### J4 — MAJOR: S1's falsifier misses a chain limit imposed as a refusal; S1's and S2's texts are not fixed
- **Sheet:**
  - SHEET:168, S1: *"The core completes each … | a crash, a detected exhaustion or external termination at any of these depths, or a difference at 300"*.
  - SHEET:216-217: *"On a case whose reference class is NO-REFERENCE-RESULT or UNSTABLE, the core's class is recorded as stress evidence. A CORE-FAULT or UNSTABLE-CORE there still fails"*.
  - SHEET:256 bans "crash" as a class word.
- **Evidence:**
  - C10: at the shipped limit, chains of 600 and 3,000 give `RecursionError`, so S1's depths 600, 3,000 and 30,000 will be NO-REFERENCE-RESULT.
  - There, a LOAD-REFUSED (a chain limit as a load refusal: what B1 forbids), a REFUSED or a STOPPED is in neither S1's falsifier list nor Amendment 2's failing classes. Only S1's prose ("completes each") excludes them.
  - "A crash" is not mapped to CORE-FAULT.
  - Beyond 300 nothing checks the output, though it is known by construction. At 300, both chains give COMPLETED ops 301; a perform chain of n gives output `1` and ops n + 1, and a rule chain of n says `1` with ops n + 1.
  - S1's and S2's exact texts are not fixed. Whether S2's chains stop at budget 10 depends on a statement after the Say (REREAD-2's C3).
- **Proposal:**
  - S1's falsifier: any class but COMPLETED at any depth, or an output or ops other than the constructed one (n + 1).
  - Map "crash" to CORE-FAULT.
  - State that each stress prediction's own falsifier still applies off RESULT.
  - Fix S1's and S2's texts by a generator and sha256.

### J5 — MAJOR: two boundaries of CORE-FAULT rest on evidence the protocol does not fix
- **Sheet and document:**
  - SHEET:200, RESOURCE-EXHAUSTED: *"an allocation the core made by a fallible call failed, and the core said so"*.
  - SHEET:201, EXTERNAL-TERMINATION: *"on evidence it records with the case (an operating system's record of a kill, say)"*.
  - Draft3:618-619.
- **Evidence:**
  - The harness can observe only exit 5 and its line. A core whose panic handler prints `RESOURCE-EXHAUSTED: stack` and exits 5 is classed RESOURCE-EXHAUSTED. Off RESULT (S2 at 64, R6's non-RESULT mutants), that is not a failure, while the honest CORE-FAULT would be.
  - The milestone's acceptance (SHEET:260-262) includes no re-read of the core. One is required only before a production path (268).
  - What counts as "evidence" of a host act is left open, against his *"The time limit, repeat count, and classification rules must be written into the sheet before experiments begin."*
- **Proposal:**
  - Before testing, enumerate the admissible host evidence per OS. On the owner's Windows host, probably none, so every end the harness did not cause is CORE-FAULT.
  - Require, as a milestone condition, a reading of the core's source that exit 5 is reached only from a failed `try_reserve`-class call. Record that reading.

### J6 — MAJOR: section 0's list of fallible stores omits the law's storage, and section 10 promises what cannot be promised
- **Document:**
  - draft3:64-66: *"These stores grow only by fallible allocation …: the explicit stacks, lists, text values, the output buffer and the trace."*
  - draft3:580-581 and 599 give exhaustion while *"reading or loading LAW"* the kind `law`.
  - draft3:613-614: *"Section 0 forbids host recursion … and requires fallible allocation for the named stores, so that a law cannot drive the core to such an end."*
- **Evidence:**
  - A core that meets section 0 to the letter may read and load LAW (bytes, tree, derivation tables, the closure of derivation 5, the variable store, event payloads) by infallible allocation. On exhaustion it aborts: CORE-FAULT, not RESOURCE-EXHAUSTED (law). Off RESULT the two score differently (SHEET:216-217).
  - The sentence at 613-614 contradicts draft3:68 and the owner's B1 correction 2 (*"Do not promise that Rust can catch every possible process-level memory failure."*). Under memory overcommit a fallible call succeeds and the OS kills the process.
- **Proposal:**
  - List `law` (the bytes read and every structure built from them) in section 0, or say "every store whose size depends on the law or the run".
  - Replace the end of 613-614 with "so that such ends are not caused by the law's chains; where they occur they remain core faults".

### J7 — MINOR (checker): it skips the blocks of a chain that fails W4, which the document does not
- **Code:**
  - `format_check.py:619-621` (`if k in bad_ref: bad_chain.add(k); continue`) and 884 (`whole = … k not in bad_chain`).
  - The docstring at :9: *"no walk into a chain failing W4 or W5"*.
- **Document:** draft3:544-545, *"The walk enters no block of an If chain that fails W5"*. A W4-failing chain's shape check is "not made" (draft3:541-543).
- **Evidence (C12):**
  - The law: an If (line 3) whose block holds an inner If (line 4) whose block declares `let 0`, with the outer inline else declaring `let 1`.
    - With the inner chain sound: ACCEPTED.
    - With the inner else naming clause 99: the checker reports **W8 line 3**, where the document walks the block and reports **W4 line 4**.
  - REREAD-2's "Every reported result is unchanged" was wrong.
  - The skip also yields a spurious `(4, 5, 'clause 2 has children and no body')`, since no block is recorded for the chain.
- **Proposal:** decide in the document (W5, or W4 or W5), make the checker equal, and plant this law.

### J8 — MINOR: the mode a decimal literal is judged under is ambiguous when line 2 and a decimals clause disagree
- **Document:** draft3:441: *"Line 2's mode is derivation "Decimals". A `(lit fix …)` stands only under `fixed`, a `(lit float …)` only under `floats`"*. Derivation "Decimals" (draft3:388-389): *"Every decimal literal is of that mode."*
- **Code:** `format_check.py:694` (`dec_type` from line 2), 716.
- **Evidence (C13):** line 2 `(decimals fixed)`, a `(lit float …)` on line 3, then `(decimals floats)` on line 4.
  - The checker gives **W6 line 3**.
  - Under derivation "Decimals" the literal is of the law's mode, and the failures are the decimals line's: **W6 line 4**.
  - REREAD-2 called this unobservable.
- **Proposal:** say "under the mode of derivation Decimals" (or "of line 2"), make the checker equal, and plant the law.

### J9 — MINOR (checker): it crashes on any ⟨n⟩ or label part of more than 4,300 digits; G10 has no plant
- **Document:** draft3:135, 141-144: an ⟨n⟩ is *"of any length"*, compared as a number, and *"An id greater than any clause, variable or claim is that check's failure, not a parse failure."*
- **Code:** `int()` at `format_check.py:185` (`nat`), 471-472 (phase 1), 543 (`labelled`).
- **Evidence (C8):** Python 3.14.5's `int_max_str_digits` is 4300.

| input | expected | got |
|---|---|---|
| a 4,300-digit Int literal | W13 | W13 line 3 |
| a 5,000-digit literal | W13 | `ValueError`, uncaught |
| a 5,000-digit clause number | W1 | `ValueError` |
| a 5,000-digit parent | W1 | `ValueError` |
| a 5,000-digit while bound | W13 | `ValueError` |
| a 5,000-digit variable id | W8 | `ValueError` |
| a 5,000-digit perform target | W4 | `ValueError` |
| a 5,000-digit label part | W4 | `ValueError` |

  - `main()` catches only `RecursionError` (`format_check.py:1423`), so such a plant would end the whole run.
  - No plant tests an ⟨n⟩ above 2^63 or a very long one.
- **Proposal:**
  - Compare ⟨n⟩ by length and then by digits, or call `sys.set_int_max_str_digits(0)` inside `read`.
  - Plant a 5,000-digit literal (W13), clause number (W1) and label part (W4).

### J10 — MINOR (checker): super-linear time on many defines of one rule and on many sibling Ifs
- **Code:**
  - `format_check.py:991-1008`: a fixed point of set unions per pass.
  - 644-645: `sibs.index(k)` per If.
- **Evidence (C9):** the table under Q3: cubic in defines (3,200 defines of 174 KB take 26.5 s) and quadratic in sibling Ifs. The closure's own size is quadratic, so part of this is inherent to derivation 5 as a stored set.
- **Proposal:** a cycle check by depth-first search, the closure by memoized reachability, and sibling positions precomputed.

### J11 — MINOR: H5's plants do not test the string and escape rules of the count
- **Document:** draft3:502-507. **Plants:** `format_check.py:1301-1304`, neither holding a string.
- **Evidence (C18):** a line whose string holds `\"` and then 131 `(` is ACCEPTED and written back exactly. The checker's count is 3. A count that does not skip the byte after `\` gives 134, so it would be W14.
- **Proposal:** plant this line (accepted), and its twin with the 131 `(` outside the string (W14).

### J12 — MINOR: the document and the sheet name the stop and the unstable core differently
- **Document:**
  - draft3:595: stopped's kind is *"budget (the host's)"*.
  - draft3:603-604: *"It is the host's budget, not a language outcome, though it is compared"*.
  - draft3:629-630: *"Two runs of one case whose classes differ are an unstable core"*.
- **Sheet:**
  - SHEET:197, STOPPED *"a language outcome (the budget), compared"*.
  - SHEET:214-215: *"No outcome counts toward agreement but a compared language outcome"*.
  - SHEET:203: UNSTABLE-CORE *"differ in class or in result"*.
- **Evidence:**
  - Read with the document's taxonomy, the sheet's rule would never let a STOPPED count toward agreement, and so R5 and S3 could never pass.
  - Two COMPLETED runs with different P are unstable by the sheet, but not by the document's sentence.
  - UNSTABLE-CORE also sits in a table of classes for "every run" (SHEET:191), but it is a property of two runs.
- **Proposal:** one taxonomy in both. Say "a compared outcome (COMPLETED, REFUSED, STOPPED)" in SHEET:214. Add "or in result" to draft3:629, and make UNSTABLE-CORE a class of the case.

### J13 — MINOR: the protocol does not require fresh output paths per run
- **Document:** draft3:587-589: *"The core removes nothing, so a caller that wants no stale file removes it before the run, as the arbiter does"*.
- **Sheet:** Amendment 2 classes by *"the files written"* (SHEET:254), but nothing requires OUT, RECEIPT and TRACE to be absent before each of the two runs.
- **Evidence:** a second run that exits 0 without writing would find the first run's receipt, and could be read as COMPLETED. A stopped run could find a stale receipt and be read as CORE-FAULT. Either way an end could be scored as something it was not, against his *"never award a pass merely because execution stopped"*.
- **Proposal:** each run in a fresh empty folder, with its listing recorded before and after.

### J14 — MINOR: edges of "the reference as shipped"
- **Sheet:**
  - SHEET:179-185: every reference run is one fresh process, recording the OS *"and its release"*.
  - The ruling: *"A reference crash or timeout must reproduce in both runs"*.
- **Evidence:**
  - Phase 3 and R8 use *"the arbiter's own build and run"* (SHEET:77-79), and the arbiter runs `Interp` in its own process (`arbiter.py:330`), not a fresh one.
  - `s3-budgets.txt` records the OS once, from the parent, as `Windows 11`. That is `platform.release()`, not the exact build (`gen_s3_budgets.py:131-132`), and not one record per run.
  - `classify` (`gen_s3_budgets.py:78-83`) treats any two crashes as NO-REFERENCE-RESULT, whatever their exit status or exception. The sheet does not say what a crash must share to "reproduce".
- **Proposal:**
  - State R8's reference conditions.
  - Record `platform.platform()` from each child.
  - Define "reproduce" as the same exit status and exception type, or say explicitly "any crash".

### J15 — MINOR: the budget's derived sentence is incomplete, and the check before a do-nothing clause is untested
- **Document:** draft3:319-321: *"A check stands before each clause of a sequence, and the body of a `while`, a `for`, a `perform` or a `(block ⟨C⟩)` is run as a sequence … So a run can stop inside those statements"*. This omits the If's inline arm and else check (draft3:312), which also stops a run inside an If after its conditions are counted (C5, rows D, D2, D3).
- **Evidence:**
  - In C5's E, E2 and E3, the check at the do-nothing clause and the check at the next statement read the same ops. The stop's count and trace are then identical with or without the do-nothing check.
  - It shows only when such a clause is followed by no statement.
  - S3's "at the same statement" (SHEET:170) is not observable there, and no R7 plant (SHEET:98-105) targets this check, though his first correction names it (*"whether a do-nothing clause is counted"*).
- **Proposal:**
  - Add "or before an inline arm or else statement" to the sentence.
  - Add a fixture whose last clause is a procedure, a define or a decimals clause, and an R7 plant "no check before a do-nothing clause".

### J16 — MINOR: section 0 redirects the author away from `numeric_ref.py`, but not from `sema.py`
- **Document:** draft3:45-48 redirects numbers only.
- **Evidence:** SPEC.md:284 (*"the law's bytes, which `src/orlog/sema.py` (`law_bytes`) defines"*) and SPEC.md:410 (*"The law's bytes are defined by `sema.py`."*). These sit in the author's reading set and point to a file it forbids, as the definition of this very format.
- **Proposal:** add "SPEC §9 and §11 items 61–62 say the law's bytes are defined by `sema.py`. For you they are defined by this document."

### J17 — MINOR: section 10 leaves stdout and a LAW path equal to an output path unsaid
- **Document:** draft3:567-572 and 591-602. The rows and CORE-FAULT's *"files or stderr contradict its row"* (draft3:610) say nothing of stdout.
- **Evidence:** the author must guess whether anything may be printed on stdout, and whether that is a contradiction. LAW equal to OUT, RECEIPT or TRACE is no usage error, so the core would overwrite its own input after reading it.
- **Proposal:** "The core writes nothing to stdout, and anything there contradicts its row". Add "LAW equal to OUT, RECEIPT or TRACE, compared as the strings given" to the usage errors.

---

## Appendix: commands and outputs

All from `⟦HOME⟧\Desktop\Orlog`, in Git Bash, as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B -` with the script fed on stdin, unless marked otherwise.

**C1:**
```
sha256sum research/rust-core/LAW-FORMAT-0-DRAFT-3.md … evidence/rust-core-format-3.txt
→ 4947bdec…0485, draft 2 f3b6c2a0…7a5b, SHEET 2c6a3d00…06d1, RULINGS 7b2028a2…5049,
  format_check 6ae82f52…3422, gen_s3 adb50cf0…a8ac, s3-budgets 86f3a7b0…78bd, evidence 054e4b37…a8a2
sha256sum SPEC.md RUNTIME-SPEC.md vectors/runtime-vectors.txt research/rust-core/vectors-as-integer.txt src/orlog/interp.py src/orlog/numeric_ref.py research/rust-core/gen_worked.py
→ 27dfff0c…6de5, 0bd571d6…ec35, 841240b7…f204, 2bff1c69…ad2f, f8432918…4d27, eacac3dd…bb64, 163e54f4…b738   (all equal to the draft's)
wc -l: runtime-vectors 20015; vectors-as-integer 446 (f_as_i 268, x_as_i 178; INEXACT-CONVERSION 143, NOT-FINITE 6, OVERFLOW 40)
grep -n setrecursionlimit research/rust-core/format_check.py research/rust-core/gen_s3_budgets.py src/ → none
```

**C2:** `diff LAW-FORMAT-0-DRAFT-2.md LAW-FORMAT-0-DRAFT-3.md`. The changes are those of the draft's table. The appendix is unchanged.

**C3:**
```
python -B research/rust-core/gen_s3_budgets.py --out <scratchpad>/s3-budgets.repro.txt   (30 s)
→ GEN-S3: 298 texts; RESULT 298; 2100 values; envs 1; sha256 86f3a7b08f6713b240b3705fdf5fe3abb93b4d75de104fad7c5e194c4bb578bd
sha256sum of both files → equal
```

**C4:** tallies, and a recomputation from the sheet's words.
```
237 RESULT COMPLETED; 61 RESULT REFUSED; values 2100
rows 298 sorted by id: True distinct: True
values 2100 rows disagreeing with the sheet's procedure: 0 rows capped by the budget: 0
```

**C5 (Q2):** 11 source laws, compiled by `orlog.front.compile_bytes` and run by `orlog.interp.Interp`. Each was run unbudgeted with `seq` and `body` instrumented to record ops at the document's check positions, then at every B from 0 to ops + 1. `format_check imported: False limit 1000`. Every law: `mismatches vs the document's positions: []`. The samples are in Q2's table.

**C6 (Q3, the cap):** the checker, and the same law with `format_check.DEPTH_CLAUSE` raised to 10^9 during the walk, its W14(a) failures added back from the capped run.
```
let deep (var 0), inline else let 1   capped: W8 line 3 (variable 1 declared where 0 is next in the walk)   whole: W14 line 27
let deep (var 1), inline else let 0   capped: W14 line 27                                                   whole: W8 line 3
claim deep 0, inline else claim 1     capped: W8 line 3 (claim 1 where 0 is next in the walk)               whole: W14 line 27
must deep 0, inline else must 1       capped: W8 line 3 (must 1 where 0 is next in the walk)                whole: W14 line 27
control: depth 24 tree, same ids      ACCEPTED / ACCEPTED
```

**C7:**
```
let at depth 26, used at a later top clause                bounded W14 line 27  whole W14 line 27  same
given label naming a later claim at depth 26               bounded W14 line 28  whole W14 line 28  same
certificate naming a clause at depth 26                    bounded W14 line 27  whole W14 line 27  same
rule use deep, its define after; over naming another rule  bounded W14 line 28  whole W14 line 28  same
```

**C8:**
```
python 3.14.5 recursion limit 1000 int max str digits 4300
a 5,000-digit Int literal (W13 expected)     -> CRASHED: ValueError: Exceeds the limit (4300 digits) for integer string conversion …
a 4,300-digit Int literal (W13 expected)     -> refused W13 line 3
5,000-digit clause number / parent / while bound / variable id / perform target / label part -> CRASHED: ValueError (each)
```

**C9:**
```
top-level inline Ifs n=5000/10000/20000/40000: 0.15/0.39/1.15/3.80 s; top-level says n=10000/40000: 0.10/0.53 s
defines each over the one before m=100/200/400/800/1600/3200: 0.00/0.01/0.06/0.43/3.44/26.53 s (ACCEPTED)
defines each over the one after  m=100/200/400/800/1600: 0.01/0.03/0.15/1.27/10.35 s
nested If blocks n=100000 (6.7 MB): W14 line 27 2.03 s; n=300000 (20.9 MB): W14 line 27 6.49 s
a 200,000-part label in a 30,000-deep tree: W14 line 27 0.59 s; 2,000,000 cat parts: ACCEPTED 8.18 s
```

**C10:** the reference, with no checker in the process.
```
fresh process: format_check imported: False | recursion limit 1000 | python 3.14.5
perform chain 300: COMPLETED ops 301; 600: RecursionError; 3000: RecursionError
rule chain    300: COMPLETED ops 301; 600: RecursionError; 3000: RecursionError
```

**C11:** the checker, on raw bytes.
```
after import: recursion limit 1000
perform chain n=100000 (7,666,745 bytes) -> ACCEPTED, written back exactly True (2.3 s)
rule chain    n=100000 (6,066,750 bytes) -> ACCEPTED, written back exactly True (2.3 s)
perform chain, each perform 24 deep, n=5000 (7,771,509 bytes) -> ACCEPTED, written back exactly True (2.9 s)
```

**C12:**
```
inner If's chain sound:               ACCEPTED
inner If's else names clause 99 (W4): W8 line 3 (variable 1 declared where 0 is next in the walk)
  failures: [(3, 8, …), (4, 4, 'clause 99 does not exist'), (4, 5, 'clause 2 has children and no body')]
```

**C13:**
```
(decimals fixed) / (lit float …) line 3 / (decimals floats) line 4 → W6 line 3
  failures [(3,6,'a float literal in a law whose decimals are fixed'), (4,6,'a decimal literal before the decimals clause'), (4,6,"line 2's mode is not the law's")]
(decimals floats) / (lit fix 5) line 3 / (decimals fixed) line 4 → W6 line 3 (the same three)
```

**C14:**
```
tests/fixtures/redteam/E16a_upper_to.orl      unbudgeted ops 2; floor(ops/2) = 1: COMPLETED ops 2, a receipt
tests/fixtures/e21/self_store.orl             unbudgeted ops 14; floor(ops/2) = 7: STOPPED after 9
tests/fixtures/redteam/E16b_to_two_spaces.orl unbudgeted ops 2; floor(ops/2) = 1: COMPLETED ops 2, a receipt
```

**C15:** the results are the table in Q1.

**C16:** appendix A, rebuilt from source texts and run in the reference.
```
A.1–A.4: law bytes in doc: True | seal words True | receipt (minus text-seal) equal: True | trace equal: True
```

**C17:** `python -B research/rust-core/format_check.py`, stdout redirected to the scratchpad (the slip disclosed above). Exit 0. Its output equals `tail -n +5 evidence/rust-core-format-3.txt` under `diff --strip-trailing-cr`. Its last line: `FORMAT CHECK (DRAFT 3) HELD: 304 of 304 laws pass and come back exactly, derivations equal on 304; plants 52 of 52 caught, 0 not run`.

**C18:**
```
string holding an escaped quote then 131 '(': ACCEPTED, written back exactly True
the checker's count: 3 | a count that ignores the escape rule: 134
```

**C19, greps:**
- `grep -n -i budget` over the draft and the sheet: the sentences quoted in Q2, J2 and J12.
- `grep -n -i "decoder1\|seed" SHEET.md`: lines 94, 123, 161 and 170 only.
- `grep -n "sema.py\|numeric_ref" SPEC.md RUNTIME-SPEC.md`: SPEC.md:5, 269, 284, 296, 405, 406 and 410; RUNTIME-SPEC.md:4, 7 and 42.
- `git status --short` and `git rev-parse HEAD`, at the end: unchanged from the start, HEAD `2e9805aa…`.
