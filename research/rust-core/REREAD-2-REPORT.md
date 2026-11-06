> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on the ten older reports, by REREAD-9's ASK 9-2 procedure): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-2: the targeted independent re-read of LAW-FORMAT-0 draft 2 and its checker, its report word for word (2026-10-30)

Saved as returned by the re-reader, a fresh general-purpose agent with no part in writing the document or the checker.
Its brief:
- read draft 2 (sha256 `f3b6c2a0…`) whole, appendix A included; RULINGS.md's B1 section; SHEET.md's Amendment 1;
  REREAD-1's report and dispositions; `format_check.py` and its recorded run; SPEC.md, RUNTIME-SPEC.md, and
  `src/orlog/` for faithfulness;
- never open `research/law-sufficiency/`;
- write nothing, and run only read-only commands;
- verify specifically what the owner named (*"termination reasoning, budget preservation, explicit-stack
  requirements, and the distinction between detected resource failure and external process termination"*), and that
  the checker turns no resource limit into a nesting restriction;
- answer draft 2's Q1–Q7 with evidence, and list its findings, H1 onward, by severity.

Its report follows, unedited, taken from its own transcript rather than retyped. Its section "A slip, disclosed"
records that one discarded sweep may have opened `.orl` files under `research/law-sufficiency/`; see
REREAD-2-DISPOSITION.md.

---

LAW-FORMAT-0-DRAFT-2.md read: sha256 `f3b6c2a0ef943bc3fa5e2142c686ec5697f8c61ca3abc33c3ba4830ba5c27a5b`

# REREAD-2: an independent re-read of LAW-FORMAT-0 draft 2 and its checker (2026-10-30)

## What I read, what I ran, and what I could not check

**Read in full:**
- `research/rust-core/LAW-FORMAT-0-DRAFT-2.md`, appendix A included. Its sha256 is above, and it equals the one recorded in `evidence/rust-core-format-2.txt`.
- `RULINGS.md` (all of it, B1 included), `SHEET.md` (Amendment 1 included), `REREAD-0-REPORT.md`, `REREAD-0-DISPOSITION.md`, `REREAD-1-REPORT.md` and `REREAD-1-DISPOSITION.md`.
- `format_check.py`, sha256 `b59c221c…e517`, which equals the evidence's.
- `evidence/rust-core-format-2.txt`, sha256 `c7a1d3a1…`.
- `SPEC.md` and `RUNTIME-SPEC.md`.
- `src/orlog/interp.py` and `sema.py`.
- `gen_worked.py`, read only to get appendix A's source texts. Its sha256 `163e54f4…` equals the appendix's.

**Read in part:**
- `syntax.py`, for its limits and `ast_depth`;
- `numeric_ref.py`, for its limits;
- `seal.py`, by use;
- `arbiter.py` and `orl.py`, for how a host stop is handled;
- a diff of draft 1 against draft 2.

**Ran:** only read-only commands, from `⟦HOME⟧\Desktop\Orlog`:
- `sha256sum`, `grep`, `wc` and `diff`;
- `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B -` scripts fed on stdin, which import `format_check` or `src/orlog` and write nothing.

The environment was Git Bash on Windows with CPython 3.14.5, at HEAD `2e9805a`, with the research files uncommitted. Every reference run that tests recursion ran in a process that did not import `format_check`. The commands and their outputs are in the appendix.

**A slip, disclosed.** My first sweep of `.orl` texts (C9a) used a directory filter that fails on Windows path separators. It walked 2,975 paths, and so may have opened `.orl` files under `build/`, `work/` and `research/law-sufficiency/`. I printed nothing from them and kept only aggregate counts. I discarded that run and re-ran it with a correct filter (C9b). Nothing below rests on the first run.

**Could not check:**
1. `format_check.main()`. It imports `common` and `closure_tests` from `research/law-sufficiency/`, so "304 of 304" is the recorded evidence, not a re-run. Instead I re-ran:
   - every fixture;
   - all 44 plants on 222 laws of my own (C9b): 44 of 44 caught;
   - the derivation comparison on those 222 laws: 222 of 222 equal.
2. Any core. None exists, so what a Rust process does on a panic or a stack overflow (H3) is Rust's documented behaviour, not measured here.
3. Linux. Nothing was run there.

## Verdict

Draft 2 and its checker are **not ready** to hand to the clean-room author as they stand. The findings:
- **0 BLOCKER.**
- **4 MAJOR: H1–H4.**
  - H1 and H2 are in the document.
  - H3 and H4 are in the comparison protocol: section 10 together with SHEET Amendment 1.
- **11 MINOR: H5–H15.**
- **15 in all.**

**What holds:**
- The termination claim is true. I found no accepted law that runs without end. Every recursion I tried is refused (C8).
- The budget's check positions, its counting and the stop's report equal the reference (C3).
- Explicit stacks and fallible allocation are stated as implementation obligations. The document, the sheet and the checker set no nesting limit on `perform` or rule uses: the checker accepts chains of 100,000 (C5).
- Detected exhaustion is kept apart from external termination and from every language outcome, and nothing promises to catch what cannot be caught.
- Every F and G finding is resolved or narrowed. All four worked runs of appendix A reproduce byte for byte (C2).

**What must change before handoff:**
- **H1.** One sentence in section 5 redefines the budget, which the owner's first correction forbids: "A statement that begins with ops ≤ B runs to its end". The reference stops inside a While, a For, a Perform and an If's block.
- **H2.** G9's defect has moved from expression depth to clause depth. Phase 3 must walk a clause tree of any depth: W14(a) and (b) are collected failures, not a gate. The checker crashes at 11,000 levels, and a core written from the document can overflow its stack instead of refusing.

**What must change before the experiments:**
- **H3.** Amendment 1's catch-all puts a core's own panics and stack-overflow aborts under "external termination", which is never counted as a disagreement.
- **H4.** Amendment 1 leaves open the reference's recursion limit and process isolation, which decide its class at S1's depth 600. It also has no rule for a core whose two runs differ.

---

## Q1. Termination

**Is section 5's reasoning complete and correct?** It is correct in substance and incomplete as written (H10).

**The argument, checked against the code.** A cycle of performs or of rule uses is impossible, because along each a clause id strictly decreases:
- **Performs.** W6 makes procedures top-level. W11 requires `P < U`, where U is the clause the perform is checked at, and requires the perform to be outside P's body. Inside a procedure Q's body, Q < U, and P is top-level and outside Q's subtree, so P < Q. Procedure ids strictly decrease along a perform chain.
- **Rule uses.** W10 checks a define's value and proviso at the define's own clause d. Let L(r) be the id of r's last define. A use of r in a define of s needs L(r) < d ≤ L(s). L strictly increases along every use edge.
- **The two together.** A rule's value and proviso are expressions and hold no statement, so no rule use leads to a perform. The combined graph is acyclic.
- **Loops.** A While refuses `FUEL-EXHAUSTED` at fuel N ≤ 2^62 (`interp.py:219-228`). A For iterates over an i64 range and breaks before it would overflow (`interp.py:233-241`).
- **Lists and text.** Lists stop at 2^24 items (`LIST_MAX`, `numeric_ref.py:28`; `interp.py:272`, `391`). Text stops at 2^24 bytes (`TEXT_MAX`), and output at 2^30 bytes.
- **Overrides.** The override closure is a static fixed point over finite sets.
- **Conversions and printing** are bounded work; the smallest subnormal prints 1,074 digits.

**What the text leaves out (H10):**
- the strictly decreasing measures above;
- that expressions hold no `perform`;
- that every repetition counts at least one operation (a loop iteration, a perform, a rule use). So uncounted work between two counted operations is bounded by the law's size and the list and text bounds. Do-nothing clauses, skipped absorbed clauses and list copies are uncounted but bounded.

"Ends after finitely many counted operations" implies termination only with that last point. Separately, "a `for` may run 2^63 times" (draft:247) understates it: from −2^63 to 2^63−1 is 2^64 iterations.

**Attempts to break it (C8), each refused:**

| attempt | refused |
|---|---|
| a self-perform from the body | W11 line 4 |
| a self-perform from the body's absorbed else | W11 line 4 |
| p performs a later q, and q performs p | W11 line 4 |
| a perform of a procedure nested in a While | W6 line 4 |
| a rule's proviso using its own rule | W10 line 3 |
| a second define using the rule | W10 line 4 |
| a rule used in a procedure body, with a define after the procedure | W10 line 5 |
| two rules using each other through their provisos | W10 line 3 |
| an override naming itself | W10 line 3 (cycle) |
| a While bound of 2^62 + 1 | W13 line 3 |

A `list-of` above 2^24 is accepted, and refused at run time (`LIST-TOO-LONG`, `interp.py:391-392`).

**Practical completion is not promised, and the draft says so (draft:245-247).** A doubling chain of 10 rules makes one Say cost 1,535 operations (C3). REREAD-1 measured 393,215 for a chain of 18.

## Q2. Budget preservation

**The check's positions equal the reference.** `interp.py:132-154`:
- `seq` calls `stmt` for each non-absorbed clause (134-141);
- `body` calls `stmt` for an inline arm or else statement (147);
- `stmt` checks `ops > budget` at 151, before the early return for Define, ProcDef and Decimals (153-154).

This is exactly draft:286-292. It also holds that there is no check:
- for an absorbed clause (135);
- before an arm's condition (213-214);
- before a loop's iteration (220-228, 234-238);
- inside an expression or a rule use (295-440).

**Counting** is delegated whole to SPEC §7 (draft:292-293: "The check reads the count; it never counts"). Section 5a's `and`, `or` and `not` rows match `interp.py:310-317` and `340-345`.

**The stop's report** matches the code:
- stderr: `STOPPED-BY-HOST after <ops> counted operations (budget <B>)` (draft:534) is `HostStop`'s message (`interp.py:38`);
- no receipt;
- every event before the stop.

**Tests (C3), run in the reference:**

| law | budget | result |
|---|---|---|
| `Let x be 1. Let y be 2. Define r as 3.` | 0, 1, 2 | stopped after 1; stopped after 2, at the define; COMPLETED ops 2 |
| `Let x be 1. Decimals are floats.` | 0 | stopped after 1, at the decimals clause |
| `Say 1. To p…` (the procedure clause last) | 0 | stopped after 1, at the procedure clause |
| `Let x be 1 plus 1. If true, say 1; otherwise say 2.` | 2 | stopped after 3: the If ran its arm's count, then the check before the inline Say stopped it |
| `If false, say 1. Otherwise, do the following. Say 2.` | 0 | stopped after 1, at the block's child; no check for the absorbed clause |
| 10 doubling rules, `Say r10`, `Say 2` | 0, 3, 10 | the Say began at 0 ≤ B and ran 1,535 operations: stopped after 1,535 each time |
| `Let n be 0. While n < 100 (at most 200): increase n. Say n.` | 10 | **stopped after 11, inside the While**; unbudgeted it is COMPLETED ops 404 |

**One sentence redefines the budget (H1).** Draft:295-297: *"A statement that begins with ops ≤ B runs to its end, however many operations that adds."* The last row refutes it: the While began at ops 1 ≤ 10 and was stopped inside its body. Read literally, the sentence stops that run at clause 4, after 403 operations. Everything else in sections 5 and 10 preserves the budget.

## Q3. Explicit stacks

**Stated as implementation obligations: yes.**
- Draft:55-59: "That is an implementation obligation, not a language construct."
- Draft:261-263: "A host's recursion depth is an implementation detail and never a language restriction."
- Draft:402-403: "No check limits how deeply `perform` and rule uses nest."

The wording needs tightening (H11):
- "A reader may nest…" puts the nesting in the reader. It is the law that nests, and the reader must run it.
- The measurable obligation is unstated: the host call-stack depth must be bounded by W14's static bounds alone. A rule use stands inside an expression, so the expression evaluator must itself be resumable.
- Fallible allocation covers "stacks, lists, output buffer … and the like", while the exhaustion kinds name "stack, list, output, trace". Text values and the trace are named in one place and not the other.

**No nesting limit on `perform` or rule uses** in the document, the sheet or the checker:
- W14(a) bounds clause depth, and procedures are top-level.
- W14(b) restarts its loop count at a procedure.
- W14(c) bounds parentheses on one line.
- S1's depths are test points, not limits.
- The checker's B1 fixtures, two chains of 3,000, pass. I fed it raw chains of 30,000 and 100,000, for performs and for rules, and a doubling chain of 64. All were accepted and written back exactly, the 100,000 chains in 2.3 s (C5). The checker follows neither performs nor rule uses.

**The checker's own limits:**
1. **Recursion over clause depth in phase 3.** `visit`, then `walk_seq`, then `visit` (`format_check.py:938-944`) uses about two frames per level, under the 20,000 limit it sets at import (line 35).
   - 9,000 nested Whiles: W14 line 19, in 12.1 s.
   - 11,000 nested Whiles: **RecursionError**, in 17.0 s.
   - 11,000 nested If blocks: **RecursionError**, in 8.3 s.

   W14(a) already refuses these laws at depth 25, so no law is refused because of this limit. The checker's resource limit therefore never becomes a language restriction; it becomes a crash on input the format already refuses (H2).
2. **Quadratic time in clause depth**, from the ancestor walks at 632-647 and `proc_of` (526-532).
3. **Parser recursion** (`expr`, `etype`, `w_expr`), bounded at 130 by the lexical W14(c), which phase 2 checks first.
4. **The recursion limit itself.** Importing it raises the process's limit to 20,000, which changes the reference's own behaviour in the same process (H4).

## Q4. Detected exhaustion against external termination

**Kept apart: yes.**
- Detected exhaustion is a row of its own: exit 5, `RESOURCE-EXHAUSTED: <kind>`, no receipt (draft:538).
- External termination is explicitly no outcome of the core (draft:540-543): "The harness classifies it on its own … The core does not and cannot promise to catch it."
- Draft:545-551 says these are never a refusal, a stop or a completion, carry no receipt, and are never compared.
- Section 0 (draft:58-59) and SHEET:151 promise nothing about process-level memory failures.

This matches B1's correction 2.

**Each outcome, and what tells it apart:**

| outcome | exit | files | stderr | told apart from the others by |
|---|---|---|---|---|
| completed | 0 | TRACE?, OUT, RECEIPT | none | the receipt's `status COMPLETED` |
| refused | 0 | TRACE?, OUT, RECEIPT | none | `status REFUSED …` |
| stopped | 4 | TRACE? | STOPPED-BY-HOST line | the exit status |
| load refusal | 3 | none | LAW-REFUSED line | the exit status and the stderr prefix |
| usage error | 2 | none | `USAGE:` | the stderr prefix |
| I/O error | 2 | partial, never a receipt after it | `IO-ERROR:` | the stderr prefix |
| detected exhaustion | 5 | TRACE as far as it was written | `RESOURCE-EXHAUSTED:` | the exit status |

Each row is unique by its exit status and its stderr or receipt. The table is not complete:
- **No row for a core fault (H3).** A Rust panic (status 101), a stack-overflow abort or an aborting infallible allocation fall into SHEET:147-148's "any other way that gives none of the exit statuses above", so they are classed external termination. By SHEET:158-160 that is "never a semantic disagreement" and only "counted against R3–R5's coverage". The owner's correction names "an OS kill or externally enforced timeout". The catch-all also covers the core's own crashes, including the host-stack recursion that section 0 forbids. Nothing says what happens when an exit status contradicts its files: exit 0 without a receipt, say.
- **Exhaustion has no place in the order of outcomes** (draft:520-524). Its files row ("OUT and RECEIPT not written") is false if allocation fails after OUT is written. Whether running out of memory while reading LAW is `IO-ERROR` or `RESOURCE-EXHAUSTED` is unsaid (H12).
- **Smaller gaps:**
  - whether the stderr line ends in LF;
  - what "the same path" means;
  - draft 1's statement that `<reason>` is free text no comparison reads, which was dropped (H12).

## Q5. F1–F17 and G1–G19

| finding | resolved? | evidence |
|---|---|---|
| F1 | yes | draft:113-116, 407; plant caught, W1 line 5 (C9b) |
| F2 | yes | §7 obligation 3 with its example (draft:367-388); the fixtures are accepted and their derivations equal; the line-order plant is caught |
| F3 | **partly** | W14(a)–(c) and explicit stacks are present; phase 3 still walks unbounded clause depth (H2) |
| F4 | yes | W9's placement rules (draft:448-454); 3 plants, plus G4's 3, caught |
| F5 | yes | draft:136-148; `\u{d800}` and `\u{110000}` refused; `\u{0}` accepted |
| F6 | yes | draft:183-191; both plants caught |
| F7 | yes in the positions; **contradicted** by one sentence | draft:286-293 equal `interp.py:132-154` (C3); H1 |
| F8 | mostly | the table, the precedence and the W2/W3 split are present; H3 and H12 remain |
| F9 | yes | draft:42-45; the supplementary file's counts verified (C10) |
| F10 | yes | §5a, row by row against `interp.py:287-421` |
| F11 | yes | W6 (draft:412); plant caught |
| F12 | yes | draft:103; A.1 reproduced; fixture accepted |
| F13 | yes | draft:249-284 |
| F14 | yes | draft:152-154 |
| F15 | yes | draft:428, 427, 349 |
| F16 | yes | derivation 19; A.1's words reproduced |
| F17 | mostly | §0 is present; SPEC.md and RUNTIME-SPEC.md are not named by sha256 (H15) |
| G1 | yes | draft:272-277 and W8, W10, W11, W12. T3 is refused W10 line 3, and T4 W8 line 3; both separate "checked at" from "runs as" |
| G2 | yes in substance, by B1 | draft:55-59, 234-247, 261-263, 295-298, 538-551; SHEET Amendment 1; residuals H1, H3, H4, H11 |
| G3 | yes | fixture accepted and written back exactly |
| G4 | yes | three plants caught (W9 line 3) |
| G5 | yes | no crash. Only 2 of the disposition's 3 plants are present; the third, `(else 99 (perform 1))`, run here is W4 line 5, correct (H13) |
| G6 | yes | T1 and T2 are W1 line 3, T2b W1 line 1 |
| G7 | yes | draft:106-112; `(clause 1  0 …)` is W1, two spaces before `absorbed` W3. Neither plant is in the document's list (H13) |
| G8 | yes | the line column; the walk rule (draft:497-498); its 3 plants caught; residuals H7 and H14 |
| G9 | yes for expressions | W14(c) is lexical, in phase 2; the plants at 131 and at 25,000 then a W2 line are caught; the same defect remains for clause depth (H2) |
| G10 | yes | draft:131-134 |
| G11 | yes in substance | derivation steps 1–4; an arithmetic slip remains (H9) |
| G12 | yes | draft:279-284; A.4 reproduced: `claim 0 4 2 2 0 2 0` and `claim 1 5 1 1 0 2 12` |
| G13 | partly | the order, the TRACE's creation, distinct paths and `--` are present; residuals and losses from draft 1 (H12) |
| G14 | yes | draft:74-77; the §5a rows |
| G15 | yes | `nalog-tupug-sivik-siduh` reproduced |
| G16 | yes | the sha256 and counts verified (C10); A.1–A.4 reproduced byte for byte (C2) |
| G17 | yes | draft:15-18; the analysis-field column |
| G18 | yes | every listed plant is present and caught; the document's list omits G7's two (H13) |
| G19 | yes | draft:113; W5's line column |

**Does each G-plant test what its finding says? Yes:**
- T3 would pass under a "runs as" reading, since 3 > 2 > 1, so it discriminates G1. T4 likewise.
- The line-order plant fails exactly at the else's `let 0` on line 3.
- W14(a) is tested with If blocks and no loops; W14(b) with 17 Whiles at depth 17 ≤ 24.
- The 131 and 130 cases sit exactly at the boundary.
- G6's T1, T2 and T2b put the first failure before a later one.
- G8's inline If names a While body that would otherwise be walked twice.
- G5's laws had crashed the old checker.

## Q6. The checker against sections 2–4 and 8

**Phase 1** matches (`format_check.py:430-464`):
- line by line, each line completely;
- the prefix byte by byte (PREFIX, line 40) and the final `)`;
- the numbering and the parent rule;
- a missing LF on the last line;
- an empty input refused W1 line 1, and a missing line 2 refused W1 line 2.

**Phase 2** matches the order: W14(c), then W2, then W3, line by line (467-477). The W2/W3 split agrees with "Once W2 holds, writing back gives the rest exactly iff W3 holds": the lexer tolerates spacing, and atoms and escapes are W2. One difference:
- **H5.** The lexical count on unbalanced lines is undefined in the document. The checker keeps a running count that may go negative.

**Phase 3**, W by W:

| W | checker against the document |
|---|---|
| W1 | as written |
| W2 | as written |
| W3 | as written |
| W4 | as written |
| W5 | **differs (H7):** an absorbed clause named by two Ifs through `(block …)` is reported at the absorbed clause's line ("named by two blocks", lines 618-624), where the document says the later If's line |
| W6 | as written. The checker judges a literal's mode against line 2's mode, not derivation "Decimals"; no observable difference, since a mismatch is already reported on an earlier or equal line |
| W7 | as written |
| W8 | **differs (H6):** `remove-last` on a For counter gives W9 only (932-935). The document's W8 forbids it ("never … removed from"), so W8 is the least W on that line |
| W9 | **differs (H8):** with a promote beside a rule that has no define, the checker makes the placement check against an underived type and reports W9 (712-720). The document says that check is not made, so the line's W10 is reported |
| W10 | as written; the line column is incomplete (H14) |
| W11 | as written |
| W12 | as written |
| W13 | as written |
| W14(a), (b) | the values are as written; the walk crashes above about 10,000 levels (H2) |
| W14(c) | H5 |

**The walk-skip set.** The checker skips the blocks of a chain that fails W4 or W5 (lines 577-617); the document says W5. Every reported result is unchanged, because the If's line already holds a W4 or W5 failure.

**Stale docstrings.** Line 14 says "written from draft 1's sections". Lines 26-27 say "Its recursive parser handles nesting to a few thousand levels". Since W14(c), the unbounded recursion is the walk, not the parser.

**Re-run here:**
- every fixture, accepted and written back exactly, with derivations equal;
- all 44 plants, caught on my own 222 laws (C9b);
- 222 of 222 front-end laws from the repository (outside law-sufficiency, build and work), accepted, written back exactly, derivations equal. The deepest parentheses were 65.

## Q7. What a clean-room author would still have to guess

1. Whether the budget stops inside compound statements: section 5 says both yes (the check list) and no (H1).
2. Whether the phase-3 walk may recurse, and on what depth (H2).
3. How to count parentheses on an unbalanced line (H5).
4. How far "explicit stacks" reaches: for example, whether an expression holding a rule use must be resumable (H11).
5. Section 10's losses (H12):
   - what OUT, RECEIPT and TRACE hold: draft 1 said "RUNTIME-SPEC §6's output, receipt and trace paths";
   - whether the trace streams or is buffered;
   - where exhaustion falls in the order of outcomes;
   - what "same path" means;
   - whether stderr ends in LF.
6. The line of W10's other failures, such as an over target that is no define or a non-bool proviso (H14).
7. The width of the ops counter. SPEC §7 says u64 (SPEC.md:209), and RUNTIME-SPEC §6 `rt.ops: u64`. What happens past 2^64 is unsaid. That is not reachable in practice, so it is not counted as a finding.

**Appendix A against the reference (C2).** A.1–A.4 reproduce exactly:
- the law bytes;
- the TEXTSEAL;
- the law seal and the seal words;
- the receipt, with backend line `reference`;
- the trace.

The cited sha256s of `interp.py` (`f8432918…`), `numeric_ref.py` (`eacac3dd…`) and `gen_worked.py` (`163e54f4…`) match the files.

---

## Findings

### H1 — MAJOR: one sentence redefines the budget for compound statements
- **Document:** draft:295-297, *"A statement that begins with ops ≤ B runs to its end, however many operations that adds. So ops may exceed B by any amount before the next check stops the run."*
- **Evidence:**
  - `interp.py:228`, `238`, `244` and `145` run the bodies of a While, a For, a Perform and a block through `seq`, which checks before each clause.
  - C3: a While that began at ops 1 under budget 10 stops after 11 operations, at event 3 on clause 3. Under the sentence it would stop at clause 4 after 403.
  - C3: an If's absorbed-else block is stopped at its child.
  - The owner's correction 1: *"Do not redefine the budget in prose."* His B1 part 3 speaks of *"Work inside one statement"*. That holds only for work that no check position separates.
- **Proposal:** replace the two sentences with: "Between two checks nothing stops the run. The expressions of one statement, its rule uses included, run to their end however many operations they add. A While, a For, a Perform and an If's block run their bodies as sequences, so the check is made again before each clause of those bodies, and the run can stop inside them."

### H2 — MAJOR: phase 3 needs a walk of unbounded clause depth; the checker crashes, and a recursive core would too
- **Document:**
  - W1 (draft:407) allows any chain of parents.
  - W14(a) and (b) (draft:467-470) are phase-3 failures "among every failure of W4–W14" (draft:493).
  - The walk (draft:367-375) descends into every block and body.
  - Only W14(c) is a gate: "so a reader's parser never goes deeper" (draft:471-472).
- **Evidence (C5):** the checker gives
  - 9,000 nested Whiles: W14 line 19, in 12.1 s;
  - 11,000 nested Whiles: RecursionError;
  - 11,000 nested If blocks: RecursionError.

  The cause is `format_check.py:938-944` under its 20,000 limit. A core whose reader walks recursively, as REREAD-1 noted for the parser (G9), overflows its stack instead of refusing.
- **Proposal:**
  - Add to phase 3: "The walk enters no child of a clause that is 25 deep." The walk is then at most 25 deep, and the reported (line, W) is unchanged:
    - every skipped clause lies on a later line than its 25-deep ancestor, which carries W14 on its own line;
    - that ancestor's own statement is still walked;
    - every relational line the table names for a skipped part (the later If, the decimals clause, a define) is also later.
  - Compute depth iteratively from the parent links.
  - Do the same in the checker, and plant 30,000 nested Whiles (W14 line 19) and 30,000 nested If blocks (W14 line 27).

### H3 — MAJOR: the protocol files the core's own crashes under external termination
- **Document and sheet:**
  - SHEET:147-148, external termination is the harness's kill "or the process ends by the operating system or any other way that gives none of the exit statuses above";
  - SHEET:158-160, such an outcome is "counted against R3–R5's coverage, not their agreement";
  - draft:540-543 includes "an allocation failure that does not return".
- **Evidence:**
  - The owner's correction 2 names *"an OS kill or externally enforced timeout"*.
  - By Rust's documented behaviour (not measured; no core exists), each of these is "none of the exit statuses above":
    - a panic exits with status 101;
    - a host-stack overflow aborts (on Windows `STATUS_STACK_OVERFLOW`);
    - a failed infallible allocation aborts.

    So each is classed external termination, never a disagreement. That includes the host recursion section 0 forbids.
  - No coverage threshold for R3–R5 is stated.
  - No rule covers an exit status whose files contradict it.
- **Proposal:**
  - Add a class **core fault**: any end the harness did not cause that is no row of section 10, or whose files or stderr contradict its row. It falsifies the prediction under test (R3–R6, S1–S4).
  - Reserve external termination for the harness's own kill, and for an end it can attribute to the host (a SIGKILL by an OOM killer, say), with that evidence recorded.
  - State now that R3–R5 hold only on full coverage of RESULT cases, or name the threshold.

### H4 — MAJOR: Amendment 1 leaves open parameters that decide the classes
- **Sheet:** SHEET:119-136 fix the time limits, the repeats and the reference's classes. They do not fix:
  - the reference's Python recursion limit;
  - the Python version;
  - whether each run is a fresh process that never imports `format_check`.

  Also left open:
  - no class covers a core whose two runs differ;
  - R6 (SHEET:94) keeps "never hangs past the budget", against B1 part 3;
  - S3 (SHEET:170) names a seed but no sampling algorithm, and no rule for texts with fewer than 20 values of B.
- **Evidence:**
  - C4: at the default limit of 1,000, perform and rule chains of 600 raise RecursionError.
  - REREAD-1's C6: at 20,000 (`format_check.py:35`, raised on import) the same laws complete with ops 601.
  - So S1's depth 600 flips between NO REFERENCE RESULT and RESULT on an unwritten setting.
  - The owner's correction 3: *"The time limit, repeat count, and classification rules must be written into the sheet before experiments begin."*
- **Proposal:**
  - Each reference run in a fresh `python -B` process with `PYTHONHASHSEED=0`, Python's default recursion limit and thread stack, never importing the checker; the Python version recorded.
  - A core class "unstable" (two runs that differ in class or result), counted as a falsifier.
  - R6: "never exceeds the core's time limit where the reference's class is RESULT".
  - S3's sampler written out, for example `random.Random(20261030).sample(range(ops+1), min(20, ops+1))` per text, in a stated order.

### H5 — MINOR: W14(c)'s lexical count is undefined on unbalanced lines
- **Document:** draft:471, "No clause line nests parentheses outside strings more than 130 deep".
- **Evidence (C6):** take the line `(clause 1 0 ))` followed by 131 `(`, 129 `)` and a final `)`.
  - The checker's running count (`paren_depth`, 59-80) peaks at 130, so the line is refused W2 ("a ')' with no '('").
  - A count that ignores an unmatched `)` peaks at 131, so W14.
  - A count that stops at the first unmatched `)` gives W2 even where the checker gives W14: `(clause 1 0 )` followed by 131 `(` is W14 line 3 in the checker.
  - The checker's skipping of whatever byte follows a backslash is also unstated.
- **Proposal:** "the running count of `(` minus `)` outside strings, from the line's first byte; a string opens at `"` and closes at the next `"` not escaped, where `\` escapes the next byte; the line fails W14 if the count ever exceeds 130."

### H6 — MINOR (checker): `remove-last` on a For counter is W9, not W8
- **Checker:** lines 932-935 have no counter check, unlike `append` (924-925).
- **Evidence (C6):** `(clause 1 0 (for 0 …))`, `(clause 2 1 (remove-last 0))` is refused W9 line 4. The document's W8 (draft:414) forbids it, so W8 line 4.
- **Proposal:** add the W8 check to `remove-last`, and a plant.

### H7 — MINOR (checker): an absorbed clause named by two Ifs through blocks is reported on the wrong line
- **Checker:** lines 611-624 count blocks across chains, and report "named by two blocks" at the named clause's line.
- **Evidence (C7):** an If at clause 1 has `(else 2 (block 2))`; clause 2 is absorbed with child 3; an If at clause 4 has `(else 2 (block 2))`. Failures collected: `(4, W5)` and `(6, W5)`. The checker reports W5 line 4. The document (draft:411: "One named by two Ifs: the later If's line") gives line 6. The G8 plant uses inline bodies, so it misses this.
- **Proposal:** count only blocks of chains that pass the shape check, or attribute to the later If. Plant this law.

### H8 — MINOR (checker): a check is made on a type an earlier failure left underived
- **Checker:** lines 712-720 pass `promote_to=None` when the other operand's type is None, and line 671 then fails W9.
- **Evidence (C6):** `(say (+ fix (promote fix (lit int 1)) (rule "r")))` with no define of r is refused W9 line 3. Draft:495-496 lists "a rule with no define" among what leaves a type underived, so the placement check is not made, and W10 line 3 is reported. This is REREAD-1's row 12, now with an observable difference.
- **Proposal:** skip the placement check when the other operand's type is None. Plant this law.

### H9 — MINOR: W14(c)'s derivation omits the If-Unless `not` in its arithmetic
- **Document:** draft:476-480. Step 2 adds "an If-Unless's `not` above a condition", but step 3 concludes "at most 63 + 32 = 95 deep".
- **Evidence:** an Unless condition can be 63 + 32 + 1 = 96 deep. Step 4's 99 still holds: a condition has 3 wrappers (3 + 96 = 99), and an inline statement's 62 + 31 + 4 = 97.
- **Proposal:** say 96 for an Unless condition, and give the per-place sums. The 130 bound is unaffected.

### H10 — MINOR: the termination reasoning is a sketch
- **Document:** draft:234-247.
- **Evidence:** see Q1. The measures, the fact that expressions hold no `perform`, and the bound on uncounted work are not stated. "a `for` may run 2^63 times" should read 2^64.
- **Proposal:** add three sentences:
  - "W6 and W11 make the performed procedure's id smaller than the performing one's."
  - "W10 makes the last define of a used rule smaller than the using define."
  - "Every loop iteration, perform and rule use counts at least one operation, so uncounted work between counted operations is bounded by the law's length and the list and text bounds."

  And correct 2^63 to 2^64.

### H11 — MINOR: the explicit-stack obligation is worded loosely and its scope is vague
- **Document:**
  - draft:261, "A reader may nest `perform` and rule uses to any depth";
  - draft:56-57, "its stacks, its lists and its output buffer … and the like";
  - draft:538, the kinds "stack, list, output, trace, or another named store".
- **Evidence:** a law nests and a reader runs it. A rule use stands inside an expression, so avoiding host recursion requires a resumable expression evaluator. The text never says so.
- **Proposal:**
  - "A law may nest them to any depth, and a reader must run it."
  - "The host call-stack depth is bounded by a constant that depends only on W14's bounds, never on a chain of performs or rule uses."
  - List the stores held to fallible allocation once: stacks, lists, text values, output, trace.

### H12 — MINOR: section 10 lost parts of draft 1 and leaves edges open
- **Document:** draft:510-554, against draft 1's §10.
- **Evidence:** dropped from draft 1:
  - "LAW: a path to the law bytes";
  - "OUT, RECEIPT, TRACE: RUNTIME-SPEC §6's output, receipt and trace paths";
  - "The trace is written as events happen";
  - "`<k>`, `<n>`: the W and the line chosen in section 8. `<reason>` is free text, which no comparison reads";
  - the usage error's causes.

  Open edges:
  - exhaustion is not placed in the order of outcomes;
  - its files row is false after OUT is written;
  - "the same path" is undefined (string or file identity);
  - the stderr line's final LF is unsaid;
  - the stop is labelled "language (the host's budget)", while SPEC §12 (SPEC.md:453) says *"the law said nothing"* and B1 part 4 lists a budget result as its own kind.
- **Proposal:**
  - restore the dropped lines;
  - "an allocation that fails before the run starts is RESOURCE-EXHAUSTED; after OUT is written, whatever was written stays";
  - paths compared as given strings;
  - stderr ends with one LF;
  - label the stop's kind "budget (host)".

### H13 — MINOR: section 11 and the checker disagree on the lists; stale docstrings
- **Document and checker:**
  - The draft's fixture list (draft:568-571) omits the checker's two B1 chains of 3,000, which are the evidence for "no limit" (draft:565).
  - The plant list (draft:573-587) omits G7's two plants, so it lists 20 of the checker's 22 draft-2 plants.
  - REREAD-1-DISPOSITION promised "G5's three laws", and the checker has two.
  - Docstrings at `format_check.py:9` ("a chain failing W4 or W5"), 14 ("draft 1's sections") and 26-27 ("Its recursive parser handles nesting to a few thousand levels").
- **Evidence:** C6, the third G5 law: W4 line 5, correct.
- **Proposal:** align the lists, add the third G5 plant, and correct the docstrings.

### H14 — MINOR: W10's line column covers only three of its failures
- **Document:** draft:416, "a use: its line. Two types: the later define's line. A cycle: each define's line in it."
- **Evidence:** no line is given for an `(over C)` naming a clause that is not a define of the name, for a proviso that is not bool, or for a list-valued define. REREAD-1-DISPOSITION's G8 principle, "a failure that relates two lines belongs to the later one", was not carried into draft 2. So an over target later than its define is ambiguous. The checker uses the define's line.
- **Proposal:** "every other W10 failure: the define's line."

### H15 — MINOR: reading-set citations
- **Document:**
  - Section 0 gives the sha256 of the two vector files but not of `SPEC.md` (`27dfff0c…`) or `RUNTIME-SPEC.md` (`0bd571d6…`), though SHEET D1 says each is named by sha256.
  - Draft:269-270 cites "(SPEC §6)" for "a use in an absorbed arm's condition runs as that absorbed clause". SPEC §6 says "the clause of the statement that used the rule" (SPEC.md:204). The settling text is SPEC §11 item 18 (SPEC.md:341).
- **Proposal:** add both sha256s, and cite item 18.

---

## Appendix: commands and outputs

All from `⟦HOME⟧\Desktop\Orlog`, Git Bash, as `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B -` with the script fed on stdin, unless marked otherwise.

**C1:**
```
sha256sum research/rust-core/LAW-FORMAT-0-DRAFT-2.md research/rust-core/format_check.py evidence/rust-core-format-2.txt
→ f3b6c2a0…7a5b, b59c221c…e517, c7a1d3a1…a5fa0c5
sha256sum src/orlog/interp.py src/orlog/numeric_ref.py research/rust-core/gen_worked.py vectors/runtime-vectors.txt research/rust-core/vectors-as-integer.txt SPEC.md RUNTIME-SPEC.md
→ f8432918…4d27, eacac3dd…bb64, 163e54f4…b738, 841240b7…f204, 2bff1c69…ad2f, 27dfff0c…6de5, 0bd571d6…ec35
```

**C2:** compile gen_worked's four texts, run `interp.Interp(…, trace=True)`, and compare with the appendix's code blocks.
```
A.1 law equal True, receipt equal True, trace equal True, … words nalog-tupug-sivik-siduh in doc True
A.2 … True True True … kasah-mivis-zomub-kibog True
A.3 … True True True … virim-rahoz-loton-hahug True
A.4 … True True True … vilug-lujag-kakab-fival True
```

**C3:** the reference under budgets, in a process without `format_check`.
```
stop at a define: no budget COMPLETED ops 2; budget 0: STOPPED after 1; budget 1: STOPPED after 2 (last event 2 A 2); budget 2: COMPLETED ops 2
stop at a decimals clause: budget 0: STOPPED after 1; budget 1: COMPLETED ops 1
stop at a procedure clause, the last: budget 0: STOPPED after 1; budget 1: COMPLETED
check before an inline arm statement ((if (arm 2 … (say …)) (else 2 (say …)))): budget 1: STOPPED after 2; budget 2: STOPPED after 3, 1 event; budget 3: COMPLETED ops 4
absorbed else with a block: budget 0: STOPPED after 1, 0 events; budget 1: COMPLETED ops 2
10 doubling rules, Say r10, Say 2: no budget COMPLETED ops 1536; budgets 0, 3, 10: STOPPED after 1535, 1 event (1 S 11)
While n < 100 (fuel 200), increase n, Say n: no budget COMPLETED ops 404 events 102; budget 10: STOPPED after 11, 3 events, last (3 A 3)
```

**C4:** front-end chains in the reference, recursion limit 1000, CPython 3.14.5.
```
perform chain 300 | accepts | COMPLETED ops 301     rule chain 300 | accepts | COMPLETED ops 301
perform chain 600 | accepts | RecursionError        rule chain 600 | accepts | RecursionError
perform chain 3000 | accepts | RecursionError       rule chain 3000 | accepts | RecursionError
perform chain 30000 | accepts (1.5 s) | RecursionError   rule chain 30000 | accepts (1.1 s) | RecursionError
```

**C5:** the checker on deep input. Its recursion limit after import is 20000.
```
perform chain 30000 / 100000 (raw bytes) -> ACCEPTED, written back exactly True (0.7 s / 2.3 s)
rule chain 30000 / 100000 (raw bytes)    -> ACCEPTED, written back exactly True (0.6 s / 2.3 s)
doubling rule chain 64                   -> ACCEPTED
25 / 5000 / 9000 nested whiles           -> refused W14 line 19 (0.0 s / 3.4 s / 12.1 s)
11000 nested whiles                      -> CRASHED: RecursionError (17.0 s)
25 nested If blocks                      -> refused W14 line 27
11000 nested If blocks                   -> CRASHED: RecursionError (8.3 s)
```

**C6:** the checker on edge cases.
```
remove-last on a for counter                         -> refused W9 line 4: remove-last on int
append to a for counter                              -> refused W8 line 4
(else 99 (perform 1)) after a procedure              -> refused W4 line 5
"(clause 1 0 ))" + "("*131 + ")"*129 + ")"           -> refused W2 line 3: a ')' with no '('
"(clause 1 0 )" + "("*131 + ")"*130 + ")"            -> refused W14 line 3
trailing space in the rest / two spaces after parent -> refused W3 line 3
inline if whose (block 1) names its own clause       -> refused W5 line 3
promote beside a rule with no define                 -> refused W9 line 3: a promote where SPEC §5 puts none
the same with a define of r (fix) first              -> ACCEPTED
promote beside an undeclared variable                -> refused W8 line 3
```

**C7:** two Ifs naming absorbed clause 2 through blocks.
```
refused W5 line 4: clause 2 is named by two blocks
every failure collected: [(4, 5, 'clause 2 is named by two blocks'), (6, 5, 'absorbed clause 2 is named twice')]
```

**C8:** attempted recursion and unbounded constructs, each in the checker. The results are the table in Q1.

**C9a:** the first sweep, discarded. Its directory filter failed on Windows separators: 2,975 paths. See "A slip, disclosed".

**C9b:** every `.orl` outside `research/law-sufficiency`, `build`, `work` and `.git`.
```
any path under research/law-sufficiency: False
texts 475, front end refuses 253, accepts 222; checker accepts and writes back exactly 222; derivations equal 222; deepest parens 65
fixtures (REREAD-0's four and B1's two chains): accepted, written back True, derivations equal True
byte fixtures (U+0000; 130 deep): accepted, written back True
plants 44 of 44 caught, 44 run, on 222 laws of my own sweep
```

**C10:**
```
wc -l < research/rust-core/vectors-as-integer.txt → 446
op counts: 268 f_as_i, 178 x_as_i
refusals: 143 INEXACT-CONVERSION, 6 NOT-FINITE, 40 OVERFLOW
wc -l < vectors/runtime-vectors.txt → 20015
sha256 lines: 9
```

**Grep:**
- `grep -n -i "nest\|depth\|limit\|recurs\|stack\|fallible\|exhaust"` over the draft and the sheet finds no nesting limit on `perform` or rule uses.
- `diff` of draft 1 against draft 2 shows the losses listed in H12.
