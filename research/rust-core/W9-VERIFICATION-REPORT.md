> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on REREAD-9's ASK 9-2): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# W9's enumeration verified independently (the owner's L3), the verifier's report word for word (2026-10-31)

His ruling L3 on REREAD-8: *"Write down the exact W9 parts and their individual type checks in Draft 9. Then
independently verify that the checker implements that enumeration. Bring back any ambiguity rather than resolving it by
implementation convention."* The verifier was a fresh general-purpose agent with no part in writing anything it read.
It was briefed to build its own decision procedure for W9 from LAW-FORMAT-0 draft 9 (sha256 `5880ca54…`) alone, never
to read the checker's typing code, to use `format_check.read` only as a black box, to implement both readings of the
two open parts, and to bring back every ambiguity with a minimal witness. It wrote only under its own scratch folder
and changed nothing in the repository.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

## Independent verification of draft 9's W9 enumeration (owner's ruling L3)

### 1. What I read and ran, what I could not check, and independence

**What I read** (read-only):
- `research/rust-core/LAW-FORMAT-0-DRAFT-9.md` (sha256 `5880ca54…2e6868`): sections 0 to 8 and 11 to 12, and appendix A (for spelling laws). In section 8 that covers the W9 table, the open parts (A) and (B), the promote places, W8's scope rules, the rows for W6, W10 and W14, phase 4's underived list, and "Which refusal is reported".
- `SPEC.md` §5–§6, for the conversion table the `as`/`rounded` row points to.

**Independence.** I did not open, read or grep `research/rust-core/format_check.py` (sha256 `073b4ebc…63ed`). I used it only as a black box: `import format_check as fc`, then `fc.read(bytes)`, catching `fc.Refused` and reading `.w` and `.line`.

**One disclosure.** At the end I ran `git status --porcelain=v2 --untracked-files=all` to confirm I had changed nothing. It printed the names of untracked files, including file names under `research/law-sufficiency/`. Those were names only; I opened, read or grepped nothing there.

**How I ran things.** Every run was `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B` from the repository root, with TEMP and TMP pointed at the scratch folder. One process at a time. Every process started on the first try.

**Repository state.** HEAD is `2e9805a`. No file was created or changed, and no new `__pycache__` appeared (MEASURED by `find`).

**What I built.**
- `w9decide.py`: an independent decider written from the document alone. It reports accepted, W9 at line n, or W10 at line n. It contains:
  - every part of the W9 table, each made only when the inputs in its "needs" column are derived;
  - the underived list;
  - derivation 17: the first define in clause order, self-using rules found from mentions alone with an explicit stack, other types by a least fixed point;
  - a promote's own two parts made wherever it stands, and its place part not made when the type the place needs is underived;
  - the part of W10 my laws can reach: a rule use with no define or before its last define (the procedure rule included), two types, a list value, a proviso that is not bool, `over` names;
  - least line, then least W.
- Switches: A (`form`/`none`) and B (`alone`/`both`) for the two open parts, and V (`any`/`met`/`scope`) for the ambiguity in finding D1 below.

**What I could not check.**
- Laws that fail another W first. I kept them out by construction; the final runs met none.
- W10 beyond what is listed above (cycles of `over`).
- Deep nesting, `perform` chains, and multi-arm chains beyond a few probes.
- Any run of the core.

### 2. Verdict

Outside the two open parts, the checker implements draft 9's W9 table part for part, with one exception (D1).
- **MEASURED.** It agreed with my decider on every law in which no rule's first define reads a variable declared later in the walk: 258 targeted cases, a 168,596-law exhaustive sweep, and 2,379 laws in floats mode.
- **The exception (D1).** The table's inputs do not say how the type of a variable is read inside a rule's first define when that variable is declared later, and the checker settles it by a convention of its own. Under that convention, read as an added switch in my decider, it agreed on all 300,000 random laws and all 2,970 laws of a sweep built for this case (MEASURED).

### 3. The open parts (A) and (B)

The checker matches the reading the document says it has now, on both. Neither is chosen here; they are the owner's to rule.
- **(A): the checker makes "⟨type⟩ is numeric" for `neg`, `abs`, `sqrt` from the form alone.** The document's witness `(clause 1 0 (say (neg bool (rule "r"))))` gives W9 at line 3. The other reading would give W10. MEASURED.
  - In the sweep, the 72 laws that separate the readings (3 operators × 6 non-numeric types × 4 underived operands) all follow A=form.
  - In the random run, 49 laws are told apart, all A=form.
- **(B): the checker makes an operand's own kind when that operand alone is derived.** MEASURED.
  - `(say (< bool (lit bool 1) (rule "r")))` gives W9 at line 3.
  - `(clause 1 0 (let 0 "l" (list list-int (lit int 1))))` followed by `(clause 2 0 (say (== bool (var 0) (rule "r"))))` gives W9 at line 4.
  - The other reading would give W10 for both.
  - In the sweep, 432 laws separate the readings, all B=alone; in the random run, 128 do.

### 4. Disagreements and ambiguities

**D1 (the main finding; an ambiguity the checker settles by convention).** The question is what type a variable has inside a rule's first define when it is declared after the define.
- **What the text gives.**
  - Derivation 8 (DECLARED): "a let's variable: the type of its ⟨E⟩".
  - The underived list makes underived only "an undeclared variable's type", and never defines "undeclared".
- **Three readings:**
  - (i) undeclared means no clause declares the id. This is the literal text and my decider's default.
  - (ii) undeclared means not in scope at the use, as W8's code UNDECLARED would suggest.
  - (iii) undeclared means not yet declared in the walk at the clause the use is checked at.
- **The checker follows (iii)** (MEASURED):
  - 2,970 of 2,970 in the dedicated sweep, against 2,333 for (i) and 2,333 for (ii);
  - 300,000 of 300,000 random laws, against 299,100 for (i) and 299,277 for (ii);
  - all 900 random disagreements under (i) are this one class.
- **Witness V1**, which separates (i) from (ii) and (iii):
  ```
  orlog-law 0
  (decimals fixed)
  (clause 1 0 (say (neg fix (rule "q"))))
  (clause 2 0 (define "q" (var 0) - (over )))
  (clause 3 0 (let 0 "y" (lit int 1)))
  ```
  The checker gives W10 at line 3. Under (i), q is int and "the operand's type is ⟨type⟩" fails, giving W9 at line 3.
- **Witness V2**, which separates (ii) from (i) and (iii):
  ```
  orlog-law 0
  (decimals fixed)
  (clause 1 0 (say (neg fix (rule "q"))))
  (clause 2 0 (if (arm 2 (lit bool 1) (let 0 "y" (lit int 1))) -))
  (clause 3 0 (define "q" (var 0) - (over )))
  ```
  The checker gives W9 at line 3. Reading (ii) gives W10.
- **Where it can show** (REASONED). Only at a rule used on a line before its first define. Everywhere else, a W8 on the same line or an earlier one masks it.
- **A note.** Reading (iii) is "typing as met" for variables, while section 11 records E2's rejection of typing as met for rules. Derivation 17 also calls its own computation order-free.
- **Proposal.** The owner chooses (i), (ii) or (iii). The underived list then states it, and V1 and V2 become plants.

**D2 (a documentation gap; the checker and I agree).** "Derivation 17, computed" says a non-self-using rule's type is reached "never round a cycle". A cycle through a variable breaks that, and the mention search cannot find it.
- Witness C1:
  ```
  orlog-law 0
  (decimals fixed)
  (clause 1 0 (say (neg fix (rule "q"))))
  (clause 2 0 (let 0 "y" (rule "q")))
  (clause 3 0 (define "q" (var 0) - (over )))
  ```
  The checker gives W10 at line 3, with no crash. That is the least fixed point (underived), and my decider gives the same.
- The same holds through `list-of` and `item` (C2: W10). With the cycle broken by a form such as `abs int`, the checker gives W9 (C3).
- **Proposal.** Correct the sentence, and state that a type that depends on itself through variables is underived.

**D3 (minor; the text is not explicit; the checker follows section 7).** When a variable id is written twice, which declaration gives its type? The checker uses the first declaration met in the walk, keyed by the written id. MEASURED witnesses:
- V3: `let 0` int, then `let 0` fix, then `(define "q" (var 0))`, with the use `(neg fix (rule "q"))` on line 3. The checker gives W9 at line 3: typed by the first let.
- V4: the same with fix first, then int. The checker gives W10 at line 3.
- V6: a misnumbered second let does not declare id 1; `(var 1)` stays underived and the checker gives W10.
- V7: a block's let, written on a later line but met earlier in the walk, wins over an inline else's let; the checker gives W9.
- My first decider took the last declaration. That was my own departure, by implementation convention, and I corrected it from section 7's "the i-th declaration the walk meets has id i".
- **Proposal.** State this in derivation 8.

**D4 (wording).** For a promote standing at none of the three places, the "needs" column names no type.
- The checker makes the place part anyway, and so do I: `(say (promote fix (rule "r")))` gives W9 at line 3 (MEASURED).
- **Proposal.** Write "needs nothing at no place".

**D5 (no verdict depends on it).** For an indexed `set` or `change`, or an `append`, on a variable that is not a list, the table does not say whether the parts naming the element type are made.
- "The variable is a list" fails on the same line, so the verdict is W9 either way (REASONED).
- **Proposal.** Optional wording.

**D6 (wording).** The `as`/`rounded` row says "for the mode and the target". The mode is not the decimals mode.
- In floats mode, all 2,379 laws (conversions, promotes, `+ < ==`, `set`, `append`) agreed with a table that depends only on `as`/`rounded` and the target (MEASURED).
- **Proposal.** Write "for `as` or `rounded`".

### 5. Counts (all MEASURED)

| run | laws | agreement with the checker |
|---|---|---|
| targeted, every table row, hand-annotated | 258 | (form, alone) 258 of 258; (none, alone) 253; (form, both) 254; (none, both) 249. My hand expectations against my decider: 0 mismatches across all four readings |
| exhaustive sweep | 168,596 | (form, alone) 168,596, under both V=any and V=met; (none, alone) 168,524; (form, both) 168,164; (none, both) 168,092 |
| first defines reading variables declared at 10 kinds of place | 2,970 | V=met 2,970; V=any 2,333; V=scope 2,333 |
| random, seeds 0 to 299,999 | 300,000 | (form, alone, met) 300,000; (form, alone, any) 299,100; (form, alone, scope) 299,277; (none, alone) 299,051; (form, both) 298,972; (none, both) 298,921 |
| floats mode | 2,379 | 2,379 |
| extra probes and minimal witnesses | 43 | as quoted in section 4 |

**The sweep's families.**
- `binary`: 138,384, which is 8,649 for each of the 16 operators (9 type annotations × 31 operands × 31 operands).
- `unary` 2,790; `conversion` (as, rounded, promote) 279; `item` 279; `length` 9; `list-of` 961; `list` 124 one-item plus 3,844 two-item; `cat` 961.
- `say` 31; `let` 31; `set` 279; indexed `set` 8,649; `change` 558; indexed `change` 8,649; `if` 31; `while` 31; `must` 31; `claim` 31; `for` 961; `append` 279; `remove-last` 9; inline `set` 279; `define` with each proviso 992; first define 124.
- The checker's verdicts over the sweep: ok 948, W9 163,117, W10 4,531.
- The 31 operands are:
  - a variable of each of the 9 types, and the 5 earlier scalar rules;
  - 5 promotes: good, wrong target, to int, over a bool, over an underived operand;
  - 4 underived: no define, a self-using later define, a first define that is underived, `list-of` over an underived rule;
  - 5 rules typed by a later define, a list type and "the first define, not the second" among them;
  - 3 items.

**The random run** (three statement kinds also had a mistyped `while`/`for` bound or child variant):
- The checker's verdicts: ok 130,139, W9 113,960, W10 55,901.
- Laws containing each form in a test line; every one agrees under (form, alone, met):

| forms | laws containing each |
|---|---|
| `+` `-` `*` `/` `max` `min` | 16,512; 16,478; 16,434; 16,477; 16,394; 16,576 |
| `quot` `rem` | 21,377; 21,371 |
| `<` `>` `<=` `>=` | 6,734; 6,757; 6,744; 6,921 |
| `==` `!=` | 12,938; 13,234 |
| `and` `or` `not` | 12,277; 12,447; 24,151 |
| `even` `odd` | 13,340; 13,380 |
| `zero` `positive` `negative` | 9,046; 9,030; 9,047 |
| `neg` `abs` `sqrt` | 31,357; 31,331; 31,743 |
| `trunc` `as` `rounded` `promote` | 41,974; 68,168; 45,030; 92,259 |
| `item` `length` `list-of` `list` `cat` | 96,747; 63,131; 47,084; 51,455; 27,923 |
| `let` `set` `change` `say` | 43,051; 43,172; 43,373; 139,175 |
| `if` `while` `for` `must` `claim` | 38,735; 38,630; 38,912; 43,191; 43,558 |
| `append` `remove-last` `define` | 42,947; 43,271; 38,401 |

**Superseded runs.** A 200,000-law run with an earlier generator, which had no D1 structure, agreed under (form, alone) on 200,000 of 200,000.

### 6. Files I created

All are in `⟦HOME83⟧\AppData\Local\Temp\w9verify\`. Nothing else was written.
- **Code:** `w9decide.py`, `w9common.py`, `w9targeted.py`, `w9gen.py`, `w9sweep.py`, `w9extra.py`, `w9extra2.py`, `minimal.py`, `minimal2.py`, `run_targeted.py`, `run_sweep.py`, `run_random.py`, `run_fwd.py`, `run_floats.py`, `probe0.py`.
- **Results:** `sweep_binary.json`, `sweep_rest.json`, `random_A.json`, `random_B.json`.
- **Superseded:** `random_0_200k.json`, `pilot.json`, `pilot2.json`.

### Appendix: commands and outputs

The prefix for every command is `TEMP="$W" TMP="$W" PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, with `W='⟦HOME83⟧\AppData\Local\Temp\w9verify'`, run from `⟦HOME⟧\Desktop\Orlog`.

- **`run_targeted.py`:** `cases 258; decider-vs-hand mismatches 0`; then `form/alone 258 of 258`, `none/alone 253`, `form/both 254`, `none/both 249`.
- **`run_sweep.py sweep_rest.json <24 families>`:** `laws 30212 in 57.1s; errors 0; other W {}`, with TOTAL agreement `30212 / 30140 / 30212 / 30140 / 30212 / 30212` for form/alone/any, none/alone/any, form/both/any, none/both/any, form/alone/met and form/alone/scope.
- **`run_sweep.py sweep_binary.json binary`:** `laws 138384 in 172.6s; errors 0; other W {}`, with `138384 / 138384 / 137952 / 137952 / 138384 / 138384`.
- **`run_random.py 0 150000 random_A.json`:**
  - `compared 150000 of 150000 in 290.1s; checker verdicts {'W9': 56907, 'ok': 65015, 'W10': 28078}; other W {}; errors 0`;
  - `form/alone/any 149542`, `form/alone/met 150000`, `form/alone/scope 149648`.
- **`run_random.py 150000 150000 random_B.json`:**
  - `compared 150000 of 150000 in 252.3s; {'ok': 65124, 'W9': 57053, 'W10': 27823}`;
  - `form/alone/any 149558`, `form/alone/met 150000`, `form/alone/scope 149629`.
- **`run_fwd.py`:**
  - `laws 2970`; `V=any 2333`, `V=met 2970`, `V=scope 2333`;
  - every `after-*` position disagrees under (i), and every out-of-scope `before-*` position under (ii).
- **`run_floats.py`:** `floats mode: compared 2379, agree 2379, other {}`.
- **`minimal.py` and `minimal2.py`:**
  - V1 `('W10', 3)`, V2 `('W9', 3)`, V3 `('W9', 3)`, V4 `('W10', 3)`, V6 `('W10', 3)`, V7 `('W9', 3)`;
  - A witness `('W9', 3)`; B witness `('W9', 3)`; B list witness `('W9', 4)`;
  - C1 `('W10', 3)`, C2 `('W10', 3)`, C3 `('W9', 3)`, P1 `('W9', 3)`, P2 `('W10', 3)`.

**Grades.** Every verdict, count and agreement above is MEASURED here, on this host. The classification of each finding, and where D1 can show, is REASONED. What the document states is DECLARED.
