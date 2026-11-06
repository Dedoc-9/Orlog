# REREAD-9, reader 1 of 3: the format, the checker and the 91 challenge, its report word for word (2026-10-31)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-9 ran
as three readers working at the same time, under the owner's authorization (RULINGS.md, "REREAD-9 authorized"):
reader 1 the format, the checker and the 91 challenge; reader 2 the protocol, the runner, and the evidence and its
keeping, with the hash closure; reader 3 the rulings and cross-document consistency. Each started fresh, had its own
scratch folder and its own letter for findings (NA, NB, NC), and saw nothing of the others' work.

**Its brief** is `work/rust-core/reread-9/briefs/brief-1.md`, sha256 `c2025877bdb2aab523bc0e33fa6254af08048f19c437f4812320535fc8a0235e`, kept in `kept/`; the reader was given only
its path and sha256, and told to check the hash before following it. The brief pinned 34 files by sha256, among them
draft 9 (`86716702…`), SHEET.md (`883888d7…`, Amendments 8 to 12) and RULINGS.md (`f8bc6d6f…`), and told the reader:
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to change nothing in the repository, in the owner's words *"Do not change the checker, runner, reference, laws,
  gate, or release files"*, and to run git read-only;
- to write only under its own scratch folder, run at most two processes of its own at once, never run mutant 09729
  through the reference, and write no absolute path or account name in its report.

No pinned file changed while the readers worked (`work/rust-core/reread-9/record.jsonl`, append-only, kept in
`kept/`). Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-9, reader 1 of 3: the format, the checker and the 91 challenge

Brief: `work/rust-core/reread-9/briefs/brief-1.md`, sha256 `c2025877bdb2aab523bc0e33fa6254af08048f19c437f4812320535fc8a0235e`. I checked that hash first and it matched. HEAD is `2e9805aaa1ceeae0beb443d527680796b66f39c7`.

## The deeper line (Q1.3)

**I found no valid front-end law with a line deeper than 91.**

- **What I searched:** 41 families of deep texts and a randomized search, all through `orlog.front.compile_bytes`. The front end was run and never edited.
  - About 53,900 texts in the families.
  - 77,000 random and hill-climbed texts.
- **What I found:** the deepest line any search reached is 91. Eight families reach it. All are a Fix/Int comparison under an Unless, or under an otherwise-if after an Unless, or in a block statement under an Unless.
- **What that means:** a search shows no maximum. The upper bound rests on the argument (part 2 of Q1 below). I read that argument against `syntax.py` and `sema.py` and found that each of its three steps holds. Two sentences in step 3 are worded loosely (NA4).

## 1. What I read and ran, and what I could not check

**Pinned files.** Every file the brief pins matched its sha256 before I read it. I checked again at the end:
- no pinned file changed;
- `git status --porcelain -- src tests vectors` printed nothing;
- no `__pycache__` appeared under `research/rust-core/`.

**The order I followed.** I did the blind search first, and read only:
- `SPEC.md` §1–§5;
- `src/orlog/front.py`, `syntax.py`, `sema.py` and `lower.py`;
- draft 9's W14(c) count rule (section 8, the lines from "W14, depth" to the end of the count's words).

To find that rule I ran one `grep -n W14` over draft 9. It printed some one-line mentions elsewhere in the draft, but no line of the derivation. After the search I read:
- `LAW-FORMAT-0-DRAFT-9.md`, whole;
- its diff against draft 8;
- `format_check.py`, `plant_reverts.py`, `depth_probe.py` and `run_format.py`, whole;
- the three evidence records the brief names (`-9-zb`, `-9-zb-reverts`, `depth-9-zb`);
- `RULINGS.md` from "REREAD-8's dispositions ruled, G to L" to its end;
- `RULING-SHEET-2026-10-31.md`;
- the ZA5–ZA9 rows of `REREAD-8-DISPOSITION.md`;
- last, `W9-VERIFICATION-REPORT.md` and `-2.md`, after I had formed my own view.

**Disclosure.** Before starting, I opened part of a notes file the agent environment keeps outside the repository. It summarises this project's history up to the law-sufficiency rulings of 2026-10-30, and holds nothing on depth or W14(c). I stopped reading it once I saw what it was. I read nothing under `research/law-sufficiency/`; the checker's `main()` imports from it and I ran it. I read nothing else under `work/`.

**What I ran** (all with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, from the root, TEMP and TMP set to my scratch folder):
- `format_check.py`, `plant_reverts.py` and `depth_probe.py`, once each. Each stdout, with line ends normalised, is byte-identical to the body of its pinned record. **MEASURED.**
- My own search scripts and probes (section 5).
- I did not run `run_format.py`, because it writes into `evidence/`.

At most two of my processes ran at once. No process failed to start, and there was no WinError 1450. One smoke run of my random search had a generator that grew trees exponentially. I stopped it, then checked that no process of mine was left running.

**What I could not check:**
- the 10,000 R6 mutants and the 1,558 R2b twins under the checker (I read only the records' headers and tails);
- anything that runs the reference;
- any core.

## 2. Verdict

In my part, draft 9 and its checker hold. I found **no BLOCKER and no MAJOR**, and seven MINOR findings.

- **The 91 bound.** It survives an independent search, and its argument survives a step-by-step reading against the code. It is still REASONED, not proved by a search.
- **The checker.** It implements G (E2 followed literally), L3's W9 enumeration, his rulings A to D, and R1 and R4, as draft 9 states them. Where it does a little more or less than the table's words, no verdict changes (NA6).
- **Plants.** All 113 plants are caught. 69 of them change under some undoing, and each of G's, RS's and ZA5's plants bites under its own undoing.
- **Wording that is out of date or inaccurate:**
  - the checker decides W3 by writing back, against W3's row (NA1);
  - M10's count is stale, and half of its check is vacuous (NA2);
  - draft 9 points to records made on an earlier text of itself (NA3);
  - step 3 of the argument is worded loosely (NA4);
  - a stop's printed count is left to guess (NA5);
  - the checker's comment on ZA5 is mislabelled (NA7).

## 3. Answers

### Q1, the 91 challenge

**1. The search, made blind to the argument.** Each family was swept over its parameters. The deepest valid line each reached (law-line depth by W14(c)'s count, MEASURED):

| family | deepest |
|---|---|
| Say, left-associative chain | 65 |
| Say, parentheses alone | 4 |
| Say, parentheses around a chain | 65 |
| **Unless condition: k levels of `(…) as an integer + 1.5` over an Int chain, the comparison promoting** | **91** (k=23, chain 15) |
| If condition, same | 90 |
| Unless then Set (store promote) | 90 |
| top-level Set | 89 |
| Define, `unless` proviso | 89 |
| Define value | 89 |
| `the sum of` phrases nested | 65 |
| phrase inside parentheses, converted | 79 |
| `the integer part of the sum of …` | 79 |
| list-literal item | 88 |
| `not` chain | 67 |
| `it is not the case that` chain | 67 |
| minus chain | 65 |
| `item (…) of` nested | 65 |
| `item … of` a Fix list, then `as an integer` | 68 |
| `followed by` chain | 13 |
| otherwise-if arm | 90 |
| **otherwise-if after an Unless** | **91** |
| Unless then claim, must, increase item, append | 90 each |
| postfix conversion chain | 65 |
| `is not less than` under an `and` spine | 67 |
| **Unless condition under an `and` spine** | **91** |
| inline otherwise Set | 90 |
| parentheses inside a string | 4 (not counted) |
| For bounds | 88 |
| While condition | 89 |
| **`rounded to an integer` levels** | **91** |
| `as a float as an integer` levels | 88 |
| **`is not less than` at the top** | **91** |
| **`and` chain, deep on the right** | **91** |
| `followed by` in Say | 88 |
| Say a Fix sum | 89 |
| **claim with `given`, under Unless** | **91** |
| `the larger of` phrases in parentheses | 79 |
| **`Decimals are floats`, Unless** | **91** |

- **Randomized search:** typed random trees over SPEC §4's grammar, in 14 statement forms, each with 500 random trees and 5,000 hill-climb steps (seed 1). It reached only 50, so it is weak evidence beside the families.
- **Refusals met:** only EXPRESSION-DEPTH and TYPE.
- **The two limits that stop every family:** the tree's 64 and the nesting's 24.

**2. The argument, step by step against the code** (REASONED, with the MEASURED edges above):

- **Step 1 (the tree has at most 64 nodes on a path): holds.**
  - `syntax.py:412` checks `ast_depth(st) > 64` on every statement, the inline statements and the RawIf included.
  - `ast_depth` (`syntax.py:79-92`) counts every node.
  - Every law expression form is one node to one parenthesis level (`sema.py:513-542`).
  - An absorbed arm's condition and body are checked in their own clause, whose RawIf node stands where the parent's `(if` stands.
- **Step 2 (wrappers): holds.**
  - Nodes added after the check:
    - Unless's `Un("not")` and the IfS (`syntax.py:283-288`);
    - promotes (`sema.py:295-298`, used at `:308`, `:317`, `:320`, `:471`);
    - nothing else (I searched every constructor).
  - The law-only forms are `(clause`, `(arm`, `(else`, `(given`, `(over`, the oracle and `(block`. Only the first three can lie on an expression's path.
  - `(if` stands for the RawIf node. A define's `unless` builds its `not` inside the parser (`syntax.py:672`), so it is counted.
- **Step 3 (at most 24 promotes): holds.**
  - Between two promotes on a path, an Int node must stand over a Fix or Float node. The only such nodes are `as`/`rounded` to an integer and `integer part of`, because every Int binary has Int operands (`sema.py:311-322`, `:385-389`).
  - Their operand ends in an atom: a postfix conversion applies to an atom (`syntax.py:799-821`), and `integer part of` takes a unary.
  - The next promote's parent is a binary (or a list), which stands inside a parenthesis or is a phrase's own node. Either way its operands sit one nesting level deeper, because `atom()` always calls `nest()` (`syntax.py:823-828`).
  - So at most 23 such atoms are nested, plus the topmost promote.
  - A phrase can never be converted without parentheses: its last operand takes the postfix (`syntax.py:939-942`). So phrases cost more, not less, which is why those families reach 79.

  I found no wrapper the argument leaves out, no node added after the check beyond the two it names, no promote standing elsewhere, and no atom that holds an operator without a nesting level. The loose wording is NA4.

### Q2, E2 followed literally

**Yes, on all three counts.**

- **First define alone.** The rule's type comes only from its first define in clause order (`format_check.py:1101-1102`).
- **Self-using first define.** It is found from the first defines' values alone, by an explicit stack (`:795-807`), and gets no type whatever its form gives (`:1094-1095`).
- **A promote's own parts.** Its operand-is-Int and target-is-Fix-or-Float parts are made wherever it stands (`:822-831`). Only its place waits for the type the place needs.
- **My own probes** (`<scratch>/e2_probes.py`, MEASURED, 6 of 6 agree with my reading of the words):
  - a three-rule cycle: W10 at line 3;
  - a self-use inside an `item` index: W10 at line 4;
  - a self-use only in the proviso, so typed by the value: W9 at line 3;
  - a first define underived, later defines typed apart: W10 at line 3;
  - a list-typed first define, typing the rule as a list: W9 at line 3;
  - an indexed set on an Int variable with a promote value: W9 at line 4.
- **Plants bite** (reproduced, MEASURED):
  - the two self-use plants bite under "a self-using first define typed by its form";
  - the first-define plant bites under "a rule typed by its first derived define";
  - the two promote plants bite under "a promote's parts gated by its place";
  - the no-crash plant bites only by a crash, under both undoings together, as draft 9 says.

### Q3, W9's parts and his rulings (A) to (D), R1 and R4

**My view, formed before reading the reports.** Every form of section 4 that takes a W9 part is in the table with a "needs" column, and every part matches the checker:

| form | checker lines |
|---|---|
| binaries | `:885-899` |
| unaries | `:900-910` |
| conversions | `:863-867` |
| promote | `:822-833` |
| `item`, `length`, `list-of` | `:915-935` |
| `list` | `:936-945` |
| statements | `:994-1121` |

His rulings in the checker:
- **(A):** no part on ⟨type⟩ alone (`:906`).
- **(B):** a part of the pair (`:892`, `:895`).
- **(C):** an unmet variable is undeclared and underived (`:962-964`).
- **R1:** an out-of-scope variable keeps its type (`:965-967`).
- **(D):** the first declaration met keeps the id (`:974-976`).
- **R4:** the written id is the declared id (`:969-978`). The witness gives W10 at line 3 (MEASURED).

The table's words decide every verdict. Where the checker does a little more or less than the table's parts, no verdict changes; I bring these back as NA6.

**Where I differ from the verifiers.**
- They found 0 disagreements at the ruled switches. I agree.
- They noted D5 and R5 as residues that decide no verdict. I agree, and add two more of that kind (NA6).
- Their R2 has since been applied: the cycle sentence of derivation 17 no longer says "least fixed point".
- They did not look at W3 or M10, which were outside their scope (NA1, NA2).

### Q4, the test additions and the wording

- **ZA5's six plants bite, each by its own undoing (MEASURED):**
  - musts and claims: W8 line 3 becomes W8 line 5;
  - `+`, `not` and `list-of`: W9 line 3 becomes W10 line 3;
  - `item`: W9 line 4 becomes W10 line 4.
- **They change no verdict.** "ZA5" occurs in `format_check.py` only in the PLANTS entries (`:1659-1676`). No reading code names them; the E1 counters date from draft 8. REASONED. The R6 and R2b records name the same checker sha (`2965ed15…`); I took that as DECLARED and did not re-run them.
- **The wording:**
  - E1, each kind numbered on its own: stated (draft 9:533-536).
  - E4, the operation count unbounded: stated (:104-106, :407-410), with ZA7's extension withheld as he ruled (see NA5).
  - W3's pointer: stated (:589), though it conflicts with the checker's method (NA1).
  - The writer plants' scope: stated in his words (:910-911).
  - D5: stated (:645, :651). R5: stated (:647).

### Q5, his B1 requirements, and what an author would still guess

All four are stated:
- **termination:** section 5 (:340-360). I checked the perform measure: W11 with W6 gives P < Q, because between Q and a clause of its body there is no top-level clause. REASONED.
- **budget preservation:** :412-431.
- **explicit stacks:** :117-122 and :374-376.
- **detected exhaustion against external termination:** :883-887 and :951-973.

**Still a guess:** NA5, whether a stop's printed `<ops>` is unbounded.

## 4. Findings

**NA1 (MINOR). W3's row says the opposite of what the checker does, and section 11 admits it.**
- **Where:**
  - draft 9:589: "a reader decides W3 by the spacing rule itself, never by writing back";
  - draft 9:1002: "the checker decides W3 by writing back";
  - `format_check.py:557-558`: `written = … w_stmt(…)`, `need(written == rest, 3, …)`.
- **Evidence:** reading the code (REASONED). The iff stated in the row holds for this checker's W2, so no verdict differs on the 305 laws. MEASURED: 305 of 305 pass, as stated. But the checker's W3 is not independent of its writer, which is exactly what ZA9 asks of the core.
- **Proposal:** in the row, say "the core decides W3…". In section 11, state that the checker alone decides W3 by writing back, and why that is acceptable for evidence. Any change to the checker waits for his ruling.

**NA2 (MINOR). M10's count is stale, and its "fell" half is vacuous.**
- **Where:**
  - `plant_reverts.py:400-401` tests that the count line does not end in "304 of 304";
  - the label at :403 reads "the 304 laws' write-back count";
  - draft 9:1106-1107 says "falls to 0 of 304".
- **Evidence:** the run prints `BITES: 0 of 305` (MEASURED). On the unbroken checker's own line ("305 of 305"), the fell test is `True` (`<scratch>/m10_vacuous.py`, MEASURED). So the check now bites only through its "run fails" half (:402).
- **Proposal:** correct the draft to 305. When he allows `plant_reverts.py` to change, compare against the count of laws actually read.

**NA3 (MINOR). Draft 9 points to records made on an earlier text of itself.**
- **Where:** draft 9 names `evidence/rust-core-depth-9.txt` (:731-732), `-format-9-reverts.txt` (:1097), and `-format-9.txt` with `-depth-9.txt` (:1155-1156).
- **Evidence:** `rust-core-format-9.txt` records draft 9's sha as `12d95962…`, not the pinned `86716702…`. Its body differs from `-9-zb`'s only on that line. The other two bodies are identical to the `-9-zb` ones (MEASURED by diff). The records made on the pinned text are the `-9-zb` ones, which `run_format.py` writes (Amendment 12).
- **Proposal:** name the `-9-zb` records as draft 9's evidence, and keep the `-9` ones as history.

**NA4 (MINOR). Step 3 of the argument for 91 is worded loosely; the conclusion stands.**
- **Where:** draft 9:744-747.
- **Evidence (MEASURED, `<scratch>/step3_words.py`):**
  - "whose operand is an atom" is not always true: `(x + 1) as a float as an integer` is accepted, and the conversion's operand is another conversion.
  - "An atom that holds a binary operator is a parenthesis or a phrase" is not literally true: `Let L be a list of i + 1 copies of 2.` is accepted.
  - Neither breaks the step. A postfix chain ends in an atom, a `list-of` is a list and is never converted, and every atom costs a nesting level.
- **Proposal:** "…whose operand ends, through any further postfix conversions, in an atom; every atom costs one nesting level, so the binary that holds the next promote sits at least one level deeper."

**NA5 (MINOR). A stop's printed count is left to guess.**
- **Where:**
  - draft 9:104-106 says whether "a stop's printed count" is unbounded "is not decided here";
  - section 10:879 prints `STOPPED-BY-HOST after <ops> …`, and `<ops>` is the operation count that section 5 makes unbounded.
- **Evidence:** reading only (REASONED). A clean-room author cannot tell whether to print the unbounded count or a u64. No run reaches 2^64 within the time limit, so no outcome depends on it.
- **Proposal:** bring it back to him together with ZA7's withheld counters. Until he rules, section 10 says the printed `<ops>` is the operation count as section 5 defines it, or marks it open in the same words as section 0.

**NA6 (MINOR). Two places where the table's words do not say whether a part is made; no verdict changes either way.** Brought back, not resolved by me.
- **Case 1, a promote's place at a slot with no element type.** For an indexed `set` or `change`, or an `append`, on a variable that is not a list (e.g. Int), the checker makes the place part and fails it (`format_check.py:1002-1013`, `:1110-1113`, `place(None, True)`). D5's words make the value part only for a list (draft 9:632, :645, :651).
- **Case 2, a list literal whose every item is a promote.** Place 3's "with at least one item not a promote" (:703-704) is not checked on each promote; only the list's own part fails (`:938-942`).
- **Why no verdict changes:** in each case a W9 failure stands on the same line (MEASURED: `<scratch>/e2_probes.py` P6 gives W9 line 4; `<scratch>/r4_witness.py` gives W9 line 3).
- **Proposal:** a sentence in the table saying whether these parts are made, or that no verdict depends on it.

**NA7 (MINOR). The checker's comment mislabels ZA5.**
- **Where:** `format_check.py:1659`: "(adopted as test corrections under E1 and E2)".
- **Evidence:** his words: *"Record them as test additions under ZA5, preserving their provenance and their status as non-semantic changes."*
- **Proposal:** correct the comment at the next checker change he authorises. Draft 9's own wording is right.

## 5. Files I created

All of them are under `<scratch>/`; nothing in the repository was written.
- **Code:**
  - `measure.py`: W14(c)'s count over `compile_bytes` and the law;
  - `families.py`, `families2.py`: the 41 families;
  - `random_search.py`;
  - `step3_words.py`, `e2_probes.py`, `r4_witness.py`, `m10_vacuous.py`.
- **Outputs:**
  - `families-out.txt`, `families2-out.txt`, `random-1.txt`;
  - `deepest.orl`: one of the 91-deep texts, from family D;
  - `random-deepest-1.orl`;
  - `fc-run1.txt`, `fc-run1-lf.txt`, `fc-run1.err`;
  - `pr-run1.txt`, `pr-run1-lf.txt`, `pr-run1.err`;
  - `dp-run1.txt`, `dp-run1-lf.txt`, `dp-run1.err`;
  - `fc-evidence-body.txt`, `pr-evidence-body.txt`, `dp-evidence-body.txt`: the evidence records without their `#` lines;
  - `draft8-9.diff`.

## 6. Appendix: commands and outputs

Every Python run used the prefix `TEMP=<scratch> TMP=<scratch> PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, from the root.

- **Hashes.** `sha256sum` of the 36 pinned files and `decoder1.py`: every one as pinned (`decoder1.py` `3584f565…`). `git rev-parse HEAD`: `2e9805aaa1ceeae0beb443d527680796b66f39c7`. `SPEC.md` `27dfff0c…` and `RUNTIME-SPEC.md` `0bd571d6…`, matching draft 9 section 0.
- **`<scratch>/families.py`** (41,004 texts, about 38 s). The deepest lines are in the table above, ending with:
  > `DEEPEST OVER ALL FAMILIES: 91, family D unless cond, conv+promote, params (23, 15)`

  Its line: `(clause 6 0 (if (arm 6 (not bool (< bool (lit fix 6442450944) (promote fix (as int (+ fix …` with 23 promote and `as int` levels over 15 Int additions.
- **`<scratch>/families2.py`** (12,900 texts):
  > `DEEPEST OVER THESE FAMILIES: 91, family BC rounded to an integer, params (23, 15)`
- **`<scratch>/random_search.py 1 500 5000`:**
  > `refusals met: {'EXPRESSION-DEPTH': 15289, 'TYPE': 4987}`
  > `DEEPEST: 50 in unless then increase x`
- **`research/rust-core/format_check.py`:** exit 0, about 10 s.
  > `FORMAT CHECK (DRAFT 9) HELD: 305 of 305 laws pass, 305 written back exactly, derivations equal on 305; plants 113 of 113 caught, 0 not run`

  `cmp` with the body of `evidence/rust-core-format-9-zb.txt`: identical.
- **`research/rust-core/plant_reverts.py`:** exit 0, about 19 s.
  > `M10 undone: the writer appends a byte  the 304 laws' write-back count  BITES: 0 of 305`
  > `PLANT REVERTS HELD: 69 plants and fixtures, 69 changed by at least one undoing, 4 of them only by a crash`

  `cmp` with the body of `-9-zb-reverts.txt`: identical.
- **`research/rust-core/depth_probe.py`:** exit 0, about 23 s.
  > `D1 MEASURED: the limits held at their edges 4 of 4, the deepest line's own edges 2 of 2; the deepest law line found is 91`

  `cmp` with the body of `depth-9-zb.txt`: identical.
- **Diffs of the `-9` records against the `-9-zb` records:**
  - format: one body line differs, `LAW-FORMAT-0-DRAFT-9.md sha256 12d95962…` against `86716702…`;
  - reverts and depth: bodies identical.
- **`<scratch>/e2_probes.py`:** P1 W10 line 3; P2 W10 line 4; P3 W9 line 3; P4 W10 line 3; P5 W9 line 3; P6 W9 line 4. All agree with my expectations.
- **`<scratch>/r4_witness.py`:**
  > `R4 witness W10 line 3 (rule 'q' used before its last define)`
  > `every item a promote W9 line 3 (every item of a list literal is a promote)`
- **`<scratch>/m10_vacuous.py <scratch>/fc-run1-lf.txt`:**
  > `plant_reverts' fell test on it: True`
- **`<scratch>/step3_words.py`:**
  > `(clause 2 0 (let 1 "L" (list-of (+ int (var 0) (lit int 1)) (lit int 2))))`
  > `(clause 2 0 (say (as int (as float (+ fix (var 0) (promote fix (lit int 1)))))))`

  Both accepted.
- **Final check.** `GIT_OPTIONAL_LOCKS=0 git status --porcelain -- src tests vectors` printed nothing. The same command over the four scripts lists them as untracked (`??`), as the brief says. The pinned hashes are unchanged, and no `__pycache__` exists under `research/rust-core/`.

**Grades.** Runs, counts and hashes are MEASURED here. The analysis of the argument and of the checker's code is REASONED. Ruling texts and the R6 and R2b records are DECLARED.
