> **A tokened copy, not the original hand-back** (2026-10-31, his ruling on REREAD-9's ASK 9-2): each spelling of the home folder's path is replaced by a token, `⟦HOME⟧` or `⟦HOME83⟧`; the original is kept outside the repository and named in `kept/TOKENED.txt` by its length and sha256, and `kept_tokens.py restore` gives it back exactly with the prefixes. After this line and the blank line below it, the file is the kept tokened bytes exactly, so its line numbers are the original's plus two.

# REREAD-8, reader 1 of 3: the format and the checker, its report word for word (2026-10-30)

Saved as returned by the reader, a fresh general-purpose agent with no part in writing anything it read. REREAD-8 ran
as three readers working at the same time, under the owner's F2 (RULINGS.md): reader 1 the format and the checker,
reader 2 the protocol, the runner and the evidence, with the hash closure of `r6-reference-5.txt`, reader 3 the rulings
and cross-document consistency. Each started fresh, had its own scratch folder and its own letter for findings (ZA, ZB,
ZC), and saw nothing of the others' work. Each was briefed:
- to check, before reading, the sha256 of every file it read against the brief's pins, among them draft 8 (`94a989a6…`),
  SHEET.md (`b9a3057e…`, Amendment 7 with the record `r6-reference-5.txt`, `636a2873…`) and RULINGS.md (`387ef2e8…`);
- never to open, read, list or grep anything under `research/law-sufficiency/`;
- to write only under its own scratch folder in the system's temp directory, run at most two processes of its own at
  once, and change nothing in the repository; reader 2 was told not to run mutant 09729, which commits about 24 GiB.

Its report follows, unedited, taken from its own transcript rather than retyped.

---

# REREAD-8, reader 1 of 3: the format and the checker (findings ZA1 to ZA9)

## 1. What I read and ran, and what I could not check

**Pins.**
- All 24 pinned files hash to the brief's sha256 values.
- `research/law-sufficiency/decoder1.py` hashes to `3584f565…`.
- HEAD is `2e9805aaa1ceeae0beb443d527680796b66f39c7`.

**Read whole:**
- `LAW-FORMAT-0-DRAFT-8.md`, and its diff against draft 7. Every change in the diff is in draft 8's change table.
- `format_check.py`, `plant_reverts.py`, `depth_probe.py` and `run_format.py`.
- RULINGS.md, sections "REREAD-7's dispositions adopted, A to F" and "The R6 remake".
- `REREAD-7-DISPOSITION.md`.

**Read in part:**
- SHEET.md: section 6, and Amendments 6 and 7.
- `src/orlog/syntax.py` (sha256 `ad4e3bc5…`): the limits, `ast_depth`, the statement and expression parsers, and where Unless's `not` is added (:284).
- `src/orlog/sema.py`: where promotes are inserted (:295–321, :471).
- `src/orlog/interp.py`: how `ops` and the claim costs are counted.
- SPEC.md and RUNTIME-SPEC.md: their hashes match draft 8 §0; I read only the lines I grepped.

**Ran.** All runs from the repository's root, with `PYTHONHASHSEED=0 PYTHONUTF8=1 python -B`, TEMP and TMP pointed at my scratch folder, Python 3.14.5, Windows.
- `format_check.py`, `plant_reverts.py` and `depth_probe.py`, each twice. Each pair was byte-identical, and each output equals the body of its evidence record exactly (the record's four header lines aside).
- I did not run `run_format.py`, because it writes into `evidence/`.
- Six scripts of my own, all read-only (section 5).
- Never more than two processes of mine at once (`plant_reverts.py` and its one child). No process failed to start.

**Could not check, or not mine:**
- Any core: none exists.
- `ref_run*.py`, `gen_r6_reference.py` and `r6-reference-5` (reader 2's part).
- `rust-core-r6-checker-8.txt` and `rust-core-r2b-checker-8.txt`: not regenerated. I only diffed their rows against the `-7` records: 0 lines differ in each.
- REREAD-7's reader reports: not pinned, not read.
- The upper bound of 91 in Q4 is REASONED, not measured.

**Disclosure.** My first command was a whole-tree `git status --porcelain=v2 --untracked-files=all`. Its output listed the names of untracked files under `research/law-sufficiency/`. I opened, read and grepped none of them, and every later `git status` was limited to paths. My scripts import `common` and `closure_tests` from that folder, as `format_check.py` does, which the brief allows. The repository is unchanged: no tracked change and no `__pycache__`.

## 2. Verdict

**Not yet.** Draft 8 states rulings A to F in text. The evidence reproduces exactly and twice. The six new plants bite, each by its own undoing. 130 is kept.

**E2 is not implemented as stated, and its text contradicts itself.** Four MAJOR findings:
- ZA1: the checker types a rule by its first *derived* define, against derivation 17's "first define". The same fallback crashes the checker on a 4-clause law.
- ZA2: derivation 17's parenthetical, and his E2 words, contradict section 8's "the type its form gives it". The checker follows section 8.
- ZA3: the checker skips a promote's own two W9 parts whenever its place is underived.
- ZA4: W9's parts are not enumerated, so the checker's split is a guess.

**Five MINOR findings:**
- ZA5: no plant pins E1 for claims and musts, or W9's parts outside set and change.
- ZA6: E1's wording reads as one counter shared by all three kinds.
- ZA7: E4 overrides SPEC's `u64` without saying so.
- ZA8: D1's probe misses a reachable 91-deep line.
- ZA9: the writer's extent, and section 8's W3 row.

No BLOCKER. ZA2 needs his ruling. ZA1, ZA3 and ZA4 are corrections to the text and the checker, each with a plant.

## 3. Answers

### Q1, the writer plants (his A)

**Section 10 requires it.**
- Draft 8:781–784: *"W3 is decided by code that does not call the writer that produces OUT"*, followed by his words *"W3 must be determined by code independent of the writer used to produce `OUT`"*.
- It says a load refusal never counts as catching a plant, and that neither plant is ever declared equivalent.

**Section 0 (:110–122) establishes OUT's provenance as his points 1 to 5 state.**
- It records his point 4's three facts: each atom decoded and re-encoded under section 3; no slice of the input reaches OUT; *"W3 does not call the writer"*.
- It carries point 5: the reading is recorded before R2 counts, and a copy path or a writer-dependent W3 fails R2.
- Point 3's *"the result comes to me"* is in SHEET.md Amendment 7 (:770), not in draft 8, which is enough.

**Can a core meet the text and still escape both plants? I found no such core (REASONED).**
- An echoing core has no writer to plant, so the plant changes nothing and R7 fails.
- A core whose W3 calls its writer meets the plant as a load refusal, which does not count.
- A "decoy" core runs its writer, but writes the input bytes whenever they equal the writer's output. It catches both plants, because a planted writer differs from the input and so its output is written. It is caught only by the source reading ("no slice reaches OUT"). That is his *"Neither substitutes for the other"*, working as designed.

**What is left (ZA9):**
- The text fixes neither the plant's site in a core's copy nor how far "the writer" extends. A plant placed in code that W2's canonical-escape check also calls would make a compliant core fail R7: a false failure, not an escape.
- Section 8's W3 row (:539) still reads as "decide W3 by writing back", with no pointer to section 10.

### Q4, D1

**The probe's measurement is what draft 8 says (MEASURED, reproduced twice, byte for byte):**
- the tree limit holds at its edge: 64 accepted, 65 refused;
- the nesting limit holds at its edge: 24 atoms accepted, 25 refused;
- the deepest line over its search is 90;
- the corpus reaches 66, the fixture laws 5.
- 130 is unchanged: `DEPTH_PARENS = 130`, the 130-deep fixture is accepted and the 131-deep plant is refused.

**A deeper text exists: 91 (MEASURED).** The probe always puts its innermost level in parentheses (`depth_probe.py:66–70`).
- In my family the innermost level is `w plus CHAIN`, where CHAIN is an Int conversion chain: promoted under the Fix sum, with no parentheses of its own. The parenthesis saved buys one more level.
- `Unless w is less than (…22 levels…) as an integer, do the following.` with a 15-step chain is accepted by the front end, and its law line is 91 deep.
- The checker accepts it, writes it back exactly, and reads its depth as 91.
- One level more is refused EXPRESSION-DEPTH by the nesting limit; a chain two longer is refused by the tree limit.

**No line deeper than 91 exists (REASONED):**
- A law line's depth is its law-only wrappers, plus the parsed tree nodes on its path, plus the promotes on that path.
- **The tree:** at most 64 nodes, the statement node included (`syntax.py:412`).
- **The wrappers:** at most 3 on a condition's path (`clause`, `arm`, and Unless's `not`, added after the tree check at `syntax.py:284`). At most 2 on an inline statement's path, and 1 on any other statement's.
- **The promotes:** each promote below the topmost one sits under an Int-from-Fix conversion (`as`/`rounded` to int, or `integer part of`). That conversion's operand is an atom (`postfix()` and `unary()`, `syntax.py:789–828`). An atom that holds a binary operator is a parenthesis or a phrase, and each costs one nesting level (`atom()` calls `nest()`, `EXPR_NEST_MAX = 24`). So there are at most 23 enclosing atoms, and at most 1 + 23 = 24 promotes.
- So at most 3 + 64 + 24 = 91, which the witness reaches. Draft 8's 99 ignores what the nesting limit does to the promotes.

So the actual limit is 91 by a witness and an argument, not "between 90 and 99, not established" (ZA8). 130 stays. Tightening to 90 would refuse a law the front end writes.

### Q5, E1 to E4

**All four readings are stated:**
- E1: :484–486, and W8's row (:544).
- E2: derivation 17 (:455), W9's parts (:552–555), and the underived list (:670–679).
- E3: W8's row.
- E4: §5, :373–376.

**The checker implements E1 for variables, claims and musts alike:**
- `declare()` counts every declaration met (`format_check.py:924–927`), and musts and claims are counted the same way (:1015, :1022).
- My witnesses give W8 at line 3. Counting distinct ids gives W8 at line 5.

**The six new plants bite, each by its own undoing (MEASURED):**

| plant | stated | undone |
|---|---|---|
| E1 | W8 line 3 | W8 line 5 |
| E2, a rule typed by its first define | W9 line 3 | W10 line 3 |
| E2, indexed set | W9 line 4 | W10 line 4 |
| E2, indexed change | W9 line 4 | W10 line 4 |
| V4, W14(b) reset at a procedure | W6 line 13 | W14 line 20 |
| V4, a block naming another clause | W5 line 5 | W5 line 3 |

- V5's fixed-width reader moves 3 of J9's 4 plants without a crash.
- 46 of 46 plants and fixtures change under at least one undoing, 3 of them only by a crash.
- Every undoing changes at least one plant except K1's, which the draft says changes none.
- R2's 11 write-back fixtures: each hash checks, and each is accepted and written back exactly.

**E2 is not implemented as stated:**
- ZA1: the first *derived* define, not the first define; and a crash.
- ZA2: the text contradicts itself on a self-using first define.
- ZA3: a promote's own parts are skipped when its place is underived.
- ZA4: W9's parts are not enumerated.

**E4 is stated, but SPEC's `u64` stands unacknowledged (ZA7).**

**Left to an author's guess:** ZA2, ZA4 and ZA6, and how to compute derivation 17 at all (draft 8 gives no method; the checker's repeated walks take quadratic time, ZA1).

### Q7, B1's requirements

**All four are stated, and I re-derived the termination argument (REASONED):**
- Perform ids strictly decrease. A perform at U inside Q's body has P < U, P top-level and P ≠ Q, so P < Q.
- The last define of each used rule strictly decreases.
- Rule values hold no perform.
- Every loop body's first child is a non-absorbed clause, so the budget is checked once per iteration. That is consistent with draft 8's §5 positions and with REREAD-7's X5 (a `while` with no statement fails W5).
- Explicit stacks, fallible allocation and exit 5's reading are in §0.
- Detected exhaustion against external termination is in §10.

**Still a guess for a clean-room author:**
- derivation 17's algorithm, which must stay off the host stack ("bounded by a constant that depends only on W14's bounds") and be fast enough for S1's 30,000-rule chains;
- ZA2, ZA4, ZA6 and ZA7.

## 4. Findings

### ZA1 (MAJOR): derivation 17 is implemented as "the first derived define", and the same fallback crashes the checker

**Where.**
- Draft 8:455: *"the type of its first `define`'s value … underived when that value's type is"*.
- `format_check.py:1050–1052`: `if te is not None: … L.rule_types.setdefault(name, te)`. A define whose value is underived is skipped, so a later define types the rule.
- `format_check.py:1085–1102`: the repeated walks. The comment at :1087 says *"a type once derived stays"*.

**Evidence (MEASURED, `readings.py`).**
- **Law B:** `(clause 1 0 (say (as int (rule "s"))))`, then `(clause 2 0 (define "s" (rule "u") - (over )))`, then `(clause 3 0 (define "s" (lit int 1) - (over )))`.
  - The checker gives W9 line 3: s is typed int by its *second* define.
  - By derivation 17, s is underived (its first define names a rule with no define), so W10 line 3.
- **Law C:** r = `(list-of (lit int 1) (rule "s"))`, s = `(rule "r")`, then r = `(lit int 1)`, s = `(lit bool 0)`.
  - The checker raises `AssertionError: the rules' types did not hold still`. The types cycle with period 4 and never settle.
- **The strict reading, made in a copy:** the rule's type is its first define's (clause order), and W10's one-type check is kept among the derived defines.
  - It moves no plant, no fixture, and no corpus law's outcome or derivations (0 of 304).
  - Law B becomes W10 line 3, and law C W10 line 3.
- **Why the strict reading always settles (REASONED):** a first define's type flows from at most one leaf, through rule uses, variables, `item` and `list-of`. So the rules form a functional graph. Starting from underived, a cycle stays underived, and everything else settles within the number of rules.
- **Time:** the checker's walks are quadratic on a rule chain written as bytes. 0.18 s, 0.68 s and 2.85 s at 500, 1,000 and 2,000 rules (software timings, one run each).

**Proposal.**
- Type each rule by the first define in clause order, underived when that value is, as the text says. Then the comment's bound holds.
- Plant law B (W10 line 3) and law C (W10 line 3, no crash). Undo each.
- Optionally, use the current walk's types for rules already defined in that walk, so that a legal chain settles in two walks.
- Say in draft 8 how derivation 17 is computed without recursion.

### ZA2 (MAJOR): a first define that uses its own rule: derivation 17 and his E2 words against section 8

**Where.**
- Draft 8:455's parenthetical: *"(a first define whose value uses its own rule, directly or through other rules, is one)"*, that is, one whose value's type is underived.
- His E2: *"A first definition that uses its own rule leaves the type underived; the relevant use remains W10."*
- Draft 8:678: *"Every other expression has the type its form gives it (section 4)."*
- The checker follows :678.

**Evidence (MEASURED).**
- **Law A:** `(clause 1 0 (define "r" (as int (rule "r")) - (over )))`.
  - The checker gives W9 line 3. By its form, `(as int …)` is int, so r is int, and `as int` from int fails W9 beside the W10.
  - By his words, r is underived, so W10 line 3.
- The strict patch of ZA1 leaves law A at W9, so this is a separate question.
- Mutual use through two rules, each first define `(as int (rule …))` of the other, gives the same split (REASONED).

**Proposal.** Put it to him.
- **(i) His words govern.** "Uses its own rule" means a mention in the first define's value, followed through other rules' first defines. Such a rule's type is underived, whatever the value's form gives. Section 8's list gains that item, and the checker detects the cycle by syntax. Law A gives W10.
- **(ii) The form governs.** The parenthetical is narrowed to a value whose type flows back to its own rule. Law A stays W9, and his sentence is noted as covering only that case.
- Either way, plant law A.

### ZA3 (MAJOR): a promote's own W9 parts are skipped when its place is underived

**Where.**
- `format_check.py:787–794`: `if promote_to is UNDERIVED: pass` precedes both the target check and `ta != "int"`.
- Draft 8:565: *"`promote`: an int operand; the target is fix or float"*. Each of those parts needs only the promote's own operand or target.
- Draft 8:552–555 requires each part to be made once its own inputs are derived. H8 exempts only *"a promote's place"* (:678).

**Evidence (MEASURED, `parts.py`).**
- `(say (+ float (promote float (lit bool 1)) (rule "r")))`: the checker gives W10 line 3. The text gives W9 (the operand is bool).
- `(say (+ int (promote int (lit int 1)) (rule "r")))`: the checker gives W10 line 3. The text gives W9 (the target is int). Beside a derived int, the checker does give W9 (G4's plant).

**Proposal.** Make both parts whatever the place, and skip only the place. Plant both laws (W9 line 3) and undo each.

### ZA4 (MAJOR): W9's parts are not enumerated, so the checker's split is an author's guess

**Where.**
- Draft 8:556–568 states each rule as prose. :552 says each is a conjunction of parts, but names them only for `item` and an indexed `set` or `change`.
- The checker's split: `UN_RULES` (`format_check.py:81–84`) gives `neg`, `abs` and `sqrt` a result part "⟨type⟩ numeric". The arithmetic split is {⟨type⟩ numeric, a = ⟨type⟩, b = ⟨type⟩} (:847).

**Evidence (MEASURED).**
- `(say (neg bool (rule "r")))`: the checker gives W9 line 3.
- *"a numeric operand of ⟨type⟩"*, read as its two stated conjuncts, both need the operand, so W10 line 3.
- For `+`, a split into {a numeric, b numeric, a = b, a = ⟨type⟩} omits b = ⟨type⟩. Then `(+ int (rule "r") (lit fix 1))` would be W10, where the checker gives W9 (REASONED).

**Proposal.** List every rule's parts, each with the inputs it needs, as the checker now has them, or as he rules. Plant one law per form whose split differs.

### ZA5 (MINOR): no plant pins E1 for claims and musts, or W9's parts outside set and change

**Where.** `plant_reverts.py:147–161`. E1's plant has only variables. E2's whole-or-nothing undoing covers only `set` and `change`.

**Evidence (MEASURED, `readings.py`).** Each of the following undoings, made in a copy, moves 0 plants, 0 fixtures and 0 of the 304 laws:
- musts counted by distinct id, and claims counted by distinct id;
- the whole-or-nothing W9 check in a binary operator, a unary one, `item` and `list-of`.

Each moves its witness law:
- two musts of id 0 in a block, then an inline else's must 1: W8 line 3 becomes W8 line 5 (likewise for claims);
- the binary, unary, `item` and `list-of` witnesses: W9 becomes W10.

**Proposal.** Add these six witnesses as plants, each with its undoing.

### ZA6 (MINOR): E1's wording reads as one counter for all three kinds

**Where.** Draft 8:480 and :484: *"Variables, claims and musts get ids 0, 1, …"* and *"The i-th declaration the walk meets has id i"*.

**Evidence.**
- The checker keeps three counters. `let 0`, `claim 0`, `must 0` is accepted (MEASURED).
- Only appendix A.4 (`let 0`, then `claim 0`, `claim 1`) shows that each kind is counted on its own.

**Proposal.** Say: "each kind numbered on its own: the i-th variable declaration met has variable id i, likewise claims and musts".

### ZA7 (MINOR): E4 overrides SPEC's `u64` without saying so, and the counts derived from `ops` are unstated

**Where.**
- Draft 8:373–376.
- SPEC.md:209: *"`ops` (u64, starting at 0)"*.
- RUNTIME-SPEC.md:177: `uint64_t orl_ops` (`rt.ops: u64`).
- Both are in the core author's reading set.
- The reference's clause costs, claim costs and evaluation counts are Python ints too (`interp.py:139`, :255, :264).

**Proposal.**
- State in §0, as J16 does for the law's bytes, that draft 8's unbounded count governs for the core whatever those lines say.
- Extend it to the cost counters, the claims' costs and evaluations, and the stop's printed count.

### ZA8 (MINOR): D1's probe misses a reachable 91, and 91 is the actual limit

**Where.**
- `depth_probe.py:66–70` and :115–116.
- Draft 8:625–636: *"the actual limit lies between 90 and 99"*.

**Evidence.** Q4: the 91 witness (MEASURED), and its edges refused for nesting and for tree depth.

**Proposal.**
- Record the 91 witness and the argument.
- Have the argument re-read independently. A search cannot prove it.
- If he tightens W14(c), the limit is 91, planted on both sides: the witness's law line accepted, a 92-deep line refused. Never 90.

### ZA9 (MINOR): the writer's extent, and section 8's W3 row

**Where.**
- Draft 8:539: *"Once W2 holds, writing back gives the rest exactly if and only if W3 holds"*. It has no pointer to :781–784.
- Draft 8:117 and SHEET.md:668–678 ("in copies of the core"): neither says what "the writer" covers, or where a plant goes.

**Evidence (REASONED).**
- W2's canonical-escape check is naturally made by re-encoding. The checker does so (`format_check.py:227`).
- The text does not constrain W2, unlike W3.
- A plant placed in an atom encoder that W2 shares would make a compliant core fail R7 by a load refusal.
- The present two plants (a `let`'s name written empty, an `(over …)` list reversed) are structural, so a sensible placement meets them as byte mismatches.

**Proposal.**
- In W3's row: "a reader decides W3 by the spacing rule itself, never by writing back (section 10)".
- Have the source reading name the writer's code, and place R7's writer plants in that code alone, outside any code W2 or W3 calls.

## 5. Files created

All are in `⟦HOME83⟧\AppData\Local\Temp\reread8-1\`.

Scripts, all read-only:
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\deeper.py` (the search for a line deeper than 90)
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\save_witness.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\readings.py` (the E1 and E2 laws, the undoings, the strict reading)
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\parts.py`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\r2fix_and_chain.py`

The witness:
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\witness91.orl`, sha256 `4a8398cc6b357db9205c999976e4ff2a211158c76aaea286906d05af49fc30cd`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\witness91.law`, sha256 `74cd16d5d8edd4e0006a153586a313259dae317b761263a9e727c9892454cce1`

Outputs:
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\fc1.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\fc2.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\pr1.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\pr2.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\dp1.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\dp2.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\deeper1.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\deeper2.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\readings1.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\parts1.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\r2fix1.txt`

The comparison copies, the evidence bodies and my outputs in LF:
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\fc_ev_body.txt`, `⟦HOME83⟧\AppData\Local\Temp\reread8-1\pr_ev_body.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\dp_ev_body.txt`
- `⟦HOME83⟧\AppData\Local\Temp\reread8-1\fc1_lf.txt`, `⟦HOME83⟧\AppData\Local\Temp\reread8-1\pr1_lf.txt` and `⟦HOME83⟧\AppData\Local\Temp\reread8-1\dp1_lf.txt`

Nothing was written in the repository.

## 6. Appendix: commands and outputs

All run with TEMP and TMP set to the scratch folder, `PYTHONHASHSEED=0 PYTHONUTF8=1`, from the repository's root.

**1. The pins.** `sha256sum` of the 24 pinned files: every value matches the brief. `sha256sum research/law-sufficiency/decoder1.py`: `3584f565f6929879…`.

**2. The checker.** `python -B research/rust-core/format_check.py`: exit 0, about 9 s. Its last line:
```
FORMAT CHECK (DRAFT 8) HELD: 304 of 304 laws pass, 304 written back exactly, derivations equal on 304; plants 94 of 94 caught, 0 not run
```
The second run is identical, and both equal `evidence/rust-core-format-8.txt` from line 5 on ("MATCHES evidence body").

**3. The reverts.** `python -B research/rust-core/plant_reverts.py`: exit 0, run twice, identical, equal to the record's body:
```
M10 undone: the writer appends a byte  ...  BITES: 0 of 304
changed only by a crash of an undone checker: H2: 30,000 nested If blocks, ...; H2: 30,000 nested whiles, ...; J9: a 5,000-digit clause number
PLANT REVERTS HELD: 46 plants and fixtures, 46 changed by at least one undoing, 3 of them only by a crash
```
Draft 8's undoings: as in Q5's table. Each undoing's count of plants it changes: every one at least 1, but `K1 undone alone` (0).

**4. The depth probe.** `python -B research/rust-core/depth_probe.py`: exit 0, run twice, identical, equal to the record's body:
- `tree depth: 62 conversions (a tree 64 deep) accepted …`, and 63 refused EXPRESSION-DEPTH;
- `nesting: 23 parentheses (24 atoms deep) accepted`, and 24 refused;
- `deepest found: 90, in an Int compared at the top, clause Unless`;
- `298 texts: deepest law line 66; 6 fixture laws: deepest 5`.

**5. The search for a deeper line.** `python -B deeper.py <root>`, run twice, identical:
```
clause Unless, an Int compared at the top                  deepest 91 at (levels 22, tail 15)
inline Unless, an Int compared at the top                  deepest 91 at (levels 22, tail 15)
clause If, an Int compared at the top                      deepest 90 at (levels 22, tail 15)
an inline Set in an If's arm, the stored value an Int      deepest 90 at (levels 22, tail 15)
a Let's value                                              deepest 89 at (levels 23, tail 15)
  one level more                       refused: EXPRESSION-DEPTH ... expressions nest at most 24 deep ...
  chain two longer                     refused: EXPRESSION-DEPTH ... a statement's expression tree is at most 64 deep
  one level less, chain two longer     accepted, deepest 90
```
The witness's statements, in `prog()`'s header (`§1 Let w be 1.5.`, `§2 Let k be 2.`, `§3 Let b be true.`):
```
§4 Unless w is less than (w plus (w plus … 22 times … (w plus w as an integer as a fixed ×7 as an integer) as an integer) … as an integer) as an integer, do the following.
§4.1 Say 1.
```
Its law line begins:
```
(clause 4 0 (if (arm 4 (not bool (< bool (var 0) (promote fix (as int (+ fix (var 0) (promote fix (as int …
```
22 such levels follow, then `(+ fix (var 0) (promote fix (as int (as fix … 15 conversions … (var 0)` and the closing parentheses, then ` (block 4)) -))`. Its parenthesis count is 91. The full bytes are in `witness91.law`.

`python -B r2fix_and_chain.py <root> witness91.law`, part 3:
```
accepted; written back exactly; deepest line 91
```

**6. R2's fixtures and the rule chains.** The same command, parts 1 and 2:
- `mutant/s1/0026 given reversed: (given 2 1) -> (given 1 2)  sha256 ok  accepted, written back exactly`, and so for all 11 rows;
- `n = 500: 0.18 s`, `n = 1000: 0.68 s`, `n = 2000: 2.85 s` (perf_counter, one run each).

**7. E1 and E2.** `python -B readings.py <root>` (3 min 51 s), section 1:
```
B: first define underived, a later one int; use before both        W9 line 3
C: two rules through list-of, each with a later constant define    CRASHED (AssertionError: the rules' types did not hold still)
A: a first define's value (as int (rule r)) uses its own rule      W9 line 3
A': the same, then a use typed by it                               W10 line 3
W9 part: + int over an underived rule and a bool                   W9 line 3
W9 part: neg int over an underived rule, result bool               W9 line 3
W9 part: item of an int variable, index underived                  W9 line 4
W9 part: list-of with a text value, count underived                W9 line 3
E1 musts: two musts of id 0 in a block, then an inline else's must 1 W8 line 3
E1 claims: the same with claims                                    W8 line 3
E1: a let 0 and a claim 0 and a must 0 (each kind its own count)   accepted
```
Sections 2 and 3, the undoings in copies (plants, fixtures and laws moved, then the witness each moves):
```
E1 musts counted by distinct id        0   E1 musts: W8 line 3 -> W8 line 5
E1 claims counted by distinct id       0   E1 claims: W8 line 3 -> W8 line 5
E2 binary W9 whole or nothing          0   + int over an underived rule and a bool: W9 line 3 -> W10 line 3
E2 unary W9 whole or nothing           0   neg over an underived rule: W9 line 3 -> W10 line 3
E2 item W9 whole or nothing            0   item, index underived: W9 line 4 -> W10 line 4
E2 list-of W9 whole or nothing         0   list-of, count underived: W9 line 3 -> W10 line 3
derivation 17 strictly                 0   B: W9 line 3 -> W10 line 3;  C: CRASHED -> W10 line 3
```

**8. W9's parts.** `python -B parts.py <root>`:
```
promote int beside an underived rule                         W10 line 3 (no define of rule 'r')
promote int beside a defined int (G4's plant, for contrast)  W9 line 3 (a promote where SPEC §5 puts none)
promote float of a bool beside an underived rule             W10 line 3 (no define of rule 'r')
neg bool over an underived rule                              W9 line 3 (neg on None as bool)
+ int over an underived rule and a fix                       W9 line 3 (+ on None and fix as int)
+ bool over an underived rule and an int                     W9 line 3 (+ on None and int as bool)
```

**9. The checker's records against draft 7's.** `diff` of the rows (lines not starting `#`) of `rust-core-r6-checker-7.txt` against `-8.txt`: 0 lines. Of `rust-core-r2b-checker-7.txt` against `-8.txt`: 0 lines. Both `-8` headers name `format_check.py` `3bc07ca8…`, and R2b's reads "agrees on 1558 of 1558".

**10. Greps.**
- `SPEC.md:209`: `` `ops` (u64, starting at 0); ``
- `RUNTIME-SPEC.md:177`: `` a plain public counter `uint64_t orl_ops` (Rust `rt.ops: u64`) ``
- `syntax.py:75–76`: `EXPR_NEST_MAX = 24`, `AST_DEPTH_MAX = 64`
- `syntax.py:284`: `cond = Un("not", st.cond)`, in `_attach_otherwise`, after `statement()`'s check at :412
- `syntax.py:824`: `atom()` calls `self.nest()`

**11. After the work.** `git status --porcelain=v2 -- research/rust-core evidence src` shows no tracked change, and no `__pycache__` stands in `research/rust-core` or `src/orlog`.
