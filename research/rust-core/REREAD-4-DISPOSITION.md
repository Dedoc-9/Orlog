# REREAD-4: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted F1(b) and F2(a), R2b included, and the thirteen minor findings as wording
corrections, *"provided they do not change the adopted format rules or evidence classifications"* (recorded whole in
[RULINGS.md](RULINGS.md)). His precisions:
- F1: three gates before the walk, and the walk then whole; the gates' order left open by him, to be settled from the
  specification or proposed and frozen before the next evidence run, never taken from draft 4;
- F2: the reader's determination recorded with the exact rule and diagnostic, and checker agreement never counted as
  proof;
- R2b's fixtures and expected outcomes frozen before testing; the R6 reference runner in the sheet by path and sha256.

Held to his proviso, K8's proposed new exhaustion kind `state` is dropped (RULINGS.md, "As kept"). They are applied in
draft 5, the checker, and SHEET.md's Amendment 4. The text below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 16 findings in [REREAD-4-REPORT.md](REREAD-4-REPORT.md), the
re-read of LAW-FORMAT-0 draft 4 (sha256 `0978c7f1…`), its checker (`b39bbd05…`) and SHEET Amendment 3 (`fff19111…`).
Nothing changes until the owner rules. He answers ASK F1 and F2. Then:
- draft 5 applies every DRAFT item and F1;
- the checker and `plant_reverts.py` are amended to match;
- SHEET.md gains Amendment 4 with F2, the DRAFT items, and the files they fix;
- a fresh independent re-read follows.

No core code is written before its findings are resolved. In his words: *"No Rust-core implementation,
production-source changes, gate changes, release changes, commit, or push is authorized by this ruling. Phase 0 remains
the active scope."*

**What the re-read found holds** (MEASURED there; the claims below re-run here):
- **E1's depth gate, as ruled.** One pass over the parent links, no recursion; a law that fails it reaches no walk.
  300,000-deep trees are refused in 5.35 s, linear in depth, at Python's default recursion limit.
- **The chain gate.** It is the most literal reading of his fifth point, and the only one consistent with his fourth.
- **Every file Amendment 3 fixes** reproduces byte for byte, and decoder1's sha256 is as recorded.
- **The budget.** 13 laws at every B from 0 to ops + 1: the reference stops at section 5's first position where
  ops > B, with 0 mismatches, J15's inline-arm sentence and the do-nothing tails included.
- **No limit on chains.** Perform and rule chains of 100,000 are accepted and written back exactly.
- **Exit 5 and the Windows rule** are no broader than his words.

**What it found wrong, by area:**

| | findings |
|---|---|
| the walk | **K1 (MAJOR)**: the walk never enters the children of a clause that has children and no body, a third skip draft 4 says does not exist. Two readings report different (line, W) |
| R6 and R7 | **K2 (MAJOR)**: R7's plant *"a decoder accepting a non-canonical number"* can be caught by no prediction R7 lists. **K3 (MAJOR)**: R6's reference runner is unwritten, so the line between a refusal and a crash is the harness's, and *"an accepted non-canonical form"* has no judge |
| the gates' edges | K4 (W6 or W7 for an inline `define`), K5 (two points of E1 for his word), K6 (the chain gate's own property unplanted) |
| the protocol's wording | K7–K15 |
| stale wording | K16 |

**The report's count is right:** 0 BLOCKER, 3 MAJOR (K1–K3), 13 MINOR (K4–K16), 16 in all. By re-read, the findings
have run 17 (F), 19 (G), 15 (H), 17 (J), 16 (K).

**Which findings are mine:**
- **K1:** draft 4's sentences *"The walk covers the whole tree"* and *"Only two parts are not entered (G8)"*. I wrote
  them without checking the walk's own definition (section 7 enters children only through a `while`, a `for`, a
  procedure or a block). It is J1's mechanism a third time: a claim about the walk made from its intent, not its rule.
- **K2:** I widened R7's list for the budget plants and did not check the other plants against it.
- **K3:** my R6 design fixed the mutants and the classes, but not the program that runs the reference, nor who judges
  canonicity.
- **K5, K6:** my reading of his fifth point, and a revert that "bites" only by crashing.
- **K7, K8, K16:** wording I did not carry through (S2's falsifier, the exhaustion kinds for J6's stores, a stale
  comment, the change table, a manifest's note).

**How each finding was checked.** Each concrete claim was run again here, read-only (scratch `rr4_check.py`):
through `format_check.read`; through two copies of the checker changed in memory, one that also walks the children of
a body-less clause and one with no chain gate that does not crash; and through Python itself for the exception-type
edges.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| K1 | MAJOR | the walk skips the children of a clause with children and no body; draft 4 says only two parts are skipped | **CONFIRMED.** A1: checker W8 line 3, whole-tree reading W5 line 4. A2: W5 line 4 against W8 line 3. A4: W8 line 3 against W5 line 4. C1: W11 line 3 against W5 line 4 | **ASK F1** |
| K2 | MAJOR | R7's decoder plant is caught by none of R1, R3, R4, R5, S3 or the fixtures | **CONFIRMED** by the text: every one of them runs only canonical law bytes. Here 8 mutants are refused W2 for a non-canonical number and 2 W1 for a leading zero in the prefix (the report counts 9). decoder1 reads every number with `int()`, which accepts a leading zero, so R6 as written cannot catch the plant either | **ASK F2** |
| K3 | MAJOR | R6's runner unwritten; the refusal-or-crash line is the harness's; "an accepted non-canonical form" has no judge | **CONFIRMED.** A module's uncaught `DecodeError` ends the process with exit 1 and the last line `fakedecoder.DecodeError: line 3: a refusal`: a crash under Amendment 3's rule. And see *decoder1's reach* below | **ASK F2**; the runner is DRAFT |
| K4 | MINOR | an inline `define`, `procedure` or `decimals` fails W6 and W7 on one line; the least-W rule gives W6, the checker W7 | **CONFIRMED** (W7 line 3, all three) | **DRAFT** with F1: under F1(b) the structure gate reports W7, as the checker does; under F1(a) the document says the W7 failure is all that is checked of that statement. Plant the three |
| K5 | MINOR | the gates' order is the writer's; G8's skip keeps J1's cross-line effect | **CONFIRMED.** With a sound inner chain the law is accepted; with an inner chain failing W5 on line 4, W8 is reported on line 3, a sound line | **ASK F1** |
| K6 | MINOR | the chain gate's defining property is unplanted; one revert bites only by crashing | **CONFIRMED** for the two new laws: `perform 99` on line 3 and a chain naming 99 on line 4 gives W4 line 4 with the gate, W4 line 3 without; an undeclared variable on line 3 and `(block 99)` on line 4 gives W4 line 4 with, W8 line 3 without. J7's plant depends on how the gate is undone: here, a no-gate checker that treats the missing clause as W5 skips the block and gives W8 line 3; the report's variant gave W4 line 4 | **DRAFT:** plant the two laws. `plant_reverts.py` undoes the chain gate without a crash (W5 guarded against a missing clause, as here), and counts a crash of an undone checker apart from a changed report |
| K7 | MINOR | S2's falsifier not restated as a comparison of class and result | **CONFIRMED** by the text (SHEET:169, Amendment 3) | **DRAFT** (Amendment 4): S2 in R5's words. Under each budget, the core gives the reference's class and result, STOPPED with the same count and trace or COMPLETED with the same P and trace, where the reference's class is RESULT; at 64, any outcome reported as a semantic result fails; anywhere, CORE-FAULT or UNSTABLE-CORE fails |
| K8 | MINOR | the exhaustion kinds do not cover J6's stores; "and the like" leaves infallible allocators to guess | **CONFIRMED** by the text (draft4:71-74, :640) | **DRAFT:** each store mapped to a kind: `law` (the bytes and every structure built from them), `stack`, `state` (variables, claim accumulators, cost counters; a new kind), `list`, `text`, `output`, `trace` (the trace and every event's payload). Section 0 names the fallible calls (the `try_reserve` family) and forbids, for those stores, any allocation not preceded by one that succeeded: `Box::new`, `vec!`, `format!`, `to_string`, `to_vec`, `clone`, `collect`, `BTreeMap` insertion, and `fs::read` or `read_to_end` |
| K9 | MINOR | UNSTABLE-CORE's "result" undefined outside the compared classes | **CONFIRMED** by the text | **DRAFT:** the result, by class. COMPLETED and REFUSED: P and the trace. STOPPED: the count and the trace. LOAD-REFUSED: W and the line. RESOURCE-EXHAUSTED: the kind. USAGE-ERROR, IO-ERROR, EXTERNAL-TERMINATION: the class alone. CORE-FAULT: the exit status |
| K10 | MINOR | J17's stdout rule not carried into the sheet | **CONFIRMED** (SHEET:202, :253) | **DRAFT** (Amendment 4): stdout joins the CORE-FAULT row and every run's record |
| K11 | MINOR | the fresh-folder rule leaves LAW's place and the working directory open | **CONFIRMED** by the text | **DRAFT:** LAW lies outside the run's folder; the working directory is the run's folder; OUT, RECEIPT and TRACE are names in it |
| K12 | MINOR | R8's exception covers the reference only; the arbiter's `run` sets the core's conditions too | **CONFIRMED** (`arbiter.py:136`, `RUN_TIMEOUT = 600`; `:236`, a timeout *"reported as the host's stop, never a dissent"*; `:225-227`, stale files removed) | **DRAFT:** R8's conditions for the core are the arbiter's as shipped. A core run the arbiter stops at its 600 s is recorded in R8's records as EXTERNAL-TERMINATION: a coverage failure where the reference has a result, never a dissent and never agreement |
| K13 | MINOR | exit 5's reading names neither its reader nor its record | **CONFIRMED** by the text | **DRAFT:** an independent reader, a fresh agent with no part in writing the core, as the re-reads are. Its record lists every exit-5 site and the fallible call guarding it, and shows by lines that no panic hook, alloc-error handler or other path reaches exit 5. The core's author's word is not the reading |
| K14 | MINOR | a harness-caused end other than the 60 s kill is unclassed | **CONFIRMED** by the text | **DRAFT:** the harness starts the core in a process group of its own (on Windows, `CREATE_NEW_PROCESS_GROUP`), so a console's Ctrl-C does not reach it. If the experiment itself is interrupted, the whole experiment run is void and is run again from the start. No single case's run is ever voided, so no end can be set aside one at a time, and his rule stands as he put it: *"Any termination not caused by the harness is a core fault."* |
| K15 | MINOR | the exception-type rule's edges | **CONFIRMED:** with a note, the last stderr line is the note; a bare `raise AssertionError` prints no `:`; a module's exception is qualified | **DRAFT:** the type is not parsed from a traceback. The reference's runner (K3) catches every exception at its top level and writes, as its last stderr line, `REFERENCE-EXCEPTION <module>.<qualname>`, then exits 1. With no such line (the process ended otherwise), the type is `none` |
| K16 | MINOR | stale or missing wording | **CONFIRMED:** `format_check.py:47` (*"its walk (25)"*); draft 4's change table cites section 11 for J10; `stress-texts.txt` says of `s2-doubling-64` *"compared with the reference"* where the sheet says stress evidence only | **DRAFT:** each corrected. `stress-texts.txt` is made again, and Amendment 4 records its new sha256. Amendment 3's row stays as written |

**decoder1's reach on the 10,000 mutants** (OBSERVED here: one process, decode and re-encode only, no interpreter run,
the default recursion limit; scratch `decoder1_reach.py`; not R6's protocol run):

| what decoder1 does | the checker refuses | the checker accepts |
|---|---|---|
| refuses (`DecodeError`) | 6,994 | 0 |
| crashes (`UnicodeDecodeError` 326, `ValueError` 117, `IndexError` 4) | 447 | 0 |
| decodes, and the reference's own writer (`sema.law_bytes`) re-encodes it to the same bytes | 1,984 | 538 |
| decodes, and the writer re-encodes it to other bytes | 37 | 0 |

What this shows:
- **decoder1 is a decoder, not a checker of section 8.** It decodes 2,021 mutants that section 8 refuses: by the
  checker's first failure, W5 893, W8 460, W1 306, W2 107, W10 82, W11 57, W9 32, W6 31, W12 12, W4 3 and W14 1. The
  reference then runs them, as RESULT cases.
- **On those, a core that wrongly accepts and agrees on P passes R6 as written.** Only the falsifier *"an accepted
  non-canonical form"* could catch it, and it has no judge (K3).
- **The 447 crashes are NO-REFERENCE-RESULT** under Amendment 3's rule. Most are bytes outside ASCII. A core that
  accepts one of them is only recorded.
- **The reference's own writer** can judge canonical form alone. It catches the 37, not the 2,021.

## The questions for the owner

### ASK F1 (K1, K4, K5). Does the walk cover the whole tree?

His fourth point reads: *"Once the checks pass, the subsequent walk covers the entire tree."* Draft 4 says the walk
skips two parts (G8's): the blocks of a chain that fails W5, and an inline statement that fails W7. It also skips a
third, which draft 4 does not name: the children of a clause that has children and no body (K1). Every skip lets an
early line's inline statement be numbered after a part that may or may not be walked, so the report moves across lines
(J1's mechanism; K1's A1–C1; K5's measurement).

| | what it entails |
|---|---|
| **(b) a structure gate** | W5 and W7 become a third gate, after the depth gate and the chain gate. Both can be computed from the parsed lines and the parent links alone, with no walk: which clauses have children, what each If chain's shape is, which absorbed clause each arm or else names, whether an inline body is an inline form. A law that fails either is refused there, the least such line reported, nothing walked. The walk that follows then provably covers every clause: each clause is top-level, or the child of a `while`, `for` or procedure, or the child of a clause one block names, or an absorbed clause its one chain reaches. **G8's skips disappear, and with them every cross-line effect.** K4 is settled (W7, as the checker gives). W11's "procedure clause" and the procedures the walk has met coincide. **What changes:** a law that fails W5 or W7 reports it even where a W6 or W8–W13 failure stands on an earlier line. No law the front end writes fails them (DECLARED). It supersedes G8's adopted rule (*"The walk enters no block that fails W5"*), so it needs his word |
| (a) name the third skip | Draft 5 states it: the children of a clause that has children and no body, absorbed or not, are not entered, numbered or checked. The numbering after any skipped part counts only what is walked, by definition. W11 reads "a procedure clause", and the checker tests procedure clauses by their statement, not by what the walk has met. A1, A2, A4 and C1 are planted. The three skips stay, and so does the cross-line effect, by definition. His fourth point then holds only modulo the skips |

**With either, the gates' order.** Draft 4 put the depth gate before the chain gate. That order is mine, not ruled;
either is "before traversal". Under (b) the order would be: depth, chain, structure, then the walk.

Recommended: **(b)**, in that order. It makes his fourth point literally true. It removes the last mechanism by which
a skipped part renumbers a sound line, and the core's author then implements a walk with no skip at all.

### ASK F2 (K2, K3). In R6, what decides that the core accepted, or refused, a mutant wrongly?

The reference cannot decide it. decoder1 decodes 2,021 mutants that section 8 refuses, and accepts a number with a
leading zero. So R7's plant *"a decoder accepting a non-canonical number"* passes R6 as written, and no other
prediction holds non-canonical bytes (K2). The checker is an executable reading of section 8. But it is, in his word,
evidence and not authority.

| | what it entails |
|---|---|
| **(a) section 8, read by hand, on every disagreement with the checker** | The core's verdict on each mutant is compared with the checker's: accepted, or refused with W and line. Every mutant where they differ goes to an independent re-reader, who decides against section 8's text which is right. A core found wrong fails R6. A checker found wrong is a checker finding, and any ambiguity in section 8 goes to the owner. The checker only selects what is read; the document decides. A correct core and a correct checker agree on all 10,000, so each disagreement is a defect somewhere, and the number read by hand is the number of defects. This also compares two independent readings of section 8's (line, W) on 9,462 refused mutants: R6's real power |
| (b) the checker decides | A core verdict unlike the checker's fails R6. Mechanical, but it makes the checker the authority for R6, against his word |
| (c) the reference decides what it can | The reference's own writer judges canonical form (it catches 37 mutants); decoder1's refusals decide the rest; whatever it decodes is compared on P. The 1,984 decodable mutants section 8 refuses, and the 447 crashes, are never judged, and R7's decoder plant still passes |

**And with any of them, R2b.** A fixed, hashed set of canonicity twins: for each of the 298 laws and each kind of
break that applies (a leading zero, two spaces between items, an uppercase hex digit in a float literal, `\u{41}` for
`A`, a non-canonical `\u{…}`), one byte string with that one break, and section 8's (W, line). The core must refuse
each with that W and line. R7's list gains R2b and R6. That catches the decoder plant deterministically, whatever R6's
mutants hold.

**With any of them, the runner (DRAFT).** The program that runs the reference is written now and fixed by its sha256:
- for R6, decoder1's `decode`, then the interpreter, with the law seal the sha256 of the mutant's bytes, the trace on,
  under the mutant budget;
- it catches only `decoder1.DecodeError`, and prints `REFUSED <str(e)>` with exit 0: that message is the one
  REFERENCE-REFUSED compares;
- every other exception takes K15's line and exit 1.

decoder1's class on each of the 10,000 is then recorded, by that runner, in a hashed file before the experiment.

Recommended: **(a), with R2b**.

## One note on the re-read itself

**Its disclosed slips.** Its first `git status --porcelain=v2 --untracked-files=all` printed the names of the untracked
files under `research/law-sufficiency/`. One `find … -not -path "./research/law-sufficiency/*"` descended into that
folder, and its filter printed nothing from it. It opened, read and grepped no file there. HEAD and the repository were
unchanged at its end, and are unchanged here (`2e9805a`; `src/`, `tests/` and `vectors/` as committed). Recorded, not
repeated.

## What follows his answers

1. **LAW-FORMAT-0 draft 5:** every DRAFT item and F1, each change marked with its finding. Drafts 0–4 and the five
   re-read reports stay as they are.
2. **`format_check.py` and `plant_reverts.py` amended to match**, run twice with every law still accepted:
   - F1's gate, or the third skip named;
   - W11 against procedure clauses;
   - K16's comment.

   New plants:
   - K1's four laws (A1, A2, A4, C1);
   - K4's three;
   - K6's two;
   - under F1(b), one law per structure failure that the gate reports before an earlier phase-6 failure.

   The chain gate is undone without a crash, and an undone checker's crash is counted apart.
3. **SHEET.md Amendment 4:** F2, K7–K15's wording, and the files they fix, each made twice with identical bytes:
   - the reference runner;
   - decoder1's classes on the 10,000;
   - R2b's twins, if he rules for them;
   - `stress-texts.txt` made again (K16).
4. **A fresh independent re-read** of draft 5, the checker and Amendment 4.
5. **No core code** before its findings are resolved.
