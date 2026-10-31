# REREAD-3: the dispositions of its findings (PROPOSED, 2026-10-30; adopted, below)

**Adopted (2026-10-30).** The owner adopted E1(b), E2 as proposed and E3(a), and the twelve document, checker and
sheet dispositions (J6–J17), recorded whole in [RULINGS.md](RULINGS.md). His precisions:
- E1: the depth check is bounded and non-recursive, and the walk covers the whole tree once it passes;
- E2: reference refusals, reference crashes, core faults and operational outcomes are kept distinct, and none is
  silently converted into a successful comparison;
- E3: exit 5's source reading is a narrow classification rule, not a claim that every memory failure can be caught.

They are applied in draft 4, the checker, and SHEET.md's Amendment 3. The text below is kept as it was proposed.

**Status.** Proposed, not adopted. These dispose of the 17 findings in [REREAD-3-REPORT.md](REREAD-3-REPORT.md), the
targeted re-read of LAW-FORMAT-0 draft 3 (sha256 `4947bdec…`), its checker (`6ae82f52…`) and SHEET Amendment 2.
Nothing changes until the owner rules. He answers ASK E1, E2 and E3. Then:
- draft 4 applies every DRAFT item and E1;
- the checker is amended to match;
- SHEET.md gains Amendment 3 with E2 and E3, and the files those answers fix;
- a fresh targeted re-read follows.

No core code is written before its findings are resolved. In his words: *"No core implementation, `src/` changes, gate
changes, or release changes are authorized. Phase 0 continues."*

**What the re-read found holds** (MEASURED there, and the claims below re-run here):
- **Termination:** the reasoning is complete and right; seven more attempts at recursion or unbounded loops were refused.
- **Budget:** the reference's stop equals section 5's positions on 11 laws at every B, with 0 mismatches, including
  stops inside a While, a performed body and a block, and at do-nothing clauses. No sentence redefines the budget.
- **Explicit stacks:**
  - they are stated as obligations;
  - there is no limit on chains (perform and rule chains of 100,000 accepted);
  - syntactic depth is kept apart from execution nesting;
  - a 300,000-deep tree is refused in 6.5 s, linear in depth;
  - the checker raises no recursion limit.
- **The protocol:** `s3-budgets.txt` reproduced byte for byte, and recomputed from the sheet's words with 0 rows
  differing.

**What it found wrong, by area:**

| | findings |
|---|---|
| the walk's depth bound (H2) | **J1 (MAJOR)**: the cap changes the reported (line, W). My proof that it does not was wrong |
| the protocol | **J2–J5 (MAJOR)**: R5 fails a correct core; R6 is unfixed; S1 misses a load refusal; two class boundaries rest on unfixed evidence |
| the document | **J6 (MAJOR)**: the stores list omits the law's own, and one sentence promises what his correction forbids |
| the checker and wording | eleven MINOR findings, J7–J17 |

**The report's count is right:** 0 BLOCKER, 6 MAJOR (J1–J6), 11 MINOR (J7–J17), 17 in all. By re-read, the findings
have run 17 (F), 19 (G), 15 (H), 17 (J).

**Which findings are mine:**
- **J1:** my equality proof. It considered failures *of* skipped parts, and missed walked parts whose ids depend on
  them. The inline statements of an If's later arms are written on the If's line, but walked after its block.
- **J6:** the sentence that ends *"so that a law cannot drive the core to such an end"*. It promises what his second
  correction forbids, a second time after H1.
- **J12:** the taxonomy the draft and the sheet do not share.
- **J14:** the generator records the OS once.
- **J2:** RUST-CORE-0's R5, which I wrote and he accepted.

**How each finding was checked.** Each concrete claim was run again here, read-only.
- **The checker's claims** ran through `format_check.read`.
- **J1's "whole tree" reading** ran through a copy of the checker with its cap removed in memory, every W14(a) failure
  still collected.
- **The reference's claims** ran in a process without the checker, at the default recursion limit.

| | severity | finding | re-run here | disposition |
|---|---|---|---|---|
| J1 | MAJOR | phase 3's cap at 25 changes the reported (line, W), and draft 3 says it does not | **CONFIRMED** on all four laws. The capped walk gives W8 line 3, W14 line 27, W8 line 3, W8 line 3; the whole tree gives W14 line 27, W8 line 3, W14 line 27, W14 line 27. The control at depth 23 is accepted both ways | **ASK E1** |
| J2 | MAJOR | R5's falsifier ("a receipt") fails a correct core | **CONFIRMED.** E16a and E16b: ops 2, B = 1, COMPLETED with a receipt. `self_store.orl`: ops 14, B = 7, stopped after 9 | **ASK E2** |
| J3 | MAJOR | R6's seed value, mutation procedure, budget and decoder1's identity are unfixed; a reference refusal has no class | **CONFIRMED.** `grep seed\|decoder1 SHEET.md` gives lines 94, 123, 161 and 170, with no seed value and no path or sha256 | **ASK E2** |
| J4 | MAJOR | S1's falsifier does not fail a load refusal at the depths where the reference crashes; S1's and S2's texts are unfixed | **CONFIRMED** by the text (SHEET:168, 216-217). The reference's `RecursionError` at 600 was MEASURED again in REREAD-2's re-run | **ASK E2** |
| J5 | MAJOR | RESOURCE-EXHAUSTED rests on the core's own claim; EXTERNAL-TERMINATION on host evidence no standard defines | **CONFIRMED** by the text (SHEET Amendment 2's table). That a panic handler could print the line and exit 5 is Rust's documented behaviour, NOT MEASURED | **ASK E3** |
| J6 | MAJOR | section 0's fallible stores omit the law's; draft3:613-614 overpromises | **CONFIRMED** (draft3:64-66, 580-581, 599, 614) | **DRAFT:** section 0's list becomes "every store whose size depends on the law or the run: the law's bytes and every structure built from them, the explicit stacks, variables, lists, text values, the output buffer and the trace". The sentence ends "so that the law's chains do not cause such ends; where one occurs it remains a core fault" |
| J7 | MINOR | the checker enters no block of a chain that fails W4; the document says W5 | **CONFIRMED.** The inner else naming 99 gives W8 line 3; the document's walk gives W4 line 4 | **ASK E1** (its second part) |
| J8 | MINOR | the mode a decimal literal is judged under is ambiguous | **CONFIRMED** (W6 line 3) | **DRAFT:** a literal is judged under line 2's mode, which the reader has read first, as the checker does; a disagreeing `decimals` clause fails on its own line. Plant |
| J9 | MINOR | the checker crashes on an ⟨n⟩ of more than 4,300 digits | **CONFIRMED** (`ValueError` on a literal, a clause number and a perform target; 4,300 digits is W13) | **DRAFT** (checker): `read` lifts Python's int-string limit while it runs and puts it back after, so it changes nothing else in its process. Plants: 5,000 digits as a literal (W13), a clause number (W1), a perform target (W4) and a label part (W4) |
| J10 | MINOR | the checker is super-linear on many defines of one rule and on many sibling Ifs | **CONFIRMED.** 400, 800 and 1,600 defines take 0.06, 0.44 and 3.42 s; 10,000, 20,000 and 40,000 Ifs take 0.40, 1.17 and 3.87 s | **DRAFT** (checker): the closure by a search from each define; the cycle read off the closure; sibling positions computed once. The closure is quadratic in size as a stored set, so quadratic time is the floor there |
| J11 | MINOR | H5's plants do not test the string and escape rules | **CONFIRMED.** An escaped quote, then 131 `(` inside the string: accepted, count 3 | **DRAFT:** that line as a byte fixture (accepted), and its twin with the `(` outside the string as a plant (W14) |
| J12 | MINOR | the draft and the sheet name the stop and the unstable core differently | **CONFIRMED** (draft3:595, 603-604, 629-630; SHEET:197, 203, 214-215) | **DRAFT** (in Amendment 3 and draft 4): one taxonomy. "A compared outcome (COMPLETED, REFUSED, STOPPED)" in the sheet's coverage and no-pass rules; "in class or in result" in the draft; UNSTABLE-CORE a class of a case, not of a run |
| J13 | MINOR | the protocol does not require fresh output paths | **CONFIRMED** by the text | **DRAFT** (Amendment 3): each run in a fresh empty folder, its listing recorded before and after |
| J14 | MINOR | edges of "the reference as shipped" | **CONFIRMED.** `arbiter.py:330-335` runs `Interp` in its own process. `gen_s3_budgets.py` records `platform.release()` once. `classify` takes any two crashes as one | **DRAFT** (Amendment 3): R8 measures the arbiter as it ships, in its own process, and says so. Every experiment's run records `platform.platform()` from its own process. `s3-budgets.txt` stays as it is: its values are what Amendment 2 fixed, and its header is a record. What a crash must share is in **ASK E2** |
| J15 | MINOR | the budget's derived sentence omits the inline arm and else check; the do-nothing check is untested | **CONFIRMED** by the text | **DRAFT:** the sentence names the check before an inline arm or else statement too. Amendment 3 adds an R7 plant, "no check before a do-nothing clause", caught on a fixture whose last clause is a `procedure`, a `define` or a `decimals` |
| J16 | MINOR | SPEC points the author to `sema.py` for the law's bytes | **CONFIRMED** (SPEC.md:284, 410) | **DRAFT:** section 0 adds that for the author the law's bytes are defined by this document, whatever SPEC §9 and §11 items 61–62 say |
| J17 | MINOR | stdout and a LAW path equal to an output path are unsaid | **CONFIRMED** by the text | **DRAFT:** the core writes nothing to stdout, and anything there contradicts its row. LAW equal to OUT, RECEIPT or TRACE, compared as strings, is a usage error |

## The questions for the owner

### ASK E1 (J1, J7). What does phase 3 walk, when the tree is too deep or a chain is malformed?

His second qualification reads: *"W14's existing clause-tree depth restriction must be checked before any unbounded
recursive traversal."* Draft 3 computed depth first, but then walked a capped tree and collected every W4–W13 failure.
The walk numbers ids. So skipping a deep subtree renumbers what comes after, and the report moves (J1).

| | what it entails |
|---|---|
| **(b) W14(a) and (b) as a gate** | Phase 3 begins with W14(a) and (b), computed from the parent links without recursion. If any clause fails, the least such line is reported as W14, and no W4–W13 check is made. The walk then runs only on trees at most 24 deep, so it is whole, and no equality claim is needed. It changes the precedence only for laws that fail W14(a) or (b): one with an earlier W4–W13 failure now reports W14. No text the front end accepts is such a law. This is the literal reading of his words, and it is what a core can do most simply: check depth, then walk |
| (a) the capped walk as the definition | The failure set is defined as that of a walk that enters no clause deeper than 25, its numbering included. The equality claim and its proof are deleted. The checker already does this. A core must reproduce the cap's renumbering exactly |

**And J7, with either:** a chain that fails W4 has none of its blocks walked, as the checker does. Today the document
says only W5. The checker's rule is the simpler one to implement: a chain whose structure is not whole is not entered.
It extends G8's adopted rule, *"The walk enters no block that fails W5"*, by W4. The document then says plainly that a
skipped part changes the walk's numbering after it, by definition.

The other way is for the checker to walk the blocks of a W4-failing chain whose clauses exist. That keeps G8's words, but
the core would have to walk a half-formed chain.

Recommended: **(b), with J7's extension**. Plants: J1's four laws (W14 line 27 under (b)) and J7's law. J7's law gives
W8 line 3, by the definition, with a note on why.

### ASK E2 (J2, J3, J4, J14). The predictions the sheet has not fixed: R5, R6, S1, S2, and what a crash must share

His third correction: *"The time limit, repeat count, and classification rules must be written into the sheet before
experiments begin."* These four predictions are not fixed yet, and R5 as written would fail a correct core.

| | recommended |
|---|---|
| **R5** | At B = ⌊ops / 2⌋, where ops is the count of the text's RESULT run under its own budget (texts of 2 operations or more), the core gives the reference's class and result: STOPPED with the same count and trace, or COMPLETED or REFUSED with the same P and trace. The values are fixed now in a hashed file, `r5-budgets.txt`, made as `s3-budgets.txt` was. (E16a and E16b complete at B = 1, and a correct core must too.) |
| **R6** | The 10,000 mutants are fixed now as a hashed file. A generator names in its header: the seed's value, the four operators with 2,500 mutants each, the source law bytes (the 298), the budget (COMPAT-0's mutant budget, 1,000,000), and decoder1's path and sha256. The reference gains the class **REFERENCE-REFUSED**: both runs refuse with the same code. The outcomes: (i) both refuse: agreement. (ii) The core refuses and the reference has a RESULT: recorded "refused", as his condition 3 allows. (iii) **The core accepts and the reference refuses: a falsifier.** (iv) Both accept: compared as R3–R5. The checker's verdict on each mutant is recorded beside them, as evidence only |
| **S1, S2** | Their texts are made by a generator and fixed by sha256. S1's falsifier: at any depth, any class but COMPLETED, or an output or count other than the constructed one (a chain of n gives ops n + 1). "A crash" in any falsifier means CORE-FAULT. Each stress prediction's own falsifier applies whatever the reference's class |
| **What a crash must share** | A reference crash reproduces when both runs end with the same exit status and the same exception type (the last line of the traceback names it). Otherwise the case is UNSTABLE. (The other way, "any two crashes", is what `gen_s3_budgets.py` does now; no S3 text crashed, so `s3-budgets.txt` is the same under either) |

Recommended: **all four as put**. They are written before any experiment, as his correction requires. R6's and S1's
falsifiers become stricter, and R5's becomes correct.

### ASK E3 (J5). What evidence decides RESOURCE-EXHAUSTED against CORE-FAULT, and EXTERNAL-TERMINATION against CORE-FAULT?

| | what it entails |
|---|---|
| **(a) none from the host; the core's exit 5 read in its source** | No host evidence is admissible on the host the milestone runs on (Windows). So every end the harness did not cause is CORE-FAULT. A list for another OS needs a ruling before it is used. The milestone adds one condition: a reading of the core's source, recorded before R1–R8 count, that exit 5 is reached only from a failed fallible allocation (the `try_reserve` family), never from a panic handler or any other path |
| (b) admissible host evidence listed now | A list per OS of what counts as the host's act: an out-of-memory kill record in the system log, say. Each needs a probe to show it can be read and is not forged by the core. More work, and more room for an end to be filed as the host's |

Recommended: **(a)**. It applies his *"must never award a pass merely because execution stopped"* most strictly. An end
nobody can attribute fails, and the one class the core declares itself is checked at its source.

## One note on the re-read itself

**Its disclosed slip.** It redirected one run of the checker to a second file in its own scratchpad, beyond the one file
its brief allowed. That file lies outside the repository, and the re-read compared it with the evidence and nothing more.
`git status` and HEAD were unchanged at its end, and are unchanged here (`2e9805a`; `src/`, `tests/` and `vectors/` as
committed). Recorded, not repeated.

## What follows his answers

1. **LAW-FORMAT-0 draft 4:** every DRAFT item and E1, each change marked with its finding. Drafts 0–3 and the four
   re-read reports stay as they are.
2. **`format_check.py` amended to match**, running twice with every law still accepted:
   - E1's gate or cap;
   - J7's rule and the children record;
   - J8, J9 and J10.

   New plants:
   - J1's four laws and J7's law;
   - J8's law;
   - J9's four;
   - J11's twin.

   New byte fixture: J11's accepted line.
3. **SHEET.md Amendment 3:** E2 and E3, J12–J15's wording, and the files E2 fixes. Those are `r5-budgets.txt`, the R6
   mutants, and the S1 and S2 texts, each made twice with identical bytes.
4. **A fresh targeted re-read** of draft 4's changes, the checker and Amendment 3.
5. **No core code** before its findings are resolved.
