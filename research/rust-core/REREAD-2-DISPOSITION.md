# REREAD-2: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted these dispositions with C1(a) and C2(a), and with three precision rulings
(recorded whole in [RULINGS.md](RULINGS.md)):
- the budget is stated by its exact check positions and nothing beyond them (H1);
- syntactic depth is kept apart from execution nesting (H2);
- operational outcomes are kept honest, and never pass because execution stopped.

He also required that the evidence records keep no reference result, unstable, core fault, recognized resource
exhaustion and external termination apart. They are applied in draft 3, the checker, and SHEET.md's Amendment 2. The
text below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 15 findings in [REREAD-2-REPORT.md](REREAD-2-REPORT.md). That
report is the targeted re-read of LAW-FORMAT-0 draft 2 (sha256 `f3b6c2a0…`) and of its checker (`b59c221c…`). Nothing
changes until the owner rules. He answers ASK C1 (H3) and ASK C2 (H4). Then:
- draft 3 applies every DRAFT item;
- the checker is amended to match;
- SHEET.md gains Amendment 2 with his answers;
- a fresh targeted re-read follows.

No core code is written before its findings are resolved (his condition 5). He also said: *"No core implementation,
`src/` changes, gate changes, or release changes are authorized yet."*

**What the re-read verified, as he required.** In his words: *"termination reasoning, budget preservation,
explicit-stack requirements, and the distinction between detected resource failure and external process termination"*.
Its answers:

| | its answer | finding |
|---|---|---|
| termination reasoning | true. No accepted law runs without end: ten attempts at recursion, each refused, and a bound past 2^62 refused. The argument is a sketch, and its measures are unstated | H10 (MINOR) |
| budget preservation | the check's positions, the counting and the stop's report equal `interp.py:132-154`. One sentence of draft 2 redefines the budget for compound statements | **H1 (MAJOR)** |
| explicit stacks | stated as implementation obligations. No nesting limit on `perform` or rule uses in the document, the sheet or the checker: the checker accepts chains of 100,000. The obligation is worded loosely | H11 (MINOR) |
| detected vs external | kept apart in the document. The sheet's catch-all files the core's own crashes under external termination, and leaves the reference's run conditions open | **H3, H4 (MAJOR)** |

Further findings outside those four:
- **H2 (MAJOR).** The clause-depth walk recurses without bound before W14(a) refuses the law.
- **Eight MINOR findings:** H5–H9 and H12–H14.

**How each finding was checked.** Each concrete claim was run again here, read-only, by two scratch scripts.
- The reference's claims ran in a fresh process that never imported the checker, once at Python's default recursion
  limit and once at 20,000.
- The checker's claims ran through `format_check.read`.
- Where a finding cites wording, the text cited was read in the file.

**The report's count is right this time:** 0 BLOCKER, 4 MAJOR (H1–H4), 11 MINOR (H5–H15), 15 in all. By re-read, the
findings have run 17 (F), 19 (G), 15 (H).

**Four of the findings are mine:**
- **H1:** I wrote the sentence that redefines the budget, against his first correction (*"Do not redefine the budget
  in prose."*).
- **H2:** my G9 disposition bounded the parser and did not look at the walk.
- **H12:** I dropped lines of draft 1's section 10 when I rewrote it.
- **H13:** I made the section 11 lists.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| H1 | MAJOR | draft:295-297 says a statement that begins with ops ≤ B "runs to its end". The reference stops inside a While, a For, a Perform and an If's block | **CONFIRMED.** `While n < 100` (fuel 200) under budget 10 is `STOPPED-BY-HOST after 11 counted operations (budget 10)`. Its last event is `3 A 3…`, inside the body, at clause 3 (§2.1). Unbudgeted it is `COMPLETED ops 404` | **DRAFT:** replace the two sentences with the re-read's. Between two checks nothing stops the run. One statement's expressions, its rule uses included, run to their end. A While, a For, a Perform and an If's block run their bodies as sequences, so the check is made again before each clause of them, and the run can stop inside them. His part 3, *"Work inside one statement may exceed the budget by an arbitrary amount"*, is then read as the work no check position separates. That reading is the code's, which his part 3 also orders preserved *"exactly"* |
| H2 | MAJOR | phase 3 walks clause depth without bound before W14(a) refuses; the checker crashes, and a recursive core would too | **CONFIRMED.** 9,000 nested Whiles: `W14 line 19` (11.6 s). 11,000 nested Whiles: `RecursionError` (17.6 s). 11,000 nested If blocks: `RecursionError` (8.2 s) | **DRAFT:** phase 3's walk enters no clause deeper than 25, so it is at most 25 deep, and depth and loop count are computed from the parent links, not by recursion. The reported (line, W) is unchanged. Every skipped clause is a descendant of a clause 25 deep, which fails W14(a) on its own earlier line, and every line the table gives a failure of a skipped part is later still. **Checker:** depth computed in one linear pass (`depth[k] = depth[parent] + 1`; parents come first), and the walk capped. Plants: 30,000 nested Whiles (W14 line 19) and 30,000 nested If blocks (W14 line 27) |
| H3 | MAJOR | Amendment 1's catch-all ("any other way that gives none of the exit statuses above") classes the core's own panics and aborts as external termination, never a disagreement | **CONFIRMED** by the text (SHEET Amendment 1). That a Rust panic exits 101 and a stack overflow or an infallible allocation's failure aborts is Rust's documented behaviour, NOT MEASURED: no core exists | **ASK C1** |
| H4 | MAJOR | Amendment 1 leaves open the reference's recursion limit, Python version and process isolation, a core whose two runs differ, R6's "never hangs past the budget", and S3's sampler | **CONFIRMED.** The perform chain of 600 is `RecursionError` at the default limit 1,000, and `COMPLETED ops 601` at 20,000. The chain of 300 completes at both. The reference sets no limit of its own: `grep setrecursionlimit src/` finds nothing. `format_check` sets 20,000 on import (line 35) | **ASK C2** |
| H5 | MINOR | W14(c)'s count is undefined on unbalanced lines | **CONFIRMED.** `(clause 1 0 ))` + 131 `(` + 129 `)` + `)` is W2 line 3. `(clause 1 0 )` + 131 `(` + 130 `)` + `)` is W14 line 3 | **DRAFT:** define it as the checker counts. Take the running count of `(` minus `)` outside strings, from the line's first byte. A string opens at `"` and closes at the next `"` not escaped. Inside a string, `\` skips the next byte. The line fails W14 if the count ever exceeds 130. Plants: both laws |
| H6 | MINOR | `remove-last` on a For counter is W9 in the checker; the document's W8 forbids it | **CONFIRMED.** `remove-last` is `W9 line 4: remove-last on int`, while `append` is `W8 line 4` | **DRAFT** (checker): the W8 check added to `remove-last`, as `append` has it. Plant |
| H7 | MINOR | an absorbed clause named by two Ifs through blocks is reported at the absorbed clause's line | **CONFIRMED.** `W5 line 4: clause 2 is named by two blocks`. Collected: `(4, 5, …)` and `(6, 5, 'absorbed clause 2 is named twice')` | **DRAFT** (checker): a clause named by two blocks fails on the later If's line, the document's attribution. Plant |
| H8 | MINOR | the checker checks a promote's place against a type left underived | **CONFIRMED.** `W9 line 3: a promote where SPEC §5 puts none`. With a define of `r` first, it is accepted | **DRAFT** (checker): no placement check when the other operand's type is underived (section 8, phase 3). Plant (W10 line 3) |
| H9 | MINOR | W14(c)'s derivation omits the Unless `not` in its sum | the arithmetic: an Unless condition is 63 + 32 + 1 = 96 deep, wrapped 3 times, 99. An inline statement is 62 + 31 + 4 = 97 | **DRAFT:** the sums by place. 99 and 130 stand |
| H10 | MINOR | the termination argument is a sketch; "2^63" | the For loop runs `while k <= hi` with a break at `hi` (`interp.py:234-241`), so −2^63 … 2^63−1 is 2^64 iterations | **DRAFT:** the three sentences proposed (procedure ids decrease along performs; a used rule's last define comes before the using define; every repetition counts an operation, so uncounted work between counted ones is bounded by the law's length and the list and text bounds). Also: expressions hold no `perform`. 2^64 |
| H11 | MINOR | the explicit-stack obligation is worded loosely | read | **DRAFT:** "A law may nest them to any depth, and a reader must run it". The host call-stack depth is bounded by a constant from W14's bounds alone, never by a chain of performs or rule uses, so a rule use inside an expression must be evaluated without host recursion. The stores held to fallible allocation are listed once: stacks, lists, text values, output, trace |
| H12 | MINOR | section 10 lost lines of draft 1, and leaves edges open | **CONFIRMED** against draft 1's section 10. Lost: LAW's line, "RUNTIME-SPEC §6's output, receipt and trace paths", "The trace is written as events happen", `<k>`/`<n>` and "`<reason>` is free text, which no comparison reads", the usage error's causes. SPEC.md:453 says the stop is where *"the law said nothing"* | **DRAFT:** restore every lost line. Exhaustion may end any stage from reading LAW on, at the stage where it happens. Running out of memory while reading LAW is RESOURCE-EXHAUSTED, not IO-ERROR. Files: TRACE as far as written, never a RECEIPT, and whatever was written stays. Paths are compared as the strings given. Each stderr line ends with one LF. The stop's kind is "budget (host)", as B1 part 4 lists *"budget result"* apart |
| H13 | MINOR | section 11's lists and the checker disagree; docstrings are stale | **CONFIRMED.** G5's third law, `(else 99 (perform 1))` after a procedure, is `W4 line 5`, correct, and not planted. The fixture list omits the two B1 chains. The plant list omits G7's two. Docstrings: `format_check.py:14` says "draft 1's sections", 21 says "298 laws", 26-27 speak of the parser | **DRAFT:** the lists made equal to the checker; the third G5 plant; the docstrings corrected |
| H14 | MINOR | W10's line column names three of its failures | **CONFIRMED.** An `(over 2)` naming a later clause that is no define is `W10 line 3`, the define's line | **DRAFT:** "every other W10 failure: the line holding the define", as W4 gives the line holding the reference. It is said as the exception to "a relation belongs to the later line", which governs only failures of two parts that fail only together (two types, two Ifs) |
| H15 | MINOR | section 0 names SPEC.md and RUNTIME-SPEC.md without sha256; "(SPEC §6)" cites the wrong item | **CONFIRMED.** `27dfff0c…6de5` and `0bd571d6…ec35`. SPEC.md:204 (§6) says the clause of the statement that used the rule. SPEC.md:341, §11 item 18, says an absorbed arm's condition carries its own clause id | **DRAFT:** both sha256s; cite item 18 |

## The questions for the owner

Both amend the comparison protocol his third correction fixed before testing (*"The time limit, repeat count, and
classification rules must be written into the sheet before experiments begin."*). No experiment has run, so either
answer still comes before testing.

### ASK C1 (H3). What is an end of the core that no row of section 10 gives?

Amendment 1 classes every such end as external termination, and an operational outcome is *"never a semantic
disagreement"*. So a panic (101), a host-stack overflow or an aborting allocation in the core counts only against
coverage, and nothing says coverage must be full. The core could crash on every deep law and still meet R3–R5.

| | what it entails |
|---|---|
| **(a) a core-fault class and full coverage** | A **core fault** is any end the harness did not cause that is no row of section 10, or whose files or stderr contradict its row (exit 0 without a receipt, say). A core fault falsifies the prediction under test (R3–R6, S1–S4). External termination keeps only two ends: the harness's own kill, and an end the harness attributes to the host with recorded evidence. R3–R5 also require full coverage: on every case whose reference class is RESULT, the core gives a language outcome. Any operational outcome there fails the prediction **as a coverage failure**, never as a disagreement. So a core that runs out of memory, or past 60 s, where Python gave a result fails the milestone |
| (b) the core-fault class, coverage reported only | As (a), but R3–R5 hold on the cases covered, and the coverage is stated beside them. Weaker: a core that gives up where Python does not still meets R3–R5 |
| (c) Amendment 1 as it stands | A core's crash is never counted against it. Not recommended |

Recommended: **(a)**. It keeps his rule that an operational failure is never a semantic disagreement. It also stops
the core's own crashes, which section 0 forbids by its explicit-stack obligation, from being filed as the host's.

### ASK C2 (H4). Under what conditions does the reference run, and what fills the protocol's other gaps?

S1's perform chain of 600 is `RecursionError` at Python's default recursion limit, and `COMPLETED ops 601` at 20,000
(MEASURED here, CPython 3.14.5, one host). So that case's class depends on a setting the sheet does not name.

| | what it entails |
|---|---|
| **(a) the reference as it ships** | Each reference run in a fresh `python -B` process, with `PYTHONHASHSEED=0`, Python's default recursion limit and thread stack (the reference sets none), never importing `format_check`. The Python version and the platform recorded with every run. Depth 600 is then NO REFERENCE RESULT (both runs crash), and the core's outcome there is stress evidence only |
| (b) a raised limit | As (a), but the reference runs with a recursion limit the sheet names (say 20,000, as the checker sets). More of S1 becomes comparable, but the reference is measured under a setting it does not ship with, and a deep enough chain crashes all the same |

With either, the same amendment fills three gaps:
- **A core's two runs that differ** in class or in result are an UNSTABLE core, a falsifier.
- **R6's "never hangs past the budget"** becomes "never exceeds the core's time limit where the reference's class is
  RESULT". Under B1 part 3 a hang "past the budget" names nothing.
- **S3's sampler:** one `random.Random(20261030)`, drawn through the 298 texts in the order of their ids. Per text, every
  B from 0 to its operation count when there are at most 20, else `sample(range(ops + 1), 20)`, sorted. A text whose
  reference class is not RESULT is listed, not sampled.

Recommended: **(a)**. It measures the reference the owner made the authority, as it is. His scope note already calls
the recursion failure *"reference implementation defect/limitation, not a language restriction"*.

## Two notes on the re-read itself

- **Its disclosed slip.** One sweep (its C9a) used a directory filter that failed on Windows separators. So it may have
  opened `.orl` texts under `research/law-sufficiency/`, against its brief. It printed nothing from them, kept only
  counts, discarded the run, and re-ran with a correct filter (C9b). No finding rests on the first run. The texts there
  are laws, not the decoders. The exclusion keeps the re-read apart from LAW-SUFFICIENCY's decoders, and D1 binds the
  core's author, not a re-reader. Recorded, not repeated.
- **What it could not run.** `format_check.main()` imports its corpus from `research/law-sufficiency/` (`common`,
  `closure_tests`, lines 1280-1281), so the brief's exclusion kept it from re-running "304 of 304". It re-ran every
  fixture and all 44 plants on 222 laws of its own sweep instead: all caught, derivations equal. The next re-read's
  brief may let it run `run_format.py` without reading those files.

## What follows his answers

1. **LAW-FORMAT-0 draft 3:** every DRAFT item above, each change marked with its finding. Drafts 0–2 and the three
   re-read reports stay as they are.
2. **`format_check.py` amended to match**, running twice with every law still accepted. The changes:
   - the linear depth pass and the walk capped at 25 (H2);
   - the W8 check on `remove-last` (H6), the later If's line (H7), and no placement check on an underived type (H8);
   - the docstrings (H13).

   New plants:
   - 30,000 nested Whiles and 30,000 nested If blocks;
   - H5's two laws, H6, H7 and H8;
   - G5's third law.
3. **SHEET.md Amendment 2:** his answers to C1 and C2, written before any experiment.
4. **A fresh targeted re-read** of draft 3's changes, the checker and Amendment 2.
5. **No core code** before its findings are resolved.
